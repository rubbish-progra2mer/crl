<!-- CRL_CARD_META {"schema_version":1,"card_id":"failure-diminishing-compute-return","card_kind":"failure","paper_id":"P020","evidence_ids":["ev-p020-diminishing-compute-return"],"source_refs":[{"path":"papers/P020_agenttts.pdf","sha256":"454906b0f931fd092ab25163c1ea3fd69e793eac570320ba257d174bee9b0c7c"}]} -->
# Additional Test-Time Compute Has Diminishing or Zero Return

## Observed failure
[AUTHOR_FACT] 论文观察到计算增加到一定点后出现 diminishing or no gains，且上游预算影响下游需求。[[evidence:ev-p020-diminishing-compute-return]]

## Conditions and scope
[CODEX_SYNTHESIS] 结论针对所测多阶段任务、model pool 与 FLOPs 定义，不是通用 scaling law。

## Failed intervention
[CODEX_SYNTHESIS] 均匀增加每阶段采样没有考虑 subtask 异质性和阶段间依赖。

## Evidence and alternative explanations
[CODEX_SYNTHESIS] 饱和可能来自 verifier、候选多样性、模型能力或预算换算；不能仅由总 FLOPs 解释。

## Warning for future candidates
[CODEX_SYNTHESIS] “更多 test-time compute”不是机制，必须写清分配位置、模型池与 fixed-budget baseline。

## Possible repair boundary
[CODEX_HYPOTHESIS] 选择性 allocation 可减少无效计算，但需控制搜索 prior 和配置试验成本。

## Evidence ledger
[AUTHOR_FACT] `ev-p020-diminishing-compute-return` 定位到 PDF p.2 的收益递减或无收益边界。[[evidence:ev-p020-diminishing-compute-return]]

## Retrieval vocabulary
[CODEX_SYNTHESIS] diminishing returns；test-time compute saturation；budget allocation；fixed FLOPs；测试时计算饱和。
