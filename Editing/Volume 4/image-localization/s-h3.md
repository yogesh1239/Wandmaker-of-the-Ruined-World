# s-h3 — booklet colophon (no localization)

## Source

- **Path:** `Source/Volume 4/images/s-h3.jpg`
- **Canvas:** 1440 × 2048 portrait JPEG
- **Source SHA-256:** `7fb3124de0f832e3de6a192046e1a95984577045a364f81495041791be05092b`
- **Type:** the booklet's colophon — pale-grey stock, publisher and editorial credits low on the
  page, copyright line at the foot, the upper half left blank
- **Output:** `English/Volume 4/localized-images/s-h3.jpg` — a byte-identical copy of the source

## Verbatim text by visual region

| Region | Ink extent | Content |
|-|-|-|
| Booklet line | 114–518, 1197–1219 | `崩壊世界の魔法杖職人４　小冊子` |
| Booklet title | 113–319, 1242–1282 | `極秘資料` |
| Publisher | 114–590, 1376–1401 | `発行　　株式会社KADOKAWA` |
| Editorial | 114–526, 1433–1457 | `編集　　ＭＦ文庫Ｊ編集部` |
| Design credit | 115–818, 1488–1515 | `デザイン　　ムシカゴグラフィクス（たにごめかぶと）` |
| Legal line | 114–567, 1916–1936 | `© Hagane Kurodome 2026　Printed in Japan` |

## Localization decision — no render, original retained

`novel.config.md:122` sets the edition policy: *"retain the Japanese cover and colophon as-is;
retain original publisher/legal matter in Japanese."* This page is the colophon in full — it is
nothing but publisher, editorial, design and copyright matter. Localizing it is not a judgement
call the spec gets to make; the configured policy forbids it.

The reasoning behind that policy holds here plainly. A colophon is a record of who actually
published this book, in Japan, in Japanese. `株式会社KADOKAWA` is a legal entity's registered name,
`ＭＦ文庫Ｊ編集部` is a named editorial department, and `ムシカゴグラフィクス（たにごめかぶと）` is
a design studio and the individual designer credited inside it. Rendering any of them in English
would assert a name those parties do not use. The copyright line is already partly Latin and is a
legal notice besides — it says what it says.

Note that the legal line sets the author given-name-first, `Hagane Kurodome`, where the rest of this
edition uses `Kurodome Hagane`. That is the publisher's own Latin rendering inside a copyright
notice, and it is retained exactly as printed rather than reconciled with the project convention.

Filed precedent: Volume 3's colophon ships byte-identical to its source, SHA-256
`a2dbd4169de1e40d906d1c38f20aeb20ad7ca76eee0afd35868293114899e476` on both. Volume 4 follows.

## Why a copy is shipped rather than nothing

Unlike the gaiji glyphs or the retailer logo, this page ships into the build as a page. Placing a
byte-identical copy in `localized-images/` keeps the build's page list uniform — every booklet page
resolves from the same directory — without changing a pixel. The alternative, special-casing this
one filename to read from `Source/`, buys nothing and invites a build-time miss.

## Notes and uncertainties

- No illegible text; all six regions read at 3×.
- Pass A and Pass B are recorded as not applicable rather than complete: no string on this page is
  translated, so there is no embedded English to edit.
- No new glossary terms.

- **Image-edit renders:** 0 — intentional
- **Saved output:** `English/Volume 4/localized-images/s-h3.jpg`, byte-identical to the source
- **Source integrity:** original unmodified
