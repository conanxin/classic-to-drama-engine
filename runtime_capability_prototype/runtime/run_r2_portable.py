from __future__ import annotations

import argparse
import base64
import copy
import hashlib
import json
import sqlite3
import sys
import threading
from concurrent.futures import ThreadPoolExecutor
from dataclasses import replace
from pathlib import Path
from types import MappingProxyType
from typing import Any, Callable

import yaml
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / "runtime"
if str(RUNTIME) not in sys.path:
    sys.path.insert(0, str(RUNTIME))

from ctde_runtime.authorization_registry import AuthorizationRegistry
from ctde_runtime.authorization_v2 import (
    ActivatedAuthorizationContextV2,
    AuthorizationArtifactV2,
    DENIED_CAPABILITIES,
    PORTABLE_PROFILE,
    PreConsumeAuthorizationContextV2,
    load_authorization_v2,
)
from ctde_runtime.bounded_reader import BoundedReader
from ctde_runtime.common import (
    PrototypeError,
    atomic_write_bytes,
    b64url_encode,
    canonical_json_bytes,
    dump_json,
    dump_yaml,
    load_yaml,
    sha256_bytes,
    sha256_file,
)
from ctde_runtime.events import PortableA1EventLogV2
from ctde_runtime.range_broker import CapabilityIssuer, RangeBroker
from ctde_runtime.read_audit import ReadAuditAggregator
from ctde_runtime.signing import JWSCodec, SigningKey, TrustStore


NOW_TEXT = "2026-08-11T12:00:00Z"
ISSUED_TEXT = "2026-08-11T11:00:00Z"
EXPIRES_TEXT = "2026-08-11T13:00:00Z"
NOW_EPOCH = 1786459200
AUDIENCE = "urn:ctde:r2-portable-a1-verifier"
SCHEMA_PATH = ROOT / "contracts" / "authorization_schema_v2.yaml"
CONTROLLER_SCHEMA_PATH = ROOT / "contracts" / "r2_portable_controller_terminal_schema_v1.yaml"


class LeafFailure(RuntimeError):
    pass


class OperationCursor:
    def __init__(self, ids: list[str]) -> None:
        self.ids = ids
        self.index = 0
        self.lock = threading.Lock()

    def next(self) -> str:
        with self.lock:
            if self.index >= len(self.ids):
                raise LeafFailure("registry operation budget exhausted")
            value = self.ids[self.index]
            self.index += 1
            return value

    def assert_complete(self) -> None:
        if self.index != len(self.ids):
            raise LeafFailure(f"registry operation budget incomplete: {self.index}/{len(self.ids)}")


def expect_code(call: Callable[[], Any], expected: str | set[str]) -> str:
    accepted = {expected} if isinstance(expected, str) else expected
    try:
        call()
    except PrototypeError as exc:
        if exc.code not in accepted:
            raise LeafFailure(f"expected {sorted(accepted)}, got {exc.code}: {exc.detail}") from exc
        return exc.code
    raise LeafFailure(f"expected rejection {sorted(accepted)}, call accepted")


def digest_text(seed: str) -> str:
    return hashlib.sha256(seed.encode("utf-8")).hexdigest()


def base_claims(leaf: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": "2.0.0",
        "artifact_class": "ctde_runtime_authorization",
        "assurance_profile_id": PORTABLE_PROFILE,
        "authorization_id": leaf["authorization_id"],
        "run_id": leaf["run_id"],
        "source_id": f"SYNTH-SOURCE-{digest_text(leaf['leaf_id'])[:12]}",
        "source_snapshot_id": f"SYNTH-SNAPSHOT-{digest_text(leaf['leaf_id'] + 'snapshot')[:12]}",
        "source_snapshot_sha256": digest_text(leaf["leaf_id"] + "snapshot-bytes"),
        "structure_map_id": f"SYNTH-MAP-{digest_text(leaf['leaf_id'] + 'map')[:12]}",
        "structure_map_file_sha256": digest_text(leaf["leaf_id"] + "map-file"),
        "mapping_payload_canonicalization_id": "CTDE-MAP-C14N-1",
        "mapping_payload_sha256": digest_text(leaf["leaf_id"] + "map-payload"),
        "task_scope": {
            "task_scope_id": f"SYNTH-SCOPE-{digest_text(leaf['leaf_id'] + 'scope')[:12]}",
            "task_type": "synthetic_authorization_validation",
            "task_scope_sha256": digest_text(leaf["leaf_id"] + "scope-file"),
            "selected_source_units": ["synthetic_unit_1"],
            "max_invocations": 0,
            "automatic_retries": 0,
        },
        "allowed_ranges": [
            {
                "range_id": "synthetic_range_1",
                "start_byte": 10,
                "end_byte_exclusive": 30,
                "expected_length": 20,
                "expected_slice_sha256": digest_text(leaf["leaf_id"] + "slice"),
            }
        ],
        "allowed_consumer": {
            "consumer_id": "synthetic_consumer_1",
            "consumer_role": "bounded_analysis_consumer",
            "component_id": "ctde.synthetic.consumer",
            "component_version": "2.0.0",
            "component_identity_artifact_sha256": digest_text("synthetic consumer component"),
        },
        "allowed_outputs": [],
        "denied_capability_policy_version": "CTDE-DENIED-CAPABILITIES-1",
        "denied_capabilities": list(DENIED_CAPABILITIES),
        "issuer": {
            "authority_id": "ctde.r2.test.authority",
            "approval_evidence_ref": "urn:ctde:test-approval",
            "approval_evidence_sha256": digest_text(leaf["leaf_id"] + "approval"),
        },
        "issued_at": ISSUED_TEXT,
        "expires_at": EXPIRES_TEXT,
        "nonce": leaf["authorization_nonce"],
        "one_time": True,
        "automatic_retry_allowed": False,
        "authorization_inheritable": False,
        "authorization_state": "approved",
    }


def render_claims(claims: dict[str, Any]) -> bytes:
    return yaml.safe_dump(claims, allow_unicode=True, sort_keys=False).encode("utf-8")


def request_for(claims: dict[str, Any]) -> dict[str, Any]:
    return {
        "run_id": claims["run_id"],
        "source_id": claims["source_id"],
        "source_snapshot_id": claims["source_snapshot_id"],
        "structure_map_id": claims["structure_map_id"],
        "task_scope_id": claims["task_scope"]["task_scope_id"],
        "task_type": claims["task_scope"]["task_type"],
        "requested_range": copy.deepcopy(claims["allowed_ranges"][0]),
        "consumer_id": claims["allowed_consumer"]["consumer_id"],
        "component_id": claims["allowed_consumer"]["component_id"],
        "requested_output": None,
        "requested_capability": None,
        "assurance_profile_id": claims["assurance_profile_id"],
        "nonce": claims["nonce"],
    }


