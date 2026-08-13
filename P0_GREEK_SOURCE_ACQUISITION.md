# 《奥德赛》P0 Greek TEI 单来源获取计划

> 项目：Classic-to-Drama Engine  
> 阶段：Phase 1-E / P0-3-A  
> 对象：Perseus Greek TEI  
> 日期：2026-08-10  
> 文档状态：`ready_for_review`  
> 执行状态：`pending`  
> 获取状态：`pending`  
> 验证状态：`pending`

## 1. 文档目的与边界

本文只确认第一个 P0 真实来源——Perseus Greek TEI——的来源身份、未来保存路径、登记流程和单文件验收条件。本文是单个来源的获取计划，不表示获取动作已经开始。

本文继承以下已批准或待批准的资料工程契约：

1. `SOURCE_MANIFEST.md`：来源身份、`canonical_anchor` 权限和 `book.line` 定位规则；
2. `01_SOURCE_PACKAGE_STRUCTURE.md`：目录、`file_id`、单文件记录和 SHA-256 契约；
3. `02_SOURCE_ACQUISITION_PLAN.md`：固定上游 commit、实际获取 URL 和检查规则；
4. `03_SOURCE_ACQUISITION_EXECUTION_CHECKLIST.md`：P0 顺序、目标路径和状态词表；
5. `SOURCE_RECORD_TEMPLATE.yaml`：13 个统一登记字段；
6. `P0_SOURCE_REGISTRY.md`：当前 P0 文件登记与 `pending` 状态；
7. `SOURCE_DIRECTORY_INITIALIZATION.md`：`source/` 最终目录和 `grc/` 语言目录规范。

本阶段只允许创建本文档。明确不执行：

- 下载、克隆、复制、缓存或保存 Greek TEI 字节；
- 解析、抽取、清洗、规范化、切分或索引文本；
- 创建 `source/` 目录、空文件、临时文件或占位文件；
- 解析或填写上游 commit SHA、文件大小、获取时间或 checksum；
- 修改 `P0_SOURCE_REGISTRY.md` 中任何 `pending` 状态；
- 分析剧情、人物、场景或文学内容；
- 创建人物数据库、剧情数据库、改编方案或剧本。

如本文与上游资料工程文档出现未解决冲突，未来执行状态必须改为 `blocked_spec_conflict`，不得在获取现场自行选择另一版本或路径。

## 2. Greek TEI 来源确认

### 2.1 规范来源身份

