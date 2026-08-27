# P9 Web Publication QA Report

status: `PASS_P9_WEB_PUBLICATION_QA`

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

- implementation commit: `810e699de675c180a26d3c5160eda571f7dc70c9`
- release: `https://github.com/conanxin/classic-to-drama-engine/releases/tag/odyssey-p9-publication-v1.0.0`
- release assets: 21 / 21
- release bytes: 1,559,135,367
- release target commit: implementation commit, exact match
- sampled release Range delivery: omnibus PDF / EPUB / CBZ / print-layout PDF all HTTP 206
- Pages workflow run: `33092566840`
- Pages workflow status: SUCCESS
- public route: `https://conanxin.github.io/classic-to-drama-engine/publication/`
- live public route HTTP: 200

## Live full-site verification

- audited at: `2026-08-27T17:27:25.481Z`
- sitemap routes: 130
- route failures: 0
- canonical failures: 0
- internal assets checked: 2,866
- internal asset failures: 0
- video Range checks: 32 / 32
- privacy leaks: 0
- rejected visual promotions: 0
- robots / sitemap declaration: PASS
- duplicate titles: 0

Production Chromium reloaded the public route, traversed the full document to trigger lazy delivery, and verified all ten cover placements. Desktop 1440 × 900 and mobile 390 × 844 both had zero horizontal overflow, zero broken images, 21 release links, and five accessible print-layout disclosure controls. Large exports remain GitHub Release downloads and are not embedded in the Pages artifact or preloaded by the publication center.
