# Schema: `character-voices.md`

Per-character voice profiles + the narrator guide, built with `core/guides/voice-building-guide.md`. Seeded at `/setup-novel`, refined by the updater. `/setup-novel` hard-fails unless the Narrator ceiling line and a ≥5-row kill-list are present (spec §5.5).

## Required sections

### `## Narrator`
- **`**Register ceiling:**`** — one line stating the highest register the narration may reach (never elevated past the source's ceiling). Required verbatim marker.
- **Mode** — fixed first-person / rotating first-person / third-person (+ active-narrator identification if rotating).
- **`### Elevation kill-list`** — table with **≥5 rows** of over-elevated phrasings and their corrected forms:

```
| Elevated (wrong) | Correct |
```

### `## <Character Name>` (one block per character)
Each block must give: first-person **pronoun** (+ what it signals), **register**, **address/honorific forms**, verbal **tics**/particles, and **2+ sample lines** showing the voice.

## Filled example

## Narrator
- **Register ceiling:** plain conversational narration; narrative/indirect thought past, direct immediate thought in natural speech tense; no literary/archaic diction.
- **Mode:** fixed first-person (protagonist).

### Elevation kill-list
| Elevated (wrong) | Correct |
|-|-|
| "I could not help but ponder" | "I couldn't help wondering" |
| "a countenance of displeasure" | "an annoyed look" |
| "made haste toward" | "hurried to" |
| "it was with trepidation that I" | "nervously, I" |
| "an abundance of" | "a lot of" |

## Haibara
- **Pronoun:** 私 (watashi) — neutral, composed.
- **Register:** polite-casual; softens with -kun for close friends.
- **Address:** "Senpai," teachers as -sensei.
- **Tics:** trails off with "...you know?" when unsure.
- **Samples:**
  - "Senpai, you skipped lunch again, didn't you?"
  - "I'm not angry. I'm just... a little disappointed, you know?"
