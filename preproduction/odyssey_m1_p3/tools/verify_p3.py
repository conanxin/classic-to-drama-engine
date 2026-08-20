#!/usr/bin/env python3
"""Independent structural, production and immutability verification for Odyssey P3."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
P3 = ROOT / "preproduction" / "odyssey_m1_p3"
BASELINE = "17cbd562fae17f55ab075cc8643549cfc6a80eab"
OUT = P3 / "P3_INDEPENDENT_VERIFICATION.json"
MANIFEST = P3 / "P3_ARTIFACT_MANIFEST.json"
RESULT = P3 / "P3_FINAL_RESULT.md"

FROZEN = {
    "scripts/odyssey_m1_v2": "fe1045bf959b57149d13ba1aa8d6908a84508021",
    "editorial/odyssey_m1_v2": "86b06571a3dd91004522d46f8aaf301204267e08",
    "production/odyssey_m1_v2": "eab18ebe8186dd1e964060bec4878ddcfe31b282",
    "ODYSSEY_V2_FINAL_RESULT.md": "a850597bd727120fa7356da4f8463e107a0cbb30",
    "runtime_capability_prototype": "0615e1dd144d69a12f2e40cb88a3bb0a0392896c",
}

REQUIRED = {
    "DIRECTOR_PACKAGE.md", "DIRECTOR_VISION.md", "VISUAL_GRAMMAR.md", "CAMERA_GRAMMAR.md",
    "EDITING_GRAMMAR.md", "PERFORMANCE_DIRECTION.md", "EPISODE_DIRECTOR_BREAKDOWN.md",
    "S1_ITHACA_HALL_FLOOR_PLAN.json", "EP26_EP28_ACTION_PREVIS.json", "SCENE_MASTER_INDEX.json",
    "SHOT_LIST_GRAMMAR.md", "SHOT_LIST_MASTER.json", "STORYBOARD_PLAN.md", "STORYBOARD_PLAN.json",
    "CASTING_BREAKDOWN.md", "CASTING_PRIORITY_MATRIX.md", "EXTRAS_ENSEMBLE_PLAN.md",
    "WARDROBE_CONTINUITY_PLAN.md", "HAIR_MAKEUP_CONTINUITY_PLAN.md", "PROP_CONTINUITY_BOOK.md",
    "VFX_BREAKDOWN.md", "VFX_CREATURE_EXECUTION_MATRIX.json", "EP10_CYCLOPS_EXECUTION_PLAN.md",
    "EP14_STRAIT_EXECUTION_PLAN.md", "EP27_EP28_BATTLE_SHOOTING_PLAN.md", "SFX_STUNT_BREAKDOWN.md",
    "SOUND_MUSIC_CUE_PLAN.md", "STRIPBOARD.json", "SHOOTING_SCHEDULE.md",
    "SHOOTING_SCHEDULE_LEAN.json", "SHOOTING_SCHEDULE_TARGET.json", "SHOOTING_SCHEDULE_SAFE.json",
    "CALL_SHEET_LOGIC.md", "BUDGET_MODEL.md", "BUDGET_RISK_REGISTER.md", "PRODUCTION_RISK_REGISTER.md",
    "INDEPENDENT_PRODUCTION_REVIEW.md", "SCRIPT_CHANGE_REQUESTS.md",
}


def run(*args: str) -> str:
    return subprocess.check_output(args, cwd=ROOT, text=True).strip()


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(name: str) -> dict:
    return json.loads((P3 / name).read_text())


def verify_manifest() -> None:
    manifest = json.loads(MANIFEST.read_text())
    entries = manifest["entries"]
    assert manifest["artifact_count"] == len(entries)
    assert len({entry["path"] for entry in entries}) == len(entries)
    for entry in entries:
        path = ROOT / entry["path"]
        assert path.is_file()
        assert path.stat().st_size == entry["bytes"]
        assert sha(path) == entry["sha256"]
    payload = (json.dumps(entries, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode()
    assert hashlib.sha256(payload).hexdigest() == manifest["entry_payload_sha256"]


def build_verification() -> dict:
    missing = sorted(name for name in REQUIRED if not (P3 / name).is_file())
    assert not missing, missing
    for path, expected in FROZEN.items():
        assert run("git", "rev-parse", f"{BASELINE}:{path}") == expected
    changed = run("git", "diff", "--name-only", BASELINE, "--", *FROZEN.keys())
    dirty = run("git", "status", "--porcelain", "--", *FROZEN.keys())
    assert changed == "" and dirty == ""

    index = load("SCENE_MASTER_INDEX.json")
    scenes = index["scenes"]
    scene_ids = [scene["scene_id"] for scene in scenes]
    assert index["episode_count"] == 30 and len(scenes) == 150 and len(set(scene_ids)) == 150
    required_scene = {"scene_id", "episode", "scene_number", "int_ext", "day_night", "story_location", "production_unit", "standing_set", "cast", "extras", "props", "wardrobe", "hmu", "stunt", "vfx", "sfx", "animals", "water", "boats", "estimated_runtime_seconds", "complexity"}
    assert all(required_scene <= scene.keys() for scene in scenes)
    animal_scenes = [scene for scene in scenes if scene["animals"]]
    assert len(animal_scenes) == 17
    assert {scene["scene_id"] for scene in scenes if scene["production_unit"] == "S1" and scene["animals"]} == {"EP20-S03", "EP24-S02"}

    floor = load("S1_ITHACA_HALL_FLOOR_PLAN.json")
    assert floor["status"] == "FROZEN_S1_FLOOR_PLAN"
    assert [state["id"] for state in floor["states"]] == ["S1-A", "S1-B", "S1-C", "S1-D", "S1-E", "S1-F"]
    assert {"WW-W", "WW-E", "WW-S", "WW-NW"} == set(floor["wild_walls"])

    action = load("EP26_EP28_ACTION_PREVIS.json")
    beats = action["beats"]
    beat_ids = [beat["id"] for beat in beats]
    assert len(beats) == 44 and len(set(beat_ids)) == 44
    assert sum(beat_id.startswith("A26-") for beat_id in beat_ids) == 12
    assert sum(beat_id.startswith("A27-") for beat_id in beat_ids) == 15
    assert sum(beat_id.startswith("A28-") for beat_id in beat_ids) == 17
    required_beat = {"starting_state", "initiator", "action", "target", "weapon", "blocking", "camera_priority", "stunt_requirement", "vfx_sfx", "safety", "continuity_consequence", "ending_state"}
    assert all(required_beat <= beat.keys() for beat in beats)
    arrows = action["ledgers"]["arrows"]
    assert arrows[0]["available"] == 11 and arrows[-1]["available"] == 0 and arrows[-1]["expended"] == 12

    shots = load("SHOT_LIST_MASTER.json")
    shot_rows = shots["shots"]
    shot_ids = [shot["shot_id"] for shot in shot_rows]
    shot_scene_ids = {shot["scene_id"] for shot in shot_rows}
    assert shots["total_shots"] == 831 and len(shot_rows) == 831 and len(set(shot_ids)) == 831
    assert shot_scene_ids == set(scene_ids) and shots["orphan_shots"] == 0
    assert shots["coverage_status"] == "PASS_NO_OVER_OR_UNDER_COVERED_SCENES"
    assert round(len(shot_rows) / len(scenes), 2) == 5.54

    story = load("STORYBOARD_PLAN.json")
    assert story["scene_count"] == 150 and story["must_storyboard_scene_count"] == 60
    assert story["frame_count"] == 711 and story["must_storyboard_shot_coverage"] == "100%"
    assert story["final_storyboard_images_generated"] == 0

    fight = [scene for scene in scenes if scene["fight"]]
    medium = [scene for scene in scenes if scene["vfx"] == "MEDIUM"]
    creature = [scene for scene in scenes if scene["creature"]]
    stunt = [scene for scene in scenes if scene["stunt"]]
    assert len(fight) == 8 and len(medium) == 16 and len(creature) == 8 and len(stunt) == 30
    assert all(scene["scene_id"] in shot_scene_ids for scene in fight + medium + creature)
    vfx = load("VFX_CREATURE_EXECUTION_MATRIX.json")
    assert vfx["medium_plus_vfx_scene_count"] == 16 and vfx["creature_scene_count"] == 8
    assert vfx["series_planned_vfx_shot_count"] == 171 and not vfx["full_cg_hero_creature_required"]
    assert all(row["clean_plate_required"] and row["actor_eyeline_reference_required"] for row in vfx["rows"])

    strip = load("STRIPBOARD.json")
    strips = strip["strips"]
    assert strip["scene_count"] == 150 and strip["unassigned_scene_count"] == 0
    assert len(strips) == 150 and {row["scene_id"] for row in strips} == set(scene_ids)

    schedule_counts = {}
    for option, expected_days in (("LEAN", 42), ("TARGET", 54), ("SAFE", 62)):
        schedule = load(f"SHOOTING_SCHEDULE_{option}.json")
        assigned = [scene_id for day in schedule["days"] for scene_id in day["scene_ids"]]
        assert schedule["shooting_day_count"] == expected_days and len(assigned) == 150 and len(set(assigned)) == 150
        assert set(assigned) == set(scene_ids) and schedule["total_planned_shots"] == 831
        assert schedule["unassigned_scene_count"] == 0 and schedule["impossible_cast_overlap"] == 0
        schedule_counts[option.lower()] = expected_days
    target = load("SHOOTING_SCHEDULE_TARGET.json")
    target_by_scene = {sid: day for day in target["days"] for sid in day["scene_ids"]}
    for scene in scenes:
        day = target_by_scene[scene["scene_id"]]
        if scene["water"]: assert day["wet"]
        if "blood" in scene["tags"] or "PRACTICAL_BLOOD" in scene["sfx"]: assert day["blood"]
    assert max(day["planned_shots"] for day in target["days"]) == 26
    assert max(day["script_minutes"] for day in target["days"]) == 7.42

    budget = (P3 / "BUDGET_MODEL.md").read_text()
    assert "¥23,440,968" in budget and "¥38,262,784" in budget and "¥67,977,248" in budget
    assert "NOT VENDOR QUOTE" in budget and all(cut in budget for cut in ("-10%", "-20%", "-30%"))
    requests = (P3 / "SCRIPT_CHANGE_REQUESTS.md").read_text()
    assert "script_change_request_count: 0" in requests and "PASS_NO_SCRIPT_CHANGE_REQUIRED" in requests
    review = (P3 / "INDEPENDENT_PRODUCTION_REVIEW.md").read_text()
    for label in ("Director result", "DP result", "1st AD result", "Line producer result", "Stunt/VFX result"):
        assert label in review

    return {
        "artifact_class": "odyssey_p3_independent_verification",
        "schema_version": "1.0.0",
        "status": "PASS_ODYSSEY_P3_INDEPENDENT_VERIFICATION",
        "baseline_commit": BASELINE,
        "episodes": 30,
        "scenes": 150,
        "scene_index_coverage": "150/150",
        "stripboard_coverage": "150/150",
        "shot_list_scene_coverage": "150/150",
        "total_shots": 831,
        "average_shots_per_scene": 5.54,
        "orphan_shots": 0,
        "duplicate_shot_ids": 0,
        "must_storyboard_scenes": 60,
        "must_storyboard_coverage": "100%",
        "storyboard_frames_planned": 711,
        "final_storyboard_images_generated": 0,
        "fight_scene_coverage": "8/8",
        "medium_plus_vfx_scene_coverage": "16/16",
        "creature_scene_coverage": "8/8",
        "stunt_scenes": 30,
        "animal_scenes": 17,
        "false_s1_animal_calls": 0,
        "schedule_days": schedule_counts,
        "schedule_unassigned_scenes": 0,
        "impossible_cast_overlap": 0,
        "s1_state_continuity": "PASS",
        "wet_continuity": "PASS",
        "blood_continuity": "PASS",
        "v2_modified": 0,
        "runtime_modified": 0,
        "script_change_requests": 0,
        "frozen_git_identities": FROZEN,
        "key_artifact_sha256": {
            "scene_master_index": sha(P3 / "SCENE_MASTER_INDEX.json"),
            "shot_list_master": sha(P3 / "SHOT_LIST_MASTER.json"),
            "storyboard_plan": sha(P3 / "STORYBOARD_PLAN.json"),
            "stripboard": sha(P3 / "STRIPBOARD.json"),
            "target_schedule": sha(P3 / "SHOOTING_SCHEDULE_TARGET.json"),
            "vfx_creature_matrix": sha(P3 / "VFX_CREATURE_EXECUTION_MATRIX.json"),
            "budget_model": sha(P3 / "BUDGET_MODEL.md"),
        },
    }


def encoded(value: dict) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    expected = encoded(build_verification())
    if args.write:
        OUT.write_bytes(expected)
    if OUT.exists():
        assert OUT.read_bytes() == expected
    if MANIFEST.exists() and not args.write:
        verify_manifest()
    if RESULT.exists():
        result = RESULT.read_text()
        assert "PASS_ODYSSEY_P3_DIRECTOR_AND_PRODUCTION_PACKAGE" in result
        if MANIFEST.exists() and not args.write: assert sha(MANIFEST) in result
    manifest_status = "DEFERRED_REBUILD" if args.write and MANIFEST.exists() else ("PASS" if MANIFEST.exists() else "PENDING")
    print(f"PASS verification_sha256={hashlib.sha256(expected).hexdigest()} manifest={manifest_status} result={'PASS' if RESULT.exists() else 'PENDING'}")


if __name__ == "__main__":
    main()
