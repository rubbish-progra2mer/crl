<!-- CRL_CARD_META {"schema_version":1,"card_id":"operator-terminal-state-reliability-evaluation","card_kind":"operator","paper_id":"P007","evidence_ids":["ev-p007-terminal-state-evaluation"],"source_refs":[{"path":"papers/P007_tau_bench.pdf","sha256":"e2d45d573e1fce753ead1a44cc468ad386dd384e2668450d0a9c0e2c7920ada0"}]} -->
# Terminal-State Reliability Evaluation

## Intervention target
[AUTHOR_FACT] 在 episode 结束后比较数据库状态与 ground-truth expected state。[[evidence:ev-p007-terminal-state-evaluation]]

## Before and after computation
[CODEX_SYNTHESIS] Changed computation 是执行完整交互后核验标注环境终态；当前 Evidence 不建立“文本匹配或单点 judge”这一直接 baseline。

## Inputs outputs information and timing
[CODEX_SYNTHESIS] 输入为执行后的数据库与标注目标，输出为 task success；核验发生在对话完成后，不把目标状态暴露给 Agent。相较静态输出评测，需要运行完整多轮交互并读取终态；当前 Evidence 未量化额外 token、tool-call 或 latency 成本。

## Mechanism hypothesis
[CODEX_SYNTHESIS] 终态比较能容纳多条等价对话路径，同时捕获“说对但没做对”的工具执行错误。

## Predicted observable signature
[CODEX_HYPOTHESIS] 文本 judge 与终态核验分歧时，后者应更接近真实 side effect 是否完成。

## Preconditions and transfer risks
[CODEX_SYNTHESIS] 需要确定、完整且非泄漏的目标状态；无法枚举副作用的开放 Web 任务不能直接迁移。

## Source lineage
[CODEX_SYNTHESIS] tau-bench 是直接评测来源；它是 evaluation Operator，不是 Agent policy 改进。

## Evidence ledger
[AUTHOR_FACT] `ev-p007-terminal-state-evaluation` 定位到 PDF p.2 的终态核验定义。[[evidence:ev-p007-terminal-state-evaluation]]

## Retrieval vocabulary
[CODEX_SYNTHESIS] terminal state verification；database-state evaluation；tool-agent-user；non-oracle execution check；终态校验。
