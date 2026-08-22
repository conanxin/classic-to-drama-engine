# Graphic Script Image Coverage Plan

status: `P7A_SCALE_PLAN_COMPLETE`  
scope: 30 episodes / 150 scenes  
production mode: reuse-first, approved-authority-first, medium-density illustrated screenplay

## 1. 覆盖底线

- 30 集每集 1 张 cover key art；
- 150 场每场至少 1 个视觉锚点；
- 人物第一次进入一个新身份状态时提供 recognition card/approved state；
- 识别物（name、story、scar、bow、axes、bed、father/land、community）首次出现必须建立清楚视觉记忆；
- technical storyboard、set anchor、identity sheet 可以承担“解释空间/身份”的图，但必须正确标注类型；
- 同一批准图可在 cover 与同一集关键场复用，页面通过裁切/说明区分功能，避免为了数量制造漂移视觉。

## 2. 密度分级

| 层级 | 场景特征 | 建议图量 | 适用 |
|---|---|---:|---|
| A 视觉必要 | 新世界、动作地理、识别、神迹、怪物、不可逆状态变化 | 2–4/场 | EP05、10、14、19、25、27–30 等 |
| B 标准叙事 | 人物目标明确、空间稳定、一个主要转折 | 1–2/场 | 大多数家庭/航行/政治场 |
| C 图少文多 | 对话主导、同一稳定空间、表演连续性优先 | 1/场 | 认亲前试探、谈判、余波 |

“图少文多”不等于无图，至少要有地点、物件或共享构图作为场锚。performance scene 不被碎图切成短视频式覆盖。

## 3. 30 集量产建议

| 集段 | 主要阅读难点 | 密度策略 | 优先资产 |
|---|---|---|---|
| EP01–05 | 伊萨卡人物与青年远行世界建立 | EP01/05 A，其余 B | S1、主角 identity、港口/海 |
| EP06–10 | 叙述层、法埃西亚、独眼巨人 | EP10 A，其余 B | approved hero、Phaeacia set、Cyclops boards |
| EP11–15 | 魔法、冥界、海峡、多种异境 | 11/13/14/15 A | technical boards、environment anchors、sound/shape cues |
| EP16–20 | 返乡、伪装、父子相认、身份层叠 | 19 A，18/20 B+ | farm, dual identity, recognition props |
| EP21–25 | 家中试探、伤疤、弓与十二斧 | 23/25 A | S1 states、scar/bow/axes |
| EP26–30 | 空间封锁、战斗、夫妻/父亲/共同体识别 | 26–30 A；29 保持表演连续 | S1 battle states、boards、bed/olive/boundary props |

## 4. 必须有图的事件

- 新 standing set 第一次进入；
- 伪装身份改变、伤疤发现、弓/斧/婚床/土地验证；
- 谁控制门、武器、船、绳、火或出口发生变化；
- Cyclops、Circe transformation、Sirens、Scylla/Charybdis、Underworld、Athena transformation、Poseidon pressure；
- 任何多人动作场中阵营或武器 custody 改变；
- 结尾 hook 是空间/物件状态而非纯对白时。

## 5. 可图少文多的事件

- 同一地点内的连续证词判断；
- 共享构图能保护表演连续的夫妻、父子或主仆试探；
- 已建立空间中不改变 blocking 的短对话；
- 战后责任、哀悼、共同体协商等以脸与共享距离为核心的段落。

这些场仍需 scene establishing anchor，随后用 reduced prose + exact dialogue 保持阅读流。

## 6. 量产数量范围

基础层：30 covers + 150 scene anchors = 180 个画面用途。考虑批准资产复用、每集 3–7 个关键 beat 与部分场 2 张图，目标出版集合约 260–330 个独立 image placements；不等于 260–330 个全新生成图。优先顺序：既有 approved hero frame → technical board → approved set/character/prop anchor → P5 still extraction（须单独批准）→ 有限新增视觉。

## 7. 性能与发布

- 每集首屏只 eager 加载 cover；其余 lazy；
- 默认移动端 720px WebP，桌面按 responsive `srcset`；
- 一集页面不嵌入 animatic/video；通过链接进入媒体页；
- scene visual 采用固定长宽/内在尺寸降低 CLS；
- publication manifest 显式记录 source、published path、bytes、SHA-256、authority、status；
- rejected、concept-only、temporary render 永不进入 active prototype。

## 8. 扩展批次

推荐 P7B 批次：

1. EP02–05：验证开季连续阅读；
2. EP16–18、20、21–25：补齐返乡到弓赛的识别链；
3. EP26、28–30：补齐战斗和最终识别；
4. EP06–15：完成异境与叙述段；
5. 全季 continuity / anti-drift / mobile / source-binding audit。

每批 5 集完成后冻结 cast alias、relationship spoiler、recognition object、地点、道具与页面 payload 报告。

