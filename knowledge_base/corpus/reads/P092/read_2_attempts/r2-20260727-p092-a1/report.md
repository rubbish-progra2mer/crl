# P092 独立二读报告（fresh 读者，W06 扩充波次）

- 报告 ID：r2-20260727-p092-a1
- 读者角色：独立二读（未读取 read_1、任何 reconciliation、Card、Run 目录或波次计划文件）
- 论文：MemConflict: Evaluating Long-Term Memory Systems Under Memory Conflicts
- canonical metadata（任务给定）：MemConflict, arXiv 2605.20926v1 (2026-05-20), preprint (ACM template)
- 实测 SHA-256：`1918dd32c20affd501ac314ab4f1c5b67ab71dc2178784d31b6596030abbebce`（与任务给定值一致）
- 实测物理页数：33 页（PyMuPDF page_count = 33；文件 1,298,872 字节）
- 页码约定：本报告一律使用物理页码 p.1–p.33；论文自身印刷页码为 111:1–111:33（一一对应，物理 p.N = 印刷 111:N）
- 元数据核对：[AUTHOR_FACT] p.1 右侧竖排水印为 "arXiv:2605.20926v1 [cs.IR] 20 May 2026"，与 canonical metadata 一致；页脚 "J. ACM, Vol. 37, No. 4, Article 111. Publication date: August 2018." 及 p.32 末尾 "Received 20 February 2007; revised 12 March 2009; accepted 5 June 2009" 为 ACM 模板占位符（见第 8 节讨论）。
- 文本抽取方式：python + PyMuPDF 逐页抽文本；对 p.6、p.16、p.18、p.19、p.20、p.26、p.27 做了 150dpi 渲染视觉抽查。

---

## 0. 论文一句话定位

[READER_INTERPRETATION] 这是一篇**评测/基准（benchmark + 诊断协议）论文**，不提出新的记忆系统或推理方法；它构造带受控"记忆冲突"的长程多会话对话数据，并用"黑盒答案 + 白盒检索排名"两级协议评测 6 个现成长期记忆系统。因此统一问题清单中"方法改变哪一步计算"应理解为"评测协议改变了评测流水线的哪一步"，而非改变被测系统的计算。

---

## 1. 方法究竟改变哪一步计算？

1.1 [AUTHOR_FACT] MemConflict 把"记忆有效性"重构为 query 条件下的 fitness-for-use 问题，沿三个维度形式化：时间有效性（temporal validity）、事实正确性（factual correctness）、语境适用性（contextual applicability），对应 dynamic / static / conditional 三类冲突。定位：p.1 摘要 "treats memory validity as a query-conditioned fitness-for-use problem"；p.8 §3.1；p.3 Fig. 1 图注。

1.2 [AUTHOR_FACT] 相对既有评测，MemConflict 改变的第一步是**数据构造**：从 Persona Hub 采样 persona seed，由 LLM 生成结构化用户画像 U_u=(I_u, D_u, C_u, T_u, R_u)（式 2，p.9 §3.2），在 2022.01–2025.12 的按月时间线上模拟 chat/update 会话（p.10 §3.3.1 "The timeline spans January 2022 to December 2025"），再注入动态更新 Δ_t（式 4–5，p.10–11）、静态矛盾 P_t（p.11 §3.3.3）、条件绑定 B_t（p.11 §3.3.4）与相关实体干扰项 E_t（式 6，p.12 §3.3.5），最后两阶段（synopsis→dialogue，式 7–8，p.12 §3.4）生成多轮对话。整体流水线见 p.8 Fig. 2 与 p.14 Algorithm 1。

1.3 [AUTHOR_FACT] 改变的第二步是**查询时点**：查询不是在全部会话结束后统一发出，而是"在系统摄入引入冲突的会话之后立即发出"，且以该时刻的历史前缀 H_t 为可用记忆。定位：p.8 §3.1 "each query is issued immediately after the system ingests a session that introduces information conflicting or competing with previously mentioned memory candidates"；p.13 §3.5；p.6 Table 1 中 MemConflict 行 Timing = "After each conflict bearing session"（与其他框架多为 "After all sessions" 对比）。

