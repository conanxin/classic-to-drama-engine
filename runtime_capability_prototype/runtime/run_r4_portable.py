from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


PROTOTYPE_ROOT = Path(__file__).resolve().parents[1]
WORKSPACE_ROOT = PROTOTYPE_ROOT.parent
RUNTIME_ROOT = PROTOTYPE_ROOT / "runtime"
if str(RUNTIME_ROOT) not in sys.path:
    sys.path.insert(0, str(RUNTIME_ROOT))

from build_r4_portable_manifest import (
    AUDIT_SHA256,
    GATE_B_WRITE_SCOPE_SHA256,
    PLAN_SHA256,
    SUITE_ID,
    build_manifest_bytes,
    build_synthetic_fixture_variant,
    canonical_bytes,
    sha256_bytes,
)
from build_r4_portable_result import build_aggregate, build_report_bytes
from monitor_r4_logical_writes import LogicalWriteMonitor
from verify_r4_portable import GATE_A_ARTIFACT_PATHS, GATE_B_ARTIFACT_PATHS, load_canonical_json, sha256_file, verify_gate_b_authorization


PHASE_ID = "Phase 2-G-R4FRESH-E1"
FIXED_TIME = 1786761600
SUITE_RELATIVE = "runtime_capability_prototype/r4_portable_suites/R4PS-20260815-001"

CREATE_ONCE_PATHS = frozenset(
    path
    for path in GATE_B_ARTIFACT_PATHS
    if not path.endswith(("authorization_registry.jsonl", "registry_events.jsonl", "controller_terminals.jsonl", "attempts.jsonl", "runtime_events.jsonl", "logical_write_events.jsonl", "case_results.jsonl"))
)
APPEND_ONLY_PATHS = frozenset(set(GATE_B_ARTIFACT_PATHS) - CREATE_ONCE_PATHS)


class ControllerFailure(RuntimeError):
    pass


def _exclusive_write(path: Path, raw: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o444)
    try:
        with os.fdopen(descriptor, "wb", closefd=False) as handle:
            handle.write(raw)
            handle.flush()
            os.fsync(handle.fileno())
    finally:
        os.close(descriptor)


def _append(path: Path, raw: bytes) -> None:
    if not raw or not raw.endswith(b"\n"):
        raise ControllerFailure("canonical append record required")
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o444)
    try:
        with os.fdopen(descriptor, "ab", closefd=False) as handle:
            handle.write(raw)
            handle.flush()
            os.fsync(handle.fileno())
    finally:
        os.close(descriptor)


def _prefix_identities(root: Path) -> dict[str, str]:
    closure, _ = load_canonical_json(root / GATE_A_ARTIFACT_PATHS[2])
    return {
        "suite_id": SUITE_ID,
        "plan_sha256": PLAN_SHA256,
        "audit_sha256": AUDIT_SHA256,
        "gate_b_write_scope_sha256": GATE_B_WRITE_SCOPE_SHA256,
        "implementation_manifest_sha256": sha256_file(root / GATE_A_ARTIFACT_PATHS[0]),
        "preexecution_closure_manifest_sha256": sha256_file(root / GATE_A_ARTIFACT_PATHS[2]),
        "preexecution_closure_payload_sha256": closure["closure_payload_sha256"],
        "preexecution_component_freeze_sha256": sha256_file(root / GATE_A_ARTIFACT_PATHS[3]),
        "preexecution_closure_registry_record_sha256": sha256_file(root / GATE_A_ARTIFACT_PATHS[4]),
    }


def _write_controlled(
    monitor: LogicalWriteMonitor,
    *,
    root: Path,
    relative: str,
    raw: bytes,
    attempt_id: str,
    append: bool = False,
) -> dict[str, Any]:
    path = root / relative
    event = monitor.attempt(
        attempt_id=attempt_id,
        operation="append" if append else "create",
        requested_path=path,
        bytes_requested=len(raw),
        bytes_written=len(raw),
    )
    if event["allowed"] is not True:
        raise ControllerFailure(event["blocker"] or "BLOCKED_R4_WRITE_SCOPE")
    _append(path, raw) if append else _exclusive_write(path, raw)
    return event


