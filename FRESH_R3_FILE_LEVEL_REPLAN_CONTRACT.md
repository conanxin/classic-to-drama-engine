# Fresh R3 File-Level Replan Machine Contract

## 0. Contract conclusion and boundary

This contract defines the machine phase that replaces the historical pre-adjudication R3 plan with a current-tree, file-level Portable R3 closure plan. It authorizes planning artifacts only. It does not materialize the R3 implementation bundle, execute R3, execute R4, start a Candidate Run, read English or Greek TEI content, invoke a model, or create business output.

```yaml
contract_definition_status: "PASS_FRESH_R3_FILE_LEVEL_REPLAN_CONTRACT_DEFINED"
planning_phase:
  phase_id: "Phase 2-G-R3FRESH-P1"
  phase_kind: "fresh_r3_file_level_replan_and_deterministic_closure_planning_only"
  scope_status_before_execution: "planning_contract_defined_under_standing_human_planning_authority"
  planning_execution_authorized: true
  r3_execution_authorized: false
current_tree_audit_artifact_path: "FRESH_R3_CURRENT_TREE_AUDIT.json"
fresh_r3_plan_artifact_path: "FRESH_R3_PORTABLE_TRANSITIVE_CLOSURE_PLAN.md"
planning_write_scope_sha256: "befb8af99a450c298152330d950cea2521b00a1ce209fa42583acc42155fe8f9"
r3_execution_count: 0
r4_execution_count: 0
candidate_run_count: 0
model_call_count: 0
english_tei_content_read_count: 0
greek_tei_content_read_count: 0
business_output_count: 0
```

The planning authority above is the user's standing authority for contract definition, contract reconciliation, scope audit, file-level replan, closure/dependency planning, and deterministic static verification. It is not an authorization for a future R3 execution whose Plan digest, execution phase identity, suite identity, and write-scope identity do not exist until this planning phase completes.

## 1. Normative source identities

The following exact files are the closed normative source set. Each digest was recomputed from current disk bytes before this contract was created.

| Exact path | SHA-256 | Bytes | Purpose |
| --- | --- | ---: | --- |
| `R3G03_MINIMAL_EMBEDDED_ROLE_MAPPING_CONTRACT.md` | `208a9fa5a6fc098068cb247102918f3e97273c71bad840366ccc285179720602` | 38,478 | parser-scope mapping contract |
| `R3G03_MINIMAL_EMBEDDED_ROLE_MAPPING_RESULT.json` | `78df12d69794d5fdc54d5e18c422744ec65ee6e898589ff8b833bb628e24e8b2` | 43,047 | parser-scope PASS identity |
| `R3G04_MINIMAL_EMBEDDED_ROLE_MAPPING_CONTRACT.md` | `cb8a7af7c25c386bcad65af14aaacdb5e295ced66ce20bf0de0b22e627985d4a` | 41,248 | discard-only gateway mapping contract |
| `R3G04_MINIMAL_EMBEDDED_ROLE_MAPPING_RESULT.json` | `aee66549193c3608d689e004298fafa17cc5a26717f71d63f75335482d354090` | 56,223 | discard-only gateway PASS identity and fresh-replan successor |
| `PORTABLE_RUNTIME_ROLE_GAP_R3G07_REPAIR_RESULT.md` | `f5c93ed0dccea6c985dc16654742eea7ea42474e750d32a946b765468835654e` | 11,811 | public-trust repair PASS identity |
| `PORTABLE_RUNTIME_PUBLIC_TRUST_BINDING_PLAN.md` | `fbd689f287be47aa5aa9cc3ebb256c9b7512101be073d92b1d27ae65ce0c577a` | 64,046 | immutable public-trust contract |
| `PORTABLE_RUNTIME_ROLE_GAP_RESOLUTION_PLAN.md` | `72f116ff0b93403961a045228706f9322deea008f41718acae6178b0780b8798` | 47,613 | seven-gap adjudication |
| `PORTABLE_RUNTIME_TRANSITIVE_CLOSURE_PLAN.md` | `f8ca07eaee1fff534e97bf4a0d037ba73a3c1838107e132f7c072b1fe05b39f5` | 85,839 | historical R3P and closure algorithm input |
| `RUNTIME_CAPABILITY_REPAIR_PLAN.md` | `a2c52dbaecf3956cf4a2189abe5401f269d255e8099d3345985619be25be4213` | 45,397 | upstream R3/R4 requirements |
| `RUNTIME_ASSURANCE_PROFILE_DECISION.md` | `57471c85c57946f6ceb6da288301cc802533b09c137bfbe8e6e247dad57206e2` | 29,635 | Portable / Development / A1 claim ceiling |
| `CANDIDATE_EXECUTION_CONTRACT_REPAIR.md` | `12ceb01cab4901cb2b7472b1b56f93750a43cb8c28b5f0c9ab89acf3ad4fe7bd` | 76,814 | Candidate and content boundary |

