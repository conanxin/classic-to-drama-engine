# Classic-to-Drama Engine：Runtime Capability Prototype Repair Plan

> 项目：Classic-to-Drama Engine  
> 阶段：Phase 2-G-R  
> 文档类型：Runtime Capability Prototype Repair Plan  
> 日期：2026-08-11  
> 文档状态：`ready_for_review`  
> 当前效力：`repair_plan_only / runtime_unchanged / tests_not_executed / not_authorized`  
> 关联 Prototype Suite：`RCPTS-20260811-002`  
> 关联结果：`BLOCKED_RUNTIME_CAPABILITY_PROTOTYPE_FAILED`  
> 关联 Candidate Run：`AC-20260811-STORYSTRUCT-002`  
> Candidate 正文读取授权：否  
> Formal Phase 2 授权：否

## 0. 目的、依据与本阶段边界

本文为 Phase 2-G 暴露的 Runtime Capability Prototype 缺口制定关闭式修复计划。修复目标不是把已有的 99 个 PASS leaf 重新解释为整体 PASS，而是明确下一次 synthetic prototype run 之前必须完成的环境、schema、snapshot closure 与端到端证明条件。

本文只依据以下三份文件：

| 依据文件 | 本阶段读取时 SHA-256 | 用途 |
| --- | --- | --- |
| `RUNTIME_CAPABILITY_PROTOTYPE_RESULT.md` | `6811bcc4ef0efcaee89013648dd0bb06bbaca154625f3dc47bdfa0f295851753` | Phase 2-G 的真实枚举、PASS/FAIL、blocker 与已有证据边界 |
| `RUNTIME_CAPABILITY_PROTOTYPE_PLAN.md` | `e799d2713f1d013b9433aa35a755ba751e7953a4c560dc9fdb80022bebfcb6fa` | 五组件、37 个 requirement groups、synthetic fixture、测试布局及 fail-closed 验收合同 |
| `CANDIDATE_EXECUTION_CONTRACT_REPAIR.md` | `12ceb01cab4901cb2b7472b1b56f93750a43cb8c28b5f0c9ab89acf3ad4fe7bd` | authorization、snapshot、signed profiles、两阶段 audit 与新 Candidate Run Gate |

### 0.1 Phase 2-G 的冻结事实

以下数字来自 Phase 2-G 的冻结 manifest 与 runner aggregate，不在本文中重新枚举或重算：

| 指标 | 冻结值 |
| --- | ---: |
| Requirement groups | 37 |
| Manifest leaves | 197 |
| Runner discovered / executed / evidence-complete | 197 / 197 / 197 |
| PASS / FAIL | 99 / 98 |
| Skip / Unknown | 0 / 0 |
| 独立 grants | 181 |
| 完全通过 / 含失败的 groups | 21 / 16 |

旧 suite `RCPTS-20260811-002` 的结论永久保持：

```yaml
suite_id: "RCPTS-20260811-002"
result: "BLOCKED_RUNTIME_CAPABILITY_PROTOTYPE_FAILED"
mutable_for_repair: false
leaf_results_may_be_reclassified: false
spent_grants_may_be_reused: false
evidence_may_be_rewritten: false
eligible_as_future_pass_evidence: false
eligible_as_historical_regression_evidence: true
```

### 0.2 本阶段唯一产物

本阶段只创建：

```text
RUNTIME_CAPABILITY_REPAIR_PLAN.md
```

本阶段不会：

- 修改 `runtime_capability_prototype/` 中任何 implementation、schema、manifest、fixture recipe、suite、case、evidence、attestation、aggregate 或 report；
- 执行 prototype test、monitor qualification、runner、audit verifier 或 Candidate Run；
- 创建新的 `RCPTS-*` suite、`RCPT-*` attempt、grant、capability、delivery 或 attestation；
- 打开、扫描、解析、stat、hash 或复制 Odyssey English TEI；
- 打开、扫描、解析、stat、hash、复制或挂载 Greek TEI；
- 创建 `story_structure.yaml`、Candidate `execution_report.md` 或 Candidate Run 目录；
- 创建人物、事件、主题、母题、改编、分集、场景、对白或剧本数据；
- 分配或规划新的 Candidate Run ID；
- 改写 Run 002 或 Formal Phase 2 的状态。

### 0.3 计划效力

本文只定义未来修复的顺序、接口与成功标准。本文完成不表示：

- PID／`/proc` 可观测性已经修复；
- ptrace、eBPF、audit 或其他 OS observer 已可用；
- authorization schema 已修改或 181 个旧 artifact 已迁移；
- component freeze 已形成传递闭包；
- Book 1 positive path 已通过；
- Runtime Prototype 已取得 PASS；
- B-overlay、production runtime 或 Candidate Run 已获批准。

## 1. Blocker 分类

### 1.1 总表

| Blocker ID | Phase 2-G 原始 code | 类别 | Phase 2-G 事实 | 被阻断的声明 | 修复归属 |
| --- | --- | --- | --- | --- | --- |
| `P2GR-BLK-001` | `BLOCKED_SANDBOX_ISOLATION_UNPROVEN`、`TRACE_MONITOR_UNAVAILABLE_PTRACE_DENIED`、2 个 `UNEXPECTED_EXCEPTION` | 执行环境／外部可观测性 | `Popen.pid` 与挂载的 `/proc/<pid>` 视图不一致；`PTRACE_TRACEME` 被拒；96 leaf fail-closed，另有 2 个 PID 别名碰撞导致 `PermissionError` | consumer sandbox 身份、FD、process tree、syscall coverage、full raw／Greek 零访问与完整 independent audit | `R1` |
| `P2GR-BLK-002` | `AUTHORIZATION_SCHEMA_ARTIFACT_MISMATCH` | Authorization schema／identity | schema 把 `authorization_file_sha256` 错误设为 authorization 文件本体的必填字段；181 个持久 artifact 把该摘要正确保存在文件外 | artifact schema validation、authorization identity 与 downstream binding 的一致性 | `R2` |
| `P2GR-BLK-003` | `COMPONENT_FREEZE_TRANSITIVE_CLOSURE_INCOMPLETE` | Runtime snapshot／供应链闭包 | 冻结 manifest 的 12 项摘要均匹配，但未覆盖 `common.py`、`verify_trace.py`、`build_manifest.py`、package initializer 等传递依赖 | “执行与审计代码完整冻结、无未登记代码参与”的声明 | `R3` |
| `P2GR-BLK-004` | `Book 1 E2E proof gap`（由以上 blocker 派生） | 端到端验收／派生缺口 | broker 已完成一次 `[4076,36515)`、32,439-byte `pread`，但 bounded reader 在 OS supervisor 处 fail-closed | Book 1 从一次性授权到 reader/parser/gateway/audit closure 的 E2E PASS | `R4` |