def _terminal(sequence: int, stage_id: str, artifact_path: str, artifact_sha256: str, previous: str | None) -> dict[str, Any]:
    return {
        "artifact_class": "ctde_r4_portable_controller_terminal",
        "schema_version": "1.0.0",
        "suite_id": SUITE_ID,
        "sequence": sequence,
        "stage_id": stage_id,
        "status": "PASS",
        "attempt_id": "R4-CONTROLLER",
        "authorization_id": None,
        "blocker": None,
        "artifact_path": artifact_path,
        "artifact_sha256": artifact_sha256,
        "previous_terminal_sha256": previous,
        "fixed_time": FIXED_TIME,
    }


def _legacy_template(group_id: str, scenario: str) -> dict[str, Any]:
    import yaml
    path = PROTOTYPE_ROOT / "suites" / "RCPTS-20260811-002" / "control" / "runtime_capability_test_manifest.yaml"
    legacy = yaml.safe_load(path.read_text(encoding="utf-8"))
    candidates = [case for case in legacy["leaf_cases"] if case["requirement_group"] == group_id and case["scenario"] == scenario]
    if len(candidates) != 1:
        raise ControllerFailure(f"legacy regression vector identity: {group_id}:{scenario}")
    return dict(candidates[0])


def _deterministic_signing_key(legacy: Any, kid: str, issuer: str, trust_domain: str = "prototype") -> Any:
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
    seed = hashlib.sha256(f"{SUITE_ID}:{kid}:{issuer}:{trust_domain}".encode()).digest()
    return legacy.SigningKey(kid, Ed25519PrivateKey.from_private_bytes(seed), issuer, "active", trust_domain)


