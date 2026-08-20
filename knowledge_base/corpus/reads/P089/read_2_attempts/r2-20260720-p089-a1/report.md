# P089 独立二读报告

## 0. 证据口径

- `AUTHOR_FACT`：PDF 直接陈述、图表直接给出或可由其数字机械抄录的内容。
- `AUTHOR_INTERPRETATION`：作者对结果、动机、因果或实用性的解释；不自动视为已被实验充分证明。
- `AUDIT_JUDGMENT`：本次独立二读基于指定 PDF 作出的边界、缺口或先行关系判断。
- 页码均为 PDF 物理页码（1–18）；必要时同时给出论文印刷页码（5465–5482）。短定位语仅用于回到页面，不代替上下文。

## 1. Canonical metadata

- `AUTHOR_FACT` 标题：*ToolDreamer: Instilling LLM Reasoning Into Tool Retrievers*。作者：Saptarshi Sengupta、Zhengyu Zhou、Jun Araki、Xingbo Wang、Bingqing Wang、Suhang Wang、Zhe Feng。单位：The Pennsylvania State University 与 Bosch Research North America；Saptarshi Sengupta 的工作注明完成于 Bosch Research North America 实习期间。定位：物理页 1，标题与作者栏、星号脚注。
- `AUTHOR_FACT` 出版信息：*Proceedings of the 19th Conference of the European Chapter of the Association for Computational Linguistics*, Volume 1: Long Papers，印刷页 5465–5482，2026-03-24 至 2026-03-29。定位：物理页 1 页眉“Volume 1: Long Papers”。
- `AUTHOR_FACT` 指定 PDF 共 18 个物理页；文件 SHA-256 为 `d13b84ab7c2a66069f8d160ab78dfb3e7efd5dabab06c219995c5f92b2093918`，与 invocation 给定值一致。PDF 内未给 DOI；附录 H 只给出公开代码仓库地址。定位：物理页 15，“Paper Code”。
- `AUDIT_JUDGMENT` 本报告只核验了指定 PDF 的内部元数据与正文，没有通过互联网或代码仓库补充版本、DOI、勘误或实现事实，因此“canonical”限定为该 PDF 所呈现的书目信息。

## 2. 方法的 changed computation

### 2.1 Hypothetical-tool generation

- `AUTHOR_FACT` ToolDreamer 先让 LLM 根据用户问题生成一个或多个 hypothetical tools（HT）。每个 HT 只有三段元数据：Thought、Tool Name、Tool Description；不生成工具实现。定位：物理页 3，§3.1.1，“only metadata (thoughts + name + description)”；物理页 17–18，Figures 7–8。
- `AUTHOR_FACT` 训练 prompt 要求逐步分解显式和隐式子任务、每个子任务对应一个独立无状态工具、命名一致、模块化且 implementation-agnostic；测试 prompt 仍做子任务分解，但开放决定工具数，至少生成一个工具，并明确不要合并子任务或建议 pipeline。定位：物理页 17 Figure 7；物理页 18 Figure 8。
- `AUTHOR_FACT` 主实验用 GPT-4.1 生成训练与测试 HT；RQ3 另用 Qwen3-32B 检查开放模型生成器。定位：物理页 6，§4.1 “HT Generation Model”；物理页 8–9，§4.4 与 Table 5。
- `AUTHOR_INTERPRETATION` 作者认为 Thought 提供“为何需要该工具”的推理信号，而 Name/Description 把搜索表达移入 tool-description language space，因此比原问题与工具描述直接相似度更自然。定位：物理页 1 Abstract；物理页 5，§3.1.3。
- `AUDIT_JUDGMENT` 这里的“reasoning”是生成器输出的自然语言 rationale，不是对真实工具可执行性、参数模式或调用约束的验证；HT 可能描述不存在的工具，但作者有意把这种开放性用于检索提示。

### 2.2 训练期 gold-count knowledge

- `AUTHOR_FACT` 训练时作者知道每个问题需要多少个 gold tools（GT），并在 prompt 中强制 GPT-4.1 生成与 GT 数量完全相同的 HT。约 0.3% 问题未得到正确工具数，这些样本从抽样训练集移除。定位：物理页 3，§3.1.1，“know a priori the number of tools required”；物理页 17 Figure 7，“exactly the number of tools specified”。
- `AUTHOR_FACT` 测试时不知道工具数量，不向 LLM 提供 gold count；生成器开放地决定多少个 HT。定位：物理页 5，§3.2.1，“do not know a priori how many”。
- `AUDIT_JUDGMENT` 训练数据构造使用了 gold cardinality supervision。它没有直接泄漏测试 GT 身份，但让训练期 HT–GT 矩阵天然为方阵并保证可做 1:1 配对；训练与推理在“工具数已知/未知”上存在分布差异。删掉不服从数量指令的 0.3% 样本还会轻微选择性过滤训练分布。

