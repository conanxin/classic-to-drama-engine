# 《奥德赛》P0 Perseus 来源质量报告

> 范围：Phase 1-E / P0-3-B Greek TEI；Phase 1-F / P0-4-B English TEI  
> 检查日期：2026-08-10  
> 总体结果：`P0_INCOMPLETE`；Greek 保持 `BLOCKED_STRUCTURE_VALIDATION`，English 技术验证为 `verified`

## 1. Greek 已通过检查

- 固定 commit、仓库路径和 commit-pinned 获取地址已确认；同一 commit 下其余三个 P0 路径仅做存在性核验。
- raw 文件存在且为普通非空文件，远程与本地字节数均为 `1,560,139`。
- 本地 Git blob SHA-1 与 GitHub 文件身份 `f38f5f238d665eafb9c6878b11283822ed418a07` 一致。
- HTML／错误页特征未检出；XML 严格解析通过。
- XML 声明为 UTF-8，严格解码通过，未检出 U+FFFD。
- TEI root、namespace、题名、作者、编辑者、Murray 1919 书目信息、`grc` 和 CTS URN 均一致。
- Book 共 24 个，编号按 `1..24` 排列；TEI `cRefPattern` 明确支持 `book.line`。
- 所有 line locator 均为正整数，卷内没有重复 locator。
- SHA-256 已以两种独立实现复算一致，并与记录和 checksum 索引一致。

## 2. Greek 阻断项

| ID | 类型 | 结构证据 | 状态 |
| --- | --- | --- | --- |
| `LOCAL-STRUCTURE-B03-ORDER` | 行 locator 顺序不单调 | `303, 305, 304, 306` | unresolved / blocking |
| `LOCAL-STRUCTURE-B14-ORDER` | 行 locator 顺序不单调 | `62, 64, 63, 65` | unresolved / blocking |
| `LOCAL-STRUCTURE-B16-GAP` | 未分类 locator 缺口 | `100 -> 102`，缺 `16.101` | unresolved / blocking |

这些是对标签和 locator 的结构检查结果，不涉及诗文内容解释。按照 `P0_GREEK_SOURCE_ACQUISITION.md` 的“卷内单调递增”和“所有异常完成人工分类”硬门槛，当前文件不能进入 `verified` 或 `approved`。

## 3. Greek 已分类的上游已知项

- Perseus issue `#1652` 仍为 open；上游说明 Murray 来源版没有 `10.456` 和 `23.49`，归类为 source-edition omission。
- Perseus issue `#1655` 仍为 open，并标记 `wontfix / on hold`；其 `23.49` 问题由 `#1652` 的来源版说明覆盖。

上述两个已知项保留在记录中，未修改 raw。它们不消除本报告第 2 节的三个阻断项。

## 4. Greek 状态结论

```yaml
acquisition_status: acquired
verification_status: verification_failed
source_record_status: acquired
record_status: draft
raw_modified_after_download: false
normalized_files_created: 0
unresolved_blockers: 3
```

## 5. English TEI 验证结果

### 5.1 已通过检查

- 固定 commit `790c84289edbdbe289dd7b752bfea29f0af4299d` 与仓库路径 `data/tlg0012/tlg002/tlg0012.tlg002.perseus-eng3.xml` 已确认。
- 最终 raw 文件为 `870,905` bytes；本地 Git blob SHA-1 `00012e531976c182625bacc9374b07cd4411750d` 与固定 commit 的上游文件身份一致。
- 文件非 HTML／错误页；XML 严格解析通过，声明编码为 UTF-8，严格解码通过，未发现 U+FFFD。
- TEI root 与 namespace、题名、Homer、Augustus Taber Murray、Heinemann / Putnam、1919、两卷本信息均与 `perseus-eng3` 身份一致。
- CTS URN 精确为 `urn:cts:greekLit:tlg0012.tlg002.perseus-eng3`；`cRefPattern` 明确给出原生 `book.card`。
- 恰有 Book 1–24；共 `288` 个 card。所有 card locator 均为正整数、卷内唯一，并按原生文档顺序严格递增；不要求 card 连续。
- Greek `book.line` 单调／缺口规则明确记为 `not_applicable_book_card_source`；English–Greek alignment 保持 `not_started`。
- SHA-256 已由 `sha256sum` 与 OpenSSL 两种实现独立复算一致，并与具体记录及 checksum 索引完全一致。

### 5.2 语言代码映射说明

上游 raw TEI 使用 `xml:lang="eng"` 和 `<language ident="eng">English</language>`；项目目录与 `SOURCE_RECORD.language` 使用 `en`。`eng` 是上游采用的 ISO 639-2 English 代码，`en` 是项目采用的 BCP 47 / ISO 639-1 English 代码。本次将其显式登记为同一语言身份的元数据映射，未把 raw 字面值伪写为 `en`，也未修改 XML。该映射不构成未解决的 English 验证阻断。

### 5.3 English 状态结论

```yaml
acquisition_status: acquired
verification_status: verified
source_record_status: verified
record_status: verified
raw_modified_after_final_blob_match: false
book_line_rule: not_applicable_book_card_source
english_greek_alignment: not_started
unresolved_english_blockers: 0
human_approval_status: pending
```

English 单文件技术通过不解除 Greek 的三项结构阻断，也不完成两个 CTS metadata、P0 全批次、Gate S1 或 Phase 2 Analysis Gate。
