# kuchie-004 — colour frontispiece spread, Spider Witch

- **Source:** `Source/Volume 4/images/kuchie-004.jpg` — JPEG, RGB, 2048 x 1456
- **Output:** `English/Volume 4/localized-images/kuchie-004.jpg`
- **Scene:** the giant Spider Witch on the tunnel ceiling, Ori's inverted face at right, and a chibi
  spider vignette at lower left.
- **Chapter:** `Source/Volume 4/11 蜘蛛の魔女.md` lines 325-349, filed as
  `English/Volume 4/Chapter 8 - Spider Witch.md` lines 215-231.

## Text-bearing regions

Four. The small speech balloon beside the inverted face is **empty in the source** — pure art,
verified at magnification. So is the drawn `?` in the chibi vignette at lower left, and the row of
glowing dots below the left-hand column. None of them carry text.

| # | Region | Ink box (native px) | Colour |
|-|-|-|-|
| 1 | Title, small Latin `Spider Witch` | x1546-1744, y80-119 | yellow, RGB(231, 201, 128) |
| 1 | Title, large kanji 蜘蛛の魔女 | x1461-1719, y127-161 | yellow, RGB(229, 198, 128) |
| 2 | Spider Witch's line, 1 column | x122-160, y173-837 | white, soft dark glow |
| 3 | Ori's line, 2 columns | x1461-1562, y916-1344 | white, soft dark glow |
| 4 | Ori's narration, 14 columns | x409-893, y848-1219 | white, soft dark glow |

Region 3 columns, right to left: x1527-1562 · x1461-1500.

Region 4 is a dense block of 14 evenly spaced columns on a 36 px pitch, from x877-893 at the right
to x409-425 at the left.

## Verbatim Japanese by region

### Region 1 — title

Small Latin line: `Spider Witch`. Large kanji line: `蜘蛛の魔女`.

### Region 2 — the Spider Witch, 1 column

```
「どうして怖がってないの……？」
```

### Region 3 — Ori, 2 columns RTL

```
「いいなぁ。
機能美生物だ……！」
```

### Region 4 — Ori's narration, 14 columns RTL

Seven source paragraphs, set as fourteen columns. Column breaks fall inside paragraphs; the
paragraph boundaries are what carry meaning and are what the English must preserve.

```
1  蜘蛛ってだけでストライクなのに、
2  この巨大サイズ！　カッケェ～！
3  どこ住みですか？　ご趣味は？　主食はやっぱ人間？
4  俺は昔から蜘蛛が好きだ。だって器用だから。
5  蜘蛛は生まれながらにして
6  あの幾何学的な放射状の巣を紡ぐ事ができる。
7  誰にも教わる事なく、本能で糸の操り方を識っているのだ。
8  彼らは生来の職工なのである！
9  すげぇよな。流石に尊敬する。生物として優秀すぎるぞ。
10 俺の中で蜘蛛はダム作りの達人ビーバーと並ぶ
11 リスペクト生物二大巨頭だ。
12 俺がキラキラした宝石のような
13 複眼を見つめ感嘆していると、
14 大蜘蛛は昆虫っぽいカクッとした動きで首を傾げた。
```

Paragraph mapping: columns 1-2 · 3 · 4 · 5-8 · 9 · 10-11 · 12-14.

All four regions match the chapter source character for character. The source prints ruby on
`識[し]って` and `傾[かし]げた`; both resolve to plain English and carry no ruby in the output.

## Exact English by region

### Region 1 — title

```
Spider Witch
```

Set **once**, in the large kanji slot. The source stacks a small Latin line over a larger Japanese
line saying the same thing; in English that is the same title printed twice.

### Region 2 — the Spider Witch

```
“Why aren't you scared...?”
```

### Region 3 — Ori

```
“Nice. It's a creature of functional beauty...!”
```

### Region 4 — Ori's narration, seven paragraphs in this order

```
It was already right in my strike zone just for being a spider, and it was this huge! So cool!

So, where do you live? Hobbies? Are humans your main food?

I've always liked spiders. Because they're dexterous.

Spiders could spin those geometric radial webs from the moment they were born. Without anyone teaching them, they knew instinctively how to handle thread. They were craftsmen from birth!

Amazing, right? I seriously respect them. They're way too good at being alive.

To me, spiders and beavers, the masters of dam building, shared the top spot among animals I respected.

As I stared at those sparkling, jewel-like compound eyes and marveled, the giant spider tilted its head with an insect-like, jerky movement.
```

All strings are the filed chapter prose verbatim. The filed translation is the wording authority.

## Terminology decisions

| Source | English | Authority |
|-|-|-|
| 蜘蛛の魔女 | `Spider Witch` | `glossary.md:27`; `Witch of Spiders` is a **banned alias** |
| 機能美生物 | `a creature of functional beauty` | filed prose |
| 職工 | `craftsmen` | filed prose |
| リスペクト生物二大巨頭 | `shared the top spot among animals I respected` | filed prose |
| 複眼 | `compound eyes` | filed prose |

