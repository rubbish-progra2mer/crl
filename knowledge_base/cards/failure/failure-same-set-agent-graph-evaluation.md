<!-- CRL_CARD_META {"schema_version":1,"card_id":"failure-same-set-agent-graph-evaluation","card_kind":"failure","paper_id":"P056","evidence_ids":["ev-p056-graph-optimization","ev-p056-same-set-crosswords"],"source_refs":[{"path":"papers/P056_gptswarm.pdf","sha256":"63aab69835f124fd1bee714a21433a696c4d8d36da9f7883e0b5b01b836fd6ed"}]} -->
# Optimizing and Evaluating an Agent Graph on the Same Small Set

## Observed failure
[AUTHOR_FACT] Mini Crosswords 使用同一 20 题子集做 optimization 与 evaluation。[[evidence:ev-p056-same-set-crosswords]]

## Conditions and scope
[CODEX_SYNTHESIS] 该警告只约束此实验设置，不否定其他任务结果。

## Failed intervention
[CODEX_SYNTHESIS] node/edge search 可适配 evaluation instances，而非仅学习可迁移 topology。[[evidence:ev-p056-graph-optimization]]

## Evidence and alternative explanations
[CODEX_SYNTHESIS] observed score 可能同时包含真实图机制与 instance selection overfit，现有 Evidence 不能分解二者。

## Warning for future candidates
[CODEX_SYNTHESIS] workflow/topology search 必须冻结独立 final holdout，并计入全部尝试次数。

## Possible repair boundary
[CODEX_HYPOTHESIS] 未参与搜索的一次性 holdout 可收窄该混杂。

## Evidence ledger
[CODEX_SYNTHESIS] same-set fact 和被优化对象均有 Evidence。

## Retrieval vocabulary
[CODEX_SYNTHESIS] workflow search overfit; same-set optimization; small evaluation set; topology selection leakage
