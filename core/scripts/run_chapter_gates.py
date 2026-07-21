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
