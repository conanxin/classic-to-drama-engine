# P10B Web Release QA Report

status: `PASS_P10B_WEB_RELEASE_QA`

## Production build

- `npm run check`: PASS — Astro 54 files, 0 errors, 0 warnings, 0 hints
- `npm run verify`: PASS — P7 through P10 source and publication verification
- `npm run build`: PASS — 133 static pages, 132 Pagefind documents, final dist verification PASS
- P10 assets in the public allowlist: reader sample, five cover sets, three promotional images and checksum documents only

## Local browser QA

- viewports: 1440 × 900 and 390 × 844
- route/view combinations: 18 / 18 PASS
- direct public-resource checks: 3 / 3 PASS
- broken images: 0
- missing image alt attributes: 0
- horizontal overflow: 0
- root-relative base-path defects: 0
- canonical defects: 0
- visual inspection: homepage, /read/, /publication/ and /publication/verify/ PASS on both viewports

## Reader sample QA

- pages: 20
- content: frozen P9 Volume I pages 1–20, including complete EP01
- SHA-256: `1f6270d7bb1420df3833bccf38a3f17a8310a605b7c13742fe3f02a8ce7bd725`
- visual inspection: cover and representative interior page PASS

## Live QA

- deployment commit: `cdc87228e2c3dbc655203878137bbf4c4890126a`
- Pages workflow run: `33129982947`
- sitemap routes checked: 133
- internal/public assets checked: 2893
- public URL: https://conanxin.github.io/classic-to-drama-engine/
- reader entry, publication center, verification page, sample PDF and canonical GitHub Release links: PASS
