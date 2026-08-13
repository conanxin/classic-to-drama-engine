# Fresh Portable Runtime Transitive Closure Plan

## 0. Planning conclusion

This Plan replaces the historical pre-adjudication R3P for the current tree. It is a file-level execution contract for a future Portable R3 closure phase, not an R3 execution. It binds the completed R3G03 parser-scope mapping, R3G04 discard-only gateway mapping, and R3G07 public-trust repair; it retains R3G01/02/05/06 with explicit stage-scoped R4 dispositions.

```yaml
plan_status: "PASS_FRESH_R3_FILE_LEVEL_REPLAN"
plan_artifact_class: "ctde_fresh_r3_portable_transitive_closure_plan"
plan_schema_version: "1.0.0"
planning_phase_id: "Phase 2-G-R3FRESH-P1"
planning_phase_kind: "fresh_r3_file_level_replan_and_deterministic_closure_planning_only"
future_r3_phase_id: "Phase 2-G-R3FRESH-E1"
future_r3_phase_kind: "fresh_r3_portable_transitive_closure_materialization_and_deterministic_verification"
future_r3_scope_status: "fresh_r3_plan_frozen_waiting_for_explicit_plan_bound_execution_authorization"
suite_id: "R3PS-20260814-001"
r3_result_artifact_path: "PORTABLE_RUNTIME_TRANSITIVE_CLOSURE_RESULT.md"
r3_write_scope_sha256: "8b1e9e4012bad4e60bbc9096a7b1b5841f55e48171ae6c1bb341a1d0383778c5"
execution_authorized: false
r3_execution_authorized: false
human_authorization_required: true
r4_execution_authorized: false
candidate_execution_authorized: false
```

The Plan's SHA-256 is external: it is computed from the exact persisted bytes after this file is created. No field inside this Plan claims to be its self-digest.

## 1. Frozen planning inputs

### 1.1 Planning contract and current-tree audit

| Exact path | SHA-256 | Bytes | Git identity |
| --- | --- | ---: | --- |
| `FRESH_R3_FILE_LEVEL_REPLAN_CONTRACT.md` | `0d68aff9948a2f50c31bcf40ca4a7a36fec3606048732c8398a45369358ee8b1` | 23,991 | `a0b5e742e55f07b81497d2dd3c2326e908363c23` |
| `FRESH_R3_CURRENT_TREE_AUDIT.json` | `3b1d7715548c6dcff8100b21986aa57f144653518d9d1dcdd88ce39d75635b16` | 99,836 | `75dff72d1a08fb6e4ff3790e24c39ee7b734f096` |

The audit is canonical compact sorted-key UTF-8 JSON with one terminal LF. It freezes 45 current Runtime/control/config/native files, 32 callable roots, 9 control/legacy entrypoints, 261 static closure edges, 23 non-Python config/data/native inputs, and all seven formal role identities. Future R3 must recompute every recorded digest from current disk bytes before the first project write.

### 1.2 Formal predecessor identities

```yaml
historical_r3p:
  path: "PORTABLE_RUNTIME_TRANSITIVE_CLOSURE_PLAN.md"
  sha256: "f8ca07eaee1fff534e97bf4a0d037ba73a3c1838107e132f7c072b1fe05b39f5"
  authority: "historical_requirement_input_only"
r3g03:
  result_path: "R3G03_MINIMAL_EMBEDDED_ROLE_MAPPING_RESULT.json"
  result_sha256: "78df12d69794d5fdc54d5e18c422744ec65ee6e898589ff8b833bb628e24e8b2"
  final_status: "PASS_R3G03_MINIMAL_EMBEDDED_ROLE_MAPPING"
r3g04:
  result_path: "R3G04_MINIMAL_EMBEDDED_ROLE_MAPPING_RESULT.json"
  result_sha256: "aee66549193c3608d689e004298fafa17cc5a26717f71d63f75335482d354090"
  final_status: "PASS_R3G04_MINIMAL_EMBEDDED_ROLE_MAPPING"
r3g07:
  result_path: "PORTABLE_RUNTIME_ROLE_GAP_R3G07_REPAIR_RESULT.md"
  result_sha256: "f5c93ed0dccea6c985dc16654742eea7ea42474e750d32a946b765468835654e"
  final_status: "PASS_PORTABLE_RUNTIME_ROLE_GAP_R3G07_REPAIRED"
```

The runtime/control baseline immediately after R3G04 was `4a090e123bade31add9249457726c96cf9030335`. The planning-only contract and audit commits changed no file under `runtime_capability_prototype/`; therefore the exact Runtime/control identities remain those in the audit. The immutable handoff tag remains `work-handoff-pre-r3g03-20260813 -> 063fa0eb9d74a4da4e15dec29164eb78fde33655`.

## 2. Assurance and scope ceiling

