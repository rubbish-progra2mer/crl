# P096 独立二读报告（fresh reader, W06 扩充波次）

- 读者：r2-20260727-p096-a1（独立二读，未接触 read_1 / reconciliation / 任何 Card）
- 日期：2026-07-27
- 论文文件：D:\Desktop\crl\crl_agent_v3\knowledge_base\staging\w06_targeted\P096_verisimpl.pdf
- 实测 SHA-256：81b34a7084aa5552ef9a1491ec5e5f9da5c149e80beb06fe81fc163ae4d595b3（与任务给定值一致）
- 实测物理页数：33（pymupdf page_count；PDF 物理页与印刷页码一一对应，第 1 物理页印刷页码为 1）
- canonical metadata 核对：标题 "VeriSimpl: Robust Optimization Modeling from Natural Language using Simplification-based Verification"（p1）；arXiv 水印 "arXiv:2607.20474v1 [cs.AI] 24 May 2026"（p1 左缘竖排，视觉确认）；出版脚注 "Proceedings of the 43rd International Conference on Machine Learning, Seoul, South Korea. PMLR 306, 2026"（p1 脚注，视觉确认）。与 canonical（arXiv 2607.20474v1, ICML 2026, PMLR 306）一致。
- 作者（p1）：Sumaya Abdul Rahman (Texas A&M University at Qatar), Seckhen Ariel Andrade Cuellar, Ghani Raissov (Carnegie Mellon University in Qatar), Mohammad Raza (Qatar Computing Research Institute；通讯 mraza@hbku.edu.qa)。
- 读取方法：python+pymupdf 全文逐页抽取；对 p1, p2, p5, p6, p7, p13, p15, p21, p22, p27 共 10 页做 150 dpi 渲染视觉抽查（覆盖全部主表 Table 1-4 与附录表 Table 11-13、Figure 1、Algorithm 3、两处异常引文页、一处 prompt 示例页）。

标签纪律：每条内容陈述恰用一个标签 [AUTHOR_FACT] / [READER_INTERPRETATION] / [OPEN_QUESTION]。

---

## Q1. 方法究竟改变哪一步计算？

1.1 [AUTHOR_FACT] 基线流水线是“LLM 先把问题写成求解器代码、solver 只负责执行”的顺序过程；VeriSimpl 改变的是生成与最终执行之间的一步：加入 solver-LLM 联合的候选验证与选择。定位：p2, §2，"Standard approaches generally follow a sequential process"；p3, §2 Outline，"The program with the highest verification score is selected and executed on the input data to return the optimal solution."

1.2 [AUTHOR_FACT] 具体计算改动（Algorithm 1, p4）：(a) 用温度采样生成 K 个候选程序（"in our experiments we consider up to K = 10"，p5）；(b) 对每个候选计算四个验证分数：sc=CONSTRAINTVERIFY（约束突变可行性探针）、sd=VARVERIFY 对所有 singleton 变量掩码、sf=VARVERIFY 对全变量集掩码、st=TYPEVERIFY（并回写修订后的类型注释）；(c) 按字典序聚合 s(Pk)=(sc+sd+sf, st)，"prioritizing semantic correctness (constraints and variables) followed by type-based correctness"（p5）；(d) argmax 选出候选后才交给 solver 求最终解。

1.3 [AUTHOR_FACT] 概念上的反转：不是让 LLM 出测试、solver 核对，而是让 solver 从候选程序构造简化诊断查询、LLM 依据 NL 描述独立作答。定位：p2, §1，"instead of using the LLM to propose test scenarios that are then checked by the solver, we leverage the solver's reliability in constructing feasible and optimal solutions in high-dimensional space"；p3，"simplification queries are not test cases in the standard sense"。

1.4 [READER_INTERPRETATION] 本质上这是一个 test-time best-of-K 选择器（外加唯一的一处程序修改：类型注释回写）。它不改训练、不改 solver、不改除类型外的程序内容；所有“新计算”都发生在候选打分环节。

