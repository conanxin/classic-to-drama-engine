from __future__ import annotations

import argparse
import ast
import hashlib
import importlib.metadata
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


PROTOTYPE_ROOT = Path(__file__).resolve().parents[1]
WORKSPACE_ROOT = PROTOTYPE_ROOT.parent
SUITE_ID = "R4PS-20260815-001"
GATE_A_PHASE_ID = "Phase 2-G-R4FRESH-M1"
GATE_B_PHASE_ID = "Phase 2-G-R4FRESH-E1"
PLAN_SHA256 = "c1ddff51020880c22787f75722166656647ac18a0a8dd6b21c8af1d3ade24fb8"
AUDIT_SHA256 = "210f5c1e4e205b1e17e731cb87180d72680d576f97a96e746d8f9fc82fde5b6a"
CONTRACT_SHA256 = "b6b10f5cf06ef596270ae00ebd27343e96556593d05d17f6a0af5930e3615422"
GATE_A_WRITE_SCOPE_SHA256 = "6e25a9fd26f8fbe484692b9e3c3b095fc10cd6f177cf3a38530c360b692fe548"
GATE_B_WRITE_SCOPE_SHA256 = "d4bf4ac03afe22461831261e06c82797cf86c50eb3b4882d6275895436baf71c"
PREDECESSOR_MANIFEST_SHA256 = "56491b3fd08332327e98284a5dce0b482d3d6ae4bd23517204c62fa63fa3a4a5"
PREDECESSOR_PAYLOAD_SHA256 = "703dcba04e0ce669c5472ef4d9b3fc6ed7080eb112e9d5770b3d40c3296e2eca"
PREDECESSOR_COMMIT = "d22ba2c006a8011a2dfe08ee8c81e7d535593423"

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

GATE_B_ARTIFACT_PATHS = [
    "runtime_capability_prototype/r4_portable_suites/R4PS-20260815-001/control/r4_test_manifest.json",
    "runtime_capability_prototype/r4_portable_suites/R4PS-20260815-001/control/r4_execution_snapshot.json",
    "runtime_capability_prototype/r4_portable_suites/R4PS-20260815-001/control/r4_snapshot_registry_record.json",
    "runtime_capability_prototype/r4_portable_suites/R4PS-20260815-001/fixtures/synthetic_full_fixture.bin",
    "runtime_capability_prototype/r4_portable_suites/R4PS-20260815-001/fixtures/synthetic_greek_deny.bin",
    "runtime_capability_prototype/r4_portable_suites/R4PS-20260815-001/fixtures/r4_synthetic_fixture_catalog.json",
    "runtime_capability_prototype/r4_portable_suites/R4PS-20260815-001/registry/authorization_registry.jsonl",
    "runtime_capability_prototype/r4_portable_suites/R4PS-20260815-001/registry/authorization_state.json",
    "runtime_capability_prototype/r4_portable_suites/R4PS-20260815-001/registry/registry_events.jsonl",
    "runtime_capability_prototype/r4_portable_suites/R4PS-20260815-001/evidence/controller_terminals.jsonl",
    "runtime_capability_prototype/r4_portable_suites/R4PS-20260815-001/evidence/attempts.jsonl",
    "runtime_capability_prototype/r4_portable_suites/R4PS-20260815-001/evidence/runtime_events.jsonl",
    "runtime_capability_prototype/r4_portable_suites/R4PS-20260815-001/evidence/logical_write_events.jsonl",
    "runtime_capability_prototype/r4_portable_suites/R4PS-20260815-001/evidence/case_results.jsonl",
    "runtime_capability_prototype/r4_portable_suites/R4PS-20260815-001/evidence/start_verification.json",
    "runtime_capability_prototype/r4_portable_suites/R4PS-20260815-001/evidence/dynamic_observation.json",
    "runtime_capability_prototype/r4_portable_suites/R4PS-20260815-001/evidence/end_verification.json",
    "runtime_capability_prototype/r4_portable_suites/R4PS-20260815-001/evidence/evidence_manifest.json",
    "runtime_capability_prototype/r4_portable_suites/R4PS-20260815-001/aggregate/r4_portable_results.json",
    "PORTABLE_RUNTIME_SYNTHETIC_E2E_RESULT.md",
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


def verify_gate_b_authorization(root: Path, payload: dict[str, Any]) -> dict[str, str]:
    expected_static = {
        "current_status": "READY_FOR_PORTABLE_R4_SYNTHETIC_E2E_EXECUTION_AUTHORIZATION_REVIEW",
        "plan_path": "FRESH_R4_SYNTHETIC_E2E_PLAN.md",
        "plan_sha256": PLAN_SHA256,
        "current_tree_audit_sha256": AUDIT_SHA256,
        "phase_id": GATE_B_PHASE_ID,
        "phase_kind": "portable_r4_fresh_synthetic_e2e_deterministic_execution",
        "suite_id": SUITE_ID,
        "gate_b_write_scope_sha256": GATE_B_WRITE_SCOPE_SHA256,
        "approval_scope": "one Portable R4 fresh synthetic E2E execution attempt only; no Candidate, source read, model call, or business output",
    }
    for key, value in expected_static.items():
        if payload.get(key) != value:
            raise VerificationFailure(f"Gate B authorization mismatch: {key}")
    prefix_paths = {
        "implementation_manifest_sha256": GATE_A_ARTIFACT_PATHS[0],
        "refreshed_closure_manifest_sha256": GATE_A_ARTIFACT_PATHS[2],
        "preexecution_component_freeze_sha256": GATE_A_ARTIFACT_PATHS[3],
        "preexecution_closure_registry_record_sha256": GATE_A_ARTIFACT_PATHS[4],
    }
    verified: dict[str, str] = {}
    for key, relative in prefix_paths.items():
        actual = sha256_file(root / relative)
        if payload.get(key) != actual:
            raise VerificationFailure(f"Gate B persisted digest mismatch: {key}")
        verified[key] = actual
    closure, _ = load_canonical_json(root / GATE_A_ARTIFACT_PATHS[2])
    if payload.get("refreshed_closure_payload_sha256") != closure.get("closure_payload_sha256"):
        raise VerificationFailure("Gate B closure payload mismatch")
    verified["refreshed_closure_payload_sha256"] = closure["closure_payload_sha256"]
    if any((root / path).exists() for path in GATE_B_ARTIFACT_PATHS):
        raise VerificationFailure("Gate B partial materialization")
    return verified


def main() -> int:
    parser = argparse.ArgumentParser(description="Independent R4 verifier")
    parser.add_argument("--mode", choices=("preexecution", "gate-b-authorization"), required=True)
    parser.add_argument("--root", default=str(WORKSPACE_ROOT))
    parser.add_argument("--implementation-manifest")
    parser.add_argument("--materialization-plan")
    parser.add_argument("--closure-manifest")
    parser.add_argument("--component-freeze")
    parser.add_argument("--closure-registry")
    parser.add_argument("--builder-pass-a")
    parser.add_argument("--builder-pass-b")
    parser.add_argument("--authorization-payload")
    args = parser.parse_args()
    try:
        root = Path(args.root)
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
        else:
            if args.authorization_payload is None:
                raise VerificationFailure("authorization payload required")
            payload, _ = load_canonical_json(Path(args.authorization_payload))
            result = {"status": "PASS_GATE_B_AUTHORIZATION", "verified": verify_gate_b_authorization(root, payload)}
        sys.stdout.buffer.write(canonical_bytes(result))
        return 0
    except Exception as exc:
        print(f"BLOCKED_R4_VERIFICATION: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
