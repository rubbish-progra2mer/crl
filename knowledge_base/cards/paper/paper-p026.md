<!-- CRL_CARD_META {"schema_version":1,"card_id":"paper-p026","card_kind":"paper","paper_id":"P026","evidence_ids":["ev-p026-transition-decomposition","ev-p026-uniform-terminal-return"],"source_refs":[{"path":"papers/P026_agent_lightning.pdf","sha256":"e223648a09b021785a46f60dd5ce13301622eca930ff91a5b45e971b53422561"}]} -->
# Agent Lightning: Train ANY AI Agents with Reinforcement Learning

## Role in the knowledge base
[CODEX_SYNTHESIS] Agent 轨迹解耦训练的机制来源，也是 GiGPO 所针对的 uniform-return 直接基线。

## Problem and setting
[AUTHOR_FACT] 方法把已有 Agent 的 policy-LLM 调用抽取为逐调用 transition。[[evidence:ev-p026-transition-decomposition]]

## Changed computation
[CODEX_SYNTHESIS] 训练侧从整段 Agent 实现中分离出可学习的 LLM 决策 transition；当前实现仍把终局 return 广播给全部动作。

## Evidence-backed findings
[AUTHOR_FACT] 抽取单位包含每次调用的输入、输出与 reward。[[evidence:ev-p026-transition-decomposition]]

## Limitations and failure signals
[AUTHOR_FACT] 当前 credit assignment 对同一 episode 内动作使用相同 terminal return。[[evidence:ev-p026-uniform-terminal-return]]

## Lineage and baselines
[CODEX_SYNTHESIS] 作为 P065 anchor-state credit 的直接前序；不能把训练框架解耦本身当成细粒度 credit 已解决。

## Evidence ledger
[CODEX_SYNTHESIS] transition 结构由 `ev-p026-transition-decomposition` 支撑；uniform return 边界由 `ev-p026-uniform-terminal-return` 支撑。

## Retrieval vocabulary
[CODEX_SYNTHESIS] agent RL decoupling; transition decomposition; terminal reward broadcast; agent credit assignment
