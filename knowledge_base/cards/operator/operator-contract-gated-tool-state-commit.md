<!-- CRL_CARD_META {"schema_version":1,"card_id":"operator-contract-gated-tool-state-commit","card_kind":"operator","paper_id":"P074","evidence_ids":["ev-p074-contract-state-commit","ev-p074-missing-schema-true-postcondition"],"source_refs":[{"path":"papers/P074_toolgate.pdf","sha256":"7073bc0a27cf0f002ea4d1ef0ec3726d5c70c7e44a218e78f46d92284aba289d"}]} -->
# Contract-Gated Tool State Commit

## Intervention target
[CODEX_SYNTHESIS] 干预 tool result 从不可信 runtime output 进入 Agent trusted state 的边界。

## Before and after computation
[CODEX_SYNTHESIS] Before：缺少独立 contract gate 时，tool call/result 可被自然语言推理直接接受。[AUTHOR_FACT] After：P 检查调用合法性，Q 检查返回结构、类型与语义，只有验证通过才更新 state。[[evidence:ev-p074-contract-state-commit]]

## Inputs outputs information and timing
[CODEX_SYNTHESIS] 输入为 typed state、由 tool documentation/interface schema 预先提取的 P/Q contract、arguments 与 runtime result；输出为 reject/commit 及下一 trusted state；时点横跨调用前和返回后。

## Mechanism hypothesis
[CODEX_HYPOTHESIS] 若长轨迹错误主要通过一次错误返回污染后续推理，post-return commit gate 应降低错误级联，而不仅减少非法调用。

## Predicted observable signature
[CODEX_HYPOTHESIS] 在 matched tool calls 下，invalid-result state contamination 下降；移除 Q 时的退化应大于仅换 prompt 的波动。

## Preconditions and transfer risks
[AUTHOR_FACT] 没有结构化 response schema 时，来源实现对约 25% ToolBench tools 使用 Q=True。[[evidence:ev-p074-missing-schema-true-postcondition]] [CODEX_SYNTHESIS] contract 未覆盖副作用或语义时，verified 只表示“符合现有 contract”。

## Source lineage
[CODEX_SYNTHESIS] 来源 P074；未来 implement 应与 precondition-only gate、postcondition-only gate 及等调用预算 baseline 比较。

## Evidence ledger
[CODEX_SYNTHESIS] changed computation 与 contract completeness 风险均被 Evidence 固定。

## Retrieval vocabulary
[CODEX_SYNTHESIS] postcondition commit gate; verified state update; tool result validation; Hoare contract; trusted state contamination
