from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import sys
from pathlib import Path
from typing import Any


PROTOTYPE_ROOT = Path(__file__).resolve().parents[1]
WORKSPACE_ROOT = PROTOTYPE_ROOT.parent
RUNTIME_ROOT = PROTOTYPE_ROOT / "runtime"
if str(RUNTIME_ROOT) not in sys.path:
    sys.path.insert(0, str(RUNTIME_ROOT))

import build_r3_portable_closure as r3


CONTRACT_ROOT = PROTOTYPE_ROOT / "contracts"
PLAN_PATH = WORKSPACE_ROOT / "R4_GATE_B_RECOVERY_001_PLAN.md"
AUDIT_PATH = WORKSPACE_ROOT / "R4_GATE_B_RECOVERY_001_AUDIT.json"
CONTRACT_PATH = WORKSPACE_ROOT / "R4_GATE_B_RECOVERY_001_CONTRACT.md"
PREDECESSOR_MANIFEST_PATH = PROTOTYPE_ROOT / "r4_portable_suites" / "R4PS-20260815-001" / "repair" / "R4R-20260815-001" / "control" / "r4r_repaired_preexecution_closure_manifest.json"
PLAN_SHA256 = "c8740b9fdfc88f8761f8882d8e53bdae3e1a8095ab11dd6a2b3d8ad71cc0fa3e"
AUDIT_SHA256 = "4da3c32aeb188f1790bd2e872c1e6a77a9e3d48d36c5e1f2fca212bef9ecca09"
CONTRACT_SHA256 = "57b75f845d2718b85097fdd3864401356a5eeb02a02a20e3bb035ab175cfb3e2"
PREDECESSOR_MANIFEST_SHA256 = "70b48a10b04ff3a31cae8dd2e3224a7d89278031ed95d2b56957618ea3d0326a"
PREDECESSOR_PAYLOAD_SHA256 = "448fc78f6345d4f0ebf53fa60e20ab730f7f130dcf7794d50de7d03d79b143f1"
PREDECESSOR_NODE_COUNT = 356
GATE_A_WRITE_SCOPE_SHA256 = "8b30132ddd1c2c819adcb73269c3dd65601a94d5a80839bbec313059a82acdba"
SUITE_ID = "R4PS-20260815-002"
PHASE_ID = "Phase 2-G-R4FRESH-M2"
PHASE_KIND = "r4_versioned_recovery_implementation_and_preexecution_closure_refresh"

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
    "runtime_capability_prototype/runtime/ctde_runtime/sandbox.py",
]

CONTROL_INPUT_PATHS = [
    "R4_GATE_B_RECOVERY_001_CONTRACT.md",
    "R4_GATE_B_RECOVERY_001_AUDIT.json",
    "R4_GATE_B_RECOVERY_001_PLAN.md",
    "runtime_capability_prototype/r4_portable_suites/R4PS-20260815-002/recovery/R4X-20260815-002/control/r4x_implementation_manifest.json",
    "runtime_capability_prototype/r4_portable_suites/R4PS-20260815-002/recovery/R4X-20260815-002/control/r4x_materialization_plan.json",
]

SCHEMA_BINDINGS = {
    "runtime_capability_prototype/runtime/build_r4_preexecution_closure.py": [
        "runtime_capability_prototype/contracts/r4_preexecution_closure_manifest_schema_v1.yaml",
        "runtime_capability_prototype/contracts/r4_preexecution_closure_result_schema_v1.yaml",
    ],
    "runtime_capability_prototype/runtime/build_r4_portable_manifest.py": [
        "runtime_capability_prototype/contracts/r4_portable_e2e_policy_v1.yaml",
        "runtime_capability_prototype/contracts/r4_portable_test_requirements_v1.yaml",
        "runtime_capability_prototype/contracts/r4_portable_test_manifest_schema_v1.yaml",
    ],
    "runtime_capability_prototype/runtime/monitor_r4_logical_writes.py": [
        "runtime_capability_prototype/contracts/r4_portable_logical_write_event_schema_v1.yaml",
    ],
    "runtime_capability_prototype/runtime/verify_r4_portable.py": [
        "runtime_capability_prototype/contracts/r4_preexecution_closure_manifest_schema_v1.yaml",
        "runtime_capability_prototype/contracts/r4_preexecution_closure_result_schema_v1.yaml",
        "runtime_capability_prototype/contracts/r4_portable_case_result_schema_v1.yaml",
    ],
    "runtime_capability_prototype/runtime/run_r4_portable.py": [
        "runtime_capability_prototype/contracts/r4_portable_e2e_policy_v1.yaml",
        "runtime_capability_prototype/contracts/r4_portable_execution_snapshot_schema_v1.yaml",
        "runtime_capability_prototype/contracts/r4_portable_controller_terminal_schema_v1.yaml",
    ],
    "runtime_capability_prototype/runtime/build_r4_portable_result.py": [
        "runtime_capability_prototype/contracts/r4_portable_aggregate_schema_v1.yaml",
        "runtime_capability_prototype/contracts/r4_portable_case_result_schema_v1.yaml",
    ],
}

