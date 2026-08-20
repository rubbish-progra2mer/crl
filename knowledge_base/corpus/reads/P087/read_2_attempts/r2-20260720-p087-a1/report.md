# P087 独立二读报告

- Attempt ID：`r2-20260720-p087-a1`
- 指定来源：`P087_tool_rex.pdf`
- 来源 SHA-256：`0e6dc98171a7ada43eb7b2a415099853afb090f29c25887d512660501d343eff`（本次实算一致）
- 来源范围：仅对所给 21 个物理 PDF 页作判断；不推断未读终稿或后续版本。
- 标签：`AUTHOR_FACT` 表示作者在这些 bytes 中直接报告的事实；`AUTHOR_INTERPRETATION` 表示作者对结果的解释；`AUDIT_JUDGMENT` 表示本次二读基于这些 bytes 作出的审计判断。

## 1. 这些 bytes 中可见的规范元数据

- `AUTHOR_FACT` 标题：*Tools are under-documented: Simple Document Expansion Boosts Tool Retrieval*（物理 PDF 第 1 页，标题区）。
- `AUTHOR_FACT` 作者：Xuan Lu、Haohang Huang（共同一作标记）、Rui Meng、Yaohui Jin、Wenjun Zeng、Xiaoyu Shen（通讯作者标记）；Rui Meng 标注工作单位为 Google Cloud AI Research（第 1 页作者与脚注区）。
- `AUTHOR_FACT` 署名单位：Shanghai Jiao Tong University；Ningbo Key Laboratory of Spatial Intelligence and Digital Derivative；Institute of Digital Twin, Eastern Institute of Technology, Ningbo（第 1 页）。
- `AUTHOR_FACT` 首页明确显示 `arXiv:2510.22670v1 [cs.IR] 26 Oct 2025`；因此本报告只把它识别为 arXiv v1，不把它称作会议终稿或最终版本（第 1 页左侧版本标识）。
- `AUTHOR_FACT` PDF 元数据中的标题与作者顺序和首页相符；Creator 为 `arXiv GenPDF (tex2pdf:e76afa9)`。正文脚注给出代码地址 `https://github.com/EIT-NLP/Tool-DE`，但本次未访问该地址（第 1 页脚注）。

## 2. ToolRet 文档问题与作者审计

### 2.1 作者报告的问题

- `AUTHOR_FACT` 作者称 ToolRet 汇集 35 个工具使用数据集，形成约 7.6k retrieval tasks 和 43k tools，并分成 Web、Code、Customized 三域（第 3 页，§2.1，定位语 “7.6k retrieval tasks”）。
- `AUTHOR_FACT` 作者把原始文档问题分为两类：字段命名/表达异构，以及信息不完整。附录把观察到的原始字段归一为 8 类：`name`、`description`、`category`、`parameters`、`responses`、`method`、`example usage`、`limitations`（第 13–14 页，§A.2，表 4）。同一功能类字段据称最多出现 7 种表达；MNMS 被举作缺少 `description` 的例子（第 3、14 页，§2.1、§A.3，图 4）。
- `AUTHOR_FACT` 作者的“不完整”判据只有两项：是否有清楚的功能陈述、是否有上下文使用指导；两者任一缺失即标为不完整。每域随机抽 100 份，共 300 份，由未具名 LLM 输出单一 `true/false`（第 14–15 页，§A.4，图 5）。作者报告扩展前不完整率 41.6%，扩展后 23.5%（第 14 页）。
- `AUTHOR_INTERPRETATION` 作者据此认为文档缺陷是检索语义差距和性能上限的根因，扩展能改善关键字段覆盖（第 2–3、14 页）。

### 2.2 二读审计

