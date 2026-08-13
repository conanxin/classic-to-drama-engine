# 《奥德赛》Perseus English TEI 获取与验证结果

> 项目：Classic-to-Drama Engine  
> 阶段：Phase 1-F / P0-4-B  
> 执行日期：2026-08-10  
> 最终状态：`PASS_TECHNICAL_VERIFICATION`  
> English 状态：`acquired / verified`  
> 人工批准：`pending`  
> P0 总体状态：`blocked`（Greek `BLOCKED_STRUCTURE_VALIDATION` 未解除；两个 CTS metadata 尚未获取）

## 1. 来源与固定版本

| 项目 | 实际值 |
| --- | --- |
| `source_id` | `ODY-ENG-MURRAY1919` |
| `file_id` | `ODY-ENG-MURRAY1919-RAW-FULL-TEI` |
| title | *The Odyssey, Volumes 1–2* |
| edition | A. T. Murray 英译；William Heinemann / G. P. Putnam's Sons；1919；CTS `perseus-eng3` |
| translator | Augustus Taber Murray |
| repository | `https://github.com/PerseusDL/canonical-greekLit` |
| fixed commit | `790c84289edbdbe289dd7b752bfea29f0af4299d` |
| repository path | `data/tlg0012/tlg002/tlg0012.tlg002.perseus-eng3.xml` |
| commit-pinned retrieval URL | `https://raw.githubusercontent.com/PerseusDL/canonical-greekLit/790c84289edbdbe289dd7b752bfea29f0af4299d/data/tlg0012/tlg002/tlg0012.tlg002.perseus-eng3.xml` |
| canonical CTS URN | `urn:cts:greekLit:tlg0012.tlg002.perseus-eng3` |

指定 commit 已由官方仓库提交对象确认，完整 SHA 与 P0-3-B Greek 所用 commit 相同。未解析或使用 `main`、`master`、`latest` 等浮动引用，也未获取两个 CTS metadata 或其他来源文件。

## 2. 最终落盘与字节身份

| 项目 | 结果 |
| --- | --- |
| 本地目标路径 | `source/translations/en/ody-eng-murray1919/raw/ody-eng-murray1919__raw__full.xml` |
| 文件类型 | 普通文件 |
| 文件大小 | `870,905` bytes |
| SHA-256 | `dda5b206e332e56c570c1d92ea41e9a510339a454bc2ea90491788e34174a7e7` |
| Git blob SHA-1 | `00012e531976c182625bacc9374b07cd4411750d` |
| 上游 blob 身份匹配 | `PASS` |
| raw 最终化后字节修改 | `false` |

SHA-256 已分别使用 `sha256sum` 与 OpenSSL 对最终落盘字节独立计算，两次结果一致；同一值已写入具体 `SOURCE_RECORD` 和 `source/metadata/checksums/checksums.sha256`。Git blob SHA-1 与固定 commit 返回的文件身份完全一致，证明最终 raw 字节没有换行、编码或 XML 内容漂移。

## 3. English 专属验证结果

| 检查 | 结果 | 证据摘要 |
| --- | --- | --- |
| 文件存在且非空 | `PASS` | 普通文件，`870,905` bytes |
| 非 HTML／错误页 | `PASS` | 未检出 HTML、登录、限流或错误页特征 |
| XML 完整解析 | `PASS` | 标准 namespace-aware XML parser 严格解析成功 |
| 编码 | `PASS` | XML declaration 为 UTF-8；严格解码成功；无 BOM、无 U+FFFD |
| TEI root / namespace | `PASS` | `{http://www.tei-c.org/ns/1.0}TEI` |
| Murray 1919 English identity | `PASS` | Odyssey、Homer、A. T. Murray、Heinemann、Putnam、1919、Volumes 1–2 均由 TEI header 确认 |
| CTS identity | `PASS` | 精确为 `urn:cts:greekLit:tlg0012.tlg002.perseus-eng3` |
| 24 Book structure | `PASS` | 恰有 Book `1..24`，无缺失、重复或倒序 |
| `book.card` citation scheme | `PASS` | CTS `cRefPattern` 为 `card` 与 `book` |
| card 可定位性 | `PASS` | 共 `288` 个 card；均为正整数、卷内唯一并按原生文档顺序递增 |
| card 连续性 | `not_required` | card 是版本原生页面／段块锚点，不要求连续 |
| Greek `book.line` 规则 | `not_applicable_book_card_source` | 未执行 Greek locator 单调、gap 或异常规则 |
| English–Greek alignment | `not_started` | 本阶段未建立 card-to-line 映射 |
| 记录闭环 | `PASS` | `file -> file_id -> SOURCE_RECORD -> checksums.sha256` 一对一成立 |

