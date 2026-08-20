# P026 独立二读报告

## 0. Provenance 与阅读边界

- Invocation snapshot：`knowledge_base/corpus/reads/P026/read_2_attempts/r2-20260720-p026-a1/invocation.md`，Attempt ID `r2-20260720-p026-a1`。
- Canonical metadata：*Agent Lightning: Train ANY AI Agents with Reinforcement Learning*，arXiv:2508.03680，2025，Microsoft technical report。
- 指定 PDF：`knowledge_base/staging/plan05_sat_a1/P026_agent_lightning.pdf`。
- [AUTHOR_FACT] 本地实算 PDF SHA-256 为 `e223648a09b021785a46f60dd5ce13301622eca930ff91a5b45e971b53422561`，与 invocation 一致；PDF 共 20 个物理页，印刷页码也是 1–20。
- 阅读角色：fresh independent full-paper source checker；本报告不接触首读结论，不生成 Card/Evidence，不评价 Candidate。
- 隔离性质：`procedural_blinding`。没有可验证的文件级 allowlist，不能声称技术隔离。
- Actual model/version：不可见，记为 `unknown`。当前 canonical agent task：`/root/plan05_p026_second_reader`；平台 thread ID 不可见，记为 `unknown`。

以下页码均指 PDF 物理页；“短定位”只用于在原页快速定位，不替代上下文。

## 1. 方法究竟改变哪一步计算

### 1.1 execution 到训练样本的切分

- [AUTHOR_FACT] Agent Lightning 先把一次 agent execution 表示为 component calls 序列；每个 call 包含 component metadata、input、output，状态是 semantic variables 的快照。位置：p.5，§3.1.1，Eqs. (1)–(4)；短定位：“State and Call”“Semantic Variable”。
- [AUTHOR_FACT] 有奖励的 execution 被写成 `(call_i, r_i)` 序列；奖励可以是中间奖励，也可以只有 terminal reward。位置：p.5，§3.1.2，Eq. (5)；短定位：“only a terminal reward”。
- [AUTHOR_FACT] 真正交给 RL 更新的不是完整 execution DAG，而是从中筛出的待优化 policy LLM 调用，形成 `(input_t, output_t, r_t)` transitions。位置：p.7，§3.2.2，Eqs. (6)–(7)；短定位：“extract ... only the relevant information”。
- [READER_INTERPRETATION] 因而核心 changed computation 是“按单次 LLM invocation 切片并独立构造训练样本”，不是重新求解或显式解析完整 agent DAG。工具调用及其他非目标 component 可被记录为状态变化，但不会直接进入 policy-gradient loss，除非它们的结果进入某次 LLM 的 input 或被转成 reward。依据：p.6，§3.1.3，Figure 2；p.7，§3.2.2。

### 1.2 LightningRL 的两层 credit assignment

- [AUTHOR_FACT] 高层把一次 LLM invocation 生成的整段 token sequence 当成一个 action；低层仍由既有 single-turn RL 算法生成 token-level supervision。位置：p.7，§3.2.1；p.8–9，§3.3.2，Figure 3；短定位：“entire token sequence ... one action”“decomposed across tokens”。
- [AUTHOR_FACT] 当前实现的高层 credit assignment 并未学习细粒度价值：episode 内每个 action 都被赋予相同值，即最终 return `R`。位置：p.9，§3.3.2 首段；短定位：“each action ... same value”。
- [AUTHOR_FACT] 对 GRPO，作者按同一 task 多次执行得到 executions，将其拆成 transitions 后按 task 分组估计统计量；PPO、REINFORCE++ 被称为可类似适配。位置：p.9，§3.3.2；短定位：“grouped by task”。
- [READER_INTERPRETATION] “hierarchical”在本文已实现部分主要指两级分解：episode return → invocation/action value → single-turn token loss；第一层目前是 uniform terminal-return broadcasting，而非状态依赖、因果或 learned credit assignment。

### 1.3 训练—agent 执行的系统切分

