from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)

from .common import (
    PrototypeError,
    b64url_decode,
    b64url_encode,
    canonical_json_bytes,
    require,
    sha256_bytes,
)


CAPABILITY_TYP = "ctde-range-capability+jws"
ENVELOPE_TYP = "ctde-broker-envelope+jws"
AUDIT_TYP = "ctde-audit-attestation+jws"
EVENT_TYP = "ctde-prototype-event+jws"
FORMAL_TYP = "ctde-formal-test-manifest+jws"
PROFILE_VERSION = 1


@dataclass(frozen=True)
class KeyRecord:
    kid: str
    public_key: Ed25519PublicKey
    status: str
    not_before: int
    expires_at: int
    trust_domain: str = "prototype"

    def public_key_hex(self) -> str:
        raw = self.public_key.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw,
        )
        return raw.hex()


class TrustStore:
    def __init__(self, records: list[KeyRecord], trust_domain: str = "prototype") -> None:
        self.records = {record.kid: record for record in records}
        self.trust_domain = trust_domain

    def get_active(self, kid: str, now: int) -> KeyRecord:
        record = self.records.get(kid)
        require(record is not None, "BLOCKED_SIGNED_OBJECT_PROFILE_INVALID", "unknown kid")
        require(
            record.trust_domain == self.trust_domain,
            "BLOCKED_SIGNED_OBJECT_PROFILE_INVALID",
            "trust root mismatch",
        )
        require(record.status == "active", "BLOCKED_SIGNED_OBJECT_PROFILE_INVALID", "key not active")
        require(
            record.not_before <= now <= record.expires_at,
            "BLOCKED_SIGNED_OBJECT_PROFILE_INVALID",
            "key outside validity window",
        )
        return record


@dataclass
class SigningKey:
    kid: str
    private_key: Ed25519PrivateKey
    issuer: str
    status: str = "active"
    trust_domain: str = "prototype"

    @classmethod
    def generate(cls, kid: str, issuer: str, trust_domain: str = "prototype") -> "SigningKey":
        return cls(kid, Ed25519PrivateKey.generate(), issuer, "active", trust_domain)

    def record(self, not_before: int, expires_at: int, status: str | None = None) -> KeyRecord:
        return KeyRecord(
            kid=self.kid,
            public_key=self.private_key.public_key(),
            status=status or self.status,
            not_before=not_before,
            expires_at=expires_at,
            trust_domain=self.trust_domain,
        )


