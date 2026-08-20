# P059 独立二读报告

## 0. 读取身份、来源与边界

- paper_id：`P059`
- attempt_id：`r2-20260720-p059-a1`
- 论文：*Multi-Agent Collaboration via Evolving Orchestration*（NeurIPS 2025；arXiv:2505.19591）
- 冻结 PDF：`knowledge_base/staging/plan05_sat_a1/P059_evolving_orchestration.pdf`
- PDF SHA-256：`244c86ebd95a9fa7ca06539854186ea3dcdbf794ceb6e7827fff6e642e647bf6`
- 冻结提示词 SHA-256：`ffb7c12e663f44318d8eda1c270cbc26ad66665fd803247a2ab66a8f23fa333a`
- 完成时间：`2026-07-20T02:20:39+08:00`
- 执行身份：`/root/plan03_blind_evaluator_v1`；模型具体产品名/版本在本上下文中不可验证，故不作推断。
- provenance：`reused independent reader thread due platform thread cap`

[AUTHOR_FACT] 本报告逐页读取了指定 PDF 的全部 28 个物理页；文本层由 PyMuPDF 分段提取，版面层由 pdfjs-dist 与 Canvas 在内存中渲染并逐页核对，未落地任何中间渲染文件。

[READER_INTERPRETATION] 本线程此前承载过与 P059 无关的 P056/盲读上下文，因此它不是“全新空线程”；但本次首次接触 P059，且没有利用任何 P059 的一读结论、卡片、饱和度材料或其他报告。

[AUTHOR_FACT] 本次实际访问仅包括：工作区与项目 `AGENTS.md`、`CRL.md`、`CRL_ENVIRONMENT.md`，`paper-ingestion-and-evidence-builder` 技能及其 `rules.md`、`output_schema.md`、`checklists.md`，`pdf` 技能，P059 本 attempt 的 `invocation.md`，冻结二读提示词，以及上述指定 PDF。

[READER_INTERPRETATION] 本次没有访问 P059 `read_1`、Cards、Evidence、其他 read_2 报告、饱和度报告、检索记录或互联网，也没有枚举工作区。由于 invocation 明确限定为 report-only 独立二读，技能通常要求的路由筛选、索引写回、Cards/Evidence 生成均未执行。

## 1. 改变了什么计算

[AUTHOR_FACT] 论文把多智能体系统表示成有向图：节点是 agent，边表示依赖与信息流；最小 agent 由基础模型、推理/提示模式和工具组成。（物理页 2–3，§2，定位：`a=(m,r,t)` 与 `G=(V,E)`）

[AUTHOR_FACT] 核心改变不是预先固定工作流，而是由一个中心化 orchestrator/“puppeteer”在每个时间步依据当前全局状态和任务，串行选择下一名 agent。被选 agent 读取自己的局部状态与全局状态，产生输出并更新共享状态；遇到 terminator 或资源上限即停止，最后聚合已生成输出。（物理页 3，§2，式 (2)–(4)，定位：`a_t`、`S_{t+1}=Phi(S_t,o_t)`、terminator）

[AUTHOR_FACT] orchestrator 用完整轨迹的终局回报通过 REINFORCE 更新；回报同时含任务正确性/质量和按步 token/FLOP 成本，成本项为 `F log(1+t/phi)`，实验默认 `lambda=0.1`、`gamma=0.99`。（物理页 4–5，§2，式 (5)–(6)，定位：RL Adaptive Evolution / Experimental Setup）

[READER_INTERPRETATION] 因而论文真正新增的计算模块是“状态条件化的下一-agent策略 + 在线轨迹级策略优化 + 可提前终止的序列执行”，不是单纯扩大 agent 数量。执行轨迹按时间展开是序列；论文再按 agent 身份折叠成图时，同一 agent 的重复激活可形成自环或周期，二者不应混为时间环路。（物理页 7–9，§3.3，图 4–6）

## 2. 输入、输出、可用信息与干预时点

[AUTHOR_FACT] 系统输入是任务 `tau`；每一步决策可用信息是当前全局状态 `S_t` 和任务，当前 agent 的输出再写回状态。论文将该决策过程表述为满足 Markov 性。（物理页 3，§2，式 (2)–(4)，定位：Dynamic Orchestration）

