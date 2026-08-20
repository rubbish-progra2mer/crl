# v172 失败归因

## 类型

`INTERVENTION_RESPONSE_REPLICATION_CLOSED_BY_DIFFERENTIAL_METAMORPHIC_AND_ACTIVE_TESTING_PRIORS`

## 直接原因

- 相同干预下比较原始与候选科学软件的离名义响应，差分故障注入已直接实现；
- 从已有成功测试或规格关系派生新测试并比较响应，蜕变测试已覆盖；
- 在有限成本下选择最有信息的测试点或区分候选程序，主动测试、顺序诊断和主动程序测试已覆盖；
- 当前复现基准并非只看最终图：Replica、PaperBench、ReplicationBench 与 SciReplicate-Bench 已显式检查实现、过程或方法忠实度；新候选只是增加一类隐藏测试。

## 非原因

- 不是目标缺口不存在；PaperBench 23 份评分表的静态审计没有发现显式评分器生成的留出干预响应项；
- 不是该加固没有工程价值；它可能揭示名义结果相似但离名义行为不同的复现；
- 不是合成实验不可运行；是不运行人为植入差异后再检出的同义反复实验；
- 不是宿主安全控制、科研反证、Prior collision 之外的 Run 终局或用户终止。v029 仍仅是外部执行边界。

## 决定

不注册 Seed 或实验。v173 转向结构不同的 frontier，Run 保持 `ACTIVE`。