```yaml
assurance_profile_id: "CTDE-PORTABLE-DEV-1"
environment_class: "Development"
highest_claimed_evidence_level: "A1"
certified: false
hardened: false
candidate_ready: false
real_source_content_reads: 0
model_calls: 0
candidate_runs: 0
r4_execution: 0
business_outputs: 0
```

R3 proves a deterministic file/dependency/component freeze for the current Portable Runtime surface. It does not prove a hardened syscall-complete boundary, OS certification, Candidate execution, semantic source reading, independent model mediation, production deployment, or R4 synthetic E2E.

## 3. Current entrypoints and callable roots

### 3.1 Entrypoint decision

There is no current production CLI or orchestrator. The production Runtime roots are callable Python APIs. Existing executable Python entrypoints are test, build, or legacy control paths only:

| Path and callable | Classification |
| --- | --- |
| `runtime/build_manifest.py::main` | legacy manifest builder; excluded dependency |
| `runtime/build_r2_portable_manifest.py::main` | R2 build-only evidence |
| `runtime/build_r3g07_public_trust_test_manifest.py::main` | completed R3G07 test control |
| `runtime/run_suite.py::main` | legacy 197-leaf driver; excluded dependency |
| `runtime/run_r2_portable.py::main` | R2 test control |
| `runtime/run_r3g07_public_trust.py::main` | completed R3G07 test control |
| `runtime/verify_r3g07_public_trust.py::main` | completed R3G07 test verifier |
| `runtime/verify_trace.py::main` | legacy Hardened trace helper; excluded dependency |
| `runtime/build_r3g07_public_trust_result.py::build_report_bytes` | completed R3G07 importable result builder |

The future `runtime/run_r3_portable_closure.py::main` is a test/control entrypoint, never a production Runtime root.

### 3.2 Closed production/runtime callable-root set

Each root below is the exact `module::qualname` recorded by the audit, with `definition_count=1` and its containing file digest bound there:

```text
ctde_runtime.authorization_v2::load_authorization_v2
ctde_runtime.authorization_v2::validate_request_binding
ctde_runtime.authorization_v2::validate_activated_projection
ctde_runtime.authorization_registry::AuthorizationRegistry.register_authorization_v2
ctde_runtime.authorization_registry::AuthorizationRegistry.resolve_preconsume_v2
ctde_runtime.authorization_registry::AuthorizationRegistry.consume_authorization_v2
ctde_runtime.authorization_registry::AuthorizationRegistry.revoke_authorization_v2
ctde_runtime.authorization_registry::AuthorizationRegistry.claim_mint_lease_v2
ctde_runtime.authorization_registry::AuthorizationRegistry.prepare_capability_v2
ctde_runtime.authorization_registry::AuthorizationRegistry.activate_capability_v2
ctde_runtime.authorization_registry::AuthorizationRegistry.abort_mint_eligibility_v2
ctde_runtime.authorization_registry::AuthorizationRegistry.abort_preparation_v2
ctde_runtime.authorization_registry::AuthorizationRegistry.abort_activation_v2
ctde_runtime.authorization_registry::AuthorizationRegistry.validate_context_v2
ctde_runtime.range_broker::CapabilityIssuer.validate_preparation_binding_v2
ctde_runtime.range_broker::CapabilityIssuer.build_pending_capability_v2
ctde_runtime.range_broker::CapabilityIssuer.validate_activation_binding_v2
ctde_runtime.range_broker::RangeBroker.handle_request
ctde_runtime.range_broker::RangeBroker.validate_authorization_binding_v2
ctde_runtime.range_broker::RangeBroker.deliver
ctde_runtime.bounded_reader::BoundedReader.validate_authorization_binding_v2
ctde_runtime.bounded_reader::BoundedReader.consume
ctde_runtime.formal_loader::FormalLoader.load
ctde_runtime.read_audit::ReadAuditAggregator.validate_authorization_correlation_v2
ctde_runtime.read_audit::ReadAuditAggregator.create_scope_attestation
ctde_runtime.read_audit::ReadAuditAggregator.create_closure_attestation
ctde_runtime.events::SignedEventLog.append
ctde_runtime.events::SignedEventLog.verify
ctde_runtime.events::PortableA1EventLogV2.append
ctde_runtime.events::PortableA1EventLogV2.verify
ctde_runtime.sandbox::SandboxSupervisor.run
ctde_runtime.public_trust::load_portable_public_trust
```

The 32 roots define traversal starts, not a reduced closure. `common.py`, `signing.py`, `fixture_factory.py`, package initializers, schemas, configurations, native boundaries, interpreter, distributions, and other reachable nodes remain mandatory when actually reachable.

## 4. Seven-role reconciliation

The formal role inventory remains seven. Fresh R3 uses the following sole current-stage disposition table:

