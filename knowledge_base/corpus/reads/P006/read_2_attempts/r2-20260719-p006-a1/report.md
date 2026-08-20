# P006 独立二读报告

## 0. provenance、边界与核查方式

- [AUTHOR_FACT] 本报告引用冻结快照 `r2-20260719-p006-a1/invocation.md`：Attempt ID 为 `r2-20260719-p006-a1`；canonical metadata 为 `PMLR:v235/kim24y`、题名 *An LLM Compiler for Parallel Function Calling*、ICML 2024；快照记录的 PDF SHA-256 为 `36dde899ed8abe0df728215e054aab21d1699add719afeb0ddadbb4e4eb23263`，prompt SHA-256 为 `ffb7c12e663f44318d8eda1c270cbc26ad66665fd803247a2ab66a8f23fa333a`。（定位：invocation，“Independent read-2 invocation”清单）
- [AUTHOR_FACT] 本次逐页读取了 PDF 的全部 22 页；先用 `pypdf` 分页提取文本，再用 PyMuPDF/`fitz` 将同一 PDF 的第 1–22 页逐页内存栅格化并回传图像检查；未把渲染图写入磁盘。（定位：本次工具可观察输出；PDF 页码 1–22）
- [AUTHOR_FACT] 实际读取的研究文件仅为：`P006_llmcompiler.pdf`、`second_read_prompt.md`、本 attempt 的 `invocation.md`。另因平台技能规则读取了非研究指令文件：`pdf/SKILL.md`、`control-in-app-browser/SKILL.md`、`assumption-ledger-manager/SKILL.md` 及其 `references/rules.md`、`output_schema.md`、`checklists.md`；未读取首读、Cards、其他报告、blind query，也未枚举工作区。
- [AUTHOR_FACT] 实际使用工具：PowerShell `Get-Content`（仅指定文件）、Python `pypdf`、PyMuPDF/`fitz`、内存图像回传，以及 `apply_patch`（仅创建本报告）。曾尝试连接本地浏览器打开同一 PDF，但工具返回 `No browser is available`，未发生浏览器读取；未联网。
- [OPEN_QUESTION] 平台不提供可验证的文件级访问审计，因此系统级 observable file-access/tool trace 为 `unavailable`；以上工具与路径是本读者可观察并自报的 trace。隔离类型仍为 invocation 所述 `procedural_blinding`，不能称为技术隔离。实际底层 model/version 对本读者不可见，记为 `unknown`；可见 canonical task 名为 `/root/p006_second_read`。
- [READER_INTERPRETATION] `assumption-ledger-manager` 通常要求另写 ledger，但本任务只授权写 `report.md`；故未产生额外 ledger 文件。下文所有未充分验证的因果解释均保留为 `[READER_INTERPRETATION]` 或 `[OPEN_QUESTION]`，并附最小验证路径，不把它们伪装为作者事实。

## 1. 方法究竟改变哪一步计算？

- [AUTHOR_FACT] LLMCompiler 改变的是“多次函数调用的编排与执行顺序”，而非底层 LLM 推理内核：Planner 把自然语言请求编译成带依赖关系的任务 DAG；Task Fetching Unit 在依赖满足时贪心取出任务并替换占位符；Executor 异步并发执行彼此独立的工具任务。（定位：PDF p.3–4，§3、§3.1–3.3；Fig.2；短定位文本：“directed acyclic graph of task dependencies”“fetches tasks … based on a greedy policy”“asynchronously executes tasks”）
- [AUTHOR_FACT] 当执行图依赖运行时观察时，Executor 把中间结果反馈给 Planner，Planner 重新生成下一批任务及依赖，循环至可回答为止。（定位：PDF p.4–5，§3.4；短定位文本：“sent back from the Executor to the Function Calling Planner”）
- [AUTHOR_FACT] Planner 还可流式输出任务，使已就绪任务无需等待整个计划生成完毕即可进入执行；ParallelQA 上有/无 streaming 的延迟为 16.69/21.72 秒，作者报告 1.30× 改善。（定位：PDF p.5，§4.2；p.15，Table C.1；短定位文本：“asynchronously stream the dependency graph”）
- [READER_INTERPRETATION] 核心干预可概括为“把 ReAct 的交替式 `reason→act→observe` 串行循环，改写为一次或分轮生成依赖图，再做依赖约束下的并行调度”。准确率变化不是并行执行本身的必然结果，还同时包含观察隔离、调用次数约束与更完整信息收集的影响。（依据：PDF p.1–2，Fig.1；p.13–15，Appendix A–B；验证路径：做同一 DAG、同一调用集合下仅切换串行/并行的消融）

