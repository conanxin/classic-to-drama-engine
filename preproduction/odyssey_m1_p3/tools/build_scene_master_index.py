#!/usr/bin/env python3
"""Build or check the deterministic Odyssey P3 150-scene master index."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
EPISODE_DIR = ROOT / "scripts" / "odyssey_m1_v2" / "episodes"
OUTPUT = ROOT / "preproduction" / "odyssey_m1_p3" / "SCENE_MASTER_INDEX.json"
V2_MANIFEST = ROOT / "scripts" / "odyssey_m1_v2" / "SCREENPLAY_V2_MANIFEST.json"

SCENE = re.compile(r"^## 场\s*(\d+)｜([^｜]+)｜约\s*(\d+)'(\d+)\"$", re.MULTILINE)
PRODUCTION = re.compile(r"<!-- production: (.+?) -->")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def parse_fields(value: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for item in value.split(";"):
        key, separator, field_value = item.strip().partition("=")
        if separator:
            fields[key] = field_value.strip()
    return fields


def parse_list(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


def extras_count(value: str) -> int:
    values = [int(item) for item in re.findall(r"\d+", value)]
    if values:
        return max(values)
    if value == "crowd":
        return 16
    if value == "background":
        return 8
    return 0


def split_location(value: str) -> tuple[str, str, str]:
    parts = value.split("·")
    prefix = parts[0]
    story_location = "·".join(parts[1:-1]) if len(parts) > 2 else parts[-1]
    time_value = parts[-1]
    if "内景" in value and "外景" in value:
        int_ext = "INT/EXT"
    elif prefix == "内外景":
        int_ext = "INT/EXT"
    elif prefix == "内景":
        int_ext = "INT"
    else:
        int_ext = "EXT"
    if time_value == "无时":
        day_night = "TIMELESS"
    elif any(token in time_value for token in ("转", "／")):
        day_night = "MIXED"
    elif any(token in time_value for token in ("夜", "暮", "黄昏")):
        day_night = "NIGHT"
    else:
        day_night = "DAY"
    return int_ext, day_night, story_location


def production_unit(episode: int, location: str, tags: set[str]) -> tuple[str, str | None, list[str]]:
    secondary: list[str] = []
    if tags & {"creature-medium", "creature-scale"}:
        secondary.append("U12")
    if "underworld" in tags or any(name in location for name in ("冥界", "血沟")):
        return "U09", None, secondary
    if any(name in location for name in ("果园", "田野")) and episode == 30:
        return "U10", None, secondary
    if tags & {"water-heavy", "storm"} or "雷暴海面" in location:
        return "U11", None, secondary
    if any(name in location for name in ("集会场", "竞技场")):
        return "U06", None, secondary
    if any(name in location for name in ("海港", "外港", "水道")) and "甲板" not in location:
        return "U07", None, secondary
    if any(name in location for name in ("道路", "森林", "山路", "街道")):
        return "U08", None, secondary
    if any(name in location for name in ("欧迈俄斯", "猪场", "猪栏", "茅屋")):
        return "S4", "S4", secondary
    if any(name in location for name in ("伊萨卡厅堂", "封闭厅堂", "夜间厅堂", "清洗后的厅堂", "婚房", "洗脚处", "武器库", "宫殿庭院", "宫殿门槛", "磨坊", "佩涅洛佩", "忒勒马科斯寝室")):
        return "S1", "S1", secondary
    if any(name in location for name in ("涅斯托耳宫院", "斯巴达宫", "菲埃克斯", "喀耳刻宫殿", "埃俄罗斯岛露台")):
        return "S2", "S2", secondary
    if "boat" in tags:
        return "S3", "S3", secondary
    if "甲板" in location or "返航船" in location or ("船" in location and "海岸" not in location):
        return "S3", "S3", secondary
    if any(name in location for name in ("海岸", "河口", "洞穴", "洞口", "近岸", "岸边", "林地")):
        return "S5", "S5", secondary
    if episode in {1, 2, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29}:
        return "S1", "S1", secondary
    return "S5", "S5", secondary


def odysseus_wardrobe(episode: int, location: str) -> str:
    if episode == 5:
        return "W-OD-05-OGYGIA-RAFT-SALT"
    if episode == 6:
        return "W-OD-06-SCHERIA-WRECK-BORROWED"
    if episode in {7, 8} or "菲埃克斯" in location:
        return "W-OD-07-PHAEACIA-BORROWED-WHITE"
    if 9 <= episode <= 15:
        return f"W-OD-{episode:02d}-VOYAGE-MEMORY"
    if episode == 16:
        return "W-OD-16-ITHACA-ARRIVAL-DISGUISE"
    if episode in {17, 18}:
        return "W-OD-17-FARM-BEGGAR"
    if episode == 19:
        return "W-OD-19-BEGGAR-REVEAL"
    if 20 <= episode <= 26:
        return "W-OD-20-BEGGAR-HALL"
    if episode in {27, 28}:
        return "W-OD-27-BATTLE"
    if episode == 29:
        return "W-OD-29-CLEANED-RETURNED"
    return "W-OD-30-RETURNED-FIELD"


def wardrobe_states(episode: int, cast: list[str], location: str) -> list[str]:
    states: list[str] = []
    joined = ",".join(cast)
    if "奥德修斯" in joined:
        states.append(odysseus_wardrobe(episode, location))
    if "佩涅洛佩" in joined:
        if episode == 25:
            states.append("W-PE-25-CONTEST-CUSTODY")
        elif episode == 29:
            states.append("W-PE-29-RECOGNITION")
        elif episode == 30:
            states.append("W-PE-30-CIVIC-RESTORATION")
        else:
            states.append("W-PE-01-HOUSEHOLD-MOURNING-PURPLE")
    if "忒勒马科斯" in joined:
        if episode <= 2:
            states.append("W-TE-01-BOY-HOUSEHOLD")
        elif episode <= 4:
            states.append("W-TE-03-TRAVELER")
        elif episode == 18:
            states.append("W-TE-18-RETURNING-TRAVELER")
        elif 19 <= episode <= 25:
            states.append("W-TE-19-SECRET-HEIR")
        elif 26 <= episode <= 29:
            states.append("W-TE-26-BATTLE-HEIR")
        else:
            states.append("W-TE-30-CIVIC-AUTHORITY")
    if "雅典娜" in joined:
        disguise = next((name.split("/", 1)[1] for name in cast if name.startswith("雅典娜/")), "DIVINE")
        states.append(f"W-AT-{disguise}")
    if not states:
        states.append(f"W-ENS-{episode:02d}-SCENE")
    return states


def hmu_states(episode: int, cast: list[str], tags: set[str]) -> list[str]:
    states: list[str] = []
    joined = ",".join(cast)
    if "奥德修斯" in joined:
        if episode <= 6:
            states.append("HMU-OD-SALT-CUTS-PROGRESSION")
        elif 9 <= episode <= 15:
            states.append(f"HMU-OD-VOYAGE-{episode:02d}")
        elif 16 <= episode <= 25:
            states.append("HMU-OD-OLD-BEGGAR-SCAR-COVER")
        elif episode in {26, 27, 28}:
            states.append("HMU-OD-BEGGAR-BATTLE-BLOOD")
        elif episode == 29:
            states.append("HMU-OD-CLEANED-BRUISED-SCAR")
        else:
            states.append("HMU-OD-RETURNED-FIELD")
    if "忒勒马科斯" in joined:
        states.append("HMU-TE-BATTLE-ARM-WOUND" if episode in {28, 29, 30} else "HMU-TE-AGE-PROGRESSION")
    if "佩涅洛佩" in joined:
        states.append("HMU-PE-HOUSEHOLD-PRESSURE")
    if "雅典娜" in joined:
        states.append("HMU-AT-DISGUISE-EYELIGHT-CONTINUITY")
    if "makeup" in tags:
        states.append("HMU-SPECIAL-PROSTHETIC")
    if not states:
        states.append(f"HMU-ENS-{episode:02d}")
    return states


def animals_in(text: str) -> list[str]:
    mapping = {
        "猪": "PIG",
        "羊": "SHEEP",
        "牛": "CATTLE",
        "狗": "DOG",
        "鹰": "RAPTOR",
        "骡": "MULE",
        "马": "HORSE",
        "海豹": "SEAL",
    }
    return sorted({label for token, label in mapping.items() if token in text})


def vfx_level(tags: set[str]) -> str:
    if tags & {"vfx-medium", "divine-medium", "underworld"}:
        return "MEDIUM"
    if tags & {"vfx-low", "divine-low", "divine", "wind-vfx", "animal-vfx-low"}:
        return "LOW"
    return "NONE"


def sfx_items(tags: set[str]) -> list[str]:
    mapping = {
        "blood": "PRACTICAL_BLOOD",
        "fire": "CONTROLLED_FIRE",
        "storm": "WIND_RAIN_SPRAY",
        "water-heavy": "WATER_INTERACTION",
        "weather": "WEATHER_EFFECT",
        "practical-effect": "PRACTICAL_EFFECT",
        "stunt": "BREAKAWAY_IMPACT",
    }
    return sorted({value for key, value in mapping.items() if key in tags})


def scene_score(extras: int, tags: set[str]) -> int:
    score = 1
    if extras >= 16:
        score += 3
    elif extras >= 8:
        score += 2
    elif extras:
        score += 1
    if tags & {"water", "water-heavy", "boat", "storm"}:
        score += 2
    if tags & {"fight", "stunt", "stunt-low", "stunt-safe"}:
        score += 2
    if tags & {"vfx-medium", "divine-medium", "underworld"}:
        score += 2
    elif tags & {"vfx-low", "divine-low", "divine"}:
        score += 1
    if "creature-medium" in tags:
        score += 2
    if tags & {"fire", "blood", "makeup"}:
        score += 1
    return min(score, 10)


def build_index() -> dict[str, object]:
    scenes: list[dict[str, object]] = []
    for episode in range(1, 31):
        episode_id = f"EP{episode:02d}"
        path = EPISODE_DIR / f"{episode_id}.md"
        payload = path.read_bytes()
        text = payload.decode("utf-8")
        matches = list(SCENE.finditer(text))
        if len(matches) != 5:
            raise ValueError(f"{episode_id}: expected 5 scenes, found {len(matches)}")
        for index, match in enumerate(matches):
            chunk_end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
            chunk = text[match.end() : chunk_end]
            production_match = PRODUCTION.search(chunk)
            if not production_match:
                raise ValueError(f"{episode_id}-S{index + 1:02d}: missing production comment")
            fields = parse_fields(production_match.group(1))
            cast = parse_list(fields.get("cast", ""))
            props = parse_list(fields.get("props", ""))
            tags = set(parse_list(fields.get("tags", "")))
            extra_raw = fields.get("extras", "0")
            extras = extras_count(extra_raw)
            scene_number, full_location, minutes, seconds = match.groups()
            int_ext, day_night, story_location = split_location(full_location)
            unit, standing_set, secondary_units = production_unit(episode, full_location, tags)
            water = bool(tags & {"water", "water-heavy", "low-water", "storm", "shore"})
            boats = "boat" in tags
            prop_text = ",".join(props)
            weapon_blood_action = (
                "blood" in tags
                and not tags & {"underworld", "cleanup"}
                and any(token in prop_text for token in ("弓", "箭", "剑", "矛", "木杖", "刀"))
            )
            stunt = bool(
                tags & {"fight", "fight-low", "fight-map", "stunt", "stunt-low", "stunt-safe", "athletics"}
            ) or weapon_blood_action
            scene_id = f"{episode_id}-S{int(scene_number):02d}"
            scenes.append(
                {
                    "animals": animals_in(chunk),
                    "boats": boats,
                    "cast": cast,
                    "complexity": scene_score(extras, tags),
                    "creature": "creature-medium" in tags,
                    "day_night": day_night,
                    "episode": episode_id,
                    "estimated_runtime_seconds": int(minutes) * 60 + int(seconds),
                    "extras": extras,
                    "extras_declared": extra_raw,
                    "fight": "fight" in tags,
                    "hmu": hmu_states(episode, cast, tags),
                    "int_ext": int_ext,
                    "production_unit": unit,
                    "props": props,
                    "scene_id": scene_id,
                    "scene_number": int(scene_number),
                    "secondary_units": secondary_units,
                    "sfx": sfx_items(tags),
                    "source_episode_path": path.relative_to(ROOT).as_posix(),
                    "source_episode_sha256": sha256_bytes(payload),
                    "standing_set": standing_set,
                    "story_location": story_location,
                    "stunt": stunt,
                    "tags": sorted(tags),
                    "time_label": full_location.split("·")[-1],
                    "vfx": vfx_level(tags),
                    "wardrobe": wardrobe_states(episode, cast, full_location),
                    "water": water,
                }
            )
    ids = [scene["scene_id"] for scene in scenes]
    if len(scenes) != 150 or len(set(ids)) != 150:
        raise ValueError("scene coverage or uniqueness failed")
    return {
        "artifact_class": "odyssey_p3_scene_master_index",
        "episode_count": 30,
        "production_units": ["S1", "S2", "S3", "S4", "S5", "U06", "U07", "U08", "U09", "U10", "U11", "U12"],
        "scene_count": len(scenes),
        "schema_version": "1.0.0",
        "scenes": scenes,
        "status": "PASS_SCENE_MASTER_INDEX_150_OF_150",
        "standing_sets": ["S1", "S2", "S3", "S4", "S5"],
        "v2_baseline_commit": "17cbd562fae17f55ab075cc8643549cfc6a80eab",
        "v2_manifest_sha256": sha256_bytes(V2_MANIFEST.read_bytes()),
    }


def canonical_bytes(value: dict[str, object]) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    expected = canonical_bytes(build_index())
    if args.check:
        actual = OUTPUT.read_bytes()
        if actual != expected:
            raise SystemExit("SCENE_MASTER_INDEX.json is stale or noncanonical")
        print(f"PASS {sha256_bytes(actual)} {len(actual)} bytes")
        return
    OUTPUT.write_bytes(expected)
    print(f"WROTE {OUTPUT.relative_to(ROOT)} {sha256_bytes(expected)} {len(expected)} bytes")


if __name__ == "__main__":
    main()
