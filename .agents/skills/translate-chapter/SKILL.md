---
name: translate-chapter
description: Runs the Japanese chapter pipeline: pre-gloss, translate/edit, assemble when parted, update references, then run the romaji and consistency gates. Accepts one chapter.
---

# Translate Chapter

Read `AGENTS.md`, `core/pipeline.md`, and `novel.config.md`.

1. Pre-gloss the complete JP source before translation.
2. If the source exceeds the configured part threshold, dispatch `translator` then `editor` for each part in order; do not release the next part until the prior edit exists on disk. Otherwise dispatch each once for the whole chapter.
3. On the parted path, dispatch `assembler`. On the whole path, the editor writes the final chapter.
4. Dispatch `updater` after the final chapter exists.
5. Run `python3 core/scripts/run_chapter_gates.py --chapter <N>`; add `--unit <Unit>` when the chapter number is ambiguous. Fix failures through the editor and rerun until clean.
6. Confirm the final chapter and progress update on disk.

Use only `translator`, `editor`, `assembler`, and `updater` from `.codex/agents/`. Put the assigned JP source scope once at the top of translate/edit dispatches; pass paths and line ranges thereafter. Verify outputs structurally with shell commands; the editor's line-by-line accuracy pass owns content verification.

Report the final path, whole/parted path, reference changes, discrepancies, and gate results.
