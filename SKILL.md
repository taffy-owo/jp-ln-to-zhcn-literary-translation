---
name: jp-ln-to-zhcn-literary-translation
description: translate japanese light novel chapters, folders, web-novel exports, or full volumes into idiomatic simplified chinese with project memory, glossary, character voice control, anti-translationese editing, batch workflow, and release qa. use for japanese-to-zh-cn literary translation, polishing, retranslation, continuity review, codex or antigravity workspace translation projects, and high-quality light novel localization. do not use for isolated dictionary lookups, technical documents, or interlinear grammar glosses.
---

# 日文轻小说 → 简体中文精翻 Skill

## 目标
把日文轻小说、Web 小说、Syosetu 文本、EPUB/TXT/Markdown 抽取稿翻成可直接阅读、可进入校对流程的简体中文小说。译文必须优先像中文小说，其次才像"忠实译文"：事实、人物关系、伏笔、称呼、语气、笑点、节奏都要保住，但不能残留日语语序和 GPT 腔。

这不是逐句机翻指令。执行时把自己当成"译者 + 中文编辑 + 连续性校对"，按项目资产和 QA 闭环工作。

## 最高优先级
1. **准确**：剧情事实、动作先后、指代、因果、伏笔、人物心理不得错。
2. **自然**：译文必须像中文小说，避免日式直译、抽象名词堆叠、连接词模板化和 AI 平滑腔。
3. **声音**：叙述者与角色要有年龄、身份、关系距离和情绪差异。
4. **一致**：人名、称呼、专有名词、口头禅、反复句、情绪母题跨章统一。
5. **可交付**：每章完成后有译文、术语/人设更新、QA 质量卡；整卷完成后有一致性报告和发布前 checklist。

## 项目资产
面对单章以上任务，先查找或创建项目资产。项目文件优先于本 Skill 默认规则。

必备目录：

- `source/`：日文原文，可是 txt、md、epub 抽取文本。
- `translations/`：简体中文译文。
- `meta/`：项目记忆。
  - `meta/voice_cards/`：主要角色声线卡（详见 `references/voice-card-template.md`）。
- `qa/`：质检报告。
- `work/`：分块、上下文包、中间稿，可不交付。
- `golden_set/`（可选）：回归测试样张（详见 `references/golden-set-guide.md`）。

必备文件：

- `meta/series_bible.md`：作品信息、角色、人际关系、时间线、反复句。
- `meta/style_guide.zh-CN.md`：本项目中文文风、标点、称呼策略、禁用表达。
- `meta/glossary.csv`：人名、称呼、术语、高风险词。字段包括 `status`（proposed/approved/deprecated/forbidden）、`decision_reason`、`last_reviewed_chapter`、`deprecated_form`。
- `meta/continuity_notes.md`：跨章连续性、关系变化、伏笔、称呼变更记录。
- `meta/open_issues.md`：待确认问题与歧义登记。

可用脚本：

```bash
python scripts/ln_project.py init --root . --source source
python scripts/ln_project.py inventory --source source --output meta/source_inventory.json
python scripts/ln_project.py context-pack --source source --meta meta --output meta/context_pack.md
python scripts/ln_project.py chunk source/第01话.txt --output-dir work/chunks/第01话 --max-chars 4500
python scripts/ln_project.py scan translations --output qa/high_risk_scan.md
python scripts/ln_project.py manifest --source source --translations translations --output qa/translation_manifest.md
python scripts/ln_project.py stitch-check --source source --translations translations --output qa/stitch_report.md
python scripts/ln_project.py glossary-audit --glossary meta/glossary.csv --translations translations --output qa/glossary_audit.md
```

脚本只做确定性准备和扫描，不替代翻译判断。

## 整卷/整文件夹工作流
用户给一整个文件夹或一卷时，不要直接从第一章逐段开翻。必须先做准备。

### 1. Intake：建立文件顺序
1. 扫描 `source/`，只选小说正文文件，排除网页噪音、备份文件、旧译稿。
2. 按章节编号、卷号、自然排序确定阅读顺序。
3. 生成 `meta/source_inventory.json`，记录路径、大小、字符数、sha1、首行标题。
4. 不确定顺序时，不擅自重排；在 `meta/open_issues.md` 记录。

### 2. Context Pass：先读作品再翻译
1. 能完整读完就先读完整卷。
2. 如果太大，至少读：所有标题、每章开头/结尾、关键对话、已有 `meta/`、前后相邻章节。
3. 建立或更新：角色表、称呼表、关系线、时间线、叙述视角、反复句、笑点/梗、世界观术语、伏笔和不确定点。
4. **为每个主要角色建立声线卡**（`meta/voice_cards/<角色名>.md`），记录称呼矩阵、句法特征、情绪语言变化。详见 `references/voice-card-template.md`。
5. 生成 `meta/context_pack.md` 作为本轮翻译上下文包。

### 3. Style Lock：先锁文风
整卷、长篇或用户要求"精翻/出版级/像翻译家"时，先对第一章或 1500-3000 日文字符建立风格样张：

