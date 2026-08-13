# 《奥德赛》P0 来源注册表

> 项目：Classic-to-Drama Engine  
> 阶段：Phase 1-E / Source Acquisition / P0-1  
> 日期：2026-08-10  
> 当前状态：`blocked`（Greek 已获取但验证失败；English 已获取并通过技术验证；P0 总体未完成）  
> 边界：本表只登记 P0 最小来源集；Greek 与 English 行分别记录 P0-3-B、P0-4-B 的真实状态，两个 CTS metadata 项仍是预定目标。

## 1. 注册表规则

- `target_path` 以 `source/` 逻辑根为起点，并与 `03_SOURCE_ACQUISITION_EXECUTION_CHECKLIST.md` 保持一致。
- 一个物理文件占一行；因此 Required Metadata 以 textgroup 与 work 两个 CTS XML 文件分别登记。
- 状态必须反映真实证据：未执行项保持 `pending`；文件到达后可进入 `acquired`；失败验证使用既有 `verification_failed`。
- 本注册表不直接填写访问日期、实际获取 URL 或 SHA-256；这些值只进入具体 `SOURCE_RECORD`、checksum 索引和获取日志。未获取项不创建占位符。

## 2. P0 Minimum Source Set

| 类别 | 文件 | `source_id` | `target_path` | `acquisition_status` | `verification_status` |
| --- | --- | --- | --- | --- | --- |
| Perseus Greek Text | Greek TEI (`perseus-grc2`) | `ODY-GRC-MURRAY1919` | `source/original_text/grc/ody-grc-murray1919/raw/ody-grc-murray1919__raw__full.xml` | `acquired` | `verification_failed` |
| Perseus English Translation | English TEI (`perseus-eng3`) | `ODY-ENG-MURRAY1919` | `source/translations/en/ody-eng-murray1919/raw/ody-eng-murray1919__raw__full.xml` | `acquired` | `verified` |
| Required Metadata | CTS textgroup metadata | `ODY-META-PERSEUS-CTS` | `source/references/textual_reference/ref-ody-perseus-tei/raw/ody-meta-perseus-cts__raw__textgroup.xml` | `pending` | `pending` |
| Required Metadata | CTS work metadata | `ODY-META-PERSEUS-CTS` | `source/references/textual_reference/ref-ody-perseus-tei/raw/ody-meta-perseus-cts__raw__work.xml` | `pending` | `pending` |

## 3. 当前计数

| 指标 | 数量 |
| --- | ---: |
| P0 登记文件 | 4 |
| `acquisition_status: pending` | 2 |
| `verification_status: pending` | 2 |
| 已获取文件 | 2 |
| 已验证文件 | 1 |
| 验证失败文件 | 1 |

Greek TEI 因 locator 结构异常保持 `verification_failed`；English TEI 已达到 `acquired / verified`，但人工批准仍未执行；两个 CTS metadata 文件继续保持 `pending / pending`。本注册表不包含 P1、P2、link-only 参考入口或任何作品内容。
