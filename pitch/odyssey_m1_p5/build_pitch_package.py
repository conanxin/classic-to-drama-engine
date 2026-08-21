#!/usr/bin/env python3
"""Build the P5 pitch package and original-temp-sound pitch teaser."""
from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/"pitch/odyssey_m1_p5"; SCRATCH=OUT/".render"; SCRATCH.mkdir(parents=True,exist_ok=True)
W,H=640,360
REJECTED={"P4-HF-19","P4-HF-29","P4-HF-34","P4-HF-39","P4-HF-43","P4-HF-44"}


def load(p): return json.loads((ROOT/p).read_text(encoding="utf-8"))
def dump(p,x): p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
def write(p,x): p.write_text(x.rstrip()+"\n",encoding="utf-8")
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def font(n,b=False):
 f=Path("/usr/share/fonts/opentype/noto")/("NotoSansCJK-Bold.ttc" if b else "NotoSansCJK-Regular.ttc")
 if not f.exists(): f=Path("/usr/share/fonts/truetype/dejavu")/("DejaVuSans-Bold.ttf" if b else "DejaVuSans.ttf")
 return ImageFont.truetype(str(f),n)
F18,F24,F38,F54=font(18),font(24,True),font(38,True),font(54,True)


def title_card(path,kicker,title,subtitle):
 img=Image.new("RGB",(W,H),(19,18,15)); d=ImageDraw.Draw(img)
 d.rectangle((38,38,W-38,H-38),outline=(136,112,72),width=2); d.line((90,230,550,230),fill=(136,112,72),width=1)
 d.text((W//2,80),kicker,font=F18,fill=(190,172,138),anchor="ma")
 d.text((W//2,135),title,font=F54,fill=(235,222,190),anchor="ma")
 d.text((W//2,247),subtitle,font=F18,fill=(192,198,194),anchor="ma")
 img.save(path,quality=92,optimize=True)


title=OUT/"P5_PITCH_TITLE_CARD.jpg"; end=OUT/"P5_PITCH_END_CARD.jpg"
title_card(title,"A 30 × 7 MINUTE MYTHIC RETURN DRAMA","归途：奥德修斯","THE HOMEWARD ROAD: ODYSSEUS · PITCH PREVIS")
title_card(end,"PRODUCTION-HANDOFF-READY DESKTOP PACKAGE","谁能认出归来的人？","NOT FINANCED · NOT CAST · NOT PERMITTED · NOT VENDOR-QUOTED")

look=load("visual-development/odyssey_m1_p4/LOOKDEV_RENDER_MANIFEST.json")["assets"]
by_id={x["asset_id"]:x for x in look}
for r in REJECTED: assert by_id[r]["status"]=="REJECTED"
selected=[
 ("TITLE",title,5.0,"Identity before spectacle","P5_ORIGINAL_GRAPHIC"),
 ("P4-HF-01",None,7.0,"An occupied home","P4_APPROVED_HIGH_FIDELITY"),
 ("P4-HF-02",None,6.0,"A missing father","P4_APPROVED_HIGH_FIDELITY"),
 ("P4-HF-09",None,6.0,"Story becomes a dangerous name","P4_APPROVED_HIGH_FIDELITY"),
 ("P4-HF-16",None,8.0,"The sea answers identity with consequence","P4_APPROVED_HIGH_FIDELITY"),
 ("P4-HF-32",None,7.0,"The returned man controls his face","P4_APPROVED_HIGH_FIDELITY"),
 ("P4-HF-37",None,7.0,"The scar proves private history","P4_APPROVED_HIGH_FIDELITY"),
 ("P4-HF-40",None,8.0,"The bow turns public claim into test","P4_APPROVED_HIGH_FIDELITY"),
 ("P4-HF-45",None,6.0,"Violence begins inside finite geography","P4_APPROVED_HIGH_FIDELITY"),
 ("P4-HF-46",None,6.0,"The armory reversal has a cost","P4_APPROVED_HIGH_FIDELITY"),
 ("P4-HF-48",None,7.0,"The bed asks what only two people know","P4_APPROVED_HIGH_FIDELITY"),
 ("P4-HF-50",None,7.0,"Father and land verify lineage","P4_APPROVED_HIGH_FIDELITY"),
 ("P4-HF-53",None,7.0,"The community lowers its weapons","P4_APPROVED_HIGH_FIDELITY"),
 ("END",end,3.0,"Real-world validation is the next gate","P5_ORIGINAL_GRAPHIC"),
]
events=[]; concat=[]; t=0.0
for asset,explicit,duration,purpose,source_class in selected:
 if explicit is not None: p=explicit; shot_id=None
 else:
  row=by_id[asset]; assert row["status"]=="APPROVED" and asset not in REJECTED
  shot_id=row["shot_id"]; p=ROOT/f"animatic/odyssey_m1_p5/cards/{shot_id}.jpg"
 concat += [f"file '{p.as_posix()}'\n",f"duration {duration:.3f}\n"]
 events.append({"event_id":f"PT-{len(events)+1:02d}","start":t,"end":t+duration,"duration":duration,
  "source_asset_id":asset,"source_shot_id":shot_id,"source_path":str(p.relative_to(ROOT)),"source_sha256":sha(p),
  "source_class":source_class,"dramatic_purpose":purpose,"rejected_p4_imagery":False,
  "audio":"P5 original locally synthesized temp sea/wood/pulse; no voice or commercial music"})
 t+=duration
concat.append(f"file '{end.as_posix()}'\n")
assert t==90.0
cf=SCRATCH/"pitch.concat"; cf.write_text("".join(concat),encoding="utf-8")
# Four local layers create a temp sea/wood/pulse vocabulary. No copyrighted recording is sampled.
audio=("anoisesrc=color=pink:amplitude=.022:duration=90:sample_rate=48000,highpass=f=45,lowpass=f=1350,volume=.55[a0];"
       "sine=frequency=56:duration=90:sample_rate=48000,volume=.010,tremolo=f=.12:d=.5[a1];"
       "sine=frequency=112:duration=90:sample_rate=48000,volume=.004,tremolo=f=.5:d=.75[a2];"
       "anoisesrc=color=brown:amplitude=.010:duration=90:sample_rate=48000,highpass=f=200,lowpass=f=2800[a3];"
       "[a0][a1][a2][a3]amix=inputs=4:normalize=0,afade=t=in:st=0:d=2,afade=t=out:st=87:d=3,alimiter=limit=.35[a]")
teaser=OUT/"PITCH_TEASER_PREVIS.mp4"
subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-f","concat","-safe","0","-i",str(cf),"-filter_complex",audio,
 "-map","0:v","-map","[a]","-t","90","-r","12","-c:v","libx264","-preset","veryfast","-crf","25","-pix_fmt","yuv420p",
 "-c:a","aac","-b:a","48k","-metadata","title=The Homeward Road: Odysseus — P5 pitch teaser previs","-movflags","+faststart",str(teaser)],check=True)
runtime=round(float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",str(teaser)],capture_output=True,text=True,check=True).stdout),3)
assert 75<=runtime<=105
dump(OUT/"PITCH_TEASER_TIMELINE.json",{"artifact_class":"P5_PITCH_TEASER_TIMELINE","runtime_seconds":runtime,"events":events,
 "identity_chain":["occupied home","missing father","story/name","sea consequence","disguise","scar","bow","finite violence","bed","land","weapons lowered"],
 "rejected_p4_imagery_used_as_approved":0,"commercial_music":False,"voice_track":False,"status":"PASS"})
dump(OUT/"PITCH_TEASER_EDL.json",{"artifact_class":"P5_PITCH_TEASER_EDL","frame_rate":12,"runtime_seconds":runtime,
 "events":[{"event_id":x["event_id"],"source_path":x["source_path"],"source_in":0,"record_in":x["start"],"record_out":x["end"],"source_class":x["source_class"]} for x in events],"status":"PASS"})
write(OUT/"PITCH_TEASER_RESULT.md",f"""# P5 Pitch Teaser Result

Status: **PASS_PITCH_TEASER_PREVIS**  
Runtime: {runtime:.3f}s  
File: `pitch/odyssey_m1_p5/PITCH_TEASER_PREVIS.mp4`

The cut follows occupied home → missing father → story/name → sea consequence → disguise → scar → bow → finite violence → bed → land → weapons lowered. It uses approved P4 high-fidelity frames carried through P5 timing cards plus original P5 graphics and locally synthesized temp sound. Rejected targets used as approved: 0. Commercial music, external footage and actor/synthetic voice: 0. This is a pitch previs, not a final trailer.
""")

write(OUT/"TITLE_AND_GRAPHIC_PACKAGE.md","""# Title and Graphic Package

## Lockups

- Chinese master title: **《归途：奥德修斯》**
- English working title: **The Homeward Road: Odysseus**
- Phase/use descriptor is never part of the public title; “pitch previs” appears only on internal review assets.

The lockup uses a narrow horizontal rule and warm olive/bronze-on-charcoal hierarchy. Episode cards use `第 XX 集 / EPXX` with title below; no recap prose. Location cards appear only when a geographic jump cannot be inferred from sea, threshold or production design. Credits hierarchy: title → principal authorship/production entity → director/producers → department heads → legal line. Subtitle-safe area is the inner 80% width and 80% height; no critical text sits in the lower 12%.

Typography direction: humanist CJK serif or restrained inscriptional CJK display paired with an open-licensed/readily licensed Latin oldstyle; verify glyph coverage, screen legibility and license in P6. No font file is distributed by P5 and no license is claimed.
""")

write(OUT/"PITCH_PACKAGE.md","""# 《归途：奥德修斯》— P5 Production Pitch Package

> **PREPRODUCTION PACKAGE — NOT FINANCED / CAST / PERMITTED / VENDOR-QUOTED**

## Logline

After ten years of war and ten years of impossible return, a king reaches an occupied home where survival depends not on declaring his name, but on controlling who may recognize him—and on accepting that his wife, son, father and community must each verify a different truth.

## Series promise and format

Thirty approximately seven-minute episodes deliver one continuous mythic return thriller. Each episode has a concrete want, irreversible turn and hook; the season alternates household politics, testimony, sea consequence, disguise and finite spatial violence. The gods are real and alter conditions, but human choices carry responsibility.

## Why this Odyssey

The familiar voyage becomes an identity-and-recognition engine: public story is not proof; face is not identity; objects remember custody; private knowledge can defeat spectacle. Penelope is the final human verifier, Telemachus grows into action and judgment, and Odysseus moves from exposed cleverness to controlled identity.

## Audience experience

Grounded Mediterranean material, close human stakes and compressed episodic hooks make an ancient epic binge-readable without turning every myth into a full-CG showcase. Wonder enters through condition, scale, sound, reaction and practical interaction.

## Architecture and principal arcs

Books 1–24 remain covered across 30 episodes. Telemachus speaks, travels, judges testimony, keeps secrets and stands beside his father. Penelope actively governs household politics before conducting scar/bow/bed tests. Odysseus learns that being believed requires surrendering control to other people's verification.

## Visual and production identity

Five standing sets and 12 redress units carry most production. S1 Ithaca Hall moves through six frozen states from occupied home to restored community. P4 supplies 57 approved high-fidelity targets, 48 approved hero frames, 711 technical boards, four principal identity sheets, five set anchors, 30 color keys and all eight creature scenes. P5 translates these into 75 build-index assets, 30 episode animatics, 12 critical VFX previs sequences and 17 desktop production tests.

## Production method

The 54-day TARGET schedule and ¥38,262,784 TARGET planning budget remain the authority. Creatures privilege partial practical contact, forced perspective, shadow, sound and limited extension; full-CG hero creature required: false. The 12-axis/bow line, EP26–28 44-beat battle and recognition objects are protected before spectacle.

## Temporal and technical proof

Thirty animatics represent 150/150 scenes and 831/831 shots in 211.32 minutes, with an episode range of 6:52–7:15. Twelve VFX/stunt extracts prove plate and eyeline relationships; exact 44-beat S1 battle timing proves finite geography. The 90-second P5 teaser demonstrates the identity chain without becoming a monster reel.

## Risk control

High-risk water, stunts, creature contact, blood/wet continuity, S1 state changes and VFX plates are isolated into explicit tests and reset plans. Desktop evidence finds no formal P3 budget or schedule variance. That does not substitute for real engineering, vendor quotes, performer tests, location surveys or insurance.

## Existing proof links

- `animatic/odyssey_m1_p5/FULL_SERIES_ANIMATIC_RESULT.md`
- `vfx-previs/odyssey_m1_p5/VFX_PREVIS_RESULT.md`
- `production-tests/odyssey_m1_p5/PRODUCTION_TEST_RESULT.md`
- `art-department/odyssey_m1_p5/ART_DEPARTMENT_HANDOFF_RESULT.md`
- `pitch/odyssey_m1_p5/PITCH_TEASER_PREVIS.mp4`

## Remaining real-world dependencies

Rights/legal confirmation, financing, producer and department-head commitments, principal/supporting casting, location/stage scouting, construction and VFX bids, physical camera/costume/HMU/stunt/water/creature tests, permits, insurance, welfare and safety systems, procurement and final greenlight all remain external P6 work.
""")

slides=[
 (1,"Title","Chinese lockup, English working title, one occupied-home image."),
 (2,"Logline","A returned king must be verified, not merely seen."),
 (3,"Why this story","Identity, veterans' return, household legitimacy and civic repair."),
 (4,"Series engine","30 × ~7 minutes; want → test → irreversible turn → hook."),
 (5,"World","Gods alter conditions; people own choices and consequences."),
 (6,"Odysseus","Exposed cleverness → controlled identity; physical and moral cost."),
 (7,"Penelope","Household strategist and final human verifier."),
 (8,"Telemachus","Speech → travel → testimony → secrecy → action → civic authority."),
 (9,"Recognition system","Name/story/scar/bow/axes/bed/father-land/community."),
 (10,"Visual world","Home/sea/memory/disguise/recognition/violence/return grammars."),
 (11,"Myth and creatures","Partial practical contact + forced scale + sound + limited extension."),
 (12,"Episode shape","Six 5-episode rhythm blocks; sample hook and runtime evidence."),
 (13,"Production approach","Five standing sets, 12 redresses, medium-cost grammar."),
 (14,"S1 Ithaca Hall","Frozen geometry, states A–F, 12 axes, armory and wild walls."),
 (15,"Action/VFX proof","12 previs sequences; 44 exact battle beats; Cyclops/Scylla decisions."),
 (16,"Schedule","Lean 42 / TARGET 54 / Safe 62; TARGET remains executable on desktop evidence."),
 (17,"Budget","Lean ¥23.44m / TARGET ¥38.26m / Premium ¥67.98m; assumption-based, not quotes."),
 (18,"Existing proof assets","V2 scripts, P3 package, P4 lookdev/boards, P5 30-episode animatics."),
 (19,"Teaser","90-second pitch previs; identity chain, no commercial music/footage."),
 (20,"Next step","P6 real casting, scouting, bids, tests, rights/insurance, financing/greenlight."),
]
lines=["# Pitch Deck Outline","","> PREPRODUCTION PACKAGE — NOT FINANCED / CAST / PERMITTED / VENDOR-QUOTED","","Twenty-slide source outline; design execution must preserve approved visual IDs and evidence labels.",""]
for n,tle,content in slides: lines += [f"## {n}. {tle}","",content,""]
write(OUT/"PITCH_DECK_OUTLINE.md","\n".join(lines))

readiness=[
 ("Script","READY","V2 frozen and source fidelity passed"),("Director","READY","P3 grammar plus P5 full timing proof"),
 ("DP","PLANNED","shot grammar and previs exist; real camera/lens tests pending"),("Art","READY","desktop build handoff complete; shop validation pending"),
 ("Costume","PLANNED","build/duplicate logic complete; fittings and bids pending"),("HMU","PLANNED","application specifications complete; human tests pending"),
 ("Props","PLANNED","build/custody plans complete; fabrication and physical safety tests pending"),("Stunts","PLANNED","44-beat spatial proof; rehearsal and coordinator sign-off pending"),
 ("VFX","READY","12 technical sequences and seams defined; vendor methodology/bid pending"),("SFX","PLANNED","practical boundaries defined; engineering pending"),
 ("Sound","PLANNED","motif and temp timing exist; recording/design team pending"),("Casting","NEEDS REAL-WORLD VALIDATION","no actors contacted, attached or tested"),
 ("Locations","NEEDS REAL-WORLD VALIDATION","no scout, stage hold, permit or owner consent"),("Schedule","PLANNED","54-day target reconciled; cast/location/vendor calendars pending"),
 ("Budget","PLANNED","P3 assumption model reconciled; no quotes or financing"),("Post","PLANNED","edit/VFX/color strategy exists; facilities and bids pending"),
 ("Legal/rights","NEEDS REAL-WORLD VALIDATION","rights, labor and jurisdiction review not performed"),("Insurance","NEEDS REAL-WORLD VALIDATION","no broker, carrier or policy contacted"),
 ("Real-world procurement","BLOCKED","intentionally outside P5; requires P6 authorization and greenlight"),
]
rl=["# Production Readiness Matrix","","> **PREPRODUCTION PACKAGE — NOT FINANCED / CAST / PERMITTED / VENDOR-QUOTED**","","| Department | State | Evidence / remaining dependency |","|---|---|---|"]
for a,b,c in readiness: rl.append(f"| {a} | {b} | {c} |")
rl += ["","Overall: **READY_FOR_P6_REAL_WORLD_VALIDATION**, not ready to commence physical production."]
write(OUT/"PRODUCTION_READINESS_MATRIX.md","\n".join(rl))

write(OUT/"P5_BUDGET_VARIANCE_REGISTER.md","""# P5 Budget Variance Register

Frozen planning authority: LEAN **¥23,440,968**; TARGET **¥38,262,784**; PREMIUM **¥67,977,248**. These are assumption-based planning ranges, not vendor quotes.

| Item | P3 assumption | P5 evidence | Likely impact | Within contingency? | Action |
|---|---|---|---|---|---|
| S1 replaceable skins | battle/reset allowance | six-state build handoff confirms zones | no authority change | expected | validate construction bid |
| Wet/blood duplicates | wardrobe/art continuity allowance | explicit duplicate matrix | no authority change identified | expected | validate department quantities |
| Cyclops method | medium practical/VFX grammar | CYC-B forced perspective recommended | protects rather than expands VFX exposure | expected | lens/rig/vendor test |
| Scylla | six readable grabs | practical contact + limited extensions | remains medium strategy | expected | stunt/VFX joint bid |
| Animatic/VFX post | planned previs/edit development | P5 desktop assets complete | sunk preproduction proof; no production budget addition asserted | n/a | archive source and re-estimate with vendors |

Formal P5 budget variances: **0**. Status: **PASS_P3_BUDGET_AUTHORITY_RETAINED**. Real quotes may create future variances; P5 does not conceal that dependency.
""")

write(OUT/"P5_SCHEDULE_VARIANCE_REGISTER.md","""# P5 Schedule Variance Register

Frozen authorities: LEAN 42 days; **TARGET 54 days**; SAFE 62 days.

P5 checks redress custody, S1 A–F order, wet progression, blood/damage panels, creature interaction/clean plates and EP26–28 rehearsal geography. No desktop finding adds a required shooting day or makes the 54-day TARGET impossible. Construction, reset labor, performer availability, stage/location access, marine weather and vendor methodology still need P6 validation.

Formal P5 schedule variances: **0**. Status: **PASS_TARGET_SCHEDULE_STILL_EXECUTABLE**.
""")

write(OUT/"P5_SCRIPT_TIMING_CHANGE_REQUESTS.md","""# P5 Script Timing Change Requests

Count: **0**.

All 30 episode timelines fall inside 6:30–7:30 and the intended 6:50–7:15 operating window without changing V2. No script change request is raised. Physical table read and actor pace may reveal later requests; none are asserted from silent desktop timing.
""")

write(OUT/"PITCH_PACKAGE_RESULT.md",f"""# Pitch Package Result

Status: **PASS_P5_PITCH_PACKAGE**

- Pitch package: complete
- Deck source outline: 20/20 slides
- Production readiness matrix: complete and honest about real-world gaps
- Budget authority: P3 TARGET ¥38,262,784 retained; formal P5 variances 0
- Schedule authority: P3 TARGET 54 days retained; formal P5 variances 0
- Pitch teaser: {runtime:.3f}s, PASS
- Rejected P4 visual used as approved: 0
- Commercial music / unauthorized footage / voice performance: 0
""")

assert SCRATCH.resolve()==(ROOT/"pitch/odyssey_m1_p5/.render").resolve()
for p in SCRATCH.iterdir(): p.unlink()
SCRATCH.rmdir()
print(json.dumps({"status":"PASS","teaser_runtime":runtime,"slides":len(slides),"budget_variances":0,"schedule_variances":0,"script_requests":0},ensure_ascii=False))
