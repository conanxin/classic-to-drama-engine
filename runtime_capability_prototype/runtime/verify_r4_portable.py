from __future__ import annotations

import argparse
import ast
import base64
import hashlib
import importlib.metadata
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

import yaml


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
SUITE_ID = "R4PS-20260815-002"
GATE_A_PHASE_ID = "Phase 2-G-R4FRESH-M1"
GATE_B_PHASE_ID = "Phase 2-G-R4FRESH-E2"
PLAN_SHA256 = "c1ddff51020880c22787f75722166656647ac18a0a8dd6b21c8af1d3ade24fb8"
AUDIT_SHA256 = "210f5c1e4e205b1e17e731cb87180d72680d576f97a96e746d8f9fc82fde5b6a"
CONTRACT_SHA256 = "b6b10f5cf06ef596270ae00ebd27343e96556593d05d17f6a0af5930e3615422"
GATE_A_WRITE_SCOPE_SHA256 = "6e25a9fd26f8fbe484692b9e3c3b095fc10cd6f177cf3a38530c360b692fe548"
GATE_B_WRITE_SCOPE_SHA256 = "db661411179360060acec24dd540fdbb29099b68551fb48bd1379ead5c3668ed"
PREDECESSOR_MANIFEST_SHA256 = "56491b3fd08332327e98284a5dce0b482d3d6ae4bd23517204c62fa63fa3a4a5"
PREDECESSOR_PAYLOAD_SHA256 = "703dcba04e0ce669c5472ef4d9b3fc6ed7080eb112e9d5770b3d40c3296e2eca"
PREDECESSOR_COMMIT = "d22ba2c006a8011a2dfe08ee8c81e7d535593423"
REPAIR_ID = "R4R-20260815-001"
REPAIR_PHASE_ID = "Phase 2-G-R4FRESH-R1"
REPAIR_CONTRACT_PATH = "R4_GATE_A_REPAIR_001_CONTRACT.md"
REPAIR_CONTRACT_SHA256 = "a6d7a3fb4a504c2977b98813d6b221b83fcf3eb99d3d67767e7bd527257e7fa2"
REPAIR_PLAN_PATH = "R4_GATE_A_REPAIR_001_PLAN.md"
REPAIR_PLAN_SHA256 = "3bf2fd6e127023468873165cb5cb7e6153aeb167695ecbae9bf3fd7e299d6a61"
REPAIR_RESULT_PATH = "PORTABLE_RUNTIME_R4_PREEXECUTION_CLOSURE_REPAIR_001_RESULT.md"
EXPANDED_REPAIR_SCOPE_SHA256 = "e2812b2d1d9c072b3b6765771142a17bb2c8694339a6bf263c07ad59ee753729"
REPAIR_ROOT = "runtime_capability_prototype/r4_portable_suites/R4PS-20260815-001/repair/R4R-20260815-001"
STANDING_AUTHORIZATION_ID = "CTDE-GOAL-COMPLETION-20260815-001"
RECOVERY_ID = "R4X-20260815-002"
RECOVERY_CONTRACT_PATH = "R4_GATE_B_RECOVERY_001_CONTRACT.md"
RECOVERY_PLAN_PATH = "R4_GATE_B_RECOVERY_001_PLAN.md"
RECOVERY_AUDIT_PATH = "R4_GATE_B_RECOVERY_001_AUDIT.json"
AUTONOMOUS_AUTHORIZATION_PATH = "CTDE_AUTONOMOUS_GOAL_AUTHORIZATION.json"
RECOVERY_ROOT = f"runtime_capability_prototype/r4_portable_suites/{SUITE_ID}/recovery/{RECOVERY_ID}"
PREDECESSOR_FAILURE_CASE_RESULTS_PATH = "runtime_capability_prototype/r4_portable_suites/R4PS-20260815-001/evidence/case_results.jsonl"
PREDECESSOR_FAILURE_CASE_RESULTS_SHA256 = "6122439e551b57fc2eb393567eadd0f05584d726f3aa40ef6095fce2b9e0e260"
TRACKED_PROBE_RELATIVE = "runtime_capability_prototype/bin/consumer_probe"
TRACKED_PROBE_SHA256 = "f1f4849e078169d14ae18c91a5469b171534479dd8255de359f588ca1b475c80"
TRACKED_PROBE_BYTES = 803952
TRACKED_PROBE_MODE = 0o644
TEMPORARY_PROBE_MODE = 0o500

HISTORICAL_GATE_A_SHA256 = {
    "historical_implementation_manifest_sha256": "cbf774e6a3c941b0f3de82905410e6f96adc0b7234e3d322da04d729f4bd03e0",
    "historical_materialization_plan_sha256": "a6ed1c4c7dc289618f3a7abc5d9965b8669206d4121a54ef69a6015c141fe2d0",
    "historical_preexecution_closure_manifest_sha256": "a5c5ae42d0e746bdb8925493a3f8955889093d9a2d09a1d03596a20209406f30",
    "historical_preexecution_closure_payload_sha256": "c48ef58c031f873def12c4230648bb7ae95390cda09bfa340373d654b416b104",
    "historical_preexecution_component_freeze_sha256": "38e0b56973103f76f53263f902a3ab799f7d99124ef09f3251a76aee38e00b6a",
    "historical_preexecution_closure_registry_record_sha256": "ea6b4ef1e36f40de64c998da80ca9a9ccff4bc989254793ccf7e818d27c58260",
    "historical_preexecution_closure_verification_sha256": "2dfd43ed2dab3cd6e0e80cc4f0c98e4e356f8ef27dc11f0575dad049260fbae3",
    "historical_preexecution_closure_result_sha256": "990cd8b3e410a0993103ce62a5842f90a0c03438b1626748084d1e4c7692e4a3",
}

IMPLEMENTATION_PATHS = [
    "runtime_capability_prototype/contracts/r4_portable_e2e_policy_v1.yaml",
    "runtime_capability_prototype/contracts/r4_portable_test_requirements_v1.yaml",
    "runtime_capability_prototype/contracts/r4_portable_test_manifest_schema_v1.yaml",
    "runtime_capability_prototype/contracts/r4_portable_case_result_schema_v1.yaml",
    "runtime_capability_prototype/contracts/r4_portable_logical_write_event_schema_v1.yaml",
    "runtime_capability_prototype/contracts/r4_portable_aggregate_schema_v1.yaml",
    "runtime_capability_prototype/contracts/r4_portable_execution_snapshot_schema_v1.yaml",
    "runtime_capability_prototype/contracts/r4_preexecution_closure_manifest_schema_v1.yaml",
    "runtime_capability_prototype/contracts/r4_preexecution_closure_result_schema_v1.yaml",
    "runtime_capability_prototype/contracts/r4_portable_controller_terminal_schema_v1.yaml",
    "runtime_capability_prototype/runtime/build_r4_preexecution_closure.py",
    "runtime_capability_prototype/runtime/build_r4_portable_manifest.py",
    "runtime_capability_prototype/runtime/monitor_r4_logical_writes.py",
    "runtime_capability_prototype/runtime/verify_r4_portable.py",
    "runtime_capability_prototype/runtime/run_r4_portable.py",
    "runtime_capability_prototype/runtime/build_r4_portable_result.py",
]

GATE_A_ARTIFACT_PATHS = [
    "runtime_capability_prototype/r4_portable_suites/R4PS-20260815-001/control/r4_implementation_manifest.json",
    "runtime_capability_prototype/r4_portable_suites/R4PS-20260815-001/control/r4_materialization_plan.json",
    "runtime_capability_prototype/r4_portable_suites/R4PS-20260815-001/control/r4_preexecution_closure_manifest.json",
    "runtime_capability_prototype/r4_portable_suites/R4PS-20260815-001/control/r4_preexecution_component_freeze.json",
    "runtime_capability_prototype/r4_portable_suites/R4PS-20260815-001/control/r4_preexecution_closure_registry_record.json",
    "runtime_capability_prototype/r4_portable_suites/R4PS-20260815-001/evidence/r4_preexecution_closure_verification.json",
    "PORTABLE_RUNTIME_R4_PREEXECUTION_CLOSURE_RESULT.md",
]

REPAIRED_GATE_A_ARTIFACT_PATHS = [
    f"{RECOVERY_ROOT}/control/r4x_implementation_manifest.json",
    f"{RECOVERY_ROOT}/control/r4x_materialization_plan.json",
    f"{RECOVERY_ROOT}/control/r4x_preexecution_closure_manifest.json",
    f"{RECOVERY_ROOT}/control/r4x_component_freeze.json",
    f"{RECOVERY_ROOT}/control/r4x_closure_registry_record.json",
    f"{RECOVERY_ROOT}/evidence/r4x_temp_gate_b_qualification.json",
    f"{RECOVERY_ROOT}/evidence/r4x_recovery_verification.json",
]

