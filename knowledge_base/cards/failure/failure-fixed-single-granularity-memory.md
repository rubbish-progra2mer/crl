<!-- CRL_CARD_META {"schema_version":1,"card_id":"failure-fixed-single-granularity-memory","card_kind":"failure","paper_id":"P090","evidence_ids":["ev-p090-fixed-granularity-selection","ev-p090-entropy-router"],"source_refs":[{"path":"papers/P090_memgas.pdf","sha256":"256eba2430611820eb4b18978fdd35f05a3bcf26c7b808b03ef0971ab3bc49c8"}]} -->
# Fixed Single-Granularity Memory Segmentation Loses Recall or Adds Noise

## Observed failure
[AUTHOR_FACT] 现有长期记忆方法依赖固定 granularity 策略（session/turn 切分或 LLM summary），导致 incomplete context recall 或因 granularity 不当引入 noise；topic-aware 切分也缺少 per-query 的自适应选择机制。[[evidence:ev-p090-fixed-granularity-selection]]

## Conditions and scope
[CODEX_SYNTHESIS] 多 session 对话记忆检索；查询对最佳粒度的需求随查询而变（精确匹配偏细粒度、模糊查询偏粗粒度）。载体为对话 QA/检索基准（LongMemEval、LoCoMo 系）。

## Failed intervention
[CODEX_SYNTHESIS] 把单一预定粒度（只用 session chunk、只用 turn、只用 summary）作为记忆检索单元，并寄望嵌入检索器自行补偿粒度错配。

## Evidence and alternative explanations
[AUTHOR_FACT] MemGAS 以 entropy 度量各粒度上 query-memory 相似度分布的不确定性，作为粒度置信信号——低熵对应精确匹配置信高。[[evidence:ev-p090-entropy-router]]
[CODEX_SYNTHESIS] 该论文的增益数字含检索+生成管线联动，不能把全部增益归于粒度路由单项；但"固定粒度=错配来源"的失败定性由其消融与动机分析共同支撑。

## Warning for future candidates
[CODEX_SYNTHESIS] 任何只在单一粒度上操作的 memory-read 候选方法，都必须说明为何粒度错配不构成残差来源；读侧多粒度分配已被本文直接覆盖，后续工作需要真正不同的粒度决策计算。

## Possible repair boundary
[CODEX_HYPOTHESIS] per-query 粒度路由（熵或其他分布形状信号）+ 跨粒度关联图是已占位的修复族；未占位的是把粒度选择与时序有效性（版本/新鲜度）联合裁决的组合。

## Evidence ledger
[CODEX_SYNTHESIS] 固定粒度失败定性与 entropy 路由机制分别绑定 exact Passage（Introduction 与 §2.3）。

## Retrieval vocabulary
[CODEX_SYNTHESIS] single granularity; session chunk; turn-level segmentation; summary memory; granularity mismatch; adaptive granularity selection; multi-granularity memory; MemGAS; fixed segmentation; session-level chunking; incomplete recall; noisy memory retrieval; per-query granularity routing; segmenting conversations
