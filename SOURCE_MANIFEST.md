# 《奥德赛》Source Package 来源清单与定位规范

> 项目：Classic-to-Drama Engine  
> 阶段：Phase 1 / Source Package Design v0.1  
> 文档状态：`draft_recommendation`  
> 核验日期：2026-08-10  
> 当前边界：只设计来源、版本、定位、输入与质量规则；不进行剧情分析，不建立人物数据库，不提出改编方案。

## 1. 文档目的

本文件为《奥德赛》项目建立 L0 来源层契约。它需要回答四个问题：

1. 哪个公开版本承担主工作底本；
2. 古希腊文、英文、中文译本与背景资料分别有什么权限；
3. 任意文本片段如何稳定记录到卷、行、段落与后续场景；
4. 后续 AI 接收什么格式的输入，如何把输出返回到原始证据。

本文件不是来源文本本身，也不表示来源已经下载、校验或批准。所有候选来源在完成文件锁定、完整性检查和人工批准前均保持 `proposed` 状态。

## 2. 核心决策摘要

### 2.1 推荐采用“双层主底本”

| 层级 | 推荐版本 | 稳定身份 | 唯一职责 |
| --- | --- | --- | --- |
| 规范引用脊柱 | A. T. Murray 编校的 1919 年古希腊文版 | `urn:cts:greekLit:tlg0012.tlg002.perseus-grc2` | 提供 24 卷的规范卷—行坐标；裁决所有文本事实引用的位置 |
| 主要 AI 工作文本 | A. T. Murray 1919 年英译 | `urn:cts:greekLit:tlg0012.tlg002.perseus-eng3` | 提供公开、机器可读的主要阅读文本；每个英文单元必须映射到希腊文行范围 |

推荐入口：

