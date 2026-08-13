# 《奥德赛》English Source Analysis Gate Decision

> 项目：Classic-to-Drama Engine  
> 阶段：Phase 1-F / P0-4-C  
> 文档类型：English Source Analysis Gate 决策记录  
> 日期：2026-08-11  
> 文档状态：`ready_for_review`  
> 当前 Gate 决策：**暂不允许进入 Phase 2 analysis**  
> English 技术资格：`passed`  
> English 人工批准：`pending`

## 0. 目的与执行边界

本文只根据现有 English 获取计划、实际获取与验证结果、统一来源记录模板和 P0 来源注册表，决定 English TEI 是否可以作为 Phase 2 analysis input，并定义未来放行条件与使用边界。

本文不执行来源批准、状态更新或任何数据处理，不授权本轮开始文学分析。本文不修改或覆盖 raw XML，不创建 normalized 文件、人物数据库、事件数据库、主题数据库、短剧内容或其他派生产物。

## 1. English Source 状态摘要

| 项目 | 当前事实 |
| --- | --- |
| `source_id` | `ODY-ENG-MURRAY1919` |
| `file_id` | `ODY-ENG-MURRAY1919-RAW-FULL-TEI` |
| title | *The Odyssey, Volumes 1–2* |
| edition | A. T. Murray 英译；William Heinemann / G. P. Putnam's Sons；1919；CTS `perseus-eng3` |
| translator | Augustus Taber Murray |
| provider | Perseus Digital Library / Scaife ATLAS；物理分发仓库为 `PerseusDL/canonical-greekLit` |
| fixed commit | `790c84289edbdbe289dd7b752bfea29f0af4299d` |
| repository path | `data/tlg0012/tlg002/tlg0012.tlg002.perseus-eng3.xml` |
| raw file | `source/translations/en/ody-eng-murray1919/raw/ody-eng-murray1919__raw__full.xml` |
| checksum | `sha256:dda5b206e332e56c570c1d92ea41e9a510339a454bc2ea90491788e34174a7e7` |
| native citation scheme | `book.card` |
| verification result | `PASS_TECHNICAL_VERIFICATION`：XML、严格 UTF-8、TEI/CTS `perseus-eng3` 身份、Murray 1919 English identity、24 Books、288 Cards 与 `book.card` 可定位性均通过 |
| source status | `acquired / verified` |
| `SOURCE_RECORD` | `status: verified / record_status: verified` |
| human approval | `pending` |
| P0 overall status | `blocked`：Greek `BLOCKED_STRUCTURE_VALIDATION` 未解除，两个 CTS metadata 尚未获取 |

`verified` 表示 English raw 已通过技术验证；它不等于人工 `approved`，也不自动构成 Phase 2 analysis 授权。

## 2. Analysis 使用决策

### 2.1 当前决策

**当前 English TEI 不允许进入 Phase 2 analysis。**

理由如下：

1. English 已达到 `acquired / verified`，具备作为 `primary_working_text` 的技术资格；
2. 独立人工批准仍为 `pending`，来源尚未达到现有合同规定的 `approved`；
3. P0 总体仍为 `blocked`，Greek `BLOCKED_STRUCTURE_VALIDATION`、两个 CTS metadata、Gate S1 与 Phase 2 入口条件均未完成；
4. P0-4-B 的技术通过只能证明 English 文件自身可用，不能单独绕过项目级 Source Gate 或启动内容分析。

因此，当前判定为：

| 决策层 | 状态 | 含义 |
| --- | --- | --- |
| English technical gate | `passed` | 文件身份、字节、XML 与 `book.card` 结构满足技术要求 |
| English approval gate | `pending` | 尚未获得独立人工批准 |
| Project Phase 2 gate | `blocked` | Greek 与其余 P0 / Gate S1 前置条件尚未闭合 |
| Formal analysis input | `no` | 当前不得被分析程序作为正式 corpus 读取 |

### 2.2 条件满足后的预定角色

第 5 节全部 Gate 条件满足后，English TEI 可以正式成为 Phase 2 的 `primary_working_text`，供分析程序以只读方式解析。English 当前技术验证不存在强制建立 normalized layer 的要求；如未来工具确实需要 normalized 表示，必须另立任务、文件、来源关系和验证记录，不能在本决策下静默生成。

## 3. 使用边界

### 3.1 Gate 未解除时允许的操作

当前只允许非内容型、只读的来源管理操作：

- 核对 `source_id`、edition、translator、provider、fixed commit、路径与 checksum；
- 复核 XML、TEI/CTS 身份、24 Books 与 `book.card` 结构验证证据；
- 审查 SOURCE_RECORD、注册表、Gate 决策和人工批准状态；
- 为后续 Phase 2 定义只读输入、派生标记与 provenance 契约。

这些操作不得提取、概括、解释或分析《奥德赛》正文。

### 3.2 Gate 解除后允许的操作

仅在第 5 节全部条件满足、且 Phase 2 另行正式启动后，允许基于 English working source 开展：

- 文本结构分析；
- 人物分析；
- 事件分析；
- 主题分析。

分析程序必须以只读方式访问 raw XML。所有输出都必须明确标记为派生数据，并至少保留：`source_id`、fixed commit、input checksum、输入文件路径、适用的 English `book.card` locator，以及生成步骤或版本标识。派生产物不得伪装成 source/raw 文件。

### 3.3 始终禁止的操作

