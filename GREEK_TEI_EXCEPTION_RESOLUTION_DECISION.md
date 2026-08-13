# 《奥德赛》Greek TEI 异常处理决策记录

> 项目：Classic-to-Drama Engine  
> 阶段：Phase 1-E / P0-3-D  
> 决策记录 ID：`P0-GRC-EXC-RES-001`  
> 日期：2026-08-10  
> 前置状态：`P0-3-B = BLOCKED_STRUCTURE_VALIDATION`  
> 前置异常登记：`GREEK_TEI_VALIDATION_EXCEPTION.md` 已完成  
> 文档状态：`ready_for_review`  
> 决策执行状态：`not_executed`

## 0. 文档目的与边界

本文只评估 Greek TEI 三项 locator 结构异常的处置方案，提出推荐决策，并定义解除 `BLOCKED_STRUCTURE_VALIDATION` 的证据门槛。本文不构成异常修复、Gate 豁免、来源批准或 analysis 启动授权。

本阶段不执行以下动作：

- 不修改、重排、重编号或覆盖 raw XML；
- 不改变 raw XML 的 SHA-256；
- 不创建 normalized 文件、映射、索引或转换日志；
- 不获取 English TEI、CTS metadata 或其他来源；
- 不更新 `SOURCE_RECORD`、P0 注册表、质量报告或执行清单中的状态；
- 不读取、摘要、翻译或解释《奥德赛》文本内容；
- 不创建人物、剧情、事件、改编或剧本数据。

本文使用现有受控状态词汇，不新增来源生命周期状态。文中“接受异常”是异常处置结论，不是新的 `status` 或 `verification_status` 值。

## 1. 当前问题摘要

### 1.1 来源与状态身份

| 字段 | 当前已证实值 |
| --- | --- |
| `source_id` | `ODY-GRC-MURRAY1919` |
| `file_id` | `ODY-GRC-MURRAY1919-RAW-FULL-TEI` |
| repository | `https://github.com/PerseusDL/canonical-greekLit` |
| 固定 commit | `790c84289edbdbe289dd7b752bfea29f0af4299d` |
| raw file path | `source/original_text/grc/ody-grc-murray1919/raw/ody-grc-murray1919__raw__full.xml` |
| SHA-256 | `184fa4fc598f0cd9d2964b17eaabe36bd9c61d44c2eae264c4b016feacf28530` |
| acquisition status | `acquired` |
| 当前 verification status | `verification_failed` |
| SOURCE_RECORD `status` | `acquired` |
| SOURCE_RECORD `record_status` | `draft` |
| 当前阻断状态 | `BLOCKED_STRUCTURE_VALIDATION` |
| exception 文档 | `GREEK_TEI_VALIDATION_EXCEPTION.md` |
| 获取结果文档 | `P0_GREEK_SOURCE_ACQUISITION_RESULT.md` |
| 质量报告 | `source/metadata/quality/source_quality_report.md` |

### 1.2 已通过与阻断项

固定 commit、不可变获取地址、raw 文件存在性、文件字节完整性、XML/UTF-8 解析、TEI/CTS 身份、Murray 1919 版本身份、24 卷、`book.line` 可寻址性及 checksum 闭环均已通过。

当前阻断只来自以下三个已登记结构异常：

| 异常 ID | 结构事实 | 当前主分类 | 当前状态 |
| --- | --- | --- | --- |
| `LOCAL-STRUCTURE-B03-ORDER` | Book 3 出现 `303, 305, 304, 306` | `locator normalization issue` | `unresolved / blocking` |
| `LOCAL-STRUCTURE-B14-ORDER` | Book 14 出现 `62, 64, 63, 65` | `locator normalization issue` | `unresolved / blocking` |
| `LOCAL-STRUCTURE-B16-GAP` | Book 16 从 `100` 到 `102`，未见 `16.101` | `locator normalization issue` | `unresolved / blocking` |

P0-3-C 同时将 `validation rule mismatch` 认定为流程层次的待批准次级分类：现有验证规则把 raw 来源的真实性／完整性与分析消费层对 locator 单调性、连续性或排序行为的要求合并在同一硬门槛内。该分类本身不能自动覆盖失败结果。

## 2. 处理方案评估

### 2.1 评估原则

四个方案按以下原则评估：

