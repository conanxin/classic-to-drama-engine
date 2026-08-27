# EP01 Final Comic Grammar Repair Review

## Scope

`ODYSSEY-P8R2` is limited to EP01 Graphic Mode presentation. It preserves the five scenes, all 17 narrative slots, the P8/P8R1 visual selections, exact-source dialogue, Script Mode, and the character/context assists. It does not propagate the grammar to EP02–EP30 and does not perform P8 final closeout.

## Before

- The P8R1 direction already read as a graphic narrative, but lazy image delivery could expose black, image-sized rectangles carrying only a caption or dialogue. Human review reasonably read those states as missing comic panels.
- The cover still opened with a large project-like black copy pane before the art carried the story.
- Scene 4 had four slots, but its second slot repeated the assembly composition instead of functioning clearly as the listeners' reaction.
- Speech and narration were structurally distinct but still close enough in rectangular treatment to feel like interface cards.

## After

- Every EP01 panel has a lightweight responsive derivative of its real approved artwork as the immediate panel background. The high-resolution image remains responsive and lazy where appropriate; the reader no longer sees caption text stranded inside a black image rectangle.
- Text-only helpers use intrinsic height. The consequence note and collapsed source control occupy only the height their content needs.
- The cover is now a story-first full-art composition. Episode identity, title, core hook, and the Script/Graphic switch sit over the hero art; runtime, source, and progress live behind one optional disclosure.
- Character assistance remains at GLANCE level in the scene flow, with CONTEXT and DETAIL on demand.
- Narration is a compact dark caption attached to the image edge. Speech is a light, speaker-coloured, tailed element aligned left or right according to the scene composition.

## Panel Sequence

The original 17 narrative slots remain intact:

| Scene | Composition | Visual reading sequence |
|---|---|---|
| EP01-S01 | establish–reaction pair | violated household → cup passes out of reach → Penelope reads the violation → Telemachus recovers the marked cup |
| EP01-S02 | threshold dialogue | guest at the threshold → Telemachus performs hospitality → the occupied chair becomes a test |
| EP01-S03 | intimate prop triptych | inventory proof → the bone breaks at day forty-one → a route replaces passive waiting |
| EP01-S04 | crowd action mosaic | assembly and Telemachus's demand → suitor/listener reaction crop → Penelope receives the evidence → the demand becomes public consequence |
| EP01-S05 | intimate cliffhanger | inherited sword does not fit → the truth he seeks is named → his own short knife and route carry him toward EP02 |

## Scene 4 Repair

No new art was needed. `EP01-S04-PNL02` now uses a deliberate reaction crop of the existing accepted assembly artwork, holding on the seated suitors rather than repeating the wide speech composition. The following Penelope panel carries reaction plus evidence transfer; the fourth slot remains the consequence beat. The sequence is therefore legible as establish → action/speech → listener reaction → consequence.

## Layout Variation

The five P8R1 compositions are preserved. P8R2 changes their presentation hierarchy, not their narrative authority: cover, wide-plus-pair, threshold sequence, intimate triptych, crowd mosaic, and cliffhanger retain distinct pacing.

## Empty-Block Removal

- Real-art preview coverage: 17/17 slots.
- Text containers with artificial panel-like minimum height: 0.
- Full source text remains collapsed.
- Panel-sized empty text rectangles permitted: 0.

## Dialogue Grammar

- `SPEECH`: semantic HTML, speaker label, speaker colour, directional tail, character-aligned placement.
- `NARRATION CAPTION`: compact dark strip anchored to the visual; no speech tail and no speaker badge.
- `ORIENTATION ASSIST`: compact scene header or on-demand disclosure.
- `SOURCE LAYER`: collapsed by default and visually subordinate.
- Rasterized Chinese text: 0.

## Mobile Behaviour

At 390×844, panels become one continuous column. Reaction crops remain intentional, dialogue has a minimum readable width without horizontal overflow, helpers remain content-height, and source details stay collapsed. The cover remains art-first instead of forcing the reader through a tall text-only panel.

## Acceptance Boundary

The intended default reading path is now art → caption → essential dialogue → reaction → next beat. A reader can follow all five scenes without opening the source layer. Series propagation remains explicitly unauthorized pending a new human EP01 review.