- `AUDIT_JUDGMENT` “35 个数据集”的可复核性有内部缺口：§A.1 实际逐名列出 15 个 Web、6 个 Code、7 个 Customized，共 28 个；图 4 的可见列也对应这批名称，而正文/图注仍称 35 个。缺少的 7 个来源没有在这些 bytes 中解释（第 13–14 页，§A.1、图 4）。
- `AUDIT_JUDGMENT` 审计没有报告判定 LLM 的模型、版本、解码配置、抽样种子、逐域计数、扩展前后是否使用同一 300 份文档，也没有人工复核该审计标签。尤其在 300 个二元样本的口径下，23.5% 对应 70.5 份文档，无法直接还原为整数计数；41.6% 也未给原始计数。故两个百分比只能作为作者报告值，不能从本文复算（第 14–15 页，§A.4、图 5）。
- `AUDIT_JUDGMENT` 这个二元审计只覆盖“功能陈述/使用上下文”，不验证参数、响应、调用方法、前置条件等完整性；因此 41.6%→23.5% 不能解释为完整 API schema 的总体正确率提升。
- `AUDIT_JUDGMENT` 作者一方面要求 optional fields 仅在原文“明确支持”时生成，另一方面声称修复缺失信息。严格遵守该约束时，系统能标准化、显化或改写原文已有/隐含信息，却不能恢复原文真正没有提供的事实。这限制了“从源头修复缺文档”的强解释（第 3–4、17 页，§2.2、图 6）。
- `AUDIT_JUDGMENT` 附录案例暴露了 grounding 风险：Web 案例的 `when_to_use` 引入“planning movie outings”等原文未明确陈述的场景；Code 案例把 “specific value” 改成 “specific query”；Customized 案例从“Send money”推出 “not receiving money”，并把 `money transfer` 与 `send money` 同列为 tags，分别触及“不得假设限制/保持语义一致/不重复”的生成规则（第 19–21 页，图 9–11；规则见第 17 页图 6）。这些只是案例级反例，足以否定“展示样例均严格符合规则”，但不足以估计全语料错误率。

## 3. 结构化扩展字段与四阶段流程

### 3.1 字段

| 字段 | 作者规则 | 最终检索配置 |
|---|---|---|
| `function`（正文写作 `function description`） | 必选；少于 20 词；概括核心功能 | 保留 |
| `tags` | 必选；3–5 个小写关键词/短语，覆盖主题、操作和同义词 | 保留 |
| `when_to_use` | 可选；少于 20 词；仅在原文明确支持时生成 | 保留 |
| `limitation`（正文多写作 `limitations`） | 可选；仅记录原文明示的限制、rate limit 或特殊条件 | 保留 |
| `example_usage` | 可选；最多 2 个，每个可含 `query` 与参数一致的 `api_call`；仅可由原文字段直接构造 | 在最终检索 profile 中删除 |

`AUTHOR_FACT` 字段规则来自第 3–4 页 §2.2 和第 17 页图 6。生成的 `tool_profile` 与原始文档合并，作者写为 `d_expansion = d_original ∪ d_profile`；扩展不依赖查询（第 4 页）。

`AUDIT_JUDGMENT` 正文与实际 prompt 的 schema 名不完全一致：`function description`/`function`、`limitations`/`limitation` 混用；这会影响严格复现、序列化与字段级消融定义。本文也未说明 JSON profile 如何序列化成 retriever 的最终输入文本、字段顺序以及截断策略。

### 3.2 阶段

| 阶段 | `AUTHOR_FACT` |
|---|---|
| Expansion | Qwen3-32B 开启 reasoning mode，以原始工具文档生成 profile；必选字段必须输出，可选字段无明确依据则省略（第 3–4 页，§2.2；第 17 页图 6）。 |
| Judgement | 先做非空与合法 JSON 规则检查，再由 LLaMA-3.1-70B 判断 profile 是否忠于原文；prompt 只输出整体 `true/false`（第 4、18 页，图 7）。 |
| Refinement | 约 1.5%、约 600 个未通过样本由 GPT-4o 使用与 Step 1 相同的 prompt 重新生成（第 4 页）。 |
| Human validation | 从 Step 3 重生成结果随机抽 100 个，按 faithfulness、completeness、hallucination、consistency 评估；作者称 100 个均通过（第 4、15–16 页，§C）。 |