1. **证据保真：** raw 必须继续代表从固定 commit 取得的原始字节。
2. **身份稳定：** `source_id`、版本、commit、路径和 checksum 之间的闭环不得被静默替换。
3. **层次分离：** raw 来源验证与 normalized／analysis 消费就绪必须分别判断。
4. **不得补造：** 不得凭空生成 `16.101` 的文本、复制相邻行或把未知根因写成已证实结论。
5. **可追溯：** 任何未来转换必须能从输出回到 raw locator、raw SHA-256、规则版本和异常 ID。
6. **最小变更：** 在现有来源已通过身份、完整性和基础结构验证的前提下，不因三个 locator 异常无必要地更换整个底本。

### 2.2 方案 A：接受 raw source，并永久保留 exception

#### 方案定义

继续把当前 commit-pinned Greek TEI 作为 `ODY-GRC-MURRAY1919` 的 raw 来源字节。三项异常保留在异常登记、质量证据与后续消费合同中；不修改 raw，不删除失败历史，也不把“异常存在”改写为“异常不存在”。

#### 优点

- 最大限度保存已验证的上游来源身份和原始证据；
- 不破坏已建立的 commit、路径、文件大小与 SHA-256 闭环；
- 与 Source Layer 的 raw 不可变原则完全一致；
- 三项问题均已局限为 locator 表示／消费问题，目前没有来源损坏或 XML 编码损坏证据；
- 可避免为了结构顺序问题重新选择并重新审计整套 Greek 底本。

#### 风险

- 若下游默认 locator 严格单调或连续，直接消费 raw 可能产生排序、漏取或错误范围判断；
- `16.101` 的不存在容易被错误代码当成“应自动补齐”的内容缺口；
- 若未正式修订验证合同，直接把状态改为 `verified` 会构成绕过原 Gate；
- 异常记录若未被输入清单强制引用，后续流程可能静默遗忘风险。

#### 适用条件

- 项目正式批准“raw 完整性验证”与“locator 消费就绪验证”分离；
- 三项异常均获得明确 disposition，且下游缺失／倒序行为已写入 locator 合同；
- 非内容型复核确认 raw SHA-256 和已通过检查均未回退；
- 质量报告不再含“未处置”的阻断项，而是逐项引用本决策及批准证据。

#### 对当前阻断的能力

方案 A **可以作为推荐的 raw 层解阻路径**，但只有在决策获批、原验证合同被显式修订、三项异常完成 disposition、重新验证通过并同步证据后才能解除阻断。仅创建本文不能解阻。

### 2.3 方案 B：创建独立 normalized locator layer

#### 方案定义

未来在 `source/original_text/grc/ody-grc-murray1919/normalized/` 中创建独立、可追溯的 locator 消费层。该层可以提供确定性顺序、缺失标记和 raw↔normalized 映射，但不得覆盖或回写 raw。

#### 可能解决的问题

- 为依赖单调顺序的索引、切分和对齐工具提供稳定输入；
- 明确区分 XML 文档顺序、locator 数值顺序和缺失 locator；
- 使 Book 3、Book 14 的排序规则可测试、可复现；
- 对 `16.101` 返回显式缺失状态，而不是伪造文本。

#### 风险

- normalized 顺序若设计不严谨，可能掩盖 raw 文档顺序这一原始证据；
- mapping 或转换规则错误会制造新的定位偏差；
- normalized 产物需要新的 `file_id`、记录、checksum、转换日志和验证证据，增加维护成本；
- B 不能证明 raw 本身满足原“locator 单调递增”规则，也不能自动把 raw 的失败历史删除。

#### 必要约束

若后续选择并执行 B，至少必须：

- 以当前 raw 路径和 SHA-256 作为唯一输入身份；
- 给 normalized 产物分配独立 `file_id`、路径、SOURCE_RECORD 和 SHA-256；
- 记录转换工具／版本、规则版本、执行日期及完整日志；
- 为每个 locator 保存 raw 文档位置、raw locator、normalized locator 与异常 ID 的可逆映射；
- 对 `16.101` 只记录 `missing_in_source` 或等价的获批缺失语义，不创建文本；
- 同时保留 raw 文档顺序视图和 normalized 消费顺序，不把二者混称为原始顺序；
- 独立验证 XML／输出格式、24 卷、locator 唯一性、映射完整性、确定性和 checksum。

#### 对当前阻断的能力

方案 B **适合作为条件性 downstream 方案**，但不能单独改写 raw 的验证事实。若项目拒绝修改原 raw 验证合同，B 的完成最多解除 normalized／analysis 消费阻断，不能让未改变的 raw 在原规则下突然通过。要使 B 参与 P0-3-B 解阻，仍需正式定义 raw 验证与 normalized 消费验证的边界。

