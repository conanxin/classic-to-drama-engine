# Runtime Capability Prototype Result

Phase: `2-G — Runtime Capability Prototype Implementation`  
Suite: `RCPTS-20260811-002`  
Environment: `prototype_fixture_only`  
Final result: `BLOCKED_RUNTIME_CAPABILITY_PROTOTYPE_FAILED`

本结果没有声明 PASS。Runtime Prototype 的五个组件、合成 fixture、RCPT manifest、独立 leaf attempt/grant 和 suite aggregate 已实现并执行；但当前执行环境无法提供合同要求的 OS 级隔离可观测性与独立 syscall/process-tree audit，因此关键验收未闭合。

## 机械枚举结果

测试数量来自冻结 manifest 的 `leaf_cases` 枚举和 runner 的实际发现/执行结果，不是手工声明。

| 指标 | 实际值 |
|---|---:|
| Requirement groups | 37 |
| Manifest leaves | 197 |
| Unique attempts | 197 |
| Unique authorization grants | 181 |
| Runner discovered | 197 |
| Runner executed | 197 |
| Evidence complete | 197 |
| PASS leaves | 99 |
| FAIL leaves | 98 |
| Skip | 0 |
| Unknown | 0 |
| 完全通过的 requirement groups | 21 |
| 存在失败的 requirement groups | 16 |

`manifest = discovered = executed = evidence-complete = 197`，因此枚举闭合；但 `pass != manifest`，suite acceptance 不闭合。

## 验收结论

| 必须证明的能力 | 结论 | 实际证据 |
|---|---|---|
| Book 1 可访问 | **未证明** | Broker 实际完成一次 `[4076,36515)` 的 32,439-byte `pread`，union 精确；但 T01 在 bounded reader 的 OS sandbox supervisor 处 fail-closed，未形成端到端 PASS。 |
| Book 2 不可访问 | **部分证明，整体未验收** | T32 的直接 Book 2 range 请求在读取前以 `BLOCKED_TEST_SCOPE_CONTRACT_MISMATCH` 拒绝、实际 read union 为空；consumer/parser/gateway 隔离因 sandbox proof 不可用而未证明。 |
| full raw 不可访问 | **未证明** | 正向 consumer FD/path inventory 无法由 supervisor 独立检查；T14/T15 没有完成所需 OS 级证明。 |
| Greek 不可访问 | **部分证明，整体未验收** | 1,043-byte host-only synthetic Greek deny object 有非真空 existence attestation；四个 Greek/production role broker leaf 全部精确拒绝，但 consumer-path 隔离未证明。 |
| authorization 必须存在 | **行为已证明；artifact schema 未闭合** | Missing/invalid/expired/replay、并发双 CAS 单赢家、CAS 后崩溃保持 spent 均按预期通过；T02 无授权时 broker calls、capabilities、deliveries 均为 0。但 authorization schema 与持久化 artifact 的 digest 外置语义不一致。 |
| read audit 完整 | **未证明** | 197/197 case evidence 完整、内部签名 event chain 及 scope/closure 文件均生成；外部 process-tree/syscall monitor 无法启动，因此不能把内部证据提升为完整独立 audit。 |

任一关键能力未证明即必须 BLOCKED；本 suite 因此不能通过 Phase 2-G 验收。

## Blockers

1. `BLOCKED_SANDBOX_ISOLATION_UNPROVEN`

   - 当前容器的 `Popen.pid` 与已挂载 `/proc/<pid>` 视图不一致，supervisor 无法可靠读取 child 的 `status`、`root` 和 FD inventory。
   - 96 个失败 leaf 以该精确能力 blocker 终止。

2. `TRACE_MONITOR_UNAVAILABLE_PTRACE_DENIED`

   - 独立 `strace -ff` 可用性探针返回 1，`PTRACE_TRACEME` 被环境以 `Operation not permitted` 拒绝。
   - 因覆盖未启动，English/Greek real-source stat/open/read/hash/parse/copy 及 source-tree scan 的独立计数均记录为 `unknown`，没有伪造为 0。

3. `UNEXPECTED_EXCEPTION`

   - 两个末端 signed-profile leaf 遇到 `/proc` PID 别名碰撞后的 FD inspection `PermissionError`；作为真实 FAIL 保留，没有改写成预期拒绝。

