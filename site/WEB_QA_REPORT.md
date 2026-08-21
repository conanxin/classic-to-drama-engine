# CTDE Web Archive QA Report

Status: **PASS_LOCAL_PRODUCTION_AND_BROWSER_QA**

Baseline: `478fd10f5b115c70f7b4b8ce5146ae2b6c6d37e5`

## Build and publication verification

- Astro check: 31 files, 0 errors, 0 warnings, 0 hints.
- Static routes: 94.
- Pagefind: 93 indexed pages, 8,115 indexed words, language `zh-cn`.
- Deterministic CJK index: 61 records covering 30 episodes, 18 curated documents, four principals and nine world families.
- Episodes / scenes: 30 / 150.
- Curated documents: 18.
- Storyboard board pages: 173, plus 30 episode contact sheets.
- Public media allowlist: 254 images and 32 videos, 286 total.
- Mobile image derivations: 254 WebP files, 7,164,612 bytes.
- Internal reference check: PASS.
- Duplicate route / HTML ID check: PASS.
- Rejected P4 target promotion: 0.
- Forbidden absolute path publication: 0.
- Frozen V2/P3/P4/P5/Runtime modifications: 0.

## Browser method

The in-app Browser was attempted first. Its available `26.818.31338` client requested a missing `26.818.32112` service, so the connection could not be established. The Playwright CLI wrapper also carried Windows line endings in WSL, and headed CLI mode could not return control without a display server. QA therefore used the bundled Playwright API with a real local Chromium executable in headless mode. This was a tool-runtime fallback only; all checks used the production static server at the GitHub Pages base path.

## Desktop route matrix

At 1440 × 1000, each route returned HTTP 200, had one H1, no viewport overflow and no image missing `alt`:

`/`, `/episodes/`, `/episodes/01/`, `/episodes/30/`, `/characters/`, `/visual/`, `/storyboards/`, `/storyboards/27/`, `/watch/`, `/production/`, `/project/`.

## Mobile route matrix

At 390 × 844, each route returned HTTP 200 with zero page-level horizontal overflow and a functional responsive menu:

`/`, `/episodes/`, `/episodes/01/`, `/characters/`, `/visual/`, `/storyboards/27/`, `/watch/`, `/production/`, `/project/`.

Long tables in Production Complexity and P3 Final Result remain keyboard-scrollable within 350px containers without widening the page. Long SHA/status tokens wrap. The first mobile image request resolves to the 720px WebP derivative.

## Script reader

The build verifier reads EP01, EP10, EP19, EP25, EP27, EP29 and EP30 final HTML and requires each episode title, first scene heading, first action and final-scene dialogue probe. All passed.

EP01 browser structure: five scene headings, 32 action blocks, 42 character cues, 40 dialogue blocks and one next-episode link. Font size, reading width and light/dark state persist through `localStorage` and a page reload.

## Search

Final query recall, before the 30-result display cap:

| Query | Results |
|---|---:|
| 奥德修斯 | 44 |
| 佩涅洛佩 | 22 |
| 忒勒马科斯 | 24 |
| 独眼巨人 | 3 |
| 弓 | 19 |
| 床 | 18 |
| recognition | 22 |
| 身份 | 20 |

Pagefind's initial Chinese tokenization returned only one Odysseus result. A deterministic exact CJK substring index was added and merged with Pagefind ranking. Final searches produced no browser console errors.

## Media and interaction

- P5 pitch teaser metadata duration: 90 seconds.
- Play: PASS; timeline progressed.
- Pause: PASS.
- Seek: PASS.
- Video preload: metadata only.
- EP27 technical-board lightbox: opens the allowlisted full-resolution board and closes correctly.
- Storyboard and visual images: lazy except above-fold priority media.

## Accessibility

- `lang="zh-CN"`, semantic header/nav/main/footer and one H1 per audited page: PASS.
- Heading-level leap check: PASS.
- Skip link is the first keyboard focus target and has a visible 2px outline: PASS.
- Image alt text: PASS.
- Native video controls: PASS.
- Reduced-motion media query reduces transition and animation durations to 0.01ms: PASS.
- Table scroll regions are keyboard focusable and named: PASS.

## Concept-to-browser visual review

The four accepted concepts are preserved under `design/concepts/`. They were compared in the same review pass with the latest homepage, reader, visual archive and mobile-reader screenshots.

1. **Palette** — browser output keeps the concept's ink black, warm paper, worked-earth brown and restrained terracotta; no invented brand color was introduced.
2. **Typography** — both use large Song-style Chinese display type and compact sans-serif metadata. Browser line-height is slightly more generous for sustained reading.
3. **Homepage geometry** — the split text/image hero, compact actions and approved S1 visual match. The browser gives the source image slightly more width and moves the numerical rail immediately below the fold.
4. **Reader hierarchy** — episode rail, screenplay column and contextual rail match on desktop; mobile becomes one column. The browser uses real V2 titles and cue counts instead of concept placeholders.
5. **Visual archive treatment** — full-width approved image bands, thin rules and sparse captions match. The browser adds an explicit rejected-target/technical-board boundary above the first band.
6. **Controls** — the concept's custom selector shells became simpler native buttons with stronger keyboard focus. This is an intentional accessibility deviation, not an unfinished state.
7. **Above-fold copy** — the concept used a compact descriptive label; the browser uses the final thesis line “关于归乡、身份与被重新认出的故事” and authoritative EP01 title “没有父亲的家.” The visual archive uses “风留下方向，物件留下证词” to explain the archive before imagery.
8. **Theme** — the mobile concept showed the optional paper mode; the browser screenshot used the default ink mode. Both modes were tested and persist locally.

Material repairs made after comparison: Pagefind runtime import, Chinese recall, mobile production overflow, mobile document token/table overflow, scoped reader control styling, and responsive image delivery.

## Result

Local production build, content integrity, browser behavior, visual fidelity, mobile layout, accessibility and media QA: **PASS**.

Online GitHub Pages verification is recorded separately in `WEB_PUBLICATION_FINAL_RESULT.md` after deployment.
