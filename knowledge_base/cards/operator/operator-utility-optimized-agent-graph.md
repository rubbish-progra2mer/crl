<!-- CRL_CARD_META {"schema_version":1,"card_id":"operator-utility-optimized-agent-graph","card_kind":"operator","paper_id":"P056","evidence_ids":["ev-p056-graph-optimization","ev-p056-same-set-crosswords"],"source_refs":[{"path":"papers/P056_gptswarm.pdf","sha256":"63aab69835f124fd1bee714a21433a696c4d8d36da9f7883e0b5b01b836fd6ed"}]} -->
# Utility-Optimized Agent Information-Flow Graph

## Intervention target
[CODEX_SYNTHESIS] 多 Agent 节点之间的信息传递边与节点 prompt。

## Before and after computation
[CODEX_SYNTHESIS] fixed hand-written topology → task-utility-driven node and edge optimization。[[evidence:ev-p056-graph-optimization]]

## Inputs outputs information and timing
[CODEX_SYNTHESIS] 输入为任务、候选图与执行分数；输出为节点 prompt/connectivity 参数，发生在部署前搜索。

## Mechanism hypothesis
[CODEX_HYPOTHESIS] 删除无效消息边、保留互补路径可降低多 Agent 冗余。

## Predicted observable signature
[CODEX_HYPOTHESIS] matched calls 下 topology 消融仍改变质量；仅增加候选数的收益不算机制信号。

## Preconditions and transfer risks
[AUTHOR_FACT] 一个 Crossword 设置在同一 20 题上优化与评价。[[evidence:ev-p056-same-set-crosswords]]

## Source lineage
[CODEX_SYNTHESIS] P056 原始机制；P057/P058 把搜索空间扩到可执行 Agent 代码/workflow。

## Evidence ledger
[CODEX_SYNTHESIS] graph optimization 和 same-set boundary 有直接 Evidence。

## Retrieval vocabulary
[CODEX_SYNTHESIS] optimizable multi-agent graph; information flow topology; stochastic edge; topology search
