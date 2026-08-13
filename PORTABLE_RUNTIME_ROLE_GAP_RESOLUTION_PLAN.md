# Classic-to-Drama Engine：Portable Runtime Role Gap Resolution Plan

> 项目：Classic-to-Drama Engine  
> 阶段：Phase 2-G-R3G  
> 文档类型：Portable Runtime Role Gap 识别、分类、依赖与原子修复排序计划  
> 日期：2026-08-11  
> 最终状态：`PASS_PORTABLE_RUNTIME_ROLE_GAP_RESOLUTION_PLAN`  
> 当前效力：`planning_only / runtime_unchanged / tests_not_executed / r3_not_authorized`  
> 目标 Profile：`CTDE-PORTABLE-DEV-1`  
> 最高可声明证据：`A1 runtime logical evidence only`  
> 认证状态：`Portable / Development / non-certified`  
> Candidate Analysis：`BLOCKED`

## 0. 最终结论

本计划从 `PORTABLE_RUNTIME_TRANSITIVE_CLOSURE_PLAN.md` §3.3 原样恢复全部七个 formal runtime role gap，再以当前真实 Runtime 文件逐项复核。七项均保留，未按记忆新增、改名或静默删除。

复核结论不是“七项都必须在 R3 前实现”，但也不改写当前 R3P 的 fail-closed Gate：

- 在当前仍有效的 R3P 下，七项全部属于 `required_runtime_role_gaps`，因此七项全部继续阻断当前 R3；本计划不授权绕过该 Gate。
- 经 profile/stage adjudication，唯一需要在 fresh R3 replan 之前实际修复的 gap 是 `R3G-07-IMMUTABLE-PUBLIC-TRUST-KEY-STATUS`；没有独立、可冻结的 public-key/status identity 时，component freeze 无法绑定实际签名信任边界。
- `R3G-01/02/06` 是 future Portable R4 suite control-plane 职责；`R3G-05` 的 Portable logical write-monitor 职责只有在 R4 引入 publisher/output path 后才有完整被监测对象；它们均不得提前进入当前 R3。
- `R3G-03` parser scope 与 `R3G-04` discard-only/no-call gateway 的 R3P 现状描述被当前真实代码部分反证，故保留为 `stale_gap_candidate`，而不是删除。该标记只表示“only-in-legacy-runner”的事实描述可能过时，不表示 gap 已获正式解除；当前 R3P 仍将二者计为 active blockers。当前嵌入式 A1 逻辑能否充当正式 role identity，必须由 fresh R3 replan 明确裁决；更强的独立 mediation 只能在 R4P 中决定。
- 完整 OS write-set、syscall/process attribution、ptrace/strace/fanotify/eBPF 与 A2/A3 仍是 Hardened-only；不进入 Portable R3 re-entry Gate。
- 当前未发现 Authorization Schema V2 的 semantic regression。R2 历史结果保持 `PASS_PORTABLE_AUTHORIZATION_SCHEMA_V2_IMPLEMENTED`，16 个 R2 implementation assets 全部只读。

```yaml
phase: "Phase 2-G-R3G"
final_status: "PASS_PORTABLE_RUNTIME_ROLE_GAP_RESOLUTION_PLAN"

total_role_gaps: 7
gap_count: 7
confirmed_current_gaps: 7
stale_gap_candidates: 2
stale_gap_candidates_resolved: 0
current_r3p_active_gap_count: 7
blocks_r3_under_current_r3p_count: 7
r3_precondition_gap_count: 1
deferred_to_r4_count: 6
hardened_only_count: 0
hardened_only_secondary_aspect_count: 1
dependency_edges_count: 8
repair_phase_count: 2
defined_followup_scope_phase_count: 2
implementation_repair_phase_count: 0
scope_requires_additional_audit_count: 5
r2_semantic_regression_count: 0

r3_replan_required: true
r3_execution_authorized: false
r4_execution_authorized: false
candidate_execution_authorized: false
```

`confirmed_current_gaps=7` 与 `stale_gap_candidates=2` 是重叠口径：七项均仍是当前 R3P 的 formal active gaps，其中 R3G-03/04 另有事实描述可能过时的证据；在 fresh replan 正式裁决前，两项均未被视为 resolved。`repair_phase_count=2` 与 `defined_followup_scope_phase_count=2` 只统计当前证据足以给出精确文件范围的两个后续 planning/audit 阶段：R3G1 与 R3G2。`implementation_repair_phase_count=0`，因为真正 implementation 和独立验证阶段必须由 R3G2 以 exact paths 冻结后另行授权；本计划不以占位路径冒充可执行白名单。

## 1. 正式依据与只读基线

### 1.1 正式依据

| 文件 | 当前 SHA-256 | 本计划用途 |
| --- | --- | --- |
| `PORTABLE_RUNTIME_TRANSITIVE_CLOSURE_PLAN.md` | `f8ca07eaee1fff534e97bf4a0d037ba73a3c1838107e132f7c072b1fe05b39f5` | 七项 gap 的唯一恢复来源、R3 写范围、formal-role Gate、R4/Hardened deferred 边界 |
| `RUNTIME_CAPABILITY_PROTOTYPE_RESULT.md` | `6811bcc4ef0efcaee89013648dd0bb06bbaca154625f3dc47bdfa0f295851753` | Prototype 的真实 blocker、已有组件与 legacy evidence 边界 |
| `RUNTIME_CAPABILITY_REPAIR_PLAN.md` | `a2c52dbaecf3956cf4a2189abe5401f269d255e8099d3345985619be25be4213` | closure roots/node types、public trust、R3 acceptance 与 R4 E2E 职责 |
| `RUNTIME_ASSURANCE_PROFILE_DECISION.md` | `57471c85c57946f6ceb6da288301cc802533b09c137bfbe8e6e247dad57206e2` | Portable A1 与 Hardened A3 的互斥 claim 边界 |
| `PORTABLE_AUTHORIZATION_SCHEMA_V2_PLAN.md` | `32513cdb2c004ea91c7d7208eb3a40901934dc80440af048b84701facf1bdbe9` | R2 原子白名单、纯 binding probe 与 R3/R4 deferred 边界 |
| `PORTABLE_AUTHORIZATION_SCHEMA_V2_IMPLEMENTATION_RESULT.md` | `b47c7280880af70325a5e5c45426951567390441ad4cd61465724fbb8eabcd06` | R2 实际实现、51/51 PASS、immutable upstream assets 与零 source-I/O 边界 |
| `CANDIDATE_EXECUTION_CONTRACT_REPAIR.md` | `12ceb01cab4901cb2b7472b1b56f93750a43cb8c28b5f0c9ab89acf3ad4fe7bd` | signed-object key-status、parser/gateway/write domains 与 future Candidate/R4 组件合同 |

### 1.2 Runtime Prototype 当前状态

本阶段未运行 Runtime 或 Python import；只使用目录枚举、文本读取和 SHA-256 复核。

