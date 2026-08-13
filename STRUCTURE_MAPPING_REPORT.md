# Classic-to-Drama Engine：English TEI Structure Mapping Report

> 项目：Classic-to-Drama Engine  
> 阶段：Phase 2-C-R2  
> 任务：English TEI Structure Mapping  
> 日期：2026-08-11  
> 最终状态：`PASS_VALIDATED_STRUCTURE_MAPPING`  
> Map 状态：`validated`  
> Candidate Run 执行：否  
> 文学分析执行：否

## 1. 执行范围与结论

本阶段仅对固定 English TEI 来源执行独立的 Structure Mapping Preflight，生成 Book、Card、Paragraph 的结构元数据与原始 UTF-8 字节边界。Character data 在 parser 事件层被丢弃，未写入 Map、报告或其他文件；本阶段未启动或复用任何 Candidate Run。

结构映射通过 mapper 与独立 validator 的双通道检查，最终结果为：

```yaml
status: PASS_VALIDATED_STRUCTURE_MAPPING
mapping_status: validated
validation_overall_result: pass
blockers: []
unresolved_source_notices:
  - NOTICE_CREFPATTERN_CARD_SEPARATOR_UNESCAPED
```

`AC-20260811-STORYSTRUCT-001` 继续保持 `BLOCKED_SCOPE_ENFORCEMENT_FAILED / invalidated`，本阶段未修改其文件、状态或结果，也没有创建新的 Run ID。

## 2. 输入来源身份

| 字段 | 验证值 |
| --- | --- |
| `source_id` | `ODY-ENG-MURRAY1919` |
| `file_id` | `ODY-ENG-MURRAY1919-RAW-FULL-TEI` |
| raw path | `source/translations/en/ody-eng-murray1919/raw/ody-eng-murray1919__raw__full.xml` |
| fixed commit | `790c84289edbdbe289dd7b752bfea29f0af4299d` |
| size | `870,905 bytes` |
| source SHA-256 | `dda5b206e332e56c570c1d92ea41e9a510339a454bc2ea90491788e34174a7e7` |
| Git blob SHA-1 | `00012e531976c182625bacc9374b07cd4411750d` |
| source object ID | `urn:sha256:dda5b206e332e56c570c1d92ea41e9a510339a454bc2ea90491788e34174a7e7` |
| encoding | strict `UTF-8` |
| TEI namespace | `http://www.tei-c.org/ns/1.0` |
| native locator scheme | `book.card` |

来源大小与 SHA-256 和 `P0_ENGLISH_SOURCE_ACQUISITION_RESULT.md` 完全一致。Mapper 与 validator 绑定同一个 filesystem object identity，并分别复核内容寻址身份；映射前后 raw 的 inode、size、mtime 与 SHA-256 均未改变。

## 3. 结构识别结果

| 层级 | element QName | namespace-aware path | 结构 attributes | 表示方式 |
| --- | --- | --- | --- | --- |
| Book | `{http://www.tei-c.org/ns/1.0}div` | `TEI/text/body/div/div` 的 Clark-QName 等价路径 | `type=textpart`、`subtype=book`、`n=1..24` | XML container |
| Card | `{http://www.tei-c.org/ns/1.0}div` | `TEI/text/body/div/div/div` 的 Clark-QName 等价路径 | `type=textpart`、`subtype=card`、正整数 `n` | `container` |
| Paragraph | `{http://www.tei-c.org/ns/1.0}p` | `TEI/text/body/div/div/div/p` 的 Clark-QName 等价路径 | 无 | XML element；与 Card 以 byte-range overlap/span 关联 |

识别总数：

| 结构项 | 数量 | 验证结果 |
| --- | ---: | --- |
| Books | 24 | `1..24` 各唯一一次，文档顺序正确 |
| Cards | 288 | 每卷为正整数、唯一且严格递增；不要求连续 |
| Paragraphs | 288 | 每个 Card 恰有一个直接子 `tei:p` |
| Card 外的正文 Paragraph | 0 | `PASS` |
| 跨 Card Paragraph | 0 | `PASS` |
| 排除的 `unit=line` milestones | 2,434 | 全部为 Paragraph 内自闭合元素，未误作 Card |
| body 内 ancillary notes | 192 | 未误作 Paragraph |

