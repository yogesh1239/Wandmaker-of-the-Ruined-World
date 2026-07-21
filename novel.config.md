# Novel Config — Wand Maker of the Ruined World

The per-novel knobs the harness reads. The `/build-epub` skill derives the JSON that `core/scripts/build_epub.py --config` needs from the values here.

## Identity
- **Title (JP):** 崩壊世界の魔法杖職人
- **Title (EN):** Wand Maker of the Ruined World
- **Type:** Japanese light novel
- **Genre / setting:** Post-apocalyptic modern fantasy and survival story set in Japan after civilization collapsed and magic emerged.
- **Author:** Kurodome Hagane

## Source ebooks → volumes

| Vol | Source file | Format | Extraction |
|-|-|-|-|
| 1 | `崩壊世界の魔法杖職人１ - 黒留 ハガネ.epub` | epub | `split_ebook.py` direct |
| 2 | `崩壊世界の魔法杖職人２　小冊子付き特装版【電子特典付き】.epub` | epub | `split_ebook.py` direct |
| 3 | `崩壊世界の魔法杖職人３【電子特典付き】.epub` | epub | `split_ebook.py` direct |

## Paths
- Source (split chapters + images): `Source/Volume N/`
- Output (drafts, assembled chapters, EPUBs): `English/Volume N/`
- Edit logs / reconciliation / image specs: `Editing/Volume N/`

## Conventions
- **Romanization:** no macrons; use vowel-doubling (`ou`, `uu`, `aa`, `ii`, `ee`). Enforced by `core/scripts/normalize_romaji.py --check`.
- **Reading direction:** source is RTL → build EPUB as **LTR** (`page-progression-direction="ltr"`).
- **Furigana:** preserved from source as `漢字[かな]`.
- **Part-split threshold:** 400 source lines — chapters longer than this split into parts; shorter ones translate/edit whole.
- **qa_major_threshold:** 3 — QA fails if a chapter has more than three major findings, or any critical finding.

## Register lock
**Status:** LOCKED
**Register:** Casual / Comedy
**Evidence:** Volume 1 used short, plain first-person narration, blunt self-commentary, frequent casual interjections, and fast gag-like reactions such as 「マジじゃん!?」 and 「魔石やんけ！」; English stayed contemporary, direct, and unornamented.

## Chapter-title map
Single source of truth for output filenames and EPUB `<h1>`/TOC/contents-image titles. Rows followed each volume's primary Contents in order; secondary booklet-internal reference entries were excluded.

