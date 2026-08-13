# 《奥德赛》Source Acquisition Execution Checklist

> 项目：Classic-to-Drama Engine  
> 阶段：Phase 1-D / Source Acquisition Execution Preparation  
> 文档版本：`c2d.odyssey-source-acquisition-checklist.v1`  
> 文档状态：`ready_for_review`  
> 执行状态：`blocked`（P0-4-B English 已获取并技术验证通过；P0-3-B Greek 结构阻断仍未解除）  
> 日期：2026-08-10  
> 当前边界：本文原始职责仍是执行清单；Phase 1-E / P0-3-B 已执行 Greek TEI，Phase 1-F / P0-4-B 已执行 English TEI。两轮均只做单文件获取、登记与非内容型验证，未获取 CTS/P1/P2 来源，也未进行 normalization、内容分析或改编。

## 1. 文档目的

本文件把 `02_SOURCE_ACQUISITION_PLAN.md` 转换为可以逐项勾选、复核和批准的执行清单。它只回答四个问题：

1. Minimum Source Set 以什么优先级和顺序获取或登记；
2. 每个实际字节资产进入 `source/` 的哪个精确路径；
3. 文件到达后依次完成哪些存在性、格式、编码、SHA-256 与 Book/Line 检查；
4. 什么条件表示 Phase 1-D 的**执行准备**已经完成。

本文创建时不表示任何来源已经下载，所有执行框也均未勾选。Phase 1-E / P0-3-B 之后，只有具备真实证据的 Greek 项目已更新；其他复选框和初始值不得被预填为成功。

## 2. 规范继承与状态边界

### 2.1 规范优先级

执行时必须同时遵守：

1. `SOURCE_MANIFEST.md`：来源身份、角色、引用权限与 locator 规则；
2. `01_SOURCE_PACKAGE_STRUCTURE.md`：目录、文件名、`file_id`、`SOURCE_RECORD` 与 SHA-256 契约；
3. `02_SOURCE_ACQUISITION_PLAN.md`：具体来源、版本、provider、URL、获取模式与 Gate S1-C 验收合同；
4. 本文件：获取顺序、精确目标路径与逐项执行状态。

如四份文档存在冲突，对应任务状态改为 `blocked_spec_conflict`，先统一规范，不在执行现场自行猜测。

### 2.2 逻辑根

本文所有目标路径均从逻辑根 `source/` 开始。若仓库实际使用：

```text
projects/odyssey/sources/
```

则该目录直接等价于 `source/`。不得创建 `source/source/`、`sources/source/` 或 `source/sources/`。

### 2.3 状态词表

| 状态 | 含义 |
| --- | --- |
| `not_started` | 尚未执行；本文创建时所有任务的初始状态 |
| `blocked` | 前置审批、身份、路径、许可或上游版本尚未解决 |
| `acquired` | 原始字节已到达目标路径，但尚未完成全部验证 |
| `registered` | `reference_only` 或 `link_only` 条目已完成登记；不表示存在本地来源字节 |
| `verification_failed` | 文件已到达但至少一项检查失败 |
| `verified` | 规定的技术检查已通过或被正确标为 `not_applicable` |
| `approved` | 人工复核通过；含字节文件的记录完成 `draft -> verified -> approved` |
| `deferred` | 尚未获准进入当前执行波次，不计入当前完成率 |

`reference_only`、`link_only` 和二进制文件的“不适用”检查必须写成明确的 `not_applicable_*`，不得用虚假的 `passed` 代替。

## 3. Minimum Source Set 优先级

### 3.1 优先级映射

| 执行级别 | 对应 Phase 1-C 类别 | 含义 | 对后续 Gate 的影响 |
| --- | --- | --- | --- |
| **P0 必须获取** | `required_core` | 建立可复现的希腊文引用脊柱、英文工作文本和 CTS 身份链 | 任一核心文件缺失或来自不同 commit，禁止进入后续文本处理 |
| **P1 后续获取/登记** | `required_audit`、`required_reference` | 在 P0 后补齐页面复核、中文参考登记、历史数据集和 link-only 权威入口 | 对 Gate S1-C / 完整 Source Package 仍是必需项；“后续”不等于“可选” |
| **P2 延后** | `optional_aux`、`deferred` | 辅助对读或遇到具体研究问题后才启用的候选 | 缺失不阻断 P0、P1 或 Gate S1-D；启用前必须重新通过 preflight |

