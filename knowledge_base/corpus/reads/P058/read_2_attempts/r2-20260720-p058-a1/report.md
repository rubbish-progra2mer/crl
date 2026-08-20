# P058 独立二读报告

## 0. Provenance 与输入边界

- Invocation snapshot：`knowledge_base/corpus/reads/P058/read_2_attempts/r2-20260720-p058-a1/invocation.md`，Attempt ID `r2-20260720-p058-a1`。
- Canonical metadata：*AFlow: Automating Agentic Workflow Generation*，ICLR 2025 / arXiv:2410.10762。
- PDF：`knowledge_base/staging/plan05_sat_a1/P058_aflow.pdf`。
- [AUTHOR_FACT] 本地实算 PDF SHA-256 为 `9be15f695f11dd5bc634c1c026bd2270eff3d3c4a53c4d9b51c012b7bd03d521`，与 invocation 一致；共 38 个物理页。
- Reader-context provenance：`reused independent reader thread due platform thread cap`。这不是 fresh empty context；独立性仅指本轮未读取 P058 的 read_1、Cards、其他报告、saturation/retrieval/blind 材料，也未接受其他读者结论。
- 隔离性质：`procedural_blinding`；App 没有提供可验证的文件级 allowlist，不能声称技术隔离。
- Actual model/version：不可见，记为 `unknown`。当前 agent task 路径为 `/root/plan05_p026_second_reader`（平台线程上限下复用）；平台 thread ID 不可见，记为 `unknown`。
- 本报告只做原文核源，不生成 Card/Evidence/manifest，不评价 Candidate。以下页码均为 PDF 物理页；短定位文本只用于回到原页。

## 1. 方法究竟改变哪一步计算

### 1.1 从人工 workflow 设计改为代码 workflow 搜索

- [AUTHOR_FACT] 论文把 workflow `W` 定义为由 edges 连接的一系列 LLM-invoking nodes；每个 node 的形式化参数包括 model `M`、prompt `P`、temperature `τ`、output format `F`。位置：p.4，§3.1，Figure 2；短定位：“Model M”“Prompt P”“Temperature τ”“Output format F”。
- [AUTHOR_FACT] Edge 可用 graph、neural network 或 code 表示；作者选择 code，理由是标准控制结构可表达顺序、条件、循环及 graph/network。位置：p.4，§3.1 “Edge”。
- [AUTHOR_FACT] 形式化搜索空间涵盖 node 参数与 edge structure，但实际 AFLOW 为提高效率固定 model、temperature 与 format，主要搜索 prompts 和 code-represented edges，并向 optimizer 提供预定义 operators。位置：p.5–6，§3.2，Eqs. (1)–(2)，Figure 3；短定位：“fixing key parameters”。
- [READER_INTERPRETATION] 实际 changed computation 不是在完整形式化空间联合优化所有 node 参数，而是：用 LLM 对一个可执行 Python workflow 做单步代码/prompt 修改，在 validation evaluator 上反复执行，再用树状成败经验选择下一父 workflow。

### 1.2 AFLOW 所称的 MCTS variant

