# Novel-Agnostic Japanese Light Novel Translation Workflow — Design

**Date:** 2026-06-14
**Status:** Approved design (pending spec review)
**Location:** `G:\Translations\White Empire` (the current folder becomes a live project running this workflow)

## 1. Goal

Generalize the series-specific Quintuplets translation pipeline into a **reusable, novel-agnostic harness for Japanese light novels**, installed in the current folder as a live project (translating *白き帝国 / White Empire*). The harness must be copyable to start any future JP LN by clearing a few per-novel files and editing one config file.

The design directly fixes the failure modes found in the Quintuplets analysis:
- A fat guide file (`AGENTS.md`) that duplicated per-novel data and silently drifted.
- Three platform copies of every agent that drifted apart.
- Romanization regressions that slipped through because enforcement was manual.
- EPUB build that was un-hand-offable because per-novel knobs lived in prose, not config.
- In-file chapter headings that were inconsistent (H2 / Japanese / English) and blocked the build.

## 2. Locked decisions

| Decision | Choice |
|-|-|
| Agnostic scope | Japanese-focused, series-agnostic (not also Chinese) |
| Folder role | Live project with agnostic internals + scaffolded per-novel files |
| Platforms | Claude Code only — one canonical source, no drift |
| Pipeline depth | Full pipeline: split → translate → edit → assemble → update → image-localize → build → verify |
| Per-chapter ordering | Interleaved per part: translate Pi → edit Pi, looped; not translate-all-then-edit-all |
| Output filenames | Translated English chapter title; no in-file title heading (exception below) |
| azw3 handling | Direct extraction via KindleUnpack, no Calibre conversion; furigana preserved |
| Romanization | No-macron convention (vowel-doubling), enforced by script gate |
| Orchestration | Team-based (`TeamCreate` + shared task board), not ephemeral one-off subagents |

## 3. Architecture — three layers

One source of truth per fact. Nothing is duplicated across layers.

- **Agnostic harness** (`.claude/`, `guides/`, `scripts/`) — reusable, copies unchanged between novels.
- **Per-novel data** (`glossary.md`, `character-reference.md`, `character-voices.md`, `translation-progress.md`) — this novel's accumulated knowledge. Never duplicated into a guide file.
- **Config** (`novel.config.md`) — the handful of knobs that vary per novel.

### Directory layout

```
White Empire/
  CLAUDE.md              # lean index → guides + config (single entry point)
  novel.config.md        # per-novel knobs

  .claude/agents/        # AGNOSTIC
    translator.md  editor.md  assembler.md  updater.md
    image-localizer.md  epub-builder.md
  .claude/skills/        # AGNOSTIC
    setup-novel.md  translate-chapter.md  build-epub.md

  guides/                # AGNOSTIC (JP-LN conventions)
    translation-guide.md  footnote-guide.md  voice-building-guide.md
    quality-checklist.md  epub-build-spec.md

  scripts/               # AGNOSTIC (parameterized, no hardcoded paths)
    split_ebook.py  normalize_romaji.py  build_epub.py  verify_epub.py
    kindleunpack/        # vendored, for azw3 extraction

  glossary.md            # PER-NOVEL (scaffolded)
  character-reference.md # PER-NOVEL
  character-voices.md    # PER-NOVEL
  translation-progress.md# PER-NOVEL

  Source/Volume N/       # split chapter .md + images/
  English/Volume N/      # drafts, assembled chapters, built EPUBs
  Editing/Volume N/      # edit logs, reconciliation logs, image-localization specs

  白き帝国 *.epub / *.azw3 # raw inputs (already present)
```

## 4. Agents

All agents are agnostic: they reference per-novel files by name and embed zero series facts. They run as **registered teammates on a team** (not ephemeral subagents): each claims its task from the shared task board, does the work, marks the task complete, and messages the lead. Their tool grants already include `TaskList` / `TaskCreate` / `TaskUpdate` / `SendMessage` for this.

