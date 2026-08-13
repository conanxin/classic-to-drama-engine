# Classic-to-Drama Engine：Candidate Execution Contract Repair

> 项目：Classic-to-Drama Engine  
> 阶段：Phase 2-E-R  
> 文档类型：Candidate Execution Contract Repair  
> 日期：2026-08-11  
> 文档状态：`ready_for_review`  
> 当前效力：`repair_specification_only / not_implemented / not_authorized`  
> 关联阻断 Run：`AC-20260811-STORYSTRUCT-002`  
> 关联状态：`BLOCKED_BEFORE_CONTENT_READ`  
> Candidate 正文读取授权：否  
> Formal Phase 2 授权：否

## 0. 目的、依据与本阶段边界

本文修复 `AC-20260811-STORYSTRUCT-002` 在 Phase 2-E 授权检查中暴露的执行合同缺口。修复对象包括：B-overlay 尚未实现、source snapshot 与其他运行合同尚未冻结、一次性授权缺失、业务输出与审计输出的文件合同冲突，以及 range broker、bounded reader、formal loader 隔离和独立 read audit 尚无可验证实现。

本文只依据以下三份文件：

| 依据文件 | 本阶段读取时 SHA-256 | 用途 |
| --- | --- | --- |
| `CANDIDATE_RUN_002_PLAN.md` | `75f86e219cd2c75b89e5dcd906973df9dddb0b7ec6baf65dadd6d6bb5ff74112` | Run 002 的输入、范围、20 项 preflight、原输出合同与阻断规则 |
| `ANALYSIS_CANDIDATE_WORKFLOW.md` | `dff075de96729332f324ce6a07332129d49d2cbece766a3b5411ca18664bbc50` | B-overlay、候选授权、隔离、不可晋级与 formal handoff 的通用设计 |
| `TEXT_STRUCTURE_MAPPING_SPEC.md` | `259df6ceb6464ae7eadc84bc5603f3bdd16c603f5fe5c9ba9f82e3836cfcc3eb` | validated structure map、exact-range 输入与 scope proof 的技术合同 |

本阶段只创建本修订文档，不会：

- 打开、扫描、解析或分析 English TEI 正文；
- 打开或访问 Greek raw；
- 创建、授权或执行任何 Candidate Run；
- 创建 `analysis_candidate/runs/<run_id>/`；
- 创建 `story_structure.yaml`、`execution_report.md` 或任何运行工件；
- 创建人物、事件、主题、母题、改编、分集、场景或剧本数据；
- 实现、测试或宣称已部署 range broker、bounded reader、formal loader、read audit 或 B-overlay；
- 修改 Run 002 计划、raw、structure map、Gate、Source Layer 或正式 Analysis Layer。

本文形成的是**未来新 Run 的执行合同修订规范**。本文获得评审通过，也只表示修订设计可进入实现；不表示 B-overlay 已生效，不表示运行组件已通过测试，更不构成任何 Run 的一次性授权。

### 0.1 合同适用与优先级

1. 本文不原地修订、重开或补授权 Run 002。
2. 本文不全局改写 `ANALYSIS_CANDIDATE_WORKFLOW.md`；它为未来新 Run 定义一组必须显式批准的 Run-specific 修订。
3. 未来新 Run 的有效合同必须同时引用：已批准的 B-overlay 实现合同、本文的获批版本、为该新 ID 单独创建并批准的新 Run Plan、validated structure map、冻结的运行工件和一次性授权记录。
4. 若本文与未来获批的 Run Plan、authorization artifact 或实际 runtime identity 不一致，正确结果是在正文交付前阻断；不得选择较宽松条款继续。
5. 所有 `<new_run_id>`、`<identity>`、`<sha256>`、`<timestamp>` 等占位符必须在授权前替换为真实、可复核值。任何占位符、`TBD`、`unknown` 或未批准状态存在时，Gate 不得 PASS。

### 0.2 已知范围基线

本文只继承 Run 002 Plan 中已经登记的结构范围身份，不重新读取来源或 structure map：

```yaml
source_id: ODY-ENG-MURRAY1919
source_object_id: urn:sha256:dda5b206e332e56c570c1d92ea41e9a510339a454bc2ea90491788e34174a7e7
source_full_sha256: dda5b206e332e56c570c1d92ea41e9a510339a454bc2ea90491788e34174a7e7
fixed_upstream_commit: 790c84289edbdbe289dd7b752bfea29f0af4299d
structure_map_id: ODY-ENG-MURRAY1919-TEI-STRUCTURE-MAP-20260811
structure_map_file_sha256: fd0314844ee2e9c28487ea3d717d3bc75a96be4cbe0a9c74cb2defd8640d6bc3
mapping_payload_sha256: 45740c706b615bb0f83d5b763db189bff0b87228e5814f5f16b92f46dc5faaa5
selected_books: [1]
allowed_byte_range:
  start_byte: 4076
  end_byte_exclusive: 36515
expected_slice_size_bytes: 32439
expected_slice_sha256: 7bd8baca8c89f91c1cad6ca54c9e6e8f1eae1139d7543ef0941a88f83151ac39
expected_card_count: 10
```

这些值是未来冻结与校验的预期基线，不是本阶段重新验证的结果，也不自动授予 English Candidate 使用资格。

## 1. 当前阻断项分析

### 1.1 阻断总表

| 阻断项 | 当前证据 | 为什么不能执行 | 本文的修复决定 | 解除条件 |
| --- | --- | --- | --- | --- |
| B-overlay 未实现 | `ANALYSIS_CANDIDATE_WORKFLOW.md` 自声明 `design_only / not_implemented`、`candidate_architecture_approved: false` | 通用 Candidate 权限模型尚不是有效执行合同，不能仅靠单次用户指令跳过 | 要求独立的、版本化且已实现的 B-overlay execution policy；本文只定义其验收接口 | policy 文件、实现身份、批准记录和无正文测试全部 PASS |
| snapshot 未冻结 | Run 002 Plan 中 source snapshot、task scope、execution snapshot、output contract 仍为 `proposed / must_*_before_authorization` | 输入、方法、组件或输出可在授权后漂移，无法证明执行与批准对象相同 | 将 frozen source/task/output bindings 放入 authorization artifact，将模型、prompt、schema、工具与参数放入 execution snapshot | 所有 block 均为 `frozen / approved`，digest 可独立复算且无占位符 |
| authorization 缺失 | 没有精确绑定 Run、全部摘要、组件身份和输出合同的一次性授权记录 | “执行 Run 002”的自然语言命令没有满足既有 20 项 preflight 的完整授权链 | 为未来新 Run 定义唯一 `authorization.yaml`；只有该文件可设置一次性 run authority | 授权状态 `approved`、未过期、未消费，绑定值与运行时逐项匹配 |
| output contract 冲突 | Run 002 Plan 把 `output/story_structure.yaml` 规定为唯一运行文件；Phase 2-E 又要求根目录下 `execution_report.md`；通用 workflow 还要求 `candidate__` 前缀及多类控制工件 | 直接创建报告会违反冻结的单文件合同；不创建报告又无法保留授权与 scope proof 审计 | 用 artifact class 分离 control、business output 与 audit；按类别计数和 allowlist，不再用“唯一运行文件”混淆三类工件 | 新 Run 的 output contract 明确批准四工件布局和两项 Run-specific variance |
| range broker 缺失 | 只有设计要求，没有可调用实现、版本、digest 或测试证据 | Candidate 无法在不接触完整 raw 的情况下取得 Book 1 exact range | 定义只由 broker 绑定 immutable source object、接受 capability-scoped exact range 的接口 | 实现身份冻结，正向及拒绝测试 PASS，Candidate 对 raw 零访问能力 |
| bounded reader 缺失 | 没有证明 reader 无 EOF／全文 fallback，也没有固定 API | 即使有 range 数据，也不能证明 reader 不扩大范围或重新打开 source | reader 只能消费 broker 返回的内存 slice；不得接受 path 或任意 offset | fixture 测试证明只请求获批 range、长度/hash匹配、所有 fallback 被拒绝 |
| independent read audit 缺失 | Candidate 自报不能证明实际 read ranges；无独立 audit authority | 无法机械证明 Book 2–24 与 Greek 访问为 0 | audit 由 broker 或独立 monitor 生成，Candidate 无写权限；report 只引用其 identity 与 digest | actual read calls、union、越界字节、直接访问、Greek 访问均可独立复核 |
| formal loader 隔离缺失 | 只有“应排除 `analysis_candidate/`”的设计声明，没有 loader identity 与负向测试 | Candidate 裸文件名可能被 formal discovery、manifest 或下游加载器误发现 | formal loader 必须实施根路径硬排除并通过负向 fixture | loader version/digest 冻结，candidate tree、symlink 与裸文件名均不可被发现 |

### 1.2 B-overlay：设计存在不等于执行能力存在

`ANALYSIS_CANDIDATE_WORKFLOW.md` 已经定义 source lifecycle、analysis eligibility 与 run authority 三条独立控制轴，但其当前效力明确是 `design_only / not_implemented`。因此，validated structure map 只能解除结构边界问题，不能替代 Candidate architecture 的实现与批准。

未来 B-overlay 必须至少提供：

- 一个稳定 `overlay_contract_id`、版本和完整文件 digest；
- 可执行的入口 Gate，分别检查来源资格、任务资格与单次 Run authority；
- 对 Greek raw、范围外 English、formal path 和下游消费的 deny rules；
- artifact class allowlist 与写入边界执行；
- 失效、阻断、一次性授权消费和 Run ID 不复用规则；
- 只使用无正文 fixture 的正向、越界、缺授权、过期授权、路径逃逸与 formal discovery 测试；
- 独立批准记录，明确 `implemented: true` 与 `effective: true`。

本文不创建这些实现或批准记录。未出现上述真实证据时，B-overlay Gate 必须继续返回 `BLOCKED_OVERLAY_NOT_IMPLEMENTED`。

### 1.3 Snapshot：必须冻结的是完整执行对象

未来授权不能只绑定 source SHA-256。不可拆分的授权对象必须为：