| Gap ID | Fresh R3 disposition | Active R3 blocker | Evidence/future rule |
| --- | --- | ---: | --- |
| `R3G-01-PORTABLE-R4-SUITE-MANIFEST-BUILDER` | `stage_scoped_deferred_to_R4` | false | R4-specific builder bytes do not exist; R4P must define them and trigger a new closure refresh |
| `R3G-02-PORTABLE-R4-SUITE-RUNNER` | `stage_scoped_deferred_to_R4` | false | R3 closure runner cannot impersonate R4 suite runner |
| `R3G-03-BOUNDED-PARSER-SCOPE` | `fulfilled_by_minimal_embedded_role_mapping` | false | exact PASS result `78df12d6…e8b2`; stronger independent parser deferred to R4 |
| `R3G-04-DISCARD-ONLY-MODEL-GATEWAY` | `fulfilled_by_minimal_embedded_role_mapping` | false | exact PASS result `aee66549…4090`; real/independent gateway deferred to R4/Candidate |
| `R3G-05-PORTABLE-LOGICAL-WRITE-MONITOR` | `stage_scoped_deferred_to_R4` | false | logical publisher/output monitor waits for R4 paths; syscall-complete monitoring remains Hardened-only |
| `R3G-06-PORTABLE-R4-AGGREGATE-REPORT-GENERATOR` | `stage_scoped_deferred_to_R4` | false | R3 result generator is closure-only and cannot impersonate R4 aggregation |
| `R3G-07-IMMUTABLE-PUBLIC-TRUST-KEY-STATUS` | `fulfilled_by_r3g07_repair` | false | exact public-trust freeze identity is an R3 input |

```yaml
formal_role_inventory_count: 7
fulfilled_role_count: 3
stage_scoped_deferred_role_count: 4
active_r3_role_gap_count: 0
role_identity_deleted_count: 0
```

Any drift in R3G03, R3G04, or R3G07 reactivates the corresponding blocker. Any appearance of R4-specific implementation bytes invalidates this closure and requires a fresh R3 refresh before R4 execution.

## 5. Public trust and signed-role binding

```yaml
public_trust_freeze_identity: "7a4a664a8fcccea98ee600d853fc9d36107e307ec2e7e078c9fad42363a831f3"
kid: "ctde-portable-dev-20260813-01"
public_key_bytes_sha256: "32a457033c8eefa8bea45ce347cb17ef08c928fabf7c2139ead1ab8af29aef5f"
public_key_status: "active"
trust_material_sha256: "dcac3ed439a24639736b01f035ef121ac025bd7c9e93882040c7ebcc7350e3cc"
status_registry_sha256: "d0e13ff804bbd224146133b67853b4256756fbd4c995c8045edadfdbc576bc4d"
loader_sha256: "72103c6de973a7f575c553681edcf097c46123d263c81b0edbdbed28f94dd5b8"
signing_sha256: "5c41a1601b9824715d17ae416513646575006a9207dedd26bb2036336e66cc36"
trust_domain: "ctde-portable-runtime"
private_key_dependency: false
```

`runtime_capability_prototype/r3g07_portable_suites/R3G07PS-20260812-001/fixtures/r3g07_test_signing_key_ed25519_seed.hex`, SHA-256 `e6da730935c44bba9f380afb0845844e04dbef6e61bcaabfbe7dfbf03fa5e699`, is test-only reproducibility material. It is never a production/private trust root and is not loaded by production Runtime closure.

R3 must freeze the public trust material, status registry, their schemas, `public_trust.py`, `signing.py`, and actual caller edges. It may read public records and test-only evidence. It may not generate trust assets, rotate the key, read a production private key, or reinterpret the test seed.

## 6. Exact future R3 write scope

### 6.1 Canonical identity

The write-scope object is compact key-sorted UTF-8 JSON without a terminal LF. Arrays retain the exact order printed in sections 6.2 and 6.3.

```yaml
canonicalization_id: "CTDE-CANONICAL-JSON-SORTED-COMPACT-NO-LF-1"
canonical_byte_length: 3815
r3_write_scope_sha256: "8b1e9e4012bad4e60bbc9096a7b1b5841f55e48171ae6c1bb341a1d0383778c5"
mutable_existing_files: []
creatable_file_count: 31
creatable_directory_count: 11
```

No existing project file may be modified. Every path not explicitly listed is default-deny.

### 6.2 Sole creatable files

