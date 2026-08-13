from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / "runtime"
if str(RUNTIME) not in sys.path:
    sys.path.insert(0, str(RUNTIME))

from ctde_runtime.common import dump_json, dump_yaml, load_yaml, sha256_file


PRE_REGISTRATION = {
    "malformed_yaml_rejected",
    "duplicate_key_rejected",
    "self_digest_rejected",
    "missing_required_field_rejected",
    "missing_version_rejected",
    "legacy_version_rejected",
    "unknown_version_rejected",
    "profile_missing_rejected",
    "wrong_profile_rejected",
    "one_time_false_rejected",
    "retry_true_rejected",
    "inheritance_true_rejected",
    "time_ordering_rejected",
    "invalid_timezone_rejected",
    "denied_policy_mutation_rejected",
}

REGISTRY_OPERATION_BUDGET = {
    "valid_authorization_accepted": 5,
    "first_consume_accepted": 2,
    "wrong_run_rejected": 2,
    "wrong_source_rejected": 2,
    "wrong_source_snapshot_rejected": 2,
    "wrong_structure_map_rejected": 2,
    "wrong_task_scope_rejected": 2,
    "out_of_range_rejected": 2,
    "unauthorized_consumer_rejected": 2,
    "unauthorized_output_rejected": 2,
    "denied_capability_rejected": 2,
    "expired_rejected": 2,
    "expiry_boundary_rejected": 2,
    "revoked_rejected": 3,
    "authorization_replay_rejected": 3,
    "registry_digest_mismatch_rejected": 1,
    "duplicate_nonce_rejected": 1,
    "wrong_nonce_rejected": 2,
    "wrong_stage_context_rejected": 5,
    "stale_context_rejected": 3,
    "caller_claims_mutation_rejected": 2,
    "registry_blob_tamper_rejected": 1,
    "audit_copy_mutation_detected": 1,
    "concurrent_consume_single_winner": 3,
    "crash_after_consume_blocks_recovery": 3,
    "post_consume_abort_blocks_retry": 4,
    "mint_lease_replay_rejected": 4,
    "preparation_failure_before_object": 4,
    "preparation_failure_after_object": 4,
    "capability_preparation_replay_rejected": 5,
    "crash_after_lease_blocks_preparation": 4,
    "crash_after_preparation_blocks_activation": 5,
    "capability_activation_replay_rejected": 6,
    "audit_writer_unavailable_pre_consume": 2,
    "audit_writer_failure_post_consume": 3,
    "audit_writer_failure_post_preparation": 5,
}

TWO_CONSUME_OPERATIONS = {"authorization_replay_rejected", "concurrent_consume_single_winner"}
NO_CONSUME_OPERATIONS = PRE_REGISTRATION | {
    "registry_digest_mismatch_rejected",
    "duplicate_nonce_rejected",
    "registry_blob_tamper_rejected",
    "audit_copy_mutation_detected",
}
TWO_CONTROLLER_RECORDS = {
    "authorization_replay_rejected",
    "concurrent_consume_single_winner",
    "crash_after_consume_blocks_recovery",
    "mint_lease_replay_rejected",
    "capability_preparation_replay_rejected",
    "crash_after_lease_blocks_preparation",
    "crash_after_preparation_blocks_activation",
    "capability_activation_replay_rejected",
}


