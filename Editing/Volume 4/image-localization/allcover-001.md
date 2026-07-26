# Image Localization Spec — `allcover-001.jpg`

## Source

- **Path:** `Source/Volume 4/images/allcover-001.jpg`
- **Type:** full wraparound dust-jacket spread laid flat — front flap, front cover, spine, back cover
- **Canvas:** 2048 × 859 landscape JPEG (aspect ≈ 2.38 : 1)

## Panel geometry

Japanese binding, so laid flat the jacket runs front-flap/front-cover on the left, spine in the middle, back cover on the right.

| Region | Approx. x-range | Contents |
|-|-|-|
| Front flap | 0 – 330 | author bio block, illustrator bio block |
| Front cover | 330 – 965 | large vertical title, characters, Latin sub-title, credits, bottom design credits |
| Spine | 965 – 1075 | title, green Latin title, circled volume mark, credits, publisher mark |
| Back cover | 1075 – 2048 | ruined-shack landscape; all lettering here is painted in-world signage |

## Verbatim Japanese by visual region

**Front flap — author block**

- `黒留ハガネ`
- `くろどめ・はがね`
- `明治元年、東京に生まれる。`
- `大正九年、東京魔法大学理論魔法学部を卒業。`
- `月面基地駐在員、`
- `急いでる人の目の前の信号を赤にする仕事などを経て、`
- `現在は南極で文筆業を営む。`
- `著書に『崩壊世界の魔法杖職人』`
- `『嘘全開のカバー袖コメントを書く100の方法』など。`

**Front flap — illustrator block**

- `かやはら`
- `絵を描くお仕事をしています。`

**Front cover**

- Large vertical title: `崩壊世界の魔法杖職人`
- Small vertical Latin, already Latin in the source: `Wandmaker of` / `the Ruined World`
- `黒留ハガネ`
- `Illustrator` (already Latin) + `かやはら`
- Circled volume mark: `4`
- Bottom credits: `Cover Illustration` (already Latin) + `かやはら`
- Bottom credits: `Design` (already Latin) + `たにごめかぶと(ムシカゴグラフィクス)`

**Spine**

- `崩壊世界の魔法杖職人`
- Green letterspaced Latin, already Latin in the source: `Wandmaker of the Ruined World`
- Circled volume mark: `4`
- `黒留ハガネ`
- `Illustrator` (already Latin) + `かやはら`
- Publisher mark: `MEDIA FACTORY` with the MF monogram

**Back cover**

- No editorial typography. The only lettering is painted into the illustration: weathered notices and a vertical banner on the derelict shack, including an anti-organised-crime neighbourhood notice and a crime-prevention banner. These are artwork, not display copy.

## Exact English by visual region

**Front flap — author block**

- `Kurodome Hagane`
- (romanization gloss line — see Notes; not carried into English)
- `Born in Tokyo in the first year of Meiji.`
- `Graduated from the Faculty of Theoretical Magic, Tokyo Magic University, in the ninth year of Taisho.`
- `Served as a resident officer at the lunar base,`
- `worked a stint turning the light red right in front of people who were in a hurry,`
- `and now makes a living as a writer in Antarctica.`
- `Works include Wand Maker of the Ruined World`
- `and 100 Ways to Write a Cover-Flap Comment That Is Nothing But Lies.`

**Front flap — illustrator block**

- `Kayahara`
- `I draw pictures for a living.`

**Front cover**

- Large title: `Wand Maker of the Ruined World`
- Latin sub-title, corrected in place: `Wand Maker of` / `the Ruined World`
- `Kurodome Hagane`
- `Illustrator` + `Kayahara`
- Circled volume mark: `4`
- `Cover Illustration` + `Kayahara`
- `Design` + `Tanigome Kabuto (Mushikago Graphics)`

**Spine**

- `Wand Maker of the Ruined World`
- Green letterspaced Latin, corrected in place: `Wand Maker of the Ruined World`
- Circled volume mark: `4`
- `Kurodome Hagane`
- `Illustrator` + `Kayahara`
- `MEDIA FACTORY` + MF monogram — retained verbatim as a publisher trademark

**Back cover**

- No change. The painted signage stays Japanese.

