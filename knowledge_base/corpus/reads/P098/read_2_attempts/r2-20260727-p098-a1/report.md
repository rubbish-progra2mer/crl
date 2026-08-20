# P098 独立二读报告（fresh reader, W06 扩充波次）

- 论文：Beyond Objective Equivalence: Constraint Injection for LLM-Based Optimization Modeling on Vehicle Routing Problems
- canonical metadata 核对：PDF 第 1 页左侧竖排水印为 "arXiv:2606.04816v1 [cs.AI] 3 Jun 2026"（视觉 Read 确认），与 canonical（arXiv 2606.04816v1, 2026-06-03, preprint）一致。[AUTHOR_FACT]（p.1，页边水印）
- 实测 SHA-256：f73aaa44ab843311d0676030081b8f1b9e18f9e9bb0bb0b9a87c761917b43ab3（与任务给定值一致）
- 实测物理页数：28 页（PyMuPDF page_count = 28）
- 抽取方式：PyMuPDF 逐页抽文本（28/28 页）；对 p.1（标题/Fig.1）、p.5（编码公式/Fig.3）、p.8（Table 2/3）、p.12（Table 4）做了 150dpi 渲染视觉抽查。
- 阅读日期：2026-07-27。本报告只依据 PDF 本身与任务内嵌问题清单，未读取任何 Card、read_1、reconciliation 或 Run 目录。

## Q1 方法究竟改变哪一步计算？

1.1 [AUTHOR_FACT] 方法不改变模型结构、解码过程或推理时流程；它改变的是训练管线中"接受信号"的计算：在数据合成的拒绝采样过滤器与 GRPO 的 per-rollout 奖励中，把单一的目标值等价检验（DIFF）替换为 DIFF+INJ 双验证器。定位：p.1 Abstract "The verifier is reused as a rejection-sampling filter during data synthesis and as a per-rollout reward in group relative policy optimization (GRPO)"；p.5 Sec 4.1 "Reuse. The same INJ implementation serves as the rejection-sampling filter in Stage 4 ... and as the per-rollout reward in GRPO ... ensuring identical signals"。

1.2 [AUTHOR_FACT] INJ 算子的具体计算：给定 (C, I, s)，执行候选脚本 C 得到 Gurobi 模型对象，把目标函数替换为常数（变成纯可行性查询），追加 addConstr 把探针解 s 编码进候选脚本的变量空间，返回求解器可行性判定 INJ(C,I,s) ∈ {Feasible, Infeasible}，与真值标签 ℓ(s) 比较得 0/1 信号。定位：p.3–4 Sec 3.3 "Constraint Injection. Given (C, I, s) ... replaces the objective with a constant, thereby turning the problem into a pure feasibility query, appends Gurobi addConstr calls"。实现细节见 p.18 Appendix D "executes Cregen to obtain the Gurobi model, copies the model, replaces the objective with a constant feasibility objective"。

1.3 [AUTHOR_FACT] SFT 阶段的改变体现在数据集组成：Stage 4 双验证拒绝采样只保留 DIFF 与 INJ 全部通过的样本（Table 1 规则：DIFF✓+INJ✓→Accept；DIFF✓+INJ×→Reserved；DIFF×→Discard）。定位：p.6 Sec 4.2 Table 1 "Rules for dual-verified rejection sampling"。SFT 损失本身是标准因果 LM 交叉熵（p.6 Eq. (10)），未被修改。

1.4 [AUTHOR_FACT] GRPO 阶段的改变体现在奖励函数：r(q,y) = λ_build·r_build + λ_diff·r_diff + λ_inj·r_inj，其中 r_inj(y,P) = |P|^{-1} Σ_{s∈P} 1[INJ(y,s)=ℓ(s)]，P = {s+} ∪ {s−_i}。权重为 0.2/0.5/0.3。定位：p.7 Eq. (11) 与 Sec 5.1 "reward 0.2rbuild +0.5rdiff+0.3rinj"。GRPO 目标（Eq. 12）为标准 clipped surrogate + KL，未做算法级修改。

1.5 [READER_INTERPRETATION] 因此这是一篇"验证信号工程"论文：计算图、优化器、策略梯度算法均为现成组件（LoRA SFT + GRPO），新颖性全部集中在 oracle 侧——用探针把约束层面的正确性转成可判定的可行性查询，再把该判定注入过滤与奖励两个时点。

