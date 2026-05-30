---
name: jp-light-novel-translate
description: Specialized Japanese light novel and Syosetu/Web novel translation workflow from Japanese to Simplified Chinese. Use when translating Japanese fiction chapters, web novels, light novels, manga-adjacent prose, character dialogue, honorific-heavy scenes, isekai/fantasy/romcom/battle academy/R18-adjacent novel text, or when the user asks for 日轻翻译, 轻小说精翻, Web小说翻译, Syosetu翻译, 角色语气一致, 术语表/glossary, 多章连载翻译, or publication-quality Chinese novel localization.
---

# JP Light Novel Translate

Translate Japanese light novels into polished Simplified Chinese with high priority on accuracy, character voice, reading rhythm, and cross-chapter consistency. Treat this as faithful human translation with a controlled memory system, not sentence-by-sentence machine translation.

## Quality Target

Aim for "正版轻小说中文译稿初校后质量": faithful events and facts, natural Chinese prose, distinct character voices, stable terminology, minimal translationese, and no unauthorized plot embellishment.

Do not promise perfect translation. For top quality, require a glossary/character memory and iterative review for long works.

## Execution Model

This skill is for Codex to perform the translation work directly, guided by source text, project memory, and review passes. Bundled scripts may be used only for deterministic file operations such as chunking and EPUB/project assembly.

If a whole book is too large to finish in one turn, work incrementally: translate chapters in order, save each completed chapter, rebuild the EPUB with completed chapters, and record progress. Do not generate fake completion or low-quality automated filler.

## Operating Modes

- `quick`: Translate directly. Use only for short snippets, examples, or rough comprehension.
- `normal`: Analyze context, update memory, translate, and self-check. Use by default for ordinary chapters.
- `refined`: Analyze, translate, critique, revise, polish, and produce notes. Use for important chapters, public release, or when the user says 精翻, 顶级质量, 出版级, or 完美.

If the user does not specify a mode, choose `refined` for fiction longer than 1,500 Japanese characters and `normal` for shorter text.

## Required Context Handling

Before translating a work or chapter, look for these files near the source, then in the project root:

- `glossary.md`
- `characters.md`
- `style-guide.md`
- `translation-memory.md`

If they exist, read them first and follow them. If they do not exist, infer a lightweight memory during translation and suggest saving one after the result. Do not block the user unless consistency across many chapters is explicitly required.

Use the templates in:

- `references/memory-template.md` when creating or updating memory files.
- `references/voice-and-style.md` when analyzing dialogue, honorifics, narration, comedy, innuendo, or R18-adjacent scenes.
- `references/quality-rubric.md` for refined-mode critique and final checks.
- `references/default-glossary.md` for built-in JP -> ZH light novel terms when no project glossary overrides them.

## Bundled Long-Form Tools

For long Markdown chapters, use the bundled chunker before translation when the file is too large to translate safely in one pass:

```bash
npx -y bun C:\Users\adm\.codex\skills\jp-light-novel-translate\scripts\main.ts chapter.md --max-words 3500 --output-dir chapter-zh-CN
```

The chunker preserves Markdown block boundaries and writes `chunks/chunk-NN.md` files. Translate chunks in order using the same analysis, glossary, and character memory, then merge them before refined review.

## Workflow

### 1. Source Preparation

Preserve paragraph order, dialogue boundaries, scene breaks, ruby/furigana hints, emphasis, and author notes unless the user asks otherwise.

For long chapters, split by scene or paragraph groups, not by arbitrary token count. Keep the previous and next scene summaries available while translating each chunk.

If the source is a Markdown file and needs chunking, prefer `scripts/main.ts` with `--max-words 3500`. If a scene break is obvious, keep scenes together even when a chunk could be smaller.

For multi-chapter projects, maintain these invariants:

- Names, titles, abilities, organizations, locations, and item names must not drift.
- Character speech habits must remain stable unless the plot changes them.
- Important foreshadowing, ambiguity, and unreliable narration must stay ambiguous.

