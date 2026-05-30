---
name: jp-ln-to-zhcn-literary-translation
description: Translates Japanese light novel chapters, folders, or whole volumes into idiomatic simplified Chinese with context-aware preprocessing, glossary generation, style control, and continuity QA. Use for full-project literary translation or revision.
---

# 日本轻小说译为简体中文技能

## 目标
将日文轻小说翻译为自然、流畅、具有文学感的简体中文，并保持剧情、人物声音、称呼系统、术语系统和跨章连续性稳定。

## 触发条件
以下情况应优先使用本技能：
- 用户提供整卷、整文件夹、多个章节文件
- 任务是端到端翻译、续翻、修订、统一术语、做 QA
- 任务需要整章或整卷上下文

以下情况不要使用本技能：
- 只查一个词
- 只做逐句对照
- 文档不是叙事文本

## 预处理
1. 扫描项目并确定源文件顺序。
2. 检查并创建 `meta/series_bible.md`、`meta/style_guide.zh-CN.md`、`meta/glossary.csv`、`meta/continuity_notes.md`、`meta/open_issues.md`。
3. 尽可能先读完整卷；若太长，则先读全部标题、每章开头与结尾、现有 meta 资产。
4. 提取并记录人物表、称呼表、叙事视角、角色口头禅、世界观术语、未决歧义。

## 切块规则
- 优先按场景、对话段、内心独白段切分。
- 不在笑点、告白、转折句中间切块。
- 每块都带滚动上下文包：上一块摘要、当前章摘要、活跃角色 voice notes、相关 glossary、未决问题清单。

## 翻译规则
- 保证事实准确，但中文表达必须自然。
- 允许重组句法，不允许篡改信息。
- 敬语要译出社会意义，不机械保留形式。
- 拟声拟态词：有自然汉语对应则可直用；无则译 effect，不硬造生僻声响词。
- 双关和笑点：先保剧情功能，再保反应与喜剧时机，最后尽量保形式。
- 文化负载词：已读者熟悉者直接自然处理；不熟且影响理解者做轻量嵌入解释；非必要不用长注。

## 每章完成后的动作
1. 通读中文稿，删除翻译腔。
2. 检查人名、称呼、术语、口头禅、引号和段落、指代恢复。
3. 更新 meta 资产。
4. 生成 `qa/<chapter>.qa.md`。

## 每卷完成后的动作
1. 做跨章节 consistency pass。
2. 比对角色称呼变化、世界观术语、重复笑点与反复句、情绪线与关系线。
3. 生成 `qa/volume_consistency_report.md`。

## 输出
默认输出章节译文、新增 glossary 项、未决歧义、QA 摘要。若用户要求“仅输出译文”，则只输出润色后的最终译文。