# Classic-to-Drama Engine：Runtime Capability Prototype Plan

> 项目：Classic-to-Drama Engine  
> 阶段：Phase 2-F  
> 文档类型：Runtime Capability Prototype 设计计划  
> 日期：2026-08-11  
> 文档状态：`ready_for_review`  
> 当前效力：`prototype_plan_only / not_implemented / not_tested / not_authorized`  
> 关联历史 Run：`AC-20260811-STORYSTRUCT-002`  
> 关联 Run 状态：`reserved / invalid_reserved / not_authorized / not_executed / non_reusable`  
> Candidate 正文读取授权：否  
> Formal Phase 2 授权：否

## 0. 目的、依据与本阶段边界

本文设计一个最小、可机械验收的 Runtime Capability Prototype，用无正文 synthetic fixture 验证以下执行能力：

1. authorization 只能被一次性原子消费；
2. range broker 只能交付授权中冻结的唯一字节范围；
3. bounded reader 不能获得完整 source object 的路径、handle、mount 或任意范围接口；
4. Greek 内容对象无法被授权、解析、挂载或交付；
5. formal loader 不会把 Candidate／prototype 工件识别为正式内容输入；
6. 独立 read audit 能把授权、capability、delivery、实际读取范围和拒绝证据关联到同一测试尝试。

本文只依据以下四份文件：

| 依据文件 | 本阶段读取时 SHA-256 | 用途 |
| --- | --- | --- |
| `CANDIDATE_EXECUTION_CONTRACT_REPAIR.md` | `12ceb01cab4901cb2b7472b1b56f93750a43cb8c28b5f0c9ab89acf3ad4fe7bd` | 修订后的四类工件、runtime component、两阶段 audit 与新 Run Gate |
| `ANALYSIS_CANDIDATE_WORKFLOW.md` | `dff075de96729332f324ce6a07332129d49d2cbece766a3b5411ca18664bbc50` | B-overlay、Candidate 隔离、不可晋级与新 Run 规则 |
| `TEXT_STRUCTURE_MAPPING_SPEC.md` | `259df6ceb6464ae7eadc84bc5603f3bdd16c603f5fe5c9ba9f82e3836cfcc3eb` | exact-range reader、source-object 隔离与 scope proof 语义 |
| `CANDIDATE_RUN_002_PLAN.md` | `75f86e219cd2c75b89e5dcd906973df9dddb0b7ec6baf65dadd6d6bb5ff74112` | Book 1 范围、10-Card scope 与 Run 002 历史阻断事实 |

### 0.1 本阶段唯一产物

本阶段只创建：

```text
RUNTIME_CAPABILITY_PROTOTYPE_PLAN.md
```

本文不会：

- 实现 authorization registry、range broker、bounded reader、formal loader 或 read audit；
- 执行任何 prototype test、Candidate Run 或 Formal Run；
- 分配新的 Candidate Run ID；
- 创建 `runtime_capability_prototype/`、`analysis_candidate/runs/` 或任何测试尝试目录；
- 打开、扫描、解析、hash 或复制 English TEI raw；
- 打开、探测、解析、复制或挂载 Greek raw；
- 读取 `book_structure_map.yaml` 或重新验证 Book 1；
- 调用模型；
- 创建 `story_structure.yaml`、`execution_report.md` 或其他 Run-local 工件；
- 创建人物、事件、主题、母题、改编、分集、场景、对白或剧本数据；
- 修改既有 Plan、Workflow、Spec、Map、Report、raw、Gate 或状态文件。

### 0.2 设计效力

本文是 prototype 实施与测试的计划，不是实现证据。即使本文获批，也不表示：

- B-overlay 已从 `design_only / not_implemented` 转为有效执行政策；
- runtime components 已存在、可调用或通过测试；
- production 签名 key、component digest 或 sandbox profile 已冻结；
- English source 已获得 Candidate 或 formal 资格；
- 任何一次性 Candidate authorization 已创建；
- Run 002 可以重启；
- 新 Candidate Run 可以立即规划或执行。

只有未来按本文实现并完成全部强制测试，才能得到 `PASS_RUNTIME_CAPABILITY_PROTOTYPE`。该 PASS 仍只是新 Candidate Run Planning 的前置工程证据，不是运行授权。

### 0.3 继承的目标范围与本阶段不复核事实

本文只把既有合同中的以下值作为未来 synthetic fixture 的形状参数，不读取真实 source 或 Map：

```yaml
reference_source_id: "ODY-ENG-MURRAY1919"
reference_scope_label: "Book 1"
reference_allowed_range:
  start_byte: 4076
  end_byte_exclusive: 36515
reference_expected_length: 32439
reference_card_count: 10
reference_selected_books: [1]
```

真实 source object ID、真实 full-source checksum、真实 Book 1 slice checksum 和真实 TEI character data不得进入 prototype fixture、token、日志或报告。Prototype 只复用 range 坐标和长度语义，以证明 runtime capability 的边界行为。

## 1. Prototype 信任模型与验证目标

### 1.1 测试命名空间

Prototype 必须使用与 Candidate Run 完全不同的测试身份：

```yaml
prototype_attempt_id_format: "RCPT-YYYYMMDD-NNN"
candidate_run_id_format_used: false
candidate_run_authorized: false
formal_phase_2_input: false
prototype_fixture_authority: "synthetic_test_only"
production_source_binding_allowed: false
```

`RCPT-*` 只表示一次 runtime capability test attempt：

- 不是 `AC-*`；
- 不能被改名为 Candidate Run；
- 不能成为 authorization artifact 的 `run_id`；
- 不能写入 `analysis_candidate/runs/`；
- 不能引用真实 source object；
- 不能产生业务内容输出；
- 失败后可创建新的 `RCPT-*` 测试尝试，但不能复用失败测试的 token、delivery 或 registry consumption event。

### 1.2 最小可信边界

Prototype 使用五个外部可审计组件：

| 组件 | 唯一权限 | 明确禁止 |
| --- | --- | --- |
| authorization registry | 保存 test authorization 的不可变 identity，并原子记录一次性消费 | 读取 source bytes、修改授权文件、创建 Candidate authorization |
| range broker | 唯一可绑定并打开 synthetic full fixture object 的组件 | 接受调用者自报 path／offset／length，交付 full object |
| bounded reader | 消费一次性 signed envelope 与内存 slice | 打开 source、调用 broker 重读、请求任意 range |
| formal loader | 按 signed formal-manifest provenance 正向加载正式测试工件 | 发现或消费 Candidate／prototype 工件 |
| read audit | 汇总独立观测并生成 test-only scope／closure attestations | 接收 probe 自报作为唯一证据、保存 fixture payload |

Capability issuer 作为 authorization control plane 内的最小子组件存在，不另形成第六个外部数据访问主体。它只能在 registry 已生成成功的原子消费事件后签发 test-only capability；它本身没有 source 访问权。

未来验证必须运行真实的 prototype component implementations，不能用 mock broker、mock registry 或预填的 audit JSON 冒充实现通过。只允许两类受控 test double：synthetic source fixture 和不会调用模型的 discard-only model gateway sink。Production verifier 必须拒绝 prototype trust root；prototype broker／issuer 必须拒绝 production source identity 与 production trust root，形成双向隔离。

