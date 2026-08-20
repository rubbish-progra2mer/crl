# P022 Reconciliation

- Disposition：`ACCEPT_WITH_NARROWING`
- Read 1 SHA-256：`00cbe9408835dc52eda2b4027c42b8313d78b543db049cffdb18e0f862dfc134`
- Accepted read-2：`read_2_attempts/r2-20260719-p022-a1/`
- Invocation SHA-256：`ef37afafc1838377590f39d9c31d553de84d93c2b61ce4cafddaee2ff3e3dcd3`
- Report SHA-256：`0c58c89caa31d549ec6d8603a696f326d9f08b5e931b486a7133fb54d700bc71`
- 其他 attempts：无。

## Source reconciliation

- `AGREE`：目标 Agent 接收按最短拓扑距离分组、由远到近的多跳祖先消息，超预算时由 9B distiller 做语义—拓扑合并（§4，pp.3–6）。
- `AGREE`：K=2 最稳，K=3 在密图不稳定；target-agent token 下降不含 compression token，distillation 主导约 80 秒/样本开销（§5 与附录表）。
- `RESOLVED_BY_SOURCE`：Operator 为 `Source-Preserving Higher-Order Message Exposure`，但“source-preserving”只指合并前保留来源/顺序，不能保证合并后逻辑或少数证据不丢失。Failure 优先记录 hidden consolidation cost 与 receptive-field saturation。

## Frozen source role

准入为 multi-agent information-flow Operator、成本/密图负向证据。不得称系统总 token/延迟更低，也不得声称更高 K 普遍更强。
