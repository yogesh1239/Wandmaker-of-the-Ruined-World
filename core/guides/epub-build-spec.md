# EPUB Build Spec — Japanese Light Novels (Agnostic)

How to build an English EPUB from a Japanese source ebook plus the finalized
English chapter files. This spec is series-agnostic: every per-novel value
(titles, spine map, image swaps, romanization, metadata) comes from
`novel.config.md`. `core/scripts/derive_build_config.py` derives the JSON
`build_epub.py --config` needs from `novel.config.md`; the `epub-builder` agent
runs that derive step, then `build_epub.py` and `verify_epub.py` against the
derived JSON, and self-verifies the gates.

Goal: an English EPUB that mirrors the original's structure and assets, with the
prose replaced by the finalized English translations, text-bearing illustrations
swapped for their localized versions, and reading direction forced to horizontal
LTR (required for English).

## Build Invocation

The **derive→build→verify invocation**: derive the JSON config from
`novel.config.md`, then build and verify against that JSON (never invoke
`build_epub.py`/`verify_epub.py` directly against
`novel.config.md` — they only understand the derived JSON):

```bash
python core/scripts/derive_build_config.py novel.config.md --volume N
python core/scripts/build_epub.py --config "Editing/Volume N/build_config.json"
python core/scripts/verify_epub.py --config "Editing/Volume N/build_config.json"
```

`derive_build_config.py` writes `Editing/Volume N/build_config.json` by default
(pass `--out <path>.json` to override). It warns to stderr and excludes any
chapter-title-map row whose assembled `.md` isn't found under `English/Volume
N/`, and exits 2 if zero chapters are found for the volume.

## Inputs (all resolved from `novel.config.md`)

- **Original ebook** for the volume — `.epub` (read XHTML directly) or `.azw3`
  (already extracted to XHTML via vendored KindleUnpack at split time; no
  Calibre conversion). The build reads the original package for structure,
  assets, and CSS.
- **English chapters** (assembled, FINAL): `English/Volume N/<Translated
  Title>.md`, one per chapter, in spine order.
- **Localized images**: the rendered English versions of the 1–3 text-bearing
  illustrations (front/back-matter image pages + any in-prose text images),
  produced from the `image-localizer` specs and dropped in
  `English/Volume N/localized-images/`.
- **Chapter-title map** from `novel.config.md` — the single source of truth for
  each chapter's number, `<h1>`/TOC title, and contents-image entry.
- **EPUB metadata** from `novel.config.md` — title, series, per-volume title,
  language (`en`), author/creator.

## Output

- `English/<Series Title> v<NN> (EN).epub` (exact name from config).
- Build in a temp dir (e.g. `English/_epub_build/`); assemble the zip from there.

## Mapping the Source Spine

Do not hardcode page IDs — derive the spine from the original package each run:

1. Read the original OPF `<spine>` in order; resolve each idref to its manifest
   item and the XHTML/image it points to.
2. Classify each spine item:
   - **Front matter:** cover, caution/disclaimer page, title/tobira image,
     character-intro image pages, contents/TOC image, part-divider text page.
   - **Body:** prose pages and standalone full-page illustration pages,
     interleaved. A chapter is one or more prose pages with illustration pages
     between them.
   - **Back matter:** afterword, previews, info/colophon pages, publisher logo
     image.
3. Group body pages into chapters and align each chapter group to its English
   `.md` file via the config chapter-title map (by order/number, not by JP
   heading text).
4. **Absorb** standalone interior-illustration XHTML pages: remove them from the
   spine/manifest, because their images become **inline** in the chapter docs at
   the corresponding `![pXXX]` markers. Keep every image **file** in the package.

Record the derived mapping in the build log so the run is hand-offable.

## Target Structure (consolidated)

Typical target spine (adapt to what the source actually has):

1. **cover** — keep page & image as-is (original cover/logo stays).
2. **caution / disclaimer page** — translate its short text to English; keep page.
3. **title / tobira image** — keep as-is if it's already romaji/decorative;
   otherwise swap for a localized version.
4. **character-intro / front-matter image pages** — keep page, swap image →
   localized version (these are usually text-bearing).
5. **contents page** — keep page, swap image → localized contents (titles from
   the config chapter-title map).
6. **part-divider text page** (if any) — translate its short text; keep page, or
   keep as-is if purely decorative.
7. **Chapter 1 … Chapter N** — one XHTML each, full English prose, with the
   chapter's illustrations inlined at their marker points.
8. **back matter** — afterword/previews translated if they're authorial content;
   colophon/legal/info pages kept **as-is** (leave Japanese — never fabricate
   publisher/legal text).
9. **end logo image** — keep as-is.

## Per-Chapter Markdown → XHTML Rules

- **Chapter title:** comes from the config chapter-title map → `<h1>` on the
  page. Do **not** read it from an in-file heading (the assembled `.md` has no
  title heading, except the sanitized-filename exception — if an in-file `#`
  heading exists for that reason, prefer the config title for `<h1>` and TOC).
- **Front-matter image markers inside the first chapter:** if the splitter left
  front-matter image markers (cover, tobira, intro, contents) at the head of
  chapter 1's `.md`, DROP them — they are front-matter pages, not chapter
  content. Keep genuine interior illustration markers.
- **Back-matter tail in the last chapter:** if the final chapter's `.md` ends
  with a back-matter image (publisher logo) and/or a trailing text block,
  inspect that block. If it's an afterword/preview/credits, emit it as a separate
  back-matter page **after** the chapter; if it's clearly story epilogue prose,
  keep it as the chapter's end. Do **not** inline the publisher-logo image into
  the chapter. Report the decision.