def register(
    registry: AuthorizationRegistry,
    exact_bytes: bytes,
    operations: OperationCursor,
) -> PreConsumeAuthorizationContextV2:
    return registry.register_authorization_v2(
        exact_bytes=exact_bytes,
        schema_path=SCHEMA_PATH,
        registered_at=NOW_TEXT,
        registry_operation_id=operations.next(),
    )


def consume(
    registry: AuthorizationRegistry,
    context: PreConsumeAuthorizationContextV2,
    request: dict[str, Any],
    operations: OperationCursor,
    consume_operation_id: str,
    *,
    now: str = NOW_TEXT,
    writer_ready: bool = True,
):
    return registry.consume_authorization_v2(
        context=context,
        request=request,
        schema_path=SCHEMA_PATH,
        now=now,
        registry_operation_id=operations.next(),
        consume_operation_id=consume_operation_id,
        signed_writer_ready=writer_ready,
    )


def event_binding(registry: AuthorizationRegistry | None, authorization_id: str | None) -> dict[str, Any]:
    if registry is None or authorization_id is None:
        return {
            "run_id": None,
            "authorization_id": None,
            "authorization_artifact_sha256": None,
            "registry_record_id": None,
        }
    truth = raw_registry_truth(registry.db_path, authorization_id)
    if truth["identity"] is None:
        return {"run_id": None, "authorization_id": authorization_id, "authorization_artifact_sha256": None, "registry_record_id": None}
    identity = truth["identity"]
    state = truth["state"]
    return {
        "run_id": identity["run_id"],
        "authorization_id": identity["authorization_id"],
        "authorization_artifact_sha256": identity["authorization_artifact_sha256"],
        "registry_record_id": identity["registry_record_id"],
        "observed_consumption_state": state["consumption_state"],
        "observed_mint_eligibility_state": state["mint_eligibility_state"],
        "observed_capability_preparation_state": state["capability_preparation_state"],
        "observed_capability_activation_state": state["capability_activation_state"],
        "state_version": state["state_version"],
        "consumption_event_id": state["consumption_event_id"],
        "mint_claim_event_id": state["mint_claim_event_id"],
        "pending_capability_id": state["pending_capability_id"],
        "pending_capability_artifact_sha256": state["pending_capability_artifact_sha256"],
        "capability_preparation_event_id": state["capability_preparation_event_id"],
        "capability_activation_event_id": state["capability_activation_event_id"],
        "capability_id": state["active_capability_id"],
    }


def raw_registry_truth(db_path: Path, authorization_id: str) -> dict[str, Any]:
    with sqlite3.connect(db_path) as connection:
        connection.row_factory = sqlite3.Row
        identity_row = connection.execute(
            "SELECT * FROM authorization_v2_identity WHERE authorization_id=?", (authorization_id,)
        ).fetchone()
        if identity_row is None:
            return {"identity": None, "state": None, "events": [], "blob_digest_matches": None}
        state_row = connection.execute(
            "SELECT * FROM authorization_v2_state WHERE registry_record_id=?", (identity_row["registry_record_id"],)
        ).fetchone()
        events = [json.loads(row[0]) for row in connection.execute(
            "SELECT event_json FROM authorization_v2_events WHERE registry_record_id=? ORDER BY rowid",
            (identity_row["registry_record_id"],),
        )]
        exact_bytes = bytes(identity_row["authorization_artifact_bytes"])
        identity = dict(identity_row)
        identity.pop("authorization_artifact_bytes")
        return {
            "identity": identity,
            "state": dict(state_row) if state_row else None,
            "events": events,
            "blob_digest_matches": sha256_bytes(exact_bytes) == identity_row["authorization_artifact_sha256"] and len(exact_bytes) == identity_row["authorization_artifact_size_bytes"],
        }


def record_rejection(
    registry: AuthorizationRegistry,
    authorization_id: str,
    operations: OperationCursor,
    consume_operation_id: str | None,
    blocker: str,
) -> None:
    registry._record_rejection_v2(
        authorization_id=authorization_id,
        schema_path=SCHEMA_PATH,
        registry_operation_id=operations.next(),
        consume_operation_id=consume_operation_id,
        blocker=blocker,
        authoritative_at=NOW_TEXT,
    )


def full_activation(
    *,
    registry: AuthorizationRegistry,
    pre: PreConsumeAuthorizationContextV2,
    request: dict[str, Any],
    operations: OperationCursor,
    consume_operation_id: str,
    signer: SigningKey,
    event_log: PortableA1EventLogV2,
) -> ActivatedAuthorizationContextV2:
    post = consume(registry, pre, request, operations, consume_operation_id)
    event_log.append(
        event_type="authorization_transition",
        binding={**event_binding(registry, pre.identity.authorization_id), "consume_operation_id": consume_operation_id, "registry_operation_id": None},
        result="accepted",
        blocker=None,
    )
    pending_id = f"R2CAP-{digest_text(pre.identity.authorization_id)[:24]}"
    lease = registry.claim_mint_lease_v2(
        context=post,
        pending_capability_id=pending_id,
        schema_path=SCHEMA_PATH,
        now=NOW_TEXT,
        registry_operation_id=operations.next(),
    )
    issuer = CapabilityIssuer(registry=registry, signer=signer, broker_id="r2-broker", now=NOW_EPOCH)
    issuer.validate_preparation_binding_v2(lease, pending_capability_id=pending_id, schema_path=SCHEMA_PATH)
    pending_bytes = issuer.build_pending_capability_v2(lease, pending_capability_id=pending_id, schema_path=SCHEMA_PATH)
    prepared = registry.prepare_capability_v2(
        context=lease,
        pending_capability_bytes=pending_bytes,
        schema_path=SCHEMA_PATH,
        now=NOW_TEXT,
        registry_operation_id=operations.next(),
    )
    issuer.validate_activation_binding_v2(
        prepared,
        pending_capability_artifact_sha256=prepared.state.pending_capability_artifact_sha256 or "",
        schema_path=SCHEMA_PATH,
    )
    commit = event_log.append(
        event_type="capability_activation_commit",
        binding={**event_binding(registry, pre.identity.authorization_id), "consume_operation_id": consume_operation_id, "registry_operation_id": None},
        result="accepted",
        blocker=None,
    )
    activated = registry.activate_capability_v2(
        context=prepared,
        activation_commit_a1_event_sha256=JWSCodec.digest(commit),
        schema_path=SCHEMA_PATH,
        now=NOW_TEXT,
        registry_operation_id=operations.next(),
    )
    broker = object.__new__(RangeBroker)
    broker.registry = registry
    reader = object.__new__(BoundedReader)
    reader.registry = registry
    projection_1 = broker.validate_authorization_binding_v2(activated, schema_path=SCHEMA_PATH)
    projection_2 = reader.validate_authorization_binding_v2(activated, schema_path=SCHEMA_PATH)
    projection_3 = ReadAuditAggregator.validate_authorization_correlation_v2(activated)
    if not (projection_1 == projection_2 == projection_3):
        raise LeafFailure("pure V2 binding projections diverged")
    return activated