- [AUTHOR_FACT] TA Disaggregation 将 trainer/LLM generation 放在 Lightning Server 一侧，把 application logic、agent framework 与工具放在 Lightning Client/agent runtime 一侧；server 暴露 OpenAI-like API。位置：p.9–10，§3.4.1，Figure 4；短定位：“compute-intensive LLM generation”“application logic and tools”。
- [AUTHOR_FACT] Server 分批派发任务、在 generation/training 阶段间切换，并为任务提供 endpoint；Client 执行 agent、采集 trace/reward、回传给 server。位置：p.10，§3.4.1；Appendix B p.20，Figure 8。
- [AUTHOR_FACT] Client 使用 OpenTelemetry/AgentOps 自动 instrumentation，或使用嵌在 OpenAI-like endpoint 中的基础 tracing；并提供同节点/跨节点 agent execution 并行。位置：p.10–11，§3.4.2；短定位：“Data Capture without Code Modification”“two-level parallelism”。
- [AUTHOR_FACT] AIR 被描述为将系统监控信号（例：tool-call return status）转成 intermediate rewards。位置：p.2，Introduction；p.11，§3.4.2；短定位：“Automatic Intermediate Rewarding”。
- [OPEN_QUESTION] §4 的三个实验没有说明是否实际启用 AIR、使用了哪些 monitoring signals、权重如何设定或与 terminal-only reward 做过何种对照，因此 AIR 的实验贡献无法由本文隔离。

## 2. 输入、输出、可用信息与干预时点

| 层级 | 输入/可用信息 | 输出 | 干预时点 | 原文定位 |
|---|---|---|---|---|
| Execution state | program counter、变量值、call stack、resource context 等的 semantic-variable 快照；具体 component 只看到其中必要/可见部分 | component call 导致的新 semantic-variable 值 | agent 正常执行期间 | [AUTHOR_FACT] p.5，§3.1.1，Eqs. (1)–(4)；p.6，Figure 2 |
| Policy observation/action | 当前 LLM call 的原始 input/context；可含 instruction、history、query、retrieved documents、template 结果 | 单次调用的完整 output token sequence，被视为一个高层 action | 每次待优化 LLM invocation | [AUTHOR_FACT] p.7，§3.2.1–3.2.2 |
| Credit assignment | execution 中选出的 policy transitions 与奖励；常见情形只有最终奖励 | 每个 action 的 assigned return；当前实现均等于 final `R` | rollout/execution 完成后、single-turn RL loss 前 | [AUTHOR_FACT] p.8–9，§3.3.2，Figure 3 |
| Token update | 每个 transition 自己的 input、output、assigned reward/advantage | policy parameters 更新 | server 的 training stage | [AUTHOR_FACT] p.8，Eq. (8)；p.9–10，§3.3.2/§3.4.1 |
| AIR | runtime monitoring signal | intermediate scalar reward | execution 中相关 transition 发生后、轨迹送训前 | [AUTHOR_FACT] p.2、p.11；[OPEN_QUESTION] 具体 timing/aggregation API 与实验用法未报告 |

- [AUTHOR_FACT] Figure 2 的 RAG 例子清楚显示：完整状态可含 UserInput、Query、Passages、Answer，但首个 LLM 只见 UserInput，Search 只见 Query，末次 LLM 见 UserInput 与 Passages。位置：p.5–6，§3.1.3，Figure 2。
- [READER_INTERPRETATION] “capture complete execution context in each state”不等于“policy 每次都看到完整状态”；真正训练 observation 是当前 call 的 input。该边界对判断是否存在额外信息泄漏很关键。依据：p.5 Eq. (4)、p.6 末段、p.7 §3.2.1。
- [AUTHOR_FACT] 多角色但单一共享 LLM 时，可通过 prompt 赋予不同角色并仅选择部分角色 transitions 训练。位置：p.7，§3.2.2 “Application to single-LLM multi-agent setting”；p.12，§4.1。
- [OPEN_QUESTION] Text-to-SQL 中 SQL writer、checker、rewriter 被称为“same LLM”但只优化 writer/rewriter transitions；如果三者共享同一参数副本，更新仍会改变 checker 的行为。论文未说明角色级 checkpoint/adapter 隔离，因此“selectively optimizing agents”是数据选择还是参数隔离并不清楚。

