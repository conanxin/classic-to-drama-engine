# Portable Runtime R4 Gate A Versioned Repair 001 Result

Status: `PASS_R4_GATE_A_VERSIONED_REPAIR`

```yaml
repair_id: "R4R-20260815-001"
suite_id: "R4PS-20260815-001"
phase_id: "Phase 2-G-R4FRESH-R1"
base_commit: "dc3d47635d44dfe72ac5333ec702cf762de5a182"
defect_count: 8
repair_scope_sha256: "e2812b2d1d9c072b3b6765771142a17bb2c8694339a6bf263c07ad59ee753729"
canonical_scope_bytes: 2379
historical_gate_a_unchanged: true
formal_gate_b_execution_authorized: false
formal_gate_b_outputs: 0
```

## Defect results

| Defect | Result |
| --- | --- |
| `R4R-D01-SYNTHETIC-BOOK-MARKER-LOCATOR` | `PASS` |
| `R4R-D02-APPEND-ONLY-INITIAL-MODE` | `PASS` |
| `R4R-D03-DENIED-LOGICAL-WRITE-EVENT` | `PASS` |
| `R4R-D04-LOGICAL-WRITE-FINALIZATION` | `PASS` |
| `R4R-D05-COMPONENT-SUBJECT-RCPT-GROUP-ID-PARSER` | `PASS` |
| `R4R-D06-SYNTHETIC-FIXTURE-OBJECT-ID-NAMESPACE` | `PASS` |
| `R4R-D07-SANDBOX-PROBE-EXECUTABLE-PREPARATION` | `PASS` |
| `R4R-D08-PYTHON-BYTECODE-PROJECT-WRITE-ESCAPE` | `PASS` |

## Fresh temporary qualification

The first two full attempts remain consumed and blocked by their independent verifiers. The newly authorized third attempt used a fresh OS-temporary clone descended directly from the frozen base, began only after targeted D08 and qualification-authorization PASS, and completed R4-E0 through R4-E10.

```yaml
attempts_authorized_total: 3
attempts_consumed_total: 3
latest_status: "PASS_R4_REPAIR_TEMP_GATE_B_QUALIFICATION"
requirement_groups: 37
manifest_leaf_count: 75
runner_discovered: 75
runner_executed: 75
evidence_complete: 75
passed: 75
failed: 0
skipped: 0
unknown: 0
timeout: 0
duplicate_attempt_ids: 0
cross_case_authorization_reuse: 0
independent_verifier_status: "PASS"
denied_write_events: 1
repeated_jsonl_append: true
logical_write_finalization: "PASS"
object_identity_consistency: "PASS"
sandbox_probe_preparation: "PASS"
unauthorized_project_tree_outputs: 0
project_python_bytecode_outputs: 0
```

D08 independently proved runner, all workers, and verifier bytecode-disabled before project imports. Project cache counts before execution, after workers, after runner, after verifier late import, and at verifier return were all zero. No cache deletion was used as proof. The exact 20-path temporary Gate B inventory was preserved without allowing Python cache paths.

## Repaired active Gate A prefix

```yaml
repair_contract_sha256: "a6d7a3fb4a504c2977b98813d6b221b83fcf3eb99d3d67767e7bd527257e7fa2"
repair_plan_sha256: "3bf2fd6e127023468873165cb5cb7e6153aeb167695ecbae9bf3fd7e299d6a61"
repaired_materialization_plan_sha256: "05a36521712b9c4afb9d042ce76fe76f225a387f654e66b8d5f215d3fe9680ce"
repaired_implementation_manifest_sha256: "b6d67dd16b1fdc15d75e344b720fd8e3534b991e7cb0ff10907e02d7ae3f3504"
repaired_closure_manifest_sha256: "70b48a10b04ff3a31cae8dd2e3224a7d89278031ed95d2b56957618ea3d0326a"
repaired_closure_payload_sha256: "448fc78f6345d4f0ebf53fa60e20ab730f7f130dcf7794d50de7d03d79b143f1"
repaired_component_freeze_sha256: "009a7f91a51092a3d55344c01fc83ad0859286e07770d1b9371d7cf55c93f881"
repaired_registry_record_sha256: "0df8453058ee5fcec33a002fef9af21a9d3a8db86c2dffa773359c872a4ccea9"
qualification_evidence_sha256: "b32ac9db75922480bceda12e2338ff37b5a5378c0d09a96dfe4b6577383277b9"
repair_verification_sha256: "d182ff03549f329715dd44698e152ed4b77371281e0a4c6553e5f3c6a665df5e"
deterministic_closure_build_count: 2
deterministic_closure_builds_byte_identical: true
implementation_file_count: 16
closure_node_count: 356
closure_edge_count: 438
verified_callable_root_count: 40
```

The tracked `runtime_capability_prototype/bin/consumer_probe` remains SHA-256 `f1f4849e078169d14ae18c91a5469b171534479dd8255de359f588ca1b475c80`, 803952 bytes, Git/filesystem mode `0644`. Historical Gate A artifacts retain their original hashes.

## Action boundary

```yaml
model_calls: 0
Candidate_runs: 0
English_TEI_content_reads: 0
Greek_TEI_content_reads: 0
business_outputs: 0
```

The repaired Gate A prefix is ready for an independent repair commit and normal push. Every prior Gate B payload remains superseded. After persistence, a new human-approval payload must be generated from actual committed bytes. This result does not authorize or execute formal `Phase 2-G-R4FRESH-E1`.
