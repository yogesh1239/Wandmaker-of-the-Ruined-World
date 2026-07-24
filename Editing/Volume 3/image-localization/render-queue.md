# Volume 3 Remaining Render and Reference Queue

This queue is a handoff for a rendering-capable worker. The image-localizer did
not edit or generate image binaries.

## Priority 1 — revise an existing failed render

1. `p057.jpg` → revise `English/Volume 3/localized-images/p057.png`.
   Keep `Huh?` on one line, but center it horizontally and vertically inside the
   lower-left rectangular speech field. Change nothing else. Re-run a fresh
   visual verifier against source/spec/output and append the result to
   `verification-ledger.md`.

## Priority 2 — text-bearing images referenced by current English Markdown

These originals are still referenced and need localized copies before their
Markdown paths may be swapped:

| Image | Current reference | State |
|-|-|-|
| `s-h1.jpg` | Chapter 19 | Exact title/branding replacements specified; render after applying the revised spec. |
| `s-h2.jpg` | Chapter 19 | **Blocked:** advertising/creator-profile text is untranscribed. Preserve source until an authoritative transcription and English rendering exist. |
| `s-p003.jpg` | Chapter 19 | Booklet contents labels are grounded in `Source/Volume 3/22 Contents.md`; render-ready after the worker verifies every visible label/page number against the image. |
| `allcover-001.jpg` | Chapter 20 | **Blocked for full localization:** title is grounded, but peripheral cover text remains untranscribed. Do not produce a partially guessed render. |

After each output passes fresh visual QA, change only its corresponding Markdown
reference from `images/<name>.jpg` to
`localized-images/<rendered-name>`.

## Priority 3 — omitted source front matter

The source front matter contains `kuchie-003.jpg`, `kuchie-004.jpg`,
`p010.jpg`, and `p011.jpg`, but `English/Volume 3/Front Matter.md` currently
omits them.

- `kuchie-003.jpg`, `kuchie-004.jpg`: **blocked**; multiple labels/captions are
  untranscribed.
- `p010.jpg`, `p011.jpg`: **blocked for full localization**; the roster heading
  is grounded on `p010`, but the character labels/descriptions across both pages
  require authoritative transcription and glossary/character-reference
  grounding.

Once localized and verified, insert all four in source order between
`kuchie-002` and `kuchie-005` (`kuchie-003`, `kuchie-004`) and between
`titlepage` and `toc-001` (`p010`, `p011`).

## Priority 4 — source-spine promotional and booklet pages

### Promotional/back-matter spreads

- `p292-293.jpg`: **blocked for full localization**; `次巻予告` and the release
  date are transcribed, but the central promotional copy is not.
- `p294-295.jpg`: **blocked**; promotional headings/captions are untranscribed.
  The QR code must remain pixel-identical.
- `s-h1-4.jpg`: partially specified; small promotional text remains
  untranscribed.
- `s-h3.jpg`: intentional Japanese colophon; retain unchanged.

### Booklet profile/reference pages

- `s-p004.jpg`–`s-p034.jpg`: **blocked for full localization** except for the
  individually transcribed headings/names in their specs. Dense statistics,
  labels, body prose, timeline rows, guide text, and commentary require
  authoritative transcription and glossary-consistent English before a
  fully-English render.
- `s-p035.jpg`–`s-p038.jpg`: transcription and finalized English are already
  grounded by the exact ranges named in each spec. These four are render-ready,
  but the renderer must map the finalized English to the correct source page
  without moving text across page boundaries.

The EPUB builder must derive the original spine and explicitly decide where
these source-spine pages live. Do not silently drop them merely because they are
not referenced by the current configured chapter Markdown.

## Explicit no-render / preserve-original assets

- Verified clean illustrations: `p024.jpg`, `p042.jpg`, `p089.jpg`,
  `p110.jpg`, `p135.jpg`, `p174.jpg`, `p219.jpg`, `p227.jpg`.
- Existing English trademark with no Japanese replacement:
  `i-bookwalker.jpg`.
- Punctuation-only illustration: `p284.jpg` (`・・・` remains unchanged).
- Intentional Japanese colophon: `s-h3.jpg`.
- Isolated glyph assets with no recoverable positioned context:
  `gaiji-0000.png`–`gaiji-0007.png`.

Preserve these source pixels exactly. Existing source-identical copies are not
localized renders and do not require synthetic re-rendering.

## Required grounding before any blocked page becomes render-ready

1. Transcribe visible Japanese verbatim, region by region. Uncertain characters
   remain noted and unchanged; never fill a gap by inference.
2. Search each name, title, place, label, and technical term (including variants)
   across `glossary.md`, `character-reference.md`, `character-voices.md`,
   `style-guide.md`, and filed `English/Volume 3` chapters.
3. Read the surrounding glossary/profile/prose usage and use the locked
   rendering exactly. Do not consult `reference-archive.md`.
4. Update the corresponding spec before rendering. The edit prompt must list
   only verified source regions and exact English replacements.

## Per-image gates

- Exact source pixel dimensions.
- Exact spec text; no additions, omissions, substitutions, or guessed glyphs.
- Source position, hierarchy, color, weight, alignment, line/paragraph breaks,
  and artwork preserved under `Editing/image-localization-typesetting-style.md`.
- Full-scale and thumbnail visual inspection.
- Fresh low-reasoning verifier PASS recorded in `verification-ledger.md` after
  every new or revised binary.

## Reference and volume gates

1. Every English Markdown image reference resolves on disk.
2. Every text-bearing source-spine image is either a verified localized swap or
   an explicit preserve-original exception above.
3. No clean illustration is altered.
4. No text-bearing source original remains referenced where a verified
   localized output exists.
5. Run the Volume 3 romanization/consistency gates after Markdown reference
   edits, then derive/build/verify the EPUB so image count, dimensions, manifest,
   spine, and all XHTML image references are checked together.
