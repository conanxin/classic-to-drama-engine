# Classic-to-Drama Engine：Text Structure Mapping Specification

> 项目：Classic-to-Drama Engine  
> 阶段：Phase 2-C-R  
> 文档类型：Candidate Scope Enforcement Repair 结构映射规范  
> 日期：2026-08-11  
> 文档状态：`ready_for_review`  
> 当前效力：`specification_only / not_implemented`  
> 关联失效运行：`AC-20260811-STORYSTRUCT-001`  
> 关联运行状态：`BLOCKED_SCOPE_ENFORCEMENT_FAILED / invalidated`  
> Candidate Run 授权：否  
> Formal Phase 2 授权：否

## 0. 目的、依据与本阶段边界

本文修复 Candidate 范围执行架构中“必须先读取到 EOF，才能确认 Book 1 容器未被识别”的设计缺陷。修复目标不是解释或分析《奥德赛》正文，而是定义一份可机械验证的 TEI 结构映射合同，使未来运行在打开候选正文前就能知道 Book、Card、Paragraph 的精确结构身份与字节边界。

本文只依据：

- `CANDIDATE_RUN_001_PLAN.md`；
- `ANALYSIS_CANDIDATE_WORKFLOW.md`；
- `P0_ENGLISH_SOURCE_ACQUISITION_RESULT.md`；
- `ENGLISH_SOURCE_ANALYSIS_GATE_DECISION.md`。

已知且允许写入本规范的来源事实仅包括：

```yaml
source_id: ODY-ENG-MURRAY1919
file_id: ODY-ENG-MURRAY1919-RAW-FULL-TEI
fixed_upstream_commit: 790c84289edbdbe289dd7b752bfea29f0af4299d
raw_path: source/translations/en/ody-eng-murray1919/raw/ody-eng-murray1919__raw__full.xml
sha256: dda5b206e332e56c570c1d92ea41e9a510339a454bc2ea90491788e34174a7e7
native_locator_scheme: book.card
verified_source_structure: 24 Books / 288 Cards
source_status: acquired / verified
human_approval_status: pending
formal_phase_2_input: false
```

本阶段只创建本规范，不会：

- 打开或解析 English／Greek raw XML；
- 枚举任何 Book、Card 或 Paragraph 的实际节点；
- 读取、提取、概括或分析《奥德赛》正文；
- 生成 `book_structure_map.yaml`；
- 创建或执行新的 Candidate Run；
- 复用或重启已失效的 Run 001；
- 修改 English raw、SOURCE_RECORD、注册表、Gate 或既有运行审计文件；
- 创建 normalized、alignment、人物、事件、主题、改编或剧本产物。

## 1. TEI 结构识别目标

### 1.1 总体目标

结构映射必须在来源管理／运行预检阶段，把原生 TEI 的 XML 结构转换为一个**只含结构元数据、不含正文**的确定性映射。映射必须回答：

1. 哪一个 XML 元素唯一表示每个 Book；
2. 哪一种 XML 元素或 milestone 唯一表示每个 Card；
3. 哪些 `tei:p` 元素属于哪个 Book 与 Card 范围；
4. 每个结构单元在原始 UTF-8 文件中的精确字节边界；
5. Candidate reader 如何在不重新发现全书结构的情况下，只向解析器提供获批 Book 的字节；
6. 映射是否仍与固定来源快照完全一致。

结构映射是技术元数据，不是文学分析、文本摘要、normalized 文本、passage index 或 English–Greek alignment。

### 1.2 Book 识别目标

每个 Book 映射记录必须唯一确定：

- TEI namespace 下的实际 element QName；
- 从 `tei:TEI/tei:text/tei:body` 到 Book 容器的 namespace-aware 结构路径；
- 用于 Book 标识的实际 attribute QName、原始字符串值与规范化整数值；
- Book 容器在文档中的结构序号；
- 起始标签、内容区域、结束标签的字节边界；
- 容器内 Card 与 Paragraph 的数量及引用；
- 是否存在重复、嵌套、缺失或歧义 Book 匹配。

Book 的映射身份使用 `book_number` 表达。对于本来源，最终通过的 map 必须与已验证的 `1..24` Book 集合一致；不得仅因某个元素具有 `@n="1"` 就把它推断为 Book 1。

### 1.3 Card 识别目标

每个 Card 映射记录必须唯一确定：

- 由 TEI `refsDecl/cRefPattern` 与实际 XML 结构共同确认的 element QName；
- 结构表示类型 `representation_kind: milestone | container`；
- 表达 Card 层级的 attribute 规则，例如 cRefPattern 指向的 `@unit`、`@type`、`@subtype`、`@n` 或其他明确属性；
- 原始 card 值、规范化正整数值与原生 locator `book.card`；
- Card anchor 的字节位置；
- 该 Card 内容区间的 `start_byte` 与 `end_byte_exclusive`；
- 所属 Book、文档顺序、相邻 Card 边界和 Paragraph 引用；
- locator 是否唯一、是否按原生文档顺序递增。

