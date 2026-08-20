# P010 独立二读报告

## 0. 任务身份与来源边界

- [AUTHOR_FACT] 论文题名为 *LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory*，发表于 ICLR 2025。定位：PDF p.1，首页标题与页眉，短定位文本“Published as a conference paper at ICLR 2025”。
- [AUTHOR_FACT] 本次读取所用 PDF 的实际 SHA-256 为 `c6c6d75072d316d7b040dbbbb9caf7607821e6dd34d986e6f6c7e3e1721179f7`，与 invocation 中冻结值一致。定位：`r2-20260719-p010-a1/invocation.md` 的 “PDF SHA-256”。
- [AUTHOR_FACT] 本报告遵循冻结的 invocation snapshot：`knowledge_base/pilot/reads/P010/read_2_attempts/r2-20260719-p010-a1/invocation.md`。输入隔离性质是 `procedural_blinding`，不是平台可验证的文件级技术隔离。定位：invocation 的 “Read boundary”。
- [READER_INTERPRETATION] 本报告是 fresh 独立核源结果，仅回答统一问题清单；不生成 Card，不合并其他读者结论，不作 Candidate 评价。

## 1. 论文研究对象与评价任务

- [AUTHOR_FACT] LONGMEMEVAL 用四元组 `(S, q, t_q, a)` 表示实例：`S=[(t_1,S_1),...,(t_N,S_N)]` 是按时间排列的多轮会话序列；测试时各会话逐个提供给系统；问题 `q` 在全部历史之后、日期为 `t_q>t_N`；答案 `a` 是短语或开放问题的自然语言 rubric。定位：PDF p.4，§3.1，短定位文本“The evaluation of LONGMEMEVAL requires an instance of 4-tuple”。
- [AUTHOR_FACT] 基准包含 500 个经人工构造的问题，覆盖五类长期记忆能力：信息抽取、跨会话推理、知识更新、时间推理和拒答；细分为七种问题类型。定位：PDF pp.2,4，§3.2；Figure 1；短定位文本“five core long-term memory abilities”。
- [AUTHOR_FACT] 两个标准历史规模是 LONGMEMEVALS（约 115k tokens/问题）和 LONGMEMEVALM（500 sessions，约 1.5M tokens）。定位：PDF pp.2,5，§3.2，短定位文本“two standard settings”。
- [AUTHOR_FACT] 问题由人工专家筛选、重写并分解为证据陈述；证据会话由 LLM 自对话生成后人工筛改；无关会话来自 ShareGPT、UltraChat 与其他不冲突的模拟会话。定位：PDF pp.5,18–19，Figure 2，Appendix A.1–A.2，短定位文本“human experts manually filter and rewrite all the questions”。
- [AUTHOR_FACT] 历史混合比例固定为 25% ShareGPT、25% UltraChat、50% 模拟会话；若没有预定义时间锚点，时间戳随机分配在 2023 年 5 月。定位：PDF p.19，Appendix A.2，“Session sampling”“Timestamp resolution”。
- [READER_INTERPRETATION] 该基准主要测量在大量无关但形式相似的会话中定位、组合与更新少量人工指定证据的能力；它比纯粹的自由对话长期人格一致性更接近“带时间元数据的个性化多会话 QA”。依据：PDF pp.4–5，§3.1–3.2，Figure 2。
- [OPEN_QUESTION] 论文没有报告对自然发生、未经 LLM 模拟与人工修订的长期用户历史做同等规模验证；因此从该构造分布外推到真实长期交互的程度无法由本文确定。定位：PDF pp.5,17–19，Figure 2，Appendix A.1–A.2。

## 2. 方法究竟改变哪一步计算

### 2.1 统一执行框架

