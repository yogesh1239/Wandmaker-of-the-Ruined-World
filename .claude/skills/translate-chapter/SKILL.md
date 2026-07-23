---
name: translate-chapter
description: Runs the full per-chapter Japanese-LN pipeline — pre-gloss, translate/edit (interleaved per part for long chapters), assemble, update, then the consistency and romaji gates. Usage: /translate-chapter [chapter]
argument-hint: "[chapter]"
---

# /translate-chapter [chapter]

Run the full per-chapter pipeline for the chapter at `$ARGUMENTS` (ask the user which chapter if none is given). You act as **lead** of the session's team. The canonical stage list, dependency graph, file contracts, gate commands, and per-stage done-criteria live in `core/pipeline.md`; this skill orchestrates them and does not restate them.

## Orchestration

The team is implicit — the session already has one, so you register no team and create none. You spawn teammates directly with the **Agent** tool (`subagent_type` = the `.claude/agents/` name: `translator`, `editor`, `assembler`, `updater`) and coordinate them with `TaskCreate` / `TaskList` / `TaskUpdate` dependencies plus `SendMessage`.

**Teammate lifetime is one chapter (`core/pipeline.md`, "Teammate lifetime").** Spawn one `translator` and one `editor` at the start of this chapter and **reuse each across all of this chapter's parts by sending the next part assignment with `SendMessage`** — their hot context (this chapter's source and edited parts) is exactly the continuity the interleave needs. Retire both at chapter end; the next chapter gets fresh spawns, because a teammate carrying prior chapters' drafts accumulates dead context that fights an updater-revised glossary.

**When lead-side work is genuinely independent — e.g. pre-glossing this chapter while confirming paths and counting source lines — spawn the needed subagents in the same turn** rather than serializing them; only serialize where the dependency graph forces it. **The chapter's parts are never translated in parallel:** the interleave (`Translate P(i+1)` blockedBy `Edit Pi`) exists precisely so part i+1 is translated against the *edited* part i, so exactly one translate task is ever unblocked at a time — releasing part i+1 early defeats the continuity the whole graph is built for. Front-load each dispatch with the complete task spec (source file, part `P<i>` and its source line range, output path, and the reference files to read) instead of drip-feeding follow-ups. **Every translate and edit dispatch places the raw JP source for that scope at the TOP of the prompt and the instructions after it** — long source at the top, query after, is what preserves accuracy on long inputs. Embed that source scope **once**, in the dispatch; a later `SendMessage` to a reused teammate (the next part's assignment) references file paths and line ranges only — never re-echo chapter text into the thread.

Before each dispatch, derive relevant names, titles, places, organizations, abilities, technical terms, and recurring phrases from the JP scope. `Grep` their JP/base and known EN forms across `glossary.md`, `character-reference.md`, `character-voices.md`, `style-guide.md`, and relevant filed chapters; read the complete surrounding entry for every hit and include those hits in the dispatch. Subagents repeat targeted lookup for uncovered source items. A single no-hit search never proves novelty; search furigana-free, spelling, and EN variants first.

Verify each stage's output **structurally** with `Bash` — `wc -l` against the expected scope, `head`/`tail` for the required leading/trailing sections, `grep` for required markers — before marking its task complete; never `Read` a draft or chapter in full (`core/pipeline.md`, structural-verification rule). The translator and editor own content accuracy; the lead verifies each stage output before releasing dependents.

## 1. Setup + PRE-GLOSS

Read `novel.config.md`: the chapter-title map (`<N>` + translated title → output filename), the locked register, paths, and the **part-split threshold**. Locate the chapter's JP source under `Source/Volume N/` and count its source lines.

Run **Stage 0 (PRE-GLOSS)** yourself before any translate task starts: scan the whole chapter source for candidates, perform the targeted multi-file and variant searches above, and add only truly new rows per `core/schemas/glossary-schema.md`. Translators must inject a complete glossary, not a stale one, so finish this before dispatching Stage 1.

