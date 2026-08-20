# P056 独立第二读报告

## 1. Provenance 与读取边界

- Attempt：`r2-20260720-p056-a1`
- 论文：PMLR v235/zhuge24a，*GPTSwarm: Language Agents as Optimizable Graphs*，ICML 2024。
- Invocation snapshot：`knowledge_base/corpus/reads/P056/read_2_attempts/r2-20260720-p056-a1/invocation.md`。
- PDF：`knowledge_base/staging/plan05_sat_a1/P056_gptswarm.pdf`。
- PDF SHA-256：`63aab69835f124fd1bee714a21433a696c4d8d36da9f7883e0b5b01b836fd6ed`，与 invocation 一致。
- PDF 页数：25 个物理页；正文 1–9，参考文献 10–12，附录 13–25。
- 完成时间：`2026-07-20T02:12:21.2591478+08:00`。
- Actual model/version：`unknown`（运行界面未暴露可验证的精确模型与版本）。
- Canonical task/thread：`/root/plan03_blind_evaluator_v1`；`reused independent reader thread due platform thread cap`。这是本线程第一次接触 P056，但不是全新线程。线程中存在此前无关 blind 任务的上下文残留；本次未重新读取或使用任何 blind 文件，也未把该残留作为 P056 判断依据，因此独立性属于程序性隔离而不是可验证的 fresh-context 技术隔离。
- Blinding：`procedural_blinding`；App 没有提供文件级 allowlist，不能声称技术只读隔离。
- 访问的项目文件仅限：两级 `AGENTS.md`、`CRL.md`、`CRL_ENVIRONMENT.md`、本 attempt 的 `invocation.md`、统一 `second_read_prompt.md`、指定 P056 PDF。
- 访问的环境技能文件：`paper-ingestion-and-evidence-builder/SKILL.md` 及其直接要求的 `references/rules.md`、`references/output_schema.md`、`references/checklists.md`，以及 `pdf/SKILL.md`。
- 未访问：P056 `read_1`、Cards、其他报告、其他论文读稿、Corpus Report、saturation 材料、retrieval/blind 文件；未枚举工作区；未联网。
- 工具轨迹：先用 SHA-256 与 PyMuPDF 1.28.0 核对 PDF 并按 `1–5 / 6–10 / 11–15 / 16–20 / 21–25` 逐页抽取文本；直接把 PDF 交给图片查看器失败后，改用 `pdfjs-dist` 与 `@napi-rs/canvas` 在内存中按同样五组渲染并检查全部页面，没有生成渲染文件。报告是唯一持久化写入。
- 技能适用说明：本任务是独立二读核源，不是正式 ingestion；因此遵守了来源、定位、不确定性与“不凭记忆补写”的规则，但没有读取通常 ingestion 所需的 `paper_index.json` 或 route registry，也没有创建 Paper Card、Evidence、parsing log 或 citation context。这样处理服从本 invocation 更窄的显式读取边界。

## 2. 结论摘要

- [AUTHOR_FACT] GPTSwarm 把 agent 表示为有向无环计算图：节点执行 LLM、工具或函数等操作，边传递前驱节点输出；多个 agent graph 通过跨图边组成 composite graph/swarm。定位：物理页 2–3，§2.1–2.2，Figure 1、Algorithm 1。
- [AUTHOR_FACT] 论文提出两种不同的优化：用 REINFORCE/Adam 学习潜在跨 agent 边的概率分布；用节点执行历史改善各节点 prompt。定位：物理页 3–4，§2.3–2.4，Algorithms 2–3。
- [READER_INTERPRETATION] 核心 changed computation 不是简单“增加多个 agent”，而是把固定 agent 模块间的信息路由显式参数化，并以任务效用更新路由分布；节点优化则是另一条、基于历史与质量反馈的 prompt 更新机制。两者应分开归因。
- [READER_INTERPRETATION] 证据强度不均：MMLU、Mini Crosswords 主要验证 edge optimization；HumanEval 主要验证 node optimization；GAIA 只验证框架组合，作者明确说没有运行 edge 或 node optimization。不能用 GAIA 结果支持自动图优化有效性。定位：物理页 5–8，§3.1–3.4。
- [READER_INTERPRETATION] 最接近的 topology comparator 是 DyLAN；它在 MMLU 上略高于 GPTSwarm，但代价明显更大。最接近 node/prompt comparator（如 OPRO、DSPy、PromptBreeder）只在相关工作中讨论，没有进行同任务经验比较。定位：物理页 9、17，§4.3、Appendix D.1、Table 3。
- [READER_INTERPRETATION] 论文提供了较完整的美元、token 与时间核算，但没有形成统一的 matched-compute 主表；若直接比较最终准确率，模型、agent 数、prompt、token、工具调用和 oracle 信息可能同时变化。定位：物理页 6–8、17、25，Figures 4–6、Tables 1–3、11。

