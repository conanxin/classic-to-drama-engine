# R3G-04 Minimal Embedded-Role Mapping Machine Contract

## 0. Contract conclusion and execution boundary

This contract defines and freezes the missing machine contract for `R3G-04-DISCARD-ONLY-MODEL-GATEWAY`. It does not execute the mapping. It does not modify Runtime bytes, run Runtime code, invoke a model, read TEI content, create a fresh R3 plan, or authorize R3, R4, Candidate, analysis, episode, or screenplay work.

```yaml
contract_definition_status: "PASS_R3G04_MINIMAL_EMBEDDED_ROLE_MAPPING_CONTRACT_DEFINED"
future_mapping_phase:
  phase_id: "Phase 2-G-R3G04-M1"
  phase_kind: "r3g04_minimal_embedded_role_mapping_and_deterministic_verification_only"
  scope_status_before_execution: "mapping_contract_defined_waiting_for_explicit_mapping_authorization"
  execution_authorized: false
  mapping_authorized: false
  mapping_ready_for_authorization_review: true
mapping_result_artifact_path: "R3G04_MINIMAL_EMBEDDED_ROLE_MAPPING_RESULT.json"
mapping_write_scope_sha256: "5d9c4d6af45310ee81d7f5d4fb588e36cfbb5cbadb37c002722f0fed551a8811"
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

The phase identity above is the one and only future R3G-04 mapping phase defined by this contract. No synonym, alias, alternate candidate, or prose-derived phase identity is valid.

## 1. Normative sources and frozen current identities

The following exact files are the closed normative source set for this contract. SHA-256 values were recomputed from current disk bytes before contract creation.

| Exact path | SHA-256 | Normative purpose |
| --- | --- | --- |
| `R3G03_MINIMAL_EMBEDDED_ROLE_MAPPING_RESULT.json` | `78df12d69794d5fdc54d5e18c422744ec65ee6e898589ff8b833bb628e24e8b2` | PASS prerequisite, parser-scope identity, and logical successor |
| `R3G03_MINIMAL_EMBEDDED_ROLE_MAPPING_CONTRACT.md` | `208a9fa5a6fc098068cb247102918f3e97273c71bad840366ccc285179720602` | prior phase identity and signed-role binding |
| `PORTABLE_RUNTIME_ROLE_GAP_RESOLUTION_PLAN.md` | `72f116ff0b93403961a045228706f9322deea008f41718acae6178b0780b8798` | exact R3G-04 adjudication and role evidence |
| `PORTABLE_RUNTIME_PUBLIC_TRUST_BINDING_PLAN.md` | `fbd689f287be47aa5aa9cc3ebb256c9b7512101be073d92b1d27ae65ce0c577a` | R3G-07 ordering and public-trust dependency |
| `PORTABLE_RUNTIME_TRANSITIVE_CLOSURE_PLAN.md` | `f8ca07eaee1fff534e97bf4a0d037ba73a3c1838107e132f7c072b1fe05b39f5` | member, callable, edge, and deterministic evidence rules |
| `RUNTIME_CAPABILITY_REPAIR_PLAN.md` | `a2c52dbaecf3956cf4a2189abe5401f269d255e8099d3345985619be25be4213` | bounded-reader and audit repair boundary |
| `RUNTIME_ASSURANCE_PROFILE_DECISION.md` | `57471c85c57946f6ceb6da288301cc802533b09c137bfbe8e6e247dad57206e2` | Portable / Development / A1 claim ceiling |
| `CANDIDATE_EXECUTION_CONTRACT_REPAIR.md` | `12ceb01cab4901cb2b7472b1b56f93750a43cb8c28b5f0c9ab89acf3ad4fe7bd` | Candidate boundary and prohibition on treating this role as real model mediation |

A future mapping must recompute every digest in this table. Any absent file or mismatch is `BLOCKED_R3_ROLE_GAP_UNRESOLVED`; no new digest may be substituted.

## 2. Frozen R3G-04 gap identity

The following identity is recovered from the formal role-gap adjudication and must be preserved without reclassification:

```yaml
gap_identity:
  gap_id: "R3G-04-DISCARD-ONLY-MODEL-GATEWAY"
  gap_short_id: "R3G-04"
  runtime_role: "model gateway"
  primary_classification: "G.deferred_to_R4"
  secondary_classifications:
    - "C.missing_contract_or_schema_binding"
  embedded_runtime_logic_evidence_present: true
  blocks_r3_under_current_r3p: true
  requires_pre_r3_repair_after_adjudication: false
  stale_gap_candidate: true
  scope_status_at_gap_level: "current_logic_paths_resolved; formal_identity_requires_fresh_replan; future_strengthening_deferred_to_R4P"
  repair_phase: null