### 3.2 严格执行顺序

#### P0：Perseus 核心批次

- [ ] `P0-00`：Gate S1-B 与 `02_SOURCE_ACQUISITION_PLAN.md` 已获批准，执行授权明确。
- [x] `P0-01`：已锁定 `PerseusDL/canonical-greekLit` 完整 commit `790c84289edbdbe289dd7b752bfea29f0af4299d`；同一 commit 下四个核心路径均确认存在。
- [x] `P0-02`：已按该 commit 获取 Greek TEI；技术验证结果为 `verification_failed`，详见 `P0_GREEK_SOURCE_ACQUISITION_RESULT.md`。
- [x] `P0-03`：已按同一 commit 获取 English TEI；English 专属技术验证为 `verified`，详见 `P0_ENGLISH_SOURCE_ACQUISITION_RESULT.md`。
- [ ] `P0-04`：按同一 commit 获取 textgroup `__cts__.xml`。
- [ ] `P0-05`：按同一 commit 获取 work `__cts__.xml`。
- [ ] `P0-06`：四文件分别登记、计算 SHA-256、完成格式与编码检查。
- [ ] `P0-07`：完成 Greek `book.line`、English `book.card`、CTS 身份及四文件交叉一致性检查。
- [ ] `P0-08`：Scaife ATLAS 与 legacy Perseus Catalog 两个 link-only 身份入口已登记；legacy `grc1/eng1` 未覆盖当前 `grc2/eng3`。

P0-4-B 只完成 P0-06、P0-07 中的 English 单文件子证据；由于 Greek 仍为 `verification_failed` 且两个 CTS metadata 文件尚未获取，这两个四文件累计项继续保持未勾选。

P0 未完成前，不执行 P1 字节获取，不进行 normalized 转换、passage 切分或 Greek–English 对齐。

#### P1：必需后续批次

- [ ] `P1-01`：从 Internet Archive item metadata 锁定 Murray 1919 卷一 PDF 的具体资产身份，再获取卷一影像。
- [ ] `P1-02`：以同样方式锁定并获取卷二影像。
- [ ] `P1-03`：为 Perseus #1652、#1655 建立只读复核记录；不修改 raw TEI。
- [ ] `P1-04`：完成王焕生 2014 四册本的 `reference_only / metadata_only` 登记和使用说明；不导入译文正文。
- [ ] `P1-05`：从 Zenodo 4.1 记录锁定 Pleiades 正式 release ZIP，再获取编号版资产；不得用滚动 `latest` 替代。
- [ ] `P1-06`：登记本计划规定的十个历史/方法 link-only 入口；不抓取网页正文。
- [ ] `P1-07`：完成 P1 三个字节资产、一个 reference-only 来源和全部 link-only 条目的适用检查。

#### P2：延后批次

- [ ] `P2-01`：仅在 P0–P1 完成且项目明确批准辅助对读后，启用 Project Gutenberg #1727 UTF-8 TXT。
- [ ] `P2-02`：其余 deferred 中文译本、Perseus 英译候选、词典、注释及纸草入口继续保持 `deferred`。
- [ ] `P2-03`：任何 P2 项启用前，先将其改为明确的 `required_*` 或 `optional_aux`，再完成独立 preflight；不得直接下载。

## 4. 字节资产目标路径

下表锁定全部执行路径及其**初始状态**。P0-3-B 后 Greek、P0-4-B 后 English 目标文件均已真实存在；其余路径仍是未来执行目标。当前实绩以第 8 节矩阵和第 11 节最新执行块为准。

### 4.1 P0 必须获取：四个核心文件

