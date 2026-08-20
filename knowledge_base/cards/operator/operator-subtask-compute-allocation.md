<!-- CRL_CARD_META {"schema_version":1,"card_id":"operator-subtask-compute-allocation","card_kind":"operator","paper_id":"P020","evidence_ids":["ev-p020-compute-allocation-search"],"source_refs":[{"path":"papers/P020_agenttts.pdf","sha256":"454906b0f931fd092ab25163c1ea3fd69e793eac570320ba257d174bee9b0c7c"}]} -->
# Subtask Model-and-Budget Allocation Search

## Intervention target
[AUTHOR_FACT] 在多阶段任务中搜索各 subtask 的 compute-optimal budget allocation。[[evidence:ev-p020-compute-allocation-search]]

## Before and after computation
[CODEX_SYNTHESIS] 最近 baseline 是同样进行迭代 trial-feedback 搜索的 AgentHPO/MLCopilot；changed computation 是把三条 task-derived scaling priors 与特定初始化加入搜索，并联合选择每阶段 model 与 sample budget。固定模型/均匀采样只作为概念对照。

## Inputs outputs information and timing
[CODEX_SYNTHESIS] 输入为任务分解、候选模型/预算与历史试验反馈，输出为阶段配置；搜索发生在部署配置确定前并消耗额外试验计算。

## Mechanism hypothesis
[CODEX_SYNTHESIS] 把计算分配给最敏感阶段并考虑上游选择对下游的影响，可优于均匀扩算。

## Predicted observable signature
[CODEX_HYPOTHESIS] 相同总 FLOPs 下应出现非均匀 allocation 优势，而不是仅由更强模型池或更多先验试验解释。

## Preconditions and transfer risks
[CODEX_SYNTHESIS] 需要可分阶段任务、可比成本度量与冻结 model pool；搜索 prior 和模型能力是重要混杂。

## Source lineage
[CODEX_SYNTHESIS] AgentTTS 是直接来源；ToT 搜索 thought states，本 Operator 搜索执行配置，两者不能合并为同一机制。

## Evidence ledger
[AUTHOR_FACT] `ev-p020-compute-allocation-search` 定位到 PDF p.2 的 changed computation。[[evidence:ev-p020-compute-allocation-search]]

## Retrieval vocabulary
[CODEX_SYNTHESIS] test-time scaling；compute allocation；model routing；sample budget；multi-stage task；测试时计算分配。
