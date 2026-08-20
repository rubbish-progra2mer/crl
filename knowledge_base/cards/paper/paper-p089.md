<!-- CRL_CARD_META {"schema_version":1,"card_id":"paper-p089","card_kind":"paper","paper_id":"P089","evidence_ids":["ev-p089-training-gold-count-hypothetical-tools","ev-p089-overview-alignment-rrf","ev-p089-hungarian-alignment","ev-p089-forced-alignment-proxy","ev-p089-retrieval-only-metrics","ev-p089-api-latency-boundary"],"source_refs":[{"path":"papers/P089_tooldreamer.pdf","sha256":"d13b84ab7c2a66069f8d160ab78dfb3e7efd5dabab06c219995c5f92b2093918"}]} -->
# ToolDreamer: Instilling LLM Reasoning Into Tool Retrievers

## Role in the knowledge base
[CODEX_SYNTHESIS] query-side hypothetical/latent-tool expansion、HT-to-real alignment 与 multi-list fusion 的直接先行；仅改名为 intent/tool sketch 不构成差异。

## Problem and setting
[CODEX_SYNTHESIS] 用户 query 可能隐含工具需求，却不使用 tool-description language；直接 query–tool similarity 因而可能缺少检索线索。

## Changed computation
[AUTHOR_FACT] 训练期 LLM 生成 tool thought/name/description，并被告知 gold-tool count。[[evidence:ev-p089-training-gold-count-hypothetical-tools]]
[AUTHOR_FACT] 推理期每个 hypothetical tool 独立检索，多个 top-k list 由 RRF 合并。[[evidence:ev-p089-overview-alignment-rrf]]
[AUTHOR_FACT] 训练 pairing 使用 embedding similarity 与 Hungarian matching。[[evidence:ev-p089-hungarian-alignment]]

## Evidence-backed findings
[CODEX_SYNTHESIS] 最强 QTND 把原 query 与 hypothetical-tool metadata 共同作为 retrieval input；论文评价 NDCG/P/R/MRR，而非工具执行或最终任务成功。[[evidence:ev-p089-retrieval-only-metrics]]

## Limitations and failure signals
[AUTHOR_FACT] square alignment 总会给出匹配，作者明确把它称为可能不完美的 proxy。[[evidence:ev-p089-forced-alignment-proxy]]
[AUTHOR_FACT] 主流程使用 API-based generator，并报告相对 basic retrieval 的额外秒级 latency。[[evidence:ev-p089-api-latency-boundary]]
[CODEX_SYNTHESIS] RRF 仅在输入 lists 冻结后确定；上游 HT generation 仍依赖 LLM。CRL 不把 retrieval gain 外推为参数/执行/答案正确。

## Lineage and baselines
[CODEX_SYNTHESIS] 任何 query decomposition→textual hypothetical tools→per-tool retrieval→fusion 的 Candidate 都应视为强 pipeline collision；差异必须落在真正不同表示、非强制集合对齐或 execution-coupled computation。

## Evidence ledger
[CODEX_SYNTHESIS] gold-count generation、inference pipeline、alignment、forced-proxy、retrieval-only endpoint 与 cost/latency 分别绑定 exact Passage。

## Retrieval vocabulary
[CODEX_SYNTHESIS] ToolDreamer; hypothetical tool generation; latent tool descriptions; HT GT alignment; Hungarian matching; QTND; reciprocal rank fusion; query-side expansion; gold tool count; tool-to-tool retriever; API generation latency