## 2. 输入、输出、可用信息与干预时点

- [AUTHOR_FACT] 框架输入包括用户自然语言请求、用户提供的工具定义（描述与参数规格），以及可选的 Planner in-context examples；预定义 Planner prompt 规定任务 ID、动作类型、`$id` 中间变量与“最大化可并行性”。（定位：PDF p.4–5，§3.1、§4.1；p.20，Appendix H；短定位文本：“Tool Definitions”“optional in-context examples”“Ensure the plan maximizes parallelizability”）
- [AUTHOR_FACT] Planner 的直接输出是逐行任务计划/依赖 DAG；Fetching Unit 可用的信息是计划、依赖状态和已完成任务结果；Executor 可用的信息是已派发任务、相应工具及每任务独立 memory。（定位：PDF p.4，Fig.2、§3.1–3.3；短定位文本：“placeholder variable”“dedicated memory”）
- [AUTHOR_FACT] 最终输出由硬编码的 `finish`/join 语义收集并组合先前动作结果；它可直接回答，也可在当前计划尚不足时等待执行并触发后续规划。（定位：PDF p.20–21，Appendix H；短定位文本：“Collects and combines results from prior actions”）
- [AUTHOR_FACT] 静态场景中的干预发生在工具执行前（先生成 DAG）与每个依赖完成时（替换变量、解锁后继任务）；动态场景还在每轮工具执行后反馈中间结果并重新规划。（定位：PDF p.4–5，Fig.2、§3.2、§3.4）
- [READER_INTERPRETATION] “可用信息”并非各方法严格等量：ReAct 每步看到追加的历史 observations；LLMCompiler 的各工具仅得到相关任务上下文，最终 join 再看到汇总结果。这种上下文结构差异可能影响准确率。（依据：PDF p.1、p.4、p.15；短定位文本：“provides only relevant contexts to each tool”；验证路径：固定 observations 与上下文顺序/长度的对照实验）

## 3. 最强基线与最接近组合基线

