# EP01 Comic Reading Grammar Repair Review

## Formal status

- repair_id: `ODYSSEY-P8R1`
- scope: `EP01_GRAPHIC_MODE_ONLY`
- result: `PASS_EP01_COMIC_READING_GRAMMAR`
- P8 final closeout: `NOT_EXECUTED`
- human follow-up: inspect the deployed EP01 Graphic page before any 30-episode propagation
- P6: `PAUSED_BY_USER`

## Before

The accepted P8 art was visually strong, but the reader assembled EP01 as an illustrated screenplay: one apparent master image, a large dark text region, another image, then another dark text region. Repeated right-bottom dialogue cards weakened speaker-to-image association. The cover was followed by a full orientation section, a full identity rail, and a relationship map before Scene 1. Five scenes used nearly the same visual rhythm. The last hook depended more on a large heading than on the final action.

## After

EP01 now enters the story through one compact strip: core conflict plus four essential cast glances. Full identity anchors and relationships remain available through progressive disclosure. The five scenes retain the authoritative 17 narrative slots, but each slot now participates in an explicit visual sequence. Seven slots use bounded P8R1 final-comic renders where the former single-master crops could not carry the causal beat. Captions, speech, silent action, orientation assistance, and the full source layer now have separate visual grammars.

No V2 dialogue or event was rewritten. The complete source scene remains folded under every scene.

## Human findings resolved

| Finding | Repair | Verification |
|---|---|---|
| F1 fake-empty black blocks | Panel cards no longer create large black containers. Story narration is attached to the relevant image; full source text is folded. | No EP01 scene bridge precedes the panel sequence; repair cards use transparent flow and image-bound text. |
| F2 one apparent image per scene | Seven causal beats received independent art. Existing accepted P8 art remains for the other ten slots. | 17 slots, seven P8R1 visual overrides, five scene sequences. |
| F3 fixed lower-right speech cards | Speech can be left/right, overlay/under-image, and remains semantic HTML. | Six alignment patterns are present; mobile normalizes them below the image. |
| F4 onboarding dominates story | Full identity rail is collapsed; the default entry shows only conflict and four essential characters. | Scene 1 follows the compact entry and optional relationship disclosure. |
| F5 five repeated scene templates | Five named compositions are frozen. | Five distinct composition values; required minimum was three. |
| F6 text lacks weight | Exact dialogue uses larger serif treatment and speaker-colored top rules; narration has a separate caption grammar. | Dialogue remains byte-for-byte equal to the P7B panel authority. |
| F7 weak end hook | The last visual becomes a full comic cliffhanger with one exact V2 line and an immediate EP02 entry. | Final frame shows the long sword put aside, short knife chosen, and the route turned toward the sea. |

## Panel sequence

### Scene 1 — establish / reaction pair

1. `EP01-S01-PNL01` — the occupied hall and the broken wine seal establish loss of household control.
2. `EP01-S01-PNL02` — Antinous passes the dolphin cup away while Telemachus reaches and misses.
3. `EP01-S01-PNL03` — Penelope pauses on the stair and looks first at the chopped seal.
4. `EP01-S01-PNL04` — Telemachus reclaims the cup and discovers the new chip.

### Scene 2 — threshold / dialogue sequence

1. `EP01-S02-PNL01` — Mentes knocks with the spear butt; Telemachus removes the bar himself.
2. `EP01-S02-PNL02` — the available seat becomes a test conducted under Antinous's gaze.
3. `EP01-S02-PNL03` — Telemachus converts the grain measure into a footstool and takes the seat.

### Scene 3 — intimate prop triptych

1. `EP01-S03-PNL01` — the tally board and empty shelves convert humiliation into a deadline.
2. `EP01-S03-PNL02` — the sheep bone reaches day forty-one and breaks.
3. `EP01-S03-PNL03` — Mentes redirects the boy from the door to Pylos and Sparta.

### Scene 4 — crowd / action mosaic

1. `EP01-S04-PNL01` — song, hall, and crowd make the conflict public.
2. `EP01-S04-PNL02` — Telemachus places his body between Penelope and the occupied tables.
3. `EP01-S04-PNL03` — Penelope takes the board while seeing the chipped cup.
4. `EP01-S04-PNL04` — Telemachus remains below as Penelope carries the evidence upstairs.

### Scene 5 — intimate cliffhanger

1. `EP01-S05-PNL01` — the father's sword drags and overturns the basin.
2. `EP01-S05-PNL02` — Eurycleia accepts the key and the secret, but demands his return.
3. `EP01-S05-PNL03` — Telemachus puts aside the long sword, chooses his short knife, and turns the route toward the night sea.

## Dialogue grammar

- `NARRATION CAPTION`: attached to the image edge, not placed in a separate content slab.
- `SPEECH`: speaker first, exact dialogue second, with a character-color anchor.
- `THOUGHT / INTERNAL`: supported by the grammar but unused in EP01 because the source does not authorize an internal line.
- `ORIENTATION ASSIST`: location, people, and stakes remain compact and optional.
- `SOURCE LAYER`: complete V2 scene text remains folded and unchanged.
- `SILENT ACTION`: no explanatory text is added when the action image is sufficient.

## Layout variation

The five compositions are `establish-reaction-pair`, `threshold-dialogue-sequence`, `intimate-prop-triptych`, `crowd-action-mosaic`, and `intimate-cliffhanger`. Their desktop widths and speech alignments differ; none require a repeated master/medium/reverse template.

## Empty-block removal

EP01 suppresses the pre-panel prose bridge because the information is already carried by scene stakes, images, captions, and dialogue. Consequences are short ruled transitions. Production provenance and full source text remain folded. No placeholder, TODO block, or empty image container is introduced.

## Mobile behavior

At `390 × 844`, every sequence becomes a single stream. Images retain their natural ratio, captions follow the image, and overlay speech becomes a full-width semantic block rather than shrinking across a face. The scene progress control remains available without adding a sidebar or horizontal overflow. The cliffhanger uses a single tall image with its text anchored above the bottom safe area.

## Image generation disclosure

Seven limited EP01 sequence renders were created from approved P4/P8 identities and scene references. Three candidates were rejected for `NARRATIVE_AMBIGUITY`, `PROP_ERROR`, or `IDENTITY_DRIFT`; rejected files are preserved as evidence and excluded from the publication manifest. No Chinese text is baked into any image.

## Scope preservation

- V2_modified: `0`
- P3_modified: `0`
- P4_modified: `0`
- P5_modified: `0`
- Runtime_modified: `0`
- P7B_narrative_authority_modified: `0`
- P8_visual_authority_modified: `0`
- EP02–EP30 presentation propagation: `0`

