# Vendored KindleUnpack (for `.azw3` extraction)

This directory vendors **KindleUnpack** — a pure-Python tool (no Calibre) that
decompresses Kindle KF8 (`.azw3`) books back into their source HTML/CSS/images.

`split_ebook.py` uses it as the front-end for `.azw3` inputs: it imports
KindleUnpack's `unpackBook(...)`, unpacks the book to a temp dir, and feeds the
KF8 (`mobi8`) HTML into the same XHTML→markdown splitter used for `.epub`.

## Why KindleUnpack, not Calibre

The KF8 source HTML retains `<ruby>…<rt>…</rt></ruby>` furigana. A Calibre
**conversion** can flatten or drop that ruby markup, silently destroying the
kanji readings we need for translation. KindleUnpack only *decompresses* — it
does not re-render — so the furigana survives intact and the splitter can turn
it into `漢字[かな]`.

## Install

Clone the upstream repo directly into this folder:

```sh
cd "<path>/core/scripts/kindleunpack"
git clone https://github.com/kevinhendricks/KindleUnpack .
```

(Or download a release zip from https://github.com/kevinhendricks/KindleUnpack
and extract its contents here.)

`split_ebook.py` resolves the module automatically, trying in order:

1. `import kindleunpack` (a package whose `__init__` exposes `unpackBook`)
2. `core/scripts/kindleunpack/kindleunpack.py`
3. `core/scripts/kindleunpack/lib/kindleunpack.py`

If none expose `unpackBook`, the splitter prints these install instructions and
exits non-zero. It never falls back to Calibre.

## Notes

- Pure Python; runs under the same Python 3 as the rest of `core/scripts/`.
- Nothing here is committed to this repo by default — it is a local vendor dir.
- License: KindleUnpack is GPL-licensed; keep its `LICENSE` file when cloning.
