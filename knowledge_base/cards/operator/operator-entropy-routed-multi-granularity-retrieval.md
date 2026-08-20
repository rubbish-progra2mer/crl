<!-- CRL_CARD_META {"schema_version":1,"card_id":"operator-entropy-routed-multi-granularity-retrieval","card_kind":"operator","paper_id":"P090","evidence_ids":["ev-p090-entropy-router","ev-p090-association-graph"],"source_refs":[{"path":"papers/P090_memgas.pdf","sha256":"256eba2430611820eb4b18978fdd35f05a3bcf26c7b808b03ef0971ab3bc49c8"}]} -->
# Entropy-Routed Multi-Granularity Memory Retrieval with Association Graph

## Intervention target
[CODEX_SYNTHESIS] memory read path 的检索单元选择：查询应在哪个粒度（session/turn/summary/keyword）上检索，以及跨粒度记忆如何互联。

## Before and after computation
[CODEX_SYNTHESIS] Before：固定粒度检索（单一 chunk 类型 top-k）。After：对每个查询计算各粒度相似度分布的 Shannon 熵，逆熵归一化成 soft router 权重；写入时各粒度节点经 accept/reject 集建边，维护跨粒度关联图，检索时以 PPR 在图上扩展关键节点。

## Inputs outputs information and timing
[AUTHOR_FACT] 输入：query 与全部粒度记忆的相似度向量；熵 Hg 量化 query 在粒度 g 上匹配的不确定性。输出：粒度权重与路由决策。时点：检索时（路由）+ 写入时（关联图构建）。[[evidence:ev-p090-entropy-router]] [[evidence:ev-p090-association-graph]]

## Mechanism hypothesis
[CODEX_HYPOTHESIS] 低熵=分布尖锐=该粒度存在明确对应记忆；把粒度选择变成分布形状判断，避免为每个查询训练粒度分类器。

## Predicted observable signature
[CODEX_HYPOTHESIS] 相对最优单一粒度，多粒度路由在混合查询集上同时降低漏检与噪声；按查询类型分层时，精确事实查询路由向细粒度、聚合型查询路由向 summary。

## Preconditions and transfer risks
[CODEX_SYNTHESIS] 前提：各粒度记忆表示已存在且可比相似度；熵信号依赖记忆池规模（池过小时分布退化）。转移风险：路由单项贡献仅在单基准消融（Table 3, LongMemEval-s，含检索侧指标）中被量化，主结果为检索+生成管线联动；λ 温度超参影响熵的判别力。

## Source lineage
[CODEX_SYNTHESIS] 单粒度记忆系统 → topic-aware 切分 → MemGAS 多粒度关联与熵路由。

## Evidence ledger
[AUTHOR_FACT] 熵定义/soft 权重与关联图 accept-set 构建分别绑定 exact Passage。[[evidence:ev-p090-entropy-router]] [[evidence:ev-p090-association-graph]]

## Retrieval vocabulary
[CODEX_SYNTHESIS] entropy router; multi-granularity association; personalized PageRank; soft router weights; Shannon entropy; granularity confidence; memory association graph; GMM; entropy-based granularity routing; adaptive granularity selection; query-adaptive memory retrieval; retrieving memories at multiple granularities; routing by similarity entropy
