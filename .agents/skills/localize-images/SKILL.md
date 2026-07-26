---
name: localize-images
description: Localizes Japanese text-bearing light-novel illustrations into publication-quality English image edits. Use when asked to translate, typeset, render, redo, or quality-check text inside a volume's JPG/PNG illustrations, diagrams, title cards, maps, or info panels, and save the accepted images under English/Volume N/localized-images/.
---

# Localize Images

Localize the requested images (ask the user for the volume and image list if none is given).

Perform the entire workflow in the main agent. Never dispatch, spawn, or delegate to a subagent.

## The goal

**Produce a page that looks like it was designed in English from the start** — not a Japanese page with English pasted into it. A reader should never be able to tell the layout was translated.

That goal governs. Where a rule in this document would produce something that reads as templated, mechanical, or obviously converted, the goal wins: choose the better page, and record in the spec what you did and why. Rules here describe the usual case; they are not a substitute for looking at the image and exercising taste.

There are exactly two things the goal never licenses:

### Inviolable — facts, never a matter of taste

- **Names of real people.** Author, illustrator, designer, studio. Take them from `novel.config.md` and the filed specs. Never romanize by guess, never abbreviate, never invent. Getting this wrong misattributes a real person's work and is the single worst defect this skill can ship.
- **Glossary-locked forms and banned aliases.** Exact strings, exact spelling, exact word division.
- **Titles from the chapter-title map**, page numbers, volume numbers, dates, and any other figure carried from the source.
- **The artwork itself.** Characters, faces, anatomy, poses, clothing, focal objects, lighting and palette. Never regenerate, redraw or re-synthesize the illustration.

Verify these by measurement and against the filed sources, never from memory or from what the rendered image appears to say.

### Free — everything about the design

Orientation, placement, framing, type size, typeface, hierarchy, ornament, and how much negative space the type claims are all yours to decide in service of the goal. You may redesign the typographic layer wholesale rather than dropping English into the Japanese layout's footprint. You may add restrained design elements — rules, flourishes, a circled volume mark — where they extend the source's own design language and make the page read as a real English edition. You may reframe or recrop a cover when that serves the design, provided no protected art is lost.

The test is not "did I preserve the Japanese layout." It is "would a reader believe an English designer made this."

## Inputs and paths

Read `novel.config.md` first. Resolve all paths from it; never hardcode series facts.

For Volume N:

- Originals: `Source/Volume N/images/` or the configured source image directory
- Filed English prose: `English/Volume N/`
- Localization specs: `Editing/Volume N/image-localization/`
- Final renders: `English/Volume N/localized-images/`

Read `glossary.md`, `character-reference.md`, `character-voices.md`, and `style-guide.md`. Do not read `reference-archive.md`.

## Sequential image loop

Process requested images strictly one by one in the user's order. Complete the entire workflow for the current image—open and inspect it, create or audit its spec and prompt, edit the translation embedded in them, render it, visually QA and rerender as needed, save it, and verify the saved file—before opening or reading the next image.

Do not create contact sheets, montages, or other bulk previews. Do not open, classify, transcribe, or create specs for later images in advance. Do not batch or parallelize any image-localization stage.

## Judgement

The rules below describe the usual case. They are not a substitute for looking at the image. When a rule and the artwork disagree, the artwork wins — say so in the spec, give the measured reason, and proceed. Blindly applied defaults produce pages that read as templated rather than art-directed, which is the one outcome this skill exists to prevent.

### Decide what to localize at all

Not every text-bearing image should be re-rendered. Inspect, then classify:

- **Editorial copy** — titles, credits, contents, headers, labels, captions, info panels, diagram text. Localize.
- **Diegetic lettering painted into the artwork** — shop signs, notices, banners, graffiti, packaging in the world of the story. Usually leave in Japanese: it is set dressing, and replacing it repaints the illustration. Localize only when the text carries plot information the reader must read.
- **Trademarks, logos, publisher and retailer marks, colophon and legal matter** — leave verbatim. Check `novel.config.md` for the project's cover/colophon policy before touching any of it.
- **Already-Latin text** — re-set only if it is wrong, such as a banned alias or a misspelling. Correct it in place and keep its design.
- **Glyph-substitute images** — tiny inline PNGs standing in for characters the ebook font lacks. They are typography, not illustration. Never localize; the surrounding prose already handles them.
- **Assets whose text cannot survive the resolution** — micro-copy a few pixels tall, or a full jacket spread that a publisher would re-typeset from layered source. Record the transcription and the English so the work is not lost, then decide not to render and give the reason.