### 1.3 要证明的三个核心不变量

#### 不变量 A：只允许 Book 1 range

成功测试必须证明：

```yaml
authorized_range:
  start_byte: 4076
  end_byte_exclusive: 36515
authorized_length: 32439
broker_actual_union:
  - start_byte: 4076
    end_byte_exclusive: 36515
bytes_outside_authorized_range: 0
bounded_reader_received_bytes: 32439
range_override_interface_exposed: false
automatic_retry_count: 0
```

少一字节、多一字节、起点变化、终点变化、第二范围、读取到 EOF、重复 delivery 或 token replay 必须全部拒绝。

#### 不变量 B：consumer 不可访问 full raw

这里的 `consumer` 包括 bounded reader、synthetic parser probe、model-input test sink 和任何未来 Candidate 内容进程。成功测试必须证明它们：

- 没有 synthetic full fixture path；
- 没有 full fixture file descriptor 或可复用 object handle；
- 没有 project `source/` mount；
- 没有通用 source object catalog；
- 没有网络取源能力；
- 不能调用 broker 请求第二个 range；
- 只能收到一个 sealed／immutable Book 1 slice；
- 对 host-only fixture path 的负向 open 尝试为拒绝；
- `/proc`／handle inventory 中不存在指向 full fixture 的 consumer-visible handle；
- 成功读取 full fixture 的计数为 0。

Broker 对 synthetic fixture 的 exact-range open 不计为 consumer direct access；它必须由 broker audit 单独记录。Prototype 不对物理存储设备 read-ahead 作保证，其 proof level 固定为：

```yaml
scope_proof_level: "candidate_visible_bytes_and_application_exact_range"
physical_device_read_ahead_proof_claimed: false
```

#### 不变量 C：Greek 永远不可访问

Prototype 不使用、复制或探测真实 Greek raw。它通过一个无文学内容、由 fixture controller 确认实际存在、但对 broker／consumer 不可达的 host-only `FIXTURE-GREEK-DENY` synthetic object 和对应 host-only path string 验证 deny chain：

1. test authorization schema 不允许 Greek role；
2. capability issuer 的 source allowlist 只有 synthetic English fixture object；
3. broker catalog 不解析 `FIXTURE-GREEK-DENY`；
4. consumer sandbox 不挂载 host fixture store 或项目 `source/`；
5. bounded reader API 不接受 source ID／path；
6. model-input gateway test sink拒绝任何非 Book 1 fixture scope；
7. audit 记录 Greek-like 请求的拒绝尝试，但成功 open／read／parse／copy／gateway delivery 均为 0。

负向测试中的虚拟 Greek-like identifier 不得解析到真实文件，测试不得对真实 Greek 路径调用 `stat`、`open`、glob 或目录扫描。

### 1.4 Signed-object integrity profiles

Prototype 必须使用修订合同定义的三类 JWS profile 语义，只替换为 test-only trust root、test component IDs 和 synthetic claims。Baseline algorithm 固定为 JWS `EdDSA`／Ed25519 test keys，protected profile version 固定为 `1`：

| Profile | Test 对象 | Protected `typ` | 冻结 audience |
| --- | --- | --- | --- |
| `CTDE-CAPABILITY-JWS-1` | opaque test range capability | `ctde-range-capability+jws` | prototype range broker component ID |
| `CTDE-BROKER-ENVELOPE-JWS-1` | broker test response envelope | `ctde-broker-envelope+jws` | prototype bounded reader component ID |
| `CTDE-AUDIT-ATTESTATION-JWS-1` | prototype scope／closure attestation | `ctde-audit-attestation+jws` | scope subtype：prototype scope verifier + audit controller；closure subtype：prototype audit controller |

每个 profile 必须使用标准 compact JWS 或等价 detached JWS，并满足：

- protected header 固定 `alg`、`typ`、`kid`、`ctde_profile_version`；
- Prototype execution snapshot 固定 `alg=EdDSA`、suite-specific test key IDs、issuer IDs、verifier IDs、key status 和 verifier clock policy；
- `alg=none`、未冻结算法、header／payload algorithm confusion、未知／撤销／过期 key 均拒绝；
- payload 为 UTF-8 JSON，并包含唯一 object／token ID、`iss`、`aud`、`iat`、`nbf`、`exp`、`environment=prototype_fixture_only`、attempt ID 与 authorization file digest；
- capability 还必须绑定 consumption event、fixture object、synthetic structure contract、唯一 range、length、slice hash、nonce 与 anti-replay state；
- envelope 还必须绑定 capability、consumption event、delivery、range、length、slice hash 与 broker-read attestation digest；
- audit attestation 必须绑定 subtype、所需 component attestations、前序 attestation digest与该 subtype 的冻结 audience；
- capability、envelope 与 attestation 的 TTL／clock skew policy 必须在 execution snapshot 中冻结，过期、尚未生效或时间字段缺失均拒绝；
- signature 或对象自身 digest 不得写入 payload；完整 signed-object bytes 的 SHA-256 由接收者或下一层计算；
- test trust root 不被 production verifier 信任，production key／issuer 不被 prototype verifier 信任。

Baseline time policy 为：capability 与 envelope TTL 各不超过 60 秒，attestation TTL 不超过 300 秒，deterministic test clock 的允许偏差为 0；任何不同值都必须在新 suite snapshot 中重新冻结，并触发新的 suite ID。

未来如改用非 JWS 容器，必须另立 prototype profile ID，并独立证明 protected header、algorithm／key、audience、expiry、canonical signed bytes 与 anti-replay 语义等价；不能继续使用以上 profile 名称。

## 2. Runtime 组件设计

### 2.1 Authorization registry

#### 责任

Authorization registry 是 test authorization 消费状态的唯一事实来源。Prototype 最小实现可以使用单进程事务数据库或语义等价的原子存储，但必须把不可变 authorization bytes 与可变 consumption state 分离。

Registry 本体及其 state 位于 Candidate／prototype attempt artifact root 之外；`suites/<suite>/cases/<case>/<attempt>/evidence/registry_events.jsonl` 只是不可变审计投影，不是可恢复或改写 registry state 的控制入口。

#### Test authorization 合同

未来 prototype authorization 只能使用 synthetic 身份：

```yaml
artifact_class: "runtime_capability_test_authorization"
environment: "prototype_fixture_only"
attempt_id: "RCPT-YYYYMMDD-NNN"
prototype_fixture_authorized: true
candidate_run_authorized: false
formal_phase_2_input: false
one_time: true
automatic_retry_allowed: false
authorization_inheritable: false
fixture_object_id: "urn:ctde:fixture:<digest>"
fixture_structure_contract_id: "urn:ctde:fixture-structure:<digest>"
fixture_structure_contract_sha256: "<synthetic structure-only manifest sha256>"
allowed_range:
  start_byte: 4076
  end_byte_exclusive: 36515
expected_length: 32439
expected_slice_sha256: "<synthetic fixture slice sha256>"
forbidden_source_roles:
  - "greek"
  - "production_raw"
```

