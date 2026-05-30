# 日文轻小说整卷翻译工作流

使用技能：`jp-ln-to-zhcn-literary-translation`

## 输入约定
- 源文件目录：`./source/`
- 中文输出目录：`./translations/`
- 元数据目录：`./meta/`
- QA 目录：`./qa/`

## 目标
把 `./source/` 下按顺序排列的整卷日文轻小说翻译为高质量简体中文，并同步维护术语、风格、连续性资产。

## 执行步骤

### 准备阶段
- 扫描并排序 source 文件。
- 读取已有 meta 文件。
- 若缺失则创建 `series_bible.md`、`style_guide.zh-CN.md`、`glossary.csv`、`continuity_notes.md`、`open_issues.md`。

### 通读阶段
- 先通读整卷或尽可能多的章节。
- 生成全卷概要、角色关系表、叙事视角说明、初始 style guide、初始 glossary。

### 翻译阶段
对每一章重复以下步骤：
1. 读取前章摘要与本章原文。
2. 按场景切块。
3. 完成初译。
4. 完成文学化润色。
5. 全章中文通读。
6. 更新 glossary / continuity notes / open issues。
7. 写入 `translations/<chapter>.zh-CN.md` 与 `qa/<chapter>.qa.md`。

### 全卷审核阶段
- 运行跨章节 consistency review。
- 检查术语漂移、称呼漂移、人设漂移、笑点丢失、翻译腔复发。
- 输出 `qa/volume_consistency_report.md`。

## 结束条件
只有满足以下条件才算完成：
- 全章均有中文稿。
- glossary 与 style guide 已更新。
- volume consistency report 已生成。
- open issues 只剩低风险项，或均已明确记录。