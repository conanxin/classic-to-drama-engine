from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import yaml


PROTOTYPE_ROOT = Path(__file__).resolve().parents[1]
WORKSPACE_ROOT = PROTOTYPE_ROOT.parent
CONTRACT_ROOT = PROTOTYPE_ROOT / "contracts"
SUITE_ROOT = PROTOTYPE_ROOT / "r3g07_portable_suites" / "R3G07PS-20260812-001"
CONTROL_ROOT = SUITE_ROOT / "control"
FIXTURE_ROOT = SUITE_ROOT / "fixtures"
ATTEMPTS_PATH = SUITE_ROOT / "attempts" / "r3g07_attempts.jsonl"
EVIDENCE_PATH = SUITE_ROOT / "evidence" / "r3g07_public_trust_verification.json"
AGGREGATE_PATH = SUITE_ROOT / "aggregate" / "r3g07_public_trust_results.json"
REQUIREMENTS_PATH = CONTRACT_ROOT / "r3g07_public_trust_test_requirements.yaml"

PHASE_ID = "Phase 2-G-R3G3"
PHASE_KIND = "r3g07_atomic_implementation_and_deterministic_verification_only"
GAP_ID = "R3G-07-IMMUTABLE-PUBLIC-TRUST-KEY-STATUS"
RUNTIME_ROLE = "immutable public trust material / key-status registry"
PROFILE_ID = "CTDE-PORTABLE-DEV-1"
AUTHORIZATION_REF = "R3G3-IA-20260813-001"
AUTHORIZATION_SHA256 = "49a61f4f1ffb779777576ae597d239eca9e6bee5f233cb7eb91b9966c2c88964"

FILE_CLASSIFICATIONS = {
    "runtime_capability_prototype/contracts/public_trust_material_schema_v1.yaml": "runtime_contract",
    "runtime_capability_prototype/contracts/public_key_status_registry_schema_v1.yaml": "runtime_contract",
    "runtime_capability_prototype/contracts/portable_public_trust_material_v1.json": "configuration_semantic_asset",
    "runtime_capability_prototype/contracts/portable_public_key_status_registry_v1.json": "configuration_semantic_asset",
    "runtime_capability_prototype/runtime/ctde_runtime/public_trust.py": "runtime_implementation",
    "runtime_capability_prototype/contracts/r3g07_public_trust_test_requirements.yaml": "test_control_contract",
    "runtime_capability_prototype/contracts/r3g07_public_trust_test_manifest_schema_v1.yaml": "test_contract",
    "runtime_capability_prototype/runtime/build_r3g07_public_trust_test_manifest.py": "build_only_control",
    "runtime_capability_prototype/runtime/verify_r3g07_public_trust.py": "verification_code",
    "runtime_capability_prototype/runtime/run_r3g07_public_trust.py": "test_controller",
    "runtime_capability_prototype/runtime/build_r3g07_public_trust_result.py": "build_only_control",
    "runtime_capability_prototype/r3g07_portable_suites/R3G07PS-20260812-001/control/r3g07_implementation_manifest.json": "control_artifact",
    "runtime_capability_prototype/r3g07_portable_suites/R3G07PS-20260812-001/control/r3g07_execution_plan.json": "control_artifact",
    "runtime_capability_prototype/r3g07_portable_suites/R3G07PS-20260812-001/control/r3g07_test_manifest.json": "test_manifest",
    "runtime_capability_prototype/r3g07_portable_suites/R3G07PS-20260812-001/fixtures/r3g07_synthetic_fixtures.json": "test_fixture",
    "runtime_capability_prototype/r3g07_portable_suites/R3G07PS-20260812-001/fixtures/r3g07_test_signing_key_ed25519_seed.hex": "test_secret_fixture",
    "runtime_capability_prototype/r3g07_portable_suites/R3G07PS-20260812-001/attempts/r3g07_attempts.jsonl": "test_evidence",
    "runtime_capability_prototype/r3g07_portable_suites/R3G07PS-20260812-001/evidence/r3g07_public_trust_verification.json": "a1_test_evidence",
    "runtime_capability_prototype/r3g07_portable_suites/R3G07PS-20260812-001/aggregate/r3g07_public_trust_results.json": "aggregate_test_evidence",
    "PORTABLE_RUNTIME_ROLE_GAP_R3G07_REPAIR_RESULT.md": "external_phase_result",
}


