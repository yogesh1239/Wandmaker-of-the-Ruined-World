# Independent Narrative/Direct-Thought Tense Audit

## Scope

- Audited every filed chapter in `English/Volume 1/` (Chapters 1–14) and `English/Volume 2/` (Chapters 1–8).
- Matched source and translation by paragraph sequence where structure was preserved, and by exact Japanese/English phrasing plus surrounding context where paragraphs had been split or merged; the Volume 1 dossier artifact and ebook-bonus title offset were handled separately.
- Reviewed unquoted questions, exclamations, deductions, self-address, current plans, technical/general conclusions, and mixed narrative/thought paragraphs.
- Left narrated action, description, indirect/reported thought, genuine retrospection, and source-required conditional/past-perfect forms in past tense.
- Kept unmarked direct thought roman and did not reinterpret Ori's parenthetical qualifications or asides as thought by default.

## Filed-Chapter Results

- **Volume 1, Chapters 1–6:** Restored natural speech tense in Ori's live deductions, technical conclusions, self-praise, plans, and immediate reactions; retained past-tense narrated events.
- **Volume 1, Chapter 7:** Corrected the Blue Witch's final immediate assessment and expectation while retaining the surrounding Council narration in past tense.
- **Volume 1, Chapters 8–11:** Restored natural speech tense in immediate questions, reactions, current assessments, and plans. Close-third direct thought was corrected without shifting surrounding action out of past tense.
- **Volume 1, Chapter 12:** Audited; its explicitly reported childhood thought and embedded direct questions already preserved the required distinction.
- **Volume 1, Chapter 13:** Audited; image-only dossier artifact contained no English narrative prose requiring a tense edit.
- **Volume 1, Chapter 14:** Retained the descriptive ebook-bonus narration in past tense, while correcting Ori's explicit current “for now” assessment of the crystal rain.
- **Volume 2, Chapters 1–8:** Restored natural speech tense in immediate inner speech, discoveries, current evaluations, technical reasoning, and forward plans; retained past narration and semantically required past forms.

## Referent Correction

- **Volume 1, Chapter 9:** Changed the Foresight Mage's secretary from singular `they/them` to `she/her` in the filed chapter and editable Part 2 draft.
- Added `Foresight Mage's Secretary (未来視の魔法使いの秘書)` to `character-reference.md` with **Female** locked from the Volume 1 booklet profile: `文京区役所で未来視の魔法使いの秘書を務める女性`.
- The chapter's own edit log contains the detailed referent correction entry.

## Verification

- Completion re-audit found and corrected residual half-converted thought sequences left by the initial pass, including sequences whose final question was present but whose setup remained past.
- Manually adjudicated the final residual-pattern scan rather than mechanically converting all first-person past forms; historical facts, narrated reactions, counterfactuals, and reported thought remain past where required.
- `normalize_romaji.py --check` passed all 22 filed chapter files after the completion re-audit.
- Whole-volume `check_consistency.py --all` passed independently for both `English/Volume 1/` and `English/Volume 2/`.
- `test_check_consistency.py` passed.
- `git diff --check` passed.
- The consistency gate's proper-title alias handling was corrected and regression-tested so banned game-title alias `Gather` still fails while ordinary lowercase verb `gather` does not false-positive against canonical `Gath`.