- [AUTHOR_FACT] HotpotQA（GPT）中，准确率最高的报告基线是 ReAct† 62.47%，OpenAI parallel function calling 为 62.05%，LLMCompiler 为 62.00%；相对 ReAct†，LLMCompiler 延迟 3.95 秒、1.80× 加速。LLaMA-2 行中 LLMCompiler 为 57.83%，高于 ReAct† 54.40%。（定位：PDF p.6，Table 1）
- [AUTHOR_FACT] Movie Recommendation（GPT）中，最强基线是 OpenAI parallel function calling 77.00%，与 LLMCompiler 77.13%接近；LLMCompiler 相对 ReAct† 的延迟加速为 3.74×。LLaMA-2 下 LLMCompiler 77.80%，ReAct† 70.60%。（定位：PDF p.6，Table 1）
- [AUTHOR_FACT] ParallelQA（GPT）中 ReAct 89.09%是准确率最强基线，LLMCompiler 89.38%；OpenAI parallel function calling 为 87.32%。LLaMA-2 下 ReAct 59.59%、LLMCompiler 68.14%。（定位：PDF p.6，Table 1）
- [AUTHOR_FACT] Game of 24 的直接基线是 Tree-of-Thoughts：GPT 下 74.00%、241.2 秒，对比 LLMCompiler 75.33%、83.6 秒；LLaMA-2 下 30.00%、952.06 秒，对比 32.00%、456.02 秒。（定位：PDF p.6，Table 1；p.8，§5.3）
- [AUTHOR_FACT] WebShop 的最强报告基线随模型而异：gpt-3.5-turbo 用 LATS（38.0% success，1066 秒；N=50），gpt-4 用 LASER（50.0%，72.16 秒；N=500）；LLMCompiler 分别报告 44.0%/10.72 秒（同 N=50）与 55.6%/26.73 秒（N=500）。（定位：PDF p.9，Table 3）
- [AUTHOR_FACT] 最接近“组合能力”的比较不是单一基线。Table E.3 将 HuggingGPT 标为 planning+parallel execution 但 domain limited，将 TPTU-OA 标为 planning 但无 replanning/parallel，将 ReAct/TPTU-SA 标为通用域但无显式 planning/parallel；作者声称只有 LLMCompiler 同时具备 planning、replanning、parallel execution、all-domain。量化的最近 plan-and-solve 对照是 TPTU-OA：HotpotQA 57.50%、1.35×，LLMCompiler 62.00%、1.51×。（定位：PDF p.18，Table E.3；p.19，Table F.4、§F.1）
- [READER_INTERPRETATION] 因没有“相同 Planner + 相同 DAG + 串行 Executor”以及“相同调用预算 + 无独立 memory”的完整组合消融，论文不能仅凭现有基线把收益唯一归因于并行调度。（验证路径：加入上述两项组合基线，并固定模型、prompt、工具结果、调用数与 join）

## 4. 模型、token、tool-call、prompt、oracle 差异能否解释结果？

- [AUTHOR_FACT] 同一 benchmark 的主要方法对照使用相同模型版本和相同 few-shot examples；HotpotQA/Movie Rec 用 gpt-3.5-turbo-1106，ParallelQA 用 gpt-4-turbo-1106，Game of 24 用 gpt-4-0613；开源模型是部署在 2×A100-80GB/vLLM 上的 LLaMA-2 70B。除 Game of 24 的 proposer/evaluator 温度为 0.7 外，其余为 0；GPT 即使温度 0 仍有随机性，因此准确率取 3 次运行平均。（定位：PDF p.15–16，Appendix D；短定位文本：“same examples across different methods”“reported the average accuracy”）
- [AUTHOR_FACT] prompt 并非完全相同：作者称 instruction prompts 跨方法相同，但 ReAct† 明确加入避免 looping/early stopping 的专用 prompt；LLMCompiler 自身还有预定义 Planner prompt、工具定义和可选/实际使用的 in-context plan examples。（定位：PDF p.6–7，§5.1；p.16，Appendix D；p.19–21，Appendix G–H）
- [AUTHOR_FACT] token/tool-call 数量是显著不同的：例如 Movie Rec 输入 token 为 ReAct 20,000、OpenAI parallel 5,800、LLMCompiler 2,800；LLMCompiler 在该任务几乎总是完成 8 次搜索，而 ReAct 约 85% 样本提前停止。HotpotQA 上约 10% ReAct 样本超过 4 次调用并发散，而 LLMCompiler 通常仅两次搜索。（定位：PDF p.6，Table 2；p.13–14，Fig. A.1–A.4）
- [AUTHOR_FACT] OpenAI parallel function calling 的内部机制未公开，作者明确说无法断定其较高延迟原因，只提出可能存在函数/参数验证和 system prompt 转换开销的猜测。（定位：PDF p.7，§5.2 前脚注 1；短定位文本：“unable to conclude why”“One speculation”）
- [AUTHOR_FACT] ParallelQA 为 113 个 GPT-4 生成后由人标注的样本；实体与问题被刻意选择为可从 Wikipedia 首段取得属性，以尽量排除搜索失败，主要测任务分解、规划与基于 observations 作答。（定位：PDF p.7，§5.2；p.21，Appendix I）
- [AUTHOR_FACT] WebShop 中 LLMCompiler 会访问 search 返回的全部约 10 个商品并取回选项/价格/属性，而 ReAct 常在信息不完整时较早决策；因此两者探索广度不同。（定位：PDF p.8–9，§5.4；短定位文本：“visiting all ten items”“commit to a decision with imperfect information”）
- [READER_INTERPRETATION] 准确率增益至少可能由四个共同变化造成：减少中间 observation 干扰、避免重复调用、强制完整搜索、扩大 WebShop 探索预算；现有实验不足以把它们与“并行执行”单独分离。（风险：若该解释错误，会误判机制；验证路径：2×2 消融 parallel/serial × shared/separate context，并严格匹配调用预算）
- [OPEN_QUESTION] 论文未提供逐方法完整 system prompt、API function-calling 隐式 prompt/token 计费口径及所有 benchmark 的逐例 tool trace，无法排除隐藏 prompt、tokenization 或 API 编排差异。（验证路径：公开完整请求日志、固定工具返回的 replay harness 和逐例 token/tool-call trace）
- [OPEN_QUESTION] ParallelQA 的“首段可答”筛选降低了 retrieval failure，却可能形成接近 oracle 的工具可得性条件；其结果能否外推到搜索失败、证据冲突或网页变化场景未测试。（验证路径：在不可答、噪声检索、多候选实体与陈旧信息集上复测）

