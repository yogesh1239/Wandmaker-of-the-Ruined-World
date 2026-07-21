# Harness Overhaul (JP) + CN Sibling Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rebuild the JP light-novel translation harness as a model-agnostic `core/` + Opus 4.8-tuned Claude Code runtime + GPT-5.5-tuned Codex runtime with new quality gates, then derive the Chinese-webnovel sibling harness.

**Architecture:** Single-source-of-truth `core/` (guides, scripts, pipeline spec, schemas); thin runtime packs that reference core by path; deterministic script gates + an independent QA-audit agent stage; CN sibling produced by copy-and-substitute per the spec's §8 table.

**Tech Stack:** Markdown (agents/skills/guides), Python 3 stdlib (scripts; Pillow only where already required), Codex TOML agents.

**Spec:** `docs/superpowers/specs/2026-07-03-harness-overhaul-and-cn-sibling-design.md` — every task cites its section.
**Research digests (implementers MUST read the ones their task names):**
- `docs/superpowers/research/2026-07-03-opus-4-8-prompting-rules.md` (RD-OPUS)
- `docs/superpowers/research/2026-07-03-gpt55-codex-rules.md` (RD-GPT)
- `docs/superpowers/research/2026-07-03-llm-literary-translation-findings.md` (RD-LIT)

## Global Constraints

- Past-tense narration; honorifics retained; JP name order; furigana `漢字[かな]`; no-macron romanization (vowel-doubling ō→ou etc.); glossary exact matches mandatory; no in-file title heading (Windows-illegal-char exception: `< > : " / \ | ? *` → sanitized filename + in-file `#` heading). These are unchanged spec invariants (spec §2).
- No fact may exist in two places: conventions/gates/contracts live ONLY in `core/`; runtime packs reference them by relative path (spec §3).
- No BLEU/n-gram metric anywhere (spec §10).
- One polish iteration only (spec §5.2).
- Scripts: Python 3 stdlib only (Pillow stays only in `build_epub.py`/`verify_epub.py` where it already exists). Each new script gets a small `test_*.py` beside it, runnable with `python -m pytest` or plain `python test_x.py`.
- All paths platform-neutral (forward slashes, no drive letters) (spec §6).
- Commit after every task (message prefix `overhaul:` for Phase A, `cn:` for Phase B).
- Suggested implementation models: **opus** for agent/skill/guide authoring and `build_epub_scratch.py`; **sonnet** for mechanical/move/TOML/stub/test-only tasks. Marked per task.

---

## Phase A — JP harness overhaul

### Task A1: Repo hygiene (sonnet) — spec §9 step 0

**Files:**
- Create: `.gitignore`
- Delete: every `*:Zone.Identifier` file in the repo

**Interfaces:** Produces a clean tree later tasks copy from.

- [ ] **Step 1:** Write `.gitignore`:

```gitignore
*Zone.Identifier
__pycache__/
*.pyc
.pytest_cache/
*.epub.tmp
```

- [ ] **Step 2:** Delete sidecars: `find . -name '*Zone.Identifier' -delete`
- [ ] **Step 3:** Verify: `find . -name '*Zone.Identifier' | wc -l` → `0`
- [ ] **Step 4:** Commit: `git add -A && git commit -m "overhaul: repo hygiene — gitignore + purge Zone.Identifier sidecars"`

### Task A2: Create `core/`, move guides+scripts, sweep old paths (sonnet) — spec §3, §9 step 1

**Files:**
- Move: `guides/` → `core/guides/`, `scripts/` → `core/scripts/` (use `git mv`)
- Modify: every file containing `scripts/` or `guides/` path references: `CLAUDE.md`, `novel.config.md`, `.claude/agents/*.md`, `.claude/skills/*/SKILL.md`, `core/guides/*.md` (post-move self-references)

**Interfaces:** Produces the `core/guides/…` and `core/scripts/…` paths all later tasks use. Old top-level `guides/`, `scripts/` must not exist afterward.

- [ ] **Step 1:** `git mv guides core/guides && git mv scripts core/scripts`
- [ ] **Step 2:** Sweep references: `grep -rn --include='*.md' -E '(^|[^/a-z])(scripts|guides)/' . | grep -v core/ | grep -v docs/` and rewrite each hit to `core/scripts/` / `core/guides/`. Do NOT edit `docs/` (historical specs stay as written).
- [ ] **Step 3:** Verify sweep clean: the grep from Step 2 returns nothing.
- [ ] **Step 4:** Verify scripts still run: `python core/scripts/normalize_romaji.py --check core/guides/translation-guide.md` → exits 0 (guide contains no macrons) or lists real macrons only.
- [ ] **Step 5:** Commit.

