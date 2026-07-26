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
import posixpath
import zipfile
import xml.etree.ElementTree as ET

try:
    from PIL import Image
except ImportError:
    Image = None

from harness_config import clean, get_section, parse_bullets, parse_table, split_sections


def _norm_text(value):
    return re.sub(r"\s+", " ", value or "").strip()


def _source_shell(base_dir, source_epub, volume_rows, chapters):
    """Derive reusable front/back matter and package paths from a standard EPUB."""
    if not source_epub or not os.path.isfile(source_epub):
        return {}

    with zipfile.ZipFile(source_epub) as z:
        container = ET.fromstring(z.read("META-INF/container.xml"))
        rootfile = container.find(".//{*}rootfile")
        if rootfile is None:
            return {}
        opf_path = rootfile.attrib["full-path"]
        opf_dir = posixpath.dirname(opf_path)
        opf = ET.fromstring(z.read(opf_path))

        manifest = {}
        nav_href = None
        for item in opf.findall(".//{*}manifest/{*}item"):
            iid, href = item.attrib.get("id"), item.attrib.get("href")
            if iid and href:
                manifest[iid] = href
                if "nav" in item.attrib.get("properties", "").split():
                    nav_href = href
        spine_ids = [
            item.attrib.get("idref")
            for item in opf.findall(".//{*}spine/{*}itemref")
            if item.attrib.get("idref") in manifest
        ]
        if not spine_ids:
            return {}

        def zip_path(href):
            return posixpath.normpath(posixpath.join(opf_dir, href))

        first_body_id = None
        if nav_href and volume_rows:
            nav_path = zip_path(nav_href)
            nav = ET.fromstring(z.read(nav_path))
            first_jp = _norm_text(volume_rows[0].get("jp title", ""))
            for anchor in nav.findall(".//{*}a"):
                if _norm_text("".join(anchor.itertext())) != first_jp:
                    continue
                target = posixpath.normpath(
                    posixpath.join(posixpath.dirname(nav_href),
                                   anchor.attrib.get("href", "").split("#", 1)[0])
                )
                first_body_id = next(
                    (iid for iid, href in manifest.items()
                     if posixpath.normpath(href) == target),
                    None,
                )
                if first_body_id:
                    break

        if not first_body_id:
            # Older EPUB2 packages may expose only NCX navigation. Their
            # hand-filed structural config is preserved by main() below.
            return {}

        fields = {
            "opf_path": opf_path,
            "src_xhtml_prefix": (
                posixpath.dirname(zip_path(manifest[first_body_id])) + "/"
                if first_body_id else None
            ),
            "src_image_prefix": None,
            "src_style_prefix": None,
        }
        image_hrefs = [
            href for href in manifest.values()
            if os.path.splitext(href.lower())[1] in (".jpg", ".jpeg", ".png", ".gif", ".webp")
        ]
        style_hrefs = [href for href in manifest.values() if href.lower().endswith(".css")]
        if image_hrefs:
            fields["src_image_prefix"] = posixpath.dirname(zip_path(image_hrefs[0])) + "/"
        if style_hrefs:
            fields["src_style_prefix"] = posixpath.dirname(zip_path(style_hrefs[0])) + "/"
        fields = {k: v for k, v in fields.items() if v is not None}

        if first_body_id in spine_ids:
            front_ids = spine_ids[:spine_ids.index(first_body_id)]
            # The source's text TOC points at removed JP spine pages. Keep the
            # localized image TOC and rely on the newly generated English nav.
            front_ids = [iid for iid in front_ids if not iid.endswith("toc-002")]
            # Retain image pages and the caution page. Untranslated recap/prose
            # pages are replaced only when they have an English chapter entry.
            front_ids = [
                iid for iid in front_ids
                if "caution" in iid.lower()
                or b"<img" in z.read(zip_path(manifest[iid])).lower()
                or b"<svg" in z.read(zip_path(manifest[iid])).lower()
            ]
            fields["front_matter"] = [
                {"id": iid, "source": zip_path(manifest[iid]), "href": manifest[iid]}
                for iid in front_ids
            ]
            caution = next((iid for iid in front_ids if "caution" in iid.lower()), None)
            if caution:
                fields["caution_page_id"] = caution

        back_ids = [
            iid for iid in spine_ids
            if re.search(r"(?:allcover|colophon|bookwalker)", iid, re.IGNORECASE)
        ]
        if back_ids:
            fields["back_matter"] = [
                {"id": iid, "source": zip_path(manifest[iid]), "href": manifest[iid]}
                for iid in back_ids
            ]

        if fields.get("src_xhtml_prefix") and fields.get("src_image_prefix"):
            chapter_dir = fields["src_xhtml_prefix"]
            image_dir = fields["src_image_prefix"]
            fields["img_href_base"] = posixpath.relpath(
                image_dir, chapter_dir.rstrip("/")
            ).rstrip("/") + "/"
        if fields.get("src_xhtml_prefix") and fields.get("src_style_prefix"):
            chapter_dir = fields["src_xhtml_prefix"]
            style_dir = fields["src_style_prefix"]
            rel_style = posixpath.relpath(style_dir, chapter_dir.rstrip("/")).rstrip("/") + "/"
            fields["css_links"] = [rel_style + os.path.basename(href) for href in style_hrefs]
            fields["css_links"].append(rel_style + "english.css")

        toc = []
        front = fields.get("front_matter", [])
        if front:
            toc.append({"label": "Cover", "href": front[0]["href"]})
            contents = next(
                (p for p in front if re.search(r"(?:toc|contents)", p["id"], re.IGNORECASE)),
                None,
            )
            if contents:
                toc.append({"label": "Contents", "href": contents["href"]})
        chapter_prefix = posixpath.relpath(
            fields.get("src_xhtml_prefix", "item/xhtml/"),
            posixpath.dirname(opf_path) or ".",
        ).rstrip("/") + "/"
        for ch in chapters:
            toc.append({"label": ch["title"], "href": chapter_prefix + ch["id"] + ".xhtml"})
        colophon = next(
            (p for p in fields.get("back_matter", []) if "colophon" in p["id"].lower()),
            None,
        )
        if colophon:
            toc.append({"label": "Colophon", "href": colophon["href"]})
        if toc:
            fields["toc"] = toc

        return fields


