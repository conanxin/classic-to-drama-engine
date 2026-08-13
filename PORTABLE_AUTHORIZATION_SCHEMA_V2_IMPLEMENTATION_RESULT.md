# Classic-to-Drama Engine：Portable Authorization Schema V2 Implementation Result

> 项目：Classic-to-Drama Engine  
> 阶段：Phase 2-G-R2  
> 日期：2026-08-11  
> 最终状态：`PASS_PORTABLE_AUTHORIZATION_SCHEMA_V2_IMPLEMENTED`  
> Assurance Profile：`CTDE-PORTABLE-DEV-1`  
> 最高声明证据等级：`A1`  
> 认证状态：`Portable only / non-certified`  
> Candidate Analysis：`BLOCKED`

## 1. 最终判定

Phase 2-G-R2 已在 `PORTABLE_AUTHORIZATION_SCHEMA_V2_PLAN.md` 批准的原子文件白名单内完成。以下条件全部真实成立：

- canonical Authorization Schema V2 已实现，`$id=urn:ctde:schema:runtime-authorization:2`、`schema_version=2.0.0`；
- authorization artifact 不含自身文件 SHA-256、size、Registry row ID 或可变消费状态；
- authoritative exact bytes BLOB、外部 SHA-256、size、schema/Profile/run/source/nonce identity 由 Registry 保存；
- V1／缺版本／未知版本／legacy alias／self-digest／缺字段／类型与语义错误均 fail closed；
- `unconsumed -> spent | revoked | expired` 为单向消费状态机；
- consume、mint lease、capability preparation、capability activation 分别使用独立 CAS、state version、durable event 和 domain-separated one-shot handle；
- authorization replay、nonce 冲突、过期、撤销、Registry digest mismatch 与 stale/wrong-stage context 均被拒绝；
- issuer、broker、bounded reader 和 read audit 的 V2 path 只接受 typed context；R2 实际调用的 broker/reader/audit path 为纯 binding probe，未打开或读取 source；
- frozen manifest 实际展开的所有 deterministic synthetic tests 全部 PASS，evidence complete；
- 最终文件树不存在 R2 白名单外差异。

因此：

```text
PASS_PORTABLE_AUTHORIZATION_SCHEMA_V2_IMPLEMENTED
```

该状态只关闭 Portable Authorization Schema V2 原子工作包，不表示 Portable Runtime、R3、R4-P、Candidate 或 Hardened 已通过。

## 2. 执行前 scope 与基线

### 2.1 正式依据摘要

| 文件 | 执行前／执行后 SHA-256 | 结果 |
| --- | --- | --- |
| `RUNTIME_CAPABILITY_PROTOTYPE_RESULT.md` | `6811bcc4ef0efcaee89013648dd0bb06bbaca154625f3dc47bdfa0f295851753` | 未变 |
| `RUNTIME_CAPABILITY_REPAIR_PLAN.md` | `a2c52dbaecf3956cf4a2189abe5401f269d255e8099d3345985619be25be4213` | 未变 |
| `RUNTIME_OS_OBSERVABILITY_PREFLIGHT_RESULT.md` | `0ca51394315199683cd790e01d160addb80f1cb0e32bb23df212045b49c433c0` | 未变 |
| `RUNTIME_ASSURANCE_PROFILE_DECISION.md` | `57471c85c57946f6ceb6da288301cc802533b09c137bfbe8e6e247dad57206e2` | 未变 |
| `CANDIDATE_EXECUTION_CONTRACT_REPAIR.md` | `12ceb01cab4901cb2b7472b1b56f93750a43cb8c28b5f0c9ab89acf3ad4fe7bd` | 未变 |
| `PORTABLE_AUTHORIZATION_SCHEMA_V2_PLAN.md` | `32513cdb2c004ea91c7d7208eb3a40901934dc80440af048b84701facf1bdbe9` | 未变 |

### 2.2 Runtime 基线

```yaml
git_state: "NOT_A_GIT_WORKTREE"
equivalent_tree_snapshot_used: true
runtime_file_count_before: 2781
runtime_content_tree_sha256_before: "4acda62cdc02fe4e72e095f56ad895f5afbcbeba9ad32d9699c7eb78c90b7072"
allowed_new_targets_existing_before: 0
fresh_r2_suite_existing_before: false
```