禁止把真实 `source_object_id`、真实 source checksum、真实 slice checksum、`AC-*` ID 或 production key 写入该 artifact。

#### 状态机

| Registry state | 允许动作 | 禁止动作 |
| --- | --- | --- |
| `unconsumed` | 在 digest、expiry、attempt 与 fixture binding 全匹配时执行一次 CAS | 直接 mint capability 而不消费 |
| `spent` | 只读查询和审计 | 第二次消费、回退为 unconsumed、再次 mint |
| `revoked` | 只读查询和拒绝 | 消费或 mint |
| `expired` | 只读查询和拒绝 | 消费或 mint |
| `unknown / unavailable` | fail closed | 推断为 unconsumed |

原子操作必须为：

```text
compare authorization_digest + state=unconsumed
set state=spent
emit unique consumption_event_id
commit once
```

capability issuer 只能消费已提交的 `consumption_event_id`。CAS 失败、数据库不可用、digest 不匹配、authorization 过期或 event replay 时，capability 数必须为 0，broker read 数必须为 0。

Registry 还必须证明两个故障边界：并发双消费恰好一个成功；CAS 已提交但 issuer 在 mint 前崩溃时，authorization 仍为 `spent`，不得 reset、补发或在同一 test grant 上重试。

#### Prototype 签名边界

- 使用 test-only signing key 和固定 test `kid`；
- issuer／audience 使用 `ctde-prototype-*` component IDs；
- token 必须含 `environment=prototype_fixture_only`；
- token 必须绑定 attempt ID、authorization digest、consumption event、fixture object、synthetic structure-contract identity、唯一 range、length、slice hash、expiry、nonce 和 one-shot state；
- test key 不得被 production verifier 信任；
- token payload 不含 raw path；
- token 完整 bytes 的 digest 由接收者计算，不能写回 token 形成自摘要。

### 2.2 Range broker

#### 责任

Range broker 是唯一可访问 synthetic full fixture object 的进程。它接收一个 opaque signed capability，不接受调用者另行提供的 source ID、path、offset、length、expected hash 或 fallback 选项。

#### 请求接口

```yaml
request:
  opaque_capability: "<test-only signed token>"
```

以下请求字段在接口层必须不存在：

```yaml
forbidden_request_fields:
  - raw_path
  - source_path
  - source_id_override
  - start_byte
  - end_byte_exclusive
  - length
  - read_to_eof
  - next_range
  - retry
```

#### 行为

Broker 必须：

1. 验证 token signature、issuer、audience、environment、expiry、nonce 和 anti-replay；
2. 验证 consumption event 已由 registry 成功提交并绑定同一 authorization digest；
3. 从 capability claims 解析唯一 fixture object 与 `[4076,36515)`；
4. 将 claims 与 registry 中不可变 authorization、synthetic structure contract 逐项复核，再在 broker-only object catalog 中解析 content-addressed／sealed fixture object；
5. 使用 fixed-offset／fixed-length API 获取 32439 bytes；
6. 记录每次底层 read call 与 actual union；
7. 验证返回长度和 synthetic slice SHA-256；
8. 只返回 immutable／sealed slice、test-only signed envelope 与 broker-read attestation reference；
9. 原子消费 capability ID 和 delivery ID；
10. 关闭 object handle，不把 path 或 handle暴露给 reader。

Broker 不得：

- 对 synthetic full fixture 做 full-file hash 作为运行时 fallback；
- 读取 byte 0 到 EOF 后截取 Book 1；
- 在 slice hash 失败后扩大范围；
- 解析真实 project source path；
- 解析 Greek-like source object；
- 自动重试；
- 把 payload 写入 envelope、日志、报告或 test artifact。

#### 响应接口

```yaml
response_envelope:
  environment: "prototype_fixture_only"
  attempt_id: "RCPT-YYYYMMDD-NNN"
  authorization_file_sha256: "<digest>"
  consumption_event_id: "<id>"
  capability_id: "<id>"
  delivery_id: "<id>"
  broker_component_id: "<id, version, digest>"
  audience: "<bounded reader prototype component id>"
  fixture_structure_contract_sha256: "<synthetic structure-only manifest sha256>"
  start_byte: 4076
  end_byte_exclusive: 36515
  returned_bytes: 32439
  slice_sha256: "<synthetic slice sha256>"
  broker_read_attestation_id: "<id>"
  broker_read_attestation_sha256: "<digest>"
  payload_transport: "sealed_memory_only"
```

### 2.3 Bounded reader

#### 责任

Bounded reader 是 consumer 侧唯一字节入口。它不能打开 fixture、workspace 或 source tree，只能消费 broker 一次性交付的 signed envelope 与 sealed Book 1 slice。

#### 接口不变量

- API 只接受 `signed_envelope + sealed_slice_handle`；
- slice handle 只指向 32439-byte payload，不指向 full fixture；
- API 不接受 path、glob、source ID、offset、length、XPath、EOF 或第二次读取参数；
- reader 没有 broker credential 或 capability mint 权限；
- reader 验证 envelope signature、audience、authorization digest、event、capability、delivery、range、length、hash 与 broker attestation；
- delivery ID 只可消费一次；
- wrong／expired／tampered envelope 在解析 payload 前拒绝；
- slice 长度或 hash 不匹配时拒绝，不请求 broker 重发；
- parser probe 只处理 synthetic structure markers，不处理文学正文；
- model-input gateway 使用 discard-only test sink，模型调用数固定为 0；
- reader、probe 和 gateway 均不得持久化 slice bytes。
- reader 启动时必须关闭所有未登记继承 file descriptors，并由独立 supervisor 检查 process tree 与 `/proc/<pid>/fd` 中不存在 full fixture handle；
- synthetic fragment parser 必须禁用 DTD、internal／external entity、网络和 recovery mode，且只允许唯一 Book 1、10 Card 与 10 Paragraph structural markers；
- in-memory wrapper 不得进入 gateway、日志、evidence 或持久文件。

#### Consumer sandbox

Prototype 必须采用真实 OS 级隔离后端，而不是只改变工作目录或依赖代码约定。实现可以选择经过记录的 container、mount namespace、Landlock／seccomp 组合或语义等价机制，但 PASS 条件固定为：

```yaml
project_workspace_mounted: false
project_source_tree_visible: false
broker_fixture_store_mounted: false
greek_fixture_or_raw_mounted: false
network_source_fetch_allowed: false
consumer_visible_full_object_handles: 0
consumer_writable_project_paths: 0
consumer_received_only_sealed_slice: true
```

如果运行环境只能证明“代码没有主动调用 open”，但不能证明 consumer 缺少路径／handle 能力，结果必须为 `BLOCKED_SANDBOX_ISOLATION_UNPROVEN`。

### 2.4 Formal loader

#### 责任

Prototype formal loader 只验证发现与 provenance policy，不加载文学内容。它使用签名 formal-manifest 正向 allowlist，并把 Candidate／prototype path deny 作为补充防线。

#### 最小 policy

