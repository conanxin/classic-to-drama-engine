# Classic-to-Drama Engine：Runtime Assurance Profile Architecture Decision

> 项目：Classic-to-Drama Engine  
> 阶段：Phase 2-G-R1D  
> ADR ID：`CTDE-ADR-2G-R1D-001`  
> 日期：2026-08-11  
> 文档类型：Runtime Assurance Profile Architecture Decision  
> 最终决策：`ADOPT_DUAL_ASSURANCE_PROFILES`  
> 决策效力：`prospective_architecture_only`  
> 既有状态／合同修改：无  
> Runtime／测试／Candidate execution：未执行

## 0. 最终决策

本 ADR 决定采用两个名称、Gate、证据声明和结果状态均不可混淆的 Runtime Assurance Profile：

1. `Portable / Development Profile`
   - 最低强制证据等级为 `A1 runtime logical proof`；
   - 用于可移植的开发、合成 Runtime 验证和开发性 Candidate Analysis；
   - 不提供 A2 OS-level file-access proof；
   - 不得声明 A3、hardened、certified 或等价含义。
2. `Hardened / Certification Profile`
   - 强制要求 `A3 combined runtime and OS proof`；
   - 用于 release certification、高保证隔离验证和可选严格 CI；
   - 必须在具备完整、独立、PID 归属明确且不可由被测进程篡改的 OS observer 环境中重新执行。

最终选择：

```yaml
decision: "ADOPT_DUAL_ASSURANCE_PROFILES"
a1_definition_changed: false
a2_definition_changed: false
a3_definition_changed: false

portable_is_weakened_a3: false
portable_pass_implies_hardened_pass: false
portable_result_may_be_promoted_to_hardened: false

phase_2g_status_changed: false
phase_2g_r_status_changed: false
phase_2g_r1_status_changed: false
legacy_r1_allow_r2_changed: false

r2_may_be_replanned_for_portable: true
r2_execution_authorized_by_this_adr: false
candidate_analysis_currently_blocked: true
hardened_certification_currently_blocked: true
```

本决策改变的是未来 Gate 的适用范围，不是 A1／A2／A3 的定义。任何既有 A3 claim 的最低证据等级不得改为 A1；Portable 必须使用更窄、措辞不同的 logical claim。

## 1. 决策依据与冻结事实

### 1.1 本阶段依据

| 依据文件 | SHA-256 | 决策用途 |
| --- | --- | --- |
| `RUNTIME_CAPABILITY_PROTOTYPE_RESULT.md` | `6811bcc4ef0efcaee89013648dd0bb06bbaca154625f3dc47bdfa0f295851753` | Phase 2-G 的真实实现、测试与 blocker 边界 |
| `RUNTIME_CAPABILITY_REPAIR_PLAN.md` | `a2c52dbaecf3956cf4a2189abe5401f269d255e8099d3345985619be25be4213` | 现有单一 A3 修复路线、证据等级与后续 Gate |
| `RUNTIME_OS_OBSERVABILITY_PREFLIGHT_RESULT.md` | `0ca51394315199683cd790e01d160addb80f1cb0e32bb23df212045b49c433c0` | 当前环境的 R1 实测结论 |
| `OS_OBSERVABILITY_CAPABILITY_MATRIX.json` | `5fdf7dd8088fcb817b484a8dc699f97338dd8e2955e8ead739420bd62f814162` | 40 项 capability 的机器可读结果与 blocker |

### 1.2 不得重解释的历史状态

```yaml
phase_2g:
  status: "BLOCKED_RUNTIME_CAPABILITY_PROTOTYPE_FAILED"
  suite: "RCPTS-20260811-002"
  pass_fail: "99 / 98"

phase_2g_r:
  status: "PASS_REPAIR_PLAN_ONLY"

phase_2g_r1:
  status: "BLOCKED_OS_OBSERVABILITY_INSUFFICIENT"
  suite: "OSOP-20260811-001"
  probes: 40
  pass: 22
  fail: 16
  unknown: 2
  highest_end_to_end_evidence_level: "A1"
  highest_individual_capability_level: "A2"
  allow_r2_under_legacy_single_a3_route: false
```

以下事实保持原样：

