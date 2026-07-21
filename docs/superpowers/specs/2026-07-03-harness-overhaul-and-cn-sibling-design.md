# Harness Overhaul (JP) + Chinese Webnovel Sibling — Design

**Date:** 2026-07-03
**Status:** Approved design
**Supersedes:** `2026-06-14-novel-agnostic-translation-workflow-design.md` (architecture retained; orchestration, quality machinery, and layout revised)

## 1. Goals

1. **Modernize orchestration** — the harness was built on `TeamCreate`/`TeamDelete`, which no longer exist in Claude Code. Re-express the pipeline on current tooling (Agent tool + implicit session team + TaskCreate/TaskList/TaskUpdate + SendMessage).
2. **Fix production quality failures** — stiff/literal prose, term/voice drift across chapters, editor passes that rubber-stamp instead of catching mistranslations.
3. **Model-agnostic core + two tuned runtimes** — one source of truth for all facts; a Claude Code runtime written to Anthropic's Opus 4.8 prompting guidelines; a Codex CLI runtime written to OpenAI's GPT-5.5 guidelines.
4. **CN webnovel sibling harness** — a parallel template folder for Chinese webnovels (raw scraped chapters, no source EPUB), sharing the architecture.

## 2. Locked decisions

| Decision | Choice |
|-|-|
| Variant architecture | Shared `core/` + two thin runtime packs (`.claude/`, `codex/`); no fact duplicated |
| Runtimes | Claude Code (Opus 4.8-tuned) and Codex CLI (GPT-5.5-tuned, AGENTS.md + Codex skills) |
| Quality gates added | QA spot-audit agent (MQM-style), `check_consistency.py` deterministic gate, mandatory voice/kill-list authoring at setup |
| Editor reframing | Line-by-line accuracy pass + explicit **polish sub-pass** ("native-authored English", register-capped) |
| New per-novel file | `style-guide.md` (persistent style guide + running plot summary) |
| CN harness | Sibling folder `CN Translation Initialisation`; raw .txt/.html chapter ingestion; from-scratch EPUB3 builder; pinyin gate |
| Unchanged | Three-layer separation, per-novel file set, interleaved translate→edit ordering, assembler/updater/image-localizer roles, EPUB verification gates, no-title-heading rule, past-tense rule, honorifics, JP name order, furigana `漢字[かな]`, no-macron romanization |

## 3. Architecture — shared core + runtime packs

```
JP Translation Initialisation/
  CLAUDE.md                  # entry point for Claude Code → core/ + .claude/
  novel.config.md            # per-novel knobs (stays at root — user-edited)
  glossary.md                # per-novel (gains Aliases/Banned column)
  character-reference.md     # per-novel
  character-voices.md        # per-novel (register ceiling + kill-list now REQUIRED)
  style-guide.md             # per-novel (NEW — style guide + running plot summary)
  translation-progress.md    # per-novel

  core/                      # MODEL-AGNOSTIC single source of truth
    pipeline.md              # canonical pipeline spec: stages, ordering, gates,
                             #   file contracts, dependency graph, done-criteria
    guides/                  # translation-guide, footnote-guide, voice-building-guide,
                             #   quality-checklist, epub-build-spec, qa-audit-guide (NEW)
    scripts/                 # split_ebook.py, normalize_romaji.py, build_epub.py,
                             #   verify_epub.py, derive_build_config.py (NEW),
                             #   check_consistency.py (NEW), kindleunpack/
    schemas/                 # documented schemas for novel.config.md + per-novel files

  .claude/                   # CLAUDE CODE RUNTIME (Opus 4.8-tuned, thin)
    agents/                  # translator, editor, qa-auditor (NEW), assembler,
                             #   updater, image-localizer, epub-builder
    skills/                  # setup-novel, translate-chapter, build-epub

  AGENTS.md                  # CODEX CLI RUNTIME entry (GPT-5.5-tuned, thin) — MUST
                             #   sit at repo root or Codex never discovers it;
                             #   lean (<32 KiB incl. chain) → points into core/
  .codex/agents/             # Codex per-stage custom agents (TOML): translator,
                             #   editor, qa-auditor, assembler, updater,
                             #   image-localizer, epub-builder — per-agent model,
                             #   model_reasoning_effort, sandbox_mode
  .agents/skills/            # Codex skills mirroring the three slash commands
                             #   (official discovery path; custom prompts are
                             #   deprecated). Orchestration order lives in the
                             #   skill body — Codex has no task board.

  Source/  English/  Editing/  docs/
```

