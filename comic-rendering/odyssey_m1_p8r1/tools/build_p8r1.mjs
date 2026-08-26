import { createHash } from 'node:crypto';
import { mkdir, readFile, readdir, stat, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import sharp from '../../../site/node_modules/sharp/dist/index.mjs';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../..');
const base = path.join(root, 'comic-rendering/odyssey_m1_p8r1');
const configPath = path.join(base, 'P8R1_EP01_COMIC_GRAMMAR.json');
const config = JSON.parse(await readFile(configPath, 'utf8'));
const hash = (bytes) => createHash('sha256').update(bytes).digest('hex');
const relative = (value) => path.join(root, value);

await mkdir(path.join(base, 'web/EP01'), { recursive: true });
const visuals = [];
for (const entry of config.visual_overrides) {
  const masterBytes = await readFile(relative(entry.master_path));
  const webTarget = relative(entry.web_path);
  await sharp(masterBytes).resize({ width: 1600, withoutEnlargement: true }).webp({ quality: 84, effort: 5 }).toFile(webTarget);
  const webBytes = await readFile(webTarget);
  const masterMeta = await sharp(masterBytes).metadata();
  const webMeta = await sharp(webBytes).metadata();
  visuals.push({
    panel_id: entry.panel_id,
    version: entry.version,
    source_kind: 'P8R1_EP01_FINAL_COMIC_ART',
    source_path: entry.web_path,
    master_path: entry.master_path,
    public_path: entry.public_path,
    authority: entry.authority,
    source_status: 'APPROVED_EP01_R1',
    alt: entry.alt,
    visible_action: entry.visible_action,
    master: { bytes: masterBytes.length, sha256: hash(masterBytes), width: masterMeta.width, height: masterMeta.height },
    web: { bytes: webBytes.length, sha256: hash(webBytes), width: webMeta.width, height: webMeta.height }
  });
}

const rejected = [];
for (const entry of config.rejected_versions) {
  const bytes = await readFile(relative(entry.path));
  rejected.push({ ...entry, bytes: bytes.length, sha256: hash(bytes), publication_status: 'REJECTED_NOT_PUBLISHED' });
}

const visualManifest = {
  artifact_class: 'ODYSSEY_P8R1_EP01_VISUAL_OVERRIDE_MANIFEST',
  schema_version: '1.0.0',
  episode: 'EP01',
  visual_override_count: visuals.length,
  panels: visuals,
  status: 'PASS_P8R1_EP01_VISUAL_OVERRIDES'
};
const rejectionRegister = {
  artifact_class: 'ODYSSEY_P8R1_EP01_REJECTION_REGISTER',
  schema_version: '1.0.0',
  episode: 'EP01',
  rejection_count: rejected.length,
  rejected,
  status: 'REJECTED_ASSETS_EXCLUDED_FROM_PUBLICATION'
};
await writeFile(path.join(base, 'P8R1_EP01_VISUAL_OVERRIDE_MANIFEST.json'), `${JSON.stringify(visualManifest, null, 2)}\n`);
await writeFile(path.join(base, 'P8R1_REJECTION_REGISTER.json'), `${JSON.stringify(rejectionRegister, null, 2)}\n`);

const artifactPaths = [];
async function walk(directory) {
  for (const name of await readdir(directory)) {
    const target = path.join(directory, name);
    const info = await stat(target);
    if (info.isDirectory()) await walk(target);
    else if (name !== 'P8R1_ARTIFACT_MANIFEST.json') artifactPaths.push(target);
  }
}
await walk(base);
const artifacts = [];
for (const target of artifactPaths.sort()) {
  const bytes = await readFile(target);
  artifacts.push({ path:path.relative(root, target).replaceAll(path.sep, '/'), bytes:bytes.length, sha256:hash(bytes) });
}
await writeFile(path.join(base, 'P8R1_ARTIFACT_MANIFEST.json'), `${JSON.stringify({
  artifact_class:'ODYSSEY_P8R1_ARTIFACT_MANIFEST',
  schema_version:'1.0.0',
  repair_id:'ODYSSEY-P8R1',
  episode:'EP01',
  artifact_count:artifacts.length,
  artifacts,
  status:'PASS_EP01_COMIC_READING_GRAMMAR',
  P8_final_closeout:'NOT_EXECUTED',
  P6_status:'PAUSED_BY_USER'
}, null, 2)}\n`);

const configInfo = await stat(configPath);
console.log(JSON.stringify({ episode: 'EP01', visual_overrides: visuals.length, rejections: rejected.length, artifacts:artifacts.length, config_bytes: configInfo.size }));
