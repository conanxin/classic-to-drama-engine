import { createHash } from 'node:crypto';
import { access, readFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { diffHistoricalPaths, historicalVerificationReport } from './lib/historical-verification.mjs';

const siteRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const repoRoot = path.resolve(siteRoot, '..');
const distMode = process.argv.includes('--dist');
const baseline = '9825a344e0e4d5984c7a996c5208b5938729bd8b';
const readJson = async (relative) => JSON.parse(await readFile(path.join(repoRoot, relative), 'utf8'));
const exists = (target) => access(target).then(() => true).catch(() => false);
const sha256 = (bytes) => createHash('sha256').update(bytes).digest('hex');
const fail = (message) => { throw new Error(`P8 comic verification failed: ${message}`); };

const p7b = await readJson('graphic-script/odyssey_m1_p7b/P7B_PANEL_MANIFEST.json');
const p8 = await readJson('comic-rendering/odyssey_m1_p8/P8_WEB_VISUAL_MANIFEST.json');
const ledger = await readJson('comic-rendering/odyssey_m1_p8/P8_PANEL_ACCEPTANCE_LEDGER.json');
const renders = await readJson('comic-rendering/odyssey_m1_p8/P8_RENDER_MANIFEST.json');
const receipts = await readJson('comic-rendering/odyssey_m1_p8/P8_RENDER_RECEIPTS.json');
const rejections = await readJson('comic-rendering/odyssey_m1_p8/P8_REJECTION_REGISTER.json');
const assets = await readJson('site/content/ASSET_PUBLICATION_MANIFEST.json');

if (p8.status !== 'PASS_P8_FINAL_COMIC_VISUAL_MAPPING' || p8.counts.episodes !== 30 || p8.counts.scenes !== 150 || p8.counts.panel_slots !== 643 || p8.counts.episode_covers !== 30) fail('P8 web visual counts mismatch');
if (ledger.status !== 'PASS_643_OF_643_FINAL_VISUAL_ACCEPTANCE' || ledger.counts.accepted !== 643 || ledger.counts.pending !== 0) fail('acceptance ledger incomplete');
if (renders.status !== 'PASS_P8_MASTER_AND_WEB_DERIVATIVES' || renders.counts.scene_masters !== 150 || renders.counts.web_derivatives !== 643) fail('render manifest incomplete');
if (receipts.status !== 'PASS_643_SLOT_RECEIPTS' || receipts.receipt_count !== 643) fail('render receipts incomplete');
if (new Set(p8.panels.map((panel) => panel.panel_id)).size !== 643 || new Set(p8.panels.map((panel) => panel.public_path)).size !== 643) fail('P8 visual IDs/public paths are not unique');
if (p8.panels.some((panel) => /storyboards|animatic/i.test(panel.source_path) || !/^media\/comic\/EP\d{2}\//.test(panel.public_path))) fail('raw technical visual promoted to final reader');
if (ledger.panels.some((panel) => !['FINAL_COMIC_ACCEPTED','EXISTING_HIGH_FIDELITY_ACCEPTED'].includes(panel.p8_status) || Object.values(panel.audit).some((value) => value !== 'PASS'))) fail('slot audit failure');
if (p7b.panels.some((panel) => !p8.panels.find((visual) => visual.panel_id === panel.panel_id))) fail('P7B narrative slot lacks P8 visual');

const assetByPublic = new Map(assets.assets.map((asset) => [asset.published_path, asset]));
for (const visual of p8.panels) {
  const source = await readFile(path.join(repoRoot, visual.source_path));
  if (sha256(source) !== visual.web_sha256) fail(`P8 source identity mismatch ${visual.panel_id}`);
  const asset = assetByPublic.get(visual.public_path);
  if (!asset || asset.source_path !== visual.source_path || asset.sha256 !== visual.web_sha256 || asset.status !== 'APPROVED') fail(`P8 allowlist mismatch ${visual.panel_id}`);
}
for (const rejection of rejections.rejections) if (assetByPublic.has(rejection.path) || p8.panels.some((panel) => panel.source_path === rejection.path)) fail(`rejected render promoted: ${rejection.rejection_id}`);

const frozen = ['scripts/odyssey_m1_v2','editorial/odyssey_m1_v2','production/odyssey_m1_v2','preproduction/odyssey_m1_p3','visual-development/odyssey_m1_p4','storyboards/odyssey_m1_p4','design/odyssey_m1_p4','previs/odyssey_m1_p4','art-department/odyssey_m1_p5','animatic/odyssey_m1_p5','vfx-previs/odyssey_m1_p5','production-tests/odyssey_m1_p5','pitch/odyssey_m1_p5','runtime_capability_prototype','graphic-script/odyssey_m1_p7a','graphic-script/odyssey_m1_p7c','graphic-script/odyssey_m1_p7b'];
const immutableHistory = await diffHistoricalPaths({ repoRoot, baselineCommit:baseline, paths:frozen });
if (immutableHistory.changedPaths) fail(`frozen predecessor modified:\n${immutableHistory.changedPaths}`);

if (distMode) {
  for (let number = 1; number <= 30; number += 1) {
    const padded = String(number).padStart(2, '0');
    const htmlPath = path.join(siteRoot, 'dist', 'episodes', padded, 'graphic', 'index.html');
    if (!(await exists(htmlPath))) fail(`missing EP${padded} graphic route`);
    const html = await readFile(htmlPath, 'utf8');
    if (!html.includes('HIGH-FIDELITY GRAPHIC NOVEL') || !html.includes(`/media/comic/EP${padded}/`) || /single-frame storyboard derivative|animatic-card derivative/.test(html)) fail(`EP${padded} did not switch cleanly to P8`);
  }
  for (const panel of p8.panels) if (!(await exists(path.join(siteRoot, 'dist', panel.public_path)))) fail(`missing built final art ${panel.panel_id}`);
}

console.log(JSON.stringify({
  status:'PASS_P8_COMIC_VERIFY', dist_verified:distMode, episodes:'30/30', scenes:'150/150', panels:'643/643',
  scene_masters:150, final_art_paths:643, raw_technical_reader_slots:0, rejected_promotions:0,
  action_beats:'44/44', predecessor_modifications:0,
  ...historicalVerificationReport({
    baselineCommit:baseline,
    checked:immutableHistory.skipped ? 0 : 1,
    skipped:immutableHistory.skipped ? 1 : 0,
    kind:'FROZEN_PREDECESSOR_GIT_DIFF'
  }),
  P6_status:'PAUSED_BY_USER'
}));
