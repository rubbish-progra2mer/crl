# P074 独立来源二读报告

## 1. 来源、边界与覆盖

- `[AUTHOR_FACT]` 本报告引用的 invocation snapshot 为 `r2-20260720-p074-a1/invocation.md`；其记录的角色是 fresh independent full-paper source checker，blinding 状态为 `procedural_blinding`，且不提供技术性文件 allowlist。
- `[AUTHOR_FACT]` canonical 路径 `knowledge_base/papers/P074_toolgate.pdf` 在本次读取时不存在；因此按 invocation 的回退规则，实际读取路径为 `knowledge_base/staging/plan05_sat_a2/P074_toolgate.pdf`，没有读取第二份 PDF。
- `[AUTHOR_FACT]` 实际读取 PDF 的 SHA-256 为 `7073bc0a27cf0f002ea4d1ef0ec3726d5c70c7e44a218e78f46d92284aba289d`，与 invocation 记录一致。
- `[AUTHOR_FACT]` PDF 共 32 个物理页；本次对物理页 1–32 全部进行了文本解析与逐页可视核验。物理页 1–32 对应论文印刷页码 9653–9684，覆盖摘要、正文、Limitations、全部参考文献及附录 A–I。
- `[AUTHOR_FACT]` 论文元数据与首页一致：题名为 *ToolGate: Contract-Grounded and Verified Tool Execution for LLMs*，发表于 Findings of ACL 2026（物理页 1，印刷页 9653）。
- `[READER_INTERPRETATION]` 解析文本与可视 PDF 的章节、公式、表格、图和页码没有发现实质冲突。可视核验尤其确认了图 1、图 2、表 1–5、算法 1、两组契约推导例子和附录 I 的公式均在页面中实际存在。正文与附录之间存在若干语义不一致，见第 7 节；这不是解析错误。

## 2. 方法究竟改变了哪一步计算

- `[AUTHOR_FACT]` ToolGate 将工具增强推理中的隐式自然语言“是否调用、是否相信返回值”改成一个显式闭环：维护 typed symbolic state `S`；检索并重排候选工具；用工具前置条件 `P_t` 在调用前过滤；执行工具；以返回值 `r_t` 和状态 `S_k` 检查后置条件 `Q_t` 与 well-formedness；仅当检查通过时才执行 `Update_t(S_k,r_t)` 并将结果注入后续推理，否则状态保持不变且结果被丢弃（物理页 3–5，§3.2–3.4，式 2–14；物理页 19，算法 1）。
- `[AUTHOR_FACT]` symbolic state 被定义为 typed key–value tuple 的集合 `Σ={(k,v,σ)}`，论文声称其中只存放已验证实体、中间结果和工具返回，并以 `S |= φ` 表示状态满足逻辑谓词（物理页 3，§3.2）。
- `[AUTHOR_FACT]` 候选工具先由 embedding Top-K 检索，再由 reranker 排序；实验默认 `K=10`，使用 Qwen3-embedding-0.6B 与 Qwen3-Reranker-0.6B（物理页 4，式 6–8；物理页 6，§4.4；物理页 15，附录 E）。前置条件指示函数将不满足 `S_k |= P_t` 的候选概率置零并重新归一化（物理页 5，式 9–10）。
- `[AUTHOR_FACT]` 后置门的接受事件为 `A_t=1` 当且仅当 `(S_k,r_t) |= Q_t` 且 `wf(r_t)`；只有 `A_t=1` 才更新状态并把结果放入 reasoning trajectory，失败时保持 `S_k`（物理页 5，式 11–12）。算法 1 进一步在失败时把该工具加入贯穿整条运行的 `T_failed`，随后尝试其他候选；没有候选成功则返回 `Fail`（物理页 19）。
- `[READER_INTERPRETATION]` 真正新增的计算并非一般意义上的定理证明器，而是“模式/谓词检查 + 受控提交”的运行时事务门：前门控制能否执行，后门控制返回值能否进入受信状态。它使状态提交可追踪，但不会自动证明工具输出在现实世界中为真。

## 3. 输入、输出、可用信息与干预时点