```

`R3G-04` is blocked by `R3G-03`. The completed R3G-03 result in §10 satisfies that prerequisite. This contract does not reopen or re-execute R3G-03.

## 3. Minimal embedded-role definition and claim ceiling

For `CTDE-PORTABLE-DEV-1`, Development, A1 only, the minimal embedded role is the exact current logic that:

1. records the accepted scope as `synthetic_book1_only`;
2. fails closed when the existing `gateway_book2_injection` trigger is true;
3. records `greek_events` as integer `0`;
4. records `range_outside_events` as integer `0`;
5. records `model_invocations` as integer `0`;
6. records `payload_persisted` as JSON boolean `false`;
7. signs the resulting gateway event and correlates that signed event through the scope attestation and closure attestation paths; and
8. performs no real model invocation.

This role is not a real LLM or model gateway, Candidate payload mediation, an independent gateway service, model API integration, prompt construction, or payload-trimming implementation. Independent model-input mediation and any real Candidate model-input gateway remain `deferred_to_R4` / Candidate. A mapping PASS does not strengthen that boundary.

## 4. Runtime member, support, and historical-driver classification

### 4.1 Minimal embedded Runtime role members

The minimal Runtime role has exactly two members:

| Member ID | Module | Exact relative path | SHA-256 | Role |
| --- | --- | --- | --- | --- |
| `R3G04-M01` | `ctde_runtime.bounded_reader` | `runtime_capability_prototype/runtime/ctde_runtime/bounded_reader.py` | `65c8f0a3af625c505fcdc05f7a754075e4829d2183931d71fa8c4dfdbf46f68c` | produces the fixed gateway event and raises the Book 2 fail-closed error |
| `R3G04-M02` | `ctde_runtime.read_audit` | `runtime_capability_prototype/runtime/ctde_runtime/read_audit.py` | `b5c8a9210c4f9f295351b32e3f2a5e310ad0531720ff886a9d84385ec1ab6b4d` | verifies the signed gateway log, checks direct gateway predicates, and binds scope to closure |

Both members are required. No test harness, model service, prompt layer, payload mediator, or trimming component is a member.

### 4.2 Direct support paths

These paths are immutable direct support inputs, not independent gateway-role members:

| Support ID | Exact relative path | SHA-256 | Purpose |
| --- | --- | --- | --- |
| `R3G04-S01` | `runtime_capability_prototype/runtime/ctde_runtime/events.py` | `808115293ec818eedd926e4ef63869a7d5f9eeb1dca26a6902c12850b4e7fd15` | `SignedEventLog` append and verification |
| `R3G04-S02` | `runtime_capability_prototype/runtime/ctde_runtime/signing.py` | `5c41a1601b9824715d17ae416513646575006a9207dedd26bb2036336e66cc36` | frozen R3G-07 JWS implementation input |
| `R3G04-S03` | `runtime_capability_prototype/runtime/ctde_runtime/common.py` | `20a1d4c184753f007e4da2b11cabc3f96b1049d75aa69673ddfbe0d26344aa56` | `PrototypeError` error identity |

### 4.3 Historical and test-driving evidence

```yaml
historical_driver_identity:
  driver_id: "R3G04-H01"
  path: "runtime_capability_prototype/runtime/run_suite.py"
  sha256: "caf32bdb9c49ba78ee1671d41b62bc9eb8297343624ceb7afd562443a6794749"
  classification: "legacy_injection_vector_and_historical_driver_evidence_only"
  minimal_runtime_role_member: false
  production_gateway_identity: false
