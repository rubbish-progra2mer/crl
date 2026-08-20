# P101 独立二读报告（fresh reader, attempt r2-20260727-p101-a1）

## 0. 报告头部：文件校验
- 实测 SHA-256: `50aa8da6bf61c37f4819f45a5db19cafba4721540d14bf97b4ab29a196265d1a`（与任务给定值一致）
- 实测物理页数: 16 页（PyMuPDF page_count）
- 文件: `D:\Desktop\crl\crl_agent_v3\knowledge_base\staging\w06_targeted\P101_distilled_test_suites.pdf`
- canonical metadata 核对: [AUTHOR_FACT] 论文标题 "Semantic Evaluation for Text-to-SQL with Distilled Test Suites"，作者 Ruiqi Zhong, Tao Yu, Dan Klein（UC Berkeley / Yale），物理第 1 页左侧竖排水印 "arXiv:2010.02840v1 [cs.CL] 6 Oct 2020"。与给定 canonical metadata（arXiv 2010.02840v1, EMNLP 2020）中的 arXiv 号与版本一致；PDF 内文未出现 "EMNLP 2020" 字样，该会议归属为外部元数据。[READER_INTERPRETATION] EMNLP 2020 归属无法仅凭 PDF 本身确认，但与 arXiv 时间点相容。

## 1. 方法究竟改变哪一步计算？
1.1 [AUTHOR_FACT] 该论文不改变任何模型的训练或推理计算，改变的是 Text-to-SQL 的**评测计算**：把"在单一数据库上比对执行结果"（single denotation）或"字符串/子句集合比对"（exact string match / exact set match, ESM）替换为"在一个蒸馏出的高代码覆盖率数据库测试套件上逐库比对执行 denotation"。定位：物理第 1 页 Abstract，"We propose test suite accuracy to approximate semantic accuracy for Text-to-SQL models"；物理第 3 页 Section 2，"We use the test suite S to evaluate a model-predicted query q: q is correct iff DS(g,q) = 0"。
1.2 [AUTHOR_FACT] 评测前的离线计算被改变/新增：对每条 gold 查询 g，(a) 自动生成邻居查询集合 Ng（每次只改 gold 的一个方面：整/浮点常数替换、字符串替换、比较运算符/列名替换、删 span），(b) 从随机数据库分布 Ig 采样约 1000 个数据库并贪心保留能区分尚未被区分邻居的数据库，得到蒸馏测试套件 Sg。定位：物理第 3 页 Section 3.1（Figure 2）与 "we modify one of the following aspects of the gold query"；物理第 4 页 Section 4.2 "We initialize S g to be empty and proceed greedily"；物理第 13 页 Appendix A.1 Algorithm 1。
1.3 [READER_INTERPRETATION] 用 CRL 语言说：干预点在评测 pipeline 的"判分函数"，即把 metric 从语法近似换成用 fuzzing 预先蒸馏的多数据库执行语义近似；不涉及模型参数、解码或数据。

## 2. 输入、输出、可用信息与干预时点
2.1 [AUTHOR_FACT] 蒸馏阶段输入：gold SQL 查询 g 与其数据库 schema（表/列名、外键结构、列类型）；输出：测试套件 Sg（一组随机生成的数据库）。数据库按外键拓扑序生成，数值列在 [-2^63, 2^63] 均匀采样、字符串随机，并 "randomly add in constant values used in g (e.g., 34 and "Alice") and their close variants"。定位：物理第 4 页 Section 4.1 与 Figure 3。
2.2 [AUTHOR_FACT] 评测阶段输入：模型预测查询 q、gold g、套件 Sg；输出：二值判定（q 在所有 w∈Sg 上 denotation 与 g 相同则判对）。执行用 Sqlite3，不终止的执行定义为 ⊥（超时实现）。定位：物理第 2 页脚注 4，"we use Sqlite3 to obtain the denotation... implemented as timeout in practice"；物理第 3 页式 (2)(3)。
2.3 [AUTHOR_FACT] 可用信息约束（防泄漏设计）：测试套件构建**不使用**任何模型预测信息——"The first author obtained these model-predicted queries from the second author after producing the test suites to ensure that our method is general and not tailored to a specific family of model-predicted queries"。定位：物理第 5 页 Section 5.2。
2.4 [AUTHOR_FACT] 干预时点：蒸馏是一次性的离线预处理（Spider 1000 随机库、16 CPU 约一周，见物理第 5 页 Section 6.1 "takes around a week on 16 CPUs"）；此后每次评测只需在蒸馏套件上执行（Spider 全套 gold 单 CPU 75.3 分钟，物理第 7 页 Section 6.4）。
2.5 [AUTHOR_FACT] 为与 Spider 官方 metric 公平比较所做的适配（物理第 5 页 Section 5.3）：(1) 官方不查常数正确性→测试套件枚举把预测中常数替换为 gold 常数的所有方式，任一替换通过即判对；(2) 不查列序→denotation 仅列序不同视为等价；(3) 官方脚本 "accidentally ignores any join predicate"→作者修复此 bug；(4) 不查表变量名→保留该特性（会引入新的 false positive，如 Figure 8 行 1）。文中此后 "ESM" 与 "test suite accuracy" 均指适配后版本。