- [AUTHOR_FACT] 作者把记忆增强助手分为三阶段：索引（把每个历史会话转成一个或多个 key-value 项）、检索（构造查询并取最相关的 `k` 个项）、阅读（LLM 读取检索结果并生成回答）；四个控制点是 Value、Key、Query 和 Reading Strategy。定位：PDF p.7，§4.1，Figure 4，短定位文本“three stages and four control points”。
- [AUTHOR_FACT] 附录形式化了 `I/Q/S/R`：索引函数、查询构造函数、显著性排序函数和阅读函数；`I_online` 可以在新会话到来时增删改 datastore 中的项目。定位：PDF p.22，Appendix C.1，短定位文本“four functions: I, Q, S, R”。
- [READER_INTERPRETATION] 论文的核心技术贡献不是训练一个新的端到端记忆模型，而是在既定 RAG 式三阶段流水线上改变数据单元、检索表示、时间过滤和阅读提示。

### 2.2 Value：存储粒度/表示

- [AUTHOR_FACT] 作者比较整 session、拆成 round、session summary、session facts、round facts；将 session 拆成 round 对 GPT-4o 阅读器显著改善 QA，而 summary/fact 替换原文总体上因信息损失降低 QA；multi-session 子集是例外，fact decomposition 持续改善。定位：PDF pp.8–9，§5.2，Figure 5，短定位文本“replacing sessions or rounds with extracted summaries or facts negatively impacts QA performance”。
- [AUTHOR_FACT] 索引抽取统一用 Llama 3.1 8B Instruct，并且 session/round 作为 key 时只保留用户侧 utterance；压缩实验也只向抽取器提供用户消息。定位：PDF pp.8,23–24，§5.1，Appendix D，Figure 11。
- [READER_INTERPRETATION] Value 操作改变的是进入索引与后续阅读的原子记忆单元：`session -> rounds`，或进一步 `text -> summary/facts`；前者减少单项主题混杂，后者以信息丢失换取更统一、更短的表示。

### 2.3 Key：事实增强的索引键

- [AUTHOR_FACT] 压缩表示单独作为 key（fact/keyphrase/summary）通常不优于 `K=V`；作者最终采用索引阶段的 document expansion，把抽取出的用户 facts 与原始 value 直接拼接为 key，即 `K=V+fact`。定位：PDF p.9，§5.3，Table 3，短定位文本“compressed information is concatenated with the original value”。
- [AUTHOR_FACT] `K=V+fact` 相对相应 `K=V`，作者汇总称 Recall@k 平均提升 9.4%，最终准确率跨模型平均提升 5.4%。定位：PDF p.9，§5.3。
- [AUTHOR_FACT] 把抽取信息另建并行 key、再在检索后做 rank merging 的方案表现低于 key merging；作者推测原因是索引规模增加约 `m+1` 倍。定位：PDF pp.26–27，Appendix E.3，Table 10，短定位文本“rank merging has much lower performance than key merging”。
- [READER_INTERPRETATION] 这里的“multi-pathway”并非最终采用多个独立索引再融合，而是让同一向量键同时含原文和抽取事实，从而在不复制 value 的情况下突出事实语义。

### 2.4 Query：时间感知索引与检索范围过滤

- [AUTHOR_FACT] 索引阶段由 Llama 3.1 8B 抽取可推断日期的事件；检索阶段由模型 `M_T` 从时间敏感问题中抽取起止日期，并用该范围过滤大量无关 value。定位：PDF pp.9,23–24，§5.4，Appendix D，Figure 12。
- [AUTHOR_FACT] 在 temporal-reasoning 子集上，使用 GPT-4o 做时间范围抽取时，作者报告 round value 平均 recall 提升 11.3%，session value 提升 6.8%；Llama 3.1 8B 会在无显式时间范围的问题上产生假阳性范围并错误裁剪搜索空间。定位：PDF pp.9–10,27–28，§5.4，Table 4，Appendix E.4，Table 11。
- [READER_INTERPRETATION] Query 操作改变的是检索候选集，而不只是 query embedding：先判断是否存在可安全推断的时间范围，再以硬过滤限制相似度检索域。

### 2.5 Reading：结构化输入与先抽取后推理

