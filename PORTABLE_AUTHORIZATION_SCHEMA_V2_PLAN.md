# Classic-to-Drama Engine：Portable Authorization Schema V2 Implementation Plan

> 项目：Classic-to-Drama Engine  
> 阶段：Phase 2-G-R2P  
> 文档类型：Portable Authorization Schema V2 Implementation Plan  
> 日期：2026-08-11  
> 最终状态：`PASS_PORTABLE_R2_PLAN_ONLY`  
> 当前效力：`planning_only / not_implemented / not_tested / not_authorized`  
> 目标 Profile：`CTDE-PORTABLE-DEV-1`  
> 最低证据等级：`A1 runtime logical proof`  
> 认证状态：`non-certified`  
> Candidate Analysis：`CURRENTLY_BLOCKED`

## 0. 结论、依据与阶段边界

### 0.1 计划结论

本计划将原 Repair Plan 的 R2 重新定义为 **Portable / Development Profile 下的 Authorization Schema V2 实施工作包**。R2-P 的目标是关闭 authorization artifact、外部 registry identity、一次性消费状态和下游 consumer binding 之间的确定性合同缺口，并以 A1 runtime logical evidence 证明其行为。

本计划不降低或重新解释 A1、A2、A3：

- Portable R2-P 最低并最高只声明 A1；
- R2-P 不提供 A2 OS-level file-access proof；
- R2-P 不形成 A3，不产生 hardened／certified 标记；
- 同一 Schema V2 的业务授权语义可由未来 Hardened Profile 复用，但 Hardened 必须重新物化 Profile-bound authorization、registry record 和运行证据；
- Portable R2-P PASS 永远不能升级、补证或解释为 Hardened R2-H PASS。

```yaml
phase: "Phase 2-G-R2P"
final_status: "PASS_PORTABLE_R2_PLAN_ONLY"
portable_r2_replanned: true
r2_implemented: false
r2_tested: false
r2_execution_authorized_by_this_plan: false
candidate_analysis_currently_blocked: true
```

### 0.2 正式依据

| 依据文件 | 本阶段读取时 SHA-256 | 用途 |
| --- | --- | --- |
| `RUNTIME_CAPABILITY_PROTOTYPE_RESULT.md` | `6811bcc4ef0efcaee89013648dd0bb06bbaca154625f3dc47bdfa0f295851753` | Phase 2-G 的冻结 blocker、旧 suite 结果与局部 authorization 行为证据 |
| `RUNTIME_CAPABILITY_REPAIR_PLAN.md` | `a2c52dbaecf3956cf4a2189abe5401f269d255e8099d3345985619be25be4213` | 原 R2 self-digest 修复、external registry binding 与 A0–A3 定义 |
| `RUNTIME_OS_OBSERVABILITY_PREFLIGHT_RESULT.md` | `0ca51394315199683cd790e01d160addb80f1cb0e32bb23df212045b49c433c0` | 当前环境 qualification-wide 最高 A1、R1 历史 BLOCKED 事实 |
| `RUNTIME_ASSURANCE_PROFILE_DECISION.md` | `57471c85c57946f6ceb6da288301cc802533b09c137bfbe8e6e247dad57206e2` | 双 Profile 决策、Portable R2 可重新规划但尚未授权执行 |
| `CANDIDATE_EXECUTION_CONTRACT_REPAIR.md` | `12ceb01cab4901cb2b7472b1b56f93750a43cb8c28b5f0c9ab89acf3ad4fe7bd` | run/source/scope/output binding、一次性 authorization 与 external digest 语义 |

为准确区分已确认缺陷与计划性增强，本阶段还对现有 Prototype 的下列 authorization 相关文件做了只读核对；未执行或修改它们：

| 只读实现证据 | SHA-256 |
| --- | --- |
| `runtime_capability_prototype/contracts/authorization_schema.yaml` | `f6f2940a41867c5471a1a81751112dd7c090b7e56d8ba428664140ffd0420da6` |
| `runtime_capability_prototype/runtime/ctde_runtime/authorization_registry.py` | `26dc60926826db207cace0e871d15b587032d4cb3e861c111415d0819707ea82` |
| `runtime_capability_prototype/runtime/run_suite.py` | `caf32bdb9c49ba78ee1671d41b62bc9eb8297343624ceb7afd562443a6794749` |
| `runtime_capability_prototype/runtime/ctde_runtime/range_broker.py` | `19aaaef83c92d871467a5e463581cc574b6b419f85a9a6ac9086f27868f76b26` |
| `runtime_capability_prototype/runtime/ctde_runtime/bounded_reader.py` | `c49bd965a40e52120207192fe082dc9737b565253dd4cfe62fc200a1a9cf1a99` |
| `runtime_capability_prototype/runtime/ctde_runtime/read_audit.py` | `735d25ff6ff41c6b77538daf1d27550d76211c20098a99a4246b5c91eb662b8b` |
| `runtime_capability_prototype/runtime/ctde_runtime/events.py` | `84d05a5c49bdf7e66f9cd68a3941e18b2577420479acf5389c69f1e6852322ac` |

只读核对时 Prototype 全文件内容树摘要为：

```text
4acda62cdc02fe4e72e095f56ad895f5afbcbeba9ad32d9699c7eb78c90b7072
```

### 0.3 本阶段唯一产物与禁止项

本阶段只创建：

```text
PORTABLE_AUTHORIZATION_SCHEMA_V2_PLAN.md
```

本阶段不会：

- 创建 `authorization_schema_v2.yaml`、registry record schema 或任何 Schema V2 实体；
- 修改 `runtime_capability_prototype/` 中任何文件、数据库、suite、case 或 evidence；
- 执行 Runtime、validator、manifest builder、runner 或测试；
- 执行 R2、R3、R4-P、R1-H 或 R4-H；
- 创建、授权或执行 Candidate Run；
- 打开、扫描、解析、stat、hash、复制或处理 Odyssey English TEI；
- 打开、扫描、解析、stat、hash、复制、挂载或处理 Greek TEI；
- 创建 `story_structure.yaml` 或人物、事件、主题、母题、文学分析、改编、分集、场景、对白、剧本数据；
- 改写 Phase 2-G、R1、旧 `allow_r2=false`、旧 suite 或 Run 002 的历史状态。

## 1. 现有 Authorization Schema 问题基线

### 1.1 判定分类规则

本文严格区分：

- `confirmed_defect`：已经由 Phase 2-G 正式结果或本阶段对冻结代码的直接只读核对确认；
- `confirmed_working_baseline`：现有 Prototype 已有真实行为证据，未来 V2 必须保留并重新验证；
- `planned_improvement`：为形成统一 V2、双 Profile 和 Candidate-compatible 语义而新增，不能伪称为旧 suite 已证明的缺陷；
- `out_of_scope_for_r2`：属于 R3 closure、R4 E2E 或 Hardened A2/A3，不得混入 R2。

### 1.2 基线总表

| Baseline ID | 分类 | 当前事实 | R2-P 决定 |
| --- | --- | --- | --- |
| `R2P-BL-001` | `confirmed_defect` | 正式 blocker `AUTHORIZATION_SCHEMA_ARTIFACT_MISMATCH`：V1 schema 要求 artifact 内含 `authorization_file_sha256`，181 个持久 artifact 的 exact bytes 不含该字段 | Breaking V2；artifact 内明确禁止任何 self-digest 字段或别名 |
| `R2P-BL-002` | `confirmed_defect` | Runner 先序列化无摘要 bytes，再计算 SHA-256，只向内存 dict 注入摘要；落盘 bytes 仍无摘要 | exact bytes digest 只进入外部 registry identity；不得注入 claims dict |
| `R2P-BL-003` | `confirmed_defect` | Prototype 没有实际加载 `authorization_schema.yaml` 或调用 JSON Schema／等价 validator | registration 前强制执行 safe parse + V2 schema + semantic validation |
| `R2P-BL-004` | `confirmed_defect` | Registry 同时信任调用方 dict 与 immutable bytes；不会从 bytes 解析并证明 dict claims 与 artifact 一致 | Registry 只接受 exact bytes，经唯一 loader 产生 canonical validated context |
| `R2P-BL-005` | `confirmed_defect` | Issuer、broker、reader、audit 使用注入外部 digest 的增强内存 dict；持久 artifact、schema、registry 与 consumer 没有共同 canonical view | 下游只接收 `(validated claims, external registry identity, registry state)` 的不可混淆只读 context |
| `R2P-BL-006` | `planned_improvement`（基于已确认的命名分裂事实） | `attempt_id/run_id`、`fixture_object_id/source_id/source_snapshot_id`、`allowed_range/allowed_ranges`、`forbidden_source_roles/denied_capabilities`、`initial_state/state` 命名分裂 | V2 选择唯一名称；旧名称不作为 alias 接受 |
| `R2P-BL-007` | `confirmed_working_baseline` | Missing／invalid／expired／replay、并发双 CAS 单赢家、CAS 后崩溃保持 spent 已有局部真实证据 | 作为 regression expectation；必须在 V2 新 manifest 中 fresh execution，旧 PASS 不可复用 |
| `R2P-BL-008` | `confirmed_working_baseline` | Registry 已把 immutable digest 与 mutable state 分列，并有 authorization/capability/delivery one-shot 状态 | 保留原则，修正 canonical identity 与精确状态码 |
| `R2P-BL-009` | `planned_improvement` | V1 artifact 无 `schema_version`、Profile、`run_id`、source snapshot、task scope、consumer/output、issued time、authorization nonce | 增加为 V2 必填字段；不得写成旧 suite 已验证缺陷 |
| `R2P-BL-010` | `planned_improvement` | DB enum 有 `revoked`，但无显式 revoke API；所有非 `unconsumed` 消费失败均可能落为 SPENT 码 | 增加单向 revoke transition 与精确 `REVOKED` 拒绝码 |
| `R2P-BL-011` | `planned_improvement` | authorization-level nonce 不存在；capability nonce 不等于 authorization nonce | 新增 registry-unique authorization nonce；capability/delivery nonce 生命周期保持独立 |
| `R2P-BL-012` | `out_of_scope_for_r2` | 完整 file-open set、OS 旁路、PID attribution、event-loss、evidence tamper isolation 未证明 | 保持 A2/A3 未提供；转入 deferred Hardened work，不在 R2 伪造修复 |

### 1.3 Self-digest 与 schema mismatch 的精确机制

现有 V1 实现顺序为：

```text
build payload without digest
  -> serialize exact artifact bytes
  -> SHA-256(exact bytes)
  -> add authorization_file_sha256 to in-memory dict only
  -> persist the original bytes without that field
```

而 V1 schema 把 `authorization_file_sha256` 列为 required property。由此产生三个同时成立但互不一致的对象：

1. 持久 artifact：没有该字段；
2. schema 所描述的 artifact：必须有该字段；
3. Runtime consumer 使用的内存 dict：有该字段，但它不是持久 artifact 的 parsed representation。

V2 不尝试求解自递归摘要，也不回填旧 artifact。唯一正确语义是：**authorization artifact 不保存自己的文件摘要；完整文件摘要由外部 registry identity 保存并向下游引用。**

### 1.4 Registry 与 consumer 理解不一致

现有 Registry 的 `register(authorization, immutable_bytes)` 接口允许调用者同时传入 claims dict 和 bytes。Registry 比较 bytes digest 与 dict 中被注入的摘要，但没有：

- 从 exact bytes 自行 safe parse；
- 实际执行 schema validation；
- 证明 dict 的 run/source/range/expiry/deny claims 等于 exact bytes 中的 claims；
- 把完整 canonical claims 绑定为 registry-resolved immutable view。

Capability issuer 从调用方 dict 读取 source/range/hash；range broker、bounded reader 和 read audit 也把调用方 dict 当作 correlation authority。正向 runner 因复用同一个内存对象而能保持内部一致，但这不证明各组件理解的是 exact artifact bytes 中的同一授权对象。

V2 必须删除这种双输入信任：Registry 注册接口接收 exact artifact bytes；唯一 V2 loader 负责 parse／validate；下游只能获得 registry-resolved context 或 opaque registry reference，不能传入任意 claims dict。

### 1.5 字段命名不一致：事实与处理

| 语义 | V1 Prototype | Candidate repair draft／audit | V2 唯一名称 | 分类 |
| --- | --- | --- | --- | --- |
| 授权执行身份 | `attempt_id` | `run_id` | `run_id` | planned unification |
| artifact 摘要 | artifact schema 的 `authorization_file_sha256`；registry 的 `authorization_digest`／`immutable_bytes_sha256` | `authorization_file_sha256` 外置语义 | registry-only `authorization_artifact_sha256` | confirmed mismatch + planned rename |
| source identity | `fixture_object_id` | `source_id`、`source_object_id`、`source_snapshot_id` | `source_id` + `source_snapshot_id` + digest | planned unification |
| structure identity | `fixture_structure_contract_id` | `structure_map_id`／`map_id` | `structure_map_id` + digests | planned unification |
| ranges | artifact `allowed_range`；audit `allowed_ranges` | `allowed_byte_ranges` | `allowed_ranges` | planned unification |
| deny policy | `forbidden_source_roles` | `forbidden_inputs` | `denied_capabilities` | planned unification |
|批准状态 | `initial_state` | `authorization.status` | immutable `authorization_state` | planned separation |
|消费状态 | registry `state` | `registry_observed_state` | registry-only `consumption_state` | planned separation |
| 时间 | integer `expires_at`，无 `issued_at` | ISO-8601 strings | quoted RFC 3339 UTC strings | planned unification |