```text
candidate_execution_binding =
  new_run_id
  + new_run_plan_digest
  + new_run_plan_approval_digest
  + overlay_contract_digest
  + repair_contract_digest
  + source_snapshot_digest
  + structure_map_file_digest
  + structure_map_payload_digest
  + task_scope_digest
  + execution_snapshot_digest
  + output_contract_digest
  + runtime_component_digests
  + isolation_policy_digest
```

其中：

- source snapshot 必须绑定同一个 immutable/content-addressed `source_object_id`；
- structure map 的完整文件 digest 与 `CTDE-MAP-C14N-1` payload digest 必须分别复算；
- task scope 必须固定为 English `ODY-ENG-MURRAY1919`、Book 1、`[4076,36515)`、10 Cards、`story_structure_extraction`；
- execution snapshot 必须冻结模型、prompt、schema、parser、wrapper、broker、reader、audit、loader、参数与运行环境身份；
- output contract 必须冻结 artifact class、路径、writer、生成条件、内容限制和 formal exclusion。

任何一项变化都使原授权失效，不能在同一 Run ID 下更新摘要后继续。

### 1.4 Authorization：自然语言执行命令不能替代闭合记录

一次性授权必须是可机械读取的控制工件，明确回答：谁或哪一授权机制批准、批准了哪个新 Run、精确批准哪一份新 Run Plan 及其 approval、哪些 digest、何时生效和失效、是否已被消费。授权记录不能从计划文件存在、用户意图、Map 已验证或组件测试通过中推断。`CANDIDATE_RUN_002_PLAN.md` 只能作为历史证据，不能作为未来新 Run 的 active plan binding。

授权记录必须遵守：

未来 finalized authorization 的 PASS 值必须是：`candidate_run_authorized = true`、`formal_phase_2_input = false`、`candidate_output_promotable = false`、`downstream_consumption_allowed = false`、`one_time_authorization = true`、`automatic_retry_allowed = false`、`authorization_inheritable = false`。这些值只能由已经批准的新 Run authorization artifact 表达。

本文、旧 Plan、structure map、测试报告和审计报告均不得自行设置或暗示当前 `candidate_run_authorized = true`。

### 1.5 Output conflict：按工件类别修订，而不是扩大业务输出

原冲突来自把所有落盘文件都称为“输出”。修订后使用四种工件角色：

1. `authorization artifact`：控制面批准与不可拆分输入绑定；
2. `execution snapshot`：冻结实际方法和运行组件；
3. `output artifact`：唯一业务内容输出 `story_structure.yaml`；
4. `audit artifact`：独立审计输出 `execution_report.md`。

因此：

- `story_structure.yaml` 仍是唯一**业务输出**；
- `execution_report.md` 是唯一**Run-local 审计报告**，不属于业务内容输出；
- authorization 与 execution snapshot 是只读控制工件，不属于运行内容输出；
- 文件数量按 artifact class 分别校验，不能再使用一个全局 `planned_output_file_count: 1` 排除必要审计；
- 新 Run 若未生成业务结果，`story_structure.yaml` 必须不存在，但 `execution_report.md` 仍可记录 `blocked / failed / cancelled / invalidated`；
- report 不得包含来源正文、摘要或文学判断。

### 1.6 Broker／reader／audit：设计声明不能作为范围证明

Run 002 已有 range、slice hash 与 Card allowlist，但没有真实组件身份和独立观测。因此下列说法均不足以 PASS：

- “代码理论上可以使用 `pread`”；
- “Candidate 被 prompt 要求只分析 Book 1”；
- “Candidate 日志自报只读取了 Book 1”；
- “输出只引用 Book 1 locator”；
- “完整文件是只读的”；
- “Map 已 validated”。

范围证明必须来自实际隔离能力、exact-range 交付和不可由 Candidate 改写的 read audit。组件任一缺失或证据为 `unknown` 时，应在正文交付前阻断。

## 2. 修订后的 Run Artifact Layout

### 2.1 新 Run 专用布局

未来新 Run 只允许以下关闭式布局：

```text
analysis_candidate/runs/<new_run_id>/
├── control/
│   ├── authorization.yaml
│   └── execution_snapshot.yaml
├── output/
│   └── story_structure.yaml
└── audit/
    └── execution_report.md
```

这四个路径构成完整 allowlist。除它们外，不得在新 Run 根内创建 manifest、自由文本日志、正文副本、临时文件、cache、normalized、alignment、evaluation、review、数据库、链接或隐藏文件。

运行中的中间值必须保留在隔离内存或受控临时运行时中，不得作为额外 Run artifact 落盘。`story_structure.yaml` 只能在业务 schema、范围与禁止项检查全部通过后由 output publisher 原子发布；不得把半成品或失败结果留在该路径。

### 2.2 工件角色与写入权限

| 工件 | Artifact class | 唯一 writer | Candidate 权限 | 生成时点 | 是否计入业务输出 |
| --- | --- | --- | --- | --- | --- |
| `control/authorization.yaml` | `candidate_authorization` | 独立 control plane／授权机制 | 只读最小投影；不可修改 | 新 Run 启动前 | 否 |
| `control/execution_snapshot.yaml` | `candidate_execution_snapshot` | Orchestrator／snapshot freezer | 只读；不可修改 | 新 Run 启动前 | 否 |
| `output/story_structure.yaml` | `analysis_candidate_business_output` | 隔离 Candidate 的 output publisher | 只能通过受控发布接口创建；不可写其他路径 | 内容任务成功并通过输出校验后 | 是，且是唯一业务输出 |
| `audit/execution_report.md` | `candidate_execution_audit` | 独立 audit controller | 不可创建、修改或删除 | 每次已分配新 Run 的授权／preflight／执行尝试结束时 | 否 |

`authorization.yaml` 与 `execution_snapshot.yaml` 必须在 Candidate 启动前完成写入并转为只读。`execution_report.md` 的 writer 必须与 Candidate 内容进程分离。Candidate 不能通过自身日志覆盖独立 audit。

### 2.3 Authorization artifact 合同

`control/authorization.yaml` 是未来新 Run 的唯一 run authority 与控制清单。下列代码块是**不可执行的 draft schema 示例**；其默认状态故意保持未授权，不能复制后直接启动：

