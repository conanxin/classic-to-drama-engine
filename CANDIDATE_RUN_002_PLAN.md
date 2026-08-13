# Classic-to-Drama Engine：Candidate Run 002 Plan

> 项目：Classic-to-Drama Engine  
> 阶段：Phase 2-D  
> 文档类型：Analysis Candidate Run 002 运行计划  
> 日期：2026-08-11  
> 文档状态：`ready_for_review`  
> 当前效力：`design_only / not_authorized / not_executed`  
> 预留 Run ID：`AC-20260811-STORYSTRUCT-002`  
> 前序失效 Run：`AC-20260811-STORYSTRUCT-001`  
> Candidate 正文读取授权：否  
> Formal Phase 2 授权：否

## 0. 目的、依据与本阶段边界

本文设计修复 scope enforcement 后的第二次 `analysis_candidate` 运行。唯一目标是为一个未来可能获批的、仅限 English TEI Book 1 的 `story_structure_extraction` 运行，冻结新的运行身份、来源快照、validated structure map、任务范围、启动前校验、唯一输出与隔离合同。

本文只依据：

- `CANDIDATE_RUN_001_PLAN.md`；
- `ANALYSIS_CANDIDATE_WORKFLOW.md`；
- `TEXT_STRUCTURE_MAPPING_SPEC.md`；
- `book_structure_map.yaml`；
- `STRUCTURE_MAPPING_REPORT.md`。

本文不读取 English 或 Greek TEI 正文，不启动 Candidate 进程，不调用模型，不创建 Run 002 目录，也不生成 `story_structure.yaml`。本文同样不会创建人物、事件、主题、改编或剧本产物，不会修改 raw、structure map、Run 001 审计或任何 Gate／状态文件。

Run 001 的状态永久保持：

```yaml
run_id: AC-20260811-STORYSTRUCT-001
status: BLOCKED_SCOPE_ENFORCEMENT_FAILED
run_result: invalidated
reusable: false
restartable: false
```

Phase 2-C-R2 已生成并验证 structure map，但 Map 的存在与验证通过只解除“缺少可信结构边界”这一技术前置阻断；它不自动批准 English 来源、不授权 Run 002，也不解除 Formal Phase 2 Gate。

## 1. 新 Run ID

### 1.1 预留身份

```yaml
run_id: AC-20260811-STORYSTRUCT-002
run_id_status: reserved_not_authorized
run_authority: not_authorized
execution_status: not_executed
retry_of_run_id: AC-20260811-STORYSTRUCT-001
supersedes_run_content: false
formal_run_id: false
```

该 ID 与 Run 001 不同，序号 `002` 表示同一日期、同一 `STORYSTRUCT` 任务命名空间中的新候选运行。`retry_of_run_id` 只保留审计关系，不允许继承 Run 001 的授权、输入可见性、失败输出或状态。

### 1.2 ID 激活条件

`AC-20260811-STORYSTRUCT-002` 只有在实际一次性运行授权日期确为 2026-08-11 时才可被激活。若实际授权发生在其他日期：

1. 本 ID 保留为 `never_authorized`；
2. 不得修改 ID 中的日期后继续使用同一目录；
3. 必须按 `AC-YYYYMMDD-STORYSTRUCT-NNN` 分配新的、日期正确且未使用的 ID；
4. 新 ID 仍须以 `retry_of_run_id` 指向 Run 001，并重新冻结全部输入绑定。

本计划文件的创建、审查或批准均不等于 `candidate_run_authorized: true`。正文读取只能由后续明确绑定本 ID 与本计划全部输入摘要的一次性授权触发。

## 2. 输入绑定

### 2.1 不可拆分的 Run 002 绑定

Run 002 的授权对象扩展为：

```text
run_002_binding =
  run_id
  + source_id
  + source_snapshot
  + structure_map_id
  + structure_map_checksum
  + task_scope
```

任一绑定项变化、缺失或无法复核时，原授权请求失效；不得在同一 Run ID 下替换来源、Map、Book range 或 task scope 后继续运行。

