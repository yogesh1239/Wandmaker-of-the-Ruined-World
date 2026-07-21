#!/usr/bin/env python3
# Deterministic consistency gate: cross-checks translated chapter text against
# glossary.md (schema: core/schemas/glossary-schema.md) for banned aliases,
# name drift, honorific mismatches, and stray macrons.
# Usage:
#   python check_consistency.py --glossary glossary.md chapter1.md chapter2.md
#   python check_consistency.py --glossary glossary.md --all English/Volume 1
import argparse
import difflib
import io
import os
import re
import sys

HONORIFICS = ["san", "kun", "chan", "sama", "sensei", "senpai", "dono"]
MACRON_CHARS = "āēīōūĀĒĪŌŪ"
DRIFT_RATIO = 0.86  # ponytail: difflib ratio 0.86 heuristic — tune threshold if false positives appear in production


def parse_glossary(path):
    with io.open(path, "r", encoding="utf-8") as f:
        text = f.read()

    entries = []
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.split("|")]
        # split("|") on a "|a|b|c|" style row yields a leading/trailing "" — drop them.
        if cells and cells[0] == "":
            cells = cells[1:]
        if cells and cells[-1] == "":
            cells = cells[:-1]
        if len(cells) < 2:
            continue
        if cells[0].lower() == "jp":
            continue  # header row
        if all(re.fullmatch(r"-+", c) for c in cells):
            continue  # alignment row, e.g. |-|-|-|-|

        jp = cells[0]
        en = cells[1]
        aliases_raw = cells[2] if len(cells) > 2 else ""
        aliases = [a.strip() for a in aliases_raw.split(",") if a.strip()]
        entries.append({"jp": jp, "en": en, "aliases": aliases})
    return entries


def honorific_split(en):
    m = re.match(r"^(.+)-(%s)$" % "|".join(HONORIFICS), en)
    if m:
        return m.group(1), m.group(2)
    return None


def check_file(path, entries, violations):
    with io.open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    known_terms = set()
    for e in entries:
        known_terms.add(e["en"])
        known_terms.update(e["aliases"])

    for lineno, line in enumerate(lines, start=1):
        # (1) banned-alias hit: case-insensitive whole-word/phrase match.
        for e in entries:
            for alias in e["aliases"]:
                pattern = r"\b%s\b" % re.escape(alias)
                m = re.search(pattern, line, re.IGNORECASE)
                if m:
                    violations.append(
                        "%s:%d: banned alias %r used (glossary requires %r)"
                        % (path, lineno, m.group(0), e["en"])
                    )

        # (2) name-drift: capitalized tokens close to (but not equal to) a glossary EN name.
        for tok_m in re.finditer(r"\b[A-Z][a-z]+\b", line):
            token = tok_m.group(0)
            if token in known_terms:
                continue
            for e in entries:
                name = e["en"]
                if token == name:
                    continue
                ratio = difflib.SequenceMatcher(None, token, name).ratio()
                if ratio >= DRIFT_RATIO:
                    violations.append(
                        "%s:%d: possible name drift %r (close to glossary name %r)"
                        % (path, lineno, token, name)
                    )
                    break

        # (3) honorific mismatch: glossary "Base-honorific" vs "Base-<other honorific>" in text.
        for e in entries:
            split = honorific_split(e["en"])
            if not split:
                continue
            base, honorific = split
            pattern = r"\b%s-(%s)\b" % (re.escape(base), "|".join(HONORIFICS))
            for m in re.finditer(pattern, line):
                if m.group(1) != honorific:
                    violations.append(
                        "%s:%d: honorific mismatch %r (glossary specifies %r)"
                        % (path, lineno, m.group(0), e["en"])
                    )

        # (4) macron characters.
        for ch in line:
            if ch in MACRON_CHARS:
                violations.append(
                    "%s:%d: macron character %r found (romanize with vowel-doubling instead)"
                    % (path, lineno, ch)
                )


def collect_files(all_dir):
    files = []
    for root, _dirs, names in os.walk(all_dir):
        for name in names:
            if name.endswith(".md"):
                files.append(os.path.join(root, name))
    return sorted(files)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--glossary", required=True)
    parser.add_argument("--all", metavar="DIR")
    parser.add_argument("chapters", nargs="*")
    args = parser.parse_args()

    entries = parse_glossary(args.glossary)

    files = collect_files(args.all) if args.all else args.chapters
    if not files:
        print("no chapter files given")
        sys.exit(2)

    violations = []
    for path in files:
        check_file(path, entries, violations)

    for v in violations:
        print(v)

    sys.exit(1 if violations else 0)


if __name__ == "__main__":
    main()
