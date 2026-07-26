# Image Localization Spec — s-h2.jpg

## Source

- Image: `English/Volume 2/images/s-h2.jpg`
- Type: special-edition booklet contents page
- Canvas: 1440 × 2048 JPEG, portrait
- Wording authority: `novel.config.md`, `glossary.md`, `character-reference.md`, the Volume 1 filed booklet contents terminology, and `Source/Volume 2/21 Contents.md`

## Text Regions

The existing English heading `Contents` is already correct and must remain unchanged.

| Region | Verbatim Japanese | Exact English |
|---|---|---|
| Upper section heading | キャラクター紹介 | Character Profiles |
| Entry, page 3 | 煙草の魔女 | Tobacco Witch |
| Entry, page 4 | 地獄の魔女 | Hell Witch |
| Entry, page 6 | 花の魔女 | Flower Witch |
| Entry, page 8 | 入間の魔法使い | Iruma Mage |
| Entry, page 10 | 継火の魔女 | Flame Witch |
| Entry, page 12 | 京極大和 | Kyogoku Yamato |
| Entry, page 13 | 垂田紀見 | Dareda Kimi |
| Entry, page 14 | 半田作之助 | Handa Sakunosuke |
| Lower entry, page 15 | ２巻の各話解説 | Volume 2 Chapter Commentary |
| Lower entry, page 18 | キノコ病について | About Mushroom Disease |
| Lower entry, page 19 | 魔法道具紹介 | Magic Item Showcase |
| Lower entry, page 22 | ２巻時点での年表 | Timeline as of Volume 2 |
| Lower entry, page 24 | 東京都内住居地人気ランキング | Tokyo Residential Area Popularity Rankings |
| Lower entry, page 26 | 東京魔法大学 | Tokyo Magic University |
| Lower entry, page 28 | 作品設定 | Setting Notes |
| Lower entry, page 31 | ショートストーリー | Short Stories |
| Lower entry, page 35 | 奥付 | Colophon |

All page numbers and leader rules remain exactly as drawn.

## Production Edit Prompt

Use case: text-localization

Edit target: the supplied `s-h2.jpg`. Produce a finished official-English-edition booklet contents page.

Replace only the Japanese strings listed above with their quoted exact English strings. Retain the existing English word `Contents`, all page numbers, every blue horizontal leader rule, the white paper background, canvas, crop, margins, spacing system, and restrained navy-blue print aesthetic.

Typeset every English replacement upright, horizontal, and left-to-right. Use the same dark navy as the source. Match the existing editorial serif character where practical: a dignified medium-weight serif for names and entries, with the upper section heading slightly bolder and larger. Do not use generic sans-serif subtitles, boxes, shadows, outlines, gradients, or decorative effects.

Preserve the two-part hierarchy and reading order:

1. Upper `Character Profiles` heading.
2. Eight profile entries with page numbers 3, 4, 6, 8, 10, 12, 13, and 14.
3. Lower list from `Volume 2 Chapter Commentary` through `Colophon`, with the existing page numbers.

Lay out each entry as one clean horizontal line wherever it fits. For the longest entry, `Tokyo Residential Area Popularity Rankings`, reduce its type size moderately before considering a two-line wrap; if wrapping is unavoidable, break after `Area`, keep both lines left-aligned as one compact block, and preserve visibly comfortable leading. Maintain consistent baselines, optical alignment, page-number alignment, and leader-rule endpoints. Do not compress tracking or crowd adjacent rows.

Exact text is mandatory. Do not paraphrase, omit, duplicate, translate the already-English `Contents`, alter any numeral, or add any text. Remove all targeted Japanese cleanly with no visible remnants. No vertical English, rotated words, mirrored letters, one-letter-per-line stacking, clipped text, watermark, or artwork changes.

## Notes and Uncertainties

- No illegible text was found.
- `Magic Item Showcase` is a natural contents-label rendering of 魔法道具紹介; no filed Volume 2 prose version exists because the booklet section is image-only.
- The existing English heading and all numbers are excluded from replacement.
