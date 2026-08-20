<!-- CRL_CARD_META {"schema_version":1,"card_id":"failure-repeat-run-reliability-collapse","card_kind":"failure","paper_id":"P007","evidence_ids":["ev-p007-repeat-reliability-collapse"],"source_refs":[{"path":"papers/P007_tau_bench.pdf","sha256":"e2d45d573e1fce753ead1a44cc468ad386dd384e2668450d0a9c0e2c7920ada0"}]} -->
# Single-Run Success Hides Repeat-Run Reliability Collapse

## Observed failure
[AUTHOR_FACT] 作者报告所测强 function-calling agents 的总体单次成功有限，且 retail 的 pass^8 低于 25%。[[evidence:ev-p007-repeat-reliability-collapse]]

## Conditions and scope
[CODEX_SYNTHESIS] 这是特定工具—用户交互任务、agent setup 与重复独立 trials 下的结果。

## Failed intervention
[CODEX_SYNTHESIS] 只优化或报告 pass^1 没有改变 stochastic policy 的重复可靠性。

## Evidence and alternative explanations
[CODEX_SYNTHESIS] 用户模拟变化、policy compliance、tool formatting 与模型采样都可能造成跨 trial 不一致。

## Warning for future candidates
[CODEX_SYNTHESIS] 候选若声称“可靠”，必须给 repeat-run 指标，而不能展示一次成功轨迹。

## Possible repair boundary
[CODEX_HYPOTHESIS] 显式状态核验、约束动作或不确定性触发复查可能改善 pass^k，需要等预算检验。

## Evidence ledger
[AUTHOR_FACT] `ev-p007-repeat-reliability-collapse` 定位到 PDF p.1 的 pass^8 负向结果。[[evidence:ev-p007-repeat-reliability-collapse]]

## Retrieval vocabulary
[CODEX_SYNTHESIS] pass^k；repeatability；stochastic reliability；tool-agent inconsistency；重复运行可靠性。
