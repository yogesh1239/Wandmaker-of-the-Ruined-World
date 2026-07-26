# Image Localization Spec — kuchie-004.jpg

## Source image path and type

- Source: `English/Volume 3/images/kuchie-004.jpg`
- Type: color fire-salamander character collage with names, cries, and dialogue; JPEG, 2048 × 1473

## Verbatim Japanese

1. Three large red-outlined fire-salamander cries:
   - `「ミィー」`
   - `「ミィッー」`
   - `「ミィー」`
2. Yellow name labels paired with existing English romanization:
   - `セキタン` / `Sekitan`
   - `ツバキ` / `Tsubaki`
   - `モクタン` / `Mokutan`
3. Right-side white dialogue:
   - `「すごいなこれは。`
   - `よくここまで`
   - `調教できたものだ」`
4. Lower-center pale-cyan dialogue:
   - `「それほどでもある。`
   - `二カ月かけたし」`
5. Several small decorative handwritten marks near the feeding and inset scenes:
   - not confidently legible

## English Localization

1. Three cries:
   - `“Mii!”`
   - `“Mii!”`
   - `“Mii!”`
2. Character labels:
   - `Sekitan`
   - `Tsubaki`
   - `Mokutan`
3. Right dialogue, matching the filed chapter:
   - `“This is amazing. You trained them this well.”`
4. Lower-center dialogue, matching the filed chapter:
   - `“It is pretty impressive. I did spend two months on it.”`

## Edit Prompt

Edit `English/Volume 3/images/kuchie-004.jpg` as the image-edit target. Preserve the full 2048 × 1473 landscape canvas, crop, collage geometry, every fire salamander, person, face, anatomy, pose, hand, chopsticks, coal, bowl, flame, grass, sky, building, inset scene, lighting, palette, texture, and every non-text artwork detail exactly.

Replace only the confidently legible listed text:

- Replace each of the three large red-outlined Japanese cries with the exact cry `“Mii!”`, for three total occurrences.
- Consolidate `Sekitan / セキタン` into one label `Sekitan`.
- Consolidate `Tsubaki / ツバキ` into one label `Tsubaki`.
- Consolidate `Mokutan / モクタン` into one label `Mokutan`.
- Replace the right-side white dialogue with `“This is amazing. You trained them this well.”`
- Replace the lower-center pale-cyan dialogue with `“It is pretty impressive. I did spend two months on it.”`
- Leave the small uncertain decorative handwritten marks unchanged. Do not guess, reconstruct, or translate them.

Cry treatment: keep each cry near its original salamander in the existing negative space. Use energetic white display lettering with a vivid red outline matching the source SFX hierarchy. Set each `“Mii!”` upright, horizontal, and left-to-right; do not rotate it or stack letters.

Name-label treatment: keep each name in its original location and saturated yellow. Use one clean, compact classic serif/display label per salamander, with the same scale and soft glow. Each name appears once only.

Dialogue treatment: place the Blue Witch's line as a compact horizontal white serif block in the right-side negative space above the two human figures, clear of faces, bodies, grass, and the training demonstration. Place Ori's reply as a separate horizontal pale-cyan serif block in the lower-center negative space, clear of Tsubaki, flames, and the human figures. Preserve the source's distinct speaker colors. Use balanced phrase-based wrapping, comfortable leading, and subtle source-matched shadows.

Quoted English is verbatim copy. Require exact capitalization and punctuation: three occurrences of `“Mii!”`, `Sekitan`, `Tsubaki`, `Mokutan`, `“This is amazing. You trained them this well.”`, and `“It is pretty impressive. I did spend two months on it.”`. Permit no paraphrase, omission, extra occurrence, invented text, or leftover targeted Japanese.

All English must be upright, horizontal, and left-to-right. Forbid vertical or rotated English, one-letter-per-line stacking, mirrored text, generic subtitles, meme captions, and unrequested boxes. Use professional kerning, leading, optical alignment, and balanced line lengths. Protect every character, creature, face, hand, food item, flame, and focal detail.

Before returning the edit, perform visual QA: confirm all required strings, quotation marks, and punctuation are exact; there are exactly three `“Mii!”` cries and one of each name; no targeted Japanese remains; uncertain marks remain unchanged; no text is clipped or overlapping; and the artwork is otherwise unchanged.

## Notes / Uncertainties

- The dialogue matches `English/Volume 3/Chapter 10 - The Magic Beasts.md`, lines 41–43.
- The fire-salamander cry is rendered as `Mii` in the filed chapter.
- Small handwritten reaction marks are not confidently legible; they must remain unchanged under the zero-hallucination rule.
