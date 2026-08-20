<!-- CRL_CARD_META {"schema_version":1,"card_id":"operator-dynamic-linked-memory-evolution","card_kind":"operator","paper_id":"P063","evidence_ids":["ev-p063-dynamic-link-generation","ev-p063-neighbor-rewrite-action","ev-p063-retrieval-k-varies"],"source_refs":[{"path":"papers/P063_a_mem.pdf","sha256":"fec32b521c4a1f793442bf1aeb26139c583078350d1cd4ab8f4eccc54a0694f0"}]} -->
# Dynamic Linked-Memory Evolution

## Intervention target
[CODEX_SYNTHESIS] 新 memory note 的链接结构与被检索邻居的持久内容。

## Before and after computation
[CODEX_SYNTHESIS] append-only vector memory → retrieve neighbors, generate links, optionally rewrite neighbor context/tags。[[evidence:ev-p063-dynamic-link-generation]] [[evidence:ev-p063-neighbor-rewrite-action]]

## Inputs outputs information and timing
[CODEX_SYNTHESIS] 输入为新 note 与近邻；输出为 links 和持久 rewrite；发生在 memory write 时并增加 LLM 调用。

## Mechanism hypothesis
[CODEX_HYPOTHESIS] write-time consolidation 可使相关经验形成可导航结构，而非只依赖 query-time similarity。

## Predicted observable signature
[CODEX_HYPOTHESIS] 关闭 link/evolution 后，跨 note 的检索或决策应下降；仅扩大 k 不应复制收益。

## Preconditions and transfer risks
[AUTHOR_FACT] retrieval k 可按类别调整。[[evidence:ev-p063-retrieval-k-varies]] [CODEX_SYNTHESIS] rewrite 会损失原始 provenance，且论文实现叙述存在内部不一致。

## Source lineage
[CODEX_SYNTHESIS] static vector memory → linked notes → mutable neighbors；与 reranking-only 不是同一 changed computation。

## Evidence ledger
[CODEX_SYNTHESIS] link generation、rewrite 权限、k boundary 各有 Evidence。

## Retrieval vocabulary
[CODEX_SYNTHESIS] dynamic memory links; write-time consolidation; neighbor rewrite; memory graph evolution; provenance
