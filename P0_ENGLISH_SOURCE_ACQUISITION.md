# 《奥德赛》Perseus English TEI Source Acquisition Plan

> 项目：Classic-to-Drama Engine  
> 阶段：Phase 1-F / P0-4-A  
> 文档类型：单来源获取计划  
> 文档状态：`ready_for_review`  
> 执行状态：`not_started`  
> 日期：2026-08-10  
> 当前 English 状态：`pending / pending`  
> 当前 Greek 状态：`acquired / verification_failed`  
> 当前 Analysis Gate：`C_reference_only`

## 0. 目的与边界

本文只定义 Perseus English TEI（Murray 1919，`perseus-eng3`）的单来源获取、落盘、登记、SHA-256 与非内容型验证计划，不执行任何获取或数据处理。

本文不授权、也不执行：

- 下载 English TEI、CTS metadata 或其他外部字节资产；
- 创建 `source/translations/en/ody-eng-murray1919/` 或任何占位目录、空文件；
- 创建具体 `SOURCE_RECORD`、填写获取日期、文件大小或 SHA-256；
- 读取、提取、摘要、翻译或解释《奥德赛》正文；
- 创建 normalized 文件、passage、索引、向量、Greek–English 对齐或 locator 映射；
- 创建人物、剧情、事件、改编、剧本或制作数据；
- 修改 Greek raw XML、Greek checksum、Greek exception、Greek verification 状态或 Analysis Gate；
- 把本计划等同于 English 已获取、已验证、已批准或 Phase 2 已获授权。

## 1. English TEI 来源确认

### 1.1 唯一来源身份

| 项目 | 已锁定值 |
| --- | --- |
| `source_id` | `ODY-ENG-MURRAY1919` |
| `file_id` | `ODY-ENG-MURRAY1919-RAW-FULL-TEI` |
| title | *The Odyssey, Volumes 1–2* |
| author | Homer（传统归属；实际记录使用项目统一表述 `Homer (traditional attribution)`） |
| edition | A. T. Murray 英译，William Heinemann / G. P. Putnam's Sons，1919；CTS version `perseus-eng3` |
| translator | Augustus Taber Murray（A. T. Murray） |
| language | `en` |
| provider | 版本身份：Perseus Digital Library / Scaife ATLAS；物理分发：`PerseusDL/canonical-greekLit` |
| canonical URL | `https://atlas.perseus.tufts.edu/library/urn%3Acts%3AgreekLit%3Atlg0012.tlg002.perseus-eng3/` |
| canonical CTS URN | `urn:cts:greekLit:tlg0012.tlg002.perseus-eng3` |
| repository | `https://github.com/PerseusDL/canonical-greekLit` |
| repository path | `data/tlg0012/tlg002/tlg0012.tlg002.perseus-eng3.xml` |
| planned file format | XML；实际获取后必须验证为可解析的 TEI XML，预期媒体类型为 `application/tei+xml` |
| intended usage | `primary_working_text` |
| native citation scheme | `book.card`；不是 `book.line` |

本计划只针对 `perseus-eng3`。不得用 legacy Catalog 中的 `eng1`、Butler / Gutenberg `PG1727`、Perseus `perseus-eng4` 或其他英译替代，也不得共用其 `source_id`、locator 或登记记录。

### 1.2 固定 commit 策略

P0-3-B 已锁定并使用以下完整 40 位 commit，且已确认 P0 四个核心仓库路径在该 commit 下均存在：

```text
790c84289edbdbe289dd7b752bfea29f0af4299d
```

English TEI 获取阶段必须复用这一 commit，不重新解析 `main`、`master`、`latest` 或其他浮动引用，也不得选择与 Greek TEI 不同的 commit。

计划中的唯一不可变获取地址为：

```text
https://raw.githubusercontent.com/PerseusDL/canonical-greekLit/790c84289edbdbe289dd7b752bfea29f0af4299d/data/tlg0012/tlg002/tlg0012.tlg002.perseus-eng3.xml
```

