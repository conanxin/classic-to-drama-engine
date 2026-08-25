# P8 Comic Rendering Handoff

Status: `READY_AFTER_P7B_ONLY`

P8 may replace technical/animatic-derived visual authorities with publication-grade comic panels, but it must not re-derive the story or alter the P7B narrative manifest.

## Machine inputs

- `P7B_EPISODE_MANIFEST.json` — episode/scene order, cast states, conflict, selected exact dialogue, source bindings and route chain.
- `P7B_PANEL_MANIFEST.json` — 643 ordered panel placements with panel type, ratio, shot, blocking, caption, dialogue, alt, continuity and visual authority.
- `P7B_CHARACTER_REGISTRY.json` — stable base identities and disguise/source labels.
- `P7B_PROP_VISUAL_LEDGER.json` — recognition/weapon/door/arrow continuity.
- `P7B_NEW_PANEL_GENERATION_QUEUE.json` — non-blocking scenes that most benefit from a high-fidelity upgrade.
- P4 Look Bible, character state/costume matrices, standing sets and color script.
- P3 EP26–28 action previs for all 44 battle beats.

## Required render receipt per panel

P8 output must preserve:

- `panel_id`, `episode`, `scene_id`, `sequence`, `shot_id`;
- base character IDs and scene identity states;
- costume, scar, injury, prop custody, set state and light state;
- aspect ratio and mobile-safe composition;
- clean artwork with no Chinese dialogue/caption/speaker text baked into pixels;
- prompt/spec, source references, generator/artist version, output path, bytes, SHA-256 and approval status.

## Replacement rule

Only `visual` may be replaced. HTML captions, exact-source bubbles, scene order, source layer and navigation remain authoritative. A P8 asset is accepted only when it passes character identity, prop/state continuity, spoiler, mobile crop, text-free image and publication-allowlist checks.

## Priority order

1. Recognition chain: Argos, scar, bow/axes, bed, Laertes/land, weapons lowering.
2. EP26–28 action geography and custody.
3. Principal performance close-ups.
4. Mythic/VFX climaxes.
5. Remaining atmosphere/transition upgrades.

P8 is a suggested future phase. It is not authorized or executed by P7B.