Card 是本 English TEI 的原生定位层。Card 编号不要求连续，但必须是正整数、卷内唯一并按文档顺序递增。不得把印刷 line milestone、Greek `book.line` 或推测的 canonical line 当作 Card。

### 1.4 Paragraph 识别目标

Paragraph 只指结构上可确认的 TEI paragraph 元素：

- element QName 必须精确为 `{http://www.tei-c.org/ns/1.0}p`；
- 必须位于已映射 Book 容器内，并位于 `tei:text/tei:body` 内容域；
- 位于 `tei:teiHeader`、`tei:front`、`tei:back`、`tei:note` 或其他 ancillary 容器中的 `tei:p`，默认不得作为 Candidate 正文 Paragraph；
- 若来源存在嵌套、跨 Card 或无法唯一归属的 paragraph，必须显式记录歧义，不能静默重排或拆写 raw。

Paragraph 若没有来源原生 locator，只能获得 map-local 的派生结构 ID，例如 `B01-P0001`。该 ID 必须标记：

```yaml
locator_authority: derived_structure_map_only
native_locator: null
canonical_locator: false
```

Paragraph 映射可以记录其起止 Card 范围和字节边界，但不得保存正文、摘录、token、摘要、人物、事件、主题或语义标签。

### 1.5 三层结构关系

结构关系必须满足：

```text
Book container
  -> Card anchor / Card interval
  -> Paragraph element

Paragraph element <-> Card interval: overlaps / spans
```

并遵守以下规则：

- 每个 Card 恰好属于一个 Book；
- 每个获准正文 Paragraph 恰好属于一个 Book；
- Paragraph 可以跨越一个以上 Card anchor，但必须记录 `start_card`、`end_card` 与 `crosses_card_boundary: true`；
- Paragraph 与 Card 是 `overlaps / spans` 关系，不是“Paragraph 必须被单一 Card interval 包含”的父子关系；
- map 不得为跨 Card Paragraph 复制、切分或改写正文；
- Card interval 与 Paragraph element 的字节区间都必须落在所属 Book 区间内；
- Card 为 `container` 时，其自身 element 区间必须正确嵌套；Card 为 `milestone` 时只校验 anchor 与派生 interval，不把 interval 当作 XML 父元素；
- 任一父子关系不唯一时，map 验证失败。

## 2. Structure Mapping 方法

### 2.1 两阶段架构

结构发现与 Candidate 正文读取必须分离：

| 阶段 | 目的 | 可读取内容 | 可生成内容 | 是否属于 Candidate Run |
| --- | --- | --- | --- | --- |
| Structure Mapping Preflight | 发现 XML 元素、属性、locator 与字节边界 | 可在另行授权下扫描 XML 结构；character data 必须丢弃，不得输出或分析 | 仅 `book_structure_map.yaml` | 否 |
| Candidate Runtime | 执行已批准的有限任务 | 只可读取 validated map 指定的获批 Book 字节区间 | 隔离的 candidate 产物 | 是 |

Structure Mapping Preflight 可以为了建立全书结构表顺序扫描 English raw，但必须由独立的预检身份执行，并遵守：

- 只处理 XML start/end event、namespace、attribute 与字节位置；
- character data handler 不得缓存、记录、输出、发送给模型或用于任何语义判断；
- 不调用模型；
- 不生成文本片段或 normalized 文件；
- 不接触 Greek raw；
- 不与任何 Candidate Run 共用 `run_id`；
- map 生成完成后接受独立机械验证，状态达到 `validated` 才可被运行引用。

Candidate Runtime 绝不能在启动后重新扫描全书来寻找 Book 容器，也不能把“读取到 EOF 后再确认范围”作为容错路径。

### 2.2 XML 层级检查

Structure Mapping Preflight 必须使用 namespace-aware、非恢复模式的 XML parser，并按以下顺序检查：

1. 严格 UTF-8 解码与 XML well-formedness；
2. root 精确为 `{http://www.tei-c.org/ns/1.0}TEI`；
3. 定位 `tei:teiHeader` 中的 CTS `refsDecl/cRefPattern`，确认原生层级为 `book.card`；
4. 根据 cRefPattern 的 match／replacement 规则形成 Book 与 Card 的候选结构 selector；
5. 在 `tei:text/tei:body` 内将 selector 与实际 element QName、ancestor path 和 attributes 对齐；
6. 验证每个 Book 只有一个匹配容器；
7. 在每个 Book 内验证 Card anchors；
8. 在已确认 Book 内枚举合格 `tei:p`，建立父子关系与字节边界；
9. 完成全局计数、顺序、唯一性、嵌套与范围检查；
10. 只在全部检查通过后写出 `mapping_status: validated`。

