from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml

from build_r3_portable_closure import (
    AUDIT_SHA256,
    PLAN_SHA256,
    PROFILE_ID,
    SUITE_ID,
    WORKSPACE_ROOT,
    canonical_bytes,
    load_canonical_json,
    sha256_file,
    validate_manifest,
)


PROTOTYPE_ROOT = Path(__file__).resolve().parents[1]
REQUIREMENTS_PATH = PROTOTYPE_ROOT / "contracts" / "r3_portable_closure_test_requirements.yaml"


class TestManifestFailure(RuntimeError):
    pass


def _leaf(group: str, subject_kind: str, subject_id: str, method: str, locator: str, expected: Any, earliest_stage: str = "R3-S7-OBSERVE") -> dict[str, Any]:
    payload = canonical_bytes({"group": group, "subject_kind": subject_kind, "subject_id": subject_id, "method": method, "locator": locator})
    slug = re.sub(r"[^A-Z0-9]+", "-", subject_kind.upper()).strip("-")[:24]
    return {
        "leaf_id": f"{group}-{slug}-{hashlib.sha256(payload).hexdigest()[:16]}",
        "requirement_group_id": group,
        "subject_kind": subject_kind,
        "subject_id": subject_id,
        "method": method,
        "evidence_locator": locator,
        "expected": expected,
        "earliest_stage": earliest_stage,
    }


def _requirements() -> dict[str, Any]:
    value = yaml.safe_load(REQUIREMENTS_PATH.read_bytes())
    if type(value) is not dict:
        raise TestManifestFailure("requirements object")
    groups = [item["requirement_group_id"] for item in value.get("requirement_groups", [])]
    if groups != [f"R3-VG{index:02d}" for index in range(1, 19)]:
        raise TestManifestFailure("requirements group identity")
    return value


def build_fixture_catalog(manifest: dict[str, Any], manifest_raw: bytes) -> dict[str, Any]:
    validate_manifest(manifest, manifest_raw)
    return {
        "artifact_class": "ctde_r3_portable_synthetic_fixture_catalog",
        "schema_version": "1.0.0",
        "suite_id": SUITE_ID,
        "synthetic_only": True,
        "source_content_allowed": False,
        "model_calls_allowed": False,
        "candidate_execution_allowed": False,
        "r4_execution_allowed": False,
        "business_outputs_allowed": False,
        "closure_manifest_sha256": hashlib.sha256(manifest_raw).hexdigest(),
        "recipes": [
            {"recipe_id": "R3FX-IDENTITY", "kind": "identity_rehash", "content_bytes": 0},
            {"recipe_id": "R3FX-AST", "kind": "ast_exact_locator", "content_bytes": 0},
            {"recipe_id": "R3FX-PLATFORM", "kind": "platform_boundary_rehash", "content_bytes": 0},
            {"recipe_id": "R3FX-DYNAMIC", "kind": "no_content_runtime_import_observation", "content_bytes": 0},
            {"recipe_id": "R3FX-DELTA", "kind": "start_end_immutable_delta", "content_bytes": 0},
        ],
    }


