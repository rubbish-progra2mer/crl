<!-- CRL_CARD_META {"schema_version":1,"card_id":"failure-one-shot-expert-gold-is-brittle","card_kind":"failure","paper_id":"P068","evidence_ids":["ev-p068-audit-then-score","ev-p068-one-shot-gold-brittle"],"source_refs":[{"path":"papers/P068_deepfact.pdf","sha256":"a26aeaefd0f1c763a40c1383c3a18ac723629519f6089abcdfe85ad74057f079"}]} -->
# One-Shot Expert Gold Can Mis-score Deep Research Claims

## Observed failure
[AUTHOR_FACT] hidden micro-golds 上的人类 benchmark accuracy 经审计轮次由 60.8% 升至 90.9%。[[evidence:ev-p068-one-shot-gold-brittle]]

## Conditions and scope
[CODEX_SYNTHESIS] 绑定需要多来源事实核验的 Deep Research benchmark，不外推到所有静态标签任务。

## Failed intervention
[CODEX_SYNTHESIS] 把首版 expert gold 当不可修订真值，直接判 Agent claim 对错。

## Evidence and alternative explanations
[CODEX_SYNTHESIS] gold 错误与 Agent factuality error 会混合；多轮 audit 也引入更多 token、模型与潜在共演化偏差。

## Warning for future candidates
[CODEX_SYNTHESIS] factuality 实验必须保留 evidence-backed label dispute 与版本，不得用更贵 verifier 的总分替代机制消融。

## Possible repair boundary
[AUTHOR_FACT] 仅当 challenger 与 current benchmark disagreement 时，challenger→auditor→accepted revision→score 提供可审计修订路径；这不是全量标签重审。[[evidence:ev-p068-audit-then-score]]

## Evidence ledger
[CODEX_SYNTHESIS] gold brittleness 与 audit pipeline 有直接 Evidence。

## Retrieval vocabulary
[CODEX_SYNTHESIS] brittle benchmark gold; factuality label error; evidence adjudication; deep research scoring