| 顺序 | `source_id` | `file_id` | 上游资产 | 目标路径 | 文件记录路径 | 初始状态 |
| --- | --- | --- | --- | --- | --- | --- |
| P0-02 | `ODY-GRC-MURRAY1919` | `ODY-GRC-MURRAY1919-RAW-FULL-TEI` | `data/tlg0012/tlg002/tlg0012.tlg002.perseus-grc2.xml` | `source/original_text/grc/ody-grc-murray1919/raw/ody-grc-murray1919__raw__full.xml` | `source/metadata/records/ody-grc-murray1919-raw-full-tei.source.yaml` | `not_started` |
| P0-03 | `ODY-ENG-MURRAY1919` | `ODY-ENG-MURRAY1919-RAW-FULL-TEI` | `data/tlg0012/tlg002/tlg0012.tlg002.perseus-eng3.xml` | `source/translations/en/ody-eng-murray1919/raw/ody-eng-murray1919__raw__full.xml` | `source/metadata/records/ody-eng-murray1919-raw-full-tei.source.yaml` | `not_started` |
| P0-04 | `ODY-META-PERSEUS-CTS` | `ODY-META-PERSEUS-CTS-RAW-TEXTGROUP-XML` | `data/tlg0012/__cts__.xml` | `source/references/textual_reference/ref-ody-perseus-tei/raw/ody-meta-perseus-cts__raw__textgroup.xml` | `source/metadata/records/ody-meta-perseus-cts-raw-textgroup-xml.source.yaml` | `not_started` |
| P0-05 | `ODY-META-PERSEUS-CTS` | `ODY-META-PERSEUS-CTS-RAW-WORK-XML` | `data/tlg0012/tlg002/__cts__.xml` | `source/references/textual_reference/ref-ody-perseus-tei/raw/ody-meta-perseus-cts__raw__work.xml` | `source/metadata/records/ody-meta-perseus-cts-raw-work-xml.source.yaml` | `not_started` |

P0 四条记录的 `provider_identity.upstream_commit` 必须完全相同；四个 `retrieval_url` 必须包含该完整 commit，而不是可变分支名。

### 4.2 P1 后续获取：三个字节资产

| 顺序 | `source_id` | `file_id` | Provider 资产身份 | 目标路径 | 文件记录路径 | 初始状态 |
| --- | --- | --- | --- | --- | --- | --- |
| P1-01 | `ODY-SCAN-MURRAY1919-V1` | `ODY-SCAN-MURRAY1919-V1-SCAN-VOL01-PDF` | IA item `odysseymurray01homeuoft` 中经 metadata 锁定的具体 PDF | `source/references/textual_reference/ref-ody-murray1919-scans/raw/ody-scan-murray1919-v1__scan__vol01.pdf` | `source/metadata/records/ody-scan-murray1919-v1-scan-vol01-pdf.source.yaml` | `not_started` |
| P1-02 | `ODY-SCAN-MURRAY1919-V2` | `ODY-SCAN-MURRAY1919-V2-SCAN-VOL02-PDF` | IA item `odysseywithengli02home` 中经 metadata 锁定的具体 PDF | `source/references/textual_reference/ref-ody-murray1919-scans/raw/ody-scan-murray1919-v2__scan__vol02.pdf` | `source/metadata/records/ody-scan-murray1919-v2-scan-vol02-pdf.source.yaml` | `not_started` |
| P1-05 | `CTX-GEO-PLEIADES-R4-1` | `CTX-GEO-PLEIADES-R4-1-RAW-RELEASE-ZIP` | Zenodo record `15540082` 中的 Pleiades 4.1 正式 release ZIP | `source/references/historical_context/ctx-geo-pleiades/raw/ctx-geo-pleiades-r4-1__raw__release.zip` | `source/metadata/records/ctx-geo-pleiades-r4-1-raw-release-zip.source.yaml` | `not_started` |

扫描文件的记录使用 `state: scan`，但原始字节仍位于 `raw/` 目录并遵守不可变策略。Pleiades ZIP 在本阶段不持久展开为数万文件。

### 4.3 P2 延后：可选字节资产

| 顺序 | `source_id` | `file_id` | 目标路径 | 文件记录路径 | 初始状态 |
| --- | --- | --- | --- | --- | --- |
| P2-01 | `ODY-ENG-BUTLER-PG1727` | `ODY-ENG-BUTLER-PG1727-RAW-FULL-TXT` | `source/translations/en/ody-eng-butler-pg1727/raw/ody-eng-butler-pg1727__raw__full.txt` | `source/metadata/records/ody-eng-butler-pg1727-raw-full-txt.source.yaml` | `deferred` |

若以后另取 EPUB，必须建立新的 `file_id`、目标路径、文件记录与 SHA-256；不得与 TXT 共用物理文件身份。

