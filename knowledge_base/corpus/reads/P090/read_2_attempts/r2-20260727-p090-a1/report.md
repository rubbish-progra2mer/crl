# P090 独立二读报告（read_2）— MemGAS

## 报告头部（校验信息）

- 论文文件：`D:\Desktop\crl\crl_agent_v3\knowledge_base\staging\w06_targeted\P090_memgas.pdf`
- 实测 SHA-256：`256eba2430611820eb4b18978fdd35f05a3bcf26c7b808b03ef0971ab3bc49c8`（与任务给定值完全一致）
- 实测物理页数：33（PyMuPDF `page_count=33`；印刷页码与物理页码一一对应，物理第 1 页页脚印 "1"，物理第 33 页页脚印 "33"）
- canonical metadata 核对：物理 p.1 边栏逐字 "arXiv:2505.19549v2 [cs.CL] 29 Sep 2025"；标题 "FROM SINGLE TO MULTI-GRANULARITY: TOWARD LONG-TERM MEMORY ASSOCIATION AND SELECTION OF CONVERSATIONAL AGENTS"；与 canonical（arXiv 2505.19549v2, 2025-09-29, preprint）一致。文中含 ICLR 风格的 Ethics Statement 与 Reproducibility Statement（p.10），无会议接收标注，按 preprint 对待。
- 抽取方式：python + PyMuPDF 全文文本抽取；对 p.6、p.7、p.8、p.19、p.20、p.21、p.32 共 7 个关键表格/图页做了 150dpi 渲染视觉抽查（结论见第 8 题）。
- 读者：fresh 独立二读（r2-20260727-p090-a1），未读取 read_1、任何 Card、reconciliation 或 Run 目录。

---

## 1. 方法究竟改变哪一步计算？

1.1 [AUTHOR_FACT] MemGAS 是训练无关（training-free）的外部记忆系统：不改动任何模型权重，改动的是"记忆写入/索引"与"检索排序/上下文构造"两段计算。定位：p.5, §3.1, "Since our task is training-free, the whole QA pairs in datasets are used"。

1.2 [AUTHOR_FACT] 写入步改动一：每个 session 用 LLM 生成 summary 与 keywords，并切分 turns，与原 session 一起构成四粒度记忆单元 Mi = {Si, Ti, Ui, Ki}。定位：p.3, §2.2, Eq.(1)(2), "Ui, Ki = fLLM(Si), Ti = segment(Si)"。

1.3 [AUTHOR_FACT] 写入步改动二：新记忆插入时，用 Contriever 编码、计算新旧记忆两两相似度，再以 GMM 把相似度分数聚成 Accept/Reject 两个概率集合，仅对 Accept 集建边，维护一张随时间增量更新的关联图 Acur。定位：p.3–4, §2.2, "a Gaussian Mixture Model (GMM)-based clustering strategy"; "Acur ← Acur ∪ Anew"。

1.4 [AUTHOR_FACT] 检索步改动一（打分）：对每个查询，先按粒度 g 分别对全部记忆算相似度分布，softmax（温度 λ）归一后取香农熵 Hg，粒度权重 wg ∝ 1/Hg（熵低=匹配确定=权重大），初始得分为跨粒度加权和。定位：p.4–5, §2.3–2.4, Eq.(3)(4)(5), "normalizing their inverse entropy"。

1.5 [AUTHOR_FACT] 检索步改动二（图传播）：以初始得分选 top-α 种子节点，在关联图上跑 Personalized PageRank，按最终 PPR 分数取 top-K 候选。定位：p.5, §2.4, "we select the top α nodes as seed nodes and run the PPR algorithm"。

1.6 [AUTHOR_FACT] 生成前改动三（过滤）：top-K 记忆连同 query 送入一次额外的 LLM 过滤调用，删除无关/冗余内容后才交给回答生成器；过滤提示词要求 "Preserve original tokens, do not paraphrase"。定位：p.5, §2.4, "LLM-Based Redundancy Filtering"；p.26, Figure 9。

1.7 [READER_INTERPRETATION] 概括：被改变的计算是 (a) 记忆库的表示（单粒度块 → 四粒度节点 + GMM 关联图）、(b) 检索打分函数（单一向量相似度 → 熵驱动的粒度加权 + PPR 图排序）、(c) 上下文构造（直接拼接 → 查询感知的 LLM 抽取式过滤）。生成模型、生成提示词与 top-K 预算保持与基线一致。

