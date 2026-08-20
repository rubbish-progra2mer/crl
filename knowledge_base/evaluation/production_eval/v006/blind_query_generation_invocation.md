# Production retrieval v006: hidden blind-query generation invocation

- Task ID: `prod-v006-blind-query-generator`
- Started at: `2026-07-20T21:31:28+08:00`
- Purpose: create a fresh hidden blind split for the repaired, frozen 87-paper production knowledge snapshot. This is a retrieval-integrity test for CRL machine optimization, not Candidate generation or scientific review.

## Required output

Write exactly one machine-readable file:

`crl_agent_v3/knowledge_base/evaluation/production_eval/v006/blind_queries.json`

Use the v005 schema (`schema_version`, `split`, `query_language`, `generation`, `queries`). Create 18 English natural-language queries: for each of the nine mechanism clusters below, one Failure query and one Operator or Paper query. Do not copy wording from v005. Each entry needs `query_id`, `query`, `target_kind`, `critical`, `mechanism_cluster`, and `intent_note`. Do not include expected Card IDs, answers or labels.

Mechanism clusters:

- `planning_reasoning`
- `test_time_search_verification`
- `tool_use_action_interface`
- `memory_context_long_horizon`
- `reflection_self_improvement`
- `multi_agent_information_flow`
- `agent_learning_credit_assignment`
- `evaluation_reliability_safety`
- `efficiency_cost_deep_research`

Queries must ask for mechanism/failure semantics useful to text/tool LLM Agent research, not paper-title lookup. Mark as critical only a small number whose miss would materially prevent CRL from discovering a changed computation or a decisive negative condition. In the `generation` object, record this invocation path, procedural isolation, and that no Card, corpus read, prior evaluation query/result or Run material was accessed.

## Allowed reads

- `AGENTS.md`
- `crl_agent_v3/AGENTS.md`
- `crl_agent_v3/CRL.md`
- `crl_agent_v3/CRL_ENVIRONMENT.md`
- `crl_agent_v3/knowledge_base/CORPUS_SCOPE.md`
- this invocation file

## Forbidden reads

- all files under `crl_agent_v3/knowledge_base/cards/`
- all files under `crl_agent_v3/knowledge_base/corpus/reads/`
- `manifest.json`, `evidence.json`, PDFs and derived databases/indexes
- all earlier `production_eval` attempts, including v005
- v006 `calibration_queries.json`
- all CRL Runs, candidates, experiments, reviews, history and memory

Do not run retrieval. Do not expose query text in the response to the main agent. After writing the file, respond only with query count, per-kind counts, critical count and SHA-256.
