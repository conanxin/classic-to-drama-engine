from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml


PROTOTYPE_ROOT = Path(__file__).resolve().parents[1]
WORKSPACE_ROOT = PROTOTYPE_ROOT.parent
REQUIREMENTS_PATH = PROTOTYPE_ROOT / "contracts" / "r3g07_public_trust_test_requirements.yaml"
FIXTURE_PATH = (
    PROTOTYPE_ROOT
    / "r3g07_portable_suites"
    / "R3G07PS-20260812-001"
    / "fixtures"
    / "r3g07_synthetic_fixtures.json"
)

FIXTURE_FIELDS = {
    "artifact_class", "schema_version", "suite_id", "assurance_profile_id", "synthetic_only",
    "source_content_allowed", "candidate_allowed", "model_calls_allowed", "business_outputs_allowed",
    "test_seed_path", "test_seed_sha256", "test_public_key_hex", "test_public_key_bytes_sha256",
    "formal_public_key_bytes_sha256", "recipes",
}
RECIPE_FIELDS = {
    "recipe_id", "requirement_group_id", "scenario", "expected_blocker", "side_effect_ceiling",
}


class _UniqueSafeLoader(yaml.SafeLoader):
    pass


def _unique_mapping(loader: yaml.Loader, node: yaml.MappingNode, deep: bool = False) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if type(key) is not str or key in result:
            raise ValueError("duplicate or non-string YAML key")
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


_UniqueSafeLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _unique_mapping)


def _sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")


def _load_requirements() -> dict[str, Any]:
    raw = REQUIREMENTS_PATH.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf") or b"\r" in raw or not raw.endswith(b"\n"):
        raise ValueError("requirements framing")
    value = yaml.load(raw.decode("utf-8"), Loader=_UniqueSafeLoader)
    if type(value) is not dict:
        raise ValueError("requirements object")
    return value


def _load_fixtures() -> tuple[dict[str, Any], bytes]:
    raw = FIXTURE_PATH.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf") or b"\r" in raw or not raw.endswith(b"\n") or raw.count(b"\n") != 1:
        raise ValueError("fixture framing")

    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"duplicate fixture key: {key}")
            result[key] = value
        return result

    fixtures = json.loads(raw.decode("utf-8"), object_pairs_hook=unique)
    if type(fixtures) is not dict or set(fixtures) != FIXTURE_FIELDS or raw != _canonical(fixtures) + b"\n":
        raise ValueError("fixture closed canonical contract")
    recipes = fixtures["recipes"]
    if type(recipes) is not list or not recipes or any(type(item) is not dict or set(item) != RECIPE_FIELDS for item in recipes):
        raise ValueError("fixture recipe closed contract")
    recipe_ids = [item["recipe_id"] for item in recipes]
    recipe_pairs = [(item["requirement_group_id"], item["scenario"]) for item in recipes]
    if len(recipe_ids) != len(set(recipe_ids)) or len(recipe_pairs) != len(set(recipe_pairs)):
        raise ValueError("duplicate fixture recipe identity")
    return fixtures, raw


def _input_paths(requirements: dict[str, Any]) -> list[dict[str, str]]:
    items = [
        ("runtime_capability_prototype/contracts/public_trust_material_schema_v1.yaml", "runtime_contract"),
        ("runtime_capability_prototype/contracts/public_key_status_registry_schema_v1.yaml", "runtime_contract"),
        ("runtime_capability_prototype/contracts/portable_public_trust_material_v1.json", "runtime_asset"),
        ("runtime_capability_prototype/contracts/portable_public_key_status_registry_v1.json", "runtime_asset"),
        ("runtime_capability_prototype/runtime/ctde_runtime/public_trust.py", "runtime_implementation"),
        ("runtime_capability_prototype/contracts/r3g07_public_trust_test_requirements.yaml", "test_contract"),
        ("runtime_capability_prototype/contracts/r3g07_public_trust_test_manifest_schema_v1.yaml", "test_contract"),
        (
            "runtime_capability_prototype/r3g07_portable_suites/R3G07PS-20260812-001/fixtures/r3g07_synthetic_fixtures.json",
            "test_fixture",
        ),
        (
            "runtime_capability_prototype/r3g07_portable_suites/R3G07PS-20260812-001/fixtures/r3g07_test_signing_key_ed25519_seed.hex",
            "test_secret",
        ),
    ]
    result = [
        {"path": path, "sha256": _sha256_file(WORKSPACE_ROOT / path), "classification": classification}
        for path, classification in items
    ]
    for caller in requirements["callers"]:
        path = caller["path"]
        actual = _sha256_file(WORKSPACE_ROOT / path)
        if actual != caller["file_sha256"]:
            raise ValueError(f"caller digest mismatch: {caller['caller_id']}")
        result.append(
            {
                "path": f"{path}::{caller['callable']}",
                "sha256": actual,
                "classification": "caller",
            }
        )
    return result