- PID namespace 映射、父子关系、已知 process tree、生命周期以及 `/proc` status／cmdline／fd／fdinfo 等窄能力存在局部 A2 supporting evidence；
- `strace` launch／attach、`PTRACE_TRACEME`、`PTRACE_ATTACH` 和 `fanotify_init` 均在实际探针中被拒绝；
- 完整 successful file-open set、descendant syscall coverage、第二读取通道、network/write coverage、event-loss 精确计数和 evidence tamper isolation 均未证明；
- qualification-wide A2 不成立，A3 不成立；
- `RCPTS-20260811-002` 还存在 Authorization Schema mismatch 与 Runtime snapshot closure gap，不能因本 ADR 被重标为 Portable PASS；
- R1 Matrix 中的 `allow_r2=false` 是原单一 A3 路线下的真实历史结论，不得回写为 `true`。

## 2. 架构问题与风险适配

原项目目标是：

```text
经典文本 -> AI analysis -> 短剧剧本研发
```

该目标同时包含两类不同命题：

1. **开发正确性命题**：授权是否存在、范围是否正确、交付是否受限、来源是否可追溯、逻辑审计是否闭合、执行代码是否可复现。
2. **高保证隔离命题**：完整 consumer process tree 是否确实没有通过任何 path、FD、descendant、mmap、io_uring、network 或其他 OS 通道越界访问。

A1 可以对第一类命题形成有边界的逻辑证明。A3 才能对第二类命题形成“逻辑合同 + 独立 OS 观测”的联合证明。

开发性文学分析的功能价值并不以“完整 OS 文件访问集合已独立认证”为内在前提。只要运行在受信开发模型下，并继续强制 authorization、range、bounded delivery、formal loading、provenance 和 frozen snapshot，A1 足以支持诚实标注的研发运行。A3 对 release certification、高保证隔离、潜在敌对代码或严格合规环境仍然必要。

因此：把 A3 作为**所有**文学分析与短剧研发的硬依赖，相对于当前项目的开发性风险属于过度工程化；把 A3 保留为 Hardened／Certification Gate 则不是过度工程化。

### 2.1 Portable Profile 的适用威胁模型

Portable 只适用于以下条件：

- 运行代码、组件和依赖处于开发者控制下，不把 Candidate consumer 当作主动恶意代码；
- source 使用本身已获项目授权，当前关注点是范围正确性与可追溯性；
- 输出用于开发、研究、调试或创作，不用于对外安全认证；
- 可以接受“没有完整 OS 级零旁路证明”这一明确残余风险；
- 任一 A1 必需字段缺失、签名无效、provenance 不完整或 snapshot 漂移时均 fail closed。

以下情形必须使用 Hardened Profile：

- 需要对外声明完整 file-access set、零旁路或 OS-isolated；
- release certification、严格 CI 或第三方安全验收；
- 输入具有敏感、保密、许可或合规边界，越界读取不可接受；
- consumer、插件、工具或动态代码不受信；
- 多租户执行，或网络／写入／子进程逃逸会造成高影响后果。

若未来项目威胁模型整体转为上述任一情形，应重新评审本 ADR；届时 `KEEP_SINGLE_A3_GATE` 可能成为正确选择。

## 3. 方案 A：保持单一 A3 Gate

### 3.1 定义

所有 synthetic Runtime、Candidate Analysis、文学结构分析、人物／事件／主题抽取和短剧改编研发，均只有在同一 attempt 上形成 A1+A2 的 A3 后才能运行或通过。

### 3.2 优点

- 单一结果语义，几乎没有 Profile 混淆风险；
- 所有运行都具备完整 OS-level process/file assurance；
- full raw、Greek、descendant、第二通道和零访问声明可使用同一严格标准；
- release certification 与开发 Gate 不需要转换。

### 3.3 当前 ChatGPT Work 环境中的实际后果

- R1 持续为 `BLOCKED_OS_OBSERVABILITY_INSUFFICIENT`；
- R2、R3、R4 均不能在本环境推进；
- Authorization Schema V2 和 snapshot closure 这两类不以 ptrace 为逻辑前提的缺陷也被环境 Gate 连带阻断；
- synthetic E2E、开发性 Candidate Analysis、文学结构分析、人物／事件／主题抽取和短剧改编研发全部停止；
- 项目必须迁移到具备 ptrace/strace、eBPF/audit/fanotify 或语义等价能力的环境后才能继续；
- 开源贡献者和普通容器环境难以复现实质功能，只能阅读文档或运行不产生有效 Gate 的局部测试。