- `[AUTHOR_FACT]` 框架输入包括用户 query `q`、对话/上下文 `H`、工具集 `T`、当前状态 `S_k` 和 reasoning trajectory `R_k`；LLM 决定回答或产生 `<start_call_tool>`，并生成工具需求表示 `u_k`（物理页 4，式 4–7；物理页 17–18，提示词模板；物理页 19，算法 1）。
- `[AUTHOR_FACT]` 初始状态由 `InitState(q,H)` 构造；工具参数由 `GenParams(t,S_k)` 生成；工具返回为 `r_t`；最终输出为答案 `a`，无可行工具时为 `Fail`，达到最大轮数时为 `Timeout`（物理页 18–19，附录 G、算法 1）。
- `[AUTHOR_FACT]` 两个明确干预点分别是执行前的 `P_t` 检查和执行后的 `Q_t` 检查。前者在副作用发生前过滤候选，后者发生在工具已经执行之后、符号状态提交之前（物理页 5；物理页 19，算法 1 第 11–17 行）。
- `[OPEN_QUESTION]` 论文没有给出 `InitState(q,H)` 如何从自然语言提取 typed facts、如何校验这些初始 facts，或如何区分用户陈述、模型推断与外部验证事实。因而“trusted state”在第一步如何获得信任基础不清楚。
- `[OPEN_QUESTION]` `Update_t` 在形式部分被假设为确定函数，但正文没有说明实际系统如何为上万工具生成 key 映射、冲突处理、覆盖规则及全局 invariant；附录示例是手写风格的映射，不能证明实现对所有工具都完整（物理页 29–31，附录 I.1、I.6）。

## 4. 契约构造、oracle 与形式保证的边界

- `[AUTHOR_FACT]` 作者明确说 `P/Q` 不由 reasoning-time LLM 动态生成，而由工具文档与接口规范结构化抽取。`P` 来自 required parameters；`Q` 来自响应 schema 的 required fields、类型与结构。MCP-Universe 使用 MCP `inputSchema` 与 typed response interfaces（物理页 4，§3.2）。
- `[AUTHOR_FACT]` 对 ToolBench，约 25% 工具没有结构化响应 schema、只有类似 `{api_list: []}` 的默认 response example；作者将这些工具的 `Q` 设为 `True`，即不提供返回后约束（物理页 4，§3.2）。
- `[AUTHOR_FACT]` Limitations 进一步承认 ToolBench 的 response schema 是在 LLM assistance 和 expert-written in-context examples 下产生的，因此 `Q` 代表该流程暗示的“expected shape”，而非 ground-truth formal specification；部署时可在存在时改用官方 OpenAPI（物理页 9–10，Limitations）。
- `[AUTHOR_FACT]` 附录的 Google Search 示例只检查字段存在与列表类型，明确允许 `organic_results=[]`；只有 schema 明确声明长度至少为 1 时，才加入非空约束（物理页 27–28，附录 H）。
- `[READER_INTERPRETATION]` 因而当前 oracle 本质上是接口 schema（ToolBench 中又部分来自 LLM 辅助构造）而非返回内容真值。一个字段齐全、类型正确但数值虚假的返回仍可通过示例中展示的 `Q`。论文的“verified”主要是“相对于给定契约通过”，不能等同于事实正确、语义正确或外部操作正确。
- `[AUTHOR_FACT]` 附录 I 给出的 soundness theorem 是条件式 sketch：只有所有 contract 对 `Exec` 与 `Update_t` 都 sound，初始状态满足 invariant，且更新保持 invariant 时，才推出 reachable trajectory 的安全性（物理页 29–31，式 15、21）。
- `[READER_INTERPRETATION]` 这些前提正是系统最难保证之处，论文没有验证实际抽取的契约 soundness，也没有证明实际 `Update_t` 保持 invariant。因此“formal logical guarantee”应读成条件保证，而非对实验系统的无条件端到端证明。
- `[READER_INTERPRETATION]` 正文把 precondition filter 描述成检查 weakest precondition（物理页 5），但实际式 9 和算法 1只检查 `S |= P_t`。附录把 `wp(t,⊤)` 定义为还存在某个执行结果满足 `Q_t` 的条件（物理页 30，附录 I.3）；这一量在调用前通常不可直接判定。论文没有说明实现如何计算该 `wp`，因此实际机制与 weakest-precondition 表述之间存在未闭合的形式跳跃。
- `[OPEN_QUESTION]` 表 3 报告“Semantic Constraint Mismatch”和“State Update Inconsistency”，但契约抽取章节主要说明 schema 字段/类型映射，未交代语义约束、值域约束和 update-consistency 谓词如何系统构建、由谁标注、准确率如何验证（物理页 8–9，§5.4、表 3；物理页 4，§3.2）。

