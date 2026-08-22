# 《归途：奥德修斯》Graphic Script System

status: `FROZEN_P7A_PROTOTYPE_SYSTEM`  
phase: `ODYSSEY-P7A`  
format: `illustrated screenplay / graphic script / visual reading edition`  
source authority: V2 screenplay → P4 lookdev/storyboards/design → P5 animatic/previs → P3/P5 production geography

## 1. 目标与用户问题

Graphic Mode 不是“给剧本配几张图”，而是为普通读者建立第二种、可连续阅读的叙事层。它首先解决五个问题：人物姓名难记、关系负担高、空间难以脑补、纯文本长读疲劳，以及多人/动作场面中视线丢失。其成败指标不是图像数量，而是读者能否迅速回答：这一集要做什么、这一场谁阻止谁、人物现在是什么身份、空间里发生了什么改变、为什么继续读。

## 2. 双模式约束

| 模式 | authority | 阅读任务 | 允许变化 |
|---|---|---|---|
| Script Mode | `scripts/odyssey_m1_v2/episodes/EPxx.md` | 阅读完整 V2 剧本 | 仅解析与排版，不改字 |
| Graphic Mode | 本系统的源绑定场块 | 快速理解人物、关系、空间与戏剧变化 | 提炼、压缩、结构重排、图文化重述 |

Graphic Mode 绝不覆盖 Script Mode。每个 Graphic 场块都提供“展开原剧本”，完整显示同一场的 V2 文本；页面顶部保留显式双模式切换。Graphic Mode 中标为关键对白的文字必须逐字存在于 V2；压缩叙事不能改变谁行动、谁选择、谁受损、谁识别、谁承担后果。

## 3. 路由与信息架构

采用嵌套路由：

- `/graphic/`：Graphic Mode 入口与原型目录；
- `/episodes/01/graphic/`：EP01 图文模式；
- `/episodes/01/`：EP01 完整剧本模式；
- 相同模式扩展至 `/episodes/30/graphic/`。

这种结构把“一集”保留为主资源，以末级路径表达阅读方式。它不破坏既有剧本 URL，分享链接能明确指向一种阅读体验，静态生成与 SEO 也可分别建立 canonical、标题和描述。未完成 Graphic 版本的集数不显示失效入口。

## 4. Episode 模板

1. **Episode Cover**：集号、标题、故事阶段、批准主视觉、时长、来源；
2. **Previously On**：只复位进入本集所需状态；
3. **Core Conflict**：一句可执行的本集冲突；
4. **Cast in This Episode**：横向人物识别条，可点击展开；
5. **Relationship Now**：本集开始时人物间有效关系，按 spoiler level 控制；
6. **Scene Stream**：按原剧本五场顺序连续阅读；
7. **End Hook**：由本集不可逆变化产生，而非总结；
8. **Next Entry**：下一集 Script Mode、下一个 Graphic 原型、本集完整剧本。

## 5. Scene Block 模板

每场必须包含：

- `scene_id` 与原场次一一对应；
- 地点/时间与本场 `conflict_goal`；
- `characters present` 人物识别 chip；
- 一个批准视觉锚点，且清楚标示 story frame、technical storyboard、set anchor 或 identity anchor；
- `relation_tip`：谁影响谁，不能提前泄露场内未知；
- `space_tip`：入口、距离、控制区或行动路线；
- `prop_tip`：本场承载身份/选择的具体物；
- 两段左右的 reduced narrative；
- 2–3 条 exact-source essential dialogue；
- `irreversible_change`；
- 可展开的完整 V2 本场原文。

缺少冲突、视觉锚点、关系、空间、道具或不可逆变化的场块不得发布。

## 6. 图像类型系统

| 类型 | 主要用途 | 原型建议量 | 优先级 |
|---|---|---:|---|
| Episode cover key art | 立即建立本集人物/压力/色调 | 1/集 | 必须 |
| Recognition portrait/card | 稳定人物识别，不承担事件叙述 | 核心角色按需 | 必须 |
| Location/environment anchor | 解释门、桌、路径、高差与控制区 | 1–2/集 | 高 |
| Scene establishing frame | 复位人物和空间 | 至少 1/场 | 必须 |
| Conflict beat frame | 冲突策略或力量关系改变 | 0–2/场 | 高 |
| Emotional close-up | 只在识别、选择或代价发生时使用 | 0–1/场 | 中 |
| End-hook frame | 保留尚未解决的动作/问题 | 0–1/集 | 高 |

