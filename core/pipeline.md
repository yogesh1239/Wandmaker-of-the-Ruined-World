# Pipeline — Canonical Per-Chapter Spec (Codex)

This is the single source of truth for the per-chapter translation pipeline:
stages, ordering, the dependency graph, file contracts, gate commands, and
per-stage done-criteria. The Codex runtime (`.agents/` skills and `.codex/`
subagents) **cites this file** — those files carry role framing and tool wiring
without restating the facts below. When a stage
references a data format, it names the schema in `core/schemas/`; it never
copies the schema's contents.

Scripts live at `core/scripts/`. All commands below are run from the novel-root
directory (where `novel.config.md` sits).

## Stages

| # | Stage | Agent | Runs |
|-|-|-|-|
| 0 | PRE-GLOSS | lead | once per chapter, before any translation |
| 1 | Translate P*i* | translator | per part (parted) / once (whole) |
| 2 | Edit P*i* | editor | per part (parted) / once (whole) |
| 3 | Assemble | assembler | once, parted path only |
| 4 | Update | updater | once per chapter |
| 5 | Gates | lead | after Update |

## Dependency graph

```
Translate P1 → Edit P1 → Translate P2 → Edit P2 → … → Edit Pn
                                                          │
                                    (all Edit Pi) ────────┤
                                                          ▼
                                                      Assemble ──► Update ──► Gates
```

- `Edit Pi` **blockedBy** `Translate Pi`.
- `Translate P(i+1)` **blockedBy** `Edit Pi` — the interleave. Part *i+1* is
  translated against the *edited* part *i*, so continuity (names, voice,
  address forms) carries forward clean rather than compounding raw-draft drift.
- `Assemble` **blockedBy** every `Edit Pi` (parted path only).
- `Update` **blockedBy** `Assemble` (parted) or `Edit` (whole).
- The chapter is filed **done** only after the whole-unit consistency gate
  passes post-Update (Stage 5). For light novels the unit is usually a volume;
  for webnovels it may be `main`, an arc, a part, or another project-defined
  grouping.

Verify every stage's output **structurally** before marking its task complete —
`wc -l` against the expected scope, `head`/`tail` for the required leading and
trailing sections, `grep` for required markers (scene breaks, `## Translator
Notes`, edit-log part headings). The lead need not read a draft or chapter in
full; the editor's line-by-line accuracy pass owns content verification.

### Targeted reference retrieval

Every stage that interprets or verifies prose must actively retrieve the
series context relevant to its assigned scope; a generic instruction to "read
the references" is not enough.

1. Derive lookup keys from the assigned JP source and, when present, its EN
   draft: names, titles, honorific-bearing forms, places, organizations,
   abilities, weapons, technical terms, recurring phrases, and plausible base
   forms without furigana or inflection.
2. `Grep` those JP keys and known EN renderings across `glossary.md`,
   `character-reference.md`, `character-voices.md`, and `style-guide.md`, then
   read the complete row/profile/summary entry around each hit. Also search the
   already-edited prior part and relevant filed chapters when wording, address
   form, or continuity has precedent there.
3. Always inspect the narrator register ceiling, elevation kill-list, and
   applicable style-guide conventions even when no character-specific search
   hits. Do not read `reference-archive.md`; it is storage, not live context.
4. One no-hit search does not establish novelty. Search script/base variants,
   the source form without furigana, and the proposed EN rendering before
   coining or adding anything. Report unresolved collisions or missing locks.

The lead applies the same lookup before PRE-GLOSS and includes the resulting
chapter-specific terms, voices, and continuity in each dispatch. Subagents
still run their own targeted searches; dispatch curation is a starting point,
not a substitute for grounding.

The dispatch embeds each teammate's source scope **once**. A follow-up
`SendMessage` to a live teammate references file paths and line ranges only and
**never re-echoes chapter text** — re-sending source the teammate already holds
is pure lead-output-token waste.

## Path by length

