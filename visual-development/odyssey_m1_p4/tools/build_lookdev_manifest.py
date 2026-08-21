#!/usr/bin/env python3
"""Freeze high-fidelity P4 image-generation requests before native rendering."""

from __future__ import annotations

import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
P3=ROOT/'preproduction/odyssey_m1_p3'
OUT=ROOT/'visual-development/odyssey_m1_p4'

STYLE=(
    "historical-scene; grounded mythic Mediterranean, lived-in salted worked woven smoked weathered handled repaired; "
    "timber, lime plaster, stone, worn bronze, rope, wool, linen, leather, olive wood, clay, ash, salt and water; "
    "cinematic production concept art with believable practical set and costume construction; human-scale stakes; no readable text"
)
NEG=(
    "no celebrity or real-person likeness, no white-marble fantasy, no generic fantasy armor, no blue-orange blockbuster grade, "
    "no continuous magical glow, no clean full-CG monster beauty shot, no modern objects, no logos, no captions, no watermark, "
    "no poster pose, no excessive gore, no impossible extra doors or axes, no duplicated limbs"
)

CHAR_SHEETS=[
    ("P4-CHAR-ODY-IDENTITY-V02","Odysseus","fictional Mediterranean man in his late forties; broad back, rope-work forearms, dark curls broken by salt-grey left temple, asymmetric brow; exactly one healed old boar scar on the right outer thigh just above the knee and no other scars; neutral model sheet showing sea-worn, controlled beggar and returned states without changing identity","3:2","ODY-A..J","W-OD state family"),
    ("P4-CHAR-PEN-IDENTITY-V01","Penelope","fictional Mediterranean woman in her early forties; work-trained hands, high asymmetric brow, controlled dark coils, key and cloth weight on left side; neutral model sheet showing household administrator, strategist, verifier and restored-not-reset states","3:2","PEN-A..G","W-PE state family"),
    ("P4-CHAR-TEL-IDENTITY-V01","Telemachus","fictional Mediterranean young man about nineteen; long neck, left-foot lead, inherited clothing initially wrong at shoulder; neutral model sheet showing boy, traveler, returning heir, battle and civic states through fit and custody rather than armor","3:2","TEL-A..H","W-TE state family"),
    ("P4-CHAR-ATH-IDENTITY-V01","Athena","fictional cast-neutral woman with disciplined stillness; small physical owl pin, one forward shoulder and exact half-turn; neutral model sheet showing credible human disguises, almost-recognized condition and restrained structural divine state without glow","3:2","ATH human/almost/divine","W-AT state family"),
]

SET_SHEETS=[
    ("P4-SET-S1-ANCHOR-V01","S1 Ithaca hall","same 16 by 22 meter worked limestone and lime-plaster hall; north-center N0 double entrance, east E0 side door, southwest family stair and armory, four columns, east-offset hearth, center bow mark and exact twelve-axes line; occupied but structurally intact","16:9","S1-A","L-I-DAY"),
    ("P4-SET-S2-ANCHOR-V01","S2 ceremonial court","reusable cedar, plaster and cloth ceremonial court; lateral hospitality and scrutiny axis; camera-facing portal and work/throne relationship; Phaeacian sea-glass redress while preserving practical construction","16:9","PHAEACIA","L-PHAE"),
    ("P4-SET-S3-ANCHOR-V01","S3 dry ship deck","4.8 by 14 meter practical hero deck, mast socket, oar line, tarred rope grid, removable safe rails; sun direction and danger side readable; weathered and repairable, not pristine","16:9","FLEET","L-SHIP-D"),
    ("P4-SET-S4-ANCHOR-V01","S4 Eumaeus farm","low stone pen, worked hearth, gate, olive edge, humble hut wall and repair table; animal heat and honest labor create foreground; father-son proof axis kept playable","16:9","WORK","L-I-DAY"),
    ("P4-SET-S5-ANCHOR-V01","S5 shore/cave adaptable","reversible practical rock and shore environment with controlled cave mouth, black backing, water-tray edge, partial vegetation and fire position; suited to Ogygia and Cyclops redress without changing core geometry","16:9","CYCLOPS","L-CAVE"),
]

