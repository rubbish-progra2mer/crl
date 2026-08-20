# v006 研究地图

## Run 内知识库命中

- P027 `Verified Critical Step Optimization for LLM Agents`：替换单步动作并重放后缀，只在终局翻转时构造局部偏好。
- P074 `ToolGate`：调用前条件、返回后条件与验证后状态提交，但不测试最终动作对结果的反事实依赖。
- P041 `LLM Agents Already Know When to Call Tools`：探测工具必要性并在生成前引导，不处理调用后的因果依赖。

## 近期直接先行

- Counterfactual Sensitivity for Faithful Reasoning in Language Models（2025，arXiv:2509.01544）：通过中间推理反事实干预定义结果敏感度，并用训练正则强化输出依赖。
- Causal Agent Replay: Counterfactual Attribution for LLM-Agent Failures（2026，arXiv:2606.08275）：把智能体运行建模为结构因果模型，用 `do` 干预和后缀重执行测量结果分布变化。
- Verify Before You Commit: Towards Faithful Reasoning in LLM Agents（ACL 2026）：在外部动作前审计证据支持的内部信念并迭代修复。
- Auditing Provenance Sensitivity in LLM Agent Action Selection（2026，arXiv:2607.20827）：对智能体动作做受控来源干预与部分证据交互审计。

## 判断

“置换合法工具结果并测量动作变化”是上述反事实敏感度与因果重放的直接工具场景实例化；“提交前阻止不敏感动作”又落入已有的提交前信念审计。工具消息角色本身没有产生新的因果估计量、验证边界或修复计算。
