# P9 Web Publication QA Report

status: `PASS_P9_LOCAL_WEB_PUBLICATION_QA`

## Publication center

- route: `/publication/`
- framework: Astro static generation
- volumes represented: 5 / 5
- download mappings: 21 / 21
- digital PDF links: 6 / 6
- EPUB links: 5 / 5
- CBZ links: 5 / 5
- print-layout links: 5 / 5
- approved cover derivatives: 5 / 5
- P9 release tag: `odyssey-p9-publication-v1.0.0`

## Local production-browser verification

- desktop viewport: 1280 px browser binding and 1440 × 900 screenshot review
- mobile viewport: 390 × 844
- horizontal overflow: 0
- broken images: 0
- cover natural-width failures: 0
- publication volumes in DOM: 5
- print-layout progressive disclosure: PASS
- keyboard-focusable print summaries: PASS
- semantic headings: one `h1`, ordered section headings
- source/local path leakage: 0
- large release asset preload: 0

At 390 × 844 the document scroll width remained below the viewport width, download rows retained usable width, and the five volume covers resolved through responsive WebP sources. The print-layout master remains a secondary disclosure with the `PRESS_READY: NOT_CLAIMED` boundary visible before download.

## Build verification

- P9 source verifier: PASS
- P9 dist verifier: PASS
- Astro diagnostics: 0 errors / 0 warnings / 0 hints
- static route generated: PASS
- Pagefind indexing: PASS

## Deployment evidence

Pending implementation commit, GitHub Release publication, Pages deployment and live re-verification. This report will be frozen again after those external states exist.
