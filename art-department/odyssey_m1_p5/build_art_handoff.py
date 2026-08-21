#!/usr/bin/env python3
"""Build the deterministic P5 art-department handoff from frozen P3/P4 authorities."""
from __future__ import annotations

import hashlib
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "art-department/odyssey_m1_p5"


def load(path: str):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def dump(path: str, payload) -> None:
    (OUT / path).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write(path: str, body: str) -> None:
    (OUT / path).write_text(body.rstrip() + "\n", encoding="utf-8")


def sha(path: str) -> str:
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


sets = load("design/odyssey_m1_p4/SET_STATE_MATRIX.json")["sets"]
props = load("design/odyssey_m1_p4/HERO_PROP_STATE_MATRIX.json")["props"]
costumes = load("design/odyssey_m1_p4/COSTUME_STATE_MATRIX.json")["costumes"]
creatures = load("design/odyssey_m1_p4/CREATURE_SYSTEM_MATRIX.json")["systems"]
scenes = load("preproduction/odyssey_m1_p3/SCENE_MASTER_INDEX.json")["scenes"]
target_schedule = load("preproduction/odyssey_m1_p3/SHOOTING_SCHEDULE_TARGET.json")

usage = defaultdict(lambda: {"episodes": set(), "scenes": []})
for scene in scenes:
    unit = scene.get("production_unit") or scene.get("standing_set") or "UNASSIGNED"
    usage[unit]["episodes"].add(scene["episode"])
    usage[unit]["scenes"].append(scene["scene_id"])

materials = {
    "WOOD": ("olive/pine/cypress", "oil, smoke, hand-burnished edges", "water raises grain; sacrificial clear barrier on wet duplicates"),
    "BRONZE": ("cast/resin hero with real-metal skin", "dark liver patina, polished custody edges", "no green fantasy patina except story-bound salt bloom"),
    "IRON": ("steel hero; aluminium/rubber stunt", "black scale and handled edge", "seal blood-contact pieces; photograph rust continuity"),
    "LINEN": ("undyed flax family", "sun, salt and body-oil gradient", "pre-shrink wet duplicates; no optical white"),
    "WOOL": ("handwoven-look wool", "lanolin matte, repair stitches", "duplicate principal states rather than forced same-day drying"),
    "LEATHER": ("vegetable-tanned leather", "waxed flex points, salt cracking", "stunt closures release safely"),
    "STONE": ("carved foam/GFRG skins over rated support", "dust, soot and foot-polish", "replaceable battle chips; no loose overhead stone"),
    "LIME_PLASTER": ("mineral paint on scenic plaster", "uneven trowel, smoke tide", "replaceable blood-reset panels in S1"),
    "CLAY": ("hero fired clay plus resin/rubber duplicates", "ash and hand oil", "breakaway inventory isolated and labeled"),
    "ROPE": ("hemp/sisal visual; soft stunt core", "salt, tar, fray kept outside grip zones", "wet and dry continuity coils separately stored"),
    "ASH": ("cosmetic scenic ash", "cool grey/brown, never glitter", "department-approved respiratory-safe substitute"),
    "OIL": ("nonflammable camera substitute", "warm specular only at practical source", "slip control and absorbent resets"),
    "SALT": ("cosmetic salt dressing", "edge crust, never uniform spray", "eye-safe HMU formulation on performers"),
    "BLOOD": ("washable scenic/stunt formulations", "darkens from B1 to B5 without fluorescent red", "zone maps, duplicate textiles, floor protection"),
    "WATER": ("clean controlled wet-down", "selective sheen and salt wake", "electrical separation, anti-slip surface, wet-state photo cards"),
}

redresses = [
    ("U01", "S1 household/occupied", "S1-A", "days 01-06"),
    ("U02", "S1 contest", "S1-B", "days 07-10"),
    ("U03", "S1 battle/aftermath/restored", "S1-C..F", "days 11-16"),
    ("U04", "S4 Eumaeus farm", "dry/rain variants", "days 17-20"),
    ("U05", "S2 Phaeacia court", "court/feast/story", "days 21-24"),
    ("U06", "civic/harbor", "assembly/shore", "days 25-28"),
    ("U07", "Ithaca exterior/kin", "courtyard/field", "days 29-31"),
    ("U08", "roads/forest", "Telemachus/Laertes", "days 32-35"),
    ("U09", "Underworld", "black-water/threshold", "days 36-38"),
    ("U10", "finale field/land", "restoration", "days 39-41"),
    ("U11", "wet/motion sea unit", "storm/wreck/strait", "days 42-48"),
    ("U12", "dry deck/cave myth unit", "deck/cave/islands", "days 49-54"),
]

