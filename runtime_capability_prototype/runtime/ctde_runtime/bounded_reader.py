from __future__ import annotations

import fcntl
import os
from pathlib import Path
from typing import Any

from .authorization_registry import AuthorizationRegistry
from .common import PrototypeError, require, sha256_bytes
from .events import SignedEventLog
from .range_broker import BrokerDelivery
from .sandbox import SandboxSupervisor
from .signing import AUDIT_TYP, ENVELOPE_TYP, JWSCodec
from .authorization_v2 import ActivatedAuthorizationContextV2, validate_activated_projection


ENVELOPE_REQUIRED_CLAIMS = {
    "object_id",
    "environment",
    "attempt_id",
    "authorization_file_sha256",
    "iss",
    "aud",
    "iat",
    "nbf",
    "exp",
    "consumption_event_id",
    "capability_id",
    "delivery_id",
    "broker_component_id",
    "fixture_structure_contract_sha256",
    "start_byte",
    "end_byte_exclusive",
    "returned_bytes",
    "slice_sha256",
    "broker_read_attestation_id",
    "broker_read_attestation_sha256",
    "payload_transport",
}

F_GET_SEALS = 1034
F_SEAL_SEAL = 0x0001
F_SEAL_SHRINK = 0x0002
F_SEAL_GROW = 0x0004
F_SEAL_WRITE = 0x0008