CALLABLES = [
    ("R4-C001", "runtime_capability_prototype/runtime/build_r4_preexecution_closure.py", "build_preexecution_closure", "build_r4_preexecution_closure"),
    ("R4-C002", "runtime_capability_prototype/runtime/build_r4_portable_manifest.py", "build_manifest_bytes", "build_r4_portable_manifest"),
    ("R4-C003", "runtime_capability_prototype/runtime/monitor_r4_logical_writes.py", "LogicalWriteMonitor.attempt", "monitor_r4_logical_writes"),
    ("R4-C004", "runtime_capability_prototype/runtime/verify_r4_portable.py", "verify_preexecution_bundle", "verify_r4_portable"),
    ("R4-C005", "runtime_capability_prototype/runtime/verify_r4_portable.py", "verify_gate_b_authorization", "verify_r4_portable"),
    ("R4-C006", "runtime_capability_prototype/runtime/run_r4_portable.py", "run_authorized_suite", "run_r4_portable"),
    ("R4-C007", "runtime_capability_prototype/runtime/build_r4_portable_result.py", "build_aggregate_bytes", "build_r4_portable_result"),
    ("R4-C008", "runtime_capability_prototype/runtime/build_r4_portable_result.py", "build_report_bytes", "build_r4_portable_result"),
    ("R4-C009", "runtime_capability_prototype/runtime/run_r4_portable.py", "_ensure_sandbox_namespace_at_process_start", "run_r4_portable"),
    ("R4-C010", "runtime_capability_prototype/runtime/ctde_runtime/sandbox.py", "SandboxSupervisor.run", "ctde_runtime.sandbox"),
]

MANIFEST_FIELDS = {
    "artifact_class", "schema_version", "canonicalization_id", "suite_id", "phase_id",
    "phase_kind", "assurance", "identities", "callable_roots", "nodes", "edges", "roles",
    "discovery", "platform", "action_ledger", "closure_payload_sha256",
}


class PreexecutionClosureFailure(RuntimeError):
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
        raise PreexecutionClosureFailure(f"noncanonical JSON: {path}")
    return value, raw


def _definition_count(path: Path, qualname: str) -> int:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    scope: list[ast.stmt] = tree.body
    for index, part in enumerate(qualname.split(".")):
        matches = [node for node in scope if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and node.name == part]
        if len(matches) != 1:
            return len(matches)
        if index < len(qualname.split(".")) - 1:
            if not isinstance(matches[0], ast.ClassDef):
                return 0
            scope = matches[0].body
    return 1


