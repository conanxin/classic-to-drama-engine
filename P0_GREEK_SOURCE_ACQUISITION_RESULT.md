# 《奥德赛》P0 Greek TEI 获取执行结果

> 项目：Classic-to-Drama Engine  
> 阶段：Phase 1-E / P0-3-B  
> 执行日期：2026-08-10  
> 最终状态：`BLOCKED_STRUCTURE_VALIDATION`

## 1. 结果摘要

Greek TEI 已从固定 commit 的不可变 raw 地址取得并原样落盘；来源身份、XML、编码、24 卷、CTS、`book.line` 支持与 SHA-256 均已确认。严格 locator 检查同时发现两个卷内非单调顺序和一个尚无上游处置说明的缺口，因此按既有 P0-3-A 合同不能把该来源标为 `verified` 或 `approved`。

当前保留真实状态：文件获取为 `acquired`，技术验证为 `verification_failed`，具体记录为 `draft`。未伪造成功，未修改 raw，也未获取其他 P0 来源。

## 2. 来源与版本身份

| 字段 | 实际值 |
| --- | --- |
| `source_id` | `ODY-GRC-MURRAY1919` |
| `file_id` | `ODY-GRC-MURRAY1919-RAW-FULL-TEI` |
| repository | `https://github.com/PerseusDL/canonical-greekLit` |
| 固定 commit SHA | `790c84289edbdbe289dd7b752bfea29f0af4299d` |
| commit 时间 | `2026-08-03T21:01:46Z` |
| 仓库内部路径 | `data/tlg0012/tlg002/tlg0012.tlg002.perseus-grc2.xml` |
| commit-pinned 获取地址 | `https://raw.githubusercontent.com/PerseusDL/canonical-greekLit/790c84289edbdbe289dd7b752bfea29f0af4299d/data/tlg0012/tlg002/tlg0012.tlg002.perseus-grc2.xml` |
| 本地目标路径 | `source/original_text/grc/ody-grc-murray1919/raw/ody-grc-murray1919__raw__full.xml` |
| 文件字节数 | `1,560,139` |
| SHA-256 | `184fa4fc598f0cd9d2964b17eaabe36bd9c61d44c2eae264c4b016feacf28530` |
| Git blob SHA-1 交叉核验 | `f38f5f238d665eafb9c6878b11283822ed418a07`，与官方文件元数据一致 |
| SOURCE_RECORD | `source/metadata/records/ody-grc-murray1919-raw-full-tei.source.yaml` |

该 commit 下四个核心路径均已确认存在；本轮只传输 Greek TEI。English TEI、textgroup CTS 与 work CTS 未下载。

## 3. 非内容型验证结果

| 检查 | 结果 | 证据摘要 |
| --- | --- | --- |
| 文件存在／非空 | PASS | 普通文件，`1,560,139` bytes |
| 非 HTML／错误页 | PASS | 无 HTML、登录、限流或 Not Found 特征 |
| XML 完整解析 | PASS | namespace-aware 严格解析成功 |
| 编码 | PASS | XML 声明 UTF-8；严格解码成功；U+FFFD 为 0 |
| TEI root／namespace | PASS | `TEI` / `http://www.tei-c.org/ns/1.0` |
| TEI／CTS 身份 | PASS | `urn:cts:greekLit:tlg0012.tlg002.perseus-grc2` 精确匹配 |
| Murray 1919 edition | PASS | header 记录 Homer、Augustus Taber Murray、Heinemann／Putnam、1919、Volumes 1–2 |
| Greek language | PASS | edition `xml:lang="grc"` |
| 24 卷 | PASS | 恰有 24 个 book，顺序 `1..24` |
| `book.line` 支持 | PASS | `cRefPattern` 同时定义 `book` 与 `line`；locator 均为正整数且卷内唯一 |
| locator 单调性 | FAIL | Book 3：`303,305,304,306`；Book 14：`62,64,63,65` |
| locator 缺口分类 | FAIL | Book 16 缺 `16.101`，未发现对应上游处置说明 |
| SHA-256 双重复算 | PASS | `sha256sum` 与 OpenSSL 结果一致 |
| 记录／索引一致 | PASS | raw、SOURCE_RECORD 和 `checksums.sha256` 三者一致 |

### 已知上游问题

- `#1652`：open；上游将 `10.456`、`23.49` 说明为 Murray 来源版本身未收录。
- `#1655`：open，`wontfix / on hold`；由 `#1652` 的来源版说明覆盖。

raw 文件未自动补行、重排、重编号或修补。

## 4. 状态更新结果

| 对象 | 更新结果 |
| --- | --- |
| Greek acquisition | `pending -> acquired` |
| Greek verification | `pending -> verification_failed` |
| Greek SOURCE_RECORD `status` | `acquired` |
| Greek SOURCE_RECORD `record_status` | `draft` |
| `P0_SOURCE_REGISTRY.md` | 仅 Greek 行更新；其余三行仍为 `pending / pending` |
| 执行清单 | `P0-01`、`P0-02` 已完成；Greek 单文件矩阵记录失败；复合项 `P0-06`、`P0-07` 未勾选 |
| Gate S1-B / S1-C / S1 | 未声称通过 |

## 5. 尚未获取的 P0 项目

| 项目 | acquisition | verification | checksum |
| --- | --- | --- | --- |
| English TEI `perseus-eng3` | `pending` | `pending` | `null` |
| CTS textgroup metadata | `pending` | `pending` | `null` |
| CTS work metadata | `pending` | `pending` | `null` |

## 6. 实际创建或修改的文件

### 新增

1. `source/original_text/grc/ody-grc-murray1919/raw/ody-grc-murray1919__raw__full.xml`
2. `source/metadata/records/ody-grc-murray1919-raw-full-tei.source.yaml`
3. `source/metadata/sources.yaml`
4. `source/metadata/checksums/checksums.sha256`
5. `source/metadata/logs/acquisition_log.jsonl`
6. `source/metadata/quality/source_quality_report.md`
7. `P0_GREEK_SOURCE_ACQUISITION_RESULT.md`

### 修改

1. `P0_SOURCE_REGISTRY.md`
2. `03_SOURCE_ACQUISITION_EXECUTION_CHECKLIST.md`

## 7. 边界核验

```yaml
external_byte_assets_downloaded: 1
greek_raw_xml_files: 1
concrete_source_records_created: 1
real_source_sha256_values: 1
english_tei_downloaded: false
cts_metadata_downloaded: false
normalized_files_created: 0
content_analysis_created: 0
character_database_created: 0
plot_database_created: 0
adaptation_files_created: 0
script_files_created: 0
```

## 8. 阻断原因与下一动作

阻断原因是当前 commit 中 Book 3、Book 14 的 line locator 文档顺序违反既有“卷内单调递增”要求，且 Book 16 的 `16.101` 缺口尚未完成人工分类。继续把该文件提升为 `verified / approved` 会违反 P0-3-A。

下一步应先就这三个纯结构异常形成获批处置结论（保留为版本已知异常、选择另一经验证 commit，或在未来 normalized 层建立不修改 raw 的修正策略）。在此之前，不应获取其他来源来掩盖本项失败，也不应改写 raw。
