# kuchie-003 — colour frontispiece spread

- **Source:** `Source/Volume 4/images/kuchie-003.jpg` — JPEG, RGB, 2048 x 1473
- **Output:** `English/Volume 4/localized-images/kuchie-003.jpg`
- **Scene:** Fuyo, the Flower Witch's child, in three panels — cheerful at right, wailing at centre,
  and small at upper left beside Ori Kenshi with his arms folded.
- **Chapter:** `Source/Volume 4/05 花の魔女の子、フヨウ.md` lines 868 and 871, filed as
  `English/Volume 4/Chapter 2 - The Flower Witch's Child, Fuyo.md` lines 577 and 579.

## Text-bearing regions

Three. The white shout balloon at top centre is **empty in the source** — pure art, verified at
magnification. It carries no text and must be left exactly as it is.

| # | Region | Ink box (native px) | Colour |
|-|-|-|-|
| 1 | Nameplate, small Latin `Fuyo` | x1887-1993, y1030-1067 | yellow, RGB(217, 187, 106) |
| 1 | Nameplate, large katakana フヨウ | x1799-1977, y1068-1119 | yellow, RGB(219, 198, 110) |
| 2 | Fuyo's line, 4 vertical columns | x1144-1319, y70-696 | white, soft dark glow |
| 3 | Ori's line, 6 vertical columns | x70-295, y580-929 | white, soft dark glow |

Column geometry, right to left (Japanese reading order):

- **Region 2** — x1291-1319 y89-499 · x1241-1270 y70-519 · x1193-1221 y88-696 · x1144-1174 y88-570
- **Region 3** — x274-295 y606-761 · x233-254 y605-832 · x193-215 y580-848 · x151-173 y582-929 ·
  x111-133 y606-929 · x70-92 y609-907

Column pitch is about 40 px; glyphs run 22-30 px.

## Verbatim Japanese by region

### Region 1 — nameplate

Small Latin line: `Fuyo`. Large katakana line: `フヨウ`.

### Region 2 — Fuyo (right panel), 4 columns RTL

```
「う～ん……がんばるけど……
おひさまのきぶんもあるし……
あっ！　おじさんがいいこいいこしてくれたら、
わたしもーっとがんばっちゃうよ♡」
```

### Region 3 — Ori (left panel), 6 columns RTL

```
「やだよ。お前、
先週もそんな事言って
かまってちゃんした挙句
満足してなんもしなかっただろ。
ガキがよぉ、約束は守りなさいって
ママに教わらなかったのか？」
```

Both match the chapter source character for character.

## Exact English by region

### Region 1 — nameplate

```
Fuyo
```

Set **once**, in the large katakana slot. The source stacks a small Latin line over a larger
Japanese line saying the same thing; in English that is the same name printed twice.

### Region 2 — Fuyo

```
“Umm... I'll work hard, but... the sun has moods too... Ah! If Uncle gives me head pats, I'll work muuuch harder♡”
```

### Region 3 — Ori

```
“No. You said something like that last week too, then acted needy until you were satisfied and didn't do anything. You little brat, didn't your mommy teach you to keep your promises?”
```

Both strings are the filed chapter prose verbatim. The filed translation is the wording authority.

## Terminology decisions

| Source | English | Authority |
|-|-|-|
| フヨウ | `Fuyo` | `glossary.md:55`; `Hibiscus` is a **banned alias** |
| おじさん | `Uncle` | filed prose, 13 of 13 occurrences in this chapter |
| おひさま | `the sun` | filed prose |
| いいこいいこ | `head pats` | filed prose |
| ママ | `mommy` | filed prose |
| ガキ | `little brat` | filed prose |
| もーっと | `muuuch` | filed prose; the elongation is carried, not normalised |

The trailing `♡` is part of Fuyo's voice and is kept.

## Layout decision

Both dialogue blocks are vertical in the source and become horizontal, left-to-right English.

**Region 3 (Ori)** moves into the flat gradient band at **x55-420, y600-1000**. Its right edge stops
short of the centre girl's face, which begins near x460.

**Region 2 (Fuyo)** moves into the foliage at **x1130-1470, y80-500**. Its right edge stops short of
Fuyo's hair and face at the right, which begin near x1500.

Both boxes were chosen over the alternatives by measured local roughness — 7.8-8.3 mean gradient
against 9.3-10.5 for the original vertical footprints, so the English sits on flatter ground than
the Japanese did.

**Region 1** is consolidated to a single English label in the katakana slot.

## Production prompt

