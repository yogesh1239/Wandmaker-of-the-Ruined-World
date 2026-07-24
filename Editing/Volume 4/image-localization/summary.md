# Volume 4 Image-Localization Summary

## Coverage

- Source images audited: **70**
- Text-bearing images: **61**; each has a spec in this directory.
- Clean illustrations: **9**; all nine were visually verified and are byte-identical to their copies in `English/Volume 4/localized-images/`.
- Required localized outputs under the current specs/policies: **29**
- Required outputs currently passing independent visual verification: **7**
- Existing required output needing revision: **1** (`s-h2.png`)
- Required outputs not yet rendered: **21**
- Text-bearing assets intentionally retained unchanged: **32**

## Text-Bearing

`allcover-001.jpg`, `cover.jpg`, `gaiji-0000.png`, `gaiji-0001.png`, `gaiji-0002.png`, `gaiji-0003.png`, `gaiji-0004.png`, `i-bookwalker.jpg`, `kuchie-001.jpg`, `kuchie-002.jpg`, `kuchie-003.jpg`, `kuchie-004.jpg`, `kuchie-005.jpg`, `p010.jpg`, `p011.jpg`, `p285.jpg`, `p290-291.jpg`, `p292-293.jpg`, `p294-295.jpg`, `s-h1-4.jpg`, `s-h1.jpg`, `s-h2.jpg`, `s-h3.jpg`, `s-p003.jpg` through `s-p038.jpg`, `titlepage.jpg`, and `toc-001.jpg`.

## Clean

`p022.jpg`, `p048.jpg`, `p068.jpg`, `p111.jpg`, `p116.jpg`, `p142.jpg`, `p196-197.jpg`, `p208.jpg`, and `p271.jpg`.

## Required Render / Revision Queue

See `render-queue.md` for the exact 22-file handoff: 21 missing renders plus one revision.

## Retain Original

- Policy: `allcover-001.jpg` and `s-h3.jpg` (Japanese cover-wrap / colophon and legal matter).
- Non-Japanese or already-English-only: `i-bookwalker.jpg` and `kuchie-005.jpg`.
- Inline source glyphs, not standalone illustration regions: `gaiji-0000.png` through `gaiji-0004.png`.
- Text-bearing but no verified complete replacement authorized: `p011.jpg`, `p285.jpg`, `p290-291.jpg`, `p292-293.jpg`, `p294-295.jpg`, `s-p007.jpg`, `s-p015.jpg`, `s-p017.jpg`, `s-p018.jpg`, `s-p020.jpg`, `s-p021.jpg`, `s-p022.jpg`, `s-p024.jpg`, `s-p025.jpg`, `s-p027.jpg`, `s-p029.jpg`, `s-p031.jpg`, and `s-p033.jpg` through `s-p038.jpg`.

The last group remains unchanged because its dense Japanese regions are not fully transcribed with character-level confidence. No English is invented for those regions.

## Integration Status

The whole-volume deterministic consistency gate passes. EPUB image integration is not ready: 16 chapter image markers currently use `localized-images/...`, but `core/scripts/build_epub.py` recognizes only `images/<filename>` markers, and the derived Volume 4 build config currently contains neither `localized_images_dir` nor `image_swaps`. Chapter 18 also stops at `s-h3` and omits `s-p007` through `s-p038`. These requirements are itemized in `render-queue.md` and `verification-ledger.md`.