```text
runtime_capability_prototype/contracts/r3_portable_closure_policy_v1.yaml
runtime_capability_prototype/contracts/runtime_transitive_closure_manifest_schema_v1.yaml
runtime_capability_prototype/contracts/component_freeze_schema_v1.yaml
runtime_capability_prototype/contracts/execution_snapshot_closure_binding_schema_v1.yaml
runtime_capability_prototype/contracts/r3_portable_closure_test_requirements.yaml
runtime_capability_prototype/contracts/r3_portable_test_manifest_schema_v1.yaml
runtime_capability_prototype/contracts/r3_portable_controller_terminal_schema_v1.yaml
runtime_capability_prototype/contracts/native_component_build_policy_v1.yaml
runtime_capability_prototype/contracts/closure_snapshot_registry_record_schema_v1.yaml
runtime_capability_prototype/contracts/r3_portable_closure_control_artifact_schema_v1.yaml
runtime_capability_prototype/runtime/build_r3_portable_closure.py
runtime_capability_prototype/runtime/build_r3_portable_test_manifest.py
runtime_capability_prototype/runtime/verify_r3_portable_closure.py
runtime_capability_prototype/runtime/run_r3_portable_closure.py
runtime_capability_prototype/runtime/build_r3_portable_result.py
runtime_capability_prototype/r3_portable_suites/R3PS-20260814-001/control/r3_implementation_manifest.json
runtime_capability_prototype/r3_portable_suites/R3PS-20260814-001/control/r3_execution_plan.json
runtime_capability_prototype/r3_portable_suites/R3PS-20260814-001/control/runtime_transitive_closure_manifest.json
runtime_capability_prototype/r3_portable_suites/R3PS-20260814-001/control/r3_synthetic_test_manifest.json
runtime_capability_prototype/r3_portable_suites/R3PS-20260814-001/control/component_freeze.json
runtime_capability_prototype/r3_portable_suites/R3PS-20260814-001/control/execution_snapshot_closure_binding.json
runtime_capability_prototype/r3_portable_suites/R3PS-20260814-001/control/closure_snapshot_registry_record.json
runtime_capability_prototype/r3_portable_suites/R3PS-20260814-001/fixtures/r3_synthetic_fixtures.json
runtime_capability_prototype/r3_portable_suites/R3PS-20260814-001/attempts/r3_attempts.jsonl
runtime_capability_prototype/r3_portable_suites/R3PS-20260814-001/evidence/start/closure_start_verification.json
runtime_capability_prototype/r3_portable_suites/R3PS-20260814-001/evidence/dynamic/dynamic_dependency_observation.json
runtime_capability_prototype/r3_portable_suites/R3PS-20260814-001/evidence/end/closure_end_verification.json
runtime_capability_prototype/r3_portable_suites/R3PS-20260814-001/evidence/controller_terminal/controller_terminals.jsonl
runtime_capability_prototype/r3_portable_suites/R3PS-20260814-001/evidence/evidence_manifest.json
runtime_capability_prototype/r3_portable_suites/R3PS-20260814-001/aggregate/r3_portable_closure_results.json
PORTABLE_RUNTIME_TRANSITIVE_CLOSURE_RESULT.md
```

The first 15 paths are the implementation/control-code bundle. The final 16 are suite control, fixture, evidence, aggregate, and formal result artifacts. No implementation manifest digest exists before execution; the human authority binds this Plan and its exact scope. The implementation manifest is then the create-once canonical inventory of the actual 15-file bundle and must be independently validated before any suite artifact is created.

### 6.3 Sole creatable directories

```text
runtime_capability_prototype/r3_portable_suites/
runtime_capability_prototype/r3_portable_suites/R3PS-20260814-001/
runtime_capability_prototype/r3_portable_suites/R3PS-20260814-001/control/
runtime_capability_prototype/r3_portable_suites/R3PS-20260814-001/fixtures/
runtime_capability_prototype/r3_portable_suites/R3PS-20260814-001/attempts/
runtime_capability_prototype/r3_portable_suites/R3PS-20260814-001/evidence/
runtime_capability_prototype/r3_portable_suites/R3PS-20260814-001/evidence/start/
runtime_capability_prototype/r3_portable_suites/R3PS-20260814-001/evidence/dynamic/
runtime_capability_prototype/r3_portable_suites/R3PS-20260814-001/evidence/end/
runtime_capability_prototype/r3_portable_suites/R3PS-20260814-001/evidence/controller_terminal/
runtime_capability_prototype/r3_portable_suites/R3PS-20260814-001/aggregate/
```

OS temporary directories are not project artifacts. They must be outside the project, contain only the exact frozen member subset needed for a test, and be deleted after use.

## 7. Read-only and forbidden boundaries

The following are read-only inputs:

- all 45 `runtime_file_identities` in `FRESH_R3_CURRENT_TREE_AUDIT.json`;
- all 12 `formal_source_identities` in that audit;
- the audit and this Plan;
- R3G07 suite public/test evidence needed to revalidate the frozen public-trust result;
- selected R2 and legacy control evidence only when used as historical comparison, never as active Runtime bytes.

All current files under `runtime_capability_prototype/` remain immutable. The only exception is creation of the 30 new paths under that subtree listed in section 6.2.

Forbidden reads/writes include:

1. English or Greek TEI content;
2. `book_structure_map.yaml` content;
3. Candidate payloads, invalid Run 001/002 payload reuse, or any new Candidate root;
4. real-source hashing performed by opening source bodies;
5. production/private key material, credentials, cookies, sessions, tokens, or `.env` secrets;
6. any model API, prompt construction, payload mediation, or business output;
7. any R4 builder, runner, write monitor, aggregate/report generator, or publisher implementation;
8. caches, `.codex/`, `.agents/`, `.git/`, OS temp, or local debug files as closure members.

