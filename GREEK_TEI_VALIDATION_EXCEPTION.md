# 《奥德赛》Greek TEI 验证异常登记

> 项目：Classic-to-Drama Engine  
> 阶段：Phase 1-E / P0-3-C  
> 登记日期：2026-08-10  
> 上一阶段：`P0-3-B = BLOCKED_STRUCTURE_VALIDATION`  
> 当前处置：只登记异常，不修复、不解除阻断、不改变来源状态

## 1. 原始验证结果

| 字段 | 已证实值 |
| --- | --- |
| `source_id` | `ODY-GRC-MURRAY1919` |
| `file_id` | `ODY-GRC-MURRAY1919-RAW-FULL-TEI` |
| 固定 commit | `790c84289edbdbe289dd7b752bfea29f0af4299d` |
| raw file path | `source/original_text/grc/ody-grc-murray1919/raw/ody-grc-murray1919__raw__full.xml` |
| SHA-256 | `184fa4fc598f0cd9d2964b17eaabe36bd9c61d44c2eae264c4b016feacf28530` |
| acquisition status | `acquired` |
| 当前 verification status | `verification_failed` |
| SOURCE_RECORD status | `acquired` |
| SOURCE_RECORD record status | `draft` |
| 上一阶段最终状态 | `BLOCKED_STRUCTURE_VALIDATION` |

P0-3-B 已确认：raw 文件真实存在且非空，原始字节保持不变；XML 与 UTF-8 严格解析通过；TEI/CTS 身份、Murray 1919、24 卷结构和 `book.line` 可寻址性通过；实际文件、SOURCE_RECORD 与 checksum 索引中的 SHA-256 一致。

本登记不重新执行获取，不产生新的来源字节，也不改变上述事实或状态。

## 2. 异常列表

| 异常 ID | 位置 | 已观察到的结构证据 | 违反的既有验证条件 | 当前状态 |
| --- | --- | --- | --- | --- |
| `LOCAL-STRUCTURE-B03-ORDER` | Book 3 | locator 文档顺序出现 `303, 305, 304, 306` | 卷内 locator 应单调递增 | `unresolved / blocking` |
| `LOCAL-STRUCTURE-B14-ORDER` | Book 14 | locator 文档顺序出现 `62, 64, 63, 65` | 卷内 locator 应单调递增 | `unresolved / blocking` |
| `LOCAL-STRUCTURE-B16-GAP` | Book 16 | locator 从 `100` 到 `102`，未见 `16.101` | locator 缺口必须完成人工分类 | `unresolved / blocking` |

这些记录仅描述标签、locator 顺序和覆盖范围，不判断诗文内容，也不推断缺失 locator 对应的文本内容。

## 3. 异常分类

### 3.1 分类结论

| 候选分类 | 判断 | 依据与边界 |
| --- | --- | --- |
| `source corruption` | 当前证据不支持 | 文件大小、不可变获取身份、XML 完整解析、双重 SHA-256 复核以及记录／索引一致性均已通过。现有证据不能证明下载截断、传输损坏或本地字节篡改。 |
| `TEI encoding issue` | 当前证据不支持作为已确认主分类 | XML、UTF-8、TEI root/namespace、CTS URN、语言和版本身份均通过。若“TEI encoding”特指上游标签排序或标签遗漏，其根因仍未被上游证据确认，不能在本阶段写成定论。 |
| `locator normalization issue` | **适用；三项异常的主分类** | 三项异常均局限于 locator 的文档顺序或编号覆盖范围；raw 仍可按 `book.line` 寻址，locator 为正整数且卷内唯一。它们属于未来消费层需要显式处置的 locator 规范化问题。 |
| `validation rule mismatch` | **适用；流程层次的次级分类，待批准** | 既有 Gate 用“严格单调／所有缺口已分类”判断 raw 来源验证，而来源真实性、XML 合法性与引用能力已经通过。该规则把 raw 来源完整性与分析消费层的 locator 连续性要求合并，因而导致阻断；是否调整 Gate 必须另行批准，本登记不能自行放宽规则。 |

### 3.2 逐项归类

| 异常 ID | 主分类 | 次级流程分类 | 根因结论 |
| --- | --- | --- | --- |
| `LOCAL-STRUCTURE-B03-ORDER` | `locator normalization issue` | `validation rule mismatch`（待批准） | locator 次序异常已证实；上游标签为何如此排序尚未证实 |
| `LOCAL-STRUCTURE-B14-ORDER` | `locator normalization issue` | `validation rule mismatch`（待批准） | locator 次序异常已证实；上游标签为何如此排序尚未证实 |
| `LOCAL-STRUCTURE-B16-GAP` | `locator normalization issue` | `validation rule mismatch`（待批准） | `16.101` 未出现已证实；来源版本省略、标签遗漏或其他原因尚未证实 |

