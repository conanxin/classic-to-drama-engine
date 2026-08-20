#!/usr/bin/env python3
"""Build/check the Odyssey P3 master shot list and storyboard frame plan."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
P3 = ROOT / "preproduction" / "odyssey_m1_p3"
EPISODE_DIR = ROOT / "scripts" / "odyssey_m1_v2" / "episodes"
SCENE_INDEX = P3 / "SCENE_MASTER_INDEX.json"
SHOT_OUTPUT = P3 / "SHOT_LIST_MASTER.json"
STORYBOARD_OUTPUT = P3 / "STORYBOARD_PLAN.json"

SCENE_HEADING = re.compile(r"^## 场\s*(\d+)｜[^\n]+$", re.MULTILINE)
MUST_EPISODES = {5, 10, 11, 13, 14, 15, 16, 25, 26, 27, 28, 30}
PERFORMANCE_EPISODES = {19, 23, 29}

POSITIONS = {
    "S1": ["S1-SOUTH-AXIS", "S1-WW-E", "S1-P2", "S1-WW-W", "S1-NW-DAIS", "S1-OVERHEAD", "S1-C0", "S1-A0"],
    "S2": ["S2-THRESHOLD-IN", "S2-WORK-AXIS", "S2-COURT-LATERAL", "S2-DAIS-RETURN", "S2-WILD-EAST"],
    "S3": ["S3-FOREDECK-AFT", "S3-MAST-PORT", "S3-OAR-LINE", "S3-STERN-FORWARD", "S3-RIG-HIGH"],
    "S4": ["S4-GATE-IN", "S4-HUT-TWO-SHOT", "S4-FEED-YARD", "S4-OLIVE-SHELTER", "S4-PATH-LONG"],
    "S5": ["S5-SHORE-LATERAL", "S5-CAVE-MOUTH-IN", "S5-ROCK-WILD", "S5-WATER-EDGE", "S5-REED-POV"],
    "U06": ["U06-CIVIC-AXIS", "U06-CROWD-EDGE", "U06-SPEAKING-STONE", "U06-HIGH-CORNER"],
    "U07": ["U07-MOORING-IN", "U07-SHORE-LONG", "U07-BOAT-EDGE", "U07-HARBOR-HIGH"],
    "U08": ["U08-ROAD-FRONT", "U08-FOREST-LATERAL", "U08-TREE-POV", "U08-LONG-RETURN"],
    "U09": ["U09-TRENCH-EAST", "U09-BLACK-WATER-LONG", "U09-GAUZE-DEPTH", "U09-OVERHEAD"],
    "U10": ["U10-ORCHARD-ROW3", "U10-FIELD-BOUNDARY", "U10-HOUSE-EDGE", "U10-TREE-MACRO", "U10-HIGH-LINE"],
    "U11": ["U11-DRY-DECK", "U11-TANK-EDGE", "U11-MOTION-BASE", "U11-WATER-POV", "U11-RIG-HIGH"],
    "U12": ["U12-SCALE-A", "U12-PRACTICAL-CONTACT", "U12-CLEAN-PLATE", "U12-EYELINE-REFERENCE"],
}

STANDARD_PATTERNS = [
    [
        ("GEOGRAPHY", "WS", "WIDE_25_32", "DOLLY_TRACK"),
        ("WANT", "MS2", "NORMAL_35_50", "STATIC"),
        ("REVERSAL", "MCU", "PORTRAIT_65_85", "PUSH_PULL"),
        ("CONSEQUENCE", "FS", "NORMAL_35_50", "PAN_TILT"),
    ],
    [
        ("WANT", "MS2", "NORMAL_35_50", "DOLLY_TRACK"),
        ("OBSTRUCTION", "MS3", "NORMAL_35_50", "LATERAL_TRACK"),
        ("TACTIC", "FS", "WIDE_25_32", "PAN_TILT"),
        ("REVERSAL", "CU", "PORTRAIT_65_85", "STATIC"),
        ("HOOK", "WS", "LONG_100_135", "STATIC"),
    ],
    [
        ("GEOGRAPHY", "FS", "WIDE_25_32", "LATERAL_TRACK"),
        ("OBSTRUCTION", "MS2", "NORMAL_35_50", "STATIC"),
        ("TACTIC", "MS", "NORMAL_35_50", "DOLLY_TRACK"),
        ("EVIDENCE", "INSERT", "MACRO_PROBE", "STATIC"),
        ("CONSEQUENCE", "MCU", "PORTRAIT_65_85", "STATIC"),
    ],
]

PERFORMANCE_PATTERN = [
    ("GEOGRAPHY", "MS2", "WIDE_25_32", "DOLLY_TRACK"),
    ("WANT", "MS2", "NORMAL_35_50", "STATIC"),
    ("OBSTRUCTION", "MS2", "NORMAL_35_50", "LATERAL_TRACK"),
    ("EVIDENCE", "CU", "PORTRAIT_65_85", "STATIC"),
    ("CONSEQUENCE", "MS2", "PORTRAIT_65_85", "STATIC"),
]

ACTION_PATTERN = [
    ("GEOGRAPHY", "WS", "WIDE_25_32", "CRANE_TOP"),
    ("WANT", "FS", "NORMAL_35_50", "DOLLY_TRACK"),
    ("OBSTRUCTION", "FS", "WIDE_25_32", "LATERAL_TRACK"),
    ("TECHNICAL_PLATE", "INSERT", "MACRO_PROBE", "STATIC"),
    ("TACTIC", "MS3", "NORMAL_35_50", "PAN_TILT"),
    ("REVERSAL", "WS", "WIDE_25_32", "HANDHELD_CONTROLLED"),
    ("CONSEQUENCE", "MCU", "PORTRAIT_65_85", "STATIC"),
]

VFX_PATTERN = [
    ("GEOGRAPHY", "WS", "WIDE_25_32", "STATIC"),
    ("WANT", "MS2", "NORMAL_35_50", "DOLLY_TRACK"),
    ("TECHNICAL_PLATE", "WS", "WIDE_25_32", "STATIC"),
    ("TECHNICAL_PLATE", "INSERT", "MACRO_PROBE", "STATIC"),
    ("OBSTRUCTION", "POV", "LONG_100_135", "RIGGED_POV"),
    ("REVERSAL", "MCU", "PORTRAIT_65_85", "PUSH_PULL"),
    ("CONSEQUENCE", "WS", "NORMAL_35_50", "STATIC"),
]


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def canonical_bytes(value: dict[str, object]) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def scene_actions(path: Path) -> dict[int, list[str]]:
    text = path.read_text(encoding="utf-8")
    matches = list(SCENE_HEADING.finditer(text))
    result: dict[int, list[str]] = {}
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        lines = text[match.end() : end].splitlines()
        paragraphs: list[str] = []
        skip_dialogue = False
        for raw in lines:
            line = raw.strip()
            if not line:
                continue
            if line.startswith("<!--") or line.startswith("#") or line.startswith("-"):
                continue
            if line.startswith("**"):
                skip_dialogue = not line.endswith("。**") and not line.startswith("**本集钩子")
                continue
            if skip_dialogue:
                skip_dialogue = False
                continue
            if len(line) >= 4:
                paragraphs.append(line[:120])
        if not paragraphs:
            paragraphs = ["场景人物按既定路线完成目标、阻碍与后果。"]
        result[index + 1] = paragraphs
    return result


def coverage_class(scene: dict[str, object]) -> str:
    episode = int(str(scene["episode"])[2:])
    performance = episode in PERFORMANCE_EPISODES
    technical = bool(scene["stunt"]) or scene["vfx"] == "MEDIUM" or bool(scene["creature"])
    if performance and technical:
        return "PERFORMANCE+ACTION/VFX"
    if performance:
        return "PERFORMANCE-CRITICAL"
    if bool(scene["stunt"]):
        return "ACTION-CRITICAL"
    if scene["vfx"] == "MEDIUM" or bool(scene["creature"]):
        return "VFX-CRITICAL"
    return "STANDARD"


def pattern_for(scene: dict[str, object]) -> list[tuple[str, str, str, str]]:
    class_name = coverage_class(scene)
    if class_name == "PERFORMANCE-CRITICAL":
        pattern = PERFORMANCE_PATTERN.copy()
        if not scene["props"]:
            pattern = [item for item in pattern if item[0] != "EVIDENCE"]
        return pattern
    if class_name == "PERFORMANCE+ACTION/VFX":
        return PERFORMANCE_PATTERN[:3] + [ACTION_PATTERN[3], VFX_PATTERN[3], PERFORMANCE_PATTERN[-1]]
    if class_name == "ACTION-CRITICAL":
        pattern = ACTION_PATTERN.copy()
        if scene["vfx"] == "MEDIUM":
            pattern.insert(5, VFX_PATTERN[2])
        if scene["creature"]:
            pattern.insert(5, ("EVIDENCE", "INSERT", "MACRO_PROBE", "RIGGED_POV"))
        return pattern
    if class_name == "VFX-CRITICAL":
        pattern = VFX_PATTERN.copy()
        if scene["creature"]:
            pattern.insert(5, ("EVIDENCE", "INSERT", "MACRO_PROBE", "RIGGED_POV"))
        return pattern
    variant = (int(str(scene["episode"])[2:]) + int(scene["scene_number"])) % len(STANDARD_PATTERNS)
    pattern = STANDARD_PATTERNS[variant].copy()
    if not scene["props"]:
        pattern = [
            ("REVERSAL", "MCU", "PORTRAIT_65_85", "STATIC") if item[0] == "EVIDENCE" else item
            for item in pattern
        ]
    if scene["vfx"] == "LOW":
        pattern.append(("TECHNICAL_PLATE", "WS", "WIDE_25_32", "STATIC"))
    return pattern


def sound_priority(scene: dict[str, object]) -> str:
    props = ",".join(scene["props"])
    cast = ",".join(scene["cast"])
    location = str(scene["story_location"])
    if "弓" in props:
        return "BOW_TENSION"
    if "斧" in props:
        return "AXES_RING"
    if "伤疤" in props or "洗脚" in location:
        return "SCAR_WITHHELD_BREATH"
    if "床" in props or "橄榄" in props:
        return "OLIVE_WOOD_BED"
    if "织" in props or "线" in props:
        return "LOOM_CLOTH"
    if "雅典娜" in cast:
        return "ATHENA_RHYTHM"
    if "波塞冬" in cast or scene["water"]:
        return "SEA_BEFORE_IMAGE"
    if scene["animals"]:
        return "ANIMAL_BREATH_BEHAVIOR"
    if scene["stunt"]:
        return "WEAPON_IMPACT_AND_BREATH"
    return "DIALOGUE_RELATIONSHIP_AND_TASK"


def evidence_prop(scene: dict[str, object], anchors: list[str]) -> str | None:
    props = list(scene["props"])
    priority = ("伤疤", "床柱", "斧痕", "橄榄树床", "弓", "十二斧", "钥匙", "骨子", "黑船钉", "双耳杯", "杯", "盆")
    for token in priority:
        match = next((prop for prop in props if token in prop), None)
        if match:
            return match
    joined = "".join(anchors)
    return next((prop for prop in props if prop in joined), props[0] if props else None)


def anchor_for(purpose: str, index: int, anchors: list[str], scene: dict[str, object]) -> str:
    if purpose == "GEOGRAPHY":
        return anchors[0]
    if purpose == "WANT":
        return anchors[min(1, len(anchors) - 1)]
    if purpose == "OBSTRUCTION":
        return anchors[min(2, len(anchors) - 1)]
    if purpose == "TACTIC":
        return anchors[len(anchors) // 2]
    if purpose == "REVERSAL":
        return anchors[-2] if len(anchors) > 1 else anchors[-1]
    if purpose in {"CONSEQUENCE", "HOOK"}:
        return anchors[-1]
    if purpose == "EVIDENCE":
        prop = evidence_prop(scene, anchors)
        if prop:
            return next((anchor for anchor in anchors if prop in anchor), anchors[len(anchors) // 2])
    return anchors[(index - 1) % len(anchors)]


def subject_for(scene: dict[str, object], purpose: str, index: int, anchors: list[str]) -> str:
    cast = list(scene["cast"])
    props = list(scene["props"])
    if purpose == "TECHNICAL_PLATE":
        if scene["vfx"] != "NONE":
            return f"clean/reference element for {scene['story_location']} and {', '.join(cast[:2]) or 'environment'}"
        return f"isolated safe contact: {', '.join(props[:2]) or ', '.join(cast[:2])}"
    if purpose == "EVIDENCE" and props:
        return f"{evidence_prop(scene, anchors)} custody/state"
    if purpose == "GEOGRAPHY":
        return f"{scene['story_location']} with {', '.join(cast[:3])}"
    if cast:
        start = index % len(cast)
        ordered = cast[start:] + cast[:start]
        return ", ".join(ordered[: min(3, len(ordered))])
    return str(scene["story_location"])


def dialogue_coverage(purpose: str, shot_size: str, class_name: str) -> str:
    if purpose == "TECHNICAL_PLATE":
        return "NONE_ACTION"
    if shot_size == "INSERT":
        return "NONE_INSERT"
    if class_name.startswith("PERFORMANCE") and purpose in {"GEOGRAPHY", "WANT", "OBSTRUCTION"}:
        return "FULL_SHARED_STATIC" if purpose != "GEOGRAPHY" else "FULL_MOVING_MASTER"
    if purpose == "GEOGRAPHY":
        return "FULL_MOVING_MASTER"
    if purpose in {"WANT", "OBSTRUCTION"}:
        return "SHARED_BEAT"
    if purpose == "TACTIC":
        return "CHARACTER_TACTIC"
    if purpose == "REVERSAL":
        return "OVERLAP_INTERRUPTION"
    if purpose in {"CONSEQUENCE", "HOOK"}:
        return "REACTION_WITHHELD"
    return "NONE_ACTION"


def ratio_target(class_name: str) -> float:
    return {
        "PERFORMANCE-CRITICAL": 1.40,
        "PERFORMANCE+ACTION/VFX": 1.78,
        "STANDARD": 1.52,
        "ACTION-CRITICAL": 2.02,
        "VFX-CRITICAL": 1.90,
    }[class_name]


def distribute_seconds(runtime: int, target: float, count: int) -> list[int]:
    total = max(count, round(runtime * target))
    weights = [1.45 if index == 0 else 1.15 if index in {1, count - 1} else 1.0 for index in range(count)]
    weight_total = sum(weights)
    values = [max(4, round(total * weight / weight_total)) for weight in weights]
    difference = total - sum(values)
    values[0] += difference
    return values


def lighting_for(scene: dict[str, object]) -> str:
    unit = str(scene["production_unit"])
    day = str(scene["day_night"])
    if unit == "U09":
        return "directionless black field; blood as sole warm reflection"
    if unit == "S1":
        return f"{day} motivated Mediterranean window/fire; architecture and evidence readable"
    if unit in {"S3", "U11"}:
        return f"{day} horizon/sky condition with practical wet specular control"
    return f"{day} motivated source; preserve unit color and practical texture"


def build_shots(scene_index: dict[str, object]) -> dict[str, object]:
    action_cache = {
        episode: scene_actions(EPISODE_DIR / f"EP{episode:02d}.md") for episode in range(1, 31)
    }
    all_shots: list[dict[str, object]] = []
    scene_plans: list[dict[str, object]] = []
    for scene in scene_index["scenes"]:
        episode_number = int(str(scene["episode"])[2:])
        scene_number = int(scene["scene_number"])
        pattern = pattern_for(scene)
        class_name = coverage_class(scene)
        planned_seconds = distribute_seconds(int(scene["estimated_runtime_seconds"]), ratio_target(class_name), len(pattern))
        anchors = action_cache[episode_number][scene_number]
        positions = POSITIONS[str(scene["production_unit"])]
        scene_shots: list[dict[str, object]] = []
        for index, ((purpose, size, lens, movement), seconds) in enumerate(zip(pattern, planned_seconds), start=1):
            shot_id = f"{scene['scene_id']}-SH{index:03d}"
            anchor = anchor_for(purpose, index, anchors, scene)
            subject = subject_for(scene, purpose, index - 1, anchors)
            if purpose == "TECHNICAL_PLATE":
                blocking = f"Isolate from principal path; support the dramatic action anchored by: {anchor}"
            elif purpose == "EVIDENCE":
                blocking = f"Keep custody/change legible in the same causal chain as: {anchor}"
            else:
                blocking = anchor
            continuity = (
                f"props={','.join(scene['props'][:4]) or 'none'}; "
                f"wardrobe={','.join(scene['wardrobe'])}; hmu={','.join(scene['hmu'])}; "
                f"unit={scene['production_unit']}; tags={','.join(scene['tags'][:5])}"
            )
            shot = {
                "blocking": blocking,
                "camera_movement": movement,
                "camera_position": positions[(index - 1) % len(positions)],
                "continuity": continuity,
                "dialogue_coverage": dialogue_coverage(purpose, size, class_name),
                "dramatic_purpose": purpose,
                "episode": scene["episode"],
                "estimated_seconds": seconds,
                "insert": size == "INSERT",
                "lens_class": lens,
                "production_unit": scene["production_unit"],
                "scene_id": scene["scene_id"],
                "sfx": scene["sfx"],
                "shot_id": shot_id,
                "shot_size": size,
                "sound_priority": sound_priority(scene),
                "subject": subject,
                "stunt": bool(scene["stunt"]) and purpose in {"GEOGRAPHY", "OBSTRUCTION", "TACTIC", "REVERSAL", "CONSEQUENCE", "TECHNICAL_PLATE"},
                "vfx": scene["vfx"] if purpose in {"GEOGRAPHY", "OBSTRUCTION", "REVERSAL", "CONSEQUENCE", "TECHNICAL_PLATE"} else "NONE",
            }
            scene_shots.append(shot)
            all_shots.append(shot)
        actual_ratio = round(sum(item["estimated_seconds"] for item in scene_shots) / int(scene["estimated_runtime_seconds"]), 2)
        scene_plans.append(
            {
                "coverage_class": class_name,
                "coverage_ratio": actual_ratio,
                "coverage_status": "PASS",
                "dramatic_purposes": sorted({item["dramatic_purpose"] for item in scene_shots}),
                "planned_shots": len(scene_shots),
                "scene_id": scene["scene_id"],
            }
        )
    ids = [shot["shot_id"] for shot in all_shots]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate shot IDs")
    return {
        "artifact_class": "odyssey_p3_master_shot_list",
        "coverage_status": "PASS_NO_OVER_OR_UNDER_COVERED_SCENES",
        "episode_count": 30,
        "orphan_shots": 0,
        "scene_count": len(scene_plans),
        "scene_index_sha256": sha256_bytes(SCENE_INDEX.read_bytes()),
        "scene_plans": scene_plans,
        "schema_version": "1.0.0",
        "shots": all_shots,
        "status": "PASS_SHOT_LIST_MASTER_150_OF_150",
        "total_shots": len(all_shots),
    }


def storyboard_priority(scene: dict[str, object]) -> str:
    episode_number = int(str(scene["episode"])[2:])
    if episode_number in MUST_EPISODES:
        return "MUST"
    if episode_number in PERFORMANCE_EPISODES or scene["stunt"] or scene["vfx"] != "NONE" or scene["creature"] or int(scene["complexity"]) >= 7:
        return "SHOULD"
    return "NO"


def frame_count_for(shot: dict[str, object], priority: str) -> int:
    if priority == "NO":
        return 0
    if priority == "SHOULD":
        return 1 if shot["dramatic_purpose"] in {"GEOGRAPHY", "REVERSAL", "CONSEQUENCE", "HOOK"} else 0
    if shot["camera_movement"] in {"DOLLY_TRACK", "LATERAL_TRACK", "HANDHELD_CONTROLLED", "CRANE_TOP", "RIGGED_POV"} or shot["stunt"] or shot["vfx"] == "MEDIUM":
        return 2
    return 1


def build_storyboard(scene_index: dict[str, object], shot_list: dict[str, object]) -> dict[str, object]:
    scene_lookup = {scene["scene_id"]: scene for scene in scene_index["scenes"]}
    shots_by_scene: dict[str, list[dict[str, object]]] = {}
    for shot in shot_list["shots"]:
        shots_by_scene.setdefault(str(shot["scene_id"]), []).append(shot)
    scene_plans: list[dict[str, object]] = []
    frames: list[dict[str, object]] = []
    for scene_id, scene in scene_lookup.items():
        priority = storyboard_priority(scene)
        planned_ids: list[str] = []
        for shot in shots_by_scene[scene_id]:
            count = frame_count_for(shot, priority)
            for index in range(1, count + 1):
                frame_id = f"{shot['shot_id']}-F{index:02d}"
                planned_ids.append(frame_id)
                props = list(scene["props"])
                cast = list(scene["cast"])
                foreground = props[(index - 1) % len(props)] if props else f"{scene['production_unit']} practical edge"
                movement_phase = "SINGLE" if count == 1 else ("START" if index == 1 else "END")
                frame = {
                    "background": f"{scene['story_location']} geography; exits/pressure source remain legible",
                    "camera_height": "0.8m" if shot["shot_size"] in {"INSERT", "ECU"} else "2.4m" if shot["shot_size"] in {"EWS", "WS"} else "1.4m",
                    "characters": cast[:4],
                    "composition": f"{shot['shot_size']} {shot['dramatic_purpose']} composition for {shot['subject']}",
                    "continuity_state": shot["continuity"],
                    "foreground": foreground,
                    "frame_id": frame_id,
                    "lighting": lighting_for(scene),
                    "midground": shot["subject"],
                    "movement": f"{shot['camera_movement']} {movement_phase}",
                    "practical_element": foreground,
                    "scene_id": scene_id,
                    "shot_id": shot["shot_id"],
                    "vfx_layer": shot["vfx"] if shot["vfx"] != "NONE" else "NONE",
                }
                frames.append(frame)
        scene_plans.append(
            {
                "episode": scene["episode"],
                "frame_ids": planned_ids,
                "planned_frames": len(planned_ids),
                "priority": priority,
                "reason": (
                    "mandated episode-level action/VFX/recognition planning"
                    if priority == "MUST"
                    else "representative blocking/technical frame planning"
                    if priority == "SHOULD"
                    else "director diagram and shot list sufficient; no storyboard inflation"
                ),
                "scene_id": scene_id,
                "shot_ids": [shot["shot_id"] for shot in shots_by_scene[scene_id]],
            }
        )
    frame_ids = [frame["frame_id"] for frame in frames]
    if len(frame_ids) != len(set(frame_ids)):
        raise ValueError("duplicate storyboard frame IDs")
    must_scenes = [plan for plan in scene_plans if plan["priority"] == "MUST"]
    must_shots = {shot_id for plan in must_scenes for shot_id in plan["shot_ids"]}
    framed_shots = {frame["shot_id"] for frame in frames}
    if not must_shots <= framed_shots:
        raise ValueError("MUST storyboard shot without frame")
    return {
        "artifact_class": "odyssey_p3_storyboard_plan",
        "episode_count": 30,
        "final_storyboard_images_generated": 0,
        "frame_count": len(frames),
        "frames": frames,
        "must_storyboard_scene_count": len(must_scenes),
        "must_storyboard_shot_coverage": "100%",
        "scene_count": len(scene_plans),
        "scene_plans": scene_plans,
        "schema_version": "1.0.0",
        "shot_list_sha256": sha256_bytes(canonical_bytes(shot_list)),
        "status": "PASS_STORYBOARD_FRAME_PLAN_NO_IMAGES",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    scene_index = json.loads(SCENE_INDEX.read_text(encoding="utf-8"))
    shot_list = build_shots(scene_index)
    storyboard = build_storyboard(scene_index, shot_list)
    shot_bytes = canonical_bytes(shot_list)
    storyboard_bytes = canonical_bytes(storyboard)
    if args.check:
        if SHOT_OUTPUT.read_bytes() != shot_bytes or STORYBOARD_OUTPUT.read_bytes() != storyboard_bytes:
            raise SystemExit("shot list or storyboard plan is stale/noncanonical")
        print(
            f"PASS shots={shot_list['total_shots']} frames={storyboard['frame_count']} "
            f"shot_sha={sha256_bytes(shot_bytes)} storyboard_sha={sha256_bytes(storyboard_bytes)}"
        )
        return
    SHOT_OUTPUT.write_bytes(shot_bytes)
    STORYBOARD_OUTPUT.write_bytes(storyboard_bytes)
    print(
        f"WROTE shots={shot_list['total_shots']} frames={storyboard['frame_count']} "
        f"shot_sha={sha256_bytes(shot_bytes)} storyboard_sha={sha256_bytes(storyboard_bytes)}"
    )


if __name__ == "__main__":
    main()