## 5. 非字节登记目标

非字节条目没有下载文件，不创建虚假 `SOURCE_RECORD`，也不进入 `checksums.sha256`。

### 5.1 P0 身份核验入口

| `resource_id` | 登记目标 | 检查目的 | 初始状态 |
| --- | --- | --- | --- |
| `REF-ODY-SCAIFE-ATLAS` | `source/metadata/resources.yaml` | 交叉核验 `perseus-grc2`、`perseus-eng3`、Murray、1919 与语言身份 | `not_started` |
| `REF-ODY-PERSEUS-CATALOG` | `source/metadata/resources.yaml` | 只作 legacy 书目核验；明确旧 `grc1/eng1` 不具覆盖权 | `not_started` |

### 5.2 P1 中文 reference-only

| `source_id` | 登记/说明目标 | 必填内容 | 明确不创建 | 初始状态 |
| --- | --- | --- | --- | --- |
| `ODY-ZHO-WANG2014` | `source/metadata/sources.yaml`；`source/metadata/rights.yaml`；`source/translations/zh-Hans/ody-zho-wang2014/reference-only/README.md` | 出版社、ISBN、全四册、译者、版次/印次状态、volume+page 定位规则、`metadata_only` 权利边界 | 译文正文、来源文件 `SOURCE_RECORD`、来源字节 SHA-256 | `not_started` |

实体书版权页尚未核验时，版次/印次字段必须明确保留为 `pending_verification`，不得根据聚合页面猜测为已确认。

### 5.3 P1 历史/方法 link-only 入口

以下十项统一登记到 `source/metadata/resources.yaml`：

| `resource_id` | 资源 | 初始状态 |
| --- | --- | --- |
| `CTX-ORAL-HMT` | Homer Multitext 项目说明 | `not_started` |
| `CTX-ORAL-PARRY` | Milman Parry Collection 馆藏入口 | `not_started` |
| `CTX-ORAL-LORD` | *The Singer of Tales* 持久入口 | `not_started` |
| `CTX-ARCH-DARTMOUTH` | Dartmouth Aegean Prehistoric Archaeology | `not_started` |
| `CTX-ARCH-MET-MYC` | Met：Mycenaean Civilization | `not_started` |
| `CTX-ARCH-MET-GEO` | Met：Geometric Art in Ancient Greece | `not_started` |
| `CTX-ARCH-BM-MYC` | British Museum：Minoans and Mycenaeans | `not_started` |
| `CTX-ARCH-BM-1050` | British Museum：Greece 1050–520 BC | `not_started` |
| `CTX-GEO-IDAI` | iDAI.gazetteer | `not_started` |
| `CTX-MAP-AWMC` | Ancient World Mapping Center Maps | `not_started` |

每项只检查 `resource_id`、题名、provider、canonical URL、访问日期、角色、权利状态和时间层标签是否完整。不保存 HTML 快照、PDF、图片、音频、API 全量响应或页面正文。

### 5.4 P2 deferred 清单

| ID | 登记目标 | 当前动作 |
| --- | --- | --- |
| `ODY-ZHO-CHEN2022` | `source/metadata/sources.yaml` | 保持 `deferred / reference_only` |
| `ODY-ZHO-YANG2019` | `source/metadata/sources.yaml` | 保持 `deferred / reference_only` |
| `ODY-ENG-BUTLER-POWER-NAGY-PERSEUS-ENG4` | `source/metadata/sources.yaml` | 保持 `deferred` |
| `REF-ODY-DCC` | `source/metadata/resources.yaml` | 保持 `deferred / link_only` |
| `REF-GRC-LOGEION` | `source/metadata/resources.yaml` | 保持 `deferred / discovery_only` |
| `REF-ODY-PAPYRI-DISCOVERY` | `source/metadata/resources.yaml` | 保持 `deferred / link_only` |
| `REF-PAPYRI-VERIFY` | `source/metadata/resources.yaml` | 保持 `deferred / link_only` |

## 6. 执行前 Preflight

真实获取开始前逐项确认：

