<!-- CRL_CARD_META {"schema_version":1,"card_id":"paper-p062","card_kind":"paper","paper_id":"P062","evidence_ids":["ev-p062-unified-memory-action-policy","ev-p062-broadcast-advantage"],"source_refs":[{"path":"papers/P062_agentic_memory_unified.pdf","sha256":"ba41464f84dbd8e0d0aeb1e6e0d7fd83b4086b2922579b88f7947448a8e1958f"}]} -->
# Agentic Memory: Learning Unified Long-Term and Short-Term Memory Management

## Role in the knowledge base
[CODEX_SYNTHESIS] 将语言动作与 STM/LTM 管理统一为单一 learned policy 的机制来源。

## Problem and setting
[AUTHOR_FACT] policy 同时观察 STM、LTM 与 task state，并在同一 action space 选择语言或 memory operation。[[evidence:ev-p062-unified-memory-action-policy]]

## Changed computation
[CODEX_SYNTHESIS] memory write/read/evict 不再是固定外围模块，而成为与 task action 联合决策的可学习动作。

## Evidence-backed findings
[AUTHOR_FACT] 尽管以逐步动作描述，同一个 trajectory-level advantage 监督此前 memory 与 reasoning steps。[[evidence:ev-p062-broadcast-advantage]]

## Limitations and failure signals
[AUTHOR_FACT] 训练时 task specification `T` 包含 expected answer `A_q`。[[evidence:ev-p062-unified-memory-action-policy]] [CODEX_SYNTHESIS] 该 training-only oracle boundary 不得迁移为部署输入；联合动作空间改变了控制权，但 credit 仍是终局广播，不能证明关键 memory step 被单独识别。

## Lineage and baselines
[CODEX_SYNTHESIS] fixed memory pipeline → learned CRUD controller → unified language-memory action policy。

## Evidence ledger
[CODEX_SYNTHESIS] 联合策略和 credit 边界分别由两条 Evidence 支撑。

## Retrieval vocabulary
[CODEX_SYNTHESIS] unified memory action policy; STM LTM coupling; learned memory operation; trajectory advantage broadcast