只有同时满足以下条件的 test fixture entry 才可被当作 formal test input：

- 独立 formal-test run ID；
- signed formal-test manifest；
- manifest entry 的 artifact identity、digest 和 provenance 完整；
- 路径不在 `analysis_candidate/**` 或 `runtime_capability_prototype/**`；
- artifact class 不是 Candidate／prototype；
- signature、issuer、audience 与 allowlist component identity 匹配。

Loader 在安全打开对象后必须再次核对 object identity／digest 与 manifest binding，防止 path check 后的 TOCTOU object swap。正向对照必须有且只有一个具完整 signed formal-test provenance 的无内容 fixture 可以被加载；否则“loader 永远返回空集”不能算 PASS。

必须拒绝以下 virtual entries 或无内容 probe artifacts：

- Candidate 根中的裸文件名；
- Candidate 根中的带 `candidate__` 前缀文件；
- prototype attempt tree 中的任何文件；
- symlink／hardlink／相对路径逃逸；
- 被复制、移动或重命名到根外但缺少 formal provenance 的副本；
- 删除 Candidate／prototype 标记后的副本；
- 伪造 manifest reference；
- 只有内容 digest 相同、但没有正式批准 identity 的对象。

当前 Phase 2-F 不创建任何上述文件。未来实现应使用 `candidate_probe.yaml` 或内存 virtual manifest entry，不得生成 `story_structure.yaml` 作为测试夹具。

### 2.5 Read audit

#### 责任

Read audit 由 consumer 无写权限的独立 aggregator 生成。Prototype 必须覆盖五个观测域：

| 观测域 | 记录内容 | 证据 authority |
| --- | --- | --- |
| broker read | fixture object、capability、底层 calls、actual union、length、hash、关闭 | broker monitor |
| sandbox／syscall | consumer direct-open attempts、成功 full-object handles、Greek-like attempts、mount／network、继承 FD 与子进程状态 | sandbox supervisor／syscall monitor |
| parser scope | 可见 Book marker、Card marker、范围外 marker 数 | parser-scope test adapter |
| model gateway | 进入 discard-only sink 的 scope、Greek／range-outside event 数、真实模型调用数 | gateway test adapter |
| write monitor | fixture、workspace、formal path、unallowlisted test path 的写入计数 | independent write monitor |

Probe process 的 stdout、自报 JSON 或应用日志不能单独构成 PASS 证据。

Sandbox／syscall 观测必须在 broker source open 前启动并覆盖完整 consumer process tree。除 `open/openat/read/pread` 外，还必须阻断或观测 `mmap`、`sendfile`、`splice`、`copy_file_range`、`io_uring` 及语义等价的数据逃逸通道。`actual_union_of_read_ranges` 必须按真实 returned bytes 计算，不能从 requested range 复制。丢事件、monitor late-start、子进程未纳入或字段 unknown 必须 fail closed，不能补零。

#### 两阶段 test attestation

Prototype 复用 production 合同的两阶段语义，但必须使用 test-only identity：

1. `prototype_scope_execution_attestation`：在任何 test result 被标记 PASS 前生成，绑定 broker、sandbox、parser 与 model-gateway evidence；
2. `prototype_closure_audit_attestation`：绑定 scope attestation、write monitor、formal-loader 结果、test artifact presence 和最终 prototype status。

Prototype 不发布业务输出，因此 closure 必须如实记录 `business_output_status: absent`、`business_output_sha256: null` 与 closed absent reason；不得创建空业务文件或虚构 checksum。

两种 attestation 必须包含：

```yaml
environment: "prototype_fixture_only"
attempt_id: "RCPT-YYYYMMDD-NNN"
candidate_run_id: null
candidate_run_authorized: false
fixture_object_id: "urn:ctde:fixture:<digest>"
authorization_file_sha256: "<test artifact digest>"
consumption_event_id: "<id or null>"
capability_id: "<id or not_issued>"
delivery_id: "<id or not_issued>"
actual_read_calls: []
actual_union_of_read_ranges: []
bytes_outside_allowed_ranges: "<integer or null before broker observation>"
consumer_direct_full_object_open_success_count: "<integer>"
consumer_direct_full_object_access_attempt_count: "<integer>"
greek_like_access_attempt_count: "<integer>"
greek_like_access_denied_count: "<integer>"
greek_like_open_success_count: "<integer>"
greek_like_read_success_count: "<integer>"
greek_like_successful_read_bytes: "<integer>"
model_invocations: 0
raw_or_fixture_payload_persisted: false
```

完整 signed-object digest 由接收者／下一层计算，不写入对象自身。Test attestation 不能作为 production scope attestation、Candidate execution report 或 Run authorization 使用。

`PROTOTYPE_TEST_REPORT.md` 完成后的文件 checksum 由 Run 外的 prototype test registry 记录，不写回报告形成 self-hash。

### 2.6 组件组合顺序

未来最小 prototype test attempt 必须按以下顺序执行：

1. 创建仅含 synthetic identity 的 immutable test authorization；
2. 冻结 component manifest、fixture recipe、test policy 与 test-only key IDs；
3. 启动 independent audit adapters 和 consumer sandbox supervisor；
4. registry 原子执行 `unconsumed -> spent`；
5. capability issuer 只基于已提交 consumption event mint test token；
6. broker 验证 token 后 exact-range 读取 synthetic fixture；
7. broker 验证长度／hash，生成 broker attestation 与 signed envelope；
8. bounded reader 验证 envelope，消费一次性 sealed slice；
9. parser probe 只验证 synthetic Book 1／Card markers；
10. discard-only model gateway 记录 scope，模型调用保持 0；
11. aggregator 生成 prototype scope attestation；
12. formal loader 执行 Candidate／prototype exclusion 测试；
13. write monitor 关闭观测，aggregator 生成 prototype closure attestation；
14. test controller 写入 prototype report 并 seal attempt。

任一步失败必须停止后续 delivery 主路径；已消费 authorization 仍保持 spent。允许独立 closure 分支记录真实到达状态，但不得自动重试或复用 capability／delivery。

## 3. 最小验证流程

### 3.1 Synthetic fixture 设计

Future prototype 只能由确定性 fixture generator 在临时 broker-only 根中创建无文学内容的 binary／XML-like fixture。计划形状如下：

| Zone | Range | 内容类型 | 目的 |
| --- | --- | --- | --- |
| prefix deny zone | `[0,4076)` | deterministic non-prose marker bytes | 证明 Book 1 前字节不可见 |
| Book 1 allowed zone | `[4076,36515)` | synthetic Book 1／10-Card／10-Paragraph structural markers 与 padding | 唯一可交付范围 |
| suffix deny zone | `[36515,N)` | deterministic Book 2/out-of-scope marker bytes | 证明 Book 1 后字节不可见 |
| Greek deny object | 独立、实际存在的 host-only synthetic object | deterministic `FIXTURE-GREEK-DENY` bytes | 验证非空对象仍不可达；不映射真实 Greek |

要求：