- [AUTHOR_FACT] MCTS tree 的每个 tree node 是一份完整 workflow，而不是一个 LLM-invoking node。位置：p.6，§4 首段；短定位：“each tree node represents a complete workflow”。
- [AUTHOR_FACT] 搜索循环由 soft mixed probability selection、LLM-based expansion、execution evaluation、experience backpropagation 构成。位置：p.5 Figure 3；p.6–7 §4；p.7 Algorithm 1。
- [AUTHOR_FACT] 初始化从 blank/template workflow `W0` 开始；20% 数据为 validation、80% 为 test，seed 固定为 42。作者先将 blank template 在 validation data 上执行 5 次，再选择 score 高方差的问题形成最终 validation subset。位置：p.6，§4 “Initialization”。
- [AUTHOR_FACT] Selection 在 top-k workflows 与初始 workflow之间结合 uniform 与 score-based probability；主文 Eq. (3) 写 `α=0.4`、`λ=0.2`。位置：p.6–7，§4 “Selection”，Eq. (3)。
- [AUTHOR_FACT] Expansion 使用 LLM optimizer，读取所选 workflow 的 experience，生成 prompts 或通过改 code 改 node connections；每次要求 single modification，optimizer prompt 限制 graph complexity 不超过 10。位置：p.7，§4 “Expansion”；p.15，Appendix A.1。
- [AUTHOR_FACT] 每个生成 workflow 在 validation subset 上执行 5 次，取 mean 与 standard deviation；作者称重复执行虽增加单轮成本，但可提高反馈精度。位置：p.7，§4 “Evaluation”；p.19，Appendix A.6 lines 13–17。
- [AUTHOR_FACT] Backpropagated experience 记录 workflow performance、相对 parent 的 modification、相对 parent 成功与否；另将 performance 加入 global selection record。位置：p.7，§4 “Backpropagation”；p.26–28，Appendix C.1。
- [READER_INTERPRETATION] 该算法保留树状 parent/child 与回退，但原文未呈现经典 MCTS 的 visit counts、UCB/PUCT、rollout policy 或 cumulative value backup；Appendix A.6 更像“top-k 随机选择 + LLM 单步变异 + 重复验证”的 tree-structured stochastic search。应保留作者的“MCTS variant”表述，不把它扩写为标准 MCTS 等价实现。

### 1.3 Experience 与 execution feedback 改变了 optimizer 的可用信息

- [AUTHOR_FACT] Experience 包含所选 workflow 历次 modification 及其 improvement/failure，并包括精确 prediction logs 与 expected output。位置：p.7，§4 “Expansion”；短定位：“precise logs of predictions and expected output”。
- [AUTHOR_FACT] Execution feedback prompt 把表现较好但出错的日志交给 optimizer；Appendix C.2 展示 optimizer 从 score/error pattern 学到 `\boxed{}` 格式、简洁性与多答案格式。位置：p.29，Appendix C.2；短定位：“Below are the logs”。
- [READER_INTERPRETATION] 因此 execution feedback 不只是标量 reward：optimizer 可看到实例级 prediction、expected output 和错误日志。这显著增强了搜索信号，也构成 validation-label/oracle 边界，需与只见 aggregate score 的 workflow search 区分。

## 2. 输入、输出、信息边界与干预时点

| 阶段 | 输入与可用信息 | 输出 | 干预时点 | 定位 |
|---|---|---|---|---|
| Search-space setup | task type、blank/template workflow、fixed executor model/temperature/format、operator library、code interface | 可被修改的 prompt + code-edge 空间 | 搜索开始前 | [AUTHOR_FACT] p.5–6，§3.2，Figure 3 |
| Validation construction | 原始 20% split；blank workflow 五次执行分数 | 高方差 validation subset | 搜索开始前一次 | [AUTHOR_FACT] p.6，§4 Initialization |
| Selection | top-k/global scores、tree experience，且主文称保留 blank workflow 被选概率 | parent workflow | 每轮 expansion 前 | [AUTHOR_FACT] p.6–7，Eq. (3) |
| LLM expansion | parent code/prompt、success/failure modifications、prediction/expected-output logs、operator signatures | 单步修改后的 executable workflow | 每轮搜索 | [AUTHOR_FACT] p.7；p.15 Appendix A.1 |
| Execution evaluation | candidate workflow、validation subset、numeric evaluator `G` | 五次 score/cost、mean/std、logs | 每次 expansion 后 | [AUTHOR_FACT] p.7；p.19 Algorithm 1 |
| Experience update | parent、modification、average score、相对成败 | child experience 与 global result | 每轮 evaluation 后 | [AUTHOR_FACT] p.7；p.26–28 |
| Final use | 选出的 workflow + test instance + executor API | task answer与 test inference cost | 搜索结束后 | [AUTHOR_FACT] p.8–10 Tables 1–2/Figures 4–6；p.30 Appendix D |