GATE_B_ARTIFACT_PATHS = [
    f"runtime_capability_prototype/r4_portable_suites/{SUITE_ID}/control/r4_test_manifest.json",
    f"runtime_capability_prototype/r4_portable_suites/{SUITE_ID}/control/r4_execution_snapshot.json",
    f"runtime_capability_prototype/r4_portable_suites/{SUITE_ID}/control/r4_snapshot_registry_record.json",
    f"runtime_capability_prototype/r4_portable_suites/{SUITE_ID}/fixtures/synthetic_full_fixture.bin",
    f"runtime_capability_prototype/r4_portable_suites/{SUITE_ID}/fixtures/synthetic_greek_deny.bin",
    f"runtime_capability_prototype/r4_portable_suites/{SUITE_ID}/fixtures/r4_synthetic_fixture_catalog.json",
    f"runtime_capability_prototype/r4_portable_suites/{SUITE_ID}/registry/authorization_registry.jsonl",
    f"runtime_capability_prototype/r4_portable_suites/{SUITE_ID}/registry/authorization_state.json",
    f"runtime_capability_prototype/r4_portable_suites/{SUITE_ID}/registry/registry_events.jsonl",
    f"runtime_capability_prototype/r4_portable_suites/{SUITE_ID}/evidence/controller_terminals.jsonl",
    f"runtime_capability_prototype/r4_portable_suites/{SUITE_ID}/evidence/attempts.jsonl",
    f"runtime_capability_prototype/r4_portable_suites/{SUITE_ID}/evidence/runtime_events.jsonl",
    f"runtime_capability_prototype/r4_portable_suites/{SUITE_ID}/evidence/logical_write_events.jsonl",
    f"runtime_capability_prototype/r4_portable_suites/{SUITE_ID}/evidence/case_results.jsonl",
    f"runtime_capability_prototype/r4_portable_suites/{SUITE_ID}/evidence/start_verification.json",
    f"runtime_capability_prototype/r4_portable_suites/{SUITE_ID}/evidence/dynamic_observation.json",
    f"runtime_capability_prototype/r4_portable_suites/{SUITE_ID}/evidence/end_verification.json",
    f"runtime_capability_prototype/r4_portable_suites/{SUITE_ID}/evidence/evidence_manifest.json",
    f"runtime_capability_prototype/r4_portable_suites/{SUITE_ID}/aggregate/r4_portable_results.json",
    "PORTABLE_RUNTIME_SYNTHETIC_E2E_RESULT_002.md",
]


class VerificationFailure(RuntimeError):
    pass


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8") + b"\n"


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def load_canonical_json(path: Path) -> tuple[dict[str, Any], bytes]:
    raw = path.read_bytes()
    value = json.loads(raw.decode("utf-8"))
    if type(value) is not dict or raw != canonical_bytes(value):
        raise VerificationFailure(f"noncanonical JSON: {path}")
    return value, raw


def load_canonical_jsonl(path: Path) -> tuple[list[dict[str, Any]], bytes]:
    raw = path.read_bytes()
    if raw and not raw.endswith(b"\n"):
        raise VerificationFailure(f"noncanonical JSONL framing: {path}")
    records: list[dict[str, Any]] = []
    rebuilt = bytearray()
    for line in raw.splitlines(keepends=True):
        value = json.loads(line.decode("utf-8"))
        if type(value) is not dict or line != canonical_bytes(value):
            raise VerificationFailure(f"noncanonical JSONL record: {path}")
        records.append(value)
        rebuilt.extend(line)
    if bytes(rebuilt) != raw:
        raise VerificationFailure(f"noncanonical JSONL bytes: {path}")
    return records, raw


def _git(root: Path, *args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=root, text=True).strip()


def _definition_count(path: Path, qualname: str) -> int:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    scope: list[ast.stmt] = tree.body
    parts = qualname.split(".")
    for index, part in enumerate(parts):
        matches = [node for node in scope if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and node.name == part]
        if len(matches) != 1:
            return len(matches)
        if index < len(parts) - 1:
            if not isinstance(matches[0], ast.ClassDef):
                return 0
            scope = matches[0].body
    return 1


def _node_file(root: Path, node: dict[str, Any]) -> Path | None:
    identity = node["identity"]
    candidate = root / identity
    if candidate.is_file() and not candidate.is_symlink():
        return candidate
    if identity.startswith("shared-library:") or identity.startswith("interpreter:"):
        path = Path(identity.split(":", 1)[1])
        return path if path.is_file() else None
    if identity.startswith("python-module:"):
        origin = identity.split(":", 2)[2]
        path = Path(origin)
        return path if path.is_file() else None
    if identity.startswith("distribution:"):
        _, distribution_name, relative = identity.split(":", 2)
        try:
            path = Path(importlib.metadata.distribution(distribution_name).locate_file(relative)).resolve()
        except importlib.metadata.PackageNotFoundError:
            return None
        return path if path.is_file() and not path.is_symlink() else None
    return None


def _verify_manifest_nodes(root: Path, manifest: dict[str, Any]) -> int:
    verified = 0
    node_ids: list[str] = []
    for node in manifest.get("nodes", []):
        required = {"node_id", "classification", "member_type", "identity", "sha256", "bytes"}
        if not required.issubset(node):
            raise VerificationFailure("node required fields")
        expected_id = "N-" + hashlib.sha256(node["identity"].encode("utf-8")).hexdigest()[:20]
        if node["node_id"] != expected_id:
            raise VerificationFailure(f"node ID: {node['identity']}")
        path = _node_file(root, node)
        if path is None:
            descriptor = node.get("virtual_descriptor")
            if type(descriptor) is not dict:
                raise VerificationFailure(f"node bytes unavailable: {node['identity']}")
            raw = canonical_bytes(descriptor)
            actual_digest, actual_bytes = sha256_bytes(raw), len(raw)
        else:
            actual_digest, actual_bytes = sha256_file(path), path.stat().st_size
        if actual_digest != node["sha256"] or actual_bytes != node["bytes"]:
            raise VerificationFailure(f"node drift: {node['identity']}")
        node_ids.append(node["node_id"])
        verified += 1
    if node_ids != sorted(node_ids) or len(node_ids) != len(set(node_ids)):
        raise VerificationFailure("node ordering or uniqueness")
    known = set(node_ids)
    edge_keys = []
    for edge in manifest.get("edges", []):
        key = (edge.get("from_id"), edge.get("to_id"), edge.get("relation"), edge.get("locator"))
        if key[0] not in known or key[1] not in known:
            raise VerificationFailure("edge target resolution")
        edge_keys.append(key)
    if edge_keys != sorted(edge_keys) or len(edge_keys) != len(set(edge_keys)):
        raise VerificationFailure("edge ordering or uniqueness")
    return verified


def _verify_callable_roots(root: Path, manifest: dict[str, Any]) -> int:
    count = 0
    ids: set[str] = set()
    for record in manifest.get("callable_roots", []):
        path = root / record["relative_path"]
        if record["callable_id"] in ids or sha256_file(path) != record["containing_file_sha256"] or _definition_count(path, record["qualname"]) != 1:
            raise VerificationFailure(f"callable root: {record.get('callable_id')}")
        ids.add(record["callable_id"])
        count += 1
    return count


def _actual_untracked_files(root: Path) -> list[str]:
    output = _git(root, "status", "--porcelain=v1", "--untracked-files=all")
    records = output.splitlines() if output else []
    if any(not record.startswith("?? ") for record in records):
        raise VerificationFailure("existing tracked project file modification")
    return sorted(record[3:] for record in records)


def _project_python_cache_outputs(root: Path) -> list[str]:
    outputs: set[str] = set()
    for path in root.rglob("__pycache__"):
        if path.is_dir():
            outputs.add(path.relative_to(root).as_posix() + "/")
    for path in root.rglob("*.pyc"):
        if path.is_file():
            outputs.add(path.relative_to(root).as_posix())
    return sorted(outputs)


def _assert_verifier_bytecode_boundary(root: Path, stage: str) -> int:
    if not sys.flags.dont_write_bytecode or os.environ.get("PYTHONDONTWRITEBYTECODE") != "1":
        raise VerificationFailure(f"verifier bytecode startup protection: {stage}")
    outputs = _project_python_cache_outputs(root)
    if outputs:
        raise VerificationFailure(f"project Python cache output at {stage}: {outputs}")
    return 0


