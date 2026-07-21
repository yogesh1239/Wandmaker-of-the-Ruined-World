# Schema: `glossary.md`

Per-novel term-mapping table. Seeded at `/setup-novel`, extended cumulatively by the updater after each chapter. `core/scripts/check_consistency.py` parses this file to enforce that only the EN rendering is used and no banned rendering appears in translated text.

## Required table

```
| JP | EN | Aliases/Banned | Gender/Context |
```

- **JP** — the source term exactly as it appears (kanji/kana; furigana form if that is what appears).
- **EN** — the **one** permitted English rendering. This is the ONLY rendering allowed in translated text; no synonyms or variants.
- **Aliases/Banned** — comma-separated list of forbidden EN renderings the translator/editor must NOT use (common wrong choices, earlier drafts, MTL defaults). No pipe characters. May be empty.
- **Gender/Context** — for character names: `Male` / `Female` / `Unknown`. For abilities/weapons/techniques/locations/organizations/titles: leave gender out, note context.

## Rules
- Romanization: no macrons (vowel-doubling: ō→ou, ū→uu, ā→aa, ī→ii, ē→ee).
- Only add terms that actually appear in translated text — do not speculate.
- Keep the EN rendering stable across the whole novel once added.

## Filled example

| JP | EN | Aliases/Banned | Gender/Context |
|-|-|-|-|
| 天雷斬 | Heavenly Thunder Slash | Sky Lightning Cut, Tenraizan | attack / signature technique |
| 灰原 | Haibara | Grey Field, Ashfield | Female / protagonist's classmate |