- [AUTHOR_FACT] Operators 是人工预定义的 node combinations：Generate、Format、Review & Revise、Ensemble、Test、Programmer，以及基础 Custom。位置：p.6，§3.2；具体代码 p.16–18，Appendix A.4。
- [AUTHOR_FACT] Test operator 运行 public tests；MBPP 没有 public test 时，作者把每题第一个 test case 当 public test。位置：p.18，Appendix A.4 末段。
- [OPEN_QUESTION] Table 1 的手工 baseline 是否获得与 AFLOW-discovered workflows 相同的 public-test/tool access 未说明；若只有搜索出的 code workflow调用 Test/Programmer，则性能差异不仅来自搜索算法，还来自 workflow 可用工具/oracle 的差异。
- [OPEN_QUESTION] 高方差 validation subset 的阈值和最终样本数没有报告，无法判断 search feedback 的有效样本量、选择偏差或过拟合程度。

## 3. 最强基线、最近先行与组合基线

### 3.1 实际比较的基线

- [AUTHOR_FACT] 手工 baselines：IO、CoT、CoT Self-Consistency（5 answers）、MultiPersona Debate、Self-Refine（最多 3 rounds）、MedPrompt（3 answers、5 votes）。自动 workflow baseline 只有 ADAS。位置：p.8，§5.1 “Baselines”。
- [AUTHOR_FACT] Table 1 在相同 divided test set 上全部使用 GPT-4o-mini 执行，每种方法测试 3 次并报告平均。位置：p.8，Table 1 caption。
- [AUTHOR_FACT] 按 Table 1 的平均列，最强手工 baseline 是 CoT SC（76.0）；唯一自动 baseline ADAS 为 67.2；AFLOW 为 80.3。位置：p.8，Table 1。
- [READER_INTERPRETATION] “比手工方法平均提升 5.7%”是相对提升：`(80.3-76.0)/76.0≈5.7%`，不是 5.7 percentage points；“比 ADAS 提升 19.5%”同样近似相对提升：`(80.3-67.2)/67.2≈19.5%`。依据：p.3 contributions；p.8 Table 1。

### 3.2 GPTSwarm 与 ADAS 的邻近程度

- [AUTHOR_FACT] GPTSwarm 用 graph + reinforcement learning 优化，但作者认为其 graph representation 难表达 conditional states；ADAS 使用 code representation 和 linear history/list，目标最接近 AFLOW。位置：p.3，§2 “Automated Agentic Optimization”。
- [AUTHOR_FACT] AFLOW 与 ADAS 比较时都用 Claude-3.5-sonnet optimizer 和 GPT-4o-mini executor；AFLOW 20 rounds，ADAS 30 rounds。位置：p.8，§5.1 Implementation Details。
- [READER_INTERPRETATION] 表示空间最近的已测 comparator 是 ADAS；搜索结构邻近但未测的是 GPTSwarm。论文没有实测“code representation + GPTSwarm search”或“同 operators/feedback、仅把 linear history 换成 AFLOW tree/MCTS”的组合基线。
- [READER_INTERPRETATION] 最接近的公平组合基线应固定相同 blank template、operator set、optimizer/executor、validation subset、五次重复、总 optimizer tokens、总 workflow executions/API 美元和 early stopping，仅替换 selection/history：ADAS linear heuristic vs AFLOW tree search。现有 20 vs 30 iterations 不能证明计算预算相等。
- [OPEN_QUESTION] 原文没有给 ADAS 的每轮候选数、每候选五次重复与否、token/API cost或 early stopping，因此 Table 1 的 AFLOW–ADAS差异无法纯归因于 tree-structured experience/MCTS。

## 4. 公平性、oracle 与成本归因

### 4.1 模型、prompt 与执行预算

