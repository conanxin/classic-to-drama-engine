from __future__ import annotations

import collections
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
V1 = ROOT / "scripts/odyssey_m1_v1/episodes"
OUT = ROOT / "editorial/odyssey_m1_v2/PRODUCTION_FEASIBILITY_AUDIT.md"

PROP_TERMS = [
    "酒杯", "杯", "骰", "剑", "矛", "盾", "弓", "箭", "斧", "脚凳", "斗篷", "袍", "别针", "织", "寿衣",
    "船", "木筏", "桅杆", "绳", "蜡", "袋", "魔草", "酒", "木桩", "奶酪", "羊", "猪", "牛", "血沟",
    "铁饼", "钥匙", "门闩", "硫磺", "床", "橄榄树", "果树", "磨坊", "火盆", "礼物", "项链", "长矛",
]

STANDING_SET = {
    "伊萨卡厅堂": "S1 Ithaca hall/courtyard", "厅堂": "S1 Ithaca hall/courtyard", "夜间厅堂": "S1 Ithaca hall/courtyard",
    "封闭厅堂": "S1 Ithaca hall/courtyard", "清洗后的厅堂": "S1 Ithaca hall/courtyard", "宫殿庭院": "S1 Ithaca hall/courtyard",
    "庭院": "S1 Ithaca hall/courtyard", "庭院火盆": "S1 Ithaca hall/courtyard", "宫殿门槛": "S1 Ithaca hall/courtyard",
    "宫殿侧门": "S1 Ithaca hall/courtyard", "武器墙": "S1 Ithaca hall/courtyard", "武器库": "S1 Ithaca hall/courtyard",
    "武器库暗道": "S1 Ithaca hall/courtyard", "洗脚处": "S1 Ithaca hall/courtyard", "佩涅洛佩卧室": "S1 Ithaca hall/courtyard",
    "婚房": "S1 Ithaca hall/courtyard", "忒勒马科斯寝室": "S1 Ithaca hall/courtyard", "磨坊": "S1 Ithaca service annex",
    "菲埃克斯王宫": "S2 Phaeacian hall", "菲埃克斯宴会厅": "S2 Phaeacian hall",
    "欧迈俄斯猪场": "S3 Eumaeus farm", "海上木筏": "S4 hero deck/water tank", "伊萨卡近海": "S4 hero deck/water tank",
    "近岸海面": "S4 hero deck/water tank", "海妖海域": "S4 hero deck/water tank", "斯库拉海峡": "S4 hero deck/water tank",
    "雷暴海面": "S4 hero deck/water tank", "阿斯忒里斯水道": "S4 hero deck/water tank",
}


def yes(condition: bool) -> str:
    return "Y" if condition else "—"


episodes = []
scene_rows = []
locations: set[str] = set()
principals: set[str] = set()
tag_counts: collections.Counter[str] = collections.Counter()

for path in sorted(V1.glob("EP*.md")):
    text = path.read_text(encoding="utf-8")
    episode = path.stem
    matches = list(re.finditer(r"^## 场 (\d+)｜(内景|外景)·([^·\n]+)·(日|暮|夜)$", text, flags=re.MULTILINE))
    episode_scores = []
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else text.find("**切黑。**", start)
        body = text[start:end]
        summary = next((line.strip() for line in body.splitlines() if line.strip()), "")
        cast = []
        for cue in re.findall(r"^\*\*([^*]+)\*\*$", body, flags=re.MULTILINE):
            if cue not in cast and cue not in {"淡入。", "切黑。"}:
                cast.append(cue)
        location = match.group(3)
        locations.add(location)
        principals.update(cast)
        combined = location + " " + body
        extras = any(term in combined for term in ["求婚者", "人群", "众人", "同伴", "船员", "侍女", "女仆", "亡魂", "公民大会"])
        animals = any(term in combined for term in ["狗", "猪", "羊", "牛", "鹰", "鹅", "鹿"])
        water = any(term in combined for term in ["海", "岸", "港", "河", "水道", "木筏", "桅杆", "船"])
        boat = any(term in combined for term in ["船", "木筏", "桅杆", "船队"])
        fight = any(term in combined for term in ["杀", "攻击", "冲锋", "激战", "长矛", "掷矛", "射倒", "抓走", "打碎", "决斗"])
        stunt = fight or any(term in combined for term in ["摔", "击中", "扑", "绑", "爬", "赤裸", "投得更远"])
        vfx = any(term in combined for term in ["雅典娜", "波塞冬", "宙斯", "赫尔墨斯", "神明", "变成", "化作", "亡魂", "冥界", "海妖", "斯库拉", "巨人", "石化", "雷声"])
        creature = any(term in combined for term in ["波吕斐摩斯", "独眼巨人", "海妖", "斯库拉", "变成猪", "莱斯特律戈涅斯"])
        weather = any(term in combined for term in ["风暴", "雷", "雨", "逆风", "海浪", "风正在变"])
        fire = any(term in combined for term in ["火", "硫磺", "祭火", "雷电"])
        blood = any(term in combined for term in ["血", "尸体", "喉咙", "吞食", "杀死", "死亡"])
        makeup = any(term in combined for term in ["乞丐", "伤疤", "变成猪", "赤裸", "亡魂", "巨人"])
        props = []
        for term in PROP_TERMS:
            if term in combined and term not in props:
                props.append(term)
        score = min(10, 1 + extras + animals + 2 * water + 2 * boat + 2 * fight + stunt + 2 * vfx + 2 * creature + weather + fire + blood + makeup)
        episode_scores.append(score)
        flags = {"extras": extras, "animals": animals, "water": water, "boat": boat, "fight": fight, "stunt": stunt, "vfx": vfx, "creature": creature, "weather": weather, "fire": fire, "blood": blood, "makeup": makeup}
        tag_counts.update(name for name, value in flags.items() if value)
        scene_rows.append(
            [episode, match.group(1), f"{match.group(2)}·{location}·{match.group(4)}", ", ".join(cast) or "—", "crowd" if extras else "—", ", ".join(props[:6]) or "—",
             yes(animals), yes(water), yes(boat), yes(fight), yes(stunt), yes(vfx), yes(creature), yes(weather), yes(fire), yes(blood), yes(makeup), str(score), summary]
        )
    episodes.append((episode, round(sum(episode_scores) / len(episode_scores), 1), max(episode_scores)))

