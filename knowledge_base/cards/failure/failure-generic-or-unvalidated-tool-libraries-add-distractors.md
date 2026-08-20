<!-- CRL_CARD_META {"schema_version":1,"card_id":"failure-generic-or-unvalidated-tool-libraries-add-distractors","card_kind":"failure","paper_id":"P078","evidence_ids":["ev-p078-validated-tool-creation-retrieval","ev-p078-multiview-tool-retrieval","ev-p078-generic-tool-and-baseline-boundary","ev-p078-toolset-construction-cost","ev-p078-baseline-fairness-boundary"],"source_refs":[{"path":"papers/P078_craft.pdf","sha256":"59263fffdc51e21530d9dba1aeeeacefb2b5c4048012a7e385b4f555a362f155"}]} -->
# Generic or Unvalidated Tool Libraries Can Fail to Improve and May Hurt

## Observed failure
[AUTHOR_FACT] 外部 Python tools、LATM、CREATOR 与检索 baselines 在所测任务中表现不稳定，某些数学设置甚至退化。[[evidence:ev-p078-generic-tool-and-baseline-boundary]]

## Conditions and scope
[CODEX_HYPOTHESIS] 当 tool relevance、correctness、abstraction 或 retrieval 与当前任务不匹配时，更多 tools 可能扩大错误选择面；P078 没有隔离或直接测量 distractor-induced errors。

## Failed intervention
[AUTHOR_FACT] 直接加入 external Python tools 及若干 creation/retrieval baselines 没有稳定提升。[[evidence:ev-p078-generic-tool-and-baseline-boundary]]

## Evidence and alternative explanations
[AUTHOR_FACT] CRAFT 先验证抽象工具能解决原始问题。[[evidence:ev-p078-validated-tool-creation-retrieval]] [AUTHOR_FACT] 在线选择结合问题、函数名与 docstring 三视图。[[evidence:ev-p078-multiview-tool-retrieval]]

## Warning for future candidates
[CODEX_SYNTHESIS] “加入工具库”不是机制；必须分别对照 tool quality、retrieval、prompt length、backbone ability 与 execution correction，且原题回放不能冒充跨分布验证。[AUTHOR_FACT] 来源估算离线建库约 USD 2,500。[[evidence:ev-p078-toolset-construction-cost]] [AUTHOR_FACT] TabMWP 上 BM25 略高，且 CREATOR comparison 移除了 checking/rectifying loop。[[evidence:ev-p078-baseline-fairness-boundary]]

## Possible repair boundary
[CODEX_HYPOTHESIS] 在同成本下验证、去重并按任务语义召回专用 tools；跨分布与 backbone 依赖仍需独立实验。

## Evidence ledger
[CODEX_SYNTHESIS] baseline failure、validation、retrieval、成本与 comparator 修改均由 Evidence 支撑；distractor 因果仅为 hypothesis。

## Retrieval vocabulary
[CODEX_SYNTHESIS] tool library distractor; generic tools hurt; unvalidated generated tools; specialized tool retrieval; tool relevance failure