```yaml
runtime_root: "runtime_capability_prototype"
runtime_file_count: 3062
runtime_directory_count: 1218
runtime_symlink_count: 0
runtime_content_tree_sha256_before: "820afae1806d4cec398b54193574e62e1933c2e8745dfb570d00b969bd69fe43"
authorization_schema_v2_sha256: "f1d7c2e36e0d3072624609591eb8dfc20d0e42dce6accc8e87de730ec4478e33"
r2_implementation_result_sha256: "b47c7280880af70325a5e5c45426951567390441ad4cd61465724fbb8eabcd06"
r3p_plan_sha256: "f8ca07eaee1fff534e97bf4a0d037ba73a3c1838107e132f7c072b1fe05b39f5"
```

内容树摘要算法沿用 R3P：按 Runtime-root-relative POSIX path 排序，对每个普通文件计算 SHA-256，再对 `sha256 + two spaces + relative_path + LF` 的完整排序列表计算 SHA-256。

### 1.3 Gap 恢复规则

唯一恢复 authority 是 R3P §3.3 的七项清单：

1. Portable Runtime/R4 suite manifest builder；
2. Portable Runtime/R4 suite runner；
3. parser scope；
4. model gateway；
5. write monitor；
6. Portable Runtime/R4 aggregate/report generator；
7. immutable public trust material / key-status registry。

`gap_count=7`。R3P 中的现状描述与当前源码冲突时，本计划保留原 gap ID，增加 `stale_gap_candidate` 证据，不改写 R3P 历史文本，也不在 fresh replan 前解除其 formal blocker。

本文依赖图使用以下唯一 short-ID alias；`gap_id` 的 authority 仍是右栏 long-form 值：

| gap_short_id | gap_id |
| --- | --- |
| `R3G-01` | `R3G-01-PORTABLE-R4-SUITE-MANIFEST-BUILDER` |
| `R3G-02` | `R3G-02-PORTABLE-R4-SUITE-RUNNER` |
| `R3G-03` | `R3G-03-BOUNDED-PARSER-SCOPE` |
| `R3G-04` | `R3G-04-DISCARD-ONLY-MODEL-GATEWAY` |
| `R3G-05` | `R3G-05-PORTABLE-LOGICAL-WRITE-MONITOR` |
| `R3G-06` | `R3G-06-PORTABLE-R4-AGGREGATE-REPORT-GENERATOR` |
| `R3G-07` | `R3G-07-IMMUTABLE-PUBLIC-TRUST-KEY-STATUS` |

## 2. 唯一分类规则

每项只能有一个 primary classification；secondary classification 仅描述附带问题，不改变主集合计数。

| Code | Primary classification | 本计划解释 |
| --- | --- | --- |
| A | `missing_runtime_implementation` | 所需 Runtime 角色完全没有实现 |
| B | `missing_runtime_binding` | 实现存在，但没有进入实际 Runtime 调用/身份链 |
| C | `missing_contract_or_schema_binding` | 合同/schema 与实现或 execution identity 未绑定 |
| D | `missing_deterministic_verifier` | 没有可独立、确定性验证该职责的 verifier |
| E | `missing_freeze_identity` | 能力或配置无法形成稳定、可复核的 component identity |
| F | `test_only_gap` | 仅影响测试/control，且生产/Portable runtime 不依赖 |
| G | `deferred_to_R4` | 职责属于 fresh Portable synthetic E2E 或其 control plane |
| H | `hardened_only` | 只服务 A2/A3、OS observability 或 certification |
| I | `other_confirmed_runtime_gap` | 经证据确认且不属于 A–H 的 Runtime 缺口 |

本计划选择：`R3G-01..06 = G`，`R3G-07 = E`。`R3G-03/04` 同时是 stale candidates：primary `G` 表示若未来要求强化或拆成独立组件，唯一归属是 R4；它不表示当前嵌入式逻辑不存在。

## 3. 七项 role gap 逐项分析

### 3.1 `R3G-01-PORTABLE-R4-SUITE-MANIFEST-BUILDER`

```yaml
gap_id: "R3G-01-PORTABLE-R4-SUITE-MANIFEST-BUILDER"
gap_short_id: "R3G-01"
runtime_role: "Portable Runtime/R4 suite manifest builder"
primary_classification: "G.deferred_to_R4"
secondary_classifications:
  - "C.missing_contract_or_schema_binding"
blocks_r3_under_current_r3p: true
requires_pre_r3_repair_after_adjudication: false
stale_gap_candidate: false
scope_status: "scope_requires_additional_audit"
repair_phase: "future Phase 2-G-R4P"
```

- **Expected responsibility**：根据 Portable R4-P requirement contract 生成 fresh synthetic E2E manifest，冻结 Profile、leaf identity、组件/信任身份与测试范围；测试数量由 manifest 实际展开。
- **Current implementation state**：没有 Portable/R4 counterpart。现有 builder 均绑定已完成或 legacy suite。
- **Current real files**：
  - `runtime_capability_prototype/runtime/build_manifest.py` — `78a206e28365cfe7d6caf677ef818ddaddb7db2b920cac535ea84d206205213d`；硬编码 legacy `RCPTS-20260811-002`。
  - `runtime_capability_prototype/runtime/build_r2_portable_manifest.py` — `8f75e72d33d3c1cabf2bce866eac9fb44aec5775c68127576073ce510498828c`；仅服务 R2 V2 authorization tests。
- **Missing capability**：R4-P 的正式 requirement source、manifest schema、leaf expansion 与 Profile/public-trust/component binding 尚未设计和冻结。
- **Evidence / why repair is deferred while the current R3P still blocks**：R3P §3.3/§16 让该 gap 继续阻断当前 R3；Repair Plan §4.2/§4.6 把 suite builder列为最终 Runtime snapshot root。但 R3P §15.3 又明确把 R4-specific builder/schema/policy 延后，并要求这些 bytes 出现后再 fresh R3 refresh。因此 fresh replan必须显式作stage-scoped deferred disposition；当前 R3 自己的 `build_r3_portable_test_manifest.py` 是 closure-test builder，不得冒充R4 builder，也不得直接从旧Gate删除本项。
- **Contract reference**：R3P §3.3、§15.3；Repair Plan §4.2、§4.6；Assurance ADR §8.1。

### 3.2 `R3G-02-PORTABLE-R4-SUITE-RUNNER`

```yaml
gap_id: "R3G-02-PORTABLE-R4-SUITE-RUNNER"
gap_short_id: "R3G-02"
runtime_role: "Portable Runtime/R4 suite runner"
primary_classification: "G.deferred_to_R4"
secondary_classifications:
  - "B.missing_runtime_binding"
blocks_r3_under_current_r3p: true
requires_pre_r3_repair_after_adjudication: false
stale_gap_candidate: false
scope_status: "scope_requires_additional_audit"
repair_phase: "future Phase 2-G-R4P"
```