### 3.4 评价

方案 A 最大化单次运行保证，但把“能否进行开发”与“能否取得认证”绑定为同一个问题。对当前项目目标而言，这种绑定的成本高于其开发阶段的风险收益；因此不采用。

## 4. 方案 B：双 Assurance Profile

### 4.1 Profile 总表

| 属性 | Portable / Development | Hardened / Certification |
| --- | --- | --- |
| Profile ID（建议） | `CTDE-PORTABLE-DEV-1` | `CTDE-HARDENED-CERT-1` |
| 最低证据 | A1 | A3 |
| OS-level file-access proof | 不提供；必须显式声明 | 强制提供 |
| 独立完整 file-open set | 不得声称 | 必须证明 |
| 允许结果码 | `PASS_PORTABLE_DEVELOPMENT_A1_NONCERTIFIED` | `PASS_HARDENED_CERTIFICATION_A3` |
| hardened/certified 标记 | 永远为 `false` | 仅 A3 全部 Gate 通过后为 `true` |
| 主要用途 | 开发、研究、创作、可移植测试 | 发布认证、高保证隔离、严格 CI |
| 能否由 Portable 结果升级 | 不适用 | 不允许；必须 fresh run |

### 4.2 Portable / Development Profile

Portable 的最低强制组件与证据为：

| ID | 强制要求 | 最低证明 |
| --- | --- | --- |
| `PORT-001` | authorization registry：schema、identity、CAS、expiry、replay 与一次性消费闭合 | A1 |
| `PORT-002` | range broker：只接受有效 capability，并按授权范围请求与交付 | A1 |
| `PORT-003` | bounded reader：只接受已验证 envelope／sealed delivery，并执行一次性交付合同 | A1 |
| `PORT-004` | formal loader：profile-aware allowlist、provenance、identity/digest 与 TOCTOU 逻辑检查 | A1 |
| `PORT-005` | runtime logical read audit：签名事件、真实到达状态、拒绝副作用和 terminal closure | A1 |
| `PORT-006` | provenance：source/slice identity、authorization、capability、delivery、component 与 output binding | A1 |
| `PORT-007` | frozen execution snapshot：完整 project-owned logical execution closure 与 start/end identity | A1 |
| `PORT-008` | immutable profile binding：suite、attempt、grant、attestation、result 与 output 均绑定 Portable | A1 |

Portable PASS 只能声明：

- authorization artifact、external registry identity 与 CAS 状态机按合同工作；
- broker 的受 instrumentation 覆盖逻辑记录了 requested／returned range；
- bounded reader、parser、gateway 和 formal loader 按各自受 instrumentation 覆盖的逻辑合同执行；
- signed provenance、event chain 与 frozen execution snapshot 闭合；
- Runtime/controller 逻辑账本记录的 Candidate、model、business action 数值；
- 未通过受控 Runtime 路径请求或交付 Book 2、Greek 或 full object。

Portable PASS 不得声明：

- consumer 的完整实际 file-open set 已被观察；
- consumer 没有其他 path、继承 FD、瞬时 open/read/close、descendant、mmap、sendfile、splice、io_uring、network 或写入旁路；
- Book 2、Greek 或 full raw 在 OS 层“不可访问”；
- real-source access、Candidate Run、model call 或 business output 已由独立 OS observer 证明为 0；
- observer evidence 不可由 consumer、broker 或 bounded reader 篡改；
- A2、A3、hardened、certified、secure sandbox certified 或任何等价保证。

Portable 报告必须至少包含：

```yaml
assurance_profile_id: "CTDE-PORTABLE-DEV-1"
result: "PASS_PORTABLE_DEVELOPMENT_A1_NONCERTIFIED"
highest_claimed_evidence_level: "A1"
a2_os_file_access_proof: "NOT_PROVIDED"
a2_verified_access_counts: null
hardened: false
certified: false
portable_to_hardened_promotion_allowed: false
```