### Task A3: `core/schemas/` — file contracts (opus) — spec §3, §5.4, §5.5

**Files:**
- Create: `core/schemas/novel-config-schema.md`, `core/schemas/glossary-schema.md`, `core/schemas/character-voices-schema.md`, `core/schemas/style-guide-schema.md`, `core/schemas/edit-log-schema.md`, `core/schemas/qa-report-schema.md`

**Interfaces:** Produces the authoritative column/section definitions that scripts (A4, A5) parse and agents (A7) write. Exact contracts:

- `glossary-schema.md`: table `| JP | EN | Aliases/Banned | Gender/Context |`. Aliases/Banned = comma-separated forbidden EN renderings, no pipes, may be empty. EN column is the ONLY permitted rendering.
- `character-voices-schema.md`: required sections `## Narrator` (with `**Register ceiling:**` line + `### Elevation kill-list` table `| Elevated (wrong) | Correct |`) and `## <Character Name>` blocks (pronoun, register, address forms, tics, 2+ sample lines). Setup fails without Narrator ceiling + ≥5 kill-list rows (spec §5.5).
- `style-guide-schema.md`: `## Style Guide` (tone, audience, conventions — authored at setup) + `## Running Summary` (per-chapter `### Chapter N` 2–3 sentence entries, appended by updater).
- `qa-report-schema.md`: header block (chapter, sample %, lines sampled), findings table `| Line | Category | Severity | JP | EN | Problem |` with Category ∈ accuracy/fluency/terminology/style/voice and Severity ∈ minor/major/critical, then `## Verdict` PASS/FAIL with counts. Fail rule: any critical OR > qa_major_threshold majors (default 3, knob in novel.config.md).
- `edit-log-schema.md`: existing format + `[polish]` tag on polish-pass entries.
- `novel-config-schema.md`: documents every knob incl. NEW `qa_major_threshold` (default 3) and existing ones (register lock, part-split threshold, chapter-title map, per-volume source map, EPUB metadata, romanization convention). States that `derive_build_config.py` (A5) is the consumer for build fields.

- [ ] **Step 1:** Author all six schema files per the contracts above (each ≤ ~60 lines; include one filled example row/section per file).
- [ ] **Step 2:** Add `qa_major_threshold: 3` knob + Aliases/Banned column mention to root `novel.config.md` template and root `glossary.md` stub header row; create root `style-guide.md` stub matching its schema (empty sections).
- [ ] **Step 3:** Verify: root `glossary.md` header row has 4 columns; `grep -l 'qa_major_threshold' novel.config.md` hits.
- [ ] **Step 4:** Commit.

### Task A4: `check_consistency.py` + tests (sonnet) — spec §5.4

**Files:**
- Create: `core/scripts/check_consistency.py`, `core/scripts/test_check_consistency.py`

**Interfaces:**
- CLI: `python core/scripts/check_consistency.py --glossary glossary.md <chapter.md ...>` or `--glossary glossary.md --all <english-dir>` (recurses `*.md`).
- Exit 0 clean; exit 1 with `file:line: <violation>` lines on stdout.
- Checks: (1) banned-alias hit (case-insensitive whole word, from Aliases/Banned column); (2) name-drift: capitalized token with difflib ratio ≥ 0.86 to a glossary EN name but not equal to it (and not itself another glossary term/alias) → flag; (3) honorific mismatch: for glossary EN of form `Base-honorific` (honorifics: san,kun,chan,sama,sensei,senpai,dono), flag `Base-<other-honorific>` occurrences; (4) macron chars `āēīōūĀĒĪŌŪ`.
- Skips ` ## Translator Notes` sections for CJK-adjacent checks? No — all checks apply whole-file EXCEPT banned-alias/name-drift also apply in notes. Keep simple: all checks whole file.

- [ ] **Step 1:** Write failing tests:

