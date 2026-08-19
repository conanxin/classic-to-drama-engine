#!/usr/bin/env python3
"""Read-only editorial metrics for the Odyssey M1 V2 screenplay."""

from __future__ import annotations

import collections
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
EPISODE_DIR = ROOT / "scripts" / "odyssey_m1_v2" / "episodes"
ARCHITECTURE = ROOT / "adaptation" / "odyssey_m1_v1" / "episode_architecture.json"

HAN = re.compile(r"[\u3400-\u9fff]")
SCENE = re.compile(r"^## 场\s*(\d+)｜([^｜]+)｜约\s*(\d+)'(\d+)\"$", re.MULTILINE)
DIALOGUE = re.compile(r"^\*\*([^*]+)\*\*\n\n([^\n]+)", re.MULTILINE)

BANNED_META = (
    "空间先于人物发出压力",
    "人物不再停留在判断上",
    "一个可见动作改变相互距离",
    "新事实落地",
    "选择被执行而不是宣布",
    "短暂的静默把转折坐实",
    "最后的动作没有释放压力",
    "画面在答案出现前切断",
    "先改变了场面方向",
    "没有立刻追问",
    "都明白，刚才那一步不能撤回",
)

SHORTCUTS = ("沉默", "看着", "转身", "没有回答", "终于", "从今晚起", "别等")
NON_SPEAKERS = {"淡入。", "淡出。", "切黑。", "全剧终。"}


def han_count(value: str) -> int:
    return len(HAN.findall(value))


def dialogue_blocks(text: str) -> list[tuple[str, str]]:
    return [
        (speaker, line)
        for speaker, line in DIALOGUE.findall(text)
        if speaker not in NON_SPEAKERS and not speaker.startswith("本集钩子")
    ]


