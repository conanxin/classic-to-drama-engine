# 《奥德赛》Source Package 实体目录规范

> 项目：Classic-to-Drama Engine  
> 阶段：Phase 1-B / Source Package 实体化  
> 规范版本：`c2d.odyssey-source-package.v1`  
> 文档状态：`ready_for_review`  
> 日期：2026-08-10  
> 当前边界：只定义目录、文件身份、元数据记录和验收规则；不下载文本，不分析内容，不建立人物数据库，不进行短剧改编。

## 1. 文档目的

本文件把 `SOURCE_MANIFEST.md` 中的来源设计转换为可直接实施和检查的资料目录规范。它只回答四个工程问题：

1. 来源文件应放在哪里；
2. 每类文件承担什么职责、采用什么格式、如何命名；
3. 每一个本地来源文件如何用 `SOURCE_RECORD.yaml` 记录身份和字节校验值；
4. 什么条件满足后，Phase 1-B 才可以被标记为完成。

本文件不替代 `SOURCE_MANIFEST.md`：

- `SOURCE_MANIFEST.md` 决定采用哪些来源、各来源的角色和引用权限；
- 本文件决定这些来源进入项目后如何落盘、登记和验收；
- 两份文档冲突时，不得自行猜测，应先修订并统一版本。

## 2. 适用范围与目录根

### 2.1 逻辑根

本文统一使用 `source/` 表示一个作品的 Source Package 逻辑根。

当前项目在 Phase 0 和 Phase 1 中曾建议使用：

```text
projects/odyssey/sources/
```

若仓库沿用该路径，则该目录直接等价于本文的 `source/`，不得再创建 `sources/source/` 或 `source/sources/`。以后迁移到其他作品时，只替换项目路径，不改变包内四个顶层目录。

`SOURCE_MANIFEST.md` 第 7 节的目录树是 Phase 1 的概念草图；本文作为 Phase 1-B 的物理落盘规范，取代该草图中的具体层级，但不改变其中的 raw 不可变、normalized 可追溯、权利分离和校验值规则。原草图的顶层 `raw/` 与 `normalized/` 在本文中下沉到具体原文、译本或参考来源目录内。

### 2.2 四个顶层资料域

`source/` 下必须包含且仅以以下四个目录承载来源资料：

| 目录 | 职责 | 是否允许存放来源正文 |
| --- | --- | --- |
| `original_text/` | 原作语言文本及其规范化副本 | 是 |
| `translations/` | 各语言译本及其规范化副本或受限使用说明 | 是，但受许可和访问策略约束 |
| `metadata/` | 来源记录、校验值、索引、对齐、日志和质量状态 | 否 |
| `references/` | 文本学、历史背景和发现型参考资源 | 仅在权利允许且已登记时可以 |

`README.md` 可以位于 `source/` 根目录，用于说明包版本和使用入口；除该文件外，不得把来源文件散放在根目录。

## 3. `source/` 目录结构设计

### 3.1 规范目录树

以下是 Phase 1-B 锁定的目标结构。尖括号表示待来源实体化时替换的变量，不表示现在需要创建或下载文件。

```text
source/
├── README.md
├── original_text/
│   └── grc/
│       └── <source_id_slug>/
│           ├── raw/
│           └── normalized/
├── translations/
│   ├── en/
│   │   └── <source_id_slug>/
│   │       ├── raw/
│   │       └── normalized/
│   └── zh-Hans/
│       └── <source_id_slug>/
│           ├── raw/
│           ├── normalized/
│           └── reference-only/
├── metadata/
│   ├── SOURCE_RECORD.yaml
│   ├── records/
│   │   └── <file_id_slug>.source.yaml
│   ├── sources.yaml
│   ├── resources.yaml
│   ├── rights.yaml
│   ├── checksums/
│   │   └── checksums.sha256
│   ├── indexes/
│   │   └── passages.jsonl
│   ├── alignments/
│   │   └── alignments.jsonl
│   ├── logs/
│   │   ├── acquisition_log.jsonl
│   │   └── normalization_log.jsonl
│   └── quality/
│       ├── source_quality_report.md
│       └── gate_s1b.yaml
└── references/
    ├── textual_reference/
    │   └── <resource_id_slug>/
    │       ├── raw/
    │       └── normalized/
    ├── historical_context/
    │   └── <resource_id_slug>/
    │       ├── raw/
    │       └── normalized/
    └── discovery_only/
        └── <resource_id_slug>/
            └── reference-only/
```

