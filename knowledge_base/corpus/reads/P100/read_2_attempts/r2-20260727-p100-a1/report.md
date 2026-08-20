# P100 独立二读报告（fresh reader，W06 扩充波次）

- 报告 ID：r2-20260727-p100-a1
- 读者角色：独立二读（未接触 read_1、reconciliation、任何 Card 或 Run 目录）
- 读取对象：D:\\Desktop\\crl\\crl_agent_v3\\knowledge_base\\staging\\w06_targeted\\P100_tool_shortlist_size.pdf
- 实测 SHA-256：4db89bfac79bc90dd5b532d04ac1012ed1691657a45379bbbb2312682847164c（与任务给定值一致）
- 实测物理页数：13 页（PyMuPDF page_count=13）
- canonical metadata 核对：PDF 第 1 页左侧竖排水印 "arXiv:2605.24660v2 [cs.IR] 7 Jun 2026"，标题 "How Many Tools Should an LLM Agent See? A Chance-Corrected Answer"，页脚 "Preprint."，作者单位 Meta Platforms——与给定 canonical metadata（arXiv 2605.24660v2, 2026-06-07, preprint）一致。[AUTHOR_FACT]（p.1，标题区与左缘水印）
- 抽取方式：PyMuPDF 全文抽取（45,799 字符）+ 对 p.1、p.5、p.7、p.8、p.9、p.13 做 150dpi 渲染视觉抽查。

体例说明：每条内容陈述恰用一个标签 [AUTHOR_FACT] / [READER_INTERPRETATION] / [OPEN_QUESTION]；定位格式为（物理页码，章节/图表，"短逐字定位语"）。本文物理页码与论文印刷页码一致（p.1 即印刷第 1 页）。

---

## Q1. 方法究竟改变哪一步计算？

1.1 [AUTHOR_FACT] 论文改变的是"检索器打分之后、LLM 看到 prompt 之前"的截断步骤：不再对每个查询用固定 K 截取候选工具，而是把"呈现多少个工具"本身作为评估对象与学习对象。定位：（p.1，Abstract，"We treat the number of tools shown to an LLM agent as the object of evaluation"）；（p.1，Sec.1，"This search depth K ... is typically chosen once and never revisited"）。

1.2 [AUTHOR_FACT] 具体机制分两层：(a) 评估层——用 Bits-over-Random（BoR）这一 chance-corrected 指标衡量给定深度下的成功率是否优于同深度随机选择，BoR = log2(Pobs/Prand)；(b) 控制层——把同一原理变成 RL 奖励，训练一个逐项检查排序列表并决定 STOP/CONTINUE 的停止策略。定位：（p.2，Sec.1 末，"we apply the Bits-over-Random (BoR) metric"）；（p.4，Sec.3.2，"present the tools examined so far to the LLM (STOP), or look at the next candidate (CONTINUE)"）。

1.3 [AUTHOR_FACT] 检索打分器本身不变（BM25 或 sentence embeddings 对全部 N 个工具排序），LLM 的选择步骤也不变；被替换的仅是排序列表上的截断规则。定位：（p.4，Sec.3.2，"a scorer (BM25 or a sentence-embedding model) ranks all N candidate tools"）。

1.4 [READER_INTERPRETATION] 换言之，这是一篇"指标 + 以指标为奖励的探针"论文，不是新检索器、不是新 LLM 调用方式；作者自己也把 RL agent 定位为对指标性质的探针而非提案系统（见 Q5）。

## Q2. 输入、输出、可用信息与干预时点分别是什么？

2.1 [AUTHOR_FACT] MDP 框定：一个查询 = 一个 episode。状态输入包括：已检查工具的相似度分数（含 top score、首分与当前分的 gap、分数 spread）、当前深度 kt、registry 大小 N、当前深度下的 BoR ceiling。定位：（p.4，Sec.3.2 State，"the top score, the gap between the first and current score, and the score spread"）。

2.2 [AUTHOR_FACT] 动作输出：二元 STOP / CONTINUE；停止时输出的即是呈现给 LLM 的前 kstop 个工具。定位：（p.5，Action 段，"Binary: STOP or CONTINUE"）。

