# P024 Reconciliation

- Disposition：`ACCEPT_WITH_NARROWING`
- Read 1 SHA-256：`fd8c6162e93ccc16f03918516b23654bce9412775044bef41ba9d168da634fa3`
- Accepted read-2：`read_2_attempts/r2-20260719-p024-a1/`
- Invocation SHA-256：`b64416d9c4541b2f9634edc539d58e980e50aaf73a992e3db9c59e20d9dda952`
- Report SHA-256：`35cf7c897e7f19ddbff927dc25050a584b0688a5a52d64f4e2343803fd782005`
- 其他 attempts：无。

## Source reconciliation

- `AGREE`：同质模型副本先独立回答，再读取其他回答迭代修订，末轮多数汇总；这是 peer-answer exposure，不是独立证据 Reviewer（§2，pp.2–4）。
- `AGREE`：主要设置优于 single/reflection/majority，但 debate 的生成 token 常为 single 的约 5–8 倍，且 consensus 可因 agreeability 收敛到共同错误（主表、Table A9 与案例）。
- `RESOLVED_BY_SOURCE`：Operator 命名为 `Cross-Trajectory Peer Critique Update`；Failure 为 `Consensus Without Independent Evidence`。不得把 consensus 当事实支撑或把旧任务结果直接外推到工具型长轨迹。

## Frozen source role

作为 multi-agent debate 直接祖先、majority/成本基线及公正独立 Reviewer 的反面边界准入。