最终审计通过“排除批准的新文件与 fresh suite、并将 5 个允许修改文件替换为其执行前摘要”的方式重建原始 2,781 文件树；重建摘要仍为：

```text
4acda62cdc02fe4e72e095f56ad895f5afbcbeba9ad32d9699c7eb78c90b7072
```

因此批准白名单外的 Runtime 内容差异为 0。

## 3. 实际修改文件

| 文件 | 修改前 SHA-256 | 修改后 SHA-256 | R2 原子用途 |
| --- | --- | --- | --- |
| `runtime_capability_prototype/runtime/ctde_runtime/authorization_registry.py` | `26dc60926826db207cace0e871d15b587032d4cb3e861c111415d0819707ea82` | `e6ee8923c1c05c1ebdf04106fed659d40b8d394f6cbca4688d437dd58ee446af` | 独立 V2 identity/state/event/pending/active 表与 CAS 状态机 |
| `runtime_capability_prototype/runtime/ctde_runtime/range_broker.py` | `19aaaef83c92d871467a5e463581cc574b6b419f85a9a6ac9086f27868f76b26` | `ef2be994b82f10f025411e1d074cda3d0336e352f063bb9162edbcaed105958a` | issuer preparation/activation 与 broker 纯 binding probe |
| `runtime_capability_prototype/runtime/ctde_runtime/bounded_reader.py` | `c49bd965a40e52120207192fe082dc9737b565253dd4cfe62fc200a1a9cf1a99` | `65c8f0a3af625c505fcdc05f7a754075e4829d2183931d71fa8c4dfdbf46f68c` | reader 纯 typed-context binding probe |
| `runtime_capability_prototype/runtime/ctde_runtime/read_audit.py` | `735d25ff6ff41c6b77538daf1d27550d76211c20098a99a4246b5c91eb662b8b` | `b5c8a9210c4f9f295351b32e3f2a5e310ad0531720ff886a9d84385ec1ab6b4d` | A1 correlation pure probe |
| `runtime_capability_prototype/runtime/ctde_runtime/events.py` | `84d05a5c49bdf7e66f9cd68a3941e18b2577420479acf5389c69f1e6852322ac` | `808115293ec818eedd926e4ef63869a7d5f9eeb1dca26a6902c12850b4e7fd15` | Portable V2 signed A1 event chain |

V1 methods and现有 V1 schema exact bytes均未原地改写；V2 只通过显式 V2 API 与独立表进入。

## 4. 实际新增实现／合同文件

这些目标执行前全部为 `ABSENT`：

| 新文件 | SHA-256 |
| --- | --- |
| `runtime_capability_prototype/contracts/authorization_schema_v2.yaml` | `f1d7c2e36e0d3072624609591eb8dfc20d0e42dce6accc8e87de730ec4478e33` |
| `runtime_capability_prototype/contracts/authorization_registry_record_schema_v2.yaml` | `4f5241697c987fbefb4531f61e85b010332b988062ee02c83ba2052e5c1c31be` |
| `runtime_capability_prototype/contracts/authorization_registry_event_schema_v2.yaml` | `16dc8fec0ab7c1ae152781f7ec177c6679ca4a52a465254f0c98a122c8a59bea` |
| `runtime_capability_prototype/contracts/r2_portable_controller_terminal_schema_v1.yaml` | `7b2a983750a903e43489854750d56d4f6fee31a8fb541615d8247e2bf90454ac` |
| `runtime_capability_prototype/contracts/capability_claims_schema_v2.yaml` | `3f872d00524c683ff93a9a8c3e02b63cc1f40da4bec72bb1289887cc0bca06bf` |
| `runtime_capability_prototype/contracts/broker_envelope_schema_v2.yaml` | `c7b8ff11745d607b1511b4f7a11c7944896b9f2f1383e0ccbadda89f0ef91010` |
| `runtime_capability_prototype/contracts/audit_attestation_schema_v2.yaml` | `9728fa6fb64ebfbc1cb260e6986f2d1947fc340445d515e27880e419d0d16da3` |
| `runtime_capability_prototype/runtime/ctde_runtime/authorization_v2.py` | `5359cf7289e130f8a3c4228dd6d4c8b0e961ef9da716c05a78169191d571ba4d` |
| `runtime_capability_prototype/contracts/r2_portable_authorization_test_requirements.yaml` | `0c206312075dc34123fcaef0ec81475f72197618fb7003c1764d9898dee84965` |
| `runtime_capability_prototype/runtime/build_r2_portable_manifest.py` | `8f75e72d33d3c1cabf2bce866eac9fb44aec5775c68127576073ce510498828c` |
| `runtime_capability_prototype/runtime/run_r2_portable.py` | `ec1c86ed0f89a76b497dc9d48ff4fc092c5ff1e78d84fb3dff407a9040a4ca75` |

