# P085 独立二读报告

## 1. 来源身份与阅读边界

- **AUTHOR_FACT**｜题名：*Retrieval Models Aren’t Tool-Savvy: Benchmarking Tool Retrieval for Large Language Models*。作者：Zhengliang Shi、Yuhan Wang、Lingyong Yan、Pengjie Ren、Shuaiqiang Wang、Dawei Yin、Zhaochun Ren；Zhaochun Ren 为通讯作者。单位分别为山东大学、百度、莱顿大学。（物理 PDF 第 1 页，标题与作者栏）
- **AUTHOR_FACT**｜出版信息：*Findings of the Association for Computational Linguistics: ACL 2025*，论文集页码 24497–24524，会议日期 2025-07-27 至 2025-08-01。（物理 PDF 第 1 页，页眉）
- **AUTHOR_FACT**｜本文提出评测集 `TOOLRET` 与训练集 `TOOLRET-train`，并报告一次 ToolBench 下游联动实验。（物理 PDF 第 1–2 页，Abstract、§1；第 8 页，§7）
- **AUDIT_JUDGMENT**｜本报告只以 SHA-256 为 `26ce2766e8c4b72e88dfd2cf93bfe56ff758fea6fe0ec0bea34228f555311d2a` 的 28 页指定 PDF 为论文事实来源；没有用项目中的首读、Cards、其他 attempt、reconciliation、Corpus Report、history/audit、retrieval calibration/blind、Candidate、Commissioning 或科研 Reviewer 资产补全结论。

## 2. 精确规模、构造与标签来源

### 2.1 TOOLRET 评测集

- **AUTHOR_FACT**｜精确总量为 **7,615 个 retrieval tasks** 与 **43,215 个 tools**。任务按工具文档形式分为：Web API 4,916、Code Function 950、Customized App 1,749；工具分别为 36,978、3,794、2,443。三个任务数与三个工具数各自都精确加总到总量。（物理 PDF 第 4 页，表 1，定位语 “Basic statistics of our benchmark TOOLRET”）
- **AUTHOR_FACT**｜平均 query / instruction 长度为 46.87 / 43.43 tokens，平均工具文档长度为 174.56 tokens；平均每个 query 有 2.17 个 target tools。query 与 target 文档的 ROUGE-L 重叠为 0.06，低于表 2 所列 NQ 0.31、MSMARCO 0.34、HotpotQA 0.11 与 MTEB 0.27。（物理 PDF 第 4 页，表 1、表 2，§4.1）
- **AUTHOR_FACT**｜作者称最终 corpus 合并自 **34 个数据集**；原始数据发布时间范围为 2023 年 8 月至 2024 年 12 月，下载自官方渠道，并执行去重与文本规范化。（物理 PDF 第 3 页，§3.1–§3.2，定位语 “merge all toolsets from the 34 datasets”）
- **AUTHOR_FACT**｜任务采样算子：先用 NV-Embed-v1 编码某数据集的任务，再做 K-means；cluster 数设为 `min(query 数, toolset 大小)`，每簇随机抽一个任务；若 toolset 大于 query 数则保留全部 query。（物理 PDF 第 3 页，§3.2 “Task sampling”）
- **AUTHOR_FACT**｜工具集采样/合并：人工检查原数据集文档，识别并合并相同或重叠工具集；文中举例 COLT 与 ToolBench 的交叠工具被合并；最终为每个工具分配唯一 ID。（物理 PDF 第 3 页，§3.2 “Toolset sampling”）
- **AUTHOR_FACT**｜每个 retrieval task 被统一成 query、instruction、target tools（labels）；target tools 来自原工具使用数据集为 query 标注的调用目标，而不是作者在合并后的 43,215 工具全集上重新做穷尽式相关性标注。（物理 PDF 第 3 页，§3.1；第 18 页，Appendix B.5 “Task format”）
- **AUDIT_JUDGMENT**｜因此，7,615 是采样后的 query/task 数，不是原始全部任务数；43,215 是跨来源合并去重后的候选工具数。标签的权威来源是各原始数据集的 target tools，不能解释为对合并语料中所有可行工具的穷尽判定。

### 2.2 target-aware instruction 的来源