## 3. 方法究竟改变哪一步计算

### 3.1 图表示与执行

- [AUTHOR_FACT] 单 agent 图定义为 `G=(N,E,F,o)`；每个节点 `n` 接收原始输入 `x` 和前驱输出集合 `z_n`，按拓扑序执行 `f_n(z_n,x)`，输出节点产生最终结果。论文限定 DAG，且当前实验中的输入输出是自然语言字符串。定位：物理页 2–3，§2.2，Algorithm 1。
- [AUTHOR_FACT] composite graph 取多个 agent 内部节点、边与函数的并集，再加入来自不同 agent 节点之间的边；这些新边表示通信通道。定位：物理页 3，§2.2，`Swarm of language agents as a composite graph`。
- [AUTHOR_FACT] 实验中还加入一个虚拟 final-decision 节点作为 composite output；潜在边来自不同 agent 的节点对，不允许从 composite output 节点向其他节点连边。定位：物理页 17，Appendix E 首段。
- [READER_INTERPRETATION] 表示层带来的实际计算变化是：前驱 agent/node 的自然语言输出被拼入后继节点上下文，边的存在与方向决定哪些中间结果可见、以何顺序可见。图并非只作可视化标签。

### 3.2 Edge optimization

- [AUTHOR_FACT] 对任务 `τ` 和效用 `u_τ`，论文把离散边集合搜索改写成对可行 DAG 分布 `D_θ` 的期望效用最大化。每条潜在边有参数；采样时若加入边会成环则拒绝，否则按对应概率加入。定位：物理页 3–4，§2.3.1–2.3.2，Equation 1。
- [AUTHOR_FACT] 梯度由多个独立 graph sample 的效用估计通过 REINFORCE 得到；实验实际用 Adam，而不是 Algorithm 2 展示的 vanilla gradient ascent。定位：物理页 4、17，§2.3.3，Algorithm 2，Appendix E。
- [READER_INTERPRETATION] 输出是“图分布/边概率”，不是一次训练必然返回唯一确定拓扑；评测往往继续从该分布采样。因此必须区分学到的概率分布、被采样的实例图和最终可能被选中的单个图。

### 3.3 Node optimization

- [AUTHOR_FACT] 每个节点函数由 prompt `p_n` 参数化；节点历史 `h_n` 保存该节点看到的 `(z_n,x)` 及其输出，改进器 `I(h_n,p_n,d_n)` 产生新 prompt。作者假设一次更新某节点时其余 prompt 固定。定位：物理页 4，§2.4，Algorithm 3。
- [AUTHOR_FACT] HumanEval 的实例化不是自由文本式 OPRO：每四个新问题更新一次；根据可见测试反馈把节点样本分为正负，最多保留四个 demonstration，并在保留旧 demonstrations 与加入近期正例两种方案间，用最近十个输入的测试表现选择。定位：物理页 7、20，§3.3、Appendix E.3.1。
- [AUTHOR_FACT] Mini Crosswords 的追加实验在 edge optimization 后，再用 UCB1 为每个节点选择一个历史 demonstration 或保持不变，共一百次迭代，准确率从 `0.575±0.0275` 提升到 `0.668±0.0060`。定位：物理页 17，Appendix D.2。
- [READER_INTERPRETATION] 论文的一般 Algorithm 3 与具体实验实现差别较大；可复用 Operator 应保留“节点级、历史条件化、质量反馈驱动”的共同机制，同时把 HumanEval demonstration selection 和 Crosswords UCB1 作为不同实例，不能混成一个固定算法。

