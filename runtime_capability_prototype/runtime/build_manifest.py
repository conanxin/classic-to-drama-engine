from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "runtime"))

from ctde_runtime.common import dump_yaml  # noqa: E402


SUITE_ID = "RCPTS-20260811-002"


def group(
    requirement: str,
    suffixes: list[str],
    expected: str | dict[str, str],
    *,
    requires_grant: bool = True,
    bundle: str = "Z",
) -> list[dict[str, object]]:
    leaves: list[dict[str, object]] = []
    for suffix in suffixes:
        expected_value = expected[suffix] if isinstance(expected, dict) else expected
        leaves.append(
            {
                "requirement_group": requirement,
                "leaf_suffix": suffix,
                "scenario": f"{requirement}.{suffix}",
                "requires_grant": requires_grant,
                "expected_component_result": expected_value,
                "expected_case_result": "pass",
                "side_effect_bundle": bundle,
            }
        )
    return leaves


def materialize() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    rows += group("RCPT-T01-EXACT-RANGE", ["BASELINE"], "PASS_EXACT_RANGE", bundle="D")
    rows += group("RCPT-T02-AUTH-MISSING", ["MISSING"], "BLOCKED_TEST_AUTHORIZATION_MISSING", requires_grant=False)
    rows += group("RCPT-T03-AUTH-DIGEST", ["MISMATCH"], "BLOCKED_TEST_AUTHORIZATION_INVALID")
    rows += group("RCPT-T04-AUTH-EXPIRED", ["EXPIRED"], "BLOCKED_TEST_AUTHORIZATION_EXPIRED")
    rows += group("RCPT-T05-AUTH-REPLAY", ["CAS-REPLAY", "EVENT-REPLAY"], "BLOCKED_TEST_AUTHORIZATION_SPENT")
    rows += group("RCPT-T06-CAP-TAMPER", ["CLAIMS", "SIGNATURE"], "BLOCKED_RANGE_CAPABILITY_INVALID")
    rows += group("RCPT-T07-CAP-AUDIENCE", ["WRONG-BROKER"], "BLOCKED_RANGE_CAPABILITY_INVALID")
    rows += group(
        "RCPT-T08-RANGE-OVERRIDE",
        ["RAW-PATH", "SOURCE-PATH", "SOURCE-ID", "START", "END", "LENGTH", "EOF", "NEXT-RANGE", "RETRY"],
        "BLOCKED_RANGE_OVERRIDE_FORBIDDEN",
    )
    rows += group("RCPT-T09-RANGE-SHORT", ["ONE-BYTE"], "BLOCKED_TEST_SCOPE_CONTRACT_MISMATCH")
    rows += group("RCPT-T10-RANGE-LONG", ["ONE-BYTE"], "BLOCKED_TEST_SCOPE_CONTRACT_MISMATCH")
    rows += group("RCPT-T11-SLICE-HASH", ["MISMATCH"], "BLOCKED_SLICE_HASH_MISMATCH", bundle="B")
    rows += group("RCPT-T12-DELIVERY-REPLAY", ["REPLAY"], "BLOCKED_BOUNDED_READER_REPLAY", bundle="D")
    rows += group(
        "RCPT-T13-ENVELOPE-TAMPER",
        ["CLAIMS", "SIGNATURE", "BROKER-ATTESTATION-DIGEST"],
        "BLOCKED_BROKER_ENVELOPE_INVALID",
        bundle="B",
    )
    rows += group("RCPT-T14-FULL-PATH", ["OPEN"], "BLOCKED_SANDBOX_DIRECT_SOURCE_ACCESS", bundle="N")
    rows += group(
        "RCPT-T15-HANDLE-INVENTORY",
        ["INHERITED-FD-SANITIZED", "RESIDUAL-FD-DETECTED"],
        {
            "INHERITED-FD-SANITIZED": "PASS_INHERITED_FD_SANITIZED",
            "RESIDUAL-FD-DETECTED": "BLOCKED_SANDBOX_ISOLATION_UNPROVEN",
        },
        bundle="N",
    )
    rows += group(
        "RCPT-T16-GREEK-ID",
        ["AUTH-GREEK-ROLE", "CAP-GREEK-OBJECT", "AUTH-PRODUCTION-RAW", "CAP-PRODUCTION-SOURCE"],
        "BLOCKED_FORBIDDEN_SOURCE_ROLE",
    )
    rows += group("RCPT-T17-GREEK-PATH", ["HOST-PATH"], "BLOCKED_SANDBOX_DIRECT_SOURCE_ACCESS", bundle="N")
    rows += group("RCPT-T18-BOOK2-MARKER", ["PARSER", "GATEWAY"], "INVALIDATED_PROTOTYPE_SCOPE_EXCEEDED", bundle="D")
    rows += group(
        "RCPT-T19-WRITE-ESCAPE",
        ["FIXTURE-STORE", "WORKSPACE", "FORMAL-PATH", "UNALLOWLISTED-TEST-PATH"],
        "BLOCKED_TEST_WRITE_ISOLATION",
        bundle="N",
    )
    rows += group(
        "RCPT-T20-FORMAL-DISCOVERY",
        ["CANDIDATE-BARE", "CANDIDATE-PREFIXED", "CANDIDATE-NESTED", "PROTOTYPE-TREE"],
        "PASS_FORMAL_EXCLUDED",
        requires_grant=False,
        bundle="F",
    )
    rows += group(
        "RCPT-T21-RENAMED-COPY",
        ["SYMLINK", "HARDLINK", "RELATIVE-ESCAPE", "COPIED-OUTSIDE", "RENAMED-OUTSIDE", "MARKER-REMOVED", "FORGED-MANIFEST", "DIGEST-ONLY-CLONE"],
        "PASS_FORMAL_EXCLUDED",
        requires_grant=False,
        bundle="F",
    )
    rows += group(
        "RCPT-T22-AUDIT-MISSING",
        ["MISSING-BROKER", "MISSING-SANDBOX", "MISSING-PARSER", "MISSING-GATEWAY", "MISSING-WRITE", "MISSING-FORMAL", "LATE-MONITOR", "DROPPED-EVENT", "UNMONITORED-CHILD", "UNKNOWN-FIELD", "SELF-REPORT-ONLY", "ATTEMPT-MISMATCH", "AUTH-DIGEST-MISMATCH", "EVENT-MISMATCH", "CAPABILITY-MISMATCH", "DELIVERY-MISMATCH", "SCOPE-CLOSURE-LINK-MISMATCH"],
        "BLOCKED_SCOPE_PROOF_UNAVAILABLE",
        bundle="D",
    )
    rows += group("RCPT-T23-AUTH-CONCURRENT", ["DUAL-CAS-BARRIER"], "PASS_AUTH_CONCURRENT_SINGLE_WINNER")
    rows += group(
        "RCPT-T24-CAS-CRASH",
        ["AFTER-CAS-BEFORE-MINT", "RESTART-REISSUE-DENIED"],
        {
            "AFTER-CAS-BEFORE-MINT": "PASS_CAS_CRASH_SPENT_NO_MINT",
            "RESTART-REISSUE-DENIED": "BLOCKED_TEST_AUTHORIZATION_SPENT",
        },
    )
    rows += group(
        "RCPT-T25-AUDIT-TAMPER",
        ["REGISTRY-EVENT", "BROKER-EVENT", "COMPONENT-ATTESTATION", "SCOPE-ATTESTATION", "EVENT-REORDER", "OLD-EVIDENCE-REPLAY", "OLD-SCOPE-IN-CLOSURE"],
        "INVALIDATED_AUDIT_TAMPERED",
        bundle="D",
    )
    rows += group("RCPT-T26-FORMAL-POSITIVE", ["SIGNED-PROVENANCE"], "PASS_FORMAL_POSITIVE", requires_grant=False, bundle="F")
    rows += group("RCPT-T27-FORMAL-TOCTOU", ["OBJECT-SWAP", "DIGEST-MUTATE"], "PASS_FORMAL_TOCTOU_REJECTED", requires_grant=False, bundle="F")
    rows += group(
        "RCPT-T28-PARSER-UNSAFE",
        ["DTD", "INTERNAL-ENTITY", "EXTERNAL-FILE-ENTITY", "EXTERNAL-NETWORK-ENTITY", "RECOVERY", "BOOK2", "DUPLICATE-BOOK1", "WRONG-BOOK", "EXTRA-CARD", "MISSING-CARD", "EXTRA-PARAGRAPH", "MISSING-PARAGRAPH", "QNAME-NAMESPACE"],
        {
            "DTD": "BLOCKED_BOUNDED_FRAGMENT_UNPARSABLE",
            "INTERNAL-ENTITY": "BLOCKED_BOUNDED_FRAGMENT_UNPARSABLE",
            "EXTERNAL-FILE-ENTITY": "BLOCKED_BOUNDED_FRAGMENT_UNPARSABLE",
            "EXTERNAL-NETWORK-ENTITY": "BLOCKED_BOUNDED_FRAGMENT_UNPARSABLE",
            "RECOVERY": "BLOCKED_BOUNDED_FRAGMENT_UNPARSABLE",
            "BOOK2": "INVALIDATED_PROTOTYPE_SCOPE_EXCEEDED",
            "DUPLICATE-BOOK1": "INVALIDATED_PROTOTYPE_SCOPE_EXCEEDED",
            "WRONG-BOOK": "INVALIDATED_PROTOTYPE_SCOPE_EXCEEDED",
            "EXTRA-CARD": "BLOCKED_CARD_MAPPING_INVALID",
            "MISSING-CARD": "BLOCKED_CARD_MAPPING_INVALID",
            "EXTRA-PARAGRAPH": "BLOCKED_CARD_MAPPING_INVALID",
            "MISSING-PARAGRAPH": "BLOCKED_CARD_MAPPING_INVALID",
            "QNAME-NAMESPACE": "BLOCKED_CARD_MAPPING_INVALID",
        },
        bundle="D",
    )
    rows += group("RCPT-T29-BROKER-OBJECT-SWAP", ["IDENTITY-SWAP", "SAME-ID-CONTENT-MUTATION"], "BLOCKED_SOURCE_OBJECT_NOT_IMMUTABLE")
    rows += group("RCPT-T30-SECOND-CHANNEL", ["MMAP", "SENDFILE", "SPLICE", "COPY-FILE-RANGE", "IO-URING", "CHILD-ESCAPE"], "BLOCKED_SANDBOX_SECOND_CHANNEL", bundle="N")
    rows += group("RCPT-T31-BROKER-FALLBACK", ["FULL-HASH", "READ-TO-EOF", "MMAP", "SENDFILE", "SPLICE", "COPY-FILE-RANGE", "IO-URING", "AUTO-RETRY"], "BLOCKED_BROKER_FALLBACK_FORBIDDEN")
    rows += group("RCPT-T32-RANGE-ONLY-MISMATCH", ["BOOK2-DIRECT-RANGE"], "BLOCKED_TEST_SCOPE_CONTRACT_MISMATCH")

    targets = ["CAP", "ENV", "AUD-SCOPE", "AUD-CLOSURE"]
    rows += group("RCPT-T33-PROFILE-ALG", [f"{target}-{vector}" for target in targets for vector in ("ALG-NONE", "ALG-UNAPPROVED", "ALG-CONFUSION")], "BLOCKED_SIGNED_OBJECT_PROFILE_INVALID")
    rows += group("RCPT-T34-PROFILE-TYP", [f"{target}-{vector}" for target in targets for vector in ("TYP-MISSING", "TYP-WRONG", "VERSION-MISSING", "VERSION-WRONG")], "BLOCKED_SIGNED_OBJECT_PROFILE_INVALID")
    rows += group("RCPT-T35-PROFILE-KID", [f"{target}-{vector}" for target in targets for vector in ("KID-UNKNOWN", "KID-REVOKED", "KID-EXPIRED", "ISS-WRONG", "PROD-ROOT-IN-PROTO", "PROTO-ROOT-IN-PROD")], "BLOCKED_SIGNED_OBJECT_PROFILE_INVALID")
    rows += group(
        "RCPT-T36-PROFILE-AUD",
        ["CAP-AUD-MISSING", "CAP-AUD-WRONG", "ENV-AUD-MISSING", "ENV-AUD-WRONG", "SCOPE-AUD-MISSING", "SCOPE-AUD-WRONG-SET", "CLOSURE-AUD-MISSING", "CLOSURE-AUD-WRONG", "SCOPE-USING-CLOSURE-AUD", "CLOSURE-USING-SCOPE-AUD"],
        "BLOCKED_SIGNED_OBJECT_PROFILE_INVALID",
    )
    rows += group("RCPT-T37-PROFILE-TIME", [f"{target}-{vector}" for target in targets for vector in ("IAT-MISSING", "NBF-MISSING", "EXP-MISSING", "NBF-FUTURE", "EXP-PAST", "TTL-EXCEEDS")], "BLOCKED_SIGNED_OBJECT_PROFILE_INVALID")

    for index, row in enumerate(rows, 201):
        row["leaf_case_id"] = f"{row['requirement_group']}-{row['leaf_suffix']}"
        row["attempt_id"] = f"RCPT-20260811-{index:03d}"
        row["grant_id"] = f"GRANT-RCPT-20260811-{index:03d}" if row["requires_grant"] else None
    return rows


def main() -> None:
    leaves = materialize()
    requirement_groups = sorted({str(row["requirement_group"]) for row in leaves})
    assert len(requirement_groups) == 37
    assert len({str(row["leaf_case_id"]) for row in leaves}) == len(leaves)
    assert len({str(row["attempt_id"]) for row in leaves}) == len(leaves)
    grants = [str(row["grant_id"]) for row in leaves if row["grant_id"]]
    assert len(set(grants)) == len(grants)
    manifest = {
        "schema_version": "1.0.0",
        "artifact_class": "runtime_capability_test_manifest",
        "environment": "prototype_fixture_only",
        "suite_id": SUITE_ID,
        "namespace": "RCPT-*",
        "candidate_run_id": None,
        "candidate_run_authorized": False,
        "formal_phase_2_input": False,
        "frozen_before_attempts": True,
        "requirement_groups": requirement_groups,
        "leaf_cases": leaves,
        "count_authority": "enumerate leaf_cases at runtime",
    }
    target = ROOT / "suites" / SUITE_ID / "control" / "runtime_capability_test_manifest.yaml"
    dump_yaml(target, manifest, mode=0o444)


if __name__ == "__main__":
    main()
