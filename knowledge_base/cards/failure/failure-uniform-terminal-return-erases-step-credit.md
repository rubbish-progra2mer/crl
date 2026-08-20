<!-- CRL_CARD_META {"schema_version":1,"card_id":"failure-uniform-terminal-return-erases-step-credit","card_kind":"failure","paper_id":"P026","evidence_ids":["ev-p026-transition-decomposition","ev-p026-uniform-terminal-return"],"source_refs":[{"path":"papers/P026_agent_lightning.pdf","sha256":"e223648a09b021785a46f60dd5ce13301622eca930ff91a5b45e971b53422561"}]} -->
# Uniform Terminal Return Does Not Identify Decisive Agent Steps

## Observed failure
[AUTHOR_FACT] P026 当前实现把 final return 均匀广播给 episode 内每个 action。[[evidence:ev-p026-uniform-terminal-return]]

## Conditions and scope
[CODEX_SYNTHESIS] 仅绑定该实现的 per-call transition training，不宣称所有 terminal-reward RL 都无效。

## Failed intervention
[CODEX_SYNTHESIS] 虽已把 LLM calls 分成 transitions，但 reward 没有进一步区分各调用的局部作用。[[evidence:ev-p026-transition-decomposition]]

## Evidence and alternative explanations
[CODEX_SYNTHESIS] uniform label 直接造成 credit 不可辨识；系统仍可能靠整体 policy update 获益。

## Warning for future candidates
[CODEX_SYNTHESIS] 不得把 transition decomposition 本身写成细粒度 credit assignment；需报告 decisive-step signal。

## Possible repair boundary
[CODEX_HYPOTHESIS] 只有使用非 Oracle 的局部比较或结构信号时，才可能区分 step credit。

## Evidence ledger
[CODEX_SYNTHESIS] transition granularity 与 reward granularity 由两条 Evidence 分别约束。

## Retrieval vocabulary
[CODEX_SYNTHESIS] uniform terminal reward; credit smearing; sparse trajectory reward; step credit ambiguity
