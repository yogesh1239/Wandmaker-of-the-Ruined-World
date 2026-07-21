# LLM Literary Translation Best Practices (2025–2026) — digest for quality machinery

## Pipeline design

- **TransAgents** (arXiv 2405.11804): multi-agent translation company; the durable takeaways are a **persistent per-project style guide** + **running chapter/plot summary** maintained across chapters, and that d-BLEU **anti-correlates** with human literary preference — never gate on n-gram metrics.
- **Reflection pattern** (Ng's translation-agent): translate → explicit critique → apply. Matches our editor-with-edit-log; the critique should be explicit before rewriting.
- **Iterative refinement ceiling** (arXiv 2306.03856): repeated refinement drifts from source. Cap at ONE polish iteration.

## Anti-translationese (the big one)

- **Lost in Literalism** (arXiv 2503.04369): translationese comes from literal-faithfulness bias. **Self-polishing the English output cut translationese 43%→25%** — the single most effective lever. Adding "translate naturally" adjectives to the translate prompt did NOT help (sometimes hurt). The task FRAMING ("polish this English to read as native-authored prose") does the work, not adjectives.
- **Emotion profiling** (arXiv 2606.10113): two systematic failures — emotional flattening and register drift (toward neutral OR elevated), both **worst in dialogue and character voice**. QA must over-sample dialogue + high-emotion passages.

## Terminology consistency

- WMT25 terminology task + industry consensus: prompt-instructed glossary use is **probabilistic only**. Required: (a) inject only segment-relevant glossary entries into prompts, (b) **deterministic post-hoc compliance check** as a gate, (c) glossary correctness is load-bearing — models faithfully enforce obsolete entries.

## Character voice

- LLMs default to homogenized narrative voice across characters (Ken Liu vs ChatGPT study). Per-character voice profiles must be explicit AND enforced by a checker; the model won't maintain distinction on its own.
- Style-rewrite with explicit voice planning before rewriting dialogue (arXiv 2603.05933) helps.

## QA / evaluation

- **GEMBA-MQM v2**: LLM-as-judge emitting **error spans classified by MQM type** (accuracy/fluency/style/terminology) **× severity** (minor/major/critical). Single judgments are noisy — aggregate multiple independent judgments for reliability.
- **JP-TL-Bench** (arXiv 2601.00223): JP→EN-specific failure classes to check explicitly — **zero-pronoun/dropped-subject resolution, keigo→register mapping, information-density compression**. Anchored pairwise comparison beats absolute scoring.
- **Rubric-MQM**: chapter-specific rubric derived from project conventions beats a generic rubric.

## Applied in this harness

1. Editor = accuracy pass (vs source) + ONE polish pass framed as "make it read native-authored," register-capped, changed spans re-verified against source.
2. `check_consistency.py` deterministic glossary/name/honorific gate.
3. QA auditor: MQM-classified error spans; over-samples dialogue/high-emotion; checks zero-pronoun recovery, keigo→register, compression (JP) / dropped-subject, address-term mapping, chengyu (CN); voice-profile conformance per character-voices.md.
4. `style-guide.md` per novel: style guide + running plot summary, updater-maintained.
5. No BLEU/n-gram gates anywhere.