各 Book 的 Card 数依次为：

```text
10, 10, 11, 20, 11, 8, 9, 14, 14, 14, 15, 12,
11, 13, 14, 11, 14, 11, 14, 9, 10, 12, 9, 12
```

## 4. 字节边界与交叉验证

所有 offset 均以原始 UTF-8 字节流为基准，采用 zero-based、half-open 区间 `[start_byte, end_byte_exclusive)`。

Mapper 使用 namespace-aware Expat 结构事件，并以独立 quote-aware lexical scanner 计算原始 tag 边界；validator 另用 lxml target parser 丢弃 character data，并使用 exact `pread(offset, length)` 对每个 Book、Card、Paragraph 的完整 slice 反向取字节和复算 SHA-256。

| 检查项 | 结果 |
| --- | --- |
| namespace-aware start/end events | `3,703 / 3,703` |
| lexical start tags | `3,703` |
| explicit end tags | `1,269` |
| self-closing elements | `2,434` |
| parser／lexical QName 与 byte-index 一一对应 | `PASS` |
| 24 个 Book slice SHA-256 反向复算 | `PASS` |
| 288 个 Card slice SHA-256 反向复算 | `PASS` |
| 288 个 Paragraph slice SHA-256 反向复算 | `PASS` |
| Book／Card／Paragraph containment 与顺序 | `PASS` |
| Card／Paragraph overlap 关系 | `PASS` |

边界集合摘要：

| 集合 | SHA-256 |
| --- | --- |
| Books | `9fa65e799ff09cf808d87eff36cc393539e3f531f1d78c9417b1551d8d6a005b` |
| Cards | `19a67aaab5e6f64ab22011723e15ec4a470f678ac706a073b88d9e63e4c5ab5c` |
| Paragraphs | `7e24f0e200826855f7503edd4e8b54c84327397750e01a87546be29b052bbbc6` |

## 5. Book 1 独立定位证明

严格 Book selector 对 Book 1 的匹配数为 `1`。

```yaml
book_number: 1
element_qname: "{http://www.tei-c.org/ns/1.0}div"
full_element_range:
  start_byte: 4076
  end_byte_exclusive: 36515
start_tag_range:
  start_byte: 4076
  end_byte_exclusive: 4118
content_range:
  start_byte: 4118
  end_byte_exclusive: 36509
end_tag_range:
  start_byte: 36509
  end_byte_exclusive: 36515
slice_size_bytes: 32439
slice_sha256: 7bd8baca8c89f91c1cad6ca54c9e6e8f1eae1139d7543ef0941a88f83151ac39
card_count: 10
fragment_parse_supported: true
```

Book 1 的 Card allowlist 为：

```text
1.1, 1.44, 1.80, 1.125, 1.178,
1.230, 1.280, 1.325, 1.365, 1.421
```

Book 元素自身未重复声明默认 TEI namespace，并继承 `xml:lang="eng"`。Validator 使用只含 namespace 与继承 XML attribute 的无正文内存 wrapper 对 24 个 Book slice 分别严格重解析，全部通过。Wrapper 未写入磁盘；其模板 SHA-256 为 `d4d45a2c2d43e9197b4ca24b3c39a697aec5118c4e4058ce1b44cc95678f75b5`。

因此，Book 1 已具备唯一 locator、完整元素 range、slice size、slice checksum、Card allowlist 与安全片段解析证据，可以在未来由独立 range broker 精确选择；本结论不等于启动 Candidate Run。

## 6. Map 身份与验证记录

