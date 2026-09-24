# 《八台》BATAYI｜项目进展检查点｜2026-09-24

> 状态：PAUSED / CHECKPOINTED
> 本文件记录当前阶段成果与恢复入口。当前暂停继续开发，不生成新图像、视频或音频。

## 1. 当前阶段

- Storyboard V3 已实际重建并可审阅
- Animatic V3 尚未制作
- 声音、配乐、AI motion、最终视频尚未开始
- SH-05-002 仍为 pending hybrid shot
- 恢复项目时应先审阅 Storyboard V3，而不是继续生成媒体

## 2. Canonical / 边界

- screenplay / SPN / STX / SB / DD / WP 不被生成图反向修改
- GENERATED_IMAGE_CAN_UPDATE_CANONICAL_WORLD=false
- DETERMINISTIC_IMAGE_CAN_UPDATE_CANONICAL_WORLD=false
- 视觉实现服从 canonical；不得为了 provider 能力反改 canonical
- 史料能证实的优先用史料、文献、地图、实景；无法具体重建的保留抽象或 deterministic 表达

## 3. Provider 校准结论

- MMX-01 CLOSED_WORLD_OBJECT_EXCLUSION：避免长 forbidden-noun inventory，优先 closed-world allowed-element specification
- MMX-02 LIGHTING_NOT_ENVIRONMENT：光照属性与环境身份分离
- MMX-03 HUMAN_GROUNDING_BIAS：站立人物易出现脚下 tonal grounding / 空间分层
- MMX-04 PROMPT_BREVITY：provider prompt 优先可执行性
- MMX-05 CANONICAL_EXECUTION_SEPARATION：canonical 完整保存，provider 可压缩但不得新增世界事实
- MMX-06 SILHOUETTE_PHOTOREALISM_BIAS：cutout wording 可降低 photorealism，但 production 泛化有限
- MMX-07 LOW_SEMANTIC_SUBJECT_INSTABILITY：低语义抽象主体会出现省略或过度具体化
- MMX-08 ANONYMITY_FIRST_ROUTE_ESCALATION：strict anonymous human / multi-human 改走 deterministic
- MMX-09 LANDSCAPE_SPECIFICITY_DRIFT：strict generic landscape 不再默认由 MMX 直接生产

## 4. Calibration

### CAL-01
- long negative inventory 失败；closed-world 明显改善；形成 MMX-01～05。

### CAL-02
- silhouette 容易生成摄影式人物；simplified human-form cutout 可降低内部细节；形成 MMX-06。

### CAL-03
- R1 主体省略；R2 矩形；R3 房屋轮廓。
- image-01 判定不适合 strict generic mass，改用 deterministic Python + Pillow 并验证通过。

## 5. Production Frames

原 Shotlist V1.1：31 shots。

完成/验证的主要批次：
- B1 BLACK_FRAME：7
- B2 TEXT_ONLY：16
- B3 DETERMINISTIC_GENERIC_MASS：1
- B4 STRICT_ANONYMOUS_HUMAN：2（MMX 失败后 deterministic remake 通过）
- B5 MULTI_HUMAN：1（3 人 exact count）
- B7 EXACT_GROUP：1（13 人 exact count）

Production evidence：
- B4：2/2 strict-anonymity MMX shots 失败
- deterministic B4：2/2 通过
- B5：3 人 exact count 通过
- B7：13 人 exact count 通过
- strict anonymous human / strict multi-human / exact count 均优先 DETERMINISTIC_2D

## 6. B6 Abstract Landscape

SH-01-002：
- canonical scene core 基本存在，restrained / flat-diffuse 合规
- 但存在 canvas-fill / scale 问题
- 后续采用 non-generative remediation
- 无 verified visual source，只能归类为 ABSTRACT_IMPLEMENTATION_VISUAL

SH-07-002 MiniMax 出现明显 closed-world semantic drift：
- vintage truck
- horses / harness
- human
- road sign
- paved highway / center line
- warm golden-hour lighting
- 地理 / 时代具体化

结论：strict generic abstract landscape 不再默认由 MMX 直接生产。

## 7. Visual Bible / Routing

已形成：
- Visual Language Bible V2
- Style Calibration Profile V1 / V1.1 / V1.2 / V1.3
- Visual Render Routing Matrix V1 / V1.1 / V1.2

Deterministic 优先：
- black frame
- text-only
- strict featureless background
- precise frame position / area
- low-semantic abstract mass
- strict anonymous human
- strict multi-human / exact count
- strict generic abstract landscape

MiniMax 条件使用：
- semantic scene where provider specificity is tolerable
- atmosphere / landscape only when canonical allows limited specificity

Hybrid：
- generative atmosphere + deterministic critical canonical element

## 8. Animatic V1 / V2

Animatic V1：
- 31 shots × 3s review placeholder
- runtime 93s
- 仅用于检查 shot order / visual language

Animatic V2：
- review timing 约 255.6s / 4:15.6
- TEXT runtime 110.75s
- BLACK runtime 26.0s
- IMAGE runtime 89.0s
- SH-05-002 pending 30.0s review timing
- 无音频、无 AI motion
- timing 仍为 review timing，不是 canonical timing

