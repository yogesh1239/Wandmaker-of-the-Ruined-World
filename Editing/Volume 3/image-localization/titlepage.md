# titlepage.jpg — Volume 3 front-matter title page

## Source

- **Path:** `Source/Volume 3/images/titlepage.jpg`
- **Type:** front-matter title page (half-title), text-only. No illustration.
- **Canvas:** 1440 × 2048.
- **Output:** `English/Volume 3/localized-images/titlepage.jpg`
- **Wording authority:** `novel.config.md` (locked EN title line 7, locked author romanization line 10), and the accepted `Editing/Volume 2/image-localization/titlepage.md` / `English/Volume 2/localized-images/titlepage.jpg`.

### Measured geometry

| Element | Measurement |
|-|-|
| Field | flat pure white RGB(255,255,255), edge to edge, no gradient, band, rule or page number |
| Main title column | x 690–791, y 232–1626, vertical; 10 glyph runs plus the volume mark |
| Volume mark | the 11th run in that column, y 1529–1626 — a bold numeral inside a hand-drawn irregular circle, not a typeset circled-digit glyph |
| Author column | x 421–467, y 868–1138 |
| Illustrator role label | x 378–396, y 868–1023 — already Latin, rotated with the vertical Japanese |
| Illustrator name column | x 328–364, y 868–1043 |
| Body ink colour | warm near-black, mean RGB(57,49,47) on the title column |
| Left-edge lettering | x 0–59, y 0–2040; uniform light grey RGB(198,198,198), bold widely letterspaced slab-serif Latin, rotated 90° counter-clockwise to read bottom-to-top, running off the trim edge so each glyph's left side is cropped |

**This page has no subtitle column.** Volume 2's title page carries `小冊子付き特装版` → "Special Edition with Booklet"; Volume 3's does not. Column-run measurement finds exactly four ink columns plus the left edge. Do not carry Volume 2's edition line over.

**This page is white with dark text.** Volume 2's title page is a flat mid-grey field with white type. That grey belongs to Volume 2's own source, not to the series template — do not carry it over.

---

## Verbatim Japanese by region

### Main title column (large, right of centre)
```
崩壊世界の魔法杖職人
```

### Volume mark (below the title column, inside a hand-drawn circle)
```
3
```

### Author credit column
```
黒留ハガネ
```

### Illustrator role label (already Latin, rotated)
```
Illustrator
```

### Illustrator name column
```
かやはら
```

### Left-edge vertical lettering (already Latin, rotated bottom-to-top, cropped at the trim)
```
Wandmaker of the Ruined World
```

---

## Exact English by region

### Main title
```
Wand Maker of the Ruined World
```
Set as two centred lines: `Wand Maker` over `of the Ruined World`.

### Volume mark
```
3
```

### Author credit
```
Kurodome Hagane
```

### Illustrator role label
```
Illustrator
```

### Illustrator name
```
Kayahara
```

### Left-edge vertical lettering
```
Wand Maker of the Ruined World
```

---

## Terminology decisions

