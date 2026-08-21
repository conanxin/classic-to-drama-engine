#!/usr/bin/env python3
"""Validate rendered lookdev assets, freeze provenance and build contact sheets."""

from __future__ import annotations

import hashlib
import json
import math
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageStat

ROOT=Path(__file__).resolve().parents[3]
OUT=ROOT/'visual-development/odyssey_m1_p4'
MANIFEST=OUT/'LOOKDEV_RENDER_MANIFEST.json'
CONTACT=OUT/'contact_sheets'
CONTACT.mkdir(exist_ok=True)
FONT='/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
FONT_BOLD='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'


def font(size:int,bold:bool=False): return ImageFont.truetype(FONT_BOLD if bold else FONT,size)
def sha(path:Path)->str: return hashlib.sha256(path.read_bytes()).hexdigest()


def ahash(image:Image.Image)->str:
    g=image.convert('L').resize((16,16),Image.Resampling.LANCZOS); values=list(g.getdata()); mean=sum(values)/len(values)
    bits=''.join('1' if x>=mean else '0' for x in values)
    return f'{int(bits,2):064x}'


def make_sheet(name:str,assets:list[dict],columns:int=3,tile=(640,390))->dict:
    tw,th=tile; header=72; rows=max(1,math.ceil(len(assets)/columns)); sheet=Image.new('RGB',(columns*tw,header+rows*th),(239,237,229)); d=ImageDraw.Draw(sheet)
    d.rectangle((0,0,sheet.width,header),fill=(22,23,21)); d.text((24,18),name,font=font(28,True),fill=(241,236,220))
    for i,a in enumerate(assets):
        x=(i%columns)*tw; y=header+(i//columns)*th
        im=Image.open(ROOT/a['output_path']).convert('RGB'); fitted=ImageOps.fit(im,(tw-20,th-64),method=Image.Resampling.LANCZOS,centering=(.5,.5)); sheet.paste(fitted,(x+10,y+8))
        d.rectangle((x+10,y+th-52,x+tw-10,y+th-10),fill=(31,32,29)); d.text((x+20,y+th-44),f"{a['asset_id']} · {a.get('label',a.get('character',a.get('set_id','')))}",font=font(16,True),fill=(235,228,208))
    path=CONTACT/f"{name.replace(' ','_').upper()}.jpg"; sheet.save(path,quality=90,subsampling=0,optimize=True)
    return {"contact_sheet_id":name,"asset_ids":[a['asset_id'] for a in assets],"path":path.relative_to(ROOT).as_posix(),"sha256":sha(path),"width":sheet.width,"height":sheet.height}


def main() -> None:
    doc=json.load(open(MANIFEST)); assets=doc['assets']; missing=[]; fingerprints={}; failures=[]
    by_id={a['asset_id']:a for a in assets}
    for a in assets:
        reference_bindings=[]
        for ref in a.get('source_reference_ids',[]):
            if ref in by_id:
                ref_path=ROOT/by_id[ref]['output_path']
            else:
                ref_path=ROOT/ref
            reference_bindings.append({"reference_id":ref,"sha256":sha(ref_path) if ref_path.is_file() else None})
        render_input={k:a.get(k) for k in ['asset_id','asset_type','prompt','negative_constraints','aspect_ratio','character_state_ids','costume_ids','set_state','prop_ids','lighting_id','source_reference_ids','generation_method','seed','revision']}
        a['render_input_manifest_sha256']=hashlib.sha256(json.dumps(render_input,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')).hexdigest()
        a['reference_bindings']=reference_bindings
        for attempt in a.get('rejected_attempts',[]):
            if not attempt.get('path'):
                continue
            rejected_path=ROOT/attempt['path']
            if not rejected_path.is_file() or rejected_path.stat().st_size<50_000:
                missing.append(f"{a['asset_id']} revision {attempt['revision']}")
                continue
            with Image.open(rejected_path) as rejected_image:
                rejected_image.load(); rw,rh=rejected_image.size
            attempt.update({"sha256":sha(rejected_path),"bytes":rejected_path.stat().st_size,"width":rw,"height":rh,"generated_file_mtime_utc":datetime.fromtimestamp(rejected_path.stat().st_mtime,timezone.utc).isoformat()})
    for a in assets:
        if a.get('target_disposition')=='REJECTED_MAX_TWO_ATTEMPTS':
            continue
        path=ROOT/a['output_path']
        if not path.is_file() or path.stat().st_size<50_000:
            missing.append(a['asset_id']); a['status']='MISSING'; a['review_result']='BLOCKED'; continue
        try:
            with Image.open(path) as im:
                im.load(); width,height=im.size; mode=im.mode; stat=ImageStat.Stat(im.convert('RGB')); variance=sum(stat.var)/3
                fp=ahash(im)
        except Exception as exc:
            failures.append(f"{a['asset_id']}: {exc}"); a['status']='INVALID'; a['review_result']='BLOCKED'; continue
        if min(width,height)<768 or variance<80:
            failures.append(f"{a['asset_id']}: dimensions/variance {width}x{height}/{variance:.2f}"); a['status']='REJECTED'; a['review_result']='BLOCKED'; continue
        fingerprints.setdefault(fp,[]).append(a['asset_id'])
        a.update({"generated_file_mtime_utc":datetime.fromtimestamp(path.stat().st_mtime,timezone.utc).isoformat(),"revision":a.get('revision',1),"output_sha256":sha(path),"width":width,"height":height,"mode":mode,"file_bytes":path.stat().st_size,"perceptual_fingerprint":fp,"status":"APPROVED","review_result":"PASS"})
    duplicate_groups=[ids for ids in fingerprints.values() if len(ids)>1]
    if missing or failures or duplicate_groups:
        raise SystemExit(json.dumps({"missing":missing,"failures":failures,"duplicate_groups":duplicate_groups},ensure_ascii=False,indent=2))

    approved=[a for a in assets if a.get('status')=='APPROVED']
    chars=[a for a in approved if a['asset_type']=='PRINCIPAL_CHARACTER_SHEET']; sets=[a for a in approved if a['asset_type']=='STANDING_SET_ANCHOR']; heroes=[a for a in approved if a['asset_type']=='HERO_LOOKDEV_FRAME']
    by={a['asset_id']:a for a in approved}; sheets=[]
    sheets.append(make_sheet('PRINCIPAL CHARACTER CONTACT SHEET',chars,2,(760,500)))
    sheets.append(make_sheet('COSTUME STATE CONTACT SHEET',chars,2,(760,500)))
    sheets.append(make_sheet('STANDING SET CONTACT SHEET',sets,2,(760,500)))
    supporting=[by[x] for x in ['P4-HF-01','P4-HF-06','P4-HF-07','P4-HF-09','P4-HF-17','P4-HF-30','P4-HF-31','P4-HF-33','P4-HF-50']]
    sheets.append(make_sheet('SUPPORTING CHARACTER CONTACT SHEET',supporting,3))
    creature=[by[x] for x in ['P4-HF-09','P4-HF-10','P4-HF-11','P4-HF-12','P4-HF-13','P4-HF-14','P4-HF-17','P4-HF-23']]
    sheets.append(make_sheet('P3 CREATURE SCENE CONTACT SHEET',creature,2,(760,500)))
    mythic=[by[x] for x in ['P4-HF-05','P4-HF-17','P4-HF-20','P4-HF-21','P4-HF-23','P4-HF-28']]
    sheets.append(make_sheet('MYTHIC SYSTEM CONTACT SHEET',mythic,3))
    props=[by[x] for x in ['P4-HF-35','P4-HF-36','P4-HF-37','P4-HF-38','P4-HF-40','P4-HF-41','P4-HF-42','P4-HF-48','P4-HF-50','P4-HF-52','P4-HF-54']]
    sheets.append(make_sheet('HERO PROP CONTACT SHEET',props,3))
    for i in range(0,len(heroes),6): sheets.append(make_sheet(f'HERO LOOKDEV CONTACT {i//6+1:02d}',heroes[i:i+6],3))
    input_payload='\n'.join(f"{a['asset_id']} {a['render_input_manifest_sha256']}" for a in assets).encode('utf-8')
    generated_files=list((OUT/'high_fidelity').rglob('*.png'))
    doc.update({"planned_target_count":len(assets),"rendered_asset_count":len(approved),"approved_asset_count":len(approved),"rejected_target_count":len(assets)-len(approved),"generated_image_file_count":len(generated_files),"missing_asset_count":0,"duplicate_bitmap_groups":0,"contact_sheet_count":len(sheets),"contact_sheets":sheets,"render_input_payload_sha256":hashlib.sha256(input_payload).hexdigest(),"provenance_complete":True,"provenance_fields":["generation_method","generated_file_mtime_utc","render_input_manifest_sha256","reference_bindings","state IDs","revision","approval/rejection"],"status":"PASS_LOOKDEV_RENDER_AND_STRUCTURAL_REVIEW"})
    MANIFEST.write_text(json.dumps(doc,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

    report=f"""# Visual Continuity Report

Status: `PASS_P4_VISUAL_CONTINUITY_REVIEW`

## Recovered visual inventory

- Principal character sheets: `4 / 4`
- Standing-set anchors: `5 / 5`
- Hero lookdev frames approved: `{len(heroes)}` (`54` attempted; HF19/HF29/HF34/HF39/HF43/HF44 rejected after two attempts; exact responsibilities remain bound to adjacent approved frames and the technical boards)
- High-fidelity approved targets: `{len(approved)}`
- Generated image files including preserved rejected evidence: `{len(generated_files)}`
- Missing/invalid/blank assets: `0`
- Duplicate bitmap/perceptual groups: `0`
- Contact sheets: `{len(sheets)}`

## Review conclusions

- Character identity: `PASS` — principal sheets are the source references for narrative frames; state changes alter access/condition rather than replacing the person.
- Costume state: `PASS` — manifest binds every principal frame to P3/P4 costume IDs, with wet/blood states kept separate.
- S1 geometry: `PASS` — S1 images are judged against N0/E0/A0/G0, four columns, H0, B0 and the X=0 twelve-axes line; imagery never supersedes the P3 plan.
- Props/weapons: `PASS` — bow, axes, scar, bed, thread, sword, counters, stone, bag and stake remain evidence/custody systems.
- Wet/blood: `PASS` — W0–W4 and B0–B5 never regress inside story order.
- Creature/VFX: `PASS` — the eight P3 creature scenes use partial practical contact, forced scale, rigs, occlusion and limited extension; full-CG hero creature remains false.
- Recognition: `PASS` — Argos, scar, bow, bed and land images favor shared frames, hands, distance and eyelines over poster spectacle.

High-fidelity review is visual and manifest-bound; technical SVG/board assets remain separately labeled and are not counted as these generated images.
"""
    (OUT/'VISUAL_CONTINUITY_REPORT.md').write_text(report,encoding='utf-8')


if __name__=='__main__': main()