另创建唯一 fresh suite：

```text
runtime_capability_prototype/r2_portable_suites/R2PS-20260811-001/
```

suite 包含 270 个文件、9,069,099 bytes；内容树摘要为：

```text
fefbc901a85b160cf599bcd153d1227b90267258a4e5bfe4d0ab7c6c16076709
```

其文件全部位于批准的 `control/`、`artifacts/`、`registry/`、`evidence/`、`terminal/`、`aggregate/` 路径。未产生 `__pycache__` 或白名单外 Runtime 文件。

本报告 `PORTABLE_AUTHORIZATION_SCHEMA_V2_IMPLEMENTATION_RESULT.md` 是用户明确要求的阶段结果文件；为避免 self-digest，其自身摘要不写入正文，由外部交付信息报告。

## 5. Canonical Authorization Schema V2 身份

```yaml
schema_id: "urn:ctde:schema:runtime-authorization:2"
schema_version: "2.0.0"
artifact_class: "ctde_runtime_authorization"
portable_profile: "CTDE-PORTABLE-DEV-1"
hardened_profile_compatible: true
additional_properties_allowed: false
authorization_artifact_self_digest_allowed: false
legacy_alias_allowed: false
```

唯一 loader 强制：UTF-8、单文档、安全 YAML JSON-compatible 子集、string mapping key、duplicate-key/custom-tag/merge/anchor/alias/float/implicit timestamp 拒绝、closed nested objects 与 cross-field semantic validation。

## 6. Migration 行为

| 输入 | V2 行为 |
| --- | --- |
| 缺 `schema_version` | `BLOCKED_AUTHORIZATION_SCHEMA_VERSION_UNSUPPORTED` |
| `schema_version=1.x` | `BLOCKED_AUTHORIZATION_SCHEMA_VERSION_UNSUPPORTED` |
| unknown/future version | `BLOCKED_AUTHORIZATION_SCHEMA_VERSION_UNSUPPORTED` |
| 缺其他必填字段 | `BLOCKED_AUTHORIZATION_SCHEMA_INVALID` |
| legacy field alias | `BLOCKED_AUTHORIZATION_SCHEMA_INVALID` |
| artifact self-digest alias | `BLOCKED_AUTHORIZATION_SCHEMA_INVALID` |
| 缺／错误 Profile | `BLOCKED_AUTHORIZATION_PROFILE_MISMATCH` |
| caller dict 与 Registry custody bytes 不同 | `BLOCKED_AUTHORIZATION_CONTEXT_MISMATCH` |
| Registry custody BLOB/digest/size 不同 | `BLOCKED_AUTHORIZATION_REGISTRY_DIGEST_MISMATCH` |

V1 artifact、181 个旧 grants、旧 Registry rows、旧 suite 和旧 evidence 未转换、未重标、未回填、未重置状态，也不能由 V2 Runtime active path 消费。不存在“V2 失败后回退 V1”的 compatibility fallback。

## 7. Registry binding 与 one-time/replay 行为

Registration 只接受 authorization exact bytes；Registry 自行 safe-parse、validate、计算 digest/size，并在单事务中创建：

```text
authoritative bytes BLOB
  + immutable identity
  + state_version=0 / unconsumed
  + authorization_registered durable event
```

Resolver 只从 Registry custody BLOB 重建 typed view，并重新计算 digest/size；caller path、caller dict 或外部审计副本均不是 authorization authority。

成功路径为：

