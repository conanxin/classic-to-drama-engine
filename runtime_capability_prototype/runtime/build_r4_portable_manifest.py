from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any

import yaml


PROTOTYPE_ROOT = Path(__file__).resolve().parents[1]
WORKSPACE_ROOT = PROTOTYPE_ROOT.parent
CONTRACT_ROOT = PROTOTYPE_ROOT / "contracts"
POLICY_PATH = CONTRACT_ROOT / "r4_portable_e2e_policy_v1.yaml"
REQUIREMENTS_PATH = CONTRACT_ROOT / "r4_portable_test_requirements_v1.yaml"
SCHEMA_PATH = CONTRACT_ROOT / "r4_portable_test_manifest_schema_v1.yaml"
LEGACY_MANIFEST_PATH = PROTOTYPE_ROOT / "suites" / "RCPTS-20260811-002" / "control" / "runtime_capability_test_manifest.yaml"
SUITE_ID = "R4PS-20260815-002"
PREDECESSOR_SUITE_ID = "R4PS-20260815-001"
PHASE_ID = "Phase 2-G-R4FRESH-E2"
PLAN_SHA256 = "c1ddff51020880c22787f75722166656647ac18a0a8dd6b21c8af1d3ade24fb8"
AUDIT_SHA256 = "210f5c1e4e205b1e17e731cb87180d72680d576f97a96e746d8f9fc82fde5b6a"
GATE_B_WRITE_SCOPE_SHA256 = "db661411179360060acec24dd540fdbb29099b68551fb48bd1379ead5c3668ed"
FULL_RECIPE_ID = "CTDE-R4-SYNTHETIC-BOOK1-1"
GREEK_RECIPE_ID = "CTDE-R4-SYNTHETIC-GREEK-DENY-1"
FULL_SIZE = 40960
START = 4076
END = 36515
LENGTH = END - START
BOOK_MARKER = b'<BOOK_01 xmlns="urn:ctde:synthetic">'


class ManifestBuildFailure(RuntimeError):
    pass


class _UniqueSafeLoader(yaml.SafeLoader):
    pass


def _unique_mapping(loader: yaml.Loader, node: yaml.MappingNode, deep: bool = False) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if type(key) is not str or key in result:
            raise ManifestBuildFailure("duplicate or non-string YAML key")
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


_UniqueSafeLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _unique_mapping)


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8") + b"\n"


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def synthetic_book1_object_id(full_raw: bytes) -> str:
    return f"urn:ctde:fixture:{sha256_bytes(full_raw)}"


def synthetic_greek_object_id(greek_raw: bytes) -> str:
    return f"urn:ctde:fixture-greek-deny:{sha256_bytes(greek_raw)}"


def load_yaml(path: Path) -> dict[str, Any]:
    raw = path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf") or b"\r" in raw or not raw.endswith(b"\n"):
        raise ManifestBuildFailure(f"invalid YAML framing: {path}")
    value = yaml.load(raw.decode("utf-8"), Loader=_UniqueSafeLoader)
    if type(value) is not dict:
        raise ManifestBuildFailure(f"YAML object required: {path}")
    return value


def _stable(prefix: str, value: str, length: int = 24) -> str:
    return f"{prefix}-{hashlib.sha256(value.encode('utf-8')).hexdigest()[:length]}"


def _deterministic_bytes(domain: str, size: int) -> bytes:
    return hashlib.shake_256(("ctde-r4:" + domain).encode("ascii")).digest(size)


