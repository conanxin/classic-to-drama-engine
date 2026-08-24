# P7C Cognitive Load Audit

status: `BASELINE_AND_POLISHED_COMPARISON_COMPLETE`
scope: `EP01 / EP19 / EP27 Graphic Mode`
audit date: `2026-08-24`
evidence: fresh local production-equivalent render, desktop `1440×900`, mobile `390×844`, DOM counts, source-bound prototype JSON

## 1. Audit scope and user goal

The user goal is to enter a scene, identify the people, understand the current relationship and spatial stakes, then keep reading without repeatedly returning to an encyclopedia. This audit does not claim a clinical or scientific measure of cognitive load. It uses a fixed internal comparative heuristic to locate density spikes before and after P7C changes.

## 2. Internal heuristic

For one viewport section:

`CLS = 1.4C + 2.4N + 0.35L + 0.9R + 0.6W + 0.8P + 0.5I + 0.7D + 0.2K + 0.25E`

Where `C` is visible characters/groups, `N` new names, `L` UI labels, `R` relationship facts, `W` location/spatial facts, `P` prop facts, `I` images, `D` dialogue blocks, `K` controls, and `E` expandable regions. Persistent site navigation and the five-scene rail are excluded so scene-to-scene comparison remains stable.

Bands: `≤10 LOW`, `>10–16 MODERATE`, `>16–22 HIGH`, `>22 SPIKE`. The bands only rank this product against itself.

## 3. Fresh screen evidence

| evidence | viewport | observed state | finding |
|---|---|---|---|
| QA-E1 | 1440×900 | Graphic index first viewport | purpose and three-prototype scope are immediately legible |
| QA-E2 | 1440×900 | EP01-S01 | six cast chips plus three equal-weight aid blocks create a high first-scene burden |
| QA-E3 | 1440×900 | EP19-S01 | technical board orients space, but name chips do not explain current identity |
| QA-E4 | 1440×900 | EP27-S01 | board, four names, goal, relation, space and arrow state compete simultaneously |
| QA-E5 | 390×844 | EP27-S01 | no horizontal overflow; relation/space/prop become three long stacked blocks before story text |
| QA-E6 | 1440×900 | EP27 cast and relationship sections | five of eight identities appear at once; relationship map arrives as a separate memory task |

Screenshots are task-owned temporary QA evidence and are intentionally not published or committed.

## 4. Baseline section scores

| episode | section | visible cast | dialogue blocks | baseline score | band | main source of load |
|---|---|---:|---:|---:|---|---|
| EP01 | cover | 0 | 0 | 3.7 | LOW | mode and episode metadata |
| EP01 | cast rail initial desktop viewport | 5 | 0 | 22.3 | SPIKE | five new names before story action |
| EP01 | relationship map | 6 endpoints | 0 | 11.8 | MODERATE | three abstract relationships |
| EP01 | S01 | 6 | 2 | 17.5 | HIGH | six people/groups plus three aid blocks |
| EP01 | S02 | 3 | 2 | 13.9 | MODERATE | disguised divine identity |
| EP01 | S03 | 2 | 2 | 12.7 | MODERATE | space and prop explanation |
| EP01 | S04 | 7 | 2 | 18.7 | HIGH | household and suitor crowd reassembled |
| EP01 | S05 | 2 | 2 | 12.7 | MODERATE | low-load private decision |
| EP19 | cover | 0 | 0 | 3.7 | LOW | mode and episode metadata |
| EP19 | cast rail initial desktop viewport | 4 | 0 | 18.2 | HIGH | four names and two identity layers |
| EP19 | relationship map | 6 endpoints | 0 | 11.8 | MODERATE | reader knowledge versus scene knowledge |
| EP19 | S01 | 3 | 2 | 13.9 | MODERATE | father knows/son does not |
| EP19 | S02 | 2 | 2 | 12.7 | MODERATE | divine condition change |
| EP19 | S03 | 2 | 3 | 13.4 | MODERATE | evidence chain and identity claim |
| EP19 | S04 | 2 | 3 | 13.4 | MODERATE | verification becomes choice |
| EP19 | S05 | 4 | 2 | 15.1 | MODERATE | new alliance while Eumaeus remains outside knowledge |
| EP27 | cover | 0 | 0 | 3.7 | LOW | mode and episode metadata |
| EP27 | cast rail initial desktop viewport | 5 | 0 | 22.3 | SPIKE | five of eight names shown before action |
| EP27 | relationship map | 8 endpoints | 0 | 15.5 | MODERATE | four faction relationships |
| EP27 | S01 | 4 | 2 | 15.1 | MODERATE | exits, factions and arrow state |
| EP27 | S02 | 5 | 3 | 17.2 | HIGH | new named suitor plus right-wing handoff |
| EP27 | S03 | 5 | 3 | 17.2 | HIGH | armory route and weapon custody |
| EP27 | S04 | 6 | 2 | 17.5 | HIGH | betrayal trace and battle line |
| EP27 | S05 | 6 | 3 | 18.2 | HIGH | alternate route, enemy weapons and three arrows |