The historical R3P remains evidence and a requirement source. Its old suite identity, old environment observations, unresolved role-gap state, and old proposed authorization bundle are not current machine authority and may not be copied without current-tree reconciliation.

## 2. Recovered current gate

```yaml
predecessor_phase_id: "Phase 2-G-R3G04-M1"
predecessor_status: "PASS_R3G04_MINIMAL_EMBEDDED_ROLE_MAPPING"
predecessor_result_path: "R3G04_MINIMAL_EMBEDDED_ROLE_MAPPING_RESULT.json"
predecessor_result_sha256: "aee66549193c3608d689e004298fafa17cc5a26717f71d63f75335482d354090"
logical_successor: "fresh R3 file-level replan"
successor_machine_contract_defined_by_predecessor: false
successor_execution_authorized_by_predecessor: false
```

The missing successor contract is supplied by this file. Undefined machine fields in the predecessor are not execution authority. They also are not a reason to abandon planning, because the standing human instruction explicitly authorizes definition of this planning contract and completion of all planning work possible before a new digest-bound execution gate.

## 3. Planning write scope

The canonical write-scope object is the following compact, key-sorted UTF-8 JSON byte sequence without a terminal LF:

```json
{"creatable_directories":[],"creatable_files":["FRESH_R3_CURRENT_TREE_AUDIT.json","FRESH_R3_PORTABLE_TRANSITIVE_CLOSURE_PLAN.md"],"mutable_existing_files":[]}
```

```yaml
canonicalization_id: "CTDE-CANONICAL-JSON-SORTED-COMPACT-NO-LF-1"
canonical_byte_length: 158
planning_write_scope_sha256: "befb8af99a450c298152330d950cea2521b00a1ce209fa42583acc42155fe8f9"
mutable_existing_files: []
creatable_directories: []
creatable_files:
  - "FRESH_R3_CURRENT_TREE_AUDIT.json"
  - "FRESH_R3_PORTABLE_TRANSITIVE_CLOSURE_PLAN.md"
```

Each artifact is create-once. The audit-only subset digest is `cb5c795a755df5652d3fb887d0e6b53fb17c491ab6f1baab97f50871c8a05bfe`; the Plan-only subset digest is `bcf5f42e3c59a37247061ff6a1a1c6c6b8b3836c9f4f6df52070ede3a65c367d`. No runner, helper, manifest, schema, evidence directory, result, Runtime source, suite directory, or debug artifact may be created in this planning phase. Static analysis helpers, if needed, must remain in OS temporary storage and be removed before each project commit.

## 4. Current-tree audit artifact contract

### 4.1 Identity and canonical bytes

```yaml
artifact_path: "FRESH_R3_CURRENT_TREE_AUDIT.json"
schema_id: "urn:ctde:contract:fresh-r3-current-tree-audit:1"
schema_version: "1.0.0"
artifact_class: "ctde_fresh_r3_current_tree_audit"
canonicalization_id: "CTDE-FRESH-R3-AUDIT-JCS-1"
encoding: "UTF-8"
json_form: "compact_sorted_keys"
terminal_lf_required: true
self_digest_field: null
self_digest_rule: "artifact digest is external; no self-digest field is permitted"
```

The closed top-level field set is exactly:

```yaml
closed_top_level_fields:
  - "action_ledger"
  - "artifact_class"
  - "assurance_identity"
  - "audit_summary"
  - "callable_roots"
  - "canonicalization_id"
  - "closure_edges"
  - "config_and_data_inputs"
  - "entrypoint_inventory"
  - "formal_source_identities"
  - "git_identity"
  - "platform_observation_policy"
  - "role_gap_dispositions"
  - "runtime_file_identities"
  - "schema_id"
  - "schema_version"
  - "signed_role_binding"
```

