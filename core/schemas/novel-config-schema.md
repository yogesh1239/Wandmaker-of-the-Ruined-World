# Schema: `novel.config.md`

The single per-novel knob file. Every field the harness reads lives here. `core/scripts/derive_build_config.py` (A5) is the consumer for the build fields — it derives the JSON that `core/scripts/build_epub.py --config` needs from the values in this file.

## Knobs

- **Identity** — Title (JP), Title (EN), Type, Genre/setting, Author *(set by /setup-novel)*.
- **Source → volume map** — table `| Vol | Source file | Format | Extraction |` mapping each volume to its source ebook and extraction path (epub direct vs. azw3 via vendored KindleUnpack). Consumed by `split_ebook.py` and `derive_build_config.py`.
- **Paths** — `Source/Volume N/`, `English/Volume N/`, `Editing/Volume N/`.
- **Unit paths** — optional table `| Unit | Source path | English path | Editing path |`.
  Use this for webnovels or any project whose release unit is not a numbered
  volume when running chapter gates. If absent, scripts retain the legacy
  fallback: `Source/Volume N/`, `English/Volume N/`, `Editing/Volume N/`.
  The EPUB build path remains volume-based until `derive_build_config.py` and
  `/build-epub` are made unit-aware.
- **Romanization convention** — no macrons; explicitly lock whether Japanese long vowels are doubled or left unmarked. Exact names and terms remain controlled by `glossary.md`; macrons are rejected by `core/scripts/normalize_romaji.py --check`.
- **Reading direction** — source RTL → build EPUB LTR (`page-progression-direction`).
- **Furigana** — preserved as `漢字[かな]`.
- **Part-split threshold** — integer source-line count; chapters longer split into parts, shorter translate/edit whole. Default 400.
- **Register lock** — the locked register + one-line justification. `UNSET` until `/setup-novel`; holds for the whole novel once set.
- **Chapter-title map** — the legacy table `| Vol | N | JP title | EN title |`
  remains required for volume-based projects and EPUB builds. The chapter gate
  wrapper also accepts `| Unit | N | JP title | EN title |` for webnovel-style
  gate runs. This table remains the single source of truth for output filenames;
  EPUB `<h1>`/TOC/contents titles are still consumed through the legacy `Vol`
  form until the build path is made unit-aware.
- **EPUB metadata (per volume)** — series, title pattern, language, original title+author, cover/colophon policy, per-volume spine map + image pages. Consumed by `derive_build_config.py`.