## 3. 最强基线与最接近组合基线
3.1 [AUTHOR_FACT] 被比较的基线 metric：(a) 官方 Spider exact set match（Official ESM）；(b) 适配后 ESM（Adapted）；(c) single denotation accuracy（只在 Yu et al. 2018 原始发布数据库上比对执行结果）。定位：物理第 8 页 Table 3 表头 "Adapted / Official / Single Denot." 及注文。
3.2 [AUTHOR_FACT] 与本方法最接近的"组合/消融"对照是**加速版**：只在从 Ig 采样的单个随机数据库上比对 denotation。作者报告 "retrospectively, it produces the exact same outcomes as running the full test suite on the 21 submissions"，但仍推荐完整套件，因为单样本不能区分所有邻居。定位：物理第 8 页 Section 6.4，"We may speed up the evaluation by checking denotation only on a single database sampled from the distribution Ig"。
3.3 [AUTHOR_FACT] 概念上的上界参照：无限计算下在大量随机数据库上做 fuzzing 比对（物理第 1-2 页 Introduction）；形式化验证工具（K-relations、UniNomial、U-semiring/Cosette）被作者作为不可行基线排除，理由是 "these representations cannot express sort operations and float comparisons"（物理第 1 页 Introduction）。
3.4 [READER_INTERPRETATION] 本文没有"模型基线"概念——21 个 Spider 提交是被评测对象而非对照组；metric 之间的对照即是本文的基线结构。最接近的组合基线（single database from Ig）恰好隔离了"随机生成的高覆盖数据库"与"多数据库套件"两个成分的贡献：前者已足以在这 21 个提交上复现全套件结论。

## 4. 结果是否可能来自模型、token、tool-call、prompt 或 oracle 差异？
4.1 [READER_INTERPRETATION] 本文是评测方法论文，不训练模型、无 LLM、无 prompt/token/tool-call 维度，故这些混淆源不适用。需要检查的替代混淆是 oracle/评判偏置，逐项如下。
4.2 [AUTHOR_FACT] 防"套件对预测过拟合"：套件先于取得模型预测生成（见 2.3，物理第 5 页 Section 5.2）。
4.3 [AUTHOR_FACT] 人工验证的方向性：100 条人工核验样本是从"ESM 判错但测试套件判对"的分歧集合中随机抽取的，结论是 "All of them are semantically equivalent to the gold query"，并公开这 100 条与注释理由（物理第 6 页 Section 6.1 及脚注 7）。[READER_INTERPRETATION] 这只验证了套件不产生 false positive 的一个方向（相对 ESM 分歧侧）；"测试套件判错但实际语义等价"（套件产生 false negative）的方向在 Spider 上未做对称的人工抽验——作者依赖第 8-9 页的论断 "test suite evaluation provably never creates false negatives in a strict programming language sense"（因为语义等价的查询在任何数据库上 denotation 必同）。该论断在严格 PL 意义下成立，但见 5.4 的 "broader sense" 限制。
4.4 [AUTHOR_FACT] 已承认的 oracle 缺口：WikiSQL 上 200K 条预测中发现 1 条测试套件判对但实际语义不等价（gold: SELECT MAX(col2) table WHERE col4 = 10; 预测多出 WHERE col2 > 10；"None of our sampled database leads to a gold denotation fewer or equal to 10"）。定位：物理第 14 页 Appendix A.3 Metric Difference。
4.5 [AUTHOR_FACT] "常数替换适配"本身会放松 metric：Figure 8 行 6（LIKE "UAL" vs = "UAL"）说明把 gold 常数插回预测后，本可能反映模型误解的 LIKE 用法被判对——"Inserting gold values into model-predicted queries as described in Section 5 might also unexpectedly loosen the semantic accuracy metric"（物理第 8 页 Section 7）。[READER_INTERPRETATION] 因此文中报告的 ESM false negative 率是在"适配后（较松）"的语义判定下测得的，若严格要求值预测正确，数值会不同。
4.6 [READER_INTERPRETATION] Table 1/2 的 "false positive/negative rate" 以测试套件准确率为 ground truth proxy（作者明言 "we use test suite accuracy as ground truth"，物理第 6 页 Section 6.2），故这些错误率数字继承了 4.3-4.5 的全部 oracle 假设，属于"以一个近似 oracle 度量另一 metric"的自举结构；作者用 100 例人工核验 + WikiSQL 1/200K 支撑该 proxy 的可信度。