[AUTHOR_FACT] 最终输出由聚合函数从累计状态/各 agent 输出得到；实验默认每个 episode 最长 4 步，以 majority voting 聚合，并允许最多 3 路并行探索。（物理页 3、5，§2、§3.1，定位：termination / implementation details）

[AUTHOR_FACT] 对有标准答案的任务，终局任务奖励是二元正确性；开放式任务使用 `[0,1]` 质量分。策略初始化采用一个基于 Llama-3.1 的奖励模型变体。（物理页 4–5，式 (6) 后说明与 §3.1 脚注）

[READER_INTERPRETATION] 干预发生在运行中的每个 agent 选择点以及终止点，而非仅在任务开始前选定一张固定图。论文没有给 agent 内部推理步骤中更细粒度的 orchestrator 干预。

[OPEN_QUESTION] 开放式任务的质量评估器、校准方法及其与最终报告指标的关系没有被充分交代；闭卷任务使用标准答案训练则构成明确的训练期 oracle。训练样本与最终评测样本的严格隔离方式也需要进一步核实。（物理页 4–5、17，式 (6)、附录 A.2）

## 3. 最强与最近的复合基线

[AUTHOR_FACT] 表 1 比较了单模型、Self-Refine、AFlow、MacNet、EvoAgent，以及同一基础模型驱动全部 agent 的 Puppeteer-Mono；默认 Puppeteer 使用异构模型池。（物理页 5–6，§3.1–3.2，表 1）

[READER_INTERPRETATION] 在已实测基线中，结构上最近的是 MacNet（静态 DAG 多智能体）与 AFlow（搜索/代码化工作流）；EvoAgent 是最近的演化式多智能体生成对照；Puppeteer-Mono 则最适合隔离“动态编排”与“异构强模型路由”的贡献。

[AUTHOR_FACT] Mimas 平均分中，AFlow 是最强外部复合基线（0.5364）；Puppeteer 初始/演化后为 0.6273/0.6324，Puppeteer-Mono 为 0.5068/0.6147。Titan 中 AFlow 同样是最强外部复合基线（0.6899）；Puppeteer 为 0.6893/0.7731，Puppeteer-Mono 为 0.6671/0.7453。（物理页 6，表 1，定位：Average 列）

[READER_INTERPRETATION] Titan 初始 Puppeteer 的均值 0.6893 并未高于 AFlow 的 0.6899；主要增益出现在 RL 演化后。Puppeteer-Mono 的演化增益支持动态策略有独立作用，但不能完全消除训练计算、探索和聚合预算差异。

[OPEN_QUESTION] 相关工作中与“运行时动态路由”更接近的 DyLAN、MAS-GPT、GPTSwarm 等没有进入表 1 的直接实验比较，因此“最近既有动态方法”这一基线槽位仍不完整。（物理页 2，§1/Related Work；物理页 5–6，表 1）

## 4. 模型、token、工具调用、提示词与 oracle 混杂

[AUTHOR_FACT] Mimas 池包含 Qwen2.5 7B/14B、Llama 3.1 8B、Llama 3.2 3B、Mistral 7B、Mistral-Nemo 12B；Titan 池包含 GPT-4 Turbo、GPT-4o-mini、Gemini 1.5 Pro/Flash、Claude 3 Sonnet/Haiku、Qwen2.5 72B、Llama 3.1 405B。（物理页 5，§3.1，定位：Agent Subspaces）

[READER_INTERPRETATION] 默认 Puppeteer 同时改变了模型身份、模型规模、提示角色和工具能力，因此其对单模型或固定拓扑基线的优势不是纯粹的 topology effect。Puppeteer-Mono 缓解模型异构混杂，但仍保留多步执行、训练和投票聚合的额外计算。

[AUTHOR_FACT] 工具角色包括 `read_file`、`search_arxiv`、`search_bing`、`access_website`、`run_python`；推理角色包括 reasoning、critique、reflect、question、summarize、conclude、modify、planning。工具 agent 的提示词负责生成 JSON 参数，并非在该提示词中直接执行工具。（物理页 21–22、24–28，附录 B，表 2、图 12–16）

[READER_INTERPRETATION] “agent 数量”不等于实际模型调用数或工具调用数；生成工具参数之后的外部执行、orchestrator 自身推理、最多 3 路探索和 majority vote 都可能增加未单列的开销。只比较 token 数也无法反映异构模型的价格、FLOP、时延和工具成本。

