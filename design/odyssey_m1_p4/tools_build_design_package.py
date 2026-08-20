#!/usr/bin/env python3
"""Generate deterministic P4 state matrices and labeled technical design sheets."""

from __future__ import annotations

import hashlib
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "design" / "odyssey_m1_p4"
SVG = OUT / "technical_sheets"
SVG.mkdir(parents=True, exist_ok=True)

CHARACTERS = {
    "Odysseus": ["ODY-A", "ODY-B", "ODY-C", "ODY-D", "ODY-E", "ODY-F", "ODY-G", "ODY-H", "ODY-I", "ODY-J"],
    "Penelope": ["PEN-A", "PEN-B", "PEN-C", "PEN-D", "PEN-E", "PEN-F", "PEN-G"],
    "Telemachus": ["TEL-A", "TEL-B", "TEL-C", "TEL-D", "TEL-E", "TEL-F", "TEL-G", "TEL-H"],
    "Athena": ["ATH-MENTES", "ATH-MENTOR", "ATH-GIRL", "ATH-COMPANION", "ATH-BOY", "ATH-SHEPHERD", "ATH-ALMOST", "ATH-DIVINE"],
}

COSTUMES = {
    "Odysseus": ["W-OD-05-CALYPSO-WORN", "W-OD-05-RAFT-SALT", "W-OD-06-PHAEACIA-BORROWED", "W-OD-09-15-STORY", "W-OD-16-LANDFALL", "W-OD-17-26-BEGGAR", "W-OD-27-BATTLE", "W-OD-29-CLEANED-RETURNED", "W-OD-30-RETURNED-FIELD"],
    "Telemachus": ["W-TE-01-BOY-HOUSEHOLD", "W-TE-03-TRAVELER", "W-TE-18-RETURNING-HEIR", "W-TE-26-BATTLE-HEIR", "W-TE-30-CIVIC-AUTHORITY"],
    "Penelope": ["W-PE-01-HOUSEHOLD-MOURNING-PURPLE", "W-PE-25-CONTEST", "W-PE-29-RECOGNITION", "W-PE-30-CIVIC-RESTORATION"],
    "Athena": ["W-AT-MENTES", "W-AT-MENTOR", "W-AT-GIRL", "W-AT-COMPANION", "W-AT-BOY", "W-AT-SHEPHERD", "W-AT-DIVINE"],
}

SETS = {
    "S1": {"name": "Ithaca hall", "states": ["S1-A", "S1-B", "S1-C", "S1-D", "S1-E", "S1-F"], "palette": ["#806b4e", "#66504f", "#2f2b25", "#9d845c"]},
    "S2": {"name": "ceremonial court", "states": ["PYLOS", "SPARTA", "PHAEACIA", "CIRCE"], "palette": ["#c2b58f", "#607d82", "#844b45", "#4f6848"]},
    "S3": {"name": "dry ship deck", "states": ["TELEMACHUS", "FLEET", "LAST-SHIP", "PHAEACIAN"], "palette": ["#564331", "#485b63", "#a28d68", "#252c2e"]},
    "S4": {"name": "Eumaeus farm", "states": ["WORK", "GUEST", "RECOGNITION", "DEPARTURE"], "palette": ["#6d4f37", "#8a6746", "#332b25", "#a5906b"]},
    "S5": {"name": "shore/cave adaptable", "states": ["OGYGIA", "CYCLOPS", "ITHACA-SHORE", "CREATURE-COAST"], "palette": ["#717772", "#312d29", "#776b52", "#445a5c"]},
}

MYTHIC = ["CYCLOPS", "CIRCE", "SIRENS", "CHARYBDIS", "SCYLLA", "UNDERWORLD", "POSEIDON", "ATHENA", "PETRIFICATION"]

PROPS = ["PR-BOW-01", "PR-AXES-01..12", "PR-SCAR-01", "PR-BED-01", "PR-WEAVE-01", "PR-TE-SWORD-01", "PR-OD-WEAPON-SET", "PR-BONE-01..06", "PR-BOUNDARY-01", "PR-WIND-01", "PR-STAKE-01", "PR-SHIP-INV-01"]


