# v101 研究地图

## 自动科研过程评价

- [Beyond Final Scores](https://arxiv.org/abs/2608.13417) 已用解题定框、执行和反馈控制刻画长周期研发代理的过程，并比较任务内外经验复用与不同运行框架的稳定性。
- [Training AI Scientists to Replicate Research](https://arxiv.org/abs/2608.13331) 已建立论文复现任务空间、自动量规裁判和经训练的科研代理。
- [ARAC-Bench](https://arxiv.org/abs/2608.12788) 已把研究过程拆为提案、实验和综合，并量化与人类研究过程的对齐和完整性。
- [Sampling Luck Masquerades as Allocation Gain](https://arxiv.org/abs/2608.13087) 已证明同一存储样本上选择并评价分配策略会产生虚假收益，并以样本外校正保留真实分布移位收益。
- [Agentic Auto-Research is Fuzz Testing](https://arxiv.org/abs/2608.09855) 已明确提出稠密认识进展信号、反馈引导搜索和受保护最终验证。
- Run 内 v020、v055、v067、v084 已分别覆盖实现方差、自适应验证污染、科研有效性与反馈信号。过程分解、覆盖引导或保护验证的组合没有剩余独立计算。

## 用户—代理共享代码工作区

- [SWE-Touch](https://arxiv.org/abs/2608.02499) 在任务关键区域注入与任务冲突的用户修改；九个模型平均解决率下降 7.7 个百分点。论文还包含有益 `Co-Edit` 对照，其平均变化为 -0.1 个百分点，并明确把有益、不完整、含糊和冲突干预的校准列为未来扩展。
- [CORVUS](https://arxiv.org/abs/2607.22711) 已用同步文件注册表替换追加式陈旧快照，使每轮推理读取当前文件内容。
- [CoAgent](https://arxiv.org/abs/2606.15376) 已用顺序过滤读取、冲突通知、计划修补和事务式逆操作处理共享状态并发。
- [Effective Strategies for Asynchronous Software Engineering Agents](https://arxiv.org/abs/2603.21489) 已用中心化委派、隔离工作区、分支合并和可执行测试验证处理并行代码修改。
- Run 内 v012、v061、v079 已覆盖依赖失效、动作修订和共享状态并发。拟议的“监测变化—使读集失效—三方协调—定向测试”是上述方法的组合，不注册实验。

## 分解边界与取得但未使用的表示

- [Decomposition-Induced Context-Memory Conflict](https://arxiv.org/abs/2608.10627) 已证明原子主张分解器会用参数记忆替换源文本，并用跨设置线性探针与上下文感知解码研究机制和缓解边界。
- [Detecting an Effect Is Not Learning to Act on It](https://arxiv.org/abs/2608.10441) 区分总体效应存在与逐实例路由可学习性，并给出奖励信噪比下限。
- [Causal Structure is Inducible but Functionally Decoupled](https://arxiv.org/abs/2608.11767) 直接显示类型化路由结构可被诱导却不驱动答案读出。
- Run 内 v006、v023、v044、v067、v083 已处理观察取得但未用于动作、诊断证据压缩、声明—执行差分、因果观察和注意/读出边界。新增分解器配对题或路由标签实验不会越过直接工作。

## 结论

三类系统级对象均是真实问题，但核心现象、评价协议和主要干预已经公开；当前可做的本地缩小实验只会复现，而不会改变剩余贡献差分。
