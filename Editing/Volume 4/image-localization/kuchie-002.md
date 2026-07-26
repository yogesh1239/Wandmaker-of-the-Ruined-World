# Image Localization Spec — `kuchie-002.jpg`

## Source

- **Path:** `Source/Volume 4/images/kuchie-002.jpg`
- **Type:** colour frontispiece spread — two panels split by a diagonal, with two character
  nameplates and four vertical dialogue blocks set over the artwork
- **Canvas:** 2048 × 1456 landscape JPEG
- **Output:** `English/Volume 4/localized-images/kuchie-002.jpg`
- **Wording authority:** `English/Volume 4/Chapter 1 - Illness and Recovery.md`, lines 35–43 —
  every line on this plate is a verbatim quotation from that scene. `glossary.md` for the
  nameplates and the terms; the accepted `English/Volume 3/localized-images/kuchie-002.jpg` for the
  nameplate treatment.

### Measured geometry

| Element | Bounds | Notes |
|-|-|-|
| Blue Witch plate — Latin `Blue Witch` | x 168–279, y 683–695 | ink height 13, letterspaced |
| Blue Witch plate — `青の魔女` | x 108–284, y 707–740 | ink height 34, the dominant line |
| Ori plate — Latin `Kenshi Ori` | x ≈ 1306–1450, y ≈ 1108–1124 | letterspaced |
| Ori plate — `大利賢師` | x ≈ 1243–1480, y ≈ 1129–1180 | the dominant line |
| Dialogue R (Hiyori) | x 1774–1949, y 907–1384 | 5 vertical columns, right-to-left |
| Dialogue C1 (Ori) | x ≈ 780–847, y 725–1120 | 1 column |
| Dialogue C2 (Hiyori) | x ≈ 690–760, y 760–1120 | 1 column |
| Dialogue L (Ori) | x 155–472, y 1060–1426 | 8 vertical columns, right-to-left |
| Ellipsis (Hiyori) | x 123–150, y 1126–1262 | 1 short column, leftmost = last |

Ink colours, sampled from dense glyph interiors rather than region means:

| Element | RGB |
|-|-|
| Blue Witch nameplate | (111, 77, 159) violet |
| Ori nameplate | (35, 43, 46) near-black on a teal glow |
| All dialogue | white, with a soft dark outer glow that carries it over both light and dark art |

**Unlike `kuchie-001`, every element here sits over painted artwork.** Clearing the Japanese
requires reconstructing the art beneath it. There is no flat field to repaint.

---

## Verbatim Japanese by region

### Blue Witch nameplate — two tiers, the Latin already present

```
Blue Witch
青の魔女
```

### Ori nameplate — two tiers, the Latin already present

```
Kenshi Ori
大利賢師
```

### Dialogue R — Hiyori

```
「んー。確かにキュアノスも御守り[アミュレット]も青だし……寒色系で合わせるのもアリか。大利的にはどうなんだ？　赤が好きか？　大利の火蜥蜴[ペット]たちの色に合わせるのもアリな気がしてきた」
```

### Dialogue C1 — Ori

```
「なんで俺のペットと色合わせするんだよ」
```

### Dialogue C2 — Hiyori

```
「なんでって……それは……」
```

### Dialogue L — Ori

```
「ヒヨリの目とかスゲー綺麗な青色してるしさあ、髪も青みがかってるし、好みの色が特に無いならペットもヒヨリの持ち味の色彩に合わせた方がハマるんじゃねえの」
```

### Ellipsis — Hiyori

```
「…………」
```

---

## Exact English by region

### Blue Witch nameplate — consolidated to one label

```
Blue Witch
```

### Ori nameplate — consolidated to one label, alias corrected

```
Ori Kenshi
```

### Dialogue R — Hiyori

```
"Hmm. Cyanos and my amulet are both blue, so... going with cool colors might work. What about you, Ori? Do you like red? I'm starting to think matching your fire salamanders' colors could work too."
```

### Dialogue C1 — Ori

```
"Why would you match the colors to my pets?"
```

### Dialogue C2 — Hiyori

```
"Why...? Well..."
```

### Dialogue L — Ori

```
"Your eyes are a really pretty blue, Hiyori, and your hair has a bluish tint too. If you don't have a particular favorite color, wouldn't a pet that matches your own distinctive colors suit you better?"
```

### Ellipsis — Hiyori

```
"............"
```

---

## Terminology decisions