## 5. 作者明示限制、负向结果与未测试边界

- [AUTHOR_FACT] 并行加速上界不是自动达到 N×：Planner 和最终回答阶段不可并行，且 join 受 straggler 影响。Movie Rec 中 Planner/answer 平均开销分别 1.88/1.62 秒；最慢 search 平均 1.13 秒，接近全部 task 平均 0.61 秒的 2×。作者给出的理论速度范围约为 1 到 N。（定位：PDF p.16–17，Appendix E.1，Eq.1–6；短定位文本：“reduce the planner overhead”“minimize … stragglers”）
- [AUTHOR_FACT] WebShop 是明确负向延迟结果：LLMCompiler 比 ReAct 慢（gpt-3.5：10.48 vs 5.98 秒；gpt-4：26.73 vs 19.90 秒），作者归因于 Planner overhead，并以成功率提升作权衡。（定位：PDF p.9，Table 3、§5.4；短定位文本：“slightly slower than ReAct”）
- [AUTHOR_FACT] ParallelQA 的总失败中（作者写为 10.6%、36 个样例/运行实例），Planner/Executor/final output 分别占 8%/64%/28%；Planner 可把错误任务 ID 作为后继输入形成错误 DAG，math tool 会选错属性或错误换算单位，最终阶段会从已收集观察得出错误结论。（定位：PDF p.15，Appendix B）
- [AUTHOR_FACT] ReAct 并非在所有适应性情形都差：HotpotQA 中少于 3%的三调用案例可通过替代实体名重试初次失败搜索，其准确率高于固定两搜索的 LLMCompiler。（定位：PDF p.14，Appendix A；短定位文本：“potential adaptability advantage of ReAct”）
- [AUTHOR_FACT] 简单 branching 可静态编译，但复杂 branching 可能需要 replanning；Game of 24 中单一静态图不可行，Planner 每次只能规划一个 iteration。（定位：PDF p.4–5，§3.4；p.8，§5.3）
- [READER_INTERPRETATION] 实证边界包括：少量特定 GPT 发布版与 LLaMA-2 70B、固定工具集合、最多 2–8 路并行的主要 benchmark、一个人工设计的 ParallelQA，以及 WebShop/ToT 特定实例化；尚未覆盖工具副作用、并发写冲突、限流、不可重入工具、权限/安全策略、超长 DAG、循环依赖或恶意工具输出。（验证路径：并发安全与失败注入 benchmark；这些边界是未测试推断，不是作者声明）
- [OPEN_QUESTION] 作者将 Executor 并发执行建立在 Fetching Unit “保证派发任务独立”的前提上，但 Planner 由 LLM 生成依赖，论文没有报告面向隐藏依赖、工具副作用或错误独立性判断的安全验证。（定位：PDF p.4，§3.3；验证路径：带读写集合/副作用标注的依赖审计与冲突检测）

