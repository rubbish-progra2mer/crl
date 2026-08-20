# PLAN_05 Card 来源审计 H 主 Codex 处置

## 结论

`ACCEPT_AFTER_REVISION`

主 Codex 接受独立审计的 4 个 PASS 与 9 个 REVISE，不以 Card 已通过机械 schema 校验替代科研核源。

## 已执行修正

- P077 Failure 不再把 PPO–ArCHer 差异唯一归因于 token-local credit；标题限定为 turn-level delayed reward 下 token-level on-policy PPO 的 sample inefficiency，并披露 replay/critic/algorithm confounds。
- P078 Operator/Failure 明确 originating-instance validation、不稳定基线与未隔离 distractor 因果；新增两条原文 Evidence，保存约 USD 2,500 离线建库成本、TabMWP 的 BM25 反例与 CREATOR comparison 删除 correction loop。
- P079 Operator 改为 `Next-Action-Supervised` 标题；Failure 将 raw-observation overload 降为 hypothesis，并把 unseen affordance 漏元素、planning/fidelity/每步额外调用与 teacher/judge 边界写清。
- P080 Operator 补充 0–4 searches、`t_c` 表述歧义与未计 intermediate-answer/PPO/retrieval 的 net-cost 边界。
- P081 Failure 将 interactive-collapse 改为 hypothesis，并明确 matched independent sampling 只是必要对照而非充分因果证明。
- P082 Operator 精确到 `<API>` token 进入 top-10 时允许触发，补外部工具系统与高调用率预算边界，并把“直接祖先”降为“早期代表性方法”。

## 最终机械事实

- Evidence：169 条；SHA-256 `3bef3d940ebed18f8bebaf65bcc960c3ac8eebb5ba9b7649dfef109ef488f257`。
- Cards：179 张，Paper=81、Operator=50、Failure=48。
- 全量 Card validate 对 81-paper scratch SQLite：PASS。

以上修正只提升来源忠实性与下游科研约束，没有扩展 corpus、引入新模块或启动 Candidate/Commissioning。
