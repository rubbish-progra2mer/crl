# v067 研究图谱

## 入口一：工具观察是否真正影响答案

- *The Illusion of Visual Tool-Use* 已用策略、轨迹与单步反事实干预审计返回观察的因果贡献，并定义 Calling Without Looking / Looking Without Planning。
  - https://arxiv.org/abs/2608.06270
- 当前 Run v006 已因反事实敏感度、因果轨迹重放和提交前信念审计的直接碰撞关闭文本工具结果重放。

结论：把最新视觉因果审计平移到文本工具，仍是 v006 已关闭的“替换观察—重放—看翻转”。

## 入口二：完成判断与行为惯性

- *LATTE* 直接处理深度搜索智能体过早终止、工具调用不足，并围绕继续/停止决策训练。
  - https://openreview.net/forum?id=cXKzStnOIQ
- *Agentic Abstention* 把继续、回答或停止建模为顺序决策，并提出 CONVOLVE 停止规则。
  - https://arxiv.org/abs/2606.28733
- *Mitigating Conversational Inertia in Multi-Turn Agents* 已定义多轮自我模仿惯性，并用上下文偏好学习修复。
  - https://arxiv.org/abs/2602.03664
- *ToolAnchor* 已把扩展工具集中的熟悉工具回退定义为行为惯性，并用反事实锚点与后训练干预。
  - https://arxiv.org/abs/2607.14145

结论：完成线索捕获、工具惯性或“继续一步”提示均已有直接现象和方法。

## 入口三：接口等价与表示扰动

- *ToolScope* 已合并冗余等价工具并做上下文过滤。
  - https://arxiv.org/abs/2510.20036
- *Diagnosing Tool-Selection Reasoning with Canary Tools* 已包含语义诱饵、能力幻象、前置条件、时间与粒度陷阱。
  - https://arxiv.org/abs/2608.04719
- *Towards a Science of AI Agent Reliability* 已把参数重命名、字段重排和工具接口变化列为保持语义的环境鲁棒性。
  - https://arxiv.org/abs/2602.16666

结论：把同一能力拆分/合并后做不变性评测，只剩已有环境鲁棒性和工具合并的交集。

## 入口四：科研智能体的新颖性判断

- *Literature-Grounded Novelty Assessment of Scientific Ideas* 的 Idea Novelty Checker 已按应用域、目的、机制、评价和组合分面检索、重排与比较相关工作。
  - https://aclanthology.org/2025.sdp-1.9/
- *RINoBench* 已把研究想法结构化为问题、目标与方案，给出相关工作，并评测五级新颖性及有文献根据的解释；强模型的宏 F1 仍很低。
  - https://arxiv.org/abs/2603.10303
- *On the Limits of LLM-as-Judge for Scientific Novelty Assessment* 直接报告新颖性幻觉：模型评审偏爱模型生成问题，而领域专家偏好作者锚定问题。
  - https://arxiv.org/abs/2606.12071
- *Navigating Ideation Space* 已以问题、方法和发现的分解表示服务相关工作检索与新颖性定位。
  - https://arxiv.org/abs/2601.08901

结论：把“changed computation”写成额外分面仍属于已有分面检索与贡献比较，没有新的判定计算或监督信号。

## 入口五：前瞻记忆

- *PM-Bench* 已直接定义智能体在持续活动中维持并按未来线索/状态执行意图的问题，覆盖时间触发、事件触发、隐藏状态监测、更新敏感任务及多种账本/心跳/层级配置。
  - https://arxiv.org/abs/2607.12385
- *Do Proactive Agents Really Need an LLM to Decide When to Wake and What to Anchor?* 已用结构化事件流和时序图学习器计算触发概率与实体路由。
  - https://arxiv.org/abs/2605.30152

结论：前瞻记忆是真实未解现象，但事件编译、待办账本、心跳或学习触发器都有直接先行；退回事件—条件—动作规则又被经典复杂事件处理吸收。
