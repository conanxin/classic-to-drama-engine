# 《奥德赛》Greek Source Analysis Gate Decision

> 项目：Classic-to-Drama Engine  
> 阶段：Phase 1-E / P0-3-E  
> 决策记录 ID：`P0-GRC-ANALYSIS-GATE-001`  
> 日期：2026-08-10  
> 当前决定：`C — 仅允许作为引用与来源证据`  
> 当前阻断：`BLOCKED_STRUCTURE_VALIDATION` 保持  
> 本文授权数据处理：否

## 0. 决策目的与边界

本文只决定当前 Greek raw source 能否作为 analysis 输入，并定义未来切换到直接 raw 分析或 normalized 分析路径的条件。A、B、C 是本文的 **analysis 使用类别**，不是新的来源生命周期状态。

本文不执行下列动作：

- 不修改、重排、重编号或覆盖 raw XML；
- 不改变 raw XML 的 SHA-256；
- 不创建 normalized 文件、locator 映射、索引或转换日志；
- 不获取 English TEI、CTS metadata 或其他来源；
- 不更新 SOURCE_RECORD、P0 注册表、质量报告或执行清单；
- 不读取、提取、摘要、翻译或解释《奥德赛》正文；
- 不创建人物、剧情、事件、改编或剧本数据；
- 不解除任何 Gate 或改变现有来源状态。

## 1. 当前 Greek Source 状态摘要

### 1.1 来源身份与状态

| 项目 | 当前已证实值 |
| --- | --- |
| `source_id` | `ODY-GRC-MURRAY1919` |
| `file_id` | `ODY-GRC-MURRAY1919-RAW-FULL-TEI` |
| acquisition status | `acquired` |
| verification status | `verification_failed` |
| SOURCE_RECORD `status` | `acquired` |
| SOURCE_RECORD `record_status` | `draft` |
| 当前 block status | `BLOCKED_STRUCTURE_VALIDATION` |
| fixed commit | `790c84289edbdbe289dd7b752bfea29f0af4299d` |
| raw file | `source/original_text/grc/ody-grc-murray1919/raw/ody-grc-murray1919__raw__full.xml` |
| raw SHA-256 | `184fa4fc598f0cd9d2964b17eaabe36bd9c61d44c2eae264c4b016feacf28530` |

### 1.2 Exception status

`GREEK_TEI_VALIDATION_EXCEPTION.md` 已完成异常登记，但不构成异常豁免或 Gate 批准。三个 locator 异常仍保持 `unresolved / blocking`：

| 异常 ID | 已登记事实 | 当前分类 |
| --- | --- | --- |
| `LOCAL-STRUCTURE-B03-ORDER` | Book 3 出现 `303, 305, 304, 306` | `locator normalization issue` |
| `LOCAL-STRUCTURE-B14-ORDER` | Book 14 出现 `62, 64, 63, 65` | `locator normalization issue` |
| `LOCAL-STRUCTURE-B16-GAP` | Book 16 未见 locator `16.101` | `locator normalization issue` |

`validation rule mismatch` 仍只是流程层次的待批准次级分类，不能自行覆盖 `verification_failed`。

### 1.3 Resolution decision

`GREEK_TEI_EXCEPTION_RESOLUTION_DECISION.md` 已完成，状态为：

```yaml
decision_status: ready_for_review
execution_status: not_executed
recommended_source_strategy: A_accept_raw_with_exception
conditional_consumption_strategy: B_normalized_locator_layer_if_required
current_block_status: retained
```

其推荐是 Source Layer 采用 A、Consumption Layer 条件性采用 B；但该文档尚未获得记录在案的批准，也未执行验证合同修订、异常 disposition、复核或状态同步。因此，推荐方案目前不能等同于 analysis 放行。

## 2. Analysis 使用决策

### 2.1 当前决定：C

**当前 Greek raw source 选择 C：仅允许作为引用与来源证据，不允许作为 Phase 2 analysis 的数据输入。**