## Q2. 输入、输出、可用信息与干预时点

2.1 [AUTHOR_FACT] 输入：自然语言描述 x + 结构化输入数据 d（"tabular data and parameters formatted in a structured format such as JSON or CSV"）。输出：(Pk*, st, v*)，即被选中的程序、solver 状态与最优 valuation（Algorithm 1 line 11-12）。定位：p4, §3 "Problem Setup"。

2.2 [AUTHOR_FACT] 两个黑盒接口：SOLVE(S;M)→(status, v)，status∈{OPT, FEAS, INFEAS}；LLM 侧 LLMGENPROGRAMS（温度采样 + "standard error-based refinement"，引 Shinn et al. 2023，prompts 在 Fig.4/5）与 LLMINFER（回答验证查询）。定位：p4。

2.3 [AUTHOR_FACT] 验证时 LLM 的可用信息被刻意限制为 NL 描述 + 数据 + 具体数值 valuation："the LLM is asked to independently reason about the query and its expected outcome based only on the natural language problem description"（p3）。oracle 值（witness valuation / v*）由 solver 对候选程序自身的模型计算，不接触数据集 ground truth。

2.4 [AUTHOR_FACT] 干预时点：纯推理期（候选程序生成之后、最终求解之前）；唯一改动程序本体的是 TYPEVERIFY "returns an updated program with the revised type annotations"（p5）。

2.5 [AUTHOR_FACT] 实现细节（附录 prompts）：约束可行性查询的 LLMINFER 实际是让 LLM 生成一个 "Feasibility Checking Program"（Python）再在流水线中执行（Fig.6, p26-28）；变量掩码查询是直接输出 JSON 推理（Fig.7, p29-30）；类型查询输出每变量 [meaning, reasoning, final_answer] JSON（Fig.8, p31-33）。

2.6 [AUTHOR_FACT] 算法细节（p4-5）：每个约束归一化为 e(V)<=0，取小固定 margin δ>0，做三个突变 c<: e(V)<=-δ、c=: e(V)=0、c>: e(V)>=+δ；只有当突变后模型可满足（OPT/FEAS）时该查询才计入 total（Algorithm 2 line 6-11）；判分为 1[y_hat ⇔ (τ∈{<,=})]。变量掩码验证仅当原模型 status=OPT 才执行，返回 pass/|T|（Algorithm 3）。

2.7 [AUTHOR_FACT] 效率限制："our implementation also imposes a fixed upper bound on the number of singleton variables considered for masking"（p5），具体数值未给。

2.8 [OPEN_QUESTION] 等式约束如何进入 e(V)<=0 归一化、以及 Gurobi 中 addConstrs 生成的 indexed 约束族按什么粒度算“一个约束 c”，原文均未说明。δ 的取值也未给（代码生成 prompt 中的 epsilon=1e-4 是另一回事，p23）。

## Q3. 最强基线与最接近组合基线

3.1 [AUTHOR_FACT] 基线集合（p6 "Baselines"）：BASELLM（直接提示）、COE（Chain-of-Experts；数字直接照抄 Xiao et al. 2024）、SELFDEBUG（solver 报错反馈迭代修正，引 Chen et al. 2024）、OPTIMUS（"we ran the authors' released implementation of OPTIMUS with the LLM models that we use"）。

3.2 [AUTHOR_FACT] 平均意义上最强基线是 SELFDEBUG：GPT-4o avg 59.1（Table 1, p6）、R1 avg 67.9（Table 2, p6）、Mistral avg 58.3（Table 10, p20）；对应 VeriSimpl 为 65.5 / 72.8 / 62.5。单数据集最强单点基线是 OPTIMUS 在 NL4Opt+GPT-4o 的 85.9（VeriSimpl 88.1）。

3.3 [READER_INTERPRETATION] 最接近的“组合”基线是 SELFDEBUG（LLM+solver 执行反馈），但它只保证可执行性、不验证语义。真正应该有而缺失的组合对照是：同样采样 K=10 个候选、用朴素选择器（多数投票 / 目标值自一致性 / 随机挑一个可执行的）——论文没有任何 compute-matched 的 best-of-K 对照。

