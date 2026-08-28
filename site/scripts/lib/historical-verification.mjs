import { execFile } from 'node:child_process';
import { promisify } from 'node:util';

const run = promisify(execFile);

export const HISTORICAL_VERIFICATION_RELEASE = 'PASS_FULL_GIT_HISTORY';
export const HISTORICAL_VERIFICATION_SKIPPED = 'SKIPPED_VERCEL_SHALLOW_GIT_HISTORY';

const configuredMode = process.env.CTDE_HISTORICAL_VERIFICATION_MODE;
if (configuredMode && !['release', 'deployment'].includes(configuredMode)) {
  throw new Error(`Unsupported CTDE historical verification mode: ${configuredMode}`);
}

export const historicalVerificationMode = configuredMode
  ?? (process.env.VERCEL === '1' ? 'deployment' : 'release');

export const historicalVerificationStatus = historicalVerificationMode === 'deployment'
  ? HISTORICAL_VERIFICATION_SKIPPED
  : HISTORICAL_VERIFICATION_RELEASE;

export const historicalVerificationIsSkipped = historicalVerificationMode === 'deployment';

const commandFailure = (operation, error) => {
  const detail = String(error?.stderr || error?.message || error).trim();
  throw new Error(`Historical verification failed closed during ${operation}: ${detail}`, { cause:error });
};

export async function readHistoricalBytes({ repoRoot, baselineCommit, relativePath }) {
  if (historicalVerificationIsSkipped) {
    return { bytes:null, skipped:true };
  }
  try {
    const { stdout } = await run(
      'git',
      ['show', `${baselineCommit}:${relativePath}`],
      { cwd:repoRoot, encoding:null, maxBuffer:64 * 1024 * 1024 }
    );
    return { bytes:stdout, skipped:false };
  } catch (error) {
    commandFailure(`git show ${baselineCommit}:${relativePath}`, error);
  }
}

export async function diffHistoricalPaths({ repoRoot, baselineCommit, paths }) {
  if (historicalVerificationIsSkipped) {
    return { changedPaths:null, skipped:true };
  }
  try {
    const { stdout } = await run(
      'git',
      ['diff', '--name-only', baselineCommit, '--', ...paths],
      { cwd:repoRoot, encoding:'utf8', maxBuffer:16 * 1024 * 1024 }
    );
    return { changedPaths:stdout.trim(), skipped:false };
  } catch (error) {
    commandFailure(`git diff ${baselineCommit}`, error);
  }
}

export function historicalVerificationReport({ baselineCommit, checked, skipped, kind }) {
  return {
    historical_artifact_verification:historicalVerificationStatus,
    historical_verification_mode:historicalVerificationMode,
    historical_verification_kind:kind,
    historical_baseline_commit:baselineCommit,
    historical_checks_executed:checked,
    historical_checks_skipped:skipped
  };
}