## 2. Choose the path by length

Compare the chapter's source-line count to the part-split threshold (`core/pipeline.md`, "Path by length"):

- **Source lines > threshold → evaluate natural scopes.** Target roughly one threshold-sized source scope per translation part. Around each target line, choose the nearest appropriate boundary: prefer an explicit `---`, then a scene or POV break, then a paragraph break. Never cut a scene merely to hit the exact line count. If the final remainder would be much smaller, move the preceding boundary earlier or merge it. When that merge leaves the complete chapter as one scope still reasonably close to the threshold, use the WHOLE path rather than creating undersized parts; otherwise use the PARTED path. Do not use the editor's ~150–200-line audit chunks as translation-part boundaries. Then build and drive the full dependency graph.
- **Source lines ≤ threshold → WHOLE path.** One Translate, one Edit; the editor finalizes the chapter file itself after its two passes (no Assemble stage — `core/pipeline.md`, Stage 2 "Whole-path finalization").

## 3. Build the task graph

Create the tasks with the dependencies from `core/pipeline.md` ("Dependency graph"). Do not invent an ordering — mirror the graph:

- `Edit Pi` **blockedBy** `Translate Pi`.
- `Translate P(i+1)` **blockedBy** `Edit Pi` (the interleave — part i+1 is translated against the *edited* part i).
- `Assemble` **blockedBy** every `Edit Pi` (parted path only).
- `Update` **blockedBy** `Assemble` (parted) or `Edit` (whole).

Drafts and the edit log live under `Editing/Volume N/` per the File contracts table in `core/pipeline.md`; the final chapter is filed to `English/Volume N/` only at assembly (parted) or as the edited draft (whole).

## 4. Drive the graph

Release each task as its blockers clear, dispatching the owning teammate:

1. **Translate Pi / whole** → `translator`. For i > 1 it reads the already-*edited* prior parts for continuity, which the graph guarantees are on disk.
2. **Edit Pi / whole** → `editor`. Only after Edit Pi is verified on disk do you release Translate P(i+1). On the **whole** path the editor also **finalizes** the chapter — writing the final `English/Volume N/` file itself (`core/pipeline.md`, Stage 2); verify that file on disk.
3. **Assemble** (parted only) → `assembler`. Route any reconciliation fix it surfaces (e.g. a drifted pronoun) back to the relevant `editor` via `SendMessage`.

## 5. UPDATE

After the final chapter exists, dispatch the `updater` (**Stage 4**). It adds new terms/characters to `glossary.md` / `character-reference.md` / `character-voices.md`, web-verifies against an official EN release or wiki when `novel.config.md` records one (else marks project-original), appends this chapter's `## Running Summary` entry to `style-guide.md`, and **flags** discrepancies rather than silently rewriting established voice or terms.

## 6. Gates (wrapper must exit 0)

Run the gate wrapper from `core/pipeline.md`. If the chapter number is unique:

```bash
python3 core/scripts/run_chapter_gates.py --chapter N
```

If the chapter number appears in more than one configured unit:

```bash
python3 core/scripts/run_chapter_gates.py --unit "<Unit>" --chapter N
```

The wrapper runs romanization, chapter consistency, and whole-unit consistency
in order. On any non-zero exit, fix (or route to the `editor`) and re-run until
clean.

## 7. Confirm the filed output + lifecycle

By now the final chapter is filed at `English/Volume N/Chapter <N> - <Translated Title>.md` (number and title from the config chapter-title map) by its owner — the **assembler** on the parted path, the **editor** on the whole path (`core/pipeline.md`, File contracts + Stage 2/3), which is why the gates in §6 could already run against it. Confirm it is on disk.

Update `translation-progress.md` (chapter status + any flagged discrepancies). Retire this chapter's `translator` and `editor` (`SendMessage` shutdown); spawn fresh ones for the next chapter.

## Report

Final chapter path; parted vs whole; new glossary/character entries (count); flagged discrepancies; and the wrapper output for the chapter gates.