## 3. 最强基线与最近组合基线

### 3.1 本文实际测量的基线

- [AUTHOR_FACT] Figures 5–7 每个 panel 只画一条 Agent Lightning 的 train/test reward 曲线；没有独立方法对照、误差带或结果表。位置：p.12 Figure 5、p.13 Figure 6、p.14 Figure 7。
- [READER_INTERPRETATION] 因此本文唯一可见的“实测基线”是每条曲线的训练初始点/早期 checkpoint，即相同 agent workflow 与 Llama-3.2-3B-Instruct 在更新前后的纵向比较；它不是独立 comparator，也不能排除训练时长、采样或 checkpoint 选择效应。

### 3.2 原文给出的最近方法族，但未做 head-to-head

- [AUTHOR_FACT] Figure 3(b) 把“previous multi-turn GRPO”画成整条 trajectory 拼接并对非模型 token 加 mask；Figure 3(c) 才是本文 transition decomposition。位置：p.8，Figure 3；短定位：“concatenate”“masked”。
- [AUTHOR_FACT] Related Work 将 RAGEN、Trinity-RFT、rLLM、Search-R1 等归为多轮交互 RL，并称其通常采用拼接+mask；将 verl、OpenRLHF、TRL、ROLL、AReaL 列为 RL training systems。位置：p.13–15，§5.1。
- [AUTHOR_FACT] 对应用邻近工作，作者列出 RAG 的 Search-R1/R1-Searcher，以及 tool-integrated reasoning 的 ReTool/SimpleTIR。位置：p.15，§5.1 “Application-Specific RL Training”。
- [READER_INTERPRETATION] 对 changed computation 最接近的组合基线应是：同一 agent、同一 base model、同一 rollout/reward、同一 RL optimizer 与预算，仅把 transition decomposition 替换为完整 trajectory concatenation + correct loss/attention masking。本文没有运行这个控制实验。
- [READER_INTERPRETATION] 对系统主张最接近的组合基线应是：同一 agent 与训练配置，比较 Agent Lightning 的 Server/Client disaggregation 与在 verl 等训练框架内部重写 agent loop 的 coupled 实现，并测 LOC、吞吐、延迟、失败恢复和资源占用。本文没有该比较。
- [OPEN_QUESTION] 作者没有指明三个任务实际采用 GRPO、PPO 还是 REINFORCE++中的哪一个，也没有给出 closest-comparator config；因此不能从 Figure 3 的示意图推断实验确实与 multi-turn GRPO baseline 公平对照过。

## 4. 公平性、oracle、成本与潜在混杂

### 4.1 跨三类任务的共同点与不可比处

- [AUTHOR_FACT] 三项实验均使用 Llama-3.2-3B-Instruct，但分别使用 LangChain/Spider/SQL executor、OpenAI Agents SDK/MuSiQue/Wikipedia retriever、AutoGen/Calc-X/calculator。位置：p.11 Table 1；p.12–13，§4.1–4.3。
- [AUTHOR_FACT] Text-to-SQL 是 3 个 prompt-defined agents、训练其中 2 个；RAG 与 Math 各是单 LLM agent。位置：p.11 Table 1；p.12 §4.1；p.12–13 §4.2–4.3。
- [READER_INTERPRETATION] 共同 base model 说明框架在三种 agent SDK 上都能运行，但不同数据集、reward scale、工具与 workflow 使曲线不可横向比较；它们证明的是三个 case study 的可训练性，不是跨任务统一效应量。

### 4.2 Reward/oracle 边界

