#!/usr/bin/env python3
"""Independently recover and verify P4 technical storyboard coverage."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path
from xml.etree import ElementTree as ET

from PIL import Image

ROOT=Path(__file__).resolve().parents[2]
P3=ROOT/'preproduction/odyssey_m1_p3'
OUT=ROOT/'storyboards/odyssey_m1_p4'


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    source=json.load(open(P3/'STORYBOARD_PLAN.json'))
    shots_doc=json.load(open(P3/'SHOT_LIST_MASTER.json'))
    scenes_doc=json.load(open(P3/'SCENE_MASTER_INDEX.json'))
    render=json.load(open(OUT/'STORYBOARD_RENDER_MANIFEST.json'))
    images=json.load(open(OUT/'STORYBOARD_IMAGE_MANIFEST.json'))
    source_ids=[x['frame_id'] for x in source['frames']]; rows=render['frames']; row_ids=[x['frame_id'] for x in rows]
    assert len(source_ids)==711 and len(rows)==711
    assert set(source_ids)==set(row_ids)
    assert not [x for x,n in Counter(row_ids).items() if n>1]
    shot_ids={x['shot_id'] for x in shots_doc['shots']}; scene_ids={x['scene_id'] for x in scenes_doc['scenes']}
    for row in rows:
        assert row['shot_id'] in shot_ids and row['scene_id'] in scene_ids
        path=ROOT/row['path']; assert path.is_file() and sha(path)==row['sha256']; ET.parse(path)
        text=path.read_text(encoding='utf-8'); assert row['frame_id'] in text and row['shot_id'] in text and row['scene_id'] in text
    dispositions=images['scene_dispositions']; assert len(dispositions)==150
    assert sum(x['p3_priority']=='MUST' and x['p4_disposition']=='FULL_TECHNICAL_BOARD' for x in dispositions)==60
    assert sum(x['p3_priority']=='SHOULD' and x['p4_disposition']=='REPRESENTATIVE_TECHNICAL_BOARD' for x in dispositions)==35
    assert sum(x['p3_priority']=='NO' and x['p4_disposition']=='NO_STORYBOARD_REQUIRED' for x in dispositions)==55
    board_scenes={x['scene_id'] for x in images['board_pages']}
    assert {x['scene_id'] for x in dispositions if x['p3_priority']=='MUST'} <= board_scenes
    assert {x['scene_id'] for x in dispositions if x['p3_priority']=='SHOULD'} <= board_scenes
    for asset in images['board_pages']+images['episode_contact_sheets']:
        path=ROOT/asset['path']; assert path.is_file() and sha(path)==asset['sha256']
        with Image.open(path) as im: im.verify()
    assert len(images['episode_contact_sheets'])==30
    print(json.dumps({
        'status':'PASS_TECHNICAL_STORYBOARD_INDEPENDENT_VERIFICATION','planned_frames':711,'rendered_frames':len(rows),
        'missing':0,'duplicates':0,'must_scenes':60,'should_scenes':35,'no_scenes':55,
        'board_pages':len(images['board_pages']),'episode_contacts':len(images['episode_contact_sheets'])
    },sort_keys=True))


if __name__=='__main__':
    main()
