<!-- CRL_CARD_META {"schema_version":1,"card_id":"operator-hypothetical-tool-query-expansion","card_kind":"operator","paper_id":"P089","evidence_ids":["ev-p089-training-gold-count-hypothetical-tools","ev-p089-overview-alignment-rrf","ev-p089-hungarian-alignment","ev-p089-forced-alignment-proxy","ev-p089-retrieval-only-metrics","ev-p089-api-latency-boundary"],"source_refs":[{"path":"papers/P089_tooldreamer.pdf","sha256":"d13b84ab7c2a66069f8d160ab78dfb3e7efd5dabab06c219995c5f92b2093918"}]} -->
# Hypothetical-Tool Query Expansion with Learned Alignment and Rank Fusion

## Intervention target
[CODEX_SYNTHESIS] query 与 real-tool description 的 semantic-space mismatch，尤其 query 隐含多个能力却未直接命名工具时的 retrieval decision。

## Before and after computation
[CODEX_SYNTHESIS] 直接用 query 检索一次 → LLM 生成多个 tool thoughts/names/descriptions，每个表示分别检索，再用 RRF 合并；训练时用 HT–GT alignment 优化 retriever。[[evidence:ev-p089-training-gold-count-hypothetical-tools]] [[evidence:ev-p089-overview-alignment-rrf]] [[evidence:ev-p089-hungarian-alignment]]

## Inputs outputs information and timing
[CODEX_SYNTHESIS] 输入是用户 query；中间表示是 textual hypothetical tools；输出是 fused real-tool ranking。训练 generation 读取 gold count，推理不读取；主实现的 HT generation 可能调用外部模型。

## Mechanism hypothesis
[CODEX_HYPOTHESIS] 把隐式子任务翻译到 tool-description language，再让 retriever 学习 hypothetical-to-real alignment，可提供 query-only embedding 缺少的接口线索。

## Predicted observable signature
[CODEX_HYPOTHESIS] 收益应随隐式、多工具需求上升；matched comparator 必须包含 query-only、untrained hypothetical expansion、trained alignment、RRF-only，并分开报告 generator quality 与 retrieval change。

## Preconditions and transfer risks
[AUTHOR_FACT] square Hungarian alignment 总会给出 match，作者承认其可能不完美。[[evidence:ev-p089-forced-alignment-proxy]]
[AUTHOR_FACT] 论文只评价 ranked-list retrieval metrics。[[evidence:ev-p089-retrieval-only-metrics]]
[AUTHOR_FACT] API/open generator 引入额外成本与秒级延迟。[[evidence:ev-p089-api-latency-boundary]]
[CODEX_SYNTHESIS] textual HT 可 hallucinate，gold-count supervision 造成 train/inference 差异；RRF 确定性不覆盖上游 LLM。付费复现必须先请求用户授权。

## Source lineage
[CODEX_SYNTHESIS] 从 P089 ToolDreamer 抽象；query→hypothetical tools→per-tool retrieval→fusion 是直接 pipeline prior，不能靠 latent intent/tool sketch 改名规避。

## Evidence ledger
[CODEX_SYNTHESIS] generation、alignment、inference fusion、forced-proxy、retrieval endpoint 与 cost/latency 均有独立 Evidence。

## Retrieval vocabulary
[CODEX_SYNTHESIS] hypothetical tools; latent tool query; tool thoughts names descriptions; HT GT alignment; Hungarian assignment; QTND; reciprocal rank fusion; tool-to-tool retrieval; query expansion; gold-count supervision