def _validate_frozen_inputs(implementation: dict[str, Any], materialization: dict[str, Any]) -> tuple[dict[str, Any], bytes]:
    expected = {
        PLAN_PATH: PLAN_SHA256,
        AUDIT_PATH: AUDIT_SHA256,
        CONTRACT_PATH: CONTRACT_SHA256,
        PREDECESSOR_MANIFEST_PATH: PREDECESSOR_MANIFEST_SHA256,
    }
    for path, digest in expected.items():
        if not path.is_file() or path.is_symlink() or sha256_file(path) != digest:
            raise PreexecutionClosureFailure(f"frozen input drift: {path}")
    predecessor, predecessor_raw = load_canonical_json(PREDECESSOR_MANIFEST_PATH)
    if predecessor.get("closure_payload_sha256") != PREDECESSOR_PAYLOAD_SHA256 or len(predecessor.get("nodes", [])) != PREDECESSOR_NODE_COUNT:
        raise PreexecutionClosureFailure("predecessor closure identity")
    if implementation.get("bundle_file_count") != len(IMPLEMENTATION_PATHS) or [item.get("path") for item in implementation.get("files", [])] != IMPLEMENTATION_PATHS:
        raise PreexecutionClosureFailure("implementation inventory")
    if implementation.get("materialization_status") != "complete_create_once_bundle":
        raise PreexecutionClosureFailure("implementation status")
    exact_materialization = {
        "suite_id": SUITE_ID,
        "phase_id": PHASE_ID,
        "phase_kind": PHASE_KIND,
        "plan_sha256": PLAN_SHA256,
        "audit_sha256": AUDIT_SHA256,
        "contract_sha256": CONTRACT_SHA256,
        "gate_a_write_scope_sha256": GATE_A_WRITE_SCOPE_SHA256,
        "predecessor_closure_manifest_sha256": PREDECESSOR_MANIFEST_SHA256,
        "predecessor_closure_payload_sha256": PREDECESSOR_PAYLOAD_SHA256,
        "execution_authorized": True,
        "gate_b_execution_authorized": False,
    }
    for key, expected_value in exact_materialization.items():
        if materialization.get(key) != expected_value:
            raise PreexecutionClosureFailure(f"materialization mismatch: {key}")
    for record in implementation["files"]:
        path = WORKSPACE_ROOT / record["path"]
        if not path.is_file() or path.is_symlink() or path.stat().st_size != record["bytes"] or sha256_file(path) != record["sha256"]:
            raise PreexecutionClosureFailure(f"implementation drift: {record['path']}")
    return predecessor, predecessor_raw


def _project_node(identity: str, classification: str, member_type: str | None = None) -> dict[str, Any]:
    path = WORKSPACE_ROOT / identity
    if identity.startswith("source/") or identity == "book_structure_map.yaml":
        raise PreexecutionClosureFailure("source identity forbidden in R4 closure")
    return r3._file_node(path, identity, classification, member_type)


def _local_import_target(imported: str, path_to_node: dict[str, str]) -> str | None:
    top = imported.lstrip(".").split(".", 1)[0]
    names = {
        Path(path).stem: node_id
        for path, node_id in path_to_node.items()
        if path.startswith("runtime_capability_prototype/runtime/") and path.endswith(".py")
    }
    if top in names:
        return names[top]
    if imported.startswith("ctde_runtime"):
        parts = imported.split(".")
        relative = "runtime_capability_prototype/runtime/ctde_runtime/__init__.py" if len(parts) == 1 else f"runtime_capability_prototype/runtime/ctde_runtime/{parts[1]}.py"
        return path_to_node.get(relative)
    return None