Candidate repair 中的 schema 代码块明确是不可执行 draft 示例，不是已实施的第二套 schema。因此命名差异本身多属于 V2 统一工作，不应伪造成 Phase 2-G 已单独裁定的 blocker。

### 1.6 One-time authorization／anti-replay 基线

#### 必须保留并重新验证的已有行为

- SQLite `BEGIN IMMEDIATE` 与 `unconsumed -> spent` CAS；
- authorization ID、attempt ID 与 digest 的唯一约束；
- concurrent dual CAS 恰好一个 winner；
- CAS commit 后 issuer 崩溃，authorization 仍保持 spent；
- mint lease 只能 claim 一次；
- capability 与 delivery 分别只能消费一次；
- replay 不得把 terminal state 回退到 unconsumed；
- 自动重试不产生新的 authority。

#### V2 需要新增或精化的行为

- artifact 中 `one_time=true` 必须由实际 V2 validator 强制，而非只靠代码惯例；
- authorization-level `nonce` 必须在 Registry 全局唯一，并绑定 authorization ID、run ID、Profile 与 artifact digest；
- `authorization_id`、`run_id`、nonce 与 artifact digest 的重复／冲突必须在注册或 CAS 前 fail closed；
- `expires_at == now` 明确定义为 expired，即使用 `now >= expires_at` 拒绝；
- `revoked`、`expired`、`spent` 使用互斥精确 blocker；
- `unconsumed -> spent | revoked | expired` 为单向 terminal state machine；
- authorization、capability、delivery 的 nonce／one-shot 状态彼此独立，不得用一个 nonce 代替三层 replay protection；
- DB commit 后 signed event 生成失败时，state 不回退，capability 不 mint，attempt 以 BLOCKED terminal audit 收口。

## 2. Authorization Schema V2 唯一 Canonical Contract

### 2.1 对象模型

V2 将 authorization 相关数据分成五类不可混淆对象；其中 validated context 是按状态阶段区分的 typed context family：

| 对象 | 权威内容 | 可变性 | 是否包含 artifact 自身 SHA-256 |
| --- | --- | --- | --- |
| `authorization_artifact_v2` | immutable business authorization claims | 完成后不可变 | 否，且任何 self-digest alias 均拒绝 |
| `authorization_registry_identity_v2` | authoritative exact bytes BLOB、bytes identity、schema/Profile/run/source binding | append-only／不可变 | 是 |
| `authorization_registry_state_v2` | consumption state与mint/activation substate、event、revocation／expiry | 两个维度均单向可变 | 通过 registry identity 引用 |
| `authorization_registry_event_v2` | registration／consume／mint-lease／capability-activation／revoke／expire／reject 的 durable transition facts | append-only／不可变 | 引用 registry identity 的 external digest |
| `authorization_context_family_v2` | claims + registry identity + **特定 state version** 的只读组合 | 每次 state transition 产生下一阶段 context；旧 context 立即 stale | 只在 identity 子对象中可见 |

不存在第六种“向 parsed artifact dict 注入外部摘要”的对象。

### 2.2 顶层字段合同

下表是未来 V2 实体 schema 的规范性字段计划；本阶段没有创建该实体文件。Canonical JSON Schema `$id` 冻结为：

```text
urn:ctde:schema:runtime-authorization:2
```

Portable 与 Hardened 必须引用该同一 `$id` 和 `schema_version=2.0.0`，不得各自另命名一份“V2”。

除另有const/enum说明外，artifact内所有以`_id`结尾的标识字段使用同一lexical type：1–128个ASCII字符，正则 `^[A-Za-z0-9][A-Za-z0-9._:/-]{0,127}$`，case-sensitive，禁止空白、反斜杠、percent-decoding别名或Unicode同形字符。ID只按exact string equality比较；不同ID类别不得因字节相同而互换语义。

| 字段 | 类型 | 必填 | 唯一语义与约束 |
| --- | --- | --- | --- |
| `schema_version` | string | 是 | 常量 `2.0.0`；缺失、`1.x`、未知版本均在 registration 前拒绝 |
| `artifact_class` | string | 是 | 常量 `ctde_runtime_authorization` |
| `assurance_profile_id` | enum string | 是 | Schema V2 精确 enum：`CTDE-PORTABLE-DEV-1`、`CTDE-HARDENED-CERT-1`；R2-P manifest 额外要求常量 Portable；不得跨 Profile 复用 artifact |
| `authorization_id` | string | 是 | 全局唯一、不可复用；与 exact artifact identity 一一绑定 |
| `run_id` | string | 是 | 唯一被授权执行身份；Prototype runner 的内部 `attempt_id` 只能与其 1:1 映射，不能作为第二个 artifact alias |
| `source_id` | string | 是 | 逻辑 source/version identity；不能替代 snapshot 或 content identity |
| `source_snapshot_id` | string | 是 | 冻结 source snapshot identity |
| `source_snapshot_sha256` | string，64 位小写 hex | 是 | `source_snapshot_id` 所指 immutable snapshot artifact 的 **exact file bytes** SHA-256；不允许 canonical block／重序列化 digest |
| `structure_map_id` | string | 是 | 与本 run 绑定的 structure map／synthetic structure contract identity |
| `structure_map_file_sha256` | string，64 位小写 hex | 是 | 绑定完整 map artifact bytes |
| `mapping_payload_canonicalization_id` | string | 是 | 常量 `CTDE-MAP-C14N-1`；冻结 payload digest 的输入域与序列化规则 |
| `mapping_payload_sha256` | string，64 位小写 hex | 是 | 对 `CTDE-MAP-C14N-1` canonical mapping payload计算的 SHA-256；与完整文件 digest 不可互换 |
| `task_scope` | closed object | 是 | 见 §2.3；以 ID + task type + digest 唯一绑定任务语义 |
| `allowed_ranges` | array of closed objects | 是 | 见 §2.4；V2 当前恰好一个 range，排序、非空、非重叠；不得接受 caller override |
| `allowed_consumer` | closed object | 是 | 见 §2.5；绑定唯一 logical consumer／component identity |
| `allowed_outputs` | array of closed objects | 是 | 见 §2.6；可以为空；只能列精确 relative path 与 artifact class |
| `denied_capability_policy_version` | string | 是 | 常量 `CTDE-DENIED-CAPABILITIES-1`，冻结 deny vocabulary 与 exact set |
| `denied_capabilities` | exact ordered string array | 是 | 见 §2.7；Schema 使用 exact const set；表达 Runtime logical deny contract，不是 OS-level absence claim |
| `issuer` | closed object | 是 | 见 §2.8；绑定 authority 与 immutable approval evidence |
| `issued_at` | quoted RFC 3339 UTC string | 是 | 以 `Z` 结尾；不得由 YAML parser 转为 timestamp object |
| `expires_at` | quoted RFC 3339 UTC string | 是 | 必须严格晚于 `issued_at`；`now >= expires_at` 即拒绝 |
| `nonce` | string，64 位小写 hex | 是 | 32-byte authorization-level nonce；Registry 全局唯一 |
| `one_time` | boolean | 是 | 常量 `true` |
| `automatic_retry_allowed` | boolean | 是 | 常量 `false` |
| `authorization_inheritable` | boolean | 是 | 常量 `false` |
| `authorization_state` | string | 是 | 可执行 V2 artifact 常量 `approved`；只表达不可变批准决定，不表达消费状态 |

Schema 顶层采用 `additionalProperties: false`。下列 legacy／self-digest 字段即使值正确也必须拒绝：

```text
authorization_file_sha256
authorization_artifact_sha256
self_digest
file_digest
attempt_id
fixture_object_id
fixture_structure_contract_id
allowed_range
forbidden_source_roles
initial_state
```

其中 `authorization_artifact_sha256` 只允许出现在外部 registry identity、capability、envelope、audit event 或 result 中，禁止出现在 authorization artifact 本体。

### 2.3 `task_scope`

| 子字段 | 类型 | 必填 | 语义 |
| --- | --- | --- | --- |
| `task_scope_id` | string | 是 | 稳定 scope identity |
| `task_type` | string | 是 | 冻结的任务类型；不得由 consumer 改写 |
| `task_scope_sha256` | 64 位小写 hex | 是 | `task_scope_id` 所指 immutable task-scope artifact 的 **exact file bytes** SHA-256；不接受 canonical block alias |
| `selected_source_units` | non-empty unique string array | 是 | 逻辑 source unit allowlist；必须与 structure map 和 ranges 一致 |
| `max_invocations` | non-negative integer | 是 | 本 task 允许的 logical invocation 上限；R2 synthetic validation 可为 0 |
| `automatic_retries` | integer | 是 | 常量 0 |

`task_scope` 使用 `additionalProperties: false`。其 digest 是外部 task scope 的身份，不是本 authorization artifact 的摘要。

### 2.4 `allowed_ranges`

V2 字段使用复数，但当前 Profile 合同为 `minItems=1`、`maxItems=1`。每项为：

| 子字段 | 类型 | 必填 | 语义 |
| --- | --- | --- | --- |
| `range_id` | string | 是 | 本 authorization 内唯一 range identity |
| `start_byte` | non-negative integer | 是 | inclusive start |
| `end_byte_exclusive` | positive integer | 是 | 必须大于 start |
| `expected_length` | positive integer | 是 | 必须等于 `end_byte_exclusive - start_byte` |
| `expected_slice_sha256` | 64 位小写 hex | 是 | 对该 snapshot/range 的预期 slice digest |

如果未来确需多 range 组合，必须发布新的 schema／policy revision并定义组合语义；R2-P 不以 `allowed_ranges` 的复数拼写静默扩大当前单一 exact-range authority。

### 2.5 `allowed_consumer`

| 子字段 | 类型 | 必填 | 语义 |
| --- | --- | --- | --- |
| `consumer_id` | string | 是 | logical consumer identity |
| `consumer_role` | string | 是 | 冻结 role，例如 bounded analysis consumer；不能由 caller 声明 |
| `component_id` | string | 是 | 实际实现组件 ID |
| `component_version` | string | 是 | 版本或 immutable revision |
| `component_identity_artifact_sha256` | 64 位小写 hex | 是 | `component_id/version` 所指 immutable component identity artifact 的 **exact file bytes** SHA-256；不是 R3 closure digest |

该对象不是 JWS `aud` 的别名。Capability、envelope 的 audience 仍由各自 signed-object schema 验证；所有层必须最终关联到同一 Profile/run/authorization identity。

### 2.6 `allowed_outputs`

每项为：

| 子字段 | 类型 | 必填 | 语义 |
| --- | --- | --- | --- |
| `artifact_class` | string | 是 | 精确 output class |
| `relative_path` | canonical POSIX relative path string | 是 | Unicode NFC；分隔符只允许 `/`；禁止 leading/trailing slash、反斜杠、NUL、空段、`.`、`..`、glob与首尾空白；Runtime另拒绝symlink ambiguity |
| `writer_component_id` | string | 是 | 唯一获准 publisher/writer |
| `max_count` | positive integer | 是 | 对该 class/path 的最大数量 |

R2-P 的 synthetic validator tests 不创建业务输出，因此其 authorization 使用空数组。空数组不等于“OS 已证明没有写入”；它只表示 Runtime logical contract 不授权任何输出。

### 2.7 `denied_capabilities`

数组值使用版本化、精确枚举，不接受自由文本或 wildcard。`denied_capability_policy_version=CTDE-DENIED-CAPABILITIES-1` 时，Schema 把下列按既定顺序排列的数组作为 exact const：不得缺项、增项、重复或重排。

```text
direct_source_open
raw_path_disclosure
caller_supplied_range_override
unbounded_read
read_to_eof
automatic_retry
second_source
network_source_fetch
unapproved_output_write
authorization_inheritance
authorization_replay
profile_promotion
```

这些值表示 Registry／issuer／broker／reader／publisher 的逻辑接口必须拒绝相应请求。Portable 报告不得把它们写成“对应 OS capability 不存在”或“旁路在 OS 层不可达”。若未来需要扩充 vocabulary 或 exact set，必须发布新的 deny-policy／schema revision；不能只在 artifact 中临时多写一个字符串。

### 2.8 `issuer`

| 子字段 | 类型 | 必填 | 语义 |
| --- | --- | --- | --- |
| `authority_id` | string | 是 | control-plane authority／approved mechanism identity |
| `approval_evidence_ref` | string | 是 | immutable evidence reference；不能是可写临时路径 |
| `approval_evidence_sha256` | 64 位小写 hex | 是 | approval evidence exact bytes digest |

R2-P synthetic tests使用 test-only authority。Candidate authorization、production authority 或 production key identity不得进入 R2-P fixture。

### 2.9 Artifact parsing 与 encoding

V2 artifact 格式必须是：

