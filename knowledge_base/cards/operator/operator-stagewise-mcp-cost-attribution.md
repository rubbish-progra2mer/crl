<!-- CRL_CARD_META {"schema_version":1,"card_id":"operator-stagewise-mcp-cost-attribution","card_kind":"operator","paper_id":"P070","evidence_ids":["ev-p070-six-stage-attribution","ev-p070-light-tool-runtime-boundary","ev-p070-orchestration-bottleneck"],"source_refs":[{"path":"papers/P070_promcp.pdf","sha256":"d67090fae5dd6eef7edb633ad9e3b7f4b3873b48fea8276aecb5d5877377f777"}]} -->
# Stagewise MCP Token-and-Latency Attribution

## Intervention target
[CODEX_SYNTHESIS] MCP Agent 执行的 measurement boundary；不自动改变 Agent 决策。

## Before and after computation
[CODEX_SYNTHESIS] one aggregate latency/token total → stage-separated prompting, planning, tool, context, synthesis attribution。[[evidence:ev-p070-six-stage-attribution]]

## Inputs outputs information and timing
[CODEX_SYNTHESIS] 输入为一次 Agent trace 与 timestamps/token counts；输出为阶段成本；运行后分析，不引入科研评分器。

## Mechanism hypothesis
[CODEX_HYPOTHESIS] 分阶段测量能阻止优化错误瓶颈或把更多 token 偷换成质量机制。

## Predicted observable signature
[CODEX_HYPOTHESIS] Candidate 声称节省某阶段时，该阶段的绝对成本下降且其他阶段未隐性膨胀。

## Preconditions and transfer risks
[AUTHOR_FACT] 被测轻量/中等工具的 runtime 很小，不能外推到重工具。[[evidence:ev-p070-light-tool-runtime-boundary]]

## Source lineage
[CODEX_SYNTHESIS] aggregate efficiency reports → P070 stagewise profiling；这是实验归因工具，不是自动优化模块。

## Evidence ledger
[AUTHOR_FACT] 已测部署的主要瓶颈落在 orchestration/synthesis。[[evidence:ev-p070-orchestration-bottleneck]]

## Retrieval vocabulary
[CODEX_SYNTHESIS] MCP token flow; stagewise latency; orchestration cost; tool runtime attribution; matched cost
