# Chapter 18 — Edit Log

### Accuracy Fixes
- No changes required; the draft exactly matched all five source lines and contained no prose.
- [polish] No changes required; the image-only scope contained no English prose to polish.

### Register and Flow
**Image-only scope:** Accuracy and polish passes completed; no narrative, dialogue, or register-bearing text was present.

### Formatting Confirmed
- All three inline image markers were preserved exactly, in source order, with the same blank-line spacing: `![s-h1.jpg](images/s-h1.jpg)`, `![s-h2.jpg](images/s-h2.jpg)`, and `![s-p003.jpg](images/s-p003.jpg)`.
- No title heading, invented prose, scene breaks, glossary terms, furigana, footnotes, or `## Translator Notes` section was present or required.

## Source-image continuation (s-p016–s-p038)

### Accuracy Fixes
- **s-p021 (鮫島の趣味は…粛清)**: "cleaning fish" → "purges" — accuracy
- **s-p031 (タラの芽)**: "taro shoots" → "angelica-tree shoots" — accuracy
- **s-p031 (今回は干し椎茸にする)**: "dry them into taro stems" → "make dried shiitake" — accuracy
- **s-p034 (ほかの花やさんにおじさんとられる)**: "another florist is with you" → "another florist takes you from me" — accuracy
- **s-p033 (もっとたいせつにして)**: "Treat me more importantly" → "Make me more important to you" — polish
- **s-p021 (渡鴉)**: plain "Watarigarasu" → semantic ruby on each source occurrence — glossary
- **s-p010 carryover (姐御)**: "the boss's lady" → "the Boss Lady" — glossary
- [polish] **s-p032–s-p038**: tightened literal OCR draft into Ori's blunt first-person cadence while preserving sentence energy — polish
- [polish] **s-p023–s-p029**: standardized dossier labels, scores, paper titles, and list parallelism — polish

### Register and Flow
**Ori Kenshi:** kept casual, technical, defensive, and socially oblivious; narrative action stayed past tense while immediate reactions remained natural speech tense.

**Fuyo:** kept simple child vocabulary, jealousy, repetition, praise-seeking, and the source's “Uncle” / “Blue Witch” address forms.

**Booklet dossiers:** kept dry institutional structure and plain technical register without converting entries into elevated prose.

### Formatting Confirmed
- All 23 requested image markers, `s-p016.jpg` through `s-p038.jpg`, are present once and in ascending source order.
- Section order, guard scores, numbered futures, paper lists, blockquoted directive memos, semantic ruby, and existing colophon placement verified.
- No in-file title heading, macrons, raw source furigana, or added translator notes.

## Re-edit Pass — 2026-09-29

The booklet JP exists only as page images (s-p011–s-p038); it was OCR-transcribed and verified before editing. Hard-wrapped paragraphs were first joined to one line each (rendering unchanged). The prose was then re-edited line by line against the JP in three sequential segments by ln-segment-reeditor subagents, and each segment passed check_reedit and the chapter gates.

### Segments
- **s1** — s-p011 up to `## Story Settings` (timeline, magic items, chapter commentary): ~60 edits. Key fixes: the 遠距離 joke restored; "ice, fire, and grass"; omitted clauses restored; 組長 → "gang boss"; timeline rows as present-tense headlines.
- **s2** — `## Story Settings` up to `## Short Stories` (settings, Arataki Group dossiers, tournament, communities, paper archive, memos): ~75 edits. Key fixes: "Three-Pronged Witch" → "Mitaka Witch" ×2; 魔法暴走魔法 → "magic-rampage spell"; 甘い汁 kept as "sweet juice"; memo order on s-p031 matched to the JP (wasabi before hair dye); "5 centimeters"; Lost Mist.
- **s3** — `## Short Stories` up to `## Colophon` ("Flower Language"): ~120 edits. Key fixes: shoulder, not leg; tendril, not arm; "Don't ask me"; the Ori Kenshi/kenshi pun glossed inline; the 拍手/搾取 slip rendered "Stop exploding me!" / "*Exploiting.*"; Fuyo's ♡ restored.
- Flow (whole file, narration): short sentences 27.3% → 23.1%; runs of 3+ short 13 → 6; words 10072 → 10530.

### Codex Critique Debate
Independent critique by Codex (gpt-5.6-sol, high reasoning, read-only) against the JP; the editor debated each finding (concede / push back / counter) in Codex's own session and applied what survived on the merits.

Codex: 272 reviewed, 18 flagged. Round 1: 4 conceded, 5 pushed back, 9 countered. Codex after round 1: 5 withdrew, 8 accepted, 0 maintained, 1 countered. Round 2: no.
Final: 13 changed, 5 kept as re-edited.

Lead rulings for the debate: magic-item profile properties stay present (they were present as filed); past events inside them stay past; dossiers stay past; document-framing "Below are…" stays present.