### 2.3 Hungarian HT–GT alignment

- `AUTHOR_FACT` 对每个问题，作者用 Qwen3-8B embeddings 计算所有 HT–GT 对的语义相似度矩阵，再用 Hungarian algorithm 做最小成本匹配，得到一一对应的 aligned `(HT, GT)` pairs。定位：物理页 4，§3.1.2，“semantic similarity ... matrix”与“minimal cost matching”。
- `AUTHOR_FACT` 论文承认方阵总能产生匹配，即使 HT–GT 语义并不真正对应；该匹配被当作“rough and often accurate proxy”。Hungarian 复杂度为 `O(n^3)`；ToolRet 中每题工具数范围 1–8，56% 的问题为 1 个、0.1% 为 8 个、平均约 2 个，故作者认为成本不大。定位：物理页 4，§3.1.2 及脚注 1。
- `AUTHOR_FACT` alignment 消融把 Qwen3 embeddings 换成弱 DPR、仍用 Hungarian，或保留 Qwen embeddings 但改为 greedy matching。定位：物理页 8，§4.3.2 与 Table 3。
- `AUDIT_JUDGMENT` PDF 没有明确写出如何把 semantic similarity 转成 Hungarian 所需的 cost，也未设置“拒配/无匹配”阈值；在强制方阵与 1:1 配对下，低质量 HT 也必被指派 GT。因此 alignment 是带噪伪标签构造，而不是经过人工验证的 ground-truth correspondence。

### 2.4 Retriever input 与 loss

- `AUTHOR_FACT` 两种 anchor：`TND = Thoughts + Tool Name + Tool Description`；`QTND = Question + TND`。精确格式在正文写为 `Thoughts:{} Tool Name:{} Tool Description:{}`。定位：物理页 5，§3.1.3。
- `AUTHOR_FACT` retriever 用 InfoNCE：提高 anchor 与 aligned GT 的相似度，同时压低 anchor 与随机无关工具 `n_i` 的相似度。Eq. (1) 为正例指数相似度除以正例加 `k` 个负例指数相似度之和。定位：物理页 5，§3.1.3、Eq. (1)。
- `AUTHOR_FACT` 训练 Qwen retriever 使用 LoRA：rank 8、alpha 16、dropout 0.1；1 epoch，学习率 `1e-5`，batch size 1；训练用 4 张 NVIDIA A100 80GB，推理用 1 张。定位：物理页 14，Appendix C。
- `AUTHOR_INTERPRETATION` 作者把核心变化概括为从 query–tool 训练转向 tool–tool 对齐，同时 QTND 又保留 query 作为额外信号。定位：物理页 2，Related Work “train on tool-tool pairs”；物理页 5，§3.1.3。
- `AUDIT_JUDGMENT` “tool–tool”并非纯 HT–GT：最佳版本 QTND 的 anchor 明确包含原 query。PDF 对负例数 `k`、负例采样细节、温度项、随机种子与重复次数没有给出足够可复现信息；Eq. (1) 也未显示常见 temperature。

### 2.5 Inference 与 RRF

- `AUTHOR_FACT` 测试问题先由同一类 LLM 开放生成 HT；每个 HT 按 TND 或 QTND 构成独立 search vector，由 retriever 各自返回 top-K 工具列表。评测沿 ToolRet 设 `K=10`。定位：物理页 5，§§3.2.1–3.2.2；物理页 6，Evaluation Metrics。
- `AUTHOR_FACT` 若生成的 thoughts、names、descriptions 数量不一致，作者丢弃该题的 HT，回退为以原问题作 search vector。定位：物理页 5，§3.2.2，“fall back on the base question”。
- `AUTHOR_FACT` 各 HT 的 top-K lists 用 Reciprocal Rank Fusion（RRF）合并为统一列表；作者把同一问题派生的不同 search vectors 视为相关列表，承认这超出 RRF 通常融合“不同 retrievers、同一 query”的原始用法。定位：物理页 5–6，§3.2.3；物理页 4 Figure 2。
- `AUTHOR_FACT` 作者没有采用“每个列表取 top-1”，理由包括列表间依赖/重叠，以及该方案会让最终工具数等于 HT 数、与固定 `@10` 评测不一致。定位：物理页 5–6，§3.2.3。
- `AUDIT_JUDGMENT` PDF 未给 RRF 的明确公式、rank constant、重复工具处理和最终截断细节；因而论文层面能确认“多 HT 检索后 RRF”，但不能仅凭 PDF 精确复现融合实现。

