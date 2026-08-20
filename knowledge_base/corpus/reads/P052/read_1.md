# P052 first read — general-purpose formalized programming for planning

Status: `DRAFT_BEFORE_INDEPENDENT_READS`  
Reader: main Codex  
Read date: 2026-07-19 (Asia/Shanghai)

## Canonical source and bytes

- Title: Planning Anything with Rigor: General-Purpose Zero-Shot Planning with LLM-based Formalized Programming
- Authors: Yilun Hao, Yang Zhang, Chuchu Fan
- Venue: ICLR 2025 Conference Paper
- Canonical ID: OpenReview `0K1OaL6XuK`; arXiv:2410.12112 v3
- PDF: `knowledge_base/staging/papers/P052_llmfp.pdf`
- PDF SHA-256: `e59c5c55b3befeeb4774a20990b8629f487e9fb1520cc2a953f041b7bb6fdaec`
- Parse check: 57 pages, 169546 extracted characters, zero empty pages

## Scope and lineage

P052 is the direct generalization successor of P051. P051 uses task-specific demonstrations to translate TravelPlanner queries into an executable constraint model; P052 attempts to retain the formal solver boundary while removing task-specific examples across nine multi-constraint and multi-step tasks. The in-scope mechanism is therefore not a new generic “agent pipeline”, but the transfer from task-specific formal encoding to a fixed, task-agnostic decomposition of definition, formulation, code generation, solving, formatting, and self-assessment.

## Changed computation

LLMFP receives a natural-language task description, background information or APIs, and a query, then executes five substantive stages (pp.4–7):

1. `Definer` identifies the optimization goal, decision variables, explicit constraints, and implied constraints;
2. `Formulator` converts each variable and constraint into structured representation/formulation pairs; its prompt contains two fixed task-agnostic examples, but no task-specific examples;
3. `Code Generator` translates the formulation to executable solver code and retries runtime errors up to five times;
4. the optimization/SMT solver searches the encoded model and `Result Formatter` renders the solution;
5. `Self Assess & Modification` asks the same LLM to locate the first incorrect stage and regenerate downstream artifacts, for at most five iterations.

Relative to a direct Code-SMT baseline, the material change is the explicit intermediate variable/constraint decomposition and staged localization of encoding errors. The solver still guarantees only the correctness of the encoded optimization problem, not fidelity between the natural-language request and that encoding.

## Experimental evidence

- Across nine tasks, GPT-4o LLMFP averages 83.7% optimal rate and Claude 3.5 Sonnet averages 86.8% (Tables 1–2, pp.8–9). Inputs and formatters are matched across zero-shot baselines, and Code-SMT uses the same Z3 tool.
- The strongest reported baseline is task dependent: Code/Code-SMT is stronger on multi-constraint tasks, while direct o1-preview or CoT is stronger on multi-step tasks. LLMFP exceeds these per-group baselines, not just the weakest direct generator.
- Removing `Definer`, `Formulator`, or `Self Assess & Modification` reduces aggregate performance, but the ablation does not cost-match the removed calls and the effects are highly task dependent (Table 3, pp.9–10).
- Replacing the two task-agnostic Formulator examples with one task-specific Coffee example raises Coffee performance from 61.2% to 85.4% (Table 4, p.10). This supports the zero-shot trade-off boundary rather than claiming task-specific examples are unnecessary for peak performance.

## Cost and implementation burden

LLMFP is substantially more expensive than ordinary GPT-4o baselines. On Coffee it costs $0.139/query versus $0.008 direct, $0.013 CoT, and $0.024 Code-SMT; the paper reports roughly $0.1/query across the nine tasks (Tables 11–13, p.21). Average wall time is 52.7 seconds on multi-constraint tasks and 73.0 seconds on multi-step tasks, versus 15.8 and 10.3 seconds for Code-SMT (Tables 8–10, p.20). The self-assessment and runtime-retry limits permit multiple extra calls, so future transfer must compare under both equal-model and explicit compute/call budgets.

## Failures and limits

- Ambiguous queries can be formalized with the opposite intended intervention; task-specific examples improve precisely this class (pp.10, 24).
- `Definer` omits implicit flow constraints, allowing formally optimal but physically invalid solutions (p.24).
- Code generation can overwrite trusted APIs, omit false initial states, or create incorrect values (pp.24–25).
- The same-model self-assessor can misdiagnose code errors as insufficient planning horizon and generate a non-terminating loop (p.25).
- Solver optimization may exceed the 15-minute limit on large solution spaces, and the authors require clear, detailed task descriptions (pp.10–11, 24).

These observations make formalization fidelity, trusted-interface preservation, and diagnosis quality the residual failure surface. They also prevent treating solver success as end-to-end semantic verification.

## Draft Operator and Failure candidates

### Operator draft: `Task-Agnostic Decomposed Formalized Planning`

- Baseline: direct plan generation or one-shot natural-language-to-SMT code.
- Changed computation: separate problem definition, representation/formulation, solver code, and bounded diagnosis so errors can be localized before formal search.
- Predicted signature: gains should be largest when tasks share an optimization structure but differ in surface schema; errors should shift from combinatorial search toward omitted/mistranslated constraints and generated-interface corruption.
- Transfer boundary: the domain must expose a sufficiently complete textual specification or trusted API, admit formal optimization, and tolerate added calls/solver latency.

### Failure draft: `Formal Solver Success Does Not Establish Specification Fidelity`

- Failure: missing implicit constraints or an inverted ambiguous query can yield an optimal solver result for the wrong problem.
- Evidence strength: directly illustrated by Coffee and Facility failures and acknowledged task-description limitations.
- Not refuted: formal search reliably improves encoded feasibility and optimality; the failure narrows the guarantee to the formalized model.

### Failure draft: `Self-Diagnosis Can Amplify an Encoding Error`

- Failure: a same-model diagnostic loop may attribute a code-generation fault to an insufficient horizon and introduce non-termination.
- Evidence strength: explicit Gripper failure case; frequency is not separately reported.
- Not refuted: aggregate removal ablation supports a net positive effect for self-assessment, so this is a bounded failure mode rather than a rejection of refinement.

## Draft Evidence locators

- `ev-p052-decomposed-formalization-draft`: pp.4–7, framework stages and fixed task-agnostic examples.
- `ev-p052-formalization-fidelity-draft`: pp.24–25, implicit-constraint, API overwrite, initialization, and self-diagnosis failures.
- `ev-p052-budget-draft`: pp.20–21, stagewise wall time and cost.

All remain drafts until independent second/third reads and source reconciliation finish.