- YAML 1.2 Core Schema 的单文档、safe-mode、JSON-compatible 子集；
- duplicate keys、custom tags、merge keys、anchors、aliases、binary、float、隐式 timestamp 与实现特有类型全部拒绝；
- mapping keys 必须为 Unicode string；value 只允许 null、boolean、base-10 integer、quoted Unicode string、ordered array 或 mapping；
- 所有 schema object 均 `additionalProperties: false`；
- artifact identity 始终是 exact file bytes SHA-256，不是 parse 后重序列化 digest；
- 如另有 canonical block digest，必须使用不同字段名和 domain，并且不能替代 exact artifact digest。

## 3. 摘要职责分离与 Registry Binding

### 3.1 不可变规则

Authorization artifact 不保存：

- 自己的完整文件 SHA-256；
- 自己的 size；
- registry row ID；
- current consumption state；
- consumption event ID；
- capability ID 或 delivery ID；
- A2/A3 evidence、OS counts 或 certification result。

这些值在 artifact 完成后才产生，写回 artifact 会改变 exact bytes 并破坏 identity。

### 3.2 External registry identity record

未来 `authorization_registry_identity_v2` 至少包含：

| 字段 | 可变性 | 约束 |
| --- | --- | --- |
| `registry_record_id` | immutable | 唯一外部记录 ID |
| `authorization_id` | immutable／unique | 等于 validated artifact claim |
| `schema_id` | immutable | 常量 `urn:ctde:schema:runtime-authorization:2` |
| `schema_version` | immutable | `2.0.0` |
| `assurance_profile_id` | immutable | 等于 artifact；R2-P 为 Portable |
| `run_id` | immutable／unique | 等于 artifact；一个 active authorization 对应一个 run |
| `source_id` | immutable | 等于 artifact |
| `source_snapshot_id` | immutable | 等于 artifact |
| `structure_map_id` | immutable | 等于 artifact |
| `nonce` | immutable／unique | 等于 artifact authorization nonce |
| `authorization_artifact_bytes` | immutable BLOB | Registry custody 下的 authoritative exact artifact bytes；resolver 不得向 caller 重新索取 bytes／dict |
| `authorization_artifact_sha256` | immutable／unique | exact frozen bytes SHA-256 |
| `authorization_artifact_size_bytes` | immutable | exact frozen byte length |
| `registered_at` | immutable | Registry authoritative time |

Mutable state 必须位于独立 `authorization_registry_state_v2`：

| 字段 | 语义 |
| --- | --- |
| `registry_record_id` | 引用 immutable identity |
| `consumption_state` | `unconsumed | spent | revoked | expired` |
| `state_version` | CAS 单调版本 |
| `consumption_event_id` | 仅 spent 后存在；引用 append-only Registry event |
| `last_state_event_id` | 最近一次 accepted state transition event；所有 terminal state 均可关联 |
| `state_changed_at` | Registry authoritative time |
| `terminal_reason` | 精确 closed reason；不包含自由文本 authority expansion |
| `mint_eligibility_state` | `unavailable | available | claimed | aborted`；consume CAS产生一次性eligibility，失败路径burn为aborted |
| `mint_eligibility_handle_sha256` | unconsumed时null；consume CAS后为unique、non-null opaque handle digest；Registry不得保存或返回明文handle |
| `mint_eligibility_event_id` | unconsumed时null；spent event或后续eligibility abort event的引用 |
| `mint_claimed` | one-shot mint state |
| `mint_claim_event_id` | 仅 `mint_claimed=true` 后存在；引用 append-only mint-lease event |
| `capability_preparation_state` | `not_claimed | unprepared | prepared | aborted`；单向substate |
| `preparation_handle_sha256` | mint-lease CAS后non-null/unique；绑定attempt-local opaque preparation handle，明文不落盘 |
| `pending_capability_id` | mint-lease CAS时绑定的全局唯一test/runtime capability ID；未claim时null |
| `pending_capability_artifact_sha256` | preparation CAS后non-null；Registry custody pending capability exact bytes digest |
| `capability_preparation_event_id` | prepared/aborted后引用append-only preparation event |
| `capability_activation_state` | `not_ready | eligible | activated | aborted`；单向substate |
| `activation_handle_sha256` | preparation CAS后non-null/unique；绑定attempt-local opaque activation handle，明文不落盘 |
| `active_capability_id` | 仅activated后存在且全局唯一；必须等于已绑定的pending ID |
| `capability_activation_event_id` | activated或aborted后引用相应append-only Registry event |
| `activation_commit_a1_event_sha256` | 仅activated后存在；绑定CAS前已持久化并验证的signed A1 commit record exact bytes digest |

Identity 与 state 可以位于同一数据库的不同表，也可以采用语义等价隔离；不得把 mutable state 写回 authorization artifact。Registry 保存的 exact bytes BLOB 是 resolve 的唯一 authoritative byte source；外部文件只可作为注册输入或审计副本，consumer 不得从 caller path／dict 重建 authorization view。

所有opaque one-shot handles固定为CSPRNG生成的32-byte secret。Registry只存domain-separated digest，并使用constant-time comparison验证：

```text
mint eligibility:
  SHA-256(ASCII("CTDE-R2P-MINT-ELIGIBILITY-V1") || 0x00 || handle_bytes)
capability preparation:
  SHA-256(ASCII("CTDE-R2P-CAPABILITY-PREPARATION-V1") || 0x00 || handle_bytes)
capability activation:
  SHA-256(ASCII("CTDE-R2P-CAPABILITY-ACTIVATION-V1") || 0x00 || handle_bytes)
```

Handle明文不得落盘、进入event/audit/log、被复制/序列化或通过resolver返回；各domain的handle/digest不可互换。它们不是authorization artifact字段、nonce别名或A2 evidence。

`authorization_registry_event_v2` 是独立的 append-only durable object，至少包含：

| 字段 | 语义 |
| --- | --- |
| `registry_event_id` | 全局唯一 event ID |
| `event_type` | `authorization_registered | authorization_spent | authorization_mint_eligibility_aborted | authorization_mint_lease_claimed | authorization_mint_lease_claim_rejected | authorization_capability_prepared | authorization_capability_preparation_rejected | authorization_capability_preparation_aborted | authorization_capability_activated | authorization_capability_activation_rejected | authorization_capability_activation_aborted | authorization_revoked | authorization_expired | authorization_request_rejected` |
| `registry_record_id` | identity reference；pre-registration rejection 可为明确 absent |
| `authorization_id`、`run_id`、`assurance_profile_id`、`nonce` | 与 validated identity绑定；无法 parse 时使用显式 unavailable，而非猜测 |
| `authorization_artifact_sha256` | external exact-bytes digest或显式 unavailable |
| `registry_operation_id` | 每次 registration／consume／revoke／expire／eligibility-abort／mint-lease／preparation／activation／reject operation 的全局唯一关联 ID |
| `consume_operation_id` | required nullable consume-suboperation ID；spent/replay/concurrency及由同一consume触发的eligibility/mint/preparation/activation事件必须非null并保持同一值；独立registration/revoke/expire操作为null；不能替代通用`registry_operation_id` |
| `from_consumption_state`、`to_consumption_state` | consumption axis；无变化时相同，pre-registration为null |
| `from_mint_eligibility_state`、`to_mint_eligibility_state` | eligibility axis；不适用时null |
| `from_capability_activation_state`、`to_capability_activation_state` | activation axis；不适用时null |
| `from_capability_preparation_state`、`to_capability_preparation_state` | preparation axis；不适用时null |
| `mint_eligibility_handle_sha256`、`preparation_handle_sha256`、`activation_handle_sha256` | 仅相关事件包含domain-separated opaque handle digest；永不包含明文 |
| `mint_claim_event_id`、`pending_capability_id`、`active_capability_id` | 相关mint/activation事件的精确绑定；不适用时null |
| `pending_capability_artifact_sha256`、`capability_preparation_event_id` | 相关preparation/activation事件的精确绑定；不适用时null |
| `activation_commit_a1_event_sha256` | activation accepted event必须非null；其他event按schema为null |
| `expected_state_version`、`result_state_version` | CAS 前后版本 |
| `cas_outcome` | `accepted | rejected | not_applicable` |
| `blocker` | accepted 时 null；rejected 时精确 code |
| `authoritative_at` | Registry authoritative timestamp |

事务不变量：

1. identity row + authoritative bytes BLOB + initial `consumption_state=unconsumed`、`mint_eligibility_state=unavailable`、`mint_claimed=false`、`capability_preparation_state=not_claimed`、`capability_activation_state=not_ready` + `authorization_registered` event 必须在**同一数据库事务**中 all-or-nothing 创建；
2. accepted consume CAS + state version + fresh opaque mint-eligibility handle hash + `available` eligibility + durable spent event 必须在**同一数据库事务**中 commit；handle明文只能作为CAS返回值进入该attempt的`PostConsumeMintContextV2`，Registry resolver不得重建或再次返回；
3. rejected consume/revoke/expire request 若已有 registry identity，其 durable rejection event与“不改变 state/version”的结果在同一事务记录；
4. mint lease 必须以 `consumption_state=spent AND mint_eligibility_state=available AND mint_claimed=false AND expected state_version`，并验证opaque handle明文的digest，做one-shot CAS；同一事务把eligibility改为`claimed`、设置`mint_claimed=true`、递增`state_version`、写入`mint_claim_event_id`并append `authorization_mint_lease_claimed` event；
5. mint-lease CAS同时绑定fresh `pending_capability_id`、生成preparation handle hash并设置`capability_preparation_state=unprepared`、`capability_activation_state=not_ready`；明文handle只在一次性`PostMintLeaseContextV2`返回。第二次/stale claim保持state/version/lease不变并append rejected event；
6. capability preparation必须以current post-lease version、`mint_claim_event_id`、bound pending ID、`preparation_state=unprepared`和opaque preparation handle做one-shot CAS；同一事务存储唯一pending capability exact bytes BLOB/digest、设置`prepared`与activation=`eligible`、生成activation handle hash、递增version并append `authorization_capability_prepared` event；返回的`PreparedCapabilityContextV2`独占activation handle明文；
7. 数据库必须强制`pending_capability_id`全局unique、`(registry_record_id, mint_claim_event_id)`至多一个pending row。第二次／并发preparation保持state/version/pending row不变，以`BLOCKED_AUTHORIZATION_CAPABILITY_ALREADY_PREPARED`或精确stale/handle blocker拒绝并append preparation-rejected event；loser构造的内存candidate bytes立即销毁；
8. capability activation必须以current prepared version、preparation event/digest、bound pending ID、`capability_activation_state=eligible`、opaque activation handle及已验证signed commit record digest做one-shot CAS；同一事务设置`activated`、写入`active_capability_id`、递增version并append activation event；数据库同时强制`active_capability_id`全局unique及`(registry_record_id, capability_preparation_event_id)`至多一个active capability；
9. 第二次／stale activation保持state/version/active capability不变，以`BLOCKED_AUTHORIZATION_CAPABILITY_ALREADY_ACTIVATED`或精确mismatch/stale/handle blocker拒绝并append activation-rejected event；pre-activation writer failure原子设置activation=`aborted`、递增version并append activation-aborted event，不得retry；
10. consume成功但mint-lease尚未claim时的writer failure必须原子把mint eligibility`available -> aborted`、递增version并append eligibility-abort event；旧context立即stale，resolver不得为spent record重建handle；
11. 任何process crash都不会自动制造一个“已执行abort”事实：若crash发生在lease后/preparation前或preparation后/activation前，durable substate可分别保持`unprepared`或`eligible`，但相应明文handle随attempt消失且resolver永不重发，因此fresh process无法推进；测试必须证明这一点，不能把stranded state伪报为aborted；
12. malformed／unknown-version 等 pre-registration rejection 无 registry row，由独立 controller terminal ledger记录；不得创建半 identity；
13. signed runtime event writer 失败不回滚已 commit 的 consumption state或mint lease；catchable failure必须burn remaining eligibility/preparation/activation、阻止 activation/release，并由durable aborted event + 独立 controller terminal ledger收口。

### 3.3 唯一 binding 顺序

