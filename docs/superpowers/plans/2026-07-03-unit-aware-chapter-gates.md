# Unit-Aware Chapter Gates Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a one-command chapter gate runner that works for both volume-based light novels and non-volume webnovels.

**Architecture:** Add a small shared config resolver module under `core/scripts/` that understands the existing legacy `Vol` chapter-title map and a new optional `Unit` shape. Then add `run_chapter_gates.py` as the shallow operator interface: caller supplies chapter plus optional unit, and the script resolves paths, runs the existing gates in order, and returns one final status. Keep the old raw gate commands documented for debugging.

**Tech Stack:** Python 3 standard library only, Markdown config parsing consistent with `derive_build_config.py`, existing `normalize_romaji.py` and `check_consistency.py` gates, direct self-running test files.

---

## File Structure

- Create `core/scripts/harness_config.py`
  - Shared Markdown config helpers copied and narrowed from `derive_build_config.py`.
  - Resolves chapter rows from either `| Vol | N | JP title | EN title |` or `| Unit | N | JP title | EN title |`.
  - Resolves unit paths from an optional `## Unit paths` table, with legacy fallback to `Source/Volume N`, `English/Volume N`, and `Editing/Volume N`.
  - Resolves final chapter files by exact title filename first, then `Chapter <N> - *.md` fallback for sanitized titles.

- Create `core/scripts/run_chapter_gates.py`
  - CLI wrapper around the three existing gate commands.
  - Accepts `--chapter N`, optional `--unit UNIT`, optional `--config novel.config.md`, and optional `--python python3`.
  - Runs gates in order and exits non-zero on the first failure.

- Create `core/scripts/test_harness_config.py`
  - Directly runnable tests for unit/path/title resolution.
  - Covers legacy volume config, webnovel `main` unit, ambiguous chapter without unit, sanitized filename fallback, and ambiguous sanitized fallback.

- Create `core/scripts/test_run_chapter_gates.py`
  - Directly runnable tests for CLI behavior using temporary fixture projects.
  - Covers success, macron failure, missing chapter, ambiguous unit, and use of a fake Python executable to verify command order without relying on shell parsing.

- Modify `core/scripts/derive_build_config.py`
  - Only after the new resolver tests pass, refactor its duplicate Markdown helpers to import from `harness_config.py`.
  - Keep `--volume` behavior unchanged.

- Modify `core/scripts/test_derive_build_config.py`
  - Add one assertion that legacy volume behavior still derives the same config after the helper extraction.

- Modify `core/pipeline.md`
  - Add the wrapper as the preferred Stage 6 command.
  - Keep the three raw commands below it as the debugging equivalent.
  - Replace “whole volume” wording in the gate explanation with “whole unit,” noting that legacy light-novel units are usually volumes.

- Modify `AGENTS.md`
  - Add the wrapper command in `<gate_commands>`.
  - Keep raw commands as fallback/debug commands.

- Modify `CLAUDE.md`
  - Update the runtime summary line for consistency gates from “whole volume” to “whole unit.”

- Modify `.agents/skills/translate-chapter/SKILL.md`
  - Update Stage 5/6 gate instructions to run `run_chapter_gates.py --chapter N` or `--unit UNIT --chapter N`.

- Modify `.claude/skills/translate-chapter/SKILL.md`
  - Mirror the Codex skill gate-instruction update so the Claude Code runtime does not keep the old raw-command, volume-only flow.

- Modify `core/guides/quality-checklist.md`
  - Update the Gates section to prefer the wrapper.

- Modify `core/schemas/novel-config-schema.md`
  - Document the new optional `Unit paths` table.
  - Document the compatibility rule narrowly: `Unit` title maps are supported by the chapter gate wrapper; the EPUB build path remains volume-based until `derive_build_config.py` and `/build-epub` are made unit-aware.

---

### Task 1: Add Shared Config Resolver Tests

**Files:**
- Create: `core/scripts/test_harness_config.py`
- Create later: `core/scripts/harness_config.py`

- [ ] **Step 1: Write failing tests for legacy and unit-aware resolution**

Create `core/scripts/test_harness_config.py` with this content:

```python
import os
import tempfile
import textwrap

import harness_config


LEGACY_CONFIG = textwrap.dedent("""\
    # Novel Config

    ## Chapter-title map

    | Vol | N | JP title | EN title |
    |-|-|-|-|
    | 1 | 1 | 一 | First |
    | 1 | 2 | 二 | Reunion: A New Dawn |
""")


UNIT_CONFIG = textwrap.dedent("""\
    # Novel Config

    ## Unit paths

    | Unit | Source path | English path | Editing path |
    |-|-|-|-|
    | main | Source/main | English/main | Editing/main |
    | arc-2 | Source/Arc 2 | English/Arc 2 | Editing/Arc 2 |

    ## Chapter-title map

    | Unit | N | JP title | EN title |
    |-|-|-|-|
    | main | 37 | 第37話 | The Visitor |
    | arc-2 | 37 | 第37話 | The Visitor Returns |
""")


def write_project(config_text, files):
    root = tempfile.mkdtemp()
    with open(os.path.join(root, "novel.config.md"), "w", encoding="utf-8") as f:
        f.write(config_text)
    for relpath, text in files.items():
        path = os.path.join(root, relpath)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
    return root


def load(root):
    return harness_config.load_project_config(os.path.join(root, "novel.config.md"))


def test_legacy_volume_row_resolves_as_unit_1():
    root = write_project(
        LEGACY_CONFIG,
        {"English/Volume 1/Chapter 1 - First.md": "clean prose\n"},
    )
    cfg = load(root)
    row = cfg.resolve_chapter(unit="1", chapter="1")
    assert row.unit == "1"
    assert row.chapter == "1"
    assert row.title == "First"
    assert row.english_dir == os.path.join(root, "English", "Volume 1")
    assert row.final_path == os.path.join(root, "English", "Volume 1", "Chapter 1 - First.md")


def test_single_unit_can_be_inferred_for_webnovel():
    config = UNIT_CONFIG.replace(
        "| arc-2 | 37 | 第37話 | The Visitor Returns |\n",
        "",
    ).replace(
        "| arc-2 | Source/Arc 2 | English/Arc 2 | Editing/Arc 2 |\n",
        "",
    )
    root = write_project(
        config,
        {"English/main/Chapter 37 - The Visitor.md": "clean prose\n"},
    )
    cfg = load(root)
    row = cfg.resolve_chapter(unit=None, chapter="37")
    assert row.unit == "main"
    assert row.final_path == os.path.join(root, "English", "main", "Chapter 37 - The Visitor.md")


def test_ambiguous_unit_requires_unit_argument():
    root = write_project(
        UNIT_CONFIG,
        {
            "English/main/Chapter 37 - The Visitor.md": "clean prose\n",
            "English/Arc 2/Chapter 37 - The Visitor Returns.md": "clean prose\n",
        },
    )
    cfg = load(root)
    try:
        cfg.resolve_chapter(unit=None, chapter="37")
    except harness_config.ConfigError as exc:
        assert "multiple units" in str(exc)
    else:
        raise AssertionError("expected ambiguous unit failure")


def test_sanitized_filename_falls_back_to_chapter_glob():
    root = write_project(
        LEGACY_CONFIG,
        {"English/Volume 1/Chapter 2 - Reunion A New Dawn.md": "clean prose\n"},
    )
    cfg = load(root)
    row = cfg.resolve_chapter(unit="1", chapter="2")
    assert row.title == "Reunion: A New Dawn"
    assert row.final_path.endswith("Chapter 2 - Reunion A New Dawn.md")


def test_ambiguous_sanitized_glob_is_fatal():
    root = write_project(
        LEGACY_CONFIG,
        {
            "English/Volume 1/Chapter 2 - Reunion A New Dawn.md": "clean prose\n",
            "English/Volume 1/Chapter 2 - Reunion, A New Dawn.md": "clean prose\n",
        },
    )
    cfg = load(root)
    try:
        cfg.resolve_chapter(unit="1", chapter="2")
    except harness_config.ConfigError as exc:
        assert "multiple files" in str(exc)
    else:
        raise AssertionError("expected ambiguous file failure")


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
    print("ok")
```

- [ ] **Step 2: Run tests and verify they fail because the module is absent**

Run:

```bash
python3 core/scripts/test_harness_config.py
```