2.3 [AUTHOR_FACT] 奖励（训练期可用信息）：STOP 时若呈现集合含至少一个相关工具，奖励为 −log2(Prand(kstop; Rq))，否则为 0；另有每步 continuation cost（step_cost=0.01, γ=0.95；例外：MetaTool+BM25 用 γ=1.0，BFCL+BM25 用 step_cost=0.005）。定位：（p.5，Reward 段，"the reward is −log2(Prand(kstop; Rq)), and zero otherwise"）。

2.4 [AUTHOR_FACT] 训练用 oracle Rq（相关性标注），推理时假设 Rq=1，因为各基准每个查询恰有一个正确工具。定位：（p.5，Reward 段，"trained with oracle Rq and assumes Rq=1 at inference"）。

2.5 [AUTHOR_FACT] 干预时点：在 scorer 完成全量排序之后、prompt 构建之前；成功判据是 Success@K（呈现集中至少含一个相关工具），全部实验用 ≥1 规则。定位：（p.4，Sec.3.1，"all experiments in this paper use the ≥1 rule"）；（p.5，Sec.4，"We report 'Found%' as Success@K"）。

2.6 [AUTHOR_FACT] 下游验证（Sec.4.3）的输入输出：各方法的工具集合呈现给 Claude Sonnet 4.6，约束其恰选一个工具；工具描述与 scorer 排序在各方法间保持一致，仅集合大小不同；120 个测试查询，N=370，3 seeds，temperature=0。定位：（p.8，Sec.4.3，"a constraint that forces the model to select exactly one tool"；"only the set size varying"）。

2.7 [READER_INTERPRETATION] 值得注意：策略只看分数形状特征（不看查询或工具文本本身），因此它学到的是"从分数分布推断该查询难度并决定停在哪"，这解释了为何 scorer 质量直接决定策略行为（Q5 的负向结果）。

## Q3. 最强基线与最接近组合基线是什么？

3.1 [AUTHOR_FACT] 基线一（最强覆盖率基线）：Fixed-K，逐条件取最优深度报告为 "Best FK"。各条件最强值：BFCL+BM25 为 FK=50（90.8%）；BFCL+embed 为 FK=5（97.5%）；ToolBench(N=50) 为 FK=20（77.3%）；MetaTool+BM25 为 FK=50（83.7%）等，见 Table 2。定位：（p.9，Table 2，"Best FK Found%" 列）。

3.2 [AUTHOR_FACT] 基线二（最接近的组合基线/消融）：F1 ablation——同样的 RL 架构与训练流程，但把奖励换成 F1 = 2/(K+1)（recall=1、precision=1/K 时），即"深度惩罚存在但与查询/registry 无关"的深度感知奖励。目的为检验"任何深度压力是否都能产生同样的自适应行为"。定位：（p.5，Baselines 段，"an F1 ablation, which tests whether any depth-aware reward produces the same adaptive behavior"）。

3.3 [AUTHOR_FACT] 重要脚注：BFCL+BM25 条件下的 F1 基线用的是更简化的变体——常数终端奖励 1.0，深度压力仅来自 γ 折扣；作者称这比 2/(K+1) 更宽松，使比较偏保守（"The true F1 baseline would stop earlier"）。定位：（p.5，脚注 1，"a constant terminal reward of 1.0"）。

3.4 [READER_INTERPRETATION] 就"组合基线"意义而言，F1 ablation 是干净的：它保留"RL+自适应停止"、只拿掉"chance correction"，因此 BoR vs F1 的差值可归因于奖励的 chance-corrected 结构而非 RL 本身。但 3.3 的脚注意味着九个条件中有一个条件的 F1 对比不是同一公式，跨条件比较 F1 列时需要记住这一点。

3.5 [AUTHOR_FACT] 相关工作中作者明确承认 DynamicRAG 是最接近的先行系统（动态调整重排数量，但面向文档、以下游生成质量为奖励），并声明未见先行工作以 chance-corrected 奖励学习搜索深度。定位：（p.2，Sec.2.1，"DynamicRAG [34] is closely related"）；（p.4，Sec.2.4 末，"We are not aware of prior work that treats search depth as a first-class property"）。

## Q4. 结果是否可能来自模型、token、tool-call、prompt 或 oracle 差异？

4.1 [AUTHOR_FACT] 覆盖率实验（Sec.4.1/4.2、Table 2）完全不涉及 LLM：Found% 是纯集合包含判定（gold 是否在前 K），故不存在模型/prompt/tool-call 混淆。Prand 在所有工具选择实验中按候选集大小 N 计算。定位：（p.5，Sec.4，"Prand is computed against the candidate set size N"）。

