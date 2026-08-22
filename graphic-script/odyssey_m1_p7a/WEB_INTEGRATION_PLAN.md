# Graphic Script Web Integration Plan

status: `P7A_WEB_ARCHITECTURE_FROZEN`  
site: Astro static archive  
deployment base: `/classic-to-drama-engine/`

## 1. 路由选型

| 方案 | 优点 | 缺点 | 决定 |
|---|---|---|---|
| 同页 JS 模式切换 | URL 少 | 分享/SEO/静态索引含糊；页面 payload 增大 | 不采用 |
| `/graphic/episodes/01/` | Graphic 目录整齐 | 把同一集拆成两类资源；与既有 episode hierarchy 远 | 不采用 |
| `/episodes/01/graphic/` | 同一集为主资源；独立 URL/SEO；不破坏 Script route；可静态生成 | 需维护双入口 | **采用** |

正式结构为 `/graphic/` 总入口、`/episodes/NN/graphic/` 图文页、`/episodes/NN/` 原剧本页。未完成 Graphic 的剧集不显示可点击模式入口，避免死路。

## 2. 导航与入口

- 主导航增加“图文”，指向 `/graphic/`；
- 首页 archive rail 增加 Graphic Mode；
- `/episodes/` 顶部说明原型集；
- EP01/19/27 Script 页面显示双模式 switch；
- Graphic 页顶部使用相同 switch，active state 和 `aria-current` 清楚；
- Graphic 页末尾同时提供下一集 Script、下一个 Graphic 原型和本集完整 Script。

## 3. 页面结构与交互

Desktop：cover → previously/core conflict → cast strip → relationship now → 左侧 sticky 场次 progress + scene stream + 场内关系/空间/道具提示。Mobile：全部改为单列，人物卡横向滚动，场次切换保留轻量 sticky row，右侧辅助并入每场。

人物卡使用 native `details/summary`，hover 不是依赖；完整原剧本也用 native details。唯一增强脚本是 IntersectionObserver 更新场次进度及记录最近阅读模式。禁用 JS 后所有内容、链接和展开交互仍可用。

## 4. 搜索与 discoverability

- Pagefind 与 deterministic CJK index 将 Graphic 页面标为 `type: 图文剧本`；
- 搜索结果 title 使用 `EPxx《标题》图文剧本`，与 `完整剧本` 明确区分；
- 人名/道具/地点搜索可命中 reduced narrative、关系提示与关键对白；
- 同一集两条结果时，普通探索入口可提高 Graphic 权重，精确“完整剧本/场次/对白”查询优先 Script；
- `/graphic/` 通过主页、剧集目录、主导航进入，而不是藏在制作档案中。

## 5. SEO 与 metadata

- 每个 Graphic route 有独立 title、description、Open Graph image 与 canonical；
- canonical 绑定 public GitHub Pages subpath，不与 Script page 互指为同一内容；
- sitemap 自动纳入四个新增 route；
- 搜索摘录来自图文叙事而非被折叠的完整剧本重复内容；完整 source layer 标为 pagefind ignore；
- 所有内部 link 使用 `withBase`，保证 GitHub Pages deep link。

## 6. 性能

- cover image `eager/fetchpriority=high`，每场图 lazy；
- 使用 publication pipeline 已生成的 720/1600 WebP 与内在尺寸；
- 不在 Graphic 页面嵌入视频或加载 30 集 animatic；
- 每页只读取该集静态 JSON 与页面必要媒体；
- 无客户端框架 hydration；交互用原生 HTML + 小型页面脚本；
- 30 集扩展后仍按 route split，不产生全季单页 payload。

## 7. 可访问性

- 模式切换是 `nav`，active 链接使用 `aria-current=page`；
- 人物与原文使用键盘可操作的 native details；
- 每个场块为 heading 顺序中的 section；
- 人物颜色辅以姓名/道具/轮廓，不只靠色；
- 场次 sticky nav 不遮挡 focus，场块设置 scroll margin；
- alt 说明画面承载的叙事/识别功能，并标技术板类型；
- reduced-motion 环境不加入平移/缩放动画。

## 8. 内容生成与验证

`site/scripts/build-content-data.mjs` 从 P7A JSON 与冻结 V2 读取数据，不复制第二套 Markdown 剧本。`verify-graphic-prototypes.mjs` 验证：

- EP01/19/27 三集与 15 场完整；
- source SHA-256 精确；
- 精选对白逐字存在于 V2；
- cast ID 全部解析到 recognition system；
- 所有视觉在 publication allowlist 中且 `APPROVED`；
- 六个 rejected P4 target 不出现；
- built route、双模式切换、原文展开层、隐私与 base-path 完整。

## 9. 发布边界

P7A 只增加 Graphic 系统、三集 prototype data 和 Web routes。它不改 V2/P3/P4/P5/Runtime，不进入 P6，不进行读者追踪/账户/CMS。真实外部读者研究属于未来 P7C，只有用户另行授权才进行。

