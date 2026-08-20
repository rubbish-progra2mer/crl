# P011 主 Codex 首读

- PDF：`knowledge_base/staging/papers/P011_secom.pdf`
- PDF SHA-256：`998ab05ece554a83870b1baf5762f314837165e99f22ef2af8ffd7ba473c5004`
- 读取时间：`2026-07-19T15:34:00+08:00`
- 读取范围：逐页检查 1–35 页；正文 1–10 页，参考文献 10–15 页，segmentation/cost/evaluation/dataset 与扩展实验附录 15–27 页，四组完整 case studies 28–35 页。

## Changed computation / 方法对象

- [AUTHOR_FACT] SECOM 将预先按 turn 或 session 切分的 memory units 改为由 conversation segmentation model 识别 topic-coherent contiguous segments；检索前再用 LLMLingua-2 以 75% 保留率压缩每个 unit，作为 retrieval denoising。
- [AUTHOR_FACT] 生成时按 query 检索 memory units，在 context token budget 内把命中的 units 按时间顺序拼接给 response LLM；不经摘要替换原 conversation，避免 summary information loss。
- [AUTHOR_FACT] QA 主实验采用 GPT-4-0125 zero-shot segmentation；有人工 segmentation labels 的独立 segmentation benchmark 才用 hard-example reflection 学 10 条 textual rubric 与代表 examples。该 reflection 未用于 LOCOMO/Long-MT-Bench+ 主 QA。
- [READER_INTERPRETATION] 论文有两个可分离 changed computations：语义 segment boundary 与压缩后检索。主 baseline 的 turn/session retrieval 已同样使用 denoising，故主表的 SECOM 差异主要检验 granularity；Table 2 才检验 SECOM 内 compression 的边际贡献。

## 数据、比较与评估边界

- LOCOMO 原始主实验发生在官方 QA 发布前：按 Alonso et al. 用 GPT-4 为每 session 生成 QA；Appendix Table 6 另用后发布的 official QA 复验。两组不可混称同一 test set。
- Long-MT-Bench+ 由 MT-Bench+ 重构：用 54 个 human long-range questions 作 few-shot，让 GPT-4 为每 dialogue topic 生成问题，并合并 5 个 consecutive sessions；平均 26.09 QA、4.91 sessions、65.45 rounds、19,287 tokens。它不是原 benchmark 的原封不动结果。
- 主 response generator 为 GPT-3.5-Turbo，robustness 用 Mistral-7B-v0.3。Retriever 同时测 BM25 和 MPNet；主 retrieval budget LOCOMO 4k tokens、Long-MT-Bench+ 1k tokens，而不同 granularity 的 units 数不同。
- GPT4Score 只要求 response faithful to retrieved history 且 answer question，以 1–100 打分；pairwise 交替答案顺序再评一次。PDF 未给 judge-vs-human correctness meta-evaluation，另有 10 annotators 在 Long-MT-Bench+ 上按五维 0–? rubric 打分。
- 主表比较 MemoChat（同为 segment-level memory）最接近，但 MemoChat 同时训练 memory construction/retrieval，context tokens 与 pipeline 不同；Table 5 报告每问 total input/output/latency，SECOM 1722/135/2.61s，MemoChat 7233/229/5.60s，session-level 3642/102/2.17s。

## 主要结果与归因边界

- LOCOMO Table 1：BM25+GPT4-Seg SECOM GPT4Score 71.57，高于 denoised turn BM25 65.58、session BM25 63.16 与 MemoChat 65.10；MPNet SECOM 69.33，而 Mistral/RoBERTa segmentation 降至 66.37/61.84，说明 segmentation model 能力贡献明显。
- Long-MT-Bench+：MPNet SECOM 88.81，对 turn 84.91、session 73.38、MemoChat 85.14；但 BM25 SECOM 86.67 只比 MemoChat 1.53。优势随 retriever/dataset 变化，不是固定大幅提升。
- Table 2 在 MPNet+75% setting 中去 denoise：LOCOMO 69.33→59.87（-9.46），Long-MT-Bench+ 88.81→87.51（-1.30）。Compression 收益在两数据集高度不同，不能称普遍同量级。
- Table 3 换 Mistral generator 后，Long-MT-Bench+ SECOM 89.43/90.58，仍高于对应 turn 83.14/85.61；但所有 SECOM contexts 约 820–906 tokens，而 full history 19,287 tokens，结果支持相关性筛选，不是同输入量下 reader 能力比较。
- Official LOCOMO Table 6：GPT-3.5 SECOM 84.21 vs turn 81.52、MemoChat 75.77；Mistral SECOM 80.07 vs turn 78.82。对最强 turn baseline 的 margin 仅 2.69/1.25，明显小于原生成 QA 主表的若干差距。
- Segmentation Table 4 中 GPT-4 zero-shot 在三集均优于无监督 baselines，reflection 用 source top-100 hard examples 后迁移；但对话 labels 的粒度偏好不同，Appendix Figure 11 展示 GPT-4 会相对 ground truth 严重过切，且 learned rubrics 多条语义重复地强调避免 over-segmentation。
- Appendix human Table 10：SECOM average 1.55，仅略高 COMEDY 1.51、MemoChat 1.48；在 coherence 上低于 COMEDY（2.13 vs 2.20），支持多维收益并非全面占优。