```

`CaseHarness._read_delivery` forwards `gateway_book2_injection` to `BoundedReader.consume`; `CaseHarness._positive_pipeline` forwards the same parameter; and the `RCPT-T18-BOOK2-MARKER` driver supplies `self.suffix == "GATEWAY"`. These facts are historical test-driving evidence only. They do not promote `run_suite.py` into the Runtime role or define a production gateway.

## 5. Selected callable identity contract

Each selected identity is the closed tuple `(callable_id, callable_classification, module, qualname, relative_path, containing_file_sha256, definition_count)`. Definition uniqueness means exactly one AST definition with the exact qualname in the exact containing bytes; line numbers are not identity fields.

| Callable ID | Classification | Module | Qualname | Relative path | Containing-file SHA-256 | Definition count |
| --- | --- | --- | --- | --- | --- | --- |
| `R3G04-C01` | `minimal_gateway_core` | `ctde_runtime.bounded_reader` | `BoundedReader.consume` | `runtime_capability_prototype/runtime/ctde_runtime/bounded_reader.py` | `65c8f0a3af625c505fcdc05f7a754075e4829d2183931d71fa8c4dfdbf46f68c` | `1` |
| `R3G04-C02` | `signed_event_direct_support` | `ctde_runtime.events` | `SignedEventLog.append` | `runtime_capability_prototype/runtime/ctde_runtime/events.py` | `808115293ec818eedd926e4ef63869a7d5f9eeb1dca26a6902c12850b4e7fd15` | `1` |
| `R3G04-C03` | `signed_event_direct_support` | `ctde_runtime.events` | `SignedEventLog.verify` | `runtime_capability_prototype/runtime/ctde_runtime/events.py` | `808115293ec818eedd926e4ef63869a7d5f9eeb1dca26a6902c12850b4e7fd15` | `1` |
| `R3G04-C04` | `minimal_gateway_core` | `ctde_runtime.read_audit` | `ReadAuditAggregator._verify_logs` | `runtime_capability_prototype/runtime/ctde_runtime/read_audit.py` | `b5c8a9210c4f9f295351b32e3f2a5e310ad0531720ff886a9d84385ec1ab6b4d` | `1` |
| `R3G04-C05` | `minimal_gateway_core` | `ctde_runtime.read_audit` | `ReadAuditAggregator._event_data` | `runtime_capability_prototype/runtime/ctde_runtime/read_audit.py` | `b5c8a9210c4f9f295351b32e3f2a5e310ad0531720ff886a9d84385ec1ab6b4d` | `1` |
| `R3G04-C06` | `minimal_gateway_core` | `ctde_runtime.read_audit` | `ReadAuditAggregator.create_scope_attestation` | `runtime_capability_prototype/runtime/ctde_runtime/read_audit.py` | `b5c8a9210c4f9f295351b32e3f2a5e310ad0531720ff886a9d84385ec1ab6b4d` | `1` |
| `R3G04-C07` | `minimal_gateway_core` | `ctde_runtime.read_audit` | `ReadAuditAggregator.create_closure_attestation` | `runtime_capability_prototype/runtime/ctde_runtime/read_audit.py` | `b5c8a9210c4f9f295351b32e3f2a5e310ad0531720ff886a9d84385ec1ab6b4d` | `1` |

This seven-callable set is exact. `JWSCodec.sign`, `JWSCodec.verify`, and `JWSCodec.digest` remain frozen signed-role support under the R3G-07 binding in §11; they are not remapped as gateway-role callables. Historical `CaseHarness` methods are not selected callables.

## 6. Closed dependency-edge contract

Edge direction is gateway evidence flow from producer toward the attestation consumer. Every edge has exactly `edge_id`, `from_id`, `to_id`, `relation`, and `exact_semantic_locator`.

| Edge ID | From | To | Relation | Exact semantic locator |
| --- | --- | --- | --- | --- |
| `R3G04-E01` | `R3G04-C01` | `R3G04-C02` | `gateway_event_emitted_through` | the unique call on `gateway_events.append` whose first argument is exact string `gateway_scope_result` and whose second argument is the six-key dictionary in §7 |
| `R3G04-E02` | `R3G04-C03` | `R3G04-C04` | `signed_domain_log_verified_by` | the unique `_verify_logs` call to `SignedEventLog.verify` using expected attempt, domain, issuer, and audience identities |
| `R3G04-E03` | `R3G04-C04` | `R3G04-C06` | `verified_gateway_domain_supplied_to` | the unique `create_scope_attestation` call of `_verify_logs(logs, SCOPE_DOMAINS, attempt_id)` |
| `R3G04-E04` | `R3G04-C05` | `R3G04-C06` | `gateway_event_selected_by` | the unique `_event_data(verified["gateway"], "gateway_scope_result")` call |
| `R3G04-E05` | `R3G04-C06` | `R3G04-C07` | `scope_attestation_digest_bound_into` | the unique assignment of `scope_digest` from `JWSCodec.digest(scope_attestation)` when present, followed by the unique closure payload field `scope_execution_attestation_sha256` whose value is `scope_digest` |

A locator must match exactly one AST/source semantic site. A broad first-match rule, including “the first raise” or “the first append,” is invalid. Missing, duplicate, or changed endpoints or locators are BLOCKED.

## 7. Embedded gateway event contract

The gateway event kind is exact string `gateway_scope_result`. Its gateway-specific `data` object has exactly six fields and no others:

| Field | JSON type | Canonical representation | Allowed value | PASS meaning | Fail-closed condition |
| --- | --- | --- | --- | --- | --- |
| `accepted_scope` | string | JSON string | exact `synthetic_book1_only` | current synthetic scope is Book 1 only | absent, non-string, or any other string |
| `book2_events` | integer | JSON integer | `0` on accepted path; `1` only on the exact injection path in §8 | accepted path contains no Book 2 event | any non-injection nonzero; any value outside `{0,1}`; or injection value not `1` |
| `greek_events` | integer | JSON integer | exact `0` | Greek events remain zero | any other value or type |
| `range_outside_events` | integer | JSON integer | exact `0` | range-outside events remain zero | any other value or type |
| `model_invocations` | integer | JSON integer | exact `0` | no model call occurred | any other value or type |
| `payload_persisted` | boolean | JSON literal | exact `false` | payload was not persisted | `true` or any non-boolean |

JSON booleans are not integers. No coercion is permitted. Dictionary key spelling, case, and cardinality are exact. The signed event envelope created by `SignedEventLog.append` is support infrastructure and is not an extension of this six-field gateway data schema.

The normal accepted identity is:

```json
{"accepted_scope":"synthetic_book1_only","book2_events":0,"greek_events":0,"model_invocations":0,"payload_persisted":false,"range_outside_events":0}
```

Its meaning is limited to the synthetic Book 1-only A1 path. It is not evidence that a Candidate payload was accepted or mediated.

## 8. Book 2 injection and rejection contract

```yaml
injection_identity:
  trigger_owner: "ctde_runtime.bounded_reader.BoundedReader.consume"
  trigger_parameter: "gateway_book2_injection"
  trigger_type_identity: "bool_default_false"
  injected_value: true
  event_kind: "gateway_scope_result"
  event_book2_events: 1
  event_accepted_scope: "synthetic_book1_only"
  event_greek_events: 0
  event_range_outside_events: 0
  event_model_invocations: 0
  event_payload_persisted: false
  event_precedes_rejection: true
  rejection_exception_module: "ctde_runtime.common"
  rejection_exception_qualname: "PrototypeError"
  rejection_code: "INVALIDATED_PROTOTYPE_SCOPE_EXCEEDED"
  rejection_detail: "gateway Book 2"
  expected_outcome: "fail_closed"
