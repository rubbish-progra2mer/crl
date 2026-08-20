<!-- CRL_CARD_META {"schema_version":1,"card_id":"paper-p100","card_kind":"paper","paper_id":"P100","evidence_ids":["ev-p100-fixed-depth-buckets","ev-p100-bor-self-pruning","ev-p100-weak-scorer-collapse"],"source_refs":[{"path":"papers/P100_tool_shortlist_size.pdf","sha256":"4db89bfac79bc90dd5b532d04ac1012ed1691657a45379bbbb2312682847164c"}]} -->
# How Many Tools Should an LLM Agent See? A Chance-Corrected Answer

## Role in the knowledge base
[CODEX_SYNTHESIS] 查询条件化工具菜单宽度的直接先行工作，并为 tool 簇提供失败模式与测量方法。

## Problem and setting
[CODEX_SYNTHESIS] 检索深度 K 通常一次选定不再复查；把"展示多少工具"本身作为评测与学习对象。

## Changed computation
[AUTHOR_FACT] 评估层 BoR（chance-corrected 选择性）+ 控制层 RL 停止策略（BoR 奖励内生深度压力）。[[evidence:ev-p100-bor-self-pruning]]

## Evidence-backed findings
[AUTHOR_FACT] 难度分桶分离（hard 桶其他方法全 0%）与聚合掩盖；弱 scorer 负结果（K=80.7 膨胀）。[[evidence:ev-p100-fixed-depth-buckets]] [[evidence:ev-p100-weak-scorer-collapse]]
[CODEX_SYNTHESIS] BFCL 90.3%@K=7.4≈FK=50；下游 over-presentation 有害方向稳健（点值含条件化偏差）。

## Limitations and failure signals
[CODEX_SYNTHESIS] BoR 归属 [30]（本文 RL 化）；下游超参绑定（step_cost 敏感 3 倍）；F1 消融一条件用简化变体；MetaTool 单 seed；构造候选集数字不代表原基准检索性能；found@1 两处口径不一致（OPEN）；单 LLM 下游、执行正确性超范围、Rq=1 全域。

## Lineage and baselines
[CODEX_SYNTHESIS] DynamicRAG（文档侧最近先行，其自认）；Less-is-More/ToolRerank 过滤线。作者明确留下的开放面是执行层正确性与 Rq>1 多工具场景。

## Evidence ledger
[CODEX_SYNTHESIS] 三条 evidence 锚定分桶失败、self-pruning、弱 scorer 崩溃。

## Retrieval vocabulary
[CODEX_SYNTHESIS] tool shortlist size; search depth K; Bits-over-Random; adaptive stopping; tool retrieval; BFCL MetaTool ToolBench; distractor load; Meta Platforms; how many tools should an agent see; adaptive search depth; sizing the tool shortlist