4.2 [AUTHOR_FACT] 下游验证做了如下控制：同一 LLM（Claude Sonnet 4.6）、temperature=0、强制单选、工具描述与排序一致、仅集合大小变化。定位：（p.8，Sec.4.3 正文）。

4.3 [READER_INTERPRETATION] 残余混淆一（条件化选择偏差）：Choice Acc% 以"gold 被呈现"为条件，而各方法的条件集不同——BoR 只在 76.9% 查询上呈现 gold（多为 scorer 排名靠前的容易查询），FK=5 在 84.2% 上呈现（含更难的查询）。BoR 的 93.1% 与 FK=5 的 87.1% 因此在不同查询子集上计算。分桶分析（medium 桶内 76.8% vs 60.9%）部分缓解了这一点，但即使在 medium 桶内，BoR 也只在 62.3±2.0% 的查询上呈现，其条件子集仍可能偏容易。该混淆不推翻"over-presentation 有害"的方向性结论（FK=5 桶内 100% 呈现仍只有 60.9% 选对），但可能放大表面差距。依据数值定位：（p.8，Table 1 及 per-bucket 段）。

4.4 [READER_INTERPRETATION] 残余混淆二（超参数不对齐）：下游验证的 RL agent 用 step_cost=0.01/γ=0.95 重训，得 K=2.2，而主表 BFCL+BM25 agent 是 step_cost=0.005、K=7.4。作者明示了这一点（p.8，"retrained for this setup with the standard hyperparameters"），但这意味着"BoR 策略"的行为对 step_cost 敏感（同一奖励、不同 step_cost，K 差 3 倍多），下游结论绑定于特定超参选择。

4.5 [READER_INTERPRETATION] oracle 差异：训练期 BoR 与 F1 两个 RL 基线同样使用 oracle 相关性标注（对称，不构成 BoR 独有优势）；Fixed-K 完全无需训练与标注。推理期无 oracle。因此"BoR vs F1"无 oracle 不对称；"RL 方法 vs Fixed-K"存在训练数据需求上的不对称，但这是方法类别的固有差别而非测量泄漏。

4.6 [READER_INTERPRETATION] token 差异：下游实验中列表长度不同意味着 prompt token 数不同，但这正是被操纵的自变量（distractor load），不是混淆项。覆盖率实验与 token 无关。

4.7 [READER_INTERPRETATION] 构造性混淆（候选集构造）：MetaTool 与 ToolBench 实验的候选集由"gold + hard distractors (+ 随机填充)"人工构造（p.6），gold 恒在候选集内，Prand 按该构造集的 N 计算。这使 Found% 的绝对值依赖构造方式，跨论文比较时不应把这些数字当作对原基准的检索性能。MS MARCO 一例中本地索引仅约 51K passages 而 Prand 按全库 N=8,841,823 计算（p.12，"BoR is computed against the full corpus"），使 reward 位数（20.28 bits）显著偏大——奖励量级跨语料不可比。

4.8 [OPEN_QUESTION] found@1 数值不一致：p.5 报 BFCL BM25 found@1=60.0%、embed=73.2%；p.8 称 "The embedding scorer's higher found@1 on this split (77% vs 65%)"。65 vs 60、77 vs 73.2 的差异未在文中解释（可能是不同 split 或不同 seed 聚合），原文无法裁决。

4.9 [OPEN_QUESTION] Claude Sonnet 4.6 的确切 prompt 模板、强制单选的实现方式（工具调用 API 还是文本约束）未给出；无法排除 prompt 格式与呈现方式交互带来的次级效应（作者仅声明描述与排序一致）。

## Q5. 作者明示限制、负向结果和未测试边界是什么？

5.1 [AUTHOR_FACT] 明示负向结果：MetaTool+BM25（found@1 仅 33%）下 BoR agent 扩到 K=80.7、近乎全量展示，found 96.2% 但仅 1.04 bits 选择性；作者称 "This is a negative result, but an informative one"——scorer 无判别力时没有可靠停止信号。定位：（p.6–7，Sec.4.2，"the BoR agent expands to K=80.7"）。

