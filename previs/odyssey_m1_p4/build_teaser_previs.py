#!/usr/bin/env python3
"""Build timeline authorities and assemble the P4 teaser once lookdev images exist."""

from __future__ import annotations

import hashlib
import json
import math
import subprocess
import tempfile
import wave
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'previs/odyssey_m1_p4'
LOOK=ROOT/'visual-development/odyssey_m1_p4/high_fidelity/hero_frames'
FPS=24
W,H=1920,1080
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'

SEGMENTS=[
 ('CARD-Q',3.5,'QUESTION','FADE'),('P4-HF-01',3.5,'occupied home','PUSH'),('P4-HF-02',3.0,'son leaves','PAN_R'),
 ('P4-HF-05',4.0,'sea pressure','PUSH'),('P4-HF-08',3.0,'name disclosed','HOLD'),('P4-HF-09',3.0,'Cyclops fragment','PAN_L'),
 ('P4-HF-12',0.8,'stake consequence','PUSH'),('P4-HF-20',3.5,'mother cannot be held','PUSH'),('P4-HF-21',3.0,'bound to hear','PAN_R'),
 ('P4-HF-23',3.0,'first grab','PAN_L'),('P4-HF-27',3.0,'home as stranger','PUSH'),('P4-HF-28',3.0,'access changes','HOLD'),
 ('P4-HF-32',3.5,'Argos','PUSH'),('P4-HF-36',3.5,'scar','HOLD'),('P4-HF-37',2.8,'bow custody','PAN_R'),
 ('P4-HF-41',2.8,'bow note','PUSH'),('P4-HF-42',3.0,'twelve axes','HOLD'),('P4-HF-45',2.0,'armory reversal','PAN_L'),
 ('P4-HF-46',3.5,'battle geometry','PUSH'),('P4-HF-47',3.0,'aftermath','HOLD'),('P4-HF-48',5.0,'bed test','PUSH'),
 ('P4-HF-50',3.5,'father and land','PAN_R'),('P4-HF-53',3.2,'weapons lowering','HOLD'),('P4-HF-54',3.3,'return remains work','PUSH'),
 ('CARD-END',3.0,'title','FADE'),
]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def authorities() -> tuple[list[dict],dict]:
    look=json.load(open(ROOT/'visual-development/odyssey_m1_p4/LOOKDEV_RENDER_MANIFEST.json'))
    by_id={x['asset_id']:x for x in look['assets']}
    cursor=0.0; clips=[]
    for n,(asset,duration,purpose,motion) in enumerate(SEGMENTS,1):
        clip={"clip_id":f"PV-{n:03d}","asset_id":asset,"purpose":purpose,"start_seconds":round(cursor,3),"duration_seconds":duration,"end_seconds":round(cursor+duration,3),"start_frame":round(cursor*FPS),"end_frame_exclusive":round((cursor+duration)*FPS),"motion":motion,"transition":"HARD_CUT" if n not in {1,2,len(SEGMENTS)} else "FADE"}
        if asset.startswith('P4-HF'):
            src=by_id[asset]; clip.update({"source_path":src['output_path'],"scene_id":src['scene_id'],"shot_id":src['shot_id'],"frame_id":src.get('frame_id')})
        clips.append(clip); cursor+=duration
    shotlist={"artifact_class":"odyssey_p4_teaser_previs_shotlist","fps":FPS,"runtime_seconds":round(cursor,3),"clip_count":len(clips),"clips":clips,"status":"FROZEN_PENDING_ASSEMBLY"}
    timeline={"artifact_class":"odyssey_p4_teaser_previs_timeline","fps":FPS,"width":W,"height":H,"runtime_seconds":round(cursor,3),"total_frames":round(cursor*FPS),"video_codec":"H.264","audio":{"sample_rate":48000,"channels":1,"source":"original abstract synthesized P4 sound","copyrighted_music":False},"clips":clips,"status":"FROZEN_PENDING_ASSEMBLY"}
    return clips,{"shotlist":shotlist,"timeline":timeline}


