# P063 独立二读报告

## 0. Provenance 与读取边界

- Invocation snapshot：`knowledge_base/corpus/reads/P063/read_2_attempts/r2-20260720-p063-a1/invocation.md`，Attempt ID `r2-20260720-p063-a1`。
- Canonical metadata：*A-MEM: Agentic Memory for LLM Agents*，NeurIPS 2025 / arXiv:2502.12110。
- 指定 PDF：`knowledge_base/staging/plan05_sat_a1/P063_a_mem.pdf`。
- [AUTHOR_FACT] 本地实算 PDF SHA-256 为 `fec32b521c4a1f793442bf1aeb26139c583078350d1cd4ab8f4eccc54a0694f0`，与 invocation 一致；共 28 个物理页。
- Reader provenance：`reused independent reader thread due platform thread cap`。这不是 fresh empty model context；独立性仅指本轮没有读取 P063 read_1、Cards、其他报告/论文读稿、Corpus/saturation/retrieval/blind 文件，也未接收其他 P063 读者结论。
- 隔离性质：`procedural_blinding`；没有可验证的文件级 allowlist，不能声称技术隔离。
- Actual model/version：不可见，记为 `unknown`。当前 agent task 路径为 `/root/plan05_p026_second_reader`（平台限制下复用）；平台 thread ID 不可见，记为 `unknown`。
- 本报告只做原文核源，不生成 Card/Evidence/manifest，不评价 Candidate。以下页码均为 PDF 物理页。

## 1. 方法究竟改变哪一步计算

### 1.1 Note Construction：把原始交互改写为多表示 note

- [AUTHOR_FACT] 每条 memory note 被定义为 `m_i={c_i,t_i,K_i,G_i,X_i,e_i,L_i}`：原始 interaction content、timestamp、LLM-generated keywords、tags、contextual description、embedding、linked-memory set。位置：p.4，§3.1，Eq. (1)；短定位：“Note Construction”。
- [AUTHOR_FACT] LLM 根据原始 content、timestamp 与 prompt `Ps1` 生成 `K_i/G_i/X_i`；随后 text encoder 对 `concat(c_i,K_i,G_i,X_i)` 编码。位置：p.4，Eqs. (2)–(3)。
- [AUTHOR_FACT] `Ps1` 要求至少三个 keywords、至少三个 tags，并生成一句 context summary。位置：p.19，Appendix B.1。
- [READER_INTERPRETATION] 第一项 changed computation 是将每段原始对话扩展成 LLM 生成的检索代理文本，再对“原文+生成属性”整体 embedding。性能变化因此不能只归因于 graph links；更丰富的 note construction 本身改变了索引内容。

### 1.2 Link Generation：embedding 候选筛选后再由 LLM 判断连接

- [AUTHOR_FACT] 新 memory `m_n` 与所有旧 memory embeddings 做 cosine similarity，取 top-k `M_n^near`，再把新 note、这些近邻与 `Ps2` 交给 LLM。位置：p.4，§3.2，Eqs. (4)–(6)。
- [AUTHOR_FACT] 作者称 LLM 可识别共享属性、因果或概念关系，超越简单 embedding similarity。位置：p.4，§3.2 末段。
- [READER_INTERPRETATION] “dynamic indexing/linking”实际是两阶段：dense top-k 限定候选范围，LLM 只在候选中决定语义关系；不是全库开放式 link discovery。
- [OPEN_QUESTION] Eq. (6) 讨论新 memory `m_n` 的 link set，却写 `L_i ← LLM(...)`，而后又写“Each generated link `l_i` is structured as `L_i={m_i,...,m_k}`”。`i/n` 下标、单条 link 与 link set 被混用，边的精确定义不清。
- [OPEN_QUESTION] Appendix B.2 的 `Ps2` 只问“Should this memory be evolved?”，没有要求返回 link IDs、link type、direction、confidence 或结构化 output schema。该 prompt 与正文“Link Generation”公式不足以唯一复现连接写入。

### 1.3 Memory Evolution：新记忆触发旧 note 的原位替换