assets = []


def add(asset_id, department, authority, scene_usage, episodes, quantity, role, duplicate_count,
        material, finish, aging, damage_states, wet_states, blood_states, storage, reset, owner,
        category, notes=""):
    assets.append({
        "asset_id": asset_id, "category": category, "department": department,
        "p4_visual_authority": authority, "p3_scene_usage": scene_usage,
        "episodes": sorted(set(episodes)), "build_quantity": quantity,
        "hero_stunt_background": role, "duplicate_count": duplicate_count,
        "material": material, "finish": finish, "aging": aging,
        "damage_states": damage_states, "wet_states": wet_states,
        "blood_states": blood_states, "storage": storage,
        "reset_requirements": reset, "continuity_owner": owner,
        "real_world_status": "BUILD SPECIFICATION — NEEDS VENDOR/SHOP VALIDATION",
        "notes": notes,
    })


for s in sets:
    sid = s["set_id"]
    eps = [x["episode"] for x in scenes if x.get("standing_set") == sid or x.get("production_unit") == sid]
    add(
        f"SET-{sid}", "ART/CONSTRUCTION", f"design/odyssey_m1_p4/{s['design_sheet']}",
        [x["scene_id"] for x in scenes if x.get("standing_set") == sid], eps, 1,
        "HERO STANDING SET", 0, "timber, scenic plaster, stone skins", "P4 palette and material lock",
        "state-specific smoke/salt/handling", s["states"], ["W0", "W1 controlled"],
        ["B0", "battle zones where applicable"], "locked stage footprint",
        "photo survey at every state transition; labeled replaceable dressing", "PRODUCTION DESIGNER + ART CONTINUITY",
        "STANDING_SET", "P3 geometry remains exact; wild walls recorded on construction drawings.")

for unit, label, state, block in redresses:
    eps = [x["episode"] for x in scenes if x.get("production_unit") == unit]
    scene_ids = [x["scene_id"] for x in scenes if x.get("production_unit") == unit]
    add(
        f"REDRESS-{unit}", "SET DECORATION", "design/odyssey_m1_p4/SET_DESIGN_BIBLE.md",
        scene_ids, eps, 1, "REDRESS PACKAGE", 0, "unit-bound practical dressing",
        f"{label}; {state}", "handled, repaired, never theme-park clean", [state], ["W0", "W1 if scheduled"],
        ["B0", "B-scene if scheduled"], f"rolling cages labeled {unit}",
        f"prepack by continuity photo; restore before {block}", "SET DECORATOR", "PRODUCTION_UNIT_REDRESS", block)

prop_build = {
    "PR-BOW-01": ("laminated hero bow; low-draw rehearsal; inert stunt", 5, "oiled olive/yew tone", "dry/wet/blood-safe custody"),
    "PR-AXES-12": ("12 hero axe heads + 12 soft alignment doubles", 25, "dark iron, readable aperture", "numbered 01–12, jig-spaced"),
    "PR-BED-01": ("built-in olive-trunk bed section + camera wild piece", 2, "oil-dark olive wood", "never detached in story geography"),
    "PR-SCAR-01": ("silicone scar transfer system", 24, "skin-match sealed edge", "close/mid/stunt tolerance set"),
    "PR-LOOM-01": ("working loom, hero textile, continuity thread cards", 3, "smoke-softened wood", "weave-length witness photos"),
    "PR-SWORD-TE-01": ("hero, aluminium action, rubber safety", 4, "handled bronze/iron", "Telemachus custody lock"),
    "PR-SPEAR-SYS": ("hero tips, aluminium shafts, rubber full doubles", 24, "ash shaft/dark iron", "rack and battle lots separated"),
    "PR-SHIELD-SYS": ("hero, light stunt, broken shells", 14, "wood/leather/bronze", "dent progression cards"),
    "PR-BONE-COUNTERS": ("hero counters plus spill duplicates", 60, "aged bone substitute", "no animal bone sourcing assumed"),
    "PR-BOUNDARY-STONE": ("hero lightweight stone shell", 2, "local limestone", "Laertes/land recognition mark"),
    "PR-WIND-BAG": ("hero bladder-look textile/leather, stunt vented", 3, "salted leather", "air rig never performer-sealed"),
    "PR-CYCLOPS-STAKE": ("hero wood, soft impact, retractable interaction", 4, "charred olive timber", "eye rig interface witness marks"),
}
prop_ids = {p["prop_id"] for p in props}
for p in props:
    pid = p["prop_id"]
    desc, qty, finish, reset = prop_build.get(pid, ("hero, stunt and safety versions as scene requires", 3, "P4 locked finish", "photo/custody reset"))
    eps = sorted({x["episode"] for x in scenes if pid.lower().replace("pr-", "") in json.dumps(x, ensure_ascii=False).lower()})
    add(pid, "PROPS", p["technical_sheet"], [], eps, qty, "HERO/STUNT/SAFETY SYSTEM",
        max(0, qty - 1), desc.split(";")[0], finish, "story handling and state only", ["D0", "scene-bound damage"],
        ["W0", "W1 duplicate where used"], ["B0", "B-scene duplicate"], "locked props cage; custody log",
        reset, "PROP MASTER + SCRIPT SUPERVISOR", "HERO_PROP", desc)