1.8 [READER_INTERPRETATION] 值得注意：附录 H 的讨论明确说图传播模块 "is not a contribution of our method"（p.26, §H.2 Discussion, "e.g., graph propagation ... not a contribution"），而正文 §2.4 又把 PPR 写为方法组成部分并在 Table 3 消融。作者对 PPR 的"贡献归属"表述在正文与附录间不完全一致。

---

## 2. 输入、输出、可用信息与干预时点

2.1 [AUTHOR_FACT] 任务设定：系统持有多 session 用户-助手交互构成的外部记忆库 M；收到查询 q 时检索相关记忆 Mrel 并生成回答 a = LLM(q, Mrel)。定位：p.3, §2.1, "generates responses via a = LLM(q, Mrel)"。

2.2 [AUTHOR_FACT] 写入时输入：原始对话 session（LoCoMo 为 user-user，其余为 user-AI，见 p.16 Table 4 "Conversation Subject" 行）；由 gpt-4o-mini-2024-07-18 生成 summary/keywords（p.6, "backbone for all tasks, including multi-granularity information generation and QA"），由 Contriever 生成向量（p.6, "Contriever is used as the encoding model"）。

2.3 [AUTHOR_FACT] 查询时输入：query 及其 Question Date；QA 提示词与过滤提示词均含 {question_date} 字段。定位：p.26–27, Figures 9–10。

2.4 [READER_INTERPRETATION] Question Date 对所有方法的 QA 提示词统一提供（Figure 10 注明 "follows Lu et al. (2023); Pan et al. (2025)"，且 p.6 声明所有基线共享一致生成提示词），因此不构成 MemGAS 独有的信息优势。

2.5 [AUTHOR_FACT] 输出：QA 任务输出自然语言回答（按 GPT4o-J/F1/BLEU/ROUGE/BERTScore 评估）；检索任务输出 session 级排序（Recall@K/NDCG@K，p.7 Table 2）。

2.6 [AUTHOR_FACT] 干预时点共三处：(i) 每次新 session 写入时（元数据生成 + GMM 建边，"When a new memory Mnew is added"，p.3）；(ii) 每次查询的检索排序时（熵路由 + PPR）；(iii) 检索后、生成前（LLM 过滤）。生成步本身不被干预。

2.7 [AUTHOR_FACT] 可用信息边界：推理期不使用检索 ground-truth 或 query type 标签；路由权重完全由查询-记忆相似度分布的熵无监督算出（p.4–5, "eliminating the need for manual intervention"）。Table 7 的 "Optimal Selection" 仅作为上界对照列出（p.19）。

---

## 3. 最强基线与最接近组合基线

3.1 [AUTHOR_FACT] 基线共 9 个：Full History、MPNet、Contriever、RecurSum、MPC、A-Mem、SeCom、HippoRAG 2、RAPTOR（p.5–6, §3.1 "Baselines"；正文将 HippoRAG 2 与 RAPTOR 归为 "structured RAG models"）。

3.2 [AUTHOR_FACT] 按数据看最强基线是 HippoRAG 2：LongMemEval-s 上基线最高 4o-J 57.60、R@3 75.53（p.6 Table 1；p.7 Table 2）；LoCoMo 上 4o-J 45.62 为全表最高（加粗，超过 MemGAS 的 41.07）。其次 SeCom（LoCoMo 4o-J 44.21，同样高于 MemGAS）。

3.3 [AUTHOR_FACT] 最接近的"组合基线"是附录 C 的 "Combination"（简单多粒度并联，无 GMM/路由/PPR/过滤），与四个单粒度设置一起在 Table 5（QA, p.17）与 Table 6（检索, p.18）中对照；例如 LongMemEval-s 上 Combination F1 14.59 vs MemGAS 20.38。

3.4 [AUTHOR_FACT] 消融表中 "w/o All" 行（Table 3, p.8）数值与 Contriever 单粒度基线完全一致（4o-J 55.40 / F1 13.78 / R@3 71.06），即作者把"全部组件去掉"定义回退到 Contriever session 级检索。

3.5 [READER_INTERPRETATION] 公平性较强的对照是附录 D.2 的同 token 成本比较（p.20–21, Table 10）：over-retrieval 后按固定输入 token 截断，MemGAS 在两个预算档均最高（59.8 / 60.3 vs HippoRAG2 57.4 / 58.2）。但该表存在印刷疑点（见 8.2.1）。

