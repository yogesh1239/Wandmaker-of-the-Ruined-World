# Volume 2 Image-Localization Verification Ledger

Verifier: fresh independent low-reasoning agent, read-only visual comparison of source + spec + output.  
Run date: 2026-07-24.  
Checks: exact listed text, canonical terms, removal completeness, placement, legibility, artwork preservation, and source/output dimensions.

| Output | Dimensions | SHA-256 | Result | Finding |
|-|-|-|-|-|
| `cover.jpg` | 1800×2560 | `c0aa9c3f4a1490cb1c070ed91d4d4ac87130a8e665a665036f8e21149895f58a` | **FAIL** | Large Japanese title `崩壊世界の魔法杖職人` remains visible; remove it and restore the artwork beneath while retaining the English title once. |
| `i-bookwalker.jpg` | 1443×2048 | `7cd722f5a19b77ac2c3b9e336a39ecc9803b7a4263dd236f4e8253f15adf2a4a` | PASS | Unchanged English logo; dimensions match. |
| `kuchie-001.jpg` | 1440×2048 | `579a248863f7fe4fae0d82f5ec0ed67253e451e13723e420d7c29257d44a58f1` | PASS | Exact specified text and canonical title/name order; art preserved. |
| `kuchie-002.jpg` | 2048×1473 | `e597857745827075b9b4853801fd2a0a5d8f89c5395106b1741c5728399cc762` | PASS | Exact dialogue and names; listed Japanese removed; art preserved. |
| `kuchie-003.jpg` | 2048×1474 | `2eb5c4e35856ad50f56c182fca4433b080c3dc6e9a081d36c4a1ffa6e23321e3` | PASS | Exact dialogue/narration and names; paragraph layout legible; art preserved. |
| `kuchie-004.jpg` | 2048×1473 | `5f68784edca484354edda2ea3cb1c951ad1883ab7af34135d329747182598009` | PASS | Exact dialogue/title; listed Japanese removed; art preserved. |
| `kuchie-005.jpg` | 1440×2048 | `54b67981dd76eb4d18eec3dfc42637df9cd4cc15f07c09c28996f8c2ebb064ae` | PASS | Canonical title normalized; paper/art preserved. |
| `p256.jpg` | 1439×2048 | `943e1d0223f602b134678998895d3d964f84461240b1956a01cb8bd34f379774` | PASS | Exact cough text; language-neutral punctuation retained; art preserved. |
| `p271.jpg` | 1485×2048 | `f0c32bce77ae5790e35f41b741b5365b9b3555b6fb841420163ded83dd44c5b8` | PASS | Exact axis labels; graph data and geometry preserved. |
| `s-h3.jpg` | 1440×2048 | `5d1a5f6029e92a2dab4f960045ab6fdd4676e6ee0677d0b859f4d50bbe872a8d` | PASS | Colophon unchanged by policy; dimensions match. |
| `titlepage.jpg` | 1439×2048 | `0a10287e91989737c6c24c59a0c37f9eaab148f0573a9f1a98aec22d858dde97` | PASS | Exact title/edition/credits; listed Japanese removed; composition preserved. |
| `toc-001.jpg` | 1439×2048 | `52b230483b928bdab0520362af9a74f4f042aaf42a6da8aa8422d23daa6dc949` | PASS | All 17 configured chapter titles and credit are exact and legible. |

## Reverification rule

Every revised or newly rendered file must receive the same independent source/spec/output visual pass. Append a new ledger row with its SHA-256; do not overwrite this historical result.