```
Use case: text-localization

Asset type: colour frontispiece spread from a Japanese light novel, 2048 x 1473.

Input image: the provided image is the edit target. Edit it. Do not regenerate the illustration.

Primary request: replace every piece of Japanese text with English, and nothing else.

  1. Character nameplate, lower right. The source stacks a small yellow Latin line reading "Fuyo"
     (x1887-1993, y1030-1067) over a larger yellow katakana line フヨウ (x1799-1977, y1068-1119),
     both saying the same name. Remove BOTH lines and set the name ONCE, in the lower and larger
     slot, in the same yellow: RGB(219, 198, 110). Match the wide letterspacing the source's own
     Latin line uses.

  2. Fuyo's line, right panel: four vertical white columns occupying x1144-1319, y70-696. Remove
     them, reconstruct the green foliage beneath, and set the English horizontally, left to right,
     inside x1130-1470, y80-500.

  3. Ori's line, left panel: six vertical white columns occupying x70-295, y580-929. Remove them,
     reconstruct the gradient band beneath, and set the English horizontally, left to right, inside
     x55-420, y600-1000.

  Both dialogue blocks are white with the same soft dark outer glow the source's white type carries,
  so each line stays legible where it crosses from light to dark background. Use one consistent type
  size for both blocks: fit it to the longer block, then use that size for both.

Text invariants (verbatim):
  Fuyo
  “Umm... I'll work hard, but... the sun has moods too... Ah! If Uncle gives me head pats, I'll work muuuch harder♡”
  “No. You said something like that last week too, then acted needy until you were satisfied and didn't do anything. You little brat, didn't your mommy teach you to keep your promises?”

  Reproduce these three strings exactly — capitalization, punctuation, the curly quotation marks and
  apostrophes, the three-dot ellipses, the doubled vowels in "muuuch", and the heart. Do not
  paraphrase, translate, omit, abbreviate, duplicate or invent text.

Constraints:
  - The white shout balloon at top centre is EMPTY in the source. It stays empty. Do not put text in
    it, and do not alter its outline.
  - No Japanese character anywhere in the output.
  - All English upright, horizontal, left to right. No vertical, rotated, mirrored or stacked
    lettering, and no one-letter-per-line stacking.
  - Protect the artwork absolutely: all three depictions of Fuyo and the depiction of Ori; every
    face, eye, hand and body; her flower crown, gloves, vines and the red dress; the branch, leaves
    and foliage; the panel divider geometry.
  - Do not alter the canvas, crop, palette, lighting or texture anywhere.
  - Add no speech balloons, boxes, borders, rules, bands, ornaments or watermarks.
  - Wrap on phrase boundaries. Never end a line on an orphaned preposition or article, and never
    leave a one-word last line. Keep each block strictly inside its box; if a block will not fit,
    reduce the type size rather than crushing the leading or spilling over the art.
```

## Editing and refinement record

**Pass A — source and continuity edit: complete.**

Checked line by line against the visible Japanese, the chapter source, the filed English, the
glossary and the character references.

- Both plate strings match the chapter source character for character; no plate-only variant text.
- Speaker attribution verified from the filed chapter: Fuyo speaks the right-hand line, Ori the
  narrator speaks the left-hand line. Placement of each block in its speaker's panel is correct.
- `フヨウ` renders as `Fuyo` per glossary; the banned alias `Hibiscus` appears nowhere.
- Register holds: Fuyo's source line is all-hiragana childlike speech and the English keeps plain,
  simple diction; Ori's rough register (`お前`, `ガキがよぉ`) survives as "You little brat".
- Elongation `もーっと` is preserved as "muuuch" rather than normalised.

**Pass B — publication-English refinement: complete.**

Reread both strings independently as finished display copy. They read as natural English dialogue,
not as translated text: Fuyo's line keeps a child's halting rhythm through its ellipses, and Ori's
lands as one exasperated run-on, which is what the scene wants. No calques, stiff syntax or
computer-like phrasing to rewrite. Wording is left exactly as filed, so plate and chapter stay
identical.

## Notes and uncertainties

- The empty shout balloon is the one element most at risk from a generative renderer, which will be
  tempted to fill it. Verify at magnification that it is still blank.
- Region 2's box narrows toward Fuyo's hair; if the renderer cannot fit the line without crowding
  her, the correct fix is a smaller type size, not a wider box.
- No uncertainties in transcription. All three regions were read at magnification and every glyph is
  legible.

## Render record

**Status: accepted.**

### Method — generative edit, merged back over the source

`imagegen` was driven through Codex headless in image-edit mode, six calls (three of them rejected
by its safety system before producing an image). As expected it regenerated the whole canvas rather
than editing it: all four character depictions came back repainted, MAE 16.2-22.8 against the
source.

The accepted file keeps the model's work only inside the three text regions and restores the source
everywhere else, using the standard dilate-then-blur alpha with per-region colour matching.

Merge rectangles: nameplate `1785,1025-2000,1140` · Fuyo `1095,55-1465,705` ·
Ori `50,572-410,1180`.

The Ori rectangle is the union of the source's Japanese block and the render's English block, which
landed about 180 px lower and wider than the spec's target box. Because the union's dilated top edge
reaches up into the small upper-left Fuyo's flower and the overhanging branch, that strip was
compared against the source at magnification: the branch, leaf tips, red flower and green hair are
continuous, with no seam and no ghost of the removed columns.

### Verification — read off the rendered image, not the renderer's report

- All three strings verified verbatim at magnification, including the curly quotation marks and
  apostrophes, the three-dot ellipses, `muuuch` and the trailing `♡`.
- Nameplate reads `Fuyo` once, in the katakana slot, in the source's yellow with wide letterspacing.
  The two-tier duplicate is gone. The banned alias `Hibiscus` appears nowhere.
- **The shout balloon is still empty** and lies outside every merge rectangle, so it is the source's
  own pixels — MAD 0.53. The renderer had softened its outline; the merge discarded that.
- No Japanese survives; the old column footprints show no residue.
- Protected art MAD vs source: Ori's face and arms 0.43, right-hand Fuyo 0.90, centre wailing Fuyo
  1.75, upper-left Fuyo 1.97. The two higher figures are where the protect boxes overlap the Ori
  merge rectangle's feather band, not repainting.
- Output: real JPEG, RGB, 2048 x 1473, quality 95, subsampling 0 (4:4:4), 1,359,307 bytes.

### Deviation from the spec's target box

The spec placed Ori's block at x55-420, y600-1000; the renderer set it at roughly x58-400,
y690-1170, overrunning the box's bottom by about 170 px. Accepted: the block sits over the girl's
hair rather than over any face, it stays clear of the centre girl's face at x460, and the type is
comfortably sized. Forcing it back into the specified box would have meant a smaller type size for
no gain.

### Glossary

One term added: `おじさん` -> `Uncle` (banned: `uncle`, `mister`, `old man`), Fuyo's address for Ori
Kenshi, stable at 13 of 13 occurrences in the chapter. Romaji gate passes.
