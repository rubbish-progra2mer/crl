# P093 独立二读报告（fresh reader, W06 扩充波次）

## 0. 校验头

- 读者：r2-20260727-p093-a1（独立二读，未接触 read_1.md、任何 Card、reconciliation 或其他读者材料）
- 日期：2026-07-27
- 文件：D:\Desktop\crl\crl_agent_v3\knowledge_base\staging\w06_targeted\P093_dense_retriever_collapse.pdf
- 实测 SHA-256：e62a61bf3e0bfbfcbd08f9fe09cdb29079f9e87035c32b3ee7eee89df1630fb1（与任务给定值一致）
- 实测物理页数：17（PyMuPDF page_count）
- canonical metadata 核对：[AUTHOR_FACT] PDF 第 1 页左侧竖排水印 "arXiv:2503.05037v2 [cs.CL] 2 Jun 2025"；标题 "Collapse of Dense Retrievers: Short, Early, and Literal Biases Outranking Factual Evidence"；作者 Mohsen Fayyaz, Ali Modarressi, Hinrich Schütze, Nanyun Peng（UCLA / LMU Munich / MCML）。与 canonical（arXiv 2503.05037v2, 2025-06-02）一致。[READER_INTERPRETATION] PDF 本体未出现 "ACL 2025" 字样，会议归属无法从本文件内证实，只能靠外部元数据。
- 抽查方式：全部 17 页 PyMuPDF 文本抽取；对 p.1（Figure 1）、p.3（Table 2）、p.6（Table 3）、p.8（Table 4/5）、p.16（Table A.6/A.7/A.8/A.9）做了 150–300 dpi 渲染视觉核对。

## 1. 方法究竟改变哪一步计算？

1.1 [READER_INTERPRETATION] 这是一篇分析/基准论文，不提出新模型，也不改动检索器任何一步前向计算。它改变的是"评测输入的构造"：从 Re-DocRED 关系抽取标注出发，受控地合成文档对 (D1, D2)，然后比较冻结检索器的打分 M(Q,D1) 与 M(Q,D2)，用配对 t 检验量化偏差。干预全部发生在数据构造层，模型侧零改动。

1.2 [AUTHOR_FACT] 构造框架：p.3, §3.1，"we take a novel approach by repurposing a relation extraction dataset"；每个关系映射到查询模板（p.3："we map each relation to a query template (Templates are in Table A.5)"，模板全表在 p.15 Table A.5）；证据句 Sev 须同时含 head 与 tail 实体，并引入记号 S+h−t（含 head 不含 tail）与 S−h−t（两者皆无）（p.3，"We also introduce the notation..."）。每个分析设定 250 条查询（p.3："for each of our six analysis settings, we compile 250 queries"）。

1.3 [AUTHOR_FACT] 唯一"改计算"的部件是分析工具 DecompX：p.4, §3.2，"Instead of using the original embeddings, we compute the similarity score via a dot product of the decomposed vectors"——仅用于可视化 token 级贡献（Figure 2, p.4；Figures A.7–A.9, p.17），不参与任何主实验统计。

1.4 [AUTHOR_FACT] 统计量定义：p.5, Eq.(2)，t = 平均差 / 标准误；"A positive t-statistic indicates higher scores for D1"。脚注 3：SciPy ttest_rel；p.1 脚注 2："p < .05 ⇒ |t| ≥ 1.97, df = 249"。

## 2. 输入、输出、可用信息与干预时点

2.1 [AUTHOR_FACT] 输入：由 Wikidata 关系模板生成的自然语言查询（Table A.5, p.15，共 51 个关系模板，如 P190 → "What is the sister city of <head_entity>?"）；以及由 Re-DocRED 句子拼装的合成文档。数据来自 Re-DocRED 的 test+validation 集（p.3）。

2.2 [AUTHOR_FACT] 输出：三类。(a) 检索器相似度分数（点积）；(b) 配对 t 统计量与 accuracy（"proportion of 250 example pairs where M(Q,D2) > M(Q,D1)"，Table 4 caption, p.8）；(c) RAG 准确率（Table 5, p.8，GPT-4o 判分，prompts 在 Table A.7, p.16）。

