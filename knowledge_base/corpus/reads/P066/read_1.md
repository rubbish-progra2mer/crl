# P066 first read — stateful function-calling evaluation

Status: `DRAFT_BEFORE_INDEPENDENT_READ`  
Reader: main Codex  
Read date: 2026-07-20 (Asia/Shanghai)

## Canonical source and bytes

- Title: The Berkeley Function Calling Leaderboard (BFCL): From Tool Use to Agentic Evaluation of Large Language Models
- Authors: Shishir G. Patil et al.
- Venue: ICML 2025
- PDF: `knowledge_base/staging/plan05_sat_a1/P066_bfcl.pdf`
- PDF SHA-256: `5248f4770823b2a73fd52e3b12339d94121ff1b359c45163c5a47168edab7a2f`
- Parse check: 22 physical pages

## Changed evaluation computation

BFCL expands tool evaluation from isolated calls to single/parallel calls, real user-contributed queries, stateful multi-turn API suites and agentic web/memory/SQL tasks. It uses AST or execution checks for simple calls and combines response and final-state checks for multi-turn tasks, avoiding a single unconstrained LLM judge as the outcome oracle.

## Evidence and closest lineage

The benchmark contains 5,551 question-function-answer pairs, 2,251 curated crowd-sourced entries, eight multi-turn API suites and 1,000 multi-turn queries. AST matching strongly correlates with executable checks on the tested subset. The multi-turn error analysis shows environment-state misunderstanding dominates, while the memory category leader reaches only 12% in the reported snapshot despite much stronger simple function-calling performance.

## Measurement and fairness boundaries

- AST substring equivalence is scalable but cannot prove arbitrary real execution behavior.
- Multi-turn tasks rely on custom transparent APIs and human-written trajectories, so valid alternative paths can be missed.
- Agentic web/memory/SQL exact matching narrows evaluation but may under-credit semantically correct variants.
- Leaderboard versions evolve and contamination analysis is diagnostic, not definitive proof of training exposure.
- The paper is retained as a strong experimental carrier and evaluation mechanism, not as evidence that benchmark performance alone identifies a research gap.

## Draft knowledge objects

### Operator draft: `State-and-Response Grounded Multi-Turn Tool Evaluation`

Evaluate not only the emitted call syntax but also abstention, ordered dependencies, resulting environment state and response correctness over a full tool interaction.

### Failure draft: `Single-Turn Tool Accuracy Does Not Imply Stateful Agent Competence`

Models that call one function correctly can still hallucinate state, skip prerequisite key discovery, terminate after one failed lookup or mishandle long multi-turn context.

## Draft Evidence locators

- pp.1–5: dataset taxonomy and evaluation protocols.
- pp.6–9: multi-turn results, error analysis, contamination diagnostic and memory-category failure.

All claims remain draft until independent read and reconciliation.
