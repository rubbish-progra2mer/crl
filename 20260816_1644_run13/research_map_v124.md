# v124 研究图谱

- [Handover of In-Context Learning State Across Session Boundaries](https://arxiv.org/abs/2608.14528) 把移交写成先于下游输入的状态编码问题；在每个既往上下文共享同一下游输入分布的外生性条件下，预测等价类给出最粗确定性充分记录与固定长度比特下界。
- 该论文没有把外生性暗中外推到自由行动智能体。它明确指出：自由行动会改变下一观察，因此一个目标的充分性不保证自适应轨迹被保留；当下游输入依赖既往上下文时，充分性必须在联合任务分布上评价，不能使用共同输入测度的商集。论文还显式给出行动—观察轨迹分布和轨迹损失。
- 因而可研究的剩余不是纠正论文错误，而是为自适应轨迹构造更强的等价关系。该关系需要同时保持行动相关的转移、观察与价值，已经是经典决策状态抽象问题。
- [On learning history-based policies for controlling Markov decision processes](https://proceedings.mlr.press/v238/patil24b.html) 已正式分析基于历史特征抽象控制马尔可夫决策过程，并据此构造强化学习算法。
- [Near Optimal Behavior via Approximate State Abstraction](https://proceedings.mlr.press/v48/abel16.html) 与 [Value Preserving State-Action Abstractions](https://proceedings.mlr.press/v108/abel20a.html) 已给出近似状态/状态—行动抽象的价值保持和次优性边界；双模拟类关系正是要求合并状态保持奖励与转移。
- [Common Information based Approximate State Representations in Multi-Agent Reinforcement Learning](https://proceedings.mlr.press/v151/kao22a.html) 已在去中心化部分可观测场景压缩共同与私有历史状态，并给出近似动态规划的最优性差距。
- [ACE](https://arxiv.org/abs/2606.31564) 在大语言模型智能体层面保存无损原始轨迹，并根据每一步当前任务状态动态选择原文、摘要或丢弃，避免一次移交编码永久决定后续可见信息。
- 本 Run 的 v031 又已记录 Decision-Aware Memory Cards：它按动作变化、结果提升、必要性和负迁移风险评价上下文单元；v060 已关闭保留未完成义务和开放依赖的结构化移交候选。

所以，“将预测等价换成轨迹/价值等价”是重要边界，但改变计算已由历史状态抽象、双模拟/价值保持抽象和决策感知记忆覆盖。将这些原理重新命名为跨会话轨迹充分性，不形成独立方法核。
