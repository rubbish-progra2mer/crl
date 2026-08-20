# v107 研究地图

## 主动诊断事实

- `workbench_v107/diagnosis/v107_frontier_convergence_20260817/report.md` 的权限为 `ADVISORY_NON_AUTHORITATIVE`；其事实哈希为 `c0c6e52685d2698c603e63820a5d705fe8e0af2f8b3d8b47d17c160210fb893a`。
- 诊断时 Run 为 Contract v3、`ACTIVE`、当前版本 `v107`。全 Run 有 106 个已归档科学版本、13 次 Recorded 尝试和 3 次 Formal / Review-support 尝试；v107 自身没有实验。
- 词法召回已重建且可用；语义召回因 `semantic_index_missing` 降级。索引没有污染或陈旧源。该降级只限制语义召回便利性，不构成科研结论。
- 机械统计显示近期主要产出是问题图谱与先行工作碰撞，而不是跨模型现象复现。主研究者据此把下一步从“方法标题扫描”改为“先验证稳定现象”；这是一项解释，不是诊断器自动给出的决策。

## v029 安全转化复核

- 宿主平台安全控制继续被记录为外部执行边界，不是反证、先行工作碰撞或 Run 终局；没有尝试规避、绕过或削弱控制，也没有继续研究可操作的过滤绕过。
- 唯一安全的本地转化是无真实目标、无密钥、无网络和无漏洞载荷的能力—效果抽象图审计。
- v029 已确认该计算等同于结构化能力/效果事实、组合策略规则和禁止效果可达性查询；ToolGuardian、AgentGuard、能力增强型工具协议以及传统权限图分析均直接覆盖。重新实现只能产生玩具复现，不能恢复方法差分。

## 跨会话状态移交

- [Handover of In-Context Learning State Across Session Boundaries](https://arxiv.org/abs/2608.14528) 已把移交定义为任务相对的上下文学习状态，在外生性条件下以预测等价刻画最粗确定性充分移交，并区分精确保留、重复证据统计和未被统计保持的原始观察。
- Run v060 已检查压缩时控制状态丢失，v103 已检查人机责任移交。把决策、约束和必要观察编译成会话交接包，已同时被最新充分移交理论和 Run 内边界吸收。

## 后果敏感的核验预算

- [LLMs Don't Pay for the Jump](https://arxiv.org/abs/2608.14397) 提出模型在因果难度上升时输出熵未同步变化，但其“让认识错误产生物理代价”是理论论点，不直接给出工具智能体方法。
- 可执行化后，候选只能根据错误损失、当前不确定性、核验成本和核验结果的行动价值分配额外计算。这归约为期望信息价值、风险敏感决策与自适应测试时计算。
- [Structured Uncertainty guided Clarification for LLM Agents](https://aclanthology.org/2026.findings-acl.2028/) 已用完美信息期望价值与提问成本选择澄清；[Adaptive Test-Time Compute Allocation via Learned Heuristics over Categorical Structure](https://arxiv.org/abs/2602.03975) 已按局部不确定性分配核验调用；[Adaptive Test-Time Compute Allocation for Reasoning LLMs via Constrained Policy Optimization](https://arxiv.org/abs/2604.14853) 已把准确性—计算预算分配写成约束优化。
- 因而“高后果任务多核验”可以是工程策略或评价切片，但没有留下新的方法计算。

## 纠错路线独立性

- [Grounding Without Corrective Control](https://arxiv.org/abs/2608.14252) 已区分继承约束与当前纠错能力，并用路线配置表示哪些证据/工具/反馈路径约束系统及其相互依赖。
- Run v085 已检查权限、事实与完成依赖，v089/v090 已检查来源链和伪多源依赖。再用“独立纠错路线数量”选择工具或置信度，会回到来源依赖图、数据乱伦消除和证据路由。

## 结论

三个入口均未留下可注册方法。v107 不运行实验；下一版本必须从良性任务中的跨模型可重复失败出发，而不是从某篇论文的未来工作措辞生成方法。
