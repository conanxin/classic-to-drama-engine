import { readFile, readdir, stat, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const siteRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const repoRoot = path.resolve(siteRoot, '..');
const config = JSON.parse(await readFile(path.join(repoRoot, 'graphic-script/odyssey_m1_p7c/P7C_STUDY_CONFIG.json'), 'utf8'));
const args = process.argv.slice(2);
const outIndex = args.indexOf('--out');
const outPath = outIndex >= 0 ? args[outIndex + 1] : null;
const inputs = outIndex >= 0 ? args.filter((_, index) => index !== outIndex && index !== outIndex + 1) : args;
if (!inputs.length) {
  console.error('usage: node analyze-reader-test-results.mjs <json-file-or-directory> [more inputs] [--out aggregate.json]');
  process.exit(2);
}

const collect = async (target) => {
  const absolute = path.resolve(target);
  const info = await stat(absolute);
  if (info.isFile()) return absolute.endsWith('.json') ? [absolute] : [];
  const entries = await readdir(absolute, { withFileTypes:true });
  const nested = await Promise.all(entries.map((entry) => collect(path.join(absolute, entry.name))));
  return nested.flat();
};
const files = (await Promise.all(inputs.map(collect))).flat();
const required = ['schema_version','prototype_version','study_id','participant_anonymous_code','participant_consent','synthetic_fixture','device_class','condition','started_at','completed_at','tasks','events','answers'];
const objectiveQuestions = Object.values(config.questions).flat();
const sameAnswers = (left = [], right = []) => [...left].map(String).sort().join('|') === [...right].map(String).sort().join('|');
const mean = (values) => values.length ? values.reduce((sum, value) => sum + value, 0) / values.length : null;
const median = (values) => {
  if (!values.length) return null;
  const sorted = [...values].sort((a,b) => a-b);
  const middle = Math.floor(sorted.length / 2);
  return sorted.length % 2 ? sorted[middle] : (sorted[middle - 1] + sorted[middle]) / 2;
};
const countBy = (records, key) => Object.fromEntries([...Map.groupBy(records, (item) => item[key] || 'unknown')].map(([value, group]) => [value, group.length]));

const parsed = [];
const invalid = [];
for (const file of files) {
  try {
    const result = JSON.parse(await readFile(file, 'utf8'));
    const missing = required.filter((field) => !(field in result));
    if (missing.length || result.schema_version !== config.schema_version || result.study_id !== config.study_id || !['A','B'].includes(result.condition) || !Array.isArray(result.tasks) || result.tasks.length !== 3 || !Array.isArray(result.events)) {
      invalid.push({ file, reason:missing.length ? 'missing:' + missing.join(',') : 'identity_or_shape' });
      continue;
    }
    parsed.push({ file, result });
  } catch (error) {
    invalid.push({ file, reason:error.message });
  }
}

const synthetic = parsed.filter(({ result }) => result.synthetic_fixture === true || String(result.participant_anonymous_code).startsWith('SYNTHETIC-'));
const external = parsed.filter(({ result }) => !synthetic.some((item) => item.result === result) && result.participant_consent === true);
const completed = external.filter(({ result }) => Boolean(result.completed_at) && result.tasks.every((task) => task.status === 'completed'));
const partial = external.filter(({ result }) => !completed.some((item) => item.result === result));

const accuracyByMetric = {};
for (const question of objectiveQuestions) {
  const scores = completed.map(({ result }) => sameAnswers(result.answers[question.id] || [], question.correct) ? 1 : 0);
  accuracyByMetric[question.metric] ||= [];
  accuracyByMetric[question.metric].push(...scores);
}
const metricSummary = Object.fromEntries(Object.entries(accuracyByMetric).map(([metric, scores]) => [metric, { correct:scores.reduce((a,b) => a+b,0), total:scores.length, accuracy:mean(scores) }]));
const overallScores = completed.flatMap(({ result }) => objectiveQuestions.map((question) => sameAnswers(result.answers[question.id] || [], question.correct) ? 1 : 0));
const taskDurations = completed.flatMap(({ result }) => result.tasks.map((task) => task.started_offset_ms == null || task.completed_offset_ms == null ? null : task.completed_offset_ms - task.started_offset_ms).filter((value) => value != null));
const eventCounts = {};
for (const { result } of external) for (const event of result.events) eventCounts[event.type] = (eventCounts[event.type] || 0) + 1;
const subjective = {};
for (const question of config.subjective_questions) {
  const values = completed.map(({ result }) => Number(result.answers[question.id]?.[0])).filter(Number.isFinite);
  subjective[question.id] = { count:values.length, mean:mean(values), median:median(values) };
}
const qualitative = Object.fromEntries(config.open_questions.map((question) => [question.id, completed.map(({ result }) => String(result.answers[question.id]?.[0] || '').trim()).filter(Boolean)]));

const aggregate = {
  status: completed.length >= 6 ? 'REAL_READER_EVIDENCE_AVAILABLE_FOR_DECISION' : 'AWAIT_REAL_READER_EVIDENCE',
  schema_version:config.schema_version,
  prototype_version:config.prototype_version,
  inputs:{ files:files.length, parsed:parsed.length, invalid:invalid.length, synthetic_excluded:synthetic.length },
  participants:{ external_valid:external.length, completed:completed.length, partial:partial.length, by_condition:countBy(external.map(({result})=>result),'condition'), by_device:countBy(external.map(({result})=>result),'device_class') },
  comprehension:{ overall_accuracy:mean(overallScores), by_metric:metricSummary },
  completion_rate:external.length ? completed.length / external.length : null,
  task_time_ms:{ count:taskDurations.length, mean:mean(taskDurations), median:median(taskDurations) },
  interactions:eventCounts,
  subjective,
  qualitative,
  invalid_files:invalid,
  evidence_note:completed.length ? 'Only non-synthetic consented exports are aggregated.' : 'No real completed participant results were found; no reader-outcome claim is authorized.'
};
if (outPath) await writeFile(path.resolve(outPath), JSON.stringify(aggregate,null,2) + '\n');
console.log(JSON.stringify(aggregate,null,2));
