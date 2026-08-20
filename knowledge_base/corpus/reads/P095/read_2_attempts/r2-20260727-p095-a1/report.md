# P095 独立二读报告（fresh 读者 / W06 扩充波次）

## 0. 报告头部与核源方式

- 读者标识：r2-20260727-p095-a1（独立二读；未读取 read_1.md、任何 reconciliation、任何 Card、任何其他读者材料）
- 报告日期：2026-07-27
- canonical metadata（任务给定）：Don't Ask the LLM to Track Freshness, arXiv 2606.01435v1 (2026-05-31), preprint
- PDF 路径：D:\Desktop\crl\crl_agent_v3\knowledge_base\staging\w06_targeted\P095_deterministic_freshness.pdf
- 实测 SHA-256：60f5542186d6e629e00885922dd57ee18e55f7775932c6991c2d76796c75b4a1（与任务给定值一致）
- 实测物理页数：29
- 抽取方式：python + PyMuPDF 逐页全文抽取；另对 p1、p3、p11、p14、p15、p18、p19、p27 做 110dpi 渲染视觉抽查（含全部关键表格页）。
- 页码约定：论文页脚印刷页码与物理页码一致（如物理第 14 页页脚为 "14"），下文所有页码均为物理页码。
- [AUTHOR_FACT] p1 标题为 "Don't Ask the LLM to Track Freshness: A Deterministic Recipe for Memory Conflict Resolution"，作者 Vikas Reddy 与 Sumanth Challaram，右侧竖排 "arXiv:2606.01435v1 [cs.AI] 31 May 2026"，与 canonical metadata 一致。

---

## 1. 方法究竟改变哪一步计算？

1.1 [AUTHOR_FACT] 被改变的是检索之后的"答案组装（assembly）"一步：把"LLM 自由文本一步完成过滤+新鲜度判断+作答"替换为"LLM 结构化候选抽取 + Python max(serial) 确定性挑选"。定位：p1 摘要 "replacing the LLM-judgment-based answer pipeline with a candidate-extraction + Python max(serial) pipeline"；p4 §1.4 "the bottleneck ... is assembly (post-retrieval aggregation), not storage"。

1.2 [AUTHOR_FACT] 单跳 SH-conflict 管线三步（p9 §3.1）：(1) BM25 检索 top-k=10；(2) LLM 候选抽取，输出 JSON 列表 {serial, text, entity}，prompt 明确要求包含所有匹配项、"do not compare serials, do not pick a 'best'"、verbatim 抽取；(3) 新鲜度挑选 argmax serial，候选集为空则返回 "no answer"。整个管线 "≈50 lines of Python"（p9）。

1.3 [AUTHOR_FACT] 多跳 CAR（Chain-Aware Resolution，p9–10 §3.2）：Self-Ask 式分解为原子 hop（{hop_k_answer} 占位符串链），每个 hop 内运行同一 SH-conflict 原语；任一中间 hop 返回 "no answer" 则断链，返回最后有效答案或 "no answer"。分解 prompt 带 HARD_CONSTRAINT：每 hop 至多一个关系词（p10 "forbids more than one relationship word per hop"）。

1.4 [AUTHOR_FACT] 存储与检索本身不变：无向量库、无图库、无 embedding 模型，依赖仅 openai、rank_bm25、datasets（p11 §3.4）。

1.5 [READER_INTERPRETATION] 干预的实质是把"版本比较"这一个子计算从 LLM 前向传播中整体移出到确定性代码，并同步把 LLM 的任务从 decide-and-answer 收窄为 extract-candidates；这两件事在本文中是绑定发生的（见第 3、4 节的混杂讨论）。

## 2. 输入、输出、可用信息与干预时点

2.1 [AUTHOR_FACT] 输入：带编号事实语料 C={(s_i, t_i)}（s_i 为整数版本序号、t_i 为事实文本）与查询 q（p9 §3.1）；数据为 MAB FactConsolidation（MQUAKE 反事实改写，原事实与反事实按序拼接、反事实序号更高），4 个上下文长度 6K/32K/64K/262K，每 cell n=100（p11 §4.1）。

2.2 [AUTHOR_FACT] fact-level chunking 用正则 (\d+)\.\s+(.+?)(?=\d+\.\s|$) 逐条切分，每事实一 chunk（p12 §4.4）；对照 chunk-4096 为 4096 字符滑窗。

2.3 [AUTHOR_FACT] 输出：短实体答案（从抽取候选中取 max serial 者的 entity）或 "no answer"；CAR 输出末 hop 答案（p9–10）。评测指标 SubEM（大小写不敏感子串匹配，p12 §4.5）。

