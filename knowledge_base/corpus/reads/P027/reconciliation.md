# P027 Reconciliation

- Disposition：`ACCEPT_WITH_NARROWING`
- Read 1 SHA-256：`54a48988b1a3d4cecc8c334798627d4d5694d3ff68a2de5d1f658457cb26312e`
- Accepted read-2：`read_2_attempts/r2-20260719-p027-a1/`
- Invocation SHA-256：`b46abf2e2c4770fddd34f027cf0fd4ba116b97fb1850a8e5658045e11c874e17`
- Report SHA-256：`21a7a8ff2397d5fce62fd10486d223e8ecdd1bc2f0fd00d9b9bea80ee5eaf5a9`
- 其他 attempts：无。

## Source reconciliation

- `AGREE`：强 expert 提议替代动作、PRM 预筛，当前 policy 从替代点续跑；只有 gold outcome 翻转才形成局部 DPO pair（§3，pp.3–6）。
- `AGREE`：去 PRM 结果接近完整方法但产生更多 pairs，说明 PRM 主要是选择效率；gold verifier 与强 teacher 才是不可省略的信息优势。
- `RESOLVED_BY_SOURCE`：Operator 为 `Verified Single-Branch Counterfactual Repair`，但“verified”只表示该状态/该后续 rollout 的终局成功，不证明原动作是唯一因果点。Failure 保留 whole-trajectory negative contamination 与 same-source expert/critic blind spot。

## Frozen source role

准入为 agent-learning 数据构造机制与 oracle/cost 边界；不支持无监督自我改进或开放科研任务直接迁移。