`null`、`unknown` 或 `not evaluated` 不得改写为整数 `0`。

### 4.3 Portable 允许用途评估

| 用途 | Portable 是否适用 | 条件 |
| --- | --- | --- |
| synthetic runtime tests | 是 | 使用 Portable manifest 与 A1 claim，不产生 Hardened 结论 |
| `analysis_candidate` | 将来可用 | Portable 合同、R2、R3、全新 Portable E2E 与新 Candidate authorization 全部通过后 |
| 文学结构分析 | 将来可用 | 输出携带 Portable provenance 与 non-certified 标记 |
| 人物／事件／主题抽取 | 将来可用 | 同上；不得进入 certified namespace |
| 短剧改编研发 | 将来可用 | 仅开发／创作流程，不代表 release certification |
| release certification | 否 | 必须 Hardened A3 |
| 高保证隔离验证 | 否 | 必须 Hardened A3 |
| 严格 CI 认证 Gate | 否 | 必须 Hardened A3；普通开发 CI 可运行 Portable |

“Candidate 隔离”在两个 Profile 中必须拆成两个不同 claim：

```yaml
portable_claim: "candidate_input_scope_logically_enforced"
hardened_claim: "candidate_file_access_isolation_os_verified"
```

Portable 可以保持授权、范围、交付与输出边界的 Runtime 设计，但不能把这种逻辑隔离描述为完整 OS 非旁路证明。

### 4.4 Hardened / Certification Profile

Hardened 强制要求 A3，即同一 fresh attempt 上的 A1 与完整 A2 可验证关联。运行环境必须提供：

- 独立于 consumer、broker、bounded reader 自报的 OS-level process/file evidence；
- ptrace/strace、eBPF、Linux Audit、fanotify 或覆盖语义等价的 observer；
- host／namespace PID、start time、cgroup 或等价稳定 identity 与完整 descendant attribution；
- process create／exec／exit、root、mount、FD、file-open/read、网络、写入和第二读取通道的 closed coverage；
- observer ready-before-open、零 event loss、decode error 计数和 crash fail-closed；
- 被测进程无法修改、截断或删除 observer evidence；
- A1 authorization/range/delivery/provenance 与 A2 trace 在同一 attempt 上绑定。

Hardened 结果建议使用：

```yaml
assurance_profile_id: "CTDE-HARDENED-CERT-1"
result: "PASS_HARDENED_CERTIFICATION_A3"
highest_claimed_evidence_level: "A3"
a2_os_file_access_proof: "COMPLETE"
hardened: true
certified: true
```

当前环境不满足这些条件，因此 Hardened Profile 继续保持 blocked。

## 5. 防止 Profile 混淆的架构不变量

以下规则是采用双 Profile 的必要条件，而非可选实现细节：

1. `assurance_profile_id` 必须在 suite／attempt 创建前选择并冻结；不存在默认 Profile。
2. manifest、authorization、registry identity、grant、capability、envelope、delivery、snapshot、event、scope/closure attestation、result、report 和业务输出均必须绑定同一 Profile ID。
3. Profile 不得在运行期间或运行后切换、补写或重标。
4. 两个 Profile 使用互斥结果码；禁止裸 `PASS`、`PASS_RUNTIME` 或语义不明确的 success。
5. Portable 的 A2 字段必须是 `null`／`unknown`／`NOT_PROVIDED`，不得因 A1 逻辑计数为 0 而写成 A2 verified 0。
6. Portable suite、attempt、grant、capability、delivery、evidence 或 attestation 不得用于形成 Hardened aggregate。
7. Hardened 必须在 A2-capable 环境中使用全新 suite、attempt、grant 与同一运行窗口重新执行；不得给旧 Portable attempt 追加 A2 后追认。
8. Hardened formal loader、certified namespace 和 release Gate 必须精确拒绝 Portable 状态与 Portable provenance。
9. Portable 输出在所有 UI、报告、manifest 和导出中持续显示 `A1 / non-certified`，不能只在脚注披露。
10. 共同代码可以共享，但两个 Profile 的 mandatory claim set、result schema 与 Gate 必须分别验证，防止测试矩阵静默漂移。
11. 两个 Profile 可以共享 schema、实现代码、closure builder 与 policy definition；不得共享 profile-bound authorization artifact、validation evidence、snapshot instance、start/end verification 或 suite Gate result。
12. Hardened 必须重新物化并验证绑定 Hardened Profile 的 R2/R3 evidence；Portable 的 R2/R3 execution PASS 不得进入 Hardened aggregate。