## 5. 基准、基线与主要结果

- `[AUTHOR_FACT]` 实验使用 ToolBench 和 MCP-Universe。ToolBench 报告 G1/G2/G3 的 Pass Rate 与 Win Rate；MCP-Universe 主表只报告 Location Navigation、Repository Management、Financial Analysis 三个子任务的 Success Rate（物理页 5–6，§4.1–4.2、表 1）。
- `[AUTHOR_FACT]` 基线为 ReACT、DFSDT、LATS、ToolChain* 与 Tool-Planner；LLM backbone 为 Qwen-3-235B、DeepSeek V3.2、GPT-5.2 和 Gemini 3 Pro（物理页 6，§4.3–4.4、表 1；物理页 15，附录 D）。
- `[AUTHOR_FACT]` 在表 1 中 ToolGate 对大多数 backbone/任务取得最高值。例如 GPT-5.2 下，ToolBench G1/G2/G3 的 Pass/Win 分别为 85.5/83.5、93.0/90.5、91.8/95.3；MCP 三项为 35.52、45.45、90.0。对应 ToolChain* 为 82.8/80.0、90.5/88.3、88.5/92.5，以及 29.97、39.39、85.0（物理页 6–7，表 1及 §5.1）。
- `[AUTHOR_FACT]` “所有格都最好”并不成立：例如 Qwen-3-235B 的 ToolGate G3 Win Rate 为 82.3，低于 LATS 的 83.3 和 ToolChain* 的 83.5；正文用的是“best or near-best”（物理页 6–7，表 1、§5.1）。
- `[AUTHOR_FACT]` 表 2 的消融同时包含 `w/o Hoare`、`No {P}`、`No {Q}`。GPT-5.2 的 MCP-Avg 从 full 57.0 降至 No-P 52.5、No-Q 46.2、w/o-Hoare 37.6；DeepSeek V3.2 从 38.0 降至 34.5、30.9、27.2。该表显示移除 `Q` 的性能损失大于移除 `P`（物理页 7–8，表 2、§5.2）。
- `[READER_INTERPRETATION]` 这是本文最直接支持“后置验证不只是装饰”的证据：在两个 backbone、两个 benchmark family 上，No-Q 都明显弱于 full，且一般弱于 No-P。但它仍是系统级消融，不能单独证明每个被拒结果都是错误，也不能把性能差全部归因于形式 soundness。
- `[AUTHOR_FACT]` 作者报告 MCP-Universe 上 29.4% 的 tool-call attempts 被验证层拦截：`P` 共 17.6%（value/entity hallucination 8.4%、schema/format 5.1%、missing dependency 4.1%），`Q` 共 11.8%（empty/null 6.3%、semantic mismatch 3.7%、state-update inconsistency 1.8%）（物理页 8–9，表 3、§5.4）。
- `[AUTHOR_FACT]` 合约不完整性实验随机移除 5%/10% 的 `P/Q`；两种 backbone 都随移除比例增加而下降，但表中移除 10% 后仍高于 ToolChain*（物理页 13–14，附录 B、表 5）。
- `[READER_INTERPRETATION]` 该鲁棒性实验只测试“随机缺失约束”，没有测试错误、过强、过时或互相冲突的契约；且没有报告随机种子、重复次数或方差，因此不能外推为对契约错误的鲁棒性。

## 6. runtime cost 与归因风险