- **Expected responsibility**：只执行 future frozen R4-P manifest，组合 fresh authorization、broker、reader、parser、discard-only gateway、logical write monitor、formal loader与A1 audit；从实际 terminal records聚合 counts。
- **Current implementation state**：无 Portable/R4 runner。现有 runner 分别绑定 legacy E2E 与 R2 authorization-only tests；future R3 runner只负责 closure tests。
- **Current real files**：
  - `runtime_capability_prototype/runtime/run_suite.py` — `caf32bdb9c49ba78ee1671d41b62bc9eb8297343624ceb7afd562443a6794749`；legacy 197-leaf runner，会重编 probe与写 legacy control artifacts。
  - `runtime_capability_prototype/runtime/run_r2_portable.py` — `ec1c86ed0f89a76b497dc9d48ff4fc092c5ff1e78d84fb3dff407a9040a4ca75`；R2 51-leaf runner。
- **Missing capability**：R4-P lifecycle、fresh suite identity、terminal/evidence/resume contract 与 component orchestration尚未确定。
- **Evidence / why repair is deferred while the current R3P still blocks**：R3P §3.3/§16当前仍把本项计为blocker；§15.3同时将 R4 runner/evidence全部 deferred。R3 closure runner只验证closure，不能执行source-range E2E。Fresh replan必须批准stage-scoped deferred disposition；R4 runner实现后必须纳入新的fresh R3 refresh，而不是提前放进当前R3。
- **Contract reference**：R3P §3.3、§3.2 rule 7、§15.2–15.3；Repair Plan §6–7；Assurance ADR §8.1。

### 3.3 `R3G-03-BOUNDED-PARSER-SCOPE`

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
```

- **Expected responsibility**：在 bounded delivery 内检查 Book、Card、Paragraph、DTD/entity/external reference、namespace和non-recovery条件，生成可关联的 parser-scope logical result。
- **R3P recorded state**：R3P §3.3称“只有 legacy `run_suite.py` 内 synthetic harness logic，没有独立 production callable/file”。
- **Current real files / actual call chain**：
  - `runtime_capability_prototype/native/consumer_probe.c` — `f4057def41b265723538eb28aa7a9e3172536d44de5a54d276fedf3df1aad3fb`；真实执行 BOOK/Card/Paragraph/DTD/entity/namespace marker判定并产生 `parser_status`。
  - `runtime_capability_prototype/bin/consumer_probe` — `f1f4849e078169d14ae18c91a5469b171534479dd8255de359f588ca1b475c80`；由 supervisor 实际执行的 frozen binary候选。
  - `runtime_capability_prototype/runtime/ctde_runtime/sandbox.py` — `c60aca6b25e933a12e37862c55df8ae8472dca55f03b0ceb871cbcd8eaf8a9d1`；`SandboxSupervisor.run`启动 probe并返回 parser字段。
  - `runtime_capability_prototype/runtime/ctde_runtime/bounded_reader.py` — `65c8f0a3af625c505fcdc05f7a754075e4829d2183931d71fa8c4dfdbf46f68c`；写入 `parser_scope_result`并对非-PASS parser状态 fail closed。
  - `runtime_capability_prototype/runtime/ctde_runtime/read_audit.py` — `b5c8a9210c4f9f295351b32e3f2a5e310ad0531720ff886a9d84385ec1ab6b4d`；校验 parser事件的 Book/Card/Paragraph范围。
- **Stale-gap-candidate evidence**：formal role并未要求必须是单独 Python module。上述 executable→supervisor→bounded reader→audit 是实际可达链，且 `SandboxSupervisor.run`、`BoundedReader.consume`、`ReadAuditAggregator` 已在 R3P approved callable roots 中。故“仅在 legacy runner”这一事实描述可能过时；但 Candidate execution snapshot另有 `fragment_parser`、`parser_scope_monitor` component identities，当前链是否足以承担该正式身份仍须fresh replan裁决。
- **Residual missing capability**：是否为 R4/Candidate另建独立 parser component、真实 XML fragment parser与独立 component ID，必须由 future R4P/Candidate contract决定；本阶段不能为追求“独立文件”修改 R2-protected `bounded_reader.py`。
- **Why no pre-replan implementation is authorized while the current R3P still blocks**：旧R3P在fresh adjudication前仍让本项阻断R3。Fresh R3 replan只能在逐字节冻结该嵌入式链并明确其formal role identity后，才可把future strengthening deferred；R3本体不执行parser E2E。
- **Contract reference**：R3P §3.2–3.3、§10.3、§15.2；Repair Plan §6.2 steps 10–12；Assurance ADR §4.2；Candidate Contract §4.3、§4.5。

### 3.4 `R3G-04-DISCARD-ONLY-MODEL-GATEWAY`

```yaml
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
scope_status: "current_logic_paths_resolved; formal_identity_requires_fresh_replan; future_strengthening_deferred_to_R4P"
repair_phase: null
```

- **Expected responsibility**：Portable R4-P 的 gateway只记录接受的 synthetic scope、拒绝范围外 injection，保持实际模型调用为0；未来 Candidate gateway才负责真实 model-input mediation。
- **R3P recorded state**：R3P §3.3称逻辑只在 legacy runner、没有独立 callable/file。
- **Current real files**：
  - `runtime_capability_prototype/runtime/ctde_runtime/bounded_reader.py` — `65c8f0a3af625c505fcdc05f7a754075e4829d2183931d71fa8c4dfdbf46f68c`；在 parser PASS后发出 `gateway_scope_result`、记录 `model_invocations=0`，对 Book 2 injection fail closed。
  - `runtime_capability_prototype/runtime/ctde_runtime/read_audit.py` — `b5c8a9210c4f9f295351b32e3f2a5e310ad0531720ff886a9d84385ec1ab6b4d`；校验 gateway Book2/Greek/model counters。
  - `runtime_capability_prototype/runtime/run_suite.py` — `caf32bdb9c49ba78ee1671d41b62bc9eb8297343624ceb7afd562443a6794749`；仅提供 legacy injection vector/驱动，不是唯一 gateway logic所在地。
- **Stale-gap-candidate evidence**：Repair Plan §6.2 对 R4 discard-only gateway 的最低描述正是“只记录scope，模型调用保持0”；当前 approved `BoundedReader.consume` 已有这一嵌入式行为。因此“仅 legacy runner”的描述可能过时。但 Candidate execution snapshot另有 `model_input_gateway` component identity，当前没有独立payload handoff/mediation boundary；candidate标记不等于role gap已解除。
- **Residual missing capability**：当前没有独立输入裁剪/丢弃 callable、独立 gateway component identity或真实 Candidate model-input mediation。若 R4P决定独立化，必须新规划；R3严禁模型集成/调用。
- **Why no pre-replan implementation is authorized while the current R3P still blocks**：旧R3P仍把本项计为blocker。Fresh replan必须先明确嵌入式gateway bytes、事件/audit边能否承担minimal A1 role identity，再可将独立mediation deferred到R4/Candidate；当前closure不得自行删除本项。
- **Contract reference**：R3P §3.3、§15.2–15.3；Repair Plan §6.2 step 12；Assurance ADR §4.2；Candidate Contract §4.5、§4.6。

### 3.5 `R3G-05-PORTABLE-LOGICAL-WRITE-MONITOR`

```yaml
gap_id: "R3G-05-PORTABLE-LOGICAL-WRITE-MONITOR"
gap_short_id: "R3G-05"
runtime_role: "write monitor"
primary_classification: "G.deferred_to_R4"
secondary_classifications:
  - "A.missing_runtime_implementation"
  - "H.complete_os_write_observation_is_hardened_only"
