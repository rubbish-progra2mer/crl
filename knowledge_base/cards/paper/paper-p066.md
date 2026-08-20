<!-- CRL_CARD_META {"schema_version":1,"card_id":"paper-p066","card_kind":"paper","paper_id":"P066","evidence_ids":["ev-p066-single-to-stateful-gap","ev-p066-multiturn-state-evaluation"],"source_refs":[{"path":"papers/P066_bfcl.pdf","sha256":"5248f4770823b2a73fd52e3b12339d94121ff1b359c45163c5a47168edab7a2f"}]} -->
# Berkeley Function Calling Leaderboard: From Tool Use to Agentic Evaluation

## Role in the knowledge base
[CODEX_SYNTHESIS] tool-use/stateful evaluation carrier，不作为新方法 Operator。

## Problem and setting
[AUTHOR_FACT] strong single-turn function calling 不足以建立 memory、stateful decision 与 long-horizon competence。[[evidence:ev-p066-single-to-stateful-gap]]

## Changed computation
[CODEX_SYNTHESIS] benchmark 从单次函数映射扩展到带缺参、缺函数和跨轮状态的执行评价。

## Evidence-backed findings
[AUTHOR_FACT] multi-turn suite 明确区分 missing parameter、missing function 与 long-context state handling。[[evidence:ev-p066-multiturn-state-evaluation]]

## Limitations and failure signals
[CODEX_SYNTHESIS] Web 子集受时间变化影响；单个 benchmark 的状态类型也不能穷尽真实 Agent 的全部长程能力。

## Lineage and baselines
[CODEX_SYNTHESIS] single-turn function call accuracy → stateful multi-turn tool-use evaluation。

## Evidence ledger
[CODEX_SYNTHESIS] 单轮外推边界与多轮分解均有 Evidence。

## Retrieval vocabulary
[CODEX_SYNTHESIS] BFCL; stateful tool use; multi-turn function calling; missing function; long-context state
