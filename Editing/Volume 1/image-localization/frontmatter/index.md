# Volume 1 Front-Matter Localization Prompts

These are the final, editorially revised image-generation specs for the eight requested assets before Chapter 1. Pass the original image together with its spec's `## Image-Generation Edit Prompt` section to the image-generation model. Do not use the English text by itself as a prompt.

All localized prose is upright, horizontal, and left-to-right. The prompts preserve each source canvas and artwork, prohibit invented text and art, and use glossary-locked names and terms. ImageMagick 2x crops were used to verify the small vertical text on the three 1920x1381 color spreads.

| # | Source image | Classification | Prompt spec | Action |
|-:|---|---|---|---|
| 1 | `cover.jpeg` | Text-bearing front cover | `cover.md` | Localize per explicit user request |
| 2 | `image_rsrc4ZW.jpg` | Text-bearing color title/frontispiece | `image_rsrc4ZW.md` | Localize |
| 3 | `image_rsrc4ZX.jpg` | Text-bearing color Blue Witch spread | `image_rsrc4ZX.md` | Localize |
| 4 | `image_rsrc4ZY.jpg` | Text-bearing color Ohinata Kei / Ori Kenshi spread | `image_rsrc4ZY.md` | Localize |
| 5 | `image_rsrc4ZZ.jpg` | Text-bearing color Dragon Witch spread | `image_rsrc4ZZ.md` | Localize |
| 6 | `image_rsrc500.jpg` | Clean decorative page; English-only | — | Use original unchanged |
| 7 | `image_rsrc501.jpg` | Text-bearing monochrome special-edition title page | `image_rsrc501.md` | Localize |
| 8 | `image_rsrc502.jpg` | Text-bearing monochrome contents page | `image_rsrc502.md` | Localize |

## Editorial Notes

- Seven of the eight targets are text-bearing and have specs. `image_rsrc500.jpg` contains only the already-English decorative title `Wandmaker of the Ruined World` and no Japanese text; it is classified as English-only/clean and deliberately receives no edit prompt. Because it is not being edited, its decorative closed-up `Wandmaker` form remains source art rather than localized terminology.
- The exact filed English lines were used for all color-spread dialogue and narration; chapter-title-map forms were used for the contents page.
- The cover spec implements the user's explicit localization request. This conflicts with the default `novel.config.md` policy to retain the Japanese cover unchanged, so the build coordinator must treat the user's request as the scoped override if the localized cover is rendered.
- Contents page numbers are preserved from the source print layout; they do not represent stable reflowable-EPUB pagination.
- The only unresolved reference-level uncertainty is the illustrator's English spelling: `Kayahara` is the direct no-macron romanization of visible `かやはら`, but the project contains no independently locked English illustrator entry.