## Editing and refinement record

- **Pass A: complete.** Every region was transcribed from LANCZOS-upscaled crops (5×–6× on the flap blocks, 3× on the rotated spine strip), not from a page-level read. Checked against `novel.config.md` identity block, the glossary, and the filed Volume 1/3 image specs. `崩壊世界の魔法杖職人` → `Wand Maker of the Ruined World` per config line 7. `黒留ハガネ` → `Kurodome Hagane` per config line 10. `かやはら` → `Kayahara` and the `Illustrator` role label per the filed Volume 3 `cover.md` and Volume 1 frontmatter specs. `東京魔法大学` → `Tokyo Magic University` per the chapter-title map (Vol 1 ch. 9). No macrons and no long-vowel doubling: `Kurodome`, `Tanigome`, `Mushikago`, `Taisho`.
- **Pass B: complete.** The flap bio is a deadpan joke résumé and was read as finished copy in the locked Casual/Comedy register, not calqued. `月面基地駐在員` became `Served as a resident officer at the lunar base` rather than the stiff `lunar base resident staff member`. `急いでる人の目の前の信号を赤にする仕事` became `turning the light red right in front of people who were in a hurry`, which keeps the petty-malice gag that a literal `a job making the signal red` loses. The three middle clauses were joined into one `Served… , worked… , and now…` sentence so the CV reads as one continuous straight-faced list, which is how the Japanese runs. `嘘全開` became `Nothing But Lies` rather than the flat `full of lies`. Book titles are set in italic-equivalent plain text without the Japanese corner brackets, per English trade practice.

## Notes and uncertainties

- **No unresolved or illegible text.** Every region resolved at 5×–6×, including the 6-px flap body copy.
- **The `くろどめ・はがね` line is a furigana-style romanization gloss** giving the reading of the author's name for Japanese readers. It carries no information an English reader needs once the name is already romanized as `Kurodome Hagane`, so it has no English counterpart and would be dropped, not translated, in a real English edition.
- **`Wandmaker` as one word is a banned alias.** It appears twice in this source, in the front-cover Latin sub-title and in the green spine Latin. Both are corrected to `Wand Maker of the Ruined World`, matching the locked config form and the filed Volume 3 `cover.md` decision.
- **The back-cover signage is diegetic.** The notices and banner on the shack are painted set-dressing describing the ruined world, not display copy addressed to the reader. Localizing them would alter the illustration, so they stay Japanese.
- **`たにごめかぶと(ムシカゴグラフィクス)` is the real jacket designer and design studio.** Romanized, not translated: `Tanigome Kabuto (Mushikago Graphics)`.

## Render decision — no render, original retained

**This spread is deliberately not re-rendered. The original Japanese jacket is kept.** Reasons, in order of weight:

1. **Project policy.** `novel.config.md` line 122 sets the cover/colophon policy as *"retain the Japanese cover and colophon as-is; retain original publisher/legal matter in Japanese."* The flap author bio, the design credit, and the `MEDIA FACTORY` mark are exactly that publisher matter. The localized front cover the build actually consumes is `cover.jpg`, which is specced and rendered separately.
2. **Filed precedent.** Volume 3 localized `cover.jpg` and left `allcover-001.jpg` unrendered. Localizing it here alone would make Volume 4 inconsistent with Volume 3 for the same asset.
3. **Resolution.** At 2048 × 859 the flap body copy is roughly 6 px tall. Re-typesetting eleven lines of micro-copy, a large vertical display title, and a full spine at that pixel density cannot be done by image edit without smearing the lettering and damaging the painting underneath it. English runs longer than the Japanese here, which makes the fit worse, not better. This is the kind of asset a publisher's designer re-typesets from the layered source file, which is not available.
4. **The back cover is nearly all protected artwork**, so a whole-canvas edit pass would risk the largest panel for no editorial gain.

The transcription and English above are complete and verified, so this spread can be rendered later without redoing any analysis if the project decides the jacket should be localized after all.

- **Built-in image edit renders:** 0 — intentional
- **Saved output:** none; `Source/Volume 4/images/allcover-001.jpg` remains the shipping asset
- **Source integrity:** original unmodified