禁止使用以下宽松发现规则：

- 仅按 local name 匹配、忽略 TEI namespace；
- 仅按 `@n` 值猜测层级；
- 在 cRefPattern 解析失败后自动改用模糊 XPath；
- 把任意 `div[1]`、第一个 `@n="1"` 或第一个数字 milestone 当作 Book 1；
- 将 line milestone 当成 `book.card`；
- XML 错误恢复、静默跳过未知节点或以文本内容辅助猜测容器。

若 cRefPattern、element path 与实际层级不能形成唯一映射，正确结果是阻断，不是 fallback。

### 2.3 TEI element 类型规则

map 不应在本规范阶段预先假定 raw 中 Book 或 Card 的具体标签；实际 QName 必须由未来 Structure Mapping Preflight 以 cRefPattern 和 XML 层级证据确定。允许进入 validated map 的结构类型如下：

| 结构层 | 合法识别依据 | 禁止依据 |
| --- | --- | --- |
| Book | TEI namespace QName + cRefPattern 对应层级 + 固定 ancestor path + Book attribute | local-name、文档位置或 `@n` 单独猜测 |
| Card | TEI namespace QName + cRefPattern 对应层级 + Card attribute／unit + 所属 Book + `representation_kind` | 任意数字 milestone、印刷 line 或顺序推算 |
| Paragraph | 精确 `tei:p` QName + 已映射 Book ancestor + body 内容域规则 | 文本换行、空行、句号或模型分段 |

若实际 Book 使用 `tei:div`、Card 使用 `tei:milestone`、`tei:pb` 或其他 TEI element，map 必须记录实际 QName 和完整 selector；不得因为本规范列举了常见类型就直接选用其中之一。

### 2.4 Attribute 规则

所有用于结构识别的 attributes 必须：

- 以 QName 和 namespace 记录，不依赖未声明前缀；
- 保存 raw lexical value 与规范化 value；
- 明确其角色：`level_discriminator`、`native_locator_value` 或 `ancillary_metadata`；
- 由 cRefPattern、固定 XML 路径或两者共同支持；
- 在同一层级内保持一致，不能对个别 Book 静默改用另一 attribute；
- 缺失、重复、非预期格式或多值歧义时阻断。

可持久化的 attribute value 必须限制在结构白名单：locator 值、level discriminator、namespace binding 以及安全解析片段所必需的 `xml:*` 继承值。不得把 `@title`、`@desc`、`@ana`、`@note` 或其他可能承载散文／语义内容的任意 attributes 整体复制进 map；如未列入白名单，map 只能记录 attribute QName 的存在性或返回阻断。

数值规范化只用于比较和生成 locator，不修改 raw：

```yaml
raw_value: "<source lexical value>"
normalized_integer: <positive integer>
normalization_effect: metadata_only
raw_xml_modified: false
```

Book 必须最终规范化为唯一的 `1..24`。Card 必须规范化为卷内唯一的正整数并按文档顺序递增，但不要求连续。Paragraph 的派生序号只反映同一 Book 中合格 `tei:p` 的文档顺序，不声称是原生或 canonical locator。

### 2.5 Locator 映射

唯一原生 locator 组合为：

```text
book.card
```

map 必须分别保存：

```yaml
book:
  raw_value: "..."
  normalized_value: 1
card:
  raw_value: "..."
  normalized_value: 1
native_locator: "1.1"
native_locator_scheme: book.card
```

Paragraph 的 map-local ID 与原生 locator 必须分开：

```yaml
paragraph_id: B01-P0001
paragraph_id_authority: derived_structure_map_only
native_locator_span:
  start: "1.1"
  end: "1.1"
canonical_span: null
```

不得生成或推断 Greek `book.line`、English–Greek alignment、canonical line span 或虚构的 paragraph citation。Paragraph 跨 Card 时只登记一个原生 locator span，不修改源结构。

### 2.6 字节边界规则

所有 offsets 均以**原始文件 UTF-8 字节流**为基准，采用 zero-based、half-open 区间：

```text
[start_byte, end_byte_exclusive)
```

每个 Book 至少记录：

- `start_tag_start_byte`：Book 起始标签 `<` 的位置；
- `content_start_byte`：Book 起始标签闭合 `>` 后的第一个字节；
- `content_end_byte_exclusive`：Book 结束标签 `<` 的位置；
- `end_tag_end_byte_exclusive`：Book 结束标签 `>` 后的第一个字节；
- `slice_sha256`：完整 Book 元素字节片段的 SHA-256。

每个 Card 必须先确定 `representation_kind`，再按对应算法计算边界：

- `milestone`：记录 anchor 边界；内容 interval 从当前 anchor 结束处起，到同一 Book 内下一 Card anchor 起始处或 Book 内容结束处止；
- `container`：内容 interval 严格使用该 Card element 自身的 start/end element 边界，不得延伸到下一 sibling anchor；
- 其他或混合形式：返回 `BLOCKED_CARD_REPRESENTATION_UNSUPPORTED`，不得用 milestone 算法猜测。

