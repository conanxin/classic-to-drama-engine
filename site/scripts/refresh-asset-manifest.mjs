import { createHash } from 'node:crypto';
import { readFile, writeFile, stat } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const siteRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const repoRoot = path.resolve(siteRoot, '..');
const readJson = async (p) => JSON.parse(await readFile(path.join(repoRoot, p), 'utf8'));
const hash = async (p) => createHash('sha256').update(await readFile(path.join(repoRoot, p))).digest('hex');
const entries = [];

async function add(sourcePath, publishedPath, type, authority, status = 'APPROVED') {
  const info = await stat(path.join(repoRoot, sourcePath));
  entries.push({
    source_path: sourcePath,
    published_path: publishedPath,
    type,
    bytes: info.size,
    sha256: await hash(sourcePath),
    authority,
    status
  });
}

const look = await readJson('visual-development/odyssey_m1_p4/LOOKDEV_RENDER_MANIFEST.json');
const selectedHero = new Set(['P4-HF-01','P4-HF-02','P4-HF-09','P4-HF-16','P4-HF-31','P4-HF-36','P4-HF-37','P4-HF-40','P4-HF-45','P4-HF-46','P4-HF-48','P4-HF-53']);
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

entries.sort((a, b) => a.published_path.localeCompare(b.published_path));
const duplicatePublished = entries.filter((x, i) => entries.findIndex((y) => y.published_path === x.published_path) !== i);
if (duplicatePublished.length) throw new Error(`Duplicate published asset paths: ${duplicatePublished.map((x) => x.published_path).join(', ')}`);

const payload = {
  artifact_class: 'CTDE_WEB_ASSET_PUBLICATION_MANIFEST',
  schema_version: '1.0.0',
  baseline_commit: '478fd10f5b115c70f7b4b8ce5146ae2b6c6d37e5',
  strategy: 'Curated approved P4/P5 media; all 30 compressed animatics are online, while intermediate high-resolution renders and 711 individual SVG frames remain repository-only.',
  selected_hero_frame_ids: [...selectedHero].sort(),
  rejected_hero_frame_ids: ['P4-HF-19','P4-HF-29','P4-HF-34','P4-HF-39','P4-HF-43','P4-HF-44'],
  asset_count: entries.length,
  total_bytes: entries.reduce((n, x) => n + x.bytes, 0),
  assets: entries,
  status: 'APPROVED_PUBLIC_MEDIA_ALLOWLIST'
};

await writeFile(path.join(siteRoot, 'content/ASSET_PUBLICATION_MANIFEST.json'), `${JSON.stringify(payload, null, 2)}\n`);
console.log(JSON.stringify({ assets: payload.asset_count, total_bytes: payload.total_bytes, output: 'content/ASSET_PUBLICATION_MANIFEST.json' }));