## Q2 输入、输出、可用信息与干预时点

2.1 [AUTHOR_FACT] 任务定义：输入是自然语言 VRP 场景 q，输出是端到端 Gurobi 脚本 y = fθ(q)，"without intermediate scaffolding such as .lp files, formula templates, or symbol tables"。定位：p.3 Sec 3.2。

2.2 [AUTHOR_FACT] 训练样本是六元组 S = (I*, q, Cgold, Cregen, s+, {s−_i})：VRP 实例、问题陈述、专家 gold 脚本、教师再生成脚本、可行探针、单约束违反探针集。定位：p.4 Sec 4 "Each training sample is defined as a six-tuple"。

2.3 [AUTHOR_FACT] 可用信息（oracle 侧）：每个变体配有 OR 专家编写并在微型实例上验证的 gold 脚本 Cgold；Cgold 全程作为 oracle——验证探针可行性、播种问题陈述、作为 DIFF 参照。定位：p.4 "Cgold serves as the oracle throughout the pipeline"；p.5 Stage 1 "Each variant ships with a gold script Cgold, developed by OR experts and validated on micro-instances"。

2.4 [AUTHOR_FACT] 探针构造输入：变体特定启发式（最近邻插入 + 逐步资源检查）产 s+，失败则回退到 Cgold 限时求解（TimeLimit=15s, MIPFocus=1）；{s−_i} 由攻击算子从 s+ 派生，结构攻击只改访问序列，参数攻击额外把一个资源上界收紧到开区间 (g,b) 内（插值系数 0.85，Eq. 13）。定位：p.14 B.3、p.15–16 B.4/Eq. (13)。

2.5 [AUTHOR_FACT] 干预时点有两个，均在训练期：(i) 数据合成 Stage 4（SFT 数据过滤，样本级）；(ii) GRPO 每个 rollout 的奖励计算（rollout 级）。评测时不使用 INJ：四个基准只报 Pass@1（目标值容差 10^-3）。定位：p.6 Table 1；p.7 Eq. (11)；p.7 Sec 5.2 "We report Pass@1 on all benchmarks with an absolute objective tolerance of 10−3"。

2.6 [AUTHOR_FACT] INJ 的可注入性依赖输出协议约定：共享代码生成提示词强制路由变量命名为 x、arc-first 索引（x[i,j] 或 x[i,j,k]）、变量覆盖全节点集且不得用 tuplelist 预过滤弧。定位：p.26 Figure 10 "Route variable MUST be named x with name='x' in addVars, indexed arc−first"。若变量或节点索引无法可靠匹配，"the case is not used as a valid INJ verdict and the sample fails rejection sampling"（p.18 Appendix D）。

2.7 [AUTHOR_FACT] 索引重写路径要求教师返回一一对应的 node_id_map，验证器用它把探针路线翻译回候选脚本的内部索引空间。定位：p.17 C.1 "The rewrite call must also return a one-to-one node_id_map"；p.18 Appendix D "the recorded node_id_map is used to translate probe routes back"。

2.8 [READER_INTERPRETATION] 干预是纯"黑盒后置"的：INJ 不读代码文本、不做静态分析，只操作执行后得到的求解器模型对象。这使它对代码风格不敏感，但也使它强依赖 2.6 的命名/索引契约——契约由提示词而非方法本身保证。

## Q3 最强基线与最接近组合基线

3.1 [AUTHOR_FACT] 最强外部基线是 Gemini-3.1-Pro Preview：AVG 95.00（700 题合并计算），四基准 95.81/89.39/91.89/96.40；VRPCoder-GRPO AVG 93.00，在 B1/B2/B3 上胜出（96.13/96.97/93.24），在 B4 落后 8.40 分。定位：p.8 Table 2 及 p.7 Sec 5.3 "trails on Benchmark 4 by 8.40 points"。

3.2 [READER_INTERPRETATION] 注意 headline 表述的选择性：摘要说"outperforms Gemini-3.1-Pro Preview on three benchmarks"，这是准确的，但按合并 AVG（Table 2 的 AVG 列，逐题平均）Gemini 95.00 > VRPCoder-GRPO 93.00，即最强基线在总平均上仍领先。Table 2 视觉核对确认 Gemini 的 96.40 与 95.00 是加粗的最优值。

