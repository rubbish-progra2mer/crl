# P054 first read — limits of complete PDDL formalization

Status: `DRAFT_BEFORE_INDEPENDENT_READS`  
Reader: main Codex  
Read date: 2026-07-20 (Asia/Shanghai)

## Canonical source and bytes

- Title: On the Limit of Language Models as Planning Formalizers
- Authors: Cassie Huang, Li Zhang
- Venue: ACL 2025, Volume 1: Long Papers, pages 4880–4904
- Canonical ID: ACL Anthology `2025.acl-long.242`; arXiv:2412.09879
- PDF: `knowledge_base/staging/papers/P054_planning_formalizer_limits.pdf`
- PDF SHA-256: `f1e766c715ddaef8b671a9176c75c65759ddf09316dffd8ea32eab4a2c05a5a1`
- Parse check: 25 pages, 79438 extracted characters, zero empty pages

## Scope and lineage

P054 is the direct complete-PDDL formalizer ancestor used by P053. Unlike partial formalizers that receive a domain or most of a problem file, it asks an LLM to recover both the PDDL domain file and problem file from natural-language descriptions, after receiving only the available action identifiers and parameters needed to ground evaluation. It belongs in the P004/P051/P052 planning cluster as a distinct PDDL lineage and strong baseline, not as proof of open-domain planning.

## Changed computation

The direct-planner baseline maps domain/problem descriptions to an action sequence. The formalizer maps the same descriptions to a complete PDDL domain and problem representation, invokes a deterministic planner on the generated model, and then validates the resulting plan against the withheld ground-truth PDDL. The computation changes from language-space plan generation to explicit world-model recovery plus symbolic search.

## Experimental evidence

- Four fully observed synthetic domains are used: BlocksWorld, Mystery BlocksWorld, Logistics and Barman, with 100 problems per dataset and up to three description-naturalness levels.
- GPT-family models and DeepSeek-R1 can produce non-trivial complete PDDL; many Gemma/Llama settings fail largely through syntax errors. Barman is omitted from the main figure because all models are near zero.
- On heavily templated BlocksWorld, GPT-4o formalization yields 60 correct plans from 64 solvable generated models versus 33/100 for direct planning. Similar superiority appears in several model/domain combinations, but o3-mini and DeepSeek-R1 provide counterexamples where direct planning is competitive or preferred.
- More natural descriptions consistently reduce performance. The paper attributes part of the failure to omitted implicit predicates such as `clear`, and its manual error study separates syntax errors from semantic domain/problem errors.
- Mystery BlocksWorld lexical obfuscation hurts direct planning much more than capable formalizers, but results vary substantially by model.

## Measurement and baseline boundaries

- Predicted PDDL is not required to textually match ground truth: the generated model is solved, and the resulting plan is validated against ground-truth dynamics with VAL. This is stronger than syntax-only evaluation and permits equivalent formalizations.
- Only zero-shot direct planning is the main baseline. The authors explicitly acknowledge that planner-plus-symbolic-validation methods would be stronger; no matched LLM-Modulo or P051/P052-style decomposition is run.
- Model capacities and reasoning budgets differ; open models use four RTX A6000 GPUs and the paper reports average input/output tokens only for one formalizer setting, not matched cost, calls or wall time across methods.
- Natural descriptions are model-generated from seeds and manually verified, still within four toy domains. The action space identifiers/parameters are supplied.

## Failures and limits

- Solvable generated PDDL can remain semantically wrong relative to the intended environment; solver success is not specification fidelity.
- Natural language omits predicates humans infer, which creates unsolvable or incorrect formal models even when syntax is valid.
- Formalization is not uniformly better: the preferred computation depends on model, domain complexity and whether the model can reliably emit the low-resource formal language.
- Toy fully observed domains, weak direct-planning baseline and lack of matched cost prevent broad real-world or compute-efficiency claims.

## Draft knowledge role

- Paper/lineage: complete-PDDL formalizer direct ancestor for P053.
- Existing Operator support: natural-language specification → explicit formal world model → programmatic search.
- Existing Failure support: solver guarantee ends at the generated specification; naturalness and implicit facts create semantic translation errors.
- Strong-baseline warning: future Candidates must compare against complete formalization, not only direct planning, and should include natural-description stress tests.

## Draft Evidence locators

- `ev-p054-complete-formalizer-draft`: pp.3–5, full DF/PF generation, solver and VAL evaluation.
- `ev-p054-formalizer-result-draft`: pp.6–7, formalizer/planner results and naturalness degradation.
- `ev-p054-semantic-failure-draft`: pp.7–8, implicit `clear` omission and syntax/semantic error taxonomy.
- `ev-p054-strong-baseline-boundary-draft`: p.10, explicit acknowledgement that validated planner methods are stronger baselines.

All remain drafts until independent reads and reconciliation finish.