def verify_preexecution_bundle(
    *,
    root: Path,
    implementation_path: Path,
    materialization_path: Path,
    closure_path: Path,
    component_freeze_path: Path,
    registry_path: Path,
    builder_pass_a: Path,
    builder_pass_b: Path,
) -> dict[str, Any]:
    root = root.resolve(strict=True)
    implementation, implementation_raw = load_canonical_json(implementation_path)
    materialization, materialization_raw = load_canonical_json(materialization_path)
    closure, closure_raw = load_canonical_json(closure_path)
    freeze, freeze_raw = load_canonical_json(component_freeze_path)
    registry, registry_raw = load_canonical_json(registry_path)
    pass_a = builder_pass_a.read_bytes()
    pass_b = builder_pass_b.read_bytes()
    if pass_a != pass_b or pass_a != closure_raw:
        raise VerificationFailure("two-pass closure bytes differ")
    if implementation.get("bundle_file_count") != 16 or [item.get("path") for item in implementation.get("files", [])] != IMPLEMENTATION_PATHS:
        raise VerificationFailure("implementation inventory")
    for record in implementation["files"]:
        path = root / record["path"]
        if not path.is_file() or path.is_symlink() or path.stat().st_size != record["bytes"] or sha256_file(path) != record["sha256"]:
            raise VerificationFailure(f"implementation identity: {record['path']}")
    expected_final = IMPLEMENTATION_PATHS + GATE_A_ARTIFACT_PATHS
    if materialization.get("creatable_files") != expected_final or materialization.get("mutable_existing_files") != []:
        raise VerificationFailure("materialization exact write scope")
    if materialization.get("gate_a_write_scope_sha256") != GATE_A_WRITE_SCOPE_SHA256:
        raise VerificationFailure("Gate A scope digest")
    if sha256_file(root / "FRESH_R4_SYNTHETIC_E2E_PLAN.md") != PLAN_SHA256 or sha256_file(root / "FRESH_R4_CURRENT_TREE_AUDIT.json") != AUDIT_SHA256 or sha256_file(root / "FRESH_R4_SYNTHETIC_E2E_MACHINE_CONTRACT.md") != CONTRACT_SHA256:
        raise VerificationFailure("formal identity drift")
    payload = {key: value for key, value in closure.items() if key != "closure_payload_sha256"}
    if closure.get("closure_payload_sha256") != sha256_bytes(canonical_bytes(payload)):
        raise VerificationFailure("closure payload digest")
    if closure.get("suite_id") != SUITE_ID or closure.get("phase_id") != GATE_A_PHASE_ID:
        raise VerificationFailure("closure phase identity")
    verified_nodes = _verify_manifest_nodes(root, closure)
    callable_count = _verify_callable_roots(root, closure)
    predecessor_path = root / "runtime_capability_prototype/r3_portable_suites/R3PS-20260814-001/control/runtime_transitive_closure_manifest.json"
    predecessor, predecessor_raw = load_canonical_json(predecessor_path)
    if sha256_bytes(predecessor_raw) != PREDECESSOR_MANIFEST_SHA256 or predecessor.get("closure_payload_sha256") != PREDECESSOR_PAYLOAD_SHA256:
        raise VerificationFailure("predecessor closure identity")
    refreshed_lookup = {node["node_id"]: node for node in closure["nodes"]}
    if any(refreshed_lookup.get(node["node_id"]) != node for node in predecessor["nodes"]):
        raise VerificationFailure("predecessor closure not exact subset")
    if [role.get("gap_id") for role in closure.get("roles", [])] != [
        "R3G-01-PORTABLE-R4-SUITE-MANIFEST-BUILDER",
        "R3G-02-PORTABLE-R4-SUITE-RUNNER",
        "R3G-05-PORTABLE-LOGICAL-WRITE-MONITOR",
        "R3G-06-PORTABLE-R4-AGGREGATE-REPORT-GENERATOR",
    ]:
        raise VerificationFailure("R4 role inventory")
    if freeze.get("members") != closure["nodes"] or freeze.get("closure_manifest_sha256") != sha256_bytes(closure_raw) or freeze.get("closure_payload_sha256") != closure["closure_payload_sha256"] or freeze.get("implementation_manifest_sha256") != sha256_bytes(implementation_raw):
        raise VerificationFailure("component freeze")
    expected_registry = {
        "implementation_manifest_sha256": sha256_bytes(implementation_raw),
        "materialization_plan_sha256": sha256_bytes(materialization_raw),
        "closure_manifest_sha256": sha256_bytes(closure_raw),
        "closure_payload_sha256": closure["closure_payload_sha256"],
        "component_freeze_sha256": sha256_bytes(freeze_raw),
    }
    for key, value in expected_registry.items():
        if registry.get(key) != value:
            raise VerificationFailure(f"registry identity: {key}")
    if registry.get("registry_pass") != "independent_controller_rehash" or registry.get("suite_id") != SUITE_ID:
        raise VerificationFailure("registry status")
    prefix_expected = sorted(set(expected_final) - {GATE_A_ARTIFACT_PATHS[-2], GATE_A_ARTIFACT_PATHS[-1]})
    actual_untracked = _actual_untracked_files(root)
    if actual_untracked != prefix_expected:
        raise VerificationFailure("M6 exact created prefix")
    if any((root / path).exists() for path in GATE_B_ARTIFACT_PATHS):
        raise VerificationFailure("Gate B artifact exists")
    discovery = closure["discovery"]
    action_ledger = closure["action_ledger"]
    zero_actions = all(value == 0 for value in action_ledger.values())
    if not zero_actions:
        raise VerificationFailure("forbidden action ledger")
    if discovery.get("unknown_dynamic_dependency_count") != 0 or discovery.get("unknown_project_owned_loaded_bytes") != 0 or discovery.get("unresolved_symlinks") != 0:
        raise VerificationFailure("unresolved closure inventory")
    evidence = {
        "artifact_class": "ctde_r4_preexecution_closure_verification",
        "schema_version": "1.0.0",
        "suite_id": SUITE_ID,
        "phase_id": GATE_A_PHASE_ID,
        "status": "PASS_R4_PREEXECUTION_TRANSITIVE_CLOSURE_REFRESH",
        "implementation_file_count": len(implementation["files"]),
        "expected_created_paths": expected_final,
        "actual_created_paths": prefix_expected,
        "predecessor_node_count": len(predecessor["nodes"]),
        "refreshed_node_count": len(closure["nodes"]),
        "refreshed_edge_count": len(closure["edges"]),
        "verified_node_count": verified_nodes,
        "verified_callable_root_count": callable_count,
        "deterministic_build_count": 2,
        "deterministic_builds_byte_identical": True,
        "existing_project_file_modifications": 0,
        "unknown_dynamic_dependency_count": discovery["unknown_dynamic_dependency_count"],
        "unknown_project_owned_loaded_bytes": discovery["unknown_project_owned_loaded_bytes"],
        "unresolved_symlinks": discovery["unresolved_symlinks"],
        "scope_violations": 0,
        "action_ledger": action_ledger,
        "independently_rehashed": True,
        "evidence": {
            "implementation_manifest_sha256": sha256_bytes(implementation_raw),
            "materialization_plan_sha256": sha256_bytes(materialization_raw),
            "closure_manifest_sha256": sha256_bytes(closure_raw),
            "closure_payload_sha256": closure["closure_payload_sha256"],
            "component_freeze_sha256": sha256_bytes(freeze_raw),
            "closure_registry_record_sha256": sha256_bytes(registry_raw),
            "builder_pass_a_sha256": sha256_bytes(pass_a),
            "builder_pass_b_sha256": sha256_bytes(pass_b),
            "predecessor_closure_manifest_sha256": PREDECESSOR_MANIFEST_SHA256,
            "predecessor_closure_payload_sha256": PREDECESSOR_PAYLOAD_SHA256,
        },
    }
    return evidence