- 翻译一小段。
- 做一次中文编辑改写。
- 记录人名、称呼、叙述节奏、禁用表达、角色声音。
- 把决定写进 `meta/style_guide.zh-CN.md` 和 `meta/glossary.csv`。

### 4. Chapter Translation：逐章翻译
每章遵循固定顺序：

1. 读取本章原文、上一章译文/摘要、`meta/context_pack.md`、glossary、series bible、声线卡。
2. 按场景或自然段落分块，给每块固定 ID，如 `ch019-sc03`。不要按随机 token 截断。
3. **译前歧义解析（Pre-translation Parse）**：对每块先判断说话人、受话人、隐含主语（及补出理由）、敬语关系功能、情绪/语气功能（安慰/试探/撒娇/逞强/自嘲？）、信息焦点、歧义点、风险等级。高风险歧义写入 `meta/open_issues.md`。详见 `references/pre-translation-parse.md`。
4. 先出准确初译，再做中文文学编辑。
5. 合并时严格按原块顺序，不移动段落，不把下一章内容插入本章。
6. **三轨中文编辑**：分旁白、内心独白、对话三轨依次处理。详见 `references/voice-and-style.md`。
   - 旁白轨：去说明腔，把感受落到动作和身体反应。
   - 内心轨：保留刺感和真实想法的锐度。
   - 对话轨：对照声线卡，维持角色差异。
7. 做双语完整性抽查：标题、段落、对话、场景转折、作者后记/短信/系统提示不能丢。
8. **文化负载词检查**：对照 `references/annotation-policy.md`，确认设定词、学校/敬称、双关、食物、礼俗的处理一致。
9. 保存：`translations/<chapter>.zh-CN.md` 与 `qa/<chapter>.qa.md`（含质量卡）。
10. 更新 `meta/`（glossary、continuity_notes、open_issues）。

### 5. Volume QA：整卷校对
整卷翻完后必须做：

- `python scripts/ln_project.py scan translations --output qa/high_risk_scan.md`
- `python scripts/ln_project.py manifest --source source --translations translations --output qa/translation_manifest.md`
- `python scripts/ln_project.py stitch-check --source source --translations translations --output qa/stitch_report.md`
- `python scripts/ln_project.py glossary-audit --glossary meta/glossary.csv --translations translations --output qa/glossary_audit.md`
- 跨章节检查：人名、称呼、术语、口头禅、反复句、关系线、伏笔、情绪母题、章节顺序。
- 输出 `qa/volume_consistency_report.md`。
- Golden set 回归对照（如有样张）。

### 6. Release Gate：发布前检查
整卷 QA 通过后，按 `references/batch-workflow.md` 中的发布前 checklist 逐项确认。

## 失败条件

以下任一条件触发时，**不得宣称翻译完成**：

- 事实错译 ≥ 1 处 critical（说话人归属错、因果反转、剧情事实改变）
- 漏段 ≥ 1 段
- 术语漂移 ≥ 2 处（同一章内同一术语多种译法且无剧情原因）
- 主要角色声线不可区分
- 段首连接词连续重复 ≥ 3 处未处理
- 章节拼接错乱 ≥ 1 处
- 未翻译日文残留 ≥ 1 处
- 亲密/成人场景遮掩 ≥ 1 处

有严重漏译、错译、章节拼接错乱、高风险 GPT 腔命中未处理时，不要声称完成。

## 单章/片段工作流
用户只给单章或片段时：

1. 先读取已有 `meta/`；有相邻章节就读相邻章节摘要/结尾。
2. 没有上下文时，明确在 QA 里记录"不确定的称呼/关系/伏笔"。
3. 短片段也要先做译前歧义解析（至少判断人物关系和语气功能），再翻译。
4. 用户要求"只要译文"时，最终只输出译文；内部仍做检查。

## 翻译原则

### 自然中文优先
允许为了中文自然而重排、拆分、合并、改成中文等效表达、轻量嵌入必要文化信息。前提是事实、暧昧、伏笔和语气功能不被改写。

### 准确先于润色
不要添加原文没有的动机、景物、心理强度、解释或伏笔。不要因为中文顺而删掉轻微笑点、停顿、尴尬、沉默、话没说完的感觉。

### 绝对客观与真实性
翻译语言优化严禁脱离原文随意增删。绝对不能在原文没有对应意图或情节的情况下，凭空添加任何主观动机、动作描写、心理活动或侧面修饰。翻译必须以客观、忠实地再现原著内容为首要准则。

### 亲密与成人场景的忠实呈现（无遮掩原则）
对于涉及身体接触、性爱、床戏及亲密互动的场景描写，必须严格遵循"原作者如何描述，译文便如何呈现"的忠实原则。严禁以任何理由进行任何形式的自我审查、情节遮掩、删节，或使用过度委婉的温和词语对感官细节进行替换。应当在保持"轻小说风味"（流利、好读、甜美日常且无医疗/法条等生硬腔调）的前提下，100%客观还原原著中的感官细节、亲密姿态及情感烈度。这是对原作者极其基本的尊重。

