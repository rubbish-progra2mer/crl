<!-- CRL_CARD_META {"schema_version":1,"card_id":"paper-p080","card_kind":"paper","paper_id":"P080","evidence_ids":["ev-p080-gold-supervised-minimal-depth","ev-p080-fixed-depth-under-over-search","ev-p080-shallow-depth-boundary"],"source_refs":[{"path":"papers/P080_autosearch.pdf","sha256":"ab078ee4e0221166d92ea3856d028f92a9348899f8fa9d63ec8841764edd8a86"}]} -->
# AutoSearch: Towards Adaptive Search Depth via Self-Answer Supervision

## Role in the knowledge base
[CODEX_SYNTHESIS] 自适应 test-time retrieval depth 的近期机制锚点，尤其用于阻止把固定步数或“少搜即好”当成充分策略。

## Problem and setting
[CODEX_SYNTHESIS] 固定 retrieval steps 无法同时适配问题复杂度与模型能力。

## Changed computation
[AUTHOR_FACT] 训练用每一步 intermediate answer 与 gold exact match 找到最早正确深度，并据此奖励有效搜索、惩罚过搜。[[evidence:ev-p080-gold-supervised-minimal-depth]]

## Evidence-backed findings
[AUTHOR_FACT] 单跳与多跳任务、不同模型的最佳深度不同；超过近优深度会提高 over-search ratio 并可能降低表现。[[evidence:ev-p080-fixed-depth-under-over-search]]

## Limitations and failure signals
[AUTHOR_FACT] 研究仅覆盖较低 maximum search steps。[[evidence:ev-p080-shallow-depth-boundary]] [CODEX_SYNTHESIS] 这是 gold-supervised hindsight training，不是无 oracle 的线上停止证明。

## Lineage and baselines
[CODEX_SYNTHESIS] 属于 adaptive test-time compute / Agentic RAG；fixed-depth、answer-only reward 与同成本 adaptive stopping 是关键比较面。

## Evidence ledger
[CODEX_SYNTHESIS] gold depth label、fixed-depth failure 与 shallow-depth 限制分别有 Evidence。

## Retrieval vocabulary
[CODEX_SYNTHESIS] adaptive search depth; minimal sufficient retrieval; over-searching; under-searching; gold-supervised hindsight depth; agentic RAG efficiency