Read the **part-split threshold** (integer source-line count; default per
`core/schemas/novel-config-schema.md`) from `novel.config.md`. Count the
chapter's JP source lines.

- **Source lines > threshold → PARTED path.** Split the source into parts
  P1…Pn at natural scene breaks; run Translate/Edit interleaved per the graph
  above; then Assemble.
- **Source lines ≤ threshold → WHOLE path.** One Translate, one Edit; there is
  no Assemble stage, so **the editor finalizes** — after its two passes it writes
  the final chapter file itself (Stage 2, "Whole-path finalization").

## Stage details

### 0 — PRE-GLOSS
The lead scans the whole chapter source for terms not yet in `glossary.md`
(names, places, organizations, abilities/weapons/techniques, recurring phrases,
honorific-bearing forms), searches each candidate and its variants across the
live reference files per **Targeted reference retrieval**, and adds each truly
new row in the format defined by
`core/schemas/glossary-schema.md`, consistent with existing entries. Done when
every new term in the chapter has a
glossary row **before** any Translate task starts — so translators inject a
complete glossary, not a stale one.

### 1 — Translate P*i*
Translator produces a raw English draft against the JP source, following
`core/guides/translation-guide.md` (register lock, past tense, honorifics, name
order, furigana, SFX) and the voice profiles + kill-list in
`character-voices.md`. For *i* > 1 it reads the already-**edited** prior parts
and `style-guide.md` for continuity. The translate stage optimizes **accuracy +
register fidelity**; naturalness is the editor's polish pass, not this stage.
- Draft → `Editing/Volume N/Chapter <N> - P<i> draft.md` (parted) or
  `Editing/Volume N/Chapter <N> - draft.md` (whole).
- Done when the draft covers the whole part and preserves every source image
  marker and scene break.

### 2 — Edit P*i*
Editor works in two sub-passes over the draft, one teammate (see
`core/guides/translation-guide.md` and `quality-checklist.md`):
1. **Accuracy pass** — line-by-line against the raw JP in ~150–200-line chunks;
   targeted edits only; every change logged before→after + a taxonomy tag (see
   `core/schemas/edit-log-schema.md`).
2. **Polish pass** — reads the English first, chunk by chunk, and lifts it to
   read as native-authored prose, capped by the register ceiling and kill-list
   in `character-voices.md`. Sentence length/energy must track the JP (choppy JP
   stays choppy), so every span it changes is re-checked against its JP line
   before the change is finalized. One polish iteration only. Its log entries
   carry the `[polish]` tag.
- Log → appended to `Editing/Volume N/Chapter <N> - Edit Log.md`, format per
  `core/schemas/edit-log-schema.md` (parted chapters append a `## Part <i>`
  section under the same file).
- **Whole-path finalization (whole path only).** On the whole path no Assemble
  stage follows, so the editor produces the final chapter file after both
  passes: it writes `English/Volume N/Chapter <N> - <Title>.md` from the edited
  draft, applying the **File contracts** below (no in-file title heading; a
  single consolidated `## Translator Notes`; the Windows-illegal-char
  exception). Like the assembler, the editor has no Write tool — it does this as
  a Python-via-Bash copy/transform of the edited draft with line-count
  verification, not a hand-retype. On the **parted** path the editor finalizes
  nothing; the assembler (Stage 3) does.
- Done when both sub-passes have run over the whole part and the log records
  them — and, on the whole path, the final chapter file is on disk per that
  contract. Then, and only then, release `Translate P(i+1)`.

### 3 — Assemble (parted path only)
Assembler concatenates the edited parts in order (Python-via-Bash with
line-count verification), runs a cross-section consistency pass, consolidates a
single `## Translator Notes` section, and emits the chapter body with **no title
heading**. Reconciliation fixes (e.g. a pronoun that drifted between parts) go
back to the relevant editor via SendMessage.
- Output → the final chapter path (see File contracts).
- Done when the assembled line count matches the sum of edited parts (minus
  intentional de-duplication of a shared notes section) and the cross-section
  pass is clean.

