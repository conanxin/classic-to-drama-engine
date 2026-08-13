# 《奥德赛》Source Acquisition 资料获取与登记计划

> 项目：Classic-to-Drama Engine  
> 阶段：Phase 1-C / Source Acquisition  
> 计划版本：`c2d.odyssey-source-acquisition.v1`  
> 文档状态：`ready_for_review`  
> 执行状态：`not_started`  
> 核验日期：2026-08-10  
> 当前边界：只定义来源文件、获取入口、登记方式与下载后检查；本阶段文档编制不下载文本，不读取或分析剧情，不建立人物数据库，不进行短剧改编，不生成剧本。

## 1. 文档目的

本文件把 `SOURCE_MANIFEST.md` 的来源选择和 `01_SOURCE_PACKAGE_STRUCTURE.md` 的落盘契约转换为一份可执行的获取清单。它回答四个问题：

1. Phase 1-C 需要获取或登记哪些具体来源；
2. 每项来源从哪里取得、以什么格式保存、承担什么职责；
3. 文件到达后如何验证字节、编码和 Book/Line 结构；
4. 满足什么条件后，Phase 1-C 才能进入 `approved`。

本文是**获取计划**，不是来源包本身。本文中的文件名、路径和检查项不表示对应文件已经下载、校验或批准。

## 2. 上游规范与执行前提

### 2.1 规范优先级

Phase 1-C 必须同时服从以下文件：

1. `SOURCE_MANIFEST.md`：决定来源角色、CTS 身份和引用权限；
2. `01_SOURCE_PACKAGE_STRUCTURE.md`：决定目录、文件身份、`SOURCE_RECORD.yaml` 和 SHA-256 规则；
3. 本文件：决定本轮具体获取对象、顺序和验收方法。

若三者发生冲突，暂停对应来源的获取，先修订规范；不得在执行脚本中临时猜测。

### 2.2 逻辑目录根

本文使用 `source/` 作为逻辑根。若项目实际采用 `projects/odyssey/sources/`，则后者直接等价于 `source/`，不得重复嵌套。

### 2.3 执行前置条件

实际下载开始前必须满足：

- `SOURCE_MANIFEST.md` 的“双层主底本”方案获得项目负责人批准；
- Gate S1-B 的目录与记录规范获得 `approved`；
- 本文件中的必需来源、受限来源边界和历史资料最小集获得批准；
- 获取程序只被授权写入各来源的 `raw/` 目录及 `metadata/` 日志/记录目录。

当前 `01_SOURCE_PACKAGE_STRUCTURE.md` 仍是 `ready_for_review`，因此本文可以完成和评审，但真实获取仍保持 `not_started`。

## 3. 获取对象与登记类型

### 3.1 五种获取模式

| `acquisition_mode` | 含义 | 是否产生本地来源字节 | 是否创建 `SOURCE_RECORD` | 是否填写 SHA-256 |
| --- | --- | ---: | ---: | ---: |
| `byte_acquisition` | 从批准的公开提供方取得文件 | 是 | 是 | 是 |
| `shared_metadata_asset` | 获取 CTS、许可或版本元数据文件 | 是 | 是 | 是 |
| `conditional_audit_asset` | 仅为版本或异常复核取得扫描/影像 | 是 | 是 | 是 |
| `reference_only` | 只登记纸本、受限平台或用户本地查阅方式 | 否，除非以后合法提供本地文件 | 否 | 否 |
| `link_only` | 只登记权威网页、目录或 API 入口 | 否 | 否；写入 `resources.yaml` | 否 |

`reference_only` 和 `link_only` 没有本地来源文件，不能为了满足模板而创建零字节占位文件、虚构 `checksum` 或伪造 `file_id`。

### 3.2 身份分工

- `source_id` 标识一个书目、版本或可获取数据集；
- `file_id` 标识该来源下的一个实际物理文件；
- `resource_id` 标识没有本地字节的历史、文本学或发现入口；
- 一个 `source_id` 可以有多个 `file_id`；
- `resource_id` 不得直接填进 `SOURCE_RECORD.yaml` 的 `source_id` 字段。

### 3.3 优先级

| `priority` | 含义 | 对 Gate S1-C 的影响 |
| --- | --- | --- |
| `required_core` | 规范原文、主要工作英译及其 CTS 身份文件 | 任一缺失即阻断 |
| `required_reference` | 已批准的中文参考登记和历史资料最小集 | 登记缺失即阻断；link-only 不要求 checksum |
| `required_audit` | 已知版本异常所需的页面影像 | 未完成已知异常复核时阻断 |
| `optional_aux` | 辅助译本或扩展背景资源 | 缺失不阻断 Phase 1-C |
| `deferred` | 只保留候选身份，待未来明确需求再处理 | 不进入本轮完成率 |

### 3.4 `source_id` 与 `context_resource_id` 映射

凡文件落在 `references/`，其 `SOURCE_RECORD.context_resource_id` 必须指向 `resources.yaml` 中的资源条目：

