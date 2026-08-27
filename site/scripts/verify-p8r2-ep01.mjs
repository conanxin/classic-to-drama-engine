import { createHash } from 'node:crypto';
import { readFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const siteRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const repoRoot = path.resolve(siteRoot, '..');
const distMode = process.argv.includes('--dist');
const readJson = async (relativePath) => JSON.parse(await readFile(path.join(repoRoot, relativePath), 'utf8'));
const sha = (bytes) => createHash('sha256').update(bytes).digest('hex');
const assert = (condition, message) => { if (!condition) throw new Error(message); };

const grammar = await readJson('comic-rendering/odyssey_m1_p8r2/P8R2_EP01_FINAL_GRAMMAR.json');
const artifacts = await readJson('comic-rendering/odyssey_m1_p8r2/P8R2_ARTIFACT_MANIFEST.json');
const p7b = await readJson('graphic-script/odyssey_m1_p7b/P7B_PANEL_MANIFEST.json');
const p8 = await readJson('comic-rendering/odyssey_m1_p8/P8_WEB_VISUAL_MANIFEST.json');
const p8r1Grammar = await readJson('comic-rendering/odyssey_m1_p8r1/P8R1_EP01_COMIC_GRAMMAR.json');
const p8r1Visuals = await readJson('comic-rendering/odyssey_m1_p8r1/P8R1_EP01_VISUAL_OVERRIDE_MANIFEST.json');
const generatedPanels = await readJson('site/src/generated/graphic-panels.json');
const generatedEpisodes = await readJson('site/src/generated/graphic-episodes.json');

assert(grammar.status === 'PASS_EP01_FINAL_COMIC_GRAMMAR_LOCK', 'P8R2 grammar status mismatch');
assert(grammar.scope === 'EP01_GRAPHIC_PRESENTATION_ONLY', 'P8R2 scope mismatch');
assert(grammar.preserved.scenes === 5 && grammar.preserved.narrative_slots === 17, 'P8R2 scene/slot preservation mismatch');
assert(grammar.preserved.art_reused === 17 && grammar.preserved.art_newly_generated === 0, 'P8R2 art boundary mismatch');
assert(grammar.repairs.real_art_preview_slots === 17 && grammar.repairs.panel_sized_empty_text_rectangles_allowed === 0, 'P8R2 empty-panel repair mismatch');
assert(grammar.repairs.scene4_sequence.length === 4 && grammar.repairs.scene4_sequence[1].function === 'SUITOR_LISTENER_REACTION', 'P8R2 Scene 4 sequence mismatch');
assert(grammar.repairs.reaction_beats.length === 5 && grammar.repairs.insert_beats.length === 3, 'P8R2 reaction/insert coverage mismatch');
assert(JSON.stringify(Object.keys(grammar.source_modifications).map((key) => grammar.source_modifications[key])) === JSON.stringify([0,0,0,0,0,0,0,0]), 'P8R2 predecessor mutation declaration mismatch');
assert(grammar.comic_grammar_propagation === 'NOT_AUTHORIZED' && grammar.P8_final_closeout === 'NOT_EXECUTED', 'P8R2 stop boundary mismatch');
assert(artifacts.status === grammar.status && artifacts.artifact_count === artifacts.artifacts.length, 'P8R2 artifact manifest mismatch');
for (const artifact of artifacts.artifacts) {
  const bytes = await readFile(path.join(repoRoot, artifact.path));
  assert(bytes.length === artifact.bytes && sha(bytes) === artifact.sha256, `P8R2 artifact identity mismatch: ${artifact.path}`);
}

const p7bById = new Map(p7b.panels.map((panel) => [panel.panel_id, panel]));
const p8ById = new Map(p8.panels.map((visual) => [visual.panel_id, visual]));
const p8r1ById = new Map(p8r1Visuals.panels.map((visual) => [visual.panel_id, visual]));
const ep01Panels = generatedPanels.panels.filter((panel) => panel.episode === 'EP01');
assert(generatedPanels.panels.length === 643 && ep01Panels.length === 17, 'P8R2 generated panel coverage mismatch');
for (const panel of ep01Panels) {
  const source = p7bById.get(panel.panel_id);
  const expectedVisual = p8r1ById.get(panel.panel_id) || p8ById.get(panel.panel_id);
  assert(JSON.stringify(panel.dialogue) === JSON.stringify(source.dialogue), `Exact-source dialogue changed: ${panel.panel_id}`);
  assert(panel.visual.public_path === expectedVisual.public_path, `P8R2 changed visual authority: ${panel.panel_id}`);
  assert(panel.presentation, `Missing P8R2 panel presentation: ${panel.panel_id}`);
}
assert(JSON.stringify(p8r1Grammar.scene_compositions) === JSON.stringify(Object.fromEntries(generatedEpisodes[0].scenes.map((scene) => [scene.scene_id, scene.composition]))), 'P8R2 changed five scene compositions');
assert(generatedEpisodes[0].repair_variant === 'ep01-r2' && generatedEpisodes[0].repair_status === grammar.status, 'P8R2 EP01 route join mismatch');
assert(generatedEpisodes.slice(1).every((episode) => !episode.repair_variant), 'P8R2 repair variant escaped EP01');
const ep02Hash = sha(Buffer.from(JSON.stringify(generatedEpisodes[1])));
assert(ep02Hash === grammar.ep02_baseline.graphic_episode_canonical_json_sha256, 'EP02 generated authority changed');

if (distMode) {
  const ep01 = await readFile(path.join(siteRoot, 'dist/episodes/01/graphic/index.html'), 'utf8');
  const ep02 = await readFile(path.join(siteRoot, 'dist/episodes/02/graphic/index.html'), 'utf8');
  assert(ep01.includes('data-comic-repair="P8R2"'), 'Built EP01 lacks P8R2 marker');
  assert((ep01.match(/data-panel-id=/g) || []).length === 17, 'Built EP01 lost narrative slots');
  assert(ep01.includes('data-preview-art="real"'), 'Built EP01 lacks real-art preview coverage');
  assert(ep01.includes('crop-reaction-right'), 'Built EP01 lacks Scene 4 reaction crop');
  assert(ep01.includes('集数资料') && ep01.includes('EP01 · 最后一格'), 'Built EP01 story-first onboarding/cliffhanger missing');
  assert(!ep02.includes('data-comic-repair="P8R2"') && !ep02.includes('ep01-r2'), 'P8R2 presentation escaped EP01');
}

console.log(JSON.stringify({
  status:'PASS_EP01_FINAL_COMIC_GRAMMAR_LOCK',
  episode:'EP01',
  scenes:5,
  panels:17,
  art_reused:17,
  art_newly_generated:0,
  reaction_beats:5,
  insert_beats:3,
  empty_panel_like_blocks_remaining:0,
  ep02_unchanged:true,
  dist_verified:distMode,
  scope:'EP01_ONLY'
}));
