# kuchie-005 — back frontispiece, series title plate

- **Source:** `Source/Volume 4/images/kuchie-005.jpg` — JPEG, RGB, 1440 x 2048 (portrait)
- **Output:** `English/Volume 4/localized-images/kuchie-005.jpg`
- **Scene:** a pale green paper field with a washed-out illustration band across the upper half, and
  the series title set small in green at the lower right.

## Text-bearing regions

One, and it is **already Latin**. There is no Japanese anywhere on this plate.

The washed-out band was contrast-boosted and inspected across its full width: it is a faded scene —
a large monster on a ruined street, two figures at the right, a small plant creature at the left —
with no lettering of any kind. The rest of the page is bare paper texture.

| # | Region | Ink box (native px) | Colour |
|-|-|-|-|
| 1 | Series title, line 1 | x854-1333, y1793-1825 | green, RGB(177, 205, 153) |
| 1 | Series title, line 2 | x735-1331, y1881-1912 | green, RGB(177, 205, 153) |

Paper ground is RGB(209, 227, 194). Cap-height is 33 px on line 1 and 32 px on line 2; the two lines
are right-aligned at x≈1332, with 88 px between their tops. The face is a letterspaced serif with
wide, even tracking.

## Verbatim source text

```
Wandmaker of
the Ruined World
```

## Exact English

```
Wand Maker of
the Ruined World
```

## Terminology decision

| Source | English | Authority |
|-|-|-|
| `Wandmaker` | `Wand Maker` | `novel.config.md:7`, locked EN title; `Wandmaker` is a **banned alias** |

The plate prints the series title in the publisher's own one-word styling. The project's locked
English title is two words, and every other title-bearing image in this edition has been corrected
the same way — see `Editing/Volume 4/image-localization/cover.md` and, in the previous volume,
`Editing/Volume 3/image-localization/cover.md` and `kuchie-001.md`. Leaving this plate alone would
have the same book print its own title two different ways.

This is the same class of correction as the `Kenshi Ori` nameplate on `kuchie-002`: where the
source's own Latin contradicts a locked project form, the locked form wins.

## Layout decision

Nothing moves. The correction inserts one space and capitalises the resulting `M`; line 2 is
untouched. Both lines keep their position, right alignment, typeface, tracking, size and colour.

Line 1 grows by one space width. Because the block is right-aligned, its left edge extends further
left — from x854 to roughly x820 — into bare paper. Nothing else on the page shifts.

## Production prompt

```
Use case: text-localization

Asset type: back frontispiece from a Japanese light novel, 1440 x 2048 portrait, a pale green paper
field with a washed-out illustration band across the upper half.

Input image: the provided image is the edit target. Edit it. Do not regenerate the illustration.

Primary request: a single two-word correction to the small green series title at the lower right.

  The title is set as two right-aligned lines in a letterspaced serif:
      line 1  "Wandmaker of"      at x854-1333, y1793-1825
      line 2  "the Ruined World"  at x735-1331, y1881-1912

  Re-set line 1 to read "Wand Maker of" — inserting a space and capitalising the M. Line 2 is
  already correct and must not change.

  Keep both lines exactly as they are in every other respect: same position, same right alignment at
  x1332, same letterspaced serif face, same wide even tracking, same cap-height of about 32 px, and
  the same green, RGB(177, 205, 153), on the RGB(209, 227, 194) paper. Line 1 grows by one space
  width and so extends further left into bare paper; nothing else moves.

Text invariants (verbatim):
  Wand Maker of
  the Ruined World

  Reproduce these two lines exactly, with this capitalization and spacing. "Wand Maker" is two
  words. The one-word form "Wandmaker" must not survive anywhere on the page.

Constraints:
  - There is NO Japanese on this plate. Do not add any, and do not "translate" anything.
  - Do not alter the washed-out illustration band across the upper half — the monster, the figures at
    the right, the small plant creature at the left, the ruined street, or its faded wash.
  - Do not alter the paper colour, its texture and flecks, the canvas, the crop, or the diagonal
    edges of the illustration band.
  - Add no text, boxes, borders, rules, ornaments or watermarks anywhere.
  - All English upright, horizontal, left to right.
```