def write_authorities() -> None:
    _,d=authorities()
    (OUT/'TEASER_PREVIS_SHOTLIST.json').write_text(json.dumps(d['shotlist'],ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (OUT/'TEASER_PREVIS_TIMELINE.json').write_text(json.dumps(d['timeline'],ensure_ascii=False,indent=2)+'\n',encoding='utf-8')


def title_card(kind: str) -> np.ndarray:
    im=Image.new('RGB',(W,H),(17,18,16)); d=ImageDraw.Draw(im)
    if kind=='QUESTION':
        d.text((W//2,H//2-65),'当无人认出他，他是谁？',font=ImageFont.truetype(FONT,58),anchor='mm',fill=(224,216,194))
        d.line((W//2-260,H//2+22,W//2+260,H//2+22),fill=(117,95,64),width=3)
    else:
        d.text((W//2,H//2-65),'《归途：奥德修斯》',font=ImageFont.truetype(FONT,72),anchor='mm',fill=(228,220,198))
        d.text((W//2,H//2+35),'视觉预演 / ODYSSEY P4',font=ImageFont.truetype(FONT,28),anchor='mm',fill=(146,137,115))
    return cv2.cvtColor(np.array(im),cv2.COLOR_RGB2BGR)


def fit_image(path: Path) -> np.ndarray:
    arr=cv2.imread(str(path),cv2.IMREAD_COLOR)
    if arr is None: raise RuntimeError(f'cannot read {path}')
    ih,iw=arr.shape[:2]; scale=max(W/iw,H/ih); nw,nh=math.ceil(iw*scale),math.ceil(ih*scale)
    arr=cv2.resize(arr,(nw,nh),interpolation=cv2.INTER_LANCZOS4)
    x=(nw-W)//2; y=(nh-H)//2
    return arr[y:y+H,x:x+W]


def motion_frame(base: np.ndarray, t: float, motion: str) -> np.ndarray:
    max_zoom=1.055 if motion=='PUSH' else 1.025
    z=1+(max_zoom-1)*t
    nw,nh=round(W*z),round(H*z); scaled=cv2.resize(base,(nw,nh),interpolation=cv2.INTER_CUBIC)
    if motion=='PAN_R': x=round((nw-W)*t)
    elif motion=='PAN_L': x=round((nw-W)*(1-t))
    else: x=(nw-W)//2
    y=(nh-H)//2
    return scaled[y:y+H,x:x+W]


def synth_audio(seconds: float,path: Path) -> None:
    sr=48000; n=round(seconds*sr); t=np.arange(n)/sr; rng=np.random.default_rng(20260821)
    noise=rng.normal(0,1,n); smooth=np.convolve(noise,np.ones(1200)/1200,mode='same')
    sea=.12*smooth/np.max(np.abs(smooth)); audio=sea
    # sparse original object cues: low wood, bow strain, axes ring, weapon earth.
    for at,freq,amp,decay in [(6.5,82,.13,1.1),(16.0,46,.20,.8),(21.3,57,.18,.6),(42.5,110,.08,1.5),(47.8,165,.10,1.4),(50.2,880,.16,2.2),(54.1,54,.23,.8),(72.8,96,.18,1.0)]:
        start=round(at*sr); length=min(n-start,round(3.2*sr)); tt=np.arange(length)/sr
        audio[start:start+length]+=amp*np.sin(2*np.pi*freq*tt)*np.exp(-tt/decay)
    # protect recognition silences.
    for a,b in [(38.0,40.5),(43.2,45.0),(61.0,64.0)]:
        audio[round(a*sr):round(b*sr)]*=.18
    pcm=np.int16(np.clip(audio,-.95,.95)*32767)
    with wave.open(str(path),'wb') as f: f.setnchannels(1); f.setsampwidth(2); f.setframerate(sr); f.writeframes(pcm.tobytes())


def assemble() -> None:
    clips,data=authorities(); missing=[c['source_path'] for c in clips if c['asset_id'].startswith('P4-HF') and not (ROOT/c['source_path']).is_file()]
    if missing: raise SystemExit('missing approved lookdev assets: '+', '.join(missing))
    silent=Path(tempfile.gettempdir())/'odyssey_p4_teaser_silent.mp4'; writer=cv2.VideoWriter(str(silent),cv2.VideoWriter_fourcc(*'mp4v'),FPS,(W,H))
    if not writer.isOpened(): raise RuntimeError('OpenCV VideoWriter unavailable')
    for clip in clips:
        count=clip['end_frame_exclusive']-clip['start_frame']
        base=title_card('QUESTION' if clip['asset_id']=='CARD-Q' else 'END') if clip['asset_id'].startswith('CARD') else fit_image(ROOT/clip['source_path'])
        for i in range(count): writer.write(motion_frame(base,i/max(1,count-1),clip['motion']))
    writer.release()
    wav=OUT/'TEASER_PREVIS_ORIGINAL_TEMP_SOUND.wav'; synth_audio(data['timeline']['runtime_seconds'],wav)
    final=OUT/'TEASER_PREVIS.mp4'
    try:
        subprocess.run(['ffmpeg','-y','-loglevel','error','-i',str(silent),'-i',str(wav),'-c:v','libx264','-preset','medium','-crf','20','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','-shortest','-movflags','+faststart',str(final)],check=True)
    finally:
        silent.unlink(missing_ok=True)
    probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(final)]))
    data['shotlist']['status']='PASS_ASSEMBLED'; data['shotlist']['output_path']=final.relative_to(ROOT).as_posix(); data['shotlist']['output_sha256']=sha(final)
    (OUT/'TEASER_PREVIS_SHOTLIST.json').write_text(json.dumps(data['shotlist'],ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    data['timeline']['status']='PASS_ASSEMBLED'; data['timeline']['output_path']=final.relative_to(ROOT).as_posix(); data['timeline']['output_sha256']=sha(final)
    (OUT/'TEASER_PREVIS_TIMELINE.json').write_text(json.dumps(data['timeline'],ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    result=f"""# Teaser Previs Result

Status: `PASS_TEASER_PREVIS_PRODUCED`

- Runtime: `{float(probe['format']['duration']):.3f} s`
- Clips: `{len(clips)}`
- Frame rate: `{FPS} fps`
- Canvas: `{W}×{H}`
- Video: `{final.relative_to(ROOT).as_posix()}`
- Video SHA-256: `{sha(final)}`
- Sound: original abstract synthesized P4 temp track; no commercial/copyrighted music
- Formal trailer claim: `false`

The edit proves the season's home/sea/disguise/recognition/violence/return grammar without summarizing the complete climax.
"""
    (OUT/'TEASER_PREVIS_RESULT.md').write_text(result,encoding='utf-8')


if __name__=='__main__':
    import sys
    write_authorities()
    if '--assemble' in sys.argv: assemble()