- [AUTHOR_FACT] Spider 的训练 reward 与测试指标均按最终答案是否正确/accuracy。位置：p.12，§4.1；短定位：“whether the final answer ... correct”。
- [AUTHOR_FACT] MuSiQue reward 为 `0.9 ×` gold-answer word-level F1 `+ 0.1 ×` format score；format 要求特定 `<think>/<query>/<answer>` 标记。位置：p.13，§4.2；短定位：“weighted combination”。
- [AUTHOR_FACT] Calc-X 的 final reward 与 test accuracy 均基于最终答案是否正确。位置：p.13，§4.3。
- [READER_INTERPRETATION] 训练时均依赖 dataset ground truth 形成 outcome reward；MuSiQue 还含显式格式 shaping。这些是训练 oracle/reward-function 差异，不能把三条曲线视为仅由同一算法改变造成。
- [OPEN_QUESTION] 原文没有明确声明 gold answer 只进入 reward service、绝不进入 policy observation 或 trace；按流程应当如此，但本文没有给出防泄漏检查。
- [OPEN_QUESTION] Spider 的“final answer correctness”判定器、MuSiQue F1 normalization、Calc-X answer extraction/等价性规则均未给出实现细节，可能影响 reward 噪声和测试可比性。

### 4.3 Model、prompt、token、tool-call 与检索混杂

- [AUTHOR_FACT] 三项实验报告了同一 base model 名称；RAG 还报告用 BGE embedding + cosine similarity 在约 2,100 万 Wikipedia documents 上检索。位置：p.12，§4.2。
- [OPEN_QUESTION] 未报告 model revision/checkpoint SHA、tokenizer、context/window、sampling temperature、top-p、generation length、prompt 原文、tool-call上限、最大交互轮数或超时规则。
- [OPEN_QUESTION] 未报告 MuSiQue 的 Wikipedia snapshot/index、retrieval top-k、BGE 精确版本以外的索引配置，亦未报告 Spider rewrite 次数上限和 Calc-X calculator protocol。
- [READER_INTERPRETATION] 因这些量未冻结，训练改善可能与更长 rollout、更多 tool calls、不同采样温度、prompt 格式或 checkpoint selection 混合；本文没有提供可排除这些解释的控制实验。

### 4.4 训练与系统成本

- [AUTHOR_FACT] 系统段声称 agent logic 不必与 GPU 共置，支持 intra-/inter-node execution parallelism，并称大 batch 可降低 rollout latency。位置：p.10，§3.4.1–3.4.2。
- [AUTHOR_FACT] Appendix A 的“almost ZERO code modification”示例保留原 `agent.py`，但新增 `train.py` 来构造 environment、Client、上传数据并调用 `client.train`。位置：p.19，Appendix A，Listings 1–2。
- [READER_INTERPRETATION] 这支持“agent logic 可保留”，但不是零集成成本；仍需 wrapper、reward/environment 接入、数据上传与 server URL。论文没有测改动 LOC 或工程工时。
- [OPEN_QUESTION] 未报告 GPU/CPU 型号与数量、wall-clock、token 数、rollout 次数、batch/group size、optimizer、learning rate、epochs、随机种子、训练/测试样本数、工具/检索调用量、网络/存储成本、失败重试率或吞吐。全文定向复核也未发现这些实验配置。
- [OPEN_QUESTION] Figures 5–7 的横轴是 steps，但三个任务的步数范围不同，且没有说明一步对应多少任务执行、transitions 或 tokens；因此无法归一化样本效率和计算成本。

## 5. 三类任务结果的独立核验

### 5.1 Text-to-SQL / Spider / LangChain

- [AUTHOR_FACT] 工作流依次含 SQL writer、SQL executor、checker、可能的 rewriter/final answer；writer/checker/rewriter由同一 LLM 配不同 prompts 扮演，训练选择 writer 与 rewriter。位置：p.12，§4.1。
- [AUTHOR_FACT] Figure 5 的 train reward 总体从低值上升后高噪声波动；test reward 的稀疏 checkpoints 总体上升但存在多次回落。位置：p.12，Figure 5(a)(b)。
- [READER_INTERPRETATION] 图支持“相对初始点总体改善”，但“stable”应收窄：训练曲线方差明显、测试点非单调；无 seeds/误差带，无法判断统计稳定性。