- 修改 raw XML 的任何字节；
- 覆盖、替换或就地清洗 source 文件；
- 在 raw 路径写入分析结果或中间文件；
- 生成未明确标记来源、派生身份和处理过程的派生文本；
- 把 English `book.card` 冒充 Greek `book.line`；
- 为 English 虚构 `book.line` locator；
- 使用 English 补写、重排或修复 Greek locator 异常；
- 未经独立任务批准建立 English–Greek alignment 或 normalized layer；
- 在 Gate 解除前执行文本结构、人物、事件、主题或改编分析。

## 4. 与 Greek Source 的关系

| 来源 | 当前状态 | 项目角色 | 原生定位体系 | 当前使用权限 |
| --- | --- | --- | --- | --- |
| Greek `ODY-GRC-MURRAY1919` / `perseus-grc2` | `acquired / verification_failed` | `canonical_anchor`；reference backbone | `book.line` | `reference-only`；不得进入内容分析 |
| English `ODY-ENG-MURRAY1919` / `perseus-eng3` | `acquired / verified`；approval `pending` | `primary_working_text`；analysis working source | `book.card` | 当前不得进入 Phase 2；Gate 解除后可作为分析工作文本 |

关系规则如下：

- Greek 负责规范引用脊柱；English 负责面向 AI 的分析工作文本；
- 两者来自同一 fixed commit，只证明处于同一上游版本快照，不证明 `book.card` 与 `book.line` 已对齐；
- English 的技术通过不改变 Greek 的 `verification_failed`，也不解除 `BLOCKED_STRUCTURE_VALIDATION`；
- 未来需要 canonical citation 的分析结果必须遵守 Greek reference backbone 的已批准异常处置规则；
- English–Greek locator 映射属于独立 alignment／normalization 工作，不包含在本 Gate 决策中；
- 在 Greek 结构阻断未按批准路径解除前，English 不能凭单文件 `verified` 状态启动正式 Phase 2 analysis。

## 5. Gate 解除条件

English source 只有在以下条件**全部满足**后，才正式成为 Phase 2 analysis input：

1. **技术身份持续有效**  
   English raw 仍位于批准路径；其 SHA-256 仍为 `dda5b206e332e56c570c1d92ea41e9a510339a454bc2ea90491788e34174a7e7`；`perseus-eng3`、Murray 1919、24 Books 与 `book.card` 验证没有新增未解决阻断。

2. **完成人工批准**  
   由独立人工审查明确记录批准决定、审查日期和审查依据；不得把本文档本身或技术验证结果当作隐式批准。

3. **按现有状态合同登记批准**  
   在获得真实人工批准后，English SOURCE_RECORD 才可从 `status: verified / record_status: verified` 更新为 `approved / approved`，P0 注册表的 English `verification_status` 才可从 `verified` 更新为 `approved`。任何更新必须引用实际批准记录。

4. **项目级来源 Gate 闭合**  
   Greek reference backbone 的异常处置获得批准，`BLOCKED_STRUCTURE_VALIDATION` 按既定决策门槛解除；两个 Required CTS metadata 项完成其规定的获取与验证；Gate S1 及 Phase 2 入口条件均明确通过。English 单来源批准不能替代这些条件。

5. **只读输入与派生标记契约就绪**  
   Phase 2 执行方案明确 raw 为只读输入，明确 English `book.card` 的保留方式，并要求所有分析输出携带第 3.2 节规定的 provenance 与派生标记。

6. **Phase 2 获得独立启动授权**  
   另行批准具体分析范围、输出位置与任务边界。本 Gate 解除仅使 English 成为合格输入，不自动执行任何分析。

在上述条件闭合之前，应继续保持：

```yaml
english_acquisition_status: acquired
english_verification_status: verified
english_approval_status: pending
english_formal_analysis_input: false
phase_2_analysis_authorized: false
```

## 6. Gate 解除后的 Phase 2 交接规则

完成第 5 节后，Phase 2 启动任务应：

1. 读取已批准的 English SOURCE_RECORD、fixed commit、checksum 与本 Gate 决策；
2. 将 English raw 注册为只读 `primary_working_text`，不得复制或覆盖为另一份未登记 source；
3. 以 English 原生 `book.card` 保存工作文本定位信息；
4. 将 Greek 保持为独立 reference backbone，不在分析任务中静默建立 card-to-line 映射；
5. 把文本结构、人物、事件和主题分析输出写入明确的派生层，并携带来源与处理 provenance；
6. 如分析工具必须依赖 normalized 输入，停止直接执行，转入单独批准的 normalization 任务；该任务必须创建独立文件并保留 raw 不变。

任一 Gate 条件未满足、批准被拒绝、checksum 发生不明变化或来源身份出现冲突时，English 必须继续停留在非正式输入状态，不得以部分通过代替正式授权。

## 7. 决策状态块

```yaml
phase: Phase 1-F
task: P0-4-C
document: ENGLISH_SOURCE_ANALYSIS_GATE_DECISION.md
document_status: ready_for_review

english_source_id: ODY-ENG-MURRAY1919
english_source_role: primary_working_text
english_acquisition_status: acquired
english_verification_status: verified
english_approval_status: pending
english_technical_eligibility: passed
english_formal_analysis_input: false
current_phase_2_decision: not_authorized

greek_source_role: reference_backbone
greek_analysis_use: reference_only
greek_blocked_structure_validation_released: false
project_phase_2_gate: blocked

raw_xml_modified_this_task: false
source_files_overwritten_this_task: 0
normalized_files_created_this_task: 0
content_analysis_created_this_task: 0
character_database_created_this_task: 0
event_database_created_this_task: 0
theme_database_created_this_task: 0
short_drama_outputs_created_this_task: 0
```

本决策确认 English TEI 已具备技术分析资格，但在人工批准与项目级 Phase 2 Gate 完成前，仍不得作为正式 analysis input。本轮不执行任何文学分析或数据处理。
