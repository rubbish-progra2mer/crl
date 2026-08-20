<!-- CRL_CARD_META {"schema_version":1,"card_id":"operator-chance-corrected-depth-reward","card_kind":"operator","paper_id":"P100","evidence_ids":["ev-p100-bor-self-pruning","ev-p100-fixed-depth-buckets"],"source_refs":[{"path":"papers/P100_tool_shortlist_size.pdf","sha256":"4db89bfac79bc90dd5b532d04ac1012ed1691657a45379bbbb2312682847164c"}]} -->
# Chance-Corrected Depth Reward (BoR) for Per-Query Shortlist Sizing

## Intervention target
[CODEX_SYNTHESIS] 检索截断深度 K：从固定超参变为逐查询决策变量，深度惩罚由度量结构内生。

## Before and after computation
[AUTHOR_FACT] BoR 奖励随列表增长自然下降——Prand 随每个新增工具上升（K=3/500 工具约 7 bits，K=100 约 2 bits）；下降不是工程惩罚项而是度量结构的数学后果。[[evidence:ev-p100-bor-self-pruning]]
[CODEX_SYNTHESIS] 停止策略：逐项检查排序列表，STOP/CONTINUE 二元 MDP，STOP 命中时奖励 -log2(Prand(kstop))；状态只看分数形状特征（top score/gap/spread/深度/N）。

## Inputs outputs information and timing
[CODEX_SYNTHESIS] 输入：scorer 全量排序 + 相似度分数形状。输出：逐查询 kstop。时点：打分后、prompt 构建前；训练用 oracle 相关性标注、推理不用。

## Mechanism hypothesis
[CODEX_HYPOTHESIS] 分数分布形状携带查询难度信息；chance-correction 使"短列表命中"天然更值钱，无需逐条件调深度惩罚。

## Predicted observable signature
[AUTHOR_FACT] 深度随难度桶单调上升（2.5→6.9）而 F1 型固定惩罚各桶不动（K≈1.5）；hard 桶恢复其他方法全灭的覆盖。[[evidence:ev-p100-fixed-depth-buckets]]

## Preconditions and transfer risks
[CODEX_SYNTHESIS] 归属注意：BoR 指标本身出自引文 [30]（作者重叠，ICLR Blogposts 2026）——本文贡献是奖励化+分桶+下游验证。前提：scorer 有判别力（弱 scorer 退化为全展示）、Rq 已知或=1。风险：策略对 step_cost 敏感（0.005→0.01 使 K 7.4→2.2）；奖励 bits 跨语料不可比（Prand 分母口径）；MetaTool 条件单 seed。

## Source lineage
[CODEX_SYNTHESIS] 化学信息学 chance-correction（BEDROC/enrichment factor）→ BoR [30] → 工具选择强化学习化（本文）。

## Evidence ledger
[AUTHOR_FACT] self-pruning 结构与分桶签名绑定 exact Passage。[[evidence:ev-p100-bor-self-pruning]] [[evidence:ev-p100-fixed-depth-buckets]]

## Retrieval vocabulary
[CODEX_SYNTHESIS] Bits-over-Random; chance-corrected reward; self-pruning; STOP CONTINUE policy; per-query depth; hypergeometric Prand; BoR ceiling; doubling rule; chance-corrected stopping reward; probability a random selection succeeds; per-query stopping policy; deciding how many tools to show; adaptive shortlist depth; stopping over a ranked candidate list
