<!-- CRL_CARD_META {"schema_version":1,"card_id":"paper-p067","card_kind":"paper","paper_id":"P067","evidence_ids":["ev-p067-capability-preserving-safety","ev-p067-agentic-harm-not-chat-refusal"],"source_refs":[{"path":"papers/P067_agentharm.pdf","sha256":"1f3bbfa41e9e8d0c1218fba19af5a7b9cffc04a1d9fba8b739ce57b080489560"}]} -->
# AgentHarm

## Role in the knowledge base
[CODEX_SYNTHESIS] Agent safety 的 capability-preserving evaluation carrier，用于阻止把聊天拒答率偷换成工具 Agent 安全性。

## Problem and setting
[AUTHOR_FACT] 安全评价必须区分 refusal 与保留的 multi-step task capability。[[evidence:ev-p067-capability-preserving-safety]]

## Changed computation
[CODEX_SYNTHESIS] 评价从文本拒答转向完整 multi-step tool-use trajectory 的 harmful capability 与 benign capability。

## Evidence-backed findings
[AUTHOR_FACT] 在 AgentHarm 所测模型、任务及 universal jailbreak/template 条件下，agentic misuse 仍可保持基本工具调用能力；单纯 chatbot refusal 不能充分证明 Agent 安全。[[evidence:ev-p067-agentic-harm-not-chat-refusal]]

## Limitations and failure signals
[CODEX_SYNTHESIS] benchmark 覆盖的危害类别与工具 sandbox 限定了外推范围；本卡不保存可操作危害指令。

## Lineage and baselines
[CODEX_SYNTHESIS] chatbot refusal benchmark → capability-preserving agentic harm evaluation。

## Evidence ledger
[CODEX_SYNTHESIS] 两条 Evidence 分别约束评价目标与拒答外推失败。

## Retrieval vocabulary
[CODEX_SYNTHESIS] agentic safety; capability preservation; tool-use harm; refusal insufficiency; AgentHarm