`P2GR-BLK-004` 不是孤立的第四个根因。它是 `P2GR-BLK-001..003` 尚未关闭后产生的最终验收缺口；因此不得只重跑 T01 或放宽 supervisor 来“修复” Book 1 E2E。

### 1.2 PID／ptrace／audit evidence limitation

#### 已有证据

- 当前环境无法用 `Popen.pid` 在可见 `/proc` 中稳定定位被监督进程；
- supervisor 无法可靠读取 child 的 `status`、`root` 与 FD inventory；
- `strace -ff` 可执行文件虽存在，但 ptrace 探针以 `Operation not permitted` 终止；
- 两个 signed-profile leaf 因 PID 别名碰撞后的 FD inspection 权限错误而保留为真实 FAIL；
- external monitor 未启动，所以 real English／Greek 的 stat/open/read/hash/parse/copy 与 source-tree scan 计数保持 `unknown`，没有伪写为 0。

#### 分类决定

该问题属于 `environment_capability_and_observer_identity_blocker`，不是普通测试期望值错误，也不是可以通过应用层日志补齐的报告缺字段。

#### 不可接受的“修复”

- 根据 PID 数值相近猜测 host／namespace 映射；
- 遇到 `/proc/<pid>` 不存在时跳过 FD 检查；
- 把 probe stdout、自报 JSON 或 signed runtime event 当成 OS process-tree proof；
- 把 ptrace unavailable 降级为 warning；
- 只证明 seccomp filter 已安装，却不证明 child、继承 FD、子进程与第二通道均在 observer 覆盖内；
- 将 `unknown` 归零；
- 为提高通过率删除 T14、T15、T17、T30 或相关 leaf。

#### 正确修复方向

下一次 suite 必须运行在经过独立 qualification 的 observer backend 上。可以使用 ptrace/strace、eBPF、Linux Audit、fanotify 加 process/cgroup correlation，或语义等价的内核边界 observer；技术名称不是 PASS 条件，完整覆盖与不可由被测进程篡改才是 PASS 条件。

### 1.3 Authorization schema mismatch

#### 已有证据

Runtime 的正确设计已把 immutable authorization bytes 与 mutable registry state 分离，并把完整文件 SHA-256 存在 authorization 文件之外；错误发生在 `contracts/authorization_schema.yaml` 仍要求文件把自身完整摘要写入自身。

#### 风险

- self-digest 无有限稳定值；
- 若按 schema 强行写入，会形成递归 identity；
- 若不写入，181 个 artifact 无法通过正式 schema validation；
- 若 schema validator 未实际运行，suite 可能对无效 artifact 产生空洞 PASS。

#### 分类决定

这是 `deterministic_contract_defect`。必须通过 breaking schema revision 关闭；不得回填旧 artifact，不得删除 schema validation，也不得把 validation failure 标为 cosmetic。

### 1.4 Component freeze closure gap

#### 已有证据

当前 component manifest 只能证明已列出的 12 个 artifact 在执行后没有摘要漂移。它没有证明所有参与 manifest 构建、runtime 共用逻辑、package 初始化、trace verification 或其他动态加载依赖均已列入。

#### 风险

- 未冻结依赖可以改变 authorization、range、audit 或 aggregation 语义；
- manifest generator 自身变化可能改变 leaf 布局而未被记录；
- external audit verifier 变化可能让相同 evidence 得到不同结论；
- “12/12 摘要匹配”可能被错误解释为“传递闭包完整”。

#### 分类决定

这是 `reproducibility_and_integrity_closure_defect`。修复必须从 entrypoints 自动求传递闭包，并将平台边界与动态加载观测显式化；不能只把当前已知的四个漏项手工追加后宣称闭合。

### 1.5 Book 1 E2E proof gap

#### 已有证据

- broker 侧已实际完成一次唯一范围读取；
- read union 精确等于 `[4076,36515)`，长度为 32,439 bytes；
- consumer delivery、sandbox inventory、parser scope 与 terminal independent audit 没有形成同一 positive attempt 的闭合 PASS。

#### 尚未证明

- bounded reader 只收到 sealed Book 1 slice，且没有 full fixture path／FD／mount；
- consumer process tree 的所有成员均受 sandbox 与 observer 覆盖；
- parser 只观察 `BOOK_01`、10 Card 与 10 Paragraph markers；
- prefix／Book 2／Greek sentinels 在 consumer、parser、gateway 中均不可见；
- scope attestation 与 closure attestation 绑定同一 authorization、CAS event、capability 与 delivery；
- full raw、Greek 与第二读取通道的成功访问为 OS 级可证明的 0。

#### 分类决定

这是 `combined_acceptance_gap`。只有 R1、R2、R3 均 PASS 后，才允许以全新 suite、attempt 与 grant 执行 R4。

### 1.6 已有局部证据的处理

以下 Phase 2-G 证据可作为修复后的 regression expectation，但不能直接计入下一次 suite PASS：

- missing／invalid／expired／replay authorization 拒绝；
- 并发双 CAS 单赢家；
- CAS 后崩溃仍保持 spent；
- Book 2 broker-range 拒绝；
- formal loader 正向、负向与 TOCTOU 行为；
- 2,742 个 evidence-manifest 条目的存在性／size／digest；
- 1,379 个 signed event 的 JSON、签名、attempt/domain/sequence/hash chain；
- 394 个 audit JWS 的 signature 与 attempt binding。

