import { createHash } from 'node:crypto';
import { access, readFile } from 'node:fs/promises';
import { execFileSync } from 'node:child_process';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const siteRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const repoRoot = path.resolve(siteRoot, '..');
const distMode = process.argv.includes('--dist');
const baseline = '912cdd6715fe5ae4fe82418b30035440938a9c17';
const readJson = async (relative) => JSON.parse(await readFile(path.join(repoRoot, relative), 'utf8'));
const readText = async (relative) => readFile(path.join(repoRoot, relative), 'utf8');
const exists = (target) => access(target).then(() => true).catch(() => false);
const hash = (bytes) => createHash('sha256').update(bytes).digest('hex');
const normalize = (value) => String(value).replace(/\r/g, '').replace(/[\t ]+/g, ' ').trim();
const fail = (message) => { throw new Error(`P7B rollout verification failed: ${message}`); };

const episodeManifest = await readJson('graphic-script/odyssey_m1_p7b/P7B_EPISODE_MANIFEST.json');
const panelManifest = await readJson('graphic-script/odyssey_m1_p7b/P7B_PANEL_MANIFEST.json');
const characters = await readJson('graphic-script/odyssey_m1_p7b/P7B_CHARACTER_REGISTRY.json');
const props = await readJson('graphic-script/odyssey_m1_p7b/P7B_PROP_VISUAL_LEDGER.json');
const queue = await readJson('graphic-script/odyssey_m1_p7b/P7B_NEW_PANEL_GENERATION_QUEUE.json');
const assets = await readJson('site/content/ASSET_PUBLICATION_MANIFEST.json');
const screenplay = await readJson('scripts/odyssey_m1_v2/SCREENPLAY_V2_MANIFEST.json');
const sceneMaster = await readJson('preproduction/odyssey_m1_p3/SCENE_MASTER_INDEX.json');
const actionPrevis = await readJson('preproduction/odyssey_m1_p3/EP26_EP28_ACTION_PREVIS.json');
const p8Visuals = await readJson('comic-rendering/odyssey_m1_p8/P8_WEB_VISUAL_MANIFEST.json');

if (episodeManifest.authorization !== 'USER_AUTHORIZED_WITHOUT_REAL_READER_EVIDENCE' || episodeManifest.real_reader_validation !== 'NOT_CLAIMED') fail('authorization/evidence boundary mismatch');
if (episodeManifest.counts.episodes !== 30 || episodeManifest.episodes.length !== 30) fail('episode coverage is not 30/30');
if (episodeManifest.counts.scenes !== 150 || episodeManifest.episodes.reduce((sum, episode) => sum + episode.scenes.length, 0) !== 150) fail('scene coverage is not 150/150');
if (episodeManifest.episodes.some((episode) => episode.scenes.length !== 5)) fail('an episode lacks five scenes');
if (episodeManifest.story_movements.length !== 5 || episodeManifest.story_movements.map((item) => item.range.join('-')).join(',') !== '1-4,5-8,9-15,16-24,25-30') fail('formal story movements changed');