# asset_id, label, scene_id, shot ordinal in scene (1-based or -1), characters/state summary,
# costume summary, set state, props, lighting, composition/action
HERO=[
 (1,"Occupied Ithaca hall","EP01-S01",1,"TEL-A; PEN-A; Antinous","W-TE-01; W-PE-01; suitor wine/rust","S1-A","stolen chipped cup, split wine seal, work tables","L-I-DAY","wide moving-master feeling: Telemachus held at frame edge while Antinous occupies the off-axis seat; Penelope crosses a work route"),
 (2,"Telemachus night departure","EP02-S05",-1,"TEL-B; ATH-MENTOR","W-TE-01 with travel layer; W-AT-MENTOR","Ithaca harbor","rope, oil lamp, sword, loaded sacks","L-SHIP-N","low harbor threshold: young man steps onto a practical boat while home lamps stay behind; Athena controls crew rhythm, not a glowing reveal"),
 (3,"Calypso shore refusal","EP05-S02",1,"ODY-A/B; Calypso","W-OD-05-CALYPSO-WORN","S5 OGYGIA","old model boat, bronze axe, gold cup set aside","L-SHORE","shared shore frame; Odysseus faces worked timber and mortal sea, Calypso remains near but cannot complete his choice"),
 (4,"Raft built by hand","EP05-S03",3,"ODY-B; Calypso","W-OD-05-RAFT-SALT","S5 OGYGIA","bronze axe, hand drill, wedges, rope, partial raft","L-SHORE","hands and body weight on rough timber; practical construction and rope tension dominate, no picturesque island glamour"),
 (5,"Poseidon storm pressure","EP05-S04",4,"ODY-B; Poseidon condition only","W-OD-05-RAFT-SALT W2","U11 raft","partial raft, torn sail, rope, spray","L-POS","actor grip and lost horizon before spectacle; compact practical raft nearly disappears behind spray, no visible god body"),
 (6,"Nausicaa encounter","EP06-S02",2,"ODY-B/C; Nausicaa","shipwrecked wet / working laundry state","S5 river mouth","wet cloth, laundry line, olive branch, ball","L-SHORE","respectful distance across a laundry line; shipwrecked Odysseus covers himself with branch, Nausicaa holds public space without rescue pose"),
 (7,"Phaeacian court scrutiny","EP07-S02",2,"ODY-C; Arete; Alcinous","W-OD-06-PHAEACIA-BORROWED","S2 PHAEACIA","hearth, blue repair thread, low stool, family cup","L-PHAE","lateral shared court frame: Odysseus low at hearth, Arete's eyes on exact blue stitch, architecture luminous but supervised"),
 (8,"Storyteller says his name","EP08-S05",-1,"ODY-D; Arete; Alcinous; singer","W-OD-06-PHAEACIA-BORROWED","S2 PHAEACIA","ship registry board, carving knife, small horse figure","L-PHAE","close shared table geometry; blank registry becomes named through human testimony, face not treated as proof"),
 (9,"Cyclops threshold seizure","EP09-S05",4,"ODY-D memory; Polyphemus fragments; crew","W-OD-09-15-STORY","S5 CYCLOPS","giant rock door, tree staff, fire, wine","L-CAVE","low human eyeline with giant hand and shoulder fragment crossing cave mouth; object displacement proves scale, no clean full body"),
 (10,"Cyclops scale and waiting choice","EP10-S01",4,"ODY-D memory; Polyphemus fragments; crew","W-OD-09-15-STORY","S5 CYCLOPS","bronze sword held, giant rock and sheep pen","L-CAVE","wide practical cave geography: Odysseus restrains a sword because rock-door consequence is visible; giant foot/hand only"),
 (11,"Olive stake preparation","EP10-S02",3,"ODY-D memory; crew; Cyclops eye withheld","W-OD-09-15-STORY soot","S5 CYCLOPS","raw/sharpened olive stake, fire, strong wine, scaled bowl","L-CAVE","collective crew work around one long stake; heat, sharpened grain and smoke carry threat; eye remains offscreen"),
 (12,"Cyclops eye contact effect","EP10-S03",4,"ODY-D memory; Polyphemus eye unit; crew hands","W-OD-09-15-STORY soot/blood","S5 CYCLOPS","retracting heated stake, practical partial eye, smoke and controlled blood","L-CAVE","tight diagonal of six hands driving retracting stake toward a practical partial eye; impact implied through heat, smoke and reaction, no gore spectacle"),
 (13,"Ram-underbelly escape","EP10-S04",3,"ODY-D memory; Cyclops hand; crew","W-OD-09-15-STORY","S5 CYCLOPS THRESHOLD","oversized wool belly, floor hand, rope","L-CAVE","floor-level view under oversized ram wool; bound human bodies pass a searching giant hand; cave-mouth light defines exit"),
 (14,"Name boast and thrown rock","EP10-S05",4,"ODY-D exposed cleverness; Polyphemus silhouette; crew","W-OD-09-15-STORY","S3 fleet / Cyclops shore","ship rail, rope, breakaway rock splash","L-SHIP-D","compressed shore axis from boat: Odysseus stands too visible while crew pulls him down and partial giant silhouette launches rock"),
 (15,"Ithaca visible, wind bag closed","EP11-S03",3,"ODY-D; Eurylochus; crew","W-OD-09-15-STORY","S3 FLEET","tarred wind bag with nine knots, steering oar, distant Ithaca lamps","L-SHIP-N","hope compressed in distant home lights; exhausted Odysseus guards deformed bag while crew studies knots"),
 (16,"Laestrygonian fleet destruction","EP11-S05",4,"ODY-D; Eurylochus; crew; distant attackers","W-OD-09-15-STORY W1","U11 harbor","partial decks, scaled rock impacts, breaking hull, mooring stones","L-POS","one readable survivor boat escapes a harbor lane as practical hull fragments and rocks close exits; scale extension stays background"),
 (17,"Circe transformation","EP12-S01",3,"Circe; Eurylochus; crew transformation states","Circe poison-green; sailors practical","U08/S2 CIRCE","medicine cup, loom, animal collar, pen key","L-I-NIGHT","reflection and partial hand/face prosthetic phases around one clay cup; practical animals separate; no full morph showcase"),
 (18,"Circe terms change","EP12-S03",4,"ODY-D; Circe","W-OD-09-15-STORY / Circe controlled court","S2 CIRCE","medicine cup, bronze sword, curtain, wand lowered","L-I-NIGHT","two-shot across cup and sword; Circe's power has failed and stillness renegotiates access, not romantic glamour"),
 (19,"Underworld blood boundary","EP13-S01",3,"ODY-D; Eurylochus; Elpenor dead","W-OD-09-15-STORY","U09 UNDERWORLD","practical blood trench, black sheep, grave oar, wine bowl","L-UW","black reflective floor and gauze depth; Odysseus controls warm blood access while the first dead remains beyond it"),
 (20,"Mother cannot be held","EP13-S03",3,"ODY-D; Anticleia","W-OD-09-15-STORY / muted dead state","U09 UNDERWORLD","blood trench, shuttle shadow, Ithaca soil","L-UW","three-pass embrace feeling in one restrained frame: his arms close through empty depth while her face remains relational, not ghost spectacle"),
 (21,"Sirens at the mast","EP14-S03",3,"ODY-D; Eurylochus; crew; Sirens distant","W-OD-09-15-STORY","S3 FLEET","mast rope, beeswax, distant old armor/cloth silhouettes","L-SHIP-D","bound Odysseus strains toward barely resolved shore figures while waxed crew row; rope and remembered voices lead image"),
 (22,"Six counters before strait","EP14-S04",2,"ODY-D; Eurylochus; crew","W-OD-09-15-STORY","U11 strait entry","six bone counters at named oar stations, helm, spear","L-POS","over-shoulder strategic deck geography; six pale counters in foreground, six people unknowingly fixed in danger lanes"),
 (23,"Scylla first grab","EP14-S05",4,"ODY-D; Eurylochus; crew; Scylla fragment","W-OD-09-15-STORY W1","U11 strait","overhead rig, partial neck/limb silhouette, oar station tags","L-POS","readable deck axis and first independent overhead grab; fragment intersects rig line and actor eyelines, no monster-wide reveal"),
 (24,"Six empty stations","EP14-S05",-1,"ODY-D; survivors; Scylla absent condition","W-OD-09-15-STORY W2","U11 strait aftermath","six empty oar stations, scattered bone counters, blood cloth","L-POS","consequence frame: six named gaps and altered balance, Odysseus cannot cover the frame edges; creature absent"),
 (25,"Last ship wreck","EP15-S04",4,"ODY-D; Eurylochus; last crew","W-OD-09-15-STORY W3","U11 storm deck","breakaway mast, keel fragment, rope, cattle tag","L-STORM","finite practical wreck: mast breaks across readable deck, crew choices remain visible, sky effect secondary"),
 (26,"Story ends before Phaeacians","EP15-S05",-1,"ODY-D; Arete; Alcinous; singer","W-OD-06-PHAEACIA-BORROWED","S2 PHAEACIA","named registry board, six empty cups, extinguished lamp","L-PHAE","still court after violent memory: six empty cups and changed listeners frame Odysseus, no heroic absolution"),
 (27,"Return to Ithaca as stranger","EP16-S03",3,"ODY-C/D","W-OD-16-LANDFALL","S5 ITHACA SHORE","gift chests, registry board, blanket, stones","L-SHORE","sleep-worn man wakes among inventoried gifts on an unrecognized shore; land texture denies immediate triumph"),
 (28,"Athena makes beggar access","EP16-S05",4,"ODY-E; ATH-SHEPHERD/ALMOST","W-OD-17-26-BEGGAR; W-AT-SHEPHERD","U08 Ithaca road","gift cave door, patched cloak, staff, dust","L-ATH","same body identity inside altered social silhouette; cloth and wrong-timed shadow change access while Athena remains nearly ordinary"),
 (29,"Eumaeus gate test","EP17-S01",2,"ODY-E; Eumaeus","W-OD-17-26-BEGGAR / repaired farm cloak","S4 WORK","pig gate, throwing stone stopped, staff","L-I-DAY","gate divides guest law from suspicion; Eumaeus' body blocks animals and stranger yet offers a route"),
 (30,"Telemachus returns to farm","EP18-S05",-1,"TEL-E; Eumaeus; ODY-E","W-TE-18-RETURNING-HEIR; W-OD-17-26-BEGGAR","S4 GUEST","travel bag, bread, gate, thick cloak","L-I-DAY","returning son enters working foreground while disguised father remains socially small in same frame"),
 (31,"Father and son proof","EP19-S03",3,"ODY unmasked; TEL-F","W-OD-16/identity base; W-TE-18","S4 RECOGNITION","broken stool, black ship nail, short knife","L-REC","continuous two-shot with refused touch and exact black nail between them; belief carries cost, no divine reunion tableau"),
 (32,"Argos recognizes","EP20-S03",3,"ODY-E; Eumaeus; old Argos","W-OD-17-26-BEGGAR","S1 threshold","worn dog collar, dung/threshold, staff","L-I-DAY","low shared threshold frame: old dog sees him while humans look elsewhere; collar and tiny distance carry recognition"),
 (33,"Beggar inside occupied hall","EP20-S04",2,"ODY-E; TEL-F; Antinous; suitors","W-OD-17-26-BEGGAR; W-TE-18","S1-A","begging bag, bread, stool, stolen cup","L-I-DAY","long foreground occlusion gives beggar restricted path through his own hall; Telemachus cannot publicly acknowledge him"),
 (34,"Penelope converts pressure to debt","EP21-S04",3,"PEN-B/C; TEL-F; suitors","W-PE-01; W-TE-18","S1-A","gift ledger, necklace, earrings, broken loom wood","L-I-DAY","Penelope moves gifts into an accountable ledger line; suitors remain publicly framed as debtors, not romantic options"),
 (35,"Father and son empty weapon wall","EP22-S01",3,"ODY-E; TEL-F; Eurycleia","W-OD-17-26-BEGGAR; W-TE-18","S1-A late","emptying W0 hooks, spears, shields, keys","L-I-NIGHT","moving task frame with visible W0 hooks and A0 route; every carried weapon changes later battle possibility"),
 (36,"Scar recognition","EP23-S01",3,"ODY-F; Eurycleia; Penelope held distant","W-OD-17-26-BEGGAR scar access; W-PE-01","S1-A night","bronze basin, oil, fixed scar, wet cloth","L-REC","hand-to-scar-to-basin causal chain in one shared frame; stopped work and eye line, no isolated epic close-up"),
 (37,"Penelope opens bow box","EP23-S04",3,"PEN-C/D; Eurycleia","W-PE-01","S1 private room","bow-box key, Odysseus bow, oilcloth, axes model","L-I-NIGHT","administrator hands unlock a custody object; bow is partly revealed as worked wood, not weapon glamour"),
 (38,"Bow enters the hall","EP23-S05",3,"PEN-D; Eurycleia; ODY-E; TEL-F","W-PE-25-CONTEST; W-OD-BEGGAR; W-TE-18","S1-A to B","hero bow, box, twelve axe pieces, scar cloth","L-I-NIGHT","Penelope descends S0 route controlling bow custody; father and son cannot share recognition in public"),
 (39,"Twelve axes contest line","EP25-S01",1,"PEN-D; TEL-F; suitors","W-PE-25; W-TE-18","S1-B","bow, exact AX01-12 at X=0, calibration line, key","L-I-DAY","protected long south-axis composition: all twelve numbered axe throats visible, Penelope controls procedure off axis"),
 (40,"Telemachus almost strings bow","EP25-S02",3,"TEL-F; PEN-D; ODY-E; Antinous","W-TE-18; W-PE-25; W-OD-BEGGAR","S1-B","bow, foot mark, exact axe line","L-REC","young man tests strength then obeys secret timing; father remains in shared background, no sudden hero pose"),
 (41,"Odysseus strings the bow","EP26-S02",3,"ODY-G; TEL-F; suitors","W-OD-17-26-BEGGAR; W-TE-18","S1-B","hero bow, string wax, eleven-plus-test arrow custody","L-REC","quiet hand-and-ear relation to bow; hall listens before face changes, still in beggar access state"),
 (42,"Arrow through twelve axes","EP26-S03",4,"ODY-G; TEL-F; loyalists; suitors","W-OD-BEGGAR; W-TE-18","S1-B","test arrow, exact twelve axes, N1 backstop","L-I-DAY","clean X=0 trajectory through twelve distinct axe throats; side witnesses and protected backstop remain visible"),
 (43,"First kill and first blood","EP26-S05",3,"ODY-G/H; Antinous; TEL-G; suitors","W-OD-BATTLE base B1; W-TE-26","S1-C","bow, cup, table, eleven-arrow ledger","L-HALL-B","cause and consequence across N2 table seam: arrow/cup/body change state; no gore insert; exits remain readable"),
 (44,"Finite arrow control","EP27-S01",2,"ODY-H; Eurymachus; TEL-G; suitors","W-OD-27-BATTLE B2; W-TE-26","S1-D early","bow, eleven-to-nine arrows, empty W0, long tables","L-HALL-B","north-readable hall with arrows controlling three lanes; every shot changes visible inventory and distance"),
 (45,"Armory reversal","EP27-S03",3,"ODY-H; TEL-G; loyalists; armed suitors","battle B3","S1-D","A0 one finger open, shields, helmets, spears, remaining arrows","L-HALL-B","A0 route and unexpected enemy weapons enter same geography; Telemachus recognizes his custody error"),
 (46,"Full hall battle under shield shadow","EP28-S03",3,"ODY-H; TEL-G; Eumaeus; Philoetius; ATH-ALMOST","battle B4","S1-D","spears, shields, three arrows, Athena shield shadow","L-HALL-B","four-column geography and table wall remain legible as one wrong-timed shield shadow buys a beat, humans still act"),
 (47,"Sulfur aftermath","EP28-S05",3,"ODY-H; TEL-G; Eurycleia; loyalists","battle aftermath B5","S1-E","sulfur basin, water, washed cup, ledgers, damaged grout","L-HALL-B","bodies removed through defined routes; smoke and residue reveal consequence, no pristine victory hall"),
 (48,"Bed test","EP29-S04",3,"ODY-I; PEN-E; Eurycleia","W-OD-29; W-PE-29","S1-F bedroom","living olive bed, root/post joint, maker marks, threshold","L-BED","Penelope issues false move order in shared frame; Odysseus reacts to impossible construction, bed remains work evidence not romantic reveal"),
 (49,"Recognized partners","EP29-S05",2,"ODY-I; PEN-F","W-OD-29; W-PE-29","S1-F bedroom","olive bed, old purple thread, cleaned cup, old string","L-BED","two exhausted adults share frame after verification; distance closes without glamour reset, repaired room and old pressure remain"),
 (50,"Laertes recognizes land testimony","EP30-S02",3,"ODY-J; Laertes; TEL-H","W-OD-30; W-TE-30; orchard work state","U10 orchard","numbered trees, hoe, fixed scar, old cloak","L-FIELD","father names worked trees before touching son; numbered bark and soil occupy foreground, recognition is land knowledge"),
 (51,"Three generations arm","EP30-S03",3,"ODY-J; Laertes; TEL-H; loyalists","field/civic states","U10 orchard house","three distinct spears, old helmet, arm cloth, pruning knife","L-FIELD","three weapon patinas and three stances show lineage without triumph; each can still choose to lower"),
 (52,"Boundary stone shared","EP30-S04",4,"ODY-J; Laertes; TEL-H; kin leaders; ATH-MENTOR","field/civic states","U10 field","two-sided boundary stone, shields, spears","L-FIELD","opposed groups hold the same worked stone from both sides; Athena alters crowd rhythm but does not place it"),
 (53,"Weapons lowering","EP30-S05",3,"ODY-J; TEL-H; Laertes; civic kin","field/civic states","U10 field","three spears and group weapons lowering, shared stone","L-FIELD","wide frame expands to both kin groups as weapons touch earth at different moments; no coronation pose"),
 (54,"Purple thread and self-cut staff","EP30-S05",-1,"PEN-G intercut; TEL-H; ODY-J","W-PE-30; W-TE-30; W-OD-30","S1-F/U10 intercut concept","old purple joined to undyed thread, Telemachus cutting his own staff","L-FIELD","paired physical closure without montage gloss: working hands join old and new thread while young heir cuts his own civic staff; return remains work"),
]