- [AUTHOR_FACT] AFLOW 用 Claude-3.5-sonnet 作 optimizer；executor 涵盖 DeepSeek-V2.5、GPT-4o-mini-0718、Claude-3.5-sonnet-0620、GPT-4o-0513。DeepSeek temperature=1，其余 temperature=0。位置：p.8，§5.1 Implementation Details。
- [AUTHOR_FACT] Table 1 固定 GPT-4o-mini 作为各方法 test executor，这是主性能表最重要的公平控制。位置：p.8 Table 1 caption。
- [READER_INTERPRETATION] 但 AFLOW 的搜索 prompt 明示 review/revise/ensemble、Python loops/conditions/ML techniques，并提供 operator library；这些是强人类先验。ADAS/GPTSwarm baseline 是否获得逐字相同 prompt、operators 与 code API 未说明。
- [OPEN_QUESTION] 未报告 optimizer/executor 的完整 system prompts、API sampling seeds、max tokens、context limit、retry policy、并发、版本冻结日期、stop sequences或每轮生成失败率；仅模型名、部分版本和 temperature 不足以精确复现。

### 4.2 Validation oracle 与工具边界

- [AUTHOR_FACT] Search 使用 numeric evaluation function；optimizer experience 可含 expected output，Test operator可运行 public tests，Programmer 可生成并执行 Python。位置：p.7；p.17–18 Appendix A.4。
- [READER_INTERPRETATION] expected output/public tests 是合法 validation-side feedback，但信息强于纯黑盒分数；它可能推动格式、测试适配或 validation-specific prompt，而不必学习一般 workflow principle。
- [AUTHOR_FACT] Appendix C.2 明示 optimizer 在不知道具体 scoring rule 时从日志学到 `\boxed{}` 格式；round 13 的通用 comma-separated instruction 反而干扰解题并降分。位置：p.29。
- [OPEN_QUESTION] 作者没有报告 hidden test 与 validation 的 prompt/template leakage audit，也未说明 expected outputs 是否逐实例完整展示、截断或脱敏。

### 4.3 主结果与模型迁移

- [AUTHOR_FACT] Table 1：AFLOW 在 HotpotQA/DROP/HumanEval/MBPP/GSM8K/MATH 上分别为 73.5/80.6/94.7/83.4/93.5/56.2，平均 80.3；六项均高于表中各 baseline。位置：p.8 Table 1，视觉对应 p.2 Figure 1。
- [AUTHOR_FACT] Table 2 的 HumanEval transfer 显示，用 GPT-4o-mini 搜索的 workflow 在 GPT-4o-mini 上为 94.7；用 DeepSeek 搜索的 workflow迁到 GPT-4o-mini 仅 90.8。作者据此承认不同模型需要不同 workflow。位置：p.8–9，Table 2 前后文字。
- [READER_INTERPRETATION] Table 2 支持一定 transfer，但也直接否定强 model-agnostic 解释：跨 executor 的 workflow 常仍优于 IO，却不一定接近针对该 executor 搜索的最优 workflow。

### 4.4 成本数值究竟包含什么

- [AUTHOR_FACT] 主文说明 cost 通过 token usage 计算 Pareto front；Figure 4 caption进一步限定为“执行 divided HumanEval test set 的总费用”。位置：p.8 Metrics；p.9 Figure 4 caption。
- [AUTHOR_FACT] Appendix D：DeepSeek 执行 `AFLOW (gpt-4o-mini)` workflow 的 score=0.9390、cost=$0.0291；GPT-4o IO score=0.9389、cost=$0.6371，费用比例约 4.57%，对应文中“4.55%”的近似陈述。位置：p.30，Appendix D。
- [READER_INTERPRETATION] 该 4.55% 是“已发现 workflow 的 test-time API inference cost”，不包含 Claude optimizer、20 rounds 搜索、每候选 validation 五次执行、高方差筛选、失败候选或人工 operator设计成本。全文没有“search cost”记录。
- [AUTHOR_FACT] Appendix D 的相同 executor 内，GPT-4o-mini AFLOW(gpt-4o-mini) 为 94.7/$0.0513，IO 为 87.02/$0.0223；性能更高但约 2.3 倍 test inference cost。位置：p.30。
- [READER_INTERPRETATION] “weaker model outperforms stronger model at lower cost”在特定 HumanEval 点上成立，但不能等价为 AFLOW 端到端更便宜；搜索 amortization 需要任务量、workflow reuse次数和发现成本。
- [OPEN_QUESTION] 成本表未计本地 code execution、public tests、latency、失败重试、并发/基础设施费用，也没有把不同 provider 的价格时间戳/缓存计费写入论文。

