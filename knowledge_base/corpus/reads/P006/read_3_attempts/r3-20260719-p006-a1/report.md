# P006 fresh independent read-3 报告

## Provenance 与核查边界

- [AUTHOR_FACT] 本报告对应 invocation `r3-20260719-p006-a1`，论文为 *An LLM Compiler for Parallel Function Calling*（PMLR 235 / ICML 2024）；PDF SHA-256 实测为 `36dde899ed8abe0df728215e054aab21d1699add719afeb0ddadbb4e4eb23263`，与 invocation 一致。定位：invocation；PDF p.1 标题与会议信息。
- [READER_INTERPRETATION] 本次只读取了 invocation 明列的三个输入：论文 PDF、`second_read_prompt.md`、本 invocation；未枚举工作区，未读取 read_1、任何 read_2、Cards、其他读者报告或 blind query，未联网。报告仅写入本 attempt 的 `report.md`。
- [READER_INTERPRETATION] 已逐页提取并检查 PDF p.1–22；另检查了每页原生页面尺寸、文本块坐标、图像对象和表格/公式区块的版面顺序。未创建中间文件。当前工具链无法把内存渲染结果回传为可观看图像，因此下文“解析文本与可视 PDF”结论限于原生 PDF 文本层与页面几何核查，不把它夸大为完整的人眼像素级复核。
- [READER_INTERPRETATION] actual model/version 在当前子任务上下文中不可见，记为 `unknown`；canonical task 为 `/root/p006_third_read`；独立 thread ID 不可见，记为 `unavailable`。完成时间：`2026-07-19T16:27:59.1001221+08:00`。

## 1. 方法究竟改变哪一步计算？

- [AUTHOR_FACT] LLMCompiler 改变的是“多次函数调用的编排与执行”步骤，而不是底层 LLM 权重或单个工具的实现：Planner 将自然语言请求一次性分解为带依赖关系的任务 DAG，Task Fetching Unit 按依赖就绪情况取任务并替换占位变量，Executor 异步并行执行互不依赖的任务。定位：PDF p.3–4，Sec. 3、3.1–3.3；Fig. 2；短定位文本：“forming a directed acyclic graph”“fetches tasks … based on a greedy policy”“asynchronously executes tasks”。
- [AUTHOR_FACT] 对运行时才知道分支结果的问题，Executor 会把中间结果反馈给 Planner，后者生成新的任务及依赖，循环到得到最终结果。定位：PDF p.4–5，Sec. 3.4；短定位文本：“intermediate results are sent back … to the Function Calling Planner”。
- [AUTHOR_FACT] Planner 可流式输出任务，使已满足依赖的任务无需等待完整计划生成即可进入执行。定位：PDF p.5，Sec. 4.2；Table C.1（PDF p.15）；短定位文本：“asynchronously stream the dependency graph”。
- [READER_INTERPRETATION] 因而核心计算改动可概括为：把 ReAct 式“LLM 推理一次—调用一次工具—拼回观察—再推理”的串行控制流，改成“LLM 先生成显式依赖图—运行时按就绪关系并发调度—必要时重规划—统一 join/finalize”的控制流。该解释由 Fig. 1（PDF p.2）、Fig. 2（PDF p.4）和 Sec. 3.4（PDF p.4–5）共同支持。
- [AUTHOR_FACT] 终止/汇合由硬编码的 `finish` 动作触发；调用 join 的 LLM agent 要么生成最终回答，要么等待已计划任务执行后进入重规划。定位：PDF p.20–21，Appendix H；短定位文本：“special, hard-coded finish function”“finalize … or wait”。

## 2. 输入、输出、可用信息与干预时点

