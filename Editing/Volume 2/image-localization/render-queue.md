# Volume 2 Remaining Render and Reference Queue

## Immediate revision

1. `cover.jpg` — remove the still-visible large Japanese title `崩壊世界の魔法杖職人` and reconstruct only the artwork beneath it. Retain `Wand Maker of the Ruined World` exactly once. Reverify against `cover.md`.

## Fully specified, ready to render

1. `s-h1.jpg` — localize the booklet cover using `s-h1.md`.
2. `s-h2.jpg` — localize the complete booklet contents labels using `s-h2.md`.

## Requires verified manual transcription before complete localization

1. `p295.jpg` — next-volume advertisement: transcribe every promotional bullet/title/release region, then translate and revise `p295.md`.
2. `s-p003.jpg`–`s-p014.jpg` — character profiles: transcribe every statistic label/value, quotation, rating, and prose block; retain the already locked names/titles.
3. `s-p015.jpg`–`s-p017.jpg` — Volume 2 chapter commentary: transcribe every numbered heading and commentary block.
4. `s-p018.jpg` — mushroom-disease document: transcribe the complete document.
5. `s-p019.jpg`–`s-p021.jpg` — magic-item profiles: transcribe every item name, specification, caption, and prose block; resolve the currently untranscribed wand name on `s-p021.jpg`.
6. `s-p022.jpg`–`s-p023.jpg` — timeline: transcribe every date and event.
7. `s-p024.jpg`–`s-p025.jpg` — residential ranking: transcribe every rank/ward heading and explanation.
8. `s-p026.jpg`–`s-p027.jpg` — Tokyo Magic University notes: transcribe every subhead and prose block.
9. `s-p028.jpg`–`s-p030.jpg` — setting notes: transcribe every subhead and prose block.
10. `s-p031.jpg`–`s-p034.jpg` — short story `お隣の姐さん`: obtain a complete verified Japanese transcript and finalized English story before typesetting.

The current specs authorize safe partial replacements only. They deliberately leave all untranscribed Japanese unchanged and must not be treated as approval to erase or improvise dense copy.

## No render required

- Clean: `p018.jpg`, `p072.jpg`, `p073.jpg`, `p093.jpg`, `p126.jpg`, `p162.jpg`, `p178.jpg`, `p197.jpg`, `p207.jpg`, `p226.jpg`, `p238.jpg`.
- Retain by policy/context: `allcover-001.jpg`, `s-h1-4.jpg`, `s-h3.jpg`, `i-bookwalker.jpg`, and `gaiji-0000.png`–`gaiji-0006.png`.
- Existing verified PASS outputs: `kuchie-001.jpg`–`kuchie-005.jpg`, `p256.jpg`, `p271.jpg`, `titlepage.jpg`, and `toc-001.jpg`.

## Markdown and build-reference requirements

- Existing correct localized references:
  - `English/Volume 2/Chapter 14 - Three Steps Forward, Two Steps Back.md` → `localized-images/p256.jpg`
  - `English/Volume 2/Chapter 15 - Amulet.md` → `localized-images/p271.jpg`
- After `s-h1.jpg` and `s-h2.jpg` pass verification, change the two references in `English/Volume 2/Chapter 18 - Wand Maker of the Ruined World 2 Special Edition Booklet - Top Secret Files.md` from `images/` to `localized-images/`.
- The filed Chapter 18 currently omits the booklet content pages. A complete special-edition artifact must place `s-p003.jpg` through `s-p034.jpg` in source order after `s-h2.jpg`, using `localized-images/` only after each page has a verified localized render. Then preserve `s-h3.jpg` (colophon) and `s-h1-4.jpg` (full-wrap booklet cover) unchanged if the derived source-spine mapping includes them.
- `English/Volume 2/Chapter 19 - Ebook Bonus Original Short Story - Ori's Picture.md` correctly keeps `images/allcover-001.jpg` under the cover-retention policy.
- Front-matter cover/title/color/contents swaps are source-spine image-page swaps handled by the derived build config, not chapter Markdown markers. The build config must point only to verified localized copies.

## Gates after rendering/reference edits

1. Confirm every localized image exists, matches source dimensions, and has a fresh independent PASS ledger row.
2. Confirm every Markdown image target exists and no required text-bearing marker still points to `images/`.
3. Run `python3 core/scripts/normalize_romaji.py --check` on every changed Volume 2 chapter.
4. Run `python3 core/scripts/check_consistency.py --glossary glossary.md --all "English/Volume 2"`.
5. Derive the Volume 2 build config, build, and run `verify_epub.py`; verify image references, source-dimension parity, and image count.
