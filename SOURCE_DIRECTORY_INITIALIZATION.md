# 《奥德赛》Source Package 目录初始化规范

> 项目：Classic-to-Drama Engine  
> 阶段：Phase 1-E / P0-2  
> 日期：2026-08-10  
> 文档状态：`ready_for_review`  
> 执行状态：`not_initialized`  
> 边界：本文只定义目录契约，不创建 `source/`、来源文件、占位文件、校验值或内容数据库。

## 1. 文档目的与适用范围

本文将已批准的 Source Package 结构收敛为后续可执行的目录初始化规范，回答以下问题：

1. `source/` 最终包含哪些目录；
2. raw、normalized、reference-only 与 metadata 分别放在哪里；
3. 目录、来源文件和登记记录如何命名；
4. 哪些分析与创作产物不得进入 Source Package；
5. 何时可以认定 Phase 1-E / P0-2 的“目录设计”完成。

本阶段不代表 Source Package 已实体化，也不代表任何来源已经获取或验证。本文中的目录树、文件槽位和示例路径都是规范，不是文件存在声明。

## 2. 逻辑根与初始化边界

### 2.1 唯一逻辑根

本文统一使用：

```text
source/
```

作为单部作品的 Source Package 逻辑根。若仓库最终沿用 `projects/odyssey/sources/`，则该路径直接等价于 `source/`；不得再嵌套为：

```text
source/source/
sources/source/
source/sources/
```

一个项目必须在真正初始化前锁定唯一物理根，并在项目配置或 README 中记录这一映射。

### 2.2 P0-2 允许与不允许的动作

本阶段唯一允许创建的成果是本文档 `SOURCE_DIRECTORY_INITIALIZATION.md`。

本阶段不执行以下文件系统动作：

- 不创建 `source/` 或其任何子目录；
- 不复制或移动 `SOURCE_RECORD_TEMPLATE.yaml`；
- 不创建 `.gitkeep`、空白 XML、空白 YAML、空白 JSONL 或零字节占位文件；
- 不创建 `checksums.sha256`，也不填写任何 checksum；
- 不改变 `P0_SOURCE_REGISTRY.md` 中的 `pending` 状态；
- 不下载、打开、切分、规范化或分析《奥德赛》来源文本。

## 3. `source/` 最终目录结构

### 3.1 目录契约

尖括号表示后续实体化时替换的变量；所有行均表示目录，不表示目录现在已经存在。

```text
source/
├── original_text/
│   └── <language>/
│       └── <source_id_slug>/
│           ├── raw/
│           └── normalized/
├── translations/
│   └── <language>/
│       └── <source_id_slug>/
│           ├── raw/
│           ├── normalized/
│           └── reference-only/
├── metadata/
│   ├── records/
│   ├── checksums/
│   ├── indexes/
│   ├── alignments/
│   ├── logs/
│   └── quality/
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

四个一级目录 `original_text/`、`translations/`、`metadata/`、`references/` 是固定契约。不得用 `texts/`、`docs/`、`data/` 等并行目录承载同类来源资产。

### 3.2 《奥德赛》P0 具体目录映射

P0-1 已登记四个待获取物理文件。未来执行初始化时，它们只允许落入以下目录；本阶段不创建这些目录或文件：

```text
source/
├── original_text/
│   └── grc/
│       └── ody-grc-murray1919/
│           ├── raw/
│           └── normalized/
├── translations/
│   └── en/
│       └── ody-eng-murray1919/
│           ├── raw/
│           └── normalized/
├── metadata/
│   ├── records/
│   ├── checksums/
│   ├── indexes/
│   ├── alignments/
│   ├── logs/
│   └── quality/
└── references/
    └── textual_reference/
        └── ref-ody-perseus-tei/
            ├── raw/
            └── normalized/