实际获取前仍须执行非内容型 preflight：确认完整 commit 格式、repository path 在该 commit 下存在，并确认响应对象是目标 raw 文件而不是 Scaife HTML、GitHub 浏览器页面、登录页、错误页或重定向包装页。该 preflight 不得改变已锁定 commit。

## 2. 目标保存路径

### 2.1 唯一批准路径

English TEI 的唯一完整目标路径是：

```text
source/translations/en/ody-eng-murray1919/raw/ody-eng-murray1919__raw__full.xml
```

以 `source/` 为逻辑根时，具体 `SOURCE_RECORD.file_path` 使用：

```text
translations/en/ody-eng-murray1919/raw/ody-eng-murray1919__raw__full.xml
```

未来执行时只创建该 raw 文件实际需要的父目录；传输成功前不得创建正式文件，失败的临时文件不得冒充来源资产。

### 2.2 `source/original_text/eng/` 的规范映射

本阶段需求中写出的 `source/original_text/eng/` 与既有项目契约存在两处冲突：

1. English Murray 1919 是译本，必须进入固定一级目录 `translations/`，不能进入承载原作语言文本的 `original_text/`；
2. 项目已锁定英语语言目录为 `en/`，不得另建 `eng/` 别名。

因此，本计划将该表述解析为“English 来源的目标保存位置”这一语义要求，并依照 `01_SOURCE_PACKAGE_STRUCTURE.md`、`02_SOURCE_ACQUISITION_PLAN.md`、`03_SOURCE_ACQUISITION_EXECUTION_CHECKLIST.md`、`P0_SOURCE_REGISTRY.md` 与 `SOURCE_DIRECTORY_INITIALIZATION.md` 的共同约束，继续使用第 2.1 节的唯一物理路径。

以下路径均禁止创建：

```text
source/original_text/eng/
source/original_text/en/
source/translations/eng/
```

### 2.3 raw 不可变规则

未来取得的 raw 文件必须保持 provider 返回的原始字节：

- 不统一换行；
- 不移除 BOM；
- 不重编码；
- 不执行 Unicode NFC；
- 不修改缩进、XML declaration、TEI header、标签、文本或 locator；
- 不因验证结果就地修补、重排或覆盖；
- 不在本步骤创建 normalized 副本。

## 3. `SOURCE_RECORD` 登记流程

### 3.1 记录路径与创建时点

只有 English raw 字节真实到达批准路径后，才创建一份具体文件记录：

```text
source/metadata/records/ody-eng-murray1919-raw-full-tei.source.yaml
```

一个 raw 文件对应一个 `file_id`、一个 `SOURCE_RECORD` 和一个真实 SHA-256。本文计划阶段不创建该记录或任何占位记录。

### 3.2 13 个统一字段的填写规则

具体记录以 `SOURCE_RECORD_TEMPLATE.yaml` 为基础，完整填写全部 13 个字段：

| 字段 | 获取后的填写规则 |
| --- | --- |
| `source_id` | 固定为 `ODY-ENG-MURRAY1919` |
| `title` | 以 Scaife canonical identity 与实际 TEI header 交叉核验后的正式题名填写，不凭计划猜测覆盖上游身份 |
| `author` | 使用项目统一表述 `Homer (traditional attribution)` |
| `edition` | 记录 A. T. Murray 英译、Heinemann / Putnam、1919、CTS version `perseus-eng3`，并与 TEI header 核验 |
| `language` | `en`；必须与实际 TEI 的语言声明一致 |
| `provider` | Perseus Digital Library / Scaife ATLAS；物理分发记录 `PerseusDL/canonical-greekLit` |
| `url` | 写入包含完整固定 commit 的实际 raw 获取地址，不写 canonical 页面或浮动分支地址 |
| `access_date` | 实际获取日，格式 `YYYY-MM-DD`；本文日期不得预填为未来获取日 |
| `license` | 获取时同时核验固定 commit 的仓库许可与文件级 TEI header；填写 SPDX ID、`NOASSERTION` 或已批准的 `LicenseRef-*`，不得从 Greek 记录无条件复制 |
| `file_type` | 格式验证通过后填写 `tei_xml` |
| `intended_usage` | 固定为 `primary_working_text` |
| `status` | raw 字节、实际 URL、身份和 checksum 完成登记后为 `acquired`；技术验证通过后为 `verified`；人工批准后才能为 `approved`；失败时使用既有 `blocked` 或保留 `acquired` 并另记验证失败 |
| `checksum` | 仅根据最终落盘 raw 字节计算，格式 `sha256:<64位小写十六进制>`；获取前保持 `null` |