- [AUTHOR_FACT] 系统级输入是用户自然语言请求，以及用户提供的工具定义（描述与参数规范）；Planner 的 in-context examples 为可选输入。定位：PDF p.4–5，Sec. 3.1、4.1；短定位文本：“users are only required to provide tool definitions, and optional in-context examples”。
- [AUTHOR_FACT] Planner 可用的信息包括用户请求、预定义语法/依赖图提示、工具定义及可选示例；其输出是逐行任务、工具参数、递增 ID 与用 `$id` 表示的依赖。定位：PDF p.4，Sec. 3.1；PDF p.19–21，Appendix G–H；短定位文本：“use the format $id”“Ensure the plan maximizes parallelizability”。
- [AUTHOR_FACT] Task Fetching Unit 不使用专门 LLM；它在前置任务完成后将占位符替换为实际输出，并按贪心就绪策略向 Executor 分发任务。定位：PDF p.4，Sec. 3.2；Fig. 2。
- [AUTHOR_FACT] Executor 的输入是已满足依赖的任务及用户工具；每个任务有独立 memory，完成输出会被送往依赖它的后续任务。定位：PDF p.4，Sec. 3.3；短定位文本：“each task has dedicated memory”“forwarded as input to the tasks dependent on them”。
- [AUTHOR_FACT] 干预发生在四个时点：初始调用前由 Planner 生成 DAG；计划生成过程中可流式发出任务；每个前置任务完成时解锁并替换后续参数；当前计划不足时把中间结果反馈给 Planner 重规划。定位：PDF p.4–5，Sec. 3.1–4.2。
- [AUTHOR_FACT] 最终输出是 join/finish 阶段基于全部已收集观察生成的用户回答；在 Game of 24 中还可输出“需要重规划”的控制决定。定位：PDF p.8，Sec. 5.3；PDF p.21，Appendix H。
- [READER_INTERPRETATION] 可用信息被分阶段隔离：Planner 先看请求和工具接口形成结构；单个工具任务只获得相关参数/前置结果；最终回答阶段再汇总观察。论文将这种隔离视为减少中间观察干扰的一部分，但没有给出形式化的信息流安全保证。定位：PDF p.1–2、p.15，Abstract/Introduction、Appendix B。

## 3. 最强基线与最接近组合基线

- [AUTHOR_FACT] 主实验的通用直接基线是 ReAct；HotpotQA、Movie Recommendation、ParallelQA 的 GPT 实验还比较 OpenAI Parallel Function Calling；Game of 24 比较原始 Tree-of-Thoughts；WebShop 比较 ReAct、LATS、LASER。定位：PDF p.6，Table 1；PDF p.8–9，Sec. 5.4、Table 3。
- [AUTHOR_FACT] 没有一个基线在所有任务/指标上都“最强”。例如：HotpotQA/GPT 的最高基线准确率是 ReAct† 62.47%，基线中最低报告延迟是 OpenAI Parallel Function 4.42s；Movie Recommendation/GPT 的最强基线准确率/延迟为 OpenAI 77.00%/7.42s；ParallelQA/GPT 的最高基线准确率是 ReAct 89.09%，最低基线延迟是 OpenAI 19.29s。定位：PDF p.6，Table 1。
- [AUTHOR_FACT] 在 WebShop，质量较强的直接基线是 LATS（gpt-3.5，成功率 38.0%，N=50）和 LASER（gpt-4，50.0%，N=500）；ReAct 更快，但质量较低。定位：PDF p.9，Table 3。
- [READER_INTERPRETATION] 就“组成部件最接近”而言，论文正文描述的最近邻是两类：ReWOO 提供“规划与执行/观察分离”但不提供本文式并行及动态重规划；OpenAI Parallel Function Calling 提供并行函数调用，但论文称其只规划当前可并行任务且限于 OpenAI 模型。定位：PDF p.3，Sec. 2.1–2.2；PDF p.7，Sec. 5.2。
- [READER_INTERPRETATION] 若把“规划 + 并行执行 + 重规划”拆开看，Appendix F 的组合对照还包括 TPTU-OA（规划、无并行/重规划）、HuggingGPT（规划与并行、无重规划、领域受限）以及 ReAct/TPTU-SA（迭代式动态执行、无显式规划/并行）。这只是作者给出的组件矩阵，不等于外部核验过的完整最近工作集合。定位：PDF p.18，Table E.3 与 Appendix F。
- [AUTHOR_FACT] Appendix F.1 还在 HotpotQA comparison 上给出 TPTU-SA/OA 的作者复现；因官方实现不可用，作者依据原论文提示自行实现。定位：PDF p.19，Table F.4；短定位文本：“official implementation … is not available”。