Expected: FAIL with `ModuleNotFoundError: No module named 'harness_config'`.

---

### Task 2: Implement `harness_config.py`

**Files:**
- Create: `core/scripts/harness_config.py`
- Test: `core/scripts/test_harness_config.py`

- [ ] **Step 1: Add the resolver implementation**

Create `core/scripts/harness_config.py` with this content:

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Shared config helpers for the translation harness scripts.

The harness historically used "Vol" as the release unit. Webnovels often do
not have volumes, so this module exposes a neutral unit resolver while keeping
legacy Vol tables working unchanged.
"""

import glob
import io
import os
import re
from dataclasses import dataclass


BULLET_RE = re.compile(r"^\s*-\s*\*\*(.+?):\*\*\s*(.*)$")


class ConfigError(Exception):
    """Raised when novel.config.md cannot identify one unambiguous artifact."""


@dataclass(frozen=True)
class ChapterResolution:
    unit: str
    chapter: str
    title: str
    source_dir: str
    english_dir: str
    editing_dir: str
    final_path: str


def split_sections(text):
    parts = re.split(r"(?m)^##\s+(.*)$", text)
    sections = {}
    for i in range(1, len(parts), 2):
        heading = parts[i].strip().lower()
        body = parts[i + 1] if i + 1 < len(parts) else ""
        sections[heading] = body
    return sections


def get_section(sections, *keywords):
    for heading, body in sections.items():
        if all(k in heading for k in keywords):
            return body
    return ""


def clean(value):
    return value.strip().strip("`").strip()


def parse_bullets(body):
    out = {}
    for line in body.splitlines():
        m = BULLET_RE.match(line.strip())
        if m:
            out[m.group(1).strip().lower()] = clean(m.group(2))
    return out


def parse_table(body):
    rows = []
    for line in body.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.split("|")]
        if cells and cells[0] == "":
            cells = cells[1:]
        if cells and cells[-1] == "":
            cells = cells[:-1]
        if all(re.fullmatch(r":?-+:?", c) for c in cells):
            continue
        rows.append(cells)
    if not rows:
        return []
    header = [h.strip().lower() for h in rows[0]]
    return [
        {header[i]: (row[i] if i < len(row) else "") for i in range(len(header))}
        for row in rows[1:]
    ]


def _abspath(base_dir, relpath):
    relpath = clean(relpath)
    if os.path.isabs(relpath):
        return os.path.normpath(relpath)
    return os.path.normpath(os.path.join(base_dir, relpath))


def _row_unit(row):
    unit = clean(row.get("unit", ""))
    if unit:
        return unit
    vol = clean(row.get("vol", ""))
    if vol:
        return vol
    return ""


def _legacy_paths(base_dir, unit):
    return {
        "source": os.path.join(base_dir, "Source", "Volume %s" % unit),
        "english": os.path.join(base_dir, "English", "Volume %s" % unit),
        "editing": os.path.join(base_dir, "Editing", "Volume %s" % unit),
    }


def _path_rows_by_unit(base_dir, path_rows):
    paths = {}
    for row in path_rows:
        unit = _row_unit(row)
        if not unit:
            continue
        paths[unit] = {
            "source": _abspath(base_dir, row.get("source path", "Source/%s" % unit)),
            "english": _abspath(base_dir, row.get("english path", "English/%s" % unit)),
            "editing": _abspath(base_dir, row.get("editing path", "Editing/%s" % unit)),
        }
    return paths


class ProjectConfig:
    def __init__(self, config_path, text):
        self.config_path = os.path.abspath(config_path)
        self.base_dir = os.path.dirname(self.config_path)
        self.sections = split_sections(text)
        self.identity = parse_bullets(get_section(self.sections, "identity"))
        self.source_table = parse_table(get_section(self.sections, "source ebooks"))
        self.chapter_table = parse_table(get_section(self.sections, "chapter-title map"))
        self.epub_metadata = parse_bullets(get_section(self.sections, "epub metadata"))
        self.unit_paths = _path_rows_by_unit(
            self.base_dir,
            parse_table(get_section(self.sections, "unit paths")),
        )

    def paths_for_unit(self, unit):
        unit = clean(str(unit))
        if unit in self.unit_paths:
            return self.unit_paths[unit]
        return _legacy_paths(self.base_dir, unit)

    def chapter_rows(self, chapter):
        chapter = clean(str(chapter))
        return [
            row for row in self.chapter_table
            if clean(row.get("n", "")) == chapter and _row_unit(row)
        ]

    def resolve_chapter(self, unit, chapter):
        chapter = clean(str(chapter))
        wanted_unit = clean(str(unit)) if unit is not None else ""
        rows = self.chapter_rows(chapter)
        if wanted_unit:
            rows = [row for row in rows if _row_unit(row) == wanted_unit]

        if not rows:
            scope = "unit %r " % wanted_unit if wanted_unit else ""
            raise ConfigError("chapter %s%snot found in chapter-title map" % (scope, chapter))

        units = sorted({_row_unit(row) for row in rows})
        if not wanted_unit and len(units) > 1:
            raise ConfigError(
                "chapter %s appears in multiple units (%s); pass --unit"
                % (chapter, ", ".join(units))
            )
        if len(rows) > 1:
            raise ConfigError("chapter %s has multiple title rows for unit %s" % (chapter, units[0]))

        row = rows[0]
        resolved_unit = _row_unit(row)
        title = clean(row.get("en title", ""))
        if not title:
            raise ConfigError("chapter %s in unit %s has no EN title" % (chapter, resolved_unit))

        paths = self.paths_for_unit(resolved_unit)
        final_path = resolve_chapter_file(paths["english"], chapter, title)
        return ChapterResolution(
            unit=resolved_unit,
            chapter=chapter,
            title=title,
            source_dir=paths["source"],
            english_dir=paths["english"],
            editing_dir=paths["editing"],
            final_path=final_path,
        )


def resolve_chapter_file(english_dir, chapter, title):
    exact = os.path.join(english_dir, "Chapter %s - %s.md" % (chapter, title))
    if os.path.isfile(exact):
        return exact
    matches = sorted(glob.glob(os.path.join(english_dir, "Chapter %s - *.md" % chapter)))
    if len(matches) == 1:
        return matches[0]
    if len(matches) > 1:
        names = ", ".join(os.path.basename(m) for m in matches)
        raise ConfigError(
            "chapter %s (%r) matches multiple files on disk: %s; rename so exactly one remains"
            % (chapter, title, names)
        )
    raise ConfigError("chapter file not found: expected %s" % exact)


def load_project_config(config_path):
    with io.open(config_path, "r", encoding="utf-8") as f:
        return ProjectConfig(config_path, f.read())
```

- [ ] **Step 2: Run resolver tests**

Run:

```bash
python3 core/scripts/test_harness_config.py
```

Expected: `ok`.

---

### Task 3: Add Gate Runner Tests

**Files:**
- Create: `core/scripts/test_run_chapter_gates.py`
- Create later: `core/scripts/run_chapter_gates.py`

- [ ] **Step 1: Write failing CLI tests**

Create `core/scripts/test_run_chapter_gates.py` with this content:

```python
import os
import shutil
import stat
import subprocess
import sys
import tempfile
import textwrap


SCRIPT = os.path.join(os.path.dirname(__file__), "run_chapter_gates.py")
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
CORE_DIR = os.path.join(REPO_ROOT, "core")


CONFIG = textwrap.dedent("""\
    # Novel Config

    ## Unit paths

    | Unit | Source path | English path | Editing path |
    |-|-|-|-|
    | main | Source/main | English/main | Editing/main |

    ## Chapter-title map

    | Unit | N | JP title | EN title |
    |-|-|-|-|
    | main | 37 | 第37話 | The Visitor |