3.4 [AUTHOR_FACT] COE 在 NLP4LP 与 IndOR 无数值（表中 "-"），且底座模型与本文不同（表题 "except COE"，p6），不可直接比较。

## Q4. 结果是否可能来自模型、token、tool-call、prompt 或 oracle 差异？

4.1 [READER_INTERPRETATION] 推理算力不对等是主要归因风险：VeriSimpl 每题最多 10 个候选，每候选要做（每约束 3 次 solver 求解 + 一次约束检查代码生成执行）+（受上界限制的 singleton 掩码查询 + 1 次全掩码查询）+ 1 次类型查询；BASELLM/SELFDEBUG 单链路。论文完全未报告 token 数、LLM/solver 调用次数、成本或时延。

4.2 [READER_INTERPRETATION] 消融数据反而暗示 best-of-K 效应占了增益大头：GPT-4o 下 BASELLM 56.8 → 任何单一验证信号的 10 候选选择器即达 62.2-64.8，全量 65.5（Table 4, p7）；即“采样+任意合理选择器”贡献约 5.4-8.0 点，各信号叠加的边际只有约 0.7-3.3 点。注意 A-CONS/A-SINGLEVAR/A-FULLVAR 是 "performs only" 变体、A-TYPE 是 "disables ... (line 7)" 的 drop-one 变体（p7），两种消融语义混用。

4.3 [AUTHOR_FACT] 跨底座一致性是作者的反驳证据：GPT-4o、R1、Mistral large 三个底座上 VeriSimpl 平均都最高（65.5 / 72.8 / 62.5），作者称这表明是方法性改进 "as opposed to model-specific improvements from prompt engineering or fine-tuning"（p6）。

4.4 [AUTHOR_FACT] oracle 无泄漏：验证 oracle（witness/最优 valuation）由 solver 对候选自身模型计算；LLM 答题只用 NL+数据；数据集真值不进入验证环节（p3-5）。[OPEN_QUESTION] 但 accuracy 的判定标准（与 ground-truth 最优值比对的方式与数值容差）全文未定义。

4.5 [READER_INTERPRETATION] 基线侧的 prompt/移植风险：OPTIMUS 用其原实现跑在 GPT-4o/R1/Mistral 上，在 NLP4LP/CompOR/IndOR 跌至 13.1-56.3（Tables 1/2/10），可能部分反映移植失配而非方法差；COE 为模型不匹配的照抄数字。

4.6 [READER_INTERPRETATION] 有效样本数疑点影响与外部文献数字的可比性：NLP4LP 名义 67 题，但各系统百分比几乎都可写成 /62 的整数比（43.5=27/62、51.6=32/62、58.1≈36/62），Table 13 的 57.4/55.7 吻合 /61，Mistral 行吻合 /61；IndOR 名义 100 题，GPT-4o/R1 百分比吻合 /96（42.7=41/96、67.7=65/96），Mistral 行吻合 /95。论文只声明 NL4Opt 有剔除（269 题）与 CompOR 用 17 题。见不一致清单 I-6。

## Q5. 作者明示限制、负向结果、未测试边界

5.1 [AUTHOR_FACT] 假阳性主因是“共享误解”："a misinterpretation of the natural-language specification that can lead both the symbolic formulation and the LLM's concrete reasoning to consistently agree on the same incorrect model of the problem, e.g. a shared incorrect decision-variable interpretation of 'start time' in a shift scheduling problem, or not considering certain costs in a profit objective calculation"（p7-8, §4.4）。

5.2 [AUTHOR_FACT] 明示的两条能力边界（p8）："decision variables are assumed as given and shared between the llm reasoning and solver analysis, and simplification queries do not cover any aspects of the NL description that may be completely missed or ignored by the candidate program rather than incorrectly formulated"；future work 指向 variable definitions 验证与 coverage-oriented checks。