| Vol | N | JP title | EN title |
|-|-|-|-|
| 1 | 1 | そして文明は滅んだ | And Then Civilization Fell |
| 1 | 2 | サバイバル、魔法を添えて | Survival, with a Side of Magic |
| 1 | 3 | 青の魔女 | The Blue Witch |
| 1 | 4 | オーバーテクノロジー | Overtechnology |
| 1 | 5 | 竜炉彫七層型青魔杖キュアノス | Dragon-Furnace-Carved Seven-Layer Blue Wand Cyanos |
| 1 | 6 | 魔女がいる暮らし | Life with a Witch |
| 1 | 7 | 東京魔女集会 | Tokyo Witches' Council |
| 1 | 8 | 魔法言語学 | Magic Linguistics |
| 1 | 9 | 東京魔法大学 | Tokyo Magic University |
| 1 | 10 | 励起魔力感応吸音鑑定法 | Magic-Excitation Acoustic Appraisal |
| 1 | 11 | 竜の魔女 | The Dragon Witch |
| 1 | 12 | 番外編　ペットロス | Side Story - Pet Loss |
| 1 | 13 | 崩壊世界の魔法杖職人 １ 特装版小冊子　極秘資料 | Wand Maker of the Ruined World 1 Special Edition Booklet - Top Secret Files |
| 1 | 14 | 電子書籍特典　書き下ろし短編『【晶雨】』 | Ebook Bonus Original Short Story - Crystal Rain |
| 2 | 1 | 便利魔法を覚えよう | Let's Learn Useful Magic |
| 2 | 2 | 奥多摩の山奥に、ＵＭＡを見た！ | I Saw a UMA Deep in the Okutama Mountains! |
| 2 | 3 | 煙草の魔女 | The Tobacco Witch |
| 2 | 4 | 融解再凝固グレムリン | Melt-Recast Gremlin |
| 2 | 5 | 魔力逆流防止機構 | Backlash-Prevention Mechanism |
| 2 | 6 | グレムリン工学教授、その経歴 | The Gremlin Engineering Professor's Career |
| 2 | 7 | 白指たち | The White Fingers |
| 2 | 8 | 地獄の魔女 | The Hell Witch |
| 2 | 9 | 村を襲う悪い鬼 | The Bad Oni Who Attacked the Village |
| 2 | 10 | 儀式魔法十三祭具 | The Thirteen Ritual Implements |
| 2 | 11 | 港区奪還作戦 | Minato Ward Recapture Operation |
| 2 | 12 | バイオハザード・パンデミック | Biohazard Pandemic |
| 2 | 13 | 花の魔女 | The Flower Witch |
| 2 | 14 | 三歩進んで二歩下がる | Three Steps Forward, Two Steps Back |
| 2 | 15 | アミュレット | Amulet |
| 2 | 16 | 世界を広げて | Expanding the World |
| 2 | 17 | 番外編　この主人公はワシが育てた | Side Story - I Raised This Protagonist |
| 2 | 18 | 崩壊世界の魔法杖職人 ２ 特装版小冊子　極秘資料 | Wand Maker of the Ruined World 2 Special Edition Booklet - Top Secret Files |
| 2 | 19 | 電子書籍特典　書き下ろし短編『大利の絵』 | Ebook Bonus Original Short Story - Oori's Picture |
| 3 | 1 | 魔法系統カスタマイズ | Magic-School Customization |
| 3 | 2 | 東北狩猟組合の秘伝 | Secret Techniques of the Touhoku Hunting Association |
| 3 | 3 | 継火の魔女 | The Flame Witch |
| 3 | 4 | 火守乃杖 | Himori Wand |
| 3 | 5 | 闇商人、０９３３を語る | A Black Marketeer Talks About 0933 |
| 3 | 6 | 魔物素材を活用しよう | Let's Put Monster Materials to Use |
| 3 | 7 | 火蜥蜴 | Fire Salamander |
| 3 | 8 | 北海道魔獣農場の秘伝 | Secret Techniques of the Hokkaidou Magic Beast Farm |
| 3 | 9 | 火蜥蜴といっしょ | Together with the Fire Salamanders |
| 3 | 10 | 魔獣たち | The Magic Beasts |
| 3 | 11 | 無名叙事詩仮説 | The Nameless Epic Hypothesis |
| 3 | 12 | 新時代の新通貨 | New Currency for a New Era |
| 3 | 13 | 銃杖巨神殺し | Gun-Wand Giant Slayer |
| 3 | 14 | そんな人間、いるわけない | No One Like That Could Exist |
| 3 | 15 | 英雄の証 | Proof of a Hero |
| 3 | 16 | 吹奏儀式魔法七祭具 | The Seven Wind-Instrument Ritual Implements |
| 3 | 17 | 魔力を測ろう！ | Let's Measure Magic Power! |
| 3 | 18 | 番外編　赤いのさんびき、青いのひとり | Side Story - Three Red Ones, One Blue One |
| 3 | 19 | 崩壊世界の魔法杖職人 ３ 小冊子　極秘資料 | Wand Maker of the Ruined World 3 Booklet - Top Secret Files |
| 3 | 20 | 電子書籍特典　書き下ろし短編『フクロスズメ馴致手引き』 | Ebook Bonus Original Short Story - Pouch Sparrow Taming Guide |

## EPUB metadata (per volume)
- **Series:** Wand Maker of the Ruined World
- **Title pattern:** `Wand Maker of the Ruined World, Vol. N`
- **Language:** en
- **Original:** 崩壊世界の魔法杖職人 — Kurodome Hagane
- **Cover / colophon:** retain the Japanese cover and colophon as-is; retain original publisher/legal matter in Japanese.
- **Volume 1 title / source edition:** *Wand Maker of the Ruined World, Vol. 1* — special edition with booklet and ebook bonus; issued 2025-09-25.
- **Volume 2 title / source edition:** *Wand Maker of the Ruined World, Vol. 2* — special edition with booklet and ebook bonus; issued 2025-11-25.
- **Volume 3 title / source edition:** *Wand Maker of the Ruined World, Vol. 3* — ebook bonus edition; issued 2026-03-25.
- **Spine / image-page policy:** derive each source EPUB spine at build time; retain front cover, title, character, and contents image pages, localizing text-bearing images where specified; absorb standalone interior illustrations into their chapter at the source image marker; preserve the Japanese colophon and end-logo page.