## Layout decision

All four regions are vertical in the source and become horizontal, left-to-right English.

**Region 2** moves to **x60-500, y200-390**, in the dark upper left where the Japanese column
already ran. It clears the spider's red eye markings, which begin near x740.

**Region 3** moves to **x1440-1900, y960-1140**, over the same hair and glow the Japanese column
crossed. It stays well below the inverted face, which ends near y840.

**Region 4** moves to **x400-1010, y800-1250** — 610 x 450 against the Japanese block's 484 x 371,
because English needs more room than vertical Japanese for the same content. The right edge stops at
x1010 to clear the cocooned figure hanging at x1030-1120, and the box sits below the spider's legs.
Measured roughness there is 8.2 against 15.0 for the original vertical footprint, so the narration
sits on markedly flatter ground than the Japanese did.

**Region 1** is consolidated to a single English label in the kanji slot.

### Dense-text handling for Region 4

- Keep all **seven paragraph boundaries**. They are the semantic units; the fourteen columns are
  only how the Japanese happened to wrap.
- Set paragraph spacing visibly larger than line spacing — roughly 0.6 to 1.0 line.
- One consistent body size and consistent leading throughout. Do not solve fit by crushing leading
  or tracking, and do not scatter the paragraphs across the artwork.
- Left-aligned, ragged right, in one compact block.

## Production prompt

