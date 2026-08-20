<!-- CRL_CARD_META {"schema_version":1,"card_id":"operator-transition-decomposed-agent-training","card_kind":"operator","paper_id":"P026","evidence_ids":["ev-p026-transition-decomposition","ev-p026-uniform-terminal-return"],"source_refs":[{"path":"papers/P026_agent_lightning.pdf","sha256":"e223648a09b021785a46f60dd5ce13301622eca930ff91a5b45e971b53422561"}]} -->
# Transition-Decomposed Training for Existing Agents

## Intervention target
[CODEX_SYNTHESIS] Agent 运行轨迹中的 policy-LLM 调用边界；不改原 Agent 的工具与控制代码。

## Before and after computation
[CODEX_SYNTHESIS] monolithic agent episode → per-call input/output/reward transitions。[[evidence:ev-p026-transition-decomposition]]

## Inputs outputs information and timing
[CODEX_SYNTHESIS] 输入为调用上下文，输出为模型 response；训练发生在已收集轨迹上，当前 reward 仍来自终局广播。

## Mechanism hypothesis
[CODEX_HYPOTHESIS] 显式 transition 接口允许在不重写 Agent 的情况下替换学习算法。

## Predicted observable signature
[CODEX_HYPOTHESIS] 同一 Agent implementation 可接入训练；但没有额外 credit 机制时，各 step 的 advantage 不会分化。

## Preconditions and transfer risks
[AUTHOR_FACT] 当前实现把同一 final return 分配给 episode 内所有 actions。[[evidence:ev-p026-uniform-terminal-return]]

## Source lineage
[CODEX_SYNTHESIS] P026 原样抽象；P065 是其 uniform-return 的 refinement，不是独立同义机制。

## Evidence ledger
[CODEX_SYNTHESIS] transition 与 reward 边界分别对应两条 Evidence。

## Retrieval vocabulary
[CODEX_SYNTHESIS] agent training decoupling; policy call transition; monolithic agent RL; terminal return broadcast
