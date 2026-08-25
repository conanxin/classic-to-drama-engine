# P7B Graphic Novel Script Bible

Status: `FROZEN_P7B_GRAPHIC_NOVEL_SYSTEM`

Authorization: `USER_AUTHORIZED_WITHOUT_REAL_READER_EVIDENCE`

Real-reader validation: `NOT_CLAIMED`

## Product definition

P7B is the complete 30-episode illustrated-screenplay reading layer for 《归途：奥德修斯》. It sits between screenplay, graphic novel, technical storyboard and web visual narrative. It makes the story readable to a general audience while preserving the complete V2 screenplay beside it.

The product has two equal routes:

- Script Mode: `/episodes/NN/`
- Graphic Mode: `/episodes/NN/graphic/`

Graphic Mode never overwrites, summarizes away or silently edits Script Mode.

## Reader promise

Each scene answers, in this order:

1. **WHERE** — one location/time line and a visual anchor.
2. **WHO** — a glance-level cast strip, with context/details only on demand.
3. **WHAT IS AT STAKE** — the frozen scene function/goal.
4. **WHAT HAPPENS** — a 3–6 panel sequence in P3 shot order.
5. **WHAT CHANGED** — the scene consequence.
6. **WHAT THE SOURCE SAYS** — the complete expandable V2 scene.

This hierarchy prevents character, relationship, prop and production metadata from competing at equal visual weight.

## Formal story movements

The `/graphic/` directory uses the five frozen movements in `adaptation/odyssey_m1_v1/episode_architecture.json`:

1. EP01–04 — 伊萨卡失序与出航.
2. EP05–08 — 脱离停滞与重新获得名字.
3. EP09–15 — 漂流自述：聪明、骄傲与损失.
4. EP16–24 — 返乡伪装、忠诚测试与判断准备.
5. EP25–30 — 弓、清算、识别与共同体归位.

No alternate arc map is invented for the website.

## Episode template

Every episode contains:

- distinct cover visual and episode palette;
- short spoiler-safe `Previously On` (EP01 uses world entry);
- story movement and core conflict;
- progressive cast recognition;
- optional relationship context;
- five complete graphic scenes;
- an exact-source/full-source boundary;
- graphic end hook;
- working Graphic→Graphic previous/next links;
- Script Mode switch;
- per-episode and series progress;
- local-only Continue Reading state.

## Character recognition

P7A’s sixteen detailed entries remain byte-frozen. P7B adds context-only registry entries for every remaining credited/day/group source label so that 100% of the 76 source cast labels resolve to stable IDs. Disguises map to the base identity plus a scene state:

- `奥德修斯/乞丐` → `odysseus` + `乞丐` state;
- all `雅典娜/*` labels → `athena` + current disguise state.

The UI keeps the P7C progression:

- GLANCE: name, short role, identity color.
- CONTEXT: current scene, faction, relation/state.
- DETAIL: P7A anchor where available; P7B context-only note otherwise.

Reader knowledge and character knowledge remain separate. Athena and Odysseus visual states cannot reveal identity earlier than the screenplay.

## Exact-source text policy

- V2 Markdown is the only dialogue authority.
- Selected bubble text must be byte-normalized exact V2 dialogue.
- EP01/19/27 may reuse their frozen P7A reduced narrative and relation guidance.
- Other episodes use exact V2 action excerpts and frozen episode/scene-card statements.
- The full scene source is always recoverable from `scripts/odyssey_m1_v2/episodes/EPxx.md` and displayed in the reader.
- No image carries generated Chinese dialogue, captions, speaker names or narration.

## Visual system

Visual priority is:

1. P4 approved high-fidelity exact-shot art for cover, recognition and climax.
2. P4 single-frame technical storyboard derivatives.
3. P5 animatic-card derivatives where P4 did not board the shot.
4. P4 color key for cover identity where no high-fidelity episode hero exists.

All derivative crops retain source path, SHA-256 through the publication allowlist, authority class and shot/frame identity. P7B generates no new story art; the non-blocking queue is exclusively a P8 upgrade list.

## Core continuity locks

- Odysseus: returned self → beggar state → scar/bow/bed verification → restored public identity.
- Athena: divine/human disguises track reader and character knowledge separately.
- Recognition chain: Argos → scar → bow/axes → bed → Laertes/land → community.
- EP26–28: all 44 P3 action-previs beat IDs remain bound; door geography, arrows and weapon custody cannot be reordered for visual excitement.
- Prop ledger binds bow, axes, scar, bed, ship, weapons, weaving, doors and arrows to source scenes.
- The visual thesis remains: **Home Must Recognize the Person Who Returns.**

## Performance and publication

- 30 pages are statically generated; each loads only its episode media.
- Responsive derivatives, `srcset`, lazy loading and route splitting are mandatory.
- First cover and first-scene anchor may be eager; later panels are lazy.
- All image, link, progress, assist and source-layer controls remain keyboard/touch accessible.
- Search records explicitly identify `图文剧本`, distinct from `剧本`.
- Canonical routes use the GitHub Pages subpath.

## Evidence boundary

The rollout is authorized directly by the user after P7C. It is supported by source binding, P3/P4/P5 continuity, deterministic verification, browser QA and internal AI/heuristic review. It does not assert that real readers preferred, completed, remembered or understood Graphic Mode better.
