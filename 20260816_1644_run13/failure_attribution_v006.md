# v006 失败归因

## 失败类型

`PRIOR_WORK_COLLISION`

## 直接原因

候选的核心计算是合法工具结果反事实干预与后缀重放；Counterfactual Sensitivity 已覆盖敏感度目标，Causal Agent Replay 已覆盖智能体轨迹干预重放，SAVER 已覆盖动作提交前审计与修复。

## 后续路由

不把工具响应模式约束或一次额外调用包装成方法差分；继续寻找改变执行语义、状态更新或信息获取策略的正交机制。