建议冻结以下失败状态：

```yaml
portable_failure: "BLOCKED_PORTABLE_A1_REQUIREMENTS_UNMET"
hardened_unavailable: "BLOCKED_HARDENED_A3_OS_OBSERVABILITY_INSUFFICIENT"
profile_missing: "BLOCKED_ASSURANCE_PROFILE_MISSING_OR_AMBIGUOUS"
profile_mismatch: "BLOCKED_ASSURANCE_PROFILE_BINDING_MISMATCH"
promotion_attempt: "BLOCKED_PORTABLE_TO_HARDENED_PROMOTION"
```

## 6. 对评审问题的回答

### 6.1 开发性 Candidate Analysis 是否确实需要 A3

不需要。A3 是“完整 OS 非旁路与逻辑合同联合认证”的必要条件，不是文学结构分析、人物／事件／主题抽取或短剧研发产生开发价值的必要条件。

开发性 Candidate Analysis 可以在 Portable A1 下进行，但必须满足三个限制：

- A1 必需组件与 provenance/snapshot 全部通过；
- 输出显式为 Portable、non-certified；
- 不得把任何逻辑拒绝或零计数升级成 OS-level inaccessible/zero-access claim。

### 6.2 单一 A3 是否过度工程化

对全部开发运行而言，是。它把 ptrace、fanotify 或等价 observer 权限变成文学分析功能开发的先决条件，并连带阻断与 A2 无逻辑依赖的 schema 和 snapshot 修复。

对 release certification、高保证隔离和严格 CI 而言，不是。A3 应继续作为这些用途的硬 Gate。

### 6.3 双 Profile 能否同时保持六项目标

| 目标 | 结论 | 保持方式与边界 |
| --- | --- | --- |
| 不伪造安全保证 | 可以 | 互斥状态码、A2 null、强制 non-certified、禁止 promotion |
| 来源可追溯 | 可以 | 两个 Profile 都强制 provenance、digest binding 与 snapshot identity |
| Candidate 隔离 | 有边界地可以 | Portable 保持 Runtime 逻辑范围隔离；只有 Hardened 声明 OS-verified isolation |
| 开发可执行性 | 可以 | Portable 不依赖当前环境无法提供的完整 A2 observer |
| 开源可移植性 | 可以 | 普通开发环境可实现 A1 核心；高级 observer 作为 Hardened 环境能力 |
| 后续严格认证能力 | 可以 | A3 定义与完整 Gate 原样保留，未来在合格环境 fresh run |

因此，双 Profile 能同时保留这些目标，但“Candidate 隔离”必须使用 Profile-qualified claim，不能继续作为无修饰的单一安全声明。

## 7. 未来需要修订的既有 Gate

本阶段不修改以下任何文件或 Gate；这里只记录未来影响面。

### 7.1 `RUNTIME_CAPABILITY_REPAIR_PLAN.md`

