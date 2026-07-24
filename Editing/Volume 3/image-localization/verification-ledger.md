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
| `p057.png` | 1438×2048; matches source | **FAIL** | `Huh?` is exact and the art is intact, but the text is pinned near the left edge instead of centered horizontally and vertically in the specified lower-left rectangular field. Re-render required. |
| `p266.png` | 1492×2048; matches source | PASS | Exact chart title, axes, and terminal `~`; chart bars, grid, ticks, numbers, frame, spacing, and geometry preserved. |

## Current disposition

- Verified usable outputs: **7**.
- Failed output awaiting revision and fresh re-verification: **1** (`p057.png`).
- A PASS applies only to the exact committed binary inspected. Any later edit invalidates that row and requires a new fresh-verifier entry.