- [ ] `SOURCE_MANIFEST.md` 的双层主底本方案已获批准。
- [ ] Gate S1-B 状态为 `approved`。
- [ ] `02_SOURCE_ACQUISITION_PLAN.md` 已获项目负责人批准。
- [ ] `source/` 与仓库实际目录的映射唯一。
- [ ] 本轮只授权写入目标 `raw/`、reference-only 说明和 `metadata/` 登记目录。
- [ ] 每个含字节来源的 `source_id` 已存在于 `sources.yaml`。
- [ ] 每个 `file_id` 在全包唯一，记录文件名和目标路径无碰撞。
- [ ] 位于 `references/` 的字节资产已有正确的 `context_resource_id`，且该 ID 存在于 `resources.yaml`。
- [ ] provider、canonical URL、未来实际使用的 immutable retrieval URL 与预期媒体类型均已明确。
- [ ] Perseus P0 四文件将使用同一完整 commit SHA。
- [ ] IA PDF 已有可区分原始/派生状态的具体 provider asset 身份。
- [ ] Pleiades 使用 Zenodo 4.1 编号版具体资产，不使用滚动 `latest`。
- [ ] 每项许可可写为明确 SPDX ID、`NOASSERTION` 或项目 `LicenseRef-*`，没有用站点级声明代替文件级核验。
- [ ] 目标位置不存在未处理的同名 approved 文件；如存在，先进入版本差异流程，不静默覆盖。
- [ ] 获取日志、记录目录、checksum 清单和质量报告的写入位置已经固定。
- [ ] 本轮授权仍只限资料获取与登记，不包含文本内容分析或改编任务。

任一项未满足，停止对应资产，不创建零字节正式文件或伪造成功记录。

## 7. 获取完成后的通用检查步骤

以下是所有资产共用的检查合同。P0-3-B 与 P0-4-B 已分别对 Greek、English 单文件执行适用检查，并将结果写入第 8 节矩阵及质量报告；本节通用复选框不整体勾选，以免误示 CTS 或其他资产也已完成。

### 7.1 文件存在检查

- [ ] 目标路径存在且是普通文件，不是目录、符号链接误指、登录页或错误页。
- [ ] 文件大小大于 0，并与 `SOURCE_RECORD.bytes` 完全一致。
- [ ] 获取动作已写入 `source/metadata/logs/acquisition_log.jsonl`，成功、失败和重试均有独立事件。
- [ ] 临时文件已完成原子命名；不存在被当作正式资产的 `.part`、`.tmp` 或零字节占位文件。
- [ ] 一个本地来源文件只对应一个 `file_id` 和一条 `metadata/records/*.source.yaml`。

### 7.2 文件格式检查

| 资产类型 | 必须检查 | 失败条件 |
| --- | --- | --- |
| XML / TEI / CTS | XML 可严格解析；root、namespace、TEI header 或 CTS 元数据结构与预期身份相符 | HTML/错误页伪装成 XML、XML 不闭合、namespace 或版本身份冲突 |
| PDF scans | PDF 签名和容器可识别；页数大于 0；页面序列可访问；卷次与 provider metadata 一致 | 文件损坏、零页、卷次错误、OCR 文本冒充页面影像 |
| ZIP dataset | ZIP 容器完整性测试通过；目录可列出；包含 release 说明、许可和预期数据类型 | 损坏、使用错误版本、滚动 latest 冒充 4.1、解压内容被当作原始 ZIP |
| UTF-8 TXT | 纯文本资产身份与 provider 记录一致；不存在 HTML 下载页 | 非目标电子书、编码声明不符、错误页面或截断文件 |
| YAML / Markdown 登记 | 项目自建文件语法可解析或可读，字段齐全 | 把登记说明误当成来源正文或来源字节 |

格式失败时状态改为 `verification_failed`；不得继续生成 approved 记录。

### 7.3 编码检查

- [ ] XML declaration 与实际字节编码一致，并能按声明编码严格解码。
- [ ] 禁止使用 replacement mode 隐藏非法字节。
- [ ] TEI 的 `xml:lang` 与记录语言一致：Greek 为 `grc`，English 为 `en`。
- [ ] TXT 使用 provider 声明的编码；未声明时记录检测结果并人工确认。
- [ ] 项目自建 YAML、JSONL 与 Markdown 使用 UTF-8、LF。
- [ ] PDF、ZIP 和图像标为 `not_applicable_binary_container`；只检查容器及内部文本自己的编码声明。
- [ ] raw 字节未执行换行统一、BOM 删除、Unicode NFC、标点替换或其他清洗。