- [AUTHOR_FACT] 对每个 `m_j∈M_n^near`，LLM 接收新 memory、除 `m_j` 外的其他近邻、`m_j` 与 `Ps3`，输出 `m_j*`；随后 `m_j*` replaces original `m_j`。位置：p.4–5，§3.3，Eq. (7)；短定位：“replaces the original memory”。
- [AUTHOR_FACT] 正文说 evolution 可更新旧 memory 的 context、keywords 与 tags。位置：p.5，§3.3 首段。
- [AUTHOR_FACT] `Ps3` 的自然语言动作写 `strengthen`、`update_neighbor`；其 JSON schema 的 `actions` 示例却写 `strengthen/merge/prune`，同时返回 suggested connections、updated tags、neighbor contexts/tags。位置：p.20，Appendix B.3。
- [READER_INTERPRETATION] 第二项 changed computation 是“新写入不仅增加一个 node，还可重写 top-k 旧 notes 的生成属性及关系”。这是主动 memory rewrite，而不只是追加/链接。
- [OPEN_QUESTION] Eq. (7) 把输出写成完整 `m_j*`，但 prompt 只清楚定义 context/tags/link相关字段；原始 `c_j`、timestamp、keywords、embedding、旧 links 如何保留或更新没有形式化。
- [OPEN_QUESTION] 原文没有说明 context/tags/keywords 变化后是否重新计算 `e_j`。若不 re-embed，evolution 不能改变后续向量检索；若 re-embed，则需定义索引更新、级联影响与一致性。

### 1.4 Retrieval：公式与 Figure 2 的 link expansion 未闭合

- [AUTHOR_FACT] 查询 `q` 用相同 text encoder编码，与全部 note embeddings 做 cosine similarity，再取 top-k `M_retrieved`。位置：p.5，§3.4，Eqs. (8)–(10)。
- [AUTHOR_FACT] Figure 2 caption 另称：当一个相关 memory 被检索，同一 “box” 中 linked similar memories 也会 automatically accessed。位置：p.3，Figure 2 caption。
- [READER_INTERPRETATION] 查询侧只编码 raw query，而 memory 侧编码 raw content + LLM-generated keywords/tags/context；这是非对称表示，但仍在同一 MiniLM空间比较。
- [OPEN_QUESTION] Eq. (10) 只定义向量 top-k，没有 link-neighbor expansion、box traversal、去重、hop数或最终 context budget。Figure 2 的自动访问行为与公式/Appendix没有实现级闭合。

## 2. 输入、输出、可用信息与干预时点

| 阶段 | 输入/可用信息 | 输出 | 干预时点 | 定位 |
|---|---|---|---|---|
| Note construction | 当前 interaction content、timestamp、`Ps1` | keywords/tags/context 与 enriched embedding | 每次新记忆写入时 | [AUTHOR_FACT] p.4 Eqs. (1)–(3)；p.19 |
| Candidate linking | 新 note embedding、全库旧 embeddings、top-k | 候选近邻集合 | note 构造后 | [AUTHOR_FACT] p.4 Eqs. (4)–(5) |
| LLM link decision | 新 note + top-k neighbors + `Ps2` | 作者所称的 link set/boxes | candidate retrieval 后 | [AUTHOR_FACT] p.4 Eq. (6)；[OPEN_QUESTION] p.19 output schema 缺失 |
| Old-memory evolution | 新 note、目标旧 note、其他近邻、`Ps3` | 旧 note 的 context/tags/links 等改写 | link generation 后、每次新写入时 | [AUTHOR_FACT] p.4–5 Eq. (7)；p.20 |
| Query retrieval | raw query embedding、memory embeddings | top-k notes；图示还称扩展到 linked notes | 每轮回答前 | [AUTHOR_FACT] p.3 Figure 2；p.5 Eqs. (8)–(10) |
| Answer generation | query + retrieved memory context +统一 system prompt | QA response | retrieval 后 | [AUTHOR_FACT] p.5–7 §4；p.21 example |

- [AUTHOR_FACT] 全部实验固定 embedding model 为 `all-minilm-l6-v2`。位置：p.6，§4.2。
- [AUTHOR_FACT] 本地 Qwen/Llama 用 Ollama部署并通过 LiteLLM生成 structured output；GPT使用官方 structured output API。位置：p.6，§4.2。
- [READER_INTERPRETATION] structured-output遵循度可能随底模与接口不同，直接影响 note/link/evolution JSON有效率；论文未单独报告 parse failure/retry率。

## 3. 最强基线与最近组合基线

### 3.1 外部 baselines

