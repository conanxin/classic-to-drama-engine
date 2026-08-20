# Call Sheet Logic

Status: `PASS_CALL_SHEET_GENERATION_LOGIC`

The call sheet is generated from one TARGET schedule day plus the referenced stripboard rows. It never replaces the stripboard, risk assessment, stunt plan or departmental continuity book.

## Required header

- Production, date, `day_id`, day-of-days, block, weather source/time, sunrise/sunset, nearest hospital, unit base, parking/transport, meal, estimated wrap and emergency contacts.
- Current S1 state or non-S1 set/redress state; incoming and outgoing continuity photograph IDs.
- Script minutes, planned shots, scene IDs, episodes and exact pages/minutes; no hidden “pickup” bucket.

## Cast and background calls

| Call | Computation | Hold / release rule |
|---|---|---|
| Principal | earliest HMU/wardrobe/rehearsal requirement among assigned scenes | release only after sound wilds, continuity photos and next-state check |
| Supporting/day player | exact scene and blocking call plus fitting if first use | no all-day hold without a scene/rehearsal reason |
| Stunt/body double | rehearsal, rig/weapon inspection and camera tech before performer call | medic/stunt coordinator clear at call and wrap |
| Extras | pool ID, foreground face IDs, wardrobe wave, holding capacity | foreground continuity list reconciled before release |
| Voice only | separate ADR/record session unless an on-set eyeline depends on live read | recorded file/slate checksum at wrap |

## Department call offsets

- Art/props: hero assets and incoming state verified before camera; bow, axes, arrow/weapon, scar, bed, tree map and boundary stone require joint property/script sign-off.
- Wardrobe/HMU: current and next state, wet/blood/prosthetic layer, duplicates and application/removal window.
- Camera/grip/electric: shot list, camera wall/wild wall, lens/movement, sun axis, clean/contact plates and protected performance take.
- Sound/music reference: cue IDs, material wild tracks and any unequal-hearing POV.
- SFX/stunt/animals/water/VFX: named supervisor, rehearsal window, exclusion zone, stop authority, plate list and safety meeting.

## Special flags

`STUNT`, `WEAPONS`, `PROJECTILE`, `WET`, `BOAT`, `ANIMAL`, `FIRE`, `SMOKE`, `BLOOD`, `PROSTHETIC`, `NIGHT`, `CROWD`, `VFX PLATES`, `SUN HARD`, `PERFORMANCE PROTECTED`. A flag cannot be removed because the scene appears short.

## Day flow

1. Department safety/continuity preflight.
2. Cast/ensemble calls by actual first need, not blanket call.
3. Orientation master or protected performance take before fragmentary coverage.
4. Clean/technical plates before wet, blood, breakaway, crowd or light state makes them irrecoverable.
5. Escalate state only after prior-state photographs and shot completion.
6. Meal/turnaround/weather decision at the posted threshold.
7. Wrap by asset, performer, set state and evidence—not merely “camera wrap.”

## Variance and incident logic

The 1st AD records omitted/reordered shots, overtime forecast, weather loss, safety stops, injuries/near misses and continuity deviations. A deferred shot receives exact scene/shot/state/department requirements and a scheduled pickup slot; it may not become an unowned note. Safety stop authority belongs to the responsible supervisor and medic, not to creative or schedule pressure.

Final result: `PASS_CALL_SHEET_DATA_SAFETY_CONTINUITY_AND_WRAP_LOGIC`.