def _structural_payload(variant: str) -> bytes:
    preamble = b""
    book_open = b'<BOOK_01 xmlns="urn:ctde:synthetic">'
    book_close = b"</BOOK_01>"
    trailer = b""
    card_count = 10
    paragraph_count = 10
    if variant == "dtd":
        preamble = b"<!DOCTYPE BOOK_01 []>"
    elif variant == "external_entity":
        preamble = b'<!DOCTYPE BOOK_01 [<!ENTITY x SYSTEM "file:///etc/passwd">]>'
        trailer = b"&x;"
    elif variant == "book2":
        trailer = b"<BOOK_02/>"
    elif variant == "wrong_namespace":
        book_open = b'<BOOK_01 xmlns="urn:ctde:wrong">'
    elif variant == "missing_card":
        card_count = 9
        paragraph_count = 9
    elif variant == "extra_card":
        card_count = 11
        paragraph_count = 11
    elif variant != "baseline":
        raise ManifestBuildFailure(f"unsupported synthetic fixture variant: {variant}")
    structural = [preamble, book_open]
    for index in range(1, card_count + 1):
        structural.append(f"<CARD_{index:02d}>".encode("ascii"))
        if index <= paragraph_count:
            structural.append(f"<PARA_{index:02d}/>".encode("ascii"))
        structural.append(f"</CARD_{index:02d}>".encode("ascii"))
    structural.extend([trailer, book_close])
    return b"".join(structural)


def build_synthetic_fixture_variant(variant: str = "baseline") -> bytes:
    full = bytearray(_deterministic_bytes("full-object", FULL_SIZE))
    slice_bytes = bytearray(_deterministic_bytes("authorized-book1-slice:" + variant, LENGTH))
    payload = _structural_payload(variant)
    if len(payload) >= LENGTH:
        raise ManifestBuildFailure("synthetic structure exceeds authorized range")
    slice_bytes[: len(payload)] = payload
    full[START:END] = slice_bytes
    prefix_sentinel = b"CTDE_R4_PREFIX_SENTINEL"
    book2_sentinel = b"CTDE_R4_SYNTHETIC_BOOK_02_SENTINEL"
    full[64 : 64 + len(prefix_sentinel)] = prefix_sentinel
    full[38000 : 38000 + len(book2_sentinel)] = book2_sentinel
    return bytes(full)


def build_synthetic_fixtures() -> tuple[bytes, bytes, dict[str, Any]]:
    full_raw = build_synthetic_fixture_variant("baseline")
    greek = bytearray(_deterministic_bytes("greek-deny-object", 4096))
    greek_marker = b"CTDE_R4_SYNTHETIC_GREEK_DENY_SENTINEL"
    greek[: len(greek_marker)] = greek_marker
    greek_raw = bytes(greek)
    if len(full_raw) <= END or len(full_raw[START:END]) != LENGTH or not greek_raw:
        raise ManifestBuildFailure("synthetic fixture boundary")
    allowed = full_raw[START:END]
    if allowed.count(BOOK_MARKER) != 1:
        raise ManifestBuildFailure("synthetic Book marker identity")
    marker_offsets: dict[str, int] = {"BOOK_01": allowed.index(BOOK_MARKER) + START}
    for index in range(1, 11):
        marker_offsets[f"CARD_{index:02d}"] = allowed.index(f"<CARD_{index:02d}>".encode()) + START
        marker_offsets[f"PARAGRAPH_{index:02d}"] = allowed.index(f"<PARA_{index:02d}/>".encode()) + START
    catalog = {
        "artifact_class": "ctde_r4_synthetic_fixture_catalog",
        "schema_version": "1.0.0",
        "suite_id": SUITE_ID,
        "synthetic_only": True,
        "source_content_inputs": 0,
        "fixtures": [
            {
                "recipe_id": FULL_RECIPE_ID,
                "object_id": synthetic_book1_object_id(full_raw),
                "sha256": sha256_bytes(full_raw),
                "bytes": len(full_raw),
                "allowed_range": [START, END],
                "allowed_length": LENGTH,
                "allowed_slice_sha256": sha256_bytes(allowed),
                "marker_offsets": marker_offsets,
                "book2_sentinel_offset": 38000,
            },
            {
                "recipe_id": GREEK_RECIPE_ID,
                "object_id": synthetic_greek_object_id(greek_raw),
                "sha256": sha256_bytes(greek_raw),
                "bytes": len(greek_raw),
                "authorization_allowed": False,
            },
        ],
    }
    return full_raw, greek_raw, catalog


