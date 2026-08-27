# P9 Page Grammar

status: `FROZEN_P9_PAGE_GRAMMAR`

The publication master converts a vertical web sequence into left-to-right book rhythm. It does not screenshot the site. A page is a dramatic unit whose panel order, text, page parity and turn role are explicit in `P9_PAGE_MANIFEST.json`.

## Composition families

- `CHAPTER_OPENER`: one establishing narrative panel, episode number/title and a short source-bound hook. It starts on recto whenever possible.
- `FULL_BLEED_HERO`: one image can cross the trim edge; text and faces stay inside the safe area.
- `FULL_PAGE`: one decisive panel with vector speech/caption treatment.
- `TWO_PANEL`: two readable panels, normally stacked; the second changes or answers the first.
- `THREE_PANEL`: one anchor plus two smaller consequences. Used only when text load remains readable.
- `FOUR_PANEL`: four low-text beats with a clear left-to-right/top-to-bottom order.
- `ASYMMETRIC`: one dominant panel and one or two reaction/insert panels.
- `REACTION_SEQUENCE`: action/reveal followed by one or two human responses.
- `INSERT_SEQUENCE`: geography/action plus a custody-changing object detail.
- `QUIET_PAGE`: one or two silent/low-text panels; whitespace is intentional and never styled like an unloaded image.
- `CLIMAX_PAGE`: high-consequence action with no competing metadata.
- `SPREAD`: reserved for landscape, storm, monster, battle geography or major recognition; faces and key props never sit in the gutter.
- `CLIFFHANGER_PAGE`: the final source-bound beat, isolated enough to land but never padded by empty black UI blocks.

## Sequencing rules

1. Panel order remains the P7B narrative order.
2. A publication page contains panels from one scene unless an explicit transition is recorded.
3. Scene-first panels establish geography; reaction and insert panels are grouped with their causal beat.
4. A reveal is placed after a page turn when the adjacent grouping permits it without inserting a meaningless blank page.
5. Chapter length is adjusted with legitimate panel regrouping so the next chapter can begin on recto.
6. Caption, speech and silent beat remain different typographic objects. Full source prose never becomes front-facing publication UI.
7. Intentional detail crops retain their source panel ID and are separately counted.

## Page geometry

- Trim: ISO B5, 176 × 250 mm.
- Bleed: 3 mm for print-layout output.
- General safe area: 12 mm; binding side: 15 mm.
- Reading: left-to-right, top-to-bottom.
- Important faces, hands, weapons, recognition objects and all text remain out of the gutter/trim danger zone.
