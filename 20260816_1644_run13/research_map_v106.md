# v106 研究地图

## 消息的轨迹价值

- [Wrong but Useful](https://arxiv.org/abs/2608.14375) 已把消息自身答案正确性与其对下游整合器的上下文条件轨迹价值分开，用固定消息池、可见/隐藏重放和重复对照测量逐消息效应，并报告同题一项删除选择机会；论文明确不声称对未见问题的在线选择器。
- [Contextual Counterfactual Credit Assignment](https://arxiv.org/abs/2603.06859) 已在固定转录上下文和固定继续策略下以留一基线提取逐消息边际优势，并用于策略梯度训练。
- [Nash-Pruned CredMAS](https://aclanthology.org/2026.findings-acl.1975/) 已从偏置日志离线学习上下文条件边际价值函数，再在线按预测效用选择通信成员。
- [Semantic Cooperative Games](https://arxiv.org/abs/2607.18255) 又以语义超图和语义夏普利值降低反事实重放成本。因而“用轨迹价值标签训练未见问题消息选择器”已有直接方法族。

## 技能的适用性与执行

- [Demystifying Agent Skills](https://arxiv.org/abs/2608.14036) 已在 8,135 条试验记录上分解表示、结果注释、检索、跨框架迁移和下游执行，指出技能主要作为程序锚点，且正确技能调用既非成功的充分条件也非必要条件。
- [Skill-Use](https://arxiv.org/abs/2608.04828) 已分别评价触发、程序遵从和边界；[SLBench](https://arxiv.org/abs/2607.09016) 已从技能文件抽取前置条件、约束与回退等逻辑关系并形成可执行测试。
- [SoK: Agentic Skills](https://arxiv.org/abs/2602.20867) 已把适用条件、执行策略和终止条件列为技能一等组成；[Don’t Offer What Can’t Be Done](https://arxiv.org/abs/2608.01050) 已按权威状态与退出条件确定性过滤不可执行技能。

## 等待窗口与观察条件分支

- [Second Thought](https://arxiv.org/abs/2608.13667) 已在动作—观察等待窗口并行生成检查、回忆、预演和备选原子想法，并在观察到达时收集给下一轮。
- [Building Interactive Real-Time Agents with Asynchronous I/O and Speculative Tool Calling](https://arxiv.org/abs/2605.13360) 已重叠模型处理与外部等待，并管理信息未完整时的投机工具调用。
- [Speculate While You Reason](https://arxiv.org/abs/2607.25816) 已让同一智能体预测并提前执行下一工具调用，同时仅在预测命中时获得延迟收益。
- Run v052 已关闭未来值、完成中断和依赖感知并行；v065 已关闭取消栅栏和迟到效果隔离。给预先想法附观察守卫、结果到达后只提交匹配分支，是经典投机执行的提交规则迁移，没有留下新的语言智能体计算。

## 证据解释—聚合接口

- [Split the Labor](https://arxiv.org/abs/2608.14509) 已用假设、可靠性桶、理由和来源四元组分离逐源解释与固定聚合，推导计数尺度漂移，并以校准对数似然比和依赖块折扣修复。
- Run v009/v090 已因数据乱伦、重复计数消除和依赖感知融合关闭证据根归一化及伪多源佐证。

## 结论

四项均有直接计算或当前 Run 精确边界；本版不注册实验。