def main() -> None:
    architecture = json.loads(ARCHITECTURE.read_text(encoding="utf-8"))["episodes"]
    expected = {episode["episode_id"]: episode for episode in architecture}

    episodes = []
    exact_lines: collections.Counter[str] = collections.Counter()
    scene_openings: collections.Counter[str] = collections.Counter()
    dialogue_ngrams: collections.Counter[str] = collections.Counter()
    action_ngrams: collections.Counter[str] = collections.Counter()
    hooks: collections.Counter[str] = collections.Counter()
    speaker_chars: collections.Counter[str] = collections.Counter()
    shortcut_counts: collections.Counter[str] = collections.Counter()
    banned_counts: collections.Counter[str] = collections.Counter()
    symmetric_triples = 0
    dialogue_triples = 0
    consecutive_same_speaker = 0
    exactly_three_cue_scenes = 0
    exactly_three_cue_a_b_a_scenes = 0
    adjacent_same_speaker_without_action = []

    for number in range(1, 31):
        episode_id = f"EP{number:02d}"
        path = EPISODE_DIR / f"{episode_id}.md"
        text = path.read_text(encoding="utf-8")
        scenes = SCENE.findall(text)
        blocks = dialogue_blocks(text)
        raw_blocks = [
            match
            for match in DIALOGUE.finditer(text)
            if match.group(1) not in NON_SPEAKERS and not match.group(1).startswith("本集钩子")
        ]
        for left, right in zip(raw_blocks, raw_blocks[1:]):
            if left.group(1) == right.group(1) and not text[left.end() : right.start()].strip():
                adjacent_same_speaker_without_action.append(
                    {
                        "episode_id": episode_id,
                        "speaker": left.group(1),
                        "first_line": left.group(2),
                        "second_line": right.group(2),
                    }
                )
        runtime_seconds = sum(int(minutes) * 60 + int(seconds) for _, _, minutes, seconds in scenes)

        for speaker, line in blocks:
            compact = re.sub(r"\s+", "", line)
            exact_lines[compact] += 1
            speaker_chars[speaker] += han_count(line)
            han_only = "".join(HAN.findall(line))
            dialogue_ngrams.update(set(han_only[index : index + 8] for index in range(max(0, len(han_only) - 7))))

        speakers = [speaker for speaker, _ in blocks]
        consecutive_same_speaker += sum(left == right for left, right in zip(speakers, speakers[1:]))
        dialogue_triples += max(0, len(speakers) - 2)
        symmetric_triples += sum(
            first == third and first != middle
            for first, middle, third in zip(speakers, speakers[1:], speakers[2:])
        )

        scene_chunks = re.split(r"^## 场[^\n]+\n", text, flags=re.MULTILINE)[1:]
        for chunk in scene_chunks:
            scene_speakers = [speaker for speaker, _ in dialogue_blocks(chunk)]
            if len(scene_speakers) == 3:
                exactly_three_cue_scenes += 1
                if scene_speakers[0] == scene_speakers[2] and scene_speakers[0] != scene_speakers[1]:
                    exactly_three_cue_a_b_a_scenes += 1
            prose = [
                line.strip()
                for line in chunk.splitlines()
                if line.strip()
                and not line.startswith("<!--")
                and not line.startswith("**")
                and not line.startswith("#")
            ]
            if prose:
                first_sentence = re.split(r"[。！？]", prose[0])[0]
                scene_openings[first_sentence] += 1
                for paragraph in prose:
                    han_only = "".join(HAN.findall(paragraph))
                    action_ngrams.update(set(han_only[index : index + 10] for index in range(max(0, len(han_only) - 9))))

        hook_match = re.search(r"^\*\*本集钩子：(.+)\*\*$", text, re.MULTILINE)
        if hook_match:
            hooks[hook_match.group(1)] += 1

        for phrase in BANNED_META:
            banned_counts[phrase] += text.count(phrase)
        for phrase in SHORTCUTS:
            shortcut_counts[phrase] += text.count(phrase)

        source_events_match = re.search(r"^- 来源事件：(.+)$", text, re.MULTILINE)
        declared_events = []
        if source_events_match:
            declared_events = [item.strip() for item in source_events_match.group(1).split(",")]

        episodes.append(
            {
                "episode_id": episode_id,
                "scene_count": len(scenes),
                "runtime_seconds": runtime_seconds,
                "chinese_characters": han_count(text),
                "dialogue_characters": sum(han_count(line) for _, line in blocks),
                "dialogue_cues": len(blocks),
                "source_events_exact": declared_events == expected[episode_id]["source_event_ids"],
            }
        )

    repeated_lines = [
        {"line": line, "count": count}
        for line, count in exact_lines.most_common()
        if count > 1 and len(line) >= 4
    ]
    repeated_openings = [
        {"opening": line, "count": count}
        for line, count in scene_openings.most_common()
        if count > 1 and len(line) >= 4
    ]
    repeated_dialogue_ngrams = [
        {"ngram": ngram, "count": count}
        for ngram, count in dialogue_ngrams.most_common()
        if count >= 3
    ]
    repeated_action_ngrams = [
        {"ngram": ngram, "count": count}
        for ngram, count in action_ngrams.most_common()
        if count >= 3
    ]
    repeated_hooks = [
        {"hook": hook, "count": count}
        for hook, count in hooks.most_common()
        if count > 1
    ]

    report = {
        "episodes": len(episodes),
        "scenes": sum(item["scene_count"] for item in episodes),
        "dialogue_cues": sum(item["dialogue_cues"] for item in episodes),
        "chinese_characters": sum(item["chinese_characters"] for item in episodes),
        "dialogue_characters": sum(item["dialogue_characters"] for item in episodes),
        "estimated_runtime_seconds": sum(item["runtime_seconds"] for item in episodes),
        "runtime_min_seconds": min(item["runtime_seconds"] for item in episodes),
        "runtime_max_seconds": max(item["runtime_seconds"] for item in episodes),
        "all_five_scenes": all(item["scene_count"] == 5 for item in episodes),
        "all_dialogue_in_locked_range": all(450 <= item["dialogue_characters"] <= 850 for item in episodes),
        "all_source_events_exact": all(item["source_events_exact"] for item in episodes),
        "banned_meta_occurrences": dict(banned_counts),
        "shortcut_occurrences": dict(shortcut_counts),
        "repeated_exact_dialogue_lines": repeated_lines,
        "repeated_dialogue_8han_ngrams_at_least_3": repeated_dialogue_ngrams,
        "repeated_action_10han_ngrams_at_least_3": repeated_action_ngrams,
        "repeated_scene_openings": repeated_openings,
        "repeated_hooks": repeated_hooks,
        "consecutive_same_speaker_cues": consecutive_same_speaker,
        "a_b_a_speaker_triples": symmetric_triples,
        "dialogue_triples": dialogue_triples,
        "a_b_a_triple_ratio": round(symmetric_triples / dialogue_triples, 4) if dialogue_triples else 0,
        "exactly_three_cue_scenes": exactly_three_cue_scenes,
        "exactly_three_cue_a_b_a_scenes": exactly_three_cue_a_b_a_scenes,
        "adjacent_same_speaker_without_action": adjacent_same_speaker_without_action,
        "speaker_dialogue_characters": dict(speaker_chars.most_common()),
        "episode_metrics": episodes,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
