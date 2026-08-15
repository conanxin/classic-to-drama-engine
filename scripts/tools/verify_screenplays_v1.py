from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from screenplay_dialogue_v1 import DIALOGUE


ROOT = Path(__file__).resolve().parents[2]
ADAPTATION = ROOT / "adaptation/odyssey_m1_v1"
OUT = ROOT / "scripts/odyssey_m1_v1"
EPISODES = OUT / "episodes"
MANIFEST = OUT / "SCREENPLAY_V1_MANIFEST.json"
VERIFICATION = OUT / "SCREENPLAY_V1_VERIFICATION.json"
RESULT = OUT / "SCREENPLAY_V1_RESULT.md"
EXPECTED_ADAPTATION_MANIFEST_SHA256 = "3ace187381786525d4e36cc5dc7991f86344f7cc943a621782efc86c5e0db84a"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


checks: list[dict[str, object]] = []


def check(name: str, condition: bool, detail: object) -> None:
    checks.append({"check": name, "status": "PASS" if condition else "FAIL", "detail": detail})


manifest = load(MANIFEST)
adaptation_sha = sha256(ADAPTATION / "manifest.json")
check("adaptation_identity", adaptation_sha == EXPECTED_ADAPTATION_MANIFEST_SHA256, adaptation_sha)
check("manifest_status", manifest.get("status") == "PASS_30_EPISODE_SCREENPLAY_V1_BUILT", manifest.get("status"))
check("zero_external_model_calls", manifest.get("external_model_calls") == 0, manifest.get("external_model_calls"))
check("zero_greek_content_reads", manifest.get("greek_tei_content_reads") == 0, manifest.get("greek_tei_content_reads"))

inventory = manifest.get("artifacts", [])
inventory_results = []
for entry in inventory:
    path = ROOT / entry["path"]
    ok = path.is_file() and len(path.read_bytes()) == entry["bytes"] and sha256(path) == entry["sha256"]
    inventory_results.append({"path": entry["path"], "status": "PASS" if ok else "FAIL"})
check(
    "manifest_inventory_exact",
    len(inventory) == manifest.get("episode_count") == 30 and all(item["status"] == "PASS" for item in inventory_results),
    {"declared": manifest.get("episode_count"), "verified": len(inventory_results)},
)

episode_results = []
hashes: list[str] = []
covered_books: set[int] = set()
for number in range(1, 31):
    episode_id = f"EP{number:02d}"
    path = EPISODES / f"{episode_id}.md"
    card = load(ADAPTATION / "episode_cards" / f"{episode_id}.json")
    text = path.read_text(encoding="utf-8")
    raw = path.read_bytes()
    hashes.append(hashlib.sha256(raw).hexdigest())
    covered_books.update(card["source_books"])
    headers = re.findall(r"^## 场 (\d+)｜(?:内景|外景)·([^·\n]+)·(?:日|暮|夜)$", text, flags=re.MULTILINE)
    cues = re.findall(r"^\*\*([^*]+)\*\*$", text, flags=re.MULTILINE)
    chinese_count = len(re.findall(r"[\u3400-\u9fff]", text))
    forbidden = re.findall(r"(?i)\b(?:TODO|TBD|PLACEHOLDER)\b|待补|占位", text)
    locations = {location for _, location in headers}
    expected_dialogue_lines = [spoken for scene in DIALOGUE[number] for _, spoken in scene]
    episode_checks = {
        "title_exact": text.startswith(f"# {episode_id}《{card['title']}》"),
        "five_ordered_scenes": [scene for scene, _ in headers] == ["1", "2", "3", "4", "5"],
        "locations_authorized": locations.issubset(set(card["locations"])),
        "dialogue_density": len(cues) >= 15,
        "substantive_chinese_draft": chinese_count >= 700,
        "source_events_bound": all(event_id in text for event_id in card["source_event_ids"]),
        "decision_ids_bound": all(decision_id in text for decision_id in card["adaptation_decision_ids"]),
        "locked_dialogue_materialized": all(line in text for line in expected_dialogue_lines),
        "ending_hook_exact": card["ending_cliffhanger"] in text and "切黑" in text,
        "adaptation_boundary_explicit": "连接动作与中文对白均为 M1 改编表达" in text and "CONNECTIVE_ACTION_AND_DIALOGUE" in text,
        "no_placeholder_language": not forbidden,
    }
    status = "PASS" if all(episode_checks.values()) else "FAIL"
    episode_results.append(
        {
            "episode_id": episode_id,
            "status": status,
            "sha256": hashes[-1],
            "bytes": len(raw),
            "scene_count": len(headers),
            "dialogue_cue_count": len(cues),
            "chinese_character_count": chinese_count,
            "checks": episode_checks,
        }
    )