class ResultBuildFailure(RuntimeError):
    pass


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8") + b"\n"


def load_canonical_json(path: Path) -> tuple[dict[str, Any], bytes]:
    raw = path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf") or b"\r" in raw or not raw.endswith(b"\n") or raw.count(b"\n") != 1:
        raise ResultBuildFailure(f"noncanonical framing: {path}")

    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise ResultBuildFailure(f"duplicate JSON key: {path}:{key}")
            result[key] = value
        return result

    try:
        value = json.loads(raw.decode("utf-8"), object_pairs_hook=unique)
    except ResultBuildFailure:
        raise
    except Exception as exc:
        raise ResultBuildFailure(f"malformed JSON: {path}") from exc
    if type(value) is not dict or raw != canonical_bytes(value):
        raise ResultBuildFailure(f"noncanonical JSON: {path}")
    return value, raw


def _requirements() -> dict[str, Any]:
    value = yaml.safe_load(REQUIREMENTS_PATH.read_bytes())
    if type(value) is not dict:
        raise ResultBuildFailure("requirements object")
    return value


def _validate_closed(value: dict[str, Any], fields: list[str], label: str) -> None:
    if set(value) != set(fields):
        raise ResultBuildFailure(f"{label} closed fields")


def _validate_evidence(
    evidence: dict[str, Any],
    evidence_raw: bytes,
    manifest: dict[str, Any],
    attempts: list[dict[str, Any]],
) -> None:
    requirements = _requirements()
    _validate_closed(evidence, requirements["artifact_contracts"]["verification_evidence_fields"], "verification evidence")
    constants = {
        "artifact_class": "ctde_r3g07_public_trust_verification_evidence",
        "schema_version": "1.0.0",
        "suite_id": "R3G07PS-20260812-001",
        "assurance_profile_id": PROFILE_ID,
        "highest_claimed_evidence_level": "A1",
        "overall_result": "PASS",
    }
    if any(evidence.get(field) != expected for field, expected in constants.items()):
        raise ResultBuildFailure("verification evidence constant mismatch")
    if not evidence["subject_digests"]:
        raise ResultBuildFailure("verification evidence subjects absent")
    for item in evidence["subject_digests"]:
        if set(item) != {"path", "sha256"}:
            raise ResultBuildFailure("subject digest closed fields")
        path = WORKSPACE_ROOT / item["path"]
        if not path.is_file() or path.is_symlink() or sha256_file(path) != item["sha256"]:
            raise ResultBuildFailure(f"subject digest mismatch: {item['path']}")
    if set(evidence["schema_checks"].values()) != {True} or set(evidence["canonical_checks"].values()) != {True}:
        raise ResultBuildFailure("schema or canonical verification failure")
    if evidence["loader_checks"].get("fixed_epoch") != 1786597200 or not evidence["loader_checks"].get("repeated_load_reproducible"):
        raise ResultBuildFailure("loader verification failure")
    coverage = evidence["requirement_group_coverage"]
    if [item["requirement_group_id"] for item in coverage] != [f"PT-{index:02d}" for index in range(1, 22)]:
        raise ResultBuildFailure("requirement group evidence identity")
    if any(item["leaf_count"] <= 0 or item["passed"] != item["leaf_count"] or item["complete"] is not True for item in coverage):
        raise ResultBuildFailure("requirement group evidence incomplete")
    bindings = evidence["caller_bindings"]
    if [item["caller_id"] for item in bindings] != [f"C0{index}" for index in range(1, 7)]:
        raise ResultBuildFailure("caller binding identity")
    if any(item["result"] != "PASS" or item["existing_file_modified"] is not False for item in bindings):
        raise ResultBuildFailure("caller binding result")
    freezes = {item["public_trust_freeze_identity"] for item in bindings}
    if len(freezes) != 1:
        raise ResultBuildFailure("caller freeze identity divergence")
    if evidence["r2_baseline_check"] != {"checked": 16, "mismatches": [], "semantic_regressions": 0}:
        raise ResultBuildFailure("R2 baseline evidence")
    if any(value != 0 for value in evidence["scope_delta"].values()):
        raise ResultBuildFailure("scope delta evidence")
    private = evidence["private_exclusion"]
    if private.get("test_public_key_distinct") is not True or private.get("production_closure_membership") is not False or private.get("seed_bytes_in_evidence") is not False:
        raise ResultBuildFailure("private test material exclusion")
    seed = (FIXTURE_ROOT / "r3g07_test_signing_key_ed25519_seed.hex").read_bytes()[:-1]
    if seed in evidence_raw:
        raise ResultBuildFailure("private seed bytes in evidence")
    counts = evidence["counts"]
    n = manifest["leaf_count"]
    if any(counts.get(field) != n for field in ("manifest_leaf_count", "discovered", "executed", "evidence_complete", "passed")):
        raise ResultBuildFailure("evidence count mismatch")
    if any(counts.get(field) != 0 for field in ("failed", "skipped", "unknown", "timeout")):
        raise ResultBuildFailure("evidence terminal failures")
    if len(attempts) != n:
        raise ResultBuildFailure("attempt count mismatch")


