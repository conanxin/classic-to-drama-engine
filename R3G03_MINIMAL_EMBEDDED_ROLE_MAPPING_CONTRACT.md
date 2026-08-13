# Classic-to-Drama Engine: R3G-03 Minimal Embedded-Role Mapping Machine Contract

> Contract-definition result: `PASS_R3G03_MINIMAL_EMBEDDED_ROLE_MAPPING_CONTRACT_DEFINED`  
> Contract path: `R3G03_MINIMAL_EMBEDDED_ROLE_MAPPING_CONTRACT.md`  
> Contract effect: definition only; mapping execution is not authorized  
> Assurance boundary: Portable / Development; A1 only; non-certified

## 0. Contract conclusion and current boundary

This contract closes the missing machine contract for the logical next action `R3G-03 minimal embedded-role mapping`. It does not execute that mapping, does not run Runtime code or tests, and does not authorize R3G-04, fresh R3 replanning, R3, R4, Candidate, model, TEI, Source Layer content, or literary work.

```yaml
contract_definition_status: "PASS_R3G03_MINIMAL_EMBEDDED_ROLE_MAPPING_CONTRACT_DEFINED"

gap_id: "R3G-03-BOUNDED-PARSER-SCOPE"
runtime_role: "parser scope"

future_mapping_phase:
  phase_id: "Phase 2-G-R3G03-M1"
  phase_kind: "r3g03_minimal_embedded_role_mapping_and_deterministic_verification_only"
  scope_status_before_execution: "mapping_contract_defined_waiting_for_explicit_mapping_authorization"
  mapping_authorized: false
  execution_authorized: false
  mapping_ready_for_authorization_review: true

mapping_result_artifact_path: "R3G03_MINIMAL_EMBEDDED_ROLE_MAPPING_RESULT.json"
mapping_write_scope_sha256: "f570cbd2274c09f801467859e6ac7a86db31618be706d20c345d78141b7e5a0f"

r3_execution_authorized: false
r4_execution_authorized: false
candidate_execution_authorized: false
```

`Phase 2-G-R3G03-M1` and `r3g03_minimal_embedded_role_mapping_and_deterministic_verification_only` are the only valid machine identity for the future mapping. The human-readable title `R3G-03 Minimal Embedded-Role Mapping` is not a substitute for either value. No completed R3G1, R3G2, or R3G3 identity may be reused.

## 1. Normative sources and frozen identities

The following exact files are the only normative source documents for this contract. Their SHA-256 values were recomputed from current disk bytes before this contract was created.

| Path | SHA-256 | Normative role |
| --- | --- | --- |
| `PORTABLE_RUNTIME_ROLE_GAP_R3G07_REPAIR_RESULT.md` | `f5c93ed0dccea6c985dc16654742eea7ea42474e750d32a946b765468835654e` | R3G-07 PASS, trust identities, caller bindings, and current authorization state |
| `PORTABLE_RUNTIME_PUBLIC_TRUST_BINDING_PLAN.md` | `fbd689f287be47aa5aa9cc3ebb256c9b7512101be073d92b1d27ae65ce0c577a` | required post-R3G07 logical order and public-trust boundary |
| `PORTABLE_RUNTIME_ROLE_GAP_RESOLUTION_PLAN.md` | `72f116ff0b93403961a045228706f9322deea008f41718acae6178b0780b8798` | R3G-03 identity, classification, paths, dependencies, and re-entry rule |
| `PORTABLE_RUNTIME_TRANSITIVE_CLOSURE_PLAN.md` | `f8ca07eaee1fff534e97bf4a0d037ba73a3c1838107e132f7c072b1fe05b39f5` | callable/member/edge identity and canonicalization requirements |
| `RUNTIME_ASSURANCE_PROFILE_DECISION.md` | `57471c85c57946f6ceb6da288301cc802533b09c137bfbe8e6e247dad57206e2` | Portable / Development A1 claim boundary |

The current upstream state remains:

```yaml
r3g07_status: "PASS_PORTABLE_RUNTIME_ROLE_GAP_R3G07_REPAIRED"
r3g07_result_sha256: "f5c93ed0dccea6c985dc16654742eea7ea42474e750d32a946b765468835654e"
r3_execution_authorized: false
r4_execution_status: "not_executed"
candidate_status: "blocked"
```

Any future mismatch in one of the five source-document digests blocks the mapping before any project-tree write with `BLOCKED_R3_ROLE_GAP_UNRESOLVED`. It may not be repaired, normalized, or replaced within the mapping phase.

## 2. Frozen R3G-03 gap identity

The future mapping must preserve this exact classification without reinterpretation:

```yaml
gap_id: "R3G-03-BOUNDED-PARSER-SCOPE"
gap_short_id: "R3G-03"
runtime_role: "parser scope"
primary_classification: "G.deferred_to_R4"
secondary_classifications:
  - "C.missing_contract_or_schema_binding"
embedded_runtime_logic_evidence_present: true
blocks_r3_under_current_r3p: true
requires_pre_r3_repair_after_adjudication: false
stale_gap_candidate: true
scope_status: "current_role_paths_resolved; future_strengthening_deferred_to_R4P"
repair_phase: null
future_strengthening: "deferred_to_R4"
```

