# Image Localization Spec — kuchie-002

## Source Image Path + Type
`Source/Volume 4/images/kuchie-002.jpg` — character montage; text-bearing.

## Verbatim Japanese
- Character label: `青の魔女`
- Character label: `大利賢師`
- Dialogue region, lower left: `「ヒヨリの目とかスゲェ綺麗な青色してるしさぁ、髪も青かかってるし、好きの色が特に無いならペットもヒヨリの持ち味の色彩に合わせた方がハマるんじゃねぇの」`
- Dialogue region, center: `「なんで俺のペットと色合わせするんだよ」`
- Dialogue region, center: `「なんでって……それは……」`
- Dialogue region, right: `「んー。確かにキュアノスも御守りも青だし……寒色系で合わせるのもアリか。大利的にはどうなんだ？　赤が好きか？　大利の火蜥蜴たちの色に合わせるのもアリな気がしてきた」`
- Dialogue region, lower right: `「いいなぁ。機能美生物だ……！」`
- Existing roman label beside `大利賢師`: `Kenshi Ori`

## English Localization
- `Blue Witch`
- `Ori Kenshi`
- `Hiyori's eyes are this amazing blue, and her hair has blue in it too. If you don't have a favorite color, wouldn't a pet that matches Hiyori's color scheme suit you better?`
- `Why would I match my pet to my color scheme?`
- `Why? Well... that's...`
- `Hmm. Cyanos and the amulet are both blue too... Going with cool colors could work. What about you, Ori? Do you like red? Matching the colors of Ori's fire salamanders might work too.`
- `Nice. A functionally beautiful creature...!`
- Replace the existing reversed-order roman label `Kenshi Ori` with `Ori Kenshi`.

## Edit Prompt
Use `Editing/image-localization-typesetting-style.md`. Replace only each transcribed Japanese label and dialogue region with its paired English line. Also replace only the existing roman label `Kenshi Ori` with the glossary-locked Japanese name order `Ori Kenshi`; retain the existing roman `Blue Witch` label. Use the illustrated-dialogue category (Noto Sans SemiBold, 1.12 line height, 0.45-line paragraph spacing), preserving each region's line breaks as far as English permits, color, glow, weight, and placement. Do not add dialogue to the empty speech balloon. Do not alter the bird inset or any art.

## Notes / Uncertainties
`キュアノス` is rendered as `Cyanos` per glossary. `Kenshi Ori` is a banned reversed-order form under the glossary's `大利賢師` entry, so this spec explicitly authorizes correcting that existing roman label.
