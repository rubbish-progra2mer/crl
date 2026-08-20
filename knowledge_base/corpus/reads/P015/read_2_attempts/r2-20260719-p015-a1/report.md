# P015 独立二读报告

## 0. Provenance 与读取边界

- Invocation snapshot：`read_2_attempts/r2-20260719-p015-a1/invocation.md`；Attempt ID：`r2-20260719-p015-a1`；角色：fresh independent full-paper source checker。
- [AUTHOR_FACT] 论文 canonical metadata 为 PMLR:v235/smit24a，题名 *Should we be going MAD? A Look at Multi-Agent Debate Strategies for LLMs*，ICML 2024；PDF 共 23 页。定位：PDF p.1，标题及页脚 “PMLR 235, 2024”。
- 输入核验：PDF SHA-256 为 `8d0330933f495a3804842e8c8b0f778d8529fefeaf8d2a2dbf89d94f97bd0e70`；`second_read_prompt.md` SHA-256 为 `ffb7c12e663f44318d8eda1c270cbc26ad66665fd803247a2ab66a8f23fa333a`，均与 invocation 一致。
- 作为输入材料实际读取的文件仅有：
  1. `D:/Desktop/crl_judge/crl_agent_v3/knowledge_base/staging/papers/P015_should_we_be_going_mad.pdf`
  2. `D:/Desktop/crl_judge/crl_agent_v3/knowledge_base/templates/second_read_prompt.md`
  3. `D:/Desktop/crl_judge/crl_agent_v3/knowledge_base/pilot/reads/P015/read_2_attempts/r2-20260719-p015-a1/invocation.md`
- 写入完成后，另回读了本次新生成的 `report.md` 本身一次，仅用于核验文件存在、字节数、行数和三类标签计数；它不是额外研究输入。
- 未读取 read_1、Cards、其他读者报告或 blind query；未枚举工作区；未联网；未生成 Card，也未作 Candidate 评价。
- 读取/核验工具：PowerShell 精确路径读取、SHA-256 核验及报告回读计数；Python 3 + PyMuPDF 1.27.2.2 逐页提取 PDF 文本、读取页数和元数据；PyMuPDF + Pillow 在内存中逐页渲染并以 4 页 contact sheet（末组 3 页）显示检查；`view_image` 直接打开 PDF 的一次尝试因工具不支持 PDF 而未产生可查看内容。除本 `report.md` 外未创建持久文件。
- Actual model/version：Codex（系统仅表明 GPT-5 系列）；精确部署版本不可见，记为 `unknown`。Canonical agent task：`/root/p015_second_read`；用户侧 thread ID 不可见，记为 `unknown`。
- 隔离性质：`procedural_blinding`，不是技术文件级 allowlist。平台无法观察/证明的 trace 包括：底层 OS 级完整文件访问审计、工具封装器内部访问、精确模型部署 ID、用户侧 thread ID；这些记为 `unavailable`，不能据此宣称技术隔离。

## 1. 方法究竟改变哪一步计算？

- [AUTHOR_FACT] 论文的核心比较对象不是单一新模型，而是多种推理时协议：Single Agent、Self-Consistency、Ensemble Refinement、Medprompt、Society of Minds、ChatEval、Multi-Persona；它们改变的是推理时回答的生成、共享、汇总和最终选择流程，不做梯度更新。定位：PDF p.2，§2，短定位文本 “entirely using in-context prompting” 与 “no gradient-based parameter updates”。
- [AUTHOR_FACT] Society of Minds 让多个代理互相看到答案，可选先总结再进入后续轮次；ChatEval 改变回答顺序/异步生成/总结历史；Self-Consistency 独立采样多个推理路径后做多数选择；Ensemble Refinement 先采样多个推理，再将其串接为 student reasonings 并执行聚合；Multi-Persona 由 angel、devil 向 judge 提供答案，judge 可提前结束。定位：PDF pp.2–3，§2 与 Table 1；短定位文本分别为 “provide their answers to each other”“selects the most frequent answer”“multiple rounds of aggregation”“end the debate early”。
- [AUTHOR_FACT] 论文提出的具体干预是，在辩论开始前通过提示指定代理对其他代理的目标同意比例：`you should agree with the other agents X% of the time`，X 被称为 agreement intensity。定位：PDF p.6，§3 “Improving MAD via agreement modulation”；短定位文本如前述提示句。
- [AUTHOR_FACT] 在 Multi-Persona 实验中，question 给 angel，agreement/disagreement 的调节施加到 devil 的 system prompt；之后作者观察首轮实际 agreement、最终 consensus 与 accuracy。定位：PDF pp.6–7，§3，Figures 5–6；短定位文本 “modulate the disagreement using the ‘devil’s’ system prompt”。
- [READER_INTERPRETATION] 因而本文最窄、可复现的计算变化是：保持基础 LLM 权重不变，在第一次跨代理信息交换之前，把一个显式 agreement-intensity 控制量写入代理系统提示，从而改变后续辩论轨迹与最终聚合结果；这不是训练新模型，也不是增加一个外部事实 oracle。
- [OPEN_QUESTION] 原文没有给出 agreement-intensity 提示在不同协议中的完整模板拼接位置、与既有 system message 的确切顺序，也没有给出模型是否把百分比校准成概率的机制；Figures 5–6 只说明它能改变经验 agreement，不能证明模型内部按 X 做概率控制。定位：PDF pp.6–7，Figures 5–6。

