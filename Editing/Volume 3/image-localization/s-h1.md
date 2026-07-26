# Image Localization Spec — s-h1.jpg

## Source image path and type

- Source: `English/Volume 3/images/s-h1.jpg`
- Type: color Volume 3 booklet cover featuring Himori Wand; JPEG, 1440 × 2048

## Verbatim Japanese

1. Upper-left red booklet label:
   - `極秘資料`
2. Right-side vertical series title:
   - `崩壊世界の魔法杖職人`
3. Large lower-left red seal:
   - `秘`
4. Small engraving on the wand handle:
   - `火守乃杖`
5. Volume numeral:
   - `③`

## Existing English requiring correction

- `Wandmaker of the Ruined World`

## English Localization

1. Booklet label:
   - `Top Secret Files`
2. Series title:
   - `Wand Maker of the Ruined World`
3. Large seal:
   - `SECRET`
4. Wand engraving:
   - `Himori Wand`
5. Volume numeral:
   - retain `3`
6. Correct the existing subtitle to:
   - `Wand Maker of the Ruined World`

## Edit Prompt

Edit `English/Volume 3/images/s-h1.jpg` as the image-edit target. Preserve the full 1440 × 2048 portrait canvas, crop, aged fibrous paper texture, cream/red/brown palette, central hanging lantern, flame, frame, tassels, smoke-like black wand form, upright wand and handle, brush textures, red side blocks, circular seal geometry, margins, lighting, and every non-text artwork detail exactly.

Replace only the listed text:

- Replace upper-left `極秘資料` with `Top Secret Files`.
- Replace the right-side vertical Japanese series title with `Wand Maker of the Ruined World`.
- Replace the large red seal character `秘` with `SECRET`.
- Replace the small handle engraving `火守乃杖` with `Himori Wand`.
- Retain the bottom-right volume number as `3`.
- Correct the existing small red English subtitle `Wandmaker of the Ruined World` to the exact configured title `Wand Maker of the Ruined World`.

Booklet-label treatment: use large distressed red display lettering in the upper-left negative space, matching the source's stamped texture and weight. Keep it clear of the lantern and left red blocks.

Series-title treatment: set `Wand Maker of the Ruined World` as an upright horizontal red serif title in the white right-side strip. Wrap by complete words into a balanced compact block; do not rotate it, stack individual letters, or let it touch the wand or page edge.

Seal treatment: retain the original large distressed circular red seal and replace only its internal character with the centered word `SECRET` in bold distressed stamp lettering. The English may wrap as complete syllable-free words only if necessary, but do not stack individual letters vertically.

Handle treatment: place `Himori Wand` as two compact horizontal lines (`Himori` / `Wand`) within the original dark handle plaque. Use small pale engraved lettering. Preserve the plaque shape and all handle shading.

Small-subtitle treatment: keep the existing two-line red typewriter/serif hierarchy and location, but render the exact words `Wand Maker of` / `the Ruined World`. Keep it clear of the lantern.

Quoted English is verbatim copy. Require exact capitalization and spacing: `Top Secret Files`, `Wand Maker of the Ruined World`, `SECRET`, `Himori Wand`, and `3`. Permit no `Wandmaker`, paraphrase, omission, duplicate decorative copy beyond the intentional two title occurrences, invented text, or leftover targeted Japanese.

All English must be upright, horizontal, and left-to-right. Forbid vertical or rotated English, one-letter-per-line stacking, mirrored text, generic subtitles, added logos, barcodes, publisher marks, watermarks, or unrequested boxes. Protect the lantern, flame, tassels, smoke-wand silhouette, upright wand, handle, seal outline, and all focal artwork.

Before returning the edit, perform visual QA: confirm all required strings and capitalization are exact; the configured series title appears exactly twice (right title and small subtitle); `Top Secret Files`, `SECRET`, `Himori Wand`, and `3` each appear once; no targeted Japanese or `Wandmaker` remains; no text is clipped or overlapping; the handle engraving is readable; and the cover artwork is otherwise unchanged.

## Notes / Uncertainties

- `火守乃杖` follows the glossary's locked rendering `Himori Wand`.
- The right-side title follows `novel.config.md` exactly.
- The red seal is confidently legible as `秘`; it is functional cover text, not an abstract mark.