## 5. Ablation、负结果、限制与未测试边界

### 5.1 原文直接报告的负向结果

- [AUTHOR_FACT] GSM8K ablation 中，去掉预定义 operators 后仍可搜索到 93.1%，但 operators 可更快找到更高分 workflow；无 operator 时还自行生成 ensemble-like structure。位置：p.9 “Ablation Study”；p.10 Figure 5；p.23–24 Appendix B.1。
- [AUTHOR_FACT] GSM8K round 5 加入无额外 reasoning 的 custom review node 导致 accuracy下降；round 14 过度聚焦 “discount” 信息也降分。位置：p.9 “Case Study”，p.10 Figure 6。
- [AUTHOR_FACT] MATH trajectory 中，round 1→8 移除 Programmer 后分数 0.4873→0.4336；round 9→16 简化生成且丢失 review 后 0.5378→0.5210；若干 ensemble modifications 得分为 0。位置：p.26–28，Appendix C.1。
- [AUTHOR_FACT] Execution feedback 的 round 13 通用多答案逗号格式要求增加 comma-separated outputs，但得分低于较好 rounds，作者认为其可能干扰解题。位置：p.29，Appendix C.2。

### 5.2 一个硬约束与 judge score 的直接错位

- [AUTHOR_FACT] 开放式 novel task 明确要求 “exactly 20,000 words”；搜索出的 workflow 用 10 chapters，chapter prompt却写“approximately 10,000 words per chapter”。最终输出被作者报告为 27,000 words，而非 20,000。位置：p.33–35，Appendix F.2.1。
- [AUTHOR_FACT] 尽管违反精确字数，round 8 仍获 LLM score 20/20、human average 19.3，均排第一。位置：p.35，Table A1。
- [READER_INTERPRETATION] 这是可直接记录的 evaluator/constraint failure：LLM judge 与 human ranking重奖总体质量，却没有强制硬字数约束。它说明 open-ended AFLOW 可能优化 judge preference 而非完整 task contract。

### 5.3 作者范围限制与证据边界

- [AUTHOR_FACT] 主方法聚焦有 numerical evaluation functions 的 reasoning tasks；open-ended extension改用 GPT-4o judge，并只作为 Appendix F 讨论/案例。位置：p.6 “Tasks Scope”；p.31–32 Appendix F.1。
- [AUTHOR_FACT] 开放任务评估另聘 3 名人类标注者、$10/hour；novel 展示一个问题，idea case虽称测试 10 个问题，正文只展示一个代表例。位置：p.32–37，Appendix F.2。
- [OPEN_QUESTION] 未报告 annotator instructions/qualification、blindness、inter-annotator agreement、逐题分数、置信区间或 judge-human correlation；两张表的排名不能建立广泛 open-ended effectiveness。
- [AUTHOR_FACT] Appendix G 声称 search-space completeness依赖 code能表达全部有效关系、LLM 对有效修改具有非零概率；有限迭代最优性还要求 bounded evaluator、valid workflows和非零 improvement probability。位置：p.37–38，Appendix G。
- [READER_INTERPRETATION] 这些是强假设下的性质讨论而非有限预算证明；非零 improvement probability 本身不足以保证在固定 20 rounds 找到全局最优，尤其搜索空间近似无限、概率下界与可达路径长度均未给出。
- [OPEN_QUESTION] 未测试大型真实工具链、动态 agent、长期运行、非 API 模型、multi-objective安全/latency、workflow robustness under distribution shift、adversarial evaluator、完整搜索成本或跨 task workflow transfer。

## 6. 原文内部不一致与复现风险

