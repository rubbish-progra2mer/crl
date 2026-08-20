<!-- CRL_CARD_META {"schema_version":1,"card_id":"failure-token-local-credit-misses-turn-level-delayed-value","card_kind":"failure","paper_id":"P077","evidence_ids":["ev-p077-hierarchical-utterance-critic-token-actor","ev-p077-trajectory-only-sample-efficiency","ev-p077-oracle-reward-hacking-boundary"],"source_refs":[{"path":"papers/P077_archer.pdf","sha256":"9a25030a872732dc5fc544e04e3d20382be1d512eeefd97e7e92179dd2c5f8ec"}]} -->
# Token-Level On-Policy PPO Can Be Sample-Inefficient under Turn-Level Delayed Rewards

## Observed failure
[AUTHOR_FACT] 在 Twenty Questions 同数据量比较中，token-level PPO 不具竞争力，并需大量 on-policy rollouts 才稳定改善。[[evidence:ev-p077-trajectory-only-sample-efficiency]]

## Conditions and scope
[CODEX_SYNTHESIS] 适用于 reward 延迟到多轮结果、utterance 是有意义 action 单位的语言交互；不是所有 token RL 的全局否定。

## Failed intervention
[CODEX_SYNTHESIS] 直接使用 token-level on-policy PPO 没有在同样 data regime 下解决论文所述高 variance 与 sample reuse 问题；比较同时改变 credit granularity、off-policy replay、critic 粒度及其他 actor-critic computation，不能把全部差异唯一归因于 utterance-level credit。

## Evidence and alternative explanations
[AUTHOR_FACT] ArCHer 以 utterance-level TD critic 和 token-level policy 分离 credit。[[evidence:ev-p077-hierarchical-utterance-critic-token-actor]]

## Warning for future candidates
[AUTHOR_FACT] 环境含模拟 oracle 与 reward-hacking patch。[[evidence:ev-p077-oracle-reward-hacking-boundary]] [CODEX_SYNTHESIS] 未来实验不得把 trajectory threshold 等同 wall-clock/token efficiency，且本方向受项目排除边界限制。

## Possible repair boundary
[CODEX_HYPOTHESIS] 若研究边界允许，可将 critic 时间粒度对齐 utterance；本项目只保留为 baseline，不主动展开该排除方向。

## Evidence ledger
[CODEX_SYNTHESIS] observed failure、changed computation 与 confound 分别绑定 Evidence。

## Retrieval vocabulary
[CODEX_SYNTHESIS] delayed turn credit; token PPO variance; utterance action value; multi-turn RL failure; simulated oracle confound