- [Scaife Viewer《奥德赛》作品页](https://scaife.perseus.org/library/urn%3Acts%3AgreekLit%3Atlg0012.tlg002/)
- [Murray 1919 古希腊文版](https://atlas.perseus.tufts.edu/library/urn%3Acts%3AgreekLit%3Atlg0012.tlg002.perseus-grc2/)
- [Murray 1919 英译版](https://atlas.perseus.tufts.edu/library/urn%3Acts%3AgreekLit%3Atlg0012.tlg002.perseus-eng3/)
- [Perseus `canonical-greekLit` TEI 仓库](https://github.com/PerseusDL/canonical-greekLit)

这不是两个互相竞争的“主版本”。古希腊文版控制身份和定位，英译版承担工作可读性；二者组成一套来源包，但职责不能互换。

### 2.2 为什么推荐 Murray / Perseus 体系

1. **同版关系清楚**：古希腊文和英译均来自 Murray 1919 两卷本，便于建立版本对照。
2. **定位稳定**：作品、版本和选段都有 CTS URN；规范引用可以精确到 `book.line`。
3. **适合机器处理**：Perseus 提供 EpiDoc/TEI XML，而不是只有扫描页或网页排版。
4. **适合开源复现**：数字文本可按其许可进入公开工作流；固定上游 commit 和文件 SHA-256 后可以重建同一输入。
5. **可以回看页面影像**：当 TEI 行号、字符或注记有争议时，可复核 [1919 卷一扫描](https://archive.org/details/odysseymurray01homeuoft) 与 [1919 卷二扫描](https://archive.org/details/odysseywithengli02home)。

### 2.3 优点与缺点

| 维度 | 优点 | 缺点或风险 | 工程处理 |
| --- | --- | --- | --- |
| 可定位性 | 古希腊文具备规范卷—行 CTS 引用 | Murray 英译的 CTS 子单元实际是 `book.card`，不是逐行节点 | 所有 `canonical_span` 只写古希腊文 URN；英文另存 `english_card_urn` |
| 机器可读性 | TEI XML 保留结构、语言与版本元数据 | 上游仓库仍会修订，`master` 不是字节级固定版本 | 保存上游 commit、获取日期、原始文件 SHA-256 与转换日志 |
| 可读性 | 英译完整、公开、与同版希腊文可对照 | 英语具有 20 世纪初风格，不能代表现代英文表达 | 只把它当证据工作文本；现代语言判断由辅助译本对照 |
| 形式保真 | 保留可回到希腊文的行坐标 | 英文散文无法再现希腊语韵律、程式和全部语义歧义 | 歧义回查希腊文、荷马词典和受控辅助资料 |
| 文本质量 | 有成熟的学术数字基础设施 | 当前仓库公开记录过第 23 卷行号/缺行问题 | 入库时做 24 卷连续性检查，并以扫描页复核异常 |
| 权利管理 | 1919 版与 Perseus 数字编码具有可复用基础 | 古代作品、1919 版、数字编码和网页呈现不是同一个权利对象 | 对 `edition`、`encoding`、`scan`、`metadata` 分开登记权利 |

已知质量问题不得隐去：Perseus 仓库仍有与第 23 卷行号有关的开放问题 [#1652](https://github.com/PerseusDL/canonical-greekLit/issues/1652) 与 [#1655](https://github.com/PerseusDL/canonical-greekLit/issues/1655)。因此本项目不能把“来自 Perseus”直接等同于“零错误”。

### 2.4 不采用 Butler / Gutenberg 作为主底本的原因

[Project Gutenberg #1727](https://www.gutenberg.org/ebooks/1727) 的 Samuel Butler 英译提供 UTF-8 纯文本，下载和清洗非常方便，而且明确标注为美国公版；但它没有可靠的传统行号，段落、电子书位置和文件行号都不能承担学术定位。因此它适合作为公开英文辅助对读本，不适合作为规范引用脊柱。

还必须区分两个 Butler 数字版本：

- `PG1727`：Project Gutenberg 提供的 Butler 文本；
- `perseus-eng4`：Perseus 中经 Timothy Power 与 Gregory Nagy 修订的 Butler 版本。

它们文字与数字身份不同，不能共用一个 `source_id`，也不能把其中一个的定位移植到另一个。

## 3. 来源角色与登记规则

### 3.1 来源角色

| `role` | 含义 | 能否单独支持“原著明确如此” |
| --- | --- | --- |
| `canonical_anchor` | 规范原文与卷—行坐标 | 是；本项目仅限 Murray 1919 希腊文版 |
| `primary_working_text` | AI 主要读取的完整工作译文 | 否；必须携带 `canonical_span` |
| `aux_translation` | 比较译名、句界、语气或歧义 | 否；只进入 `consulted_sources` |
| `textual_reference` | 词典、注释、异文或纸草见证 | 否；用于解释或复核 |
| `historical_context` | 历史、考古、物质文化、口头传统与地理 | 否；不能反向创造文本事实 |
| `discovery_only` | 发现线索的检索入口 | 否；结论必须回查更高等级来源 |

### 3.2 每个来源的必备元数据

```yaml
source_id: ODY-GRC-MURRAY1919
work_id: ODY
role: canonical_anchor
title: The Odyssey, Volume 1-2
language: grc
contributors:
  editor: A. T. Murray
publication:
  year: 1919
  publisher: William Heinemann / G. P. Putnam's Sons
identity:
  cts_urn: urn:cts:greekLit:tlg0012.tlg002.perseus-grc2
  isbn: null
provider:
  name: Perseus Digital Library / Scaife Viewer
  canonical_url: https://atlas.perseus.tufts.edu/library/urn%3Acts%3AgreekLit%3Atlg0012.tlg002.perseus-grc2/
acquisition:
  status: proposed
  retrieved_at: null
  upstream_commit: null
  original_file: null
  bytes: null
  sha256: null
format:
  media_type: application/tei+xml
  encoding: UTF-8
  locator_scheme: book.line
rights:
  edition_status: verify_at_ingestion
  digital_encoding_license: verify_tei_header_and_repository
  repository_policy: open_repo
quality:
  completeness: unverified
  known_issues: []
  qa_report: null
normalization:
  status: not_started
  normalizer_version: null
  normalized_file: null
  normalized_sha256: null
status: proposed
```

### 3.3 版本身份规则

- CTS URN 负责“这是哪部作品、哪个版本、哪个选段”的语义身份。
- 上游 Git commit 与原始文件 SHA-256 负责“本次运行实际使用了哪些字节”的复现身份。
- ISBN、馆藏号或 Project Gutenberg eBook 号负责纸本或外部发行版身份。
- 网页 URL 只是访问入口；可变化的 GitHub 分支 URL 不能代替版本身份。
- 每次重新获取文件都计算新 SHA-256。哈希变化时先生成差异报告，不得静默覆盖。
- `raw` 文件永不原地清洗；任何编码、换行、标点或标签转换只写入 `normalized` 副本并记录转换日志。

### 3.4 权利字段必须拆分

同一来源至少分别记录：

- `underlying_work`：古代作品；
- `edition`：特定编校本；
- `translation`：特定译文；
- `digital_encoding`：TEI、OCR 或电子书文件；
- `metadata`：书目与结构数据；
- `scan_or_image`：页面影像。

站点级许可不能自动覆盖全部内容。Perseus 仓库目前说明默认采用 CC BY-SA 4.0，但正式导入时仍要检查具体 TEI header；Project Gutenberg 的权利标记与其他 Butler 数字版本不能互相替代。

## 4. 建议来源清单

### 4.1 规范原文与主要工作译文

| `source_id` | 资源 | 角色 | 定位粒度 | 项目状态 |
| --- | --- | --- | --- | --- |
| `ODY-GRC-MURRAY1919` | [Murray 1919 古希腊文 `perseus-grc2`](https://atlas.perseus.tufts.edu/library/urn%3Acts%3AgreekLit%3Atlg0012.tlg002.perseus-grc2/) | `canonical_anchor` | `book.line` | `proposed` |
| `ODY-ENG-MURRAY1919` | [Murray 1919 英译 `perseus-eng3`](https://atlas.perseus.tufts.edu/library/urn%3Acts%3AgreekLit%3Atlg0012.tlg002.perseus-eng3/) | `primary_working_text` | `book.card` + 对齐的希腊文行范围 | `proposed` |
| `ODY-SCAN-MURRAY1919-V1` | [1919 卷一页面影像](https://archive.org/details/odysseymurray01homeuoft) | `textual_reference` | 卷/页/印刷行 | `proposed` |
| `ODY-SCAN-MURRAY1919-V2` | [1919 卷二页面影像](https://archive.org/details/odysseywithengli02home) | `textual_reference` | 卷/页/印刷行 | `proposed` |

不得把当前 Loeb 在线修订版混入 `ODY-GRC-MURRAY1919`。如未来引入其他校勘本，必须创建新 `source_id` 并建立异文对照，不能覆盖现有来源。

### 4.2 中文辅助译本

中文译本用于译名、句界、中文可读性和歧义对照，不承担唯一事实锚点。现代中文译本只登记书目信息和本地查阅状态，公开仓库不保存其全文。

| `source_id` | 建议版本 | 用途 | 处理方式 |
| --- | --- | --- | --- |
| `ODY-ZHO-WANG2014` | 荷马著、王焕生译，《奥德赛 = ΟΔΥΣΣΕΙΑ》（全四册；古希腊语—汉语对照），上海人民出版社，2014 年 7 月，ISBN `9787208114029` | **首选中文辅助本**；译者说明采用 Loeb 希腊文本、诗体译文与原诗对行，适合核对卷—行、译名和句界 | `reference_only`；先以实体书版权页锁定版次/印次。参见[译者说明](https://www.chinawriter.com.cn/wxpl/2014/2014-09-28/219764.html)与[版本书目](https://book.douban.com/subject/25900268/) |
| `ODY-ZHO-CHEN2022` | 荷马著、陈中梅译注，《奥德赛》，译林出版社，2022，ISBN `9787544794367` | 第二校验本；利用注释核对语义歧义、专名和文化术语 | `reference_only`；正式登记前复核版权页，不用页码跨版引用 |
| `ODY-ZHO-YANG2019` | 荷马著、杨宪益译，《杨宪益中译作品集：奥德修纪》，上海人民出版社，2019，ISBN `9787208155459` | 可选第三校验本；用于散文表达与译名史对照 | `reference_only`；不能承担逐行定位 |

中文引用规则：

- 文本事实仍引用 `canonical_span`；
- 中文译本只写入 `consulted_sources` 与具体版次定位；
- 页码必须同时带 `source_id + edition + printing + volume + page`；多册本的 `edition_locator.volume` 不得为空；
- 不同印次分页不一致时，页码不得直接继承；
- 若未来需要可公开分发的中文工作文本，应作为独立项目译文创建新的来源与校订记录，不能拼接现有译本。

王焕生 2014 对照本还应登记：

```yaml
publication:
  volumes: 4
format:
  bilingual: grc-zh-Hans
rights:
  open_license: none_verified
  redistribution: metadata_only
  full_text_in_open_repo: false
```

陈中梅、杨宪益等现代中译本采用同样的可审计权利字段；在没有开放许可的情况下，`redistribution` 均保持 `metadata_only`。

### 4.3 英文辅助译本

| `source_id` | 资源 | 用途 | 限制 |
| --- | --- | --- | --- |
| `ODY-ENG-BUTLER-PG1727` | [Samuel Butler / Project Gutenberg #1727](https://www.gutenberg.org/ebooks/1727) | 公开散文对读、清洗流程测试、第二英文措辞 | 另记 `translation_first_published: 1900`、`digital_source_edition: verify_at_ingestion`；没有规范行号；保存下载日期与 SHA-256 |
| `ODY-ENG-BUTLER-POWER-NAGY-PERSEUS-ENG4` | [Perseus `perseus-eng4`](https://atlas.perseus.tufts.edu/library/urn%3Acts%3AgreekLit%3Atlg0012.tlg002.perseus-eng4/) | 经 Power / Nagy 修订的 Butler 对照版 | TEI 来源年份带不确定性；不得把年份写入稳定 ID；与 PG1727 为不同数字文本，必须单独登记 |

若团队以后采购现代英文译本，只能新增为 `aux_translation / reference_only`；不能改变已经批准的规范行坐标。

### 4.4 古希腊文与文本学辅助资源

| `resource_id` | 资源 | 工程用途 | 边界 |
| --- | --- | --- | --- |
| `REF-ODY-PERSEUS-TEI` | [Perseus `canonical-greekLit`](https://github.com/PerseusDL/canonical-greekLit) | 获取 TEI、CTS 元数据和版本结构 | 导入时固定 commit；检查文件级 header 与已知问题 |
| `REF-ODY-DCC` | [Dickinson College Commentaries：Odyssey](https://dcc.dickinson.edu/homer-odyssey/intro/preface) | 部分卷的古希腊文、语法、词汇与教学注释复核 | 覆盖不完整，不能替代全诗底本 |
| `REF-GRC-LOGEION` | [University of Chicago Logeion](https://logeion.uchicago.edu/about) | 查询 LSJ、Autenrieth、Cunliffe 等词典 | 聚合资源权利不同；默认查询使用，不整库抓取 |
| `REF-ODY-PAPYRI-DISCOVERY` | [CHS Homer & the Papyri](https://www-current.chs.harvard.edu/homer-the-papyri-home/) | 发现纸草与异文线索 | 数据时效有限，只作发现入口 |
| `REF-PAPYRI-VERIFY` | [Papyri.info](https://papyri.info/) | 用 DCLP、Trismegistos、馆藏号和 canonical URI 复核具体见证 | 元数据、转写和图像分别登记许可；不能把纸草异文静默写回主底本 |

### 4.5 历史背景资料体系

历史资料必须与文本证据分层。它们可以解释时代、制度、物质文化、口头传统和地理，但不能证明某段原文明确写了什么。

| `resource_id` | 资源 | `context_role` | `authority_tier` | `external_id_scheme` | `access_mode` | `rights_status` | `status` |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `CTX-ORAL-HMT` | [CHS Homer Multitext：项目说明](https://www.homermultitext.org/about/) | `methodological_reference` | `scholarly_project` | `canonical_url` | `open_web` | `item_level_review` | `proposed` |
| `CTX-ORAL-PARRY` | [Harvard Milman Parry Collection](https://library.harvard.edu/collections/milman-parry-collection-oral-literature) | `comparative_archive` | `institutional_archive` | `collection_id` | `open_catalog` | `item_level_review` | `proposed` |
| `CTX-ORAL-LORD` | [The Singer of Tales](https://www-current.chs.harvard.edu/read/lord-albert-bates-the-singer-of-tales/) | `scholarly_synthesis` | `scholarly_publication` | `bibliographic_id` | `link_only` | `item_level_review` | `proposed` |
| `CTX-ARCH-DARTMOUTH` | [Dartmouth Aegean Prehistoric Archaeology](https://sites.dartmouth.edu/aegean-prehistory/) | `archaeology_reference` | `university_resource` | `canonical_url` | `link_only` | `no_open_license_verified` | `proposed` |
| `CTX-ARCH-MET-MYC` | [Met：Mycenaean Civilization](https://www.metmuseum.org/essays/mycenaean-civilization) | `material_culture_reference` | `museum_scholarship` | `canonical_url` | `open_web` | `article_and_object_rights_separate` | `proposed` |
| `CTX-ARCH-BM-MYC` | [British Museum：Minoans and Mycenaeans](https://www.britishmuseum.org/collection/galleries/greece-minoans-and-mycenaeans) | `material_culture_reference` | `museum_scholarship` | `collection_object_id` | `open_web` | `item_level_review` | `proposed` |
| `CTX-ARCH-MET-GEO` | [Met：Geometric Art in Ancient Greece](https://www.metmuseum.org/essays/geometric-art-in-ancient-greece) | `material_culture_reference` | `museum_scholarship` | `canonical_url` | `open_web` | `article_and_object_rights_separate` | `proposed` |
| `CTX-ARCH-BM-1050` | [British Museum：Greece 1050–520 BC](https://www.britishmuseum.org/collection/galleries/greece-1050-520-bc) | `material_culture_reference` | `museum_scholarship` | `collection_object_id` | `open_web` | `item_level_review` | `proposed` |
| `CTX-GEO-PLEIADES` | [Pleiades](https://pleiades.stoa.org/) | `canonical_place_authority` | `primary_authority` | `pleiades_uri` | `open_web_api` | `CC-BY-3.0` | `proposed` |
| `CTX-GEO-IDAI` | [iDAI.gazetteer](https://gazetteer.dainst.org/app/) | `secondary_authority` | `crosswalk` | `idai_gazetteer_id` | `open_web` | `CC-BY_item_check` | `proposed` |
| `CTX-MAP-AWMC` | [Ancient World Mapping Center](https://awmc.unc.edu/maps/) | `cartographic_source` | `institutional_map_source` | `dataset_or_map_id` | `open_catalog` | `dataset_level_review` | `proposed` |

Homer Multitext 必须按材料级路由：项目说明和口头传统方法论页面登记为 `historical_context`；从中取得的具体版本、抄本图像、转写、纸草或异文必须新建独立 `resource_id`，改登为 `textual_reference`，并保存见证编号、具体定位和单项权利。

背景记录必须使用时间层标签，而不是一个模糊的 `homeric_age`：

| 标签 | 资料分类范围 |
| --- | --- |
| `LBA_MYCAENAEAN` | 约前 1600–1100 年的爱琴海晚期青铜时代资料 |
| `POSTPALATIAL_EIA` | 约前 1100–800 年的后宫殿与早期铁器时代资料 |
| `ARCHAIC_PERFORMANCE` | 约前 800–600 年的古风时代与表演传统资料 |
| `HELLENISTIC_EDITING` | 希腊化时期的校勘、注释与文本整理资料 |
| `ROMAN_PAPYRUS` | 罗马时期纸草及相关文本见证 |
| `MEDIEVAL_MANUSCRIPT` | 中世纪抄本及相关文本见证 |
| `MODERN_SCHOLARSHIP` | 现代语言学、考古学、文献学与接受史研究 |

`LATER_TRANSMISSION` 可作为 `ROMAN_PAPYRUS` 与 `MEDIEVAL_MANUSCRIPT` 的父级检索标签，但不能成为记录上的唯一时间标签。`subject_period_tags` 允许多值；研究对象年代、见证物年代和资源出版年代必须分开：

```yaml
temporal:
  subject_period_tags: []
  witness_date:
    start: null
    end: null
    certainty: null
  publication_date: null
```

这些标签只是资料分类桶，不预先宣布单一成书年代，也不把后世材料自动投射到诗中。现代论文或档案的 `publication_date` 不能代替其所讨论对象的 `subject_period_tags`；纸草或抄本还必须单独填写 `witness_date`。

## 5. 文本定位规则

### 5.1 定位层级与优先级

| 优先级 | 定位 | 稳定性 | 用途 |
| --- | --- | --- | --- |
| 1 | 规范希腊文 `Book.Line` + CTS URN | 最高 | 所有文本事实的主引用 |
| 2 | 版本原生定位，如英文 `book.card`、纸本页码 | 版本内稳定 | 回到具体译本或页面 |
| 3 | 项目 `passage_id` / `paragraph_id` | 项目版本内稳定 | 数据库、AI 分包与检索 |
| 4 | 项目 `source_scene_id` | 人工解释性 | 后续文本结构分析；不能取代原文坐标 |

禁止把 GitHub 文件行号、网页滚动位置、电子书 location、搜索结果片段或聊天消息位置作为来源引用。

### 5.2 卷（Book）

- 字段名：`book`；类型为整数；允许范围 `1..24`。
- 人类显示：`Od. 1`、`Od. 23`；不补零。
- 内部 ID：`B01`、`B23`；固定两位，便于排序。
- 不允许罗马数字、中文卷名和阿拉伯数字在结构化字段中混用；它们只能作为显示别名。
- 跨卷引用必须拆成两个或更多 `SourceSpan`，不得构造跨卷单一 CTS range。

### 5.3 行（Line）

- `line_start` 与 `line_end` 只表示 `ODY-GRC-MURRAY1919` 的规范希腊文行号。
- 单行时二者相同；范围必须包含端点。
- 人类显示：`Od. 1.1–10`。
- 项目内部显示：`ODY.B01.L0001-L0010`。
- CTS 表达：`urn:cts:greekLit:tlg0012.tlg002.perseus-grc2:1.1-1.10`。
- 行号必须来自 TEI 的结构标记并通过连续性校验，不能由页面 OCR 或英译行距推算。
- 英译 `perseus-eng3` 只保存其原生 card URN，例如 `english_card_urn`；不得把 card 编号命名为 `english_line`。

规范引用示例只演示位置，不包含任何文本分析：

```yaml
canonical_span:
  source_id: ODY-GRC-MURRAY1919
  book: 1
  line_start: 1
  line_end: 10
  human_ref: Od. 1.1–10
  cts_urn: urn:cts:greekLit:tlg0012.tlg002.perseus-grc2:1.1-1.10
```

### 5.4 段落（Paragraph）与工作片段（Passage）

段落不是跨版本规范单位。译者、编辑、网页和电子书可能在不同位置分段，因此段落 ID 必须包含来源身份。

建议格式：

- 来源段落：`PAR-ODY-ENG-MURRAY1919-B01-0001`；
- 项目工作片段：`SP-ODY-B01-L0001-L0010-001`；
- Butler 段落：`PAR-ODY-ENG-BUTLER-PG1727-B01-0001`。

每个 `SourcePassage` 至少保存：

```yaml
passage_id: SP-ODY-B01-L0001-L0010-001
source_id: ODY-ENG-MURRAY1919
canonical_span:
  book: 1
  line_start: 1
  line_end: 10
  cts_urn: urn:cts:greekLit:tlg0012.tlg002.perseus-grc2:1.1-1.10
native_locator:
  scheme: book.card
  urns: []
paragraph_ids: []
raw_anchor:
  raw_file_sha256: null
  char_start: null
  char_end: null
normalization:
  version: null
  text_sha256: null
text: "<source text omitted from this design example>"
```

规则：

- `passage_id` 一旦发布不得因文字修正而复用给另一段；内容变化通过版本字段处理。
- 段落边界变更时保留旧映射，不批量重命名下游对象。
- 段落和 passage 必须至少映射到一个 `canonical_span`；无法精确对齐时标为 `approximate` 并给出原因。
- 页码只存放在 `edition_locator`，同时记录版次与印次，不能成为唯一引用。

### 5.5 场景编号（Scene）

“原文场景”和“剧本场景”属于不同数据层，必须使用不同命名空间。

| 类型 | ID 格式 | 创建阶段 | 性质 |
| --- | --- | --- | --- |
| 来源场景 | `SS-ODY-B01-001` | 后续文本/戏剧结构分析 | 人工划分的解释性单元；必须包含一个或多个 `canonical_span` |
| 剧本场景 | `DS-ODY-EP001-001` | 剧集规划或剧本阶段 | 改编生产单元；引用来源场景、事件或改编决策 |

Phase 1 只保留编号规则，**不创建任何实际场景记录**。将来创建 `source_scene_id` 时必须记录：

```yaml
source_scene_id: SS-ODY-B01-001
scene_no_within_book: 1
canonical_spans: []
boundary_basis: []
boundary_note: null
status: draft
reviewed_by: null
```

`boundary_basis` 以后可以使用 `location_change`、`time_change`、`speaker_frame_change`、`narrative_mode_change` 或 `editorial_split`，但这些都是分析性标注，不得写入 CTS URN。

### 5.6 跨版本对齐记录

```yaml
alignment_id: ALN-ODY-B01-L0001-L0010
canonical_span:
  source_id: ODY-GRC-MURRAY1919
  cts_urn: urn:cts:greekLit:tlg0012.tlg002.perseus-grc2:1.1-1.10
members:
  - source_id: ODY-ENG-MURRAY1919
    native_refs: []
    mapping_type: overlap
    confidence: null
  - source_id: ODY-ZHO-WANG2014
    native_refs: []
    mapping_type: pending_manual_alignment
    confidence: null
alignment_status: draft
reviewed_by: null
```

`mapping_type` 仅允许：`exact`、`overlap`、`approximate`、`unmapped`、`pending_manual_alignment`。模型不得把 `approximate` 自动升级为 `exact`。

## 6. 后续 AI 分析输入格式建议

### 6.1 推荐组合

- `sources.yaml`：来源注册表与版本、权利、文件身份；
- `passages.jsonl`：一行一个 `SourcePassage`，便于流式处理和增量更新；
- `alignments.jsonl`：希腊文、英文和受控中文对照映射；
- `analysis_packet.yaml`：单次 AI 任务的封闭输入包；
- `checksums.sha256`：实际输入文件的字节身份；
- `normalization_log.jsonl`：从 raw 到 normalized 的每一步变换。

默认分包建议以 20–40 个规范希腊文行为一个候选窗口，并在不改变 `canonical_span` 的前提下调整到完整句界；必要时提供少量前后文。窗口大小只是运行参数，不能成为新的文献坐标。

### 6.2 单次 AI 输入包

```yaml
schema_version: c2d.source-analysis-packet.v1
packet_id: PKT-ODY-B01-L0001-L0010-V001
work_id: ODY
task_type: future_source_analysis
phase_boundary:
  allow_plot_analysis: false
  allow_character_database_write: false
  allow_adaptation: false
canonical:
  source_id: ODY-GRC-MURRAY1919
  book: 1
  line_start: 1
  line_end: 10
  cts_urn: urn:cts:greekLit:tlg0012.tlg002.perseus-grc2:1.1-1.10
texts:
  - role: canonical_anchor
    source_id: ODY-GRC-MURRAY1919
    native_ref: urn:cts:greekLit:tlg0012.tlg002.perseus-grc2:1.1-1.10
    language: grc
    distribution: open_repo
    text_sha256: null
    text: "<source text inserted only after verified ingestion>"
  - role: primary_working_text
    source_id: ODY-ENG-MURRAY1919
    native_ref: null
    aligned_to: urn:cts:greekLit:tlg0012.tlg002.perseus-grc2:1.1-1.10
    language: en
    mapping_type: overlap
    distribution: open_repo
    text_sha256: null
    text: "<aligned source text inserted only after verified ingestion>"
  - role: aux_translation
    source_id: ODY-ZHO-WANG2014
    native_ref: null
    aligned_to: urn:cts:greekLit:tlg0012.tlg002.perseus-grc2:1.1-1.10
    language: zh-Hans
    mapping_type: pending_manual_alignment
    distribution: local_reference_only
    text_sha256: null
    text: null
context_resources:
  - resource_id: null
    context_role: null
    authority_tier: null
    canonical_url: null
    external_ids: []
    citation_locator: null
    subject_period_tags: []
    witness_date:
      start: null
      end: null
      certainty: null
    rights_scope: null
    status: proposed
provenance:
  source_registry_version: null
  normalizer_version: null
  built_at: null
instructions:
  - "只使用 texts 中提供的文本建立文本性结论。"
  - "每个结论必须返回 canonical.cts_urn 或更小的有效规范范围。"
  - "辅助译本只能用于比较，不得取代 canonical_anchor。"
  - "背景资料不得转写为原著事实。"
  - "证据不足时返回 unknown，不得补写。"
```

在 Phase 1 期间，`task_type` 只允许来源清洗、对齐、完整性检查和格式验证；`future_source_analysis` 只是保留给下一阶段的模式示例，当前不得执行。

### 6.3 AI 输入硬约束

1. 没有 `source_id`、`canonical_span`、原始文件 SHA-256 或规范化版本的片段不得进入正式分析。
2. 模型只能读取本包列出的材料，不能凭预训练记忆补充“原著内容”。
3. 主工作英译必须与希腊文行范围一起提供；英文 card 不能冒充行号。
4. 受限辅助译本如果未获准进入模型输入，只提供元数据和人工校验结果，不传递正文。
5. 背景资料使用独立 `context_resources`，其结论必须标记 `context_claim`，不能进入 `text_fact`。
6. 输入过长时按规范行范围拆包；跨包结论必须列出全部相关 `packet_id`。
7. 同一任务使用的来源注册表、规范化规则和 prompt 都必须有版本号。

## 7. 建议的 Source Package 目录

```text
projects/odyssey/sources/
├── SOURCE_MANIFEST.md
├── metadata/
│   ├── sources.yaml
│   └── rights.yaml
├── raw/
│   ├── open/
│   └── reference-only/README.md
├── normalized/
│   ├── grc/
│   └── en/
├── indexes/
│   └── passages.jsonl
├── alignments/
│   └── alignments.jsonl
├── checksums/
│   └── checksums.sha256
├── logs/
│   └── normalization_log.jsonl
└── quality/
    └── source_quality_report.md
```

`reference-only` 目录只保存说明、书目信息与本地挂载约定，不保存现代中文译本正文。原始公开文件、规范化文本、索引、对齐和质量报告彼此分离。

## 8. Phase 1 来源就绪门槛

只有同时满足以下条件，才能进入剧情、事件或人物分析：

- [ ] 项目负责人批准“双层主底本”及各辅助来源的权限；
- [ ] 古希腊文和 Murray 英译的具体上游 commit 已固定；
- [ ] 原始文件已保存 SHA-256、获取时间、格式和许可信息；
- [ ] 24 卷存在性、顺序和希腊文行号连续性已完成自动检查；
- [ ] 已知第 23 卷问题已与页面影像复核并形成明确处理记录；
- [ ] raw 与 normalized 文件可以双向追溯，所有转换都有日志；
- [ ] 每个 `passage_id` 都能返回有效 `canonical_span`；
- [ ] Murray 英译 card 与希腊文行范围已建立可审计映射；
- [ ] 中文辅助本的具体版次、印次和使用方式已由人工确认；
- [ ] `sources.yaml`、`passages.jsonl`、`alignments.jsonl` 通过模式校验；
- [ ] `source_quality_report.md` 没有未处理的阻断项；
- [ ] Gate S1 获得人工 `approved` 状态。

## 9. 当前阶段结论

当前只形成来源工程方案，尚未执行文本下载、规范化、段落切分、场景划分或任何内容分析。

建议待项目负责人批准后，下一小步仅做一件事：锁定 Perseus `canonical-greekLit` 的具体版本，获取 `perseus-grc2`、`perseus-eng3` 与 CTS 元数据文件，并生成原始文件校验清单；仍不进入剧情和人物分析。