### 3.2 目录不变量

1. `raw/` 只保存从提供方取得的原始字节，不在原文件上清洗、改码或修订。
2. `normalized/` 只保存由一个或多个 `raw/` 文件派生的工作副本；每个副本必须记录全部上游文件和转换过程。
3. `reference-only/` 只保存书目信息、访问说明或本地挂载说明，不保存未获准进入仓库的正文。
4. `metadata/` 不保存原文、译文或长篇参考资料正文。
5. `original_text/` 与 `translations/` 必须按语言和 `source_id` 隔离，不能把不同版本混在同一目录。
6. `references/` 必须按 `textual_reference`、`historical_context`、`discovery_only` 分权；参考资料不得伪装成原作文本。
7. 每个本地、含字节的来源文件必须在 `metadata/records/` 中有且只有一个对应记录。
8. 一个文件发生任何字节变化后，必须生成新校验值；不得保留旧 `checksum` 冒充同一文件。

### 3.3 可执行的目录契约

后续目录初始化器和验收器应按以下契约工作：

```yaml
schema_version: c2d.source-package-structure.v1
logical_root: source/
required_top_level_directories:
  - original_text
  - translations
  - metadata
  - references
allowed_root_files:
  - README.md
  - SOURCE_MANIFEST.md
record_template: metadata/SOURCE_RECORD.yaml
record_directory: metadata/records/
checksum_index: metadata/checksums/checksums.sha256
raw_policy: immutable
normalized_policy: derived_and_traceable
reference_only_policy: metadata_without_source_body
```

`SOURCE_MANIFEST.md` 可以保留在 `source/` 根目录，也可以由项目文档目录链接到此处；若保留在根目录，它属于规范文档，不属于来源正文。

## 4. 各类文件说明

### 4.1 原作语言文本：`original_text/`

| 文件类别 | 用途 | 推荐格式 | 存放位置 | 关键规则 |
| --- | --- | --- | --- | --- |
| 原始数字文本 | 保存提供方发布的原作语言文件 | 保持上游原格式；优先 TEI/EpiDoc XML、XML、TXT | `original_text/<lang>/<source>/raw/` | 字节不可变；记录获取 URL 与 SHA-256 |
| 原始扫描或页面影像 | 复核数字文本或版本页面 | PDF、TIFF、PNG、JPEG | `references/textual_reference/<resource>/raw/` | 作为版本见证，不作为机器正文的默认入口 |
| 规范化工作文本 | 供后续切分、索引和对齐使用 | UTF-8、Unicode NFC 的 TXT、XML 或 JSONL | `original_text/<lang>/<source>/normalized/` | 必须链接到原始文件及规范化日志 |

《奥德赛》的规范原文语言目录使用 `grc/`。这里的 `grc` 是语言代码，不代表具体版本；具体版本必须继续由 `source_id` 子目录区分。

### 4.2 译本：`translations/`

| 文件类别 | 用途 | 推荐格式 | 存放位置 | 关键规则 |
| --- | --- | --- | --- | --- |
| 公开译本原始文件 | 保存合法取得的译本原始字节 | 保持上游原格式；常见为 TEI XML、TXT、EPUB | `translations/<lang>/<source>/raw/` | 不用译本文件行号冒充规范行号 |
| 规范化译本文本 | 供对齐与后续封闭输入包使用 | UTF-8、Unicode NFC 的 TXT、XML 或 JSONL | `translations/<lang>/<source>/normalized/` | 必须保留版本原生定位和派生关系 |
| 受限辅助译本说明 | 登记纸本、个人本地文件或不可再分发译本的使用方式 | YAML 或 Markdown | `translations/<lang>/<source>/reference-only/` | 只存元数据、页码规则和挂载约定，不存正文 |

语言目录使用 BCP 47 或 ISO 639 兼容标记，例如 `en/`、`grc/`、`zh-Hans/`。不得使用 `english/`、`chinese/`、`中文/` 等并行别名。

### 4.3 元数据：`metadata/`

