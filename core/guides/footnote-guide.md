# Footnote Guide — Japanese Light Novels (Agnostic)

Footnotes are **default-on** for Japanese light novels: they let the prose stay
clean and readable while preserving the cultural texture a Western reader would
otherwise miss. This guide is series-agnostic — the reference table below covers
JP-general culture, not any one novel.

## When to Add a Footnote

Add `[^N]` the FIRST time any of the following appears **in a chapter**:

- A Japanese term retained untranslated (beyond standard honorifics).
- A pun or wordplay that cannot survive translation unchanged.
- A Japanese cultural practice, food, festival, or custom unfamiliar to a
  Western reader.
- A historical, mythological, or religious reference (figures, eras, battles,
  deities, folklore).
- A name or term whose meaning is plot-relevant or is being played on
  (including a furigana gloss that pairs an unexpected reading with a kanji).
- An intertextual reference to another work (novel, film, game, song).
- A number, date, or measurement with cultural significance (unlucky numbers,
  calendar days, traditional units).
- Any place where a translation choice sacrifices nuance for readability and the
  reader would benefit from knowing what was lost.

## What NOT to Footnote

- Standard honorifics (-kun, -san, -chan, -sama, -sensei, etc.) — covered by the
  translation guide's blanket retention rule.
- Common Japanese loanwords already familiar to the target audience (e.g.
  *samurai*, *ramen*, *kimono*, *sensei* as a standalone word).
- Anything already explained by context in the same paragraph.
- Things you can simply translate. A footnote is for what *can't* be carried in
  the prose, not a place to show research.

Keep footnotes short. One to three sentences. The reader wants to get back to
the story.

## Numbering

- Footnote numbering **resets to `[^1]` each chapter**.
- When a chapter is split into multiple part/section files during translation,
  continue numbering **sequentially across the parts** so the assembled chapter
  has one clean `[^1]…[^N]` run with no resets mid-chapter.

## Format

Inline marker immediately after the relevant word or phrase (no space before it):

```
"They ate osechi[^1] while watching the sunrise."
```

Collect every footnote in a single `## Translator Notes` section at the very end
of the assembled chapter file:

```markdown
## Translator Notes

[^1]: **Osechi** (おせち): Traditional Japanese New Year's cuisine, served in
      tiered lacquered boxes. Each dish carries symbolic meaning — black beans
      for health, herring roe for fertility.

[^2]: **Pun — 「A」/「B」**: The Japanese 「A」 sounds like 「B」, meaning X.
      The English substitutes a comparable near-homophone.
```

The EPUB build turns these into EPUB3 popup footnotes; the `## Translator Notes`
section is what it reads. Always include the section when any footnote exists,
and never leave a `[^N]` marker without a matching note (or vice versa).

## Puns and Wordplay

When a Japanese pun cannot be replicated:

1. Translate for **meaning** — never leave the line broken or nonsensical.
2. Add a footnote explaining the original wordplay.

```
[^N]: **Pun (original):** The Japanese 「[word A]」 sounds like 「[word B]」,
      meaning [X]. The English loses this double meaning.
```

If you can reproduce the effect with an English wordplay, do so and footnote the
substitution so the reader knows the original mechanism.

## Cultural Terms — Generic JP Reference

These appear across many Japanese works; footnote on first use when they're not
already context-explained. This is a starting set, not exhaustive — add novel-
specific terms to the per-novel `glossary.md`, not here.

| Term | Reading | Footnote content (one line) |
|-|-|-|
| おせち | osechi | New Year's cuisine in tiered lacquered boxes, each dish symbolic |
| 初詣 | hatsumoude | First shrine/temple visit of the New Year |
| 初夢 | hatsuyume | First dream of the New Year (Jan 1→2 night), said to foretell luck |
| お年玉 | otoshidama | New Year's money gift given to children |
| 振袖 | furisode | Long-sleeved formal kimono for unmarried women |
| 浴衣 | yukata | Light cotton kimono worn in summer / at festivals |
| 袴 | hakama | Formal pleated trouser-skirt worn over kimono |
| 下駄 | geta | Traditional elevated wooden sandals |
| 甘酒 | amazake | Sweet warm fermented-rice drink served at shrine stalls |
| 餅 | mochi | Glutinous rice cake; sweet (kinako, red bean) or savory (grilled) |
| 弁当 | bentou | Boxed single-portion meal |
| お盆 | obon | Summer festival honoring ancestral spirits |
| 花見 | hanami | Cherry-blossom viewing |
| 七五三 | shichi-go-san | Coming-of-age festival for children aged 7, 5, and 3 |
| 絵馬 | ema | Wooden plaque for written prayers/wishes at a shrine |
| お守り | omamori | Protective amulet sold at shrines/temples |
| こたつ | kotatsu | Low table with a heater and quilt underneath |
| 銭湯 / 温泉 | sentou / onsen | Public bathhouse / natural hot spring |
| 文化祭 | bunkasai | School cultural festival |
| 部活 | bukatsu | After-school club activity |

## Domain References (Adapt per Novel)

Different novels lean on different reference domains. Footnote within the domain
the novel actually uses; record recurring per-novel terms in `glossary.md`.

- **Historical / military fantasy:** real or invented historical figures,
  battles, eras, ranks, and tactics. Give who/what it is, why it matters, and
  (if relevant) how it ties to the scene or character. Invented in-world
  history goes in the glossary, not a footnote, unless the text plays on it.
- **Mythology / folklore:** name the figure or creature, its tradition, and the
  one trait the scene relies on.
- **Food-centric scenes:** footnote a dish only when it is central to the scene,
  its preparation/context drives the moment, or a Western equivalent would
  mislead. Keep it to one sentence.
- **Name meanings:** footnote only when the text itself draws attention to the
  meaning (a character comments on it, or it's used as a pun). Record fixed name
  meanings in `character-reference.md`.