| 字段 | 确认值 |
| --- | --- |
| `source_id` | `ODY-GRC-MURRAY1919` |
| `file_id` | `ODY-GRC-MURRAY1919-RAW-FULL-TEI` |
| title | *Ὀδύσσεια*（Greek edition）；书目说明为 *The Odyssey, Volumes 1–2* |
| author | Homer（传统归属；实际登记时按项目统一作者表述填写） |
| edition | A. T. Murray 编校；London: William Heinemann；New York: G. P. Putnam's Sons；1919；CTS version `perseus-grc2` |
| provider | 版本身份：Perseus Digital Library / Scaife ATLAS；物理分发：`PerseusDL/canonical-greekLit` |
| canonical URL | [Scaife ATLAS：`perseus-grc2`](https://atlas.perseus.tufts.edu/library/urn%3Acts%3AgreekLit%3Atlg0012.tlg002.perseus-grc2/) |
| canonical CTS URN | `urn:cts:greekLit:tlg0012.tlg002.perseus-grc2` |
| upstream repository | [PerseusDL/canonical-greekLit](https://github.com/PerseusDL/canonical-greekLit) |
| upstream path | `data/tlg0012/tlg002/tlg0012.tlg002.perseus-grc2.xml` |
| file format | XML；预期为 TEI XML，具体 root、namespace、header、编码声明和媒体类型须在获取后由文件本身验证 |
| language | `grc` |
| intended usage | `canonical_anchor`；《奥德赛》唯一规范 `Book.Line` 引用脊柱 |
| acquisition mode | `required_core / byte_acquisition / commit_pinned_raw` |

Scaife ATLAS 的版本页是稳定的**书目与 CTS 身份入口**，不是未来 `SOURCE_RECORD.yaml` 中的实际文件获取地址。实际字节必须来自固定 commit 下的上游路径。

### 2.2 版本冻结与 URL 规则

未来实际获取前，必须先完成以下确认：

- 选定并人工记录 `PerseusDL/canonical-greekLit` 的一个完整 40 位 commit SHA；
- 确认该 commit 中存在上述唯一 upstream path；
- 不以 `master`、`main`、`latest`、短 SHA 或浏览器文件页作为字节级版本身份；
- 不将旧 Catalog 中的 `grc1` 或其他数字版本覆盖为本来源；
- 同一 P0 批次后续获取 English TEI 与两个 CTS metadata 文件时，必须复用同一完整 commit。

未来不可变获取地址只允许按以下模板生成：

```text
https://raw.githubusercontent.com/PerseusDL/canonical-greekLit/<FULL_40_HEX_COMMIT>/data/tlg0012/tlg002/tlg0012.tlg002.perseus-grc2.xml
```

其中 `<FULL_40_HEX_COMMIT>` 当前必须保持未填写。只有实际执行阶段解析并批准 commit 后，生成的完整地址才可写入具体文件记录的 `url` 字段。

### 2.3 格式与权利确认边界

- 当前只能确认计划格式为 XML、预期内容模型为 TEI；不得在未读取实际文件时预填具体 namespace、XML declaration 或媒体类型检查结果。
- 上游仓库声明默认采用 `CC-BY-SA-4.0`，但实际登记前仍须确认目标文件或其 header 没有更具体的权利说明；如存在覆盖说明，以文件级证据为准。
- 当前不填写 `license` 的最终登记值，不填写 `access_date`，也不创建 `SOURCE_RECORD` 实例。
- 已知上游问题 [#1652](https://github.com/PerseusDL/canonical-greekLit/issues/1652) 与 [#1655](https://github.com/PerseusDL/canonical-greekLit/issues/1655) 必须在未来记录的 `known_issues` 中显式登记；不得直接修改 raw 文件来掩盖问题。

## 3. 目标保存路径

### 3.1 语言目录解释

本任务所说的 `source/original_text/greek/` 表示“Greek 原文资料类别”。既有 Source Package 规范已经规定语言目录使用 BCP 47 / ISO 639 兼容代码，因此唯一物理目录继续使用 `grc/`：

```text
语义类别：source/original_text/greek/
规范物理目录：source/original_text/grc/
```

不得同时创建 `greek/` 与 `grc/` 两套目录，也不得修改 P0 注册表中的既有目标路径。

### 3.2 唯一目标与登记路径

| 用途 | 未来路径 |
| --- | --- |
| raw 目录 | `source/original_text/grc/ody-grc-murray1919/raw/` |
| Greek TEI 唯一目标文件 | `source/original_text/grc/ody-grc-murray1919/raw/ody-grc-murray1919__raw__full.xml` |
| 预留 normalized 目录 | `source/original_text/grc/ody-grc-murray1919/normalized/` |
| 单文件登记记录 | `source/metadata/records/ody-grc-murray1919-raw-full-tei.source.yaml` |
| SHA-256 批量索引 | `source/metadata/checksums/checksums.sha256` |
| 获取日志 | `source/metadata/logs/acquisition_log.jsonl` |
| 质量报告 | `source/metadata/quality/source_quality_report.md` |

路径约束：

- Greek TEI 只能进入上述 `raw/` 目标，不得先放入 `normalized/`、`translations/`、`references/` 或项目根目录；
- raw 文件必须保存 provider 返回的原始字节，不统一换行、不删除 BOM、不做 Unicode NFC、不重编码、不修补标签；
- 获取时可使用同目录临时文件，但只有传输成功后才原子命名为正式文件；失败的临时文件不得冒充来源资产；
- normalized 副本属于未来独立阶段，本次获取不得生成；
- 本 P0-3-A 计划阶段不创建表中任何目录或文件。

## 4. 获取后的登记流程

以下流程只在未来获得明确执行授权并实际取得文件后使用。本阶段不执行、不勾选，也不预填任何结果。

### 4.1 获取前锁定身份

- [ ] 记录完整 40 位上游 commit SHA。
- [ ] 确认目标 upstream path 在该 commit 中唯一存在。
- [ ] 生成包含该 commit 的 immutable retrieval URL。
- [ ] 确认 canonical URL、CTS URN、上游路径、`source_id` 与 `file_id` 互相一致。
- [ ] 确认目标路径不存在需要人工处置的同名已批准文件。

任一身份项不明确时停止执行，状态保持 `pending` 或改为 `blocked`，不得改用可变分支地址继续获取。

### 4.2 原始文件落盘

- [ ] 将传输结果先写入临时路径；完整传输后原子命名为规范目标文件。
- [ ] 确认正式文件存在、是普通文件且大小大于 0。
- [ ] 确认文件不是 HTML、登录页、错误页、限流页或 GitHub 浏览器包装页。
- [ ] 在获取日志中记录开始、成功或失败事件；不得保存凭据或临时签名信息。

只有真实字节到达规范目标路径后，`acquisition_status` 才允许从 `pending` 进入 `acquired`。文件到达不等于验证完成，也不允许直接进入 `approved`。

### 4.3 创建并更新单文件 `SOURCE_RECORD`

以项目级 `SOURCE_RECORD_TEMPLATE.yaml` 为基础，为该物理文件创建：

```text
source/metadata/records/ody-grc-murray1919-raw-full-tei.source.yaml
```

13 个统一字段按以下规则填写：

| 字段 | 获取后的填写规则 |
| --- | --- |
| `source_id` | `ODY-GRC-MURRAY1919` |
| `title` | 与 Scaife canonical identity 和文件 header 核验一致的正式题名 |
| `author` | Homer 的项目统一传统归属表述 |
| `edition` | Murray 1919、`perseus-grc2`，并与文件 header 核验 |
| `language` | `grc`；必须与文件 `xml:lang` / header 一致 |
| `provider` | Perseus Digital Library；物理分发记录为 `PerseusDL/canonical-greekLit` |
| `url` | 包含完整 commit SHA 的 immutable retrieval URL，不写 mutable branch URL |
| `access_date` | 实际获取日，格式 `YYYY-MM-DD`；不得回填本文档日期代替获取日 |
| `license` | 根据仓库许可与文件级权利说明核验后填写 SPDX ID、`NOASSERTION` 或批准的 `LicenseRef-*` |
| `file_type` | `tei_xml`；只有实际格式验证通过后填写 |
| `intended_usage` | `canonical_anchor` |
| `status` | 原始字节、真实 URL、基础身份和 checksum 写入后为 `acquired`；技术验证通过后为 `verified`；人工批准后为 `approved` |
| `checksum` | `sha256:<64位小写十六进制>`；基于正式 raw 文件的实际字节生成 |

同时补齐完整记录契约中的扩展字段：

- `file_id: ODY-GRC-MURRAY1919-RAW-FULL-TEI`；
- `file_path: original_text/grc/ody-grc-murray1919/raw/ody-grc-murray1919__raw__full.xml`；
- 经文件验证得到的 `media_type`；
- 实际 `bytes`；
- `role: canonical_anchor`；
- `state: raw`；
- 含时区的 `retrieved_at`；
- `provider_identity.upstream_commit`；
- `known_issues`；
- `record_status: draft`。

`status` 表示来源文件的获取/验证生命周期；`record_status` 表示登记记录的审批生命周期。二者必须同步推进，但不能相互替代：

```text
status:        pending -> acquired -> verified -> approved
record_status:           draft    -> verified -> approved
```

任一关键检查失败时，`status` 改为 `blocked` 或保留在 `acquired` 并记录失败原因；不得伪装成 `verified`。

### 4.4 生成并核验 checksum

- [ ] 对规范目标路径中的原始字节计算 SHA-256，不先做任何文本转换。
- [ ] 将摘要写入单文件记录：`sha256:<64-lowercase-hex>`。
- [ ] 将同一摘要写入 `source/metadata/checksums/checksums.sha256`：

```text
<64-lowercase-hex>  original_text/grc/ody-grc-murray1919/raw/ody-grc-murray1919__raw__full.xml
```

- [ ] 重新计算一次，并确认实际结果、YAML 值和批量索引三者完全一致。
- [ ] 记录实际文件大小与获取时间。

任何摘要均不得在文件到达前预填。相同 URL 后续返回不同字节时必须建立变更事件和新记录版本，不得静默覆盖旧批准记录。

### 4.5 技术验证与状态更新

- [ ] XML 可由 namespace-aware parser 严格完整解析。
- [ ] XML declaration 与实际字节编码一致；严格解码不产生非法字节或 `U+FFFD`。
- [ ] TEI root、namespace、header、题名、语言和版本身份不互相冲突。
- [ ] CTS identity 精确等于 `urn:cts:greekLit:tlg0012.tlg002.perseus-grc2`。
- [ ] citation scheme 为 `book.line`。
- [ ] 恰有 Book 1–24，编号不缺失、不重复、顺序正确。
- [ ] 每卷 line locator 为可解析的正整数，卷内单调递增且不重复。
- [ ] gap、duplicate、倒序、空 Book 和异常标签全部输出明细。
- [ ] #1652、#1655 及实际发现的异常均进入 `known_issues`；未经人工分类的异常保持阻断。
- [ ] raw 文件未因验证而被修改。
- [ ] `file -> file_id -> SOURCE_RECORD -> checksums.sha256` 一对一闭环成立。
- [ ] 质量报告没有与本文件有关的未处置阻断项。

完成技术检查后：

1. 单文件记录的 `status` 从 `acquired` 更新为 `verified`；
2. `record_status` 从 `draft` 更新为 `verified`；
3. `P0_SOURCE_REGISTRY.md` 中本文件的 `acquisition_status` 更新为 `acquired`，`verification_status` 更新为 `verified`；
4. 人工审核通过后，单文件记录的 `status` 与 `record_status` 才可进入 `approved`；
5. 注册表若采用最终批准态，应将 `verification_status` 更新为 `approved`，并保留审核证据引用。

## 5. Greek TEI 获取完成验收标准

### 5.1 单来源完成定义

只有以下条件全部满足，才认为 **Perseus Greek TEI 单来源获取完成**：

- [ ] `source_id`、`file_id`、canonical URL、CTS URN、固定 commit 和 upstream path 全部唯一且一致；
- [ ] 实际 retrieval URL 包含完整 40 位 commit SHA，不依赖 mutable branch；
- [ ] 目标文件存在于唯一规范 raw 路径，非空且不是错误页面或包装页面；
- [ ] XML、编码、TEI identity、`grc` 语言和媒体类型检查通过；
- [ ] `book.line`、Book 1–24 和 line locator 结构检查通过；
- [ ] 所有结构异常均已记录并完成人工分类；存在未处置阻断项时不得完成；
- [ ] 单文件 `SOURCE_RECORD` 的必填字段及扩展身份字段完整；
- [ ] SHA-256 已基于 raw 原始字节生成，并在实际文件、单文件记录与 checksum 索引之间复核一致；
- [ ] 获取日志和质量报告提供可追溯证据；
- [ ] `P0_SOURCE_REGISTRY.md` 中该文件不再是 `pending`，且状态与真实证据一致；
- [ ] 单文件 `status` 和 `record_status` 均经 `acquired/draft -> verified -> approved` 的顺序推进并获得人工批准；
- [ ] 没有创建 normalized 文本、人物/剧情数据库、改编内容或剧本。

完成规则：

```yaml
gate_id: P0-GREEK-TEI
meaning: single_greek_tei_acquired_verified_and_approved
current_status: pending
completion_rule:
  source_record_status: approved
  record_status: approved
  registry_acquisition_status: acquired
  registry_verification_status: approved
  unresolved_blockers: 0
requires_full_p0_batch: false
does_not_complete:
  - P0 English TEI acquisition
  - P0 CTS metadata acquisition
  - P0 same-commit cross-file verification
  - Gate S1-C
  - Gate S1
```

### 5.2 阻断条件

出现任一项时，Greek TEI 获取不得标记为完成：

- 未固定完整 commit，或 `url` 仍指向 `master`、`main`、`latest`；
- 获取到的不是目标 XML，文件为空、截断、损坏或为 HTML/错误页；
- CTS URN、题名、语言、edition 或 TEI header 与 `perseus-grc2` 身份冲突；
- 文件不在唯一规范路径，或同时出现 `greek/` 与 `grc/` 两套资产；
- 缺少唯一 `file_id`、单文件记录、真实 SHA-256、获取日志或质量报告；
- checksum 三方结果不一致；
- Book 1–24、`book.line` 或 line locator 存在未分类异常；
- 为通过检查而直接修补 raw 文件；
- 在没有真实证据时提前修改状态、填写获取日期、文件大小或 checksum；
- 本阶段越界开始规范化、内容分析、人物/剧情建模、改编或剧本生成。

### 5.3 当前状态

| 项目 | 当前值 |
| --- | --- |
| 单来源获取计划 | `created` |
| 计划评审状态 | `ready_for_review` |
| Greek TEI 获取 | `pending` |
| Greek TEI 验证 | `pending` |
| `source/` 物理目录 | `not_initialized` |
| 来源文件 | `0` |
| 新建具体 `SOURCE_RECORD` | `0` |
| checksum | `0` |
| normalized 文件 | `0` |
| 内容分析或改编产物 | `0` |

下一步只能是人工评审本计划。只有获得后续独立执行授权后，才可锁定具体 commit 并获取 Greek TEI；本 P0-3-A 不执行该动作。