def write_json(name: str, payload: dict) -> None:
    (OUT / name).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sheet(title: str, subtitle: str, columns: list[tuple[str, str, str]], path: Path) -> None:
    width, height = 1600, 900
    n = len(columns)
    gap = 20
    col_w = (width - 80 - gap * max(0, n - 1)) / max(1, n)
    chunks = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
              '<rect width="1600" height="900" fill="#171816"/>',
              f'<text x="40" y="58" fill="#eee8d8" font-family="sans-serif" font-size="34" font-weight="700">{html.escape(title)}</text>',
              f'<text x="40" y="92" fill="#a9a28e" font-family="sans-serif" font-size="18">{html.escape(subtitle)} · TECHNICAL DESIGN SHEET</text>']
    for i, (label, color, note) in enumerate(columns):
        x = 40 + i * (col_w + gap)
        chunks += [f'<rect x="{x:.1f}" y="130" width="{col_w:.1f}" height="680" rx="8" fill="#252720" stroke="#77715e"/>',
                   f'<rect x="{x+18:.1f}" y="150" width="{col_w-36:.1f}" height="46" fill="{color}"/>',
                   f'<text x="{x+22:.1f}" y="226" fill="#eee8d8" font-family="sans-serif" font-size="20" font-weight="700">{html.escape(label)}</text>',
                   # cast-neutral silhouette, deliberately technical
                   f'<circle cx="{x+col_w/2:.1f}" cy="330" r="46" fill="none" stroke="#d4c6a5" stroke-width="7"/>',
                   f'<path d="M {x+col_w/2-92:.1f} 585 Q {x+col_w/2-70:.1f} 405 {x+col_w/2:.1f} 395 Q {x+col_w/2+70:.1f} 405 {x+col_w/2+92:.1f} 585" fill="none" stroke="#d4c6a5" stroke-width="9"/>',
                   f'<line x1="{x+col_w/2:.1f}" y1="376" x2="{x+col_w/2:.1f}" y2="690" stroke="#8d876f" stroke-width="3" stroke-dasharray="8 8"/>',
                   f'<text x="{x+22:.1f}" y="742" fill="#c4bea9" font-family="sans-serif" font-size="15">{html.escape(note[:55])}</text>',
                   f'<text x="{x+22:.1f}" y="775" fill="#77715e" font-family="sans-serif" font-size="13">identity / material / access witness</text>']
    chunks += ['<text x="40" y="866" fill="#77715e" font-family="sans-serif" font-size="14">P4 · geometry and state reference only · not high-fidelity concept art</text>', '</svg>']
    path.write_text("\n".join(chunks) + "\n", encoding="utf-8")