### 5.2 Open-domain QA / MuSiQue / OpenAI Agents SDK

- [AUTHOR_FACT] 单 LLM 先生成 query，再依据 retrieved documents 决定 refine query 或 answer；database 是 entire Wikipedia，检索为 BGE embedding cosine similarity。位置：p.12–13，§4.2。
- [AUTHOR_FACT] Figure 6 train reward 总体上升但噪声较强；test reward 先快速上升，随后平台并有轻微回落，再在末段上升。位置：p.13，Figure 6(a)(b)。
- [READER_INTERPRETATION] 曲线显示 composite reward 改善，不能分辨改善来自 answer F1、format compliance、query quality 还是更多 retrieval interactions；没有 reward-component 分解或 retrieval-quality 指标。

### 5.3 Math QA / Calc-X / AutoGen

- [AUTHOR_FACT] 单 LLM 决定何时调用 calculator、解释 tool output 并生成 final answer。位置：p.13，§4.3。
- [AUTHOR_FACT] Figure 7 train reward 总体上升后在较高区间持续噪声波动；test reward 快速上升后趋于平台。位置：p.14，Figure 7(a)(b)。
- [READER_INTERPRETATION] 图支持 test reward 随训练改善，但没有 no-tool、frozen-agent、single-turn RL 或 concat+mask 对照，无法把增益归因于 transition decomposition、TA Disaggregation 或工具使用学习中的某一项。

### 5.4 跨任务结论边界

- [AUTHOR_FACT] 作者据 Figures 5–7 概括“continuous and stable performance improvement”。位置：p.11 §4 开头；p.12–14 各任务结果段。
- [READER_INTERPRETATION] 三图确实都呈总体上升趋势，但均为单 run 风格曲线、没有 baselines、误差带、数值表或显著性检验。可核验结论应限定为“报告的三条单设置曲线相对其初始段总体提高”，不能升级为框架优于最强基线、样本更高效或普遍稳定。

## 6. 作者明示限制、负向结果与未测试边界

### 6.1 作者明示的限制/未来工作

- [AUTHOR_FACT] 对多 LLM，分别当作独立 MDP 会忽略 policy inter-dependencies，可能导致 suboptimal coordination；更原则化的 MARL/game-theory 方案仅被提出。位置：p.7，§3.2.2 “Extension to multi-LLM setting”。
- [AUTHOR_FACT] 当前 equal credit assignment 只是简单实现，更复杂的 heuristic/learned credit 或 high-level value function 属未来方向。位置：p.9，§3.3.2 “More sophisticated credit assignment”。
- [AUTHOR_FACT] long-horizon credit assignment、exploration、off-policy algorithms 被列为 future work。位置：p.15，§5.2 “Improvement on RL Algorithms”。
- [AUTHOR_FACT] 更彻底分离 trainer、rollout engine 与 agent workflows，以及 serverless environment/reward services、长上下文/serving 优化都在未来工作。位置：p.11 §3.4.2；p.15 §5.2。
- [AUTHOR_FACT] prompt optimization/Component of Interest 的更广泛优化支持也是 future roadmap；本文聚焦 LLM-centric optimization。位置：p.6 §3.1.3；p.15 §5.2 “More Optimization Methods”。

### 6.2 可记录的负向证据与缺失边界

- [AUTHOR_FACT] 作者明确承认独立优化多个 LLM 可能忽略依赖并产生次优协调；这是全文最清楚的机制级负向陈述。位置：p.7，§3.2.2。
- [AUTHOR_FACT] 系统段指出 RL exploration 会增加 agent crash、network interruption、invalid output、long-hanging tool call 等错误频率，并设计 retry/reassignment。位置：p.11，§3.4.2 “Error Handling and Robustness”。
- [READER_INTERPRETATION] 论文没有报告任何 empirical negative result、失败率、任务退化、训练崩溃、ablation 失败或超参敏感性；“没有报告负结果”不能被改写为“没有负结果”。
- [OPEN_QUESTION] 未测试/未报告：多 LLM joint training、真正长 horizon、动态 multi-agent 协作、模型规模扩展、异构模型、off-policy、AIR ablation、credit-assignment ablation、transition-vs-mask head-to-head、系统吞吐/扩展性、故障恢复、代码改动量与成本。
- [READER_INTERPRETATION] “ANY AI agent”依赖作者对 agent 的宽定义（含一个或多个 LLM calls），而实验只覆盖三个框架/三个任务/一个 3B base model；这是一项广泛适用性主张，不是被 exhaustive experiments 验证的事实。位置：p.3，§2；p.11 Table 1。

