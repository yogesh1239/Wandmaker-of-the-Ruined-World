# OpenCode Runtime Harness (DeepSeek v4 Pro) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add an OpenCode-native runtime layer (7 subagent definitions + 3 commands + wiring doc) so the JP translation pipeline runs under OpenCode with DeepSeek v4 Pro as the session model.

**Architecture:** Third runtime beside `.claude/` and `.codex/`: markdown agents in `.opencode/agents/`, commands in `.opencode/command/`, wiring in `.opencode/RUNTIME.md` injected via `opencode.json` `instructions`. Content parity with the Codex TOML briefs, restructured to DeepSeek v4 Pro prompting guidance. `AGENTS.md` is never touched.

**Tech Stack:** OpenCode 1.17.13 markdown agent/command format (YAML frontmatter + body-as-system-prompt); plain files, no code.

**Spec:** `docs/superpowers/specs/2026-07-04-opencode-runtime-design.md`

## Global Constraints

- **Codex untouched:** never edit `AGENTS.md`, `.codex/**`, `.agents/**`, `.claude/**`, `core/**`, or any per-novel file. Only create `opencode.json`, `.opencode/**`, and make the single CLAUDE.md table-row edit in Task 1.
- **No model pinning:** no `model:` and no `temperature:` key anywhere under `.opencode/**` or in `opencode.json`.
- **Agent frontmatter is exactly:** `description` + `mode: subagent` (plus `permission:\n  edit: deny` for qa-auditor only). No `tools:` lists.
- **DeepSeek v4 Pro prompt structure (every agent body):** one role sentence (no persona flourish), then exactly these tagged sections in order: `<context>`, `<objective>`, `<grounding_rules>`, `<workflow>`, `<output_format>`. `<workflow>` is a numbered step list. Constraints are written as wrong→right pairs where applicable (e.g. 気づいた → "noticed", not "registered"), never bare negations alone.
- **Single source of truth:** cite `core/pipeline.md` for stages/paths/gates — never restate its tables. Zero series-specific facts (no novel names, character names, or hardcoded titles).
- **Language:** instructions in English; Japanese text appears only as data/examples.
- **Content parity sources:** each agent's content comes from its sibling `.codex/agents/<name>.toml` (primary) and `.claude/agents/<name>.md` (secondary). The implementer must read both before writing.
- Commit at the end of every task with the message given in the task.

---

### Task 1: Wiring — opencode.json, RUNTIME.md, CLAUDE.md row

**Files:**
- Create: `opencode.json`
- Create: `.opencode/RUNTIME.md`
- Modify: `CLAUDE.md` (the "Where things live" table, Runtimes row only)

**Interfaces:**
- Produces: the runtime doc that all agents/commands in Tasks 2–6 assume is loaded; the directory convention `.opencode/agents/` and `.opencode/command/` used by every later task.

- [ ] **Step 1: Create `opencode.json`** at repo root with exactly:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "instructions": [".opencode/RUNTIME.md"]
}
```

- [ ] **Step 2: Create `.opencode/RUNTIME.md`** with exactly:

```markdown
# OpenCode runtime wiring — JP Light-Novel Translation Harness

You are running under **OpenCode** (session model: whatever the operator configured — typically DeepSeek v4 Pro). OpenCode also auto-loads `AGENTS.md`; read it for the **shared, runtime-neutral** material: the non-negotiables, the `core/` pointers, and the gate commands. Its *dispatch wiring*, however, is for the Codex runtime and does **not** apply to you: ignore every reference to `.codex/agents/` and `.agents/skills/`. Your wiring is below.

## Dispatch

- Per-stage subagents live in `.opencode/agents/` — `translator`, `editor`, `assembler`, `qa-auditor`, `updater`, `image-localizer`, `epub-builder`. Invoke them **by name** with the task tool. Each inherits the session model; none pins its own.
- Pipeline commands live in `.opencode/command/` — `/setup-novel`, `/translate-chapter <N>`, `/build-epub <N>`.
- `core/pipeline.md` owns stages, ordering, file contracts, and done-criteria. Commands and agents cite it; when anything disagrees with it, `core/pipeline.md` wins.

## Runtime rules

