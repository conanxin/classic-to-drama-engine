from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any, Iterable


SUITE_ID = "R4PS-20260815-001"
PASS_STATUS = "PASS_PORTABLE_RUNTIME_SYNTHETIC_E2E"
BLOCKED_STATUS = "BLOCKED_PORTABLE_RUNTIME_SYNTHETIC_E2E"


class ResultBuildFailure(RuntimeError):
    pass


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8") + b"\n"


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def load_canonical_json(path: Path) -> tuple[dict[str, Any], bytes]:
    raw = path.read_bytes()
    value = json.loads(raw.decode("utf-8"))
    if type(value) is not dict or raw != canonical_bytes(value):
        raise ResultBuildFailure(f"noncanonical JSON: {path}")
    return value, raw


def load_canonical_jsonl(path: Path) -> tuple[list[dict[str, Any]], bytes]:
    raw = path.read_bytes()
    if not raw or not raw.endswith(b"\n") or b"\r" in raw:
        raise ResultBuildFailure(f"invalid JSONL framing: {path}")
    records: list[dict[str, Any]] = []
    for line in raw.splitlines(keepends=True):
        value = json.loads(line.decode("utf-8"))
        if type(value) is not dict or line != canonical_bytes(value):
            raise ResultBuildFailure(f"noncanonical JSONL record: {path}")
        records.append(value)
    return records, raw


def _sum_field(records: Iterable[dict[str, Any]], key: str) -> int:
    total = 0
    for record in records:
        value = record.get(key, 0)
        if type(value) is not int or value < 0:
            raise ResultBuildFailure(f"invalid action count: {key}")
        total += value
    return total


def build_aggregate(
    *,
    manifest: dict[str, Any],
    manifest_raw: bytes,
    case_results: list[dict[str, Any]],
    case_results_raw: bytes,
    logical_write_events: list[dict[str, Any]],
    logical_write_events_raw: bytes,
    evidence_manifest: dict[str, Any],
    evidence_manifest_raw: bytes,
) -> dict[str, Any]:
    if manifest.get("suite_id") != SUITE_ID or evidence_manifest.get("suite_id") != SUITE_ID:
        raise ResultBuildFailure("suite identity")
    leaves = manifest.get("leaves")
    groups = manifest.get("requirement_groups")
    if type(leaves) is not list or type(groups) is not list or len(groups) != 37:
        raise ResultBuildFailure("manifest inventory")
    leaf_ids = [leaf.get("leaf_id") for leaf in leaves]
    result_ids = [record.get("leaf_id") for record in case_results]
    if leaf_ids != result_ids:
        raise ResultBuildFailure("case result order or coverage")
    attempts = [leaf.get("attempt_id") for leaf in leaves]
    authorizations = [leaf.get("authorization_id") for leaf in leaves if leaf.get("authorization_id") is not None]
    duplicate_attempt_ids = len(attempts) - len(set(attempts))
    cross_case_reuse = len(authorizations) - len(set(authorizations))
    dispositions = [record.get("disposition") for record in case_results]
    passed = sum(value == "pass" for value in dispositions)
    failed = sum(value == "fail" for value in dispositions)
    unknown = sum(value == "unknown" for value in dispositions)
    timeout = sum(value == "timeout" for value in dispositions)
    skipped = len(leaves) - len(case_results)
    evidence_complete = sum(record.get("evidence_complete") is True for record in case_results)
    group_results = {
        group: {
            "leaf_count": sum(record.get("group_id") == group for record in case_results),
            "passed": all(record.get("disposition") == "pass" for record in case_results if record.get("group_id") == group),
        }
        for group in groups
    }
    action_records = [record.get("side_effect_counts", {}) for record in case_results]
    action_ledger = {
        "model_calls": _sum_field(action_records, "model_calls"),
        "candidate_runs": _sum_field(action_records, "candidate_runs"),
        "business_outputs": _sum_field(action_records, "business_outputs"),
        "english_tei_content_reads": _sum_field(action_records, "english_tei_content_reads"),
        "greek_tei_content_reads": _sum_field(action_records, "greek_tei_content_reads"),
    }
    denied_writes = sum(event.get("allowed") is False for event in logical_write_events)
    allowed_writes = sum(event.get("allowed") is True for event in logical_write_events)
    closure = evidence_manifest.get("closure", {})
    pass_conditions = [
        failed == skipped == unknown == timeout == 0,
        passed == evidence_complete == len(leaves),
        duplicate_attempt_ids == cross_case_reuse == 0,
        all(item["passed"] and item["leaf_count"] > 0 for item in group_results.values()),
        closure.get("closure_delta_count") == 0,
        closure.get("unknown_project_owned_loaded_bytes") == 0,
        all(value == 0 for value in action_ledger.values()),
        denied_writes > 0,
        evidence_manifest.get("evidence_complete") is True,
    ]
    status = PASS_STATUS if all(pass_conditions) else BLOCKED_STATUS
    positive = [record for record in case_results if record.get("group_id") == "RCPT-T01-EXACT-RANGE"]
    return {
        "artifact_class": "ctde_r4_portable_results",
        "schema_version": "1.0.0",
        "suite_id": SUITE_ID,
        "status": status,
        "identities": {
            "test_manifest_sha256": sha256_bytes(manifest_raw),
            "case_results_sha256": sha256_bytes(case_results_raw),
            "logical_write_events_sha256": sha256_bytes(logical_write_events_raw),
            "evidence_manifest_sha256": sha256_bytes(evidence_manifest_raw),
            **dict(sorted(evidence_manifest.get("gate_a_identities", {}).items())),
        },
        "assurance": {
            "profile_id": "CTDE-PORTABLE-DEV-1",
            "highest_claimed_evidence_level": "A1",
            "historical_a3_prototype_status": "NOT_CLAIMED",
            "r1_requalification_status": "NOT_REQUIRED_FOR_PORTABLE_A1",
            "real_source_zero_access_a2": "not_claimed_under_portable_a1",
            "candidate_ready": False,
            "candidate_execution_authorized": False,
        },
        "counts": {
            "requirement_groups": len(groups),
            "manifest_leaves": len(leaves),
            "discovered": len(case_results),
            "executed": len(case_results),
            "evidence_complete": evidence_complete,
            "passed": passed,
            "failed": failed,
            "skipped": skipped,
            "unknown": unknown,
            "timeout": timeout,
            "duplicate_attempt_ids": duplicate_attempt_ids,
            "cross_case_authorization_reuse": cross_case_reuse,
        },
        "group_results": group_results,
        "positive_path": positive,
        "negative_coverage": {"denied_leaf_count": sum(record.get("blocker") is not None for record in case_results), "exact_blockers_persisted": all(record.get("blocker") or record.get("group_id") in {"RCPT-T01-EXACT-RANGE", "RCPT-T26-FORMAL-POSITIVE"} for record in case_results)},
        "closure": closure,
        "logical_writes": {"allowed_events": allowed_writes, "denied_events": denied_writes, "syscall_complete_claimed": False},
        "action_ledger": action_ledger,
        "evidence": {"complete": evidence_manifest.get("evidence_complete") is True, "artifact_count": evidence_manifest.get("artifact_count")},
    }