P7A 网页只发布 P4/P5 publication allowlist 中的 `APPROVED` 资产。技术板必须标为 `TECHNICAL STORYBOARD`，不得冒充 final art。设计概念图只说明版式，不是故事 authority，也不进入读者页面。

## 7. 文本压缩规则

### 完整保留

- 造成选择、身份验证、责任归属或不可逆后果的关键对白；
- 原剧本场次顺序、人物行动主体和结果；
- 首次建立 recognition object 的事实；
- 误解、迟疑、回避本身是剧情时的必要节拍。

### 可改为叙事 prose

- 可由一幅批准图像承担的连续空间动作；
- 重复说明相同空间或状态的动作句；
- 为制作阅读写出的技术性移动，但其结果必须留下。

### 可压缩

- 对已可见动作的再次解释；
- 不改变人物策略的应答；
- 同一信息被连续复述的部分。

### 放入 expandable layer

- 完整动作细节；
- 非精选对白；
- 专业剧本节奏与过场；
- 需要深读但会打断 Graphic 流的制作信息。

压缩后的 narrative 是忠实转述，不使用新台词。所有引号内文字均须通过 exact-source verifier。

## 8. 人物、关系与 spoiler 规则

- 人物用 **姓名 + 稳定色 + 轮廓/物件** 三重编码，不能只依赖颜色；
- 首次出现先说当前功能，再补神话姓名；
- 神的读者身份与其人类伪装并列，但场内未知仍保留；
- 奥德修斯伪装期显示“双层身份：读者知道 / 场内人物判断中”；
- 群体先以阵营表示，只有责任不同才拆成个人；
- 关系分为 `public`、`reader`、`revealed`，后者只有事件发生后才出现；
- hover 只作增强；移动端 tap/details 必须完整可用；
- “上次出现”只复位已有事实，不替未来识别给答案。

## 9. 视觉节奏

- 每场先空间后表情；人物位置不清时不使用孤立 close-up；
- 连续两个场块避免同一构图和同一图文比例；
- 关键对白旁保留留白，禁止用装饰图压低阅读性；
- 图像说明始终标注 authority；
- EP01 使用占领赭红与家庭土金，EP19 使用返乡麦金与农舍橄榄，EP27 使用战斗血锈与烟黑青铜；
- 一场的视觉不承担下一场信息，避免视觉剧透；
- 场块完成时必须可指出一个可见的状态变化。

## 10. P7A 原型边界

P7A 固定验证三种难题：EP01 的世界/主问题建立，EP19 的伪装与父子识别，EP27 的多人动作与空间追踪。每集五场全部覆盖，形成 15 个可连续阅读场块；不是传统漫画页，也不生成新的全量角色/场景视觉。其内部评审能验证结构、可访问性、移动布局和 source binding，但不能冒充真实外部读者测试。

## 11. 30 集扩展规则

1. 每集先冻结 source SHA-256，再产生 Graphic 数据；
2. 每集五场 100% 覆盖，不许只做精彩场；
3. 每场至少一个视觉锚点；无批准 story frame 时优先使用 technical board / set / identity anchor；
4. 原型人物系统扩展而不是每集另造配色；
5. 每 5 集做人物 alias、关系 spoiler、道具与地点连续性审计；
6. 先处理人物/空间负担最高的集，再处理对话主导集；
7. 量产不得把一场拆成几十张高成本漫画图；
8. 所有新视觉必须进入显式 publication allowlist；
9. 每集独立通过 source dialogue、scene coverage、asset approval、mobile 与 no-script-regression 检查；
10. P7B 才可扩展到 30 集，P7A 在三集原型完成后停止。

## 12. Web 设计 token

- `ink #151513` / `paper #d8cfbb`：继承现有 cinematic editorial archive；
- 集级 accent 来自 P4 color script，不另造品牌色；
- 中文正文优先系统宋体 fallback，导航/标签使用系统黑体；
- desktop：左侧场次进度 + 中央叙事 + 右侧关系/空间辅助；
- mobile：单列场块 + 横向人物条 + 轻量 sticky 场次导航；
- 图片 responsive WebP、lazy loading；封面仅一张 eager；
- 无 JavaScript 时全文、人物、关系和场次仍可读。

