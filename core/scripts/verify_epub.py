#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify a built English EPUB against the EPUB build gates.

Novel-agnostic and config-driven: chapter ids and (optional) image-swap dims
come from the same build config JSON used by build_epub.py.

Gates checked:
  1. zip integrity; mimetype is the FIRST entry and STORED; correct content.
  2. container -> opf resolves; all manifest hrefs exist; all spine idrefs are
     in the manifest; nav reachable; spine page-progression-direction="ltr";
     dc:language + dc:title present.
  3. every <img src> in every xhtml resolves to a packaged file.
  4. zero macrons (a e i o u with macrons) anywhere in chapter docs.
  5. zero untranslated CJK in story PROSE (outside the notes section). The
     '・' interpunct bullet and JP terms cited inside the Translator's Notes
     section are benign and reported SEPARATELY, not failed.
  6. popup footnotes paired: every [^N] noteref has a matching
     <aside epub:type="footnote"> and vice-versa; targets resolve both ways.
  7. (optional) swapped images present at the configured pixel dimensions.

Usage:
  python verify_epub.py --config <config.json> [--epub <built.epub>]
  python verify_epub.py --epub <built.epub> [--chapter-ids chapter-1,chapter-2]
"""

import io
import os
import re
import sys
import json
import zipfile
import shutil
import argparse
import subprocess

sys.stdout.reconfigure(encoding="utf-8")

try:
    from PIL import Image
except ImportError:
    Image = None

# CJK / kana ranges (Hiragana, Katakana, CJK ideographs, halfwidth kana).
CJK = re.compile(r"[぀-ヿ㐀-䶿一-鿿ｦ-ﾟ]")
MACRONS = "āēīōūĀĒĪŌŪ"
INTERPUNCT = "・"

fails = []


def check(name, ok, detail=""):
    print(("PASS" if ok else "FAIL"), "-", name, ("| " + detail if detail else ""))
    if not ok:
        fails.append(name)


def load_config(path):
    with open(path, encoding="utf-8") as f:
        cfg = json.load(f)
    base = os.path.dirname(os.path.abspath(path))
    for key in ("source_epub", "out_epub"):
        if cfg.get(key) and not os.path.isabs(cfg[key]):
            cfg[key] = os.path.normpath(os.path.join(base, cfg[key]))
    return cfg


def main():
    ap = argparse.ArgumentParser(description="Verify a built English EPUB.")
    ap.add_argument("--config", "-c", default=None, help="build config JSON")
    ap.add_argument("--epub", "-e", default=None, help="path to the built .epub")
    ap.add_argument("--chapter-ids", default=None,
                    help="comma-separated chapter xhtml stems (if no config)")
    args = ap.parse_args()

    cfg = load_config(args.config) if args.config else {}
    out = args.epub or cfg.get("out_epub")
    if not out:
        sys.exit("ERROR: provide --epub or a --config with out_epub")
    if not os.path.exists(out):
        sys.exit("ERROR: built epub not found: %s" % out)

    # chapter ids (xhtml stems)
    if args.chapter_ids:
        chapter_ids = [c.strip() for c in args.chapter_ids.split(",") if c.strip()]
    elif cfg.get("chapters"):
        chapter_ids = [c["id"] for c in cfg["chapters"]]
    else:
        chapter_ids = None  # auto-detect below

    z = zipfile.ZipFile(out)
    names = z.namelist()
    nameset = set(names)

    # 1. integrity + mimetype
    check("1a zip integrity", z.testzip() is None)
    first = z.infolist()[0]
    check("1b mimetype first", first.filename == "mimetype")
    check("1c mimetype stored", first.compress_type == zipfile.ZIP_STORED)
    check("1d mimetype content", z.read("mimetype") == b"application/epub+zip")
    cont = z.read("META-INF/container.xml").decode("utf-8")
    opf_path = re.search(r'full-path="([^"]+)"', cont).group(1)
    check("1e container->opf", opf_path in nameset, opf_path)

    # 2. manifest / spine
    opf = z.read(opf_path).decode("utf-8")
    opf_dir = os.path.dirname(opf_path)
    items = dict(re.findall(r'<item [^>]*id="([^"]+)"[^>]*href="([^"]+)"', opf))
    missing_href = [h for h in items.values()
                    if (opf_dir + "/" + h).replace("\\", "/") not in nameset]
    check("2a all manifest hrefs exist", not missing_href, str(missing_href[:5]))
    spine_ids = re.findall(r'idref="([^"]+)"', opf)
    missing_spine = [s for s in spine_ids if s not in items]
    check("2b all spine idrefs in manifest", not missing_spine, str(missing_spine))
    nav_href = re.search(r'<item [^>]*properties="[^"]*nav[^"]*"[^>]*href="([^"]+)"', opf)
    nav_full = (opf_dir + "/" + nav_href.group(1)).replace("\\", "/") if nav_href else None
    check("2c nav reachable", bool(nav_full) and nav_full in nameset, str(nav_full))
    check("2d spine ltr", 'page-progression-direction="ltr"' in opf)
    check("2e dc:language present", "<dc:language>" in opf)
    check("2f title set", "<dc:title" in opf)

    # auto-detect chapter docs if not given: spine xhtml that carry an <h1> and notes/prose
    xhtml_dir_files = [n for n in names if n.endswith(".xhtml")]

    def read(n):
        return z.read(n).decode("utf-8", errors="replace")

    if chapter_ids is None:
        chapter_files = [n for n in xhtml_dir_files
                         if '<body class="chapter"' in read(n)]
    else:
        chapter_files = []
        for cid in chapter_ids:
            href = items.get(cid)
            if href:
                chapter_files.append((opf_dir + "/" + href).replace("\\", "/"))
            else:
                hits = [n for n in xhtml_dir_files if n.rsplit("/", 1)[-1] == cid + ".xhtml"]
                chapter_files.extend(hits)
    chapter_files = [n for n in chapter_files if n in nameset]
    check("2g chapter docs located", bool(chapter_files), "%d found" % len(chapter_files))

    # 3. all <img src> resolve
    img_problems = []
    for n in xhtml_dir_files:
        t = read(n)
        for src in re.findall(r'<img[^>]*src="([^"]+)"', t):
            full = os.path.normpath(os.path.join(os.path.dirname(n), src)).replace("\\", "/")
            if full not in nameset:
                img_problems.append((n.split("/")[-1], src))
    check("3 all <img src> resolve", not img_problems, str(img_problems[:5]))

    # 4. zero macrons in chapter docs
    macron_hits = {}
    for n in chapter_files:
        t = read(n)
        found = "".join(sorted({c for c in t if c in MACRONS}))
        if found:
            macron_hits[n.split("/")[-1]] = found
    check("4 zero macrons in chapter docs", not macron_hits, str(macron_hits))

    # 5. CJK in prose vs. notes
    prose_hits, notes_hits, interpunct = {}, {}, {}
    for n in chapter_files:
        t = read(n)
        mm = re.search(r'<section class="notes">', t)
        prose = t[:mm.start()] if mm else t
        notes = t[mm.start():] if mm else ""
        p = [c for c in CJK.findall(prose) if c != INTERPUNCT]
        if p:
            prose_hits[n.split("/")[-1]] = "".join(sorted(set(p)))
        ip = prose.count(INTERPUNCT)
        if ip:
            interpunct[n.split("/")[-1]] = ip
        nh = CJK.findall(notes)
        if nh:
            notes_hits[n.split("/")[-1]] = "".join(sorted(set(nh)))
    check("5 zero untranslated CJK in story prose", not prose_hits, str(prose_hits))
    print("INFO benign '・' interpunct per chapter:", interpunct)
    print("INFO Translator's-Notes JP citations (expected, benign):", list(notes_hits.keys()))

    # 6. popup footnotes paired
    fn_ok, detail = True, []
    for n in chapter_files:
        t = read(n)
        # ids look like fnref-<chid>-<num> and fn-<chid>-<num>
        refs = set(re.findall(r'<a epub:type="noteref"[^>]*id="fnref-[^"]*-(\d+)"', t))
        notes = set(re.findall(r'<aside epub:type="footnote" id="fn-[^"]*-(\d+)"', t))
        href_targets = set(re.findall(r'href="#fn-[^"]*-(\d+)"', t))
        back_targets = set(re.findall(r'href="#fnref-[^"]*-(\d+)"', t))
        base = n.split("/")[-1]
        if refs != notes:
            fn_ok = False
            detail.append("%s refs!=notes %s vs %s" % (base, sorted(refs), sorted(notes)))
        if href_targets - notes:
            fn_ok = False
            detail.append("%s noteref->missing fn %s" % (base, href_targets - notes))
        if back_targets - refs:
            fn_ok = False
            detail.append("%s backref->missing fnref %s" % (base, back_targets - refs))
    check("6 popup footnotes paired", fn_ok, "; ".join(detail))

    # 6b. namespaces on chapter docs
    ns_ok = all('xmlns="http://www.w3.org/1999/xhtml"' in read(n)
                and 'xmlns:epub="http://www.idpf.org/2007/ops"' in read(n)
                for n in chapter_files)
    check("6b chapter <html> declares both namespaces", ns_ok)

    # 7. optional swapped-image dimension check
    swaps = cfg.get("image_swaps", {})
    if swaps:
        if Image is None:
            check("7 swapped image dims", False, "Pillow not installed")
        else:
            img_prefix = next((n.rsplit("/", 1)[0] + "/" for n in names
                               if re.search(r"/(image|images)/", n) and n.endswith(".jpg")),
                              "item/image/")
            dims_ok, dd = True, []
            for stem, (w, h) in swaps.items():
                key = "%s%s.jpg" % (img_prefix, stem)
                if key not in nameset:
                    dims_ok = False
                    dd.append("%s missing" % stem)
                    continue
                im = Image.open(io.BytesIO(z.read(key)))
                if im.size != (w, h):
                    dims_ok = False
                    dd.append("%s=%s want %s" % (stem, im.size, (w, h)))
            check("7 swapped images at configured dims", dims_ok, "; ".join(dd))

    # 8. epubcheck if available
    ec = shutil.which("epubcheck")
    if ec:
        r = subprocess.run([ec, out], capture_output=True, text=True)
        print("epubcheck rc=%d\n%s\n%s" % (r.returncode, r.stdout[-1500:], r.stderr[-400:]))
    else:
        print("INFO epubcheck not on PATH - not run")

    print("\nSPINE ORDER:")
    for s in spine_ids:
        print("  ", s, "->", items.get(s))
    print("\nRESULT:", "ALL PASS" if not fails else ("FAILURES: " + ", ".join(fails)))
    sys.exit(0 if not fails else 1)


if __name__ == "__main__":
    main()