| 绑定项 | 本计划冻结值 | 当前状态 |
| --- | --- | --- |
| `run_id` | `AC-20260811-STORYSTRUCT-002` | `reserved / not_authorized` |
| `source_id` | `ODY-ENG-MURRAY1919` | 唯一内容来源；仅具 Candidate 申请基础 |
| `source_snapshot_id` | `SS-ODY-ENG-MURRAY1919-790C8428-DDA5B206-V2` | `proposed / must_refreeze_before_authorization` |
| `structure_map_id` | `ODY-ENG-MURRAY1919-TEI-STRUCTURE-MAP-20260811` | Map 内状态 `validated` |
| `structure_map_file_sha256` | `fd0314844ee2e9c28487ea3d717d3bc75a96be4cbe0a9c74cb2defd8640d6bc3` | 本计划生成时与报告一致；启动前必须复算 |
| `mapping_payload_sha256` | `45740c706b615bb0f83d5b763db189bff0b87228e5814f5f16b92f46dc5faaa5` | `CTDE-MAP-C14N-1` payload identity |
| `task_scope_id` | `TS-STORYSTRUCT-BOOK01-MAPBOUND-V2` | `proposed / must_approve_before_authorization` |
| `execution_snapshot_id` | `ES-STORYSTRUCT-002-V1` | `proposed / must_freeze_before_authorization` |
| `output_contract_id` | `OC-STORYSTRUCT-YAML-BOOK01-V1` | `proposed / includes two variances / must_approve_before_authorization` |

### 2.2 Source snapshot

```yaml
source_snapshot_id: SS-ODY-ENG-MURRAY1919-790C8428-DDA5B206-V2
source_snapshot_status: proposed_pending_pre_authorization_refreeze
source_id: ODY-ENG-MURRAY1919
file_id: ODY-ENG-MURRAY1919-RAW-FULL-TEI
source_role_if_authorized: candidate_working_source
content_language: English
raw_path: source/translations/en/ody-eng-murray1919/raw/ody-eng-murray1919__raw__full.xml
fixed_upstream_commit: 790c84289edbdbe289dd7b752bfea29f0af4299d
size_bytes: 870905
sha256: dda5b206e332e56c570c1d92ea41e9a510339a454bc2ea90491788e34174a7e7
source_object_id: urn:sha256:dda5b206e332e56c570c1d92ea41e9a510339a454bc2ea90491788e34174a7e7
native_locator_scheme: book.card
source_lifecycle_status: acquired / verified
human_approval_status: pending
formal_phase_2_input: false
```

上述值来自 validated Map 与 Phase 2-C-R2 报告，不表示本计划重新读取或重新计算了 raw。正式启动前，全文件身份复核必须在 Candidate Runtime 之外完成，并由 validator／range broker 绑定同一 immutable/content-addressed `source_object_id`。Candidate 进程不得为了核对 SHA-256 而打开或顺序扫描完整 raw。

### 2.3 Structure map binding

```yaml
structure_map_file: book_structure_map.yaml
structure_map_id: ODY-ENG-MURRAY1919-TEI-STRUCTURE-MAP-20260811
structure_map_schema_version: 1.0.0
structure_map_status_required: validated
structure_map_authority: technical_mapping_only
structure_map_checksum_algorithm: sha256
structure_map_checksum_scope: complete_file_bytes
structure_map_checksum: fd0314844ee2e9c28487ea3d717d3bc75a96be4cbe0a9c74cb2defd8640d6bc3
mapping_payload_canonicalization: CTDE-MAP-C14N-1
mapping_payload_sha256: 45740c706b615bb0f83d5b763db189bff0b87228e5814f5f16b92f46dc5faaa5
specification: TEXT_STRUCTURE_MAPPING_SPEC.md
specification_sha256: 259df6ceb6464ae7eadc84bc5603f3bdd16c603f5fe5c9ba9f82e3836cfcc3eb
attestation_id: urn:sha256:63aaf1f0fa834815d0a5652051444522a84cb681412442420b6d471d78707e8c
validation_overall_result_required: pass
validation_blockers_required: []
```

`structure_map_checksum` 明确指最终 `book_structure_map.yaml` 文件字节的 SHA-256；`mapping_payload_sha256` 是删除顶层 `validation` 后按 `CTDE-MAP-C14N-1` 计算的语义 payload 摘要。两者不可互换，启动前均须匹配。