```text
PreConsumeAuthorizationContextV2
  -> consume CAS / PostConsumeMintContextV2
  -> mint-lease CAS / PostMintLeaseContextV2
  -> preparation CAS / PreparedCapabilityContextV2
  -> signed activation commit
  -> activation CAS / ActivatedAuthorizationContextV2
  -> pure issuer/broker/reader/audit binding probes
```

三个 one-shot handle 使用不同 domain-separated SHA-256；Registry 仅保存 digest，handle 明文不落盘且 resolver 不重发。state version 每次成功状态转换递增，旧 context 立即 stale。并发消费实际证明恰好一个 winner，loser 为 `BLOCKED_AUTHORIZATION_REPLAY`；重复 lease/preparation/activation、post-crash handle reconstruction 与 post-failure retry 均拒绝。

## 8. 实际测试数量与闭包

### 8.1 Leaf 统计

```yaml
suite_id: "R2PS-20260811-001"
manifest_sha256: "a8f712657b05eb2ea4a55719a664585c0f0754e07709f11ee2683cb130abcd76"
aggregate_sha256: "3941449585b1d7071f703c2858a3f72bbed929ef092f496ae3b30037900c4e61"

discovered: 51
executed: 51
evidence_complete: 51
passed: 51
failed: 0
skipped: 0
unknown: 0
timeout: 0
```

### 8.2 Operation 与 controller ledger 闭包

```yaml
registry_operations:
  expected: 103
  observed: 103
  terminal: 103
  evidence_complete: 103
  duplicate_ids: 0

consume_operations:
  expected: 34
  observed: 34
  terminal: 34
  evidence_complete: 34
  duplicate_ids: 0

controller_terminal_records:
  expected: 59
  observed: 59
  schema_valid: 59
  canonicalization_valid: 59
  signature_valid: 59
  chain_valid: 59
  manifest_correlated: 59
  registry_truth_verified: 59
  evidence_complete: 59
```

Controller ledger 使用 suite-wide 单一 Ed25519 test key、单一 sequence `0..58`、单一 genesis 和 exact previous-record SHA-256 chain。它是独立 A1 controller channel，不构成 A2 tamper isolation。

## 9. 核心 acceptance requirement 结果

| 核心要求 | 实际结果 |
| --- | --- |
| valid authorization accepted | PASS |
| authorization exists / unique ID | PASS |
| wrong run rejected | PASS — `BLOCKED_AUTHORIZATION_RUN_MISMATCH` |
| wrong source rejected | PASS — `BLOCKED_AUTHORIZATION_SOURCE_MISMATCH` |
| wrong source snapshot rejected | PASS — `BLOCKED_AUTHORIZATION_SOURCE_MISMATCH` |
| wrong structure map rejected | PASS — `BLOCKED_AUTHORIZATION_STRUCTURE_MAP_MISMATCH` |
| wrong task scope rejected | PASS — `BLOCKED_AUTHORIZATION_TASK_SCOPE_MISMATCH` |
| out-of-range rejected | PASS — `BLOCKED_AUTHORIZATION_RANGE_EXCEEDED` |
| unauthorized consumer rejected | PASS — `BLOCKED_AUTHORIZATION_CONSUMER_MISMATCH` |
| unauthorized output rejected | PASS — `BLOCKED_AUTHORIZATION_OUTPUT_NOT_ALLOWED` |
| denied capability rejected | PASS — `BLOCKED_AUTHORIZATION_CAPABILITY_DENIED` |
| expired / at-expiry rejected | PASS — `BLOCKED_AUTHORIZATION_EXPIRED` |
| revoked rejected | PASS — `BLOCKED_AUTHORIZATION_REVOKED` |
| first consume accepted | PASS |
| replay rejected | PASS — `BLOCKED_AUTHORIZATION_REPLAY` |
| malformed / duplicate key / self-digest rejected | PASS — `BLOCKED_AUTHORIZATION_SCHEMA_INVALID` |
| missing required field rejected | PASS — `BLOCKED_AUTHORIZATION_SCHEMA_INVALID` |
| missing / legacy / unknown version rejected | PASS — `BLOCKED_AUTHORIZATION_SCHEMA_VERSION_UNSUPPORTED` |
| external Registry digest mismatch rejected | PASS — `BLOCKED_AUTHORIZATION_REGISTRY_DIGEST_MISMATCH` |
| wrong/missing Profile rejected | PASS — `BLOCKED_AUTHORIZATION_PROFILE_MISMATCH` |
| duplicate/wrong nonce rejected | PASS |
| one-time/retry/inheritance flags enforced | PASS |
| caller claims vs bytes mismatch rejected | PASS — `BLOCKED_AUTHORIZATION_CONTEXT_MISMATCH` |
| external audit-copy mutation separated from authority | PASS |
| concurrent CAS single winner | PASS |
| consume/lease/preparation crash-stranding | PASS |
| mint-lease/preparation/activation replay | PASS |
| three signed-writer failure windows fail closed | PASS |
| complete logical audit/controller terminal evidence | PASS |

