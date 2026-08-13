from __future__ import annotations

import fcntl
import ctypes
import json
import os
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

from .authorization_registry import AuthorizationRegistry, MintLease
from .common import PrototypeError, require, sha256_bytes, union_half_open
from .events import SignedEventLog
from .fixture_factory import BOOK1_END, BOOK1_LENGTH, BOOK1_START, FixtureIdentity
from .signing import AUDIT_TYP, CAPABILITY_TYP, ENVELOPE_TYP, JWSCodec, SigningKey
from .authorization_v2 import (
    ActivatedAuthorizationContextV2,
    PostMintLeaseContextV2,
    PreparedCapabilityContextV2,
    validate_activated_projection,
)


CAPABILITY_REQUIRED_CLAIMS = {
    "object_id",
    "jti",
    "environment",
    "attempt_id",
    "authorization_file_sha256",
    "iss",
    "aud",
    "iat",
    "nbf",
    "exp",
    "capability_id",
    "nonce",
    "one_shot",
    "consumption_event_id",
    "fixture_object_id",
    "fixture_structure_contract_id",
    "fixture_structure_contract_sha256",
    "start_byte",
    "end_byte_exclusive",
    "expected_length",
    "expected_slice_sha256",
}


def _memfd_create(name: str) -> int:
    libc = ctypes.CDLL(None, use_errno=True)
    descriptor = libc.syscall(319, name.encode("utf-8"), 0x0001 | 0x0002)
    if descriptor < 0:
        error = ctypes.get_errno()
        raise OSError(error, os.strerror(error))
    return int(descriptor)


F_ADD_SEALS = 1033
F_SEAL_SEAL = 0x0001
F_SEAL_SHRINK = 0x0002
F_SEAL_GROW = 0x0004
F_SEAL_WRITE = 0x0008


@dataclass
class BrokerDelivery:
    sealed_slice_fd: int
    signed_envelope: str
    broker_read_attestation: str
    metadata: dict[str, Any]