The only future question authorized by this contract is:

> Do the frozen existing embedded-chain bytes and identities suffice to carry the Portable / Development A1 minimal parser-scope runtime role identity?

The mapping must not ask whether a new independent `parser.py` should be created. No independent parser component, XML parser strengthening, mediation component, Runtime implementation, or R4 strengthening may be designed or created in `Phase 2-G-R3G03-M1`.

## 3. Five-path Runtime identity contract

All five paths are required. Their current exact SHA-256 values were recomputed before contract creation and match the formally recorded values.

| Member ID | Exact relative path | Exact SHA-256 | Frozen role |
| --- | --- | --- | --- |
| `R3G03-M01-NATIVE-SOURCE` | `runtime_capability_prototype/native/consumer_probe.c` | `f4057def41b265723538eb28aa7a9e3172536d44de5a54d276fedf3df1aad3fb` | source identity containing Book/Card/Paragraph/DTD/entity/external-reference/namespace/non-recovery decisions |
| `R3G03-M02-PROBE-EXECUTABLE` | `runtime_capability_prototype/bin/consumer_probe` | `f1f4849e078169d14ae18c91a5469b171534479dd8255de359f588ca1b475c80` | executable identity launched by the supervisor; no reproducible-build claim is made here |
| `R3G03-M03-SUPERVISOR` | `runtime_capability_prototype/runtime/ctde_runtime/sandbox.py` | `c60aca6b25e933a12e37862c55df8ae8472dca55f03b0ceb871cbcd8eaf8a9d1` | launches the probe and returns its parser fields |
| `R3G03-M04-BOUNDED-READER` | `runtime_capability_prototype/runtime/ctde_runtime/bounded_reader.py` | `65c8f0a3af625c505fcdc05f7a754075e4829d2183931d71fa8c4dfdbf46f68c` | validates authorization binding, consumes the bounded delivery, emits `parser_scope_result`, and rejects non-PASS parser status |
| `R3G03-M05-READ-AUDIT` | `runtime_capability_prototype/runtime/ctde_runtime/read_audit.py` | `b5c8a9210c4f9f295351b32e3f2a5e310ad0531720ff886a9d84385ec1ab6b4d` | verifies signed logs, authorization correlation, parser scope, and scope/closure attestation callables |

The future G00 preflight must hash raw bytes directly. A mismatch in any one path produces `BLOCKED_R3_ROLE_GAP_UNRESOLVED` before any project write. The executor must not freeze an expected value over a different observed value.

## 4. Six-callable identity contract

Every callable identity is the closed tuple `(module, qualname, relative_path, containing_file_sha256)`. All four fields are required; matching only a symbol name, source line, import alias, or object display name is insufficient.

| Callable ID | Module | Qualname | Relative path | Containing file SHA-256 |
| --- | --- | --- | --- | --- |
| `R3G03-C01` | `ctde_runtime.sandbox` | `SandboxSupervisor.run` | `runtime_capability_prototype/runtime/ctde_runtime/sandbox.py` | `c60aca6b25e933a12e37862c55df8ae8472dca55f03b0ceb871cbcd8eaf8a9d1` |
| `R3G03-C02` | `ctde_runtime.bounded_reader` | `BoundedReader.validate_authorization_binding_v2` | `runtime_capability_prototype/runtime/ctde_runtime/bounded_reader.py` | `65c8f0a3af625c505fcdc05f7a754075e4829d2183931d71fa8c4dfdbf46f68c` |
| `R3G03-C03` | `ctde_runtime.bounded_reader` | `BoundedReader.consume` | `runtime_capability_prototype/runtime/ctde_runtime/bounded_reader.py` | `65c8f0a3af625c505fcdc05f7a754075e4829d2183931d71fa8c4dfdbf46f68c` |
| `R3G03-C04` | `ctde_runtime.read_audit` | `ReadAuditAggregator.validate_authorization_correlation_v2` | `runtime_capability_prototype/runtime/ctde_runtime/read_audit.py` | `b5c8a9210c4f9f295351b32e3f2a5e310ad0531720ff886a9d84385ec1ab6b4d` |
| `R3G03-C05` | `ctde_runtime.read_audit` | `ReadAuditAggregator.create_scope_attestation` | `runtime_capability_prototype/runtime/ctde_runtime/read_audit.py` | `b5c8a9210c4f9f295351b32e3f2a5e310ad0531720ff886a9d84385ec1ab6b4d` |
| `R3G03-C06` | `ctde_runtime.read_audit` | `ReadAuditAggregator.create_closure_attestation` | `runtime_capability_prototype/runtime/ctde_runtime/read_audit.py` | `b5c8a9210c4f9f295351b32e3f2a5e310ad0531720ff886a9d84385ec1ab6b4d` |

Future verification must use static syntax/symbol inspection without importing these modules or invoking any callable. Each callable must exist exactly once at its expected class qualname. Missing, duplicate, dynamically substituted, or unparsable identities fail closed.

## 5. Embedded chain and dependency-edge contract

### 5.1 Edge direction and closed representation

For this mapping, edge direction is **parser-role evidence flow from producer to downstream consumer**. Each edge item has exactly these required fields:

