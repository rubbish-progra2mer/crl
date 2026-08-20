# v068 假设组合

本版本没有注册实验假设。

- 非重置环境的未来任务可达性：`CLASSICAL_AND_DIRECT_PRIOR_COLLISION`；经典副作用正则化已把未来任务纳入当前决策。
- 路径依赖的跨任务干扰：`DIRECT_PRIOR_COLLISION`；PATH-Bench 已以帮助/干扰历史测迁移与遗忘。
- 长期累积后果：`DIRECT_PRIOR_COLLISION`；MerchantBench 已在持久环境中测动作约束未来选择及累积结果。
- 状态差分副作用审计：`DIRECT_PRIOR_COLLISION`；Agent-Diff 已使用闭世界状态不变量识别意外副作用。

没有运行本地实验；复现这些现象不会恢复论文级贡献差分。
