# v154 失败归因

## 类型

`IDLE_WINDOW_CREDIT_AND_INSTRUCTION_SURFACE_FRONTIERS_CLOSED_BY_RUN_MEMORY_DISCLOSED_LIMITS_AND_CLASSICAL_OPERATORS`

## 直接原因

- Second Thought 观察守卫是 v106/v131 的精确负记忆重复；
- CrEST 只证明逐词元标量符号保留，目标论文已明确承认聚合梯度、驻点与全局上限不受保证；
- 聚合梯度投影和跨轮延迟信用分别落入经典梯度手术与因果信用分配；
- Harness-IF 的目标模型有／无规则配对能改进测量解释，但属于标准因果消融；
- 当前可做的本地反例或小模型提示实验不会改变方法归属。

## 非原因

- 不是 CrEST、Second Thought 或 Harness-IF 的公开经验结果已被推翻；
- 不是没有计算资源就把候选当成科研反证；
- 不是 v029 宿主安全控制的延伸；
- 不是 Run 终局。

## 决定

不注册实验或 Seed。保留 CrEST 的局部—聚合保证边界和 Harness-IF 的行为分层—因果响应区别；Run 保持 `ACTIVE`，下一版离开上述方法族。