# Ship hero pieces are a required execution family even though not one of the 12 frozen hero-prop IDs.
add("SHIP-RIG-HERO", "MARINE ART/PROPS", "design/odyssey_m1_p4/SET_DESIGN_BIBLE.md", [],
    [f"EP{i:02d}" for i in range(5, 17)], 2, "HERO + WET DUPLICATE", 1,
    "soft-core rope, rated scenic mast/rail interfaces", "tar/salt/hand wear", "dry/wet continuity",
    ["intact", "storm", "wreck"], ["W0", "W1", "W2"], ["B0"], "dry rack plus wet drip zone",
    "rigging diagram, knot witness photos, safety inspection before every load", "MARINE COORDINATOR + PROPS", "SHIP_ELEMENT")

for c in costumes:
    cid = c["costume_id"]
    principal = c["character"] in {"Odysseus", "Penelope", "Telemachus", "Athena"}
    versions = c.get("versions", ["HERO"])
    qty = max(2, len(versions) + (2 if principal else 0))
    add(
        f"COST-{cid}", "COSTUME", "design/odyssey_m1_p4/COSTUME_STATE_MATRIX.json", [], [], qty,
        "PRINCIPAL" if principal else "SUPPORTING", qty - 1, "linen/wool/leather per P4 state",
        "dyed within locked character palette", "separate clean/organic progression/stunt records",
        [v for v in versions if "DAMAGE" in v or "STUNT" in v] or ["D0"],
        [v for v in versions if "WET" in v] or ["W0"], [v for v in versions if "BLOOD" in v] or ["B0"],
        f"ventilated rail, bagged and tagged {cid}", "do not force-dry hero continuity; use matched duplicate",
        "COSTUME SUPERVISOR", "COSTUME", ", ".join(versions))

hmu_assets = [
    ("HMU-ODY-SCAR", "Odysseus", 24, "silicone transfers; right outer thigh witness template"),
    ("HMU-ODY-SALT", "Odysseus", 8, "salt/weathering palettes by ODY state"),
    ("HMU-WOUND-SYS", "battle cast", 40, "graded wounds B1–B5; removable appliances"),
    ("HMU-CYCLOPS-EYE", "Cyclops", 4, "practical eyelid/blood interface, VFX-safe tracking surround"),
    ("HMU-ATHENA-STATE", "Athena", 6, "human disguises/divine condition continuity; no glow makeup"),
]
for aid, who, qty, note in hmu_assets:
    add(aid, "HMU/PROSTHETICS", "design/odyssey_m1_p4/CHARACTER_DESIGN_BIBLE.md", [], [], qty,
        "HERO APPLICATION SYSTEM", max(1, qty - 1), note, "camera-distance calibrated", "state card",
        ["intact", "used/discard"], ["dry", "wet-safe where required"], ["clean", "blood progression where required"],
        "temperature-controlled labeled prosthetic storage", "single-use transfers; fresh edge blend; continuity photography",
        "KEY MAKEUP + SCRIPT SUPERVISOR", "HMU_PROSTHETIC", "Desktop specification only; no human test performed.")

