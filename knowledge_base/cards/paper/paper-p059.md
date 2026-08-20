<!-- CRL_CARD_META {"schema_version":1,"card_id":"paper-p059","card_kind":"paper","paper_id":"P059","evidence_ids":["ev-p059-state-conditioned-orchestrator","ev-p059-compact-cyclic-topology"],"source_refs":[{"path":"papers/P059_evolving_orchestration.pdf","sha256":"244c86ebd95a9fa7ca06539854186ea3dcdbf794ceb6e7827fff6e642e647bf6"}]} -->
# Multi-Agent Collaboration via Evolving Orchestration

## Role in the knowledge base
[CODEX_SYNTHESIS] 从静态 multi-agent topology 过渡到 state-conditioned agent activation 的直接机制来源。

## Problem and setting
[AUTHOR_FACT] 中央策略依据不断变化的 task state，在每一步选择下一名激活 Agent。[[evidence:ev-p059-state-conditioned-orchestrator]]

## Changed computation
[CODEX_SYNTHESIS] 决策对象从预设通信边变为每步状态条件下的下一名 Agent identity。

## Evidence-backed findings
[AUTHOR_FACT] 学得的 orchestrator 与更紧凑、含环的推理结构相关。[[evidence:ev-p059-compact-cyclic-topology]]

## Limitations and failure signals
[CODEX_SYNTHESIS] 集中式 controller、异质 Agent 能力与 terminal outcome 共同作用，不能把全部收益归因于 topology 形状。

## Lineage and baselines
[CODEX_SYNTHESIS] 固定 topology/GPTSwarm → dynamic state-conditioned orchestration。

## Evidence ledger
[CODEX_SYNTHESIS] 激活策略与观测 topology 各由一条 Evidence 支撑。

## Retrieval vocabulary
[CODEX_SYNTHESIS] evolving orchestration; state-conditioned agent selection; dynamic topology; centralized multi-agent controller