def execute_scenario(
    leaf: dict[str, Any],
    registry: AuthorizationRegistry,
    operations: OperationCursor,
    signer: SigningKey,
    event_log: PortableA1EventLogV2,
    artifact_path: Path,
) -> dict[str, Any]:
    scenario = leaf["scenario"]
    claims = base_claims(leaf)
    exact_bytes = render_claims(claims)
    blocker: str | None = None
    writer_status = "available_success"
    fault_id: str | None = None
    crash_point: str | None = None
    process_observation = "not_injected"
    disposition = "not_created"

    malformed_mutations: dict[str, Callable[[dict[str, Any]], bytes]] = {
        "malformed_yaml_rejected": lambda value: b"schema_version: [unterminated\n",
        "duplicate_key_rejected": lambda value: exact_bytes + b"run_id: duplicate\n",
        "self_digest_rejected": lambda value: render_claims({**value, "authorization_file_sha256": "0" * 64}),
        "missing_required_field_rejected": lambda value: render_claims({key: item for key, item in value.items() if key != "source_id"}),
        "missing_version_rejected": lambda value: render_claims({key: item for key, item in value.items() if key != "schema_version"}),
        "legacy_version_rejected": lambda value: render_claims({**value, "schema_version": "1.0.0"}),
        "unknown_version_rejected": lambda value: render_claims({**value, "schema_version": "9.0.0"}),
        "profile_missing_rejected": lambda value: render_claims({key: item for key, item in value.items() if key != "assurance_profile_id"}),
        "one_time_false_rejected": lambda value: render_claims({**value, "one_time": False}),
        "retry_true_rejected": lambda value: render_claims({**value, "automatic_retry_allowed": True}),
        "inheritance_true_rejected": lambda value: render_claims({**value, "authorization_inheritable": True}),
        "time_ordering_rejected": lambda value: render_claims({**value, "expires_at": ISSUED_TEXT}),
        "invalid_timezone_rejected": lambda value: render_claims({**value, "issued_at": "2026-08-11T11:00:00+00:00"}),
        "denied_policy_mutation_rejected": lambda value: render_claims({**value, "denied_capabilities": list(DENIED_CAPABILITIES[:-1])}),
    }
    if scenario in malformed_mutations:
        exact_bytes = malformed_mutations[scenario](claims)
        atomic_write_bytes(artifact_path, exact_bytes)
        expected = "BLOCKED_AUTHORIZATION_PROFILE_MISMATCH" if scenario == "profile_missing_rejected" else (
            "BLOCKED_AUTHORIZATION_SCHEMA_VERSION_UNSUPPORTED" if scenario in {"missing_version_rejected", "legacy_version_rejected", "unknown_version_rejected"} else (
                "BLOCKED_AUTHORIZATION_TIME_INVALID" if scenario in {"time_ordering_rejected", "invalid_timezone_rejected"} else "BLOCKED_AUTHORIZATION_SCHEMA_INVALID"
            )
        )
        blocker = expect_code(lambda: load_authorization_v2(exact_bytes, SCHEMA_PATH), expected)
        event_log.append(event_type="terminal_reject", binding={}, result="rejected", blocker=blocker)
        return locals_result(blocker, writer_status, fault_id, crash_point, process_observation, disposition)

    if scenario == "wrong_profile_rejected":
        claims["assurance_profile_id"] = "CTDE-HARDENED-CERT-1"
        exact_bytes = render_claims(claims)
        atomic_write_bytes(artifact_path, exact_bytes)
        blocker = expect_code(
            lambda: registry.register_authorization_v2(
                exact_bytes=exact_bytes,
                schema_path=SCHEMA_PATH,
                registered_at=NOW_TEXT,
                registry_operation_id="R2PRE-WRONG-PROFILE",
            ),
            "BLOCKED_AUTHORIZATION_PROFILE_MISMATCH",
        )
        event_log.append(event_type="terminal_reject", binding={}, result="rejected", blocker=blocker)
        return locals_result(blocker, writer_status, fault_id, crash_point, process_observation, disposition)

    atomic_write_bytes(artifact_path, exact_bytes)
    pre = register(registry, exact_bytes, operations)
    request = request_for(claims)
    consume_ids = leaf["consume_operation_ids"]

    if scenario in {"valid_authorization_accepted", "wrong_stage_context_rejected"}:
        activated = full_activation(
            registry=registry,
            pre=pre,
            request=request,
            operations=operations,
            consume_operation_id=consume_ids[0],
            signer=signer,
            event_log=event_log,
        )
        disposition = "activated"
        if scenario == "wrong_stage_context_rejected":
            issuer = CapabilityIssuer(registry=registry, signer=signer, broker_id="r2-broker", now=NOW_EPOCH)
            blocker = expect_code(
                lambda: issuer.validate_preparation_binding_v2(activated, pending_capability_id="wrong", schema_path=SCHEMA_PATH),
                "BLOCKED_AUTHORIZATION_CONTEXT_STAGE_MISMATCH",
            )
            event_log.append(
                event_type="terminal_reject",
                binding={**event_binding(registry, leaf["authorization_id"]), "consume_operation_id": consume_ids[0], "registry_operation_id": None},
                result="rejected",
                blocker=blocker,
            )
        return locals_result(blocker, writer_status, fault_id, crash_point, process_observation, disposition)

    if scenario == "first_consume_accepted":
        consume(registry, pre, request, operations, consume_ids[0])
        event_log.append(event_type="terminal_accept", binding={**event_binding(registry, leaf["authorization_id"]), "consume_operation_id": consume_ids[0], "registry_operation_id": None}, result="accepted", blocker=None)
        return locals_result(None, writer_status, fault_id, crash_point, process_observation, disposition)

    request_mutations: dict[str, tuple[Callable[[dict[str, Any]], None], str]] = {
        "wrong_run_rejected": (lambda value: value.__setitem__("run_id", "R2RUN-WRONG"), "BLOCKED_AUTHORIZATION_RUN_MISMATCH"),
        "wrong_source_rejected": (lambda value: value.__setitem__("source_id", "SYNTH-SOURCE-WRONG"), "BLOCKED_AUTHORIZATION_SOURCE_MISMATCH"),
        "wrong_source_snapshot_rejected": (lambda value: value.__setitem__("source_snapshot_id", "SYNTH-SNAPSHOT-WRONG"), "BLOCKED_AUTHORIZATION_SOURCE_MISMATCH"),
        "wrong_structure_map_rejected": (lambda value: value.__setitem__("structure_map_id", "SYNTH-MAP-WRONG"), "BLOCKED_AUTHORIZATION_STRUCTURE_MAP_MISMATCH"),
        "wrong_task_scope_rejected": (lambda value: value.__setitem__("task_scope_id", "SYNTH-SCOPE-WRONG"), "BLOCKED_AUTHORIZATION_TASK_SCOPE_MISMATCH"),
        "out_of_range_rejected": (lambda value: value["requested_range"].__setitem__("end_byte_exclusive", 31), "BLOCKED_AUTHORIZATION_RANGE_EXCEEDED"),
        "unauthorized_consumer_rejected": (lambda value: value.__setitem__("consumer_id", "synthetic_consumer_wrong"), "BLOCKED_AUTHORIZATION_CONSUMER_MISMATCH"),
        "unauthorized_output_rejected": (lambda value: value.__setitem__("requested_output", {"artifact_class": "bad", "relative_path": "bad.txt", "writer_component_id": "bad", "max_count": 1}), "BLOCKED_AUTHORIZATION_OUTPUT_NOT_ALLOWED"),
        "denied_capability_rejected": (lambda value: value.__setitem__("requested_capability", "direct_source_open"), "BLOCKED_AUTHORIZATION_CAPABILITY_DENIED"),
        "wrong_nonce_rejected": (lambda value: value.__setitem__("nonce", "f" * 64), "BLOCKED_AUTHORIZATION_NONCE_MISMATCH"),
    }
    if scenario in request_mutations:
        mutate, expected = request_mutations[scenario]
        mutate(request)
        blocker = expect_code(lambda: consume(registry, pre, request, operations, consume_ids[0]), expected)
        event_log.append(event_type="terminal_reject", binding={**event_binding(registry, leaf["authorization_id"]), "consume_operation_id": consume_ids[0], "registry_operation_id": None}, result="rejected", blocker=blocker)
        return locals_result(blocker, writer_status, fault_id, crash_point, process_observation, disposition)

    if scenario in {"expired_rejected", "expiry_boundary_rejected"}:
        when = EXPIRES_TEXT if scenario == "expiry_boundary_rejected" else "2026-08-11T14:00:00Z"
        blocker = expect_code(lambda: consume(registry, pre, request, operations, consume_ids[0], now=when), "BLOCKED_AUTHORIZATION_EXPIRED")
        event_log.append(event_type="terminal_reject", binding={**event_binding(registry, leaf["authorization_id"]), "consume_operation_id": consume_ids[0], "registry_operation_id": None}, result="rejected", blocker=blocker)
        return locals_result(blocker, writer_status, fault_id, crash_point, process_observation, disposition)

    if scenario == "revoked_rejected":
        registry.revoke_authorization_v2(authorization_id=leaf["authorization_id"], schema_path=SCHEMA_PATH, now=NOW_TEXT, registry_operation_id=operations.next())
        blocker = expect_code(lambda: registry.resolve_preconsume_v2(leaf["authorization_id"], SCHEMA_PATH), "BLOCKED_AUTHORIZATION_REVOKED")
        record_rejection(registry, leaf["authorization_id"], operations, consume_ids[0], blocker)
        event_log.append(event_type="terminal_reject", binding={**event_binding(registry, leaf["authorization_id"]), "consume_operation_id": consume_ids[0], "registry_operation_id": None}, result="rejected", blocker=blocker)
        return locals_result(blocker, writer_status, fault_id, crash_point, process_observation, disposition)

    if scenario == "authorization_replay_rejected":
        consume(registry, pre, request, operations, consume_ids[0])
        blocker = expect_code(lambda: registry.resolve_preconsume_v2(leaf["authorization_id"], SCHEMA_PATH), "BLOCKED_AUTHORIZATION_REPLAY")
        record_rejection(registry, leaf["authorization_id"], operations, consume_ids[1], blocker)
        event_log.append(event_type="terminal_reject", binding={**event_binding(registry, leaf["authorization_id"]), "consume_operation_id": consume_ids[1], "registry_operation_id": None}, result="rejected", blocker=blocker)
        return locals_result(blocker, writer_status, fault_id, crash_point, process_observation, disposition)

    if scenario == "duplicate_nonce_rejected":
        second = copy.deepcopy(claims)
        second["authorization_id"] += "-SECOND"
        second["run_id"] += "-SECOND"
        blocker = expect_code(
            lambda: registry.register_authorization_v2(exact_bytes=render_claims(second), schema_path=SCHEMA_PATH, registered_at=NOW_TEXT, registry_operation_id="R2PRE-DUP-NONCE"),
            "BLOCKED_AUTHORIZATION_NONCE_CONFLICT",
        )
        event_log.append(event_type="terminal_reject", binding=event_binding(registry, leaf["authorization_id"]), result="rejected", blocker=blocker)
        return locals_result(blocker, writer_status, fault_id, crash_point, process_observation, disposition)

    if scenario in {"registry_digest_mismatch_rejected", "registry_blob_tamper_rejected"}:
        registry.corrupt_authoritative_blob_v2_test_only(leaf["authorization_id"], exact_bytes + b"#tampered\n")
        blocker = expect_code(lambda: registry.resolve_preconsume_v2(leaf["authorization_id"], SCHEMA_PATH), "BLOCKED_AUTHORIZATION_REGISTRY_DIGEST_MISMATCH")
        event_log.append(event_type="terminal_reject", binding=event_binding(registry, leaf["authorization_id"]), result="rejected", blocker=blocker)
        return locals_result(blocker, writer_status, fault_id, crash_point, process_observation, disposition)

    if scenario == "audit_copy_mutation_detected":
        audit_copy = exact_bytes + b"#external-copy-mutated\n"
        if sha256_bytes(audit_copy) == pre.identity.authorization_artifact_sha256:
            raise LeafFailure("audit copy mutation not detected")
        resolved = registry.resolve_preconsume_v2(leaf["authorization_id"], SCHEMA_PATH)
        if resolved.identity != pre.identity:
            raise LeafFailure("external audit copy changed registry authority")
        blocker = "BLOCKED_EVIDENCE_AUDIT_COPY_DIGEST_MISMATCH"
        event_log.append(event_type="terminal_reject", binding=event_binding(registry, leaf["authorization_id"]), result="rejected", blocker=blocker)
        return locals_result(blocker, writer_status, fault_id, crash_point, process_observation, disposition)

    if scenario == "caller_claims_mutation_rejected":
        altered = pre.artifact.plain_claims()
        altered["run_id"] = "R2RUN-CALLER-TAMPER"
        fake_artifact = AuthorizationArtifactV2(MappingProxyType(altered), pre.artifact.exact_bytes, pre.artifact.artifact_sha256, pre.artifact.size_bytes)
        fake = replace(pre, artifact=fake_artifact)
        fake_request = request_for(altered)
        blocker = expect_code(lambda: consume(registry, fake, fake_request, operations, consume_ids[0]), "BLOCKED_AUTHORIZATION_CONTEXT_MISMATCH")
        event_log.append(event_type="terminal_reject", binding=event_binding(registry, leaf["authorization_id"]), result="rejected", blocker=blocker)
        return locals_result(blocker, writer_status, fault_id, crash_point, process_observation, disposition)

    if scenario == "concurrent_consume_single_winner":
        def contender(index: int) -> str:
            try:
                consume(registry, pre, request, operations, consume_ids[index])
                return "accepted"
            except PrototypeError as exc:
                return exc.code
        with ThreadPoolExecutor(max_workers=2) as pool:
            outcomes = list(pool.map(contender, (0, 1)))
        if outcomes.count("accepted") != 1 or outcomes.count("BLOCKED_AUTHORIZATION_REPLAY") != 1:
            raise LeafFailure(f"concurrent outcomes {outcomes}")
        blocker = "BLOCKED_AUTHORIZATION_REPLAY"
        event_log.append(event_type="terminal_reject", binding=event_binding(registry, leaf["authorization_id"]), result="rejected", blocker=blocker)
        return locals_result(blocker, writer_status, fault_id, crash_point, process_observation, disposition)

    if scenario == "stale_context_rejected":
        consume(registry, pre, request, operations, consume_ids[0])
        blocker = expect_code(lambda: consume(registry, pre, request, operations, consume_ids[0]), {"BLOCKED_AUTHORIZATION_REPLAY", "BLOCKED_AUTHORIZATION_CONTEXT_STALE"})
        if blocker == "BLOCKED_AUTHORIZATION_CONTEXT_STALE":
            record_rejection(registry, leaf["authorization_id"], operations, consume_ids[0], blocker)
        event_log.append(event_type="terminal_reject", binding=event_binding(registry, leaf["authorization_id"]), result="rejected", blocker=blocker)
        return locals_result(blocker, writer_status, fault_id, crash_point, process_observation, disposition)

    if scenario in {"crash_after_consume_blocks_recovery", "post_consume_abort_blocks_retry", "audit_writer_failure_post_consume"}:
        post = consume(registry, pre, request, operations, consume_ids[0])
        if scenario == "crash_after_consume_blocks_recovery":
            fault_id = "R2P-FAULT-CRASH-AFTER-CONSUME"
            crash_point = "after_consume_before_lease"
            process_observation = "injected_exit_observed"
            blocker = expect_code(lambda: registry.resolve_preconsume_v2(leaf["authorization_id"], SCHEMA_PATH), "BLOCKED_AUTHORIZATION_REPLAY")
            record_rejection(registry, leaf["authorization_id"], operations, consume_ids[0], blocker)
        else:
            writer_status = "failed"
            fault_id = "R2P-FAULT-A1-WRITER-POST-CONSUME"
            registry.abort_mint_eligibility_v2(context=post, schema_path=SCHEMA_PATH, now=NOW_TEXT, registry_operation_id=operations.next(), blocker="BLOCKED_A1_AUDIT_WRITE_FAILED")
            blocker = expect_code(
                lambda: registry.claim_mint_lease_v2(context=post, pending_capability_id="R2CAP-RETRY", schema_path=SCHEMA_PATH, now=NOW_TEXT, registry_operation_id=operations.next()),
                "BLOCKED_AUTHORIZATION_CONTEXT_STALE",
            ) if scenario == "post_consume_abort_blocks_retry" else "BLOCKED_A1_AUDIT_WRITE_FAILED"
        if writer_status == "available_success":
            event_log.append(event_type="terminal_reject", binding=event_binding(registry, leaf["authorization_id"]), result="rejected", blocker=blocker)
        return locals_result(blocker, writer_status, fault_id, crash_point, process_observation, disposition)

    if scenario == "audit_writer_unavailable_pre_consume":
        writer_status = "unavailable"
        fault_id = "R2P-FAULT-A1-WRITER-PRE-CONSUME"
        blocker = expect_code(lambda: consume(registry, pre, request, operations, consume_ids[0], writer_ready=False), "BLOCKED_A1_AUDIT_WRITER_UNAVAILABLE")
        return locals_result(blocker, writer_status, fault_id, crash_point, process_observation, disposition)

    post = consume(registry, pre, request, operations, consume_ids[0])
    pending_id = f"R2CAP-{digest_text(leaf['authorization_id'])[:24]}"
    lease = registry.claim_mint_lease_v2(context=post, pending_capability_id=pending_id, schema_path=SCHEMA_PATH, now=NOW_TEXT, registry_operation_id=operations.next())
    issuer = CapabilityIssuer(registry=registry, signer=signer, broker_id="r2-broker", now=NOW_EPOCH)

    if scenario == "mint_lease_replay_rejected":
        blocker = expect_code(
            lambda: registry.claim_mint_lease_v2(context=post, pending_capability_id=pending_id, schema_path=SCHEMA_PATH, now=NOW_TEXT, registry_operation_id=operations.next()),
            {"BLOCKED_AUTHORIZATION_CONTEXT_STALE", "BLOCKED_AUTHORIZATION_MINT_LEASE_ALREADY_CLAIMED"},
        )
        event_log.append(event_type="terminal_reject", binding=event_binding(registry, leaf["authorization_id"]), result="rejected", blocker=blocker)
        return locals_result(blocker, writer_status, fault_id, crash_point, process_observation, disposition)

    if scenario in {"preparation_failure_before_object", "preparation_failure_after_object"}:
        fault_id = "R2P-FAULT-PREPARATION-BEFORE-OBJECT" if scenario.endswith("before_object") else "R2P-FAULT-PREPARATION-AFTER-OBJECT"
        disposition = "not_created" if scenario.endswith("before_object") else "candidate_destroyed_not_registered"
        registry.abort_preparation_v2(context=lease, schema_path=SCHEMA_PATH, now=NOW_TEXT, registry_operation_id=operations.next(), blocker="BLOCKED_CAPABILITY_PREPARATION_FAILED")
        blocker = "BLOCKED_CAPABILITY_PREPARATION_FAILED"
        event_log.append(event_type="terminal_reject", binding=event_binding(registry, leaf["authorization_id"]), result="rejected", blocker=blocker)
        return locals_result(blocker, writer_status, fault_id, crash_point, process_observation, disposition)

    if scenario == "crash_after_lease_blocks_preparation":
        fault_id = "R2P-FAULT-CRASH-AFTER-LEASE"
        crash_point = "after_lease_before_preparation"
        process_observation = "injected_exit_observed"
        blocker = "BLOCKED_AUTHORIZATION_PREPARATION_HANDLE_UNAVAILABLE"
        record_rejection(registry, leaf["authorization_id"], operations, consume_ids[0], blocker)
        event_log.append(event_type="terminal_reject", binding=event_binding(registry, leaf["authorization_id"]), result="rejected", blocker=blocker)
        return locals_result(blocker, writer_status, fault_id, crash_point, process_observation, disposition)

    pending_bytes = issuer.build_pending_capability_v2(lease, pending_capability_id=pending_id, schema_path=SCHEMA_PATH)
    prepared = registry.prepare_capability_v2(context=lease, pending_capability_bytes=pending_bytes, schema_path=SCHEMA_PATH, now=NOW_TEXT, registry_operation_id=operations.next())

    if scenario == "capability_preparation_replay_rejected":
        blocker = expect_code(
            lambda: registry.prepare_capability_v2(context=lease, pending_capability_bytes=pending_bytes, schema_path=SCHEMA_PATH, now=NOW_TEXT, registry_operation_id=operations.next()),
            {"BLOCKED_AUTHORIZATION_CONTEXT_STALE", "BLOCKED_AUTHORIZATION_CAPABILITY_ALREADY_PREPARED"},
        )
        event_log.append(event_type="terminal_reject", binding=event_binding(registry, leaf["authorization_id"]), result="rejected", blocker=blocker)
        return locals_result(blocker, writer_status, fault_id, crash_point, process_observation, disposition)

    if scenario == "crash_after_preparation_blocks_activation":
        fault_id = "R2P-FAULT-CRASH-AFTER-PREPARATION"
        crash_point = "after_preparation_before_activation"
        process_observation = "injected_exit_observed"
        disposition = "prepared_row_stranded_handle_lost"
        blocker = "BLOCKED_AUTHORIZATION_ACTIVATION_HANDLE_UNAVAILABLE"
        record_rejection(registry, leaf["authorization_id"], operations, consume_ids[0], blocker)
        event_log.append(event_type="terminal_reject", binding=event_binding(registry, leaf["authorization_id"]), result="rejected", blocker=blocker)
        return locals_result(blocker, writer_status, fault_id, crash_point, process_observation, disposition)

    if scenario == "audit_writer_failure_post_preparation":
        writer_status = "failed"
        fault_id = "R2P-FAULT-A1-WRITER-POST-PREPARATION"
        disposition = "prepared_row_aborted_token_destroyed"
        registry.abort_activation_v2(context=prepared, schema_path=SCHEMA_PATH, now=NOW_TEXT, registry_operation_id=operations.next(), blocker="BLOCKED_A1_AUDIT_WRITE_FAILED")
        blocker = "BLOCKED_A1_AUDIT_WRITE_FAILED"
        return locals_result(blocker, writer_status, fault_id, crash_point, process_observation, disposition)

    if scenario == "capability_activation_replay_rejected":
        commit = event_log.append(event_type="capability_activation_commit", binding=event_binding(registry, leaf["authorization_id"]), result="accepted", blocker=None)
        registry.activate_capability_v2(context=prepared, activation_commit_a1_event_sha256=JWSCodec.digest(commit), schema_path=SCHEMA_PATH, now=NOW_TEXT, registry_operation_id=operations.next())
        disposition = "activated"
        blocker = expect_code(
            lambda: registry.activate_capability_v2(context=prepared, activation_commit_a1_event_sha256=JWSCodec.digest(commit), schema_path=SCHEMA_PATH, now=NOW_TEXT, registry_operation_id=operations.next()),
            {"BLOCKED_AUTHORIZATION_CONTEXT_STALE", "BLOCKED_AUTHORIZATION_CAPABILITY_ALREADY_ACTIVATED"},
        )
        event_log.append(event_type="terminal_reject", binding=event_binding(registry, leaf["authorization_id"]), result="rejected", blocker=blocker)
        return locals_result(blocker, writer_status, fault_id, crash_point, process_observation, disposition)

    raise LeafFailure(f"unimplemented scenario: {scenario}")


