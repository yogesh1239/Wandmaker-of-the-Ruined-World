---
name: translate-chapter
description: Runs the Japanese chapter pipeline: pre-gloss, translate/edit, assemble when parted, update references, then run the romaji and consistency gates. Accepts one chapter.
---

# Translate Chapter

Read `AGENTS.md`, `core/pipeline.md`, and `novel.config.md`.

1. Pre-gloss the complete JP source before translation. Derive candidate names, titles, places, organizations, abilities, technical terms, and recurring phrases; grep their JP/base forms and proposed EN forms across `glossary.md`, `character-reference.md`, `character-voices.md`, `style-guide.md`, and relevant filed chapters. Read the surrounding entry for every hit, and search variants before treating a no-hit candidate as new.
2. If the source exceeds the configured part threshold, target roughly one threshold-sized source scope per translation part. Around each target line, choose the nearest appropriate boundary: prefer an explicit `---`, then a scene or POV break, then a paragraph break. Never cut a scene merely to hit the exact line count, and avoid a much smaller final remainder by moving the preceding boundary or merging the remainder when practical. Never use the editor's ~150–200-line audit chunks as translation-part boundaries. Dispatch `translator` then `editor` for each part in order; do not release the next part until the prior edit exists on disk. Otherwise dispatch each once for the whole chapter.
3. On the parted path, dispatch `assembler`. On the whole path, the editor writes the final chapter.
4. Dispatch `updater` after the final chapter exists.
5. Run `python3 core/scripts/run_chapter_gates.py --chapter <N>`; add `--unit <Unit>` when the chapter number is ambiguous. Fix failures through the editor and rerun until clean.
6. Confirm the final chapter and progress update on disk.

Use the current runtime's `translator`, `editor`, `assembler`, and `updater` subagents. Put the assigned JP source scope once at the top of translate/edit dispatches; pass paths and line ranges thereafter. Include the lead's targeted reference hits, and require subagents to grep the live reference files for any uncovered source term or character. Verify outputs structurally with shell commands; the editor's line-by-line accuracy pass owns content verification.

Report the final path, whole/parted path, reference changes, discrepancies, and gate results.