| 文件 | 用途 | 推荐格式 | 命名要求 |
| --- | --- | --- | --- |
| `SOURCE_RECORD.yaml` | 单文件记录模板和字段规范入口 | YAML 1.2 | 固定文件名；它是模板，不是某个实际来源记录 |
| `records/*.source.yaml` | 每个本地来源文件的独立记录 | YAML 1.2 | 文件名由 `file_id_slug` 生成 |
| `sources.yaml` | 汇总来源版本、角色和状态 | YAML 1.2 | `source_id` 为主键 |
| `resources.yaml` | 汇总参考资源，包括没有本地文件的 link-only 项 | YAML 1.2 | `resource_id` 为主键 |
| `rights.yaml` | 分别记录作品、版本、译文、数字编码和影像权利 | YAML 1.2 | 不用单一站点许可覆盖所有权利对象 |
| `checksums.sha256` | 批量验证本地来源文件字节身份 | GNU SHA-256 清单格式 | 每行一个摘要和相对路径 |
| `passages.jsonl` | 后续存放可引用片段索引 | UTF-8 JSON Lines | 一行一个 `SourcePassage`；Phase 1-B 不生成内容 |
| `alignments.jsonl` | 后续存放跨版本对齐 | UTF-8 JSON Lines | 一行一个 alignment；Phase 1-B 不执行对齐 |
| `acquisition_log.jsonl` | 记录获取动作、结果和失败原因 | UTF-8 JSON Lines | 只追加，不回写历史行 |
| `normalization_log.jsonl` | 记录 raw 到 normalized 的转换 | UTF-8 JSON Lines | 只追加；必须标出输入和输出校验值 |
| `source_quality_report.md` | 人工可读的完整性与缺陷报告 | Markdown | 不夹带剧情或人物分析 |
| `gate_s1b.yaml` | 保存 Phase 1-B 验收结果和批准状态 | YAML 1.2 | 状态只能按第 8 节状态机更新 |

YAML 与 JSONL 文件统一使用 UTF-8、LF 换行和两空格缩进；YAML 禁止 Tab。时间使用带时区的 ISO 8601 格式。

### 4.4 参考资料：`references/`

| 子目录 | 用途 | 推荐格式 | 边界 |
| --- | --- | --- | --- |
| `textual_reference/` | 词典、校勘、注释、抄本或版本见证 | 原始 PDF/XML/JSON/图像；规范化 TXT/JSONL | 用于解释或复核，不能取代规范原文坐标 |
| `historical_context/` | 历史、考古、地理、物质文化与口头传统资料 | PDF、HTML 快照、CSV、GeoJSON、JSON | 只能支持背景结论，不能反向生成原作事实 |
| `discovery_only/` | 搜索入口、目录页和线索集合 | YAML 或 Markdown 链接记录 | 默认 link-only；正式结论必须回查更高等级来源 |

没有下载到本地的 link-only 资源登记在 `metadata/resources.yaml`，不创建虚假的本地文件记录，也不填写虚假的 `checksum`。

## 5. 命名规范

### 5.1 `source_id` 与 `resource_id`

- `source_id` 延续 `SOURCE_MANIFEST.md` 中的稳定大写身份，例如 `ODY-GRC-MURRAY1919`。
- `resource_id` 用于参考资源，例如 `CTX-ARCH-DARTMOUTH`。
- `resource_id` 表示一个背景或文本学资源条目；该资源若产生本地文件，还必须为具体文件版本建立可登记的 `source_id`，并在文件记录的 `context_resource_id` 中链接原 `resource_id`。
- 已发布 ID 不因目录移动、文件重命名或 URL 更新而改变。
- 不同版本、译者、数字编码或实质内容不同的文件不得共用同一个来源身份。
- 不得直接把 `resource_id` 填入 `SOURCE_RECORD.yaml` 的 `source_id` 字段；两者通过显式字段关联，避免参考资源与文本底本身份混权。

### 5.2 目录 slug

路径中的 `<source_id_slug>` 或 `<resource_id_slug>` 由相应 ID 转为小写，保留连字符：

```text
ODY-GRC-MURRAY1919  -> ody-grc-murray1919
CTX-ARCH-DARTMOUTH  -> ctx-arch-dartmouth
```

slug 只用于路径；YAML 内仍保存原始大写 ID。

### 5.3 来源文件名

来源文件采用以下语法：

```text
<source-slug>__<state>__<unit>[__<revision>].<ext>
```

字段规则：

