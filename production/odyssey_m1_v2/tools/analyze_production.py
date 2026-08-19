#!/usr/bin/env python3
"""Read-only production inventory for the Odyssey M1 V2 screenplay."""

from __future__ import annotations

import collections
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
EPISODE_DIR = ROOT / "scripts" / "odyssey_m1_v2" / "episodes"
SCENE = re.compile(r"^## 场\s*(\d+)｜([^｜]+)｜约\s*(\d+)'(\d+)\"$", re.MULTILINE)
PRODUCTION = re.compile(r"<!-- production: (.+?) -->")

PRINCIPAL_IDENTITIES = {"奥德修斯", "佩涅洛佩", "忒勒马科斯", "雅典娜"}
IDENTITY_ALIASES = {
    "奥德修斯/乞丐": "奥德修斯",
    "雅典娜/女伴": "雅典娜",
    "雅典娜/少年": "雅典娜",
    "雅典娜/提灯女孩": "雅典娜",
    "雅典娜/牧童": "雅典娜",
    "雅典娜/门忒斯": "雅典娜",
    "雅典娜/门托耳": "雅典娜",
    "宙斯声": "宙斯",
    "赫利俄斯声": "赫利俄斯",
    "海妖声": "海妖",
    "斯库拉局部": "斯库拉",
}


def parse_fields(value: str) -> dict[str, str]:
    fields = {}
    for item in value.split(";"):
        key, separator, field_value = item.strip().partition("=")
        if separator:
            fields[key] = field_value.strip()
    return fields


def parse_list(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


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


def main() -> None:
    scenes = []
    cast_appearances: collections.Counter[str] = collections.Counter()
    props: collections.Counter[str] = collections.Counter()
    tags: collections.Counter[str] = collections.Counter()
    locations: collections.Counter[str] = collections.Counter()

    for number in range(1, 31):
        episode_id = f"EP{number:02d}"
        text = (EPISODE_DIR / f"{episode_id}.md").read_text(encoding="utf-8")
        scene_matches = list(SCENE.finditer(text))
        production_matches = list(PRODUCTION.finditer(text))
        if len(scene_matches) != 5 or len(production_matches) != 5:
            raise ValueError(
                f"{episode_id}: expected five scenes and production comments, "
                f"found {len(scene_matches)} and {len(production_matches)}"
            )

        for scene_match, production_match in zip(scene_matches, production_matches, strict=True):
            scene_number, location, minutes, seconds = scene_match.groups()
            fields = parse_fields(production_match.group(1))
            cast_raw = parse_list(fields.get("cast", ""))
            cast = [IDENTITY_ALIASES.get(name, name) for name in cast_raw]
            scene_props = parse_list(fields.get("props", ""))
            scene_tags = set(parse_list(fields.get("tags", "")))
            extras_values = [int(value) for value in re.findall(r"\d+", fields.get("extras", "0"))]
            extras = max(extras_values, default=0)
            score = scene_score(extras, scene_tags)
            locations[location] += 1
            cast_appearances.update(set(cast))
            props.update(scene_props)
            tags.update(scene_tags)
            scenes.append(
                {
                    "episode_id": episode_id,
                    "scene": int(scene_number),
                    "location": location,
                    "runtime_seconds": int(minutes) * 60 + int(seconds),
                    "cast": cast,
                    "cast_raw": cast_raw,
                    "extras": extras,
                    "props": scene_props,
                    "tags": sorted(scene_tags),
                    "complexity_score": score,
                }
            )

    cast_identities = set(cast_appearances)
    principal = sorted(cast_identities & PRINCIPAL_IDENTITIES)
    supporting = sorted(cast_identities - PRINCIPAL_IDENTITIES)
    episode_scores: dict[str, dict[str, int]] = {}
    for number in range(1, 31):
        episode_id = f"EP{number:02d}"
        episode_scenes = [scene for scene in scenes if scene["episode_id"] == episode_id]
        episode_scores[episode_id] = {
            "peak": max(scene["complexity_score"] for scene in episode_scenes),
            "total": sum(scene["complexity_score"] for scene in episode_scenes),
        }

    report = {
        "episodes": 30,
        "scenes": len(scenes),
        "unique_location_labels": len(locations),
        "location_counts": dict(locations.most_common()),
        "principal_cast": principal,
        "principal_cast_count": len(principal),
        "supporting_cast": supporting,
        "supporting_cast_count": len(supporting),
        "cast_scene_appearances": dict(cast_appearances.most_common()),
        "props": dict(props.most_common()),
        "tag_counts": dict(tags.most_common()),
        "extra_heavy_scenes": sum(scene["extras"] >= 12 for scene in scenes),
        "fight_scenes": sum("fight" in scene["tags"] for scene in scenes),
        "water_heavy_scenes": sum(
            bool(set(scene["tags"]) & {"water-heavy", "storm"}) for scene in scenes
        ),
        "vfx_heavy_scenes": sum(
            bool(set(scene["tags"]) & {"vfx-medium", "divine-medium", "underworld"})
            for scene in scenes
        ),
        "creature_scenes": sum("creature-medium" in scene["tags"] for scene in scenes),
        "high_complexity_scenes": sum(scene["complexity_score"] >= 7 for scene in scenes),
        "high_cost_episodes": [
            episode_id
            for episode_id, score in episode_scores.items()
            if score["peak"] >= 7 or score["total"] >= 24
        ],
        "episode_complexity": episode_scores,
        "scene_inventory": scenes,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
