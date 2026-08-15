# Fresh Portable R4 Synthetic E2E Plan

## 0. Planning conclusion

This Plan defines the first current-tree Portable R4 machine contract after Fresh R3 PASS. It is a plan, not R4 implementation or execution.

```yaml
plan_status: "PASS_FRESH_R4_SYNTHETIC_E2E_PLAN"
plan_artifact_class: "ctde_fresh_r4_synthetic_e2e_plan"
plan_schema_version: "1.0.0"
planning_phase_id: "Phase 2-G-R4FRESH-P1"
gate_a_phase_id: "Phase 2-G-R4FRESH-M1"
gate_a_phase_kind: "r4_implementation_materialization_and_preexecution_transitive_closure_refresh_only"
gate_b_phase_id: "Phase 2-G-R4FRESH-E1"
gate_b_phase_kind: "portable_r4_fresh_synthetic_e2e_deterministic_execution"
suite_id: "R4PS-20260815-001"
portable_pass_status: "PASS_PORTABLE_RUNTIME_SYNTHETIC_E2E"
blocked_status: "BLOCKED_PORTABLE_RUNTIME_SYNTHETIC_E2E"
planning_write_scope_sha256: "7d5f55e83b679ab6f7f5cda001517ba4f58d5ae763324445a271619ec5d24fb7"
gate_a_write_scope_sha256: "6e25a9fd26f8fbe484692b9e3c3b095fc10cd6f177cf3a38530c360b692fe548"
gate_b_write_scope_sha256: "d4bf4ac03afe22461831261e06c82797cf86c50eb3b4882d6275895436baf71c"
gate_a_authorized: false
gate_b_authorized: false
r4_suite_execution_authorized: false
candidate_execution_authorized: false
candidate_ready: false
certified: false
hardened: false
```

The Plan's SHA-256 is external and is reported only after these exact bytes are persisted. No self-digest field is permitted.

## 1. Frozen planning inputs

| Path | SHA-256 | Bytes |
| --- | --- | ---: |
| `FRESH_R4_SYNTHETIC_E2E_MACHINE_CONTRACT.md` | `b6b10f5cf06ef596270ae00ebd27343e96556593d05d17f6a0af5930e3615422` | 11,168 |
| `FRESH_R4_CURRENT_TREE_AUDIT.json` | `210f5c1e4e205b1e17e731cb87180d72680d576f97a96e746d8f9fc82fde5b6a` | 22,192 |
| `FRESH_R3_PORTABLE_TRANSITIVE_CLOSURE_PLAN.md` | `2e077e39ba4dc5b8f6970cc35a1aab5915fcfa340917afd78cbb3e23f17e0f83` | 37,602 |
| `PORTABLE_RUNTIME_TRANSITIVE_CLOSURE_RESULT.md` | audit-bound | audit-bound |
| `RUNTIME_CAPABILITY_REPAIR_PLAN.md` | `a2c52dbaecf3956cf4a2189abe5401f269d255e8099d3345985619be25be4213` | 45,397 |
| `RUNTIME_OS_OBSERVABILITY_PREFLIGHT_RESULT.md` | audit-bound | audit-bound |
| `PORTABLE_AUTHORIZATION_SCHEMA_V2_IMPLEMENTATION_RESULT.md` | audit-bound | audit-bound |
| `PORTABLE_RUNTIME_ROLE_GAP_RESOLUTION_PLAN.md` | `72f116ff0b93403961a045228706f9322deea008f41718acae6178b0780b8798` | 47,613 |
| `RUNTIME_ASSURANCE_PROFILE_DECISION.md` | `57471c85c57946f6ceb6da288301cc802533b09c137bfbe8e6e247dad57206e2` | 29,635 |
| `CANDIDATE_EXECUTION_CONTRACT_REPAIR.md` | `12ceb01cab4901cb2b7472b1b56f93750a43cb8c28b5f0c9ab89acf3ad4fe7bd` | 76,814 |

The audit is the closed authority for every `audit-bound` digest and byte length.

## 2. Predecessor identities

