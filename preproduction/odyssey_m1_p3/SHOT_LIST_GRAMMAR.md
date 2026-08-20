# Odyssey P3 Shot-List Grammar — Frozen

Status: `FROZEN_SHOT_LIST_GRAMMAR`

This grammar is frozen after the S1 plan, EP26–28 previs, and 150-scene index. It governs `SHOT_LIST_MASTER.json` and storyboard-frame planning. It is an editorial plan, not a mandate to collect generic safety coverage.

## Identity and inheritance

- Shot ID: `EPxx-Sxx-SHxxx`, zero-padded and unique across the season.
- A shot inherits `episode`, `scene_id`, `production_unit`, set state, cast/prop continuity, VFX/SFX/stunt flags, and source scene SHA from `SCENE_MASTER_INDEX.json`.
- `SH001` is not automatically a master. It is the first causal image required by the scene.
- No shot may exist without a valid scene; every scene must have at least one shot.

## Required shot fields

Every shot records:

`episode, scene_id, shot_id, dramatic_purpose, shot_size, camera_position, lens_class, camera_movement, subject, blocking, dialogue_coverage, insert, sound_priority, vfx, sfx, stunt, continuity, estimated_seconds, production_unit`.

The master file also records per-scene `coverage_flag`, `coverage_ratio`, planned shot count, storyboard priority, and causal-purpose coverage.

## Dramatic-purpose vocabulary

| Purpose | Question answered | Use |
|---|---|---|
| GEOGRAPHY | Where are exits, power positions, threat and safe space? | Required when spatial control changes; not required as a decorative establishing shot. |
| WANT | What concrete thing is the scene’s driver trying to obtain? | Prefer a task/object/action over an explanatory face. |
| OBSTRUCTION | Who or what prevents the want? | Shared frame preferred when power is relational. |
| TACTIC | What does a character try next? | Movement or object custody may cover dialogue. |
| REVERSAL | What changes strategy or understanding? | Motivated close-up or re-block, never automatic push-in. |
| EVIDENCE | What can another character or the viewer independently verify? | Scar, garment, key, count, route, sound, wound, door, line or witness. |
| CONSEQUENCE | What cannot be reset within the scene? | Hold long enough to register physical/social cost. |
| TRANSITION | Which state carries into the next scene? | Used only when custody, injury, route, weather or knowledge crosses the cut. |
| HOOK | What new pressure survives the cut? | Image/action, not a duplicated summary card. |

A standard scene normally needs four to six of these purposes, often combined in a moving master or shared frame. A purpose does not justify a separate shot by itself.

## Shot-size vocabulary

- `EWS`: scale/location rule with human consequence.
- `WS`: full blocking and exits.
- `FS`: full body, weapon, task or threshold.
- `MS2` / `MS3`: relationship two-/three-shot preserving hands and eyelines.
- `MS`: single with task context.
- `MCU`: pressure/reversal with some physical context.
- `CU`: evidence, withheld answer or irreversible choice.
- `ECU`: rare material proof—string seat, scar texture, lock gap, bark mark.
- `INSERT`: object custody/count/state change only.
- `POV`: restricted to perception that materially misleads, recognizes or threatens.

No scene receives a master/medium/close/reverse/insert package by default.

## Lens classes

| Class | Range assumption | Function |
|---|---|---|
| ULTRAWIDE_18_24 | 18–24 mm | Controlled scale, forced perspective, deck/cave geometry; never casual facial distortion. |
| WIDE_25_32 | 25–32 mm | Blocking-led moving masters and relationship to thresholds. |
| NORMAL_35_50 | 35–50 mm | Default shared performance and human spatial truth. |
| PORTRAIT_65_85 | 65–85 mm | Withheld answers, evidence response, compressed return corridors. |
| LONG_100_135 | 100–135 mm | Dangerous distance, sea/route pressure, public scrutiny; eyeline checked. |
| MACRO_PROBE | macro/probe | Hero evidence and miniature/practical VFX plates only. |

Camera body/sensor choice remains a DP decision; the class freezes narrative behavior, not a vendor package.

## Camera movement rules

- `STATIC`: authority, testing, restraint, or a trap already closed.
- `PAN_TILT`: follows a custody or eyeline change without manufacturing urgency.
- `DOLLY_TRACK`: follows a tactic through real geography; end mark must reveal consequence.
- `LATERAL_TRACK`: compares parallel routes, especially household/service/action lanes.
- `PUSH_PULL`: reserved for irreversible recognition or spatial loss; no generic dialogue push-ins.
- `HANDHELD_CONTROLLED`: only when negotiated control is physically lost—wreck, creature grab, hall counterattack. It stops once a plan returns.
- `CRANE_TOP`: geography, casualty/prop ledger or divine condition; never a victory ornament.
- `RIGGED_POV`: water, creature or weapon plate requiring safety separation.

## Camera-position grammar

- Standing sets use fixed position IDs. S1 positions derive from the frozen coordinate plan: `S1-SOUTH-AXIS`, `S1-WW-W`, `S1-WW-E`, `S1-NW-DAIS`, `S1-P1`, `S1-P2`, `S1-OVERHEAD`, `S1-C0`, `S1-A0`.
- Other units use `UNIT-ZONE-DIRECTION`, e.g. `S3-FOREDECK-AFT`, `S5-CAVE-MOUTH-IN`, `U09-TRENCH-EAST`, `U10-ORCHARD-ROW3`.
- Camera positions that cross a weapon, water, animal, fire, height or crowd path are prohibited unless the special plan defines the isolation plate.