```yaml
schema_version: "1.0.0"
template_execution_status: "non_executable_draft_example"
artifact_class: "candidate_authorization"
authority: "control_plane"

run:
  run_id: "<new_run_id>"
  run_id_status: "reserved"
  retry_of_run_id: "AC-20260811-STORYSTRUCT-001"
  supersedes_run_id: "AC-20260811-STORYSTRUCT-002"
  run_id_date_matches_authorization_date: true
  reusable: false
  automatic_retry_allowed: false

authorization:
  authorization_id: "<unique authorization id>"
  status: "draft"
  candidate_run_authorized: false
  one_time: true
  issued_at: "<ISO-8601>"
  expires_at: "<ISO-8601 or approved non-expiring policy>"
  approved_by_or_mechanism: "<verifiable identity>"
  approval_evidence_ref: "<immutable reference>"
  approval_evidence_sha256: "<sha256>"
  consumption_status_at_issue: "unconsumed"
  consumption_registry_ref: "<external immutable registry ref>"
  formal_phase_2_authorized: false

contract_bindings:
  new_run_plan_id: "<new Run Plan id>"
  new_run_plan_file_sha256: "<sha256>"
  new_run_plan_approval_ref: "<immutable approval reference>"
  new_run_plan_approval_sha256: "<sha256>"
  overlay_contract_id: "<implemented overlay id>"
  overlay_contract_sha256: "<sha256>"
  repair_document: "CANDIDATE_EXECUTION_CONTRACT_REPAIR.md"
  repair_document_sha256: "<sha256>"
  contract_canonicalization: "CTDE-CANDIDATE-CONTRACT-C14N-1"
  source_snapshot_id: "<source snapshot id>"
  source_snapshot_sha256: "<canonical block digest>"
  structure_map_file_sha256: "fd0314844ee2e9c28487ea3d717d3bc75a96be4cbe0a9c74cb2defd8640d6bc3"
  mapping_payload_sha256: "45740c706b615bb0f83d5b763db189bff0b87228e5814f5f16b92f46dc5faaa5"
  task_scope_id: "<task scope id>"
  task_scope_sha256: "<canonical block digest>"
  execution_snapshot_file_sha256: "<sha256>"
  output_contract_id: "<output contract id>"
  output_contract_sha256: "<canonical block digest>"
  isolation_policy_sha256: "<sha256>"

source_snapshot:
  block_id: "<source snapshot id>"
  block_status: "draft"
  source_id: "ODY-ENG-MURRAY1919"
  file_id: "ODY-ENG-MURRAY1919-RAW-FULL-TEI"
  language: "English"
  source_lifecycle_status: "acquired_verified"
  formal_human_approval_status: "pending"
  analysis_eligibility: "not_granted"
  requested_source_role: "candidate_working_source_for_this_run_only"
  source_object_id: "urn:sha256:dda5b206e332e56c570c1d92ea41e9a510339a454bc2ea90491788e34174a7e7"
  fixed_upstream_commit: "790c84289edbdbe289dd7b752bfea29f0af4299d"
  size_bytes: 870905
  sha256: "dda5b206e332e56c570c1d92ea41e9a510339a454bc2ea90491788e34174a7e7"
  approved_source_record_ref: "<immutable SOURCE_RECORD reference>"
  approved_source_record_sha256: "<sha256>"
  approved_source_object_binding_ref: "<control-plane object binding; not exposed to Candidate>"
  candidate_gate_snapshot_id: "<gate snapshot id>"
  candidate_gate_snapshot_sha256: "<sha256>"
  immutable_object_attestation_id: "<valid attestation id>"
  immutable_object_attestation_sha256: "<sha256>"
  native_locator_scheme: "book.card"
  capabilities:
    map_bound_exact_range_supported: true
    canonical_range_supported: false
    alignment_available: false
    normalization_required_for_this_task: false
  known_exceptions:
    - "NOTICE_CREFPATTERN_CARD_SEPARATOR_UNESCAPED"
  formal_phase_2_input: false

structure_map_binding:
  binding_status: "draft"
  expected_file_kind: "regular_file"
  symbolic_link_allowed: false
  map_id: "ODY-ENG-MURRAY1919-TEI-STRUCTURE-MAP-20260811"
  schema_version: "1.0.0"
  mapping_status_required: "validated"
  file_sha256: "fd0314844ee2e9c28487ea3d717d3bc75a96be4cbe0a9c74cb2defd8640d6bc3"
  mapping_payload_sha256: "45740c706b615bb0f83d5b763db189bff0b87228e5814f5f16b92f46dc5faaa5"
  specification: "TEXT_STRUCTURE_MAPPING_SPEC.md"
  specification_sha256: "259df6ceb6464ae7eadc84bc5603f3bdd16c603f5fe5c9ba9f82e3836cfcc3eb"
  specification_approval_ref: "<immutable approval reference>"
  specification_approval_sha256: "<sha256>"
  validation_attestation_id: "<attestation id>"
  validation_attestation_sha256: "<sha256>"
  selected_book: 1
  start_byte: 4076
  end_byte_exclusive: 36515
  slice_size_bytes: 32439
  slice_sha256: "7bd8baca8c89f91c1cad6ca54c9e6e8f1eae1139d7543ef0941a88f83151ac39"
  card_count: 10
  paragraph_count: 10
  paragraph_spans_computable: true
  book_element_qname: "{http://www.tei-c.org/ns/1.0}div"
  book_discriminators:
    type: "textpart"
    subtype: "book"
    n: "1"
  card_representation_kind: "container"
  paragraph_element_qname: "{http://www.tei-c.org/ns/1.0}p"
  mapping_ambiguities_required: []
  retained_notices:
    - "NOTICE_CREFPATTERN_CARD_SEPARATOR_UNESCAPED"

task_scope:
  block_id: "<task scope id>"
  block_status: "draft"
  primary_task: "story_structure_extraction"
  purpose: "validate_map_bounded_candidate_story_structure_method"
  selected_books: [1]
  allowed_byte_ranges:
    - start_byte: 4076
      end_byte_exclusive: 36515
  approved_card_locators:
    - "1.1"
    - "1.44"
    - "1.80"
    - "1.125"
    - "1.178"
    - "1.230"
    - "1.280"
    - "1.325"
    - "1.365"
    - "1.421"
  max_books: 1
  max_cards: 10
  max_output_structure_units: 10
  max_model_invocations: 1
  automatic_retries: 0
  stop_conditions:
    - "identity_or_digest_mismatch"
    - "range_or_slice_mismatch"
    - "book_or_card_outside_allowlist"
    - "missing_independent_scope_proof"
    - "forbidden_input_or_output_detected"
  evaluation_method_id: "<closed evaluation method id>"
  evaluation_method_sha256: "<sha256>"
  greek_raw_access_allowed: false
  character_event_theme_adaptation_tasks_allowed: false
  formal_phase_2_input: false

output_contract:
  block_id: "<output contract id>"
  block_status: "draft"
  business_output_allowlist:
    - "output/story_structure.yaml"
  audit_output_allowlist:
    - "audit/execution_report.md"
  control_artifact_allowlist:
    - "control/authorization.yaml"
    - "control/execution_snapshot.yaml"
  business_output_file_count_max: 1
  artifact_presence_matrix_ref: "CANDIDATE_EXECUTION_CONTRACT_REPAIR.md#2.7"
  artifact_presence_matrix_contract_sha256: "<repair document sha256>"
  approved_variances:
    - variance_id: "OUTPUT_FILENAME_CONTRACT_VARIANCE_V2"
      scope: "<new_run_id>_only"
      approval_status: "pending"
      approval_ref: "<immutable approval reference>"
      approval_sha256: "<sha256>"
    - variance_id: "CONTROL_ARTIFACT_SET_VARIANCE_V2"
      scope: "<new_run_id>_only"
      approval_status: "pending"
      approval_ref: "<immutable approval reference>"
      approval_sha256: "<sha256>"
  output_authority: "non_authoritative"
  promotion_status: "non_promotable"
  candidate_output_promotable: false
  downstream_consumption_allowed: false

runtime_bindings:
  authorization_registry: "<id, version, digest>"
  capability_issuer: "<id, version, digest>"
  range_broker: "<id, version, digest>"
  bounded_reader: "<id, version, digest>"
  read_audit_aggregator: "<id, version, digest>"
  sandbox_or_syscall_monitor: "<id, version, digest>"
  parser_scope_monitor: "<id, version, digest>"
  model_input_gateway: "<id, version, digest>"
  write_monitor: "<id, version, digest>"
  formal_loader: "<id, version, digest>"
  candidate_sandbox_profile: "<id, version, digest>"
  scope_proof_level: "candidate_visible_bytes_and_application_exact_range"
  signed_object_profiles:
    capability: "<CTDE-CAPABILITY-JWS-1 implementation id and digest>"
    broker_envelope: "<CTDE-BROKER-ENVELOPE-JWS-1 implementation id and digest>"
    audit_attestation: "<CTDE-AUDIT-ATTESTATION-JWS-1 implementation id and digest>"

forbidden_inputs:
  greek_raw: true
  english_bytes_outside_approved_range: true
  candidate_direct_source_access: true

formal_phase_2_input: false
candidate_output_promotable: false
downstream_consumption_allowed: false
```

Finalized authorization 只有在以下状态值全部成立时才可通过 G0；draft 示例本身永远不能通过：

| 字段 | G0 所需值 |
| --- | --- |
| `template_execution_status` | 字段必须从最终 artifact 中移除，或严格改为 schema 规定的 `finalized_artifact` |
| `authorization.status` | `approved` |
| `authorization.candidate_run_authorized` | `true`，且只有已批准的 finalized artifact 可以表达 |
| `source_snapshot.block_status` | `frozen_approved` |
| `source_snapshot.analysis_eligibility` | `analysis_candidate_for_this_run_only` |
| `structure_map_binding.binding_status` | `frozen_verified` |
| `task_scope.block_status` | `frozen_approved` |
| `output_contract.block_status` | `frozen_approved` |
| 两项 variance `approval_status` | 均为 `approved`，且 approval evidence digest 可复核 |
| 所有 placeholder | 0 个 |

规则：

- 授权 artifact 可以先以 `draft / denied / expired` 状态存在，但只有 finalized artifact 达到上表全部 PASS 值时才允许进入启动 Gate；
- `authorization.yaml` 的完整文件 SHA-256 由 control plane 在文件完成后计算，并记录在独立授权 registry 与最终 report 中；不得写回文件自身形成递归 checksum；
- finalized `authorization.yaml` 永久不可变；其消费状态不写回该文件，而由外部 authorization registry 以原子 compare-and-set 记录；
- 在 broker capability mint **之前**，registry 必须把该 authorization 从 `unconsumed` 原子转为 `spent`，生成不可重放的 `consumption_event_id`；即使后续 slice／reader／模型前 Gate 失败，该授权仍保持 spent，若需重试必须分配新 Run ID；
- Candidate 不得接收 `raw_path`、完整 source 文件描述符、authorization secret 或可扩大范围的 capability。

#### 2.3.1 Contract digest canonicalization

`source_snapshot_sha256`、`task_scope_sha256`、`output_contract_sha256` 与 execution snapshot 的 payload digest 必须使用 `CTDE-CANDIDATE-CONTRACT-C14N-1`，不能依赖 YAML 实现的默认序列化：

1. 输入必须是 YAML 1.2 Core Schema 的单文档、safe-mode、JSON-compatible 子集；duplicate keys、custom tags、merge keys、anchors、aliases、float、timestamp、binary 与实现特有类型均拒绝；
2. 每个被摘要 block 必须有稳定 `block_id`；mapping key 为 Unicode string，value 只允许 `null`、boolean、base-10 integer、Unicode string、ordered array 或 mapping；
3. 对指定 block 的深拷贝删除其自身 digest 字段；source、task 与 output blocks 中不得存在其他自引用文件 digest；execution snapshot 删除 `freeze.snapshot_payload_sha256` 后再计算；
4. mapping keys 按 Unicode code point 升序，array 保持顺序，按无空白 canonical JSON 序列化；string escaping 与 control-character 规则沿用 `CTDE-MAP-C14N-1`，不做 Unicode normalization，拒绝 lone surrogate；
5. 使用域分离字节：`UTF8("CTDE-CANDIDATE-CONTRACT-C14N-1") + NUL + UTF8(block_id) + NUL + canonical_json_bytes`；对该字节串计算 SHA-256，输出 64 位小写十六进制；
6. authorization、snapshot freezer、Orchestrator 与 audit controller 必须独立复算并一致；block ID、canonicalization ID 和 digest 必须一起绑定；
7. `new_run_plan_file_sha256`、repair document digest、Map file digest、execution snapshot file digest 和 finalized authorization file digest 均为完整文件字节 SHA-256，不使用 block canonicalization；approval digest 是对应 immutable approval evidence 的完整字节 SHA-256；
8. finalized authorization 文件的 SHA-256 保存在外部 registry 与 report 中，不写回自身；消费事件引用该不可变文件 digest。

### 2.4 Execution snapshot 合同

`control/execution_snapshot.yaml` 必须冻结实际运行方法，而不是只写抽象名称。至少包括：