5.3 [AUTHOR_FACT] 负向结果：coverage 低（GPT-4o avg 34.2、R1 avg 23.0、Mistral avg 27.7；Tables 3/11），成因是 all-pass 的严格性："any mismatches (whether due to problem description ambiguity or reasoning noise) can cause otherwise-correct solutions to fail full verification (false negatives)"（p7）；A-FULLVAR "shows consistently low coverage, reflecting the brittleness of end-to-end objective verification"（p7）。

5.4 [AUTHOR_FACT] B.2 显示验证信号是采样依赖的：同一实例上，一次采样中掩码 TotalProfit 的推理正确、与错误目标不符 → 验证失败（正确地拒绝）；"In a subsequent sampling instance, however, the reasoning path taken by VERISIMPL differed"，复刻同样漏成本错误 → 验证通过成为假阳性（p20）。

5.5 [READER_INTERPRETATION] R1 的 self-verification precision 系统性低于 GPT-4o（78.5 vs 91.5 avg；CompOR 上仅 66.7，Table 3, p6）——“高精度信号”并非跨模型稳定，作者未解释这一反直觉现象（更强推理模型的验证信号反而更不可靠）。

5.6 [READER_INTERPRETATION] 未测试边界：全部实验与 prompts 都是 Gurobi/LP/MILP（Fig.4-8 均为 Gurobi 专用；抽象算法虽声明 solver-agnostic，p4 "e.g. in Gurobi/CPLEX/SCIP APIs"，但未在其他 solver 上验证）；非线性/约束规划未涉及；无 K 敏感性、无 δ 与 singleton 上界数值、无 seed/方差、无成本与时延、无人类用户研究支持“减少人工检查负担”的实践性主张。

## Q6. 可抽取 Operator 与真实可记录 Failure

Operator 候选（机制为 [AUTHOR_FACT] 所述 + 抽取判断为 [READER_INTERPRETATION]）：

- OP-1 约束突变可行性探针：约束归一化为 e(V)<=0，构造 {<=-δ, =0, >=+δ} 三突变，solver 生成 witness valuation，LLM 仅凭 NL 判可行性，判分 1[y_hat ⇔ (τ∈{<,=})]；INFEAS 突变不计入分母。定位：Algorithm 2（p4）、§3 "Constraint-based Simplification"（p5）、Fig.6（p26-28，LLM 以生成检查代码的方式作答）。
- OP-2 solver-最优上下文中的变量掩码估值探针：先 SOLVE 得 v*，reveal V\t 的最优值、让 LLM 推 masked 子集 t；t 取所有 singleton（有上界）与全集 V 两档；与 v* 一致才通过。定位：Algorithm 3（p5）、Fig.7（p29-30）；全掩码档是“高精度低覆盖”信号（p5）。
- OP-3 字典序聚合选择器：s(Pk)=(sc+sd+sf, st)，语义分优先、类型分次之，argmax 后才执行。定位：Algorithm 1 line 8-11（p4）、p5 "aggregated into a lexicographic ranking"。
- OP-4 类型验证与回写：LLM 按 NL 语义判定每个决策变量 continuous/integer/binary，返回二值分并回写类型注释（唯一的程序修复动作）。定位：p5 "Type-based verification"、Fig.8（p31-33）。
- OP-5 all-pass 自验证门控作为置信信号：全部查询通过的实例集合上 precision 显著高于端到端 accuracy（GPT-4o avg 91.5 vs 65.5，Table 3, p6；Mistral 83.8，Table 11, p21），可用作“该题大概率无需人工复查”的路由信号；代价是 coverage 仅约 23-34%。
- OP-6（弱，属既有技术）solver 报错反馈的可执行性修复循环（Fig.5, p25；引 Reflexion/SelfDebug），仅保证可执行、不验证语义。

真实可记录 Failure（均 [AUTHOR_FACT] 有定位）：