def _component_subject(group_id: str) -> str:
    match = re.fullmatch(r"RCPT-T([0-9]{2})-[A-Z0-9-]+", group_id)
    if match is None:
        raise ManifestBuildFailure(f"invalid requirement group identity: {group_id}")
    number = int(match.group(1))
    if not 1 <= number <= 37:
        raise ManifestBuildFailure(f"requirement group out of range: {group_id}")
    if number <= 5 or number in {23, 24}:
        return "authorization_registry_v2"
    if number in {6, 7, 8, 9, 10, 11, 29, 31, 32, 33, 34, 35, 36, 37}:
        return "range_broker_and_signed_profiles"
    if number in {12, 13, 14, 15, 30}:
        return "bounded_reader_delivery"
    if number in {16, 17, 18, 28}:
        return "embedded_parser_scope_and_discard_gateway"
    if number in {19}:
        return "portable_logical_write_monitor"
    if number in {20, 21, 26, 27}:
        return "formal_loader"
    return "portable_a1_audit_chain"


def _authorization_required(group_id: str) -> bool:
    return group_id not in {"RCPT-T02-AUTH-MISSING", "RCPT-T20-FORMAL-DISCOVERY", "RCPT-T21-RENAMED-COPY"}


def _validate_prefix(prefix: dict[str, str]) -> None:
    required = {
        "plan_sha256": PLAN_SHA256,
        "audit_sha256": AUDIT_SHA256,
        "gate_b_write_scope_sha256": GATE_B_WRITE_SCOPE_SHA256,
        "suite_id": SUITE_ID,
    }
    for key, expected in required.items():
        if prefix.get(key) != expected:
            raise ManifestBuildFailure(f"prefix mismatch: {key}")
    for key in (
        "implementation_manifest_sha256",
        "preexecution_closure_manifest_sha256",
        "preexecution_closure_payload_sha256",
        "preexecution_component_freeze_sha256",
        "preexecution_closure_registry_record_sha256",
    ):
        value = prefix.get(key)
        if type(value) is not str or len(value) != 64 or any(character not in "0123456789abcdef" for character in value):
            raise ManifestBuildFailure(f"invalid prefix digest: {key}")