每个 Paragraph 至少记录完整元素的起止字节；若 parser 无法提供可靠的 XML lexical boundaries，Structure Mapping Preflight 必须阻断，不能用字符数、行号或序列化后的 XML 长度代替原始字节位置。

结构 mapper 必须把 namespace-aware parser events 与 XML lexical byte scanner 交叉绑定。两者对 QName、嵌套深度或边界的判断不一致时，map 不得进入 `validated`。

### 2.7 XML 片段解析条件

Candidate reader 未来以 Book 字节片段作为唯一正文输入。validated map 必须同时记录：

- Book 元素处于作用域内的 namespace bindings；
- 继承的 `xml:lang`、`xml:base` 等会影响解析身份的 XML attributes；
- 是否存在 DTD、外部实体、内部实体或其他使独立片段无法安全解析的依赖；
- `fragment_parse_supported: true|false` 及理由。

运行时可以在内存中为 Book 片段添加最小 namespace wrapper，但该 wrapper：

- 只用于 XML well-formed parsing；
- 不得写入磁盘或登记为 source／normalized 文本；
- 不得增删或改写 Book 片段内的正文；
- 必须记录 wrapper template 的版本与摘要；
- 不得启用 DTD、外部实体或网络解析。

若 Book 片段依赖无法安全重建的上游 XML context，必须返回 `BLOCKED_BOUNDED_FRAGMENT_UNPARSABLE`，不能退回全文件解析。

## 3. Scope Validation 规则

### 3.1 “只读取 Book 1”的规范定义

“只读取 Book 1”必须同时满足三个层面：

| 层面 | 成功定义 |
| --- | --- |
| 输入授权 | 可信 range broker 只接受 validated map 中 Book 1 的获批区间；Candidate 只收到该区间的结果 |
| parser 可见字节 | Candidate parser 只接收 broker 输出的 Book 1 `[start_byte, end_byte_exclusive)` 内存片段及无正文 wrapper |
| 内容事件 | 只产生 Book 1 的 XML／character-data events；Book 2–24 的正文事件为 0 |

这里的“读取”指 Candidate 进程可见并交给 parser／模型的来源字节。Candidate／模型进程不得拥有完整 raw 的路径权限、文件描述符或第二访问通道；整个 `source/` 树对其必须不可读。只有独立、受信任的 range broker 可以打开 raw，并以 unbuffered `pread` 或语义等价的 fixed-offset／fixed-length API 返回获批片段。read audit 必须由 broker 或独立 syscall／sandbox 层产生，Candidate 自报日志不能单独构成范围证明。

若运行环境还要求证明底层操作系统或存储设备没有 page-cache read-ahead，普通文件 I/O 的应用层 audit 不足以提供该证明；该环境必须使用能对物理读取范围作保证的隔离 range service。无论采用哪一等级，Candidate 都不能直接打开完整 raw。

### 3.2 Candidate 前的来源身份验证

全文件 SHA-256 复算本身会读取 Book 2–24，因此不得在 Candidate Runtime 内执行。来源身份必须在运行外完成：

1. Structure Mapping Preflight 绑定完整 raw SHA-256、size、commit、path 与稳定 `source_object_id`；
2. 独立 map validator 必须对**同一个 immutable/content-addressed 对象句柄**复核这些值；普通 filesystem `read-only` 权限本身不构成不可变性证明；
3. validator 生成 attestation，至少绑定 `source_object_id`、full SHA-256、size、commit、mapping payload SHA-256、生成时间、有效期和 validator identity；
4. range broker 必须绑定同一 `source_object_id`，并拒绝路径重新解析到另一个对象；
5. Candidate 启动时只校验获批 map identity、attestation 与 Book 1 slice SHA-256；Candidate 不得直接看到或打开 source 对象；
6. attestation 过期、对象句柄变化、map payload 变化、source 不具备真正 immutable/content-addressed 语义，或 validator 与 broker 未绑定同一对象时，在传递 Book 1 片段前阻断。

不得为了满足 source snapshot checksum 门槛，在 Candidate 内再次顺序读取整份 XML。

### 3.3 有界读取算法

未来 Candidate reader 必须按以下顺序工作：