```

The exact semantic rejection locator is the unique `if gateway_book2_injection` guard that follows the exact gateway event append and contains the exact `PrototypeError` construction above. It must not be located through an earlier generic raise or a first-match shortcut. If the event, guard, order, error code, detail, zero-model condition, or false-persistence condition cannot be uniquely and deterministically located, the injection obligation fails.

The historical `run_suite.py` trigger path in §4.3 can corroborate this identity but cannot replace direct verification of `BoundedReader.consume`. No real model may be called to test rejection.

## 9. Audit correlation contract

### 9.1 Directly verified properties

`ReadAuditAggregator.create_scope_attestation` first obtains verified scope-domain logs, requires a gateway domain, and retrieves `gateway_scope_result`. On the expected-completed path, current bytes directly predicate-check exactly:

```yaml
directly_verified:
  gateway_event_exists: true
  book2_events_equals: 0
  greek_events_equals: 0
  model_invocations_equals: 0
```

The direct locators are the exact gateway `_event_data` call, the conjunction requiring non-null gateway with `book2_events == 0` and `greek_events == 0`, and the exact `gateway["model_invocations"] == 0` predicate. A future result must not report any additional gateway data field as directly predicate-checked by this callable.

### 9.2 Properties bound by embedded signed-result identity

Current audit bytes do not directly predicate-check `accepted_scope`, `range_outside_events`, or `payload_persisted`. They are instead closed by all of the following current identities:

```yaml
bound_by_embedded_result_identity:
  fields:
    - "accepted_scope"
    - "range_outside_events"
    - "payload_persisted"
  producer: "R3G04-C01"
  exact_event_schema_required: true
  signed_event_append_required: true
  signed_gateway_log_verification_required: true
  gateway_component_event_chain_digest_required: true
  scope_attestation_digest_in_closure_required: true
```

The scope attestation payload builds `component_event_chain_digests` from `JWSCodec.digest(logs[domain].tokens[-1])` for every `SCOPE_DOMAINS` member after those same domain logs have passed `_verify_logs`; therefore its gateway entry is the digest of the final verified gateway-domain signed token. On the current success path the exact gateway event is that final gateway token. `create_closure_attestation` computes `scope_digest` as `JWSCodec.digest(scope_attestation)` when the attestation is present and places that value in `scope_execution_attestation_sha256`. The future verifier must prove each link from exact AST/source semantics and frozen file identities.

“Bound by embedded result identity” is not the same claim as “directly verified.” If signed log verification, final-token identity, scope chain digest, or closure digest linkage is absent or ambiguous, these three fields are not closed and the mapping is BLOCKED. Runtime must not be changed to turn them into direct checks during this phase.

## 10. R3G-03 prerequisite binding

The future mapping input must contain this exact prerequisite identity:

```yaml
r3g03_prerequisite_identity:
  result_path: "R3G03_MINIMAL_EMBEDDED_ROLE_MAPPING_RESULT.json"
  result_sha256: "78df12d69794d5fdc54d5e18c422744ec65ee6e898589ff8b833bb628e24e8b2"
  final_status: "PASS_R3G03_MINIMAL_EMBEDDED_ROLE_MAPPING"
  parser_scope_identity_canonicalization_id: "CTDE-R3G04-DEPENDENCY-JCS-1"
  parser_scope_identity_canonical_byte_length: 888
  parser_scope_identity_sha256: "087448cd8f133acc3ffe317f0db7c6bf52ae43db00f52cea3843fbcc0aad0aa2"
  r3g03_reexecution_required: false
  r3g03_reexecution_permitted: false
```

`CTDE-R3G04-DEPENDENCY-JCS-1` means the exact `parser_scope_identity` object from the frozen R3G-03 result, serialized as UTF-8 without BOM, compact JSON, object keys ordered by Unicode code point, followed by one LF. The 888-byte digest above was computed from the actual object. The future mapping must recompute it and require all seven parser-scope children to remain PASS. Reconstructing it from prose is forbidden.

## 11. R3G-07 signed-role and public-trust binding

R3G-07 outputs are immutable input identities. R3G-04 must not generate, rotate, replace, or reinterpret a trust asset, and must not read or create a private signing key.

```yaml
signed_role_binding:
  assurance_profile_id: "CTDE-PORTABLE-DEV-1"
  trust_domain: "ctde-portable-runtime"
  public_trust_freeze_identity: "7a4a664a8fcccea98ee600d853fc9d36107e307ec2e7e078c9fad42363a831f3"
  kid: "ctde-portable-dev-20260813-01"
  public_key_bytes_sha256: "32a457033c8eefa8bea45ce347cb17ef08c928fabf7c2139ead1ab8af29aef5f"
  public_key_status: "active"
  trust_material_path: "runtime_capability_prototype/contracts/portable_public_trust_material_v1.json"
  trust_material_sha256: "dcac3ed439a24639736b01f035ef121ac025bd7c9e93882040c7ebcc7350e3cc"
  status_registry_path: "runtime_capability_prototype/contracts/portable_public_key_status_registry_v1.json"
  status_registry_sha256: "d0e13ff804bbd224146133b67853b4256756fbd4c995c8045edadfdbc576bc4d"
  loader_path: "runtime_capability_prototype/runtime/ctde_runtime/public_trust.py"
  loader_sha256: "72103c6de973a7f575c553681edcf097c46123d263c81b0edbdbed28f94dd5b8"
  signing_path: "runtime_capability_prototype/runtime/ctde_runtime/signing.py"
  signing_sha256: "5c41a1601b9824715d17ae416513646575006a9207dedd26bb2036336e66cc36"
  binding_strength: "portable_a1_approved_composition"
  trust_assets_generated_by_mapping: false
  private_key_dependency: false