class BoundedReader:
    def __init__(
        self,
        *,
        registry: AuthorizationRegistry,
        codec: JWSCodec,
        broker_issuer_id: str,
        broker_component_id: str,
        reader_id: str,
        audit_aggregator_id: str,
        sandbox: SandboxSupervisor,
    ) -> None:
        self.registry = registry
        self.codec = codec
        self.broker_issuer_id = broker_issuer_id
        self.broker_component_id = broker_component_id
        self.reader_id = reader_id
        self.audit_aggregator_id = audit_aggregator_id
        self.sandbox = sandbox
        self.last_sandbox_result: dict[str, Any] | None = None

    def consume(
        self,
        signed_envelope: str,
        sealed_slice_fd: int,
        *,
        broker_read_attestation: str,
        authorization: dict[str, Any],
        sandbox_root: Path,
        sandbox_events: SignedEventLog,
        parser_events: SignedEventLog,
        gateway_events: SignedEventLog,
        attack: str = "none",
        host_path: Path | None = None,
        inherited_fixture_fd: int | None = None,
        preserve_inherited_fixture_fd: bool = False,
        gateway_book2_injection: bool = False,
    ) -> dict[str, Any]:
        try:
            _, envelope = self.codec.verify(
                signed_envelope,
                expected_typ=ENVELOPE_TYP,
                expected_issuer=self.broker_issuer_id,
                expected_audience=self.reader_id,
                max_ttl=60,
                expected_attempt_id=authorization["attempt_id"],
            )
        except PrototypeError as exc:
            raise PrototypeError("BLOCKED_BROKER_ENVELOPE_INVALID", exc.detail) from exc
        require(set(envelope) == ENVELOPE_REQUIRED_CLAIMS, "BLOCKED_BROKER_ENVELOPE_INVALID", "claim schema")
        require(
            envelope["authorization_file_sha256"] == authorization["authorization_file_sha256"],
            "BLOCKED_BROKER_ENVELOPE_INVALID",
            "authorization binding",
        )
        require(
            envelope["broker_component_id"] == self.broker_component_id,
            "BLOCKED_BROKER_ENVELOPE_INVALID",
            "broker identity",
        )
        require(
            JWSCodec.digest(broker_read_attestation) == envelope["broker_read_attestation_sha256"],
            "BLOCKED_BROKER_ENVELOPE_INVALID",
            "broker attestation digest",
        )
        try:
            _, broker_attestation_payload = self.codec.verify(
                broker_read_attestation,
                expected_typ=AUDIT_TYP,
                expected_issuer=self.broker_issuer_id,
                expected_audience=self.audit_aggregator_id,
                max_ttl=300,
                expected_attempt_id=authorization["attempt_id"],
            )
        except PrototypeError as exc:
            raise PrototypeError("BLOCKED_BROKER_ENVELOPE_INVALID", "broker attestation") from exc
        require(
            broker_attestation_payload["attestation_id"] == envelope["broker_read_attestation_id"],
            "BLOCKED_BROKER_ENVELOPE_INVALID",
            "broker attestation identity",
        )
        self.registry.consume_delivery(envelope["delivery_id"], authorization["attempt_id"])

        stat = os.fstat(sealed_slice_fd)
        seals = fcntl.fcntl(sealed_slice_fd, F_GET_SEALS)
        required_seals = F_SEAL_WRITE | F_SEAL_GROW | F_SEAL_SHRINK | F_SEAL_SEAL
        require((seals & required_seals) == required_seals, "BLOCKED_BROKER_ENVELOPE_INVALID", "seals")
        require(stat.st_size == envelope["returned_bytes"], "BLOCKED_BROKER_ENVELOPE_INVALID", "length")
        slice_bytes = os.pread(sealed_slice_fd, stat.st_size, 0)
        require(sha256_bytes(slice_bytes) == envelope["slice_sha256"], "BLOCKED_BROKER_ENVELOPE_INVALID", "slice hash")
        sandbox_result = self.sandbox.run(
            slice_fd=sealed_slice_fd,
            sandbox_root=sandbox_root,
            events=sandbox_events,
            attack=attack,
            host_path=host_path,
            inherited_fixture_fd=inherited_fixture_fd,
            preserve_inherited_fixture_fd=preserve_inherited_fixture_fd,
        )
        self.last_sandbox_result = sandbox_result
        parser_events.append(
            "parser_scope_result",
            {
                "book1_markers": sandbox_result["book1_markers"],
                "book2_markers": sandbox_result["book2_markers"],
                "other_book_markers": sandbox_result["other_book_markers"],
                "card_markers": sandbox_result["card_markers"],
                "paragraph_markers": sandbox_result["paragraph_markers"],
                "prefix_markers": sandbox_result["prefix_markers"],
                "greek_markers": sandbox_result["greek_markers"],
                "dtd_markers": sandbox_result["dtd_markers"],
                "entity_markers": sandbox_result["entity_markers"],
                "external_reference_markers": sandbox_result["external_reference_markers"],
                "namespace_ok": sandbox_result["namespace_ok"],
                "parser_status": sandbox_result["parser_status"],
            },
        )
        if attack in {"open_path", "greek_path"}:
            require(sandbox_result["attack_denied"], "BLOCKED_SANDBOX_ISOLATION_UNPROVEN", "path attack succeeded")
            require(sandbox_result["attack_success_bytes"] == 0, "BLOCKED_SANDBOX_ISOLATION_UNPROVEN")
            raise PrototypeError("BLOCKED_SANDBOX_DIRECT_SOURCE_ACCESS")
        if attack.startswith("write_"):
            require(sandbox_result["attack_denied"], "BLOCKED_SANDBOX_ISOLATION_UNPROVEN", "write attack succeeded")
            raise PrototypeError("BLOCKED_TEST_WRITE_ISOLATION")
        if attack in {"mmap", "sendfile", "splice", "copy_file_range", "io_uring", "child_escape"}:
            require(sandbox_result["attack_denied"], "BLOCKED_SANDBOX_ISOLATION_UNPROVEN", "second channel succeeded")
            require(sandbox_result["attack_success_bytes"] == 0, "BLOCKED_SANDBOX_ISOLATION_UNPROVEN")
            raise PrototypeError("BLOCKED_SANDBOX_SECOND_CHANNEL")
        if attack == "network":
            require(sandbox_result["attack_denied"], "BLOCKED_SANDBOX_ISOLATION_UNPROVEN", "network socket succeeded")
            raise PrototypeError("BLOCKED_SANDBOX_NETWORK_FORBIDDEN")
        if sandbox_result["parser_status"] != "pass":
            raise PrototypeError(sandbox_result["parser_status"])
        gateway_events.append(
            "gateway_scope_result",
            {
                "accepted_scope": "synthetic_book1_only",
                "book2_events": 1 if gateway_book2_injection else 0,
                "greek_events": 0,
                "range_outside_events": 0,
                "model_invocations": 0,
                "payload_persisted": False,
            },
        )
        if gateway_book2_injection:
            raise PrototypeError("INVALIDATED_PROTOTYPE_SCOPE_EXCEEDED", "gateway Book 2")
        return {
            "delivery_id": envelope["delivery_id"],
            "received_bytes": stat.st_size,
            "slice_sha256": envelope["slice_sha256"],
            "parser": sandbox_result,
            "model_invocations": 0,
            "payload_persisted": False,
        }

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
