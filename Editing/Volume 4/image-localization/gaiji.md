# gaiji-0000 … gaiji-0004 — inline character glyphs (no localization)

## Sources

| File | Canvas | Mode | Glyph |
|-|-|-|-|
| `Source/Volume 4/images/gaiji-0000.png` | 128 × 128 | P (paletted) | `杖` — heavy weight |
| `Source/Volume 4/images/gaiji-0001.png` | 128 × 128 | P | `杖` — light/serif weight |
| `Source/Volume 4/images/gaiji-0002.png` | 128 × 128 | P | `ア` |
| `Source/Volume 4/images/gaiji-0003.png` | 128 × 128 | P | `ミ` |
| `Source/Volume 4/images/gaiji-0004.png` | 128 × 128 | P | `葛` |

**Output: none. These are not localized.**

## What these are

These are *gaiji* — external-character images. A Japanese ebook embeds one when it cannot rely on
the reading device's font to render a character: either the codepoint is outside the guaranteed
set, or the publisher wants a specific glyph variant. Each file holds exactly one character,
sized to sit inline in a line of running text.

The set here is consistent with that: `杖` appears twice at two different weights, which is what a
publisher ships when the same character has to sit in both body copy and heavier display copy;
`葛` is the classic variant-glyph case, having two accepted forms that differ in the lower-right
component; `ア` and `ミ` are katakana carrying furigana or ruby duty.

## Localization decision — no render, originals retained

These are not illustrations. They are typography — single characters that the Japanese text flows
around, standing in for font glyphs the reader may not have.

In the English edition the sentences that contain them are translated into English, so there is no
line of Japanese left for them to sit inside. A gaiji image has no English counterpart because a
character is not a translatable unit: whatever `杖` or `葛` contributed to a Japanese word is
already carried by the English word that replaced that word. Nothing is dropped, because nothing
these files carry survives as a separate element into English.

Rendering them would be actively wrong — it would mean drawing an English letter at glyph size and
leaving it stranded in prose that no longer needs it.

Filed precedent: Volume 3 localized 47 images and shipped no gaiji outputs.

## Notes and uncertainties

- No unresolved or illegible glyphs; each was inspected at 2×–4×.
- The two `杖` files differ in stroke weight, not in character. Both were checked individually
  rather than assumed identical from the filename sequence.
- Pass A and Pass B are recorded as not applicable rather than complete: there is no embedded
  English to edit, because nothing on these files is translated.
- If a later build ever needs one of these characters to survive into the English text — for
  instance inside a retained Japanese term set in kanji — the glyph identifications above are
  what that build should use, and no re-analysis is required.

- **Image-edit renders:** 0 — intentional
- **Saved output:** none; the five source PNGs remain the shipping assets
- **Source integrity:** originals unmodified