1.4 [AUTHOR_FACT] 改变的第三步是**评测粒度**：两级协议——黑盒 Answer Accuracy（式 11，p.14）+ 白盒 Support Evidence Hit@K（式 12，p.14）与 Support Rank Score（对数折扣排名分，式 13，p.14），另加轻量诊断指标 UOCS（dynamic，式 14，p.15）与 CRS（static，式 15，p.15）；conditional 不设额外诊断指标（p.15 "No additional diagnostic metric is introduced for conditional conflicts"）。

1.5 [AUTHOR_FACT] 判分方式：所有答案与记忆条目判定由 LLM 辅助匹配 + 人工核验产生（p.15 §3.6 "All answer and memory-item judgments are produced through LLM-assisted matching followed by human verification"；判分 prompt 见 p.33 Fig. A5）。

1.6 [READER_INTERPRETATION] 被测系统本身的计算完全不被修改（p.17 §4.1 "each method is kept as close as possible to its intended memory design and default usage"）；MemConflict 的"计算改变"全部发生在评测侧：数据生成、查询时点、指标分解。

---

## 2. 输入、输出、可用信息与干预时点

2.1 [AUTHOR_FACT] 构造输入：persona seeds {z_u}（Persona Hub，p.9 脚注 2 "https://github.com/tencent-ailab/persona-hub"）+ 预定义属性 schema + 构造配置（p.14 Algorithm 1 Require 行）。构造输出：多会话对话 G、评测查询 Q、金标签 Y（Algorithm 1 Ensure 行）。

2.2 [AUTHOR_FACT] 数据规模：12 个基准实例（每实例一个虚拟用户），平均每实例 52.33 会话、2,349.17 对话轮、203,910.83 tokens、124.33 个查询（dynamic 90.82 / static 16.65 / conditional 16.86）；干扰项平均 32.83 条/实例；冲突距离范围 dynamic 5–25、static 10–45、conditional 9–49 个会话。定位：p.15 §3.7 "We constructed 12 benchmark instances"；p.16 Table 2（已视觉核对）。

2.3 [AUTHOR_FACT] 被测系统的输入：逐会话摄入对话历史（p.3 "Each memory system processes the histories session by session"）；查询时可用信息 = 历史前缀 H_t（p.9 "MemConflict treats each query as grounded in the history prefix available at query time, rather than in the full interaction history"）。被测系统的输出：最终答案 ŷ_i（黑盒）与 top-K 检索记忆条目 R^K_i（白盒；主设置 K=3，p.17 §4.2 "The main white-box evaluation uses K = 3"）。

2.4 [AUTHOR_FACT] 干预时点（评测意义上）：冲突实例"可评测"（所有定义金答案所需信息已出现于历史）后立即发问（p.13 §3.5 "MemConflict constructs evaluation queries only after a conflict instance becomes evaluable... issues a query immediately after the corresponding session s_t has been ingested"）。三类查询语义：static 问不变属性的真值；dynamic 问查询时刻的时间有效值；conditional 给出偏好值、问其适用条件（p.13 §3.5；式 9–10）。

2.5 [AUTHOR_FACT] 金标准定义：式 1（p.9）v* = argmax F(v | α, H_t, q_t)，且"benchmark construction guarantees a unique maximizer for each query"（p.9）。

2.6 [AUTHOR_FACT] 指标聚合：因三类冲突查询数不均衡，总体平均按冲突类型做宏平均（p.15 §3.7 "compute overall averages as macro-averages over conflict types"）。

---

## 3. 最强基线与最接近组合基线

3.1 [AUTHOR_FACT] 被比较对象为 6 个现成长期记忆系统：A-Mem、LangMem、Letta、MemOS、Mem0、Memobase（p.16 §4.1；LangMem/Letta/Memobase 以 GitHub 脚注 3–5 引用，无论文引用）。

