# P4 Visual Capability Audit

Status: `PASS_LOCAL_VISUAL_EXECUTION_CAPABILITY`

Baseline verified on 2026-08-21 (Asia/Shanghai): repository `conanxin/classic-to-drama-engine`, local `HEAD` and remote `origin/main` both `0c4a403864d9ea89afabceed3c7be7d5819f86c8`, clean Linux-native `ext4` worktree. P3 artifact manifest SHA-256 is `bd1f79516b567f4c5aa9760662e9d0c76d2cb17f745a7550488138c730353bf4`; P3 final result SHA-256 is `637a18f78f962120d36aa948a781c486e2b69e0b754023138a9d3427deaf880a`.

## Available routes

| Capability | Route | P4 use | Classification |
|---|---|---|---|
| Native image generation/edit | Codex integrated ImageGen | Cast-neutral character sheets, set/creature anchors, hero lookdev frames | High-fidelity generated bitmap |
| Vector drawing | Deterministic project SVG generator | 711 P3-bound technical frames, floor/elevation/prop diagrams | Technical visual, never labeled concept art |
| Raster composition | Python 3.12 + Pillow 12.1.1 + OpenCV 4.13 | Boards, labels, color keys, contact sheets, review derivatives | Deterministic export |
| Video/audio assembly | ffmpeg/ffprobe | 60–90 second teaser previs, original abstract sound bed | Technical previs |
| 3D / DCC | Blender absent | Not required; P3 geometry remains authoritative | Not available |
| CLI vector render | Inkscape/ImageMagick/librsvg absent | Pillow/OpenCV renderer is the fallback | Not required |

No external account, paid API, credential, copyrighted music, real-person likeness, or hidden network image source is required. The Creative Production board direct UI route is not exposed in this task runtime, so the durable review surface is the versioned project manifest plus single-image assets, contact sheets and a neutral local review page. No completion claim relies on board UI state.

## Fidelity labels

- `TECHNICAL_SVG`: composition/blocking/continuity proof, intentionally schematic.
- `TECHNICAL_BOARD_PNG`: labeled raster board composed from approved technical frames.
- `COLOR_KEY`: deterministic palette/progression tile, not a narrative frame.
- `HIGH_FIDELITY_GENERATED`: integrated ImageGen output inspected against manifest constraints.
- `PREVIS_COMPOSITE`: timed editorial proof assembled from approved P4 assets.

Final acceptance is unavailable until both technical coverage and high-fidelity review pass.
