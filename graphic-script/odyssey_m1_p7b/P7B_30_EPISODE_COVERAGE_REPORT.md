# P7B 30-Episode Coverage Report

status: `PASS_FULL_SERIES_GRAPHIC_COVERAGE`

## Coverage gate

| Measure | Actual | Required | Result |
| --- | ---: | ---: | --- |
| Graphic episodes | 30 | 30 | PASS |
| Script episodes preserved | 30 | 30 | PASS |
| Graphic scenes | 150 | 150 | PASS |
| Source-bound scenes | 150 | 150 | PASS |
| Complete source layers | 150 | 150 | PASS |
| Scene visual coverage | 150 | 150 | PASS |
| Episode covers | 30 | 30 | PASS |
| End hooks | 30 | 30 | PASS |
| Graphic previous/next chain | 30 episodes / 29 transitions | complete | PASS |
| Character labels resolved | 76 / 76 | 100% | PASS |
| Empty scenes | 0 | 0 | PASS |

## Panel inventory

- panel placements: `643`
- unique published panel assets: `643`
- exact-source dialogue bubbles: `381`
- approved P4 high-fidelity placements: `48`
- storyboard-derived placements: `344`
- animatic-derived placements: `251`
- newly generated raster assets: `0`
- nonblocking P8 upgrade queue: `104`

Panel types:

| Type | Count |
| --- | ---: |
| ESTABLISHING | 123 |
| TWO_SHOT | 123 |
| REACTION | 120 |
| REVEAL | 90 |
| TRANSITION | 69 |
| INSERT_PROP | 35 |
| ENVIRONMENT | 25 |
| CLIMAX | 23 |
| ACTION | 21 |
| POV | 14 |

## Batch verification

| Batch | Episodes | Scenes | Panels | Empty scenes | Result |
| --- | ---: | ---: | ---: | ---: | --- |
| 1 | EP02–EP06 | 25 | 99 | 0 | PASS |
| 2 | EP07–EP12 | 30 | 145 | 0 | PASS |
| 3 | EP13–EP18 | 30 | 134 | 0 | PASS |
| 4 | EP20–EP25 | 30 | 115 | 0 | PASS |
| 5 | EP26, EP28–EP30 | 20 | 87 | 0 | PASS |
| upgraded prototypes | EP01, EP19, EP27 | 15 | 63 | 0 | PASS |

The existing EP01, EP19 and EP27 narrative authorities were preserved and lifted into the P7B panel grammar. They were not silently rewritten as new episodes.

## Story movement authority

The Graphic directory uses the five movements recovered from the frozen 30-episode architecture:

1. EP01–EP04 — Ithaca disorder and departure;
2. EP05–EP08 — Telemachus' search and Odysseus' return to speech;
3. EP09–EP15 — voyage testimony, pride and loss;
4. EP16–EP24 — Ithaca return, disguise, loyalty and recognition preparation;
5. EP25–EP30 — bow, judgment, recognition and civic restoration.

## Source and continuity binding

- Every episode records the SHA-256 of its frozen V2 source file.
- Every scene records its V2 source index and exposes the complete source layer in the reader.
- Every panel records episode, scene, sequence, type, purpose, source authority, asset identity, crop/transform, cast, continuity and optional action-beat IDs.
- Nine recurring hero-prop families are tracked in `P7B_PROP_VISUAL_LEDGER.json`.
- All 44 EP26–28 action-previs beats are bound without changing order or custody logic.
- Six rejected P4 hero targets remain excluded from publication.

## Evidence boundary

`REAL_READER_VALIDATION: NOT CLAIMED`

`USER_ROLLOUT_AUTHORIZATION: CONFIRMED`