```

The future mapping must verify that current R3G-03 and R3G-07 evidence bind `BoundedReader.consume` and `ReadAuditAggregator._verify_logs` to the same public-trust freeze identity. These identities are inputs; R3G-04 creates no trust material.

## 12. Future mapping write scope

The exact canonical write-scope bytes, including one terminal LF, are:

```json
{"creatable_directories":[],"creatable_files":["R3G04_MINIMAL_EMBEDDED_ROLE_MAPPING_RESULT.json"],"mutable_existing_files":[]}
```

```yaml
mapping_write_scope_canonicalization_id: "CTDE-R3G04-WRITE-SCOPE-JCS-1"
mapping_write_scope_byte_length: 127
mapping_write_scope_sha256: "5d9c4d6af45310ee81d7f5d4fb588e36cfbb5cbadb37c002722f0fed551a8811"
mutable_existing_files: []
creatable_files:
  - "R3G04_MINIMAL_EMBEDDED_ROLE_MAPPING_RESULT.json"
creatable_directories: []
runtime_modification_count: 0
```

No manifest, runner, verifier, evidence file, schema file, helper source, Markdown result, debug artifact, cache, bytecode, directory, or fresh R3 plan may be created in the project tree. OS temporary files are not project artifacts and must be removed after the single attempt. If deterministic verification cannot close inside OS temporary storage plus the one result, the terminal state is `BLOCKED_R3_ROLE_GAP_UNRESOLVED`; the write scope must not expand.

## 13. Result artifact contract

### 13.1 Sole path and schema identity

```yaml
mapping_result_artifact_path: "R3G04_MINIMAL_EMBEDDED_ROLE_MAPPING_RESULT.json"
artifact_class: "ctde_r3g04_minimal_embedded_role_mapping_result"
schema_id: "urn:ctde:contract:r3g04-minimal-embedded-role-mapping-result:1"
schema_version: "1.0.0"
canonicalization_id: "CTDE-R3G04-MAPPING-JCS-1"
```

### 13.2 Closed result field set

The result has exactly these required top-level fields and no others:

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
  - "r3g03_prerequisite_identity"
  - "runtime_path_identities"
  - "support_path_identities"
  - "historical_driver_identity"
  - "callable_identities"
  - "dependency_edges"
  - "gateway_event_identity"
  - "book2_injection_identity"
  - "audit_correlation_identity"
  - "signed_role_binding"
  - "verification_summary"
  - "verification_records"
  - "action_ledger"
  - "final_status"
  - "logical_successor"
  - "post_mapping_authorization"
```

The first four fields have the exact scalar values in §13.1. Closed child fields are:

```yaml
contract_identity_fields: ["path", "sha256", "byte_length"]
phase_identity_fields: ["phase_id", "phase_kind", "scope_status_at_start"]
gap_identity_fields: ["gap_id", "gap_short_id", "runtime_role", "primary_classification", "secondary_classifications", "embedded_runtime_logic_evidence_present", "blocks_r3_under_current_r3p", "requires_pre_r3_repair_after_adjudication", "stale_gap_candidate", "scope_status_at_gap_level", "repair_phase"]
assurance_identity_fields: ["assurance_profile_id", "highest_claimed_evidence_level", "environment_class", "hardened", "certified", "candidate_ready"]
authorization_identity_fields: ["explicit_human_mapping_authorization_received", "approved_contract_path", "approved_contract_sha256", "approved_phase_id", "approved_phase_kind", "approved_mapping_result_artifact_path", "approved_mapping_write_scope_sha256", "approval_attempt_count"]
write_scope_identity_fields: ["mutable_existing_files", "creatable_files", "creatable_directories", "mapping_write_scope_sha256"]
r3g03_prerequisite_identity_fields: ["result_path", "result_sha256", "final_status", "parser_scope_identity_canonicalization_id", "parser_scope_identity_canonical_byte_length", "parser_scope_identity_sha256", "r3g03_reexecuted", "result"]
historical_driver_identity_fields: ["driver_id", "path", "sha256", "classification", "minimal_runtime_role_member", "production_gateway_identity", "result"]
gateway_event_identity_fields: ["event_kind", "data_field_count", "data_fields", "normal_path_values", "event_producer_callable_id", "result"]
book2_injection_identity_fields: ["trigger_owner", "trigger_parameter", "trigger_type_identity", "injected_value", "event_values", "event_precedes_rejection", "rejection_exception_module", "rejection_exception_qualname", "rejection_code", "rejection_detail", "expected_outcome", "result"]
audit_correlation_identity_fields: ["directly_verified_fields", "bound_by_embedded_result_identity_fields", "gateway_domain_required", "signed_log_verified", "gateway_chain_digest_bound", "scope_attestation_digest_bound_into_closure", "result"]
signed_role_binding_fields: ["assurance_profile_id", "trust_domain", "public_trust_freeze_identity", "kid", "public_key_bytes_sha256", "public_key_status", "trust_material_path", "trust_material_sha256", "status_registry_path", "status_registry_sha256", "loader_path", "loader_sha256", "signing_path", "signing_sha256", "binding_strength", "trust_assets_generated_by_mapping", "private_key_dependency", "result"]
verification_summary_fields: ["requirement_groups", "required_groups_covered", "leaves_discovered", "leaves_executed", "evidence_complete", "leaves_passed", "failed", "skipped", "unknown", "timeout"]
action_ledger_fields: ["existing_file_modification_count", "runtime_modification_count", "runtime_test_count", "r3g03_reexecution_count", "r3g04_mapping_attempt_count", "fresh_r3_replan_count", "r3_execution_count", "r4_execution_count", "candidate_run_count", "model_call_count", "english_tei_content_read_count", "greek_tei_content_read_count", "business_output_count", "scope_violation_count"]
logical_successor_fields: ["action", "successor_machine_contract_defined", "successor_execution_authorized", "next_phase_id", "next_phase_kind", "scope_status", "plan_artifact_path", "write_scope_sha256"]
post_mapping_authorization_fields: ["mapping_authorized", "execution_authorized", "fresh_r3_replan_authorized", "r3_execution_authorized", "r4_execution_authorized", "candidate_execution_authorized"]
```