V2 暴露的主要问题：画面太少、文字太多。因此暂停 timing refinement，转向 Visual Enrichment。

## 9. Visual Enrichment

旧结构：full-screen text 16 / black 7 / image 7 / pending 1。

V3 方向：
- date cards 合并 8 个
- full-screen text 大幅减少
- 文献 / 信件 / 地图 / deterministic visuals 增加
- 目标不是多 AI 图，而是让证据本身成为画面

视觉材料优先级：原始档案、历史照片、文献扫描、信件/报告/书刊、历史地图、地理/地形、已验证现场照片、canonical 视觉资产、deterministic 图形，最后才是 generative imagery。

## 10. V3 Visual Evidence Pack

确认材料：
- Häring 1934 letter：A-0002-01，Archiv des Erzbistums Bamberg
- Fogolla / Le Missioni Francescane 1896 页面：671, 672, 673, 674, 675, 676, 677, 678, 712, 718

关键应用：
- SH-04-003：p.672，PRIMARY_EVIDENCE_VISUAL，canonical fit HIGH
- SH-01-004：p.676，contextual / partial fit；页面不含“我要在这里建一座小教堂”原句，必须明确 non-quote
- SH-EP-002：Häring 1934 letter 原始信件视觉，并保留 unresolved boundary subtitles
- SH-02-002：未找到直接证明 1868 / Pa-tae / 一户五口基督徒家庭的对应页面，保留 FULL_SCREEN_TEXT
- SH-EP-004：无直接支持转为 archival page 的来源，保留 FULL_SCREEN_TEXT
- SH-01-002：未找到 verified site photo / missionary map，仍是 unresolved visual evidence gap

## 11. Storyboard V3 实际重建

- V3_TOTAL_SHOT_COUNT = 23
- DATE_CARD_MERGE_COUNT = 8

互斥分类：
- FULL_SCREEN_TEXT = 5
- BLACK_FRAME = 7
- PRIMARY_EVIDENCE_VISUAL = 2
- SECONDARY_CONTEXT_VISUAL = 1
- ABSTRACT_IMPLEMENTATION_VISUAL = 1
- DETERMINISTIC_SYMBOLIC_VISUAL = 6
- PENDING = 1

8 个 date-card merges：
- SH-01-001 → SH-01-002
- SH-02-001 → SH-02-002
- SH-03-001 → SH-03-002
- SH-04-001 → SH-04-002
- SH-05-001 → SH-05-002
- SH-06-001 → SH-06-002
- SH-07-001 → SH-07-002
- SH-EP-001 → SH-EP-002

日期文字保持 verbatim，以 restrained overlay 呈现。

## 12. V3 Deterministic 美术升级

ANONYMOUS_HUMAN_ORGANIC_CUTOUT_V1：
- 用于 SH-01-003 / SH-03-002 / SH-04-002 / SH-07-003
- 仍禁止 face / hair / clothing / identity / ethnicity / age / costume / internal shading / texture
- 允许 height ±3%、shoulder width ±5%、body-axis ≤3°、head offset ±2%、contour asymmetry
- 目标：从 UI pictogram 转为“匿名人的存在”

GENERIC_MASS_NATURALISTIC_CONTOUR_V1_1：
- 用于 SH-06-002
- 允许 8–12 contour anchors、organic irregularity、asymmetry、less geometric outline
- 严格保持 uniform near-black fill、no internal tonal variation、no gradient、no texture、no internal edge、non-recognizable、non-architectural

## 13. 当前暂停点

现在不要继续制作 Animatic V3。

恢复项目时优先：
1. 审看 BATAYI_STORYBOARD_V3_REVIEW
2. 比较 V2 → V3 contact sheets
3. 判断 V3 是否真正摆脱“PPT 感”
4. 检查 document visuals 是否又变成“扫描件 PPT”
5. 检查 organic human cutouts 是否仍过于 pictogram
6. 检查 generic mass refinement
7. Storyboard V3 视觉通过后，再进入 Animatic V3
8. 最后再处理 SH-05-002、声音、motion/video

## 14. 外部 handoff workspace

主要工作产物当前位于：/home/ubuntu/research-to-drama-handoffs/

关键目录：
- BATAYI_MMX_STYLE_CALIBRATION_PROFILE_V1_3/
- BATAYI_VISUAL_RENDER_ROUTING_MATRIX_V1_2/
- BATAYI_PRODUCTION_FRAMES_V1/
- BATAYI_ANIMATIC_V1/
- BATAYI_ANIMATIC_V2/
- BATAYI_VISUAL_ENRICHMENT_AUDIT_V1/
- BATAYI_VISUAL_ASSET_PACK_V3/
- BATAYI_STORYBOARD_V3_REVIEW/

大型图像、视频、PDF 与 server-side build outputs 不在本 checkpoint 中复制到 GitHub；本文件是当前阶段的可恢复项目状态索引。

## 15. GitHub checkpoint

Repository: conanxin/classic-to-drama-engine
Checkpoint date: 2026-09-24

Intent：暂停继续开发，并把《八台》当前研究 / 视觉生产 / 路由 / Storyboard V3 状态写入项目 GitHub，作为后续恢复工作的明确起点。