- **AUTHOR_FACT**｜三位具有 NLP/IR 背景的专家先手写 100 条 seed instructions；GPT-4o 同时读取 query 与 target-tool descriptions，通过 in-context learning 为每个任务生成约 20 词的 instruction。生成项加入动态 instruction pool，后续样例从手写与已生成指令中随机抽取，随后做 heuristic filtering。（物理 PDF 第 4 页，§3.3；第 18–20 页，Algorithm 1 与 Appendix B.6）
- **AUTHOR_FACT**｜五位专家从四方面审查生成指令并修订低质量项，报告 Cohen/Fleiss 类别未明示、仅给出 Kappa 0.743。表 3 给出：与 query 相关 90.1%/9.9%；描述 target tool feature 92.3%/8.7%；完整覆盖全部 target features 89.2%/10.8%；存在 hallucination 5.9%/94.1%。正文称剩余 10.8% 不匹配项被人工修订。（物理 PDF 第 5 页，表 3、§4.3；第 20 页，Appendix B.7）
- **AUDIT_JUDGMENT**｜`w/ inst.` 不是自然用户只给 query 的设置：instruction 明确由 ground-truth target 文档生成，含有标签侧功能信息。它适合测试“给定目标感知指令时能否检索”，但不应与无标签辅助的开放世界检索混为一谈。
- **AUDIT_JUDGMENT**｜表 3 第二行的 92.3% 与 8.7% 合计为 101.0%，PDF 内部算术不一致；正文没有解释。表中质量率看起来是修订前审查结果，论文没有提供修订后的独立复测率。

## 3. 比较的检索器、重排器与评测协议

- **AUTHOR_FACT**｜§5.2 实际列出五类：
  1. sparse retrieval：BM25s；
  2. single-task dense retrieval：gtr-t5-base/large、contriever-msmarco、ColBERTv2.0，以及在工具检索数据上训练的 COLT；
  3. multi-task embedding：all-MiniLM-L6-v2、e5-small/base/large-v2、gte-base/large-en-v1.5、bge-base/large-en-v1.5，以及 gte-Qwen2-1.5B-instruct、e5-mistral-7b、GritLM-7B、NV-Embed-v1；
  4. cross-encoder reranking：mxbai-rerank-large-v1、MonoT5-base、bge-reranker-v2-m3、jina-reranker-v2-base、bge-reranker-v2-gemma；
  5. LLM agent reranking：RankGPT，backbone 为 Mixtral-8x22B、GPT-3.5-turbo-1106、GPT-3.5-turbo-0125。
  （物理 PDF 第 5–6 页，§5.2；第 23 页，Appendix D.1、表 9）
- **AUTHOR_FACT**｜表 4/5 各列出 26 个命名模型/配置行。重排器和 RankGPT 的初始候选工具均由 NV-Embed-v1 检索，因此其结果是 `NV first-stage retrieval + reranking`，不是在 43,215 工具上独立全排序。（物理 PDF 第 6–7 页，表 4、表 5；第 23 页，定位语 “initial tools … are retrieved by NV-embedd-v1”）
- **AUDIT_JUDGMENT**｜摘要称评测“six types of models”，§1 与 §5.2 则称/列出 five types；可验证的正文分类是上述五类，类型数量在 PDF 内部不一致。（物理 PDF 第 1 页 Abstract；第 2 页 §1；第 5–6 页 §5.2）
- **AUTHOR_FACT**｜指标为 NDCG@K、Recall@K、Precision@K 与 Completeness@K。Completeness@K 对单个 query 是二值量：仅当全部 target tools 都进入 top-K 时取 1，否则取 0。主要设置为 `w/o inst.`（只输入 query）与 `w/ inst.`（拼接 query 和 instruction）。（物理 PDF 第 5 页，§5.1）

## 4. 主要检索结果与范围差异