同时按既有完整记录契约填写扩展字段：

- `schema_version: c2d.source-record.v1`；
- `file_id: ODY-ENG-MURRAY1919-RAW-FULL-TEI`；
- `file_path: translations/en/ody-eng-murray1919/raw/ody-eng-murray1919__raw__full.xml`；
- 经实际检查确认的 `media_type` 与 `bytes`；
- `role: primary_working_text`；
- `state: raw`；
- 含时区的实际 `retrieved_at`；
- `canonical_url`；
- `identity.cts_urn: urn:cts:greekLit:tlg0012.tlg002.perseus-eng3`；
- `identity.citation_scheme: book.card`；
- `contributors.translator: Augustus Taber Murray`；
- `provider_identity.repository`、完整 `upstream_commit`、`upstream_path`，以及能够可靠取得时的 Git blob 交叉身份；
- `derivation.inputs: []` 与 `transformation_log_ref: null`，表明这是未转换的 raw；
- 实际发现的 `known_issues`；
- 逐项 `verification` 结果；
- `record_status: draft`，技术验证后才进入 `verified`，人工批准后才进入 `approved`。

### 3.3 状态更新规则

计划中的生命周期为：

```text
SOURCE_RECORD.status:        pending -> acquired -> verified -> approved
SOURCE_RECORD.record_status:            draft    -> verified -> approved
Registry acquisition_status: pending -> acquired
Registry verification_status: pending -> verified -> approved
```

规则如下：

- 未取得真实字节时，English 在 `P0_SOURCE_REGISTRY.md` 中继续保持 `pending / pending`；
- raw 字节成功落盘但尚未完成验证时，只能进入 `acquired / pending`；
- 验证失败时，注册表使用既有 `verification_failed`，具体记录保持 `status: acquired`、`record_status: draft` 并保存失败明细，或在无法可靠建立文件身份时使用模板允许的 `blocked`；
- 所有技术检查通过后，才可进入 `acquired / verified`；
- `approved` 必须来自独立人工批准，不能由下载脚本自动赋值；
- English 的状态更新不得修改 Greek 的 `acquired / verification_failed`、Greek exception 文档或 Analysis Gate。

未来执行还应同步：

- `source/metadata/checksums/checksums.sha256` 中的 English 单文件摘要行；
- `source/metadata/logs/acquisition_log.jsonl` 中的实际执行事件；
- `source/metadata/sources.yaml` 中的 English 来源索引；
- `source/metadata/quality/source_quality_report.md` 中的 English 验证结果；
- `P0_SOURCE_REGISTRY.md` 的 English 单行；
- `03_SOURCE_ACQUISITION_EXECUTION_CHECKLIST.md` 中 P0-03、P0-06、P0-07 及分文件验证矩阵里有实际证据支持的对应项。

CTS textgroup 与 work metadata 尚未获取时，不得把 P0-04、P0-05 或完整的四文件交叉身份检查标为完成。

## 4. SHA-256 与验证流程

### 4.1 原始落盘与 SHA-256

未来执行顺序固定为：

1. 复核 `source_id`、`file_id`、固定 commit、upstream path、不可变 URL 与目标路径唯一一致；
2. 将响应字节先写入目标目录中的临时文件；
3. 确认传输成功、文件为普通文件且大小大于 0，并排除 HTML、错误页和包装页；
4. 不改变任何字节，原子命名为批准的 raw 文件名；
5. 对最终 raw 文件实际字节计算 SHA-256；
6. 将 `sha256:<digest>` 写入具体 `SOURCE_RECORD.checksum`；
7. 将同一摘要与相对路径写入 `source/metadata/checksums/checksums.sha256`：