```yaml
repository_full_name: "conanxin/classic-to-drama-engine"
predecessor_commit: "d22ba2c006a8011a2dfe08ee8c81e7d535593423"
predecessor_remote_main: "d22ba2c006a8011a2dfe08ee8c81e7d535593423"
r2_status: "PASS_PORTABLE_AUTHORIZATION_SCHEMA_V2_IMPLEMENTED"
r2_suite_id: "R2PS-20260811-001"
r3_status: "PASS_PORTABLE_RUNTIME_TRANSITIVE_CLOSURE"
r3_suite_id: "R3PS-20260814-001"
r3_closure_manifest_sha256: "56491b3fd08332327e98284a5dce0b482d3d6ae4bd23517204c62fa63fa3a4a5"
r3_closure_payload_sha256: "703dcba04e0ce669c5472ef4d9b3fc6ed7080eb112e9d5770b3d40c3296e2eca"
r3_component_freeze_sha256: "73478ed2ee2f33c3ee348f83328737bb4877d25f1e3859b5b72ca5615a193b14"
r3_registry_record_sha256: "1c858c5d11b436dfd873989eb71c99390556d633c2d23deb100ba28f0678fb3f"
r3_actual_leaves: 780
r3_failed: 0
r3_skipped: 0
r3_unknown: 0
r3_timeout: 0
historical_r1_status: "BLOCKED_OS_OBSERVABILITY_INSUFFICIENT"
current_machine_r1_status: "NOT_REQUALIFIED"
```

The historical R1 result belongs to the old environment. The current WSL planning observation is more permissive (`PTRACE_TRACEME` succeeds, seccomp is off) but is not R1 evidence. Neither may be rewritten as an R1 PASS.

## 3. Assurance and claim ceiling

Portable R4 is a complete logical synthetic E2E under `CTDE-PORTABLE-DEV-1` at A1. It may PASS only as:

```text
PASS_PORTABLE_RUNTIME_SYNTHETIC_E2E
```

That status means all 37 logical requirement groups and all newly expanded leaves pass against fresh synthetic fixtures, V2 authorization state, the refreshed closure, and the Portable logical write boundary.

It does not mean:

- `PASS_RUNTIME_CAPABILITY_PROTOTYPE` under the historical A3 contract;
- R1/A2 OS observer qualification;
- complete syscall/file-open-set proof;
- production or hardened certification;
- real source zero-access independently proved at A2;
- Candidate readiness or Candidate authorization;
- model mediation or business output.

Portable evidence must report operator/controller action counts as integers. Fields requiring A2 independence remain `not_claimed_under_portable_a1`, not fabricated zeros. This does not create skipped test leaves: the A1 logical denial leaves still execute and terminate, while the result's assurance section preserves the higher-evidence boundary.

## 4. R4 role implementation bundle

Gate A materializes exactly these 16 implementation files as one create-once bundle:

```text
runtime_capability_prototype/contracts/r4_portable_e2e_policy_v1.yaml
runtime_capability_prototype/contracts/r4_portable_test_requirements_v1.yaml
runtime_capability_prototype/contracts/r4_portable_test_manifest_schema_v1.yaml
runtime_capability_prototype/contracts/r4_portable_case_result_schema_v1.yaml
runtime_capability_prototype/contracts/r4_portable_logical_write_event_schema_v1.yaml
runtime_capability_prototype/contracts/r4_portable_aggregate_schema_v1.yaml
runtime_capability_prototype/contracts/r4_portable_execution_snapshot_schema_v1.yaml
runtime_capability_prototype/contracts/r4_preexecution_closure_manifest_schema_v1.yaml
runtime_capability_prototype/contracts/r4_preexecution_closure_result_schema_v1.yaml
runtime_capability_prototype/contracts/r4_portable_controller_terminal_schema_v1.yaml
runtime_capability_prototype/runtime/build_r4_preexecution_closure.py
runtime_capability_prototype/runtime/build_r4_portable_manifest.py
runtime_capability_prototype/runtime/monitor_r4_logical_writes.py
runtime_capability_prototype/runtime/verify_r4_portable.py
runtime_capability_prototype/runtime/run_r4_portable.py
runtime_capability_prototype/runtime/build_r4_portable_result.py
```

Responsibilities are exact:

