#!/usr/bin/env python3
"""Build the frozen P3 casting matrix and VFX/creature execution matrix."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
P3 = ROOT / "preproduction" / "odyssey_m1_p3"
INDEX = P3 / "SCENE_MASTER_INDEX.json"
SHOTS = P3 / "SHOT_LIST_MASTER.json"
CAST_OUT = P3 / "CASTING_PRIORITY_MATRIX.md"
VFX_OUT = P3 / "VFX_CREATURE_EXECUTION_MATRIX.json"

PRINCIPALS = {"奥德修斯", "佩涅洛佩", "忒勒马科斯", "雅典娜"}

MUST_UNIQUE = {
    "安提诺俄斯", "安提诺俄斯亡魂", "欧律马科斯", "安菲诺摩斯",
    "欧迈俄斯", "欧律克勒娅", "菲洛提俄斯", "墨兰提俄斯", "墨兰托",
    "拉厄耳忒斯", "涅斯托耳", "墨涅拉俄斯", "海伦", "庇西斯特拉托斯",
    "瑙西卡", "阿尔喀诺俄斯", "阿瑞忒", "得摩多科斯",
    "卡吕普索", "喀耳刻", "埃俄罗斯", "波吕斐摩斯", "波塞冬",
    "欧律洛科斯", "厄尔佩诺耳", "忒瑞西阿斯", "阿伽门农", "阿喀琉斯",
    "忒奥克吕墨诺斯",
}
CAN_DOUBLE = {
    "伊诺", "伊洛斯", "劳达玛斯", "厄刻涅俄斯", "埃及普提俄斯", "埃阿斯",
    "墨冬", "多利俄斯", "安提克勒娅", "欧佩忒斯", "菲埃克斯船长",
}
DAY_PLAYER = {
    "侦察船员", "年长船员", "斐弥俄斯", "欧律阿罗斯", "赫尔墨斯",
    "雷奥克里托斯", "雷奥得斯", "磨坊女奴",
}
VOICE_ONLY = {"宙斯声", "赫利俄斯声", "伏击者声", "海妖声"}
ENSEMBLE = {
    "三名船员", "伊萨卡亲族", "众求婚者", "伏击船员", "复原船员", "女伴们",
    "桨手", "求婚者亡魂", "洞外独眼巨人们", "猪场帮工", "船员", "莱斯特律戈涅斯人",
}
STUNT_DOUBLE = {"斯库拉局部"}

DOUBLE_GROUP = {
    "伊诺": "D01 with 安提克勒娅; EP05/EP13, face and age separation",
    "安提克勒娅": "D01 with 伊诺; maternal body language cannot echo rescue beat",
    "伊洛斯": "D02 with 欧佩忒斯; EP21/EP30, no release adjacency",
    "欧佩忒斯": "D02 with 伊洛斯; kin styling, beard and gait reset",
    "劳达玛斯": "D03 with 多利俄斯; EP08/EP30, athlete/old worker separation",
    "多利俄斯": "D03 with 劳达玛斯; age prosthetic and silhouette separation",
    "厄刻涅俄斯": "D04 with 埃及普提俄斯; EP07/EP02, distinct civic staff and palette",
    "埃及普提俄斯": "D04 with 厄刻涅俄斯; no same block or wardrobe reuse",
    "埃阿斯": "D05 with 墨冬; EP13/EP28, Underworld treatment hides no story identity",
    "墨冬": "D05 with 埃阿斯; clean living voice and herald staff",
    "菲埃克斯船长": "D06 option with one non-visible creature/stand-in contract only",
}

CREATURE_METHOD = {
    "EP09-S05": ("Cyclops threshold and first seizure", "forced-perspective performer; giant hand/foot; scaled rock", "shadow/body pass; clean cave; contact matte"),
    "EP10-S01": ("Cyclops choice-to-wait", "forced scale, practical rock, performer eyeline pole", "clean cave; scale witness; hand contact"),
    "EP10-S02": ("Nobody intoxication and stake preparation", "performer, scaled cup/stake, heat/smoke practical", "eye unit clean; smoke holdout; empty cave"),
    "EP10-S03": ("Cyclops blinding", "practical eye unit, retracting stake, performer reaction, blood tubing", "clean eye; stake no-contact; smoke; blood element"),
    "EP10-S04": ("ram-underbelly escape", "trained sheep inserts, oversized wool belly, floor-level performer hand", "clean threshold; wool contact; hand pass"),
    "EP10-S05": ("shore throw and name exposure", "partial giant silhouette, breakaway rock splash, compressed shore axis", "clean sea; rock trajectory; shoreline reaction"),
    "EP12-S01": ("Circe animal transformation", "partial prosthetics, choreographed hands/face, practical penned animals", "clean reflection; performer plate; animal safety plate"),
    "EP14-S05": ("Scylla six named grabs", "six mapped overhead rigs, partial limbs/maw, six independent safe releases", "clean deck; each rig path; empty oar stations; blood elements"),
}

MEDIUM_METHOD = {
    "EP03-S04": ("Athena departure/reveal", "match body position, practical wind and raptor pass", "clean courtyard; eye-light; departure holdout"),
    "EP05-S01": ("Hermes arrives under Calypso's roof", "practical threshold light, matched staff and environmental pause", "clean cave; Hermes entry; atmosphere"),
    "EP05-S04": ("Poseidon storm pressure", "partial raft, motion base, spray, horizon removal", "clean horizon; raft dry pass; spray pass; actor safety close"),
    "EP11-S01": ("wind made visible through custody", "practical bag deformation, knot insert, restrained air distortion", "clean terrace; bag element; cloth motion"),
    "EP11-S05": ("Laestrygonian harbor destruction", "one hero deck, scaled fragments, practical rock impacts", "clean harbor; rocks; hull breaks; survivor boat"),
    "EP12-S03": ("Circe's power fails then terms change", "cup reaction, matched hand/face transition, practical curtain movement", "clean room; cup element; transformation holdout"),
    "EP13-S01": ("Underworld boundary opens", "reflective floor, gauze depth, practical blood trench", "clean black stage; trench; crowd depth; reflection"),
    "EP13-S02": ("Tiresias gains access to blood", "selective absence, layered gauze, reflection separation", "clean trench; Tiresias; reflection; horn shadow"),
    "EP13-S03": ("mother cannot be held", "three-pass embrace separation and body absence", "Odysseus solo; Anticleia solo; overlap matte; cloth shadow"),
    "EP13-S04": ("Agamemnon testimony", "depth isolation and weapon-shadow memory fragment", "clean trench; speaker; knife/shroud element"),
    "EP13-S05": ("dead crowd closes in", "layered practical ensemble, selective edge loss", "clean trench; Achilles/Ajax; crowd groups; exit plate"),
    "EP15-S04": ("Zeus destroys the ship", "motion deck, breakaway mast, controlled strike, water elements", "clean sky/sea; dry deck; mast break; wet actor pass"),
    "EP16-S02": ("Phaeacian ship petrifies", "locked hull fragment, progressive texture, witness-led wide", "clean hull; texture references; witness crowd; water"),
    "EP16-S05": ("Athena changes access through disguise", "matched body position, costume/face blend, practical dust", "clean road; Odysseus clean; disguised pass; eye-light"),
    "EP19-S02": ("beggar form releases before Telemachus", "matched body position, practical wash and limited face blend", "clean olive background; both looks; eyeline; cloth"),
    "EP30-S01": ("dead revise the public story", "reflective black floor, root/bow shadows, layered dead ensemble", "clean Underworld; hero dead; crowd groups; shadow elements"),
}


def canonical_name(name: str) -> str:
    if name == "奥德修斯/乞丐":
        return "奥德修斯"
    if name.startswith("雅典娜/"):
        return "雅典娜"
    return name


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build_cast(index: dict) -> str:
    appearances: dict[str, dict[str, object]] = defaultdict(lambda: {"scenes": 0, "episodes": set()})
    for scene in index["scenes"]:
        for raw in scene["cast"]:
            name = canonical_name(raw)
            appearances[name]["scenes"] += 1
            appearances[name]["episodes"].add(scene["episode"])
    names = set(appearances)
    classified = PRINCIPALS | MUST_UNIQUE | CAN_DOUBLE | DAY_PLAYER | VOICE_ONLY | ENSEMBLE | STUNT_DOUBLE
    assert names == classified, (sorted(names - classified), sorted(classified - names))
    assert len(names) == 69 and len(names - PRINCIPALS) == 65
    categories = [
        ("PRINCIPAL", PRINCIPALS),
        ("MUST UNIQUE", MUST_UNIQUE),
        ("CAN DOUBLE", CAN_DOUBLE),
        ("DAY PLAYER", DAY_PLAYER),
        ("VOICE ONLY", VOICE_ONLY),
        ("ENSEMBLE", ENSEMBLE),
        ("STUNT DOUBLE", STUNT_DOUBLE),
    ]
    lines = [
        "# Casting Priority Matrix",
        "",
        "Status: `PASS_CASTING_IDENTITY_CLASSIFICATION`",
        "",
        "Count authority: `4 principal + 65 nonprincipal = 69 normalized performance identities`. Athena's disguises and Odysseus' beggar state remain the same actors. Antinous' EP30 dead return must use the Antinous actor even though it is separately credited in the scene inventory.",
        "",
        "| Classification | Count | Contract rule |",
        "|---|---:|---|",
    ]
    rules = {
        "PRINCIPAL": "series availability, chemistry, movement and continuity hold",
        "MUST UNIQUE": "one recognisable performer; no inter-role doubling",
        "CAN DOUBLE": "only the listed non-overlap pair, after camera/wardrobe test",
        "DAY PLAYER": "named and individually cast; no assumption of doubling",
        "VOICE ONLY": "recorded identity; not counted as visible ensemble",
        "ENSEMBLE": "pool booking with foreground continuity ledger",
        "STUNT DOUBLE": "technical creature/action performance, not a story-identity substitution",
    }
    for label, group in categories:
        lines.append(f"| {label} | {len(group)} | {rules[label]} |")
    lines += ["", "## Identity-level matrix", "", "| Identity | Class | Scenes | Episodes | Doubling / integrity lock |", "|---|---|---:|---|---|"]
    for label, group in categories:
        for name in sorted(group):
            data = appearances[name]
            eps = ", ".join(sorted(data["episodes"]))
            if name == "安提诺俄斯亡魂":
                lock = "same performer as 安提诺俄斯; death-state HMU, no new casting"
            elif label == "CAN DOUBLE":
                lock = DOUBLE_GROUP[name]
            elif label == "MUST UNIQUE":
                lock = "no doubling across recognition, family, command, or consequence chain"
            elif label == "ENSEMBLE":
                lock = "foreground faces tracked by pool and episode; no adjacent-block identity collision"
            elif label == "VOICE ONLY":
                lock = "unique voice print; record dry and environment layers separately"
            elif label == "STUNT DOUBLE":
                lock = "credited rig performer; face not used as a second character"
            elif label == "PRINCIPAL":
                lock = "full-series hold; disguise/state continuity belongs to this performer"
            else:
                lock = "named call; reassignment requires 1st AD + director continuity check"
            lines.append(f"| {name} | {label} | {data['scenes']} | {eps} | {lock} |")
    lines += [
        "",
        "## Supplemental doubles (not additional credited identities)",
        "",
        "| Contract | Covers | Use boundary |",
        "|---|---|---|",
        "| SD-OD-WATER | Odysseus | raft, wreck, submerged grip; face replacement prohibited in choice beats |",
        "| SD-OD-FIGHT | Odysseus | contact passes in EP10 and EP26–28; bow hand inserts remain principal/specialist matched |",
        "| SD-TE-ACTION | Telemachus | horse, boat edge, battle falls; recognition and wound reaction remain principal |",
        "| BD-AT-MATCH | Athena | transformation match body only; voice, eyes, and condition-setting beat remain principal |",
        "| SD-POLY | Polyphemus | forced-scale contact and fall; integrated with the unique creature performer |",
        "| STAND-IN-PE | Penelope | lighting/bed geometry only; no hand, loom, bow-key, or verification performance replacement |",
        "",
        "No double may cross the recognition chain, impersonate a family relation, or cause one visible foreground performer to appear as two identities within an adjacent release block.",
        "",
        "Final result: `PASS_CASTING_69_IDENTITIES_AND_SAFE_DOUBLING`.",
        "",
    ]
    return "\n".join(lines)


def build_vfx(index: dict, shots: dict) -> dict:
    index_scene_by_id = {scene["scene_id"]: scene for scene in index["scenes"]}
    by_scene: dict[str, list[str]] = defaultdict(list)
    tech_by_scene: dict[str, list[str]] = defaultdict(list)
    for shot in shots["shots"]:
        if shot["vfx"] != "NONE":
            by_scene[shot["scene_id"]].append(shot["shot_id"])
        if shot["dramatic_purpose"] == "TECHNICAL_PLATE":
            tech_by_scene[shot["scene_id"]].append(shot["shot_id"])
    rows = []
    for scene in index["scenes"]:
        sid = scene["scene_id"]
        if scene["vfx"] != "MEDIUM" and not scene["creature"]:
            continue
        if scene["creature"]:
            effect, practical, plates = CREATURE_METHOD[sid]
            tier = "CREATURE_MEDIUM_COST"
        else:
            effect, practical, plates = MEDIUM_METHOD[sid]
            tier = "MEDIUM_VFX"
        rows.append({
            "scene_id": sid,
            "episode": scene["episode"],
            "story_location": scene["story_location"],
            "tier": tier,
            "medium_plus_vfx_scene": scene["vfx"] == "MEDIUM",
            "creature_scene": scene["creature"],
            "effect": effect,
            "practical_core": practical,
            "plate_package": [x.strip() for x in plates.split(";")],
            "vfx_shot_ids": sorted(set(by_scene[sid] + (tech_by_scene[sid] if scene["creature"] else []))),
            "technical_plate_shot_ids": tech_by_scene[sid],
            "full_cg_hero_creature_required": False,
            "actor_eyeline_reference_required": True,
            "physical_contact_reference_required": scene["creature"] or scene["stunt"],
            "clean_plate_required": True,
            "sound_leads_reveal": scene["creature"] or "underworld" in scene["tags"] or "storm" in scene["tags"],
            "choice_visibility_lock": "effect may alter conditions, scale or access; it may not obscure the human choice or consequence",
            "safety_owner": "STUNT/VFX SUPERVISOR" if scene["stunt"] or scene["creature"] else "VFX SUPERVISOR",
            "production_unit": scene["production_unit"],
        })
    assert len([r for r in rows if r["medium_plus_vfx_scene"]]) == 16
    assert len([r for r in rows if r["creature_scene"]]) == 8
    assert len(rows) == 24
    return {
        "artifact_class": "odyssey_p3_vfx_creature_execution_matrix",
        "schema_version": "1.0.0",
        "status": "PASS_16_MEDIUM_PLUS_AND_8_CREATURE_SCENES",
        "source_scene_index_sha256": sha(INDEX),
        "source_shot_list_sha256": sha(SHOTS),
        "medium_plus_vfx_scene_count": 16,
        "creature_scene_count": 8,
        "execution_scene_count": 24,
        "matrix_vfx_shot_count": len({shot_id for row in rows for shot_id in row["vfx_shot_ids"]}),
        "series_planned_vfx_shot_count": len({
            shot["shot_id"] for shot in shots["shots"]
            if shot["vfx"] != "NONE" or (
                index_scene_by_id[shot["scene_id"]]["creature"]
                and shot["dramatic_purpose"] == "TECHNICAL_PLATE"
            )
        }),
        "full_cg_hero_creature_required": False,
        "rows": rows,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    index = json.loads(INDEX.read_text())
    shots = json.loads(SHOTS.read_text())
    cast_bytes = build_cast(index).encode()
    vfx_bytes = (json.dumps(build_vfx(index, shots), ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode()
    if args.check:
        assert CAST_OUT.read_bytes() == cast_bytes
        assert VFX_OUT.read_bytes() == vfx_bytes
        print(f"PASS cast_sha={hashlib.sha256(cast_bytes).hexdigest()} vfx_sha={hashlib.sha256(vfx_bytes).hexdigest()}")
    else:
        CAST_OUT.write_bytes(cast_bytes)
        VFX_OUT.write_bytes(vfx_bytes)
        print(f"WROTE cast={CAST_OUT.name} vfx={VFX_OUT.name}")


if __name__ == "__main__":
    main()