class CapabilityIssuer:
    def __init__(
        self,
        *,
        registry: AuthorizationRegistry,
        signer: SigningKey,
        broker_id: str,
        now: int,
    ) -> None:
        self.registry = registry
        self.signer = signer
        self.broker_id = broker_id
        self.now = now

    def mint(
        self,
        lease: MintLease,
        authorization: dict[str, Any],
        events: SignedEventLog,
    ) -> str:
        self.registry.claim_mint_lease(lease)
        capability_id = f"CAP-{uuid.uuid4()}"
        payload = {
            "object_id": f"urn:ctde:capability:{capability_id}",
            "jti": capability_id,
            "environment": "prototype_fixture_only",
            "attempt_id": authorization["attempt_id"],
            "authorization_file_sha256": authorization["authorization_file_sha256"],
            "iss": self.signer.issuer,
            "aud": self.broker_id,
            "iat": self.now,
            "nbf": self.now,
            "exp": self.now + 60,
            "capability_id": capability_id,
            "nonce": f"NONCE-{uuid.uuid4()}",
            "one_shot": True,
            "consumption_event_id": lease.consumption_event_id,
            "fixture_object_id": authorization["fixture_object_id"],
            "fixture_structure_contract_id": authorization["fixture_structure_contract_id"],
            "fixture_structure_contract_sha256": authorization["fixture_structure_contract_sha256"],
            "start_byte": authorization["allowed_range"]["start_byte"],
            "end_byte_exclusive": authorization["allowed_range"]["end_byte_exclusive"],
            "expected_length": authorization["expected_length"],
            "expected_slice_sha256": authorization["expected_slice_sha256"],
        }
        token = JWSCodec.sign(self.signer, CAPABILITY_TYP, payload)
        self.registry.register_capability(capability_id, lease.consumption_event_id, authorization["attempt_id"])
        events.append(
            "capability_minted",
            {
                "capability_id": capability_id,
                "consumption_event_id": lease.consumption_event_id,
                "token_sha256": JWSCodec.digest(token),
            },
        )
        return token

    def validate_preparation_binding_v2(
        self,
        context: PostMintLeaseContextV2,
        *,
        pending_capability_id: str,
        schema_path: Path,
    ) -> dict[str, Any]:
        require(isinstance(context, PostMintLeaseContextV2), "BLOCKED_AUTHORIZATION_CONTEXT_STAGE_MISMATCH")
        state = self.registry.validate_context_v2(context, schema_path)
        require(state.consumption_state == "spent", "BLOCKED_AUTHORIZATION_CONTEXT_STAGE_MISMATCH")
        require(state.mint_eligibility_state == "claimed" and state.mint_claimed, "BLOCKED_AUTHORIZATION_CONTEXT_STAGE_MISMATCH")
        require(state.capability_preparation_state == "unprepared", "BLOCKED_AUTHORIZATION_CONTEXT_STAGE_MISMATCH")
        require(state.capability_activation_state == "not_ready", "BLOCKED_AUTHORIZATION_CONTEXT_STAGE_MISMATCH")
        require(state.pending_capability_id == pending_capability_id, "BLOCKED_AUTHORIZATION_CONTEXT_MISMATCH")
        return {
            "assurance_profile_id": context.identity.assurance_profile_id,
            "run_id": context.identity.run_id,
            "authorization_id": context.identity.authorization_id,
            "authorization_artifact_sha256": context.identity.authorization_artifact_sha256,
            "authorization_nonce": context.identity.nonce,
            "consumption_event_id": state.consumption_event_id,
            "mint_claim_event_id": state.mint_claim_event_id,
            "pending_capability_id": state.pending_capability_id,
        }

    def build_pending_capability_v2(
        self,
        context: PostMintLeaseContextV2,
        *,
        pending_capability_id: str,
        schema_path: Path,
    ) -> bytes:
        projection = self.validate_preparation_binding_v2(
            context,
            pending_capability_id=pending_capability_id,
            schema_path=schema_path,
        )
        claims = context.artifact.claims
        payload = {
            "schema_version": "2.0.0",
            **projection,
            "capability_id": pending_capability_id,
            "allowed_consumer": dict(claims["allowed_consumer"]),
            "allowed_ranges": [dict(claims["allowed_ranges"][0])],
            "active": False,
        }
        return (json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")

    def validate_activation_binding_v2(
        self,
        context: PreparedCapabilityContextV2,
        *,
        pending_capability_artifact_sha256: str,
        schema_path: Path,
    ) -> dict[str, Any]:
        require(isinstance(context, PreparedCapabilityContextV2), "BLOCKED_AUTHORIZATION_CONTEXT_STAGE_MISMATCH")
        state = self.registry.validate_context_v2(context, schema_path)
        require(state.capability_preparation_state == "prepared", "BLOCKED_AUTHORIZATION_CONTEXT_STAGE_MISMATCH")
        require(state.capability_activation_state == "eligible", "BLOCKED_AUTHORIZATION_CONTEXT_STAGE_MISMATCH")
        require(
            state.pending_capability_artifact_sha256 == pending_capability_artifact_sha256,
            "BLOCKED_AUTHORIZATION_CONTEXT_MISMATCH",
        )
        return {
            "assurance_profile_id": context.identity.assurance_profile_id,
            "run_id": context.identity.run_id,
            "authorization_id": context.identity.authorization_id,
            "authorization_artifact_sha256": context.identity.authorization_artifact_sha256,
            "authorization_nonce": context.identity.nonce,
            "consumption_event_id": state.consumption_event_id,
            "mint_claim_event_id": state.mint_claim_event_id,
            "capability_preparation_event_id": state.capability_preparation_event_id,
            "pending_capability_id": state.pending_capability_id,
            "pending_capability_artifact_sha256": state.pending_capability_artifact_sha256,
        }


class RangeBroker:
    def __init__(
        self,
        *,
        registry: AuthorizationRegistry,
        codec: JWSCodec,
        capability_issuer_id: str,
        broker_id: str,
        reader_id: str,
        signer: SigningKey,
        catalog: dict[str, FixtureIdentity],
        monitors_active: Callable[[], bool],
        now: int,
    ) -> None:
        self.registry = registry
        self.codec = codec
        self.capability_issuer_id = capability_issuer_id
        self.broker_id = broker_id
        self.reader_id = reader_id
        self.signer = signer
        self.catalog = catalog
        self.monitors_active = monitors_active
        self.now = now

    def handle_request(
        self,
        request: dict[str, Any],
        *,
        authorization: dict[str, Any],
        events: SignedEventLog,
    ) -> BrokerDelivery:
        if set(request) != {"opaque_capability"}:
            raise PrototypeError("BLOCKED_RANGE_OVERRIDE_FORBIDDEN")
        return self.deliver(request["opaque_capability"], authorization=authorization, events=events)

    def validate_authorization_binding_v2(
        self,
        context: ActivatedAuthorizationContextV2,
        *,
        schema_path: Path,
    ) -> dict[str, Any]:
        self.registry.validate_context_v2(context, schema_path)
        claims = context.artifact.claims
        return validate_activated_projection(
            context,
            expected_consumer_id=claims["allowed_consumer"]["consumer_id"],
            expected_component_id=claims["allowed_consumer"]["component_id"],
        )

    def deliver(
        self,
        opaque_capability: str,
        *,
        authorization: dict[str, Any],
        events: SignedEventLog,
    ) -> BrokerDelivery:
        try:
            _, claims = self.codec.verify(
                opaque_capability,
                expected_typ=CAPABILITY_TYP,
                expected_issuer=self.capability_issuer_id,
                expected_audience=self.broker_id,
                max_ttl=60,
                expected_attempt_id=authorization["attempt_id"],
            )
        except PrototypeError as exc:
            raise PrototypeError("BLOCKED_RANGE_CAPABILITY_INVALID", exc.detail) from exc

        if set(claims) & {"broker_read_strategy", "read_to_eof", "full_hash", "automatic_retry"}:
            raise PrototypeError("BLOCKED_BROKER_FALLBACK_FORBIDDEN")
        require(set(claims) == CAPABILITY_REQUIRED_CLAIMS, "BLOCKED_RANGE_CAPABILITY_INVALID", "claim schema")
        fixture_object_id = claims["fixture_object_id"]
        if (
            "GREEK" in fixture_object_id.upper()
            or "PRODUCTION" in fixture_object_id.upper()
            or fixture_object_id.startswith("urn:sha256:")
        ):
            raise PrototypeError("BLOCKED_FORBIDDEN_SOURCE_ROLE")
        expected_range = authorization["allowed_range"]
        range_matches = (
            claims["start_byte"] == expected_range["start_byte"]
            and claims["end_byte_exclusive"] == expected_range["end_byte_exclusive"]
            and claims["expected_length"] == authorization["expected_length"]
        )
        require(range_matches, "BLOCKED_TEST_SCOPE_CONTRACT_MISMATCH")
        for field in (
            "authorization_file_sha256",
            "fixture_object_id",
            "fixture_structure_contract_id",
            "fixture_structure_contract_sha256",
            "expected_slice_sha256",
        ):
            require(claims[field] == authorization[field], "BLOCKED_TEST_SCOPE_CONTRACT_MISMATCH", field)
        state = self.registry.state(authorization["authorization_id"])
        require(state.get("state") == "spent", "BLOCKED_RANGE_CAPABILITY_INVALID", "registry state")
        require(
            state.get("consumption_event_id") == claims["consumption_event_id"],
            "BLOCKED_RANGE_CAPABILITY_INVALID",
            "consumption event",
        )
        require(self.monitors_active(), "BLOCKED_SCOPE_PROOF_UNAVAILABLE", "monitor late start")
        identity = self.catalog.get(fixture_object_id)
        require(identity is not None, "BLOCKED_FORBIDDEN_SOURCE_ROLE", "object absent from catalog")

        self.registry.consume_capability(claims["capability_id"], authorization["attempt_id"])
        events.append(
            "broker_open_attempt",
            {
                "fixture_object_id": fixture_object_id,
                "capability_id": claims["capability_id"],
                "consumption_event_id": claims["consumption_event_id"],
            },
        )
        descriptor = os.open(identity.full_path, os.O_RDONLY | os.O_CLOEXEC | os.O_NOFOLLOW)
        actual_calls: list[dict[str, int]] = []
        try:
            stat = os.fstat(descriptor)
            require(
                stat.st_dev == identity.device
                and stat.st_ino == identity.inode
                and stat.st_size == identity.full_size
                and stat.st_mtime_ns == identity.mtime_ns,
                "BLOCKED_SOURCE_OBJECT_NOT_IMMUTABLE",
            )
            start = claims["start_byte"]
            remaining = claims["expected_length"]
            position = start
            chunks: list[bytes] = []
            while remaining:
                chunk = os.pread(descriptor, remaining, position)
                returned = len(chunk)
                actual_calls.append(
                    {
                        "offset": position,
                        "requested_bytes": remaining,
                        "returned_bytes": returned,
                    }
                )
                if returned == 0:
                    break
                chunks.append(chunk)
                position += returned
                remaining -= returned
            payload = b"".join(chunks)
        finally:
            os.close(descriptor)

        ranges = [
            (call["offset"], call["offset"] + call["returned_bytes"])
            for call in actual_calls
            if call["returned_bytes"] > 0
        ]
        actual_union = union_half_open(ranges)
        events.append(
            "broker_read_complete",
            {
                "actual_read_calls": actual_calls,
                "actual_union_of_read_ranges": actual_union,
                "returned_bytes": len(payload),
                "outside_allowed_bytes": 0
                if actual_union == [{"start_byte": BOOK1_START, "end_byte_exclusive": BOOK1_END}]
                else None,
                "handle_closed": True,
            },
        )
        require(len(payload) == claims["expected_length"], "BLOCKED_SLICE_HASH_MISMATCH", "length")
        require(
            sha256_bytes(payload) == claims["expected_slice_sha256"],
            "BLOCKED_SLICE_HASH_MISMATCH",
            "slice digest",
        )

        broker_attestation_id = f"BRA-{uuid.uuid4()}"
        broker_attestation_payload = {
            "object_id": f"urn:ctde:broker-read-attestation:{broker_attestation_id}",
            "environment": "prototype_fixture_only",
            "attempt_id": authorization["attempt_id"],
            "authorization_file_sha256": authorization["authorization_file_sha256"],
            "iss": self.signer.issuer,
            "aud": "ctde-prototype-audit-aggregator",
            "iat": self.now,
            "nbf": self.now,
            "exp": self.now + 300,
            "attestation_id": broker_attestation_id,
            "capability_id": claims["capability_id"],
            "consumption_event_id": claims["consumption_event_id"],
            "actual_read_calls": actual_calls,
            "actual_union_of_read_ranges": actual_union,
            "returned_bytes": len(payload),
            "slice_sha256": sha256_bytes(payload),
            "handle_closed": True,
        }
        broker_attestation = JWSCodec.sign(self.signer, AUDIT_TYP, broker_attestation_payload)
        broker_attestation_sha256 = JWSCodec.digest(broker_attestation)
        delivery_id = f"DEL-{uuid.uuid4()}"
        envelope_payload = {
            "object_id": f"urn:ctde:broker-envelope:{delivery_id}",
            "environment": "prototype_fixture_only",
            "attempt_id": authorization["attempt_id"],
            "authorization_file_sha256": authorization["authorization_file_sha256"],
            "iss": self.signer.issuer,
            "aud": self.reader_id,
            "iat": self.now,
            "nbf": self.now,
            "exp": self.now + 60,
            "consumption_event_id": claims["consumption_event_id"],
            "capability_id": claims["capability_id"],
            "delivery_id": delivery_id,
            "broker_component_id": self.broker_id,
            "fixture_structure_contract_sha256": claims["fixture_structure_contract_sha256"],
            "start_byte": claims["start_byte"],
            "end_byte_exclusive": claims["end_byte_exclusive"],
            "returned_bytes": len(payload),
            "slice_sha256": sha256_bytes(payload),
            "broker_read_attestation_id": broker_attestation_id,
            "broker_read_attestation_sha256": broker_attestation_sha256,
            "payload_transport": "sealed_memory_only",
        }
        envelope = JWSCodec.sign(self.signer, ENVELOPE_TYP, envelope_payload)
        memfd = _memfd_create("ctde-book1-slice")
        os.write(memfd, payload)
        os.lseek(memfd, 0, os.SEEK_SET)
        fcntl.fcntl(
            memfd,
            F_ADD_SEALS,
            F_SEAL_WRITE | F_SEAL_GROW | F_SEAL_SHRINK | F_SEAL_SEAL,
        )
        self.registry.register_delivery(delivery_id, authorization["attempt_id"])
        events.append(
            "broker_delivery_created",
            {
                "delivery_id": delivery_id,
                "envelope_sha256": JWSCodec.digest(envelope),
                "payload_transport": "sealed_memory_only",
                "payload_persisted": False,
            },
        )
        return BrokerDelivery(
            sealed_slice_fd=memfd,
            signed_envelope=envelope,
            broker_read_attestation=broker_attestation,
            metadata=envelope_payload,
        )