```python
# core/scripts/test_check_consistency.py
import subprocess, sys, tempfile, os, textwrap
SCRIPT = os.path.join(os.path.dirname(__file__), "check_consistency.py")

GLOSSARY = textwrap.dedent("""\
    | JP | EN | Aliases/Banned | Gender/Context |
    |-|-|-|-|
    | 西部戦線 | Western Front | Western Theatre, West Front | place |
    | 田中 | Tanaka-san | | male, teacher |
    | 大鳥 | Ootori | Otori, Ōtori | female |
""")

def run(chapter_text, extra_args=()):
    d = tempfile.mkdtemp()
    g = os.path.join(d, "glossary.md"); c = os.path.join(d, "ch.md")
    open(g, "w", encoding="utf-8").write(GLOSSARY)
    open(c, "w", encoding="utf-8").write(chapter_text)
    p = subprocess.run([sys.executable, SCRIPT, "--glossary", g, c, *extra_args],
                       capture_output=True, text=True)
    return p.returncode, p.stdout

def test_clean_passes():
    rc, out = run("They marched to the Western Front. Tanaka-san smiled. Ootori waited.")
    assert rc == 0, out

def test_banned_alias_fails():
    rc, out = run("They reached the Western Theatre at dawn.")
    assert rc == 1 and "Western Theatre" in out

def test_name_drift_fails():
    rc, out = run("Ootorri turned away.")  # close-but-wrong spelling
    assert rc == 1 and "Ootorri" in out

def test_honorific_mismatch_fails():
    rc, out = run("Tanaka-kun raised a hand.")
    assert rc == 1 and "Tanaka-kun" in out

def test_macron_fails():
    rc, out = run("Ōtori is banned anyway, but ō alone must flag too.")
    assert rc == 1 and "macron" in out.lower()

if __name__ == "__main__":
    for f in [v for k, v in list(globals().items()) if k.startswith("test_")]:
        f()
    print("ok")
```

- [ ] **Step 2:** Run: `python core/scripts/test_check_consistency.py` → fails (script missing).
- [ ] **Step 3:** Implement `check_consistency.py` (argparse; glossary table parser tolerant of alignment rows; `re` word-boundary search for aliases/honorifics/macrons; `difflib.SequenceMatcher` for drift over `[A-Z][a-z]+` tokens; `--all` walks dir with `os.walk`). `# ponytail: difflib ratio 0.86 heuristic — tune threshold if false positives appear in production`.
- [ ] **Step 4:** Run tests → all pass.
- [ ] **Step 5:** Commit.

### Task A5: `derive_build_config.py` + tests (sonnet) — spec §6

**Files:**
- Create: `core/scripts/derive_build_config.py`, `core/scripts/test_derive_build_config.py`

**Interfaces:**
- CLI: `python core/scripts/derive_build_config.py novel.config.md --volume 1 [--out <path>.json]` (default out: `Editing/Volume 1/build_config.json`).
- Reads the config sections defined in `core/schemas/novel-config-schema.md` (volume→source-epub map, chapter-title map, EPUB metadata block, English dir) and the chapter files present under `English/Volume N/`.
- Emits JSON in exactly the schema `build_epub.py --config` documents in its docstring: `source_epub`, `chapters_dir`, `out_epub`, `metadata{title,language,identifier,creators}`, `chapters[]{id,md,title}` ordered by the title map. Chapters listed in the map but missing on disk → warning to stderr, excluded; exit 2 if ZERO chapters found.

- [ ] **Step 1:** Write failing tests: build a temp dir with a minimal `novel.config.md` (volume map for Volume 1 → `source.epub`, two title-map rows, metadata block per schema), touch `English/Volume 1/Chapter 1 - First.md` only (second chapter missing). Assert: JSON has 1 chapter with `title == "First"`, `source_epub` endswith `source.epub`, warning on stderr mentions the missing chapter, exit 0; empty English dir → exit 2.
- [ ] **Step 2:** Run tests → fail.
- [ ] **Step 3:** Implement (stdlib: `re` section parsing keyed off the schema's headings, `json.dump`).
- [ ] **Step 4:** Tests pass.
- [ ] **Step 5:** Update `core/guides/epub-build-spec.md` build-invocation section to the real two-step:

```bash
python core/scripts/derive_build_config.py novel.config.md --volume N
python core/scripts/build_epub.py --config "Editing/Volume N/build_config.json"
python core/scripts/verify_epub.py --config "Editing/Volume N/build_config.json"
```

- [ ] **Step 6:** Commit.

### Task A6: `core/pipeline.md` + guide updates (opus; read RD-LIT) — spec §3, §4, §5, §6

**Files:**
- Create: `core/pipeline.md`, `core/guides/qa-audit-guide.md`
- Modify: `core/guides/translation-guide.md`, `core/guides/quality-checklist.md`, `core/guides/voice-building-guide.md`

**Interfaces:** `core/pipeline.md` is the canonical stage/gate/contract spec BOTH runtimes cite instead of restating. Contents (all copied/adapted from spec §4–§6, not invented): stage list with dependency graph incl. QA-Audit placement and post-Update `check_consistency.py --all`; teammate-lifetime rule (one chapter; reuse across parts only — with the context-rot + stale-glossary rationale); file contracts (draft paths, edit log, QA report, final chapter naming incl. Windows-illegal exception); gate commands with explicit file arguments; done-criteria per stage; PRE-GLOSS step; parted-vs-whole threshold rule.

`qa-audit-guide.md` (agnostic method, JP specifics marked): sampling rule (10–15% random floor independent of edit log + dialogue/high-emotion over-sample + capped untouched-region weighting; log = signal, never evidence); per-line checks (accuracy vs source, register vs ceiling, voice-profile conformance, glossary compliance, failure classes: JP = zero-pronoun recovery / keigo→register / compression); MQM categories × severities; report format per `core/schemas/qa-report-schema.md`; fail rule (any critical OR > qa_major_threshold majors); coverage prompting note (report everything with confidence+severity — per RD-OPUS rule 9); re-audit after editor fixes.

Guide edits:
- `translation-guide.md`: kill-list section reworked to wrong→right positive-pair table (keep existing pairs, add scope line "applies to every sentence of every part of every chapter"); ADD explicit note that naturalness is the polish pass's job — the translate stage optimizes accuracy + register fidelity (RD-LIT: adjectives don't work, task framing does); platform-neutral path examples.
- `quality-checklist.md`: add gates — QA report PASS exists; `check_consistency.py` clean; `check_consistency.py --all` clean post-update; style-guide Running Summary entry appended.
- `voice-building-guide.md`: Narrator register ceiling + ≥5-row kill-list now REQUIRED outputs (schema A3); add "editor may not smooth choppy JP — match the source's flow" as the naturalness rule replacing any merge-choppy language.

