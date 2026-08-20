# v122 研究图谱

- [From Agent Traces to Trust](https://arxiv.org/abs/2606.04990) 已把检索证据、工具输出、记忆条目、中间声明、动作与最终答案统一为执行来源关系，并覆盖声明级语义来源、记忆谱系、故障诊断和恢复。
- [ProvenanceGuard](https://arxiv.org/abs/2606.18037) 已把答案拆成原子声明，路由到带稳定来源标识的证据，分别检查支持关系与声明的来源归属；其多来源评测显示精确“来源加关系”准确率仅 0.229，直接暴露相似来源间责任归属的困难。
- [MemIR](https://arxiv.org/abs/2605.25869) 已用带类型的记忆中间表示分离原始证据、检索线索和可承载事实的声明原子，并以来源作用域限制使用。
- [MemLineage](https://arxiv.org/abs/2605.14421) 已给每个记忆条目附加密码学来源和大语言模型派生有向无环图，记录哪些检索条目影响新记忆；这直接覆盖跨变换的派生责任链。
- [Who&When](https://arxiv.org/abs/2505.00212) 已把多智能体失败归因定义为识别责任智能体和首个决定性错误步骤，并发布 127 个系统的细粒度标注轨迹。
- [AgenTracer](https://arxiv.org/abs/2509.03312) 通过反事实回放和程序化故障注入生成归因数据，并训练模型定位责任智能体与步骤；[TraceElephant](https://aclanthology.org/2026.acl-long.912/) 又提供完整输入、上下文和可复现环境的全执行轨迹，报告完整可观测性相对仅输出轨迹最高提升 76.5%。
- [ErrorProbe](https://aclanthology.org/2026.findings-acl.98/) 已按症状逆向追踪并用工具落地执行验证错误假设；[RAFFLES](https://aclanthology.org/2026.eacl-long.359/) 同样直接执行步骤级错误归因。
- [Understanding the Information Propagation Effects](https://aclanthology.org/2025.emnlp-main.623/) 已用因果框架分析正确与错误信息在多智能体通信拓扑中的传播，并据此学习兼顾抑错和信息扩散的拓扑。

因此，“来源是谁”到“谁在何步首次改变语义”的整个自然梯度已有来源图、派生图、全轨迹、反事实回放、逆向追踪和因果传播方法。把边类型从 `derived_from` 改名为 `mutated_by` 不产生新的改变计算。
