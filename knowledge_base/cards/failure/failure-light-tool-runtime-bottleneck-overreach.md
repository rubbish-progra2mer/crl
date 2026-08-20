<!-- CRL_CARD_META {"schema_version":1,"card_id":"failure-light-tool-runtime-bottleneck-overreach","card_kind":"failure","paper_id":"P070","evidence_ids":["ev-p070-six-stage-attribution","ev-p070-light-tool-runtime-boundary","ev-p070-orchestration-bottleneck"],"source_refs":[{"path":"papers/P070_promcp.pdf","sha256":"d67090fae5dd6eef7edb633ad9e3b7f4b3873b48fea8276aecb5d5877377f777"}]} -->
# Lightweight MCP Tool Runtime Does Not Generalize to All Agent Bottlenecks

## Observed failure
[AUTHOR_FACT] P070 被测部署的主要成本来自 planning/schema injection 或 synthesis，而非 tool runtime。[[evidence:ev-p070-orchestration-bottleneck]]

## Conditions and scope
[AUTHOR_FACT] 可忽略 runtime 的结论只覆盖所测轻量至中等工具。[[evidence:ev-p070-light-tool-runtime-boundary]]

## Failed intervention
[CODEX_SYNTHESIS] 从少量轻工具直接宣称“工具执行从来不是瓶颈”，或只优化 runtime 而不看阶段归因。

## Evidence and alternative explanations
[CODEX_SYNTHESIS] 模型、schema、拓扑和工具复杂度可重排瓶颈；重型 I/O 工具可能造成与论文轻量工具设置不同的 regime shift。

## Warning for future candidates
[CODEX_SYNTHESIS] 效率 claim 必须先用同一 trace 做 stagewise attribution。[[evidence:ev-p070-six-stage-attribution]]

## Possible repair boundary
[CODEX_SYNTHESIS] 分阶段测量可以限定 claim，但不自动决定优化方法。

## Evidence ledger
[CODEX_SYNTHESIS] 方法、观测瓶颈和外推边界各有 Evidence。

## Retrieval vocabulary
[CODEX_SYNTHESIS] MCP bottleneck; tool runtime overreach; schema injection latency; stagewise cost attribution