Source Layer presence may be checked by directory-entry metadata without opening content. R3 synthetic tests must remain no-content.

## 8. Closure graph and classification contract

### 8.1 Closed node classifications

Every node has exactly one primary closure classification:

```text
runtime_closure_member
test_only_dependency
build_only_dependency
platform_boundary
excluded_dependency
```

`member_type` is orthogonal and uses a closed vocabulary including `python_module`, `package_initializer`, `schema`, `policy`, `configuration`, `public_trust_record`, `native_source`, `native_executable`, `interpreter`, `stdlib_module`, `distribution_file`, `shared_library`, `control_builder`, `verification_code`, `test_runner`, `evidence_schema`, and `external_registry_record`.

Test/build/legacy labels cannot hide actual production reachability. If a production callable root reaches a node classified test-only or excluded, R3 is BLOCKED unless the policy's exact current-stage classification requires it and the manifest records that fact without weakening the claim.

### 8.2 Static discovery

The closure builder must deterministically traverse:

1. the 32 callable roots, exact containing modules, and package initializers;
2. Python `import` and `from` edges, including relative imports and reachable symbol bodies;
3. module-level constants and path construction used for schema, policy, config, data, public-trust, executable, or native loads;
4. direct and indirect project-owned file opens;
5. `importlib`, plugin, dynamic module, reflection, and late-binding sites;
6. subprocess/executable invocations and fixed child-environment construction;
7. `ctypes` and native/shared-library resolution;
8. native source, compiler identity, version, flags, include/link inputs, build recipe, output, ABI, loader, and reproducible rebuild identity;
9. Python interpreter, all relevant stdlib module origins, distribution metadata and file trees for PyYAML and cryptography, and their native dependencies;
10. symlinks and resolved targets, with unresolved links equal to zero;
11. every R3 builder, verifier, runner, schema, policy, manifest, evidence, aggregate, result generator, and external-registry record.

String matching alone is not a complete locator. AST/source locators must identify exact semantic nodes. The verifier may not select the first generic raise, first open, or first matching string when multiple candidates exist.

### 8.3 Edge vocabulary

Each edge is sorted by `(from_id,to_id,relation,locator)` and uses one of:

```text
imports
initializes_package
calls
loads_schema
loads_policy
loads_config
loads_public_trust
executes
dlopens
builds_from
links_to
resolves_to
observes
verifies
classified_by
binds_identity
```

Unknown relation, target, dynamic dependency, project-owned loaded byte, or symlink target is BLOCKED.

### 8.4 R3G03/R3G04 role edges

The closure manifest must bind, without re-execution:

- R3G03's five Runtime paths, six callable identities, parser-scope identity, signed audit correlation, and exact result digest;
- R3G04's two minimal role members, support paths, selected callables, gateway event fields, Book 2 fail-closed injection identity, audit correlation, R3G03 prerequisite, and exact result digest;
- both mappings' `existing_file_modification_count=0` and `runtime_modification_count=0` ledgers.

The current embedded parser/gateway mapping is sufficient only for Portable / Development / A1 identity. R3 must not call the parser on real content, inject Book 2 into a real payload, or invoke a model.

## 9. Canonical closure artifacts

### 9.1 Closure manifest

`runtime_transitive_closure_manifest.json` is canonical compact sorted-key UTF-8 JSON with terminal LF and a closed schema. It must contain:

- schema/artifact/canonicalization identity;
- Plan, audit, phase, suite, profile, Git, and public-trust identities;
- root callables;
- nodes with stable IDs, classification, member type, exact path/origin, byte digest, size, and platform identity as applicable;
- edges with exact locators;
- role inventory and dispositions;
- static discovery summary, dynamic observation contract, unknown/unresolved counts;
- canonical payload digest excluding only the explicitly named payload-digest field.

Two independent fresh-process builds over the same frozen inputs must produce byte-identical payload and full manifest bytes.

### 9.2 Component freeze

`component_freeze.json` must cover every runtime, test, build, platform, excluded, control, verifier, runner, schema, policy, public-trust, native, interpreter, distribution, shared-library, environment, and external-registry node. It must bind the exact closure manifest file digest and payload digest.

Legacy `build_manifest.py`, `run_suite.py`, `verify_trace.py`, and `contracts/component_manifest.yaml` are frozen excluded nodes with current exact digests and non-reachability evidence. `common.py`, `signing.py`, `public_trust.py`, and `ctde_runtime/__init__.py` are real closure members when reachable.

### 9.3 Snapshot binding and external registry

`execution_snapshot_closure_binding.json` binds the execution plan, closure manifest, test manifest, fixture catalog, component freeze, fixed environment, suite ID, and public trust identity. `closure_snapshot_registry_record.json` is created by an independent controller pass that rehashes committed closure/freeze/binding bytes; the closure builder may not create or mutate it.