2.4 [AUTHOR_FACT] 可用信息对齐：MAB 任务对所有系统公开规则 "newer facts have larger serial numbers"（p1 摘要引述），且 MAB 的 BM25 基线 prompt 本身含新鲜度规则（p2 "with the freshness rule in its prompt"）；LongMemEval 迁移实验用 chat-session timestamp 替换 serial（p19 §5.7）。

2.5 [AUTHOR_FACT] 干预时点：检索完成之后、答案生成之前（post-retrieval aggregation）；CAR 中该干预在每个 hop 各发生一次（p9–10）。

2.6 [READER_INTERPRETATION] fact-level 切分实际上把干预前移到了索引期：在索引粒度上保住 serial 元数据，这正是 p23 §6.5 建议 1 "Preserve fact-level metadata at indexing time" 的来源；因此该方法有两个干预点（索引粒度 + 检索后聚合），而匹配对比只对齐了后者所在的管线段。

## 3. 最强基线与最接近组合基线

3.1 [AUTHOR_FACT] 最强已发表基线（MAB v3 Table 3，262K）：FC-SH 上 HippoRAG-v2 54.0%（gpt-4o-mini 骨干最佳）与 GPT-4o long-context 60.0%；FC-MH 上最佳已发表 7%（Contriever / MemoRAG，p14 Finding 3 与 p27–28 附录 E 一致）。作者结果：FC-SH@262K gpt-4o-mini 82.0 / gpt-4o 93.0；FC-MH@262K CAR gpt-4o-mini 27.0（p14 §5.2 表）。

3.2 [AUTHOR_FACT] 最接近的作者自建组合基线是 "LLM-judgment baseline"：同骨干（gpt-4o-mini）、同检索（BM25 TOP_K=10）、同 fact-level chunking、同数据、同 n=100，用 MAB 官方发布的 BM25 答题 prompt、温度 0.7，得 67.2 [62.5, 71.7]，对 Headline 78.0 [73.7, 81.8] 差 +10.8 pp（6K +8、32K +8、64K +6、262K +21；p15 §5.3 表）。

3.3 [AUTHOR_FACT] 追加匹配 cell：chunk-4096 下 LLM-judgment 61.0% vs 确定性 80.8%（+19.8 pp；分长度 +23/+22/+12/+22），作者称此填补初稿缺口（p6 §1.6、p16 §5.3）。

3.4 [AUTHOR_FACT] 作者明确声明该对比"不是 resolver 单独消融"：两管线在 (1) resolver、(2) prompt 与输出格式（自由文本 T=0.7 vs 结构化 JSON T=0.0）、(3) LLM 任务（decide-and-answer vs extract-candidates）三处联动不同，+10.8 pp 是 whole-pipeline 效应（p15 "Caveat: what this comparison does and does not isolate"）。

3.5 [READER_INTERPRETATION] 概念上"最接近"的组合基线——共享同一次候选抽取、让 LLM 从同一候选列表挑最新（LLM-picks-newest）——本文没有跑，作者自己列为 future work（p23 §6.6 条 4）。因此文内不存在能把 resolver 单独归因的对照组；+10.8/+19.8 pp 只能记作管线级差距。

3.6 [AUTHOR_FACT] 与 22 个已发表系统的对比全部使用 MAB Table 3 的发表数字，作者明言 "we do not re-run the published systems to avoid implementation differences"（p13 §4.7）。

## 4. 结果是否可能来自模型、token、tool-call、prompt 或 oracle 差异？

4.1 模型差异：[AUTHOR_FACT] 主对比在骨干上对齐——MAB 论文基线均用 gpt-4o-mini（p12 §4.2 "per MAB §4.1"），Finding 2 的 94.8% 对照对象是同型号 GPT-4o long-context 60%（"same model, different post-processing"，p14）。[READER_INTERPRETATION] 未见与 gpt-4o-mini-2024-07-18 具体快照是否与 MAB 所用快照一致的说明，属于残余不确定性。

4.2 prompt/温度差异：[AUTHOR_FACT] 存在且作者承认为混杂（T=0.7 vs T=0.0；自由文本 vs JSON；p6 §1.6、p15 §5.3、p22 §6.4）。[READER_INTERPRETATION] 单是温度 0.7→0.0 与输出格式约束就可能贡献若干 pp，本文数据无法排除；这正是 3.5 所指缺失对照的后果。