- fixture 不包含《奥德赛》原文、译文、摘要或人物／事件／主题信息；
- allowed zone 的总长度精确为 32439 bytes；
- 10 个 Card 与 10 个 Paragraph 只用 `CARD_01`、`PARA_01` 等无语义标记；
- fixture 包含确定性的安全 UTF-8 多字节标记，range 起止不以字符数、行边界或序列化长度推导，用于检出 byte offset／character offset 混淆；
- prefix、allowed、suffix 与 Greek deny object 使用互不相同的 sentinel；
- fixture recipe 固定 generator ID／version／seed；
- full fixture 与 slice digest 在生成后由 fixture controller 计算；
- fixture full bytes 和 slice bytes 只存在于临时 broker-only 根／内存，不进入持久测试工件；
- test attempt 结束后删除 ephemeral fixture 不影响 audit，因为 recipe、size、digests 与 events 已持久化；
- fixture generator 不接受 project raw path；
- fixture controller 在隔离外证明 synthetic Greek deny object 确实存在，但不得把其 path／handle／catalog entry 交给 broker 或 consumer；
- 任何真实 source object ID 或真实 slice hash出现都使测试无效。

### 3.2 正向最小流程

正向测试 `RCPT-T01-EXACT-RANGE` 必须证明：

1. test authorization 只绑定 synthetic fixture 与 `[4076,36515)`；
2. registry 仅成功消费一次；
3. capability 只在成功 consumption event 后签发；
4. broker actual union 恰好等于授权 range；
5. broker 返回 32439 bytes，synthetic slice hash 匹配；
6. consumer 只获得 sealed slice；
7. parser probe 只观察 `BOOK_01`、精确 10 个 Card marker 与 10 个 Paragraph marker；
8. prefix／suffix／Book 2 sentinel 可见次数均为 0；
9. Greek-like object 的成功访问次数为 0；
10. model 调用次数为 0；
11. fixture／workspace／formal path 写入次数为 0；
12. formal loader 对 prototype attempt artifacts 的 content input 数为 0；
13. scope 与 closure attestations 关联同一 attempt、authorization、event、capability 和 delivery。

### 3.3 强制拒绝测试矩阵

| Test ID | 场景 | 期望结果 | broker read | delivery |
| --- | --- | --- | --- | --- |
| `RCPT-T02-AUTH-MISSING` | 无 authorization | `BLOCKED_TEST_AUTHORIZATION_MISSING` | 0 | 0 |
| `RCPT-T03-AUTH-DIGEST` | authorization digest 不匹配 | `BLOCKED_TEST_AUTHORIZATION_INVALID` | 0 | 0 |
| `RCPT-T04-AUTH-EXPIRED` | authorization 过期 | `BLOCKED_TEST_AUTHORIZATION_EXPIRED` | 0 | 0 |
| `RCPT-T05-AUTH-REPLAY` | 第二次 CAS／消费 | `BLOCKED_TEST_AUTHORIZATION_SPENT` | 0 | 0 |
| `RCPT-T06-CAP-TAMPER` | token claims／signature 被修改 | `BLOCKED_RANGE_CAPABILITY_INVALID` | 0 | 0 |
| `RCPT-T07-CAP-AUDIENCE` | 错误 broker audience | `BLOCKED_RANGE_CAPABILITY_INVALID` | 0 | 0 |
| `RCPT-T08-RANGE-OVERRIDE` | caller 试图附加 offset／length | `BLOCKED_RANGE_OVERRIDE_FORBIDDEN` | 0 | 0 |
| `RCPT-T09-RANGE-SHORT` | capability 绑定少一字节 | `BLOCKED_TEST_SCOPE_CONTRACT_MISMATCH` | 0 | 0 |
| `RCPT-T10-RANGE-LONG` | capability 绑定多一字节 | `BLOCKED_TEST_SCOPE_CONTRACT_MISMATCH` | 0 | 0 |
| `RCPT-T11-SLICE-HASH` | fixture slice hash 与授权不符 | `BLOCKED_SLICE_HASH_MISMATCH` | 允许仅在授权 range 内 | 0 |
| `RCPT-T12-DELIVERY-REPLAY` | 重复消费 delivery ID | `BLOCKED_BOUNDED_READER_REPLAY` | 不增加 | 0 for replay |
| `RCPT-T13-ENVELOPE-TAMPER` | envelope／broker attestation 被修改 | `BLOCKED_BROKER_ENVELOPE_INVALID` | 不增加 | 0 |
| `RCPT-T14-FULL-PATH` | consumer 尝试打开 host-only full fixture path | `BLOCKED_SANDBOX_DIRECT_SOURCE_ACCESS` | broker 不增加 | 0 |
| `RCPT-T15-HANDLE-INVENTORY` | consumer 可见 full fixture handle | `BLOCKED_SANDBOX_ISOLATION_UNPROVEN` | test invalid | 0 |
| `RCPT-T16-GREEK-ID` | capability 请求 Greek-like object | `BLOCKED_FORBIDDEN_SOURCE_ROLE` | 0 | 0 |
| `RCPT-T17-GREEK-PATH` | fixture controller 先证明 synthetic Greek deny object 实际存在；consumer 再尝试同一 host-only synthetic path string | sandbox 内 resolve/open/read 均拒绝；success count 0 | broker 不增加 | 0 |
| `RCPT-T18-BOOK2-MARKER` | parser／gateway 观察到 Book 2 sentinel | `INVALIDATED_PROTOTYPE_SCOPE_EXCEEDED` | 记录实际 | 0 business path |
| `RCPT-T19-WRITE-ESCAPE` | probe 尝试写 workspace／formal path | OS deny；`BLOCKED_TEST_WRITE_ISOLATION` | 不增加 | 0 business path |
| `RCPT-T20-FORMAL-DISCOVERY` | loader 接收 Candidate／prototype virtual entry | 0 formal content inputs | 不适用 | 不适用 |
| `RCPT-T21-RENAMED-COPY` | 去标记／改名但无 formal provenance | 0 formal content inputs | 不适用 | 不适用 |
| `RCPT-T22-AUDIT-MISSING` | required observer 缺失或不可关联 | `BLOCKED_SCOPE_PROOF_UNAVAILABLE` | 按真实值 | 不得标 PASS |
| `RCPT-T23-AUTH-CONCURRENT` | 两个消费者并发 CAS 同一 grant | 恰好一个 spent event；另一个拒绝 | 0 before winner token | 0 before winner token |
| `RCPT-T24-CAS-CRASH` | CAS commit 后、mint 前 issuer 崩溃 | grant 保持 spent；capability 0；不得补发 | 0 | 0 |
| `RCPT-T25-AUDIT-TAMPER` | event／attestation 篡改、重排或旧证据 replay | `INVALIDATED_AUDIT_TAMPERED` | 按真实值 | 不得标 PASS |
| `RCPT-T26-FORMAL-POSITIVE` | 唯一具完整 signed formal-test provenance 的对照 | 恰好 1 formal content input | 不适用 | 不适用 |
| `RCPT-T27-FORMAL-TOCTOU` | path check 后 object swap／digest 变化 | 0 formal content inputs | 不适用 | 不适用 |
| `RCPT-T28-PARSER-UNSAFE` | DTD／entity／recovery／Book 2／额外 Card fixture | `BLOCKED_BOUNDED_FRAGMENT_UNPARSABLE` 或 scope blocker | 不增加 | 0 |
| `RCPT-T29-BROKER-OBJECT-SWAP` | capability 后 fixture object identity／digest 被替换 | `BLOCKED_SOURCE_OBJECT_NOT_IMMUTABLE` | 0 或仅已审计失败 call | 0 |
| `RCPT-T30-SECOND-CHANNEL` | consumer 尝试 `mmap/sendfile/splice/copy_file_range/io_uring` 或子进程逃逸 | OS deny；成功来源字节为 0 | broker 不增加 | 0 |
| `RCPT-T31-BROKER-FALLBACK` | broker process tree 尝试 full-hash／EOF／`mmap/sendfile/splice/copy_file_range/io_uring` fallback | fail closed；仅批准的 fixed-range calls 可存在 | 不得形成额外 union | 0 |
| `RCPT-T32-RANGE-ONLY-MISMATCH` | signature、event、audience 等均有效，仅 range claim 与 scope contract 不同 | `BLOCKED_TEST_SCOPE_CONTRACT_MISMATCH` | 0 | 0 |
| `RCPT-T33-PROFILE-ALG` | `alg=none`、未冻结算法或 algorithm confusion | `BLOCKED_SIGNED_OBJECT_PROFILE_INVALID` | 0 | 0 |
| `RCPT-T34-PROFILE-TYP` | protected `typ`／profile version 错误或缺失 | `BLOCKED_SIGNED_OBJECT_PROFILE_INVALID` | 0 | 0 |
| `RCPT-T35-PROFILE-KID` | unknown／revoked／expired key 或错误 issuer | `BLOCKED_SIGNED_OBJECT_PROFILE_INVALID` | 0 | 0 |
| `RCPT-T36-PROFILE-AUD` | capability／envelope／attestation audience 或 subtype audience 错误 | `BLOCKED_SIGNED_OBJECT_PROFILE_INVALID` | 0 | 0 |
| `RCPT-T37-PROFILE-TIME` | `iat/nbf/exp` 缺失、尚未生效或过期 | `BLOCKED_SIGNED_OBJECT_PROFILE_INVALID` | 0 | 0 |

