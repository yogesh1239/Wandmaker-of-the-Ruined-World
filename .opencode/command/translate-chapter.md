---
description: Runs the full per-chapter JP-LN pipeline — pre-gloss, translate/edit (interleaved per part), assemble, update, then the consistency and romaji gates.
---

Translate chapter $ARGUMENTS end to end.

Run the full per-chapter pipeline for the given chapter. The canonical stage list, dependency graph, file contracts, gate commands, and per-stage done-criteria live in `core/pipeline.md`; this command orchestrates them and does not restate them.

## Outcome

The chapter filed to `English/Volume N/Chapter <N> - <Translated Title>.md` — accurate to the JP, at the locked register, glossary-consistent — having passed all three deterministic gates, with the reference files updated to reflect it.

## Orchestration

Dispatch the per-stage subagents in `.opencode/agents/` **by name** with the task tool: `translator`, `editor`, `assembler`, `updater`. Subagents are ephemeral and isolated (that isolation is the design); you hold the ordering and pass each stage's full context in its dispatch. Dispatch at most **6 subagents concurrently**.

**Front-load every dispatch** with the complete spec: the source file, the part `P<i>` and its source line range, the output path, and the reference files to read. **Every translate and edit dispatch places the raw JP source for that scope at the TOP of the prompt and the instructions after it** — long source first, query after, preserves accuracy on long inputs. Embed that source scope **once** per dispatch; never repeat chapter text in a follow-up message — reference file paths and line ranges instead.

Before dispatching, derive the chapter's names, titles, places, organizations, technical terms, and recurring phrases from the JP source. `Grep` their JP/base forms and any known EN renderings across `glossary.md`, `character-reference.md`, `character-voices.md`, `style-guide.md`, and relevant filed chapters; read the surrounding row/profile/summary for every hit. Include that curated context in the dispatch, while requiring each linguistic subagent to repeat targeted lookup for anything it encounters outside the curation. A single no-hit grep never proves a term is new; search furigana-free, spelling, and EN variants first.

Verify each stage's output **structurally** with `Bash` (`wc -l`, `head`/`tail`, `grep` for required markers) before treating it as done — never `Read` a draft or chapter in full (`core/pipeline.md`, structural-verification rule). The editor's line-by-line pass owns content verification.

## 1. Setup + PRE-GLOSS

Read `novel.config.md`: chapter-title map (`<N>` + translated title → filename), locked register, paths, and the **part-split threshold**. Locate the chapter's JP source under `Source/Volume N/` and count its source lines. Then run **Stage 0 (PRE-GLOSS)** yourself: scan the whole chapter source for candidate terms, perform the targeted multi-file searches above for each candidate and its variants, and add only truly new rows per `glossary-schema.md`. Finish this before any translate dispatch so translators inject a complete glossary, not a stale one.

## 2. Choose the path by length

- **Source lines > threshold → PARTED:** split the source into parts P1…Pn at natural scene breaks; run translate/edit interleaved per the graph; then assemble.
- **Source lines ≤ threshold → WHOLE:** one translate, one edit; the editor finalizes the chapter file itself after its two passes (no assemble stage — `core/pipeline.md`, Stage 2 "Whole-path finalization").

## 3. Drive the pipeline (gated ordering)

Follow the dependency graph in `core/pipeline.md` exactly; do not invent an ordering.

1. **Translate P_i / whole** → dispatch `translator`. For i > 1, it reads the already-**edited** prior parts for continuity.
2. **Edit P_i / whole** → dispatch `editor`. On the **whole** path the editor also **finalizes** — writing the final `English/Volume N/` file itself (`core/pipeline.md`, Stage 2); verify it on disk.
3. **Assemble** (parted only) → dispatch `assembler`; route any reconciliation fix it surfaces (a drifted pronoun) back to an `editor`.

**The parts are never translated in parallel.** The interleave is a **gated handoff**: **do not proceed to part i+1 until part i's edit is verified on disk.** Part i+1 is translated against the *edited* part i so continuity (names, voice, address forms) carries forward clean — releasing i+1 early defeats the whole point of the graph. Exactly one translate is ever unblocked at a time.

## 4. UPDATE

After the final chapter exists, dispatch the `updater` (**Stage 4**): it adds new terms/characters to the reference files, web-verifies against an official EN release or wiki when `novel.config.md` records one (else marks project-original), appends this chapter's `## Running Summary` entry to `style-guide.md`, and **flags** discrepancies rather than rewriting established voice/terms.

## 5. Gates (wrapper must exit 0)

Run the gate wrapper from `core/pipeline.md`. If the chapter number is unique:

```bash
python3 core/scripts/run_chapter_gates.py --chapter N
```

If the chapter number appears in more than one configured unit:

```bash
python3 core/scripts/run_chapter_gates.py --unit "<Unit>" --chapter N
```

The wrapper runs romanization, chapter consistency, and whole-unit consistency
in order. On any non-zero exit, fix (or route to an `editor`) and re-run until
clean.

## 6. Confirm + close

By now the final chapter is filed at `English/Volume N/Chapter <N> - <Translated Title>.md` (number and title from the config map) by its owner — the **assembler** on the parted path, the **editor** on the whole path (`core/pipeline.md`, File contracts + Stage 2/3), which is why the §5 gates could already run against it. Confirm it is on disk. Update `translation-progress.md` (status + any flagged discrepancies).

## Disposition

Persistence: keep going until the chapter is filed, all three gates exit 0, and the references are updated. Scope guard: translate only the requested chapter; note anything larger (other chapters, a full-volume build) as optional. Never ask clarifying questions; cover the most likely intent.

## Report

Final chapter path; parted vs whole; new glossary/character entries (count); flagged discrepancies; and the wrapper output for the chapter gates.
