<!-- CRL_CARD_META {"schema_version":1,"card_id":"paper-p072","card_kind":"paper","paper_id":"P072","evidence_ids":["ev-p072-structured-clarification-gate","ev-p072-unstructured-clarification-failure","ev-p072-compute-boundary"],"source_refs":[{"path":"papers/P072_structured_clarification.pdf","sha256":"def959b625902e0381ddbac6f25e042c8670f07435248e50a075fe8ef3945598"}]} -->
# Structured Uncertainty guided Clarification for LLM Agents

## Role in the knowledge base
[CODEX_SYNTHESIS] 提供一个把“是否追问”从自由文本习惯改写为 schema 参数不完整性、问题价值与重复成本共同决定的 Operator；同时保留计算成本和自由追问失败。

## Problem and setting
[AUTHOR_FACT] 无结构澄清方法缺少选择问题与停止追问的机制标准。[[evidence:ev-p072-unstructured-clarification-failure]]

## Changed computation
[AUTHOR_FACT] Agent 先枚举可能含未知参数的 tool calls，再量化结构化不确定性、生成候选问题、以 cost-penalized EVPI 选择问题，并在信息足够时执行。[[evidence:ev-p072-structured-clarification-gate]]

## Evidence-backed findings
[AUTHOR_FACT] 在来源所报 ClarifyBench 配置中，系统减少用户问题但仍约使用 22K tokens；用户交互成本与模型计算成本不能混为一谈。[[evidence:ev-p072-compute-boundary]]

## Limitations and failure signals
[CODEX_SYNTHESIS] 本 Card 只支持 schema-completeness clarification gate，不把启发式 EVPI 扩写成已校准的 Bayesian uncertainty，也不纳入执行错误恢复。

## Lineage and baselines
[CODEX_SYNTHESIS] 最近基线是自由文本 clarification、domain-aware prompting 与枚举式 active disambiguation；真正差异是决策标准，不是多写一条“先提问”提示词。

## Evidence ledger
[CODEX_SYNTHESIS] 三条 Evidence 分别约束问题、changed computation 与计算预算。

## Retrieval vocabulary
[CODEX_SYNTHESIS] structured clarification; schema uncertainty; ask execute gate; question value; clarification cost; tool parameter ambiguity