1. [AUTHOR_FACT] 主文 p.7 Eq. (3) 写 `α=0.4, λ=0.2`；Appendix A.6 p.19 lines 36–40 写 `λ=0.4, α=0.2`。两者交换，且会实质改变 uniform/score weighting。
2. [AUTHOR_FACT] 主文 p.7 的 terminal condition 是“top-k average score 连续 n rounds 无改善”；Appendix A.6 p.19 line 24 是“Top k workflows remains unchanged in n rounds”。一个按均值，一个按成员身份，停止规则不等价。
3. [AUTHOR_FACT] 主文 p.6 与 §5.1 把 20%/80%称 validation/test；Appendix A.6 p.19 line 2 注释却写 80% 为 training。算法其余部分仍返回 `DT` 未用于 search，故更像注释错误，但应核实现码。
4. [AUTHOR_FACT] 主文 p.6 说 selection 包含 initial workflow以保持探索；Appendix A.6 p.19 `SelectParent` 只从 sorted top-k results采样，未显式加入 `W0`。实际实现需源码核验。
5. [OPEN_QUESTION] 以上冲突不能由 PDF 内部消解；任何复现或 baseline重跑必须先选择并记录实际参数/停止逻辑/候选集合，不能混用。

## 7. Operator 候选与 Failure 候选

以下仅为二读抽取候选，供主 Codex reconciliation；不是正式 Card。

### 7.1 Operator 候选

1. [READER_INTERPRETATION] **Code-workflow mutation**：让 optimizer 对完整可执行 workflow做单步 prompt/code-edge修改，而非只调 prompt或 graph weight。证据：p.4–7，§3–4；p.15 Appendix A.1。
2. [READER_INTERPRETATION] **Soft mixed top-k selection**：对高分 workflows 混合 uniform与softmax-score概率，并保留从空白路径重新探索的意图。证据：p.6–7 Eq. (3)；注意参数/候选集合与附录冲突。
3. [READER_INTERPRETATION] **Tree-structured modification memory**：按 parent/child保存成功与失败 modification、score和日志，使 optimizer回用局部路径经验而非线性拼接全部历史。证据：p.7；p.26–28。
4. [READER_INTERPRETATION] **Repeated execution evaluator**：候选在筛选后的 validation subset上执行五次，以 mean/std作为反馈。证据：p.7；p.19。
5. [READER_INTERPRETATION] **Execution-log feedback**：把错误 prediction、expected output与表现日志送回 optimizer，以发现格式或推理问题。证据：p.7；p.29。
6. [READER_INTERPRETATION] **Operator-seeded search**：提供 Generate/Format/Review/Revise/Ensemble/Test/Programmer作为高阶构件，提高产生有效 code的概率。证据：p.6；p.16–18；p.9–10 ablation。
7. [READER_INTERPRETATION] **High-variance validation focusing**：先用 blank workflow重复运行，挑高方差实例作为搜索反馈集。证据：p.6；p.19。

### 7.2 Failure 候选

1. [AUTHOR_FACT] **Linear-history overload（作者对 ADAS 的诊断）**：完整 workflows 随迭代线性累积导致信息量与无关信息膨胀，LLM难以提取有效修改。位置：p.25，Appendix B.2。论文没有在等预算控制下单独 ablate history structure。
2. [AUTHOR_FACT] **去掉 concrete computation 导致退化**：MATH 删除 Programmer 后 0.4873→0.4336。位置：p.28 Appendix C.1。
3. [AUTHOR_FACT] **丢失 review/quality control 导致退化**：MATH 0.5378→0.5210；GSM8K某些 review/prompt变更也降分。位置：p.9、p.28。
4. [AUTHOR_FACT] **泛化格式规则干扰内容**：comma-separated多答案通用要求增多、分数下降。位置：p.29。
5. [AUTHOR_FACT] **workflow 的模型依赖**：DeepSeek搜索 workflow迁到 GPT-4o-mini 为 90.8，低于 GPT-4o-mini自身搜索的94.7。位置：p.9 Table 2。
6. [AUTHOR_FACT] **hard-constraint evaluator miss**：要求精确20,000词，却生成27,000词仍被judge/human排第一。位置：p.33–35 Table A1。
7. [READER_INTERPRETATION] **成本归因遗漏**：只报最终 test inference dollars，未计搜索/optimizer/重复validation成本；不能据此声称端到端更便宜。位置：p.8–9、p.30。
8. [READER_INTERPRETATION] **oracle/tool-access混杂**：optimizer可见expected outputs，workflow可用public tests/Programmer，而baseline访问边界未对齐。位置：p.7、p.17–18。
9. [READER_INTERPRETATION] **搜索配置不可唯一复现**：`α/λ`、early stopping、W0候选与split注释在主文/附录冲突。位置：p.7、p.19。