| 位置 | 未来修订方向 |
| --- | --- |
| §2.1 优先级总表 | 将 R2/R3 设为共享基础；将 R1 改为 Hardened observer qualification；R4 分成 Portable 与 Hardened 两条出口 |
| §2.2 依赖规则 | 从唯一 `R1 ∧ R2 ∧ R3 -> R4` 改为 `R2 ∧ R3 -> R4-P` 与 `R1-H ∧ R2 ∧ R3 -> R4-H` |
| §2.3 R1 | 保留全部原资格要求和 BLOCKED 语义，但只阻断 Hardened，不再阻断 Portable 的 schema/snapshot 修复 |
| §2.6 R4 | 拆分 fresh Portable A1 synthetic E2E 与 future Hardened A3 certification suite |
| §5.1 Evidence tiers | A0–A3 定义不改；只新增 Profile-to-tier applicability policy |
| §5.2 Claim-to-tier matrix | 原 A2/A3 claim 保留；Portable 新增措辞更窄的 logical claim ID，不降低原 claim 的 tier |
| §5.5 两阶段聚合 | `A1 PASS + A2 unavailable -> BLOCKED` 保留为 Hardened 规则；Portable 使用独立 non-certified result |
| §6.1–§6.4 Book 1 E2E | 保留现有 A3 路径；新增 A1 logical chain，不复用 full raw/Greek/second-channel 的 OS 零访问措辞 |
| §7.1 `P2GR-NP-001` | 改为 Hardened-only；`NP-002/003` 继续是两个 Profile 的共享 Gate |
| §7.2 manifest/runner | 增加 immutable profile binding；两个 Profile 具有独立 mandatory leaf set，测试数仍由实际枚举 |
| §7.3 acceptance IDs | 原 A3 acceptance 保留给 Hardened；Portable 使用新 ID 与新 claim，不把 evidence 列从 A3 改成 A1 |
| §7.4 零真实来源证明 | 保留为 Hardened-only；Portable 分开记录 logical count 与 `a2_verified_count: null` |
| §7.5 最终判定 | 删除无 Profile 的通用 PASS；新增互斥 Portable/Hardened result |
| §7.6 结果报告 | 强制记录 Profile、最高证据、未提供的 A2 claim、`certified=false` 与两个独立结果域 |
| §8.2 后续顺序 | Portable PASS 后可规划全新 Portable Candidate；Hardened certification 仍必须 A3 |
| §9 总结 | 从单线 R1→R2→R3→R4 改为共享 R2/R3 加双出口 |

### 7.2 其他未来合同／计划

- `RUNTIME_CAPABILITY_PROTOTYPE_PLAN.md`：未来需把单一 A3 suite acceptance 拆成 Portable logical claim set 与 Hardened A3 claim set。
- `CANDIDATE_EXECUTION_CONTRACT_REPAIR.md`：未来需为 Candidate authorization、execution snapshot、attestation、result label、Formal loader destination 与输出 provenance 增加不可变 Profile binding。
- 任何 Candidate Run Plan／result schema：未来必须明确 `assurance_profile_id`、允许用途、最高 evidence level 与 certification 状态。

以上两份文件不属于本阶段的四份读取依据，因此本 ADR 不声称其精确章节；后续合同修订阶段必须按完整文件重新盘点。

### 7.3 不应修改的历史证据

- `RUNTIME_CAPABILITY_PROTOTYPE_RESULT.md` 继续保持 Phase 2-G BLOCKED；
- `RUNTIME_OS_OBSERVABILITY_PREFLIGHT_RESULT.md` 继续保持 R1 BLOCKED 与 `allow_r2=false`；
- `OS_OBSERVABILITY_CAPABILITY_MATRIX.json` 的 40 项结果、18 个 required non-PASS、顶层 `r1` 和 `allow_r2` 均保持原样；
- 旧 suite `RCPTS-20260811-002` 不得重分类、补证或升级；
- 既有 Candidate Run 002 不得复用或因本 ADR 解锁。

## 8. 后续路线与 Phase 影响

### 8.1 推荐依赖图

```text
Shared foundation:
  Profile-aware schema / implementation / closure definitions

Portable track:
  R2-P profile-bound validation + R3-P profile-bound snapshot
  -> fresh R4-P A1 synthetic E2E
  -> new Portable Candidate Plan/authorization
  -> development Candidate Analysis

Hardened track:
  R1-H A2-capable environment
  + fresh R2-H profile-bound validation
  + fresh R3-H profile-bound snapshot/start-end verification
  -> fresh R4-H A3 suite
  -> release certification / high-assurance validation / strict CI
```

共享的是定义与实现，不是运行证据：

```yaml
shared_implementation_allowed: true
shared_schema_and_policy_definitions_allowed: true
cross_profile_authorization_artifact_reuse: false
cross_profile_snapshot_instance_reuse: false
cross_profile_execution_evidence_reuse: false
hardened_profile_bound_r2_r3_revalidation_required: true
```

### 8.2 Phase 状态表

