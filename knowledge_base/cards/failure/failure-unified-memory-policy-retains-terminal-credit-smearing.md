<!-- CRL_CARD_META {"schema_version":1,"card_id":"failure-unified-memory-policy-retains-terminal-credit-smearing","card_kind":"failure","paper_id":"P062","evidence_ids":["ev-p062-unified-memory-action-policy","ev-p062-broadcast-advantage"],"source_refs":[{"path":"papers/P062_agentic_memory_unified.pdf","sha256":"ba41464f84dbd8e0d0aeb1e6e0d7fd83b4086b2922579b88f7947448a8e1958f"}]} -->
# Unified Memory Actions Do Not by Themselves Localize Credit

## Observed failure
[AUTHOR_FACT] P062 用同一 trajectory-level advantage 监督此前 memory 与 reasoning steps。[[evidence:ev-p062-broadcast-advantage]]

## Conditions and scope
[AUTHOR_FACT] 训练 task specification `T` 含 expected answer `A_q`。[[evidence:ev-p062-unified-memory-action-policy]] [CODEX_SYNTHESIS] 这是 training-only oracle 与 credit-identification 边界，不否认统一 policy 的总体结果，也不得把 `A_q` 带入部署。

## Failed intervention
[CODEX_SYNTHESIS] 联合 language/memory action space 改变了控制权，但没有单独识别哪次 memory action 产生效果。[[evidence:ev-p062-unified-memory-action-policy]]

## Evidence and alternative explanations
[CODEX_SYNTHESIS] policy 可从统计相关中学习，但不能据此声称获得 step-specific causal credit。

## Warning for future candidates
[CODEX_SYNTHESIS] memory-learning Candidate 必须区分“能选择 memory action”与“知道该 action 的局部价值”。

## Possible repair boundary
[CODEX_HYPOTHESIS] 非 Oracle 的 counterfactual/action grouping 才可能提供更局部比较。

## Evidence ledger
[CODEX_SYNTHESIS] action-space change 与 credit broadcast 各有 Evidence。

## Retrieval vocabulary
[CODEX_SYNTHESIS] memory credit assignment; trajectory advantage broadcast; unified memory action; step credit