下一次 suite 因 schema、snapshot closure、observer backend 或 component identity 发生变化，必须重新执行全部 mandatory leaf；不得只重跑原 98 个 FAIL。

## 2. 修复优先级：R1／R2／R3／R4

### 2.1 优先级总表

| 优先级 | 工作包 | 目标 | 进入条件 | 退出条件 | 未通过时允许动作 |
| --- | --- | --- | --- | --- | --- |
| `R1` | OS Evidence Backend Qualification | 建立稳定 PID/process-tree/FD/syscall/write 可观测边界 | 仅 synthetic monitor probe；不需要 fixture payload | qualification 全项 PASS，observer identity 与环境 fingerprint 冻结 | 更换／修复测试环境；不得启动 suite |
| `R2` | Authorization Schema V2 | 消除 self-digest，闭合 immutable artifact 与外部 registry identity | R1 可并行准备；不得修改旧 suite | 新 schema、registry binding 与正反 schema tests PASS | 继续修 schema；不得迁移或回写旧 grant |
| `R3` | Runtime Snapshot Transitive Closure | 冻结所有执行、构建、验证、policy 与动态依赖 | R2 schema identity 已确定；entrypoints 已冻结 | closure DAG 无未分类节点，start/end/dynamic checks 均 PASS | 扩展 closure；不得启动新 suite |
| `R4` | Fresh Synthetic E2E Prototype Run | 用全新 suite 证明 Book 1 positive path 与全部拒绝链 | R1、R2、R3 均 PASS | 全部 success criteria PASS | 输出真实 BLOCKED/FAIL；不得规划 Candidate Run |

### 2.2 依赖规则

```text
R1 PASS ─┐
R2 PASS ─┼──> R4 may start
R3 PASS ─┘
```

- R1 是环境硬门槛，应最先资格审查，避免在不可能产生 OS proof 的环境中再次运行 197 级别的 suite；
- R2 与 R1 的实现准备可以并行，但 R2 的验证不得借用不合格 observer 声称 OS proof；
- R3 必须包含 R2 最终 schema、validator 与 registry binding implementation，因此其最终 freeze 晚于 R2；
- R4 必须使用 R3 冻结的同一 closure，不得在 suite 运行中修改 component、schema、policy、fixture recipe、observer 或 verifier；
- 任一 repair exit condition 为 `unknown`，视为未通过。

### 2.3 R1 — OS Evidence Backend Qualification

R1 必须使用无文学内容的小型 probe，在新 suite 创建前证明：

1. controller、observer、broker probe 与 consumer probe 共享可验证的 process identity 关联；
2. observer 可覆盖完整 child process tree，而不是只覆盖初始 PID；
3. `/proc` 路径、PID namespace inode、start time、cgroup ID 或等价稳定 identity 不发生别名碰撞；
4. observer 能独立读取／记录 consumer root、mount namespace、FD inventory、UID/GID map、`NoNewPrivs` 与 seccomp state；
5. observer 能观察或内核拒绝 `open/openat/openat2/read/pread64/mmap/sendfile/splice/vmsplice/tee/copy_file_range/io_uring_setup/io_uring_enter` 等输入通道；
6. observer 能观察 process creation、exec、exit、signal 与尝试逃逸的子进程；
7. observer 能观察网络 socket 与写入路径；
8. event loss、late start、process escape、permission failure 和 observer crash 均可检测并 fail closed；
9. observer 在任何 broker object open 前完成 ready handshake；
10. 被测进程没有修改、截断或删除 observer evidence 的权限。

若 ptrace 在目标环境被禁止，可换用满足相同覆盖合同的外部内核 observer；不得仅换一个工具名而缩小观测域。

R1 的最终资格记录至少冻结：

```yaml
observer_backend_id: "<id>"
observer_backend_version: "<version>"
observer_backend_digest: "<sha256>"
host_or_image_identity: "<immutable identity>"
kernel_identity: "<version and build identity>"
pid_namespace_identity: "<identity>"
mount_namespace_identity: "<identity>"
process_scope_mechanism: "<pid namespace | cgroup | equivalent>"
syscall_coverage_profile: "<closed profile id and digest>"
event_loss_count: 0
qualification_result: "PASS"
```

### 2.4 R2 — Authorization Schema V2

R2 按第 3 节实施。旧 schema 与旧 suite 保留原样；新 schema 使用新的 identity/version，所有新 authorization-related leaf 使用全新 grant。

### 2.5 R3 — Runtime Snapshot Transitive Closure

R3 按第 4 节实施。闭包不是手工文件表，而是 roots、nodes、edges、platform boundary 与动态加载复核的组合。

### 2.6 R4 — Fresh Synthetic E2E Prototype Run

R4 按第 6、7 节执行。它不是 Candidate Run，不读取真实来源，不复用旧 suite 的 authorization、capability、delivery、nonce、attestation、test key usage state 或 case result。

## 3. Authorization Schema 修复方案

### 3.1 修复原则

Authorization 的三个对象必须分离：

| 对象 | 是否不可变 | 保存内容 | 是否包含 authorization 文件自身 SHA-256 |
| --- | --- | --- | --- |
| `prototype_authorization.yaml` | 是 | 授权 claims、attempt、fixture、range、expiry、禁止角色 | 否 |
| external registry identity record | append-only／状态独立 | exact authorization file bytes 的 SHA-256、size、schema identity、注册事件 | 是 |
| external mutable consumption state | 状态机 | `unconsumed/spent/revoked/expired`、CAS event | 通过 registry identity 引用，不写回 artifact |

完整 authorization 文件摘要只能由外部 registry identity record、capability、envelope、attestation 与 case report 引用；不得写入 authorization 文件本体。

### 3.2 Breaking schema revision

未来实现必须新建 breaking revision，例如：

```yaml
schema_id: "CTDE-RCPT-AUTHORIZATION-SCHEMA-2"
schema_version: "2.0.0"
artifact_class: "runtime_capability_test_authorization"
self_digest_field_allowed: false
external_identity_binding_required: true
```

版本号与最终 identity 由未来实现冻结；本文不创建 schema 文件。

V2 必须：

