# P7B Web QA Report

status: `PASS_LOCAL_PRODUCTION_BROWSER_QA`

## Build and route evidence

- Astro production pages generated: `126`
- Graphic routes generated: `30 / 30`
- Script routes preserved: `30 / 30`
- Pagefind indexed pages: `125`
- output files: `2,974`
- production artifact size: approximately `345 MiB` (archive total, not initial-page transfer)
- broken publication references: `0`
- rejected P4 images promoted: `0`
- local-path/privacy disclosures: `0`

`npm run build` completed with Astro check at 0 errors, 0 warnings and 0 hints. Source and built-output P7B verifiers passed independently.

## Browser matrix

Playwright Chromium was used because the in-app browser was unavailable under the current administrator policy. Production output was served under the real GitHub Pages base path: `/classic-to-drama-engine/`.

Stratified episodes checked at 1440 × 900 and 390 × 844:

`EP01`, `EP05`, `EP10`, `EP15`, `EP19`, `EP23`, `EP27`, `EP28`, `EP29`, `EP30`.

Every sample produced:

- exactly 5 rendered scenes;
- complete source layer for all 5 scenes;
- 0 broken images;
- 0 horizontal overflow;
- readable dialogue width on mobile;
- correct Graphic next route and Script-mode route.

## Interaction checks

| Interaction | Evidence | Result |
| --- | --- | --- |
| Character assist | Tap/click opened the contextual identity layer; native summary received keyboard focus and toggled with Enter. | PASS |
| Re-orient control | “现在有哪些人？” opened current cast, target and relationship information without leaving the scene. | PASS |
| Reading progress | EP27 moved from scene 01 to scene 03 and updated 20% → 60%. | PASS |
| Continue Reading | Local state restored EP27 scene 03 at the exact saved scroll position. | PASS |
| Graphic chain | EP01–EP29 link to the next Graphic episode; EP30 returns to the complete directory. | PASS |
| Dual mode | Every Graphic sample linked back to the same episode's Script route. | PASS |
| Search | “奥德修斯” returned 73 indexed matches with meaningful Graphic results and valid subpath links. | PASS |

## Initial-load observation

A fresh browser session opened EP10, the heaviest sampled page by panel count:

- declared images: `34`
- images loaded in the first viewport: `9`
- lazy images: `28`
- total resource requests: `12`
- measured transfer: approximately `218 KB`
- JavaScript resource requests: `0` (page behavior is inline and route-local)

This confirms that the 345 MiB static archive is not downloaded as an episode's initial payload.

## Design-system comparison

Accepted P7A references:

- `graphic-script/odyssey_m1_p7a/design/GRAPHIC_MODE_CONCEPT_DESKTOP.png`
- `graphic-script/odyssey_m1_p7a/design/GRAPHIC_MODE_CONCEPT_MOBILE.png`

Actual browser captures were compared at native viewport size. Five required comparison points passed:

1. typography — large Chinese display serif remains paired with compact archival labels and readable body text;
2. palette — warm ink, bone and episode accent colors match the accepted cinematic system;
3. navigation — Script/Graphic distinction is immediate and the global archive header remains quieter than story content;
4. media treatment — approved high-fidelity covers anchor episodes while technical sources become clean, cropped story panels;
5. hierarchy and responsive behavior — desktop uses asymmetric editorial grids; mobile becomes a single narrative stream without shrinking panel text.

The above-the-fold copy intentionally changes from the three-episode prototype language to the episode-specific P7B story stage and full-series progress. This is a product-state update, not an unapproved redesign. The P7B reader uses a taller cover than the concept mockup so each episode can establish title, conflict, dual-mode choice and one approved visual before entering the dense sequence.

No material visual deviation remains. The rendered system meets agency-signoff quality for this static Graphic Novel Script edition.

## Accessibility and mobile

- semantic headings, figures, blockquotes and native details are retained;
- every visual has contextual alt text;
- dialogue is real HTML text, never baked into artwork;
- character assistance is keyboard and touch accessible;
- focus remains visible through the existing site system;
- mobile panel grids collapse to one column;
- the sticky scene progress bar uses a small portion of the viewport and does not cover dialogue.

## Deployment verification

The deployment run and public crawl are recorded in `P7B_FINAL_RESULT.md` after the authoritative commit is deployed. Local production QA is complete.