- [ ] **Step 1:** Author `core/pipeline.md` (~150 lines) per the contract above.
- [ ] **Step 2:** Author `core/guides/qa-audit-guide.md` (~100 lines).
- [ ] **Step 3:** Apply the three guide edits.
- [ ] **Step 4:** Verify: `grep -n 'merge.*choppy\|smooth.*out' core/guides/*.md` → no instruction telling editors to smooth choppy source; `grep -c 'check_consistency' core/pipeline.md core/guides/quality-checklist.md` → ≥1 each.
- [ ] **Step 5:** Commit.

### Task A7: Rewrite `.claude/agents/` (opus; read RD-OPUS + RD-LIT) — spec §4, §5, §7.1

**Files:**
- Modify: `.claude/agents/translator.md`, `editor.md`, `assembler.md`, `updater.md`, `image-localizer.md`, `epub-builder.md`
- Create: `.claude/agents/qa-auditor.md`

**Interfaces:** Frontmatter `model:` — translator/editor/qa-auditor `opus`; others `sonnet`. Tools unchanged for existing agents; qa-auditor gets `Read, Grep, Glob, Bash, TaskList, TaskUpdate, SendMessage, Write` (Write ONLY for the QA report file). Every agent: no TeamCreate/TeamDelete references; cites `core/pipeline.md` + relevant `core/guides/` + `core/schemas/` paths instead of restating rules.

Authoring rules (RD-OPUS): explicit scope on all cross-item rules; positive examples; plain "Do X when Y" (no "CRITICAL: MUST"); rationale attached; source-at-top dispatch note; no progress-update scaffolding.

Per-agent content deltas (beyond restructuring):
- `translator.md`: reads `style-guide.md` too; accuracy+register fidelity focus, naturalness deferred to polish (state why, per RD-LIT); reads edited prior parts — "for every part after the first."
- `editor.md`: two sub-passes — Pass 1 accuracy line-by-line vs raw JP in ~150–200-line chunks, every chunk, in order; Pass 2 polish, English-first reading, "make each chunk read as native-authored prose," every changed span re-checked against its JP line before finalizing, register ceiling + kill-list as hard cap, choppy JP stays choppy, ONE iteration, entries tagged `[polish]`.
- `qa-auditor.md` (new): implements `core/guides/qa-audit-guide.md`; never edits chapter files; writes report per schema; coverage prompting ("report every issue found, with confidence and severity").
- `updater.md`: additionally appends the chapter's 2–3 sentence Running Summary entry to `style-guide.md`; after ANY glossary change, runs `python core/scripts/check_consistency.py --glossary glossary.md --all English/` and reports violations to the lead instead of fixing silently.
- `assembler.md`, `image-localizer.md`, `epub-builder.md`: path sweep to `core/`, phrasing per RD-OPUS, epub-builder switched to the A5 two-step invocation; otherwise role-identical.