- 从 authorization artifact 的 required／optional properties 中移除 `authorization_file_sha256`；若 artifact 出现该字段，schema validation 必须拒绝，避免混用 V1 语义；
- 要求稳定的 `authorization_id`、`attempt_id`、`environment=prototype_fixture_only`、`fixture_object_id`、structure-contract identity、唯一 range、expected length、expected synthetic slice hash、expiry、one-time、no-retry 与 forbidden source roles；
- 禁止真实 source object ID、真实 source checksum、真实 Book 1 slice checksum、`AC-*` Run ID 与 production key identity；
- 使用 safe-mode、single-document、duplicate-key rejection 与 JSON-compatible YAML 子集；
- 在 registry registration 之前实际执行 schema validation；
- 将 exact immutable file bytes、size、schema ID/version 与 SHA-256 作为一个不可分割的 registry identity；
- 将 registry identity 与 mutable CAS state 分表或以等价隔离实现，禁止消费状态回写 artifact；
- 使 capability、broker envelope、scope attestation、closure attestation 与 case result 都绑定同一 external `authorization_file_sha256`。

### 3.3 Identity 生成顺序

```text
build immutable authorization bytes
  -> safe parse
  -> V2 schema validate
  -> freeze exact bytes
  -> SHA-256(exact bytes)
  -> register immutable identity
  -> create unconsumed state
  -> CAS unconsumed -> spent
  -> mint capability bound to digest + CAS event
```

顺序规则：

1. schema validation 失败时不得注册 identity；
2. identity 注册后 artifact bytes 不得变化；
3. runtime 读取时必须重新计算 exact file SHA-256，并与 registry identity 比较；
4. CAS 必须同时匹配 authorization ID、file digest、attempt ID 与 `state=unconsumed`；
5. CAS commit 前 capability 数必须为 0；
6. CAS commit 后即使 issuer 崩溃，state 仍为 spent，不补发、不回退；
7. capability payload 可以引用 authorization file digest，但不得引用可写路径或 mutable authorization bytes；
8. authorization file digest 变化必须产生新的 authorization ID、attempt 与 suite，不得更新 registry 原记录。

### 3.4 Schema 闭合范围

R2 不能只修改一个 required 字段。以下 binding 必须一起核对：

- authorization artifact schema；
- registry identity record schema；
- registry consumption-event schema；
- capability claims schema；
- broker envelope schema；
- scope／closure attestation schema；
- manifest leaf `grant_required` 与 grant identity；
- case result 与 suite aggregate 的 authorization evidence fields；
- independent audit verifier 的 digest-location 规则。

### 3.5 旧 artifact 处理

- 181 个 Phase 2-G authorization artifact 保持原字节与原 digest；
- 不向旧 artifact 写入 self-digest；
- 不把旧 artifact 批量重标为 V2；
- 不修改旧 registry consumption state；
- 旧 artifact 只作为 `schema_mismatch_historical_evidence`；
- 新 suite 每个 authorization-related leaf 均生成新的 V2 grant；
- missing-authorization 与 formal-loader-only leaf 继续按 manifest presence matrix 合法缺少 authorization，但 absence reason 必须闭合。

### 3.6 R2 验收标准

| ID | PASS 条件 |
| --- | --- |
| `P2GR-R2-001` | V2 schema 不要求且禁止 artifact 内的 self-digest 字段 |
| `P2GR-R2-002` | 一个合法 authorization artifact 经真实 validator PASS 后才可注册 |
| `P2GR-R2-003` | external registry digest 等于 exact artifact bytes SHA-256，size 与 schema identity 匹配 |
| `P2GR-R2-004` | artifact 注册后任一字节变化均在 CAS／mint 前拒绝 |
| `P2GR-R2-005` | missing／invalid external identity、digest mismatch、schema mismatch 均产生精确 blocker 且 capability/read/delivery 为 0 |
| `P2GR-R2-006` | capability、envelope、scope 与 closure objects 绑定同一 authorization digest |
| `P2GR-R2-007` | 并发双 CAS 恰好一名赢家；CAS 后崩溃仍为 spent |
| `P2GR-R2-008` | independent verifier 实际执行 schema validation，不接受“文件已生成”作为替代证据 |

任一项未通过，R2 不得标记 PASS。

## 4. Runtime Snapshot Closure 方案

### 4.1 闭包目标

Runtime snapshot 必须证明：所有可以影响 suite 枚举、authorization、capability、broker range、reader sandbox、formal loader、audit evidence、aggregate 与最终判断的 project-owned bytes 均已冻结；所有平台依赖均已明确落在受控 boundary 内。

### 4.2 Closure roots

未来 closure builder 至少从以下 roots 开始：

- suite manifest builder 与 runner entrypoint；
- authorization registry、issuer 与 signed-object implementation；
- range broker 与 bounded reader；
- sandbox supervisor、native probe 及其 build inputs；
- parser scope、model gateway、write monitor 与 formal loader；
- read-audit aggregator、event signer、scope/closure attestation builder；
- independent artifact／trace verifier；
- aggregate 与 report generator；
- schema、test policy、fixture recipe、component policy 与 public trust material；
- package initializers 与所有共享模块。

当前已知漏项 `common.py`、`verify_trace.py`、`build_manifest.py` 与 package initializer 必须进入闭包，但“加入这四项”本身不等于闭包已完成。

### 4.3 Closure node 类型

每个 node 必须标记类型与身份：

| Node class | 示例 | 冻结要求 |
| --- | --- | --- |
| `project_source` | Python/shared module/package initializer | relative path、size、SHA-256 |
| `native_source` | sandbox probe C/Rust source | path、size、SHA-256 |
| `native_binary` | 编译后的 probe／helper | binary SHA-256、build recipe、link mode |
| `contract_schema` | authorization/capability/envelope/audit schema | schema ID/version、file SHA-256 |
| `runtime_policy` | seccomp、sandbox、test policy | policy ID/version、SHA-256 |
| `control_generator` | manifest/snapshot/report builders | path、version、SHA-256 |
| `verification_code` | trace/artifact/signed-object verifier | path、version、SHA-256 |
| `fixture_definition` | generator、recipe、structure contract | identity、seed contract、SHA-256；不得含 payload |
| `public_trust_material` | public keys／key status | key ID、algorithm、SHA-256 |
| `platform_boundary` | interpreter、stdlib、kernel、libc、image | immutable fingerprint 或明确外部 boundary |