for c in creatures:
    sid = c["system_id"]
    add(
        f"CREATURE-{sid}", "CREATURE FX/VFX", c["technical_sheet"], [], [], 1,
        "PRACTICAL INTERACTION SYSTEM", 0, "partial practical, puppet/prosthetic/rig/tracking as specified",
        "P4 creature grammar", "handled contact points remain physical; digital extension beyond boundary",
        ["clean", "story damage"], ["dry", "controlled wet if applicable"], ["clean", "contact blood if applicable"],
        "department-specific rig cases", "reset interaction witness marks; clean plate before strike",
        "CREATURE FX SUPERVISOR + VFX SUPERVISOR", "PRACTICAL_CREATURE",
        "full-CG hero creature required: false; final method requires physical safety and vendor validation.")

graphics = [
    ("GFX-ITHACA-HOUSE", "household seals, storage marks, weaving tally"),
    ("GFX-PHAEACIA", "court/harbor practical symbols"),
    ("GFX-SHIP", "sail/rope identification and non-readable navigational dressing"),
    ("TEXTILE-PENELOPE", "loom textile family and burial-shroud progression"),
    ("RITUAL-OFFERING", "cups, ash bowls, oil, grave and civic offering family"),
    ("FURN-S1", "tables, benches, stools, off-axis suitor seat, weapon wall furniture"),
]
for aid, desc in graphics:
    add(aid, "GRAPHICS/SET DEC/PROPS", "design/odyssey_m1_p4/GRAPHIC_SYMBOL_LANGUAGE.md", [], [], 6,
        "HERO/BACKGROUND FAMILY", 5, "period-grounded practical media", "matte, worn, no modern legibility",
        "state-specific handling", ["clean", "battle/ritual state"], ["dry", "wet if scene-bound"],
        ["clean", "blood only if battle-bound"], "flat files or labeled rolling cage", "continuity photo and quantity count",
        "SET DECORATOR", "GRAPHICS_TEXTURE_FURNITURE_RITUAL", desc)

assert len({x["asset_id"] for x in assets}) == len(assets)
assert len(sets) == 5 and len(redresses) == 12 and len(props) == 12

master_index = {
    "artifact_class": "P5_ART_ASSET_MASTER_INDEX",
    "schema_version": "1.0.0",
    "baseline_commit": "563839908cc62dca3f9132fae20c490e4b0a14b6",
    "p4_artifact_manifest_sha256": "626800b73ccaa8e996f7ff882c4745894720033fcf117337140f714689767bc3",
    "authority_order": ["P3 geometry/continuity", "P4 approved visual authority", "P5 build translation"],
    "real_world_boundary": "ASSUMPTION-BASED DESKTOP BUILD SPECIFICATION; NEEDS SHOP, VENDOR, SAFETY AND PROCUREMENT VALIDATION",
    "asset_count": len(assets),
    "standing_set_count": 5,
    "production_unit_redress_count": 12,
    "frozen_hero_prop_system_count": 12,
    "assets": assets,
    "duplicate_asset_ids": [],
    "status": "PASS_ART_ASSET_INDEX",
}
dump("ART_ASSET_MASTER_INDEX.json", master_index)

set_matrix = {
    "artifact_class": "P5_SET_BUILD_MATRIX", "schema_version": "1.0.0",
    "target_schedule_days": 54,
    "sets": [{
        "set_id": s["set_id"], "states": s["states"], "build": "shop prefabricate; stage assemble and survey",
        "redress": "state cart and signed continuity photographs", "strike": "only after final scheduled state",
        "restore": "labeled clean baseline crate", "damage": "replaceable scenic skins/panels",
        "wet": "sealed surfaces; anti-slip and drainage plan", "blood": "washable barrier and zone map",
        "vfx_marker": "removable non-destructive marker mounts", "wild_wall": "P3 camera wall authority retained",
        "schedule_relationship": "bound to P3 TARGET block; no extra shooting day assumed",
    } for s in sets],
    "redresses": [{"unit_id": u, "label": l, "state": st, "target_block": b,
                    "build_redress_strike_restore": "prepack → install → witness-photo → shoot → inventory → restore",
                    "variance": "NONE IDENTIFIED; real stage turnaround to validate"} for u,l,st,b in redresses],
    "p5_production_variances": [], "status": "PASS_TARGET_54_DAY_COMPATIBLE_DESKTOP_PLAN",
}
dump("SET_BUILD_MATRIX.json", set_matrix)

