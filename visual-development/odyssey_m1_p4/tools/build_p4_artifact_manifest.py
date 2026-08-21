#!/usr/bin/env python3
"""Freeze the final P4 content payload, excluding self and final result."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
OUT=ROOT/'visual-development/odyssey_m1_p4/P4_ARTIFACT_MANIFEST.json'
ROOTS=[ROOT/'visual-development/odyssey_m1_p4',ROOT/'design/odyssey_m1_p4',ROOT/'storyboards/odyssey_m1_p4',ROOT/'previs/odyssey_m1_p4']
EXCLUDE={OUT.resolve(),(ROOT/'ODYSSEY_P4_FINAL_RESULT.md').resolve()}


def sha(path:Path)->str: return hashlib.sha256(path.read_bytes()).hexdigest()


def main()->None:
    entries=[]
    for base in ROOTS:
        for path in sorted(p for p in base.rglob('*') if p.is_file()):
            if path.resolve() in EXCLUDE or '__pycache__' in path.parts: continue
            entries.append({"path":path.relative_to(ROOT).as_posix(),"bytes":path.stat().st_size,"sha256":sha(path),"suffix":path.suffix.lower()})
    payload='\n'.join(f"{x['sha256']} {x['bytes']} {x['path']}" for x in entries).encode('utf-8')
    doc={"artifact_class":"odyssey_p4_artifact_manifest","schema_version":"1.0.0","baseline_commit":"0c4a403864d9ea89afabceed3c7be7d5819f86c8","artifact_count":len(entries),"entry_payload_sha256":hashlib.sha256(payload).hexdigest(),"entries":entries,"exclusions":["visual-development/odyssey_m1_p4/P4_ARTIFACT_MANIFEST.json (self)","ODYSSEY_P4_FINAL_RESULT.md (final verification record; persistence commit recovered from git)"],"status":"FROZEN_P4_CONTENT_PAYLOAD"}
    OUT.write_text(json.dumps(doc,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')


if __name__=='__main__': main()