def verify_recovery_prefix(root: Path) -> dict[str, Any]:
    root = root.resolve(strict=True)
    _assert_verifier_bytecode_boundary(root, "recovery_prefix_start")
    implementation, implementation_raw = load_canonical_json(root / REPAIRED_GATE_A_ARTIFACT_PATHS[0])
    materialization, materialization_raw = load_canonical_json(root / REPAIRED_GATE_A_ARTIFACT_PATHS[1])
    closure, closure_raw = load_canonical_json(root / REPAIRED_GATE_A_ARTIFACT_PATHS[2])
    freeze, freeze_raw = load_canonical_json(root / REPAIRED_GATE_A_ARTIFACT_PATHS[3])
    registry, registry_raw = load_canonical_json(root / REPAIRED_GATE_A_ARTIFACT_PATHS[4])
    if implementation.get("suite_id") != SUITE_ID or implementation.get("recovery_id") != RECOVERY_ID or implementation.get("standing_authorization_id") != STANDING_AUTHORIZATION_ID:
        raise VerificationFailure("recovery implementation identity")
    files = implementation.get("files")
    if type(files) is not list or implementation.get("bundle_file_count") != len(files) or len(files) != 17:
        raise VerificationFailure("recovery implementation inventory")
    for record in files:
        path = root / record.get("path", "")
        if not path.is_file() or path.is_symlink() or path.stat().st_size != record.get("bytes") or sha256_file(path) != record.get("sha256"):
            raise VerificationFailure(f"recovery implementation drift: {record.get('path')}")
    expected_materialization = {
        "suite_id": SUITE_ID,
        "recovery_id": RECOVERY_ID,
        "standing_authorization_id": STANDING_AUTHORIZATION_ID,
        "phase_id": "Phase 2-G-R4FRESH-M2",
        "phase_kind": "r4_versioned_recovery_implementation_and_preexecution_closure_refresh",
        "gate_a_write_scope_sha256": "8b30132ddd1c2c819adcb73269c3dd65601a94d5a80839bbec313059a82acdba",
        "implementation_manifest_sha256": sha256_bytes(implementation_raw),
        "execution_authorized": True,
        "gate_b_execution_authorized": False,
    }
    if any(materialization.get(key) != value for key, value in expected_materialization.items()):
        raise VerificationFailure("recovery materialization identity")
    builder = root / "runtime_capability_prototype/runtime/build_r4_preexecution_closure.py"
    command = [
        sys.executable,
        "-B",
        str(builder),
        "--implementation-manifest",
        str(root / REPAIRED_GATE_A_ARTIFACT_PATHS[0]),
        "--materialization-plan",
        str(root / REPAIRED_GATE_A_ARTIFACT_PATHS[1]),
    ]
    environment = os.environ.copy()
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    pass_a = subprocess.check_output(command, cwd=root, env=environment)
    pass_b = subprocess.check_output(command, cwd=root, env=environment)
    if pass_a != pass_b or pass_a != closure_raw:
        raise VerificationFailure("recovery closure independent deterministic builds")
    if closure.get("suite_id") != SUITE_ID or closure.get("phase_id") != "Phase 2-G-R4FRESH-M2":
        raise VerificationFailure("recovery closure identity")
    verified_nodes = _verify_manifest_nodes(root, closure)
    if freeze.get("closure_manifest_sha256") != sha256_bytes(closure_raw) or freeze.get("closure_payload_sha256") != closure.get("closure_payload_sha256") or freeze.get("implementation_manifest_sha256") != sha256_bytes(implementation_raw) or freeze.get("members") != closure.get("nodes"):
        raise VerificationFailure("recovery component freeze")
    if registry.get("closure_manifest_sha256") != sha256_bytes(closure_raw) or registry.get("closure_payload_sha256") != closure.get("closure_payload_sha256") or registry.get("component_freeze_sha256") != sha256_bytes(freeze_raw) or registry.get("implementation_manifest_sha256") != sha256_bytes(implementation_raw) or registry.get("materialization_plan_sha256") != sha256_bytes(materialization_raw) or registry.get("deterministic_builds_byte_identical") is not True:
        raise VerificationFailure("recovery registry record")
    _assert_verifier_bytecode_boundary(root, "recovery_prefix_end")
    return {
        "artifact_class": "ctde_r4_recovery_prefix_verification",
        "schema_version": "1.0.0",
        "status": "PASS_R4_RECOVERY_PREFIX_VERIFICATION",
        "standing_authorization_id": STANDING_AUTHORIZATION_ID,
        "recovery_id": RECOVERY_ID,
        "suite_id": SUITE_ID,
        "implementation_manifest_sha256": sha256_bytes(implementation_raw),
        "materialization_plan_sha256": sha256_bytes(materialization_raw),
        "closure_manifest_sha256": sha256_bytes(closure_raw),
        "closure_payload_sha256": closure["closure_payload_sha256"],
        "component_freeze_sha256": sha256_bytes(freeze_raw),
        "registry_record_sha256": sha256_bytes(registry_raw),
        "verified_closure_nodes": verified_nodes,
        "deterministic_build_count": 2,
        "project_python_bytecode_outputs": 0,
    }


def _verify_standing_recovery_authorization(
    root: Path,
    payload: dict[str, Any],
    *,
    qualification_only: bool,
) -> dict[str, str]:
    expected = {
        "standing_authorization_id": STANDING_AUTHORIZATION_ID,
        "recovery_id": RECOVERY_ID,
        "predecessor_suite_id": "R4PS-20260815-001",
        "suite_id": SUITE_ID,
        "phase_id": GATE_B_PHASE_ID,
        "phase_kind": "portable_r4_versioned_recovery_synthetic_e2e",
        "gate_b_write_scope_sha256": GATE_B_WRITE_SCOPE_SHA256,
        "authorization_payload_complete": True,
        "qualification_only": qualification_only,
        "current_status": "AUTHORIZED_R4_RECOVERY_TEMP_QUALIFICATION" if qualification_only else "AUTHORIZED_R4_SUCCESSOR_EXECUTION",
        "approval_scope": (
            "one fresh OS-temporary full R4 recovery qualification; no source semantic reads, Candidate runs, model calls, or business outputs"
            if qualification_only
            else "one formal versioned R4 successor execution under CTDE-GOAL-COMPLETION-20260815-001; no source semantic reads, Candidate runs, model calls, or business outputs"
        ),
    }
    for key, value in expected.items():
        if payload.get(key) != value:
            raise VerificationFailure(f"standing recovery authorization mismatch: {key}")
    if payload.get("git_head") != _git(root, "rev-parse", "HEAD"):
        raise VerificationFailure("standing recovery Git identity")
    governance_paths = {
        "governance_authorization_sha256": AUTONOMOUS_AUTHORIZATION_PATH,
        "recovery_contract_sha256": RECOVERY_CONTRACT_PATH,
        "recovery_plan_sha256": RECOVERY_PLAN_PATH,
        "recovery_audit_sha256": RECOVERY_AUDIT_PATH,
    }
    verified: dict[str, str] = {}
    for key, relative in governance_paths.items():
        actual = sha256_file(root / relative)
        if payload.get(key) != actual:
            raise VerificationFailure(f"standing recovery governance identity: {key}")
        verified[key] = actual
    authorization, _ = load_canonical_json(root / AUTONOMOUS_AUTHORIZATION_PATH)
    audit, _ = load_canonical_json(root / RECOVERY_AUDIT_PATH)
    if authorization.get("standing_authorization_id") != STANDING_AUTHORIZATION_ID or authorization.get("status") != "ACTIVE":
        raise VerificationFailure("standing authorization artifact")
    if audit.get("standing_authorization_id") != STANDING_AUTHORIZATION_ID or audit.get("failure_evidence_sha256") != PREDECESSOR_FAILURE_CASE_RESULTS_SHA256:
        raise VerificationFailure("standing recovery audit binding")
    predecessor_failure = root / PREDECESSOR_FAILURE_CASE_RESULTS_PATH
    if predecessor_failure.exists():
        if sha256_file(predecessor_failure) != PREDECESSOR_FAILURE_CASE_RESULTS_SHA256:
            raise VerificationFailure("predecessor formal failure evidence drift")
    elif not qualification_only:
        raise VerificationFailure("predecessor formal failure evidence absent")
    prefix_paths = {
        "active_implementation_manifest_sha256": REPAIRED_GATE_A_ARTIFACT_PATHS[0],
        "active_materialization_plan_sha256": REPAIRED_GATE_A_ARTIFACT_PATHS[1],
        "active_closure_manifest_sha256": REPAIRED_GATE_A_ARTIFACT_PATHS[2],
        "active_component_freeze_sha256": REPAIRED_GATE_A_ARTIFACT_PATHS[3],
        "active_registry_record_sha256": REPAIRED_GATE_A_ARTIFACT_PATHS[4],
    }
    if not qualification_only:
        prefix_paths.update(
            {
                "recovery_qualification_sha256": REPAIRED_GATE_A_ARTIFACT_PATHS[5],
                "recovery_verification_sha256": REPAIRED_GATE_A_ARTIFACT_PATHS[6],
            }
        )
    for key, relative in prefix_paths.items():
        actual = sha256_file(root / relative)
        if payload.get(key) != actual:
            raise VerificationFailure(f"standing recovery prefix identity: {key}")
        verified[key] = actual
    closure, _ = load_canonical_json(root / REPAIRED_GATE_A_ARTIFACT_PATHS[2])
    if payload.get("active_closure_payload_sha256") != closure.get("closure_payload_sha256"):
        raise VerificationFailure("standing recovery closure payload")
    verified["active_closure_payload_sha256"] = closure["closure_payload_sha256"]
    if any((root / path).exists() for path in GATE_B_ARTIFACT_PATHS):
        raise VerificationFailure("successor Gate B partial materialization")
    return verified