| Agent | Model | Role | Key discipline |
|-|-|-|-|
| translator | opus | Raw English draft of a chapter or one part | Reads locked register + `character-voices.md` + `glossary.md`; past tense; honorifics retained; footnotes per `footnote-guide.md`. When translating part Pi, reads the already-edited prior parts. |
| editor | sonnet | Line-by-line edit vs. JP source, in ~150–200-line chunks; appends to the per-chapter edit log | Targeted `Edit`s only; accuracy first; no tone elevation; register-locked |
| assembler | sonnet | Combine edited parts → one chapter file; cross-section consistency | No `Write` tool — Python-via-Bash with line-count verification. Emits no title heading. |
| updater | sonnet | Add new terms/characters to per-novel files | `WebSearch`/`WebFetch` to check official EN release / wiki if one exists; flags discrepancies, never silently rewrites |
| image-localizer | sonnet | Find text-bearing illustrations; emit localization specs (verbatim JP + EN + zero-hallucination edit prompt) | Specs only; rendering is a manual/user step |
| epub-builder | sonnet | Parameterize and run `build_epub.py` + `verify_epub.py` from config | Scripts write the EPUB; agent self-verifies the gates |

## 5. Skills (slash-command orchestrators)

- **`/setup-novel`** — one-time bootstrap. Splits Volume 1, scans it to seed `glossary.md` / `character-reference.md` / `character-voices.md`, translates the chapter-title table of contents into `novel.config.md`, classifies and **locks the register**, and fills the rest of `novel.config.md`.
- **`/translate-chapter [chapter]`** — per-chapter pipeline (see §8). Section-splitting triggers only when a chapter exceeds the configured part-split threshold.
- **`/build-epub [volume]`** — image-localize → build → verify for a whole volume.

### Team orchestration

Each skill runs as a **team lead** over a persistent team, not as a series of one-off subagent spawns:

1. `TeamCreate` a team (e.g. `white-empire`) if one does not already exist; register the agents from `.claude/agents/` as teammates.
2. The lead builds the **task board** for the run with explicit dependencies, then teammates claim and execute their tasks. Per-chapter dependency graph (parted chapter):
   - `Edit Pi` blockedBy `Translate Pi`
   - `Translate P(i+1)` blockedBy `Edit Pi` (enforces the interleaving + clean continuity context)
   - `Assemble` blockedBy all `Edit Pi`; `Update` blockedBy `Assemble`
3. Coordination is via the shared `TaskList` + `SendMessage` (lead ↔ teammate), e.g. pronoun/term reconciliation messages.
4. **Lifecycle:** reuse idle teammates across chapters within a volume; on completion, `SendMessage` a shutdown to teammates and `TeamDelete`. Verify outputs on disk before marking tasks complete — an idle teammate is not proof of a finished file (a known Quintuplets gotcha).

## 6. Guides (agnostic JP-LN conventions)

- `translation-guide.md` — author-voice principle, past-tense rule, the register framework (Casual/Comedy · Literary/Fantasy · Action/Military · Romance), honorifics, JP name order, SFX/onomatopoeia, thoughts→italics, scene-break normalization.
- `footnote-guide.md` — when to annotate (cultural terms, puns, historical refs) and the `[^N]` + `## Translator Notes` format. Default-on for JP LN.
- `voice-building-guide.md` — the method for deriving per-character voice profiles (pronoun, register, address forms, verbal tics), so every novel's `character-voices.md` is built the same way.
- `quality-checklist.md` — agnostic pre-submission checklist.
- `epub-build-spec.md` — how to map a source spine, force RTL→LTR, handle front/back matter, popup footnotes, and the verification gates.

## 7. Per-novel files & config

**Per-novel data files** (scaffolded empty, filled as translation proceeds):
- `glossary.md` — `JP | EN | Gender/Context`.
- `character-reference.md` — names, genders, roles, speech patterns, example quotes.
- `character-voices.md` — this novel's per-character voice profiles + active-narrator guide.
- `translation-progress.md` — chapter status tracker + known issues.

**`novel.config.md`** — the knobs that vary per novel:
- Source ebooks and per-volume mapping; `Source/` and `English/` paths.
- **Chapter-title map** — JP title → translated EN title per chapter (single source of truth for filenames and EPUB headings/TOC/contents image).
- **Romanization convention** (White Empire: no-macron, vowel-doubling).
- **Reading direction** (source RTL → build LTR).
- **Register lock** (classified once at `/setup-novel`).
- **Part-split threshold** (chapter source-line count above which a chapter splits into parts).
- EPUB metadata (title, series, per-volume titles).

