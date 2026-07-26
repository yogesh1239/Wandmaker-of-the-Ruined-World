# Image Localization Spec — titlepage.jpg

## Source

- Image: `Source/Volume 2/images/titlepage.jpg`
- Type: front-matter title page (half-title / bastard title), text-only
- Canvas: 1439 × 2048 JPEG, portrait
- Output: `English/Volume 2/localized-images/titlepage.jpg`
- Wording authority: `novel.config.md` (locked EN title, locked author romanization), the filed front-matter precedent in `Editing/Volume 1/image-localization/frontmatter/image_rsrc4ZW.md` and `Editing/Volume 3/image-localization/cover.md`, and the visible source page
- Page furniture: flat mid-grey field (measured `#727272` / RGB 114,114,114, uniform edge to edge with no gradient or vignette), no illustration, no rules, no page number, no colour band of any kind. Along the extreme left edge, bold widely letterspaced dark-brown (measured RGB 32,24,22) slab-serif Latin display lettering is rotated 90° counter-clockwise to read bottom-to-top, set directly on the grey field with its letterforms running off the trim edge so the left side of every glyph is cropped; the surviving ink occupies only about x = 0–55 of the 1439 px width. All Japanese is set vertically, right-to-left, in a thin white serif (Mincho): the oversized main title occupies the right-of-centre column, a small letterspaced subtitle column sits to its left, and the two credit columns sit further left again. A hand-drawn irregular white circle enclosing a bold white numeral `2` terminates the main-title column.

## Verbatim Japanese by Visual Region

### Main title column (large, right of centre)

崩壊世界の魔法杖職人

### Volume mark (below the main-title column, inside a hand-drawn circle)

2

### Subtitle column (small, immediately left of the title)

小冊子付き特装版

### Author credit column

黒留ハガネ

### Illustrator credit column (Latin role label already printed, rotated)

Illustrator
かやはら

### Left-edge vertical lettering (already Latin, rotated bottom-to-top, no band behind it)

Wandmaker of the Ruined World

## Exact English

### Main title

Wand Maker of the Ruined World

### Volume mark

2

### Subtitle

Special Edition with Booklet

### Author credit

Kurodome Hagane

### Illustrator credit

Illustrator
Kayahara

### Left-edge vertical lettering

Wand Maker of the Ruined World

## Production Edit Prompt

Use case: text-localization of the supplied source image. Treat the supplied image as the edit target. This is a text-only front-matter title page: there is no illustration to protect, but the page's restrained typographic design must be preserved and must read as an official English edition's title page.

Preserve exactly: the portrait canvas and aspect ratio, the flat mid-grey background field (`#727272`) covering the whole page edge to edge with no gradient, texture, vignette, or added artwork, the thin white serif letterforms, and the hand-drawn irregular white circle enclosing the numeral `2`. The page has no coloured band, stripe, bar, panel, or border anywhere: do not add one, and in particular do not place any dark bar along the left edge. Add no rules, boxes, frames, ornaments, logos, page numbers, or decorative flourishes that are not in the source.

Remove every Japanese glyph. Re-set the page as upright, horizontal, left-to-right English, centred on the page's horizontal axis, in this vertical order:

1. `Wand Maker of the Ruined World` — the main title, large, thin white serif matching the source's high-contrast Mincho-like weight and its hairline strokes. Set it as two balanced centred lines, `Wand Maker` over `of the Ruined World`, with the first line at the larger optical weight. This is the page's dominant element and must occupy roughly the upper-middle third.
2. The hand-drawn irregular white circle enclosing the bold white numeral `2` — carried over from the source unchanged in style, scale, and hand-drawn wobble, centred directly beneath the title block.
3. `Special Edition with Booklet` — small, white, generously letterspaced, clearly subordinate to the title, centred beneath the circled numeral.
4. `Kurodome Hagane` — the author credit, small white serif, centred, in the lower third, set larger than the role label below it.
5. `Illustrator` — a smaller white role label on its own line beneath the author credit, matching the source's thin sans-serif Latin role label and its wide letterspacing.
6. `Kayahara` — the illustrator name, centred directly beneath the `Illustrator` label, at the same size as the author credit.