| 字段 | 值 |
| --- | --- |
| artifact | `book_structure_map.yaml` |
| serialization | YAML 1.2 的 JSON-compatible single-document 子集 |
| final file size | `1,177,213 bytes` |
| final map file SHA-256 | `fd0314844ee2e9c28487ea3d717d3bc75a96be4cbe0a9c74cb2defd8640d6bc3` |
| canonicalization | `CTDE-MAP-C14N-1` |
| mapping payload SHA-256 | `45740c706b615bb0f83d5b763db189bff0b87228e5814f5f16b92f46dc5faaa5` |
| attestation ID | `urn:sha256:63aaf1f0fa834815d0a5652051444522a84cb681412442420b6d471d78707e8c` |
| generated at | `2026-08-11T08:43:04Z` |
| validated at | `2026-08-11T08:46:30Z` |

最终文件同时通过严格 JSON 解析与 YAML safe parsing，语义树一致。`mapping_payload_sha256` 在删除顶层 `validation` 后按 `CTDE-MAP-C14N-1` 独立复算一致；最终文件 SHA-256 单独保存在本报告中，未写回 Map 形成递归 checksum。

Validator 结果：

```yaml
source_object_id_match: pass
source_identity_match: pass
xml_hierarchy_check: pass
locator_check: pass
byte_boundary_check: pass
parent_child_check: pass
fragment_parse_check: pass
no_text_payload_check: pass
overall_result: pass
blockers: []
```

## 7. 未解决异常

存在 1 项来源级、非阻断 warning：

- `NOTICE_CREFPATTERN_CARD_SEPARATOR_UNESCAPED`：Card 的原始 `cRefPattern.matchPattern` 为 `(\w+).(\w+)`，其中分隔点号未转义，正则接受范围比字面 `book.card` 更宽。Map 未修改或“修正”来源值；validator 通过 replacement XPath、严格 TEI QName、完整 ancestor path、`type/subtype` discriminator、数字 locator 及实际 24／288 结构的共同约束，确认本文件中的 Book／Card 匹配唯一。因此该项保留为 `unresolved_source_lexical_issue / warning_non_blocking`，不构成结构映射 blocker。

未解决阻断项：`0`。

## 8. 禁止项检查

| 项目 | 结果 |
| --- | --- |
| Greek raw open／read／parse／copy | `0` |
| Candidate Run 执行 | `0` |
| 模型调用 | `0` |
| English raw 写入 | `0` |
| XML character data 持久化 | `false` |
| prose-bearing attribute payload 持久化 | `false` |
| 文学摘要、人物、事件、主题、改编或剧本字段 | `0` |
| normalized／alignment 文件 | `0` |
| raw／状态文件修改 | `0` |

Map 仅包含 locator、QName、结构白名单 attributes、byte ranges、checksums、父子／overlap 关系、工具身份与验证元数据。

## 9. 最终状态块

```yaml
phase: Phase 2-C-R2
task: English TEI Structure Mapping
status: PASS_VALIDATED_STRUCTURE_MAPPING

source_id: ODY-ENG-MURRAY1919
source_sha256: dda5b206e332e56c570c1d92ea41e9a510339a454bc2ea90491788e34174a7e7
map_file: book_structure_map.yaml
map_file_sha256: fd0314844ee2e9c28487ea3d717d3bc75a96be4cbe0a9c74cb2defd8640d6bc3
mapping_payload_sha256: 45740c706b615bb0f83d5b763db189bff0b87228e5814f5f16b92f46dc5faaa5
mapping_status: validated

book_count: 24
card_count: 288
paragraph_count: 288
book_1_unique: true
book_1_fragment_parse_supported: true
card_representation_kind: container
paragraph_spans_computable: true

unresolved_blockers: []
unresolved_non_blocking_notices:
  - NOTICE_CREFPATTERN_CARD_SEPARATOR_UNESCAPED

failed_run_id: AC-20260811-STORYSTRUCT-001
failed_run_status_preserved: BLOCKED_SCOPE_ENFORCEMENT_FAILED / invalidated
candidate_runs_executed_this_task: 0
greek_raw_access_count: 0
model_invocations: 0
literary_analysis_created: 0
```

本报告确认结构映射已完成并通过独立机械验证。它不授权 Candidate Run，不改变 English 的人工批准状态，也不解除 Greek 或正式 Phase 2 Gate。
