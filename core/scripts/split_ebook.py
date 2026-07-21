#!/usr/bin/env python3
"""Split a Japanese light-novel ebook into per-chapter markdown + images.

Novel-agnostic. Two front-ends feed one shared XHTML->markdown splitter:

  .epub  -> read the zip's XHTML directly.
  .azw3  -> unpack with vendored KindleUnpack first (KF8 HTML with ruby intact),
            then feed the same splitter. NO Calibre fallback (Calibre conversion
            can flatten furigana).

Furigana is preserved for all formats:
  <ruby>漢字<rt>かな</rt></ruby>  ->  漢字[かな]
Square brackets are used deliberately so the readings never collide with the
（）/ 《》 thought markers used downstream in translation.

Inline images become  ![filename](images/filename)  and are extracted to images/.

Usage:
  python split_ebook.py <ebook-path> <output-dir> [--volume N]

Output:
  <output-dir>/<chapter>.md ...
  <output-dir>/images/...
If --volume N is given (or the output dir is not already a "Volume N" dir),
output is written under <output-dir>/Volume N/.
"""

import os
import io
import re
import sys
import shutil
import zipfile
import tempfile
import argparse
import importlib
import importlib.util
import contextlib
import traceback
import xml.etree.ElementTree as ET
from pathlib import Path
from collections import OrderedDict

sys.stdout.reconfigure(encoding="utf-8")

IMG_EXTS = (".jpg", ".jpeg", ".png", ".gif", ".svg", ".webp", ".bmp")


# --------------------------------------------------------------------------
# Shared XHTML -> markdown conversion
# --------------------------------------------------------------------------

def ruby_to_furigana(xhtml):
    """Convert <ruby>漢字<rt>かな</rt></ruby> (and rb/rp variants) to 漢字[かな].

    Handles:
      <ruby>漢字<rt>かな</rt></ruby>
      <ruby><rb>漢字</rb><rt>かな</rt></ruby>
      <ruby>漢字<rp>(</rp><rt>かな</rt><rp>)</rp></ruby>
    Groups all base text and all readings within one <ruby> together so that
    multi-character compounds collapse to a single base[reading] pair.
    """
    def repl(m):
        inner = m.group(1)
        # Drop <rp> parenthesis hints entirely.
        inner = re.sub(r"<rp\b[^>]*>.*?</rp>", "", inner, flags=re.DOTALL)
        # Collect the readings, then remove the <rt> elements from the base.
        reading = "".join(re.findall(r"<rt\b[^>]*>(.*?)</rt>", inner, flags=re.DOTALL))
        reading = re.sub(r"<[^>]+>", "", reading).strip()
        base = re.sub(r"<rt\b[^>]*>.*?</rt>", "", inner, flags=re.DOTALL)
        base = re.sub(r"<[^>]+>", "", base).strip()
        if base and reading:
            return f"{base}[{reading}]"
        return base or reading
    return re.sub(r"<ruby\b[^>]*>(.*?)</ruby>", repl, xhtml, flags=re.DOTALL)


