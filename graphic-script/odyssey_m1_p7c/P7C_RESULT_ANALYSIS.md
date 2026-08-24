# P7C Result Analysis

status: `NO_REAL_PARTICIPANT_DATA_IMPORTED`
real participant count: `0`
synthetic fixtures excluded: `1`

## Analysis contract

`site/scripts/analyze-reader-test-results.mjs` accepts one or more exported JSON files or directories. It validates the P7C identity, rejects malformed results, excludes every `synthetic_fixture: true` record, reports partial sessions separately, and aggregates only consented external results.

The aggregate reports sample count, condition/device mix, completion, objective accuracy by research domain, task duration, help use, mode switches, continuation intent, overload ratings and recurring open-response themes. It does not calculate statistical significance or infer causality from this usability sample.

## Current evidence

The repository contains one explicitly labelled synthetic fixture for analyzer regression. It proves the exclusion path and contributes zero participants, zero completions and zero accuracy observations to real-reader evidence.

No statements about improved memory, faster completion, preference or willingness to continue are authorized at this stage.

## Import procedure

Place voluntarily shared anonymous exports in a task-owned local folder outside the public site, then run:

```text
node site/scripts/analyze-reader-test-results.mjs <result-file-or-directory> [more inputs]
```

Review invalid/excluded counts before interpreting metrics. A future versioned analysis may write a formal aggregate only after at least six valid external results are available.