Private keys、ephemeral fixture payload、sealed slice 与 transient registry state 不进入可公开 component snapshot；它们只记录 key ID／custody boundary 或 ephemeral identity。

### 4.4 Closure discovery 算法

未来 builder 必须执行以下过程：

1. 从冻结 entrypoints 解析 project-owned static imports 与直接 file/config/schema references；
2. 递归加入 package initializer、shared module、helper、generator、validator、template 与 native build input；
3. 对动态 import、plugin lookup、subprocess executable、shared-library load 与运行时打开的 code/config path 建立 allowlist；
4. 在无正文 closure probe 中记录实际 loaded modules、executables、libraries 与 code/config opens；
5. 将实际加载集合与静态 closure 比较；任何未登记 project-owned node、未分类 executable 或未知 dynamic load 均 fail closed；
6. 对 Python interpreter、stdlib、native ABI、libc、kernel 与 container/VM image 建立 platform boundary fingerprint；
7. 生成有向依赖图 `roots -> nodes -> edges`，每个 edge 说明 `import/build/load/configure/verify` 关系；
8. 对排序后的 canonical graph 计算 closure digest；graph 不包含自己的完整文件摘要，snapshot 文件 SHA-256 由外部 suite registry 保存；
9. suite manifest 创建前冻结 closure；suite 启动和结束时分别复算所有 node；
10. suite 执行期间出现 closure delta、mtime-only replacement 后 digest 变化、未知 module 或 verifier 漂移，整套 suite invalidated。

### 4.5 Canonical closure identity

未来实现必须定义版本化 canonicalization，例如：

```yaml
closure_profile: "CTDE-RUNTIME-CLOSURE-C14N-1"
roots: []
nodes: []
edges: []
platform_boundary: {}
dynamic_load_allowlist: []
closure_payload_sha256: "<digest excluding this field>"
```

要求：

- path 使用相对 prototype root 的规范形式；拒绝 `..`、symlink ambiguity 与重复 node identity；
- nodes 按稳定 ID 排序，edges 按 `(from,to,relation)` 排序；
- 每个 project-owned regular file 使用完整文件字节 SHA-256；
- native binary 同时绑定 source、compiler identity、flags、link inputs 与最终 binary digest；
- platform boundary 不能写 `system`、`current`、`unknown` 等不可复核值；
- closure manifest builder 与 verifier 自身都作为 nodes 被其他独立 control-plane checker 复核；
- 最终 snapshot 文件摘要由外部 registry 保存，不形成 self-hash。

### 4.6 R3 验收标准

| ID | PASS 条件 |
| --- | --- |
| `P2GR-R3-001` | entrypoints、roots、node types 与 platform boundary 均有关闭式定义 |
| `P2GR-R3-002` | 当前已知四类漏项全部进入 graph |
| `P2GR-R3-003` | static discovery、dynamic load observation 与实际 code/config open 集合一致 |
| `P2GR-R3-004` | 未登记 project-owned loaded bytes、unknown dynamic dependencies 与 unresolved symlink 均为 0 |
| `P2GR-R3-005` | native probe 的 source→build recipe→binary 闭合 |
| `P2GR-R3-006` | schema、policy、manifest builder、runner、audit verifier、aggregate/report generator 全部冻结 |
| `P2GR-R3-007` | start/end 全量 digest 复算一致，执行期间 closure delta 为 0 |
| `P2GR-R3-008` | closure payload digest、snapshot file digest 与 external registry identity 可独立复算 |

任何手工声明的“文件数齐全”不能替代 graph 与动态加载闭合。

## 5. Audit Evidence 分级方案

### 5.1 Evidence tiers

| Tier | 名称 | 证据来源 | 可以证明 | 不能单独证明 |
| --- | --- | --- | --- | --- |
| `A0` | `unknown_or_unobserved` | observer 未启动、丢事件、字段缺失或无法关联 | 只能证明证据不可用 | 任何零访问、隔离或 PASS |
| `A1` | `runtime_logical_proof` | registry、issuer、broker、reader、parser、gateway、formal loader 的签名事件／attestation | 合同状态机、claim validation、requested/returned range、parser/gateway/formal 逻辑结果 | consumer 没有其他 path/FD、未通过未监控 syscall 访问、完整 process tree 受控 |
| `A2` | `os_level_proof` | 被测进程无写权限的 kernel／supervisor observer | process tree、PID/namespace/root/mount/FD、syscall、network、write 与第二通道的实际覆盖 | authorization claims 是否语义正确、parser marker 或 signed-object binding 是否正确 |
| `A3` | `combined_runtime_and_os_proof` | 同一 attempt 上 A1 与 A2 的可验证关联 | 既证明逻辑合同，也证明无旁路能力；用于关键 suite acceptance | 真实 production runtime 或 Candidate authorization |

`A2` 不是 `A1` 的替代品，`A1` 也不能升级冒充 `A2`。关键能力通常要求 `A3`。

### 5.2 Claim-to-tier matrix

| Claim | 最低 tier | 额外条件 |
| --- | --- | --- |
| authorization 存在、schema 合法、CAS 一次性 | `A1` | registry evidence 独立于 consumer，artifact digest 外置且闭合 |
| capability/envelope/JWS profile 正确 | `A1` | signature、issuer、audience、time、nonce、anti-replay 全验证 |
| broker actual union 恰为 Book 1 range | `A3` | A1 broker calls 与 A2 broker syscall/process evidence 同一 attempt |
| bounded reader 只收到 sealed slice | `A3` | envelope/delivery logical proof + consumer FD/mount/process OS proof |
| consumer 无 full fixture path／handle | `A2`，suite 总结要求 `A3` | 完整 process tree、FD、mount、open/handle syscalls 全覆盖 |
| Book 2 不可访问 | `A3` | broker logical deny + consumer/parser/gateway OS/logic coverage |
| Greek 不可访问 | `A3` | 非真空 synthetic Greek existence proof + broker deny + consumer OS coverage |
| parser 只见 Book 1／10 Card／10 Paragraph | `A1`，E2E 要求 `A3` | parser proof 与同一 sealed delivery、OS consumer identity 关联 |
| model invocation 为 0 | `A3` | gateway event + process/network/exec coverage |
| formal loader exclusion | `A1`，write/path escape 要求 `A3` | signed positive control、negative entries、TOCTOU 与 OS file evidence |
| real English／Greek access count 为 0 | `A2`，suite 总结要求 `A3` | project/source visibility、process tree、syscall coverage与 event loss 均闭合 |