### 2.4 方案 C：更换其他 Greek 版本

#### 方案定义

放弃当前文件作为默认 Greek 工作底本，改用另一固定 commit 下的 `perseus-grc2`，或改用另一 Greek edition。

#### 优点

- 若存在经完整验证、且没有这些 locator 问题的候选文件，可能获得更符合严格 locator 规则的输入；
- 可避免为现有异常设计专门的消费规则。

#### 风险与成本

- 必须重新执行版本身份、权利、固定 commit、下载、checksum、XML、TEI/CTS、24 卷和 locator 全套验证；
- 更换 commit 会影响“P0 Perseus 四个核心文件使用同一 commit”的既有合同，English 与两个 CTS 文件必须重新按同一新 commit 核验；
- 另一 commit 可能修复一处问题却引入其他未发现差异；
- 若更换 edition，则不能沿用 `ODY-GRC-MURRAY1919` 的身份，需要新的 `source_id`、路径、记录和方法学审查；
- 不得覆盖现有 raw、复用其 checksum，或把新文件伪装成同一物理资产。

#### 启用条件

只有出现以下任一情形时，才建议把 C 提升为候选主方案：

- 上游证据证明当前 raw 存在来源身份错误、传输损坏或不可接受的 TEI 编码缺陷；
- 无法形成不伪造内容且可审计的 locator 合同；
- A/B 无法满足项目必须达到的引用精度；
- 经独立对比验证的候选版本，在身份、完整性、结构和 P0 同 commit 约束上具有明确净优势。

#### 对当前阻断的能力

C 只有在新候选完成全套获取、登记、验证和批准后才可能替代当前来源并解阻；“找到另一个版本”或“换一个 commit 试试”均不构成完成。

### 2.5 方案 D：放弃该来源

#### 方案定义

不再使用 `ODY-GRC-MURRAY1919` 作为 Greek canonical anchor，也不提供替代 Greek 主来源。

#### 影响

- P0 Minimum Source Set 将缺失 primary Greek text；
- 失去既有 canonical `book.line` 锚点；
- English、中文参考本和历史资料不能替代 Greek 原文的来源权限；
- Gate S1-C、P0 Greek 单来源 Gate 和总 Gate S1 无法按现有方案完成；
- analysis 不应在没有获批 Greek canonical anchor 的情况下启动。

#### 对当前阻断的能力

D 只能终止当前来源路线，不能完成项目目标或有效解除 Source Package 阻断。除非项目范围被正式重写为“不需要 Greek primary text”，否则不推荐。

### 2.6 横向比较

| 评估维度 | A：接受 raw + exception | B：normalized locator layer | C：更换 Greek 版本 | D：放弃来源 |
| --- | --- | --- | --- | --- |
| 保持当前 raw 字节 | 是 | 是 | 是，但另增新来源 | 是，但不再使用 |
| 当前新增外部字节 | 否 | 否 | 是 | 否 |
| 当前创建派生文件 | 否 | 未来会 | 否，改为新 raw | 否 |
| 保留现有 SHA-256 闭环 | 完全保留 | 完全保留并新增派生摘要 | 保留历史，但新来源另建闭环 | 仅作历史证据 |
| 解决 raw 来源真实性问题 | 已无该类问题 | 不涉及 | 需重新验证 | 失去主来源 |
| 支持严格 locator 消费 | 需异常感知合同 | 最强 | 取决于候选版本 | 不支持 |
| 对 P0 同 commit 约束影响 | 无 | 无 | 高 | P0 无法完成 |
| 主要风险 | 下游忽略异常 | 派生规则／映射错误 | 版本漂移与重新审计 | 项目失去 Greek anchor |
| 建议等级 | **主方案** | **条件性配套方案** | 备用方案 | 不推荐 |

## 3. 推荐方案

### 3.1 推荐决策

推荐采用以下分层组合：

1. **Source Layer 选择 A：接受当前 raw source，并永久保留 exception。**
2. **Consumption Layer 条件性选择 B：只有当 normalization、索引、对齐或 analysis 确实要求单调／连续 locator 接口时，才在独立后续阶段创建 normalized locator layer。**
3. **C 仅保留为失败回退方案。** A/B 无法形成可靠、无伪造、可审计的引用体系时，才启动候选版本比较与重新获取流程。
4. **拒绝 D 作为当前项目方案。** 在现有 Source Package 目标下，放弃 Greek primary text 会使 P0 与 analysis 前置条件无法成立。

