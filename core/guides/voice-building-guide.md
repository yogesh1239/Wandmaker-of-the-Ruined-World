# Voice-Building Guide — Method (Agnostic)

This guide teaches the **method** for deriving a per-character voice profile for
*any* Japanese light novel. It contains no specific characters. Follow it to
fill this novel's `character-voices.md`, which is where the actual profiles
live. Do that during `/setup-novel` (seed from Volume 1) and extend it via the
`updater` as new characters appear.

The goal is a single test the whole translation must pass: **a reader can tell
who is speaking from the dialogue alone, with the tags removed.** Japanese
encodes speaker identity through pronoun, register, and particles far more than
English does; if you translate to a neutral default, that information is lost.
Your job is to rebuild each voice in English so the distinction survives.

## Part 1 — Building One Character's Profile

For each named character, work through these axes and record the findings in
`character-voices.md`.

### 1. First-Person Pronoun

The pronoun is the single most reliable voice signal. Identify it and record
what it signals — then keep that signal *consistent in English* (English has
only "I", so the signalled register must show up in word choice and rhythm
instead).

| Pronoun | Typical signal | English handling |
|-|-|-|
| 俺 (ore) | Masculine, casual, self-assured / rough | Blunt, plain, confident phrasing |
| 僕 (boku) | Soft/boyish masculine, often younger or polite | Gentler, more measured masculine voice |
| 私 (watashi) | Neutral/standard; formal for men | Default; disambiguate by other axes |
| わたくし (watakushi) | Very formal/refined | Elevated, precise diction |
| あたし (atashi) | Casual feminine, often assertive | Forward, colloquial feminine voice |
| わし (washi) | Elderly/archaic masculine | Old-fashioned cadence |
| 拙者 / 某 / etc. | Archaic, samurai/warrior role language | Period-flavored register (sparingly) |
| Name as self-reference | Childish/cute (often young girls) | Keep only if it reads naturally; usually render as "I" + childlike phrasing |

When several characters share 私, the pronoun alone won't separate them — lean
on the other axes below.

### 2. Register / Politeness Level

Classify where the character sits: plain-form (タメ口), polite (です/ます keigo),
or formal/humble. Note whether it's stable or context-dependent. In English this
becomes: contraction frequency, sentence completeness, vocabulary formality, and
hedging. A keigo speaker uses complete sentences and few contractions; a
plain-form speaker contracts freely and clips.

### 3. Address & Honorific Forms

Record how this character addresses every *other* significant character: name
order, honorific used, and any nickname. These are character markers and often
plot-load-bearing (a shift from -san to a given name, or to a diminutive, is a
beat). This table is the cross-reference the translator uses to keep address
forms consistent and to make shifts land. Note the *baseline* form and any
documented *shift points*.

### 4. Sentence-Ending Particles & Verbal Tics

These rarely translate one-to-one, but they tell you the *flavour* to reproduce.
Catalogue the character's habits:

- Feminine-assertive enders (わよ, でしょ, じゃない) → forward, declarative English.
- Polite enders (です, ます, ですが) → complete, measured English.
- Energetic enders (よ！, だよ！, plus frequent ！) → exclamatory, peppy English.
- Dropped/minimal enders → clipped, flat English; let short lines stay short.
- Rhetorical でしょ → render as assertion ("Obviously," "Right?!"), not a real
  question.
- Catchphrases, stutters, verbal fillers (えっと, あの, signature interjections),
  dialect/role-language markers → carry an equivalent English tic, used at the
  same frequency. Don't over-deploy it; match the source's density.

### 5. Vocabulary, Syntax & Topic Domain

- **Vocabulary band:** formal conjunctions (しかし, したがって) vs. casual
  (でも, だから, slang).
- **Subject dropping:** some characters drop subjects constantly (translate as
  clipped fragments); others always state them (translate as full sentences).
- **Sentence length & chaining:** run-on chaining with し/て signals an
  excitable voice; one-clause sentences signal a terse one.
- **Topic domain:** a character who lights up about a specific subject (history,
  food, machines, magic theory) often shifts register there — usually *more*
  verbose. Preserve that contrast; it's characterization.

### 6. Emotional Default & Contrast Behaviour