- **AUTHOR_FACT**｜在完整合并 corpus、`w/o inst.`、K=10 时，NV-Embed-v1 的平均 NDCG@10 / Completeness@10 为 **33.83 / 32.12**；BM25s 为 22.32 / 22.19。重排器中 bge-reranker-v2-gemma 为 35.51 / 34.14；MonoT5 对 NV 候选重排后平均 NDCG@10 为 28.92，低于 NV 的 33.83。（物理 PDF 第 6–7 页，表 4、§6.1）
- **AUTHOR_INTERPRETATION**｜作者据此认为常规 IR 强模型仍不擅长工具检索，并将原因归于 query–tool 词面重叠低，以及从常规 information-seeking 到 tool retrieval 的 domain/task shift。（物理 PDF 第 6 页，§6.1，定位语 “Existing retrievers struggle”）
- **AUTHOR_FACT**｜完整合并 corpus、`w/ inst.` 时，NV-Embed-v1 平均 NDCG@10 / Completeness@10 为 **42.71 / 43.41**；gte-Qwen2-1.5B-inst 为 45.96 / 45.39；bge-reranker-v2-gemma 达 47.52 / 48.90。BM25s 也从 22.32 / 22.19 上升到 36.46 / 39.03。（物理 PDF 第 7 页，表 5；与第 6 页表 4 对照）
- **AUTHOR_INTERPRETATION**｜作者把普遍提升解释为附加指令、尤其 instruction tuning 对工具检索有利。（物理 PDF 第 7 页，§6.2）
- **AUTHOR_FACT**｜TOOLRET 与 MTEB retrieval subset 的模型表现相关性报告为 Pearson 0.790、Spearman 0.441，但 TOOLRET 的绝对分数更低。（物理 PDF 第 6–7 页，图 5、§6.3；第 24 页，图 7）
- **AUTHOR_FACT**｜候选范围会显著改变数值。以 bge-reranker-v2-gemma 为例：在 43,215 工具完整 corpus 的 `w/ inst.` 表 5 中，平均 NDCG@10 / Completeness@10 为 47.52 / 48.90；限制为“每个原始数据集自己的 toolset”的控制实验表 10 中为 74.14 / 78.09。（物理 PDF 第 7 页表 5；第 24–25 页，表 10 与 Appendix D.3）
- **AUDIT_JUDGMENT**｜完整 corpus、单一 subset、单一原始数据集 toolset 是三个不同候选范围；不能跨范围直接把高分解释为模型本身变强。完整 corpus 结果才直接对应论文强调的 43,215 工具检索难题。

## 5. TOOLRET-train 与 hard-negative operator

- **AUTHOR_FACT**｜TOOLRET-train 来自 ToolACE、APIGen、ToolBench 的**训练集**。表 7 的精确规模为 **205,826 tasks**；平均 query 52.87 tokens、instruction 46.72、tool documentation 163.52；平均 targets 2.31。（物理 PDF 第 8 页，§7.2；第 20–21 页，Appendix C、表 7）
- **AUTHOR_FACT**｜优化目标对每个 target tool 最大化相对 negatives 的 similarity softmax：输入为 `instruction I ⊕ query q`，对 targets 求平均；§7.2 明写 K=10、learning rate=5e-5。（物理 PDF 第 8 页，“Learning objective”及公式）
- **AUTHOR_FACT**｜hard-negative 描述存在三处不一致：
  - §1 称每个训练任务配 **10 个由 NV-Embed-v1 检索的 negative tools**；
  - §7.2 称先由待训练模型 `θ` 自身检索 top-K、排除 `T` 后作为 negatives，并设 K=10；
  - 表 7 却写 **每个 query 有 5 个 negative tools**。
  （物理 PDF 第 2 页，定位语 “10 negative tools retrieved by the NV-embed-v1”；第 8 页公式前；第 21 页表 7）
- **AUDIT_JUDGMENT**｜仅凭 PDF 无法唯一恢复实际训练时是固定 NV-Embed-v1 mining 还是 per-model self-mining，也无法确定落盘训练实例实际含 5 个还是 10 个 negatives；这不是可安全代作者消解的同义表述。复现或比较训练收益前必须查公开数据/代码，但本次隔离二读没有联网，也没有读取外部资产。
- **AUTHOR_FACT**｜表 14 的清晰例子：e5-large-v2 未训练时平均 NDCG@10 / Completeness@10 为 20.78 / 20.02；query-only 训练（†）为 27.30 / 28.05；instruction+query 训练（‡）为 30.18 / 30.39。（物理 PDF 第 27 页，表 14）
- **AUTHOR_INTERPRETATION**｜作者据此把 instruction-aware 训练增益解释为 TOOLRET-train 能提升检索，并进一步改善工具调用 agent。（物理 PDF 第 8 页，§7.2；第 25–27 页，Appendix D.5、表 14）

## 6. ToolBench 下游链接