### 7.4 SHA-256 记录

- [ ] 对每个实际保存的来源字节按原样计算 SHA-256。
- [ ] 每条 `SOURCE_RECORD.checksum` 使用 `sha256:<64位小写十六进制>`。
- [ ] 同一摘要与相对路径写入 `source/metadata/checksums/checksums.sha256`。
- [ ] YAML 摘要、checksum 清单摘要和重新计算结果三者完全一致。
- [ ] 同一 `source_id` 下的多个物理文件分别拥有独立 `file_id`、记录和摘要。
- [ ] `reference_only` README、link-only 条目和尚未取得的 P2 项没有伪造来源 checksum。
- [ ] 任一字节变化都产生新的记录版本与摘要，不静默复用旧值。

### 7.5 Book/Line 与 locator 结构检查

#### Greek `perseus-grc2`

- [ ] CTS identity 精确等于 `urn:cts:greekLit:tlg0012.tlg002.perseus-grc2`。
- [ ] citation scheme 为 `book.line`。
- [ ] 恰有 Book 1–24，编号不缺失、不重复、顺序正确。
- [ ] 每卷 line locator 是可解析的正整数，卷内单调递增且不重复。
- [ ] 所有 gap、duplicate、倒序、空 Book 与异常标签均输出明细。
- [ ] #1652、#1655 进入 `known_issues`，未经人工分类的异常保持阻断。
- [ ] 没有自动补行、重新编号、删标签或修改 raw TEI。

#### English `perseus-eng3`

- [ ] CTS identity 精确等于 `urn:cts:greekLit:tlg0012.tlg002.perseus-eng3`。
- [ ] citation scheme 为 `book.card`。
- [ ] 恰有 Book 1–24；每卷 card locator 可解析、唯一并保持原生顺序。
- [ ] Book/Line 检查明确记录为 `not_applicable_book_card_source`。
- [ ] 没有把 card 数字、card 连续性或页面 chunk 冒充希腊文行号。
- [ ] English–Greek line range alignment 仍为 `not_started`。

#### CTS metadata、scans、Chinese 与 historical

- [ ] textgroup/work CTS 元数据包含目标作品及 `grc2`、`eng3` 版本身份。
- [ ] Murray scans 只检查卷次、页序和可见印刷定位；OCR 行号不作为 CTS line。
- [ ] `ODY-ZHO-WANG2014` 自动 Book/Line 检查为 `not_applicable_reference_only`；实体书可用时只人工核验四册与 24 Book 覆盖。
- [ ] Pleiades 的 Book/Line 为 `not_applicable_dataset`，另检查 release 版本、目录、数据类型和许可文件。
- [ ] link-only 资源的 Book/Line 为 `not_applicable_link_only`。

### 7.6 交叉身份与记录闭环

- [ ] P0 四文件的完整 `upstream_commit` 完全一致。
- [ ] Greek/English TEI header、CTS 元数据与 Scaife canonical identity 不冲突。
- [ ] 每个 `references/` 字节资产的 `context_resource_id` 能回到 `resources.yaml`。
- [ ] 每个本地来源文件形成唯一闭环：`file -> file_id -> SOURCE_RECORD -> checksums.sha256`。
- [ ] `record_status` 按 `draft -> verified -> approved` 顺序推进，没有跳级。
- [ ] 失败和例外均有明确状态、原因与人工处置结论；没有静默忽略。
- [ ] `source/metadata/quality/source_quality_report.md` 没有未处理的阻断项。

## 8. 分文件验证矩阵

此矩阵记录逐文件真实结果。P0-3-B 更新 Greek 行，P0-4-B 更新 English 行；CTS、P1 和 P2 行保持原状态。