3.2 [AUTHOR_FACT] 综合最强：MemOS——平均 AA 0.5539（p.19 Table 3，视觉核对），平均 SEH@3 0.6710 / SRS 0.5879（p.20 Table 4，视觉核对），总运行时最低 1356.3033 秒（p.26 Table 6，视觉核对）。分项最强：dynamic AA 最高为 LangMem 0.4966；dynamic SEH@3/SRS 最高为 LangMem 0.7842/0.7089；conditional AA 最高为 MemOS 0.8449、conditional SEH@3 最高为 Letta 0.9046。定位：p.19 Table 3、p.20 Table 4。

3.3 [OPEN_QUESTION] 本文没有任何"组合基线"或朴素对照：没有 full-context / long-context 无记忆系统基线，没有朴素 RAG over raw history 基线，也没有"最新提及优先"（recency heuristic）之类的规则基线。因此无法从文中判断这 6 个系统相对"把全部历史塞进上下文"或"简单向量检索原始对话"能好多少。原文未提供，须在后续实验中自行补充。

3.4 [READER_INTERPRETATION] 由于这是基准论文，"最强基线"问题应转述为"被测系统中的最强者"（MemOS），而"最接近组合基线"在本文语境下不存在——这是该基准作为证据源的一个结构性空缺（与 3.3 同）。

---

## 4. 结果是否可能来自模型、token、tool-call、prompt 或 oracle 差异？

4.1 [AUTHOR_FACT] 模型统一：所有基准构造 LLM 调用（画像生成、对话生成、查询生成）及"需要 LLM 的记忆系统后端"均使用 gpt-5.0-mini。定位：p.18 §4.2 末段 "All LLM calls used in benchmark construction, including profile generation, dialogue generation, query generation, and memory-system backends that require an LLM, use gpt-5.0-mini."（该模型名已对 p.18 渲染图视觉核对，等宽字体原文即为 "gpt-5.0-mini"）。

4.2 [READER_INTERPRETATION] 因此跨系统比较中 LLM 主干差异被大体控制，但仍存在以下可能的非方法性差异来源：
  (a) **构造-评测同源偏置**：数据由 LLM 生成、判分由 LLM 辅助（p.15；p.33 Fig. A5），生成与判分若共享风格/措辞偏好，可能系统性利好与该风格对齐的记忆表示；人工核验（p.13 §3.4、p.15 §3.6、p.8 Fig. 2 "Human Verification"）可部分缓解但文中未报告核验的规模、一致率或修正率。
  (b) **白盒接口适配差异**：各系统以"同一查询协议、答案归一化、白盒检索接口"接入（p.17 §4.1 "all systems follow the same query protocol, answer normalization procedure, and white-box memory retrieval interface"），但各系统记忆条目粒度不同（linked notes / profile / 层级记忆），"gold memory item 是否命中"依赖 LLM 判分对不同粒度条目的语义匹配（p.33 Fig. A5 规则 5），粒度差异可能造成 SEH/SRS 的跨系统不可比。
  (c) **默认配置差异**：系统按"默认用法"运行（p.17），检索深度以外的内部超参（如各系统自己的 top-k、消解策略、prompt 模板）未逐一对齐；文中未报告各系统的 token 消耗或 tool-call 次数，无法排除计算预算不均。
  (d) **oracle 差异**：金标准由构造过程定义并保证唯一（p.9 式 1），不存在外部 oracle；但 UOCS/CRS 的 u_i、o_i、c_i 判定同样经 LLM 判分（p.15 式 14–15；p.33 Fig. A5 规则 2–3），这些二值诊断位的判分噪声未单独报告。
  (e) **样本量**：12 个实例、平均 124.33 查询/实例（p.15–16），static 与 conditional 每实例平均仅 ~16.7 个查询；全文未报告方差、置信区间或显著性检验，表内四位小数差异（如 Table 4 中 Letta 平均 SEH@3 0.6202 vs MemOS 0.6710）的稳定性无法评估。
  (f) [OPEN_QUESTION] gpt-5.0-mini 未给出版本号/日期与供应商 API 细节；被测系统中哪些属于"需要 LLM 的后端"、哪些自带默认模型未逐一列明，无法完全排除个别系统实际调用配置不同。

