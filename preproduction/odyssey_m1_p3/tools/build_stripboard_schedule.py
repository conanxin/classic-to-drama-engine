#!/usr/bin/env python3
"""Build the 150-scene stripboard and three deterministic shooting-day options."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
P3 = ROOT / "preproduction" / "odyssey_m1_p3"
INDEX_PATH = P3 / "SCENE_MASTER_INDEX.json"
SHOT_PATH = P3 / "SHOT_LIST_MASTER.json"
STRIP_PATH = P3 / "STRIPBOARD.json"

BLOCKS = {
    1: ("S1_CLEAN_PALACE", "S1 clean palace"),
    2: ("S1_CONTEST_PREBATTLE", "S1 contest / pre-battle"),
    3: ("S1_BATTLE", "S1 battle progression"),
    4: ("S4_FARM", "S4 Eumaeus farm"),
    5: ("S2_COURT_REDRESS", "S2 court redress"),
    6: ("S5_SHORE_CAVE", "S5 shore/cave plus U12 creature stage"),
    7: ("S3_DRY_DECK", "S3 dry deck"),
    8: ("U11_WET_MOTION", "U11 wet/motion"),
    9: ("U09_UNDERWORLD", "U09 Underworld"),
    10: ("U06_U07_CIVIC_HARBOR", "U06/U07 civic and harbor"),
    11: ("U08_ROADS_FOREST", "U08 roads/forest"),
    12: ("U10_FINALE", "U10 finale orchard/field"),
}

DAY_COUNTS = {
    "LEAN": [6, 2, 5, 2, 4, 4, 4, 3, 2, 4, 3, 3],
    "TARGET": [8, 3, 6, 3, 6, 6, 5, 4, 3, 4, 3, 3],
    "SAFE": [9, 3, 7, 3, 7, 7, 6, 5, 3, 5, 3, 4],
}
DAY_PREFIX = {"LEAN": "LEA", "TARGET": "TGT", "SAFE": "SAF"}
assert {k: sum(v) for k, v in DAY_COUNTS.items()} == {"LEAN": 42, "TARGET": 54, "SAFE": 62}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def block_number(scene: dict) -> int:
    unit = scene["production_unit"]
    ep = int(scene["episode"][2:])
    if unit == "S1":
        if ep in (25, 26):
            return 2
        if ep in (27, 28):
            return 3
        return 1
    return {
        "S4": 4, "S2": 5, "S5": 6, "U12": 6, "S3": 7, "U11": 8,
        "U09": 9, "U06": 10, "U07": 10, "U08": 11, "U10": 12,
    }[unit]


def special_equipment(scene: dict) -> list[str]:
    equipment = []
    if scene["stunt"]:
        equipment += ["STUNT_MATS", "SAFETY_VIDEO"]
    if scene["fight"]:
        equipment += ["RUBBER_WEAPONS", "ARMORER_CONTROL"]
    if scene["vfx"] != "NONE":
        equipment += ["CLEAN_PLATE_KIT", "VFX_REFERENCE_KIT"]
    if scene["creature"]:
        equipment += ["CREATURE_SCALE_REFERENCE", "CREATURE_CONTACT_RIG"]
    if scene["water"]:
        equipment += ["WET_SAFETY", "WARMING_STATION"]
    if scene["boats"]:
        equipment += ["MARINE_COMMS", "PFD_OFF_CAMERA"]
    if scene["animals"]:
        equipment += ["ANIMAL_HOLDING", "HANDLER_BARRIER"]
    if scene["sfx"]:
        equipment += [f"SFX_{x}" for x in scene["sfx"]]
    if scene["day_night"] in ("NIGHT", "TIMELESS"):
        equipment += ["CONTROLLED_LIGHTING"]
    return sorted(set(equipment))


def setup_minutes(scene: dict) -> int:
    value = 20 + scene["complexity"] * 10
    value += min(40, math.ceil(scene["extras"] / 6) * 5)
    value += 25 if scene["stunt"] else 0
    value += 20 if scene["vfx"] == "MEDIUM" or scene["creature"] else 0
    value += 20 if scene["water"] else 0
    value += 10 if scene["animals"] else 0
    return int(math.ceil(value / 5) * 5)


def scene_weight(scene: dict, shot_count: int) -> float:
    return (
        shot_count
        + scene["complexity"] * 1.8
        + min(scene["extras"], 40) / 8
        + (5 if scene["stunt"] else 0)
        + (4 if scene["vfx"] == "MEDIUM" or scene["creature"] else 0)
        + (4 if scene["water"] else 0)
        + (2 if scene["day_night"] in ("NIGHT", "TIMELESS") else 0)
    )


def scene_sort_key(block: int, scene: dict) -> tuple:
    story = (scene["episode"], scene["scene_number"])
    if block in (2, 3, 8, 9, 12):
        return story
    return (
        scene["production_unit"],
        scene["standing_set"] or "ZZ",
        scene["story_location"],
        scene["day_night"],
        *story,
    )


def schedule_cluster(block: int, scene: dict) -> tuple[int, str]:
    ep = int(scene["episode"][2:])
    location = scene["story_location"]
    unit = scene["production_unit"]
    if block == 1:
        if ep == 1: return (1, "EARLY_HOUSE")
        if ep in (20, 21): return (2, "RETURN_OCCUPATION")
        if ep in (22, 23): return (3, "INTERVIEW_SCAR")
        if ep == 24: return (4, "OMEN_PREP")
        return (5, "MARRIAGE_RECOGNITION")
    if block == 5:
        if "涅斯托耳" in location: return (1, "PYLOS")
        if "斯巴达" in location: return (2, "SPARTA")
        if "菲埃克斯" in location or "福耳库斯" in location: return (3, "PHAEACIA")
        return (4, "ISLAND_COURTS")
    if block == 6:
        if ep in (9, 10) and ("独眼" in location or "洞" in location): return (1, "CYCLOPS")
        if ep == 5: return (2, "OGYGIA")
        if ep == 6 or "斯刻里亚" in location: return (3, "SCHERIA_SHORE")
        return (4, "VOYAGE_SHORES")
    if block == 9:
        return (1, "EP13_DEAD") if ep == 13 else (2, "EP30_DEAD")
    if block == 10:
        return (1, "CIVIC") if unit == "U06" else (2, "HARBOR")
    if block == 11:
        if ep in (6, 12): return (1, "FOREST")
        if ep in (3, 7): return (2, "TRAVEL_ROAD")
        return (3, "ITHACA_ROAD")
    return (1, "PRIMARY")


def partition_contiguous(items: list[dict], groups: int, shot_counts: dict[str, int]) -> list[list[dict]]:
    assert groups <= len(items)
    weights = [scene_weight(scene, shot_counts[scene["scene_id"]]) for scene in items]
    result: list[list[dict]] = []
    cursor = 0
    remaining_weight = sum(weights)
    for group_index in range(groups):
        groups_left = groups - group_index
        items_left = len(items) - cursor
        if groups_left == 1:
            result.append(items[cursor:])
            break
        target = remaining_weight / groups_left
        maximum_take = items_left - (groups_left - 1)
        take = 0
        load = 0.0
        while take < maximum_take:
            next_weight = weights[cursor + take]
            if take > 0 and load + next_weight > target and abs(target - load) <= abs(target - (load + next_weight)):
                break
            load += next_weight
            take += 1
            if load >= target:
                break
        take = max(1, take)
        result.append(items[cursor:cursor + take])
        cursor += take
        remaining_weight -= sum(weights[cursor - take:cursor])
    assert len(result) == groups and all(result)
    assert [x["scene_id"] for group in result for x in group] == [x["scene_id"] for x in items]
    return result


def partition_by_clusters(items: list[dict], block: int, groups: int, shot_counts: dict[str, int]) -> list[list[dict]]:
    clusters: dict[tuple[int, str], list[dict]] = defaultdict(list)
    for scene in items:
        clusters[schedule_cluster(block, scene)].append(scene)
    ordered = [(key, sorted(value, key=lambda s: scene_sort_key(block, s))) for key, value in sorted(clusters.items())]
    assert groups >= len(ordered), (block, groups, len(ordered))
    allocation = {key: 1 for key, _ in ordered}
    weights = {key: sum(scene_weight(s, shot_counts[s["scene_id"]]) for s in value) for key, value in ordered}
    sizes = {key: len(value) for key, value in ordered}
    while sum(allocation.values()) < groups:
        candidates = [key for key, _ in ordered if allocation[key] < sizes[key]]
        assert candidates, (block, groups, allocation)
        key = max(candidates, key=lambda k: (weights[k] / allocation[k], sizes[k] - allocation[k], -k[0]))
        allocation[key] += 1
    result: list[list[dict]] = []
    for key, value in ordered:
        result.extend(partition_contiguous(value, allocation[key], shot_counts))
    assert len(result) == groups and all(result)
    return result


def build_stripboard(index: dict, shot_counts: dict[str, int]) -> dict:
    strips = []
    for scene in index["scenes"]:
        block = block_number(scene)
        strips.append({
            "scene_id": scene["scene_id"],
            "episode": scene["episode"],
            "int_ext": scene["int_ext"],
            "day_night": scene["day_night"],
            "production_unit": scene["production_unit"],
            "set": scene["standing_set"],
            "story_location": scene["story_location"],
            "cast": scene["cast"],
            "extras": scene["extras"],
            "props": scene["props"],
            "wardrobe": scene["wardrobe"],
            "hmu": scene["hmu"],
            "stunt": scene["stunt"],
            "fight": scene["fight"],
            "vfx": scene["vfx"],
            "creature": scene["creature"],
            "sfx": scene["sfx"],
            "animals": scene["animals"],
            "water": scene["water"],
            "boats": scene["boats"],
            "special_equipment": special_equipment(scene),
            "estimated_setup_minutes": setup_minutes(scene),
            "estimated_runtime_seconds": scene["estimated_runtime_seconds"],
            "planned_shots": shot_counts[scene["scene_id"]],
            "complexity": scene["complexity"],
            "shooting_block": {"number": block, "id": BLOCKS[block][0], "name": BLOCKS[block][1]},
        })
    assert len(strips) == 150 and len({s["scene_id"] for s in strips}) == 150
    return {
        "artifact_class": "odyssey_p3_stripboard",
        "schema_version": "1.0.0",
        "status": "PASS_150_OF_150_ASSIGNED_TO_12_BLOCKS",
        "source_scene_index_sha256": sha(INDEX_PATH),
        "source_shot_list_sha256": sha(SHOT_PATH),
        "scene_count": 150,
        "unassigned_scene_count": 0,
        "duplicate_scene_id_count": 0,
        "production_block_count": 12,
        "strips": strips,
    }


def risk_notes(scenes: list[dict]) -> list[str]:
    notes = []
    if any(s["stunt"] for s in scenes): notes.append("stunt coordinator and medic hold; no unrehearsed escalation")
    if any(s["water"] for s in scenes): notes.append("wet ladder, warming and marine/weather stop criteria")
    if any(s["vfx"] != "NONE" or s["creature"] for s in scenes): notes.append("clean/contact plates and measured eyelines before turnover")
    if any(s["animals"] for s in scenes): notes.append("animal coordinator owns pace and stop")
    if any(s["extras"] >= 12 for s in scenes): notes.append("foreground face/wardrobe pool ledger at check-in and wrap")
    if any("blood" in s["tags"] for s in scenes): notes.append("photographic blood and costume state before every reset")
    if any(s["day_night"] == "NIGHT" for s in scenes): notes.append("night turnaround and controlled-light limit")
    return notes or ["standard continuity and performance protection"]


def build_schedule(option: str, index: dict, shot_counts: dict[str, int]) -> dict:
    days = []
    day_counter = 0
    for block in range(1, 13):
        scenes = sorted([s for s in index["scenes"] if block_number(s) == block], key=lambda s: scene_sort_key(block, s))
        groups = partition_by_clusters(scenes, block, DAY_COUNTS[option][block - 1], shot_counts)
        for block_day, group in enumerate(groups, 1):
            day_counter += 1
            locations = list(dict.fromkeys(s["story_location"] for s in group))
            units = list(dict.fromkeys(s["production_unit"] for s in group))
            sets = list(dict.fromkeys((s["standing_set"] or s["production_unit"]) for s in group))
            cast = sorted({c for s in group for c in s["cast"]})
            episodes = sorted({s["episode"] for s in group})
            props = list(dict.fromkeys(p for s in group for p in s["props"]))[:12]
            external_day = any("EXT" in s["int_ext"] and s["day_night"] == "DAY" for s in group)
            blood = any("blood" in s["tags"] or "PRACTICAL_BLOOD" in s["sfx"] for s in group)
            company_move = len(units) > 1 and block not in (6, 10)
            if block in (6, 10) and len(units) > 1:
                move_note = "controlled adjacent-unit transfer inside the preplanned block; no public-road company move"
            elif company_move:
                move_note = "one planned company move; meal and daylight windows protected"
            else:
                move_note = "none; redress or zone change within the same production base"
            days.append({
                "day_id": f"{DAY_PREFIX[option]}-{day_counter:02d}",
                "option": option,
                "block": {"number": block, "id": BLOCKS[block][0], "name": BLOCKS[block][1], "day_within_block": block_day},
                "production_units": units,
                "sets": sets,
                "locations": locations,
                "scene_ids": [s["scene_id"] for s in group],
                "episodes": episodes,
                "cast": cast,
                "extras": max(s["extras"] for s in group),
                "extra_person_calls": sum(s["extras"] for s in group),
                "script_minutes": round(sum(s["estimated_runtime_seconds"] for s in group) / 60, 2),
                "planned_shots": sum(shot_counts[s["scene_id"]] for s in group),
                "shot_ids_authority": "SHOT_LIST_MASTER.json by scene_ids",
                "stunt": any(s["stunt"] for s in group),
                "vfx": any(s["vfx"] != "NONE" or s["creature"] for s in group),
                "wet": any(s["water"] for s in group),
                "blood": blood,
                "special_props": props,
                "company_move": company_move,
                "company_move_note": move_note,
                "sun_dependency": "HARD" if external_day else "NONE_OR_CONTROLLED",
                "risk_notes": risk_notes(group),
            })
    assigned = [sid for day in days for sid in day["scene_ids"]]
    assert len(days) == sum(DAY_COUNTS[option])
    assert len(assigned) == 150 and len(set(assigned)) == 150
    all_ids = {s["scene_id"] for s in index["scenes"]}
    assert set(assigned) == all_ids
    return {
        "artifact_class": "odyssey_p3_shooting_schedule",
        "schema_version": "1.0.0",
        "option": option,
        "recommended": option == "TARGET",
        "status": "PASS_150_OF_150_SCENES_SCHEDULED",
        "source_scene_index_sha256": sha(INDEX_PATH),
        "source_shot_list_sha256": sha(SHOT_PATH),
        "shooting_day_count": len(days),
        "scene_count": 150,
        "unassigned_scene_count": 0,
        "duplicate_scene_assignments": 0,
        "parallel_main_units": 0,
        "impossible_cast_overlap": 0,
        "company_move_days": sum(day["company_move"] for day in days),
        "total_planned_shots": sum(day["planned_shots"] for day in days),
        "total_script_minutes": round(sum(day["script_minutes"] for day in days), 2),
        "days": days,
    }


def encoded(data: dict) -> bytes:
    return (json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    index = json.loads(INDEX_PATH.read_text())
    shot_list = json.loads(SHOT_PATH.read_text())
    shot_counts: dict[str, int] = defaultdict(int)
    for shot in shot_list["shots"]:
        shot_counts[shot["scene_id"]] += 1
    outputs = {STRIP_PATH: encoded(build_stripboard(index, shot_counts))}
    for option in ("LEAN", "TARGET", "SAFE"):
        outputs[P3 / f"SHOOTING_SCHEDULE_{option}.json"] = encoded(build_schedule(option, index, shot_counts))
    if args.check:
        for path, payload in outputs.items():
            assert path.read_bytes() == payload, path
        print("PASS " + " ".join(f"{p.name}={hashlib.sha256(b).hexdigest()}" for p, b in outputs.items()))
    else:
        for path, payload in outputs.items():
            path.write_bytes(payload)
        print("WROTE " + " ".join(path.name for path in outputs))


if __name__ == "__main__":
    main()
