import { createHash } from 'node:crypto';
import { access, readFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const siteRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const repoRoot = path.resolve(siteRoot, '..');
const distMode = process.argv.includes('--dist');
const readJson = async (relativePath) => JSON.parse(await readFile(path.join(repoRoot, relativePath), 'utf8'));
const sha = (bytes) => createHash('sha256').update(bytes).digest('hex');
const assert = (condition, message) => { if (!condition) throw new Error(message); };

const grammar = await readJson('comic-rendering/odyssey_m1_p8r1/P8R1_EP01_COMIC_GRAMMAR.json');
const visuals = await readJson('comic-rendering/odyssey_m1_p8r1/P8R1_EP01_VISUAL_OVERRIDE_MANIFEST.json');
const rejections = await readJson('comic-rendering/odyssey_m1_p8r1/P8R1_REJECTION_REGISTER.json');
const artifacts = await readJson('comic-rendering/odyssey_m1_p8r1/P8R1_ARTIFACT_MANIFEST.json');
const p7b = await readJson('graphic-script/odyssey_m1_p7b/P7B_PANEL_MANIFEST.json');
const generated = await readJson('site/src/generated/graphic-panels.json');
const generatedEpisodes = await readJson('site/src/generated/graphic-episodes.json');
const publication = await readJson('site/content/ASSET_PUBLICATION_MANIFEST.json');

assert(grammar.status === 'PASS_EP01_COMIC_READING_GRAMMAR', 'P8R1 grammar status mismatch');
assert(Object.keys(grammar.scene_compositions).length === 5, 'EP01 must freeze five scene compositions');
assert(new Set(Object.values(grammar.scene_compositions)).size >= 3, 'EP01 needs at least three layout compositions');
assert(Object.keys(grammar.panel_presentations).length === 17, 'EP01 must map all 17 panel presentations');
assert(visuals.visual_override_count === 7 && visuals.panels.length === 7, 'P8R1 visual override count mismatch');
assert(visuals.panels.every((panel) => panel.panel_id.startsWith('EP01-')), 'P8R1 visual override escaped EP01');
assert(rejections.rejection_count === 3 && rejections.rejected.every((item) => item.publication_status === 'REJECTED_NOT_PUBLISHED'), 'P8R1 rejection register mismatch');
assert(artifacts.status === 'PASS_EP01_COMIC_READING_GRAMMAR' && artifacts.P8_final_closeout === 'NOT_EXECUTED', 'P8R1 artifact manifest status mismatch');
assert(artifacts.artifact_count === artifacts.artifacts.length, 'P8R1 artifact count mismatch');
for (const artifact of artifacts.artifacts) {
  const bytes = await readFile(path.join(repoRoot, artifact.path));
  assert(bytes.length === artifact.bytes && sha(bytes) === artifact.sha256, `P8R1 artifact identity mismatch: ${artifact.path}`);
}

for (const visual of visuals.panels) {
  const bytes = await readFile(path.join(repoRoot, visual.source_path));
  assert(bytes.length === visual.web.bytes && sha(bytes) === visual.web.sha256, `P8R1 web identity mismatch: ${visual.panel_id}`);
  const published = publication.assets.find((asset) => asset.published_path === visual.public_path);
  assert(published && published.source_path === visual.source_path, `P8R1 asset missing from publication allowlist: ${visual.panel_id}`);
}
for (const rejected of rejections.rejected) {
  assert(!publication.assets.some((asset) => asset.source_path === rejected.path), `Rejected P8R1 asset published: ${rejected.path}`);
}

assert(generated.panels.length === 643, 'P8R1 must not change 643-slot P8 authority');
const p7bById = new Map(p7b.panels.map((panel) => [panel.panel_id, panel]));
const ep01Panels = generated.panels.filter((panel) => panel.episode === 'EP01');
assert(ep01Panels.length === 17, 'EP01 generated panel coverage mismatch');
assert(ep01Panels.filter((panel) => panel.visual.source_kind === 'P8R1_EP01_FINAL_COMIC_ART').length === 7, 'EP01 generated visual override join mismatch');
for (const panel of ep01Panels) {
  const source = p7bById.get(panel.panel_id);
  assert(JSON.stringify(panel.dialogue) === JSON.stringify(source.dialogue), `Exact-source dialogue changed: ${panel.panel_id}`);
  assert(panel.presentation, `Missing EP01 comic presentation: ${panel.panel_id}`);
}
assert(generated.panels.filter((panel) => panel.episode !== 'EP01').every((panel) => !panel.presentation), 'P8R1 presentation escaped EP01');
const ep01 = generatedEpisodes.find((episode) => episode.episode === 'EP01');
assert(['ep01-r1','ep01-r2'].includes(ep01?.repair_variant) && ep01.scenes.every((scene) => scene.composition), 'EP01 route repair/successor join mismatch');
assert(generatedEpisodes.filter((episode) => episode.episode !== 'EP01').every((episode) => !episode.repair_variant), 'P8R1 episode repair escaped EP01');

if (distMode) {
  const pagePath = path.join(siteRoot, 'dist/episodes/01/graphic/index.html');
  const html = await readFile(pagePath, 'utf8');
  assert(html.includes('data-comic-repair="P8R1"') || html.includes('data-comic-repair="P8R2"'), 'Built EP01 lacks P8R1 or bounded successor marker');
  assert((html.match(/data-panel-id=/g) || []).length === 17, 'Built EP01 panel sequence mismatch');
  assert(html.includes('故事从一只被夺走的杯子开始'), 'Built EP01 compact onboarding missing');
  assert(html.includes('门锁好。别替我告别。'), 'Built EP01 comic cliffhanger missing');
  for (const visual of visuals.panels) await access(path.join(siteRoot, 'dist', visual.public_path));
  const ep02 = await readFile(path.join(siteRoot, 'dist/episodes/02/graphic/index.html'), 'utf8');
  assert(!ep02.includes('data-comic-repair="P8R1"') && !ep02.includes('data-comic-repair="P8R2"'), 'Built EP01 repair marker escaped to EP02');
}

console.log(JSON.stringify({
  status: 'PASS_EP01_COMIC_READING_GRAMMAR',
  episode: 'EP01',
  scenes: 5,
  panels: 17,
  visual_overrides: 7,
  rejected_attempts: 3,
  layout_compositions: new Set(Object.values(grammar.scene_compositions)).size,
  dist_verified: distMode,
  scope: 'EP01_ONLY'
}));