## 4. 结果是否可能来自模型、token、tool-call、prompt 或 oracle 差异？

- [AUTHOR_FACT] 同一 benchmark 内，作者称不同方法使用相同 instruction prompts 和相同 few-shot examples；例外是 ReAct†/TPTU-SA† 加入避免循环和早停的专用提示。大多数运行 temperature=0，Game of 24 的 proposer/evaluator 为 0.7；GPT 即使 temperature=0 仍有随机性，因此作者运行 3 次并报告平均准确率。定位：PDF p.15–16，Appendix D。
- [AUTHOR_FACT] 不同 benchmark 使用了不同模型：HotpotQA/Movie Recommendation 为 gpt-3.5-turbo-1106，ParallelQA 为 gpt-4-turbo-1106，Game of 24 为 gpt-4-0613；开源列为 LLaMA-2 70B，在 2×A100-80GB 上用 vLLM。定位：PDF p.15–16，Appendix D。
- [READER_INTERPRETATION] 因此不能跨 benchmark 把绝对准确率或延迟差异归因于编排方法；Table 1 的有效比较单位是“同一 benchmark、同一模型列内”的方法差异。
- [AUTHOR_FACT] HotpotQA/Movie Recommendation 中 ReAct 与 LLMCompiler 使用同一 Wikipedia search 工具；ParallelQA 两者都使用 search 与 math，math 为 LLM agent 解释问题后调用 `numexpr`。定位：PDF p.6–7，Sec. 5.1–5.2。
- [AUTHOR_FACT] Token/cost 差异是机制的一部分：LLMCompiler 减少 LLM 调用次数，其 Planner 示例只含 plans、不含 observations；Table 2 报告输入/输出 token 和按对应 GPT 价格估算的费用。定位：PDF p.6–7，Table 2、Sec. 5.1 “Costs”。
- [READER_INTERPRETATION] 准确率提升不能被解释为“纯并行调度”的孤立效应。Movie Recommendation 中 LLMCompiler 几乎总是搜索满 8 部电影，而 ReAct 常在不足 8 次时提前停止；WebShop 中 LLMCompiler 访问搜索返回的 10 个条目，而 ReAct 常在信息不完整时提交。更广的固定探索/完整工具调用本身可提高准确率，同时也改变 tool-call 数量和信息预算。定位：PDF p.9，Sec. 5.4；PDF p.13–14，Fig. A.1–A.4。
- [AUTHOR_FACT] ReAct† 的额外 prompt 改善准确率但未完全消除早停/循环；作者用它作为延迟基准，因为原始 ReAct 的循环/早停使延迟难以精确比较。定位：PDF p.6–7，Table 1 与 Sec. 5.1。
- [READER_INTERPRETATION] Table 2 标为 “ReAct” 而非 “ReAct†”，但正文的延迟比较使用 ReAct†；论文未在该处清楚说明成本表对应原始 ReAct 还是干预后的 ReAct†，故成本与延迟的基准口径可能不完全一致。定位：PDF p.6，Tables 1–2；PDF p.7。
- [AUTHOR_FACT] 作者明确说 OpenAI 未公开其函数调用机制，因此无法确定 LLMCompiler 相对其延迟优势的原因；关于参数校验/系统提示开销只是推测。定位：PDF p.7，脚注 1。
- [OPEN_QUESTION] OpenAI baseline 的隐藏 system prompt、函数 schema 编码、服务端并发和速率限制未披露，无法从本文排除 prompt/token/tool-call 实现差异对延迟和成本的贡献。定位：PDF p.7，脚注 1。
- [OPEN_QUESTION] WebShop 的 LATS/LASER 成功率与分数来自各自论文，仅 ReAct 由本文复现；Table 3 未交代跨论文延迟是否在相同服务日期、硬件、并发和完整提示下测得，因此 101.7×/2.69× 的跨系统延迟比不具备完全受控的本文内对照。定位：PDF p.9，Table 3 图注与 Sec. 5.4。
- [OPEN_QUESTION] 论文没有提供所有逐样例原始调用日志、完整 token 计费展开或 oracle/人工介入日志；据本文可见信息，除 benchmark 标签/环境 reward 外未报告答案 oracle 介入推理过程，但无法仅靠汇总表进一步排除数据清洗和失败重试策略差异。

