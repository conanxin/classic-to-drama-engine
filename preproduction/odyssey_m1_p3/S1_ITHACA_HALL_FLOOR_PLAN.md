# S1 Ithaca Hall Floor Plan — Frozen Director/Production Geometry

Status: `FROZEN_S1_FLOOR_PLAN`

Authority: Screenplay V2 EP01–02, EP20–30; V2 Production Bible; V2 Location Matrix; V2 Prop and Hero Asset List. This plan adds physical coordinates and shooting access without changing a V2 event.

## Coordinate lock

- Interior clear dimensions: `16 m west–east × 22 m south–north`, 6 m grid height.
- North is always screen-plan north. Battle coverage may cross a character axis only after a new north-establishing shot.
- Floor origin `(0,0)` is the center of the south wall. West is negative X; north is positive Y.
- The contest/arrow safe line is `X=0`, from shooting mark `(0,3)` through the twelve axes to practical backstop `(0,19)`. The royal seat is off-axis at `(-4.5,18.5)`.

```text
                              NORTH / N
        ┌────────────── N0 MAIN ENTRANCE ──────────────┐
        │  N2 royal dais / main seat     N1 backstop   │
        │        (-4.5,18.5)               (0,19)       │
        │                                               │
 W0     │   P3 ●            AXES LINE          ● P4    │  E0
 WEAPON │ (-3,14)             X=0            (3,14)    │  SIDE DOOR
 WALL   │                                               ├── courtyard
        │ west aisle       H0 hearth          east aisle│  / service
        │                (4.5,11)                       │
        │   P1 ●         center aisle          ● P2    │
        │ (-3,6)                               (3,6)    │
        │                                               │
        │ A0 ARMORY DOOR       B0 BOW MARK              │
        │ under stair (-5,1)     (0,3)                  │
        ├── S0 FAMILY STAIR ── S1 SOUTH CAMERA PORT ────┤
                     SOUTH / family rooms
```

## Fixed architectural elements

| ID | Element | Coordinate / dimension | Story and production rule |
|---|---|---|---|
| N0 | Main entrance | north center, 3.2 m double leaf | Public/guest route. Barred before EP26 reveal; cannot be silently reopened during battle. |
| E0 | Servant side door | east wall `(8,9)`, 1.1 m leaf | Links hall to inner courtyard and service yard. Eumaeus guards it; bodies/table create one-person choke in EP27. |
| S0 | Family stair | southwest run, 1.4 m clear | Penelope/women route between upper rooms and hall. Athena/Mentor may emerge from its shadow; never becomes an untracked escape. |
| A0 | Armory access | under S0 at `(-5,1)`, 0.9 m door | Hall → dark corridor → store. Store also connects upward by G0 grain ladder to courtyard shed roof. Telemachus leaves A0 one finger open in EP27. |
| W0 | Weapon wall | west wall, Y 7–16 | Full in early occupation; emptied in EP22; hooks remain visible through EP28. Removable/wild wall for camera only, never an in-story exit. |
| P1–P4 | Four columns | `(-3,6)`, `(3,6)`, `(-3,14)`, `(3,14)` | Divide west, center, east aisles and define two battle lines. Practical impact sleeves and replaceable blood skins required. |
| H0 | Hearth | `(4.5,11)`, 2.2 m diameter | Offset from arrow line. Low practical flame; fallen pan in EP27 may spill but must not block E0. |
| N2 | Dais/main seat | northwest, 0.45 m rise | Antinous occupies Odysseus’ seat; off the test-arrow line but visible from B0. One step and table edge are stunt hazards. |
| B0 | Bow/stringing mark | `(0,3)` | Odysseus strings here; test shot moves half-step south to `(0,2.5)`. Permanent floor witness mark hidden under contest mat outside S1-B. |
| AX01–AX12 | Twelve axe bases | X=0, Y 5.0–16.0 at 1 m centers | Numbered south-to-north; safe hollow/hero heads. Alignment cannot be reset between EP25 and EP26 coverage. |
| N1 | Arrow backstop | north wall `(0,19)` | Timber target with replaceable face; shields N0 sightline. Cleared before pivot toward N2. |
| T-W/T-C/T-E | Table lanes | west/center/east between columns | Independent breakaway tables. Central tables become moving wall; west and east tables create crawl/throw cover. |
| C0 | Courtyard | east of E0 | Witness holding, cleanup, side-door lock, and access to G0 shed roof. Courtyard is not visible as an unlimited safe exit. |
| G0 | Grain ladder | armory-to-courtyard shed | Two-person bypass used by Eumaeus and Philoetius in EP28. Height work; controlled platform and fall protection. |

## Character routes

| Route ID | Character/use | Locked path | Continuity purpose |
|---|---|---|---|
| R-PEN | Penelope | upper private rooms → S0 → south threshold → hall perimeter → dais/contest line | She controls whether private knowledge enters public space. She does not use E0 as a servant shortcut. |
| R-TEL-PUB | Telemachus public | N0/assembly return → east aisle → P2/P4 line → south family boundary | Early episodes keep him at edges; EP26 places him beside B0/P2, not in father’s place. |
| R-TEL-ARM | Telemachus armory | P2 line → south crossing → A0 → store → same path back | His known route creates EP27 access and the unlatched-door consequence. |
| R-SERV | Servants/herdsmen | courtyard C0 → E0 → east aisle/service tables | Makes food, keys, cleanup, and witness movement legible. E0 is a controllable choke. |
| R-OD-BOW | Odysseus contest | east guest edge → B0 → half-step south → pivot northwest to N2 | Test shot and first blood share a body orientation without placing actors behind the safe arrow line. |
| R-ARM-BYPASS | Herdsmen | C0 shed → G0 → armory rear → A0/hall | EP28 capture route; never available to suitors because C0/E0 custody is controlled. |
| R-WOMEN | Women/inner rooms | S0 landing → upper corridor | Locked during battle. No stunt or crowd traffic crosses this route. |