- `AUDIT_JUDGMENT` 图 1 可视流程实际只画到生成、判定、GPT-4o 回退和新文档，没有画出声称的第四阶段人工验证（第 3 页图 1）。
- `AUDIT_JUDGMENT` Judgement 被正文描述为检查“each expanded field”，但图 7 只要求单一整体布尔值，没有字段级理由或错误定位。GPT-4o 重生成后是否再次经过相同 judge 没有写明。
- `AUDIT_JUDGMENT` 人工验证只抽 Step 3 的 100 个回退样本，不覆盖约 98.5% 被自动接受的 profile；本文只给一个“代表性 annotator”背景，未给标注者总数、每例标注人数、一致性统计或分歧裁决。“unanimously”因而无法独立复核（第 15–16 页，表 5、指南）。

## 4. Tool-Embed 与 Tool-Rank 训练

### 4.1 `AUTHOR_FACT`

- Tool-Embed：以 Qwen3-Embedding-0.6B 和 4B 为底座；`ms-swift`；InfoNCE；50k query–tool pairs；每个正对随机抽取来自其他 query 的 5 个 tools 作负样本；全参数训练 1 epoch；DeepSpeed ZeRO-3（第 5 页，§2.3，定位语 “randomly sample 5 tools”）。
- Tool-Rank：以 Qwen3-Reranker-4B 为底座；LLaMA-Factory；cross-entropy；LoRA `r=32, α=64, dropout=0.1`；200k reranking instances；1 epoch。评测时对 query–document pair 输出 `true/false` token logits，经二项 softmax 得到 relevant score（第 5 页，§2.3；prompt 见第 18 页图 8）。
- 两个 `original` 对照删除训练数据中的 `tool_profile`，其余数据对与训练配置声称保持相同（第 5、8 页）。
- 作者称所有实验使用 2 张 NVIDIA A100 80GB（第 4–5 页，§2.3、§3.1）。

### 4.2 `AUDIT_JUDGMENT`

- 本文没有给学习率、optimizer、batch size、max sequence length、随机种子、训练步数/墙钟时间、负样本去重或 hard-negative 规则，也没有给 50k/200k 样本从约 43k tools 和 7.6k tasks 构造出来的完整配方。因此无法仅据本文复现实验训练。
- “固定训练预算”的作者解释最多指数据对数/epoch/声称相同超参数；没有 GPU-hours、峰值显存、总 token 或能耗，不能把它解释为严格的等算力比较。
- 扩展生成侧使用 Qwen3-32B、LLaMA-3.1-70B 和约 600 次 GPT-4o 回退，但本文没有报告生成硬件、吞吐、token 数、API 价格或总成本；“low-cost/scalable”是未量化的作者判断，不是本文可复算的成本事实。

## 5. 匹配的扩展/非扩展结果

### 5.1 同一现成 retriever：ToolRet 原文档 vs TOOL-DE 扩展文档

下表均为表 2 的 Avg.；这是本文最直接的 evaluation-time 配对，模型不变、文档视图改变。

| 模型 | ToolRet N/R/C@10 | TOOL-DE N/R/C@10 | 差值 N/R/C |
|---|---:|---:|---:|
| BM25s | 36.41 / 46.40 / 39.02 | 39.35 / 48.17 / 40.08 | +2.94 / +1.77 / +1.06 |
| GritLM-7B | 41.13 / 51.28 / 40.37 | 43.54 / 54.07 / 43.57 | +2.41 / +2.79 / +3.20 |
| NV-Embed-v1 | 42.71 / 53.43 / 43.41 | 43.21 / 54.00 / 43.71 | +0.50 / +0.57 / +0.30 |
| gte-Qwen2-1.5B | 41.27 / 51.62 / 40.57 | 41.78 / 51.94 / 41.03 | +0.51 / +0.32 / +0.46 |
| e5-mistral-7B | 40.02 / 50.10 / 40.59 | 38.85 / 49.13 / 40.09 | -1.17 / -0.97 / -0.50 |
| Qwen3-Embedding-0.6B | 43.13 / 52.80 / 42.97 | 43.30 / 52.89 / 43.03 | +0.17 / +0.09 / +0.06 |
| Qwen3-Embedding-4B | 45.54 / 57.36 / 47.27 | 45.65 / 56.13 / 46.04 | +0.11 / -1.23 / -1.23 |
| Qwen3-Embedding-8B | 46.21 / 57.52 / 47.52 | 46.23 / 56.83 / 46.70 | +0.02 / -0.69 / -0.82 |

