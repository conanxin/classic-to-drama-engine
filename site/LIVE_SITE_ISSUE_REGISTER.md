# CTDE-WEB-02 Live Site Issue Register

Scope: public GitHub Pages archive only. P6 remains `PAUSED_BY_USER`; V2, P3, P4, P5 and Runtime are immutable.

## WEB02-001 — English search could fall into a stale error state

- issue_id: `WEB02-001`
- route: `/search/`
- viewport: desktop and mobile
- severity: `S1 major`
- category: search / resilience
- reproduction: run the required Chinese query set, then search `recognition`.
- expected: current results with title, type, excerpt and a valid internal route.
- actual: the Pagefind worker could fail with invalid compressed index data; the single shared error boundary replaced the status while leaving the previous query's results visible.
- root cause: deterministic substring search and Pagefind were coupled through one failure path.
- fix: make the deterministic case-folded index independently authoritative for exact Chinese and English matches; invoke Pagefind only when the deterministic index has no match; never retain stale results behind an error status.
- verification: local production build returns 18 current `recognition` matches and valid results for all 13 required terms with zero console error/warn entries.
- status: `FIXED_LOCAL_PENDING_LIVE_DEPLOYMENT`

## WEB02-002 — Desktop images lacked intrinsic geometry and used original PNGs

- issue_id: `WEB02-002`
- route: `/`, `/visual/`, `/storyboards/*`, `/animatics/`, `/characters/*`
- viewport: desktop 1440×900 and 1920×1080
- severity: `S2 moderate`
- category: performance / CLS / image delivery
- reproduction: open the home page on desktop and inspect the P4-HF-01 hero request and image attributes.
- expected: a right-sized WebP with width and height available before decode.
- actual: the 2,598,096-byte source PNG was selected; `width` and `height` were absent.
- root cause: publication generation produced only a mobile derivative and the shared image component did not expose source dimensions.
- fix: deterministically generate `-w720.webp` and `-w1600.webp`, emit image metadata, use a width-based `srcset`, add intrinsic dimensions and async decoding, and verify both derivative families.
- verification: P4-HF-01 desktop candidate is 202,762 bytes; mobile candidate is 45,296 bytes; all 254 published images have dimensions and both derivatives.
- status: `FIXED_LOCAL_PENDING_LIVE_DEPLOYMENT`

## WEB02-003 — P4 teaser was allowlisted but had no public viewer entry

- issue_id: `WEB02-003`
- route: `/watch/`
- viewport: desktop and mobile
- severity: `S2 moderate`
- category: media / archive completeness
- reproduction: browse the live Watch page and crawl video references.
- expected: primary P5 Pitch Teaser plus the earlier P4 visual-development teaser, both explicitly labelled PREVIS.
- actual: only P5 and the 30 episode animatics were linked, exposing 31 of 32 approved videos.
- root cause: the generated media model contained `p4_teaser`, but the Watch template rendered only `pitch_teaser`.
- fix: add a secondary P4 PREVIS viewer with an approved poster, native controls and `preload="none"`; retain P5 as the primary 90-second feature.
- verification: local Watch page exposes two labelled videos; P5 reports 90.0 seconds and is seekable; P4 remains at readyState 0 before interaction.
- status: `FIXED_LOCAL_PENDING_LIVE_DEPLOYMENT`

## WEB02-004 — Reader preference state was visual-only and theme was page-scoped

- issue_id: `WEB02-004`
- route: `/episodes/*` and deep routes after leaving the reader
- viewport: desktop and mobile
- severity: `S2 moderate`
- category: reader UX / accessibility
- reproduction: change font, width or color mode, reload, then navigate to a project route.
- expected: persistent settings, programmatically exposed selected controls, system mode before override, and consistent color mode on deep routes.
- actual: localStorage persistence worked, but controls had no `aria-pressed`; light variables existed only inside episode CSS; system preference was not applied explicitly.
- root cause: reader settings owned color presentation that belongs to the global shell.
- fix: apply system preference in the document head, retain user override across routes, move light tokens to global theme CSS, and synchronize `aria-pressed` plus contextual color-toggle labels.
- verification: system light initializes as `source=system`; user dark survives reload and `/project/provenance/`; large/wide survives EP27→EP30; selected controls expose correct `aria-pressed` values.
- status: `FIXED_LOCAL_PENDING_LIVE_DEPLOYMENT`

## WEB02-005 — Storyboard navigation stopped at each board image

- issue_id: `WEB02-005`
- route: `/storyboards/[episode]/`
- viewport: desktop and mobile
- severity: `S2 moderate`
- category: storyboard reader / keyboard accessibility
- reproduction: open a technical board in the lightbox and attempt to continue without closing it; reach the end of an episode page.
- expected: previous/next board, Escape close, previous/next episode, storyboard index and screenplay return.
- actual: the lightbox only enlarged and closed one image; the footer only linked to the screenplay and index.
- root cause: navigation state was not represented in the viewer.
- fix: add board index state, previous/next controls, disabled boundaries, ArrowLeft/ArrowRight, explicit Escape close, live board/shot label, and adjacent episode links.
- verification: EP27 advances from `EP27-S01-P01` to `EP27-S01-P02`, updates shot IDs, disables the first previous control, closes on Escape, and links EP26/EP28.
- status: `FIXED_LOCAL_PENDING_LIVE_DEPLOYMENT`

## WEB02-006 — Curated documents lacked archive return and sequential reading

- issue_id: `WEB02-006`
- route: `/documents/[slug]/`
- viewport: desktop and mobile
- severity: `S2 moderate`
- category: document reader / navigation
- reproduction: open Character Voice Bible and finish or abandon the document.
- expected: TOC and heading anchors plus an obvious route back to Production and adjacent curated documents.
- actual: TOC, anchors, tables and frozen GitHub source links existed, but there was no back/previous/next navigation.
- root cause: the document component received only the current record.
- fix: pass adjacent manifest records, add a Production back link and previous/next document footer.
- verification: Character Voice Bible exposes 17 TOC links, 17 anchored headings, frozen source, Production return, Editorial Result previous and Character Arc Audit next.
- status: `FIXED_LOCAL_PENDING_LIVE_DEPLOYMENT`

## WEB02-007 — One transient GitHub Pages edge response during the first crawl

- issue_id: `WEB02-007`
- route: `/storyboards/11/`
- viewport: HTTP crawler
- severity: `S3 polish`
- category: hosting resilience / audit accuracy
- reproduction: first 94-route crawl returned the GitHub `Unicorn!` 503 page once.
- expected: 200 HTML.
- actual: one transient 503; an immediate independent request returned the correct 200 page.
- root cause: transient GitHub Pages edge response, not a deterministic site route or artifact failure.
- fix: live auditor retries bounded 5xx responses while still failing persistent route errors.
- verification: the subsequent full crawl completed 94/94 with zero route, canonical, asset, Range, privacy or rejected-image failures.
- status: `VERIFIED_RECOVERED`

## Register Summary

- S0: 0
- S1: 1 fixed locally
- S2: 5 fixed locally
- S3: 1 recovered and hardened in audit tooling
- unresolved product issues: 0
- live deployment verification: pending