| `file_id` | 存在 | 格式 | 编码 | SHA-256 | Locator / 结构 | 记录闭环 | 最终状态 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `ODY-GRC-MURRAY1919-RAW-FULL-TEI` | [x] | [x] | [x] | [x] | [ ] `book.line` 可寻址，但 B3/B14 非单调且 B16 有未分类缺口 | [x] | `verification_failed` |
| `ODY-ENG-MURRAY1919-RAW-FULL-TEI` | [x] | [x] | [x] | [x] | [x] `book.card`; `book.line` = `not_applicable_book_card_source` | [x] | `verified` |
| `ODY-META-PERSEUS-CTS-RAW-TEXTGROUP-XML` | [ ] | [ ] | [ ] | [ ] | [ ] CTS identity | [ ] | `not_started` |
| `ODY-META-PERSEUS-CTS-RAW-WORK-XML` | [ ] | [ ] | [ ] | [ ] | [ ] CTS identity | [ ] | `not_started` |
| `ODY-SCAN-MURRAY1919-V1-SCAN-VOL01-PDF` | [ ] | [ ] | [ ] binary N/A | [ ] | [ ] page/print locator | [ ] | `not_started` |
| `ODY-SCAN-MURRAY1919-V2-SCAN-VOL02-PDF` | [ ] | [ ] | [ ] binary N/A | [ ] | [ ] page/print locator | [ ] | `not_started` |
| `CTX-GEO-PLEIADES-R4-1-RAW-RELEASE-ZIP` | [ ] | [ ] | [ ] container N/A | [ ] | [ ] release structure; Book/Line N/A | [ ] | `not_started` |
| `ODY-ENG-BUTLER-PG1727-RAW-FULL-TXT` | [ ] | [ ] | [ ] | [ ] | [ ] Book/Line N/A | [ ] | `deferred` |

## 9. 非字节登记验证矩阵

| 对象 | 身份/版本 | Provider/URL | 权利/访问 | 角色/locator 边界 | 正文未落盘 | 最终状态 |
| --- | --- | --- | --- | --- | --- | --- |
| `ODY-ZHO-WANG2014` | [ ] | [ ] | [ ] | [ ] volume+page；Book/Line N/A | [ ] | `not_started` |
| P0 两个 Perseus link-only 入口 | [ ] | [ ] | [ ] | [ ] 仅身份核验 | [ ] | `not_started` |
| P1 十个历史/方法 link-only 入口 | [ ] | [ ] | [ ] | [ ] 不产生原著事实 | [ ] | `not_started` |
| P2 七个 deferred 候选 | [ ] | [ ] | [ ] | [ ] 保持 deferred | [ ] | `deferred` |

## 10. Gate S1-D 完成标准

### 10.1 Gate 含义

Gate S1-D 的含义是 **Acquisition Execution Checklist Ready**：实际执行所需的顺序、身份、路径、检查方法和停止条件已经锁定并获批。

由于本轮明确只做准备工作，Gate S1-D **不要求也不证明文件已经下载**。未来实际获取完成后，应使用本文矩阵生成真实证据，再按 `02_SOURCE_ACQUISITION_PLAN.md` 的 Gate S1-C 与后续 Gate S1 评估 Source Package 是否真正就绪。

### 10.2 验收清单

只有以下条件全部满足，Gate S1-D 才能标记为 `approved`：

- [ ] `SOURCE_MANIFEST.md`、`01_SOURCE_PACKAGE_STRUCTURE.md` 与 `02_SOURCE_ACQUISITION_PLAN.md` 的身份和路径无未解决冲突。
- [ ] P0、P1、P2 的映射唯一；每项只属于一个执行级别。
- [ ] P0 四个字节资产均有唯一 `source_id`、`file_id`、上游路径、目标路径和记录路径。
- [ ] P1 三个字节资产均有唯一物理身份、目标路径和记录路径。
- [ ] 中文 `reference_only`、Perseus 身份入口和历史 `link_only` 条目均有明确登记目标，且不会创建虚假来源文件或 checksum。
- [ ] P2 项的重新启用条件明确，未被计入 P0/P1 完成率。
- [ ] 存在性、文件格式、编码、SHA-256、Book/Line/Book.Card 和交叉身份检查均已转化为可勾选步骤。
- [ ] Greek `book.line` 与 English `book.card` 权限分离，English Book/Line 明确为不适用。
- [ ] `raw` 不可变、同 commit、编号 release、逐文件记录和异常阻断规则均已写入清单。
- [ ] 所有执行状态初始化为 `not_started` 或 `deferred`，没有把计划值写成真实结果。
- [ ] 本次文档任务下载文件数为 0、来源记录数为 0、checksum 数为 0。
- [ ] 未开始 normalized 转换、对齐、内容分析、人物分析、改编或剧本生成。
- [ ] 人工评审者将未来的 `source/metadata/quality/gate_s1d.yaml` 状态批准为 `approved`。