3.6 [OPEN_QUESTION] "Combination" 的具体实现（四粒度分数如何合并、是否含过滤步）原文未给公式；只能从上下文推断为等权或朴素并联，无法据此精确复现该组合基线。

---

## 4. 结果是否可能来自模型、token、tool-call、prompt 或 oracle 差异？

4.1 [AUTHOR_FACT] 模型与 prompt 层面的控制：所有方法统一 gpt-4o-mini-2024-07-18 生成、共享一致生成提示词、temperature=0、zero-shot、统一 top-3 session 检索（SeCom 用 top-3 segments、RAPTOR 用 sessions/summaries）、除 MPNet/Full History 外统一 Contriever 编码。定位：p.6, "Implementation Details", "To ensure fairness, all baselines share consistent generation prompts"。

4.2 [READER_INTERPRETATION] token 预算：Table 1 中 MemGAS 平均 tokens（LongMemEval-s 8,829）与多数基线同量级，但约为 SeCom（2,741）的 3.2 倍；对 SeCom 的 QA 优势部分可能来自更大的上下文预算。D.2 的定预算实验缓解了这一疑虑（同预算下 MemGAS 仍高于 SeCom 约 2 分）。

4.3 [READER_INTERPRETATION] 正文效率声明与自家表格不完全相符：p.7 称 "average tokens and latency ... below HippoRAG2 and A-Mem"，但 Table 1 LongMemEval-s 中 MemGAS tokens 8,829 > HippoRAG 2 的 8,530（latency 确实更低：2.55 vs 4.51）。属措辞过强。

4.4 [READER_INTERPRETATION] 额外 LLM 调用（近似 tool-call 差异）：MemGAS 每查询多一次过滤调用、建库期多 summary/keyword 生成调用。建库开销已在 Table 8（p.20）披露（输入 52.9M/输出 5.2M tokens，低于 HippoRAG 2 与 SeCom）；查询期延迟已计入 Table 1/Table 3。但 Table 3 的消融只拆 GMM/PPR/MA/Router 四项，没有单独的 "w/o LLM-Filter" 行——过滤步的独立贡献未被隔离，而多数基线不享有这一查询感知压缩步。这是主要的未受控组件差异。

4.5 [READER_INTERPRETATION] 指标口径：F1/BLEU/ROUGE 的提升幅度（LongMemEval-s F1 13.78→20.38，+48%）远大于 GPT4o-J 的提升（55.40→60.20，+8.7%）。过滤提示词要求保留原 token、QA 提示词要求 concise，词面重叠类指标可能被"更抽取式、更短的回答风格"放大；GPT4o-J（二值判定，prompt 见 p.27 Figure 11）是更稳健的口径。

4.6 [AUTHOR_FACT] 无 oracle 泄漏的直接证据：路由为无监督熵驱动；Table 7 中 Router 距 "Optimal Selection" 上界仍有明显差距（如 knowledge-update 51.39 vs 72.22，p.19），侧面说明未使用 per-query 最优粒度标签。

4.7 [OPEN_QUESTION] 检索指标的映射口径：ground-truth 是 session 级（Table 4, p.16），MemGAS 检回的是多粒度节点；turn/summary/keyword 命中如何折算为 session 级 Recall/NDCG 原文未写明。若按"所属 session 记命中"，多粒度天然增加同一 session 的命中通道；这一口径细节影响 Table 2 的可比性，需查代码（github.com/quqxui/MemGAS，p.1 脚注）确认。

4.8 [OPEN_QUESTION] LoCoMo 上 Table 1（4o-J 41.07）与 Table 5（40.08）、Table 2 与 Table 6 的 MemGAS 检索行（57.30/58.76/67.32/63.62/81.82/68.42 vs 57.45/58.84/67.12/63.60/81.07/68.24）数值不一致，疑为不同 run 或不同配置混排；原文未解释（详见 8.3）。

---

## 5. 作者明示限制、负向结果和未测试边界

5.1 [AUTHOR_FACT] 全文没有独立的 "Limitations" 章节；p.10 仅有 Ethics Statement 与 Reproducibility Statement。

