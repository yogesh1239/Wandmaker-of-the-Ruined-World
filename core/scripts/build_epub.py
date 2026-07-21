#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build an English EPUB from assembled chapter .md files + a source EPUB shell.

Novel-agnostic and CONFIG/CLI-driven: chapter titles, the spine map, EPUB
metadata, the source paths, RTL->LTR, and any localized-image swaps all come
from a config dict (a JSON file) -- nothing is hardcoded.

Reading direction is FORCED to ltr (page-progression-direction="ltr") plus an
injected english.css that sets horizontal-tb / direction:ltr.

Assembled chapter .md files carry NO in-file title heading; the chapter <h1>
and the TOC entry are taken from the config's per-chapter "title".

EPUB3 popup footnotes are kept: [^N] in prose -> <a epub:type="noteref">, and a
trailing "## Translator Notes" section -> <aside epub:type="footnote"> popups.

The mimetype entry is written first and STORED. Pillow is required for image
swaps (resizing a localized PNG to the original JPEG's pixel dimensions).

Usage:
  python build_epub.py --config <config.json> [--out <out.epub>]

Config schema (JSON), all paths absolute or relative to the config file:
{
  "source_epub":   "...\\<JP source>.epub",       # original JP epub shell
  "chapters_dir":  "...\\English\\Volume 1",      # holds assembled .md files
  "out_epub":      "...\\<Novel> v01 (EN).epub",
  "localized_images_dir": "...\\English\\Volume 1\\localized-images",  # optional

  "metadata": {
    "title":     "<Novel Title>, Vol. 1",
    "file_as":   "<Novel Title> 1",
    "language":  "en",
    "identifier":"urn:uuid:....",      # optional; a urn:uuid is generated if omitted
    "modified":  "2026-06-14T00:00:00Z",
    "creators":  [ {"name": "Author Name", "role": "aut"},
                   {"name": "Illustrator", "role": "ill"} ],
    "publisher": "Publisher",
    "cover_image_id": "cover"          # manifest id of the cover image (default "cover")
  },

  # Internal layout of the source epub (auto-detected if omitted):
  "src_xhtml_prefix": "item/xhtml/",   # where source xhtml pages live in the zip
  "src_image_prefix": "item/image/",   # where source images live
  "src_style_prefix": "item/style/",   # where css lives
  "opf_path":         "item/standard.opf",
  "img_href_base":    "../image/",     # how chapter xhtml references images
  "css_links":        ["../style/book-style.css", "../style/english.css"],

  # Chapters, in spine order. md is relative to chapters_dir.
  "chapters": [
    { "id": "chapter-1", "md": "Chapter 1 - Title.md", "title": "Chapter 1: Title",
      "drop_images": ["tobira.jpg"] }   # optional per-chapter image markers to drop
  ],

  # Front/back matter pages kept verbatim from the source epub (english.css injected).
  # Each is a source page id (xhtml stem). Placed before/after the chapters.
  "front_matter": [ {"id": "p-0001"} ],
  "back_matter":  [ {"id": "p-0043"} ],

  # Optional regenerated caution page id -> use the built-in EN caution text.
  "caution_page_id": "p-0002",

  # Localized image swaps: localized PNG (stem.png in localized_images_dir)
  # resized to (w,h) and written over item/image/<stem>.jpg.
  "image_swaps": { "p002": [1370, 2048] },

  # TOC entries (label -> href stem). If omitted, built from front matter +
  # chapters + back matter automatically.
  "toc": [ {"label": "Cover", "href": "xhtml/p-0001.xhtml"} ]
}
"""

import io
import os
import re
import sys
import html
import json
import uuid
import zipfile
import argparse

sys.stdout.reconfigure(encoding="utf-8")

try:
    from PIL import Image
except ImportError:
    Image = None


XML_HEAD = (
    '<?xml version="1.0" encoding="UTF-8"?>\n'
    "<!DOCTYPE html>\n"
    '<html xmlns="http://www.w3.org/1999/xhtml" '
    'xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="en" lang="en">\n'
)

ENGLISH_CSS = (
    "html,body{ -epub-writing-mode:horizontal-tb; writing-mode:horizontal-tb;"
    " direction:ltr; text-align:left; }\n"
    "body{ margin:0 5%; line-height:1.7; }\n"
    "p{ margin:0 0 0.8em 0; text-indent:1em; }\n"
    "h1{ font-size:1.5em; margin:1.5em 0 1em; line-height:1.4; text-indent:0; }\n"
    "h2{ font-size:1.1em; text-indent:0; }\n"
    ".illust img{ max-width:100%; height:auto; display:block; margin:1em auto; }\n"
    ".image-page .fit{ max-width:100%; height:auto; display:block; margin:0 auto; }\n"
    ".ornament{ height:1.2em; width:auto; }\n"
    ".gap-mark{ text-align:center; margin:1.2em 0; text-indent:0; }\n"
    ".notes{ margin-top:2em; border-top:1px solid #ccc; padding-top:1em;"
    " font-size:0.9em; }\n"
    ".notes p{ text-indent:0; }\n"
    ".notes aside{ margin:0 0 0.8em 0; }\n"
    ".noteref{ text-decoration:none; }\n"
    ".backlink{ text-decoration:none; }\n"
)

CAUTION_BODY = (
    '<body class="caution-page">\n<div class="main">\n'
    "<p>This work is best viewed in the original layout. Some formatting may "
    "appear slightly distorted depending on your reading environment.</p>\n"
    "<p><br/></p>\n"
    "<p>Display may vary depending on the browser or viewer you use.</p>\n"
    "</div>\n</body>\n</html>\n"
)

IMG_RE = re.compile(r"^!\[[^\]]*\]\(images/([^)]+)\)\s*$")
HEAD_RE = re.compile(r"^#{1,6}\s+(.*)$")
FNREF_RE = re.compile(r"\[\^(\d+)\]")


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------

def page_head(title, css_links):
    links = "\n".join(
        '<link rel="stylesheet" type="text/css" href="%s"/>' % h for h in css_links)
    return (XML_HEAD + '<head>\n<meta charset="UTF-8"/>\n<title>%s</title>\n%s\n</head>\n'
            % (html.escape(title), links))


def inline_md(text):
    text = html.escape(text, quote=False)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<em>\1</em>", text)
    return text


def apply_fnrefs(text, ch_id):
    def repl(m):
        n = m.group(1)
        return ('<a epub:type="noteref" class="noteref" id="fnref-%s-%s"'
                ' href="#fn-%s-%s"><sup>%s</sup></a>' % (ch_id, n, ch_id, n, n))
    return FNREF_RE.sub(repl, text)


def ornament(img_href_base):
    return ('<p class="gap-mark"><img class="ornament" src="%su273f.png" alt="*"/></p>'
            % img_href_base)


def build_chapter(ch, md_path, cfg):
    """Render one assembled .md into a chapter XHTML doc. Returns (doc, note_ids)."""
    ch_id = ch["id"]
    title = ch["title"]
    img_base = cfg["img_href_base"]
    drop = set(ch.get("drop_images", []))
    orn = ornament(img_base)

    raw = open(md_path, encoding="utf-8").read()
    body_md, notes_md = raw, ""
    m = re.search(r"\n##\s*Translator'?s?\s*Notes\s*\n", raw)
    if m:
        body_md, notes_md = raw[:m.start()], raw[m.end():]

    lines = body_md.split("\n")
    out = ['<body class="chapter">', '<div class="main">', "<h1>%s</h1>" % inline_md(title)]
    block = []

    def flush():
        if not block:
            return
        para = " ".join(s.strip() for s in block).strip()
        block.clear()
        if para:
            out.append("<p>%s</p>" % apply_fnrefs(inline_md(para), ch_id))

    for line in lines:
        s = line.strip()
        if s == "":
            flush()
            continue
        if HEAD_RE.match(s):           # drop any md heading; the h1 is already set
            flush()
            continue
        im = IMG_RE.match(s)
        if im:
            flush()
            fn = im.group(1)
            if fn in drop:
                continue
            if fn == "u273f.png":
                out.append(orn)
                continue
            out.append('<div class="illust"><img src="%s%s" alt=""/></div>'
                       % (img_base, html.escape(fn)))
            continue
        if s == "---":
            flush()
            out.append(orn)
            continue
        block.append(line)
    flush()

    while out and out[-1] == orn:      # strip trailing scene-break ornament
        out.pop()

    note_ids = []
    if notes_md.strip():
        out.append('<section class="notes">')
        out.append("<h2>Translator's Notes</h2>")
        for part in re.split(r"\n(?=\[\^\d+\]:)", notes_md.strip()):
            mm = re.match(r"\[\^(\d+)\]:\s*(.*)$", part.strip(), re.S)
            if not mm:
                continue
            num, txt = mm.group(1), mm.group(2).strip()
            txt = apply_fnrefs(inline_md(txt), ch_id)
            note_ids.append(num)
            out.append('<aside epub:type="footnote" id="fn-%s-%s">'
                       '<p><sup>%s</sup> %s '
                       '<a class="backlink" href="#fnref-%s-%s">↩</a></p></aside>'
                       % (ch_id, num, num, txt, ch_id, num))
        out.append("</section>")

    out += ["</div>", "</body>\n</html>\n"]
    return page_head(title, cfg["css_links"]) + "\n".join(out), note_ids


def detect_prefixes(names):
    """Auto-detect zip layout prefixes from a source epub's namelist."""
    def common_prefix(suffixes):
        hits = [n for n in names if any(n.lower().endswith(s) for s in suffixes)
                and not n.endswith("/")]
        if not hits:
            return None
        # most common directory prefix
        from collections import Counter
        dirs = Counter(n.rsplit("/", 1)[0] + "/" for n in hits if "/" in n)
        return dirs.most_common(1)[0][0] if dirs else ""
    return {
        "xhtml": common_prefix((".xhtml", ".html")),
        "image": common_prefix((".jpg", ".jpeg", ".png", ".gif", ".webp")),
        "style": common_prefix((".css",)),
    }


def load_config(path):
    with open(path, encoding="utf-8") as f:
        cfg = json.load(f)
    base = os.path.dirname(os.path.abspath(path))

    def resolve(p):
        return p if os.path.isabs(p) else os.path.normpath(os.path.join(base, p))

    for key in ("source_epub", "chapters_dir", "out_epub", "localized_images_dir"):
        if cfg.get(key):
            cfg[key] = resolve(cfg[key])
    return cfg


# --------------------------------------------------------------------------
# main build
# --------------------------------------------------------------------------

def build(cfg, out_override=None):
    src = cfg["source_epub"]
    z = zipfile.ZipFile(src)
    names = set(z.namelist())

    detected = detect_prefixes(names)
    xhtml_prefix = cfg.get("src_xhtml_prefix") or detected["xhtml"] or "item/xhtml/"
    image_prefix = cfg.get("src_image_prefix") or detected["image"] or "item/image/"
    style_prefix = cfg.get("src_style_prefix") or detected["style"] or "item/style/"
    cfg.setdefault("img_href_base", "../image/")
    cfg.setdefault("css_links", ["../style/english.css"])

    opf_path = cfg.get("opf_path")
    if not opf_path:
        cont = z.read("META-INF/container.xml").decode("utf-8")
        opf_path = re.search(r'full-path="([^"]+)"', cont).group(1)
    item_root = opf_path.rsplit("/", 1)[0] + "/" if "/" in opf_path else ""

    out_epub = out_override or cfg["out_epub"]
    md = cfg["metadata"]

    # --- chapter docs ---
    chapter_docs, chapter_notes = {}, {}
    for ch in cfg["chapters"]:
        md_path = os.path.join(cfg["chapters_dir"], ch["md"])
        doc, note_ids = build_chapter(ch, md_path, cfg)
        chapter_docs[ch["id"]] = doc
        chapter_notes[ch["id"]] = note_ids

    # --- keep a source page verbatim, inject english.css ---
    def keep(pid):
        t = z.read("%s%s.xhtml" % (xhtml_prefix, pid)).decode("utf-8")
        link = '<link rel="stylesheet" type="text/css" href="../style/english.css"/>'
        if link not in t and "</head>" in t:
            i = t.find("</head>")
            t = t[:i] + link + "\n" + t[i:]
        return t

    caution_id = cfg.get("caution_page_id")
    caution_doc = (page_head(md["title"], cfg["css_links"]) + CAUTION_BODY) if caution_id else None

    # --- assemble target spine: (idref, href, doc) ---
    spine = []
    rel_xhtml = xhtml_prefix[len(item_root):] if xhtml_prefix.startswith(item_root) else "xhtml/"

    def add_page(pid):
        href = "%s%s.xhtml" % (rel_xhtml, pid)
        if pid == caution_id and caution_doc:
            spine.append((pid, href, caution_doc))
        else:
            spine.append((pid, href, keep(pid)))

    for fm in cfg.get("front_matter", []):
        add_page(fm["id"])
    for ch in cfg["chapters"]:
        href = "%s%s.xhtml" % (rel_xhtml, ch["id"])
        spine.append((ch["id"], href, chapter_docs[ch["id"]]))
    for bm in cfg.get("back_matter", []):
        add_page(bm["id"])

    # --- manifest ---
    manifest = ['<item media-type="application/xhtml+xml" id="toc" '
                'href="toc.xhtml" properties="nav"/>']
    cover_id = md.get("cover_image_id", "cover")

    css_files = sorted(n for n in names if n.startswith(style_prefix) and n.endswith(".css"))
    for n in css_files:
        href = n[len(item_root):]
        cid = os.path.basename(href).rsplit(".", 1)[0]
        manifest.append('<item media-type="text/css" id="css-%s" href="%s"/>' % (cid, href))
    rel_style = style_prefix[len(item_root):] if style_prefix.startswith(item_root) else "style/"
    manifest.append('<item media-type="text/css" id="english-css" href="%senglish.css"/>'
                    % rel_style)

    rel_image = image_prefix[len(item_root):] if image_prefix.startswith(item_root) else "image/"
    img_files = sorted(n.split("/")[-1] for n in names
                       if n.startswith(image_prefix) and not n.endswith("/"))
    for f in img_files:
        iid = f.rsplit(".", 1)[0]
        mt = "image/png" if f.lower().endswith(".png") else "image/jpeg"
        extra = ' properties="cover-image"' if iid == cover_id else ""
        manifest.append('<item media-type="%s" id="img-%s" href="%s%s"%s/>'
                        % (mt, iid, rel_image, f, extra))

    for idref, href, _ in spine:
        manifest.append('<item media-type="application/xhtml+xml" id="%s" href="%s"/>'
                        % (idref, href))

    spine_xml = "\n".join('<itemref linear="yes" idref="%s"/>' % s[0] for s in spine)
    manifest_xml = "\n".join(manifest)

    # --- OPF metadata ---
    identifier = md.get("identifier") or ("urn:uuid:" + str(uuid.uuid4()))
    modified = md.get("modified", "2026-01-01T00:00:00Z")
    creators_xml = []
    for i, c in enumerate(md.get("creators", []), start=1):
        cid = "creator%02d" % i
        creators_xml.append('<dc:creator id="%s">%s</dc:creator>' % (cid, html.escape(c["name"])))
        creators_xml.append('<meta refines="#%s" property="role" scheme="marc:relators">%s</meta>'
                            % (cid, c.get("role", "aut")))
        creators_xml.append('<meta refines="#%s" property="display-seq">%d</meta>' % (cid, i))
    creators_block = "\n".join(creators_xml)
    publisher_block = ('<dc:publisher id="publisher">%s</dc:publisher>'
                       % html.escape(md["publisher"])) if md.get("publisher") else ""

    opf = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<package xmlns="http://www.idpf.org/2007/opf" version="3.0" xml:lang="en"\n'
        ' unique-identifier="unique-id">\n'
        '<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">\n'
        '<dc:title id="title">%s</dc:title>\n'
        '<meta refines="#title" property="file-as">%s</meta>\n'
        '%s\n%s\n'
        '<dc:language>%s</dc:language>\n'
        '<dc:identifier id="unique-id">%s</dc:identifier>\n'
        '<meta property="dcterms:modified">%s</meta>\n'
        '<meta name="cover" content="img-%s"/>\n'
        '</metadata>\n'
        '<manifest>\n%s\n</manifest>\n'
        '<spine page-progression-direction="ltr">\n%s\n</spine>\n'
        '</package>\n'
    ) % (html.escape(md["title"]), html.escape(md.get("file_as", md["title"])),
         creators_block, publisher_block, md.get("language", "en"),
         identifier, modified, cover_id, manifest_xml, spine_xml)

    # --- TOC ---
    toc_entries = cfg.get("toc")
    if not toc_entries:
        toc_entries = []
        for fm in cfg.get("front_matter", [])[:1]:
            toc_entries.append({"label": "Cover", "href": "%s%s.xhtml" % (rel_xhtml, fm["id"])})
        for ch in cfg["chapters"]:
            toc_entries.append({"label": ch["title"], "href": "%s%s.xhtml" % (rel_xhtml, ch["id"])})
        for bm in cfg.get("back_matter", [])[-1:]:
            toc_entries.append({"label": "Colophon", "href": "%s%s.xhtml" % (rel_xhtml, bm["id"])})
    toc_li = "\n".join('<li><a href="%s">%s</a></li>'
                       % (e["href"], html.escape(e["label"])) for e in toc_entries)
    first_href = toc_entries[0]["href"] if toc_entries else "toc.xhtml"

    toc = (
        '<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE html>\n'
        '<html xmlns="http://www.w3.org/1999/xhtml" '
        'xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="en">\n'
        '<head>\n<meta charset="UTF-8"/>\n'
        '<style type="text/css"> ol { list-style: none; padding-left: 1em; } </style>\n'
        '<title>%s</title>\n</head>\n<body>\n'
        '<nav epub:type="toc" id="toc">\n<h1>Navigation</h1>\n<ol>\n%s\n</ol>\n</nav>\n'
        '<nav epub:type="landmarks" id="guide">\n<h1>Guide</h1>\n<ol>\n'
        '<li><a epub:type="bodymatter" href="%s">Start</a></li>\n</ol>\n</nav>\n'
        '</body>\n</html>\n'
    ) % (html.escape(md["title"]), toc_li, first_href)

    # --- images (with swaps) ---
    image_bytes = {}
    for n in names:
        if n.startswith(image_prefix) and not n.endswith("/"):
            image_bytes[n] = z.read(n)

    swaps = cfg.get("image_swaps", {})
    if swaps:
        if Image is None:
            raise SystemExit("ERROR: Pillow is required for image_swaps. pip install Pillow")
        loc_dir = cfg.get("localized_images_dir")
        if not loc_dir:
            raise SystemExit("ERROR: image_swaps set but localized_images_dir missing in config")
        for stem, dims in swaps.items():
            w, h = dims
            png = os.path.join(loc_dir, stem + ".png")
            im = Image.open(png).convert("RGB").resize((w, h), Image.LANCZOS)
            buf = io.BytesIO()
            im.save(buf, "JPEG", quality=92)
            image_bytes["%s%s.jpg" % (image_prefix, stem)] = buf.getvalue()

    # --- styles ---
    style_bytes = {}
    for n in names:
        if n.startswith(style_prefix) and not n.endswith("/"):
            style_bytes[n] = z.read(n)
    style_bytes["%senglish.css" % style_prefix] = ENGLISH_CSS.encode("utf-8")

    container = z.read("META-INF/container.xml")

    # --- write the epub: mimetype FIRST and STORED ---
    out_dir = os.path.dirname(os.path.abspath(out_epub))
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    if os.path.exists(out_epub):
        os.remove(out_epub)

    zf = zipfile.ZipFile(out_epub, "w", zipfile.ZIP_DEFLATED)
    zi = zipfile.ZipInfo("mimetype")
    zi.compress_type = zipfile.ZIP_STORED
    zf.writestr(zi, "application/epub+zip")
    zf.writestr("META-INF/container.xml", container)
    zf.writestr(opf_path, opf.encode("utf-8"))
    zf.writestr("%stoc.xhtml" % item_root, toc.encode("utf-8"))
    for n, b in style_bytes.items():
        zf.writestr(n, b)
    for n, b in image_bytes.items():
        zf.writestr(n, b)
    for idref, href, doc in spine:
        zf.writestr(item_root + href, doc.encode("utf-8"))
    zf.close()

    print("WROTE", out_epub, os.path.getsize(out_epub), "bytes")
    print("spine pages:", len(spine))
    for ch in cfg["chapters"]:
        print("  %s notes:" % ch["id"], chapter_notes[ch["id"]])


def main():
    ap = argparse.ArgumentParser(description="Build an English EPUB from a config.")
    ap.add_argument("--config", "-c", required=True, help="path to the build config JSON")
    ap.add_argument("--out", "-o", default=None, help="override the output .epub path")
    args = ap.parse_args()
    cfg = load_config(args.config)
    build(cfg, args.out)


if __name__ == "__main__":
    main()