- [AUTHOR_FACT] LoCoMo baseline把完整 preceding conversation与问题放入prompt；ReadAgent做pagination/gisting/lookup；MemoryBank含Ebbinghaus forgetting与user portrait；MemGPT采用main/external context层级。位置：p.5 §4.1；p.14 Appendix A.1。
- [AUTHOR_FACT] 论文称所有 baselines 与 A-MEM 使用相同 system prompts。位置：p.6，§4.2。
- [READER_INTERPRETATION] 主表不存在单一永远最强 baseline：GPT模型的Open Domain、Single Hop、Adversarial中，LoCoMo或MemGPT常优于A-MEM；非GPT小模型与Multi-Hop/Temporal上A-MEM优势更一致。位置：p.6 Table 1；p.16–17 Tables 5–7。
- [AUTHOR_FACT] DialSim只比较LoCoMo、MemGPT、A-MEM；A-MEM F1=3.45，LoCoMo=2.55，MemGPT=1.18。位置：p.7 Table 2。

### 3.2 最近组合 baseline 与 ablation

- [AUTHOR_FACT] `w/o LG & ME` 去掉 link generation 和 memory evolution；`w/o ME` 保留 link generation、去掉 evolution；full A-MEM含两者。位置：p.7，Table 3/§4.4。
- [READER_INTERPRETATION] 最接近的内部组合 baseline 是 `w/o LG & ME`：它应保留 note construction + dense top-k retrieval，可隔离“丰富 note/retrieval”与“links/evolution”的增益；`w/o ME`进一步估计在已有LG上的evolution增量。
- [OPEN_QUESTION] 缺少 `w/o LG` 但保留 ME 的对称 ablation；由于 evolution候选本身来自embedding top-k，是否概念上可独立于link generation也未说明。
- [AUTHOR_FACT] Related Work讨论Mem0 graph database，但实验没有比较Mem0。位置：p.1–3 §1/§2.1。
- [READER_INTERPRETATION] 最近外部组合 baseline应是“相同LLM-enriched notes + MiniLM top-k +静态graph/link retrieval但不重写旧notes”；论文没有该对照，因而不能把增益唯一归因于memory evolution而非note enrichment或graph expansion。

## 4. 底模依赖、模型/上下文公平性与结果边界

### 4.1 底模依赖是作者明示限制

- [AUTHOR_FACT] 作者明确承认memory organization质量受底层LLM能力影响，不同LLM会生成不同context descriptions与connections。位置：p.9，§6 Limitations。
- [AUTHOR_FACT] 主表覆盖GPT-4o-mini、GPT-4o、Qwen2.5-1.5B/3B、Llama3.2-1B/3B；附录另报DeepSeek-R1-32B、Claude 3.0/3.5 Haiku。位置：p.6 Table 1；p.17 Table 7。
- [AUTHOR_FACT] DeepSeek-R1-32B的Adversarial F1中，MemGPT=30.77，高于A-MEM=27.92；GPT系列也存在A-MEM并非各类别最优的情况。位置：p.17 Table 7；p.6 Table 1。
- [READER_INTERPRETATION] “across models总体改善”不等于“每模型每类别SOTA”；应限定为跨多底模大多数组合、尤其non-GPT与multi-hop/temporal上表现更强。

### 4.2 Retrieval k 并非统一

- [AUTHOR_FACT] 主文说主要使用 `k=10`，特定类别会调整；Table 8显示GPT-4o-mini/GPT-4o实际为Multi-Hop 40、Temporal 40、Open Domain 50、Single Hop 50、Adversarial 40。位置：p.6 §4.2；p.18 Table 8。
- [AUTHOR_FACT] Qwen/Llama多数类别为10，但Qwen2.5-3B Open Domain=50，Llama3.2-3B Temporal=20。位置：p.18 Table 8。
- [READER_INTERPRETATION] GPT主结果并非“k=10设置”；category/model-specific k显著改变上下文量，可能是底模性能差异和token length的混杂来源。
- [OPEN_QUESTION] k在何种split上选择、是否按test category调优、link-generation候选k是否与answer retrieval k共用均未报告。

### 4.3 Hyperparameter与统计边界

- [AUTHOR_FACT] Figure 3测试k=10/20/30/40/50，作者报告增益通常逐渐plateau，有时高k略降，原因可能是噪声与长序列处理负担。位置：p.7–8，§4.5，Figure 3。
- [AUTHOR_FACT] NeurIPS checklist明确回答未报告error bars/statistical significance，理由是LLM API多次调用成本高。位置：p.25，Checklist item 7。
- [OPEN_QUESTION] 主表未给runs、sampling temperature、random seed、confidence interval或显著性；细小差异不能视为稳定胜出。