## 5. Mobile baseline

| episode | page height at 390×844 | horizontal overflow | interactive controls | observation |
|---|---:|---:|---:|---|
| EP01 | 10,724 px | 0 | 58 | eight-name onboarding is cumulative even though only two to three cards are visible at once |
| EP19 | 10,610 px | 0 | 47 | identity burden is lower, but current knowledge is separated from names |
| EP27 | 11,067 px | 0 | 63 | longest and densest prototype; aid blocks delay narrative entry |

## 6. Strengths

### P7C polished mobile comparison

The same routes were re-measured after progressive disclosure, compact scene orientation and collapsed relationship context were implemented. Content events and exact-source dialogue were not removed.

| episode | baseline height | polished height | reduction | overflow | default relationship detail | scene re-orient controls |
|---|---:|---:|---:|---:|---|---:|
| EP01 | 10,724 px | 9,260 px | 1,464 px / 13.7% | 0 | collapsed | 5 |
| EP19 | 10,610 px | 9,096 px | 1,514 px / 14.3% | 0 | collapsed | 5 |
| EP27 | 11,067 px | 9,459 px | 1,608 px / 14.5% | 0 | collapsed | 5 |

These are interface-density observations, not reader-outcome evidence. The retained story content means the reduction comes from hierarchy and spacing, not narrative deletion.

- all 15 source layers are collapsed by default;
- visual references are approved and labelled by authority;
- mobile has no horizontal overflow;
- each scene already has a stable image, conflict goal and exact-source dialogue;
- native `details` provides a sound no-JS disclosure base.

## 7. UX risks

1. The cast rail can introduce five new names in a single desktop viewport, above the introduction budget.
2. Scene cast chips answer “who” only by name. They do not answer “who is this now?” without a long return scroll.
3. Relationship, space and prop blocks share equal visual weight, so the reader must decide the hierarchy.
4. EP27 repeats large support blocks in every scene, creating scroll fatigue before narrative and dialogue.
5. The scene rail reports `01/05` but not overall reading progress or a resumable position.
6. The end hook links to a later prototype as “next graphic prototype,” which is accurate but can still be mistaken for the next story episode.

## 8. Accessibility risks

- cast chips are links back to the identity rail, not contextual disclosures; keyboard and touch users pay the same navigation cost;
- no low-interruption recovery control exists for a reader who loses track mid-scene;
- the sticky mobile row is compact, but the three support blocks that follow consume most of a viewport;
- screenshots cannot prove screen-reader announcement quality; that requires semantic and keyboard testing after implementation.

## 9. P7C recommendations

- enforce `GLANCE → CONTEXT → DETAIL`, with Level 3 closed by default;
- cap the initial desktop introduction viewport at four priority identities;
- make cast names contextual, keyboard/touch operable, and scene-bound;
- introduce one “现在有哪些人？” disclosure containing scene cast, factions, relation and stakes;
- replace three equal-weight aid blocks with one clear WHERE/WHO/AT STAKE hierarchy plus optional depth;
- add percentage/scene progress and local Continue Reading;
- make research capture conditional on Test Mode only.

## 10. Evidence limits

This audit identifies product risks; it does not prove that memory, comprehension, completion, or continuation intent improves. Those claims remain gated by exported results from real external participants.