## 4. 输入、输出、信息边界与干预时点

- [AUTHOR_FACT] Graph execution 的外部输入是任务输入 `x`；节点还看到前驱输出 `z_n`。节点可以忽略 `x`，只用前驱上下文。定位：物理页 3，§2.2。
- [AUTHOR_FACT] Edge optimizer 需要任务效用及其独立无偏估计，并在每轮执行若干 sampled graphs 后更新边参数。定位：物理页 3–4，Equation 1–2、Algorithm 2。
- [AUTHOR_FACT] MMLU edge optimization 每轮评估四个 graph samples、运行 200 轮；优化问题来自 dev set，报告分数来自 validation set 最初 10%（153 题）。定位：物理页 5、18，§3.1.1、Appendix E.1、Figure 10。
- [AUTHOR_FACT] Mini Crosswords 仅使用 20 题子集，作者明确说该子集同时用于优化和评估；每轮用 20 个 sampled graphs，十轮 REINFORCE。定位：物理页 5–6，§3.2。
- [AUTHOR_FACT] HumanEval 节点优化可读取问题陈述内测试案例的执行反馈；作者还进行“不重启、持续优化并评估”的 online-learning 设置。定位：物理页 7、20，§3.3、Appendix E.3.1。
- [OPEN_QUESTION] HumanEval 文中没有充分澄清：prompt 更新所用的“problem statement 内测试”和最终 accuracy 判定测试是否严格隔离，以及多轮对整个数据集评估是否影响后续更新。原文不足以排除评测反馈泄漏。
- [READER_INTERPRETATION] Edge 干预发生在 agent 内部函数固定之后、跨 agent 信息通道选择阶段；node 干预发生在完整 graph execution 产生历史与质量反馈之后。二者访问的监督信号不同，不能以同一“self-improvement”标签掩盖。

## 5. 最强基线、最近组合基线与公平性

### 5.1 MMLU

- [AUTHOR_FACT] 主文基线包含 single IO direct answer、full graph、初始 `D_0.5` 随机图与 optimized swarm；adversarial swarm 的目标只是恢复到 single-agent baseline。定位：物理页 5，§3.1.1，Figure 2。
- [AUTHOR_FACT] 同质 IO agents 的 adversarial setting 没有超过 single-agent baseline；换成七种不同角色后，比 §3.1.1 baseline 高 `2.1%±1.1%`，五个训练 seed。定位：物理页 5，§3.1.2。
- [AUTHOR_FACT] Appendix D.1 比较 Multiagent Debate、DyLAN 与 GPTSwarm。DyLAN inference accuracy 为 `0.8366`，GPTSwarm 为 `0.8301`；作者把 `0.0065` 差距归因于 DyLAN 更复杂的 debate scheme 和 prompts，同时指出其成本更高。定位：物理页 17，Table 3。
- [AUTHOR_FACT] Table 3 的优化成本分别为 DyLAN `$105.93`、GPTSwarm `$5.32`；inference 成本分别为 `$14.99`、`$1.82`。对应 prompt/completion token 和时间也分别报告。定位：物理页 17，Table 3。
- [READER_INTERPRETATION] DyLAN 是最接近的强组合基线，但并非严格同 prompt/同通信协议/同搜索空间；论文展示的是性能—成本权衡，不是控制所有组件后的纯 edge-optimizer 因果比较。

### 5.2 Mini Crosswords

