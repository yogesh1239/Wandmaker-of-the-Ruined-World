# GPT-5.5 + Codex CLI Rules — digest for authoring the Codex runtime pack

Sources: developers.openai.com (GPT-5.5 prompting guide, Codex prompting guide, AGENTS.md guide, skills, subagents, config reference, sandboxing), cookbook.openai.com.

## GPT-5.5 prompt-writing

1. **Fresh baseline, not ported prompts.** Legacy step-by-step process prompts add noise on 5.5. Start from the smallest prompt that preserves the contract; define the OUTCOME (what good looks like, constraints, required evidence, required output) and leave the solution path to the model.
2. **`reasoning_effort`**: none|minimal|low|medium|high|xhigh. Pin explicitly; medium is the baseline; high/xhigh for hardest accuracy-critical work.
3. **`verbosity`** separate from reasoning; reinforce in-prompt ("Default: 3–6 sentences or ≤5 bullets…").
4. **Contradiction-sensitive.** 5.5 has strong instruction adherence, so internal contradictions actively degrade output. Put discrete rule clusters in separate tagged blocks; audit for conflicts.
5. **Persistence up, eagerness scoped:** "Keep going until the task is truly done." + "Do not expand the task beyond what was asked; if you notice new work, call it out as optional."
6. **Tool preambles:** brief updates only at new major phases or plan changes, each carrying a concrete outcome; no routine narration.
7. **Anti-sycophancy / autonomous mode:** for pipeline agents — "Never ask clarifying questions; cover the most likely intent," and never end turn with unrequested clarifications.
8. **Long inputs (>10k tokens):** first produce a short internal outline of relevant sections; restate constraints before answering; never fabricate figures/line numbers.
9. **Structured output:** 5.5 follows schemas strictly; "no extra fields; null rather than guessing; re-scan before returning."

## Codex CLI mechanics

10. **AGENTS.md discovery:** `~/.codex/AGENTS.md` (global) then git-root→cwd walk; closer-to-cwd overrides; ~32 KiB chain cap — once hit, deeper files are silently dropped. Repo AGENTS.md must be at repo root; keep lean.
11. **Skills:** repo path `.agents/skills/<name>/SKILL.md` (official docs; some secondary sources claim `.codex/skills/` — verify live at implementation). Frontmatter `name` + `description`; description alone drives selection. Custom prompts (`~/.codex/prompts/`) are DEPRECATED — use skills.
12. **Subagents (GA March 2026):** custom agents = TOML files in `.codex/agents/` (project) or `~/.codex/agents/` (personal). Fields: `name`, `description`, `developer_instructions` (required); `model`, `model_reasoning_effort`, `sandbox_mode`, `nickname_candidates`, `mcp_servers`, `skills.config` (optional). Built-in roles: default, worker, explorer.
13. **Subagent lifecycle:** spawn → wait → collect → close. Ephemeral; NO persistent named teammates, NO shared task board. Invoked by naming them in prose (from the user or a skill's instructions) — no programmatic dispatch API. Parallel: yes; isolated context: yes (design purpose = keep noise out of the main thread).
14. **Limits:** `agents.max_depth` default 1 (no nesting); `agents.max_threads` default 6; `agents.job_max_runtime_seconds` 1800. Subagents inherit parent sandbox; per-agent `sandbox_mode` read-only|workspace-write. Batch primitive: `spawn_agents_on_csv`.
15. **Sandbox/approvals:** read-only | workspace-write (default) | danger-full-access × untrusted | on-request | on-failure | never. Two independent controls.
16. **Codex defaults to bias-to-action / don't-ask.** Gated handoffs (per-part interleave) must be explicitly encoded: "do not proceed to part i+1 until part i's edit is verified on disk."

## Net rules applied to our Codex pack

- Root `AGENTS.md`: non-negotiables (register lock, past tense, honorifics, glossary compliance, gates) + pointers into `core/`; well under 32 KiB.
- Per-role TOML agents in `.codex/agents/`: translator/editor/qa-auditor `model_reasoning_effort = "high"`, others `"medium"`; qa-auditor `sandbox_mode = "read-only"`.
- Three orchestrating skills in `.agents/skills/`; ordering + disk-verification gates expressed as explicit prose; qa-auditor always dispatched as a subagent for context isolation.
- Outcome-oriented phrasing throughout; separate tagged rule blocks; persistence + scope-guard lines in each skill.