推荐的简写为：

```yaml
decision_id: P0-GRC-EXC-RES-001
decision_status: ready_for_review
recommended_source_strategy: A_accept_raw_with_exception
conditional_consumption_strategy: B_normalized_locator_layer_if_required
fallback_strategy: C_replace_only_after_independent_candidate_validation
rejected_strategy: D_abandon_without_replacement
current_block_status: retained
execution_authorized_by_this_document: false
```

### 3.2 选择理由

- 当前 raw 的来源身份、字节完整性、XML、编码、版本、24 卷和 `book.line` 可寻址能力已通过；现有证据没有支持更换或放弃整个底本的强理由。
- 三项异常都发生在 locator 顺序或覆盖范围，最适合通过异常合同与可选 normalized 消费层处理。
- A 保存证据，B 隔离派生行为；二者共同符合 `raw immutable / normalized derived_and_traceable` 的既有 Source Layer 设计。
- 该组合不要求把异常说成不存在，也不要求为通过检查而修改原始文件。
- 与 C 相比，它避免了不必要的重新下载、版本漂移和 P0 共同 commit 重审；与 D 相比，它保留 canonical Greek anchor。

### 3.3 推荐方案风险

| 风险 | 后果 | 决策层要求 |
| --- | --- | --- |
| 下游忽略异常登记 | 错序、漏取或错误范围判断 | 所有消费输入必须引用 exception 文档和获批 locator 合同 |
| 把 locator 排序误当成文本校勘 | 派生层篡改原始证据 | normalized 同时保留 raw 文档顺序与消费顺序的映射 |
| 为 `16.101` 补造内容 | 产生不存在的来源证据 | 明确禁止生成文本，只能返回缺失状态 |
| 把 A 误当作自动通过 | 绕过既有 Gate | 未完成第 4 节全部门槛前保持 `verification_failed` |
| B 的转换不确定或不可逆 | 无法审计引用来源 | 规则版本化、确定性复跑、双向映射、独立 checksum |
| English 被用来“修复”Greek | 混淆 `book.card` 与 `book.line` | English 独立验证，不能覆盖 Greek locator 事实 |

### 3.4 对 Source Layer 的影响

**本阶段即时影响：无状态、无字节、无目录变化。** 当前 raw、SOURCE_RECORD、checksum、质量报告和注册表保持原样。

若推荐方案以后获批并执行：

- raw 文件仍位于原路径且 SHA-256 不变；
- exception 文档成为该 raw 来源的永久质量证据之一；
- 质量报告需逐项记录获批 disposition，不删除原失败证据；
- 来源生命周期仍只使用 `pending / acquired / verified / approved / blocked` 等既有词汇；
- 若启用 B，normalized 产物必须作为独立文件身份登记，不能复用 raw 的 `file_id`、记录或 checksum；
- analysis 只消费明确列入冻结输入清单的 raw 或 normalized 身份，不得隐式选择。

## 4. 决策门槛

### 4.1 当前结论

创建并评审本文 **不足以** 解除 `BLOCKED_STRUCTURE_VALIDATION`。在任何批准和执行动作发生前，Greek 状态必须继续保持：

```yaml
acquisition_status: acquired
verification_status: verification_failed
source_record_status: acquired
record_status: draft
block_status: BLOCKED_STRUCTURE_VALIDATION
```

### 4.2 解除 `BLOCKED_STRUCTURE_VALIDATION` 的必要条件

只有以下条件全部满足，才可以解除当前结构阻断：