## 7. Operator 候选与 Failure 候选

以下仅为二读抽取候选，供主 Codex reconciliation，不是正式 Card。

### 7.1 Operator 候选

1. [READER_INTERPRETATION] **Invocation-transition slicing**：从完整 agent trace 中选择目标 policy LLM calls，把每次 `(current input, generated output, assigned reward)` 作为独立训练样本。证据：p.7 Eqs. (6)–(7)，p.8 Figure 3(c)。
2. [READER_INTERPRETATION] **Uniform terminal-return broadcasting**：把 episode final return 等值分配给 episode 内所有 policy actions，再调用既有 single-turn token loss。证据：p.8–9 §3.3.2。
3. [READER_INTERPRETATION] **Role/CoI transition selection**：按 prompt-defined role 或 component identity 选择哪些 transitions 进入优化，跳过其他 calls。证据：p.7 §3.2.2；p.12 §4.1；p.15 §5.2。
4. [READER_INTERPRETATION] **Training–Agent endpoint disaggregation**：trainer/model serving 留在 server，agent application/tools 留在 client，以 task-specific OpenAI-like endpoint 连接并回传 trace/reward。证据：p.9–10 Figure 4、§3.4.1；p.20 Figure 8。
5. [READER_INTERPRETATION] **Observability-to-transition capture**：用 OpenTelemetry/AgentOps 或 endpoint tracing 自动采集 calls/environment interactions。证据：p.10–11 §3.4.2。
6. [READER_INTERPRETATION] **Monitoring-to-intermediate-reward (AIR)**：把 tool status 等 runtime monitoring signal 映射为中间奖励。证据：p.2、p.11；但其训练配置与效果未验证，应标成 system-design operator，而非已证实有效 operator。
7. [READER_INTERPRETATION] **Failure containment/reassignment**：未捕获 crash 或 hanging tool call 被 runtime 检测后 retry/reassign，避免单个 agent instance 中断整体训练。证据：p.11 §3.4.2；无实测恢复率。

### 7.2 Failure 候选

1. [AUTHOR_FACT] **独立 MDP 的多策略协调失败风险**：多个 distinct LLM 分别优化会忽略相互依赖并可能产生次优协调。位置：p.7 §3.2.2。
2. [READER_INTERPRETATION] **长 horizon 下均匀 credit 混淆**：所有 actions 接收同一 final return，不能区分有益/有害中间决策；作者将更细 credit 与 long-horizon credit 列为未来工作。位置：p.9 §3.3.2；p.15 §5.2。本文未直接测得退化，不能标为 observed empirical failure。
3. [AUTHOR_FACT] **拼接+mask 的伸缩/工程风险（作者主张）**：累积上下文变长、自定义 mask 与 agent logic 耦合、位置连续性和 kernel/debug 复杂度。位置：p.9 §3.3.2；p.14 §5.1。没有 head-to-head 量化，故只能作为 claimed failure mode。
4. [AUTHOR_FACT] **agent rollout 的运行时失败面**：crash、network interruption、invalid output、long-hanging tool calls 在 RL exploration 下更频繁。位置：p.11 §3.4.2。没有实际发生率/恢复率。
5. [READER_INTERPRETATION] **证据归因不足**：单曲线、无 comparator/ablation/seed/成本记录，使 transition decomposition、credit assignment、TA disaggregation 与 AIR 的各自因果贡献不可分辨。位置：p.12–14 Figures 5–7；全文实验配置缺失。这是报告证据边界，不是任务性能负结果。
6. [OPEN_QUESTION] **共享参数下的角色选择泄漏**：只采样 writer/rewriter transitions 是否仍会通过共享权重改变 checker，原文未澄清。位置：p.7 §3.2.2；p.12 §4.1。