""")


GLOSSARY = textwrap.dedent("""\
    | JP | EN | Aliases/Banned | Gender/Context |
    |-|-|-|-|
    | 西部戦線 | Western Front | Western Theatre | place |
""")


def make_project(chapter_text):
    root = tempfile.mkdtemp()
    shutil.copytree(CORE_DIR, os.path.join(root, "core"))
    with open(os.path.join(root, "novel.config.md"), "w", encoding="utf-8") as f:
        f.write(CONFIG)
    with open(os.path.join(root, "glossary.md"), "w", encoding="utf-8") as f:
        f.write(GLOSSARY)
    chapter_path = os.path.join(root, "English", "main", "Chapter 37 - The Visitor.md")
    os.makedirs(os.path.dirname(chapter_path), exist_ok=True)
    with open(chapter_path, "w", encoding="utf-8") as f:
        f.write(chapter_text)
    return root


def run(root, *args):
    return subprocess.run(
        [sys.executable, SCRIPT, "--config", "novel.config.md", "--chapter", "37", *args],
        cwd=root,
        capture_output=True,
        text=True,
    )


def test_success_runs_all_three_gates():
    root = make_project("They marched to the Western Front.\n")
    p = run(root)
    assert p.returncode == 0, p.stdout + p.stderr
    assert "PASS normalize_romaji" in p.stdout
    assert "PASS consistency_chapter" in p.stdout
    assert "PASS consistency_unit" in p.stdout


def test_macron_failure_stops_before_consistency():
    root = make_project("Ōtori marched to the Western Front.\n")
    p = run(root)
    assert p.returncode == 1, p.stdout + p.stderr
    assert "FAIL normalize_romaji" in p.stdout
    assert "consistency_chapter" not in p.stdout


def test_missing_chapter_fails_before_gates():
    root = make_project("They marched to the Western Front.\n")
    os.remove(os.path.join(root, "English", "main", "Chapter 37 - The Visitor.md"))
    p = run(root)
    assert p.returncode == 2
    assert "chapter file not found" in p.stderr


def test_ambiguous_unit_fails_before_gates():
    root = make_project("They marched to the Western Front.\n")
    with open(os.path.join(root, "novel.config.md"), "a", encoding="utf-8") as f:
        f.write("| arc-2 | 37 | 第37話 | Other Visitor |\n")
    p = run(root)
    assert p.returncode == 2
    assert "multiple units" in p.stderr


def test_fake_python_receives_gate_commands_in_order():
    root = make_project("They marched to the Western Front.\n")
    log = os.path.join(root, "commands.log")
    fake_python = os.path.join(root, "fake-python")
    with open(fake_python, "w", encoding="utf-8") as f:
        f.write("#!/bin/sh\necho \"$@\" >> commands.log\nexit 0\n")
    os.chmod(fake_python, stat.S_IRWXU)

    p = run(root, "--python", fake_python)
    assert p.returncode == 0, p.stdout + p.stderr
    with open(log, encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines()]
    assert lines[0].startswith("core/scripts/normalize_romaji.py --check ")
    assert lines[1].startswith("core/scripts/check_consistency.py --glossary glossary.md ")
    assert lines[2] == "core/scripts/check_consistency.py --glossary glossary.md --all English/main"


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
    print("ok")
```

- [ ] **Step 2: Run tests and verify they fail because the script is absent**

Run:

```bash
python3 core/scripts/test_run_chapter_gates.py
```

Expected: FAIL because `core/scripts/run_chapter_gates.py` does not exist.

---

### Task 4: Implement `run_chapter_gates.py`

**Files:**
- Create: `core/scripts/run_chapter_gates.py`
- Test: `core/scripts/test_run_chapter_gates.py`

- [ ] **Step 1: Add gate runner implementation**

Create `core/scripts/run_chapter_gates.py` with this content:

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run the chapter completion gates with a small operator interface.

Examples:
  python3 core/scripts/run_chapter_gates.py --chapter 37
  python3 core/scripts/run_chapter_gates.py --unit main --chapter 37
  python3 core/scripts/run_chapter_gates.py --unit 1 --chapter 3
"""

