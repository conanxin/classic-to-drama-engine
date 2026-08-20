# Independent Production Review

Status: `PASS_FIVE_DISCIPLINE_INDEPENDENT_REVIEW`

Review baseline: complete P3 content through schedule/budget/risk commit `baee97dcee510be9cec725be0847ff8c7b3718cf`. Reviewers were simulated independently against the frozen V2 and then reconciled only after each discipline recorded findings.

## Director review

**Questions:** Is the season’s visual idea playable rather than decorative? Do recognition scenes retain performance continuity? Does divine spectacle steal a decision? Is action geography understandable?

**Evidence reviewed:** `DIRECTOR_VISION.md`, visual/camera/editing/performance grammars, 30-episode breakdown, motif chain, S1 floor plan, action previs, 831-shot list and 711 frame specifications.

**Findings and disposition:**

- Recognition chain is progressively photographed as public claim versus private proof: name/story, Argos, scar, bow/axes, bed, father/land, community. `PASS`.
- EP19, EP23 and EP29 use shared frames and controlled close work rather than alternating-singles efficiency coverage. `PASS`.
- Athena’s EP28 condition change occurs after humans close the breach; EP30 truce still requires weapons lowering and shared stone. `PASS`.
- S1 movement remains legible across clean, contest, first blood, battle, aftermath and restored states. `PASS`.
- Script change required: `no`; `SCRIPT_CHANGE_REQUESTS.md` remains count 0.

Director result: `PASS_NO_VISUAL_OR_PERFORMANCE_AMBIGUITY`.

## DP review

**Questions:** Are camera walls, screen direction, lens/movement classes, eye-lines, coverage and VFX plates physically recoverable? Are performance scenes overcut? Are creature scales measurable?

**Evidence reviewed:** S1 camera/wild walls, shot grammar, shot master, storyboard plan, VFX matrix, EP10/EP14/EP27–28 execution plans and target day records.

**Findings and disposition:**

- 150/150 scenes have shots; 831 shot IDs are unique; orphan count 0; coverage ratios remain inside class bands. `PASS`.
- Sixteen medium VFX scenes and eight creature scenes carry clean, contact/eyeline and technical plate requirements. Eleven practical-creature technical shots plus 160 LOW/MEDIUM shots produce 171 VFX-handled shots. `PASS`.
- Full-CG hero creature is never the emergency assumption; forced scale, partial practical, shadow, POV, reaction and sound carry contact. `PASS`.
- Multiple story labels inside a target day were audited: they are standing-set zones, controlled redresses or adjacent unit work, not hidden public-road company moves. `PASS`.
- EP19/23/29 close-ups are motivated by proof or failed access; no generic shot/reverse package is required. `PASS`.

DP result: `PASS_COVERAGE_PLATES_SCALE_AND_SCREEN_DIRECTION`.

## 1st AD review

**Questions:** Can the 54-day target run without impossible cast overlap, unowned scenes, unsafe resets or false animal requirements? Are night/wet/crowd/stunt demands called explicitly?

**Findings and repair:**

- Initial P3 animal extraction searched single Han characters across entire scene text. It falsely interpreted the `马` inside `忒勒马科斯` and animal-derived props such as bone/hide as live animals. Finding `P3-IR-001` was fixed in P3 only: `build_scene_master_index.py` now accepts the exact V2 `animals=` production field and distinguishes sheep from goat. Regenerated result: 17 genuine animal scenes; false S1 animal calls: 0. V2 modified: 0.
- An earlier 50-day target produced a 47-shot/12.25-minute day. Finding `P3-IR-002` was fixed by allocating protected cluster days to S1, court, shore/cave and Underworld. Final TARGET: 54 days, max 26 shots and 7.42 script minutes. `PASS`.
- LEAN remains an explicit risk boundary, not the master. SAFE supplies weather/technical separation. `PASS`.
- 150 scenes are assigned exactly once in every option; parallel main units 0; impossible cast overlaps 0. `PASS`.
- Call-sheet flags and stop authority cover wet, boats, animals, fire/smoke, weapons/projectiles, blood, prosthetics, crowds, night and VFX plates. `PASS`.

1st AD result: `PASS_ASSIGNMENT_CAST_RESET_AND_SAFETY_LOGIC`.

## Line producer review

**Questions:** Is the plan priced from quantities? Does the block order reduce moves and resets? Are cost tiers and cuts honest? Are risks owned?

**Evidence reviewed:** stripboard, three schedules, call-sheet logic, budget model, budget/production risk registers, casting/ensemble matrices and continuity books.

**Findings and disposition:**

- LEAN/TARGET/SAFE contain 42/54/62 days and the same 150 scenes/831 shots. TARGET is operationally recommended. `PASS`.
- TARGET carries zero true company-move days after twelve-block grouping; no duplicate savings claim is made. `PASS`.
- ¥23.44M/¥38.26M/¥67.98M are quantity×unit assumptions, marked NOT VENDOR QUOTE and backed by contingency. `PASS`.
- Sensitivity tests protect recognition, bow/axes, S1 battle geography/safety, EP29 and EP30 before spectacle/crowd/extensions. `PASS`.
- Budget concern: extras use peak pool-person calls per schedule day rather than the sum of scene declarations; this is a deliberate planning assumption and requires pool-by-pool bids before greenlight. It is recorded in the budget risk register, not hidden as precision. `PASS WITH BID REPLACEMENT NOTE`, nonblocking for P3.

Line producer result: `PASS_QUANTITY_MODEL_BLOCK_EFFICIENCY_AND_RISK_OWNERSHIP`.

## Stunt / VFX supervisor review

**Questions:** Are action beats unique and safe? Do weapons, blood, bodies, arrows and doors progress without contradiction? Are contact/clean plates sufficient? Are practical creature fallbacks real?

**Findings and disposition:**

- 44 unique EP26–28 beats carry start/end state, initiator, target, weapon, blocking, camera, stunt, VFX/SFX, safety and consequence. `PASS`.
- Earlier scene classification undercalled four safe-execution scenes (EP09-S05, EP10-S01, EP26-S05, EP27-S01). Finding `P3-IR-003` had already been fixed by promoting them to stunt-supervised preparation. Final stunt scenes: 30. `PASS`.
- Arrow ledger 12→recovered test→11→0, A0/G0 armory route, table/body/blood progression and Telemachus wound are all state-bound. `PASS`.
- Cyclops eye/stake, sheep escape, Scylla six rigs and hall weapons use physical contact references and fail-soft edit paths. No live projectile/blade or full-CG rescue assumption. `PASS`.
- Seven dedicated TARGET rehearsal days are retained. `PASS`.

Stunt/VFX result: `PASS_ACTION_STATE_PLATES_FALLBACK_AND_SAFETY`.

## Combined closeout

| Gate | Result |
|---|---|
| visual ambiguity | PASS |
| coverage insufficiency | PASS — 0 under-covered |
| overcoverage | PASS — 0 over-covered |
| cast overlap | PASS — 0 impossible |
| schedule impossibility | PASS — TARGET 54-day cap verified |
| continuity conflict | PASS after P3-IR-001 regeneration |
| reset risk | PASS with S1 and wet progression locks |
| budget spike | PASS with owned register and contingency |
| unsafe blocking | PASS with supervisor veto and rehearsals |
| VFX plate omission | PASS for 16 medium + 8 creature scenes |

Open blockers: `0`. Script change requests: `0`. V2 modifications: `0`. Runtime modifications: `0`.

Final result: `PASS_INDEPENDENT_PRODUCTION_REVIEW`.
