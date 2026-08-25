# P7B Panel Grammar

Status: `FROZEN_P7B_PANEL_GRAMMAR`

## Purpose

This grammar converts the frozen 30×5-scene Screenplay V2 into a continuous Graphic Novel Script without replacing Script Mode. A panel is a narrative placement bound to one P3 shot, one approved P4/P5 visual authority, one source scene, and optional exact-source text. It is not a claim of final comic art.

All speech, captions, speaker names, interface labels and sound/narrative text remain semantic HTML. No P7B Chinese dialogue or narration is baked into raster media.

## Panel families

| Type | Narrative use | Default ratio | Text placement | Mobile rule |
|---|---|---:|---|---|
| `ESTABLISHING` | Establish WHERE and the controlling route | 16:9 | one short lower caption when needed | full-width first panel |
| `TWO_SHOT` | Make relationship distance readable | 3:2 | dialogue may bridge the two figures | full-width; never squeeze into two columns |
| `CLOSE_UP` | Recognition, restraint, decision | 4:3 | one bubble or silence | crop remains face/hand legible |
| `REACTION` | Register consequence after an action | 4:3 | usually silent; optional short caption | follows its initiating panel |
| `ACTION` | Show an executed physical beat | 16:9 | minimum text; verb remains visible in image/action line | full-width for EP26–28 |
| `INSERT_PROP` | Bind evidence, custody or recognition object | 1:1 | prop label in HTML, not image | may sit beside text on desktop; full-width on mobile |
| `REVEAL` | Change reader understanding or identity state | 16:9 | delayed caption/bubble below image | no overlay that hides the reveal |
| `POV` | Restrict knowledge to a character view | 3:2 | reader/character knowledge note outside image | explicit accessible alt |
| `TRANSITION` | Carry geography, time or condition change | 3:2 | short caption only | reduced vertical gap |
| `ENVIRONMENT` | Let home, sea, cave or hall act as pressure | 16:9 | usually silent | wide landscape crop |
| `CLIMAX` | Finish the scene/episode on a visual consequence | 16:9 | final exact-source line or silence | full-width; never thumbnail |
| `SILHOUETTE` | Preserve disguise, divine distance or threat | 16:9 | no identity-spoiling label | use only when knowledge state requires it |

## Adaptive density

- Complexity 1–3: 3 panels.
- Complexity 4: 4 panels.
- Complexity 5–6: 5 panels.
- Complexity 7–10, fight, stunt, creature, or medium/high VFX: 6 panels.
- P3 shot order is never reordered. First/last beats and exact high-fidelity shot matches are retained.
- Panel count is a ceiling on useful visual beats, not a target to inflate.

The frozen rollout produces 643 placements across 150 scenes, inside the authorized preferred range of 450–650.

## Bubble grammar

1. Bubbles contain only exact V2 dialogue selected from the source scene.
2. Speaker name, faction cue and character assist are HTML text.
3. One panel carries at most one selected dialogue beat in the rollout layer; the full exchange remains in the expandable source layer.
4. A bubble follows the picture it motivates. It cannot float above an unrelated image.
5. Silent panels are intentional when reaction, recognition, travel, violence aftermath or restraint is the beat.
6. No line is rewritten for “comic effect.” Selection and omission are allowed; paraphrase is not.

## Caption and action grammar

- The first and last selected action sentences provide a scene bridge where useful.
- Captions are exact V2 action excerpts or frozen P7A prototype narrative for EP01/19/27.
- P3 `blocking` remains machine-readable as `visible_action`; it may support accessibility/provenance without being duplicated as a paragraph on every panel.
- When the image already shows an action, the normal reader surface prefers silence or one short exact caption.
- Every scene keeps a complete expandable V2 source layer.

## Visual authority and crops

1. Exact-shot P4 approved high-fidelity image.
2. Single-frame crop from a P4 technical storyboard page.
3. Clean narrative crop from a P5 animatic timing card.
4. Episode color key only for a cover when no approved episode hero exists.

P4 technical pages are cropped to one frame and P5 cards to the story field; production headers and technical footers are excluded. Provenance remains available in panel metadata. Rejected P4 hero targets remain forbidden.

## Layout rhythm

- Desktop alternates wide anchors, paired medium panels and single performance panels.
- Mobile is one continuous column at 390×844; no desktop grid is scaled down.
- Recognition and action climaxes use a wide beat followed by a quieter consequence.
- Repeated source assets are prohibited inside a scene. The deterministic rollout uses one unique visual authority per placement.
- Lazy loading begins after the first scene anchor. The current episode never requests assets from the other 29 episodes.

## Accessibility

- Every image has source-bound alt text.
- Dialogue remains selectable/searchable HTML.
- Panel sequence uses semantic ordered structure.
- Details/popovers are keyboard and touch accessible.
- Decorative provenance labels cannot be the only way to understand a beat.
