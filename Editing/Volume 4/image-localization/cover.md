# Image Localization Spec — `cover.jpg`

## Source

- **Path:** `Source/Volume 4/images/cover.jpg`
- **Type:** front-cover illustration with editorial display typography
- **Canvas:** 1800 × 2560 portrait JPEG

## Composition and protected art

Three characters on a cracked, overgrown road under a pale blown-out sky: a tall witch in a black dress with a long blue-black ponytail on the left holding a wand across her body; a green-haired witch in a bright red-to-pink skirt on the right, mouth open mid-speech, one gauntleted hand raised around a glowing blue orb; and a dark-haired boy with a bandaged eye crouching between and behind them. Everything except the listed text regions is protected: all three faces, eyes, mouths, hands, gauntlets, anatomy, poses, hair, the black dress and its ragged trim, the red skirt, the wand, the blue orb and its glow, the leaf-and-flower headpiece, the broken asphalt, the pale sky, the birds, the drifting embers, the palette, and the paint texture.

## Verbatim Japanese by visual region

1. **Main title** — oversized white brush lettering set as two vertical columns running down the outer edges, reading right column first: `崩壊世界の` then `魔法杖職人`, i.e. `崩壊世界の魔法杖職人`
2. **Latin sub-title** — already Latin in the source, upper-centre, two rotated lines in a letterspaced serif: `Wandmaker of` / `the Ruined World`
3. **Author credit** — upper-centre, vertical white sans serif: `黒留ハガネ`
4. **Illustrator credit** — upper-centre, vertical, beneath the printed Latin role label `Illustrator`: `かやはら`
5. **Volume mark** — upper-centre, numeral inside a thin hand-drawn white circle: `4`

## Exact English by visual region

1. **Main title:** `Wand Maker of the Ruined World`
2. **Latin sub-title, corrected in place:** `Wand Maker of` / `the Ruined World`
3. **Author credit:** `Kurodome Hagane`
4. **Illustrator credit:** `Illustrator` + `Kayahara`
5. **Volume mark:** `4`

## Production edit prompt

Use case: text-localization of the supplied source image. Treat the supplied image as the edit target and produce a finished official-English-edition front cover.

Replace only these text regions. Everything else in the image is protected artwork.

- Replace the oversized white Japanese brush title, currently set as two vertical columns down the outer edges reading `崩壊世界の魔法杖職人`, with the exact English title `Wand Maker of the Ruined World`.
- Replace the two-line Latin sub-title `Wandmaker of` / `the Ruined World` with `Wand Maker of` / `the Ruined World`. This is a one-word-to-two-word correction only: keep its position, rotation, letterspaced serif face, scale, and soft white colour exactly as they are. The only change is a space inserted in `Wandmaker` and the resulting capital `M`.
- Replace the vertical author credit `黒留ハガネ` with `Kurodome Hagane`.
- Replace the vertical illustrator credit `かやはら` with `Kayahara`, keeping the existing Latin role label `Illustrator` as its own separate smaller line.
- Preserve the volume mark as the exact numeral `4` inside its existing thin hand-drawn white circle, at its original scale and position.

Main-title treatment: preserve the source hierarchy of huge distressed white brush lettering, but typeset the English upright, horizontal, and left-to-right. Use a bold condensed display face with rough hand-painted edges, a pure-to-warm white fill, and the same subtle irregular texture and soft edge bleed the Japanese lettering has. Arrange the exact title as two balanced horizontal phrase blocks, `Wand Maker` over `of the Ruined World`, placed in the outer-edge negative space the vertical columns currently occupy. Do not rotate words, stack one letter per line, clip letters, or let any letter cover a face, an eye, a hand, the wand, the blue orb, or the headpiece. Reduce the type size moderately before encroaching on the characters.

Credits treatment: keep the credits in their existing upper-centre negative space, but set every line horizontal and left-to-right. Set `Kurodome Hagane` in a thin, clean white sans serif matching the weight and restraint of the source author credit. Keep `Illustrator` as a separate, noticeably smaller white sans-serif role label with `Kayahara` on its own line in the same restrained credit style. Do not merge the role label into the name, and do not enlarge the credits relative to the title.

The quoted English is verbatim copy. Preserve exact capitalization and spacing in `Wand Maker of the Ruined World`, `Wand Maker of`, `the Ruined World`, `Kurodome Hagane`, `Illustrator`, `Kayahara`, and `4`. Render `Wand Maker` as two words everywhere it appears. The single-word form `Wandmaker` must not survive anywhere on the finished cover. Do not paraphrase, translate, omit, duplicate, renumber, or invent text.