def build_preexecution_closure(
    implementation: dict[str, Any],
    materialization: dict[str, Any],
    implementation_raw: bytes | None = None,
    materialization_raw: bytes | None = None,
) -> dict[str, Any]:
    predecessor, predecessor_raw = _validate_frozen_inputs(implementation, materialization)
    nodes: dict[str, dict[str, Any]] = {}
    path_to_node: dict[str, str] = {}
    python_records: list[tuple[Path, str, str]] = []

    successor_mutable = set(IMPLEMENTATION_PATHS)
    for old_node in predecessor["nodes"]:
        if old_node["classification"] == "platform_boundary":
            continue
        identity = old_node["identity"]
        if identity in successor_mutable:
            continue
        node = _project_node(identity, old_node["classification"], old_node["member_type"])
        if node["node_id"] != old_node["node_id"] or node["sha256"] != old_node["sha256"] or node["bytes"] != old_node["bytes"]:
            raise PreexecutionClosureFailure(f"predecessor member drift: {identity}")
        nodes[node["node_id"]] = node
        path_to_node[identity] = node["node_id"]
        if identity.endswith(".py"):
            python_records.append((WORKSPACE_ROOT / identity, identity, node["classification"]))

    implementation_by_path = {item["path"]: item for item in implementation["files"]}
    for identity in IMPLEMENTATION_PATHS:
        record = implementation_by_path[identity]
        node = _project_node(identity, record["classification"])
        nodes[node["node_id"]] = node
        path_to_node[identity] = node["node_id"]
        if identity.endswith(".py"):
            python_records.append((WORKSPACE_ROOT / identity, identity, node["classification"]))

    control_classifications = {
        CONTROL_INPUT_PATHS[0]: "build_only_dependency",
        CONTROL_INPUT_PATHS[1]: "build_only_dependency",
        CONTROL_INPUT_PATHS[2]: "build_only_dependency",
        CONTROL_INPUT_PATHS[3]: "build_only_dependency",
        CONTROL_INPUT_PATHS[4]: "build_only_dependency",
    }
    for identity, classification in control_classifications.items():
        if identity in path_to_node:
            continue
        node = _project_node(identity, classification, "policy" if identity.endswith(".md") else "configuration")
        nodes[node["node_id"]] = node
        path_to_node[identity] = node["node_id"]

    module_names = {record["module"] for record in predecessor["platform"]["module_origins"]}
    dynamic_sites: list[dict[str, Any]] = []
    process_boundaries: list[dict[str, Any]] = []
    import_edges: list[tuple[str, str]] = []
    for path, identity, classification in python_records:
        imports, sites, boundaries = r3._scan_python(path, identity, classification)
        dynamic_sites.extend(sites)
        process_boundaries.extend(boundaries)
        if identity in IMPLEMENTATION_PATHS:
            for imported in imports:
                if imported and not imported.startswith(".") and _local_import_target(imported, path_to_node) is None:
                    module_names.add(imported)
                import_edges.append((identity, imported))
    unresolved = [site for site in dynamic_sites if site["production_reachable"] and not site["resolved"]]
    if unresolved:
        raise PreexecutionClosureFailure("unresolved production dynamic import")

    fixed_environment = materialization["fixed_environment"]
    platform_nodes, platform_record, module_to_node = r3._platform_capture(module_names, fixed_environment)
    for node in platform_nodes:
        existing = nodes.get(node["node_id"])
        if existing is not None and existing != node:
            raise PreexecutionClosureFailure(f"platform node collision: {node['identity']}")
        nodes[node["node_id"]] = node
    for old_node in predecessor["nodes"]:
        if old_node["classification"] != "platform_boundary" or old_node["node_id"] in nodes:
            continue
        descriptor = old_node.get("virtual_descriptor")
        if type(descriptor) is not dict:
            raise PreexecutionClosureFailure(f"platform member not recomputed: {old_node['identity']}")
        node = r3._virtual_node(old_node["identity"], old_node["member_type"], descriptor)
        if node["node_id"] != old_node["node_id"] or node["sha256"] != old_node["sha256"]:
            raise PreexecutionClosureFailure(f"virtual platform drift: {old_node['identity']}")
        nodes[node["node_id"]] = node

    edges: dict[tuple[str, str, str, str], dict[str, Any]] = {}
    for edge in predecessor["edges"]:
        if edge["from_id"] not in nodes or edge["to_id"] not in nodes:
            raise PreexecutionClosureFailure(f"predecessor edge unresolved: {edge['locator']}")
        key = (edge["from_id"], edge["to_id"], edge["relation"], edge["locator"])
        edges[key] = dict(edge)
    for source, imported in import_edges:
        target_id = _local_import_target(imported, path_to_node)
        if target_id is None:
            target_id = module_to_node.get(imported) or module_to_node.get(imported.split(".", 1)[0])
        if target_id is None:
            raise PreexecutionClosureFailure(f"new import unresolved: {source}:{imported}")
        edge = {"from_id": path_to_node[source], "to_id": target_id, "relation": "imports", "locator": f"r4_ast:{source}:{imported}"}
        edges[(edge["from_id"], edge["to_id"], edge["relation"], edge["locator"])] = edge
    policy_node = path_to_node["runtime_capability_prototype/contracts/r4_portable_e2e_policy_v1.yaml"]
    for identity in IMPLEMENTATION_PATHS:
        if identity.endswith("r4_portable_e2e_policy_v1.yaml"):
            continue
        edge = {"from_id": path_to_node[identity], "to_id": policy_node, "relation": "classified_by", "locator": f"r4_policy:{identity}"}
        edges[(edge["from_id"], edge["to_id"], edge["relation"], edge["locator"])] = edge
    for source, targets in SCHEMA_BINDINGS.items():
        for target in targets:
            relation = "loads_policy" if target.endswith("policy_v1.yaml") or "requirements" in target else "loads_schema"
            edge = {"from_id": path_to_node[source], "to_id": path_to_node[target], "relation": relation, "locator": f"r4_contract_binding:{source}:{target}"}
            edges[(edge["from_id"], edge["to_id"], edge["relation"], edge["locator"])] = edge
    builder_id = path_to_node["runtime_capability_prototype/runtime/build_r4_preexecution_closure.py"]
    for control in CONTROL_INPUT_PATHS:
        edge = {"from_id": builder_id, "to_id": path_to_node[control], "relation": "loads_config", "locator": f"r4_gate_a_input:{control}"}
        edges[(edge["from_id"], edge["to_id"], edge["relation"], edge["locator"])] = edge

    successor_callable_ids = {record[0] for record in CALLABLES}
    callable_roots = [record for record in predecessor["callable_roots"] if record.get("callable_id") not in successor_callable_ids]
    for callable_id, identity, qualname, module in CALLABLES:
        path = WORKSPACE_ROOT / identity
        if _definition_count(path, qualname) != 1:
            raise PreexecutionClosureFailure(f"R4 callable root mismatch: {callable_id}")
        callable_roots.append({
            "callable_id": callable_id,
            "module": module,
            "qualname": qualname,
            "relative_path": identity,
            "containing_file_sha256": sha256_file(path),
            "definition_count": 1,
        })

    roles = []
    audit, _ = load_canonical_json(AUDIT_PATH)
    for role in audit["r4_role_requirements"]:
        roles.append({**role, "node_id": path_to_node[role["planned_path"]], "status": "MATERIALIZED_AND_CLOSURE_BOUND"})
    manifest = {
        "artifact_class": "ctde_r4_preexecution_transitive_closure_manifest",
        "schema_version": "1.0.0",
        "canonicalization_id": "CTDE-CANONICAL-JSON-SORTED-COMPACT-LF-1",
        "suite_id": SUITE_ID,
        "phase_id": PHASE_ID,
        "phase_kind": PHASE_KIND,
        "assurance": {
            "assurance_profile_id": "CTDE-PORTABLE-DEV-1",
            "environment_class": "Development",
            "highest_claimed_evidence_level": "A1",
            "certified": False,
            "hardened": False,
            "candidate_ready": False,
            "r1_requalified": False,
        },
        "identities": {
            "contract_path": CONTRACT_PATH.name,
            "contract_sha256": CONTRACT_SHA256,
            "audit_path": AUDIT_PATH.name,
            "audit_sha256": AUDIT_SHA256,
            "plan_path": PLAN_PATH.name,
            "plan_sha256": PLAN_SHA256,
            "gate_a_write_scope_sha256": GATE_A_WRITE_SCOPE_SHA256,
            "implementation_manifest_sha256": sha256_bytes(implementation_raw or canonical_bytes(implementation)),
            "materialization_plan_sha256": sha256_bytes(materialization_raw or canonical_bytes(materialization)),
            "predecessor_closure_manifest_sha256": PREDECESSOR_MANIFEST_SHA256,
            "predecessor_closure_payload_sha256": PREDECESSOR_PAYLOAD_SHA256,
            "predecessor_node_count": len(predecessor["nodes"]),
            "git_head": materialization["git_head"],
            "remote_main": materialization["remote_main"],
        },
        "callable_roots": sorted(callable_roots, key=lambda item: item["callable_id"]),
        "nodes": sorted(nodes.values(), key=lambda item: item["node_id"]),
        "edges": sorted(edges.values(), key=lambda item: (item["from_id"], item["to_id"], item["relation"], item["locator"])),
        "roles": roles,
        "discovery": {
            "predecessor_node_count": len(predecessor["nodes"]),
            "predecessor_edge_count": len(predecessor["edges"]),
            "refreshed_node_count": len(nodes),
            "refreshed_edge_count": len(edges),
            "r4_implementation_member_count": len(IMPLEMENTATION_PATHS),
            "new_control_input_count": len(CONTROL_INPUT_PATHS),
            "dynamic_sites": sorted(dynamic_sites, key=lambda item: item["site_id"]),
            "process_boundaries": sorted(process_boundaries, key=lambda item: item["boundary_id"]),
            "unknown_dynamic_dependency_count": 0,
            "unknown_project_owned_loaded_bytes": 0,
            "unresolved_symlinks": 0,
            "predecessor_node_subset": all(node["node_id"] in nodes for node in predecessor["nodes"]),
        },
        "platform": platform_record,
        "action_ledger": {
            "r4_gate_b_executions": 0,
            "model_calls": 0,
            "candidate_runs": 0,
            "english_tei_content_reads": 0,
            "greek_tei_content_reads": 0,
            "business_outputs": 0,
        },
        "closure_payload_sha256": "",
    }
    manifest["closure_payload_sha256"] = sha256_bytes(canonical_bytes({key: value for key, value in manifest.items() if key != "closure_payload_sha256"}))
    validate_manifest(manifest, canonical_bytes(manifest), predecessor)
    return manifest