- [AUTHOR_FACT] 作者把召回项表示为 JSON，并用 Chain-of-Note 提示先逐项抽取证据、再基于 notes 推理；生成采用 greedy search，最大 800 tokens。定位：PDF pp.10,23,25，§5.5，Appendix D，Figure 13。
- [AUTHOR_FACT] 在只提供证据 session 的 oracle retrieval 设置下，JSON+CoN 是 Figure 6 中三个阅读器的最佳组合；对 GPT-4o，较差阅读策略相对最佳方案最多差约 10 个绝对准确率点。定位：PDF p.10，§5.5，Figure 6。
- [AUTHOR_FACT] JSON 在没有 CoN 时并不稳定优于自然语言；在 LONGMEMEVALS 全历史直接阅读的 pilot 中，CoN 还使 Llama 3.1 70B 从 0.334 降到 0.286、Llama 3.1 8B 从 0.454 降到 0.420。定位：PDF pp.6,10，Figure 3b、Figure 6。
- [READER_INTERPRETATION] CoN/JSON 的增益依赖输入组织、上下文长度和 reader；不能把 oracle 证据上下文上的正增益无条件外推为超长全历史上的普适增益。

## 3. 输入、输出、可用信息与干预时点

- [AUTHOR_FACT] 在线输入是带 session timestamp 的用户—助手多轮历史，按时间逐 session 到达；问题和问题日期在全部历史之后到达。定位：PDF p.4，§3.1。
- [AUTHOR_FACT] 索引时可使用当前 session/round 的用户侧文本与 session 日期；事实、摘要、关键词和 timestamped events 均由 Llama 3.1 8B Instruct 抽取。定位：PDF pp.8,23–24，§5.1，Appendix D，Figures 11–12。
- [AUTHOR_FACT] 检索时可使用问题文本与 current/question date；时间扩展模型输出起止范围或 N/A。定位：PDF p.24，Figure 12。
- [AUTHOR_FACT] 阅读时可使用 top-k recalled items、各项时间信息、current date 和 question；检索项始终按 timestamp 排序。定位：PDF pp.8,25，§5.1，Figure 13。
- [AUTHOR_FACT] 最终输出是自然语言答案；评测同时可计算 QA 正确率，若系统暴露检索结果则计算 Recall@k 与 NDCG@k。定位：PDF pp.5–6，§3.3。
- [READER_INTERPRETATION] 四个实际干预时点分别是：会话到达时决定 value 切分；写入索引前扩展 key/事件日期；问题到达后做时间范围过滤和相似度召回；回答生成前做排序、JSON 编排和 CoN 阅读。
- [OPEN_QUESTION] 虽然框架允许 `I_online` 删除或编辑旧记忆，本文优化实现没有展示一个可执行的知识删除/冲突合并算子，也没有报告在线索引维护的延迟或成本。定位：PDF pp.11,22–24，Ethics Statement、Appendix C.1、Appendix D。

## 4. 最强基线与最接近组合基线

- [AUTHOR_FACT] 长上下文直接阅读（LC）是无显式记忆操作的基线，oracle sessions（只给证据会话）是诊断性上界，不是可部署检索基线。定位：PDF pp.6,26，Figure 3b，Table 8。
- [AUTHOR_FACT] 对 key 扩展最接近的单变量基线是相同 value、retriever、reader、top-k 与读取设置下的 `K=V`。例如 Table 3 中 round value：`K=V` 的 Recall@10=0.692，`K=V+fact`=0.784；GPT-4o Top-10 QA 从 0.670 到 0.720。定位：PDF p.9，Table 3。
- [AUTHOR_FACT] 在 Table 3 的未扩展简单索引中，session `K=V` 的检索分数高于 round `K=V`（Recall@5 0.706 vs 0.582；Recall@10 0.783 vs 0.692），且 GPT-4o Top-5 QA 为 0.670；但不同 reader/top-k 下 QA 强弱不一致。定位：PDF p.9，Table 3。
- [AUTHOR_FACT] 时间扩展最接近的基线是相同 key 设置下的无 Query Expansion 行；Table 4 分别在 `K=V` 与 `K=V+fact` 上做了该对照。定位：PDF p.10，Table 4。
- [AUTHOR_FACT] 阅读策略的最接近组合基线是 Figure 6 的 2×2 组合：NL/JSON × Direct/CoN；最佳报告组合为 JSON+CoN。定位：PDF p.10，Figure 6。
- [AUTHOR_FACT] 作者在最终 error analysis 中采用的“best memory design”是 round value、`K=V+fact`、Stella V5 1.5B、top-10、JSON+CoN。定位：PDF pp.27–28，Appendix E.5，Figure 14。
- [READER_INTERPRETATION] 若问“最强基线”，必须按比较对象拆开：LC 是系统级无记忆基线，oracle 是不可部署诊断上界，session/round `K=V` 是索引级强基线，NL/JSON+Direct/CoN 是阅读级组合基线。论文没有给出一张把所有新增组件逐步累加、保持其余条件完全相同的端到端总消融表。
- [OPEN_QUESTION] 时间过滤只在 temporal-reasoning 子集报告 retrieval 指标，未给出其与 round+fact+JSON+CoN 全组合的统一总体 QA 增益；因此无法从本文精确分解完整系统中每个组件的边际贡献。定位：PDF pp.9–10，Tables 3–4，Figure 6。