- [AUTHOR_FACT] agent 组件为 ToT、Reflexion 与三节点 COT；效用采用所有 graph-returned solutions 中的 best-state word accuracy。定位：物理页 5–6，§3.2。
- [AUTHOR_FACT] GPT-3.5-Turbo edge optimization 从初始分布 `0.465±0.0509` 提升到 `0.575±0.0275`；best-of-three 为 `0.320±0.0415`。定位：物理页 6，§3.2、Figure 4。
- [AUTHOR_FACT] 平均边数控制使用全参数 `0.125` 的分布：其预期边数 `32.80±0.11`，学习分布为 `32.76±1.93`，但准确率仅 `0.510±0.0552`。定位：物理页 6，§3.2。
- [AUTHOR_FACT] 作者随机选择一个最终分布并换用 GPT-4-Turbo 评估，得到 `0.800±0.0616`；原 ToT GPT-4 为 `0.675`，作者自己的 ToT GPT-4-Turbo 复现为 `0.668`。由于 API 成本，只评估了一个 graph distribution。定位：物理页 6，Figure 4 与脚注 2。
- [READER_INTERPRETATION] 边数匹配消除了最粗粒度的 graph-density 解释，但没有匹配每个节点的实际 token、上下文长度或 LLM 调用数。它是必要而非充分的 compute control。
- [READER_INTERPRETATION] `best-state word accuracy` 在多个候选中使用正确填词数选最好结果，属于 evaluator 可访问 ground truth 的 oracle 式效用；若系统部署时不能获得该效用，论文结果不能直接解释为无 oracle 的答案选择能力。
- [READER_INTERPRETATION] GPT-4 transfer 结果同时改变模型且只用一个随机选择的分布；它支持“某一学得拓扑可迁移”的存在性示例，不足以估计分布间方差或稳定迁移率。

### 5.3 HumanEval

- [AUTHOR_FACT] ReAct-style agent 在持续 node optimization 中从 `0.76` 提升到 `0.88±0.007`，三次重复；主要增益出现在前五轮。定位：物理页 7，§3.3、Figure 5。
- [AUTHOR_FACT] Table 11 中无优化 HumanEval 成本为 `$1.61`、`59,646/33,951` prompt/completion tokens、`0.68h`；有优化为 `$28.46`、`2,298,140/182,594` tokens、`1.49h`。定位：物理页 25，Table 11。
- [READER_INTERPRETATION] 论文没有与 OPRO、DSPy、PromptBreeder 或等量 demonstrations/repeated sampling 的实证对照；因此不能把全部提升唯一归因于“graph node decomposition”。

### 5.4 GAIA

- [AUTHOR_FACT] GAIA 实验使用多个相同 agent 与 prompt-based self-consistency/choose-best；作者明确说明这些实验既没有 edge optimization，也没有 node optimization。定位：物理页 7，§3.4。
- [AUTHOR_FACT] Table 2 展示从单 TOT `25.66±3.50`、约 `71.31s` 到七 TOT self-consistency `30.56±3.25`、约 `414.89s`；作者观察时间近似随 agent 数线性增长。定位：物理页 8，Table 2。
- [AUTHOR_FACT] Table 1 的 `GPT-4 with plugins` 由人工为每题选择工具，作者自己称该基线意义较弱；其他 GPT/AutoGPT 数字来自 GAIA 报告。定位：物理页 7，Table 1 caption 与正文。
- [READER_INTERPRETATION] GAIA 的增益主要伴随 agent 数、工具集合和聚合方式变化；它不能作为自动 edge/node optimization 的公平验证，也不是固定 compute 下的 swarm 优势证据。

## 6. Oracle、成本与替代解释总表

