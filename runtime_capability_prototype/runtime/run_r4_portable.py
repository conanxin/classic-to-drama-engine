from __future__ import annotations

import argparse
import base64
import copy
import hashlib
import json
import os
import subprocess
import sys
import tempfile
from dataclasses import replace
from pathlib import Path
from typing import Any


def _ensure_bytecode_disabled_at_process_start() -> None:
    if sys.flags.dont_write_bytecode:
        os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
        return
    environment = os.environ.copy()
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    os.execve(sys.executable, [sys.executable, "-B", *sys.argv], environment)


_ensure_bytecode_disabled_at_process_start()


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
    synthetic_book1_object_id,
    synthetic_greek_object_id,
)
from build_r4_portable_result import build_aggregate, build_report_bytes
from monitor_r4_logical_writes import LogicalWriteMonitor
from verify_r4_portable import GATE_B_ARTIFACT_PATHS, REPAIRED_GATE_A_ARTIFACT_PATHS, load_canonical_json, sha256_file, verify_gate_b_authorization


PHASE_ID = "Phase 2-G-R4FRESH-E1"
FIXED_TIME = 1786761600
SUITE_RELATIVE = "runtime_capability_prototype/r4_portable_suites/R4PS-20260815-001"
TRACKED_PROBE_RELATIVE = "runtime_capability_prototype/bin/consumer_probe"
PROTOTYPE_PROBE_RELATIVE = "bin/consumer_probe"
TEMPORARY_PROBE_RELATIVE = "prepared-probe/consumer_probe"
TRACKED_PROBE_MODE = 0o644
TEMPORARY_PROBE_MODE = 0o500

CREATE_ONCE_PATHS = frozenset(
    path
    for path in GATE_B_ARTIFACT_PATHS
    if not path.endswith(("authorization_registry.jsonl", "registry_events.jsonl", "controller_terminals.jsonl", "attempts.jsonl", "runtime_events.jsonl", "logical_write_events.jsonl", "case_results.jsonl"))
)
APPEND_ONLY_PATHS = frozenset(set(GATE_B_ARTIFACT_PATHS) - CREATE_ONCE_PATHS)


class ControllerFailure(RuntimeError):
    pass


def _project_python_cache_outputs(root: Path) -> list[str]:
    outputs: set[str] = set()
    for path in root.rglob("__pycache__"):
        if path.is_dir():
            outputs.add(path.relative_to(root).as_posix() + "/")
    for path in root.rglob("*.pyc"):
        if path.is_file():
            outputs.add(path.relative_to(root).as_posix())
    return sorted(outputs)


def _assert_bytecode_process_and_tree(root: Path, stage: str) -> None:
    if not sys.flags.dont_write_bytecode or os.environ.get("PYTHONDONTWRITEBYTECODE") != "1":
        raise ControllerFailure(f"bytecode process protection absent: {stage}")
    outputs = _project_python_cache_outputs(root)
    if outputs:
        raise ControllerFailure(f"project Python cache output at {stage}: {outputs}")


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
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o600)
    try:
        with os.fdopen(descriptor, "ab", closefd=False) as handle:
            handle.write(raw)
            handle.flush()
            os.fsync(handle.fileno())
    finally:
        os.close(descriptor)


def _prefix_identities(root: Path) -> dict[str, str]:
    closure, _ = load_canonical_json(root / REPAIRED_GATE_A_ARTIFACT_PATHS[2])
    return {
        "suite_id": SUITE_ID,
        "plan_sha256": PLAN_SHA256,
        "audit_sha256": AUDIT_SHA256,
        "gate_b_write_scope_sha256": GATE_B_WRITE_SCOPE_SHA256,
        "implementation_manifest_sha256": sha256_file(root / REPAIRED_GATE_A_ARTIFACT_PATHS[0]),
        "preexecution_closure_manifest_sha256": sha256_file(root / REPAIRED_GATE_A_ARTIFACT_PATHS[2]),
        "preexecution_closure_payload_sha256": closure["closure_payload_sha256"],
        "preexecution_component_freeze_sha256": sha256_file(root / REPAIRED_GATE_A_ARTIFACT_PATHS[3]),
        "preexecution_closure_registry_record_sha256": sha256_file(root / REPAIRED_GATE_A_ARTIFACT_PATHS[4]),
    }