A deliberate no-render decision with its reasoning recorded is a valid, complete outcome. Say which asset the build actually consumes instead.

### Orientation — judgement, not a blanket rule

Default to upright horizontal left-to-right, because that is what English readers expect and what most localized pages need.

Override the default when the source's own design makes vertical or rotated type the art-directed choice — most often a cover or spine whose title runs in full-height columns, or a page whose composition is built around a vertical axis. Two reliable signals: the source already sets *Latin* text rotated on that same asset, or the layout collapses into unrecognizability when flattened to horizontal.

When setting vertical English:

- Rotate whole words and lines as a unit, matching the source's rotation direction. Verify the direction by rotating a crop of the source's own Latin back to horizontal rather than assuming.
- Never stack one letter per line. That is illegible and is a defect regardless of orientation.
- Keep the reading order consistent with the edition's binding direction, and check where the source's own columns sit semantically before assigning phrases to them.

Putting English back where the source's type was has a real fidelity benefit: it covers exactly the art the original covered, instead of exposing one region and obscuring another. Weigh that against legibility, and record which you chose and why.

### Typefaces — name the file, never leave the choice open

A renderer told to use "an elegant display serif" will reach for whatever serif it finds first. That
is usually a body face — Nimbus Roman, DejaVu Serif, Liberation Serif — which at display size reads
word-processed rather than art-directed, and it is a plausible-looking wrong answer that survives QA
unless you compare against the precedent. **Always specify the exact font file path in the prompt.**

An open-licensed (OFL) set is installed at `~/.local/share/fonts/lightnovel/`:

| Use | Files |
|-|-|
| Didone display — titles, covers, frontispiece plates | `PlayfairDisplay-400/500/700.ttf` |
| Elegant old-style display — refined, lighter alternative | `CormorantGaramond-300/400/500/600/700.ttf`, `EBGaramond-400/500/600.ttf` |
| Trajan-style caps — ornate title lettering | `Cinzel-400/600/700.ttf`, `Marcellus-400.ttf` |
| Text serif — dense booklet prose, captions | `Spectral-300/400/600.ttf`, `LibreBaskerville-400/700.ttf`, `CrimsonPro-400/600.ttf`, `Cardo-400/700.ttf` |
| Geometric sans — credits, labels, role lines | `Montserrat-300/400/500/600.ttf`, `Jost-300/400/500.ttf`, `Raleway-300/400/600.ttf`, `Lato-300/400/700.ttf` |

Add to the set rather than settling for a poor match — the families above came from Google Fonts via
the CSS API with an old user-agent, which returns static TTFs rather than woff2. Install into that
directory and run `fc-cache -f`.

Match the sibling volume's face by comparing crops side by side at magnification, not by name.
Restoring a precedent's *internal* hierarchy matters as much as the family: on this series'
frontispiece the connector words are set noticeably smaller than the phrases around them, and a line
set at one uniform size reads flat even when the face is right.

### Placement

Where source type cannot keep its shape, choose the new position by measuring, not by eye:

- Find the actual negative space — block-level detail (local standard deviation) and colour scans locate it reliably; impressions do not.
- Confirm the candidate box is clear of faces, hands, focal objects and signature silhouettes by measuring their bounds.
- Match a sibling volume's treatment for typeface, weight, hierarchy and credit-block shape. Absolute position is dictated per asset by its own artwork; a series looks art-directed when the type system is consistent, not when every cover puts the title in the same corner.

### Rendering method

**Generative image editing is the default. Use it for every illustrated page.**

Drive it through Codex headless, which must invoke its **`imagegen`** tool (namespace `image_gen`) in
image-edit mode — passing the source as the edit target, not as a style reference:

```
imagegen({
  referenced_image_paths: ["<absolute path to the source image>"],
  prompt: "Use case: text-localization\n
           Asset type: <what the page is>\n
           Input image: the provided image is the edit target.\n
           Primary request: <what to replace, region by region>\n
           Text invariants (verbatim): <every exact string>\n
           Constraints: <canvas, composition, art, typography to preserve>"
})
```