## 8. Pipeline data flow

### Per chapter (`/translate-chapter`)

```
PRE-GLOSS  (once per chapter — scan whole source, add new terms to glossary.md)
if chapter source-lines > part-split threshold:
    for each part P1…Pn, in order:
        translate Pi   ← reads the already-EDITED prior parts for continuity
        edit Pi        ← vs JP source, immediately after its translation
    assemble edited P1…Pn → chapter file (consistency pass, no heading)
else:
    translate whole → edit whole
update  (glossary / character-reference / character-voices)
normalize_romaji.py --check   (gate)
update translation-progress.md
→ output: English/Volume N/<Translated Title>.md
```

### Per volume (`/build-epub`)

```
image-localizer scans illustrations → specs in Editing/Volume N/image-localization/
(user renders the 1–3 text-bearing images)
epub-builder parameterizes build_epub.py from config (titles, spine map, RTL→LTR, image swaps)
build_epub.py → verify_epub.py
gates: zero macrons · zero stray CJK in prose · all refs resolve · popup footnotes paired
```

## 9. Output naming & in-file title rule

- **Filename = the translated chapter title**, pattern `Chapter <N> - <Translated Title>.md`. Source `第５話 ５月５日` → `Chapter 5 - May 5th.md`. The number `<N>` and `<Translated Title>` both come from the chapter-title map in `novel.config.md`.
- **No title heading inside the file.** Prose starts directly; `## Translator Notes` (if any) at the end. The assembler emits no `#` chapter heading.
- **Exception:** if a translated title contains a Windows-illegal filename character (`< > : " / \ | ? *`), the filename uses a sanitized version and the full true title is written as the in-file `#` heading so nothing is lost.
- The EPUB build reads chapter `<h1>` / TOC / contents-image titles from the config title map, not from any in-file heading.

## 10. Source extraction & furigana

- `split_ebook.py` has two front-ends feeding one shared XHTML splitter:
  - `.epub` → read XHTML directly.
  - `.azw3` (KF8) → run vendored **KindleUnpack** first (decompresses the KF8 source HTML, ruby intact — no Calibre conversion, which can flatten furigana), then feed the same XHTML splitter.
- **Furigana preserved** for all formats: `<ruby>漢字<rt>かな</rt></ruby>` → inline `漢字[かな]`. Square brackets are used deliberately to avoid colliding with the `（）` / `《》` thought markers. The translator sees both the kanji and its reading.
- Output per volume: `Source/Volume N/<JP chapter file>.md` + `images/`.

## 11. White Empire specifics & constraints

- Vol 1 (`白き帝国 １ ～ガトランド炎上.epub`) and Vol 2 (`白き帝国 2 ~約束の戦旗~ … .epub`) are `.epub` — split directly.
- Vol 3 (`白き帝国 ３　～アルテミシア純情～.azw3`) is `.azw3` — extracted via KindleUnpack (no conversion). **Prerequisite:** vendored KindleUnpack in `scripts/kindleunpack/` (pure Python, no Calibre).
- Register: military/war fantasy — `/setup-novel` will lock it to Literary/Action, not comedy.
- Romanization defaults to no-macron; `normalize_romaji.py` reused as the enforcement gate.

## 12. Copy-to-new-novel procedure

1. Duplicate the folder.
2. Clear the four per-novel files (or run `/setup-novel`, which repopulates them).
3. Clear `Source/`, `English/`, `Editing/`; drop in the new ebooks.
4. Edit `novel.config.md`.
   The agnostic layers (`.claude/`, `guides/`, `scripts/`) are untouched.

## 13. Non-goals (out of scope)

- Non-Japanese source languages (the existing Chinese Workflow Template covers Chinese).
- Other agent platforms (OpenCode, Codex).
- Actually translating White Empire chapters — that is the next action triggered after the harness is built (`/setup-novel`, then `/translate-chapter`). This spec delivers the workflow and the scaffolding only.

## 14. Open items

- Confirm whether to also run `/setup-novel` for White Empire as part of this work, or stop at delivering the runnable harness.
- Git is not initialized in this folder; this spec is not committed. Offer to `git init` if version control is wanted.
