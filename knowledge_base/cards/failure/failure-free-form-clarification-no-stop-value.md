<!-- CRL_CARD_META {"schema_version":1,"card_id":"failure-free-form-clarification-no-stop-value","card_kind":"failure","paper_id":"P072","evidence_ids":["ev-p072-structured-clarification-gate","ev-p072-unstructured-clarification-failure","ev-p072-compute-boundary"],"source_refs":[{"path":"papers/P072_structured_clarification.pdf","sha256":"def959b625902e0381ddbac6f25e042c8670f07435248e50a075fe8ef3945598"}]} -->
# Free-Form Clarification Lacks a Stop and Value Criterion

## Observed failure
[AUTHOR_FACT] 自由文本 clarification 不显式建模参数依赖、重要性与可行性，因而可能过问低影响细节、漏问关键参数或无法识别不可行请求。[[evidence:ev-p072-unstructured-clarification-failure]]

## Conditions and scope
[CODEX_SYNTHESIS] 警告针对有明确 tool schema、歧义落在调用参数上的任务，不说明开放式对话都应结构化。

## Failed intervention
[CODEX_SYNTHESIS] 仅在 prompt 中要求“必要时追问”，但没有问题价值、重复成本或停止边界。

## Evidence and alternative explanations
[AUTHOR_FACT] P072 的替代计算显式做结构化不确定性与 cost-penalized 问题选择。[[evidence:ev-p072-structured-clarification-gate]] [CODEX_SYNTHESIS] 收益仍可能部分来自更多推理计算。

## Warning for future candidates
[CODEX_SYNTHESIS] 新 Candidate 若只是增加 reflection/clarification 文本，而没有改变 ask-versus-execute computation，应视为高碰撞、低信息路线。

## Possible repair boundary
[AUTHOR_FACT] 在来源所报 ClarifyBench 配置中，结构化 gate 仍使用约 22K tokens，故修复必须分别报告用户问题、模型调用和 tokens。[[evidence:ev-p072-compute-boundary]]

## Evidence ledger
[CODEX_SYNTHESIS] Failure、替代机制和预算偷换风险均已绑定 Evidence。

## Retrieval vocabulary
[CODEX_SYNTHESIS] free-form clarification failure; over questioning; missing parameter; no stopping rule; ask execute ambiguity
