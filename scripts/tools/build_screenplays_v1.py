from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from screenplay_dialogue_v1 import DIALOGUE


ROOT = Path(__file__).resolve().parents[2]
ADAPTATION_ROOT = ROOT / "adaptation/odyssey_m1_v1"
ADAPTATION_MANIFEST = ADAPTATION_ROOT / "manifest.json"
EXPECTED_ADAPTATION_MANIFEST_SHA256 = "3ace187381786525d4e36cc5dc7991f86344f7cc943a621782efc86c5e0db84a"
OUT = ROOT / "scripts/odyssey_m1_v1"
EPISODES = OUT / "episodes"
FIXED_TIME = "2026-08-15T11:00:00Z"


TIME_LABELS = ["日", "日", "暮", "夜", "夜"]
SCENE_LOCATION_INDEX = {
    1: [0, 0, 0, 0, 1], 2: [0, 0, 0, 1, 1], 3: [0, 1, 1, 1, 2], 4: [0, 0, 0, 1, 2],
    5: [0, 0, 0, 1, 2], 6: [0, 0, 0, 1, 1], 7: [0, 1, 1, 1, 1], 8: [0, 1, 1, 0, 0],
    9: [0, 0, 1, 2, 2], 10: [0, 0, 0, 0, 1], 11: [0, 1, 1, 0, 2], 12: [0, 0, 1, 1, 1],
    13: [0, 1, 1, 1, 1], 14: [0, 0, 0, 1, 1], 15: [0, 0, 0, 1, 2], 16: [0, 0, 0, 1, 2],
    17: [0, 0, 0, 0, 0], 18: [0, 0, 1, 2, 2], 19: [0, 0, 0, 0, 0], 20: [2, 1, 2, 2, 2],
    21: [0, 0, 0, 0, 0], 22: [0, 0, 1, 1, 2], 23: [0, 0, 1, 2, 2], 24: [1, 0, 0, 2, 2],
    25: [0, 0, 1, 0, 0], 26: [0, 1, 1, 1, 1], 27: [0, 0, 0, 1, 1], 28: [1, 0, 0, 0, 2],
    29: [0, 0, 1, 1, 1], 30: [0, 1, 1, 2, 2],
}
FUNCTION_ACTION = {
    "opening_pressure": "空间先于人物发出压力：声响、距离和谁占据中央，都让冲突无需解释便已成立。",
    "escalation": "人物不再停留在判断上。一个可见动作改变相互距离，也把退路压缩成必须回答的问题。",
    "midpoint_reversal": "新事实落地。此前可维持的解释失效，场内每个人都必须重新选择站位和说话方式。",
    "irreversible_turn": "选择被执行而不是宣布；门、武器、道路或身份随之改变，任何人都无法回到本场开始前。",
    "cliffhanger": "最后的动作没有释放压力，只把它交给下一处空间。声音先断，后果仍留在画面里。",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def render_episode(card: dict[str, object]) -> str:
    number = int(card["episode_number"])
    dialogue_scenes = DIALOGUE[number]
    if len(dialogue_scenes) != 5:
        raise SystemExit(f"BLOCKED_DIALOGUE_SCENE_COUNT_EP{number:02d}")
    locations = list(card["locations"])
    source_books = ", ".join(f"Book {book}" for book in card["source_books"])
    source_events = ", ".join(card["source_event_ids"])
    decisions = ", ".join(card["adaptation_decision_ids"])
    lines = [
        f"# EP{number:02d}《{card['title']}》",
        "",
        "- 稿本：SCREENPLAY V1",
        "- 目标时长：约 7 分钟",
        f"- 来源卷次：{source_books}",
        f"- 来源事件：{source_events}",
        f"- 改编决策：{decisions}",
        "- 边界：主要事件、责任与后果取自锁定语料；场面调度、连接动作与中文对白均为 M1 改编表达。",
        "",
        "---",
        "",
        "**淡入。**",
        "",
    ]
    for index, scene in enumerate(card["scene_cards"], start=1):
        location = locations[SCENE_LOCATION_INDEX[number][index - 1]]
        scene_dialogue = dialogue_scenes[index - 1]
        scene_speakers = list(dict.fromkeys(speaker for speaker, _ in scene_dialogue))
        scene_primary = scene_speakers[0]
        scene_counterforce = scene_speakers[1] if len(scene_speakers) > 1 else str(card["counterforce_character"])
        heading_kind = "内景" if any(token in location for token in ["厅", "堂", "宫", "洞", "寝", "屋", "磨坊", "武器", "墙", "洗脚", "侧门", "婚房", "门槛"]) else "外景"
        lines.extend(
            [
                f"## 场 {index}｜{heading_kind}·{location}·{TIME_LABELS[index - 1]}",
                "",
                str(scene["summary"]),
                "",
                FUNCTION_ACTION[str(scene["function"])],
                "",
            ]
        )
        for speaker, spoken in scene_dialogue:
            lines.extend([f"**{speaker}**", "", spoken, ""])
        if index == 1:
            action = f"{scene_primary}没有立刻追问。镜头留在{scene_primary}与{scene_counterforce}之间那段无人愿意先跨过的距离。"
        elif index == 2:
            action = f"{scene_counterforce}先改变了场面方向；{scene_primary}看见变化，仍把下一步做完。"
        elif index == 3:
            action = f"短暂的静默把转折坐实。{scene_primary}收住第一反应，选择一个更危险、也更清醒的回答。"
        elif index == 4:
            action = f"动作完成。{scene_primary}与{scene_counterforce}都明白，刚才那一步不能撤回。"
        else:
            action = f"{card['ending_cliffhanger']}画面在答案出现前切断。"
        lines.extend([action, "", "---", ""])
    lines.extend(
        [
            "**切黑。**",
            "",
            f"**本集钩子：{card['ending_cliffhanger']}**",
            "",
            f"<!-- source-events: {source_events}; adaptation-decisions: {decisions}; invention-class: CONNECTIVE_ACTION_AND_DIALOGUE -->",
        ]
    )
    return "\n".join(lines) + "\n"


def write_episode(number: int) -> Path:
    card_path = ADAPTATION_ROOT / "episode_cards" / f"EP{number:02d}.json"
    card = load(card_path)
    if card.get("status") != "locked":
        raise SystemExit(f"BLOCKED_UNLOCKED_EPISODE_CARD_EP{number:02d}")
    path = EPISODES / f"EP{number:02d}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_episode(card), encoding="utf-8")
    return path


def write_manifest(paths: list[Path]) -> None:
    artifacts = []
    for path in paths:
        raw = path.read_bytes()
        artifacts.append(
            {
                "path": path.relative_to(ROOT).as_posix(),
                "bytes": len(raw),
                "sha256": hashlib.sha256(raw).hexdigest(),
            }
        )
    manifest = {
        "artifact_class": "ctde_30_episode_screenplay_v1_manifest",
        "schema_version": "1.0.0",
        "status": "PASS_30_EPISODE_SCREENPLAY_V1_BUILT",
        "standing_authorization_id": "CTDE-GOAL-COMPLETION-20260815-001",
        "season_id": "ODY-M1-S01-V1",
        "adaptation_manifest_sha256": EXPECTED_ADAPTATION_MANIFEST_SHA256,
        "episode_count": len(paths),
        "target_minutes_per_episode": 7,
        "language": "zh-CN",
        "external_model_calls": 0,
        "greek_tei_content_reads": 0,
        "generated_at": FIXED_TIME,
        "artifacts": artifacts,
        "self_identity": {
            "path": "scripts/odyssey_m1_v1/SCREENPLAY_V1_MANIFEST.json",
            "sha256": None,
            "reason": "self_reference",
        },
    }
    (OUT / "SCREENPLAY_V1_MANIFEST.json").write_text(
        json.dumps(manifest, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--episode", type=int)
    group.add_argument("--all", action="store_true")
    args = parser.parse_args()
    actual_manifest = sha256(ADAPTATION_MANIFEST)
    if actual_manifest != EXPECTED_ADAPTATION_MANIFEST_SHA256:
        raise SystemExit(f"BLOCKED_ADAPTATION_MANIFEST_IDENTITY:{actual_manifest}")
    if set(DIALOGUE) != set(range(1, 31)) or any(len(value) != 5 for value in DIALOGUE.values()):
        raise SystemExit("BLOCKED_SCREENPLAY_DIALOGUE_COVERAGE")
    if args.episode is not None:
        if not 1 <= args.episode <= 30:
            raise SystemExit("BLOCKED_EPISODE_RANGE")
        path = write_episode(args.episode)
        print(f"BUILT_{path.stem}_SCREENPLAY_V1")
        return
    paths = [write_episode(number) for number in range(1, 31)]
    write_manifest(paths)
    print("PASS_30_EPISODE_SCREENPLAY_V1_BUILT")


if __name__ == "__main__":
    main()