Closed array item fields and order are:

```yaml
source_document_identities:
  exact_count: 8
  item_fields: ["path", "sha256", "result"]
  exact_members: "the eight paths and digests in section 1"
  order: "path"
runtime_path_identities:
  exact_count: 2
  item_fields: ["member_id", "module", "path", "sha256", "role", "result"]
  exact_members: ["R3G04-M01", "R3G04-M02"]
  order: "member_id"
support_path_identities:
  exact_count: 3
  item_fields: ["support_id", "path", "sha256", "purpose", "minimal_runtime_role_member", "result"]
  exact_members: ["R3G04-S01", "R3G04-S02", "R3G04-S03"]
  order: "support_id"
callable_identities:
  exact_count: 7
  item_fields: ["callable_id", "callable_classification", "module", "qualname", "relative_path", "containing_file_sha256", "definition_count", "result"]
  exact_members: ["R3G04-C01", "R3G04-C02", "R3G04-C03", "R3G04-C04", "R3G04-C05", "R3G04-C06", "R3G04-C07"]
  order: "callable_id"
dependency_edges:
  exact_count: 5
  item_fields: ["edge_id", "from_id", "to_id", "relation", "exact_semantic_locator", "result"]
  exact_members: ["R3G04-E01", "R3G04-E02", "R3G04-E03", "R3G04-E04", "R3G04-E05"]
  order: "edge_id"
gateway_event_identity.data_fields:
  exact_count: 6
  item_fields: ["field", "json_type", "allowed_value", "verification_class", "result"]
  order: "field"
verification_records:
  exact_count: "N discovered from actual leaf expansion; not preset"
  item_fields: ["leaf_id", "requirement_group_id", "verification_method", "subject_identity", "expected_value", "observed_value", "evidence_class", "result"]
  order: ["requirement_group_id", "subject_identity", "verification_method"]
```

`gateway_event_identity.normal_path_values` and `book2_injection_identity.event_values` each have exactly the six field names in §7. `audit_correlation_identity.directly_verified_fields` is exactly `gateway_event_exists`, `book2_events`, `greek_events`, and `model_invocations`; `bound_by_embedded_result_identity_fields` is exactly `accepted_scope`, `range_outside_events`, and `payload_persisted`. All objects and item objects are closed. Missing, extra, duplicate, incorrectly typed, or unknown fields are BLOCKED.

For a completed future mapping attempt, `action_ledger` is exactly:

```yaml
existing_file_modification_count: 0
runtime_modification_count: 0
runtime_test_count: 0
r3g03_reexecution_count: 0
r3g04_mapping_attempt_count: 1
fresh_r3_replan_count: 0
r3_execution_count: 0
r4_execution_count: 0
candidate_run_count: 0
model_call_count: 0
english_tei_content_read_count: 0
greek_tei_content_read_count: 0
business_output_count: 0
scope_violation_count: 0
```

### 13.3 Canonical serialization and exact byte identity

`CTDE-R3G04-MAPPING-JCS-1` requires:

1. UTF-8 without BOM;
2. compact JSON with no insignificant whitespace;
3. object keys ordered by Unicode code point;
4. arrays ordered by the stable IDs or exact order declared above;
5. no float, NaN, Infinity, duplicate key, unknown field, absolute path, `..`, symlink alias, host-derived path separator, timestamp, mtime, PID, random value, or UUID; and
6. exactly one terminal LF with no bytes after it.

The result contains no self-digest field. The exact SHA-256 covers all persisted bytes, including the terminal LF, and is computed after create-once persistence. It is reported only in external delivery metadata and any later contract or authorization that consumes the result. This self-digest exclusion rule avoids a recursive identity.

Before the one project-tree creation, two fresh-process renders from the same frozen observations in approved OS temporary storage must be byte-identical and have the same SHA-256 and byte length. Re-serializing after persistence is not a substitute for hashing exact persisted bytes.

## 14. Deterministic static verification contract