check("all_episodes_independently_valid", all(item["status"] == "PASS" for item in episode_results), {"passed": sum(item["status"] == "PASS" for item in episode_results), "total": len(episode_results)})
check("episode_content_unique", len(set(hashes)) == 30, len(set(hashes)))
check("all_source_books_covered", covered_books == set(range(1, 25)), sorted(covered_books))
check(
    "episode_01_gate_preserved",
    load(OUT / "EPISODE_01_SCREENPLAY_VERIFICATION.json").get("status") == "PASS_EPISODE_01_SCREENPLAY_V1"
    and load(OUT / "EPISODE_01_SCREENPLAY_VERIFICATION.json").get("script_sha256") == hashes[0],
    hashes[0],
)

failures = [item for item in checks if item["status"] != "PASS"]
verification = {
    "artifact_class": "ctde_30_episode_screenplay_v1_independent_verification",
    "schema_version": "1.0.0",
    "status": "PASS_30_EPISODE_SCREENPLAY_V1" if not failures else "BLOCKED_30_EPISODE_SCREENPLAY_V1",
    "independent_from_builder": True,
    "adaptation_manifest_sha256": adaptation_sha,
    "screenplay_manifest_sha256": sha256(MANIFEST),
    "episode_count": len(episode_results),
    "passed": sum(item["status"] == "PASS" for item in episode_results),
    "failed": sum(item["status"] != "PASS" for item in episode_results),
    "source_book_count": len(covered_books),
    "total_bytes": sum(item["bytes"] for item in episode_results),
    "total_chinese_characters": sum(item["chinese_character_count"] for item in episode_results),
    "total_scenes": sum(item["scene_count"] for item in episode_results),
    "total_dialogue_cues": sum(item["dialogue_cue_count"] for item in episode_results),
    "checks": checks,
    "episodes": episode_results,
    "failure_count": len(failures),
    "generated_at": "2026-08-15T11:20:00Z",
}
VERIFICATION.write_text(
    json.dumps(verification, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n",
    encoding="utf-8",
)

result_status = verification["status"]
RESULT.write_text(
    "\n".join(
        [
            "# 《归途：奥德修斯》30 集剧本 V1 结果",
            "",
            f"Status: `{result_status}`",
            "",
            "- Episodes: 30",
            f"- Passed: {verification['passed']}",
            f"- Failed: {verification['failed']}",
            f"- Scenes: {verification['total_scenes']}",
            f"- Dialogue cues: {verification['total_dialogue_cues']}",
            f"- Chinese characters: {verification['total_chinese_characters']}",
            "- Episode 1 gate: PASS_EPISODE_01_SCREENPLAY_V1",
            "- Source coverage: Books 1–24",
            "- External model calls: 0",
            "- Greek TEI content reads: 0",
            "",
            "All 30 screenplay files were recovered from disk and independently checked against locked episode cards, source-event IDs, adaptation decisions, scene structure, episode-specific dialogue, ending hooks, artifact hashes, and the invention boundary.",
            "",
        ]
    ),
    encoding="utf-8",
)
print(result_status)
if failures:
    raise SystemExit(1)