```yaml
edge_id: "<stable R3G03-E##>"
from_id: "<exact member ID>"
to_id: "<exact member ID>"
relation: "<closed relation value>"
locator: "<exact static locator>"
result: "PASS | BLOCKED"
```

Allowed `relation` values are closed to:

```yaml
allowed_relations:
  - "source_identity_for"
  - "probe_output_consumed_by"
  - "sandbox_result_consumed_by"
  - "parser_scope_event_consumed_by"
```

The required direct edges are:

| Edge ID | From | To | Relation | Locator |
| --- | --- | --- | --- | --- |
| `R3G03-E00` | `R3G03-M01-NATIVE-SOURCE` | `R3G03-M02-PROBE-EXECUTABLE` | `source_identity_for` | `runtime_capability_prototype/native/consumer_probe.c=>runtime_capability_prototype/bin/consumer_probe` |
| `R3G03-E01` | `R3G03-M02-PROBE-EXECUTABLE` | `R3G03-M03-SUPERVISOR` | `probe_output_consumed_by` | `ctde_runtime.sandbox.SandboxSupervisor.run:subprocess.stdout=>probe` |
| `R3G03-E02` | `R3G03-M03-SUPERVISOR` | `R3G03-M04-BOUNDED-READER` | `sandbox_result_consumed_by` | `ctde_runtime.bounded_reader.BoundedReader.consume:self.sandbox.run=>sandbox_result` |
| `R3G03-E03` | `R3G03-M04-BOUNDED-READER` | `R3G03-M05-READ-AUDIT` | `parser_scope_event_consumed_by` | `ctde_runtime.read_audit.ReadAuditAggregator.create_scope_attestation:parser_scope_result` |

`R3G03-E00` binds the two current identities only; it does not claim that the binary is reproducibly built from the source. That stronger native-build proof remains outside this mapping.

### 5.2 Direct-dependency IDs and canonicalization

The result must record these exact direct downstream dependency IDs:

```yaml
R3G03-M01-NATIVE-SOURCE:
  - "R3G03-M02-PROBE-EXECUTABLE"
R3G03-M02-PROBE-EXECUTABLE:
  - "R3G03-M03-SUPERVISOR"
R3G03-M03-SUPERVISOR:
  - "R3G03-M04-BOUNDED-READER"
R3G03-M04-BOUNDED-READER:
  - "R3G03-M05-READ-AUDIT"
R3G03-M05-READ-AUDIT: []
```

Only the four direct edges may be persisted. Transitive rows such as executable-to-audit are prohibited; reachability may be recomputed in memory but must not be duplicated as an edge. Duplicate `(from_id,to_id,relation,locator)` tuples, alternate locators, extra members, cycles, or unresolved endpoints fail closed.

Members are ordered by `member_id`. Callable identities are ordered by `callable_id`. Edges are ordered lexicographically by `(from_id,to_id,relation,locator)`. Arrays may not use filesystem discovery order.

## 6. Parser-scope identity contract

The future result field `parser_scope_identity` is a closed object with exactly seven required child fields. No literary, story, character, event, theme, Odyssey, TEI, or business field is allowed.

| Machine field | Required canonical representation | PASS semantics | Fail-closed semantics |
| --- | --- | --- | --- |
| `book_scope` | `required=true`, `allowed_book_marker="BOOK_01"`, `allowed_book_marker_count=1`, `disallowed_book_marker_count=0`, `result` | Existing bytes represent exactly one allowed Book 1 marker and reject Book 2/other-book markers | Missing representation, nonzero disallowed markers in the rule, or absence of rejection logic is BLOCKED |
| `card_scope` | `required=true`, `expected_card_marker_count=10`, `result` | Existing bytes require exactly 10 card markers | Any non-exact or recovery-permitting rule is BLOCKED |
| `paragraph_scope` | `required=true`, `expected_paragraph_marker_count=10`, `result` | Existing bytes require exactly 10 paragraph markers | Any non-exact or recovery-permitting rule is BLOCKED |
| `markup_safety_scope` | `required=true`, `dtd_marker_count=0`, `entity_marker_count=0`, `external_reference_marker_count=0`, `result` | DTD, entity, and external-reference presence maps to a non-PASS parser status | Missing one category or allowing recovery is BLOCKED |
| `namespace_scope` | `required=true`, `expected_namespace="urn:ctde:synthetic"`, `expected_namespace_occurrences=1`, `namespace_ok=true`, `result` | The namespace rule is exact and deterministic | Missing, alternate, multiple, or nondeterministic namespace acceptance is BLOCKED |
| `non_recovery_scope` | `required=true`, `recovery_allowed=false`, `non_pass_parser_status_raises=true`, `result` | Incomplete/malformed or other non-PASS state cannot continue past `BoundedReader.consume` | Fallback, recovery, silent coercion, or continued processing after non-PASS is BLOCKED |
| `correlated_parser_scope_result` | `required=true`, `event_kind="parser_scope_result"`, `authorization_correlation_required=true`, `signed_event_required=true`, `result` | The bounded reader emits the parser fields and the audit path consumes signed, authorization-correlated parser-domain evidence | Missing event, unsigned consumption, or missing authorization correlation is BLOCKED |