### 4 — Update
Updater scans the finalized chapter + source, adds new terms/characters to
`glossary.md` / `character-reference.md` / `character-voices.md` (web-verifying
against an official EN release or wiki when one exists, else marking
project-original), appends a 2–3 sentence entry to the `## Running Summary` of
`style-guide.md` per `core/schemas/style-guide-schema.md`, and **flags**
discrepancies rather than silently rewriting established voice or terms.
- Done when the reference files and the style-guide summary reflect this
  chapter.

### 5 — Gates
Run all three, in order, against the filed chapter; every one must pass before
the chapter is done (see Gate commands).

## Gate commands

Preferred wrapper. If the chapter number is unique in the chapter-title map:

```bash
python3 core/scripts/run_chapter_gates.py --chapter <N>
```

If the same chapter number appears in more than one unit, pass the unit:

```bash
python3 core/scripts/run_chapter_gates.py --unit <Unit> --chapter <N>
```

Multi-volume light novels often restart chapter numbering in each volume, so
they will commonly use `--unit 1`, `--unit 2`, and so on. Single-stream
webnovels commonly omit `--unit` once `main` is the only configured unit.

The wrapper resolves the final chapter file from `novel.config.md`, runs the
chapter romanization gate, the chapter consistency gate, and the whole-unit
consistency gate in order, then exits non-zero on the first failure.

Debug equivalent, with explicit paths substituted from `novel.config.md`:

```bash
# Romanization: no macrons
python3 core/scripts/normalize_romaji.py --check "<English path>/Chapter <N> - <Title>.md"

# Deterministic consistency, this chapter
python3 core/scripts/check_consistency.py --glossary glossary.md "<English path>/Chapter <N> - <Title>.md"

# Deterministic consistency, whole unit
python3 core/scripts/check_consistency.py --glossary glossary.md --all "<English path>"
```

`check_consistency.py` and `normalize_romaji.py` are complements: the romaji
gate catches macrons in the surface, the consistency gate catches
string-detectable term/name/honorific drift. The editor's line-by-line pass
catches contextual issues that deterministic gates cannot. Each gate exits
non-zero on a violation; fix and re-run until clean.

## Teammate lifetime — one chapter

Translator and editor are **reused across a chapter's parts** and **retired at
chapter end**; the next chapter gets fresh spawns.

- **Reuse within a chapter** is deliberate: the translator/editor's hot context
  — this chapter's source and edited parts — is exactly the continuity the
  interleave needs.
- **Retire between chapters** is deliberate too. A teammate carrying prior
  chapters' full source + drafts accumulates unbounded dead context; the rot
  degrades register and kill-list adherence, and its stale in-context term
  choices fight an updater-revised glossary — the exact cross-chapter drift this
  pipeline exists to prevent. Cross-chapter continuity is **file-borne only**
  (glossary, `character-voices.md`, `style-guide.md`, prior edited chapters),
  which fresh spawns read current.

## File contracts

| Artifact | Path |
|-|-|
| JP source | `Source/Volume N/…` |
| Part draft | `Editing/Volume N/Chapter <N> - P<i> draft.md` |
| Whole draft | `Editing/Volume N/Chapter <N> - draft.md` |
| Edit log | `Editing/Volume N/Chapter <N> - Edit Log.md` |
| Final chapter | `English/Volume N/Chapter <N> - <Translated Title>.md` |

`<N>` and the translated title come from the chapter-title map in
`novel.config.md` — the single source for output filenames.

**Final chapter file:** its producer depends on the path — the **assembler**
writes it on the parted path (Stage 3), the **editor** on the whole path
(Stage 2, "Whole-path finalization"). Either way: prose starts directly with
**no in-file title heading**; a `## Translator Notes` section (if any footnotes)
goes at the end.
**Windows-illegal exception:** if the translated title contains any of
`< > : " / \ | ? *`, the filename uses a sanitized version and the full true
title is written once as a single leading `#` heading so nothing is lost. (EPUB
`<h1>`/TOC titles still come from the config map, not the file.)
