<!-- CRL_CARD_META {"schema_version":1,"card_id":"operator-state-conditioned-agent-activation","card_kind":"operator","paper_id":"P059","evidence_ids":["ev-p059-state-conditioned-orchestrator","ev-p059-compact-cyclic-topology"],"source_refs":[{"path":"papers/P059_evolving_orchestration.pdf","sha256":"244c86ebd95a9fa7ca06539854186ea3dcdbf794ceb6e7827fff6e642e647bf6"}]} -->
# State-Conditioned Agent Activation

## Intervention target
[CODEX_SYNTHESIS] 每一步由哪一名 Agent 接续计算。

## Before and after computation
[CODEX_SYNTHESIS] static topology → centralized policy selects one next active Agent from evolving state。[[evidence:ev-p059-state-conditioned-orchestrator]]

## Inputs outputs information and timing
[CODEX_SYNTHESIS] 输入为当前 task state；输出为下一名 Agent identity；每个协作 step 前发生，并通过逐步单 Agent activation 改变调用预算。

## Mechanism hypothesis
[CODEX_HYPOTHESIS] 只在有用时激活专长 Agent，可减少固定拓扑中的冗余和错误传播。

## Predicted observable signature
[CODEX_HYPOTHESIS] matched total calls 下仍出现 state-dependent activation sequence，而非恒定选择同一强 Agent。

## Preconditions and transfer risks
[CODEX_SYNTHESIS] 中央 state 表示必须可用；异质模型能力会与 orchestrator 机制混杂。

## Source lineage
[CODEX_SYNTHESIS] P056 topology optimization → P059 online state-conditioned activation。

## Evidence ledger
[CODEX_SYNTHESIS] activation rule 与 compact cyclic structure 各有 Evidence。[[evidence:ev-p059-compact-cyclic-topology]]

## Retrieval vocabulary
[CODEX_SYNTHESIS] dynamic multi-agent orchestration; next-agent selection; agent activation policy; evolving topology
