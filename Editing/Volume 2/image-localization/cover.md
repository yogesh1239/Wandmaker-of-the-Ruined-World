# Image Localization Spec — cover

## Source Image Path + Type

`Source/Volume 2/images/cover.jpg` — front cover / title artwork; text-bearing.

Apply the shared typography and preservation rules in `Editing/image-localization-typesetting.md`. Do not introduce a Volume 2-only font or display system.

## Verbatim Japanese

- Main vertical title: `崩壊世界の魔法杖職人`
- Edition line, upper left: `小冊子付き`
- Edition line, upper left: `特装版`
- Volume mark: `②`
- Author credit: `黒留ハガネ`
- Illustrator name beneath the existing English label `Illustrator`: `かやはら`

Existing English title region, retained as the sole title treatment: `Wandmaker of the Ruined World`

## English Localization

- Existing English title region: `Wand Maker of the Ruined World`
- Main Japanese title region: remove the Japanese title and restore the underlying artwork; do **not** place a second English title there.
- `小冊子付き` → `INCLUDES BOOKLET`
- `特装版` → `SPECIAL EDITION`
- `②` → `2`
- `黒留ハガネ` → `Kurodome Hagane`
- `かやはら` → `Kayahara`
- Existing English label `Illustrator`: retain unchanged.

The finished cover must display `Wand Maker of the Ruined World` exactly once.

## Edit Prompt

Apply `Editing/image-localization-typesetting.md`. Normalize the wording inside the existing decorative English title region to `Wand Maker of the Ruined World` while preserving that region’s established white distressed lettering, orientation intent, scale, placement, and contrast treatment. Remove only the large Japanese title `崩壊世界の魔法杖職人`, reconstructing the artwork directly beneath it; add no replacement title in that Japanese-title region. The canonical English title must appear exactly once.

Replace only `小冊子付き`, `特装版`, `②`, `黒留ハガネ`, and `かやはら` with their paired English text above. Use the shared Noto hierarchy, fit ordinary English horizontally left-to-right rather than stacking or rotating letters, and preserve the source white color, weight, relative prominence, and original text-region boundaries. Retain the existing `Illustrator` label.

Do not crop, repaint, reposition, add, remove, or otherwise alter any character, prop, background object, glow, texture, border, or unlisted text. Do not add a subtitle, tagline, duplicate title, logo, credit, or decorative element.

## Notes / Uncertainties

- The single-title requirement follows the project-wide shared typesetting specification and the user’s explicit cover direction.
- `Kurodome Hagane` follows `novel.config.md`; `Kayahara` follows the established Volume 1 localized-credit convention.
- There are no uncertain Japanese characters in the listed replacement regions.