### 14.1 Execution mechanism

Future execution uses one read-only static verification controller in OS temporary storage. It may parse exact source bytes and ASTs but may not import or execute project Runtime modules, run Runtime tests, monkeypatch Runtime, invoke a model, or read fixture/TEI content. The controller must:

1. start from an exact file allowlist, not a directory traversal root;
2. verify the contract digest approved by the human authorization before other evaluation;
3. verify the sole write-scope identity and a clean project tree before any project write;
4. recompute all frozen file and prerequisite digests;
5. enumerate every required leaf from actual members, callables, edges, fields, locators, and bindings;
6. assign stable leaf IDs only after inventory expansion;
7. sort leaves by `(requirement_group_id, subject_identity, verification_method)`;
8. execute each leaf exactly once and retain complete evidence in memory/OS temp;
9. render the sole result twice in fresh processes and require byte equality; and
10. create the result once only after scope, count, evidence, and canonical-byte predicates pass.

No verifier-authored status string, expected-equals-observed rewrite, string-search-only pseudo-evidence, skipped leaf, broad first-match shortcut, or hard-coded PASS is evidence. AST/source locators must target exact semantic guards. In particular, a rejection locator must target the exact `gateway_book2_injection` parser-status-independent Book 2 guard and exact `PrototypeError`, never the first generic raise.

The same frozen input bytes and authorization identity must yield identical leaf inventory, evidence values, canonical result bytes, and digest. Any nondeterminism is BLOCKED.

### 14.2 Closed requirement-group inventory

There are exactly 18 groups. The number of leaves is the actual expanded `N`, never a preset value.

| Group ID | Required future verification obligation |
| --- | --- |
| `R3G04-VG01` | Recompute the eight normative source identities and the future contract identity; reject drift. |
| `R3G04-VG02` | Verify the two exact Runtime members, three direct support paths, and historical-driver non-member classification. |
| `R3G04-VG03` | Verify all seven callable tuples and definition count `1` by exact AST qualname. |
| `R3G04-VG04` | Verify all five dependency edges and unique exact semantic locators. |
| `R3G04-VG05` | Verify exact `gateway_scope_result` kind and the closed six-field data schema, JSON types, and allowed values. |
| `R3G04-VG06` | Verify normal synthetic Book 1-only accepted identity, including `accepted_scope == synthetic_book1_only` and `book2_events == 0`. |
| `R3G04-VG07` | Verify the exact Book 2 trigger, pre-rejection event values, unique guard, exact error class/code/detail, and fail-closed order. |
| `R3G04-VG08` | Verify every role-member write of `greek_events` is integer literal `0` and the audit direct predicate is exact. |
| `R3G04-VG09` | Verify every role-member write of `range_outside_events` is integer literal `0` and classify it only as signed-result-bound, not directly audit-checked. |
| `R3G04-VG10` | Verify every role-member production/return value of `model_invocations` is integer literal `0` and the audit direct predicate is exact. |
| `R3G04-VG11` | Verify every role-member production/return value of `payload_persisted` is JSON boolean `false` and classify it only as signed-result-bound, not directly audit-checked. |
| `R3G04-VG12` | Verify gateway signed-event append, signed-domain verification, exact direct predicates, final gateway-token chain digest, and direct-versus-bound classification. |
| `R3G04-VG13` | Verify scope-attestation digest binding into closure and reject any missing or ambiguous correlation link. |
| `R3G04-VG14` | Verify the R3G-03 result digest, PASS status, exact seven-child parser-scope identity digest, and zero R3G-03 re-execution. |
| `R3G04-VG15` | Verify every frozen R3G-07 public-trust/signed-role identity and that no trust asset or private key is generated/read. |
| `R3G04-VG16` | Verify the exact minimal write scope, clean pre-write tree, zero existing/Runtime modifications, and absence of any extra project artifact. |
| `R3G04-VG17` | Verify zero real model calls, zero Runtime tests/import execution, zero English/Greek TEI content reads, zero business outputs, and no model/network SDK import or model-call target in the selected role surface. |
| `R3G04-VG18` | Verify Development/A1/non-hardened/non-certified/non-Candidate claim ceiling, result closed schema, actual counts, two-render determinism, and canonical exact bytes. |

### 14.3 Actual counts and terminal predicates

The future result must report actual nonnegative integers:

```yaml
requirement_groups: 18
leaves_discovered: "N"
leaves_executed: "N"
evidence_complete: "N"
leaves_passed: "N"
failed: 0
skipped: 0
unknown: 0
timeout: 0
```

`N` is accepted only when obtained by actual expansion and `N > 0`. PASS requires all four `N` fields equal, every group represented by at least one leaf, every record evidence-complete and PASS, and every zero counter exactly zero. Inventory drift between the two render passes is BLOCKED; it must not be adjusted to an expected historical number.

## 15. PASS, BLOCKED, and authorization semantics

The only mapping success status is:

```text
PASS_R3G04_MINIMAL_EMBEDDED_ROLE_MAPPING
```

It means only that the frozen current embedded gateway bytes, event identity, signed audit correlation, R3G-03 prerequisite, and R3G-07 binding are sufficient for the Portable / Development / A1 minimal discard-only model-gateway role.

The unified failure status is:

```text
BLOCKED_R3_ROLE_GAP_UNRESOLVED
```