| Gap identity | Formal role | Sole implementation |
| --- | --- | --- |
| `R3G-01-PORTABLE-R4-SUITE-MANIFEST-BUILDER` | Portable R4 suite-manifest builder | `build_r4_portable_manifest.py` |
| `R3G-02-PORTABLE-R4-SUITE-RUNNER` | Portable R4 suite runner | `run_r4_portable.py` |
| `R3G-05-PORTABLE-LOGICAL-WRITE-MONITOR` | Portable logical write monitor | `monitor_r4_logical_writes.py` |
| `R3G-06-PORTABLE-R4-AGGREGATE-REPORT-GENERATOR` | Portable R4 aggregate/report generator | `build_r4_portable_result.py` |

`verify_r4_portable.py` is the independent verifier. `build_r4_preexecution_closure.py` is the mandatory refresh producer. Existing R3 or legacy builders/runners may be inputs or comparison evidence but cannot impersonate these roles.

The current embedded parser-scope and discard-only gateway remain the approved A1 implementations. R4 must bind their exact R3G03/R3G04 identities, test the Book 1/Book 2/unsafe-parser boundaries with synthetic bytes, persist no model payload, and perform zero model calls. No independent parser or gateway redesign is required for Portable R4.

## 5. Gate A exact write scope

Canonicalization is compact key-sorted UTF-8 JSON with no terminal LF.

```yaml
canonical_byte_length: 2309
gate_a_write_scope_sha256: "6e25a9fd26f8fbe484692b9e3c3b095fc10cd6f177cf3a38530c360b692fe548"
mutable_existing_files: []
creatable_file_count: 23
creatable_directory_count: 4
```

In addition to the 16 implementation files in section 4, Gate A may create only:

```text
runtime_capability_prototype/r4_portable_suites/R4PS-20260815-001/control/r4_implementation_manifest.json
runtime_capability_prototype/r4_portable_suites/R4PS-20260815-001/control/r4_materialization_plan.json
runtime_capability_prototype/r4_portable_suites/R4PS-20260815-001/control/r4_preexecution_closure_manifest.json
runtime_capability_prototype/r4_portable_suites/R4PS-20260815-001/control/r4_preexecution_component_freeze.json
runtime_capability_prototype/r4_portable_suites/R4PS-20260815-001/control/r4_preexecution_closure_registry_record.json
runtime_capability_prototype/r4_portable_suites/R4PS-20260815-001/evidence/r4_preexecution_closure_verification.json
PORTABLE_RUNTIME_R4_PREEXECUTION_CLOSURE_RESULT.md
```

Creatable directories are exactly:

```text
runtime_capability_prototype/r4_portable_suites/
runtime_capability_prototype/r4_portable_suites/R4PS-20260815-001/
runtime_capability_prototype/r4_portable_suites/R4PS-20260815-001/control/
runtime_capability_prototype/r4_portable_suites/R4PS-20260815-001/evidence/
```

Every other project path is default-deny. All existing project files are immutable.

## 6. Gate A lifecycle and refreshed closure

```text
R4-M0-AUTH
-> R4-M1-IMPLEMENTATION
-> R4-M2-MATERIALIZATION-PLAN
-> R4-M3-TWO-PASS-CLOSURE-REFRESH
-> R4-M4-COMPONENT-FREEZE
-> R4-M5-EXTERNAL-REGISTRY
-> R4-M6-INDEPENDENT-VERIFICATION
-> R4-M7-RESULT
-> R4-M8-GIT
```

Gate A must:

1. revalidate exact Git/remote, contract/audit/Plan, suite absence, and write scope before any write;
2. materialize all 16 implementation files and their canonical manifest atomically;
3. build the refreshed closure twice in separate processes and require byte identity;
4. include every prior R3 member, every R4 implementation member, all new imports/configs/platform boundaries, and all actual control edges;
5. recompute the current interpreter, stdlib, PyYAML, cryptography, native, loader, shared-library, environment, symlink, and process boundaries;
6. require unknown/unresolved/project-owned-unregistered counts zero;
7. freeze the refreshed component set and create an independent external registry record;
8. verify all existing project bytes unchanged and the exact 23-file changeset;
9. create one Gate A commit and normally push `main` only on PASS.

