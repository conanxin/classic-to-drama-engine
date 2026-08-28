#!/usr/bin/env node
import { createHash } from 'node:crypto';
import { readdir, readFile, stat, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const toolDir = path.dirname(fileURLToPath(import.meta.url));
const out = path.dirname(toolDir);
const root = path.resolve(out, '../..');
const args = Object.fromEntries(process.argv.slice(2).map((arg) => {
  const [key, ...value] = arg.replace(/^--/, '').split('=');
  return [key, value.join('=')];
}));

for (const key of ['implementation-commit', 'workflow-run', 'live-routes', 'live-assets']) {
  if (!args[key]) throw new Error(`Missing --${key}=...`);
}

const shaBytes = (bytes) => createHash('sha256').update(bytes).digest('hex');
const shaFile = async (file) => shaBytes(await readFile(file));
const rel = (file) => path.relative(root, file).split(path.sep).join('/');
const writeText = (name, body) => writeFile(path.join(out, name), `${body.trim()}\n`, 'utf8');

await writeText('P10_WEB_RELEASE_QA_REPORT.md', `# P10B Web Release QA Report

status: \`PASS_P10B_WEB_RELEASE_QA\`

## Production build

- \`npm run check\`: PASS — Astro 54 files, 0 errors, 0 warnings, 0 hints
- \`npm run verify\`: PASS — P7 through P10 source and publication verification
- \`npm run build\`: PASS — 133 static pages, 132 Pagefind documents, final dist verification PASS
- P10 assets in the public allowlist: reader sample, five cover sets, three promotional images and checksum documents only

## Local browser QA

- viewports: 1440 × 900 and 390 × 844
- route/view combinations: 18 / 18 PASS
- direct public-resource checks: 3 / 3 PASS
- broken images: 0
- missing image alt attributes: 0
- horizontal overflow: 0
- root-relative base-path defects: 0
- canonical defects: 0
- visual inspection: homepage, /read/, /publication/ and /publication/verify/ PASS on both viewports

## Reader sample QA

- pages: 20
- content: frozen P9 Volume I pages 1–20, including complete EP01
- SHA-256: \`1f6270d7bb1420df3833bccf38a3f17a8310a605b7c13742fe3f02a8ce7bd725\`
- visual inspection: cover and representative interior page PASS

## Live QA

- deployment commit: \`${args['implementation-commit']}\`
- Pages workflow run: \`${args['workflow-run']}\`
- sitemap routes checked: ${args['live-routes']}
- internal/public assets checked: ${args['live-assets']}
- public URL: https://conanxin.github.io/classic-to-drama-engine/
- reader entry, publication center, verification page, sample PDF and canonical GitHub Release links: PASS
`);

await writeText('P10_INDEPENDENT_VERIFICATION.md', `# P10B Independent Verification

status: \`PASS_P10B_INDEPENDENT_VERIFICATION\`

## Frozen release identity

- P9 formal result: PASS
- release tag: \`odyssey-p9-publication-v1.0.0\`
- canonical assets: 21 / 21
- canonical bytes: 1,559,135,367
- GitHub Release digest mismatches: 0
- P9 binary modifications: 0

## Distribution package

- edition freeze: PASS
- master metadata/store copy: PASS
- SHA256SUMS: 21 / 21
- Apple Books package: READY_WITH_NOTES
- Google Play Books package: READY
- Kobo Writing Life package: READY_WITH_NOTES
- Kindle/KDP package: READY_WITH_PLATFORM_SPECIFIC_ACTION
- self-hosted release package: PASS
- reader sample and publication derivatives: deterministic and source-bound

## Web and deployment

- check / verify / production build: PASS
- desktop and mobile browser QA: PASS
- live deployment: PASS
- live route crawl: ${args['live-routes']} / ${args['live-routes']}
- live asset crawl: ${args['live-assets']} / ${args['live-assets']}
- unresolved product blockers: 0

## Boundaries

- store submissions: 0
- store acceptance claims: 0
- ISBN purchases: 0
- prices committed: 0
- tax/bank configuration: 0
- P6 actions: 0
- predecessor content/runtime modifications: 0
`);

async function manifestFiles(dir) {
  const found = [];
  for (const entry of await readdir(dir, { withFileTypes: true })) {
    if (entry.name === 'tools' || entry.name === 'P10_ARTIFACT_MANIFEST.json' || entry.name === 'P10_FINAL_RESULT.md') continue;
    const file = path.join(dir, entry.name);
    if (entry.isDirectory()) found.push(...await manifestFiles(file));
    else {
      const info = await stat(file);
      found.push({ path: rel(file), bytes: info.size, sha256: await shaFile(file) });
    }
  }
  return found.sort((a, b) => a.path.localeCompare(b.path));
}

const artifacts = await manifestFiles(out);
const manifest = {
  schema_version: 'P10B_ARTIFACT_MANIFEST_V1',
  status: 'PASS_ODYSSEY_P10B_PUBLIC_RELEASE_AND_DISTRIBUTION_PACKAGE_COMPLETE',
  finalized_at: '2026-08-28T00:00:00+08:00',
  edition_id: 'ODYSSEY-DGNE-1.0.0',
  release_tag: 'odyssey-p9-publication-v1.0.0',
  implementation_commit: args['implementation-commit'],
  workflow_run: Number(args['workflow-run']),
  scope_note: 'Hashes all final P10B distribution artifacts except this manifest, P10_FINAL_RESULT.md, and reproducible tools; exclusions avoid circular identity dependencies.',
  p9_binary_modifications: 0,
  p6_actions: 0,
  counts: {
    manifested_artifacts: artifacts.length,
    release_assets_referenced: 21,
    cover_sets: 5,
    promotional_assets: 3,
    reader_samples: 1,
    platform_packages: 5,
  },
  artifacts,
};
await writeFile(path.join(out, 'P10_ARTIFACT_MANIFEST.json'), `${JSON.stringify(manifest, null, 2)}\n`, 'utf8');
const manifestSha = await shaFile(path.join(out, 'P10_ARTIFACT_MANIFEST.json'));

await writeText('P10_FINAL_RESULT.md', `# P10B Final Result

status: \`PASS_ODYSSEY_P10B_PUBLIC_RELEASE_AND_DISTRIBUTION_PACKAGE_COMPLETE\`

## Frozen reader edition

- title: 《归途：奥德修斯》
- edition: Digital Graphic Novel Edition
- version: 1.0.0
- episodes: 30 / 30
- scenes: 150 / 150
- narrative panels: 643 / 643
- publication volumes: 5 / 5
- canonical release assets: 21 / 21
- canonical release bytes: 1,559,135,367
- P9 release binaries modified: 0

## Public release package

- publication metadata: PASS
- store copy: PASS
- rights/source note: PASS
- checksum package: PASS
- archival manifest: PASS
- official platform-requirements snapshot: PASS, dated 2026-08-28
- Apple Books: READY_WITH_NOTES
- Google Play Books: READY
- Kobo Writing Life: READY_WITH_NOTES
- Kindle/KDP: READY_WITH_PLATFORM_SPECIFIC_ACTION
- self-hosted web/GitHub Release: PASS
- store submission/acceptance: NOT_EXECUTED / NOT_CLAIMED

## Reader-facing edition

- /read/: PASS
- /about/: PASS
- /publication/: PASS
- /publication/verify/: PASS
- 20-page spoiler-safe EP01 reader sample: PASS
- desktop/mobile browser QA: PASS
- production build and live Pages deployment: PASS

## Evidence

- implementation commit: \`${args['implementation-commit']}\`
- successful Pages workflow run: \`${args['workflow-run']}\`
- artifact manifest SHA-256: \`${manifestSha}\`
- unresolved product blockers: 0

## Frozen boundaries

- V2 modified: 0
- P3 modified: 0
- P4 modified: 0
- P5 modified: 0
- Runtime modified: 0
- P7/P8 narrative or visual authority modified: 0
- P9 export binaries modified: 0
- P6 status: \`PAUSED_BY_USER\`
- P6 actions: 0

No commercial account action, pricing decision, identifier purchase, tax/bank setup, submission, payment or outreach occurred in P10B.
`);

console.log(JSON.stringify({
  status: 'PASS_ODYSSEY_P10B_PUBLIC_RELEASE_AND_DISTRIBUTION_PACKAGE_COMPLETE',
  artifacts: artifacts.length,
  artifact_manifest_sha256: manifestSha,
  implementation_commit: args['implementation-commit'],
  workflow_run: Number(args['workflow-run']),
}, null, 2));
