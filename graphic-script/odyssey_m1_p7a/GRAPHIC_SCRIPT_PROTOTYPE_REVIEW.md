# Graphic Script Prototype Review

status: `PASS_P7A_INTERNAL_PROTOTYPE_REVIEW`  
episodes: `EP01 / EP19 / EP27`  
scene coverage: `15 / 15`  
review modes: source audit, design comparison, desktop browser, 390×844 mobile Chromium, accessibility/interaction, publication verification

## 1. 审查边界

本报告验证原型是否构成真正可连续阅读的图文剧本、人物与关系辅助是否按设计工作、Script Mode 是否保持完整，以及 Web 产品能否稳定运行。它是内部独立复核，不冒充招募读者后的可用性研究。真实“更愿意追读”的行为证据需要未来 P7C 明确授权后，以真实读者测试取得。

## 2. 三集原型结论

### EP01 — 世界与主问题建立

PASS。8 个本集角色/群体先由稳定识别卡复位，5 场分别用酒杯、门矛、账板、公共告示和不合身的剑承担视觉记忆。忒勒马科斯、佩涅洛佩、雅典娜/门忒斯和求婚者不再只是一串名字；每场冲突与家庭空间控制都有具体位置。EP01 末尾同时建立明日集会与秘密出海，具备继续进入 EP02 的双钩子。

### EP19 — 伪装与识别

PASS。读者层显示“奥德修斯／乞丐”，场内判断仍逐场推进：试探、神改变条件、船钉/航路验证、身体记忆、共同作战地图。4 张人物卡和 3 条关系提示没有提前把忒勒马科斯的相信写成既成事实。5/5 技术板/批准主帧建立茅屋、橄榄树与父子距离，解决纯文本中“谁知道什么”的负担。

### EP27 — 多人动作与关系追踪

PASS。8 个角色/群体使用阵营色、姓名、职责和物件四重编码；5 场持续更新箭数、门、柱线、武器库与武器 custody。求婚者作为集团显示，欧律马科斯、安菲诺摩斯和墨兰提俄斯在承担不同责任时拆出。墨兰提俄斯开场只显示“山羊倌”，“背叛者”被定义为 EP27-S04 后的 revealed alias，未提前剧透。移动端场内辅助改为关系/空间/道具三行，不遮挡图像或正文。

## 3. 用户问题检查

| 问题 | 原型回应 | 内部结论 |
|---|---|---|
| 能否快速知道本集讲什么 | cover 的 story stage + core conflict | PASS |
| 是否更容易记住人物 | cast rail、颜色/形状/道具、tap details | PASS（结构） |
| 能否知道谁与谁冲突 | 场级 conflict goal + relation tip + cast chips | PASS |
| 能否跟上空间变化 | 每场 space tip + approved visual anchor | PASS |
| 是否愿意继续点下一集 | end hook + next Script/Graphic 入口 | READY FOR USER TEST，不虚构行为 PASS |

## 4. Source fidelity

- 三个 source SHA-256 与 V2 manifest 一致；
- 15/15 原场次一一对应；
- 35 条关键对白逐字存在于 V2；
- 每场的完整 V2 原文通过 native details 可展开；
- Graphic narrative 只提炼动作与因果，不新增台词；
- Script Mode 30 集与 150 场原解析结果不变。

## 5. Character recognition review

16 个正式条目覆盖核心四人、忠诚 household、关键求婚者、集团、神明、菲埃克斯与怪物/异境。所有 prototype cast ID 均能解析。颜色从 P4 视觉系统延伸，同时保留姓名、轮廓与物件，避免只靠颜色。雅典娜与奥德修斯的伪装使用读者层/场内层，而不是把悬念隐藏或直接泄露。

## 6. Web 与移动验证

### 应用内真实浏览器（native 1280×720）

- `/graphic/` 主入口可见三集并可进入；
- EP19 显示 5 个场块、4 张人物卡、5 个 source layer、3 条当前关系；
- Script → Graphic → Script 双向 URL 与完整场数均正确；
- 原剧本 details 可键盘/点击展开；
- 页面横向溢出 0。

### 精确 Chromium 390×844

EP01、EP19、EP27 均为：5 scene blocks、5 semantic scene headings、5 source layers、2 mode links、`overflow: 0`、console errors 0。滚至最后一场后，lazy image 均加载成功并选择 `-w720.webp`；原文展开成功。EP27 11,067px 长页面完成整页连续阅读检查，没有固定侧栏压缩正文。

### Desktop 1440×900

