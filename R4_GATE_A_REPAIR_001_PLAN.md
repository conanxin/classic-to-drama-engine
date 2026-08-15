# R4 Gate A Versioned Repair 001 Plan

## 0. Identity and authority

```yaml
repair_id: "R4R-20260815-001"
defect_count: 8
base_commit: "dc3d47635d44dfe72ac5333ec702cf762de5a182"
repair_scope_sha256: "e2812b2d1d9c072b3b6765771142a17bb2c8694339a6bf263c07ad59ee753729"
canonical_scope_bytes: 2379
mutable_existing_file_count: 3
additional_mutable_paths: []
formal_gate_b_execution_authorized: false
```

Two previous full temporary attempts were consumed and independently blocked. This plan governs the newly authorized third attempt. Original R4 Plan, Machine Contract, audit, historical Gate A, Gate B scope, tracked probe, source and Candidate surfaces remain immutable.

## 1. Exact defect repairs

| ID | Root cause | Minimal authorized implementation |
| --- | --- | --- |
| `D01` | Marker lookup omits the namespace in the actual fixture. | Require the one exact namespace-bearing Book marker in range. |
| `D02` | Append ledger is born `0444`. | Create it `0600`; freeze all seven ledgers `0444` after final accounting. |
| `D03` | No denied event reaches the logical chain. | Register one exact denied project-root probe with zero bytes. |
| `D04` | Logical bytes precede final-output intents. | Render final four outputs through a bounded deterministic fixed point and identical confirmation. |
| `D05` | Split parser misreads formal requirement IDs. | Strict anchored `RCPT-Tnn-*` parser, `01 <= nn <= 37`. |
| `D06` | Catalog/runtime/T16 use competing object namespaces. | Digest-bound Book and Greek helpers shared across catalog, runtime, auth/capability evidence and verifier. |
| `D07` | Sandbox receives immutable tracked `0644` probe directly. | Verify/copy/chmod/execute/rehash/clean one leaf-temporary `0500` copy. |
| `D08` | Top-level imports create project `__pycache__` before monitoring; verifier can import after its scope check. | Process-inception `-B` protection, worker startup proof, repeated no-cache inventories, and a final post-late-import exact scope check. |

The existing mutable paths remain exactly `build_r4_portable_manifest.py`, `run_r4_portable.py`, and `verify_r4_portable.py` under `runtime_capability_prototype/runtime/`.

## 2. D08 broad process audit and repair

1. Runner: before the four top-level project imports, ensure the process is bytecode-disabled; otherwise `execve` the same interpreter with `-B` and `PYTHONDONTWRITEBYTECODE=1`.
2. Leaf workers: launch with the already minimal environment containing `PYTHONDONTWRITEBYTECODE=1`; prove actual flag/environment in every result.
3. Manifest/result/logical monitor: imported only inside the protected runner process, never separately during Gate B.
4. Verifier: establish the same process-inception guard before any possible project import; inventory caches before verification, after the late manifest-builder import, and before return.
5. Preexecution closure and repair orchestration: launch all Python subprocesses explicitly with `python3 -B`; do not modify the immutable closure builder.
6. Never delete a cache between assertions, ignore it, add it to an allowlist, or change the expected Gate B output count.

## 3. D06 and D07 closure

T16 AUTH-GREEK binds authorization to the catalog Greek ID with no capability ID. T16 CAP-GREEK keeps Book authorization and binds the capability to that same Greek ID. The historical placeholder is absent from all active repaired paths. T29 object-swap and T32 wrong-object remain exact fail-closed regressions.

For each leaf, bind source probe to the active closure, copy exact bytes beneath leaf temp, set only the copy `0500`, execute it through unchanged sandbox when case design reaches sandbox, then independently verify and delete the copy. Persist source/copy digest, modes, path class, execution, sandbox policy, inventory, project-mode stability, and cleanup.

## 4. Temporary preflight and attempt

Create a new OS-temporary clone from the exact clean base. Apply only D01-D08 and draft Contract/Plan. Build the repaired prefix with every Python controller command under `-B`.

Before attempt consumption, without cache cleanup between observations:

1. prove initial project cache counts zero;
2. exercise runner top-level startup/import and prove counts remain zero;
3. execute representative baseline/T16/T19/T29/T32 leaves and prove worker startup, D06/D07, fail-closed outcomes, and counts zero;
4. exercise verifier authorization and late project import paths and prove counts zero afterward;
5. execute a representative output-accounting run and require actual project outputs equal its exact temporary allowlist, unauthorized outputs zero;
6. independently validate the qualification authorization bound to the clean provisional HEAD.

Only then begin and consume one third full attempt. Run once, no retry, through R4-E0 to R4-E10. The new manifest is the sole N authority. Independent `gate-b-result` verification, including its final cache and exact-output inventories, is the final authority.

## 5. PASS and stop behavior

PASS requires D01-D08 individually PASS; 37 groups; discovered, executed, evidence-complete and passed all equal actual N; all negative counters zero; one denied write; repeated append; complete finalization; canonical D06 chain; D07 execution/cleanup; runner/worker/verifier bytecode-disabled; all pre/post cache counts zero; unauthorized outputs zero; and all five prohibited action counts zero.

A same-root cache branch in an allowed path remains D08 and is repaired before attempt start. A distinct D09, a needed additional existing path, a substantive architecture blocker, or an independent-verifier failure stops without authoritative persistence.

## 6. Authoritative workflow after temporary PASS

1. Revalidate authoritative HEAD, actual remote main, clean status, historical hashes, zero repair paths and zero formal Gate B paths.
2. Apply the exact three-file candidate and final Contract/Plan.
3. Create materialization/implementation identities, then build the transitive closure at least twice in separate `python3 -B` processes and require byte identity.
4. Create component freeze and external registry record; persist the temporary qualification summary.
5. Independently verify all bytes, cache absence, exactly three modified tracked files plus ten new files, historical immutability, zero actions, and formal Gate B absence.
6. Write the formal repair result, commit `Repair R4 Gate A implementation and refresh closure`, and push normally without history rewrite.
7. Require local HEAD equal actual `origin/main` and clean status.
8. Generate and independently validate a new complete Gate B human-approval payload from committed bytes.
9. Stop with `HUMAN_AUTHORIZATION_REQUIRED`; do not execute formal Gate B.