blocks_r3_under_current_r3p: true
requires_pre_r3_repair_after_adjudication: false
stale_gap_candidate: false
scope_status: "scope_requires_additional_audit"
repair_phase: "future Phase 2-G-R4P"
```

- **Expected responsibility**：Portable A1层面记录由 R4 controller/publisher受控的 attempted/allowed/denied writes、artifact presence和路径allowlist；terminal closure将该logical evidence与formal-loader/result关联。
- **Current implementation state**：没有独立 Portable logical monitor。legacy harness根据自身counter生成一条自报事件；audit aggregator只消费它。
- **Current real files**：
  - `runtime_capability_prototype/runtime/run_suite.py` — `caf32bdb9c49ba78ee1671d41b62bc9eb8297343624ceb7afd562443a6794749`；`CaseHarness._ensure_write_evidence`产生 legacy `write_monitor_complete`。
  - `runtime_capability_prototype/runtime/ctde_runtime/read_audit.py` — `b5c8a9210c4f9f295351b32e3f2a5e310ad0531720ff886a9d84385ec1ab6b4d`；只验证 closure-domain事件，不实施monitor。
  - `runtime_capability_prototype/runtime/ctde_runtime/sandbox.py` — `c60aca6b25e933a12e37862c55df8ae8472dca55f03b0ceb871cbcd8eaf8a9d1`；对子进程执行logical deny检查，但不是完整publisher/workspace monitor。
  - `runtime_capability_prototype/runtime/verify_trace.py` — `d8732e7e788b2ababbc7dac14c09e772daab3e96287704d77022c68e2568bc9d`；legacy strace/A2 verifier，只能作为Hardened evidence，不能替代Portable logical monitor。
- **Missing capability**：R4-P尚无publisher/output/attempt lifecycle，因此不能定义完整的Portable logical write event producer、path allowlist和terminal binding。
- **Why repair is deferred while the current R3P still blocks**：旧R3P仍把本项计为blocker；fresh replan必须明确其stage-scoped R4 disposition。R3不创建业务输出、不执行R4 writer，只冻结自身closed write ledger；R4 logical monitor bytes出现后必须fresh R3 refresh。
- **Hardened boundary**：完整file-write/open/rename/link/unlink syscall set、不可篡改OS observer与零旁路proof属于Hardened A2/A3，`hardened_only_count`不增加，因为它是该gap的secondary aspect，而非独立primary gap。
- **Contract reference**：R3P §3.3、§15.2–15.3；Repair Plan §5.4–5.5、§6.2；Assurance ADR §4.2、§9；Candidate Contract §4.5–4.6。

### 3.6 `R3G-06-PORTABLE-R4-AGGREGATE-REPORT-GENERATOR`

```yaml
gap_id: "R3G-06-PORTABLE-R4-AGGREGATE-REPORT-GENERATOR"
gap_short_id: "R3G-06"
runtime_role: "Portable Runtime/R4 aggregate/report generator"
primary_classification: "G.deferred_to_R4"
secondary_classifications:
  - "C.missing_contract_or_schema_binding"
blocks_r3_under_current_r3p: true
requires_pre_r3_repair_after_adjudication: false
stale_gap_candidate: false
scope_status: "scope_requires_additional_audit"
repair_phase: "future Phase 2-G-R4P"
```

- **Expected responsibility**：从 frozen R4 manifest、terminal/evidence records机械计算 discovered/executed/evidence-complete/pass/fail/skip/unknown/timeout，生成 Profile-qualified aggregate和无文学内容report。
- **Current implementation state**：只有 legacy、R2-specific与future R3-specific generator；没有 R4-P generator。
- **Current real files**：
  - `runtime_capability_prototype/runtime/run_suite.py` — `caf32bdb9c49ba78ee1671d41b62bc9eb8297343624ceb7afd562443a6794749`；包含 legacy `aggregate_execution`、`finalize_suite` 与内联报告。
  - `runtime_capability_prototype/runtime/run_r2_portable.py` — `ec1c86ed0f89a76b497dc9d48ff4fc092c5ff1e78d84fb3dff407a9040a4ca75`；仅生成 R2 aggregate。
- **Missing capability**：R4 result schema、evidence completeness、terminal prefix与 Portable A1 claim set尚未由 R4P定义。
- **Why repair is deferred while the current R3P still blocks**：旧R3P仍把本项计为blocker，fresh replan必须明确其stage-scoped R4 disposition。R3P预留的 `build_r3_portable_result.py`只生成closure结果，不能冒充R4 generator；R4 generator实现后需fresh R3 refresh。
- **Contract reference**：R3P §3.3、§15.3；Repair Plan §4.2、§4.6、§7.2；Assurance ADR §8.1。

### 3.7 `R3G-07-IMMUTABLE-PUBLIC-TRUST-KEY-STATUS`

```yaml
gap_id: "R3G-07-IMMUTABLE-PUBLIC-TRUST-KEY-STATUS"
gap_short_id: "R3G-07"
runtime_role: "immutable public trust material / key-status registry"
primary_classification: "E.missing_freeze_identity"
secondary_classifications:
  - "C.missing_contract_or_schema_binding"
  - "B.missing_runtime_binding"