**Single-source rule:** conventions, gates, file contracts, and pipeline ordering live only in `core/`. Runtime packs contain role framing, tool wiring, orchestration mechanics, and model-appropriate phrasing — and *reference* core files by path. A guide fix lands once.

`scripts/` moves under `core/scripts/`; a root-level `scripts/` note (or symlink) is not kept — all documented invocations use `core/scripts/…`.

## 4. Orchestration (Claude Code runtime)

- No `TeamCreate`/`TeamDelete` anywhere. Skills act as **lead of the session's implicit team**: spawn named teammates with the Agent tool, message them via SendMessage, coordinate through the shared task board.
- Dependency graph unchanged: `Edit Pi` blockedBy `Translate Pi`; `Translate P(i+1)` blockedBy `Edit Pi`; `Assemble` blockedBy all edits; **`QA-Audit` blockedBy `Assemble` (parted) or `Edit` (whole)**; `Update` blockedBy `QA-Audit` pass; **chapter is filed as done only after `check_consistency.py --all` passes post-Update** (the updater may revise the glossary, which can invalidate already-passed chapters — the `--all` run is what makes QA's glossary check non-stale).
- Verify-on-disk before marking any task complete stays, and the QA stage now verifies *content*, not just existence.
- **Teammate lifetime = one chapter.** Translator/editor are reused across a chapter's parts (their hot context — this chapter's source and edited parts — is exactly the continuity the interleave needs), then retired; the next chapter gets fresh spawns. Rationale: a translator carrying prior chapters' full source + drafts accumulates unbounded dead context (rot degrades register/kill-list adherence), and its stale in-context term choices can fight an updater-revised glossary — the exact cross-chapter drift this overhaul targets. Cross-chapter continuity is file-borne only (glossary, `character-voices.md`, `style-guide.md`, prior edited chapters), which fresh spawns read current. This also matches Codex's forced-ephemeral agents, keeping the two runtimes behaviorally identical.
- Front-load complete task specs when dispatching (Opus 4.8 token-efficiency guidance).

**Codex runtime:** same per-stage agent model as the Claude runtime. Each role is a **custom agent** (TOML in `.codex/agents/`: `name`, `description`, `developer_instructions`, plus per-agent `model` / `model_reasoning_effort` / `sandbox_mode` — e.g. editor read-heavy stages `read-only` where possible). The orchestrating skill spawns them in sequenced rounds: translate Pi → await → edit Pi → await → translate P(i+1); Codex subagents are ephemeral (spawn→wait→collect→close, no persistent teammates, no task board), so the dependency graph lives as explicit ordering in the skill body with "do not proceed to part i+1 until part i's edit is verified on disk" language. The **qa-auditor always runs as its own subagent** — isolated context is the point. Limits respected: subagent depth 1 (agents can't nest), ≤6 concurrent threads; gates remain shell commands run by the orchestrator.

## 5. Quality machinery

### 5.1 Translator (unchanged role, sharpened prompt)
Raw draft; register lock; kill-list obedience; reads edited prior parts for continuity; now also reads `style-guide.md`. Prompt rewritten per runtime style (see §7). No "translate naturally" adjectives — naturalness is the polish pass's job (research: task framing works, adjectives don't).