## 3. ToolRet 设置、baselines 与主结果

### 3.1 设置

- `AUTHOR_FACT` ToolRet 汇集 26 个数据集（计入子集为 35 个），分 Web、Code、Customized 三类。过滤后约为：Web 37K tools/5K queries，Code 4K/2K，Customized 超过 3K/约 1K。约 200K 条训练样本中，作者因 API 成本与数据质量只抽样 5K 个唯一问题。定位：物理页 6，§4.1 Dataset；物理页 15，Appendix E。
- `AUTHOR_FACT` 过滤要求工具描述非空，并去除脏话、重复 query、正负工具重叠以及无有效负例等问题。定位：物理页 15，Appendix E。
- `AUTHOR_FACT` 指标为 NDCG@10、P@10、R@10 与 MRR；各 split 只在本 split 工具池内检索，最终 Avg. 是三个 split 指标的简单平均。定位：物理页 6，§4.1；物理页 7 Table 1 caption。
- `AUTHOR_FACT` baselines/参照包括：BM25 zero-shot；Qwen3-8B zero-shot；直接拿 HT 检索的 `K` 设定（作者称类似 Kachuee et al., 2025）；ToolRet 的 query-trained Qwen3 `Q (TR)`；COLT Phase-1/Phase-2。作者有意不使用 ToolRet instruction 字段，以维持对无 instruction 数据集的最小假设。定位：物理页 6–7，Baselines 与 Table 1。
- `AUDIT_JUDGMENT` 不使用 instruction 字段使实验更接近跨数据集通用场景，但也意味着 `Q (TR)` 是作者控制下的无 instruction 版本，不应被表述成利用 ToolRet 全部监督字段的最强结果。

### 3.2 Table 1 关键平均结果

以下均为三个 split 的 Avg.，顺序为 `NDCG@10 / P@10 / R@10 / MRR`：

| 设置 | AUTHOR_FACT：Avg. |
|---|---|
| BM25 zero-shot question | `29.55 / 6.44 / 36.71 / 32.52` |
| BM25 TND，直接 HT，no training (`K`) | `29.97 / 7.06 / 40.78 / 30.62` |
| BM25 QTND，no training | `33.80 / 7.49 / 43.68 / 35.75` |
| Qwen3 zero-shot question | `38.43 / 8.13 / 48.70 / 40.44` |
| Qwen3 TND，直接 HT，no training (`K`) | `38.83 / 8.77 / 52.55 / 39.12` |
| Qwen3 QTND，no training | `41.29 / 8.71 / 52.39 / 43.02` |
| COLT Phase-1 | `21.78 / 4.55 / 25.78 / 24.54` |
| COLT Phase-2 | `0.26 / 未报告 / 0.36 / 未报告` |
| Qwen3 Q，ToolRet query–tool training | `39.87 / 8.57 / 50.18 / 42.07` |
| Trained Qwen3 TND | `39.79 / 9.16 / 53.46 / 40.04` |
| Trained Qwen3 QTND | `42.47 / 9.34 / 54.26 / 43.88` |

定位：物理页 7，Table 1。

- `AUTHOR_FACT` 论文在表中将 BM25 QTND 相对 BM25 question zero-shot 的平均提升标成约 `+14% / +16% / +19% / +10%`；trained Qwen3 QTND 相对 Qwen3 Q (TR) 标成约 `+7% / +9% / +8% / +4%`。定位：物理页 7，Table 1 caption 与着色百分比。
- `AUTHOR_INTERPRETATION` 作者据此认为：HT 给检索器更好的工具线索；HT 与原 query 结合通常优于 HT 单独使用；aligned-tool training 比 query-only training 更有效且样本效率更高。定位：物理页 6–7，§4.2。
- `AUDIT_JUDGMENT` 改善不是逐模型、逐指标一致：例如 no-training Qwen3 TND 的 MRR `39.12` 低于 question zero-shot 的 `40.44`，BM25 TND 的 MRR `30.62` 也低于 `32.52`；trained TND 的 NDCG 与 MRR 又略低于 query-trained baseline。最稳健的表内结论是 QTND 配置的平均点估计最好，而不是“HT/TND 在所有指标都提升”。
- `AUDIT_JUDGMENT` PDF 给的是单次点估计，未报告置信区间、显著性检验或跨随机种子方差；因此 4%–19% 是表中相对点估计，不能直接读成稳定因果增益。

