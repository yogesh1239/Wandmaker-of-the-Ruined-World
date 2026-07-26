# Image Localization Spec — `kuchie-001.jpg`

## Source

- **Path:** `Source/Volume 4/images/kuchie-001.jpg`
- **Type:** colour frontispiece plate — full illustration above, editorial title/credit block below on a white field
- **Canvas:** 1440 × 2048 portrait JPEG
- **Output:** `English/Volume 4/localized-images/kuchie-001.jpg`
- **Wording authority:** `novel.config.md` Identity block; the accepted `English/Volume 3/localized-images/kuchie-001.jpg` and its spec.

### Measured geometry

| Element | Bounds | Notes |
|-|-|-|
| Illustration | y 0–1583 | full-bleed to the canvas edges |
| White field | y 1584–2048 | pure RGB(255,255,255); canvas corners all pure white |
| Main title `崩壊世界の魔法杖職人` | x 113–1109, y 1654–1735 | ink height 82 |
| Circled volume mark `④` | x 1110–1185, y 1682–1730 | numeral inside a ring, sits at the title's end |
| Latin sub-title | x 115–643, y 1761–1776 | ink height 16, letterspaced |
| Author `黒留ハガネ` | x 686–899, y 1919–1950 | |
| `Illustrator` label | x 900–1081, y 1925–1945 | already Latin |
| `かやはら` | x 1103–1218, y 1924–1945 | |

All type is a soft green. Sampled means run RGB(177,214,143) to (200,224,174), but those averages
include anti-aliased edge pixels and are lighter than the true ink — the core colour must be sampled
from the source's own densest glyph pixels, not taken from this table.

**Every text element sits on the flat white field, clear of the illustration.** No inpainting over
artwork is required, and the illustration is not touched at all.

---

## Verbatim Japanese by region

### Main title
```
崩壊世界の魔法杖職人
```

### Volume mark
```
④
```

### Latin sub-title (already Latin in the source)
```
Wandmaker of the Ruined World
```

### Credit line
```
黒留ハガネ　Illustrator　かやはら
```

---

## Exact English by region

### Main title
```
Wand Maker of the Ruined World
```

### Volume mark
```
4
```

### Latin sub-title, corrected in place
```
Wand Maker of the Ruined World
```

### Credit line
```
Kurodome Hagane   Illustrator   Kayahara
```

---

## Terminology decisions

| Source | English | Basis |
|-|-|-|
| 崩壊世界の魔法杖職人 | Wand Maker of the Ruined World | `novel.config.md` Title (EN) |
| 黒留ハガネ | Kurodome Hagane | `novel.config.md` Author; no macron, no long-vowel doubling |
| かやはら | Kayahara | direct romanization, no macron |
| `Illustrator` | `Illustrator` | already Latin, retained as a separate role label |
| ④ | `4` | language-neutral numeral, kept inside its ring |
| `Wandmaker` | `Wand Maker` | **banned one-word alias**, printed by the source itself and corrected here |

---

## Production prompt

> Text-localization of the supplied source image. Treat it as the edit target. Composite onto the
> original pixels; do not regenerate the illustration.
>
> **Match the accepted Volume 3 frontispiece** `English/Volume 3/localized-images/kuchie-001.jpg` for
> face, weight, hierarchy and spacing. That page is the series treatment; this one differs only in
> that its type is green rather than pink, and its volume mark is `4`.
>
> **Do not touch the illustration.** It occupies y 0–1583 and must be carried through byte-for-byte.
> Every edit happens in the white field below it, y 1584–2048, which is pure RGB(255,255,255).
>
> **Replace, keeping each element's position, colour and hierarchy:**
> 1. The large green Japanese title at x 113–1109, y 1654–1735 becomes `Wand Maker of the Ruined World`,
>    set in an elegant high-contrast display serif, title case, on one line, filling comparable width.
> 2. The circled volume mark at x 1110–1185 keeps its ring and its numeral `4`, optically aligned at
>    the end of the title line.
> 3. The small letterspaced Latin line at x 115–643, y 1761–1776 becomes `Wand Maker of the Ruined World`.
>    Keep it small and letterspaced, clearly subordinate — it reads as a decorative sub-title, which is
>    why the repetition works rather than looking like a duplicated string.
> 4. The credit line becomes `Kurodome Hagane`, then the smaller role label `Illustrator`, then
>    `Kayahara`, in a thin clean sans serif, preserving the source's order and generous word spacing.
>    Keep `Illustrator` visually distinct as a label; do not merge it into either name.
>
> **Colour:** sample the source's own core ink green from its densest glyph pixels and use it for all
> replaced type. Do not invent a green and do not shift hue between elements.
>
> Render every English string verbatim with exact capitalization and spacing. `Wand Maker` is two
> words everywhere; the one-word form `Wandmaker` must not survive. Do not paraphrase, omit,
> duplicate beyond the two intentional title occurrences, abbreviate, translate or invent text.
>
> All English upright, horizontal, left-to-right. No vertical or rotated lettering, no one-letter-per-line
> stacking, no added boxes, rules or ornaments. Professional kerning, optical alignment, even
> letterspacing. Nothing may extend above y 1584 into the illustration.
>
> **Targeted typography correction:** set the large title in
> `/home/yogesh/.local/share/fonts/lightnovel/PlayfairDisplay-500.ttf`, with `Wand Maker` and
> `Ruined World` at 69 px and `of the` at 48 px (0.696×), sharing one baseline with balanced
> spacing. Set the subordinate tracked title in
> `/home/yogesh/.local/share/fonts/lightnovel/PlayfairDisplay-400.ttf` at 22 px. Set all three
> credit runs in `/home/yogesh/.local/share/fonts/lightnovel/Montserrat-300.ttf`, retaining
> their current sizes, placements, hierarchy, and spacing. Keep the volume ring at 3 px without
> moving its box, and set its `4` in Playfair Display Medium.