## 5. 作者明示限制、负向结果和未测试边界
5.1 [AUTHOR_FACT] 浮点精度边界：fuzzing "has trouble distinguishing semantically close queries that differ only at a floating-point precision (e.g. "<= 2.31" vs. "< 2.31")"，但在后续人工评估中未发现由此造成的 false positive。定位：物理第 5-6 页 Section 6.1。
5.2 [AUTHOR_FACT] 不解决一般 SQL 等价性：套件覆盖的是 gold 的分支，"it might not cover all the branches of model-predicted queries. Adversarially, we can always construct a query that differs from the gold only under extreme cases and fools our metric"；且因 Goodhart 定律（原文拼作 "Goodhardt's law"），metric 被优化后需重新验证。定位：物理第 9 页 Section 8。
5.3 [AUTHOR_FACT] 已实证的失败样例（负向结果）：(a) WikiSQL 1/200K 判错（见 4.4）；(b) Figure 4 第 4 行：区分 "age < AVG(AGE)" vs "age <= AVG(AGE)" 需某行恰等于均值，"This happens with low probability and our test suite fails to distinguish them"（物理第 6 页 Figure 4）；(c) 约 1% 邻居无法被 1000 随机库区分（物理第 5 页，"1000 random databases can distinguish > 99% of the neighbor queries"）。
5.4 [AUTHOR_FACT] "broader sense" false negative：随机数据库可能违反 schema 未显式表达的常识约束（"A wins" vs "scoreA > scoreB" 例），生成 "unnatural" 数据库从而误判语义可接受的预测；建议未来数据集显式定义数据库生成过程。定位：物理第 9 页 Section 8 "Beyond Semantic Evaluation"。
5.5 [AUTHOR_FACT] 语用可接受但语义错误的答案（如多返回 age 列）不被本 metric 接受；建议收集多参考 gold。定位：物理第 9 页 Section 8。
5.6 [AUTHOR_FACT] 数据集级可靠性边界（Table 4，物理第 14 页）：两类难区分情形——gold 含大量 WHERE（ATIS 单查询最多 24 个 WHERE，Spider 最多 2）与 "WHERE COUNT(*) > 5000" 型谓词（需中间表恰为特定大小）；据此估计的可靠评测比例 Advising 仅 63.2%、ATIS 76.3%、Geography 88.2%，"Future manual efforts to hand-craft test suite might be needed... on ATIS and Advising"。定位：物理第 13 页 Appendix A.2 Reliability 与第 14 页 Table 4。
5.7 [AUTHOR_FACT] WikiSQL 上明确**不推荐**使用测试套件准确率："we do NOT recommend researchers to use test suite accuracy for WikiSQL"——因该数据集唯一等价变体是换 count 的列，出于可读性仍应检查列名。定位：物理第 15 页 Appendix A.3 末段。
5.8 [AUTHOR_FACT] 成本限制：套件 3.27GB（原始库 100.7MB）、全套执行 75.3 分钟 vs 1.2 分钟；蒸馏一次需 16 CPU 约一周。定位：物理第 7 页 Section 6.4、物理第 5 页 Section 6.1。
5.9 [READER_INTERPRETATION] 未测试边界：贪心蒸馏 "far from finding the optimal solution to Objective 4"（物理第 4 页 Section 4.2）但未与任何其他集合覆盖/优化算法比较；邻居生成的四类扰动的相对贡献没有消融；框架推广到 λ-DCS/知识图谱/Python 片段（物理第 8-9 页 Section 8）只是展望，未实验。

