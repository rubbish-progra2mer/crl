<!-- CRL_CARD_META {"schema_version":1,"card_id":"failure-chatbot-refusal-does-not-establish-agent-safety","card_kind":"failure","paper_id":"P067","evidence_ids":["ev-p067-capability-preserving-safety","ev-p067-agentic-harm-not-chat-refusal"],"source_refs":[{"path":"papers/P067_agentharm.pdf","sha256":"1f3bbfa41e9e8d0c1218fba19af5a7b9cffc04a1d9fba8b739ce57b080489560"}]} -->
# Chatbot Refusal Does Not Establish Tool-Agent Safety

## Observed failure
[AUTHOR_FACT] 在 AgentHarm 所测模型、任务及 universal jailbreak/template 条件下，agentic misuse 仍可保持基本工具能力，因此 chatbot refusal alone 不足。[[evidence:ev-p067-agentic-harm-not-chat-refusal]]

## Conditions and scope
[CODEX_SYNTHESIS] 仅覆盖 AgentHarm 的所测模型、任务与 jailbreak 条件，并只讨论文本/工具 Agent 的安全评价；不保存或传播具体危害流程。

## Failed intervention
[CODEX_SYNTHESIS] 用首轮拒答或聊天安全分数替代完整 trajectory 的 harmful capability measurement。

## Evidence and alternative explanations
[AUTHOR_FACT] 安全干预还必须检查 benign capability 是否保留。[[evidence:ev-p067-capability-preserving-safety]]

## Warning for future candidates
[CODEX_SYNTHESIS] 安全收益不能来自让 Agent 普遍失能，也不能只在聊天形式下测量。

## Possible repair boundary
[CODEX_SYNTHESIS] capability-preserving trajectory evaluation 是测量修复，不是自动防御方案。

## Evidence ledger
[CODEX_SYNTHESIS] refusal insufficiency 与 capability preservation 各有 Evidence。

## Retrieval vocabulary
[CODEX_SYNTHESIS] refusal overclaim; agentic safety; harmful tool capability; benign capability preservation