Manifest 总计覆盖 33 个 mandatory requirement category；没有通过减少 manifest leaf 制造 PASS。

## 10. A1 evidence 范围与明确限制

本结果可以声明：

- V2 artifact、external Registry identity、state/events 与 typed context 在 Runtime 逻辑内闭合；
- identity、Profile、run、source/snapshot/map/scope/range/consumer/output/deny policy 被 logical Gate 强制；
- one-time CAS、nonce、expiry、revocation、replay 和 capability activation path 按合同运行；
- accept/reject operation 的 signed Runtime A1 event 与独立 controller terminal ledger 完整。

本结果不能声明：

- 完整实际 OS file-open set 已被观察；
- denied capability 在 OS 层不存在或不可旁路；
- English／Greek／Candidate／model／business action 的 0 是 A2 OS-verified count；
- A2、A3、Hardened、Certified 或 secure sandbox certification。

```yaml
assurance_profile_id: "CTDE-PORTABLE-DEV-1"
highest_claimed_evidence_level: "A1"
a2_os_file_access_proof: "NOT_PROVIDED"
a2_verified_access_counts: null
hardened: false
certified: false
portable_to_hardened_promotion_allowed: false
```

## 11. 边界终检

以下为 R2 controller A1 action ledger；不是 A2 OS-verified counts：

```yaml
english_tei_access_count: 0
greek_tei_access_count: 0
candidate_run_count: 0
model_call_count: 0
business_output_count: 0
r3_execution_count: 0
r4_execution_count: 0
broker_open_calls: 0
broker_read_calls: 0
bounded_deliveries: 0
consumer_invocations: 0
r2_scope_violation_count: 0
story_structure_yaml_created: false
```

边界依据：runner 仅物化 synthetic authorization/control/evidence/SQLite artifacts；纯 broker/reader/audit probe 不调用 source catalog、`open`、`pread`、FD delivery、sandbox、parser、model gateway或publisher。白名单外 Runtime 树重建摘要与执行前精确一致。

## 12. Deferred 项

| 项目 | 当前处置 |
| --- | --- |
| Runtime transitive dependency/component freeze closure | `deferred_to_R3` |
| Portable synthetic source-range E2E、broker open/read、bounded delivery | `deferred_to_R4` |
| OS observability、ptrace/strace/fanotify、完整 file-access observation | `hardened_only` |
| A2/A3 correlation、Hardened certification | `hardened_only` |
| Candidate runtime 与文学分析 | `blocked / not_authorized` |

R2 未修改 `component_manifest.yaml`、`build_manifest.py`、旧 `run_suite.py`、formal loader、fixture/source layer、sandbox/native probe或旧 suites。

## 13. 历史与当前状态保持

```yaml
phase_2g: "BLOCKED_RUNTIME_CAPABILITY_PROTOTYPE_FAILED"
phase_2g_r1: "BLOCKED_OS_OBSERVABILITY_INSUFFICIENT"
phase_2g_r1d: "ADOPT_DUAL_ASSURANCE_PROFILES"
phase_2g_r2p: "PASS_PORTABLE_R2_PLAN_ONLY"
phase_2g_r2: "PASS_PORTABLE_AUTHORIZATION_SCHEMA_V2_IMPLEMENTED"

historical_allow_r2_false_changed: false
old_suite_status_changed: false
run_001_status_changed: false
run_002_status_changed: false
candidate_analysis: "BLOCKED"
automatic_entry_to_r3: false
```

R2 PASS 只代表 Portable Authorization Schema V2 这一项原子修复完成。执行在本阶段停止；未自动进入 R3。
