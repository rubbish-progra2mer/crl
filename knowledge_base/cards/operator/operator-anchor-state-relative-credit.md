<!-- CRL_CARD_META {"schema_version":1,"card_id":"operator-anchor-state-relative-credit","card_kind":"operator","paper_id":"P065","evidence_ids":["ev-p065-anchor-state-credit","ev-p065-state-recurrence-boundary","ev-p026-uniform-terminal-return"],"source_refs":[{"path":"papers/P065_gigpo.pdf","sha256":"f6a4d4559c41048be67a0e4a062f9957996fc79e6a80f65fe66f1140fac82dcd"},{"path":"papers/P026_agent_lightning.pdf","sha256":"e223648a09b021785a46f60dd5ce13301622eca930ff91a5b45e971b53422561"}]} -->
# Anchor-State Relative Credit Assignment

## Intervention target
[CODEX_SYNTHESIS] 稀疏终局 reward 下同一 state 的 action-level advantage。

## Before and after computation
[CODEX_SYNTHESIS] uniform episode return for every action → compare actions that naturally occur at repeated identical anchor states。[[evidence:ev-p026-uniform-terminal-return]] [[evidence:ev-p065-anchor-state-credit]]

## Inputs outputs information and timing
[CODEX_SYNTHESIS] 输入为一组轨迹中完全相同 environment state 下的 actions 与 discounted returns；输出为该 anchor group 的 relative advantage；训练时计算，不额外 rollout 该 state。

## Mechanism hypothesis
[CODEX_HYPOTHESIS] 相同 state 下不同 action 的 outcome 差异比跨 state terminal return 更接近局部 credit。

## Predicted observable signature
[CODEX_HYPOTHESIS] 改善集中在高 recurrence states；低 recurrence 时 coverage 与收益同步下降。

## Preconditions and transfer risks
[AUTHOR_FACT] ALFWorld 中该机制依赖较高 state recurrence。[[evidence:ev-p065-state-recurrence-boundary]]

## Source lineage
[CODEX_SYNTHESIS] P026 uniform-return baseline → P065 anchor refinement；二者不是独立 evidence families。

## Evidence ledger
[CODEX_SYNTHESIS] baseline、changed credit 与 recurrence boundary 均有 Evidence。

## Retrieval vocabulary
[CODEX_SYNTHESIS] anchor-state credit; local action advantage; repeated identical state; sparse terminal reward
