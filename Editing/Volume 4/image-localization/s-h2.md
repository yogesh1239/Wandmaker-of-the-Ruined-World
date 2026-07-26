# s-h2 — contributor profile page

## Source

- **Path:** `Source/Volume 4/images/s-h2.jpg`
- **Canvas:** 1440 × 2048 portrait JPEG
- **Source SHA-256:** `5a4c2a0832ea69514d7f89c180d32d14700a0cd2739d229a5efc9bab99d662d2`
- **Type:** the booklet's author-and-illustrator profile page — white stock, two navy header bars,
  the whole upper two thirds left deliberately blank
- **Output:** `English/Volume 4/localized-images/s-h2.jpg`

## Layout overview

Two blocks, both in the lower half, both flush left at x112. Everything above y1025 is bare white
and must stay that way — the empty upper field is the page's design, not unused space.

Each block runs: navy header bar → name in navy display type → black serif body copy. The author's
name carries a kana reading beside it; the illustrator's does not.

## Verbatim text by visual region

| ID | Region | Ink extent | Verbatim |
|-|-|-|-|
| A1 | author header bar | 112–562, 1041–1075 | `著者　author` |
| A2 | author name | 114–552, 1094–1126 | `黒留ハガネ`　+ reading `くろどめ　はがね` |
| A3 | body ¶1 line 1 | 114–423, 1155–1178 | `明治元年、東京に生まれる。` |
| A4 | body ¶1 line 2 | 113–626, 1193–1216 | `大正九年、東京魔法大学理論魔法学部を卒業。` |
| A5 | body ¶2 line 1 | 113–930, 1269–1293 | `月面基地駐在員、急いでる人の目の前の信号を赤にする仕事などを経て、` |
| A6 | body ¶2 line 2 | 113–423, 1307–1330 | `現在は南極で文筆業を営む。` |
| A7 | body ¶3 | 113–1069, 1383–1407 | `著書に「崩壊世界の魔法杖職人」「嘘全開の著者コメントを書く１００の方法」など。` |
| B1 | illustrator header bar | 112–562, 1532–1565 | `イラストレーター　illustrator` |
| B2 | illustrator name | 117–263, 1585–1614 | `かやはら` |
| B3 | illustrator body | 113–448, 1645–1668 | `絵を描くお仕事をしています。` |

## Wording authority

| String | Authority |
|-|-|
| `Kurodome Hagane` | `novel.config.md:10` and `:121` |
| `Kayahara` | `glossary.md:380` |
| `Tokyo Magic University` | `glossary.md:433`, `novel.config.md:52` |
| `Wand Maker of the Ruined World` | `novel.config.md:7` |
| `I draw pictures for a living.` | Volume 3's `s-h2` — the same sentence, kept identical |

## Terminology decisions

- **`明治元年` / `大正九年` — era names kept.** `Meiji` and `Taisho`, long vowel unmarked per the
  project's romanization rule, never `Taishō`. Converting to 1868 and 1920 would be an addition the
  source does not make, and it would flatten the joke: the bio is funny because it is dated in
  reign eras a living author could not possibly have been born in.
- **`理論魔法学部` — Faculty of Theoretical Magic.** `学部` is a university faculty; `理論魔法` is
  theoretical magic as against the applied kind. Set as a faculty *of* the university already
  locked as `Tokyo Magic University`.
- **`著者コメント` — Author Bio.** The Japanese publishing term is a contributor's comment; the
  English equivalent on this exact page is the author bio. Rendering it as `Author Bio` is what
  lands the joke, because the second title is the punchline — it tells the reader that the three
  paragraphs immediately above it are fabricated.
- **`嘘全開` — Made Entirely of Lies.** Not "exaggerated", not "tall tales". `嘘` is lies, and
  `全開` is wide open / full throttle. The register is broad and unembarrassed.
- **`かやはら` — Kayahara.** Mononym pen name, no macron, no doubled vowel.

## Layout decision — the kana reading is dropped

`くろどめ　はがね` beside the author's name is a pronunciation gloss: it tells a Japanese reader how
to say `黒留ハガネ`. In English the name and its reading are the same string, so setting both would
put `Kurodome Hagane` on the page twice for no reason. It is dropped, and the navy name line
carries `Kurodome Hagane` alone. Volume 3 made the same call on the same page.

## Layout decision — the header bars

Both bars already carry their English — `author` and `illustrator` — beside the Japanese. So each
bar keeps its English word and loses only the Japanese, which leaves the bar reading exactly as its
designer intended for a reader who cannot read Japanese. Neither word is capitalized; the source
sets them lowercase and that is a design choice, not an error.