def verify_gate_b_authorization(root: Path, payload: dict[str, Any], *, repair_qualification: bool = False) -> dict[str, str]:
    root = root.resolve(strict=True)
    _assert_verifier_bytecode_boundary(root, "authorization_start")
    if payload.get("standing_authorization_id") == STANDING_AUTHORIZATION_ID:
        verified = _verify_standing_recovery_authorization(root, payload, qualification_only=repair_qualification)
        _assert_verifier_bytecode_boundary(root, "authorization_end")
        return verified
    expected_static = {
        "plan_path": "FRESH_R4_SYNTHETIC_E2E_PLAN.md",
        "plan_sha256": PLAN_SHA256,
        "current_tree_audit_sha256": AUDIT_SHA256,
        "phase_id": GATE_B_PHASE_ID,
        "phase_kind": "portable_r4_fresh_synthetic_e2e_deterministic_execution",
        "suite_id": SUITE_ID,
        "repair_id": REPAIR_ID,
        "repair_scope_sha256": EXPANDED_REPAIR_SCOPE_SHA256,
        "repair_contract_path": REPAIR_CONTRACT_PATH,
        "repair_contract_sha256": REPAIR_CONTRACT_SHA256,
        "repair_plan_path": REPAIR_PLAN_PATH,
        "repair_plan_sha256": REPAIR_PLAN_SHA256,
        "gate_b_write_scope_sha256": GATE_B_WRITE_SCOPE_SHA256,
    }
    expected_static.update(
        {
            "current_status": "AUTHORIZED_R4_REPAIR_TEMP_GATE_B_QUALIFICATION",
            "qualification_only": True,
            "qualification_attempt_ordinal": 3,
            "attempts_authorized_total": 3,
            "approval_scope": "one third fresh OS-temporary full Gate B qualification for R4R-20260815-001 D01-D08 only; not formal Gate B execution",
        }
        if repair_qualification
        else {
            "current_status": "READY_FOR_PORTABLE_R4_SYNTHETIC_E2E_EXECUTION_AUTHORIZATION_REVIEW",
            "qualification_only": False,
            "approval_scope": "one Portable R4 fresh synthetic E2E execution attempt only; no Candidate, source read, model call, or business output",
            "authorization_payload_complete": True,
        }
    )
    for key, value in expected_static.items():
        if payload.get(key) != value:
            raise VerificationFailure(f"Gate B authorization mismatch: {key}")
    if sha256_file(root / REPAIR_CONTRACT_PATH) != REPAIR_CONTRACT_SHA256 or sha256_file(root / REPAIR_PLAN_PATH) != REPAIR_PLAN_SHA256:
        raise VerificationFailure("repair Contract/Plan identity")
    if payload.get("repair_commit_sha") != _git(root, "rev-parse", "HEAD"):
        raise VerificationFailure("repair commit identity")
    historical_paths = {
        "historical_implementation_manifest_sha256": GATE_A_ARTIFACT_PATHS[0],
        "historical_materialization_plan_sha256": GATE_A_ARTIFACT_PATHS[1],
        "historical_preexecution_closure_manifest_sha256": GATE_A_ARTIFACT_PATHS[2],
        "historical_preexecution_component_freeze_sha256": GATE_A_ARTIFACT_PATHS[3],
        "historical_preexecution_closure_registry_record_sha256": GATE_A_ARTIFACT_PATHS[4],
        "historical_preexecution_closure_verification_sha256": GATE_A_ARTIFACT_PATHS[5],
        "historical_preexecution_closure_result_sha256": GATE_A_ARTIFACT_PATHS[6],
    }
    for key, relative in historical_paths.items():
        expected = HISTORICAL_GATE_A_SHA256[key]
        if payload.get(key) != expected or sha256_file(root / relative) != expected:
            raise VerificationFailure(f"historical Gate A identity: {key}")
    historical_closure, _ = load_canonical_json(root / GATE_A_ARTIFACT_PATHS[2])
    expected_historical_payload = HISTORICAL_GATE_A_SHA256["historical_preexecution_closure_payload_sha256"]
    if payload.get("historical_preexecution_closure_payload_sha256") != expected_historical_payload or historical_closure.get("closure_payload_sha256") != expected_historical_payload:
        raise VerificationFailure("historical Gate A closure payload identity")
    prefix_paths = {
        "repaired_implementation_manifest_sha256": REPAIRED_GATE_A_ARTIFACT_PATHS[0],
        "repaired_materialization_plan_sha256": REPAIRED_GATE_A_ARTIFACT_PATHS[1],
        "repaired_closure_manifest_sha256": REPAIRED_GATE_A_ARTIFACT_PATHS[2],
        "repaired_component_freeze_sha256": REPAIRED_GATE_A_ARTIFACT_PATHS[3],
        "repaired_registry_record_sha256": REPAIRED_GATE_A_ARTIFACT_PATHS[4],
    }
    if not repair_qualification:
        prefix_paths.update(
            {
                "repair_qualification_sha256": REPAIRED_GATE_A_ARTIFACT_PATHS[5],
                "repaired_verification_sha256": REPAIRED_GATE_A_ARTIFACT_PATHS[6],
            }
        )
    verified: dict[str, str] = {}
    for key, relative in prefix_paths.items():
        actual = sha256_file(root / relative)
        if payload.get(key) != actual:
            raise VerificationFailure(f"Gate B repaired digest mismatch: {key}")
        verified[key] = actual
    closure, _ = load_canonical_json(root / REPAIRED_GATE_A_ARTIFACT_PATHS[2])
    if payload.get("repaired_closure_payload_sha256") != closure.get("closure_payload_sha256"):
        raise VerificationFailure("Gate B repaired closure payload mismatch")
    verified["repaired_closure_payload_sha256"] = closure["closure_payload_sha256"]
    if not repair_qualification:
        if payload.get("repair_result_path") != REPAIR_RESULT_PATH or payload.get("repair_result_sha256") != sha256_file(root / REPAIR_RESULT_PATH):
            raise VerificationFailure("repair result identity")
    if any((root / path).exists() for path in GATE_B_ARTIFACT_PATHS):
        raise VerificationFailure("Gate B partial materialization")
    _assert_verifier_bytecode_boundary(root, "authorization_end")
    return verified