因此，本阶段不能将三项异常称为“已证实的 source corruption”，也不能用“验证规则不匹配”自动覆盖失败结果。Greek TEI 继续保持 `acquired / verification_failed`。

## 4. 处理原则

1. **raw 文件保持不变。** 不重排 Book 3 或 Book 14 的节点，不补写 `16.101`，不改编号、字符、空白、换行、XML 声明或文件头。
2. **checksum 保持不变。** raw 文件的 SHA-256 继续为 `184fa4fc598f0cd9d2964b17eaabe36bd9c61d44c2eae264c4b016feacf28530`；不得因异常登记重新推算、替换或伪造摘要。
3. **不伪造通过状态。** 在异常尚未获批处置前，`verification_status` 保持 `verification_failed`，不得提升为 `verified` 或 `approved`；acquisition 事实仍为 `acquired`。
4. **异常登记与异常豁免分离。** 本文只记录事实与分类，不构成 Gate 豁免、来源批准或 analysis 开始授权。
5. **后续处理只能发生在 normalized 层。** 如果项目决定重排 locator、建立缺口标记或形成连续引用视图，必须新建可追溯的 normalized 派生物；不得回写 raw。
6. **不得伪造缺失内容。** normalized 层不得凭空生成 `16.101` 的文本或把相邻行复制为该 locator；只能按获批规则记录缺口、映射或来源版异常。
7. **派生链必须可审计。** 未来 normalized 处理需记录 raw 输入路径及 SHA-256、转换规则、工具／版本、执行日期、输出摘要，以及 raw locator 与 normalized locator 的双向映射或异常表。

## 5. 进入 analysis 前的必要条件

在任何剧情、人物、事件或改编分析开始前，至少需要满足以下条件：

- [ ] 三项异常均有书面、获批的处置结论：接受为 raw 版本已知异常，或要求在 normalized 层建立确定性处理；不得继续保持原因与消费规则均未定义的状态。
- [ ] 批准统一 locator 合同，明确分析层对非单调 locator、缺失 locator、来源版本省略和不可解析引用分别如何处理。
- [ ] 若 analysis 依赖单调或连续的 `book.line` 视图，先在 normalized 层生成独立派生文件及 raw↔normalized 映射，并完成 XML、24 卷、locator 唯一性、映射可追溯性和输出 checksum 验证。
- [ ] 重新执行 Greek 来源／消费就绪验证，并依据既有状态词汇形成明确决定；异常登记本身不得自动把 `verification_failed` 改为 `verified` 或 `approved`。
- [ ] `P0_SOURCE_REGISTRY.md` 中仍为 pending 的 English TEI、CTS textgroup metadata、CTS work metadata，按既有 Minimum Source Set 与 Gate 规则完成真实获取和验证；在此之前不得声称 P0 或完整 Source Package 已就绪。
- [ ] analysis 的输入清单明确排除 raw 文件的直接隐式修补，并引用获批的异常登记、locator 合同和实际消费文件身份。

若项目决定 analysis 可以直接消费保留异常的 raw TEI，则仍须先批准异常感知规则：按 XML 文档顺序读取还是按 locator 排序、遇到 `16.101` 请求时如何返回明确缺失、以及如何防止生成不存在的引用。该决定不得由分析代码静默推断。

## 6. 本阶段状态影响

| 对象 | P0-3-C 后状态／影响 |
| --- | --- |
| Greek raw XML | 未修改 |
| Greek SHA-256 | 未修改 |
| Greek acquisition status | 保持 `acquired` |
| Greek verification status | 保持 `verification_failed` |
| Greek SOURCE_RECORD | 不修改 |
| P0 registry | 不修改 |
| normalized 文件 | 不创建 |
| 其他 P0 来源 | 不获取，继续保持 `pending / pending` |
| analysis／人物／剧情／改编／剧本 | 不创建 |

## 7. 本登记依据

- `P0_GREEK_SOURCE_ACQUISITION_RESULT.md`
- `source/metadata/quality/source_quality_report.md`
- `SOURCE_RECORD_TEMPLATE.yaml`
- `P0_SOURCE_REGISTRY.md`

本登记的完成只表示三个验证异常已被独立、可审计地记录；P0-3-B 的 `BLOCKED_STRUCTURE_VALIDATION` 尚未解除。