- **Paragraphs:** blank-line-separated text → `<p>…</p>`.
- **Scene break** line `---` → centered ornament mirroring the original, e.g.
  `<p class="gap-mark"><img class="ornament" src="../image/<ornament>.png" alt="*"/></p>`
  (reuse the original's ornament asset if it has one; otherwise a typographic
  centered mark).
- `*italic*` → `<em>`; `**bold**` → `<strong>`.
- **Inline image** `![pXXX.jpg](images/pXXX.jpg)` →
  `<div class="illust"><img src="../image/pXXX.jpg" alt=""/></div>`. Verify the
  relative path against how the original pages reference images.
- **Encoding:** write every XHTML as UTF-8. (With the no-macron convention there
  should be no macron characters; if any romanized term legitimately needs a
  diacritic, UTF-8 preserves it.)

## EPUB3 Popup Footnotes

Render the `## Translator Notes` block as EPUB3 popup footnotes (overlay in
supporting readers; jump-link fallback elsewhere).

- Every generated XHTML `<html>` root MUST declare both namespaces:
  `<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">`.
- Inline reference `[^N]` →
  `<a epub:type="noteref" class="noteref" id="fnref-CH-N" href="#fn-CH-N"><sup>N</sup></a>`.
- The `## Translator Notes` block → `<section class="notes"><h2>Translator's
  Notes</h2>…</section>`, with EACH note its own popup-able aside:
  `<aside epub:type="footnote" id="fn-CH-N"><p><sup>N</sup> … <a class="backlink" href="#fnref-CH-N">↩</a></p></aside>`.
- Namespace ids per chapter (`CH` = chapter number) so they're unique book-wide.
  Asides also render in the notes section as the no-popup fallback.

## Images

- Copy every image from the original package into the new package UNCHANGED,
  EXCEPT the text-bearing images listed for localization in `novel.config.md`.
- For each localized image: open the localized PNG, **upscale to the original
  asset's exact pixel dimensions** (LANCZOS), and save with the **original
  filename and format** (e.g. `pXXX.jpg`, JPEG quality ~92). Keeping the original
  filename and dimensions keeps every existing reference valid.
- Keep any ornament/divider asset (e.g. the scene-break PNG).

## CSS / Reading Direction (RTL → LTR)

JP source CSS is vertical / right-to-left; English must be horizontal LTR.

- Add a stylesheet `style/english.css` and link it in **every** XHTML you
  generate or keep (including kept image pages like cover/contents), forcing:
  ```
  html,body{ -epub-writing-mode:horizontal-tb; writing-mode:horizontal-tb;
             direction:ltr; text-align:left; }
  ```
  plus sensible defaults:
  ```
  .illust img{max-width:100%;height:auto;display:block;margin:1em auto;}
  .ornament{height:1.2em;width:auto;}
  .gap-mark{text-align:center;margin:1.2em 0;}
  .notes{margin-top:2em;border-top:1px solid #ccc;padding-top:1em;font-size:0.9em;}
  h1{ ... }
  ```
- In the OPF `<spine>`, set `page-progression-direction="ltr"`.
- Keeping the original CSS is fine (harmless), but `english.css` must win — link
  it **last** in each page.

## OPF + Nav

- Rebuild the OPF manifest + spine to the target structure: remove the absorbed
  illustration pages and any removed prose pages; add the new chapter XHTML files
  and `english.css`; keep all image items, CSS, and nav. Set
  `<spine page-progression-direction="ltr">`.
- Metadata from `novel.config.md`: set `<dc:title>` to the English series/volume
  title; set `<dc:language>` to `en`; keep author/creator and other metadata.
- Rebuild `toc.xhtml` (or the nav doc): list Cover (optional), Contents, each
  chapter by its **config title map** title, plus any back matter. Hrefs point to
  the new chapter files. Keep `epub:type="toc"`.
- Keep `META-INF/container.xml`. The `mimetype` entry MUST be the **first** zip
  entry and **STORED** (uncompressed).

## Verification Gates (REQUIRED before reporting done)

`verify_epub.py` must pass all of these; the `epub-builder` reports each:

1. **Zip / mimetype:** file opens as a zip; `mimetype` is the first entry and is
   `ZIP_STORED`; `META-INF/container.xml` present and points to the OPF.
2. **Manifest / spine integrity:** every manifest href exists in the archive;
   every spine idref exists in the manifest; the nav (toc) is reachable.
3. **References resolve:** every `<img src>` in every XHTML resolves to a file in
   the package (esp. inline `pXXX` images and the ornament asset).
4. **Zero stray CJK in prose:** grep each chapter XHTML for CJK (ranges
   `぀-ヿ`, `一-龯`) — expect ZERO; the prose is fully English. Report any hits.
   (Back-matter colophon/legal pages may legitimately retain Japanese — report
   but do not fail on those.)
5. **Zero macrons:** no macron characters (ō, ū, etc.) anywhere in the prose —
   the no-macron convention is enforced.
6. **Footnotes paired:** every `noteref` href has a matching `footnote` id and
   vice-versa, per chapter.
7. **Images present:** the swapped images exist at original dimensions; the image
   file count matches the original (none dropped — absorbed pages keep their
   image files).
8. **epubcheck:** if available on PATH, run it and report results; otherwise note
   it wasn't run.

## Report (final message)

List: output path & file size; the final spine (page list); the last-chapter
trailing-text decision; pass/fail for each verification gate above (with any CJK
hits, macron hits, or broken refs); and anything improvised. Verify outputs on
disk before claiming done.