1. Orchestrator 加载获批 `book_structure_map.yaml`，不启动 Candidate；
2. 验证 `mapping_status: validated`、source ID、commit、full SHA-256、size、spec version、map checksum 与 validator attestation；
3. 唯一选择 `book_number: 1`，确认匹配数恰好为 1；
4. 检查 Book 1 完整元素边界有效且位于文件大小内；
5. 检查 Book 1 card allowlist 数量为 `1..24`，locator 唯一且只含 Book 1；
6. 检查 `fragment_parse_supported: true`；
7. Orchestrator 向 range broker 提交 source object identity、map identity 与唯一获批 range；
8. broker 以 exact range API 从 `start_tag_start_byte` 读取至 `end_tag_end_byte_exclusive`，并由 broker／独立层生成不可由 Candidate 改写的 read audit；
9. broker 校验实际返回字节数与 Book 1 `slice_sha256`；
10. Candidate 在无法读取 `source/` 的隔离环境中，只接收该内存片段及无正文 wrapper；
11. namespace-aware parser 确认根结构与 map 记录一致，且所有可见 Book locator 均为 `1`；
12. read audit 与 parser scope check 均通过后，才允许 Candidate task 接收 Book 1 character data。

以下行为一律禁止：

- 为寻找 Book 1 从 byte 0 顺序解析到 EOF；
- map 不可用时改用 XPath／regex／文本搜索 fallback；
- 读取全文件后只丢弃 Book 2–24；
- 把完整 raw path、文件描述符、mount 或可调用的通用文件读取工具交给 Candidate／模型进程；
- 先向模型发送全书再通过 prompt 要求“只分析 Book 1”；
- 因 parser buffer 不透明而假定范围没有越界；
- slice 校验失败后自动扩大 read range。

### 3.4 范围证明证据

未来运行的执行证据至少必须记录：

```yaml
structure_map_id: <validated map id>
structure_map_sha256: <map file checksum>
mapping_payload_sha256: <attested mapping payload checksum>
source_id: ODY-ENG-MURRAY1919
source_object_id: <immutable/content-addressed object id>
source_full_sha256_attested: dda5b206e332e56c570c1d92ea41e9a510339a454bc2ea90491788e34174a7e7
range_broker_id: <broker id and version>
read_audit_authority: range_broker | independent_syscall_monitor
selected_books: [1]
allowed_byte_ranges:
  - start_byte: <integer>
    end_byte_exclusive: <integer>
actual_read_calls:
  - offset: <integer>
    requested_bytes: <integer>
    returned_bytes: <integer>
actual_union_of_read_ranges: <exact half-open ranges>
bytes_outside_allowed_ranges: 0
parsed_book_values: [1]
parsed_card_locators: [<Book 1 allowlist subset>]
parsed_books_outside_scope: 0
character_data_events_outside_scope: 0
greek_raw_access_count: 0
```

Scope 验证只有在以下条件全部成立时为 `PASS`：

- Candidate／模型进程对完整 raw 与 `source/` 的直接访问能力为 0；
- read audit 由 range broker 或独立 syscall／sandbox 层产生，而不是仅由 Candidate 自报；
- actual read range 是 Book 1 allowed range 的子集，且解析任务所需时与完整 Book 1 range 相等；
- `bytes_outside_allowed_ranges = 0`；
- parser 只观察到一个 Book，规范化值为 `1`；
- 所有 Card locator 均来自 validated Book 1 allowlist；
- Book 2–24 的 start event、character data event 与模型输入均为 0；
- Greek raw open／read／parse／copy／模型注入次数均为 0；
- raw、map 与 wrapper 均未被写回或覆盖。

任一证据无法采集、字段为 unknown、reader 使用不透明缓冲，或观测值不满足上述条件时，结果必须为 `BLOCKED_SCOPE_PROOF_UNAVAILABLE` 或 `INVALIDATED_SCOPE_EXCEEDED`，不能记为 PASS。

### 3.5 阻断代码

Structure Mapping 或 Candidate preflight 至少支持以下明确阻断：

| code | 条件 |
| --- | --- |
| `BLOCKED_STRUCTURE_MAP_MISSING` | 没有 map 文件 |
| `BLOCKED_STRUCTURE_MAP_UNVALIDATED` | map 不是 `validated` |
| `BLOCKED_STRUCTURE_MAP_STALE` | map 与 source path／size／SHA-256／commit 不一致 |
| `BLOCKED_CREFPATTERN_UNRESOLVED` | CTS 层级规则无法唯一解析 |
| `BLOCKED_BOOK_CONTAINER_AMBIGUOUS` | Book selector 为 0 或多重匹配 |
| `BLOCKED_CARD_MAPPING_INVALID` | Card selector、顺序、唯一性或父级关系失败 |
| `BLOCKED_CARD_REPRESENTATION_UNSUPPORTED` | Card 不是可验证的 milestone 或 container 表示 |
| `BLOCKED_PARAGRAPH_MAPPING_INVALID` | Paragraph 归属或边界不确定 |
| `BLOCKED_BYTE_BOUNDARY_UNRELIABLE` | 无法获得原始 UTF-8 精确字节区间 |
| `BLOCKED_BOUNDED_FRAGMENT_UNPARSABLE` | Book 片段不能安全独立解析 |
| `BLOCKED_SOURCE_IDENTITY_UNVERIFIED` | 不可变来源身份或预检 attestation 无效 |
| `BLOCKED_SOURCE_OBJECT_NOT_IMMUTABLE` | source 只有普通只读权限，不能证明与 attested object 相同且不可变 |
| `BLOCKED_RANGE_BROKER_UNAVAILABLE` | 不能把完整 raw 与 Candidate 进程隔离 |
| `BLOCKED_BOUNDED_READER_UNAVAILABLE` | 运行环境不能提供 exact range reader |
| `BLOCKED_SCOPE_PROOF_UNAVAILABLE` | 无法生成完整范围读取证据 |

