<!-- CRL_CARD_META {"schema_version":1,"card_id":"operator-capability-preserving-agent-safety-evaluation","card_kind":"operator","paper_id":"P067","evidence_ids":["ev-p067-capability-preserving-safety","ev-p067-agentic-harm-not-chat-refusal"],"source_refs":[{"path":"papers/P067_agentharm.pdf","sha256":"1f3bbfa41e9e8d0c1218fba19af5a7b9cffc04a1d9fba8b739ce57b080489560"}]} -->
# Capability-Preserving Agent Safety Evaluation

## Intervention target
[CODEX_SYNTHESIS] safety evaluator 对完整工具轨迹的测量对象，不改变 Agent 本身。

## Before and after computation
[CODEX_SYNTHESIS] chatbot refusal score → jointly measure harmful multi-step success and retained benign capability。[[evidence:ev-p067-capability-preserving-safety]]

## Inputs outputs information and timing
[CODEX_SYNTHESIS] 输入为任务与 tool-use trajectory；输出为 harmful/benign capability measures；在离线评价时发生。

## Mechanism hypothesis
[CODEX_HYPOTHESIS] 分离拒答与执行能力可发现表面安全但仍可完成有害工具链的 Agent。

## Predicted observable signature
[CODEX_HYPOTHESIS] refusal 相近的系统仍可能在 agentic harmful success 上分离，同时报告 benign capability。

## Preconditions and transfer risks
[CODEX_SYNTHESIS] 依赖安全 sandbox 与任务覆盖；不能从聊天数据直接外推。

## Source lineage
[CODEX_SYNTHESIS] refusal evaluation → AgentHarm trajectory capability evaluation。

## Evidence ledger
[AUTHOR_FACT] tool-use harm 可保留连贯能力。[[evidence:ev-p067-agentic-harm-not-chat-refusal]]

## Retrieval vocabulary
[CODEX_SYNTHESIS] capability-preserving safety; agentic harm; tool trajectory safety; refusal insufficiency