| Source | English | Basis |
|-|-|-|
| 青の魔女 | Blue Witch | `glossary.md`; banned: Blue Mage, Witch of Blue |
| 大利賢師 | Ori Kenshi | `glossary.md`; **`Kenshi Ori` is a banned alias, and the source plate prints it** |
| キュアノス | Cyanos | `glossary.md`; banned: Kyanos |
| 御守り[アミュレット] | amulet | `glossary.md`; the ruby is dropped — see Pass B |
| 火蜥蜴[ペット] | fire salamanders | `glossary.md`; the ruby is dropped — see Pass B |
| ペット (plain, C1) | pets | plain katakana in the source, no ruby to carry |
| ヒヨリ | Hiyori | `glossary.md`, `character-reference.md` |

---

## Layout decision — the dialogue is re-set horizontally, in place

The source runs four blocks of vertical Japanese down the artwork. English cannot be set that way,
so each block is re-set as a horizontal left-aligned paragraph occupying the same negative space its
column ran through. Measured target boxes, chosen so the text lands only on low-detail painted areas
and never on a face, hand, or the book:

| Block | Target box | Lines |
|-|-|-|
| R — Hiyori | x 1540–2020, y 1030–1300 | ~5, over the dark wall and trouser |
| C1 — Ori | x 700–1010, y 745–870 | ~2, over the blurred window |
| C2 — Hiyori | x 700–1010, y 900–985 | 1 |
| L — Ori | x 150–620, y 1100–1330 | ~5, across the blurred lower-left |
| Ellipsis | x 150–330, y 1360–1400 | 1, below L |

Two things change from the source's arrangement and both are deliberate:

**Reading order is rebuilt for a left-to-right reader.** In the source the eye starts at the
right-hand block, moves to the centre columns, then to the lower-left block, and finishes on the
ellipsis at the far left — because Japanese columns run right to left. Reset horizontally, that same
sequence now reads top-right → centre → lower-left → below, which an English reader follows
naturally without any line being moved out of its own panel.

**The ellipsis moves from left of Ori's speech to below it.** In the source it is the leftmost
column, which is *after* the block in Japanese order. Left of it in English would read as *before*.
Set underneath, it keeps its place as Hiyori's silent reply and stays beside her blushing close-up.

---

## Production prompt

**Method: generative image edit.** Every string on this plate sits over painted artwork, so the
flat-ground composite exception does not apply. Render through Codex headless calling `imagegen`
with this image as the edit target — the Japanese lettering is removed and the artwork beneath it
reconstructed as part of the edit, not masked and pasted over.

