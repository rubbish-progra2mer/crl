# v008 API 演化与既有工具计划迁移：精确先行工作碰撞审计

> 性质：Codex App 原生 Research Subagent 的独立、非权威草案。
>
> 范围：仅审计当前 Run `20260813_1547_run10` 的 v008 暂定方向；不读取其他 Run；不替代主 AI 研究者的科研裁决。
>
> 截止日期：2026-08-13。本文只把论文原文、出版社/会议页、作者稿或官方代码库作为方法证据；搜索聚合页只用于发现，不作为方法证据。

## 1. 被审计的问题核与最低方法增量

暂定问题核可操作化为：给定在旧版工具集合/API 版本上已经成功的工具计划或技能 `P_old`，以及变化后的新版工具集合/API `T_new`，系统不是从任务描述和新文档重新规划，而是利用旧/新版本的配对行为试验，得到迁移后的 `P_new`，尽可能保持原计划的任务相关效果。变化至少包括：

- 参数重命名、增删、位置/关键字变化；
- 默认值变化；
- 单操作拆成多操作或多操作合并；
- 返回字段、嵌套结构、错误语义变化；
- 有状态工具中的操作顺序或前置条件变化。

若方法只做以下任一项，则在本审计中不构成足够的新计算：

1. 比较两版 OpenAPI/JSON Schema 后做确定性字段映射；
2. 让大语言模型读取新文档并重写调用；
3. 运行新版工具、把错误反馈给大语言模型，直到最终验证器通过；
4. 重写工具描述、补充示例或重新规划整条轨迹；
5. 对旧/新响应做一般差分检测，但不合成迁移后的计划/适配器。

## 2. 查询记录与检索边界

### 2.1 当前 Run / 共享知识库检索

读取了当前 Run 的 purpose-aware retrieval 导航报告：`hypotheses_v008/searches/api_evolution_plan_migration_v008_01/report.md`。其中五组原始查询为：

1. `LLM tool agent cached plan or skill fails under evolving API schemas, tool names, defaults, operation split, response changes`
2. `previously successful tool workflow becomes invalid or silently semantically wrong after tool or MCP server evolution`
3. `cross-version differential behavioral equivalence, plan migration, tool sequence repair, schema matching, one-to-many API replacement`
4. `API migration, REST API differential regression testing, MCP tool evolution, agent robustness under schema drift, program repair`
5. `end-state task success under unseen tool evolution, migration exactness, extra probes, abstention, semantic equivalence`

该报告覆盖 98 篇论文，但代表命中以一般智能体计划缓存、工具鲁棒性、契约执行和行为验证为主，没有直接返回 Sprout、M³、APIFix、AppEvolve、GUPPY、SkillRevise 或 EvoC2F。因此本次外部检索沿经典软件演化与 2025–2026 智能体工具演化两条线补齐，未修改共享知识库。

### 2.2 外部精确查询

实际执行的代表性查询（搜索引擎只作导航，结论回到一级来源核验）：

- `"EvoC2F" API version migration schema changes`
- `"EvoC2F" versioned skill migration`
- `"A Sound Static Analysis Approach to I/O API Migration" Sprout`
- `"M3: Semantic API Migrations" ASE 2020`
- `"APIfix" output-oriented program synthesis API migration OOPSLA 2021`
- `"Differential Regression Testing for REST APIs" ISSTA 2020`
- `automated API usage update Android examples differential testing Fazzini Xin Orso`
- `LLM deprecated API migration generated tests old new versions iterative refinement`
- `"SkillRevise" LLM skills verifier execution repair`
- `"PLAY2PROMPT" tool use documentation`
- `"A Framework for Testing and Adapting REST APIs as LLM Tools"`
- `"Learning to Rewrite Tool Descriptions for Reliable LLM-Agent Tool Use"`
- `tool schema drift API evolution old successful plan migrate LLM agent`
- `agent plan migration API version downstream continuation equivalence tool schema`
- `site:arxiv.org tool API version migration agent plan repair`
- `site:aclanthology.org API evolution tool schema agent plan migration`

最后四组用于寻找“旧计划的下游智能体延续等价”这一精确同构工作；截至本次检索，没有定位到把它作为迁移目标并合成新版多工具片段的一级来源。该结果只能支持“当前未发现”，不能证明不存在。

## 3. EvoC2F：真实覆盖与未覆盖