def build_test_manifest(manifest: dict[str, Any], manifest_raw: bytes, fixture_raw: bytes, implementation: dict[str, Any]) -> dict[str, Any]:
    validate_manifest(manifest, manifest_raw)
    requirements = _requirements()
    leaves: list[dict[str, Any]] = []

    identities = {
        "plan_sha256": PLAN_SHA256,
        "audit_sha256": AUDIT_SHA256,
        "write_scope_sha256": manifest["identities"]["write_scope_sha256"],
        "git_head": manifest["identities"]["git_head"],
        "remote_main": manifest["identities"]["remote_main"],
        "machine_handoff_tag_target": manifest["identities"]["machine_handoff_tag_target"],
        "baseline_tag_target": manifest["identities"]["baseline_tag_target"],
        "public_trust_freeze_identity": manifest["identities"]["public_trust_freeze_identity"],
    }
    for key, expected in sorted(identities.items()):
        leaves.append(_leaf("R3-VG01", "frozen_identity", key, "value_equals", f"identity:{key}", expected))

    for record in implementation["files"]:
        leaves.append(_leaf("R3-VG02", "implementation_file", record["path"], "rehash_file", f"implementation:{record['path']}", record["sha256"]))
    leaves.append(_leaf("R3-VG02", "implementation_manifest", "bundle_file_count", "value_equals", "implementation_field:bundle_file_count", 15))

    for root in manifest["callable_roots"]:
        leaves.append(_leaf("R3-VG03", "callable_root", root["callable_id"], "ast_definition_and_digest", f"root:{root['callable_id']}", {"definition_count": 1, "sha256": root["containing_file_sha256"]}))
    for role in manifest["roles"]:
        leaves.append(_leaf("R3-VG03", "role_disposition", role["gap_id"], "value_equals", f"role:{role['gap_id']}:active_r3_blocker", False))
    for classification in sorted({node["classification"] for node in manifest["nodes"]}):
        leaves.append(_leaf("R3-VG03", "classification", classification, "inventory_contains", f"classification:{classification}", True))

    for edge in manifest["edges"]:
        edge_identity = hashlib.sha256(canonical_bytes(edge)).hexdigest()
        leaves.append(_leaf("R3-VG04", "closure_edge", edge_identity, "edge_recompute", f"edge:{edge_identity}", True))

    selected_types = {"schema", "policy", "configuration", "public_trust_record", "external_registry_record"}
    for node in manifest["nodes"]:
        if node["member_type"] in selected_types or node["identity"] in {"FRESH_R3_PORTABLE_TRANSITIVE_CLOSURE_PLAN.md", "FRESH_R3_CURRENT_TREE_AUDIT.json"}:
            leaves.append(_leaf("R3-VG05", "contract_config_or_formal", node["node_id"], "rehash_node", f"node:{node['node_id']}", node["sha256"]))

    for site in manifest["discovery"]["dynamic_sites"]:
        leaves.append(_leaf("R3-VG06", "dynamic_site", site["site_id"], "semantic_site_resolution", f"dynamic_site:{site['site_id']}", True))
    leaves.append(_leaf("R3-VG06", "unknown_dynamic_dependencies", "count", "value_equals", "discovery:unknown_dynamic_dependency_count", 0))

    for boundary in manifest["discovery"]["process_boundaries"]:
        leaves.append(_leaf("R3-VG07", "process_boundary", boundary["boundary_id"], "semantic_site_resolution", f"process_boundary:{boundary['boundary_id']}", True))
    for key in ("fixed_environment", "python_executable", "proc_available"):
        leaves.append(_leaf("R3-VG07", "execution_boundary", key, "value_present", f"platform_present:{key}", True))

    native = manifest["platform"]["native_component"]
    native_expectations = {
        "source_sha256": native["source_sha256"],
        "tracked_binary_sha256": native["tracked_binary_sha256"],
        "fresh_builds_byte_identical": True,
        "fresh_build_count": 2,
        "compiler_sha256": native["compiler_sha256"],
    }
    for key, expected in sorted(native_expectations.items()):
        leaves.append(_leaf("R3-VG08", "native_build", key, "value_equals", f"native:{key}", expected))

    for node in manifest["nodes"]:
        if node["classification"] == "platform_boundary":
            leaves.append(_leaf("R3-VG09", "platform_node", node["node_id"], "rehash_or_virtual_identity", f"platform_node:{node['node_id']}", node["sha256"]))
    for key in ("kernel", "userspace_id", "userspace_version", "filesystem_type", "mount", "python_version", "temporary_filesystem"):
        leaves.append(_leaf("R3-VG09", "platform_field", key, "value_present", f"platform_present:{key}", True))

    role_map = {item["gap_id"]: item for item in manifest["roles"]}
    leaves.append(_leaf("R3-VG10", "r3g03_binding", "result", "value_equals", "signed_role:r3g03_result_sha256", "78df12d69794d5fdc54d5e18c422744ec65ee6e898589ff8b833bb628e24e8b2"))
    leaves.append(_leaf("R3-VG10", "r3g03_binding", "disposition", "value_equals", "role:R3G-03-BOUNDED-PARSER-SCOPE:fresh_r3_disposition", role_map["R3G-03-BOUNDED-PARSER-SCOPE"]["fresh_r3_disposition"]))
    leaves.append(_leaf("R3-VG11", "r3g04_binding", "result", "value_equals", "signed_role:r3g04_result_sha256", "aee66549193c3608d689e004298fafa17cc5a26717f71d63f75335482d354090"))
    leaves.append(_leaf("R3-VG11", "r3g04_binding", "model_calls", "value_equals", "action:model_calls", 0))
    leaves.append(_leaf("R3-VG12", "r3g07_binding", "freeze", "value_equals", "signed_role:public_trust_freeze_identity", manifest["identities"]["public_trust_freeze_identity"]))
    leaves.append(_leaf("R3-VG12", "r3g07_binding", "private_key_dependency", "value_equals", "signed_role:private_key_dependency", False))
    leaves.append(_leaf("R3-VG12", "r3g07_binding", "public_key_status", "value_equals", "signed_role:public_key_status", "active"))

    for gap in ("R3G-01-PORTABLE-R4-SUITE-MANIFEST-BUILDER", "R3G-02-PORTABLE-R4-SUITE-RUNNER", "R3G-05-PORTABLE-LOGICAL-WRITE-MONITOR", "R3G-06-PORTABLE-R4-AGGREGATE-REPORT-GENERATOR"):
        leaves.append(_leaf("R3-VG13", "deferred_role", gap, "value_equals", f"role:{gap}:fresh_r3_disposition", "stage_scoped_deferred_to_R4"))

    leaves.append(_leaf("R3-VG14", "canonical_manifest", "closure_payload_sha256", "payload_digest_recompute", "manifest:closure_payload_sha256", manifest["closure_payload_sha256"]))
    leaves.append(_leaf("R3-VG14", "canonical_manifest", "schema_closed", "closed_schema", "manifest:schema_closed", True))
    leaves.append(_leaf("R3-VG14", "canonical_manifest", "two_pass_identical", "controller_attestation", "post:two_pass_manifest_identical", True))

    for path in (
        "runtime_capability_prototype/r3_portable_suites/R3PS-20260814-001/control/component_freeze.json",
        "runtime_capability_prototype/r3_portable_suites/R3PS-20260814-001/control/execution_snapshot_closure_binding.json",
        "runtime_capability_prototype/r3_portable_suites/R3PS-20260814-001/control/closure_snapshot_registry_record.json",
    ):
        leaves.append(_leaf("R3-VG15", "freeze_binding_registry", path, "artifact_present", f"artifact:{path}", True))

    for subject in ("start_verified", "dynamic_observation_complete", "end_verified", "closure_delta_count", "unknown_project_owned_loaded_bytes"):
        expected = 0 if subject in {"closure_delta_count", "unknown_project_owned_loaded_bytes"} else True
        leaves.append(_leaf("R3-VG16", "start_dynamic_end", subject, "post_evidence", f"post:{subject}", expected, "R3-S8-END"))

    for field in ("model_calls", "english_tei_content_reads", "greek_tei_content_reads", "candidate_runs", "r4_executions", "business_outputs"):
        leaves.append(_leaf("R3-VG17", "zero_action", field, "value_equals", f"action:{field}", 0))
    for field in ("existing_project_file_modifications", "scope_violations", "forbidden_path_accesses"):
        leaves.append(_leaf("R3-VG17", "scope_boundary", field, "post_evidence", f"post:{field}", 0, "R3-S8-END"))

    for subject, expected in (
        ("assurance_profile_id", PROFILE_ID),
        ("highest_claimed_evidence_level", "A1"),
        ("certified", False),
        ("hardened", False),
        ("candidate_ready", False),
        ("result_generator_present", True),
    ):
        leaves.append(_leaf("R3-VG18", "claim_and_result_contract", subject, "post_evidence", f"post:{subject}", expected, "R3-S8-END"))

    stage_order = {"R3-S7-OBSERVE": 0, "R3-S8-END": 1}
    leaves = sorted(leaves, key=lambda item: (stage_order[item["earliest_stage"]], item["leaf_id"]))
    ids = [item["leaf_id"] for item in leaves]
    if len(ids) != len(set(ids)):
        raise TestManifestFailure("duplicate leaf identity")
    groups = [f"R3-VG{index:02d}" for index in range(1, 19)]
    coverage = {group: 0 for group in groups}
    for leaf in leaves:
        coverage[leaf["requirement_group_id"]] += 1
    if any(count <= 0 for count in coverage.values()):
        raise TestManifestFailure("empty requirement group")
    result = {
        "artifact_class": "ctde_r3_portable_test_manifest",
        "schema_version": "1.0.0",
        "suite_id": SUITE_ID,
        "assurance_profile_id": PROFILE_ID,
        "synthetic_only": True,
        "requirements_sha256": sha256_file(REQUIREMENTS_PATH),
        "closure_manifest_sha256": hashlib.sha256(manifest_raw).hexdigest(),
        "fixture_catalog_sha256": hashlib.sha256(fixture_raw).hexdigest(),
        "requirement_groups": [{"requirement_group_id": group, "leaf_count": coverage[group]} for group in groups],
        "leaf_count": len(leaves),
        "leaves": leaves,
    }
    validate_test_manifest(result, canonical_bytes(result))
    return result