def xhtml_to_markdown(xhtml_content, images_dir_name="images"):
    """Convert one XHTML document body to markdown text.

    - Ruby annotations -> 漢字[かな]
    - <img>/<svg><image> -> ![filename](images/filename)
    - Emphasis-dot / bold spans -> **text**
    - Section dividers (◆ / ◇ / ＊) -> ---
    - Paragraphs -> text lines separated by blank lines
    """
    body_match = re.search(r"<body[^>]*>(.*?)</body>", xhtml_content, re.DOTALL)
    content = body_match.group(1) if body_match else xhtml_content

    # 1. Furigana first, while the <ruby>/<rt> structure is still intact.
    content = ruby_to_furigana(content)

    # 2. Images (raster <img>) -> markdown image links.
    def img_to_md(match):
        src = match.group(1)
        filename = src.split("/")[-1]
        return f"\n\n![{filename}]({images_dir_name}/{filename})\n\n"

    content = re.sub(r'<img[^>]*\bsrc="([^"]*)"[^>]*/?>', img_to_md, content)

    # SVG-wrapped images (common full-page illustrations) -> image link.
    def svg_to_md(match):
        src = match.group(1)
        filename = src.split("/")[-1]
        return f"\n\n![{filename}]({images_dir_name}/{filename})\n\n"

    content = re.sub(
        r'<svg[^>]*>.*?<image[^>]*xlink:href="([^"]*)"[^>]*/?>.*?</svg>',
        svg_to_md, content, flags=re.DOTALL,
    )
    content = re.sub(
        r'<svg[^>]*>.*?<image[^>]*\bhref="([^"]*)"[^>]*/?>.*?</svg>',
        svg_to_md, content, flags=re.DOTALL,
    )
    content = re.sub(r"<svg[^>]*>.*?</svg>", "\n", content, flags=re.DOTALL)

    # 3. Emphasis / bold spans -> **bold**.
    content = re.sub(r'<span class="[^"]*em-?dot[^"]*">([^<]+)</span>', r"**\1**", content)
    content = re.sub(r'<span class="[^"]*bold[^"]*">([^<]+)</span>', r"**\1**", content)
    content = re.sub(r"<(b|strong)\b[^>]*>(.*?)</\1>", r"**\2**", content, flags=re.DOTALL)
    content = re.sub(r"<(i|em)\b[^>]*>(.*?)</\1>", r"*\2*", content, flags=re.DOTALL)

    # tcy / vertical spans -> plain text.
    content = re.sub(r'<span class="[^"]*tcy[^"]*">([^<]+)</span>', r"\1", content)

    # 4. Headings -> markdown headings (strip inner tags & furigana brackets so a
    #    title heading stays clean).
    for level in (1, 2, 3, 4):
        prefix = "#" * level

        def heading_replace(match, prefix=prefix):
            inner = match.group(1)
            if "![" in inner:
                return inner
            text = re.sub(r"<[^>]+>", "", inner).strip()
            text = re.sub(r"\[[^\]]*\]", "", text).strip()  # drop furigana readings
            if text:
                return f"\n\n{prefix} {text}\n\n"
            return inner

        content = re.sub(rf"<h{level}[^>]*>(.*?)</h{level}>", heading_replace,
                         content, flags=re.DOTALL)

    # 5. Section dividers.
    content = re.sub(r"<div[^>]*>\s*<p>\s*[◆◇＊*※]\s*</p>\s*</div>", "\n\n---\n\n", content)
    content = re.sub(r"<p[^>]*>\s*[◆◇＊※]{1,5}\s*</p>", "\n\n---\n\n", content)
    content = re.sub(r"<hr\s*/?>", "\n\n---\n\n", content)

    # 6. Paragraphs.
    content = re.sub(r"<p[^>]*>\s*<br\s*/?>\s*</p>", "\n", content)

    def p_to_text(match):
        inner = match.group(1)
        inner = re.sub(r"<br\s*/?>", "\n", inner)
        inner = re.sub(r"<[^>]+>", "", inner)
        inner = inner.strip()
        return inner + "\n\n" if inner else "\n"

    content = re.sub(r"<p[^>]*>(.*?)</p>", p_to_text, content, flags=re.DOTALL)

    # 7. Strip any remaining tags.
    content = re.sub(r"</?(div|span|a|image|section|article|figure|figcaption)[^>]*>",
                     "", content)
    content = re.sub(r"<[^>]+>", "", content)

    # 8. HTML entity cleanup (common ones; keep it light).
    for ent, ch in (("&nbsp;", " "), ("&amp;", "&"), ("&lt;", "<"),
                    ("&gt;", ">"), ("&quot;", '"'), ("&#39;", "'")):
        content = content.replace(ent, ch)

    # 9. Whitespace cleanup.
    content = re.sub(r"\n{4,}", "\n\n\n", content)
    content = "\n".join(line.rstrip() for line in content.split("\n"))
    return content.strip()


