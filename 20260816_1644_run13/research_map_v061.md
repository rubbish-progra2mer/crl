# v061 研究图谱

## 动作具体度与澄清

- [Structured Uncertainty guided Clarification](https://aclanthology.org/2026.findings-acl.2028/) 已在工具参数及其域上分离规格不确定性与模型不确定性，并用完美信息期望价值选择澄清问题。
- [Learning to Ask](https://aclanthology.org/2025.emnlp-main.1104/) 已直接测量不完整指令下猜测参数与请求澄清。
- [Uncertainty-Aware Clarification](https://arxiv.org/abs/2606.03135) 已用信息增益奖励训练工具智能体。

## 个性化作用域

- [RealPref](https://arxiv.org/abs/2603.04191) 已直接评价偏好向未见情境的泛化。
- [PersonaAgent](https://aclanthology.org/2026.findings-acl.1315/) 与 [PersonalAlign](https://aclanthology.org/2026.acl-long.1669/) 已把情节/语义记忆连接到个性化动作与长期记录。
- [C3PO](https://openreview.net/forum?id=ngcZhfXCBW) 专门通过情境化批评与约束偏好优化减少语言反馈的过度泛化。

## 可逆性与信息寻求

- [Revisable by Design](https://arxiv.org/abs/2604.23283) 已形式化幂等、可逆、可补偿和不可逆动作，并证明不可逆冲突限制。
- [DreamPhase](https://openreview.net/forum?id=81PJ2KPnmK) 已用不确定未来模拟减少实际不可逆动作。
- [From Assumptions to Actions](https://arxiv.org/abs/2602.04326) 已把假设转成决策树，并按概率、目标收益和执行成本选择动作。

## 证明依赖调度

- [Goedel-Architect](https://arxiv.org/abs/2606.06468) 已生成定义/引理依赖图并并行关闭节点、按失败细化全局蓝图。
- [LeanMarathon](https://arxiv.org/abs/2606.05400) 已从动态叶节点向上、按持续集成门控轮次释放证明有向无环图。
- [Optimizing the Cost-Quality Tradeoff of Agentic Theorem Provers](https://arxiv.org/abs/2606.04883) 已依据失败轨迹估计继续当前目标或重启分解的成本—成功权衡。

## 评测可识别性

- [Beyond Local Accuracy](https://arxiv.org/abs/2608.13326) 对有限、冻结、确定性策略类做协议级可识别性审计，并以命中集综合最小识别支持；其局限明确包括策略类非穷尽和自然任务外部效度未知。
- [AgentAssay](https://arxiv.org/abs/2603.02601) 已为非确定性智能体工作流提供三值统计判定、智能体变异算子、变形关系和自适应试验预算。
- [Cer-Eval](https://openreview.net/forum?id=eCx0fOWiSA) 已做带置信保证的自适应评测样本选择。
- [Mutation-Guided LLM-based Test Generation](https://arxiv.org/abs/2501.12862) 已在软件测试中生成当前未检出的变异体及相应杀伤测试，但评价对象不是智能体行为协议。

现有工作分别覆盖“在给定策略类上找最小支持”和“对固定变异算子做随机智能体回归测试”。仍待检查的差分是开放策略类下的协议补全：生成在当前支持上与目标策略碰撞、却在未观测场景违反目标性质的行为程序，再综合区分场景。
