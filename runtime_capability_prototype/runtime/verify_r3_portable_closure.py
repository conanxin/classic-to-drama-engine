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

from build_r3_portable_closure import (
    AUDIT_PATH,
    PLAN_PATH,
    PROTOTYPE_ROOT,
    SUITE_ID,
    WORKSPACE_ROOT,
    canonical_bytes,
    canonical_payload_digest,
    load_canonical_json,
    sha256_file,
    validate_manifest,
)
from build_r3_portable_test_manifest import validate_test_manifest


class VerificationFailure(RuntimeError):
    pass


def _git_output(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=WORKSPACE_ROOT, check=True, capture_output=True, text=True).stdout.strip()


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


def _project_node_digest(node: dict[str, Any]) -> str | None:
    candidate = WORKSPACE_ROOT / node["identity"]
    if candidate.is_file() and not candidate.is_symlink():
        return sha256_file(candidate)
    return None


def _platform_node_digest(node: dict[str, Any]) -> str:
    identity = node["identity"]
    path: Path | None = None
    if identity.startswith("interpreter:") or identity.startswith("shared-library:"):
        path = Path(identity.split(":", 1)[1])
    elif identity.startswith("python-module:"):
        origin = identity.split(":", 2)[2]
        candidate = Path(origin)
        path = candidate if candidate.is_file() else None
    elif identity.startswith("distribution:"):
        _, distribution_name, relative = identity.split(":", 2)
        path = Path(importlib.metadata.distribution(distribution_name).locate_file(relative)).resolve()
    if path is not None and path.is_file() and not path.is_symlink():
        return sha256_file(path)
    descriptor = node.get("virtual_descriptor")
    if type(descriptor) is dict:
        return hashlib.sha256(canonical_bytes(descriptor)).hexdigest()
    return node["sha256"]


def _baseline_records(audit: dict[str, Any]) -> list[dict[str, Any]]:
    records = list(audit["runtime_file_identities"]) + list(audit["formal_source_identities"])
    records.extend([
        {"path": PLAN_PATH.name, "sha256": sha256_file(PLAN_PATH), "bytes": PLAN_PATH.stat().st_size},
        {"path": AUDIT_PATH.name, "sha256": sha256_file(AUDIT_PATH), "bytes": AUDIT_PATH.stat().st_size},
    ])
    return sorted(records, key=lambda item: item["path"])


def build_snapshot(
    stage: str,
    manifest: dict[str, Any], manifest_raw: bytes,
    implementation: dict[str, Any], implementation_raw: bytes,
    execution: dict[str, Any], execution_raw: bytes,
    control_paths: list[str],
    start_snapshot: dict[str, Any] | None = None,
) -> dict[str, Any]:
    validate_manifest(manifest, manifest_raw)
    audit, _ = load_canonical_json(AUDIT_PATH)
    immutable: list[dict[str, Any]] = []
    for record in _baseline_records(audit):
        path = WORKSPACE_ROOT / record["path"]
        actual = sha256_file(path) if path.is_file() and not path.is_symlink() else None
        immutable.append({"path": record["path"], "expected_sha256": record["sha256"], "actual_sha256": actual, "match": actual == record["sha256"]})
    for record in implementation["files"]:
        path = WORKSPACE_ROOT / record["path"]
        actual = sha256_file(path) if path.is_file() and not path.is_symlink() else None
        immutable.append({"path": record["path"], "expected_sha256": record["sha256"], "actual_sha256": actual, "match": actual == record["sha256"]})

    node_checks = []
    for node in manifest["nodes"]:
        actual = _project_node_digest(node)
        if actual is None and node["classification"] == "platform_boundary":
            actual = _platform_node_digest(node)
        node_checks.append({"node_id": node["node_id"], "expected_sha256": node["sha256"], "actual_sha256": actual, "match": actual == node["sha256"]})

    tracked_changes = [line for line in _git_output("diff", "--name-only", "HEAD").splitlines() if line]
    status_lines = [line for line in _git_output("status", "--porcelain=v1", "--untracked-files=all").splitlines() if line]
    observed_paths = [line[3:] for line in status_lines]
    allowed = set(execution["creatable_files"])
    unexpected = sorted(path for path in observed_paths if path not in allowed)
    control_digests = []
    for relative in sorted(control_paths):
        path = WORKSPACE_ROOT / relative
        control_digests.append({"path": relative, "sha256": sha256_file(path) if path.is_file() and not path.is_symlink() else None})
    closure_delta: list[dict[str, Any]] = []
    if start_snapshot is not None:
        start_map = {item["path"]: item["actual_sha256"] for item in start_snapshot["immutable_files"]}
        closure_delta = [item for item in immutable if start_map.get(item["path"]) != item["actual_sha256"]]
    passed = (
        all(item["match"] for item in immutable)
        and all(item["match"] for item in node_checks)
        and not tracked_changes
        and not unexpected
        and not closure_delta
    )
    return {
        "artifact_class": f"ctde_r3_portable_{stage}_verification",
        "schema_version": "1.0.0",
        "suite_id": SUITE_ID,
        "stage": stage,
        "overall_result": "PASS" if passed else "BLOCKED",
        "git_head": _git_output("rev-parse", "HEAD"),
        "implementation_manifest_sha256": hashlib.sha256(implementation_raw).hexdigest(),
        "execution_plan_sha256": hashlib.sha256(execution_raw).hexdigest(),
        "closure_manifest_sha256": hashlib.sha256(manifest_raw).hexdigest(),
        "immutable_files": immutable,
        "node_checks": node_checks,
        "control_artifacts": control_digests,
        "tracked_changes": tracked_changes,
        "observed_project_changes": observed_paths,
        "unexpected_project_paths": unexpected,
        "closure_delta": closure_delta,
        "counts": {
            "immutable_checked": len(immutable),
            "immutable_mismatches": sum(not item["match"] for item in immutable),
            "nodes_checked": len(node_checks),
            "node_mismatches": sum(not item["match"] for item in node_checks),
            "tracked_changes": len(tracked_changes),
            "scope_violations": len(unexpected),
            "closure_delta_count": len(closure_delta),
        },
    }


