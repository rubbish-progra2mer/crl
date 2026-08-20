<!-- CRL_CARD_META {"schema_version":1,"card_id":"paper-p090","card_kind":"paper","paper_id":"P090","evidence_ids":["ev-p090-fixed-granularity-selection","ev-p090-entropy-router","ev-p090-association-graph"],"source_refs":[{"path":"papers/P090_memgas.pdf","sha256":"256eba2430611820eb4b18978fdd35f05a3bcf26c7b808b03ef0971ab3bc49c8"}]} -->
# MemGAS: Multi-Granularity Memory Association and Selection

## Role in the knowledge base
[CODEX_SYNTHESIS] 读侧查询条件化多粒度分配的直接先行工作，也是 memory 簇 2025 段的重要谱系节点。

## Problem and setting
[AUTHOR_FACT] 多 session 对话记忆：固定单一粒度切分导致 incomplete recall 或噪声，且缺少 per-query 自适应粒度选择。[[evidence:ev-p090-fixed-granularity-selection]]

## Changed computation
[AUTHOR_FACT] 写入：LLM 生成 summary/keyword，raw session 及其 turn 切分共同构成四粒度记忆（session/turn/summary/keyword），各粒度节点经 accept/reject 集接入关联图。[[evidence:ev-p090-association-graph]]
[AUTHOR_FACT] 读取：按各粒度相似度分布的 Shannon 熵计算 soft router 权重，PPR 图扩展后过滤。[[evidence:ev-p090-entropy-router]]

## Evidence-backed findings
[CODEX_SYNTHESIS] 在 LongMemEval/LoCoMo 系基准上对单粒度与既有记忆系统报告一致增益（QA 与检索两侧）；细节数字系管线级效应，reconciliation 记录了检索/生成联动混杂。

## Limitations and failure signals
[CODEX_SYNTHESIS] 粒度路由单项贡献仅在 LongMemEval-s 消融（Table 3 w/o Router）中被量化，跨基准主表增益仍系管线级效应；LLM 生成 summary/keyword 的成本随对话增长；时序有效性（版本冲突）不在其机制内——与 P091/P095 的 freshness 轴正交。

## Lineage and baselines
[CODEX_SYNTHESIS] 单粒度记忆（MemoryBank/MemGPT 系）→ topic-aware 切分 → 多粒度关联+熵路由。任何新的读侧粒度分配方法都应将本文视为最近先行工作，并给出真正不同的决策计算。

## Evidence ledger
[CODEX_SYNTHESIS] 失败定性、熵路由、关联图三条均绑定 exact Passage。

## Retrieval vocabulary
[CODEX_SYNTHESIS] MemGAS; multi-granularity memory; entropy-based router; memory association; long-term conversational memory; granularity selection; LongMemEval; multi-granularity conversational memory; adaptive retrieval granularity; memory association and selection