```text
build immutable V2 authorization bytes
  -> reject unsafe YAML / duplicate key / multi-document
  -> parse once with the unique V2 loader
  -> validate schema_version and additionalProperties=false
  -> validate cross-field semantics
  -> freeze exact bytes
  -> SHA-256(exact bytes) + size
  -> one transaction: store bytes BLOB + identity + state=unconsumed + registration event
  -> resolve PreConsumeAuthorizationContextV2 at unconsumed state_version
  -> compare run/source/scope/profile/consumer/output request
  -> check time, revoked/expired/replay state
  -> verify signed A1 writer readiness; fail before CAS if unavailable
  -> one transaction: CAS unconsumed -> spent + fresh opaque mint-eligibility handle hash + durable transition event
  -> return PostConsumeMintContextV2 once, carrying the handle plaintext in memory
  -> persist/verify required pre-mint signed A1 transition event
     failure -> one transaction: eligibility available -> aborted + durable abort event; destroy handle; terminal
  -> allocate fresh pending_capability_id
  -> one transaction: verify/consume eligibility handle + CAS available -> claimed + bind pending ID + create preparation handle hash + durable mint-lease event
  -> return PostMintLeaseContextV2 once, carrying preparation handle plaintext
  -> construct candidate pending capability exact bytes in memory
     pre-object catchable failure -> one transaction: preparation unprepared -> aborted + durable abort event; destroy handle/partial buffers; disposition not_created; terminal
  -> validate/sign candidate against capability_claims_schema_v2 and current binding
     post-object catchable failure -> one transaction: preparation unprepared -> aborted + durable abort event; destroy handle/candidate; disposition candidate_destroyed_not_registered; terminal
  -> one transaction: verify/consume preparation handle + CAS unprepared -> prepared + store unique pending bytes/digest + create activation handle hash + durable preparation event
  -> return PreparedCapabilityContextV2 once, carrying activation handle plaintext
  -> persist/verify signed capability-activation commit record
     failure -> one transaction: activation eligible -> aborted + durable abort event; make pending row non-callable; terminal
  -> one transaction: verify/consume activation handle + CAS eligible -> activated + bind commit digest + durable activation event
  -> return ActivatedAuthorizationContextV2 at the committed activation state_version
  -> release exactly that capability; execute pure no-I/O binding probes
```

不变量：

1. schema／semantic validation 失败时 registry identity row delta 为 0；
2. registry identity 创建后 authoritative bytes BLOB 不得变化；
3. resolve／consume 时从 Registry custody BLOB 重新计算 exact bytes digest和 size，并与 Registry identity 比较；不得信任 caller bytes／dict；
4. CAS 必须同时匹配 authorization ID、artifact digest、run ID、Profile ID、nonce、state version 与 `unconsumed`；
5. request 的 source/snapshot/map/scope/range/consumer/output 不匹配时，在 CAS 和 mint 前拒绝；
6. consume CAS 前必须通过 signed A1 writer readiness Gate；capability mint 前 `consumption_state` 和 durable spent event 必须已 committed，且 pre-mint signed A1 transition event已持久化并验证；
7. CAS commit 后任何 crash 均不得回退、补发或在同一 run/auth/nonce 重试；
8. capability、envelope、event、attestation 和 result 可以引用 `authorization_artifact_sha256`，但不得把该值注入 artifact claims；
9. artifact bytes 变化要求 fresh authorization ID、run ID、nonce 与 registry record；不得 update 原 identity；
10. Registry 不接受 parsed dict + bytes 的双输入；exact bytes 是唯一注册输入，Registry BLOB是唯一 resolve source；
11. consumption、eligibility-abort、mint-lease、preparation/abort和activation/abort CAS每次成功都递增 `state_version`；成功主路径返回下一阶段 context，任何先前 context 立即 stale，不能继续prepare、activate或进入下游 probe；
12. preparation CAS是唯一durable pending-capability creation point；此前candidate bytes不算prepared且loser必须销毁。Capability在signed activation commit验证且activation CAS成功前始终不可调用、不可返回；writer失败时pending row标记aborted/non-callable，active capability delta为0；
13. activation CAS必须消费signed commit record的external exact-bytes digest并在durable event中绑定它；CAS成功本身是唯一activation point，之后没有另一个可重复的“activate”调用；
14. consume CAS返回的opaque eligibility handle必须attempt-bound、non-serializable、不可从Registry hash逆向或resolver重建；pre-lease failure显式burn它，process crash则明文随attempt消失，因此spent record不能在fresh attempt继续mint；
15. mint-lease CAS返回的preparation handle与preparation CAS返回的activation handle都必须attempt-bound、non-serializable且不可重建；catchable failure显式abort，process crash则handle明文消失且durable substate可保持unprepared/eligible，不得伪报abort；两种情况下fresh resolver均不能继续；
16. mint-lease CAS后`mint_claimed=true`及其durable event不得回退；preparation CAS后唯一pending row/digest/event不得复用。任一阶段active capability若尚未commit都保持0；
17. activation成功后的crash不得生成第二capability或第二activation；原capability保持唯一Registry identity，未发生的broker/delivery仍为0。

### 3.4 Versioned typed authorization contexts

`ValidatedAuthorizationContextV2` 不是一个可跨状态复用的宽泛对象，而是下列五个互斥、不可变类型：

| 类型 | 必需 state snapshot | 唯一用途 | 何时失效 |
| --- | --- | --- | --- |
| `PreConsumeAuthorizationContextV2` | `consumption_state=unconsumed`、`mint_claimed=false`、resolve 时的 `state_version` | request binding／expiry／revoke检查与 consume CAS输入 | consume CAS成功或任何 state version变化后立即 stale |
| `PostConsumeMintContextV2` | `consumption_state=spent`、`mint_eligibility_state=available`、`mint_claimed=false`、consume CAS返回的 `state_version`、`consumption_event_id`、仅在内存存在的opaque eligibility handle | pre-mint signed transition audit与 mint-lease CAS输入 | mint-lease／eligibility-abort CAS、任何version变化或attempt终止后立即 stale；resolver永不重建 |
| `PostMintLeaseContextV2` | spent、eligibility=claimed、mint_claimed=true、preparation=unprepared、activation=not_ready、mint-lease CAS返回的version/event、bound pending ID、仅内存opaque preparation handle | 构造candidate pending bytes并作为preparation CAS输入 | preparation/abort CAS、任何version变化或attempt终止后立即stale；resolver永不重建 |
| `PreparedCapabilityContextV2` | spent、preparation=prepared、activation=eligible、preparation CAS返回的version/event、pending artifact digest、仅内存opaque activation handle | signed activation commit与activation CAS输入 | activation/abort CAS、任何version变化或attempt终止后立即stale；resolver永不重建 |
| `ActivatedAuthorizationContextV2` | spent、eligibility=claimed、mint_claimed=true、preparation=prepared、activation=activated、activation CAS返回的version、consume/mint/preparation/activation event IDs、唯一active ID | release该唯一capability及纯 broker/reader/audit binding probes | 任何version变化、identity mismatch或attempt结束后失效；不可再次交给issuer activation path |

五个类型都包含：

```text
claims: AuthorizationArtifactV2
identity: AuthorizationRegistryIdentityV2 (resolved from Registry-custody bytes)
state: AuthorizationRegistryStateV2 (read-only snapshot + exact state_version)
```

Registry 的 consume CAS 返回一次性`PostConsumeMintContextV2`；mint-lease CAS验证eligibility handle并返回`PostMintLeaseContextV2`；preparation CAS验证preparation handle并返回`PreparedCapabilityContextV2`；activation CAS验证activation handle并返回`ActivatedAuthorizationContextV2`。调用方不得自行改写state/version、复制/序列化任何handle或在旧对象上refresh。Resolver对spent record只返回精确replay/terminal view，绝不重新签发任一post-consume context/handle。Issuer preparation只接受current PostMintLease并只能提交其bound pending ID；activation只接受current Prepared；pure probes只接受current Activated。错误阶段、旧version、丢失/burned handle、重复preparation或activation一律fail closed。

Issuer、broker、bounded reader 与 read audit 禁止接收：

- 未验证 dict；
- caller 注入的 digest；
- V1 alias；
- 缺 Profile 的 claims；
- 与 Registry state version 不一致的 stale context；
- 阶段错误的 context（例如用 pre-consume context mint capability）；
- caller 重新提供的 artifact bytes、path或parsed claims。

Capability／envelope／audit schema 中的外部 digest字段统一为 `authorization_artifact_sha256`；Registry 内部数据库列名也应归一，避免 `authorization_digest`、`immutable_bytes_sha256`、`immutable_file_sha256` 表示同一个值。

### 3.5 Authorization state machine

`authorization_state` 与 `consumption_state` 是两个不同概念：

- artifact `authorization_state=approved`：不可变的批准决定；
- Registry `consumption_state`：可变的 one-time lifecycle。

只有 finalized `approved` artifact 可以进入 V2 Runtime schema。Draft／denied 文档属于非执行 authoring artifact；它们不得通过 executable V2 schema，也不得注册为 active authorization。

允许状态转移：

```text
unconsumed -> spent
unconsumed -> revoked
unconsumed -> expired
```

`spent`、`revoked`、`expired` 都只对 **authorization consumption axis** 为 terminal：它们都不能回到`unconsumed`或产生第二次consumption event。`revoked`／`expired` 永不允许mint；`spent` 仅允许以current typed context沿一次性的mint/activation substate完成第一个且唯一一个capability。禁止：

- terminal -> unconsumed；
- revoked／expired -> spent；
- spent 后第二次 consumption event；
- revoked／expired 下claim mint lease、prepare或activate capability；
- spent 下绕过`PostConsumeMint -> PostMintLease -> PreparedCapability -> Activated`阶段或生成第二pending/active capability；
- 通过修改 artifact `authorization_state` 改变 Registry state。

`mint_eligibility_state`、`mint_claimed`、`capability_preparation_state`与`capability_activation_state`是`spent`内的独立、单向substate，不是新的consumption state：

```text
eligibility=available / mint=false / preparation=not_claimed / activation=not_ready
  -> eligibility=claimed / mint=true / preparation=unprepared / activation=not_ready
  -> preparation=prepared / activation=eligible
  -> activation=activated | aborted

eligibility=available
  -> eligibility=aborted  (pre-lease failure; no mint)

preparation=unprepared
  -> preparation=aborted  (catchable pre-preparation failure; no pending row)
```

Consume、lease claim、preparation与activation各自创建下一阶段opaque handle hash并与对应durable event原子绑定；catchable failure与durable abort event绑定。每个CAS均递增`state_version`。Eligibility的`claimed/aborted`、preparation的`prepared/aborted`和activation的`activated/aborted`均不得回退；crash-stranded `unprepared/eligible`没有handle明文，逻辑上不可恢复推进，但不得被重标为已durably aborted。

## 4. Portable Profile Assurance Contract

### 4.1 R2-P 必须以 A1 证明的能力

| Contract ID | Portable A1 必须证明 | 最低证据 |
| --- | --- | --- |
| `R2P-A1-001` | authorization exact artifact 存在、可安全解析且通过 V2 schema／semantic validator | loader result + schema identity + signed terminal event |
| `R2P-A1-002` | external registry identity 的 digest／size／schema／Profile／run 与 exact artifact 一致 | registry immutable row + independent recomputation |
| `R2P-A1-003` | authorization identity 精确匹配当前 run；wrong run 在 CAS/mint 前拒绝 | request binding event + zero prohibited side effects |
| `R2P-A1-004` | source、snapshot、map、scope 与 ranges 不得超授权 | typed context comparison + exact blocker |
| `R2P-A1-005` | allowed consumer、allowed outputs 与 denied capabilities 被 Runtime logical Gate 强制 | logical policy events；不声明 OS capability absence |
| `R2P-A1-006` | authorization 一次性消费；CAS 恰好一次成功 | registry state version + unique consumption event |
| `R2P-A1-007` | replay 被拒绝，state 不回退，不产生第二 capability | rejected-attempt delta + final spent state |
| `R2P-A1-008` | revoked／expired authorization 使用精确状态码拒绝 | terminal state + frozen logical clock／revoke event |
| `R2P-A1-009` | nonce、authorization ID、run ID 与 artifact digest 的重复／冲突 fail closed | unique constraints + terminal rejection event |
| `R2P-A1-010` | capability 只在consume CAS、mint-lease CAS、preparation CAS、signed activation commit Gate及activation CAS依次成功后激活，且绑定external digest、Profile、run、nonce与consume/mint/preparation/activation events | durable Registry events + signed commit record + claims verification |
| `R2P-A1-011` | 每个普通 accept／reject operation 都产生可关联、签名有效的 A1 event和独立 controller terminal ledger；故意破坏 signed writer 的 leaf 使用 §4.3 fallback | signed event chain／durable Registry event + controller terminal ledger |
| `R2P-A1-012` | missing／malformed／unknown version／legacy alias 不被兼容 fallback 接受 | version router／validator rejection evidence |
| `R2P-A1-013` | consume CAS 后只能通过一次性 mint-lease CAS进入 capability preparation；第二次 claim与stale context均拒绝 | state version + durable mint-lease event + exact rejected-attempt delta |
| `R2P-A1-014` | mint lease只绑定一个pending ID；preparation CAS最多创建一个durable pending row，activation CAS最多产生一个active capability；重复issuer preparation/activation必须拒绝 | unique pending/active IDs + preparation/activation events + second-attempt delta |
| `R2P-A1-015` | post-consume、post-lease与post-preparation contexts均依赖不同domain的一次性opaque handle；crash后fresh resolver不能重建或推进 | handle-digest state + restarted-process negative probes + active capability delta=0 |

### 4.2 Portable 能声明与不能声明的结论

Portable R2-P PASS 可以声明：

- V2 authorization bytes 已按唯一 loader 解析并验证；
- artifact、Registry identity 与 current run/source/scope/Profile binding 在受 instrumentation 覆盖的 Runtime 逻辑内一致；
- one-time CAS、expiry、revocation、replay、consumer/output/deny policy 按逻辑合同执行；
- accept／reject 的 Registry、issuer 和 audit 事件闭合；
- capability mint 的受控路径没有在 authorization Gate 前发生。

