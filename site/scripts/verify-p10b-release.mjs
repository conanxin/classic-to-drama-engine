#!/usr/bin/env node
import { createHash } from 'node:crypto';
import { readFile, stat } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const siteRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const root = path.resolve(siteRoot, '..');
const distMode = process.argv.includes('--dist');
const json = async (rel) => JSON.parse(await readFile(path.join(root,rel),'utf8'));
const exists = async (file) => { try { await stat(file); return true; } catch { return false; } };
const sha = (bytes) => createHash('sha256').update(bytes).digest('hex');
const fail = (message) => { console.error(`P10B VERIFY FAIL: ${message}`); process.exit(1); };

const freeze = await json('distribution/odyssey_m1_p10b/P10_EDITION_FREEZE.json');
const sums = await json('distribution/odyssey_m1_p10b/SHA256SUMS.json');
const release = await json('distribution/odyssey_m1_p10b/P10_RELEASE_ASSET_VERIFICATION.json');
const p9 = await json('publication/odyssey_m1_p9/P9_EXPORT_MANIFEST.json');
const requirements = await json('distribution/odyssey_m1_p10b/P10_PLATFORM_REQUIREMENTS_SNAPSHOT.json');
const metadata = await json('distribution/odyssey_m1_p10b/P10_METADATA_MASTER.json');
const matrix = await json('distribution/odyssey_m1_p10b/P10_DISTRIBUTION_MATRIX.json');
const media = await json('distribution/odyssey_m1_p10b/media/media-manifest.json');
if (freeze.status !== 'PASS_P10B_EDITION_FREEZE' || freeze.volumes !== 5 || freeze.chapters !== 30 || freeze.publication_pages !== 458 || freeze.source_panels !== 643) fail('edition freeze mismatch');
if (sums.asset_count !== 21 || sums.total_bytes !== 1559135367 || p9.exports.length !== 21) fail('release asset count/bytes mismatch');
for (const item of sums.assets) {
  const source = p9.exports.find((candidate) => candidate.filename === item.filename);
  if (!source || source.bytes !== item.bytes || source.sha256 !== item.sha256) fail(`checksum mismatch ${item.filename}`);
}
if (release.status !== 'PASS_P10B_CANONICAL_RELEASE_INTEGRITY' || release.observed_assets !== 21 || release.github_digest_present !== 21 || release.mismatches.length) fail('captured GitHub release evidence mismatch');
if (requirements.status !== 'PASS_P10B_OFFICIAL_REQUIREMENTS_SNAPSHOT' || Object.keys(requirements.platforms).length !== 4) fail('official platform snapshot mismatch');
if (metadata.volumes.length !== 5 || metadata.isbn !== 'NOT_ASSIGNED' || metadata.publisher !== 'NOT_CLAIMED') fail('metadata boundary mismatch');
if (matrix.channels.length !== 6 || matrix.channels.filter((c)=>c.submission_status === 'NOT_EXECUTED').length !== 4) fail('distribution matrix mismatch');
if (media.status !== 'PASS_P10B_DETERMINISTIC_MEDIA' || media.covers.length !== 5 || media.promotional.length !== 3 || media.sample.pages !== 20) fail('media manifest mismatch');
const sample = path.join(root,media.sample.path);
const sampleBytes = await readFile(sample);
if (sampleBytes.length !== media.sample.bytes || sha(sampleBytes) !== media.sample.sha256) fail('sample identity mismatch');
for (const cover of media.covers) for (const file of cover.files) {
  const bytes = await readFile(path.join(root,file.path));
  if (bytes.length !== file.bytes || sha(bytes) !== file.sha256) fail(`cover derivative mismatch ${file.path}`);
}
const required = ['P10_RELEASE_BIBLE.md','P10_RIGHTS_AND_SOURCE_NOTE.md','P10_KINDLE_COMPATIBILITY_REPORT.md','P10_PRESS_KIT.json','P10_ARCHIVAL_MANIFEST.json','P10_PLATFORM_PACKAGE_QA.md','P10_MANUAL_SUBMISSION_CHECKLIST.md','CITATION.cff'];
for (const name of required) if (!(await exists(path.join(root,'distribution/odyssey_m1_p10b',name)))) fail(`missing ${name}`);
for (const slug of ['apple-books','google-play-books','kobo-writing-life','kindle-kdp','self-hosted']) {
  for (const name of ['package-manifest.json','metadata.json','metadata-readable.md','SUBMISSION_CHECKLIST.md']) if (!(await exists(path.join(root,'distribution/odyssey_m1_p10b/packages',slug,name)))) fail(`missing package ${slug}/${name}`);
}
if (distMode) {
  for (const route of ['index.html','read/index.html','about/index.html','publication/index.html','publication/verify/index.html','episodes/01/graphic/index.html','episodes/30/graphic/index.html','project/index.html']) {
    const file = path.join(siteRoot,'dist',route);
    if (!(await exists(file))) fail(`missing dist route ${route}`);
    const html = await readFile(file,'utf8');
    if (/\/home\/conanxin\/|C:\\Users\\|API[_-]?KEY|BEGIN PRIVATE KEY/i.test(html)) fail(`privacy leak ${route}`);
  }
  for (const name of ['odyssey-homecoming-reader-sample-v1.0.0.pdf','SHA256SUMS.txt','SHA256SUMS.json']) if (!(await exists(path.join(siteRoot,'dist/media/publication/p10',name)))) fail(`missing public P10B asset ${name}`);
}
console.log(JSON.stringify({status:'PASS_P10B_RELEASE_VERIFY',dist_mode:distMode,release_assets:21,release_bytes:sums.total_bytes,volumes:5,platforms:4,sample_sha256:media.sample.sha256},null,2));
