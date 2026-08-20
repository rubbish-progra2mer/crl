# P028 Reconciliation

- Disposition：`ACCEPTED_WITH_NARROWING`
- Read 1 SHA-256：`092c7d3c17e6e21f53126c0d9b57faabde65d8b9a4b773835915df308648d5ad`
- Accepted read-2 attempt：`read_2_attempts/r2-20260719-p028-a1/`
- Read-2 invocation SHA-256：`758f609674d02f5a697fcdb5409e38be29faa73f3c689449859d248fa51316c0`
- Read-2 report SHA-256：`cd39b45e17d310d876709b77c856b04f0e7e3c22bf316f3124e76b2cacc0c485`
- Accepted read-3 attempt：`read_3_attempts/r3-20260719-p028-a1/`
- Read-3 invocation SHA-256：`454e8252af4aff756a5995ef1c4d59ce227379a98ddbce8ca38e0f67df11cc3f`
- Read-3 report SHA-256：`4cd5a7507a3464884a5a8b480d631d3cab5f23f2de31ee98a1660258284adc62`

## Source reconciliation

- `AGREE`：Memory Manager 以 downstream exact-match reward 学习 ADD/UPDATE/DELETE/NOOP，Answer Agent 从候选 memories 学证据选择与作答；changed computation 是两阶段学习式 memory control，而不是普通 retrieval 扩容。
- `AGREE`：LoCoMo question 级 `152/81/1307` 划分在三读中得到明确原文支持。
- `UNRESOLVED_NONBLOCKING`：同一训练说明同时出现 preceding 24 turns 与 previous 50 turns；主文约 600 turns/26k tokens 与附录平均约 300 turns/9k tokens 也没有可核验的口径映射。
- `RESOLVED_BY_SOURCE`：作者官方仓库 `yansikuan/memory-r1` 的 main commit `9c413a2413c4fee160ec05445856c1529d63ac7a` 明确标记 `Code coming soon`，没有训练配置可用于消歧；因此冲突必须保留，不能按便利性选择一个数字。
- `AGREE`：RL 并非所有模型/指标都胜过 SFT，且训练使用 4–8 H100 与外部 GPT 模型资产；不能形成轻量、低成本或单组件 Claim。

## Admission boundary

24/50 turns 与两套对话规模不是本库采用的 Operator 定义所必需，因此定为非阻断来源冲突；正式 Evidence 与 Card 禁止引用这些精确数字。准入只支持学习式 CRUD memory control、两阶段 manager/answer computation及其数据/算力/外部模型边界；不得把参数冲突改写为性能 Failure，也不得宣称完整可复现。

## External source record

- Official repository：`https://github.com/yansikuan/memory-r1`
- Frozen commit identity：`9c413a2413c4fee160ec05445856c1529d63ac7a`
- Repository status at cutoff：`Code coming soon`

