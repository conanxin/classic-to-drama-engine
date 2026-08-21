# CTDE Web Archive Design System

## Accepted concept evidence

- `design/concepts/homepage-desktop.png` — 1504×1055 desktop homepage and episode rail.
- `design/concepts/screenplay-reader-desktop.png` — 1528×1024 desktop screenplay reader.
- `design/concepts/visual-archive-desktop.png` — 1504×1015 visual/storyboard archive.
- `design/concepts/screenplay-reader-mobile.png` — 853×1843 mobile screenplay reader.

The concepts were produced from the frozen P4 approved occupied-hall frame. They are implementation specifications, not publishable story art.

## Direction

`cinematic editorial archive`: reading first, ink-dark global chrome, warm material typography, approved imagery without a tint wash, sharp media rectangles, hairline rules, open lists and rails rather than cards. No fantasy ornament, glass, neon, gradients, pills or bento layouts.

## Tokens

- Ink: `#141414`; deep ink: `#0d0e0e`; raised ink: `#1a1917`.
- Warm paper: `#ded6c2`; secondary paper: `#c8bda0`; muted text: `#9f9684`.
- Worked earth: `#756344`; terracotta: `#a05f55`; focus: `#d99a72`.
- Light reader: paper `#f0eadc`, ink `#191714`, muted `#6d6253`.
- Rules: 1px, warm earth at 55% opacity. Corners are square; shadows are avoided.

## Typography

- Display and screenplay: `Songti SC`, `STSong`, `Noto Serif CJK SC`, `Source Han Serif SC`, serif.
- UI: `PingFang SC`, `Microsoft YaHei`, `Noto Sans CJK SC`, system-ui, sans-serif.
- H1 desktop: clamp 3.4–6.8rem; mobile 2.45–3.7rem. Body: 1.05–1.2rem, screenplay 1.1–1.36rem. UI chrome: 0.78–0.94rem.

## Container and component model

- Global max width: 1600px. Reading measure: 44rem comfortable / 58rem wide.
- Quiet sticky header; editorial rails; numbered rows; image bands; one media stage; document TOC; technical tables.
- Buttons are rectangular text controls. Arrow icons use production SVG paths, not text glyphs.
- Desktop reader: episode rail / article / metadata. Mobile: one column, menu drawer, metadata after title.

## Copy lock — homepage first viewport

Only: `《归途：奥德修斯》`, `Classic-to-Drama Engine`, `30集短剧改编`, `关于归乡、身份与被重新认出的故事。`, `开始阅读`, `观看 Previs`, `30 Episodes`, `150 Scenes`, `~211 min`, and the seven user-specified navigation labels. No eyebrow, badge or additional claim.

## Media treatment

P4 approved image color remains unchanged. Hero uses crop/edge positioning only, never a tint overlay. Technical boards always carry a visible `TECHNICAL STORYBOARD` label. Videos use native controls and `preload="metadata"` or `none`.

## Motion and access

150–220ms opacity/underline transitions only. `prefers-reduced-motion` disables reveals and smooth scrolling. Every interactive element receives a 2px visible focus outline. Minimum mobile touch target is 44px.