### 10.3 Gate 状态机

```yaml
gate_id: S1-D
phase: source_acquisition_execution_preparation
meaning: acquisition_execution_checklist_ready
allowed_statuses:
  - draft
  - ready_for_review
  - changes_requested
  - approved
completion_rule: status == approved
requires_downloaded_source_files: false
does_not_replace:
  - Gate S1-C
  - Gate S1
```

### 10.4 阻断条件

出现任意一项时，Gate S1-D 必须保持 `draft`、返回 `changes_requested` 或标为失败：

- P0 四文件的 commit 约束不唯一或仍允许 mutable branch URL；
- 任一字节资产缺少精确目标路径、唯一 `file_id` 或记录路径；
- scan、Pleiades ZIP、中文 reference-only 或 link-only 条目的获取模式被混淆；
- English card 被写成 line，或中文/背景资料被赋予 canonical anchor 权限；
- P1 被误写成永久可选，导致 Gate S1-C 的 required audit/reference 被删去；
- P2 候选可以绕过 preflight 直接下载；
- 清单预填了不存在的 SHA-256、文件大小、获取时间或成功状态；
- 当前准备阶段实际下载、清洗、切分或分析了来源内容；
- 已开始剧情、人物、场景、短剧、剧本或视频制作工作。

## 11. 当前状态

```yaml
phase: Phase 1-D
document: 03_SOURCE_ACQUISITION_EXECUTION_CHECKLIST.md
document_status: ready_for_review
gate_s1d: draft
execution_status: blocked

planned_inventory:
  p0_byte_assets: 4
  p0_link_only_identity_entries: 2
  p1_byte_assets: 3
  p1_reference_only_sources: 1
  p1_link_only_resources: 10
  p2_optional_byte_assets: 1
  p2_deferred_candidates: 7

actual_in_this_document_task:
  source_directories_created: 0
  files_downloaded: 0
  source_records_created: 0
  checksums_computed: 0
  source_content_read: false
  text_analysis_started: false
  plot_analysis_started: false
  character_database_started: false
  adaptation_started: false
  script_generation_started: false

latest_p0_3b_execution:
  pinned_commit: 790c84289edbdbe289dd7b752bfea29f0af4299d
  external_byte_assets_downloaded: 1
  source_records_created: 1
  real_source_sha256_values: 1
  greek_acquisition_status: acquired
  greek_verification_status: verification_failed
  remaining_p0_acquisition_status: pending
  remaining_p0_verification_status: pending
  normalized_files_created: 0
  content_analysis_started: false
  character_database_started: false
  plot_database_started: false
  adaptation_started: false
  script_generation_started: false

latest_p0_4b_execution:
  pinned_commit: 790c84289edbdbe289dd7b752bfea29f0af4299d
  external_byte_assets_downloaded: 1
  bytes: 870905
  sha256: dda5b206e332e56c570c1d92ea41e9a510339a454bc2ea90491788e34174a7e7
  git_blob_sha: 00012e531976c182625bacc9374b07cd4411750d
  source_records_created: 1
  real_source_sha256_values: 1
  english_acquisition_status: acquired
  english_verification_status: verified
  english_approval_status: pending
  source_xml_lang: eng
  project_language: en
  language_mapping_explicit: true
  book_count: 24
  card_count: 288
  book_line_rule: not_applicable_book_card_source
  english_greek_alignment: not_started
  remaining_p0_pending_byte_assets: 2
  greek_acquisition_status: acquired
  greek_verification_status: verification_failed
  normalized_files_created: 0
  content_analysis_started: false
  character_database_started: false
  plot_database_started: false
  adaptation_started: false
  script_generation_started: false
```

P0-3-B 与 P0-4-B 的单文件执行均已由项目负责人分别授权；这不等于 Gate S1-B、S1-C、S1-D 或总 Gate S1 获批。Greek locator 结构阻断继续存在，两个 CTS metadata 文件继续 pending；未获后续独立授权前，不自动获取其他 P0、P1 或 P2 资产。