def build_s1_plan() -> None:
    authority = json.loads((ROOT / "preproduction/odyssey_m1_p3/S1_ITHACA_HALL_FLOOR_PLAN.json").read_text(encoding="utf-8"))
    width, height = 1500, 1100
    ox, oy, scale = 750, 950, 38
    def xy(x: float, y: float) -> tuple[float, float]:
        return ox + x * scale, oy - y * scale
    chunks = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
              '<rect width="1500" height="1100" fill="#171816"/>',
              '<text x="50" y="55" fill="#eee8d8" font-family="sans-serif" font-size="32" font-weight="700">S1 ITHACA HALL · FROZEN P3 GEOMETRY</text>',
              '<text x="50" y="88" fill="#a9a28e" font-family="sans-serif" font-size="17">16 m × 22 m · north at top · P4 surfaces and light only</text>',
              f'<rect x="{ox-8*scale}" y="{oy-22*scale}" width="{16*scale}" height="{22*scale}" fill="#302e28" stroke="#bba77c" stroke-width="8"/>']
    for item in authority["fixed_elements"]:
        x,y=xy(float(item["x"]),float(item["y"]))
        if item["id"].startswith("P"):
            chunks.append(f'<circle cx="{x}" cy="{y}" r="16" fill="#8a7957" stroke="#e6d7ae" stroke-width="4"/>')
        elif item["id"]=="H0":
            chunks.append(f'<circle cx="{x}" cy="{y}" r="42" fill="#72452f" stroke="#d58b55" stroke-width="4"/>')
        else:
            chunks.append(f'<rect x="{x-18}" y="{y-12}" width="36" height="24" fill="#5c665c" stroke="#d1c5a4" stroke-width="2"/>')
        chunks.append(f'<text x="{x+22}" y="{y+6}" fill="#eee8d8" font-family="sans-serif" font-size="15" font-weight="700">{html.escape(item["id"])}</text>')
    # Exact axes line and twelve bases.
    x0,y0=xy(0,3); x1,y1=xy(0,19)
    chunks.append(f'<line x1="{x0}" y1="{y0}" x2="{x1}" y2="{y1}" stroke="#d7b76d" stroke-width="4" stroke-dasharray="12 8"/>')
    for i,yv in enumerate(range(5,17),start=1):
        x,y=xy(0,yv); chunks.append(f'<circle cx="{x}" cy="{y}" r="8" fill="#b99656"/><text x="{x+12}" y="{y+5}" fill="#c8b990" font-family="sans-serif" font-size="11">AX{i:02d}</text>')
    # Locked production routes, using explicit P3 route semantics.
    route_specs={
        "R-PEN":([(-5.5,0),(-5,3),(-6,8),(-5,15),(-4.5,18.5)],"#8d637e"),
        "R-TEL-PUB":([(0,22),(5,18),(4,10),(3,6),(-1,1)],"#608a94"),
        "R-TEL-ARM":([(3,6),(0,3),(-5,1)],"#6a93a0"),
        "R-SERV":([(9,9),(8,9),(5,9),(3,8)],"#9f8a62"),
        "R-OD-BOW":([(6,4),(0,3),(0,2.5),(-4.5,18.5)],"#c1a252"),
        "R-ARM-BYPASS":([(9,9),(-7,-1),(-6,0),(-5,1)],"#9a584e"),
    }
    for rid,(pts,color) in route_specs.items():
        p=" ".join(f"{xy(a,b)[0]},{xy(a,b)[1]}" for a,b in pts)
        chunks.append(f'<polyline points="{p}" fill="none" stroke="{color}" stroke-width="5" opacity="0.88" marker-end="url(#arrow)"/>')
    chunks.insert(3,'<defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="#d7b76d"/></marker></defs>')
    for i,(rid,(_,color)) in enumerate(route_specs.items()):
        chunks.append(f'<line x1="1060" y1="{220+i*44}" x2="1120" y2="{220+i*44}" stroke="{color}" stroke-width="6"/><text x="1135" y="{226+i*44}" fill="#d8d1bd" font-family="sans-serif" font-size="17">{rid}</text>')
    chunks += ['<text x="1060" y="160" fill="#eee8d8" font-family="sans-serif" font-size="20" font-weight="700">LOCKED ROUTES</text>',
               '<text x="1060" y="560" fill="#a9a28e" font-family="sans-serif" font-size="16">N0 / E0 / A0 / G0 remain</text>',
               '<text x="1060" y="588" fill="#a9a28e" font-family="sans-serif" font-size="16">story constraints, never camera exits.</text>',
               '<text x="1060" y="648" fill="#d7b76d" font-family="sans-serif" font-size="18">X=0 bow / 12 axes / N1</text>',
               '<text x="50" y="1060" fill="#77715e" font-family="sans-serif" font-size="14">P4 TECHNICAL DESIGN · source: preproduction/odyssey_m1_p3/S1_ITHACA_HALL_FLOOR_PLAN.json</text>', '</svg>']
    (SVG/"P4-SET-S1-PLAN-ROUTES.svg").write_text("\n".join(chunks)+"\n",encoding="utf-8")