## 5. 成本、token与scaling边界

### 5.1 Token/cost口径

- [AUTHOR_FACT] Table 1后的正文将Token Length定义为“answering one question”的平均token length。位置：p.6，Table 1后首句。
- [AUTHOR_FACT] Table 1中A-MEM约1,126–2,520 tokens，而LoCoMo/MemGPT约16,900；正文概括为约1,200 tokens、85–93%减少，并声称每个memory operation商业API成本低于$0.0003。位置：p.6–7，§4.3 “Cost-Efficiency Analysis”；p.16正文也写1,200–2,500。
- [READER_INTERPRETATION] 表的直接可核口径是“回答时上下文/生成token”，不是完整write lifecycle。A-MEM每次写入至少可能调用note construction、link generation和多个neighbor evolution LLM calls；这些成本没有被Table 1逐项展开。
- [OPEN_QUESTION] `$0.0003`未绑定provider/model、输入输出价格、计价日期、平均top-k evolution数或是否包含写入/改写；不能据此核验端到端memory-operation成本。

### 5.2 Latency与检索scaling

- [AUTHOR_FACT] 作者报告平均processing time：GPT-4o-mini 5.4秒，单GPU本地Llama3.2-1B 1.1秒。位置：p.7，§4.3。
- [OPEN_QUESTION] 未给GPU型号、CPU、index/library、batch/concurrency、数据库、网络环境、测量次数或percentiles；checklist item 8虽回答“实验部分可找到”，正文并不足以复现compute。
- [AUTHOR_FACT] Table 4把A-MEM向量检索时间写为1k时0.31µs、1M时3.70µs；MemoryBank略快，ReadAgent显著慢。位置：p.8，Table 4/§4.6。
- [READER_INTERPRETATION] 该表只可能代表某种索引查找microbenchmark，不包含query encoding、LLM link/evolution、linked-neighbor expansion或prompt generation；不得与5.4秒端到端processing time混写。
- [OPEN_QUESTION] 表称三系统memory usage完全相同，并据此说A-MEM无额外storage overhead；但A-MEM声明额外存keywords/tags/context/links。测量似乎只覆盖相同vector content或index，metadata/graph/versioning是否排除未说明。
- [OPEN_QUESTION] §4.6称vector-based retrieval空间O(N)且Table 4时间仅随1,000倍规模增长约12倍；实际索引算法、exact/ANN、warm cache与单位均未给出，scaling主张不可精确复现。

## 6. 旧记忆重写与provenance风险

- [AUTHOR_FACT] Eq. (7)明确说evolved `m_j*` replaces original `m_j`。位置：p.5，§3.3。
- [AUTHOR_FACT] Prompt允许update neighbor context/tags，JSON action示例还含merge/prune。位置：p.20 Appendix B.3。
- [READER_INTERPRETATION] 这是原位语义重写：即便原始`c_j/t_j`可能仍保留，检索代理字段会被后续LLM解释覆盖，旧note的搜索可见性与关系会随未来输入变化。
- [OPEN_QUESTION] 全文没有version history、source-span引用、修改者/model/version、旧新diff、confidence、审核状态、rollback、tombstone或append-only lineage；定向复核也未出现provenance/audit/rollback定义。
- [READER_INTERPRETATION] 新note若误导link/evolution，错误可传播到多个top-k neighbors，随后影响embedding（若re-embed）、links与未来retrieval，形成累积memory drift/poisoning风险。
- [OPEN_QUESTION] `merge/prune`是否删除原文、只删link还是合并attributes未定义；没有冲突事实、时间变化、撤销、重复note或隐私删除策略。
- [AUTHOR_FACT] Checklist broader impacts回答“No”，理由是不同agent的社会影响超出memory system范围；safeguards为NA。位置：p.26–27，items 10–11。
- [READER_INTERPRETATION] 对会长期保存并重写对话记忆的系统，隐私、错误传播与删除可追溯性本身属于memory层风险；原文Limitations只讨论底模差异和multimodal扩展，范围很窄。

## 7. 作者负结果、限制与未测试边界

### 7.1 可直接记录的负向结果