Preserve the 1800 × 2560 canvas, the crop, all three characters, their faces, eyes, mouths, hands, anatomy, poses, hair and clothing, the wand, the glowing blue orb, the headpiece, the cracked road, the sky, the birds, the embers, the lighting, the palette, and the paint texture exactly. Do not repaint, move, crop, extend, recolour, beautify, or redesign the illustration.

Typography: professional kerning, optical alignment, balanced line lengths, and natural phrase-based wrapping. No vertical English, no rotated English other than the pre-existing sub-title keeping its original rotation, no one-letter-per-line stacking, no mirrored text, no generic subtitles, no meme captions, no added boxes, borders, bands, rules, or ornaments, and no watermarks.

Before returning the edit, verify by inspection: every required string and punctuation mark is exact; no targeted Japanese glyph and no instance of the alias `Wandmaker` remains; no extra or duplicated text appears; all English is horizontal left-to-right apart from the pre-existing rotated sub-title; nothing is clipped or overlapping; the three characters and all artwork are undamaged; and the cover plausibly looks originally designed in English.

## Editing and refinement record

- **Pass A: complete.** Every region was transcribed from a 3× LANCZOS crop of the credit block, both upright and rotated, rather than from a page-level read. Checked against `novel.config.md` and the filed precedent: `崩壊世界の魔法杖職人` → `Wand Maker of the Ruined World` per config line 7; `黒留ハガネ` → `Kurodome Hagane` per config line 10; `かやはら` → `Kayahara` and the `Illustrator` role label per the filed Volume 3 `cover.md` and the Volume 1 frontmatter specs. Volume mark confirmed as `4`. Romanization carries no macrons and no long-vowel doubling.
- **Pass B: complete.** There is no prose on this cover, so publication-English refinement reduces to the display-copy decisions: the title is set as the locked config form rather than re-worded, the two-word `Wand Maker` is enforced against the source's own one-word Latin alias, and the role-label-over-name credit shape is kept because it is how the source organises the credit and how Volumes 1 and 3 are already filed.

## Notes and uncertainties

- **No unresolved or illegible text.** All five regions resolved cleanly at 3×.
- **`Wandmaker` as one word is a banned alias.** The source itself prints it in the Latin sub-title. It is corrected in place rather than removed, since the sub-title is a deliberate design element; the correction costs one space and one capital.
- **This overrides the config's default cover policy, by request.** `novel.config.md` line 122 would otherwise retain the Japanese cover as-is. The user explicitly asked for the Volume 4 illustrations to be localized, and the filed Volume 3 `cover.md` records the same override for the same asset, so Volume 4 follows it for consistency. The original file is not modified either way.
- **The volume mark stays a numeral.** `4` is already language-neutral; only its circle and placement matter.
- **Consistency with `allcover-001.jpg`.** The wraparound jacket carries this same front-cover panel and is deliberately *not* rendered; see `allcover-001.md` for that decision. The localized cover the build consumes is this file.
- The output must be a real RGB JPEG at exactly 1800 × 2560, quality 95, 4:4:4 chroma subsampling.

## Render and final QA

### Round 1 — rejected

Whole-canvas image generation was used. The typography came out well: the main title, the corrected sub-title, all three credit strings, and the circled `4` were all correct, complete, horizontal, and free of the banned one-word alias. **The artwork was not preserved, so the render was rejected.**

The generator worked at 1052 × 1495 and upscaled to 1800 × 2560, which re-synthesized the painting rather than editing it. Measured mean absolute difference against the source, per channel, in regions carrying no text and therefore expected to be pixel-identical:

| Region | MAD |
|-|-|
| boy's face | 19.6 |
| green witch's face | 18.4 |
| dark witch's face | 17.0 |
| blue orb | 15.0 |
| red skirt | 40.9 |
| road, lower centre | 44.3 |

The damage was describable, not merely resampling noise: the crouching boy was redrawn larger and more upright, his bandage moved from over his eye to across his forehead, his shirt changed, and **he gained a pendant necklace that does not exist in the source**. The red skirt's layered petal silhouette with its sharp pointed bodice became a broad smooth drape, and the green witch's mottled bodice detailing was smoothed away.