这里的“引用与来源证据”仅指：在来源清单、方法说明、Gate 审计、版本记录和引用身份中引用该文件的 `source_id`、CTS URN、edition、fixed commit、路径、SHA-256、已有 locator 体系和 exception 文档。它不授权读取或处理正文来形成分析结论。

选择 C 的直接原因是：

1. acquisition 已完成，但 verification 仍为 `verification_failed`；
2. 三项异常尚未获得批准的 disposition，质量报告仍记录 `unresolved_blockers: 3`；
3. P0-3-D 仅为 `ready_for_review / not_executed`，没有形成已执行的 Gate 豁免或验证合同；
4. 当前不存在获批的异常感知 raw locator 合同；
5. 当前也不存在经过授权、登记和验证的 normalized locator layer；
6. P0 Minimum Source Set 的其余三个文件仍为 `pending / pending`，完整 Source Package 尚未就绪。

### 2.2 A、B、C 的适用判断

| 使用类别 | 当前判断 | 何时适用 |
| --- | --- | --- |
| A：允许 raw 直接进入 analysis | **当前不允许** | 仅在 R1 路径获批、结构阻断解除、Greek 达到所需批准状态、异常感知 locator 合同已由 analysis 工具显式实现，且 Source Package／analysis 前置 Gate 全部通过后 |
| B：必须经过 normalized layer | **当前不执行；条件性要求** | 若 analysis、索引、对齐或范围查询要求单调或连续 locator 接口，则 R2 路径下必须先创建并验证独立 normalized locator layer |
| C：仅允许作为引用来源 | **当前生效** | 从本文形成起持续生效，直至 A 或 B 路径的全部适用条件有证据地完成并获批 |

### 2.3 路径切换规则

当前 C 不永久否决 A 或 B，但禁止无证据自动切换：

- **C → A：** 只能通过获批的 R1（A-only raw 层解阻）路径；不能仅凭“XML 可解析”“24 卷存在”或“exception 已登记”切换。
- **C → B：** 只能在确认下游确需严格 locator 接口后，获得独立 normalization 授权，并完成 normalized 层的生成、登记、验证与批准；本文不授权该执行。
- **A 与 B 的关系：** B 不是修复或替换 raw。即使将来 B 完成，raw 仍保留原始字节、原 SHA-256 和永久 exception，作为 provenance 与引用锚点。

## 3. 使用限制

### 3.1 当前允许的操作

在 C 类别下，只允许下列非内容型操作：

- 保存并引用 raw 的来源身份、commit、仓库路径、本地路径、文件大小和 SHA-256；
- 在来源登记、质量报告、Gate 文档和方法说明中引用 CTS URN、Murray 1919 edition、`book.line` citation scheme 及三个 exception ID；
- 对 raw 执行不改变字节的来源完整性、XML/UTF-8、TEI/CTS 身份、24 卷、locator 唯一性和 checksum 复核；
- 审查、批准或修订验证合同、locator 合同、异常 disposition 和 analysis 输入规范；
- 设计未来 R1 或 R2 的执行计划，但不得在本文阶段运行数据转换；
- 在未来输入清单草案中登记该 raw 为 provenance／citation anchor，同时明确标注 `not_analysis_ready` 和当前 block。

### 3.2 当前禁止的操作

在 `BLOCKED_STRUCTURE_VALIDATION` 解除且 analysis 前置 Gate 通过前，禁止：

- 将 raw XML 作为语义分析、人物提取、事件提取、剧情分析、主题分析、翻译、改编或剧本生成输入；
- 批量读取、切分、tokenize、索引、向量化、对齐或导出正文；
- 以 XML 文档顺序或 locator 数值顺序静默遍历正文并生成分析结果；
- 静默重排 Book 3／14 locator，或补造、复制、猜测 `16.101` 的文本；
- 创建任何 normalized、cleaned、sorted、repaired 或派生文本；
- 用 English TEI、其他版本或二手资料填补或反推 Greek 缺失 locator；
- 修改 raw XML、checksum、SOURCE_RECORD、注册表或质量报告以制造通过状态；
- 把 Greek 标为 `verified` 或 `approved`，或声称 P0、Gate S1、Source Package 或 Phase 2 已就绪；
- 获取 English TEI、CTS metadata 或任何其他来源；
- 创建人物数据库、剧情数据库、事件表、改编方案或剧本文件。