Map 保留一项 `NOTICE_CREFPATTERN_CARD_SEPARATOR_UNESCAPED` 非阻断来源 warning。Run 002 不得修改、静默修复或扩大该正则；范围选择必须继续依赖 validated Map 中已通过验证的严格 QName、路径、discriminator、数值 locator 与 byte range。

### 2.4 Task scope binding

```yaml
task_scope_id: TS-STORYSTRUCT-BOOK01-MAPBOUND-V2
primary_task: story_structure_extraction
purpose: validate_map_bounded_candidate_story_structure_method
content_source_id: ODY-ENG-MURRAY1919
structure_metadata_source: book_structure_map.yaml
selected_books: [1]
book_scope: Book 1 only
native_locator_scheme: book.card
allowed_full_element_range:
  start_byte: 4076
  end_byte_exclusive: 36515
expected_slice_size_bytes: 32439
expected_slice_sha256: 7bd8baca8c89f91c1cad6ca54c9e6e8f1eae1139d7543ef0941a88f83151ac39
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
book_element_qname: "{http://www.tei-c.org/ns/1.0}div"
book_level_discriminators:
  type: textpart
  subtype: book
  n: "1"
card_representation_kind: container
mapped_paragraph_count: 10
paragraph_spans_computable: true
max_source_files: 1
max_books: 1
max_cards: 10
max_model_invocations: 1
automatic_retries: 0
max_output_structure_units: 10
formal_phase_2_input: false
```

## 3. Scope：只允许 English TEI Book 1

### 3.1 唯一内容范围

Run 002 若未来获得一次性授权，只允许处理：

- 唯一内容来源：English TEI `ODY-ENG-MURRAY1919`；
- 唯一 Book：Book 1；
- 唯一原生 locator 集合：本计划列出的 10 个 `book.card`；
- 唯一来源字节区间：`[4076, 36515)`；
- 唯一任务：`story_structure_extraction`；
- 唯一语义输出：隔离的候选 `story_structure.yaml`。

`book_structure_map.yaml` 是结构元数据输入，不是第二个正文来源。无正文 namespace wrapper 只可在内存中为 Book 1 片段提供安全 XML 上下文，不得写盘或进入模型内容。

### 3.2 有界输入交付

Run 002 必须采用以下路径：

1. Orchestrator 在 Candidate 启动前验证 Map、attestation、source object 与 Book 1 range；
2. Candidate 进程不获得完整 raw path、文件描述符、mount 或通用文件读取工具；
3. 只有受信 range broker 可以绑定获批 `source_object_id` 并请求 exact range；
4. broker 只返回 `[4076, 36515)` 的 `32,439` bytes；
5. broker 在交付前复核 slice SHA-256 为 `7bd8baca…151ac39`；
6. Candidate parser 只接收该 Book 1 内存片段与无正文 wrapper；
7. parser 必须确认唯一可见 Book 值为 `1`，所有 Card locator 均属于冻结 allowlist；
8. 禁止以 XPath、regex、全文扫描或读取到 EOF 作为任何 fallback。

Range broker／独立 sandbox 层必须产生不可由 Candidate 改写的 read audit。Candidate 自报“只读了 Book 1”不能单独构成范围证明。

### 3.3 明确排除

Run 002 的未来授权不得包含：

- Book 2–24 或 Book 1 range 外的任何 English 字节；
- Greek raw、Greek `book.line`、English–Greek alignment 或 canonical line 推断；
- 人物识别、人物关系或人物数据库；
- 事件抽取、事件时间线或事件数据库；
- 主题、母题、象征或主题数据库；
- adaptation、短剧方案、分集、场景、对白或剧本；
- normalized、cleaned、sorted、repaired、aligned 或 passage-indexed 来源副本；
- 正式 `story_facts`、正式 Analysis Layer 写入或下游数据库导入；
- 第二次模型调用、自动重试或同 ID 下扩大范围。

任何新增 Book、Card、来源、任务类型、输出文件、模型调用、parser、prompt、schema 或关键参数都构成合同变化，必须停止本 ID，并另立计划与新 Run ID。

