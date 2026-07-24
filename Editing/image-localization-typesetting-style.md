# Shared Image-Localization Typesetting — Volumes 2–4

This is the reusable typesetting standard for localized illustrations in *Wand
Maker of the Ruined World*, Volumes 2–4. Individual image specs may override
color, orientation, or emphasis only when the source artwork clearly requires
it. They must not introduce a volume-specific typographic system.

## Font family

- **Display/title text:** Noto Serif Bold.
- **Body copy, dialogue, labels, captions, charts, and contents:** Noto Sans.
- **Emphasis within sans-serif text:** Noto Sans SemiBold or Bold.
- **Condensed fallback for a source region that cannot fit at the regular
  width:** Noto Sans Condensed, with horizontal scaling no lower than 85%.
- Preserve an existing Latin logotype when it is already part of the artwork.
  Do not recreate or restyle brand marks.

## Sizing logic

Sizes are proportional to the image's shorter dimension so the system remains
consistent across portrait and landscape pages:

| Tier | Use | Size |
|-|-|-|
| T1 | Main title / dominant display | 5.5–7.0% |
| T2 | Section title / character name | 3.5–4.8% |
| T3 | Dialogue / callout / large label | 2.4–3.2% |
| T4 | Body copy / profile prose / contents | 1.75–2.25% |
| T5 | Caption / axis / small annotation | 1.25–1.65%, never below 18 px |

Use the largest size that preserves the source text region and hierarchy. Reduce
size within a tier before condensing the face. Do not shrink below T5; enlarge
the text region or reflow instead.

## Weight, color, and effects

- Match the source text's color and relative weight.
- On a flat light field, use dark text with no effect.
- On a flat dark field, use white or source-colored text with no effect.
- On detailed artwork, use a 2–3 px outline at a 1440 px short dimension
  (scale proportionally), chosen for contrast. Add a soft shadow only when the
  source used one or the outline alone is insufficient: 35% opacity, 45° angle,
  0.25 em offset, 0.35 em blur.
- Never add both a heavy outline and a heavy shadow. Preserve source glow,
  texture, stamp, and distressed treatments when they carry layout intent.

## Alignment and spacing

- Preserve the source region, alignment, reading order, and visual hierarchy.
- Prefer horizontal English except where a short vertical title or label is a
  deliberate compositional element; never stack English one letter per line.
- Dialogue and callouts: line height **1.12×**; paragraph gap **0.45 em**.
- Body/profile prose: line height **1.28×**; paragraph gap **0.70 em**.
- Contents, tables, timelines, and lists: line height **1.18×**; item/paragraph
  gap **0.55 em**. Keep page numbers and paired labels aligned to a common
  baseline or tab stop.
- Titles: line height **0.95–1.05×**; no paragraph gap.
- Preserve explicit paragraph breaks. Do not merge separate source paragraphs
  or simulate paragraph breaks with only a slightly larger line gap.
- Keep at least **0.5 em** internal padding around a text block and at least
  **2.5% of the shorter dimension** from trim edges unless the source text
  intentionally bleeds or touches an edge.

## Localization and rendering rules

- Replace only source-language text. Preserve characters, artwork, texture,
  framing, panels, balloons, charts, page numbers, and existing Latin branding.
- Use finalized chapter wording for pre-chapter colour illustrations when the
  pictured text quotes or closely tracks chapter prose/dialogue.
- Use `glossary.md`, `character-reference.md`, `character-voices.md`, and
  `style-guide.md` for all canonical names, terms, and voice.
- Render required English verbatim. Do not add, omit, paraphrase, or hallucinate
  text.
- For dense pages, first reconstruct the cleared text field while preserving its
  paper/texture, then typeset deterministic English above it using this standard.
- Verify at 100% scale and thumbnail scale for spelling, cropping, hierarchy,
  line breaks, paragraph breaks, leading, contrast, and untouched artwork.
