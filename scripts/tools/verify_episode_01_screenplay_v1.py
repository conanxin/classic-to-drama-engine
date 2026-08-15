from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from screenplay_dialogue_v1 import DIALOGUE


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts/odyssey_m1_v1/episodes/EP01.md"
CARD = ROOT / "adaptation/odyssey_m1_v1/episode_cards/EP01.json"
RESULT = ROOT / "scripts/odyssey_m1_v1/EPISODE_01_SCREENPLAY_VERIFICATION.json"


card = json.loads(CARD.read_text(encoding="utf-8"))
text = SCRIPT.read_text(encoding="utf-8")
checks: list[dict[str, object]] = []


def check(name: str, condition: bool, detail: object) -> None:
    checks.append({"check": name, "status": "PASS" if condition else "FAIL", "detail": detail})


scene_headers = re.findall(r"^## 场 (\d+)｜", text, flags=re.MULTILINE)
dialogue_cues = re.findall(r"^\*\*([^*]+)\*\*$", text, flags=re.MULTILINE)
chinese_characters = len(re.findall(r"[\u3400-\u9fff]", text))
forbidden = re.findall(r"(?i)\b(?:TODO|TBD|PLACEHOLDER)\b|待补|占位", text)

check("screenplay_file_identity", SCRIPT.is_file() and len(SCRIPT.read_bytes()) > 0, hashlib.sha256(SCRIPT.read_bytes()).hexdigest())
check("episode_metadata", "SCREENPLAY V1" in text and "约 7 分钟" in text and "Book 1" in text, {"episode": "EP01", "target_minutes": 7})
check("five_scene_screenplay", scene_headers == ["1", "2", "3", "4", "5"], scene_headers)
check("dialogue_density", len(dialogue_cues) >= 15, len(dialogue_cues))
check("substantive_chinese_draft", chinese_characters >= 650, chinese_characters)
check("source_events_exact", all(event_id in text for event_id in card["source_event_ids"]), card["source_event_ids"])
check("adaptation_decisions_exact", all(decision_id in text for decision_id in card["adaptation_decision_ids"]), card["adaptation_decision_ids"])
check("ending_hook_present", card["ending_cliffhanger"] in text and "切黑" in text, card["ending_cliffhanger"])
check(
    "locked_dialogue_materialized",
    all(spoken in text for scene in DIALOGUE[1] for _, spoken in scene),
    {"expected_lines": sum(len(scene) for scene in DIALOGUE[1])},
)
check("adaptation_boundary_explicit", "连接动作与中文对白均为 M1 改编表达" in text and "CONNECTIVE_ACTION_AND_DIALOGUE" in text, True)
check("no_placeholder_language", not forbidden, forbidden)

failures = [item for item in checks if item["status"] != "PASS"]
result = {
    "artifact_class": "ctde_episode_01_screenplay_v1_independent_verification",
    "schema_version": "1.0.0",
    "status": "PASS_EPISODE_01_SCREENPLAY_V1" if not failures else "BLOCKED_EPISODE_01_SCREENPLAY_V1",
    "episode_id": "EP01",
    "script_path": SCRIPT.relative_to(ROOT).as_posix(),
    "script_sha256": hashlib.sha256(SCRIPT.read_bytes()).hexdigest(),
    "script_bytes": len(SCRIPT.read_bytes()),
    "scene_count": len(scene_headers),
    "dialogue_cue_count": len(dialogue_cues),
    "chinese_character_count": chinese_characters,
    "checks": checks,
    "failure_count": len(failures),
    "generated_at": "2026-08-15T11:10:00Z",
}
RESULT.parent.mkdir(parents=True, exist_ok=True)
RESULT.write_text(
    json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n",
    encoding="utf-8",
)
print(result["status"])
if failures:
    raise SystemExit(1)
