# Token-Cost Optimization — Zero-Loss Set (in place) + Budget Siblings

Date: 2026-07-07. Applies identically to all three templates:

- `CN Translation Initialisation` (packs: `.claude/`, `.codex/` + `.agents/skills/`)
- `CN-JP Translation Initialisation` (same packs; **not yet a git repo** — init first)
- `JP Translation Initialisation` (same packs **plus** `.opencode/` agents + commands)

## Problem

Per-chapter cost on the Claude Max plan is dominated by four sinks:

1. **Reasoning-effort inheritance.** No `.claude/agents/*.md` sets `effort:`, so every
   subagent inherits the session default (currently xhigh) — including mechanical
   agents whose Codex twins already declare `model_reasoning_effort = "medium"`.
2. **Lead context bloat.** The lead embeds the full chapter source into every
   translate/edit/QA dispatch (lead output tokens), full-`Read`s stage outputs to
   "verify on disk", and in chapter-range mode accumulates all of it until repeated
   compaction.
3. **Edit-log verbosity.** Free-prose `reason` per change is an output-token tax on
   every edited line; QA only needs the before→after and a classification.
4. **Premium model on the raw draft.** The translator's draft is deliberately
   "faithful, slightly stiff" raw material — the opus editor and the QA gate are the
   quality backstop.

Sinks 1–3 are pure waste (Version 1, zero quality loss, applied in place).
Sink 4 plus two bounded relaxations form Version 2 (marginal risk, separate
`(Budget)` sibling folders).

## Version 1 — zero-loss set (edit the template in place)

### V1.1 Effort tiering (mirror the Codex map exactly)

Premium roles **high**, mechanical roles **medium**:

| Agent | Tier |
|-|-|
| translator, editor, qa-auditor | `high` |
| assembler, updater, image-localizer, epub-builder | `medium` |

- `.claude/agents/*.md`: add `effort: high` / `effort: medium` to frontmatter (all 7 agents).
- `.codex/agents/*.toml`: already carry `model_reasoning_effort` per this map — verify all 7, fix any that deviate.
- JP only, `.opencode/agents/*.md`: add the opencode per-agent reasoning-effort frontmatter key with the same map. Verify the exact key name/values against current opencode docs before writing (believed `reasoningEffort`); if opencode cannot express it per-agent, record that in the commit message and skip rather than inventing syntax.

### V1.2 Lead context hygiene

Files: `core/pipeline.md`; `.claude/skills/translate-chapter/SKILL.md`; `.agents/skills/translate-chapter/SKILL.md`; JP only `.opencode/command/translate-chapter.md`.

1. **Structural verification only.** Replace the "verify every stage's output on disk" rule's implied full read with: the lead verifies **structurally via Bash** — `wc -l` against the expected scope, `head`/`tail` for the required leading/trailing sections, `grep` for required markers (scene breaks, `## Translator Notes`, edit-log part headings). The lead **never `Read`s a draft or chapter in full**; content verification is exclusively QA-Audit's job (Stage 4). Keep the existing sentence "QA verifies *content*, not just that a file exists" — it becomes the contrast that explains the rule.
2. **Source is sent once.** The dispatch embeds the source scope once (V1 keeps source-at-top embedding); follow-up `SendMessage`s to a teammate never re-echo chapter text — they reference file paths and line ranges only.
3. **Range batching.** In "Chapter-range mode" (pipeline.md and the skills): ranges longer than **5 chapters** are run in batches of ≤5, each batch in a fresh session — cross-chapter continuity is file-borne, so a fresh lead loses nothing; an ever-growing lead context is repeatedly compacted at real token cost and degrades orchestration.

Wording lands in pipeline.md as the canonical fact; the skills/commands cite it and carry only the operational phrasing (existing citation discipline: packs never restate pipeline facts).

### V1.3 Edit-log compaction

Files: `core/schemas/edit-log-schema.md`; editor briefs (`.claude/agents/editor.md`, `.codex/agents/editor.toml`, JP `.opencode/agents/editor.md`); pipeline.md Stage 2 where it says changes are logged "before→after + reason".

- The log entry keeps **before → after** verbatim (QA sampling depends on it).
- `reason` becomes a **tag from a fixed taxonomy** + optional note of **≤ 8 words** (only when the tag alone would be misleading):
  `accuracy | referent | glossary | register | tense | address | voice | sfx | punct | polish`