| byte-bearing `source_id` | `context_resource_id` | 状态 |
| --- | --- | --- |
| `ODY-SCAN-MURRAY1919-V1` | `REF-ODY-MURRAY1919-SCANS` | 本计划新增资源条目 |
| `ODY-SCAN-MURRAY1919-V2` | `REF-ODY-MURRAY1919-SCANS` | 与卷一共享资源集合身份，物理文件身份仍分开 |
| `ODY-META-PERSEUS-CTS` | `REF-ODY-PERSEUS-TEI` | 复用 `SOURCE_MANIFEST.md` 既有条目 |
| `CTX-GEO-PLEIADES-R4-1` | `CTX-GEO-PLEIADES` | 复用 `SOURCE_MANIFEST.md` 既有条目 |

该映射不允许多个物理文件共用 `file_id` 或 checksum；它只表达“此文件属于哪个参考资源集合”。

## 4. URL、commit 与版本冻结规则

### 4.1 三类 URL

每个可下载来源应区分：

| 字段 | 用途 | 示例性质 |
| --- | --- | --- |
| `canonical_url` | 人工核对作品、版本或数据集身份 | Scaife ATLAS 版本页、出版社书目页、Pleiades DOI |
| `discovery_url` | 发现仓库路径或发行资产 | GitHub 仓库、release 页面、provider 下载目录 |
| `retrieval_url` | 实际取得字节的不可变地址 | 含完整 Git commit、release tag 或记录版本号的直接文件地址 |

最终 `SOURCE_RECORD.url` 必须写本次实际使用的 `retrieval_url`；建议在扩展字段中同时保留 `canonical_url`。只有网页登记、没有本地文件时，`resources.yaml` 可只写 `canonical_url`。

### 4.2 Perseus 冻结规则

以下四个核心资产必须来自 `PerseusDL/canonical-greekLit` 的**同一个完整 commit SHA**：

1. `data/tlg0012/tlg002/tlg0012.tlg002.perseus-grc2.xml`；
2. `data/tlg0012/tlg002/tlg0012.tlg002.perseus-eng3.xml`；
3. `data/tlg0012/__cts__.xml`；
4. `data/tlg0012/tlg002/__cts__.xml`。

`master`、`main`、`latest` 或 GitHub HTML 页面只能用于发现，不得进入已批准记录的 `retrieval_url`。执行时先解析一次 commit，然后为全部四个资产构造同一 commit 下的不可变原始文件 URL，并写入 `provider_identity.upstream_commit`。

Scaife ATLAS 当前采用 `perseus-grc2` / `perseus-eng3`。旧目录或旧 Catalog 中出现的 `grc1` / `eng1` 不得覆盖本计划的数字版本身份；实际获取后必须以同一 commit 中两级 `__cts__.xml` 和文本 TEI header 共同核验。

### 4.3 历史数据冻结规则

- 对可发布的静态研究包，优先使用编号 release 或 DOI 版本，不使用滚动 `latest`；
- Pleiades 本轮锁定编号版 `4.1`，不把日更 JSON URL 当成复现身份；
- 没有编号快照的 API 或网页只登记为 `link_only`；
- 任何页面更新都不静默覆盖旧登记，变更需新增 `retrieved_at` 或资源版本记录。

## 5. 具体来源清单

### 5.1 Primary Greek text