```text
<64-lowercase-hex>  translations/en/ody-eng-murray1919/raw/ody-eng-murray1919__raw__full.xml
```

8. 使用第二次独立重算复核摘要，并确认 raw 文件、YAML 记录与 checksum 索引三者完全一致；
9. 记录实际字节数、获取日期和含时区的获取时间。

不得根据 canonical 网页、Git blob ID、HTTP header、远程声明或 Greek 文件摘要推算 English SHA-256。本文不预填任何 English 摘要。

### 4.2 非内容型完整性与格式验证

至少执行以下检查：

- [ ] 目标文件真实存在、是普通文件且大小大于 0；
- [ ] 文件不是 Scaife HTML、GitHub HTML、登录页、错误页、限流页或重定向包装页；
- [ ] XML 可由 namespace-aware 标准 XML parser 严格完整解析；
- [ ] XML declaration 与实际字节编码一致，严格解码不以 replacement mode 隐藏错误；
- [ ] root 与 namespace 符合 TEI 身份；
- [ ] TEI header 中题名、Homer 传统归属、A. T. Murray 英译、Heinemann / Putnam、1919 与计划身份不冲突；
- [ ] 语言身份为 English / `en`；
- [ ] CTS identity 精确等于 `urn:cts:greekLit:tlg0012.tlg002.perseus-eng3`；
- [ ] citation scheme 精确识别为 `book.card`；
- [ ] 恰有 Book 1–24，编号不缺失、不重复且顺序正确；
- [ ] 每卷 card locator 可解析、卷内唯一并保持上游原生文档顺序；
- [ ] Book/Line 检查明确记录为 `not_applicable_book_card_source`；
- [ ] 未把 card 数字、card 连续性、XML 节点序号、文件行号或页面 chunk 冒充 Greek line；
- [ ] English–Greek line range alignment 明确保持 `not_started`；
- [ ] 文件的完整 commit 与 Greek 及未来两个 CTS metadata 的计划 commit 一致；
- [ ] `file -> file_id -> SOURCE_RECORD -> checksums.sha256` 一对一闭环成立；
- [ ] SHA-256 的两次重算、具体记录和 checksum 索引完全一致；
- [ ] raw 文件未因验证而发生任何字节变化；
- [ ] 所有失败、缺口、重复、乱序、身份冲突或未知结构均进入质量报告，不被静默忽略。

获取 English TEI 时只能验证该文件自身以及与既有 Greek provider/commit 身份的非内容型关系。两个 CTS metadata 文件仍为 `pending` 时，完整的四文件 CTS 交叉身份检查必须保持未完成。

## 5. English TEI 与 Greek TEI 的关系

### 5.1 职责分离

| 来源 | 项目角色 | 原生定位 | 后续用途边界 |
| --- | --- | --- | --- |
| Greek `ODY-GRC-MURRAY1919` / `perseus-grc2` | `canonical_anchor`，规范引用脊柱 | `book.line` | 提供所有规范引用的作品、卷、行坐标；当前因结构异常仅可作为来源证据与引用锚点 |
| English `ODY-ENG-MURRAY1919` / `perseus-eng3` | `primary_working_text`，AI 工作文本 | `book.card` | 在其自身验证、完整 Source Gate 与 Phase 2 授权完成后，作为 AI 的主要可读工作文本 |

“Greek 用于引用脊柱、English 用于 AI 工作文本”表示职责分工，不表示当前已授权内容分析。English 单文件获取成功也不能绕过当前 `C_reference_only` Gate。

### 5.2 关系规则