- Polish-pass entries keep their `[polish]` marker (that is the `polish` tag).
- Update the schema's example entries to the compact form.

### V1 housekeeping

- **Commit the pre-existing uncommitted work first** (CN and JP have dirty
  worktrees; CN-JP contains the same text but has no git). One commit, message:
  `packs: grep-only reference policy + curated dispatches (inherited uncommitted work)`.
  CN-JP: `git init` + commit everything as baseline `import: CN-JP template (copied from CN harness)` first.
- Then apply V1 as one commit: `cost: zero-loss set — effort tiering, lead hygiene, edit-log compaction`.
- Tag the result `cost-opt-v1`.
- Place this spec at `docs/superpowers/specs/2026-07-07-token-cost-optimization-design.md` (commit with V1).

## Version 2 — Budget sibling (new folder `<name> (Budget)`)

Create by `cp -r` of the V1-complete template (includes `.git`, so lineage is
preserved), then apply:

### V2.1 Translator model one tier down

- `.claude/agents/translator.md`: `model: opus` → `model: sonnet`.
- `.codex/agents/translator.toml`: set `model` to the current cheap Codex tier **only if verifiable** from docs; otherwise leave unset and record in `docs/budget-diff.md` as a manual knob.
- JP `.opencode/agents/translator.md`: same rule (verify opencode model-string format first).
- Editor, qa-auditor stay premium — they are the backstop.

### V2.2 Teammates self-read source

The lead stops embedding source text in dispatches. Everywhere a file says the
dispatch "places the raw CN/JP source at the TOP of the prompt" (pipeline.md,
translate-chapter skill in every pack, translator/editor/qa-auditor briefs in
every pack), replace with: **dispatch line 1 is**
`Read <source file> lines <a>–<b> in full before reading the rest of this prompt.`
— the source still lands at the front of the teammate's context; the lead pays
for it zero times instead of once per dispatch. The rationale sentence about
long-input accuracy stays, rephrased to cover the self-read form.

### V2.3 QA streak relaxation (knob, default off)

- `core/schemas/novel-config-schema.md`: new knob `qa_streak_relax` (integer K, default `0` = off).
- `core/guides/qa-audit-guide.md` (sampling section): when the knob is K > 0 and the **last K chapters** in `translation-progress.md` each passed QA on the **first round with zero critical findings**, the random sampling floor is **halved**. All other over-sampling rules (dialogue, high-emotion, edit-log-untouched weighting) unchanged. Any FAIL or any critical finding resets the streak. QA still runs on every chapter.
- qa-auditor briefs (all packs): read the knob from `novel.config.md`; derive the streak from `translation-progress.md`.

### V2 housekeeping

- `CLAUDE.md` and `AGENTS.md`: retitle as the Budget variant, one-line note + pointer to `docs/budget-diff.md`.
- Write `docs/budget-diff.md`: exact list of deviations from the parent template (V2.1–V2.3 with file paths), so the lineages never drift silently.
- One commit: `cost: budget set — sonnet drafts, self-read dispatches, QA streak knob`; tag `budget-v1`.

## Invariants (every edit, both versions)

- Model-agnostic facts live in `core/`; runtime packs carry only their own syntax and cite `core/pipeline.md` — never restate its facts.
- `core/scripts/` untouched — gates unchanged.
- V1 changes nothing about the quality machinery: two editor sub-passes, the interleave, the QA gate, fresh-spawn lifetimes all stay exactly as specified.
- CN pinyin policy, JP conventions, file contracts: untouched.

## Verification checklist (run per repo before reporting done)

```bash
# every .claude agent has an effort line matching the tier map
grep -H "^effort:" .claude/agents/*.md
# codex map intact
grep -H "model_reasoning_effort" .codex/agents/*.toml
# no full-read verification left in lead docs
grep -rn "Read.*in full\|read the draft" core/pipeline.md .claude/skills/translate-chapter/ | grep -iv "never\|not\|structural"
# edit-log taxonomy present
grep -n "accuracy | referent" core/schemas/edit-log-schema.md
# V2 only: model downgrade + self-read dispatch + knob
grep -n "model:" ".claude/agents/translator.md"; grep -rn "qa_streak_relax" core/
git log --oneline -4 && git tag
```