- F-1 共享变量语义误解假阳性：B.1（p18-19）班车排班题，决策变量被当成“该时段在岗人数”而非“该时段开始上班人数”，模型代数自洽、掩码重建 100% 通过，但运营上不可行；"VERISIMPL failed to detect this modeling error because its predictive inference relies on algebraic consistency among fixed variables rather than semantic reasoning"（p19）。
- F-2 目标函数漏项 + 采样漂移假阳性：B.2（p19-20）宠物食品题，目标漏减原料成本；掩码单变量时 LLM 以 solver 目标值为锚复原出同样的错值（"effectively solved a constrained completion problem"，p20）；掩码 TotalProfit 时不同采样一次抓到错误、一次复刻错误放行。
- F-3 低覆盖假阴性：严格 all-pass 使 66-77% 的正确解得不到 verified 标记（coverage 23.0-34.2，Tables 3/11），作者归因于描述歧义与 reasoning noise（p7）。
- F-4 端到端目标验证（全掩码）对 LLM 过难：A-FULLVAR 精度/覆盖双低、"mostly performs worse than the other features"（p7, Figure 3）。

## Q7. 判断-定位对照（补充未在上文逐条内嵌者）

7.1 [AUTHOR_FACT] 数据集规模：NL4Opt test "after removing some infeasible cases, contains 269 problems"（p5）；NLP4LP "67 problems"（p5）；CompOR "We use the 17 problems that are currently publicly released and checked with feasible solutions"（p5-6）；IndOR "100 real-world problems"（p6）。
7.2 [AUTHOR_FACT] 主结果：Table 1（p6, GPT-4o）VeriSimpl 88.1/51.6/76.5/45.8/65.5；Table 2（p6, R1）88.8/58.1/76.5/67.7/72.8；Table 10（p20, Mistral）91.4/42.6/70.6/45.3/62.5。
7.3 [AUTHOR_FACT] precision/coverage 定义："precision is defined as the proportion of correctly answered cases out of all fully verified cases, and coverage is defined as the proportion of fully verified cases out of all correctly answered cases"（p6-7, §4.2）。
7.4 [AUTHOR_FACT] "even such limited coverage of 20-30% can provide a substantial reduction in manual verification burden in practice"（p7）——注意这是作者论断，无用户研究支撑（见 5.6）。
7.5 [AUTHOR_FACT] 与 mutation testing 的关系："conceptually closest to mutation testing ... the solver not only supplies the oracle, but also constructs semantically targeted simplifications"（p8, §5）。
7.6 [AUTHOR_FACT] 机制示例（timber 例）：错误约束 inventory<=capacity/10000 时，"an inventory of 19 and 20 should be feasible, but 21 should be infeasible"，LLM 按 NL 判 21 也可行 → 突变查询失败（p3）。

## Q8. 解析文本与可视 PDF 是否冲突（就抽查页作答）

8.1 [READER_INTERPRETATION] 就我抽查的 10 页（p1, p2, p5, p6, p7, p13, p15, p21, p22, p27）而言，pymupdf 抽取文本与视觉渲染无冲突：Table 1-4、Table 11-13 的全部数字、Figure 1 的正误代码对照、Algorithm 3 与三突变定义、p13/p15 的异常引文、p27 的 <E1>/<E5> 标签问题，均在视觉上得到确认。下面清单里的异常是论文本身的内容，不是解析伪影。
8.2 [READER_INTERPRETATION] 抽取的表格是线性化的（逐单元格换行），但顺序与视觉一致，未见 OCR 型错字。

## 附一：论文内部数值/文字不一致清单（供 reconciliation 使用）