## 5. 模型、token、tool-call、prompt 与 oracle 差异

- [AUTHOR_FACT] 主实验 reader 为 GPT-4o、Llama 3.1 70B Instruct、Llama 3.1 8B Instruct；retriever 为 Stella V5 1.5B；索引抽取器为 Llama 3.1 8B。定位：PDF p.8，§5.1。
- [AUTHOR_FACT] 时间范围抽取使用 GPT-4o 时增益明显，而 Llama 3.1 8B 可能降低或仅有限改善 recall。定位：PDF pp.9–10,27–28，Table 4、Table 11。
- [READER_INTERPRETATION] 时间感知设计的收益部分依赖额外调用一个强模型；若生产系统只能使用较弱抽取器，结果不能按 GPT-4o 行复现。这属于模型/额外推理调用差异，而非纯数据结构增益。
- [AUTHOR_FACT] Figure 5 做 token-budget-aware 比较：Llama 3.1 8B 在检索文本超过约 3k tokens 后性能陡降，GPT-4o 在超过 20k tokens 时仍改善。定位：PDF pp.8–9，Figure 5 与 §5.2。
- [READER_INTERPRETATION] round/session/value 压缩同时改变 item 数量与每项长度；top-5/top-10 又改变 reader token 总量，因此某些 QA 差异可能包含 token budget 和 reader context tolerance 的作用。
- [AUTHOR_FACT] §5.2–§5.4 默认都使用 CoN+JSON，检索项也始终按 timestamp 排序。定位：PDF p.8，§5.1，短定位文本“Throughout §5.2 to §5.4, we apply Chain-of-Note and json format by default”。
- [READER_INTERPRETATION] Value/Key/Query 实验是在已强化 reading prompt 和固定时间排序下测得；这有利于受控比较，但不能把表中结果理解为不依赖 prompt/format 的孤立收益。
- [AUTHOR_FACT] QA 由 `gpt-4o-2024-08-06` 充当 judge；meta-evaluation 平均与人类判断一致率约 0.98/0.97，但 single-session-preference 与 abstention 的某些设置只有 0.90。时间问题还允许天数 off-by-one。定位：PDF pp.6,20–21，§3.3，Appendix A.4，Figure 10，Table 6。
- [READER_INTERPRETATION] 报告准确率包含 LLM judge 的剩余误差，尤其开放个性化回答和拒答；时间题的宽容规则也会影响可比性。
- [AUTHOR_FACT] 商业系统实验仅随机选 97 题、使用 3–6 个 sessions（约比 LONGMEMEVALS 短 10 倍），由人通过网页逐轮输入；跳过一部分 temporal、全部 single-session-assistant 和 abstention。定位：PDF pp.6,21，§3.4，Appendix B。
- [READER_INTERPRETATION] 商业系统与 offline GPT-4o 的比较存在界面、隐藏记忆机制、会话输入方式、可回答题型和上下文提供方式差异，不能视为只改变“有无记忆模块”的严格等模型实验。
- [AUTHOR_FACT] oracle retrieval 只给 evidence sessions，而真实检索需从完整 history 找到它们。定位：PDF pp.6,10，Figure 3b，§5.5。
- [READER_INTERPRETATION] oracle 结果用于分离 reading error 很有价值，但若拿它与完整历史/在线系统直接相减，差值同时混合检索难度、无关上下文干扰和输入 token 差异。