---

## Editing and refinement record

### Pass A — source and continuity edit

- Every region transcribed from magnified crops of the white field, not from a page-level read.
- Title and author checked against `novel.config.md` rather than retranslated; both are locked values.
- `かやはら` → `Kayahara` matches the filed Volume 1–3 frontmatter specs; no macron.
- The volume mark reads `④` and becomes `4`; confirmed it is the fourth volume against the config's
  source→volume map.
- Confirmed the `Illustrator` role label is already Latin in the source and needs no translation.
- Measured that all six text elements lie wholly within the white field, so the illustration is
  untouched — the one fact that makes this plate a safe composite.

**Pass A: complete**

### Pass B — publication-English refinement

- No prose to refine; this is display copy. The refinement decisions are typographic.
- The source's Latin sub-title prints the banned one-word alias. It is corrected in place rather
  than dropped, because it is a deliberate design element of the plate.
- **Considered dropping the sub-title entirely.** Once the main title is English, the small line
  repeats it exactly, and a duplicated title can read as a translation artifact rather than a design
  choice. Retained on the evidence of the accepted Volume 3 plate, where the line is set small and
  widely letterspaced and reads as a decorative rule-like element, not as a repeated string. Keeping
  it also holds the frontispiece consistent across the four filed volumes.
- Credit line keeps the source's `name — role — name` order rather than being restructured into an
  English `Story by / Art by` pairing, matching Volumes 1–3.
- A targeted comparison against the accepted Volume 3 plate selected Playfair Display Medium (500)
  over Regular (400): both supply the precedent's broad Playfair-class proportions, Didone contrast,
  and ball terminals, but 400 remained visibly lighter than the accepted pink plate at this fitted
  size. The 500 cut has the fuller stems and more confident colour requested without approaching the
  heaviness of 700. The smaller `of the` preserves the accepted internal hierarchy.

**Pass B: complete**

---

## Notes and uncertainties

- **No unresolved or illegible text.** All six elements resolved cleanly.
- **The illustration contains no localizable text.** It is the same scene as the cover in a wider,
  uncropped framing. Painted set dressing — the utility poles, the distant buildings, the bicycle and
  the road furniture — carries no legible signage, so nothing in the artwork needs treatment.
- The white field is pure RGB(255,255,255) edge to edge, so masking the old type and re-setting is
  exact; there is no gradient or texture to reconstruct.

---

## Render record

- **Method:** deterministic Pillow composite onto the original pixels. No image-generation model.
- **Output:** `English/Volume 4/localized-images/kuchie-001.jpg` — real JPEG, RGB, 1440 × 2048, quality 95, 4:4:4.
- **Illustration gate:** y 0–1583 MAD vs source **0.00**, differing pixels **0**. The artwork is untouched.
- **White field:** all four canvas corners RGB(255,255,255).
- **Colour:** green RGB(168,209,130), sampled as the modal value of dense interior glyph pixels after a 5 × 5 erosion, so anti-aliased edges could not lighten it.
- **Readback:** all five strings read off the rendered image at magnification. Both title occurrences read `Wand Maker of the Ruined World` with `Wand Maker` as two words. No Japanese and no `Wandmaker` survives.
- **Source integrity:** SHA-256 unchanged.

### Typography — three passes, and why

| Element | Face | Size |
|-|-|-|
| Title `Wand Maker` / `Ruined World` | `PlayfairDisplay-500` | 69 px |
| Title connector `of the` | `PlayfairDisplay-500` | 48 px (0.696×) |
| Sub-title | `PlayfairDisplay-400` | 22 px, 7 px tracking |
| Credits | `Montserrat-300` | 30 / 24 / 28 px |
| Numeral `4` | `PlayfairDisplay-500` | 32 px, 3 px ring |

Title ink spans x 113–1097, matching the source's x 113–1109 without horizontal distortion.

**Pass 1 rejected — wrong class of face.** Left to choose for itself, the renderer used Nimbus Roman,
a Times clone. That is a *body* face; at 69 px display size it read word-processed rather than
art-directed. It is a plausible-looking wrong answer that survives QA unless it is put beside the
precedent. **Lesson recorded in the skill: name the exact font file, never describe the face.**

**Pass 2 rejected — right idea, wrong weight.** Noto Serif Display Light restored the hierarchy but
was too thin and slightly condensed beside the Volume 3 plate, which is fuller and wider.

**Pass 3 accepted.** Playfair Display is the Didone class the precedent actually belongs to. Weight
500 was chosen over 400 by measurement: 400 was visibly lighter and 11 px narrower at the same size.

The second half of the lesson is that the family alone was not enough — the Volume 3 plate sets its
connector words smaller than the phrases around them, and a line set at one uniform size reads flat
even with the correct face. The 0.696× ratio restores that.

- **Status:** accepted.