Gate A PASS is:

```text
PASS_R4_PREEXECUTION_TRANSITIVE_CLOSURE_REFRESH
```

Gate A does not create fixtures, authorizations, test manifest, attempts, runtime events, case results, aggregate, or R4 result. If any R4 implementation byte exists without a complete valid prefix, stop with `BLOCKED_R4_PARTIAL_MATERIALIZATION`. Invalid resume uses `BLOCKED_R4_RESUME_IDENTITY_MISMATCH`.

Gate A approval cannot be interpreted as Gate B approval.

## 7. Gate B exact write scope

```yaml
canonical_byte_length: 2286
gate_b_write_scope_sha256: "d4bf4ac03afe22461831261e06c82797cf86c50eb3b4882d6275895436baf71c"
mutable_existing_files: []
creatable_file_count: 20
creatable_directory_count: 3
```

Gate B may create only:

```text
runtime_capability_prototype/r4_portable_suites/R4PS-20260815-001/control/r4_test_manifest.json
runtime_capability_prototype/r4_portable_suites/R4PS-20260815-001/control/r4_execution_snapshot.json
runtime_capability_prototype/r4_portable_suites/R4PS-20260815-001/control/r4_snapshot_registry_record.json
runtime_capability_prototype/r4_portable_suites/R4PS-20260815-001/fixtures/synthetic_full_fixture.bin
runtime_capability_prototype/r4_portable_suites/R4PS-20260815-001/fixtures/synthetic_greek_deny.bin
runtime_capability_prototype/r4_portable_suites/R4PS-20260815-001/fixtures/r4_synthetic_fixture_catalog.json
runtime_capability_prototype/r4_portable_suites/R4PS-20260815-001/registry/authorization_registry.jsonl
runtime_capability_prototype/r4_portable_suites/R4PS-20260815-001/registry/authorization_state.json
runtime_capability_prototype/r4_portable_suites/R4PS-20260815-001/registry/registry_events.jsonl
runtime_capability_prototype/r4_portable_suites/R4PS-20260815-001/evidence/controller_terminals.jsonl
runtime_capability_prototype/r4_portable_suites/R4PS-20260815-001/evidence/attempts.jsonl
runtime_capability_prototype/r4_portable_suites/R4PS-20260815-001/evidence/runtime_events.jsonl
runtime_capability_prototype/r4_portable_suites/R4PS-20260815-001/evidence/logical_write_events.jsonl
runtime_capability_prototype/r4_portable_suites/R4PS-20260815-001/evidence/case_results.jsonl
runtime_capability_prototype/r4_portable_suites/R4PS-20260815-001/evidence/start_verification.json
runtime_capability_prototype/r4_portable_suites/R4PS-20260815-001/evidence/dynamic_observation.json
runtime_capability_prototype/r4_portable_suites/R4PS-20260815-001/evidence/end_verification.json
runtime_capability_prototype/r4_portable_suites/R4PS-20260815-001/evidence/evidence_manifest.json
runtime_capability_prototype/r4_portable_suites/R4PS-20260815-001/aggregate/r4_portable_results.json
PORTABLE_RUNTIME_SYNTHETIC_E2E_RESULT.md
```

Creatable directories are exactly:

```text
runtime_capability_prototype/r4_portable_suites/R4PS-20260815-001/fixtures/
runtime_capability_prototype/r4_portable_suites/R4PS-20260815-001/registry/
runtime_capability_prototype/r4_portable_suites/R4PS-20260815-001/aggregate/
```

The suite `control/` and `evidence/` directories are valid Gate A prefix directories. Gate B may append only to the newly created JSONL evidence/registry ledgers. It may not modify any Gate A artifact or existing project file.

## 8. Synthetic fixture contract

The fixture builder is part of the manifest builder and returns bytes to the controller; it has no direct project write authority.

### 8.1 Synthetic full fixture

The recipe must:

- use a fixed domain-separated deterministic byte generator;
- produce a file strictly larger than 36,515 bytes;
- make `[4076,36515)` exactly 32,439 bytes;
- encode synthetic `BOOK_01`, 10 `CARD_n`, and 10 `PARAGRAPH_n` structural markers wholly inside the allowed slice;
- encode a synthetic Book 2 sentinel outside the allowed slice;
- contain no bytes copied, hashed, sampled, transformed, or inferred from literary source bodies;
- publish exact recipe ID, digest, size, marker offsets, and allowed-slice digest in the catalog.