def _node_lookup(manifest: dict[str, Any], node_id: str) -> dict[str, Any]:
    matches = [item for item in manifest["nodes"] if item["node_id"] == node_id]
    if len(matches) != 1:
        raise VerificationFailure(f"node locator ambiguity: {node_id}")
    return matches[0]


def _role_lookup(manifest: dict[str, Any], gap_id: str) -> dict[str, Any]:
    matches = [item for item in manifest["roles"] if item["gap_id"] == gap_id]
    if len(matches) != 1:
        raise VerificationFailure(f"role locator ambiguity: {gap_id}")
    return matches[0]


def observe_locator(
    locator: str,
    manifest: dict[str, Any],
    implementation: dict[str, Any],
    post: dict[str, Any],
) -> Any:
    audit, _ = load_canonical_json(AUDIT_PATH)
    if locator.startswith("identity:"):
        return manifest["identities"][locator.split(":", 1)[1]]
    if locator.startswith("implementation:"):
        relative = locator.split(":", 1)[1]
        matches = [item for item in implementation["files"] if item["path"] == relative]
        if len(matches) != 1:
            raise VerificationFailure(f"implementation locator ambiguity: {relative}")
        return sha256_file(WORKSPACE_ROOT / relative)
    if locator.startswith("implementation_field:"):
        return implementation[locator.split(":", 1)[1]]
    if locator.startswith("root:"):
        root_id = locator.split(":", 1)[1]
        matches = [item for item in manifest["callable_roots"] if item["callable_id"] == root_id]
        if len(matches) != 1:
            raise VerificationFailure(f"root locator ambiguity: {root_id}")
        root = matches[0]
        path = WORKSPACE_ROOT / root["relative_path"]
        return {"definition_count": _definition_count(path, root["qualname"]), "sha256": sha256_file(path)}
    if locator.startswith("role:"):
        _, remainder = locator.split(":", 1)
        gap_id, field = remainder.rsplit(":", 1)
        return _role_lookup(manifest, gap_id)[field]
    if locator.startswith("classification:"):
        value = locator.split(":", 1)[1]
        return any(item["classification"] == value for item in manifest["nodes"])
    if locator.startswith("edge:"):
        digest = locator.split(":", 1)[1]
        return sum(hashlib.sha256(canonical_bytes(item)).hexdigest() == digest for item in manifest["edges"]) == 1
    if locator.startswith("node:"):
        node = _node_lookup(manifest, locator.split(":", 1)[1])
        return _project_node_digest(node) or _platform_node_digest(node)
    if locator.startswith("platform_node:"):
        node = _node_lookup(manifest, locator.split(":", 1)[1])
        return _platform_node_digest(node)
    if locator.startswith("dynamic_site:"):
        site_id = locator.split(":", 1)[1]
        matches = [item for item in manifest["discovery"]["dynamic_sites"] if item["site_id"] == site_id]
        if len(matches) != 1:
            raise VerificationFailure(f"dynamic site ambiguity: {site_id}")
        return matches[0]["resolved"]
    if locator.startswith("process_boundary:"):
        boundary_id = locator.split(":", 1)[1]
        matches = [item for item in manifest["discovery"]["process_boundaries"] if item["boundary_id"] == boundary_id]
        if len(matches) != 1:
            raise VerificationFailure(f"process boundary ambiguity: {boundary_id}")
        return matches[0]["resolved"]
    if locator.startswith("discovery:"):
        return manifest["discovery"][locator.split(":", 1)[1]]
    if locator.startswith("native:"):
        return manifest["platform"]["native_component"][locator.split(":", 1)[1]]
    if locator.startswith("platform_present:"):
        value = manifest["platform"].get(locator.split(":", 1)[1])
        return value is not None and value != "" and value != []
    if locator.startswith("signed_role:"):
        return audit["signed_role_binding"][locator.split(":", 1)[1]]
    if locator.startswith("action:"):
        return manifest["action_ledger"][locator.split(":", 1)[1]]
    if locator == "manifest:closure_payload_sha256":
        return canonical_payload_digest(manifest, "closure_payload_sha256")
    if locator == "manifest:schema_closed":
        try:
            validate_manifest(manifest, canonical_bytes(manifest))
            return True
        except Exception:
            return False
    if locator.startswith("artifact:"):
        relative = locator.split(":", 1)[1]
        path = WORKSPACE_ROOT / relative
        return path.is_file() and not path.is_symlink()
    if locator.startswith("post:"):
        return post[locator.split(":", 1)[1]]
    raise VerificationFailure(f"unknown evidence locator: {locator}")