5.2 [AUTHOR_FACT] 明示总限制（Sec.5.3）：RL agent 是小型 DQN/tabular Q-learning 而非生产级策略；MetaTool 结果为单 seed（覆盖六个条件），BFCL 与 ToolBench 有 3-seed 标准差；very hard 查询上的恢复仍然有限（ToolBench 0.2%）。定位：（p.9，Sec.5.3，"MetaTool results are reported from single-seed runs"）。

5.3 [AUTHOR_FACT] 明示范围边界：评估目标是"正确工具是否出现在呈现集中"；下游工具选择只在 BFCL 上验证；"LLM 是否用正确参数调用工具"（执行正确性）超出范围。定位：（p.9，Sec.5.3 末，"outside the scope of this work"；p.2，Scope 段）。

5.4 [AUTHOR_FACT] 明示的基准适配限制：所用基准均非为深度评估设计；BFCL 的精编函数定义使多数查询对 embedding scorer 过易，ToolBench 的噪声聚合描述才产生较宽难度谱；均无"该看几个工具"的原生 ground truth，作者呼吁构建受控难度分布的专用基准。定位：（p.9，Sec.5.2，"None of the benchmarks we use were designed to evaluate search depth"）。

5.5 [AUTHOR_FACT] 结论中的自认权衡：BoR 优化选择性而非最大召回，因此当统一深度恰好足够时 Fixed-K 可取得更高聚合覆盖（如 FK=5 64.7% vs BoR 61.9% 于 ToolBench；FK=5 97.5% vs 85.0% 于 BFCL+embed）。定位：（p.9，Sec.6，"BoR optimizes selectivity rather than maximum recall"）。

5.6 [READER_INTERPRETATION] 未测试边界（作者未明示但可从设置推出）：(a) 多相关工具（Rq>1）的工具选择场景仅在文档检索附录（NFCorpus Rq=1–475）间接触及，工具域全部 Rq=1；(b) 多轮/带执行历史的工具选择未测；(c) 下游验证仅测 Claude Sonnet 4.6 一个 LLM、仅在 BFCL 上；(d) 工具域候选集最大 N=370（全 registry），3,251 全库仅通过 N=50 构造集间接评估。

## Q6. 哪些内容可抽取为 Operator，哪些是真实可记录的 Failure？

可抽取 Operator（均为论文明确操作，可复用）：

6.1 [AUTHOR_FACT] Operator：chance-corrected 深度评估——对任意 (N, K, Rq) 用超几何 Prand（Rq=1 时 Prand=K/N），报告 BoR = log2(Pobs/Prand) 而非裸 Success@K。定位：（p.4，Sec.3.1，Eq.(1)(2)）。

6.2 [AUTHOR_FACT] Operator：以 −log2(Prand(kstop)) 作为停止时的终端奖励，即得"自剪枝"深度策略——深度惩罚由指标结构内生（K 增大 → Prand 上升 → 奖励下降），无需手工深度惩罚项（仅留小常数 step cost）。定位：（p.5，Sec.3.3，"not an engineered penalty but a mathematical consequence"）。

6.3 [AUTHOR_FACT] Operator：BoR ceiling 自校准——BoRopt(K)=log2(N/K) 仅依赖语料规模与深度，可作跨系统可达选择性上界与"还值不值得继续加深"的诊断。定位：（p.4，Sec.3.1，"BoRopt(K) = log2(N/K)"）。

6.4 [AUTHOR_FACT] Operator：doubling rule——Pobs 平台期后每翻倍 K 约损失 1 bit 选择性；Pobs>0.5 后无法在加深的同时保持选择性。定位：（p.4，Sec.3.1，"doubling K costs approximately 1 bit"）。

6.5 [AUTHOR_FACT] Operator：按 gold 工具在 scorer 排名的位置分难度桶（1st / 2nd–5th / 6th–20th / 21+；小候选集用 1st / 2nd–3rd / 4th–10th / 11+）做深度评估，暴露聚合指标掩盖的分布性失败。定位：（p.5，Sec.4，"We group test queries into difficulty buckets"；p.6，"we use narrower buckets"）。

6.6 [AUTHOR_FACT] Operator：三问诊断分解——"正确工具是否被呈现 / LLM 是否选中 / 执行是否成功"分离测量（本文测前两问；Table 1 的 Presented% × Choice Acc% = End-to-End% 即该分解的操作化）。定位：（p.2，"Was the right tool presented? Did the LLM choose it?"；p.8，Table 1 表头）。