`AUDIT_JUDGMENT` 扩展不是普遍有益：e5 三项均下降；Qwen3-4B/8B 的平均 NDCG 近乎不变而 Recall、Completeness 下降。作者对此只部分承认（第 6–7 页，表 2、§3.2）。

### 5.2 专用训练与 reranking

- `AUTHOR_FACT` 原文档链：Tool-Embedoriginal-4B 为 49.21 / 60.00 / 49.47；Tool-Rankoriginal-4B rerank 后为 51.21 / 62.47 / 51.31，即 +2.00 / +2.47 / +1.84（第 6 页，表 3）。
- `AUTHOR_FACT` 扩展文档链：Tool-Embed-4B 为 52.23 / 63.13 / 51.61；Tool-Rank-4B 后为 56.44 / 67.81 / 56.60，即 +4.21 / +4.68 / +4.99（第 6–7 页，表 3、§3.2）。所有 TOOL-DE reranker 对 Tool-Embed-4B 的 top-100 结果重排。
- `AUDIT_JUDGMENT` 这两条链同时改变训练文档和评测文档，不是训练扩展的单变量隔离。表 2/3 未报告 `expanded-trained × original-eval` 与 `original-trained × expanded-eval` 两个交叉格；因此第 8 页所称“即便测试文档不扩展也持续提升”没有在这些表中呈现。
- `AUDIT_JUDGMENT` 摘要/第 2 页的 +10.23/+10.29/+9.08 正好用 Tool-Rank 的 TOOL-DE 结果减去 Qwen3-Embedding-8B 的 **ToolRet** 结果（56.44−46.21、67.81−57.52、56.60−47.52），混合了两种文档视图；若减同表 TOOL-DE 的 46.23/56.83/46.70，则是 +10.21/+10.98/+9.90。该处“相对 MTEB SoTA”的数值不是同一 evaluation view 的公平差值。
- `AUDIT_JUDGMENT` 表 3 标题说所有 reranker 都以 Tool-Embed-4B 为初始结果，但 ToolRet 区块实际基线写作 Tool-Embedoriginal-4B；第 9 页又把 jina 在原文档上的变化写成 −0.56，而表 3 与第 7 页均为 −0.08。本文未提供能解释 −0.56 的独立结果表。

## 6. 字段消融与有害字段

- `AUTHOR_FACT` Add-One 从原文档出发每次加一个字段；One-Out 从完整扩展出发每次去掉一个字段；指标为 NDCG@10（第 7–8 页，§4.1、图 2）。
- `AUTHOR_FACT` 图 2 与正文一致支持：`example_usage` 的 Add-One 收益最小、对 GritLM 甚至有害；One-Out 删除它优于保留完整扩展。`function` 与 `tags` 在 Add-One 中中性到正向，One-Out 删除时有可见下降；图注还把 `function`、`when-to-use` 称为相对更有贡献。最终检索 profile 因此删除 `example_usage`，保留 function、when-to-use、limitations、tags（第 8 页）。
- `AUTHOR_FACT` 文档平均 token 长度从 131.72 增至 177.61（profile 平均 45.89）；Code 167.62→219.43、Customized 71.55→115.34、Web 156.00→198.05（第 4 页，表 1）。
- `AUDIT_JUDGMENT` 第 4 页却写“removing when_to_use yields better performance”，下一句又据此删除 `example_usage`；第 8 页和图 2 明确支持后者，因此前一句是关键字段名冲突。
- `AUDIT_JUDGMENT` §4.1 开头称使用 Qwen3-Embeddings-8B 与 BM25，实际图 2 标题/图注是 GritLM 与 BM25s。图只给雷达图，没有精确数值表、方差、显著性、分域结果或 truncation rate。作者提出“更长输入可能稀释/截断”是合理风险陈述，但这些 bytes 未展示截断控制实验。