## 8. 解析文本与可视 PDF 核查

- [AUTHOR_FACT] 已连续读取 38/38 页文本层，并逐页检查视觉版面；重点放大 Figures 1–6、Tables 1–2、Table D、Tables A1–A2、Algorithms 1、代码块与 Appendix C tree experience。
- [READER_INTERPRETATION] 未发现视觉图与相邻 caption/table 在核心数值上的反转，但存在明显解析限制：
  - p.1 左侧 arXiv identifier/date 被抽取到摘要正文行中；视觉页显示其只是竖排页边元数据。
  - p.2 Figure 1、p.4–5 Figures 2–3、p.9 Figure 4、p.10 Figures 5–6 的多栏图在纯文本中严重错序；主结果数值以视觉图和表格共同核对。
  - p.15–28、p.31–37 的长代码块在文本层丢失缩进/着色；视觉核对确认控制流与代码块边界，但省略号表示原文也未给完整可执行实现。
  - p.7 Eq. (3) 的行内抽取错位，视觉页确认主文参数确为 `α=0.4`、`λ=0.2`；p.19视觉页确认附录确实反写，而非 parser制造。
- [READER_INTERPRETATION] §6 列出的参数/停止规则/split差异是原文内部实质不一致，不是解析冲突。

## 9. 最小结论边界

- [AUTHOR_FACT] AFLOW 在固定 GPT-4o-mini test executor的六项主表中均取得最高报告均值，并展示 operators ablation、tree trajectories、model transfer与 HumanEval test-time cost表。
- [READER_INTERPRETATION] 最窄的 changed-computation概括是：“在固定 executor参数下，把 agentic workflow表示成可执行 code，对 prompt与control-flow做LLM单步变异，以top-k混合选择、重复execution反馈和tree-structured修改经验驱动搜索。”
- [READER_INTERPRETATION] 不能由本文直接推出的更强结论包括：标准MCTS本身造成全部增益、在等端到端成本下优于ADAS/GPTSwarm、完全无人为先验、搜索成本低于强模型、对模型完全agnostic、能可靠满足open-ended硬约束或有限20轮保证全局最优。

## 10. 可观察访问/工具轨迹

1. 精确读取必要项目规则：`crl_agent_v3/AGENTS.md`、`CRL.md`、`CRL_ENVIRONMENT.md`；工作区根规则由任务上下文提供。
2. 因任务匹配论文摄取核源，精确读取 `paper-ingestion-and-evidence-builder/SKILL.md` 及其直接要求的 `references/rules.md`、`output_schema.md`、`checklists.md`。
3. 精确读取 P058 本 attempt `invocation.md` 与统一 `knowledge_base/templates/second_read_prompt.md`。
4. 仅对 invocation 指定 `P058_aflow.pdf` 执行 SHA-256、PyMuPDF metadata/page count、p.1–38逐页文本读取、逐页内存渲染与关键图表放大；未写临时图片。
5. 仅在同一 PDF 已读文本中定向复核 `search cost/inference cost/token usage/public test/expected output/GPTSwarm/ADAS/variance/seed/convergence/4.55%` 等词及命中页码。
6. 未联网；未枚举工作区；未读取 read_1、Cards、其他论文读稿/报告、Corpus Report、saturation/retrieval/blind 文件；未读取或修改 P026 报告。
7. 唯一写入目标为本文件 `knowledge_base/corpus/reads/P058/read_2_attempts/r2-20260720-p058-a1/report.md`，写入方式为 `apply_patch`。