4.3 [AUTHOR_FACT] 作者自己也提示了效率数字的解释边界："Low retrieval latency does not necessarily imply stronger retrieval quality"（p.26 §4.5.1），并指出 A-Mem 检索快是因为本地存储检索、Mem0 总时长被 addition 阶段主导（p.26 Table 6：Mem0 addition 40215.7970 秒、总计 41210.8349 秒；视觉核对）。

---

## 5. 作者明示限制、负向结果与未测试边界

5.1 作者明示限制（p.29 §5，逐条可定位）：
  (a) [AUTHOR_FACT] 基准来自受控模拟而非自然长期人机交互，"cannot fully represent the variability and ambiguity of real-world conversational memory"（p.29）。
  (b) [AUTHOR_FACT] 只覆盖时间更新、事实矛盾、条件偏好三类困难；"multimodal memory grounding, richer social interaction, or strategically omitted information are not explicitly modeled"（p.29）。
  (c) [AUTHOR_FACT] 被测系统集合有限；白盒协议假设支持金答案的记忆条目可被显式检索与排名，"may be difficult for opaque or proprietary memory systems in deployed settings"（p.29）。

5.2 负向/警示性结果（作者报告）：
  (a) [AUTHOR_FACT] CRS 对所有系统都很低，最好仅 0.2501（A-Mem）；Memobase static AA 相对高（0.4167）但 CRS 最低（0.0694）——"a system may return the correct stable value without explicitly recognizing the underlying contradiction"（p.19 §4.3.1 与 Table 3）。
  (b) [AUTHOR_FACT] static 冲突在平均 AA 上最难（p.18 §4.3.1 "static conflicts are the most difficult in terms of average AA"），在记忆层面 SEH@3/SRS 也普遍最低（p.20 §4.3.2）。
  (c) [AUTHOR_FACT] 更长历史使所有系统全部三个指标下降（p.21–22 §4.4.2，Fig. 5）；冲突距离增大（near 5–10 → far 20–25 个会话）使所有系统性能单调下降（p.24–25 §4.4.5，Fig. 7）；implicit query 普遍降低黑盒与白盒表现（p.24 §4.4.4，Table 5）。
  (d) [AUTHOR_FACT] Memobase 的 conditional SEH@K 与 SRS 在 K=2/3/5 下完全不变，说明瓶颈不是检索深度，而是条件相关记忆"可能根本不在可检索候选集中或未被记忆表示保留"（p.21 §4.4.1）。
  (e) [AUTHOR_FACT] 去掉干扰项后所有系统都改善，但系统间差距仍在——"they do not fully explain the performance gaps among memory systems"（p.23 §4.4.3，Fig. 6）。
  (f) [AUTHOR_FACT] LangMem 在 dynamic 冲突下 utilization failure 占比 53.9%，高于 retrieval failure 46.1%（p.27 Fig. 8，视觉核对），即"temporal updating remains difficult even when the relevant memory is available"（p.28）。
  (g) [AUTHOR_FACT] Mem0 平均 EUG 最小（0.0769）但作者明确警告这不是可靠性强的证据："a small gap may reflect fewer cases in which the gold memory item is retrieved"（p.27 Table 7 及正文）。

5.3 未测试边界（我的归纳）：
  (a) [READER_INTERPRETATION] 未测任何无记忆/全上下文/朴素 RAG 对照（同 3.3）。
  (b) [READER_INTERPRETATION] 未测多语言、多模态、多用户（作者列为未来工作，p.29）。
  (c) [READER_INTERPRETATION] 未报告跨随机种子/重复运行的方差；未报告人工核验统计；未报告 LLM 判分与人工判分的一致率。
  (d) [OPEN_QUESTION] "medium dialogue length"与"medium conflict distance"的默认设置只在 p.17 §4.2 一句带过（"direct queries, medium dialogue length, distractor injection, medium conflict distance"），medium 的精确 token/会话参数未给出（Table 2 的距离范围是总体范围，near/far 变体在 p.24 定义为 5–10/20–25，default 为"更宽范围采样"）。

