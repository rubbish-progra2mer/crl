<!-- CRL_CARD_META {"schema_version":1,"card_id":"failure-anchor-state-credit-needs-state-recurrence","card_kind":"failure","paper_id":"P065","evidence_ids":["ev-p065-anchor-state-credit","ev-p065-state-recurrence-boundary"],"source_refs":[{"path":"papers/P065_gigpo.pdf","sha256":"f6a4d4559c41048be67a0e4a062f9957996fc79e6a80f65fe66f1140fac82dcd"}]} -->
# Anchor-State Credit Loses Coverage Without Repeated States

## Observed failure
[AUTHOR_FACT] P065 所报告 anchor grouping 的可用性依赖 ALFWorld 中大量 state recurrence。[[evidence:ev-p065-state-recurrence-boundary]]

## Conditions and scope
[CODEX_SYNTHESIS] 这是 coverage precondition，不说明 GiGPO 在 ALFWorld 中失败。

## Failed intervention
[CODEX_SYNTHESIS] 只利用 rollout 中自然出现的 identical states；不新增 state-conditioned rollout。[[evidence:ev-p065-anchor-state-credit]]

## Evidence and alternative explanations
[CODEX_SYNTHESIS] 开放文本状态可能语义相似但字符串不同，也可能错误合并；两类都会改变 group coverage。

## Warning for future candidates
[CODEX_SYNTHESIS] 迁移前必须量化 state recurrence、canonicalization error 与可获得 action comparisons。

## Possible repair boundary
[CODEX_HYPOTHESIS] state abstraction 可能增加 coverage，但会引入错误等价的新风险。

## Evidence ledger
[CODEX_SYNTHESIS] grouping rule 与 recurrence boundary 各有 Evidence。

## Retrieval vocabulary
[CODEX_SYNTHESIS] anchor state coverage; state recurrence; local credit sparsity; state canonicalization
