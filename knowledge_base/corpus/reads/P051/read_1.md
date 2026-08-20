# P051 first read — formal verification for real-world planning

Status: `DRAFT_BEFORE_SECOND_READ`  
Reader: main Codex  
Read date: 2026-07-19 (Asia/Shanghai)

## Canonical source and bytes

- Title: Large Language Models Can Solve Real-World Planning Rigorously with Formal Verification Tools
- Authors: Yilun Hao, Yongchao Chen, Yang Zhang, Chuchu Fan
- Venue: NAACL 2025, Volume 1: Long Papers, pages 3434–3483
- Canonical ID: arXiv:2404.11891; inspected v3/NAACL-aligned full text
- PDF: `knowledge_base/staging/papers/P051_formal_verification_planning.pdf`
- PDF SHA-256: `ba9261d6d8fbf2b43817e57c29aa6ffacc0b14ef038e6c86a33f8780490bd365`
- Parse check: 50 pages, 166398 extracted characters, zero empty pages

## Scope and admission boundary

The valuable in-scope mechanism is `natural language → formal constraints/code → sound solver → verified plan`. It directly fills the gap between TravelPlanner's structured-constraint failures and generic LLM planning/search. Interactive modification of unsatisfiable user requests is documented as an experiment and cost boundary, but it is not admitted as an “environment feedback learning or execution recovery” research direction.

## Problem and closest baselines

TravelPlanner requires a plan satisfying interacting hard, commonsense, environment, and budget constraints. Direct generation, Greedy Search, TwoStage, and the paper's discussion of LLM-Modulo are the relevant baselines. The closest composition is not merely “LLM + tool”: the LLM translates a natural-language problem into an executable formal model, while an SMT solver performs the combinatorial search and feasibility check.

## Changed computation

For satisfiable queries the framework has four substantive stages (pp.3–5):

1. an LLM parses a user query into constraint-encoding steps;
2. an LLM converts those steps into Python/API/Z3 code using human-authored demonstrations;
3. the code queries the travel database and encodes constraints for the SMT solver;
4. Z3 solves the encoded problem and the output is rendered as a natural-language plan.

The solver's soundness/completeness applies to the encoded constraint program. It does not prove that the LLM translated every user requirement faithfully. This distinction is the central transfer boundary.

## Experimental evidence

- TravelPlanner Table 1 (p.7): on the 1000-query test set, final pass is 93.9 for Claude-3, 90.2 for GPT-4, and 67.8 for Mistral-Large. Direct GPT-4 is 4.4; Greedy Search is 0; TwoStage GPT-4 is 0.6.
- Validation includes Direct o1-preview at 10.0 final pass, while the solver-backed variants reach 93.3 with Claude-3/GPT-4.
- The extra natural-language-to-JSON stage is excluded from the main natural-language comparison and reported separately, which is an important fairness distinction (pp.4, 6–7).
- New-domain experiments use only 25 scenarios per domain and add task descriptions; they support limited transfer, not unrestricted general-purpose planning (p.8).

## Cost and implementation burden

Appendix B (p.16) reports, for 180 validation queries with GPT-4, an average cost of $0.74 per query and 245.66 seconds total: 5.45 s NL→JSON, 35.16 s JSON→steps, 166.66 s step→code, and 38.39 s solver time. Solver timeout is 30 minutes; one validation query exceeded it. The prompt/code demonstrations cover almost all API and SMT operations, so the method includes substantial task-specific formalization effort.

## Ablations, failures, and limits

- Interactive-plan-repair ablations (pp.7–8) mix solver feedback, information collection, user feedback, and iteration count. They are not a clean attribution for the satisfiable-plan operator and are outside the admitted research direction.
- The explicit limitations (p.9) are task-specific prompt/code design, potentially long solver runtime, and unsafe/incorrect database content.
- A more fundamental inferred limit is formalization fidelity: solver guarantees hold only for constraints present in the generated program. The paper reports delivered/final pass, but does not provide a complete independent semantic audit of every natural-language requirement-to-code mapping.
- Reported success changes model, prompt demonstrations, API access, generated code, solver search, and runtime together. Any future Candidate must compare against direct planning and verifier-only/encoding controls under matched model and information.

## Draft Operator and Failure candidates

### Operator draft: `Natural-Language-to-Constraint Solver Plan Synthesis`

- Baseline: LLM directly proposes a plan or searches in language space.
- Changed computation: LLM creates a formal executable model; a sound solver searches and verifies that model before plan delivery.
- Predicted signature: large gains should concentrate on combinatorial constraint validity, while translation omissions remain a residual error class.
- Transfer boundary: requires a formalizable domain, trusted data adapters, reviewed constraint vocabulary, and acceptable solver/runtime cost.

### Failure draft: `Solver Guarantee Stops at the Formalization Boundary`

- Failure: a SAT/optimal solution can still violate a user intent omitted or mistranslated by the LLM-generated encoding.
- Evidence strength: author-stated solver guarantee plus prompt-design limitations support the boundary; the paper does not quantify all omission errors as a separate causal category.
- Not refuted: formal solvers remain valuable for encoded feasibility; this Failure warns against calling the whole natural-language pipeline formally guaranteed.

## Draft Evidence locators

- `ev-p051-formal-plan-pipeline-draft`: pp.3–5, Framework Overview and SMT Solver; exact changed computation and the encoded-problem guarantee.
- `ev-p051-formalization-boundary-draft`: p.9, Prompt Designing and Solver Runtime; task-specific encoding work and runtime limits.
- `ev-p051-cost-draft`: p.16, Appendix B; stagewise latency and GPT-4 cost.

All three remain drafts until independent reads and source reconciliation finish.
