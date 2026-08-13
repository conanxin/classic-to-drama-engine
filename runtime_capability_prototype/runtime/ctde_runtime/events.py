from __future__ import annotations

import json
import uuid
from pathlib import Path
from typing import Any

from .common import atomic_write_bytes, sha256_bytes
from .signing import EVENT_TYP, JWSCodec, SigningKey


PORTABLE_A1_EVENT_TYP = "ctde-portable-a1-event-v2+jws"


class SignedEventLog:
    def __init__(
        self,
        *,
        attempt_id: str,
        domain: str,
        signer: SigningKey,
        audience: str,
        authorization_file_sha256: str,
        now: int,
    ) -> None:
        self.attempt_id = attempt_id
        self.domain = domain
        self.signer = signer
        self.audience = audience
        self.authorization_file_sha256 = authorization_file_sha256
        self.now = now
        self.tokens: list[str] = []

    def append(self, kind: str, data: dict[str, Any] | None = None) -> str:
        previous = JWSCodec.digest(self.tokens[-1]) if self.tokens else None
        sequence = len(self.tokens) + 1
        payload = {
            "object_id": f"urn:ctde:event:{uuid.uuid4()}",
            "event_id": f"EVT-{uuid.uuid4()}",
            "environment": "prototype_fixture_only",
            "attempt_id": self.attempt_id,
            "authorization_file_sha256": self.authorization_file_sha256,
            "iss": self.signer.issuer,
            "aud": self.audience,
            "iat": self.now,
            "nbf": self.now,
            "exp": self.now + 300,
            "domain": self.domain,
            "sequence": sequence,
            "previous_event_sha256": previous,
            "kind": kind,
            "data": data or {},
        }
        token = JWSCodec.sign(self.signer, EVENT_TYP, payload)
        self.tokens.append(token)
        return token

    def persist(self, path: Path) -> None:
        rows = [json.dumps({"event_jws": token}, sort_keys=True) for token in self.tokens]
        atomic_write_bytes(path, ("\n".join(rows) + "\n").encode("utf-8"))

    @staticmethod
    def verify(
        tokens: list[str],
        *,
        codec: JWSCodec,
        expected_attempt_id: str,
        expected_domain: str,
        expected_issuer: str,
        expected_audience: str,
    ) -> list[dict[str, Any]]:
        verified: list[dict[str, Any]] = []
        previous: str | None = None
        for index, token in enumerate(tokens, 1):
            _, payload = codec.verify(
                token,
                expected_typ=EVENT_TYP,
                expected_issuer=expected_issuer,
                expected_audience=expected_audience,
                max_ttl=300,
                expected_attempt_id=expected_attempt_id,
            )
            if payload.get("domain") != expected_domain:
                raise ValueError("domain mismatch")
            if payload.get("sequence") != index:
                raise ValueError("sequence mismatch")
            if payload.get("previous_event_sha256") != previous:
                raise ValueError("event chain mismatch")
            previous = sha256_bytes(token.encode("ascii"))
            verified.append(payload)
        if not verified:
            raise ValueError("empty evidence log")
        return verified


