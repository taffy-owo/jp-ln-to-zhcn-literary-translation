# Quality Rubric

Use this for refined-mode critique, chapter QA, volume QA, and regression checks.

## MQM-Style Dimensions

| Dimension | Weight | Check | Typical Errors |
|---|---:|---|---|
| Accuracy | 30 | facts, causality, pronouns, relationships, foreshadowing | omission, mistranslation, reversal, wrong restored subject |
| Fluency | 20 | whether Chinese reads smoothly and like fiction | stiff syntax, Japanese order, dead literalism |
| Character Voice and Register | 15 | distinct speakers, politeness, age, distance | same voice for all, flattened honorifics, register mismatch |
| Terminology and Continuity | 15 | names, address forms, world terms, catchphrases | drift, duplicate translations, unstable labels |
| Humor, Puns, Cultural Transfer | 10 | joke function, cultural handling | dead puns, lost reaction, over-explaining |
| Rhythm and Readability | 10 | pacing, paragraph movement, emotional arc | wooden rhythm, flattened confession, weak turn |

## Score Bands
- 90+: ready for light human proofreading.
- 80-89: strong but needs style unification.
- 70-79: needs focused repair.
- below 70: retranslate problem chapters instead of patching locally.

## Release Gates

| Gate | Target | Note |
|---|---:|---|
| name/place consistency | 100% | Drift is high impact. |
| glossary consistency | >= 98% | Allows documented context-variable entries. |
| high-risk banned calque hits | 0 | Examples: 社会人, abstract 接住, 违和感. |
| dropped sentence/paragraph risk | <= 0.3% | Check by paragraph or scene alignment. |
| quote/punctuation standard | >= 99% | Use Chinese publishing-style punctuation. |
| high-risk address drift | 0 major | 学长/前辈/老师/name-only etc. |
| catchphrase drift | 0 major | Series readers notice this. |
| relationship-line conflict | 0 major | Especially romance, family, hierarchy. |

## Review Layers
1. Smoke test: validate files, encoding, chapter count, and obvious banned terms.
2. Chapter test: inspect one dialogue-dense passage and one narration/introspection passage.
3. Volume consistency test: compare terms, names, address forms, jokes, and emotional motifs.
4. Cross-volume regression: compare with previous volume glossary, series bible, continuity notes, and actual translations.

## Human Editing Loop
1. First-chapter style lock: translate 1,500-3,000 source characters or one chapter sample and record style decisions.
2. Chapter-level fact audit: check speaker, pronoun chain, chronology, causality, omission, and over-translation.
3. Literary polish: remove translationese without changing facts.
4. Chinese-only readthrough: read as a Chinese novel without source beside it.
5. Cross-volume regression: confirm old names, jokes, address forms, and setting terms still hold.

Automatic metrics such as DocCOMET or XCOMET may be used as alarms when available, but never as the final judge of literary quality.