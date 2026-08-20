# v075 研究图谱

## 事务副作用与清理

- *Atomix* 处理推测分支、并发竞争和崩溃恢复中的工具副作用；不可缓冲的外部效果被跟踪，并在中止时通过清理处理器补偿。
  - https://openreview.net/attachment?id=UeRbEpSVUz&name=pdf
- *Verified Tool Calls Improve LLM Agent Reliability Under Non-Atomic Failures* 已用后置条件核验、重试前核验和幂等键处理超时后派发、延迟可见与部分状态更新，减少重复和不必要调用。
  - https://arxiv.org/abs/2608.02645

## 智能体生命周期清理

- *EffGen* 的子智能体生命周期包含完成/失败后的 `cleanup()`，明确释放临时工具资源、递减模型引用并回收临时上下文。
  - https://openreview.net/attachment?id=WUBn9uJuvj&name=originally_submitted_PDF
- *AIOS* 将智能体资源管理和隔离提升为智能体操作系统内核职责。
  - https://arxiv.org/abs/2403.16971

## 工作流与状态评价

- *Agent-Diff* 使用状态差分和闭世界不变量检测预期状态之外的修改，因此未清理的持久资源可直接作为意外副作用。
  - https://openreview.net/pdf?id=IIyIrKwKFV
- 当前 Run v034 已覆盖事务/补偿和幂等语义，v052 已覆盖异步生命周期，v065 已扫描资源、并行取消与生产运行时。

## 结论

把临时资源列成 `cleanup_obligations`、完成前逐项释放或在中止时执行补偿，分别落入现有生命周期管理、Saga/事务清理和闭世界状态验证。没有新的计算差分，不注册实验。