## 失败边界与限制

- [AUTHOR_FACT] Turn units 会把依赖多个连续问答的 evidence 碎片化；session units 会混入多 topic 噪声；RecurSum/ConditionMem cases 会因 summary 或 selective memory 丢失回答所需细节。
- [AUTHOR_FACT] Retriever 敏感性显著：LOCOMO turn/session 从 MPNet 换 BM25，GPT4Score 分别改善 7.59/11.98；segment granularity 虽更稳，仍随 retriever、segmentation backbone 改变。
- [AUTHOR_FACT] MemoChat 无法在 Mistral setting 运行，因为其 memo-writing 常生成无效 JSON；需要 LLM 产出结构化 memory 的方法有格式可靠性边界。
- [AUTHOR_FACT] GPT-4 zero-shot segmentation 倾向过细切分；reflection rubric 使用 ground truth 与 WindowDiff hard examples，属于有监督反馈条件，不能归为纯 intrinsic self-improvement。
- [READER_INTERPRETATION] Compression 同时减少 query-irrelevant token、改变 embedding representation 并降低 reader input；Table 2 未提供等 retrieved-token 的 uncompressed retraining/retuning，所谓“denoising”是合理解释但非唯一因果机制。
- [READER_INTERPRETATION] LOCOMO/Long-MT-Bench+ 问题与 GPT4Score judge 均涉及 GPT-4，segmentation 也用 GPT-4；虽不等于直接泄漏答案，但共享模型族可能形成语体/边界偏好，论文没有跨 judge/问题生成器的系统敏感性分析。
- [READER_INTERPRETATION] 所有 segmentation 在入库前执行，新增 session 只需切当前 session；但会话中 topic 跨 session 延续、旧 segment 后续应合并或重切的在线维护问题未测试。
- [READER_INTERPRETATION] Segments 按 topic coherence 优化，不直接处理 knowledge updates、contradictions、temporal scope、abstention 或 source trust；不能把 LongMemEval 的全部 memory 能力归于 chunking granularity。

## 可抽取候选（尚非正式 Card）

- Operator：`Topically Coherent Contiguous Memory Segmentation`——以完整 inquiry–response thematic exchange 为最小 retrieval unit，在 turn 碎片与 session 噪声之间调整 granularity。
- Operator：`Compression-as-Retrieval Denoising`——在保留原义的前提下压缩 unit 后建立/查询 retrieval representation；必须同时报告 retention ratio、retrieved tokens 与无压缩对照。
- Failure：`Retrieval Granularity Fragmentation–Noise Tradeoff`——过细使 evidence 分散且单 turn 不含 query keyword，过粗使多 topic 噪声淹没有效内容。
- Failure：`Summary Memory Deletes Answer-Critical Detail`——summary/conditioned records 可保留主题却删掉数量、奖项、理由等后续问题需要的细节。
- Failure：`Segmentation Model Over-Splits Thematic Exchanges`——模型把问答、setup-response 或轻微 topic shift 分开，破坏后续 retrieval coherence。

## 未解决问题

- `[OPEN_QUESTION]` LLMLingua-2 75% compression 对事实保持率、数值/否定/时间信息的错误率未直接人工标注。
- `[OPEN_QUESTION]` 主表未给不同 random seeds、置信区间或问题级显著性；pairwise win-rate 不能替代独立重复。
- `[OPEN_QUESTION]` GPT-4 segmentation 预处理成本是否按每次新增会话摊销、以及跨 session topic linking 成本未报告。
- `[OPEN_QUESTION]` GPT4Score 与 10-person human evaluation 的逐样本相关性/一致率未在 PDF 中给出。