### 2. Analysis

For `normal` and `refined`, identify:

- Genre and register: isekai, romcom, fantasy, school, battle, slice of life, suspense, adult, parody.
- Narrative POV: first person, third person, inner monologue, unreliable narrator.
- Character voices: age, social role, politeness,口癖, emotional baseline, relationship distance.
- Translation risks: honorifics, jokes, puns, idioms, dialect, otaku terms, erotic euphemisms, game UI terms, magic/system terms.
- New glossary candidates.

Keep this analysis concise unless the user asks to see it.

Load `references/default-glossary.md` during analysis and merge it after the user's project glossary. Project glossary choices always win.

### Localization / 汉化 Rules

Use localization to preserve the original reading experience, not to rewrite the work.

- Build and obey two memories: `glossary.md` for fixed names/terms/catchphrases, and `style-guide.md` for prose rhythm, dialogue distance, genre feel, and punctuation choices.
- Translate idioms, metaphors, jokes, and stock phrases by function and tone. Use natural Chinese equivalents when they carry the same scene effect; keep Japanese cultural texture when the setting, relationship, or later plot depends on it.
- Treat honorifics, first-person pronouns, and sentence endings as relationship data. Encode them through Chinese address forms, directness, sentence length, and politeness level; do not simply keep or delete every suffix.
- Preserve ambiguity, foreshadowing, unreliable narration, and delayed reveals. Natural Chinese must not resolve what the Japanese intentionally leaves open.
- Use translator notes sparingly. Prefer translating the meaning in-body; add notes only for unavoidable wordplay, culturally necessary context, or a term whose surface form matters later.
- Do a separate editor pass after drafting: fix grammar, repeated calques, inconsistent terms, voice drift, paragraph rhythm, and formatting. A readable first draft is not the final translation.
### 3. Translation Rules

Translate meaning, intent, and reading experience. Avoid Japanese word order in Chinese.

Objectivity and fidelity:

- Do not add information, explanations, emotions, motivations, scene details, or foreshadowing that are not present in the source.
- Do not intensify or soften a character's emotion beyond the source wording.
- Do not replace ambiguity with interpretation. Preserve uncertainty, hesitation, and omissions.
- Do not add translator commentary inside the 正文 unless the user explicitly asks for notes.
- Natural Chinese is required, but naturalness must serve accuracy, not rewrite the scene.

Dialogue:

- Make each speaker sound like a specific person.
- Preserve politeness level and relationship distance through Chinese wording, not mechanical suffixes.
- Keep catchphrases recognizable but not awkward.
- Do not flatten tsundere, shy, arrogant, childish, formal, archaic, or deadpan voices into the same neutral tone.

Narration:

- Use natural Chinese novel prose.
- Keep light novel pacing: short punchy sentences can stay punchy; emotional beats should breathe.
- Do not over-literarize simple Syosetu prose.
- Prefer clean, direct Chinese light-novel rhythm over visibly translated phrasing. Use culturally natural Chinese wording when it preserves the source facts and scene meaning.
- Remove forum noise, website UI text, comments, ratings, signatures, and reply metadata when source material is copied from forums or web pages.

Honorifics:

- Translate flexibly. Use "前辈", "老师", "同学", "小姐", "大人", name-only, or omitted forms based on relationship and scene.
- Preserve Japanese suffixes only when the work's style or fandom convention clearly benefits from it.
- Explain unusual choices only in a short translator note.

Onomatopoeia and mimetics:

- Render by effect, not spelling. Use natural Chinese sound words, action description, or rhythm depending on the scene.
- Do not leave long strings like "咚咚咚咚" unless the visual rhythm matters.

Terms and names:

