# CTDE-WEB-02 Live Deployment QA Report

status: `PASS_CTDE_WEB_ARCHIVE_DEPLOYED_AND_LIVE_VERIFIED`

public_url: `https://conanxin.github.io/classic-to-drama-engine/`

tested_at: `2026-08-22T01:57:45.579Z`

phase_start_commit: `a233bfe5bea569cf07587b4894bc7ddb0553d67f`

deployment_commit: `c03587dcb14f254c76563c6f46bd8805bc7a4629`

workflow_run: `https://github.com/conanxin/classic-to-drama-engine/actions/runs/32544769018`

workflow_result: `build SUCCESS; deploy SUCCESS`

## Acceptance Summary

| Area | Result | Live evidence |
| --- | --- | --- |
| GitHub Pages | PASS | Public archive and deep routes return production content under `/classic-to-drama-engine/`. |
| Route crawl | PASS | 94/94 sitemap routes; zero persistent HTTP, redirect, canonical or content-type failures. |
| Assets | PASS | 802 allowlisted/runtime assets audited; zero broken references. |
| Video delivery | PASS | 32/32 approved videos return valid Range responses. |
| Script reader | PASS | 30/30 published; EP01, 10, 19, 25, 27, 29 and 30 read in full in the live browser. |
| Search | PASS | 13 required Chinese/English queries return current title/type/excerpt/routes without errors. |
| Visual archive | PASS | Approved assets only; six rejected hero targets have zero promoted occurrences. |
| Storyboards | PASS | Technical labelling, lazy pages, adjacent episode navigation and keyboard lightbox controls work. |
| Teasers / animatics | PASS | P5 and P4 PREVIS available; 30 animatics exposed without eager video loading. |
| Desktop / mobile | PASS | 1920×1080 and 390×844 verified; no document-level horizontal overflow. |
| Accessibility | PASS | Semantic shell, skip link, visible focus, reader pressed states, keyboard lightbox and native media controls. |
| Privacy | PASS | Zero local-path, credential, token or environment-path disclosures in live HTML/JSON. |
| SEO | PASS | Robots, sitemap, canonical URLs, Open Graph and unique episode titles use the Pages subpath. |

## Live Route and Asset Crawl

- routes checked: `94`
- route successes: `94`
- redirect loops: `0`
- GitHub Pages 404 responses: `0`
- internal broken references: `0`
- canonical failures: `0`
- duplicate page titles: `0`
- assets checked: `802`
- asset failures: `0`
- video Range checks: `32`
- video Range failures: `0`
- privacy leaks: `0`
- rejected visual promotions: `0`

The first crawl observed one transient GitHub Pages edge `503` for `/storyboards/11/`; an immediate independent request returned `200`. The reproducible live auditor now retries bounded 5xx responses and continues to fail persistent errors. The final crawl passed 94/94.

## Script Reader

The seven required stratified episodes retained the exact V2 presentation authority and complete scene structure:

| Episode | Title | Scenes | Action blocks | Character cues | Dialogue blocks | Navigation |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| EP01 | 没有父亲的家 | 5 | 32 | 42 | 40 | next EP02 |
| EP10 | 我的名字叫无人 | 5 | 26 | 36 | 34 | EP09 / EP11 |
| EP19 | 父亲显形 | 5 | 18 | 33 | 31 | EP18 / EP20 |
| EP25 | 无人拉开的弓 | 5 | 22 | 34 | 32 | EP24 / EP26 |
| EP27 | 厅堂审判·上 | 5 | 24 | 41 | 39 | EP26 / EP28 |
| EP29 | 搬走我们的床 | 5 | 19 | 29 | 27 | EP28 / EP30 |
| EP30 | 归途之后 | 5 | 23 | 34 | 33 | EP29 / Project |

No scene, action, cue or ending was truncated. Scene headings, source metadata, previous/next controls and episode index links remained valid. EP27 at 390×844 had a 375 px article and 288 px dialogue measure, hidden desktop rail and no page overflow.

