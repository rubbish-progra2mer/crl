# Nearest Prior Work v015

## Inherited search result

v015 inherits the complete v014 nearest-prior search because it changes no scientific computation. No new literature claim is introduced by making the runner's input cardinalities phase-configurable.

| Source | Overlap | Surviving distinction |
|---|---|---|
| ToolFailBench, arXiv:2607.04686v1 | Exact benchmark, failure taxonomy, released traces/judges, and disclosure that exact rules can miss faithful paraphrases | Tests one released fabrication-before-required-grounding short-circuit on fixed bytes |
| Official `evaluation/detect.py`, commit `c8be7fb0...` | Exact target implementation and predicates | Does not evaluate required-grounding precedence against two-judge unanimity |
| Bulian et al., 2022, *Tomayto, Tomahto* | Complete collision with broad semantic answer-equivalence claims | Learned answer-equivalence metric; no ToolFailBench classifier-order audit |
| Kamalloo et al., 2023, *Evaluating Open-Domain QA* | Complete collision with generic exact-match critique | No structured tool-return taxonomy or required-grounding precedence |
| BFCL changelog at Gorilla `6ea57973...` | Collision with deterministic string normalization | RGP performs no normalization and changes decision precedence only |
| ToolFailBench judge prompts | Same desired evidence-attribution semantics and released reference labels | RGP is a deterministic measurement correction evaluated against those labels |

## Collision judgment

- Exact required-grounding-before-fabrication repair was not found in the fixed repository, its complete Issue/PR listing, commit history, exact-title searches, or the directly read nearest sources as of 2026-07-23.
- General exact-match brittleness, semantic equivalence, and benchmark normalization are prior work and cannot be claimed.
- The novelty ceiling is a focused benchmark correction or technical-note result.
- v015's execution-contract repair has no independent research novelty.

## Fixed source bytes

| Path | SHA-256 |
|---|---|
| `crl_agent_v3/knowledge_base/papers/P039_toolfailbench.pdf` | `6588AF66FD477D9764C20C52C2ADB7D92FCBF6A788FE09713BC71916862D3009` |
| `sources_v014/ToolFailBench/evaluation/detect.py` | `AEE4D77596BDACB9025D85CCCDE766FF2A2DDBE1A291B6C143EA46D22863DBD0` |
| `sources_v014/ToolFailBench/evaluation/judges/prompts/base_rubric.md` | `A07F89A088A1F822FCAB36C2370B9917598FE0353B2B4B92C327F513A7FA50E9` |
| `sources_v014/ToolFailBench/evaluation/judges/prompts/variant_a_decision_tree.md` | `F481AC6F12AA25F675DF582941F955167293CF3E0F4E07E4D364DDA75F872325` |
| `sources_v014/ToolFailBench/evaluation/judges/prompts/variant_b_evidence.md` | `15B3BD429C3A2E317A6DCC8B8E322B7AB8B0C0FC3C5E1631C9FFE69CE2319F63` |
| `sources_v014/Bulian_2022_answer_equivalence.pdf` | `BD320A5183A6FB507F4E3EBFBFF27EB76AF647E68F55980EA4C6762907F62B40` |
| `sources_v014/Kamalloo_2023_evaluating_open_domain_qa.pdf` | `61676B02AA277893A9AD9A4C9CF691A29ACE32A47E6FE3B024D598632D318BD2` |
| `sources_v014/BFCL_CHANGELOG_6ea57973c7a6.md` | `27CBABDB95424B5B03B6B9B34EEBDF99A5C5B64FC5D2964726EF42ECBAC104DB` |

## Forbidden novelty statements

Do not claim semantic equivalence, new normalization, human-gold labels, proof that required values exclude every fabrication, invalidity of all ToolFailBench rankings, generalization beyond the fixed data/judges, or novelty for v015's execution-only fix.