- [ ] **决策批准：** 项目负责人或获授权评审者明确批准本决策，记录批准人、日期、决策 ID 和选定路径；`ready_for_review` 本身不等于批准。
- [ ] **验证合同批准：** 明确修订 Greek 验证合同，分离 raw 来源完整性／身份验证与 locator 消费就绪验证；不得在不改合同的情况下跳过原“单调递增”硬门槛。
- [ ] **三项 disposition 完整：** B03、B14 明确为保留的 raw 文档顺序异常；B16 明确为 source 中不存在 `16.101` 的 locator 缺失，规定查询、范围和错误返回行为；不得保留 `unresolved / blocking`。
- [ ] **locator 合同获批：** 明确 XML 文档顺序与 locator 数值顺序的权限、排序策略、缺失 locator 语义、范围端点行为、异常传播方式及禁止补造规则。
- [ ] **非内容型复核通过：** 对同一 raw 文件重新验证路径、大小、XML/UTF-8、TEI/CTS、Murray 1919、24 卷、`book.line`、locator 唯一性和 checksum；已通过项不得回退。
- [ ] **raw 身份不变：** SHA-256 仍精确等于 `184fa4fc598f0cd9d2964b17eaabe36bd9c61d44c2eae264c4b016feacf28530`；若摘要变化，立即停止并进入新的来源版本流程。
- [ ] **质量证据闭环：** 质量报告逐项引用获批决策与 disposition，`unresolved_blockers` 为 0；不能删除异常或把失败历史改写成从未发生。
- [ ] **状态顺序合法：** 仅在上述技术复核完成后，才可按既有状态机把 Greek 从 `verification_failed` 重新评估为 `verified`；`approved` 仍需要后续独立人工批准。
- [ ] **状态文件一致：** SOURCE_RECORD、`source/metadata/sources.yaml`、P0 注册表、质量报告和执行清单对 Greek 的状态与同一证据一致；其他三个 P0 项保持其真实状态。
- [ ] **边界检查通过：** 没有修改 raw、伪造 `16.101`、静默重排来源、提前创建未授权 normalized 资产或用 English 替代 Greek 结构证据。

### 4.3 两条允许的解阻路径

#### R1：A-only raw 层解阻（推荐的最小路径）

当 analysis 或后续 Source 工具不要求连续 locator 视图时，可批准 A，并通过修订后的验证合同把三项异常作为已处置的已知异常保留。完成第 4.2 节的复核和状态同步后，可以解除 `BLOCKED_STRUCTURE_VALIDATION`。

R1 必须定义：

- 默认遍历是否保持 XML 文档顺序；
- 按 locator 查询时如何处理 B03/B14 的非单调文档顺序；
- 请求 `16.101` 时必须返回明确缺失，而不是邻近文本；
- 范围查询跨越缺口时如何保留缺失告警；
- exception 文档如何随每个分析输入包传播。

#### R2：A + B 消费层解阻

若 normalization、索引、对齐或 analysis 要求单调／连续接口，则先批准 A，再另行授权和执行 B。只有 normalized locator layer 的独立身份、转换日志、双向映射、缺失语义、确定性和 checksum 全部验证通过后，相关消费层阻断才能解除。

R2 不改变以下事实：raw 曾在原规则下失败，且 raw 字节未被修复。R2 仍需要第 4.2 节所述验证合同分层，不能以 normalized 文件存在为理由反向宣布 raw 本身单调连续。

### 4.4 不构成解阻的情况

以下任一项都不能解除阻断：

- 仅创建本文或仅把推荐方案写为 A/B；
- 只把异常从 `unresolved` 改名，而没有批准证据和 locator 行为合同；
- 只确认 XML 能解析、24 卷存在或 checksum 一致；这些检查已通过，但没有处置 locator 阻断；
- 在 raw 中重排 Book 3／14、补入 `16.101` 或更改 checksum；
- 只获取 English TEI 或用 English `book.card` 推断缺失 Greek `book.line`；
- 创建没有 raw↔normalized 映射的排序副本；
- 找到另一 Greek 文件但没有完成独立身份、结构、checksum 和共同 commit 验证；
- 将 Greek 标为 `verified / approved`，但质量报告仍有未处置阻断项。

### 4.5 与后续 Gate 的区别

解除 `BLOCKED_STRUCTURE_VALIDATION` 只表示 Greek locator 异常已按获批规则得到处置，不等于：

- Greek 单来源 Gate 已完成；该 Gate 仍要求来源与记录按既有流程获得 `approved`；
- P0 Minimum Source Set 已完成；English TEI 和两个 CTS metadata 仍未获取；
- Gate S1-C、Gate S1-D 或总 Gate S1 已批准；
- normalized locator layer 已创建；
- analysis phase 已获授权。

## 5. 对后续流程的影响

### 5.1 English TEI 获取

English TEI 当前继续保持 `pending / pending / checksum null`，本文不授权获取。

进入 English TEI 获取前至少需要：

