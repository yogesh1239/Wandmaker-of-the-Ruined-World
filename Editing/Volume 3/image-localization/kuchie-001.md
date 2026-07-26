# Image Localization Spec — kuchie-001.jpg

## Source image path and type

- Source: `English/Volume 3/images/kuchie-001.jpg`
- Type: illustrated title page; JPEG, 1440 × 2048

## Verbatim Japanese

1. Main pink title in the lower white panel:
   - `崩壊世界の魔法杖職人`
2. Volume number inside the pink circle:
   - `3`
3. Author credit at the bottom:
   - `黒留ハガネ`
4. Illustrator credit at the bottom after the printed English role label `Illustrator`:
   - `かやはら`
5. Existing small pink English subtitle:
   - `Wandmaker of the Ruined World`

## English Localization

1. Main title:
   - `Wand Maker of the Ruined World`
2. Volume number:
   - `3`
3. Author:
   - `Kurodome Hagane`
4. Role label:
   - `Illustrator`
5. Illustrator:
   - `Kayahara`
6. Replace the incorrect existing alias with:
   - `Wand Maker of the Ruined World`

## Edit Prompt

Edit `English/Volume 3/images/kuchie-001.jpg` as the image-edit target. Preserve the complete 1440 × 2048 portrait canvas, white margins, crop, central illustration, all three characters, faces, eyes, anatomy, poses, clothing, objects, table, cups, chair, windows, lighting, palette, texture, and every non-text artwork detail exactly.

Change text only in the lower white title/credit panel:

- Replace the large pink Japanese title `崩壊世界の魔法杖職人` with the exact title `Wand Maker of the Ruined World`.
- Preserve the exact volume numeral `3` in its small pink circular mark beside the title.
- Replace the existing incorrect subtitle `Wandmaker of the Ruined World` with the exact text `Wand Maker of the Ruined World`.
- Replace `黒留ハガネ` with `Kurodome Hagane`.
- Preserve the separate role label `Illustrator`.
- Replace `かやはら` with `Kayahara`.

Title treatment: keep the title entirely inside the lower white panel. Set `Wand Maker of the Ruined World` in an elegant high-contrast pink display serif matching the original title's scale, color, refinement, and horizontal hierarchy. Use one balanced horizontal line if it fits comfortably; otherwise use two phrase-based lines with `Wand Maker` above `of the Ruined World`. Keep the circled `3` optically aligned at the end of the title. Do not let text enter the illustration.

Subtitle treatment: set the second exact title occurrence as a much smaller pink small-cap or letter-spaced serif line directly beneath the main title, matching the source subtitle hierarchy. It must remain clearly subordinate and must spell `Wand Maker` as two words.

Credit treatment: use the bottom white negative space. Set `Kurodome Hagane` and `Illustrator Kayahara` as a centered, restrained pink credit line in a thin clean sans serif. Keep `Illustrator` visually separate as the role label while preserving the original order.

Every quoted string is verbatim copy. Require exact capitalization and spacing: `Wand Maker of the Ruined World`, `3`, `Kurodome Hagane`, `Illustrator`, and `Kayahara`. Permit no paraphrase, omission, duplication beyond the two intentional title occurrences, invented text, or the alias `Wandmaker`.

All English must be upright, horizontal, and left-to-right. Forbid vertical English, rotated words, one-letter-per-line stacking, mirrored text, generic subtitle styling, meme captions, and unrequested boxes. Use professional kerning, leading, optical alignment, balanced line lengths, and natural phrase-based wrapping. Do not clip or overlap any text.

Before returning the edit, perform visual QA: confirm every required string is exact; no targeted Japanese or `Wandmaker` remains; the main title and credits stay entirely in the white panel; no extra text appears; and the illustration is unchanged.

## Notes / Uncertainties

- All listed text is legible.
- `Kurodome Hagane` and the title are locked by `novel.config.md`.
- `Wand Maker` is the mandatory glossary form; `Wandmaker` is banned.
- `Kayahara` is the direct no-macron romanization of `かやはら`.