def find_image_refs(xhtml_content):
    """All image filenames referenced by an XHTML doc (img src + svg href)."""
    refs = re.findall(r'src="([^"]*)"', xhtml_content)
    refs += re.findall(r'xlink:href="([^"]*)"', xhtml_content)
    refs += re.findall(r'(?<!xlink:)href="([^"]*)"', xhtml_content)
    out, seen = [], set()
    for ref in refs:
        name = ref.split("/")[-1]
        if name.lower().endswith(IMG_EXTS) and name not in seen:
            seen.add(name)
            out.append(name)
    return out


def html_to_plain(fragment):
    text = re.sub(r"<rt\b[^>]*>.*?</rt>", "", fragment, flags=re.DOTALL)
    text = re.sub(r"<[^>]+>", "", text)
    return text.strip()


def detect_chapter_title(xhtml_content):
    """Best-effort chapter title from a heading or a styled title paragraph."""
    patterns = [
        r"<h1[^>]*>(.*?)</h1>",
        r"<h2[^>]*>(.*?)</h2>",
        r"<h3[^>]*>(.*?)</h3>",
        r'<p[^>]*class="[^"]*(?:title|midashi|font-1em)[^"]*"[^>]*>(.*?)</p>',
    ]
    for pat in patterns:
        m = re.search(pat, xhtml_content, re.DOTALL)
        if m:
            text = html_to_plain(m.group(1))
            if text:
                return text

    body = re.search(r"<body[^>]*>(.*?)</body>", xhtml_content, re.DOTALL)
    if not body:
        return None
    plain = html_to_plain(body.group(1))
    for line in re.split(r"[\r\n]+", plain):
        line = line.strip(" 　")
        if not line:
            continue
        if re.match(r"^第[0-9０-９一二三四五六七八九十百千]+[話章節]", line):
            return line
        if line.startswith(("プロローグ", "エピローグ", "序章", "終章")):
            return line
        break
    return None


def sanitize_filename(name):
    safe = re.sub(r'[<>:"/\\|?*]', "", name)
    safe = re.sub(r"\[[^\]]*\]", "", safe)  # drop furigana readings from titles
    safe = safe.strip().rstrip(". ")
    return safe[:80]


def is_non_chapter_page(filename):
    prefixes = ("p-cover", "cover", "p-fmatter", "p-caution", "caution",
                "p-bmatter", "p-allcover", "p-colophon", "colophon",
                "p-toc", "nav", "toc", "p-titlepage", "titlepage")
    base = filename.lower()
    return any(base.startswith(p) for p in prefixes)


def is_non_chapter_content(content):
    m = re.search(r"<body[^>]*>", content)
    if not m:
        return False
    body_tag = m.group()
    classes = ["cover-page", "caution-page", "colophon-page", "info-middle", "info-top"]
    return any(cls in body_tag for cls in classes)


# --------------------------------------------------------------------------
# Front-end: collect ordered (filename, xhtml_text) pages + image bytes
# --------------------------------------------------------------------------

def _opf_spine_pages(opf_text):
    """Return ordered list of (id, href) from an OPF manifest+spine."""
    id_to_href = {}
    for m in re.finditer(r"<item\b[^>]*>", opf_text):
        tag = m.group()
        iid = re.search(r'\bid="([^"]+)"', tag)
        href = re.search(r'\bhref="([^"]+)"', tag)
        if iid and href:
            id_to_href[iid.group(1)] = href.group(1)
    spine = []
    for m in re.finditer(r'idref="([^"]+)"', opf_text):
        iid = m.group(1)
        if iid in id_to_href:
            spine.append((iid, id_to_href[iid]))
    return spine, id_to_href