## 5. 作者明示限制、负向结果和未测试边界

- [AUTHOR_FACT] LLMCompiler 未达到 N 路任务的 N× 实测加速；Planner 和 final answering 是串行开销，join 还受最慢任务的 straggler 影响。Movie Recommendation 中 Planner/回答平均耗时 1.88s/1.62s，最慢 search 平均 1.13s，而所有 search 平均 0.61s。定位：PDF p.16–17，Appendix E.1；Eqs. 1–6。
- [AUTHOR_FACT] 流式 Planner 的收益依赖工具耗时：HotpotQA 仅 1.01×、Movie Recommendation 1.03×、ParallelQA 1.30×。定位：PDF p.15，Table C.1。
- [AUTHOR_FACT] WebShop 上 LLMCompiler 比 ReAct 慢：gpt-3.5 为 10.48s 对 5.98s，gpt-4 为 26.73s 对 19.90s；作者归因于 Planner overhead。定位：PDF p.9，Table 3 与 “Performance and Latency”。
- [AUTHOR_FACT] ParallelQA 的 LLMCompiler 失败被作者分成 Planner、Executor、最终输出三类；在作者给出的失败集合内分别占 8%、64%、28%。Planner 可把错误 identifier 接到后续任务形成错误 DAG；Executor 常选错属性或错误处理单位换算；最终输出可能从正确观察得出错误比较结论。定位：PDF p.15，Appendix B。
- [AUTHOR_FACT] ReAct 并非在所有子集都更差：HotpotQA 中约少于 3% 的三次调用样例可借额外一次备用实体名搜索重试而优于固定两次搜索的 LLMCompiler，作者称这是 ReAct 的潜在适应性优势。定位：PDF p.14，Appendix A 末段。
- [AUTHOR_FACT] ParallelQA 有 113 个样例，由 GPT-4 按准则生成后人工标注；实体和问题被刻意筛选，使答案可从 Wikipedia 第一段取得，以尽量排除 search failure，最大并行任务数只覆盖 2–5。定位：PDF p.7，Sec. 5.2；PDF p.21，Appendix I。
- [READER_INTERPRETATION] 因此 ParallelQA 主要测试规划/依赖分解，不充分覆盖真实检索中的缺失、冲突、长文档、多轮澄清、工具超时、限流、非确定返回或恶意工具输出。
- [AUTHOR_FACT] 开源模型实验只报告 LLaMA-2 70B；动态重规划主要在 Game of 24（100 instances）和 HotpotQA bridge 上展示；论文未报告更小模型、大规模 DAG、深层依赖、循环依赖、并发资源上限或生产 API 限流实验。定位：PDF p.5–8、p.15–18。
- [OPEN_QUESTION] 除 WebShop 的一项 `72.8 ± 4.01` 外，主要表格没有置信区间、标准误或显著性检验；多次 GPT 运行的方差和延迟分布未完整报告。定位：PDF p.9；PDF p.16。
- [OPEN_QUESTION] Appendix A 首段称 “HotpotQA evaluation with LLaMA-2 70B” 的 ReAct/LLMCompiler 准确率为 70.00/77.80，但 Table 1 中这组数值对应 Movie Recommendation；HotpotQA/LLaMA-2 为 54.74/57.83（或 ReAct† 54.40）。这是原文内部数据集/数值错配，需以原始实验记录确认。定位：PDF p.13，Appendix A 首段；PDF p.6，Table 1。
- [OPEN_QUESTION] Appendix B 写 “10.6% (36 examples)” 的总失败；若仅以 ParallelQA 的 113 个独立样例计，10.6% 约为 12 个而非 36 个。36 可能是 3 次运行累计失败，但该段未说明计数单位。定位：PDF p.15，Appendix B；PDF p.7/p.21 的 113-example 描述；PDF p.16 的 3-run 说明。
- [AUTHOR_FACT] Impact Statement 仅笼统表示未发现特别值得指出的社会后果，没有展开并行工具调用的权限、错误放大或资源消耗风险。定位：PDF p.9，Impact Statement。