## 2. 输入、输出、可用信息与干预时点

- [AUTHOR_FACT] 输入主要是多项选择问题及选项；PubMedQA 还包含 context，Chess 是自然语言描述的棋局状态。评测覆盖 MedQA、PubMedQA、medical MMLU、CosmosQA、CIAR、GPQA、Chess。定位：PDF pp.3–4，§3 数据集列表；短定位文本 “multiple-choice question-answering datasets”。
- [AUTHOR_FACT] 基础代理主要使用 GPT-3.5-turbo，经 API 调用；GPT-4 与 Mixtral 8x7B 仅在后续 MedQA 实验中另行评估。定位：PDF p.3，§3 “3.5-turbo engine”；PDF pp.7–9，“Evaluating using other APIs”，Figures 8–9。
- [AUTHOR_FACT] 初始轮次中，每个代理可用 question、agent-level prompt 与 system/debate prompt；后续轮次按协议可额外看到其他代理答案、历史或摘要。Multi-Persona 的 moderator/judge 看到双方答案并决定是否结束及最终答案。定位：PDF pp.2–3，Table 1；PDF pp.20–21，Appendices A.5–A.6，短定位文本 “history of all previous agents’ answers” 与 “At the end of each round, you will evaluate answers”。
- [AUTHOR_FACT] 输出被约束为代表选项的单个大写字母；Multi-Persona 的 judge 中间/最终输出使用包含 `debate_answer` 的 JSON。定位：PDF pp.20–21，Appendices A.5–A.6，短定位文本 “capital multiple choice letter” 与 `"debate_answer"`。
- [AUTHOR_FACT] 干预时点是辩论开始时的 agent prompt/system prompt，而非得到答案后的后处理；测量点包括首轮 agreement、最终轮 consensus、第一代理从首轮到末轮/最终答案的相对准确率变化。定位：PDF pp.6–7，Figures 4–6。
- [READER_INTERPRETATION] 信息可用性不对称是协议的一部分：独立采样方法不共享中间轨迹，SoM/ChatEval 共享或总结历史，Multi-Persona 又额外引入角色先验与 judge。最终准确率差异因此同时反映“是否交流”“交流什么”“谁聚合”与“何时停止”。
- [OPEN_QUESTION] 原文未完整说明各 API 运行的模型快照、随机种子、重试策略、并发/异步实现细节及 API 版本固定方式；这些都会影响生成路径和时间指标。作者在 Limitations 仅承认 inference time 变化与 unforeseen model updates。定位：PDF p.9，§4 Limitations。

## 3. 最强基线与最接近组合基线