3.3 [AUTHOR_FACT] 最接近的组合基线是消融臂 "VRPCoder-GRPO w/o Injection"：同一底模、同一提示词、同一 DIFF+build 信号，仅去掉 INJ；SFT 臂用 7347 样本（比主管线多 550 个"过 DIFF 但挂 INJ"的样本），GRPO 臂用 855 个 frontier prompts（多于主管线的 716），奖励上限降为 0.7。结果 AVG 89.00 vs 93.00（+4.00），SFT 85.57 vs 88.43（+2.86）。定位：p.8 Table 3；p.19 Appendix E "No-injection ablation ... the additional 550 samples pass differential testing but fail constraint injection"。

3.4 [AUTHOR_FACT] 作者称该消融是保守比较："This gives the no-injection baseline a larger SFT set and a larger frontier-prompt pool"（p.8 Sec 5.4）。

3.5 [READER_INTERPRETATION] "更大数据 = 更强基线"的保守性论证只在数据同质时成立；这 550 个样本按方法自身的判定是含约束缺陷的，加入它们既是数据量优势也是噪声劣势——但这恰是 DIFF-only 管线真实会训练到的数据，所以作为"现实反事实"的组合基线是恰当的。

3.6 [AUTHOR_FACT] 其余基线组：开源通用（DeepSeek-V3.2 36.29 最高）、SFT 型 OR-LLM（ORLM 5.71、OptMATH 3.71）、RL 型 OR-LLM（SIRL-Gurobi-32B 15.00 最高）。定位：p.8 Table 2。

## Q4 结果是否可能来自模型、token、tool-call、prompt 或 oracle 差异？

4.1 [AUTHOR_FACT] 提示词差异客观存在：闭源与开源通用基线用共享代码再生成提示词（Figure 10），OR-LLM 基线"with their original prompts and solver settings"。定位：p.7 Sec 5.1；p.20 Appendix F "Trained models use the shared code-regeneration system prompt in Figure 10; OR-LLM baselines use their original prompts"。

4.2 [READER_INTERPRETATION] 主表（Table 2）中对 OR-LLM 基线的巨大差距（78+ 分）可能部分来自分布/格式失配：SIRL、ORLM、OptMATH 训练分布并非 VRP 场景式长文本；SIRL-Gurobi-8B 在 B3 上 0.00、ORLM 在 B2 上 0.00 这类极端值更像协议失配而非纯能力差。论文未对此做归因实验。

4.3 [READER_INTERPRETATION] Benchmark 1/2 由论文自己的合成管线（同一教师、同一 60 场景池、同一措辞风格）生成，且 B1 样本"retained after the same dual verifier procedure used for training data"（p.20 Appendix F）——即评测题本身经过与训练数据相同的过滤器。这使 B1/B2 对 VRPCoder 是主场分布，对 frontier 基线是客场；B1/B2 上的胜出不宜外推为一般 VRP 建模能力优势。外部来源的 B3（+1.35 vs Gemini）与 B4（-8.40）给出的信号更弱且混合。

4.4 [READER_INTERPRETATION] 教师/蒸馏混杂：训练数据由 Gemini-3.1-Pro Preview 与 Claude Opus 4.6 生成（p.17 Appendix C "We use Gemini-3.1-Pro Preview ... and Claude Opus 4.6 ... as the teacher LLMs"），而 Gemini-3.1-Pro Preview 同时是最强评测基线。主表的"学生 vs 教师"比较里，学生优势主要出现在教师自家分布（B1/B2 由教师生成再被过滤）上，这与其说是超越教师，不如说是"教师输出经 Cgold 双验证过滤后的再蒸馏"效应。

4.5 [AUTHOR_FACT] 关于消融（论文的 Q2）：两臂共享底模（Qwen3-8B + 同一 LoRA 配置）、共享解码参数（temperature 0.4, top-p 0.95；评测 greedy）、共享提示词、共享 Cgold oracle 与 DIFF 信号，唯一差异是 INJ 信号的有无。定位：p.19 Appendix E "Decoding, learning rate, scheduling, LoRA configuration, and effective batch size remain aligned"。[READER_INTERPRETATION] 因此 +2.86/+4.00 的消融增益基本排除了模型/token/tool-call/prompt/oracle 差异，是全文最干净的证据；而与外部基线的主表差距则受 4.2–4.4 的混杂影响。