## 6. 可抽取的 Operator 与真实可记录的 Failure

### Operator（仅机制抽取）

- [AUTHOR_FACT] `DAG planning operator`：把自然语言请求和工具 schema 转成带递增 ID、工具参数、`$id` 依赖占位符的任务 DAG。定位：PDF p.4，Sec. 3.1；PDF p.20，Appendix H。
- [AUTHOR_FACT] `dependency-aware greedy fetch operator`：持续选取依赖已满足的任务，把占位符替换为前置输出并发给 Executor；该单元无需专用 LLM。定位：PDF p.4，Sec. 3.2。
- [AUTHOR_FACT] `asynchronous execution operator`：并发执行已证明互相独立的任务，每任务保持独立 memory，完成后传播结果。定位：PDF p.4，Sec. 3.3。
- [AUTHOR_FACT] `streamed planning operator`：Planner 生成一条任务就发送一条，用工具执行隐藏后续规划延迟。定位：PDF p.5，Sec. 4.2；PDF p.15，Table C.1。
- [AUTHOR_FACT] `feedback replanning operator`：当前计划执行后若无法回答，把中间状态送回 Planner 生成下一轮图；Game of 24 中配合 proposer、evaluator、top-k select。定位：PDF p.5，Sec. 3.4；PDF p.8，Sec. 5.3。
- [AUTHOR_FACT] `join/finish operator`：收集先前动作结果，由 LLM agent 生成最终答案或决定等待执行后重规划。定位：PDF p.21，Appendix H。
- [READER_INTERPRETATION] 上述 Operator 的共同约束是：依赖必须能表示为 DAG/占位变量，工具接口需事先给定，Planner 必须遵守格式，执行器只并发处理已就绪任务。

### Failure（论文中有实际观察或明确负向分析）

- [AUTHOR_FACT] `planner wrong-edge failure`：Planner 选错前置任务 identifier，导致后续输入映射错误和 DAG 错误。定位：PDF p.15，Appendix B；作者称在其 ParallelQA 评估中共 3 个 Planner 实例。
- [AUTHOR_FACT] `executor semantic/tool failure`：math tool 选错属性或单位换算错误；在作者失败分解中占失败集合的 64%。定位：PDF p.15，Appendix B。
- [AUTHOR_FACT] `final synthesis failure`：工具观察已收集，但最终 LLM 得出错误结论，例如没有选出最小属性；占失败集合的 28%。定位：PDF p.15，Appendix B。
- [AUTHOR_FACT] `planning/join overhead failure`：Planner 与回答阶段不可并行，短工具调用或较少并行任务时收益小，WebShop 甚至慢于 ReAct。定位：PDF p.9、p.15–17。
- [AUTHOR_FACT] `straggler-at-join failure`：并行批次由最慢任务决定完成时间，降低理论 N× 加速。定位：PDF p.16–17，Appendix E.1。
- [AUTHOR_FACT] `ReAct premature-stop failure`：Movie Recommendation 中约 85% ReAct 样例未完成 8 次搜索；额外 prompt 缓解但未根除。定位：PDF p.13，Fig. A.1–A.2。
- [AUTHOR_FACT] `ReAct repetitive-call/divergence failure`：HotpotQA/LLaMA-2 中约 10% ReAct 样例超过 4 次调用并常进入循环/发散；这些样例准确率低于 10%。定位：PDF p.14，Fig. A.3–A.4。
- [AUTHOR_FACT] `incomplete-information commit failure`：WebShop 的 ReAct 常未充分探索条目即决策，导致无法区分相似选择。定位：PDF p.9，Sec. 5.4。
- [READER_INTERPRETATION] `OpenAI immediate-only planning` 可作为作者报告的比较边界，但不是本文直接记录的运行错误：作者称它一次只规划当前可并行任务，复杂依赖图需多次 LLM 调用。定位：PDF p.7，Sec. 5.2。