---

## 6. 可抽取 Operator 与真实可记录 Failure

### 6.1 可抽取为 Operator（评测/构造侧模式，均有页码锚点）

  Op-1 [AUTHOR_FACT→可操作化] **查询时点算子**：在冲突引入会话被摄入后立即发问、以历史前缀为可用记忆（p.8 §3.1；p.13 §3.5），区别于"全部会话后统一发问"（p.6 Table 1 Timing 列）。可移植为任何流式记忆评测的干预时点设计。
  Op-2 [AUTHOR_FACT→可操作化] **两级评测算子**：AA（式 11）与 SEH@K/SRS（式 12–13）分离答案正确性与支持证据的可得性/排名（p.14 §3.6）。
  Op-3 [AUTHOR_FACT→可操作化] **EUG 诊断算子**：EUG = SEH@3 − AA，度量"检索到金记忆却答错"的利用缺口（p.27 §4.5.2 及 Table 7 Note "defined as the proportion of queries for which the gold memory item is retrieved but the final answer remains incorrect"）；配套把错误案例二分为 retrieval failure / utilization failure（p.27–28，Fig. 8）。
  Op-4 [AUTHOR_FACT→可操作化] **三类冲突构造算子**：dynamic（真实状态更新，后值有效）、static（后出现的假矛盾不得覆盖不变事实）、conditional（多值各在其条件下有效，查值问条件）（p.10–12 §3.3.2–3.3.4；构造规则 prompt 见 p.32 Fig. A2）。
  Op-5 [AUTHOR_FACT→可操作化] **干扰项注入算子**：从相关实体 R_u 选取语义相近但归属他人的信息，插入冲突跨度内的中间会话（式 6，p.12 §3.3.5），"increases retrieval and ranking difficulty while leaving the correct answer unchanged"。
  Op-6 [AUTHOR_FACT→可操作化] **冲突距离操纵算子**：以竞争候选间隔的会话数为可控难度旋钮（near 5–10 / far 20–25，p.24 §4.4.5）。
  Op-7 [AUTHOR_FACT→可操作化] **状态转移约束算子**：动态更新受 feasibility / cooldown / persona-consistency 约束与属性级更新权重控制（p.10 §3.3.2），属性级验证规则 V_d 过滤非法转移（式 5，p.11）。
  Op-8 [AUTHOR_FACT（作者建议，未实证）] **设计建议三件套**：记忆表示显式编码时间状态、来源归属、适用条件；conflict-aware reranking；生成前 memory-verification 步骤（p.28 §4.6）。注意：这些是从评测结果导出的建议，文中未实现或验证——引用时应标注为假设性 Operator。

### 6.2 真实可记录的 Failure（均为作者报告的具体失败证据）

  F-1 [AUTHOR_FACT] 所有 6 个系统的矛盾识别能力（CRS）≤0.2501；Memobase 仅 0.0694（p.19 Table 3）。
  F-2 [AUTHOR_FACT] LangMem 条件冲突崩溃：conditional AA 0.1556、SEH@3 0.2012（p.19 Table 3、p.20 Table 4）；Memobase conditional AA 0.2434、SEH@3 0.3021。
  F-3 [AUTHOR_FACT] Mem0 dynamic AA 仅 0.1224（六系统最低，p.19 Table 3），且对冲突距离与长历史最敏感（p.22 §4.4.2、p.25 §4.4.5）。
  F-4 [AUTHOR_FACT] LangMem dynamic 冲突中 53.9% 的失败是"检索到了却用错"（utilization failure）（p.27 Fig. 8）。
  F-5 [AUTHOR_FACT] Memobase conditional 检索瓶颈与 K 无关（K=2/3/5 不变，p.21 §4.4.1）——记忆写入/保留阶段的失败，而非检索深度失败。
  F-6 [AUTHOR_FACT] Mem0 写入成本失控：addition 40215.7970 秒，总运行时 41210.8349 秒，约为 MemOS（1356.3033 秒）的 30 倍（p.26 Table 6）。
  F-7 [AUTHOR_FACT] 检索失败在多数系统与冲突类型中占错误主导份额（如 Mem0 dynamic 91.4%、Memobase conditional 91.2%，p.27 Fig. 8；p.28 "retrieval failures account for the dominant share of errors"）。
  F-8 [READER_INTERPRETATION] 对 CRL 知识库而言，F-1 与 F-4 属于可复用的"失败模式"记录：答案正确 ≠ 冲突被识别（F-1），证据在场 ≠ 证据被用（F-4）；两者都只有在白盒/诊断指标存在时才可观测——这本身是记录该 Failure 的前提条件。

