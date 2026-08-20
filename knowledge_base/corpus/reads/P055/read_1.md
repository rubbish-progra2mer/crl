# P055 first read — planning formalizers under natural-language constraints

Status: `DRAFT_BEFORE_INDEPENDENT_READS`  
Reader: main Codex  
Read date: 2026-07-20 (Asia/Shanghai)

## Canonical source and bytes

- Title: Language Model as Planner and Formalizer under Constraints
- Authors: Cassie Huang, Stuti Mohan, Ziyi Yang, Stefanie Tellex, Li Zhang
- Venue: ACL 2026, Volume 1: Long Papers, pages 13724–13756
- Canonical ID: ACL Anthology `2026.acl-long.624`; arXiv:2510.05486
- PDF: `knowledge_base/staging/papers/P055_planner_formalizer_constraints.pdf`
- PDF SHA-256: `0d21a03ded6ae892d0818ec8e0f453b3ca0fc1c4cb3e30ae2c3b182c40868207`
- Parse check: 33 pages, 96677 extracted characters, zero empty pages

## Scope and lineage

P055 is the direct constraint-stress successor of P054 and a 2026 negative/measurement anchor. It tests whether direct planners and formalizers remain robust after one short natural-language constraint changes initial state, goal, action sequence or intermediate state validity. Its role is Failure and strong-baseline definition; syntax-error revision is an experimental condition, not an admitted environment-feedback/recovery Operator.

## Changed evaluation computation

CoPE pairs natural-language domain/problem descriptions and an action header with one categorized constraint. The LLM either produces a plan directly or emits PDDL 1.2, PDDL3, Python/Z3 SMT code or LTL for downstream solving. Formalizers are tested with direct generation, generate-then-edit, and up to three syntax-error revision attempts. Final plans are validated against the benchmark's ground-truth PDDL.

## Experimental evidence

- CoPE defines four constraint categories: initial, goal, action and state; 100 manually annotated constraints are paired with representative problems in BlocksWorld and a fully observable CoinCollector conversion.
- Across seven model variants and multiple method/formal-language combinations, a one-line constraint consistently degrades and often roughly halves correctness; even Gemini-3-Flash drops by about 30% overall.
- In this study direct planning outperforms the formalizer variants overall before and after constraints, although formalizers can be competitive with stronger models or syntax revision.
- PDDL generally outperforms SMT; PDDL3 performs worse despite native constraint syntax because low-resource syntax/compilation errors rise. The best representation depends on constraint category and domain.
- On 50-block BlocksWorld and lexical-obfuscated Mystery BlocksWorld, formalizers are more robust than direct planners without constraints, but that robustness sharply erodes once constraints are added.

## Measurement and budget boundaries

- Formalizers receive up to three attempts to repair syntax errors while planners receive one planning attempt; the authors call syntax checking nearly free, but calls/tokens/dollars/wall time are not matched.
- Generate-then-edit and revision change both call count and computation; improvement cannot be attributed to a formal language alone.
- DeepSeek endpoint changes may have altered model identity for PDDL3 experiments; the paper discloses this uncertainty.
- The main evaluation uses one representative problem per constraint rather than all 10,000 possible pairs. Domains remain simplified and may appear in pretraining.
- Plan correctness may be a false positive for specification faithfulness: a correct plan can arise from incorrect generated code. A 20-sample audit found none, but cannot establish zero prevalence.

## Failures and limits

- A short semantically meaningful constraint defeats robustness to complexity and lexical shift that ordinary formalizers otherwise exhibit.
- Constraint introduction increases both syntax and semantic failures; after syntax revision, missing/incorrect constraint predicates or logic dominate.
- A more expressive formalism is not automatically a better agent interface: low-resource syntax and compilation burden can outweigh native expressivity.
- The four categories do not cover conjunction, negation or ambiguity; the two domains are proof-of-concept and not real-world evidence.

## Draft knowledge role

### Failure draft: `Formalizer Robustness Collapses Under Constraint Shift`

- Failure: an LLM may successfully formalize the base domain yet fail after a short constraint changes permitted states or action traces.
- Evidence strength: broad model/method comparison on two synthetic domains, plus complexity and lexical perturbation slices.
- Alternative explanations: extra unfamiliar syntax, unmatched revision budget, benchmark/domain design and pretraining exposure.
- Not refuted: formalizers retain interpretability and can be stronger than direct planners in several unconstrained or model-specific settings.

P055 should also update the existing formalized-planning Operator's strong-baseline requirements: compare direct planning, complete PDDL formalization, generate-then-edit and matched-budget syntax revision; report failures by constraint category and formalization semantics.

## Draft Evidence locators

- `ev-p055-constraint-taxonomy-draft`: pp.3–5, formal categories and CoPE construction.
- `ev-p055-constraint-degradation-draft`: pp.6–9, Figures 2/6 and reported performance collapse.
- `ev-p055-formal-language-tradeoff-draft`: pp.6–8, PDDL/PDDL3/SMT/LTL differences and error types.
- `ev-p055-budget-boundary-draft`: p.5, formalizer syntax-revision attempts versus one planning opportunity.
- `ev-p055-faithfulness-boundary-draft`: p.10, correct-plan false-positive concern.

All remain drafts until independent reads and reconciliation finish.
