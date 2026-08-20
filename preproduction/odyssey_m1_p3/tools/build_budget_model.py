#!/usr/bin/env python3
"""Build a transparent assumption-based P3 budget model from frozen schedules."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
P3 = ROOT / "preproduction" / "odyssey_m1_p3"
OUT = P3 / "BUDGET_MODEL.md"
VFX = json.loads((P3 / "VFX_CREATURE_EXECUTION_MATRIX.json").read_text())
SCHEDULES = {tier: json.loads((P3 / f"SHOOTING_SCHEDULE_{name}.json").read_text()) for tier, name in (("LEAN", "LEAN"), ("TARGET", "TARGET"), ("PREMIUM", "SAFE"))}


def schedule_quantity(tier: str, field: str) -> int:
    days = SCHEDULES[tier]["days"]
    if field == "days": return len(days)
    if field == "extra_days": return sum(day["extras"] for day in days)
    if field == "wet_days": return sum(day["wet"] for day in days)
    if field == "stunt_days": return sum(day["stunt"] for day in days)
    raise KeyError(field)


RUNTIME_MINUTES = round(SCHEDULES["TARGET"]["total_script_minutes"])
VFX_SHOTS = VFX["series_planned_vfx_shot_count"]
assert RUNTIME_MINUTES == 212 and VFX_SHOTS == 171

ROWS = [
    ("development", "package", {"LEAN": (1, 300_000), "TARGET": (1, 450_000), "PREMIUM": (1, 700_000)}),
    ("producer/director", "package", {"LEAN": (1, 1_300_000), "TARGET": (1, 1_800_000), "PREMIUM": (1, 2_800_000)}),
    ("principal cast", "cast-days", {"LEAN": (100, 20_000), "TARGET": (112, 25_000), "PREMIUM": (125, 40_000)}),
    ("supporting cast", "cast-days", {"LEAN": (180, 4_500), "TARGET": (220, 6_000), "PREMIUM": (280, 8_500)}),
    ("extras", "pool person-days", {t: (schedule_quantity(t, "extra_days"), u) for t, u in {"LEAN": 380, "TARGET": 450, "PREMIUM": 650}.items()}),
    ("crew", "crew person-days", {"LEAN": (55 * schedule_quantity("LEAN", "days"), 800), "TARGET": (65 * schedule_quantity("TARGET", "days"), 900), "PREMIUM": (75 * schedule_quantity("PREMIUM", "days"), 1_200)}),
    ("camera", "package-days", {t: (schedule_quantity(t, "days"), u) for t, u in {"LEAN": 15_000, "TARGET": 18_000, "PREMIUM": 28_000}.items()}),
    ("grip/electric", "package-days", {t: (schedule_quantity(t, "days"), u) for t, u in {"LEAN": 18_000, "TARGET": 22_000, "PREMIUM": 32_000}.items()}),
    ("art", "production blocks", {"LEAN": (12, 80_000), "TARGET": (12, 120_000), "PREMIUM": (12, 200_000)}),
    ("set build", "standing sets", {"LEAN": (5, 260_000), "TARGET": (5, 380_000), "PREMIUM": (5, 650_000)}),
    ("wardrobe", "built/rented looks", {"LEAN": (100, 6_000), "TARGET": (125, 9_000), "PREMIUM": (150, 15_000)}),
    ("HMU", "department-days", {t: (schedule_quantity(t, "days"), u) for t, u in {"LEAN": 11_000, "TARGET": 15_000, "PREMIUM": 23_000}.items()}),
    ("props", "hero packages", {"LEAN": (24, 22_000), "TARGET": (24, 35_000), "PREMIUM": (24, 60_000)}),
    ("stunts", "shoot + rehearsal days", {"LEAN": (schedule_quantity("LEAN", "stunt_days") + 5, 18_000), "TARGET": (schedule_quantity("TARGET", "stunt_days") + 7, 25_000), "PREMIUM": (schedule_quantity("PREMIUM", "stunt_days") + 9, 38_000)}),
    ("animals", "handler/animal units", {"LEAN": (10, 12_000), "TARGET": (12, 20_000), "PREMIUM": (16, 35_000)}),
    ("boats/wet", "wet package-days", {t: (schedule_quantity(t, "wet_days"), u) for t, u in {"LEAN": 40_000, "TARGET": 55_000, "PREMIUM": 85_000}.items()}),
    ("locations", "shooting days", {t: (schedule_quantity(t, "days"), u) for t, u in {"LEAN": 10_000, "TARGET": 12_000, "PREMIUM": 20_000}.items()}),
    ("transport", "shooting days", {t: (schedule_quantity(t, "days"), u) for t, u in {"LEAN": 18_000, "TARGET": 22_000, "PREMIUM": 35_000}.items()}),
    ("accommodation", "shooting days", {t: (schedule_quantity(t, "days"), u) for t, u in {"LEAN": 30_000, "TARGET": 40_000, "PREMIUM": 60_000}.items()}),
    ("VFX", "planned shots", {"LEAN": (VFX_SHOTS, 12_000), "TARGET": (VFX_SHOTS, 18_000), "PREMIUM": (VFX_SHOTS, 32_000)}),
    ("SFX", "technical shoot-days", {t: (schedule_quantity(t, "stunt_days"), u) for t, u in {"LEAN": 12_000, "TARGET": 18_000, "PREMIUM": 30_000}.items()}),
    ("sound", "finished minutes", {"LEAN": (RUNTIME_MINUTES, 5_500), "TARGET": (RUNTIME_MINUTES, 8_000), "PREMIUM": (RUNTIME_MINUTES, 12_000)}),
    ("music", "finished minutes", {"LEAN": (RUNTIME_MINUTES, 3_500), "TARGET": (RUNTIME_MINUTES, 6_000), "PREMIUM": (RUNTIME_MINUTES, 10_000)}),
    ("post", "finished minutes", {"LEAN": (RUNTIME_MINUTES, 8_000), "TARGET": (RUNTIME_MINUTES, 12_000), "PREMIUM": (RUNTIME_MINUTES, 20_000)}),
    ("insurance/safety", "shooting days", {t: (schedule_quantity(t, "days"), u) for t, u in {"LEAN": 12_000, "TARGET": 18_000, "PREMIUM": 30_000}.items()}),
]
CONTINGENCY = {"LEAN": 0.08, "TARGET": 0.12, "PREMIUM": 0.15}


def money(value: int) -> str:
    return f"¥{value:,.0f}"


def build() -> str:
    totals: dict[str, dict[str, int]] = {}
    for tier in ("LEAN", "TARGET", "PREMIUM"):
        subtotal = sum(values[tier][0] * values[tier][1] for _, _, values in ROWS)
        contingency = round(subtotal * CONTINGENCY[tier])
        totals[tier] = {"subtotal": subtotal, "contingency": contingency, "total": subtotal + contingency}
    assert totals == {
        "LEAN": {"subtotal": 21_704_600, "contingency": 1_736_368, "total": 23_440_968},
        "TARGET": {"subtotal": 34_163_200, "contingency": 4_099_584, "total": 38_262_784},
        "PREMIUM": {"subtotal": 59_110_650, "contingency": 8_866_598, "total": 67_977_248},
    }
    lines = [
        "# Budget Model",
        "",
        "Status: `PASS_ASSUMPTION_BASED_THREE_TIER_BUDGET`",
        "",
        "> **ASSUMPTION-BASED PLANNING RANGE — NOT VENDOR QUOTE.** Currency is CNY/RMB, tax treatment and financing cost excluded. Rates are comparative planning units that must be replaced by bids before greenlight.",
        "",
        "Schedule authority: LEAN 42 days, TARGET 54 days, SAFE/PREMIUM 62 days. Target is the master recommendation. Quantity authority includes 212 estimated finished minutes, 171 planned VFX-handled shots, 25 target stunt shoot days plus seven dedicated rehearsal days, 17 target wet days, five standing sets and twelve production blocks.",
        "",
        "## Quantity × unit assumptions",
        "",
        "| Cost line | Unit | LEAN formula / amount | TARGET formula / amount | PREMIUM formula / amount |",
        "|---|---|---:|---:|---:|",
    ]
    for name, unit, values in ROWS:
        cells = []
        for tier in ("LEAN", "TARGET", "PREMIUM"):
            quantity, unit_cost = values[tier]
            cells.append(f"{quantity:,} × {money(unit_cost)} = {money(quantity * unit_cost)}")
        lines.append(f"| {name} | {unit} | {cells[0]} | {cells[1]} | {cells[2]} |")
    lines += [
        f"| **Subtotal** |  | **{money(totals['LEAN']['subtotal'])}** | **{money(totals['TARGET']['subtotal'])}** | **{money(totals['PREMIUM']['subtotal'])}** |",
        f"| Contingency | percentage of subtotal | 8% = {money(totals['LEAN']['contingency'])} | 12% = {money(totals['TARGET']['contingency'])} | 15% = {money(totals['PREMIUM']['contingency'])} |",
        f"| **Planning total** | CNY | **{money(totals['LEAN']['total'])}** | **{money(totals['TARGET']['total'])}** | **{money(totals['PREMIUM']['total'])}** |",
        "",
        "Planning range: `¥23.44M LEAN / ¥38.26M TARGET / ¥67.98M PREMIUM`. These are not quotes.",
        "",
        "## Target cost drivers",
        "",
    ]
    target_amounts = sorted(((name, values["TARGET"][0] * values["TARGET"][1]) for name, _, values in ROWS), key=lambda x: -x[1])
    for rank, (name, value) in enumerate(target_amounts[:8], 1):
        lines.append(f"{rank}. **{name}: {money(value)}** — preserve the quantity logic; negotiate rates only with the department consequence visible.")
    base = totals["TARGET"]["total"]
    lines += [
        "",
        "## Sensitivity against TARGET",
        "",
        "| Cut | Planning ceiling | First levers | Protected consequence |",
        "|---|---:|---|---|",
        f"| -10% | {money(round(base * .90))} | retain zero true company-move days; trim secondary VFX/environment extensions, far crowd layers, nonhero wardrobe builds, transport/accommodation inefficiency and one noncritical post pass | no reduction to recognition-object coverage or EP26–28 safety/rehearsal |",
        f"| -20% | {money(round(base * .80))} | add approved CAN DOUBLE packages, combine nonadjacent court/shore redress days, reduce background density, use more practical creature occlusion and cap music/VFX iteration | keep EP25 bow, six Scylla victims, S1 geography, EP29 bed and EP30 civic witnesses intact |",
        f"| -30% | {money(round(base * .70))} | move toward LEAN 42-day boundary, remove optional spectacle beats, reduce distant boats/crowd plates and accept stricter daylight/coverage limits | high schedule/quality risk; cannot cut below safety staffing, hero props or performance protection |",
        "The target already schedules zero public-road company-move days inside its twelve blocks. Therefore that preferred saving has been realized before cuts; no fictitious move saving is counted again.",
        "",
        "## Protected spend floor",
        "",
        "Do not fund cuts first from: the recognition chain; Penelope’s bed test; EP25 bow/axes; EP26–28 geography, rehearsals, safe weapons, blood and resets; EP29 marriage recognition; EP30 lineage/civic closure; water rescue; animal supervision; prosthetic safety; or independent VFX plates. If the -30% ceiling cannot retain those, the package is not production-ready at that ceiling.",
        "",
        "Final result: `PASS_TARGET_BUDGET_38262784_CNY_ASSUMPTION_BASED`.",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    payload = build().encode()
    if args.check:
        assert OUT.read_bytes() == payload
        print(f"PASS {hashlib.sha256(payload).hexdigest()} {len(payload)} bytes")
    else:
        OUT.write_bytes(payload)
        print(f"WROTE {OUT.name} {hashlib.sha256(payload).hexdigest()}")


if __name__ == "__main__":
    main()