class PortableA1EventLogV2:
    """Signed A1 logical events for the dedicated Portable R2 suite.

    This log intentionally makes no A2/A3 claim.  The controller ledger is a
    separate writer and is not implemented through this class.
    """

    def __init__(
        self,
        *,
        test_attempt_id: str,
        signer: SigningKey,
        audience: str,
        now_epoch: int,
    ) -> None:
        self.test_attempt_id = test_attempt_id
        self.signer = signer
        self.audience = audience
        self.now_epoch = now_epoch
        self.tokens: list[str] = []

    def append(self, *, event_type: str, binding: dict[str, Any], result: str, blocker: str | None) -> str:
        previous = JWSCodec.digest(self.tokens[-1]) if self.tokens else "0" * 64
        payload = {
            "event_schema_id": "urn:ctde:schema:runtime-audit-attestation:2",
            "event_schema_version": "2.0.0",
            "event_type": event_type,
            "authorization_schema_version": "2.0.0",
            "assurance_profile_id": "CTDE-PORTABLE-DEV-1",
            "test_attempt_id": self.test_attempt_id,
            "consume_operation_id": binding.get("consume_operation_id"),
            "registry_operation_id": binding.get("registry_operation_id"),
            "run_id": binding.get("run_id"),
            "authorization_id": binding.get("authorization_id"),
            "authorization_artifact_sha256": binding.get("authorization_artifact_sha256"),
            "registry_record_id": binding.get("registry_record_id"),
            "observed_consumption_state": binding.get("observed_consumption_state", "not_registered"),
            "observed_mint_eligibility_state": binding.get("observed_mint_eligibility_state", "not_registered"),
            "observed_capability_preparation_state": binding.get("observed_capability_preparation_state", "not_registered"),
            "observed_capability_activation_state": binding.get("observed_capability_activation_state", "not_registered"),
            "state_version": binding.get("state_version"),
            "consumption_event_id": binding.get("consumption_event_id"),
            "mint_claim_event_id": binding.get("mint_claim_event_id"),
            "pending_capability_id": binding.get("pending_capability_id"),
            "pending_capability_artifact_sha256": binding.get("pending_capability_artifact_sha256"),
            "capability_preparation_event_id": binding.get("capability_preparation_event_id"),
            "capability_activation_event_id": binding.get("capability_activation_event_id"),
            "capability_id": binding.get("capability_id"),
            "result": result,
            "blocker": blocker,
            "event_sequence": len(self.tokens),
            "previous_event_sha256": previous,
            "iss": self.signer.issuer,
            "aud": self.audience,
            "iat": self.now_epoch,
            "nbf": self.now_epoch,
            "exp": self.now_epoch + 300,
        }
        token = JWSCodec.sign(self.signer, PORTABLE_A1_EVENT_TYP, payload)
        self.tokens.append(token)
        return token

    def persist(self, path: Path) -> None:
        rows = [json.dumps({"event_jws": token}, sort_keys=True) for token in self.tokens]
        atomic_write_bytes(path, ("\n".join(rows) + "\n").encode("utf-8"))

    @staticmethod
    def verify(
        tokens: list[str],
        *,
        codec: JWSCodec,
        test_attempt_id: str,
        expected_issuer: str,
        expected_audience: str,
    ) -> list[dict[str, Any]]:
        require_fields = {
            "event_schema_id",
            "event_schema_version",
            "event_type",
            "authorization_schema_version",
            "assurance_profile_id",
            "test_attempt_id",
            "consume_operation_id",
            "registry_operation_id",
            "run_id",
            "authorization_id",
            "authorization_artifact_sha256",
            "registry_record_id",
            "observed_consumption_state",
            "observed_mint_eligibility_state",
            "observed_capability_preparation_state",
            "observed_capability_activation_state",
            "state_version",
            "consumption_event_id",
            "mint_claim_event_id",
            "pending_capability_id",
            "pending_capability_artifact_sha256",
            "capability_preparation_event_id",
            "capability_activation_event_id",
            "capability_id",
            "result",
            "blocker",
            "event_sequence",
            "previous_event_sha256",
            "iss",
            "aud",
            "iat",
            "nbf",
            "exp",
        }
        previous = "0" * 64
        verified: list[dict[str, Any]] = []
        for index, token in enumerate(tokens):
            _, payload = codec.verify(
                token,
                expected_typ=PORTABLE_A1_EVENT_TYP,
                expected_issuer=expected_issuer,
                expected_audience=expected_audience,
                max_ttl=300,
                require_common=False,
            )
            if set(payload) != require_fields:
                raise ValueError("Portable A1 event schema mismatch")
            if payload["test_attempt_id"] != test_attempt_id or payload["event_sequence"] != index:
                raise ValueError("Portable A1 event correlation mismatch")
            if payload["previous_event_sha256"] != previous:
                raise ValueError("Portable A1 event chain mismatch")
            if payload["assurance_profile_id"] != "CTDE-PORTABLE-DEV-1":
                raise ValueError("Portable A1 profile mismatch")
            previous = JWSCodec.digest(token)
            verified.append(payload)
        if not verified:
            raise ValueError("empty Portable A1 event log")
        return verified