Every object below the top level must also be closed by the audit renderer's literal construction. Duplicate JSON keys, non-JSON numbers, locale-dependent values, absolute workspace paths, timestamps, usernames, process IDs, and unordered filesystem iteration are forbidden.

### 4.2 Required audit surface

The audit is read-only and must enumerate current exact identities, not old-plan values:

1. repository HEAD, remote `main`, and immutable baseline tag target;
2. every file under `runtime_capability_prototype/contracts/`, `fixture_specs/`, `native/`, `bin/`, and `runtime/`, excluding cache files and suite-generated evidence directories;
3. top-level Python imports and exact AST definition identities for every current control/runtime Python file;
4. the production/runtime callable-root set, test/control entrypoints, build-only entrypoints, legacy entrypoints, native build input, executable, schemas, policy, and fixed public-trust records;
5. static import edges, package initializer edges, constant file/config references, subprocess/executable edges, `ctypes`/native edges, and environment/platform-boundary requirements;
6. all seven formal role-gap identities and their current stage-scoped dispositions;
7. the R3G03, R3G04, and R3G07 PASS identities and the public trust freeze identity;
8. assurance ceiling `CTDE-PORTABLE-DEV-1`, Development, A1 only, non-certified, non-hardened;
9. an action ledger proving zero Runtime modification, Runtime execution, model calls, TEI content reads, Candidate work, and business outputs.

The audit may parse Python source and formal control files. It must not import project Runtime modules or execute project code. It must not read any Odyssey source body, `book_structure_map.yaml`, analysis candidate payload, English TEI content, or Greek TEI content.

### 4.3 Entrypoint classification

The audit must preserve these distinctions:

- there is no current production CLI/orchestrator;
- production/runtime roots are callable APIs, not `run_suite.py` or another test runner;
- `runtime/run_suite.py::main` is a legacy 197-leaf driver;
- `runtime/run_r2_portable.py::main` is an R2 test/control runner;
- `runtime/run_r3g07_public_trust.py::main` is the completed R3G07 test/control runner;
- R3G07 manifest/result builders and verifier are historical/current test-control evidence, not production Runtime roots;
- `runtime/build_manifest.py` is legacy, and `runtime/build_r2_portable_manifest.py` is R2 build-only;
- the future R3 closure builder, verifier, runner, and result generator do not yet exist and must be proposed only by the Plan.

### 4.4 Callable-root recovery

The audit must verify exact AST uniqueness for the following current production/runtime roots and may add a current root only when direct current source reachability proves it is required:

- `ctde_runtime.authorization_v2.load_authorization_v2`
- `ctde_runtime.authorization_v2.validate_request_binding`
- `ctde_runtime.authorization_v2.validate_activated_projection`
- `ctde_runtime.authorization_registry.AuthorizationRegistry.register_authorization_v2`
- `resolve_preconsume_v2`
- `consume_authorization_v2`
- `revoke_authorization_v2`
- `claim_mint_lease_v2`
- `prepare_capability_v2`
- `activate_capability_v2`
- `abort_mint_eligibility_v2`
- `abort_preparation_v2`
- `abort_activation_v2`
- `validate_context_v2`
- `ctde_runtime.range_broker.CapabilityIssuer.validate_preparation_binding_v2`
- `build_pending_capability_v2`
- `validate_activation_binding_v2`
- `ctde_runtime.range_broker.RangeBroker.handle_request`
- `validate_authorization_binding_v2`
- `deliver`
- `ctde_runtime.bounded_reader.BoundedReader.validate_authorization_binding_v2`
- `consume`
- `ctde_runtime.formal_loader.FormalLoader.load`
- `ctde_runtime.read_audit.ReadAuditAggregator.validate_authorization_correlation_v2`
- `create_scope_attestation`
- `create_closure_attestation`
- `ctde_runtime.events.SignedEventLog.append`
- `verify`
- `ctde_runtime.events.PortableA1EventLogV2.append`
- `verify`
- `ctde_runtime.sandbox.SandboxSupervisor.run`
- `ctde_runtime.public_trust.load_portable_public_trust`

Each callable record must freeze `callable_id`, `module`, `qualname`, `relative_path`, `containing_file_sha256`, and `definition_count=1`. Unqualified names in the list above inherit the most recent fully qualified class prefix. The audit must expand them to complete module-plus-qualname values.

## 5. Formal seven-role reconciliation

The current audit and Plan must retain all seven gap IDs. They must not pretend the historical inventory never existed.

