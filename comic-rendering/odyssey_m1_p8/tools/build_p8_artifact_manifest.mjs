import { createHash } from 'node:crypto';
import { readdir, readFile, stat, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const outDir = path.resolve(here, '..');
const repoRoot = path.resolve(outDir, '..', '..');
const sha256 = (bytes) => createHash('sha256').update(bytes).digest('hex');
const rel = (absolute) => path.relative(repoRoot, absolute).split(path.sep).join('/');

async function walk(directory) {
  const entries = [];
  for (const name of await readdir(directory)) {
    if (name === 'candidate' || name === 'P8_ARTIFACT_MANIFEST.json') continue;
    const absolute = path.join(directory, name);
    const info = await stat(absolute);
    if (info.isDirectory()) entries.push(...await walk(absolute));
    else entries.push(absolute);
  }
  return entries;
}

const artifacts = [];
for (const absolute of (await walk(outDir)).sort()) {
  const bytes = await readFile(absolute);
  artifacts.push({ path:rel(absolute), bytes:bytes.length, sha256:sha256(bytes) });
}
const payload = {
  schema_version:'1.0.0', artifact_class:'P8_ARTIFACT_MANIFEST',
  status:'PASS_P8_ARTIFACT_IDENTITIES_FROZEN',
  source_baseline_commit:'9825a344e0e4d5984c7a996c5208b5938729bd8b',
  artifact_count:artifacts.length, total_bytes:artifacts.reduce((sum, item) => sum + item.bytes, 0), artifacts
};
await writeFile(path.join(outDir, 'P8_ARTIFACT_MANIFEST.json'), `${JSON.stringify(payload, null, 2)}\n`);
const manifestBytes = await readFile(path.join(outDir, 'P8_ARTIFACT_MANIFEST.json'));
console.log(JSON.stringify({ status:payload.status, artifacts:payload.artifact_count, total_bytes:payload.total_bytes, manifest_sha256:sha256(manifestBytes) }, null, 2));
