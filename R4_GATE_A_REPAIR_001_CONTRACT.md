# R4 Gate A Versioned Repair 001 Contract

## 0. Contract identity

```yaml
contract_status: "PASS_R4_GATE_A_REPAIR_001_CONTRACT"
repair_id: "R4R-20260815-001"
suite_id: "R4PS-20260815-001"
phase_id: "Phase 2-G-R4FRESH-R1"
phase_kind: "r4_gate_a_versioned_implementation_repair_and_preexecution_closure_refresh"
base_commit: "dc3d47635d44dfe72ac5333ec702cf762de5a182"
expanded_repair_scope_sha256: "e2812b2d1d9c072b3b6765771142a17bb2c8694339a6bf263c07ad59ee753729"
canonical_scope_bytes: 2379
gate_b_write_scope_sha256: "d4bf4ac03afe22461831261e06c82797cf86c50eb3b4882d6275895436baf71c"
closed_defect_count: 8
repair_execution_authorized: true
current_fresh_temporary_full_qualification_attempts_authorized: 1
previous_full_qualification_attempts_consumed: 2
formal_gate_b_execution_authorized: false
```

The 2026-08-15 human authorization expands `R4R-20260815-001` through D08, approves the exact scope below, authorizes one new fresh OS-temporary full qualification, and authorizes authoritative repair persistence only after independent qualification PASS. It does not authorize formal Gate B, Candidate execution, source-content reads, model calls, or business outputs.

## 1. Closed defect set

| ID | Defect | Required repair |
| --- | --- | --- |
| `R4R-D01` | Synthetic fixture Book marker locator mismatch | Locate the exact namespace-bearing Book marker uniquely inside the authorized range. |
| `R4R-D02` | Append-only JSONL initial mode prevents repeated append | Create append ledgers controller-writable, then freeze them read-only after final persistence. |
| `R4R-D03` | Required denied logical-write event absent | Persist one exact denied project-root probe in the authoritative logical chain with zero written bytes. |
| `R4R-D04` | Logical-write evidence finalizes before all monitored writes | Reach a deterministic fixed point containing every final-output intent before final bytes are persisted. |
| `R4R-D05` | Component-subject parser cannot parse formal `RCPT-Tnn-*` IDs | Use one strict anchored parser for 01 through 37 and reject malformed identities. |
| `R4R-D06` | Synthetic fixture object-ID namespace and identity inconsistency | Use one deterministic digest-bound object identity for each synthetic object across every binding and verifier. |
| `R4R-D07` | Sandbox probe executable preparation missing | Verify the immutable tracked probe, create a leaf-temporary byte-identical `0500` copy, execute that copy through the unchanged sandbox, and delete it. |
| `R4R-D08` | Python bytecode project-write escape | Disable bytecode at process inception before every project import and independently prove no project cache output was ever created. |

No distinct defect beyond D08 is authorized. Another same-root bytecode branch inside the existing allowlist remains D08; a genuinely independent D09 stops before authoritative persistence.

## 2. Exact repair scope

The following UTF-8 canonical JSON plus LF is the complete semantic scope preimage. Its byte length is 2379 and SHA-256 is `e2812b2d1d9c072b3b6765771142a17bb2c8694339a6bf263c07ad59ee753729`.

```json
{"creatable_directories":["runtime_capability_prototype/r4_portable_suites/R4PS-20260815-001/repair/","runtime_capability_prototype/r4_portable_suites/R4PS-20260815-001/repair/R4R-20260815-001/","runtime_capability_prototype/r4_portable_suites/R4PS-20260815-001/repair/R4R-20260815-001/control/","runtime_capability_prototype/r4_portable_suites/R4PS-20260815-001/repair/R4R-20260815-001/evidence/"],"creatable_files":["R4_GATE_A_REPAIR_001_CONTRACT.md","R4_GATE_A_REPAIR_001_PLAN.md","runtime_capability_prototype/r4_portable_suites/R4PS-20260815-001/repair/R4R-20260815-001/control/r4r_materialization_plan.json","runtime_capability_prototype/r4_portable_suites/R4PS-20260815-001/repair/R4R-20260815-001/control/r4r_repaired_implementation_manifest.json","runtime_capability_prototype/r4_portable_suites/R4PS-20260815-001/repair/R4R-20260815-001/control/r4r_repaired_preexecution_closure_manifest.json","runtime_capability_prototype/r4_portable_suites/R4PS-20260815-001/repair/R4R-20260815-001/control/r4r_repaired_component_freeze.json","runtime_capability_prototype/r4_portable_suites/R4PS-20260815-001/repair/R4R-20260815-001/control/r4r_repaired_closure_registry_record.json","runtime_capability_prototype/r4_portable_suites/R4PS-20260815-001/repair/R4R-20260815-001/evidence/r4r_temp_gate_b_qualification.json","runtime_capability_prototype/r4_portable_suites/R4PS-20260815-001/repair/R4R-20260815-001/evidence/r4r_repair_verification.json","PORTABLE_RUNTIME_R4_PREEXECUTION_CLOSURE_REPAIR_001_RESULT.md"],"defects":["R4R-D01-SYNTHETIC-BOOK-MARKER-LOCATOR","R4R-D02-APPEND-ONLY-INITIAL-MODE","R4R-D03-DENIED-LOGICAL-WRITE-EVENT","R4R-D04-LOGICAL-WRITE-FINALIZATION","R4R-D05-COMPONENT-SUBJECT-RCPT-GROUP-ID-PARSER","R4R-D06-SYNTHETIC-FIXTURE-OBJECT-ID-NAMESPACE","R4R-D07-SANDBOX-PROBE-EXECUTABLE-PREPARATION","R4R-D08-PYTHON-BYTECODE-PROJECT-WRITE-ESCAPE"],"forbidden_actions":["model_calls","candidate_runs","english_tei_content_reads","greek_tei_content_reads","business_outputs"],"formal_gate_b_execution_authorized":false,"historical_gate_a_policy":"immutable","mutable_existing_files":["runtime_capability_prototype/runtime/build_r4_portable_manifest.py","runtime_capability_prototype/runtime/run_r4_portable.py","runtime_capability_prototype/runtime/verify_r4_portable.py"],"repair_id":"R4R-20260815-001","temporary_full_gate_b_qualification_attempts_authorized":1}
```