def verify_gate_b_outputs(root: Path) -> dict[str, Any]:
    root = root.resolve(strict=True)
    pre_verifier_cache_count = _assert_verifier_bytecode_boundary(root, "gate_b_result_start")
    expected_outputs = sorted(GATE_B_ARTIFACT_PATHS)
    if _actual_untracked_files(root) != expected_outputs:
        raise VerificationFailure("Gate B exact output scope")

    tracked_probe = root / TRACKED_PROBE_RELATIVE
    tracked_probe_digest = sha256_file(tracked_probe)
    tracked_probe_bytes = tracked_probe.stat().st_size
    tracked_probe_mode = tracked_probe.stat().st_mode & 0o777
    if tracked_probe.is_symlink() or tracked_probe_digest != TRACKED_PROBE_SHA256 or tracked_probe_bytes != TRACKED_PROBE_BYTES or tracked_probe_mode != TRACKED_PROBE_MODE:
        raise VerificationFailure("tracked probe frozen identity")
    active_closure, _ = load_canonical_json(root / REPAIRED_GATE_A_ARTIFACT_PATHS[2])
    probe_nodes = [node for node in active_closure.get("nodes", []) if node.get("identity") == TRACKED_PROBE_RELATIVE]
    if len(probe_nodes) != 1 or probe_nodes[0].get("sha256") != tracked_probe_digest or probe_nodes[0].get("bytes") != tracked_probe_bytes:
        raise VerificationFailure("tracked probe active closure binding")

    manifest, manifest_raw = load_canonical_json(root / GATE_B_ARTIFACT_PATHS[0])
    snapshot, _ = load_canonical_json(root / GATE_B_ARTIFACT_PATHS[1])
    catalog, catalog_raw = load_canonical_json(root / GATE_B_ARTIFACT_PATHS[5])
    authorizations, _ = load_canonical_jsonl(root / GATE_B_ARTIFACT_PATHS[6])
    attempts, _ = load_canonical_jsonl(root / GATE_B_ARTIFACT_PATHS[10])
    runtime_events, _ = load_canonical_jsonl(root / GATE_B_ARTIFACT_PATHS[11])
    writes, writes_raw = load_canonical_jsonl(root / GATE_B_ARTIFACT_PATHS[12])
    cases, cases_raw = load_canonical_jsonl(root / GATE_B_ARTIFACT_PATHS[13])
    end_verification, _ = load_canonical_json(root / GATE_B_ARTIFACT_PATHS[16])
    evidence, evidence_raw = load_canonical_json(root / GATE_B_ARTIFACT_PATHS[17])
    aggregate, _ = load_canonical_json(root / GATE_B_ARTIFACT_PATHS[18])

    groups, leaves = manifest.get("requirement_groups"), manifest.get("leaves")
    if type(groups) is not list or type(leaves) is not list or len(groups) != 37 or len(set(groups)) != 37 or not leaves:
        raise VerificationFailure("Gate B manifest inventory")
    leaf_count = len(leaves)
    leaf_ids = [leaf.get("leaf_id") for leaf in leaves]
    attempt_ids = [leaf.get("attempt_id") for leaf in leaves]
    authorization_ids = [leaf.get("authorization_id") for leaf in leaves if leaf.get("authorization_id") is not None]
    scenario_keys = [(leaf.get("group_id"), leaf.get("scenario"), leaf.get("leaf_id")) for leaf in leaves]
    if len(set(leaf_ids)) != leaf_count or len(set(attempt_ids)) != leaf_count or len(set(authorization_ids)) != len(authorization_ids) or len(set(scenario_keys)) != leaf_count:
        raise VerificationFailure("Gate B fresh leaf identities")
    if len(attempts) != leaf_count or len(runtime_events) != leaf_count or len(cases) != leaf_count or [item.get("leaf_id") for item in cases] != leaf_ids:
        raise VerificationFailure("Gate B leaf execution coverage")
    if not all(item.get("disposition") == "pass" and item.get("evidence_complete") is True and item.get("observed_terminal") == item.get("expected_terminal") for item in cases):
        raise VerificationFailure("Gate B leaf result")

    group_pattern = re.compile(r"^RCPT-T([0-9]{2})-[A-Z0-9-]+$")
    parsed = []
    for group in groups:
        match = group_pattern.fullmatch(group) if type(group) is str else None
        if match is None or not 1 <= int(match.group(1)) <= 37:
            raise VerificationFailure("Gate B requirement group parser")
        parsed.append(int(match.group(1)))
    if sorted(parsed) != list(range(1, 38)):
        raise VerificationFailure("Gate B requirement group number coverage")
    malformed = ["RCPT-01-X", "RCPT-T1-X", "RCPT-T00-X", "RCPT-T38-X", "RCPT-TAA-X", "RCPT-T01", "XRCPT-T01-X", "RCPT-T01-x"]
    if any((match := group_pattern.fullmatch(value)) is not None and 1 <= int(match.group(1)) <= 37 for value in malformed):
        raise VerificationFailure("Gate B malformed group acceptance")

    full_path, greek_path = root / GATE_B_ARTIFACT_PATHS[3], root / GATE_B_ARTIFACT_PATHS[4]
    full_raw, greek_raw = full_path.read_bytes(), greek_path.read_bytes()
    full_digest, greek_digest = sha256_bytes(full_raw), sha256_bytes(greek_raw)
    book_object_id = f"urn:ctde:fixture:{full_digest}"
    greek_object_id = f"urn:ctde:fixture-greek-deny:{greek_digest}"
    fixtures = catalog.get("fixtures")
    if type(fixtures) is not list or len(fixtures) != 2 or manifest.get("fixture_recipes") != fixtures:
        raise VerificationFailure("Gate B fixture catalog binding")
    by_recipe = {item.get("recipe_id"): item for item in fixtures}
    book_record, greek_record = by_recipe.get("CTDE-R4-SYNTHETIC-BOOK1-1"), by_recipe.get("CTDE-R4-SYNTHETIC-GREEK-DENY-1")
    if type(book_record) is not dict or type(greek_record) is not dict:
        raise VerificationFailure("Gate B fixture recipe identity")
    if book_record.get("object_id") != book_object_id or book_record.get("sha256") != full_digest or book_record.get("bytes") != len(full_raw):
        raise VerificationFailure("Gate B Book fixture identity")
    if greek_record.get("object_id") != greek_object_id or greek_record.get("sha256") != greek_digest or greek_record.get("bytes") != len(greek_raw) or greek_record.get("authorization_allowed") is not False:
        raise VerificationFailure("Gate B Greek fixture identity")
    if book_object_id == greek_object_id or len(full_raw) != 40960 or len(greek_raw) != 4096:
        raise VerificationFailure("Gate B fixture identity separation")
    markers = book_record.get("marker_offsets")
    expected_markers = {"BOOK_01": b'<BOOK_01 xmlns="urn:ctde:synthetic">'}
    expected_markers.update({f"CARD_{index:02d}": f"<CARD_{index:02d}>".encode() for index in range(1, 11)})
    expected_markers.update({f"PARAGRAPH_{index:02d}": f"<PARA_{index:02d}/>".encode() for index in range(1, 11)})
    if type(markers) is not dict or len(markers) != 21 or len(set(markers.values())) != 21:
        raise VerificationFailure("Gate B synthetic marker catalog")
    for label, marker in expected_markers.items():
        offset = markers.get(label)
        if type(offset) is not int or not 4076 <= offset < 36515 or full_raw[offset:offset + len(marker)] != marker or full_raw[4076:36515].count(marker) != 1:
            raise VerificationFailure(f"Gate B marker identity: {label}")

    placeholder = "urn:ctde:fixture-greek-deny:" + "synthetic"
    active_paths = [
        "runtime_capability_prototype/runtime/build_r4_portable_manifest.py",
        "runtime_capability_prototype/runtime/run_r4_portable.py",
        "runtime_capability_prototype/runtime/verify_r4_portable.py",
    ]
    active_placeholder_occurrences = sum((root / path).read_text(encoding="utf-8").count(placeholder) for path in active_paths)
    if active_placeholder_occurrences != 0:
        raise VerificationFailure("historical Greek placeholder active")

    cases_by_leaf = {item["leaf_id"]: item for item in cases}
    events_by_leaf = {item["leaf_id"]: item for item in runtime_events}
    authorization_by_leaf: dict[str, dict[str, Any]] = {}
    for record in authorizations:
        raw = base64.b64decode(record.get("authorization_exact_bytes_b64", ""), validate=True)
        if sha256_bytes(raw) != record.get("authorization_sha256") or len(raw) != record.get("authorization_bytes"):
            raise VerificationFailure("Gate B authorization custody bytes")
        authorization = yaml.safe_load(raw.decode("utf-8"))
        if type(authorization) is not dict or authorization.get("authorization_id") != record.get("authorization_id") or authorization.get("attempt_id") != record.get("attempt_id"):
            raise VerificationFailure("Gate B authorization custody identity")
        authorization_by_leaf[record["leaf_id"]] = authorization
    if len(authorization_by_leaf) != len(authorization_ids):
        raise VerificationFailure("Gate B authorization custody coverage")

    snapshot_bytecode = snapshot.get("python_bytecode_control")
    if type(snapshot_bytecode) is not dict or snapshot_bytecode.get("runner_startup_bytecode_disabled") is not True or snapshot_bytecode.get("preexisting_project_cache_outputs") != 0 or snapshot_bytecode.get("cache_cleanup_used_as_proof") is not False:
        raise VerificationFailure("Gate B runner startup bytecode evidence")
    expected_namespace = {
        "runner_user_namespace_bootstrapped": True,
        "runner_effective_uid": 0,
        "runner_effective_gid": 0,
        "runner_setgroups_policy": "deny",
        "runner_userns_bootstrap_utility": "/usr/bin/unshare",
    }
    if any(snapshot_bytecode.get(key) != value for key, value in expected_namespace.items()):
        raise VerificationFailure("Gate B runner user namespace evidence")
    for key in ("runner_uid_map", "runner_gid_map"):
        mapping = snapshot_bytecode.get(key)
        if type(mapping) is not list or len(mapping) != 3 or mapping[0] != 0 or mapping[2] != 1 or type(mapping[1]) is not int or mapping[1] < 0:
            raise VerificationFailure(f"Gate B runner single-ID map: {key}")
    if snapshot_bytecode.get("runner_outer_uid") != snapshot_bytecode["runner_uid_map"][1] or snapshot_bytecode.get("runner_outer_gid") != snapshot_bytecode["runner_gid_map"][1]:
        raise VerificationFailure("Gate B runner outer identity binding")
    final_bytecode = end_verification.get("python_bytecode_control")
    if type(final_bytecode) is not dict or final_bytecode.get("post_workers_project_cache_outputs") != 0 or final_bytecode.get("all_workers_startup_bytecode_disabled") is not True or final_bytecode.get("cache_cleanup_used_as_proof") is not False:
        raise VerificationFailure("Gate B post-worker bytecode evidence")
    if evidence.get("python_bytecode_control") != final_bytecode or aggregate.get("python_bytecode_control") != final_bytecode:
        raise VerificationFailure("Gate B bytecode evidence binding")

    probe_records = []
    t16_records = []
    for leaf in leaves:
        case, event = cases_by_leaf[leaf["leaf_id"]], events_by_leaf[leaf["leaf_id"]]
        case_bytecode, event_bytecode = case.get("python_bytecode_control"), event.get("python_bytecode_control")
        if type(case_bytecode) is not dict or case_bytecode != event_bytecode or case_bytecode.get("worker_startup_bytecode_disabled") is not True or case_bytecode.get("worker_sys_flag_dont_write_bytecode") is not True or case_bytecode.get("worker_environment_dont_write_bytecode") is not True or case_bytecode.get("cache_cleanup_used_as_proof") is not False:
            raise VerificationFailure("Gate B worker bytecode evidence")
        case_probe, event_probe = case.get("sandbox_probe_preparation"), event.get("sandbox_probe_preparation")
        if type(case_probe) is not dict or case_probe != event_probe:
            raise VerificationFailure("Gate B sandbox probe evidence binding")
        required_probe = {
            "tracked_probe_relative_path": TRACKED_PROBE_RELATIVE, "tracked_probe_sha256": tracked_probe_digest,
            "tracked_probe_bytes": tracked_probe_bytes, "tracked_probe_mode_before": "0644", "tracked_probe_mode_after_worker": "0644",
            "tracked_probe_unchanged": True, "temporary_probe_relative_path": "prepared-probe/consumer_probe",
            "temporary_probe_sha256": tracked_probe_digest, "temporary_probe_bytes": tracked_probe_bytes,
            "temporary_probe_mode": "0500", "temporary_probe_executable": True,
            "temporary_probe_within_leaf_temp_root": True, "temporary_probe_copy_used": True,
            "source_copy_byte_identical": True, "active_closure_digest_exact": True, "active_closure_bytes_exact": True,
            "temporary_probe_inventory": ["prepared-probe/consumer_probe"], "temporary_probe_path_class": "leaf_os_temporary",
            "project_binary_mode_modified": False, "sandbox_policy_relaxed": False, "temporary_probe_cleanup_complete": True,
        }
        if any(case_probe.get(key) != value for key, value in required_probe.items()) or case_probe.get("sandbox_execution") not in {"executed_verified_temporary_probe", "not_reached_by_case_design"}:
            raise VerificationFailure("Gate B sandbox probe preparation")
        case_environment, event_environment = case.get("sandbox_environment"), event.get("sandbox_environment")
        if case_environment != event_environment:
            raise VerificationFailure("Gate B sandbox environment evidence binding")
        if case_probe.get("sandbox_execution") == "executed_verified_temporary_probe":
            if type(case_environment) is not dict:
                raise VerificationFailure("Gate B sandbox environment evidence absent")
            expected_full_object_handles = 0
            if (
                leaf.get("group_id") == "RCPT-T15-HANDLE-INVENTORY"
                and event.get("legacy_regression_vector") == "RCPT-T15-HANDLE-INVENTORY.RESIDUAL-FD-DETECTED"
            ):
                if (
                    case.get("expected_terminal") != "BLOCKED_SANDBOX_ISOLATION_UNPROVEN"
                    or case.get("observed_terminal") != "BLOCKED_SANDBOX_ISOLATION_UNPROVEN"
                    or type(case_environment.get("consumer_visible_full_object_handle_links")) is not dict
                    or len(case_environment["consumer_visible_full_object_handle_links"]) != 1
                ):
                    raise VerificationFailure("Gate B residual full-object handle denial evidence")
                expected_full_object_handles = 1
            required_environment = {
                "process_root_matches_empty_sandbox": True,
                "single_uid_namespace_mapping": True,
                "single_gid_namespace_mapping": True,
                "effective_capabilities_zero": True,
                "permitted_capabilities_zero": True,
                "bounding_capabilities_zero": True,
                "ambient_capabilities_zero": True,
                "no_new_privs": "1",
                "seccomp_mode": "2",
                "consumer_visible_full_object_handles": expected_full_object_handles,
                "consumer_visible_directory_handles": 0,
                "project_workspace_mounted": False,
                "project_source_tree_visible": False,
                "broker_fixture_store_mounted": False,
                "greek_fixture_or_raw_mounted": False,
                "network_source_fetch_allowed": False,
                "consumer_writable_project_paths": 0,
            }
            if any(case_environment.get(key) != value for key, value in required_environment.items()):
                raise VerificationFailure("Gate B sandbox security semantics")
            if type(case_environment.get("namespace_outer_uid")) is not int or case_environment["namespace_outer_uid"] < 0 or type(case_environment.get("namespace_outer_gid")) is not int or case_environment["namespace_outer_gid"] < 0:
                raise VerificationFailure("Gate B sandbox outer identity evidence")
        elif case_environment is not None:
            raise VerificationFailure("Gate B sandbox environment for not-reached case")
        probe_records.append(case_probe)
        if leaf.get("authorization_id") is None:
            if case.get("runtime_fixture_object_id") is not None or case.get("authorization_fixture_object_id") is not None:
                raise VerificationFailure("Gate B unauthorized leaf fixture evidence")
            continue
        variant = case.get("runtime_fixture_variant")
        authorization = authorization_by_leaf.get(leaf["leaf_id"])
        if authorization is None or case.get("authorization_fixture_object_id") != authorization.get("fixture_object_id") or event.get("authorization_fixture_object_id") != authorization.get("fixture_object_id") or case.get("capability_fixture_object_id") != event.get("capability_fixture_object_id"):
            raise VerificationFailure("Gate B authorization/capability fixture evidence")
        if leaf.get("group_id") == "RCPT-T16-GREEK-ID":
            vector = event.get("legacy_regression_vector")
            if vector == "RCPT-T16-GREEK-ID.AUTH-GREEK-ROLE":
                exact = authorization.get("fixture_object_id") == greek_object_id and case.get("capability_fixture_object_id") is None
            elif vector == "RCPT-T16-GREEK-ID.CAP-GREEK-OBJECT":
                exact = authorization.get("fixture_object_id") == case.get("runtime_fixture_object_id") and case.get("capability_fixture_object_id") == greek_object_id
            else:
                exact = False
            if not exact or case.get("observed_terminal") != "BLOCKED_FORBIDDEN_SOURCE_ROLE":
                raise VerificationFailure("Gate B Greek authorization denial")
            t16_records.append(case)
        elif not isinstance(variant, str):
            raise VerificationFailure("Gate B runtime fixture variant")
    if len(t16_records) != 2:
        raise VerificationFailure("Gate B canonical Greek T16 coverage")

    _assert_verifier_bytecode_boundary(root, "before_late_project_import")
    from build_r4_portable_manifest import build_synthetic_fixture_variant
    _assert_verifier_bytecode_boundary(root, "after_late_project_import")
    for leaf in leaves:
        if leaf.get("authorization_id") is None:
            continue
        case, event = cases_by_leaf[leaf["leaf_id"]], events_by_leaf[leaf["leaf_id"]]
        variant = case.get("runtime_fixture_variant")
        variant_raw = build_synthetic_fixture_variant(variant)
        variant_digest = sha256_bytes(variant_raw)
        variant_object_id = f"urn:ctde:fixture:{variant_digest}"
        if event.get("runtime_fixture_variant") != variant or case.get("runtime_fixture_object_id") != variant_object_id or event.get("runtime_fixture_object_id") != variant_object_id or case.get("runtime_fixture_full_sha256") != variant_digest or event.get("runtime_fixture_full_sha256") != variant_digest:
            raise VerificationFailure("Gate B runtime fixture identity evidence")
        if leaf.get("group_id") != "RCPT-T16-GREEK-ID" and authorization_by_leaf[leaf["leaf_id"]].get("fixture_object_id") != variant_object_id:
            raise VerificationFailure("Gate B Book authorization identity")

    baseline_cases = [item for item in cases if item.get("group_id") == "RCPT-T01-EXACT-RANGE"]
    if not baseline_cases or not all(item.get("runtime_fixture_variant") == "baseline" and item.get("runtime_fixture_object_id") == book_object_id and item.get("runtime_fixture_full_sha256") == full_digest and item.get("authorization_fixture_object_id") == book_object_id and item["sandbox_probe_preparation"].get("sandbox_execution") == "executed_verified_temporary_probe" for item in baseline_cases):
        raise VerificationFailure("Gate B baseline identity/sandbox execution")
    for group in ("RCPT-T29-BROKER-OBJECT-SWAP", "RCPT-T32-RANGE-ONLY-MISMATCH"):
        records = [item for item in cases if item.get("group_id") == group]
        if not records or not all(item.get("disposition") == "pass" and item.get("observed_terminal") == item.get("expected_terminal") for item in records):
            raise VerificationFailure(f"Gate B object-swap regression: {group}")

    previous = None
    allowed_bytes: dict[str, int] = {}
    allowed_events: dict[str, int] = {}
    denied = []
    for sequence, event in enumerate(writes, start=1):
        if event.get("sequence") != sequence or event.get("previous_event_sha256") != previous:
            raise VerificationFailure("Gate B logical write chain")
        previous = sha256_bytes(canonical_bytes(event))
        resolved = Path(event.get("resolved_path", ""))
        try:
            relative = resolved.relative_to(root).as_posix()
        except ValueError:
            relative = None
        if event.get("allowed") is True:
            byte_count = event.get("bytes_written")
            if relative not in GATE_B_ARTIFACT_PATHS or type(byte_count) is not int or byte_count < 0:
                raise VerificationFailure("Gate B allowed path scope")
            allowed_bytes[relative] = allowed_bytes.get(relative, 0) + byte_count
            allowed_events[relative] = allowed_events.get(relative, 0) + 1
        else:
            denied.append(event)
            if event.get("bytes_written") != 0:
                raise VerificationFailure("Gate B denied side effect")
    if set(allowed_bytes) != set(GATE_B_ARTIFACT_PATHS) or any(value != (root / relative).stat().st_size for relative, value in allowed_bytes.items()):
        raise VerificationFailure("Gate B logical path/byte accounting")
    forbidden = root / "forbidden-r4-write-probe"
    if len(denied) != 1 or denied[0].get("blocker") != "BLOCKED_R4_WRITE_SCOPE" or Path(denied[0].get("resolved_path", "")) != forbidden or forbidden.exists():
        raise VerificationFailure("Gate B denied probe")
    logical_relative = GATE_B_ARTIFACT_PATHS[12]
    logical_events = [item for item in writes if item.get("resolved_path") == str(root / logical_relative)]
    if len(logical_events) != 1 or logical_events[0].get("bytes_written") != len(writes_raw):
        raise VerificationFailure("Gate B logical self intent")
    final_relatives = [logical_relative, GATE_B_ARTIFACT_PATHS[17], GATE_B_ARTIFACT_PATHS[18], GATE_B_ARTIFACT_PATHS[19]]
    if [Path(item.get("resolved_path", "")).relative_to(root).as_posix() for item in writes[-4:]] != final_relatives:
        raise VerificationFailure("Gate B final logical intents")
    append_paths = [path for path in GATE_B_ARTIFACT_PATHS if path.endswith(("authorization_registry.jsonl", "registry_events.jsonl", "controller_terminals.jsonl", "attempts.jsonl", "runtime_events.jsonl", "logical_write_events.jsonl", "case_results.jsonl"))]
    if any((os.stat(root / relative).st_mode & 0o777) != 0o444 for relative in append_paths):
        raise VerificationFailure("Gate B append ledger mode")
    repeated_paths = set(append_paths) - {logical_relative}
    if not all(allowed_events.get(relative, 0) > 1 for relative in repeated_paths):
        raise VerificationFailure("Gate B repeated append coverage")

    expected_identities = {"book1_full_sha256": full_digest, "book1_object_id": book_object_id, "fixture_catalog_sha256": sha256_bytes(catalog_raw), "greek_full_sha256": greek_digest, "greek_object_id": greek_object_id}
    if evidence.get("synthetic_fixture_identities") != expected_identities or snapshot.get("fixture_catalog_sha256") != sha256_bytes(catalog_raw) or snapshot.get("test_manifest_sha256") != sha256_bytes(manifest_raw):
        raise VerificationFailure("Gate B fixture snapshot/evidence binding")
    if evidence.get("case_results_sha256") != sha256_bytes(cases_raw) or evidence.get("logical_write_events_sha256") != sha256_bytes(writes_raw) or evidence.get("evidence_complete") is not True:
        raise VerificationFailure("Gate B evidence identity")
    counts = aggregate.get("counts", {})
    expected_counts = {"requirement_groups": 37, "manifest_leaves": leaf_count, "discovered": leaf_count, "executed": leaf_count, "evidence_complete": leaf_count, "passed": leaf_count}
    if aggregate.get("status") != "PASS_PORTABLE_RUNTIME_SYNTHETIC_E2E" or any(counts.get(key) != value for key, value in expected_counts.items()):
        raise VerificationFailure("Gate B aggregate status")
    zero_counts = ("failed", "skipped", "unknown", "timeout", "duplicate_attempt_ids", "cross_case_authorization_reuse")
    if any(counts.get(key) != 0 for key in zero_counts):
        raise VerificationFailure("Gate B aggregate negative counts")
    zero_actions = ("model_calls", "candidate_runs", "business_outputs", "english_tei_content_reads", "greek_tei_content_reads")
    if any(aggregate.get("action_ledger", {}).get(key) != 0 for key in zero_actions):
        raise VerificationFailure("Gate B forbidden action ledger")
    if aggregate.get("logical_writes", {}).get("denied_events") != 1 or aggregate.get("identities", {}).get("logical_write_events_sha256") != sha256_bytes(writes_raw) or aggregate.get("identities", {}).get("evidence_manifest_sha256") != sha256_bytes(evidence_raw):
        raise VerificationFailure("Gate B aggregate evidence binding")
    if "Status: `PASS_PORTABLE_RUNTIME_SYNTHETIC_E2E`" not in (root / GATE_B_ARTIFACT_PATHS[19]).read_text(encoding="utf-8"):
        raise VerificationFailure("Gate B report status")

    post_late_import_cache_count = _assert_verifier_bytecode_boundary(root, "gate_b_result_final")
    if _actual_untracked_files(root) != expected_outputs:
        raise VerificationFailure("Gate B final exact output scope")

    return {
        "artifact_class": "ctde_r4_recovery_temp_gate_b_qualification", "schema_version": "1.0.0",
        "suite_id": SUITE_ID, "recovery_id": RECOVERY_ID, "standing_authorization_id": STANDING_AUTHORIZATION_ID,
        "status": "PASS_R4_RECOVERY_TEMP_GATE_B_QUALIFICATION",
        "attempt_count": 1, "qualification_attempt_ordinal": 1, "attempts_authorized_total": 1, "attempts_consumed_total": 1,
        "requirement_groups": len(groups), "manifest_leaf_count": leaf_count, "runner_discovered": len(cases), "runner_executed": len(cases),
        "evidence_complete": sum(item.get("evidence_complete") is True for item in cases), "passed": sum(item.get("disposition") == "pass" for item in cases),
        "failed": sum(item.get("disposition") == "fail" for item in cases), "skipped": counts["skipped"], "unknown": counts["unknown"],
        "timeout": counts["timeout"], "duplicate_attempt_ids": counts["duplicate_attempt_ids"], "cross_case_authorization_reuse": counts["cross_case_authorization_reuse"],
        "denied_write_events": len(denied), "repeated_jsonl_append": True, "logical_write_finalization": "PASS",
        "object_identity_consistency": "PASS", "canonical_greek_object_identity": greek_object_id,
        "historical_greek_placeholder_active_occurrences": active_placeholder_occurrences, "sandbox_probe_preparation": "PASS",
        "independent_verifier_status": "PASS", "unauthorized_project_tree_outputs": 0,
        "project_python_bytecode_outputs": 0, "runner_startup_bytecode_disabled": True,
        "workers_bytecode_disabled": True, "verifier_bytecode_disabled": True,
        "preexisting_project_cache_outputs": snapshot_bytecode["preexisting_project_cache_outputs"],
        "post_runner_project_cache_outputs": pre_verifier_cache_count,
        "post_workers_project_cache_outputs": final_bytecode["post_workers_project_cache_outputs"],
        "post_verifier_project_cache_outputs": post_late_import_cache_count,
        "cache_cleanup_used_as_proof": False,
        "defect_results": {**{f"R4R-D{index:02d}": "PASS" for index in range(1, 9)}, "R4R-D09-SANDBOX-USERNS-BOOTSTRAP": "PASS", "R4R-D10-FORMAL-ENVIRONMENT-BINDING": "PASS"},
        "action_ledger": {key: aggregate["action_ledger"][key] for key in zero_actions},
        "tracked_probe_sha256": tracked_probe_digest, "temporary_probe_sha256": tracked_probe_digest,
        "temporary_probe_mode": "0500", "temporary_probe_cleanup_complete": all(item.get("temporary_probe_cleanup_complete") is True for item in probe_records),
    }