```yaml
schema_version: "1.0.0"
template_execution_status: "non_executable_draft_example"
artifact_class: "candidate_execution_snapshot"
authority: "control_plane"
run_id: "<new_run_id>"
snapshot_status: "draft"
block_id: "<execution snapshot block id>"

model:
  provider: "<identity>"
  model_id: "<exact id>"
  model_version: "<version or immutable revision>"
  parameters: "<closed mapping>"
  max_invocations: 1
  automatic_retries: 0

prompt:
  prompt_id: "<id>"
  version: "<version>"
  sha256: "<sha256>"

output_schema:
  schema_id: "<id>"
  version: "<version>"
  sha256: "<sha256>"

runtime_components:
  orchestrator: "<id, version, digest>"
  range_broker: "<id, version, digest>"
  bounded_reader: "<id, version, digest>"
  fragment_parser: "<id, version, digest>"
  namespace_wrapper_template: "<id, version, digest>"
  output_validator: "<id, version, digest>"
  output_publisher: "<id, version, digest>"
  authorization_registry: "<id, version, digest>"
  capability_issuer: "<id, version, digest>"
  read_audit_aggregator: "<id, version, digest>"
  sandbox_or_syscall_monitor: "<id, version, digest>"
  parser_scope_monitor: "<id, version, digest>"
  model_input_gateway: "<id, version, digest>"
  write_monitor: "<id, version, digest>"
  formal_loader: "<id, version, digest>"

scope_proof:
  level: "candidate_visible_bytes_and_application_exact_range"
  physical_device_read_ahead_proof_required: false

signed_object_profiles:
  capability:
    profile: "CTDE-CAPABILITY-JWS-1"
    algorithm: "<approved algorithm>"
    key_id: "<approved key id>"
    issuer: "<approved issuer>"
    audience: "<range broker component id>"
  broker_envelope:
    profile: "CTDE-BROKER-ENVELOPE-JWS-1"
    algorithm: "<approved algorithm>"
    key_id: "<approved key id>"
    issuer: "<range broker component id>"
    audience: "<bounded reader component id>"
  audit_attestation:
    profile: "CTDE-AUDIT-ATTESTATION-JWS-1"
    algorithm: "<approved algorithm>"
    key_id: "<approved key id>"
    issuer: "<audit aggregator component id>"
    audience: "<output validator and audit controller ids>"

sandbox:
  profile_id: "<id>"
  profile_sha256: "<sha256>"
  source_tree_visible: false
  generic_file_read_tools_available: false
  greek_raw_mounted: false
  network_source_fetch_allowed: false
  candidate_process_writable_paths: []
  output_publisher_writable_paths:
    - "analysis_candidate/runs/<new_run_id>/output/story_structure.yaml via publisher only"

freeze:
  frozen_at: "<ISO-8601>"
  frozen_by: "<verifiable identity>"
  snapshot_payload_sha256: "<canonical digest>"
```

只有删除／终结 draft sentinel、`snapshot_status=frozen`、所有 identity 与 digest 已填、按 `CTDE-CANDIDATE-CONTRACT-C14N-1` 复算 payload 并完成独立冻结批准后，该 snapshot 才能进入 authorization binding。模型、prompt、schema、parser、wrapper、runtime component、sandbox profile 或关键参数任一变化，都要求新 authorization 与新 Run ID。

### 2.5 Output artifact 合同

`output/story_structure.yaml` 是唯一业务输出，只能在新 Run 获批并成功处理 Book 1 后创建。它必须至少携带：

```yaml
artifact_class: "analysis_candidate_business_output"
authority: "non_authoritative"
promotion_status: "non_promotable"
run_id: "<new_run_id>"
source_id: "ODY-ENG-MURRAY1919"
selected_books: [1]
source_snapshot_id: "<bound source snapshot id>"
source_snapshot_sha256: "<bound digest>"
structure_map_id: "ODY-ENG-MURRAY1919-TEI-STRUCTURE-MAP-20260811"
structure_map_file_sha256: "fd0314844ee2e9c28487ea3d717d3bc75a96be4cbe0a9c74cb2defd8640d6bc3"
task_scope_id: "<bound task scope id>"
task_scope_sha256: "<bound digest>"
output_contract_id: "<bound output contract id>"
output_contract_sha256: "<bound digest>"
authorization_id: "<bound authorization id>"
execution_snapshot_file_sha256: "<bound digest>"
authorization_file_sha256: "<bound digest>"
scope_execution_attestation_id: "<pre-publication immutable attestation id>"
scope_execution_attestation_sha256: "<sha256 over complete signed object bytes>"
formal_phase_2_input: false
candidate_output_promotable: false
downstream_consumption_allowed: false
canonical_span: null
```

业务内容限制：

- 只能包含 Book 1 的候选 story structure units；
- unit 数量必须为 `1..10`；
- source span 只能使用冻结的 10 个 English `book.card` locator；
- 不得生成 Greek locator、canonical line 或 English–Greek alignment；
- 不得包含结构化人物、事件、主题、改编、分集、场景、对白或剧本字段；
- 不得复制大段来源正文；
- 任何 schema、identity、scope 或禁止项检查失败时，该文件不得发布。

### 2.6 Audit artifact 合同

`audit/execution_report.md` 是唯一 Run-local 审计报告。它由独立 audit controller 创建，并采用三轴状态，避免把正文前阻断误写成已经执行：

| 状态轴 | 允许值 | 说明 |
| --- | --- | --- |
| `last_gate_result` | `PASS` 或明确 `BLOCKED_* / NOT_AUTHORIZED` | 正文前阻断记录在这里 |
| `execution_status` | `not_started / running / completed / failed / cancelled / invalidated` | G2 未通过时必须为 `not_started` |
| `run_disposition` | `closed_completed / closed_never_authorized / closed_precontent_blocked / closed_failed / closed_cancelled / closed_invalidated` | 所有关闭态均不可复用 |

因此，`BLOCKED_BEFORE_CONTENT_READ` 必须表现为 `last_gate_result`，同时 `execution_status: not_started`；不能把它混入已执行后的结果枚举。

报告至少记录：

1. Run ID；authorization 存在时记录 authorization ID 与完整文件 checksum，不存在时记录 `authorization_absent: true` 与闭合原因；
2. B-overlay、repair contract、source snapshot、Map、task scope、execution snapshot 与 output contract 的绑定 identity；
3. 每项启动 Gate 的 `pass / fail`、证据引用与 blocker code；
4. broker、reader、audit authority、sandbox 与 formal loader 的实际版本／digest；
5. audit subsystem 已启动时，记录允许 range、actual read calls、actual union、slice size/hash、越界字节数、`scope_execution_attestation` 与 `closure_audit_attestation` identities；
6. Candidate direct source access、Greek raw access、Book 2–24 content event 与范围外模型输入计数；
7. `story_structure.yaml` 的存在状态、完整文件 checksum 或明确的 absent reason；
8. 人物、事件、主题、改编、剧本、normalized、alignment 与 formal output 的禁止项检查；
9. 三轴最终状态、外部 authorization consumption event（若存在）及该 Run 是否已永久关闭。

报告禁止：

- 来源正文、摘录、摘要或 literary interpretation；
- 自由文本形式的模型输入／输出转储；
- authorization secret、raw path capability 或可重放 token；
- 将 `completed` 描述为 formal approval 或可晋级结论。

独立 audit 的原始证据可以保存在 Candidate 无写权限的 control-plane audit store 中，不作为第五个 Run-local 文件。若 audit subsystem 尚未实例化，report 必须记录 `read_audit_status: not_started`、`audit_attestation_absent: true` 与闭合原因；此时不得声称 scope proof PASS。若已经读取或执行，report 必须记录 pre-publication `scope_execution_attestation` 和 terminal `closure_audit_attestation` 的 immutable ID、完整 signed-object SHA-256、authority 与必要闭合字段。只有 report 自己宣称“范围正确”而无所需 attestation 时，Scope Gate 必须 FAIL。

### 2.7 Artifact presence matrix 与状态不变量

四个路径仍是唯一 Run-local allowlist，但不得用固定“三文件阻断态”覆盖所有失败时点。合法 presence 由状态决定：

| 状态 | authorization | execution snapshot | story structure | execution report | 外部记录 |
| --- | --- | --- | --- | --- | --- |
| 新 Plan／overlay 未通过，Run root 尚未安全初始化 | 不要求 Run-local 文件 | 不要求 | 禁止 | 不要求 Run-local report | 必须有 immutable denial record；不得创建 Run root |
| Run root 已安全初始化，但 authorization／snapshot 未闭合 | draft／denied authorization 可存在 | 可缺失或 draft | 禁止 | audit controller 能安全写入时必须存在 | denial／gate evidence 必须存在 |
| 已授权但正文前或 slice 校验阻断 | 必须存在且不可变 | 必须存在且冻结 | 禁止 | 必须存在 | consumption/read attestations 按实际情况存在 |
| 内容任务失败且业务输出未发布 | 必须存在 | 必须存在 | 禁止 | 必须存在 | read/model/write attestations 必须存在 |
| 在业务输出发布前取消 | 必须存在 | 必须存在 | 禁止 | 必须存在 | 已到达阶段的 attestations 与取消证据必须存在 |
| 技术 completed | 必须存在 | 必须存在 | 恰好一个 | 必须存在 | 完整 attestations 必须存在 |
| 发布后发现越界或隔离破坏 | 必须存在 | 必须存在 | 可以物理存在；只能由 report／外部 registry 标记为无效并禁止消费，不得回写业务文件 | 必须存在 | tamper／scope evidence 必须存在 |

```yaml
run_local_path_allowlist:
  - control/authorization.yaml
  - control/execution_snapshot.yaml
  - output/story_structure.yaml
  - audit/execution_report.md
business_output_count_max: 1
candidate_authority: non_authoritative
candidate_output_promotable: false
downstream_consumption_allowed: false
```

“允许路径缺失”只有在该状态的 matrix 把它标为必须存在时才是错误；任何额外 Run-local 文件、错误 writer 或路径逃逸始终导致阻断或 invalidation。不得为满足数量而删除审计证据、伪造 authorization、创建空业务输出，或在 Run root 尚不能安全初始化时强行写 report。

## 3. 输出合同修订

### 3.1 业务输出与审计输出不冲突

修订后的语义如下：

| 名称 | 路径 | 角色 | 允许承载的内容 | 是否受“唯一业务输出”约束 |
| --- | --- | --- | --- | --- |
| 业务输出 | `output/story_structure.yaml` | Candidate 内容结果 | 仅 Book 1 的非权威 story structure extraction | 是；业务输出最多且只能是这一种 |
| 审计输出 | `audit/execution_report.md` | 独立控制与范围证明 | 输入／组件 identity、Gate、read audit、禁止项与最终状态 | 否；它不是文学或业务内容输出 |

两者不冲突，因为它们具有不同的：

- artifact class；
- writer authority；
- 生成时点；
- schema；
- 内容边界；
- loader 可见性；
- 成功／失败时的存在规则。

`story_structure.yaml` 可以因 blocked／failed 而不存在；在 Run root 已安全初始化时，`execution_report.md` 必须如实记录这种不存在。若阻断发生在 root 可安全初始化之前，则由外部 immutable denial record 保留事实，不得为写 report 而越过失败的 isolation Gate。不得为了让报告存在而创建空的、占位的或伪成功的 `story_structure.yaml`。

### 3.2 Run-specific variance 的修订

未来新 Run 必须显式批准以下两项 variance；Run 002 的 `proposed_pending_explicit_plan_approval` 不可继承：