## 4. 启动前验证

### 4.1 校验时点

下列检查必须在以下动作之前全部通过：

- 启动 Candidate／模型进程；
- 向 Candidate 交付任何 Book 1 来源片段；
- 由 broker 交付任何 English character data；
- 创建 `story_structure.yaml`。

计划生成时已确认 Map 文件存在，Map 文件摘要与 `STRUCTURE_MAPPING_REPORT.md` 一致，Map 内 `mapping_status` 为 `validated`，Book 1 唯一且 range 已验证。这些是计划依据，不替代运行启动前的重新校验。

### 4.2 必须检查的 Map 与来源身份

| Check ID | 启动前检查 | 通过条件 | 失败结果 |
| --- | --- | --- | --- |
| `P2D-PF-001` | Map 存在 | `book_structure_map.yaml` 存在且为预期普通文件；不是替代路径、符号链接或未批准副本 | `BLOCKED_STRUCTURE_MAP_MISSING` |
| `P2D-PF-002` | Map 文件 checksum | 完整文件 SHA-256 等于 `fd0314…d6bc3` | `BLOCKED_STRUCTURE_MAP_STALE` |
| `P2D-PF-003` | Map payload identity | `CTDE-MAP-C14N-1` 复算值等于 `45740c…faaa5` | `BLOCKED_STRUCTURE_MAP_STALE` |
| `P2D-PF-004` | Map 状态 | `mapping_status=validated`、`validation.overall_result=pass`、`blockers=[]` | `BLOCKED_STRUCTURE_MAP_UNVALIDATED` |
| `P2D-PF-005` | Source binding | Map 中 source ID、object ID、path、commit、size、full SHA-256 与本计划完全一致 | `BLOCKED_SOURCE_IDENTITY_UNVERIFIED` |
| `P2D-PF-006` | Attestation binding | attestation 有效且 validator、broker 绑定同一 `source_object_id` 与 mapping payload | `BLOCKED_SOURCE_IDENTITY_UNVERIFIED` |
| `P2D-PF-007` | Book 1 唯一性 | `book_number=1` 的记录恰好 1 个，`mapping_ambiguities=[]` | `BLOCKED_BOOK_CONTAINER_AMBIGUOUS` |
| `P2D-PF-008` | Book 1 range | 完整元素范围精确为 `[4076,36515)`，size 为 `32439`，且边界位于 source size 内 | `BLOCKED_BYTE_BOUNDARY_UNRELIABLE` |
| `P2D-PF-009` | Book 1 slice | broker 返回长度为 `32439`，slice SHA-256 等于 `7bd8…151ac39` | `BLOCKED_STRUCTURE_MAP_STALE` |
| `P2D-PF-010` | Card 边界 | Card 表示固定为 `container`；10 个 locator 与 Map 的 Book 1 allowlist逐项一致且各唯一一次 | `BLOCKED_CARD_MAPPING_INVALID` |
| `P2D-PF-011` | Paragraph span | Book 1 的 10 个 Paragraph 均有确定 byte range、唯一 Book 归属与可计算 Card span；歧义为 0 | `BLOCKED_PARAGRAPH_MAPPING_INVALID` |
| `P2D-PF-012` | Fragment parse | `fragment_parse_supported=true`、DTD/entity dependencies 为空、wrapper 摘要匹配 | `BLOCKED_BOUNDED_FRAGMENT_UNPARSABLE` |
| `P2D-PF-013` | Range broker | broker 可绑定获批 source object，且 Candidate 对完整 `source/` 零访问能力 | `BLOCKED_RANGE_BROKER_UNAVAILABLE` |
| `P2D-PF-014` | Bounded reader | exact-range API 可按获批 offset／length 返回 Book 1，且无全文件／EOF fallback | `BLOCKED_BOUNDED_READER_UNAVAILABLE` |
| `P2D-PF-015` | Read audit | broker 或独立 sandbox 层可生成不可由 Candidate 改写的 exact-range audit | `BLOCKED_SCOPE_PROOF_UNAVAILABLE` |
| `P2D-PF-016` | B-overlay workflow | B-overlay 工作流已完成独立批准并成为有效项目合同；不能仍为 `design_only / not_implemented` | `not_authorized` |
| `P2D-PF-017` | Input/output contracts | source snapshot V2、task scope、execution snapshot 与 output contract 均已冻结、批准且无待填字段 | `not_authorized` |
| `P2D-PF-018` | Run identity | Run 002 ID 未使用、日期与真实授权日一致，一次性授权精确绑定本计划各摘要 | `not_authorized` |
| `P2D-PF-019` | Output isolation | Run 002 根未被复用，Candidate 只能写入该根，formal loader 明确排除 `analysis_candidate/` | `blocked_output_isolation_unproven` |
| `P2D-PF-020` | Output contract variance | Section 5.2 的两个 Run-specific 例外已随本计划获得明确批准 | `not_authorized` |