[AUTHOR_FACT] 作者称各基线在相同设置下重跑，但附录同时说明 AFlow 的推理期搜索与 Puppeteer 的梯度训练在计算形态上根本不同，直接比较计算成本“不适当”；在线训练与推理交织，也难以隔离训练成本。（物理页 5，§3.1；物理页 22，附录 C，表 3 后段）

[READER_INTERPRETATION] 因此“相同设置”不能解释为端到端 compute-matched。表 1 的效果比较与图 2–3/7–9 的效率趋势应分开阅读；后者主要展示 Puppeteer 自身训练轨迹，不是所有基线在等预算下的统一成本前沿。

[OPEN_QUESTION] 论文需明确：各基线的总模型调用、并行探索、聚合调用、工具执行、orchestrator 调用、训练更新和 wall-clock 是否计入；成本奖励在实际实验中使用 token 还是 FLOP；不同提供商模型 token 的计量是否可比。

## 5. 主要结果、负结果与未经检验的边界

[AUTHOR_FACT] Titan 上默认 Puppeteer 从初始平均 0.6893 上升到 0.7731，Mono 从 0.6671 上升到 0.7453；Mimas 上默认版本只从 0.6273 上升到 0.6324，而 Mono 从 0.5068 上升到 0.6147。（物理页 6，表 1）

[AUTHOR_FACT] Mimas 默认 Puppeteer 并非所有任务都改善：GSM-Hard 从 0.5600 降至 0.5400，SRDD 从 0.6653 降至 0.6266；CommonGen 仅从 0.7139 升至 0.7333。（物理页 6，表 1，相关任务列）

[AUTHOR_FACT] Titan 的训练趋势通常减少 token 和所用 agent 数；Mimas 中 agent 数较稳定，token 降低更多来自选择较低成本 agent。附录进一步说明，Mimas 若干任务并无一致 token 降低，少数任务也没有显著上升趋势。（物理页 7，§3.2，图 2–3；物理页 17–19，附录 A.1–A.2，图 7–9）

[AUTHOR_FACT] 作者将不稳定性归因于每项任务仅约 200 个优化样本，以及固定的最大 agent 序列长度可能不适合较弱模型；初始/演化阶段的切分只是评估便利，不代表模型本身发生阶段性改变。（物理页 17，附录 A.2）

[AUTHOR_FACT] 宽度/深度增加并非单调改善；默认 `W4D2` 被报告为性能—成本折中，继续增加会带来冗余、成本和可能的性能下降。（物理页 9，§3.4，定位：Hyper-parameters Analysis）

[AUTHOR_FACT] 折叠后的平均图密度从 1.0829 升到 1.4479；长度 1/2/3/4 的周期计数分别由 0.52/1.17/0.17/0.00 变为 0.62/1.40/0.38/0.06。（物理页 8–9，§3.3，图 5–6）

[READER_INTERPRETATION] “更紧凑且更循环”与性能同步出现，但论文未做保持 token、模型和性能预算一致的去周期/去密度干预，故这只能作为机制相关证据，不能证明周期结构导致提升。活跃 agent 更少而折叠图密度更高并不矛盾，但密度定义依赖活跃节点子集。

[AUTHOR_FACT] ALFWorld 只展示了单一 GPT-4o-mini、最大链长 50、每步一个 admissible action、探索数 1 的案例流程；正文/附录未给出相应的量化基线表或统计检验。（物理页 20–21，附录 A.4，图 11）

[READER_INTERPRETATION] 因而 embodied 证据是定性可行性示例，不能支持跨环境泛化或优于基线的结论。

[AUTHOR_FACT] 作者列出的限制包括：仅使用粗粒度最终输出/token 奖励而无中间监督；agent 和工具集合固定；复杂互动中偶发误协调或 deceptive agreement。（物理页 22–23，附录 D，定位：Limitations）

[OPEN_QUESTION] 尚未充分检验的边界包括：更长时程任务、不同 agent 池与新工具的在线加入、无标准答案且奖励模型偏置明显的任务、真实工具失败/延迟、跨任务迁移、训练集外的严格 held-out 泛化，以及在等训练+推理总预算下的比较。

