# Classic-to-Drama Engine：Candidate Run 001 Plan

> 项目：Classic-to-Drama Engine  
> 阶段：Phase 2-B  
> 文档类型：Analysis Candidate Run 001 运行计划  
> 日期：2026-08-11  
> 文档状态：`ready_for_review`  
> 当前效力：`design_only / not_authorized / not_executed`  
> B-overlay 工作流：`ready_for_review / design_only / not_implemented`  
> Candidate 正文读取授权：否  
> Formal Phase 2 授权：否

## 0. 目的、依据与本阶段边界

本文设计 B-overlay 架构下的第一次 `analysis_candidate` 运行，唯一方法目标是验证有限 English 样本上的 `story structure extraction` 工作流。本文只定义运行身份、不可变输入快照、任务范围、预期文件、验收门槛与隔离规则，不启动运行，也不构成 Candidate 架构批准、来源批准或正文读取授权。

本文只依据：

- `ANALYSIS_CANDIDATE_WORKFLOW.md`；
- `SOURCE_GATE_ARCHITECTURE_REVIEW.md`；
- `ENGLISH_SOURCE_ANALYSIS_GATE_DECISION.md`。

本阶段不会：

- 读取或解析 English／Greek TEI 正文；
- 创建 `analysis_candidate/runs/` 或任何运行子目录；
- 修改 raw XML、SOURCE_RECORD、注册表、Gate 或其他状态文件；
- 创建 normalized、alignment、passage index 或 locator 映射；
- 执行故事结构、人物、事件、主题或改编分析；
- 创建人物、事件、主题、故事事实或短剧数据库；
- 生成短剧方案或其他改编内容。

## 1. Run ID 设计

### 1.1 四元绑定

Run 001 只有在以下四项同时冻结且获得独立批准后，才可申请一次性运行授权：

```text
analysis_candidate = source_id + source_snapshot + task_scope + run_id
```

| 绑定项 | 本计划值 | 当前状态 |
| --- | --- | --- |
| `run_id` | `AC-20260811-STORYSTRUCT-001` | `reserved / not_authorized` |
| `source_id` | `ODY-ENG-MURRAY1919` | `acquired / verified`；人工批准 `pending` |
| `source_snapshot_id` | `SS-ODY-ENG-MURRAY1919-790C8428-DDA5B206-V1` | `draft / must_freeze_before_authorization` |
| `task_scope_id` | `TS-STORYSTRUCT-BOOK01-V1` | `draft / must_approve_before_authorization` |
| `execution_snapshot_id` | `ES-STORYSTRUCT-001-V1` | `draft / must_freeze_before_authorization` |

### 1.2 `run_id` 规则

`AC-20260811-STORYSTRUCT-001` 的构成是：

| 片段 | 含义 |
| --- | --- |
| `AC` | `analysis_candidate` 命名空间 |
| `20260811` | 预定运行授权日期：2026-08-11 |
| `STORYSTRUCT` | 唯一任务 slug：story structure extraction |
| `001` | 该授权日、该任务 slug 下的三位顺序号 |

本 ID 目前只被**预留**，没有获得 `candidate_run_authorized`。激活前必须核验：

1. 2026-08-11 确实是实际授权日期；
2. 当日 `STORYSTRUCT` 命名空间中 `001` 未被其他运行占用；
3. B-overlay 工作流已独立批准并成为有效项目合同；
4. 本计划、source snapshot、task scope 与 execution snapshot 均已批准。

若实际授权日期晚于 2026-08-11，本 ID 不得带错误日期启动。它应以 `never_authorized` 保留在计划审计中，并在授权日按同一格式分配新的日期正确 ID。失败、取消、拒绝或失效的已使用 ID不得复用；任何重跑也必须分配新 ID，并使用 `retry_of_run_id` 指向本次运行。

### 1.3 Source snapshot 设计

本计划已知且不得漂移的 English 来源身份如下：