State in the prompt to Codex that it **must call `imagegen`**. Left to itself it will reach for
Pillow, because a deterministic script is easier to verify — and it will report success on a page
that looks pasted-together.

**Do not mask the Japanese, fill the hole, and typeset English over it.** That composite route is
what produces a page that reads as a translation patch: flat lettering sitting on a blurred smear
where the art used to be, with none of the integration into lighting, texture and depth that makes a
page look drawn in English. It is a rendering method, not a localization.

**Compositing is the narrow exception**, allowed only where there is no artwork to reconstruct —
type on a flat field, contents pages, info panels, booklet text. If a page has a flat ground under
every string and no art is touched, a composite is exact and cheap; take it. The moment a string
sits over painted art, go generative.

When compositing does apply, its failure mode is the fill: naive neighbour-averaging leaves blocky
mosaic and smears. Use a multi-scale push-pull fill with bilinear upsampling, and inspect the filled
area at magnification *before* typesetting over it, so the fill is judged on its own rather than
excused by whatever the type happens to cover.

Generative editing has its own failure mode, and it is worse: **silent art damage.** Faces shift,
silhouettes change, details get invented, and the model reports success anyway. So verification is
non-negotiable and is yours to do, not the renderer's:

- Never accept a renderer's self-report. It will claim the characters are intact because two witches
  and a boy are still present, without ever comparing against the source.
- Compare protected regions against the source yourself. On a composite they must read exactly zero
  difference. On a generative edit, compare crops side by side at magnification and confirm no
  feature was added, moved or restyled.
- Read every string off the *rendered image*, not off the prompt you sent. Generative renderers
  rewrite names and drop word divisions while reporting the text as correct.
- If a generative edit damages the art past repair after a targeted retry, say so and fall back to a
  composite — but record that the fallback happened and why, rather than presenting it as the plan.

**Expect the renderer to repaint the entire canvas, and plan to merge its work back.** `imagegen`
does not edit pixels in place; it regenerates the page. Even a flawless-looking result will have
redrawn faces, hands and props far from any text — details vanish, eyes and linework shift. Measured
against the source it reads as a global difference, not a local one, so a whole-page accept is a
whole-page repaint.

The fix keeps both halves of what you want. Take the model's work only where text lives, and restore
the illustrator's pixels everywhere else:

1. For each text region, take the union of the **source's Japanese block** and the **render's English
   block**, padded. Every region is a rectangle around type, never around a face.
2. Build the alpha from those rectangles **dilated, then blurred** — dilate by about twice the
   feather. Alpha must reach a solid 1 across the whole block; if it only ramps up at the edge, the
   source's own lettering ghosts through under the new type. That ghost is easy to miss at page
   scale and obvious at magnification, so check the nameplates specifically.
3. Colour-match each region before blending: take the mean difference between source and render over
   a ring just outside the rectangle, and offset the render by it. The regenerated page carries a
   global colour shift that would otherwise seam at every join.
4. Composite, then re-measure. Protected art must come back to near-zero difference — only JPEG
   re-encode noise, well under 1.

This is not the forbidden mask-and-paste: the fill under the removed Japanese is the model's genuine
reconstruction, and the typography is the model's. You are discarding only its repainting.

**On a flat ground, merge the glyphs, not the region.** Where type sits on paper, a panel or a flat
field, replacing the whole rectangle imports the renderer's version of that ground — and a generated
paper texture is measurably flatter and darker than a real one, which reads as a rectangle on the
page. Instead: refill the band from the source's own blank ground nearby, lift the new lettering
from the render as an alpha matte, and paint it in an ink colour sampled from source text that was
left untouched. Check it by measuring local standard deviation inside the band against untouched
ground — a washed-out texture is the tell, and it is invisible until you boost contrast.

When a page has an untouched line beside the edited one, it is your reference for face, tracking,
cap-height, colour and alignment. Say so in the prompt, and compare against it afterwards.

