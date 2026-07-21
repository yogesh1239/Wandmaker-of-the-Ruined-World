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
