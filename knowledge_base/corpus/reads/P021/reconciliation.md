# P021 Reconciliation

- Disposition：`ACCEPT_WITH_NARROWING`
- Read 1：`read_1.md`，SHA-256 `687e7a2737bacb563fce3c67aba0e76363851e21a43b1f7b8d1c862e7a01f233`
- Accepted read-2 attempt：`read_2_attempts/r2-20260719-p021-a1/`
- Invocation SHA-256：`f61756463e2f7c06dbf21a6fc52e0e3835869d9639aa4354a88faa313ed32776`
- Report SHA-256：`3caca7edafedd284ae550527ded3d57299824aa7a3938f2b6f3b7869a3eda927`
- 其他 read-2 attempts：无；污染/失败 attempt：无。

## Source reconciliation

- `AGREE`：四模块 scaffold 只训练 Planner；最终轨迹奖励广播到各轮，核心变化是当前闭环状态上的 on-policy Planner 更新（§2–3，pp.3–6）。
- `AGREE`：Table 3 只支持同 scaffold 内 Flow-GRPO 优于 frozen/SFT；10 轮评测、外部 GPT-4o judge/embedding 与未等额 token/tool budget 阻止系统级归因（pp.7–10，附录实现）。
- `RESOLVED_BY_SOURCE`：正式 Operator 收窄为 `Outcome-Trained Planner over Explicit Execution State`；正式 Failure 同时保留 `Trajectory Reward Broadcast Masks Turn Contribution` 与离线 imitation collapse，不声称广播解决因果 credit。

## Frozen source role

可作为 Agent learning/planning Operator、轨迹级 credit Failure 与预算公平性来源。窄 Claim：在论文给定 scaffold、工具、任务和 outcome reward 下，Flow-GRPO Planner 优于 frozen 与 SFT Planner；不得外推成本优势或开放科研任务有效性。