def _find_nav_doc(root, opf_text, opf_dir):
    """Locate the EPUB3 nav document and/or NCX. Returns (nav_text, ncx_text);
    either may be None. The nav is found via the manifest's properties="nav"
    item, the spine's toc=... NCX idref, or a filename heuristic.
    """
    root = Path(root)
    nav_text = ncx_text = None

    # EPUB3 nav: manifest item with properties containing "nav".
    nav_href = None
    for m in re.finditer(r"<item\b[^>]*>", opf_text):
        tag = m.group()
        if re.search(r'properties="[^"]*\bnav\b[^"]*"', tag):
            h = re.search(r'\bhref="([^"]+)"', tag)
            if h:
                nav_href = h.group(1)
                break
    if nav_href:
        p = (opf_dir / nav_href.split("#")[0]).resolve()
        if p.exists():
            nav_text = p.read_text(encoding="utf-8", errors="replace")

    # NCX: spine toc="id" -> manifest href, else any *.ncx.
    _spine, id_to_href = _opf_spine_pages(opf_text)
    ncx_href = None
    tm = re.search(r"<spine\b[^>]*\btoc=\"([^\"]+)\"", opf_text)
    if tm and tm.group(1) in id_to_href:
        ncx_href = id_to_href[tm.group(1)]
    if not ncx_href:
        for h in id_to_href.values():
            if h.lower().endswith(".ncx"):
                ncx_href = h
                break
    if ncx_href:
        p = (opf_dir / ncx_href).resolve()
        if p.exists():
            ncx_text = p.read_text(encoding="utf-8", errors="replace")

    # Heuristic fallbacks by filename.
    if nav_text is None:
        for cand in root.rglob("*nav*.xhtml"):
            nav_text = cand.read_text(encoding="utf-8", errors="replace")
            break
    if ncx_text is None:
        for cand in root.rglob("*.ncx"):
            ncx_text = cand.read_text(encoding="utf-8", errors="replace")
            break
    return nav_text, ncx_text


def collect_from_zip_dir(root, opf_rel):
    """Given an unpacked-ebook root dir and the OPF path (relative to root),
    return (ordered_pages, images, nav_text, ncx_text) where:
        ordered_pages = [(page_name, xhtml_text), ...]   # spine order
        images        = {filename: bytes}
        nav_text      = the EPUB3 nav document text, or None
        ncx_text      = the NCX text, or None
    Works for both an unzipped .epub and KindleUnpack's mobi8 output dir.
    """
    root = Path(root)
    opf_path = root / opf_rel
    opf_text = opf_path.read_text(encoding="utf-8", errors="replace")
    opf_dir = opf_path.parent

    spine, _ = _opf_spine_pages(opf_text)

    pages = []
    for _iid, href in spine:
        href = href.split("#")[0]
        fpath = (opf_dir / href).resolve()
        if not fpath.exists():
            # try a loose basename match anywhere under root
            cand = list(root.rglob(Path(href).name))
            if not cand:
                continue
            fpath = cand[0]
        try:
            pages.append((fpath.name, fpath.read_text(encoding="utf-8", errors="replace")))
        except OSError:
            continue

    # Fallback: if the spine yielded nothing, take all (x)html in sorted order.
    if not pages:
        for fpath in sorted(root.rglob("*")):
            if fpath.suffix.lower() in (".xhtml", ".html", ".htm"):
                pages.append((fpath.name, fpath.read_text(encoding="utf-8", errors="replace")))

    nav_text, ncx_text = _find_nav_doc(root, opf_text, opf_dir)

    images = {}
    for fpath in root.rglob("*"):
        if fpath.is_file() and fpath.suffix.lower() in IMG_EXTS:
            images[fpath.name] = fpath.read_bytes()
    return pages, images, nav_text, ncx_text


