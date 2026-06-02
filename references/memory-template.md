# Project Memory Templates

Create these files under `meta/` for long-form projects.

## meta/series_bible.md
```md
# Series Bible

## Work
- Title:
- Volume:
- Genre:
- POV:
- Target reader:
- Source files:

## Characters
| Name | JP name/reading | Role | First appearance | Voice | Address forms | Voice card | Notes |
|---|---|---|---|---|---|---|---|

## Relationships
| Pair | Relationship | Current state | Address pattern | Address shift log | Change history |
|---|---|---|---|---|---|

## Timeline
| Chapter | Event | Continuity note |
|---|---|---|

## Motifs / Repeated Lines
| Source | zh-CN handling | First use | Note |
|---|---|---|---|

## Deprecated Terms
| Original | Deprecated form | Current form | Reason | Changed at |
|---|---|---|---|---|
```

## meta/voice_cards/
为每个主要角色建立声线卡。格式详见 `references/voice-card-template.md`。

文件命名：`meta/voice_cards/<角色名>.md`

## meta/continuity_notes.md
```md
# Continuity Notes

## Current Arc State

## Address-Form Changes
| Chapter | Character | Old address | New address | Reason |
|---|---|---|---|---|

## Open Foreshadowing

## Emotional Motifs

## Resolved Issues
```

## meta/open_issues.md
```md
# Open Issues

| ID | Severity | Location | Issue | Current decision | Needs review |
|---|---|---|---|---|---|
```

## meta/glossary.csv
使用 `references/glossary-template.csv` 中的格式，包含以下字段：
- `source, reading, category, approved_zh_cn, allowed_variants, banned_variants`
- `first_appearance, character_or_entity, register_or_voice_note, cultural_note`
- `status`（proposed / approved / deprecated / forbidden）
- `decision_reason`（为何选此译法）
- `last_reviewed_chapter`（最后确认的章节）
- `deprecated_form`（废弃译名记录）

## meta/style_guide.zh-CN.md
使用 `references/style-guide-template.md` 中的格式。

## golden_set/
可选。如果项目要做回归测试，按 `references/golden-set-guide.md` 的格式建立样张。