任一检查为 `fail`、`unknown`、缺少证据或无法机械复算时，Run 002 必须在正文交付前返回对应 blocker。不得降级为部分运行，不得改用 Run 001，不得在同一 ID 下换 Map 或扩大范围。

### 4.3 Scope proof 的运行证据合同

如果 Run 002 未来获批执行，最终技术验收至少必须能够证明：

```yaml
selected_books: [1]
allowed_byte_ranges:
  - start_byte: 4076
    end_byte_exclusive: 36515
actual_union_of_read_ranges:
  - start_byte: 4076
    end_byte_exclusive: 36515
bytes_outside_allowed_ranges: 0
parsed_book_values: [1]
parsed_card_locators:
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
parsed_books_outside_scope: 0
character_data_events_outside_scope: 0
candidate_direct_source_access_count: 0
greek_raw_access_count: 0
```

如果 read audit 不可用、读范围不透明、范围并非完整 Book 1 exact range、出现 Book 2–24 事件或出现任何范围外字节，Run 002 必须返回 `BLOCKED_SCOPE_PROOF_UNAVAILABLE` 或 `INVALIDATED_SCOPE_EXCEEDED`，不能记录为成功。

## 5. 唯一规划输出：`story_structure.yaml`

### 5.1 文件与位置

Run 002 唯一规划的运行输出为：

```text
analysis_candidate/runs/AC-20260811-STORYSTRUCT-002/output/story_structure.yaml
```

本文只规划该路径，不创建目录或文件。Run 002 不规划 `run_manifest.yaml`、schema、metrics、evaluation、日志、review、数据库或其他语义输出；也不得创建 `candidate__story_structure.*`、`story_facts.*` 或正式目录中的同名副本。如果未来运行基础设施要求新增任何辅助文件，必须先修改输出合同并重新审查，不能在本 ID 下静默扩展。

### 5.2 Run-specific 输出合同例外

本计划识别并显式登记两项与 `ANALYSIS_CANDIDATE_WORKFLOW.md` 早期设计的差异：

| 例外代码 | 早期设计 | 本次 Phase 2-D 明确要求 | Run 002 处理 |
| --- | --- | --- | --- |
| `OUTPUT_FILENAME_CONTRACT_VARIANCE` | Candidate 内容文件名以 `candidate__` 开头 | 唯一规划文件名为 `story_structure.yaml` | 物理文件名固定为 `output/story_structure.yaml`，通过文件内强制身份消除裸名歧义；不另建前缀别名 |
| `CONTROL_ARTIFACT_SET_VARIANCE` | 规划 manifest、snapshots、evaluation、logs 与 review 等控制工件 | 只规划 `story_structure.yaml` | 本计划不增加其他落盘文件；必要身份与 scope proof 字段并入唯一文件，授权／broker attestation 由运行外控制面提供引用 |

```yaml
output_contract_variances:
  - OUTPUT_FILENAME_CONTRACT_VARIANCE
  - CONTROL_ARTIFACT_SET_VARIANCE
variance_scope: AC-20260811-STORYSTRUCT-002_only
variance_status: proposed_pending_explicit_plan_approval
candidate_run_may_start_before_variance_approval: false
```

这些例外不修改通用 workflow，也不向未来 Run 传递。只有本计划的后续明确审批同时批准两项例外，Run 002 才可继续申请一次性运行授权；否则正确状态仍为 `not_authorized`。不得把本文件的存在视为例外已获批。

