# v063 Recorded 结果 001

两个记录均为 `SUCCESS / RECORDED_NON_SUPPORTING`，stderr 为 0 字节，且没有执行表示性的回退工具。

| 模型 | 条件 | 配对正确 | 共享故障正确 | 本地故障正确 | 未调用 |
|---|---:|---:|---:|---:|---:|
| qwen2.5:7b | raw | 0/12 | 0/12 | 12/12 | 0/24 |
| qwen2.5:7b | principle | 0/12 | 0/12 | 12/12 | 0/24 |
| qwen2.5:7b | domain-card | 12/12 | 12/12 | 12/12 | 0/24 |
| qwen3:8b | raw | 2/12 | 3/12 | 11/12 | 10/24 |
| qwen3:8b | principle | 6/12 | 12/12 | 6/12 | 6/24 |
| qwen3:8b | domain-card | 12/12 | 12/12 | 12/12 | 0/24 |

- `fault-domain-routing-qwen2-5-7b-001`：输出 SHA-256 `0a112620566b2c688a7b3734f3dd67bddeb715be71c123c64b6f58ae45b00b20`；
- `fault-domain-routing-qwen3-8b-001`：输出 SHA-256 `be6e91344dc33dd1f5cc4fdeb684d9f9e0f2200d05d12a9969ffd18d613108c3`。

H-v063-1 形式满足预注册成功阈值，但卡片直接含最佳回退，故只记为“行为缺口初步支持”，必须通过修订 2 的去推荐语消融后才能解释机制。
