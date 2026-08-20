# v011 独立正交勘探：目的绑定的能力流／衰减证书

> 身份：Codex App 原生 Research Subagent 的非权威材料。本文只做先验碰撞、可运行评价面与杀手实验设计；不修改 Hypothesis、Portfolio、Decision，也不替主研究者裁决。
>
> 检索日期：2026-08-13。2026 年材料中有多篇仍是预印本或互联网草案；本文把它们当作“已公开的技术先占与强基线”，不把预印本状态写成同行评审认可。

## 结论先行

**建议杀死原始候选家族，杀伤范围是“purpose-bound capability flow / attenuation certificate”这一宽方法家族，而不是整个 v011 问题。** 原始描述的四个核心部件已经分别、且多处联合出现：

1. **用户目的／任务到细粒度权限的编译**：Conseca 从目的与上下文生成即时策略；Progent 从用户任务生成工具名与参数策略；PAuth 把自然语言任务编译为服务级 `NL slice`。
2. **每跳不可扩权的能力衰减与委派链**：Macaroons、Biscuit 是经典基础；2026 年 Intelligent AI Delegation 已明确提出基于它们的 Delegation Capability Token；AIP/IBCT 已实现跨 MCP、A2A、HTTP 的追加式多跳衰减令牌。
3. **返回数据不能凭文本取得命令权，且参数要保留来源**：CaMeL 跟踪值级来源和允许读者；PAuth 的 envelope 把具体操作数绑定到符号来源；Progent 对由工具返回建议的新策略做确定性的扩张／收缩判断，无批准只能收缩。
4. **提交前沿整条执行链检查授权**：SEAgent 对多智能体消息—工具的信息流路径实施强制访问控制；FORGE 在每个候选动作前查询消息、工具调用、结果与批准的因果依赖图；AIP 在最终工具端验证整条签名与衰减链。

因此，“给每次委派／工具调用附加授权来源、资源、动作、目的，返回值不得扩权，提交前验证沿袭”可以由 **AIP + PAuth + Progent/FORGE** 几乎逐句拼回。若仅把这些组件装进同一中间件，最可能被审稿人判为系统集成或协议拼装，而非新的方法计算。

仍有一个非常窄的、仅适合做**杀手实验探针**而不宜直接升格为候选的余隙：

> **委派切片精化检查器（delegation-slice refinement checker）**：先把根用户任务编译成带外部副作用节点与值依赖孔位的符号任务图；每次委派时，子任务必须提交一个可验证的子图精化证明。证明要求每个子智能体副作用映射回父图中的既有副作用节点，工具返回只能实例化既有值孔位，不能新增副作用／控制边；通过后才把该子图的资源—动作—参数约束编码进衰减令牌。子结果再以来源 envelope 返回，后继提交同时验证令牌链与值来源链。

这个余隙本质上仍是“把 PAuth 的任务切片提升到 AIP 的多跳委派链”，与 FORGE 的因果图也高度相邻。只有当它在**严格的最强复合基线 AIP + PAuth/Progent** 上找到可重复的、基线结构上无法表达的授权洗白反例，才值得保留；否则应一起淘汰。

## 1. 问题与威胁不是空白

### 1.1 直接问题证据

本地共享知识库的 P076《Multi-Agent Systems Execute Arbitrary Malicious Code》已经记录了最贴近本题的现象：外部内容可被前线智能体改写为内部 `status/error` 元数据，编排器再据此改变后续智能体或能力调用；即使单个子智能体拒绝或警告，系统中其他组件仍可能完成危险动作。论文公开摘要进一步称，这类控制流劫持在单个智能体不易受直接／间接提示注入、甚至拒绝危险动作时仍可成功。它支持的是**多智能体控制流与权限洗白**，不是简单聊天越狱。