| Source | English | Basis |
|-|-|-|
| 崩壊世界の魔法杖職人 | Wand Maker of the Ruined World | locked EN title, `novel.config.md` line 7 |
| 黒留ハガネ | Kurodome Hagane | locked author romanization, `novel.config.md` line 10; family name first, no macron |
| かやはら | Kayahara | the project's filed romanization across the Volume 1 front matter and the Volume 3 cover spec; no macron |
| `Wandmaker` (source's own left-edge lettering) | `Wand Maker` | the one-word form is a banned alias of the locked title. Corrected in place, as the accepted Volume 2 title page does — one added space and one capital, with no other change to the lettering |

---

## Production prompt

> Text-localization of the supplied source image. Treat the supplied image as the edit target. This is a text-only front-matter title page: there is no illustration to protect, but the page's restrained typographic design must be preserved and must read as an official English edition's title page.
>
> **Preserve exactly:** the portrait canvas and aspect ratio, and the flat pure-white field RGB(255,255,255) covering the whole page edge to edge with no gradient, texture, vignette, band, stripe, panel, border or added artwork. The page has no coloured band anywhere — do not add one, and in particular do not place any bar along the left edge. Add no rules, boxes, frames, ornaments, logos, page numbers or flourishes absent from the source.
>
> **The type is dark on white.** Body ink is a warm near-black, measured RGB(57,49,47) on the title column. Do not invert the page, and do not reproduce Volume 2's grey field — that grey is specific to Volume 2's own source.
>
> Remove every Japanese glyph. Re-set the page as upright, horizontal, left-to-right English, centred on the page's horizontal axis, in this vertical order:
>
> 1. `Wand Maker of the Ruined World` — the main title, large, in a high-contrast serif matching the source's thin Mincho-like hairlines. Set as two balanced centred lines, `Wand Maker` over `of the Ruined World`. This is the page's dominant element and should occupy roughly the upper-middle third.
> 2. The hand-drawn irregular circle enclosing a bold numeral `3` — carried over from the source unchanged in style, scale and hand-drawn wobble, centred directly beneath the title block. It is a drawn circle, not a typeset circled-digit character.
> 3. `Kurodome Hagane` — the author credit, small serif, centred, in the lower third, set larger than the role label below it.
> 4. `Illustrator` — a smaller role label on its own line beneath the author credit, matching the source's thin sans-serif Latin label and its wide letterspacing.
> 5. `Kayahara` — the illustrator name, centred directly beneath the `Illustrator` label, at the same size as the author credit.
>
> **Do NOT add an edition line, subtitle, tagline, publisher name or series label.** Volume 2's title page carries "Special Edition with Booklet"; this page has no such column and must not gain one.
>
> **Left-edge vertical lettering:** keep the existing bold widely letterspaced light-grey RGB(198,198,198) slab-serif Latin display lettering exactly where and as it is — rotated 90° counter-clockwise to read bottom-to-top, set directly on the white field with no band or panel behind it, spanning almost the full page height, and running off the left trim edge so each glyph's left side is cropped and only about 60 px of the 1440 px width shows ink. Preserve its position, orientation, size, weight, colour, letterspacing and edge crop. **Change only its wording**, from `Wandmaker of the Ruined World` to `Wand Maker of the Ruined World` — one space added, `M` capitalized. Do not re-typeset, re-orient, recolour, rescale, move, un-crop, add a background to, or restyle this lettering, and do not duplicate it elsewhere on the page.
>
> Render every English string verbatim with exact capitalization and spacing: `Wand Maker of the Ruined World`, `3`, `Kurodome Hagane`, `Illustrator`, `Kayahara`. The alias `Wandmaker` as one word must not appear anywhere in the finished page. Do not paraphrase, omit, duplicate, abbreviate, translate, invent or garble text.
>
> **Typography:** professional kerning, optical centring, balanced line lengths, generous even leading. Keep every element clearly separated by whitespace, with the hierarchy title > volume mark > author > role label > illustrator. No Japanese; no vertical or rotated English anywhere except the pre-existing left-edge lettering described above; no one-letter-per-line stacking, mirrored text, crushed type, automatic hyphenation, overlap, clipping, watermarks or added captions.

---

## Editing and refinement record

### Pass A — source and continuity edit

- Transcribed all six regions from full-resolution crops and confirmed the column inventory by ink measurement: exactly four ink columns (x 690–791, 421–467, 378–396, 328–364) plus the left edge. **Verified there is no subtitle column** — the element Volume 2 has and this page does not.
- Verified the title column holds 10 glyph runs plus an 11th at y 1529–1626, the volume mark: a bold numeral inside a hand-drawn wobbling circle, not a typeset circled digit.
- Verified the role label between the credit columns is already Latin `Illustrator`, rotated with the vertical Japanese, and that the author column carries no role label of its own — so none was invented for the English.
- De-rotated the left edge and confirmed it already reads Latin `Wandmaker of the Ruined World`, in uniform grey RGB(198,198,198) with white field resuming between strokes. There is no band.
- Applied locked forms from `novel.config.md`: 崩壊世界の魔法杖職人 → `Wand Maker of the Ruined World` (line 7); 黒留ハガネ → `Kurodome Hagane` (line 10). Applied the filed romanization かやはら → `Kayahara`.
- Measured the field as pure white and the ink as warm near-black, and recorded both explicitly, because the accepted Volume 2 page is the inverse and is the nearest precedent a renderer would reach for.

**Pass A: complete**

### Pass B — publication-English refinement

- Reread as a finished English title page rather than a translated one. The source's right-to-left vertical column order is deliberately not preserved; reading order is remapped to the conventional English title-page stack (title → volume mark → author → illustrator), because a literal column-position transfer would leave English credits floating mid-page with no rationale.
- Chose the `Wand Maker` / `of the Ruined World` two-line break: it splits the title at its natural phrase boundary and gives two lines of comparable optical width. This matches the accepted Volume 2 page, so the two volumes' title pages stack identically.
- Kept `Illustrator` as a discrete role label on its own line, matching both the source layout and the filed front-matter precedent, rather than collapsing it to `Illustrator: Kayahara`.
- Confirmed no edition line is added. Volume 3 is described in `novel.config.md` line 125 as an ebook bonus edition, but the source title page states no edition at all, and inventing one would be adding text.
- Exact English and the production prompt carry identical wording.

**Pass B: complete**

---

## Notes and uncertainties

- The page is entirely typographic; no artwork or focal detail is at risk, so this is a type-reset rather than a text-replacement-over-art edit.
- The left-edge Latin lettering is the one deliberate exception to the horizontal-English rule. It is source-original ornamental display lettering that is already Latin, functions as a compositional edge element rather than as copy to be read, and needs only one space plus one capital. Re-typesetting it horizontally would destroy the page's balance. This follows the documented Volume 2 precedent.
- **Two traps carried by the nearest precedent.** Volume 2's accepted title page is the closest model for this layout, but differs from this source in two ways that would be defects if copied: its field is mid-grey with white type where this one is white with dark type, and it carries an edition line where this page has no subtitle column. Both are called out explicitly in the production prompt.
- Volume 2's spec records that its own first render invented a solid dark left-edge bar because that spec mis-described the cropped lettering as a band. The description here is measurement-based — ink only in x 0–59, white field resuming between glyph strokes — to avoid repeating it.
- No illegible regions. Every Japanese string has one certain, source-supported English rendering.

---

## Render record

- **Rendered:** deterministic Pillow raster composite; no image-generation model. Accepted on the first pass.
- **Output:** `English/Volume 3/localized-images/titlepage.jpg` — real JPEG, 1440 × 2048, RGB, quality 95, 4:4:4.
- **Field QA:** pure white RGB(255,255,255) measured at all four corners and at page centre. No gradient, band or vignette.
- **No left-edge band.** The failure mode recorded on Volume 2 did not recur: 62 % of the x 0–59 strip measures pure white, and sampling confirms the field resumes between glyph strokes — (45,600) reads white in both source and output, while (30,400) carries ink in both. Only cropped lettering, no bar.
- **Left-edge lettering:** modal ink RGB(198,198,198), extent x 0–59 and y 0–2040, same 90° counter-clockwise orientation and trim crop as the source. De-rotated and read back visually: it reads `Wand Maker of the Ruined World`, with the space present and the `M` capitalized. The one-word alias appears nowhere on the page.
- **Body stack:** six ink elements, in order and nothing else — title line 1 y 488–609 (122 px ink), title line 2 y 675–778 (104 px), volume mark y 894–991, author y 1397–1456 (60 px), `Illustrator` y 1520–1542 (23 px), `Kayahara` y 1577–1631 (55 px). Every element centres on x 719.5–720.0 against a 1440 px canvas.
- **Volume mark:** the source's own hand-drawn wobbling circle enclosing a bold `3`, carried over natively at 96 × 97 px — not a typeset circled-digit glyph.
- **Body ink:** modal RGB(57,49,47), matching the source's warm near-black. The page was not inverted to Volume 2's white-on-grey.
- **Content QA:** no edition line or subtitle anywhere, no Japanese character, no extra element. Both Volume 2 traps — the grey field and the inherited edition line — were avoided.