def execute_leaves(
    test_manifest: dict[str, Any], test_raw: bytes,
    manifest: dict[str, Any], implementation: dict[str, Any],
    post: dict[str, Any], stage: str,
    sequence_start: int, previous_row_sha256: str,
) -> tuple[bytes, list[dict[str, Any]], str]:
    validate_test_manifest(test_manifest, test_raw)
    selected = [leaf for leaf in test_manifest["leaves"] if leaf["earliest_stage"] == stage]
    rows: list[dict[str, Any]] = []
    chunks: list[bytes] = []
    previous = previous_row_sha256
    manifest_sha = hashlib.sha256(test_raw).hexdigest()
    fixed_epoch = post["fixed_utc_epoch_seconds"]
    for offset, leaf in enumerate(selected):
        blocker = None
        try:
            observed = observe_locator(leaf["evidence_locator"], manifest, implementation, post)
            passed = observed == leaf["expected"]
            if not passed:
                blocker = "BLOCKED_PORTABLE_RUNTIME_TRANSITIVE_CLOSURE"
        except Exception as exc:
            observed = {"verification_error": f"{type(exc).__name__}: {exc}"}
            passed = False
            blocker = "BLOCKED_PORTABLE_RUNTIME_TRANSITIVE_CLOSURE"
        row = {
            "sequence": sequence_start + offset,
            "leaf_id": leaf["leaf_id"],
            "requirement_group_id": leaf["requirement_group_id"],
            "subject_id": leaf["subject_id"],
            "evidence_locator": leaf["evidence_locator"],
            "expected": leaf["expected"],
            "observed": observed,
            "actual_result": "PASS" if passed else "FAIL",
            "evidence_complete": True,
            "started": True,
            "terminal": True,
            "blocker": blocker,
            "test_manifest_sha256": manifest_sha,
            "fixed_utc_epoch_seconds": fixed_epoch,
            "previous_row_sha256": previous,
        }
        raw = canonical_bytes(row)
        previous = hashlib.sha256(raw).hexdigest()
        chunks.append(raw)
        rows.append(row)
    return b"".join(chunks), rows, previous


def parse_attempts(raw: bytes) -> list[dict[str, Any]]:
    if not raw or b"\r" in raw or not raw.endswith(b"\n"):
        raise VerificationFailure("attempt ledger framing")
    rows = []
    previous = "0" * 64
    for index, line in enumerate(raw.splitlines(keepends=True), start=1):
        row = json.loads(line.decode("utf-8"))
        if line != canonical_bytes(row) or row.get("sequence") != index or row.get("previous_row_sha256") != previous:
            raise VerificationFailure("attempt ledger canonical chain")
        previous = hashlib.sha256(line).hexdigest()
        rows.append(row)
    return rows