| Variance | 通用 workflow 默认 | 未来新 Run 修订 | 安全补偿 |
| --- | --- | --- | --- |
| `OUTPUT_FILENAME_CONTRACT_VARIANCE_V2` | Candidate 业务输出文件名以 `candidate__` 开头 | 固定使用 `output/story_structure.yaml` | Candidate-only 根、文件内强制 identity、formal loader 硬排除、downstream false |
| `CONTROL_ARTIFACT_SET_VARIANCE_V2` | manifest、source/task snapshots、evaluation、logs、review 等多文件集合 | 使用关闭式四工件布局；source/task/output blocks 嵌入 authorization，方法 identity 独立保存在 execution snapshot | authorization 充当唯一 control manifest；audit report 绑定所有 digest；禁止未登记文件 |

这两项 variance：

- 只适用于未来明确列出它们的新 Run；
- 必须在新 Run authorization artifact 中逐项写为 `approved`；
- 不修改通用 workflow 的默认规则；
- 不授权 candidate 内容被 formal loader 发现；
- 不允许复制、移动、重命名或删除身份字段实现晋级；
- 任一 variance 未批准时，正确状态为 `not_authorized`。

### 3.3 生成条件

| 技术状态 | `story_structure.yaml` | `execution_report.md` | 规则 |
| --- | --- | --- | --- |
| Gate 在正文前、Run root 安全初始化后失败 | 必须不存在 | 必须存在 | report 记录 blocker，English content delivery 为 0 |
| Gate 在 Run root 安全初始化前失败 | 必须不存在 | Run-local report 不要求 | 外部 immutable denial record 记录 blocker；不得创建不安全 root |
| Broker slice 校验失败、Candidate 尚未收到内容 | 必须不存在 | 必须存在 | report 记录实际 range／hash 与失败码 |
| 内容处理失败，业务输出未通过校验 | 必须不存在 | 必须存在 | 不发布半成品；report 记录 `failed` |
| 在业务输出发布前取消 | 必须不存在 | 必须存在 | report 记录 `execution_status: cancelled`、`run_disposition: closed_cancelled` |
| 发生越界、身份漂移或隔离破坏 | 不得作为有效输出；若已发布则 Run invalidated | 必须存在 | report 指明污染／越界与永久关闭 |
| 全部 Gate、执行与输出校验通过 | 恰好一个 | 必须存在 | 只可记为 Candidate 技术 `completed` |

### 3.4 不可晋级与 formal 隔离

无论技术状态如何，两个 Run-local 输出都必须满足：

```yaml
formal_phase_2_input: false
candidate_output_promotable: false
downstream_consumption_allowed: false
```

Formal Phase 2 可以引用 execution report 作为工程方法证据，但不得把 `story_structure.yaml` 作为正式事实、提示种子、数据库输入或缓存输入。正式内容必须在严格 Gate 闭合后使用新的 formal run ID，从重新冻结的获批来源重新运行。

## 4. Runtime Component Contract

### 4.1 共同要求

四个必需组件都必须在新 Run authorization 前具备：

- 稳定 component ID、版本、构建或代码 digest；
- 明确进程／权限边界和输入输出 schema；
- 使用无正文 fixture 的正向、拒绝与失效测试；
- 独立测试报告及其 checksum；
- fail-closed 行为；
- 无隐式 fallback、自动扩大范围或自动重试；
- 与 authorization 和 execution snapshot 中 identity 完全一致。

“已设计”“代码存在”“能手工运行”或 Candidate 自报都不能替代上述证据。

#### 4.1.1 Signed-object integrity profiles

Capability、broker response envelope 与 audit attestation 不得在自身 payload 内保存自递归 digest。三者必须使用已实现并冻结的标准签名对象：

| Profile | 对象 | Protected `typ` | 必需 `aud` |
| --- | --- | --- | --- |
| `CTDE-CAPABILITY-JWS-1` | opaque broker capability | `ctde-range-capability+jws` | 冻结的 broker component ID |
| `CTDE-BROKER-ENVELOPE-JWS-1` | broker response envelope | `ctde-broker-envelope+jws` | 冻结的 bounded-reader component ID |
| `CTDE-AUDIT-ATTESTATION-JWS-1` | scope／closure attestations | `ctde-audit-attestation+jws` | 按 attestation subtype 在 execution snapshot 中冻结的 verifier audience 集合 |

每个 profile 必须：

- 使用 compact JWS 或语义等价的标准 detached-signature 容器；
- protected header 固定 `alg`、`typ`、`kid` 与 profile version；算法和 key ID 必须在 execution snapshot 中冻结，禁止 `alg=none`、未批准算法或未知 key；
- payload 为 UTF-8 JSON，包含唯一 token／object ID、`iss`、`aud`、`iat`、`exp`、run ID、authorization file digest 与对象专属 claims；禁止把 signature 或对象自身 digest 放入 payload；
- verifier 必须检查 signature、issuer、audience、type、key status、expiry、run/auth binding 与 anti-replay state；
- 完整 signed-object bytes 的 SHA-256 由接收者计算，记录在下一层 attestation、report 或外部 registry 中，而不是写回对象本身；
- capability 必须含 `jti`／nonce／consumption event；broker envelope 必须直接绑定 authorization digest、capability ID、delivery ID 与 broker-read attestation ID/digest；audit attestation 必须直接绑定其 component attestations 和前序 attestation digest。

若实现选择非 JWS 的语义等价容器，必须另立 profile ID 并证明上述 protected header、audience、algorithm/key、canonical signed bytes 与 anti-replay 语义完全闭合；不得沿用这些 profile 名称。

### 4.2 Range broker

#### 责任

Range broker 是唯一可以绑定并打开获批 immutable/content-addressed English source object 的组件。Candidate、模型、parser、output publisher 和 audit report writer 均不得获得 raw path、完整文件描述符或通用 source read capability。

#### 请求合同

调用者只能提交由 control plane 在外部 authorization registry 完成原子消费后签发的 opaque capability：

```yaml
request:
  opaque_capability: "<signed non-replayable token>"
```

调用者不得另行提交或覆盖 run ID、source identity、offset、length、Map identity 或 expected hash。broker 只从签名 capability claims 与其绑定的 immutable authorization 中解析这些值。capability 至少绑定：

```yaml
capability_id: "<unique id>"
jti: "<same unique token id under the signed profile>"
integrity_profile: "CTDE-CAPABILITY-JWS-1"
issuer_id: "<control-plane issuer id, version, digest>"
audience: "<frozen broker component id>"
issued_at: "<ISO-8601>"
expires_at: "<ISO-8601>"
anti_replay_nonce: "<unique nonce>"
one_shot: true
consumption_event_id: "<external authorization CAS event id>"
run_id: "<new_run_id>"
authorization_file_sha256: "<sha256>"
source_object_id: "urn:sha256:dda5b206e332e56c570c1d92ea41e9a510339a454bc2ea90491788e34174a7e7"
structure_map_file_sha256: "fd0314844ee2e9c28487ea3d717d3bc75a96be4cbe0a9c74cb2defd8640d6bc3"
mapping_payload_sha256: "45740c706b615bb0f83d5b763db189bff0b87228e5814f5f16b92f46dc5faaa5"
start_byte: 4076
end_byte_exclusive: 36515
expected_length: 32439
expected_slice_sha256: "7bd8baca8c89f91c1cad6ca54c9e6e8f1eae1139d7543ef0941a88f83151ac39"
```

#### 响应合同

成功时 broker 只返回不可变内存 payload 与不可重放的 response envelope：

```yaml
delivery_id: "<unique one-shot id>"
integrity_profile: "CTDE-BROKER-ENVELOPE-JWS-1"
capability_id: "<bound capability id>"
consumption_event_id: "<bound event id>"
run_id: "<new_run_id>"
broker_id: "<id, version, digest>"
audience: "<frozen bounded-reader component id>"
authorization_file_sha256: "<bound sha256>"
start_byte: 4076
end_byte_exclusive: 36515
returned_bytes: 32439
slice_sha256: "7bd8baca8c89f91c1cad6ca54c9e6e8f1eae1139d7543ef0941a88f83151ac39"
broker_read_attestation_id: "<immutable attestation id>"
broker_read_attestation_sha256: "<sha256 over complete signed attestation bytes>"
payload_transport: "in_memory_only"
```

payload bytes 不得被序列化进 envelope、report 或 Run-local 控制文件。

#### 行为不变量

- broker 必须绑定 attested `source_object_id`，不得在运行时按普通路径重新解析到另一对象；
- 只允许 capability 绑定的 authorization 中唯一 range；调用者不能提交任意 offset／length；
- capability issuer、expiry、nonce、signature、consumption event 与 anti-replay 状态任一失败时，在 raw open 前拒绝；
- 使用 fixed-offset／fixed-length 读取；底层可有多个部分 read，但成功交付时 actual union 必须**恰好等于** `[4076,36515)`；失败／未读取时 audit 使用对应状态和实际 ranges，不能硬编码成功值；
- 不得在 Candidate Runtime 内为了 full-file SHA-256 顺序扫描全书；完整身份由运行外 attestation 提供；
- 返回前必须验证长度和 slice SHA-256；不匹配时不交付 bytes；
- 只向 bounded reader 返回不可变内存 slice、签名 response envelope 与 audit event reference；不得返回 raw path 或可复用 handle；
- 每次请求、拒绝、实际 read call 和关闭动作都写入独立 audit；
- capability 与 delivery ID 各消费一次后失效，禁止自动重试和扩大 range；authorization 已在 capability mint 前被外部 registry 标为 spent，因此任何 broker／slice 失败也永久关闭该 Run。

#### 失败码

- `BLOCKED_SOURCE_IDENTITY_UNVERIFIED`
- `BLOCKED_SOURCE_OBJECT_NOT_IMMUTABLE`
- `BLOCKED_STRUCTURE_MAP_STALE`
- `BLOCKED_RANGE_BROKER_UNAVAILABLE`
- `BLOCKED_RANGE_CAPABILITY_INVALID`
- `BLOCKED_SLICE_HASH_MISMATCH`

### 4.3 Bounded reader

#### 责任