const episodeNumbers = episodeManifest.episodes.map((episode) => episode.number);
if (new Set(episodeNumbers).size !== 30 || episodeNumbers.some((number, index) => number !== index + 1)) fail('episode numbering/route chain is invalid');
for (const episode of episodeManifest.episodes) {
  if (episode.status !== 'COMPLETE_P7B_GRAPHIC_EPISODE' || !episode.cover_visual?.path || !episode.end_hook || !episode.core_conflict || !episode.story_stage) fail(`${episode.episode} incomplete`);
  if (episode.previous_episode !== (episode.number > 1 ? episode.number - 1 : null) || episode.next_episode !== (episode.number < 30 ? episode.number + 1 : null)) fail(`${episode.episode} previous/next chain break`);
  const artifact = screenplay.artifacts.find((item) => item.episode_id === episode.episode);
  if (!artifact || artifact.path !== episode.source_path || artifact.sha256 !== episode.source_sha256) fail(`${episode.episode} screenplay binding mismatch`);
  const sourceBytes = await readFile(path.join(repoRoot, episode.source_path));
  if (hash(sourceBytes) !== episode.source_sha256) fail(`${episode.episode} source bytes changed`);
  const source = normalize(sourceBytes.toString('utf8'));
  for (const scene of episode.scenes) {
    if (!scene.scene_id || !scene.heading || !scene.location || !scene.conflict_goal || !scene.narrative?.length || !scene.panel_ids?.length) fail(`${scene.scene_id || episode.episode} scene content incomplete`);
    if (scene.panel_ids.length < 3 || scene.panel_ids.length > 6) fail(`${scene.scene_id} adaptive panel density invalid`);
    if (!scene.essential_dialogue?.length && !scene.panel_ids.some((id) => panelManifest.panels.find((panel) => panel.panel_id === id)?.silent)) fail(`${scene.scene_id} lacks dialogue or intentional silence`);
    for (const quote of scene.essential_dialogue) if (!source.includes(normalize(quote.text))) fail(`${scene.scene_id} non-source dialogue: ${quote.text}`);
  }
}

const panelIds = panelManifest.panels.map((panel) => panel.panel_id);
if (panelManifest.counts.panel_placements !== panelIds.length || panelIds.length < 450 || panelIds.length > 650) fail(`panel placements ${panelIds.length} outside 450–650`);
if (new Set(panelIds).size !== panelIds.length) fail('duplicate panel IDs');
if (panelManifest.counts.unique_visual_assets !== new Set(panelManifest.panels.map((panel) => panel.visual.public_path)).size) fail('unique visual count mismatch');
if (panelManifest.counts.new_generated_assets !== 0) fail('unexpected new generated story art');
if (panelManifest.panels.some((panel) => !panel.visual?.source_path || !panel.visual?.public_path || !panel.alt || !panel.shot_id || !panel.panel_type || !panel.ratio)) fail('panel visual/source metadata incomplete');
if (panelManifest.panels.some((panel) => /TODO|PLACEHOLDER|IMAGE HERE/i.test(JSON.stringify(panel)))) fail('placeholder panel content found');
const rejected = ['P4-HF-19','P4-HF-29','P4-HF-34','P4-HF-39','P4-HF-43','P4-HF-44'];
if (panelManifest.panels.some((panel) => rejected.some((id) => JSON.stringify(panel).includes(id)))) fail('rejected P4 hero promoted');

if (p8Visuals.status !== 'PASS_P8_FINAL_COMIC_VISUAL_MAPPING' || p8Visuals.panels.length !== 643) fail('P8 visual overlay is incomplete');
const p8ByPanelId = new Map(p8Visuals.panels.map((visual) => [visual.panel_id, visual]));
const assetByPublished = new Map(assets.assets.map((asset) => [asset.published_path, asset]));
for (const panel of panelManifest.panels) {
  const visual = p8ByPanelId.get(panel.panel_id);
  const asset = assetByPublished.get(visual?.public_path);
  if (!visual || !asset || asset.status !== 'APPROVED' || asset.source_path !== visual.source_path) fail(`P8 panel not publication-allowlisted: ${panel.panel_id}`);
}
for (const cover of p8Visuals.episodes) if (!assetByPublished.has(cover.public_path)) fail(`P8 cover not publication-allowlisted: ${cover.episode}`);

const characterIds = new Set(characters.characters.map((character) => character.id));
if (characters.source_cast_labels !== 76 || characters.resolved_source_cast_labels !== 76) fail('source cast label resolution is not 100%');
if (new Set(characters.characters.map((character) => character.id)).size !== characters.characters.length) fail('duplicate character ID');
for (const episode of episodeManifest.episodes) for (const scene of episode.scenes) for (const entry of scene.cast) if (!characterIds.has(entry.character_id)) fail(`unresolved character ID ${entry.character_id}`);

