# Volume 4 Image Verification Ledger

Audit date: 2026-07-24. Source inventory: 70 files.

## Existing Outputs

Independent fresh visual verifier compared source + spec + output and checked text, completeness, placement, hierarchy, artifacts, and canvas dimensions.

| Output | Verdict | Evidence |
|-|-|-|
| `cover.png` | PASS | Exact sole title, volume, and credits; Japanese removed cleanly; source canvas preserved. |
| `titlepage.png` | PASS | Exact title, volume, and credits; sole-title composition and clean white background preserved. |
| `s-h1.png` | PASS | All three replacements exact; no duplicate title; stamp, wand, and texture intact. |
| `s-h2.png` | **FAIL** | Text is complete, but existing small English labels were unauthorizedly retyped as large all-caps labels. |
| `s-h3.png` | VISUAL PASS / POLICY EXCLUDE | Former text replacement is visually exact, but the corrected spec retains the original Japanese colophon/legal page. Do not swap it. |
| `s-p003.png` | PASS | Every entry and numeral exact; order, leaders, blue hierarchy, and margins preserved. |
| `s-p004.png` | PASS | Complete exact text; stats, key, body, art, rules, and page furniture preserved. |
| `s-p005.png` | PASS | Complete exact text; quote, stats, key, one-paragraph body, art, and rules preserved. |
| `s-p006.png` | PASS | Complete exact text and punctuation; placement, hierarchy, and art preserved. |

All nine clean copies have exact source dimensions and are byte-for-byte identical to source: `p022.jpg`, `p048.jpg`, `p068.jpg`, `p111.jpg`, `p116.jpg`, `p142.jpg`, `p196-197.jpg`, `p208.jpg`, and `p271.jpg`. Visual inspection found no Japanese or other translatable baked-in text.

## Complete Source Classification

| Source image(s) | Classification | Required disposition |
|-|-|-|
| `allcover-001.jpg` | Text-bearing, policy-retained | Original |
| `cover.jpg` | Text-bearing, localized | Existing PASS |
| `gaiji-0000.png`–`gaiji-0004.png` | Inline source glyphs | Original |
| `i-bookwalker.jpg` | English-only logo | Original |
| `kuchie-001.jpg`–`kuchie-004.jpg` | Text-bearing, localizable | Missing render |
| `kuchie-005.jpg` | English-only decorative endpaper | Original |
| `p010.jpg` | Text-bearing, partial authorized edit | Missing render |
| `p011.jpg` | Text-bearing, no verified replacement | Original |
| `p022.jpg`, `p048.jpg`, `p068.jpg`, `p111.jpg`, `p116.jpg`, `p142.jpg`, `p196-197.jpg`, `p208.jpg`, `p271.jpg` | Clean illustration | Original; clean copies PASS |
| `p285.jpg`, `p290-291.jpg`, `p292-293.jpg`, `p294-295.jpg` | Text-bearing, no verified complete replacement | Original |
| `s-h1-4.jpg` | Text-bearing, localizable | Missing render |
| `s-h1.jpg` | Text-bearing, localized | Existing PASS |
| `s-h2.jpg` | Text-bearing, localized | Existing FAIL; revise |
| `s-h3.jpg` | Text-bearing colophon/legal | Original by policy |
| `s-p003.jpg`–`s-p006.jpg` | Text-bearing, localized | Existing PASS |
| `s-p007.jpg` | Text-bearing, no verified replacement | Original |
| `s-p008.jpg`–`s-p014.jpg` | Text-bearing, partial authorized edits | Missing renders |
| `s-p015.jpg` | Text-bearing, no verified replacement | Original |
| `s-p016.jpg` | Text-bearing, partial authorized edit | Missing render |
| `s-p017.jpg`–`s-p018.jpg` | Text-bearing, no verified replacement | Original |
| `s-p019.jpg` | Text-bearing, partial authorized edit | Missing render |
| `s-p020.jpg`–`s-p022.jpg` | Text-bearing, no verified replacement | Original |
| `s-p023.jpg` | Text-bearing, partial authorized edit | Missing render |
| `s-p024.jpg`–`s-p025.jpg` | Text-bearing, no verified replacement | Original |
| `s-p026.jpg` | Text-bearing, partial authorized edit | Missing render |
| `s-p027.jpg` | Text-bearing, no verified replacement | Original |
| `s-p028.jpg` | Text-bearing, partial authorized edit | Missing render |
| `s-p029.jpg` | Text-bearing, no verified replacement | Original |
| `s-p030.jpg` | Text-bearing, partial authorized edit | Missing render |
| `s-p031.jpg` | Text-bearing, no verified replacement | Original |
| `s-p032.jpg` | Text-bearing, partial authorized edit | Missing render |
| `s-p033.jpg`–`s-p038.jpg` | Text-bearing, no verified replacement | Original |
| `titlepage.jpg` | Text-bearing, localized | Existing PASS |
| `toc-001.jpg` | Text-bearing, localizable | Missing render |

## Deterministic Checks

- Spec coverage: PASS — 61 text-bearing images have specs; the remaining 9 are enumerated clean illustrations.
- Required spec sections: PASS — every per-image spec contains Source Image Path + Type, Verbatim Japanese, English Localization, Edit Prompt, and Notes / Uncertainties.
- Clean-copy identity: PASS — 9/9 byte-identical to source and visually clean.
- Whole-volume glossary consistency: PASS — `python3 core/scripts/check_consistency.py --glossary glossary.md --all "English/Volume 4"` exited 0.
- Markdown image-marker compatibility: **FAIL** — 16 of 19 current image-marker lines use `localized-images/...`; the builder's block-image parser accepts only `images/...`.
- Chapter 18 booklet completeness: **FAIL** — `s-p007` through `s-p038` are absent.
- Derived image-swap configuration: **FAIL** — the derived Volume 4 JSON contains neither `localized_images_dir` nor `image_swaps`.