def _find_opf_in_dir(root):
    """Locate the OPF inside an unpacked ebook dir (via container.xml or glob)."""
    root = Path(root)
    container = root / "META-INF" / "container.xml"
    if container.exists():
        m = re.search(r'full-path="([^"]+)"', container.read_text(encoding="utf-8",
                                                                    errors="replace"))
        if m:
            return m.group(1)
    opfs = list(root.rglob("*.opf"))
    if opfs:
        return str(opfs[0].relative_to(root)).replace("\\", "/")
    return None


def load_epub(epub_path):
    """EPUB front-end: unzip to a temp dir, then collect ordered pages + images."""
    tmp = Path(tempfile.mkdtemp(prefix="epub_split_"))
    with zipfile.ZipFile(epub_path) as z:
        z.extractall(tmp)
    opf_rel = _find_opf_in_dir(tmp)
    if not opf_rel:
        shutil.rmtree(tmp, ignore_errors=True)
        raise SystemExit(f"ERROR: no OPF found inside {epub_path}")
    result = collect_from_zip_dir(tmp, opf_rel)
    shutil.rmtree(tmp, ignore_errors=True)
    return result


def _import_kindleunpack():
    """Import the vendored KindleUnpack and return its module exposing unpackBook.

    KindleUnpack's `kindleunpack.py` uses RELATIVE imports
    (`from .compatibility_utils import ...`) and bare sibling imports, so it must
    be imported as a *package member* with its directory on `sys.path` — it
    cannot be loaded as a standalone file (that raises ImportError on the
    relative imports). We put both `scripts/kindleunpack/lib` and
    `scripts/kindleunpack` on sys.path, then try, in order:
      1. `import kindleunpack`        (top-level module / package, common vendor)
      2. `import lib.kindleunpack`    (this repo's layout: kindleunpack/lib/...)
    Returns the module exposing `unpackBook`, or None.
    """
    here = Path(__file__).resolve().parent
    vendor = here / "kindleunpack"
    lib = vendor / "lib"
    # Order matters: lib first so its sibling modules resolve, then the package
    # root so `import lib.kindleunpack` works, then the scripts dir.
    for p in (str(lib), str(vendor), str(here)):
        if p not in sys.path:
            sys.path.insert(0, p)

    for modname in ("kindleunpack", "lib.kindleunpack"):
        try:
            mod = importlib.import_module(modname)
        except Exception:
            continue
        if hasattr(mod, "unpackBook"):
            return mod
    return None


KINDLEUNPACK_HELP = """\
ERROR: azw3 (KF8) extraction requires the vendored KindleUnpack, which was not found.

KindleUnpack is pure Python (NO Calibre) and preserves <ruby> furigana, which a
Calibre conversion can flatten. Install it into scripts/kindleunpack/:

    cd "<this scripts dir>/kindleunpack"
    git clone https://github.com/kevinhendricks/KindleUnpack .

After cloning, this script will import KindleUnpack's `unpackBook` automatically.
Do NOT convert the azw3 with Calibre as a workaround.
"""


def load_azw3(azw3_path):
    """AZW3 front-end: unpack via vendored KindleUnpack -> mobi8 dir -> collect."""
    ku = _import_kindleunpack()
    if ku is None:
        sys.stderr.write(KINDLEUNPACK_HELP)
        raise SystemExit(2)

    tmp = Path(tempfile.mkdtemp(prefix="azw3_split_"))
    # KindleUnpack prints Japanese to stdout; on a cp1252 console that can crash.
    # Redirect its stdout to a UTF-8 buffer for the duration of the call so its
    # prints can never abort the run, then surface the captured log.
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            # Writes a mobi7/ and (for KF8) mobi8/ tree under the out dir.
            ku.unpackBook(str(azw3_path), str(tmp))
    except Exception as e:  # noqa: BLE001
        log = buf.getvalue()
        shutil.rmtree(tmp, ignore_errors=True)
        tb = traceback.format_exc()
        raise SystemExit(
            f"ERROR: KindleUnpack failed on {azw3_path}: {e}\n{tb}\n{log[-2000:]}")

    # Prefer the KF8 (mobi8) output, which carries the ruby-bearing HTML.
    mobi8 = tmp / "mobi8"
    search_root = mobi8 if mobi8.exists() else tmp
    opf_rel = _find_opf_in_dir(search_root)
    if not opf_rel:
        shutil.rmtree(tmp, ignore_errors=True)
        raise SystemExit(f"ERROR: KindleUnpack produced no OPF for {azw3_path}")
    result = collect_from_zip_dir(search_root, opf_rel)
    shutil.rmtree(tmp, ignore_errors=True)
    return result


