# v097 假设组合

本版本没有注册实验假设。

- “何时停止轮询并等待固定时间”：`DIRECT_WAITING_POLICY_COLLISION`。
- “把单轮置信聚合为轨迹置信”：`DIRECT_TRAJECTORY_UQ_COLLISION`。
- “对多轮工具轨迹做轮间和轮内稠密信用分配”：`DIRECT_CREST_COLLISION`。
- “通过耦合策略轨迹共享昂贵反馈”：`DIRECT_TREE_COUPLED_AB_COLLISION`。

等待标签、轨迹置信汇总器、分段奖励或共享回放均只是这些直接工作的实现变体。