### 5.2 Editor — two sub-passes, one teammate
1. **Accuracy pass** (as today): line-by-line against raw JP in ~150–200-line chunks; targeted Edits only; every change logged with before→after + reason.
2. **Polish pass (NEW)**: read the *English first*, chunk by chunk, and polish it to read as native-authored prose — resolving translationese artifacts, awkward calques, unnatural rhythm. Hard cap: the register ceiling and kill-list in `character-voices.md`; sentence length/energy must track the JP (choppy JP stays choppy) — so **every span the polish pass changes is re-checked against its JP line before the change is finalized** (English-first reading, source-verified writes; an English-only pass cannot enforce a JP-flow constraint). Polish changes are logged in the same edit log, tagged `[polish]`.

The old contradictory instruction ("merge choppy sentences into smooth English" vs "keep narration lean") is deleted. Replacement rule: *match the JP's flow — smooth what the JP smooths, keep abrupt what the JP keeps abrupt.* One polish iteration only (iterative refinement drifts from source).

### 5.3 QA auditor (NEW agent + `core/guides/qa-audit-guide.md`)
Independent teammate; runs after assembly (or whole-chapter edit). Never edits — verdict only.
- **Sample:** ~10–15% of source lines, drawn **independently of the edit log** — a random floor across the whole chapter plus over-sampling of dialogue and high-emotion passages (documented locus of register elevation and emotional flattening). Edit-log-untouched regions get extra weight as a rubber-stamp signal, but capped so the audit stays a spot audit; the random floor means an editor cannot evade the audit by making superficial edits everywhere, and the log is treated as a signal, never as trusted evidence.
- **Checks per sampled line:** accuracy vs raw JP; register vs ceiling; **character-voice conformance vs the speaker's profile in `character-voices.md`** (the deterministic gate cannot see voice drift — this is where it's caught); glossary compliance; three JP→EN failure classes — zero-pronoun/dropped-subject recovery, keigo→register mapping, over/under-compression (EN markedly longer or shorter than the JP warrants).
- **Output:** MQM-style findings — error span, category (accuracy / fluency / terminology / style / voice), severity (minor / major / critical) — written to `Editing/Volume N/Chapter <N> - QA Report.md`.
- **Gate:** any critical, or >N major findings (threshold in `novel.config.md`, default 3) → FAIL → chapter returns to the editor with the report; re-audit after fixes. No BLEU or n-gram metrics anywhere.

### 5.4 `check_consistency.py` (NEW, deterministic)
- Glossary format gains a column: `JP | EN | Aliases/Banned | Gender/Context`. Aliases/Banned holds pipe-free, comma-separated *forbidden* EN renderings (old spellings, rejected variants).
- Per-chapter mode: scan a final chapter for banned renderings, name-spelling drift (fuzzy match against glossary EN names), dropped honorifics on glossary names that carry them, and macron characters (folds in the romaji surface).
- `--all` mode: scan every filed chapter — **mandatory after every updater run** (and any manual glossary revision) so changes back-propagate; failures list file + line.
- Exit non-zero on violations; runs as a gate beside `normalize_romaji.py --check` in `/translate-chapter`, and as a build gate in `/build-epub`. Both gates take the chapter file(s) under `English/Volume N/` as their explicit file arguments (`normalize_romaji.py` requires paths; none of this is inferred).
- **Known limits (by design):** the deterministic gate catches string-detectable drift only — banned renderings, name spelling, dropped honorifics, macrons. Glossary omissions rendered as plausible synonyms, wrong-referent-correct-spelling errors, and voice/register drift are *not* string-detectable; those are the QA auditor's checks (§5.3). The two gates are complements, not alternatives.