Left-edge vertical lettering: keep the existing bold widely letterspaced dark-brown (RGB 32,24,22) slab-serif Latin display lettering exactly where and as it is — rotated 90° counter-clockwise to read bottom-to-top, set directly on the grey field with no band, stripe, or panel behind it, spanning almost the full page height, and running off the left trim edge so the left side of each glyph is cropped and only a narrow sliver of ink (about 55 px of the 1439 px width) remains visible. Preserve its position, orientation, size, weight, colour, letterspacing, and edge crop. Change only its wording, from `Wandmaker of the Ruined World` to `Wand Maker of the Ruined World`, splitting the single word into two words with one space and capitalizing the `M`. Do not re-typeset, re-orient, recolour, rescale, move, un-crop, add a background to, or restyle this lettering, and do not duplicate it anywhere else on the page.

Render every English string verbatim with exact capitalization and spacing: `Wand Maker of the Ruined World`, `2`, `Special Edition with Booklet`, `Kurodome Hagane`, `Illustrator`, `Kayahara`. The alias `Wandmaker` as one word must not appear anywhere in the finished page. Do not paraphrase, omit, duplicate, abbreviate, translate, invent, or garble text. Do not add a subtitle, tagline, publisher name, series label, or any text not listed above.

Typography: professional kerning, optical centring, balanced line lengths, and generous even leading. Keep every element clearly separated by whitespace, with the hierarchy title > volume mark > subtitle > author > role label > illustrator. No Japanese, no vertical English or rotated English anywhere except the pre-existing left-edge lettering described above, no one-letter-per-line stacking, mirrored text, condensed or crushed type, automatic word hyphenation, overlap, clipping, watermarks, added captions, or decorative artwork.

## Editing and Refinement Record

- **Pass A: complete.** Transcribed all six regions from full-resolution crops. Verified the credit block at 4× — the Latin role label reads `Illustrator` and is rotated with the vertical Japanese, and the author column carries no role label of its own, so none was invented for the English. Verified the subtitle column glyph by glyph at 3×: 小冊子付き特装版. Verified the volume mark at 4× as a bold `2` inside a hand-drawn wobbling circle, not a typeset circled-digit glyph. Verified the left-edge band by de-rotating it: it already reads Latin `Wandmaker of the Ruined World`. Applied the locked forms from `novel.config.md`: 崩壊世界の魔法杖職人 → `Wand Maker of the Ruined World` (line 7), 黒留ハガネ → `Kurodome Hagane` (line 10). Applied the established filed romanization かやはら → `Kayahara`, which is used consistently across the Volume 1 front-matter and booklet specs and the Volume 3 cover and frontispiece specs. Rendered 小冊子付き特装版 as `Special Edition with Booklet`, matching the wording `novel.config.md` line 124 already uses for this edition. Confirmed the alias `Wandmaker` is banned by the filed Volume 3 cover spec and corrected the left-edge band accordingly.
- **Pass B: complete.** Reread the page as a finished English title page rather than a translated one. Reordered the source's right-to-left vertical columns into the conventional English top-to-bottom title-page hierarchy (title → volume mark → edition line → author → illustrator) instead of preserving the Japanese column positions, which would leave English credits floating mid-page with no rationale. Chose the `Wand Maker` / `of the Ruined World` two-line break because it splits the title at its natural phrase boundary and gives two lines of comparable optical width. Kept `Special Edition with Booklet` in title case as an edition line rather than expanding it into a sentence. Kept `Illustrator` as a discrete role label on its own line, matching both the source layout and the filed front-matter precedent, rather than collapsing it to `Illustrator: Kayahara`. Exact English and the production prompt carry identical wording.

## Notes and Uncertainties

- The source page is entirely typographic; no artwork, character, or focal detail is at risk, so the whole page is a type-reset rather than a text-replacement-over-art edit.
- The source's vertical right-to-left column order is deliberately not preserved. Reading order is remapped to the standard English title-page stack, because a literal column-position transfer would produce an English page that no English edition would have designed.
- The left-edge Latin lettering is the one deliberate exception to the horizontal-English rule. It is source-original ornamental display lettering that is already Latin, it functions as a compositional edge element rather than as copy to be read, it is the page's only dark mass, and the required change is one space plus one capital. Re-typesetting it horizontally would destroy the page's balance; the filed Volume 3 cover spec sets the same precedent of correcting this alias in place. Recorded here as an intentional, documented deviation.
- **Corrected mid-task:** the first version of this spec described the left edge as a solid dark full-height band. That was wrong. Column-by-column ink measurement of the source shows dark pixels only in roughly x = 0–55, with flat grey (114,114,114) resuming immediately at x ≈ 20 between glyph strokes, so there is no band — only cropped lettering on the open grey field. The error propagated into the first production prompt and the first render, which duly invented a black bar. Both the spec and the prompt are now corrected.
- `Kayahara` remains the project's direct no-macron romanization of かやはら. No independently locked English illustrator entry exists in the project references, so this carries forward the spelling already filed across Volumes 1 and 3 rather than introducing a new one.
- No illegible regions. Every Japanese string has one certain, source-supported English rendering.

