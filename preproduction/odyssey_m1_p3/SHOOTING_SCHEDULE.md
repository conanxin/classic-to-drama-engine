# Shooting Schedule Options

Status: `PASS_LEAN_TARGET_SAFE_SCHEDULES`

The three JSON schedules are the day-level authorities. Every day contains block, production unit, locations, scene IDs, episodes, cast, extras, script minutes, planned shots, stunt/VFX/wet/blood flags, special props, company-move decision, sun dependency and risk notes.

## Recommendation

| Option | Days | Scenes | Shots | Avg shots/day | Max shots/day | Max script min/day | Use |
|---|---:|---:|---:|---:|---:|---:|---|
| LEAN | 42 | 150 | 831 | 19.79 | 48 | 14.17 | compression boundary; higher reset, overtime and performance risk |
| **TARGET** | **54** | **150** | **831** | **15.39** | **26** | **7.42** | **master recommendation** |
| SAFE | 62 | 150 | 831 | 13.40 | 26 | 7.42 | weather, health, technical and performance buffer |

All options: 0 unassigned scenes, 0 duplicate scene assignments, 0 parallel main units, 0 impossible cast overlaps. TARGET is recommended because it removes the LEAN plan’s 48-shot/14.17-minute peak without inflating every low-complexity block.

## TARGET block calendar

| Order | Block | Days | Production purpose | Continuity lock |
|---:|---|---:|---|---|
| 1 | S1 clean palace | 8 | EP01, EP20–24, EP29 clean/restored coverage | photograph S1-A/S1-F and all recognition object positions before damage |
| 2 | S1 contest/pre-battle | 3 | EP25–26 | axes fixed, bow/arrow/door custody, first-blood boundary |
| 3 | S1 battle progression | 6 | EP27–28 | shoot B0→B6; blood, bodies, furniture and weapon state only move forward |
| 4 | S4 farm | 3 | EP17–19 | animal lanes, cloak/portion evidence, father-son performance |
| 5 | S2 court redress | 6 | Pylos, Sparta, Phaeacia, island courts | redress photograph/strike checklist; no same-day public company move |
| 6 | S5 shore/cave + U12 | 6 | Ogygia, Scheria, voyage shores, Cyclops | dry before wet; creature scale and cave states isolated |
| 7 | S3 dry deck | 5 | all dry ship/deck work | ship inventory and crew depletion by vessel/story block |
| 8 | U11 wet/motion | 4 | raft, strait, wreck and heavy wet | wet severity increases inside each sequence; warming/turnaround protected |
| 9 | U09 Underworld | 3 | EP13 then EP30 dead | blood-trench/dead states separate; EP30 revision gets its own state |
| 10 | U06/U07 civic-harbor | 4 | assemblies, games, civic/harbor edges | ensemble/wardrobe pools and daylight axes |
| 11 | U08 roads/forest | 3 | forest, travel road, Ithaca road | group by light direction and story region |
| 12 | U10 finale | 3 | orchard, field, civic closure | tree map, three spears, boundary stone and final light |

Total: `54 days`.

## Critical continuity

- **Performance:** EP19 father-son shared-frame work, EP23 scar chain and EP29 marriage verification retain planned rehearsal and long-take time. No schedule saving converts them to fragmented singles.
- **Wet:** 17 target days carry some water; only five are heavy/storm work. Dry dialogue, inserts and clean plates precede escalation. The target schedule never asks a principal to enter a dry continuity state after maximum wet on the same day.
- **Blood:** 11 target days carry blood. S1 first-blood/full-battle/aftermath remain consecutive state blocks; no clean palace work follows S1-D before the protected clean/restored plates are signed.
- **Night:** controlled interior night is grouped inside standing sets. Exterior night carries turnaround and lighting limits in the day record.
- **Crowds:** the six ensemble pools are called by block; Suitors remain fixed through S1-B..E and never convert to EP30 kin.
- **VFX/stunt:** 25 target stunt days and 28 target VFX/creature days include plates/rehearsal in the planned shot count, not as unpaid end-of-day additions.

## No-company-move result

TARGET has zero public-road company-move days. Multiple story locations on a day are standing-set zones, controlled redresses or adjacent sub-units inside an already established block. The schedule does not claim a second savings from moves already eliminated.

## Option change control

Moving from TARGET to LEAN requires line producer, 1st AD, director, DP and relevant safety department sign-off for each consolidated day. Moving to SAFE adds buffer and technical isolation; it does not authorize new shots, scenes or spectacle. Schedule changes cannot move recognition, EP25–28 action geography, EP29 or EP30 below their protected coverage/rehearsal floors.

Final result: `TARGET_54_DAYS_RECOMMENDED_PASS`.