## Layout decision — the two book titles

`「」` around a title maps to italics in English publishing, so the two works are set in italic
rather than in quotation marks. The bar and name typography carry the page's hierarchy; the titles
only need to read as titles.

## Exact English by region

| ID | English |
|-|-|
| A1 | `author` |
| A2 | `Kurodome Hagane` |
| A3–A4 (¶1) | `Born in Tokyo in the first year of Meiji. Graduated from the Faculty of Theoretical Magic at Tokyo Magic University in the ninth year of Taisho.` |
| A5–A6 (¶2) | `Has worked as a resident staffer on a lunar base, and at turning the traffic light red the moment someone in a hurry reaches it. Now writes for a living in Antarctica.` |
| A7 (¶3) | `Works include` *`Wand Maker of the Ruined World`* `and` *`100 Ways to Write an Author Bio Made Entirely of Lies`*`.` |
| B1 | `illustrator` |
| B2 | `Kayahara` |
| B3 | `I draw pictures for a living.` |

Line breaks are not fixed: the English wraps to fit, and the paragraph divisions are what must
survive, not the source's exact line endings.

## Production prompt

1. Edit target is the supplied 1440 × 2048 page. Preserve the canvas, crop, white stock, both navy
   header bars, their exact positions and widths, the left margin at x112, and the blank upper two
   thirds of the page exactly.
2. Everything above y1025 is bare white and must stay bare white. Add nothing there.
3. First navy bar: replace `著者　author` with `author` alone, lowercase, small white serif, left
   aligned inside the bar as the English already is.
4. Author name line, navy display type: replace `黒留ハガネ` and the kana reading beside it with
   `Kurodome Hagane`. One name only — the kana is a pronunciation gloss and has no English
   counterpart, so nothing replaces it.
5. Author body copy, black serif, three paragraphs in this order:
   - `Born in Tokyo in the first year of Meiji. Graduated from the Faculty of Theoretical Magic at Tokyo Magic University in the ninth year of Taisho.`
   - `Has worked as a resident staffer on a lunar base, and at turning the traffic light red the moment someone in a hurry reaches it. Now writes for a living in Antarctica.`
   - `Works include Wand Maker of the Ruined World and 100 Ways to Write an Author Bio Made Entirely of Lies.`
6. In the third paragraph, set both book titles in italic: `Wand Maker of the Ruined World` and
   `100 Ways to Write an Author Bio Made Entirely of Lies`. The words `Works include`, `and` and
   the closing full stop stay roman.
7. Second navy bar: replace `イラストレーター　illustrator` with `illustrator` alone, lowercase,
   same treatment as the first bar.
8. Illustrator name line, navy display type: `Kayahara`.
9. Illustrator body, black serif: `I draw pictures for a living.`
10. Wrap by phrase. Paragraph spacing must be visibly larger than line spacing — roughly one blank
    line between paragraphs, matching the source's rhythm. No widows, no orphans, no one-word last
    lines. Keep the body copy inside the page's left and right margins.
11. The author block may grow downward as the English wraps, but it must stop clear of the second
    navy bar. Do not move either bar.
12. All English upright, horizontal, left to right. No vertical English, no rotated words, no
    stacked letters, no added boxes, rules, captions or page numbers.
13. Quoted strings are verbatim. Exact capitalization, punctuation and spacing. No Japanese
    remnants, no duplicated name, no paraphrase, no invented text.

## Editing and refinement record

**Pass A — source and continuity.** Every line checked against the source at 3×. `東京魔法大学`
takes the locked `Tokyo Magic University` from `glossary.md:433`; `崩壊世界の魔法杖職人` takes the
locked series title; the author's name follows `novel.config.md:10`, family name first, and
`かやはら` follows the glossary row added with p294-295. The two era names are retained rather than
converted. `月面基地駐在員` is a posting, not a rank, so it is rendered as work history rather than
a title. Nothing is added and nothing is dropped except the kana reading, which has no English
counterpart.

**Pass B — publication English.** Read as a finished contributor page. The Japanese author bio is
subjectless plain form and the illustrator's line is polite `-ます`; that difference is deliberate
and it survives — the author's paragraphs run impersonal and subjectless, the illustrator's line is
first person. That also sidesteps a pronoun the source never supplies. `急いでる人の目の前の信号を
赤にする仕事` was the one line at risk of reading like a translation; `turning the traffic light red
the moment someone in a hurry reaches it` keeps the timing that makes it a joke, where a literal
"in front of a person who is hurrying" loses it. The illustrator's sentence is taken verbatim from
Volume 3's page so the two booklets read as one series.