Bounded reader 是 Candidate 侧唯一合法的正文输入接口。它不能打开文件；只能消费 broker 对本 Run 返回的一次性 Book 1 slice。

#### 行为不变量

- API 不接受 raw path、目录、glob、任意 XPath、任意 offset、EOF 标志或“读取下一卷”参数；
- 只接受与 authorization、Map、consumption event 和 expected slice hash 绑定的签名 response envelope；
- 验证 broker identity、integrity proof、capability ID、delivery ID、authorization digest、consumption event、range、length、hash 与 audit reference；任何不一致在 payload 解析前拒绝；
- delivery ID 只能消费一次，reader 不拥有再次调用 broker 或 mint capability 的权限；
- 在把 character data 交给任务前复核 range、length、slice hash、Book identity、10-card allowlist 与 fragment parse 条件；
- 只在内存中添加获批 namespace wrapper；wrapper 不写盘、不进入模型正文、不改写 slice；
- parser 必须禁用 DTD、外部实体、网络和 recovery mode；
- parser 观察到 Book 值不是唯一 `1`、Card 超出 allowlist 或 fragment 依赖不安全时立即停止；
- 禁止 XPath／regex／全文扫描／EOF fallback；
- 不提供第二次读取、自动重试或扩大范围功能。

#### PASS 证据

无正文 fixture 至少证明：精确范围通过、少一字节／多一字节拒绝、错误 hash 拒绝、错误／过期／重放 capability 拒绝、伪造 envelope 拒绝、重复 delivery ID 拒绝、第二次读取拒绝、路径输入拒绝、Book 2 locator 拒绝、DTD/entity 拒绝、parser recovery 禁止以及没有 source tree 能力。

#### 失败码

- `BLOCKED_BOUNDED_READER_UNAVAILABLE`
- `BLOCKED_BOUNDED_FRAGMENT_UNPARSABLE`
- `BLOCKED_CARD_MAPPING_INVALID`
- `BLOCKED_SCOPE_PROOF_UNAVAILABLE`
- `INVALIDATED_SCOPE_EXCEEDED`

### 4.4 Formal loader

#### 责任

Formal loader 必须使用**已批准且带完整 provenance 的 formal manifest 正向 allowlist**选择内容，并在发现层、manifest 层和下游加载层同时排除 Candidate 身份。`analysis_candidate/**` 路径 deny 是补充防线，不能作为唯一隔离依据。

#### 行为不变量

- 只有同时具备批准的 formal run ID、formal source/input provenance、formal artifact identity 和签名／完整性验证通过的 manifest entry 才可加载；
- 路径根 `analysis_candidate/**` 为硬 deny；
- 裸名 `story_structure.yaml` 位于 Candidate 根时不得被 formal discovery 发现；
- symlink、hardlink、相对路径逃逸不得绕过根路径隔离；被复制、重命名到根外或删除 Candidate 标记的文件，因为缺少批准的 formal manifest provenance，也必须拒绝；
- formal loader 不读取 Candidate 业务内容作为事实、prompt seed、cache、检索索引或数据库输入；
- formal manifest 可以引用 `execution_report.md` 的工程证据 identity，但不得把它或 `story_structure.yaml` 列为 formal content input；
- loader 的规则版本和 digest 必须冻结在 execution snapshot 中。

#### PASS 证据

负向 fixture 必须证明：Candidate 根中的 `story_structure.yaml`、`candidate__story_structure.yaml`、嵌套副本、链接、伪造 manifest reference、复制到根外的副本、重命名副本和删除 Candidate 标记的副本均返回 0 个 formal content input；只有具有完整获批 provenance 的 formal fixture 可以正常加载。

#### 失败码

- `BLOCKED_OUTPUT_ISOLATION_UNPROVEN`
- `INVALIDATED_FORMAL_DISCOVERY_LEAK`

### 4.5 Read audit

#### 责任

Read audit 必须由独立的受信 aggregator 生成，Candidate 没有创建、修改、截断或删除权限。单独的 range broker 只能证明 broker 自身的 read calls，不能独立证明 Candidate direct access、Greek access、parser events、model input 或写入行为。为避免业务输出与最终审计循环依赖，证明分为两阶段：

1. **`scope_execution_attestation`（发布前）**：绑定 broker、sandbox／syscall、parser、model gateway 四个观测域；业务输出只引用这一份已经完成的 attestation；
2. **`closure_audit_attestation`（发布后／终止时）**：绑定 scope attestation、write monitor、formal-loader 复核、业务输出 presence/checksum 与最终状态；由 report 引用，业务输出不得回写这一 ID。

两个阶段共同覆盖五个观测域的 immutable attestations：

1. broker read attestation：source object、capability、实际 read calls、union、length 与 hash；
2. sandbox／syscall attestation：Candidate direct source access、Greek open/read 与第二访问通道；
3. parser scope attestation：Book／Card/start event／character-data event；
4. model gateway attestation：进入模型的 source scope 与 forbidden-source counts；
5. write monitor attestation：raw、Map、wrapper、formal path 与 Run allowlist 的写入行为，并在 closure 阶段绑定。

Aggregator 是 scope proof 的技术事实汇总者，`execution_report.md` 只是其受控摘要与引用。

#### 发布前 scope attestation

```yaml
attestation_type: "scope_execution_attestation"
integrity_profile: "CTDE-AUDIT-ATTESTATION-JWS-1"
attestation_id: "<immutable id>"
audit_aggregator_id: "<id, version, digest>"
audience: "<frozen output validator and audit controller ids>"
run_id: "<new_run_id>"
authorization_file_sha256: "<sha256>"
consumption_event_id: "<external authorization CAS event>"
capability_id: "<id>"
delivery_id: "<id or explicit not_issued>"
scope_proof_level: "candidate_visible_bytes_and_application_exact_range"
read_state: "attempted | completed"
source_object_id: "urn:sha256:dda5b206e332e56c570c1d92ea41e9a510339a454bc2ea90491788e34174a7e7"
allowed_ranges:
  - start_byte: 4076
    end_byte_exclusive: 36515
actual_read_calls: []
actual_union_of_read_ranges: []
bytes_outside_allowed_ranges: "<integer or null when broker observation did not begin>"
slice_size_bytes: "<integer or null for attempted failure before complete slice>"
slice_sha256: "<sha256 or null for attempted failure before complete slice>"
candidate_direct_source_access_count: "<integer>"
greek_raw_open_count: "<integer>"
greek_raw_read_count: "<integer>"
greek_raw_parse_count: "<integer>"
greek_raw_copy_count: "<integer>"
greek_model_injection_count: "<integer>"
parsed_book_values: []
parsed_card_locators: []
book_2_24_start_event_count: "<integer>"
parsed_books_outside_scope: "<integer>"
character_data_events_outside_scope: "<integer>"
model_input_events_outside_scope: "<integer>"
component_attestations:
  broker_read: "<id and sha256 or explicit not_reached with reason>"
  sandbox_or_syscall: "<id and sha256>"
  parser_scope: "<id and sha256 or explicit not_reached with reason>"
  model_gateway: "<id and sha256 or explicit not_reached with reason>"
```

该完整 signed object 的 SHA-256 由 output validator 计算并写入 `story_structure.yaml`；attestation 自身不包含 self digest。

#### Terminal closure attestation

```yaml
attestation_type: "closure_audit_attestation"
integrity_profile: "CTDE-AUDIT-ATTESTATION-JWS-1"
attestation_id: "<immutable id>"
audit_aggregator_id: "<id, version, digest>"
audience: "<frozen audit controller id>"
run_id: "<new_run_id>"
authorization_file_sha256: "<sha256 or explicit absent>"
registry_observed_state: "<unconsumed | spent | revoked | expired | unavailable | unknown>"
consumption_event_id: "<id or null>"
scope_execution_attestation_id: "<id or explicit not_reached>"
scope_execution_attestation_sha256: "<sha256 or null>"
business_output_status: "absent | published | published_invalid"
business_output_sha256: "<sha256 or null>"
business_output_absent_reason: "<closed reason or null>"
write_monitor_attestation_id: "<id and sha256 or explicit not_reached>"
raw_write_count: "<integer or null when monitor not instantiated>"
structure_map_write_count: "<integer or null when monitor not instantiated>"
wrapper_persist_count: "<integer or null when monitor not instantiated>"
formal_path_write_count: "<integer or null when monitor not instantiated>"
run_local_unallowlisted_write_count: "<integer or null when monitor not instantiated>"
formal_loader_check_status: "pass | fail | not_reached"
formal_loader_attestation_id: "<id and sha256 or explicit not_reached>"
last_gate_result: "<PASS or blocker>"
execution_status: "<not_started | completed | failed | cancelled | invalidated>"
run_disposition: "<closed disposition>"
```

该完整 signed object 的 SHA-256 由 audit controller 计算并写入 report；attestation 自身不包含 self digest。

状态规则：

- audit subsystem 未实例化：不伪造 scope／closure attestation；report 或外部 denial record明确 `audit_attestation_absent`；
- scope `attempted`：允许 `delivery_id=not_issued`、slice 字段为 null、parser／model 为 `not_reached`；必须保存已经产生的真实 calls／union／failure 与原因，不得把部分 range 改写为完整成功 range，且不得发布业务输出；
- scope `completed`：actual union 必须恰好为 `[4076,36515)`、slice size/hash 匹配、parsed Book 仅 `[1]`、parsed Cards 恰为冻结的 10-card allowlist，全部 forbidden-input 计数为 0；
- closure：必须如实绑定业务输出是否存在、write/formal checks 与最终多轴状态；不能因业务文件缺失而虚构空 checksum；
- 任一 required component attestation 缺失、无法关联同一 run/auth/capability/delivery，或字段为未知而合同要求整数时，Scope Gate FAIL。

若运行环境要求证明物理设备没有 read-ahead，普通应用层 audit 不足以声称这一点；必须使用能提供该等级证明的隔离 range service，并在 authorization、execution snapshot 与 Gate 中冻结 `scope_proof_level`。未提出该物理层要求时，本合同证明的是 Candidate／parser／模型可见字节与应用层 exact-range 调用边界。

#### 失败码

- `BLOCKED_SCOPE_PROOF_UNAVAILABLE`
- `INVALIDATED_SCOPE_EXCEEDED`
- `INVALIDATED_AUDIT_TAMPERED`