---

## 7. 判断-定位对照表（物理页码 / 章节 / 图表 / 短逐字定位语）

| # | 判断 | 物理页 | 章节/图表 | 逐字定位语（截短） |
|---|------|--------|-----------|-------------------|
| 1 | fitness-for-use 重构 | p.1, p.8 | 摘要; §3.1 | "query-conditioned fitness-for-use problem" |
| 2 | 三类冲突定义 | p.3, p.8 | Fig. 1; §3.1 | "Dynamic conflicts arise when a later true update supersedes" |
| 3 | 查询时点 | p.8, p.13 | §3.1; §3.5 | "issued immediately after the system ingests a session" |
| 4 | 时间线 2022–2025 按月 | p.10 | §3.3.1 | "spans January 2022 to December 2025" |
| 5 | 金标准唯一性 | p.9 | §3.1 式 1 | "guarantees a unique maximizer for each query" |
| 6 | 12 实例/规模统计 | p.15, p.16 | §3.7; Table 2 | "We constructed 12 benchmark instances" |
| 7 | 指标定义 AA/SEH/SRS/UOCS/CRS | p.14, p.15 | §3.6 式 11–15 | "Support Rank Score (SRS) assigns a logarithmically discounted score" |
| 8 | LLM 判分+人工核验 | p.15 | §3.6 | "LLM-assisted matching followed by human verification" |
| 9 | 六系统与统一接入 | p.16, p.17 | §4.1 | "all systems follow the same query protocol" |
| 10 | 统一模型 gpt-5.0-mini | p.18 | §4.2 末段 | "use gpt-5.0-mini" |
| 11 | 主结果黑盒 | p.19 | Table 3 | "MemOS achieves the highest average AA" |
| 12 | 主结果白盒 | p.20 | Table 4 | "MemOS achieves the highest average SEH@3 and SRS" |
| 13 | 检索深度敏感性 | p.20, p.21 | §4.4.1; Fig. 4 | "Memobase changes only slightly" |
| 14 | 长历史敏感性 | p.21, p.22 | §4.4.2; Fig. 5 | "Longer histories reduce performance for all evaluated systems" |
| 15 | 干扰项敏感性 | p.22, p.23 | §4.4.3; Fig. 6 | "Removing distractors improves performance for all systems" |
| 16 | implicit query 敏感性 | p.24 | §4.4.4; Table 5 | "implicit queries generally reduce both black-box and white-box" |
| 17 | 冲突距离敏感性 | p.24, p.25 | §4.4.5; Fig. 7 | "Performance decreases as conflict distance increases" |
| 18 | 效率结果 | p.26 | §4.5.1; Table 6 | "Mem0 has by far the highest total runtime" |
| 19 | EUG 与失败分解 | p.27, p.28 | §4.5.2; Table 7; Fig. 8 | "the difference between SEH@3 and AA" |
| 20 | 设计建议 | p.28 | §4.6 | "conflict-aware reranking mechanisms" |
| 21 | 作者限制 | p.29 | §5 | "controlled simulation rather than collected from naturally occurring" |
| 22 | Prompt 模板 | p.32, p.33 | Appendix A, Fig. A1–A5 | "condensed from the implementation prompts for readability" |
| 23 | arXiv 标识 | p.1 | 首页水印 | "arXiv:2605.20926v1 [cs.IR] 20 May 2026" |