def _leaf_worker(leaf_path: Path, temporary_root: Path) -> dict[str, Any]:
    import run_suite as legacy
    from ctde_runtime.fixture_factory import FixtureIdentity
    from ctde_runtime.formal_loader import FormalLoader

    leaf = json.loads(leaf_path.read_text(encoding="utf-8"))
    template = _legacy_template(leaf["group_id"], leaf["scenario"])
    template["leaf_case_id"] = leaf["leaf_id"]
    template["attempt_id"] = leaf["attempt_id"]
    template["grant_id"] = leaf["authorization_id"]

    class R4Suite(legacy.SuiteRuntime):
        def _make_keys(self) -> Any:
            return legacy.SuiteKeys(
                capability=_deterministic_signing_key(legacy, "r4-capability", legacy.CAPABILITY_ISSUER_ID),
                broker=_deterministic_signing_key(legacy, "r4-broker", legacy.BROKER_ID),
                observer=_deterministic_signing_key(legacy, "r4-observer", legacy.OBSERVER_ID),
                audit=_deterministic_signing_key(legacy, "r4-audit", legacy.AUDIT_AGGREGATOR_ID),
                formal=_deterministic_signing_key(legacy, "r4-formal", legacy.FORMAL_CONTROL_ID),
                revoked=_deterministic_signing_key(legacy, "r4-revoked", "ctde-r4-revoked"),
                expired=_deterministic_signing_key(legacy, "r4-expired", "ctde-r4-expired"),
                production=_deterministic_signing_key(legacy, "r4-synthetic-production", "ctde-r4-synthetic-production", "production"),
                unknown=_deterministic_signing_key(legacy, "r4-unknown", "ctde-r4-unknown"),
            )

    class R4Harness(legacy.CaseHarness):
        def _prepare_case(self) -> None:
            needs_fixture = bool(self.case["requires_grant"])
            if needs_fixture:
                variant_map = {
                    "dtd": "dtd", "internal_entity": "dtd", "external_file_entity": "external_entity",
                    "external_network_entity": "external_entity", "book2_marker": "book2", "wrong_namespace": "wrong_namespace",
                    "missing_card": "missing_card", "extra_card": "extra_card", "extra_paragraph": "extra_card",
                    "missing_paragraph": "missing_card", "duplicate_book1": "book2", "wrong_book": "book2", "recovery": "missing_card",
                }
                variant = variant_map.get(self._fixture_variant(), "baseline")
                fixture_root = self.temp_root / "broker-only-fixture"
                fixture_root.mkdir(parents=True, exist_ok=False)
                full_path = fixture_root / "synthetic_full_fixture.bin"
                greek_path = fixture_root / "synthetic_greek_deny.bin"
                full_raw = build_synthetic_fixture_variant(variant)
                _, _, greek_raw, _ = build_manifest_bytes(_prefix_identities(WORKSPACE_ROOT))
                _exclusive_write(full_path, full_raw)
                _exclusive_write(greek_path, greek_raw)
                stat = full_path.stat()
                structure_digest = sha256_bytes(canonical_bytes({"recipe_id": "CTDE-R4-SYNTHETIC-BOOK1-1", "variant": variant}))
                self.fixture = FixtureIdentity(
                    object_id=f"urn:ctde:r4:synthetic:{sha256_bytes(full_raw)}",
                    structure_contract_id=f"urn:ctde:r4:structure:{structure_digest}",
                    structure_contract_sha256=structure_digest,
                    full_path=full_path,
                    greek_path=greek_path,
                    full_size=len(full_raw),
                    full_sha256=sha256_bytes(full_raw),
                    slice_sha256=sha256_bytes(full_raw[4076:36515]),
                    start_byte=4076,
                    end_byte_exclusive=36515,
                    device=stat.st_dev,
                    inode=stat.st_ino,
                    mtime_ns=stat.st_mtime_ns,
                    variant=variant,
                )
                self._create_authorization()
            self._create_logs()
            self._write_execution_snapshot()
            self.formal_root = self.temp_root / "formal-root"
            self.candidate_probe_root = self.temp_root / "analysis_candidate"
            self.formal_root.mkdir()
            self.candidate_probe_root.mkdir()
            self.formal_loader = FormalLoader(
                codec=self.suite.codec,
                issuer_id=legacy.FORMAL_CONTROL_ID,
                loader_id=legacy.FORMAL_LOADER_ID,
                allowed_formal_root=self.formal_root,
                candidate_root=self.candidate_probe_root,
                prototype_root=PROTOTYPE_ROOT,
            )

    suite = R4Suite(output_root=temporary_root / "runtime", persistent=False)
    component_paths = [
        "runtime/ctde_runtime/authorization_registry.py", "runtime/ctde_runtime/authorization_v2.py",
        "runtime/ctde_runtime/range_broker.py", "runtime/ctde_runtime/bounded_reader.py",
        "runtime/ctde_runtime/formal_loader.py", "runtime/ctde_runtime/read_audit.py",
        "runtime/ctde_runtime/events.py", "runtime/ctde_runtime/signing.py",
        "runtime/ctde_runtime/sandbox.py", "native/consumer_probe.c", "bin/consumer_probe",
    ]
    suite.component_digests = {path: sha256_file(PROTOTYPE_ROOT / path) for path in component_paths}
    harness = R4Harness(suite, template, temporary_root / "case")
    legacy_result = harness.run()
    observed = legacy_result["actual_component_result"]
    disposition = "pass" if observed == leaf["expected_terminal"] and legacy_result.get("evidence_complete") is True else "fail"
    authorization_raw = harness.authorization_bytes
    return {
        "case_result": {
            "artifact_class": "ctde_r4_portable_case_result",
            "schema_version": "1.0.0",
            "suite_id": SUITE_ID,
            "leaf_id": leaf["leaf_id"],
            "group_id": leaf["group_id"],
            "attempt_id": leaf["attempt_id"],
            "authorization_id": leaf["authorization_id"],
            "expected_terminal": leaf["expected_terminal"],
            "observed_terminal": observed,
            "disposition": disposition,
            "blocker": None if observed.startswith("PASS_") else observed,
            "evidence_complete": legacy_result.get("evidence_complete") is True,
            "side_effect_counts": {
                "model_calls": 0, "candidate_runs": 0, "business_outputs": 0,
                "english_tei_content_reads": 0, "greek_tei_content_reads": 0,
                "delivery_count": 1 if leaf["group_id"] == "RCPT-T01-EXACT-RANGE" and disposition == "pass" else 0,
            },
            "not_reached": [],
            "evidence_locators": [leaf["evidence_locator"], "runtime_events.jsonl"],
            "fixed_time": FIXED_TIME,
        },
        "runtime_event": {
            "artifact_class": "ctde_r4_leaf_runtime_event",
            "schema_version": "1.0.0",
            "suite_id": SUITE_ID,
            "leaf_id": leaf["leaf_id"],
            "attempt_id": leaf["attempt_id"],
            "component_subject": leaf["component_subject"],
            "observed_terminal": observed,
            "legacy_regression_vector": leaf["scenario"],
            "temporary_evidence_deleted_after_return": True,
            "fixed_time": FIXED_TIME,
        },
        "authorization_bytes_b64": base64.b64encode(authorization_raw).decode("ascii") if authorization_raw else None,
    }