1. The **qa-auditor always runs as its own fresh subagent** per audit — independent context is the point; the context that edited a chapter cannot audit it. It never edits chapter files (its `edit` permission is denied); it writes only its QA report.
2. The per-part interleave is a **gated handoff**: never translate a chapter's parts in parallel, and do not start part i+1 until part i's edit is verified on disk.
3. Dispatch at most **6 subagents concurrently**.
4. **Front-load every dispatch** with the complete spec, and place the raw JP source for the scope at the **top** of the prompt, instructions after — long source first preserves accuracy on long inputs.
5. Verify each stage's output **on disk** before treating the stage as done.
```

- [ ] **Step 3: Edit the CLAUDE.md runtimes row.** In the "Where things live" table, replace:

```
| Runtimes (agnostic) | `.claude/` (agents + skills for Claude Code); `AGENTS.md` + `.codex/agents/` + `.agents/skills/` (for Codex CLI) | No |
```

with:

```
| Runtimes (agnostic) | `.claude/` (agents + skills for Claude Code); `AGENTS.md` + `.codex/agents/` + `.agents/skills/` (for Codex CLI); `opencode.json` + `.opencode/` (agents + commands + RUNTIME.md for OpenCode / DeepSeek v4 Pro) | No |
```

- [ ] **Step 4: Verify**

Run: `python3 -c "import json; json.load(open('opencode.json'))" && grep -c "opencode" CLAUDE.md && grep -n "codex" .opencode/RUNTIME.md`
Expected: JSON parses; CLAUDE.md match count ≥ 1; RUNTIME.md `.codex` mentions are only in the scoping-out sentence.

- [ ] **Step 5: Commit**

```bash
git add opencode.json .opencode/RUNTIME.md CLAUDE.md
git commit -m "opencode: runtime wiring (opencode.json + RUNTIME.md) and CLAUDE.md layer row"
```

---

### Task 2: Agents — translator, editor

**Files:**
- Create: `.opencode/agents/translator.md`
- Create: `.opencode/agents/editor.md`
- Read first: `.codex/agents/translator.toml`, `.claude/agents/translator.md`, `.codex/agents/editor.toml`, `.claude/agents/editor.md`

**Interfaces:**
- Produces: subagent names `translator`, `editor` referenced verbatim by Tasks 5–6 commands.

- [ ] **Step 1: Write `.opencode/agents/translator.md`** with exactly:

```markdown
---
description: Translates a Japanese light-novel chapter, or a single part of one, into a raw English draft. Dispatch for Stage 1 of the per-chapter pipeline.
mode: subagent
---
You are the translator for a Japanese light-novel translation pipeline.

<context>
You implement **Stage 1 (Translate P_i)** of `core/pipeline.md` — that file owns the stage contract, file paths, and done-criteria; this brief owns only your role and method. You embed zero series-specific facts; everything novel-specific lives in the per-novel files. Your dispatch prompt places the raw JP source at the TOP and these instructions after it — read the source first.
</context>

<objective>
A raw English draft that says exactly what the JP says — correct referents, nothing added or dropped — sitting at or below the source's register ceiling. You optimize accuracy + register fidelity. Naturalness is the editor's polish pass, NOT yours: a faithful, slightly stiff draft is better raw material than smooth translationese.
</objective>

<grounding_rules>
- Keep narration plain where the JP is plain: 気づいた → "noticed", not "registered" or "perceived"; 見た → "looked"/"stared", not "gazed".
- Every `glossary.md` term rendered exactly as listed; honorifics retained (-kun, -san, -chan, -sensei, …); family name first; furigana preserved as 漢字[かな]; romanization by vowel-doubling (ō→ou), never macrons; past-tense narration throughout.
- No in-file title heading — prose starts directly; the title is applied at filing time from `novel.config.md`.
- A term not in `glossary.md`: use your best rendering and flag it in your completion message — coined silently → wrong; coined and flagged → right.
- Translate only your assigned part; note anything out of scope instead of doing it. Never ask clarifying questions — cover the most likely intent and state the assumption.
</grounding_rules>

<workflow>
1. Read `novel.config.md`: locked register and chapter-title map.
2. Read `core/guides/translation-guide.md` and `core/guides/footnote-guide.md`.
3. Read `glossary.md`, `character-reference.md`, `character-voices.md` (voice profiles + narrator ceiling/kill-list), and `style-guide.md` (conventions + running summary).
4. For any part after the first, read the already-**edited** prior parts under `Editing/Volume N/` — the gated interleave guarantees they are on disk — so names, terms, and address forms carry forward clean.
5. Translate line by line against the JP source, applying the grounding rules to every sentence.
6. Write the draft to the exact output path the dispatch gives (the `Editing/Volume N/…` path from the `core/pipeline.md` file contracts).
7. Verify on disk that the draft exists and covers the whole assigned scope — every source image marker and scene break preserved. A partial draft is not done.
</workflow>

