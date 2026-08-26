import { createHash } from 'node:crypto';
import { readFile, writeFile, stat } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const siteRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const repoRoot = path.resolve(siteRoot, '..');
const readJson = async (p) => JSON.parse(await readFile(path.join(repoRoot, p), 'utf8'));
const hash = async (p) => createHash('sha256').update(await readFile(path.join(repoRoot, p))).digest('hex');
const entries = [];

async function add(sourcePath, publishedPath, type, authority, status = 'APPROVED', transform = null) {
  const info = await stat(path.join(repoRoot, sourcePath));
  entries.push({
    source_path: sourcePath,
    published_path: publishedPath,
    type,
    bytes: info.size,
    sha256: await hash(sourcePath),
    authority,
    status,
    ...(transform ? { transform } : {})
  });
}

const look = await readJson('visual-development/odyssey_m1_p4/LOOKDEV_RENDER_MANIFEST.json');
const selectedHero = new Set(look.assets.filter((asset) => asset.status === 'APPROVED' && asset.asset_type === 'HERO_LOOKDEV_FRAME').map((asset) => asset.asset_id));
for (const asset of look.assets) {
  const include = asset.status === 'APPROVED' && (
    asset.asset_type === 'PRINCIPAL_CHARACTER_SHEET' ||
    asset.asset_type === 'STANDING_SET_ANCHOR' ||
    (asset.asset_type === 'HERO_LOOKDEV_FRAME' && selectedHero.has(asset.asset_id))
  );
  if (!include) continue;
  if (!asset.output_path) throw new Error(`Approved web asset lacks output_path: ${asset.asset_id}`);
  const folder = asset.asset_type === 'PRINCIPAL_CHARACTER_SHEET' ? 'characters' : asset.asset_type === 'STANDING_SET_ANCHOR' ? 'sets' : 'hero';
  await add(asset.output_path, `media/visual/${folder}/${path.basename(asset.output_path)}`, 'image', `P4 ${asset.asset_type} ${asset.asset_id}`);
}

const color = await readJson('visual-development/odyssey_m1_p4/COLOR_KEY_IMAGE_MANIFEST.json');
for (const asset of color.images) {
  await add(asset.path, `media/visual/color/${path.basename(asset.path)}`, 'image', `P4 approved color key ${asset.episode}`);
}

const boards = await readJson('storyboards/odyssey_m1_p4/STORYBOARD_IMAGE_MANIFEST.json');
for (const asset of boards.board_pages) {
  await add(asset.path, `media/storyboards/boards/${path.basename(asset.path)}`, 'image', `P4 ${asset.classification} ${asset.scene_id} ${asset.priority}`);
}
for (const asset of boards.episode_contact_sheets) {
  await add(asset.path, `media/storyboards/contact/${path.basename(asset.path)}`, 'image', `P4 technical contact sheet ${asset.episode}`);
}

await add('pitch/odyssey_m1_p5/PITCH_TEASER_PREVIS.mp4', 'media/video/PITCH_TEASER_PREVIS.mp4', 'video', 'P5 approved pitch previs');
await add('previs/odyssey_m1_p4/TEASER_PREVIS.mp4', 'media/video/P4_TEASER_PREVIS.mp4', 'video', 'P4 approved teaser previs');

for (let i = 1; i <= 30; i += 1) {
  const ep = `EP${String(i).padStart(2, '0')}`;
  await add(`animatic/odyssey_m1_p5/episodes/${ep}_ANIMATIC.mp4`, `media/animatics/${ep}_ANIMATIC.mp4`, 'video', `P5 timing animatic ${ep}`);
}

const p7bPanels = await readJson('graphic-script/odyssey_m1_p7b/P7B_PANEL_MANIFEST.json');
const p8Visuals = await readJson('comic-rendering/odyssey_m1_p8/P8_WEB_VISUAL_MANIFEST.json');
if (p8Visuals.status !== 'PASS_P8_FINAL_COMIC_VISUAL_MAPPING' || p8Visuals.counts.panel_slots !== 643) {
  throw new Error('P8 final comic visual mapping is incomplete');
}
const transformedPanelAssets = new Map();
for (const panel of p7bPanels.panels) {
  if (!panel.visual.transform) continue;
  const existing = transformedPanelAssets.get(panel.visual.public_path);
  const identity = JSON.stringify([panel.visual.source_path, panel.visual.transform]);
  if (existing && existing !== identity) throw new Error(`Conflicting P7B panel transform: ${panel.visual.public_path}`);
  transformedPanelAssets.set(panel.visual.public_path, identity);
}
// P7B transformed storyboard/animatic derivatives remain preserved in their source
// manifests but are superseded in the public reader by P8 final comic art.
for (const panel of p8Visuals.panels) {
  if (entries.some((entry) => entry.published_path === panel.public_path)) throw new Error(`Duplicate P8 public path: ${panel.public_path}`);
  await add(panel.source_path, panel.public_path, 'image', panel.authority);
}

entries.sort((a, b) => a.published_path.localeCompare(b.published_path));
const duplicatePublished = entries.filter((x, i) => entries.findIndex((y) => y.published_path === x.published_path) !== i);
if (duplicatePublished.length) throw new Error(`Duplicate published asset paths: ${duplicatePublished.map((x) => x.published_path).join(', ')}`);

const payload = {
  artifact_class: 'CTDE_WEB_ASSET_PUBLICATION_MANIFEST',
  schema_version: '1.0.0',
  baseline_commit: '478fd10f5b115c70f7b4b8ce5146ae2b6c6d37e5',
  strategy: 'Curated approved P4/P5 archive media plus 643 accepted P8 final-comic web derivatives. P7B technical/animatic panel derivatives remain historical source evidence and are not promoted as final reader art. All dialogue and narration remain semantic HTML; rejected and candidate P8 renders remain unpublished.',
  selected_hero_frame_ids: [...selectedHero].sort(),
  rejected_hero_frame_ids: ['P4-HF-19','P4-HF-29','P4-HF-34','P4-HF-39','P4-HF-43','P4-HF-44'],
  asset_count: entries.length,
  total_bytes: entries.reduce((n, x) => n + x.bytes, 0),
  assets: entries,
  status: 'APPROVED_PUBLIC_MEDIA_ALLOWLIST'
};

await writeFile(path.join(siteRoot, 'content/ASSET_PUBLICATION_MANIFEST.json'), `${JSON.stringify(payload, null, 2)}\n`);
console.log(JSON.stringify({ assets: payload.asset_count, total_bytes: payload.total_bytes, output: 'content/ASSET_PUBLICATION_MANIFEST.json' }));
