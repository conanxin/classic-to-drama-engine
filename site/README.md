# CTDE Public Web Archive

Static public viewer for **《归途：奥德修斯》**. It reads the frozen V2/P3/P4/P5 artifacts at build time and publishes a curated screenplay, visual and production archive under `/classic-to-drama-engine/`.

```bash
npm ci
npm run verify
npm run check
npm run build
npm run preview
```

The source of truth remains the root project artifacts. `src/generated/`, `public/media/` and `dist/` are reproducible build products and are not committed.

Publication status and browser evidence are recorded in `WEB_QA_REPORT.md`. P6 remains paused.
