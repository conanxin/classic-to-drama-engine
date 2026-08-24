import { createHash } from 'node:crypto';
import { execFile } from 'node:child_process';
import { access, readFile } from 'node:fs/promises';
import path from 'node:path';
import { promisify } from 'node:util';
import { fileURLToPath } from 'node:url';

const siteRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const repoRoot = path.resolve(siteRoot, '..');
const distMode = process.argv.includes('--dist');
const prototypeNumbers = [1, 19, 27];
const p7aBaselineCommit = 'c6cc0fc1ad29068c21a326d19e62c68ac067722f';
const rejectedIds = ['P4-HF-19', 'P4-HF-29', 'P4-HF-34', 'P4-HF-39', 'P4-HF-43', 'P4-HF-44'];
const requiredCharacters = [
  'odysseus', 'penelope', 'telemachus', 'athena', 'eumaeus', 'eurycleia',
  'antinous', 'eurymachus', 'amphinomus', 'suitors', 'poseidon', 'phaeacians', 'otherworld'
];
const fail = (message) => { throw new Error(`P7A graphic prototype verification failed: ${message}`); };
const sha256 = (bytes) => createHash('sha256').update(bytes).digest('hex');
const readRepoJson = async (relative) => JSON.parse(await readFile(path.join(repoRoot, relative), 'utf8'));
const exists = async (target) => access(target).then(() => true).catch(() => false);
const sourceText = (value) => String(value).replace(/\r/g, '').replace(/[\t ]+/g, ' ').trim();
const run = promisify(execFile);
const historicalBytes = async (relative) => {
  const { stdout } = await run('git', ['show', `${p7aBaselineCommit}:${relative}`], { cwd:repoRoot, encoding:null, maxBuffer:64 * 1024 * 1024 });
  return stdout;
};

const recognition = await readRepoJson('graphic-script/odyssey_m1_p7a/CHARACTER_RECOGNITION_SYSTEM.json');
const assetManifest = await readRepoJson('site/content/ASSET_PUBLICATION_MANIFEST.json');
const p7aManifest = await readRepoJson('graphic-script/odyssey_m1_p7a/P7A_ARTIFACT_MANIFEST.json');
const assets = new Map(assetManifest.assets.map((asset) => [asset.published_path, asset]));
const characters = new Map(recognition.characters.map((character) => [character.id, character]));

if (recognition.status !== 'FROZEN_P7A_PROTOTYPE_SYSTEM') fail('character recognition system is not frozen');
if (p7aManifest.artifact_class !== 'ODYSSEY_P7A_ARTIFACT_MANIFEST' || p7aManifest.counts.graphic_prototypes !== 3) fail('P7A artifact manifest identity is invalid');
for (const artifact of p7aManifest.artifacts) {
  const bytes = artifact.path.startsWith('site/') ? await historicalBytes(artifact.path) : await readFile(path.join(repoRoot, artifact.path));
  if (bytes.length !== artifact.bytes || sha256(bytes) !== artifact.sha256) fail(`P7A artifact identity mismatch: ${artifact.path}`);
}
if (recognition.characters.length < 16) fail(`character recognition coverage is ${recognition.characters.length}, expected at least 16`);
if (new Set(recognition.characters.map((item) => item.id)).size !== recognition.characters.length) fail('duplicate character recognition ID');
for (const id of requiredCharacters) if (!characters.has(id)) fail(`required character recognition entry missing: ${id}`);
const melanthius = characters.get('melanthius');
if (melanthius.aliases.includes('背叛者') || melanthius.revealed_alias !== '背叛者' || melanthius.revealed_at !== 'EP27-S04') {
  fail('Melanthius revealed identity is not spoiler-safe');
}
for (const character of recognition.characters) {
  for (const field of ['name', 'faction', 'color', 'anchor', 'prop', 'shape', 'first_appearance']) {
    if (!character[field]) fail(`${character.id} missing recognition field ${field}`);
  }
  if (character.image && !assets.has(character.image)) fail(`${character.id} image is not publication-allowlisted: ${character.image}`);
}