The generator self-reported all eight of its checks as passed, including "characters remain intact". That was wrong: it judged intactness by whether two witches and a boy were still present, never comparing against the source. **This is the standing reason renders are QA'd by measurement here and never on the generator's self-report.**

### Round 2 — compositing method

Method changed rather than re-rolled. The English text is composited onto the original pixels: load the source at native resolution, inpaint away only the Japanese lettering (the two outer-edge title columns and the upper-centre credit cluster) from adjacent artwork, then set the English with real fonts. Sharp, correctly-placed type is preferred over a distressed texture that costs art fidelity. Because every non-inpainted pixel is carried through untouched, the MAD gate over protected regions is expected to read exactly `0.00`, not merely below a tolerance.

### Measured element geometry

All coordinates are native 1800 × 2560 source pixels.

| Element | Bounds | Disposition |
|-|-|-|
| Left title column `魔法杖職人` | x 0–360, glyph bands at y 0–803, 923–1275, 1394–1741, 1864–2202, tail to ≈2400 | remove |
| Right title column `崩壊世界の` | x 1440–1800, y 0–2116 | remove |
| Author `黒留ハガネ` | x 1133–1239, y 72–539 | remove, re-set |
| Latin sub-title `Wandmaker of` / `the Ruined World` | x 1240–1367, y 72–619 | remove, re-set corrected |
| `Illustrator` label | x 1055–1118, y 78–299 | remove, re-set |
| `かやはら` | x 1065–1129, y 293–544 | remove, re-set |
| Circled volume mark `4` | x 1091–1259, y 540–699 | **untouched — not masked, not redrawn** |

### Layout decision — the title stays vertical, in the source's own columns

**By user direction, the English title keeps the source's vertical treatment.** The type goes back into the two full-height outer columns the Japanese title occupied, set as rotated lines rather than horizontal blocks.

This is a deliberate departure from the usual localization default of upright horizontal English, and it is justified on this asset:

- **The source already sets Latin vertically on this very cover.** Its own sub-title, `Wandmaker of` / `the Ruined World`, is printed as rotated columns in the credit cluster. Rotated Latin is therefore the established design language of this jacket, not an import.
- **Rotation direction is measured, not assumed.** Cropping that Latin column and rotating it back 90° counter-clockwise renders it correctly horizontal, so the source sets Latin **rotated 90° clockwise, reading top-to-bottom**. The English matches that exactly.
- **It is the highest-fidelity option available.** Returning the type to the columns it came from means the English covers precisely the artwork the Japanese covered. Every alternative exposes art the original hid while obscuring art the original left clear.
- **The column split is already correct in English.** The source's right column is `崩壊世界の` and its left column is `魔法杖職人` — literally *of the ruined world* and *wand maker*. Mapping `Wand Maker` to the left column and `of the Ruined World` to the right preserves the source's own semantic placement **and** reads left-to-right, matching the LTR binding this edition is built with (`novel.config.md`, reading-direction row). No reordering is required.

Resulting hierarchy: `Wand Maker` is 10 characters and `of the Ruined World` is 19, so filling comparable column heights makes the left column roughly twice the type size of the right. That falls out as a natural dominant/subordinate pairing rather than something imposed.

The credit cluster likewise stays vertical at the source's own upper-centre-right position, matching the orientation of the Japanese credits it replaces, and the circled `4` is left exactly where the illustrator drew it.

### Rejected render — blocked and smeared inpainting

The first composite was rejected on the fill, not the type. Masking the Japanese and filling by diffusion left **visible blocky mosaic artifacts down both outer strips**, worst across the right edge and the upper-right sky, plus a white vertical streak through the credit cluster that collided with the author line. Typography and copy were correct; the fill was not publication quality.

The fix is a smooth multi-scale fill rather than a coarse one, and the rejection stands as the reason the fill is inspected directly at magnification and not accepted on the renderer's report.

### Round 3 — vertical composite, superseded

The vertical composite was built and is factually correct: `Wand Maker` down the left column and
`of the Ruined World` down the right, both rotated 90° clockwise, with `Kurodome Hagane`,
`Illustrator` / `Kayahara`, the corrected secondary Latin line, and the circled `4` carried through
untouched. The artwork survived intact and the fill was far better than Round 2's.

It was still rejected, on the goal rather than on any single defect. It reads as the Japanese cover
with English swapped into it — which is literally what it is — and the brief is a cover that looks
designed in English from the start. Residual mottling remained in the right-hand background, and the
secondary line and credits sat at too low a contrast against the blown-out sky to hold.

