# P7C Reader Polish QA

status: `PASS_LOCAL_PRODUCTION_QA`
date: `2026-08-24`
baseline: `c6cc0fc1ad29068c21a326d19e62c68ac067722f`

## Scope and environments

- routes: `/graphic/`, `/episodes/01/graphic/`, `/episodes/19/graphic/`, `/episodes/27/graphic/`, `/graphic/test/`;
- modes: normal Graphic, Script, P7C Test Mode;
- viewports: desktop `1440×900`, mobile `390×844`;
- builds: Astro development render and final static production preview at the GitHub Pages base path;
- browser: Chrome through the Playwright CLI fallback. The Codex in-app browser was attempted first and was unavailable because an administrator-enforced browser security policy blocked the session.

## Issues found and repaired

| ID | severity | issue | repair | verification |
|---|---|---|---|---|
| P7C-QA-01 | S1 | participant-code pattern `[A-Z0-9-]` is invalid under the browser's Unicode `v` regular-expression semantics | generated alphanumeric-only anonymous codes and constrained the field to `[A-Z0-9]{4,32}` | form validity true; session starts; console errors 0 |
| P7C-QA-02 | S1 | component `display` declarations overrode native `[hidden]`, showing setup and active study panels together | explicit hidden-state rules for setup, active, reflection and export panels | only the correct state is visible before, during and after a session |
| P7C-QA-03 | S2 | task navigation and destination bridge emitted the same `route_open` event twice | task launch now emits `task_started`; destination emits `route_open` | new EP27 flow records distinct events |
| P7C-QA-04 | S2 | relationship, space and prop aids consumed a full mobile viewport before narrative | collapsed Level 2 relationship overview; compact WHERE/AT STAKE header; one on-demand re-orient panel | mobile height reduced 13.7–14.5% without removing story events |

No unresolved S0, S1 or S2 issue remains.

## Product checks

| check | result | evidence |
|---|---|---|
| progressive recognition hierarchy | PASS | Level 1 name/role; Level 2 scene context; Level 3 identity card |
| contextual character assist | PASS | focus/tap opens faction and current relationship; named summary remains keyboard accessible |
| re-orient control | PASS | five per prototype; exposes current cast, goal, relation, space and key prop on demand |
| scene orientation | PASS | WHERE and AT STAKE lead; secondary detail no longer shares equal default weight |
| exact-source dialogue | PASS | 35 quotes; P7A verifier recovered historical site bytes and current narrative artifacts remain unchanged |
| normal mode cleanliness | PASS | study bridge hidden and no test metrics in normal Graphic/Script routes |
| reading progress | PASS | native progress element and scene number update; EP27 end reports 100% |
| Continue Reading | PASS | local state stored EP27 scene 05 and restored the saved route/scroll position |
| P7B dead links | PASS | EP28 Graphic is described as unavailable; EP28 Script remains the valid continuation |

## Test harness checks

- informed notice explains captured events, local-only storage, no automatic upload, anonymous participation and the right to stop;
- A/B conditions are counterbalanced for EP01 and EP19; EP27 remains the shared high-load Graphic task;
- all nine source-bound objective questions can be completed;
- all five short scales and five optional open questions can be completed on mobile;
- session completion produces a JSON download;
- the browser QA export was relabelled `synthetic_fixture: true` before analysis;
- the offline analyzer excluded the synthetic export and reported `external_valid: 0` and `AWAIT_REAL_READER_EVIDENCE`;
- no database, tracker, network submission, name, email, IP or browser fingerprint is used.

## Mobile comparison

| route | baseline height | polished height | horizontal overflow | console errors |
|---|---:|---:|---:|---:|
| EP01 Graphic | 10,724 px | 9,260 px | 0 | 0 |
| EP19 Graphic | 10,610 px | 9,096 px | 0 | 0 |
| EP27 Graphic | 11,067 px | 9,459 px | 0 | 0 |
| Test Mode setup | n/a | 1,813 px | 0 | 0 |

## Accessibility and performance

- native `details/summary`, `progress`, labelled form controls and visible focus provide keyboard/touch operation without a hover-only dependency;
- character assist summaries expose the name and short role; the context layer opens by focus or tap;
- normal Graphic pages remain readable without the study bridge;
- the static production preview has no horizontal overflow at `390×844`;
- source layers remain collapsed; only the cover is eager; story visuals retain lazy/responsive delivery;
- Test Mode JavaScript is route-local and no server-side dependency was added.

## Build and integrity

- `npm run verify`: PASS;
- `npm run build`: PASS;
- static pages: `99`;
- Pagefind documents: `98`;
- P7A prototypes: `3`, scenes `15`, exact-source quotes `35`, rejected visual promotions `0`;
- publication: episodes `30`, scenes `150`, forbidden internal publication `0`;
- production-preview P7C routes: HTTP `200`, correct `text/html`;
- protected predecessor diffs: `0` for V2, P3, P4, P5 and Runtime.

## Evidence boundary

This QA verifies product behavior and study readiness. It does not verify that real readers remember more, understand more, finish faster or prefer Graphic Mode. Real participant count remains `0`.