# --------------------------------------------------------------------------
# Chapter grouping + output
# --------------------------------------------------------------------------

def parse_toc_entries(nav_text, ncx_text):
    """Return ordered [(title, href_basename), ...] from the navigation.

    Prefers the EPUB3 primary nav (the single <nav epub:type="toc">), ignoring
    the landmarks/guide nav whose duplicate 表紙/目次/本文 entries point at the
    same early pages and otherwise corrupt chapter boundaries. Falls back to the
    NCX <navMap>. As a final guard, drops any entry whose target page basename
    was already used by an earlier entry (the landmarks-duplicate symptom).
    """
    entries = []

    if nav_text:
        # Isolate ONLY the epub:type="toc" nav. If we can't, take the FIRST <nav>.
        m = re.search(r'<nav\b[^>]*epub:type="[^"]*\btoc\b[^"]*"[^>]*>(.*?)</nav>',
                      nav_text, re.DOTALL)
        if not m:
            m = re.search(r"<nav\b[^>]*>(.*?)</nav>", nav_text, re.DOTALL)
        if m:
            block = m.group(1)
            for a in re.finditer(r'<a\b[^>]*href="([^"]+)"[^>]*>(.*?)</a>',
                                 block, re.DOTALL):
                href = a.group(1)
                title = html_to_plain(a.group(2))
                if title:
                    entries.append((title, href))

    if not entries and ncx_text:
        # NCX <navPoint><navLabel><text>..</text></navLabel><content src=".."/>
        for np in re.finditer(r"<navPoint\b.*?</navPoint>", ncx_text, re.DOTALL):
            block = np.group()
            tm = re.search(r"<text\b[^>]*>(.*?)</text>", block, re.DOTALL)
            sm = re.search(r'<content\b[^>]*src="([^"]+)"', block)
            if tm and sm:
                title = html_to_plain(tm.group(1))
                if title:
                    entries.append((title, sm.group(1)))

    # Normalize to (title, basename-without-anchor) and dedupe by target page.
    out, seen_pages = [], set()
    for title, href in entries:
        base = href.split("#")[0].split("/")[-1]
        if not base or base in seen_pages:
            continue
        seen_pages.add(base)
        out.append((title, base))
    return out


def group_into_chapters(pages, nav_text=None, ncx_text=None):
    """Group ordered spine pages into chapters using the navigation TOC.

    Each TOC entry's target page marks a chapter start at its spine index; the
    chapter spans up to (but not including) the next TOC entry's start page. One
    .md is emitted per TOC entry, in spine order. Falls back to a single group
    only if the navigation is entirely unusable.
    """
    spine_names = [name for name, _text in pages]
    index_by_name = {name: i for i, name in enumerate(spine_names)}
    text_by_index = {i: text for i, (_name, text) in enumerate(pages)}

    toc = parse_toc_entries(nav_text, ncx_text)

    # Map each TOC target page basename -> its spine index (skip ones absent
    # from the spine), keeping spine order.
    starts = []
    for title, base in toc:
        idx = index_by_name.get(base)
        if idx is None:
            continue
        starts.append((idx, title))
    starts.sort(key=lambda t: t[0])

    if not starts:
        # No usable nav: degrade to one group rather than mis-splitting.
        return [{"title": "本文", "pages": list(pages)}]

    groups = []
    for k, (start_idx, title) in enumerate(starts):
        end_idx = starts[k + 1][0] if k + 1 < len(starts) else len(spine_names)
        page_range = [(spine_names[i], text_by_index[i])
                      for i in range(start_idx, end_idx)]
        groups.append({"title": title, "pages": page_range, "spine_index": start_idx})
    return groups