| 字段 | 允许值或格式 | 示例 |
| --- | --- | --- |
| `source-slug` | 小写 `source_id` slug | `ody-grc-murray1919` |
| `state` | `raw`、`normalized`、`scan`、`reference` | `raw` |
| `unit` | `full`、`vol01`、`vol02`、`b01` 等明确单元 | `vol01` |
| `revision` | 仅在确有版本依据时使用 `r001`、日期或上游短提交号 | `r001` |
| `ext` | 与实际媒体类型一致的小写扩展名 | `xml` |

语法示例只说明命名，不表示文件已存在：

```text
ody-grc-murray1919__raw__vol01.xml
ody-grc-murray1919__normalized__full.txt
ody-eng-murray1919__raw__full.xml
ody-eng-butler-pg1727__raw__full.txt
```

禁止使用空格、中文标点、`latest`、`final`、`new`、`copy`、`最终版` 或操作系统自动追加的 `(1)` 作为版本信息。

### 5.4 文件记录名

每个实际来源文件拥有一个稳定 `file_id`，建议格式：

```text
<SOURCE_ID>-<STATE>-<UNIT>-<ARTIFACT>[-<REVISION>]
```

`ARTIFACT` 用于区分同一来源、状态和单元下的不同物理资产，例如 `TEI`、`TXT`、`ZIP`、`PDF` 或提供方资产号。若格式仍不能唯一标识文件，使用稳定的提供方资产号或 `ASSET01`、`ASSET02`；不得依赖扩展名之外的隐式差异。

对应记录文件名使用小写 slug：

```text
metadata/records/<file_id_slug>.source.yaml
```

例如：

```text
file_id: ODY-GRC-MURRAY1919-RAW-VOL01-TEI
record: metadata/records/ody-grc-murray1919-raw-vol01-tei.source.yaml
```

`source_id` 表示书目和版本身份，`file_id` 表示该身份下的某个物理文件；二者不得混用。

## 6. `SOURCE_RECORD.yaml` 规范

### 6.1 适用对象

`SOURCE_RECORD.yaml` 是“一个本地来源文件对应一条记录”的模板。以下文件必须建立记录：

- `original_text/` 中的每个 raw 和 normalized 文件；
- `translations/` 中的每个 raw 和 normalized 文件；
- `references/` 中实际保存到本地的每个资料文件；
- 页面扫描、PDF、图片、EPUB、XML、TXT、JSON 等任何含来源字节的文件。

目录、README、link-only 条目、来源清单和日志本身不按来源文件登记。

### 6.2 九个必填字段

每条已验收记录必须包含以下九个顶层字段，且值不得为 `null` 或空字符串：

| 字段 | 类型 | 含义 | 验证规则 |
| --- | --- | --- | --- |
| `source_id` | string | 来源的稳定书目/版本身份 | 匹配 `^[A-Z0-9]+(?:-[A-Z0-9]+)*$`；必须存在于 `sources.yaml` |
| `title` | string | 该来源的正式题名 | 非空；不得写成本地临时文件名 |
| `author` | string | 作品作者或该参考资料作者 | 非空；传统归属或未知状态应明确写出，不能静默留空 |
| `edition` | string | 能区分该文件所属版本的版本说明 | 非空；禁止只写 `latest` |
| `language` | string | 文件正文的语言 | 使用 BCP 47/ISO 639 兼容值，如 `grc`、`en`、`zh-Hans` |
| `provider` | string | 实际提供该文件的机构或平台 | 非空；不得只填模糊的 `internet` |
| `url` | string | 来源页面或该文件的规范获取地址 | 使用绝对 `https://` URL；记录后续跳转前的规范入口 |
| `license` | string | 对该具体文件可确认的许可状态 | 优先 SPDX 标识；不能确认时使用 `NOASSERTION` 或项目定义的 `LicenseRef-*` |
| `checksum` | string | 当前文件原始字节的 SHA-256 身份 | 格式必须为 `sha256:` 加 64 位小写十六进制摘要 |

`author` 记录作品或资料的作者。译者、编辑、编校者、数字编码者等职责放在可选的 `contributors` 字段中，不能挤入 `author` 后形成不可解析的混合字符串。

### 6.3 推荐完整模板

以下是 `metadata/SOURCE_RECORD.yaml` 的规范模板；尖括号为待实体化时填写的变量，不是一条已通过验收的真实记录：

