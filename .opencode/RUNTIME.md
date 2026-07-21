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