5.2 [AUTHOR_FACT] 表内可见的负向结果（作者如实印出但正文淡化）：(a) LoCoMo 4o-J：MemGAS 41.07 低于 HippoRAG 2 的 45.62（加粗为最佳）与 SeCom 的 44.21（p.6, Table 1）；(b) Table 5 中 4o-J 指标上 Combination 在 LongMemEval-m（46.40 vs 45.40）与 LoCoMo（42.80 vs 40.08）高于 MemGAS（p.17）；(c) Table 7 中 single-session-user 查询 Router（60.94）低于 turn 级单粒度（65.62）（p.19）。

5.3 [AUTHOR_FACT] 作者明示的负向观察：LongMemEval-s 上 top-K 增大时 F1 先升后降，"longer context introduces noise, which negatively impacts the model's effectiveness"（p.9, §3.4, Figure 4）。

5.4 [AUTHOR_FACT] 错误分析（p.23 §G, p.24 Figure 7）：LongMemEval-m 上 "Wrong Retrieval + Wrong Generation" 占 40.6%，LoCoMo-10 上占 40.5%；即使 LongMemEval-s 也仅 52.6% 为"检索对且生成对"。检索仍是主要瓶颈。

5.5 [AUTHOR_FACT] 实验覆盖的明示缺口：RAPTOR、A-Mem、HippoRAG 在 LongMemEval-m 上 "unavailable due to high runtime"；RAPTOR 与 A-Mem 的检索无法评估（"retrieved information cannot be judged"）；LongMTBench+ 无检索 ground-truth 被排除出检索评测（p.6–7）。

5.6 [AUTHOR_FACT] 超参敏感性：α（种子节点数）约 15 最优、过大导致 "lose the ability to explore the memory graph"；λ 约 0.2 最优、过大导致 "the same entropy for different granularities"（p.22, §F；Figure 6 标题注明在 LoCoMo 上分析）。

5.7 [READER_INTERPRETATION] 未测试边界（原文未做）：非英语对话；更强/更大生成器（只测了 GPT4o-mini 与 qwen3-8b/1.7b，p.21–22 Table 12）；记忆遗忘/更新机制（相关工作提及但 MemGAS 未实现）；关联图随更大会话量增长的可扩展性（最大只到 LongMemEval-m 约 1M token/会话）；GMM 两簇假设在相似度分布非双峰时的行为。

5.8 [OPEN_QUESTION] 超参在 LoCoMo 上做敏感性分析后是否将同一组 (α=15, λ=0.2) 用于全部四个数据集，原文未明说；若逐数据集调参，公平性叙述需相应打折。

---

## 6. 可抽取的 Operator 与真实可记录的 Failure

### Operator 候选（均为作者报告的方法/协议，可操作化）

6.1 [AUTHOR_FACT] OP-多粒度记忆单元：对每个 session 并行存 {session, turns, LLM summary, LLM keywords} 四种粒度节点（p.3, Eq.1–2）。

6.2 [AUTHOR_FACT] OP-熵驱动粒度路由：对每粒度的 query-记忆相似度分布做温度 softmax→香农熵→按 1/Hg 归一得软权重；低熵粒度权重大（p.4–5, Eq.3–4；理论性质 p.25, Prop.2）。

6.3 [AUTHOR_FACT] OP-GMM 接受/拒绝建边：新记忆插入时对相似度分数拟合两分量 GMM，仅与 Accept 簇建关联边，增量维护记忆图（p.3–4；理论界 p.25, Prop.1 "Exponentially small mis-link rate"）。

6.4 [AUTHOR_FACT] OP-加权种子 + PPR 排序：跨粒度加权分选 top-α(≈15) 种子，在记忆图上跑 PPR 取 top-K（p.5, Eq.5）。

6.5 [AUTHOR_FACT] OP-保 token 的查询感知过滤：生成前用 LLM 按 query 过滤检回内容，指令明确 "Preserve original tokens, do not paraphrase"（p.26, Figure 9）。

6.6 [AUTHOR_FACT] OP-评测协议-同 token 成本比较：over-retrieval 后按固定输入 token 阈值截断再比 QA，隔离上下文预算混淆（p.20, §D.2）。

6.7 [READER_INTERPRETATION] OP-诊断协议-粒度×查询类型矩阵：Table 7 式的"每类查询×每粒度 Recall + Optimal Selection 上界"分析，可复用为任意多视图检索系统的路由诊断工具（p.19, §C.3）。

### Failure 候选（真实、可定位、可记录）