def main() -> None:
    shots=json.loads((P3/'SHOT_LIST_MASTER.json').read_text(encoding='utf-8'))['shots']
    shot_by_scene={}
    for shot in shots: shot_by_scene.setdefault(shot['scene_id'],[]).append(shot)
    frame_plan=json.loads((P3/'STORYBOARD_PLAN.json').read_text(encoding='utf-8'))['frames']
    frames_by_shot={}
    for f in frame_plan: frames_by_shot.setdefault(f['shot_id'],[]).append(f['frame_id'])
    scene_index={x['scene_id']:x for x in json.loads((P3/'SCENE_MASTER_INDEX.json').read_text(encoding='utf-8'))['scenes']}
    rows=[]
    for aid,char,request,ratio,state,costume in CHAR_SHEETS:
        prompt=f"Use case: historical-scene\nAsset type: P4 principal character identity sheet\nPrimary request: {request}\nStyle/medium: {STYLE}\nComposition/framing: one clean production design sheet, full-body front, three-quarter and state variation, coherent single fictional identity, plain worked-linen backdrop\nLighting/mood: neutral 5600K material truth\nConstraints: cast-neutral fictional person; state IDs {state}; costume family {costume}; no readable labels\nAvoid: {NEG}"
        row={"asset_id":aid,"asset_type":"PRINCIPAL_CHARACTER_SHEET","character":char,"character_state_ids":state,"costume_ids":costume,"aspect_ratio":ratio,"prompt":prompt,"negative_constraints":NEG,"generation_method":"Codex integrated ImageGen","seed":None,"source_reference_ids":[],"output_path":f"visual-development/odyssey_m1_p4/high_fidelity/characters/{aid}.png","status":"PLANNED","review_result":"PENDING"}
        if char=="Odysseus":
            row.update({"revision":2,"rejected_attempts":[{"asset_id":"P4-CHAR-ODY-IDENTITY-V01","path":"visual-development/odyssey_m1_p4/high_fidelity/characters/P4-CHAR-ODY-IDENTITY-V01.png","reason":"multiple random body scars weakened the single fixed EP23 boar-scar continuity","status":"REJECTED_VISUAL_CONTINUITY"}]})
        rows.append(row)
    for aid,name,request,ratio,state,lighting in SET_SHEETS:
        prompt=f"Use case: historical-scene\nAsset type: P4 standing-set visual anchor\nPrimary request: {request}\nStyle/medium: {STYLE}\nComposition/framing: one clean wide production-design view at human eye height, practical buildable architecture, camera access legible\nLighting/mood: {lighting}\nConstraints: set {name}; exact state {state}; no people as hero subject; no invented routes\nAvoid: {NEG}"
        refs=["preproduction/odyssey_m1_p3/S1_ITHACA_HALL_FLOOR_PLAN.json"] if aid.startswith('P4-SET-S1') else []
        rows.append({"asset_id":aid,"asset_type":"STANDING_SET_ANCHOR","set_id":name.split()[0],"set_state":state,"lighting_id":lighting,"aspect_ratio":ratio,"prompt":prompt,"negative_constraints":NEG,"generation_method":"Codex integrated ImageGen","seed":None,"source_reference_ids":refs,"output_path":f"visual-development/odyssey_m1_p4/high_fidelity/sets/{aid}.png","status":"PLANNED","review_result":"PENDING"})
    for number,label,scene_id,ordinal,states,costumes,set_state,props,lighting,composition in HERO:
        scene_shots=shot_by_scene[scene_id]; shot=scene_shots[ordinal-1] if ordinal>0 else scene_shots[-1]
        frame_ids=frames_by_shot.get(shot['shot_id'],[])
        aid=f"P4-HF-{number:02d}"
        prompt=f"Use case: historical-scene\nAsset type: Odyssey P4 hero lookdev keyframe\nPrimary request: {label}. {composition}\nScene/backdrop: {scene_index[scene_id]['story_location']}; production state {set_state}\nSubject: {states}\nStyle/medium: {STYLE}\nComposition/framing: cinematic 16:9 frame bound to {shot['shot_id']}; {shot['shot_size']} / {shot['camera_position']} / {shot['lens_class']}; preserve practical geography and human eyelines\nLighting/mood: {lighting}\nMaterials/textures: {props}\nConstraints: costume states {costumes}; continuity {shot['continuity']}; one coherent frame; character identity must match provided principal sheet references when present\nAvoid: {NEG}"
        refs=[]
        for key,rid in [('ODY','P4-CHAR-ODY-IDENTITY-V02'),('PEN','P4-CHAR-PEN-IDENTITY-V01'),('TEL','P4-CHAR-TEL-IDENTITY-V01'),('ATH','P4-CHAR-ATH-IDENTITY-V01')]:
            if key in states: refs.append(rid)
        set_ref=None
        if 'S1' in set_state: set_ref='P4-SET-S1-ANCHOR-V01'
        elif 'S2' in set_state: set_ref='P4-SET-S2-ANCHOR-V01'
        elif 'S3' in set_state: set_ref='P4-SET-S3-ANCHOR-V01'
        elif 'S4' in set_state: set_ref='P4-SET-S4-ANCHOR-V01'
        elif 'S5' in set_state: set_ref='P4-SET-S5-ANCHOR-V01'
        if set_ref: refs.append(set_ref)
        rows.append({"asset_id":aid,"asset_type":"HERO_LOOKDEV_FRAME","label":label,"frame_id":frame_ids[0] if frame_ids else None,"shot_id":shot['shot_id'],"scene_id":scene_id,"episode":scene_id[:4],"character_state_ids":states,"costume_ids":costumes,"set_state":set_state,"prop_ids":props,"lighting_id":lighting,"composition":composition,"aspect_ratio":"16:9","prompt":prompt,"negative_constraints":NEG,"generation_method":"Codex integrated ImageGen","seed":None,"source_reference_ids":refs,"output_path":f"visual-development/odyssey_m1_p4/high_fidelity/hero_frames/{aid}.png","status":"PLANNED","review_result":"PENDING"})
    payload={
        "artifact_class":"odyssey_p4_lookdev_render_manifest","schema_version":"1.0.0","baseline_commit":"0c4a403864d9ea89afabceed3c7be7d5819f86c8",
        "look_bible_path":"visual-development/odyssey_m1_p4/LOOK_BIBLE.md","asset_count":len(rows),"principal_sheet_count":4,"standing_set_anchor_count":5,"hero_frame_count":len(HERO),
        "generator_route":"Codex integrated ImageGen; built-in route; no API key","real_person_likeness":False,"assets":rows,"status":"FROZEN_PENDING_RENDER"
    }
    (OUT/'LOOKDEV_RENDER_MANIFEST.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')


if __name__=='__main__': main()
