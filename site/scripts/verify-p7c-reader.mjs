import { access, readFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const siteRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const repoRoot = path.resolve(siteRoot, '..');
const distMode = process.argv.includes('--dist');
const fail = (message) => { throw new Error('P7C reader verification failed: ' + message); };
const exists = (target) => access(target).then(() => true).catch(() => false);
const readRepo = (relative) => readFile(path.join(repoRoot, relative), 'utf8');
const readJson = async (relative) => JSON.parse(await readRepo(relative));

const requiredDocs = [
  'P7C_READER_RESEARCH_PLAN.md','P7C_SUCCESS_CRITERIA.md','P7C_TEST_PROTOCOL.md','P7C_PARTICIPANT_INSTRUCTIONS.md',
  'P7C_FACILITATOR_GUIDE.md','P7C_DATA_SCHEMA.json','P7C_RESULT_TEMPLATE.json','P7C_RESULT_ANALYSIS.md','P7C_PRIVACY_NOTE.md',
  'P7C_COGNITIVE_LOAD_AUDIT.md','CHARACTER_INTRODUCTION_BUDGET.md','P7C_VISUAL_NARRATIVE_AUDIT.md','P7B_SCALE_COST_MODEL.md','P7B_ROLLOUT_DECISION.md'
];
for (const file of requiredDocs) if (!(await exists(path.join(repoRoot, 'graphic-script/odyssey_m1_p7c', file)))) fail('missing ' + file);
const config = await readJson('graphic-script/odyssey_m1_p7c/P7C_STUDY_CONFIG.json');
const schema = await readJson('graphic-script/odyssey_m1_p7c/P7C_DATA_SCHEMA.json');
const template = await readJson('graphic-script/odyssey_m1_p7c/P7C_RESULT_TEMPLATE.json');
const fixture = await readJson('graphic-script/odyssey_m1_p7c/fixtures/P7C_SYNTHETIC_RESULT_FIXTURE.json');
if (config.schema_version !== '1.0.0' || config.prototype_version !== 'P7C-20260824') fail('study identity mismatch');
if (Object.keys(config.conditions).join(',') !== 'A,B') fail('counterbalanced conditions missing');
if (config.conditions.A.length !== 3 || config.conditions.B.length !== 3) fail('each condition must have three tasks');
if (config.conditions.A[0].mode !== 'script' || config.conditions.B[0].mode !== 'graphic' || config.conditions.A[1].mode !== 'graphic' || config.conditions.B[1].mode !== 'script') fail('EP01/EP19 counterbalance is invalid');
if (config.conditions.A[2].episode !== 'EP27' || config.conditions.B[2].mode !== 'graphic') fail('EP27 common Graphic condition is invalid');
const questions = Object.values(config.questions).flat();
if (questions.length !== 9 || new Set(questions.map((item) => item.id)).size !== 9) fail('objective question coverage must be nine unique items');
for (const question of questions) if (!question.prompt || !question.options?.length || !question.correct?.length || !question.metric) fail('incomplete question ' + question.id);
if (schema.properties?.synthetic_fixture?.type !== 'boolean' || template.synthetic_fixture !== false || fixture.synthetic_fixture !== true) fail('synthetic evidence boundary is invalid');
if (!schema.required.includes('participant_consent') || !schema.required.includes('synthetic_fixture')) fail('privacy/evidence fields missing from schema');

const sceneComponent = await readRepo('site/src/components/GraphicSceneBlock.astro');
const identityComponent = await readRepo('site/src/components/GraphicIdentityStrip.astro');
const bridgeComponent = await readRepo('site/src/components/StudySessionBridge.astro');
const testRoute = await readRepo('site/src/pages/graphic/test.astro');
const graphicRoute = await readRepo('site/src/pages/episodes/[number]/graphic.astro');
for (const token of ['现在有哪些人？','character-assist','LEVEL 2 · CONTEXT','data-study-event']) if (!(sceneComponent + '\n' + graphicRoute).includes(token)) fail('reader hierarchy token missing: ' + token);
for (const token of ['ctde-graphic-resume-v1','data-reading-progress','Graphic Edition 尚未制作']) if (!graphicRoute.includes(token)) fail('progress/continuation token missing: ' + token);
for (const token of ['ctde-p7c-study-v1','localStorage','participant_anonymous_code','synthetic_fixture:false','Export Reader Test Result','不会自动上传']) if (!(bridgeComponent + '\n' + testRoute).includes(token)) fail('test harness token missing: ' + token);
for (const forbidden of ['googletagmanager','google-analytics','segment.com','mixpanel','posthog','fingerprint']) if ((bridgeComponent + '\n' + testRoute).toLowerCase().includes(forbidden)) fail('forbidden test dependency/field: ' + forbidden);
if (!identityComponent.includes('data-introduction-tier') || !identityComponent.includes('LEVEL 3 · DETAIL')) fail('progressive identity level missing');

if (distMode) {
  const testHtmlPath = path.join(siteRoot, 'dist/graphic/test/index.html');
  if (!(await exists(testHtmlPath))) fail('built Test Mode route missing');
  const testHtml = await readFile(testHtmlPath, 'utf8');
  for (const token of ['data-test-root','INFORMED TEST NOTICE','Export Reader Test Result']) if (!testHtml.includes(token)) fail('built Test Mode missing ' + token);
  for (const number of ['01','19','27']) {
    const graphicHtml = await readFile(path.join(siteRoot, 'dist/episodes/' + number + '/graphic/index.html'), 'utf8');
    for (const token of ['现在有哪些人？','data-reading-progress','data-study-bridge']) if (!graphicHtml.includes(token)) fail('EP' + number + ' built Graphic route missing ' + token);
  }
  const scriptHtml = await readFile(path.join(siteRoot, 'dist/episodes/01/index.html'), 'utf8');
  if (!scriptHtml.includes('data-study-bridge') || !scriptHtml.includes('data-study-mode-switch="script"')) fail('Script Mode study bridge missing');
}

console.log(JSON.stringify({ status:'PASS_P7C_READER_VERIFY', dist_verified:distMode, prototype_episodes:3, objective_questions:questions.length, test_conditions:2, synthetic_fixture_exclusion_required:true, real_participant_claims:0 }));