- `[AUTHOR_FACT]` 表 4 在 ToolBench G1/G2/G3 报告平均端到端秒数。ToolGate 在 GPT-5.2 下为 145/172/108 秒，在 DeepSeek V3.2 下为 152/178/112 秒；均略慢于 ReACT（132/157/98 与 138/162/104），但显著快于 ToolChain*、DFSDT 和 Tool-Planner（物理页 9，§5.5、表 4）。
- `[AUTHOR_FACT]` 图 2/正文称 GPT-5.2 的平均调用步数从 6.78 降至 4.21，降幅 37.9%，并把端到端延迟竞争力归因于提前剪枝抵消 `P/Q` 检查开销（物理页 8，§5.3；物理页 9，§5.5）。
- `[READER_INTERPRETATION]` 表 4 测的是整个系统的总时间，不是 isolated contract-check latency；差异同时包含检索、rerank、工具数、失败重试、外部 API 延迟和搜索策略。因此“P/Q verification overhead minimal”是作者解释，未由单独微基准直接测出。
- `[AUTHOR_FACT]` 附录 E 声明所有模型温度为 0.2，系统共享任务指令、工具描述、execution limits 和 termination conditions，并在相同环境中执行（物理页 15）。
- `[OPEN_QUESTION]` 论文没有给出每格运行次数、误差条/置信区间、随机种子、token 消耗、统一 tool-call 上限的具体数值、API 费用或 judge model/prompt。ToolBench Win Rate 由 LLM judges 比较系统输出与 Qwen-3-235B-ReACT 输出，但 judge 的身份和一致性分析未报告（物理页 6，§4.2）。这些缺口使模型、token、tool-call、prompt 和 oracle 差异无法被完全排除。
- `[OPEN_QUESTION]` 论文没有清楚说明各基线是否共享 ToolGate 的 embedding/reranker 与完全相同的候选空间；若不共享，主结果同时比较了检索/重排、搜索策略和契约门，不能只归因于契约。

## 7. 可记录的 Failure、作者限制与未测边界

### 7.1 作者明确报告或实验直接记录的 failure

- `[AUTHOR_FACT]` 前置门实际记录到 value/entity hallucination、schema/format violation、missing state dependency；后置门记录到 empty/null、semantic constraint mismatch、state update inconsistency，比例见表 3（物理页 8–9）。这些是 trace 分类后的真实报告项，可作为 failure 记录，但论文没有给原始计数与人工核验协议。
- `[AUTHOR_FACT]` 作者明确限制包括：当前范围主要是 text/structured-data tools；未覆盖 multimodal tools 和 long-chain collaborative tasks；评估环境大体静态，未充分覆盖 network latency、rate limits、fluctuating data states；指标主要量化，缺少解释推理与主动向用户索取缺失信息的细粒度质评；契约更新与 API 规范同步、父接口/派生接口一致性留待未来（物理页 9–10，Limitations）。
- `[AUTHOR_FACT]` MCP-Universe 完整数据集有六类任务，但主实验只报告 Location、Repository、Financial 三类；3D Design、Browser Automation 和 Web Searching 未进入表 1/2（物理页 14–15，附录 C.2；物理页 6–7，表 1/2）。

### 7.2 独立二读识别的机制边界

- `[READER_INTERPRETATION]` 后置门发生在工具执行之后，只能阻止返回值提交到内部 symbolic state；它不能撤销已经发生的现实副作用，例如文件删除、交易、发信或仓库写入。论文没有事务回滚、补偿动作、幂等性或 dry-run 机制，因此“safe tool execution”不能解释为外部世界副作用安全。
- `[READER_INTERPRETATION]` 当 schema 仅约束结构和类型时，错误但类型合法的内容会通过；当 `Q=True` 时，任何 well-formedness 之外的结果都可能进入状态。故其主要保护对象是 schema-relative state integrity，不是事实真值或用户意图一致性。
- `[READER_INTERPRETATION]` 算法 1 的 `T_failed` 在循环外初始化，一次 postcondition failure 后该工具会在后续所有 step 被跳过。该行为可能把参数特定或瞬时失败误当成工具永久不可靠，也与提示词中“可用不同参数重试同一工具”存在张力（物理页 17 的 prompt；物理页 19 的算法 1）。
- `[READER_INTERPRETATION]` 正文 §5.4 说明空列表只有 schema 明确非空时才拒绝，附录 H 的 Google 示例也允许空数组（物理页 8、27）；但附录 F.2 又笼统称 `Q` “mandates a non-empty result check”（物理页 16）。两者语义冲突，应以细化规则为准，且拒绝分类如何处理合法空结果仍需核验。
- `[READER_INTERPRETATION]` 预条件只从 required parameters 映射为存在/类型谓词，未必表达权限、配额、时效、跨工具因果关系或真实环境前提；论文在附录叙述中举出权限/handle 等语义约束，却未说明这些如何从一般 OpenAPI/JSON Schema 自动得到。
- `[OPEN_QUESTION]` 对有副作用或 nondeterministic 的工具，论文没有说明如何在执行前验证后置可达性、如何处理外部状态在检查与提交间变化、并发竞争、partial observability、重复调用和补偿事务。
- `[OPEN_QUESTION]` 论文没有报告 contract extractor 的 precision/recall、契约人工审核成本、每个 benchmark 中 `Q=True` 的实际调用占比，或错误拒绝/错误接受率。29.4% rejection rate 不是验证准确率。