def build_aggregate() -> dict[str, Any]:
    requirements = _requirements()
    implementation, implementation_raw = load_canonical_json(CONTROL_ROOT / "r3g07_implementation_manifest.json")
    execution, execution_raw = load_canonical_json(CONTROL_ROOT / "r3g07_execution_plan.json")
    manifest, manifest_raw = load_canonical_json(CONTROL_ROOT / "r3g07_test_manifest.json")
    _, fixture_raw = load_canonical_json(FIXTURE_ROOT / "r3g07_synthetic_fixtures.json")
    attempts_raw = ATTEMPTS_PATH.read_bytes()
    evidence, evidence_raw = load_canonical_json(EVIDENCE_PATH)

    import verify_r3g07_public_trust as verifier

    verifier.validate_manifest(manifest, manifest_raw)
    attempts = verifier.parse_attempts_bytes(attempts_raw)
    verifier.validate_attempts(manifest, manifest_raw, attempts, attempts_raw)
    _validate_evidence(evidence, evidence_raw, manifest, attempts)
    _validate_closed(implementation, requirements["artifact_contracts"]["implementation_manifest_fields"], "implementation manifest")
    _validate_closed(execution, requirements["artifact_contracts"]["execution_plan_fields"], "execution plan")
    if execution["implementation_manifest_sha256"] != hashlib.sha256(implementation_raw).hexdigest():
        raise ResultBuildFailure("execution-to-implementation digest")

    discovered = len(manifest["leaves"])
    executed = len(attempts)
    evidence_complete = sum(row["evidence_complete"] is True for row in attempts)
    passed = sum(row["actual_result"] == "PASS" for row in attempts)
    failed = sum(row["actual_result"] == "FAIL" for row in attempts)
    skipped = sum(row["actual_result"] == "SKIPPED" for row in attempts)
    unknown = sum(row["actual_result"] == "UNKNOWN" for row in attempts)
    timeout = sum(row["actual_result"] == "TIMEOUT" for row in attempts)
    binding_count = sum(item["result"] == "PASS" for item in evidence["caller_bindings"])
    private_ok = (
        evidence["private_exclusion"]["test_public_key_distinct"] is True
        and evidence["private_exclusion"]["production_closure_membership"] is False
        and evidence["private_exclusion"]["seed_bytes_in_evidence"] is False
    )
    scope_violation_count = len(implementation["unexpected_paths"]) + len(implementation["missing_paths"])
    aggregate = {
        "artifact_class": "ctde_r3g07_public_trust_results",
        "schema_version": "1.0.0",
        "suite_id": "R3G07PS-20260812-001",
        "assurance_profile_id": PROFILE_ID,
        "highest_claimed_evidence_level": "A1",
        "implementation_manifest_sha256": hashlib.sha256(implementation_raw).hexdigest(),
        "execution_plan_sha256": hashlib.sha256(execution_raw).hexdigest(),
        "test_manifest_sha256": hashlib.sha256(manifest_raw).hexdigest(),
        "fixture_catalog_sha256": hashlib.sha256(fixture_raw).hexdigest(),
        "attempts_sha256": hashlib.sha256(attempts_raw).hexdigest(),
        "verification_evidence_sha256": hashlib.sha256(evidence_raw).hexdigest(),
        "manifest_leaf_count": manifest["leaf_count"],
        "discovered": discovered,
        "executed": executed,
        "evidence_complete": evidence_complete,
        "passed": passed,
        "failed": failed,
        "skipped": skipped,
        "unknown": unknown,
        "timeout": timeout,
        "existing_modified_files_count": len(implementation["existing_modified_files"]),
        "created_files_count": len(implementation["creatable_files"]),
        "created_directories_count": len(implementation["creatable_directories"]),
        "caller_bindings_passed": binding_count,
        "r2_asset_modification_count": len(evidence["r2_baseline_check"]["mismatches"]),
        "r2_semantic_regression_count": evidence["r2_baseline_check"]["semantic_regressions"],
        "other_r3g_modification_count": evidence["scope_delta"]["other_r3g_modifications"],
        "scope_violation_count": scope_violation_count,
        "forbidden_path_access_count": evidence["scope_delta"]["forbidden_path_accesses"],
        "private_test_exclusion": private_ok,
        "fresh_r3_replan_required": True,
        "minimal_embedded_role_mapping_required": True,
        "implementation_authorized": False,
        "r3_execution_authorized": False,
        "overall_result": "PASS",
    }
    n = manifest["leaf_count"]
    pass_predicates = (
        all(aggregate[field] == n for field in ("manifest_leaf_count", "discovered", "executed", "evidence_complete", "passed"))
        and all(aggregate[field] == 0 for field in ("failed", "skipped", "unknown", "timeout"))
        and aggregate["existing_modified_files_count"] == 0
        and aggregate["created_files_count"] == 20
        and aggregate["created_directories_count"] == 7
        and aggregate["caller_bindings_passed"] == 6
        and all(aggregate[field] == 0 for field in (
            "r2_asset_modification_count", "r2_semantic_regression_count", "other_r3g_modification_count",
            "scope_violation_count", "forbidden_path_access_count",
        ))
        and aggregate["private_test_exclusion"] is True
        and evidence["overall_result"] == "PASS"
    )
    aggregate["overall_result"] = "PASS" if pass_predicates else "FAIL"
    _validate_closed(aggregate, requirements["artifact_contracts"]["aggregate_fields"], "aggregate")
    return aggregate