### 8.2 Synthetic Greek deny object

The Greek deny object must be non-empty, generated from a separate fixed domain, and have a distinct object ID/digest. No authorization may name it. Catalog, broker, consumer, parser, and gateway denial leaves must prove logical non-reachability.

### 8.3 Temporary artifacts

Per-leaf immutable V2 authorization bytes, sealed slice handles, and formal-loader positive fixtures may exist only in an OS temporary directory with an exact controller inventory. Registry custody persists the authorization exact bytes/digest/size. Temporary paths are never closure members or project outputs and are deleted after their leaf reaches a terminal record.

## 9. Fresh identity and state contract

- Old `RCPTS-20260811-001`, `RCPTS-20260811-002`, R2, R3G07, and R3 suites are read-only historical evidence.
- No old authorization, grant, attempt, nonce, state row, capability, envelope, delivery, event, attestation, key-use state, fixture byte, or case result may be reused.
- R4 leaf IDs are generated from the new requirement recipe and subject identity.
- Attempts use a fresh `RCPT-R4-*` namespace and are unique.
- Every leaf has a unique fresh attempt identity.
- Each authorization-related leaf has its own new V2 authorization ID and registry custody record.
- No automatic retry exists. A consumed authorization remains spent after any downstream failure.
- The test signing key is deterministic, suite-specific, test-only, and distinct from the immutable public production trust root. Production private key material is forbidden.

## 10. Requirement groups and expansion

The closed group identities are:

```text
RCPT-T01-EXACT-RANGE
RCPT-T02-AUTH-MISSING
RCPT-T03-AUTH-DIGEST
RCPT-T04-AUTH-EXPIRED
RCPT-T05-AUTH-REPLAY
RCPT-T06-CAP-TAMPER
RCPT-T07-CAP-AUDIENCE
RCPT-T08-RANGE-OVERRIDE
RCPT-T09-RANGE-SHORT
RCPT-T10-RANGE-LONG
RCPT-T11-SLICE-HASH
RCPT-T12-DELIVERY-REPLAY
RCPT-T13-ENVELOPE-TAMPER
RCPT-T14-FULL-PATH
RCPT-T15-HANDLE-INVENTORY
RCPT-T16-GREEK-ID
RCPT-T17-GREEK-PATH
RCPT-T18-BOOK2-MARKER
RCPT-T19-WRITE-ESCAPE
RCPT-T20-FORMAL-DISCOVERY
RCPT-T21-RENAMED-COPY
RCPT-T22-AUDIT-MISSING
RCPT-T23-AUTH-CONCURRENT
RCPT-T24-CAS-CRASH
RCPT-T25-AUDIT-TAMPER
RCPT-T26-FORMAL-POSITIVE
RCPT-T27-FORMAL-TOCTOU
RCPT-T28-PARSER-UNSAFE
RCPT-T29-BROKER-OBJECT-SWAP
RCPT-T30-SECOND-CHANNEL
RCPT-T31-BROKER-FALLBACK
RCPT-T32-RANGE-ONLY-MISMATCH
RCPT-T33-PROFILE-ALG
RCPT-T34-PROFILE-TYP
RCPT-T35-PROFILE-KID
RCPT-T36-PROFILE-AUD
RCPT-T37-PROFILE-TIME
```

The builder must expand actual leaves from new requirements and compound vectors. It may use historical scenarios as regression inputs, but it may neither copy the old 197-leaf manifest nor force `N=197`.

Each leaf contains exactly: stable leaf ID, group ID, scenario, fresh attempt ID, optional fresh authorization ID, fixture recipe ID, component subject, expected terminal, side-effect ceiling, evidence locator, and no-retry flag. Manifest count authority is the actual leaf array.

PASS requires:

```yaml
requirement_groups_present: 37
manifest_leaf_count: N
runner_discovered: N
runner_executed: N
evidence_complete: N
passed: N
failed: 0
skipped: 0
unknown: 0
timeout: 0
duplicate_attempt_ids: 0
cross_case_authorization_reuse: 0
```