if (props.props.length !== 9 || props.action_continuity.beat_count !== 44 || new Set(props.action_continuity.beat_ids).size !== 44) fail('prop/action continuity coverage mismatch');
if (props.action_continuity.beat_ids.join('|') !== actionPrevis.beats.map((beat) => beat.id).join('|')) fail('EP26–28 action beat order changed');
const boundBeats = new Set(panelManifest.panels.flatMap((panel) => panel.action_beat_ids));
if (boundBeats.size !== 44 || actionPrevis.beats.some((beat) => !boundBeats.has(beat.id))) fail('not all 44 action beats are panel-bound');
if (queue.graphic_completion_blocked !== false || queue.status !== 'NON_BLOCKING_FUTURE_RENDER_QUEUE') fail('P8 queue incorrectly blocks P7B completion');

const immutablePaths = ['scripts/odyssey_m1_v2','editorial/odyssey_m1_v2','production/odyssey_m1_v2','preproduction/odyssey_m1_p3','visual-development/odyssey_m1_p4','storyboards/odyssey_m1_p4','design/odyssey_m1_p4','previs/odyssey_m1_p4','art-department/odyssey_m1_p5','animatic/odyssey_m1_p5','vfx-previs/odyssey_m1_p5','production-tests/odyssey_m1_p5','pitch/odyssey_m1_p5','runtime_capability_prototype'];
const immutableDiff = execFileSync('git', ['diff','--name-only',baseline,'--',...immutablePaths], { cwd:repoRoot, encoding:'utf8' }).trim();
if (immutableDiff) fail(`frozen predecessor modified:\n${immutableDiff}`);
const priorGraphicDiff = execFileSync('git', ['diff','--name-only',baseline,'--','graphic-script/odyssey_m1_p7a','graphic-script/odyssey_m1_p7c'], { cwd:repoRoot, encoding:'utf8' }).trim();
if (priorGraphicDiff) fail(`P7A/P7C authority modified:\n${priorGraphicDiff}`);

if (distMode) {
  for (let number = 1; number <= 30; number += 1) {
    const padded = String(number).padStart(2, '0');
    const graphicPath = path.join(siteRoot, 'dist', 'episodes', padded, 'graphic', 'index.html');
    const scriptPath = path.join(siteRoot, 'dist', 'episodes', padded, 'index.html');
    if (!(await exists(graphicPath)) || !(await exists(scriptPath))) fail(`missing Script/Graphic route EP${padded}`);
    const html = await readFile(graphicPath, 'utf8');
    for (const token of [`data-graphic-episode="EP${padded}"`, 'data-panel-id=', '展开原剧本', 'Graphic Mode', 'Script Mode']) if (!html.includes(token)) fail(`EP${padded} built route missing ${token}`);
    if (/TODO|PLACEHOLDER|IMAGE HERE/i.test(html)) fail(`EP${padded} contains placeholder`);
  }
  const directoryHtml = await readFile(path.join(siteRoot, 'dist', 'graphic', 'index.html'), 'utf8');
  if ((directoryHtml.match(/class="episode-row"/g) || []).length !== 30) fail('Graphic directory does not expose 30 episodes');
  for (const visual of p8Visuals.panels) if (!(await exists(path.join(siteRoot, 'dist', visual.public_path)))) fail(`missing built P8 panel asset ${visual.public_path}`);
}

console.log(JSON.stringify({
  status:'PASS_P7B_ROLLOUT_VERIFY', dist_verified:distMode, episodes:30, scenes:150, panels:panelIds.length,
  exact_source_dialogue:panelManifest.counts.exact_source_dialogue, character_source_labels_resolved:'76/76', action_beats:'44/44',
  script_routes:'30/30', graphic_routes:'30/30', rejected_visual_promotions:0, placeholders:0,
  V2_modified:0, P3_modified:0, P4_modified:0, P5_modified:0, Runtime_modified:0, P7A_P7C_authority_modified:0,
  real_reader_validation:'NOT_CLAIMED', P6_status:'PAUSED_BY_USER'
}));
