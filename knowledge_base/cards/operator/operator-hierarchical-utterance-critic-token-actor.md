<!-- CRL_CARD_META {"schema_version":1,"card_id":"operator-hierarchical-utterance-critic-token-actor","card_kind":"operator","paper_id":"P077","evidence_ids":["ev-p077-hierarchical-utterance-critic-token-actor","ev-p077-trajectory-only-sample-efficiency","ev-p077-oracle-reward-hacking-boundary"],"source_refs":[{"path":"papers/P077_archer.pdf","sha256":"9a25030a872732dc5fc544e04e3d20382be1d512eeefd97e7e92179dd2c5f8ec"}]} -->
# Hierarchical Utterance Critic with Token-Level Actor

## Intervention target
[CODEX_SYNTHESIS] 多轮语言交互中 delayed task reward 到 utterance decision 与 token generation 的 credit interface。

## Before and after computation
[CODEX_SYNTHESIS] 单一 token-level return/critic → utterance-level TD critic 估值整段 action，并由 token-level policy gradient 更新生成策略。[[evidence:ev-p077-hierarchical-utterance-critic-token-actor]]

## Inputs outputs information and timing
[CODEX_SYNTHESIS] 输入是多轮 state 与完整 utterance action；critic 在 turn 边界估值，actor 在 token 生成层更新。

## Mechanism hypothesis
[CODEX_HYPOTHESIS] 若失败来自 turn-level delayed value 被 token-local variance 淹没，层级 critic 应先改善 trajectory efficiency；来源在特定 Twenty Questions 阈值报告此信号。[[evidence:ev-p077-trajectory-only-sample-efficiency]]

## Predicted observable signature
[CODEX_HYPOTHESIS] 在相同 trajectories 下 critic error 与 return 应更稳定改善，而非仅增加 rollout 数。

## Preconditions and transfer risks
[AUTHOR_FACT] 对话任务采用模拟 oracle，且出现过需要硬编码修补的 reward hacking。[[evidence:ev-p077-oracle-reward-hacking-boundary]] [CODEX_SYNTHESIS] 受项目研究排除项约束，本算子只作为 lineage/baseline，不主动导出环境反馈学习 Candidate。

## Source lineage
[CODEX_SYNTHESIS] 从 P077 原样抽象；与 token-level PPO、filtered BC 和 CHAI 的区别必须回到原论文比较。

## Evidence ledger
[CODEX_SYNTHESIS] changed computation、特定 signature 与环境边界均有 Evidence。

## Retrieval vocabulary
[CODEX_SYNTHESIS] utterance-level critic; token-level actor; hierarchical credit assignment; multi-turn delayed reward; dialogue RL baseline