- **AUTHOR_FACT**｜下游协议是在 ToolBench-G1/G2/G3 上，用从 TOOLRET 的约 43k corpus 检索出的工具替换官方预标注 toolset（oracle），将 top-K 工具一次性传给 GPT-3.5 或 ToolLLaMA，并用 ToolBench 官方 Pass Rate 衡量是否成功调用正确工具完成任务。（物理 PDF 第 7 页，§7；第 26 页，Appendix D.6）
- **AUTHOR_FACT**｜以 bge-large-en-v1.5 为例，训练前后 TOOLRET NDCG@10 为 23.03→32.95。对 GPT-3.5：G1 retrieval NDCG 34.29→71.11、Pass Rate 50.60→59.50（oracle 62.00）；G2 为 9.48→18.11、49.00→58.40（oracle 57.20）；G3 为 29.69→67.87、56.90→59.20（oracle 67.40）。（物理 PDF 第 28 页，表 15）
- **AUTHOR_FACT**｜同一 retriever 配 ToolLLaMA 时：G1 Pass Rate 37.60→45.10（oracle 53.60）；G2 41.30→47.30（oracle 50.80）；G3 37.20→39.60（oracle 49.10）。（物理 PDF 第 28 页，表 15）
- **AUTHOR_INTERPRETATION**｜作者将 Figure 6 与表 15 的共同趋势解释为更好的 retrieval 会提高 downstream pass rate，并在结论中概括为训练后 agent pass rate 提升 10%–20%。（物理 PDF 第 8–9 页，图 6、§7.2、§9）
- **AUDIT_JUDGMENT**｜表 15 中 GPT-3.5/G2 的训练后 58.40 高于所谓 oracle 57.20，说明这里的 oracle 是官方候选集参考条件，不是严格数学上界；Pass Rate 仍同时受 agent 规划、选择、调用和评测波动影响。论文显示的是受限协议下的联动证据，不是仅由 retrieval 指标单变量决定的普适定律。

## 7. false-negative、参数/范围、生成指令、语言与 one-shot 限制

- **AUTHOR_FACT**｜作者明确承认合并数据集产生 one-to-many 问题：来自数据集 A 的 query 只把 A 的 ground truth 当 label，而数据集 B 中功能相似的工具也可能有效，却在评测中不算 relevant。（物理 PDF 第 8–9 页，§8 “Fine-grained functional differences of tools”及脚注 5）
- **AUTHOR_INTERPRETATION**｜作者的辩护是原数据集标注工具应视为“最适合”的工具；表面功能相似的工具还可能在输入参数（如是否支持语言筛选）或应用范围（医疗搜索 vs 通用新闻搜索）上不同，模型应做细粒度判别。（物理 PDF 第 9 页，§8，定位例 “search news articles in Chinese”）
- **AUDIT_JUDGMENT**｜这说明“同属搜索 API”不等于可互换，参数与适用范围确实能使某一标签更精确；但论文没有对合并 corpus 做穷尽式多相关标签复标。因此，未标注但语义可用的工具会成为 metric false negative；hard-negative mining 仅排除已知 `T`，也可能把这类工具采成假负例。作者的合理性论证没有量化该误差率。
- **AUTHOR_FACT**｜生成 instruction 的局限：论文只给每个 task 生成/修订一条 target-aware instruction；作者承认 LLM 对 prompt wording 敏感，尚未充分研究 prompt sensitivity，未来需标注更多 instruction formulations/styles。（物理 PDF 第 10 页，Limitation (i)）
- **AUTHOR_FACT**｜语言/模态局限：当前 benchmark 限于**英语**与**文本检索**，没有覆盖 multilingual retrieval；多模态数据中的图像以 URL 表示。（物理 PDF 第 10 页，Limitation；第 16 页，Appendix B.2 “Mnms”）
- **AUTHOR_FACT**｜调用时序局限：当前是 retrieval-then-calling，检索只在最初触发一次，再把 top-K 工具交给 tool-use LLM；没有评测 interleaved retrieval-and-calling，也没有让后续长链 reasoning 反复触发检索。（物理 PDF 第 10 页，Limitation (ii)）
- **AUDIT_JUDGMENT**｜所以本文的正向结果边界是：英语、文本工具描述、一次性 top-K、指定 ToolBench split、GPT-3.5/ToolLLaMA、继承标签与官方 Pass Rate。不能外推到多语言、真实动态工具库、交错检索调用或多轮纠错。