<output_format>
Report: the draft's path, confirmation of full-scope coverage, and a list of coined terms or judgment calls the editor and updater need — nothing else.
</output_format>
```

- [ ] **Step 2: Write `.opencode/agents/editor.md`.** Read `.codex/agents/editor.toml` (primary source) and `.claude/agents/editor.md`, then produce the same five-section structure as Step 1 with frontmatter:

```yaml
---
description: Line-by-line editor that edits a translator's draft against the raw Japanese source and finalizes whole-path chapters. Dispatch for Stage 2 of the per-chapter pipeline.
mode: subagent
---
```

Content requirements (all sourced from the TOML — carry its meaning, not its prose):
- `<context>`: implements Stage 2 (Edit P_i) of `core/pipeline.md`; dispatch places raw JP at top; zero series-specific facts.
- `<objective>`: a draft made accurate and natural line-by-line against the JP, capped at the locked register; on the whole path, the final `English/Volume N/` chapter file on disk.
- `<grounding_rules>`: edits happen line-by-line against the raw JP in ~150–200-line chunks — broad passes → wrong, chunked line-audit → right; polish pass is single-iteration and register-capped by the narrator ceiling + kill-list in `character-voices.md`; append every change to the per-chapter edit log per `core/schemas/edit-log-schema.md`; same mandatory-glossary/honorifics/tense/furigana/no-macron rules as the translator.
- `<workflow>`: numbered; reference-file reads first, then chunked edit passes, then (whole path only) finalization — write the final `English/Volume N/Chapter <N> - <Translated Title>.md` per the `core/pipeline.md` Stage 2 "Whole-path finalization" contract using a Python-via-Bash copy/transform with line-count verification, title from the `novel.config.md` chapter-title map, Windows-illegal-char sanitize rule honored.
- `<output_format>`: edited file path(s), edit-log confirmation, finalized-file path (whole path), open judgment calls.

- [ ] **Step 3: Verify**

Run: `python3 - <<'EOF'
import pathlib, yaml
for p in pathlib.Path('.opencode/agents').glob('*.md'):
    fm = p.read_text().split('---')[1]
    d = yaml.safe_load(fm)
    assert set(d) <= {'description','mode','permission'}, (p, set(d))
    assert d['mode'] == 'subagent', p
    for tag in ('<context>','<objective>','<grounding_rules>','<workflow>','<output_format>'):
        assert tag in p.read_text(), (p, tag)