Portable R2-P PASS 不得声明：

- consumer 的完整实际 file-open set 已被观察；
- denied capability 在 OS 层不存在或不可旁路；
- source、Greek、Book 2、full raw 在 OS 层不可访问；
- Candidate/model/business action 已由独立 OS observer 证明为 0；
- A2、A3、hardened、certified、secure sandbox certified 或等价保证。

Portable result／report 必须使用：

```yaml
assurance_profile_id: "CTDE-PORTABLE-DEV-1"
highest_claimed_evidence_level: "A1"
a2_os_file_access_proof: "NOT_PROVIDED"
a2_verified_access_counts: null
hardened: false
certified: false
portable_to_hardened_promotion_allowed: false
```

### 4.3 A1 audit event 最低字段

每个 R2 leaf 的 accept 或 reject event 至少绑定：

```yaml
event_schema_id: "urn:ctde:schema:runtime-audit-attestation:2"
event_schema_version: "2.0.0"
event_type: "authorization_transition | capability_activation_commit | terminal_accept | terminal_reject"
authorization_schema_version: "2.0.0"
assurance_profile_id: "CTDE-PORTABLE-DEV-1"
test_attempt_id: "<fresh synthetic leaf attempt>"
consume_operation_id: "<unique consume/subattempt id or explicit null when not a consume>"
registry_operation_id: "<unique registry operation id or explicit null before registration>"
run_id: "<artifact run_id or explicit absent before parse>"
authorization_id: "<id or explicit absent>"
authorization_artifact_sha256: "<external digest or explicit unavailable>"
registry_record_id: "<id or explicit not_registered>"
observed_consumption_state: "<state or explicit not_registered>"
observed_mint_eligibility_state: "<state or explicit not_registered>"
observed_capability_preparation_state: "<state or explicit not_registered>"
observed_capability_activation_state: "<state or explicit not_registered>"
state_version: "<integer or null>"
consumption_event_id: "<id or null>"
mint_claim_event_id: "<id or null>"
pending_capability_id: "<id or null>"
pending_capability_artifact_sha256: "<external digest or null>"
capability_preparation_event_id: "<id or null>"
capability_activation_event_id: "<id or null>"
capability_id: "<id or null>"
result: "accepted | rejected | blocked"
blocker: "<exact code or null>"
event_sequence: "<monotonic integer>"
previous_event_sha256: "<digest or genesis>"
```

`test_attempt_id` 关联 manifest leaf；`consume_operation_id` 关联 leaf 内的单次消费、重放或并发 contender。Replay 的第二次 operation和 concurrent CAS 的每个 loser必须有不同 operation ID，才能机械计算各自副作用增量。

`capability_activation_commit` 是activation CAS前已持久化并验证的signed A1 terminal-accept commitment：它必须绑定current prepared `state_version`、`mint_claim_event_id`、`capability_preparation_event_id`、pending artifact digest、唯一pending ID和预期accepted transition，其external exact-bytes SHA-256由activation CAS写入Registry state/event。单独存在的commit record是inert/orphan，不代表activation，也不能计入terminal count；activation CAS对其digest的原子引用使该预签名commit成为terminal accept证据。只有“signed commit digest + accepted Registry activation event + Activated context”三者一致时才算成功。这样activation后不存在另一个必须成功的fallible signed-writer步骤；若activation CAS拒绝，orphan commit必须标记不可复用，并另产生日志真实结果的signed terminal rejection。

拒绝事件是必需证据，不属于禁止副作用。普通负向 leaf 要求 signed terminal rejection event 和 controller terminal ledger 都存在，同时 consumption event、mint lease、active capability、broker read、delivery、consumer、model与业务输出的拒绝增量为 0。

故意模拟 signed runtime event writer unavailable/failure 的 leaf 是唯一例外：

- 同一已失败 writer 的 signed event 预期为 0，不能伪造；
- pre-CAS readiness failure：state/event/capability均不变，独立 controller terminal ledger恰好 1；
- post-CAS/pre-lease failure：consumption state保持spent；除CAS事务内durable spent event外，eligibility必须原子`available -> aborted`并产生一个durable abort event；opaque handle销毁，mint lease与active capability均为0，旧context与fresh resolve retry均拒绝，独立controller terminal ledger恰好1；
- post-preparation/pre-activation commit-writer failure：consumption state保持spent、mint lease与preparation各成功恰好1、activation必须原子`eligible -> aborted`并产生durable abort event；pending row保留为审计证据但标记non-callable，内存token销毁且active/released capability为0，独立controller terminal ledger恰好1，禁止retry；
- 该例外只证明 fail-closed和真实审计缺失记录，不把缺失 signed event当作普通成功证据。

Manifest显式声明的process-crash injection leaf也可在crash point之后没有Runtime terminal event，但它不是writer-failure伪装：controller terminal必须绑定injected crash point、最后一个已commit Registry event/state/version、process-exit observation和restart probe。此类leaf只有在所有pre-crash expected events存在、post-crash禁止副作用为0、opaque handle未恢复且restart精确拒绝时才PASS；否则BLOCKED/FAIL。该controller observation仍只属于A1，不是完整OS descendant/process evidence。

### 4.4 Independent controller terminal ledger contract

Controller terminal ledger 是 test runner 的独立、append-only A1 channel，不是 Runtime signed event 的替代品，也不与其共享 writer。未来新建的 `r2_portable_controller_terminal_schema_v1.yaml` 必须采用 `additionalProperties: false`，并至少要求：

| 字段 | 唯一语义 |
| --- | --- |
| `controller_terminal_schema_version` | 常量 `1.0.0` |
| `controller_terminal_id` | 全局唯一、不可复用的controller terminal record ID |
| `controller_id`、`controller_version`、`controller_binary_sha256` | test-only controller immutable writer identity |
| `controller_key_id` | test-only signing key identity；不得是 Candidate／production key |
| `controller_event_canonicalization_id` | 常量 `CTDE-R2P-CONTROLLER-JCS-1` |
| `signature_domain` | 常量 `CTDE-R2P-CONTROLLER-TERMINAL-V1` |
| `suite_id`、`manifest_sha256`、`test_attempt_id` | 绑定 frozen manifest leaf |
| `consume_operation_id` | consume／replay／concurrency subattempt ID；不适用时显式 null |
| `registry_operation_id`、`registry_event_id` | 关联 durable Registry operation/event；pre-registration 时显式 null |
| `authorization_id`、`run_id`、`assurance_profile_id` | 可解析时精确绑定；不可解析时使用 schema允许的 explicit unavailable/null，不得猜测 |
| `authorization_artifact_sha256` | external exact-bytes digest；尚未形成时显式 null |
| `observed_consumption_state`、`observed_mint_eligibility_state`、`observed_capability_preparation_state`、`observed_capability_activation_state`、`state_version`、`mint_claimed` | controller terminal观察到的 Registry真值或明确 not-registered/null |
| `mint_claim_event_id`、`pending_capability_id`、`pending_capability_artifact_sha256`、`capability_preparation_event_id`、`active_capability_id`、`capability_activation_event_id` | 相关时精确绑定；不适用时显式null |
| `signed_runtime_writer_status` | `available_success | unavailable | failed | not_reached` |
| `fault_injection_id` | manifest-bound ID或null；不得动态发明未枚举fault |
| `injected_crash_point` | `after_consume_before_lease | after_lease_before_preparation | after_preparation_before_activation | null` |
| `process_exit_observation` | `not_injected | injected_exit_observed | injected_exit_not_observed`；只构成controller A1 observation |
| `pending_capability_disposition` | closed enum：`not_created | candidate_destroyed_not_registered | prepared_row_aborted_token_destroyed | prepared_row_stranded_handle_lost | activated` |
| `result`、`blocker` | closed terminal result与精确 blocker；不得以自由文本替代 |
| `controller_sequence`、`previous_controller_event_sha256` | 单调顺序与append-only chain binding |
| `controller_recorded_at` | frozen/logically controlled RFC 3339 UTC timestamp |
| `signature_algorithm`、`signature` | 算法常量`Ed25519`；signature为unpadded base64url |

Canonicalization、签名与chain输入唯一冻结如下：

1. schema只接受UTF-8 JSON object；禁止BOM、duplicate keys、float和schema外字段；
2. `CTDE-R2P-CONTROLLER-JCS-1` 等于 RFC 8785 JCS；unsigned payload是完整event object**仅删除`signature`字段**后的JCS bytes，`signature_algorithm`、`signature_domain`、key ID及previous digest仍在输入中；
3. Ed25519签名输入为ASCII `CTDE-R2P-CONTROLLER-TERMINAL-V1` + 单个NUL byte + unsigned JCS bytes；
4. 写入signature后，持久artifact exact bytes必须是完整object的JCS UTF-8 bytes再加单个LF，不能使用其他pretty-print形式；
5. `previous_controller_event_sha256` 是前一条**完整持久artifact exact bytes（含signature与末尾LF）**的SHA-256；chain genesis固定为64个小写`0`；
6. 当前artifact的exact bytes SHA-256由suite evidence manifest外部保存，不能写入自身形成self-digest。
7. 每个frozen R2 suite只允许一个`(suite_id, controller_id, controller_version, controller_key_id)` tuple；该tuple定义唯一suite-wide chain scope，禁止per-leaf fork、mid-suite key rotation或跨suite链接；
8. chain第一条record的`controller_sequence=0`且previous digest为genesis；此后sequence必须恰好加1，previous digest必须等于sequence前一条record的exact-bytes SHA-256；
9. 并发Runtime outcomes先进入controller的单一append queue；唯一writer在一个逻辑exclusive append critical section内读取last sequence/digest、分配next sequence、签名并atomic-create完整record。Writer crash造成的缺记录使`T`闭包失败；不得重用sequence、补造假terminal或建立第二chain。

Verifier必须按sequence排序，机械确认chain恰好覆盖`0..T-1`、一个genesis、无gap/duplicate/fork，并逐条核对schema、canonicalization、controller identity、signature、manifest correlation和Registry真值；controller writer或verifier失败时，该 leaf 只能 BLOCKED／FAIL，不能以“Runtime writer也失败”为由生成 PASS。这里的single-writer/atomic-create只是A1 controller协议，不声称OS-level atomicity或A2 tamper isolation。该ledger不得记录或声称OS file-open completeness、PID attribution或任何A2/A3结论。

## 5. 与 Hardened Profile 的兼容性

### 5.1 共享内容与禁止分叉

Portable 与 Hardened 必须共享：

- 同一个 Schema V2 ID/version；
- 相同字段名、类型、requiredness 与业务语义；
- 相同 exact-bytes digest 和 external registry binding 规则；
- 相同 run/source/snapshot/map/scope/range/consumer/output/deny semantics；
- 相同 one-time、expiry、revocation、nonce 与 replay state machine；
- 相同 fail-closed version／alias／digest mismatch 行为。

不得为 Portable 另建语义不兼容的 authorization schema。Hardened 也不得通过另一套业务授权字段改变范围、consumer 或输出含义。

### 5.2 Hardened 只增加更强 evidence

Hardened 未来增加的是：

- Profile-bound A2-capable environment qualification；
- 独立 OS-level process/file evidence；
- complete PID/descendant attribution；
- complete file-access／second-channel observation；
- evidence tamper isolation 与 event-loss closure；
- 在同一 fresh attempt 上关联 A1 + A2 为 A3。

A2/A3 evidence 不写入 authorization payload，也不改变 Schema V2 的业务语义。它们由 Hardened execution snapshot、observer evidence、attestation 和 Gate 外部绑定 `authorization_artifact_sha256`。

### 5.3 Cross-profile 不变量

```yaml
shared_schema_definition_allowed: true
shared_implementation_code_allowed: true
shared_business_authorization_semantics_required: true

cross_profile_authorization_artifact_reuse: false
cross_profile_registry_record_reuse: false
cross_profile_run_id_reuse: false
cross_profile_nonce_reuse: false
cross_profile_consumption_event_reuse: false
cross_profile_validation_evidence_reuse: false
portable_r2_pass_implies_hardened_r2_pass: false
```

Hardened future run 必须 fresh 生成 Hardened Profile-bound authorization ID、run ID、nonce、exact artifact bytes、registry identity、state/event、capability、evidence 与 result。把 Portable artifact 的 `assurance_profile_id` 改为 Hardened 会改变 bytes/digest，并要求全新 identity；不能原地修改或追认。

## 6. Migration Plan

### 6.1 V1 disposition：默认 fail closed

现有 V1 schema、181 个 authorization artifacts、旧 Registry rows、旧 suite 与旧 evidence：

- 原字节保留；
- 不回填 self-digest；
- 不原地转换；
- 不批量重标 V2；
- 不重置或继承 consumption state；
- 不复用 authorization ID、attempt/run ID、nonce、event、capability 或 delivery；
- 只标为 `deprecated / historical_only / non_executable_under_v2`；
- 只允许历史 verifier 读取，不允许 active V2 Runtime 消费。

新 Runtime 对以下输入必须在 registration 前 fail closed：

