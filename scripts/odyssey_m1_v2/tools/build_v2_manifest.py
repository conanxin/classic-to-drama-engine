#!/usr/bin/env python3
"""Build or independently check the canonical Odyssey M1 V2 manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
EPISODE_DIR = ROOT / "scripts" / "odyssey_m1_v2" / "episodes"
OUTPUT = ROOT / "scripts" / "odyssey_m1_v2" / "SCREENPLAY_V2_MANIFEST.json"
ARCHITECTURE = ROOT / "adaptation" / "odyssey_m1_v1" / "episode_architecture.json"
V1_ADAPTATION_MANIFEST = ROOT / "adaptation" / "odyssey_m1_v1" / "manifest.json"
V1_SCREENPLAY_MANIFEST = ROOT / "scripts" / "odyssey_m1_v1" / "SCREENPLAY_V1_MANIFEST.json"
V1_SCREENPLAY_VERIFICATION = ROOT / "scripts" / "odyssey_m1_v1" / "SCREENPLAY_V1_VERIFICATION.json"

HAN = re.compile(r"[\u3400-\u9fff]")
SCENE = re.compile(r"^## 场\s*(\d+)｜([^｜]+)｜约\s*(\d+)'(\d+)\"$", re.MULTILINE)
DIALOGUE = re.compile(r"^\*\*([^*]+)\*\*\n\n([^\n]+)", re.MULTILINE)
SOURCE_BOOKS = re.compile(r"^- 来源卷次：(.+)$", re.MULTILINE)
SOURCE_EVENTS = re.compile(r"^- 来源事件：(.+)$", re.MULTILINE)
NON_SPEAKERS = {"淡入。", "淡出。", "切黑。", "全剧终。"}


def digest_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def digest_path(path: Path) -> str:
    return digest_bytes(path.read_bytes())


def han_count(value: str) -> int:
    return len(HAN.findall(value))


def dialogue_blocks(text: str) -> list[tuple[str, str]]:
    return [
        (speaker, line)
        for speaker, line in DIALOGUE.findall(text)
        if speaker not in NON_SPEAKERS and not speaker.startswith("本集钩子")
    ]


def split_items(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


def build_manifest() -> dict[str, object]:
    architecture = json.loads(ARCHITECTURE.read_text(encoding="utf-8"))["episodes"]
    expected = {item["episode_id"]: item for item in architecture}
    artifacts = []

    for number in range(1, 31):
        episode_id = f"EP{number:02d}"
        path = EPISODE_DIR / f"{episode_id}.md"
        payload = path.read_bytes()
        text = payload.decode("utf-8")
        scenes = SCENE.findall(text)
        dialogue = dialogue_blocks(text)
        book_match = SOURCE_BOOKS.search(text)
        event_match = SOURCE_EVENTS.search(text)
        if not book_match or not event_match:
            raise ValueError(f"{episode_id}: missing source binding")
        books = [int(value) for value in re.findall(r"\d+", book_match.group(1))]
        events = split_items(event_match.group(1))
        if books != expected[episode_id]["source_books"]:
            raise ValueError(f"{episode_id}: source book mismatch")
        if events != expected[episode_id]["source_event_ids"]:
            raise ValueError(f"{episode_id}: source event mismatch")
        if len(scenes) != 5:
            raise ValueError(f"{episode_id}: expected five scenes, got {len(scenes)}")

        artifacts.append(
            {
                "bytes": len(payload),
                "chinese_characters": han_count(text),
                "dialogue_characters": sum(han_count(line) for _, line in dialogue),
                "dialogue_cues": len(dialogue),
                "episode_id": episode_id,
                "estimated_runtime_seconds": sum(
                    int(minutes) * 60 + int(seconds) for _, _, minutes, seconds in scenes
                ),
                "path": path.relative_to(ROOT).as_posix(),
                "scene_count": len(scenes),
                "sha256": digest_bytes(payload),
                "source_books": books,
                "source_event_ids": events,
            }
        )

    source_books = sorted({book for artifact in artifacts for book in artifact["source_books"]})
    if source_books != list(range(1, 25)):
        raise ValueError(f"source coverage is not Books 1-24: {source_books}")

    return {
        "artifact_class": "ctde_30_episode_screenplay_v2_manifest",
        "artifacts": artifacts,
        "episode_count": len(artifacts),
        "external_model_calls": 0,
        "greek_tei_content_reads": 0,
        "language": "zh-CN",
        "model_calls": 0,
        "production_draft_level": "director_breakdown_ready",
        "schema_version": "2.0.0",
        "season_id": "ODY-M1-S01-V2",
        "self_identity": {
            "path": "scripts/odyssey_m1_v2/SCREENPLAY_V2_MANIFEST.json",
            "reason": "self_reference",
            "sha256": None,
        },
        "source_books": source_books,
        "status": "PASS_ODYSSEY_SCREENPLAY_V2_PRODUCTION_DRAFT",
        "target_minutes_per_episode": 7,
        "totals": {
            "chinese_characters": sum(artifact["chinese_characters"] for artifact in artifacts),
            "dialogue_characters": sum(artifact["dialogue_characters"] for artifact in artifacts),
            "dialogue_cues": sum(artifact["dialogue_cues"] for artifact in artifacts),
            "estimated_runtime_seconds": sum(
                artifact["estimated_runtime_seconds"] for artifact in artifacts
            ),
            "scene_count": sum(artifact["scene_count"] for artifact in artifacts),
        },
        "v1_baseline_commit": "fb8de1f77dd2d50f742c839a9ddb8fe29d4455e2",
        "v1_identity_locks": {
            "adaptation_manifest_sha256": digest_path(V1_ADAPTATION_MANIFEST),
            "screenplay_manifest_sha256": digest_path(V1_SCREENPLAY_MANIFEST),
            "screenplay_verification_sha256": digest_path(V1_SCREENPLAY_VERIFICATION),
        },
        "v1_paths_modified": 0,
    }


def canonical_bytes(manifest: dict[str, object]) -> bytes:
    return (json.dumps(manifest, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode(
        "utf-8"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    arguments = parser.parse_args()
    expected = canonical_bytes(build_manifest())
    if arguments.check:
        actual = OUTPUT.read_bytes()
        if actual != expected:
            raise SystemExit("SCREENPLAY_V2_MANIFEST.json is not canonical or is stale")
        print(f"PASS {digest_bytes(actual)} {len(actual)} bytes")
        return
    OUTPUT.write_bytes(expected)
    print(f"WROTE {OUTPUT.relative_to(ROOT)} {digest_bytes(expected)} {len(expected)} bytes")


if __name__ == "__main__":
    main()