所有强制测试都必须运行；不能用一个正向测试替代拒绝矩阵。测试 framework 的 skipped、xfail、unknown、timeout 或未采集 evidence 均不计为 PASS。

上表 Test ID 是 requirement group。Future suite manifest 必须把每一个复合攻击向量展开为独立 leaf case，例如 `T28-DTD`、`T28-EXTERNAL-ENTITY`、`T33-ALG-NONE`、`T33-ALG-CONFUSION`。每个 leaf case 使用独立 `RCPT-*` attempt；authorization-related leaf 各有独立 synthetic grant。Expected rejection 只有在返回精确 blocker、证据完整且 forbidden side effects 全为 0 时，才记为该 leaf 的测试 PASS。

### 3.4 零真实来源证明

Prototype report 必须机械记录：

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
```

这些值不能只由 test code 自报。测试控制器必须从允许输入 manifest、sandbox mount manifest、broker object catalog、syscall／access monitor 与 fixture identity 共同证明。若 project source tree 或真实对象是否可见为 unknown，prototype 不得 PASS。

## 4. Runtime Test Artifact Layout

### 4.1 未来实施根

未来实现与测试只能使用独立根；本阶段不创建它：

```text
runtime_capability_prototype/
├── contracts/
│   ├── component_manifest.yaml
│   ├── test_policy.yaml
│   ├── authorization_schema.yaml
│   ├── capability_claims_schema.yaml
│   ├── broker_envelope_schema.yaml
│   └── audit_attestation_schema.yaml
├── fixture_specs/
│   └── synthetic_book1_fixture.yaml
└── suites/
    └── <RCPTS-suite-id>/
        ├── control/
        │   ├── runtime_capability_test_manifest.yaml
        │   ├── suite_component_snapshot.yaml
        │   └── suite_test_policy_snapshot.yaml
        ├── fixture_attestations/
        │   ├── synthetic_book1_fixture_identity.yaml
        │   └── synthetic_greek_fixture_existence_attestation.yaml
        ├── cases/
        │   └── <leaf-case-id>/
        │       └── <RCPT-attempt-id>/
        │           ├── control/
        │           │   ├── prototype_authorization.yaml
        │           │   └── prototype_execution_snapshot.yaml
        │           ├── evidence/
        │           │   ├── registry_events.jsonl
        │           │   ├── broker_events.jsonl
        │           │   ├── broker_environment_snapshot.yaml
        │           │   ├── consumer_environment_snapshot.yaml
        │           │   ├── sandbox_events.jsonl
        │           │   ├── parser_scope_events.jsonl
        │           │   ├── model_gateway_events.jsonl
        │           │   ├── write_events.jsonl
        │           │   └── formal_loader_events.jsonl
        │           ├── attestations/
        │           │   ├── prototype_scope_execution_attestation.jws
        │           │   └── prototype_closure_audit_attestation.jws
        │           └── case_result.yaml
        ├── aggregate/
        │   ├── test_results.json
        │   └── evidence_manifest.yaml
        └── report/
            └── PROTOTYPE_TEST_REPORT.md