- I-1 [AUTHOR_FACT] p6 正文写 "(88.1 vs. 88.5)"，但 Table 2 的 R1-NL4Opt 是 88.8。二者必有一误。
- I-2 [AUTHOR_FACT] Table 2（p6）与 Table 13（p22）同为 R1 的 VeriSimpl 数字不一致：NLP4LP 58.1 vs 57.4；IndOR 67.7 vs 67.4；Avg 72.8 vs 72.5（Table 4, p7 也用 72.5）。
- I-3 [AUTHOR_FACT] Table 3（p6）与 Table 13（p22）的 R1 precision/coverage 漂移：NL4Opt 95.7/38.2 vs 95.8/38.5；CompOR cov 15.3 vs 15.4；IndOR cov 21.3 vs 20.3；avg cov 23.0 vs 22.8。GPT-4o 侧（Table 1/3/4/12）完全自洽。[READER_INTERPRETATION] R1 数字疑似来自两次不同的统计/重跑。
- I-4 [AUTHOR_FACT] Table 1 BASELLM Avg 印作 56.8，但 (75.5+43.5+64.7+42.7)/4=56.6。
- I-5 [AUTHOR_FACT] Table 11（p21）Mistral Avg coverage 印作 27.7，但 (22.8+11.5+58.3+16.3)/4=27.2。
- I-6 [OPEN_QUESTION] 有效分母：NLP4LP 百分比吻合 /62（Table 1/2）与 /61（Table 13、Mistral），IndOR 吻合 /96（GPT-4o/R1）与 /95（Mistral），与声明的 67/100 不符；NL4Opt（/269）与 CompOR（/17）完全吻合。是否存在未声明的样本剔除（如执行失败）？
- I-7 [OPEN_QUESTION] A.2（p13）与 A.3（p15）的 "LLM Masked Reasoning" 引文与其所述问题实例数值完全不符：A.2 引文说 "Each motorcycle trip produces 2 units of pollution ... at least 5 units ... not exceed 4 ... cannot exceed 3 ... total pollution is 6.0"，而问题是 40/70/100 污染、>=300 单位、<=20 趟、<=8 趟、最优污染 600；A.3 引文说 "C is mandatory ... The cost of taking C is $4 ... up to two children"（儿童 A/B/C），而问题是 Zhang 家六子、至少 3 至多 4 人、总成本 $3050。结论值（trips[1]=2、TotalCost）却与 solver 解一致。疑似贴入了缩放/匿名化后另一实例的 transcript；这两处“成功案例”的示证价值因此存疑（已视觉确认非解析错误）。
- I-8 [OPEN_QUESTION] B.1（p18）使用未在正文定义的术语 "predictive inference verification (System-10)"，疑似内部系统代号残留。
- I-9 [AUTHOR_FACT] Fig.6 一步示例（p27）里 TEST CASE #5 的标签印作 <E1>，对应代码却是 "<E5>"（小错，视觉确认）。
- I-10 [AUTHOR_FACT] Fig.7（p29-30）System Prompt 要求输出字段 "predicted_values"（map），User Prompt Template 却要求 "predicted_value": <float>——字段名与结构不一致。
- I-11 [AUTHOR_FACT] 若干笔误不影响语义："aggregated into final a verification score"（p3）、"queries. using the solver"（p5）、"misinterpration"、"Theses cases"、两处小写 "llm"（p8）。

## 附二：汇总 Open Questions

- OQ-1 [OPEN_QUESTION] accuracy 的判定标准（与真值最优目标的比较方式、数值容差、是否核对解本身）全文未定义。
- OQ-2 [OPEN_QUESTION] 关键超参数缺失：δ 数值、singleton 掩码上界、K 的敏感性、采样温度、tie-breaking（argmax 平局与全零分时如何选）。
- OQ-3 [OPEN_QUESTION] 每题 LLM/solver 调用数与 token 成本未报告；无 compute-matched best-of-K 基线，增益中验证信号 vs 采样效应的占比无法从主表分离（仅能从消融间接估计，见 4.2）。
- OQ-4 [OPEN_QUESTION] COE 行的底座模型未说明（照抄 Xiao et al. 2024）。
- OQ-5 [OPEN_QUESTION] 等式约束的突变语义与 indexed 约束族的粒度（见 2.8）。
- OQ-6 [OPEN_QUESTION] R1 上验证 precision 反而更低的原因（见 5.5），以及 R1 两套数字（I-2/I-3）哪套是最终版。