- Use existing glossary first.
- If no glossary exists, choose stable, readable Chinese names and record candidates.
- Keep Japanese names in common Chinese transliteration unless the user prefers original kanji or romaji.
- Preserve chosen name glyphs exactly. Do not substitute similar-looking variants or simplified forms for Japanese personal-name kanji when the project glossary fixes them.

Sensitive or adult content:

- Translate faithfully without moralizing, euphemizing into nonsense, or becoming gratuitously explicit.
- Preserve consent cues, speaker intent, and power dynamics accurately.

### 4. Refined Mode

Use this sequence:

1. Draft a faithful, readable translation.
2. Critique the draft against `references/quality-rubric.md`.
3. Revise concrete problems: mistranslation, unauthorized additions, voice drift, stiff Chinese, lost jokes, inconsistent terms, rhythm issues.
4. Polish only after accuracy is fixed.
5. Provide final text first. Add concise notes only when useful.

In critique, do not praise. List actionable defects and fix them.

## Learning From Each Translation

When the user corrects the translation process or a recurring issue appears, update the relevant project memory files and, when broadly reusable, this skill:

- Add term decisions to `glossary.md` or `references/default-glossary.md`.
- Add character voice decisions to `characters.md`.
- Add style/process corrections to `style-guide.md` or this SKILL.md.
- Add unresolved choices to `translation-memory.md`.

Keep updates concise and operational. Do not add general advice that does not change future translation behavior.

### 5. Output

For ordinary requests, output only the translated Chinese text.

For file-based or long-chapter work, save outputs beside the source when feasible:

- `translation.md`: final translation
- `translation-notes.md`: glossary updates, unresolved choices, optional translator notes

If the user asks for a reusable project workflow, create or update:

- `glossary.md`
- `characters.md`
- `style-guide.md`
- `translation-memory.md`

End with a short status summary including mode, files touched, and any unresolved glossary choices.

## Stop Conditions

Stop once the translation or requested setup is complete and validation/review has enough evidence. Do not keep expanding the workflow, adding unrelated tools, or rewriting the skill unless the user asks.

## Long-Form Final Polish Lessons

For full-book Japanese light novel polishing after translation, run an editorial pass after accuracy review. The goal is not rewriting the story, but removing AI/translation texture while preserving facts, ambiguity, and character intent.

- Repetition control: audit high-frequency filler such as "胸口深处", "稍微", "像是", "不由得", "视线", "轻轻", "某种", and repeated sentence frames. Replace only where the sentence remains faithful; do not vary fixed terms or emotional anchors mechanically.
- Chinese prose rhythm: shorten over-explained sentences, reduce duplicated emotional predicates, and prefer direct Chinese phrasing when Japanese connective structure leaks into the translation.
- Dialogue naturalness: make spoken lines sound like the speaker would say them in Chinese. Keep grief, hesitation, and politeness, but remove stiff calques such as overusing "这样说着", "那样的", or formal connective phrasing in casual speech.
- Emotional density: for grief-heavy works, do not intensify beyond the source. When several adjacent sentences repeat the same pain image, keep the strongest one and make the others quieter or more concrete.
- Character boundaries: when a plot intentionally blurs identities or memories, preserve the confusion but keep names and pronouns exact. Do not explain the trick before the source does.
- Contextual term rendering: do not translate `社会人` literally as "社会人" in Chinese prose. Choose by context: "上班族", "职场人", "成年人", "工作以后的人", "出来工作的人", or rewrite the sentence naturally when the point is maturity, preparedness, or adult responsibility.
- Contextual emotion verbs: do not mechanically translate `受け止める` as "接住" unless a physical catching image is intended. For emotional or conversational use, choose by context: "承受", "包容", "听进去", "认真听完", "消化", "面对", "分担", "陪你一起扛", etc. Preserve the emotional function instead of the dictionary surface.
- Final EPUB QA: check chapter count, title duplication, banned glyphs/noise, name glyph stability, and EPUB structure after rebuilding. Treat clean mechanical checks as necessary but not sufficient; still sample key emotional chapters by eye.
