<!-- CRL_CARD_META {"schema_version":1,"card_id":"failure-fixed-shortlist-depth-masks-hard-query-zero","card_kind":"failure","paper_id":"P100","evidence_ids":["ev-p100-fixed-depth-buckets","ev-p100-weak-scorer-collapse"],"source_refs":[{"path":"papers/P100_tool_shortlist_size.pdf","sha256":"4db89bfac79bc90dd5b532d04ac1012ed1691657a45379bbbb2312682847164c"}]} -->
# Fixed Shortlist Depth Zeroes Hard-Query Coverage While Winning Aggregate Numbers

## Observed failure
[AUTHOR_FACT] ToolBench 难度分桶：gold 排 6-20 时 FK=5、FK=1、F1 消融全部 found 0%（BoR 16.7±4.3%）；FK=5 聚合覆盖反而更高（64.7 vs 61.9）——均匀深度吃满 easy/medium、hard 及以上全灭，聚合指标掩盖分布性失败。[[evidence:ev-p100-fixed-depth-buckets]]

## Conditions and scope
[CODEX_SYNTHESIS] 工具检索截断步骤（scorer 排序后、prompt 前）；Rq=1 构造候选集；preprint（Meta Platforms）。与查询无关的固定深度惩罚（F1 型奖励）同病：训出的策略各桶 K≈1.5 不随难度动。

## Failed intervention
[CODEX_SYNTHESIS] 把展示深度 K 当一次性超参（选定后不再随查询调整）；或用与查询/registry 无关的固定深度惩罚做"自适应"。

## Evidence and alternative explanations
[AUTHOR_FACT] 边界条件：自适应深度依赖 scorer 判别力——BM25 found@1=33% 时 BoR agent 膨胀到 K=80.7（近全量展示，1.04 bits 选择性），弱 scorer 下无处可停。[[evidence:ev-p100-weak-scorer-collapse]]
[CODEX_SYNTHESIS] 下游"少展示提升选择质量"（93.1 vs 87.1）的点值含条件化选择偏差（各方法呈现集不同）——方向存活（FK=5 medium 桶 100% 呈现仍只 60.9% 选对），点值不引用。

## Warning for future candidates
[CODEX_SYNTHESIS] 查询条件化菜单宽度已有 [30] 与本文直接覆盖。deep-vs-fixed 对比必须按难度桶报告，单一聚合数可能选错方法。

## Possible repair boundary
[CODEX_HYPOTHESIS] 作者明确留下的开放面是执行层正确性（选中后的调用）与 Rq>1 多工具场景。

## Evidence ledger
[CODEX_SYNTHESIS] 分桶归零与弱 scorer 崩溃绑定 exact Passage。

## Retrieval vocabulary
[CODEX_SYNTHESIS] fixed K; shortlist depth; difficulty buckets; hard query zero coverage; aggregate masking; adaptive depth collapse; weak scorer; tool retrieval truncation; fixed top-k truncation; zero coverage on hard queries; aggregate coverage misleads; uniform retrieval depth failure; showing the same number of tools for every query
