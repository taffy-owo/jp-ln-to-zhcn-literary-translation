# 批量/整卷翻译细则

## 关键风险
整卷一次性交给模型时，质量问题通常不是“不懂词”，而是：

1. 上下文没建好，称呼、人设、术语漂移。
2. 分块合并错乱，章节或段落顺序断裂。
3. 初译以后没有中文-only 编辑，保留 GPT 腔和重复连接词。
4. 只扫禁词，不判断句子功能。
5. 只做局部流畅，忘了整卷情绪线。

## 推荐目录
```text
project/
  source/
  translations/
  meta/
    source_inventory.json
    context_pack.md
    series_bible.md
    style_guide.zh-CN.md
    glossary.csv
    continuity_notes.md
    open_issues.md
  qa/
  work/
```

## 文件顺序
- 优先按文件名中的卷号、章号、话数排序。
- 不要让系统默认按字典序把 `第10话` 放到 `第2话` 前。
- 生成 inventory 后再开始翻译。

## 分块原则
- 以场景、自然段、对话交换、心理段落为单位。
- 不要拆开笑点和 punchline。
- 不要拆开告白/拒绝/冲突的前后反应。
- 不要拆开动作和动作结果。
- 每块带：上一块摘要、本章摘要、活跃角色、相关 glossary、未决问题。

## 合并原则
- 合并时按 chunk ID 排序。
- 合并后通读章节，重点看转场处有没有“突然换场”“信息断裂”“重复段”。
- 如果译文出现不连贯，先怀疑 chunk 顺序、漏段、重复段，而不是只润色句子。

## 章节 QA 模板
```md
# QA - <chapter>

## 完整性
- 原文标题：
- 译文标题：
- 段落/场景顺序：ok / issue
- 漏译/重复风险：none / listed below

## 准确性风险
| severity | source location | issue | fix |
|---|---|---|---|

## 称呼与术语
| item | decision | note |
|---|---|---|

## 反 GPT 腔处理
| hit | context | action |
|---|---|---|

## 连接词与节奏
- 段首重复词：
- 删除/弱化的转折词：
- 保留的关键转折词与理由：

## 连续性备注
- 

## 未决问题
- 
```

## 整卷 QA 模板
```md
# Volume Consistency Report

## Critical

## Major

## Minor

## Names and Addresses

## Glossary Drift

## Character Voice Drift

## Relationship and Timeline

## High-Risk Translationese Scan

## Connective / Rhythm Overuse

## Final Release Decision
ready / needs focused repair / needs retranslation
```