2.3 [AUTHOR_FACT] 每种偏差的文档对构造（干预时点全部在文档构造，检索器与查询固定）：
- Answer Importance：D1 = Sev + 中性句；D2 = S+h−t + 中性句；两关键句都放开头以排除位置效应（p.4–5, Eq.(1)，"We strategically positioned the key sentences at the beginning of both documents"）。
- Position Bias：证据句移到第 1..10 位对比第 1 位（p.5–6, Eq.(3), Figure 4）；另有首 vs 末版本（p.13, §A.3, Eq.(8), Figure A.2）。
- Literal Bias：head 实体替换为最短/最长别名的 Q/D 组合（p.6, §3.3.3, Table 3；全模型在 Table A.8, p.16）。
- Brevity Bias：D1 = 仅证据句；D2 = 证据句 + 原文其余（p.6, Eq.(4)）。
- Repetition Bias：D1 = Sev + 2×S+h−t；D2 = Sev + 2×S−h−t（p.7, Eq.(5), Figure A.3, p.13）；另有分箱分析（Figure 5, p.7；Figure A.5/A.6, p.14）。
- Foil 组合：D1 = 2×h + S+h−t（无答案、堆偏差）；D2 = 4×~S−h−t + Sev + 4×~S−h−t（~S 来自无关文档，脚注 8，p.8, Eq.(6)）。
- Poison：在 foil 上追加 GPT-4o 生成的错误 tail 句（p.8, Eq.(7)；poisoning prompt 在 Table A.7, p.16）。

2.4 [AUTHOR_FACT] RAG 实验干预时点：把不同版本文档（Poison/Foil/No/Evidence）直接放进 GPT-4o 的 RAG prompt（p.8, §3.5；Table A.7）。[READER_INTERPRETATION] RAG 段没有真实检索循环——检索器偏好由 Table 4/A.9 单独证明，Table 5 只测"若该文档被送入 LLM 会怎样"，二者拼接构成攻击叙事。

## 3. 最强基线与最接近组合基线

3.1 [READER_INTERPRETATION] 本文没有"提出方法 vs 基线"的结构；被评对象即六个稠密检索器 + 两个补充模型。"最强基线"应理解为被测模型中最强者。

3.2 [AUTHOR_FACT] NQ 下游性能（Table 2, p.3，corpus 2,681,468）：Dragon RoBERTa nDCG@10 0.55 / Recall@10 0.75 最高，Dragon+ 0.54/0.74 次之；无监督 Contriever 最弱（0.25/0.41）。自建 redocred 检索集（Table A.3, p.12，7170 queries / 105,925 corpus）上 Dragon+ 0.55 反超 Dragon RoBERTa 0.53。

3.3 [AUTHOR_FACT] Foil 组合测试加测两种更强/更贵架构：ColBERT (v2) 7.6% 与 ReasonIR-8B 8.0%（Table 4, p.8；§A.1, p.12，"these models still fail on the Foil dataset, with under 9% correct document preferences"）。[READER_INTERPRETATION] 这两者是"最接近的组合基线"——late-interaction 与 8B 推理型检索器代表更高容量替代方案，仍崩溃，支撑结论的普适性。

3.4 [AUTHOR_FACT] RAG 侧对照条件即其自身基线：No Doc（gpt-4o-mini 52.0%，gpt-4o 64.8%）与 Evidence Doc（88.0%/93.6%）夹住 Foil（44.0%/62.8%）与 Poison（32.0%/30.8%）（Table 5, p.8）。摘要 "34% performance drop"（p.1）与 gpt-4o 的 64.8→30.8 一致（34.0 个百分点）。

3.5 [OPEN_QUESTION] 未与稀疏基线（BM25）在同一偏差电池上对比；BM25 仅在引言作为背景提及（p.1）。偏差是否为"稠密"特有，本文件内无法回答。

## 4. 结果是否可能来自模型、token、tool-call、prompt 或 oracle 差异？

