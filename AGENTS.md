# JP Light-Novel Translation Harness — Codex runtime

You are working inside a novel-agnostic Japanese light-novel translation pipeline. The harness carries **zero series-specific facts**: everything about *this* novel lives in the per-novel files (`novel.config.md`, `glossary.md`, `character-reference.md`, `character-voices.md`, `style-guide.md`). Read those, never hardcode a name, term, or path.

The pipeline itself — stages, dependency graph, file contracts, per-stage done-criteria — is defined once in `core/pipeline.md`. This file and the agents/skills **cite** it; they do not restate it. When the two ever disagree, `core/pipeline.md` wins.

<non_negotiables>
These hold on every line of translated output, at every stage. They are not stylistic preferences; a violation is a defect.

- **Past-tense narration** — always.
- **Register is locked.** Read the locked register from `novel.config.md` (Register Lock) and never elevate a line above the source's own ceiling. The Narrator ceiling + kill-list in `character-voices.md` are a hard cap.
- **Honorifics retained** — `-kun`, `-san`, `-chan`, `-sensei`, `onee-san`, etc.
- **JP name order** — family name first.
- **Glossary is mandatory.** Use the exact EN rendering in `glossary.md` for every listed term. A term's banned aliases (its listed wrong renderings) never appear in output.
- **Furigana notation** — preserve source furigana as `漢字[かな]`.
- **Romanization lock.** Follow the convention in `novel.config.md` and exact forms in `glossary.md`; never use macrons. This novel leaves Japanese long vowels unmarked (`Ohinata`, not `Oohinata`). Enforced by `core/scripts/normalize_romaji.py --check` and the consistency gate.
- **No in-file title heading.** The final chapter file starts directly with prose; `## Translator Notes` (if any) goes at the end. Titles come from the `novel.config.md` chapter-title map. Sole exception: a title containing a Windows-illegal char (`< > : " / \ | ? *`) → sanitize the filename and write the full true title once as a single leading `#` heading.
</non_negotiables>

<pointers>
- `core/pipeline.md` — the per-chapter spec: stages, dependency graph, file contracts, gate commands, done-criteria. Source of truth.
- `core/guides/` — `translation-guide.md`, `footnote-guide.md`, `voice-building-guide.md`, `quality-checklist.md`, `epub-build-spec.md`. The how-to for each craft; cite, don't copy.
- `core/schemas/` — the exact format for every data file (`glossary-schema.md`, `character-voices-schema.md`, `edit-log-schema.md`, `style-guide-schema.md`, `novel-config-schema.md`). Write data files to their schema; never copy a schema's contents into prose.
- `core/scripts/` — the gate and build scripts. Run from the novel-root directory (where `novel.config.md` sits).
</pointers>

<agents_and_skills>
- **Per-stage agents live in `.codex/agents/`** (translator, editor, assembler, updater, image-localizer, epub-builder). Dispatch them **by name** from a skill's instructions; each inherits the session model and carries its own reasoning-effort and sandbox settings.
- **Skills live in `.agents/skills/`** (`setup-novel`, `translate-chapter`, `build-epub`) — the discovery path this Codex build honors. (This build also honors `.codex/skills/`; the pack uses `.agents/skills/`.)
- Codex biases to action; the pipeline's per-part interleave is a **gated** handoff. Never translate a chapter's parts in parallel, and do not proceed to part i+1 until part i's edit is verified on disk.
</agents_and_skills>

<gate_commands>
Run from the novel-root directory. Prefer the wrapper; it resolves the filed chapter from `novel.config.md` and exits non-zero on a violation. If the chapter number is unique:

```bash
python3 core/scripts/run_chapter_gates.py --chapter <N>
```

If the chapter number appears in more than one configured unit:

```bash
python3 core/scripts/run_chapter_gates.py --unit <Unit> --chapter <N>
```

Debug equivalent, with explicit paths substituted from `novel.config.md`:

```bash
# Romanization: no macrons
python3 core/scripts/normalize_romaji.py --check "<English path>/Chapter <N> - <Title>.md"

# Deterministic consistency, this chapter
python3 core/scripts/check_consistency.py --glossary glossary.md "<English path>/Chapter <N> - <Title>.md"

# Deterministic consistency, whole unit
python3 core/scripts/check_consistency.py --glossary glossary.md --all "<English path>"
```
</gate_commands>

<working_disposition>
- **Persistence:** keep going until the task is truly done — every stage output verified on disk, every gate green.
- **Scope guard:** do not expand the task beyond what was asked. If you notice new work, call it out as optional rather than doing it silently.
- **Autonomous:** never ask clarifying questions mid-pipeline; cover the most likely intent and proceed. Do not end a turn with unrequested clarifications.
</working_disposition>