4.3 chunking 差异（对已发表数字的对比）：[AUTHOR_FACT] Headline 用 fact-level 切分，而 MAB 的 BM25 发表值是 chunk-512（MAB 论文 Table 15/附录 E 所列默认）且 MAB 发布配置为 chunk-4096（p9 §3.1、p12 §4.4 注）；作者自建 LLM-judgment 基线与 Headline 在 chunking 上对齐，但与 Table 3 发表值的对比在 chunking 上不对齐。[READER_INTERPRETATION] 因此"+28 pp vs HippoRAG-v2"这类跨系统差距混合了切分策略、抽取 prompt 与 resolver 三重差异；不过 chunk-4096 消融（80.8%，仍高于全部发表系统）表明差距不完全由 fact-level 切分造成。

4.4 oracle/任务结构：[READER_INTERPRETATION] max(serial) 直接消费 benchmark 构造性保证存在且可正则解析的 ground-truth 版本标记，fact-level 正则也依赖"编号事实"的表面格式；方法的适用前提（显式全序版本标记）恰是该 benchmark 的构造性质。作者以 "Version-marker assumption"（p22 §6.4）承认此前提，但对比读法上应同时理解为"其余系统未利用该显式结构"，而非其余系统在无该结构任务上也差。

4.5 指标差异：[AUTHOR_FACT] 全部对比统一用 MAB 的 SubEM；作者注明 SubEM 会略抬高冗长长上下文基线（对己方短实体输出"非问题"，p12–13 §4.5 "SubEM caveat"）。

4.6 token/调用次数差异：[AUTHOR_FACT] 两条单跳管线每查询成本相同（约 $0.0001，p20 §5.8）；CAR 每题多次 LLM 调用（约 $0.0003）。[READER_INTERPRETATION] CAR 相对单次调用的发表系统用了更多推理调用，Finding 3 的 +20/+23 pp 含"更多计算"成分；单跳 Finding 1/2 无此问题。

4.7 数据行差异：[AUTHOR_FACT] 6K 列用 MAB 发布的 factconsolidation_*_6k 行，但 MAB Table 3 不含 6K；作者已把 6K 排除出 apples-to-apples 对比，262K 单列对比为 +28/+33 pp（p4 §1.3 两条 caveat、p14 脚注）。

4.8 [OPEN_QUESTION] "Table 3 单值对应 262K cell"是作者经 MAB Table 10 核对的判断（p13 §4.7、p27 附录 E），本 PDF 内无法独立复核 MAB 原表；同样，Langfuse traces "available on request"（p27）与 GitHub 仓库 cvikasreddy/memory-conflict-resolution（p27 附录 D）为外部资源，本次核源未访问验证。

## 5. 作者明示限制、负向结果和未测试边界

5.1 明示限制（p6 §1.6 与 p22 §6.4 双处陈列）：[AUTHOR_FACT] (a) 主评测基本单一 benchmark，MQUAKE 反事实可能不代表真实冲突模式；(b) 版本标记假设——需全序，不能处理偏序或更新间因果依赖；(c) 确定性管线非严格占优（10.5% 题仅 LLM-judgment 答对 vs 21.3% 反向，p17 §5.5）；(d) 匹配对比混杂（见 3.4）；(e) 失败模式分析是 ~30 例 262K 错误抽查的定性 pilot，非系统标注（p22）；(f) 仅三骨干（gpt-4o-mini、gpt-4o、o4-mini），其他模型家族数字可能移动；(g) FC-MH 仍远未解决（30.2%），分解法 "preliminary"。

5.2 负向/中性结果：[AUTHOR_FACT] (a) LongMemEval knowledge-update：确定性 57.8% vs LLM 基线 64.4%（n=45，CI 重叠，"statistically tied"，点值更低；p19 §5.7）；(b) hybrid（空抽取时回退 LLM-judgment）"was a wash (+0.2 pp)"（p23 §6.6 条 2）；(c) CAR 在 6K 伤害 o4-mini（52 vs 纯推理 80），32K 反救（42 vs 14）（p18 §5.6）；(d) chunk-4096 与 fact-level 平均基本打平（80.8 vs 78.0，CI 内），曲线相反——短上下文 chunk-4096 胜、262K fact-level 胜（p15–16）；(e) ~2% FC-SH 保守空抽取按 SubEM 计错（p9、p20 §6.1）；(f) LLM-judgment 基线在"可证已检回正确事实"的子集上仍从 78%（64K）掉到 66%（262K）——判断失败而非检索失败（p16 §5.4）。

5.3 未测试边界：[AUTHOR_FACT] resolver 干净隔离（共享抽取 + 多候选更难 regime）；question-type-aware 组合管线（Yes/No wrapper、k-th-newest、聚合处理器，全 LongMemEval 与 LoCoMo）；真实生产冲突数据（用户偏好更新、政策替代、协作纠错、原生时间戳与偏序更新）（p23–24 §6.6 条 4–6）。

