---
name: setup-novel
description: One-time bootstrap for a new Japanese light novel — splits Volume 1, seeds the per-novel reference files, translates the chapter-title TOC, classifies and locks the register, and fills novel.config.md. Usage: /setup-novel
---

# /setup-novel

One-time bootstrap that turns the empty harness into a live project for this novel. Run once per novel; re-run to extend to a later volume. You act as **lead** of the session's team.

## Orchestration

The team is implicit — the session already has one, so you register no team and create none. You spawn teammates directly with the **Agent** tool (`subagent_type` = the `.claude/agents/` name, e.g. `translator`, `updater`) and coordinate them with `TaskCreate` / `TaskList` / `TaskUpdate` dependencies plus `SendMessage`. **When you have independent seeding work to fan out — for example seeding several reference files or translating batches of titles at once — spawn multiple subagents in the same turn** so they run in parallel; a single sequential agent here is slower for no benefit. Build a `TaskList` for the steps below with their dependencies, then drive it. Verify every output **on disk** with `Read`/`Bash` before you mark its task complete — an idle teammate is not proof of a finished file.

## 1. Split Volume 1

Read `novel.config.md` for the Volume 1 source ebook path and format, then run the splitter (format auto-detected from the extension):

```bash
python core/scripts/split_ebook.py "<Vol 1 source ebook>" Source --volume 1
```

- `.epub` → XHTML read directly.
- `.azw3` (KF8) → the splitter runs vendored KindleUnpack first (no Calibre), then the shared XHTML splitter. This needs `core/scripts/kindleunpack/lib/` populated (see its README).
- Chapter boundaries come from the ebook's nav/NCX TOC; output files are `NN <JP title>.md`.

Output: `Source/Volume 1/<JP chapter>.md` (furigana preserved as `漢字[かな]`) plus `Source/Volume 1/images/`. Confirm the chapter files and images exist on disk before continuing.

## 2. Seed the per-novel reference files

Scan the split Volume 1 source and create/seed these four files, each to its schema in `core/schemas/`. Write the data only into these files — never duplicate it into a guide:

Derive JP/base, romaji, and proposed EN lookup keys for every candidate name, title, place, organization, term, and recurring phrase. When live references or prior filed prose already exist, `Grep` all four reference files and relevant English chapters, read the complete surrounding hit, and search spelling/furigana variants before adding anything. One no-hit search does not prove novelty; never use `reference-archive.md` as live context.

- `glossary.md` — per `core/schemas/glossary-schema.md`; characters, places, organizations, recurring terms.
- `character-reference.md` — names, genders, roles, speech patterns, example quotes.
- `character-voices.md` — per-character voice profiles per `core/guides/voice-building-guide.md` and `core/schemas/character-voices-schema.md`, plus the `## Narrator` block with its **Register ceiling** line and the `### Elevation kill-list` table. This file gates the whole setup (see step 6), so build the kill-list deliberately: at least five rows of real over-elevation traps drawn from this novel's register, each written as a wrong→right pair (elevated phrasing in the left column, the plain form you want in the right).
- `style-guide.md` — the `## Style Guide` section per `core/schemas/style-guide-schema.md` (tone, audience mirroring the locked register, recurring prose conventions). Leave `## Running Summary` empty with its heading; the updater fills it per chapter.

Delegate the scanning to `updater` and/or `translator` teammates via the Agent tool. Give each teammate a complete spec up front — which file to seed, its schema path, and the source directory to scan — rather than drip-feeding follow-ups; front-loading the full task is what keeps the seeding pass efficient. Verify each seeded file on disk against its schema.

## 3. Translate the chapter-title TOC

Extract every chapter title from the Volume 1 source (and any later volumes' TOCs available in the config). Translate each JP title to EN and write the **chapter-title map** (`<N> | JP title | Translated EN title`) into `novel.config.md`. This map is the single source of truth for output filenames and for EPUB `<h1>`/TOC/contents-image titles, so translate every row — do not leave any title in JP.

## 4. Classify and LOCK the register

Using the register framework in `core/guides/translation-guide.md` (Casual/Comedy · Literary/Fantasy · Action/Military · Romance), classify this novel's dominant register from the Volume 1 prose. Write the locked register plus a one-line justification into the **Register Lock** section of `novel.config.md`. Once locked it holds for the whole novel; every agent reads it from there, which is why it must be pinned here and not re-decided per chapter.

## 5. Fill the rest of novel.config.md

Populate the remaining knobs per `core/schemas/novel-config-schema.md`: source ebooks + per-volume mapping, `Source/` / `English/` paths, an explicit no-macron romanization convention (including whether long vowels are doubled or unmarked), reading direction (source RTL → build LTR), part-split threshold, and EPUB metadata (title, series, per-volume titles).

## 6. Verify the hard gate, then close

`character-voices.md` is a **hard-fail gate**: do not report setup as successful unless it contains the Narrator **Register ceiling** line and an `### Elevation kill-list` table with **at least five rows**. Verify both on disk before you finish, and report the exact command output:

```bash
grep -q '\*\*Register ceiling:\*\*' character-voices.md && echo "ceiling: OK" || echo "ceiling: MISSING"
awk '/### Elevation kill-list/{f=1;next} f&&/^## /{f=0} f&&/^\|/{c++} END{print "kill-list data rows:", c-2}' character-voices.md
```

The first must print `ceiling: OK`; the second must print a count of **5 or more**. (The awk counts pipe-rows between `### Elevation kill-list` and the next `## ` heading, minus the table's header and separator lines; it assumes the kill-list is the only table in that span. If `core/schemas/character-voices-schema.md` ever adds another table subsection there, this gate goes lenient — re-check the awk when the schema changes.) If either fails, the setup is not done — send the responsible teammate back to fix `character-voices.md` and re-run the checks. Do not proceed to the report on a failing gate.

Then confirm on disk: split Volume 1, all four seeded reference files, and the chapter-title map + register lock + knobs in `novel.config.md`. Send teammates a shutdown via `SendMessage` (or leave them idle if the user is about to run `/translate-chapter`).

## Report

Chapters split; entries seeded per reference file; locked register; the two gate-command outputs verbatim; and what remains for the user (typically nothing, or rendering text-bearing images later during `/build-epub`).
