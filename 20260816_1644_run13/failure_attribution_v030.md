# v030 失败归因

- 现象有效：Agent-Diff 发布评测器没有实现论文声明的闭世界 `clean` 门控，本地成功见证证明未要求副作用可以在当前实现下保留满分。
- 非反证：实验没有反驳“闭世界状态差分评测”本身；相反，它说明发布代码没有执行论文所定义的方法。
- 科研主因：候选审计计算与 BenchGuard、Auto Benchmark Audit、STING、Layer-Isolated Evaluation、Protocol-Level Identifiability Audit 和通用蜕变测试发生方法级组合碰撞。
- 范围边界：本版本不声称 260 个空基础差分都是可成功任务；只把它们用于证明评测函数对某类真实模式变异不敏感。
- 决策：以 `prior_collision` 终止候选，保留脚本、固定提交、论文副本和机器可读审计结果供本 Run 审计。