**Do not burn runs on an exact count of repeated glyphs.** A run of dots, dashes or stars is the one
thing these models cannot hold: ask for twelve and you get 13, 15, 17, 22, drifting differently each
attempt — and the renderer will misreport the count in its own summary, so check it yourself by
counting blobs. Where the count is semantic (a numbered list, a data label) keep re-rendering. Where
it is cosmetic — a silence beat, a trailing ellipsis — take the closest attempt, record the
deviation in the spec, and do not re-roll strings that are already correct to chase it.

Do not repair small text defects by erasing glyphs and reconstructing the background by hand.
Interpolating vertically across a band smears any edge crossing it, and a threshold-and-fill leaves
halo rings where the anti-aliasing sat. Re-render and merge again instead; if a defect is cosmetic
and a re-render would risk strings that are already correct, keep the good render and record the
deviation.

## 1. Create or refresh specs

For the current image only, create or refresh its localization spec directly in the main agent. Use the configured paths and reference files. Verify the spec is nonempty on disk before rendering the image.

If a spec already exists, audit it against the current image and filed English prose. Never render uncertain or invented text. Keep illegible regions unchanged and record the uncertainty.

Each spec must contain:

- source image path and type
- verbatim Japanese by visual region
- exact glossary-consistent English by region
- a production-ready edit prompt
- an editing-and-refinement record confirming both post-draft passes
- notes and uncertainties

## 2. Build an English-native edit prompt

Render through Codex headless calling `imagegen` in image-edit mode, as specified under **Rendering method** above. Treat the original image as the edit target, not merely a style reference. Instruct Codex explicitly to invoke `imagegen`, and forbid a Pillow mask-and-typeset composite unless the page qualifies for the flat-ground exception. Render one image at a time so each result receives visual QA before the next.

Demand a finished page that looks designed for an official English edition:

- Protect the artwork absolutely: characters, faces, anatomy, poses, clothing, objects, background, lighting, palette and texture. The typographic layer above it is yours to redesign.
- Choose each region's orientation deliberately; see [Orientation](#orientation-judgement-not-a-blanket-rule). Never use one-letter-per-line stacking, mirrored text, generic subtitles or meme captions — those are defects at any orientation, and none of them serve the goal.
- Specify each region's source-matched color, font category and character, scale, weight, outline/shadow/glow, alignment, hierarchy, and permitted negative-space area.
- Preserve dialogue, narration, titles, names, reactions, labels, and technical text as separate visual classes.
- Quote every English string verbatim. Require exact capitalization, punctuation, apostrophes, hyphens, ellipses, names, and glossary forms. Permit no paraphrase, omission, duplication, or invented text.
- Require professional kerning, leading, optical alignment, balanced line lengths, and natural phrase-based wrapping. Avoid widows, orphans, isolated punctuation, cramped leading, excessive tracking, and ragged ladders of one- or two-word lines.
- Protect faces, eyes, hands, bodies, named objects, and focal details. Reduce type size moderately before allowing text to cover important art.

### Dense-text layout

For prose-heavy images:

1. Preserve the source's semantic paragraph and speech-unit boundaries.
2. Allocate all text regions before selecting font size.
3. Keep related prose in compact, balanced blocks or columns that follow the composition and intended reading order.
4. Use consistent within-paragraph leading and inter-paragraph spacing of roughly 0.6–1.0 line. Paragraph spacing must be visibly larger than line spacing.
5. Use moderate, consistent body size. Never solve fit by crushing leading/tracking or scattering prose across the art.
6. State block order and alignment explicitly.

For graphs and diagrams, lock every data point, number, axis, gridline, connector, symbol, and geometry. Change only the listed labels.

## 3. Edit and refine the embedded translation

Once the initial production prompt has been created, perform two separate, mandatory post-draft passes on every English string embedded in the spec and prompt before rendering.

### Pass A — source and continuity edit

Check the translation line by line against the visible Japanese, filed English prose, glossary, character references, voice rules, and style guide. Correct mistranslations, omissions, additions, inconsistent terminology, name order, honorifics, punctuation, capitalization, register, and voice. Preserve the source's meaning, tone, hierarchy, and visual-region boundaries; do not shorten, paraphrase, or embellish merely to make typesetting easier.

### Pass B — publication-English refinement

