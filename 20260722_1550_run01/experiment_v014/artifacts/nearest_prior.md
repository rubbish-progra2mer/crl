# Nearest Prior Work v014

## Search question

Has prior work already disclosed or repaired ToolFailBench's exact deterministic classifier order, or proposed the same required-grounding-before-fabrication computation?

## Direct comparison

| Source | Core contribution or disclosure | Exact overlap | Remaining v014 contribution |
|---|---|---|---|
| ToolFailBench, arXiv:2607.04686v1 | Defines the failure taxonomy, releases deterministic plus two-judge labeling, and acknowledges that exact rules can miss faithful paraphrases | Exact benchmark, data, labels, and broad limitation | Tests a specific released code-order short-circuit and a one-branch deterministic repair on frozen released traces |
| Official `evaluation/detect.py`, commit `c8be7fb0...` | Uses `<30%` global mock-leaf coverage plus two structured-keyword hits before required-value checking | Exact target implementation | Does not compare required-grounding precedence against independent unanimous judges |
| Bulian et al., 2022, *Tomayto, Tomahto* | Formalizes answer equivalence beyond token matching and trains BEM | Complete collision with broad semantic-equivalence claims | Different task and learned metric; no ToolFailBench code-order audit |
| Kamalloo et al., 2023, *Evaluating Open-Domain QA* | Finds semantic equivalence to be a major exact-match failure and compares regex, human, and semantic evaluation | Complete collision with broad exact-match critique | No structured tool-return failure taxonomy or required-grounding precedence |
| BFCL changelog at Gorilla `6ea57973...` | Records string standardization by removing whitespace and selected punctuation for more robust AST evaluation | Collision with generic deterministic normalization | RGP performs no normalization and changes a failure-mode decision order |
| ToolFailBench two-judge prompts | Attribute evidence to tool returns with formatting tolerance and check unsupported structured values | Same desired semantics and released reference labels | RGP is a low-cost deterministic repair evaluated against, not a replacement for, those judges |

## Collision judgment

- **Exact code-order repair collision:** not found in the fixed repository, its full Issue/PR listing, its commit history, exact-title searches, or directly read nearest sources as of 2026-07-23.
- **General exact-match brittleness collision:** complete. v014 cannot claim discovery of surface-form brittleness.
- **Semantic-evaluator collision:** complete. v014 cannot claim a new semantic judge, answer-equivalence model, or formatting-tolerant matcher.
- **Benchmark-normalization collision:** substantial. v014 must not frame case folding or punctuation handling as novel.
- **Surviving contribution:** a narrow measurement/reproducibility claim that the target's coarse fabrication proxy can override its own satisfied required-evidence contract, and that reversing only those two predicates improves deterministic diagnostic agreement on exposed and untouched generator-model partitions.
- **Novelty ceiling:** a focused benchmark correction or technical-note result, not a new agent architecture or general evaluation theory.

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

v014 must not claim:

- invention of semantic answer equivalence or tolerant matching;
- that ToolFailBench failed to acknowledge exact-rule brittleness;
- that the two released judges are human ground truth;
- that required-field satisfaction proves the absence of every extra fabrication;
- that published ensemble leaderboard values are invalid before that consequence is directly measured;
- generalization beyond the fixed released trace data and two fixed judge models;
- absence of all private, unpublished, or future corrections.