## 4. Ablations

### 4.1 Prompt / HT quality（Table 2）

- `AUTHOR_FACT` inferior prompt 删除关键要求、使用更宽松语言且不提供示例；以 TND 隔离 HT 质量。BM25 从 `29.97/7.06/40.78/30.62` 变为 `29.55/6.77/39.66/30.76`；Qwen3 从 `38.83/8.77/52.55/39.12` 变为 `38.23/8.33/50.58/39.21`。定位：物理页 7–8，§4.3.1、Table 2；inferior prompt 见物理页 16 Figure 5。
- `AUTHOR_INTERPRETATION` 作者认为高质量 HT 是框架基础，提示设计不可忽视。
- `AUDIT_JUDGMENT` NDCG/P/R 的确下降，但两模型 MRR 均极小幅上升（`+0.14`、`+0.09`）；所以“所有性能都下降”不精确，证据支持的是多数指标尤其 precision/recall 变差。

### 4.2 Alignment（Table 3）

- `AUTHOR_FACT` trained Qwen3 TND 原始 Qwen/Hungarian 为 `39.79/9.16/53.46/40.04`；DPR/Hungarian 为 `39.48/9.10/53.00/39.81`；Qwen/Greedy 为 `39.70/9.15/53.22/40.00`。定位：物理页 8，Table 3。
- `AUTHOR_INTERPRETATION` 作者据小幅下降认为，优质 embedding/alignment 有帮助，但 HT 本身的质量和外部信号更重要，即使存在一定 misalignment 仍能获益。
- `AUDIT_JUDGMENT` 该消融只比较两个替换项，差异约 0.1%–1%；没有人工 alignment accuracy、无对齐/随机对齐对照或误配分层，因而不能单独证明 Hungarian 的必要性，也不能量化伪标签正确率。

### 4.3 List fusion（Table 4）

- `AUTHOR_FACT` trained Qwen3 的 TND/RRF 为 `39.79/9.16/53.46/40.04`，QTND/RRF 为 `42.47/9.34/54.26/43.88`；TND/LLM-F 为 `46.48/10.16/57.64/46.83`，QTND/LLM-F 为 `46.53/10.14/57.67/46.89`。定位：物理页 8–9，§4.3.3、Table 4。
- `AUTHOR_FACT` GPT-4.1 LLM-F 对不超过 10 个候选做全量 rerank，超过 10 个则从全集选 top-10，并给 0–1 relevance score。定位：物理页 8，§4.3.3；物理页 16 Figure 6。
- `AUTHOR_INTERPRETATION` 作者把 LLM-F 相对最佳 QTND/RRF 的约 `+10% NDCG、+9% P、+6% R、+7% MRR` 归因于语义推理强于纯排名统计，但最终优先采用 RRF，因为 RRF 更便宜、可复现且确定。
- `AUDIT_JUDGMENT` Appendix D 报告 GPT 会少报/多报工具，并可能产生输入列表外工具；少报时保留全部、多报时截为 10。该后处理与固定 10 项 RRF 并不完全同口径。更重要的是，“deterministic”只成立于给定 lists 后的 RRF 融合；上游 HT 仍由 LLM 生成，而 PDF 未报告解码参数或随机种子，所以不能把整个 ToolDreamer 推理链称为确定性。

### 4.4 HT generator（Table 5）

- `AUTHOR_FACT` 此消融只在 ToolRet Code split、no training 下进行，retriever 为 BM25 与 NV-Embed-2。BM25：TND/GPT `33.91/6.47/47.15/32.25`，QTND/GPT `36.50/6.51/49.34/34.81`，TND/Qwen3-32B `31.43/5.52/42.68/30.19`，QTND/Qwen3-32B `35.27/6.00/47.47/33.68`。NV-Embed：TND/GPT `44.52/8.22/60.31/42.61`，QTND/GPT `47.41/8.07/60.76/46.53`，TND/Qwen `43.13/7.35/56.57/42.42`，QTND/Qwen `46.11/7.56/59.16/45.31`。定位：物理页 9，§4.4、Table 5。
- `AUTHOR_INTERPRETATION` 作者认为开放模型只带来不大的损失，说明 ToolDreamer 不绑定 API 模型，并有成本/隐私优势。
- `AUDIT_JUDGMENT` 表中 Qwen3-32B 在所有列均低于 GPT-4.1，部分 recall 差约 2–4 点；“flexible”有点估计支持，但仅来自一个 split、两种 retriever、无训练设定，不能外推成生成器普适可替换。

