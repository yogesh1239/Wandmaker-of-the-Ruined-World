#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Derive the JSON `build_epub.py --config` needs from `novel.config.md`.

Bridges the per-novel knob file (schema: core/schemas/novel-config-schema.md)
to the build config that build_epub.py's docstring documents. Reads, for the
requested volume: the source-ebook -> volume map, the chapter-title map, the
EPUB metadata block, and the Identity block; cross-checks the title-mapped
chapters against what's actually assembled under English/Volume N/.

A chapter whose title carries a Windows-illegal char is filed under a sanitized
name, so its exact title-derived filename is absent; derive then falls back to a
`Chapter <N> - *.md` glob (matched by number). An ambiguous glob (>1 match) is
fatal (exit 2). Chapters listed in the map but missing on disk are dropped with
a warning to stderr (not fatal); zero surviving chapters is fatal (exit 2).

Usage:
  python derive_build_config.py novel.config.md --volume 1 [--out out.json]

Default --out: <config-dir>/Editing/Volume N/build_config.json
"""

import io
import os
import re
import sys
import json
import glob
import uuid
import argparse

from harness_config import clean, get_section, parse_bullets, parse_table, split_sections


def derive(config_path, volume):
    base_dir = os.path.dirname(os.path.abspath(config_path))
    with io.open(config_path, "r", encoding="utf-8") as f:
        text = f.read()
    sections = split_sections(text)

    identity = parse_bullets(get_section(sections, "identity"))
    source_table = parse_table(get_section(sections, "source ebooks"))
    chapter_table = parse_table(get_section(sections, "chapter-title map"))
    epub_meta = parse_bullets(get_section(sections, "epub metadata"))

    vol_str = str(volume)

    source_epub = None
    for row in source_table:
        if clean(row.get("vol", "")) == vol_str:
            source_file = clean(row.get("source file", ""))
            if source_file:
                source_epub = os.path.join(base_dir, source_file)
            break

    chapters_dir = os.path.join(base_dir, "English", "Volume %d" % volume)

    chapters = []
    missing = []
    for row in chapter_table:
        if clean(row.get("vol", "")) != vol_str:
            continue
        n = clean(row.get("n", ""))
        title = clean(row.get("en title", ""))
        if not n or not title:
            continue
        md_name = "Chapter %s - %s.md" % (n, title)
        md_path = os.path.join(chapters_dir, md_name)
        if os.path.isfile(md_path):
            chapters.append({"id": "chapter-%s" % n, "md": md_name, "title": title})
            continue
        # A title carrying a Windows-illegal char (< > : " / \ | ? *) is filed
        # under a sanitized name, so the exact title-derived name is absent.
        # Fall back to matching by chapter number. The literal " - " after the
        # number keeps "Chapter 1 - *.md" from also matching "Chapter 10 - ...".
        matches = sorted(glob.glob(os.path.join(chapters_dir, "Chapter %s - *.md" % n)))
        if len(matches) == 1:
            chapters.append({"id": "chapter-%s" % n,
                             "md": os.path.basename(matches[0]), "title": title})
        elif len(matches) > 1:
            names = ", ".join(os.path.basename(m) for m in matches)
            print("error: chapter %s (%r) matches multiple files on disk: %s -- "
                  "cannot pick one; rename so exactly one 'Chapter %s - *.md' remains"
                  % (n, title, names, n), file=sys.stderr)
            sys.exit(2)
        else:
            missing.append((n, title, md_path))

    for n, title, md_path in missing:
        print("warning: chapter %s (%r) not found on disk, expected %s -- excluded"
              % (n, title, md_path), file=sys.stderr)

    if not chapters:
        print("error: zero chapters found on disk for volume %d" % volume, file=sys.stderr)
        return None

    series = epub_meta.get("series", "")
    title_pattern = epub_meta.get("title pattern", "")
    title = re.sub(r"\bN\b", vol_str, title_pattern) if title_pattern else ""
    language = epub_meta.get("language", "en") or "en"
    author = identity.get("author", "")

    metadata = {
        "title": title,
        "language": language,
        "identifier": "urn:uuid:%s" % uuid.uuid4(),
        "creators": [{"name": author, "role": "aut"}] if author else [],
    }

    out_name = ("%s v%02d (EN).epub" % (series, volume)) if series else ("Volume %d (EN).epub" % volume)
    out_epub = os.path.join(base_dir, "English", out_name)

    return {
        "source_epub": source_epub,
        "chapters_dir": chapters_dir,
        "out_epub": out_epub,
        "metadata": metadata,
        "chapters": chapters,
    }


def main():
    ap = argparse.ArgumentParser(
        description="Derive build_config.json for build_epub.py from novel.config.md")
    ap.add_argument("config", help="path to novel.config.md")
    ap.add_argument("--volume", "-v", type=int, required=True)
    ap.add_argument("--out", "-o", default=None, help="output JSON path")
    args = ap.parse_args()

    config = derive(args.config, args.volume)
    if config is None:
        sys.exit(2)

    out_path = args.out
    if not out_path:
        base_dir = os.path.dirname(os.path.abspath(args.config))
        out_path = os.path.join(base_dir, "Editing", "Volume %d" % args.volume, "build_config.json")

    out_dir = os.path.dirname(os.path.abspath(out_path))
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    with io.open(out_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print("wrote %s (%d chapters)" % (out_path, len(config["chapters"])))
    sys.exit(0)


if __name__ == "__main__":
    main()
