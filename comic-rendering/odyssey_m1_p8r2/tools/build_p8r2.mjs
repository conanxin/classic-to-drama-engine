import { createHash } from 'node:crypto';
import { readFile, readdir, stat, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../..');
const base = path.join(root, 'comic-rendering/odyssey_m1_p8r2');
const hash = (bytes) => createHash('sha256').update(bytes).digest('hex');
const grammar = JSON.parse(await readFile(path.join(base, 'P8R2_EP01_FINAL_GRAMMAR.json'), 'utf8'));
if (grammar.status !== 'PASS_EP01_FINAL_COMIC_GRAMMAR_LOCK') throw new Error('P8R2 grammar status mismatch');
if (grammar.preserved.narrative_slots !== 17 || grammar.preserved.art_newly_generated !== 0) throw new Error('P8R2 preservation mismatch');

const targets = [];
async function walk(directory) {
  for (const name of await readdir(directory)) {
    const target = path.join(directory, name);
    const info = await stat(target);
    if (info.isDirectory()) await walk(target);
    else if (name !== 'P8R2_ARTIFACT_MANIFEST.json') targets.push(target);
  }
}
await walk(base);
const artifacts = [];
for (const target of targets.sort()) {
  const bytes = await readFile(target);
  artifacts.push({ path:path.relative(root, target).replaceAll(path.sep, '/'), bytes:bytes.length, sha256:hash(bytes) });
}
await writeFile(path.join(base, 'P8R2_ARTIFACT_MANIFEST.json'), `${JSON.stringify({
  artifact_class:'ODYSSEY_P8R2_ARTIFACT_MANIFEST',
  schema_version:'1.0.0',
  repair_id:'ODYSSEY-P8R2',
  episode:'EP01',
  artifact_count:artifacts.length,
  artifacts,
  status:'PASS_EP01_FINAL_COMIC_GRAMMAR_LOCK',
  comic_grammar_propagation:'NOT_AUTHORIZED',
  P8_final_closeout:'NOT_EXECUTED',
  P6_status:'PAUSED_BY_USER'
}, null, 2)}\n`);
console.log(JSON.stringify({ episode:'EP01', scenes:5, panels:17, art_reused:17, art_newly_generated:0, artifacts:artifacts.length }));