## 8. 解析文本与可视 PDF 的冲突核查

- [AUTHOR_FACT] 已逐页读取 20/20 页文本层，并逐页核对可视版面；对 Figures 1–8、Table 1、Eqs. (1)–(8) 与 Listings 1–2 做了重点视觉复核。
- [READER_INTERPRETATION] 未发现会改变作者方法或结果含义的文本—视觉冲突，但存在以下解析层限制：
  - p.1 左侧竖排 arXiv identifier/date 被文本抽取器插入摘要与正文行中；视觉页显示其只是页边元数据。
  - p.5、p.7–8 的公式在纯文本中出现换行/上下标顺序错乱；视觉复核后按 Eqs. (1)–(8) 的排版解释。
  - p.2、p.6、p.8–9、p.12–14、p.20 的图结构与曲线信息不能由 caption 文本完整恢复；本报告的曲线判断来自可视图，不给出无法可靠读取的精确数值。
  - p.19 Listing 2 的缩进和语法着色在纯文本中损失；视觉页确认其确为新增 `train.py` wrapper，而不是对 `agent.py` 的行内修改。
- [OPEN_QUESTION] Figures 5–7 没有机器可读数表，低分辨率图像也没有 confidence intervals；任何精确 endpoint 数值都应向作者源码/原始日志核验，本报告不从像素估算后冒充精确结果。

## 9. 最小结论边界

- [AUTHOR_FACT] 论文明确提出并实现了 transition-based data interface、uniform two-level credit path、TA Disaggregation/Client runtime，并展示三个任务中总体上升的单设置 reward curves。
- [READER_INTERPRETATION] 最稳妥的 changed-computation 概括是：“把复杂 agent execution 中的目标 LLM calls 切成独立 transitions，将 terminal return（当前均匀地）下放到每个 call，再复用 single-turn RL；系统上把 trainer/model endpoint 与 agent workflow/tools 分开。”
- [READER_INTERPRETATION] 论文不能支持的更强结论包括：优于最强多轮 RL baseline、transition decomposition 本身导致全部增益、AIR 已被验证、计算/样本效率更高、零集成成本、或对任意 agent/模型规模均成立。

## 10. 可观察访问与工具轨迹

1. 从任务上下文接收工作区根 `AGENTS.md` 规则；本地精确读取 `crl_agent_v3/AGENTS.md`、`CRL.md`、`CRL_ENVIRONMENT.md`。
2. 精确读取 `C:/Users/g/.codex/skills/paper-ingestion-and-evidence-builder/SKILL.md` 及其直接要求的 `references/rules.md`、`references/output_schema.md`、`references/checklists.md`。
3. 精确读取本 attempt 的 `invocation.md` 与 `knowledge_base/templates/second_read_prompt.md`。
4. 对 invocation 指定 PDF 执行本地 SHA-256、PyMuPDF page count/metadata/逐页文本与版式元素检查；逐页读取 p.1–20。
5. PDF 直接交给本地图像查看器未能处理；随后仅在内存中用 PyMuPDF 渲染页面，不写临时图像。逐页检查全部 20 页版面，并重点放大 Figures 5–7、Table 1、Listing 2 与 Figure 8。
6. 只在同一 PDF 的已读文本中定向复核 `baseline/seed/token/GPU/oracle/cost/budget/batch/learning rate/epoch/GRPO/PPO/mask/ablation/variance/prompt/tool call/reward/accuracy` 等词及命中上下文。
7. 未使用网络；未枚举工作区；未读取 read_1、Cards、其他报告、Corpus Report、saturation/retrieval/blind 文件；未读取 P056/P057 内容。
8. 唯一写入目标是本文件 `knowledge_base/corpus/reads/P026/read_2_attempts/r2-20260720-p026-a1/report.md`，写入方式为 `apply_patch`。