Every child object has only the fields shown in its row; `result` is required and is exactly `PASS` or `BLOCKED`. Booleans and integers are JSON primitives, not strings. A final mapping PASS requires all seven child results to be `PASS`.

This contract maps static identity and fail-closed control evidence. It does not execute a real or synthetic parser E2E and does not claim complete OS-level access isolation.

## 7. Signed-role and public-trust input contract

R3G-07 outputs are immutable mapping inputs. R3G-03 must not generate, rotate, replace, or reinterpret any trust asset and must not read or create a private key.

```yaml
signed_role_binding:
  assurance_profile_id: "CTDE-PORTABLE-DEV-1"
  trust_domain: "ctde-portable-runtime"
  public_trust_freeze_identity: "7a4a664a8fcccea98ee600d853fc9d36107e307ec2e7e078c9fad42363a831f3"
  kid: "ctde-portable-dev-20260813-01"
  public_key_bytes_sha256: "32a457033c8eefa8bea45ce347cb17ef08c928fabf7c2139ead1ab8af29aef5f"
  status: "active"
  trust_material_sha256: "dcac3ed439a24639736b01f035ef121ac025bd7c9e93882040c7ebcc7350e3cc"
  status_registry_sha256: "d0e13ff804bbd224146133b67853b4256756fbd4c995c8045edadfdbc576bc4d"
  loader_sha256: "72103c6de973a7f575c553681edcf097c46123d263c81b0edbdbed28f94dd5b8"
  signing_sha256: "5c41a1601b9824715d17ae416513646575006a9207dedd26bb2036336e66cc36"
  binding_strength: "portable_a1_approved_composition"
  trust_assets_generated_by_mapping: false
  private_key_dependency: false
  result: "PASS | BLOCKED"
```

The result must recompute the two trust-asset file digests, loader digest, and signing digest; recover the kid, raw public-key digest, active status, Profile, and domain from exact current bytes; and cross-check the R3G-07 result's caller bindings for `BoundedReader.consume` and `ReadAuditAggregator._verify_logs` against the same `public_trust_freeze_identity`. Any mismatch is BLOCKED.

## 8. Future mapping artifact contract

### 8.1 Sole canonical path and schema identity

The sole persistent artifact permitted during future mapping execution is:

```yaml
mapping_result_artifact_path: "R3G03_MINIMAL_EMBEDDED_ROLE_MAPPING_RESULT.json"
artifact_class: "ctde_r3g03_minimal_embedded_role_mapping_result"
schema_id: "urn:ctde:contract:r3g03-minimal-embedded-role-mapping-result:1"
schema_version: "1.0.0"
canonicalization_id: "CTDE-R3G03-MAPPING-JCS-1"
```

No independent manifest, runner, verifier, evidence, ledger, schema file, directory, Markdown result, cache, or bytecode artifact is permitted in the project tree. Verification evidence is embedded as closed `verification_records` in this one result.

### 8.2 Closed top-level fields

The result JSON has exactly these required top-level fields and no others:

```yaml
closed_top_level_fields:
  - "artifact_class"
  - "schema_id"
  - "schema_version"
  - "canonicalization_id"
  - "contract_identity"
  - "phase_identity"
  - "gap_identity"
  - "assurance_identity"
  - "authorization_identity"
  - "write_scope_identity"
  - "source_document_identities"
  - "runtime_path_identities"
  - "callable_identities"
  - "dependency_edges"
  - "parser_scope_identity"
  - "signed_role_binding"
  - "verification_summary"
  - "verification_records"
  - "action_ledger"
  - "final_status"
  - "logical_successor"
  - "post_mapping_authorization"
```

The fixed scalar values for the first four fields are those in §8.1.

The closed child objects are:

```yaml
contract_identity:
  fields: ["path", "sha256"]

phase_identity:
  fields: ["phase_id", "phase_kind", "scope_status_at_start"]

gap_identity:
  fields:
    - "gap_id"
    - "runtime_role"
    - "primary_classification"
    - "secondary_classifications"
    - "embedded_runtime_logic_evidence_present"
    - "stale_gap_candidate"
    - "requires_pre_r3_repair_after_adjudication"
    - "future_strengthening"

assurance_identity:
  fields: ["assurance_profile_id", "highest_claimed_evidence_level", "hardened", "certified"]

authorization_identity:
  fields:
    - "explicit_human_mapping_authorization_received"
    - "approved_contract_path"
    - "approved_contract_sha256"
    - "approved_phase_id"
    - "approved_phase_kind"
    - "approved_mapping_result_artifact_path"
    - "approved_mapping_write_scope_sha256"

write_scope_identity:
  fields: ["mutable_existing_files", "creatable_files", "creatable_directories", "mapping_write_scope_sha256"]

verification_summary:
  fields:
    - "required_group_count"
    - "required_groups_covered"
    - "discovered"
    - "executed"
    - "evidence_complete"
    - "passed"
    - "failed"
    - "skipped"
    - "unknown"
    - "timeout"

action_ledger:
  fields:
    - "existing_file_modification_count"
    - "runtime_modification_count"
    - "runtime_test_count"
    - "r3g03_mapping_attempt_count"
    - "r3g04_mapping_execution_count"
    - "fresh_r3_replan_count"
    - "r3_execution_count"
    - "r4_execution_count"
    - "candidate_run_count"
    - "model_call_count"
    - "english_tei_content_read_count"
    - "greek_tei_content_read_count"
    - "business_output_count"

logical_successor:
  fields: ["gap_id", "action", "successor_machine_contract_defined", "successor_execution_authorized"]

post_mapping_authorization:
  fields: ["mapping_authorized", "execution_authorized", "r3_execution_authorized", "r4_execution_authorized", "candidate_execution_authorized", "fresh_r3_replan_required"]
```