## 6. 可抽取的 Operator 与真实可记录的 Failure
6.1 Operator（机制来源标注为 AUTHOR_FACT，抽取归纳动作本身是 READER_INTERPRETATION）：
- 6.1a [AUTHOR_FACT 机制] **邻居查询覆盖度检验**：对参考程序施加单点扰动（常数±1/随机、字符串变体、运算符/列名替换、删 span）生成近邻错误程序集，用"测试集能否区分全部近邻"作为测试充分性/代码覆盖的可计算代理（物理第 3 页 Section 3.1、式 (4)）。[READER_INTERPRETATION] 可移植为任意可执行输出（SQL/代码/logical form）评测器的质量自检算子。
- 6.1b [AUTHOR_FACT 机制] **类型约束 fuzzing + 贪心蒸馏**：按 schema/类型/外键拓扑序采样随机输入，混入参考程序中出现的常数及其近变体提升覆盖，再贪心保留"新区分至少一个未区分近邻"的输入（物理第 4 页 Sections 4.1-4.2、第 13 页 Algorithm 1）。
- 6.1c [AUTHOR_FACT 机制] **oracle 先于预测生成**以避免评测器对被评对象过拟合（物理第 5 页 Section 5.2）。
- 6.1d [AUTHOR_FACT 机制] **分歧集合定向人工审计**：只人工核验新旧 metric 分歧的样本并公开注释（物理第 6 页 Section 6.1），以最小人工成本验证 metric 替换的方向正确性。
- 6.1e [AUTHOR_FACT 机制] **metric 错误的难度分层诊断**：按查询复杂度分层报告 FP/FN 与 Kendall τ，暴露"越难越失真"的趋势（物理第 6-8 页 Tables 1-3、Figures 6-7）。
- 6.1f [AUTHOR_FACT 机制] **单样本加速评测**：容忍偶发误差的场景（如 denotation-based training）可用 Ig 单库替代全套件（物理第 8 页 Section 6.4）。
6.2 Failure（论文中真实记录的失败，可作 Failure 卡）：
- 6.2a [AUTHOR_FACT] WikiSQL 1/200K：预测多出的 "WHERE col2 > 10" 子句未被套件覆盖而误判为对（物理第 14 页 A.3）。
- 6.2b [AUTHOR_FACT] "恰等于均值"类边界条件区分失败（物理第 6 页 Figure 4 行 4）。
- 6.2c [AUTHOR_FACT] 多 WHERE 叠加（ATIS 最多 24 个）与精确基数谓词（COUNT(*) > 5000）导致随机 fuzzing 区分概率过低，Advising 可靠比例仅 63.2%（物理第 13-14 页 A.2）。
- 6.2d [AUTHOR_FACT] 官方 Spider 脚本忽略 join predicate 的实现 bug；未修复时官方 metric 与测试套件准确率 Kendall τ 仅 40%（all data），extra 难度低至 20%（物理第 5 页 Section 5.3；第 8 页 Table 3）。
- 6.2e [AUTHOR_FACT] 适配 ESM 忽略表变量名会产生 false positive（物理第 5 页 Section 5.3 第 (4) 条；第 9 页 Figure 8 行 1）。
- 6.2f [AUTHOR_FACT] Figure 4 行 2 暴露一处 Spider 原始标注错误（"BETWEEN 160000 AND 90000" 区间颠倒导致恒空结果，"Original annotation is wrong"，物理第 6 页）。

