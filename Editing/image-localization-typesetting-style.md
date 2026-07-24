# Shared Image-Localization Typesetting System — Volumes 2–4

This is the reusable typesetting source of truth for localized illustrations in
Volumes 2–4 of *Wand Maker of the Ruined World*. Preserve each source image's
composition, color intent, and hierarchy; these rules normalize the English
typography across volumes without flattening deliberate source-specific design.

## Font Family

- **Display, labels, dialogue, captions, contents, and sans-serif source text:**
  Noto Sans, using Noto Sans Condensed when horizontal space is tight.
- **Long prose, biographies, reports, directives, papers, and serif source
  text:** Noto Serif.
- Use upright Latin text. Do not imitate vertical Japanese with rotated,
  stacked, mirrored, or right-to-left English.
- Use italics only where the source visibly uses an italic/oblique treatment or
  the established English wording requires a discrete emphasis already present
  in the source.

## Hierarchy and Weight

- **Primary title:** Noto Sans Bold, 700.
- **Section heading / character name / major label:** Noto Sans SemiBold or
  Bold, 600–700.
- **Dialogue / illustrated caption:** Noto Sans SemiBold, 600.
- **Body prose:** Noto Serif Regular, 400.
- **Small metadata / credits / page furniture:** Noto Sans Regular, 400.
- Preserve the source's relative hierarchy. A replacement may shrink to fit,
  but a lower-level element must never become visually larger or heavier than
  the element above it.

## Sizing Logic

All values scale from a 1440-pixel-wide page; multiply by
`actual canvas width / 1440`.

- Primary title: 64–86 px.
- Section heading / major label: 44–60 px.
- Illustrated dialogue / caption: 34–48 px, never below 30 px at the reference
  width unless the source box physically cannot accommodate it.
- Body prose: 29–34 px.
- Small metadata / credits: 22–28 px.
- Page number: match the source furniture, normally 22–26 px.
- Prefer reflowing English into one additional line before reducing the font.
  Keep at least 90% of the category's nominal minimum when possible.

## Line and Paragraph Spacing

- Display and illustrated dialogue: line height 1.08–1.16 times the font size.
- Contents, lists, labels, and short captions: line height 1.15–1.25.
- Long-form serif body text: line height 1.30–1.38.
- Preserve every source paragraph break.
- Long-form prose paragraph spacing: 0.65 line (minimum 0.55, maximum 0.85).
- Dialogue/caption paragraph spacing: 0.45 line.
- List spacing: 0.20–0.35 line unless the source uses larger section gaps.
- Do not simulate paragraph breaks with manual leading inside a single
  paragraph; keep line leading and paragraph spacing distinct.

## Alignment and Flow

- Follow the source text region's anchor and alignment: centered titles remain
  centered; left-aligned prose remains left-aligned; labels remain attached to
  their subjects.
- Convert vertical Japanese prose and dialogue to horizontal, left-to-right
  English within the same visual region. Center short display lines only when
  the source treatment is visibly centered.
- Preserve margins, columns, leader rules, page numbers, callout shapes, and
  reading order.
- Do not let English overlap faces, hands, key props, borders, rules, or other
  text. Reflow within the source text region before moving a region.

## Color, Outline, and Shadow

- Match the source text's fill color. Do not introduce a new palette.
- On artwork, use a scaled outline only where the source text has one or where
  contrast requires the established illustrated-caption treatment:
  3 px at 1440-pixel width for normal captions, 4–5 px for major display text.
- Default contrasting outline: white around dark/saturated fill or a
  source-matched dark color around white/light fill.
- Shadow is optional and must follow the source. When present, use a soft
  source-matched dark shadow at 35–55% opacity, offset 2 px right and 2 px down
  at 1440-pixel width, blur radius 2–3 px.
- Never add both a heavy outline and a heavy shadow. Use the minimum treatment
  required for legibility.
- Text-only white or lightly textured pages use no outline and no drop shadow.

## Artwork and Texture Preservation

- Replace only the verified Japanese text regions. Preserve illustration,
  texture, borders, rules, gradients, halftone, paper grain, and page furniture.
- Reconstruct the background under removed Japanese so no glyph fragments,
  halos, smears, or flat mismatched patches remain.
- Preserve exact canvas dimensions and aspect ratio.
- Existing English, numerals, symbols, logos, and legal/publisher text remain
  unchanged unless a per-image localization spec explicitly authorizes their
  replacement.

## Translation Source of Truth

- For color illustrations before Chapter 1, reuse the corresponding filed
  English chapter wording verbatim when the artwork quotes or adapts chapter
  text.
- For every other image, use `glossary.md`, `character-reference.md`,
  `character-voices.md`, `style-guide.md`, and filed English chapters for
  canonical names, terms, and voice.
- Per-image specs must preserve source paragraph boundaries and record the
  applied line-height and paragraph-spacing category from this document.