def _localized_swaps(base_dir, volume, source_epub):
    """Select spec-backed, geometry-compatible localized images by source stem."""
    localized_dir = os.path.join(base_dir, "English", "Volume %d" % volume,
                                 "localized-images")
    specs_dir = os.path.join(base_dir, "Editing", "Volume %d" % volume,
                             "image-localization")
    if not os.path.isdir(localized_dir) or not os.path.isdir(specs_dir) or Image is None:
        return {}

    spec_stems = set()
    for root, _dirs, names in os.walk(specs_dir):
        for name in names:
            if name.lower().endswith(".md"):
                spec_stems.add(os.path.splitext(name)[0])

    local_by_stem = {}
    for name in os.listdir(localized_dir):
        stem, ext = os.path.splitext(name)
        if ext.lower() in (".png", ".jpg", ".jpeg"):
            local_by_stem.setdefault(stem, os.path.join(localized_dir, name))

    swaps = {}
    retained = {"cover", "allcover-001", "i-bookwalker", "s-h3"}
    with zipfile.ZipFile(source_epub) as z:
        source_images = {}
        for name in z.namelist():
            stem, ext = os.path.splitext(os.path.basename(name))
            if ext.lower() in (".png", ".jpg", ".jpeg", ".gif", ".webp"):
                source_images.setdefault(stem, []).append(name)
        for stem in sorted(spec_stems & set(local_by_stem) & set(source_images)):
            if stem in retained or len(source_images[stem]) != 1:
                continue
            try:
                with Image.open(io.BytesIO(z.read(source_images[stem][0]))) as src_im:
                    sw, sh = src_im.size
                with Image.open(local_by_stem[stem]) as loc_im:
                    lw, lh = loc_im.size
            except Exception:
                continue
            src_ratio = float(sw) / sh
            loc_ratio = float(lw) / lh
            if abs(loc_ratio / src_ratio - 1.0) > 0.02:
                continue
            swaps[stem] = [sw, sh]
    if not swaps:
        return {}
    return {
        "localized_images_dir": localized_dir,
        "image_swaps": swaps,
    }


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

    volume_rows = []
    chapters = []
    missing = []
    for row in chapter_table:
        if clean(row.get("vol", "")) != vol_str:
            continue
        volume_rows.append(row)
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

    result = {
        "source_epub": source_epub,
        "chapters_dir": chapters_dir,
        "out_epub": out_epub,
        "metadata": metadata,
        "chapters": chapters,
    }
    result.update(_source_shell(base_dir, source_epub, volume_rows, chapters))
    result.update(_localized_swaps(base_dir, volume, source_epub))
    return result


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

    existing = {}
    if os.path.isfile(out_path):
        try:
            with io.open(out_path, "r", encoding="utf-8") as f:
                existing = json.load(f)
        except (ValueError, OSError):
            existing = {}
    # Preserve hand-filed per-chapter build-only overrides (for example,
    # booklet image sequences or an appended translated insert) while
    # refreshing the title-map fields.
    old_chapters = {
        ch.get("id"): ch for ch in existing.get("chapters", [])
        if isinstance(ch, dict) and ch.get("id")
    }
    if old_chapters:
        merged_chapters = []
        for chapter in config.get("chapters", []):
            merged = dict(old_chapters.get(chapter.get("id"), {}))
            merged.update(chapter)
            merged_chapters.append(merged)
        config["chapters"] = merged_chapters

    # Preserve hand-filed per-volume structural overrides while refreshing all
    # values that can be derived from novel.config.md and the source package.
    existing.update(config)

    with io.open(out_path, "w", encoding="utf-8") as f:
        json.dump(existing, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print("wrote %s (%d chapters)" % (out_path, len(config["chapters"])))
    sys.exit(0)


if __name__ == "__main__":
    main()
