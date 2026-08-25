import { readdir, readFile, stat, writeFile } from 'node:fs/promises';
import { createHash } from 'node:crypto';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const output = path.join(root, 'P7B_ARTIFACT_MANIFEST.json');

async function walk(directory) {
  const rows = [];
  for (const entry of await readdir(directory, { withFileTypes: true })) {
    const absolute = path.join(directory, entry.name);
    if (entry.isDirectory()) rows.push(...await walk(absolute));
    else if (entry.isFile()) rows.push(absolute);
  }
  return rows;
}

const files = (await walk(root))
  .filter((file) => file !== output)
  .sort((a, b) => a.localeCompare(b));

const artifacts = [];
for (const file of files) {
  const bytes = await readFile(file);
  const metadata = await stat(file);
  artifacts.push({
    path: path.relative(root, file).split(path.sep).join('/'),
    bytes: metadata.size,
    sha256: createHash('sha256').update(bytes).digest('hex')
  });
}

const manifest = {
  artifact_class: 'ODYSSEY_P7B_ARTIFACT_MANIFEST',
  schema_version: '1.0.0',
  status: 'COMPLETE',
  source_baseline_commit: '912cdd6715fe5ae4fe82418b30035440938a9c17',
  user_rollout_authorization: 'CONFIRMED',
  real_reader_validation: 'NOT_CLAIMED',
  closure_policy: 'manifest excludes itself; all other files in this P7B directory are hashed',
  artifact_count: artifacts.length,
  artifacts
};

await writeFile(output, `${JSON.stringify(manifest, null, 2)}\n`);
console.log(JSON.stringify({ output, artifact_count: artifacts.length }, null, 2));