Reread the complete English independently as finished copy, not as a translation exercise. Rewrite literal calques, stiff syntax, repetitive sentence openings, dangling modifiers, unnatural collocations, and computer-like phrasing while preserving every source fact. Read dialogue and display copy for character and energy, and read dense prose as connected paragraphs rather than isolated sentences.

For living-character profiles, use past tense for completed backstory and present tense for current traits, abilities, habits, relationships, and circumstances. Follow source chronology for deceased characters or explicitly historical profiles. Apply the same convention consistently within and across volumes.

Write the edited wording back into both the exact-English section and every quoted occurrence in the production prompt so they match verbatim. Then reread the completed spec and verify that:

- every Japanese string has one certain, source-supported English rendering
- the English is accurate, natural, glossary-consistent, and publication-ready
- the exact-English copy and prompt contain identical final wording
- uncertainties remain explicitly recorded and are not guessed away
- the spec records `Pass A: complete`, `Pass B: complete`, and `Pass C: complete`

Do not render until Pass A and Pass B are complete, their completion is recorded in the spec, and the edited spec is nonempty on disk.

### Pass C — external review by Codex (mandatory)

Never render on your own reading of the Japanese alone. After Pass B, send the **raw Japanese and
the proposed English together** to Codex headless for an independent translation review, region by
region, and apply the result before rendering.

Build a single review file containing, for every visual region on the page:

- the region label and its verbatim Japanese, exactly as transcribed
- the current proposed English for that region
- the locked project constraints the reviewer must respect: register ceiling, honorific policy,
  name order, romanization rules, and every glossary form that appears on the page

Instruct the reviewer to flag mistranslations, dropped or added nuance, translationese, invented
imagery, wrong idiom, and punctuation errors, and to return a corrected English block in full.
State explicitly: **do not generate any image, do not call imagegen** — this pass is text only.

Send it with the project's standard headless invocation:

```
codex exec -m gpt-5.6-sol -c model_reasoning_effort=medium -s workspace-write \
  --skip-git-repo-check -C "<project root>" -o review.out - < review.txt > review.log 2>&1
```

Adjudicate the response rather than accepting it wholesale. Take its substantive corrections. Reject
any suggestion that contradicts a locked project decision — a glossary form, a name-order rule, or a
deliberate typographic choice the reviewer could not see — and record in the spec both what was
taken and what was overridden, with the reason.

The spec records `Pass C: complete` alongside the other two. Do not render until all three passes
are complete and recorded.

## 4. Render and inspect

Inspect every generated result at full available detail before accepting it. Check:

- every required string and punctuation mark is exact
- **every name of a real person is checked character by character against `novel.config.md` and the filed specs** — read it off the rendered image and compare, never assume the renderer used what you gave it
- no banned alias survives anywhere, including in text the source itself printed in Latin
- no Japanese targeted for replacement remains, including anti-aliased stroke fringes
- no extra or duplicated text appears
- every region's orientation matches the treatment the spec chose and justified, and no text is stacked one letter per line
- any masked-and-filled area is free of blocking, smearing and visible seams
- colors and typography preserve the source hierarchy
- line breaks are phrase-based and balanced
- paragraph spacing exceeds line spacing
- nothing is clipped or overlapping
- focal art and data geometry are unchanged
- the page plausibly looks originally designed in English

Reject and rerender on any failed check. Iterate with one targeted correction at a time and repeat the invariants in every retry. Dense text, incorrect colors, generic pasted-on typography, or damaged art are not acceptable partial success.

## 5. Save exact filenames

Keep originals untouched. Save each accepted render under:

`English/Volume N/localized-images/<exact-original-filename>`

Preserve the complete original filename, including extension. The built-in image tool may emit PNG; when the original is JPEG, convert the accepted output to a real JPEG with high-quality 4:4:4 sampling before saving it as `.jpg`. Never place PNG bytes behind a `.jpg` extension.

Verify every requested output is nonempty and readable. Compare the requested filename list with the localized folder and report `PRESENT` or `MISSING` for each.

## Done criteria

The task is done only when:

- every requested text-bearing image has a verified spec
- every spec's embedded English has passed the dedicated editing pass
- every requested image passes visual and text QA
- every accepted image exists in `localized-images/` under the exact original filename
- originals remain unchanged

Report the saved paths, unresolved text if any, rerenders performed, and any image that did not pass QA.