def verify_bytecode_preflight(root: Path, *, expect_gate_b_output_scope: bool) -> dict[str, Any]:
    root = root.resolve(strict=True)
    preexisting = _assert_verifier_bytecode_boundary(root, "bytecode_preflight_start")
    expected = sorted(GATE_B_ARTIFACT_PATHS) if expect_gate_b_output_scope else []
    if _actual_untracked_files(root) != expected:
        raise VerificationFailure("bytecode preflight exact output scope")
    from build_r4_portable_manifest import build_synthetic_fixture_variant
    raw = build_synthetic_fixture_variant("baseline")
    if len(raw) != 40960:
        raise VerificationFailure("bytecode preflight late import execution")
    after_late_import = _assert_verifier_bytecode_boundary(root, "bytecode_preflight_after_late_import")
    if _actual_untracked_files(root) != expected:
        raise VerificationFailure("bytecode preflight final exact output scope")
    final = _assert_verifier_bytecode_boundary(root, "bytecode_preflight_final")
    return {
        "status": "PASS_R4_D08_BYTECODE_PREFLIGHT",
        "verifier_bytecode_disabled": True,
        "preexisting_project_cache_outputs": preexisting,
        "post_late_import_project_cache_outputs": after_late_import,
        "post_verifier_project_cache_outputs": final,
        "unauthorized_project_tree_outputs": 0,
        "expected_gate_b_output_scope_exercised": expect_gate_b_output_scope,
        "cache_cleanup_used_as_proof": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Independent R4 verifier")
    parser.add_argument("--mode", choices=("preexecution", "recovery-prefix", "gate-b-authorization", "gate-b-result", "bytecode-preflight"), required=True)
    parser.add_argument("--root", default=str(WORKSPACE_ROOT))
    parser.add_argument("--implementation-manifest")
    parser.add_argument("--materialization-plan")
    parser.add_argument("--closure-manifest")
    parser.add_argument("--component-freeze")
    parser.add_argument("--closure-registry")
    parser.add_argument("--builder-pass-a")
    parser.add_argument("--builder-pass-b")
    parser.add_argument("--authorization-payload")
    parser.add_argument("--repair-qualification", action="store_true")
    parser.add_argument("--expect-gate-b-output-scope", action="store_true")
    args = parser.parse_args()
    try:
        root = Path(args.root).resolve(strict=True)
        _assert_verifier_bytecode_boundary(root, "main_start")
        if args.mode == "preexecution":
            required = [args.implementation_manifest, args.materialization_plan, args.closure_manifest, args.component_freeze, args.closure_registry, args.builder_pass_a, args.builder_pass_b]
            if any(value is None for value in required):
                raise VerificationFailure("preexecution arguments incomplete")
            result = verify_preexecution_bundle(
                root=root,
                implementation_path=Path(args.implementation_manifest),
                materialization_path=Path(args.materialization_plan),
                closure_path=Path(args.closure_manifest),
                component_freeze_path=Path(args.component_freeze),
                registry_path=Path(args.closure_registry),
                builder_pass_a=Path(args.builder_pass_a),
                builder_pass_b=Path(args.builder_pass_b),
            )
        elif args.mode == "recovery-prefix":
            result = verify_recovery_prefix(root)
        elif args.mode == "gate-b-authorization":
            if args.authorization_payload is None:
                raise VerificationFailure("authorization payload required")
            payload, _ = load_canonical_json(Path(args.authorization_payload))
            result = {"status": "PASS_GATE_B_AUTHORIZATION", "verified": verify_gate_b_authorization(root, payload, repair_qualification=args.repair_qualification)}
        elif args.mode == "gate-b-result":
            result = verify_gate_b_outputs(root)
        else:
            result = verify_bytecode_preflight(root, expect_gate_b_output_scope=args.expect_gate_b_output_scope)
        _assert_verifier_bytecode_boundary(root, "main_end")
        sys.stdout.buffer.write(canonical_bytes(result))
        return 0
    except Exception as exc:
        print(f"BLOCKED_R4_VERIFICATION: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