```
Use case: text-localization

Asset type: colour frontispiece spread from a Japanese light novel, 2048 x 1456.

Input image: the provided image is the edit target. Edit it. Do not regenerate the illustration.

Primary request: replace every piece of Japanese text with English, and nothing else.

  1. Title, upper right. The source stacks a small yellow Latin line reading "Spider Witch"
     (x1546-1744, y80-119) over a larger yellow kanji line 蜘蛛の魔女 (x1461-1719, y127-161), both
     saying the same thing. Remove BOTH lines and set the title ONCE, in the lower and larger slot,
     in the same yellow: RGB(229, 198, 128). Match the wide letterspacing the source's own Latin
     line uses.

  2. The Spider Witch's line: one vertical white column at x122-160, y173-837. Remove it,
     reconstruct the dark background beneath, and set the English horizontally, left to right,
     inside x60-500, y200-390.

  3. Ori's line: two vertical white columns at x1461-1562, y916-1344. Remove them, reconstruct the
     hair and glow beneath, and set the English horizontally, left to right, inside
     x1440-1900, y960-1140.

  4. Ori's narration: a dense block of fourteen vertical white columns at x409-893, y848-1219.
     Remove them, reconstruct the dark tunnel beneath, and set the English horizontally, left to
     right, inside x400-1010, y800-1250, as SEVEN separate paragraphs in the order given below.
     Paragraph spacing must be visibly larger than line spacing. Use one consistent body size and
     one consistent leading for the whole block. Left-aligned, ragged right.

  All three dialogue and narration regions are white with the same soft dark outer glow the source's
  white type carries, so the text stays legible where it crosses from light to dark background.

Text invariants (verbatim):

  Spider Witch

  “Why aren't you scared...?”

  “Nice. It's a creature of functional beauty...!”

  It was already right in my strike zone just for being a spider, and it was this huge! So cool!

  So, where do you live? Hobbies? Are humans your main food?

  I've always liked spiders. Because they're dexterous.

  Spiders could spin those geometric radial webs from the moment they were born. Without anyone teaching them, they knew instinctively how to handle thread. They were craftsmen from birth!

  Amazing, right? I seriously respect them. They're way too good at being alive.

  To me, spiders and beavers, the masters of dam building, shared the top spot among animals I respected.

  As I stared at those sparkling, jewel-like compound eyes and marveled, the giant spider tilted its head with an insect-like, jerky movement.

  Reproduce every string exactly — capitalization, punctuation, the curly quotation marks and
  apostrophes, the three-dot ellipses, and the exclamation and question marks. Do not paraphrase,
  translate, omit, abbreviate, duplicate, merge or invent text, and do not drop a paragraph.

Constraints:
  - The small speech balloon beside the inverted face at the right is EMPTY in the source. It stays
    empty. Do not put text in it and do not alter its outline.
  - The drawn "?" in the chibi spider vignette at lower left is artwork, not text. Leave it exactly
    as it is. The same goes for the row of glowing dots below the left-hand column.
  - No Japanese character anywhere in the output.
  - All English upright, horizontal, left to right. No vertical, rotated, mirrored or stacked
    lettering, and no one-letter-per-line stacking.
  - Protect the artwork absolutely: the giant spider, its body, legs, fangs and red eye markings;
    the inverted face and hair at the right; the cocooned figure hanging at x1030-1120; the chibi
    spider vignette at lower left; the tunnel arches and web strands.
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

- All four regions match the chapter source character for character; no plate-only variant text.
  The last narration column was verified to the final glyph, ending 首を傾げた.
- Speaker attribution verified from the filed chapter: the Spider Witch asks the left-hand question,
  Ori speaks the right-hand line and carries the narration. Each block is placed on its speaker's
  side.
- `蜘蛛の魔女` renders as `Spider Witch` per glossary; the banned alias `Witch of Spiders` appears
  nowhere.
- The source's ruby on `識[し]って` and `傾[かし]げた` is semantically identical to its base and
  resolves to plain English by the project's ruby convention; no ruby in the output.
- Register holds: Ori's narration keeps its enthusiast's rush — a run of short exclamations and
  rhetorical questions — and the filed English carries that without elevating it.
- The narration's tense follows the project's narrative-past lock, as filed.

**Pass B — publication-English refinement: complete.**

Reread all four regions independently as finished display copy. The narration reads as connected
paragraphs rather than isolated sentences: the opening two beats land as excitement, the middle
turns to the admiring explanation of web-spinning, and the last paragraph returns to the action and
hands off to the Spider Witch's question. No calques, stiff syntax or computer-like phrasing to
rewrite. Wording is left exactly as filed, so plate and chapter stay identical.

## Notes and uncertainties

- Region 4 is the densest block in this volume so far — seven paragraphs where the other plates
  carried one or two lines. The likeliest failure is a dropped or merged paragraph, so each of the
  seven must be checked individually on the render.
- The empty balloon and the drawn `?` are both at risk from a generative renderer that reads them as
  places text belongs. Verify both at magnification.
- No uncertainties in transcription. All four regions were read at magnification and every glyph is
  legible.

## Render record

**Status: accepted.**

### Method — generative edit, merged back over the source

`imagegen` was driven through Codex headless in image-edit mode, three calls. The text came out
right on the third; the artwork did not. As on every plate in this volume, the model regenerated the
whole canvas — spider silhouette, leg joints, the red eye markings' shapes and spacing, the inverted
face, the cocooned figure's proportions and the chibi vignette were all redrawn.

The accepted file keeps the model's work only inside the four text regions and restores the source
everywhere else, using the standard dilate-then-blur alpha with per-region colour matching.

Merge rectangles: title `1445,72-1805,208` · Spider Witch's line `90,165-305,845` ·
Ori's line `1450,908-1785,1352` · narration `380,822-1030,1370`.

Each is the union of the source's Japanese block and the render's English block. The colour offsets
this page needed were the largest so far — up to 16.9 on the title — because the render shifted the
palette substantially. The title join was checked at magnification regardless and is seamless.

### Verification — read off the rendered image, not the renderer's report

- Title reads `Spider Witch` once, in the kanji slot, in the source's yellow with wide
  letterspacing. The two-tier duplicate is gone. The banned alias `Witch of Spiders` appears
  nowhere.
- Both dialogue lines verified verbatim at magnification, including the curly quotation marks and
  apostrophes, the three-dot ellipses and the terminal `?` and `!`.
- **All seven narration paragraphs are present, in order, none merged or dropped**, with paragraph
  spacing visibly larger than line spacing. This was the page's main risk and it held.
- **The speech balloon is still empty** and is the source's own outline — MAD 0.50. The renderer had
  redrawn it; the merge discarded that. The chibi `?` and the glowing dots are likewise source
  pixels.
- No Japanese survives. The Spider Witch's column ran to y837 while the English occupies only
  y260-328; the vacated stretch below was checked at magnification and shows clean reconstructed
  art with no residue.
- Protected art MAD vs source: spider body and red eyes 0.41, inverted face and hair 0.50,
  cocooned figure 0.77, chibi vignette 0.65, speech balloon 0.50.
- Output: real JPEG, RGB, 2048 x 1456, quality 95, subsampling 0 (4:4:4), 1,062,906 bytes.

### Deviations from the spec's target boxes

- The title rendered at x1453-1795, y144-199 against a target of x1461-1719, y127-161 — wider and
  lower. Accepted: it sits in open panel space, clear of the inverted face.
- The narration rendered at x387-1020, y832-1360 against a target of x400-1010, y800-1250,
  overrunning the bottom by 110 px. Accepted: the extra depth is below the spider's legs and clear
  of the chibi vignette.
- The final narration paragraph is indented on all three of its lines while the other six are flush
  left. The renderer wrapped it around the chibi vignette's circular glow, which is a legitimate
  runaround rather than a typographic error. Accepted in preference to re-rolling seven paragraphs
  that are otherwise correct.

### Glossary

No terms added. `機能美生物` -> `a creature of functional beauty` is a one-off coinage, appearing
exactly once in the entire corpus, so a glossary row would prevent no drift; plate and chapter
already agree. `職工` -> `craftsmen` and `複眼` -> `compound eyes` are ordinary vocabulary and were
likewise left out.