```yaml
schema_version: c2d.source-record.v1

source_id: "<STABLE-SOURCE-ID>"
title: "<formal title>"
author: "<author or explicit attribution status>"
edition: "<edition statement>"
language: "<BCP47-or-ISO639-code>"
provider: "<provider name>"
url: "https://<canonical-source-or-file-url>"
license: "<SPDX-ID|NOASSERTION|LicenseRef-...>"
checksum: "sha256:<64-lowercase-hex-digits>"

file_id: "<UNIQUE-FILE-ID>"
file_path: "<path-relative-to-source-root>"
media_type: "<IANA-media-type>"
bytes: 0
role: "<canonical_anchor|primary_working_text|aux_translation|textual_reference|historical_context|discovery_only>"
state: "<raw|normalized|scan|reference>"
retrieved_at: "<ISO-8601 timestamp with timezone>"
context_resource_id: null

contributors:
  translator: null
  editor: null
  encoder: null

provider_identity:
  upstream_commit: null
  external_id: null

derivation:
  inputs: []
  transformation_log_ref: null

rights_note: null
known_issues: []
record_status: draft
```

九个指定字段是最低契约；其余字段用于把物理文件、来源角色和派生链闭合。实际记录进入 `approved` 前：

- `file_id` 必须全包唯一；
- `file_path` 必须是从 `source/` 根开始的相对路径，禁止绝对路径和 `..`；
- `media_type` 必须与文件内容及扩展名一致；
- `bytes` 必须大于 0，并等于实际文件大小；
- 文件位于 `references/` 时，`context_resource_id` 必须存在于 `resources.yaml`；
- `state: normalized` 时，`derivation.inputs` 必须包含一项或多项上游文件身份，`transformation_log_ref` 不得为空；
- `derivation.inputs` 的每一项必须采用 `{file_id, checksum}` 结构，并与对应上游记录完全一致；
- `record_status` 必须经过 `draft -> verified -> approved`，不得跳级。

单输入和多输入派生统一使用同一结构：

```yaml
derivation:
  inputs:
    - file_id: "<UPSTREAM-FILE-ID-1>"
      checksum: "sha256:<64-lowercase-hex-digits>"
    - file_id: "<UPSTREAM-FILE-ID-2>"
      checksum: "sha256:<64-lowercase-hex-digits>"
  transformation_log_ref: "metadata/logs/normalization_log.jsonl#<event-id>"
```

### 6.4 `checksum` 规则

1. 算法固定为 SHA-256；Phase 1-B 不允许用 MD5、文件时间或文件名代替。
2. 摘要基于实际保存的原始字节计算，不先统一换行、不解压、不重新编码。
3. raw 和 normalized 即使肉眼内容相同，也分别计算和登记摘要。
4. 文件字节变化时生成新记录版本和新摘要；不得静默覆盖已批准记录。
5. `metadata/checksums/checksums.sha256` 是从各记录派生的批量校验视图，格式为：

```text
<64-lowercase-hex-digits>  <relative-file-path>
```

6. YAML 中的 `checksum` 与清单中的摘要不一致时，验收失败。

### 6.5 一对一关系

```text
一个本地来源文件
    -> 一个唯一 file_id
    -> 一个 metadata/records/*.source.yaml
    -> 一个 SHA-256 条目
```

同一 `source_id` 可以有多个物理文件，例如两个册次、原始文件与规范化副本；每个文件仍需独立 `file_id`、记录和校验值。

## 7. 来源文件生命周期

### 7.1 获取

未来获取来源文件时，只允许写入对应 `raw/` 目录，并同时创建 draft 记录。获取失败只写日志，不创建零字节占位文件和伪造校验值。

### 7.2 验证

验证器检查文件存在、大小、媒体类型、必填字段、URL、许可状态和 SHA-256。全部通过后，单文件 `record_status` 才能从 `draft` 进入 `verified`。

### 7.3 规范化

规范化只产生新文件，不修改 raw。新文件沿用正确的 `source_id`，获得自己的 `file_id` 和 `checksum`，并通过 `derivation.inputs` 回到一项或多项明确上游文件；合并多卷、拼接多个 TEI 或其他多输入转换不得压缩成虚假的单一来源。

### 7.4 批准

人工确认来源身份、版本和许可记录后，文件记录才可进入 `approved`。只有 `approved` 来源文件才可在未来进入正式 AI 输入包。

本节只定义生命周期，不在 Phase 1-B 实际执行获取、规范化、对齐或内容检查。