## 7. 关键判断的物理页码/章节/图表/逐字定位（汇总）
- 7.1 核心主张与数字：物理第 1 页 Abstract，"a 2.5% false negative rate on average and 8.1% in the worst case"；"evaluate 21 models submitted to the Spider leader board"；"manually verify that our method is always correct on 100 examples"。
- 7.2 形式化与蕴含链：物理第 3 页 Section 2，"exact match => semantic accuracy => test suite accuracy => single denotation accuracy"；语义等价判定 "undecidable in general (Chu et al., 2017)"。
- 7.3 邻居生成：物理第 3 页 Section 3.1 与 Figure 2，"we only apply one modification at a time"（物理第 4 页顶部）。
- 7.4 采样与蒸馏：物理第 4 页 Section 4.1 Figure 3、Section 4.2；第 13 页 Algorithm 1（t = 1...1000）。
- 7.5 可靠性数字：物理第 5 页 Section 6.1，"on average 94 neighbor queries"、"takes around a week on 16 CPUs"、"1000 random databases can distinguish > 99%"、单库 "fails to distinguish 5% of the neighbor queries"（曲线约 600 库后停降）；第 6 页 Figure 5。
- 7.6 metric 误差：物理第 6 页 Table 1（all data FP/FN = 0.5/2.6，max 2.0/8.1；hard FN mean 4.4、max 12.1）；物理第 7 页 Table 2（single denotation FP all data mean 6.5、max 9.0；extra mean 11.0、max 17.6）。
- 7.7 相关性：物理第 7 页 Figure 6（τ=91.4% all / 74.1% hard）、Figure 7（97.9% all / 82.2% extrahard）；第 8 页 Table 3（Adapted 91 / Official 40 / Single 98，hard 行 75/28/94，extra 行 91/20/82）；第 15-16 页 Figures 9-11 分难度全集（如 Official medium 37.3%、hard 27.8%、extra 20.4%）。
- 7.8 效率：物理第 7 页 Section 6.4，"we distill 42 databases for each of the 1034 queries. In total, there are 695 databases"、"3.27GB"、"75.3 minutes"。
- 7.9 案例分析：物理第 9 页 Figure 8（行 1 FP：表变量名；行 2-4 FN：EXCEPT vs NOT IN、COUNT(*) vs COUNT(col)、ORDER BY...LIMIT 1 vs MAX；行 5/7 冗余 join；行 6 LIKE vs =）。
- 7.10 多数据集与 WikiSQL：物理第 14 页 Table 4（11 数据集统计）；A.3 "(8420 + 15878) x 8 ≈ 200K model-predicted queries"、8 个 WikiSQL 模型名单（MQAN unordered、X-SQL、HydraNet±EG、IncSQL、SQLova±EG、HardEM）。
- 7.11 引言里的排行榜误导论断：物理第 2 页 Section 1，"it undervalues a high-score submission with 61% semantic accuracy by 8%, but instead favors five other submissions with lower semantic accuracy"。

## 8. 解析文本与可视 PDF 是否冲突（就抽查页面）
8.1 [READER_INTERPRETATION] 我对物理第 1、6、7、8、14 页做了 140dpi 渲染的视觉抽查，与 PyMuPDF 抽取文本逐项比对：Table 1（第 6 页）、Table 2 与 Figures 6/7 的 τ 值（第 7 页）、Table 3（第 8 页）、Table 4 全 11 行数字（第 14 页）均一致；Figure 4 四行 SQL 与 Passing Reason、Figure 5 坐标轴说明一致。未发现抽取文本与可视渲染的冲突。抽取文本中表格数字有行序交织展平现象（如 Table 1 的 "0.5 / 2.2" 逐行铺开），但数值本身无损。
8.2 [OPEN_QUESTION] 论文内部数字不一致（非解析问题，文本与视觉两个通道显示相同）：Abstract 与 Section 1（物理第 1、2 页）称 ESM 平均 false negative 率为 "2.5%"，而 Section 6.2 正文（物理第 7 页 "a nontrivial false negative rate of 2.6% on average"）与 Table 1 all-data 行（0.5/2.6）为 2.6%。最大值 8.1% 两处一致。推测 2.5% 为旧稿数字或不同舍入，原文无法裁决。
8.3 [OPEN_QUESTION] 脚注 5 与脚注 7（物理第 5、6 页）中的 "available here" 在抽取文字层无 URL 实体（超链接目标不在文字层），仅第 2 页脚注 3 的 GitHub 仓库 https://github.com/ruiqi-zhong/TestSuiteEval 以明文出现；模型预测与 100 例人工注释的确切链接无法从 PDF 文字层核出。
8.4 [READER_INTERPRETATION] 另一处轻微体例问题：Appendix A.2 对 OrigSize 列的描述写 "in Giga-Bytes"（物理第 13 页），但 Table 4 中 Geography/Restaurants 行实际以 M（MB）计（0.26M、1.03M），属列说明与表格单位不完全一致，数值本身自洽。