let sceneCount = 0;
let exactDialogueCount = 0;
let visualCount = 0;
const allSceneIds = new Set();
for (const number of prototypeNumbers) {
  const padded = String(number).padStart(2, '0');
  const prototypePath = `graphic-script/odyssey_m1_p7a/prototypes/EP${padded}_GRAPHIC_SCRIPT_PROTOTYPE.json`;
  const prototype = await readRepoJson(prototypePath);
  const sourcePath = path.join(repoRoot, prototype.source_path);
  const sourceBytes = await readFile(sourcePath);
  const source = sourceText(sourceBytes.toString('utf8'));

  if (prototype.number !== number || prototype.episode !== `EP${padded}`) fail(`prototype identity mismatch: ${prototypePath}`);
  if (sha256(sourceBytes) !== prototype.source_sha256) fail(`${prototype.episode} source SHA-256 mismatch`);
  if (prototype.status !== 'COMPLETE_P7A_PROTOTYPE') fail(`${prototype.episode} is not complete`);
  if (prototype.scenes.length !== 5) fail(`${prototype.episode} has ${prototype.scenes.length} scene blocks, expected 5`);
  for (const field of ['previously_on', 'core_conflict', 'story_stage', 'end_hook']) {
    if (!prototype[field]) fail(`${prototype.episode} missing ${field}`);
  }
  for (const castId of prototype.cast) if (!characters.has(castId)) fail(`${prototype.episode} unknown cast ID ${castId}`);
  for (const visual of [prototype.cover_visual, ...prototype.scenes.map((scene) => scene.visual)]) {
    const asset = assets.get(visual.path);
    if (!asset || asset.status !== 'APPROVED') fail(`${prototype.episode} visual is not approved/allowlisted: ${visual.path}`);
    if (rejectedIds.some((id) => `${visual.path} ${visual.authority}`.includes(id))) fail(`${prototype.episode} promotes rejected P4 target`);
    visualCount += 1;
  }

  for (const [index, scene] of prototype.scenes.entries()) {
    const expectedId = `EP${padded}-S${String(index + 1).padStart(2, '0')}`;
    if (scene.scene_id !== expectedId) fail(`${prototype.episode} expected ${expectedId}, got ${scene.scene_id}`);
    if (allSceneIds.has(scene.scene_id)) fail(`duplicate scene ID ${scene.scene_id}`);
    allSceneIds.add(scene.scene_id);
    sceneCount += 1;
    for (const field of ['heading', 'location', 'time', 'conflict_goal', 'relation_tip', 'space_tip', 'prop_tip', 'irreversible_change']) {
      if (!scene[field]) fail(`${scene.scene_id} missing ${field}`);
    }
    if (!Array.isArray(scene.narrative) || scene.narrative.length < 2) fail(`${scene.scene_id} has insufficient reduced narrative`);
    if (!Array.isArray(scene.essential_dialogue) || scene.essential_dialogue.length < 2) fail(`${scene.scene_id} has insufficient essential dialogue`);
    for (const castId of scene.cast) if (!characters.has(castId)) fail(`${scene.scene_id} unknown cast ID ${castId}`);
    for (const quote of scene.essential_dialogue) {
      if (!quote.speaker || !quote.text) fail(`${scene.scene_id} incomplete dialogue entry`);
      if (!source.includes(sourceText(quote.text))) fail(`${scene.scene_id} dialogue is not exact V2 source text: ${quote.text}`);
      exactDialogueCount += 1;
    }
  }
}

const serialized = JSON.stringify({ recognition, prototypeNumbers });
for (const rejected of rejectedIds) if (serialized.includes(rejected)) fail(`rejected target ID appears in active P7A system: ${rejected}`);
for (const pattern of [/\/home\/conanxin\//i, /C:\\Users\\/i, /\\\\wsl\$/i, /api[_-]?key/i, /credential/i]) {
  if (pattern.test(serialized)) fail(`forbidden internal/public text ${pattern}`);
}

if (distMode) {
  const routes = ['graphic/index.html', ...prototypeNumbers.map((number) => `episodes/${String(number).padStart(2, '0')}/graphic/index.html`)];
  for (const route of routes) if (!(await exists(path.join(siteRoot, 'dist', route)))) fail(`missing built route ${route}`);
  for (const number of prototypeNumbers) {
    const padded = String(number).padStart(2, '0');
    const html = await readFile(path.join(siteRoot, 'dist', 'episodes', padded, 'graphic', 'index.html'), 'utf8');
    if (!html.includes('图文模式') || !html.includes('剧本模式')) fail(`EP${padded} dual reading mode control missing`);
    if (!html.includes(`data-graphic-episode=\"EP${padded}\"`)) fail(`EP${padded} graphic route marker missing`);
    if (!html.includes('展开原剧本')) fail(`EP${padded} expandable source layer missing`);
    if (rejectedIds.some((id) => html.includes(id))) fail(`EP${padded} built HTML contains rejected visual ID`);
  }
}

console.log(JSON.stringify({
  status: 'PASS_P7A_GRAPHIC_PROTOTYPES_VERIFY',
  dist_verified: distMode,
  prototypes: prototypeNumbers.length,
  scenes: sceneCount,
  exact_source_dialogue_quotes: exactDialogueCount,
  approved_visual_references: visualCount,
  character_recognition_entries: recognition.characters.length,
  rejected_visual_promotions: 0,
  historical_site_artifacts_verified_at: p7aBaselineCommit,
  current_p7a_narrative_artifacts_unchanged: true
}));
