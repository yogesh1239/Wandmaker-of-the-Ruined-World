#!/usr/bin/env python3
# Normalize romanization to the no-macron convention in novel.config.md.
# Projects may double Japanese long vowels or leave them unmarked.
# Novel-agnostic: no hardcoded series names or terms.
# Usage: python normalize_romaji.py [--check] file1 file2 ...
#   (no flag) rewrites each file in place; --check reports counts without writing.
import sys, io
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

DOUBLED = {
    "ā": "aa", "ē": "ee", "ī": "ii", "ō": "ou", "ū": "uu",  # a e i o u
    "Ā": "Aa", "Ē": "Ee", "Ī": "Ii", "Ō": "Ou", "Ū": "Uu",
}
UNMARKED = {
    "ā": "a", "ē": "e", "ī": "i", "ō": "o", "ū": "u",
    "Ā": "A", "Ē": "E", "Ī": "I", "Ō": "O", "Ū": "U",
}
MACRON_CHARS = set(DOUBLED)


def configured_mapping():
    try:
        config = Path("novel.config.md").read_text(encoding="utf-8").lower()
    except OSError:
        return DOUBLED

    for line in config.splitlines():
        if "romanization" not in line:
            continue
        if "unmarked" in line or "no long-vowel doubling" in line:
            return UNMARKED
        if "vowel-doubling" in line or "vowel doubling" in line:
            return DOUBLED
    return DOUBLED


def normalize(text, mapping):
    return "".join(mapping.get(c, c) for c in text)


def main():
    args = sys.argv[1:]
    check = "--check" in args
    files = [a for a in args if a != "--check"]

    if not files:
        print("Usage: python normalize_romaji.py [--check] file1 file2 ...")
        sys.exit(2)

    any_residual = False
    mapping = configured_mapping()
    for path in files:
        try:
            with io.open(path, "r", encoding="utf-8") as f:
                orig = f.read()
        except OSError as e:
            print(f"[error] {path}: {e}")
            any_residual = True
            continue

        new = normalize(orig, mapping)
        residual_macrons = sum(orig.count(c) for c in MACRON_CHARS)

        if check:
            after_macrons = sum(new.count(c) for c in MACRON_CHARS)
            if residual_macrons:
                any_residual = True
            print(f"[check] {path}: macrons {residual_macrons}->{after_macrons}")
            continue

        if new != orig:
            with io.open(path, "w", encoding="utf-8") as f:
                f.write(new)
            print(f"[fixed] {path}: stripped {residual_macrons} macron-chars")
        else:
            print(f"[clean] {path}: nothing to change")

    # In --check mode, exit non-zero if any macrons remain (use as a build gate).
    if check and any_residual:
        sys.exit(1)


if __name__ == "__main__":
    main()