## 11. Positive synthetic Book 1 path

The positive leaf performs, in order:

1. exact Gate B authorization, refreshed closure, snapshot, fixture, public-trust, and manifest verification;
2. new V2 authorization creation, schema validation, external exact-byte registration, and `unconsumed` state;
3. atomic CAS to `spent`, mint lease, capability preparation, and activation using typed V2 contexts;
4. broker fixed-offset/fixed-length read of the synthetic `[4076,36515)` slice;
5. actual range-union, length, and synthetic slice-digest verification;
6. immutable sealed-handle and signed-envelope delivery;
7. bounded-reader binding, seal, digest, length, one-shot, and replay validation;
8. embedded parser-scope validation of synthetic Book 1, 10 Card markers, and 10 Paragraph markers;
9. discard-only gateway event with zero model calls and no payload persistence;
10. A1 scope and closure attestations bound to the same attempt;
11. logical write monitor verification;
12. a synthetic formal-loader positive control in OS temporary storage;
13. case terminal and controller terminal persistence.

Positive expectations are:

```yaml
authorized_range: [4076, 36515]
expected_length: 32439
broker_actual_union: [[4076, 36515]]
bytes_outside_authorized_range: 0
bounded_reader_received_bytes: 32439
delivery_count: 1
delivery_replay_success_count: 0
parsed_books: [1]
parsed_card_count: 10
parsed_paragraph_count: 10
prefix_sentinel_visible_count: 0
book2_sentinel_visible_count: 0
greek_sentinel_visible_count: 0
consumer_visible_full_object_handles: 0
model_invocations: 0
business_outputs_created: 0
scope_proof_level: "A1"
```

## 12. Negative and fail-closed behavior

All 36 remaining groups and all compound expansions execute. They cover missing/invalid/expired/replay authorization, concurrent CAS, crash-after-CAS, capability/envelope/profile tamper, range override/short/long/fallback, slice digest, replay, full-path/handle/second-channel denial, Greek ID/path denial, Book 2 marker denial, unsafe parser denial, object swap, logical write escape, formal discovery/copy/rename/TOCTOU, missing/tampered audit, and signed-profile alg/typ/kid/aud/time failures.

A rejected operation counts as a test PASS only when the exact blocker, actual side-effect counts, not-reached fields, and terminal evidence are complete. It may not emit expected values as observations. Failure to reach an evidence producer is explicit and cannot be represented by an empty artifact.

## 13. Logical write-monitor contract

The Portable logical write monitor is A1 instrumentation. It owns a closed path policy covering only the Gate B files and OS-temporary leaf artifacts. Every attempted logical write produces an append-only event with:

```text
sequence, attempt_id, operation, requested_path_class, resolved_path,
allowed, blocker, bytes_requested, bytes_written, producer_id,
previous_event_sha256, fixed_time, snapshot_identity
```

It must observe allowed controller writes and deliberate denied path-escape/write-escape probes. It must prove existing project files unchanged and final created paths exactly equal Gate B scope. It does not claim syscall-complete observation or tamper-proof A2 evidence.

## 14. Gate B execution lifecycle

```text
R4-E0-AUTH
-> R4-E1-PREFIX-AND-CLOSURE
-> R4-E2-FIXTURES
-> R4-E3-MANIFEST
-> R4-E4-SNAPSHOT-AND-REGISTRY
-> R4-E5-START
-> R4-E6-ATTEMPTS
-> R4-E7-DYNAMIC
-> R4-E8-END
-> R4-E9-EVIDENCE
-> R4-E10-RESULT
-> R4-E11-GIT
```

Start verification occurs before any Runtime import or fixture read. Runtime imports occur only in isolated child processes with fixed environments and bytecode writes disabled. Dynamic observation must enumerate actual project-owned imports/opens and require them to be registered in the refreshed closure. End verification rehashes the complete immutable prefix and requires closure delta zero.

Controller terminal, attempts, Runtime events, registry events, logical write events, and case results are canonical append-only JSONL chains. The aggregate and report generators return bytes and have no direct write authority. The controller is the sole persistent producer.