Array item contracts are also closed:

```yaml
source_document_identities_item_fields: ["path", "sha256", "result"]
runtime_path_identities_item_fields: ["member_id", "path", "sha256", "role", "direct_dependency_ids", "result"]
callable_identities_item_fields: ["callable_id", "module", "qualname", "relative_path", "containing_file_sha256", "result"]
dependency_edges_item_fields: ["edge_id", "from_id", "to_id", "relation", "locator", "result"]
verification_records_item_fields: ["leaf_id", "requirement_group_id", "verification_method", "subject_identity", "expected_value", "observed_value", "result"]
```

Array cardinality and ordering are closed as follows:

```yaml
source_document_identities:
  exact_count: 5
  exact_members: "the five paths and digests in §1"
  order: "path"
runtime_path_identities:
  exact_count: 5
  exact_members: "R3G03-M01 through R3G03-M05 in §3"
  order: "member_id"
callable_identities:
  exact_count: 6
  exact_members: "R3G03-C01 through R3G03-C06 in §4"
  order: "callable_id"
dependency_edges:
  exact_count: 4
  exact_members: "R3G03-E00 through R3G03-E03 in §5"
  order: ["from_id", "to_id", "relation", "locator"]
verification_records:
  exact_count: "N discovered from actual leaf expansion; not preset"
  order: ["requirement_group_id", "subject_identity", "verification_method"]
```

`gap_identity.secondary_classifications` has exactly one member, `C.missing_contract_or_schema_binding`. `parser_scope_identity` has exactly the seven children and child fields in §6. `signed_role_binding` has exactly the fields shown in §7. All object fields and array item fields are required. Unknown fields, duplicate keys, duplicate stable IDs, an unknown enum, a missing required item, an extra item, or a non-closed nested object are BLOCKED.

For a completed future mapping attempt, `action_ledger` is exactly:

```yaml
existing_file_modification_count: 0
runtime_modification_count: 0
runtime_test_count: 0
r3g03_mapping_attempt_count: 1
r3g04_mapping_execution_count: 0
fresh_r3_replan_count: 0
r3_execution_count: 0
r4_execution_count: 0
candidate_run_count: 0
model_call_count: 0
english_tei_content_read_count: 0
greek_tei_content_read_count: 0
business_output_count: 0
```

### 8.3 Canonical serialization and digest rule

The result uses:

1. UTF-8 without BOM;
2. compact JSON with no insignificant whitespace;
3. object keys ordered by Unicode code point;
4. arrays ordered by the stable IDs or explicit order in this contract;
5. no float, NaN, Infinity, duplicate key, unknown field, absolute path, `..`, symlink alias, or platform-dependent path separator;
6. exactly one terminal LF and no bytes after it.

This result contains no self-digest field. Its exact full-file SHA-256, including the one terminal LF, is computed after create-once persistence and reported only in external delivery metadata and any later authorization that consumes the result. Re-serializing a parsed object is not a substitute for verifying the exact persisted bytes.

Two fresh-process render passes from the same frozen observations must produce byte-identical candidate JSON in approved OS temporary storage before the single project-tree create. Wall-clock time, mtime, random ID, UUID, host path, PID, unordered map order, or environment-derived value is forbidden from result bytes.

## 9. Mapping write scope

The exact canonical write-scope bytes, including one terminal LF, are:

```json
{"creatable_directories":[],"creatable_files":["R3G03_MINIMAL_EMBEDDED_ROLE_MAPPING_RESULT.json"],"mutable_existing_files":[]}
```

Their SHA-256 is:

```yaml
mapping_write_scope_sha256: "f570cbd2274c09f801467859e6ac7a86db31618be706d20c345d78141b7e5a0f"
```

The only valid project-tree scope is:

```yaml
mutable_existing_files: []
creatable_files:
  - "R3G03_MINIMAL_EMBEDDED_ROLE_MAPPING_RESULT.json"
creatable_directories: []

existing_file_modification_required: false
runtime_modification_required: false
runtime_modification_count_allowed: 0
```

OS temporary storage may be used only for two nonpersistent render candidates and in-memory observation data. It is not project authority; it may not be used to stage Runtime replacements, TEI/source copies, a hidden manifest, a hidden evidence file, or a reusable runner. Bytecode and cache creation must be disabled.

If the result path already exists, any other project path appears in the proposed write set, or an existing file would need modification, G00 fails before any write with `BLOCKED_R3_ROLE_GAP_UNRESOLVED`.

## 10. Closed read-only authority

