# 《归途：奥德修斯》P9 Publication Bible

status: `FROZEN_P9_PUBLICATION_MASTER`

## Product

P9 packages the completed P8 comic edition as a five-volume book system plus a digital omnibus. It creates digital PDF, B5 print-layout PDF master, native EPUB 3 and CBZ editions from one machine-readable page model. It changes no narrative, dialogue, panel order or visual authority.

## Reader promise

The edition enters the story quickly, preserves the established recognition chain and uses page turns—not web UI—to control reveal, response and consequence. Front matter is short: half title, title/edition note, contents, a spoiler-safe character guide and a compact world orientation. Technical provenance moves to back matter and the Web Archive.

## Format contract

- Master trim: ISO B5 176 × 250 mm; 3 mm bleed; 12 mm safe area, 15 mm binding side.
- Reading direction: left-to-right.
- Chapters: EP01–EP30 in formal order; each has opener, comic body and cliffhanger.
- Source panels: all 643 P8 accepted slots mapped exactly once as primary placements. Detail crops, if any, are explicit secondary placements.
- Digital PDF: RGB, searchable text, bookmarks, linked contents and optimized images.
- Print-layout PDF: B5 trim/bleed/crop marks, high-resolution source use and embedded Chinese font; `PRESS_READY` is not claimed.
- EPUB 3: XHTML speech/captions, EPUB navigation, alt text and chapter landmarks; not a PDF conversion.
- CBZ: deterministic page rasterization with zero-padded order and `ComicInfo.xml`.
- Omnibus: complete 30-chapter digital PDF only; no print omnibus claim.

## Editorial boundaries

All panel art comes from P8 accepted authority. Cropping, scaling and composition are allowed; repainting is not. Text is sourced from P7B/P8R3 machine authorities. No ISBN, publisher, press profile, paper stock, printer acceptance or commercial rights registration is invented.

## Accessibility

PDF text is selectable/searchable and chapters are bookmarked. EPUB is the primary semantic-accessibility edition: real text, headings, navigation and panel alt text. CBZ is inherently page-raster based and is supplied as a compatibility format, not the accessibility authority.

## Delivery strategy

Source/layout data is tracked in Git. Large deterministic exports are release assets and local generated artifacts, not normal Git objects. `/publication/` exposes the five-volume architecture, online edition and release downloads without preloading binaries.