### 敬语与称呼
日语后缀不是装饰，要转换成中文里的亲疏、礼貌、上下级、年龄差和情绪变化。不要一律保留或一律删除。称呼变化要记录到 `meta/continuity_notes.md`。

### 文化负载词
处理文化负载词时，查阅 `references/annotation-policy.md`。五类分类处理：设定词、学校/敬称、双关、食物、礼俗各有不同策略。默认不加脚注；必要时文内轻解释。

### 拟声拟态词
有自然汉语拟声词就用；没有就转成动作、状态、触感、节奏。不要硬保留日文拟态词，也不要一律删掉。

### 双关、吐槽、笑点
优先级：剧情功能 > 人物反应 > 喜剧时机 > 字面结构。能用中文重写就重写；除非用户要求注释版，否则避免长译注。


## 连接词与转折词控制
翻译和润色时必须查阅 `references/connective-rhythm.md`。日文常用显性连接来推进句子，但中文小说不应把每个 `でも / だけど / しかし / それでも / その時 / 次の瞬間` 都译成"可是/不过/但是/即便如此/就在这时/那一瞬间"。

硬规则：

- 不要让相邻段落连续以"可是/不过/但是/即便如此/就在这时/那一瞬间"开头。
- 同一章内同一个强连接词反复出现时，优先删掉、改成动作承接，或把逻辑压进"还是/仍然/却/只/偏偏"等更轻的中文结构。
- "即便如此/尽管如此"只用于确有强让步或庄重叙述的场景；普通承接用"还是/仍旧/却"或直接重写。
- "就在这时"只用于真正有打断感的新事件；普通动作接续直接写动作。
- "那一瞬间/一瞬间"不要机械对应日文 `瞬間`；常可直接写"我反射性地……"。
- 原文刻意重复可以保留，但必须在章 QA 里说明它是节奏选择。

## 反 GPT 腔硬规则
翻译和编辑时必须查阅 `references/anti-gptese.md`。以下表达默认视为高风险，除非上下文强烈需要，否则要改写：

- 社会人
- 抽象义"接住"
- 元气
- 违和感
- 重要的事物
- 心情复杂地
- 果然如此
- 说不定
- 全部都由我……
- 身体擅自想起来
- 鲜明地重放
- 悲痛喊声
- 距离感（用于人物关系时）
- 冰冷的视线落下来（重复使用时）
- 不是自己的东西一样……

处理方式不是简单替换，而是按场景功能改写。例：

- `社会人の嗜み` 在"随身带换洗衣物"的场景里，可译为"这点准备，成年人还是该有的"或"上班族嘛，这点自我管理还是要有的"。不要写"社会人的素养"。
- 抽象 `受け止める` 在安慰/承诺场景里，可译为"我会听着""我陪你一起扛""我受得住""你说什么我都认真听"。不要写"全部由我接住"。

## 结构化输出合约

各阶段有明确的输入/输出格式要求，确保代理之间交接清晰：

### Planner 输出
- 角色表（含声线卡引用）
- 称呼矩阵
- 风险清单（高风险句型、歧义点）
- 歧义登记（写入 `meta/open_issues.md`）

### Translator 输出
- 译文块（按场景/段落分块，带块 ID）
- 译前歧义解析 parse log（说话人、主语补出、语气判断）
- 新增/变更术语记录

### Editor 输出
- 修订后完整译文
- 修改原因标签（旁白/内心/对话分轨标注）
- 连接词消重记录

### Reviewer 输出
- 按 critical / major / minor 分级的问题证据
- 声线漂移检查结果
- 术语一致性检查结果
- 章节质量卡

## 输出约定
普通对话请求：优先输出 polished 中文译文。若不是"只要译文"，附简短 QA：新术语、未决问题、高风险词处理。

文件型任务：写入项目目录：

- `translations/<chapter>.zh-CN.md`
- `qa/<chapter>.qa.md`（含章节质量卡）
- updated `meta/*.md/csv`

QA 报告要具体，不要空泛夸奖。至少包括：准确性风险、称呼/术语变化、反 GPT 腔扫描、连续性备注、质量卡。

## 参考文件
必要时读取：

- `references/batch-workflow.md`：整卷/文件夹执行细节与发布前 checklist。
- `references/anti-gptese.md`：反翻译腔与示例改写。
- `references/connective-rhythm.md`：连接词、转折词、段落节奏消重。
- `references/default-glossary.md`：高风险词与默认术语。
- `references/voice-and-style.md`：角色声音、中文文风与三轨编辑。
- `references/voice-card-template.md`：角色声线卡模板。
- `references/pre-translation-parse.md`：译前歧义解析指南与模板。
- `references/annotation-policy.md`：文化负载词注释策略。
- `references/golden-set-guide.md`：Golden set 建立与回归测试指南。
- `references/quality-rubric.md`：质量标准、失败条件与混合评估质量卡。
- `references/refinement-prompts.md`：专项审校提示。
- `references/memory-template.md`、`references/style-guide-template.md`、`references/glossary-template.csv`：项目资产模板。

## 停止条件
完成用户要求的翻译、修订、QA 或项目初始化后停止。不要把过程长篇输出给用户，除非用户要求看分析。