No artifact self-hashes its complete file. The chain is:

```text
closure payload digest
-> closure manifest exact file digest
-> component freeze and execution snapshot binding
-> independent external registry record
-> start/end verification and aggregate
-> formal root result
```

## 10. Dynamic observation and platform closure

Dynamic observation is no-content and supplements static discovery. The future runner must use isolated processes, disable bytecode writes, use a fixed minimal environment, capture module origins and file/config opens, and prevent project-tree writes outside the allowlist. It must not import project Runtime before start verification completes.

The execution environment must newly capture rather than reuse historical Linux observations:

- resolved interpreter bytes and link mode;
- relevant stdlib module origins/digests;
- PyYAML and cryptography distribution versions, metadata, complete relevant file trees, native modules, and shared libraries;
- native probe format, source digest, compiler path/version, flags, include/link inputs, loader/libc or Windows runtime boundary, and rebuilt binary digest;
- OS/kernel boundary and `/proc` semantics when applicable;
- all environment names that affect import, loader, subprocess, temp, locale, time, or hashing behavior;
- child process executable, arguments, inherited handles/descriptors, and fixed environment.

No hard-coded operating-system path or historical interpreter digest is a PASS substitute. If the current environment cannot supply a finite, independently verifiable platform boundary, R3 is BLOCKED rather than silently downgraded.

## 11. Implementation and artifact ownership

| Persistent artifact class | Sole producer | Write rule |
| --- | --- | --- |
| first 15 implementation files | authorized implementation materializer | construct as one complete bundle; create-only; no existing-file edits |
| `r3_implementation_manifest.json` | same materializer | canonical exact path/digest/size inventory for all 15 files; committed with the complete bundle |
| `r3_execution_plan.json` | R3 controller bootstrap | only after independent implementation-manifest validation |
| closure manifest | closure builder returns bytes; controller persists | phase 1 only; builder never writes project tree |
| test manifest and fixture catalog | test-manifest builder returns bytes; controller persists | derived from frozen closure manifest and requirements; no fixed leaf count |
| component freeze and snapshot binding | closure builder phase 2 returns bytes; controller persists | cannot alter phase-1 manifest |
| external registry record | independent controller registry pass | rehashes already persisted exact bytes |
| start/end verification | verifier returns bytes; controller persists | verifier has no project write authority |
| dynamic observation, attempts, terminal ledger | controller | dynamic evidence create-once; JSONL append only by controller |
| evidence manifest, aggregate, final report | result generator returns bytes; controller persists | generator has no direct project write authority |

The implementation bundle and manifest must appear in one scoped materialization operation. Any partial bundle without its complete canonical manifest is `BLOCKED_R3_PARTIAL_MATERIALIZATION`; the executor must stop and request a separately authorized repair, not improvise or overwrite.

## 12. Execution stages and resume rules

### 12.1 Stages

```yaml
stages:
  - id: "R3-S0-AUTH"
    action: "validate exact human authorization, Plan/audit digests, clean tree, absent write paths, current Git/remote/tag identities"
  - id: "R3-S1-IMPLEMENTATION"
    action: "materialize and independently validate the 15-file implementation bundle plus implementation manifest"
  - id: "R3-S2-BOOTSTRAP"
    action: "create execution plan bound to authorization, Plan, audit, implementation manifest, profile, suite, fixed time, and write scope"
  - id: "R3-S3-MANIFEST"
    action: "two-pass static closure build; persist byte-identical canonical closure manifest"
  - id: "R3-S4-TEST-CONTROL"
    action: "expand actual test leaves; create test manifest and synthetic no-content fixture catalog"
  - id: "R3-S5-FREEZE"
    action: "create component freeze, execution snapshot binding, and independent external registry record"
  - id: "R3-S6-START"
    action: "independent start verification before Runtime import or test execution"
  - id: "R3-S7-OBSERVE"
    action: "run deterministic no-content leaves and capture dynamic observation, attempts, and controller terminals"
  - id: "R3-S8-END"
    action: "independent end verification and start/end delta comparison"
  - id: "R3-S9-RESULT"
    action: "create evidence manifest, aggregate, and formal result from independently rehashed inputs"
  - id: "R3-S10-GIT"
    action: "verify exact changeset, secret boundary, tests, and baseline tag; commit and normally push one atomic R3 PASS"
```

### 12.2 Resume

Resume is permitted only under the same human authorization, exact Plan/audit digests, phase, suite, profile, write scope, implementation manifest, execution plan, and Git ancestor. Existing artifacts must validate byte-for-byte and be a strict valid prefix of the stage ledger. Create-once artifacts cannot be regenerated, rewritten, or repaired in place.