## 4. Gate 解除条件

### 4.1 当前结论

**创建本文不会解除 `BLOCKED_STRUCTURE_VALIDATION`。** 当前 Greek 状态继续保持：

```yaml
acquisition_status: acquired
verification_status: verification_failed
source_record_status: acquired
record_status: draft
block_status: BLOCKED_STRUCTURE_VALIDATION
analysis_usage_class: C_reference_only
```

`analysis_usage_class` 只描述本文的使用决定，不写入或替代现有来源状态机。

### 4.2 共同必要条件

只有下列条件全部完成并有可审计证据时，才可以解除当前结构阻断：

- [ ] P0-3-D resolution decision 获授权评审者明确批准，并记录批准人、日期、决策 ID 与选定的 R1 或 R2 路径；
- [ ] Greek 验证合同获批修订，明确分离 raw 来源完整性／身份验证与 locator 消费就绪验证；
- [ ] B03、B14、B16 三项异常分别获得明确 disposition，不再保持 `unresolved / blocking`；
- [ ] locator 合同获批，定义 XML 文档顺序、数值 locator 顺序、单点查询、范围查询、缺失 locator、异常传播及禁止补造规则；
- [ ] 对同一 raw 文件完成非内容型复核，路径、字节数、XML/UTF-8、TEI/CTS、Murray 1919、24 卷、`book.line`、locator 唯一性和 SHA-256 均与现有证据一致；
- [ ] raw SHA-256 仍为 `184fa4fc598f0cd9d2964b17eaabe36bd9c61d44c2eae264c4b016feacf28530`；若变化，停止本解阻路径并进入新来源版本流程；
- [ ] 质量报告保留原失败历史，同时引用获批决策与三项 disposition，并使 `unresolved_blockers` 有证据地归零；
- [ ] 按既有状态机重新评估 Greek；仅在复核通过后才能从 `verification_failed` 进入 `verified`，`approved` 仍需独立人工批准；
- [ ] SOURCE_RECORD、`source/metadata/sources.yaml`、P0 注册表、质量报告和执行清单完成一致的状态同步；
- [ ] 边界检查确认 raw 未修改、`16.101` 未被伪造、来源异常未被删除、English 未被用于替代 Greek 证据。

### 4.3 R1 与 R2 的附加条件

#### R1：允许未来直接使用 raw

若选择 R1，除第 4.2 节外，还必须确认 analysis 工具不依赖 locator 连续性，并验证其显式实现以下行为：

- 对 B03／B14 区分 XML 文档顺序和 locator 数值顺序；
- 请求 `16.101` 时返回明确的 `missing_in_source`，不返回邻近文本；
- 范围查询跨越缺口时保留可见告警；
- 每个 analysis 输入包携带 raw 身份、SHA-256、exception 文档和 locator 合同版本。

完成这些条件可以解除 Greek 的结构阻断，但仍不等于 Phase 2 已启动。

#### R2：未来使用 normalized locator layer

若选择 R2，第 4.2 节仍必须完成；另外，在 Phase 2 使用该来源前，还必须：

- 获得独立 normalization 执行授权；
- 为 normalized 产物分配独立 `file_id`、路径、SOURCE_RECORD 和 SHA-256；
- 固定当前 raw 路径及 SHA-256 为唯一输入身份；
- 记录转换规则、工具／版本、执行日期和完整日志；
- 建立可逆 raw↔normalized locator 映射，并保留三个 exception ID；
- 对 `16.101` 只记录 `missing_in_source`，不生成文本；
- 验证输出格式、24 卷、locator 唯一性、映射完整性、确定性复跑和 checksum；
- 对 normalized 层完成独立批准。

R2 的完成不能反向改写 raw 曾在原验证规则下失败的事实。

### 4.4 不等价的 Gate

即使 `BLOCKED_STRUCTURE_VALIDATION` 以后解除，也不自动表示：