| Gap | Current fresh-R3 disposition | Active R3 blocker | Future boundary |
| --- | --- | --- | --- |
| `R3G-01-PORTABLE-R4-SUITE-MANIFEST-BUILDER` | `stage_scoped_deferred_to_R4` | false | R4P must define/freeze it before R4 |
| `R3G-02-PORTABLE-R4-SUITE-RUNNER` | `stage_scoped_deferred_to_R4` | false | R4P must define/freeze it before R4 |
| `R3G-03-BOUNDED-PARSER-SCOPE` | `fulfilled_by_minimal_embedded_role_mapping` | false | independent strengthening remains deferred to R4 |
| `R3G-04-DISCARD-ONLY-MODEL-GATEWAY` | `fulfilled_by_minimal_embedded_role_mapping` | false | independent mediation and real Candidate gateway remain deferred |
| `R3G-05-PORTABLE-LOGICAL-WRITE-MONITOR` | `stage_scoped_deferred_to_R4` | false | Portable logical role waits for R4 publisher/output paths; OS-complete monitor is Hardened-only |
| `R3G-06-PORTABLE-R4-AGGREGATE-REPORT-GENERATOR` | `stage_scoped_deferred_to_R4` | false | R4P must define/freeze it before R4 |
| `R3G-07-IMMUTABLE-PUBLIC-TRUST-KEY-STATUS` | `fulfilled_by_r3g07_repair` | false | frozen public assets are R3 inputs; no new trust assets |

This is a stage/profile adjudication, not a reclassification: R3G01/02/05/06 retain primary `G.deferred_to_R4`; R3G03/04 retain the classifications frozen by their contracts/results; R3G07 retains the adjudicated repair identity. The Plan must record `formal_role_inventory_count=7`, `fulfilled_role_count=3`, `stage_scoped_deferred_role_count=4`, and `active_r3_role_gap_count=0` only if all cited result and trust identities remain exact.

## 6. R3G03, R3G04, and R3G07 bindings

The audit and Plan must bind:

```yaml
r3g03:
  result_path: "R3G03_MINIMAL_EMBEDDED_ROLE_MAPPING_RESULT.json"
  result_sha256: "78df12d69794d5fdc54d5e18c422744ec65ee6e898589ff8b833bb628e24e8b2"
  final_status: "PASS_R3G03_MINIMAL_EMBEDDED_ROLE_MAPPING"
r3g04:
  result_path: "R3G04_MINIMAL_EMBEDDED_ROLE_MAPPING_RESULT.json"
  result_sha256: "aee66549193c3608d689e004298fafa17cc5a26717f71d63f75335482d354090"
  final_status: "PASS_R3G04_MINIMAL_EMBEDDED_ROLE_MAPPING"
r3g07:
  final_status: "PASS_PORTABLE_RUNTIME_ROLE_GAP_R3G07_REPAIRED"
  public_trust_freeze_identity: "7a4a664a8fcccea98ee600d853fc9d36107e307ec2e7e078c9fad42363a831f3"
  kid: "ctde-portable-dev-20260813-01"
  public_key_bytes_sha256: "32a457033c8eefa8bea45ce347cb17ef08c928fabf7c2139ead1ab8af29aef5f"
  public_key_status: "active"
  trust_material_sha256: "dcac3ed439a24639736b01f035ef121ac025bd7c9e93882040c7ebcc7350e3cc"
  status_registry_sha256: "d0e13ff804bbd224146133b67853b4256756fbd4c995c8045edadfdbc576bc4d"
  loader_sha256: "72103c6de973a7f575c553681edcf097c46123d263c81b0edbdbed28f94dd5b8"
  signing_sha256: "5c41a1601b9824715d17ae416513646575006a9207dedd26bb2036336e66cc36"
```

The R3G07 test seed remains a `test_only_reproducibility_fixture`, never a production/private trust root. Fresh R3 must consume current public trust/status bytes without generating or reading any production private key.

## 7. Fresh R3 Plan artifact contract

### 7.1 Required identity

```yaml
artifact_path: "FRESH_R3_PORTABLE_TRANSITIVE_CLOSURE_PLAN.md"
artifact_class: "ctde_fresh_r3_portable_transitive_closure_plan"
plan_schema_version: "1.0.0"
encoding: "UTF-8"
terminal_lf_required: true
```

