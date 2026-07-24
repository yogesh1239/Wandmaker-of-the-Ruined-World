# Volume 4 Remaining Render Queue

All rendered assets must preserve the source canvas dimensions and follow `Editing/image-localization-typesetting-style.md` plus the named per-image spec. Run the same fresh visual verifier against source + spec + output after each render or revision.

## Revise Existing Output

| Output | Source | Required correction |
|-|-|-|
| `s-h2.png` | `s-h2.jpg` | Preserve the source's existing small English `author` and `illustrator` labels exactly. The current output deletes/retypes them as large all-caps labels, contrary to the spec. All other localized text independently passed. |

## Missing Localized Outputs

| Output stem | Spec | Scope |
|-|-|-|
| `kuchie-001` | `kuchie-001.md` | Bottom Japanese title only |
| `kuchie-002` | `kuchie-002.md` | JP labels/dialogue plus correction of banned `Kenshi Ori` roman label |
| `kuchie-003` | `kuchie-003.md` | Two dialogue regions and `Fuyo` label |
| `kuchie-004` | `kuchie-004.md` | Character label and two dialogue regions; dense body copy stays unchanged |
| `p010` | `p010.md` | Remove `登場人物`; retain the existing `Characters` heading as the sole heading |
| `s-h1-4` | `s-h1-4.md` | Three booklet-wrap title regions |
| `s-p008` | `s-p008.md` | Name only |
| `s-p009` | `s-p009.md` | Name only |
| `s-p010` | `s-p010.md` | Name only |
| `s-p011` | `s-p011.md` | Name only |
| `s-p012` | `s-p012.md` | Name only |
| `s-p013` | `s-p013.md` | Page heading only |
| `s-p014` | `s-p014.md` | Page heading only |
| `s-p016` | `s-p016.md` | Page heading only |
| `s-p019` | `s-p019.md` | Page heading only |
| `s-p023` | `s-p023.md` | Page heading only |
| `s-p026` | `s-p026.md` | Page heading only |
| `s-p028` | `s-p028.md` | Page heading only |
| `s-p030` | `s-p030.md` | Page heading only |
| `s-p032` | `s-p032.md` | Page heading only |
| `toc-001` | `toc-001.md` | All visible Japanese contents entries |

Preferred working output is PNG in `English/Volume 4/localized-images/<stem>.png`; the EPUB swap step must resample it to the original asset's exact dimensions and original filename/format.

## Already Passing

`cover.png`, `titlepage.png`, `s-h1.png`, `s-p003.png`, `s-p004.png`, `s-p005.png`, and `s-p006.png`.

`s-h3.png` also passed its former localization spec visually, but it is **not an authorized swap**: the corrected spec follows `novel.config.md` and retains the original Japanese colophon/legal page.

## Chapter / Build Reference Requirements

1. Chapter 18 must represent the complete source booklet sequence: `s-h1`, `s-h2`, `s-p003` through `s-p038`, then the original `s-h3`. The current file stops after `s-p006` and jumps to `s-h3`.
2. `core/scripts/build_epub.py` recognizes block image markers only as `![...](images/<filename>)`. Normalize the 16 current `localized-images/...` markers to original asset basenames under `images/`; localized pixels are selected through image swaps, not through a different Markdown directory.
3. The derived config from `core/scripts/derive_build_config.py novel.config.md --volume 4` currently omits `localized_images_dir` and `image_swaps`. Before building, configure swaps for all authorized localized stems and original dimensions. Do not include `s-h3`.
4. Preserve the nine clean interior illustrations unchanged. Their existing copies are byte-identical to source, but Markdown should still use `images/<original filename>` for the builder.
5. Re-run the whole-volume consistency gate, derive/build/verify, broken-reference check, original-dimension swap check, and CJK/macron/footnote gates after integration.
