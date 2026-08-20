#!/usr/bin/env python3
"""Build the non-self-referential P3 content artifact manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
P3 = ROOT / "preproduction" / "odyssey_m1_p3"
OUT = P3 / "P3_ARTIFACT_MANIFEST.json"
EXCLUDED = {"P3_ARTIFACT_MANIFEST.json", "P3_FINAL_RESULT.md"}


def digest(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def build() -> dict:
    entries = []
    for path in sorted(P3.rglob("*")):
        if not path.is_file() or path.name in EXCLUDED or "__pycache__" in path.parts or path.suffix not in {".md", ".json", ".py"}:
            continue
        payload = path.read_bytes()
        entries.append({
            "path": path.relative_to(ROOT).as_posix(),
            "bytes": len(payload),
            "sha256": digest(payload),
        })
    entry_payload = (json.dumps(entries, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode()
    return {
        "artifact_class": "odyssey_p3_content_artifact_manifest",
        "schema_version": "1.0.0",
        "status": "PASS_P3_CONTENT_ARTIFACT_MANIFEST",
        "baseline_commit": "17cbd562fae17f55ab075cc8643549cfc6a80eab",
        "artifact_count": len(entries),
        "entry_payload_sha256": digest(entry_payload),
        "exclusions": [
            "P3_ARTIFACT_MANIFEST.json (self)",
            "P3_FINAL_RESULT.md (final verification record; self-containing commit recovered from git)",
        ],
        "entries": entries,
    }


def encoded(value: dict) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    expected = encoded(build())
    if args.check:
        assert OUT.read_bytes() == expected
        print(f"PASS artifacts={build()['artifact_count']} sha256={digest(expected)}")
    else:
        OUT.write_bytes(expected)
        print(f"WROTE artifacts={build()['artifact_count']} sha256={digest(expected)}")


if __name__ == "__main__":
    main()