4.1 [READER_INTERPRETATION] 核心设计（同一查询、同一模型下的配对文档差分）天然消除模型间与 prompt 差异；每对 D1/D2 只操纵单一因素，作者对混杂有明确防护：答案重要性测试固定关键句位置（p.5）；位置测试确保其余内容无 head/证据（p.6，"the evidence's position was the sole factor under evaluation"）；literal 测试刻意回避 long-long 组合以防重复混杂（脚注 7, p.6）；repetition 分箱把长度与重复次数分开（p.7）。主要结论受 token 级混杂影响的风险较低。

4.2 [READER_INTERPRETATION] 残余风险：(a) Brevity 测试中 D1/D2 的 token 数本身就是操纵变量，"brevity bias"与池化稀释（作者自己给的 "pollution effect" 解释，p.7）不可区分——这是解释层面而非事实层面的问题。(b) 查询是模板生成的合成查询，风格单一，t 值的绝对大小可能不外推到自然查询。(c) Foil D1 极短而 D2 含 8 句无关内容，foil 测试同时利用 brevity+repetition+literal，本就设计为多偏差叠加，不能归因于单一机制。

4.3 [AUTHOR_FACT] oracle/judge 风险点：poison 句由 GPT-4o 生成、RAG 答案由 GPT-4o 生成、评分也由 GPT-4o 判 YES/NO（p.8 脚注 10 "Evaluated using GPT-4o. Prompts in Table A.7"；Table A.7, p.16）。作者在 Limitations 承认 "it is not infallible and may introduce some variance"（p.9）。[READER_INTERPRETATION] 同一模型既当生成器又当裁判，Table 5 的绝对数字有 judge 偏置风险，但四条件相对排序（Evidence > No Doc ≳ Foil > Poison）对 judge 噪声相对稳健。

4.4 [AUTHOR_FACT] 模型版本已钉死：gpt-4o-mini-2024-07-18、gpt-4o-2024-08-06、各检索器 HuggingFace ID 见 Table A.2（p.12）。[READER_INTERPRETATION] 无 tool-call 环节，不存在工具差异问题。

4.5 [READER_INTERPRETATION] 我发现一处内部数字不一致（详见 §8.3）：Table 3（p.6）与 Table A.8/Figure A.1（p.16/p.13）在同一设定下数值有 0.01–0.05 级别的偏差（如 +14.37 vs 14.32）。量级不影响结论，但说明两表可能来自不同运行或不同舍入管线。

## 5. 作者明示限制、负向结果和未测试边界

5.1 [AUTHOR_FACT] 明示限制（p.9 Limitations）：(a) 依赖 Re-DocRED 标注质量，"may still contain imperfections that introduce minor noise"；(b) GPT-4o 评测有方差，"Nevertheless, we believe the observed trends and findings remain valid"。

5.2 [AUTHOR_FACT] 论文内的负向/反直觉结果：(a) 无监督 Contriever 在 Answer Importance 上 t = −5.92（Figure 3, p.5），即它反而偏好无答案文档；(b) 所有模型 foil accuracy < 10%（Table 4, p.8）；(c) poison 文档使 RAG 低于完全不给文档（Table 5, p.8）；(d) 更强的 ColBERT/ReasonIR-8B 也失败（§A.1, p.12）。

5.3 [AUTHOR_FACT] 范围声明：§A.1（p.12）"Our study focuses on dense retrievers that generate a single embedding per document"；ColBERT/ReasonIR 只测了 foil 设定，未跑五项单偏差电池（Figure 1 图例含 ColBERT，但 Figure 3/4、A.1–A.4 的模型列表均无 ColBERT/ReasonIR）。

5.4 [READER_INTERPRETATION] 作者未明说的未测试边界：无缓解/训练侧对策实验；无真实全库检索下的攻击端到端验证（Table 4/A.9 是成对比较而非 top-k 检索，p.8 也只说 "can potentially cause the model to select all top-k documents"——"potentially" 表明未实测）；仅英文维基百科语料；仅单跳关系型查询；重排器（cross-encoder rerank）是否能挽救未测。

## 6. 可抽取 Operator 与真实 Failure