- [ ] **Step 1:** Rewrite the six existing agent files.
- [ ] **Step 2:** Author `qa-auditor.md`.
- [ ] **Step 3:** Verify: `grep -rn 'TeamCreate\|TeamDelete' .claude/` → nothing; `grep -l 'core/pipeline.md' .claude/agents/*.md` → all 7; `grep -n 'CRITICAL' .claude/agents/*.md` → nothing.
- [ ] **Step 4:** Commit.

### Task A8: Rewrite `.claude/skills/` (opus; read RD-OPUS) — spec §4, §5.5, §7.1

**Files:**
- Modify: `.claude/skills/setup-novel/SKILL.md`, `.claude/skills/translate-chapter/SKILL.md`, `.claude/skills/build-epub/SKILL.md`

**Interfaces:** Skills are leads over the session's implicit team: spawn named teammates via the Agent tool (subagent_type = the `.claude/agents/` name), coordinate via TaskCreate/TaskList/TaskUpdate + SendMessage. Explicit fan-out authorization sentence in each skill (RD-OPUS rule 4).

- `setup-novel`: adds style-guide seeding; HARD-FAIL rule — do not report success unless `character-voices.md` contains a Narrator `**Register ceiling:**` line and an Elevation kill-list table with ≥5 rows (verify by grep before finishing); TOC translation, register lock, config fill as today.
- `translate-chapter`: dependency graph incl. `QA-Audit` (blockedBy Assemble/Edit) and `Update` (blockedBy QA pass); chapter filed done only after `normalize_romaji.py --check <chapter files>`, `check_consistency.py --glossary glossary.md <chapter files>`, AND post-Update `check_consistency.py --all English/` all exit 0; teammate lifetime = one chapter (spawn fresh translator/editor per chapter, reuse across parts via SendMessage); QA FAIL loop → editor fixes findings → re-audit; dispatch prompts put raw JP at top.
- `build-epub`: two-step derive→build→verify invocation (A5); `check_consistency.py --all` added as build gate; image-localize → user render pause unchanged.

- [ ] **Step 1:** Rewrite the three SKILL.md files.
- [ ] **Step 2:** Verify: `grep -rn 'TeamCreate\|TeamDelete\|--volume.*config novel.config.md' .claude/skills/` → nothing; `grep -l 'qa-auditor' .claude/skills/translate-chapter/SKILL.md` → hit; `grep -l 'derive_build_config' .claude/skills/build-epub/SKILL.md` → hit.
- [ ] **Step 3:** Commit.

### Task A9: Rewrite root `CLAUDE.md` (opus; read RD-OPUS) — spec §3

**Files:**
- Modify: `CLAUDE.md`