4.6 [AUTHOR_FACT] B4 落后被作者归因于变体缺口而非方法失效："largely due to Benchmark 4 containing 50 TSPTW instances, a variant absent from training"（p.7–8 Sec 5.3）。[READER_INTERPRETATION] 这一归因方向合理（TSPTW 不在 21 变体表中，Table 4 可证），但论文未给出 B4 内部按变体拆分的分数来量化验证。

4.7 [AUTHOR_FACT] 无工具调用/多轮交互差异：所有被测系统均为单轮代码生成，Gurobi 600 秒限时执行；不存在 agentic 工作流差异。定位：p.20 Appendix F "a 600-second Gurobi time limit per instance, and greedy decoding"。

## Q5 作者明示限制、负向结果和未测试边界

5.1 [AUTHOR_FACT] Limitations 一节明示三条（p.9）：(i) 域覆盖仅 VRP，"evaluating how effectively this methodology transfers to other combinatorial optimization domains, such as scheduling, facility location, or production planning, remains a natural next step"；(ii) 依赖结构化 Cgold 与人工设计攻击算子，"manual design is still required for highly unique or exotic domain-specific rules"；(iii) Pass@1 是目标等价度量，"inevitably compresses the multi-dimensional, constraint-level feedback ... into a binary success signal"。

5.2 [AUTHOR_FACT] 正文承认的负向结果：B4 上落后 Gemini 8.40 分（p.7–8）。

5.3 [AUTHOR_FACT] 明示的探针覆盖边界：不为所有建模约束造探针，只覆盖两类（逻辑结构约束与常见资源约束）；软时间窗等"mainly changes an objective penalty rather than producing a deterministic infeasibility label"的机制不造违反探针，交给 DIFF（p.14–15 B.4）；仓库出发/返回模式不直接固定，"leaving depot-structure errors primarily to DIFF"（p.5 Sec 4.1；p.19 Appendix D "they are not used as a general test of depot-structure constraints"）。

5.4 [READER_INTERPRETATION] 未测试边界（作者未讨论）：(a) 攻击算子对"伪过约束"的覆盖仅由单个 s+ 提供——一个可行探针只能证伪那些恰好排除该 s+ 的过约束，覆盖强度未量化；(b) INJ 依赖变量命名契约，对不服从契约的自由格式代码（例如换名、稀疏弧建模）只能判为验证失败，这在评测外部模型时未启用，故契约失配的影响未被测量；(c) 训练/评测实例规模都很小（客户数 4–12，B3 也降采样到 5–12 客户，p.20），规模外推未测试；(d) εobj 在训练期 DIFF 中的数值未见报告（见 Q7/OPEN）。

## Q6 可抽取的 Operator 与真实可记录的 Failure

Operator（机制级、可迁移）：

6.1 [AUTHOR_FACT] OP-约束注入：把候选优化程序变成可行性判定器——常数化目标 + 用 addConstr 固定一个已知标签的解，比较求解器判定与标签（p.3–4 Sec 3.3）。[READER_INTERPRETATION] 可迁移条件：存在可编程访问的模型对象、解可编码为线性约束、存在能出具标签的 oracle。

6.2 [AUTHOR_FACT] OP-双探针配对：可行探针（必须接受，抓伪过约束）+ 单约束违反探针（必须拒绝，抓静默缺失），每个 s−_i "target exactly one constraint family by construction"（p.4 Sec 3.4；p.15 B.4）。

6.3 [AUTHOR_FACT] OP-边界内收紧：参数攻击把资源上界置于 (g,b) 开区间、0.85 插值贴近违反侧，并配 ε 数值边距防舍入（p.15–16 Eq. (13)）。

6.4 [AUTHOR_FACT] OP-一路放松再定点收紧：先对 s+ 涉及的资源族做单向放松（只扩大可行域），为后续攻击特定收紧留出开区间；结构攻击在 I*上评，资源攻击各建攻击专用副本 I*_a（p.17 B.5）。

6.5 [AUTHOR_FACT] OP-退化修复封堵：同质车队注入违反探针时追加同车绑定 Eq. (8)，否则"the solver could split an overloaded route across vehicles, masking the capacity violation"（p.5）；SDVRP 探针防止靠重分配需求修复（p.19）。[READER_INTERPRETATION] 这是一个一般性教训：把"解"注入一个有自由度的模型时，必须封死能绕开目标约束的等价类自由度。

