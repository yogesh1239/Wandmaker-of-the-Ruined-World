# s-h1 — booklet cover

- **Source:** `Source/Volume 4/images/s-h1.jpg`
- **Size:** 1440 × 2048 portrait
- **Source SHA-256:** `fc1cec66aacc7fe0eeae40b605951c944f37947413627a910947d8585f1bd7c4`
- **Type:** cover of the Volume 4 bonus booklet — mottled off-white paper stock, the Wand of
  Arachne standing full-height through the centre, a large magenta `秘` rubber stamp across the
  lower left, and magenta display type top-left and down the right edge.

## Verbatim Japanese by visual region

| ID | Region | Ink extent | Verbatim |
|-|-|-|-|
| H1 | Display heading, top left | 105–652, 127–250 | `極秘資料` |
| H2 | Latin sub-title, line 1 | 105–425, 305–332 | `Wandmaker of` (already Latin) |
| H3 | Latin sub-title, line 2 | 105–503, 350–378 | `the Ruined World` (already Latin) |
| H4 | Vertical title, right edge | 1241–1380, 60–1830 | `崩壊世界の魔法杖職人` |
| H5 | Circled volume mark | 1265–1370, 1870–1960 | `④` (numeral only — no Japanese) |
| H6 | Rubber stamp, lower left | glyph 90–720, 1200–1900; circle 0–780, 1100–1960 | `秘` |
| H7 | Engraving on the wand shaft | ~880–980, 1100–1560 | Latin, diegetic — see *Notes* |
| H8 | Three magenta blocks, far left | 20–60, 60–340 | decorative rule, no text |

## Wording authority

`極秘資料` is locked by the chapter-title map at `novel.config.md:114`:
`崩壊世界の魔法杖職人 ４ 小冊子　極秘資料` → **Wand Maker of the Ruined World 4 Booklet - Top
Secret Files**. The booklet's own cover heading therefore reads **TOP SECRET FILES**.

`崩壊世界の魔法杖職人` → **Wand Maker of the Ruined World**, locked at `novel.config.md:7`.

## Terminology decisions

| Japanese | English | Reasoning |
|-|-|-|
| `極秘資料` | **TOP SECRET FILES** | locked via the chapter-title map; `極秘` is *top* secret, a deliberate step above the `秘` on the stamp |
| `秘` | **SECRET** | the stamp is the standard Japanese *maru-hi* confidential mark. The source deliberately grades its two secrecy words — `極秘` for the heading, plain `秘` for the stamp — and English keeps that step by pairing TOP SECRET FILES with a bare SECRET rather than repeating the heading |
| `Wandmaker` | **Wand Maker** | `Wandmaker` as one word is a banned alias. It is already Latin in the source but still wrong, and is corrected in place — the same call filed for `allcover-001`, where it appears twice |

## Layout decision — the vertical title

`崩壊世界の魔法杖職人` runs as a single vertical column down the right edge, x1241–1380: a band
139 px wide and 1770 px tall. Horizontal English at title size cannot fit 139 px, and English
cannot be set vertically.

**Decision:** keep the band and fill it with five stacked **horizontal** words, reading top to
bottom, each word upright and left-to-right:

```
WAND
MAKER
OF THE
RUINED
WORLD
```

At 139 px the longest words (`OF THE`, `RUINED`, six characters) sit at roughly 23 px per
character, which is display scale for this canvas. This is not vertical English — every word runs
left-to-right; only the *sequence* of words descends, which is an ordinary English cover
treatment for a tall narrow band.

The alternative — dropping the column and promoting the existing Latin sub-title to carry the
title alone — was rejected: it would leave the right third of the cover empty and strand the `④`
with nothing above it.

## Layout decision — the stamp

The `秘` stamp is the cover's dominant graphic and it is *type*, not scenery: a rubber-stamp
impression of one character. Left in Japanese it would be the single loudest untranslated element
on the booklet, so it is localized to `SECRET` set horizontally inside the existing circle, in the
same magenta, with the same blotchy uneven ink coverage and paper bleed. The circle itself, its
broken stroke and its ink texture are unchanged.

The circle's right edge reaches x780 and the wand shaft begins at x820, so the stamp can be
replaced without the render touching the wand.

## Exact English by region

| ID | English |
|-|-|
| H1 | `TOP SECRET FILES` |
| H2 | `Wand Maker of` |
| H3 | `the Ruined World` |
| H4 | `WAND` / `MAKER` / `OF THE` / `RUINED` / `WORLD` |
| H5 | unchanged (`④`) |
| H6 | `SECRET` |
| H7 | unchanged (diegetic Latin engraving) |
| H8 | unchanged (decorative) |

## Editing and refinement record

### Pass A — source and continuity edit: complete

- `極秘資料` checked against the chapter-title map rather than translated fresh; `novel.config.md:114`
  gives **Top Secret Files**, and the same rendering is filed for Volumes 1, 2 and 3, so the
  booklet cover must not invent a variant such as "Classified Documents" or "Confidential Material".