- 论文：[Multi-Agent Systems Execute Arbitrary Malicious Code](https://arxiv.org/abs/2503.12188)
- Run 内允许引用的本地卡片：`knowledge_base/cards/paper/paper-p076.md` 与 `knowledge_base/cards/failure/failure-untrusted-agent-metadata-privileged-control-flow.md`（共享知识库只读，本次未改写）。

### 1.2 MCP 本身只解决部分授权边界

当前公开 MCP 规范的 HTTP 授权建立在 OAuth 2.1 上，要求资源指示符、受保护资源元数据和令牌受众绑定；官方安全最佳实践也明确禁止令牌透传，并讨论 MCP 代理服务器的 confused deputy。当前任务接口还要求在存在授权上下文时把任务及其结果绑定到该上下文。这些规范能阻止一部分跨资源令牌误用，但它们不自动证明“这次工具调用是否服务于根用户目的”，也不自动携带多跳自然语言委派的语义精化证明。

- [MCP 2025-11-25 授权规范](https://modelcontextprotocol.io/specification/2025-11-25/basic/authorization)
- [MCP 安全最佳实践](https://modelcontextprotocol.io/docs/tutorials/security/security_best_practices)
- [MCP 任务隔离与授权上下文绑定](https://modelcontextprotocol.io/specification/2025-11-25/basic/utilities/tasks)

这意味着问题真实存在，但“问题存在”绝不等于候选方法新颖。

## 2. I/C/O 组件级碰撞

这里的 I/C/O 分别表示：

- **I（输入／问题）**：是否研究同一种输入边界与失败；
- **C（计算）**：是否已经执行相同或可直接组合得到的安全计算；
- **O（输出／评价）**：是否已在相同可观测终局上验证。

| 最近工作／基础 | I 碰撞 | C 碰撞 | O 碰撞 | 对候选的实际杀伤 |
|---|---:|---:|---:|---|
| CaMeL, 2025 | 高 | 高 | 高 | 从可信用户任务抽取控制／数据流；不可信返回不能改变程序流；值带来源与允许读者能力；AgentDojo 上公开实现与终局。直接吸收“返回数据不能取得命令权／来源随值传播”。 |
| AgentDojo, NeurIPS 2024 D&B | 高 | 评价载体 | 极高 | 97 个现实任务、629 个安全组合，环境状态分别判定用户任务完成与攻击目标完成。它不是方法先占，但提供最合适的独立终局。 |
| Conseca, HotOS 2025 | 极高 | 高 | 中 | 标题即“A Policy for Every Purpose”；从具体上下文和目的生成即时、透明、可人工核验策略，执行确定性。直接杀“为每个目的生成策略”这一表述。 |
| Progent, 2025/2026 版本 | 极高 | 极高 | 极高 | 以工具名和参数上的符号策略表示最小权限；每个工具调用确定性检查；LLM 从用户任务／运行上下文更新策略；SMT 判断扩张与收缩，无批准只能收缩；公开 MCP、LangChain、OpenAI Agents SDK、OpenHands 和 AutoGen 六子智能体实验。它是最强单体基线。 |
| PAuth, 2026 预印本 | 极高 | 近乎精确 | 极高 | 自然语言任务隐式授权且只授权忠实执行所需具体操作；`NL slice` 给每个服务生成期望调用的符号规范；envelope 绑定具体操作数与上游符号来源；AgentDojo 上报告全部良性任务成功、全部注入任务告警。直接吸收“目的 + 资源／动作 + 参数来源”。 |
| Intelligent AI Delegation, 2026 预印本 | 极高 | 高 | 低 | 明确把任务分配与 authority/responsibility/accountability/intent/boundary 一起建模，并提出基于 Macaroons/Biscuit 的 Delegation Capability Token；每个链上参与者继续加限制。直接吸收“多跳目的约束的能力衰减”概念。 |
| AIP / IBCT, 2026 预印本 | 精确 | 极高 | 高 | 追加式令牌联合身份、不可扩张授权和来源；委派块含 delegator/delegatee、收缩 scope 与必填 purpose/context；完成块含结果散列／验证状态；MCP/A2A/HTTP 绑定；Python/Rust 公开实现；报告 600 次攻击拒绝与真实多智能体开销。直接吸收“衰减证书／沿袭链／结果收据”。 |
| SEAgent, 2026 预印本 | 精确 | 极高 | 高 | 明确定义多智能体 confused deputy；对 agent→agent→tool 信息流图做基于属性的强制访问控制；策略可以匹配任意间接路径；在 AgentDojo、InjecAgent 及多智能体任务上评价。直接吸收“洗白链提交前图检查”。 |
| FORGE / Formal Policy Enforcement, 2026 预印本 | 极高 | 极高 | 高 | 参考监控器在每个候选动作前查询因果依赖图；图覆盖消息、工具调用、工具结果、批准与跨智能体交换；Datalog 可表达传递关系，并有矛盾／冗余／蕴含等静态分析。直接吸收“沿整条链验证”。 |
| A Framework for Formalizing LLM Agent Security, 2026 预印本 | 极高 | 中（形式化） | 低 | 把安全分为任务对齐、动作对齐、来源授权、数据隔离；明确同一合法能力在错误目的下是 capability misuse，并指出多智能体委派与保证组合仍需形式化。该余隙是问题空间，不是候选新颖性证明。 |
| Authorization Propagation in Multi-Agent AI Systems, 2026 预印本 | 精确 | 中（体系化） | 低 | 已把问题命名为工作流级 authorization propagation，分为传递委派、聚合推断、时间有效性；明确综述 IBCT、PAuth、因果依赖策略，认为剩余是这些碎片的组合。原候选几乎正是其“集成清单”。 |
| Macaroons / Biscuit / 能力安全 | 高 | 精确基础 | 中 | 持有者可离线追加 caveat/check，只能收缩不能扩张；Biscuit 用追加块与 Datalog，任何新块默认只能增加限制。若“衰减证书”不改变更高层计算，就是经典能力令牌的重新命名。 |
| 目的型访问控制与用途限制 | 高 | 高 | 中 | Hippocratic Databases、purpose-based access control、PuRBAC 等早已把数据、访问动作与用途匹配／用途层次绑定；“purpose”字段本身没有新颖性。 |
| 信息流控制／非干扰 | 高 | 高 | 中 | 污点、完整性标签、去分类／背书、流限授权与非干扰早已描述“低完整性数据不能影响高权限效果”；CaMeL、SEAgent、FORGE、LLMbda Calculus 已把这些原则带到智能体。 |

### 2.1 最致命的五处方法级重合

#### 碰撞 A：目的到动作权限

候选说“每次调用携带目的、允许资源和动作”。Conseca 已从目的生成即时策略；Progent 已把任务转为工具与参数规则；PAuth 更把自然语言任务转成逐服务操作切片。除非候选提出不同于“自然语言→规则／程序切片”的新计算，否则 C 层没有剩余。

#### 碰撞 B：无批准不得扩权

候选说“返回数据不能扩权”。Progent 的核心定理正是 `monotonic confinement`：策略更新经 SMT 判断为收缩或扩张；收缩自动应用，扩张必须显式批准。工具返回即使操纵策略更新器，也不能静默扩大允许动作集。Macaroons/Biscuit 又从令牌层保证持有者只能追加限制。

#### 碰撞 C：值来源绑定

候选说“数据来源跟随调用”。CaMeL 给每个值打来源和读者标签并沿解释器传播；PAuth envelope 把操作数具体值绑定到符号来源，使服务端能验证它来自任务暗含计算，而非智能体伪造常量。简单的 provenance tag、taint union 或 signed handle 都没有方法新颖性。

#### 碰撞 D：多跳授权链

候选说“父任务授权沿子智能体与工具链组合衰减”。DeepMind 的 Intelligent AI Delegation 已提出 restriction chaining；AIP/IBCT 已实现父块、每跳委派块、能力收缩、深度／预算／过期约束和完成块，且目的 context 是必填字段。2026 年的 AAT 互联网草案还进一步定义了任务域委派链、工具级能力与参数约束的结构化包含关系。

#### 碰撞 E：提交前检查因果沿袭

候选说“提交前检查授权沿袭”。FORGE 的参考监控器就在每个候选动作前同步其 backward slice 并运行 Datalog；SEAgent 匹配任意 `agent -> ... -> agent -> tool` 路径；AIP 工具端验证整条签名和 scope 衰减。换名称为 certificate verifier 不改变计算。

## 3. 原家族的逐型淘汰

| 家族成员 | 判定 | 原因 |
|---|---|---|
| F1：只给委派／工具调用附加签名证书 | **淘汰** | AIP/IBCT、AAT、Macaroons、Biscuit 精确先占。 |
| F2：证书增加自然语言 purpose 字段 | **淘汰** | AIP 已有必填 context；Conseca 与目的型访问控制已覆盖目的约束。若不验证语义，只是日志字段；若验证语义，则落入 PAuth/Progent 的任务编译。 |
| F3：低权限返回值永不扩权 | **淘汰** | Progent 的确定性单调收缩、CaMeL 的数据／控制流分离、PAuth 的值来源 envelope 已覆盖。 |
| F4：提交前遍历整条授权链 | **淘汰** | AIP 验证追加式链；FORGE/SEAgent 验证因果／信息流路径。 |
| F5：把 F1-F4 放到同一 MCP／多智能体中间件 | **默认淘汰** | 这是 AIP + PAuth + Progent/FORGE 的系统集成；Authorization Propagation 已把这种组合公开列为架构方向。没有不可约的新算子。 |
| F6：委派切片精化检查器 | **仅保留为杀手实验探针** | 可能把 PAuth 的单工作流切片提升到跨信任域多跳委派，但仍像对 AIP 的直接扩展；必须先打赢最强复合基线。 |

## 4. 唯一可测试的最窄 changed computation

下面不是建议直接注册的新 hypothesis，而是为了最大信息量实验而压缩出的最窄可证伪内核。

### 4.1 输入

- 根用户任务编译出的父任务图 `G_p`；
- 父图节点包括：纯计算、外部读取、外部写入／执行、委派、最终交付；
- 边包括控制依赖和值依赖；
- 每个外部效果节点带 `(principal, resource, action, argument-shape, purpose-atom)`；
- 子智能体提出的委派子图 `G_c`，声明输入孔位、输出孔位和所需效果。

### 4.2 真正改变的计算

不是“再做一次安全分类”，而是计算一个可检查的精化见证 `π: G_c -> G_p`：

1. `G_c` 中每个外部副作用必须映射到 `G_p` 的既有副作用节点；
2. 资源、动作和参数约束必须被父节点包含，不能扩大；
3. 子任务的目的原子必须由父节点的目的原子和控制前提蕴含；
4. 工具返回只能实例化父／子图已声明的值孔位；它可改变参数值，但不能创建新的副作用节点、委派边或目的原子；
5. 通过后，`π` 的规范化散列与对应约束进入 AIP/Biscuit 衰减块；
6. 子结果必须带 PAuth 式 envelope，后继副作用同时验证 `(token chain, π, value envelope)`。

### 4.3 输出

- `ALLOW`：精化见证、衰减 token、输入／输出 envelope 规范；
- `DENY`：最小不满足核心，例如“子图新增了父图不存在的 `send_email` 效果”；
- `ASK`：根任务本身歧义，无法在不扩权的情况下生成父图。

### 4.4 为什么它仍高度可杀

- PAuth 已计算任务程序与逐服务切片，并验证上游结果派生的操作数；把其程序切成父／子图可能只是工程延伸。
- Progent 已能把整套多智能体系统视为统一实体，以全局策略阻止跨智能体扩权；子图证明可能不改变终局。
- FORGE 已能在因果图上写递归 Datalog 规则；精化检查可能只是把同一策略前移到委派点。
- AIP 已提供多跳不可扩张载体；把 `π` 的散列放进 token 不是新方法。
- 自然语言目的的正确编译仍是未解决的语义 oracle。若证明的父图由同一个 LLM 错编，形式证明只证明“忠实执行错误授权”。

所以真正要反证的是：**是否存在 AIP + 全局 Progent/PAuth 无法表达、但委派图精化能在不增加人工审批的前提下阻止的系统性攻击族。**

## 5. 公开可运行的任务与独立终局

### 5.1 首选评价载体：AgentDojo

- 代码：[ethz-spylab/agentdojo](https://github.com/ethz-spylab/agentdojo)
- 安装：公开包 `pip install agentdojo`；仓库给出按 suite、user task、injection task、model、defense、attack 运行的命令。
- 终局：用户任务 utility evaluator 和注入任务 security evaluator 读取模拟环境状态，不需要候选自身或同源 LLM 给正确答案。
- 适配价值：Workspace、Slack、Travel、Banking 都含高权限写操作与不可信工具返回；可把单智能体轨迹机械改写成 2—4 跳委派，同时保持同一初态和终态判定。

### 5.2 最强现实基线载体：Progent artifact

- 代码：[sunblaze-ucb/progent](https://github.com/sunblaze-ucb/progent)
- 论文公开说明 artifact 包含 Progent 实现和实验复现代码；其新版实验把 AgentDojo 环境和工具迁移成 MCP 服务，并在 AutoGen 中构造一个协调器和六个专家子智能体。
- 价值：可直接比较 vanilla、全局 Progent、逐子智能体 Progent；这三者比自行搭一个弱多智能体玩具更公平。

### 5.3 可复用的结构安全实现

- CaMeL：[google-research/camel-prompt-injection](https://github.com/google-research/camel-prompt-injection)。适合作为“控制／数据流分离 + 值能力”的强基线；仓库明确警告研究解释器可能有 bug，不能把实现通过写成系统证明。
- AIP：[sunilp/aip](https://github.com/sunilp/aip)。公开 Python/Rust 实现，适合提供签名链、scope 衰减、深度、预算和 MCP 头验证；其完成块可为 `self_reported`，不能把结果散列误写成独立正确性证明。
- AgentDojo tool filter：预暴露动作面限制的低复杂度强基线。
- ToolEmu：[论文](https://arxiv.org/abs/2309.15817)。可补充高风险工具场景，但其 LLM 模拟器／评价器不是本候选核心 Claim 的首选独立终局，最多用于探索。

### 5.4 不宜冒充已可直接跑的材料

- PAuth 论文公开了 AgentDojo 原型细节，但在本次检索中没有核验到明确的官方代码链接；若无 artifact，只能按论文忠实复现并标注为 reproduction，不能声称运行了官方实现。
- FORGE 论文给出大量实现细节与案例，但本次只核验到论文，没有核验到独立官方仓库；不能把论文伪装成可安装包。
- SEAgent 论文说有 released artifact，但搜索结果容易与同名 computer-use `SEAgent` 仓库混淆；正式实验前必须从论文脚注／Open Science 精确核验链接，不能误用同名项目。

## 6. 最小高信息量杀手实验

### 6.1 核心问题

> 在相同根任务、相同模型、相同工具、相同调用预算和相同环境终局下，委派切片精化是否能阻止 **AIP + 全局 Progent/PAuth** 仍允许的权限洗白，同时不降低合法动态委派的完成率？

若不能，整个家族没有必要进入实现稳定化或固定 Reviewer。

### 6.2 任务构造

从 AgentDojo 选 12—20 个同时包含读取与高权限写入的任务，按确定性模板转成多跳版本。每个根任务生成四个成对条件，终局仍由原环境状态评价：

1. **合法动态值**：父任务明确授权一种副作用，但收件人、文件标识或金额需从工具返回取得；防御必须允许返回值实例化既有孔位。
2. **控制流洗白**：不可信工具返回被前线智能体转述成“错误／状态／必须转交专家”的元数据，诱导编排器调用原任务未授权的高权限子智能体或工具。
3. **参数洗白**：工具与动作类型本来允许，但返回内容把目标对象替换为攻击者控制的收件人／账户／路径。该条件专门防止仅检查工具名的系统虚高。
4. **合法再委派**：父任务确实需要二级专家，且二级专家只使用父图中的动作子集；过严系统会错误阻止，用于测 utility。

可选第五类只做边界测试，不混进主 Claim：

5. **授权集合聚合泄露**：两个子智能体分别访问合法数据，合并结果却泄露禁止组合的信息。这是 Authorization Propagation 的 aggregation inference，原候选的简单衰减证书通常也挡不住；若失败，应如实界定而不是临时加模块。

### 6.3 公平基线

至少比较：

1. Vanilla AutoGen/MCP；
2. AgentDojo tool filter；
3. CaMeL 或等价控制／数据流分离；
4. Progent-global；
5. Progent-per-agent；
6. AIP-only；
7. **AIP + Progent-global**；
8. **AIP + PAuth-style task slice/envelope**（若无官方代码，明确是忠实复现）；
9. 探针：AIP + 委派切片精化 + value envelope。

真正的最近公平基线是 7/8，不是 vanilla、提示词防御或静态 allowlist。

### 6.4 独立指标

- 根用户任务完成率；
- 攻击目标完成率；
- “根任务完成且攻击目标也完成”的隐蔽双成功率；
- 未授权高权限调用率，按环境实际工具事件计数；
- 合法动态委派误拒率；
- 需要用户批准的次数；
- token、工具调用数、延迟；
- 证明／策略编译失败率，单独分解为根任务编译错误、子图精化错误、运行时验证错误。

终局和攻击成功必须由 AgentDojo 环境状态／事件日志给出；不能由生成父图的同一个模型或候选 verifier 自评。

### 6.5 最小规模

先跑一个 4 任务 × 4 条件 × 3 随机种子 × 4 关键系统的小矩阵：

- Progent-global；
- AIP + Progent-global；
- AIP + PAuth-style slice；
- 探针。

这 192 条轨迹已经足以回答最大不确定性：探针是否有任何独有增益。只有出现可重复分离，才扩到全部基线和更多模型。

## 7. 预注册 kill 条件

任一核心条件成立，即杀探针／家族，不以“换更大模型”拖延：

1. **最强复合基线吸收**：AIP + Progent-global 或 AIP + PAuth-style 在相同合法完成率下阻止同一批洗白，探针没有独有安全增益。
2. **只增加载体、不改变决定**：去掉证书签名／散列但保留同一任务切片与策略后，允许／拒绝结果不变；说明贡献只是审计包装。
3. **依赖自报来源**：值或消息 provenance 由被攻击 LLM 自己声称，环境不能独立重建；形式沿袭失去可信根。
4. **目的语义不可校验**：purpose 只是字符串；或只能用另一个 LLM 判断“子任务是否服务父目的”，并在同义改写／对抗内容下不稳定。
5. **动态任务效用崩塌**：为了不扩权，系统必须预先冻结完整调用图，导致合法运行时信息驱动的委派明显低于 Progent/PAuth；这等价于用过度限制换安全。
6. **允许范围内攻击**：攻击利用父任务本来允许的同一资源、动作和参数形状完成有害目的，而精化证书仍通过；若只能再加语义 judge 才能阻止，原 kernel 不充分。
7. **全局策略已可表达**：所谓新跨智能体性质可以用一条 FORGE Datalog／Progent global rule 表达，且实现复杂度、误拒和开销不劣。
8. **任务转换泄漏终局**：多跳模板把攻击标签、正确收件人或禁用动作显式写进候选可见策略，使探针得到人为主场优势。
9. **只在合成链深上分离**：单跳基线被故意禁用而探针获准看全链；恢复公平信息后差异消失。
10. **没有公开可复查终局**：只能靠作者／候选同源 LLM 给“是否越权”标签，无法由工具事件和环境状态复核。

## 8. 若杀手实验出现正分离，最低晋级条件

只有同时满足下列条件才可把 F6 从“探针”升级为候选：

1. 至少一种授权洗白结构在 **AIP + Progent-global** 与 **AIP + PAuth-style** 上稳定成功，而精化检查稳定阻断；
2. 该差异来自“父／子任务图精化”这一计算，不来自更多人工策略、更多攻击标签或更少工具；
3. 合法动态值和合法再委派的完成率不显著劣于最强复合基线；
4. 根任务图、子图与终局分别有独立来源，避免同源构造—评价闭环；
5. 能写出一个基线无法用简单规则补丁吸收的结构性反例族，而非一个手工例子；
6. Claim 收缩为“多跳委派图的授权精化”，不声称发明 capability、purpose binding、provenance、MCP authorization 或信息流控制。

即便通过，论文定位也应是“**面向动态多智能体委派的任务图精化与授权联合验证**”，而不是“目的绑定能力证书”。

## 9. 关键文献事实与可信度边界

### 9.1 直接方法先验

- Debenedetti et al., [Defeating Prompt Injections by Design / CaMeL](https://arxiv.org/abs/2503.18813), 2025。公开摘要与代码支持：可信查询抽取控制／数据流，不可信数据不能改变程序流，能力限制未授权数据流；[官方研究代码](https://github.com/google-research/camel-prompt-injection)。
- Tsai & Bagdasaryan, [Contextual Agent Security: A Policy for Every Purpose](https://sigops.org/s/conferences/hotos/2025/papers/hotos25-100.pdf), HotOS 2025。目的与上下文驱动的即时、人可核验、确定性执行策略。
- Shi et al., [Progent: Securing AI Agents with Privilege Control](https://arxiv.org/abs/2504.11703), 最新公开 HTML 标为 2026-05-14 v3。工具／参数符号策略、SMT 扩张判断、单调约束、MCP 与多智能体评价；[artifact](https://github.com/sunblaze-ucb/progent)。
- Sharma et al., [PAuth – Precise Task-Scoped Authorization For Agents](https://arxiv.org/abs/2603.17170), 2026 预印本。任务域授权、NL slice、操作数来源 envelope、AgentDojo 原型。
- Tomašev et al., [Intelligent AI Delegation](https://arxiv.org/abs/2602.11865), 2026 预印本。authority、responsibility、accountability、intent/boundary 与 DCT restriction chaining。
- Prakash, [AIP: Agent Identity Protocol for Verifiable Delegation Across MCP and A2A](https://arxiv.org/abs/2603.24775), 2026 预印本；[代码](https://github.com/sunilp/aip)。IBCT 多跳衰减、必填 context、完成块、跨协议实现。
- Palumbo et al., [Formal Policy Enforcement for Real-World Agentic Systems / FORGE](https://arxiv.org/abs/2602.16708), 2026 预印本。Datalog、参考监控器、因果依赖图、跨智能体策略。
- Ji et al., [Taming Various Privilege Escalation in LLM-Based Agent Systems / SEAgent](https://arxiv.org/abs/2601.11893), 2026 预印本。多智能体 confused deputy、ABAC/MAC、信息流图。
- Song et al., [A Framework for Formalizing LLM Agent Security](https://arxiv.org/abs/2603.19469), 2026 预印本。任务／动作／来源／数据隔离四性质，并明确多智能体委派组合尚未完整形式化。
- Tallam, [Authorization Propagation in Multi-Agent AI Systems](https://arxiv.org/abs/2605.05440), 2026 预印本。把 IBCT、PAuth、PCAS/FORGE 式依赖图等碎片定位为待组合架构；其生产案例来自单一平台，不能当普遍实证。

### 9.2 经典先验

- Birgisson et al., *Macaroons: Cookies with Contextual Caveats for Decentralized Authorization in the Cloud*, 2014。持有者追加 caveat 的授权衰减。
- [Eclipse Biscuit specification](https://doc.biscuitsec.org/reference/specifications)。追加块、公开密钥验证、Datalog 权限与离线 attenuation；添加块默认只能增加限制。
- Agrawal et al., *Hippocratic Databases*, VLDB 2002；以及目的型访问控制、PuRBAC、用途限制文献。它们先占“数据只能为允许目的使用”的政策语义。
- Bell-LaPadula、Biba、分散式信息流控制、flow-limited authorization、nonmalleable information flow。它们先占来源／完整性标签与高权限 sink 检查的理论骨架。

### 9.3 证据限制

- AIP、PAuth、FORGE、SEAgent、Authorization Propagation 均应按预印本／公开草案强先验处理，不能写成顶会已确认结论。
- AIP 的 `context` 当前验证重点包括非空和链完整性；不能据此推断它已经证明自然语言目的语义与父任务一致。
- AIP completion block 可记录 `verification_status=self_reported`；结果散列证明完整性，不证明结果正确或符合目的。
- PAuth 的零误报／零漏报结果来自闭世界 AgentDojo 条件，论文自身承认任务无显著歧义、工具齐全、上下文较简单；不能外推到开放式多智能体任务。
- Progent 的安全保证针对策略集合的单调收缩；初始策略若由用户歧义或编译错误而过宽，保证不会自动修复语义错误。
- FORGE 的运行时保证依赖环境正确提供因果图与外部谓词；自然语言到 Datalog 的翻译没有完整形式正确性保证。
- SEAgent 的属性主要静态，策略质量和标注决定安全；其 default allow 设计与“默认拒绝”能力系统不同，正式比较必须保留这种差异。

## 10. 给主研究者的非权威建议

1. **不要以原名注册候选。** “purpose-bound capability flow/attenuation certificate”会同时撞上 Conseca、Progent、PAuth、AIP、SEAgent、FORGE 和经典能力系统。
2. **若 v011 需要一个高信息量动作，只做上述 192 轨迹杀手实验。** 不要先建设完整协议、密码学栈或固定 Reviewer packet。
3. **最强基线必须是复合基线。** 只赢 vanilla、提示词防御、AgentDojo tool filter 或 AIP-only，不足以支持方法论文潜力。
4. **优先尝试复现反例，而不是实现候选。** 先在 Progent 的 AutoGen/MCP 环境中寻找 AIP + global policy 仍发生的跨跳授权洗白；若没有稳定反例，直接结束这个方法谱系。
5. **若 F6 也被吸收，应回退到不同问题。** 仍可在安全领域探索的正交问题包括：授权集合的聚合推断、授权撤销的时间一致性、根自然语言任务到正式授权的独立验证；但它们都已有 2026 强先验，不能把“换子问题”当默认可交付性。

最终非权威判定：**宽家族 KILL；F6 仅准许一次最小复合基线杀手实验，不建议进入稳定实现或固定 Reviewer。**