- Greek 单来源 Gate 已获得最终 `approved`；
- English TEI 或两个 CTS metadata 已获取；
- P0 Minimum Source Set、Gate S1-C、S1-D 或总 Gate S1 已完成；
- normalized layer 已创建；
- Phase 2 analysis 已获授权。

## 5. 对后续 Phase 2 的影响

### 5.1 当前影响

Phase 2 当前保持阻断。Greek raw 只能作为 provenance／citation anchor；不得被列为 analysis corpus、人物或剧情数据源，也不得由分析程序隐式读取。

### 5.2 如果进入 raw-direct analysis（R1 / A）

进入 Phase 2 前应依次完成：

1. 批准 P0-3-D 决策、R1 路径、验证合同、三项 disposition 和异常感知 locator 合同；
2. 对未改变的 raw 完成非内容型复核，并同步 Greek 的合法状态；
3. 完成 Greek 单来源批准、其余 P0 来源获取／验证，以及 Gate S1 和项目既有 analysis 前置 Gate；
4. 验证 analysis 工具按第 4.3 节实现异常感知行为，不依赖连续 locator；
5. 冻结 analysis 输入清单，明确记录 raw `file_id`、SHA-256、exception 文档和 locator 合同版本；
6. 获得 Phase 2 独立启动授权后，才可让 analysis 直接消费 raw。

R1 下不得把异常隐藏在预处理代码中，也不得在 analysis 启动时临时重排或补行。

### 5.3 如果需要 normalized layer（R2 / B）

进入 Phase 2 前应依次完成：

1. 批准 P0-3-D 决策、R2 路径、验证合同、三项 disposition 和 normalization 规格；
2. 在独立阶段创建、登记并验证 normalized locator layer 及 raw↔normalized 映射；
3. 完成 normalized 输出 checksum、确定性复跑和独立批准；
4. 完成其余 P0 来源与 Gate S1 等 analysis 前置要求；
5. 冻结双层输入身份：normalized 文件作为 locator-sensitive analysis 输入，raw 文件作为 provenance／citation anchor；
6. 获得 Phase 2 独立启动授权后，analysis 只能使用已批准的 normalized 身份，不得使用临时或未登记副本。

### 5.4 Phase 2 启动判定

Phase 2 只能在选定路径的全部条件、完整 P0／Source Package Gate 和独立启动授权同时成立时开始。以下任一单项均不足以启动 analysis：

- exception 文档已完成；
- resolution decision 已完成但未批准／执行；
- `BLOCKED_STRUCTURE_VALIDATION` 单独解除；
- English TEI 单独获取成功；
- normalized 文件存在但未登记、验证或批准；
- Greek raw 的 XML、24 卷或 checksum 检查单独通过。

## 6. 本阶段决定与未执行动作

```yaml
current_analysis_decision: C_reference_only
raw_direct_analysis_allowed: false
normalized_layer_required_now: false
normalized_layer_conditionally_required: true
phase_2_analysis_authorized: false
block_released: false
raw_xml_modified: false
raw_checksum_changed: false
normalized_files_created: 0
english_tei_acquired: false
source_status_files_modified: 0
analysis_outputs_created: 0
character_or_plot_data_created: 0
adaptation_or_script_files_created: 0
```

## 7. 决策依据

- `P0_GREEK_SOURCE_ACQUISITION_RESULT.md`
- `source/metadata/quality/source_quality_report.md`
- `GREEK_TEI_VALIDATION_EXCEPTION.md`
- `GREEK_TEI_EXCEPTION_RESOLUTION_DECISION.md`
- `source/metadata/records/ody-grc-murray1919-raw-full-tei.source.yaml`
- `P0_SOURCE_REGISTRY.md`
- `03_SOURCE_ACQUISITION_EXECUTION_CHECKLIST.md`

本文完成只表示当前 analysis 使用类别已被明确记录为 C，并定义了未来 R1／A 与 R2／B 的证据门槛；它不构成数据处理、异常修复、状态更新、Gate 解除或 Phase 2 启动。