### 4.6 Orchestrator 与组件组合

Orchestrator 必须按以下顺序组合组件：

1. 只读加载并复核 authorization 与 execution snapshot；
2. 确认全部 Gate 为 PASS，runtime identity 与冻结 digest 完全一致；
3. 外部 authorization registry 对 finalized authorization 执行原子 CAS：`unconsumed -> spent`，生成 `consumption_event_id`；失败则不 mint capability；
4. control plane 基于该 consumption event 签发 opaque、一次性、不可重放 capability，并交给 range broker；
5. 在 raw open 前确认 broker read、sandbox／syscall 与 write monitors 已激活；
6. broker 读取并验证唯一 Book 1 slice，生成 broker-read attestation 与签名 response envelope；
7. bounded reader 只接收签名 envelope 与 slice，完成 fragment 与 scope 检查；
8. 只有 scope check PASS 后，才把 Book 1 character data 交给 `story_structure_extraction`；
9. scope aggregator 绑定 broker、sandbox／syscall、parser 与 model gateway，生成发布前 `scope_execution_attestation`；
10. output validator 验证 schema、unit 上限、locator allowlist、身份、禁止字段与 scope attestation；
11. output publisher 只发布 `output/story_structure.yaml`；
12. 执行 formal loader 正向 allowlist／Candidate exclusion 实际复核；
13. closure aggregator 绑定 scope attestation、业务输出 checksum、write monitor 与 formal-loader 结果，生成 `closure_audit_attestation`；
14. audit controller 创建 `audit/execution_report.md`，外部 closure registry 记录 report checksum，并永久关闭 Run。

任一阶段失败都必须立即停止**内容交付、模型调用和业务发布主路径**，但不能阻断独立 terminal-audit 分支。只要 Run root 已安全初始化，terminal-audit 分支必须：

1. 停止或撤销仍可停止的 runtime capability；
2. 收集所有已到达组件的真实 attestations，对未到达组件写 `not_reached`，不得伪造 PASS；
3. 若 audit subsystem 已实例化，生成 closure attestation；尚未实例化则明确记录 absent reason；
4. 在可执行时完成 formal-loader isolation check；不可执行时记录 `not_reached` 与原因；
5. 创建 execution report、由外部 registry 记录其 checksum、seal Run root 并永久关闭 ID。

若 Run root 尚未安全初始化，则 terminal 分支只能写外部 immutable denial record，不创建不安全 root。特别是 broker／reader／audit 不可用时，不得直接把 raw path 交给 Candidate 作为降级路径。

## 5. 新 Run 启动前 Gate

### 5.1 Gate 总则

未来执行必须使用新的、未占用的 `AC-YYYYMMDD-STORYSTRUCT-NNN`。日期必须是一次性授权的真实日期。Gate 对 `fail`、`unknown`、缺失证据、摘要不可复算和占位符一律 fail closed。

Gate 分为四道不可跳过的边界：

1. **G0 Contract Activation Gate**：在创建任何 Candidate 内容进程或 broker capability 前；
2. **G1A Pre-open Gate**：包含 authorization CAS、capability mint 与 monitor activation；这些动作必须全部在 broker 打开 source object 前完成；
3. **G1B Pre-delivery Gate**：broker 仅在 monitors active 后执行 exact-range read；实际 calls、union、slice 与 broker attestation PASS 后，才能向 bounded reader 交付；
4. **G2 Candidate Task Gate**：在 Book 1 character data 进入模型／任务前。

G0 或 G1A 失败时 English content read 必须为 0。G1B 可以只在获批 broker 边界内读取 Book 1 slice；slice identity 失败时不能交付 bounded reader／Candidate。G2 失败时模型调用必须为 0。

在分配新 Run ID 之前，可以对 draft contracts 做 preparation validation；该活动不是正式 G0 attempt，不创建 Run root，也不占用 ID。一旦新 ID 已分配并开始正式 G0、创建 Run-local control artifact 或写入该 ID 的 denial/report，任何 G0 failure 都永久关闭该 ID；不得在同一 ID 下修改 draft 后重试。

### 5.2 必须 PASS 的检查

| Gate ID | 检查 | PASS 条件 | 失败结果 |
| --- | --- | --- | --- |
| `P2ER-G0-001` | Repair contract | 本文已明确批准，批准版本与 digest 固定 | `BLOCKED_REPAIR_CONTRACT_UNAPPROVED` |
| `P2ER-G0-002` | B-overlay | implementation、effective policy、批准记录与无正文测试均存在且 identity 匹配 | `BLOCKED_OVERLAY_NOT_IMPLEMENTED` |
| `P2ER-G0-003` | 新 Run Plan | 为新 ID 单独创建并批准；file／approval digest 匹配，scope、date、variances 与本文一致；Run 002 Plan 仅为历史证据 | `BLOCKED_NEW_RUN_PLAN_MISSING_OR_UNAPPROVED` |
| `P2ER-G0-004` | 新 Run ID | 未使用、日期等于真实授权日，且不是 Run 001／002 | `BLOCKED_RUN_ID_INVALID` |
| `P2ER-G0-005` | 旧 Run 隔离 | Run 002 保持 invalid/reserved；其 plan、状态和路径未被复用 | `BLOCKED_OLD_RUN_REUSE_ATTEMPT` |
| `P2ER-G0-006` | Authorization artifact | finalized schema 合法、状态 approved、one-time、未过期，外部 registry 为 unconsumed | `NOT_AUTHORIZED` |
| `P2ER-G0-007` | Canonical bindings | `CTDE-CANDIDATE-CONTRACT-C14N-1` 可独立复算；new Plan、overlay、本文、source、Map、scope、execution、output、runtime、isolation 与 approval digests 全匹配 | `NOT_AUTHORIZED` |
| `P2ER-G0-008` | Source 三轴与 snapshot | lifecycle=`acquired_verified`、formal human approval 保持 pending、analysis eligibility=`analysis_candidate_for_this_run_only`、run authority 仍由本 authorization 控制；file/language/record/Gate/capability/exception/immutable attestation 全部冻结 | `BLOCKED_SOURCE_IDENTITY_OR_ELIGIBILITY_UNVERIFIED` |
| `P2ER-G0-009` | Structure map | 预期普通文件且非 link；spec 已批准；file／payload digest、validated status、source-object attestation、Book/Card selectors、10 Paragraph spans、ambiguities=[] 与 retained notice 全匹配 | `BLOCKED_STRUCTURE_MAP_STALE` |
| `P2ER-G0-010` | Task scope | 仅 English、Book 1、唯一 range、精确 10-card allowlist、purpose、上限、stop conditions、evaluation method 与禁止项均冻结批准 | `BLOCKED_TASK_SCOPE_UNFROZEN` |
| `P2ER-G0-011` | Execution snapshot | 模型、prompt、schema、parser、wrapper、组件、sandbox、scope proof level 与参数无缺失／占位，payload/file digests 可复算 | `BLOCKED_EXECUTION_SNAPSHOT_UNFROZEN` |
| `P2ER-G0-012` | Output contract | 四路径 allowlist、artifact presence matrix、身份字段与两项 V2 variance 的独立 approval evidence 均匹配 | `BLOCKED_OUTPUT_CONTRACT_UNAPPROVED` |
| `P2ER-G0-013` | Range broker | opaque capability、anti-replay、response envelope、权限边界和正反测试 PASS | `BLOCKED_RANGE_BROKER_UNAVAILABLE` |
| `P2ER-G0-014` | Bounded reader | signed envelope、one-shot delivery、exact-range、no-path、no-EOF-fallback 测试 PASS | `BLOCKED_BOUNDED_READER_UNAVAILABLE` |
| `P2ER-G0-015` | Read audit aggregator | broker、sandbox/syscall、parser、model gateway、write monitor 五域 identities、schema、不可篡改性、success/no-read/failure fixtures 与 `scope_proof_level` 全 PASS | `BLOCKED_SCOPE_PROOF_UNAVAILABLE` |
| `P2ER-G0-016` | Candidate sandbox | source tree 不可见、generic read tool 不可用、Greek 未挂载、Candidate writable paths=[]、发布仅经 publisher | `BLOCKED_SANDBOX_ISOLATION_UNPROVEN` |
| `P2ER-G0-017` | Formal loader | signed formal-manifest 正向 allowlist、Candidate path deny、根外复制／重命名／去标记负向 fixture 均 PASS | `BLOCKED_OUTPUT_ISOLATION_UNPROVEN` |
| `P2ER-G0-018` | Run root | 新根未复用，owner／writer allowlist、状态相关 presence matrix 与四路径合同一致；不能安全初始化时只写外部 denial record | `BLOCKED_OUTPUT_ISOLATION_UNPROVEN` |
| `P2ER-G0-019` | 禁止输入 | Greek、Book 2–24、范围外 English、第二来源与第二访问通道均为 deny | `BLOCKED_FORBIDDEN_INPUT_POLICY_UNPROVEN` |
| `P2ER-G0-020` | 无正文 dry run | 同一组件组合在 synthetic fixture 上通过；source raw read 0、模型调用 0 | `BLOCKED_RUNTIME_FIXTURE_FAILED` |
| `P2ER-G1A-001` | Authorization CAS | 外部 registry 原子执行 `unconsumed -> spent` 并生成唯一 consumption event；失败时不 mint capability，不覆盖 registry observed state | `BLOCKED_AUTHORIZATION_CONSUME_FAILED` |
| `P2ER-G1A-002` | Broker capability | `CTDE-CAPABILITY-JWS-1` issuer／audience／algorithm／key／expiry／nonce／signature／anti-replay／consumption event 有效，只绑定本 Run、source object、Map 与唯一 range | `BLOCKED_RANGE_CAPABILITY_INVALID` |
| `P2ER-G1A-003` | Source object | broker 将绑定的对象与 attested object 相同且不可变；尚未执行 open/read | `BLOCKED_SOURCE_OBJECT_NOT_IMMUTABLE` |
| `P2ER-G1A-004` | Book 1 contract | 起止、长度、Book 唯一性、10 Card locators、container boundaries 与 10 Paragraph spans 均与 Map 一致；尚未读取 source | `BLOCKED_BYTE_BOUNDARY_UNRELIABLE` |
| `P2ER-G1A-005` | Monitors active | broker-read、sandbox/syscall、write monitors 与 audit correlation 已在 raw open 前激活 | `BLOCKED_SCOPE_PROOF_UNAVAILABLE` |
| `P2ER-G1B-001` | Slice verification | broker 返回 32439 bytes、成功 union 恰为 `[4076,36515)` 且 SHA-256 为冻结值 | `BLOCKED_SLICE_HASH_MISMATCH` |
| `P2ER-G1B-002` | Broker／sandbox evidence | actual calls、union、direct-access 与 Greek observability 已由对应 attestations 记录；任何 G1B failure 后 authorization 仍 spent、Run closed | `BLOCKED_SCOPE_PROOF_UNAVAILABLE` |
| `P2ER-G1B-003` | Broker envelope | `CTDE-BROKER-ENVELOPE-JWS-1` 直接绑定 authorization digest、capability、delivery 与 broker-read attestation digest；尚未交付 reader | `BLOCKED_BROKER_ENVELOPE_INVALID` |
| `P2ER-G2-001` | Response delivery | reader 验证 `CTDE-BROKER-ENVELOPE-JWS-1` signature／audience／authorization digest／broker-attestation digest；delivery ID one-shot 与 consumption event linkage PASS | `BLOCKED_BOUNDED_READER_UNAVAILABLE` |
| `P2ER-G2-002` | Fragment parse | 安全 wrapper、namespace、DTD/entity 与 non-recovery 检查 PASS | `BLOCKED_BOUNDED_FRAGMENT_UNPARSABLE` |
| `P2ER-G2-003` | Visible scope | parsed Book 仅 `[1]`，Cards 精确匹配冻结 allowlist，Book 2–24 start/content event 为 0 | `INVALIDATED_SCOPE_EXCEEDED` |
| `P2ER-G2-004` | Model input boundary | 只含获批 Book 1 character data；Greek open/read/parse/copy/model injection、Book 2–24 与 wrapper 控制文本注入均为 0 | `INVALIDATED_SCOPE_EXCEEDED` |
| `P2ER-G2-005` | Consumption proof | G2 只验证 authorization file digest、spent event、capability、delivery 与 audit linkage；不得修改 authorization file 或再次消费 | `BLOCKED_AUTHORIZATION_CONSUMPTION_LINK_INVALID` |

