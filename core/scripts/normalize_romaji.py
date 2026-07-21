#!/usr/bin/env python3
# Normalize romanization to the no-macron (wapuro vowel-doubling) convention.
# Strips macrons: o->ou u->uu a->aa i->ii e->ee (e.g. Ootori, Toukyou, Juurou).
# Novel-agnostic: no hardcoded series names.
# Usage: python normalize_romaji.py [--check] file1 file2 ...
#   (no flag) rewrites each file in place; --check reports counts without writing.
import sys, io

sys.stdout.reconfigure(encoding="utf-8")

MACRON = {
    "ā": "aa", "ē": "ee", "ī": "ii", "ō": "ou", "ū": "uu",  # a e i o u
    "Ā": "Aa", "Ē": "Ee", "Ī": "Ii", "Ō": "Ou", "Ū": "Uu",
}
MACRON_CHARS = set(MACRON)


def strip_macrons(s):
    return "".join(MACRON.get(c, c) for c in s)


def normalize(text):
    # Ōtori->Ootori, Fū-kun->Fuu-kun, Fūrinkazan->Fuurinkazan, ...
    return strip_macrons(text)


def main():
    args = sys.argv[1:]
    check = "--check" in args
    files = [a for a in args if a != "--check"]

    if not files:
        print("Usage: python normalize_romaji.py [--check] file1 file2 ...")
        sys.exit(2)

    any_residual = False
    for path in files:
        try:
            with io.open(path, "r", encoding="utf-8") as f:
                orig = f.read()
        except OSError as e:
            print(f"[error] {path}: {e}")
            any_residual = True
            continue

        new = normalize(orig)
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