- 缺 `schema_version`；
- `schema_version=1.x`；
- unknown／future version；
- V1 field alias；
- artifact 内 self-digest 或 self-digest alias；
- 自动转换后的内存 dict；
- 缺 Profile 或 Profile mismatch；
- 旧 suite／旧 Registry identity reuse。

默认 blocker：`BLOCKED_AUTHORIZATION_SCHEMA_VERSION_UNSUPPORTED` 或更精确的 V2 code。不得保留“尝试 V2，失败则按 V1 解析”的 compatibility fallback。

旧 V1 schema 的 deprecated 标记应由新的 version router／R2 result 记录；不得为了标记 deprecated 而修改冻结 V1 schema 或旧 artifact。

### 6.2 字段迁移映射

| V1／draft 字段 | V2 处理 | 兼容策略 |
| --- | --- | --- |
| 无 `schema_version` | 新增 required `schema_version=2.0.0` | missing/1.x 拒绝，不推断 |
| `attempt_id` | 改为 `run_id` | 不接受 alias；test attempt 仅留在 runner evidence |
| `fixture_object_id` | 拆为 `source_id`、`source_snapshot_id`、snapshot digest | 不自动从旧 URN 推断 |
| `fixture_structure_contract_id` | `structure_map_id` + file/payload digests | 不接受旧 alias |
| `allowed_range` | `allowed_ranges`，当前恰好一项 | 不自动包裹旧对象 |
| `expected_length`／`expected_slice_sha256` | 移入唯一 range item | 必须重新生成 V2 artifact |
| `forbidden_source_roles` | 版本化 `denied_capabilities` | 不做词汇自动翻译 |
| `expires_at` integer | quoted RFC 3339 UTC string | 不隐式转换旧 epoch |
| 无 `issued_at` | 新增 required | 必须由 fresh authority 生成 |
| 无 authorization nonce | 新增 required registry-unique nonce | 不从 capability nonce 继承 |
| `initial_state` | 从 artifact 删除 | immutable `authorization_state=approved`; current state 只在 Registry |
| `authorization_file_sha256` | artifact 中禁止 | Registry 使用 `authorization_artifact_sha256` |
| `prototype_fixture_authorized` 等多重布尔 | 由 artifact class、Profile、task scope与 allowed/denied fields 表达 | 不接受旧布尔作为授权替代 |

### 6.3 未来受影响组件

| 组件 | 未来 R2-P 最小修改 |
| --- | --- |
| Authorization V2 loader／validator | safe parse、duplicate-key rejection、version route、schema + semantic validation、typed immutable claims |
| Authorization Registry | exact-bytes-only registration、immutable identity/state 分离、unique Profile/run/nonce、revocation、expiry boundary、consume/eligibility-burn/mint-lease/preparation/activation CAS及durable events |
| Capability issuer | 从current PostMintLease提交唯一pending candidate到preparation CAS；从current Prepared提交signed activation commit；activation CAS后只释放唯一active ID；绑定consume/mint/preparation/activation events |
| Range broker | 新增纯 `validate_authorization_binding_v2` pre-open path，只接收 typed context／opaque resolved identity；R2 实际调用该纯校验，但 open/read保持0 |
| Bounded reader | 新增纯 `validate_authorization_binding_v2` pre-delivery path，验证 external digest/Profile/run/nonce/event；R2 实际调用该纯校验，但FD/delivery消费保持0 |
| Read audit／events | 新增纯 context-correlation path，使用唯一字段名并记录 A1 accept/reject；不读取source、不产生A2 claim |
| Capability／envelope／attestation V2 schemas | **新建** V2 files；统一 external `authorization_artifact_sha256` 与 Profile/run/nonce/event binding；V1 schema exact bytes不改 |
| R2 manifest／runner | 只枚举 V2 parse/register/resolve/CAS/mint/audit tests；不进入 source read、R3 或 R4 |

### 6.4 Migration 顺序

1. 冻结 R2-P execution authorization、文件 allowlist、test-only trust root 与 Profile ID；
2. 新建 V2 artifact schema、Registry record schema和唯一 loader；
3. 实现 safe parse、version route、schema／semantic validator；
4. 修改 Registry 为 exact-bytes-only registration，并分离 immutable identity 与 mutable state；
5. 增加 unique authorization ID／run ID／nonce与精确 revoked／expired／spent状态机；
6. 引入 `PreConsume -> PostConsumeMint -> PostMintLease -> PreparedCapability -> Activated` typed context family、三类domain-separated opaque handles与stale-version rejection；
7. 实现 eligibility burn、one-shot mint-lease/preparation/activation CAS、各自durable event、crash-stranding拒绝及重放拒绝；
8. 仅修改 issuer／broker／reader／audit 的 authorization identity binding，不执行 source path；
9. 更新 downstream signed-object schemas 的 Profile/run/external digest 名称；
10. 构建 dedicated R2 requirement manifest、controller terminal schema，并由 runner 动态枚举 leaf／operation；
11. 在完全 synthetic、无 source read 的环境执行 deterministic R2 tests；
12. 生成独立 R2 result，明确 A1/non-certified 与 A2 not provided；
13. 若全部验收通过，才可标记 R2-P execution PASS；这仍不授权 R3、R4-P 或 Candidate。

## 7. R2 Implementation Atomic Scope

### 7.1 未来 R2 可创建／修改的闭合 allowlist

以下只是未来执行授权应采用的文件白名单；本阶段未创建或修改其中任何文件。路径名若在真正实施前需要调整，必须先更新并独立批准 R2 execution scope，不能运行中自行扩展。

#### 允许新建

```text
runtime_capability_prototype/contracts/authorization_schema_v2.yaml
runtime_capability_prototype/contracts/authorization_registry_record_schema_v2.yaml
runtime_capability_prototype/contracts/authorization_registry_event_schema_v2.yaml
runtime_capability_prototype/contracts/r2_portable_controller_terminal_schema_v1.yaml
runtime_capability_prototype/contracts/capability_claims_schema_v2.yaml
runtime_capability_prototype/contracts/broker_envelope_schema_v2.yaml
runtime_capability_prototype/contracts/audit_attestation_schema_v2.yaml
runtime_capability_prototype/runtime/ctde_runtime/authorization_v2.py
runtime_capability_prototype/contracts/r2_portable_authorization_test_requirements.yaml
runtime_capability_prototype/runtime/build_r2_portable_manifest.py
runtime_capability_prototype/runtime/run_r2_portable.py
```

#### 允许最小修改

```text
runtime_capability_prototype/runtime/ctde_runtime/authorization_registry.py
runtime_capability_prototype/runtime/ctde_runtime/range_broker.py
runtime_capability_prototype/runtime/ctde_runtime/bounded_reader.py
runtime_capability_prototype/runtime/ctde_runtime/read_audit.py
runtime_capability_prototype/runtime/ctde_runtime/events.py
```

允许修改 downstream 文件的唯一原因是新增 V2 typed-context binding path，并统一 external digest/Profile/run/nonce/event binding。现有 V1 schema exact bytes不得修改；version router必须显式选择 V2。

R2 runner 必须实际调用以下纯、无 I/O binding probes：

```text
CapabilityIssuer.validate_preparation_binding_v2
CapabilityIssuer.validate_activation_binding_v2
RangeBroker.validate_authorization_binding_v2
BoundedReader.validate_authorization_binding_v2
ReadAudit.validate_authorization_correlation_v2
```

Issuer preparation probe只接受current`PostMintLeaseContextV2`及其bound pending ID；issuer activation probe只接受current`PreparedCapabilityContextV2`及pending artifact digest；RangeBroker、BoundedReader与ReadAudit probes只接受current`ActivatedAuthorizationContextV2`。这些paths均验证stage/version、Profile、run、external digest、nonce、consume/mint/preparation/activation events、唯一capability和consumer audience。它们不得调用source catalog、`open/pread`、sealed FD、delivery CAS、sandbox、parser、model gateway或publisher；runner必须逐leaf断言broker open/read、delivery和consumer调用均为0。

#### 允许 future R2 execution 生成的 fresh suite artifacts

```text
runtime_capability_prototype/r2_portable_suites/<fresh_r2_suite_id>/control/r2_portable_manifest.yaml
runtime_capability_prototype/r2_portable_suites/<fresh_r2_suite_id>/control/component_inputs.json
runtime_capability_prototype/r2_portable_suites/<fresh_r2_suite_id>/artifacts/<leaf_id>/authorization_v2.yaml
runtime_capability_prototype/r2_portable_suites/<fresh_r2_suite_id>/registry/authorization_registry_v2.sqlite3*
runtime_capability_prototype/r2_portable_suites/<fresh_r2_suite_id>/evidence/<leaf_id>/*
runtime_capability_prototype/r2_portable_suites/<fresh_r2_suite_id>/evidence/<leaf_id>/controller_terminal/<controller_sequence>_<controller_terminal_id>.json
runtime_capability_prototype/r2_portable_suites/<fresh_r2_suite_id>/terminal/<leaf_id>.json
runtime_capability_prototype/r2_portable_suites/<fresh_r2_suite_id>/aggregate/r2_portable_results.json
runtime_capability_prototype/r2_portable_suites/<fresh_r2_suite_id>/report/PORTABLE_AUTHORIZATION_SCHEMA_V2_RESULT.md
```

`sqlite3*` 只表示该 fresh suite专用DB及其SQLite管理的WAL/SHM sidecars；不得匹配旧 Registry。每个controller-terminal JSON文件必须恰好包含§4.4定义的一条完整canonical record，不能把多条record包入一个array后再解释chain digest。Evidence目录只允许signed logical events、durable Registry event导出和controller terminal ledger，不允许source payload、slice、business output或OS trace。

### 7.2 明确不在 R2 allowlist

未来 R2 严格禁止顺便修改或实施：

- `contracts/component_manifest.yaml`、closure graph、component snapshot、platform boundary或任何 R3 transitive closure；
- 现有 `runtime/build_manifest.py` 的 R3/R4 suite语义；
- `runtime/run_suite.py` 的旧 197-leaf E2E执行语义；
- 现有 V1 `authorization_schema.yaml`、`capability_claims_schema.yaml`、`broker_envelope_schema.yaml`、`audit_attestation_schema.yaml` 的任何原地改写；
- sandbox、native probe、fixture factory、fixture recipe、formal loader、source catalog或source handling；
- 旧 suite `RCPTS-20260811-001/002`、旧 cases、旧 evidence、旧 Registry DB或旧 report；
- R4-P Book 1 synthetic E2E、Hardened A2/A3 tests；
- Candidate Plan、authorization、Run root或Candidate execution；
- English／Greek TEI path、identity、checksum、payload或structure data；
- `story_structure.yaml` 或任何业务数据。

若实现发现必须修改 allowlist 外文件，正确动作是：停止 R2，记录 `BLOCKED_R2_ATOMIC_SCOPE_EXPANSION_REQUIRED`，获得新的独立范围授权。不得把范围扩大解释为“顺手修复”。

### 7.3 R2 原子退出边界

R2 implementation 的最远成功点是：

```text
V2 parse
  -> validate
  -> register exact identity
  -> resolve pre-consume typed context
  -> compare request binding
  -> CAS one-time state and return post-consume context
  -> persist pre-mint A1 transition audit
  -> CAS mint lease/bind pending ID and return post-lease context
  -> CAS one-time preparation/store pending bytes and return prepared context
  -> persist signed activation commit
  -> CAS one-time activation and return activated context
  -> release the unique test-only capability
  -> execute pure broker/reader/audit binding probes
  -> emit controller terminal ledger
```

纯 binding probe只可读取唯一active capability与`ActivatedAuthorizationContextV2`的不可变test projection；不得再mint token，也不得生成active envelope/delivery。R2 不得打开 source object、读取 range、接收FD、消费delivery、启动 bounded consumer、形成E2E result或生成业务输出；那些动作属于R4-P。

## 8. R2 验收条件

### 8.1 测试设计规则

未来 R2 tests 必须：

- 完全 synthetic、non-literary；
- 使用 test-only source/snapshot/map/scope IDs 与 test trust root；
- 每个 leaf 使用 fresh test attempt、run、authorization ID 和 nonce；
- 不复用旧 grants、state、events、capabilities 或 result；
- 使用冻结的逻辑时钟，避免 expiry 边界竞态；
- 在 manifest 冻结前不声明测试总数；
- 每个 expected rejection 只有在精确 blocker、禁止副作用增量为 0、并按 §4.3 形成普通 signed+controller audit 或故障注入 fallback audit 时才算 leaf PASS；
- valid leaf 到 test-only capability activation、纯 broker/reader/audit binding probes和controller terminal ledger，不触发 broker open/read/delivery；
- 不借用 R3 closure 或 R4 E2E 证据。

### 8.2 必需 deterministic requirement categories

以下是 requirement categories，不是预填的 leaf 总数。Manifest builder 可以把每个类别展开为多个 leaf；实际总数只能在未来由冻结 manifest 与 runner 枚举。

