---
name: build-epub
description: Builds a volume EPUB end to end — image-localize, run the whole-volume consistency gate, build from novel.config.md via the derived JSON, then verify the build gates. Usage: /build-epub [volume]
argument-hint: "[volume]"
---

# /build-epub [volume]

Build the EPUB for the volume at `$ARGUMENTS` (ask the user which volume if none is given). You act as **lead** of the session's team. The commands, spine mapping, and gate list live in `core/guides/epub-build-spec.md`; this skill orchestrates them and does not restate them.

## Orchestration

The team is implicit — the session already has one, so you register no team and create none. You spawn teammates directly with the **Agent** tool (`subagent_type` = the `.claude/agents/` name: `image-localizer`, `epub-builder`) and coordinate them with `TaskCreate` / `TaskList` / `TaskUpdate` dependencies plus `SendMessage`. **When work is independent, spawn the subagents for it in the same turn** rather than serializing; here the ordering (localize → user render → consistency gate → build) is mostly sequential, so fan out only where a step genuinely has parallel sub-tasks. Front-load each dispatch with the complete spec (the volume, its `Source/Volume N/images/` directory, the reference files to read). Verify every output **on disk** before marking its task complete — a green idle teammate is not proof of a finished file.

Read `novel.config.md` for the volume's paths, chapter-title map, reading direction (RTL→LTR), image swaps, and EPUB metadata. Build the `TaskList`: `Build` **blockedBy** `Consistency gate` **blockedBy** `Image-localize`.

## 1. Image-localize

Dispatch the `image-localizer` for this volume. It scans `Source/Volume N/images/`, identifies text-bearing illustrations, and writes zero-hallucination specs (verbatim JP + glossary-consistent EN + edit prompt) to `Editing/Volume N/image-localization/`. It reports which images bear text and which are clean. Verify the spec files exist on disk.

## 2. User render step (manual pause)

Surface the list of text-bearing images and their specs to the user; the user renders the 1–3 localized images into `English/Volume N/localized-images/`. Wait for the user's confirmation before continuing — or proceed with the originals if the user opts to skip, noting that in the report. Do not build past this pause on your own.

## 3. Consistency gate (whole volume)

Before building, run the whole-volume consistency gate on the filed chapters, substituting the real volume number:

```bash
python core/scripts/check_consistency.py --glossary glossary.md --all "English/Volume N"
```

This is a build gate because a glossary revision after a chapter was filed can leave name/term/honorific drift the per-chapter gate never re-checked, and the EPUB packages exactly these chapters. If it exits non-zero, stop — report the offending lines and get them fixed (via `/translate-chapter`'s editor path) before building; do not package an inconsistent volume.

## 4. Build + verify

Dispatch the `epub-builder`. It runs the **derive→build→verify invocation** from `core/guides/epub-build-spec.md` §Build Invocation — derive the JSON config from `novel.config.md`, then build and verify against that JSON (the scripts understand only the derived JSON, never `novel.config.md` directly):

```bash
python core/scripts/derive_build_config.py novel.config.md --volume N
python core/scripts/build_epub.py  --config "Editing/Volume N/build_config.json"
python core/scripts/verify_epub.py --config "Editing/Volume N/build_config.json"
```

`derive_build_config.py` warns to stderr about any chapter-title-map row whose assembled `.md` is missing under `English/Volume N/` and exits 2 if it finds zero chapters — the builder reads that stderr before trusting the build. The builder self-verifies every gate in `epub-build-spec.md` §Verification Gates from the `verify_epub.py` output (mimetype present/first/STORED · spine LTR · references resolve · zero macrons · zero stray CJK in prose · popup footnotes paired · `<h1>`/TOC/contents-image titles from the config map). On any failing gate it does not mark the task done and reports the offending detail.

## 5. Close

Confirm the `.epub` exists on disk and every gate is green. `SendMessage` the teammates a shutdown. Report: the output `.epub` path, the image-localization summary (text-bearing vs clean), the consistency-gate result, and the per-gate build results.