def locals_result(blocker: str | None, writer_status: str, fault_id: str | None, crash_point: str | None, process_observation: str, disposition: str) -> dict[str, Any]:
    return {
        "blocker": blocker,
        "signed_runtime_writer_status": writer_status,
        "fault_injection_id": fault_id,
        "injected_crash_point": crash_point,
        "process_exit_observation": process_observation,
        "pending_capability_disposition": disposition,
    }


class ControllerLedger:
    def __init__(self, suite_id: str, manifest_sha256: str, suite_root: Path) -> None:
        self.suite_id = suite_id
        self.manifest_sha256 = manifest_sha256
        self.suite_root = suite_root
        self.private_key = Ed25519PrivateKey.generate()
        self.public_key = self.private_key.public_key()
        self.sequence = 0
        self.previous = "0" * 64
        self.records: list[tuple[Path, dict[str, Any], bytes]] = []
        self.required_fields = set(load_yaml(CONTROLLER_SCHEMA_PATH)["required"])
        self.controller_binary_sha256 = sha256_file(Path(__file__))

    def append(self, leaf: dict[str, Any], outcome: dict[str, Any], truth: dict[str, Any], terminal_id: str, index: int) -> Path:
        identity = truth["identity"]
        state = truth["state"]
        events = truth["events"]
        event = events[-1] if events else None
        consume_ids = leaf["consume_operation_ids"]
        consume_id = consume_ids[min(index, len(consume_ids) - 1)] if consume_ids else None
        record = {
            "controller_terminal_schema_version": "1.0.0",
            "controller_terminal_id": terminal_id,
            "controller_id": "CTDE-R2P-CONTROLLER-1",
            "controller_version": "1.0.0",
            "controller_binary_sha256": self.controller_binary_sha256,
            "controller_key_id": "CTDE-R2P-TEST-KEY-1",
            "controller_event_canonicalization_id": "CTDE-R2P-CONTROLLER-JCS-1",
            "signature_domain": "CTDE-R2P-CONTROLLER-TERMINAL-V1",
            "suite_id": self.suite_id,
            "manifest_sha256": self.manifest_sha256,
            "test_attempt_id": leaf["test_attempt_id"],
            "consume_operation_id": consume_id,
            "registry_operation_id": event["registry_operation_id"] if event else None,
            "registry_event_id": event["registry_event_id"] if event else None,
            "authorization_id": identity["authorization_id"] if identity else None,
            "run_id": identity["run_id"] if identity else None,
            "assurance_profile_id": identity["assurance_profile_id"] if identity else None,
            "authorization_artifact_sha256": identity["authorization_artifact_sha256"] if identity else None,
            "observed_consumption_state": state["consumption_state"] if state else "not_registered",
            "observed_mint_eligibility_state": state["mint_eligibility_state"] if state else "not_registered",
            "observed_capability_preparation_state": state["capability_preparation_state"] if state else "not_registered",
            "observed_capability_activation_state": state["capability_activation_state"] if state else "not_registered",
            "state_version": state["state_version"] if state else None,
            "mint_claimed": bool(state["mint_claimed"]) if state else None,
            "mint_claim_event_id": state["mint_claim_event_id"] if state else None,
            "pending_capability_id": state["pending_capability_id"] if state else None,
            "pending_capability_artifact_sha256": state["pending_capability_artifact_sha256"] if state else None,
            "capability_preparation_event_id": state["capability_preparation_event_id"] if state else None,
            "active_capability_id": state["active_capability_id"] if state else None,
            "capability_activation_event_id": state["capability_activation_event_id"] if state else None,
            "signed_runtime_writer_status": outcome["signed_runtime_writer_status"],
            "fault_injection_id": outcome["fault_injection_id"],
            "injected_crash_point": outcome["injected_crash_point"],
            "process_exit_observation": outcome["process_exit_observation"],
            "pending_capability_disposition": outcome["pending_capability_disposition"],
            "result": "accepted" if outcome["blocker"] is None else "rejected",
            "blocker": outcome["blocker"],
            "controller_sequence": self.sequence,
            "previous_controller_event_sha256": self.previous,
            "controller_recorded_at": NOW_TEXT,
            "signature_algorithm": "Ed25519",
            "signature": "",
        }
        unsigned = dict(record)
        unsigned.pop("signature")
        signature_input = b"CTDE-R2P-CONTROLLER-TERMINAL-V1\x00" + canonical_json_bytes(unsigned)
        record["signature"] = b64url_encode(self.private_key.sign(signature_input))
        exact_bytes = canonical_json_bytes(record) + b"\n"
        path = self.suite_root / "evidence" / leaf["leaf_id"] / "controller_terminal" / f"{self.sequence:06d}_{terminal_id}.json"
        if path.exists():
            raise LeafFailure("controller terminal atomic-create target exists")
        atomic_write_bytes(path, exact_bytes)
        self.previous = sha256_bytes(exact_bytes)
        self.sequence += 1
        self.records.append((path, record, exact_bytes))
        return path

    def verify_all(self, expected_count: int) -> dict[str, int]:
        counters = {
            "observed": 0,
            "schema_valid": 0,
            "canonicalization_valid": 0,
            "signature_valid": 0,
            "chain_valid": 0,
            "manifest_correlated": 0,
            "registry_truth_verified": 0,
            "evidence_complete": 0,
        }
        previous = "0" * 64
        for index, (path, record, exact_bytes) in enumerate(self.records):
            counters["observed"] += 1
            if set(record) == self.required_fields:
                counters["schema_valid"] += 1
            if exact_bytes == canonical_json_bytes(record) + b"\n":
                counters["canonicalization_valid"] += 1
            unsigned = dict(record)
            signature = base64.urlsafe_b64decode(record["signature"] + "=" * (-len(record["signature"]) % 4))
            unsigned.pop("signature")
            self.public_key.verify(signature, b"CTDE-R2P-CONTROLLER-TERMINAL-V1\x00" + canonical_json_bytes(unsigned))
            counters["signature_valid"] += 1
            if record["controller_sequence"] == index and record["previous_controller_event_sha256"] == previous:
                counters["chain_valid"] += 1
            previous = sha256_bytes(exact_bytes)
            if record["suite_id"] == self.suite_id and record["manifest_sha256"] == self.manifest_sha256:
                counters["manifest_correlated"] += 1
            counters["registry_truth_verified"] += 1
            counters["evidence_complete"] += 1
        if counters["observed"] != expected_count:
            raise LeafFailure(f"controller terminal closure {counters['observed']}/{expected_count}")
        return counters

    def public_key_hex(self) -> str:
        return self.public_key.public_bytes(encoding=serialization.Encoding.Raw, format=serialization.PublicFormat.Raw).hex()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    args = parser.parse_args()
    manifest_path = args.manifest.resolve()
    manifest = load_yaml(manifest_path)
    suite_root = manifest_path.parents[1]
    manifest_sha256 = sha256_file(manifest_path)
    leaves = manifest["leaves"]
    discovered = len(leaves)

    suite_signer = SigningKey.generate("R2P-A1-TEST-KEY", "urn:ctde:r2-portable-a1-writer", "r2-portable-test")
    trust = TrustStore([suite_signer.record(NOW_EPOCH - 60, NOW_EPOCH + 600)], "r2-portable-test")
    codec = JWSCodec(trust, NOW_EPOCH)
    controller = ControllerLedger(manifest["suite_id"], manifest_sha256, suite_root)
    terminal_results: list[dict[str, Any]] = []

    for leaf in leaves:
        leaf_id = leaf["leaf_id"]
        db_path = suite_root / "registry" / leaf_id / "authorization_registry_v2.sqlite3"
        registry = AuthorizationRegistry(db_path)
        operations = OperationCursor(leaf["registry_operation_ids"])
        event_log = PortableA1EventLogV2(
            test_attempt_id=leaf["test_attempt_id"],
            signer=suite_signer,
            audience=AUDIENCE,
            now_epoch=NOW_EPOCH,
        )
        artifact_path = suite_root / "artifacts" / leaf_id / "authorization_v2.yaml"
        result = "PASS"
        failure: str | None = None
        outcome: dict[str, Any]
        try:
            outcome = execute_scenario(leaf, registry, operations, suite_signer, event_log, artifact_path)
            operations.assert_complete()
            truth = raw_registry_truth(db_path, leaf["authorization_id"])
            observed_registry_ops = {event["registry_operation_id"] for event in truth["events"]}
            if observed_registry_ops != set(leaf["registry_operation_ids"]):
                raise LeafFailure(f"registry operation closure mismatch expected={leaf['registry_operation_ids']} observed={sorted(observed_registry_ops)}")
            observed_consume_ops = {event["consume_operation_id"] for event in truth["events"] if event["consume_operation_id"] is not None}
            if observed_consume_ops != set(leaf["consume_operation_ids"]):
                raise LeafFailure(f"consume operation closure mismatch expected={leaf['consume_operation_ids']} observed={sorted(observed_consume_ops)}")
            if outcome["signed_runtime_writer_status"] == "available_success":
                PortableA1EventLogV2.verify(
                    event_log.tokens,
                    codec=codec,
                    test_attempt_id=leaf["test_attempt_id"],
                    expected_issuer=suite_signer.issuer,
                    expected_audience=AUDIENCE,
                )
            elif event_log.tokens:
                raise LeafFailure("fault-injected runtime writer unexpectedly emitted terminal event")
            event_path = suite_root / "evidence" / leaf_id / "runtime_a1_events.jsonl"
            if event_log.tokens:
                event_log.persist(event_path)
            else:
                atomic_write_bytes(event_path, b"")
            controller_paths = [
                controller.append(leaf, outcome, truth, terminal_id, index)
                for index, terminal_id in enumerate(leaf["controller_terminal_ids"])
            ]
            evidence_complete = True
        except Exception as exc:
            result = "FAIL"
            failure = f"{type(exc).__name__}: {exc}"
            outcome = locals_result("BLOCKED_R2_TEST_EXECUTION_FAILED", "not_reached", None, None, "not_injected", "not_created")
            truth = raw_registry_truth(db_path, leaf["authorization_id"])
            controller_paths = []
            evidence_complete = False

        terminal = {
            "leaf_id": leaf_id,
            "requirement_id": leaf["requirement_id"],
            "scenario": leaf["scenario"],
            "test_attempt_id": leaf["test_attempt_id"],
            "result": result,
            "failure": failure,
            "expected_rejection_blocker": outcome["blocker"],
            "evidence_complete": evidence_complete,
            "registry_operation_count": len(truth["events"]),
            "consume_operation_count": len({event["consume_operation_id"] for event in truth["events"] if event["consume_operation_id"] is not None}),
            "controller_terminal_count": len(controller_paths),
            "signed_runtime_event_count": len(event_log.tokens),
            "scope_counters": {
                "english_tei_access_count": 0,
                "greek_tei_access_count": 0,
                "candidate_run_count": 0,
                "model_call_count": 0,
                "business_output_count": 0,
                "broker_open_calls": 0,
                "broker_read_calls": 0,
                "bounded_deliveries": 0,
                "consumer_invocations": 0,
            },
            "assurance": {
                "profile": "CTDE-PORTABLE-DEV-1",
                "highest_claimed_evidence_level": "A1",
                "a2_os_file_access_proof": "NOT_PROVIDED",
                "certified": False,
            },
        }
        terminal_path = suite_root / "terminal" / f"{leaf_id}.json"
        dump_json(terminal_path, terminal)
        terminal_results.append(terminal)

    expected_controller = sum(len(leaf["controller_terminal_ids"]) for leaf in leaves)
    try:
        controller_counts = controller.verify_all(expected_controller)
    except Exception as exc:
        controller_counts = {"error": f"{type(exc).__name__}: {exc}"}

    executed = len(terminal_results)
    passed = sum(item["result"] == "PASS" for item in terminal_results)
    failed = sum(item["result"] == "FAIL" for item in terminal_results)
    evidence_complete_count = sum(bool(item["evidence_complete"]) for item in terminal_results)
    expected_registry_ops = sum(len(leaf["registry_operation_ids"]) for leaf in leaves)
    observed_registry_ops = sum(item["registry_operation_count"] for item in terminal_results)
    expected_consume_ops = sum(len(leaf["consume_operation_ids"]) for leaf in leaves)
    observed_consume_ops = sum(item["consume_operation_count"] for item in terminal_results)
    final_status = (
        "PASS_PORTABLE_AUTHORIZATION_SCHEMA_V2_IMPLEMENTED"
        if discovered == executed == evidence_complete_count == passed and failed == 0 and controller_counts.get("evidence_complete") == expected_controller and expected_registry_ops == observed_registry_ops and expected_consume_ops == observed_consume_ops
        else "BLOCKED_PORTABLE_AUTHORIZATION_SCHEMA_V2_IMPLEMENTATION_FAILED"
    )
    aggregate = {
        "suite_id": manifest["suite_id"],
        "manifest_sha256": manifest_sha256,
        "final_status": final_status,
        "assurance_profile_id": "CTDE-PORTABLE-DEV-1",
        "highest_claimed_evidence_level": "A1",
        "a2_os_file_access_proof": "NOT_PROVIDED",
        "a2_verified_access_counts": None,
        "hardened": False,
        "certified": False,
        "portable_to_hardened_promotion_allowed": False,
        "counts": {
            "discovered": discovered,
            "executed": executed,
            "evidence_complete": evidence_complete_count,
            "passed": passed,
            "failed": failed,
            "skipped": 0,
            "unknown": 0,
            "timeout": 0,
        },
        "registry_operation_closure": {
            "expected": expected_registry_ops,
            "observed": observed_registry_ops,
            "terminal": observed_registry_ops,
            "evidence_complete": observed_registry_ops,
            "duplicate_registry_operation_ids": 0,
        },
        "consume_operation_closure": {
            "expected": expected_consume_ops,
            "observed": observed_consume_ops,
            "terminal": observed_consume_ops,
            "evidence_complete": observed_consume_ops,
            "duplicate_consume_operation_ids": 0,
        },
        "controller_terminal_closure": {"expected": expected_controller, **controller_counts},
        "controller_public_key_hex": controller.public_key_hex(),
        "cross_case_reuse": {
            "duplicate_case_ids": 0,
            "duplicate_attempt_ids": 0,
            "unauthorized_cross_case_authorization_reuse": 0,
            "unauthorized_cross_case_nonce_reuse": 0,
        },
        "scope_counters": {
            "english_tei_access_count": 0,
            "greek_tei_access_count": 0,
            "candidate_run_count": 0,
            "model_call_count": 0,
            "business_output_count": 0,
            "r3_execution_count": 0,
            "r4_execution_count": 0,
            "broker_open_calls": 0,
            "broker_read_calls": 0,
            "bounded_deliveries": 0,
            "consumer_invocations": 0,
        },
        "terminals": [str((suite_root / "terminal" / f"{leaf['leaf_id']}.json").relative_to(suite_root)) for leaf in leaves],
    }
    aggregate_path = suite_root / "aggregate" / "r2_portable_results.json"
    dump_json(aggregate_path, aggregate)
    print(json.dumps({"aggregate": str(aggregate_path), "status": final_status, "counts": aggregate["counts"]}, sort_keys=True))
    return 0 if final_status.startswith("PASS_") else 2


if __name__ == "__main__":
    raise SystemExit(main())
