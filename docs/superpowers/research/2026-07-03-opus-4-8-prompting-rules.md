# Opus 4.8 / Claude 4.x Prompting Rules — digest for authoring `.claude/` runtime pack

Sources: platform.claude.com — *Prompting Claude Opus 4.8* (model-specific) and *Claude prompting best practices*.

## Opus 4.8-specific (highest priority)

1. **Literal instruction following.** 4.8 interprets prompts literally; it does not generalize an instruction from one item to another or infer unstated requests. Every cross-item rule must state its scope explicitly: "Apply this to every part," "for all glossary terms" — never rely on generalization from one example.
2. **Favors reasoning over tool calls.** To get more tool use, explicitly describe when/why/how to use tools. Say "Change X" / "Make these edits," not "can you suggest."
3. **Verbosity is task-calibrated.** Positive examples of the desired concision beat "don't be verbose" instructions.
4. **Under-spawns subagents by default** (opposite of 4.5/4.6). Skills that want parallel teammates must explicitly authorize fan-out: "Spawn multiple subagents in the same turn when fanning out across items."
5. **Effort respected strictly**; default high. Fix shallow reasoning by raising effort, not prompting around it.
6. **Progress updates are native now** — remove old "summarize every N tool calls" scaffolding.
7. **Softened tool language.** "CRITICAL: You MUST use this tool" now over-triggers. Use plain "Use this tool when…". Remove "If in doubt, use X."
8. **Front-load complete task specs** when dispatching agents; progressive drip-feeding reduces token efficiency and performance.
9. **Coverage vs filtering:** if you want all findings (QA/audit), prompt for coverage — "Report every issue you find, including uncertain/low-severity ones, with confidence + severity" — not "only report important issues."

## General (all current models)

10. **Be explicit; no inferred "above and beyond."** Numbered sequential steps when order matters.
11. **Give the why.** The model generalizes correctly from rationale ("Your response will be read aloud by TTS, so never use ellipses").
12. **XML tags** to separate instructions / context / input / examples.
13. **Multishot examples** (3–5, diverse, wrapped in `<example>`) are the most reliable steering for format/tone.
14. **Long-context placement:** put long source documents at the TOP of the prompt, instructions/query AFTER (up to 30% quality gain). For translation dispatches: raw JP source first, then glossary/instructions.
15. **Tell what TO do, not what NOT to do**; match prompt formatting style to desired output style.
16. **Over-engineering guard** for coding agents: "Only make changes that are directly requested or clearly necessary."
17. **Hallucination guard:** "Never make claims about code/text you have not opened. Read the file before answering."
18. **Parallel tool calls:** explicitly authorize parallel independent calls.
19. Prefill on last assistant turn is dead (400 error); `budget_tokens` dead on 4.7+.

## Net rules applied to our agent/skill files

- Explicit scope on every cross-part/cross-chapter/all-terms rule.
- Kill-list rendered as wrong→right positive pairs, not "never" lists.
- Skills explicitly authorize teammate fan-out + parallel dispatch.
- Dispatch prompts: JP source at top, instructions after; complete spec up front.
- Plain "Do X when Y" phrasing; rationale attached to each non-obvious rule.
- QA auditor prompted for coverage with confidence+severity, not self-filtering.