6.7 [READER_INTERPRETATION] Operator（评审性）：用"指标能否当奖励且不需逐条件调参"作为指标质量探针——同一奖励在九个条件产出 K=1.4 到 80.7 的不同策略，本身是指标自适应性的证据（p.8–9，Sec.5.1，"No tuning was changed between conditions"）。

真实可记录 Failure（论文内有数据支撑）：

6.8 [AUTHOR_FACT] Failure：弱 scorer 下自适应深度崩溃——BM25 found@1=33% 时 BoR agent 学到 K=80.7（近全量展示），选择性仅 1.04 bits；无判别性分数即无停止信号。定位：（p.6–7，Sec.4.2；p.7，Figure 2）。

6.9 [AUTHOR_FACT] Failure：固定深度在难查询上系统性归零——ToolBench 上 gold 排 6th–20th（n=76）时 FK=5、FK=1、F1 ablation 全部 found 0%，BoR 16.7±4.3%；gold 排 21+（n=136）时除 BoR 的 0.2% 外全为 0。定位：（p.6，ToolBench 分桶段；p.7，Figure 1）。

6.10 [AUTHOR_FACT] Failure：over-presentation 降低下游选择准确率——gold 在列表内时 Claude 在 FK=5 下选对 87.1%，在 BoR(K=2.2) 下 93.1%；medium 桶（n=23）60.9% vs 76.8±2.5%；embedding scorer 复现差距更宽（84.6% vs 96.1±2.0%，medium 50.0% vs 80.1%）。定位：（p.8，Table 1 及正文）。

6.11 [AUTHOR_FACT] Failure：聚合覆盖率掩盖分布性失败——FK=5 聚合 64.7% 高于 BoR 61.9%，但其构成是"easy/medium 全收、hard 及以上全空"；单看聚合数会选错方法。定位：（p.6，"This reflects its uniform depth"）。

6.12 [AUTHOR_FACT] Failure：与查询无关的固定深度惩罚（F1 型奖励）训练出的策略一致过浅且不随难度加深（各桶 K≈1.5），ToolBench 聚合仅 47.6±1.3%，几乎不优于 FK=1 的 45.3%；SciFact 上 F1 策略 K std=0.00，完全无自适应。定位：（p.6；p.9，Table 2 末行；p.12，Appendix A SciFact 段）。

6.13 [READER_INTERPRETATION] 溯源提示（抽取 Operator 时的归属）：BoR 指标本身出自引文 [30]（Repantis et al., ICLR Blogposts 2026，作者与本文高度重叠），本文首句即声明 "BoR was introduced as a chance-corrected selectivity metric in Repantis et al. [30]"（p.4，Sec.3.1）。故 6.1/6.3/6.4 的原始出处应指向 [30]，本文的新贡献是把它用于工具选择评估并 RL 化（6.2、6.5–6.7）。

## Q7. 每项判断对应哪个物理页码、章节、图表和短逐字定位语？

7.1 [READER_INTERPRETATION] 本报告采用逐条内嵌定位（各条目末尾括号），此处汇总关键锚点：
- p.1：标题/作者/摘要/arXiv 水印（"arXiv:2605.24660v2 [cs.IR] 7 Jun 2026"）
- p.2：Scope 段（"execution correctness is out of scope"）
- p.4：Sec.3.1 Eq.(1)(2)、BoRopt、doubling rule；Sec.3.2 State
- p.5：Reward 段（oracle Rq、step_cost/γ 例外）、Sec.3.3 Baselines、脚注 1、Sec.4 难度桶定义、BFCL 两条件数值
- p.6：MetaTool 三组实验、ToolBench 主结果与分桶（n=272/116/76/136）、脚注 2（G1 单工具查询、3,251 tools）
- p.7：Figure 1（ToolBench 分桶）、Figure 2（scorer 消融）、Sec.4.2 负向结果
- p.8：Table 1（下游验证）、Sec.4.3 全部下游数值、Sec.5.1
- p.9：Table 2（九条件汇总）、Sec.5.2/5.3 限制、Sec.6 结论
- p.10–12：参考文献；p.12 Appendix A（SciFact/NFCorpus/MS MARCO，含 "N=8,841,823"）
- p.13：Table 3（文档检索验证数值）

## Q8. 解析文本与可视 PDF 是否冲突（就抽查过的页面回答）？