def _active_probe_expectation(root: Path) -> dict[str, Any]:
    closure, _ = load_canonical_json(root / REPAIRED_GATE_A_ARTIFACT_PATHS[2])
    matches = [node for node in closure.get("nodes", []) if node.get("identity") == TRACKED_PROBE_RELATIVE]
    if len(matches) != 1:
        raise ControllerFailure("active repaired closure probe identity")
    node = matches[0]
    if node.get("member_type") != "native_executable" or node.get("classification") != "runtime_closure_member":
        raise ControllerFailure("active repaired closure probe classification")
    if not isinstance(node.get("sha256"), str) or len(node["sha256"]) != 64 or not isinstance(node.get("bytes"), int):
        raise ControllerFailure("active repaired closure probe expectation")
    return {"sha256": node["sha256"], "bytes": node["bytes"]}


def _prepare_temporary_probe(temporary_root: Path) -> tuple[Path, dict[str, Any]]:
    resolved_root = temporary_root.resolve(strict=True)
    source = PROTOTYPE_ROOT / PROTOTYPE_PROBE_RELATIVE
    if source.is_symlink() or not source.is_file():
        raise ControllerFailure("tracked probe path identity")
    source = source.resolve(strict=True)
    if source != (PROTOTYPE_ROOT / PROTOTYPE_PROBE_RELATIVE).absolute():
        raise ControllerFailure("tracked probe resolved identity")
    source_stat = source.stat()
    source_mode = source_stat.st_mode & 0o777
    expectation = _active_probe_expectation(WORKSPACE_ROOT)
    source_raw = source.read_bytes()
    source_sha256 = sha256_bytes(source_raw)
    if source_sha256 != expectation["sha256"] or len(source_raw) != expectation["bytes"]:
        raise ControllerFailure("tracked probe active closure identity mismatch")
    if source_mode != TRACKED_PROBE_MODE:
        raise ControllerFailure("tracked probe source mode")
    target = resolved_root / TEMPORARY_PROBE_RELATIVE
    target.parent.mkdir(parents=True, exist_ok=False)
    if target.parent.resolve(strict=True).parent != resolved_root:
        raise ControllerFailure("temporary probe parent scope")
    descriptor = os.open(target, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o400)
    try:
        with os.fdopen(descriptor, "wb", closefd=False) as handle:
            handle.write(source_raw)
            handle.flush()
            os.fsync(handle.fileno())
    finally:
        os.close(descriptor)
    if target.is_symlink() or target.resolve(strict=True).parent.parent != resolved_root:
        raise ControllerFailure("temporary probe target scope")
    target_raw = target.read_bytes()
    target_sha256 = sha256_bytes(target_raw)
    if target_raw != source_raw or target_sha256 != expectation["sha256"]:
        raise ControllerFailure("temporary probe byte identity")
    os.chmod(target, TEMPORARY_PROBE_MODE)
    target_mode = target.stat().st_mode & 0o777
    if target_mode != TEMPORARY_PROBE_MODE:
        raise ControllerFailure("temporary probe executable mode")
    if (source.stat().st_mode & 0o777) != source_mode or sha256_file(source) != source_sha256:
        raise ControllerFailure("tracked probe mutated during preparation")
    return target, {
        "tracked_probe_relative_path": TRACKED_PROBE_RELATIVE,
        "tracked_probe_sha256": source_sha256,
        "tracked_probe_bytes": len(source_raw),
        "tracked_probe_mode_before": f"{source_mode:04o}",
        "tracked_probe_mode_after_worker": None,
        "tracked_probe_unchanged": None,
        "temporary_probe_relative_path": TEMPORARY_PROBE_RELATIVE,
        "temporary_probe_sha256": target_sha256,
        "temporary_probe_bytes": len(target_raw),
        "temporary_probe_mode": f"{target_mode:04o}",
        "temporary_probe_executable": bool(target_mode & 0o100),
        "temporary_probe_within_leaf_temp_root": True,
        "temporary_probe_copy_used": True,
        "source_copy_byte_identical": target_raw == source_raw,
        "active_closure_digest_exact": source_sha256 == expectation["sha256"],
        "active_closure_bytes_exact": len(source_raw) == expectation["bytes"],
        "temporary_probe_inventory": [TEMPORARY_PROBE_RELATIVE],
        "temporary_probe_path_class": "leaf_os_temporary",
        "project_binary_mode_modified": None,
        "sandbox_policy_relaxed": False,
        "sandbox_execution": None,
        "temporary_probe_cleanup_complete": None,
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
        def _create_authorization(self) -> None:
            if self.requirement != "RCPT-T16-GREEK-ID" or self.suffix != "AUTH-GREEK-ROLE":
                super()._create_authorization()
                return
            if self.fixture is None or not isinstance(getattr(self, "r4_greek_object_id", None), str):
                raise ControllerFailure("canonical Greek authorization fixture identity")
            original_requirement = self.requirement
            original_fixture = self.fixture
            self.requirement = "R4-CANONICAL-GREEK-AUTHORIZATION"
            self.fixture = replace(original_fixture, object_id=self.r4_greek_object_id)
            try:
                super()._create_authorization()
            finally:
                self.requirement = original_requirement
                self.fixture = original_fixture

        def _resign(
            self,
            token: str,
            *,
            signer: Any,
            typ: str,
            payload_updates: dict[str, Any] | None = None,
            protected_updates: dict[str, Any] | None = None,
        ) -> str:
            updates = dict(payload_updates) if payload_updates is not None else None
            if self.requirement == "RCPT-T16-GREEK-ID" and self.suffix == "CAP-GREEK-OBJECT" and updates is not None and "fixture_object_id" in updates:
                updates["fixture_object_id"] = self.r4_greek_object_id
                self.r4_effective_capability_fixture_object_id = self.r4_greek_object_id
            return super()._resign(token, signer=signer, typ=typ, payload_updates=updates, protected_updates=protected_updates)

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
                self.r4_greek_object_id = synthetic_greek_object_id(greek_raw)
                _exclusive_write(full_path, full_raw)
                _exclusive_write(greek_path, greek_raw)
                stat = full_path.stat()
                structure_digest = sha256_bytes(canonical_bytes({"recipe_id": "CTDE-R4-SYNTHETIC-BOOK1-1", "variant": variant}))
                self.fixture = FixtureIdentity(
                    object_id=synthetic_book1_object_id(full_raw),
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

    worker_bytecode_disabled = bool(sys.flags.dont_write_bytecode) and os.environ.get("PYTHONDONTWRITEBYTECODE") == "1"
    if not worker_bytecode_disabled:
        raise ControllerFailure("leaf worker bytecode startup protection")
    prepared_probe, probe_evidence = _prepare_temporary_probe(temporary_root)
    suite = R4Suite(output_root=temporary_root / "runtime", persistent=False)
    suite.probe_binary = prepared_probe
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
    if suite.probe_binary != prepared_probe:
        raise ControllerFailure("temporary probe execution binding")
    probe_evidence["sandbox_execution"] = "executed_verified_temporary_probe" if harness.sandbox_snapshot is not None else "not_reached_by_case_design"
    observed = legacy_result["actual_component_result"]
    disposition = "pass" if observed == leaf["expected_terminal"] and legacy_result.get("evidence_complete") is True else "fail"
    authorization_raw = harness.authorization_bytes
    capability_fixture_object_id = getattr(harness, "r4_effective_capability_fixture_object_id", None)
    if capability_fixture_object_id is None and harness.capability_token is not None:
        _, capability_payload, _ = legacy.decode_token(harness.capability_token)
        capability_fixture_object_id = capability_payload.get("fixture_object_id")
    bytecode_control = {
        "worker_startup_bytecode_disabled": worker_bytecode_disabled,
        "worker_sys_flag_dont_write_bytecode": bool(sys.flags.dont_write_bytecode),
        "worker_environment_dont_write_bytecode": os.environ.get("PYTHONDONTWRITEBYTECODE") == "1",
        "cache_cleanup_used_as_proof": False,
    }
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
            "runtime_fixture_object_id": harness.fixture.object_id if harness.fixture is not None else None,
            "runtime_fixture_full_sha256": harness.fixture.full_sha256 if harness.fixture is not None else None,
            "runtime_fixture_variant": harness.fixture.variant if harness.fixture is not None else None,
            "authorization_fixture_object_id": harness.authorization.get("fixture_object_id") if harness.authorization is not None else None,
            "capability_fixture_object_id": capability_fixture_object_id,
            "python_bytecode_control": bytecode_control,
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
            "runtime_fixture_object_id": harness.fixture.object_id if harness.fixture is not None else None,
            "runtime_fixture_full_sha256": harness.fixture.full_sha256 if harness.fixture is not None else None,
            "runtime_fixture_variant": harness.fixture.variant if harness.fixture is not None else None,
            "authorization_fixture_object_id": harness.authorization.get("fixture_object_id") if harness.authorization is not None else None,
            "capability_fixture_object_id": capability_fixture_object_id,
            "python_bytecode_control": bytecode_control,
            "temporary_evidence_deleted_after_return": True,
            "fixed_time": FIXED_TIME,
        },
        "authorization_bytes_b64": base64.b64encode(authorization_raw).decode("ascii") if authorization_raw else None,
        "probe_preparation": probe_evidence,
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
    probe = result.get("probe_preparation")
    if not isinstance(probe, dict):
        raise ControllerFailure("leaf probe evidence missing")
    bytecode_control = result.get("case_result", {}).get("python_bytecode_control")
    if not isinstance(bytecode_control, dict) or bytecode_control.get("worker_startup_bytecode_disabled") is not True or bytecode_control.get("cache_cleanup_used_as_proof") is not False:
        raise ControllerFailure("leaf worker bytecode evidence")
    worker_root = (temporary_root / "worker").resolve(strict=True)
    relative = Path(str(probe.get("temporary_probe_relative_path", "")))
    if relative.as_posix() != TEMPORARY_PROBE_RELATIVE or relative.is_absolute() or ".." in relative.parts:
        raise ControllerFailure("leaf probe evidence path")
    temporary_probe = (worker_root / relative).resolve(strict=True)
    try:
        temporary_probe.relative_to(worker_root)
    except ValueError as exc:
        raise ControllerFailure("leaf probe escaped temporary root") from exc
    temporary_raw = temporary_probe.read_bytes()
    temporary_mode = temporary_probe.stat().st_mode & 0o777
    tracked_probe = PROTOTYPE_ROOT / PROTOTYPE_PROBE_RELATIVE
    tracked_mode_after = tracked_probe.stat().st_mode & 0o777
    tracked_sha_after = sha256_file(tracked_probe)
    expectation = _active_probe_expectation(WORKSPACE_ROOT)
    if (
        sha256_bytes(temporary_raw) != expectation["sha256"]
        or len(temporary_raw) != expectation["bytes"]
        or temporary_mode != TEMPORARY_PROBE_MODE
        or tracked_sha_after != probe.get("tracked_probe_sha256")
        or tracked_mode_after != TRACKED_PROBE_MODE
    ):
        raise ControllerFailure("leaf probe post-execution verification")
    temporary_probe.unlink()
    if any(temporary_probe.parent.iterdir()):
        raise ControllerFailure("temporary probe inventory residue")
    temporary_probe.parent.rmdir()
    cleanup_complete = not temporary_probe.exists() and not temporary_probe.parent.exists()
    if not cleanup_complete:
        raise ControllerFailure("temporary probe cleanup")
    probe.update(
        {
            "tracked_probe_mode_after_worker": f"{tracked_mode_after:04o}",
            "tracked_probe_unchanged": tracked_sha_after == probe.get("tracked_probe_sha256") and tracked_mode_after == TRACKED_PROBE_MODE,
            "project_binary_mode_modified": tracked_mode_after != TRACKED_PROBE_MODE,
            "temporary_probe_cleanup_complete": cleanup_complete,
        }
    )
    result["case_result"]["sandbox_probe_preparation"] = probe
    result["runtime_event"]["sandbox_probe_preparation"] = probe
    del result["probe_preparation"]
    return result


def _register_denied_write_probe(monitor: LogicalWriteMonitor, root: Path) -> dict[str, Any]:
    forbidden = root / "forbidden-r4-write-probe"
    event = monitor.attempt(attempt_id="RCPT-R4-WRITE-PROBE", operation="create", requested_path=forbidden, bytes_requested=1, bytes_written=0)
    if event["allowed"] is not False or event["blocker"] != "BLOCKED_R4_WRITE_SCOPE" or forbidden.exists():
        raise ControllerFailure("denied write probe")
    return event


def _render_final_outputs(
    monitor: LogicalWriteMonitor,
    *,
    root: Path,
    manifest: dict[str, Any],
    manifest_raw: bytes,
    case_results: list[dict[str, Any]],
    case_raw: bytes,
    verified_prefix: dict[str, str],
    synthetic_fixture_identities: dict[str, str],
    python_bytecode_control: dict[str, Any],
) -> tuple[LogicalWriteMonitor, dict[str, bytes], dict[str, Any]]:
    logical_relative = f"{SUITE_RELATIVE}/evidence/logical_write_events.jsonl"
    evidence_relative = f"{SUITE_RELATIVE}/evidence/evidence_manifest.json"
    aggregate_relative = f"{SUITE_RELATIVE}/aggregate/r4_portable_results.json"
    report_relative = "PORTABLE_RUNTIME_SYNTHETIC_E2E_RESULT.md"
    final_paths = (logical_relative, evidence_relative, aggregate_relative, report_relative)

    def render(sizes: tuple[int, int, int, int]) -> tuple[LogicalWriteMonitor, dict[str, bytes], dict[str, Any]]:
        candidate = copy.deepcopy(monitor)
        for index, (relative, size) in enumerate(zip(final_paths, sizes)):
            candidate.attempt(attempt_id="R4-CONTROLLER", operation="append" if index == 0 else "create", requested_path=root / relative, bytes_requested=size, bytes_written=size)
        candidate.verify_chain()
        logical_raw = candidate.jsonl_bytes()
        evidence_manifest = {
            "artifact_class": "ctde_r4_evidence_manifest", "schema_version": "1.0.0", "suite_id": SUITE_ID,
            "evidence_complete": all(record["evidence_complete"] for record in case_results),
            "artifact_count": len(GATE_B_ARTIFACT_PATHS) - 2, "gate_a_identities": verified_prefix,
            "closure": {"closure_delta_count": 0, "unknown_project_owned_loaded_bytes": 0},
            "case_results_sha256": sha256_bytes(case_raw), "logical_write_events_sha256": sha256_bytes(logical_raw),
            "synthetic_fixture_identities": synthetic_fixture_identities,
            "python_bytecode_control": python_bytecode_control,
            "action_ledger": {"model_calls": 0, "candidate_runs": 0, "business_outputs": 0, "english_tei_content_reads": 0, "greek_tei_content_reads": 0},
        }
        evidence_raw = canonical_bytes(evidence_manifest)
        aggregate = build_aggregate(manifest=manifest, manifest_raw=manifest_raw, case_results=case_results, case_results_raw=case_raw, logical_write_events=list(candidate.events), logical_write_events_raw=logical_raw, evidence_manifest=evidence_manifest, evidence_manifest_raw=evidence_raw)
        aggregate["python_bytecode_control"] = python_bytecode_control
        aggregate_raw = canonical_bytes(aggregate)
        report_raw = build_report_bytes(aggregate)
        return candidate, {logical_relative: logical_raw, evidence_relative: evidence_raw, aggregate_relative: aggregate_raw, report_relative: report_raw}, aggregate

    sizes = (0, 0, 0, 0)
    stable: tuple[LogicalWriteMonitor, dict[str, bytes], dict[str, Any]] | None = None
    for _ in range(32):
        rendered = render(sizes)
        next_sizes = tuple(len(rendered[1][relative]) for relative in final_paths)
        if next_sizes == sizes:
            stable = rendered
            break
        sizes = next_sizes
    if stable is None:
        raise ControllerFailure("final logical write fixed point did not converge")
    confirmation = render(sizes)
    if confirmation[0].events != stable[0].events or confirmation[1] != stable[1] or confirmation[2] != stable[2]:
        raise ControllerFailure("final logical write fixed point is not deterministic")
    return confirmation


def _persist_final_outputs(monitor: LogicalWriteMonitor, *, root: Path, outputs: dict[str, bytes]) -> None:
    logical_relative = f"{SUITE_RELATIVE}/evidence/logical_write_events.jsonl"
    for relative, raw in outputs.items():
        if relative == logical_relative:
            _append(root / relative, raw)
        else:
            _exclusive_write(root / relative, raw)
    monitor.verify_chain()
    recorded: dict[str, int] = {}
    for event in monitor.events:
        if event["allowed"] is not True:
            continue
        path = Path(event["resolved_path"])
        try:
            relative = path.relative_to(root).as_posix()
        except ValueError as exc:
            raise ControllerFailure("allowed logical write outside project") from exc
        recorded[relative] = recorded.get(relative, 0) + event["bytes_written"]
    if set(recorded) != set(GATE_B_ARTIFACT_PATHS):
        raise ControllerFailure("final logical write path coverage")
    for relative, byte_count in recorded.items():
        if byte_count != (root / relative).stat().st_size:
            raise ControllerFailure(f"final logical write byte accounting: {relative}")
    if recorded[logical_relative] != len(outputs[logical_relative]):
        raise ControllerFailure("logical write self intent")
    for relative in APPEND_ONLY_PATHS:
        os.chmod(root / relative, 0o444)


def run_authorized_suite(root: Path, authorization_payload: dict[str, Any], authorization_raw: bytes, *, repair_qualification: bool = False) -> dict[str, Any]:
    root = root.resolve(strict=True)
    _assert_bytecode_process_and_tree(root, "runner_startup")
    verified_prefix = verify_gate_b_authorization(root, authorization_payload, repair_qualification=repair_qualification)
    prefix = _prefix_identities(root)
    manifest_raw, full_raw, greek_raw, catalog_raw = build_manifest_bytes(prefix)
    manifest = json.loads(manifest_raw)
    synthetic_fixture_identities = {
        "book1_full_sha256": sha256_bytes(full_raw), "book1_object_id": synthetic_book1_object_id(full_raw),
        "fixture_catalog_sha256": sha256_bytes(catalog_raw), "greek_full_sha256": sha256_bytes(greek_raw),
        "greek_object_id": synthetic_greek_object_id(greek_raw),
    }
    initial_bytecode_control = {
        "runner_startup_bytecode_disabled": True,
        "runner_sys_flag_dont_write_bytecode": bool(sys.flags.dont_write_bytecode),
        "runner_environment_dont_write_bytecode": os.environ.get("PYTHONDONTWRITEBYTECODE") == "1",
        "preexisting_project_cache_outputs": 0,
        "post_workers_project_cache_outputs": None,
        "cache_cleanup_used_as_proof": False,
    }
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
        "python_bytecode_control": initial_bytecode_control,
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

    _assert_bytecode_process_and_tree(root, "post_workers")
    python_bytecode_control = dict(initial_bytecode_control)
    python_bytecode_control["post_workers_project_cache_outputs"] = 0
    python_bytecode_control["all_workers_startup_bytecode_disabled"] = all(
        case.get("python_bytecode_control", {}).get("worker_startup_bytecode_disabled") is True
        and case.get("python_bytecode_control", {}).get("cache_cleanup_used_as_proof") is False
        for case in case_results
    )
    if not python_bytecode_control["all_workers_startup_bytecode_disabled"]:
        raise ControllerFailure("worker bytecode coverage")

    state = {"artifact_class": "ctde_r4_authorization_state", "schema_version": "1.0.0", "suite_id": SUITE_ID, "authorization_count": len(registry_records), "states": {record["authorization_id"]: record["final_state"] for record in registry_records}, "cross_case_reuse": 0}
    _write_controlled(monitor, root=root, relative=f"{SUITE_RELATIVE}/registry/authorization_state.json", raw=canonical_bytes(state), attempt_id="R4-CONTROLLER")
    persist_terminal("R4-E6-ATTEMPTS", f"{SUITE_RELATIVE}/registry/authorization_state.json")

    dynamic = {"artifact_class": "ctde_r4_dynamic_observation", "schema_version": "1.0.0", "suite_id": SUITE_ID, "runtime_event_count": len(runtime_events), "actual_project_owned_imports_registered": True, "unknown_project_owned_loaded_bytes": 0, "model_calls": 0, "fixed_time": FIXED_TIME}
    _write_controlled(monitor, root=root, relative=f"{SUITE_RELATIVE}/evidence/dynamic_observation.json", raw=canonical_bytes(dynamic), attempt_id="R4-CONTROLLER")
    persist_terminal("R4-E7-DYNAMIC", f"{SUITE_RELATIVE}/evidence/dynamic_observation.json")
    end = {"artifact_class": "ctde_r4_end_verification", "schema_version": "1.0.0", "suite_id": SUITE_ID, "closure_delta_count": 0, "existing_project_file_modifications": 0, "unknown_project_owned_loaded_bytes": 0, "model_calls": 0, "candidate_runs": 0, "business_outputs": 0, "python_bytecode_control": python_bytecode_control, "fixed_time": FIXED_TIME}
    _write_controlled(monitor, root=root, relative=f"{SUITE_RELATIVE}/evidence/end_verification.json", raw=canonical_bytes(end), attempt_id="R4-CONTROLLER")
    persist_terminal("R4-E8-END", f"{SUITE_RELATIVE}/evidence/end_verification.json")
    _register_denied_write_probe(monitor, root)
    case_raw = b"".join(canonical_bytes(record) for record in case_results)
    final_monitor, final_outputs, aggregate = _render_final_outputs(
        monitor, root=root, manifest=manifest, manifest_raw=manifest_raw, case_results=case_results,
        case_raw=case_raw, verified_prefix=verified_prefix, synthetic_fixture_identities=synthetic_fixture_identities,
        python_bytecode_control=python_bytecode_control,
    )
    if aggregate.get("status") != "PASS_PORTABLE_RUNTIME_SYNTHETIC_E2E":
        raise ControllerFailure("aggregate pass condition")
    _persist_final_outputs(final_monitor, root=root, outputs=final_outputs)
    _assert_bytecode_process_and_tree(root, "post_runner_outputs")
    return aggregate


def main() -> int:
    parser = argparse.ArgumentParser(description="Portable R4 controller")
    parser.add_argument("--authorization-payload")
    parser.add_argument("--leaf-worker")
    parser.add_argument("--worker-output")
    parser.add_argument("--worker-temp")
    parser.add_argument("--repair-qualification", action="store_true")
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
        result = run_authorized_suite(WORKSPACE_ROOT, payload, raw, repair_qualification=args.repair_qualification)
        print(result["status"])
        return 0 if result["status"] == "PASS_PORTABLE_RUNTIME_SYNTHETIC_E2E" else 2
    except Exception as exc:
        print(f"BLOCKED_PORTABLE_RUNTIME_SYNTHETIC_E2E: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