阻断后不得切换解析器继续同一 Run、扩大范围、读取到 EOF、忽略 map 错误或伪造成功。

## 4. Candidate Run 前置条件

### 4.1 硬性启动门槛

任何以 English TEI 为内容输入的 Candidate Run，在打开正文前必须满足：

1. `TEXT_STRUCTURE_MAPPING_SPEC.md` 已获项目批准并有明确版本；
2. 已由独立 Structure Mapping Preflight 生成 `book_structure_map.yaml`；
3. map 自身状态为 `validated`，且有独立 validator 记录；
4. map 与 `ODY-ENG-MURRAY1919` 的 path、size、commit 和完整 SHA-256 完全一致；
5. Book、Card、Paragraph selector、attribute 与 byte ranges 均无歧义；
6. 任务所需 Book 在 map 中唯一存在；
7. 获批 Card allowlist 可由 map 机械导出且不超过 task scope 上限；
8. range broker、bounded reader、fragment parser 与独立 read-audit 机制经过无正文测试夹具验证；
9. English source 仅取得该任务的 Candidate 资格，不被改写为 formal input；
10. Greek raw 保持 denylist，访问次数目标为 0；
11. source 对 Candidate 完全不可读，map 仅提供获批结构元数据，range broker 是 raw 的唯一读取者；输出根与正式 Analysis Layer 隔离；
12. 使用新的、未被占用且已获一次性授权的 Candidate Run ID。

### 4.2 无 validated map 时的决策

规则是绝对的：

```yaml
if_validated_structure_map_absent:
  candidate_run_may_start: false
  english_raw_may_be_opened_by_candidate: false
  fallback_structure_discovery_in_run: prohibited
  correct_result: blocked_before_content_read
```

`P0_ENGLISH_SOURCE_ACQUISITION_RESULT.md` 中的“24 Books / 288 Cards 技术验证通过”是 map 建立的来源证据，但不能替代含 selector、attributes、byte ranges 与 validator attestation 的 `book_structure_map.yaml`。

### 4.3 Run 001 的处理

`AC-20260811-STORYSTRUCT-001` 已为 `invalidated`，其 ID 永久保留，不得在修复后重启、覆盖或改写为成功。本文不修改其 manifest 或 execution report。

当结构 map 未来完成并通过验证后，若项目仍要执行同一有限任务，必须：

- 分配新的 `AC-YYYYMMDD-STORYSTRUCT-NNN`；
- 使用真实授权日期；
- 以 `retry_of_run_id: AC-20260811-STORYSTRUCT-001` 保留关系；
- 重新冻结 source snapshot、task scope、execution snapshot 与 structure map identity；
- 取得新的单次运行授权。

本规范的批准、map 的生成或 map 的验证都不自动创建、授权或执行该新运行。

## 5. 未来输出：`book_structure_map.yaml`

### 5.1 唯一规划输出

未来 Structure Mapping Preflight 需要生成：

```text
book_structure_map.yaml
```

本规范不决定其最终项目路径；路径必须在 Structure Mapping 实施计划中另行批准，且不得位于 raw 目录、正式 Analysis Layer 或某个 Candidate Run 的内容输出目录。map 是 source-derived technical metadata，必须与 raw 分离并保持只读引用关系。

本阶段不创建该文件。

### 5.2 必填顶层字段

`book_structure_map.yaml` 至少包含：