> **Use case:** text-localization
>
> **Asset type:** Japanese light-novel colour frontispiece spread — two panels split by a diagonal,
> carrying two character nameplates and four blocks of vertical dialogue.
>
> **Input image:** the provided image is the edit target.
>
> **Primary request:** replace every Japanese text element with English, removing the Japanese
> lettering and reconstructing the artwork beneath it naturally, so no trace of the original columns
> remains.
>
> 1. **Blue Witch nameplate**, lower left of the left panel — currently a small Latin line
>    `Blue Witch` stacked over a larger Japanese line `青の魔女` saying the same thing. In English
>    that is one name printed twice. Set the name **once**, occupying the larger line's slot
>    (x 108–284, y 707–740), and clear the small Latin line above it (x 168–279, y 683–695). Keep
>    the source's violet, RGB(111, 77, 159).
> 2. **Ori nameplate**, centre right, glowing on the dark table — currently a small Latin line
>    `Kenshi Ori` stacked over a larger Japanese line `大利賢師`. Same treatment: set the name
>    **once**, occupying the larger line's slot (x ≈ 1243–1480, y ≈ 1129–1180), clear the Latin line
>    above it (x ≈ 1306–1450, y ≈ 1108–1124). Keep the source's near-black RGB(35, 43, 46) and leave
>    the teal glow behind it exactly as it is.
> 3. **Dialogue R** (five vertical columns, x 1774–1949, y 907–1384) → one horizontal left-aligned
>    paragraph in the open dark area around x 1540–2020, y 1030–1300.
> 4. **Dialogue C1** (one column, x ≈ 780–847) → horizontal, x 700–1010, y 745–870.
> 5. **Dialogue C2** (one column, x ≈ 690–760) → horizontal, x 700–1010, y 900–985.
> 6. **Dialogue L** (eight vertical columns, x 155–472, y 1060–1426) → one horizontal left-aligned
>    paragraph, x 150–620, y 1100–1330.
> 7. **Ellipsis** (short column, x 123–150, y 1126–1262) → horizontal, x 150–330, y 1360–1400,
>    sitting below block 6.
>
> **Text invariants (verbatim).** Reproduce these strings exactly, with this capitalization,
> punctuation and spacing. Nothing may be paraphrased, abbreviated, translated, duplicated or
> invented:
>
> - `Blue Witch`
> - `Ori Kenshi`
> - `"Hmm. Cyanos and my amulet are both blue, so... going with cool colors might work. What about you, Ori? Do you like red? I'm starting to think matching your fire salamanders' colors could work too."`
> - `"Why would you match the colors to my pets?"`
> - `"Why...? Well..."`
> - `"Your eyes are a really pretty blue, Hiyori, and your hair has a bluish tint too. If you don't have a particular favorite color, wouldn't a pet that matches your own distinctive colors suit you better?"`
> - `"............"`
>
> The right-hand nameplate must read `Ori Kenshi`, family name first. The source itself prints
> `Kenshi Ori`; that form is a banned alias and must not survive anywhere on the page.
>
> **Constraints.** Preserve the exact 2048 × 1456 canvas, crop and diagonal two-panel composition.
> Preserve both depictions of the blue-haired girl and the boy — faces, eyes, hands, hair, anatomy,
> poses, expressions, clothing and accessories — the open book they are reading, the pouch sparrow in
> the inset panel at the top right, the table, the chair, the room, the window, the lamp, the
> lighting, palette and texture. Change nothing but the text.
>
> All English upright, horizontal, left-to-right, left-aligned. No vertical, rotated, mirrored or
> stacked lettering. No speech balloons, boxes, borders, rules, bands, ornaments or watermarks. Keep
> the dialogue white with the soft dark outer glow the source's own white type carries, so each line
> stays legible where it crosses from light background to dark. Use one consistent type size for all
> five dialogue blocks and a clean serif consistent with the plate's cool, composed tone. Wrap on
> phrase boundaries; no one-word last lines, no lines ending on an orphaned article or preposition.
>
> No text may touch a face, an eye, a hand, the open book, or the pouch sparrow inset. No Japanese
> character may remain anywhere on the page.

---

## Editing and refinement record

### Pass A — source and continuity edit

- All seven regions transcribed from magnified crops, column by column, not from a page-level read.
  The lower-left block's first column was re-cropped separately because the initial crop clipped it.
- The five dialogue lines were traced to their source paragraphs in
  `Source/Volume 4/04 病気と療養.md` (lines 55–64) and matched to the filed English in
  `English/Volume 4/Chapter 1 - Illness and Recovery.md` (lines 35–43). The plate quotes the scene
  verbatim, so the filed prose — not a fresh translation — is the authority for all five.
- Speaker attribution confirmed from register rather than assumed: 俺 and じゃねえの mark C1 and L as
  Ori; 大利的には (addressing Ori by name) marks R as Hiyori; the ellipsis is her reaction, which the
  left-hand panel's blush confirms.
- `大利賢師` checked against `glossary.md`: the correct form is **`Ori Kenshi`**, and **`Kenshi Ori`
  is explicitly listed as a banned alias**. The source plate prints the banned form. This is the
  same defect the accepted Volume 3 plate corrected when it replaced `Kei Ohinata` with
  `Ohinata Kei`, so the correction here follows filed precedent rather than inventing one.
- `青の魔女` → `Blue Witch`, `キュアノス` → `Cyanos`, `御守り` → `amulet`, `火蜥蜴` → `fire salamanders`,
  all exact glossary forms.
- **One defect found in the filed prose and corrected there.** Chapter 1 line 35 rendered Hiyori's
  speech as “What about you, Ori? … matching Ori's fire salamanders” — converting the first
  name-as-address to `you` but leaving the second as `Ori's`, and dropping 色 from 火蜥蜴たちの色に.
  Half-converted name-as-address reads as a translation artifact in English. Corrected in the
  chapter file to “matching your fire salamanders' colors”, which is both person-consistent and
  closer to the Japanese. The plate and the chapter now carry identical wording.

**Pass A: complete**

### Pass B — publication-English refinement

- Read as finished copy, the five lines already work: Ori's are loose and unguarded, Hiyori's are
  clipped and practical, and the joke — that Ori pays her a direct compliment while thinking only
  about lizard colours — lands without help. No rewriting was warranted beyond the person fix above.
