# P036 Reconciliation

- Disposition：`ACCEPT_WITH_NARROWING`
- Read 1 SHA-256：`a94fb856d4a44d2938181c90628ca81a6bc2fe972e6345e165e5f50d8808bf30`
- Accepted read-2：`read_2_attempts/r2-20260719-p036-a1/`
- Invocation SHA-256：`0579c3364f1e03dc07dfb3c09dd819630e0f7a91dfa46bd25fe400bdc3d1829b`
- Report SHA-256：`dedf32a3130c695dc0874a0481adca2e9d119a4d4995358cc8dd47c59ced5302`
- 其他 attempts：无。

## Source reconciliation

- `AGREE`：97 tasks 将文档检索、政策推理、工具发现与数据库状态变化联合；gold/no-KB/full-context 三角消融分解 access 与 use。
- `AGREE`：非 gold 最佳 pass^1 25.52%，gold 最佳 39.69%，说明检索不是唯一瓶颈；Terminal 增益伴随更多搜索与时延。
- `RESOLVED_BY_SOURCE`：tool discovery 可作 evaluation/safety mechanism，但不是新 Agent retrieval Operator；gold 仅为分析 oracle，simulator 仍有 4/194 task-critical errors。

## Frozen source role

以 `Retrieved Knowledge Without Action Integration` Failure 和 `Gold-Access Knowledge-Use Decomposition` evaluation Operator 准入；不宣称 terminal search 普遍最优。