## 5. Latency、API 与 determinism tradeoffs

- `AUTHOR_FACT` 示例 query 的普通 Qwen retrieval 约 `0.04 s`；ToolDreamer 的 HT 生成约为 Qwen3-32B `8 s`（1 张 A100）或 GPT `2.5 s`，semantic search + RRF 再加 `0.5 s`，总计约 `3–8.5 s`。定位：物理页 9，§4.5。
- `AUTHOR_FACT` 作者称用 OpenAI batch mode 与 GPT-4.1 完成实现成本低于 5 美元。定位：物理页 9，§4.5，“less than $5”。
- `AUTHOR_FACT` LLM-F 需要额外 API calls，并存在不遵循数量指令和 hallucination 风险；RRF 不需要这一步。定位：物理页 8，§4.3.3；物理页 14，Appendix D。
- `AUTHOR_INTERPRETATION` 作者据此称框架 highly cost-effective，并认为客户不会持续提出需要工具的问题，因此增加的延迟可接受；在融合阶段以 RRF 换取低成本、可复现与确定性。
- `AUDIT_JUDGMENT` “<$5”没有给 token 数、价格快照、训练/测试调用拆分或每 query 成本，不能据此估计生产总成本；2.5 秒 GPT 也只是一条示例 query 的观察，不是延迟分布。相对 `0.04 s` 基础检索，`3–8.5 s` 是约两个数量级的端到端检索前处理增幅。生产可接受性依赖 SLA、并发、缓存、隐私和工具调用频率，PDF 未实证这些假设。

## 6. Retrieval-only 与 end-to-end boundary

- `AUTHOR_FACT` 核心实验只评测工具检索排序：NDCG@10、P@10、R@10、MRR。没有在 Table 1–5 中执行所检工具、生成工具参数或评分最终任务答案。定位：物理页 6，Evaluation Metrics；物理页 7–9，Tables 1–5。
- `AUTHOR_FACT` Appendix B 的 Figure 3 用 SealTools 展示 GPT-4.1/Qwen3 随候选工具数增加的 tool-call hit rate 与上下文/API tool-count 上限；它是“为什么需要 retriever”的独立动机实验，不是 ToolDreamer 与 baseline 的端到端工具调用对照。定位：物理页 14，Appendix B、Figure 3。
- `AUTHOR_INTERPRETATION` 作者说“having a better retriever is closely linked with LLM tool-calling ability”，并把 ToolDreamer定位为向 LLM 提供 scoped tool sets 的一步。定位：物理页 9，Conclusion。
- `AUDIT_JUDGMENT` 论文直接支持的是 retrieval quality improvement，不直接支持最终工具选择正确率、参数正确率、执行成功率、答案质量或任务完成率提升。检索出的额外相关/无关工具如何影响 LLM，尤其固定 top-10 与多工具任务下的 downstream behavior，仍是未验证边界。

## 7. 是否为 query-side latent-tool expansion 的直接先行

- `AUDIT_JUDGMENT` **是，若“query-side latent-tool expansion”指由 LLM 从 query 生成显式或潜在的工具需求/代理工具描述，再把这些代理作为一个或多个检索向量并融合结果，ToolDreamer 是直接且高度接近的先行。** 其核心计算完全覆盖：`query → 多个 hypothetical tool descriptions → 每个 HT 检索 → RRF 合并`；最佳 QTND 还把原 query 与每个 HT 拼接。定位：物理页 4 Figure 2；物理页 5，§§3.2.1–3.2.3；物理页 9 Conclusion。
- `AUTHOR_FACT` 论文自己承认 Kachuee et al. (2025) 已用 LLM commonsense 生成 hypothetical tool descriptions 并直接用于检索；ToolDreamer 声称的主要新增点是 retriever optimization，即以训练期 gold-count 构造方阵、Hungarian HT–GT alignment、TND/QTND InfoNCE 训练，并在推理时融合多个 HT lists。定位：物理页 2–3，Related Work；物理页 6–7 Table 1 的 `(K)` 行。
- `AUDIT_JUDGMENT` 因此，候选若只提出“先想象可能需要的工具/能力，再扩展 query 检索并融合”，会与本论文的 inference pipeline 发生核心机制碰撞；若再加 HT–GT 对齐训练，则碰撞更强。可主张的差异必须落在真实 changed computation，例如不生成文本 HT 的隐空间结构、无 gold-count/无 1:1 强制配对的学习目标、可拒配/集合级对齐、与执行反馈闭环、或经端到端 tool-use 指标验证的机制，而不能只换“latent intent/tool plan/tool sketch”等名称。
- `AUDIT_JUDGMENT` 若“latent”严格指不可读的内部向量、联合学习的隐藏变量或非 LLM 文本生成，ToolDreamer 未实现该精确表示；此时它仍是 query-side tool-need expansion 的直接组件/谱系先行，但不一定是完整 pipeline 的 exact prior。该区别应在后续 novelty claim 中明确。

