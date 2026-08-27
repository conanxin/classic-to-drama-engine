import { createHash } from 'node:crypto';
import { access, readFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const siteRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const repoRoot = path.resolve(siteRoot, '..');
const hasDist = process.argv.includes('--dist');
const readJson = async (root, relative) => JSON.parse(await readFile(path.join(root, relative), 'utf8'));
const exists = (target) => access(target).then(() => true).catch(() => false);
const hash = (bytes) => createHash('sha256').update(bytes).digest('hex');
const fail = (message) => { throw new Error(message); };

const generated = await readJson(siteRoot, 'src/generated/publication.json');
const config = await readJson(repoRoot, 'publication/odyssey_m1_p9/publication-config.json');
const architecture = await readJson(repoRoot, 'publication/odyssey_m1_p9/P9_VOLUME_ARCHITECTURE.json');
const pageManifest = await readJson(repoRoot, 'publication/odyssey_m1_p9/P9_PAGE_MANIFEST.json');
const exportsManifest = await readJson(repoRoot, 'publication/odyssey_m1_p9/P9_EXPORT_MANIFEST.json');
const assetManifest = await readJson(siteRoot, 'content/ASSET_PUBLICATION_MANIFEST.json');

if (generated.volumes.length !== 5 || generated.counts.chapters !== 30 || generated.counts.scenes !== 150 || generated.counts.panels !== 643) fail('P9 generated coverage mismatch');
if (architecture.status !== 'PASS_P9_VOLUME_ARCHITECTURE' || pageManifest.counts.source_panels !== 643) fail('P9 publication authority incomplete');
if (exportsManifest.status !== 'PASS_P9_EXPORTS_VALIDATED' || exportsManifest.exports.length !== 21) fail('P9 export manifest incomplete');
if (exportsManifest.counts.PDF !== 11 || exportsManifest.counts.EPUB !== 5 || exportsManifest.counts.CBZ !== 5) fail('P9 format count mismatch');
if (generated.print_status !== 'PRINT_LAYOUT_MASTER' || generated.press_ready !== 'NOT_CLAIMED') fail('P9 print boundary mismatch');
if (generated.release_tag !== config.series.release_tag) fail('P9 release identity mismatch');

const exportNames = new Set(exportsManifest.exports.map((item) => item.filename));
for (const volume of generated.volumes) {
  if (volume.chapters.length !== volume.episode_end - volume.episode_start + 1) fail(`P9 chapter range mismatch ${volume.id}`);
  for (const item of Object.values(volume.downloads)) {
    if (!exportNames.has(item.filename) || !item.url.includes(`/${generated.release_tag}/`)) fail(`P9 download mapping mismatch ${item.filename}`);
  }
}

const p9Covers = assetManifest.assets.filter((asset) => asset.published_path.startsWith('media/publication/covers/'));
if (p9Covers.length !== 5 || p9Covers.some((asset) => asset.status !== 'APPROVED')) fail('P9 cover allowlist mismatch');
for (const cover of p9Covers) {
  const bytes = await readFile(path.join(repoRoot, cover.source_path));
  if (bytes.length !== cover.bytes || hash(bytes) !== cover.sha256) fail(`P9 cover identity mismatch ${cover.source_path}`);
}

// The large validated outputs intentionally live outside Git. Local QA checks
// their bytes when present; CI relies on the frozen export manifest and Release.
for (const item of exportsManifest.exports) {
  const local = path.join(repoRoot, item.repository_path);
  if (await exists(local)) {
    const bytes = await readFile(local);
    if (bytes.length !== item.bytes || hash(bytes) !== item.sha256) fail(`P9 local export identity mismatch ${item.filename}`);
  }
}

if (hasDist) {
  const page = path.join(siteRoot, 'dist/publication/index.html');
  if (!(await exists(page))) fail('P9 publication route missing');
  const html = await readFile(page, 'utf8');
  for (const probe of ['把三十集归途', 'Digital PDF', 'EPUB 3', 'CBZ', 'PRINT_LAYOUT_MASTER: PASS', 'PRESS_READY: NOT_CLAIMED']) {
    if (!html.includes(probe)) fail(`P9 publication page probe failed: ${probe}`);
  }
  if (/\/home\/conanxin\/|C:\\Users\\|\\\\wsl\$/i.test(html)) fail('P9 publication page leaks internal path');
  for (let number = 1; number <= 5; number += 1) {
    const volume = `v${String(number).padStart(2, '0')}`;
    for (const suffix of ['', '-w720', '-w1600']) {
      const file = `media/publication/covers/odyssey-homecoming-${volume}-cover${suffix}.webp`;
      if (!(await exists(path.join(siteRoot, 'dist', file)))) fail(`P9 published cover missing ${file}`);
    }
  }
}

console.log(JSON.stringify({
  status: 'PASS_P9_WEB_PUBLICATION_VERIFY',
  dist_verified: hasDist,
  volumes: generated.volumes.length,
  chapters: generated.counts.chapters,
  scenes: generated.counts.scenes,
  panels: generated.counts.panels,
  exports: exportsManifest.exports.length,
  publication_covers: p9Covers.length,
  press_ready: generated.press_ready
}));