- [AUTHOR_FACT] 在原始实现、跨七个数据集的最佳配置比较中，没有协议统治所有数据集；Medprompt 总体表现最好，且作者称其成本也较低。定位：PDF pp.4–5，§3 “The utility of debate”，Table 2；短定位文本 “Medprompt seems to perform the best overall”。
- [AUTHOR_FACT] Table 2 的逐数据集最佳分数显示：Medprompt 在 MedQA 0.65、PubMedQA 0.77、CosmosQA 0.48；Self-Consistency 在 MMLU 0.78、CIAR 0.56；Single Agent 在 GPQA 0.33；Multi-Persona 在 Chess 0.33。定位：PDF p.5，Table 2。该表本身说明“最强基线”随数据集变化。
- [AUTHOR_FACT] 对 agreement modulation 的最近结构匹配基线是未修改的 Multi-Persona：相同 angel/devil/judge 结构，仅改变 devil 的 agreement 提示。原始 Multi-Persona 在 MedQA 总体比 Medprompt 约低 7%，且辩论会使其相对第一代理初始答案的表现下降。定位：PDF pp.4–6，Figure 4；短定位文本 “consistently about 7% worse” 与 “reduces the overall performance”。
- [AUTHOR_FACT] 作者还把 SoM、ChatEval 与 Multi-Persona 的最佳配置都用于 agreement-intensity 扫描；在 376 个 USMLE 问题子集上，Multi-Persona 约提高 15%，SoM 约提高 5%，ChatEval 几乎不受影响。定位：PDF pp.6–7，Figure 6；短定位文本 “substantial (≈15%)” 与 “hardly affected”。
- [READER_INTERPRETATION] 若核验“agreement 提示是否有增量”，最接近组合对照应是同一 Multi-Persona 配置、相同模型/轮数/采样参数下只移除 agreement 提示；若核验“系统最终是否更好”，则应同时对比 Medprompt、Self-Consistency 与按预算匹配的 Single Agent。论文提供这些系统的总体点图和配置表，但没有呈现一个严格单变量、等预算的完整对照表。
- [OPEN_QUESTION] Table 2/Figure 1 的 MedQA 数值区间与 Appendix Table 3 的 MedQA 列并不直观一致（例如主文 Table 2 的 Single Agent 最佳为 0.60，而 Table 3 可见更高的 Single Agent 数值）。原文未解释是否来自不同子集、解析口径、运行批次或表头/排版问题；在外部复核前不应混用这些数值。定位：PDF pp.3–5，Figure 1/Table 2；PDF pp.17–18，Table 3。

## 4. 模型、token、tool-call、prompt、oracle 差异的替代解释

- [AUTHOR_FACT] 主实验选择 GPT-3.5 是成本折中；GPT-4 的 preliminary tests 仅覆盖更小数据子集，后续 GPT-4/Mixtral 图也只针对 MedQA。定位：PDF p.3，§3；PDF pp.7–9，Figures 8–9。
- [AUTHOR_FACT] 系统在 API 调用数、prompt tokens、response tokens、运行时间与美元成本上不同；Figures 1、10–16 把 accuracy 对这些资源作图。作者明确称 MAD 往往需要更多 API calls/tokens，成本更高。定位：PDF pp.3–4，Figure 1；PDF p.9，§4；PDF pp.12–15，Figures 10–16。
- [AUTHOR_FACT] 实验同时改变 agent prompt（SIMPLE、CoT、few-shot、FS-CoT、SPP）、代理数、轮数、reasoning/aggregation 次数、总结、temperature、top-p 及系统特有参数。定位：PDF pp.2–4，§2–3；PDF pp.17–18，Table 3；PDF pp.20–23，Appendices A.5–A.6。
- [AUTHOR_FACT] 作者没有使用完整 Medprompt 的 kNN 检索，因为它需要 train/test split，作者认为这会给 Medprompt 不公平优势；实现只采用 question randomization 与 few-shot CoT ensembling。定位：PDF p.2，§2 “we do not employ the kNN approach”。
- [AUTHOR_FACT] FS-CoT 的医学示例/解释来自 Med-PaLM 工作，由临床人员挑选与编写。定位：PDF p.2，脚注 1。
- [AUTHOR_FACT] 本文协议使用 LLM API 调用，没有报告外部工具调用或检索工具；Appendix 的 ER-CoT 文本虽写 “referring to authoritative sources as needed”，但论文未描述给代理配置检索工具。定位：PDF p.21，Appendix A.6。
- [READER_INTERPRETATION] 结果无法被解释为纯粹“辩论机制”效应：prompt 内容、角色先验、采样参数、调用数和上下文长度共同变化。资源图展示相关性，但没有等 token/等 API-call 的因果消融，因此“更多计算”与“更好交互结构”仍未完全分离。
- [READER_INTERPRETATION] Medprompt 的 kNN 被去除减少了训练集 oracle 优势，但医学 FS-CoT 示例仍带有专家筛选信息；与零样本/简单提示协议比较时，示例质量本身可能贡献准确率。
- [OPEN_QUESTION] 论文没有报告每个协议的严格等 token、等 wall-clock、等 API-call 结果，也没有给出控制 prompt 长度后的 agreement-modulation 消融；额外一句提示带来的上下文变化虽小，但仍未被单独排除。
- [OPEN_QUESTION] agreement intensity 在 376 个 USMLE 子集上选择后再用于“full MedQA”；原文没有说明该 376 子集是否与最终完整 MedQA 评测集合严格不重叠。若有重叠，最优 X 的选择会带来调参信息泄漏。定位：PDF p.6，§3 “subset of MedQA dataset (376...)” 与随后 “apply ... on the full MedQA dataset”。