```

目录与 P0 登记对象的映射如下：

| P0 类别 | `source_id` | 未来 raw 目录 | 说明 |
| --- | --- | --- | --- |
| Perseus Greek Text | `ODY-GRC-MURRAY1919` | `source/original_text/grc/ody-grc-murray1919/raw/` | 希腊文原始 TEI 的唯一 P0 落点 |
| Perseus English Translation | `ODY-ENG-MURRAY1919` | `source/translations/en/ody-eng-murray1919/raw/` | 英文工作译本原始 TEI 的唯一 P0 落点 |
| Required Metadata | `ODY-META-PERSEUS-CTS` | `source/references/textual_reference/ref-ody-perseus-tei/raw/` | textgroup 与 work 两个 CTS XML 分别作为独立物理文件登记 |

`ODY-META-PERSEUS-CTS` 是提供方的共享 CTS 字节资产，因此进入 `references/textual_reference/.../raw/`；它不应被误放到 `source/metadata/records/`。后者只保存本项目对来源文件建立的登记记录。

## 4. 各目录用途说明

### 4.1 `original_text/`

用于保存原作语言版本，不保存译本、研究笔记或改编产物。

| 位置 | 用途 | 规则 |
| --- | --- | --- |
| `original_text/<language>/<source_id_slug>/raw/` | 保存从提供方取得的原始文本字节 | 保持原格式和原始字节；不得就地清洗、改码、修订或覆盖 |
| `original_text/<language>/<source_id_slug>/normalized/` | 保存由一个或多个 raw 文件派生的规范化工作副本 | 必须有独立 `file_id`、来源记录和可追溯的转换链；不得覆盖 raw |

《奥德赛》原文语言目录固定使用 `grc/`。语言目录只表达语言，具体版本由下一层 `source_id_slug` 区分。

### 4.2 `translations/`

用于保存不同语言译本及其受控说明，不保存原作希腊文或背景资料。

| 位置 | 用途 | 规则 |
| --- | --- | --- |
| `translations/<language>/<source_id_slug>/raw/` | 保存合法取得的译本原始字节 | 保持提供方格式和原始定位结构 |
| `translations/<language>/<source_id_slug>/normalized/` | 保存译本规范化工作副本 | 必须回溯到明确 raw 输入；译本原生定位不得冒充希腊文 Book/Line 坐标 |
| `translations/<language>/<source_id_slug>/reference-only/` | 保存纸本、受限版本或不可入库译本的书目、访问与挂载说明 | 只允许元数据和使用说明；不得放入译文正文或伪造本地来源文件 |

英文使用 `en/`，简体中文使用 `zh-Hans/`。不得同时建立 `english/`、`chinese/`、`中文/` 等别名目录。

### 4.3 `metadata/`

用于保存 Source Package 自身的身份、权利、验证、日志与质量信息；这里的 metadata 是“项目登记层”，不是上游 CTS 元数据字节的通用收纳箱。

| 位置 | 未来用途 | 允许内容 |
| --- | --- | --- |
| `metadata/records/` | 每个本地来源文件的一对一 `SOURCE_RECORD` | `<file_id_slug>.source.yaml` |
| `metadata/checksums/` | 批量校验视图 | 经实际获取后生成的 `checksums.sha256`；P0-2 不创建 |
| `metadata/indexes/` | 后续来源片段索引 | 仅来源定位数据；不得包含剧情分析 |
| `metadata/alignments/` | 后续跨版本定位映射 | 仅文本对齐关系；不得包含改编决策 |
| `metadata/logs/` | 获取与规范化事件日志 | 只追加的机器可读日志 |
| `metadata/quality/` | 来源质量报告与 Gate 状态 | 完整性、格式、编码、定位和来源身份检查结果 |

未来 Source Package 根下还可按既有结构规范设置 `metadata/SOURCE_RECORD.yaml`、`metadata/sources.yaml`、`metadata/resources.yaml` 与 `metadata/rights.yaml`。其中：

- 当前项目级 `SOURCE_RECORD_TEMPLATE.yaml` 是 P0-1 的准备模板；
- 只有后续另行授权物理初始化时，才可将获批模板映射或复制为 `source/metadata/SOURCE_RECORD.yaml`；
- 模板本身不是具体来源记录，不对应 `file_id`，也不填写 checksum；
- link-only 与 reference-only 条目没有本地来源字节时，不创建虚假 `metadata/records/*.source.yaml`。

### 4.4 `references/`

用于保存文本学见证、历史背景资料和发现型入口；参考资料不得取得原作主文本或工作译本的身份。

| 位置 | 用途 | 规则 |
| --- | --- | --- |
| `references/textual_reference/<resource_id_slug>/raw/` | 保存 CTS 身份文件、扫描、校勘或其他文本学参考原始字节 | 每个本地文件独立登记；不得伪装为规范原文 |
| `references/textual_reference/<resource_id_slug>/normalized/` | 保存可追溯的文本学参考派生文件 | 必须链接具体 raw 输入 |
| `references/historical_context/<resource_id_slug>/raw/` | 保存合法取得的历史、地理、考古等原始资料 | 只支持背景研究，不反向定义原作事实 |
| `references/historical_context/<resource_id_slug>/normalized/` | 保存背景资料的结构化派生副本 | 必须保留来源和转换记录 |
| `references/discovery_only/<resource_id_slug>/reference-only/` | 保存搜索入口或目录页的说明 | 默认 link-only；不保存被链接网站的正文副本 |

纯 link-only 入口统一登记在未来的 `source/metadata/resources.yaml`，无需为其创建空目录、占位文件、`file_id` 或 checksum。

## 5. 文件与目录命名规则

### 5.1 固定目录名

- 一级目录固定为 `original_text`、`translations`、`metadata`、`references`；
- 生命周期目录固定为 `raw`、`normalized`、`reference-only`；
- 参考资料分类固定为 `textual_reference`、`historical_context`、`discovery_only`；
- 固定目录名全部使用小写 ASCII；下划线与连字符按上述契约使用，不得混写。

### 5.2 语言目录

使用 BCP 47 或 ISO 639 兼容标记，并保持大小写规范，例如：

```text
grc/
en/
zh-Hans/
```

同一语言不得存在两个别名目录。

### 5.3 来源与资源目录 slug

`source_id` 或 `resource_id` 转换为目录 slug 时：

1. 转为小写；
2. 保留连字符；
3. 不添加空格、中文字符或主观版本词；
4. YAML 登记中仍保留原始大写 ID。

```text
ODY-GRC-MURRAY1919  -> ody-grc-murray1919/
REF-ODY-PERSEUS-TEI -> ref-ody-perseus-tei/
```

### 5.4 来源文件名

未来来源文件统一使用：

```text
<source-slug>__<state>__<unit>[__<revision>].<ext>
```

字段约束：

- `state`：`raw`、`normalized`、`scan` 或 `reference`；
- `unit`：`full`、`vol01`、`vol02`、`b01` 等明确物理或逻辑单元；
- `revision`：仅在有上游版本、提交或正式修订依据时使用；
- `ext`：与真实媒体类型一致，使用小写扩展名。

以下仅为已登记的未来目标名，不表示文件存在：

```text
ody-grc-murray1919__raw__full.xml
ody-eng-murray1919__raw__full.xml
ody-meta-perseus-cts__raw__textgroup.xml
ody-meta-perseus-cts__raw__work.xml
```

禁止使用 `latest`、`final`、`new`、`copy`、`最终版`、空格、中文标点或系统自动追加的 `(1)` 作为版本身份。

### 5.5 登记记录名

每个实际含字节文件未来必须拥有唯一 `file_id`；其项目登记记录使用：

```text
source/metadata/records/<file_id_slug>.source.yaml
```

`file_id_slug` 是 `file_id` 的小写连字符形式。一个 `source_id` 可以对应多个物理文件，但每个物理文件必须拥有独立 `file_id` 和独立记录。P0-2 不创建这些记录。

## 6. Source 层禁止事项

`source/` 只保存来源字节、来源派生副本和来源工程元数据。以下内容禁止存放在 `source/` 的任何位置，包括 `metadata/`、`references/` 和 `normalized/`：

- 人物分析、人物关系、人物小传或人物数据库；
- 剧情梗概、情节分析、事件链、主题分析或剧情数据库；
- 改编策略、现代化方案、情节增删合并决定或分集规划；
- 剧本、场景稿、对白、旁白、分镜、镜头表或拍摄脚本；
- 视频、配音、角色图、场景图或其他制作资产；
- 模型生成但没有明确来源身份的“补全文本”；
- 未取得的来源正文、零字节占位文件或伪造的来源记录；
- 没有真实文件字节支持的 checksum；
- 临时下载残片、缓存、编辑器交换文件或个人研究便笺。

上述内容必须在后续阶段进入 `analysis/`、`adaptation/`、`scripts/`、`production/` 等 Source Package 之外的项目域；具体目录由相应阶段另行定义。

## 7. Phase 1-E / P0-2 完成标准

### 7.1 完成含义

Phase 1-E / P0-2 完成仅表示 **Source Directory Initialization Specification Ready**：目录设计、用途边界、命名规则和禁止事项已经形成可评审的书面契约。

它不表示：

- `source/` 已经物理创建；
- P0 文件已下载、存在、登记或验证；
- `SOURCE_RECORD_TEMPLATE.yaml` 已复制到 Source Package；
- checksum 已生成；
- normalized 文件、索引或对齐数据已经生成；
- Gate S1-C、Gate S1-D 或总 Gate S1 已通过。

### 7.2 验收条件

只有以下条件全部满足，P0-2 才可标记为 `completed`：

- [ ] `source/` 的逻辑根及物理根映射规则唯一、无重复嵌套；
- [ ] 四个固定一级目录已完整定义；
- [ ] raw、normalized、reference-only 和项目 metadata 的位置与职责均已定义；
- [ ] P0 Greek、English 与两个 CTS metadata 文件的未来目录落点与 `P0_SOURCE_REGISTRY.md` 一致；
- [ ] 固定目录、语言目录、ID slug、来源文件和记录文件命名规则均已定义；
- [ ] Source 层禁止存放的人物、剧情、改编和剧本产物已明确列出；
- [ ] 本轮没有创建 `source/`、来源字节、占位文件或 checksum；
- [ ] `P0_SOURCE_REGISTRY.md` 的四项获取状态与四项验证状态仍全部为 `pending`；
- [ ] 人工评审者批准本规范，并将 P0-2 状态从 `ready_for_review` 更新为 `completed`。

### 7.3 阻断条件

出现任一情况时，P0-2 不得通过：

- 缺少四个固定一级目录之一；
- `raw/` 与 `normalized/` 混放，或允许修改 raw 原始字节；
- 把 reference-only 条目当成本地正文文件；
- 把上游 CTS XML 与项目来源登记记录混为同一类 metadata；
- P0 目录落点与 `P0_SOURCE_REGISTRY.md` 不一致；
- 允许人物、剧情、改编或剧本文件进入 `source/`；
- 创建了任何未获授权的来源文件、占位文件或 checksum；
- 在没有实际获取与验证证据时把任一 P0 状态改为非 `pending`。

## 8. 当前状态

| 项目 | 当前值 |
| --- | --- |
| 目录规范文档 | `created` |
| 规范评审状态 | `ready_for_review` |
| `source/` 物理目录 | `not_initialized` |
| 来源文本资产 | `0` |
| normalized 资产 | `0` |
| 新增 checksum | `0` |
| 内容分析或改编产物 | `0` |

下一步只能是人工评审本规范。目录或来源资产的真实创建必须由后续独立阶段明确授权。