def build_manifest(prefix: dict[str, str]) -> tuple[dict[str, Any], bytes, bytes, dict[str, Any]]:
    _validate_prefix(prefix)
    policy = load_yaml(POLICY_PATH)
    requirements = load_yaml(REQUIREMENTS_PATH)
    schema = load_yaml(SCHEMA_PATH)
    legacy = load_yaml(LEGACY_MANIFEST_PATH)
    if policy.get("suite_id") != PREDECESSOR_SUITE_ID or requirements.get("suite_id") != PREDECESSOR_SUITE_ID:
        raise ManifestBuildFailure("suite identity mismatch")
    if schema.get("requirement_group_count") != 37:
        raise ManifestBuildFailure("manifest schema group count")
    full_raw, greek_raw, catalog = build_synthetic_fixtures()
    leaves: list[dict[str, Any]] = []
    groups: list[str] = []
    legacy_by_group: dict[str, list[dict[str, Any]]] = {}
    for legacy_leaf in legacy.get("leaf_cases", []):
        legacy_by_group.setdefault(legacy_leaf["requirement_group"], []).append(legacy_leaf)
    ordinal = 0
    for requirement in requirements.get("requirements", []):
        group_id = requirement.get("group_id")
        cases = requirement.get("cases")
        if type(group_id) is not str or type(cases) is not list or not cases or group_id in groups:
            raise ManifestBuildFailure("invalid requirement inventory")
        groups.append(group_id)
        templates = legacy_by_group.get(group_id, [])
        if not templates:
            raise ManifestBuildFailure(f"historical regression vector absent: {group_id}")
        for case_index, expansion_case in enumerate(cases):
            if type(expansion_case) is not str:
                raise ManifestBuildFailure("invalid scenario")
            template = templates[case_index % len(templates)]
            scenario = template["scenario"]
            ordinal += 1
            identity = f"{SUITE_ID}:{group_id}:{expansion_case}:{scenario}:{ordinal}"
            attempt_id = _stable("RCPT-R4", identity)
            authorization_id = _stable("R4AUTH", identity) if template["requires_grant"] else None
            leaves.append(
                {
                    "leaf_id": f"R4-{ordinal:03d}-{group_id}-{expansion_case.upper().replace('_', '-')}",
                    "group_id": group_id,
                    "scenario": scenario,
                    "attempt_id": attempt_id,
                    "authorization_id": authorization_id,
                    "fixture_recipe_id": FULL_RECIPE_ID,
                    "component_subject": _component_subject(group_id),
                    "expected_terminal": template["expected_component_result"],
                    "side_effect_ceiling": {
                        "model_calls": 0,
                        "candidate_runs": 0,
                        "business_outputs": 0,
                        "source_content_reads": 0,
                        "delivery_count": 1 if group_id == "RCPT-T01-EXACT-RANGE" else 0,
                    },
                    "evidence_locator": f"evidence/case_results.jsonl#{ordinal}",
                    "no_retry": True,
                }
            )
    if len(groups) != 37 or len(set(groups)) != 37:
        raise ManifestBuildFailure("closed group coverage")
    attempts = [leaf["attempt_id"] for leaf in leaves]
    authorizations = [leaf["authorization_id"] for leaf in leaves if leaf["authorization_id"]]
    if len(attempts) != len(set(attempts)) or len(authorizations) != len(set(authorizations)):
        raise ManifestBuildFailure("fresh identity collision")
    manifest = {
        "artifact_class": "ctde_r4_portable_test_manifest",
        "schema_version": "1.0.0",
        "canonicalization_id": "CTDE-CANONICAL-JSON-SORTED-COMPACT-LF-1",
        "suite_id": SUITE_ID,
        "phase_id": PHASE_ID,
        "assurance": {
            "profile_id": "CTDE-PORTABLE-DEV-1",
            "highest_claimed_evidence_level": "A1",
            "certified": False,
            "hardened": False,
            "candidate_ready": False,
        },
        "identities": {
            **dict(sorted(prefix.items())),
            "policy_sha256": sha256_file(POLICY_PATH),
            "requirements_sha256": sha256_file(REQUIREMENTS_PATH),
            "manifest_schema_sha256": sha256_file(SCHEMA_PATH),
            "historical_regression_manifest_sha256": sha256_file(LEGACY_MANIFEST_PATH),
        },
        "fixture_recipes": catalog["fixtures"],
        "requirement_groups": groups,
        "leaves": leaves,
        "action_ledger": {
            "model_calls": 0,
            "candidate_runs": 0,
            "business_outputs": 0,
            "english_tei_content_reads": 0,
            "greek_tei_content_reads": 0,
        },
    }
    return manifest, full_raw, greek_raw, catalog


def build_manifest_bytes(prefix: dict[str, str]) -> tuple[bytes, bytes, bytes, bytes]:
    manifest, full_raw, greek_raw, catalog = build_manifest(prefix)
    return canonical_bytes(manifest), full_raw, greek_raw, canonical_bytes(catalog)


def main() -> int:
    parser = argparse.ArgumentParser(description="R4 builder returns bytes and never persists project output")
    parser.add_argument("--prefix-json", required=True)
    parser.add_argument("--dry-run-manifest", action="store_true")
    args = parser.parse_args()
    try:
        prefix = json.loads(Path(args.prefix_json).read_text(encoding="utf-8"))
        manifest_raw, _, _, _ = build_manifest_bytes(prefix)
        if not args.dry_run_manifest:
            raise ManifestBuildFailure("explicit dry-run flag required")
        import sys
        sys.stdout.buffer.write(manifest_raw)
        return 0
    except Exception as exc:
        import sys
        print(f"BLOCKED_R4_MANIFEST_BUILD: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