## 5. 明示限制、负向结果与未测试边界

- [AUTHOR_FACT] 原始 MAD 实现并不可靠地优于 Medprompt/self-consistency，并通常更昂贵；增加计算并不保证提升。定位：PDF p.1 Abstract；PDF p.4 Results；PDF p.9 Conclusions，短定位文本 “do not reliably outperform” 与 “additional computing does not guarantee better results”。
- [AUTHOR_FACT] K-fold 类别迁移结果显示最优超参数往往数据集特定；在非医学数据上 Single Agent 超过除 Multi-Persona 与 Self-Consistency 外的系统，作者明确说新数据集上优于 Single Agent 没有保证。定位：PDF pp.5–6，Figure 3；短定位文本 “not assured for new datasets”。
- [AUTHOR_FACT] Multi-Persona 的 devil 被设计为反对，可能把正确的初始答案拉错，导致辩论后的总体性能低于第一代理初始回答。定位：PDF pp.5–6，Figure 4。
- [AUTHOR_FACT] agreement 的最优方向随数据集变化：MedQA/PubMedQA 受益于高 agreement，CIAR 呈相反趋势。定位：PDF pp.6–7，Figure 5。
- [AUTHOR_FACT] agreement prompt 对 ChatEval 几乎不起作用；从 GPT-3.5 调出的设置可迁移到 GPT-4，但不能良好迁移到 Mixtral 8x7B，作者把架构差异仅作为可能解释并留待未来工作。定位：PDF pp.6–9，Figures 6、8、9；短定位文本 “does not extend well to Mixtral 8x7B”。
- [AUTHOR_FACT] 作者明示限制包括 API 推理时间波动、不可预见的模型更新、大规模 API benchmark 的金钱与时间成本、复现门槛；建议未来使用开源模型和本地基础设施。定位：PDF p.9，§4 Limitations。
- [AUTHOR_FACT] 医学 QA 可能错误且对错误过度自信，可能造成 misinformation/misdiagnosis；作者要求 robust validation、transparency 与伦理谨慎。定位：PDF p.9，Impact Statement。
- [READER_INTERPRETATION] 未测试或覆盖不足的边界包括：开放式生成而非多选题、真实临床决策、非英语、长时程协作、工具增强代理、异构多模型代理、对抗/恶意代理、不同 role 数量和更多开源模型。论文没有就这些边界提供实验支持。
- [OPEN_QUESTION] 未见统计置信区间、显著性检验、重复随机种子方差或多重比较校正；大量配置搜索后的“最佳”分数可能有选择偏差。Figures 1–3/10–16 的点和箱线主要跨配置分布，不等同于独立重复运行的不确定性。
- [OPEN_QUESTION] 作者定义了 incorrectly parsed answers、messages removed due to prompt limit 等指标，但主文未报告这些指标的完整数值分布，无法判断解析失败和上下文截断对各系统排名的影响。定位：PDF p.19，Appendices A.3–A.4。

## 6. 可抽取的 Operator 与真实可记录 Failure

### 可抽取 Operator（仅作论文内容结构化，不作 Candidate 评价）

- [AUTHOR_FACT] `Agreement-intensity prompting`：在辩论开始前把目标同意比例 X 写入代理 system prompt；可扫 X 并监测首轮 agreement/最终 consensus。定位：PDF pp.6–7，Figures 5–6。
- [AUTHOR_FACT] `Role-asymmetric debate`：angel 先答，devil 被提示反对，judge 在每轮评估、可早停并输出最终答案。定位：PDF p.2，§2 Multi-Persona；PDF pp.20–21，MP MAD/MP prompts。
- [AUTHOR_FACT] `History sharing / summarization`：将其他代理回答或摘要追加到后续轮次输入；可选择 sequential、simultaneous 或 summarizer 模式。定位：PDF pp.2–3，Table 1；PDF p.20，CE MAD/SoM MAD。
- [AUTHOR_FACT] `Independent sampling + aggregation`：先独立采样多个 reasoning paths，再做多数选择或多轮 aggregation。定位：PDF p.2，Self-consistency/Ensemble Refinement；PDF pp.17–18，Table 3。
- [AUTHOR_FACT] `Category-level held-out hyperparameter selection`：用同类别另外两个数据集的平均准确率选择配置，再计算目标数据集准确率。定位：PDF p.5，“Is MAD simply sensitive to hyperparameters?”。

### 真实可记录 Failure