```

`RCPTS-YYYYMMDD-NNN` 是 suite identity，不是 Candidate Run。每个 manifest leaf case 必须分配唯一 `RCPT-*` attempt；每个 authorization-related case 必须使用独立 synthetic grant。Spent grant、capability、delivery、nonce、attestation 或 test key usage state不得跨 case 复用。Missing-authorization 与不需要 authorization 的 formal-loader cases 可以合法缺少 `prototype_authorization.yaml`，但 `case_result.yaml` 必须明确记录 absence reason。

Expected rejection case 的 component operation 可以按设计被拒绝，但只有在精确 blocker、真实 evidence、零 forbidden side effects 与 case closure 全部匹配时，其 `case_test_result` 才可为 `pass`。Suite-level report 必须依据 frozen suite manifest 和所有 leaf `case_result.yaml` 聚合，不能把 component rejection 误写成 suite failure，也不能把意外失败误写成 expected rejection。

### 4.2 Ephemeral、不得持久化的对象

以下对象只允许存在于测试进程隔离临时根或内存，不得出现在上述持久 layout：

- synthetic full fixture bytes；
- synthetic Book 1 slice bytes；
- sealed memory handle 的可重放副本；
- token signing private keys；
- raw path、project source path 或真实 object binding；
- parser character-data dump；
- gateway payload dump；
- full stdout／stderr 中的 payload；
- `story_structure.yaml`；
- `execution_report.md`；
- 人物、事件、主题、改编或剧本文件。

持久 evidence 只能保存结构 metadata、component identity、test ID、状态、offset、length、hash、计数、拒绝码和 signed attestation。

### 4.3 Writer 与权限

| 路径类别 | 唯一 writer | probe／reader 权限 |
| --- | --- | --- |
| `control/` | test control plane | 只读最小投影或不可见 |
| `evidence/registry_events.jsonl` | authorization registry | 不可见／不可写 |
| `evidence/broker_events.jsonl` | broker monitor | 不可见／不可写 |
| sandbox／parser／gateway／write evidence | 各独立 observer | 不可写 |
| formal loader evidence | formal loader test controller | 不可写 |
| `attestations/` | audit aggregator | 不可写 |
| case `case_result.yaml` | case test controller | 不可写 |
| suite `aggregate/` 与 `report/` | suite audit controller | 不可写 |

任何错误 writer、额外持久文件、payload bytes、Candidate Run 路径或 production artifact class 出现，都使该 attempt invalid。

### 4.4 Case attempt presence matrix

| Attempt 状态 | control | evidence | attestations | report |
| --- | --- | --- | --- | --- |
| sandbox／layout 初始化前失败 | 不要求 | 外部 denial evidence | 不要求 | 外部测试控制器记录，不强建 attempt root |
| authorization 前失败且 root 安全 | draft／denied 可存在 | 已到达 observer 的真实 evidence | closure 可记录 not_reached | 必须记录 blocker |
| authorization 已消费、broker 前失败 | authorization／snapshot 必须存在 | registry evidence 必须存在 | closure 必须绑定 spent state | 必须存在 |
| broker／reader 失败 | control 必须存在 | actual calls／failure evidence 必须存在 | scope attempted + closure | 必须存在 |
| Prototype PASS | control 完整 | 七域 evidence 完整 | scope + closure 均存在 | 必须存在且结论唯一 |

不得通过创建空 evidence、伪造零计数或删除失败工件满足 matrix。

### 4.5 Suite 聚合不变量

- suite manifest 在 leaf attempts 前冻结，并记录每个 requirement group、leaf case、expected result、独立 attempt ID 与是否需要 grant；
- authorization-related leaf case 与 grant 一对一；并发 CAS case 内可有两个竞争消费者，但仍只有一个 grant 和最多一个成功 event；
- suite component snapshot、profile、keys、sandbox backend 或 fixture recipe 任一变化都要求新 suite ID；
- aggregate 必须记录 manifest leaf count、runner discovered count、executed count、pass／fail／skip／unknown 与 evidence-complete count，并要求机械相等；
- `synthetic_greek_fixture_existence_attestation.yaml` 只保存 synthetic object ID、size、digest、fixture-controller identity 与 existence proof，不保存 payload或真实 Greek path；
- broker／consumer environment snapshots 必须分别记录 mount、catalog、FD、network 与 monitor coverage；
- suite report 完成后的 checksum 由外部 prototype test registry 记录，不写回报告本身。

## 5. 验收标准

### 5.1 Component acceptance

| Acceptance ID | 组件 | PASS 条件 |
| --- | --- | --- |
| `P2F-AC-001` | registry | CAS 一次成功、replay 失败、authorization 文件不可变、spent 不回退 |
| `P2F-AC-002` | issuer | 无成功 consumption event 时 capability 数为 0；test-only issuer／audience／key 生效 |
| `P2F-AC-003` | broker | 只接受 opaque token；actual union 精确等于 `[4076,36515)`；范围外 bytes 为 0 |
| `P2F-AC-004` | broker | wrong source／range／token／hash fail closed，无 EOF／full-hash fallback、无自动重试 |
| `P2F-AC-005` | reader | 无 path／offset／length API；只消费一次性 signed envelope 与 sealed slice |
| `P2F-AC-006` | reader sandbox | full fixture、workspace、source tree、Greek-like object、网络源均不可见；full-object handle 为 0 |
| `P2F-AC-007` | parser／gateway | 只见 Book 1、10 Card 与 10 Paragraph markers；Book 2／prefix／suffix／Greek markers 为 0；模型调用为 0 |
| `P2F-AC-008` | formal loader | Candidate／prototype、link、复制、重命名、去标记、伪 manifest 与 TOCTOU 均产生 0 个 formal content input；formal positive control 恰为 1 |
| `P2F-AC-009` | read audit | 五域 evidence 完整、不可由 probe 改写、同一 attempt/auth/event/capability/delivery 关联闭合；tamper／replay 被拒绝 |
| `P2F-AC-010` | closure | write／formal check、artifact presence、最终状态闭合；没有 self-hash 循环 |
| `P2F-AC-011` | signed profiles | 三类 profile 的 protected `alg/typ/kid/version`、issuer、subtype audience、time 与 key status 全冻结；所有错误向量拒绝 |
| `P2F-AC-012` | suite isolation | 每个 leaf case 有唯一 RCPT attempt；authorization-related case 独立 grant；suite manifest、runner 与 evidence counts 完全一致 |

### 5.2 Test-suite acceptance

未来 prototype 只有在以下全部成立时才能标记：

```yaml
prototype_result: "PASS_RUNTIME_CAPABILITY_PROTOTYPE"
planned_requirement_groups: 37
mandatory_tests_total: "<actual manifest enumeration>"
mandatory_tests_passed: "<must equal actual total>"
mandatory_tests_failed: 0
mandatory_tests_skipped: 0
mandatory_tests_unknown: 0
positive_exact_range_test_passed: true
replay_tests_passed: true
full_object_isolation_tests_passed: true
greek_deny_chain_tests_passed: true
formal_loader_exclusion_tests_passed: true
five_domain_audit_tests_passed: true
signed_object_profile_tests_passed: true
suite_manifest_runner_counts_match: true
real_source_access_count: 0
model_invocations: 0
candidate_runs_executed: 0
business_outputs_created: 0
```

测试数量必须由 future suite manifest 的真实 leaf-case 枚举和 test runner 输出得出，不能凭计划表或手工摘要宣称完成。上表当前规划 37 个 requirement groups，其中复合向量必须展开为多个 leaf cases；因此 `37` 不是 mandatory test 总数。Report 必须同时记录 manifest leaf count、runner discovered count、executed count 与 evidence-complete count，并要求相等。

### 5.3 Fail-closed 结果

以下任一情况使总结果为 `BLOCKED_RUNTIME_CAPABILITY_PROTOTYPE_FAILED`：

- 任一 required component 未实现或 identity／digest 未冻结；
- 任一 mandatory test fail、skip、timeout、unknown 或证据缺失；
- consumer 能看到 full fixture path／handle／mount；
- broker 接受 caller-supplied range；
- registry replay 成功或 capability 在 CAS 前签发；
- 并发双消费出现 0 个或多于 1 个成功，或 CAS 后崩溃导致 spent grant 被复原／补发；
- grant、capability、delivery、nonce 或 attestation 跨 leaf case 复用；
- signed object 接受 `alg=none`、错误 typ/version、未知／撤销 key、错误 audience、过期／尚未生效时间或 test／production trust-root 混用；
- actual union 超出或不等于获批 range；
- Greek-like object 成功 open／read／parse／gateway delivery；
- 真实 English／Greek source 被 stat、打开、读取、hash 或扫描；
- model 被调用；
- payload bytes 进入持久 evidence／report；
- formal loader 发现 Candidate／prototype 内容输入；
- formal positive control 不能加载恰好 1 项，或 TOCTOU swap 未被拒绝；
- audit 只依赖 probe 自报或无法关联同一测试尝试；
- 生成任何 Candidate business output 或 Candidate Run artifact。

不得把部分组件 PASS 汇总为整体 PASS，也不得用“测试环境限制”把 required isolation 降级为 warning。

### 5.4 Prototype PASS 能证明与不能证明的事项

Prototype PASS 可以证明：

- synthetic fixture 上的一次性 authorization consumption 语义可实现；
- exact-range capability、broker、reader 与 anti-replay 链路可实现；
- consumer 对 full object 和 forbidden source 缺少访问能力；
- independent five-domain audit 与 formal-loader exclusion 可产生机械证据；
- Runtime Capability 具备进入 production implementation／approval 阶段的技术基础。

Prototype PASS 不能证明：

- 真实 English source identity、Book 1 slice 或 Map 在未来授权时仍匹配；
- B-overlay 已经批准并生效；
- production component build、key、sandbox 或 policy 与 prototype 相同；
- source snapshot、task scope、execution snapshot 或 output contract 已冻结；
- English 已获得 formal human approval；
- Greek Source Gate 已解除；
- Candidate 或 Formal Run 已授权；
- 任何文学分析结果正确或可晋级。

### 5.5 与修订合同 Gate 的映射

| Prototype evidence | 可支持的未来 Gate | 仍需未来生产态完成 |
| --- | --- | --- |
| registry／issuer test | `P2ER-G1A-001/002` 的实现证据 | production registry、key、authorization 与真实新 Run binding |
| broker tests | `P2ER-G0-013`、G1B 行为证据 | production component digest、真实 immutable object binding、真实 slice verification |
| reader／sandbox tests | `P2ER-G0-014/016` | production sandbox profile 与新 execution snapshot |
| audit tests | `P2ER-G0-015` | production observers、attestation issuer／audience 与真实 Run correlation |
| formal loader tests | `P2ER-G0-017` | production signed formal-manifest policy 与部署 identity |
| full synthetic suite | `P2ER-G0-020` 的设计基础 | 使用未来冻结的同一生产组件组合重新执行无正文 dry run |

Prototype report 不能直接把任何 `P2ER-*` Gate 写为 production PASS；它只能作为该 Gate 后续审查的 evidence input。

## 6. 与 Candidate Run 002 的关系

### 6.1 Run 002 保持历史阻断身份

`AC-20260811-STORYSTRUCT-002` 在本阶段保持：

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
authorization_may_be_added_in_place: false
run_directory_may_be_created: false
```