| Requirement ID | 必需情形 | 预期结果 | 拒绝阶段／关键断言 |
| --- | --- | --- | --- |
| `R2P-REQ-VALID` | valid V2 authorization accepted | PASS | parse→validate→register→pre-consume→consume CAS/eligibility handle→post-consume→pre-mint audit→mint-lease CAS/preparation handle/bound ID→post-lease→preparation CAS/store pending bytes/activation handle→prepared→signed activation commit→activation CAS→activated/unique capability→pure probes→controller terminal；broker open/read/delivery=0 |
| `R2P-REQ-WRONG-RUN` | wrong run rejected | expected rejection PASS | CAS/mint 前 `BLOCKED_AUTHORIZATION_RUN_MISMATCH` |
| `R2P-REQ-WRONG-SOURCE` | wrong source／snapshot rejected | expected rejection PASS | CAS/mint 前 `BLOCKED_AUTHORIZATION_SOURCE_MISMATCH` |
| `R2P-REQ-OUT-OF-RANGE` | request range outside／larger／override rejected | expected rejection PASS | CAS/mint 前 `BLOCKED_AUTHORIZATION_RANGE_EXCEEDED` |
| `R2P-REQ-EXPIRED` | `now >= expires_at` | expected rejection PASS | state=expired；`BLOCKED_AUTHORIZATION_EXPIRED`；mint=0 |
| `R2P-REQ-REVOKED` | unconsumed authorization revoked before consume | expected rejection PASS | state remains revoked；`BLOCKED_AUTHORIZATION_REVOKED` |
| `R2P-REQ-REPLAY` | spent authorization consumed again | expected rejection PASS | second-attempt delta mint=0；state remains spent；`BLOCKED_AUTHORIZATION_REPLAY` |
| `R2P-REQ-MALFORMED` | malformed YAML/schema、duplicate key、extra field、self-digest alias | expected rejection PASS | registration row delta=0；`BLOCKED_AUTHORIZATION_SCHEMA_INVALID` |
| `R2P-REQ-UNKNOWN-VERSION` | missing／1.x／unknown version | expected rejection PASS | registration row delta=0；`BLOCKED_AUTHORIZATION_SCHEMA_VERSION_UNSUPPORTED` |
| `R2P-REQ-REGISTRY-DIGEST` | Registry authoritative BLOB重算出的 exact bytes／size 与 immutable identity mismatch | expected rejection PASS | sacrificial test DB corruption injector后，consume CAS/mint 前 `BLOCKED_AUTHORIZATION_REGISTRY_DIGEST_MISMATCH`; identity row unchanged |

### 8.3 额外 mandatory security／compatibility categories

以下同样属于未来 mandatory requirements；它们不能用十个最低类别替代：

| Requirement ID | 必需情形 | 预期 |
| --- | --- | --- |
| `R2P-REQ-PROFILE` | Profile missing、wrong、cross-profile reuse | 精确 `BLOCKED_AUTHORIZATION_PROFILE_MISMATCH`；不注册或不消费 |
| `R2P-REQ-NONCE` | duplicate／wrong nonce | registration conflict为 `BLOCKED_AUTHORIZATION_NONCE_CONFLICT`；consume mismatch为 `BLOCKED_AUTHORIZATION_NONCE_MISMATCH`；无第二 Registry identity、consumption event、mint lease或active capability；必须有terminal rejection audit |
| `R2P-REQ-CONSUMER` | wrong consumer/component identity | CAS/mint 前 `BLOCKED_AUTHORIZATION_CONSUMER_MISMATCH` |
| `R2P-REQ-CONTEXT-CONSUMERS` | issuer preparation收到current post-lease、issuer activation收到current prepared；broker/reader/audit收到current activated；并注入untyped/wrong-stage/stale/mismatched context | issuer两个stage path及三个下游pure paths实际执行；只有stage-correct current context接受，其余以精确type/stage/stale/identity blocker拒绝；open/read/delivery=0 |
| `R2P-REQ-OUTPUT` | unallowlisted output／path widening | CAS/mint 前 `BLOCKED_AUTHORIZATION_OUTPUT_NOT_ALLOWED`；业务输出=0（A1 ledger） |
| `R2P-REQ-DENY-POLICY` | denied capability 缺项、移除或请求 | malformed set为 `BLOCKED_AUTHORIZATION_SCHEMA_INVALID`；实际请求为 `BLOCKED_AUTHORIZATION_CAPABILITY_DENIED`；不得将结果描述为 OS proof |
| `R2P-REQ-ONE-TIME-FLAGS` | `one_time=false`、retry/inheritance=true | registration 前 `BLOCKED_AUTHORIZATION_SCHEMA_INVALID` |
| `R2P-REQ-TIME` | issued/expiry ordering、at-expiry boundary、invalid timezone | ordering／format为 `BLOCKED_AUTHORIZATION_TIME_INVALID`；`now >= expires_at`为 `BLOCKED_AUTHORIZATION_EXPIRED`；使用 frozen clock |
| `R2P-REQ-CLAIMS-BYTES` | parsed claims 被调用方篡改但 bytes/digest不变 | `BLOCKED_AUTHORIZATION_CONTEXT_MISMATCH`；Registry authority不变 |
| `R2P-REQ-REGISTRY-BLOB-TAMPER` | registration 后以test-only corruption injector改变 Registry custody BLOB | 独立sacrificial DB；digest/size重算不匹配并在consume/mint前以 `BLOCKED_AUTHORIZATION_REGISTRY_DIGEST_MISMATCH` 拒绝；immutable identity row不改，不能把corrupted BLOB当新artifact |
| `R2P-REQ-AUDIT-COPY-MUTATION` | 只改变 Registry 外部的audit/export copy bytes | Runtime resolver继续只读取Registry custody BLOB且authorization authority不变；独立evidence verifier产生 `BLOCKED_EVIDENCE_AUDIT_COPY_DIGEST_MISMATCH` expected-detection结果；Registry state/version不变 |
| `R2P-REQ-CONCURRENT-CAS` | 并发消费同一 authorization | 恰好一个 CAS winner；其余以 `BLOCKED_AUTHORIZATION_REPLAY` 拒绝 |
| `R2P-REQ-CRASH-AFTER-CAS` | consume CAS commit、mint前崩溃 | controller terminal为 `BLOCKED_CAPABILITY_MINT_INTERRUPTED_AFTER_SPEND`；state remains spent；opaque handle明文随attempt消失；fresh process resolve只得replay/terminal view，mint=0且不得补发／回退 |
| `R2P-REQ-POST-CONSUME-RETRY` | post-CAS/pre-lease writer failure后，以保留旧context及fresh resolver两条路径重试 | eligibility已durably aborted且version递增；旧context `BLOCKED_AUTHORIZATION_CONTEXT_STALE`，fresh resolve `BLOCKED_AUTHORIZATION_REPLAY`；mint lease/active capability增量=0 |
| `R2P-REQ-MINT-LEASE-REPLAY` | 同一 post-consume authorization第二次／stale mint-lease claim | 首次恰好一个 `authorization_mint_lease_claimed` event；第二次保持state/version/lease不变，以 `BLOCKED_AUTHORIZATION_MINT_LEASE_ALREADY_CLAIMED` 拒绝并记录rejected event；active capability增量=0 |
| `R2P-REQ-CAPABILITY-PREPARATION-FAILURE` | mint-lease成功后、preparation success CAS前的catchable failure；manifest区分candidate object形成前与形成后注入点 | 两类均精确`BLOCKED_CAPABILITY_PREPARATION_FAILED`，preparation原子`unprepared -> aborted`并产生abort event，handle销毁、durable pending row=0、旧context/fresh retry拒绝；object形成前要求destroyed=0/disposition=`not_created`，形成后的schema/signing failure要求destroyed=1/disposition=`candidate_destroyed_not_registered` |
| `R2P-REQ-CAPABILITY-PREPARATION-REPLAY` | 顺序及并发复用同一current post-lease context/handle/pending ID调用preparation | 恰好一个preparation CAS、pending row/digest和`authorization_capability_prepared` event；其余以stale/`BLOCKED_AUTHORIZATION_CAPABILITY_ALREADY_PREPARED`拒绝；第二prepared capability增量=0 |
| `R2P-REQ-POST-LEASE-CRASH` | (a) mint-lease后/preparation前crash；(b) preparation后/activation前crash | durable state分别可保持unprepared/eligible，但handle明文丢失；fresh resolver只返回spent terminal view；任何伪造/重建推进分别以`BLOCKED_AUTHORIZATION_PREPARATION_HANDLE_UNAVAILABLE`、`BLOCKED_AUTHORIZATION_ACTIVATION_HANDLE_UNAVAILABLE`拒绝；active capability=0且不得伪报aborted |
| `R2P-REQ-CAPABILITY-ACTIVATION-REPLAY` | 首次activation后，复用原prepared context/activation handle/pending ID调用issuer或activation CAS | 首次恰好一个active capability和activation event；第二次以stale/`BLOCKED_AUTHORIZATION_CAPABILITY_ALREADY_ACTIVATED`拒绝，state/version/active ID不变，第二active capability增量=0 |
| `R2P-REQ-AUDIT-FAILURE` | pre-CAS、post-CAS/pre-lease、post-preparation/pre-activation 三个signed writer failure windows | 精确`BLOCKED_A1_AUDIT_WRITER_UNAVAILABLE`或`BLOCKED_A1_AUDIT_WRITE_FAILED`；writer自身event=0；controller terminal=1；任一window active capability=0；已commit consumption/lease/preparation不回退，remaining eligibility/activation被durably aborted且禁止retry |

### 8.4 Expected rejection 的统一副作用合同

除特定 replay/concurrency setup 的首个合法消费外，每次被拒尝试的增量必须满足：

```yaml
unauthorized_registry_identity_rows_created: 0
unauthorized_state_transitions: 0
successful_consumption_cas_events: 0
successful_mint_lease_cas_events: 0
successful_capability_preparation_cas_events: 0
successful_capability_activation_cas_events: 0
consumption_events_created: 0
mint_eligibility_aborts: 0
mint_leases_claimed: 0
capability_preparation_aborts: 0
pending_capabilities_prepared: 0
pending_capabilities_destroyed: 0
capability_activation_aborts: 0
capability_activations: 0
capabilities_minted: 0
broker_open_calls: 0
broker_read_calls: 0
deliveries_created: 0
consumer_invocations: 0
model_invocations: 0
business_outputs_created: 0
signed_runtime_terminal_rejection_events: 1
controller_terminal_events: 1
```

本向量中的`pending_capabilities_prepared`只计算preparation CAS创建的唯一durable pending row；CAS前candidate bytes不计入且loser用`candidate_destroyed_not_registered`收口。`pending_capabilities_destroyed`只计算内存candidate/token销毁，**不表示删除durable pending row**。`capabilities_minted`只计算已经Registry-activated、可返回/可调用的capability。Audit Gate失败后pending row保留为审计证据、标记aborted/non-callable，controller记录`prepared_row_aborted_token_destroyed`；after-preparation crash则保持prepared/eligible真值并记录`prepared_row_stranded_handle_lost`，不能静默忽略或伪报aborted。

特殊规则：

- replay leaf 的零副作用按**第二次被拒尝试的增量**计算；首次合法 CAS/event 不计入拒绝增量；
- concurrent CAS leaf 允许且要求恰好一个 winner，其余 attempts 的成功 CAS/mint 增量为 0；
- expired/revoked/replay leaf 的 terminal-state setup使用独立 `consume_operation_id`；被拒 operation 的增量从 setup 完成后开始，原 terminal state不变；
- malformed/unknown-version 在 registration 前拒绝；
- registry digest mismatch 在 CAS/mint 前拒绝，immutable identity row 不修改；
- Registry BLOB tamper只允许使用leaf-local sacrificial DB与显式test corruption injector；不得污染其他leaf或把corrupted bytes注册为新identity；
- external audit/export copy mutation不是authorization authority mutation：Runtime decision仍只依据Registry custody BLOB；独立evidence verifier必须检测copy mismatch，且该authority-separation leaf不进入consume CAS；
- mint-lease replay 的零副作用按第二次claim的attempt-local增量计算：`mint_leases_claimed=0`、state/version不变、active capability=0，但必须有一个durable `authorization_mint_lease_claim_rejected` event和可关联terminal A1 rejection；
- capability-preparation replay按每个loser的attempt-local增量计算：`successful_capability_preparation_cas_events=0`、`pending_capabilities_prepared=0`、state/version不变；winner及其pending row不计入loser增量；
- catchable capability-preparation failure是统一零副作用向量的明确状态收口例外：所有实际manifest subleaf均要求`successful_capability_preparation_cas_events=0`、`capability_preparation_aborts=1`、`pending_capabilities_prepared=0`、preparation=aborted、active capability=0。若注入点在candidate object形成前，则`pending_capabilities_destroyed=0`且disposition=`not_created`；若在object形成后的schema/signing Gate，则destroyed=1且disposition=`candidate_destroyed_not_registered`。旧context因version变化拒绝，fresh resolver只返回spent terminal view；signed terminal rejection与controller terminal仍各为1；
- capability-activation replay 的零副作用按第二次activation的attempt-local增量计算：首次合法activation不计入；第二次`capability_activations=0`、active capability ID/version不变，并有durable rejected event与terminal A1 rejection；
- post-lease crash recovery probes按fresh-process拒绝attempt计算：不允许new preparation/activation CAS、pending/active row或handle issuance；crash前已commit的lease/preparation事实不计入该拒绝增量，且durable state不得伪造为aborted；
- terminal audit event 必须记录真实到达状态，不能为了满足“1”而伪造未发生的 Registry/capability事件；
- `R2P-REQ-AUDIT-FAILURE` 使用 §4.3 的明确例外：`signed_runtime_terminal_rejection_events=0`、`controller_terminal_events=1`；post-CAS/pre-lease vector允许且要求 `successful_consumption_cas_events=1`、`consumption_events_created=1`、`mint_eligibility_aborts=1`、consumption state=spent、eligibility=aborted，但 `successful_mint_lease_cas_events=0`、active capability=0；旧context与fresh-resolve retry均拒绝。
- post-preparation/pre-activation audit-failure vector 允许且要求`successful_consumption_cas_events=1`、`consumption_events_created=1`、`successful_mint_lease_cas_events=1`、`mint_leases_claimed=1`、`successful_capability_preparation_cas_events=1`、`pending_capabilities_prepared=1`、`pending_capabilities_destroyed=1`、`capability_activation_aborts=1`、consumption state=spent、preparation=prepared、activation=aborted、`successful_capability_activation_cas_events=0`、active capability=0、retry=0。
- manifest-declared crash leaf按上述§4.3 crash例外允许crash-point之后`signed_runtime_terminal_rejection_events=0`，但`controller_terminal_events=1`，并必须由restart operation另产生正常signed terminal rejection + controller terminal；不得把普通unexpected crash纳入此例外。