blocks_r3_under_current_r3p: true
requires_pre_r3_repair_after_adjudication: true
stale_gap_candidate: false
scope_status: "scope_requires_additional_audit"
repair_phase: "Phase 2-G-R3G1, then Phase 2-G-R3G2"
```

- **Expected responsibility**：为每个实际 verifier可达信任记录冻结 `kid`、algorithm、status、trust domain、validity与exact public-key bytes digest；明确private-key custody boundary、producer authority和runtime loader/binding，并允许component freeze和execution snapshot引用同一identity。
- **Current implementation state**：只有内存类型与运行时临时key；没有独立、create-once、可复核的public trust/key-status asset、schema或loader。
- **Current real files**：
  - `runtime_capability_prototype/runtime/ctde_runtime/signing.py` — `5c41a1601b9824715d17ae416513646575006a9207dedd26bb2036336e66cc36`；定义 `KeyRecord`、`TrustStore`、`SigningKey` 和 `JWSCodec`，不加载持久 trust registry。
  - `runtime_capability_prototype/runtime/run_suite.py` — `caf32bdb9c49ba78ee1671d41b62bc9eb8297343624ceb7afd562443a6794749`；每次运行临时生成legacy keys并写suite-local snapshot。
  - `runtime_capability_prototype/runtime/run_r2_portable.py` — `ec1c86ed0f89a76b497dc9d48ff4fc092c5ff1e78d84fb3dff407a9040a4ca75`；R2 test/controller keys同样是本次suite临时identity。
  - `runtime_capability_prototype/runtime/ctde_runtime/events.py` — `808115293ec818eedd926e4ef63869a7d5f9eeb1dca26a6902c12850b4e7fd15`；实际签名/验证事件但不提供独立trust asset。
  - `runtime_capability_prototype/runtime/ctde_runtime/formal_loader.py` — `eb866084c8dc95c52b28118a2669314559d165e6b949cb0ff7edeb111c10e11d`；消费外部注入的codec，没有冻结registry identity。
- **Missing capability**：唯一schema/record/loader路径、key lifecycle、public bytes来源、test signer与verifier绑定、private-key custody/self-digest规则和producer authority均未由现有合同唯一决定。
- **Why it blocks R3**：R3P §10.3和§11要求 component freeze/execution binding覆盖实际public trust records；当前只能冻结 `signing.py`代码，不能冻结会改变签名接受语义的key/status/config。动态可变依赖不能视为frozen。
- **Why no implementation path is guessed here**：看似合理的新 schema/JSON/loader布局仍不能回答现有callers是否必须改、固定public keys如何与future signer对应、private key如何custody、validity时间如何确定。直接选路径会重现R3执行前的scope ambiguity。
- **Contract reference**：R3P §3.3、§10.3、§11；Repair Plan §4.2–4.5；Candidate Contract §4.1.1；R2 Result §10–12。

## 4. 汇总表

| gap_id | runtime_role | classification | blocks_r3 | repair_phase | dependencies | scope_status |
| --- | --- | --- | --- | --- | --- | --- |
| `R3G-01-PORTABLE-R4-SUITE-MANIFEST-BUILDER` | Portable/R4 suite manifest builder | `G.deferred_to_R4` | true under current R3P; pre-replan repair=false | future `R4P` | `R3G-07` | `scope_requires_additional_audit` |
| `R3G-02-PORTABLE-R4-SUITE-RUNNER` | Portable/R4 suite runner | `G.deferred_to_R4` | true under current R3P; pre-replan repair=false | future `R4P` | `R3G-01,R3G-04,R3G-05` | `scope_requires_additional_audit` |
| `R3G-03-BOUNDED-PARSER-SCOPE` | parser scope | `G.deferred_to_R4` | true under current R3P; pre-replan repair=false | fresh R3 role adjudication; future `R4P` strengthening | `R3G-07` | `stale_description_candidate/current_logic_paths_resolved` |
| `R3G-04-DISCARD-ONLY-MODEL-GATEWAY` | model gateway | `G.deferred_to_R4` | true under current R3P; pre-replan repair=false | fresh R3 role adjudication; future `R4P` strengthening | `R3G-03` | `stale_description_candidate/current_logic_paths_resolved` |
| `R3G-05-PORTABLE-LOGICAL-WRITE-MONITOR` | write monitor | `G.deferred_to_R4` | true under current R3P; pre-replan repair=false | future `R4P` | `R3G-07` | `scope_requires_additional_audit` |
| `R3G-06-PORTABLE-R4-AGGREGATE-REPORT-GENERATOR` | aggregate/report generator | `G.deferred_to_R4` | true under current R3P; pre-replan repair=false | future `R4P` | `R3G-02` | `scope_requires_additional_audit` |
| `R3G-07-IMMUTABLE-PUBLIC-TRUST-KEY-STATUS` | immutable public trust/key-status | `E.missing_freeze_identity` | true under current R3P; pre-replan repair=true | `R3G1 -> R3G2` | none | `scope_requires_additional_audit` |

`scope_requires_additional_audit_count=5` 的 gap-level口径为 `R3G-01,02,05,06,07`。`R3G-03/04` 当前minimal role的真实paths已解析；若 future R4P要求独立parser或gateway strengthening，其新scope由R4P另行决定，不计入当前未决审计数。

## 5. R3 precondition 与 deferred 集合

### 5.1 `r3_precondition_gap_set`

```yaml
r3_precondition_gap_set:
  - "R3G-07-IMMUTABLE-PUBLIC-TRUST-KEY-STATUS"
```

判定准则是：在fresh role adjudication之后仍不修复时，R3无法满足正式closure/freeze合同。R3G-07符合，因为public trust records直接改变签名验证语义且当前不可冻结。该集合是“fresh replan前需要实际修复”的集合，不是对当前R3P `required_runtime_role_gaps`的原地修改。

### 5.2 `deferred_gap_set`

```yaml
deferred_gap_set:
  - gap_id: "R3G-01-PORTABLE-R4-SUITE-MANIFEST-BUILDER"
    disposition: "deferred_to_R4"
  - gap_id: "R3G-02-PORTABLE-R4-SUITE-RUNNER"
    disposition: "deferred_to_R4"
  - gap_id: "R3G-03-BOUNDED-PARSER-SCOPE"
    disposition: "stale_description_candidate; formal role mapping requires fresh R3 adjudication; future strengthening deferred_to_R4"
  - gap_id: "R3G-04-DISCARD-ONLY-MODEL-GATEWAY"
    disposition: "stale_description_candidate; formal role mapping requires fresh R3 adjudication; future independent mediation deferred_to_R4"
  - gap_id: "R3G-05-PORTABLE-LOGICAL-WRITE-MONITOR"
    disposition: "portable logical role deferred_to_R4; complete OS monitor hardened_only"
  - gap_id: "R3G-06-PORTABLE-R4-AGGREGATE-REPORT-GENERATOR"
    disposition: "deferred_to_R4"
```

这些 gap 不得被写入当前 R3 implementation bundle。但在当前R3P下，它们仍是active blockers；只有fresh R3 replan按stage/profile明确批准每项deferred disposition后，才可不进入该次R3的active repair set。Future R4P完成任何新builder/runner/parser/gateway/write/aggregate bytes后，必须先执行fresh R3 refresh并获得新授权，再允许R4执行。

### 5.3 Current R3P Gate 与 fresh-replan adjudication

```yaml
current_r3p_blocking_gap_ids:
  - "R3G-01-PORTABLE-R4-SUITE-MANIFEST-BUILDER"
  - "R3G-02-PORTABLE-R4-SUITE-RUNNER"
  - "R3G-03-BOUNDED-PARSER-SCOPE"
  - "R3G-04-DISCARD-ONLY-MODEL-GATEWAY"
  - "R3G-05-PORTABLE-LOGICAL-WRITE-MONITOR"
  - "R3G-06-PORTABLE-R4-AGGREGATE-REPORT-GENERATOR"
  - "R3G-07-IMMUTABLE-PUBLIC-TRUST-KEY-STATUS"
current_r3p_blocking_gap_count: 7
fresh_replan_precondition_repair_gap_ids:
  - "R3G-07-IMMUTABLE-PUBLIC-TRUST-KEY-STATUS"
