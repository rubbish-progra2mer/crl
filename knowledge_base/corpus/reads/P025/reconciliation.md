# P025 Reconciliation

- Disposition：`ACCEPT_WITH_NARROWING`
- Read 1 SHA-256：`6f0f6bd273e1ab9ce8468f04cc1d0a9077f05bcf0d2d425a1acf36b77eb03a10`
- Accepted read-2：`read_2_attempts/r2-20260719-p025-a1/`
- Invocation SHA-256：`a0c247e43fdcd36f5bee67518e7171996a66ea975cd630c80f7eb49c665d27ab`
- Report SHA-256：`37648d2a5db783165b6c993255a14f46f119cb2f5941de5627b8cfb244f4bd33`
- 其他 attempts：无。

## Source reconciliation

- `AGREE`：复合方法同时移除 `1/T` 轮数归一化、增加反事实 influence reward 与 restart reward；主结果不能归因于单一组件。
- `AGREE`：ReMA 可低于单 Agent GRPO，process reward 也未阻止 collapse；这是 nominal multi-agent 退化为 effective single-agent 的强 Failure 证据。
- `RESOLVED_BY_SOURCE`：正式 Operator 只保留 grouped masked-history one-step influence 与 length-debiased step credit；restart 明确为复合训练组成，不升级为独立机制。论文没有做 role removal 后的 terminal-outcome counterfactual，因此不得表述成 role-level contribution audit。

## Frozen source role

准入为 multi-agent role-collapse、credit/length bias 与过程分数失效来源；训练需 128 rollouts、GPT-4o 噪声和 SFT cold start，不能作为个人本机轻量 implement 证据。

## PLAN_05 Card source-audit disposition

- Audit: `plan05-audit-a/report.md`；SHA-256 `64f4c12681fc74c47cbae98e24f2501c92e3e8f1bb978edcfafc20dbd2f247e9`；task `/root/plan05_card_source_audit_a`
- Card SHA-256: pre `d5871a1f347bb1554461ac9176b8997c3faa85953b59d65a591e92a06d0ff180` (`operator-counterfactual-role-contribution-audit`) → post `9ed2b7449b3dfd7c73747c927f91e3d1dc2cabb13c35105ad6f42aed8a37181b` (`operator-grouped-masked-history-step-credit`)
- Disposition: `REPLACED_WITH_SOURCE-FAITHFUL_OPERATOR`

旧 Card intervention identity 不成立，已删除并以 step/turn 粒度 Card 取代；新增第 6 页方法 Evidence，Failure Evidence 只保留为动机。
