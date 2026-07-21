# Quality Checklist — Pre-Submission (Agnostic)

Verify every item before marking a translated passage or chapter complete. This
checklist is series-agnostic; the specifics it points at live in
`novel.config.md`, `character-voices.md`, and `glossary.md`.

## Narrator & Voice
- [ ] Active narrator identified for this chapter (fixed, rotating, or third-person
      per `character-voices.md`).
- [ ] Narration voice matches the correct profile: the active narrator's voice
      (first-person) or the author's locked register (third-person).
- [ ] Every speaking character is identifiable from their dialogue alone, tags
      removed.
- [ ] Each character's pronoun-signalled register, particles/tics, and emotional
      default are reproduced (per `character-voices.md`).
- [ ] Documented voice/address shifts (arc beats) land clearly in English.

## Grammar & Tense
- [ ] ALL narration in past tense.
- [ ] Internal thoughts in past tense in narration ("she thought…" not "she
      thinks…").
- [ ] Dialogue stays in natural speech tense.

## Register & Style
- [ ] Output matches the **locked register** in `novel.config.md` (Casual/Comedy ·
      Literary/Fantasy · Action/Military · Romance), including scene-level shifts.
- [ ] Prose not elevated above the source — no purple prose (see the elevation
      kill list in `translation-guide.md`: no "gaze drifted," "fury ignited," "a
      pang sprouted," "breath she didn't know she was holding," etc.).
- [ ] English sentence length/complexity tracks the source line; no padding.

## Honorifics & Names
- [ ] All honorifics retained (-kun, -san, -chan, -sama, -senpai, -sensei,
      onee-san, onii-san, and any unusual forms).
- [ ] Address forms correct per character per `character-voices.md`.
- [ ] Names in Japanese order (family name first), except documented exceptions.

## Formatting
- [ ] Sound effects / onomatopoeia naturalized, not transliterated.
- [ ] Scene breaks (✿ / ☆ / ■ / ◇ / etc.) rendered as `---`.
- [ ] Internal thoughts （…）/《…》 rendered as *italics* (no quotation marks).
- [ ] Inline images preserved exactly: `![filename](images/filename)`.
- [ ] No furigana `[かな]` brackets left in the English prose.
- [ ] No in-file title heading (unless the sanitized-filename exception applies).
- [ ] No "Illustration Mapping" header in the output.

## Glossary
- [ ] All terms and proper nouns match `glossary.md` exactly — no synonyms or
      spelling variants.

## Gates (before filing the chapter as done)
- [ ] **Chapter gates clean** —
      `python3 core/scripts/run_chapter_gates.py --chapter <N>` exits zero. If
      `<N>` is ambiguous across units, run
      `python3 core/scripts/run_chapter_gates.py --unit <Unit> --chapter <N>`.
      This includes romanization, chapter consistency, and whole-unit
      consistency after the updater runs.
- [ ] **Style-guide Running Summary entry appended** — `style-guide.md` has a
      2–3 sentence `### Chapter N` entry under `## Running Summary` for this
      chapter (schema: `core/schemas/style-guide-schema.md`).

## Footnotes
- [ ] Untranslated terms, puns, cultural/historical references footnoted on first
      appearance in the chapter.
- [ ] `## Translator Notes` section present at the end if any footnotes are used.
- [ ] Footnote numbering continues sequentially across a chapter's parts (no
      mid-chapter reset); every `[^N]` has a matching note and vice versa.

## Romanization
- [ ] **No macrons** — no-macron / vowel-doubling convention throughout
      (*Tarou*, *Yuusuke*, *senpai*; never ō/ū). `normalize_romaji.py --check`
      passes.