On Portable PASS, Gate B creates one R4 execution commit and normally pushes `main`; no amend, rebase, force, force-with-lease, or tag movement is allowed.

## 15. Evidence and result contract

`r4_portable_results.json` is computed only from independently rehashed artifacts. It must contain:

- Gate A implementation/refresh identities;
- Gate B authorization and snapshot identities;
- actual 37-group and `N` counts;
- per-domain A1 logical evidence counts;
- fresh authorization/attempt uniqueness and CAS outcomes;
- positive path exact values and negative blocker coverage;
- start/dynamic/end and closure-delta results;
- actual project changeset and logical write-monitor counts;
- source/model/Candidate/business action ledger;
- assurance fields distinguishing A1 proved facts from A2/A3 not-claimed facts.

The formal result path is:

```text
PORTABLE_RUNTIME_SYNTHETIC_E2E_RESULT.md
```

PASS status is `PASS_PORTABLE_RUNTIME_SYNTHETIC_E2E`. Any failed, skipped, unknown, timeout, incomplete evidence, unresolved dependency, closure drift, old-state reuse, source binding, model call, business output, or scope violation produces `BLOCKED_PORTABLE_RUNTIME_SYNTHETIC_E2E`.

The result must state:

```yaml
historical_a3_prototype_status: "NOT_CLAIMED"
r1_requalification_status: "NOT_REQUIRED_FOR_PORTABLE_A1"
real_source_zero_access_a2: "not_claimed_under_portable_a1"
candidate_ready: false
candidate_execution_authorized: false
```

## 16. Optional R1 requalification boundary

The current WSL planning observation justifies a future narrow requalification attempt, not an infrastructure redesign. A separately scoped R1 task may install ordinary `strace`, run a fresh non-literary probe suite, and test descendant attribution, loss accounting, network/write coverage, ready handshake, and evidence custody. It must use a new suite ID and result path and may not overwrite `OSOP-20260811-001`.

Portable R4 Gate A/B do not require that optional task and cannot claim its result. If a later Candidate contract requires A2/A3 before real content, that gate is a substantive future authorization/dependency and must be handled there.

## 17. Resume and failure rules

Resume is allowed only under the same exact human authorization, Plan/audit, phase, suite, write scope, Git ancestor, implementation manifest, refreshed closure, and valid strict stage prefix. Create-once files cannot be regenerated or repaired in place.

Stop statuses are:

```text
BLOCKED_R4_EXECUTION_GATE_FAILED
BLOCKED_R4_PARTIAL_MATERIALIZATION
BLOCKED_R4_RESUME_IDENTITY_MISMATCH
BLOCKED_R4_PREEXECUTION_TRANSITIVE_CLOSURE_REFRESH
BLOCKED_PORTABLE_RUNTIME_SYNTHETIC_E2E
```

An implementation or ordinary test bug may be fixed only before authoritative create-once materialization, or under a separately authorized repair scope after a partial-state blocker. No overwrite may manufacture PASS.

## 18. Gate A human authorization payload

The next human message may authorize Gate A only by quoting the exact persisted external Plan digest in this payload:

```yaml
current_status: "READY_FOR_R4_MATERIALIZATION_AND_CLOSURE_REFRESH_AUTHORIZATION_REVIEW"
contract_path: "FRESH_R4_SYNTHETIC_E2E_MACHINE_CONTRACT.md"
contract_sha256: "b6b10f5cf06ef596270ae00ebd27343e96556593d05d17f6a0af5930e3615422"
current_tree_audit_path: "FRESH_R4_CURRENT_TREE_AUDIT.json"
current_tree_audit_sha256: "210f5c1e4e205b1e17e731cb87180d72680d576f97a96e746d8f9fc82fde5b6a"
plan_path: "FRESH_R4_SYNTHETIC_E2E_PLAN.md"
plan_sha256: "<exact persisted external SHA-256>"
phase_id: "Phase 2-G-R4FRESH-M1"
phase_kind: "r4_implementation_materialization_and_preexecution_transitive_closure_refresh_only"
suite_id: "R4PS-20260815-001"
gate_a_write_scope_sha256: "6e25a9fd26f8fbe484692b9e3c3b095fc10cd6f177cf3a38530c360b692fe548"
predecessor_r3_commit: "d22ba2c006a8011a2dfe08ee8c81e7d535593423"
predecessor_r3_closure_manifest_sha256: "56491b3fd08332327e98284a5dce0b482d3d6ae4bd23517204c62fa63fa3a4a5"
predecessor_r3_closure_payload_sha256: "703dcba04e0ce669c5472ef4d9b3fc6ed7080eb112e9d5770b3d40c3296e2eca"
approval_scope: "R4 implementation materialization and deterministic pre-execution closure refresh only; no R4 suite execution"
```