### 5.3 文件内强制身份

由于本运行只规划单一文件，`story_structure.yaml` 自身必须携带完整 Candidate 身份，至少包括：

```yaml
artifact_class: analysis_candidate
authority: non_authoritative
run_id: AC-20260811-STORYSTRUCT-002
retry_of_run_id: AC-20260811-STORYSTRUCT-001
source_snapshot_id: SS-ODY-ENG-MURRAY1919-790C8428-DDA5B206-V2
structure_map_id: ODY-ENG-MURRAY1919-TEI-STRUCTURE-MAP-20260811
structure_map_checksum: fd0314844ee2e9c28487ea3d717d3bc75a96be4cbe0a9c74cb2defd8640d6bc3
task_scope_id: TS-STORYSTRUCT-BOOK01-MAPBOUND-V2
execution_snapshot_id: ES-STORYSTRUCT-002-V1
output_contract_id: OC-STORYSTRUCT-YAML-BOOK01-V1
formal_phase_2_input: false
candidate_output_promotable: false
downstream_consumption_allowed: false
```

这些值必须固定，不能由运行结果、人工观感或后续复制操作改写为正式身份。

### 5.4 允许字段

`story_structure.yaml` 只允许以下字段组：

| 字段组 | 允许内容 | 约束 |
| --- | --- | --- |
| Candidate identity | Section 5.3 的固定身份字段 | 全部必填；值必须与本计划一致 |
| source binding | `source_id`、source snapshot SHA-256／commit／object ID | 不嵌入 raw 或正文摘录 |
| structure map binding | Map ID、file checksum、payload checksum、Book 1 range／slice hash | 只保存技术身份 |
| scope evidence | selected book、allowed range、read audit reference／摘要、越界计数、Greek access count | 必须证明仅 Book 1 |
| story structure units | 候选 unit ID、层级、顺序、父级、English `book.card` source span、候选标签／说明、结构功能、置信度、不确定性 | 仅在未来获批运行中生成；全部为非权威候选结果 |
| execution result | `completed / failed / cancelled / invalidated`、生成时间、method/execution snapshot version | 技术结果不等于正式批准 |

每个 story structure unit 的来源范围只能使用本计划冻结的 Book 1 locator allowlist；结构单元总数必须为 `1..10`，不得超过 `max_output_structure_units: 10`。`canonical_span` 必须为 `null`；不得生成 Greek `book.line`、English–Greek 对齐或虚构 canonical locator。

### 5.5 禁止字段与文件

`story_structure.yaml` 不得包含结构化人物表、人物关系、事件表、事件时间线、主题、母题、象征、改编建议、分集、场景、对白或剧本字段；不得复制大段来源正文。除该单一文件外，禁止生成：

- `characters.*`、`character_database.*`；
- `events.*`、`event_database.*`；
- `themes.*`、`motifs.*`；
- `adaptation.*`、`episodes.*`、`scenes.*`、`screenplay.*`；
- 正式 `story_facts.*` 或任何 formal Analysis Layer 产物；
- normalized、alignment 或 passage-index 文件。

## 6. Candidate 隔离与不可晋级

### 6.1 写入隔离

- Candidate 只能写入 `analysis_candidate/runs/AC-20260811-STORYSTRUCT-002/`；
- 唯一获准文件为 `output/story_structure.yaml`；
- English raw、structure map、Source Layer、正式 Analysis Layer、Run 001 和其他 Candidate run 对 Candidate 均不可写；
- Candidate 不能直接读取 `source/`，只有 range broker 可以访问获批 source object；
- Greek raw 不得挂载、打开、解析、复制或注入模型；
- 禁止用符号链接、硬链接、复制、移动、重命名或状态字段修改跨越隔离边界。

### 6.2 身份与消费隔离

Run 002 的输出始终是：

```yaml
artifact_class: analysis_candidate
authority: non_authoritative
formal_phase_2_input: false
candidate_output_promotable: false
downstream_consumption_allowed: false
```

因此：