Reader settings were verified for small/medium/large, comfortable/wide and light/dark. User choices persist across reload and deep-route navigation; system preference applies before an override. The semantic screenplay remains readable without client-side settings JavaScript.

## Search

Required live queries all returned meaningful current results with valid subpath routes:

`奥德修斯`, `佩涅洛佩`, `忒勒马科斯`, `雅典娜`, `独眼巨人`, `弓`, `十二把斧`, `床`, `伤疤`, `伊萨卡`, `Odysseus`, `Penelope`, `recognition`.

The deterministic case-folded index is authoritative for direct CJK and English matches. Pagefind remains the fallback. This removes stale-result/error coupling while preserving static full-text search.

## Visual, Storyboard and Media QA

- `/visual/`: 51 displayed images; 50 lazy; zero missing dimensions; zero rejected P4 hero targets.
- EP27 storyboard: 13 technical board pages; P01→P02 and shot labels update in the lightbox; Arrow keys and Escape work; EP26/EP28 links resolve.
- P5 Pitch Teaser: 90 seconds, native controls, play/pause/seek and valid seekable range; no autoplay.
- P4 teaser: explicitly labelled PREVIS and starts with `preload="none"`.
- Animatics: 30 episode entries; no video `src` exists until the user opens one. EP01, 05, 10, 19, 27, 29 and 30 were sampled and were playable/seekable.

## Responsive Delivery and Performance Observations

The homepage hero no longer transfers the 2,598,096-byte source PNG by default. The published responsive candidates are 202,762 bytes at 1600 px and 45,296 bytes at 720 px, with intrinsic dimensions to prevent layout shift. All 254 approved published images have both derivative sizes and explicit geometry.

- production cold desktop homepage: approximately 209 KB transferred, dominated by the 1600 px hero;
- production cold mobile homepage: approximately 52 KB transferred, using the 720 px hero;
- homepage initial video transfer: `0`;
- animatics initial video transfer: `0`;
- storyboard, visual and animatic imagery: lazy loaded;
- media: metadata-only or none until use.

These measurements describe initial experience, not the approximately 200 MB complete on-demand archive.

## Accessibility

- document language, main landmark, heading order and skip link: PASS;
- visible focus and keyboard-accessible navigation: PASS;
- reader controls expose current state with `aria-pressed`: PASS;
- mobile menu exposes expanded state and remains touch operable: PASS;
- storyboard viewer supports previous/next and Escape: PASS;
- native video controls support keyboard play/pause/seek: PASS;
- alt text, contrast and reduced-motion handling: PASS.

## Documents, Provenance and SEO

Curated document QA covered project overview, Adaptation Bible, Character Voice Bible, Production Bible, Director Vision, P3/P4/P5 results and the full-series animatic result. TOCs, anchors, tables/code where present, frozen GitHub source links, archive return and previous/next navigation work.

The Project and Provenance pages present V1, V2, P3, P4, P5 and Web as the public milestone hierarchy. Runtime repair detail remains secondary. Robots, sitemap, canonical and Open Graph metadata resolve to `https://conanxin.github.io/classic-to-drama-engine/` with the correct base path.

## Issue Closeout

- issues found: `7`
- S0: `0`
- S1: `1 fixed and live verified`
- S2: `5 fixed and live verified`
- S3: `1 recovered; audit hardened`
- unresolved product issues: `0`

The workflow emitted a nonblocking runner annotation that the official actions' Node 20 runtime is deprecated and was forced to Node 24. Build and deploy succeeded; this is an upstream maintenance notice, not a live product defect.

## Protected Inputs and Pause Boundary

- V2 modified: `0`
- P3 modified: `0`
- P4 modified: `0`
- P5 modified: `0`
- Runtime modified: `0`
- P6 status: `PAUSED_BY_USER`
- P6 actions / research / outreach / payments: `0`

remaining_known_issues: `none affecting site use or acceptance`