## 6. 可抽取 Operator 与真实可记录 Failure

### Operator（仅作独立二读抽取，不生成 Card）

- [AUTHOR_FACT] `query_to_dependency_dag`：用 Planner 将自然语言输入分解为工具任务、参数和 DAG 依赖，占位符 `$id` 表示数据流。（定位：PDF p.4，§3.1、Fig.2）
- [AUTHOR_FACT] `dependency_ready_greedy_fetch`：依赖满足即贪心派发，并把占位符替换为前驱实际输出。（定位：PDF p.4，§3.2）
- [AUTHOR_FACT] `async_parallel_execute_with_task_memory`：对独立任务异步并发执行，为每项任务保留独立中间 memory。（定位：PDF p.4，§3.3、Fig.2）
- [AUTHOR_FACT] `stream_plan_to_execution`：Planner 逐任务流式产出，令 planning 与 execution 重叠。（定位：PDF p.5，§4.2；p.15，Table C.1）
- [AUTHOR_FACT] `observation_conditioned_replanning`：将执行结果反馈 Planner，按运行时观察生成下一轮 DAG。（定位：PDF p.4–5，§3.4；p.8，§5.3）
- [AUTHOR_FACT] `finish_join_or_replan_gate`：硬编码 finish/join 汇总结果并决定回答或等待/重规划。（定位：PDF p.20–21，Appendix H）
- [READER_INTERPRETATION] WebShop 的“搜索后并行访问全部候选商品”更像 benchmark-specific exploration policy，而不是 LLMCompiler 通用内核 Operator；若抽取，应单独标为实例化策略。（依据：PDF p.8–9，§5.4）

### Failure（论文实际观察）

- [AUTHOR_FACT] `react_premature_early_stop`：Movie Rec 中 ReAct 约 85% 样本未完成 8 次搜索即作答，且较少调用与较低准确率相关。（定位：PDF p.13，Fig. A.1–A.2）
- [AUTHOR_FACT] `react_repetitive_call_divergence`：HotpotQA 中约 10% ReAct 样本超过 4 次调用，常进入循环/超过上下文，相关组准确率低于 10%。（定位：PDF p.14，Fig. A.3–A.4）
- [AUTHOR_FACT] `planner_wrong_dependency_id`：Planner 把错误 identifier 作为后继输入，形成错误 DAG；在作者的 ParallelQA 失败分析中共有 3 个 Planner 实例。（定位：PDF p.15，Appendix B）
- [AUTHOR_FACT] `executor_attribute_or_unit_error`：math tool 选择错误属性或单位换算错误，占总失败归因中的主要部分。（定位：PDF p.15，Appendix B）
- [AUTHOR_FACT] `final_join_reasoning_error`：最终阶段即使收集了 observations，仍可能选择错误极值或得出错误结论。（定位：PDF p.15，Appendix B）
- [AUTHOR_FACT] `planner_overhead_and_join_straggler`：Planner/answer 串行开销及最慢并行任务限制实际加速；这是性能 failure/bottleneck，不是样本正确性 failure。（定位：PDF p.16–17，Appendix E.1）

## 7. 判断—页码/章节/图表定位汇总