---

## 8. 解析文本与可视 PDF 是否冲突（就抽查过的页面）

8.1 [AUTHOR_FACT/核验结论] 我对 p.6（Table 1）、p.16（Table 2）、p.18（§4.2 设置段 + Fig. 3）、p.19（Table 3）、p.20（Table 4）、p.26（Table 6）、p.27（Table 7 + Fig. 8）做了 150dpi 渲染视觉核对：所有抽查数值（含加粗最优标记）与 PyMuPDF 解析文本一致，未发现冲突。特别核对点：
  (a) p.18 等宽字体确为 "gpt-5.0-mini"（非 gpt-4o-mini 之类的解析讹误）。
  (b) p.19 Table 3 加粗：A-Mem CRS 0.2501、LangMem dynamic AA 0.4966、MemOS 的 UOCS/static AA/conditional AA/平均 AA——与解析文本数值一致。
  (c) p.27 Fig. 8 条形图百分比（如 LangMem dynamic 46.1%/53.9%、Mem0 dynamic 91.4%/8.6%、Memobase conditional 91.2%/8.8%）与解析文本一致。

8.2 [READER_INTERPRETATION] 解析文本在图页（p.21 Fig. 4、p.22 Fig. 5、p.23 Fig. 6、p.25 Fig. 7、p.8 Fig. 2、p.18 Fig. 3）呈现为坐标轴刻度与数值的碎片化列表，属正常抽取顺序伪影，不构成内容冲突；正文引用的关键数值（如 Letta SEH@K 0.5239→0.7251、MemOS K=5 时 0.7280/0.6123）在图与正文中互相印证。

8.3 [READER_INTERPRETATION] 唯一的"表观矛盾"是 ACM 模板占位符：页脚 "J. ACM, Vol. 37, No. 4, Article 111... August 2018"、版权行 "© 2018"、DOI "XXXXXXX.XXXXXXX"、p.32 "Received 20 February 2007; revised 12 March 2009; accepted 5 June 2009"，均与 arXiv 2026-05-20 的时间戳不符。这是未清理的 ACM 模板默认值（canonical metadata 亦标注 "preprint (ACM template)"），不是内容错误，但引用出版信息时不得使用这些占位符。

8.4 [OPEN_QUESTION] 论文 p.1 声称 "Source code and dataset are available at GitHub"（脚注 1：github.com/TaoZhen1110/MemConflict），本次核源仅限本地 PDF，未验证该仓库的存在性与内容一致性。

---

## 9. 残余开放问题汇总（供 reconciliation）

  OQ-1 [OPEN_QUESTION] "medium" 对话长度与 "default" 冲突距离的精确参数未在文中给出（p.17 §4.2 仅命名；p.24 仅给 near/far 区间）。
  OQ-2 [OPEN_QUESTION] 人工核验的标注人数、核验覆盖率、LLM-人工一致率均未报告（p.13、p.15 仅定性描述）。
  OQ-3 [OPEN_QUESTION] 各系统 token/tool-call 开销、内部默认超参未报告，效率表（Table 6）未说明硬件/并发条件，跨系统时间可比性存疑。
  OQ-4 [OPEN_QUESTION] 无重复运行方差/显著性检验；static/conditional 子集每实例平均仅约 16.7 个查询，小样本下表间四位小数差异的稳健性未知。
  OQ-5 [OPEN_QUESTION] gpt-5.0-mini 的具体版本/日期未标注；哪些被测系统实际消费该模型作为后端未逐一列明。
  OQ-6 [OPEN_QUESTION] 白盒协议对不同记忆粒度系统的 "gold memory item" 匹配是否存在系统性偏置，文中无校准实验。

（报告完）
