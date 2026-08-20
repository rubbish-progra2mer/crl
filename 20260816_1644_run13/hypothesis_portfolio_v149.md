# v149 假设组合

| 草案 | 判定 |
|---|---|
| 五节点图诊断后回滚 | `STATE_MACHINE_AND_FAILURE_ATTRIBUTION_COLLISION`；且没有无图同预算基线识别图贡献 |
| 从外部可疑起点向前回看并以连续对齐段停止 | `EXTERNAL_ONSET_AND_MONOTONIC_DRIFT_ASSUMPTION`；未解决起点检测，也未验证交错漂移 |
| 用文档判断写操作可逆性 | `TOOL_CONTRACT_AND_REVERSIBILITY_COLLISION`；目标只由通用裁判评分，未执行或核验逆操作 |
| 用环境回放奖励恢复决定 | `EXECUTION_GROUNDED_REPAIR_COLLISION`；MARS 已在可重放失败轨迹上搜索并消融修复 |
| 自动执行逆操作后恢复任务 | `TRANSACTION_COMPENSATION_COLLISION`；效果账本、语义事务、补偿和后置条件已直接覆盖 |
| 用小模型共享五种恢复角色 | 窄任务多任务微调与模式奖励，能降低部署成本但没有新的恢复状态或动作 |

无假设达到最小可验证 Claim 或安全本地实验门槛。