6.1 可抽取为 Operator（均 [READER_INTERPRETATION]，来源页码见括号）：
- OP-1 关系数据集改造检索评测：用 (head, relation, tail)+证据句标注反向合成可控查询-文档对（§3.1, p.3；模板表 p.15）。
- OP-2 配对差分 + 配对 t 检验协议：固定 n=250、df=249、以 t 值横向比较不同偏差强度（Eq.(2), p.5；Figure 1, p.1）。
- OP-3 单因素文档对构造配方：Eq.(1)(3)(4)(5)(8) 的五种模板（p.4–7, p.13）。
- OP-4 Foil/Poison 对抗文档配方：Eq.(6)(7)（p.8）+ GPT-4o poisoning prompt（Table A.7, p.16）——可复用为 RAG 红队工具。
- OP-5 DecompX 用于检索打分的 token 级归因（§3.2, p.4；Figure 2, p.4）。
- OP-6 长度×重复二维分箱以解耦相关混杂（Figure 5, p.7；A.5/A.6, p.14）。

6.2 真实可记录 Failure（均 [AUTHOR_FACT]，指被测系统的失败）：
- F-1 五种系统性偏差：brevity（Fig A.4, p.13，t 9.46–20.51）、position（Fig 4, p.5；Fig A.2, p.13，t 3.86–18.83）、literal（Table 3, p.6；A.8, p.16）、repetition（Fig A.3, p.13，t 5.56–8.05）、answer importance 偏弱（Fig 3, p.5）。
- F-2 组合偏差崩溃：全部 8 个模型 foil accuracy 0.4%–8.0%，t 统计 −20.96 至 −42.25，p<0.01（Table 4, p.8；重复为 Table A.1, p.12，数值一致）。
- F-3 Poison 完胜证据文档：五个微调模型 accuracy 0.0%、Contriever 1.2%（Table A.9, p.16）。
- F-4 RAG 中毒：poison 文档使 gpt-4o 从 no-doc 64.8% 跌至 30.8%（Table 5, p.8）。
- F-5 无监督 Contriever 答案识别为负（t=−5.92，Fig 3, p.5）。
- F-6 辅助观察：60 例错误标注中 Long Document 55%、Missing Answer 32%（Table A.4, p.13，preliminary annotation）。

## 7. 判断-定位对照表（物理页码 / 章节 / 图表 / 逐字定位语）

| # | 判断 | 物理页 | 章节/图表 | 逐字定位语 |
|---|------|--------|-----------|------------|
| 1 | 250 对/设定，六个设定 | 3 | §3.1 | "we compile 250 queries" |
| 2 | t 检验定义与工具 | 5 | §3.3.1, Eq.(2), fn.3 | "Using ttest_rel function of SciPy" |
| 3 | 显著性阈值 | 1 | fn.2 | "p < .05 ⇒ \|t\| ≥ 1.97, df = 249" |
| 4 | NQ 性能 | 3 | Table 2 | "2,681,468 corpus size" |
| 5 | Contriever 负 t | 5 | Figure 3 | "-5.92" |
| 6 | 位置偏差 | 5–6 | §3.3.2, Figure 4, Eq.(3) | "confirm a strong bias favoring content at document beginnings" |
| 7 | literal 偏差主表 | 6 | §3.3.3, Table 3 | "+14.37 and +16.62 in Table 3" |
| 8 | brevity 机制解释 | 7 | §3.3.4/3.3.5 交界 | "pollution effect" |
| 9 | repetition 分箱 | 7 | Figure 5 | "increases with head entity repetitions but decreases with document length" |
| 10 | foil 构造 | 8 | §3.4, Eq.(6) | "two repeated mentions of the head entity in the opening sentence" |
| 11 | foil 全线崩溃 | 8 | Table 4 | "accuracy dropping below 10%" |
| 12 | poison 构造 | 8 | §3.5, Eq.(7) | "replacing the tail entity with a contextually plausible but entirely incorrect entity" |
| 13 | RAG 四条件 | 8 | Table 5 | "worse performance than providing no document" |
| 14 | poison 100% 被偏好（脚注） | 8 | fn.9 | "in 100% of cases (Table A.9)" |
| 15 | 限制声明 | 9 | Limitations | "may introduce some variance in the RAG results" |
| 16 | 附加模型范围 | 12 | §A.1 | "with under 9% correct document preferences" |
| 17 | 模型 ID | 12 | Table A.2 | "gpt-4o-2024-08-06" |
| 18 | 首末位置版 | 13 | §A.3, Eq.(8), Fig A.2 | "First vs. Last" |
| 19 | 错误标注分布 | 13 | Table A.4 | "60 retrieval errors based on DecompX" |
| 20 | poison 成对结果 | 16 | Table A.9 | "less than 2% accuracy" |
| 21 | prompts | 16 | Table A.7 | "Only give me the complete answer" |
| 22 | 数据集发布 | 1 | fn.1 | "huggingface.co/datasets/mohsenfayyaz/ColDeR" |

