<!-- CRL_CARD_META {"schema_version":1,"card_id":"failure-incomplete-tool-contracts-false-verified-state","card_kind":"failure","paper_id":"P074","evidence_ids":["ev-p074-contract-state-commit","ev-p074-missing-schema-true-postcondition"],"source_refs":[{"path":"papers/P074_toolgate.pdf","sha256":"7073bc0a27cf0f002ea4d1ef0ec3726d5c70c7e44a218e78f46d92284aba289d"}]} -->
# Incomplete Contracts Can Admit False Verified State

## Observed failure
[AUTHOR_FACT] 当 ToolBench 工具无结构化 response schema 时，来源实现把 postcondition 设为 Q=True，约覆盖 25% tools。[[evidence:ev-p074-missing-schema-true-postcondition]]

## Conditions and scope
[CODEX_SYNTHESIS] 这是 contract-relative verification 的结构边界，不是 P074 实验中已经测得的安全事故率。

## Failed intervention
[CODEX_SYNTHESIS] 给工具加“verified”标签，却没有覆盖关键语义、所有副作用和返回约束。

## Evidence and alternative explanations
[AUTHOR_FACT] 完整设计要求 P gate 与 Q-gated state update。[[evidence:ev-p074-contract-state-commit]] [CODEX_SYNTHESIS] 若 Q 缺失，程序仍可机械通过，但无法排除 semantic false positive。

## Warning for future candidates
[CODEX_SYNTHESIS] 不得用 contract 存在性代替 contract coverage；实验需注入 schema-valid but semantically-wrong results，并报告 false commit。

## Possible repair boundary
[CODEX_HYPOTHESIS] 将“无法验证”保持为 unknown、隔离未验证结果，可能优于 Q=True；这需要新实验，不能由 P074 自动背书。

## Evidence ledger
[CODEX_SYNTHESIS] Evidence 固定了 intended gate 与来源中真实的 default-true 漏口。

## Retrieval vocabulary
[CODEX_SYNTHESIS] incomplete contract; Q true fallback; false verified state; postcondition coverage; semantic false commit