def main() -> None:
    char_rows = []
    palette = ["#81715a", "#655268", "#8b7656", "#9a8d72", "#6f5038", "#9a4f3f", "#4f6848", "#6d302b", "#b8ab8c", "#756344"]
    for c, states in CHARACTERS.items():
        if len(states) > 8:
            sheet_ref = [f"technical_sheets/P4-CHAR-{c.upper()}-TECH-A.svg", f"technical_sheets/P4-CHAR-{c.upper()}-TECH-B.svg"]
        else:
            sheet_ref = [f"technical_sheets/P4-CHAR-{c.upper()}-TECH.svg"]
        for i, state in enumerate(states):
            char_rows.append({"character": c, "state_id": state, "silhouette_lock": "character invariant", "identity_sheets": sheet_ref, "wet_state": "W0 unless scene-bound", "blood_state": "B0 unless scene-bound", "status": "FROZEN"})
        cols = [(s, palette[i % len(palette)], "same fictional identity; state changes access and condition") for i, s in enumerate(states)]
        # split long Odysseus row into two technical sheets for legibility
        if len(cols) > 8:
            sheet(f"{c} states A–E", "fictional cast-neutral identity", cols[:5], SVG / f"P4-CHAR-{c.upper()}-TECH-A.svg")
            sheet(f"{c} states F–J", "fictional cast-neutral identity", cols[5:], SVG / f"P4-CHAR-{c.upper()}-TECH-B.svg")
        else:
            sheet(f"{c} visual states", "fictional cast-neutral identity", cols, SVG / f"P4-CHAR-{c.upper()}-TECH.svg")
    write_json("CHARACTER_STATE_MATRIX.json", {"artifact_class": "odyssey_p4_character_state_matrix", "principal_count": 4, "states": char_rows, "real_person_likeness": False, "status": "FROZEN_CHARACTER_STATES"})

    costume_rows = []
    for c, states in COSTUMES.items():
        for s in states:
            costume_rows.append({"character": c, "costume_id": s, "versions": ["HERO", "WET", "STUNT"] + (["BLOOD"] if "BATTLE" in s else []), "material_continuity": "MATCH_REQUIRED", "status": "FROZEN"})
    write_json("COSTUME_STATE_MATRIX.json", {"artifact_class": "odyssey_p4_costume_state_matrix", "costumes": costume_rows, "wet_states": ["W0", "W1", "W2", "W3", "W4"], "blood_states": ["B0", "B1", "B2", "B3", "B4", "B5"], "status": "FROZEN_COSTUME_STATES"})

    set_rows=[]
    for sid, spec in SETS.items():
        set_rows.append({"set_id": sid, **spec, "p3_geometry_modified": False, "design_sheet": f"technical_sheets/P4-SET-{sid}-TECH.svg", "high_fidelity_anchor_required": True})
        cols=[(x, spec["palette"][i % len(spec["palette"])], f"same {sid} geometry; redress/light/state only") for i,x in enumerate(spec["states"])]
        sheet(f"{sid} {spec['name']}", "standing-set state package", cols, SVG / f"P4-SET-{sid}-TECH.svg")
    write_json("SET_STATE_MATRIX.json", {"artifact_class": "odyssey_p4_set_state_matrix", "standing_set_count": 5, "sets": set_rows, "status": "FROZEN_FIVE_STANDING_SET_STATES"})
    build_s1_plan()

    mythic_rows=[]
    for i, name in enumerate(MYTHIC):
        p=SVG/f"P4-CREATURE-{name}-TECH.svg"
        sheet(name, "practical base → in-camera → limited VFX → sound/reaction", [("PRACTICAL", "#6d5b42", "physical contact and measured eyeline"), ("IN-CAMERA", "#4f5d5a", "scale/absence/occlusion before reveal"), ("VFX LIMIT", "#58465b", "extension cannot replace human choice")], p)
        mythic_rows.append({"system_id": name, "technical_sheet": p.relative_to(ROOT).as_posix(), "full_cg_hero_required": False, "status": "FROZEN"})
    write_json("CREATURE_SYSTEM_MATRIX.json", {"artifact_class": "odyssey_p4_creature_system_matrix", "systems": mythic_rows, "p3_creature_scenes_covered": 8, "status": "PASS_CREATURE_SYSTEMS"})

    prop_cols=[(p, ["#815f3d", "#796449", "#69584d", "#8d764f"][i%4], "hero/stunt/safe identity and custody remain exact") for i,p in enumerate(PROPS)]
    for i in range(0,len(prop_cols),4):
        sheet(f"Hero props {i+1}–{min(i+4,len(prop_cols))}", "custody and recognition evidence", prop_cols[i:i+4], SVG/f"P4-PROPS-{i//4+1:02d}-TECH.svg")
    write_json("HERO_PROP_STATE_MATRIX.json", {"artifact_class": "odyssey_p4_hero_prop_state_matrix", "props": [{"prop_id": p, "technical_sheet": f"technical_sheets/P4-PROPS-{i//4+1:02d}-TECH.svg", "custody_lock": "P3_PROP_CONTINUITY", "status": "FROZEN"} for i,p in enumerate(PROPS)], "status": "PASS_HERO_PROP_SYSTEMS"})


if __name__ == "__main__":
    main()