### 5.3 Gate 决策与允许动作

```yaml
if_any_G0_check_not_pass:
  formal_G0_attempt_started: true
  run_reusable: false
  run_disposition: "closed_never_authorized | closed_precontent_blocked"
  broker_source_read_allowed: false
  candidate_content_delivery_allowed: false
  model_invocation_allowed: false
  story_structure_output_allowed: false
  run_local_execution_report_allowed: "only_if_run_root_safely_initialized"
  external_immutable_denial_record_required: true

if_G0_pass_and_any_G1A_check_not_pass:
  registry_observed_state: "<actual unconsumed | spent | revoked | expired | unavailable | unknown>"
  cas_failure_reason: "<actual reason or null>"
  authorization_disposition: "do_not_overwrite_registry_state"
  run_reusable: false
  broker_source_read_allowed: false
  candidate_content_delivery_allowed: false
  model_invocation_allowed: false
  story_structure_output_allowed: false
  execution_report_allowed: true

if_G0_and_G1A_pass_and_any_G1B_check_not_pass:
  registry_observed_state: "spent"
  authorization_disposition: "spent"
  run_reusable: false
  candidate_content_delivery_allowed: false
  model_invocation_allowed: false
  story_structure_output_allowed: false
  execution_report_allowed: true

if_G0_G1A_G1B_pass_and_any_G2_check_not_pass:
  authorization_disposition: "spent"
  run_reusable: false
  model_invocation_allowed: false
  story_structure_output_allowed: false
  execution_report_allowed: true

if_all_G0_G1A_G1B_G2_pass:
  candidate_task_may_start: true
  max_model_invocations: 1
  automatic_retries: 0
```

`execution_report_allowed: true` 只表示独立 audit controller 可以在已经安全初始化的新 Run layout 中记录真实 blocker；它不授权 Candidate、正文读取或业务结果生成。root isolation 本身未通过时只能写外部 denial record，不能为了生成 report 创建不安全目录。

### 5.4 成功后的关闭 Gate

技术 `completed` 还必须满足：

1. actual union 恰为 `[4076,36515)`，`bytes_outside_allowed_ranges=0`；
2. Candidate direct source access、Greek raw access、Book 2–24 content/model events 全部为 0；
3. 模型调用数为 1 或合同允许的 0，自动重试为 0；
4. 发布前 `scope_execution_attestation` 完整绑定 broker、sandbox、parser、model evidence，且业务输出引用其完整 signed-object checksum；
5. `story_structure.yaml` schema、identity、unit 上限、locator allowlist 与禁止字段全部 PASS；
6. formal loader 正向 allowlist／Candidate exclusion 复核在 closure attestation 与最终 report 写入前返回 0 个 Candidate content input；
7. `closure_audit_attestation` 绑定 scope attestation、business output checksum、write monitor、formal-loader 结果和最终状态；
8. completed 状态下 Run 根文件集合恰好等于四路径 allowlist；其他状态按 presence matrix 检查；
9. report 记录 authorization、execution snapshot、business output、scope 与 closure attestation checksums；report 自身 checksum 由外部 closure registry 在文件完成后记录，避免递归 self-hash；
10. Run 被永久关闭，外部 authorization registry 保持 spent 并绑定 consumption event，不得重启。

任一项失败只能记录 `failed` 或 `invalidated`，不能记录部分成功。

## 6. 旧 Run 处理规则

### 6.1 Run 002 的最终状态语义

`AC-20260811-STORYSTRUCT-002` 必须保留其 reservation 身份和阻断事实：

```yaml
run_id: AC-20260811-STORYSTRUCT-002
reservation_status: reserved
authorization_status: not_authorized
execution_status: not_executed
last_gate_result: BLOCKED_BEFORE_CONTENT_READ
execution_identity_status: invalid_reserved
valid_for_future_execution: false
reusable: false
restartable: false
authorization_may_be_added_in_place: false
run_directory_may_be_created_after_this_repair: false
```

这里的 `reserved` 表示该 ID 已被占用并必须保留在审计历史中；`invalid_reserved` 表示它对未来执行已经失效。两者不冲突。因为 Run 002 从未取得授权或读取正文，本文不把它伪写为 `completed`、`failed_after_execution` 或 `candidate_run_authorized`。

### 6.2 不得进行的原地修复

禁止：

- 修改 Run 002 Plan 后继续使用同一 ID；
- 为 Run 002 追加或追溯一次性授权；
- 在 Run 002 根创建新的 authorization、snapshot、output 或 audit 工件；
- 把未来实现的 broker／reader／audit identity 回填成 Run 002 当时已存在；
- 将本修订文档视为 Run 002 的 variance approval；
- 创建空的 `story_structure.yaml` 或追溯 `execution_report.md`；
- 把 `BLOCKED_BEFORE_CONTENT_READ` 改写为成功或可重试状态。

### 6.3 未来新 Run 的继承关系

如项目继续执行相同有限任务，必须在所有实现与 Gate 就绪后分配新的 ID：

```yaml
run_id: AC-<actual-authorization-date>-STORYSTRUCT-<next-unused-sequence>
retry_of_run_id: AC-20260811-STORYSTRUCT-001
supersedes_run_id: AC-20260811-STORYSTRUCT-002
inherits_authorization: false
inherits_execution_snapshot: false
inherits_output_contract_approval: false
inherits_runtime_identity: false
```

新 ID 必须有一份专属的新 Run Plan；该 Plan 的 ID、完整文件 digest 与独立 approval evidence digest 必须进入 authorization binding。新 Run Plan 不属于四个 Run-local artifact，而是外部项目控制工件。`CANDIDATE_RUN_002_PLAN.md` 只能被引用为历史证据，不能成为 active plan。

新 Run 可以引用 Run 001 的 scope failure 与 Run 002 的 pre-content authorization failure 作为历史工程证据，但必须重新创建并批准 Plan、冻结全部输入、contract 和 component digests，并获得新的单次授权。

## 7. 本阶段结论与未执行动作

本文将 Candidate 执行合同修订为：

- 先实现并批准 B-overlay，再考虑单次 Run；
- 为新的、按真实授权日分配的 ID 单独创建并批准 Run Plan；
- 用 `authorization.yaml` 闭合 source、Map、scope、output、runtime 与一次性 authority；
- 用 `execution_snapshot.yaml` 冻结模型、prompt、schema、组件和 sandbox；
- 把 `story_structure.yaml` 定义为唯一业务输出；
- 把 `execution_report.md` 定义为独立审计输出，因此两者不存在文件合同冲突；
- 只有 range broker 可以访问 attested source object，bounded reader 只能消费唯一 Book 1 slice；
- read audit 独立于 Candidate，formal loader 对整个 Candidate 根硬排除；
- 所有 G0／G1／G2 条件必须逐项 PASS；
- Run 002 保持 `invalid_reserved / not_authorized / not_executed`，永久不复用。

```yaml
phase: Phase 2-E-R
task: Candidate Execution Contract Repair
document: CANDIDATE_EXECUTION_CONTRACT_REPAIR.md
document_status: ready_for_review
current_effect: repair_specification_only

associated_run_id: AC-20260811-STORYSTRUCT-002
associated_run_status: BLOCKED_BEFORE_CONTENT_READ
associated_run_execution_identity_status: invalid_reserved
associated_run_reusable: false

b_overlay_implemented_this_task: false
source_snapshot_frozen_this_task: false
candidate_authorization_created_this_task: false
runtime_components_implemented_this_task: false
runtime_components_tested_this_task: false
new_run_id_allocated_this_task: false
new_run_plan_created_this_task: false
candidate_run_authorized: false
candidate_run_executed_this_task: false

english_tei_content_read_this_task: false
greek_raw_access_count_this_task: 0
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
```

本文完成只表示执行合同修订规范已经形成。它不实现 B-overlay 或 runtime components，不冻结真实运行 snapshot，不批准任何 variance，不创建一次性授权，不分配新 Run ID，不读取正文，也不执行 Candidate 或 Formal Phase 2。