```yaml
source_snapshot_id: SS-ODY-ENG-MURRAY1919-790C8428-DDA5B206-V1
source_id: ODY-ENG-MURRAY1919
file_id: ODY-ENG-MURRAY1919-RAW-FULL-TEI
source_role_if_authorized: candidate_working_source
source_lifecycle_status: acquired / verified
human_approval_status: pending
edition: Murray 1919 / CTS perseus-eng3
translator: Augustus Taber Murray
provider: Perseus Digital Library / Scaife ATLAS
fixed_upstream_commit: 790c84289edbdbe289dd7b752bfea29f0af4299d
repository_path: data/tlg0012/tlg002/tlg0012.tlg002.perseus-eng3.xml
raw_path: source/translations/en/ody-eng-murray1919/raw/ody-eng-murray1919__raw__full.xml
sha256: dda5b206e332e56c570c1d92ea41e9a510339a454bc2ea90491788e34174a7e7
native_locator_scheme: book.card
verified_structure: 24 Books / 288 Cards
technical_verification: PASS_TECHNICAL_VERIFICATION
capabilities:
  native_locator_readable: true
  canonical_range_supported: false
  alignment_available: false
  normalization_required: false
formal_phase_2_input: false
```

以下值在本计划中仍为待冻结项；任一项缺失时不得授权正文读取：

- `file_size_bytes` 的批准证据值及启动前复核值；
- source snapshot 生成时间、合同版本、复核者与批准记录；
- `ENGLISH_SOURCE_ANALYSIS_GATE_DECISION.md` 的 Gate 快照摘要；
- Book 1 下实际存在的完整 `book.card` allowlist；
- parser、模型、prompt、schema、工具、参数与成本上限的精确版本；
- Candidate 工作流与本运行请求的有效批准记录。

冻结后的任一路径、字节数、checksum、commit、来源状态、Gate、能力或输入范围发生影响性变化时，本次授权立即失效，运行必须标记为 `invalidated`，不能在原 `run_id` 下替换快照继续运行。

### 1.4 Task scope 设计

```yaml
task_scope_id: TS-STORYSTRUCT-BOOK01-V1
primary_task: story_structure_extraction
purpose: validate_candidate_story_structure_method
input_source_id: ODY-ENG-MURRAY1919
input_role: candidate_working_source_if_authorized
native_locator_scheme: book.card
book_scope: Book 1 only
card_selection: all_existing_cards_under_allowed_book
approved_card_locators: pending_pre_authorization_freeze
max_books: 1
max_cards: 24
max_source_files: 1
max_model_invocations: 1
automatic_retries: 0
max_output_structure_units: 24
canonical_span_status: unavailable_for_candidate
formal_phase_2_input: false
```

Book 1 的 card allowlist 必须在运行授权前通过**仅结构级 locator 枚举**形成并独立批准；该步骤不得抽取、概括或分析正文。如果 Book 1 的原生 card 数量超过 `24`、任何 locator 不可唯一定位，或必须依赖 normalization／alignment 才能完成范围选择，本请求返回 `blocked_scope_requires_revision` 或 `blocked_missing_capability`，不得自动扩大范围。

## 2. 本次 Candidate 目标

### 2.1 唯一目标

Run 001 只验证以下能力：

> 能否在一个固定 English 来源快照、一个 Book 的有限原生 `book.card` 范围内，生成 schema-valid、可追溯、非权威且完全隔离的 story structure extraction 候选结果。

本次运行的成功对象是**方法与工程链路**，不是《奥德赛》的正式故事结构结论。运行即使取得 `completed`，也只证明：输入边界、结构提取 schema、provenance、隔离与验收机制按合同工作。

### 2.2 允许的候选操作

只有在本运行另获授权后，才允许：

- 只读解析批准路径下的 English TEI；
- 只读取冻结 allowlist 中 Book 1 的原生 `book.card` 内容；
- 将获批范围组织为候选 `book_outline / sequence / beat` 结构单元；
- 为每个候选结构单元登记 English `book.card` 来源跨度、顺序、置信度与不确定性；
- 生成 schema、运行指标、自动验收与方法评审证据。

### 2.3 明确排除的任务

本次 scope 不包括：

- Book 2–24 或 Book 1 allowlist 之外的任何正文；
- 人物识别、人物关系或人物数据库；
- 事件抽取、事件时间线或事件数据库；
- 主题、母题、象征或主题数据库；
- Greek 正文读取、Greek `book.line` 引用或 Greek locator 修复；
- English–Greek alignment、canonical line 映射或跨版本比较；
- normalization、清洗、排序、补缺、passage indexing 或来源重写；
- story facts 正式化、下游数据库写入或任何短剧／改编输出；
- 第二次模型调用、自动重试或在原 ID 下扩大任务范围。

