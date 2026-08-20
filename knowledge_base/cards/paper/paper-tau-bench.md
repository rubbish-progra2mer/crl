<!-- CRL_CARD_META {"schema_version":1,"card_id":"paper-tau-bench","card_kind":"paper","paper_id":"P007","evidence_ids":["ev-p007-terminal-state-evaluation","ev-p007-repeat-reliability-collapse"],"source_refs":[{"path":"papers/P007_tau_bench.pdf","sha256":"e2d45d573e1fce753ead1a44cc468ad386dd384e2668450d0a9c0e2c7920ada0"}]} -->
# tau-bench

## Role in the knowledge base
[CODEX_SYNTHESIS] Tool-agent-user evaluation 来源，提供终态可验证性与重复可靠性负向证据。

## Problem and setting
[CODEX_SYNTHESIS] Customer-service 多轮工具交互，Agent 需遵守 policy、与用户沟通并修改 benchmark 中的任务数据库状态。

## Changed computation
[AUTHOR_FACT] 评测比较 episode 末数据库状态与 ground-truth expected state。[[evidence:ev-p007-terminal-state-evaluation]]

## Evidence-backed findings
[AUTHOR_FACT] 所测强 Agent 单次成功仍低，retail 的 pass^8 低于 25%。[[evidence:ev-p007-repeat-reliability-collapse]]

## Limitations and failure signals
[CODEX_SYNTHESIS] 用户模拟与可枚举数据库终态是 benchmark 条件；结果不直接覆盖开放 Web/API 世界。

## Lineage and baselines
[CODEX_SYNTHESIS] Function calling 与 ReAct 是主要 agent baselines；pass^k 补充 pass^1 而不自动改 policy。

## Evidence ledger
[AUTHOR_FACT] p.2 支持终态核验；p.1 支持 pass^k 负向结果。[[evidence:ev-p007-terminal-state-evaluation]] [[evidence:ev-p007-repeat-reliability-collapse]]

## Retrieval vocabulary
[CODEX_SYNTHESIS] tau-bench；tool-agent-user；terminal database state；pass^k；policy compliance；工具交互评测。