- `崩壊世界の魔法杖職人` taken from `novel.config.md:7`, not retranslated.
- `Wandmaker` flagged as the banned one-word alias and corrected, matching the filed `allcover-001`
  decision. Because it is already Latin it is easy to pass over as "no Japanese here"; it is
  nonetheless wrong and is fixed.
- `④` and the shaft engraving confirmed as non-Japanese and excluded from localization.
- `秘` confirmed as the *maru-hi* mark, not a character in a word, so it takes a word-level English
  equivalent rather than a gloss.

### Pass B — publication-English refinement: complete

- Read the cover as finished English. The heading/stamp pair now grades the same way the Japanese
  does — TOP SECRET FILES above, SECRET stamped across — instead of flattening both to one word.
- `TOP SECRET FILES` set in caps to match the weight of `極秘資料`; the source heading is the
  heaviest type on the page and the English must not read as a caption.
- The Latin sub-title stays in its existing letterspaced small-caps treatment. It is subordinate to
  the stacked title in the right band, which is the hierarchy the source has.
- Checked the three type classes stay distinct: display heading, letterspaced sub-title, stamped
  mark.
- Exact-English section and the production prompt below carry identical wording.

Pass A: complete
Pass B: complete

## Production prompt

> You are producing one localized illustration for an official English edition of a Japanese
> light novel. This is a **text-replacement edit**, not a redesign.
>
> Reference image (the original Japanese page): `Source/Volume 4/images/s-h1.jpg`
>
> **HARD REQUIREMENT — OUTPUT SIZE.** Exactly **1440 pixels wide by 2048 pixels tall**. Same
> canvas, same crop. Verify the saved file's dimensions before reporting.
>
> **HARD REQUIREMENT — DO NOT RECOMPOSE.** The wand standing through the centre of the cover —
> its cage head, the glowing blue orb inside it, every scroll and band on the shaft, the rust and
> blood staining, the engraved Latin lettering on the shaft — stays exactly where it is at exactly
> its current size. The mottled off-white paper texture, the three small magenta blocks at the far
> left edge, and the magenta ink splash running down the lower centre all stay. Only lettering changes.
>
> **ALL ENGLISH IS HORIZONTAL, UPRIGHT, LEFT-TO-RIGHT.** No vertical English, no rotated words, no
> stacked single letters.
>
> 1. Display heading top left, currently `極秘資料` at x105–652, y127–250. Replace with
>    `TOP SECRET FILES` — same magenta, same heavy rounded gothic, same position, filling the same
>    width. This is the heaviest type on the page and must stay that way.
> 2. Directly below it, two lines of letterspaced magenta small-caps serif currently reading
>    `Wandmaker of` (x105–425, y305–332) and `the Ruined World` (x105–503, y350–378). Change only
>    the first line, to `Wand Maker of` — two words, not one. The second line is already correct;
>    reproduce it exactly. Keep the letterspacing, the size and the subordinate weight.
> 3. The tall vertical Japanese title down the right edge, `崩壊世界の魔法杖職人` at x1241–1380,
>    y60–1830. **Remove it entirely** and restore the paper texture behind it. In the same band set
>    five stacked HORIZONTAL words, evenly spaced from top to bottom, all the same size, all in the
>    same magenta as the heading:
>        `WAND`
>        `MAKER`
>        `OF THE`
>        `RUINED`
>        `WORLD`
>    Each word horizontal and upright. Do not stack letters vertically. Do not rotate anything.
> 4. Leave the circled `④` at x1265–1370, y1870–1960 exactly as it is — it is a numeral.
> 5. The large magenta rubber stamp across the lower left: a broken circle at x0–780, y1100–1960
>    with the single character `秘` inside it at x90–720, y1200–1900. Keep the circle exactly as it
>    is — same position, same size, same broken uneven stroke, same ink texture. Replace only the
>    character inside it with the word `SECRET`, set horizontally across the middle of the circle,
>    filling it the way the character does. It must look stamped: the same blotchy magenta, the
>    same uneven coverage, the same bleed into the paper grain. Not clean printed type.
>    Nothing of the stamp may cross x800 — the wand shaft begins at x820 and must not be touched.
> 6. The engraved Latin lettering on the wand shaft is part of the illustration. Leave it exactly
>    as it is. Do not sharpen it, re-letter it, or replace it.
>
> Every string appears exactly once, spelled and punctuated exactly as written above. No Japanese
> may remain except the deliberately untouched `④`. Professional letterspacing and optical
> alignment. No text may cover the wand.
>
> Render one image. Then open it and inspect it at full resolution. Report the exact pixel
> dimensions; that the vertical Japanese column is gone and replaced by five horizontal words;
> that the stamp reads `SECRET` and its circle is unchanged; that the sub-title reads `Wand Maker
> of` as two words; and that no other Japanese remains. Report honestly what you actually see.

## Notes and uncertainties

