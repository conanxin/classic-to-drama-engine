import { createHash } from 'node:crypto';
import { access, readFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const siteRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const repoRoot = path.resolve(siteRoot, '..');
const distMode = process.argv.includes('--dist');
const readJson = async (relative) => JSON.parse(await readFile(path.join(repoRoot, relative), 'utf8'));
const sha256 = (bytes) => createHash('sha256').update(bytes).digest('hex');
const exists = (target) => access(target).then(() => true).catch(() => false);
const assert = (condition, message) => { if (!condition) throw new Error(`P8R3 verification failed: ${message}`); };

const grammar = await readJson('comic-rendering/odyssey_m1_p8r3/P8R3_SERIES_COMIC_GRAMMAR.json');
const artifacts = await readJson('comic-rendering/odyssey_m1_p8r3/P8R3_ARTIFACT_MANIFEST.json');
const p7b = await readJson('graphic-script/odyssey_m1_p7b/P7B_PANEL_MANIFEST.json');
const p8 = await readJson('comic-rendering/odyssey_m1_p8/P8_WEB_VISUAL_MANIFEST.json');
const p8r1Grammar = await readJson('comic-rendering/odyssey_m1_p8r1/P8R1_EP01_COMIC_GRAMMAR.json');
const p8r1Visuals = await readJson('comic-rendering/odyssey_m1_p8r1/P8R1_EP01_VISUAL_OVERRIDE_MANIFEST.json');
const p8r2 = await readJson('comic-rendering/odyssey_m1_p8r2/P8R2_EP01_FINAL_GRAMMAR.json');
const generatedPanels = await readJson('site/src/generated/graphic-panels.json');
const generatedEpisodes = await readJson('site/src/generated/graphic-episodes.json');

assert(grammar.status === 'PASS_P8R3_GRAMMAR_AUTHORITY_GENERATED', 'grammar authority status mismatch');
assert(grammar.human_authorization.exact_quote === 'EP01_FINAL_COMIC_GRAMMAR: APPROVED_FOR_SERIES_PROPAGATION', 'human propagation authorization missing');
assert(grammar.coverage.episodes === 30 && grammar.coverage.scenes === 150 && grammar.coverage.panel_slots === 643, 'grammar coverage mismatch');
assert(Object.keys(grammar.scene_compositions).length === 150, 'scene composition coverage mismatch');
assert(Object.keys(grammar.panel_presentations).length === 643, 'panel presentation coverage mismatch');
assert(grammar.rules.panel_sized_empty_text_rectangles_allowed === 0 && grammar.rules.raster_text_allowed === 0, 'presentation boundary weakened');
assert(Object.values(grammar.source_modifications).every((value) => value === 0), 'predecessor mutation declaration mismatch');

assert(artifacts.status === 'P8R3_ARTIFACTS_FROZEN' && artifacts.artifact_count === artifacts.artifacts.length, 'artifact manifest mismatch');
for (const artifact of artifacts.artifacts) {
  const bytes = await readFile(path.join(repoRoot, artifact.path));
  assert(bytes.length === artifact.bytes && sha256(bytes) === artifact.sha256, `artifact identity mismatch ${artifact.path}`);
}

const p7bById = new Map(p7b.panels.map((panel) => [panel.panel_id, panel]));
const p8ById = new Map(p8.panels.map((panel) => [panel.panel_id, panel]));
const p8r1ById = new Map(p8r1Visuals.panels.map((panel) => [panel.panel_id, panel]));
assert(generatedEpisodes.length === 30 && generatedEpisodes.every((episode) => episode.scenes.length === 5), 'generated episode/scene coverage mismatch');
assert(generatedPanels.panels.length === 643 && new Set(generatedPanels.panels.map((panel) => panel.panel_id)).size === 643, 'generated panel coverage mismatch');

const narrativeKeys = ['panel_id','episode','scene_id','sequence','panel_type','ratio','dramatic_purpose','shot_id','subject','caption','dialogue','silent','continuity','action_beat_ids'];
for (const panel of generatedPanels.panels) {
  const source = p7bById.get(panel.panel_id);
  const visual = p8r1ById.get(panel.panel_id) || p8ById.get(panel.panel_id);
  assert(source && visual, `authority join missing ${panel.panel_id}`);
  for (const key of narrativeKeys) assert(JSON.stringify(panel[key]) === JSON.stringify(source[key]), `source narrative changed ${panel.panel_id}.${key}`);
  assert(panel.visual.public_path === visual.public_path, `accepted visual changed ${panel.panel_id}`);
  assert(JSON.stringify(panel.presentation) === JSON.stringify(grammar.panel_presentations[panel.panel_id]), `presentation mismatch ${panel.panel_id}`);
}

const ep01 = generatedEpisodes[0];
assert(ep01.repair_variant === 'ep01-r2' && ep01.repair_status === p8r2.status, 'EP01 gold-standard identity changed');
assert(JSON.stringify(Object.fromEntries(ep01.scenes.map((scene) => [scene.scene_id, scene.composition]))) === JSON.stringify(p8r1Grammar.scene_compositions), 'EP01 compositions changed');
for (const scene of ep01.scenes) for (const panel of scene.panels) {
  const expected = p8r2.panel_presentation_overrides[panel.panel_id] || p8r1Grammar.panel_presentations[panel.panel_id];
  assert(JSON.stringify(panel.presentation) === JSON.stringify(expected), `EP01 presentation drift ${panel.panel_id}`);
}
assert(generatedEpisodes.slice(1).every((episode) => episode.repair_variant === 'series-r3' && episode.comic_grammar === 'P8R3'), 'P8R3 did not cover EP02-EP30');

if (distMode) {
  let builtScenes = 0;
  let builtPanels = 0;
  let previews = 0;
  let sourceLayers = 0;
  let cliffhangers = 0;
  let storyBridges = 0;
  for (const episode of generatedEpisodes) {
    const padded = String(episode.number).padStart(2, '0');
    const htmlPath = path.join(siteRoot, 'dist/episodes', padded, 'graphic/index.html');
    assert(await exists(htmlPath), `missing graphic route EP${padded}`);
    const html = await readFile(htmlPath, 'utf8');
    const episodePanels = episode.scenes.reduce((sum, scene) => sum + scene.panels.length, 0);
    const panelCount = (html.match(/data-panel-id=/g) || []).length;
    const sceneCount = (html.match(/data-scene-id=/g) || []).length;
    assert(html.includes('data-comic-grammar="P8R3"'), `P8R3 marker missing EP${padded}`);
    assert(sceneCount === 5 && panelCount === episodePanels, `built coverage mismatch EP${padded}`);
    assert((html.match(/data-preview-art="real"/g) || []).length === episodePanels, `real-art preview coverage mismatch EP${padded}`);
    assert((html.match(/class="source-layer"/g) || []).length === 5, `source layer coverage mismatch EP${padded}`);
    const sourceTags = html.match(/<details[^>]*class="source-layer"[^>]*>/g) || [];
    assert(sourceTags.length === 5 && sourceTags.every((tag) => !/\sopen(?:\s|=|>)/.test(tag)), `source layer defaults open EP${padded}`);
    assert(html.includes('comic-cliffhanger') && html.includes(`${episode.episode} · 最后一格`), `comic cliffhanger missing EP${padded}`);
    assert(!html.includes('class="scene-bridge"'), `illustrated-screenplay bridge remains EP${padded}`);
    assert(html.includes('class="panel-bubble"') && /<figcaption(?:\s|>)/.test(html), `speech/caption semantics missing EP${padded}`);
    builtScenes += sceneCount;
    builtPanels += panelCount;
    previews += (html.match(/data-preview-art="real"/g) || []).length;
    sourceLayers += (html.match(/class="source-layer"/g) || []).length;
    cliffhangers += html.includes('comic-cliffhanger') ? 1 : 0;
    storyBridges += (html.match(/class="scene-bridge"/g) || []).length;
  }
  assert(builtScenes === 150 && builtPanels === 643 && previews === 643 && sourceLayers === 150 && cliffhangers === 30 && storyBridges === 0, 'series built totals mismatch');
}

console.log(JSON.stringify({
  status:'PASS_P8R3_INDEPENDENT_VERIFICATION',
  human_authorization:'CONFIRMED',
  episodes:'30/30',
  scenes:'150/150',
  panels:'643/643',
  source_dialogue:'UNCHANGED',
  narrative_events:'UNCHANGED',
  visuals_reused:643,
  empty_panel_like_blocks_allowed:0,
  source_layers:'150/150',
  cliffhangers:'30/30',
  dist_verified:distMode,
  P6_status:'PAUSED_BY_USER'
}));
