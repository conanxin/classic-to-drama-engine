# Analysis Candidate Run 001 — Execution Report

> Run ID: `AC-20260811-STORYSTRUCT-001`  
> Phase: Phase 2-C  
> Reported at: `2026-08-11T01:01:06-07:00`  
> Status: `BLOCKED_SCOPE_ENFORCEMENT_FAILED`  
> Candidate authority: `non_authoritative`  
> Formal Phase 2 input: `false`

## 1. Result

Run 001 was stopped before story-structure extraction. The structure-only preflight parser expected a Book 1 container matching the approved `book.card` contract, but did not recognize such a container. It reached end-of-file before reporting that failure.

Consequently, the run cannot satisfy the required assertion that only Book 1 was read. No card text was extracted, no model analysis was invoked, and no `story_structure.yaml` was created. Retrying with a different selector or parser under the same run ID is prohibited.

## 2. Input

| Field | Observed value |
| --- | --- |
| `source_id` | `ODY-ENG-MURRAY1919` |
| Input role | English TEI candidate working source for this one run only |
| Path | `source/translations/en/ody-eng-murray1919/raw/ody-eng-murray1919__raw__full.xml` |
| Fixed upstream commit | `790c84289edbdbe289dd7b752bfea29f0af4299d` |
| Expected source snapshot | `SS-ODY-ENG-MURRAY1919-790C8428-DDA5B206-V1` |
| Expected task scope | Book 1 only; no more than 24 native `book.card` units |
| File size from preflight metadata | `870905` bytes |
| Bytes returned to structure parser | `870905` |
| Book 1 container recognized | `false` |
| Card locators extracted | `0` |
| Card text extracted | `0` |
| Model invocations | `0` |

The previously recorded source checksum was not recomputed because full-file content access would conflict with the Book 1-only execution boundary. This run therefore does not assert a new checksum verification.

## 3. Output

All run records are isolated under:

`analysis_candidate/runs/AC-20260811-STORYSTRUCT-001/`

| Output | Status |
| --- | --- |
| `run_manifest.yaml` | Created as a non-authoritative blocked-run manifest |
| `execution_report.md` | Created as this blocked-run audit report |
| `story_structure.yaml` | **Not created**; extraction never started |

## 4. Acceptance checks

| Check | Expected | Observed | Result |
| --- | --- | --- | --- |
| Greek raw access | `0` | Opens `0`; parses `0`; copies `0`; model injections `0` | `PASS` |
| English content scope | Book 1 only | Structure parser consumed the entire English file before failing to identify Book 1 | `FAIL` |
| Book limit | `1` | No Book container accepted | `BLOCKED` |
| Card limit | `1–24` | `0` cards accepted | `BLOCKED` |
| Output path | Exact Candidate run root | Audit records use the exact run root | `PASS` |
| Candidate marking | `non_authoritative` | Present in manifest and report | `PASS` |
| Story structure extraction | Book 1 only | Not executed | `BLOCKED` |

Because one mandatory acceptance condition failed, the run is not `completed` and must not be represented as successful.

## 5. Prohibited-item check

The stopped attempt created none of the following:

- Greek-derived content or Greek locator output;
- character database;
- event database;
- theme database;
- adaptation plan;
- screenplay or short-drama content;
- normalized, aligned, cleaned, repaired, sorted, or passage-indexed source;
- formal Analysis Layer output.

The English raw XML, source metadata, registry, Gate decisions, and the three input contract documents were not modified.

## 6. Closure

```yaml
reporting_status: BLOCKED_SCOPE_ENFORCEMENT_FAILED
execution_result: invalidated
story_structure_extraction_started: false
story_structure_output_created: false
candidate_output_promotable: false
downstream_consumption_allowed: false
formal_phase_2_input: false
retry_under_same_run_id_allowed: false
```

Any corrected attempt requires a new run ID, a structure selector proven against metadata-only fixtures or approved structural evidence, and a fresh one-run authorization.