| Phase / 工作包 | 本 ADR 后的状态 | 说明 |
| --- | --- | --- |
| Phase 2-G | `BLOCKED_RUNTIME_CAPABILITY_PROTOTYPE_FAILED` | 历史状态不变 |
| Phase 2-G-R | `PASS_REPAIR_PLAN_ONLY` | 历史状态不变 |
| Phase 2-G-R1 | `BLOCKED_OS_OBSERVABILITY_INSUFFICIENT` | Hardened qualification blocker 不变 |
| Phase 2-G-R1D | `ADOPT_DUAL_ASSURANCE_PROFILES` | 仅架构决策完成 |
| R2 Portable replanning | `MAY_BE_REPLANNED_NEXT` | 可以重新规划；本 ADR 不执行或通过 R2 |
| R2 execution | `NOT_AUTHORIZED_BY_THIS_ADR` | 需 future Profile-aware Gate／计划明确后实施 |
| R3 | `NOT_EXECUTED` | 作为两个 Profile 的共享基础，仍需未来完成 |
| R4-P | `NOT_PLANNED / NOT_EXECUTED` | 必须使用全新 Portable suite |
| R1-H / R4-H | `DEFERRED_BLOCKED` | 等待 A2-capable 环境 |
| Candidate Analysis | `CURRENTLY_BLOCKED` | 尚无 Portable 合同、R2/R3/R4-P PASS 或新授权 |
| Hardened certification | `BLOCKED` | 当前环境最高 qualification-wide A1 |

### 8.3 R2 是否可以继续

结论分两层：

- **可以**把下一阶段重新规划为 Portable 目标的 `R2 Authorization Schema V2`；因为 self-digest/schema/registry identity 是 A1 合同正确性问题，不依赖 ptrace/strace。
- **不可以**把本 ADR 当作 R2 已授权执行或已 PASS；必须先以单独阶段冻结 Profile-aware R2 范围、输入、输出与验收条件。

这不是把历史 Matrix 的 `allow_r2=false` 改成 `true`。该字段继续准确描述原单一 A3 路线；未来 Portable 路线应使用新的、profile-qualified Gate。

### 8.4 Candidate Analysis 是否仍然 blocked

当前仍然 blocked。

只有以下全部成立，才可规划新的 Portable Candidate Analysis：

1. 双 Profile 规则进入未来适用合同；
2. R2 Authorization Schema V2 在 Portable/shared Gate 下 PASS；
3. R3 frozen execution snapshot closure 在 Portable/shared Gate 下 PASS；
4. 全新 R4-P synthetic suite 达到 `PASS_PORTABLE_DEVELOPMENT_A1_NONCERTIFIED`；
5. 创建全新的 Candidate Plan、attempt、authorization 与 provenance；
6. Candidate 输出明确绑定 Portable、A1、non-certified。

现有 Candidate Run 002 永远不因这些未来工作被复用或解锁。

## 9. Deferred Hardened Work

以下工作从 Portable 开发路径中延期，但没有取消、降级或视为已完成：

1. 在具备 ptrace/strace、eBPF/audit/fanotify 或语义等价 observer 的环境重新完成 R1-H；
2. 关闭 `OSOP-016..019`、`OSOP-025..027`、`OSOP-029..039` 的 required FAIL/UNKNOWN；
3. 证明完整 descendant process attribution 与 lifecycle coverage；
4. 证明完整 PID-attributed successful file-open set；
5. 覆盖 FD passing、mmap、sendfile、splice、copy_file_range、io_uring 等第二读取通道；
6. 覆盖 network、exec 与 write/create/rename/link/unlink 路径；
7. 建立 exact event-loss／decode-error 计数和 observer crash fail-closed；
8. 隔离 observer evidence，使 consumer、broker、bounded reader 无写／删／截断权限；
9. 对真实来源、Candidate、model 与 business output 形成 OS-verified zero/count proof；
10. 在同一 fresh attempt 上关联 A1+A2，执行完整 A3 synthetic suite；
11. 建立 release certification 与可选 strict CI Gate。

Deferred 不表示 optional security claim 已获得。任何依赖这些能力的 claim 在 Hardened PASS 前均保持 blocked/not provided。

## 10. 风险与处置