def build_aggregate_bytes(**kwargs: Any) -> bytes:
    return canonical_bytes(build_aggregate(**kwargs))


def build_report_bytes(aggregate: dict[str, Any]) -> bytes:
    counts = aggregate["counts"]
    lines = [
        "# Portable Runtime Synthetic E2E Result",
        "",
        f"Status: `{aggregate['status']}`",
        "",
        f"- Suite: `{aggregate['suite_id']}`",
        f"- Assurance: `CTDE-PORTABLE-DEV-1 / A1`",
        f"- Requirement groups: `{counts['requirement_groups']}`",
        f"- Leaves discovered/executed/evidence-complete/passed: `{counts['discovered']}/{counts['executed']}/{counts['evidence_complete']}/{counts['passed']}`",
        f"- Failed/skipped/unknown/timeout: `{counts['failed']}/{counts['skipped']}/{counts['unknown']}/{counts['timeout']}`",
        f"- Model calls: `{aggregate['action_ledger']['model_calls']}`",
        f"- Candidate runs: `{aggregate['action_ledger']['candidate_runs']}`",
        f"- Business outputs: `{aggregate['action_ledger']['business_outputs']}`",
        "",
        "This Portable A1 result does not claim R1, A2, A3, production certification, or Candidate authorization.",
        "",
    ]
    return "\n".join(lines).encode("utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="R4 aggregate/report byte producer")
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--case-results", required=True)
    parser.add_argument("--logical-write-events", required=True)
    parser.add_argument("--evidence-manifest", required=True)
    parser.add_argument("--output", choices=("aggregate", "report"), required=True)
    args = parser.parse_args()
    try:
        manifest, manifest_raw = load_canonical_json(Path(args.manifest))
        cases, cases_raw = load_canonical_jsonl(Path(args.case_results))
        writes, writes_raw = load_canonical_jsonl(Path(args.logical_write_events))
        evidence, evidence_raw = load_canonical_json(Path(args.evidence_manifest))
        aggregate = build_aggregate(manifest=manifest, manifest_raw=manifest_raw, case_results=cases, case_results_raw=cases_raw, logical_write_events=writes, logical_write_events_raw=writes_raw, evidence_manifest=evidence, evidence_manifest_raw=evidence_raw)
        sys.stdout.buffer.write(canonical_bytes(aggregate) if args.output == "aggregate" else build_report_bytes(aggregate))
        return 0
    except Exception as exc:
        print(f"BLOCKED_PORTABLE_RUNTIME_SYNTHETIC_E2E: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