print('ok')
EOF`
Expected: `ok`

- [ ] **Step 4: Commit**

```bash
git add .opencode/agents/translator.md .opencode/agents/editor.md
git commit -m "opencode: translator + editor subagents (DeepSeek v4 Pro prompt structure)"
```

---

### Task 3: Agents — assembler, qa-auditor, updater

**Files:**
- Create: `.opencode/agents/assembler.md`, `.opencode/agents/qa-auditor.md`, `.opencode/agents/updater.md`
- Read first: the matching `.codex/agents/*.toml` (primary) and `.claude/agents/*.md` (secondary) for each.

**Interfaces:**
- Produces: subagent names `assembler`, `qa-auditor`, `updater` referenced verbatim by Tasks 5–6.
- Consumes: the five-section structure and frontmatter pattern exactly as shown in Task 2 Step 1.

- [ ] **Step 1: Write `assembler.md`.** Frontmatter: `description: Combines edited chapter parts into the final chapter file with line-count verification, then reviews cross-part consistency. Dispatch for Stage 3 (parted chapters only).` + `mode: subagent`. Body sections sourced from the TOML: concatenation via Python-via-Bash (never retyping content — retype → wrong, mechanical copy with line-count check → right), final file to `English/Volume N/` per the `core/pipeline.md` file contract, no title heading (sanitize exception), cross-part consistency review afterward with findings routed back to the lead, not fixed silently.

- [ ] **Step 2: Write `qa-auditor.md`.** Frontmatter exactly:

```yaml
---
description: Independent MQM spot-auditor that reads the finished chapter against the raw Japanese and returns a PASS/FAIL report. Never edits chapter files. Dispatch fresh, once per audit.
mode: subagent
permission:
  edit: deny
---
```

Body sections sourced from the TOML: samples per `core/guides/qa-audit-guide.md` (10–15% coverage, dialogue over-sampled), classifies findings per MQM against `core/schemas/qa-report-schema.md`, verdict PASS/FAIL against the `qa_major_threshold` in `novel.config.md`; grounding rule pair — fixing a defect itself → wrong, reporting it with line refs → right; writes exactly one file: the QA report at the path the dispatch names.

- [ ] **Step 3: Write `updater.md`.** Frontmatter: `description: Adds new terms and characters from a finalized chapter to the per-novel reference files, appends the Running Summary entry, and runs the whole-unit consistency gate. Dispatch for Stage 5 after a QA PASS.` + `mode: subagent`. Body sections sourced from the TOML: append rows per the `core/schemas/` schemas; web-verify new terms against an official EN release/wiki when `novel.config.md` records one, else mark project-original; flag discrepancies with established voice/terms rather than rewriting them (rewrite → wrong, flag → right); append the chapter's `## Running Summary` entry to `style-guide.md`; after any glossary change run `python3 core/scripts/check_consistency.py --all` over the unit and report its exit status.

- [ ] **Step 4: Verify** — same python check as Task 2 Step 3 (it sweeps the whole `agents/` dir; qa-auditor additionally must contain `permission` with `edit: deny`).
Expected: `ok`

- [ ] **Step 5: Commit**

```bash
git add .opencode/agents/assembler.md .opencode/agents/qa-auditor.md .opencode/agents/updater.md
git commit -m "opencode: assembler + qa-auditor + updater subagents"
```

---

### Task 4: Agents — image-localizer, epub-builder

**Files:**
- Create: `.opencode/agents/image-localizer.md`, `.opencode/agents/epub-builder.md`
- Read first: the matching `.codex/agents/*.toml` (primary) and `.claude/agents/*.md` (secondary).

**Interfaces:**
- Produces: subagent names `image-localizer`, `epub-builder` referenced verbatim by Task 6's build-epub command.
- Consumes: the five-section structure and frontmatter pattern exactly as shown in Task 2 Step 1.

- [ ] **Step 1: Write `image-localizer.md`.** Frontmatter: `description: Finds text-bearing illustrations in a volume and writes zero-hallucination localization specs (verbatim JP + EN + edit prompt). Dispatch during the build-epub pipeline, before building.` + `mode: subagent`. Body from the TOML: scan the volume's source images; for each text-bearing one write a spec to `Editing/Volume N/image-localization/` containing the verbatim JP text, the EN rendering (glossary-exact), and an image-edit prompt; unreadable text → transcribe nothing and flag (guessing → wrong, flagged-unreadable → right).

- [ ] **Step 2: Write `epub-builder.md`.** Frontmatter: `description: Derives the build config from novel.config.md, runs the derive->build->verify invocation, then self-verifies the build gates. Dispatch as the final stage of the build-epub pipeline.` + `mode: subagent`. Body from the TOML: run the two-step `core/scripts/derive_build_config.py` → `core/scripts/build_epub.py` invocation then `verify_epub.py`, from the novel root; the build gates from `core/guides/epub-build-spec.md` must all pass; a failed gate → report with the failing gate's output, never hand-patch the EPUB (hand-edit output → wrong, fix input + rebuild → right).

- [ ] **Step 3: Verify** — same python check as Task 2 Step 3.
Expected: `ok`

- [ ] **Step 4: Commit**

```bash
git add .opencode/agents/image-localizer.md .opencode/agents/epub-builder.md
git commit -m "opencode: image-localizer + epub-builder subagents"
```

---

### Task 5: Command — translate-chapter

**Files:**
- Create: `.opencode/command/translate-chapter.md`
- Read first: `.agents/skills/translate-chapter/SKILL.md` (the content source), `.opencode/RUNTIME.md`

**Interfaces:**
- Consumes: subagent names `translator`, `editor`, `assembler`, `qa-auditor`, `updater` (Tasks 2–3).

- [ ] **Step 1: Write `.opencode/command/translate-chapter.md`.** Frontmatter:

```yaml
---
description: Runs the full per-chapter JP-LN pipeline — pre-gloss, translate/edit (interleaved per part), assemble, QA-audit, update, then the consistency and romaji gates.
---
```

The body is the template (OpenCode sends it as the prompt). First line: `Translate chapter $ARGUMENTS end to end.` Then adapt the body of `.agents/skills/translate-chapter/SKILL.md` with exactly these transformations and no others:
1. Drop the SKILL.md frontmatter and `# translate-chapter` heading.
2. In the Orchestration section, replace the sentence naming `.codex/agents/` with: `Dispatch the per-stage subagents in `.opencode/agents/` **by name** with the task tool: `translator`, `editor`, `assembler`, `qa-auditor`, `updater`. Subagents are ephemeral and isolated (that isolation is the design); you hold the ordering and pass each stage's full context in its dispatch. Dispatch at most **6 subagents concurrently**.`
3. Every other section (Outcome, Setup + PRE-GLOSS, path choice, gated ordering, QA FAIL loop, UPDATE, Gates, close-out) carries over with meaning intact — including: raw JP at top of every translate/edit/QA dispatch; parts never parallel; part i+1 gated on part i's edit verified on disk; fresh qa-auditor per audit; FAIL → editor fix → fresh re-audit loop; `run_chapter_gates.py` must exit 0.

- [ ] **Step 2: Verify**

Run: `grep -n '\$ARGUMENTS' .opencode/command/translate-chapter.md && grep -n 'opencode/agents' .opencode/command/translate-chapter.md && ! grep -n 'codex' .opencode/command/translate-chapter.md`
Expected: `$ARGUMENTS` present; `.opencode/agents` present; zero `codex` mentions.

- [ ] **Step 3: Commit**

```bash
git add .opencode/command/translate-chapter.md
git commit -m "opencode: /translate-chapter command"
```

---

### Task 6: Commands — setup-novel, build-epub + final sweep

**Files:**
- Create: `.opencode/command/setup-novel.md`, `.opencode/command/build-epub.md`
- Read first: `.agents/skills/setup-novel/SKILL.md`, `.agents/skills/build-epub/SKILL.md`

**Interfaces:**
- Consumes: subagent names `image-localizer`, `epub-builder` (Task 4); the same transformation rules as Task 5.

- [ ] **Step 1: Write `setup-novel.md`.** Frontmatter `description:` copied in meaning from the SKILL.md. Body: first line `Bootstrap this novel (one-time setup).`, then the SKILL.md body with the Task-5-style transformations (drop skill frontmatter/heading; re-point any dispatch wiring at `.opencode/agents/` + task tool; everything else meaning-intact). `$ARGUMENTS` is not needed (the skill takes no argument) — omit it.

- [ ] **Step 2: Write `build-epub.md`.** Frontmatter `description:` copied in meaning from the SKILL.md. Body: first line `Build the EPUB for volume $ARGUMENTS.`, then the SKILL.md body with the same transformations — dispatches `image-localizer` and `epub-builder` by name, keeps the deliberate user pause for image rendering, the whole-volume consistency gate, and the eight verify gates.

- [ ] **Step 3: Final verification sweep**

Run, from the novel root:
```bash
ls .opencode/agents/ .opencode/command/
grep -rn 'model:\|temperature:' .opencode/ opencode.json; echo "exit=$?"
grep -rln 'core/pipeline.md' .opencode/agents/ .opencode/command/ | wc -l
git diff --stat main -- AGENTS.md .codex .agents .claude core | wc -l
```
Expected: 7 agents + 3 commands listed; the model/temperature grep finds nothing (exit=1); pipeline.md cited by ≥ 8 of the 10 files; the last diff is empty (0 lines) — Codex-facing files untouched.

- [ ] **Step 4: Smoke-load in OpenCode (best effort).** Run `cd "$(pwd)" && opencode run --agent build 'List your available subagents and commands, then exit.' 2>&1 | head -30` if a non-interactive run is available; otherwise verify statically that every `.opencode/agents/*.md` frontmatter parses (Task 2 Step 3 check) and note in the completion report that TUI verification (`@` autocomplete + `/` commands) is left to the operator.

- [ ] **Step 5: Commit**

```bash
git add .opencode/command/setup-novel.md .opencode/command/build-epub.md
git commit -m "opencode: /setup-novel + /build-epub commands; runtime harness complete"
```