6.8 [AUTHOR_FACT] F-keyword 单粒度灾难：仅用 keyword 级检索时 QA 大幅崩塌（LongMemEval-s 4o-J 17.20 vs session 级 55.40；p.17, Table 5）；summary 单粒度同样严重退化（28.80）。

6.9 [AUTHOR_FACT] F-长上下文噪声：LongMemEval-s 上 top-K 从 1 到 10 时 F1 先升后降（p.9, Figure 4 及正文）。

6.10 [AUTHOR_FACT] F-user-user 对话失利：LoCoMo（唯一 user-user 数据集）上 MemGAS 的 GPT4o-J 低于 HippoRAG 2 与 SeCom（41.07 vs 45.62/44.21，p.6 Table 1）。[READER_INTERPRETATION] 可能与其 summary/keyword 提示词假定 "user-AI assistant dialogue memory"（p.26, Figure 8）与 user-user 语料不匹配有关。

6.11 [AUTHOR_FACT] F-路由非全胜：single-session-user 查询上 Router 低于最佳单粒度 turn 级（60.94 vs 65.62），且各类查询距 Optimal Selection 上界均有 10–20 点差距（p.19, Table 7）。

6.12 [AUTHOR_FACT] F-检索瓶颈仍在：LongMemEval-m 错误中 40.6% 属 "Wrong Retrieval + Wrong Generation"（p.24, Figure 7）。

6.13 [READER_INTERPRETATION] F-简单组合在判定指标上可反超：4o-J 口径下朴素 Combination 在 2/4 数据集高于完整 MemGAS（见 5.2b），提示复杂管线的收益对指标口径敏感，不宜仅按词面指标立论。

---

## 7. 判断与物理页码/章节/图表/逐字定位对照表

（以上各条已内嵌定位；此处汇总核心锚点。物理页码=印刷页码。）

| # | 判断 | 物理页 | 章节/图表 | 短逐字定位语 |
|---|------|--------|-----------|----------------|
| 1 | 四粒度元数据生成 | p.3 | §2.2, Eq.1–2 | "Ui, Ki = fLLM(Si)" |
| 2 | GMM 接受/拒绝建边 | p.3–4 | §2.2 | "clustered by GMM into two probabilistic sets" |
| 3 | 熵路由权重 | p.4–5 | §2.3, Eq.3–4 | "normalizing their inverse entropy" |
| 4 | PPR 检索 | p.5 | §2.4, Eq.5 | "run the PPR algorithm" |
| 5 | LLM 过滤 | p.5, p.26 | §2.4; Fig.9 | "Preserve original tokens, do not paraphrase" |
| 6 | 实现细节/公平性控制 | p.6 | §3.1 | "gpt-4o-mini-2024-07-18" |
| 7 | 主 QA 结果 | p.6 | Table 1 | "MemGAS (Ours) 60.20 20.38" |
| 8 | LoCoMo 4o-J 失利 | p.6 | Table 1 LoCoMo 段 | "45.62"（HippoRAG 2 加粗） |
| 9 | 主检索结果 | p.7 | Table 2 | "78.51 86.83 88.94" |
| 10 | 消融（无过滤步消融行） | p.8 | Table 3 | "w/o GMM ... w/o Router ... w/o All" |
| 11 | top-K 噪声 | p.9 | §3.4, Fig.4 | "longer context introduces noise" |
| 12 | 数据集统计 | p.16 | Table 4 | "Avg. Token 103,137.4" |
| 13 | 单粒度 vs 多粒度 | p.17–18 | Tables 5–6 | "Combination 46.40"（LongMemEval-m 4o-J） |
| 14 | 路由诊断矩阵 | p.19 | Table 7, §C.3 | "Optimal Selection" |
| 15 | 建库 token 成本 | p.20 | Table 8 | "52.9M (100 %)" |
| 16 | 同预算比较 | p.21 | Table 10 | "8,000 ... 8,000 ... 103,137" |
| 17 | 生成器泛化 | p.21–22 | Table 12 | "Base Generator: qwen3-1.7b" |
| 18 | 超参 | p.22 | §F, Fig.6 | "around 0.2"；"around 15" |
| 19 | 错误分析 | p.23–24 | §G, Fig.7 | "40.6%" |
| 20 | 理论分析与 PPR 归属 | p.25–26 | §H | "not a contribution of our method" |
| 21 | 过滤案例（互换疑点） | p.32–33 | Figs.15–16 | "After Filter" |

---

## 8. 解析文本与可视 PDF 是否冲突（就抽查页面回答）