def validate_test_manifest(manifest: dict[str, Any], raw: bytes) -> None:
    fields = {"artifact_class", "schema_version", "suite_id", "assurance_profile_id", "synthetic_only", "requirements_sha256", "closure_manifest_sha256", "fixture_catalog_sha256", "requirement_groups", "leaf_count", "leaves"}
    if set(manifest) != fields or raw != canonical_bytes(manifest):
        raise TestManifestFailure("test manifest closed canonical contract")
    if manifest.get("suite_id") != SUITE_ID or manifest.get("synthetic_only") is not True:
        raise TestManifestFailure("test manifest identity")
    leaves = manifest.get("leaves")
    if type(leaves) is not list or manifest.get("leaf_count") != len(leaves) or not leaves:
        raise TestManifestFailure("test manifest leaf count")
    required_leaf_fields = {"leaf_id", "requirement_group_id", "subject_kind", "subject_id", "method", "evidence_locator", "expected", "earliest_stage"}
    if any(type(item) is not dict or set(item) != required_leaf_fields for item in leaves):
        raise TestManifestFailure("test leaf closed fields")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--closure-manifest", required=True)
    parser.add_argument("--fixture-catalog", required=True)
    parser.add_argument("--implementation-manifest", required=True)
    args = parser.parse_args()
    try:
        closure, closure_raw = load_canonical_json(Path(args.closure_manifest))
        _, fixture_raw = load_canonical_json(Path(args.fixture_catalog))
        implementation, _ = load_canonical_json(Path(args.implementation_manifest))
        sys.stdout.buffer.write(canonical_bytes(build_test_manifest(closure, closure_raw, fixture_raw, implementation)))
        return 0
    except Exception as exc:
        print(f"BLOCKED_PORTABLE_RUNTIME_TRANSITIVE_CLOSURE: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