If an existing artifact is invalid, an unexpected path exists, the stage prefix is impossible, the project tree contains unrelated changes, remote main diverges, or a producer identity differs, stop with `BLOCKED_R3_RESUME_IDENTITY_MISMATCH`. No automatic new suite identity is authorized.

## 13. Future deterministic verification contract

`r3_portable_closure_test_requirements.yaml` defines these closed requirement groups. The test-manifest builder expands actual leaves from the frozen node/edge/member inventories; `N` is discovered at execution and must not be preset to a historical count.

| Group | Required proof |
| --- | --- |
| `R3-VG01` | exact human authorization, Plan, audit, Git, suite, profile, and write-scope identity |
| `R3-VG02` | implementation manifest and all implementation file digests/schemas |
| `R3-VG03` | callable roots, required current-stage roles, node types, and classifications |
| `R3-VG04` | complete Python imports, package initializers, callable references, and project-owned loads |
| `R3-VG05` | schemas, policies, configs, public trust/status, and formal result dependencies |
| `R3-VG06` | dynamic import/plugin/reflection sites and unknown dynamic dependency count zero |
| `R3-VG07` | subprocess/executable, environment, handle/descriptor, and process boundaries |
| `R3-VG08` | native source -> recipe -> compiler/link inputs -> binary reproducibility |
| `R3-VG09` | interpreter, stdlib, distributions, shared libraries, loader/ABI, and OS boundary |
| `R3-VG10` | R3G03 parser-scope mapping identity and current closure edges |
| `R3-VG11` | R3G04 discard-only gateway mapping identity, zero model calls, no payload persistence |
| `R3-VG12` | R3G07 public-trust identity, active key status, caller binding, no private-key dependency |
| `R3-VG13` | R3G01/02/05/06 retained stage-scoped R4 dispositions and active R3 gap count zero |
| `R3-VG14` | two-pass canonical manifest reproducibility and closed schema validation |
| `R3-VG15` | component freeze, snapshot binding, and external registry independent recomputation |
| `R3-VG16` | start/dynamic/end agreement, complete observed-open set, and closure delta zero |
| `R3-VG17` | no existing-file mutation, no forbidden path, no source-content read, no Candidate/R4/model work |
| `R3-VG18` | evidence manifest, aggregate, formal result, actual leaf counts, and A1 claim ceiling |

Every leaf has a stable ID derived from the frozen requirement plus subject identity, an expected value, observed value, exact evidence locator, method, and terminal result. PASS requires:

```yaml
requirement_groups: 18
leaves_discovered: N
leaves_executed: N
evidence_complete: N
leaves_passed: N
failed: 0
skipped: 0
unknown: 0
timeout: 0
unknown_project_owned_loaded_bytes: 0
unresolved_symlinks: 0
closure_delta_count: 0
existing_project_file_modifications: 0
scope_violations: 0
model_calls: 0
source_content_reads: 0
```

No self-described PASS, expected-equals-actual substitution, first-match locator, hidden skip, reduced inventory, or test-only label can create PASS.

## 14. Upstream requirement mapping

| Requirement | Implementation/control | Independent evidence |
| --- | --- | --- |
| `P2GR-R3-001` roots, node types, platform and public-trust boundary | closure policy/schema/builder | manifest + start verification |
| `P2GR-R3-002` formal seven-role inventory and known legacy nodes in graph | policy + R3G03/04/07 bindings + four deferred dispositions | manifest + role records + start verification |
| `P2GR-R3-003` static, dynamic, and actual code/config open agreement | builder + no-content controller | dynamic observation + end verification |
| `P2GR-R3-004` unknown/unresolved/project-owned-unregistered/symlink counts zero | schema + builder | manifest + aggregate |
| `P2GR-R3-005` native source/build recipe/toolchain/link/binary closure | native build policy + builder | independent rebuild + start/end evidence |
| `P2GR-R3-006` current-stage Runtime schemas/policies/builders/runners/verifiers/results frozen | implementation manifest + component freeze | independent verifier + aggregate; R4-only roles retained deferred, never impersonated |
| `P2GR-R3-007` full start/end digest match and delta zero | controller + verifier | start/end evidence + aggregate |
| `P2GR-R3-008` payload/file/external-registry identities independently recomputable | closure schema + registry schema + controller | registry record + start/end + aggregate |

The fresh interpretation of `P2GR-R3-006` does not delete R4 roles. It requires zero unresolved roles for the current R3 stage, with exact formal dispositions for the four R4-scoped roles.

## 15. PASS and BLOCKED semantics

The future R3 PASS status is:

```text
PASS_PORTABLE_RUNTIME_TRANSITIVE_CLOSURE
```

The unified failure status is:

```text
BLOCKED_PORTABLE_RUNTIME_TRANSITIVE_CLOSURE
```

Pre-write authorization or scope failure uses `BLOCKED_PORTABLE_R3_EXECUTION_GATE_FAILED`. Partial materialization uses `BLOCKED_R3_PARTIAL_MATERIALIZATION`. Resume identity failure uses `BLOCKED_R3_RESUME_IDENTITY_MISMATCH`.