- **F1** — APPLIED — glossary — 猿山の大将 back to the locked idiom
  - Final text: "Even so, Kojiro undeniably had enough charisma to be a big fish in a small pond."
- **F2** — APPLIED — accuracy (tense part rejected) — unique Cyanos, no article; item profile stays present per lead ruling
  - Final text: "The Blue Witch is formidable enough on her own; wielding Cyanos, built for her alone, she is unstoppable."
- **F3** — KEPT — tense — Wise Wand entry was present as filed; standing properties/appraisal stay present (Codex withdrew)
  - Why kept: item-profile ruling; だろう kept as "probably".
- **F4** — APPLIED — accuracy (tense part rejected) — 安全確保 = "ensure security", not "secure their territory"
  - Final text: "The Lake Biwa Pact's hawks wanted to spread it widely to expand their sphere of influence and ensure security, while the doves, worried about a rise in drug addicts, kept the formula secret and clashed with the hawks."
- **F5** — APPLIED — tense (in-sentence mix) + restored 与えた — Ori's view goes present to match the craftsmanship clause
  - Final text: "To Ori, who made it, it is just a little toy he gave his pet, but the craftsmanship is remarkably elaborate: a 1.1x amplification ratio, a backlash-prevention mechanism, magic-school customization, a whitewood handle, and more."
- **F6** — KEPT — tense — was present as filed; making stays past, design/performance present (Codex withdrew)
  - Why kept: "It may have been a rush job, but" is the idiomatic concessive for とはいえ, not a hedge.
- **F7** — APPLIED — accuracy (tense part rejected) — "its components" referent fixed; Codex's counter accepted
  - Final text: "The weft is steel sheep wool steeped in molten Gremlin for seven days and seven nights, allowing the Gremlin's components to soak into the wool."
- **F8** — KEPT — accuracy — 個体 is number-neutral; 複数のコロニー supports plural; OLD already plural (Codex withdrew)
  - Why kept: singular would imply one mother for several colonies, which the JP doesn't say.
- **F9** — KEPT — tense — document-framing "Below are…" stays present (lead ruling; Codex withdrew)
  - Why kept: "Below were" is unidiomatic for a list directly below.
- **F10** — APPLIED — worse — clunky echo smoothed, 確実に…確実に echo kept
  - Final text: "Its policy was to make sure it killed every enemy it could be sure of killing."
- **F11** — APPLIED — glossary — 魔力欠乏失神 locked form, as a parenthetical inclusion (含む)
  - Final text: "Its fights took quite a long time, but it was the only district unit to finish the exercise with zero personnel ruled unable to fight, magic-power-depletion fainting included."
- **F12** — APPLIED — glossary — 呪殺魔法 locked "death-curse magic"
  - Final text: "It killed the strongest golem instantly with a ritual incantation of death-curse magic, then surrendered right afterward."
- **F13** — KEPT — tense — document-framing "Below, in descending order, are…" stays present (lead ruling; Codex withdrew)
  - Why kept: tail "had accepted to date" is already correct.
- **F14** — APPLIED — accuracy — 悔しがっていた is frustration, not fury
  - Final text: "When I'd told her about the miraculous blue rose, she had tried her hardest to make one and failed, and she'd been terribly frustrated about it."
- **F15** — APPLIED — worse + restored dropped 言う
  - Final text: "When I looked back, Fuyo was frowning, and she spoke with obvious reluctance."
- **F16** — APPLIED — worse + restored dropped やる気を漲らせる; だけ kept as "all it took"; nod = approval (preceding うむ、うむ)
  - Final text: "A little praise was all it took to blow away the kid's bad mood and fire her up. I was nodding in approval when Hiyori, who had been watching in silence, leaned in and whispered in my ear."
- **F17** — APPLIED — accuracy — added vocative "kid" removed (お前 covered by "You've got")
  - Final text: "Fuyo and I high-fived, hand to tendril. You've got a real talent for ikebana or bonsai."
- **F18** — APPLIED — worse — grammar fixed, game-stat joke kept, ようだ = "apparently"
  - Final text: "But my communication stat apparently wasn't leveled up enough to decode it."

### Lead Additions
- 不要の嫌疑 (JP s-p037): the name pun glossed inline: "Fuyo, who by the same reasoning stood accused of being *fuyou*, "unneeded," didn't get it either."
- ヒヨドリバナ (JP s-p038): translator note [^1] added: the flower's Japanese name echoes Hiyori's, and it is asked for in blue.
- check_reedit: RESULT: PASS apart from the deliberate note addition (headings/footnote counts 0 → 1).

### Reference Changes
- glossary.md: added 三鷹の魔女 = "Mitaka Witch" (Three-Pronged Witch, Witch of Mitaka banned); 白木 row context clarified as the generic sense ("pale, unfinished wood"), distinct from the Flower Witch's whitewood.