def validate_manifest(manifest: dict[str, Any], raw: bytes, predecessor: dict[str, Any] | None = None) -> None:
    if set(manifest) != MANIFEST_FIELDS or raw != canonical_bytes(manifest):
        raise PreexecutionClosureFailure("closure canonical closed schema")
    payload = {key: value for key, value in manifest.items() if key != "closure_payload_sha256"}
    if manifest["closure_payload_sha256"] != sha256_bytes(canonical_bytes(payload)):
        raise PreexecutionClosureFailure("closure payload digest")
    nodes = manifest["nodes"]
    edges = manifest["edges"]
    node_ids = [node["node_id"] for node in nodes]
    if node_ids != sorted(node_ids) or len(node_ids) != len(set(node_ids)):
        raise PreexecutionClosureFailure("closure node identity/order")
    edge_keys = [(edge["from_id"], edge["to_id"], edge["relation"], edge["locator"]) for edge in edges]
    if edge_keys != sorted(edge_keys) or len(edge_keys) != len(set(edge_keys)):
        raise PreexecutionClosureFailure("closure edge identity/order")
    known = set(node_ids)
    if any(edge["from_id"] not in known or edge["to_id"] not in known or edge["relation"] not in r3.EDGE_RELATIONS for edge in edges):
        raise PreexecutionClosureFailure("closure unresolved edge")
    if manifest["discovery"]["unknown_dynamic_dependency_count"] != 0 or manifest["discovery"]["unknown_project_owned_loaded_bytes"] != 0 or manifest["discovery"]["unresolved_symlinks"] != 0:
        raise PreexecutionClosureFailure("closure unresolved inventory")
    if predecessor is not None:
        lookup = {node["node_id"]: node for node in nodes}
        mutable = set(IMPLEMENTATION_PATHS)
        for old_node in predecessor["nodes"]:
            if old_node["identity"] not in mutable and lookup.get(old_node["node_id"]) != old_node:
                raise PreexecutionClosureFailure(f"predecessor node not preserved: {old_node['identity']}")
    identities = {node["identity"] for node in nodes}
    if not set(IMPLEMENTATION_PATHS).issubset(identities):
        raise PreexecutionClosureFailure("R4 implementation closure incomplete")