The Plan must bind its external persisted SHA-256 rather than claiming a self-hash. The Plan must bind the exact planning-contract digest, audit artifact digest, audit commit identity, current runtime/control tree identities, R3G03/R3G04/R3G07 results, assurance profile, and historical R3P digest.

### 7.2 Mandatory Plan content

The Plan is complete only if it uniquely defines all of the following without placeholders or multiple candidates:

1. one future R3 execution phase ID, phase kind, scope status, suite ID, suite root, result path, PASS status, and BLOCKED status;
2. exact create-only project write scope and its canonical SHA-256; mutable existing files must remain empty;
3. every implementation schema, policy, builder, verifier, runner, result generator, control artifact, evidence artifact, aggregate, and external-registry artifact path;
4. create ordering, ownership, create-once rules, resume rules, partial-state fail-closed rules, and cleanup rules;
5. current production/runtime callable roots and all static/transitive dependency-discovery algorithms;
6. current contracts/configs/public trust/status inputs and current test/build/legacy classifications;
7. interpreter, stdlib, distributions, shared libraries, native probe, compiler/build recipe, environment, process, and platform-boundary capture rules;
8. start snapshot, dynamic observation, end snapshot, delta rules, unknown/unresolved dependency rules, and external snapshot registry binding;
9. exact integration of R3G03 parser scope, R3G04 discard-only gateway, and R3G07 public trust;
10. stage-scoped dispositions for R3G01/02/05/06 and a rule that any later R4 bytes invalidate the R3 closure until a fresh refresh;
11. deterministic test requirement groups with future leaf count `N` discovered from the frozen requirement inventory, never predeclared to force PASS;
12. zero real-source reads, zero model calls, zero Candidate work, and no R4 implementation;
13. Portable / Development / A1, non-certified, non-hardened claim ceiling;
14. exact future human authorization payload fields and pre-write gate.

### 7.3 Static closure algorithm

The Plan must close at least these edge classes:

- Python `import` and `from ... import ...`, including relative imports and package initializers;
- callable body references reachable from the approved root set;
- module-level constants, path construction, schema/policy/config/data file opens, and exact project-owned bytes;
- dynamic import/plugin/module-loading sites, which must resolve to a finite allowlist or BLOCK;
- subprocess/executable paths, native source/build/binary edges, `ctypes`/shared-library edges, interpreter/stdlib/distribution edges, symlinks, and loader/ABI boundaries;
- environment variables and fixed child environment semantics;
- builder, verifier, runner, result-generator, schema, policy, manifest, evidence, aggregate, and external-registry control-plane nodes;
- all project-owned files observed dynamically, with unknown or unregistered nodes equal to zero.

Dynamic observation can supplement but never replace static closure. Non-executed branches require static evidence. The future R3 suite must use synthetic/no-content fixtures only; it may not open Odyssey source content or execute Candidate semantics.

## 8. Future R3 authorization boundary

The Plan must define exactly one future R3 execution gate. That gate is not approved by this contract or by the standing planning authority. Before any R3 project write, a new explicit human message must quote and approve at least:

```yaml
plan_path: "FRESH_R3_PORTABLE_TRANSITIVE_CLOSURE_PLAN.md"
plan_sha256: "<exact persisted Plan SHA-256>"
current_tree_audit_path: "FRESH_R3_CURRENT_TREE_AUDIT.json"
current_tree_audit_sha256: "<exact persisted audit SHA-256>"
phase_id: "<exact Plan-defined R3 execution phase ID>"
phase_kind: "<exact Plan-defined R3 execution phase kind>"
suite_id: "<exact Plan-defined suite ID>"
r3_result_artifact_path: "<exact Plan-defined result path>"
r3_write_scope_sha256: "<exact Plan-defined write-scope digest>"
approval_scope: "fresh R3 implementation materialization and deterministic Portable closure verification only"
```

If the Plan adds another exact digest-bound input, that field must also be quoted. Neither the agent nor a planning artifact may generate these values and then claim human approval. Until a later human message provides the exact payload, the Plan's terminal machine gate must have `execution_authorized=false`, `r3_execution_authorized=false`, and `human_authorization_required=true`.

## 9. Planning verification groups

Planning must execute deterministic static checks under the following closed group inventory. Leaf count is discovered from actual expansion and is not frozen here.

