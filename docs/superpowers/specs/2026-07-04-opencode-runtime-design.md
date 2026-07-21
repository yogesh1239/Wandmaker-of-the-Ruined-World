# OpenCode Runtime Harness (DeepSeek v4 Pro) — Design

Date: 2026-07-04
Status: approved

## Goal

Add a third runtime layer to the JP translation harness so the pipeline runs under
**OpenCode** with **DeepSeek v4 Pro** as the session model — parallel to the existing
Claude Code (`.claude/`) and Codex CLI (`.codex/` + `.agents/skills/`) runtimes.
OpenCode must load the agent definitions natively from the repo, with no shim.

Core constraint carried over from the other runtimes: the runtime layer holds only
role framing and tool wiring. Pipeline facts live once in `core/pipeline.md`; agents
and commands cite it, never restate it. Zero series-specific facts anywhere.

## Hard requirements (from the user)

1. **No model pinning.** Agent frontmatter carries no `model:` and no `temperature:`.
   Subagents inherit the invoking session's model (OpenCode semantics), so the same
   files run under DeepSeek v4 Pro today or any future session model.
2. **DeepSeek v4 Pro prompting style**, not model-specific config: the agent bodies
   and command templates are *written to* DeepSeek v4 Pro prompting guidance.
3. **Codex must be unaffected.** `AGENTS.md` is not edited. All OpenCode wiring lives
   in files Codex never reads (`opencode.json`, `.opencode/**`).

## Layout (new files only)

```
opencode.json                     project config: { "instructions": [".opencode/RUNTIME.md"] }
.opencode/
  RUNTIME.md                      OpenCode-runtime wiring doc (see below)
  agents/
    translator.md                 mode: subagent
    editor.md                     mode: subagent
    assembler.md                  mode: subagent
    qa-auditor.md                 mode: subagent, permission: edit: deny
    updater.md                    mode: subagent
    image-localizer.md            mode: subagent
    epub-builder.md               mode: subagent
  command/
    setup-novel.md
    translate-chapter.md          template uses $ARGUMENTS for the chapter number
    build-epub.md                 template uses $ARGUMENTS for the volume number
CLAUDE.md                         one table-row edit: OpenCode added to the runtimes layer
```

Directory names `agents/` and `command/` match the user's working global OpenCode
config (`~/.config/opencode/`, OpenCode 1.17.13) — the installed version's honored
discovery paths.

## RUNTIME.md (the wiring doc)

OpenCode auto-loads `AGENTS.md` and this cannot be disabled, so `RUNTIME.md` (injected
via `opencode.json` `instructions`) must:

- Declare the reader the **OpenCode runtime** and scope out the other runtimes'
  wiring: the `.codex/agents/` + `.agents/skills/` dispatch mechanics in `AGENTS.md`
  do not apply; the shared non-negotiables, pointers, and gate commands in `AGENTS.md`
  do apply.
- Wire dispatch: per-stage subagents live in `.opencode/agents/` and are invoked via
  OpenCode's task tool (or `@name`); commands live in `.opencode/command/`.
- Restate the two operational rules that are runtime-mechanic-specific:
  the qa-auditor always runs as a fresh subagent (independent context is the point),
  and the per-part interleave is a gated handoff — never translate parts in parallel;
  part i+1 waits until part i's edit is verified on disk.

## Agent definition format

OpenCode markdown agents: YAML frontmatter + body-as-system-prompt.

Frontmatter keys used: `description` (always), `mode: subagent` (always),
`permission` (qa-auditor only: `edit: deny` — it writes its QA report with the
write tool but can never modify chapter files; the OpenCode equivalent of the Codex
read-only sandbox without the approval-escalation friction). Nothing else — no
`model`, no `temperature`, no `tools` lists.

## Prompt style: DeepSeek v4 Pro guidance

Content parity with the `.codex/agents/*.toml` briefs (same roles, same stage
contracts, same constraints), restructured to what DeepSeek v4 Pro measurably
rewards:

- **Explicit structure**: bodies use tagged sections — `<context>`, `<objective>`,
  `<grounding_rules>`, `<workflow>`, `<output_format>`. v4 Pro responds strongly to
  explicit "grounding box" constraint blocks.
- **Numbered reasoning scaffolds**: each `<workflow>` is an explicit ordered step
  list (v4 Pro wants structured chain-of-thought; unstructured prose briefs
  underperform).
- **No persona flourish**: one role sentence, then structure. Character/personality
  prompts reduce v4 consistency.
- **Positive wrong→right constraint pairs**, not bare negations ("don't hallucinate"
  has no effect) — e.g. 気づいた → "noticed", not "registered". Matches the existing
  kill-list format.
- **Single language**: instructions in English; Japanese appears only as data.
- **Long-input ordering kept**: dispatch prompts place the raw JP source at the top,
  instructions after — same as the other runtimes.

## Commands

The three skills become OpenCode commands (`description` + `template` frontmatter,
`$ARGUMENTS` placeholder). Bodies adapted from `.agents/skills/*/SKILL.md` — those
are runtime-neutral except their dispatch-wiring paragraphs, which are swapped for
OpenCode task-tool dispatch. Everything else carries over unchanged: gated
interleave, fresh qa-auditor per audit, QA FAIL loop, ≤6 concurrent subagents,
on-disk verification per stage, gate wrapper `run_chapter_gates.py` must exit 0.

## Explicitly out of scope

- No changes to `core/**`, per-novel files, `.claude/**`, `.codex/**`,
  `.agents/**`, or `AGENTS.md`.
- No OpenCode plugin/JS config; markdown + `opencode.json` only.
- No CN-harness sibling in this pass (port after this lands, same as the JP→CN flow).

## Verification

- `opencode agent list` (or TUI `@` autocomplete) shows the 7 subagents; `/setup-novel`,
  `/translate-chapter`, `/build-epub` appear as commands.
- Frontmatter of every agent parses as YAML and contains no `model`/`temperature`.
- Grep gates: no series-specific facts; no `.codex/` or `.claude/` paths inside
  `.opencode/**` except the RUNTIME.md scoping note; every agent and command cites
  `core/pipeline.md`.
- Codex-unaffected check: `git diff` touches no file Codex reads (`AGENTS.md`,
  `.codex/**`, `.agents/**`).