high_cost = [episode for episode, average, maximum in episodes if average >= 6 or maximum >= 9]
standing_count = len(set(STANDING_SET.values()))

lines = [
    "# 《归途：奥德修斯》V1 Production Feasibility Audit",
    "",
    "Status: `COMPLETE_V1_PRODUCTION_AUDIT`",
    "",
    "This is a pre-rewrite audit of all 150 V1 scenes. Tags are production warnings, not mandates for literal execution. V2 must lower avoidable load through standing-set reuse, partial views, sound, foreground occlusion, and action blocking while preserving story responsibility.",
    "",
    "## Baseline totals",
    "",
    f"- Scenes audited: {len(scene_rows)}",
    f"- Unique V1 location labels: {len(locations)}",
    f"- Standing-set families currently recoverable: {standing_count}",
    f"- Speaking-role labels: {len(principals)} (includes disguises, groups, and divine voices; not equal to cast count)",
    f"- Extra-heavy scenes: {tag_counts['extras']}",
    f"- Fight scenes: {tag_counts['fight']}",
    f"- Water-heavy scenes: {tag_counts['water']}",
    f"- Boat scenes: {tag_counts['boat']}",
    f"- VFX-signaled scenes: {tag_counts['vfx']}",
    f"- Creature scenes: {tag_counts['creature']}",
    f"- Weather scenes: {tag_counts['weather']}",
    f"- Fire scenes: {tag_counts['fire']}",
    f"- Blood scenes: {tag_counts['blood']}",
    f"- Special-makeup scenes: {tag_counts['makeup']}",
    f"- High-cost episodes by V1 scene load: {', '.join(high_cost)}",
    "",
    "## Complexity scale",
    "",
    "1–2: standing-set dialogue/task; 3–4: modest extras, props, makeup, or controlled exterior; 5–6: water, stunt, VFX, or fight with containment; 7–8: combined technical departments; 9–10: creature/water/fight combinations requiring previsualization. The score measures coordination, not artistic value.",
    "",
    "## Scene inventory",
    "",
    "| EP | Sc | Location/time | Speaking characters | Extras | Hero props | Animal | Water | Boat | Fight | Stunt | VFX | Creature | Weather | Fire | Blood | Makeup | Score | V1 scene event |",
    "|---|---:|---|---|---|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|---:|---|",
]
for row in scene_rows:
    safe = [cell.replace("|", "/") for cell in row]
    lines.append("| " + " | ".join(safe) + " |")

lines.extend(
    [
        "",
        "## Feasibility findings",
        "",
        "1. The hall cycle EP20–29 is highly feasible if weapons, doors, pillars, stair, dais, service passage, and bedchamber approach are designed once and tracked as a single action geography.",
        "2. The wanderings EP09–15 are the main cost concentration. V2 must use one hero deck, one adaptable shore/cave volume, reusable rock/door units, controlled water foreground, and sound-led offscreen scale.",
        "3. V1’s location labels overstate uniqueness: many beaches, coasts, forest edges, Underworld banks, and island exteriors can share S5 adaptable shore/cave with redress, lens, direction of light, foreground plants, and sound identity.",
        "4. Divine appearances should be condition changes rather than full transformations. Athena can be carried by crowd rhythm, eye-light, costume continuity, and one match cut. Poseidon should be water pressure and sound. Zeus may be offscreen thunder with physical response.",
        "5. Animal work should be isolated into inserts and controlled units: Argos, ram fleece/legs, Helios cattle silhouettes, pig partial transformation, and bird omen plates. No episode requires an uncontrolled herd around principals.",
        "6. EP27–28 require a dedicated hall blocking plan before shooting-script lock. V2 must state ammunition, doors, height, weapon path, and bodies/obstacles continuously.",
        "",
        "The final Production Bible will replace this V1 warning inventory with V2 locked counts and a low-cost shooting order.",
        "",
    ]
)
OUT.write_text("\n".join(lines), encoding="utf-8")
print(f"WROTE {OUT.relative_to(ROOT)} scenes={len(scene_rows)} locations={len(locations)}")