6.6 [AUTHOR_FACT] OP-同一验证器双用：同一 INJ 实现既做 SFT 拒绝采样过滤又做 GRPO 奖励，"ensuring identical signals between data filtering and RL"（p.5）。

6.7 [AUTHOR_FACT] OP-前沿样本筛选：每 prompt 离线采 M=6 个 rollout，只保留组内奖励方差严格为正的 prompt（丢弃全对/全错），得 716 个 GRPO prompts（p.6 Sec 4.3.2；p.19 Appendix E）。

6.8 [AUTHOR_FACT] OP-输出协议契约 + 索引回译：提示词强制变量名/索引约定使注入可编程化（Figure 10, p.26）；索引重写路径强制返回 node_id_map 以便探针回译（p.17, p.24 Figure 8）。

6.9 [AUTHOR_FACT] OP-攻击台账按变体启用：Table 6（p.18）给出 21 变体 × {结构攻击, 参数攻击} 的启用矩阵（base pair = remove customer + subtour cycle 为全变体基线配置）。

Failure（论文内真实记录）：

6.10 [AUTHOR_FACT] FAIL-DIFF 漏检实测规模：主管线 6797 个 SFT 样本之外另有 550 个样本"pass differential testing but fail constraint injection"（p.19 Appendix E）——即在他们自己的教师生成数据上，纯 DIFF 过滤会放行约 7.5%（550/7347）带约束缺陷的样本。[READER_INTERPRETATION] 这是全文最有价值的、非构造性的失败记录。

6.11 [AUTHOR_FACT] FAIL-图示失败模式：省略子回路消除约束的候选码仍匹配参考最优值 203.18，DIFF 判过；INJ 用不连通子回路探针 {0→2→0, 1→4→3→1} 暴露之（p.1 Figure 1，视觉核对与文本一致）。[READER_INTERPRETATION] 注意这是作者构造的说明性实例，非训练日志中的自然样本。

6.12 [AUTHOR_FACT] FAIL-验证器自身的不可判定情形："Cases with model-construction failures, unsupported variable formats, unreliable node matching, or unresolved solver statuses are treated as verification failures"（p.19 Appendix D）——INJ 不是全覆盖判定器，有一类样本因工程原因整体弃用。

6.13 [AUTHOR_FACT] FAIL-泛化缺口：TSPTW 未在训练变体中，B4 上落后最强基线 8.40 分（p.7–8）。

6.14 [READER_INTERPRETATION] 不建议记为 Failure 的候选：软时间窗无探针（p.15）是明示的设计边界而非观察到的失败；Reserved 样本（Table 1）与 6.10 是同一事实的两个视角，应合并记录避免重复计数。

## Q7 判断与物理页码/章节/图表/逐字定位对照

- 双验证器概念与失败模式命名：p.2 Sec 1，"spurious over-constraint and silent constraint omission"。
- DIFF/INJ 形式定义：p.3–4 Sec 3.3，"replaces the objective with a constant"。
- 探针定义：p.4 Sec 3.4，"(1) Feasible probe s+ ... (2) One-constraint-violating probes"。
- 三种注入编码：p.5 Sec 4.1 Eq. (7)(8)(9)，"2D projection / 2D + vehicle binding / 3D direct fixing"（视觉核对 p.5）。
- 合成管线四阶段：p.5–6 Sec 4.2 Figure 3（视觉核对）；拒绝采样规则 p.6 Table 1。
- 训练两阶段与奖励：p.6–7 Sec 4.3，Eq. (10)(11)(12)；权重与规模 p.7 Sec 5.1 "6797 (q, Cregen) pairs ... 716 frontier prompts with G = 8 ... 0.2rbuild +0.5rdiff+0.3rinj ... 4×A100-40GB"。
- 基准构成：p.7 Sec 5.2（310/66/74/250，共 700）；细节 p.20 Appendix F（B4 = 200 NLCO + 50 SIRL 清洗集：9 OptMATH, 2 IndustryOR, 39 MAMO ComplexLP；600 秒限时；greedy）。
- 主结果：p.8 Table 2（视觉核对：Gemini AVG 95.00 与 B4 96.40 加粗；VRPCoder-GRPO 93.00 下划线次优）。
- 消融：p.8 Table 3 与 Sec 5.4；no-injection 细节 p.19 Appendix E（7347/550/855/max reward 0.7）。
- Limitations：p.9，"Domain coverage / Framework and attacker scaling / Metric aggregation"。
- 21 变体与 held-out：p.11 Appendix A；p.12 Table 4（视觉核对：held-out = OVRPHTW, MCVRPSTW, DCVRPHTW，粗斜体）。
- 探针构造细节：p.13–14（profiles、B.2、B.3 "TimeLimit = 15s and MIPFocus = 1"）；攻击算子 p.15–16（B.4.1/B.4.2, Eq. (13)）；放松与装配 p.17 B.5。
- 教师模型：p.17 Appendix C，"Gemini-3.1-Pro Preview ... and Claude Opus 4.6 ... as the teacher LLMs"。
- 攻击启用矩阵：p.18 Table 6。
- INJ 实现与判定处理：p.18–19 Appendix D。
- 全部提示词：p.21–26 Figures 5–10；场景池：p.27–28 Tables 7–8（60 条）。

