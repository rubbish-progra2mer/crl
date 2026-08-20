# P035 Reconciliation

- Disposition：`ACCEPT_WITH_NARROWING`
- Read 1 SHA-256：`76ebd7016d2c376bb685feafa9f53876717611ed2977714f616ed7745044c67b`
- Accepted read-2：`read_2_attempts/r2-20260719-p035-a1/`
- Invocation SHA-256：`7a16c44d87401fd3d13bb9378c4ea831a9ef9a80e3702f255441e1535bd1b18c`
- Report SHA-256：`8d0f12a5a726626bc87a956a46007dddca870bcb217f0c0624e8c226f99b5786`
- 其他 attempts：无。

## Source reconciliation

- `AGREE`：耐久贡献是 model×scaffold×benchmark 对照、accuracy–cost Pareto 与 trace audit，不是 distributed leaderboard 工程。
- `AGREE`：21/36 组合更高 reasoning effort 持平/下降；TAU few-shot 泄漏导致整组结果作废，gold lookup/unsafe shortcut 可制造 invalid success。
- `RESOLVED_BY_SOURCE`：Docent flag 只验证被 flag 样本 precision，相关性不作因果；多数昂贵配置单次运行，具体排行榜随 provider 漂移。

## Frozen source role

以 `Trace-Audited Cost-and-Scaffold-Controlled Evaluation` 和 `Aggregate Agent Score Masks Invalid Success` 准入；禁止复制其 scheduler/dashboard/VM 平台。