一级来源：[EvoC2F: Compiling Tool Orchestration for Efficient and Evolvable LLM Agents（ICML 2026 / OpenReview）](https://openreview.net/forum?id=ZSGB91kMOG)，[ICML 海报页](https://icml.cc/virtual/2026/poster/63166)。

### 3.1 它真实做了什么

EvoC2F 的方法组件已经非常接近“可演化技能基础设施”：

- 把大语言模型提出的编排转为带显式依赖、资源、效果、重试、幂等性语义的计划中间表示；
- 编译成有向无环图，做并行化、关键路径/HEFT 调度，并加入重试、熔断、令牌桶和 Saga 补偿；
- 从成功轨迹中规范化调用，利用 PrefixSpan 挖掘重复子序列，并以反统一/最小一般泛化形成可复用技能；
- 对候选技能做正常、边界和错误注入测试，做前置条件/后置条件契约检查与保留任务回归；
- 通过影子、金丝雀、稳定三个部署层级管理技能，图中明确把技能库标为 versioned。

因此，任何“保存成功工具计划，执行失败后改写，跑回归，再版本化发布”的 v008 方案都会与 EvoC2F 高度重叠。

### 3.2 它没有被核实做什么

在可定位正文、图示和针对 `API version`、`schema change`、`migration`、`old/new API` 的目标词检索中，没有看到 EvoC2F：

- 接收同一外部 API 的旧版与新版；
- 从两版的配对行为试验推断参数/返回结构/操作拆分映射；
- 把既有成功技能自动迁移成新版技能；
- 以跨版本行为等价作为迁移目标。

“versioned skill library”在论文中描述的是技能资产的版本化与安全部署生命周期，不能据此声称它已经解决 API 版本迁移。这个否定判断的强度是“核查文本中未见”，不是“形式化证明论文绝对没有”。

### 3.3 对 v008 的含义

EvoC2F 单篇没有杀死“跨版本迁移”问题，但它吃掉了外围架构贡献。v008 若存活，核心必须是一个 EvoC2F 不能由现有测试/回归/技能版本化自然补上的迁移算子，而不能把版本化、回归门、影子发布当主要新意。

## 4. 经典 API 迁移与行为差分：最强方法级碰撞

### 4.1 Sprout：行为等价、多调用、拆分/合并迁移

一级来源：[A Sound Static Analysis Approach to I/O API Migration（PACMPL/OOPSLA 2025）](https://doi.org/10.1145/3763071)，[作者稿](https://lishangyu.net/publications/oopsla25.pdf)。

精确计算：

- 将旧/新 API 语义分解为原子操作；
- 用专家提供的 API 语义规范、有限状态机/类型状态与 sketch 描述目标；
- 通过流敏感、字段敏感指针分析推断语义变量和值流；
- 定位跨函数、非连续、有状态的多 API 片段；
- 依赖驱动地合成新代码，并以行为树等价保证迁移正确性；
- 明确支持一对一、一对多、多对一和多对多 API 迁移。

这是对“参数变化 + 操作拆分/合并 + 行为等价迁移”最危险的单篇碰撞。它的可利用缺口也很明确：依赖静态程序、LLVM 与专家语义规范；迁移到新领域仍需人工定制规范、状态转换和 sketch；不处理只有黑盒工具访问、自然语言技能和大语言模型下游决策的场景。

### 4.2 M³：无目标库先验的黑盒语义建模与迁移

一级来源：[M³: Semantic API Migrations（ASE 2020）](https://arxiv.org/abs/2008.12118)，[作者稿](https://baltoli.github.io/static/ase.pdf)。

精确计算：

- 不要求目标库源代码、历史变更日志或预先给定迁移映射；
- 对源库和目标库函数生成随机输入/输出例，利用概率程序综合学习可执行行为模型；
- 用 SMT 搜索在用户程序中匹配上下文，并通过内联把库行为与周围代码合并；
- 能发现功能拆分、合并和移动形成的迁移机会；
- 用随机样例做迁移集成测试，得到经验性的观察等价，而非 Sprout 式形式保证。

M³ 直接削弱“黑盒差分试验能发现操作拆分/合并”本身的新颖性。v008 不能只把被迁移对象从 C/C++ 调用改名为工具计划。

### 4.3 APIFix：破坏性变更下的输出导向程序综合

一级来源：[APIFix: Output-Oriented Program Synthesis for Combating Breaking Changes in Libraries（OOPSLA 2021）](https://2021.splashcon.org/details/splash-2021-oopsla/65/APIfix-Output-Oriented-Program-Synthesis-for-Combating-Breaking-Changes-in-Libraries)。

APIFix 从人工适配样例和新版库使用样例中，以输出为导向综合旧到新的变换规则，再把旧版客户端代码自动转换为新版。它直接覆盖“从既有正确使用中合成 breaking-change 适配规则”，只是对象仍是程序代码，不是工具智能体的计划/技能。

### 4.4 AppEvolve：跨项目更新样例 + 差分测试验证

一级来源：[Automated API-Usage Update for Android Apps（ISSTA 2019 作者稿）](https://qixin5.github.io/files/pdf/research/issta19automated.pdf)。

精确计算为四步：识别受 API 变化影响的代码；跨代码库寻找迁移样例；分析、排序并泛化为补丁；依排名应用补丁并用差分测试验证。它已经实现“从他人的成功迁移提取修复，再用跨版本差分验证”。如果 v008 从成功轨迹库中检索类似变更并套用技能补丁，这篇是直接最近工作。

其公开工具实现 [APIMigrator（MOBILESoft 2020 作者稿）](https://www-users.cse.umn.edu/~mfazzini/publications/2020_mobilesoft-tool_fazzini.pdf) 进一步把旧版一组方法到新版一组方法形式化为 API 使用变化映射 `[m_1,...,m_p] → [m'_1,...,m'_q]`，明确容纳多对多与一对多迁移；例如把单个旧调用替换成两个新版调用。工具自动搜索跨项目迁移例、提取与 API 变化相关的抽象语法树编辑、泛化和排序补丁，再用差分测试验证。因此，“把旧工具调用子序列换成新版子序列”不是 v008 独有的结构。

### 4.5 GUPPY：大语言模型迁移 + 两版本测试 + 迭代修复

一级来源：[Automated Update of Android Deprecated API Usages with Large Language Models（GUPPY）](https://arxiv.org/abs/2411.04387)。

GUPPY 接收旧调用、弃用签名、弃用 API 级别与推荐替代签名，用 GPT-4 生成兼容旧/新 API 级别的调用；再由 GPT-4 生成 Robolectric 测试，在旧、新 API 级别都执行；任一版本失败时把失败信息反馈给 GPT-4，迭代修复 API 使用或测试，直到通过或达到预算。

这是对“让大语言模型迁移调用，用跨版本试验反证并迭代”的近乎逐项碰撞。它的限制是 Android 代码级弃用迁移，测试也由同一大语言模型生成，论文原文承认存在测试通过但更新仍不完整的情况；没有多工具长程计划或独立的下游任务判据。尽管如此，宽口径 v008 若只是把代码换成技能文本，很难成立。

### 4.6 签名差分与迁移 DSL

一级来源：[Characterization and Automatic Update of Deprecated Machine-Learning API Usages（MLCatchUp）](https://arxiv.org/abs/2011.04962)。

MLCatchUp 比较旧/新 API 签名，自动推断迁移 DSL，覆盖参数移除/重命名、位置参数转关键字参数、方法重命名、参数新增、类型变化等。它不擅长算术变换与一对多映射。由此可得一个很强的廉价基线：所有结构性可解变化先由签名差分/规则处理，研究方法只在非双射、上下文相关或行为语义改变上计贡献。

### 4.7 REST API 差分回归测试

一级来源：[Differential Regression Testing for REST APIs（ISSTA 2020）](https://conf.researchr.org/details/issta-2020/issta-2020-papers/21/Differential-Regression-Testing-for-REST-APIs)。

该工作建立客户端版本 `c_i` / 服务版本 `s_j` 的二维矩阵，用 RESTler 从 OpenAPI 生成有状态 HTTP 请求序列，比较跨版本响应，分别检测规范回归和服务回归，并处理响应噪声、乱序与非确定性。它只检测破坏性变化，不合成迁移；也明确不能以未发现差异证明无回归。v008 的“差分试验”不是新贡献，可能的新计算只能位于差分发现之后的计划局部化与迁移综合。

### 4.8 EVOL Migrators：类型无关演化模式与稳定客户端生成

一级来源：[Reducing the Impact of Breaking Changes to Web Service Clients During Web API Evolution（MOBILESoft 2023）](https://conf.researchr.org/details/mobilesoft-2023/mobilesoft-2023-research-track/4/Reducing-the-Impact-of-Breaking-Changes-to-Web-Service-Clients-During-Web-API)。

EVOL 以 Web API 类型无关的演化模式分类并解决 breaking changes，从 OpenAPI 规范或 EVOL 框架服务自动生成 migration guide，再由资源型/RPC 型 Migrator 生成稳定的 Swift 客户端库；无法自动解决的变化进入预定义人工扩展点。它对 v008 的杀伤集中在“结构模式 → 迁移指南/wrapper → 对客户端隐藏版本差异”这一层：若工具/API 版本差异可以被稳定客户端或兼容层吸收，完全没有必要迁移智能体计划。v008 只能在 EVOL/签名差分不能解决的行为语义、上下文依赖和非平凡状态变化上主张贡献。

## 5. 智能体技能、工具描述与模式漂移：另一侧碰撞

### 5.1 SkillRevise：执行证据驱动的技能修订

一级来源：[SkillRevise: Improving LLM-Authored Agent Skills via Trace-Conditioned Skill Revision](https://arxiv.org/abs/2606.01139)，[官方代码库](https://github.com/xuansenpa1/skillrevise)。

精确计算：从初始技能开始执行任务；诊断验证器可见失败；从一般修复记忆中检索并绑定原则；以执行锚点和证据到编辑的链路修订技能；重新执行；在有限预算内返回首个通过者或按经验效用回退到最优版本。它迁移/修订的是可复用技能资产，而非单次轨迹。

SkillRevise 没有显式研究 API 版本迁移，但直接吃掉“旧技能失败 → 读执行反馈 → 改技能 → 重跑验证器”的智能体侧贡献。

### 5.2 REST API 作为大语言模型工具的测试与适配

一级来源：[A Framework for Testing and Adapting REST APIs as LLM Tools](https://arxiv.org/abs/2504.15546)。

该框架从 OpenAPI 生成 Python 工具及输入/输出模式，枚举必选/可选约束测试；构造工具依赖图，以前序调用结果填充后续参数；直接执行 Python 工具作为事实基准，再把同一测试转成自然语言交给 ReAct 智能体，比较工具调用与响应处理，并据输入误解、输出处理、模式不匹配等错误给出适配建议。它不是跨版本迁移，但已经提供“工具行为测试 + 依赖链 + 智能体执行差异 + 接口适配”整套外围。

### 5.3 PLAY2PROMPT 与工具描述重写

一级来源：[PLAY2PROMPT: Zero-shot Tool Instruction Optimization for LLM Agents via Tool Play](https://arxiv.org/abs/2503.14432)，[官方代码库](https://github.com/wfangtw/play2prompt)。

PLAY2PROMPT 让模型主动试用每个工具，通过迭代试错观察输入/输出行为，再改进工具文档并生成用法示例，无需标注数据。它会杀死“探测新版 API 后补文档/示例，让智能体重新规划”的变体。

一级来源：[Learning to Rewrite Tool Descriptions for Reliable LLM-Agent Tool Use（Trace-Free+）](https://arxiv.org/abs/2602.20426)。

Trace-Free+ 把自然语言描述和参数模式视作可优化的工具接口，通过从有轨迹监督逐步过渡到无轨迹部署的课程学习，学习可迁移到未见工具的描述重写器。它不做版本迁移，但意味着“更好地描述新模式”已有强学习式基线。

### 5.4 受控智能体模式漂移基准

一级论文内容（作者接受稿镜像，附 IEEE DOI）：[Benchmarking Reference-Free LLM Agent Robustness Under Schema, Policy, and Toolset Drift](https://www.researchgate.net/publication/405178151_Benchmarking_Reference-Free_LLM_Agent_Robustness_Under_Schema_Policy_and_Toolset_Drift)，[DOI 10.1109/ACCESS.2026.3696096](https://doi.org/10.1109/ACCESS.2026.3696096)。

该工作基于 τ²-bench retail 注入三类受控漂移：参数键重命名、工具名重映射、首步策略前置；对照静态、盲重放、规则修复，并用上游环境最终状态而非轨迹一致性评分。规则层对已知模式/工具映射做确定性逆变换。论文明确把贡献定位为诊断协议而非新迁移算法，并把类型变化、参数移除、多步重排、部分弃用/回退列为未覆盖扩展。

它对 v008 有两重作用：一是证明旧轨迹盲重放并不等于适应，隐藏状态重建和分支选择是关键障碍；二是提供廉价的“已知双射归一化”基线。其漂移仍过于简单，不能替代真实的默认值改变、操作拆分与返回语义改变基准。

### 5.5 智能体工具协议的行为等价形式化

一级来源：[Formal Semantics for Agentic Tool Protocols: A Process Calculus Approach](https://arxiv.org/abs/2603.24747)。

该工作以进程演算形式化模式引导对话与 MCP，证明给定映射下的结构互模拟，并通过 MCP+ 类型扩展追求协议层行为等价。它不是从旧计划合成新计划，但会削弱“首次在智能体工具协议中谈行为等价/双模拟”的理论表述。v008 必须把等价对象落在任务相关的计划执行效果，而不是一般协议结构。

## 6. 辅助的代码 API 更新证据

这些工作不是最近方法核，但构成必须公平比较的“读新文档/更新模型”路线：

- [CodeUpdateArena](https://arxiv.org/abs/2407.06249)：构造库 API 更新和代码综合任务，评估把更新文档置入上下文或用新文档/示例微调；对象是模型知识更新，不是旧计划资产迁移。
- [CodeSync（ICML 2025）](https://proceedings.mlr.press/v267/ke25a.html)：以真实 Python 库 API 更新评测代码大语言模型的更新感知能力；对象仍是代码生成/训练。
- [ReCode](https://arxiv.org/abs/2506.20495)：用迁移数据与规则奖励强化学习 API 版本迁移；不是对单个既有智能体技能做黑盒行为适配。

它们使“让大语言模型读新文档后重新生成”成为不可省略的基线，而不是弱对照。

## 7. 最危险碰撞：不是一篇，而是三段式夹击

宽口径候选最危险的碰撞是以下组合：

1. **迁移综合段**：Sprout / M³ / APIFix / AppEvolve 已覆盖语义建模、拆分合并、输出导向综合、样例补丁与差分验证；GUPPY 更进一步把大语言模型、两版本执行和迭代修复组合起来。
2. **智能体资产修订段**：SkillRevise 已把执行失败、诊断、证据锚定编辑、重执行和效用选择用于技能资产；EvoC2F 已把计划中间表示、技能挖掘、测试、回归和版本化部署连成体系。
3. **接口探测/描述段**：PLAY2PROMPT、Trace-Free+ 与 REST-as-tools 框架已覆盖工具试用、输入输出行为发现、文档/模式改进和智能体级测试。

因此，下列流水线高度可能被评价为现有模块拼接：

`检测旧技能在新版失败 → 比较模式 → 试用新版工具 → 让大语言模型改技能/文档 → 在旧/新版重跑 → 保留通过版本`

即使无人以完全相同名字发表过，计算增量也可能只剩工程组合，不足以支撑方法论文。

## 8. 可能存活的最窄计算：下游延续等价的局部适配器综合

本次检索后仍可暂留、但尚未通过完整新颖性审计的缝隙是：

### 8.1 对象与等价定义

既有工具计划不同于普通客户端代码：工具响应会进入大语言模型上下文，决定下一分支、实体绑定和后续调用。原始 JSON 相等不是必要条件，最终任务一次通过也不足以定位迁移是否正确。

可把目标定义为**目标条件化的下游延续等价**：对旧计划片段 `p_old` 与候选新版片段 `p_new`，在成对、可复位的环境状态和任务条件下，不要求原始响应字段一致，而要求它们诱导的任务相关充分状态、合法后续动作集合或下游分支分布保持在容许差异内。

### 8.2 最窄新计算

一个足够具体的候选核可包含四个不可拆组件：

1. **配对分叉执行**：从同一可复位快照分别运行旧、新工具片段；对不可逆副作用只在模拟器、影子环境或具补偿事务的路径运行。
2. **下游切片**：从历史成功计划中识别哪些返回字段/状态差异实际影响后续实体绑定、分支谓词与调用参数，形成任务条件化观察投影，而非全响应比较。
3. **反例引导局部综合**：以参数映射、返回适配、常量/default 显式化、单调用替换为子序列等算子，综合最小新版片段；对能区分候选的测试状态主动生成反例并继续局部化。
4. **可拒绝判定**：当效果不可观察、旧新环境不可配对、存在不可补偿副作用或多个候选在现有测试下不可辨识时，拒绝迁移并回退到重新规划/人工确认。

这与现有工作的最小差别是：

- Sprout 保持静态程序的 API 行为树；M³ 保持采样输入输出语义；
- GUPPY 用同源生成的代码测试验证双版本兼容；
- SkillRevise 以最终验证器效用修订技能；
- REST 差分测试只发现服务/规范回归；
- EvoC2F 验证技能与契约但没有推断旧新接口对应；

而该核直接把“旧工具响应经下游智能体消费后会发生什么”作为迁移等价对象，并据此综合最小局部适配器/子序列。

### 8.3 必须承认的风险

这是检索后保留的假设，不是已经证明的新颖点。它可能退化为一般程序切片/观察等价，或被一篇未命中的计划修复论文覆盖。尤其需要进一步检索 `continuation equivalence`、`agent trajectory repair under tool drift`、`counterexample-guided workflow migration`、`goal-conditioned observational equivalence` 等术语及其引用链。

## 9. 公平基线与最小实验压力

若主研究者继续实现，至少应与下列等预算基线比较：

1. **新文档重新规划**：同一大语言模型获得完整新版文档和示例，从头规划。
2. **确定性模式归一化**：参数/工具重命名的双射 manifest、OpenAPI 差分、显式默认值规则。
3. **GUPPY 式修复**：让大语言模型改写旧计划，按执行失败迭代，预算相同。
4. **SkillRevise 式修复**：执行—诊断—技能编辑—重执行，使用同一最终验证器。
5. **PLAY2PROMPT 式接口增强后重规划**：先探测新版工具并补文档/例子，再执行。
6. **完整轨迹重放与局部重放**：验证迁移收益是否只是保留了更多旧动作。
7. **预言机迁移映射**：用于拆分“映射发现”和“计划执行”两类误差，而不是作为可部署方法。

变化集不能只放键重命名。最少应包括：默认值静默改变、返回嵌套/字段语义改变、一对多操作拆分、参数需要由旧输出变换生成、状态前置条件改变，以及相同 HTTP 成功码但最终效果不同。评价依据必须与迁移生成不同源，优先使用环境最终状态、数据库状态或人写性质，而非同一大语言模型生成的测试。

## 10. Kill 条件

出现任一情况，应杀死当前方法核或降级为基准/系统论文组件，而不是继续扩写表述：

1. 找到先行工作已经从旧成功多工具计划出发，用旧/新工具配对行为试验合成新版计划片段，并把下游智能体分支/最终环境状态作为等价判据。
2. 所谓下游延续等价在实现中只等于原始响应字段相等、最终任务成功或大语言模型主观判分，没有独立计算。
3. 在同等调用/令牌/修复预算下，“完整新文档重新规划 + SkillRevise/GUPPY 式迭代”达到相同结果。
4. 主要收益来自参数/工具重命名等可由 manifest、签名差分或简单 wrapper 解决的双射变化。
5. 去掉同源测试后无法验证迁移；或者测试/等价预言器与候选生成由同一模型产生，产生系统性假阳性。
6. 无法在真实或高保真成对版本中稳定复位状态，导致跨版本差分混入环境漂移；对副作用操作又没有影子/补偿路径。
7. 方法对操作拆分、默认语义变化、返回数据变换等非平凡变化无优势，只能重写文档或提示词。
8. 提供完整新版文档/示例后收益消失，说明贡献只是知识补全而非旧计划迁移。
9. 新计算无法脱离 Sprout/M³ 的一般行为等价和 SkillRevise 的执行修订之简单串联，没有新的目标函数、搜索空间或可验证性质。
10. 找不到带成对版本、可执行旧计划、独立最终状态标签的评测路径，无法稳定测量“迁移而非重新规划”的优势。

## 11. 非权威审计结论

- **EvoC2F 核查结果**：它真实处理技能挖掘、计划编译、功能/契约/回归测试与版本化部署，但本次在可定位原文中没有核实到 API 旧版到新版的自动技能迁移或跨版本行为等价推断。
- **宽口径方向**：高度碰撞。尤其 GUPPY 已经实现“大语言模型 API 迁移 + 旧/新版本测试 + 失败迭代修复”；Sprout 与 M³ 又分别覆盖形式保证和黑盒语义/拆分合并；SkillRevise 与 EvoC2F 覆盖技能修订和版本化验证。简单组合不值得作为方法核。
- **暂存缝隙**：只保留“以任务条件化的下游智能体延续等价为目标，反例引导地综合最小新版工具片段/适配器，并可拒绝”的窄计算。当前未发现精确同构一级来源，但还需要引用链级反证与最小实验验证。
- **不可由本草案做出的决定**：是否推进 v008、是否形成正式 Candidate、是否交付或 Run-level No-Delivery，均留给主 AI 研究者。