8.1 [AUTHOR_FACT] 我对 p.1、p.5、p.7、p.8、p.9、p.13 做了 150dpi 渲染视觉抽查，逐项核对：
- p.8 Table 1 四行数值（BoR 76.9±0.4 / 93.1±0.5 / 71.7±0.0 / 2.2±0.4；F1 72.8±2.7 / 94.3±1.7 / 68.6±1.7 / 1.7±0.3；FK=5 84.2 / 87.1 / 73.3 / 5.0；FK=1 65.0 / 100.0 / 65.0 / 1.0）与解析文本完全一致。
- p.9 Table 2 九行（含 BFCL+BM25 90.3±2.4 / 90.8 (FK=50) / 7.4±2.5；ToolBench 61.9±0.6 / 77.3 (FK=20) / 4.4±0.4）与解析文本完全一致。
- p.13 Table 3 三行（SciFact 78.9 / 85.6 (FK=50) / 9.76；NFCorpus 71.1 / 69.1 (FK=50) / 4.90；MS MARCO 82.7 / 80.7 (FK=50) / 20.28）与解析文本完全一致。
- p.7 Figure 1 右图显示 FK=5 在 easy/medium 桶 100%、hard/very hard 桶 0；BoR medium≈74%、hard≈17%，与正文数值一致；Figure 2 柱标（80.7/2.3/2.4；1.04/4.44/4.24）与正文一致。
- p.1、p.5 正文与脚注渲染与解析文本一致。

8.2 [READER_INTERPRETATION] 结论：抽查范围内未发现解析文本与可视 PDF 冲突；解析文本中表格被线性化（数值逐格展开为独立行），但数值无损。未视觉抽查的页面（p.2–4、p.6、p.10–12）经文本层交叉引用核对（p.6 数值与 p.7 图、p.9 表一致），冲突风险低。

8.3 [OPEN_QUESTION] 唯一悬置的数值问题是 4.8 所记 found@1 口径差异（p.5 的 60.0%/73.2% vs p.8 的 65%/77%）；这是文内两处正文之间的差异，而非解析与视觉之间的冲突。

---

## 附：核心数值速查（全部 [AUTHOR_FACT]，逐字出处见 p.9 Table 2 / p.8 Table 1 / p.13 Table 3）

| 条件 | BoR Found% | F1 Found% | Best FK | BoR K | F1 K |
|---|---|---|---|---|---|
| BFCL+BM25 (N=370) | 90.3±2.4 | 88.9±1.4 | 90.8 (FK=50) | 7.4±2.5 | 6.4±1.9 |
| BFCL+embed (N=370) | 85.0±3.0 | 85.8±1.4 | 97.5 (FK=5) | 1.4±0.1 | 1.6±0.1 |
| MetaTool+BM25 (N=100) | 96.2 | 82.8 | 83.7 (FK=50) | 80.7 | 57.2 |
| MetaTool+embed (N=100) | 73.3 | 69.0 | 74.7 (FK=3) | 2.3 | 3.0 |
| MetaTool+BGE (N=100) | 71.4 | 61.4 | 57.2 (FK=1) | 2.4 | 1.2 |
| MetaTool (N=20) | 70.6 | 63.3 | 59.2 (FK=1) | 1.6 | 1.3 |
| MetaTool (N=50) | 74.7 | 63.9 | 59.2 (FK=1) | 2.6 | 1.2 |
| MetaTool (N=100) | 72.8 | 63.3 | 59.2 (FK=1) | 2.1 | 1.5 |
| ToolBench (N=50) | 61.9±0.6 | 47.6±1.3 | 77.3 (FK=20) | 4.4±0.4 | 1.5±0.3 |

下游验证（p.8 Table 1，BFCL，Claude Sonnet 4.6）：BoR Presented 76.9±0.4 / Choice 93.1±0.5 / E2E 71.7±0.0 / K 2.2±0.4；F1 72.8±2.7 / 94.3±1.7 / 68.6±1.7 / 1.7±0.3；FK=5 84.2 / 87.1 / 73.3 / 5.0；FK=1 65.0 / 100.0 / 65.0 / 1.0。

文档检索验证（p.13 Table 3）：SciFact (N=5,183) BoR 78.9 / K=7.2 / 9.76 bits；NFCorpus (N=3,633) 71.1 / 22.9 / 4.90；MS MARCO (N=8.8M) 82.7 / 24.0 / 20.28。

（完）