任何新增分析类型、Book、card、来源、模型、prompt、schema、parser 或关键参数都需要新的请求与新的 `run_id`。

## 3. 输入范围

### 3.1 使用的唯一正文输入

| 项目 | 设计值 |
| --- | --- |
| 来源 | English TEI |
| `source_id` | `ODY-ENG-MURRAY1919` |
| 候选角色 | `candidate_working_source`，仅在本次请求获批后生效 |
| 文件 | `source/translations/en/ody-eng-murray1919/raw/ody-eng-murray1919__raw__full.xml` |
| 快照 | fixed commit `790c8428…299d` + SHA-256 `dda5b206…a7e7` + 待冻结 size |
| 定位体系 | 仅 English 原生 `book.card` |
| 内容范围 | Book 1 + 授权前冻结的完整 card allowlist，最多 24 cards |
| 访问模式 | raw 只读；一次运行；不复制正文到 snapshot、日志或其他输入文件 |

English 当前的 `acquired / verified` 只提供申请 Candidate 的技术基础。人工批准仍为 `pending`，它不是 formal analysis input；本计划也不会把它改写成 `approved`。

### 3.2 不使用的来源与能力

```yaml
excluded_content_sources:
  - source_id: ODY-GRC-MURRAY1919
    role: excluded / not_content_readable
    greek_raw_access_allowed: false
excluded_locator_schemes:
  - book.line
excluded_capabilities:
  - greek_text_analysis
  - english_greek_alignment
  - canonical_range_mapping
  - normalization
  - passage_index_generation
```

Greek raw 不得被打开、解析、复制、摘要或注入模型上下文。Greek 的来源身份、Gate 与 exception 元数据也不属于模型正文输入；仅可由 Orchestrator 在访问审计中用于证明其处于 denylist。Run 001 不得声明、推断或生成 Greek `book.line`，也不得把 English `book.card` 冒充 canonical locator。

### 3.3 启动前停止条件

以下任一情况成立时，运行保持 `not_authorized` 或返回阻断，不得读取正文：

- B-overlay 工作流或本运行计划没有有效批准记录；
- `run_id` 日期／序号不符合实际授权事实；
- English path、commit、size、SHA-256、身份或技术验证与冻结快照不一致；
- Book 1 card allowlist 尚未精确冻结，包含不存在／重复 locator，或数量超过 24；
- English 当前能力不足以用原生 `book.card` 完成任务；
- 方法依赖 Greek、`book.line`、alignment、normalization 或 passage index；
- execution snapshot 中任一模型、prompt、schema、parser、工具、参数或成本字段未冻结；
- candidate 输出根与正式 Analysis Layer 未被证明隔离；
- 不能保证 source 路径只读或 Greek raw 为不可访问。

## 4. 输出文件规划

### 4.1 唯一规划根目录

若且仅若 Run 001 未来获得授权，其全部运行文件规划于：

```text
analysis_candidate/runs/AC-20260811-STORYSTRUCT-001/
```

本文不创建该目录。若实际授权日导致 `run_id` 改变，所有下列路径必须同步使用新的、日期正确的 ID，不能保留旧 ID 路径运行。

### 4.2 文件清单与字段合同