5.4 [READER_INTERPRETATION] 本文限制披露密度显著高于常见 preprint（摘要、§1.6、§5.3、§6.4 四处重复混杂声明），核源时未发现摘要主张超出正文表格支持的情况。

## 6. Operator 抽取与真实可记录 Failure

6.1 可抽取 Operator（均可定位）：

- OP1 extract-then-aggregate：[AUTHOR_FACT] 把 LLM 职责收窄为语义候选抽取（strict、verbatim、include-all、不许挑最优），版本比较交给确定性代码 max(serial/timestamp)；空候选返回 "no answer" 作校准弃权。p9 §3.1、p20 §6.1、p23 §6.5 建议 2。
- OP2 per-hop deterministic resolution：[AUTHOR_FACT] 在 Self-Ask 式分解链的每个 hop 内做确定性冲突解析（CAR），配 HARD_CONSTRAINT（一 hop 一关系词）防止链压缩。p9–10 §3.2、p21 §6.3。
- OP3 索引期保留版本元数据粒度：[AUTHOR_FACT] "Preserve fact-level metadata at indexing time"——无论何种切分，版本标记须在冲突可能发生的粒度上可用。p23 §6.5 建议 1。
- OP4 union-accuracy 检索上界 + McNemar 配对检验：[AUTHOR_FACT] 用两管线并集准确率（88.5%）下界检索天花板、用配对列联（85 vs 42，chi^2=14.6, p<0.001）替代仅报边际 CI 的方法学。p17 §5.5。
- OP5（仅提议、未实现）question-type 路由组合：[AUTHOR_FACT] 作者提出 Yes/No wrapper、k-th-newest 选择器、聚合处理器与确定性原语组合，明确留作 future work。p19 §5.7、p23–24 §6.6 条 5。[READER_INTERPRETATION] 抽取时应标注 "proposed, untested"，不可当作已验证 Operator。

6.2 真实可记录 Failure（作者实证记录）：

- FL1 prior-override：[AUTHOR_FACT] 问题主语带强训练先验时（Finland/ice hockey vs pesäpallo 例），LLM 违背显式 "newer wins" 规则输出先验。p3 §1.2、p10–11 §3.3。
- FL2 serial-comparison drift：[AUTHOR_FACT] 候选池随上下文变大后 LLM 丢失最大序号追踪——基线 75%（64K）→61%（262K）；条件于"确定性管线解出（故事实必在 top-10）"的题上基线仍 78→66，将退化定位到检索后判断。p3、p16 §5.4。
- FL3 max() 错算子：[AUTHOR_FACT] historical/relative 题（LongMemEval Q10：max(timestamp) 返回 "Premier Gold"，GT "Premier Silver"）与按事件时间聚合题（Q19：返回 "9"，GT "7"）中 max 语义错误。p19 §5.7、p28–29 附录 F。
- FL4 Yes/No 格式失配：[AUTHOR_FACT] verbatim 抽取输出不含 "Yes" 前缀，SubEM 判错而自由文本基线合成 "Yes, ..." 通过（5 负例中 3 例）。p19、p28 附录 F Q14。
- FL5 CAR hop-1 错候选级联：[AUTHOR_FACT] 平均 2.56 hop/题、86% hop 执行成功；最常见失败是 hop-1 幻觉/错候选抽取，错误沿链级联，确定性新鲜度无法挽回。p17–18 §5.6、p21 §6.3。
- FL6 strict 抽取过度拒绝：[AUTHOR_FACT] 10.5%（42/400）题仅 LLM-judgment 答对，典型原因是谓词过严导致有效候选被拒（precision-recall 交换）。p17 §5.5、p20 §6.1。
- FL7 分解伤害强推理模型于短上下文：[AUTHOR_FACT] o4-mini 6K：CAR 52 vs 纯 80（"decomposition only adds hop-1 failure surface"）。p18 §5.6。
- FL8 序号并列：[AUTHOR_FACT] "Ambiguous serial tie"（两事实同 serial）约占 262K 错误抽查的 ~5%。p18 失败模式表。
- FL9（定位为假设而非事实）：[READER_INTERPRETATION] "Zep 的 resolve_edge 摄取期 LLM 判断继承同一问题"是作者自称的 "plausible explanation"（p21 §6.2），Zep 7.0% 的分数是作者转引的 MAB 发表数，但机制归因只能记 hypothesis。

## 7. 判断-定位对照（关键锚点汇总）