## Editing and refinement record

**Pass A — source and continuity edit: complete.**

- The plate carries no Japanese; the only text is the Latin series title, verified by contrast-boost
  inspection of the entire page.
- `Wandmaker` contradicts the locked English title in `novel.config.md:7` and is corrected to
  `Wand Maker`, consistent with the cover of this volume and with Volume 3's cover and kuchie-001.
- Line 2 already matches the locked title and is left untouched.

**Pass B — publication-English refinement: complete.**

The string is a fixed series title, not prose; there is nothing to refine beyond the locked form.
Reread against the cover and the chapter-title map: `Wand Maker of the Ruined World` is the form
used throughout the edition, so the plate now agrees with the spine, cover, contents and EPUB
metadata.

## Notes and uncertainties

- The correction is one space. The risk is a renderer re-setting the whole line in a different face
  or tracking, or nudging the baseline — so the rendered line must be compared against line 2, which
  is untouched and acts as a built-in reference for face, size, colour and alignment.
- No uncertainties. The plate has exactly one text element and it is fully legible.

## Render record

**Status: accepted.**

### Method — generative glyphs composited onto the source's own paper

`imagegen` was driven through Codex headless in image-edit mode, two calls; the second produced the
corrected line. As on every plate in this volume the model regenerated the page, so its work had to
be merged back.

This plate took a different merge from the others, because it qualifies for the **flat-ground
exception**: line 1 sits on bare paper, not over artwork, so there is no art to reconstruct.
Wholesale region replacement was tried first and rejected — inside the replaced band the render's
paper measured 199.4 mean luminance against the page's 207, with texture washed out to a local
standard deviation of 3.87 against 6.09-6.24 elsewhere. That is a visible rectangle on the page,
and the renderer reported it as seamless.

The accepted file instead keeps the real paper and takes only the letterforms:

1. The line-1 band `x790-1350, y1782-1842` is refilled from the **source's own blank paper**
   directly above it (`y1722-1782`) — real texture, real flecks, same lighting.
2. Line 1's glyphs are lifted from the render as an alpha matte and painted onto that paper in the
   ink colour sampled from the source's **untouched line 2**, RGB(165, 207, 125).
3. The band boundary is feathered 6 px; the join is paper against paper.

### Verification — read off the rendered image, not the renderer's report

- Line 1 reads `Wand Maker of`; line 2 reads `the Ruined World`. `Wandmaker` survives nowhere.
- Both lines right-align at x1333, and the corrected line matches the untouched line 2 in typeface,
  tracking and cap-height.
- Core ink colour, new line vs untouched line: RGB(164.9, 205.8, 126.4) against
  RGB(164.6, 206.3, 124.9) — a match within a level.
- Paper texture inside the band is restored to local sd 5.90 against 6.09-6.24 on untouched paper;
  the residual difference is the ink itself. No rectangle is visible at 4x contrast boost.
- No Japanese was added; none existed to begin with.
- MAD vs source outside the edit band is 0.86 — JPEG re-encode noise on heavily speckled paper. The
  washed-out illustration band is untouched.
- Output: real JPEG, RGB, 1440 x 2048 portrait, quality 95, subsampling 0 (4:4:4), 1,598,241 bytes.
- Source SHA-256 unchanged: `c27855d74584c100255b7aa4222975396f9715a35735c14f2501a1af39233e9b`.

### Glossary

No new terms. The `Wandmaker` -> `Wand Maker` correction follows the locked title in
`novel.config.md:7`; it is enforced per-image in the specs rather than as a glossary row, matching
how the cover and Volume 3 handle it.
