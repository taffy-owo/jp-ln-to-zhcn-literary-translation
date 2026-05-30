# Focused Refinement Prompts

Use these as focused review passes. Do not run all of them when the task only needs a narrow fix.

## Fact Audit Only

```text
请只检查这一章的高风险准确性问题，不要润色文风。
重点检查：
- 说话人是否判断错误
- 指代链是否断裂
- 时间顺序、动作先后、因果是否错
- 是否有漏译、反译、过译
输出：按“严重 / 重要 / 次要”三档列出问题，并给出最小修改方案。
```

## Translationese Removal Only

```text
请把本章当成中文轻小说来通读，只处理“像翻译稿”的地方，不改变剧情事实。
重点处理：
- 日语语序残留
- 僵硬抽象名词
- 机械副词堆叠
- 不自然的书面套话
- 角色说话不像中国读者能自然读下去的中文
输出：直接给出修订后的文本。
```

## Character Voice Only

```text
请只检查【角色名】在本章里的说话方式是否稳定。
关注：
- 年龄感
- 礼貌层级
- 冷淡/活泼/毒舌/软弱等气质
- 对不同对象的称呼是否一致
- 是否被写成了“任何角色都能说的话”
输出：列出有问题的句子，并给出更贴合该角色的改写。
```

## High-Risk Phrase Check Only

```text
请只检查以下高风险翻译腔是否出现，并判断是否误用：
- 社会人
- 接住（抽象义）
- 违和感
- 元气
- 重要的事物
- 果然如此
- 说不定
- 心情复杂地
如命中，请给出更自然的 zh-CN 改写。
```

## Cross-Volume Continuity Regression

```text
请对比当前卷与上一卷的 glossary、series_bible、continuity_notes 和实际译文，找出：
- 人名/称呼漂移
- 角色口头禅漂移
- 固定梗或反复句漂移
- 世界观术语口径变化
- 关系线前后不一致
输出：只列重大问题与建议统一方案。
```