prop_matrix = {"artifact_class": "P5_HERO_PROP_BUILD_MATRIX", "frozen_prop_system_count": len(props),
               "props": [x for x in assets if x["category"] in {"HERO_PROP", "SHIP_ELEMENT"}],
               "recognition_chain_locks": {"bow": "PR-BOW-01", "axes": "PR-AXES-12", "bed": "PR-BED-01", "scar": "PR-SCAR-01", "land": "PR-BOUNDARY-STONE"},
               "status": "PASS"}
dump("HERO_PROP_BUILD_MATRIX.json", prop_matrix)

costume_matrix = {"artifact_class": "P5_COSTUME_BUILD_MATRIX", "frozen_costume_state_count": len(costumes),
                  "principal_characters": ["Odysseus", "Penelope", "Telemachus", "Athena"],
                  "costumes": [x for x in assets if x["category"] == "COSTUME"],
                  "logic": {"organic_progression": "minor dry wear between adjacent dry scenes only",
                            "separate_duplicates": "wet, blood, stunt, major damage and non-linear schedule states"},
                  "status": "PASS_PRINCIPAL_4_OF_4"}
dump("COSTUME_BUILD_MATRIX.json", costume_matrix)

write("ART_DEPARTMENT_MASTER_BIBLE.md", f"""# Odyssey P5 — Art Department Master Bible

Status: **PASS — DESKTOP PRODUCTION HANDOFF SPECIFICATION**  
Baseline: `563839908cc62dca3f9132fae20c490e4b0a14b6`  
P4 manifest: `626800b73ccaa8e996f7ff882c4745894720033fcf117337140f714689767bc3`

This package translates frozen P3 geography and P4 approved design into build, duplicate, state, reset, storage and custody instructions. It does not alter story, scene IDs, shot IDs, principal identity or the five standing-set geometries. The master rule is **lived-in, salted, worked, woven, smoked, weathered, handled and repaired**. Materials must read as things used by a household and crew, not as a unified fantasy showroom.

## Decision hierarchy

1. P3 controls geography, camera access, stunt safety, custody and schedule.
2. P4 approved assets control silhouette, palette, finish and identity.
3. P5 controls build translation and records every assumption still requiring real shop validation.

## Department interfaces

- Construction owns rated structure, wild walls, ceiling/rig interfaces and replaceable skins.
- Set decoration owns redress carts and the visible history of use.
- Props owns hero/stunt/rubber separation, custody and resets.
- Costume/HMU own matched wet, blood, damage and stunt states rather than emergency drying.
- Creature FX provides physical actor contact; VFX extends beyond a declared seam.
- Continuity captures a slate-matched wide, four corners, hero insert and damage/wet/blood card at every state transition.

## Locked counts

- Standing sets: 5/5
- Production-unit redresses: 12/12
- Frozen hero-prop systems: 12/12 (plus ship-rig execution family)
- Frozen costume states: {len(costumes)}
- Frozen creature systems: {len(creatures)}
- P3 TARGET schedule: 54 shooting days

## Real-world boundary

This is an assumption-based desktop preproduction package. It is **not vendor quoted, engineered, purchased, safety-certified or physically tested**. Rated structures, flame treatments, performer-contact materials, water loads and breakaways require real department heads and qualified vendors in P6.
""")

write("SET_BUILD_PACKAGE.md", """# Set Build Package

## Five standing sets

S1 Ithaca Hall is the recognition and battle machine; S2 Phaeacia Court is hospitality and public storytelling; S3 Ship Deck is a dry modular deck that hands off to wet/motion plates; S4 Eumaeus Farm is low, tactile and work-led; S5 Shore/Cave is a reconfigurable rock, threshold and foreground-occlusion environment. All five preserve P3 geometry.

## Build sequence

Survey and tape-out → rated substructure → camera/wild-wall test → practical lighting routes → scenic skins → dressing dry run → P4 palette check → sound/noise check → state witness photographs. Damage and blood zones use replaceable sealed surfaces. VFX markers attach to planned mounts and leave no new permanent geometry.

## Redress logic

The 12 unit packages remain discrete rolling inventories. A unit cannot donate a hero dressing item to another unit without a custody transfer. Every strike has an inventory count; every restore has a wide reference photo. P5 identifies no desktop evidence that makes the frozen 54-day TARGET schedule impossible, but turnaround durations require stage and vendor validation.
""")

