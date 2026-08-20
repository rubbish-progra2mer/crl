<!-- CRL_CARD_META {"schema_version":1,"card_id":"operator-unified-language-memory-action-policy","card_kind":"operator","paper_id":"P062","evidence_ids":["ev-p062-unified-memory-action-policy","ev-p062-broadcast-advantage"],"source_refs":[{"path":"papers/P062_agentic_memory_unified.pdf","sha256":"ba41464f84dbd8e0d0aeb1e6e0d7fd83b4086b2922579b88f7947448a8e1958f"}]} -->
# Unified Language-and-Memory Action Policy

## Intervention target
[CODEX_SYNTHESIS] 当前 task action 与 STM/LTM 操作的共同决策点。

## Before and after computation
[CODEX_SYNTHESIS] fixed external memory manager + language policy → one policy chooses language or memory operations。[[evidence:ev-p062-unified-memory-action-policy]]

## Inputs outputs information and timing
[CODEX_SYNTHESIS] 输入为 task state、STM、LTM；输出为 reasoning/action 或 memory operation；每个 step 前发生。训练时 task specification `T` 含 expected answer `A_q`，该 oracle 信息不得作为部署输入。[[evidence:ev-p062-unified-memory-action-policy]]

## Mechanism hypothesis
[CODEX_HYPOTHESIS] 让 task policy 拥有 memory write/read 决策权，可按当前目标改变记忆状态而非被固定检索支配。

## Predicted observable signature
[CODEX_HYPOTHESIS] 收益应伴随情境相关 memory actions；matched context/token 下仍优于固定 CRUD 策略。

## Preconditions and transfer risks
[AUTHOR_FACT] 当前 credit 仍把同一 trajectory advantage 广播到此前 steps。[[evidence:ev-p062-broadcast-advantage]]

## Source lineage
[CODEX_SYNTHESIS] learned memory CRUD control 的 refinement；与 P063 write-side evolution 不同，前者学习动作选择，后者生成链接并改写邻居。

## Evidence ledger
[CODEX_SYNTHESIS] unified action space 与 credit boundary 有直接 Evidence。

## Retrieval vocabulary
[CODEX_SYNTHESIS] unified memory policy; memory operation action; STM LTM control; learned memory management
