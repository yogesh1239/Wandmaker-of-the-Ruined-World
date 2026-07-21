# Translation Guide — Japanese Light Novels (Agnostic)

This guide holds the reusable conventions for translating any Japanese light
novel in this harness. It contains **no series-specific facts** — per-novel
data (the author's exact register, character voices, glossary) lives in
`novel.config.md`, `character-voices.md`, `glossary.md`, and
`character-reference.md`. Read those alongside this guide.

## Core Principle — Author Voice Fidelity

Translate the author you have, not the author you wish you had. Your job is to
carry the **source register** into English, not to "improve" it.

- Most JP light novels are written in a direct, punchy register — short to
  medium sentences, dialogue-heavy, minimal descriptive flourish. A few are
  genuinely literary. Match whichever the source actually is.
- The author describes what matters and nothing more. Do not add detail,
  metaphor, or emotional colour the source does not contain.
- Dialogue carries the story voice; narration usually stays lean. Let
  characters do the heavy lifting.
- Emotional beats land through restraint. Resist the urge to underline them.

The register is **classified once and locked** at `/setup-novel` and recorded
in `novel.config.md`. Translate to that lock, not to a generic "LN voice."

**Naturalness is the polish pass's job, not the translator's.** At the translate
stage, optimize for two things: **accuracy** (the English says what the JP says)
and **register fidelity** (it sits at the source's level, no higher). Do not
chase "natural-sounding" prose here — the editor's polish pass lifts the English
to read as native-authored (`quality-checklist.md`, `core/pipeline.md` Stage 2).
This split is deliberate: research on literary MT found that telling the
translation step to "translate naturally" doesn't reduce translationese —
reframing it as a separate polish task does. So translate faithfully; trust the
polish pass to do the smoothing.

## Narrative Tense

ALL narration is past tense. Dialogue stays in natural speech tense.

- Wrong: "She walks in and sees him sitting there."
- Right: "She walked in and saw him sitting there."

Internal thoughts follow past tense in narration: "She thought…" not
"She thinks…" Present-tense narration is acceptable only if the source itself
is deliberately written in a historical-present style and the register lock
records that exception.

## Register Framework

Classify the source at `/setup-novel` into one of the registers below (a novel
may sit primarily in one and borrow another for specific scenes — e.g. a
military fantasy with romance interludes). Read the **source signals**, then
hit the **English target**. Record the lock in `novel.config.md`.

| Register | Source signals (JP) | English target |
|-|-|-|
| Casual / Comedy | Short clipped sentences, heavy dialogue, slang, interjections (えっ, うわ, げっ), exclamation-heavy, light fourth-wall asides, gag onomatopoeia | Contemporary, snappy YA prose. Contractions throughout. Punchlines land flat and fast. Never over-explain a joke. |
| Literary / Fantasy | Longer flowing sentences, archaic or elevated vocabulary, coined fantasy terms, descriptive worldbuilding passages, measured narration | Slightly fuller, smoother prose. Allow subordinate clauses. Keep coined terms consistent (glossary). Still no purple padding — elevated, not bloated. |
| Action / Military | Terse declaratives, clipped command dialogue, ranks and unit names, weapon/tactics vocabulary, present-tense urgency markers in JP | Tight, muscular English. Short sentences in combat. Keep ranks/units exact and consistent. Verbs do the work; cut adverbs. |
| Romance | Softer rhythm, internal-monologue density, hesitation markers (…, あの, えっと), feeling-verbs, blush/heartbeat onomatopoeia | Warm but unforced. Let pauses breathe (em dashes, ellipses). Render feeling through plain words, not melodrama. |

**Register discipline:** when a scene shifts register (a comedy novel turning
briefly serious, a war novel pausing for a quiet character beat), the prose
shifts with it. The contrast is the effect — do not flatten everything to one
tone.

## Honorifics

Always retained. Never dropped, adapted, or replaced with English naming
conventions (no "Mr.", "Miss", "Sir" for honorifics).

| Honorific / form | Rule |
|-|-|
| -kun | Always keep |
| -san | Always keep |
| -chan | Always keep |
| -sama | Always keep |
| -senpai / -kouhai | Always keep |
| -sensei | Always keep (teacher, doctor, master, mentor) |
| onee-san / onee-chan | Keep (incl. self-reference) |
| onii-san / onii-chan | Keep |
| -dono, -tan, -chi, etc. | Keep; footnote on first use if unusual |

Honorifics often carry plot weight: a character switching from family name to
given name, from -san to -kun, or dropping the honorific entirely is usually a
deliberate beat. Preserve the form **and** make the shift land — adjust the
surrounding phrasing so an English reader feels the change. Record per-character
address forms in `character-voices.md`, not here.

## Name Order

Japanese order always: **family name first, given name second**
(e.g. *Yamada Tarou*, not *Tarou Yamada*).

- Exception: a surname shouted or used alone as address stays bare
  (山田！ → "Yamada!").
- Western-coded characters in a fantasy/foreign setting keep the order the
  source gives them. Record any exceptions in the glossary.

## Furigana

The source splitter renders ruby as `漢字[かな]` (square brackets, deliberately
chosen so they don't collide with the `（）`/`《》` thought markers). Treat the
bracketed reading as information about pronunciation/intended reading:

- Use it to disambiguate names, coined terms, and unusual readings.
- When the author furigana-glosses a kanji compound with an unexpected reading
  (a common LN device — e.g. writing one word but reading it as another), that
  gap is usually **meaningful**: footnote it.
- Do not carry the `[かな]` brackets into the English output.

## Sound Effects / Onomatopoeia

Naturalize — do not transliterate raw kana into the prose. Render the *effect*
in idiomatic English.

| JP type | Approach | Example renderings |
|-|-|-|
| Heartbeat (ドキドキ) | Describe the feeling | "her heart pounded", "thump-thump" |
| Sigh (ため息) | Use the verb | "sighed" — never "tame-iki" |
| Scoff (ふん) | Idiomatic interjection | "Hmph." |
| Surprise (えっ) | Idiomatic interjection | "Huh?", "What?" |
| Exasperation (もう) | Context phrase | "Honestly…", "Come on…", "Ugh…" |
| Impact/action SFX (ドン, ガシャン) | Describe or use an English SFX word | "a heavy thud", "crash" |

Recurring filler expressions vary by context — don't lock one English phrase:

| JP | Options | Note |
|-|-|-|
| やはり / やっぱり | "Sure enough" / "Just as I thought" / "As expected" | Rotate; don't repeat |
| しょうがない | "Can't help it" / "Nothing to be done" / "That's just how it is" | Match speaker register |
| まあ | "Well…" / "I mean…" / "Honestly…" | Context-driven |
| ね / よね | "right?" / "isn't it?" — or drop | Often removable in English |

## Internal Thoughts

The source marks unspoken thought and telepathic/"heard" inner voice with
bracket pairs. Render both as *italics* (no quotation marks):

- `（…）` parenthetical thought → *italics*
- `《…》` mind-voice / emphasized inner line → *italics*

Do not wrap italicized thoughts in quotation marks, and do not add a "she
thought" tag unless the source has one.

## Scene Breaks

Source scene-break ornaments (✿ / ☆ / ■ / ◇ / ◆ / × × × / centred blank-line
dividers, etc.) all normalize to a single Markdown rule:

```
---
```

Use exactly `---` on its own line. The EPUB build maps `---` back to a centred
ornament; keeping the marker uniform in the prose is what lets it do that.

## Inline Images

Preserve image markers exactly as the splitter emits them:

```
![pXXX.jpg](images/pXXX.jpg)
```

Do not move, rename, or describe them, and never emit an "Illustration Mapping"
header into the output file.

## Elevation Kill List

These purple-prose reflexes creep in when a translator or editor "polishes."
For each, write the plain form in the right column, not the elevated one on the
left. **This applies to every sentence of every part of every chapter** — not
just the passages that look ornate. This generic list seeds each novel's own
kill-list in `character-voices.md` (which adds series-specific entries); the
per-novel list is the one the editor checks against.

| Elevated (wrong) | Plain (right) |
|-|-|
| "A deep crimson flush spread across her cheeks." | "Her face turned red." |
| "His gaze drifted to the middle distance." | "He looked away." |
| "Fury ignited behind her eyes." | "She was furious." |
| "A pang of melancholy sprouted in his chest." | "He felt a little sad." |
| "She let out a breath she didn't know she'd been holding." | "She exhaled." |
| "Time seemed to stand still." | (usually cut entirely) |
| "An almost imperceptible nod." | "She nodded." |
| "He couldn't help but…" | "He…" |
| "A myriad of emotions washed over her." | (name the one emotion the source names) |
| Stacked adjectives / triple-clause sentences for a plain JP line | One clean sentence |

General rule: if the English sentence is markedly longer or fancier than the JP
line it renders, you have probably elevated it. Bring it back down to match the
source's plain statement.

## Output File Rules

- **No title heading inside the file.** Prose starts directly. The chapter
  title comes from the chapter-title map in `novel.config.md` (used for the
  filename and, at build time, the `<h1>`/TOC), not from an in-file heading.
- **Exception:** if a translated title contains a Windows-illegal filename
  character (`< > : " / \ | ? *`), the filename uses a sanitized version and the
  full true title is written once as an in-file `#` heading so nothing is lost.
- Footnotes use `[^N]` inline + a `## Translator Notes` section at the end —
  see `footnote-guide.md`.
- Romanization uses the **no-macron** convention (vowel-doubling: *Tarou*,
  *Yuusuke*, *senpai*), enforced by `normalize_romaji.py`. Never emit macrons
  (ō, ū) in prose.