### 8.5 Manifest／runner 实际枚举

计划不声明 `N=10`、`N=197` 或任何测试总数。未来必须：

1. 从冻结的 R2 requirement manifest 动态展开 leaf；
2. 在执行前冻结 manifest identity/digest；
3. runner 实际 discover、execute并写 terminal ledger；
4. aggregate 只从 manifest和terminal artifacts机械计算数量；
5. result 报告不得使用手工预填数。

Manifest 还必须为 leaf 内的 consume/replay/concurrency operations 物化独立 operation records。设冻结 manifest 实际展开的 consume operation count 为 `M`，aggregate 必须满足：

```yaml
expected_consume_operations: M
observed_consume_operations: M
terminal_consume_operations: M
evidence_complete_consume_operations: M
duplicate_consume_operation_ids: 0
```

`M` 与 `N` 一样只能由未来冻结 manifest／runner 实际枚举，本文不预填数值。Replay 的首次消费和第二次拒绝、concurrent CAS 的每个 contender都必须分别进入上述闭合等式。

Registration、consume、revoke、expire、eligibility-abort、mint-lease、capability-preparation/abort、capability-activation/abort和Registry-side rejection都使用独立`registry_operation_id`。设冻结manifest实际展开的Registry operation count为`K`，aggregate还必须满足：

```yaml
expected_registry_operations: K
observed_registry_operations: K
terminal_registry_operations: K
evidence_complete_registry_operations: K
duplicate_registry_operation_ids: 0
```

`K`也只允许由未来manifest/runner实际枚举。Mint-lease、preparation、activation各自的首次accepted与后续rejected attempts必须使用不同Registry operation IDs；每个expected Registry operation都必须关联durable event。Malformed/unknown-version等在调用Registry前终止的请求不计入`K`，但必须进入`T`的controller-only terminal闭包。

Frozen manifest还必须显式枚举所需controller terminal records；普通单operation leaf通常物化一条，replay／concurrency／failure-window等多operation leaf按其独立terminal outcome展开。设该动态记录数为 `T`，aggregate必须满足：

```yaml
expected_controller_terminal_records: T
observed_controller_terminal_records: T
terminal_controller_terminal_records: T
schema_valid_controller_terminal_records: T
canonicalization_valid_controller_terminal_records: T
signature_valid_controller_terminal_records: T
chain_valid_controller_terminal_records: T
manifest_correlated_controller_terminal_records: T
registry_truth_verified_controller_terminal_records: T
evidence_complete_controller_terminal_records: T
duplicate_controller_terminal_ids: 0
controller_sequence_gaps: 0
controller_sequence_duplicates: 0
controller_chain_forks: 0
controller_chain_genesis_count: 1
controller_chain_scope_count: 1
controller_mid_suite_key_rotations: 0
```

`T` 不等于预填的leaf数，也不在本计划中给值；它只能由future frozen manifest根据leaf／operation topology枚举。`registry_truth_verified` 对pre-registration rejection表示已独立确认“无Registry row/event”，不是伪造一个Registry对象。任一controller record缺失、schema/signature/chain无效、无法关联manifest，或与Registry authoritative state/event／verified absence不符，都使对应leaf不具备PASS资格。

设未来实际 manifest leaf count 为 `N`，R2-P execution PASS 必须满足：

```yaml
manifest_leaf_count: N
runner_discovered: N
runner_executed: N
terminal_results: N
evidence_complete: N
passed: N
failed: 0
skipped: 0
unknown: 0
timed_out: 0
duplicate_case_ids: 0
duplicate_attempt_ids: 0
unauthorized_cross_case_authorization_reuse: 0
unauthorized_cross_case_nonce_reuse: 0
```

这里的 `N` 是未来 aggregate 从 artifact 读取的变量，不是本计划预先声明的数字。

### 8.6 R2 execution 最终 PASS 条件

未来只有以下全部成立，才可标记独立的 R2-P implementation result PASS：

- V2 schema、Registry identity schema 与 unique loader 已实际实现；
- 所有 V2 artifact 先 validate 后 register；
- self-digest 字段与 legacy alias 100% 拒绝；
- exact bytes digest／size／schema／Profile／run/source/scope binding 100% 匹配；
- typed validated context 已替代 caller dict；
- one-time/nonce/expiry/revocation/consume replay、eligibility burn、preparation abort、mint-lease/preparation/activation replay及post-crash handle-loss拒绝状态机完整；
- manifest/runner闭合等式成立，所有 mandatory leaf PASS；
- A1 terminal audit 完整；
- broker source read、bounded delivery、Candidate、model、business output均未执行；
- result 明确 `A1 / non-certified / A2 NOT_PROVIDED`；
- 独立 reviewer确认无 V1 fallback、Profile promotion或R3/R4 scope creep。

R2-P PASS 也只关闭 Authorization Schema V2 工作包；它不等于 Portable Runtime PASS，不授权 Candidate Analysis。

## 9. 风险、阻断与处置

| 风险 | 影响 | 计划处置 |
| --- | --- | --- |
| 把 external digest 再注入 claims dict | 重现 artifact/schema/consumer 三视图问题 | typed context 分层；artifact model 不允许 identity字段 |
| 同时接受 V1/V2 alias | downgrade／ambiguous parse | 无 compatibility fallback；legacy version fail closed |
| 把 artifact approval state 与 consumption state混合 | mutable state 回写、replay | `authorization_state` 与 Registry `consumption_state` 分离 |
| post-consume failure仍保留mint资格 | failed attempt可继续claim lease | opaque one-shot handle + durable eligibility abort + no resolver reconstruction |
| post-lease/prepared context可重复prepare/activate | 一个authorization产生多个pending/active capabilities | domain-separated handles + preparation/activation CAS + unique rows + stage-specific contexts |
| lease/preparation后crash可重建context | fresh process绕过no-retry | handle明文never persisted/resolved；durable stranded state真实记录；restart negative probes |
| 多 range 数组静默扩大 authority | 范围越权 | V2 当前恰好一个 range；多 range需新 revision |
| Portable deny policy 被误写为 OS capability absence | 伪造 A2/A3 | 强制 logical claim措辞与A2 NOT_PROVIDED |
| Portable artifact 被 Hardened 聚合 | certification污染 | Profile进入artifact/registry/capability/event；cross-profile verifier拒绝 |
| Signed event在CAS后失败 | state与A1 audit出现crash window | state保持spent、禁止mint、durable Registry event + BLOCKED terminal收口 |
| R2顺便修改closure/E2E | 原子范围失控 | 闭合文件allowlist；范围外需求触发停止与重新授权 |
| 测试数字先写后跑 | phantom success | manifest/runner实际枚举，N只来自aggregate |

如果无法在未来 R2 execution 中同时实现 exact-bytes validation、external identity binding、typed context、精确 state/replay 和 terminal A1 audit，正确结果是：

```text
BLOCKED_PORTABLE_AUTHORIZATION_SCHEMA_V2_IMPLEMENTATION_FAILED
```

不得以 schema 文件“已生成”、旧 CAS 测试已通过或 Portable 不要求 A2 为由制造 PASS。

## 10. 与当前状态的关系

### 10.1 历史状态不变

本 Plan 完成后：

- Phase 2-G 仍为 `BLOCKED_RUNTIME_CAPABILITY_PROTOTYPE_FAILED`；
- Phase 2-G-R 仍为 `PASS_REPAIR_PLAN_ONLY`；
- Phase 2-G-R1 仍为 `BLOCKED_OS_OBSERVABILITY_INSUFFICIENT`；
- Phase 2-G-R1D 的决策仍为 `ADOPT_DUAL_ASSURANCE_PROFILES`；
- R1 preflight 中历史 `allow_r2=false` 保持原值，不回写为 true；
- `RCPTS-20260811-002` 的 99 PASS／98 FAIL、181 grants与所有 terminal evidence不重分类；
- Run 002 保持 `invalid_reserved / not_authorized / not_executed / non-reusable`；
- Candidate Analysis 继续 blocked。

### 10.2 新 Profile-qualified 路线

本 Plan 只记录：

```yaml
legacy_single_a3_route_allow_r2: false
legacy_allow_r2_history_changed: false

portable_r2_replanning_completed: true
portable_r2_execution_authorized: false
portable_r2_execution_requires_new_independent_authorization: true
```

这两个字段描述不同路线，不构成历史改写。只有获得新的独立 R2 execution authorization，才允许按 §7 allowlist 实施。

### 10.3 Candidate Analysis 仍然 blocked

即使未来 R2-P implementation PASS，Candidate Analysis 仍必须等待：

1. R3-P frozen execution snapshot closure PASS；
2. 全新 R4-P synthetic A1 E2E 达到 `PASS_PORTABLE_DEVELOPMENT_A1_NONCERTIFIED`；
3. 新 Candidate Plan、fresh run ID、Profile-bound authorization、snapshot和provenance获批；
4. Candidate 输出持续标记 Portable／A1／non-certified。

现有 Run 002 不得复用或解锁。

## 11. 本阶段最终状态与边界终检

本文件完整定义了 Portable Authorization Schema V2 的问题基线、canonical fields、摘要分责、A1合同、Hardened兼容、fail-closed migration、atomic scope和未来 deterministic acceptance。因而本计划阶段的最终状态为：

```text
PASS_PORTABLE_R2_PLAN_ONLY
```

该状态只表示计划完成，不表示 R2 已执行、Schema V2 已创建或 Runtime 已通过。

```yaml
phase: "Phase 2-G-R2P"
final_status: "PASS_PORTABLE_R2_PLAN_ONLY"
current_effect: "planning_only"

assurance_profile: "CTDE-PORTABLE-DEV-1"
future_minimum_evidence_level: "A1"
certified: false
portable_runtime_passed: false
hardened_runtime_passed: false

authorization_schema_v2_entity_created: false
authorization_registry_v2_entity_created: false
r2_executed: false
r3_executed: false
r4_executed: false
runtime_tests_executed: 0
r2_execution_authorized_by_this_plan: false
r2_execution_requires_new_independent_authorization: true

historical_phase_2g_status: "BLOCKED_RUNTIME_CAPABILITY_PROTOTYPE_FAILED"
historical_phase_2g_changed: false
historical_r1_status: "BLOCKED_OS_OBSERVABILITY_INSUFFICIENT"
historical_r1_changed: false
historical_allow_r2: false
historical_allow_r2_changed: false
old_suite_promoted: false
candidate_analysis_currently_blocked: true

created_files:
  - "PORTABLE_AUTHORIZATION_SCHEMA_V2_PLAN.md"
modified_existing_files: []

controller_a1_action_ledger:
  runtime_prototype_files_modified: 0
  runtime_tests_executed: 0
  candidate_runs_executed: 0
  model_invocations: 0
  english_tei_content_reads: 0
  greek_tei_content_reads: 0
  business_outputs_created: 0
  story_structure_yaml_created: false
  character_outputs_created: 0
  event_outputs_created: 0
  theme_outputs_created: 0
  adaptation_or_script_outputs_created: 0
  r3_executed: 0
  r4_executed: 0

a2_os_verified_counts:
  status: "NOT_PROVIDED"
  runtime_modifications: null
  runtime_tests: null
  candidate_runs: null
  model_invocations: null
  english_tei_reads: null
  greek_tei_reads: null
  business_outputs: null
```

本阶段 controller A1 ledger 记录禁止动作均未执行；由于当前环境 qualification-wide A2 不成立，本文件不把这些 A1 数值冒充为独立 OS-verified counts。