- [AUTHOR_FACT] 高k的收益plateau且部分任务略降，作者归因为噪声与长上下文处理负担。位置：p.7–8 §4.5/Figure 3。
- [AUTHOR_FACT] A-MEM并非GPT/DeepSeek所有类别最优，例如DeepSeek Adversarial落后MemGPT；GPT Open Domain/Single Hop/Adversarial也存在LoCoMo/MemGPT更强。位置：p.6 Table 1；p.17 Table 7。
- [AUTHOR_FACT] 去掉LG/ME或仅保留LG均明显低于full A-MEM；这也是组件缺失时的observed degradation。位置：p.7 Table 3。
- [AUTHOR_FACT] 作者承认底模能力会改变memory organization质量。位置：p.9 §6。

### 7.2 未测试/证据不足

- [OPEN_QUESTION] 未测试multimodal memory，作者将其列为future work。位置：p.9 §6。
- [OPEN_QUESTION] 未评估长时间反复evolution后的fact retention、revision accuracy、catastrophic drift、link precision/recall、provenance fidelity、conflict handling或memory deletion。
- [OPEN_QUESTION] Link/evolution没有人工gold评价；下游QA improvement不能区分正确links、偶然prompt enrichment或answer-model prior。
- [READER_INTERPRETATION] T-SNE只展示10段dialogue的二维投影，无cluster metric、seed、perplexity或链接质量标注；更紧cluster不能单独证明语义组织正确。位置：p.9 Figure 4；p.16–18 Figure 5。
- [AUTHOR_FACT] Checklist item 7确认无统计显著性信息。位置：p.25。

## 8. 公式、prompt与实现歧义清单

1. [OPEN_QUESTION] **Eq. (6)下标/类型歧义**：新note应更新`L_n`却写`L_i`；单link与memory-set类型混用。位置：p.4。
2. [OPEN_QUESTION] **Link prompt无输出协议**：`Ps2`只问是否evolve，不要求link IDs/direction/type。位置：p.19。
3. [OPEN_QUESTION] **Evolution动作词冲突**：正文/自然语言写`update_neighbor`，JSON actions列`merge/prune`，但语义未定义。位置：p.20。
4. [OPEN_QUESTION] **旧note字段保存不明**：Eq. (7)整note替换，prompt只更新context/tags/links；content/timestamp/keywords/embedding如何处理不明。位置：p.5、p.20。
5. [OPEN_QUESTION] **embedding/index更新缺失**：改写生成属性后无re-embedding/reindex步骤。位置：p.4–5。
6. [OPEN_QUESTION] **link方向/对称性缺失**：写入新note link时，旧note的`L_j`是否反向更新没有公式。
7. [OPEN_QUESTION] **retrieval link expansion缺失**：Figure 2称same-box linked memories自动访问，Eq. (10)只有top-k。位置：p.3、p.5。
8. [OPEN_QUESTION] **k复用歧义**：link candidate top-k与answer retrieval top-k是否同值、Table 8适用于哪一步不明。位置：p.4–6、p.18。
9. [OPEN_QUESTION] **always-top-k无阈值**：无similarity threshold/tie规则；无关近邻是否被LLM拒绝、是否仍触发evolution依赖未定义prompt行为。
10. [AUTHOR_FACT] **Checklist LLM declaration矛盾**：item 16把核心方法LLM usage回答为NA，但note construction、link generation、memory evolution均以LLM为核心非标准组件。位置：p.4–5、p.19–20 vs p.28。

## 9. Operator 与 Failure 候选

以下仅为二读候选，供主Codex reconciliation；不是正式Card。

### 9.1 Operator候选

1. [READER_INTERPRETATION] **LLM-enriched atomic note indexing**：原交互→keywords/tags/context→拼接embedding。证据：p.4 Eqs. (1)–(3)。
2. [READER_INTERPRETATION] **Dense-candidate + LLM link adjudication**：cosine top-k先缩小候选，再由LLM判连接。证据：p.4 Eqs. (4)–(6)。
3. [READER_INTERPRETATION] **Neighbor-triggered memory rewrite**：新note触发top-k旧notes的context/tag/link evolution并替换原记录。证据：p.4–5 Eq. (7)。
4. [READER_INTERPRETATION] **Category/model-adaptive retrieval k**：按底模与题型选择10–50个memories。证据：p.7–8 Figure 3；p.18 Table 8。
5. [READER_INTERPRETATION] **Linked-box retrieval expansion（设计声称）**：top-k命中后自动带出同box linked notes。证据：p.3 Figure 2 caption；实现未闭合，应标设计operator而非已核实实现。