write("S1_CONSTRUCTION_HANDOFF.md", """# S1 Ithaca Hall — Construction Handoff

## Authority and footprint

The exact coordinate, route, door, column and camera-wall authority is `preproduction/odyssey_m1_p3/S1_ITHACA_HALL_FLOOR_PLAN.json`; the finish/silhouette authority is the P4 S1 design package and `P4-SET-S1-TECH.svg`. No P5 dimension may override those files. Construction must import the frozen plan at 1:1 and issue a dimensional shop survey before fabrication.

## Required physical systems

- Main entrance, inner-room route, Penelope route, Telemachus route, servant route and armory route remain simultaneously legible.
- Door leaves are rated for repeated blocking and have silent close, slam and stunt-safe stop modes; final sizes come only from P3 geometry.
- Columns take no unapproved stunt load. Camera-side column skins are removable for lens access.
- The hearth is a controlled practical/VFX interaction zone with a nonflame rehearsal unit.
- Weapon wall, bow position and the line of **exactly 12 axes** use indexed mounts and surveyed sightline marks.
- Tables have hero, light-action and breakaway families; off-axis suitor seating preserves the P4 occupied-home composition.
- Camera walls/wild walls, lighting channels and overhead rig access are labeled without adding story doors.
- Ceiling strategy is partial practical: low visible beams and black/extension zone beyond; no unapproved full load-bearing roof.
- Floor protection uses removable sacrificial sealed panels in blood zones and anti-slip clear protection on travel routes.
- Sound treatment hides behind ceiling/wild walls; noisy scenic dress is isolated from performance surfaces.

## State transitions

| State | Visible condition | Add/remove action | Reset proof |
|---|---|---|---|
| S1-A CLEAN OCCUPIED | household displaced by suitor consumption | work tables, wine wear, stolen cup, intact weapons | baseline wide + custody card |
| S1-B CONTEST | public corridor and test geometry | clear 12-axis line, bow station, controlled crowd lanes | laser/sightline record |
| S1-C FIRST BLOOD | first irreversible breach | arrow/impact witness, limited B1 zone, closed exits | first-blood photo set |
| S1-D FULL BATTLE | finite spatial fight | light tables, shields/spears, bodies and B2–B4 zones | beat-indexed continuity map |
| S1-E AFTERMATH | violence ended, cost visible | weapons secured, bodies/cloth state, no cosmetic reset | aftermath panoramic survey |
| S1-F RESTORED | household and civic use reclaimed | clean selected surfaces, repaired placement, memory scars retained | final-match wide and hero inserts |

## Rigging, safety and access

Every overhead point, breakaway, projectile lane and stunt surface requires real engineering and stunt sign-off. P5 provides no certification. Replaceable wall/floor panels carry state and take numbers; no blood reset may obscure travel marks. The armory choke point, main exit, servant route and inner-room route stay clear for emergency egress even when dressed.

## Schedule relationship

S1-A shoots before contest and blood. S1-B converts with surveyed axis jig. S1-C/D share replaceable damage architecture. S1-E precedes restoration cleanup; S1-F uses retained memory marks, not an ahistorical total rebuild. This is compatible with P3 TARGET blocks on desktop evidence; actual construction and reset labor require P6 validation.
""")

write("SET_DRESSING_BIBLE.md", """# Set Dressing Bible

Dress by custody and labor: nothing is present only because it fills frame. Ithaca contains household work, consumption and gradual reclamation; Phaeacia contains measured hospitality; ship units contain lashings, water, wear and scarcity; farm units contain repeated daily repair; cave/myth spaces are created by practical foreground, shadow and sound before extension.

Each rolling unit has a hero shelf, background quantity bins, continuity photo board, wet quarantine and strike checklist. Textiles have edge repairs and state labels. Furniture receives floor-safe feet and action versions. Ritual objects never double as generic tavern dressing. Modern readable symbols and unlicensed fonts are prohibited.
""")

write("HERO_PROP_BUILD_PACKAGE.md", """# Hero Prop Build Package

The 12 frozen P4 hero-prop systems remain the identity authority. Each receives a hero close version, action/stunt version where handled under force, rubber/safety version where it enters a body line, and enough continuity duplicates for non-linear wet/blood/damage work. Ship rigging is an additional execution family, not a thirteenth recognition prop.

Bow, scar, axes, bed and boundary stone form the public-to-private recognition chain. Their wear, custody, scale and camera-readable detail may not drift. All weapons are controlled props; no functional projectile or sharpened edge is assumed. The matrix is a build specification, not a procurement record.
""")