**Interfaces:** Lean index: layout table (core / runtimes / per-novel files incl. `style-guide.md`), pipeline one-liners pointing at `core/pipeline.md`, critical-rules list (add: QA gate, consistency gates, teammate lifetime, polish-pass cap), copy-to-new-novel procedure (platform-neutral), Codex runtime pointer ("Codex CLI users: root `AGENTS.md` is the entry point"). Remove: team-based orchestration section, `G:\` paths, old `scripts/` references, old design-doc link → new spec link.

- [ ] **Step 1:** Rewrite.
- [ ] **Step 2:** Verify: `grep -n 'TeamCreate\|G:\\\\\|[^e]/scripts/' CLAUDE.md` → nothing.
- [ ] **Step 3:** Commit.

### Task A10: Codex runtime pack (opus; read RD-GPT) — spec §3, §4, §7.2

**Files:**
- Create: `AGENTS.md` (repo root)
- Create: `.codex/agents/translator.toml`, `editor.toml`, `qa-auditor.toml`, `assembler.toml`, `updater.toml`, `image-localizer.toml`, `epub-builder.toml`
- Create: `.agents/skills/setup-novel/SKILL.md`, `.agents/skills/translate-chapter/SKILL.md`, `.agents/skills/build-epub/SKILL.md`

**Interfaces:**
- `AGENTS.md` ≤ 6 KB: identity ("JP light-novel translation harness"), non-negotiables list (past tense, register lock read from novel.config.md, honorifics, JP name order, glossary exact match + banned-alias rule, furigana notation, no-macron, no-title-heading), pointers: `core/pipeline.md`, `core/guides/`, `core/schemas/`, gate commands verbatim, "dispatch per-stage agents defined in .codex/agents/ by name; qa-auditor always as its own subagent."
- TOML per agent (RD-GPT rule 12): `name`, `description`, `developer_instructions` (outcome-oriented ≤ ~40 lines, pointing at the same core files as the Claude twin — no fact duplication), `model_reasoning_effort` = "high" (translator/editor/qa-auditor) / "medium" (rest), `sandbox_mode` = "read-only" for qa-auditor, "workspace-write" others. No `model` field — inherit session model.
- Codex skills: frontmatter `name` + `description`; body = outcome contract + ordered stage prose with explicit "do not proceed to part i+1 until part i's edit is verified on disk", persistence line, scope-guard line, gate commands, ≤6 concurrent agents note. Discovery path: verify live whether `.agents/skills/` (official docs) or `.codex/skills/` is honored by the installed Codex version — if `codex` CLI is on PATH, check `codex --help` / docs; default to `.agents/skills/`, note the alternative in AGENTS.md.

- [ ] **Step 1:** Author `AGENTS.md`.
- [ ] **Step 2:** Author the 7 TOML files.
- [ ] **Step 3:** Author the 3 Codex skills.
- [ ] **Step 4:** Verify: `wc -c AGENTS.md` ≤ 6000; `python - <<'EOF'` snippet parsing each TOML with `tomllib` asserting required keys present `EOF`; `grep -rL 'core/pipeline.md' .agents/skills/*/SKILL.md` → empty (all reference it).
- [ ] **Step 5:** Commit.

### Task A11: JP harness verification sweep (sonnet) — spec §9

**Files:** none created; fixes applied wherever found.

- [ ] **Step 1:** Dead-reference sweep: `grep -rn --include='*.md' --include='*.toml' -E 'TeamCreate|TeamDelete|G:\\\\|[^e/]scripts/|[^e/]guides/' . | grep -v docs/` → fix any hit (docs/ exempt as history).
- [ ] **Step 2:** Contract cross-check: every file path named in `.claude/` and `.agents/`/`.codex/` exists (`grep -oh` paths, test -e loop); `core/pipeline.md` gate commands match actual script CLIs (`--check`, `--glossary`, `--all`, `--volume`).
- [ ] **Step 3:** Run all script tests: `python core/scripts/test_check_consistency.py && python core/scripts/test_derive_build_config.py` → ok.
- [ ] **Step 4:** Commit fixes (if any) + tag: `git tag jp-overhaul-done`.

---

## Phase B — CN webnovel sibling

### Task B1: Copy + strip to CN skeleton (sonnet) — spec §8, §9 step 5

**Files:**
- Create: `/home/yogesh/Translations/CN Translation Initialisation/` (full copy of JP folder minus `.git/`, `docs/`, `Source/`, `English/`, `Editing/` contents, source ebooks)
- Delete in copy: `core/scripts/split_ebook.py`, `core/scripts/kindleunpack/`, `core/scripts/normalize_romaji.py`, `core/scripts/build_epub.py` (replaced in B2–B4), their tests
- Init: fresh git repo in the CN folder, root commit of the skeleton

**Interfaces:** CN folder structure identical to JP post-A11; JP-only scripts gone; per-novel stubs empty.

- [ ] **Step 1:** `rsync -a --exclude .git --exclude docs --exclude 'Source/*' --exclude 'English/*' --exclude 'Editing/*' --exclude '*.epub' --exclude '*.azw3' "…/JP Translation Initialisation/" "…/CN Translation Initialisation/"`
- [ ] **Step 2:** Delete JP-only scripts listed above; `mkdir -p docs/superpowers/{specs,plans}` and copy the spec file in.
- [ ] **Step 3:** `git init -b main && git add -A && git commit -m "cn: skeleton from JP harness"`.

### Task B2: `ingest_chapters.py` + tests (opus) — spec §8 ingestion row

**Files:**
- Create: `core/scripts/ingest_chapters.py`, `core/scripts/test_ingest_chapters.py` (in CN folder)

**Interfaces:**
- CLI: `python core/scripts/ingest_chapters.py <raw-dir> <output-dir> --config novel.config.md [--volume N]`
- Input: folder of `.txt`/`.html` chapter files (sorted naturally: `ch1, ch2, … ch10` ordering via numeric key).
- Config knobs consumed (add to CN `core/schemas/novel-config-schema.md`): `chapters_per_volume` OR explicit `volume_ranges`; `boilerplate_patterns` (regex list, stripped); `traditional_to_simplified: true|false`.
- Behavior: encoding detect (try utf-8 → gb18030 → big5; `bytes.decode` attempts); HTML → text (stdlib `html.parser`, block tags → newlines); strip boilerplate patterns; drop in-body duplicate of the chapter title (first non-empty line equal/近-equal to filename title); normalize full-width punctuation option OFF by default (CJK punctuation kept — prose is still Chinese source); collapse 3+ blank lines; separate trailing author-note blocks (heuristic: final block starting with 作者|PS|注) into `> [Author's note] …` blockquote.
- Output: `Source/Volume N/NNNN <title>.md` + per-chapter ingestion report `Editing/Volume N/ingestion/NNNN.md` (what was stripped/normalized, anomalies: suspiciously short chapter, undecodable bytes, no title found). Exit 1 if any chapter emitted an anomaly (report gate).

- [ ] **Step 1:** Write failing tests: temp raw dir with (a) `第1章 开始.txt` GB18030-encoded with an ad line matching a boilerplate pattern, (b) `2.html` with `<p>` paragraphs + duplicated title line, (c) a 3-line stub chapter (anomaly). Assert: two clean `Source/Volume 1/000*.md` outputs with ad/dup-title gone, reports exist for all three, exit 1 (stub anomaly), `--volume` boundary respected when `chapters_per_volume: 2`.
- [ ] **Step 2:** Run → fail. **Step 3:** Implement. **Step 4:** Tests pass. **Step 5:** Commit.

### Task B3: `build_epub_scratch.py` + tests (opus) — spec §8 EPUB row

**Files:**
- Create: `core/scripts/build_epub_scratch.py`, `core/scripts/test_build_epub_scratch.py`; Modify: `core/scripts/verify_epub.py` (CN copy) — replace macron gate with pinyin-convention gate hook; keep zip/spine/refs/footnote/CJK gates.

**Interfaces:**
- CLI: `python core/scripts/build_epub_scratch.py --config <build_config.json>` — same JSON shape as JP `derive_build_config.py` output MINUS `source_epub` (no shell); plus optional `cover_image` path and `css` override.
- Generates EPUB3 from scratch: `mimetype` (STORED, first), `META-INF/container.xml`, `OEBPS/content.opf` (metadata from config, spine LTR), `nav.xhtml`, one XHTML per chapter (MD → XHTML: paragraphs, `---` → centered ornament, `[^N]` → EPUB3 popup noterefs/asides with per-chapter ids, `## Translator Notes` → aside section), optional cover. Titles/H1s from config map (no in-file headings).
- `derive_build_config.py` (already in skeleton) keeps working: only change is CN schema drops the volume→source-epub map requirement (make `source_epub` optional in the CN copy).
- Must pass CN `verify_epub.py` gates.

- [ ] **Step 1:** Failing test: temp `English/Volume 1/` with 2 tiny chapter .md files (one containing a `[^1]` footnote + `---` break), minimal JSON config; build; then assert with `zipfile`: mimetype first+STORED, container.xml present, 2 chapter XHTMLs + nav, footnote noteref/aside pair present, then run `verify_epub.py --epub out.epub` → exit 0.
- [ ] **Step 2:** Run → fail. **Step 3:** Implement (~250 lines, stdlib `zipfile`/`html`). **Step 4:** Tests + verify gates pass. **Step 5:** Update CN `core/guides/epub-build-spec.md` for from-scratch flow. **Step 6:** Commit.

### Task B4: `normalize_pinyin.py` + tests (sonnet) — spec §8 gate row

**Files:**
- Create: `core/scripts/normalize_pinyin.py`, `core/scripts/test_normalize_pinyin.py` (CN folder)

**Interfaces:**
- CLI mirrors romaji script: `python core/scripts/normalize_pinyin.py [--check] [--convention toneless|diacritics] file…` (convention read from `--convention`, documented default `toneless`).
- `toneless`: tone-marked vowels (āáǎà ēéěè īíǐì ōóǒò ūúǔù ǖǘǚǜ ü + uppercase) → bare vowel (ü→u); `--check` reports and exits 1 on any tone mark. `diacritics`: `--check` only verifies NO mixed usage (flags `v` used as ü substitute and digit-tone syllables like `ni3`); no rewrite mode needed. `# ponytail: digit-tone regex is a heuristic — refine if false positives on e.g. 'ni3' in URLs`.

- [ ] **Step 1:** Failing tests: toneless check flags `Zhāng`, rewrite fixes to `Zhang`; diacritics mode passes `Zhāng` but flags `Zhang1`/`nv3`. **Step 2:** fail → **Step 3:** implement → **Step 4:** pass → **Step 5:** Commit.

### Task B5: CN guides + schemas (opus; read RD-LIT) — spec §8 guides/voice/QA rows

**Files (CN folder):**
- Rewrite: `core/guides/translation-guide.md` (CN), `core/guides/voice-building-guide.md` (CN), `core/guides/footnote-guide.md` (CN cultural table), `core/guides/qa-audit-guide.md` (CN failure classes), `core/pipeline.md` (gate names, ingestion stage, chapter-range mode)
- Modify: `core/schemas/novel-config-schema.md` (CN knobs: `pinyin_convention`, `chapters_per_volume`/`volume_ranges`, `boilerplate_patterns`, `traditional_to_simplified`; drop source-epub requirement, part-split stays), `core/schemas/character-voices-schema.md` (CN voice axes), `core/schemas/glossary-schema.md` (note: address-term renderings locked here)

**Interfaces / content contracts:**
- Pinyin policy (LOCKED by user): **pinyin for names only**; every other term translated to English; pinyin fallback ONLY when the literal EN rendering misleads → footnote on first use. Address terms (师兄/道友/前辈/公子/哥…): translate by default ("senior brother"), pinyin+footnote when translation misleads; chosen rendering locked in glossary; per-character address-form table in `character-reference.md`; address-shift moments (你→您, name→title) flagged like JP address shifts.
- CN name order family-first; chengyu: render meaning, footnote only when culturally load-bearing; no furigana/honorific-suffix machinery.
- Voice axes: address terms, 您/你 formality, classical-vs-colloquial diction, verbal tics.
- QA failure classes: dropped-subject recovery, address-term/register mapping, chengyu mistranslation, compression.
- Pipeline: ingestion stage + report gate before setup completes; `/translate-chapter` accepts a range `12-20` (sequential per-chapter runs, per-chapter gates individually; fresh teammates per chapter).

- [ ] **Step 1:** Rewrite the five guides/pipeline. **Step 2:** Update the three schemas. **Step 3:** Verify: `grep -rn 'furigana\|honorific\|romaji\|keigo' core/ --include='*.md'` in CN folder → only the address-term-tracking analogue mentions, no JP machinery; `grep -l 'pinyin for names only\|names only' core/guides/translation-guide.md` → hit. **Step 4:** Commit.

### Task B6: CN runtime packs (opus; read RD-OPUS + RD-GPT) — spec §8

**Files (CN folder):**
- Modify: all `.claude/agents/*.md`, `.claude/skills/*/SKILL.md`, `CLAUDE.md`, `AGENTS.md`, `.codex/agents/*.toml`, `.agents/skills/*/SKILL.md`

**Interfaces:** Same structure as JP twins; deltas only: setup-novel runs `ingest_chapters.py` (not split_ebook) and surfaces the ingestion reports for user review before completing; translate-chapter gains the chapter-range loop; gates swap to `normalize_pinyin.py --check --convention <from config>`; build skills call `build_epub_scratch.py`; QA failure classes per B5; kill-list/ceiling machinery identical to JP; image-localizer retained (webnovels sometimes ship art) but marked optional-when-no-images.

- [ ] **Step 1:** Apply deltas across both packs. **Step 2:** Verify: `grep -rn 'split_ebook\|normalize_romaji\|kindleunpack\|azw3' .claude/ .agents/ .codex/ CLAUDE.md AGENTS.md` in CN folder → nothing; range syntax documented in both translate-chapter skills. **Step 3:** Commit.

### Task B7: CN verification sweep + JP memory note (sonnet)

- [ ] **Step 1:** In CN folder: run all script tests (`test_ingest_chapters.py`, `test_build_epub_scratch.py`, `test_normalize_pinyin.py`, `test_check_consistency.py`, `test_derive_build_config.py`) → all pass.
- [ ] **Step 2:** Dead-reference sweep as in A11 (JP-only tool names, `G:\`, TeamCreate) → nothing.
- [ ] **Step 3:** Path-existence check: every `core/…` path cited in CN `.claude/`/`.agents/`/`.codex/`/`AGENTS.md`/`CLAUDE.md` exists.
- [ ] **Step 4:** Commit + tag `cn-harness-done`. In the JP repo, commit any stragglers.

---

## Self-review record

- Spec coverage: §3→A2/A3/A9/A10, §4→A7/A8/A10, §5.1–5.3→A6/A7, §5.4→A4, §5.5→A8/A6, §6→A5/A2, §7.1→A7/A8/A9, §7.2→A10, §8→B1–B6, §9→A1/A2/B1, §10 honored globally (no BLEU task exists), §11 persisted as research digests.
- No-placeholder scan: script tasks carry real test code; markdown tasks carry exact section/content contracts + grep-verifiable acceptance; nothing says "TBD/similar to".
- Type/name consistency: `check_consistency.py --glossary/--all`, `derive_build_config.py --volume/--out`, `qa_major_threshold`, `Aliases/Banned`, `style-guide.md` section names used identically across A3–A8, B5–B6.