- 本决策获得批准，Greek 的选定解阻路径已固定；
- 获得独立的 English acquisition 执行授权；
- 若继续采用 A/B，English 必须与 Greek 使用同一固定 commit `790c84289edbdbe289dd7b752bfea29f0af4299d`；若 C 被正式批准并更换共同 commit，则先更新并批准四个 P0 核心文件的统一 commit 合同；
- 只下载批准的 English TEI，不借机获取 CTS 或其他资产；
- 按 `perseus-eng3` 与 `book.card` 独立验证，Book/Line 明确为不适用；
- English 不得用于填补 `16.101`、重排 Greek locator 或改变 Greek verification 结论。

Greek 的结构阻断不应被 English 获取掩盖。English 可以在决策批准和独立授权后按既定顺序执行，但其成功不能替代 Greek 解阻证据。

### 5.2 Normalization

本文不创建 normalized 文件，也不授权开始 normalization。

进入 normalization 前至少需要：

- A/B 推荐决策及 locator 合同均已批准；
- 明确 normalization 是否为 analysis 的必需输入，而不是为“让 raw 看起来通过”而生成；
- 固定 raw 输入路径、`file_id` 和 SHA-256；
- 批准 normalized 文件的独立 `file_id`、目标路径、记录路径、格式和用途；
- 批准 B03、B14 的排序映射规则及 B16 的缺失语义；
- 明确禁止新增 `16.101` 文本或改写 raw；
- 定义转换日志、raw↔normalized 双向映射、checksum、确定性复跑和验证方法；
- 获得单独的 normalization 执行授权。

若下游能够安全消费异常感知的 raw，B 可以保持 `not_started`；若下游要求单调或连续 locator 视图，B 必须先完成并通过独立验证。

### 5.3 Analysis phase

当前不得进入 analysis。除现有 Source Package Gate 要求外，Greek 异常相关的最小前置条件为：

- `BLOCKED_STRUCTURE_VALIDATION` 已按第 4 节解除；
- Greek 来源与记录达到现有 Gate 要求的批准状态；
- English TEI 与两个 CTS metadata 按 P0 计划真实获取、独立验证并完成所需批准；
- 若选择 R1，analysis 工具和输入包显式实现获批的异常感知 locator 合同；
- 若选择 R2，normalized locator layer 及 raw↔normalized 映射已验证、登记、计算 checksum 并批准；
- analysis 输入清单冻结具体文件身份、checksum、exception 文档和 locator 合同版本；
- 对不存在的 locator 返回缺失，不补造、猜测、复制或用译文反推 Greek 文本；
- Gate S1 及项目既有 analysis 前置 Gate 已获得人工批准。

English 获取、normalization 完成或异常决策批准中的任意单项，都不能独立构成 analysis 启动条件。

## 6. 本阶段决定与未执行动作

### 6.1 记录的推荐

| 对象 | 本文记录 |
| --- | --- |
| raw Source Layer | 推荐 A |
| locator Consumption Layer | 条件性推荐 B |
| 备用路线 | C，仅在明确触发条件下 |
| 放弃来源 | D，不推荐 |
| 当前 block | 保持，不解除 |
| 当前 Greek 状态 | 保持 `acquired / verification_failed` |
| 当前记录状态 | 保持 `acquired / draft` |

### 6.2 本阶段执行边界

```yaml
raw_xml_modified: false
raw_checksum_changed: false
normalized_files_created: 0
english_tei_acquired: false
cts_metadata_acquired: false
source_records_created_or_modified: 0
registry_modified: false
quality_report_modified: false
analysis_created: 0
character_or_plot_data_created: 0
adaptation_or_script_files_created: 0
block_released: false
```

## 7. 决策依据

- `P0_GREEK_SOURCE_ACQUISITION_RESULT.md`
- `source/metadata/quality/source_quality_report.md`
- `GREEK_TEI_VALIDATION_EXCEPTION.md`
- `SOURCE_RECORD_TEMPLATE.yaml`
- `P0_SOURCE_REGISTRY.md`
- `P0_GREEK_SOURCE_ACQUISITION.md`
- `01_SOURCE_PACKAGE_STRUCTURE.md`
- `02_SOURCE_ACQUISITION_PLAN.md`
- `03_SOURCE_ACQUISITION_EXECUTION_CHECKLIST.md`
- `SOURCE_DIRECTORY_INITIALIZATION.md`

本文完成只表示处置方案、推荐路径和解阻门槛已经形成书面决策记录。后续第一步应是对本文与验证合同进行人工评审；在批准及证据同步完成前，P0-3-B 继续保持 `BLOCKED_STRUCTURE_VALIDATION`。