import argparse
import os
import subprocess
import sys

import harness_config


def rel(base_dir, path):
    try:
        return os.path.relpath(path, base_dir)
    except ValueError:
        return path


def run_gate(name, command, cwd):
    print("RUN  %s: %s" % (name, " ".join(command)))
    completed = subprocess.run(command, cwd=cwd, text=True, capture_output=True)
    if completed.stdout:
        print(completed.stdout, end="")
    if completed.stderr:
        print(completed.stderr, end="", file=sys.stderr)
    if completed.returncode == 0:
        print("PASS %s" % name)
        return True
    print("FAIL %s (exit %d)" % (name, completed.returncode))
    return False


def main():
    parser = argparse.ArgumentParser(description="Run chapter gates from novel.config.md")
    parser.add_argument("--config", default="novel.config.md")
    parser.add_argument("--unit", default=None, help="Unit key, e.g. 1, main, arc-2")
    parser.add_argument("--chapter", required=True, help="Chapter number/key from the title map")
    parser.add_argument("--python", default=sys.executable or "python3", help="Python executable for gates")
    args = parser.parse_args()

    config_path = os.path.abspath(args.config)
    base_dir = os.path.dirname(config_path)

    try:
        cfg = harness_config.load_project_config(config_path)
        chapter = cfg.resolve_chapter(unit=args.unit, chapter=args.chapter)
    except (OSError, harness_config.ConfigError) as exc:
        print("error: %s" % exc, file=sys.stderr)
        return 2

    chapter_rel = rel(base_dir, chapter.final_path)
    english_rel = rel(base_dir, chapter.english_dir)
    print("Resolved unit=%s chapter=%s title=%r" % (chapter.unit, chapter.chapter, chapter.title))
    print("Chapter file: %s" % chapter_rel)

    gates = [
        (
            "normalize_romaji",
            [args.python, os.path.join("core", "scripts", "normalize_romaji.py"), "--check", chapter_rel],
        ),
        (
            "consistency_chapter",
            [
                args.python,
                os.path.join("core", "scripts", "check_consistency.py"),
                "--glossary",
                "glossary.md",
                chapter_rel,
            ],
        ),
        (
            "consistency_unit",
            [
                args.python,
                os.path.join("core", "scripts", "check_consistency.py"),
                "--glossary",
                "glossary.md",
                "--all",
                english_rel,
            ],
        ),
    ]

    for name, command in gates:
        if not run_gate(name, command, base_dir):
            return 1

    print("RESULT: ALL PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 2: Run gate runner tests**

Run:

```bash
python3 core/scripts/test_run_chapter_gates.py
```

Expected: `ok`.

- [ ] **Step 3: Smoke-test the new CLI help**

Run:

```bash
python3 core/scripts/run_chapter_gates.py --help
```

Expected: usage text includes `--unit`, `--chapter`, `--config`, and `--python`.

---

### Task 5: Refactor `derive_build_config.py` to Reuse Shared Parsing

**Files:**
- Modify: `core/scripts/derive_build_config.py`
- Modify: `core/scripts/test_derive_build_config.py`
- Test: `core/scripts/test_derive_build_config.py`

- [ ] **Step 1: Replace duplicate helper definitions**

In `core/scripts/derive_build_config.py`, remove `BULLET_RE`, `split_sections`, `get_section`, `clean`, `parse_bullets`, and `parse_table`. Add this import near the other imports:

```python
from harness_config import clean, get_section, parse_bullets, parse_table, split_sections
```

Keep the rest of `derive()` unchanged in this task.

- [ ] **Step 2: Run build-config tests**

Run:

```bash
python3 core/scripts/test_derive_build_config.py
```

Expected: `ok`.

- [ ] **Step 3: Add a regression assertion for legacy volume directory**

In `test_derives_config_with_one_missing_chapter()` in `core/scripts/test_derive_build_config.py`, after loading `cfg`, add:

```python
    assert cfg["chapters_dir"].endswith(os.path.join("English", "Volume 1"))
```

- [ ] **Step 4: Re-run build-config tests**

Run:

```bash
python3 core/scripts/test_derive_build_config.py
```

Expected: `ok`.

---

### Task 6: Document Unit-Aware Gates in Core Docs

**Files:**
- Modify: `core/pipeline.md`
- Modify: `AGENTS.md`
- Modify: `CLAUDE.md`
- Modify: `core/guides/quality-checklist.md`
- Modify: `core/schemas/novel-config-schema.md`

- [ ] **Step 1: Update `core/pipeline.md` Stage 6 gate commands**

Replace the Stage 6 gate command block with:

```markdown
## Gate commands

Preferred wrapper. If the chapter number is unique in the chapter-title map:

```bash
python3 core/scripts/run_chapter_gates.py --chapter <N>
```

If the same chapter number appears in more than one unit, pass the unit:

```bash
python3 core/scripts/run_chapter_gates.py --unit <Unit> --chapter <N>
```

Multi-volume light novels often restart chapter numbering in each volume, so
they will commonly use `--unit 1`, `--unit 2`, and so on. Single-stream
webnovels commonly omit `--unit` once `main` is the only configured unit.

The wrapper resolves the final chapter file from `novel.config.md`, runs the
chapter romanization gate, the chapter consistency gate, and the whole-unit
consistency gate in order, then exits non-zero on the first failure.

Debug equivalent, with explicit paths substituted from `novel.config.md`:

```bash
# Romanization: no macrons
python3 core/scripts/normalize_romaji.py --check "<English path>/Chapter <N> - <Title>.md"

# Deterministic consistency, this chapter
python3 core/scripts/check_consistency.py --glossary glossary.md "<English path>/Chapter <N> - <Title>.md"

# Deterministic consistency, whole unit
python3 core/scripts/check_consistency.py --glossary glossary.md --all "<English path>"
```
```

- [ ] **Step 2: Update whole-volume wording in `core/pipeline.md`**

Replace this full bullet:

```markdown
The chapter is filed **done** only after `check_consistency.py --all` passes
post-Update (Stage 6). The updater may revise the glossary, and a glossary
change can invalidate an already-passed chapter's terminology; the `--all`
run is what makes QA's glossary check non-stale across the whole volume.
```

with:

```markdown
The chapter is filed **done** only after the whole-unit consistency gate passes
post-Update (Stage 6). For light novels the unit is usually a volume; for
webnovels it may be `main`, an arc, a part, or another project-defined grouping.
```

- [ ] **Step 3: Update `AGENTS.md` gate command block**

Replace the three-command primary block in `<gate_commands>` with the wrapper examples from Task 6 Step 1. Keep a short “debug equivalent” block below it with the raw `python3` commands.

- [ ] **Step 4: Update `CLAUDE.md` consistency-gate summary**

Change the line that says `check_consistency.py` runs `--all` over the whole volume to:

```markdown
10. Consistency gates — `core/scripts/check_consistency.py` runs per-chapter, and again with `--all` over the whole unit after every Update, because a glossary revision back-propagates to already-filed chapters in that unit. For light novels the unit is usually a volume; for webnovels it may be `main`, an arc, or another project-defined grouping.
```

- [ ] **Step 5: Update `core/guides/quality-checklist.md` Gates section**

Replace the two consistency gate checklist items with:

```markdown
- [ ] **Chapter gates clean** —
      `python3 core/scripts/run_chapter_gates.py --chapter <N>` exits zero. If
      `<N>` is ambiguous across units, run
      `python3 core/scripts/run_chapter_gates.py --unit <Unit> --chapter <N>`.
      This includes romanization, chapter consistency, and whole-unit
      consistency after the updater runs.
```

- [ ] **Step 6: Update `core/schemas/novel-config-schema.md`**

Add this bullet under `## Knobs` after `Paths`:

```markdown
- **Unit paths** — optional table `| Unit | Source path | English path | Editing path |`.
  Use this for webnovels or any project whose release unit is not a numbered
  volume when running chapter gates. If absent, scripts retain the legacy
  fallback: `Source/Volume N/`, `English/Volume N/`, `Editing/Volume N/`.
  The EPUB build path remains volume-based until `derive_build_config.py` and
  `/build-epub` are made unit-aware.
```

Replace the chapter-title map bullet with:

```markdown
- **Chapter-title map** — the legacy table `| Vol | N | JP title | EN title |`
  remains required for volume-based projects and EPUB builds. The chapter gate
  wrapper also accepts `| Unit | N | JP title | EN title |` for webnovel-style
  gate runs. This table remains the single source of truth for output filenames;
  EPUB `<h1>`/TOC/contents titles are still consumed through the legacy `Vol`
  form until the build path is made unit-aware.
```

---

### Task 7: Update Translate Skill Gate Instructions

**Files:**
- Modify: `.agents/skills/translate-chapter/SKILL.md`
- Modify: `.claude/skills/translate-chapter/SKILL.md`

- [ ] **Step 1: Retitle the Gates heading in both skills**

In `.agents/skills/translate-chapter/SKILL.md`, change:

```markdown
## 5. Gates (all three must exit 0)
```

to:

```markdown
## 5. Gates (wrapper must exit 0)
```

In `.claude/skills/translate-chapter/SKILL.md`, change:

```markdown
## 6. Gates (all three must exit 0)
```

to:

```markdown
## 6. Gates (wrapper must exit 0)
```

- [ ] **Step 2: Replace raw gate commands in the Gates section**

In both skill files, replace the command block in the `Gates` section with:

```markdown
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
```

- [ ] **Step 3: Replace “volume” with “unit” in the gate result report**

In both skill files, change:

```markdown
and the exit status of all three gates.
```

to:

```markdown
and the wrapper output for the chapter gates.
```

---

### Task 8: Run Full Verification

**Files:**
- Test: `core/scripts/test_harness_config.py`
- Test: `core/scripts/test_run_chapter_gates.py`
- Test: `core/scripts/test_check_consistency.py`
- Test: `core/scripts/test_derive_build_config.py`

- [ ] **Step 1: Run all direct tests**

Run:

```bash
python3 core/scripts/test_harness_config.py
python3 core/scripts/test_run_chapter_gates.py
python3 core/scripts/test_check_consistency.py
python3 core/scripts/test_derive_build_config.py
```

Expected:

```text
ok
ok
ok
ok
```

- [ ] **Step 2: Run a manual webnovel fixture smoke test**

Run:

```bash
tmpdir="$(mktemp -d)"
cp -R core "$tmpdir/core"
cat > "$tmpdir/novel.config.md" <<'EOF'
# Novel Config

## Unit paths

| Unit | Source path | English path | Editing path |
|-|-|-|-|
| main | Source/main | English/main | Editing/main |

## Chapter-title map

| Unit | N | JP title | EN title |
|-|-|-|-|
| main | 1 | 第1話 | First |
EOF
cat > "$tmpdir/glossary.md" <<'EOF'
| JP | EN | Aliases/Banned | Gender/Context |
|-|-|-|-|
| 西部戦線 | Western Front | Western Theatre | place |
EOF
mkdir -p "$tmpdir/English/main"
printf 'They marched to the Western Front.\n' > "$tmpdir/English/main/Chapter 1 - First.md"
(cd "$tmpdir" && python3 core/scripts/run_chapter_gates.py --chapter 1)
```

Expected: output ends with `RESULT: ALL PASS`.

- [ ] **Step 3: Run a manual legacy light-novel smoke test**

Run:

```bash
tmpdir="$(mktemp -d)"
cp -R core "$tmpdir/core"
cat > "$tmpdir/novel.config.md" <<'EOF'
# Novel Config

## Chapter-title map

| Vol | N | JP title | EN title |
|-|-|-|-|
| 1 | 1 | 一 | First |
EOF
cat > "$tmpdir/glossary.md" <<'EOF'
| JP | EN | Aliases/Banned | Gender/Context |
|-|-|-|-|
| 西部戦線 | Western Front | Western Theatre | place |
EOF
mkdir -p "$tmpdir/English/Volume 1"
printf 'They marched to the Western Front.\n' > "$tmpdir/English/Volume 1/Chapter 1 - First.md"
(cd "$tmpdir" && python3 core/scripts/run_chapter_gates.py --unit 1 --chapter 1)
```

Expected: output ends with `RESULT: ALL PASS`.

---

## Self-Review

**Spec coverage:** The plan covers the user concern that novels do not necessarily have volumes by introducing a neutral `Unit` model for chapter gates while preserving legacy `Vol` behavior. It deliberately does not claim Unit-only EPUB support; the schema note keeps EPUB builds on the existing volume-based path until a separate build-path change is planned. It covers easier gates by adding one wrapper command that runs the existing three gates. It covers sanitized filenames, ambiguous chapter numbers, Codex skill docs, and Claude Code skill docs.

**Placeholder scan:** No `TBD`, `TODO`, or “write tests later” placeholders are present. Every code-creating task includes concrete code.

**Type consistency:** `ProjectConfig.resolve_chapter(unit, chapter)` returns `ChapterResolution`; tests and `run_chapter_gates.py` use the same names. `ConfigError` is used consistently for config and resolution failures.