- `story_structure.yaml` 不能自动进入正式 analysis；
- 不能被正式 manifest、loader、检索库、数据库、prompt cache 或下游阶段发现和消费；
- 不能通过删除 Candidate 标记、移动路径或重命名成为正式 story structure；
- 即使 Run 002 技术结果为 `completed`，也只表示候选方法按合同结束，不表示文学结论获批；
- Formal Phase 2 仍须在严格 Gate 闭合后分配新的 formal run ID，从重新冻结的获批来源重新运行。

## 7. Run 002 成功与停止条件

### 7.1 技术成功条件

未来只有在以下条件全部通过时，Run 002 才可记录技术结果 `completed`：

1. Section 4 的全部启动前检查通过；
2. Candidate 只收到 `[4076,36515)` 的 Book 1 slice；
3. slice size、slice SHA-256、Book 值和 10-card allowlist 全部匹配；
4. `bytes_outside_allowed_ranges=0`，Book 2–24 content event 为 0；
5. Greek raw open／read／parse／copy／模型注入次数全部为 0；
6. 唯一新增运行文件是正确路径下的 `output/story_structure.yaml`；
7. 文件内 Candidate 身份字段完整且值精确匹配；
8. 只执行 `story_structure_extraction`，人物、事件、主题、改编、剧本与正式 story facts 产物数均为 0；
9. English raw、structure map、Source Layer、Run 001 与状态文件写入数均为 0；
10. 输出保持 `non_authoritative / non_promotable / downstream_consumption_allowed: false`。

### 7.2 必须停止的情况

- 正文交付前的身份、Map、Book 1 range、broker 或授权失败：`blocked` 或 `not_authorized`；
- 获批范围外读取、输出越界、输入／执行快照漂移：`invalidated`；
- 合同内方法执行失败且未发生边界破坏：`failed`；
- 获批运行在正文交付前主动终止：`cancelled`。

任何情况下都不得把 `blocked`、`failed`、`cancelled` 或 `invalidated` 写成部分成功，也不得复用 Run 001 或在 Run 002 ID 下自动重试。

## 8. 计划状态与未执行动作

```yaml
phase: Phase 2-D
task: Candidate Run 002 Planning
document: CANDIDATE_RUN_002_PLAN.md
document_status: ready_for_review
current_effect: design_only

proposed_run_id: AC-20260811-STORYSTRUCT-002
run_id_status: reserved_not_authorized
retry_of_run_id: AC-20260811-STORYSTRUCT-001
failed_run_reused: false

source_id: ODY-ENG-MURRAY1919
source_snapshot_id: SS-ODY-ENG-MURRAY1919-790C8428-DDA5B206-V2
structure_map_id: ODY-ENG-MURRAY1919-TEI-STRUCTURE-MAP-20260811
structure_map_checksum: fd0314844ee2e9c28487ea3d717d3bc75a96be4cbe0a9c74cb2defd8640d6bc3
task_scope_id: TS-STORYSTRUCT-BOOK01-MAPBOUND-V2
execution_snapshot_id: ES-STORYSTRUCT-002-V1
output_contract_id: OC-STORYSTRUCT-YAML-BOOK01-V1
selected_books: [1]

planned_output_files:
  - analysis_candidate/runs/AC-20260811-STORYSTRUCT-002/output/story_structure.yaml
planned_output_file_count: 1
planned_output_authority: non_authoritative
planned_output_promotable: false
output_contract_variance_status: proposed_pending_explicit_plan_approval

candidate_run_authorized: false
candidate_run_directory_created_this_task: false
candidate_run_executed_this_task: false
english_tei_content_read_this_task: false
greek_raw_access_count_this_task: 0
model_invocations_this_task: 0
story_structure_output_created_this_task: false
character_database_created_this_task: false
event_database_created_this_task: false
theme_database_created_this_task: false
adaptation_or_script_outputs_created_this_task: false
source_map_or_status_files_modified_this_task: 0
formal_phase_2_authorized: false
```

本文完成只表示 Run 002 已形成一份可审查的运行计划。它不构成一次性运行授权，不读取任何正文，不创建 Candidate 目录或 `story_structure.yaml`，也不改变 English、Greek 或 Formal Phase 2 的任何状态。