## 7. 相似度稀释

`AUTHOR_FACT` 作者每域随机抽 100 个 query（共 300），每个取一个 positive、一个 negative，用 GritLM 比较扩展前后平均 similarity（第 8–9 页，§4.3、图 3）。

| 域 | positive 下降 | negative 下降 | 正负间隔的净增加（由两项相减） |
|---|---:|---:|---:|
| Web | 0.0014 | 0.0055 | 0.0041 |
| Code | 0.0022 | 0.0038 | 0.0016 |
| Customized | 0.0027 | 0.0152 | 0.0125 |

- `AUTHOR_INTERPRETATION` 作者认为长度增加导致绝对相似度下降，但 negative 降得更多，使正负可分性和相对排序改善；扩展也为 reranker 提供更细粒度的语义钩子（第 8–9 页）。
- `AUDIT_JUDGMENT` “长度导致 semantic dilution”在文中明确是 plausible explanation，不是被长度控制实验识别的因果机制。抽样种子、negative 选择/难度、误差条和显著性均未给出；仅凭均值不能判断这种不对称是否稳定到 query 级。
- `AUDIT_JUDGMENT` 第 9 页声称做了“固定 retrieval pool、切换扩展/非扩展视图”的 controlled toggle，但没有给表、图、样本量或数值；该句不能单独支持因果量级。

## 8. 算力、合成数据与迁移边界

- `AUTHOR_FACT` 训练/实验算力仅报告为 2×A100 80GB；生成教师链为 Qwen3-32B→LLaMA-3.1-70B→失败样本 GPT-4o；训练语料约 50k retriever pairs 与 200k reranker instances（第 1、4–5 页）。
- `AUDIT_JUDGMENT` 50k/200k 是 LLM 扩展驱动的派生训练语料，但本文未给 query–tool pair、rerank positives/negatives、split 与去重构造细节，也未报告 train/test 工具或源数据集的重叠审计。不能据这些 bytes排除 source-level leakage 或估计合成噪声率。
- `AUDIT_JUDGMENT` TOOL-DE 是 ToolRet 同一查询、工具与标签上的文档扩展版本；它适合成对测试“改变文档表示”的效果，但不是独立采集的新任务分布。本文没有清晰的 held-out dataset/domain/tool-family 迁移表，也没有真实 MCP registry、持续更新 API、多工具组合或 end-to-end execution 成功率实验。
- `AUDIT_JUDGMENT` 作者把 ToolRet 上的结果解释为向异构未扩展文档泛化，但当前表格只展示 original-trained/original-eval 与 expanded-trained/expanded-eval 两条链，缺少必要交叉格。故可支持的迁移结论应限于：在作者汇总的 Web/Code/Customized ToolRet 派生范围内，文档扩展通常改善若干检索器和 reranker；不能外推为跨语料、跨注册表或下游执行的普适增益。
- `AUDIT_JUDGMENT` 公开的扩展案例仅展示 3 个从 top-10 外升到 rank 4/2/2 的正例（第 16、19–21 页），没有案例选择规则或失败案例；它们只能说明可能机制，不能估计总体提升或错误率。

## 9. 是否构成 schema/description-aware retrieval 的直接先行

