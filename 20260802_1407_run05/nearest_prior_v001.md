# 最近工作与公平差异 v001

## 直接系统近邻

### 智能体计划缓存（P071）

`Agentic Plan Caching: Test-Time Memory for Fast and Cost-Efficient LLM Agents`（NeurIPS 2025）的计算是：成功轨迹经规则和轻量模型抽象成计划模板与关键词；新请求按关键词定位模板，再由轻量模型适配。它直接建立了“大语言模型智能体计划可以缓存并复用”的问题，也明确报告语义请求缓存存在错误命中。

ECPC 不以关键词或向量分数作最终提交判据：文本检索只召回候选；缓存写入时主动改变任务槽位并重放参考规划/执行，以规范化工具轨迹的变化构造复用门禁。与 P071 的最小差异是“命中后能否提交”所依赖的证据由文本相似性变成了执行敏感性。

### AgentReuse

`A Plan Reuse Mechanism for LLM-Driven Agent`（arXiv:2512.21309）用意图分类判断请求是否足够相似并复用计划。它加强了文本/意图匹配基线，但没有报告在缓存写入期主动生成近邻任务、用工具轨迹差分识别复用边界。

## 契约与技能近邻

### SkillOps

`SkillOps: Managing LLM Agent Skill Libraries as Self-Maintaining Software Ecosystems`（arXiv:2605.13716）把技能表示为带前置条件、输出、假设、验证器与失败信息的类型化技能契约，并在任务期先检索、再按前置条件过滤和约束拼接。它占用了“显式契约过滤技能复用”这一宽主张。

ECPC 不应声称首创技能契约或前置条件门禁。其较窄差异是契约的获得方式和对象：针对一个已成功的整段工具计划，主动对任务槽位做单因素及有限成对干预，以轨迹骨架、依赖和绑定变化反推出这个缓存项的经验复用边界，而不是从既有日志或规则维护通用技能契约。

### ContractSkill

`ContractSkill: Repairable Contract-Based Skills for Multimodal Web Agents`（arXiv:2603.20340）把网页技能改写为带显式过程结构、前置/后置条件、恢复和终止检查的可验证、可局部修复制品。它进一步说明“显式前置条件和可执行契约”不是 ECPC 的新意。ECPC 当前只讨论既有成功计划的复用提交，不主张技能生成、验证或修复。

### SkillWrapper

`SkillWrapper: Generative Predicate Invention for Task-level Robot Planning`（arXiv:2511.18203，2026-06 修订）主动采集黑盒机器人技能的执行数据，发明可解释谓词并学习可用于规划的符号技能模型，目标包括刻画技能的起始集合、前置条件和效果。它是“主动执行以学习适用条件”的强机制近邻。

因此 ECPC 不能把“通过主动试验学习适用条件”本身作为新颖性。剩余可检验差异只在：文本工具智能体的整段缓存计划、任务描述槽位干预、规范化多步工具轨迹差分，以及由该差分生成缓存提交门禁。SkillWrapper 面向低层机器人技能到符号规划模型的抽象；ECPC 不学习完整世界模型、效果谓词或可证明完备的规划算子。

### 反事实轨迹审计

`Counterfactual Trace Auditing of LLM Agent Skills`（arXiv:2605.11946）在同一个任务上配对“带技能/不带技能”的智能体轨迹，度量技能怎样改变行为。ECPC 固定候选计划的来源，改变任务槽位以估计其适用域；它不是技能影响评估，也不以技能有无为干预量。

## 更早的计划复用传统

案例式规划长期研究从旧问题与旧计划中检索、适配并验证新问题的解。`Parameterized Complexity Results for Plan Reuse`（AAAI 2013，arXiv:1307.4440）还研究了给旧计划增加步骤等复用问题的参数化复杂度。因此 ECPC 不声称首创计划复用、计划适用性或案例适配；它提出的是缺少完整符号域模型时，为大语言模型工具计划缓存主动学习一个经验提交门禁。

## 跨领域机制来源

P097/P098 的行为敏感性与约束注入用于发现优化模型漏约束；P101 用能够区分语义邻居的小测试集检验程序。ECPC 借用了“以行为差分区分邻居”的算子，但干预点是缓存写入和命中，而非优化模型验证或程序判分。

## 最小主张

在任务槽位可抽取、参考规划可在沙箱重放、工具轨迹可规范化的文本工具工作流中，给召回到的缓存计划附加由槽位干预与轨迹差分得到的经验复用门禁，可能比只依赖文本/意图匹配更好地拒绝约束近邻，同时比全槽位精确匹配保留更多安全复用。

这不是穷尽性新颖性证明；也不主张对开放网络、不可重放副作用、任意自然语言、所有等价轨迹或高阶交互有效。

## 主要来源

- P071：https://proceedings.neurips.cc/paper_files/paper/2025/file/9549f7d06700f0966d5f938f1d11022a-Paper-Conference.pdf
- AgentReuse：https://arxiv.org/abs/2512.21309
- SkillOps：https://arxiv.org/abs/2605.13716
- ContractSkill：https://arxiv.org/abs/2603.20340
- SkillWrapper：https://arxiv.org/abs/2511.18203
- 反事实轨迹审计：https://arxiv.org/abs/2605.11946
- 参数化计划复用：https://arxiv.org/abs/1307.4440
