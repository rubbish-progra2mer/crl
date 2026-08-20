<!-- CRL_CARD_META {"schema_version":1,"card_id":"operator-validated-specialized-tool-creation-retrieval","card_kind":"operator","paper_id":"P078","evidence_ids":["ev-p078-validated-tool-creation-retrieval","ev-p078-multiview-tool-retrieval","ev-p078-generic-tool-and-baseline-boundary","ev-p078-toolset-construction-cost","ev-p078-baseline-fairness-boundary"],"source_refs":[{"path":"papers/P078_craft.pdf","sha256":"59263fffdc51e21530d9dba1aeeeacefb2b5c4048012a7e385b4f555a362f155"}]} -->
# Validated Specialized Tool Creation and Multi-View Retrieval

## Intervention target
[CODEX_SYNTHESIS] Agent 生成解法前的 executable tool memory：离线构建质量与在线选择共同改变可用 computation。

## Before and after computation
[CODEX_SYNTHESIS] 通用/未筛工具直接入 prompt → 从多样问题生成代码、抽象为复用函数、原题执行验证与去重，再按问题/函数名/docstring 三视图召回。[[evidence:ev-p078-validated-tool-creation-retrieval]] [[evidence:ev-p078-multiview-tool-retrieval]]

## Inputs outputs information and timing
[CODEX_SYNTHESIS] 离线输入是 problem-answer pairs，输出是 validated toolset；在线输入是 target problem 与生成的函数描述，输出是少量 executable tools。

## Mechanism hypothesis
[CODEX_HYPOTHESIS] 先验证专用工具、再按多表述召回，可同时减少错误工具与无关工具的干扰。

## Predicted observable signature
[CODEX_HYPOTHESIS] 相比同 token budget 的 generic library，相关工具命中与执行正确率应提高，distractor-induced errors 应下降。

## Preconditions and transfer risks
[AUTHOR_FACT] generic libraries 和多种 creation/retrieval baselines 并非稳定增益。[[evidence:ev-p078-generic-tool-and-baseline-boundary]] [CODEX_SYNTHESIS] 这里的 validation 只证明 originating-instance preservation，不证明跨分布泛化。
[AUTHOR_FACT] 离线工具库构建估算约 USD 2,500。[[evidence:ev-p078-toolset-construction-cost]] [AUTHOR_FACT] TabMWP 上 BM25 略高于 CRAFT，且 CREATOR comparison 移除了 checking/rectifying loop。[[evidence:ev-p078-baseline-fairness-boundary]] [CODEX_SYNTHESIS] 论文没有建立 equal-total-token/API/cost 优势，backbone tool-use ability 也必须匹配。

## Source lineage
[CODEX_SYNTHESIS] 从 P078 抽象，组合 tool creation、program abstraction、execution validation 与 multi-view retrieval。

## Evidence ledger
[CODEX_SYNTHESIS] validation、retrieval、负向 baseline、离线成本与 comparator 修改均绑定 Evidence。

## Retrieval vocabulary
[CODEX_SYNTHESIS] specialized executable tool memory; tool abstraction validation; multi-view retrieval; tool library distractors; reusable code tools
