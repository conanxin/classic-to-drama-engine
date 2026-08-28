#!/usr/bin/env node
import { createHash } from 'node:crypto';
import { readFile, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, '../../..');
const tag = 'odyssey-p9-publication-v1.0.0';
const manifest = JSON.parse(await readFile(path.join(root, 'publication/odyssey_m1_p9/P9_EXPORT_MANIFEST.json'), 'utf8'));
const response = await fetch(`https://api.github.com/repos/conanxin/classic-to-drama-engine/releases/tags/${tag}`, { headers: { Accept:'application/vnd.github+json', 'User-Agent':'ctde-p10b-verifier' } });
if (!response.ok) throw new Error(`GitHub release API ${response.status}`);
const release = await response.json();
const expected = new Map(manifest.exports.map((item) => [item.filename, item]));
const observed = release.assets.map((asset) => ({
  filename: asset.name, bytes: asset.size, sha256: String(asset.digest || '').replace(/^sha256:/,''), url: asset.browser_download_url,
})).sort((a,b) => a.filename.localeCompare(b.filename));
const mismatches = [];
for (const asset of observed) {
  const item = expected.get(asset.filename);
  if (!item) mismatches.push({ filename:asset.filename, reason:'unexpected asset' });
  else if (item.bytes !== asset.bytes || item.sha256 !== asset.sha256) mismatches.push({ filename:asset.filename, reason:'size or SHA-256 mismatch', expected:{bytes:item.bytes,sha256:item.sha256}, observed:asset });
}
for (const name of expected.keys()) if (!observed.some((item) => item.filename === name)) mismatches.push({filename:name, reason:'missing asset'});
const result = {
  schema_version:'P10B_RELEASE_ASSET_VERIFICATION_V1',
  status:mismatches.length ? 'BLOCK_P10B_RELEASE_INTEGRITY' : 'PASS_P10B_CANONICAL_RELEASE_INTEGRITY',
  verified_at:'2026-08-28T00:00:00+08:00',
  release:{tag_name:release.tag_name,target_commitish:release.target_commitish,published_at:release.published_at,html_url:release.html_url,draft:release.draft,prerelease:release.prerelease},
  expected_assets:expected.size, observed_assets:observed.length, observed_bytes:observed.reduce((sum,item)=>sum+item.bytes,0), github_digest_present:observed.filter((item)=>item.sha256.length===64).length,
  assets:observed, mismatches,
};
const bytes = `${JSON.stringify(result,null,2)}\n`;
await writeFile(path.join(root,'distribution/odyssey_m1_p10b/P10_RELEASE_ASSET_VERIFICATION.json'),bytes,'utf8');
console.log(JSON.stringify({...result,assets:undefined,verification_sha256:createHash('sha256').update(bytes).digest('hex')},null,2));
if (mismatches.length) process.exit(1);