- `AUDIT_JUDGMENT` **是直接先行，但需限定 claim。** 对“离线把工具描述扩展成标准化的 function/tags/when-to-use/limitations 文本，拼回文档，并把该表示用于 dense retrieval、BM25、reranker 训练或评测”这一 changed computation，本文是直接、强相关先行：它明确给出字段、生成/校验链、配对原文档/扩展文档结果与字段消融（第 3–8 页）。
- `AUDIT_JUDGMENT` 对“description-aware retrieval”它是直接碰撞；仅改字段名称、prompt 或底座模型不足以绕开该先行。
- `AUDIT_JUDGMENT` 对“schema-aware retrieval”则是**部分直接**：附录分析 `parameters/responses/method` 等 schema 字段，但生成 profile 主要是描述性摘要、场景、限制与 tags；模型侧仍把合并文档当文本输入，没有专门的 typed parameter/output 对齐、字段级编码器、约束匹配或 schema graph computation。若新方法的核心 delta 是这些显式 schema 计算，应把本文作为最近的 document-enrichment comparator，而不能说它已经实现同一种模型计算。
- `AUDIT_JUDGMENT` 本文也不是 query-conditioned 动态扩展、在线路由、多工具规划、调用参数生成或执行验证的直接先行；作者的扩展明确 query-independent，评测终点是 retrieval/reranking 指标。

## 10. 关键定位索引

- 元数据、摘要、主张：物理页 1–2。
- ToolRet 文档缺陷与四阶段流程：物理页 3–4，§2.1–2.2，图 1、表 1。
- Tool-Embed/Tool-Rank 训练：物理页 4–5，§2.3。
- 主结果：物理页 6–7，表 2–3，§3.2。
- 字段消融与相似度：物理页 7–9，§4.1–4.3，图 2–3。
- 数据集枚举、字段归一、覆盖与完整性审计：物理页 13–15，§A.1–A.4，表 4、图 4–5。
- 扩展/judge/rerank prompts、人工指南：物理页 15–18，§B–C，图 6–8、表 5。
- 三个案例：物理页 19–21，图 9–11。

## 11. 本次读取与工具轨迹

- 开始时间（invocation）：`2026-07-20T20:46:09+08:00`；报告落盘前时间：`2026-07-20T20:55:34+08:00`。
- 模型可见标识：`Codex（基于 GPT-5）`；当前上下文未暴露更细 model build/version，故不推断。
- 实际读取范围：工作区根 `AGENTS.md`、`crl_agent_v3/AGENTS.md`、`crl_agent_v3/CRL.md`、`crl_agent_v3/CRL_ENVIRONMENT.md`、`C:\Users\g\.codex\skills\pdf\SKILL.md`；本 attempt 的 `invocation.md`；以及指定 `P087_tool_rex.pdf` 的全部 21 个物理页。未读取或枚举 invocation 禁止的 read_1、Cards、其他 attempts、reconciliation、Corpus Report、history/audit、retrieval calibration/blind、Candidate、Commissioning 或科研 Reviewer 资产。
- 可观察命令/工具：PowerShell `Get-Content` 读取上述指令与 invocation（CRL/Environment 因首次合并输出截断而按明确文件分段重读）；`Get-FileHash -Algorithm SHA256` 核对 PDF；项目 `.venv` 的 PyMuPDF 读取 21 页 metadata/TOC/text（1–5、6–10、11–15、16–21 四段）；首次文本输出因控制台 GBK 不能编码而失败，随后只设置 `PYTHONIOENCODING=utf-8` 重跑；Node REPL + 本机 Chrome 以 `file:///` 打开同一 PDF，对首页、流程/长度、结果表、字段消融/相似度、字段覆盖/审计页作视觉核验。Playwright 默认 bundled Chromium 首次因本机无对应 executable 失败，随后显式使用已安装 Chrome；未安装任何依赖。
- 联网：否。没有 web 搜索、HTTP 请求或外部 API 调用；Chrome 仅访问本地 `file:///` PDF。
- Task ID：`/root/p087_second_read`；Attempt ID：`r2-20260720-p087-a1`。
- 写入范围：只新增本文件。报告 SHA-256 不嵌入正文，以避免自指；落盘后的实算值随交接返回。