class JWSCodec:
    def __init__(self, trust_store: TrustStore, now: int) -> None:
        self.trust_store = trust_store
        self.now = now

    @staticmethod
    def sign(
        key: SigningKey,
        typ: str,
        payload: dict[str, Any],
        *,
        protected_override: dict[str, Any] | None = None,
    ) -> str:
        protected: dict[str, Any] = {
            "alg": "EdDSA",
            "typ": typ,
            "kid": key.kid,
            "ctde_profile_version": PROFILE_VERSION,
        }
        if protected_override:
            for name, value in protected_override.items():
                if value is None:
                    protected.pop(name, None)
                else:
                    protected[name] = value
        protected_bytes = canonical_json_bytes(protected)
        payload_bytes = canonical_json_bytes(payload)
        signing_input = f"{b64url_encode(protected_bytes)}.{b64url_encode(payload_bytes)}".encode("ascii")
        signature = key.private_key.sign(signing_input)
        return f"{signing_input.decode('ascii')}.{b64url_encode(signature)}"

    def verify(
        self,
        token: str,
        *,
        expected_typ: str,
        expected_issuer: str,
        expected_audience: str | list[str],
        max_ttl: int,
        expected_attempt_id: str | None = None,
        expected_environment: str = "prototype_fixture_only",
        require_common: bool = True,
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        try:
            protected_segment, payload_segment, signature_segment = token.split(".")
            protected = json.loads(b64url_decode(protected_segment).decode("utf-8"))
            payload = json.loads(b64url_decode(payload_segment).decode("utf-8"))
            signature = b64url_decode(signature_segment)
        except Exception as exc:
            raise PrototypeError("BLOCKED_SIGNED_OBJECT_PROFILE_INVALID", "malformed JWS") from exc

        require(isinstance(protected, dict), "BLOCKED_SIGNED_OBJECT_PROFILE_INVALID", "header type")
        require(protected.get("alg") == "EdDSA", "BLOCKED_SIGNED_OBJECT_PROFILE_INVALID", "algorithm")
        require(protected.get("typ") == expected_typ, "BLOCKED_SIGNED_OBJECT_PROFILE_INVALID", "typ")
        require(
            protected.get("ctde_profile_version") == PROFILE_VERSION,
            "BLOCKED_SIGNED_OBJECT_PROFILE_INVALID",
            "profile version",
        )
        kid = protected.get("kid")
        require(isinstance(kid, str), "BLOCKED_SIGNED_OBJECT_PROFILE_INVALID", "kid missing")
        record = self.trust_store.get_active(kid, self.now)
        try:
            record.public_key.verify(
                signature,
                f"{protected_segment}.{payload_segment}".encode("ascii"),
            )
        except Exception as exc:
            raise PrototypeError("BLOCKED_SIGNED_OBJECT_PROFILE_INVALID", "signature") from exc

        require(isinstance(payload, dict), "BLOCKED_SIGNED_OBJECT_PROFILE_INVALID", "payload type")
        require(payload.get("iss") == expected_issuer, "BLOCKED_SIGNED_OBJECT_PROFILE_INVALID", "issuer")
        audience = payload.get("aud")
        if isinstance(expected_audience, list):
            require(
                isinstance(audience, list) and sorted(audience) == sorted(expected_audience),
                "BLOCKED_SIGNED_OBJECT_PROFILE_INVALID",
                "audience set",
            )
        else:
            require(audience == expected_audience, "BLOCKED_SIGNED_OBJECT_PROFILE_INVALID", "audience")

        for field in ("iat", "nbf", "exp"):
            require(type(payload.get(field)) is int, "BLOCKED_SIGNED_OBJECT_PROFILE_INVALID", f"{field} missing")
        require(payload["iat"] <= payload["nbf"], "BLOCKED_SIGNED_OBJECT_PROFILE_INVALID", "iat/nbf")
        require(payload["nbf"] <= self.now, "BLOCKED_SIGNED_OBJECT_PROFILE_INVALID", "not yet valid")
        require(self.now <= payload["exp"], "BLOCKED_SIGNED_OBJECT_PROFILE_INVALID", "expired")
        require(payload["exp"] - payload["iat"] <= max_ttl, "BLOCKED_SIGNED_OBJECT_PROFILE_INVALID", "ttl")

        if require_common:
            require(
                payload.get("environment") == expected_environment,
                "BLOCKED_SIGNED_OBJECT_PROFILE_INVALID",
                "environment",
            )
            require(isinstance(payload.get("object_id"), str), "BLOCKED_SIGNED_OBJECT_PROFILE_INVALID", "object id")
            require(
                isinstance(payload.get("authorization_file_sha256"), str),
                "BLOCKED_SIGNED_OBJECT_PROFILE_INVALID",
                "authorization digest",
            )
            if expected_attempt_id is not None:
                require(
                    payload.get("attempt_id") == expected_attempt_id,
                    "BLOCKED_SIGNED_OBJECT_PROFILE_INVALID",
                    "attempt",
                )
        require("signature" not in payload, "BLOCKED_SIGNED_OBJECT_PROFILE_INVALID", "self signature")
        require("signed_object_sha256" not in payload, "BLOCKED_SIGNED_OBJECT_PROFILE_INVALID", "self digest")
        return protected, payload

    @staticmethod
    def digest(token: str) -> str:
        return sha256_bytes(token.encode("ascii"))

