from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from build_r3_portable_closure import PROFILE_ID, SUITE_ID, WORKSPACE_ROOT, canonical_bytes, load_canonical_json, sha256_file, validate_manifest
from build_r3_portable_test_manifest import validate_test_manifest
from verify_r3_portable_closure import parse_attempts


PROTOTYPE_ROOT = Path(__file__).resolve().parents[1]
SUITE_ROOT = PROTOTYPE_ROOT / "r3_portable_suites" / SUITE_ID
CONTROL_ROOT = SUITE_ROOT / "control"
EVIDENCE_ROOT = SUITE_ROOT / "evidence"
ATTEMPTS_PATH = SUITE_ROOT / "attempts" / "r3_attempts.jsonl"
EVIDENCE_MANIFEST_PATH = EVIDENCE_ROOT / "evidence_manifest.json"
AGGREGATE_PATH = SUITE_ROOT / "aggregate" / "r3_portable_closure_results.json"
REPORT_PATH = WORKSPACE_ROOT / "PORTABLE_RUNTIME_TRANSITIVE_CLOSURE_RESULT.md"


class ResultBuildFailure(RuntimeError):
    pass


def _load_inputs() -> dict[str, Any]:
    names = {
        "implementation": CONTROL_ROOT / "r3_implementation_manifest.json",
        "execution": CONTROL_ROOT / "r3_execution_plan.json",
        "closure": CONTROL_ROOT / "runtime_transitive_closure_manifest.json",
        "test": CONTROL_ROOT / "r3_synthetic_test_manifest.json",
        "freeze": CONTROL_ROOT / "component_freeze.json",
        "binding": CONTROL_ROOT / "execution_snapshot_closure_binding.json",
        "registry": CONTROL_ROOT / "closure_snapshot_registry_record.json",
        "fixture": SUITE_ROOT / "fixtures" / "r3_synthetic_fixtures.json",
        "start": EVIDENCE_ROOT / "start" / "closure_start_verification.json",
        "dynamic": EVIDENCE_ROOT / "dynamic" / "dynamic_dependency_observation.json",
        "end": EVIDENCE_ROOT / "end" / "closure_end_verification.json",
        "evidence": EVIDENCE_MANIFEST_PATH,
    }
    values: dict[str, Any] = {}
    raws: dict[str, bytes] = {}
    for name, path in names.items():
        values[name], raws[name] = load_canonical_json(path)
    return {"values": values, "raws": raws, "paths": names}


def build_aggregate() -> dict[str, Any]:
    loaded = _load_inputs()
    values = loaded["values"]
    raws = loaded["raws"]
    validate_manifest(values["closure"], raws["closure"])
    validate_test_manifest(values["test"], raws["test"])
    attempts_raw = ATTEMPTS_PATH.read_bytes()
    attempts = parse_attempts(attempts_raw)
    counts = {
        "requirement_groups": len(values["test"]["requirement_groups"]),
        "leaves_discovered": values["test"]["leaf_count"],
        "leaves_executed": len(attempts),
        "evidence_complete": sum(row["evidence_complete"] is True for row in attempts),
        "leaves_passed": sum(row["actual_result"] == "PASS" for row in attempts),
        "failed": sum(row["actual_result"] == "FAIL" for row in attempts),
        "skipped": sum(row["actual_result"] == "SKIPPED" for row in attempts),
        "unknown": sum(row["actual_result"] == "UNKNOWN" for row in attempts),
        "timeout": sum(row["actual_result"] == "TIMEOUT" for row in attempts),
    }
    zero_counts = {
        "unknown_project_owned_loaded_bytes": values["dynamic"]["counts"]["unknown_project_owned_loaded_bytes"],
        "unresolved_symlinks": values["closure"]["discovery"]["unresolved_symlinks"],
        "closure_delta_count": values["end"]["counts"]["closure_delta_count"],
        "existing_project_file_modifications": values["end"]["counts"]["tracked_changes"],
        "scope_violations": values["end"]["counts"]["scope_violations"],
        "model_calls": values["closure"]["action_ledger"]["model_calls"],
        "source_content_reads": values["closure"]["action_ledger"]["english_tei_content_reads"] + values["closure"]["action_ledger"]["greek_tei_content_reads"],
    }
    passed = (
        counts["requirement_groups"] == 18
        and counts["leaves_discovered"] == counts["leaves_executed"] == counts["evidence_complete"] == counts["leaves_passed"]
        and all(counts[key] == 0 for key in ("failed", "skipped", "unknown", "timeout"))
        and all(value == 0 for value in zero_counts.values())
        and values["start"]["overall_result"] == values["dynamic"]["overall_result"] == values["end"]["overall_result"] == values["evidence"]["overall_result"] == "PASS"
        and values["freeze"]["closure_manifest_sha256"] == hashlib.sha256(raws["closure"]).hexdigest()
        and values["binding"]["component_freeze_sha256"] == hashlib.sha256(raws["freeze"]).hexdigest()
        and values["registry"]["execution_snapshot_binding_sha256"] == hashlib.sha256(raws["binding"]).hexdigest()
    )
    artifact_digests = {
        name: {"path": str(path.relative_to(WORKSPACE_ROOT)), "sha256": hashlib.sha256(raws[name]).hexdigest(), "bytes": len(raws[name])}
        for name, path in loaded["paths"].items()
    }
    return {
        "artifact_class": "ctde_r3_portable_closure_results",
        "schema_version": "1.0.0",
        "suite_id": SUITE_ID,
        "assurance_profile_id": PROFILE_ID,
        "highest_claimed_evidence_level": "A1",
        "overall_result": "PASS" if passed else "BLOCKED",
        "formal_status": "PASS_PORTABLE_RUNTIME_TRANSITIVE_CLOSURE" if passed else "BLOCKED_PORTABLE_RUNTIME_TRANSITIVE_CLOSURE",
        "artifact_digests": artifact_digests,
        "attempts": {"path": str(ATTEMPTS_PATH.relative_to(WORKSPACE_ROOT)), "sha256": hashlib.sha256(attempts_raw).hexdigest(), "bytes": len(attempts_raw)},
        "counts": counts,
        "zero_counts": zero_counts,
        "closure_inventory": {"nodes": len(values["closure"]["nodes"]), "edges": len(values["closure"]["edges"]), "dynamic_sites": len(values["closure"]["discovery"]["dynamic_sites"]), "process_boundaries": len(values["closure"]["discovery"]["process_boundaries"])},
        "native_rebuild": values["closure"]["platform"]["native_component"],
        "claim_ceiling": {"environment_class": "Development", "highest_claimed_evidence_level": "A1", "certified": False, "hardened": False, "candidate_ready": False},
        "action_ledger": values["closure"]["action_ledger"],
    }


