# v168 失败归因

## 类型

`IDLE_WINDOW_THOUGHT_GUARDING_CLOSED_BY_OBSERVATION_CONDITIONED_SPECULATIVE_PLANNING_AND_BELIEF_VERIFICATION_PRIORS`

## 直接原因

- Second Thought 自身已让预演与替代分支生成条件化下一步和触发条件；
- IdleSpec 已在未来观察不确定条件下生成空闲计划，并在观察返回后聚合；
- 推测执行已有预测—验证／纠正机制；
- SAVeR 已对中间信念做约束审计和最小修复；
- 因而观察守卫、矛盾过滤和按不确定性选分支均没有独立方法差分。

## 非原因

- 不是 Second Thought 没有效果；它有跨基准的回合与主线程解码收益；
- 不是已经观察到陈旧思考造成失败：本版未运行轨迹实验；
- 不是异步执行不可用、资源不足或安全控制；
- 不是 Run 终局或用户终止。

## 决定

不注册实验或 Seed。保存观察后有效率／冲突率作为空闲推理评价轴；v169 转向结构不同的 frontier，Run 保持 `ACTIVE`。
