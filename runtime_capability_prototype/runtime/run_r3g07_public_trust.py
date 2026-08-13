from __future__ import annotations

import hashlib
import importlib
import json
import sys
from pathlib import Path
from typing import Any

import yaml

from ctde_runtime.public_trust import load_portable_public_trust


PROTOTYPE_ROOT = Path(__file__).resolve().parents[1]
WORKSPACE_ROOT = PROTOTYPE_ROOT.parent
SUITE_ROOT = PROTOTYPE_ROOT / "r3g07_portable_suites" / "R3G07PS-20260812-001"
CONTROL_ROOT = SUITE_ROOT / "control"
ATTEMPTS_PATH = SUITE_ROOT / "attempts" / "r3g07_attempts.jsonl"
EVIDENCE_PATH = SUITE_ROOT / "evidence" / "r3g07_public_trust_verification.json"
AGGREGATE_PATH = SUITE_ROOT / "aggregate" / "r3g07_public_trust_results.json"
REPORT_PATH = WORKSPACE_ROOT / "PORTABLE_RUNTIME_ROLE_GAP_R3G07_REPAIR_RESULT.md"
REQUIREMENTS_PATH = PROTOTYPE_ROOT / "contracts" / "r3g07_public_trust_test_requirements.yaml"

PHASE_ID = "Phase 2-G-R3G3"
PHASE_KIND = "r3g07_atomic_implementation_and_deterministic_verification_only"
PROFILE_ID = "CTDE-PORTABLE-DEV-1"
TRUST_DOMAIN = "ctde-portable-runtime"
FIXED_EPOCH = 1786597200
AUTHORIZATION_REF = "R3G3-IA-20260813-001"
AUTHORIZATION_SHA256 = "49a61f4f1ffb779777576ae597d239eca9e6bee5f233cb7eb91b9966c2c88964"
PLAN_SHA256 = "fbd689f287be47aa5aa9cc3ebb256c9b7512101be073d92b1d27ae65ce0c577a"
AUDIT_SHA256 = "e5cd250eeaec8921afd6658e55d140e4f897ce99860e2825aad1af14f6eab1f7"
AUTHORIZED_SCOPE_SHA256 = "989ae9e64a055b9313d537aeffc67714c4ed47277992206fe3197131e5e24d53"

WRITE_ALLOWLIST = (ATTEMPTS_PATH, EVIDENCE_PATH, AGGREGATE_PATH, REPORT_PATH)


class ControllerFailure(RuntimeError):
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
        raise ControllerFailure(f"noncanonical framing: {path}")

    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise ControllerFailure(f"duplicate JSON key: {path}:{key}")
            result[key] = value
        return result

    try:
        value = json.loads(raw.decode("utf-8"), object_pairs_hook=unique)
    except ControllerFailure:
        raise
    except Exception as exc:
        raise ControllerFailure(f"malformed JSON: {path}") from exc
    if type(value) is not dict or raw != canonical_bytes(value):
        raise ControllerFailure(f"noncanonical JSON: {path}")
    return value, raw


def _exclusive_write(path: Path, raw: bytes) -> None:
    if path not in WRITE_ALLOWLIST:
        raise ControllerFailure(f"write outside allowlist: {path}")
    if path.exists() or path.is_symlink() or not path.parent.is_dir():
        raise ControllerFailure(f"create-once output state invalid: {path}")
    with path.open("xb") as handle:
        handle.write(raw)
        handle.flush()
    if path.read_bytes() != raw:
        raise ControllerFailure(f"persisted bytes mismatch: {path}")


def _validate_execution_plan(plan: dict[str, Any], requirements: dict[str, Any]) -> None:
    expected_fields = set(requirements["artifact_contracts"]["execution_plan_fields"])
    if set(plan) != expected_fields:
        raise ControllerFailure("execution plan closed fields")
    exact = {
        "artifact_class": "ctde_r3g07_execution_plan",
        "schema_version": "1.0.0",
        "suite_id": "R3G07PS-20260812-001",
        "assurance_profile_id": PROFILE_ID,
        "phase_id": PHASE_ID,
        "phase_kind": PHASE_KIND,
        "implementation_authorization_ref": AUTHORIZATION_REF,
        "implementation_authorization_sha256": AUTHORIZATION_SHA256,
        "plan_path": "PORTABLE_RUNTIME_PUBLIC_TRUST_BINDING_PLAN.md",
        "plan_sha256": PLAN_SHA256,
        "scope_audit_path": "PORTABLE_RUNTIME_PUBLIC_TRUST_BINDING_SCOPE_AUDIT.md",
        "scope_audit_sha256": AUDIT_SHA256,
        "fixed_utc_epoch_seconds": FIXED_EPOCH,
        "trust_domain": TRUST_DOMAIN,
        "authorized_scope_sha256": AUTHORIZED_SCOPE_SHA256,
        "implementation_status": "implemented_waiting_for_deterministic_verification",
        "test_status": "authorized_not_started",
    }
    for field, expected in exact.items():
        if plan.get(field) != expected:
            raise ControllerFailure(f"execution plan mismatch: {field}")
    if plan.get("implementation_manifest_sha256") != sha256_file(CONTROL_ROOT / "r3g07_implementation_manifest.json"):
        raise ControllerFailure("implementation manifest digest mismatch")
    if plan.get("authorization_contract_sha256") != "3954c28a8e185a54d89c5e450c2feac5e16f4ada907daec002834995c6988db8":
        raise ControllerFailure("authorization contract digest mismatch")
    if plan.get("public_trust_record_sha256") != "7395298aa4c10400d10fdf68558994fcc4a3c275bb684cf09f179c7aec7eb2dd":
        raise ControllerFailure("public trust record digest mismatch")
    if type(plan.get("mutable_existing_files")) is not list or plan["mutable_existing_files"]:
        raise ControllerFailure("mutable existing files must be empty")
    if len(plan.get("creatable_files", [])) != 20 or len(plan.get("creatable_directories", [])) != 7:
        raise ControllerFailure("execution scope count mismatch")


