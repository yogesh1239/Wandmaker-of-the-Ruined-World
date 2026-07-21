# Schema: `edit-log.md`

The one per-chapter edit log the editor appends to, at `Editing/Volume N/Chapter <N> - Edit Log.md`. Appended (never overwritten); for a parted chapter each part appends its own `## Part <i>` section under the same file. The polish pass tags its entries with `[polish]` so they are distinguishable from line-edit entries.

## Reason tag

Each change entry classifies its edit with a **single tag from this fixed taxonomy**, not free prose — QA samples on the before→after pair, so the tag alone carries the "why":

`accuracy | referent | glossary | register | tense | address | voice | sfx | punct | polish`

Append a **≤ 8-word note** after the tag only when the tag alone would mislead. Polish-pass entries take the `polish` tag (and keep the `[polish]` marker below).

## Format

```markdown
# Chapter <N> — Edit Log

## Part <i>   (omit this line for unparted chapters)

### Accuracy Fixes
- **[source line/context]**: "old" → "new" — [tag] (optional ≤8-word note)

### Register and Flow
**[Character]:** [notes on voice consistency or changes]

### Formatting Confirmed
- [sections, images, tense, glossary, footnotes verified]
```

- Polish-pass entries carry a **`[polish]`** marker so a reader can tell a polish edit from an accuracy/line edit:
  `- [polish] **[line/context]**: "old" → "new" — polish (optional ≤8-word note)`

## Filled example

```markdown
# Chapter 3 — Edit Log

## Part 1

### Accuracy Fixes
- **line 112 (天雷斬)**: "Sky Lightning Cut" → "Heavenly Thunder Slash" — glossary
- **line 118**: "she" → "Haibara" — referent
- [polish] **line 140**: "isn't it" → "you know?" — polish (restore Haibara's tic)

### Register and Flow
**Haibara:** kept polite-casual; no elevation.

### Formatting Confirmed
- Scene breaks (◇), inline images, past-tense narration, glossary terms verified.
```