Prototype 不得：

- 使用 Run 002 作为 test attempt ID；
- 在 Run 002 下写 authorization、snapshot、output 或 audit；
- 把 test capability 绑定到 Run 002；
- 把 prototype PASS 回填为 Run 002 当时已具备的能力；
- 修改 Run 002 Plan 后重新执行；
- 为 Run 002 追溯授权或 execution report；
- 把 Run 002 的原始两项 variance 视为已批准。

### 6.2 新 Candidate Run Planning 的先决顺序

只有未来 Runtime Capability Prototype 达到 `PASS_RUNTIME_CAPABILITY_PROTOTYPE` 后，项目才可进入“重新规划新的 Candidate Run”的准备阶段。顺序必须是：

1. 按本文实现 prototype components 和 test harness；
2. 使用 synthetic fixtures 完成全部 mandatory tests；
3. 独立审查 prototype report、component identities、test runner 输出与零真实来源证据；
4. 形成并批准 B-overlay 的实际 implementation／effective policy；
5. 将准备投入真实运行的 production component builds、keys、sandbox、audit 与 formal-loader identities 冻结；
6. 重新执行 production 组合的无正文 dry run；
7. 创建一份专属的新 Candidate Run Plan；
8. 按真实授权日期分配新的、未使用的 `AC-YYYYMMDD-STORYSTRUCT-NNN`；
9. 为新 ID 重新冻结 source snapshot、Map、task scope、execution snapshot 与 output contract；
10. 另行完成 Gate 审查与一次性 authorization。

Prototype PASS 只允许开始第 4–7 项的工程／规划工作，不自动完成它们。新的 Candidate Run Plan 必须引用 prototype 的最终 component／test evidence，但不能继承 test authorization、test key、fixture object、RCPT attempt 或 test attestation。

### 6.3 Prototype 未通过时

若 future prototype 为 blocked／failed：

- 不创建新的 Candidate Run Plan；
- 不分配新的 Candidate Run ID；
- 不打开真实 English raw；
- 不切换到直接文件读取、全文解析或 prompt-only scope enforcement；
- 不访问 Greek；
- 只允许在新的 `RCPT-*` attempt 中修复组件并重跑 synthetic tests；
- 失败 attempt、spent authorization、capability 和 delivery 永不复用。

## 7. 本阶段结论与未执行动作

Phase 2-F 的设计结论是：最小 Runtime Capability 验证必须在独立的 synthetic、test-only 信任域中证明一次性授权消费、exact-range broker、无 full-object 能力的 bounded reader、Greek deny chain、formal-loader exclusion 与独立五域 read audit。只有完整 prototype suite 通过并接受独立审查，项目才能重新规划新的 Candidate Run；Run 002 永久保持不可复用。

```yaml
phase: "Phase 2-F"
task: "Runtime Capability Prototype Design"
document: "RUNTIME_CAPABILITY_PROTOTYPE_PLAN.md"
document_status: "ready_for_review"
current_effect: "prototype_plan_only"

prototype_namespace: "RCPT-*"
prototype_implementation_created_this_task: false
prototype_test_artifact_root_created_this_task: false
prototype_tests_executed_this_task: 0
prototype_result_claimed_this_task: false

authorization_registry_implemented_this_task: false
range_broker_implemented_this_task: false
bounded_reader_implemented_this_task: false
formal_loader_implemented_this_task: false
read_audit_implemented_this_task: false

new_candidate_run_id_allocated_this_task: false
new_candidate_run_plan_created_this_task: false
candidate_run_authorized: false
candidate_runs_executed_this_task: 0

english_tei_content_read_this_task: false
english_real_raw_access_count_this_task: 0
greek_real_raw_access_count_this_task: 0
book_structure_map_read_count_this_task: 0
model_invocations_this_task: 0
story_structure_output_created_this_task: false
execution_report_created_this_task: false
candidate_run_directory_created_this_task: false
character_database_created_this_task: false
event_database_created_this_task: false
theme_database_created_this_task: false
adaptation_or_script_outputs_created_this_task: false
source_map_gate_or_status_files_modified_this_task: 0
formal_phase_2_authorized: false

associated_run_id: "AC-20260811-STORYSTRUCT-002"
associated_run_reusable: false
associated_run_status_changed_this_task: false
```

本文完成只表示 Runtime Capability Prototype 已形成可实施、可审查的设计计划。它不实现组件，不执行测试，不读取真实来源，不生成 Candidate 内容，不批准 B-overlay，不授权或执行任何 Run，也不改变 English、Greek、Run 002 或 Formal Phase 2 的既有状态。
