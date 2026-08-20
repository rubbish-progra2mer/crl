# v050 研究地图

## 共享知识库证据

- P100 *How Many Tools Should an LLM Agent See? A Chance-Corrected Answer* 已把候选工具数量从固定超参数变为逐查询停止决策，以机会校正奖励在覆盖和干扰之间施加内生深度压力；其公开边界包括多工具目标与执行正确性。
  - https://arxiv.org/abs/2605.24660
- P085 TOOLRET 显示 43,215 个工具规模下，现有检索器的完整集合恢复率很低，说明多目标工具集合恢复是独立瓶颈，但标签可能遗漏可替代工具。
- P048 NaviAgent 已用接口及参数依赖图把高层交互模式与动态工具链构造分开。
- P088 非负弹性网解码已经通过联合稀疏残差而非独立相似度选择互补集合。

## 最新直接先行工作

- *Dynamic Tool Dependency Retrieval for Lightweight Function Calling* 直接以初始查询和逐步展开的调用计划为条件，从示例中建模工具依赖并动态检索；这覆盖“随计划补齐依赖工具”的核心计算。
  - https://aclanthology.org/2026.findings-acl.1680/
- *Beyond Single-Shot: Multi-step Tool Retrieval via Query Planning* 把大规模动态工具库检索改写为迭代查询规划，以子任务查询桥接组合需求与工具文档。
  - https://aclanthology.org/2026.findings-acl/
- ToolReAGt 已针对多工具查询做子任务级检索和层级重排；NaviAgent 则覆盖图条件工具链构造。
  - https://openreview.net/forum?id=LTeBIM1rJL

## 差分审计

候选的“依赖补齐”被动态工具依赖检索和图驱动工具链直接覆盖，“自适应停止”被 P100 覆盖，“联合互补集合”又被 P088 覆盖。把三者串联没有改变任何组件的计算语义，只是模块组合。

## 结论

v050 不注册正式假设。多工具完整集合恢复是真实开放面，但当前草案没有独立方法内核。
