# P060 first read — syntax-aligned formalization with solver feedback

Status: `DRAFT_BEFORE_INDEPENDENT_READ`  
Reader: main Codex  
Read date: 2026-07-20 (Asia/Shanghai)

## Canonical source and bytes

- Title: Unifying Inference-Time Planning for Language Generation
- Authors: as printed in the source PDF
- Venue: Findings of ACL 2026
- PDF: `knowledge_base/staging/plan05_sat_a1/P060_unifying_planning_language.pdf`
- PDF SHA-256: `5e3695206fd0e01347e348d606ebd206387f4fba3192ed24ea5133abdef36305`
- Parse check: 44 physical pages

## Changed computation

The paper factorizes language-model planning by the number and type of intermediate representations between a natural-language task and an executable plan. It compares direct planning, one-stage formalization, and two-stage pipelines using PDDL, natural-language IRs, Python simulators and PyPDDL. The strongest pattern pairs syntax-aligned formal representations with external solver feedback and revision rather than asking the model to plan solely in free-form text.

## Evidence and closest lineage

Across four planning domains and eight open-model configurations, the best Level-2 pipeline consistently beats direct planning and Level-1 alternatives. Natural-language IRs consistently hurt, while PDDL/PyPDDL plus feedback and revision often help. The paper directly cites the NeurIPS 2023 world-model planning predecessor and subsumes it in a larger controlled comparison, so that predecessor is retained as bibliographic lineage rather than a separate corpus source.

## Measurement and fairness boundaries

- Inputs include ground-truth action header names and parameters; this is specification-to-code, not open-world environment discovery.
- The four domains contain 100 instances each and are moderately templated.
- Solver feedback is a central intervention: PDDL revision loses much of its advantage without it.
- Best-of-two controls extra responses but differs in sampling temperature, so it is informative rather than a perfect compute match.
- More formalization is not uniformly robust: direct Level-1 methods degrade less as block-world complexity rises, and grammar-constrained decoding can fail completely on some domains.
- A deterministic transpiler can underperform LLM transpilation when generated wrappers misuse the target API; adding a formal stage alone is not the mechanism.

## Draft knowledge objects

### Operator draft: `Syntax-Aligned IR with Solver-Feedback Revision`

Translate a language task into an executable representation aligned with a verifier/solver, expose concrete parser or solver feedback, and revise the representation before plan execution.

### Failure draft: `Intermediate Representation Complexity Without Verifiable Gain`

An additional IR can reduce performance when its syntax is weakly aligned with execution or when no verifier feeds back concrete errors; more stages can also reduce robustness as problem complexity grows.

## Draft Evidence locators

- Framework/method sections: planning levels and representation families.
- Main result tables: best Level-2 versus direct and Level-1 results across model configurations.
- Ablations: solver feedback, PDDL revision, best-of-two and constrained decoding.
- Complexity analysis and appendices: block-count robustness, action-header input and domain construction.

All claims remain draft until independent read and reconciliation.