## 8. Operator 抽取与 P046-style precondition check 的独立判断

### 8.1 可抽取的 Operator

- `[READER_INTERPRETATION]` `TypedStateCommitGate`：输入当前 typed state、tool result、postcondition 和 update function；先检查 `Q`/well-formedness，成功才原子化地更新受信状态并把结果暴露给后续推理，失败保持状态不变。最直接依据为物理页 5 的式 11–12、物理页 19 的算法 1、物理页 29–31 的附录 I。
- `[READER_INTERPRETATION]` `ContractFilteredToolPolicy`：对检索候选应用 `P` 指示函数并重新归一化，只在当前状态可满足前提的候选中选择。依据为物理页 5 的式 9–10。
- `[READER_INTERPRETATION]` `SchemaToContractExtraction`：将 required inputs 映射为存在/类型前置谓词，将 response schema 映射为结构、类型和明确长度约束；无 schema 时退化为 `Q=True`。依据为物理页 4 与物理页 27–28。
- `[READER_INTERPRETATION]` 这些只是可复用机制抽象，不是正式 Card，也不代表候选价值裁决。

### 8.2 是否实质超过 P046-style precondition check

- `[READER_INTERPRETATION]` 若“P046-style”仅指调用前检查前置条件，那么 ToolGate 在机制上实质超过它：新增了显式 typed state、执行后 `Q` 验证、失败不提交、受控 state transition 与返回结果注入；No-Q 消融在两个 backbone 上均显著弱于 full，支持后门具有独立经验贡献（物理页 5、7–8、19）。
- `[READER_INTERPRETATION]` 超越的范围应限定为“内部受信状态的 contract-relative 提交安全”。它没有证明外部副作用安全、返回事实真实性、契约正确性或完整性。因此不能把“pre + post”直接升级解读为端到端 verified execution。
- `[OPEN_QUESTION]` 本次读取边界不允许读取 P046 原文，故无法核验 P046 是否也包含状态提交、返回值校验或相同 oracle。以上比较只针对 invocation 中给出的“P046-style precondition check”抽象，不是两篇论文的逐项 prior-work 裁决。

## 9. 总结

- `[AUTHOR_FACT]` 论文提供了完整的 pre-call `P` gate 与 return-before-commit `Q` gate，并通过表 2 的分离消融显示二者均有贡献，且 `Q` 的移除损失更大。
- `[READER_INTERPRETATION]` 最稳健的来源结论是：ToolGate 将工具返回写入推理状态的过程变得显式、可检查、可拒绝，确实比单纯前置门多一个关键提交控制点。
- `[READER_INTERPRETATION]` 最重要的限制是：验证强度由 schema/contract 的质量上限决定；约 25% ToolBench 工具退化为 `Q=True`，ToolBench schema 又非 ground-truth specification；形式 theorem 只在 contract/update sound 的条件下成立；外部副作用发生在后置检查前且没有回滚。
- `[OPEN_QUESTION]` 在把该工作用于更强科研结论前，仍需独立核验：P046 的实际机制边界、契约抽取实现与误差、state-update 构造、基线检索公平性、运行重复/方差、LLM judge 配置、未报告的三类 MCP 任务，以及有副作用工具上的错误接受、错误拒绝和补偿行为。
