<!-- CRL_CARD_META {"schema_version":1,"card_id":"paper-p065","card_kind":"paper","paper_id":"P065","evidence_ids":["ev-p065-anchor-state-credit","ev-p065-state-recurrence-boundary"],"source_refs":[{"path":"papers/P065_gigpo.pdf","sha256":"f6a4d4559c41048be67a0e4a062f9957996fc79e6a80f65fe66f1140fac82dcd"}]} -->
# Group-in-Group Policy Optimization for LLM Agent Training

## Role in the knowledge base
[CODEX_SYNTHESIS] 针对 trajectory-level uniform return 的 anchor-state 相对 credit 机制来源。

## Problem and setting
[AUTHOR_FACT] GiGPO 对完全相同 environment states 下出现的 actions 与 discounted returns 分组，而不是为该 state 新增 rollout。[[evidence:ev-p065-anchor-state-credit]]

## Changed computation
[CODEX_SYNTHESIS] 在 trajectory group 内利用自然发生的相同 state，计算该 anchor 下 action 的相对 advantage。

## Evidence-backed findings
[AUTHOR_FACT] ALFWorld 中 anchor grouping 的实用性依赖大量 state recurrence。[[evidence:ev-p065-state-recurrence-boundary]]

## Limitations and failure signals
[CODEX_SYNTHESIS] 不重复到完全相同 environment state 的开放式任务无法直接获得这一 credit。

## Lineage and baselines
[CODEX_SYNTHESIS] terminal-return broadcast → naturally recurring anchor-state relative credit。

## Evidence ledger
[CODEX_SYNTHESIS] changed computation 与 recurrence precondition 各有直接 Evidence。

## Retrieval vocabulary
[CODEX_SYNTHESIS] anchor state credit; grouped action advantage; repeated state; GiGPO; sparse terminal reward