## Coverage ratio

`coverage_ratio = total planned usable coverage seconds ÷ estimated finished scene seconds`.

Planned usable seconds include overlapping moving-master, shared-performance, insert, stunt and VFX-plate durations. They do not include repeated takes, slates, rehearsals or clean plates. The ratio measures editorial options, not raw footage volume.

| Coverage class | Typical ratio | Typical shots | Rule |
|---|---:|---:|---|
| PERFORMANCE-CRITICAL | 1.25–1.55 | 3–5 | Preserve long shared takes, eyeline tension and actor continuity. EP19, EP23 and EP29 default here. |
| STANDARD | 1.30–1.75 | 4–6 | One blocking-led spine plus motivated evidence/consequence alternatives. |
| ACTION-CRITICAL | 1.75–2.40 | 6–10 | Geography, initiator, contact/isolated plate, consequence and continuity reset. |
| VFX-CRITICAL | 1.60–2.25 | 5–9 | Practical base, clean plate, interaction, eyeline/reaction and comp element. |
| PERFORMANCE+ACTION/VFX | 1.55–2.05 | 5–8 | Performance spine remains dominant; technical plates isolate risk. |

Flag rules:

- `UNDER-COVERED`: ratio below class minimum, no usable geography after a spatial change, missing consequence, missing VFX/stunt plate, or only isolated close-ups for a performance scene.
- `OVER-COVERED`: ratio above class maximum without a safety/VFX reason, more than six shots for a standard dialogue scene, duplicate singles covering the same lines, or an insert with no state change.
- `ACTION-CRITICAL`: scene index `fight=true`, `stunt=true`, or action previs reference.
- `PERFORMANCE-CRITICAL`: all EP19, EP23 and EP29 scenes; additional private recognition/judgment scenes may be promoted.
- `VFX-CRITICAL`: scene index `vfx=MEDIUM`; LOW VFX may be marked when a clean plate is still essential.

The builder must return `coverage_status=PASS` only when no scene remains OVER-COVERED or UNDER-COVERED after explicit exceptions.

## Performance protection

### EP19 father/son recognition

- Maintain father and son in shared frame through disbelief and failed proof.
- Transformation plates are separate from the performance take.
- A close-up may be motivated by refused touch or a specific remembered fact, not every speech.

### EP23 scar recognition

- Basin, hand, scar and Eurycleia’s stopped breath exist in one causal visual chain.
- Avoid alternating face coverage that makes the scar a surprise insert disconnected from touch.
- Preserve the dangerous shared silence and the reason speech cannot continue.

### EP29 marriage recognition

- Penelope and Odysseus share frame while the false bed instruction is issued.
- The first separated close-up occurs only when immovable construction knowledge becomes undeniable.
- Bed-root inserts are evidence plates, not sentimental montage.

## Dialogue and sound coverage

`dialogue_coverage` values:

- `FULL_MOVING_MASTER`
- `FULL_SHARED_STATIC`
- `SHARED_BEAT`
- `CHARACTER_TACTIC`
- `OVERLAP_INTERRUPTION`
- `REACTION_WITHHELD`
- `NONE_ACTION`
- `NONE_INSERT`

`sound_priority` identifies the sound that must survive the edit: dialogue, room/crowd behavior, sea-before-image, loom, wood, animal, weapon, bow string, axes ring, breath, silence-with-object, god-pressure, music or transition motif.

## Insert test

An insert is permitted only if it proves at least one of:

1. custody changes;
2. count changes;
3. damage/injury changes;
4. a lock/route changes;
5. recognition evidence becomes available;
6. a sound source changes strategy;
7. continuity state required by a later scene is established.

Decorative food, landscape, costume or weapon inserts fail the test.

## Stunt, SFX and VFX plates

- Stunt contact is never faked by putting an actor inside a live projectile/weapon path.
- Every action-critical event gets cause, isolated contact/plate as needed, consequence and reset evidence—not redundant angles on the same hit.
- Medium VFX scenes require practical interaction, clean plate, tracking/reference when applicable, subject eyeline/reaction and final-composite intent.
- Creature shots privilege partial practical, forced perspective, shadow, POV, sound, reaction, occlusion and limited comp. Full-CG hero creature remains false.
- SFX shots name the practical element and safe reset: wind/rain/spray, blood, smoke/fire, breakaway, debris, motion base, prosthetic or water interaction.

## Storyboard relationship

- MUST-storyboard shots receive frame IDs in `STORYBOARD_PLAN.json` with at least one planned frame; action/VFX transitions may require start/contact/end frames.
- SHOULD-storyboard scenes receive representative frames only for nonobvious composition, blocking or transition.
- NO-storyboard scenes remain governed by this shot grammar and director diagrams; no placeholder frames are created to inflate coverage.

## Acceptance

- Unique, deterministic shot IDs — required.
- 150/150 scene coverage — required.
- Orphan shots / duplicate IDs — zero.
- Over-/under-covered unresolved scenes — zero.
- EP19/23/29 performance protection — required.
- Fight, medium+ VFX and creature coverage — 100%.

Final status: `FROZEN_SHOT_LIST_GRAMMAR`.
