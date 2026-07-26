# Image Localization Spec — kuchie-002.jpg

## Source image path and type

- Source: `English/Volume 3/images/kuchie-002.jpg`
- Type: two-panel color character illustration with reaction copy and character labels; JPEG, 2048 × 1473

## Verbatim Japanese

1. Upper-left white reaction copy:
   - `秘伝のタレに漬けた`
   - `魔物肉！`
   - `ウマい！`
2. Lower-left blue character label:
   - `青の魔女`
3. Right orange character label:
   - `大日向慧`
4. Existing English labels:
   - `Blue Witch`
   - `Kei Ohinata`

## English Localization

1. Upper-left reaction:
   - `Monster meat soaked in secret sauce!`
   - `Delicious!`
2. Lower-left character label:
   - `Blue Witch`
3. Right character label:
   - `Ohinata Kei`

## Edit Prompt

Edit `English/Volume 3/images/kuchie-002.jpg` as the image-edit target. Preserve the full 2048 × 1473 landscape canvas, crop, diagonal two-panel geometry, both depictions of the characters, faces, eyes, hair, ears, tail, anatomy, poses, hands, chopsticks, meat, clothing, room, windows, sparks, lighting, palette, texture, and every non-text artwork detail exactly.

Replace only the listed text:

- Replace the upper-left white brush copy `秘伝のタレに漬けた / 魔物肉！ / ウマい！` with the exact two-line English reaction `Monster meat soaked in secret sauce!` and `Delicious!`.
- Consolidate the lower-left two-line label `Blue Witch / 青の魔女` into one exact label: `Blue Witch`.
- Consolidate the right two-line label `Kei Ohinata / 大日向慧` into one exact label: `Ohinata Kei`.

Reaction treatment: keep the copy in the upper-left brown negative space, away from the hanging meat and chopsticks. Use energetic hand-painted white brush lettering with the same informal, excited character and source hierarchy. Set all words upright, horizontal, and left-to-right. Use two compact phrase-based lines, with `Delicious!` larger and punchier than the first line. Preserve both exclamation marks exactly. Do not rotate the block.

Blue Witch label: keep it in the existing lower-left negative space. Use the same medium blue, small classic serif/display lettering, scale, and optical alignment as the source label. Render `Blue Witch` once only.

Ohinata label: keep it in the existing right-side negative space, clear of her face, ear, hair, raised thumb, and body. Use the same warm orange, small classic serif/display lettering, scale, and alignment as the source label. Render `Ohinata Kei` once only, in Japanese family-name-first order. Remove the incorrect `Kei Ohinata`.

Quoted English is verbatim copy. Require exact capitalization and punctuation: `Monster meat soaked in secret sauce!`, `Delicious!`, `Blue Witch`, and `Ohinata Kei`. Permit no paraphrase, omission, duplication, invented text, or leftover targeted Japanese.

Use professional kerning, leading, optical alignment, and balanced line lengths. Forbid vertical or rotated English, one-letter-per-line stacking, mirrored text, generic subtitles, meme captions, and unrequested boxes. Protect every face, eye, hand, body, food item, and focal detail.

Before returning the edit, perform visual QA: confirm all four required strings and exclamation marks are exact; no targeted Japanese or `Kei Ohinata` remains; no extra or duplicated label appears; all English is horizontal LTR; nothing is clipped or overlapping; and the artwork and panel geometry are unchanged.

## Notes / Uncertainties

- All listed Japanese is legible.
- `secret sauce`, `monster meat`, `Blue Witch`, and `Ohinata Kei` follow the glossary and filed Volume 3 prose.
- The lower-left and right labels are consolidated to avoid redundant English duplicates while preserving the source's color-coded character-label hierarchy.