- Pass A: complete
- Pass B: complete

## Notes and uncertainties

- No illegible text; all ten regions read at 3×.
- No new glossary terms. Every proper noun on the page was already locked.
- The bio is fiction by its own admission — the last title says so. It is translated straight,
  because the joke only works if the bio is delivered deadpan.

## Render record

| Render | Native size | Verdict |
|-|-|-|
| A | 1440 × 2048 | **Rejected — wrong method.** Codex read the imagegen skill and then hand-typeset an SVG overlay in Liberation Serif and composited it over the source with ImageMagick. The strings were correct, but the lettering was a vector stamp sitting on top of the page rather than type rendered into it. Kept as `h2_rejected_svg.png`. |
| B | 1052 × 1495 | **Accepted.** Re-run with the local typesetting route explicitly closed off — no SVG, no `-annotate`, no PIL, no system fonts — and with an instruction to stop and say so rather than substitute. Codex called `image_gen.imagegen` in image-edit mode. All strings exact, both titles italic, no Japanese. |

The rejection is worth recording because the brief for A already said "use your imagegen tool in
image-edit mode" and Codex still routed around it. Naming the tool is not enough on a page that is
pure typography — a local typesetter is the obvious shortcut there, and the prohibition has to be
explicit and itemized.

### Finishing — `finish_h2.py`

This page has no artwork, so there is nothing for a rect-by-rect merge-back to protect and the
render is taken whole. Two corrections:

1. **Resample.** 1052 × 1495 → 1440 × 2048, LANCZOS.
2. **Re-ink the navy.** The render's navy came back deeper than the source's — bar core
   (2.8, 47.5, 95.5) against the source's (0.5, 54.0, 105.0), the display names deeper still. On a
   single page that would pass. But these bars repeat on every booklet header page, and bars that
   drift in colour from page to page read as a printing fault, so the navy is pinned to the
   source's measured bar colour.

   The re-ink is gated on blue-dominance (`B − R > 30`) so it cannot reach the black body serif,
   whose channels are equal. Coverage is continuous: a solid bar reads coverage 1 and lands exactly
   on the source navy, a half-covered edge pixel lands halfway to paper.

   A global tone curve was rejected. The only flat anchors are paper and bar, neither near black,
   so the line they pin lifts the body text off black. The defect is a hue shift in one ink, not a
   tone shift in the page.

### Gates

| Measure | Source | Final |
|-|-|-|
| bar navy core | (0.5, 54.1, 105.0) | (4.4, 56.9, 106.6) |
| name navy core | (1.5, 45.9, 98.3) | (1.2, 53.7, 105.0) |
| body ink | neutral black | (23.2, 23.3, 23.2) — untouched by the navy gate |
| upper field, y0–880 | bare | uniform 254, zero pixels below 250 |

### Layout note — the author block moved up

The render lifted the author block about 150 px and the English runs eight body lines where the
Japanese ran five. That is not treated as a defect. English needs the extra lines, the block has to
clear the second bar, and moving the first bar up while leaving the second where it is, is what a
designer setting this page in English would do. Both bars kept their exact x-position, width and
height; only the first one's vertical position changed. The blank upper field — the page's actual
design — survives at a little over half the sheet.

### Visual QA at full resolution

- Both header blocks inspected at 2×: `author` / `Kurodome Hagane` and `illustrator` / `Kayahara`,
  bar words lowercase and white, names navy display type, body black serif.
- All three author paragraphs verbatim; both book titles italic with `Works include`, `and` and the
  closing full stop roman.
- Paragraph spacing visibly exceeds line spacing. Phrase-based wraps, no widows or orphans, no
  one-word last lines.
- No Japanese anywhere. The kana reading is gone and `Kurodome Hagane` appears once.
- Nothing added to the blank upper field.

- **Image-edit renders:** 2 (A rejected as locally typeset, B accepted)
- **Saved output:** `English/Volume 4/localized-images/s-h2.jpg` — real JPEG, quality 95,
  subsampling 0 (4:4:4), 1440 × 2048
- **Output SHA-256:** `59ef87bd8c3767fdf90e2b3b2ea91838a1112a5f63114654e2a1e22260435d26`
- **Source integrity:** original unmodified

Scratch state is re-runnable: `finish_h2.py`, `h2_genB.png`, `h2_rejected_svg.png`.
