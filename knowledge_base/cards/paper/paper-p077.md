<!-- CRL_CARD_META {"schema_version":1,"card_id":"paper-p077","card_kind":"paper","paper_id":"P077","evidence_ids":["ev-p077-hierarchical-utterance-critic-token-actor","ev-p077-trajectory-only-sample-efficiency","ev-p077-oracle-reward-hacking-boundary"],"source_refs":[{"path":"papers/P077_archer.pdf","sha256":"9a25030a872732dc5fc544e04e3d20382be1d512eeefd97e7e92179dd2c5f8ec"}]} -->
# ArCHer: Training Language Model Agents via Hierarchical Multi-Turn RL

## Role in the knowledge base
[CODEX_SYNTHESIS] 多轮语言 Agent credit assignment 的层级 RL 锚点；因本项目排除“环境反馈学习与执行恢复”，仅作机制谱系与受限基线，不作为默认研究入口。

## Problem and setting
[AUTHOR_FACT] 方法把多轮对话建模为 utterance-level high-level MDP 与 token-level low-level MDP，并用 utterance critic 配合 token policy。[[evidence:ev-p077-hierarchical-utterance-critic-token-actor]]

## Changed computation
[CODEX_SYNTHESIS] 将多轮 task value 的估计提升到 utterance 层，同时保留 token 层生成策略更新。

## Evidence-backed findings
[AUTHOR_FACT] 论文在 Twenty Questions 的特定回报阈值上报告少于 1K 与超过 100K trajectories 的差异。[[evidence:ev-p077-trajectory-only-sample-efficiency]]

## Limitations and failure signals
[AUTHOR_FACT] 部分环境使用 Flan 模拟 oracle；Guess My City 还需硬编码阻止 oracle 泄露答案后的 reward hacking。[[evidence:ev-p077-oracle-reward-hacking-boundary]]

## Lineage and baselines
[CODEX_SYNTHESIS] 可用于核对 turn-level delayed value 是否被 token-local credit 抹平；不得把特定 trajectory 阈值写成通用 token、时间或成本提升。

## Evidence ledger
[CODEX_SYNTHESIS] 层级计算、特定 sample-efficiency 结果与 oracle/reward-hacking 边界分别绑定三条 Evidence。

## Retrieval vocabulary
[CODEX_SYNTHESIS] hierarchical multi-turn RL; utterance critic; token actor; delayed dialogue reward; trajectory sample efficiency; simulated oracle reward hacking