## 8. 可复核定位摘要

| 主题 | 物理 PDF 页 / 章节或表 | 短定位语 |
|---|---|---|
| 元数据与问题动机 | p.1 / Abstract, §1 | “hypothetical (synthetic) TD” |
| 训练 HT 与 gold count | p.3 / §3.1.1 | “know a priori” |
| Hungarian alignment | p.4 / §3.1.2 | “minimal cost matching” |
| TND/QTND 与 InfoNCE | p.5 / §3.1.3, Eq. (1) | “Thoughts:{} Tool Name:{}” |
| 测试开放工具数与 fallback | p.5 / §§3.2.1–3.2.2 | “fall back on the base question” |
| RRF | pp.5–6 / §3.2.3 | “Retrieval Unification” |
| ToolRet 设置 | p.6 / §4.1 | “sample 5K instances” |
| 主结果 | p.7 / Table 1 | “Qwen3 (QTND)” |
| Prompt/alignment 消融 | p.8 / Tables 2–3 | “Weak Tool Alignment” |
| LLM-F 与 generator 消融 | p.9 / Tables 4–5 | “Varying HT Generator” |
| 延迟与成本 | p.9 / §4.5 | “~3 - 8.5 seconds” |
| 训练硬件与 LLM-F 风险 | p.14 / Appendices C–D | “4 NVIDIA A100 80 GB” |
| 数据过滤 | p.15 / Appendix E | “filter and sample 5K” |
| Prompts | pp.16–18 / Figures 5–8 | “Prompt For Test Data” |

## 9. Runtime provenance

- Attempt / Task：`r2-20260720-p089-a1`；协作任务标识 `/root/p089_second_read`。
- Start time：`2026-07-20T20:46:09+08:00`（来自 invocation）。
- End time：`2026-07-20T21:05:41+08:00`（最终机械校验前本机 `Get-Date`）。
- Model/version：`Codex / GPT-5`；当前会话未暴露更细的 model build/version，故不推测。
- Internet access：未联网；未调用 web、浏览器、外部 API 或代码仓库。
- Workspace read scope：根 `AGENTS.md`、`crl_agent_v3/AGENTS.md`、`crl_agent_v3/CRL.md`、`crl_agent_v3/CRL_ENVIRONMENT.md`、`C:/Users/g/.codex/skills/pdf/SKILL.md`、本 attempt 的 `invocation.md`，以及 invocation 指定的 `P089_tooldreamer.pdf`。未读取或枚举 invocation 禁止的资产。
- Observable tool/file trace：PowerShell `Get-Content -Raw -Encoding UTF8` 阅读指令与 invocation；`Get-FileHash -Algorithm SHA256` 核验 PDF；一次 `pdfinfo` 尝试因命令/路径不可用而整体退出码 1，但同一调用中的 SHA-256 已输出；随后使用项目 `.venv/python.exe` + PyMuPDF 取得 18 页页数/内部 metadata、逐页抽取物理页 1–18 文本，并以内存 JPEG/base64 视觉复核物理页 4、7、8、9（另有一次物理页 7 的低分辨率预览）。首次文本输出因控制台 GBK 无法编码版权字符而失败，之后以 `sys.stdout.reconfigure(encoding='utf-8')` 成功；未写中间文本或图像文件。
- Write scope：仅新增本 `report.md`；使用 `apply_patch`，目标为 UTF-8 无 BOM、LF。
- Output report SHA-256：写入并机械校验后报告。