| 风险 | 影响 | 架构处置 |
| --- | --- | --- |
| 用户或下游把 Portable 当成认证结果 | 产生虚假安全保证 | 强制 A1/non-certified 标记、互斥状态码、无裸 PASS |
| A1 instrumentation 漏记旁路访问 | 越界读取不被发现 | 明确残余风险；只允许受信开发模型；高风险输入转 Hardened |
| `unknown` 被转写为 0 | 伪造 OS 零访问 | A2 字段独立，Portable 固定为 null/NOT_PROVIDED |
| Portable artifact 被聚合进 Hardened | 认证污染 | Profile 进入全部 identity；cross-profile verifier fail closed |
| 两套测试矩阵长期漂移 | 开发与认证行为分叉 | 共享 R2/R3 核心与代码 closure；Profile claim set 分别版本化 |
| Hardened 工作被无限延期 | 永远无法发布认证 | 保留明确 backlog、环境资格 Gate 与 strict CI 入口 |
| 当前 99 个旧 PASS 被错误复用 | 掩盖 schema/snapshot/OS 缺口 | 旧 suite 永久历史化；Portable 必须 fresh suite 全量重跑 |
| Formal loader 误把 Portable 输出送入 certified namespace | 非认证输出被提升 | destination 与 loader allowlist 精确绑定 Profile/status |

采纳双 Profile 的剩余风险是可见且有标签的：Portable 信任 Runtime 核心和 A1 instrumentation，不能独立排除 OS 旁路。该风险对于开发用途可接受；对于认证用途不可接受，并由 Hardened Gate 保持阻断。

## 11. 决策记录

```yaml
phase: "Phase 2-G-R1D"
adr_id: "CTDE-ADR-2G-R1D-001"
decision: "ADOPT_DUAL_ASSURANCE_PROFILES"
rationale:
  - "A3 is necessary for certification-grade no-bypass claims, not for all literary development execution."
  - "The current Work environment cannot provide qualification-wide A2, so a single A3 gate blocks all meaningful development."
  - "A1 authorization, bounded delivery, provenance and snapshot controls address the principal development risks without claiming OS certification."
  - "Separate immutable profiles preserve both honest assurance and a future strict certification path."

affected_phases:
  - "future R2 Authorization Schema V2 planning"
  - "future R3 Runtime Snapshot Closure"
  - "future R4-P Portable synthetic E2E"
  - "deferred R1-H/R4-H Hardened certification"
  - "future profile-qualified Candidate planning and execution"

deferred_hardened_work: true
r2_may_be_replanned: true
r2_authorized_or_executed_this_phase: false
candidate_analysis_remains_blocked_now: true
portable_candidate_analysis_may_later_proceed: true
hardened_candidate_or_release_certification_blocked: true

historical_phase_2g_reclassified: false
historical_r1_reclassified: false
old_suite_promoted: false
existing_contracts_modified: false
```

## 12. 本阶段边界终检

本阶段只创建本 ADR 文档。以下 action 数值只属于本阶段 authoring/controller 的 A1 ledger；对应的 A2 OS-verified counts 明确保留为未提供：

```yaml
created_files:
  - "RUNTIME_ASSURANCE_PROFILE_DECISION.md"

controller_a1_action_ledger:
  existing_documents_modified: 0
  runtime_prototype_files_modified: 0
  runtime_tests_executed: 0
  r2_executed: 0
  r3_executed: 0
  r4_executed: 0
  candidate_runs_executed: 0
  candidate_analysis_executed: 0
  english_tei_content_reads: 0
  greek_tei_content_reads: 0
  story_structure_yaml_created: false
  character_outputs_created: 0
  event_outputs_created: 0
  theme_outputs_created: 0
  adaptation_or_script_outputs_created: 0

a2_os_verified_counts:
  status: "NOT_PROVIDED"
  existing_documents_modified: null
  runtime_prototype_files_modified: null
  runtime_tests_executed: null
  candidate_runs_executed: null
  candidate_analysis_executed: null
  english_tei_content_reads: null
  greek_tei_content_reads: null
  business_outputs_created: null
```

本 ADR 不授权 Runtime、R2/R3/R4、Candidate Run 或任何正文读取。其唯一架构结论是：未来开发路径采用明确的 Portable A1/non-certified Profile，未来认证路径继续采用定义不变的 Hardened A3 Profile；两者不得互相替代。