This payload authorizes exactly one Gate A attempt. It does not authorize Gate B.

## 19. Gate B future authorization payload template

After Gate A PASS, the controller must fill every placeholder from persisted artifacts and request a new human message:

```yaml
current_status: "READY_FOR_PORTABLE_R4_SYNTHETIC_E2E_EXECUTION_AUTHORIZATION_REVIEW"
plan_path: "FRESH_R4_SYNTHETIC_E2E_PLAN.md"
plan_sha256: "<same exact persisted Plan SHA-256>"
current_tree_audit_sha256: "210f5c1e4e205b1e17e731cb87180d72680d576f97a96e746d8f9fc82fde5b6a"
phase_id: "Phase 2-G-R4FRESH-E1"
phase_kind: "portable_r4_fresh_synthetic_e2e_deterministic_execution"
suite_id: "R4PS-20260815-001"
implementation_manifest_sha256: "<Gate A persisted digest>"
refreshed_closure_manifest_sha256: "<Gate A persisted file digest>"
refreshed_closure_payload_sha256: "<Gate A persisted payload digest>"
preexecution_component_freeze_sha256: "<Gate A persisted digest>"
preexecution_closure_registry_record_sha256: "<Gate A persisted digest>"
gate_b_write_scope_sha256: "d4bf4ac03afe22461831261e06c82797cf86c50eb3b4882d6275895436baf71c"
approval_scope: "one Portable R4 fresh synthetic E2E execution attempt only; no Candidate, source read, model call, or business output"
```

No agent-authored Gate A output can self-authorize Gate B.

## 20. Planning verification

The planning phase expands 18 groups from actual audit/source/scope inventories:

```yaml
planning_requirement_groups: 18
planning_leaves_discovered: 338
planning_leaves_executed: 338
planning_evidence_complete: 338
planning_leaves_passed: 338
planning_failed: 0
planning_skipped: 0
planning_unknown: 0
planning_timeout: 0
runtime_modifications: 0
r4_materializations: 0
r4_suite_executions: 0
candidate_runs: 0
model_calls: 0
english_tei_content_reads: 0
greek_tei_content_reads: 0
business_outputs: 0
```

The 338 leaves cover exact Git identities, three planning paths, 11 formal sources, R2 identities/counts, R3 artifacts/payload/counts, assurance reconciliation, 59 Runtime/control identities, four role mappings, synthetic boundaries, 37 logical groups, fresh-state rules, V2/public-trust binding, logical write monitoring, refreshed closure lifecycle, Gate B artifacts/lifecycle, both exact scopes, both authorization gates, and zero-action/claim-ceiling fields.

## 21. Terminal gate

```yaml
current_status: "READY_FOR_R4_MATERIALIZATION_AND_CLOSURE_REFRESH_AUTHORIZATION_REVIEW"
next_phase_id: "Phase 2-G-R4FRESH-M1"
next_phase_kind: "r4_implementation_materialization_and_preexecution_transitive_closure_refresh_only"
suite_id: "R4PS-20260815-001"
gate_a_write_scope_sha256: "6e25a9fd26f8fbe484692b9e3c3b095fc10cd6f177cf3a38530c360b692fe548"
gate_b_write_scope_sha256: "d4bf4ac03afe22461831261e06c82797cf86c50eb3b4882d6275895436baf71c"
r4_materialization_authorized: false
r4_closure_refresh_authorized: false
r4_suite_execution_authorized: false
human_authorization_required: true
```

Stop here until a human supplies the exact Gate A payload with this Plan's persisted external SHA-256.
