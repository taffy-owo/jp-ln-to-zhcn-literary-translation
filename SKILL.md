---
name: jp-ln-to-zhcn-literary-translation
description: Translate Japanese light novel chapters, folders, or full volumes into idiomatic Simplified Chinese with full-context pre-reading, project memory assets, glossary management, character-voice preservation, literary editing, and cross-volume QA. Use for end-to-end narrative translation, revision, polishing, terminology unification, or continuity review. Do not use for isolated dictionary lookups, technical documents, or interlinear glosses.
---

# Japanese Light Novel to zh-CN Literary Translation Skill

## Goal
Produce high-quality Simplified Chinese translations of Japanese light novels and Syosetu/Web novels. The translation must read like publishable Chinese fiction while preserving plot facts, tone, pacing, character voice, humor, subtext, relationship distance, and cross-chapter continuity.

This skill is not a sentence-by-sentence machine translation recipe. Treat translation as four layers: system/project constraints, this workflow, persistent project assets, and release QA.

## Use This Skill
Use this skill when:

- the user provides a chapter, chapter folder, EPUB/TXT/Markdown source, whole volume, or long narrative file
- the task is end-to-end translation, 续翻, revision, polishing, glossary building, style-guide creation, or continuity QA
- the task requires chapter-level or volume-level context
- the user asks for 日轻翻译, 轻小说精翻, Web小说翻译, Syosetu翻译, 汉化, 角色语气一致, 术语表, or publication-quality Chinese localization

Do not use this skill when:

- the user only wants a dictionary definition
- the user wants a literal crib, line-by-line gloss, or grammar explanation
- the source is not narrative prose

## Required Project Assets
Before translating a project, look for `meta/` near the source. If assets do not exist and the task is longer than a short excerpt, create or update:

- `meta/series_bible.md`
- `meta/style_guide.zh-CN.md`
- `meta/glossary.csv`
- `meta/continuity_notes.md`
- `meta/open_issues.md`

Use bundled references when creating or updating them:

- `references/memory-template.md` for project asset templates
- `references/style-guide-template.md` for `style_guide.zh-CN.md`
- `references/glossary-template.csv` for `glossary.csv`
- `references/default-glossary.md` for fallback high-risk terms and genre terms
- `references/voice-and-style.md` for character voice, honorifics, jokes, culture-loaded terms, and prose style
- `references/quality-rubric.md` for MQM-style review and release gates
- `references/refinement-prompts.md` for focused review passes

Project assets override bundled defaults. If project decisions conflict with defaults, obey the project files and update the relevant note when the change is intentional.

## Core Workflow

### 1. Intake
1. Locate source files and sort them in canonical reading order.
2. Detect source type: TXT, Markdown, EPUB-extracted text, DOCX-extracted text, or pasted chapter.
3. Preserve source paragraph order, dialogue boundaries, scene breaks, author notes, ruby/furigana meaning, and emphasis unless the user asks otherwise.
4. Remove web/forum noise only when it is clearly not part of the work: UI text, ratings, reply metadata, signatures, duplicated navigation, and scraped comments.

### 2. Full-Context Reading
1. Read the entire volume if feasible.
2. If the volume is too large, read all chapter titles, the beginning and ending of each chapter, existing summaries, and all `meta/` assets.
3. Build an internal map of characters, relationships, naming/address conventions, POV, recurring phrases, catchphrases, jokes, motifs, world-building terms, unresolved ambiguities, foreshadowing, and delayed reveals.

### 3. Chunking
Chunk by scene or natural discourse boundary, not by arbitrary token count.

Preferred chunk units:

- one short scene
- one dialogue exchange cluster
- one coherent introspection segment

Avoid splitting punchlines, confessions, action beats and consequences, setup/payoff pairs, or honorific/register-sensitive exchanges.

Maintain a rolling context packet for each chunk: previous chunk summary, current chapter summary, relevant glossary entries, voice notes for active speakers, and unresolved issues.

For long Markdown chapters, the bundled chunker may be used only for deterministic splitting; translation still follows scene-aware review:

```bash
npx -y bun C:\Users\adm\.codex\skills\jp-ln-to-zhcn-literary-translation\scripts\main.ts chapter.md --max-words 3500 --output-dir chapter-zh-CN
```

### 4. Translation Pass
For each chunk:

1. Determine speaker, addressee, emotional direction, register, and relationship distance.
2. Identify risky items: honorifics, first-person pronouns, sentence endings, culture-specific terms, onomatopoeia/mimetics, puns, jokes, ellipsis, omitted subjects, ambiguous pronouns, and high-risk calques.
3. Draft the translation in natural zh-CN.
4. Rewrite the draft for rhythm, readability, and character voice.
5. Verify consistency against project assets.
6. Save the final chunk into the chapter output when doing file-based work.

### 5. Chapter-Level Review
After every chapter:

1. Re-read the chapter as Chinese prose only.
2. Remove translationese and awkward carryover from Japanese syntax.
3. Check names, forms of address, tense/aspect interpretation, restored omitted subjects, paragraphing, dialogue punctuation, repeated terms, repeated metaphors, and voice drift.
4. Update `meta/glossary.csv`, `meta/series_bible.md`, `meta/continuity_notes.md`, and `meta/open_issues.md`.
5. Create `qa/<chapter>.qa.md` when doing file-based work.

### 6. Volume-Level Review
After the volume is complete:

1. Run a cross-chapter consistency pass.
2. Compare first appearances and later uses of character names, nicknames, kinship terms, address forms, school/job labels, recurring jokes, recurring emotional metaphors, and world-building terms.
3. Produce `qa/volume_consistency_report.md`.
4. Treat open issues as unfinished work unless they are low-risk and explicitly recorded.

## Hard Translation Rules

### Natural Chinese First
When Japanese and Chinese differ structurally, choose the most natural Chinese expression that preserves the original function. Do not preserve Japanese syntax at the expense of Chinese readability.

Allowed transformations include reordering, splitting, merging, replacing an idiom with a Chinese equivalent, and lightly embedding necessary cultural context. These are allowed only when they preserve facts, ambiguity, tone, and scene function.

### Accuracy Before Polish
- Do not add information, motivations, scene details, foreshadowing, or emotional intensity not present in the source.
- Do not delete small jokes, hesitations, relationship cues, or ambiguity because they are inconvenient.
- Do not resolve delayed reveals or unreliable narration early.
- Do not over-literarize simple Syosetu prose.

### Honorifics and Address Forms
Honorifics are not ornaments. Convert them into Chinese social meaning: distance, politeness, respect, intimacy, hierarchy, and emotional shift.

Do not mechanically keep or delete every suffix. Record stable address decisions in `meta/glossary.csv` or `meta/series_bible.md`.

### Onomatopoeia and Mimetics
- If there is a natural Chinese sound-symbolic equivalent, use it.
- If not, translate the effect, motion, mood, texture, or rhythm.
- Never keep a Japanese mimetic merely because it looks vivid in the source.
- Do not force a rare or childish Chinese sound word when action description reads better.

### Puns and Humor
Use this priority order: preserve plot function, preserve character reaction and comedic timing, preserve humorous effect, then preserve formal verbal mechanism if possible.

If full preservation is impossible, prefer creative Chinese rewriting over dead literalism. Add a note only when the wordplay itself is necessary and cannot be carried in the text.

### Culture-Loaded Items
Use a three-step decision:

1. Is the term already readable for zh-CN light-novel readers?
2. If not, does misunderstanding damage the scene?
3. If yes, add very light in-line clarification.

Avoid heavy notes unless the user explicitly wants annotation mode.

### High-Risk Calques
Do not let the following appear as lazy direct translations unless the scene truly demands them:

- `社会人`
- `元气`
- `违和感`
- `接住` for abstract `受け止める`
- `重要的事物`
- `心情复杂地`
- `温柔地笑了起来` when a simpler Chinese verb is more natural
- `说不定`
- `果然如此`

For high-risk term handling, read `references/default-glossary.md` and apply context-specific choices instead of fixed one-to-one replacements.

## Modes
- `quick`: short excerpt or rough comprehension only.
- `normal`: analyze context, translate, update memory, and self-check.
- `refined`: draft, critique, revise, Chinese-only readthrough, continuity check, and QA notes. Use for public release, full chapters, or when the user says 精翻, 顶级质量, 出版级, 完美, or 汉化.

If the user does not specify a mode, use `refined` for fiction longer than 1,500 Japanese characters and `normal` for shorter narrative text.

## Quality Gates
Use MQM-style review for literary translation. A chapter is not ready if it has unresolved critical or major errors in accuracy, fluency, character voice/register, terminology/continuity, humor/cultural transfer, or rhythm/readability.

For release QA, target:

- name/place consistency: 100%
- glossary consistency: at least 98%, allowing documented context-variable entries
- high-risk banned calque hits: 0
- major address-form drift: 0
- major relationship-line conflicts: 0
- Chinese punctuation and dialogue quote issues: near zero

Automatic scores, if available, are alarms rather than final judgment. Human-style MQM review and Chinese-only readthrough decide literary quality.

## Learning From Each Translation
When the user corrects a translation or a recurring problem appears:

- add term decisions to `meta/glossary.csv` or `references/default-glossary.md`
- add voice decisions to `meta/series_bible.md`
- add style/process corrections to `meta/style_guide.zh-CN.md` or this skill when broadly reusable
- add unresolved choices to `meta/open_issues.md`

Keep updates operational. Do not add general advice that does not change future behavior.

## Output Contract
For ordinary requests, output the polished Chinese translation first.

For file-based work, save outputs when feasible:

- `translations/<chapter>.zh-CN.md`
- `qa/<chapter>.qa.md`
- updated `meta/` assets

Unless the user asks for translation only, include a short status note listing new glossary entries, unresolved ambiguities, and high-risk continuity issues. If the user asks for only the translation, output only the final polished translation.

## Stop Conditions
Stop once the requested translation, revision, setup, or QA pass is complete and validation has enough evidence. Do not expand into unrelated tooling or rewrite the skill again unless requested.