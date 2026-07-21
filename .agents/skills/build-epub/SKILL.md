---
name: build-epub
description: Builds a volume EPUB end to end — image-localize, run the whole-volume consistency gate, build from novel.config.md via the derived JSON, then verify the build gates. Pass the volume number.
---

# build-epub

Build the EPUB for the given volume. The commands, spine mapping, and gate list live in `core/guides/epub-build-spec.md`; this skill orchestrates them and does not restate them.

## Outcome

The volume `.epub` on disk with **every** verification gate green, built from the chapters the per-chapter pipeline (`core/pipeline.md`) filed to `English/Volume N/`, with any text-bearing illustrations localized (or the originals kept with that noted).

## Orchestration

Dispatch the per-stage agents in `.codex/agents/` **by name**: `image-localizer`, `epub-builder`. Subagents are ephemeral and isolated; there is no shared task board, so ordering lives here. This pipeline is mostly sequential (localize → user render → consistency gate → build), so dispatch subagents one stage at a time; dispatch at most **6 concurrently** if a stage ever has independent sub-tasks. Front-load each dispatch with the complete spec (the volume, its `Source/Volume N/images/` directory, the reference files to read). Verify every output **on disk** before treating a step as done. Read `novel.config.md` first for the volume's paths, chapter-title map, reading direction (RTL→LTR), image swaps, and EPUB metadata.

## 1. Image-localize

Dispatch the `image-localizer` for this volume. It scans `Source/Volume N/images/`, identifies text-bearing illustrations, and writes zero-hallucination specs (verbatim JP + glossary-consistent EN + edit prompt) to `Editing/Volume N/image-localization/`, reporting which images bear text and which are clean. Verify the spec files exist on disk.

## 2. User render step (manual pause)

Surface the text-bearing images and their specs to the user; the user renders the localized images into `English/Volume N/localized-images/`. **Wait for the user's confirmation before continuing** — or proceed with the originals if the user opts to skip, noting that in the report. Do not build past this pause on your own.

## 3. Consistency gate (whole volume)

Before building, run the whole-volume gate on the filed chapters (substitute the real volume number):

```bash
python core/scripts/check_consistency.py --glossary glossary.md --all "English/Volume N"
```

The EPUB packages exactly these chapters, and a glossary revision after a chapter was filed can leave name/term/honorific drift the per-chapter gate never re-checked. If it exits non-zero, **stop** — report the offending lines and get them fixed (via the translate-chapter editor path) before building. Do not package an inconsistent volume.

## 4. Build + verify

Dispatch the `epub-builder`. It runs the **derive→build→verify invocation** from `epub-build-spec.md` §Build Invocation — the scripts understand only the derived JSON, never `novel.config.md` directly (substitute the real volume number):

```bash
python core/scripts/derive_build_config.py novel.config.md --volume N
python core/scripts/build_epub.py  --config "Editing/Volume N/build_config.json"
python core/scripts/verify_epub.py --config "Editing/Volume N/build_config.json"
```

`derive_build_config.py` warns to stderr about any chapter-title-map row whose assembled `.md` is missing under `English/Volume N/` and exits 2 on zero chapters — the builder reads that stderr before trusting the build. It then self-verifies every gate in §Verification Gates from the `verify_epub.py` output (mimetype present/first/STORED · spine LTR · references resolve · zero macrons · zero stray CJK in prose · popup footnotes paired · `<h1>`/TOC/contents-image titles from the config map). On any failing gate it does not mark done and reports the offending detail.

## 5. Close

Confirm the `.epub` exists on disk and every gate is green.

## Disposition

Persistence: keep going until the `.epub` is built and every gate passes — or you have a concrete gate failure to report. Scope guard: build only the requested volume; do not re-translate or re-edit chapters — route any content problem back to the translate-chapter path and note it as optional follow-up. Never ask clarifying questions except the one deliberate render pause in step 2.

## Report

The output `.epub` path; the image-localization summary (text-bearing vs clean); the consistency-gate result; and the per-gate build results.