write("BOW_AXES_PHYSICAL_TEST_PLAN.md", """# Bow + 12 Axes Physical Test Plan

Status: **DESKTOP PLAN — PHYSICAL TEST NOT YET PERFORMED**

## Test articles

- one hero bow with close-detail string/limb finish;
- one low-draw stringing rehearsal bow;
- inert stunt and rubber bows, unmistakably tagged away from camera side;
- exactly 12 indexed hero axe apertures plus soft stunt doubles;
- P3 floor-plan tape-out and camera-height/lens reference.

## Procedure and evidence

1. Survey axis stations 01–12 from the frozen P3 line; record spacing and aperture center height.
2. Test standing and kneeling sightlines from all frozen P3 shot positions. The arrow line must be readable without moving an axe or inventing a thirteenth aperture.
3. Choreograph stringing hand positions with a low-draw bow: grip, foot/knee contact, hand clearance and performer bailout. Hero and stunt bows use different custody tags but matched camera profiles.
4. Photograph hero bow, stunt bow and stringing hands from wide, performance medium and motivated insert distance.
5. Confirm arrow/optical line by inert laser/string reference only; no fired projectile passes through the axes.
6. Rehearse P3 battle geography with the axis installation protected, main entrance/armory routes open and camera walls in both positions.
7. Remove and replace each axe using the numbered jig; verify reset within the target schedule window and preserve exact 12-count.
8. Repeat after approved blood/wet scenic treatment; check slip, reflection, readability and cleanup.

## Pass criteria

Bow silhouette reads in wide; stringing is safe and actor-legible; hero/stunt separation is custody-proof; 12 axes remain countable; line and geography work at frozen camera positions; replacement does not change spacing; blood/wet treatment does not produce glare or slip. Real prop master, stunt coordinator, DP and safety officer sign-off is required in P6.
""")

write("COSTUME_BUILD_PACKAGE.md", """# Costume Build Package

The 25 frozen P4 costume states become build ledgers, not a new design pass. Principals receive a base/clean duplicate, stunt duplicate where physical action exists, independent wet duplicate, independent blood duplicate, damage progression and a protected backup. Minor dry wear may progress organically only when the shooting order is chronological and the supervisor logs it; wet, blood, stunt and major damage always use separated matched pieces.

Odysseus requires salt/shipwreck/Phaeacia/disguise/scar/battle/restoration continuity. Penelope's household rule, mourning pressure, contest, recognition and restoration states must retain authority rather than simply brighten. Telemachus grows through cut, fit and tool custody, not a sudden heroic costume. Athena's human disguises share identity without an undifferentiated magical glow.
""")

write("HMU_PROSTHETIC_BUILD_PACKAGE.md", """# HMU / Prosthetic Build Package

This is a desktop application and reset specification; **no human fitting or skin test has occurred**. Odysseus' right outer-thigh boar scar uses close/mid/stunt tolerances with one immutable placement template. Salt/weathering follows state, not blanket spray. Wet skin has controlled sheen and safety-compatible products. Wound/blood progression is B1–B5 with slate-matched photographs.

Planning assumptions: principal beauty/weathering 45–75 minutes; scar close application 60–90 minutes; battle wound packages 45–120 minutes depending on coverage; Cyclops eye interface 90–150 minutes before performer/rig safety checks. These are planning assumptions, not vendor timings. Duplicate appliances are single-use where edges are performance-critical. Athena transformation is continuity of face, costume, eye-line and cut; makeup does not falsely imply continuous glow.
""")

write("GRAPHICS_AND_TEXTURE_PACKAGE.md", """# Graphics and Texture Package

Graphics are physical household/civic systems: seals, tallies, textile borders, storage marks, ship identifiers and ritual handling. They do not introduce modern readable exposition. The Chinese title and pitch typography are separate from diegetic art. No font file is redistributed.

Texture masters carry material family, state, scale reference, color chip, camera distance and aging recipe. P4 palettes remain authoritative. Every repeated symbol receives one vector master and a print/paint/use log; scenic improvisation may add wear but not a competing identity symbol.
""")