4. `AUTHORIZATION_SCHEMA_ARTIFACT_MISMATCH`

   - `contracts/authorization_schema.yaml` 错误地把 `authorization_file_sha256` 设为 authorization 文件本体的必填字段。
   - 181 个持久化 authorization artifact 均按运行时设计把文件摘要保存在文件外；若执行正式 schema validation，它们会因缺少该字段而失败。摘要不得写回自身，后续 suite 必须修正 schema，而不是把 self-digest 填入文件。

5. `COMPONENT_FREEZE_TRANSITIVE_CLOSURE_INCOMPLETE`

   - 12 个列入 component manifest 的 artifact 摘要全部匹配，但 snapshot 没有覆盖传递依赖 `common.py`，也没有覆盖 external audit 实现 `verify_trace.py`；`build_manifest.py` 和 package initializer 亦未进入闭合 component set。
   - 因此只能证明已列 12 项没有漂移，不能证明完整执行/审计代码闭包已冻结。

Aggregate blockers：

- `MANDATORY_LEAF_TEST_FAILURE`
- `BLOCKED_SANDBOX_ISOLATION_UNPROVEN`
- `ZERO_REAL_SOURCE_ACCESS_PROOF_FAILED`
- `TRACE_MONITOR_UNAVAILABLE_PTRACE_DENIED`

## 已实现的 Prototype 组件

- Authorization registry：SQLite immutable authorization bytes/digest 与 mutable state 分离；原子 CAS、唯一 registry event、capability/delivery 状态。
- Range broker：只接收 opaque capability；固定 byte range `pread`、真实 read calls/union、object identity 与 slice digest 校验、sealed memfd、signed envelope。
- Bounded reader：envelope/attestation/seal/digest 验证；native chroot/capability-drop/seccomp consumer probe；当前环境在 supervisor proof 阶段 fail-closed。
- Formal loader：signed positive allowlist、safe open、identity/digest 二次校验及 TOCTOU rejection。
- Read audit：七类 case evidence channel、hash-chained signed events、scope/closure JWS，以及独立 monitor probe。

Component manifest 中 12 个实现/runner/native artifact 的当前 SHA-256 均与冻结 snapshot 匹配。
该匹配不等于传递闭包完整；未纳入 snapshot 的依赖已作为 `COMPONENT_FREEZE_TRANSITIVE_CLOSURE_INCOMPLETE` 记录。

## Fixture 与证据审计

- Baseline synthetic full object：40,611 bytes；不含文学内容。
- Book 1 byte range：`[4076,36515)`，长度 32,439 bytes。
- Synthetic Greek deny object：1,043 bytes，存在性已证明，但不在 broker catalog，也未提供给 consumer mount。
- Fixture path 和 payload 均未持久化；suite tree 未发现 synthetic pad payload 或 private-key PEM。
- Evidence manifest 实际枚举 2,742 个 case artifact；197 个 case 均有 terminal result、七类 evidence、scope 与 closure attestation。
- 独立只读 artifact audit 验证 2,742 个条目的存在性、size 与 SHA-256 全部匹配；1,379 个 event log 的 JSON、Ed25519 signature、attempt/domain/sequence/hash chain 全部有效；394 个 audit JWS 的 signature 与 attempt binding 全部有效。

## 禁止项状态

Runner/controller 记录：

- Candidate Runs executed: `0`
- Model invocations: `0`
- Business outputs created: `0`
- `story_structure.yaml` created by prototype: `false`
- Production `P2ER-*` Gate PASS claims: `0`

由于独立 syscall monitor 不可用，本结果不把 real English/Greek source access 计数声明为 0；相关字段保持 `unknown`，这本身是 BLOCKED 的组成部分。

## Artifact digests

- Manifest SHA-256: `42799e6f56802248a467af0f06b539a817ec7ae224dd91e974ad3157f669a7bf`
- Final aggregate SHA-256: `705c852c0c7c9115954b04650a71e08304536991b0e5c8568bb9eaa331c78224`
- External audit SHA-256: `a696898014ccffd7ba775bdef7385cf74fe56488e8f21e51e6f33f10bc02721e`
- Evidence manifest SHA-256: `8ce98ff8d8a6a87d59cd338687bab0d9d74b6b201fdc984b2659524638a1ee45`
- Suite report SHA-256: `b5abdb0c9a986f8db77f1f16a716f5a8cfdd059b3b1e6d5bc6b8db401cbd9ea2`
- Component manifest SHA-256: `98f808df536c84f3f989fb2a61eda7e51e2b27e1d131568f799cf43459fba033`

本结果只描述 synthetic prototype。它不授权 Candidate Run，不是 production approval，也不改变 Phase 2-F 的 `PASS_PROTOTYPE_PLAN_ONLY` 边界。