## 8. 解析文本与可视 PDF 是否冲突（就我抽查过的页面）

8.1 [READER_INTERPRETATION] p.3（Table 2）、p.6（Table 3）、p.8（Table 4/5）、p.16（Table A.6–A.9）：文本抽取的数值与 300 dpi 渲染视觉核对完全一致，仅表格线性化导致的列序拼接差异，无数值冲突。p.1 Figure 1 实为五轴雷达图（视觉），文本抽取只给出轴标签与模型图例，无法从文本恢复各模型雷达值——非冲突，但提醒 Figure 1 的具体读数不可从解析文本引用。

8.2 [READER_INTERPRETATION] p.13–14 的图（A.1–A.6）数值以纯文本形式完整嵌入抽取结果（如 Fig A.1: 13.31–17.18），与图注对应关系需靠渲染确认；我对 p.13 未做像素级核对，引用时以模型名-数值配对的文本序为准，风险低。

8.3 [READER_INTERPRETATION] 发现一处 PDF 内部（非抽取）不一致，文本与视觉两路均确认：Table 3（p.6）与 Table A.8（p.16）同设定数值不完全相等——long-long/long-short Dragon+ +21.04 vs 21.03；long-long/short-long Contriever-MSMARCO +22.04 vs 22.01；short-short/long-short +4.62/+9.04 vs 4.65/9.05；short-short/short-long +14.37/+16.62 vs 14.32/16.58。正文 p.6 引用的 "+14.37 and +16.62" 与 Figure A.1（p.13，14.32/16.58）也随之不符。差异 ≤0.05，不影响任何结论方向。[OPEN_QUESTION] 差异来源（不同运行/舍入/版本残留）本文件内无法判定。

8.4 [READER_INTERPRETATION] 第二处内部小瑕疵：p.8 脚注 9 与 Table 5 caption 称 poison 文档被检索器偏好 "100% of the time"，但 Table A.9（p.16）显示 Contriever accuracy 1.2%（即 98.8% 偏好）。对五个微调模型 0.0% 而言 "100%" 成立；对全体模型是轻微夸张。[OPEN_QUESTION] "100%" 是否有意仅指微调模型，原文未说明。

8.5 [AUTHOR_FACT] Table 4（p.8）与 Table A.1（p.12）为同一结果的重复呈现，八行数值逐一相同（文本抽取双向核对）。

## 9. 总体独立判断摘要

9.1 [READER_INTERPRETATION] 这是一篇构造严谨的诊断性论文：配对差分设计使单偏差结论内部效度高；foil/poison 结果幅度极大（accuracy < 10%、t 绝对值 20–55），远超 §8.3 那类 0.05 级数字瑕疵的影响。
9.2 [READER_INTERPRETATION] 外推的主要弱点：合成模板查询、成对比较而非真实 top-k 检索、GPT-4o 自生成自评分、无缓解实验。引用其 RAG 绝对数字时应连同这些条件一起引用。
9.3 [OPEN_QUESTION] BM25/重排器在同一电池上的表现、偏差在非英语语料的稳健性、以及 Table 3 与 A.8 的数值分歧来源，均需外部信息或作者代码库核验（fn.1 的 ColDeR 数据集与 leaderboard 未在本次读取范围内）。
