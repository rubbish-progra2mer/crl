<!-- CRL_CARD_META {"schema_version":1,"card_id":"paper-p056","card_kind":"paper","paper_id":"P056","evidence_ids":["ev-p056-graph-optimization","ev-p056-same-set-crosswords","ev-p056-dylan-cost-quality"],"source_refs":[{"path":"papers/P056_gptswarm.pdf","sha256":"63aab69835f124fd1bee714a21433a696c4d8d36da9f7883e0b5b01b836fd6ed"}]} -->
# GPTSwarm: Language Agents as Optimizable Graphs

## Role in the knowledge base
[CODEX_SYNTHESIS] 可优化 multi-agent 信息流图的早期机制来源，也是后续 workflow search 的谱系锚点。

## Problem and setting
[AUTHOR_FACT] 系统分别优化 node prompt 与 graph edge/connectivity。[[evidence:ev-p056-graph-optimization]]

## Changed computation
[CODEX_SYNTHESIS] 把固定手写拓扑变为可按任务效用优化的 stochastic computation graph。

## Evidence-backed findings
[AUTHOR_FACT] DyLAN 对照略高但结构更复杂且成本更高。[[evidence:ev-p056-dylan-cost-quality]]

## Limitations and failure signals
[AUTHOR_FACT] Mini Crosswords 的优化与评估复用了同一 20 题子集。[[evidence:ev-p056-same-set-crosswords]]

## Lineage and baselines
[CODEX_SYNTHESIS] 固定 multi-agent graph → GPTSwarm edge/node optimization → P057/P058 executable workflow search。

## Evidence ledger
[CODEX_SYNTHESIS] 机制、同集混杂、成本—质量对照分别由三条 Evidence 支撑。

## Retrieval vocabulary
[CODEX_SYNTHESIS] optimizable agent graph; stochastic edge; multi-agent topology; workflow search ancestor; same-set evaluation
