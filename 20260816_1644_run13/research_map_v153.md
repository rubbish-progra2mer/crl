# v153 研究图谱

## 目标工作

- [FlowScout: From Execution Feedback to Reliable Tool-Using Agent Workflows](https://arxiv.org/abs/2608.10039) 把语言模型节点、工具节点和依赖边表示为可编辑工作流图，从人工验证的历史工具序列中用流程挖掘得到领域级常见工具协调骨架，再用蒙特卡洛树搜索和执行反馈修改节点、边、控制结构与提示词。
- FlowScout 在金融、体育、旅行和天气四个 ToolBench 领域中使用 5:2:3 的优化、验证、测试划分；优化器为 GPT-4o，执行器为 GPT-4o-mini，工具链最长不超过 6。
- 论文报告的四领域平均工具协调分数为 0.7515，ReAct 为 0.3900；平均执行分数为 0.7381，ReAct 为 0.6273，AFlow 为 0.6172。平均运行时间为 22.80 秒，ReAct 为 11.44 秒，AFlow 为 18.37 秒。
- 金融消融中，完整方法的工具协调分数 0.6583、执行分数 0.7349；束搜索的工具协调分数反而更高，为 0.6768，但执行分数只有 0.5327。这说明精确工具序列相似度不是任务正确性的充分代理。
- 作者报告未见但功能相似工具上的金融执行分数从 0.7349 降至 0.6751；论文同时把单一语言模型裁判、只使用人工验证记录、工具链不超过 6 和工具协调指标惩罚替代有效调用列为限制。

## 候选现象

FlowScout 在每个领域从验证轨迹中抽取一个常见骨架。若同一领域内存在互不兼容的流程模态，频率聚合可能把不同分支、循环或工具次序压入一个复杂骨架，造成低频但有效的任务族被多数轨迹覆盖。这一现象在语言模型提示中可能表现为额外工具调用、错误分支或无关约束。

## 最近邻流程挖掘先验

- [Model-driven Stochastic Trace Clustering](https://arxiv.org/abs/2506.23776) 明确把高变异事件日志导致复杂、难解释的单一流程模型作为问题，并通过把轨迹分配给簇特定随机流程模型来得到更简单的控制流模式。它还说明轨迹聚类和模型驱动轨迹聚类早已是成熟路线，而该工作新增的是概率转移与随机一致性。
- [Visualizing Trace Variants From Partially Ordered Event Data](https://arxiv.org/abs/2110.02060) 把唯一活动执行序列直接定义为轨迹变体，并指出流程挖掘系统普遍分析和可视化这些变体；即“保留多个流程模态”不是语言模型智能体特有的新表示。
- [Discovering Business Area Effects to Process Mining Analysis Using Clustering and Influence Analysis](https://arxiv.org/abs/2003.08170) 先按流程流特征聚类案例，再寻找与各簇相关的业务区域，已经给出“由上下文条件解释并选择流程变体”的经典管线。

## 最近邻语言模型智能体先验

- [AutoFlow: Automated Workflow Generation for Large Language Model Agents](https://arxiv.org/abs/2407.12821) 以自然语言程序表示智能体工作流，并通过微调或上下文学习迭代优化面向复杂任务的工作流。
- [AFlow: Automating Agentic Workflow Generation](https://arxiv.org/abs/2410.10762) 把代码表示的语言模型工作流优化转成蒙特卡洛树搜索，以执行反馈和树状经验修改工作流。
- [Optimizing Agentic Workflows using Meta-tools](https://arxiv.org/abs/2601.22037) 从既有工作流轨迹发现重复工具序列并编译为确定性复合工具，覆盖另一种轨迹到工作流的直接优化路径。

## 当前 Run 内部边界

- v004 已记录 LLMCompiler 的类型化数据流执行以及 EvoFlow/Evoflux 式结构化执行反馈工作流图演化。
- v048 已记录 Living-Harness、A-Evolve 与质量多样性执行外壳演化。
- v130 已因“接受后缀解析／工作流状态编译”被执行反馈外壳演化吸收而关闭轨迹复用候选。
- v149 已记录 MARS 的诊断引导蒙特卡洛树搜索修复；再次提出执行反馈树搜索不能形成新差分。

## 结论

“单一常见骨架会平均掉多模态流程”是合理工程风险，但自然修复正是成熟的轨迹聚类、流程变体发现和上下文路由。FlowScout 自己又处在 AutoFlow/AFlow 及本 Run 已覆盖的执行反馈工作流搜索线上。即使本地合成实验得到正结果，也只能验证已知异质性问题，不能产生可辩护的方法差分，因此 `v153` 不注册实验。