def build_aggregate_bytes() -> bytes:
    return canonical_bytes(build_aggregate())


def _created_file_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    report_path = "PORTABLE_RUNTIME_ROLE_GAP_R3G07_REPAIR_RESULT.md"
    for path, classification in FILE_CLASSIFICATIONS.items():
        if path == report_path:
            rows.append(
                {
                    "path": path,
                    "classification": classification,
                    "before_state": "ABSENT",
                    "after_state": "CREATED_BY_THIS_REPORT",
                    "self_digest_in_report": False,
                }
            )
        else:
            absolute = WORKSPACE_ROOT / path
            if not absolute.is_file() or absolute.is_symlink():
                raise ResultBuildFailure(f"created file absent before report: {path}")
            rows.append(
                {
                    "path": path,
                    "classification": classification,
                    "before_state": "ABSENT",
                    "after_state": "CREATED",
                    "after_sha256": sha256_file(absolute),
                }
            )
    return rows


def build_report_payload() -> dict[str, Any]:
    requirements = _requirements()
    aggregate, aggregate_raw = load_canonical_json(AGGREGATE_PATH)
    _validate_closed(aggregate, requirements["artifact_contracts"]["aggregate_fields"], "aggregate")
    if aggregate["overall_result"] not in {"PASS", "FAIL"}:
        raise ResultBuildFailure("aggregate result vocabulary")
    implementation, _ = load_canonical_json(CONTROL_ROOT / "r3g07_implementation_manifest.json")
    execution, _ = load_canonical_json(CONTROL_ROOT / "r3g07_execution_plan.json")
    evidence, _ = load_canonical_json(EVIDENCE_PATH)
    material, _ = load_canonical_json(CONTRACT_ROOT / "portable_public_trust_material_v1.json")
    status, _ = load_canonical_json(CONTRACT_ROOT / "portable_public_key_status_registry_v1.json")

    from ctde_runtime.public_trust import load_portable_public_trust

    loaded = load_portable_public_trust()
    final_status = (
        "PASS_PORTABLE_RUNTIME_ROLE_GAP_R3G07_REPAIRED"
        if aggregate["overall_result"] == "PASS"
        else "BLOCKED_PORTABLE_RUNTIME_ROLE_GAP_R3G07_REPAIR_FAILED"
    )
    payload = {
        "final_status": final_status,
        "gap_id": GAP_ID,
        "runtime_role": RUNTIME_ROLE,
        "phase_id": PHASE_ID,
        "phase_kind": PHASE_KIND,
        "assurance_profile_id": PROFILE_ID,
        "highest_claimed_evidence_level": "A1",
        "implementation_authorization_ref": AUTHORIZATION_REF,
        "implementation_authorization_sha256": AUTHORIZATION_SHA256,
        "actual_created_files": _created_file_rows(),
        "actual_created_directories": [
            {"path": path, "before_state": "ABSENT", "after_state": "CREATED"}
            for path in implementation["creatable_directories"]
        ],
        "existing_modified_files": implementation["existing_modified_files"],
        "caller_binding_results": evidence["caller_bindings"],
        "trust_material_identity": {
            "path": "runtime_capability_prototype/contracts/portable_public_trust_material_v1.json",
            "file_sha256": loaded.material_sha256,
            "semantic_payload_sha256": loaded.semantic_payload_sha256,
            "kid_set": [item["kid"] for item in material["keys"]],
            "public_key_bytes_sha256": [item["public_key_bytes_sha256"] for item in material["keys"]],
        },
        "status_registry_identity": {
            "path": "runtime_capability_prototype/contracts/portable_public_key_status_registry_v1.json",
            "file_sha256": loaded.status_registry_sha256,
            "material_sha256": status["material_sha256"],
            "statuses": [{"kid": item["kid"], "status": item["status"]} for item in status["keys"]],
        },
        "loader_freeze_identity": {
            "loader_sha256": loaded.loader_sha256,
            "signing_sha256": loaded.signing_sha256,
            "public_trust_freeze_identity": loaded.public_trust_freeze_identity,
            "fixed_utc_epoch_seconds": execution["fixed_utc_epoch_seconds"],
        },
        "test_counts": {field: aggregate[field] for field in (
            "manifest_leaf_count", "discovered", "executed", "evidence_complete", "passed",
            "failed", "skipped", "unknown", "timeout",
        )},
        "r2_asset_modification_count": aggregate["r2_asset_modification_count"],
        "r2_semantic_regression_count": aggregate["r2_semantic_regression_count"],
        "other_r3g_modification_count": aggregate["other_r3g_modification_count"],
        "scope_violation_count": aggregate["scope_violation_count"],
        "forbidden_path_access_count": aggregate["forbidden_path_access_count"],
        "private_test_exclusion": {
            "proven": aggregate["private_test_exclusion"],
            "test_public_key_distinct": evidence["private_exclusion"]["test_public_key_distinct"],
            "production_closure_membership": evidence["private_exclusion"]["production_closure_membership"],
            "seed_bytes_in_report": False,
        },
        "english_tei_content_read_count": 0,
        "greek_tei_content_read_count": 0,
        "candidate_run_count": 0,
        "model_call_count": 0,
        "business_output_count": 0,
        "fresh_r3_replan_required": True,
        "minimal_embedded_role_mapping_required": True,
        "execution_authorized": False,
    }
    _validate_closed(payload, requirements["artifact_contracts"]["result_report_required_fields"], "result report")
    if len(payload["actual_created_files"]) != 20 or len(payload["actual_created_directories"]) != 7:
        raise ResultBuildFailure("result scope accounting")
    if hashlib.sha256(aggregate_raw).hexdigest() != sha256_file(AGGREGATE_PATH):
        raise ResultBuildFailure("aggregate exact byte identity")
    return payload


def render_report(payload: dict[str, Any]) -> bytes:
    status = payload["final_status"]
    body = canonical_bytes(payload).decode("utf-8").rstrip("\n")
    text = (
        "# Portable Runtime Role Gap R3G-07 Repair Result\n\n"
        f"{status}\n\n"
        "Portable / Development; A1 only; non-certified. R3 has not executed and has not passed.\n\n"
        "```json\n"
        f"{body}\n"
        "```\n"
    )
    return text.encode("utf-8")


def build_report_bytes() -> bytes:
    return render_report(build_report_payload())


if __name__ == "__main__":
    import sys

    sys.stdout.buffer.write(build_aggregate_bytes())