stage_scoped_deferred_to_r4_allowed_gap_ids:
  - "R3G-01-PORTABLE-R4-SUITE-MANIFEST-BUILDER"
  - "R3G-02-PORTABLE-R4-SUITE-RUNNER"
  - "R3G-05-PORTABLE-LOGICAL-WRITE-MONITOR"
  - "R3G-06-PORTABLE-R4-AGGREGATE-REPORT-GENERATOR"
minimal_embedded_role_mapping_required_gap_ids:
  - "R3G-03-BOUNDED-PARSER-SCOPE"
  - "R3G-04-DISCARD-ONLY-MODEL-GATEWAY"
minimal_embedded_role_mapping_failure_result: "BLOCKED_R3_ROLE_GAP_UNRESOLVED"
future_strengthening_deferred_to_r4_gap_ids:
  - "R3G-03-BOUNDED-PARSER-SCOPE"
  - "R3G-04-DISCARD-ONLY-MODEL-GATEWAY"
```

Fresh R3 replan必须建立stage/profile-scoped `required_runtime_roles`：保留七个gap identity及其证据，不得由builder临时删项。R3G-01/02/05/06可由fresh Plan与人工授权逐项批准stage-scoped `deferred_to_R4`；R3G-03/04则必须先验证并冻结当前minimal embedded role identity，只有future strengthening可以defer。若任一minimal mapping不成立，该gap必须重新进入pre-R3 repair set，R3 re-entry保持BLOCKED。若fresh replan没有完成上述正式reconciliation，旧R3P的七项non-zero Gate继续生效，R3仍必须BLOCKED。

### 5.4 过度保证检查

| 检查项 | 判定 |
| --- | --- |
| 与文学改编目标无关的过度保证 | 当前 R3 Gate 不要求R4 control-plane、真实model mediation或business-output monitor；未提前实现 |
| Hardened-only 要求 | complete OS write/open/process/syscall coverage继续deferred；不进入Portable前置 |
| R4 E2E 能力 | builder/runner/parser/gateway/write/aggregate均与当前R3分离 |
| A2/A3 promotion | 禁止；Portable结果始终A1/non-certified |

## 6. Gap dependency graph

### 6.1 Edge 口径

只记录 transitive-reduction 的直接语义依赖，不重复传递边。`A -> B` 表示 B 的可信身份或执行合同必须先取得 A 的产物/决定。

```text
R3G-07 -> R3G-01
R3G-07 -> R3G-03
R3G-07 -> R3G-05
R3G-03 -> R3G-04
R3G-01 -> R3G-02
R3G-04 -> R3G-02
R3G-05 -> R3G-02
R3G-02 -> R3G-06
```

解释：

- R4 manifest、parser/write signed evidence都需要已冻结的 public-trust identity；
- discard-only gateway只接受parser已批准scope；
- runner依赖manifest、gateway和write-monitor contracts；
- aggregate/report只消费runner terminal outputs。

### 6.2 Graph properties

```yaml
dependency_edges_count: 8
cycle_count: 0
root_gaps:
  - "R3G-07-IMMUTABLE-PUBLIC-TRUST-KEY-STATUS"
leaf_gaps:
  - "R3G-06-PORTABLE-R4-AGGREGATE-REPORT-GENERATOR"
independent_gaps: []
```

`blocked_by`：

| gap | blocked_by |
| --- | --- |
| `R3G-01` | `R3G-07` |
| `R3G-02` | `R3G-01`, `R3G-04`, `R3G-05` |
| `R3G-03` | `R3G-07`（仅signed-role identity；当前parser逻辑已存在） |
| `R3G-04` | `R3G-03` |
| `R3G-05` | `R3G-07` |
| `R3G-06` | `R3G-02` |
| `R3G-07` | none |

图无循环；不需要 blocker。

## 7. 唯一 repair sequence

当前 pre-R3 分支只有 R3G-07，唯一顺序为：

```text
Phase 2-G-R3G1  public-trust binding scope audit
  -> Phase 2-G-R3G2  file-level atomic implementation plan
  -> future implementation phase defined by R3G2
  -> dedicated deterministic verification defined by R3G2
  -> fresh R3 file-level replan
  -> fresh human R3 execution authorization
```

R3G1与R3G2已经按最小职责拆分，不能合并：前者只回答事实/architecture/path问题，后者只把已经批准的决定转换为implementation白名单。把二者合并会让plan在尚未确定key custody与binding时自我批准，因此不是原子变更。

Implementation与verification不能在本计划中获得phase ID或路径白名单：只有R3G1审计通过、R3G2列出exact files后才可定义。此处的缺失是明确的fail-closed scope状态，不是“实施时再决定”。

Deferred R4 分支只能在future R4P内排序：

```text
R3G-01 + current R3G-03 mapping + R3G-04 + R3G-05
  -> R3G-02
  -> R3G-06
  -> fresh R3 refresh
  -> R4-P execution
```

该分支不计入当前 `repair_phase_count`，也不授权任何R4文件。

## 8. Phase 2-G-R3G1：Public Trust Binding Scope Audit

### 8.1 单一目标

只读确定 R3G-07 的唯一可实施architecture与exact path集合。不得实现schema、asset、loader、key或binding，不得运行测试。

### 8.2 精确文件范围

```yaml
phase: "Phase 2-G-R3G1"
phase_kind: "read_only_scope_audit"
mutable_existing_files: []
creatable_files:
  - "PORTABLE_RUNTIME_PUBLIC_TRUST_BINDING_SCOPE_AUDIT.md"