| 判断主题 | 标签 | 页码与结构 | 短定位文本 |
|---|---|---|---|
| 串行 ReAct 改为 DAG 并行执行 | [AUTHOR_FACT] | p.2 Fig.1；p.4 Fig.2、§3.1–3.3 | “Parallel tool invocations”；“DAG of Tasks” |
| 动态重规划 | [AUTHOR_FACT] | p.4–5 §3.4；p.8 §5.3 | “feedback loop”；“replan” |
| 输入与用户配置 | [AUTHOR_FACT] | p.5 §4.1；p.20–21 App. H | “Tool Definitions”；“optional in-context examples” |
| 主要准确率/延迟结果 | [AUTHOR_FACT] | p.6 Table 1；p.9 Table 3 | “Accuracy”；“Latency” |
| token/cost 差异 | [AUTHOR_FACT] | p.6 Table 2 | “Input and output token consumption” |
| ReAct 两类失败 | [AUTHOR_FACT] | p.13–14 Fig. A.1–A.4 | “premature early stopping”；“repetitive function calls” |
| LLMCompiler 三类失败来源 | [AUTHOR_FACT] | p.15 App. B | “Planner, Executor, and final output process” |
| streaming 消融 | [AUTHOR_FACT] | p.15 Table C.1 | “w/o streaming”；“w/ streaming” |
| 延迟上限与瓶颈 | [AUTHOR_FACT] | p.16–17 App. E.1，Eq.1–6 | “planner overhead”；“stragglers” |
| 组合能力基线 | [AUTHOR_FACT] | p.18 Table E.3；p.19 Table F.4 | “Planning / Replanning / Parallel Execution” |
| ParallelQA 生成与筛选 | [AUTHOR_FACT] | p.21 App. I | “113 examples”；“labeled by humans” |

## 8. 解析文本与可视 PDF 是否冲突？

- [AUTHOR_FACT] 对第 1–22 页逐页比对后，未发现文本解析与可视 PDF 在标题、章节顺序、表格主要数值、公式编号或图号上的实质冲突。可视页中的双栏、图表与代码框均存在；解析文本在图示元素和双栏阅读顺序上会线性化，但本报告的关键数值均以可视表格复核。（定位：PDF p.1–22；重点复核 p.2 Fig.1、p.4 Fig.2、p.6 Tables 1–2、p.9 Table 3、p.13–14 Figs. A.1–A.4、p.15 Table C.1、p.16–17 Eq.1–6、p.18–19 Tables E.2–F.4、p.22 Fig. J.6）
- [AUTHOR_FACT] 发现的是论文内部文本/表格不一致，而不是解析器与可视 PDF 冲突：p.8 正文称 LLaMA-2 Game of 24 延迟改善 `2.01×`，p.6 Table 1 为 `2.09×`；可视 PDF 与解析文本在各自位置一致地保留了这两个不同数值。（定位：PDF p.6 Table 1；p.8 §5.3，“2.01× improvement”）
- [AUTHOR_FACT] Appendix A 开头把 `70.00 vs. 77.80` 描述为 “HotpotQA evaluation with LLaMA-2 70B”，但 p.6 Table 1 显示这两个数值实际属于 Movie Recommendation 的 ReAct 与 LLMCompiler；HotpotQA LLaMA-2 对应 54.74/57.83（或 ReAct† 54.40）。可视 PDF 与解析文本均如此，属于正文错配。（定位：PDF p.13 App. A 首段；p.6 Table 1）
- [OPEN_QUESTION] Game of 24 的 LLaMA-2 正确 speedup 应以原始逐例延迟重算；在未取得原始日志前，不能在 2.01× 与 2.09× 之间裁决。（验证路径：用 952.06/456.02 重算约为 2.09，并核对作者运行日志；这里只记录内部不一致）

## 独立二读结论边界

- [READER_INTERPRETATION] 论文充分展示了依赖感知规划、并行执行、streaming 与 replanning 组成的可复用编排框架，并在给定 benchmark 上报告明确的延迟、token/cost 与部分准确率收益；但准确率收益同时受到调用预算、上下文组织、探索策略和 prompt 的共同影响，不能仅归因于并行性。
- [OPEN_QUESTION] 最小后续核验集合：加入匹配 DAG/调用预算的串行组合基线；公开完整 prompts 与逐例 tool traces；在检索失败、工具副作用、限流和隐藏依赖场景复测；重算并澄清 Game of 24 的 2.01×/2.09×。
- [AUTHOR_FACT] 本报告未合并任何首读内容，未生成正式 Card，未评价 Candidate，未运行科研 Reviewer。