[OPEN_QUESTION] 尚无法从原文解决的点：
- O1：训练期 DIFF 的容差 εobj 从未给出数值（p.3 只说 "differ by at most εobj"；p.7/p.20 的 10^-3 是评测 Pass@1 容差，二者是否同值原文未说明）。
- O2：p.12 B.1 说 profile 的 "sample counts and their use in training or ablation studies are reported with the data-flow statistics"，但全文（含附录）未见对应的数据流统计表；逐 profile/逐变体的样本量不可复核。
- O3：所有结果为单次训练/单次评测（greedy），未报方差、种子重复或显著性；+2.86/+4.00 的消融增益的稳定性不可评估。
- O4：Stage 4 各环节的通过率（除 550 这一处外）、INJ "验证失败"类样本占比未报告，无法估计契约失配（6.12）的实际规模。
- O5：B4 是否对 VRPCoder 之外的基线也做了 "adding the annotated vehicle count to CVRP statements" 等改写（p.20 说的是对 NLCO 提示的统一改造，应为所有模型共享，但未逐字确认基线是否用改造前原题）。

## Q8 解析文本与可视 PDF 是否冲突（就抽查页作答）

8.1 [AUTHOR_FACT] 抽查页：p.1、p.5、p.8、p.12（150dpi 渲染后视觉 Read）。数值层面无冲突：Table 2/3 全部数字（含 95.81/89.39/91.89/96.40/95.00、96.13/96.97/93.24/88.00/93.00、85.57/88.43/89.00/93.00、+2.86/+4.00）与抽取文本逐一相符；Figure 1 的探针 "{0→2→0, 1→4→3→1}" 与参考最优 203.18 相符；p.1 水印确认 arXiv 号与日期。

8.2 [READER_INTERPRETATION] 非冲突性的抽取噪声：(i) PyMuPDF 对表格与图的线性化顺序打乱——p.5 Figure 3 的节点标签与公式碎片交错、p.12 Table 4 的列勾选项在纯文本中难以对齐行（视觉确认后行列归属明确）、p.8 两张表按列拆散；(ii) 连字（fi/fl）以 Unicode 连字形式保留（"verifier" 等词在原始抽取中含连字符号），属编码习惯而非内容差异；(iii) p.4 Figure 2 的标签文本在抽取中与正文交错，本报告对该图内容的引用（路线/载荷 14.5/16.1/18.0/12.6、收紧容量 17.48）取自其图注文字，图本身未做视觉核对。未抽查的其余页面不做无冲突担保。

## 附：一句话总评（读者解释）

[READER_INTERPRETATION] 本文的可信内核是：在自建 VRP 合成分布上，(a) 纯差分测试确实以可测量的比例（550/7347）放行约束缺陷样本；(b) 在其余条件严格对齐的消融中，把约束注入信号加进过滤与奖励带来 +2.86（SFT）/+4.00（GRPO）的平均 Pass@1 增益，且分布外基准（B2/B4）增益最大。与外部 frontier 模型的主表比较则受主场分布、教师蒸馏与提示词协议的多重混杂，证据强度显著低于消融。