creatable_directories: []
default_deny_outside_exact_creatable_files: true
```

`read_only_files`：

```text
PORTABLE_RUNTIME_ROLE_GAP_RESOLUTION_PLAN.md
PORTABLE_RUNTIME_TRANSITIVE_CLOSURE_PLAN.md
RUNTIME_CAPABILITY_PROTOTYPE_RESULT.md
RUNTIME_CAPABILITY_REPAIR_PLAN.md
RUNTIME_ASSURANCE_PROFILE_DECISION.md
PORTABLE_AUTHORIZATION_SCHEMA_V2_PLAN.md
PORTABLE_AUTHORIZATION_SCHEMA_V2_IMPLEMENTATION_RESULT.md
CANDIDATE_EXECUTION_CONTRACT_REPAIR.md
runtime_capability_prototype/runtime/ctde_runtime/__init__.py
runtime_capability_prototype/runtime/ctde_runtime/common.py
runtime_capability_prototype/runtime/ctde_runtime/signing.py
runtime_capability_prototype/runtime/ctde_runtime/events.py
runtime_capability_prototype/runtime/ctde_runtime/authorization_v2.py
runtime_capability_prototype/runtime/ctde_runtime/authorization_registry.py
runtime_capability_prototype/runtime/ctde_runtime/range_broker.py
runtime_capability_prototype/runtime/ctde_runtime/bounded_reader.py
runtime_capability_prototype/runtime/ctde_runtime/formal_loader.py
runtime_capability_prototype/runtime/ctde_runtime/read_audit.py
runtime_capability_prototype/runtime/run_suite.py
runtime_capability_prototype/runtime/run_r2_portable.py
runtime_capability_prototype/runtime/build_manifest.py
runtime_capability_prototype/runtime/build_r2_portable_manifest.py
runtime_capability_prototype/contracts/authorization_schema_v2.yaml
runtime_capability_prototype/contracts/authorization_registry_record_schema_v2.yaml
runtime_capability_prototype/contracts/authorization_registry_event_schema_v2.yaml
runtime_capability_prototype/contracts/capability_claims_schema_v2.yaml
runtime_capability_prototype/contracts/broker_envelope_schema_v2.yaml
runtime_capability_prototype/contracts/audit_attestation_schema_v2.yaml
runtime_capability_prototype/contracts/r2_portable_controller_terminal_schema_v1.yaml
runtime_capability_prototype/contracts/r2_portable_authorization_test_requirements.yaml
runtime_capability_prototype/r2_portable_suites/R2PS-20260811-001/control/component_inputs.json
runtime_capability_prototype/r2_portable_suites/R2PS-20260811-001/control/r2_portable_manifest.yaml
runtime_capability_prototype/r2_portable_suites/R2PS-20260811-001/aggregate/r2_portable_results.json
```

`forbidden_paths` 使用精确workspace-relative directory path；`recursive: true` 表示该exact directory及全部descendants：

```yaml
forbidden_paths:
  - path: "runtime_capability_prototype"
    access: "write"
    recursive: true
    read_exception: "only the exact read_only_files listed above"
  - path: "source"
    access: "read_and_write"
    recursive: true
  - path: "analysis_candidate"
    access: "read_and_write"
    recursive: true
  - path: "runtime_os_observability_preflight"
    access: "read_and_write"
    recursive: true
workspace_write_policy: "default_deny"
workspace_write_exception:
  - "PORTABLE_RUNTIME_PUBLIC_TRUST_BINDING_SCOPE_AUDIT.md"
```

上述 `read_only_files` 与 `forbidden_paths` 是本阶段的closed authority；未明确列为唯一 `creatable_files` 的任何workspace-relative file均不可写，因此R3/R4/Hardened suite、registry、`story_structure.yaml`及任何其他business output即使未预先存在也不可创建。

### 8.3 Audit 必须唯一决定

1. public-trust registry schema、immutable record/asset、loader与必要caller-binding的exact relative paths；
2. 哪些existing files保持只读，是否任何non-R2 caller确需修改；
3. `kid`、algorithm、status、trust domain、`not_before`、`expires_at`的closed schema；
4. public-key exact bytes encoding、canonicalization、digest与external file identity规则；
5. private-key custody boundary、signer acquisition和“不把private key放入public freeze”的机制；
6. producer authority、create-once/update/revocation policy、self-digest分责；
7. verifier如何从record重建 `KeyRecord/TrustStore`，并证明actual runtime verifier使用同一identity；
8. R2 test keys与future R3/R4 trust identity的隔离，不修改或重解释R2历史；
9. deterministic synthetic validation与tamper/revoked/expired/unknown-kid test范围；
10. fresh R3 entrypoint、configuration、member和dependency-edge变化。

任一项不能唯一决定时：

```text
BLOCKED_PORTABLE_RUNTIME_PUBLIC_TRUST_BINDING_SCOPE_AUDIT
```

R3G1完成后停止，不自动进入R3G2。

## 9. Phase 2-G-R3G2：Public Trust Binding File-Level Atomic Plan

### 9.1 单一目标

只把已批准的R3G1结论转换为future implementation的闭合文件白名单、contracts、deterministic acceptance与evidence layout；不修改Runtime、不运行测试。

### 9.2 精确文件范围

```yaml
phase: "Phase 2-G-R3G2"
phase_kind: "file_level_atomic_planning_only"
mutable_existing_files: []
creatable_files:
  - "PORTABLE_RUNTIME_PUBLIC_TRUST_BINDING_PLAN.md"
creatable_directories: []
default_deny_outside_exact_creatable_files: true
```

`read_only_files`等于R3G1 §8.2清单，并新增：

```text
PORTABLE_RUNTIME_PUBLIC_TRUST_BINDING_SCOPE_AUDIT.md
```

`forbidden_paths`：

```yaml
forbidden_paths:
  - path: "runtime_capability_prototype"
    access: "write"
    recursive: true
    read_exception: "only the exact R3G1 read_only_files plus PORTABLE_RUNTIME_PUBLIC_TRUST_BINDING_SCOPE_AUDIT.md"
  - path: "source"
    access: "read_and_write"
    recursive: true
  - path: "analysis_candidate"
    access: "read_and_write"
    recursive: true
  - path: "runtime_os_observability_preflight"
    access: "read_and_write"
    recursive: true
workspace_write_policy: "default_deny"
workspace_write_exception:
  - "PORTABLE_RUNTIME_PUBLIC_TRUST_BINDING_PLAN.md"