- **Both rubies dropped.** The source glosses 御守り as アミュレット and 火蜥蜴 as ペット. Both are
  semantic rubies whose two layers collapse into a single English word: the amulet gloss says
  "amulet", and the pets gloss is already carried in C1, where Ori says plain `pets` about the same
  animals. Setting two-tier gloss type over an illustration would read as apparatus, not design, and
  the filed chapter prose drops them at this point too.
- **Nameplates consolidated rather than translated line by line.** Rendering both tiers would print
  each character's name twice in English. The accepted Volume 3 plate consolidated for the same
  reason; following it also keeps the four filed volumes consistent.
- Retained the sixteen-dot silent line rather than substituting a single ellipsis. It is the beat
  the whole left-hand panel is built on, and its length is doing the work.
- Straight double quotes used throughout, matching the filed chapter prose.

**Pass B: complete**

---

## Notes and uncertainties

- **No unresolved or illegible text.** All seven regions resolved cleanly at magnification.
- **The artwork contains no other localizable text.** The book the two are reading shows no legible
  print, the pouch sparrow inset carries none, and the room's picture frame and lamp are blurred
  set dressing.
- **This plate is not a safe composite in the way `kuchie-001` was.** Every string sits over painted
  art, so the illustration cannot be carried through byte-for-byte and no zero-MAD gate applies.
  The QA gate is instead that all protected regions — both figures, the inset, the book — are
  untouched, and that the vacated strips show no mosaic, seam or rectangular ghost.

---

## Render record

**Status: accepted.**

### Method — generative edit, merged back over the source

`imagegen` was driven through Codex headless in image-edit mode, with the source as the edit target.
It produced excellent English typography, but it regenerated the entire canvas rather than editing
it: measured against the source the whole page differed (global MAD 19.3, open book 44.9). At
magnification the left girl's fingerless glove had disappeared, her eyes and lashes were redrawn,
and hair linework was re-inked — all far from any text. A whole-page accept would have shipped a
repaint of the illustrator's art, so the raw render was rejected.

The accepted file keeps the model's work only where text lives and restores the source everywhere
else:

- Per region, the merge rectangle is the union of the source's Japanese block and the render's
  English block, padded.
- Alpha is built from those rectangles dilated by 32 px, then Gaussian-blurred by 16 px, so alpha
  reaches a solid 1 across each block. An earlier attempt that only feathered the rectangle let the
  source's own `Kenshi Ori` Latin line ghost through beneath the new nameplate.
- Each region is colour-matched before blending, using the mean source-minus-render difference over
  a 48 px ring outside the rectangle, to cancel the regenerated page's global colour shift.

Merge rectangles: `95,670-315,760` · `1230,1095-1495,1205` · `670,710-925,1135` ·
`1510,890-1990,1400` · `85,1050-645,1440`.

This is not a mask-and-typeset composite: the fill under the removed Japanese is the model's own
reconstruction and the typography is the model's. Only the repainting was discarded.

### Verification — read off the rendered image, not the renderer's report

- All six prose strings verified verbatim at magnification.
- Right nameplate reads `Ori Kenshi`, letter by letter. The banned alias `Kenshi Ori`, which the
  source plate itself prints, appears nowhere.
- No Japanese survives in any of the seven regions; no ghost, smear or halo in the vacated strips.
- Protected art MAD vs source: left girl's face 0.63, right pair's faces 0.61, pouch sparrow 0.43,
  open book 0.54 — JPEG re-encode noise only.
- Output: real JPEG, RGB, 2048 x 1456, quality 95, subsampling 0 (4:4:4).

### Recorded deviation — silent line dot count

The source column carries exactly 12 dots (measured; this spec previously mis-stated 16, now
corrected). The accepted render sets 22.

Five generative attempts across two runs could not hold an exact count: 22, 13, 15, 17, and a
second run's best at 17 — and the renderer misreported that last one as 13. Image models do not
reliably reproduce a specified number of repeated identical glyphs. The 17-dot attempt was also
rejected because it stranded the closing quotation mark far right of the final dot.

Two attempts to trim the run by hand were reverted: interpolating vertically across the glyph band
smeared the diagonal panel edge behind it, and a threshold-and-fill left halo rings where the
anti-aliasing had been. Both were worse than the deviation.

Accepted as a cosmetic deviation in a silence beat, in preference to re-rolling six strings that are
already correct.

### Glossary

No new terms. Every term on the plate is already locked, including the plate's furigana form
`御守り[アミュレット]`, covered by the existing `御守り` -> `amulet` entry.