## Doors, custody, and escape logic

| Portal | S1-A | S1-B | S1-C/D | S1-E | S1-F |
|---|---|---|---|---|---|
| N0 main | public/open | closed, then barred | barred; no exit | controlled cleanup | public under guard |
| E0 side | working/service | Philoetius locks; key to Eumaeus | Eumaeus guard → body/table choke | witness/cleanup controlled | normal service |
| S0 stair | household controlled | women withdrawn upstairs | guarded/unused by fighters; Athena entry only | Eurycleia descends | family route restored |
| A0 armory | locked after EP22 | locked | opened by Telemachus; left ajar; rebarred EP28 | evidence seal | locked under new custody |
| G0 grain ladder | service maintenance | clear but unknown to suitors | herdsmen bypass | safety/evidence route | maintenance only |

In-story escape routes are only N0, E0, S0, and A0/G0. Wild walls, camera ports, smoke extraction, and stunt pads are never staged as character exits.

## Camera walls and wild walls

- `WW-W`: weapon wall W0 and lower-west return remove in three sections. Reinstall exact hook/grid witnesses before every wide.
- `WW-E`: east wall south of E0 removes for performance two-shots and battle lateral track. E0 frame remains practical.
- `WW-S`: south-center camera port behind B0 provides the protected axes-line lens. S0/A0 architecture stays in frame or is re-established.
- `WW-NW`: dais quarter removes for Penelope/Odysseus eyeline and EP29 shared-frame work. N0/N1 geometry remains fixed.
- Overhead removable grid supports top shot, Athena shield pattern, and clean VFX plates. It is not a playable balcony.
- `CAM-TRACK-1`: west–east recessed floor track south of P1/P2; covered during actor/stunt work.
- `CAM-TRACK-2`: north–south east-aisle lane; prohibited when E0 is an active stunt route.

## Choke points and safe zones

1. `CH-N`: N0 double door, broad but barred; crowd pressure only, no uncontrolled crush.
2. `CH-E`: E0 one-person side door; bodies and one flipped table may narrow it, never fully obstruct fire egress off-camera.
3. `CH-C`: central aisle between P1/P2 and P3/P4; table wall creates controlled funnel.
4. `CH-W`: west aisle against empty weapon hooks; dangerous because no lateral escape after table rotation.
5. `CH-A`: A0 armory threshold; one performer at a time, padded jamb, separate stunt insert for impact.
6. `SAFE-S`: south family stair landing; no thrown weapons cross its marked 30-degree exclusion cone.
7. `SAFE-C0`: courtyard holding zone for noncombatants and medical reset.

## S1 story-state transitions

| State | Episodes/scenes | Physical state | Transition lock |
|---|---|---|---|
| S1-A CLEAN OCCUPIED | EP01–02; EP20–24 before contest | Structure intact; suitor food/wine and personal objects displace household order; W0 becomes empty in EP22; old stool/loom damage remains | Photograph clean architecture, then occupation dressing and weapon-removal witnesses before any contest installation. |
| S1-B CONTEST | EP25–EP26-S03 | AX01–12 aligned; B0 and N1 live; W0 empty; N0/E0 closure prepared; bow/12-arrow custody active; floors dry | No blood or battle debris. Shoot EP29 clean hall/bedroom material before moving past this state. |
| S1-C FIRST BLOOD | EP26-S04–S05; EP27-S01 | Antinous at N2/main table; test arrow becomes first-blood arrow; cup/table fall; first blood path follows table seam; one/two bodies | Arrow ledger begins at 11 after Antinous. Cup moves behind column and cannot reset to table. |
| S1-D FULL BATTLE | EP27-S02–EP28-S04 | Table wall, spilled wine, hearth pan, bodies, damaged columns, open/rebarred A0, shields/spears, escalating blood, Telemachus arm wound | Build in numbered damage layers D1–D6. No clean-state insert after blood application without an independently dressed duplicate. |
| S1-E AFTERMATH | EP28-S05; EP29 opening hall | Bodies removed by defined routes; sulfur smoke; water and blood residue; W0 still empty; cup washed; grout and cloth damage remain | Cleanup reduces loose blood but does not erase consequence. Photograph residue map before EP29 hall coverage. |
| S1-F RESTORED | EP29–EP30 palace intercut | Hall safe and ordered but visibly repaired; doors under explicit custody; bedroom/bed root intact; weapon store barred | Restoration is governance, not visual reset. Scars on grout/column and missing objects remain. |

## Shooting-state order

For cost and continuity, production order is `S1-A → S1-B → S1-F clean bedroom/hall → S1-C → S1-D → S1-E`. S1-F is filmed early but logged as story state after S1-E. Each turnover requires a 360° reference set, prop ledger, floor laser check, and signed script-supervisor/art-department handoff.

## Freeze acceptance

- Required episodes mapped: EP01–02, EP20–30 — `PASS`.
- Main/side/inner/armory/courtyard access defined — `PASS`.
- Bow and twelve-axes geometry defined — `PASS`.
- Four columns, hearth, tables, camera/wild walls defined — `PASS`.
- Penelope, Telemachus, servant, armory-bypass routes defined — `PASS`.
- Escape routes and battle choke points defined — `PASS`.
- S1-A through S1-F transitions and shoot-order continuity defined — `PASS`.

Final S1 status: `FROZEN_S1_FLOOR_PLAN`.