- [AUTHOR_FACT] `Failure—MAD non-dominance/cost`：原始 MAD 未稳定超过非辩论方法，并增加 API/tokens/cost。定位：PDF pp.1、4、9，Abstract/Results/Conclusions。
- [AUTHOR_FACT] `Failure—contrarian degradation`：原始 Multi-Persona 的 devil 反对先验可把正确初答拉错，最终性能低于第一代理初答。定位：PDF pp.5–6，Figure 4。
- [AUTHOR_FACT] `Failure—hyperparameter brittleness`：最佳设置依赖数据集；新数据集上优势不保证。定位：PDF pp.5–6，Figure 3。
- [AUTHOR_FACT] `Failure—protocol-specific controllability`：ChatEval 对 agreement prompt 几乎不响应。定位：PDF pp.6–7，Figure 6。
- [AUTHOR_FACT] `Failure—cross-model non-transfer`：GPT-3.5 上调出的 agreement 设置未良好迁移到 Mixtral 8x7B。定位：PDF p.9，Figure 9 后正文。
- [AUTHOR_FACT] `Failure—direction reversal`：高 agreement 在 MedQA/PubMedQA 有利，但 CIAR 反向，说明固定 agreement 策略不稳健。定位：PDF pp.6–7，Figure 5。
- [READER_INTERPRETATION] Appendix A.3/A.4 中的解析错误、prompt-limit 消息移除、被其他代理“bully”等只是被定义的监测指标；因缺少主文数值，不应把它们升级为本文已经实证量化的 Failure。定位：PDF p.19。

## 7. 关键判断—位置索引

| 判断 | 页码 | 章节/图表 | 短定位文本 |
|---|---:|---|---|
| 原始 MAD 不可靠优于非辩论方法 | p.1 | Abstract | “do not reliably outperform” |
| 推理时 in-context 交互，无梯度更新 | p.2 | §2 | “no gradient-based parameter updates” |
| 协议功能差异 | p.3 | Table 1 | “Feature comparison” |
| 成本/API calls/准确率关系 | pp.3–4 | Figure 1 / Results | “Accuracy vs average cost” |
| 跨数据集最佳结果、无单一统治者 | pp.4–5 | Table 2 | “no protocol dominates” |
| K-fold 超参数敏感性 | pp.5–6 | Figure 3 | “dataset-specific fine-tuning” |
| Multi-Persona 辩论后退化 | pp.5–6 | Figure 4 | “reduces the overall performance” |
| agreement-intensity 提示定义 | p.6 | §3 | “agree ... X% of the time” |
| 数据集间方向反转 | pp.6–7 | Figure 5 | “CIAR follows a reverse pattern” |
| USMLE 子集增益及协议差异 | pp.6–7 | Figure 6 | “≈15% ... ≈5%” |
| GPT-4/Mixtral 迁移 | pp.7–9 | Figures 8–9 | “does not extend well to Mixtral” |
| API/成本/模型更新限制 | p.9 | Limitations | “unforeseen model updates” |
| 各配置与成本 | pp.17–18 | Table 3 | “Complete table” |
| 解析/截断等监测指标 | p.19 | A.3–A.4 | “incorrectly parsed”“messages removed” |
| 具体 debate/agent prompts | pp.20–23 | A.5–A.6 | “ANGEL”“DEVIL”“judge_system_message” |

## 8. 解析文本与可视 PDF 的一致性检查

- [AUTHOR_FACT] 已逐页提取 p.1–23 的文本，并将全部 23 页从 PDF 原始页面在内存中渲染检查；正文、双栏结构、Figures 1–16、Tables 1–3、Appendices A.1–A.6 的页面位置与解析结果一致。p.16 仅有 Appendix A.2 标题和引导句，视觉上确为大面积留白；p.17–18 是跨页宽表；p.21–23 是长 prompt 示例。
- [READER_INTERPRETATION] 未发现会改变本文主要结论的“解析文本—可视页面”冲突。解析器对 Table 3 的多行单元格会拆行，图中点位/曲线也只能通过视觉图形而非线性文本恢复；因此本报告对精确数值优先引用正文和清晰表格，不从低分辨率图形估读额外数值。
- [OPEN_QUESTION] 主文 Table 2/Figure 1 与 Appendix Table 3 的部分 MedQA 数值口径看起来存在内部不一致，但这不是 PDF 渲染与文本解析冲突，而是原文跨表口径未解释的问题；需要代码/运行产物或作者说明才能消解，本次隔离二读不联网且不读取其他材料，故保持开放。

## 9. 二读边界声明

本报告仅回答统一问题并记录可核源事实、读者解释与开放问题；没有读取或合并首读意见，没有生成正式 Card，没有投票、打分或作 Candidate 科研裁决。