```yaml
schema_version: <semver>
specification: TEXT_STRUCTURE_MAPPING_SPEC.md
specification_sha256: <full sha256>
map_id: <stable id>
artifact_class: source_structure_map
authority: technical_mapping_only
contains_xml_character_data: false
contains_prose_bearing_attribute_payload: false
contains_literary_analysis: false
mapping_status: draft | mapped_unvalidated | validated | invalidated

source:
  source_id: ODY-ENG-MURRAY1919
  file_id: ODY-ENG-MURRAY1919-RAW-FULL-TEI
  raw_path: source/translations/en/ody-eng-murray1919/raw/ody-eng-murray1919__raw__full.xml
  fixed_upstream_commit: 790c84289edbdbe289dd7b752bfea29f0af4299d
  size_bytes: 870905
  sha256: dda5b206e332e56c570c1d92ea41e9a510339a454bc2ea90491788e34174a7e7
  encoding: UTF-8
  tei_namespace: http://www.tei-c.org/ns/1.0
  native_locator_scheme: book.card
  source_object_id: <immutable/content-addressed object id>
  source_object_immutability: required

mapper:
  implementation_id: <id>
  implementation_version: <version>
  parser_name: <name>
  parser_version: <version>
  lexical_scanner_version: <version>
  generated_at: <ISO-8601>
  model_invocations: 0
  character_data_persisted: false

locator_contract:
  c_ref_patterns: <structure-only representation>
  book_mapping: <QName, path and attribute rules>
  card_mapping: <QName, path and attribute rules>
  paragraph_mapping: <QName, inclusion and exclusion rules>

xml_context:
  namespace_bindings: <map>
  inherited_xml_attributes: <map>
  dtd_or_entity_dependencies: <list>
  fragment_parse_supported: <boolean>
  fragment_parse_blocker: <null or code>

books: <ordered Book records>

validation:
  validator_id: <id>
  validator_version: <version>
  validated_at: <ISO-8601>
  attestation_id: <id>
  attestation_generated_at: <ISO-8601>
  attestation_expires_at: <ISO-8601 or explicit non-expiring policy>
  source_object_id_match: <pass|fail>
  mapping_payload_canonicalization: CTDE-MAP-C14N-1
  mapping_payload_sha256: <sha256 over defined non-validation payload>
  source_identity_match: <pass|fail>
  xml_hierarchy_check: <pass|fail>
  locator_check: <pass|fail>
  byte_boundary_check: <pass|fail>
  parent_child_check: <pass|fail>
  no_text_payload_check: <pass|fail>
  overall_result: <pass|fail>
  blockers: <list>
```

`mapping_payload_sha256` 必须使用固定算法 `CTDE-MAP-C14N-1`，不得对实现默认序列化结果直接取摘要：

1. 按 YAML 1.2 Core Schema 以 safe mode 严格解析单文档 YAML；关闭 YAML 1.1 implicit resolvers 与 timestamp implicit resolution；duplicate keys、custom tags、merge keys、anchors、aliases 和多文档 YAML 均为非法；
2. 从解析后的顶层 mapping 中删除整个 `validation` key/value；除此之外不得删除、补入或重排语义数据；
3. 剩余数据必须可无损表示为 JSON-compatible tree：mapping keys 全部为字符串，values 只允许 `null`、boolean、base-10 integer、Unicode string、ordered array 或 mapping；禁止 float、timestamp、binary 与实现特有类型；源 YAML 中 null 只能写为 `null`，boolean 只能写为 `true|false`，integer 只能匹配 `0|-?[1-9][0-9]*`，所有 string scalars 必须使用双引号，从词法层消除 `yes/on/date/leading-zero` 等隐式解析差异；
4. 将 tree 序列化为 canonical JSON bytes：mapping keys 按 Unicode code point 升序；array 保持原顺序；对象与数组使用 `,`，key/value 使用 `:`；不输出空白、换行或 BOM；
5. string 采用 JSON 双引号：U+0022 固定编码为 `\"`，U+005C 固定编码为 `\\`，所有 U+0000–U+001F control characters 一律编码为 `\u00XX`（`XX` 为两位大写十六进制，不得使用 `\b`、`\t`、`\n`、`\f`、`\r` 简写）；其他 Unicode code points 直接以 UTF-8 编码，不执行 Unicode normalization；拒绝 U+D800–U+DFFF lone surrogate code points；boolean 与 `null` 使用小写；integer 使用无前导零的十进制形式，零只能写作 `0`；
6. 对 canonical JSON bytes 计算 SHA-256，保存为 64 位小写十六进制 `validation.mapping_payload_sha256`；
7. validator、range broker 与运行前 Orchestrator 都必须按 `CTDE-MAP-C14N-1` 独立复算，并与 attestation 中的同名摘要一致。

validator 写入或更新顶层 `validation` block 不会改变上述 payload digest。最终 `book_structure_map.yaml` 文件的普通字节级 SHA-256 是另一项身份：必须在 validator 完成写入后计算，并保存于 Candidate 授权记录／run manifest，不得写回 map 自身形成递归摘要。

### 5.3 每个 Book 的必填结构

每个 `books[]` 记录至少包含：

```yaml
- book_number: 1
  raw_book_value: "<source value>"
  element_qname: "{http://www.tei-c.org/ns/1.0}<local-name>"
  element_path: <namespace-aware structural path>
  element_occurrence: <positive integer>
  attributes_used: <QName/value records>
  start_tag_start_byte: <integer>
  content_start_byte: <integer>
  content_end_byte_exclusive: <integer>
  end_tag_end_byte_exclusive: <integer>
  slice_size_bytes: <integer>
  slice_sha256: <sha256>
  fragment_parse_supported: <boolean>
  card_count: <integer>
  paragraph_count: <integer>
  cards: <ordered Card records>
  paragraphs: <ordered Paragraph records>
  mapping_ambiguities: []
```