Any missing/extra member, callable, edge, field, group, leaf, evidence item, authorization binding, digest, exact locator, or correlation link; any failed/skipped/unknown/timeout leaf; any project scope violation; any Runtime mutation/import execution; any real model call; or any claim above A1 is BLOCKED. PASS does not mean Candidate gateway implementation, independent model mediation, payload trimming, R4 strengthening, real model integration, fresh R3 planning, or R3 PASS.

This contract-definition PASS does not authorize mapping. One future mapping attempt requires a new explicit human authorization quoting and approving at least:

```yaml
contract_path: "R3G04_MINIMAL_EMBEDDED_ROLE_MAPPING_CONTRACT.md"
contract_sha256: "<exact persisted contract SHA-256>"
phase_id: "Phase 2-G-R3G04-M1"
phase_kind: "r3g04_minimal_embedded_role_mapping_and_deterministic_verification_only"
mapping_result_artifact_path: "R3G04_MINIMAL_EMBEDDED_ROLE_MAPPING_RESULT.json"
mapping_write_scope_sha256: "5d9c4d6af45310ee81d7f5d4fb588e36cfbb5cbadb37c002722f0fed551a8811"
approval_scope: "R3G-04 minimal embedded-role mapping and contract-enumerated deterministic static verification only"
```

The authorization applies to exactly one attempt and cannot be inferred from this contract, a logical successor, a prior R3G-03 authorization, or an agent-authored artifact. Before that message, `execution_authorized` and `mapping_authorized` remain false.

## 16. Future pre-write gate and allowed reads

Before any future mapping write, the authorized executor must verify:

- exact human authorization fields from §15;
- this contract path, exact persisted digest, and phase identity;
- clean project tree and the absent result path;
- all §1 source digests, §4 Runtime/support/historical digests, §10 prerequisite identities, and §11 trust identities;
- exact write-scope digest; and
- no project change before terminal PASS.

The future mapping read allowlist is limited to this contract, the eight §1 sources, the six §4 Runtime/support/historical files, and the exact public trust/status/loader files already named by the frozen R3G-07 binding. Reading source code is allowed; importing/executing Runtime, reading private key material, fixture content, English/Greek TEI content, or unrelated project files is not.

If the result path already exists, the tree is dirty, an input drifts, authorization is absent/mismatched, or the allowlist is insufficient, stop without a project write. A blocked result may be persisted only if every input, authorization, and write-scope gate first passed and this sole artifact can truthfully and canonically record the blocked attempt without modifying an existing file. No automatic retry is authorized.

## 17. Post-R3G-04 logical successor

On a future mapping PASS, the only logical successor is fresh R3 file-level replan:

```yaml
logical_successor:
  action: "fresh R3 file-level replan"
  successor_machine_contract_defined: false
  successor_execution_authorized: false
  next_phase_id: null
  next_phase_kind: null
  scope_status: null
  plan_artifact_path: null
  write_scope_sha256: null
```

No formal source currently supplies those successor machine fields. The mapping result must preserve the nulls and false values unless a later, independently authorized contract-definition phase creates their exact identities. R3G-04 mapping must not execute or define the fresh R3 replan.

## 18. Contract-definition acceptance and action ledger

This contract definition is PASS only because all of these predicates close on current exact bytes:

```yaml
contract_definition_acceptance:
  r3g04_gap_identity_closed: true
  minimal_role_definition_closed: true
  runtime_members_closed: true
  selected_callable_identities_closed: true
  gateway_event_contract_closed: true
  book2_rejection_contract_closed: true
  audit_correlation_contract_closed: true
  r3g03_prerequisite_closed: true
  r3g07_signed_role_binding_closed: true
  future_phase_identity_closed: true
  future_write_scope_closed: true
  result_artifact_contract_closed: true
  deterministic_verification_contract_closed: true
  pass_blocked_semantics_closed: true
  human_authorization_semantics_closed: true
  fresh_r3_successor_semantics_closed: true
  unresolved_machine_contract_ambiguity: 0
  runtime_modification_required: 0
  r2_semantic_regression: 0
  model_calls: 0
  r4_scope_expansion: 0
```

```yaml
contract_definition_action_ledger:
  existing_project_file_modification_count: 0
  project_file_creation_count: 1
  created_project_files:
    - "R3G04_MINIMAL_EMBEDDED_ROLE_MAPPING_CONTRACT.md"
  runtime_modification_count: 0
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

## 19. Next-step machine Gate

```yaml
current_status: "PASS_R3G04_MINIMAL_EMBEDDED_ROLE_MAPPING_CONTRACT_DEFINED"
next_phase_id: "Phase 2-G-R3G04-M1"
next_phase_kind: "r3g04_minimal_embedded_role_mapping_and_deterministic_verification_only"
scope_status: "mapping_contract_defined_waiting_for_explicit_mapping_authorization"
execution_authorized: false
mapping_authorized: false
mapping_ready_for_authorization_review: true
mapping_result_artifact_path: "R3G04_MINIMAL_EMBEDDED_ROLE_MAPPING_RESULT.json"
mapping_write_scope_sha256: "5d9c4d6af45310ee81d7f5d4fb588e36cfbb5cbadb37c002722f0fed551a8811"
```

This contract stops at the waiting gate. It does not automatically enter R3G-04 mapping execution.