## 8. Source Package 验收标准

### 8.1 Phase 1-B 的完成含义

Phase 1-B 是“目录与记录契约锁定”，不是“来源文本已就绪”。本阶段可以在没有任何来源正文文件的情况下完成；下载、字节校验、24 卷完整性检查、文本规范化和对齐属于后续实体导入及 Gate S1 工作。

### 8.2 Gate S1-B：结构规范就绪

只有以下项目同时通过，Phase 1-B 才可标记为 `completed`：

- [ ] `01_SOURCE_PACKAGE_STRUCTURE.md` 已存在并标明规范版本；
- [ ] `source/` 的逻辑根及其与仓库实际路径的映射唯一、无二义性；
- [ ] `original_text/`、`translations/`、`metadata/`、`references/` 四个顶层目录已被锁定；
- [ ] raw、normalized、reference-only 三类生命周期边界已定义；
- [ ] 每类文件的用途、推荐格式、存放位置和命名规则已定义；
- [ ] `source_id`、`resource_id`、`file_id` 三种身份的职责互不混用；
- [ ] `SOURCE_RECORD.yaml` 的九个必填字段、类型和验证规则已定义；
- [ ] 一个本地来源文件到记录、`file_id` 和 SHA-256 的一对一关系已定义；
- [ ] 受限译本和 link-only 资源的登记方式已定义，且不要求保存正文；
- [ ] raw 不可变、normalized 可追溯、校验值不可伪造三项规则已成为硬约束；
- [ ] 本规范与 `SOURCE_MANIFEST.md` 的来源角色、定位权限和阶段边界一致；
- [ ] 人工评审者将 `metadata/quality/gate_s1b.yaml` 状态批准为 `approved`。

### 8.3 Gate 状态机

```yaml
gate_id: S1-B
phase: source_package_structure
allowed_statuses:
  - draft
  - ready_for_review
  - changes_requested
  - approved
completion_rule: status == approved
```

当前本文档状态为 `ready_for_review`。在获得人工批准前，不得对外声称 Gate S1-B 已通过。

### 8.4 阻断条件

出现任意一项时，Gate S1-B 必须失败或返回 `changes_requested`：

- 四个顶层资料域缺失、重名或职责重叠；
- raw 与 normalized 文件允许原地覆盖；
- 一个本地来源文件可以没有记录或没有 SHA-256；
- `source_id` 同时承担物理文件身份，导致多册或派生文件冲突；
- 不同版本、译本或数字编码被合并进同一个来源身份；
- link-only 资源被要求填写不存在的本地校验值；
- 受限参考译本正文被默认纳入仓库；
- 目录规范要求执行剧情、人物或改编分析；
- 本规范与 `SOURCE_MANIFEST.md` 的 L0 权限规则不一致且未记录修订。

### 8.5 本阶段不要求完成的事项

以下事项不属于 Phase 1-B 验收前置条件：

- 下载 Murray 古希腊文、Murray 英译或任何其他文本；
- 创建真实的来源文件 SHA-256；
- 校验《奥德赛》24 卷及行号连续性；
- 切分 `passages.jsonl`；
- 建立 `alignments.jsonl`；
- 划分来源场景；
- 生成剧情事件、人物记录或改编决策；
- 生成任何短剧剧本、镜头或视频资产。

这些工作必须在本结构规范获批后，按后续独立阶段执行。

## 9. 与 Phase 1 / Gate S1 的关系

Gate S1-B 只确认“容器和记录规则已经确定”；`03_WORKFLOW.md` 与 `SOURCE_MANIFEST.md` 中的 Gate S1 仍需确认真实来源文件完整、可定位、可回溯并经负责人批准。

两者关系如下：

```text
Gate S1-B：目录与记录规范 approved
    -> 后续来源实体导入、校验与规范化
    -> Gate S1：真实 Source Package approved
    -> 才允许进入剧情、事件或人物分析
```

任何 Gate S1-B 的通过都不能替代 Gate S1，也不能被解释为来源文本、译本或参考资料已经下载和验证。

## 10. 当前结论

本文件已经把 Phase 1 的来源选择方案转换为一套可实施、可校验的 Source Package 目录与记录契约。当前没有下载任何文本，没有生成任何真实来源记录或校验值，也没有进行内容分析、人物建库或短剧改编。
