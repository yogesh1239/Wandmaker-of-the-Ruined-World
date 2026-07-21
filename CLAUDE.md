# [Novel Name] — JP Light Novel Translation Harness

Novel-agnostic Japanese light-novel translation pipeline (reusable template). The pipeline spec, guides, schemas, scripts, agents, and skills carry no series-specific facts; everything novel-specific lives in the per-novel files and `novel.config.md`.

This file is the entry point for Claude Code. Codex CLI users: root `AGENTS.md` is the entry point.

## Where things live

Three layers. The `core/` and runtime layers are agnostic and never edited per novel; the per-novel files are yours to fill.

| Layer | Files | Edit per novel? |
|-|-|-|
| Core (agnostic) | `core/pipeline.md` (canonical per-chapter spec), `core/guides/*.md`, `core/schemas/*.md`, `core/scripts/*.py` | No |
| Runtimes (agnostic) | `.claude/` (agents + skills for Claude Code); `AGENTS.md` + `.codex/agents/` + `.agents/skills/` (for Codex CLI); `opencode.json` + `.opencode/` (agents + commands + RUNTIME.md for OpenCode / DeepSeek v4 Pro) | No |
| Per-novel data | `novel.config.md` (the knobs), `glossary.md`, `character-reference.md`, `character-voices.md`, `style-guide.md`, `translation-progress.md` | Yes — filled as you translate |

Both runtimes cite `core/pipeline.md` for stages, ordering, file contracts, and gates; they carry only role framing and tool wiring, not the pipeline facts. Every agent reads `novel.config.md` (locked register + conventions), `glossary.md`, `character-reference.md`, `character-voices.md`, and `style-guide.md` before working.

### Core guides

| File | Purpose |
|-|-|
| [core/pipeline.md](core/pipeline.md) | Canonical per-chapter spec: stages, dependency graph, file contracts, gate commands, done-criteria |
| [core/guides/translation-guide.md](core/guides/translation-guide.md) | Author voice, tense, register framework, honorifics, name order, SFX |
| [core/guides/footnote-guide.md](core/guides/footnote-guide.md) | When/how to annotate; cultural-term reference |
| [core/guides/voice-building-guide.md](core/guides/voice-building-guide.md) | Method for deriving per-character voice profiles |
| [core/guides/quality-checklist.md](core/guides/quality-checklist.md) | Pre-submission checklist |
| [core/guides/epub-build-spec.md](core/guides/epub-build-spec.md) | Spine mapping, RTL→LTR, popup footnotes, build gates |

## Pipeline

Each skill runs as lead of the session's team, spawning `.claude/agents/` teammates and coordinating them over a task board. `core/pipeline.md` is the single source of truth for the per-chapter flow; the one-liners below only point at it.

```
/setup-novel                  one-time: split Vol 1 → seed glossary/characters/voices/style-guide → translate TOC → lock register → fill config
/translate-chapter [chapter]  pre-gloss → translate/edit (interleaved per part for long chapters) → assemble → update → consistency + romaji gates
/build-epub [volume]          image-localize → whole-volume consistency gate → build_epub.py → verify_epub.py
```

## Output convention

- Final chapter file: `English/Volume N/Chapter <N> - <Translated Title>.md`.
- No title heading inside the file — prose starts directly; a `## Translator Notes` section (if any) goes at the end. Titles come from the chapter-title map in `novel.config.md`. Exception: if a title contains a Windows-illegal char (`< > : " / \ | ? *`), sanitize the filename and write the full true title once as a leading `#` heading. Full contract in [core/pipeline.md](core/pipeline.md).

## Critical rules (non-negotiable)

1. Past-tense narration — always.
2. Register is locked — read it from `novel.config.md`; never elevate past the source's ceiling.
3. Honorifics retained — -kun, -san, -chan, -sensei, onee-san, etc.
4. JP name order — family name first.
5. Glossary terms are mandatory — exact matches from `glossary.md`.
6. Furigana preserved from source as `漢字[かな]`.
7. Romanization: no macrons — vowel-doubling (ō→ou, ū→uu, ā→aa, ī→ii, ē→ee); enforced by `core/scripts/normalize_romaji.py --check`.
8. Editors edit line-by-line against the raw Japanese, not broad passes.
9. Consistency gates — `core/scripts/check_consistency.py` runs per-chapter, and again with `--all` over the whole unit after every Update, because a glossary revision back-propagates to already-filed chapters in that unit. For light novels the unit is usually a volume; for webnovels it may be `main`, an arc, or another project-defined grouping.
10. Teammate lifetime is one chapter — translator/editor are reused across a chapter's parts and retired at chapter end; cross-chapter continuity is file-borne only.
11. Polish pass is single-iteration and register-capped — one polish pass per part, bounded by the register ceiling and kill-list in `character-voices.md` (see [core/pipeline.md](core/pipeline.md) Stage 2).

## Starting a new novel (template → live project)

1. Copy this whole folder to your translations directory under the novel's name.
2. Drop the source ebook(s) (`.epub` / `.azw3`) into the folder root.
3. Edit `novel.config.md` (identity, source→volume map, conventions).
4. For `.azw3` sources, vendor KindleUnpack into `core/scripts/kindleunpack/` (see its README — no Calibre).
5. Reset the per-novel data files to empty stubs: `glossary.md`, `character-reference.md`, `character-voices.md`, `style-guide.md`, `translation-progress.md`.
6. Run `/setup-novel` — it splits Volume 1, seeds the reference files, translates the chapter-title TOC into `novel.config.md`, and locks the register.
7. Run `/translate-chapter [chapter]` per chapter; `/build-epub [volume]` per volume.

## Design

Full design + rationale: [docs/superpowers/specs/2026-07-03-harness-overhaul-and-cn-sibling-design.md](docs/superpowers/specs/2026-07-03-harness-overhaul-and-cn-sibling-design.md)
</content>
</invoke>