## 6. 作者明示限制、负向结果与未测试边界

### 6.1 明示负向结果

- [AUTHOR_FACT] 将 session/round 压缩成 summary 或 facts 总体损害 QA，作者归因于信息损失；仅 multi-session 子集受益于 fact decomposition。定位：PDF pp.8–9，§5.2，Figure 5。
- [AUTHOR_FACT] summary/fact/keyphrase 单独充当 key 通常不优于 `K=V`；最有效的是保留原 value 并拼接 fact。定位：PDF p.9，§5.3，Table 3。
- [AUTHOR_FACT] 检索后 rank merging 明显低于索引时 key merging。定位：PDF pp.26–27，Appendix E.3，Table 10。
- [AUTHOR_FACT] 弱时间抽取器会把没有可安全限定范围的问题误判成有时间范围并剪掉正确证据。定位：PDF pp.27–28，Appendix E.4，Table 11。
- [AUTHOR_FACT] 即使 Recall@10 正确，仍有约 15%–19% 的全部实例生成错误；在所有错误中约 40%–50% 属于“召回正确、生成错误”。定位：PDF pp.27–28，Appendix E.5，Figure 14。
- [AUTHOR_FACT] 商业系统中，Coze 常漏记间接提供的信息，ChatGPT 会在后续压缩历史时修改/覆盖关键事实。定位：PDF pp.6,21，§3.4，Appendix B。

### 6.2 明示风险/限制

- [AUTHOR_FACT] 作者明确指出存储和召回用户信息可能泄露个人信息，缺少 memory deletion operator 会损害可信度，恶意内容可能污染 datastore 并诱发 jailbreak；建议监控记忆读写流。定位：PDF p.11，Ethics Statement，短定位文本“lack of a memory ‘deletion’ operator”。
- [AUTHOR_FACT] 复杂层级/图索引可能需要新会话到来后的重索引，增加在线计算开销；交互式检索/阅读也增加 LLM 推理延迟。定位：PDF p.22，Appendix C.2。
- [AUTHOR_FACT] 作者没有比较更大的 embedding retriever，理由是其延迟通常不适合真实应用。定位：PDF p.26，Appendix E.2。

### 6.3 本文未解决或未充分测试

- [OPEN_QUESTION] 没有置信区间、显著性检验或多随机种子方差，表格中数值差异的统计稳定性无法从论文判断。定位：PDF pp.8–10,26–28，Figures 5–6，Tables 3–4、8–10。
- [OPEN_QUESTION] 没有量化索引抽取、GPT-4o 时间查询扩展、JSON+CoN 长生成和 top-k 阅读的端到端延迟、美元成本、吞吐或增量存储成本。定位：PDF pp.8–10,23–27，§5 与 Appendices D–E。
- [OPEN_QUESTION] 没有展示用户主动删除、隐私请求、恶意记忆注入、冲突事实合并或长期索引漂移的实验。定位：PDF p.11，Ethics Statement。
- [OPEN_QUESTION] 数据以属性本体、模拟会话和人工证据为核心；跨语言、跨文化、语音/多模态、真实长周期时间漂移和多人共享账户均未报告。定位：PDF pp.17–19，Appendix A。
- [OPEN_QUESTION] 图 5 只展示曲线，没有提供每个 token budget 的逐点表格，因此无法仅据 PDF 精确复核所有曲线数值。定位：PDF p.8，Figure 5。
- [OPEN_QUESTION] “500 sessions ≈1.5M tokens”衡量上下文深度，但没有报告每种问题类型在两个标准规模上的独立置信区间及数据泄漏/训练集污染检测。定位：PDF pp.2,5,19，§3.2，Appendix A.3。
- [OPEN_QUESTION] 检索项固定按时间排序本身可能帮助时间/更新题，但论文未提供“排序 vs 不排序”的单独消融。定位：PDF p.8，§5.1。

