import { createHash } from 'node:crypto';
import { mkdir, readFile, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const outDir = path.resolve(here, '..');
const repoRoot = path.resolve(outDir, '..', '..');
const readJson = async (relative) => JSON.parse(await readFile(path.join(repoRoot, relative), 'utf8'));
const writeJson = async (name, value) => writeFile(path.join(outDir, name), `${JSON.stringify(value, null, 2)}\n`);
const writeText = async (name, value) => writeFile(path.join(outDir, name), `${value.trim()}\n`);
const sha256 = (value) => createHash('sha256').update(value).digest('hex');

await mkdir(outDir, { recursive: true });
await mkdir(path.join(outDir, 'candidate', 'gold-standard'), { recursive: true });
await mkdir(path.join(outDir, 'master'), { recursive: true });
await mkdir(path.join(outDir, 'web'), { recursive: true });
await mkdir(path.join(outDir, 'rejected'), { recursive: true });
await mkdir(path.join(outDir, 'contact-sheets'), { recursive: true });

const panels = await readJson('graphic-script/odyssey_m1_p7b/P7B_PANEL_MANIFEST.json');
const episodes = await readJson('graphic-script/odyssey_m1_p7b/P7B_EPISODE_MANIFEST.json');
const props = await readJson('graphic-script/odyssey_m1_p7b/P7B_PROP_VISUAL_LEDGER.json');
const p7bCharacters = await readJson('graphic-script/odyssey_m1_p7b/P7B_CHARACTER_REGISTRY.json');
const queue = await readJson('graphic-script/odyssey_m1_p7b/P7B_NEW_PANEL_GENERATION_QUEUE.json');

if (panels.counts.panel_placements !== 643 || panels.panels.length !== 643) throw new Error('P7B 643-slot authority mismatch');
if (episodes.counts.episodes !== 30 || episodes.counts.scenes !== 150) throw new Error('P7B episode authority mismatch');
if (queue.queue_count !== 104) throw new Error('P7B upgrade seed mismatch');

const principalLocks = [
  {
    character_id: 'odysseus', display_name: '奥德修斯', tier: 'PRINCIPAL_HARD_LOCK', identity: 'P4 selected V02',
    reference: 'visual-development/odyssey_m1_p4/high_fidelity/characters/P4-CHAR-ODY-IDENTITY-V02.png',
    face_anchors: ['compact weathered face', 'asymmetric brow', 'deep-set brown eyes', 'dark curls with salt-grey temples', 'irregular short beard'],
    silhouette: ['broad back', 'rope forearms', 'compact force', 'sloped right shoulder'],
    costume_states: ['normal', 'storm-wrecked', 'returned', 'beggar-disguise', 'revealed', 'battle', 'restored'],
    hard_continuity: ['right outer thigh scar only', 'no early scar reveal', 'same face through disguise', 'no heroic glamour drift']
  },
  {
    character_id: 'penelope', display_name: '佩涅洛佩', tier: 'PRINCIPAL_HARD_LOCK', identity: 'P4 selected V01',
    reference: 'visual-development/odyssey_m1_p4/high_fidelity/characters/P4-CHAR-PEN-IDENTITY-V01.png',
    face_anchors: ['mature Mediterranean face', 'high asymmetric brow', 'controlled dark coils', 'fatigue without fragility'],
    silhouette: ['vertical authority', 'key-and-cloth waist habit', 'deliberate stillness'],
    costume_states: ['household-rule', 'mourning-pressure', 'contest', 'recognition', 'restoration'],
    hard_continuity: ['active observer', 'calculating hands and gaze', 'never passive beauty treatment']
  },
  {
    character_id: 'telemachus', display_name: '忒勒马科斯', tier: 'PRINCIPAL_HARD_LOCK', identity: 'P4 selected V01',
    reference: 'visual-development/odyssey_m1_p4/high_fidelity/characters/P4-CHAR-TEL-IDENTITY-V01.png',
    face_anchors: ['young open face', 'dense dark curls', 'long neck', 'clean jaw'],
    silhouette: ['left-foot lead', 'initially uncertain shoulders', 'gradual weapon confidence'],
    costume_states: ['boy-household', 'traveler', 'returning-heir', 'battle', 'civic-authority'],
    hard_continuity: ['growth through posture and fit', 'no sudden adult-warrior jump', 'same young face']
  },
  {
    character_id: 'athena', display_name: '雅典娜', tier: 'PRINCIPAL_HARD_LOCK', identity: 'P4 selected V01',
    reference: 'visual-development/odyssey_m1_p4/high_fidelity/characters/P4-CHAR-ATH-IDENTITY-V01.png',
    face_anchors: ['same dark-haired woman across states', 'steady frontal gaze', 'owl pin'],
    silhouette: ['forward shoulder', 'half-turn', 'wrong-timed shadow'],
    costume_states: ['human-disguise', 'divine', 'threshold-manifestation'],
    hard_continuity: ['divinity through light posture gaze and environment', 'no cheap glow', 'reader knowledge never exceeds scene authority']
  }
];

const supportingLocks = [
  ['eumaeus', '欧迈俄斯', 'sun-browned older herdsman; practical layered wool; steady lowered center of gravity'],
  ['eurycleia', '欧律克勒娅', 'elder household authority; brown head cloth; working hands; attentive eyes'],
  ['antinous', '安提诺俄斯', 'confident suitor leader; wine-rust accent; entitlement expressed through occupied space'],
  ['eurymachus', '欧律马科斯', 'smooth calculating suitor; controlled dress; lateral gaze'],
  ['amphinomus', '安菲诺摩斯', 'labor shoulder line; hesitation at shared work objects'],
  ['poseidon', '波塞冬', 'durable environmental pressure; human figure only where scene authority permits'],
  ['polyphemus', '波吕斐摩斯', 'single-eyed practical giant sharing the same stone-and-wool world; never generic game monster'],
  ['alcinous', '阿尔喀诺俄斯', 'Phaeacian civic host; sea-glass and redress court language'],
  ['nausicaa', '瑙西卡', 'young Phaeacian authority; poised movement; practical court linen'],
  ['laertes', '拉厄耳忒斯', 'elder orchard body; soil-marked hands; land memory rather than royal display']
].map(([character_id, display_name, visual_lock]) => ({ character_id, display_name, tier: 'SUPPORTING_LOCK', visual_lock }));

await writeJson('P8_CHARACTER_VISUAL_LOCK.json', {
  schema_version: '1.0.0', artifact_class: 'P8_CHARACTER_VISUAL_LOCK', status: 'FROZEN_FOR_RENDERING',
  principal_locks: principalLocks, supporting_locks: supportingLocks,
  source_character_count: p7bCharacters.characters.length,
  universal_rules: ['no face drift', 'no modern costume leakage', 'no baked text', 'state transitions must be episode-causal']
});

await writeJson('P8_SET_VISUAL_LOCK.json', {
  schema_version: '1.0.0', artifact_class: 'P8_SET_VISUAL_LOCK', status: 'FROZEN_FOR_RENDERING',
  standing_sets: [
    { set_id: 'S1', name: 'Ithaca Hall', reference: 'visual-development/odyssey_m1_p4/high_fidelity/sets/P4-SET-S1-ANCHOR-V01.png', geometry: ['16×22m hall', 'four fixed columns', 'main entrance opposite dais', 'left stair and armory return', 'right hearth', 'courtyard relationship'], states: ['S1-A CLEAN OCCUPIED','S1-B CONTEST','S1-C FIRST BLOOD','S1-D FULL BATTLE','S1-E AFTERMATH','S1-F RESTORED'] },
    { set_id: 'S2', name: 'Phaeacian Hall', reference: 'visual-development/odyssey_m1_p4/high_fidelity/sets/P4-SET-S2-ANCHOR-V01.png', geometry: ['bright civic sea-glass redress', 'same practical material family'] },
    { set_id: 'S3', name: 'Ship Deck', reference: 'visual-development/odyssey_m1_p4/high_fidelity/sets/P4-SET-S3-ANCHOR-V01.png', geometry: ['fixed mast', 'oar rails', 'deck hatches', 'working rigging'] },
    { set_id: 'S4', name: 'Eumaeus Farm', reference: 'visual-development/odyssey_m1_p4/high_fidelity/sets/P4-SET-S4-ANCHOR-V01.png', geometry: ['stone wall', 'pig pen', 'olive trees', 'coastal sightline', 'low working hut'] },
    { set_id: 'S5', name: 'Shore / Cave', reference: 'visual-development/odyssey_m1_p4/high_fidelity/sets/P4-SET-S5-ANCHOR-V01.png', geometry: ['rock mouth', 'shoreline', 'olive growth', 'practical baskets nets fire'] }
  ],
  hard_rules: ['architecture persists across episodes', 'redress and damage change state not floor plan', 'mobile crops retain spatial cause and effect']
});

await writeJson('P8_PROP_RENDER_LOCK.json', {
  schema_version: '1.0.0', artifact_class: 'P8_PROP_RENDER_LOCK', status: 'FROZEN_FOR_RENDERING',
  props: props.props.map((prop) => ({ ...prop, p8_rule: 'stable silhouette, custody and state change; render consequence legibly' })),
  hard_locks: {
    bow: 'dark seasoned olive/horn composite curve; stable grip and string geometry',
    axes: 'twelve matched bronze-headed axes; consistent aperture alignment',
    scar: 'Odysseus right outer thigh only',
    bed: 'living olive root passes through frame and floor; cannot be moved without cutting',
    arrows: 'EP26–28 begins with 12 usable arrows and reaches zero only at A28-010',
    doors: 'S1 thresholds and armory route follow P3 frozen geography'
  }
});

const goldIds = [
  'EP01-S01-PNL01','EP01-S02-PNL02','EP05-S05-PNL06','EP10-S02-PNL04','EP10-S04-PNL04',
  'EP13-S03-PNL04','EP16-S04-PNL02','EP19-S02-PNL04','EP19-S04-PNL02','EP25-S01-PNL02',
  'EP25-S05-PNL04','EP27-S01-PNL03','EP27-S03-PNL03','EP28-S02-PNL04','EP28-S05-PNL03',
  'EP29-S04-PNL02','EP29-S05-PNL02','EP30-S02-PNL02','EP30-S04-PNL04','EP30-S05-PNL04'
];
const panelById = new Map(panels.panels.map((panel) => [panel.panel_id, panel]));
const goldSpecs = goldIds.map((panelId, index) => {
  const panel = panelById.get(panelId);
  if (!panel) throw new Error(`Missing Gold Standard panel ${panelId}`);
  const tier = /EP29|EP30|EP27|EP28|EP10|EP19/.test(panelId) ? 'TIER_A_HERO_FINAL' : 'TIER_B_NARRATIVE_FINAL';
  return {
    gold_order: index + 1, panel_id: panelId, episode: panel.episode, scene_id: panel.scene_id, tier,
    panel_type: panel.panel_type, ratio: panel.ratio, shot_id: panel.shot_id, subject: panel.subject,
    visible_action: panel.visible_action, narrative_context: panel.caption, dialogue: panel.dialogue,
    p7b_visual: panel.visual, render_version: 'V01', render_status: panel.visual.source_kind === 'P4_HIGH_FIDELITY' ? 'EXISTING_HIGH_FIDELITY_AUDIT' : 'CANDIDATE_RENDER_REQUIRED',
    required_checks: ['identity','costume','set','prop','composition','mobile crop','spoiler','style','text contamination','panel function'],
    text_safe_zone: panel.ratio === '1:1' ? 'upper-left 22% or lower-third 18%, preserve central prop' : 'one lateral 25% negative-space band; never cover face, hands, weapon or consequence'
  };
});
await writeJson('P8_GOLD_STANDARD_RENDER_SPECS.json', { schema_version: '1.0.0', artifact_class: 'P8_GOLD_STANDARD_RENDER_SPECS', count: goldSpecs.length, specs: goldSpecs });

const acceptance = panels.panels.map((panel) => ({
  panel_id: panel.panel_id, episode: panel.episode, scene_id: panel.scene_id, sequence: panel.sequence,
  p7b_source_kind: panel.visual.source_kind, p7b_source_path: panel.visual.source_path,
  p8_quality_tier: panel.panel_type === 'CLIMAX' || /EP2[5-9]|EP30/.test(panel.episode) ? 'TIER_A_HERO_FINAL' : panel.panel_type === 'TRANSITION' || panel.panel_type === 'ENVIRONMENT' ? 'TIER_C_TRANSITION_FINAL' : 'TIER_B_NARRATIVE_FINAL',
  p8_status: 'P8_VISUAL_AUDIT_PENDING', final_visual_asset_id: null, master_path: null, web_path: null,
  audit: { identity: null, continuity: null, composition: null, artifact: null, spoiler: null, style: null, panel_function: null, text_contamination: null, crop_safety: null }
}));
await writeJson('P8_PANEL_ACCEPTANCE_LEDGER.json', { schema_version: '1.0.0', artifact_class: 'P8_PANEL_ACCEPTANCE_LEDGER', status: 'IN_PROGRESS', counts: { total: 643, pending: 643, accepted: 0 }, panels: acceptance });
await writeJson('P8_RENDER_MANIFEST.json', { schema_version: '1.0.0', artifact_class: 'P8_RENDER_MANIFEST', status: 'IN_PROGRESS', source_panel_manifest_sha256: sha256(await readFile(path.join(repoRoot, 'graphic-script/odyssey_m1_p7b/P7B_PANEL_MANIFEST.json'))), assets: [] });
await writeJson('P8_RENDER_RECEIPTS.json', { schema_version: '1.0.0', artifact_class: 'P8_RENDER_RECEIPTS', status: 'IN_PROGRESS', receipts: [] });
await writeJson('P8_REJECTION_REGISTER.json', { schema_version: '1.0.0', artifact_class: 'P8_REJECTION_REGISTER', status: 'ACTIVE', allowed_reasons: ['IDENTITY_DRIFT','COSTUME_DRIFT','PROP_ERROR','SET_ERROR','SCAR_ERROR','ANATOMY_ERROR','HAND_ERROR','EXTRA_LIMB','FACE_ARTIFACT','STYLE_DRIFT','LIGHTING_ERROR','WRONG_GEOGRAPHY','SPOILER','TEXT_IN_IMAGE','BAD_CROP','NARRATIVE_AMBIGUITY','DUPLICATE_COMPOSITION'], rejections: [] });

await writeText('P8_COMIC_VISUAL_BIBLE.md', `# P8 Comic Visual Bible

Status: FROZEN_FOR_GOLD_STANDARD

## Core proposition

P8 turns the 643 P7B narrative slots into sequential publication art. It changes only visual assets. Episode order, scene order, panel function, captions, exact-source dialogue, source layer and navigation remain frozen.

## Visual grammar

- Cinematic, mythic Mediterranean, editorial, textured dramatic naturalism.
- Tactile salt, repaired lime plaster, worked bronze, wool, linen, leather, olive wood and clay.
- Human performance and recognition take priority over spectacle.
- Variation follows the thirty-episode colour keys while remaining inside one visual grammar.
- No generic fantasy-game gloss, superhero grammar, anime drift, plastic skin, random film-still casting, overprocessed HDR or modern leakage.
- No text, letters, pseudo-writing, captions, names or speech baked into raster art.

## Sequential rules

Every scene is reviewed as a sequence: shot-size variation, screen direction, eye line, action continuity, emotional progression, repetition and page rhythm. Artwork reserves a text-safe zone without sacrificing face, hand, key prop or consequence. Desktop crops may be asymmetric; 390px mobile crops must keep the causal action readable.

## Quality tiers

- TIER A HERO FINAL: recognition, climax, cover and principal emotional turns.
- TIER B NARRATIVE FINAL: dialogue and action continuity.
- TIER C TRANSITION FINAL: environment, travel, prop and silent bridges.

All tiers are final publication art. Tiers differ in complexity, not completion.

## Acceptance

Each slot must be FINAL_COMIC_ACCEPTED or EXISTING_HIGH_FIDELITY_ACCEPTED after identity, continuity, composition, artifact, spoiler, style, function, text-contamination and crop-safety review. Raw technical storyboard and animatic frames cannot pass as final reader art.
`);

await writeText('P8_VISUAL_MOTIF_LEDGER.md', `# P8 Visual Motif Ledger

The series proposition is **Home Must Recognize the Person Who Returns**.

| Motif | First use | Recurrence grammar | Payoff |
|---|---|---|---|
| Threshold / door | EP01 occupied hall | Figures tested at edges; doors show custody and permission | EP29–30 home accepts person and civic order |
| Hand | EP01 cup custody | Hands take, withhold, test, clean and lower weapons | Bed knowledge and weapons-lowering |
| Scar | Kept latent until recognition chain | Right outer thigh; never decorative | Eurycleia recognition without public disclosure |
| Bow curve | Seeded before contest | Stable silhouette; tension shown through body not glow | Public claim becomes executable proof |
| Bed / root | Early domestic wood motif | Olive grain, joinery and rooted weight | Penelope's private verification |
| Gaze / partial face | Penelope observation | Reader knowledge and character knowledge separated by light | Marriage recognition |
| Empty seat | EP01 absent father | Occupied, challenged, avoided, restored | Return without erasing Telemachus's growth |
| Olive tree / land | Ithaca exterior language | Root, boundary, orchard memory | Laertes and civic closure |
| Sea | Pressure before image | Salt, timber, horizon and offscreen force | Return remains consequence-bearing |
| Silhouette | Gods, disguise, monsters | Identity revealed by posture before face | Athena continuity and Odysseus disguise |
`);

await writeText('P8_PUBLICATION_EXPORT_PLAN.md', `# P8 Publication Export Plan

The P7B panel manifest remains the narrative slot authority. P8 maps every panel ID to one master and responsive web derivatives. The same mapping can later drive PDF spreads, CBZ archives, vertical Webtoon strips and tablet layouts without rewriting dialogue.

- Master: high-quality source image, ratio-appropriate, retained outside the public payload.
- Web: AVIF/WebP derivatives with dimensions, srcset and lazy loading.
- PDF/CBZ: master-or-print derivative plus deterministic HTML text composition.
- Webtoon: scene-order vertical composition; never flatten Chinese text into art.

No export format may change source dialogue, panel order or spoiler timing.
`);

await writeText('P8_GOLD_STANDARD_RESULT.md', `# P8 Gold Standard Result

Status: IN_PROGRESS

- Candidate set: 20 panels
- Existing high-fidelity audit candidates: ${goldSpecs.filter((spec) => spec.render_status === 'EXISTING_HIGH_FIDELITY_AUDIT').length}
- New candidate renders required: ${goldSpecs.filter((spec) => spec.render_status === 'CANDIDATE_RENDER_REQUIRED').length}
- Required result: PASS_P8_GOLD_STANDARD_STYLE_LOCK
`);

console.log(JSON.stringify({ status: 'P8_FOUNDATION_READY', panels: acceptance.length, gold_standard: goldSpecs.length, queue_seed: queue.queue_count }, null, 2));
