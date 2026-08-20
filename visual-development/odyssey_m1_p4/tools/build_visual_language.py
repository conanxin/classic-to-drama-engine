#!/usr/bin/env python3
"""Build deterministic P4 color and style authorities from curated records."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "visual-development" / "odyssey_m1_p4"

EPISODES = [
    (1, "没有父亲的家", "occupied ochre", "wine rust", "warm-stale", "restrained", "deep ash", "olive-warm", "worn bronze", "sea only in sound", "low hearth", "none", "old purple thread", ["#6f5738", "#9a4f3f", "#2b2924", "#66504f", "#b09a72"]),
    (2, "伊萨卡第一次集会", "sun-bleached ochre", "civic dust", "warm-open", "restrained", "charcoal", "dry neutral", "dull bronze", "cold horizon", "none", "Athena air pause", "new sail white", ["#aa8a5d", "#7f6b55", "#313234", "#657b7b", "#d1c5a4"]),
    (3, "皮洛斯的火", "sacrificial ember", "shore chalk", "hot/cool", "moderate", "smoke black", "fire-warm", "fire bronze", "distant steel-blue", "ritual ember", "Athena rhythm", "clean red ember", ["#8d3f2b", "#c4a77c", "#262626", "#52666c", "#d87942"]),
    (4, "记忆的宫殿", "faded red textile", "cold polished wood", "warm/cool split", "muted", "ink brown", "controlled warm", "polished but scarred", "reported blue-grey", "lamp amber", "memory pause", "blue repair hint", ["#844b45", "#73665c", "#292522", "#566979", "#b48762"]),
    (5, "不死也不回家", "salt grey", "olive green", "cool exposed", "low", "storm black", "weathered cool", "rope/timber only", "lead green", "shelter ember", "conditioned stillness", "living olive", ["#717772", "#5d6448", "#20272b", "#445a5c", "#a07c56"]),
    (6, "河边的陌生人", "river chalk", "sea-glass blue", "cool clearing", "soft", "wet umber", "rewarming", "minimal", "pale blue", "none", "Athena reflected lift", "blue repair thread", ["#b9b7a0", "#5f8587", "#4a514d", "#857764", "#d2c6a5"]),
    (7, "王后的膝前", "chalk and cedar", "sea-glass", "balanced cool", "moderate", "cedar brown", "warm under scrutiny", "hand-polished bronze", "architectural blue", "oil points", "crowd timing", "borrowed cloth blue", ["#c2b58f", "#607d82", "#4a392c", "#8d6f50", "#e0cfaa"]),
    (8, "说出你的名字", "court chalk", "Trojan rust", "cool/warm fracture", "moderate", "deep brown", "held warm", "sport bronze", "bright lateral", "low lamp", "song-triggered pause", "name/face warmth", ["#b8ab8c", "#9a5a47", "#41382f", "#5f7884", "#d3a26f"]),
    (9, "无人进入洞穴", "tar umber", "cave soot", "warm collapsing", "low", "near black", "smoke-warm", "dirty bronze", "small mouth blue", "stake fire", "none", "wine-black red", ["#564331", "#312d29", "#121516", "#7b563d", "#9b3f32"]),
    (10, "我的名字叫无人", "cave black", "blood rust", "hot center/cold mouth", "selective", "crushed black", "fire and fear", "soot bronze", "exit slit blue", "heated stake", "Poseidon echo after boast", "eye blood rust", ["#211e1b", "#78372e", "#aa6b3f", "#364b50", "#b59069"]),
    (11, "看得见伊萨卡", "wind-bag ochre", "home green", "warm hope/cold rupture", "moderate", "storm charcoal", "salt warm then cold", "rope hardware", "visible olive-blue", "none", "wind reverses unnaturally", "nine knots", ["#987344", "#607055", "#2b3234", "#657f83", "#d1b477"]),
    (12, "喀耳刻的杯", "poison green", "clay red", "warm interior/green edge", "controlled", "moss black", "seductive warm", "small polished edge", "absent", "hearth/cup", "Athena herb clarity", "cup reflection", ["#4f6848", "#934f3f", "#252c24", "#b08a5f", "#d5c89a"]),
    (13, "死者要血", "black reflection", "blood warmth", "cold void/warm trench", "very low except blood", "absolute black", "edge-muted", "none", "none", "blood glow practical", "impossible depth", "scar rose", ["#101315", "#5b1f23", "#34272b", "#9c574d", "#b8a58d"]),
    (14, "绑在桅杆上", "rope flax", "sea iron", "cold hard", "desaturated", "storm navy-black", "wind-cool", "dull wet bronze", "slate/foam", "none", "sound pressure", "six bone ivory", ["#a28d68", "#485b63", "#202a31", "#7c715f", "#d4c6a5"]),
    (15, "最后一条船", "famine ash", "forbidden cattle gold", "sick warm/cold storm", "low", "thunder black", "hollow neutral", "minimal", "green-black", "lightning only", "Zeus pressure", "last sail white", ["#665e4f", "#9a7a3d", "#24272a", "#475a5c", "#b7a883"]),
    (16, "睡着回到故乡", "Ithaca mud", "transport cloth blue", "cool dawn to olive", "muted", "soft charcoal", "rewarmed dust", "treasure muted", "sea receding", "none", "Athena shadow error", "hidden gold/olive", ["#776b52", "#617879", "#3d4037", "#998668", "#c3b690"]),
    (17, "忠诚住在猪圈", "earth brown", "animal heat", "warm worked", "low-moderate", "smoke umber", "fire-warm", "tool iron", "distant grey", "small work fire", "none", "patched cloth", ["#6d4f37", "#8a6746", "#332b25", "#9c865f", "#c2a97e"]),
    (18, "儿子穿过伏击", "road dust", "sea ambush blue", "warm land/cold threat", "muted", "olive black", "travel-warm", "sword dull", "compressed blue", "none", "Athena route rhythm", "black nail", ["#8b7656", "#4f6970", "#293232", "#6b684e", "#b9a47b"]),
    (19, "父亲显形", "farm umber", "divine pale edge", "warm close", "restrained", "brown-black", "shared warm", "sword held dark", "absent", "hearth", "brief structural lift", "scar/belt evidence", ["#6f5038", "#b1a98d", "#302923", "#897458", "#c7b68e"]),
    (20, "狗认出了国王", "Ithaca dust", "old collar leather", "dry warm", "low", "doorway black", "weathered neutral", "worn bronze", "heard only", "H0 low", "none", "Argos eye/collar", ["#806b4e", "#59483b", "#302d28", "#a08c66", "#b9aa8a"]),
    (21, "乞丐之王", "wine rust", "beggar mud", "warm hostile", "moderate", "deep olive", "uneven warm", "soft wealth bronze", "absent", "hearth", "none", "ledger clay", ["#8c4938", "#685845", "#282722", "#a07a56", "#c2a97a"]),
    (22, "把武器藏起来", "empty-hook ash", "key bronze", "night warm/cold", "low", "blocked black", "lamp warm", "brief edge flashes", "absent", "oil lamp", "Athena impossible shadow", "blue repair thread", ["#5d594f", "#8b7148", "#252726", "#6e604f", "#b2a17c"]),
    (23, "伤疤没有撒谎", "basin grey", "scar rose", "warm intimate", "very restrained", "soft brown-black", "human warm", "basin bronze", "absent", "one lamp", "none", "scar rose/old purple", ["#77756b", "#8e5a52", "#302a27", "#aa8c72", "#c5b8a2"]),
    (24, "最后一次忍耐", "meal ochre", "omen charcoal", "stale warm", "low", "dense ash", "held neutral", "weapons absent", "heard pressure", "hearth", "condition not spectacle", "door/key mark", ["#846b47", "#4c4a43", "#282823", "#9d7c55", "#b7a777"]),
    (25, "无人拉开的弓", "contest flax", "bow honey", "warm controlled", "moderate", "plaster charcoal", "even public", "axe bronze", "absent", "H0 low", "none", "old purple + bow", ["#a58c63", "#845d37", "#33302a", "#9f7e52", "#d0b88a"]),
    (26, "箭穿过十二把斧", "axe bronze", "first-blood red", "hard warm", "selective", "deep soot", "tense warm", "ring highlights", "absent", "H0", "air stops after string", "arrow white", ["#7b633e", "#733129", "#28241f", "#b08a55", "#c7b48a"]),
    (27, "厅堂审判·上", "bronze/soot", "blood B2-B3", "hard zones", "moderate", "crushed aisle black", "mixed fire/door", "impact bronze", "absent", "spilled hearth", "none", "arrow inventory", ["#554735", "#782f29", "#24221f", "#8d6b42", "#b19a72"]),
    (28, "厅堂审判·下", "ash bronze", "blood B4-B5", "smoke warm/cool", "low-moderate", "smoke black", "fatigued neutral", "scarred bronze", "absent", "sulfur/fire", "Athena shield shadow", "lowered weapons", ["#50483d", "#6d302b", "#292a27", "#8e7657", "#b9aa90"]),
    (29, "搬走我们的床", "olive wood", "old purple", "warm close", "restrained", "soft umber", "cleaned not reset", "minimal", "absent", "one oil lamp", "none", "root-green/wood gold", ["#6e6547", "#604553", "#312a25", "#a48d66", "#c3b69a"]),
    (30, "归途之后", "worked earth", "undyed white", "open warm", "moderate natural", "lifted ash", "honest sun", "three weapon patinas", "distant calm", "small household ember", "Athena crowd stillness", "purple joined to white", ["#756344", "#c8bda0", "#414036", "#8b7b57", "#a05f55"]),
]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    path = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc" if bold else "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"
    return ImageFont.truetype(path, size)


def make_color_keys(records: list[dict[str, object]]) -> None:
    key_dir = OUT / "color_keys"
    key_dir.mkdir(exist_ok=True)
    rows = []
    for idx, record in enumerate(records, start=1):
        palette = [tuple(bytes.fromhex(x.removeprefix("#"))) for x in record["palette_hex"]]
        image = Image.new("RGB", (1280, 720), palette[2])
        draw = ImageDraw.Draw(image)
        # Deterministic atmosphere: horizon, wall/work plane, light leak, five exact swatches.
        for y in range(720):
            t = y / 719
            a = palette[2] if t < 0.54 else palette[0]
            b = palette[0] if t < 0.54 else palette[4]
            u = (t / 0.54) if t < 0.54 else ((t - 0.54) / 0.46)
            c = tuple(round(a[k] * (1-u) + b[k] * u) for k in range(3))
            draw.line((0, y, 1280, y), fill=c)
        seed = int(hashlib.sha256(record["episode"].encode()).hexdigest()[:8], 16)
        for n in range(34):
            x = (seed * (n + 7) * 37) % 1280
            y = 110 + (seed * (n + 11) * 19) % 470
            length = 80 + (seed >> (n % 13)) % 280
            draw.line((x, y, min(1279, x + length), y + (n % 5) - 2), fill=palette[(n + idx) % 5], width=1)
        draw.rectangle((0, 0, 1280, 94), fill=(20, 20, 18))
        draw.text((38, 25), f"{record['episode']}  {record['title']}", font=font(33, True), fill=(238, 233, 218))
        draw.text((40, 125), str(record["dominant_family"]).upper(), font=font(46, True), fill=palette[4])
        draw.text((42, 187), f"{record['temperature']} / {record['saturation']}", font=font(23), fill=(235, 227, 206))
        labels = ["DOMINANT", "SECONDARY", "BLACK", "ACCENT", "SKIN/LIGHT"]
        for n, (hex_value, color) in enumerate(zip(record["palette_hex"], palette)):
            x0 = 40 + n * 235
            draw.rectangle((x0, 574, x0 + 205, 666), fill=color, outline=(220, 214, 197), width=2)
            text_color = (245, 243, 236) if sum(color) < 360 else (28, 27, 24)
            draw.text((x0 + 12, 589), labels[n], font=font(16, True), fill=text_color)
            draw.text((x0 + 12, 623), hex_value.upper(), font=font(18), fill=text_color)
        draw.text((830, 132), f"recognition: {record['recognition_accent']}", font=font(19), fill=(235, 227, 206))
        draw.text((830, 166), f"divine: {record['divine_exception']}", font=font(19), fill=(235, 227, 206))
        path = key_dir / f"{record['episode']}_COLOR_KEY.png"
        image.save(path, optimize=True)
        rows.append({"episode": record["episode"], "path": path.relative_to(ROOT).as_posix(), "sha256": digest(path), "width": 1280, "height": 720, "classification": "COLOR_KEY"})
    (OUT / "COLOR_KEY_IMAGE_MANIFEST.json").write_text(json.dumps({
        "artifact_class": "odyssey_p4_color_key_image_manifest",
        "episode_count": 30,
        "images": rows,
        "status": "PASS_COLOR_KEYS_30_OF_30",
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    thumb_w, thumb_h = 320, 180
    sheet = Image.new("RGB", (thumb_w * 5, thumb_h * 6), (18, 18, 17))
    for n, row in enumerate(rows):
        im = Image.open(ROOT / row["path"]).resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
        sheet.paste(im, ((n % 5) * thumb_w, (n // 5) * thumb_h))
    sheet.save(OUT / "COLOR_SCRIPT_CONTACT_SHEET.png", optimize=True)


def main() -> None:
    records = []
    for row in EPISODES:
        (episode, title, dominant, secondary, temp, saturation, black, skin, metal,
         sea, fire, divine, recognition, palette) = row
        records.append({
            "episode": f"EP{episode:02d}", "title": title,
            "dominant_family": dominant, "secondary_family": secondary,
            "temperature": temp, "saturation": saturation, "black_level": black,
            "skin_treatment": skin, "metal_treatment": metal,
            "sea_treatment": sea, "fire_treatment": fire,
            "divine_exception": divine, "recognition_accent": recognition,
            "palette_hex": palette,
        })

    payload = {
        "artifact_class": "odyssey_p4_color_script",
        "schema_version": "1.0.0",
        "episode_count": len(records),
        "progression": ["absence", "journey", "self-narration", "concealment", "recognition", "violence", "restoration"],
        "episodes": records,
        "status": "FROZEN_30_OF_30_COLOR_SCRIPT",
    }
    json_path = OUT / "COLOR_SCRIPT.json"
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = ["# 30-Episode Color Script", "", "Status: `FROZEN_30_OF_30_COLOR_SCRIPT`", "",
             "Progression: absence → journey → self-narration → concealment → recognition → violence → restoration.", "",
             "| Episode | Dominant / secondary | Temperature / saturation | Black / skin | Sea / fire | Divine exception | Recognition accent | Palette |",
             "|---|---|---|---|---|---|---|---|"]
    for r in records:
        lines.append(f"| {r['episode']} {r['title']} | {r['dominant_family']} / {r['secondary_family']} | {r['temperature']} / {r['saturation']} | {r['black_level']} / {r['skin_treatment']} | {r['sea_treatment']} / {r['fire_treatment']} | {r['divine_exception']} | {r['recognition_accent']} | {' '.join(r['palette_hex'])} |")
    lines += ["", "The palette is a continuity constraint, not a grade preset. Skin remains human; metal follows custody and damage; sea/fire/divinity may override the base only for the declared condition.", ""]
    md_path = OUT / "COLOR_SCRIPT.md"
    md_path.write_text("\n".join(lines), encoding="utf-8")
    make_color_keys(records)

    style = {
        "artifact_class": "odyssey_p4_visual_style_manifest",
        "schema_version": "1.0.0",
        "baseline_commit": "0c4a403864d9ea89afabceed3c7be7d5819f86c8",
        "p3_manifest_sha256": "bd1f79516b567f4c5aa9760662e9d0c76d2cb17f745a7550488138c730353bf4",
        "p3_final_result_sha256": "637a18f78f962120d36aa948a781c486e2b69e0b754023138a9d3427deaf880a",
        "look_bible_sha256": digest(OUT / "LOOK_BIBLE.md"),
        "color_script_sha256": digest(json_path),
        "lighting_script_sha256": digest(OUT / "LIGHTING_SCRIPT.md"),
        "material_language_sha256": digest(OUT / "MATERIAL_LANGUAGE.md"),
        "motif_atlas_sha256": digest(OUT / "VISUAL_MOTIF_ATLAS.md"),
        "immutable_bindings": {
            "episodes": 30, "scenes": 150, "shots": 831, "planned_storyboard_frames": 711,
            "p3_s1_geometry": "FROZEN", "p3_shot_ids": "FROZEN", "v2_story": "FROZEN"
        },
        "visual_rules": {
            "world": ["lived-in", "salted", "worked", "woven", "smoked", "weathered", "handled", "repaired"],
            "exclude": ["generic Hollywood Greece", "white marble fantasy", "generic fantasy armor", "blue-orange blockbuster", "continuous magic glow", "celebrity likeness"],
            "high_fidelity_method": "Codex integrated ImageGen",
            "technical_method": "deterministic project SVG and Pillow/OpenCV",
            "full_cg_hero_creature_required": False,
        },
        "status": "FROZEN_P4_VISUAL_LANGUAGE",
    }
    (OUT / "VISUAL_STYLE_MANIFEST.json").write_text(json.dumps(style, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