The future mapping uses an allowlist, not a traversal root. It may read only the following exact project files.

### 10.1 Contract and normative documents

```text
R3G03_MINIMAL_EMBEDDED_ROLE_MAPPING_CONTRACT.md
PORTABLE_RUNTIME_ROLE_GAP_R3G07_REPAIR_RESULT.md
PORTABLE_RUNTIME_PUBLIC_TRUST_BINDING_PLAN.md
PORTABLE_RUNTIME_ROLE_GAP_RESOLUTION_PLAN.md
PORTABLE_RUNTIME_TRANSITIVE_CLOSURE_PLAN.md
RUNTIME_ASSURANCE_PROFILE_DECISION.md
```

The contract file is read using the exact SHA-256 supplied by the future human authorization; this contract does not embed its own digest.

### 10.2 Five embedded-chain files

```text
runtime_capability_prototype/native/consumer_probe.c
runtime_capability_prototype/bin/consumer_probe
runtime_capability_prototype/runtime/ctde_runtime/sandbox.py
runtime_capability_prototype/runtime/ctde_runtime/bounded_reader.py
runtime_capability_prototype/runtime/ctde_runtime/read_audit.py
```

### 10.3 Direct support and signed-role files

| Exact path | Frozen current SHA-256 | Read-only purpose |
| --- | --- | --- |
| `runtime_capability_prototype/contracts/public_trust_material_schema_v1.yaml` | `95ec649fbc158df2859c37628927211f9fd46443f3274ef881465bb1ef6b60b8` | material closed-schema identity |
| `runtime_capability_prototype/contracts/public_key_status_registry_schema_v1.yaml` | `33a71d1d69bf1586039f0be066b87e83b2c5aaad605fef813208fd4ba9eb28e3` | status closed-schema identity |
| `runtime_capability_prototype/contracts/portable_public_trust_material_v1.json` | `dcac3ed439a24639736b01f035ef121ac025bd7c9e93882040c7ebcc7350e3cc` | formal public verification material |
| `runtime_capability_prototype/contracts/portable_public_key_status_registry_v1.json` | `d0e13ff804bbd224146133b67853b4256756fbd4c995c8045edadfdbc576bc4d` | formal key status and validity |
| `runtime_capability_prototype/runtime/ctde_runtime/public_trust.py` | `72103c6de973a7f575c553681edcf097c46123d263c81b0edbdbed28f94dd5b8` | loader/freeze identity |
| `runtime_capability_prototype/runtime/ctde_runtime/signing.py` | `5c41a1601b9824715d17ae416513646575006a9207dedd26bb2036336e66cc36` | signed-object implementation identity; no private material |
| `runtime_capability_prototype/runtime/ctde_runtime/authorization_registry.py` | `e6ee8923c1c05c1ebdf04106fed659d40b8d394f6cbca4688d437dd58ee446af` | bounded-reader authorization validation dependency |
| `runtime_capability_prototype/runtime/ctde_runtime/authorization_v2.py` | `5359cf7289e130f8a3c4228dd6d4c8b0e961ef9da716c05a78169191d571ba4d` | activated projection and correlation dependency |
| `runtime_capability_prototype/runtime/ctde_runtime/events.py` | `808115293ec818eedd926e4ef63869a7d5f9eeb1dca26a6902c12850b4e7fd15` | signed parser-domain event verification |
| `runtime_capability_prototype/runtime/ctde_runtime/common.py` | `20a1d4c184753f007e4da2b11cabc3f96b1049d75aa69673ddfbe0d26344aa56` | fail-closed helpers and digest semantics |
| `runtime_capability_prototype/runtime/ctde_runtime/range_broker.py` | `ef2be994b82f10f025411e1d074cda3d0336e352f063bb9162edbcaed105958a` | bounded delivery/envelope dependency identity |
| `runtime_capability_prototype/runtime/ctde_runtime/fixture_factory.py` | `c40aef7040c808b68a7f315ec7051cdbbe7424dbc2a62e4bce6278e08743519b` | static Book 1 range constants consumed by read audit |

Any other project read is outside authority. In particular, the mapping must not read English TEI content, Greek TEI content, structure/source maps, Source Layer bodies, raw source objects, Candidate inputs or outputs, literary artifacts, model inputs, business outputs, R3G-07 test private material, or unrelated suite/evidence trees. Directory recursion, content search outside the allowlist, symlink escape, network fetch, and environment-supplied input paths are prohibited.

## 11. Deterministic verification contract

### 11.1 Mechanism

No persistent manifest or runner is required or permitted. The mapping uses the closed requirement-group inventory below and a single read-only static verification controller operated from approved OS temporary storage. It must:

1. perform G00 before any project write;
2. read raw bytes only from §10;
3. compute exact SHA-256 directly;
4. parse Python with a non-importing static syntax/symbol inventory;
5. inspect the C source and Python control-flow markers statically without executing the binary or Runtime callables;
6. build verification leaf records in memory from the actual subjects required by each group;
7. enumerate and sort those leaves by `(requirement_group_id,subject_identity,verification_method)`;
8. execute every enumerated static check exactly once;
9. render the sole result twice in fresh processes/temp locations and require exact-byte equality;
10. create the result once only after scope, count, evidence, and canonical-byte checks pass.