| 规划文件 | 主要字段／内容 | 作用与约束 |
| --- | --- | --- |
| `run_manifest.yaml` | `artifact_class`、`authority`、`run_id`、snapshot/scope/execution ID、三轴状态、授权引用、技术结果、文件清单、每文件 size/SHA-256、起止时间、失效原因 | 唯一入口清单；不得登记为 formal manifest；自身 inventory 项使用 `sha256: null / reason: self_reference`，其余文件必须实填摘要 |
| `input/source_snapshot.yaml` | Section 1.3 的完整来源身份、size、commit、checksum、Gate、能力、限制、批准记录、card allowlist | 只保存身份与 locator allowlist，不复制或嵌入正文 |
| `input/task_scope.yaml` | Section 1.4 的范围、允许／禁止操作、hard caps、停止条件、输出 schema、验收阈值、批准记录 | 授权后只读；范围变化即新 run |
| `input/execution_snapshot.yaml` | model/prompt/schema/parser/tool/parameter 版本、一次调用上限、成本边界、隔离配置 | 任一关键值变化即失效或新 run |
| `output/candidate__story_structure.schema.json` | JSON Schema；受控枚举、字段类型、必填 provenance、禁止附加正式数据库字段 | 工程资产候选；包含非权威扩展元数据 |
| `output/candidate__story_structure.jsonl` | 每行一个候选结构单元，字段见 Section 4.3 | 唯一候选语义输出；不得命名为正式 `story_facts` |
| `output/candidate__run_metrics.json` | 输入/输出计数、coverage、schema 通过数、模型调用数、越界数、Greek/raw/formal 写入计数、耗时、技术结果 | 只报告候选运行技术事实 |
| `evaluation/candidate__acceptance_report.json` | 每条验收项的 `check_id`、expected、observed、result、evidence_file、blocker | 自动与人工验收汇总；不得写成 Gate S2 通过 |
| `logs/run_events.jsonl` | 封闭字段：`event_id`、timestamp、`run_id`、stage、action、status、code、可选 locator reference | schema 禁止 source text、excerpt、XML 与自由文本 payload，不得保存正文或模型内容副本 |
| `CANDIDATE_REVIEW.md` | 范围合规、方法表现、失败模式、工程资产建议、技术结论、正式阶段建议 | 只评审方法；不得批准文学事实或来源 |

### 4.3 `candidate__story_structure.jsonl` 字段

每个 JSONL 记录至少包含：

| 字段 | 类型／约束 |
| --- | --- |
| `artifact_class` | 固定 `analysis_candidate` |
| `authority` | 固定 `non_authoritative` |
| `run_id` | 固定为本次有效 `AC-...` ID |
| `source_snapshot_id` | 固定为已批准的不可变 snapshot ID |
| `task_scope_id` | 固定为已批准的 scope ID |
| `execution_snapshot_id` | 固定为已冻结的 execution snapshot ID |
| `formal_phase_2_input` | 固定 `false` |
| `candidate_output_promotable` | 固定 `false` |
| `downstream_consumption_allowed` | 固定 `false` |
| `record_id` | 本 run 内唯一且稳定，例如 `CSU-0001` |
| `source_id` | 固定 `ODY-ENG-MURRAY1919` |
| `native_locator_scheme` | 固定 `book.card` |
| `source_span` | `book`、`start_card`、`end_card`、非空 `evidence_cards[]`；全部值必须来自批准 allowlist |
| `canonical_span` | 固定 `null` |
| `canonical_span_status` | 固定 `unavailable_for_candidate`；不提供 `book.line` |
| `structure_level` | 受控值：`book_outline`、`sequence` 或 `beat` |
| `sequence_index` | 正整数；同一 parent 下严格递增 |
| `parent_record_id` | 根记录为 `null`，其他记录指向本文件已有 parent |
| `candidate_label` | 简短候选结构标签；不得伪写为 formal fact |
| `structural_function` | 受控候选结构功能；枚举由冻结 schema 定义 |
| `candidate_description` | 候选结构说明；不得复制大段来源正文 |
| `confidence` | `0.0–1.0` 数值 |
| `uncertainties` | 字符串数组；无已知不确定性时为空数组 |
| `ambiguity_codes` | 受控代码数组；无已知歧义时为空数组 |
| `method_version` | 与 execution snapshot 完全一致 |
| `generated_at` | ISO 8601 时间戳 |

schema 禁止添加结构化 `characters`、`events`、`themes`、`adaptation`、`screenplay`、Greek locator 或 formal approval 字段。未来若要增加这些字段，必须另立任务与新 `run_id`。

### 4.4 强制身份标记

每个候选输出与 `run_manifest.yaml` 都必须携带：

