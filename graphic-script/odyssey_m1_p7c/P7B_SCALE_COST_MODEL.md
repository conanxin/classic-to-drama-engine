# P7B Scale Cost Model

status: `ESTIMATE_ONLY_NO_ROLLOUT`
currency: effort and payload units, not vendor pricing

## Scope

The full series contains 30 episodes and 150 scenes. P7A/P7C cover 3 episodes and 15 scenes, leaving 27 episodes and 135 scene adaptations. The P7A placement model targets 260–330 published image placements across the season; the prototypes currently use 18 placements.

## Reuse and new visual demand

| item | planning range |
|---|---:|
| remaining placements | 242–312 |
| reuse of approved hero/board/set/identity/prop assets | 55–70% |
| reused or recropped placements | 135–215 |
| new or deliberately recomposed visual needs | 85–140 |
| high-load episodes requiring dense spatial coverage | 10–12 |
| performance-led episodes requiring fewer, larger images | 6–8 |

## Editorial effort

| work | unit assumption | total |
|---|---:|---:|
| source-bound scene reduction | 1.5–2.5 hours × 135 | 203–338 hours |
| character/relationship/spoiler overlays | 0.4–0.8 hours × 135 | 54–108 hours |
| visual selection/crop/authority QA | 0.5–1.0 hours × 242–312 | 121–312 hours |
| mobile/desktop/content QA | 1.5–3 hours × 27 | 41–81 hours |
| batch continuity and anti-drift review | 6 batches × 6–10 hours | 36–60 hours |
| planning total | — | about 455–899 hours |

These are internal planning assumptions, not paid-production quotes. Reader evidence should determine whether all layers deserve this investment.

## Payload and build impact

With mobile WebP in the 120–300 KB range and only cover eager-loaded, a typical episode should transfer about 1–2.5 MB after a full scroll while initial HTML/CSS/JS remains light. A 30-episode Graphic archive likely adds 50–100 MB of published derivatives. Route splitting prevents a reader from loading the full-season asset set.

## QA cost controls

Use five-episode batches; freeze alias/spoiler state, scene/prop continuity and approved-asset identities per batch; run exact-source dialogue checks, missing-route checks, mobile overflow checks and payload checks before proceeding. Do not begin this work while `P7B_ROLLOUT_DECISION` is awaiting evidence.