## 7. 关键判断的页码、章节、图表与短定位文本索引

| 判断 | 位置 | 短定位文本 |
|---|---|---|
| 串行 ReAct 与并行 LLMCompiler 的控制流差异 | PDF p.2，Fig. 1 | “Parallel tool invocations” |
| Planner / Fetcher / Executor 三组件 | PDF p.4，Fig. 2；Sec. 3.1–3.3 | “DAG of Tasks”“Resolves Dependency” |
| 动态重规划反馈环 | PDF p.4–5，Sec. 3.4 | “sent back … to the Function Calling Planner” |
| 用户输入与可选示例 | PDF p.5，Sec. 4.1 | “Tool Definitions”“In-context Examples” |
| 流式 Planner | PDF p.5，Sec. 4.2；p.15，Table C.1 | “immediately processed” |
| 四组主实验结果 | PDF p.6，Tables 1–2 | “Accuracy and latency comparison” |
| OpenAI 机制未知/解释仅为推测 | PDF p.7，脚注 1 | “unable to conclude why” |
| Game of 24 重规划 | PDF p.8，Sec. 5.3 | “limited to planning only within one iteration” |
| WebShop 结果与负延迟结果 | PDF p.9，Table 3 | “slightly slower than ReAct” |
| ReAct 早停与循环 | PDF p.13–14，Figs. A.1–A.4 | “premature early stopping”“repetitive function calls” |
| LLMCompiler 自身失败分解 | PDF p.15，Appendix B | “Planner, Executor, and final output process” |
| 实验模型、shots、温度、运行次数 | PDF p.15–16，Appendix D | “zero temperature”“conducted 3 runs” |
| 串行开销、straggler 与速度上下界 | PDF p.16–17，Appendix E.1，Eqs. 1–6 | “not achieving the N× latency speedup” |
| HotpotQA bridge 补充实验 | PDF p.18，Table E.2 | “bridge benchmark” |
| 组件型近邻矩阵与 TPTU 对照 | PDF p.18–19，Tables E.3/F.4 | “Planning / Replanning / Parallel Execution” |
| Planner 具体语法与 finish | PDF p.20–21，Appendix H | “use the format $id”“hard-coded finish” |
| ParallelQA 生成与范围 | PDF p.21，Appendix I | “113 examples”“ranging from 2 to 5” |

## 8. 解析文本与可视 PDF 是否冲突？

- [AUTHOR_FACT] PDF 共 22 页；p.1–12 为正文与参考文献，p.13–22 为附录。原生文本层可逐页提取；Fig. 1、Fig. 2、Fig. J.6 含图像/矢量对象，Tables 1–3、C.1、E.2、E.3、F.4 和 Eqs. 1–6 的文本散布在多个坐标块中。
- [READER_INTERPRETATION] 对正文双栏顺序、表格列标题、图注、公式编号与页面几何的核查未发现内容缺页；但简单线性文本提取会把图内标签、表格多列和公式上下标串接在一起，不能据线性顺序直接恢复视觉关系。例如 Table 1 的 GPT/LLaMA-2 两组列、Table 3 的不同 N 行、Fig. 3 的三种依赖图以及 Eqs. 1–6 均必须结合块坐标/标题读取。定位：PDF p.6、p.9、p.16–18。
- [READER_INTERPRETATION] 本报告中的表格数值均按页面列标题和几何分组重新对应，而不是照搬线性抽取顺序；未发现因此造成的数值列错配。
- [OPEN_QUESTION] 当前工具无法将内存渲染页作为可观看图像返回，且写入被限定为仅 `report.md`，故没有进行逐像素的人眼对照。能够确认的是“文本层—页面坐标—图表标题/公式编号”之间未发现结构冲突；不能声称已排除扫描像素、颜色图例或细微矢量标记层面的冲突。

## 非任务输出声明

- [READER_INTERPRETATION] 本报告不生成 Card，不评价 Candidate，不作 novelty 判断，不评价科研价值，也不对论文或方法作最终裁决；所有未由原文明示支持的内容均标为解释或开放问题。