```yaml
artifact_class: analysis_candidate
authority: non_authoritative
run_id: AC-20260811-STORYSTRUCT-001
source_snapshot_id: SS-ODY-ENG-MURRAY1919-790C8428-DDA5B206-V1
task_scope_id: TS-STORYSTRUCT-BOOK01-V1
execution_snapshot_id: ES-STORYSTRUCT-001-V1
formal_phase_2_input: false
candidate_output_promotable: false
downstream_consumption_allowed: false
```

若格式不能内嵌这些字段，`run_manifest.yaml` 必须对该文件作一对一登记并保存 SHA-256；不能只依赖目录名表达 Candidate 身份。

## 5. 验收标准

### 5.1 可启动门槛

Run 001 只有在以下条件全部形成证据后才可启动：

1. B-overlay 工作流已独立批准并写入有效合同；
2. 本计划获得只针对该 `run_id` 的审查批准；
3. source snapshot、task scope、execution snapshot 与 output contract 无待填字段；
4. English raw path、size、commit、SHA-256、身份、24 Books／288 Cards 与 `book.card` 能力在启动前复核一致；
5. Book 1 的精确 card allowlist 已冻结，数量为 `1–24` 且每项唯一可定位；
6. English 仅取得本任务的 `analysis_candidate` 资格，没有被改写为 `approved` 或 formal input；
7. `candidate_run_authorized` 明确绑定本 ID、snapshot、scope 与一次运行；
8. source/formal 路径只读，Candidate 根可写，Greek raw 在进程权限与输入清单中均被拒绝；
9. Orchestrator 验证所有 checksum、Gate snapshot、hard caps 与停止条件仍有效；
10. 授权记录显式包含 `formal_phase_2_input: false`、`candidate_output_promotable: false` 和 `downstream_consumption_allowed: false`。

任一门槛失败时，正确结果是 `not_authorized`、`blocked` 或 `rejected`，不是“部分运行”。

### 5.2 Candidate Run 001 技术成功标准

只有下列全部通过时，`run_manifest.yaml` 才可记录技术结果 `completed`：

| 验收项 | 成功阈值 |
| --- | --- |
| 输入身份 | 实际 source ID、path、size、commit、SHA-256 与 snapshot 100% 一致 |
| 输入范围 | 仅 1 个 English 文件、Book 1、冻结 allowlist 内 `1–24` cards；范围外读取为 0 |
| Greek 隔离 | Greek raw 打开／解析／复制／模型注入次数均为 0 |
| 任务边界 | 只生成 story structure 单元；人物、事件、主题、改编与正式 story facts 文件数均为 0 |
| 调用边界 | 模型调用恰好 1 次；自动重试 0 次 |
| 输出数量 | `candidate__story_structure.jsonl` 含 `1–24` 个结构单元 |
| Schema | JSONL 解析成功率 100%；schema 通过率 100%；未知禁止字段数为 0 |
| 身份字段 | 每条记录与每个候选输出的强制身份标记完整率 100% |
| Locator | 所有 `source_span` 与 `evidence_cards` 均在批准 allowlist；Greek `book.line` 与虚构 canonical span 数为 0 |
| 输入覆盖 | 批准 allowlist 中每个 card 至少被一个候选单元引用；coverage = 100% |
| 结构一致性 | `record_id` 唯一；parent 引用有效且无环；同 parent 的 `sequence_index` 严格递增 |
| Provenance | 每条记录均可追溯到 run、snapshot、scope、source 与 English 原生 locator |
| Source 不可变 | raw、SOURCE_RECORD、注册表与 Gate 文件写入数为 0；启动前后批准证据摘要一致 |
| 派生限制 | normalized、alignment、passage index、cleaned、sorted、repaired 文件数为 0 |
| 路径隔离 | 所有新增运行文件都在本 run 根；Source Layer、formal Analysis Layer 和其他 candidate run 写入数为 0 |
| 日志边界 | 日志无正文副本、长文本片段或范围外模型内容 |
| 文件身份 | inventory 中除 manifest 自身外的每个文件，其 path、size 与 SHA-256 均与落盘文件一致；无指向 source/formal 的符号链接或硬链接 |
| 评审闭环 | acceptance report 全部为 `pass`；`CANDIDATE_REVIEW.md` 无未解决方法阻断项 |

### 5.3 非成功结果

