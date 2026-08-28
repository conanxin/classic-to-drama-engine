#!/usr/bin/env node
import { spawn } from 'node:child_process';

const [requestedMode, command, ...args] = process.argv.slice(2);
if (!['auto', 'release', 'deployment'].includes(requestedMode) || !command) {
  throw new Error('Usage: run-with-historical-verification-mode.mjs <auto|release|deployment> <command> [args...]');
}

const resolvedMode = requestedMode === 'auto'
  ? (process.env.VERCEL === '1' ? 'deployment' : 'release')
  : requestedMode;

console.log(JSON.stringify({
  historical_verification_policy:resolvedMode,
  vercel_environment:process.env.VERCEL === '1'
}));

const child = spawn(command, args, {
  env:{ ...process.env, CTDE_HISTORICAL_VERIFICATION_MODE:resolvedMode },
  shell:process.platform === 'win32',
  stdio:'inherit'
});

child.on('error', (error) => {
  console.error(error);
  process.exitCode = 1;
});
child.on('exit', (code, signal) => {
  if (signal) {
    console.error(`Verification command terminated by signal ${signal}`);
    process.exitCode = 1;
    return;
  }
  process.exitCode = code ?? 1;
});