| Group | Requirement |
| --- | --- |
| `R3FP-VG01` | Git, remote-main, baseline-tag, and clean-tree identity |
| `R3FP-VG02` | normative source paths and exact digests |
| `R3FP-VG03` | current Runtime/control/config/native/public-trust file inventory and digests |
| `R3FP-VG04` | entrypoint presence, AST uniqueness, and classification |
| `R3FP-VG05` | production callable-root presence, AST uniqueness, module/path/digest binding |
| `R3FP-VG06` | Python import and package-initializer edges |
| `R3FP-VG07` | config/data/open/path and executable/native dependency edges |
| `R3FP-VG08` | dynamic import, subprocess, environment, platform, and unknown-edge policy |
| `R3FP-VG09` | R3G03 result and parser-scope identity |
| `R3FP-VG10` | R3G04 result and discard-only gateway identity |
| `R3FP-VG11` | R3G07 result, public trust/status/loader/signing identity, and F16 boundary |
| `R3FP-VG12` | seven-role inventory reconciliation and active-R3-gap count |
| `R3FP-VG13` | exact future R3 file/directory/write-scope inventory |
| `R3FP-VG14` | implementation ownership, ordering, create-once, resume, and partial-state rules |
| `R3FP-VG15` | static/dynamic closure, native build, platform, start/end, delta, and registry algorithms |
| `R3FP-VG16` | future deterministic requirements, actual-N counting, PASS/BLOCKED predicates |
| `R3FP-VG17` | no Runtime mutation/execution, no source-content reads, no model/Candidate/R4 work |
| `R3FP-VG18` | claim ceiling, artifact canonicalization, deterministic rerender, and human gate |

Planning PASS requires all groups present, every expanded leaf executed with complete evidence, and `failed=skipped=unknown=timeout=0`. A static locator must identify the exact semantic node; a first generic match, source-string assertion without parser identity, self-described PASS, expected-equals-actual substitution, or skipped evidence is failure.

## 10. PASS, BLOCKED, and commit semantics

The planning phase PASS status is:

```text
PASS_FRESH_R3_FILE_LEVEL_REPLAN
```

The failure status is:

```text
BLOCKED_FRESH_R3_FILE_LEVEL_REPLAN_FAILED
```

PASS means only that the current tree was audited and a complete future R3 execution contract was planned. It does not mean R3 implementation exists, R3 executed, R3 passed, R4 is ready, Candidate is ready, or any source analysis occurred.

The planning contract, audit, and Plan are separate atomic formal artifacts. Each must be committed and normally pushed to `main` in its own commit after confirming that the changeset contains only that artifact. No amend, force push, history rewrite, or baseline-tag mutation is allowed.

## 11. Contract-definition acceptance

```yaml
contract_definition_acceptance:
  predecessor_gate_recovered: true
  normative_sources_closed: true
  planning_phase_identity_closed: true
  planning_write_scope_closed: true
  audit_artifact_contract_closed: true
  current_tree_scope_closed: true
  callable_root_recovery_closed: true
  seven_role_reconciliation_closed: true
  r3g03_binding_closed: true
  r3g04_binding_closed: true
  r3g07_binding_closed: true
  plan_artifact_contract_closed: true
  future_r3_scope_requirements_closed: true
  human_authorization_boundary_closed: true
  planning_verification_contract_closed: true
  unresolved_planning_contract_ambiguity: 0
  runtime_modification_required: 0
  runtime_execution_count: 0
  model_call_count: 0
  english_tei_content_read_count: 0
  greek_tei_content_read_count: 0
  r4_scope_expansion: 0
```

## 12. Next-step machine gate

```yaml
current_status: "PASS_FRESH_R3_FILE_LEVEL_REPLAN_CONTRACT_DEFINED"
next_phase_id: "Phase 2-G-R3FRESH-P1"
next_phase_kind: "fresh_r3_file_level_replan_and_deterministic_closure_planning_only"
scope_status: "planning_contract_defined_under_standing_human_planning_authority"
planning_execution_authorized: true
r3_execution_authorized: false
current_tree_audit_artifact_path: "FRESH_R3_CURRENT_TREE_AUDIT.json"
fresh_r3_plan_artifact_path: "FRESH_R3_PORTABLE_TRANSITIVE_CLOSURE_PLAN.md"
planning_write_scope_sha256: "befb8af99a450c298152330d950cea2521b00a1ce209fa42583acc42155fe8f9"
```

The executor may now create the audit and Plan within the exact write scope. It must stop before future R3 execution unless a later human message supplies the Plan-bound authorization required by section 8.
