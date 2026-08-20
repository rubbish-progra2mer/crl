# P053 first read — higher-order planning formalizers

Status: `DRAFT_BEFORE_INDEPENDENT_READ`  
Reader: main Codex  
Read date: 2026-07-20 (Asia/Shanghai)

## Canonical source and bytes

- Title: Language Models as Higher-Order Planning Formalizers
- Authors: Owen Jiang, Cassie Huang, Ashish Sabharwal, Li Zhang
- Venue: arXiv preprint
- Canonical ID: arXiv:2603.23844 v2, revised 2026-07-04
- PDF: `knowledge_base/staging/papers/P053_higher_order_planning_formalizers.pdf`
- PDF SHA-256: `224970784bd45edc3191b71c2aadd81e01f5869fcd004c4fa10bac4ed1217b19`
- Parse check: 44 pages, 129041 extracted characters, zero empty pages

## Scope and admission boundary

This paper is a direct recent stress test and refinement of the P051/P052 formalized-planning lineage. It asks whether direct grounded formalization still scales when a succinct natural-language rule denotes a much larger formal instance. The in-scope contribution is the representational change `NL → compact generator program → grounded PDDL → programmatic planner`, plus the negative result that ordinary formalizers can fail under a description-to-formalization compression gap. It does not establish open-domain or real-world generality.

## Problem and closest baselines

The paper studies fixed-domain classical planning. The direct baselines are: an LLM that emits a plan; an LLM that emits the grounded PDDL problem file; a sentence-wise divide-and-conquer formalizer for long enumerative descriptions; and the proposed higher-order formalizer that emits Python generating PDDL. A ground-truth PDDL domain file is supplied. The closest-composition comparison is ordinary formalization plus the same downstream planner/parser, not free-form language planning.

## Changed computation

For an “unraveling” problem, a short description can expand to many grounded facts. A conventional formalizer must emit that large grounded representation. The proposed method instead asks the LLM to generate a compact Python program encoding the repeated rule; executing the program produces the PDDL problem file, which is then handled by a programmatic planner or exact parser comparison. The method also uses a second prompt asking the model to review repeating patterns before finalizing its program, so the reported system changes both representation and prompting budget.

## Experimental evidence

- The paper constructs 280 synthetic problems over BlocksWorld, OpenStacks, Transport and ChildSnack, varying one main problem-size parameter while fixing other parameters.
- On ordinary BlocksWorld-XXL, direct planners fall to 20% or less around 30 blocks, while frontier formalizers stay much stronger; a sentence-wise D&C formalizer raises Qwen2.5-Coder-32B to 100% at 100 blocks.
- On unraveling variants, ordinary formalizers fluctuate or degrade in BlocksWorld and Transport, while the higher-order formalizer matches or improves them in nearly all reported settings. Frontier ordinary formalizers remain robust on OpenStacks and ChildSnack, so higher-order generation is not uniformly necessary.
- The Qwen ablation removes the repeating-pattern review prompt. Manual error analysis finds loop/object construction errors, and the review raises accuracy on all three scheduling domains. This supports the full representation-plus-review system, but does not isolate the compact representation alone.

## Measurement and implementation boundaries

- The setting provides the natural-language and ground-truth PDDL domain specifications; only problem-instance formalization is generated.
- When the programmatic planner crashes on large problems, evaluation compares generated objects/initial/goal facts with ground-truth PDDL through custom parsers. For known-solvable domains an exact match is counted as implying a valid plan. This is a formalization-fidelity test, not always a completed planning run.
- Problems are synthetic, regular and deliberately pattern-generated; one main variable is scaled while other difficulty variables are fixed.
- Gemini 3 Flash, DeepSeek-V4-Flash and Qwen2.5-Coder-32B are not a matched capacity family. Open models run on one H100, but no matched token, dollar or wall-time comparison across paradigms is reported.
- Each binary sample is run once. The two-stage pattern-review prompt gives the proposed method extra inference work relative to single-stage Planner/Formalizer prompts.

## Failures and limits

- Ordinary formalization can fail from output-size/context overload even though it avoids combinatorial plan search; one-to-one NL–PDDL benchmarks can therefore overstate scalability.
- Higher-order programs shift errors into recurrent rule and loop construction. A compact program can amplify one mistake across many generated facts.
- The paper's own limitations restrict evidence to four fixed-domain classical planning settings, Python generators and handcrafted pattern-reflection prompts; it does not test partial observability, stochasticity, temporal planning or transfer of learned representations.
- The real-world risk statement is qualitative. The experiments do not measure ambiguous natural language, missing implicit constraints, API/data errors or semantic-equivalence audit in the P051/P052 settings.

## Draft Operator and Failure candidates

### Operator draft: `Higher-Order Generative Formalization`

- Baseline: LLM enumerates the grounded formal representation directly.
- Changed computation: LLM writes a compact generator for recurrent formal structure, then deterministic execution expands it before symbolic planning.
- Predicted signature: benefits grow with the ratio between grounded representation size and compact description/program size; residual failures concentrate in loop/rule induction.
- Transfer boundary: requires repeated structure that can be expressed programmatically, a trusted expansion runtime, known formal schema and validation of generated facts.

### Failure draft: `Grounded Formalization Has an Output-Expansion Limit`

- Failure: moving search to a solver does not remove the need to emit the formal instance; succinct descriptions can still force a conventional formalizer to enumerate too many facts.
- Evidence strength: direct controlled comparison on four synthetic fixed domains; not yet real-world or open-domain evidence.
- Not refuted: ordinary formalizers remain strong on several large enumerative and some unraveling settings, especially frontier models.

## Draft Evidence locators

- `ev-p053-higher-order-computation-draft`: pp.2 and 4, definition `Dn → Rn → In` and compact generator program.
- `ev-p053-formalizer-scaling-failure-draft`: pp.6–8, Figure 5 and discussion comparing Formalizer/H-O Formalizer.
- `ev-p053-pattern-review-boundary-draft`: pp.6 and 8, two-stage pattern review and Qwen ablation.
- `ev-p053-evaluation-boundary-draft`: pp.3 and 11, custom parser/exact ground-truth comparison when planner crashes.

All remain drafts until independent read and reconciliation finish.