PASS means the exact current Portable Runtime/control surface is transitively closed, frozen, reproducibly described, and supported by complete A1 deterministic evidence. PASS does not mean R4 PASS, Candidate readiness, real source access, model gateway implementation, production certification, or hardened isolation.

## 16. Exact future human authorization gate

R3 execution requires a new human message after this Plan is persisted and published. The message must quote the exact values below, replacing only the digest placeholder with the actual persisted Plan SHA-256:

```yaml
current_status: "READY_FOR_R3_EXECUTION_AUTHORIZATION_REVIEW"
plan_path: "FRESH_R3_PORTABLE_TRANSITIVE_CLOSURE_PLAN.md"
plan_sha256: "<exact persisted Plan SHA-256>"
current_tree_audit_path: "FRESH_R3_CURRENT_TREE_AUDIT.json"
current_tree_audit_sha256: "3b1d7715548c6dcff8100b21986aa57f144653518d9d1dcdd88ce39d75635b16"
phase_id: "Phase 2-G-R3FRESH-E1"
phase_kind: "fresh_r3_portable_transitive_closure_materialization_and_deterministic_verification"
scope_status: "fresh_r3_plan_frozen_waiting_for_explicit_plan_bound_execution_authorization"
suite_id: "R3PS-20260814-001"
r3_result_artifact_path: "PORTABLE_RUNTIME_TRANSITIVE_CLOSURE_RESULT.md"
r3_write_scope_sha256: "8b1e9e4012bad4e60bbc9096a7b1b5841f55e48171ae6c1bb341a1d0383778c5"
approval_scope: "fresh R3 implementation materialization and deterministic Portable closure verification only"
```

The approval applies to one R3 attempt under this exact Plan and suite identity. It does not authorize R4, Candidate, source reading, model calls, or business output. An agent-authored Plan, commit, or execution artifact cannot substitute for the human message.

## 17. Planning-phase deterministic verification

The fresh planning phase expanded and checked the 18 groups defined by `FRESH_R3_FILE_LEVEL_REPLAN_CONTRACT.md`. Its actual closed count is:

```yaml
planning_requirement_groups: 18
planning_leaves_discovered: 527
planning_leaves_executed: 527
planning_evidence_complete: 527
planning_leaves_passed: 527
planning_failed: 0
planning_skipped: 0
planning_unknown: 0
planning_timeout: 0
runtime_modifications: 0
runtime_executions: 0
model_calls: 0
english_tei_content_reads: 0
greek_tei_content_reads: 0
candidate_runs: 0
business_outputs: 0
```

The 527 leaves are the actual expansion over Git/formal identities, 45 file identities, 9 entrypoints, 32 callable roots, 254 Python-import/package-initializer edges, 30 config/native/executable identities, seven role records, the 31-file/11-directory write scope, algorithms, lifecycle rules, zero-action ledgers, canonicalization, claim ceiling, and human gate. It is a planning verification count only; it is not the future R3 test leaf count `N`.

## 18. Post-R3 logical successor

If and only if future R3 passes and is independently committed/pushed, its logical successor is Portable R4 synthetic E2E planning/execution under a new machine contract. This Plan does not define that future contract:

```yaml
logical_successor: "Portable R4 synthetic E2E planning"
successor_machine_contract_defined: false
successor_execution_authorized: false
next_phase_id: null
next_phase_kind: null
scope_status: null
```

R4 implementation bytes, suite ID, write scope, and authorization must be defined by a later formal contract. Their appearance invalidates this R3 closure until a fresh refresh.

## 19. Terminal machine gate

```yaml
current_status: "READY_FOR_R3_EXECUTION_AUTHORIZATION_REVIEW"
next_phase_id: "Phase 2-G-R3FRESH-E1"
next_phase_kind: "fresh_r3_portable_transitive_closure_materialization_and_deterministic_verification"
scope_status: "fresh_r3_plan_frozen_waiting_for_explicit_plan_bound_execution_authorization"
execution_authorized: false
r3_execution_authorized: false
human_authorization_required: true
plan_path: "FRESH_R3_PORTABLE_TRANSITIVE_CLOSURE_PLAN.md"
current_tree_audit_path: "FRESH_R3_CURRENT_TREE_AUDIT.json"
current_tree_audit_sha256: "3b1d7715548c6dcff8100b21986aa57f144653518d9d1dcdd88ce39d75635b16"
suite_id: "R3PS-20260814-001"
r3_result_artifact_path: "PORTABLE_RUNTIME_TRANSITIVE_CLOSURE_RESULT.md"
r3_write_scope_sha256: "8b1e9e4012bad4e60bbc9096a7b1b5841f55e48171ae6c1bb341a1d0383778c5"
```

Stop here until a human supplies the exact Plan-bound authorization payload in section 16.