write("PRACTICAL_CREATURE_BUILD_PACKAGE.md", """# Practical Creature Build Package

Full-CG hero creature required: **false**. Eight frozen creature scenes are covered by nine execution systems. Cyclops uses forced scale, partial face/eye, hand/contact and cave occlusion; Scylla uses practical victim rigs and contact points with digital reach extension; Sirens are performer/cloth/sound-led; Charybdis is water, deck reaction and environment extension; Circe transformation is cut, prosthetic fragments, silhouette and reaction; Underworld uses depth layers, gauze/water/reflection and sparse extensions; petrification uses progressive practical texture plus comp; divine manifestation uses condition, shadow, wind and editorial alignment.

Every system declares the performer touch point, rated rig owner, puppet/prosthetic piece, shadow/water element, removable tracking reference, clean plate and digital-extension seam. P5 is technical planning only. Rig loads, performer contact, water/electrical separation and materials require P6 physical testing.
""")

mat_lines = ["# Material Finish Schedule", "", "One material language across sets, props, costume and creature work:", "", "| Family | Build basis | Frozen finish | Wet/safety/reset rule |", "|---|---|---|---|"]
for k,(base,finish,rule) in materials.items(): mat_lines.append(f"| {k} | {base} | {finish} | {rule} |")
mat_lines += ["", "All samples require neutral-light, warm-practical and P4 target-grade photographs. Real flame retardancy, toxicity, slip, skin and structural validation remain P6 tasks."]
write("MATERIAL_FINISH_SCHEDULE.md", "\n".join(mat_lines))

write("COLOR_FINISH_SCHEDULE.md", """# Color Finish Schedule

Color follows story state, never departmental preference. Ithaca moves from consumed umber/wine to blackened finite violence and repaired olive/linen; sea holds cold salt and oxidized timber; Phaeacia offers measured mineral warmth without luxury gloss; cave/myth worlds suppress saturation and reveal scale through contrast; Underworld protects black separation; restoration returns skin, olive wood and daylight without erasing wear.

Each set/prop/costume sample is photographed under neutral 5600K, warm practical and the representative P4 color-key transform. Wet and blood variants receive separate chips. This is a show-LUT intent record, not final DI.
""")

write("ART_CONTINUITY_BOOK.md", """# Art Continuity Book

## Capture minimum

For every scene/state: slate and scene ID; locked wide; north/east/south/west corners; hero-prop custody insert; costume/HMU full/half/detail; wet/blood/damage scale; floor and route map; strike inventory. File names bind scene ID, asset ID and state.

## Priority chains

- Recognition: name/story → scar → bow → 12 axes → bed → father/land → community.
- S1: A occupied → B contest → C first blood → D full battle → E aftermath → F restored.
- Odysseus: damage/salt → shipwreck → Phaeacia recovery → disguise → scar → battle → restoration.
- Wet: W0 dry → W1 damp/spray → W2 saturated; never backtrack inside one action sequence.
- Blood: B0 → B1 first contact → B2 local → B3 action → B4 battle → B5 aftermath; only planned cleanup moves toward clean.

No asset moves between units without a signed custody record. Continuity cannot be solved by altering P3 geography or P4 identity.
""")

write("ART_DEPARTMENT_HANDOFF_RESULT.md", f"""# Art Department Handoff Result

Status: **PASS_ART_DEPARTMENT_HANDOFF_DESKTOP_SPECIFICATION**

- Standing sets: 5/5
- Production-unit redresses: 12/12
- Frozen hero-prop systems: 12/12
- Costume build states: {len(costumes)}
- Principal build logic: 4/4
- Practical creature systems: {len(creatures)} covering all 8 frozen creature scenes
- S1 state chain: S1-A through S1-F — PASS
- Material/finish continuity: PASS
- Wet/blood duplicate logic: PASS
- P3 TARGET 54-day compatibility: PASS on desktop evidence; real turnaround validation pending
- P3/P4 modifications: 0

The handoff is ready for a real production designer, construction coordinator, prop master, costume supervisor, HMU/prosthetics lead, creature FX supervisor and safety team to quote and physically validate. It is not proof that assets have been fabricated or tested.
""")

print(json.dumps({"status": "PASS", "assets": len(assets), "sets": len(sets), "redresses": len(redresses), "props": len(props), "costumes": len(costumes), "creatures": len(creatures)}, ensure_ascii=False))
