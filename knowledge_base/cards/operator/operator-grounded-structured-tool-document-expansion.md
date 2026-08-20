<!-- CRL_CARD_META {"schema_version":1,"card_id":"operator-grounded-structured-tool-document-expansion","card_kind":"operator","paper_id":"P087","evidence_ids":["ev-p087-structured-query-independent-expansion","ev-p087-merge-and-semantic-judge","ev-p087-fields-not-universally-beneficial"],"source_refs":[{"path":"papers/P087_tool_document_expansion.pdf","sha256":"0e6dc98171a7ada43eb7b2a415099853afb090f29c25887d512660501d343eff"}]} -->
# Grounded Structured Tool-Document Expansion

## Intervention target
[CODEX_SYNTHESIS] retrieval 前的 tool representation：原始文档缺少标准化 function intent、use conditions、limitations 或 discriminative tags。

## Before and after computation
[CODEX_SYNTHESIS] 直接编码异构 raw documentation → 离线生成受源文档约束的 structured profile，与原文合并后用于 retriever/reranker。[[evidence:ev-p087-structured-query-independent-expansion]] [[evidence:ev-p087-merge-and-semantic-judge]]

## Inputs outputs information and timing
[CODEX_SYNTHESIS] 离线输入是单个 tool document，输出是保留原文的 expanded document；生成与 judgement 均发生在 query 到来前，在线 ranking 仍消费文本表示。

## Mechanism hypothesis
[CODEX_HYPOTHESIS] 显化 function、when-to-use、limitations 与 tags 可减少跨 registry 的字段/叙述异构，为相近工具提供更稳定的检索锚点。

## Predicted observable signature
[CODEX_HYPOTHESIS] 改善应集中在原文缺少用途/限制的 tools；matched raw-vs-expanded view 下 positive/negative separation 或 ranking 应改变，而不是只因文档更长。

## Preconditions and transfer risks
[AUTHOR_FACT] full expansion 不总是最优，example usage 可为负并被移除。[[evidence:ev-p087-fields-not-universally-beneficial]]
[CODEX_SYNTHESIS] generated profile 不能恢复原文没有的事实；semantic judge 不是 oracle。该 Operator 仍是 text enrichment，不等于 typed schema computation、argument binding 或 execution validation；原论文训练规模也不是本机轻量 comparator。

## Source lineage
[CODEX_SYNTHESIS] 从 P087 arXiv v1/TOOL-DE 抽象；对任何 prompt-based tool-profile expansion 是直接 prior，对 field-aware typed computation 是最近 document-side comparator。

## Evidence ledger
[CODEX_SYNTHESIS] query-independent generation、merge/judgement 与 harmful-field ablation 均绑定 exact Passage；不复用论文内部冲突数值。

## Retrieval vocabulary
[CODEX_SYNTHESIS] tool document expansion; grounded profile; function description; when to use; limitations; tags; query-independent representation; under-documented APIs; TOOL-DE; TOOL-REX; description-aware retrieval