```

该清单是closed authority；唯一可写文件是 `PORTABLE_RUNTIME_PUBLIC_TRUST_BINDING_PLAN.md`，其余workspace-relative paths全部default-deny。

R3G2必须输出：

- future implementation的全部 `mutable_existing_files`、`creatable_files`、`creatable_directories`、`read_only_files`和`forbidden_paths` exact paths；
- 每个允许修改文件的baseline SHA-256；
- schema/asset/loader/binding/verification/evidence/result的唯一producer和canonical paths；
- tests由manifest+runner实际枚举、不得预设数量；
- R2 semantic regression hard Gate；
- implementation后fresh R3 replan的明确要求。

若R3G1未PASS、path仍不唯一或需要修改R2 assets：

```text
BLOCKED_PORTABLE_RUNTIME_PUBLIC_TRUST_BINDING_PLAN
```

R3G2完成后停止，不自动执行implementation。

## 10. R2 immutable boundary 与 regression rule

R2已经：

```text
PASS_PORTABLE_AUTHORIZATION_SCHEMA_V2_IMPLEMENTED
```

Role-gap audit/plan/repair不得：

- 重设计 `authorization_schema_v2.yaml`；
- 改变authorization业务语义、typed contexts、CAS、nonce、replay、expiry或binding行为；
- 修改R2的16个implementation assets、fresh suite或历史result；
- 把R3 closure发现的`signing.py`/`common.py`传递依赖反推为R2 semantic failure。R2没有声称完整transitive closure；该事项属于R3。

如果后续证据证明真正的R2 semantic defect或public-trust修复必须改变R2语义：

```text
BLOCKED_R2_REGRESSION_DISCOVERED
```

必须记录path、digest、contract impact并停止；不得在R3G内patch或重写R2历史。

当前只读审计：

```yaml
r2_semantic_regression_count: 0
r2_asset_modification_count: 0
```

## 11. `R3_REENTRY_GATE`

```yaml
R3_REENTRY_GATE:
  current_r3p_blocking_gap_ids:
    - "R3G-01-PORTABLE-R4-SUITE-MANIFEST-BUILDER"
    - "R3G-02-PORTABLE-R4-SUITE-RUNNER"
    - "R3G-03-BOUNDED-PARSER-SCOPE"
    - "R3G-04-DISCARD-ONLY-MODEL-GATEWAY"
    - "R3G-05-PORTABLE-LOGICAL-WRITE-MONITOR"
    - "R3G-06-PORTABLE-R4-AGGREGATE-REPORT-GENERATOR"
    - "R3G-07-IMMUTABLE-PUBLIC-TRUST-KEY-STATUS"
  required_gap_ids:
    - "R3G-07-IMMUTABLE-PUBLIC-TRUST-KEY-STATUS"
  stage_scoped_deferred_to_r4_allowed_gap_ids:
    - "R3G-01-PORTABLE-R4-SUITE-MANIFEST-BUILDER"
    - "R3G-02-PORTABLE-R4-SUITE-RUNNER"
    - "R3G-05-PORTABLE-LOGICAL-WRITE-MONITOR"
    - "R3G-06-PORTABLE-R4-AGGREGATE-REPORT-GENERATOR"
  minimal_embedded_role_mapping_required_gap_ids:
    - "R3G-03-BOUNDED-PARSER-SCOPE"
    - "R3G-04-DISCARD-ONLY-MODEL-GATEWAY"
  minimal_embedded_role_mapping_failure_result: "BLOCKED_R3_ROLE_GAP_UNRESOLVED"
  deferred_gap_ids:
    - "R3G-01-PORTABLE-R4-SUITE-MANIFEST-BUILDER"
    - "R3G-02-PORTABLE-R4-SUITE-RUNNER"
    - "R3G-03-BOUNDED-PARSER-SCOPE"
    - "R3G-04-DISCARD-ONLY-MODEL-GATEWAY"
    - "R3G-05-PORTABLE-LOGICAL-WRITE-MONITOR"
    - "R3G-06-PORTABLE-R4-AGGREGATE-REPORT-GENERATOR"
  r3_replan_required: true
  fresh_replan_role_adjudication_required: true
  r3_execution_authorized: false
```

真正 R3 重新获准前必须全部满足：

1. R3G1 scope audit PASS且exact digest由外部授权记录；
2. R3G2 atomic plan PASS且所有implementation/evidence paths唯一；
3. 根据R3G2另行授权的implementation真实完成；
4. dedicated deterministic synthetic tests全部由其manifest/runner实际枚举并PASS，evidence complete；
5. R2 asset modifications=0、R2 semantic regression=0；
6. public trust schema/record/loader/runtime binding与actual signer/verifier identity闭合；
7. fresh R3 replan重新枚举改变后的Runtime tree、entrypoint set、configuration和dependency graph；
8. fresh R3 replan建立stage/profile-scoped `required_runtime_roles`，保留七项identity与证据；仅R3G-01/02/05/06可逐项批准stage-scoped deferred disposition；任何builder不得在执行时临时删除gap；
9. R3G-03 parser与R3G-04 gateway的minimal embedded-role mapping必须各自确定性验证并冻结为PASS；只有future strengthening可defer；任一mapping失败即把对应gap重新纳入pre-R3 repair set并拒绝R3 re-entry；
10. fresh R3 replan重新冻结write scope与creatable paths；现有R3P保持原字节只读，不原地更新；
11. fresh human R3 execution authorization明确引用fresh replan exact SHA-256；
12. deferred R4/Hardened gap未被偷渡进当前R3 implementation/Gate。

`R3 replan required=true` 的原因：R3P当前 `mutable_existing_files=[]`、31个creatable paths均没有public-trust schema/asset/loader/binding；修复必然改变Runtime tree、closure roots/config/member set或dependency edges。只要这些bytes变化，旧Plan digest和旧entrypoint inventory就不能授权执行。

## 12. 本阶段禁止与状态保持

本阶段只创建本计划文件，不得：

- 修改Runtime、legacy files或R2 assets；
- 创建public-trust implementation、closure manifest、runner或evidence tree；
- 执行Runtime tests、R3、R4或Candidate；
- 读取English/Greek TEI content或structure map；
- 调用模型或创建任何文学/业务输出；
- 创建Hardened/A2/A3 artifacts；
- 修改R3P、旧suite、Run 001/002或Candidate status。

历史状态保持：

```yaml
phase_2g: "BLOCKED_RUNTIME_CAPABILITY_PROTOTYPE_FAILED"
phase_2g_r1: "BLOCKED_OS_OBSERVABILITY_INSUFFICIENT"
phase_2g_r1d: "ADOPT_DUAL_ASSURANCE_PROFILES"
phase_2g_r2: "PASS_PORTABLE_AUTHORIZATION_SCHEMA_V2_IMPLEMENTED"
phase_2g_r3p: "PASS_PORTABLE_R3_PLAN_ONLY"
historical_allow_r2_false_changed: false
old_suite_status_changed: false
run_001_status_changed: false
run_002_status_changed: false
candidate_analysis: "BLOCKED"
```

## 13. Plan-only acceptance 与 action ledger

以下条件均满足，故允许本规划阶段返回：

```text
PASS_PORTABLE_RUNTIME_ROLE_GAP_RESOLUTION_PLAN
```

- 七项gap全部从R3P恢复并逐项解释；
- 每项只有一个primary classification；
- 当前R3P的七项formal blockers与fresh-replan前只需实际修复的precondition集合被明确分层；
- 两个stale-description candidates有真实调用链证据，仍计入七项current formal gaps，未静默删除或提前解除；
- dependency graph有8条direct edges、0个cycle；
- 唯一precondition gap已有下一阶段exact scope；
- scope不足处全部明确标记additional audit，没有猜implementation path；
- R2 semantic regression=0；
- R4/Hardened工作没有提前；
- R3 replan与fresh human authorization被设为硬Gate。

本阶段controller A1 action ledger如下；它不是A2 OS-verified counts：

```yaml
created_files:
  - "PORTABLE_RUNTIME_ROLE_GAP_RESOLUTION_PLAN.md"
modified_existing_files: []

runtime_modifications: 0
r2_asset_modifications: 0
r3_execution_count: 0
r4_execution_count: 0
runtime_tests_executed: 0
candidate_run_count: 0
model_call_count: 0
english_tei_content_read_count: 0
greek_tei_content_read_count: 0
business_output_count: 0
story_structure_yaml_created: false

runtime_content_tree_sha256_before: "820afae1806d4cec398b54193574e62e1933c2e8745dfb570d00b969bd69fe43"
runtime_content_tree_sha256_after: "820afae1806d4cec398b54193574e62e1933c2e8745dfb570d00b969bd69fe43"
runtime_tree_unchanged: true

a2_os_verified_counts:
  status: "NOT_PROVIDED"
```

本计划完成后停止，不自动执行R3G1、任何gap repair、R3或R4。