### 9.2 Failure候选

1. [AUTHOR_FACT] **context overload/noise at high k**：更大k收益plateau并可下降。位置：p.7–8 Figure 3。
2. [AUTHOR_FACT] **底模依赖的组织漂移**：不同LLM产生不同descriptions/connections。位置：p.9 §6。
3. [AUTHOR_FACT] **特定模型/类别不胜基线**：GPT/DeepSeek若干Open Domain/Single Hop/Adversarial格子落后。位置：p.6、p.17。
4. [READER_INTERPRETATION] **unversioned rewrite provenance loss**：旧note原位替换且无diff/rollback/source lineage。位置：p.5、p.20；全文未给控制。
5. [READER_INTERPRETATION] **stale embedding after evolution**：若未re-embed，新context/tags不改变dense retrieval；若re-embed，索引一致性未定义。位置：p.4–5。
6. [READER_INTERPRETATION] **link retrieval specification gap**：Figure 2与Eq. (10)不一致，link的性能贡献无法机械复现。位置：p.3、p.5。
7. [READER_INTERPRETATION] **成本口径遗漏write amplification**：回答token节省不等于多次写入/evolution调用的总成本。位置：p.6–7。
8. [READER_INTERPRETATION] **T-SNE organization proxy不足**：投影cluster不能验证link正确性。位置：p.9、p.18。

## 10. 解析文本与可视PDF冲突核查

- [AUTHOR_FACT] 已读取28/28页文本层，并逐页检查可视版面；重点放大Figures 1–5、Tables 1–8、Eqs. (1)–(25)与Appendix B prompts。
- [READER_INTERPRETATION] 未发现会反转主表数值的视觉—文本冲突，但有以下解析限制：
  - p.1竖排arXiv identifier/date被抽入摘要正文；视觉页显示为页边元数据。
  - p.3 Figure 2、p.6/16/17大型表格、p.8 Figure 3/Table 4、p.18 Figure 5/Table 8在纯文本中列顺序严重错乱；本报告以视觉表格与相邻正文共同核对。
  - p.18 Figure 5含大量vector paths，文本层不能表达cluster形态；视觉页只支持“二维点分布不同”的描述，不支持精确结构指标。
  - p.19–21 boxed prompt/example的换行在文本层损失，但关键字段与动作词经视觉核验。
- [READER_INTERPRETATION] §8的Eq./prompt差异是原文自身的不闭合，不是parser造成。

## 11. 最小结论边界

- [AUTHOR_FACT] A-MEM将原始交互扩展为LLM-enriched notes，用dense top-k+LLM建立关系，并允许新记忆改写旧note属性；在LoCoMo/DialSim多模型QA上报告较强结果与显著回答上下文压缩。
- [READER_INTERPRETATION] 可支持的最窄changed-computation结论是：“在memory写入时增加LLM生成的检索代理字段、候选link判定和旧neighbor语义改写；回答时再做MiniLM top-k retrieval。”
- [READER_INTERPRETATION] 不能由本文直接推出的更强结论包括：link graph实现已完整定义、evolution可审计且不会fact drift、端到端memory operation只需约1,200 tokens、无额外storage、所有底模/类别均SOTA、或T-SNE cluster证明连接正确。

## 12. 可观察访问边界与工具轨迹

1. 本轮沿用线程中已加载的统一二读规则，不重新读取任何规则文件。
2. 精确读取P063本attempt的`invocation.md`与统一`knowledge_base/templates/second_read_prompt.md`。
3. 仅对指定`P063_a_mem.pdf`执行SHA-256、PyMuPDF page count/metadata、p.1–28逐页文本读取、逐页内存渲染及关键图表放大；未写临时图片。
4. 仅在同一PDF已读文本中定向复核`recompute/re-embed/version/provenance/audit/rollback/replace/merge/prune/same box/token length/memory operation/GPU/seed/error bars/k`等词及页码。
5. 未联网；未枚举工作区；未读取read_1、Cards、其他报告、其他论文读稿、Corpus/saturation/retrieval/blind文件。
6. 唯一写入目标为本文件`knowledge_base/corpus/reads/P063/read_2_attempts/r2-20260720-p063-a1/report.md`，写入方式为`apply_patch`。