The number of verification leaves is not specified by this contract. It is the actual length `N` of `verification_records` produced by expanding the required subjects at execution time. The 15 requirement groups are coverage obligations, not a test-count proxy.

### 11.2 Required groups

| Group ID | Required verification obligation |
| --- | --- |
| `R3G03-VG01` | Recompute and match the five exact path digests |
| `R3G03-VG02` | Resolve and match all six callable tuples |
| `R3G03-VG03` | Verify the four direct embedded-chain edges and exact order/reachability |
| `R3G03-VG04` | Verify `BoundedReader.validate_authorization_binding_v2` exists and statically invokes registry/context projection validation |
| `R3G03-VG05` | Verify `BoundedReader.consume` validates authorization-bound signed envelope/attestation and consumes only the sealed bounded slice before parser flow |
| `R3G03-VG06` | Verify audit authorization correlation is bound to the activated authorization identity and signed domain logs |
| `R3G03-VG07` | Verify `ReadAuditAggregator.create_scope_attestation` exists and consumes correlated parser-scope evidence |
| `R3G03-VG08` | Verify `ReadAuditAggregator.create_closure_attestation` exists and binds the scope-attestation digest into closure evidence |
| `R3G03-VG09` | Verify Book/Card/Paragraph identities are representable in probe output, `parser_scope_result`, and audit checks |
| `R3G03-VG10` | Verify DTD/entity/external-reference presence produces fail-closed non-PASS status and cannot continue through bounded reader |
| `R3G03-VG11` | Verify namespace identity and exact acceptance rule are deterministic |
| `R3G03-VG12` | Verify recovery outside the authorized parser scope is prohibited and non-PASS status raises |
| `R3G03-VG13` | Recompute and match R3G-07 public-trust/signed-role inputs and the two relevant caller bindings |
| `R3G03-VG14` | Recompute pre/post hashes and prove no existing or Runtime file was modified and no path outside §9 was written |
| `R3G03-VG15` | Prove the mapping controller executed no Runtime callable/test and made zero model calls |

### 11.3 Counts and terminal predicates

The future result must report actual integers:

```yaml
required_group_count: 15
required_groups_covered: 15
discovered: N
executed: N
evidence_complete: N
passed: N
failed: 0
skipped: 0
unknown: 0
timeout: 0
```

`N` is obtained only from the actual canonical `verification_records` array. It must not be inferred from the number of groups. Every group must contribute at least one leaf; a leaf belongs to exactly one group. Missing evidence, unexecuted leaf, skipped/unknown/timeout outcome, duplicate leaf ID, inconsistent count, or a failed check yields the BLOCKED status.

`verification_method`, `subject_identity`, `expected_value`, and `observed_value` are deterministic UTF-8 strings. Structured expected/observed values are themselves compact canonical JSON strings. A PASS may not be based on prose alone.

## 12. G00 and human authorization transition

### 12.1 Waiting state

The state created by this contract is exactly:

```yaml
current_status: "PASS_R3G03_MINIMAL_EMBEDDED_ROLE_MAPPING_CONTRACT_DEFINED"
next_phase_id: "Phase 2-G-R3G03-M1"
next_phase_kind: "r3g03_minimal_embedded_role_mapping_and_deterministic_verification_only"
scope_status: "mapping_contract_defined_waiting_for_explicit_mapping_authorization"
execution_authorized: false
mapping_authorized: false
mapping_ready_for_authorization_review: true
```

Contract-definition PASS is not execution authorization.

### 12.2 Required future human action

Only a new explicit human message may transition the future mapping into its one authorized execution attempt. That message must quote and approve all of:

```yaml
contract_path: "R3G03_MINIMAL_EMBEDDED_ROLE_MAPPING_CONTRACT.md"
contract_sha256: "<exact external SHA-256 of this contract>"
phase_id: "Phase 2-G-R3G03-M1"
phase_kind: "r3g03_minimal_embedded_role_mapping_and_deterministic_verification_only"
mapping_result_artifact_path: "R3G03_MINIMAL_EMBEDDED_ROLE_MAPPING_RESULT.json"
mapping_write_scope_sha256: "f570cbd2274c09f801467859e6ac7a86db31618be706d20c345d78141b7e5a0f"
approval_scope: "R3G-03 minimal embedded-role mapping and contract-enumerated deterministic static verification only"
```

The message must explicitly authorize mapping execution. Merely repeating a logical goal, saying `approve`, authorizing planning, or citing a filename without the exact digest is insufficient.

After exact validation of that new action, and only for G00 plus the single mapping attempt, the execution controller may observe:

```yaml
scope_status: "explicitly_authorized_for_single_r3g03_mapping_execution"
mapping_authorized: true
execution_authorized: true
r3_execution_authorized: false
r4_execution_authorized: false
candidate_execution_authorized: false
```

This transition does not occur in the present contract-definition phase. Authorization is non-transferable to R3G-04, fresh R3 replan, R3, R4, Candidate, a retry with changed bytes, or any alternate path.

### 12.3 Future G00

Before any project write, future execution must verify:

