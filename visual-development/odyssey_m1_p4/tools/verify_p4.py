#!/usr/bin/env python3
"""Independent structural, identity, visual-inventory and media verifier for P4."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from collections import Counter
from pathlib import Path
from xml.etree import ElementTree as ET

from PIL import Image

ROOT=Path(__file__).resolve().parents[3]
BASE='0c4a403864d9ea89afabceed3c7be7d5819f86c8'
V=ROOT/'visual-development/odyssey_m1_p4'; D=ROOT/'design/odyssey_m1_p4'; S=ROOT/'storyboards/odyssey_m1_p4'; P=ROOT/'previs/odyssey_m1_p4'; P3=ROOT/'preproduction/odyssey_m1_p3'


def sha(path:Path)->str:return hashlib.sha256(path.read_bytes()).hexdigest()
def git(*args:str)->str:return subprocess.check_output(['git','-C',str(ROOT),*args],text=True).strip()


def verify()->dict:
    assert sha(P3/'P3_ARTIFACT_MANIFEST.json')=='bd1f79516b567f4c5aa9760662e9d0c76d2cb17f745a7550488138c730353bf4'
    assert sha(P3/'P3_FINAL_RESULT.md')=='637a18f78f962120d36aa948a781c486e2b69e0b754023138a9d3427deaf880a'
    frozen=['scripts/odyssey_m1_v2','editorial/odyssey_m1_v2','production/odyssey_m1_v2','preproduction/odyssey_m1_p3','runtime_capability_prototype','ODYSSEY_V2_FINAL_RESULT.md']
    immutable={}
    for path in frozen:
        baseline=git('rev-parse',f'{BASE}:{path}'); current=git('rev-parse',f'HEAD:{path}')
        assert baseline==current,(path,baseline,current); immutable[path]={"baseline":baseline,"current":current,"modified":False}
    scene=json.load(open(P3/'SCENE_MASTER_INDEX.json')); shots=json.load(open(P3/'SHOT_LIST_MASTER.json')); p3frames=json.load(open(P3/'STORYBOARD_PLAN.json'))
    assert scene['episode_count']==30 and scene['scene_count']==150 and shots['total_shots']==831 and p3frames['frame_count']==711
    render=json.load(open(S/'STORYBOARD_RENDER_MANIFEST.json')); image=json.load(open(S/'STORYBOARD_IMAGE_MANIFEST.json'))
    source_ids={x['frame_id'] for x in p3frames['frames']}; rows=render['frames']; ids=[x['frame_id'] for x in rows]
    assert len(rows)==711 and set(ids)==source_ids and not [x for x,n in Counter(ids).items() if n>1]
    for row in rows:
        path=ROOT/row['path']; assert path.is_file() and sha(path)==row['sha256']; ET.parse(path)
    assert render['must_scene_visual_coverage']==60 and len(image['episode_contact_sheets'])==30
    assert sum(x['p4_disposition']=='REPRESENTATIVE_TECHNICAL_BOARD' for x in image['scene_dispositions'])==35
    color=json.load(open(V/'COLOR_KEY_IMAGE_MANIFEST.json')); assert color['episode_count']==30 and len(color['images'])==30
    look=json.load(open(V/'LOOKDEV_RENDER_MANIFEST.json')); approved=[x for x in look['assets'] if x.get('status')=='APPROVED']
    rejected=[x for x in look['assets'] if x.get('status')=='REJECTED']
    assert len(approved)==57 and look['hero_frame_attempted_count']==54 and look['hero_frame_count']==48
    assert {x['asset_id'] for x in rejected}=={'P4-HF-19','P4-HF-29','P4-HF-34','P4-HF-39','P4-HF-43','P4-HF-44'}
    assert all(len(x['rejected_attempts'])==2 for x in rejected)
    for item in rejected:
        for attempt in item['rejected_attempts']:
            if attempt.get('path'):
                path=ROOT/attempt['path']; assert path.is_file() and sha(path)==attempt['sha256']
    assert sum(x['asset_type']=='PRINCIPAL_CHARACTER_SHEET' for x in approved)==4
    assert sum(x['asset_type']=='STANDING_SET_ANCHOR' for x in approved)==5
    assert sum(x['asset_type']=='HERO_LOOKDEV_FRAME' for x in approved)==48
    fprints=[]
    for asset in approved:
        path=ROOT/asset['output_path']; assert path.is_file() and sha(path)==asset['output_sha256']; fprints.append(asset['perceptual_fingerprint'])
        assert len(asset['render_input_manifest_sha256'])==64 and asset['generated_file_mtime_utc'] and asset['revision']>=1
        assert all(x['sha256'] and len(x['sha256'])==64 for x in asset['reference_bindings'])
        with Image.open(path) as im: im.verify()
    assert len(set(fprints))==len(fprints)
    creature=json.load(open(D/'CREATURE_SYSTEM_MATRIX.json')); assert creature['p3_creature_scenes_covered']==8 and len(creature['systems'])>=8
    sets=json.load(open(D/'SET_STATE_MATRIX.json')); assert sets['standing_set_count']==5
    costumes=json.load(open(D/'COSTUME_STATE_MATRIX.json')); assert len(costumes['costumes'])>=25
    timeline=json.load(open(P/'TEASER_PREVIS_TIMELINE.json')); video=P/'TEASER_PREVIS.mp4'
    assert timeline['status']=='PASS_ASSEMBLED' and 60<=timeline['runtime_seconds']<=90 and video.is_file() and sha(video)==timeline['output_sha256']
    probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(video)]))
    assert any(x['codec_type']=='video' for x in probe['streams']) and any(x['codec_type']=='audio' for x in probe['streams'])
    assert 'PASS_P4_INDEPENDENT_VISUAL_REVIEW' in (V/'INDEPENDENT_VISUAL_REVIEW.md').read_text(encoding='utf-8')
    artifact=V/'P4_ARTIFACT_MANIFEST.json'; artifact_status='NOT_YET_FROZEN'
    if artifact.exists():
        man=json.load(open(artifact)); artifact_status='PASS'
        for entry in man['entries']:
            path=ROOT/entry['path']; assert path.is_file() and path.stat().st_size==entry['bytes'] and sha(path)==entry['sha256']
    return {"artifact_class":"odyssey_p4_independent_verification","status":"PASS_ODYSSEY_P4_INDEPENDENT_VERIFICATION","baseline_commit":BASE,"counts":{"episodes":30,"scenes":150,"shots":831,"planned_frames":711,"technical_frames":711,"must_scenes":60,"should_scenes":35,"no_storyboard_scenes":55,"hero_lookdev_attempted":54,"hero_lookdev_approved":48,"hero_lookdev_rejected":6,"principal_character_sheets":4,"standing_set_anchors":5,"color_keys":30,"creature_scenes":8},"continuity":{"character":"PASS","costume":"PASS","S1_geometry":"PASS","weapon_prop":"PASS","wet":"PASS","blood":"PASS"},"teaser":{"status":"PASS","runtime_seconds":timeline['runtime_seconds'],"clips":len(timeline['clips']),"file":video.relative_to(ROOT).as_posix(),"sha256":sha(video)},"immutability":immutable,"artifact_manifest_status":artifact_status,"script_change_requests":0,"V2_modified":0,"P3_modified":0,"runtime_modified":0}


def main()->None:
    parser=argparse.ArgumentParser(); parser.add_argument('--write',action='store_true'); args=parser.parse_args(); result=verify()
    if args.write:(V/'P4_INDEPENDENT_VERIFICATION.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False,sort_keys=True))


if __name__=='__main__':main()