def resolve_output_dir(output_dir, volume):
    out = Path(output_dir)
    if volume is not None:
        if out.name.lower().startswith("volume"):
            return out
        return out / f"Volume {volume}"
    return out


def write_chapters(groups, images, out_dir):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    images_dir = out_dir / "images"
    images_dir.mkdir(exist_ok=True)

    # Clear stale outputs.
    for old in out_dir.glob("*.md"):
        old.unlink()
    for old in images_dir.glob("*"):
        if old.is_file():
            old.unlink()

    for name, data in images.items():
        (images_dir / name).write_bytes(data)
    print(f"Extracted {len(images)} images -> {images_dir}")

    used, created = {}, 0
    for i, chapter in enumerate(groups, start=1):
        title = chapter["title"]
        safe = sanitize_filename(title) or f"chapter_{i:02d}"
        # 2-digit spine-order prefix so files sort in reading order, e.g.
        # "05 一章 聖珠継承 Holy Orb.md".
        prefix = f"{i:02d}"
        stem = f"{prefix} {safe}"
        if stem in used:
            used[stem] += 1
            stem = f"{stem}_{used[stem]}"
        else:
            used[stem] = 1

        body_parts = []
        for _pname, text in chapter["pages"]:
            md = xhtml_to_markdown(text, "images")
            if md:
                body_parts.append(md)

        compact = re.sub(r"[\s　#]+", "", "\n".join(body_parts))
        if not compact:
            print(f"  Skipped (empty): {stem}.md")
            continue

        final_md = "\n\n".join(p.strip() for p in body_parts if p.strip()).strip() + "\n"
        (out_dir / f"{stem}.md").write_text(final_md, encoding="utf-8")
        print(f"  Created: {stem}.md ({len(chapter['pages'])} pages)")
        created += 1

    print(f"\nDone! {created} chapter file(s) in: {out_dir}")
    return created


def split_ebook(ebook_path, output_dir, volume=None):
    ebook_path = Path(ebook_path)
    if not ebook_path.exists():
        raise SystemExit(f"ERROR: {ebook_path} not found")

    ext = ebook_path.suffix.lower()
    if ext == ".epub":
        pages, images, nav_text, ncx_text = load_epub(ebook_path)
    elif ext in (".azw3", ".azw", ".mobi", ".kfx"):
        pages, images, nav_text, ncx_text = load_azw3(ebook_path)
    else:
        raise SystemExit(f"ERROR: unsupported ebook type '{ext}' (need .epub or .azw3)")

    print(f"Loaded {len(pages)} spine pages, {len(images)} images from {ebook_path.name}")
    print(f"Navigation: nav={'yes' if nav_text else 'no'} ncx={'yes' if ncx_text else 'no'}")
    groups = group_into_chapters(pages, nav_text, ncx_text)
    print(f"Grouped into {len(groups)} chapter(s):")
    for i, g in enumerate(groups, 1):
        print(f"  {i:02d}. {g['title']} ({len(g['pages'])} pages)")

    out_dir = resolve_output_dir(output_dir, volume)
    write_chapters(groups, images, out_dir)


def main():
    ap = argparse.ArgumentParser(
        description="Split a JP light-novel .epub/.azw3 into chapter markdown + images.")
    ap.add_argument("ebook", help="path to the .epub or .azw3 file")
    ap.add_argument("output_dir", help="output directory (Source/ or a Volume N dir)")
    ap.add_argument("--volume", "-v", type=int, default=None,
                    help="volume number; writes under <output_dir>/Volume N/")
    args = ap.parse_args()
    split_ebook(args.ebook, args.output_dir, args.volume)


if __name__ == "__main__":
    main()