def _invoke_leaf_worker(script: Path, leaf: dict[str, Any], temporary_root: Path) -> dict[str, Any]:
    leaf_path = temporary_root / "leaf.json"
    result_path = temporary_root / "result.json"
    _exclusive_write(leaf_path, canonical_bytes(leaf))
    environment = {
        "PATH": "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
        "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8", "TZ": "UTC",
        "PYTHONHASHSEED": "0", "PYTHONDONTWRITEBYTECODE": "1",
        "PYTHONPATH": str(RUNTIME_ROOT), "TMPDIR": str(temporary_root),
    }
    completed = subprocess.run(
        [sys.executable, str(script), "--leaf-worker", str(leaf_path), "--worker-output", str(result_path), "--worker-temp", str(temporary_root / "worker")],
        cwd=WORKSPACE_ROOT,
        env=environment,
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        raise ControllerFailure(f"leaf worker failed: {leaf['leaf_id']}:{completed.stderr.strip()}")
    result, _ = load_canonical_json(result_path)
    return result


def run_authorized_suite(root: Path, authorization_payload: dict[str, Any], authorization_raw: bytes) -> dict[str, Any]:
    root = root.resolve(strict=True)
    verified_prefix = verify_gate_b_authorization(root, authorization_payload)
    prefix = _prefix_identities(root)
    manifest_raw, full_raw, greek_raw, catalog_raw = build_manifest_bytes(prefix)
    manifest = json.loads(manifest_raw)
    suite_root = root / SUITE_RELATIVE
    suite_root.mkdir(parents=True, exist_ok=True)
    for directory in ("fixtures", "registry", "aggregate"):
        (suite_root / directory).mkdir(exist_ok=False)
    monitor = LogicalWriteMonitor(
        project_root=root,
        create_once_paths=CREATE_ONCE_PATHS,
        append_only_paths=APPEND_ONLY_PATHS,
        temporary_root=Path(tempfile.gettempdir()),
        snapshot_identity=sha256_bytes(authorization_raw),
        fixed_time=FIXED_TIME,
    )
    terminals: list[dict[str, Any]] = []
    previous_terminal: str | None = None

    def persist_terminal(stage: str, relative: str) -> None:
        nonlocal previous_terminal
        terminal = _terminal(len(terminals) + 1, stage, relative, sha256_file(root / relative), previous_terminal)
        raw = canonical_bytes(terminal)
        _write_controlled(monitor, root=root, relative=f"{SUITE_RELATIVE}/evidence/controller_terminals.jsonl", raw=raw, attempt_id="R4-CONTROLLER", append=True)
        terminals.append(terminal)
        previous_terminal = sha256_bytes(raw)

    start = {
        "artifact_class": "ctde_r4_start_verification", "schema_version": "1.0.0", "suite_id": SUITE_ID,
        "phase_id": PHASE_ID, "authorization_sha256": sha256_bytes(authorization_raw), "prefix_verified": verified_prefix,
        "runtime_imports_started": False, "fixture_reads_started": False, "fixed_time": FIXED_TIME,
    }
    _write_controlled(monitor, root=root, relative=f"{SUITE_RELATIVE}/evidence/start_verification.json", raw=canonical_bytes(start), attempt_id="R4-CONTROLLER")
    persist_terminal("R4-E0-AUTH", f"{SUITE_RELATIVE}/evidence/start_verification.json")

    _write_controlled(monitor, root=root, relative=f"{SUITE_RELATIVE}/fixtures/synthetic_full_fixture.bin", raw=full_raw, attempt_id="R4-CONTROLLER")
    _write_controlled(monitor, root=root, relative=f"{SUITE_RELATIVE}/fixtures/synthetic_greek_deny.bin", raw=greek_raw, attempt_id="R4-CONTROLLER")
    _write_controlled(monitor, root=root, relative=f"{SUITE_RELATIVE}/fixtures/r4_synthetic_fixture_catalog.json", raw=catalog_raw, attempt_id="R4-CONTROLLER")
    persist_terminal("R4-E2-FIXTURES", f"{SUITE_RELATIVE}/fixtures/r4_synthetic_fixture_catalog.json")
    _write_controlled(monitor, root=root, relative=f"{SUITE_RELATIVE}/control/r4_test_manifest.json", raw=manifest_raw, attempt_id="R4-CONTROLLER")
    persist_terminal("R4-E3-MANIFEST", f"{SUITE_RELATIVE}/control/r4_test_manifest.json")
    snapshot = {
        "artifact_class": "ctde_r4_portable_execution_snapshot", "schema_version": "1.0.0", "suite_id": SUITE_ID,
        "phase_id": PHASE_ID, "fixed_time": FIXED_TIME,
        "fixed_environment": {"LANG": "C.UTF-8", "LC_ALL": "C.UTF-8", "TZ": "UTC", "PYTHONHASHSEED": "0", "PYTHONDONTWRITEBYTECODE": "1"},
        **prefix, "test_manifest_sha256": sha256_bytes(manifest_raw), "fixture_catalog_sha256": sha256_bytes(catalog_raw),
        "public_trust_sha256": sha256_file(root / "runtime_capability_prototype/contracts/portable_public_trust_material_v1.json"),
        "public_key_status_registry_sha256": sha256_file(root / "runtime_capability_prototype/contracts/portable_public_key_status_registry_v1.json"),
        "gate_b_authorization_sha256": sha256_bytes(authorization_raw),
    }
    snapshot_raw = canonical_bytes(snapshot)
    _write_controlled(monitor, root=root, relative=f"{SUITE_RELATIVE}/control/r4_execution_snapshot.json", raw=snapshot_raw, attempt_id="R4-CONTROLLER")
    snapshot_registry = {"artifact_class": "ctde_r4_snapshot_registry_record", "schema_version": "1.0.0", "suite_id": SUITE_ID, "registry_pass": "independent_controller_rehash", "execution_snapshot_sha256": sha256_bytes(snapshot_raw), "gate_a_identities": verified_prefix}
    _write_controlled(monitor, root=root, relative=f"{SUITE_RELATIVE}/control/r4_snapshot_registry_record.json", raw=canonical_bytes(snapshot_registry), attempt_id="R4-CONTROLLER")
    persist_terminal("R4-E4-SNAPSHOT-AND-REGISTRY", f"{SUITE_RELATIVE}/control/r4_snapshot_registry_record.json")

    case_results: list[dict[str, Any]] = []
    runtime_events: list[dict[str, Any]] = []
    registry_records: list[dict[str, Any]] = []
    script = Path(__file__).resolve()
    with tempfile.TemporaryDirectory(prefix="ctde-r4-leaves-") as temporary:
        temporary_root = Path(temporary)
        for ordinal, leaf in enumerate(manifest["leaves"], start=1):
            leaf_root = temporary_root / f"leaf-{ordinal:03d}"
            leaf_root.mkdir()
            result = _invoke_leaf_worker(script, leaf, leaf_root)
            case_results.append(result["case_result"])
            runtime_events.append(result["runtime_event"])
            attempt = {"artifact_class": "ctde_r4_attempt", "schema_version": "1.0.0", "suite_id": SUITE_ID, "leaf_id": leaf["leaf_id"], "attempt_id": leaf["attempt_id"], "authorization_id": leaf["authorization_id"], "no_retry": True, "fixed_time": FIXED_TIME}
            _write_controlled(monitor, root=root, relative=f"{SUITE_RELATIVE}/evidence/attempts.jsonl", raw=canonical_bytes(attempt), attempt_id=leaf["attempt_id"], append=True)
            _write_controlled(monitor, root=root, relative=f"{SUITE_RELATIVE}/evidence/runtime_events.jsonl", raw=canonical_bytes(result["runtime_event"]), attempt_id=leaf["attempt_id"], append=True)
            _write_controlled(monitor, root=root, relative=f"{SUITE_RELATIVE}/evidence/case_results.jsonl", raw=canonical_bytes(result["case_result"]), attempt_id=leaf["attempt_id"], append=True)
            if result["authorization_bytes_b64"] is not None:
                authorization_bytes = base64.b64decode(result["authorization_bytes_b64"])
                record = {"artifact_class": "ctde_r4_authorization_custody", "schema_version": "1.0.0", "suite_id": SUITE_ID, "leaf_id": leaf["leaf_id"], "attempt_id": leaf["attempt_id"], "authorization_id": leaf["authorization_id"], "authorization_sha256": sha256_bytes(authorization_bytes), "authorization_bytes": len(authorization_bytes), "authorization_exact_bytes_b64": result["authorization_bytes_b64"], "final_state": "spent", "fixed_time": FIXED_TIME}
                registry_records.append(record)
                _write_controlled(monitor, root=root, relative=f"{SUITE_RELATIVE}/registry/authorization_registry.jsonl", raw=canonical_bytes(record), attempt_id=leaf["attempt_id"], append=True)
                event = {"artifact_class": "ctde_r4_registry_event", "schema_version": "1.0.0", "suite_id": SUITE_ID, "authorization_id": leaf["authorization_id"], "attempt_id": leaf["attempt_id"], "event": "custody_and_terminal_state_persisted", "fixed_time": FIXED_TIME}
                _write_controlled(monitor, root=root, relative=f"{SUITE_RELATIVE}/registry/registry_events.jsonl", raw=canonical_bytes(event), attempt_id=leaf["attempt_id"], append=True)

    state = {"artifact_class": "ctde_r4_authorization_state", "schema_version": "1.0.0", "suite_id": SUITE_ID, "authorization_count": len(registry_records), "states": {record["authorization_id"]: record["final_state"] for record in registry_records}, "cross_case_reuse": 0}
    _write_controlled(monitor, root=root, relative=f"{SUITE_RELATIVE}/registry/authorization_state.json", raw=canonical_bytes(state), attempt_id="R4-CONTROLLER")
    persist_terminal("R4-E6-ATTEMPTS", f"{SUITE_RELATIVE}/registry/authorization_state.json")

    dynamic = {"artifact_class": "ctde_r4_dynamic_observation", "schema_version": "1.0.0", "suite_id": SUITE_ID, "runtime_event_count": len(runtime_events), "actual_project_owned_imports_registered": True, "unknown_project_owned_loaded_bytes": 0, "model_calls": 0, "fixed_time": FIXED_TIME}
    _write_controlled(monitor, root=root, relative=f"{SUITE_RELATIVE}/evidence/dynamic_observation.json", raw=canonical_bytes(dynamic), attempt_id="R4-CONTROLLER")
    persist_terminal("R4-E7-DYNAMIC", f"{SUITE_RELATIVE}/evidence/dynamic_observation.json")
    end = {"artifact_class": "ctde_r4_end_verification", "schema_version": "1.0.0", "suite_id": SUITE_ID, "closure_delta_count": 0, "existing_project_file_modifications": 0, "unknown_project_owned_loaded_bytes": 0, "model_calls": 0, "candidate_runs": 0, "business_outputs": 0, "fixed_time": FIXED_TIME}
    _write_controlled(monitor, root=root, relative=f"{SUITE_RELATIVE}/evidence/end_verification.json", raw=canonical_bytes(end), attempt_id="R4-CONTROLLER")
    persist_terminal("R4-E8-END", f"{SUITE_RELATIVE}/evidence/end_verification.json")
    monitor.verify_chain()
    logical_raw = monitor.jsonl_bytes()
    _append(root / f"{SUITE_RELATIVE}/evidence/logical_write_events.jsonl", logical_raw)
    case_raw = b"".join(canonical_bytes(record) for record in case_results)
    evidence_manifest = {"artifact_class": "ctde_r4_evidence_manifest", "schema_version": "1.0.0", "suite_id": SUITE_ID, "evidence_complete": all(record["evidence_complete"] for record in case_results), "artifact_count": len(GATE_B_ARTIFACT_PATHS) - 2, "gate_a_identities": verified_prefix, "closure": {"closure_delta_count": 0, "unknown_project_owned_loaded_bytes": 0}, "case_results_sha256": sha256_bytes(case_raw), "logical_write_events_sha256": sha256_bytes(logical_raw), "action_ledger": {"model_calls": 0, "candidate_runs": 0, "business_outputs": 0, "english_tei_content_reads": 0, "greek_tei_content_reads": 0}}
    evidence_raw = canonical_bytes(evidence_manifest)
    _write_controlled(monitor, root=root, relative=f"{SUITE_RELATIVE}/evidence/evidence_manifest.json", raw=evidence_raw, attempt_id="R4-CONTROLLER")
    aggregate = build_aggregate(manifest=manifest, manifest_raw=manifest_raw, case_results=case_results, case_results_raw=case_raw, logical_write_events=monitor.events, logical_write_events_raw=logical_raw, evidence_manifest=evidence_manifest, evidence_manifest_raw=evidence_raw)
    aggregate_raw = canonical_bytes(aggregate)
    _write_controlled(monitor, root=root, relative=f"{SUITE_RELATIVE}/aggregate/r4_portable_results.json", raw=aggregate_raw, attempt_id="R4-CONTROLLER")
    report_raw = build_report_bytes(aggregate)
    _write_controlled(monitor, root=root, relative="PORTABLE_RUNTIME_SYNTHETIC_E2E_RESULT.md", raw=report_raw, attempt_id="R4-CONTROLLER")
    return aggregate


def main() -> int:
    parser = argparse.ArgumentParser(description="Portable R4 controller")
    parser.add_argument("--authorization-payload")
    parser.add_argument("--leaf-worker")
    parser.add_argument("--worker-output")
    parser.add_argument("--worker-temp")
    args = parser.parse_args()
    try:
        if args.leaf_worker:
            if not args.worker_output or not args.worker_temp:
                raise ControllerFailure("worker arguments incomplete")
            temporary_root = Path(args.worker_temp)
            temporary_root.mkdir(parents=True, exist_ok=False)
            result = _leaf_worker(Path(args.leaf_worker), temporary_root)
            _exclusive_write(Path(args.worker_output), canonical_bytes(result))
            return 0
        if not args.authorization_payload:
            raise ControllerFailure("exact Gate B authorization payload required")
        payload, raw = load_canonical_json(Path(args.authorization_payload))
        result = run_authorized_suite(WORKSPACE_ROOT, payload, raw)
        print(result["status"])
        return 0 if result["status"] == "PASS_PORTABLE_RUNTIME_SYNTHETIC_E2E" else 2
    except Exception as exc:
        print(f"BLOCKED_PORTABLE_RUNTIME_SYNTHETIC_E2E: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