1. the exact contract bytes and externally approved digest;
2. exact phase ID, phase kind, result path, write-scope digest, and approval scope;
3. a new explicit human mapping authorization exists;
4. the result path is absent and no existing modification or directory creation is proposed;
5. all five normative documents and all §10 frozen files match their exact digests;
6. R3G-07 still has the exact PASS result and trust identities in this contract;
7. the five embedded paths and six callable tuples match;
8. mapping ambiguity, unresolved input, scope expansion, and required Runtime modification are all zero;
9. R3/R4/Candidate execution remains unauthorized;
10. English/Greek TEI, Source Layer content, Candidate, model, and business inputs are absent from read and write authority.

Any G00 mismatch returns `BLOCKED_R3_ROLE_GAP_UNRESOLVED` externally with project writes equal to zero. Inputs may not be modified to make G00 pass.

## 13. PASS, BLOCKED, and claim boundary

The only success status is:

```text
PASS_R3G03_MINIMAL_EMBEDDED_ROLE_MAPPING
```

It is permitted only when G00 passes, all result-schema predicates pass, all 15 groups have complete actual leaf coverage, all seven parser-scope child results pass, all four direct edges and six callables pass, signed-role binding matches R3G-07, existing/Runtime modifications are zero, Runtime tests and model calls are zero, and the sole canonical result is created within the exact write scope.

PASS means only:

> The frozen current embedded Runtime logic is sufficient to carry the Portable / Development / A1 minimal parser-scope role identity.

The only failure status is:

```text
BLOCKED_R3_ROLE_GAP_UNRESOLVED
```

It applies to any failed required predicate. PASS does not mean parser strengthening is complete, an independent parser exists, R4 parser/gateway work is complete, R3 has passed, R4 is authorized, Candidate is available, OS-level no-bypass is proven, or the result is hardened/certified.

```yaml
assurance_profile_id: "CTDE-PORTABLE-DEV-1"
highest_claimed_evidence_level: "A1"
a2_os_file_access_proof: "NOT_PROVIDED"
hardened: false
certified: false
```

## 14. Post-mapping semantics

On future mapping PASS, the only logical successor is:

```yaml
logical_successor:
  gap_id: "R3G-04-DISCARD-ONLY-MODEL-GATEWAY"
  action: "R3G-04 minimal embedded-role mapping"
  successor_machine_contract_defined: false
  successor_execution_authorized: false
```

This contract deliberately does not define R3G-04's complete machine phase, artifact schema, path, write scope, or authorization transition. It does not execute R3G-04. A later contract-recovery/definition action must establish those fields before R3G-04 mapping can run.

After R3G-03 PASS, mapping and general execution authority return to false. Fresh R3 replan remains required but may occur only after the separately contracted R3G-04 mapping PASS and its own authorization boundary.

## 15. Contract-definition acceptance and action ledger

The contract-definition acceptance predicates are:

```yaml
phase_id_uniquely_defined: true
phase_kind_uniquely_defined: true
scope_status_uniquely_defined: true
mapping_authorization_semantics_closed: true
mapping_result_artifact_path_count: 1
mapping_write_scope_closed: true
read_only_authority_closed: true
five_path_identity_contract_complete: true
six_callable_identity_contract_complete: true
dependency_edge_contract_complete: true
parser_scope_identity_contract_complete: true
signed_role_binding_contract_complete: true
deterministic_verification_contract_complete: true
pass_blocked_states_unique: true
human_authorization_transition_semantics_closed: true

unresolved_machine_contract_ambiguity_count: 0
runtime_modification_required_count: 0
r2_semantic_regression_count: 0
scope_expansion_into_r4_count: 0

final_status: "PASS_R3G03_MINIMAL_EMBEDDED_ROLE_MAPPING_CONTRACT_DEFINED"
```

This contract-definition phase created only this file:

```yaml
created_files:
  - "R3G03_MINIMAL_EMBEDDED_ROLE_MAPPING_CONTRACT.md"
modified_existing_files: []

existing_file_modification_count: 0
runtime_modification_count: 0
test_count: 0
r3g03_mapping_execution_count: 0
r3g04_mapping_execution_count: 0
fresh_r3_replan_count: 0
r3_execution_count: 0
r4_execution_count: 0
candidate_run_count: 0
model_call_count: 0
english_tei_content_read_count: 0
greek_tei_content_read_count: 0
business_output_count: 0
```

## 16. Next-step machine Gate

```yaml
current_status: "PASS_R3G03_MINIMAL_EMBEDDED_ROLE_MAPPING_CONTRACT_DEFINED"
next_phase_id: "Phase 2-G-R3G03-M1"
next_phase_kind: "r3g03_minimal_embedded_role_mapping_and_deterministic_verification_only"
scope_status: "mapping_contract_defined_waiting_for_explicit_mapping_authorization"
execution_authorized: false
mapping_authorized: false
mapping_ready_for_authorization_review: true

mapping_result_artifact_path: "R3G03_MINIMAL_EMBEDDED_ROLE_MAPPING_RESULT.json"
mapping_write_scope_sha256: "f570cbd2274c09f801467859e6ac7a86db31618be706d20c345d78141b7e5a0f"
```

This contract stops here. It does not automatically enter mapping execution.