### 5.3 A1 runtime logical proof 要求

每个 runtime event／attestation 至少绑定：

```yaml
suite_id: "<fresh RCPTS id>"
leaf_case_id: "<leaf id>"
attempt_id: "<fresh RCPT id>"
authorization_file_sha256: "<digest or explicit absent>"
consumption_event_id: "<id or explicit not_issued>"
capability_id: "<id or explicit not_issued>"
delivery_id: "<id or explicit not_issued>"
component_id: "<id, version, digest>"
closure_snapshot_sha256: "<external snapshot digest>"
event_sequence: "<monotonic integer>"
previous_event_sha256: "<digest or genesis>"
observed_value: "<actual value; never default zero>"
```

要求：

- event writer 与 consumer 权限分离；
- rejected case 只有精确 blocker、真实副作用计数和 terminal closure 齐全时才算 test PASS；
- missing observer／not reached 使用明确状态，不创建空 evidence；
- signed event chain、scope attestation 与 closure attestation 的 verifier 必须属于 R3 closure；
- A1 只能陈述被 instrumentation 覆盖的逻辑事实。

### 5.4 A2 OS-level proof 要求

OS evidence 必须包含：

- observer ready time，且早于 broker object open；
- stable process identity：PID namespace、start time 与 cgroup/process-tree correlation；
- root、mount namespace、UID/GID map、capabilities、`NoNewPrivs`、seccomp state；
- 启动时与终止时 FD inventory，以及 FD open/dup/pass/close events；
- process create/exec/exit 与所有 descendants；
- source-read syscalls、memory/file transfer syscalls、io_uring、handle/pidfd/process-vm 与网络取源通道；
- write/create/rename/link/symlink/unlink 行为；
- observer coverage start/end、dropped/lost events、decode errors 与 permission failures；
- raw trace 或规范化 trace 的 immutable digest、observer identity 与 attempt correlation；
- 被测 consumer 对 trace store 的写权限为 0。

以下任一情况使 A2 降为 A0，而不是“部分 A2”：

- PID 或 process tree 无法唯一关联；
- child 在 observer ready 前启动或 source open 早于 ready handshake；
- `/proc`、cgroup 或 namespace identity 发生未解释碰撞；
- ptrace/eBPF/audit permission 被拒；
- descendant、FD passing、io_uring 或约定的第二通道未覆盖；
- dropped events 非 0 或未知；
- observer 意外终止、trace 不完整或 digest 无法验证；
- 任何必须为整数的 access count 为 `unknown`。

### 5.5 两阶段聚合

`prototype_scope_execution_attestation` 必须在 positive result 判为 PASS 前绑定：

- A1 broker、reader、parser 与 gateway evidence；
- A2 process-tree、FD、mount、syscall 与 network evidence；
- 同一 authorization、CAS event、capability、delivery 与 closure snapshot；
- exact Book 1 union、范围外 bytes、full/Greek access count 与 observer coverage。

`prototype_closure_audit_attestation` 必须进一步绑定：

- scope attestation 的完整 signed-object digest；
- write monitor 与 formal-loader evidence；
- artifact presence、final case status 与 suite identity；
- model invocation、Candidate Run 与 business output 为 0；
- A1/A2 evidence completeness 与 event-loss 状态。

若 A1 PASS、A2 unavailable，case 结果必须是 `BLOCKED_OS_PROOF_UNAVAILABLE`；不得记为 partial PASS 后由 suite aggregate 忽略。

## 6. Book 1 E2E Proof 修复方案

### 6.1 新 positive attempt

R4 必须为 Book 1 positive path 创建全新的 leaf、`RCPT-*` attempt 与 V2 grant。不得复用旧 T01 的 authorization、spent state、capability、delivery、memfd、events 或 attestations。

### 6.2 端到端顺序

1. 验证 R1 qualification identity 与 R3 closure snapshot；
2. 创建无文学内容的 deterministic synthetic full fixture、Book 1 allowed range与非真空 synthetic Greek deny object；
3. 生成 V2 authorization，真实 schema validation 后登记外部 file digest；
4. 启动 A2 observer 并完成 ready handshake；
5. 启动 consumer sandbox，独立核对 root/mount/FD/process/security state；
6. registry 原子 CAS `unconsumed -> spent`；
7. issuer 签发只绑定 synthetic fixture 与 `[4076,36515)` 的 opaque capability；
8. broker 以 fixed-offset/fixed-length API 读取 32,439 bytes，A1/A2 同时记录实际 calls；
9. broker 验证 synthetic slice digest，生成 sealed immutable handle 与 signed envelope；
10. bounded reader 验证 envelope、seal、length、digest、delivery one-shot 与 attestation binding；
11. parser probe 只验证 `BOOK_01`、10 Card、10 Paragraph structural markers；
12. discard-only gateway 只记录 scope，模型调用保持 0；
13. aggregator 生成 A3 scope attestation；
14. formal loader 与 write monitor 完成 closure checks；
15. aggregator 生成 A3 closure attestation，case controller 封存 result；
16. suite controller 验证 closure snapshot 未漂移后再聚合。

任一步失败均终止 delivery／parser／gateway 主路径；terminal audit 分支仍记录真实到达状态。authorization 一旦 CAS 成功即永久 spent。

### 6.3 Positive Book 1 必须同时证明