8.1 [READER_INTERPRETATION] 总体结论：在抽查的 p.6、p.7、p.8、p.19、p.20、p.21、p.32 七页上，PyMuPDF 解析文本与 150dpi 渲染图像逐项核对一致，未发现"解析引入"的数字或语句错误；表格数值（Table 1/2/3/7/8/9/10/11）双通道相符。

8.2 以下异常经双通道（文本+视觉）确认为 PDF 原生内容，属论文自身缺陷而非解析伪影：

8.2.1 [AUTHOR_FACT] Table 10（p.21）两个分块的 "Input Tokens" 列均印为 "8,000"，而 §D.2 正文（p.20）明确写 "thresholds of 8,000 and 16,000 input tokens"。[READER_INTERPRETATION] 第二个 "8,000" 应为 "16,000" 的排版错误；两块的 latency/分数确实不同（MemGAS 2.42/59.8 vs 3.15/60.3），支持"两个不同预算档"的解读。

8.2.2 [AUTHOR_FACT] Figure 15（p.32）的 Query 问 "doing a great job with sustainability"（答案 "Patagonia"），但其 After Filter 框内容却是"两家重视员工安全的公司"（Patagonia + Southwest Airlines）；Figure 16（p.33）恰好相反。[READER_INTERPRETATION] 两图的 After Filter 输出框互换了位置，属排版错配；不影响主实验数据，但削弱案例研究的证据力。

8.2.3 [AUTHOR_FACT] p.20 §D.1 正文称 HippoRAG 2 与 SeCom 输出 token "over 100 M and 70 M"，但同页 Table 8 显示 HippoRAG 2 输出仅 10.9M（其输入为 111.1M）。[READER_INTERPRETATION] 正文把 HippoRAG 2 的输入 token 误写成输出；MemGAS 相对 HippoRAG 2 的"输出 token 优势"实际是 5.2M vs 10.9M（约 2 倍），而非 20 倍。

8.3 [AUTHOR_FACT] 同一设置数值跨表不一致（双通道确认）：LoCoMo 上 MemGAS 的 GPT4o-J 在 Table 1 为 41.07、Table 5 为 40.08；MemGAS 检索行 Table 2 为 57.30/58.76/67.32/63.62/81.82/68.42、Table 6 为 57.45/58.84/67.12/63.60/81.07/68.24（Table 11 的 Contriever 段与 Table 2 一致，§C.2 正文引用的 81.07/68.24 与 Table 6 一致）。[OPEN_QUESTION] 何者为 canonical run 无法从原文判定；引用 LoCoMo 数字时应注明表号。

8.4 [AUTHOR_FACT] 数据集统计口径不一致：p.16 正文称 LongMemEval-s "average of 115k tokens"、LongMemEval-m "avg. 1.5 million tokens"，而同页 Table 4 为 103,137.4 与 1,019,116.7。[READER_INTERPRETATION] 正文数字疑沿用 LongMemEval 原论文口径，表格为作者自测；差异约 10%–47%。

8.5 [AUTHOR_FACT] 其他印刷缺陷（不影响结论但反映校对粗糙）：p.3 §2.1 粒度选择映射印作 "{αs, αt, αk, αs}"（αs 重复，末位应为 summary 对应符号）；p.6 基线名误拼 "RAPOTR"；p.20 Table 9 两处 "milinon"（应为 million）；p.8 正文引用查询类型结果指向 Figure 5（在附录 p.23），而主文 p.8 的 Figure 3 才是同主题柱状图。

---

## 附：本读者的总体独立判断（非评分）

[READER_INTERPRETATION] 该论文的核心可信主张是：在统一生成器/提示词/top-K 的受控设置下，"多粒度节点 + 无监督熵路由 + 图传播 + 查询感知过滤"的组合在 LongMemEval-s/m 与 LongMTBench+ 的 QA 与 session 级检索上稳定优于九个基线；同预算实验（Table 10）与建库成本表（Table 8）增强了结论稳健性。核心保留意见有三：(i) LLM 过滤步未单独消融且为多数基线所无（4.4）；(ii) 词面指标增幅远大于判定指标，存在回答风格放大效应（4.5）；(iii) LoCoMo（user-user）上判定指标输给两家基线且多表数值不一致（5.2、8.3）。多粒度检索折算 session 级指标的口径（4.7）是复现前必须向代码求证的最大空白。