def build_aggregate_bytes() -> bytes:
    return canonical_bytes(build_aggregate())


def build_report_bytes(aggregate: dict[str, Any] | None = None) -> bytes:
    result = aggregate or build_aggregate()
    counts = result["counts"]
    zero = result["zero_counts"]
    inventory = result["closure_inventory"]
    native = result["native_rebuild"]
    lines = [
        "# Portable Runtime Transitive Closure Result",
        "",
        f"**{result['formal_status']}**",
        "",
        "```yaml",
        f"phase_id: Phase 2-G-R3FRESH-E1",
        f"suite_id: {SUITE_ID}",
        f"assurance_profile_id: {PROFILE_ID}",
        "environment_class: Development",
        "highest_claimed_evidence_level: A1",
        "certified: false",
        "hardened: false",
        "candidate_ready: false",
        f"requirement_groups: {counts['requirement_groups']}",
        f"leaves_discovered: {counts['leaves_discovered']}",
        f"leaves_executed: {counts['leaves_executed']}",
        f"evidence_complete: {counts['evidence_complete']}",
        f"leaves_passed: {counts['leaves_passed']}",
        f"failed: {counts['failed']}",
        f"skipped: {counts['skipped']}",
        f"unknown: {counts['unknown']}",
        f"timeout: {counts['timeout']}",
        f"closure_nodes: {inventory['nodes']}",
        f"closure_edges: {inventory['edges']}",
        f"unknown_project_owned_loaded_bytes: {zero['unknown_project_owned_loaded_bytes']}",
        f"unresolved_symlinks: {zero['unresolved_symlinks']}",
        f"closure_delta_count: {zero['closure_delta_count']}",
        f"existing_project_file_modifications: {zero['existing_project_file_modifications']}",
        f"scope_violations: {zero['scope_violations']}",
        f"model_calls: {zero['model_calls']}",
        f"source_content_reads: {zero['source_content_reads']}",
        "candidate_runs: 0",
        "r4_executions: 0",
        "business_outputs: 0",
        "```",
        "",
        "## Deterministic closure",
        "",
        "The exact current Portable Runtime/control surface is transitively enumerated, frozen, and independently rehashed under the Development/A1 claim ceiling. Dynamic observation used synthetic no-content imports only.",
        "",
        "## Native boundary",
        "",
        f"Two fresh `{native['component_id']}` builds were byte-identical at `{native['fresh_build_sha256']}`. The historical tracked binary remains separately frozen at `{native['tracked_binary_sha256']}`; `tracked_binary_matches_fresh_build` is `{str(native['tracked_binary_matches_fresh_build']).lower()}` and no existing Runtime byte was replaced.",
        "",
        "## Scope ceiling",
        "",
        "This PASS is not R4 PASS, Candidate readiness, source-semantic authorization, a model call, production certification, or hardened isolation.",
        "",
    ]
    return "\n".join(lines).encode("utf-8")