### 5.5 Setup hardening
`/setup-novel` **fails** unless it has authored, in `character-voices.md`: a narrator register ceiling, a per-novel elevation kill-list (seeded from `core/guides/translation-guide.md`'s generic list + novel-specific entries), and per-character voice profiles for the leads. It also seeds `style-guide.md` (tone, audience, conventions) — the updater appends a 2–3 sentence plot/state summary per chapter thereafter.

## 6. Script repairs & additions

| Script | Change |
|-|-|
| `derive_build_config.py` (NEW) | `novel.config.md` + volume number → the JSON `build_epub.py` requires. Kills the fictional `--volume N --config novel.config.md` invocation; skills/agents document the real two-step: derive → build. |
| `check_consistency.py` (NEW) | §5.4. |
| `build_epub.py`, `verify_epub.py`, `split_ebook.py`, `normalize_romaji.py` | Unchanged behavior; docs corrected; paths under `core/scripts/`. |
| Docs | All Windows-flavored examples (`G:\…`, backslashes) made platform-neutral. Windows-illegal-char filename rule kept (output may be consumed on Windows). |

## 7. Runtime pack styles

### 7.1 `.claude/` — Opus 4.8 rules applied
- Every cross-item rule states its scope explicitly ("for every part", "every glossary term") — 4.8 does not generalize scope from examples.
- Positive target examples over "never" lists; kill-list rendered as wrong→right pairs.
- Skills explicitly authorize teammate fan-out and parallel dispatch (4.8 under-spawns by default).
- "CRITICAL: you MUST" phrasing softened to plain "Do X when Y" (over-trigger regression).
- Task dispatches place raw JP source at the top of the teammate prompt, instructions/glossary after (long-context placement).
- Rules carry their *why* (model generalizes from rationale). No interim progress-update scaffolding.
- Agent `model:` frontmatter — translator/editor/qa-auditor: `opus`; assembler/updater/image-localizer/epub-builder: `sonnet`.

### 7.2 `codex/` — GPT-5.5 rules applied
- Outcome-oriented, minimal prompts: define what a good chapter/edit/audit looks like + hard constraints; leave the path to the model. No step-by-step hand-holding carried over from the Claude pack.
- `AGENTS.md` lean and under the 32 KiB chain cap: non-negotiables (register lock, past tense, honorifics, glossary compliance, gates) + pointers into `core/`.
- Pipeline stages as per-role **custom agents** (`.codex/agents/*.toml`) orchestrated by repo-shared **skills** under `.agents/skills/` (the officially documented discovery path). Custom prompts are deprecated — not used. Recommended per-agent settings: translator/editor/qa-auditor `model_reasoning_effort = "high"`, others `"medium"`; qa-auditor `sandbox_mode = "read-only"`.
- Persistence + scope-guard language per GPT-5.5 guide ("keep going until truly done"; "do not expand the task; call out new work as optional"); explicit sequential gating for the per-part interleave; recommended `reasoning_effort`: high for translate/edit/audit, medium elsewhere.
- Contradiction-audited: discrete rule clusters in separate tagged blocks.

## 8. CN webnovel sibling — `CN Translation Initialisation/`

Same architecture (`core/` + `.claude/` + `codex/`), same agents/skills/gates/quality machinery. Differences only:

| Area | JP harness | CN harness |
|-|-|-|
| Ingestion | `split_ebook.py` (epub/azw3) | `ingest_chapters.py` (NEW): folder of scraped `.txt`/`.html` → `Source/Volume N/NNNN <title>.md`; volume boundaries from config (chapters-per-volume or explicit ranges); HTML stripped to text; encoding detection (UTF-8/GB18030/Big5). **Scraped-text cleanup is part of ingestion**: strip site boilerplate/ad blocks (configurable pattern list), drop duplicated in-body chapter titles, normalize paragraphing and full-width punctuation, simplified/traditional normalization knob in config, separate author's-notes blocks from prose. Emits a per-chapter **ingestion report** (what was stripped/normalized, anomalies flagged); `/setup-novel` surfaces the report for user review before translation starts — dirty source poisons every downstream stage |
| EPUB build | Source-shell-based `build_epub.py` | `build_epub_scratch.py` (NEW): from-scratch EPUB3 (no source shell — webnovels have none; MTF-U pattern): nav/OPF/CSS generated, LTR, popup footnotes, cover optional |
| Romanization gate | `normalize_romaji.py` (no macrons) | `normalize_pinyin.py` (NEW): config knob `pinyin: toneless` (default) or `diacritics`; enforces one convention |
| Language guides | JP guides | CN guides: **pinyin for names only** — all other terms are translated into English; pinyin is the fallback *only* when the literal English rendering doesn't make sense (untranslatable cultural/genre term), footnoted on first use. Address terms (师兄/道友/哥哥-class) follow the same rule: translate by default ("senior brother"), pinyin fallback + footnote when translation misleads. Also: CN name order (family first); chengyu/idiom policy (render meaning, footnote only when culturally load-bearing); cultivation/genre term conventions. JP furigana and honorific-suffix machinery is dropped, but **CN address/status terms get equivalent tracking**: per-character address-form tables (师兄/前辈/公子/道友/kinship-as-address, sect titles) in `character-reference.md`, chosen EN renderings locked in the glossary, and address-shift moments (e.g. 你→您, name→title) flagged the same way JP address-form shifts are |
| Voice axes | JP pronoun/keigo axes | CN axes: address terms, formality (您/你), classical vs colloquial diction, verbal tics |
| QA failure classes | zero-pronoun, keigo→register, compression | dropped-subject recovery, address-term/register mapping, chengyu mistranslation, compression |
| Cadence | Per-chapter command | `/translate-chapter` accepts a chapter **range** (e.g. `12-20`): sequential per-chapter runs with continuity carry-over; per-chapter gates still apply individually |
| Furigana rule | `漢字[かな]` preserved | N/A (no ruby in webnovel sources) |

Footnotes default-on in both. Register lock, past tense, no-title-heading, glossary/consistency gates, QA audit: identical.

## 9. Migration plan (JP folder)

0. Repo hygiene: add `.gitignore` (`*Zone.Identifier`, build artifacts); delete existing `*:Zone.Identifier` sidecar files so they don't propagate into the CN copy.
1. Create `core/`; move `guides/`, `scripts/` into it; add `pipeline.md`, `schemas/`, new guides/scripts. **Sweep every reference to the old `scripts/` path** (skills, agents, guides, `novel.config.md` prose, CLAUDE.md) in the same change — no stale invocations.
2. Rewrite `.claude/agents/*` + `.claude/skills/*` (orchestration + Opus 4.8 style + QA auditor).
3. Add the Codex pack: root `AGENTS.md` + `.codex/agents/*.toml` + `.agents/skills/`.
4. Update `CLAUDE.md` (lean index), glossary schema (Aliases/Banned column), add `style-guide.md` stub.
5. Copy the finished JP folder → strip JP-specifics → author CN substitutions → `CN Translation Initialisation`.

Existing per-novel stubs stay at root untouched (they're empty in the template).

## 10. Non-goals

- Translating any actual novel (template only; live projects copy from it).
- Automated image rendering (specs remain a manual render step).
- Scraping webnovel sites (CN ingestion starts from already-downloaded files).
- Any BLEU/n-gram quality metric.
- Other runtimes beyond Claude Code and Codex CLI.

## 11. Research basis (for the record)

- Anthropic, *Prompting Claude Opus 4.8* + *Claude prompting best practices* (platform.claude.com) — §7.1 rules.
- OpenAI, *GPT-5.5 prompting guide*, *Codex prompting guide*, *AGENTS.md guide*, *Codex sandboxing* (developers.openai.com) — §7.2 rules.
- *Lost in Literalism* (arXiv 2503.04369) — polish-pass framing; 43%→25% translationese; "natural" adjectives ineffective. → §5.2.
- TransAgents (arXiv 2405.11804) — persistent style guide + running summary; d-BLEU anti-correlates with human preference. → `style-guide.md`, no-BLEU rule.
- GEMBA-MQM v2 / Rubric-MQM — MQM error-span judging. → §5.3.
- JP-TL-Bench (arXiv 2601.00223) — JP→EN failure classes (zero-pronoun, keigo, compression). → §5.3.
- Emotion-profiling study (arXiv 2606.10113) — dialogue/high-emotion over-sampling. → §5.3.
- WMT25 terminology task + industry consensus — deterministic post-hoc glossary gate. → §5.4.
- Iterative refinement ceiling (arXiv 2306.03856) — single polish iteration. → §5.2.