## 7. 可抽取的 Operator 与真实可记录的 Failure（仅核源，不作 Candidate 评价）

### 7.1 Operator 级机制

- [READER_INTERPRETATION] `RoundDecompose`：在索引前把多轮 session 拆为 user-assistant round，以减少单个 value 的主题混杂。核源：PDF pp.7–9，§4.2 CP1、§5.2，Figure 5。
- [READER_INTERPRETATION] `FactAugmentedKey`：用 Llama 3.1 8B 抽取 user facts，并在索引阶段构造 `key = facts || original value`；value 仍指向原始 round/session。核源：PDF pp.9,23–24，§5.3，Appendix D，Table 3，Figure 11。
- [READER_INTERPRETATION] `TimeAwareCandidateFilter`：索引时抽取 dated events；查询时仅在可推断安全时间范围时输出 `[start,end]` 并过滤候选，否则返回 N/A。核源：PDF pp.9–10,23–24,27–28，§5.4，Figure 12，Table 11。
- [READER_INTERPRETATION] `ChronologicalStructuredRead`：把 top-k 项按 timestamp 排序并编码为 JSON。核源：PDF pp.8,10，§5.1、§5.5。
- [READER_INTERPRETATION] `ExtractThenReason`：先逐项抽取相关信息，再对 notes 推理并回答。核源：PDF pp.10,25，§5.5，Figure 13。
- [READER_INTERPRETATION] `JudgeWithTypeSpecificRubric`：按 question type 切换 judge prompt，并为时间天数设置 off-by-one 宽容。该项属于评测 Operator，不属于记忆系统 Operator。核源：PDF pp.20–21，Appendix A.4，Figure 10。

### 7.2 Failure 级现象

- [AUTHOR_FACT] `CoarseValueFailure`：整 session 作为单项会妨碍有效检索/阅读，round decomposition 在 GPT-4o reader 上改善。定位：PDF pp.7–9，CP1、§5.2，Figure 5。
- [AUTHOR_FACT] `OverCompressionInformationLoss`：只存 summary/facts 会丢失细节并降低总体 QA。定位：PDF pp.7–9，CP1、§5.2。
- [AUTHOR_FACT] `CompressedKeyOnlyRecallLoss`：fact/keyphrase/summary 单独作 key 未提升、常降低 recall。定位：PDF p.9，§5.3，Table 3。
- [AUTHOR_FACT] `TemporalFilterFalsePositive`：弱 `M_T` 对无时间范围问题虚构范围，错误裁剪证据。定位：PDF pp.27–28，Appendix E.4，Table 11。
- [AUTHOR_FACT] `CorrectRetrievalWrongGeneration`：top-10 召回正确后，reader 仍可能生成错答，占全部样本约 15%–19%。定位：PDF pp.27–28，Appendix E.5，Figure 14。
- [AUTHOR_FACT] `OnlineMemoryOverwrite`：ChatGPT 在后续压缩历史时修改先前记录的信息。定位：PDF pp.6,21，§3.4，Appendix B。
- [AUTHOR_FACT] `IndirectEvidenceRecordingMiss`：Coze 常未记录间接表达的用户信息。定位：PDF pp.6,21，§3.4，Appendix B。
- [AUTHOR_FACT] `RankMergingIndexExplosion`：并行 key + 后融合增大索引且实测低于 key merging。定位：PDF pp.26–27，Appendix E.3，Table 10。
- [READER_INTERPRETATION] 上述 Failure 均有论文内证据；“为何发生”的机制解释中，信息损失、索引膨胀和 reader 容量等部分仍是作者假设或读者解释，不应提升为已被因果验证的事实。

## 8. 解析文本与可视 PDF 核验