TEI body 中存在提供方的印刷行 milestone，但 CTS 原生 locator 仍只有 `book.card`。这些 milestone 未被当作 English `book.line`，也未套用 Greek Book 3、14、16 的 locator 验证规则。

## 4. `eng` 与 `en` 的显式登记

上游 raw TEI 的实际语言标记是 `xml:lang="eng"`，TEI header 同时声明 `<language ident="eng">English</language>`；项目目录和 `SOURCE_RECORD.language` 采用 `en`。

本次按统一模板允许的 ISO 639 / BCP 47 兼容规则，将其登记为：

```yaml
source_xml_lang: eng
semantic_language_identity: English
project_language: en
mapping: ISO 639-2 eng -> BCP 47 en
result: pass_non_destructive_metadata_mapping
```

没有声称 raw 的字面标记为 `en`，没有修改 XML，也没有创建 normalized 文件。该已显式记录的等价映射不构成未解决的 English 阻断。

## 5. 登记与状态同步

| 对象 | 结果 |
| --- | --- |
| SOURCE_RECORD | `source/metadata/records/ody-eng-murray1919-raw-full-tei.source.yaml`；`status: verified`；`record_status: verified` |
| checksum index | 已新增 English raw 的一条真实 SHA-256 |
| acquisition log | 已新增 English `started` 与 `succeeded` 事件 |
| sources registry | English 已更新为 `acquired / verified / approval pending` |
| P0 registry | English 已更新为 `acquired / verified`；计数同步 |
| execution checklist | `P0-03` 与 English 分文件矩阵已按证据更新；累计 `P0-06/P0-07` 仍未勾选 |
| quality report | 已加入 English 技术验证结果与 `eng -> en` 映射说明 |

技术验证通过只推进到 `verified`。本步骤未执行独立人工批准，因此没有把 English 自动标为 `approved`。

## 6. 未完成的 P0 项目与边界

- Greek `ODY-GRC-MURRAY1919`：继续保持 `acquired / verification_failed`；三项 locator exception 与 `BLOCKED_STRUCTURE_VALIDATION` 未解除。
- CTS textgroup metadata：继续保持 `pending / pending / checksum null`。
- CTS work metadata：继续保持 `pending / pending / checksum null`。
- P0 四文件交叉身份检查、Gate S1-C、Gate S1-D、总 Gate S1 与 Phase 2 Analysis Gate 均未完成。
- English–Greek alignment 保持 `not_started`。
- 未创建 normalized、passage、alignment、人物、剧情、事件、改编、剧本或制作数据。

## 7. 实际创建或修改的文件

### 新增

1. `source/translations/en/ody-eng-murray1919/raw/ody-eng-murray1919__raw__full.xml`
2. `source/metadata/records/ody-eng-murray1919-raw-full-tei.source.yaml`
3. `P0_ENGLISH_SOURCE_ACQUISITION_RESULT.md`

### 修改

1. `source/metadata/checksums/checksums.sha256`
2. `source/metadata/logs/acquisition_log.jsonl`
3. `source/metadata/sources.yaml`
4. `source/metadata/quality/source_quality_report.md`
5. `P0_SOURCE_REGISTRY.md`
6. `03_SOURCE_ACQUISITION_EXECUTION_CHECKLIST.md`

本轮最终新增的外部字节资产恰好为 1 个，新增具体来源记录恰好为 1 份，新增真实来源 SHA-256 恰好为 1 条。

## 8. 最终状态块

```yaml
phase: Phase 1-F
task: P0-4-B
status: PASS_TECHNICAL_VERIFICATION

english_source_id: ODY-ENG-MURRAY1919
english_acquisition_status: acquired
english_verification_status: verified
english_approval_status: pending
english_bytes: 870905
english_sha256: dda5b206e332e56c570c1d92ea41e9a510339a454bc2ea90491788e34174a7e7
english_git_blob_sha: 00012e531976c182625bacc9374b07cd4411750d
english_books: 24
english_cards: 288
book_line_rule: not_applicable_book_card_source
english_greek_alignment: not_started

greek_acquisition_status: acquired
greek_verification_status: verification_failed
blocked_structure_validation_released: false
pending_cts_metadata_files: 2

external_byte_assets_acquired_this_task: 1
source_records_created_this_task: 1
real_source_sha256_values_added_this_task: 1
normalized_files_created: 0
content_analysis_created: 0
character_database_created: 0
plot_database_created: 0
adaptation_outputs_created: 0
script_files_created: 0
```