EP19 首屏 cover、冲突、模式切换、时长/来源均在第一屏；批准视觉与文本形成约 43/57 的双栏。首屏无被拒绝视觉；初次测试约 1.01 MB。随后为人物小卡增加 `sizes="80px"`，使其从 1600px 候选降到 720px 候选；cover/scene visual 也获得用途化 sizes。

## 7. Concept → implementation fidelity ledger

概念文件：

- `design/GRAPHIC_MODE_CONCEPT_DESKTOP.png`
- `design/GRAPHIC_MODE_CONCEPT_MOBILE.png`

实施截图（QA 临时、不入 Git）：

- `output/playwright/p7a-ep19-desktop.png`（1440×900）
- `output/playwright/p7a-ep19-mobile.png`（390×844）
- `output/playwright/p7a-ep27-mobile-full.png`（390×844 full page）

一致性要点：

1. **双模式控制**：概念和实施都在 episode identity 后提供等宽 Script/Graphic switch；
2. **人物识别 rail**：均采用稳定肖像/字标、角色名、当前称谓和阵营色，不把说明塞进场景正文；
3. **场次进度**：desktop 左 rail、mobile 横向 01–05，服务连续阅读而非 dashboard；
4. **场块层次**：画面 → 在场人物 → 关系/空间/道具 → reduced narrative → exact dialogue → source layer；
5. **视觉语气**：墨黑、暖纸、土金/血锈 accent、大宋体标题、细规则延续 cinematic editorial archive；
6. **辅助位置**：desktop 关系/空间靠右，mobile 合并到图后，均不覆盖主体；
7. **原文回路**：概念中的“展开原剧本”在实现中成为 15 个可操作 native details。

### Above-fold copy 差异

概念桌面首屏把 cast rail 与一个 scene block 同时塞入视口，并误写“1/10 场”；实际 authority 每集是 5 场。实现首屏改为 title、story stage、core conflict、双模式、时长/场次/来源和批准 cover，cast rail 在下一段完整出现。这减少首屏认知密度，同时让用户十秒内先明白作品和阅读方式。

概念移动首屏含非源绑定人物/场景文字；实现用 EP19/EP27 的正式 V2 事件、批准 P4 图像和 5 场结构替换。概念底部固定上一场/下一场控制会占用 390×844 正文高度，实现改为较薄的 sticky 01–05 进度行。

### 有意偏离与 material mismatch

- 概念中的生成故事画面和人物组合不是 P4 authority，实施全部替换为 publication allowlist 中的 approved P4 hero、character、set 和 technical storyboard；
- 概念虚构的 10 场、角色名/关系和对白未进入产品；
- EP27 被拒绝的 `P4-HF-44` 未出现，使用 approved `P4-HF-45`；
- 联系表式概念在实现中拆成可读场块，不使用缩小到不可读的分镜总表；
- 未发现仍需修复的 material mismatch。

## 8. QA 中发现并解决的问题

| issue | severity | fix | verification |
|---|---|---|---|
| Graphic 入口在 light system mode 下深色区域文字继承错误 | S1 | 固定 Graphic index 自有 ink/paper token | 浏览器截图 PASS |
| 入口 hero picture 未成为稳定 grid item | S1 | 增加 `hero-visual` figure wrapper | 1280 首屏双栏 PASS |
| 场次名不是语义 heading | S2 | `h2` 化 | 3 集 × 5 headings PASS |
| 关系图显示内部英文 ID | S2 | 映射为中文人物/家宅名 | built HTML PASS |
| 小人物卡请求 1600px 图 | S2 | ResponsiveImage `sizes` 参数与 80px usage | build/browser PASS |
| 墨兰提俄斯提前出现“背叛者” | S1 | revealed alias 固定到 EP27-S04 | verifier PASS |

## 9. 综合结论

P7A 的结构性命题成立：同一集可以保留完整 Script Mode，同时通过 Graphic Mode 的人物、关系、空间、道具与批准视觉，形成不依赖 Markdown 原样堆叠的连续阅读版本。三种困难集均达到内部原型 PASS，设计可扩展到 30 集。真实读者的记忆改善、完成率与下一集点击意愿仍须在未来 P7C 测试，当前不虚构该证据。

推荐下一阶段二选一：

- `ODYSSEY-P7B 30-EPISODE GRAPHIC SCRIPT ROLLOUT`；
- `ODYSSEY-P7C GRAPHIC SCRIPT WEB POLISH AND READER TESTING`。

P6 继续 `PAUSED_BY_USER`。