def _attempt_row(
    sequence: int,
    leaf: dict[str, Any],
    manifest_sha256: str,
    previous_row_sha256: str,
    result: dict[str, Any] | None,
    failure: BaseException | None,
) -> dict[str, Any]:
    if failure is None and result is not None:
        actual_result = result.get("actual_result", "FAIL")
        blocker = result.get("blocker")
        side_effect_counts = result.get("side_effect_counts", {})
        evidence_complete = actual_result == "PASS"
    else:
        actual_result = "FAIL"
        blocker = getattr(failure, "code", None) or "BLOCKED_R3G07_TEST_LEAF_FAILED"
        side_effect_counts = {
            "source_reads": 0,
            "path_actions": 0,
            "fd_actions": 0,
            "model_calls": 0,
            "business_outputs": 0,
        }
        evidence_complete = True
    return {
        "sequence": sequence,
        "leaf_id": leaf["leaf_id"],
        "requirement_group_id": leaf["requirement_group_id"],
        "scenario": leaf["scenario"],
        "caller_id": leaf["caller_id"],
        "input_identity_sha256": leaf["input_identity_sha256"],
        "expected_result": leaf["expected_result"],
        "actual_result": actual_result,
        "started": True,
        "terminal": True,
        "blocker": blocker,
        "evidence_complete": evidence_complete,
        "side_effect_counts": side_effect_counts,
        "fixed_utc_epoch_seconds": FIXED_EPOCH,
        "test_manifest_sha256": manifest_sha256,
        "previous_row_sha256": previous_row_sha256,
    }


def build_attempts_bytes(manifest: dict[str, Any], manifest_raw: bytes) -> tuple[bytes, list[dict[str, Any]]]:
    verifier = importlib.import_module("verify_r3g07_public_trust")
    verifier.validate_manifest(manifest, manifest_raw)
    loaded = load_portable_public_trust()
    bound_codec = loaded.codec(FIXED_EPOCH)
    manifest_sha256 = hashlib.sha256(manifest_raw).hexdigest()
    previous = "0" * 64
    chunks: list[bytes] = []
    rows: list[dict[str, Any]] = []
    for sequence, leaf in enumerate(manifest["leaves"], start=1):
        result: dict[str, Any] | None = None
        failure: BaseException | None = None
        try:
            result = verifier.execute_leaf(leaf, loaded, bound_codec)
        except BaseException as exc:  # terminal evidence is required even for a failed leaf
            failure = exc
        row = _attempt_row(sequence, leaf, manifest_sha256, previous, result, failure)
        raw = canonical_bytes(row)
        previous = hashlib.sha256(raw).hexdigest()
        chunks.append(raw)
        rows.append(row)
    if len(rows) != manifest["leaf_count"] or len({row["leaf_id"] for row in rows}) != len(rows):
        raise ControllerFailure("attempt/manifest cardinality mismatch")
    return b"".join(chunks), rows


def run() -> int:
    for path in WRITE_ALLOWLIST:
        if path.exists() or path.is_symlink():
            raise ControllerFailure(f"output must be absent before controller start: {path}")
    requirements = yaml.safe_load(REQUIREMENTS_PATH.read_bytes())
    execution_plan, _ = load_canonical_json(CONTROL_ROOT / "r3g07_execution_plan.json")
    _validate_execution_plan(execution_plan, requirements)
    manifest, manifest_raw = load_canonical_json(CONTROL_ROOT / "r3g07_test_manifest.json")
    attempts_raw, attempts = build_attempts_bytes(manifest, manifest_raw)

    # I17: exact terminal ledger only.
    _exclusive_write(ATTEMPTS_PATH, attempts_raw)

    # I18: independent verifier returns bytes; only this controller persists them.
    verifier = importlib.import_module("verify_r3g07_public_trust")
    evidence = verifier.build_verification_evidence(manifest, manifest_raw, attempts, attempts_raw)
    evidence_raw = canonical_bytes(evidence)
    _exclusive_write(EVIDENCE_PATH, evidence_raw)

    # I19 and I20: F11 is a pure byte builder; controller owns both writes.
    result_builder = importlib.import_module("build_r3g07_public_trust_result")
    aggregate_raw = result_builder.build_aggregate_bytes()
    _exclusive_write(AGGREGATE_PATH, aggregate_raw)
    report_raw = result_builder.build_report_bytes()
    _exclusive_write(REPORT_PATH, report_raw)
    aggregate, _ = load_canonical_json(AGGREGATE_PATH)
    return 0 if aggregate["overall_result"] == "PASS" else 1


def main() -> int:
    try:
        return run()
    except ControllerFailure as exc:
        print(f"BLOCKED_R3G07_CONTROLLER_INVALID: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
