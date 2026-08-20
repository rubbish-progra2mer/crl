# v069 研究图谱

## 重复执行与可靠性曲面

- *τ-bench* 已用 `pass^k` 衡量多次试验下的智能体行为可靠性，并报告同一任务上的显著不一致。
  - https://arxiv.org/abs/2406.12045
- *ReliabilityBench* 直接联合重复执行、语义等价任务扰动与工具/API 故障强度，形成可靠性曲面，并注入超时、限流、部分响应和模式漂移。
  - https://arxiv.org/abs/2601.06112

## 工具环境故障

- *ToolBench-X* 直接评价可恢复的工具环境危害，覆盖规格漂移、调用错误、执行失败、输出漂移和跨来源冲突，并要求每个实例至少保留一条重试、回退、验证或交叉检查的恢复路径。
  - https://arxiv.org/abs/2606.25819
- *Faithful Simulation of User–Agent–Environment Interactions* 把用户、智能体和环境统一模拟，并报告环境可靠性是智能体成功的主导因素。
  - https://openreview.net/forum?id=Dg1IcqsRgt

## 方差归因

- *Stochasticity in Agentic Evaluations* 用级内相关系数把总方差分解为任务间难度与同任务试次间智能体不一致，并讨论模型采样、插件错误、环境延迟/限流、重试及评分启发式等来源。
  - https://arxiv.org/abs/2512.06710
- *Deployment Decision Reliability* 在 TheAgentCompany、τ²-bench 与 AppWorld 上使用四因素广义化理论分解，报告智能体主效应很小而智能体×任务交互占有显著方差，并据此讨论评测规模与部署决策可靠性。
  - https://arxiv.org/abs/2608.11323

## 结论

重复执行、故障强度扫描、同任务/跨任务方差分解以及环境可靠性归因均已有直接工作。把本地确定性工具改成带随机失败、延迟或输出抖动的版本，只能复现 ReliabilityBench 或 ToolBench-X；把结果拟合为随机效应模型，则落入现有级内相关和四因素广义化理论。因此不注册实验。