- Greek 与 English 必须来自同一 `canonical-greekLit` commit，以固定同一数字来源快照；同 commit 只证明版本快照关系，不自动证明 passage 对齐关系；
- 所有未来的 `canonical_span` 只能使用 Greek `perseus-grc2` 的 `book.line` URN；
- English 只保存其原生 `book.card` 身份，例如未来的 `english_card_urn`；不得创建 `english_line`；
- English card 与 Greek line range 的映射属于后续独立 alignment 阶段，不属于获取或本计划；
- 当前 Greek Book 3、Book 14 locator 顺序异常与 Book 16 locator 缺失不能由 English 文本补写、推断、重排或反向修复；
- English 不得替代 Greek 成为 canonical anchor，也不得改变 Greek raw、checksum、异常分类或验证状态；
- 在 Greek block、P0 最小来源集、Gate S1 和 Phase 2 启动条件未全部按批准路径完成前，English 即使技术验证通过，也不得被分析程序读取为正式 analysis corpus。

### 5.3 当前 Gate 影响

当前 Greek 状态与 Gate 保持：

```yaml
greek_acquisition_status: acquired
greek_verification_status: verification_failed
greek_analysis_use: reference_only
blocked_structure_validation: true
```

本 English 获取计划不解除 `BLOCKED_STRUCTURE_VALIDATION`。未来 English 获取与验证可以作为 P0 独立进度推进，但它既不能关闭 Greek 三项 exception，也不能单独启动 normalization、alignment 或 Phase 2 analysis。

## 6. 完成标准与阻断条件

### 6.1 P0-4-A 计划文档完成标准

只有以下条件全部满足，才认为本计划文档完成：

- [x] English 的 `source_id`、`file_id`、title、edition、translator、provider、canonical URL、CTS URN、repository 与 upstream path 唯一明确；
- [x] fixed commit 策略明确复用 P0-3-B 已锁定的完整 commit；
- [x] 唯一 raw 路径与既有 P0 注册表及目录契约一致；
- [x] `source/original_text/eng/` 与批准路径之间的冲突已经显式处置，没有建立第二套目录；
- [x] `SOURCE_RECORD`、SHA-256、非内容型验证、状态同步和失败处置流程完整；
- [x] Greek 引用脊柱与 English AI 工作文本的角色和 locator 权限已经分离；
- [x] English 获取完成标准与阻断条件已经定义；
- [x] 本轮下载外部字节资产为 0，新增具体来源记录为 0，新增真实 checksum 为 0；
- [x] English 与两个 CTS metadata 继续保持 `pending / pending / checksum null`；
- [x] Greek raw、checksum、状态和 Analysis Gate 未改变；
- [x] 未创建 normalized、alignment、内容分析、人物、剧情、改编或剧本数据。

### 6.2 未来 English TEI 单来源获取完成标准

未来执行阶段只有以下条件全部满足，才认为 English TEI 单来源获取完成：

- [ ] 使用固定 commit `790c84289edbdbe289dd7b752bfea29f0af4299d` 下的唯一 upstream path 和不可变 raw URL；
- [ ] 实际传输的外部字节资产恰好为 English TEI 这 1 个文件；
- [ ] raw XML 位于第 2.1 节批准路径，非空、非 HTML、未被修改；
- [ ] 具体 `SOURCE_RECORD` 恰好新增 1 份，13 个统一字段及必要扩展字段完整；
- [ ] 本次执行新增的真实 SHA-256 恰好为 English raw 的 1 个摘要，且基于最终落盘字节计算；
- [ ] XML、编码、TEI namespace/header、English / `en`、Murray 1919 与 `perseus-eng3` 身份检查通过；
- [ ] Book 1–24 与原生 `book.card` 结构检查通过，Book/Line 明确为不适用；
- [ ] 两次 SHA-256 重算、`SOURCE_RECORD` 与 checksum 索引完全一致；
- [ ] English 注册表状态按真实证据更新，所有异常均有明确记录；
- [ ] `unresolved_english_blockers` 为 0；技术验证完成后获得独立人工批准，具体记录达到 `status: approved / record_status: approved`，注册表达到 `acquisition_status: acquired / verification_status: approved`；
- [ ] Greek 状态保持 `acquired / verification_failed`，两个 CTS metadata 项继续保持 `pending / pending / checksum null`；
- [ ] 没有 normalized、alignment、分析、人物、剧情、改编或剧本产物。