- **The wand-shaft engraving is diegetic and only partly legible.** At 4× it resolves to Latin
  letters running along the shaft — the beginning reads as `Witch of Arachne` and there is further
  lettering below it that does not resolve cleanly against the rust and blood staining. It is
  already Latin, it is engraved into the prop rather than set as page type, and it is damaged in
  the artwork by design. It is therefore left exactly as it is, and no reading is asserted for the
  illegible portion. This follows the `allcover-001` decision on the painted back-cover signage:
  lettering inside the illustration is set-dressing, not display copy.
- The three magenta blocks at x20–60 are a decorative rule, not characters.
- `④` is a numeral and is retained; the same call as the starburst numeral on `p294-295`.

## Render record

| Render | Native size | Verdict |
|-|-|-|
| A | 1054 × 1492 | Wording, spelling and all five horizontal title words correct. Rejected: recomposed the page — wand drawn much larger, the five words bunched into the upper two thirds, the `④` stranded mid-page, the stamp shrunk and moved. Nothing aligned for merge-back. |
| B | 1440 × 2048 (native, correct) | **Accepted.** Wording correct; the five title words and the `④` land in the right band at close to source positions. The wand is still drawn larger and the stamp circle redrawn — neither matters, both fall outside the merge rects, so the source wand and the source circle are what ship. |

Merged with `merge_sh1.py` — 4 rects, GROW 6 / FEATHER 5.

- coverage test: **leak 0** — nothing changed outside the rects
- untouched-wand probe x850–1010 / y400–900: MAD **0.293** — the focal art survives intact
- global MAD 12.26

### Tone matching — what failed, and why the band was a different problem

Four attempts, and the first three are recorded because each was wrong in an instructive way:

1. *Global two-anchor curve.* Failed. The only flat anchors on this cover — paper and wand shaft —
   are ~20 levels apart, so the slope they pin is unstable. It over-brightened the render and left
   every rect visible as a bright rectangle.
2. *Per-rect constant ring offset.* Correct for the heading and the stamp; the sub-title and the
   title band stayed visible.
3. *Per-rect ring plane fit* (`a + bx + cy` per channel). Fixed the sub-title. The band's plane came
   back near zero — proof the mismatch there was never a gradient.
4. *Percentile paper offset.* Reported +27/+35/+32 for the band and turned it into a bright strip.
   The number was an artefact: on near-white stock the 80th percentile saturates at 255 in the
   source, so the "offset" was measuring the clip, not the paper.

The distribution inside the band settled it. More than 75 % of the source band is pure 255 white —
it is a white plate on mottled cover stock, not paper — with deep purple ink at the low end. The
render's band paper tops out near 230 and its ink is far weaker. That is a **gain** error, not an
offset, and every one of the four attempts above was trying to correct it with an offset.

So the shipped merge uses a **paper-anchored gain**: per rect, the source's 90th percentile over
the render's, clipped to 0.9–1.3. Heading, sub-title and stamp take ×1.02; the band takes
×1.11/1.14/1.13.

### Re-inking the title band

Gain alone left one real defect. The source's vertical title is deep purple, measured at
**(82, 49, 84)**; the render set the five English words in the same magenta as the heading,
**(153, 73, 125)**. That flattens the page's hierarchy — on this cover the title has to be the
darkest thing, darker than `TOP SECRET FILES`. No gain fixes it: the slope needed to move the ink
that far also blows out the paper.

`H4` is therefore re-inked instead of tone-corrected. The render's letterforms are read as a
coverage map — coverage 0 at the render's paper level 230, coverage 1 at its densest stroke 103 —
and the source's own ink colour, sampled at **(73, 40, 76)** from pixels below luminance 90 inside
the band, is laid through it. Antialiasing survives because coverage is continuous, and the paper
texture the render invented flattens back toward the white plate.

The recolour is **gated on magenta** (`min(R,B) − G > 15`), and that gate is not optional. The band
is not text-on-white the whole way down: the wand's upper tendril reaches into it around y380–520,
and re-inking the rect wholesale turned that green curl purple. Magenta ink has green well below
both red and blue, the tendril is the opposite, and paper is neutral — so the gate separates them
cleanly and leaves art and plate to the ordinary gain path.

This is a merge refinement, not a change of localization method: every letterform still comes from
`imagegen`. Only its colour is corrected to the source's.

### Visual QA at full resolution

- Heading, sub-title, band and stamp inspected at 1:1; band edges profiled column by column across
  x1150–1430 against the source.
- All English horizontal, LTR, upright. No vertical or rotated English anywhere.
- No Japanese survives: the vertical column is gone end to end, with no gaps left standing between
  the five words.
- Hierarchy matches the source — title darkest, heading magenta, sub-title light, stamp pink.
- Wand, orb, engraving and stamp circle unchanged from source.

- **Image-edit renders:** 2 (A rejected, B accepted)
- **Saved output:** `English/Volume 4/localized-images/s-h1.jpg` — real JPEG, quality 95,
  subsampling 0 (4:4:4), 1440 × 2048
- **Output SHA-256:** `a29600c3243d058fb41263e0bdc791daccf1ca1519d3d22bda17d5008e906084`
- **Source integrity:** original unmodified

Scratch state is intact and re-runnable: `rects_sh1.py`, `merge_sh1.py`, `sh1_genB.png`.