### Round 4 — accepted design, corrected facts

An externally produced design was adopted instead: `cover-2.png`. It is a genuine improvement and
the reasons are worth recording, because they define the target for the rest of the volume.

- The Japanese lettering is removed cleanly — no blocking, no smearing, no seams. This was the
  defect that sank Round 2.
- The artwork is the source artwork. Height-normalised side-by-side comparison of the upper-left
  quadrant confirms the witch's hair strands, dress, pose and wand all match; nothing was
  re-synthesized.
- The typography is integrated into the illustration rather than laid on top of it, and the credits
  are set vertically, echoing the source's own treatment.

**It carried three factual errors, all of which were corrected in place rather than by re-rendering,
so the approved design is preserved exactly.**

| Region | As delivered | Corrected to | Authority |
|-|-|-|-|
| Author | `Kurobe Kuro` | `Kurodome Hagane` | `novel.config.md` Identity — 黒留ハガネ |
| Illustrator | `Illustrated by ks` | `Illustrated by Kayahara` | かやはら, no macron |
| Title | `WANDMAKER` | `WAND MAKER` | banned one-word alias |

The wrong author name is the most serious defect this spec has recorded. It is not a style slip — it
misattributes a real person's book, and it was stated confidently by a renderer that reported its
own text as correct. **Names of real people are now read back off the rendered image and compared
character by character, never taken from the prompt that was sent.**

`Illustrated by` was kept rather than reverted to the `Illustrator` / name pairing used in Volumes
1–3. It is better English and it is the phrasing this cover's design already uses; only the name was
ever wrong.

### Known deviations, accepted deliberately

- **Canvas is 948 × 1659, not the source's 1800 × 2560**, and the aspect differs (0.571 vs 0.703),
  so roughly 19 % of the width is cropped — the outer strips the vertical Japanese title occupied.
  The design was not stretched or padded to force a match: distorting an approved cover is worse
  than shipping it at its own geometry. If a full-resolution cover is wanted later, the design
  should be regenerated at 1800 × 2560 **with the corrected strings**, not upscaled from this file.
- **The volume mark was redrawn** as `VOL. 4` inside a compass motif, where the source has a plain
  numeral in a thin hand-drawn circle, and small decorative flourishes were added around the title.
  Both are invented rather than source-derived. They are consistent with the cover's own design
  language and are accepted under the design freedom this project grants; they are recorded here so
  the deviation is deliberate rather than unnoticed.

### Verification of the corrections

All three strings were read back **off the rendered image** at magnification, not taken from the
prompt — the rule this cover's history established:

| Region | Reads on the page | Verdict |
|-|-|-|
| Author | `Kurodome Hagane` | correct |
| Illustrator | `Illustrated by Kayahara` | correct |
| Title | `WAND MAKER` | correct, two words |

No instance of `Wandmaker`, `WANDMAKER`, `Kurobe`, standalone `Kuro` or ` ks` survives. `OF THE` and
`RUINED WORLD` are pixel-identical to the approved design. Output is a real JPEG, RGB, 948 × 1659,
quality 95, 4:4:4, 907,686 bytes. `cover-2.png` is unmodified (SHA-256 unchanged).

The title fix used the preferred approach: the existing `MAKER` letterforms were translated 24 px
right as raster pixels, so the ornate distressing is the original artwork, not a re-typeset
imitation. No display font was substituted.

### Outstanding defect — visible seam at the `D`/`M` junction

Shifting `MAKER` and filling the vacated gap left **visible artifacts in the artwork behind the new
word space**: a soft light smudge above the gap, and a vertical tonal step in the dark background
where the moved block's boundary falls. The letterforms are clean; the background around them is
not. It is subtle at full-cover viewing size and obvious at magnification.

This was not chased further, because the better fix is the one already recommended below rather
than more retouching of a low-resolution file.

### Recommendation

**Regenerate this design at 1800 × 2560 with the corrected strings.** That resolves three things at
once — the seam, the 948 px width (well under normal ebook-cover standards), and the cropped aspect
— and it costs one generation with `Wand Maker`, `Kurodome Hagane` and `Illustrated by Kayahara`
supplied correctly up front. Do not upscale this file to get there.

Until then, `cover.jpg` as filed is factually correct and is the asset the build should consume.

- **Status:** accepted with the seam defect recorded; regeneration at full resolution recommended.