## 6. Operator 候选（供主 Codex 后续裁决，不是 Candidate 评分）

1. [READER_INTERPRETATION] **O1：当前状态条件化的中心化串行路由。** 每步依据 `S_t,tau` 选下一 agent，以动态序列替代静态 DAG。（物理页 3，式 (2)–(4)）
2. [READER_INTERPRETATION] **O2：成本塑形的轨迹级策略更新。** 用终局任务回报和逐步 token/FLOP 成本共同执行 REINFORCE。（物理页 4，式 (5)–(6)）
3. [READER_INTERPRETATION] **O3：terminator/资源上限控制的自适应停止。** 路径长度由策略和预算共同决定。（物理页 3，§2）
4. [READER_INTERPRETATION] **O4：异构 agent 子空间路由。** 单一动作同时决定模型、推理角色与工具组合；Mono 是其消融方向。（物理页 2、5–6，agent 定义与表 1）
5. [READER_INTERPRETATION] **O5：重复 agent 激活形成的折叠回访结构。** 可表达自我修订、回溯和跨分支信息复用，但目前只获得观察性机制证据。（物理页 7–9，图 4–6）

## 7. Failure 候选（供主 Codex 后续裁决，不是 Candidate 评分）

1. [READER_INTERPRETATION] **F1：终局奖励代理与长程 credit assignment。** 粗粒度任务/成本奖励可能把错误归因给整条轨迹。（物理页 4、22–23，式 (6)、Limitations）
2. [READER_INTERPRETATION] **F2：固定 agent/tool 池导致能力上限。** 策略只能重排既有组件，不能补充缺失能力。（物理页 22–23，Limitations）
3. [READER_INTERPRETATION] **F3：拓扑容量过大引发冗余和退化。** 增宽、加深并非单调有效。（物理页 9，§3.4）
4. [READER_INTERPRETATION] **F4：弱模型池的效率信号不稳定。** Mimas 的 agent 数或 token 未在所有任务下降。（物理页 7、17–19，图 2–3、7–9）
5. [READER_INTERPRETATION] **F5：有限在线样本导致早期下降或无显著趋势。** 约 200 个优化样本与固定最长序列可能不足。（物理页 17，附录 A.2）
6. [READER_INTERPRETATION] **F6：演化后任务级回退。** Mimas 默认版本在 GSM-Hard 与 SRDD 上出现明确下降。（物理页 6，表 1）
7. [READER_INTERPRETATION] **F7：多 agent 误协调与 deceptive agreement。** 作者明确承认复杂互动中的该类失败。（物理页 22–23，Limitations）
8. [READER_INTERPRETATION] **F8：结构—效果的因果混淆。** 周期/密度与提升共现，却没有 matched causal ablation。（物理页 8–9，图 5–6）
9. [READER_INTERPRETATION] **F9：异构模型与总计算预算混杂。** 强模型路由、投票、探索和训练成本可能解释部分增益。（物理页 5–6、22，表 1、表 3）
10. [READER_INTERPRETATION] **F10：长时程 embodied 结论证据不足。** ALFWorld 仅有案例图，缺少量化对照。（物理页 20–21，图 11）

## 8. 解析文本与视觉 PDF 核对

[AUTHOR_FACT] 文本层与视觉层均覆盖物理页 1–28。视觉核对确认：表 1 位于物理页 6；图 2–3 位于页 7；图 4–6 位于页 8–9；附录效率图位于页 17–19；ALFWorld 设置/案例位于页 20–21；agent 类别、资源表与限制位于页 22–23；角色提示词位于页 24–28。

[READER_INTERPRETATION] 未发现影响本报告结论的文本解析—视觉版式冲突。数学符号在纯文本中有少量字符归一化损失，因此本报告的式号和语义以视觉页为准；本报告引用的表 1 数值与视觉表格一致。本报告未对表中的匕首符号作显著性解释，因为当前可见页没有提供足以无歧义解释该符号的图例。

## 9. 独立性声明

[READER_INTERPRETATION] 本报告是冻结输入下的第二遍独立阅读记录，只提供作者事实、读者解释、开放问题、Operator/Failure 候选及精确物理页定位；未自动调和一读结论，未创建或修改 Cards/Evidence，未执行 Candidate 评价、novelty/prior-work 审查或任何 Commissioning Cycle。
