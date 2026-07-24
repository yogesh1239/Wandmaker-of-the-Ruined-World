# Volume 3 Localized-Image Verification Ledger

## Verification protocol

- Verifier: fresh low-reasoning read-only agent, dispatched with no inherited task context.
- Comparison set: source image, per-image localization spec, localized output, and `Editing/image-localization-typesetting-style.md`.
- Checks: exact English text, spelling, completeness, placement, hierarchy, line breaks, contrast, artwork preservation, cropping, thumbnail readability, and source/output pixel dimensions.
- Verification date: 2026-07-24.

## Results

| Output | Dimensions | Result | Evidence |
|-|-|-|-|
| `cover.png` | 1800×2560; matches source | PASS | Exact title, author, illustrator label/name, and volume numeral; duplicate Japanese title removed; artwork and circle preserved; no stray Japanese or crop. |
| `titlepage.png` | 1440×2048; matches source | PASS | Exact single rotated title, volume numeral, and credits; duplicate edge logotype removed; hierarchy, white field, and placement preserved. |
| `toc-001.png` | 1440×2048; matches source | PASS | All 18 titles, page numbers, and illustration credit exact and ordered; tab stops, leader rules, spacing, margins, and `Contents` preserved. |
| `kuchie-001.png` | 1440×2048; matches source | PASS | Exact sole title, volume numeral, and full credit line; duplicate subtitle removed; pale-pink hierarchy and title-band geometry preserved. |
| `kuchie-002.png` | 2048×1473; matches source | PASS | Exact three-line callout and canonical labels; Japanese duplicates removed; character, food, clothing, sparks, window, and background preserved. |
| `kuchie-005.png` | 1440×2048; matches source | PASS | Exact `Pen` annotation and corrected two-line title; other illegible board marks untouched; paper texture and artwork preserved. |
| `p057.png` | 1438×2048; matches source | PASS | Revised `Huh?` is exact, on one line, and centered horizontally and vertically in the lower-left rectangular field; panel art remains intact. |
| `p266.png` | 1492×2048; matches source | PASS | Exact chart title, axes, and terminal `~`; chart bars, grid, ticks, numbers, frame, spacing, and geometry preserved. |
| `s-h1.png` | 1440×2048; matches source | PASS | Exact booklet titles and branding; 82 px T1 / 51–58 px T2 hierarchy; source paper, lantern, wand, seal, and untouched regions preserved. |
| `s-p003.png` | 1441×2048; matches source | PASS | All specified contents entries and page numbers exact; blue hierarchy, leaders, header, margins, and background preserved. |
| `s-p035.png` | 1441×2048; matches source | PASS | Exact story header/title and English lines 1–39; line 39 split at the source page break; ruby visible; 28 px T4 body; yellow bands preserved. |
| `s-p036.png` | 1441×2048; matches source | PASS | Exact line-39 continuation through line 79; ruby visible; 28 px T4 body; yellow bands and page number preserved. |
| `s-p037.png` | 1441×2048; matches source | PASS | Exact English lines 81–117; ruby visible; 28 px T4 body; yellow bands and page number preserved. |
| `s-p038.png` | 1441×2048; matches source | PASS | Exact English lines 119–171; Translator Note excluded; ruby visible; 28 px T4 body; yellow bands and page number preserved. |

## Current disposition

- Verified usable outputs: **14**.
- Failed outputs awaiting revision: **0**.
- Remaining text-bearing assets are being transcribed and rendered from the
  full-resolution source; this ledger is updated only after each fresh visual
  verifier PASS.
- A PASS applies only to the exact committed binary inspected. Any later edit invalidates that row and requires a new fresh-verifier entry.
