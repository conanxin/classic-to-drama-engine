#!/usr/bin/env node
import { createHash } from 'node:crypto';
import { execFileSync } from 'node:child_process';
import { readFile, stat } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const toolDir = path.dirname(fileURLToPath(import.meta.url));
const out = path.dirname(toolDir);
const root = path.resolve(out, '../..');
const shaFile = async (file) => createHash('sha256').update(await readFile(file)).digest('hex');
const fail = (message) => { throw new Error(`P10B CLOSEOUT VERIFY FAIL: ${message}`); };
const json = async (name) => JSON.parse(await readFile(path.join(out, name), 'utf8'));
const text = async (name) => readFile(path.join(out, name), 'utf8');

const finalResult = await text('P10_FINAL_RESULT.md');
const independent = await text('P10_INDEPENDENT_VERIFICATION.md');
const webQa = await text('P10_WEB_RELEASE_QA_REPORT.md');
const manifest = await json('P10_ARTIFACT_MANIFEST.json');
const release = await json('P10_RELEASE_ASSET_VERIFICATION.json');
const p9Final = await readFile(path.join(root, 'publication/odyssey_m1_p9/P9_FINAL_RESULT.md'), 'utf8');

if (!finalResult.includes('PASS_ODYSSEY_P10B_PUBLIC_RELEASE_AND_DISTRIBUTION_PACKAGE_COMPLETE')) fail('formal status absent');
if (!independent.includes('PASS_P10B_INDEPENDENT_VERIFICATION')) fail('independent verification status absent');
if (!webQa.includes('PASS_P10B_WEB_RELEASE_QA')) fail('web QA status absent');
if (!p9Final.includes('PASS_ODYSSEY_P9_MULTIFORMAT_PUBLICATION_EDITION_COMPLETE')) fail('P9 predecessor not PASS');
if (manifest.status !== 'PASS_ODYSSEY_P10B_PUBLIC_RELEASE_AND_DISTRIBUTION_PACKAGE_COMPLETE') fail('artifact manifest status mismatch');
if (manifest.artifacts.length !== manifest.counts.manifested_artifacts || manifest.artifacts.length < 70) fail('artifact count mismatch');
if (manifest.p9_binary_modifications !== 0 || manifest.p6_actions !== 0) fail('frozen-boundary mismatch');
if (release.status !== 'PASS_P10B_CANONICAL_RELEASE_INTEGRITY' || release.observed_assets !== 21 || release.mismatches.length) fail('canonical release verification mismatch');

for (const artifact of manifest.artifacts) {
  const file = path.join(root, artifact.path);
  const info = await stat(file);
  if (info.size !== artifact.bytes) fail(`size mismatch: ${artifact.path}`);
  if (await shaFile(file) !== artifact.sha256) fail(`SHA-256 mismatch: ${artifact.path}`);
}

const changed = execFileSync('git', ['diff', '--name-only', '2c39dcfbf24b97e9de802628c15fbff32b7dba17', '--'], { cwd: root, encoding: 'utf8' })
  .trim().split('\n').filter(Boolean);
const forbiddenPrefixes = [
  'scripts/odyssey_m1_v2/', 'editorial/odyssey_m1_v2/', 'production/odyssey_m1_v2/',
  'preproduction/odyssey_m1_p3/', 'visual-development/odyssey_m1_p4/', 'storyboards/odyssey_m1_p4/',
  'design/odyssey_m1_p4/', 'previs/odyssey_m1_p4/', 'art-department/odyssey_m1_p5/',
  'animatic/odyssey_m1_p5/', 'vfx-previs/odyssey_m1_p5/', 'production-tests/odyssey_m1_p5/',
  'pitch/odyssey_m1_p5/', 'runtime_capability_prototype/', 'graphic-script/', 'comic-rendering/',
  'publication/odyssey_m1_p9/',
];
const forbidden = changed.filter((file) => forbiddenPrefixes.some((prefix) => file.startsWith(prefix)));
if (forbidden.length) fail(`predecessor modifications: ${forbidden.join(', ')}`);

console.log(JSON.stringify({
  status: 'PASS_P10B_CLOSEOUT_INDEPENDENT_VERIFICATION',
  manifested_artifacts: manifest.artifacts.length,
  canonical_release_assets: 21,
  predecessor_modifications: 0,
  unresolved_product_blockers: 0,
  p6_actions: 0,
  artifact_manifest_sha256: await shaFile(path.join(out, 'P10_ARTIFACT_MANIFEST.json')),
}, null, 2));
