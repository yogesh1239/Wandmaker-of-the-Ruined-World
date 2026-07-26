# Image Localization Spec — s-h2.jpg

## Source image path and type

- Source: `English/Volume 3/images/s-h2.jpg`
- Type: author and illustrator profile page; JPEG, 1440 × 2048

## Verbatim Japanese

### Author section

- `著者`
- `黒留ハガネ`
- `くろどめ　はがね`
- `一度覚えた創作ノウハウは全て紙に書いて部屋のドアに貼っている。`
- `新しい技術やコツを覚えると、`
- `古い物の重要度を無意識に下げたり忘れたりしてしまう悪癖があるから、`
- `何千回でも見て思い出すために。`
- `だからドアはメモ書きで埋まっている。`

### Illustrator section

- `イラストレーター`
- `かやはら`
- `絵を描くお仕事をしています。`

## English Localization

### Author section

- `author`
- `Kurodome Hagane`
- `I write down every bit of creative know-how I learn and stick it to my bedroom door.`
- `Whenever I learn a new technique or trick, I have a bad habit of unconsciously treating the old ones as less important or forgetting them, so I keep them there to look at and remind myself thousands of times.`
- `That's why my door is covered in notes.`

### Illustrator section

- `illustrator`
- `Kayahara`
- `I draw pictures for a living.`

## Edit Prompt

Edit `English/Volume 3/images/s-h2.jpg` as the image-edit target. Preserve the full 1440 × 2048 portrait canvas, crop, white background, large upper negative space, dark-blue header bars, section positions, margins, spacing, and all non-text design exactly.

Replace only the listed Japanese text. Remove the duplicate kana pronunciation line under the author's Japanese name rather than creating a second English name.

Set the author section in this order:

1. Dark-blue header bar: `author`
2. Dark-blue name: `Kurodome Hagane`
3. First paragraph: `I write down every bit of creative know-how I learn and stick it to my bedroom door.`
4. Second paragraph: `Whenever I learn a new technique or trick, I have a bad habit of unconsciously treating the old ones as less important or forgetting them, so I keep them there to look at and remind myself thousands of times.`
5. Third paragraph: `That's why my door is covered in notes.`

Set the illustrator section in this order:

1. Dark-blue header bar: `illustrator`
2. Dark-blue name: `Kayahara`
3. Body line: `I draw pictures for a living.`

Typography: preserve the source hierarchy. Use small white sans-serif text inside each dark-blue header bar, bold dark-blue sans-serif/display type for names, and compact black serif body copy. Keep all English upright, horizontal, and left-to-right. Use phrase-based line wrapping, comfortable leading, and clearly larger paragraph spacing. Keep the author and illustrator sections in their original lower-page positions and leave the large upper field blank.

All quoted English is verbatim copy. Require exact capitalization, punctuation, and apostrophes. `Kurodome Hagane` and `Kayahara` each appear once. Permit no Japanese remnants, duplicated names, invented text, vertical English, rotated words, mirrored text, clipped lines, or additional boxes.

Before returning the edit, perform visual QA: confirm every English string is exact; paragraph order is correct; paragraph spacing exceeds line spacing; no Japanese remains; the upper blank area stays blank; no text is clipped or overlapping; and the page design is otherwise unchanged.

## Notes / Uncertainties

- The author's name follows `novel.config.md`: `Kurodome Hagane`.
- `かやはら` is romanized as `Kayahara`, without macrons or long-vowel doubling.
- The prose is newly translated because no filed English counterpart was found for this contributor-profile page.