- [AUTHOR_FACT] Table 11 报告代表性实验的美元、prompt tokens、completion tokens 与时间。Mini Crosswords GPT-3.5 edge optimization 为 `$77.42`、约 `50.39M/13.51M` tokens；GPT-4 edge-opt evaluation 为 `$377.54`。定位：物理页 25，Table 11。
- [AUTHOR_FACT] 同表 ToT Mini Crosswords 为 `$65.61`、约 `1.52M/2.01M` tokens；Crosswords GPT-3.5 node-opt 与 node-opt-eval 分别为 `$11.22` 与 `$28.18`。定位：物理页 25，Table 11。
- [READER_INTERPRETATION] 这些成本行对应不同阶段与模型，不能简单相加后当成严格 end-to-end 对照；论文没有对所有主要准确率结果统一给出 inference-only、optimization-only 与 amortized cost。
- [READER_INTERPRETATION] 主要替代解释包括：更多 LLM calls；更长的前驱上下文；不同模型（GPT-3.5、GPT-4、GPT-4-Turbo）；不同 prompt/role；utility/ground-truth oracle；同一题集反复用于优化；以及 agent/tool 数量变化。
- [OPEN_QUESTION] 原文没有报告统一的固定 token、固定 LLM-call、固定 wall-time 或固定美元预算曲线，因而无法回答“同资源预算下 topology optimization 是否仍优于最近组合基线”。

## 7. 作者明示限制、负向结果与未测试边界

- [AUTHOR_FACT] 作者只优化 agent 间通信边，未动态改变单个 agent 内部节点拓扑；后者被列为未来工作。定位：物理页 22，§G Limitation and Future Work。
- [AUTHOR_FACT] 作者指出 agent 数超过 100 时，通信效率和系统鲁棒性成为显著挑战。定位：物理页 22，§G。
- [AUTHOR_FACT] 当前图形式限定 DAG；周期操作未被方法与实验覆盖。定位：物理页 2–3，§2.2。
- [AUTHOR_FACT] GAIA 当前 web 实现仅下载题目提供 URL 或调用 Google search，不进行进一步网页导航；作者认为增强 web 能力可继续提高表现。定位：物理页 8，§3.4。
- [AUTHOR_FACT] GAIA Level 3 上 GPTSwarm 为 `3.85±2.43`，相对 AutoGPT 的表中 improvement 为 `0.0%`；整体仍远低于表中 human `94%`。定位：物理页 7–8，Tables 1–2。
- [AUTHOR_FACT] DyLAN 的 MMLU accuracy 略高于 GPTSwarm；这是作者直接报告的负向比较，不应因 GPTSwarm 成本更低而删除。定位：物理页 17，Appendix D.1、Table 3。
- [AUTHOR_FACT] adversarial MMLU 的 optimized swarm 只恢复 single-agent baseline，没有超过；作者认为同质 IO prompts 限制了协作增益。定位：物理页 5，§3.1.1–3.1.2。
- [AUTHOR_FACT] Mini Crosswords 的边概率前六轮变化混乱，之后才近似单调；这说明早期优化轨迹不稳定。定位：物理页 6，Figure 3。
- [READER_INTERPRETATION] Mini Crosswords 的 20 题同时用于优化与评估构成明确的泛化边界；论文没有独立 held-out crossword 集来证明拓扑学习超出这 20 题。
- [READER_INTERPRETATION] node optimization 与 edge optimization 的联合证据只有 Crosswords 附录实验；主文没有在所有任务上做完整二因素消融，也没有证明两者稳定互补。

## 8. 可供后续主 Codex 考虑的 Operator 候选

以下只是二读候选，不是正式 Card 或科研裁决。

- [READER_INTERPRETATION] **Operator 候选 O1：cycle-constrained stochastic edge-distribution optimization。** 固定节点与内部 agent 后，把跨 agent 潜在边参数化为 Bernoulli 概率，拒绝成环边，用 sampled-graph task utility 的 REINFORCE/Adam 更新概率。精确定位：物理页 3–4，§2.3，Equation 1–2、Algorithm 2；实验边界见物理页 17 Appendix E。
- [READER_INTERPRETATION] **Operator 候选 O2：history-conditioned per-node prompt update。** 收集节点输入、前驱上下文、节点输出及质量反馈，在其余 prompt 固定的假设下逐节点更新 prompt。精确定位：物理页 4，§2.4、Algorithm 3。
- [READER_INTERPRETATION] **Operator 候选 O3：feedback-selected demonstration maintenance。** HumanEval 中每四题更新，基于可见测试反馈维护最多四个 demonstrations，并按最近十个输入的通过情况选择更新。精确定位：物理页 20，Appendix E.3.1。
- [READER_INTERPRETATION] **Operator 候选 O4：edge-then-node staged optimization。** 先学跨 agent edge distribution，再在固定的已优化分布上用 UCB1 选择节点 demonstrations。精确定位：物理页 17，Appendix D.2。
- [OPEN_QUESTION] O1 对 utility oracle、训练题重用和 graph sampling variance 的依赖是否可在无标签在线环境中保留，原文未解决。