技术验证通过可以把 English 推进到 `verified`，但最终 `approved` 仍需独立人工批准。English 单来源完成不等于 P0 四文件、Gate S1-C、Gate S1-D、总 Gate S1 或 Phase 2 完成。

### 6.3 阻断条件

出现以下任一情况时，不得把 English 标为 `verified` 或 `approved`：

- 固定 commit 不是完整 40 位 SHA、与 Greek 不同，或 retrieval URL 使用浮动分支；
- upstream path 不能在固定 commit 下可靠确认，或实际取得对象不是目标 `perseus-eng3` raw 文件；
- 创建了 `source/original_text/eng/` 等第二套目录，或目标路径与 P0 注册表不一致；
- 正式文件不存在、为零字节、被截断，或是 HTML、错误页、登录页、限流页、重定向／GitHub 包装页；
- XML 无法严格解析，编码声明与实际字节不符，TEI root／namespace 不符；
- title、author、translator、edition、language 或 CTS identity 与 Murray 1919 `perseus-eng3` 冲突；
- 不能可靠确认 24 Book 或原生 `book.card` 结构；
- card 被当作 Greek line，或获取阶段开始进行 Greek–English 对齐；
- checksum 不是根据最终 raw 字节计算、两次重算不一致，或记录／索引值不一致；
- raw 在获取或验证中被清洗、改码、重排、修补或覆盖；
- 具体文件与 `file_id`、`SOURCE_RECORD` 或 checksum 索引不能形成一对一闭环；
- 未处理异常被忽略，或用猜测值、占位文件、伪造 checksum 制造成功；
- English 被用于填补 Greek locator 异常、解除 Greek block 或提前启动 analysis。

失败处置必须反映真实状态：

- 未取得可靠字节：P0 注册表保持 `pending / pending`，执行任务可标为 `blocked` 并记录原因；不得为此创建占位 `SOURCE_RECORD`，也不得把未在注册表契约中定义的 `blocked` 擅自写入注册表两列；
- 字节已可靠落盘但技术验证失败：acquisition 保持 `acquired`，verification 使用 `verification_failed`，具体记录保持 `status: acquired / record_status: draft` 并保存失败明细；
- checksum 无法可靠确认：不得填写猜测摘要，不得完成来源记录闭环；
- 任何失败均不得修改 raw 以追求通过。

## 7. 本阶段状态声明

```yaml
phase: Phase 1-F
task: P0-4-A
document: P0_ENGLISH_SOURCE_ACQUISITION.md
document_status: ready_for_review
execution_status: not_started

english_source_id: ODY-ENG-MURRAY1919
english_file_id: ODY-ENG-MURRAY1919-RAW-FULL-TEI
english_acquisition_status: pending
english_verification_status: pending
english_checksum: null
english_source_record_created: false
english_raw_file_downloaded: false

pinned_repository_commit: 790c84289edbdbe289dd7b752bfea29f0af4299d
commit_reused_from_p0_3b: true
target_path_contract: source/translations/en/ody-eng-murray1919/raw/ody-eng-murray1919__raw__full.xml
requested_alias_source_original_text_eng_created: false

greek_acquisition_status: acquired
greek_verification_status: verification_failed
greek_analysis_use: reference_only
blocked_structure_validation_released: false

external_byte_assets_downloaded_this_task: 0
source_records_created_this_task: 0
checksums_computed_this_task: 0
normalized_files_created: 0
alignment_outputs_created: 0
content_analysis_created: 0
character_database_created: 0
plot_database_created: 0
adaptation_outputs_created: 0
script_files_created: 0
```

本文完成只表示 English TEI 获取方案已形成并可供后续单来源执行阶段评审；它不构成下载授权、来源验证、Gate 解除或 Phase 2 analysis 授权。
