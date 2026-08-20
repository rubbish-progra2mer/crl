<!-- CRL_CARD_META {"schema_version":1,"card_id":"paper-p087","card_kind":"paper","paper_id":"P087","evidence_ids":["ev-p087-structured-query-independent-expansion","ev-p087-merge-and-semantic-judge","ev-p087-fields-not-universally-beneficial"],"source_refs":[{"path":"papers/P087_tool_document_expansion.pdf","sha256":"0e6dc98171a7ada43eb7b2a415099853afb090f29c25887d512660501d343eff"}]} -->
# Tools Are Under-Documented: Simple Document Expansion Boosts Tool Retrieval

## Role in the knowledge base
[CODEX_SYNTHESIS] description-aware tool-document expansion 的直接先行。当前 Evidence 来自 arXiv:2510.22670 v1（TOOL-DE）；ICLR 2026/TOOL-REX 只作为版本 provenance，不冒充已读终稿。

## Problem and setting
[CODEX_SYNTHESIS] 研究把异构、缺少使用语境的 tool documentation 视为 retrieval representation bottleneck，并在 ToolRet 派生设置中构建扩展文档与专用 retriever/reranker。

## Changed computation
[AUTHOR_FACT] 离线、query-independent 生成 function description、tags、when-to-use、limitations 等 structured profile，optional fields 仅在原文支持时生成。[[evidence:ev-p087-structured-query-independent-expansion]]
[AUTHOR_FACT] profile 与原文合并，随后经过格式检查和 LLM semantic judgment。[[evidence:ev-p087-merge-and-semantic-judge]]

## Evidence-backed findings
[AUTHOR_FACT] field ablation 表明 full expansion 并非始终最优，example usage 增益最小且可能有害，因此从最终 retrieval profile 移除。[[evidence:ev-p087-fields-not-universally-beneficial]]

## Limitations and failure signals
[CODEX_SYNTHESIS] 生成/裁判链不能恢复原文真正缺失的事实，也不能保证零 hallucination；部分现成 retriever 的 Recall/Completeness 下降。训练与评测 document view 未形成完整交叉格，且没有 live registry 或端到端执行实验。

## Lineage and baselines
[CODEX_SYNTHESIS] 对字段扩写、标准化描述、pseudo-use-context 或 retrieval document enrichment 是直接 comparator；对 typed parameter/output alignment 只是相邻先行，不是 exact computation。

## Evidence ledger
[CODEX_SYNTHESIS] 扩展字段、merge/judge pipeline 与 non-universal field effect 分别绑定 exact Passage；内部数据集计数/审计比例冲突未进入强 claim。

## Retrieval vocabulary
[CODEX_SYNTHESIS] TOOL-DE; TOOL-REX; under-documented tools; structured document expansion; function description; when to use; limitations; tags; query-independent enrichment; description-aware retrieval; harmful example usage