- 合同内执行失败但未破坏快照／边界：`failed`；
- 获批运行在读取正文前被主动终止：`cancelled`；
- 输入、范围、执行身份、路径或禁止写入发生漂移：`invalidated`；
- 尚未取得授权：`not_authorized`，不得冒充已执行结果。

`completed` 只表示候选运行按本合同结束，不表示候选结构在文学上成为事实，不表示 English 获得人工批准，不解除 Greek `BLOCKED_STRUCTURE_VALIDATION`、Gate S1 或 formal Phase 2 Gate，也不构成 Stage 2／Gate S2 通过。

## 6. 隔离规则

### 6.1 文件系统隔离

- Candidate 进程只能写入 `analysis_candidate/runs/<effective_run_id>/`；
- English raw、整个 `source/`、正式 Analysis Layer 与其他 Candidate run 对该进程只读或不可写；
- Greek raw 不在输入挂载、文件 allowlist、prompt 构建或工具可读范围中；
- 临时文件也必须位于本 run 的隔离域，不得落入 source 或 formal 目录；
- 禁止通过复制、移动、重命名、硬链接、符号链接或状态字段修改将候选内容送入正式目录；
- 正式 Stage 2 的文件发现、manifest、索引、打包与下游加载规则必须显式排除 `analysis_candidate/`。

### 6.2 身份与消费隔离

- Candidate 内容始终为 `non_authoritative / non_promotable / downstream_consumption_allowed: false`；
- Candidate manifest 不得进入正式 source manifest、Stage 2 输出清单、故事事实、人物、事件、主题、剧情或改编数据库；
- Candidate 输出不得成为 formal run 的事实输入、prompt cache、检索库种子或已知结论；
- Candidate review 只评价方法、schema、prompt、parser、评估规则与失败模式，不批准文学事实；
- 可申请复用的只有工程资产，且必须独立评审、版本化和批准；候选内容本身不能原地晋级。

### 6.3 Formal Phase 2 交接

若未来正式 Gate 全部闭合，正式 Phase 2 必须：

1. 重新冻结获批来源与 checksum；
2. 分配新的 formal run ID，不能沿用或改名 `AC-...`；
3. 只读取 formal manifest 中列出的获批输入；
4. 从获批输入重新执行 story structure extraction；
5. 不导入、复制或继承 Run 001 的候选内容结论；
6. 另行接受正式 schema、provenance、独立检查与 Gate S2 人工裁决。

Formal manifest 最多将 Run 001 引用为“方法验证证据”，不得把其 JSONL 或候选结论列为正式输入。

## 7. 计划状态与未执行动作

```yaml
phase: Phase 2-B
task: Analysis Candidate Run 001 Design
document: CANDIDATE_RUN_001_PLAN.md
document_status: ready_for_review
current_effect: design_only
candidate_workflow_status: ready_for_review / design_only / not_implemented
candidate_architecture_approved: false

proposed_run_id: AC-20260811-STORYSTRUCT-001
run_id_status: reserved_not_authorized
source_id: ODY-ENG-MURRAY1919
source_snapshot_id: SS-ODY-ENG-MURRAY1919-790C8428-DDA5B206-V1
source_snapshot_status: draft_pending_freeze_and_approval
task_scope_id: TS-STORYSTRUCT-BOOK01-V1
task_scope_status: draft_pending_approval
execution_snapshot_id: ES-STORYSTRUCT-001-V1
execution_snapshot_status: draft_pending_freeze_and_approval
primary_task: story_structure_extraction

english_candidate_working_source_effective: false
greek_raw_in_scope: false
candidate_run_authorized: false
formal_phase_2_authorized: false
candidate_output_promotable: false
downstream_consumption_allowed: false

english_tei_content_read_this_task: false
greek_tei_content_read_this_task: false
candidate_run_directory_created_this_task: false
analysis_runs_executed_this_task: 0
source_or_status_files_modified_this_task: 0
normalized_or_alignment_files_created_this_task: 0
character_event_theme_databases_created_this_task: 0
short_drama_outputs_created_this_task: 0
```

本文完成只表示 Candidate Run 001 已形成一份可审查的运行计划。它不激活 English Candidate 资格，不授权读取任何 TEI 正文，不创建运行目录或分析产物，也不解除任何当前 Gate。