## Render and QA Record

### Round 1 — rejected

- Two renders were produced against the first, faulty version of the prompt. The second was self-accepted by the generator.
- Independent QA rejected it. Body typography, the two-line title break, the circled `2`, the edition line, both credits, and the corrected two-word left-edge wording were all exact, and the grey field measured a genuinely flat 114,114,114 at all four corners. The defect was structural: the render carried a solid dark bar filling x = 0–95 at full page height, an element that does not exist in the source. Measured against the source at y = 1000, the render reads (31,23,21) continuously across x = 20–90 where the source reads flat grey (~118).
- Root cause was this spec, not the generator: the first draft mis-described the cropped left-edge lettering as a dark band, and the generator reproduced what it was told. Spec and prompt corrected before re-rendering.

### Round 2 — accepted

- Re-rendered from the corrected prompt in image-edit mode against the original `titlepage.jpg`. The model correctly removed every Japanese glyph, set the complete English title-page stack, preserved the hand-drawn circled `2`, corrected the left-edge wording to the two-word `Wand Maker`, and did not recreate the rejected solid bar.
- The raw edit introduced a slight neutral-grey vignette. Because this page is purely typographic, the accepted render received a deterministic flat-field cleanup: all non-lettering pixels were reset to exact RGB 114,114,114; the generated white horizontal typography and the cropped dark-brown left-edge glyph strokes were retained. No text, geometry, wording, or source file was altered by that cleanup.
- **Accepted.** Full-resolution visual inspection confirmed the exact visible strings `Wand Maker of the Ruined World`, `2`, `Special Edition with Booklet`, `Kurodome Hagane`, `Illustrator`, and `Kayahara`; no Japanese, one-word `Wandmaker`, extra text, clipping, overlap, or unintended decoration remains. The only rotated English is the documented left-edge title. Region bboxes remain inside the canvas: title `(245,487)–(1288,778)`, circle `(674,893)–(842,1062)`, edition line `(399,1136)–(1148,1178)`, and credits `(544,1396)–(998,1631)`.
- Saved as a real baseline RGB JPEG at exactly 1439 × 2048, quality 95, 4:4:4 chroma sampling (`PIL sampling = 0`). Background samples far from text all read `(114,114,114)`. At `y = 1900`, samples at `x = 20, 40, 60, 80, 120, 400, 1200` read `(112,114,113)`, `(114,114,114)`, `(114,114,114)`, `(114,114,114)`, `(114,114,114)`, `(114,114,114)`, `(114,114,114)` respectively; the tiny first-sample deviation is JPEG bleed adjacent to a cropped dark glyph, not a bar. Dark-pixel coverage ends by `x = 65`, and columns `x = 70, 80, 90` contain zero dark pixels over the full page height.

### Independent QA (not the generator's self-report)

- Re-measured the delivered file directly rather than trusting the render report. `PIL` reports `JPEG RGB (1439, 2048)`. Per-column dark-pixel counts sampled every 4th row confirm ink at x = 0–65 and exactly zero dark pixels at x = 70, 80, and 95, so the rejected bar is genuinely absent rather than merely lightened. At y = 1900 the row reads 34 at x = 0 (a glyph stroke) and 113/112/114/114/114/114/114/114 across x = 10–1435.
- De-rotated the left edge and read it at full width: it reads `Wand Maker of the Ruined World`, two words with a capital `M`, in the source's bold widely letterspaced dark-brown slab serif, sitting on open grey with nothing behind it.
- Read the credit block at 2× and confirmed `Kurodome Hagane`, the letterspaced role label `Illustrator` with its capital `I`, and `Kayahara`.
- One cosmetic difference from the source, accepted rather than re-rendered: the source's edge lettering is trimmed by the page edge so each glyph loses part of its left side, while the render's glyphs sit essentially complete within x = 0–65. This is marginally more legible and does not change the page's character.
- `git status --porcelain "Source/Volume 2/images/"` is clean; the original is unmodified.