Card record 至少包含 native locator、`representation_kind`、element／attribute 证据、anchor／container 与 interval byte ranges、所属 Book、document order 和 overlapped paragraph IDs。Paragraph record 至少包含 derived ID、QName、父级 Book、native Card span、完整 element byte range、跨 Card 标记、ancillary exclusion 状态与歧义代码。Paragraph 与 Card 的关联字段必须使用 `overlaps_card_ids`／`native_locator_span`，不得伪装成单一 Card 父子关系。

### 5.4 内容最小化与禁止字段

map 可以保存：

- QName、namespace、XPath-like structural path；
- 白名单内 attributes 的 QName 及结构识别所需值；
- locator、计数、顺序、byte offsets、sizes 与 hashes；
- parent／child IDs、验证结果、歧义代码与工具版本。

map 禁止保存：

- XML character data、正文、摘录或句子；
- Book／Card／Paragraph 内容摘要；
- 人物、事件、地点、物件、主题、母题或象征；
- story beat、story structure、剧情或改编字段；
- prompt、模型输出或 embeddings；
- Greek raw 内容、Greek `book.line` 或 English–Greek alignment；
- normalized、cleaned、reordered 或 repaired 文本。

`contains_xml_character_data`、`contains_prose_bearing_attribute_payload` 与 `contains_literary_analysis` 必须固定为 `false`。这里的“无正文 payload”专指不持久化 XML character data，也不持久化可能承载散文／语义内容的非白名单 attribute values；必要的 locator、namespace 与 XML 继承结构值仍属于可审计结构元数据。任何禁止字段出现时，map 验证失败。

### 5.5 Map 验收条件

`mapping_status` 只有在以下条件全部通过后才能为 `validated`：

- source ID、path、size、commit 与 SHA-256 精确匹配；
- XML root、namespace 与 `book.card` cRefPattern 通过；
- Book 集合与既有 24 Books 技术验证一致，Book `1..24` 各唯一一次；
- Card 总数与既有 288 Cards 技术验证一致；
- 每卷 Card 为正整数、唯一、按文档顺序递增，不强制连续；
- 每个 Card 的 `representation_kind` 已确定，milestone／container 边界算法与实际结构一致；
- 所有合格 Paragraph 均有唯一 Book 归属和确定 byte range；
- 所有 Book containment、Card 表示边界与 Paragraph-to-Card overlap 关系合法；
- 每个 Book slice hash 可由 raw exact range 复算；
- fragment parse 条件明确；
- validator 与 mapper 的结构结果一致；
- map 不含正文或文学分析字段；
- Greek raw 访问次数为 0；
- English raw 写入次数为 0；
- 模型调用次数为 0。

任何一项失败时，map 必须保持 `mapped_unvalidated` 或转为 `invalidated`，并列出 blockers；不得为启动 Candidate 而手工改写为 `validated`。

## 6. 本阶段结论与未执行动作

Phase 2-C-R 的架构结论是：未来 Candidate 范围执行必须依赖**先生成、后独立验证、与 immutable/content-addressed 来源对象严格绑定**的 `book_structure_map.yaml`。只有可信 range broker 可以读取 raw；Candidate 本身只能接收 broker 提供的 Book 1 exact-range 内存片段，不能访问完整 source、承担全书结构发现，也不能在 map 失效时回退到 EOF 扫描。

```yaml
phase: Phase 2-C-R
task: Candidate Scope Enforcement Repair
document: TEXT_STRUCTURE_MAPPING_SPEC.md
document_status: ready_for_review
current_effect: specification_only

failed_run_id: AC-20260811-STORYSTRUCT-001
failed_run_status_preserved: BLOCKED_SCOPE_ENFORCEMENT_FAILED / invalidated
failed_run_reusable: false

required_future_artifact: book_structure_map.yaml
required_future_artifact_created_this_task: false
validated_structure_map_available: false
candidate_run_may_start_without_validated_map: false
fallback_full_file_scan_in_candidate: prohibited
candidate_direct_source_access: prohibited
trusted_range_broker_required: true

english_raw_opened_this_task: false
english_raw_modified_this_task: false
greek_raw_access_count_this_task: 0
candidate_runs_executed_this_task: 0
model_invocations_this_task: 0
content_analysis_created_this_task: 0
character_database_created_this_task: 0
event_database_created_this_task: 0
theme_database_created_this_task: 0
adaptation_or_script_outputs_created_this_task: 0
normalized_or_alignment_files_created_this_task: 0
source_or_status_files_modified_this_task: 0
```

本文完成只表示结构映射与范围证明规范已形成可审查设计。它不生成 structure map，不修复或重跑 Run 001，不授权任何正文读取，也不解除 English、Greek 或正式 Phase 2 Gate。
