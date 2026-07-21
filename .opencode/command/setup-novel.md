---
description: One-time bootstrap for a new Japanese light novel — splits Volume 1, seeds the per-novel reference files, translates the chapter-title TOC, classifies and locks the register, and fills novel.config.md. Run once per novel.
---

Bootstrap this novel (one-time setup).

One-time bootstrap that turns the empty harness into a live project for this novel. Run once per novel; re-run to extend to a later volume. You drive the sequence and dispatch the per-stage agents in `.opencode/agents/` **by name** (`updater`, `translator`) with the task tool — spawn → wait → collect → close. Subagents are ephemeral and isolated; there is no shared task board, so ordering lives in this prose. Dispatch at most **6 subagents concurrently**. Verify every output **on disk** before you treat a step as done — an agent returning is not proof of a finished file.

## Outcome

A live project: Volume 1 split to `Source/Volume 1/`; the four per-novel reference files seeded to their schemas; every chapter title translated into the `novel.config.md` chapter-title map; the register classified and **locked**; and the remaining `novel.config.md` knobs filled. These are exactly the inputs the per-chapter pipeline (`core/pipeline.md`) reads on every later run, so seeding them correctly here is what makes that pipeline work. Setup is not successful until the hard gate in step 6 passes.

## 1. Split Volume 1

Read `novel.config.md` for the Volume 1 source ebook path and format, then split (format auto-detected):

```bash
python core/scripts/split_ebook.py "<Vol 1 source ebook>" Source --volume 1
```

`.epub` reads XHTML directly; `.azw3` (KF8) runs vendored KindleUnpack first (no Calibre; needs `core/scripts/kindleunpack/lib/` populated). Output: `Source/Volume 1/<JP chapter>.md` (furigana as `漢字[かな]`) plus `Source/Volume 1/images/`. Confirm the chapter files and images exist on disk before continuing.

## 2. Seed the four reference files

Scan the split source and seed each file to its schema in `core/schemas/`; write data only into these files, never into a guide:

- `glossary.md` — `glossary-schema.md`; characters, places, organizations, recurring terms.
- `character-reference.md` — names, genders, roles, speech patterns, example quotes.
- `character-voices.md` — per-character profiles per `core/guides/voice-building-guide.md` and `character-voices-schema.md`, plus the `## Narrator` block with its **Register ceiling** line and an `### Elevation kill-list` table of **at least five** wrong→right rows drawn from this novel's real over-elevation traps. This file gates setup (step 6) — build the kill-list deliberately.
- `style-guide.md` — the `## Style Guide` section per `style-guide-schema.md`; leave `## Running Summary` empty with its heading (the updater fills it per chapter).

Delegate scanning to `updater` and/or `translator` subagents, each with a complete spec up front (which file, its schema path, the source dir). When several files can be seeded independently, dispatch those subagents in the same batch (≤6). Verify each seeded file on disk against its schema before continuing.

## 3. Translate the chapter-title TOC

Extract every chapter title from the Volume 1 source (and any later-volume TOCs the config lists), translate each JP→EN, and write the chapter-title map (`| Vol | N | JP title | EN title |`) into `novel.config.md`. This map is the single source of truth for output filenames and EPUB `<h1>`/TOC titles — translate every row; leave none in JP.

## 4. Classify and LOCK the register

Using the register framework in `core/guides/translation-guide.md`, classify this novel's dominant register from the Volume 1 prose and write it plus a one-line justification into the **Register Lock** section of `novel.config.md`. Once locked it holds for the whole novel; every agent reads it from there.

## 5. Fill the rest of novel.config.md

Populate the remaining knobs per `core/schemas/novel-config-schema.md`: source→volume map, `Source/`/`English/`/`Editing/` paths, romanization (no-macron, vowel-doubling), reading direction (source RTL → build LTR), part-split threshold, `qa_major_threshold`, and EPUB metadata.

## 6. Hard gate, then close

`character-voices.md` is a **hard-fail gate** — do not report setup successful unless it has the Narrator **Register ceiling** line and an `### Elevation kill-list` with **≥5 rows**. Verify on disk and report the exact output:

```bash
grep -q '\*\*Register ceiling:\*\*' character-voices.md && echo "ceiling: OK" || echo "ceiling: MISSING"
awk '/### Elevation kill-list/{f=1;next} f&&/^## /{f=0} f&&/^\|/{c++} END{print "kill-list data rows:", c-2}' character-voices.md
```

The first must print `ceiling: OK`; the second `5` or more. On failure, send the responsible subagent back to fix `character-voices.md` and re-run — do not proceed on a failing gate. (The awk assumes the kill-list is the only table in that span; re-check it if the schema adds another.)

## Disposition

Persistence: keep going until Volume 1 is split, all four reference files are seeded and verified, the title map + register lock + knobs are in `novel.config.md`, and the hard gate passes. Scope guard: bootstrap only — do not begin translating chapters; note that as the user's next step (`/translate-chapter`). Never ask clarifying questions; cover the most likely intent.

## Report

Chapters split; entries seeded per reference file; the locked register; the two gate-command outputs verbatim; and what remains for the user (typically nothing, or rendering text-bearing images later during build-epub).
