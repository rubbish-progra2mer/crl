<!-- CRL_CARD_META {"schema_version":1,"card_id":"paper-p070","card_kind":"paper","paper_id":"P070","evidence_ids":["ev-p070-six-stage-attribution","ev-p070-light-tool-runtime-boundary","ev-p070-orchestration-bottleneck"],"source_refs":[{"path":"papers/P070_promcp.pdf","sha256":"d67090fae5dd6eef7edb633ad9e3b7f4b3873b48fea8276aecb5d5877377f777"}]} -->
# ProMCP

## Role in the knowledge base
[CODEX_SYNTHESIS] MCP Agent token/latency 的阶段归因证据，用于校验优化是否攻击真实瓶颈。

## Problem and setting
[AUTHOR_FACT] ProMCP 分解 prompting、planning、tool call/response、context update 与 synthesis 的 token/latency。[[evidence:ev-p070-six-stage-attribution]]

## Changed computation
[CODEX_SYNTHESIS] 主要是 measurement decomposition，不是自动优化 Operator。

## Evidence-backed findings
[AUTHOR_FACT] 被测部署中 planning/schema injection 或 answer synthesis 主导，而非 tool runtime。[[evidence:ev-p070-orchestration-bottleneck]]

## Limitations and failure signals
[AUTHOR_FACT] tool runtime 可忽略只适用于论文评测的轻量至中等工具；重型 I/O 可改变瓶颈结构。[[evidence:ev-p070-light-tool-runtime-boundary]]

## Lineage and baselines
[CODEX_SYNTHESIS] aggregate agent latency → stage-wise MCP profiling。

## Evidence ledger
[CODEX_SYNTHESIS] 分解方法、外推边界与已测瓶颈各有 Evidence。

## Retrieval vocabulary
[CODEX_SYNTHESIS] MCP profiling; token flow; latency attribution; schema injection cost; orchestration bottleneck