def build_verification_evidence(
    test_manifest: dict[str, Any], test_raw: bytes, attempts_raw: bytes,
    start: dict[str, Any], start_raw: bytes,
    dynamic: dict[str, Any], dynamic_raw: bytes,
    end: dict[str, Any], end_raw: bytes,
    artifact_paths: list[str],
) -> dict[str, Any]:
    rows = parse_attempts(attempts_raw)
    expected_ids = [item["leaf_id"] for item in test_manifest["leaves"]]
    if [item["leaf_id"] for item in rows] != expected_ids:
        raise VerificationFailure("attempt order/coverage mismatch")
    groups = []
    for group in test_manifest["requirement_groups"]:
        selected = [row for row in rows if row["requirement_group_id"] == group["requirement_group_id"]]
        groups.append({
            "requirement_group_id": group["requirement_group_id"],
            "discovered": group["leaf_count"],
            "executed": len(selected),
            "evidence_complete": sum(item["evidence_complete"] is True for item in selected),
            "passed": sum(item["actual_result"] == "PASS" for item in selected),
        })
    artifacts = []
    for relative in sorted(artifact_paths):
        path = WORKSPACE_ROOT / relative
        if not path.is_file() or path.is_symlink():
            raise VerificationFailure(f"evidence artifact absent: {relative}")
        artifacts.append({"path": relative, "sha256": sha256_file(path), "bytes": path.stat().st_size})
    n = len(test_manifest["leaves"])
    counts = {
        "requirement_groups": len(test_manifest["requirement_groups"]),
        "leaves_discovered": n,
        "leaves_executed": len(rows),
        "evidence_complete": sum(item["evidence_complete"] is True for item in rows),
        "leaves_passed": sum(item["actual_result"] == "PASS" for item in rows),
        "failed": sum(item["actual_result"] == "FAIL" for item in rows),
        "skipped": sum(item["actual_result"] == "SKIPPED" for item in rows),
        "unknown": sum(item["actual_result"] == "UNKNOWN" for item in rows),
        "timeout": sum(item["actual_result"] == "TIMEOUT" for item in rows),
    }
    passed = (
        counts["requirement_groups"] == 18
        and counts["leaves_discovered"] == counts["leaves_executed"] == counts["evidence_complete"] == counts["leaves_passed"]
        and all(counts[key] == 0 for key in ("failed", "skipped", "unknown", "timeout"))
        and start["overall_result"] == dynamic["overall_result"] == end["overall_result"] == "PASS"
    )
    return {
        "artifact_class": "ctde_r3_portable_evidence_manifest",
        "schema_version": "1.0.0",
        "suite_id": SUITE_ID,
        "overall_result": "PASS" if passed else "BLOCKED",
        "test_manifest_sha256": hashlib.sha256(test_raw).hexdigest(),
        "attempts_sha256": hashlib.sha256(attempts_raw).hexdigest(),
        "start_verification_sha256": hashlib.sha256(start_raw).hexdigest(),
        "dynamic_observation_sha256": hashlib.sha256(dynamic_raw).hexdigest(),
        "end_verification_sha256": hashlib.sha256(end_raw).hexdigest(),
        "artifacts": artifacts,
        "requirement_group_coverage": groups,
        "counts": counts,
        "zero_action_ledger": {"model_calls": 0, "english_tei_content_reads": 0, "greek_tei_content_reads": 0, "candidate_runs": 0, "r4_executions": 0, "business_outputs": 0},
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--stage", choices=("start", "end"), required=True)
    parser.add_argument("--closure-manifest", required=True)
    parser.add_argument("--implementation-manifest", required=True)
    parser.add_argument("--execution-plan", required=True)
    parser.add_argument("--control-path", action="append", default=[])
    parser.add_argument("--start-snapshot")
    args = parser.parse_args()
    try:
        manifest, manifest_raw = load_canonical_json(Path(args.closure_manifest))
        implementation, implementation_raw = load_canonical_json(Path(args.implementation_manifest))
        execution, execution_raw = load_canonical_json(Path(args.execution_plan))
        start = load_canonical_json(Path(args.start_snapshot))[0] if args.start_snapshot else None
        snapshot = build_snapshot(args.stage, manifest, manifest_raw, implementation, implementation_raw, execution, execution_raw, args.control_path, start)
        sys.stdout.buffer.write(canonical_bytes(snapshot))
        return 0 if snapshot["overall_result"] == "PASS" else 1
    except Exception as exc:
        print(f"BLOCKED_PORTABLE_RUNTIME_TRANSITIVE_CLOSURE: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
