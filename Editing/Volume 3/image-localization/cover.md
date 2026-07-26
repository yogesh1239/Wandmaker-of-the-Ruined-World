# Image Localization Spec — cover.jpg

## Source image path and type

- Source: `English/Volume 3/images/cover.jpg`
- Type: front-cover illustration; JPEG, 1800 × 2560

## Verbatim Japanese

1. Main cover title, oversized white brush lettering distributed around the outer edges:
   - `崩壊世界の魔法杖職人`
2. Author credit, upper-left:
   - `黒留ハガネ`
3. Illustrator credit, upper-left beneath the printed English role label `Illustrator`:
   - `かやはら`
4. Volume number, upper-right:
   - `3`
5. Existing small vertical English title near the left-center:
   - `Wandmaker of the Ruined World`

## English Localization

1. Main title:
   - `Wand Maker of the Ruined World`
2. Author credit:
   - `Kurodome Hagane`
3. Illustrator credit:
   - `Kayahara`
4. Volume number:
   - `3`
5. Replace the existing incorrect alias `Wandmaker of the Ruined World` with:
   - `Wand Maker of the Ruined World`

## Edit Prompt

Edit `English/Volume 3/images/cover.jpg` as the image-edit target and produce a finished official-English-edition front cover.

Replace only these text regions:

- Replace the oversized white Japanese brush title `崩壊世界の魔法杖職人` with the exact title `Wand Maker of the Ruined World`.
- Replace `黒留ハガネ` with `Kurodome Hagane`.
- Replace `かやはら` with `Kayahara`, retaining the nearby role label `Illustrator`.
- Preserve the volume number as the exact numeral `3`.
- Replace the existing incorrect vertical English alias `Wandmaker of the Ruined World` with the exact title `Wand Maker of the Ruined World`.

Main-title treatment: preserve the source hierarchy of huge distressed white brush lettering, but typeset the English upright, horizontal, and left-to-right in the existing outer-edge negative space. Use a bold condensed display face with rough hand-painted edges, pure-to-warm white fill, and the same subtle irregular texture. Arrange the exact title as a small number of balanced horizontal phrase blocks—prefer `Wand Maker` / `of the Ruined World`—without rotating words, stacking one letter per line, clipping letters, or covering any face, eye, hand, body, wand, teacup, or other focal detail. Moderately reduce type size before encroaching on the characters.

Credits treatment: use the upper-left negative space. Set `Kurodome Hagane` in a thin, clean white sans serif matching the source author credit. Keep `Illustrator` as a separate smaller white sans-serif role label and place `Kayahara` beneath it in the same restrained credit style. All credit text must be horizontal and left-to-right.

Volume treatment: retain `3` in the upper-right within a thin white circular outline, matching its original scale and placement.

The quoted English is verbatim copy. Preserve exact capitalization and spacing: `Wand Maker of the Ruined World`, `Kurodome Hagane`, `Illustrator`, `Kayahara`, and `3`. Do not paraphrase, omit, duplicate, or invent text.

Preserve the 1800 × 2560 canvas, crop, panel geometry, all three characters, faces, eyes, anatomy, poses, clothing, objects, windows, butterflies, magical effects, lighting, palette, texture, and every non-text artwork detail exactly. Do not repaint, move, crop, extend, recolor, beautify, or redesign the illustration. Use professional kerning, optical alignment, balanced line lengths, and natural phrase-based wrapping. Forbid vertical English, rotated English, one-letter-per-line stacking, mirrored text, generic subtitles, meme captions, and unrequested boxes.

Before returning the edit, perform visual QA: confirm every required string and punctuation mark is exact; no targeted Japanese or the alias `Wandmaker` remains; no extra or duplicated text appears; all English is horizontal LTR; nothing is clipped or overlapping; the original art is undamaged; and the cover plausibly looks originally designed in English.

## Notes / Uncertainties

- All listed Japanese text is legible.
- `Kurodome Hagane` is locked by `novel.config.md`.
- `Wand Maker` is the mandatory glossary rendering; `Wandmaker` is a banned alias and must not remain.
- `Kayahara` is the direct no-macron romanization of `かやはら`.
- The user explicitly requested localization of `cover.jpg`; this output therefore overrides the config's default build-time instruction to retain the Japanese cover, without changing the original file.