def build_component_freeze(manifest: dict[str, Any], manifest_raw: bytes, implementation_raw: bytes) -> dict[str, Any]:
    validate_manifest(manifest, manifest_raw)
    counts: dict[str, int] = {}
    for node in manifest["nodes"]:
        counts[node["classification"]] = counts.get(node["classification"], 0) + 1
    return {
        "artifact_class": "ctde_r4_preexecution_component_freeze",
        "schema_version": "1.0.0",
        "suite_id": SUITE_ID,
        "phase_id": PHASE_ID,
        "closure_manifest_sha256": sha256_bytes(manifest_raw),
        "closure_payload_sha256": manifest["closure_payload_sha256"],
        "implementation_manifest_sha256": sha256_bytes(implementation_raw),
        "members": manifest["nodes"],
        "platform": manifest["platform"],
        "counts": dict(sorted(counts.items())),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Build R4 pre-execution closure bytes")
    parser.add_argument("--implementation-manifest", required=True)
    parser.add_argument("--materialization-plan", required=True)
    args = parser.parse_args()
    try:
        implementation, implementation_raw = load_canonical_json(Path(args.implementation_manifest))
        materialization, materialization_raw = load_canonical_json(Path(args.materialization_plan))
        manifest = build_preexecution_closure(implementation, materialization, implementation_raw, materialization_raw)
        sys.stdout.buffer.write(canonical_bytes(manifest))
        return 0
    except Exception as exc:
        print(f"BLOCKED_R4_PREEXECUTION_TRANSITIVE_CLOSURE_REFRESH: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