- [AUTHOR_FACT] PDF 共 28 页；已按 PDF physical page 1–28 逐页抽取文本，并对同一 28 页逐页内存渲染后以 4 页拼图方式做版面核验。
- [READER_INTERPRETATION] 未发现标题、章节顺序、表格/图编号、提示词框、页码或正文段落在解析文本与可视版面之间存在明显冲突。Figure 1–14、Table 1–11 与 Appendix A–E 的版面位置均与解析结果相符。
- [READER_INTERPRETATION] 表格抽取为线性阅读顺序，列结构需要结合可视版面恢复；本报告引用的关键数字已对照对应可视表格页进行结构核验。
- [OPEN_QUESTION] 可视核验使用逐页缩略渲染检查整体版面，并非对每个字符做独立 OCR；图 5 曲线等纯图形信息无法从解析文本恢复精确逐点值，论文正文也未提供这些点值表。

## 9. Provenance、实际读取文件与可观察 trace

### 9.1 实际读取文件（仅以下三项）

1. `D:/Desktop/crl_judge/crl_agent_v3/knowledge_base/staging/papers/P010_longmemeval.pdf`
2. `D:/Desktop/crl_judge/crl_agent_v3/knowledge_base/templates/second_read_prompt.md`
3. `D:/Desktop/crl_judge/crl_agent_v3/knowledge_base/pilot/reads/P010/read_2_attempts/r2-20260719-p010-a1/invocation.md`

### 9.2 实际使用的本地工具

- PowerShell `Get-Content -LiteralPath -Raw -Encoding UTF8`：读取 prompt 与 invocation。
- PowerShell `Get-FileHash -Algorithm SHA256`：核验 PDF 哈希。
- `pdfinfo`：尝试读取 PDF 元数据，但环境返回“The system cannot find the path specified”，未成功；未据此声称任何结果。
- Python 3 + PyMuPDF (`fitz`)：直接打开指定 PDF，读取 28 页页数/元数据，按 physical page 逐页提取全文。
- Python 3 + PyMuPDF + Pillow：在内存中渲染页面与生成缩略拼图；未落盘任何中间图片。
- Codex 工具编排层的 shell 调用与图像查看输出：用于接收本地解析文本和查看内存渲染结果。

### 9.3 可观察异常与重试

- 初次抽取 PDF p.1 时，Windows GBK 标准输出无法编码字符 `U+2217`，进程在正文输出前报 `UnicodeEncodeError`；随后仅在 Python 进程内将 stdout 设为 UTF-8，重新成功抽取。
- 第一次图像 data URL 传递方式未被平台处理；改用结构化 `image_url` 后成功查看。一次尝试同时传两张拼图也未被处理，随后按单张拼图逐次查看。
- 除指定 `report.md` 外，没有写入临时文本、图像或其他产物；没有联网。

### 9.4 平台无法观察或无法技术证明的 trace

- Actual model/version：`unknown`。会话将角色呈现为 Codex/GPT 系列代理，但平台未向本读者暴露可核验的精确部署版本号，因此不作猜测。
- Canonical agent task：可观察为 `/root/p010_second_read`；上层 Codex desktop thread ID 不可见，记为 `unavailable`。
- File-level allowlist：`unavailable`；隔离仅由任务约束执行，性质为 `procedural_blinding`，不能声称技术 read-only 或技术文件隔离。
- 平台级、内核级或宿主进程级完整 file-access audit：`unavailable`；本节只能报告本代理显式发起且可观察的文件/工具调用。

## 10. 二读摘要（不作裁决）

- [READER_INTERPRETATION] 论文最清晰的机制链条是：`session -> round value`，`K=V -> K=V+fact`，时间问题上增加日期事件索引与安全时间范围过滤，最后用时间排序的 JSON+CoN 阅读。其证据分别来自 Figure 5、Table 3、Table 4 和 Figure 6，而不是一个统一的全组件端到端累加消融。
- [READER_INTERPRETATION] 最可靠的负向证据同样重要：过度压缩会丢信息、压缩 key 单独使用不强、rank merging 更差、弱时间模型会误剪枝、正确召回后仍有显著生成错误。
- [OPEN_QUESTION] 若要后续 reconciliation，最需要保持的边界是：oracle 与真实系统不可混同；GPT-4o 时间抽取的额外模型成本不可隐藏；§5.2–§5.4 已默认叠加 CoN+JSON 和时间排序；商业系统实验不是完整 LONGMEMEVAL 标准设置。
