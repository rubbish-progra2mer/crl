<!-- CRL_CARD_META {"schema_version":1,"card_id":"paper-reflexion","card_kind":"paper","paper_id":"P012","evidence_ids":["ev-p012-verbal-reflection-memory","ev-p012-forced-retry-harmful-edits"],"source_refs":[{"path":"papers/P012_reflexion.pdf","sha256":"efba04cd48b779131fc4c3c58ae49e8523ded534f9225a7c57c7bdad0823803d"}]} -->
# Reflexion

## Role in the knowledge base
[CODEX_SYNTHESIS] Reflection、verbal learning 与 episodic memory 的直接祖先；同时保留 grounded feedback 和 harmful retry 边界。

## Problem and setting
[CODEX_SYNTHESIS] Agent 在多次 trial 间利用环境、测试或 heuristic feedback 改进决策，不更新模型权重。

## Changed computation
[AUTHOR_FACT] 把对 task feedback 的 verbal reflection 写入 episodic memory，供后续 trial 条件化。[[evidence:ev-p012-verbal-reflection-memory]]

## Evidence-backed findings
[AUTHOR_FACT] 固定继续迭代且不能提前返回时，Agent 会对实现作 harmful edits。[[evidence:ev-p012-forced-retry-harmful-edits]]

## Limitations and failure signals
[CODEX_SYNTHESIS] 依赖 feedback 的可判别性、额外 trials 与 context；不应与无反馈 intrinsic self-correction 混同。

## Lineage and baselines
[CODEX_SYNTHESIS] ReAct retry/EPM 是关键相邻 baseline。

## Evidence ledger
[AUTHOR_FACT] p.1 支持 verbal memory；p.8 支持 forced retry 的 harm。[[evidence:ev-p012-verbal-reflection-memory]] [[evidence:ev-p012-forced-retry-harmful-edits]]

## Retrieval vocabulary
[CODEX_SYNTHESIS] Reflexion；verbal reinforcement learning；episodic reflection memory；retry；语言反思记忆。