The allowlist is exactly the three paths above. The ten create-only files and four directories are exact. Original R4 authorities, historical Gate A, source, Candidate paths, tracked probe, Gate B write scope, Python installation, site-packages, `.gitignore`, and formal Gate B outputs remain immutable.

## 3. D01-D06 evidence contract

The Book marker is the single exact namespace-bearing marker within `[4076,36515)`. Append ledgers begin `0600`, accept repeated append, and freeze `0444`. One denied project-root write with zero bytes is in the chain. Final logical-write, evidence, aggregate, and report intents are rendered through a deterministic fixed point and identical confirmation. Requirement IDs match only anchored `RCPT-T01-*` through `RCPT-T37-*`.

Book identity is `urn:ctde:fixture:<sha256(full_raw)>`; Greek identity is `urn:ctde:fixture-greek-deny:<sha256(greek_raw)>`. Catalog, runtime fixture, authorization, capability, broker, bounded reader, case evidence, snapshot, and verifier must agree exactly. T16 AUTH-GREEK and CAP-GREEK use the canonical Greek ID; the historical placeholder is absent from active paths. Book and Greek digests remain independent exact byte bindings. Object swap and wrong-object cases remain fail-closed.

## 4. D07 executable contract

Each worker recovers the one frozen probe node from the active repaired closure, verifies source digest/length and actual tracked `0644`, copies exact bytes only to `prepared-probe/consumer_probe` under the leaf OS-temporary root, verifies equality, chmods only the copy to `0500`, and binds `SuiteRuntime.probe_binary` to it. The parent independently rehashes/restats, unlinks the exact copy, removes its empty inventory directory, confirms cleanup, and persists the facts. Full historical bootstrap, tracked chmod/replacement, system binaries, and sandbox relaxation are forbidden.

## 5. D08 process-inception and evidence contract

Every formal R4 Python process that may import project modules must have bytecode disabled before its first project import. Top-level runner and verifier self-reexec with the same interpreter under `-B` and `PYTHONDONTWRITEBYTECODE=1` when the incoming process lacks that protection. Leaf workers receive `PYTHONDONTWRITEBYTECODE=1` in their complete environment before interpreter startup. Repair-time closure and other controller-launched Python processes use explicit `python3 -B`; builders imported by the runner inherit its protected process.

Runner checks the project tree before R4-E0, after all workers, and after final outputs. Each worker reports actual startup flag/environment. Verifier checks before semantic verification, after every late local import, and immediately before success. At each point project `__pycache__` directories and `*.pyc` files must be zero. Exact output inventory is repeated after late imports. Cache deletion is never performed or accepted as proof; Gate B write scope is not expanded.

## 6. Fresh qualification gate

The third total full qualification uses a brand-new clone of clean `dc3d47635d44dfe72ac5333ec702cf762de5a182`. Targeted D01-D08 regressions precede attempt consumption. D08 preflight begins with zero caches and, without intervening cleanup, exercises runner startup/import, representative workers, verifier authorization, verifier late import, and representative exact-output accounting; every cache count and unauthorized output count must remain zero.

The attempt starts only after a qualification-only authorization bound to the provisional clean HEAD passes independent verification and the top-level controller begins R4-E0. It is then consumed regardless of outcome. It covers R4-E0 through R4-E10, 37 groups, actual N leaves, fresh identities, registries, append lifecycle, sandbox, D06, denied write, fixed-point evidence, aggregate, report, and independent result verification. PASS requires D01-D08 PASS, all failure/skip/unknown/timeout/duplicate/reuse counts zero, no unauthorized project output, no project Python cache output, and all forbidden actions zero.

## 7. Authoritative persistence and terminal rule

Only after qualification PASS may the controller revalidate the authoritative baseline, apply the exact three-file patch and final Contract/Plan, create the versioned repaired prefix, build the closure twice in separate `-B` processes with byte-identical output, freeze, register, persist qualification evidence, independently verify, write the formal repair result, commit, and push normally. Exactly three tracked modifications and ten new files are permitted. Historical Gate A remains unchanged.

After local/remote convergence and clean status, produce a new complete Gate B human-approval payload from actual committed bytes and stop with `HUMAN_AUTHORIZATION_REQUIRED`. Formal `Phase 2-G-R4FRESH-E1` remains unexecuted.