```yaml
authorized_range:
  start_byte: 4076
  end_byte_exclusive: 36515
expected_length: 32439
broker_actual_union:
  - start_byte: 4076
    end_byte_exclusive: 36515
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
consumer_direct_full_object_open_success_count: 0
model_invocations: 0
business_outputs_created: 0
audit_tier: "A3"
```

### 6.4 与拒绝链共同闭合

Book 1 positive PASS 不能替代以下负向证明：

- Book 2 range／marker 请求在 broker、reader、parser 与 gateway 相应边界被拒绝；
- caller supplied range override、short/long range、EOF/full-hash fallback 被拒绝；
- consumer 对 full fixture host path、继承 FD、第二读取通道与子进程逃逸均失败；
- synthetic Greek deny object 先由 fixture controller 证明非空存在，再证明 authorization、catalog、broker、mount、consumer、parser 与 gateway 全链不可达；
- monitor missing、event loss、PID collision 与 evidence tamper 测试按精确 blocker fail closed。

只有 positive path 与全部 mandatory rejection leaf 在同一 R1/R2/R3 identity 下通过，才能形成 suite PASS。

## 7. 下一次 Prototype Run 的成功标准

### 7.1 Run 前硬门槛

| Gate ID | PASS 条件 | 失败结果 |
| --- | --- | --- |
| `P2GR-NP-001` | R1 monitor qualification 全项 PASS；observer identity 与环境 fingerprint 冻结 | `BLOCKED_OS_PROOF_UNAVAILABLE` |
| `P2GR-NP-002` | Authorization Schema V2 及 external registry binding PASS | `BLOCKED_AUTHORIZATION_SCHEMA_INVALID` |
| `P2GR-NP-003` | R3 transitive closure graph、dynamic load check 与 start digest PASS | `BLOCKED_COMPONENT_CLOSURE_INCOMPLETE` |
| `P2GR-NP-004` | 使用新的 `RCPTS-*` suite ID；旧 suite 完全只读 | `BLOCKED_OLD_SUITE_REUSE_ATTEMPT` |
| `P2GR-NP-005` | suite manifest 在 attempts 前冻结；每个 leaf 有唯一新 `RCPT-*` attempt，authorization-related leaf 有独立 V2 grant | `BLOCKED_TEST_IDENTITY_INVALID` |
| `P2GR-NP-006` | fixture、keys、policy、signed profiles、observer 与 component closure 均为 test-only identity | `BLOCKED_TEST_PRODUCTION_TRUST_MIXED` |
| `P2GR-NP-007` | 真实 English／Greek paths、object IDs、checksums 与 payload 未进入 fixture、manifest、token或环境 | `BLOCKED_REAL_SOURCE_BINDING_DETECTED` |

任一 Run 前 Gate 失败时，不启动完整 suite，不生成 PASS report，不创建 Candidate Run。

### 7.2 Manifest 与 runner 闭合

下一次 suite 的测试总数必须由新 manifest 与 runner 实际枚举。不得把旧值 `197` 或计划中的 `37` 手工当作 leaf 总数。