## 9. 可供后续主 Codex 考虑的 Failure 候选

- [READER_INTERPRETATION] **Failure 候选 F1：homogeneous-agent collaboration ceiling。** 相同 IO prompt 的 swarm 在 adversarial MMLU 中只恢复 single-agent 水平；角色多样化后才出现小幅增益。定位：物理页 5，§3.1.1–3.1.2。
- [READER_INTERPRETATION] **Failure 候选 F2：topology gain confounded by compute and context。** 边数控制仍未控制 token、调用数和前驱上下文长度。定位：物理页 6 §3.2、物理页 25 Table 11。
- [READER_INTERPRETATION] **Failure 候选 F3：utility-oracle mismatch。** Crosswords 用 ground-truth best-state accuracy 从多候选中计效用；部署时若没有同类 oracle，优化和选择机制可能不可用。定位：物理页 6 §3.2、物理页 20 Appendix E.3.1。
- [READER_INTERPRETATION] **Failure 候选 F4：same-set topology overfitting。** Crosswords 的同一 20 题既优化又评估，未显示 held-out 泛化。定位：物理页 5–6，§3.2。
- [READER_INTERPRETATION] **Failure 候选 F5：nearest baseline retains a quality edge。** DyLAN 比 GPTSwarm 高 `0.0065`，说明低成本并不等同于绝对最强性能。定位：物理页 17，Appendix D.1、Table 3。
- [READER_INTERPRETATION] **Failure 候选 F6：scale-induced communication/robustness risk。** 作者预计超过 100 agents 后通信效率和鲁棒性成为挑战，而论文实验远未覆盖该规模。定位：物理页 22，§G。
- [READER_INTERPRETATION] **Failure 候选 F7：framework result substituted for optimizer evidence。** GAIA 没有运行两类优化，不能证明 automatic graph optimization。定位：物理页 7，§3.4。

## 10. 解析文本与可视 PDF 核对

- [AUTHOR_FACT] 可视 PDF 共 25 页，页码连续；Figure 1–11 与 Table 1–11 均在相应页出现。物理页 14–16 主要由 class diagram、swarm example 和 agent/swarm visualizations 构成，文本抽取无法保留其结构。
- [READER_INTERPRETATION] PyMuPDF 对物理页 1–10、17–20 的双栏内容存在跨栏交错，对 Equation 2、图注和若干表格也有字符粘连；因此方法与实验结论按可视栏序复核，没有依赖拼接后的线性文本顺序。
- [READER_INTERPRETATION] Table 2、3、4、11 的数值和 Figure 2–6、10 的总体含义均与可视页面一致；未发现解析文本与可视 PDF 在结论层面的冲突。
- [OPEN_QUESTION] Figure 7、8、9、11 的细小节点/边标签在联系图尺度下不适合逐字作为证据；本报告只把这些图用于确认结构与 pruning/realized-edge 的可视存在，具体算法判断以正文、Algorithms 和表格为准。

## 11. 二读边界声明

- [READER_INTERPRETATION] 本报告支持把 edge optimization 与 node optimization 作为两个可追溯机制来源，并记录同质 swarm、oracle utility、same-set evaluation、成本混杂与规模限制等负向边界。
- [OPEN_QUESTION] 是否接纳为正式 Evidence、如何与首读 reconciliation、是否生成 Operator/Failure Card、以及对当前 Candidate 的影响，均由主 Codex 后续决定；本二读不作这些裁决。