| 判断 | 页码 | 章节/图表 | 逐字定位语 |
|---|---|---|---|
| 干预点=assembly 非 storage | p1, p4 | 摘要, §1.4 | "assembly (post-retrieval aggregation), not storage" |
| SH-conflict 三步与伪代码 | p9 | §3.1 | "do not compare serials, do not pick a 'best'" |
| CAR 分解与断链规则 | p9–10 | §3.2 | "{hop_k_answer} placeholders" |
| 匹配对比 67.2 vs 78.0, +10.8 | p15 | §5.3 表 | "AVG [95% CI] ... 67.2 [62.5, 71.7]" |
| 混杂声明 | p15 | §5.3 Caveat | "what this comparison does and does not isolate" |
| 主表 5 管线×4 长度 | p14 | §5.1 表 | "78.0 [73.7, 81.8]" |
| 262K 对比 82/93/27 vs 54/60/7 | p14 | §5.2 表 | "For apples-to-apples comparison, we report our 262K column" |
| chunk-4096 匹配 cell +19.8 | p16 | §5.3 | "80.8% vs LLM-judgment's 61.0%" |
| 检索非因（条件化分析） | p16 | §5.4 | "Retrieval is not the cause" |
| 并集 88.5 / 21.3% vs 10.5% / McNemar 14.6 | p17 | §5.5 | "Both correct: 227 (56.8%)" |
| FC-MH 骨干扫描 30.2/43.2/51.5 | p17–18 | §5.6 表 | "gpt-4o + CAR ... 51.5" |
| o4-mini 交叉（52 vs 80; 42 vs 14） | p18 | §5.6 | "at 6K, CAR hurts o4-mini" |
| 失败模式抽查表（~30 例） | p18 | §5.6 表 | "Ambiguous serial tie ~5%" |
| LongMemEval 平局 57.8 vs 64.4 | p19 | §5.7 表 | "overlapping CIs, statistically tied" |
| 成本表 $0.0001 vs $0.005 | p20 | §5.8 表 | "Ablation C (gpt-4o) $0.005 (50x cost)" |
| hybrid 无效 +0.2 pp | p23 | §6.6 条 2 | "was a wash (+0.2 pp)" |
| 版本标记假设 | p22 | §6.4 | "Version-marker assumption" |
| 未重跑发表系统 | p13 | §4.7 | "we do not re-run the published systems" |
| 22 系统全表 | p27–28 | 附录 E | "Zep / Graphiti (temporal KG) 7.0" |
| LongMemEval 负例逐字 | p28–29 | 附录 F | "GT: ['Premier Silver'] Ours: 'Premier Gold'" |

## 8. 解析文本与可视 PDF 是否冲突（就抽查页作答）

8.1 [READER_INTERPRETATION] 就抽查过的 p1、p3、p11、p14、p15、p18、p19、p27：全部关键数值（67.2/78.0/+10.8、80.8/61.0/+19.8、30.2/43.2/51.5、94.8、57.8/64.4、93.0/82.0/27.0、54.0/60.0/7.0、chi^2=14.6）在解析文本与渲染图像间一致，无实质冲突。

8.2 [AUTHOR_FACT]（PDF 自身排版缺陷，两处，视觉与文本一致地截断）：(a) p11 §3.4 行 "scripts/13_paper_experiment." 溢出右边界，".py" 后缀在渲染版中即被裁掉；(b) p19 §5.7 末行 "result in poc_results/longmemeval_knowledg..." 同样溢出右边界截断。两处均为论文源排版溢出，非抽取管线错误。

8.3 [OPEN_QUESTION] p13–14 主表脚注称 "⋆ marks the three headline findings"，但渲染版中仅 Ablation B 行标 ⋆、Ablation C 行标 ⋆⋆，Headline 行（Finding 1，78.0）无星标——排版与文字说明轻微不一致，不影响数值。

8.4 [OPEN_QUESTION] p1 作者-邮箱疑似交叉：Vikas Reddy 配 vikas.challaram@gmail.com、Sumanth Challaram 配 sumanth.reddy@iitkgp.ac.in（姓氏互换样式）；文内无法解决，仅记录。

8.5 [OPEN_QUESTION] 计数口径备注：§1.3 说 "Total: 2000 evaluations across the master table"（20 cells），p12 §4.6 说 "Total LLM-driven evaluations: 4400 (44 cells)"（含 24 个消融/诊断 cell）——两者口径不同但内部自洽（20+24=44）；附录 C "All 20 cells (5 pipelines x 4 context lengths)" 与主表一致。此条仅为口径提示，非矛盾。

——报告完——