设新 manifest leaf count 为 `N`，成功必须满足：

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
timed_out: 0
duplicate_attempt_ids: 0
cross_case_grant_reuse: 0
```

如果修复导致复合向量新增 leaf，`N` 可以不同于 197；报告只能从冻结 manifest 与 runner aggregate 读取 N。

### 7.3 能力成功标准

| Acceptance ID | 必须证明 | 所需 evidence |
| --- | --- | --- |
| `P2GR-AC-001` | Book 1 positive path 从 V2 authorization 到 closure 全链 PASS | A3 |
| `P2GR-AC-002` | broker actual union 恰为 `[4076,36515)`，返回 32,439 bytes，范围外 bytes 为 0 | A3 |
| `P2GR-AC-003` | Book 2 range、marker、parser与gateway输入不可达 | A3 |
| `P2GR-AC-004` | consumer 无 full fixture path、mount、FD、catalog、network或第二 broker通道 | A3 |
| `P2GR-AC-005` | non-empty synthetic Greek object 在 authorization、broker、sandbox、parser、gateway 全链不可达 | A3 |
| `P2GR-AC-006` | authorization 缺失、错误、过期、replay 均在 read前拒绝；并发 CAS 单赢家；crash 后保持 spent | A1，关键进程行为由 A2 关联 |
| `P2GR-AC-007` | authorization-related artifacts 100% 通过 V2 schema；external file digest 100% 匹配 | A1 |
| `P2GR-AC-008` | capability/envelope/attestation 的 alg/typ/kid/version/issuer/audience/time/anti-replay profile 全部正反测试 PASS | A1 |
| `P2GR-AC-009` | bounded reader 只消费一次 sealed slice，delivery replay、tamper与unsafe parser均拒绝 | A3 |
| `P2GR-AC-010` | 五域 audit 完整，A1/A2 同 attempt 关联，event loss、unknown与late-start为 0 | A3 |
| `P2GR-AC-011` | formal positive control 恰为 1；Candidate/prototype/link/copy/rename/TOCTOU 输入均为 0 | A1/A3 按路径行为闭合 |
| `P2GR-AC-012` | workspace/formal/unallowlisted writes、payload persistence与trace tamper为 0 | A3 |
| `P2GR-AC-013` | R3 closure start/end digest一致；未登记 loaded code/config与platform drift为 0 | A1 + external closure verifier |
| `P2GR-AC-014` | test trust root 与 production trust root 双向拒绝 | A1 |
| `P2GR-AC-015` | Candidate Runs、model invocations、business outputs、`story_structure.yaml` 均为 0 | A3 |

### 7.4 零真实来源证明

只有 A2 coverage 完整、process/source visibility 与 event loss 均闭合时，下一次 report 才可以把以下字段写为整数 0：

```yaml
english_real_raw_stat_count: 0
english_real_raw_open_count: 0
english_real_raw_read_count: 0
english_real_raw_hash_count: 0
greek_real_raw_stat_count: 0
greek_real_raw_open_count: 0
greek_real_raw_read_count: 0
greek_real_raw_parse_count: 0
greek_real_raw_copy_count: 0
project_source_tree_scan_count: 0
book_structure_map_read_count: 0
model_invocations: 0
candidate_runs_executed: 0
business_outputs_created: 0
```

若 observer 未覆盖这些对象是否可见、路径是否进入进程或相应 syscall，字段必须保持 `unknown`，suite 总结果必须 BLOCKED。

### 7.5 Suite 最终判定

只有以下全部成立，才允许：

```yaml
prototype_result: "PASS_RUNTIME_CAPABILITY_PROTOTYPE"
r1_os_observer_qualification: "PASS"
r2_authorization_schema: "PASS"
r3_component_transitive_closure: "PASS"
r4_fresh_suite_e2e: "PASS"
all_requirement_groups_passed: true
all_manifest_leaves_passed: true
book1_e2e_passed: true
book2_denied: true
full_object_isolation_proved: true
greek_deny_chain_proved: true
five_domain_combined_audit_passed: true
real_source_access_proved_zero: true
candidate_runs_executed: 0
model_invocations: 0
business_outputs_created: 0
```

判定规则：

- 环境、observer、schema、closure、evidence 或 required field 不可用／unknown：`BLOCKED_RUNTIME_CAPABILITY_PROTOTYPE_FAILED`；
- 已执行组件出现真实安全／范围／授权行为违约：保持 leaf FAIL，并将 suite 标为 `BLOCKED_RUNTIME_CAPABILITY_PROTOTYPE_FAILED`，同时记录精确根因；
- 任何 mandatory leaf fail、skip、unknown、timeout 或 evidence-incomplete：不得 PASS；
- 不允许设置“conditional PASS”“PASS with audit warning”或用 99 个旧 PASS 抵扣新失败。

### 7.6 下一轮结果报告的最低内容

新的 `RUNTIME_CAPABILITY_PROTOTYPE_RESULT.md` 或版本化等价结果必须从实际 artifacts 聚合：

1. 新 suite identity、manifest digest、R3 closure digest与 observer qualification identity；
2. requirement group、manifest、discovered、executed、evidence-complete、PASS/FAIL/skip/unknown/timeout 实际数；
3. R1/R2/R3/R4 各自 Gate 结果；
4. authorization schema validation 与 external digest binding 统计；
5. Book 1 E2E、Book 2、full object、Greek、formal loader 与 write isolation 的 A1/A2/A3 结论；
6. observer coverage、process scope、event loss与任何 unknown 字段；
7. closure roots/nodes/edges 的实际枚举与未登记依赖计数；
8. Candidate Run、model、business output与真实来源访问事实；
9. blockers 与未证明项；
10. 不把 result report 的自身 SHA-256 写回自身；由外部 registry 保存。

## 8. 与 Candidate Run 002 及后续阶段的关系

### 8.1 Run 002 不变

```yaml
run_id: "AC-20260811-STORYSTRUCT-002"
reservation_status: "reserved"
execution_identity_status: "invalid_reserved"
authorization_status: "not_authorized"
execution_status: "not_executed"
last_gate_result: "BLOCKED_BEFORE_CONTENT_READ"
valid_for_future_execution: false
reusable: false
restartable: false
```

本 Repair Plan 不允许：

- 为 Run 002 追加 authorization 或 execution snapshot；
- 在 Run 002 根创建任何文件；
- 把 future Runtime PASS 回填为 Run 002 当时已具备；
- 读取真实 English 来验证 prototype；
- 在 R4 之前或 R4 未 PASS 时规划新的 Candidate Run。

### 8.2 后续顺序

只有新的 Runtime Prototype 达到 `PASS_RUNTIME_CAPABILITY_PROTOTYPE`，才允许恢复以下准备工作：

1. 实现并批准 B-overlay effective policy；
2. 冻结拟投入真实运行的 production component builds、keys、sandbox、audit与formal-loader identities；
3. 使用 production 组合完成无正文 dry run；
4. 创建并批准一份新的 Candidate Run Plan；
5. 按真实授权日期分配新的 Candidate Run ID；
6. 重新冻结 source snapshot、Map、task scope、execution snapshot、output contract与一次性 authorization。

Prototype PASS 仍不是 Candidate authorization，也不允许直接读取 English 或生成 `story_structure.yaml`。

## 9. 本阶段结论与未执行动作

Phase 2-G-R 的修复决定是：先在 R1 建立可独立验证的 OS observer，再用 R2 消除 authorization self-digest contract defect，用 R3 自动冻结完整 Runtime 传递闭包，最后以 R4 的全新 synthetic suite 重新执行全部 mandatory leaf。Book 1 E2E、full raw 隔离、Greek deny 与 independent audit 只有在 A1 runtime logical proof 和 A2 OS-level proof 关联为 A3 后才能 PASS。

```yaml
phase: "Phase 2-G-R"
task: "Runtime Capability Prototype Repair"
document: "RUNTIME_CAPABILITY_REPAIR_PLAN.md"
document_status: "ready_for_review"
current_effect: "repair_plan_only"

runtime_modified_this_task: false
authorization_schema_modified_this_task: false
component_snapshot_modified_this_task: false
observer_backend_qualified_this_task: false
prototype_suite_created_this_task: false
prototype_tests_executed_this_task: 0
candidate_runs_executed_this_task: 0
model_invocations_this_task: 0

english_tei_content_read_this_task: false
greek_tei_content_read_this_task: false
story_structure_output_created_this_task: false
candidate_execution_report_created_this_task: false
character_database_created_this_task: false
event_database_created_this_task: false
theme_database_created_this_task: false
adaptation_or_script_outputs_created_this_task: false

associated_prototype_suite: "RCPTS-20260811-002"
associated_prototype_result_unchanged: "BLOCKED_RUNTIME_CAPABILITY_PROTOTYPE_FAILED"
associated_candidate_run: "AC-20260811-STORYSTRUCT-002"
associated_candidate_run_reusable: false
candidate_run_authorized: false
formal_phase_2_authorized: false
```

本文完成只表示 Runtime Capability Prototype 的修复路径、证据分级与下一轮成功标准已经形成。它不修改 Runtime，不执行测试，不读取真实来源，不生成 Candidate 内容，也不授权任何 Run。