| `source_id` | title | edition | provider | URL | file format | intended usage | priority / mode |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `ODY-GRC-MURRAY1919` | *The Odyssey, Volumes 1–2* / `Ὀδύσσεια` | A. T. Murray 编校，1919；CTS `perseus-grc2` | Perseus Digital Library / Scaife ATLAS；物理分发为 `PerseusDL/canonical-greekLit` | [Scaife ATLAS 版本页](https://atlas.perseus.tufts.edu/library/urn%3Acts%3AgreekLit%3Atlg0012.tlg002.perseus-grc2/)；[上游仓库](https://github.com/PerseusDL/canonical-greekLit) | XML；取得后依据 namespace/header 确认 TEI/EpiDoc 细节 | `canonical_anchor`；唯一 Book.Line 引用脊柱 | `required_core / byte_acquisition` |
| `ODY-SCAN-MURRAY1919-V1` | *The Odyssey with an English Translation*, Volume I | Murray 1919，卷一页面影像 | Internet Archive | [IA item：Volume I](https://archive.org/details/odysseymurray01homeuoft) | PDF；IA item metadata 只用于解析具体资产身份 | 核对版本页面、印刷行和数字文本异常；不作为默认机器正文 | `required_audit / conditional_audit_asset` |
| `ODY-SCAN-MURRAY1919-V2` | *The Odyssey with an English Translation*, Volume II | Murray 1919，卷二页面影像 | Internet Archive | [IA item：Volume II](https://archive.org/details/odysseywithengli02home) | PDF；IA item metadata 只用于解析具体资产身份 | 核对版本页面，尤其已知 Book 23 行号/缺行问题；不替代 CTS 原文 | `required_audit / conditional_audit_asset` |

#### 5.1.1 主希腊文物理资产

| `file_id` | upstream path / asset | 计划本地路径 | 备注 |
| --- | --- | --- | --- |
| `ODY-GRC-MURRAY1919-RAW-FULL-TEI` | `data/tlg0012/tlg002/tlg0012.tlg002.perseus-grc2.xml` | `original_text/grc/ody-grc-murray1919/raw/ody-grc-murray1919__raw__full.xml` | 上游单一 XML 覆盖全书；不得虚构为 vol01/vol02 两个 TEI 文件 |
| `ODY-SCAN-MURRAY1919-V1-SCAN-VOL01-PDF` | IA item 中经元数据确认的卷一 PDF 资产 | `references/textual_reference/ref-ody-murray1919-scans/raw/ody-scan-murray1919-v1__scan__vol01.pdf` | 父目录按 `resource_id` 建立；下载前记录具体 IA 资产名、大小和生成/原始状态 |
| `ODY-SCAN-MURRAY1919-V2-SCAN-VOL02-PDF` | IA item 中经元数据确认的卷二 PDF 资产 | `references/textual_reference/ref-ody-murray1919-scans/raw/ody-scan-murray1919-v2__scan__vol02.pdf` | 父目录按 `resource_id` 建立；Book 23 复核所需；不能用 OCR 文本替代页面影像 |

已知结构风险必须预先写入 `known_issues`：

- [Perseus issue #1652：Missing lines](https://github.com/PerseusDL/canonical-greekLit/issues/1652)；
- [Perseus issue #1655：Book 23 行范围问题](https://github.com/PerseusDL/canonical-greekLit/issues/1655)。

这些问题不能在 raw 文件中直接修补。获取后只生成异常报告和页面复核记录；任何规范化修正属于后续独立步骤。

### 5.2 English working translation

| `source_id` | title | edition | provider | URL | file format | intended usage | priority / mode |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `ODY-ENG-MURRAY1919` | *The Odyssey, Volumes 1–2* | A. T. Murray 英译，1919；CTS `perseus-eng3` | Perseus Digital Library / Scaife ATLAS；物理分发为 `PerseusDL/canonical-greekLit` | [Scaife ATLAS 版本页](https://atlas.perseus.tufts.edu/library/urn%3Acts%3AgreekLit%3Atlg0012.tlg002.perseus-eng3/)；[上游文件清单](https://github.com/PerseusDL/canonical-greekLit/blob/master/manifest.txt) | XML；取得后依据 namespace/header 确认 TEI/EpiDoc 细节 | `primary_working_text`；AI 主要可读文本，原生定位仅为 `book.card` | `required_core / byte_acquisition` |
| `ODY-ENG-BUTLER-PG1727` | *The Odyssey* | Samuel Butler 英译；Project Gutenberg eBook #1727，数字版身份在获取时核验 | Project Gutenberg | [eBook #1727](https://www.gutenberg.org/ebooks/1727) | UTF-8 plain text；可另登记 EPUB，但不同资产需独立 `file_id` | 公开英文辅助对读和清洗流程测试；没有规范行号，不承担工作底本身份 | `optional_aux / byte_acquisition` |

#### 5.2.1 主要英译物理资产

| `file_id` | upstream path / asset | 计划本地路径 | 备注 |
| --- | --- | --- | --- |
| `ODY-ENG-MURRAY1919-RAW-FULL-TEI` | `data/tlg0012/tlg002/tlg0012.tlg002.perseus-eng3.xml` | `translations/en/ody-eng-murray1919/raw/ody-eng-murray1919__raw__full.xml` | 与 Greek TEI 使用同一 commit；原生 citation scheme 为 `book.card` |
| `ODY-ENG-BUTLER-PG1727-RAW-FULL-TXT` | PG1727 提供的 UTF-8 plain text 资产 | `translations/en/ody-eng-butler-pg1727/raw/ody-eng-butler-pg1727__raw__full.txt` | 可选；必须记录 Project Gutenberg 实际下载地址和取得日期 |

`perseus-eng3` 的 `card` 不能命名为 `line`，也不能假定 card 数字等于希腊文行号。Book/Line 对齐属于后续 alignment 工作，不在 Phase 1-C 执行。

### 5.3 Shared Perseus identity metadata

以下两个共享元数据文件是 Greek 与 English 版本身份检查的一部分。它们产生真实字节，因此需要独立 `source_id`、`file_id`、记录和 SHA-256。

| `source_id` | title | edition | provider | URL | file format | intended usage | priority / mode |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `ODY-META-PERSEUS-CTS` | Perseus CTS metadata for Homer / *Odyssey* | 与核心 TEI 相同的 pinned commit | PerseusDL `canonical-greekLit` | [仓库文件清单](https://github.com/PerseusDL/canonical-greekLit/blob/master/manifest.txt) | XML | 核验 textgroup、work、`perseus-grc2`、`perseus-eng3`、语言和 citation scheme 身份 | `required_core / shared_metadata_asset` |

| `file_id` | upstream path | 计划本地路径 |
| --- | --- | --- |
| `ODY-META-PERSEUS-CTS-RAW-TEXTGROUP-XML` | `data/tlg0012/__cts__.xml` | `references/textual_reference/ref-ody-perseus-tei/raw/ody-meta-perseus-cts__raw__textgroup.xml` |
| `ODY-META-PERSEUS-CTS-RAW-WORK-XML` | `data/tlg0012/tlg002/__cts__.xml` | `references/textual_reference/ref-ody-perseus-tei/raw/ody-meta-perseus-cts__raw__work.xml` |

另外建立两个无本地字节的目录核验入口：

| `source_id` | `resource_id` | title | provider | URL | file format | intended usage |
| --- | --- | --- | --- | --- | --- | --- |
| `N/A` | `REF-ODY-SCAIFE-ATLAS` | Scaife ATLAS records for Murray 1919 Greek/English *Odyssey* | Scaife Viewer / Perseus | [Greek `grc2`](https://atlas.perseus.tufts.edu/library/urn%3Acts%3AgreekLit%3Atlg0012.tlg002.perseus-grc2/)；[English `eng3`](https://atlas.perseus.tufts.edu/library/urn%3Acts%3AgreekLit%3Atlg0012.tlg002.perseus-eng3/) | link-only HTML/JSON display | 公开交叉核验 CTS URN、Murray、1919 和语言；不替代 pinned raw files |
| `N/A` | `REF-ODY-PERSEUS-CATALOG` | Perseus Catalog *Odyssey* work record | Perseus Digital Library | [legacy work record](https://catalog.perseus.org/catalog/urn%3Acts%3AgreekLit%3Atlg0012.tlg002) | link-only HTML/Atom metadata | 仅复核书目；显式记录其 legacy `grc1/eng1`，不得覆盖当前 `grc2/eng3` |

### 5.4 Chinese reference translation

| `source_id` | title | edition | provider | URL | file format | intended usage | priority / mode |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `ODY-ZHO-WANG2014` | 《奥德赛（全四册）》；平行题名 `ΟΔΥΣΣΕΙΑ` | 上海人民出版社，2014-07-01，古希腊语—汉语对照，全四册，王焕生译；具体版次/印次待实体版权页锁定 | 上海人民出版社；获取载体为用户合法持有实体书或受许可平台访问 | [上海人民出版社书目页](https://www.shsjcb.com/sjcb/view.aspx?id=2020100001000028)；[译者说明](https://www.chinawriter.com.cn/wxpl/2014/2014-09-28/219764.html) | 上游载体：print/hardcover/4 volumes；包内仅存 UTF-8 YAML/Markdown 访问说明 | `aux_translation`；核对中文译名、句界、可读性和卷—行对应；不得承担 canonical anchor | `required_reference / reference_only` |

固定书目字段：

```yaml
source_id: ODY-ZHO-WANG2014
title: 奥德赛（全四册）
author: 荷马（传统归属）
edition: 上海人民出版社，2014-07-01，古希腊语—汉语对照，全四册，2014修订版；版次与印次待实体版权页确认
language: zh-Hans
provider: 上海人民出版社；用户合法持有实体书或受许可平台访问
url: https://www.shsjcb.com/sjcb/view.aspx?id=2020100001000028
license: NOASSERTION
acquisition_mode: reference_only
redistribution: metadata_only
full_text_in_open_repo: false
isbn: "9787208114029"
volumes: 4
contributors:
  translator: 王焕生
```

包内计划只创建：

```text
translations/zh-Hans/ody-zho-wang2014/reference-only/README.md
```

该 README 记录书目、实体书访问方式、卷/页定位规则和权利边界；它是项目说明，不是取得的译文文件，因此不创建来源文件 `SOURCE_RECORD`，也不写 checksum。

本轮没有核验到出版社或图书馆提供的开放许可全文下载。授权在线阅读或应用内缓存不等于可导出的开放来源文件。若未来由用户合法提供本地文件：

- 按真实提供者和真实格式登记；
- 四册若为四个文件，必须分别建立四个 `file_id` 和四个 SHA-256；
- 正文保持本地受限，不进入开源仓库；
- 多册引用必须包含 `source_id + edition + printing + volume + page`。

书目冲突需保留为 `known_issues`：不同平台目前出现 1070/1078 页、2014-06-01/2014-07-01 和责任者字段差异。计划身份以出版社页面为首要入口，最终以实体版权页锁定，不用聚合平台字段覆盖。

### 5.5 Historical references

历史资料分成一个可复现数据集和一组 link-only 权威入口。纳入本表只表示来源身份获准登记，不表示已经从中形成任何关于《奥德赛》的历史结论。

#### 5.5.1 可获取历史数据集

| `source_id` | title | edition | provider | URL | file format | intended usage | priority / mode |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `CTX-GEO-PLEIADES-R4-1` | *Pleiades Gazetteer Datasets* | Version 4.1，2025-05-28；DOI `10.5281/zenodo.15540082`；release commit `b6a6790` | Pleiades / Institute for the Study of the Ancient World, NYU；Zenodo 归档 | [Pleiades 下载说明](https://pleiades.stoa.org/downloads)；[Zenodo 4.1 record](https://zenodo.org/records/15540082) | 版本化 ZIP；包内含 JSON、GIS CSV、RDF、README/许可等 | `canonical_place_authority`；以后只用于地名 ID、坐标、名称和时代标签的权威映射，不产生原著事实；数据许可按 release 文件核验，预期 CC BY 3.0 | `required_reference / byte_acquisition` |

计划物理资产：

| `file_id` | provider asset | 计划本地路径 | 规则 |
| --- | --- | --- | --- |
| `CTX-GEO-PLEIADES-R4-1-RAW-RELEASE-ZIP` | Zenodo 4.1 record 中的正式 release ZIP；执行时按记录返回的精确资产名登记 | `references/historical_context/ctx-geo-pleiades/raw/ctx-geo-pleiades-r4-1__raw__release.zip` | 父目录按 `resource_id` 建立；不使用日更 `pleiades-places-latest.json.gz` 代替编号版；原始 ZIP 不原地解压覆盖 |

Pleiades 4.1 的发行说明记录 41,480 个 place resources。官方说明 JSON 是唯一包含全部已发布 place/name/location/connection 属性的完整导出，GIS CSV 是便利但不完整的序列化。因此若后续只派生一种机器工作副本，优先从编号版中的 JSON 生成，并把转换留到 normalization 阶段。Phase 1-C 只保存原始 ZIP，不持久展开数万 JSON 文件，否则会立即触发数万条逐文件记录义务。

#### 5.5.2 Link-only 历史与方法入口

以下记录没有本地来源文件，`source_id` 为 `N/A`；使用既有 `resource_id` 写入 `metadata/resources.yaml`，不创建 `SOURCE_RECORD` 或 checksum。

| `source_id` | `resource_id` | title | edition | provider | URL | file format | intended usage |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `N/A` | `CTX-ORAL-HMT` | Homer Multitext：About / project methodology | 持续更新网页；访问日期入记录 | Homer Multitext / Center for Hellenic Studies | [项目说明](https://www.homermultitext.org/about/) | link-only HTML | 口头传统与多文本方法论入口；具体见证必须另建条目 |
| `N/A` | `CTX-ORAL-PARRY` | Milman Parry Collection of Oral Literature | 馆藏目录持续更新 | Harvard Library | [馆藏页](https://library.harvard.edu/collections/milman-parry-collection-oral-literature) | link-only catalog | 比较性口头传统档案入口；音频、转写、影像需逐项核权 |
| `N/A` | `CTX-ORAL-LORD` | *The Singer of Tales* | Online 2nd edition, 2000 | Center for Hellenic Studies / Harvard University Press | [持久标识](http://nrs.harvard.edu/urn-3:hul.ebook:CHS_LordA.The_Singer_of_Tales.2000) | link-only HTML/EPUB landing | 口头诗学背景；页面标示由 HUP 授权发布，未核权前不复制整本进入仓库 |
| `N/A` | `CTX-ARCH-DARTMOUTH` | Aegean Prehistoric Archaeology | 持续更新教学资源 | Dartmouth College | [资源入口](https://sites.dartmouth.edu/aegean-prehistory/) | link-only HTML | 晚期青铜时代与早期铁器时代考古背景入口 |
| `N/A` | `CTX-ARCH-MET-MYC` | Mycenaean Civilization | 在线馆藏论文 | The Metropolitan Museum of Art | [Met essay](https://www.metmuseum.org/essays/mycenaean-civilization) | link-only HTML | 迈锡尼物质文化背景；文章和对象图像权利分开核验 |
| `N/A` | `CTX-ARCH-MET-GEO` | Geometric Art in Ancient Greece | 在线馆藏论文 | The Metropolitan Museum of Art | [Met essay](https://www.metmuseum.org/essays/geometric-art-in-ancient-greece) | link-only HTML | 后宫殿、早期铁器与古风时代物质文化背景；文章和对象图像分权 |
| `N/A` | `CTX-ARCH-BM-MYC` | Greece: Minoans and Mycenaeans | 持续更新展厅页 | British Museum | [gallery page](https://www.britishmuseum.org/collection/galleries/greece-minoans-and-mycenaeans) | link-only HTML | 博物馆物质文化发现入口；对象、图像和页面文字逐项核权 |
| `N/A` | `CTX-ARCH-BM-1050` | Greece 1050–520 BC | 持续更新展厅页 | British Museum | [gallery page](https://www.britishmuseum.org/collection/galleries/greece-1050-520-bc) | link-only HTML | 早期铁器至古风时代物质文化发现入口；自动访问失败不得误报为 acquired |
| `N/A` | `CTX-GEO-IDAI` | iDAI.gazetteer | Web application/API；具体版本与访问日期入记录 | German Archaeological Institute | [iDAI.gazetteer](https://gazetteer.dainst.org/app/) | link-only web/API JSON | Pleiades 之外的地名 ID 交叉映射；没有固定全量快照时不假装可复现数据包 |
| `N/A` | `CTX-MAP-AWMC` | Ancient World Mapping Center Maps | 持续更新目录 | Ancient World Mapping Center, UNC | [地图入口](https://awmc.unc.edu/maps/) | link-only catalog | 发现可引用地图或数据集；每个实际资产需单独登记许可和版本 |

Met、British Museum、Dartmouth、HMT、Parry、CHS、iDAI 和 AWMC 入口在本轮只登记，不进行整站抓取。以后若某个具体 PDF、数据文件、音频、图像或 HTML 快照需要落盘，必须新建独立 `source_id` 和文件记录，并做单项权利检查。

### 5.6 Manifest 候选的本轮去向

`SOURCE_MANIFEST.md` 中未进入 Phase 1-C 最小获取集的候选必须显式保留，避免“未列出”等同于“被删除”。以下项目状态统一为 `deferred`，不进入 Gate S1-C 完成率：

| ID | 既有角色 | Phase 1-C 处置 | 推迟原因与重新启用条件 |
| --- | --- | --- | --- |
| `ODY-ZHO-CHEN2022` | `aux_translation` | `deferred / reference_only` | 王焕生 2014 已承担首选中文参考；未来需要第二中文注释本且已核验具体版权页时启用 |
| `ODY-ZHO-YANG2019` | `aux_translation` | `deferred / reference_only` | 仅作可选译名史与散文表达对照；未来批准第三校验本时启用 |
| `ODY-ENG-BUTLER-POWER-NAGY-PERSEUS-ENG4` | `aux_translation` | `deferred` | 与 PG1727 是不同数字文本；只有需要 Butler 数字版本比较并完成 edition/year 核验时获取 |
| `REF-ODY-DCC` | `textual_reference` | `deferred / link_only` | 覆盖不完整；未来遇到具体语法或注释复核任务时逐项登记 |
| `REF-GRC-LOGEION` | `textual_reference` | `deferred / discovery_only` | 聚合词典权利不同；未来只做受控查询，不在本轮抓取词典库 |
| `REF-ODY-PAPYRI-DISCOVERY` | `discovery_only` | `deferred / link_only` | 只有出现具体异文/见证问题时才启用发现入口 |
| `REF-PAPYRI-VERIFY` | `textual_reference` | `deferred / link_only` | 需要明确的 DCLP/Trismegistos/馆藏号后才逐项建立见证记录 |

`deferred` 项一旦重新启用，必须通过本文件第 7 节的 preflight，并在获取前从 `deferred` 改为明确的 `required_*` 或 `optional_aux`；不得直接绕过来源审批。

## 6. 获取批次与落盘顺序

### 6.1 Batch A：Perseus 核心四文件

1. 解析并固定一个 `canonical-greekLit` commit；
2. 获取 Greek TEI、English TEI、textgroup CTS、work CTS；
3. 四文件只写入各自 `raw/` 目录；
4. 为四文件分别创建 draft `SOURCE_RECORD`；
5. 记录同一 `upstream_commit`、实际 `retrieval_url`、字节数和 SHA-256；
6. 完成 XML、编码、24 Book 与 locator 检查。

Batch A 未通过时，不进入任何文本规范化或对齐。

### 6.2 Batch B：Murray 页面影像

1. 从两个 Internet Archive item 的 metadata 中解析可用 PDF 资产；
2. 记录实际资产名、媒体类型、字节数和生成状态；
3. 获取卷一、卷二 PDF 并分别登记；
4. 两条文件记录使用 `state: scan`，同时保留物理目录 `raw/` 的不可变字节策略；
5. 检查 PDF 可打开、页数大于零、页面序列可访问；
6. 为 Book 23 已知问题建立只读复核任务，不在 raw TEI 中改字节。

### 6.3 Batch C：中文 reference-only 登记

1. 将出版社页面、ISBN、四册信息和权利边界写入 `sources.yaml` / `rights.yaml`；
2. 创建 `reference-only/README.md`，不保存译文正文；
3. 实体书可用时，人工核验四册版权页、版次、印次和册次覆盖；
4. 若实体信息与聚合页面冲突，以版权页为准并记录差异。

### 6.4 Batch D：历史资料最小集

1. 从 Zenodo DOI 记录解析 Pleiades 4.1 的精确 ZIP 资产；
2. 获取并登记版本化 ZIP；
3. 将本计划列出的 link-only 历史/方法入口写入 `resources.yaml`；
4. 不抓取入口页面正文，不从背景资料推导原作事实。

### 6.5 Batch E：可选英文辅助本

只有 Batch A–D 完成后，才可按需获取 PG1727 UTF-8 TXT。该文件缺失不阻断 Gate S1-C，也不得改变 Murray 英译的 `primary_working_text` 身份。

## 7. 下载与登记流程

### 7.1 Preflight

每个实际字节资产下载前检查：

- `source_id` 已在批准清单中；
- `file_id` 在全包唯一；
- provider、canonical URL、retrieval URL 和预期格式已确定；
- 目标路径位于正确 `raw/` 目录且不存在未处理的同名已批准文件；
- 许可状态至少能写成明确的 SPDX ID、`NOASSERTION` 或项目 `LicenseRef-*`；
- mutable URL 已被 commit、tag、DOI record 或 provider asset ID 冻结。

### 7.2 原始字节写入

- 下载先写同目录临时文件，成功结束后再原子命名为规范文件名；
- HTTP 失败、连接中断或校验失败时删除临时文件，不创建零字节正式文件；
- raw 文件保存 provider 返回的实际字节，不统一换行、不移除 BOM、不解压后冒充原文件；
- 重试写入 `acquisition_log.jsonl`，不能覆盖之前失败记录。

### 7.3 单文件记录

每个本地来源文件创建一条 `metadata/records/<file_id_slug>.source.yaml`，至少完整填写：

- `source_id`
- `title`
- `author`
- `edition`
- `language`
- `provider`
- `url`
- `license`
- `checksum`

并同时填写 `file_id`、`file_path`、`media_type`、`bytes`、`role`、`state`、`retrieved_at`、`provider_identity.upstream_commit` 或外部资产 ID、`known_issues` 和 `record_status`。

- Greek、English、CTS metadata 和 Pleiades 原始包使用 `state: raw`；
- Murray 页面影像使用 `state: scan`，即使其不可变字节物理存放在资源目录的 `raw/` 子目录；
- `record_status` 必须按 `draft -> verified -> approved` 逐级更新，不能因文件下载成功直接跳到 `approved`。

### 7.4 获取日志建议格式

```json
{"event_id":"ACQ-<timestamp>-<sequence>","source_id":"<SOURCE-ID>","file_id":"<FILE-ID>","started_at":"<ISO-8601>","completed_at":null,"canonical_url":"https://...","retrieval_url":"https://...","provider_version":"<commit|tag|record-id>","http_status":null,"bytes":null,"sha256":null,"result":"started|succeeded|failed","error_code":null}
```

日志不保存来源正文、授权 cookie、token 或临时签名 URL。

## 8. 下载完成后的检查流程

### 8.1 文件完整性检查

每个 `byte_acquisition`、`shared_metadata_asset` 或 `conditional_audit_asset` 必须通过：

1. 文件存在且大小大于 0；
2. 实际媒体类型与扩展名、HTTP Content-Type 和计划格式不冲突；
3. XML 可由 namespace-aware parser 完整解析；
4. ZIP 可列目录并完成压缩完整性测试；
5. PDF header、尾部结构与页树可读取，页数大于 0；
6. 文件不是登录页、错误页、限流页或 GitHub HTML 包装页伪装成 XML/PDF/ZIP；
7. provider 身份、版本、URN/DOI/asset ID 与计划记录一致；
8. 下载字节数与 provider 给出的大小一致；若 provider 未给大小，明确记为 `not_provided`，不能伪造期望值。

任何检查失败时：

- `record_status` 保持 `draft`；
- 在 `acquisition_log.jsonl` 写失败事件；
- 在 `source_quality_report.md` 写阻断项；
- 不生成 normalized 文件；
- 不把失败文件加入批准 checksum 清单。

### 8.2 SHA-256 记录

对每个本地原始文件：

1. 对**实际保存的原始字节**计算 SHA-256；
2. YAML 记录为 `sha256:<64位小写十六进制>`；
3. `metadata/checksums/checksums.sha256` 记录为 `<64hex>  <relative-path>`；
4. 记录文件大小和取得时间；
5. 写完清单后立即反向验证一次；
6. 相同 URL 再次获取但摘要变化时，生成差异事件，不静默覆盖旧批准记录。

压缩包与解压后的派生文件分别计算摘要。原始 ZIP 的 checksum 不能代替未来解压/规范化文件的 checksum。

### 8.3 编码检查

#### XML / TEI

- 读取 XML declaration 与实际字节编码；
- 以声明编码严格解码，禁止用 replacement mode 隐藏非法字节；
- 检查是否出现由错误解码产生的 `U+FFFD`；
- 核对 TEI root、namespace、`xml:lang` 和 header；
- BOM 若存在只记录，不在 raw 文件中删除；
- UTF-8、Unicode NFC、换行统一只能发生在后续 normalized 副本。

#### TXT / JSON / CSV / YAML / Markdown

- 记录 provider 声明的编码；未声明时检测并人工确认；
- JSON 必须完整解析；CSV 必须按 provider schema 解析，不能用电子表格软件的默认编码作为判断依据；
- 项目自己创建的 YAML/Markdown 使用 UTF-8、LF；
- 字符替换、智能引号统一或 NFC 转换不在 raw 阶段执行。

#### PDF / ZIP / 图像

二进制文件不做文本编码推断；只检查容器完整性、媒体类型和内部文件的独立编码声明。

### 8.4 Book/Line 结构检查

#### A. Greek `perseus-grc2`

必须检查：

- CTS identity 等于 `urn:cts:greekLit:tlg0012.tlg002.perseus-grc2`；
- citation scheme 为 `book.line`；
- 恰有 Book 1–24，编号不缺失、不重复、顺序正确；
- 每卷 line locator 为可解析的正整数；
- 每卷内 line locator 单调递增且不重复；
- 所有跳号、重复、倒序、空 Book 和异常标签均输出明细；
- #1652、#1655 涉及的异常进入 `known_issues` 并与 Murray 页面影像复核；
- 未经人工分类的 gap/duplicate/order anomaly 一律阻断，不自动补行、重编号或删标签。

检查结果只能说明结构是否可引用，不构成剧情、人物或文学分析。

#### B. English `perseus-eng3`

必须检查：

- CTS identity 等于 `urn:cts:greekLit:tlg0012.tlg002.perseus-eng3`；
- citation scheme 为 `book.card`；
- 恰有 Book 1–24；
- 每卷 card locator 可解析、唯一且按原生顺序排列；
- `book.line` 检查结果明确写 `not_applicable`；
- 不把 card 连续性、card 值或 Atlas 页面 chunk 当成希腊文行号。

English 到 Greek 的 line range 映射在 Phase 1-C 中保持 `not_started`。

#### C. Chinese `ODY-ZHO-WANG2014`

本轮没有数字全文，因此自动 Book/Line 检查为 `not_applicable_reference_only`，不能写成 `passed`。实体书可用时只做人工书目结构检查：

- 全四册均存在；
- 每册版权页的版次、印次、册次和 ISBN 已记录；
- 24 Book 的册次覆盖可人工核对；
- 页码引用始终带 volume；
- “译诗与原诗对行”只作为待人工核验的版本特征，不能假装已有自动行级对齐。

#### D. Scans 与 historical references

- Murray scans 检查卷次、页序和可见的印刷定位，不把 OCR 行号当 CTS line；
- Pleiades 检查 release version、目录结构、JSON/CSV/RDF 可解析性和许可文件，不适用 Book/Line；
- link-only 资源只检查 URL、provider、访问日期和资源角色，不适用 checksum 与 Book/Line。

### 8.5 交叉文件身份检查

Perseus 核心四文件还必须通过：

- 四个文件 `upstream_commit` 完全一致；
- textgroup/work CTS 元数据包含目标 work 与 `grc2` / `eng3` 版本；
- Greek/English TEI header 的题名、贡献者、语言和版本不与 CTS 元数据冲突；
- Scaife canonical identity 与本地文件记录一致；
- provider header 中的拼写或旧目录差异原样保留在 provider metadata，不擅自改成另一数字版本身份。

## 9. Phase 1-C 完成条件

### 9.1 Gate S1-C：Source Acquisition Complete

只有以下条件全部满足，Phase 1-C 才能标记为 `completed`：

- [ ] Gate S1-B 已 `approved`；
- [ ] 本计划已由项目负责人批准；
- [ ] Greek TEI、English TEI、textgroup CTS、work CTS 四个核心文件来自同一 pinned commit；
- [ ] 四个核心文件均存在、非空、格式正确，并有独立 `file_id`、`SOURCE_RECORD` 和 SHA-256；
- [ ] Greek 通过 24 Book、Book.Line 顺序/重复/缺口检查，所有异常都有明确状态；
- [ ] English 通过 24 Book 与 Book.Card 检查，并明确 Book/Line 为 `not_applicable`；
- [ ] #1652、#1655 已写入质量报告，相关异常已用 Murray 页面影像复核，并形成获得人工批准的保留、修正或版本例外处置结论；
- [ ] 两册 Murray 扫描的身份、完整性和 SHA-256 已登记；
- [ ] `ODY-ZHO-WANG2014` 已按 `reference_only / metadata_only` 登记，四册、ISBN、版次/印次状态和使用边界明确；
- [ ] 未把任何未获开放许可的中文译文正文放入开源目录；
- [ ] Pleiades 4.1 编号版资产已固定、获取、验证并登记；
- [ ] Scaife、legacy Perseus Catalog、HMT、Parry、Lord、Dartmouth、Met、British Museum、iDAI、AWMC 的 link-only 资源记录已写入 `resources.yaml`；
- [ ] 所有本地来源文件都能一对一回到 `file_id`、记录和 `checksums.sha256`；
- [ ] 所有 `required_core`、`required_audit` 和 byte-bearing `required_reference` 文件记录均已完成 `draft -> verified -> approved` 生命周期；
- [ ] 编码、容器、媒体类型和 provider identity 检查全部完成；
- [ ] `acquisition_log.jsonl` 没有未解释的失败或静默覆盖；
- [ ] `source_quality_report.md` 没有未处理的阻断项；
- [ ] 人工评审者将 `metadata/quality/gate_s1c.yaml` 状态批准为 `approved`。

### 9.2 Gate 状态机

```yaml
gate_id: S1-C
phase: source_acquisition
allowed_statuses:
  - draft
  - acquiring
  - verification_failed
  - ready_for_review
  - changes_requested
  - approved
completion_rule: status == approved
```

### 9.3 阻断条件

出现任意一项时不得通过 Gate S1-C：

- 核心 Perseus 文件来自不同 commit 或只记录 mutable branch URL；
- 下载的是 GitHub HTML、登录页或错误页，却按 XML/PDF/ZIP 登记；
- 本地来源文件没有 SHA-256、没有 `SOURCE_RECORD` 或多个文件共用一个 `file_id`；
- Greek 的 Book/Line 异常被自动修补、忽略或未报告；
- #1652、#1655 或其他结构异常仍无获批处置结论；
- English card 被标成 line；
- 中文现代译本正文被当成开放文件下载或写入开源仓库；
- link-only 资源被伪造成本地文件并填写假 checksum；
- Pleiades 使用滚动 `latest` 取代已批准的编号 release；
- raw 文件在获取阶段被清洗、改码、重排或覆盖；
- 获取流程开始进行剧情、人物、场景、改编或剧本分析。

### 9.4 本阶段不要求完成的事项

Phase 1-C 不执行：

- raw 到 normalized 的文本转换；
- Greek 与 English 的 passage 切分或 line/card 对齐；
- 中文译本数字化、OCR 或全文导入；
- `passages.jsonl` 与 `alignments.jsonl` 的内容生成；
- 来源场景划分；
- 剧情、事件、主题或人物分析；
- 剧集规划、现代化表达、剧本或视频制作。

这些工作必须在 Source Package 的后续验证、规范化与 Gate S1 总验收中另行授权。

## 10. 当前状态

```yaml
phase: Phase 1-C
document: 02_SOURCE_ACQUISITION_PLAN.md
plan_status: ready_for_review
execution_status: not_started
files_downloaded_in_this_phase_document_task: 0
source_records_created: 0
checksums_computed: 0
content_analysis_started: false
adaptation_started: false
gate_s1c: draft
```

当前成果仅是可执行资料获取计划。下一步应先评审并批准 Gate S1-B 与本计划；获批后，Phase 1-C 的第一个原子执行批次只能是：锁定一个 Perseus commit，获取并验证 Greek TEI、English TEI 和两级 CTS 元数据四个文件。仍不得进入文本内容分析。