def stable_hex(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def build(suite_id: str) -> Path:
    requirements_path = ROOT / "contracts" / "r2_portable_authorization_test_requirements.yaml"
    requirements = load_yaml(requirements_path)
    suite_root = ROOT / "r2_portable_suites" / suite_id
    if suite_root.exists():
        raise SystemExit(f"suite already exists: {suite_root}")
    leaves: list[dict[str, object]] = []
    ordinal = 0
    for requirement in requirements["requirements"]:
        for scenario in requirement["cases"]:
            ordinal += 1
            leaf_id = f"R2P-{ordinal:03d}-{scenario.upper().replace('_', '-')}"
            attempt_id = f"R2ATT-{stable_hex(suite_id + leaf_id)[:24]}"
            registry_count = 0 if scenario in PRE_REGISTRATION else REGISTRY_OPERATION_BUDGET[scenario]
            consume_count = 0 if scenario in NO_CONSUME_OPERATIONS else (2 if scenario in TWO_CONSUME_OPERATIONS else 1)
            controller_count = 2 if scenario in TWO_CONTROLLER_RECORDS else 1
            leaves.append(
                {
                    "leaf_id": leaf_id,
                    "requirement_id": requirement["requirement_id"],
                    "scenario": scenario,
                    "test_attempt_id": attempt_id,
                    "run_id": f"R2RUN-{stable_hex(attempt_id + 'run')[:24]}",
                    "authorization_id": f"R2AUTH-{stable_hex(attempt_id + 'auth')[:24]}",
                    "authorization_nonce": stable_hex(attempt_id + "nonce"),
                    "consume_operation_ids": [f"R2CON-{stable_hex(attempt_id + str(i))[:24]}" for i in range(consume_count)],
                    "registry_operation_ids": [f"R2OP-{stable_hex(attempt_id + str(i) + 'registry')[:24]}" for i in range(registry_count)],
                    "controller_terminal_ids": [f"R2TERM-{stable_hex(attempt_id + str(i) + 'terminal')[:24]}" for i in range(controller_count)],
                    "expected_leaf_result": "PASS",
                }
            )
    leaf_ids = [leaf["leaf_id"] for leaf in leaves]
    attempt_ids = [leaf["test_attempt_id"] for leaf in leaves]
    authorization_ids = [leaf["authorization_id"] for leaf in leaves]
    nonces = [leaf["authorization_nonce"] for leaf in leaves]
    if not (len(leaf_ids) == len(set(leaf_ids)) and len(attempt_ids) == len(set(attempt_ids))):
        raise SystemExit("duplicate leaf or attempt identity")
    if not (len(authorization_ids) == len(set(authorization_ids)) and len(nonces) == len(set(nonces))):
        raise SystemExit("cross-case authorization or nonce reuse")

    manifest = {
        "schema_version": "1.0.0",
        "artifact_class": "ctde_r2_portable_manifest",
        "suite_id": suite_id,
        "assurance_profile_id": "CTDE-PORTABLE-DEV-1",
        "highest_claimed_evidence_level": "A1",
        "a2_os_file_access_proof": "NOT_PROVIDED",
        "certified": False,
        "synthetic_only": True,
        "source_open_allowed": False,
        "broker_open_allowed": False,
        "bounded_delivery_allowed": False,
        "candidate_allowed": False,
        "model_calls_allowed": False,
        "business_outputs_allowed": False,
        "requirements_sha256": sha256_file(requirements_path),
        "leaves": leaves,
    }
    control = suite_root / "control"
    manifest_path = control / "r2_portable_manifest.yaml"
    dump_yaml(manifest_path, manifest)

    component_paths = [
        ROOT / "contracts" / "authorization_schema_v2.yaml",
        ROOT / "contracts" / "authorization_registry_record_schema_v2.yaml",
        ROOT / "contracts" / "authorization_registry_event_schema_v2.yaml",
        ROOT / "contracts" / "r2_portable_controller_terminal_schema_v1.yaml",
        ROOT / "contracts" / "capability_claims_schema_v2.yaml",
        ROOT / "contracts" / "broker_envelope_schema_v2.yaml",
        ROOT / "contracts" / "audit_attestation_schema_v2.yaml",
        ROOT / "runtime" / "ctde_runtime" / "authorization_v2.py",
        ROOT / "runtime" / "ctde_runtime" / "authorization_registry.py",
        ROOT / "runtime" / "ctde_runtime" / "range_broker.py",
        ROOT / "runtime" / "ctde_runtime" / "bounded_reader.py",
        ROOT / "runtime" / "ctde_runtime" / "read_audit.py",
        ROOT / "runtime" / "ctde_runtime" / "events.py",
        ROOT / "runtime" / "build_r2_portable_manifest.py",
        ROOT / "runtime" / "run_r2_portable.py",
    ]
    dump_json(
        control / "component_inputs.json",
        {
            "suite_id": suite_id,
            "manifest_sha256": sha256_file(manifest_path),
            "components": [
                {"path": str(path.relative_to(ROOT)), "sha256": sha256_file(path)} for path in component_paths
            ],
        },
    )
    return manifest_path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--suite-id", required=True)
    args = parser.parse_args()
    path = build(args.suite_id)
    print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
