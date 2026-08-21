#!/usr/bin/env python3
"""Build the P5 artifact closure and independently verify final acceptance."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
PITCH=ROOT/"pitch/odyssey_m1_p5"
MANIFEST=PITCH/"P5_ARTIFACT_MANIFEST.json"
VERIFY=PITCH/"P5_INDEPENDENT_VERIFICATION.json"
BASELINE="563839908cc62dca3f9132fae20c490e4b0a14b6"
P4SHA="626800b73ccaa8e996f7ff882c4745894720033fcf117337140f714689767bc3"
ROOTS=["art-department/odyssey_m1_p5","animatic/odyssey_m1_p5","vfx-previs/odyssey_m1_p5","production-tests/odyssey_m1_p5","pitch/odyssey_m1_p5"]
EXCLUDE={"pitch/odyssey_m1_p5/P5_ARTIFACT_MANIFEST.json","pitch/odyssey_m1_p5/P5_INDEPENDENT_VERIFICATION.json"}
FROZEN=["scripts/odyssey_m1_v2","editorial/odyssey_m1_v2","production/odyssey_m1_v2","preproduction/odyssey_m1_p3","visual-development/odyssey_m1_p4","storyboards/odyssey_m1_p4","design/odyssey_m1_p4","previs/odyssey_m1_p4","ODYSSEY_V2_FINAL_RESULT.md","ODYSSEY_P4_FINAL_RESULT.md","runtime_capability_prototype"]


def load(p): return json.loads((ROOT/p).read_text(encoding="utf-8"))
def sha(p):
 h=hashlib.sha256()
 with p.open("rb") as f:
  for b in iter(lambda:f.read(1024*1024),b""): h.update(b)
 return h.hexdigest()
def git(*args,check=True): return subprocess.run(["git",*args],cwd=ROOT,text=True,capture_output=True,check=check)
def artifact_class(p):
 s=p.suffix.lower(); rel=p.relative_to(ROOT).as_posix()
 if s==".mp4": return "TIMED_VIDEO_PREVIS"
 if s in {".jpg",".jpeg",".png"}: return "RASTER_TECHNICAL_OR_APPROVED_DERIVATIVE"
 if s==".svg": return "VECTOR_TECHNICAL"
 if s in {".wav",".m4a",".aac"}: return "ORIGINAL_TEMP_AUDIO"
 if "EDL" in p.name: return "EDIT_DECISION_LIST_JSON"
 if s==".json": return "MACHINE_MANIFEST_OR_TIMELINE"
 if s==".md": return "HUMAN_HANDOFF_DOCUMENT"
 if s==".py": return "DETERMINISTIC_BUILD_OR_VERIFICATION_TOOL"
 return "P5_SUPPORT_ARTIFACT"
def authority(rel):
 if rel.startswith("animatic/"): return "P3 frozen shots + P4 approved visual authorities + P5 neutral timing"
 if rel.startswith("vfx-previs/") or rel.startswith("production-tests/"): return "P3 frozen geography/shot/beat authority + P4 approved visuals"
 if rel.startswith("art-department/"): return "P3 frozen production authority + P4 approved design"
 return "P3/P4/P5 approved evidence chain"


def build_manifest():
 entries=[]
 for root in ROOTS:
  for p in sorted((ROOT/root).rglob("*")):
   if not p.is_file(): continue
   rel=p.relative_to(ROOT).as_posix()
   if rel in EXCLUDE or "/.render/" in rel: continue
   entries.append({"path":rel,"bytes":p.stat().st_size,"sha256":sha(p),"artifact_class":artifact_class(p),"source_authority":authority(rel)})
 payload_hash=hashlib.sha256(json.dumps(entries,ensure_ascii=False,separators=(",",":"),sort_keys=True).encode()).hexdigest()
 payload={"artifact_class":"P5_ARTIFACT_MANIFEST","schema_version":"1.0.0","baseline_commit":BASELINE,
          "p4_artifact_manifest_sha256":P4SHA,"artifact_count":len(entries),"entry_payload_sha256":payload_hash,"entries":entries,
          "exclusions":["manifest itself","independent verification output over this payload","root final result created after closure"],
          "status":"FROZEN_P5_ARTIFACT_PAYLOAD"}
 MANIFEST.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 print(json.dumps({"manifest":str(MANIFEST.relative_to(ROOT)),"entries":len(entries),"sha256":sha(MANIFEST)}))


def check(cond,name,checks,detail=""):
 checks.append({"check":name,"status":"PASS" if cond else "FAIL","detail":str(detail)})
 if not cond: raise AssertionError(f"{name}: {detail}")


def verify():
 checks=[]
 check(git("cat-file","-e",BASELINE+"^{commit}").returncode==0,"baseline_commit_exists",checks,BASELINE)
 check(sha(ROOT/"visual-development/odyssey_m1_p4/P4_ARTIFACT_MANIFEST.json")==P4SHA,"p4_manifest_identity",checks,P4SHA)
 for p in FROZEN:
  check(git("diff","--quiet",BASELINE,"--",p,check=False).returncode==0,f"frozen_unchanged:{p}",checks)

 # Scope: every baseline-to-working-tree change belongs to an allowed P5 root or root result.
 changed=set(git("diff","--name-only",BASELINE).stdout.splitlines())|set(git("diff","--name-only","--cached",BASELINE).stdout.splitlines())
 # Include committed post-baseline paths.
 changed |= set(git("diff","--name-only",BASELINE,"HEAD").stdout.splitlines())
 allowed=lambda p: p=="ODYSSEY_P5_FINAL_RESULT.md" or any(p.startswith(r+"/") for r in ROOTS)
 bad=sorted(p for p in changed if not allowed(p))
 check(not bad,"p5_write_scope",checks,bad)

 p3shots=load("preproduction/odyssey_m1_p3/SHOT_LIST_MASTER.json")["shots"]
 p3scenes=load("preproduction/odyssey_m1_p3/SCENE_MASTER_INDEX.json")["scenes"]
 anim=load("animatic/odyssey_m1_p5/ANIMATIC_MASTER_MANIFEST.json")
 check((len(p3shots),len(p3scenes))==(831,150),"p3_locked_counts",checks)
 check((anim["episodes"],anim["scenes"],anim["shots"])==(30,150,831),"animatic_counts",checks)
 timelines=[]
 for p in sorted((ROOT/"animatic/odyssey_m1_p5/episodes-json").glob("EP*_TIMELINE.json")): timelines+=json.loads(p.read_text(encoding="utf-8"))["shots"]
 tids=[x["shot_id"] for x in timelines]
 check(len(timelines)==831 and len(set(tids))==831,"timeline_unique_831",checks)
 check(set(tids)=={x["shot_id"] for x in p3shots},"timeline_exact_p3_shot_set",checks)
 check(len({x["scene_id"] for x in timelines})==150,"timeline_scene_coverage_150",checks)
 check(all(x.get("planned_duration",0)>0 and all(k in x for k in ["dialogue_duration","action_duration","hold","transition","sound_cue"]) for x in timelines),"timing_fields_831",checks)
 check(all((ROOT/x["visual_path"]).exists() and sha(ROOT/x["visual_path"])==x["visual_sha256"] for x in timelines),"visual_sha_bindings_831",checks)
 check(not any(x["p4_rejected_imagery_used_as_approved"] for x in timelines),"rejected_imagery_zero",checks)
 check(anim["audio_source_provenance"]=="831/831" and anim["unauthorized_commercial_music"]==0,"audio_provenance",checks)
 check(anim["runtime_range_seconds"][0]>=390 and anim["runtime_range_seconds"][1]<=450,"runtime_acceptance_window",checks,anim["runtime_range_seconds"])
 for e in anim["episode_animatics"]:
  p=ROOT/e["file"]
  probe=subprocess.run(["ffprobe","-v","error","-show_entries","stream=codec_type","-of","csv=p=0",str(p)],text=True,capture_output=True,check=True).stdout
  check("video" in probe and "audio" in probe,f"episode_av_streams:{e['episode']}",checks)

 art=load("art-department/odyssey_m1_p5/ART_ASSET_MASTER_INDEX.json")
 check((art["standing_set_count"],art["production_unit_redress_count"],art["frozen_hero_prop_system_count"])==(5,12,12),"art_locked_counts",checks)
 check(len({x["asset_id"] for x in art["assets"]})==art["asset_count"],"art_unique_asset_ids",checks)
 sets=load("art-department/odyssey_m1_p5/SET_BUILD_MATRIX.json")
 check([x["set_id"] for x in sets["sets"]]==["S1","S2","S3","S4","S5"],"standing_sets_5",checks)
 check(load("art-department/odyssey_m1_p5/COSTUME_BUILD_MATRIX.json")["status"]=="PASS_PRINCIPAL_4_OF_4","principal_costumes_4",checks)

 vfx=load("vfx-previs/odyssey_m1_p5/VFX_PREVIS_MASTER_MANIFEST.json")
 check(vfx["sequence_coverage"]=="12/12" and len(vfx["sequences"])==12,"vfx_previs_12",checks)
 for x in vfx["sequences"]: check((ROOT/x["file"]).exists() and sha(ROOT/x["file"])==x["sha256"],f"vfx_file:{x['sequence_id']}",checks)
 battle=load("production-tests/odyssey_m1_p5/EP26_28_SPATIAL_BATTLE_TEST/ACTION_BEAT_TIMELINE.json")
 p3beats=load("preproduction/odyssey_m1_p3/EP26_EP28_ACTION_PREVIS.json")["beats"]
 check([x["beat_id"] for x in battle["beats"]]==[x["id"] for x in p3beats],"battle_exact_44_beat_ids",checks)
 check(all(x=="PASS" for x in battle["continuity_checks"].values()),"battle_continuity",checks)
 tests=load("production-tests/odyssey_m1_p5/PRODUCTION_TEST_MASTER_MANIFEST.json")
 check(tests["test_count"]==17 and tests["passes"]==17,"production_tests_17",checks)

 teaser=ROOT/"pitch/odyssey_m1_p5/PITCH_TEASER_PREVIS.mp4"
 tr=float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",str(teaser)],text=True,capture_output=True,check=True).stdout)
 check(75<=tr<=105,"pitch_teaser_runtime",checks,tr)
 tt=load("pitch/odyssey_m1_p5/PITCH_TEASER_TIMELINE.json")
 check(tt["rejected_p4_imagery_used_as_approved"]==0 and not tt["commercial_music"] and not tt["voice_track"],"pitch_media_provenance",checks)
 check("Formal P5 budget variances: **0**" in (ROOT/"pitch/odyssey_m1_p5/P5_BUDGET_VARIANCE_REGISTER.md").read_text(),"budget_variances_zero",checks)
 check("Formal P5 schedule variances: **0**" in (ROOT/"pitch/odyssey_m1_p5/P5_SCHEDULE_VARIANCE_REGISTER.md").read_text(),"schedule_variances_zero",checks)
 check("Count: **0**" in (ROOT/"pitch/odyssey_m1_p5/P5_SCRIPT_TIMING_CHANGE_REQUESTS.md").read_text(),"script_requests_zero",checks)

 m=json.loads(MANIFEST.read_text(encoding="utf-8")); rebuilt=[]
 for e in m["entries"]:
  p=ROOT/e["path"]; check(p.exists() and p.stat().st_size==e["bytes"] and sha(p)==e["sha256"],f"artifact:{e['path']}",checks)
  rebuilt.append(e)
 ph=hashlib.sha256(json.dumps(rebuilt,ensure_ascii=False,separators=(",",":"),sort_keys=True).encode()).hexdigest()
 check(ph==m["entry_payload_sha256"],"artifact_payload_identity",checks)
 result={"artifact_class":"P5_INDEPENDENT_VERIFICATION","status":"PASS_ODYSSEY_P5_INDEPENDENT_VERIFICATION",
         "baseline_commit":BASELINE,"p4_artifact_manifest_sha256":P4SHA,"p5_artifact_manifest_sha256":sha(MANIFEST),
         "checks_total":len(checks),"checks_failed":0,"acceptance":{"episodes":30,"scenes":150,"shots":831,"animatics":"30/30","vfx_previs":"12/12","battle_beats":"44/44","production_tests":"17/17","pitch_teaser_seconds":round(tr,3)},
         "immutability":{"V2_modified":0,"P3_modified":0,"P4_modified":0,"runtime_modified":0},"checks":checks}
 VERIFY.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 print(json.dumps({k:result[k] for k in ["status","checks_total","checks_failed","p5_artifact_manifest_sha256"]}))


ap=argparse.ArgumentParser(); ap.add_argument("mode",choices=["build-manifest","verify"]); a=ap.parse_args()
build_manifest() if a.mode=="build-manifest" else verify()