## 8. 对“检索后语义正确性”的证据裁决

- **AUTHOR_FACT**｜论文直接测量的是 retrieval relevance/completeness 指标与 ToolBench 官方 Pass Rate；没有单列最终自然语言答案的语义正确率、工具返回内容真实性、参数值正确率，也没有把错误分解为 retrieval、planning、argument filling、execution 与 answer synthesis。（物理 PDF 第 5 页 §5.1；第 7–8 页 §7；第 26–28 页 Appendix D.6、表 15）
- **AUTHOR_INTERPRETATION**｜作者把较低 retrieval 与较低 Pass Rate、训练后两者同步上升解释为 retrieval 对下游成功至关重要。（物理 PDF 第 1 页图 1；第 8 页图 6、§7.2）
- **AUDIT_JUDGMENT**｜本源**能支持**：在其英语 one-shot ToolBench 协议中，候选工具集质量是下游任务通过率的重要约束；用 TOOLRET-train 调整若干 retriever 后，多数组合的官方 Pass Rate 上升。
- **AUDIT_JUDGMENT**｜本源**不能证明**：只要 Recall/NDCG/Completeness 提升，检索后的 agent 输出就在语义上正确；也不能证明 label 外的工具语义错误、正确工具被调用时参数一定正确、或最终答案忠实于工具结果。理由是标签非穷尽、instruction 使用 target 信息、Pass Rate 未做语义错误分解、且 one-shot/英语/指定 agent 的范围有限。
- **AUDIT_JUDGMENT**｜因此，对 CRL 中“semantic correctness after retrieval”的最稳妥用途是把本文视为“retrieval bottleneck 与 downstream pass-rate 联动”的证据，而不是“检索提升已经解决端到端语义正确性”的证据。

## 9. 独立二读结论

- **AUDIT_JUDGMENT**｜TOOLRET 的核心贡献是把跨 34 个来源、7,615 个任务、43,215 个工具置于统一全语料检索设置，并揭示完整候选范围下的明显难度；target-aware instruction 与 TOOLRET-train 确有表内增益。
- **AUDIT_JUDGMENT**｜对后续使用最关键的保留项有三条：其一，合并来源后的非穷尽标签会产生 false negatives；其二，hard-negative 数量与生成者在 PDF 内部矛盾，复现前必须外部核验；其三，下游 Pass Rate 证明的是特定协议中的任务联动，不等价于检索后语义正确性证明。

## 10. 本次读取与工具轨迹

- **读取范围**：工作区根 `AGENTS.md`、`crl_agent_v3/AGENTS.md`、`crl_agent_v3/CRL.md`、`crl_agent_v3/CRL_ENVIRONMENT.md`、PDF skill、指定 `invocation.md`、指定 P085 PDF 的物理页 1–28，以及本输出路径是否存在的布尔检查；没有读取 invocation 明令禁止的资产。
- **指令读取轨迹**：首次把五份指令合并输出时发生控制台乱码且输出截断，未把该次结果冒充完整读取；随后以 `Get-Content -Encoding utf8` 按文件/行段重读到各自 EOF。首次抽取 PDF 物理页 1–7 时遇到 stdout 的 GBK `UnicodeEncodeError`，随后显式把 Python stdout 配为 UTF-8 并成功重跑；该失败没有产生文件。
- **论文读取工具**：`Get-FileHash`/`Get-Item` 核验 PDF 身份；受支持解释器 `D:\Desktop\crl_judge\crl_agent_v3\.venv\python.exe` 中的 PyMuPDF 1.28.0 获取页数/metadata，并按 1–7、8–14、15–21、22–28 四段抽取原页文本；对物理页 4、5、21、28 额外运行版面表格探测。曾在内存中渲染物理页 4、5，界面未能解码图像；没有为此写临时文件，数字判断回到原始页文本、表题、行列顺序与上下文。
- **联网状态**：未联网；未调用外部 API、搜索引擎或付费模型。
- **模型可见标识**：当前上下文只暴露 `Codex（基于 GPT-5）`；更精确的后端 model/version 不可见，因此不推测。
- **任务标识**：attempt `r2-20260720-p085-a1`；协作任务 `/root/p085_second_read`。