def build_manifest() -> dict[str, Any]:
    requirements = _load_requirements()
    fixtures, fixtures_raw = _load_fixtures()
    required_pairs_list = [
        (group["requirement_group_id"], scenario)
        for group in requirements["requirement_groups"]
        for scenario in group["scenarios"]
    ]
    recipe_pairs_list = [(recipe["requirement_group_id"], recipe["scenario"]) for recipe in fixtures["recipes"]]
    if len(required_pairs_list) != len(set(required_pairs_list)) or required_pairs_list != recipe_pairs_list:
        raise ValueError("fixture/requirements scenario mismatch")
    input_digests = _input_paths(requirements)
    input_set_sha = hashlib.sha256(_canonical(input_digests) + b"\n").hexdigest()
    expansions = requirements.get("caller_expansions", {})
    leaves: list[dict[str, Any]] = []
    ordinal = 0
    for recipe in fixtures["recipes"]:
        caller_ids = expansions.get(recipe["scenario"], [None])
        if not caller_ids:
            raise ValueError(f"empty expansion: {recipe['scenario']}")
        for caller_id in caller_ids:
            ordinal += 1
            scenario_slug = re.sub(r"[^A-Z0-9]+", "-", recipe["scenario"].upper()).strip("-")
            caller_suffix = f"-{caller_id}" if caller_id is not None else ""
            leaf_id = f"R3G07-{ordinal:03d}-{scenario_slug}{caller_suffix}"
            identity_payload = {
                "caller_id": caller_id,
                "fixture_catalog_sha256": hashlib.sha256(fixtures_raw).hexdigest(),
                "input_set_sha256": input_set_sha,
                "leaf_id": leaf_id,
                "requirement_group_id": recipe["requirement_group_id"],
                "requirements_sha256": _sha256_file(REQUIREMENTS_PATH),
                "scenario": recipe["scenario"],
            }
            leaves.append(
                {
                    "leaf_id": leaf_id,
                    "requirement_group_id": recipe["requirement_group_id"],
                    "scenario": recipe["scenario"],
                    "caller_id": caller_id,
                    "input_identity_sha256": hashlib.sha256(_canonical(identity_payload) + b"\n").hexdigest(),
                    "expected_result": "PASS",
                    "expected_blocker": recipe["expected_blocker"],
                    "side_effect_ceiling": recipe["side_effect_ceiling"],
                }
            )
    leaf_ids = [leaf["leaf_id"] for leaf in leaves]
    if len(leaf_ids) != len(set(leaf_ids)):
        raise ValueError("duplicate leaf identity")
    manifest = {
        "artifact_class": "ctde_r3g07_public_trust_test_manifest",
        "schema_version": "1.0.0",
        "suite_id": requirements["suite_id"],
        "assurance_profile_id": requirements["assurance_profile_id"],
        "highest_claimed_evidence_level": requirements["highest_claimed_evidence_level"],
        "synthetic_only": True,
        "requirements_sha256": _sha256_file(REQUIREMENTS_PATH),
        "fixture_catalog_sha256": hashlib.sha256(fixtures_raw).hexdigest(),
        "input_digests": input_digests,
        "leaf_count": len(leaves),
        "leaves": leaves,
    }
    return manifest


def build_manifest_bytes() -> bytes:
    return _canonical(build_manifest()) + b"\n"


def main() -> int:
    sys.stdout.buffer.write(build_manifest_bytes())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