Note the character's baseline affect **and how it breaks**. The break is often
the most important thing to translate correctly:

- A normally bright character whose register drops sharply in a painful moment —
  keep the quiet line quiet; the contrast does the work. Do not add energy.
- A normally flat character who goes *more* silent when flustered — shorten, do
  not amplify.
- Deadpan humor — let the flat line land flat; never editorialize it into a joke.

### 7. Sample Lines

Record at least one canonical sample per character: the JP line, the ✅ correct
English, and a ❌ wrong (over-/under-shot) version. These calibrate every later
translation and edit faster than prose description does.

## Part 2 — The Narrator

Two narrator outputs are **required** in `character-voices.md` — `/setup-novel`
hard-fails without them (schema: `core/schemas/character-voices-schema.md`):

1. **A narrator register ceiling** — one line stating the highest register the
   narration may reach. Everything downstream caps against it: the translator,
   and the editor's accuracy and polish passes read this
   line. Never elevate the narration past the source's ceiling.
2. **An elevation kill-list of ≥5 rows** — wrong→right pairs of over-elevated
   phrasings and their plain corrections, seeded from the generic list in
   `translation-guide.md` plus novel-specific entries. The editor checks against
   this per-novel list, not the generic one.

**Match the source's flow — the naturalness rule.** The editor's polish pass
lifts the English to read as native-authored prose, but it **may not smooth
choppy JP into flowing English**: sentence length and energy must track the
source. Smooth what the JP smooths; keep abrupt what the JP keeps abrupt. Choppy
narration is a deliberate authorial effect, not a defect to fix — flattening it
elevates the register the ceiling exists to hold. (This is why the polish pass
re-checks every changed span against its JP line before finalizing it.)

Identify the narration mode before translating each chapter:

- **Single fixed first-person narrator:** the narration voice = that character's
  voice profile (Part 1), applied to prose. Match their pronoun-signalled
  register, sentence rhythm, and emotional default in the narration itself, not
  just their dialogue.
- **Rotating / alternating first-person narrator:** chapters (or sections)
  switch narrator. **Identify the active narrator first** — from a header, a
  pronoun, an address form, or topic — and write that chapter's narration in
  that character's voice exactly. A "Per-Narrator" table in `character-voices.md`
  (narrator → narration voice in one line) makes this fast.
- **Third-person narrator:** the narration follows the *author's* locked register
  (see `translation-guide.md`), not any character's voice; only dialogue and
  quoted thought take character voice.

Record the mode and (if rotating) the active-narrator detection signals in
`character-voices.md`.

The narrator block must also preserve the shared tense distinction: narrative
action, description, and indirect/reported thought stay past; clearly direct,
immediate internal monologue uses natural speech tense, often present. Apply
this only after identifying the line as a discrete inner utterance. Do not turn
every rhetorical question, parenthetical aside, or free-indirect comment into
present tense, and do not add quotation marks or italics to unmarked thought.

## Part 3 — Keeping Characters Distinguishable

When a line has no dialogue tag, identify the speaker before translating — in
this priority order:

1. **First-person pronoun** in the line (most reliable).
2. **Address form** used for whoever they're speaking to.
3. **Keigo level** (a polite-form line in a cast of plain speakers fingers the
   one polite character).
4. **Particles / verbal tics** (signature enders, catchphrases, dialect).
5. **Vocabulary & syntax** (subject-dropping, sentence length, topic domain).
6. **Fallback:** count A-B-A-B alternation back from the nearest tagged line, and
   sanity-check against length/affect (terse short line vs. long complete
   sentence vs. exclamatory run-on).

Then translate so that *those same distinctions* are visible in English. The
recurring self-check: **"Does this line sound like THIS character and no one
else?"** If two characters could have said it, the voice work isn't done.

## Part 4 — Maintaining `character-voices.md`

- Seed it at `/setup-novel` from Volume 1: one profile per named speaker plus the
  narrator section and a quick distinguishing-markers table (character → 3 fastest
  tells).
- The `updater` adds new characters as they appear and refines profiles when a
  documented shift (address-form change, arc turn) occurs — it **flags** changes,
  never silently overwrites established voice.
- Keep it consistent with `glossary.md` (name spellings, romanization) and
  `character-reference.md` (genders, roles, relationships).
