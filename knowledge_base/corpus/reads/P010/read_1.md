# P010 主 Codex 首读

- PDF：`knowledge_base/staging/papers/P010_longmemeval.pdf`
- PDF SHA-256：`c6c6d75072d316d7b040dbbbb9caf7607821e6dd34d986e6f6c7e3e1721179f7`
- 读取时间：`2026-07-19T15:35:00+08:00`
- 读取范围：逐页检查 1–28 页；正文 1–11 页，参考文献 11–16 页，数据构建/评测/商业系统附录 17–21 页，统一形式化与实现细节 22–25 页，扩展模型、retriever、rank merge、时间查询与错误分析 26–28 页。

## Changed computation / 研究对象

- [AUTHOR_FACT] 论文首先构建 500 个问题的长时交互 memory benchmark，覆盖 information extraction、multi-session reasoning、knowledge update、temporal reasoning、abstention；提供约 115k-token 与 500-session/约 1.5M-token 两档历史。
- [AUTHOR_FACT] 方法分析把 memory-augmented assistant 分为 indexing、retrieval、reading 三阶段及 value/key/query/reading 四个 control points；推荐 round value、原值加 fact 的 key expansion、time-aware query filtering、JSON+Chain-of-Note reading。
- [READER_INTERPRETATION] 它不是一个不可分割的新 memory architecture。可迁移资产应拆成互相可消融的四类 Operator 与失败边界，不把 unified view 本身当性能方法。

## Benchmark 数据与评估边界

- 500 个问题由 164 个用户属性上的 LLM background/seed 生成开始，但 human experts 过滤、重写问题并分解 evidence statements；每类约生成 1000 个 seed，最终 yield 约 5%。Evidence session 由 Llama-3 70B self-chat 后人工筛改，约 70% sessions 被编辑。
- 长历史由 25% ShareGPT、25% UltraChat、50% simulated sessions 加 evidence sessions 编译，问题间各自构造 history；这是受控 needle/haystack 式合成历史，而非同一真实用户持续数月的自然演化日志。
- QA judge 为 `gpt-4o-2024-08-06`。每类抽 30 问、分别检查 GPT-4o 与 Llama-3.1-8B 输出，judge 对人类 accuracy 平均 0.98/0.97；preference 与 abstention 某些设置为 0.90。Temporal prompt 容忍 day 数 off-by-one，knowledge-update 允许同时提旧信息，只要含更新答案。
- Commercial study 只选 97 问、3–6 sessions，跳过部分 temporal、全部 assistant-origin 与 abstention，并由五名人工经网页操作；与完整 LONGMEMEVALS 不是同一难度。
- “Oracle”是只给 evidence sessions 的 reading 条件，不是系统整体上界；它移除了 retrieval 干扰但仍受 reader 与 judge 影响。

## 实验控制与主要结果

- 主要 indexing/retrieval 实验使用 Stella V5 1.5B；Llama-3.1-8B 抽 summaries/keyphrases/facts/events；reader 为 GPT-4o、Llama-3.1 70B/8B。Retrieved items 均按 timestamp 排序，§5.2–5.4 默认已启用 JSON 与 CoN，因此各 control point 的表不能与无 CoN 条件直接混合归因。
- Long-context Figure 3b：约 115k-token 全历史相对 evidence-only oracle 下跌约 30–60%；但 CoN 对 Llama 70B/8B、Phi-3/3.5 的 full-history accuracy 并非一致改善，不能表述为 CoN 普遍提升长上下文。
- Value Figure 5：GPT-4o 上 session→round 在相同 retrieved-token budget 下明显改善；Llama-8B 接近。以 summary/facts 替换原文通常因信息损失而降低总体 QA，但 facts 在 multi-session subset 上改善；最优 token budget 随 reader 能力改变，Llama-8B 超过约 3k retrieved tokens 后陡降，GPT-4o 可持续到 20k+。
- Key Table 3：round 的 `K=V` Recall@5/10 为 .582/.692，`V+fact` 为 .644/.784；三 reader 的 QA 随之改善。单独 fact/keyphrase 通常不及原值，说明收益来自保留原信息的 expansion，而不是压缩替代。
- Retriever Appendix Table 9：`V+fact` 对 BM25、Contriever、Stella 的主要设置一致改善；但具体 NDCG 与 granularity 有例外，且正文声称 “9.4% Recall@k/5.4% final accuracy” 是跨设定平均，不是所有 cell 的绝对增幅。
- Time-aware Table 4：GPT-4o time-range extraction 在 temporal subset 改善 recall，但 Llama-8B 可降低某些 recall/NDCG；附录显示它会在无明确时间范围的问题上误造日期并剪掉正确 evidence。
- Reading Figure 6：oracle retrieval 下 JSON+CoN 对 GPT-4o/Llama-70B 最好，对 Llama-8B 与 JSON direct 持平 .710；最优相对 suboptimal strategy 可差约 10 points，但这不是 retrieval 改进。
- Error Figure 14：best design 下仍有 13.2–24.6% correct-retrieval/wrong-generation，以及 14.8–18.8% wrong-retrieval/wrong-generation；memory failure 必须区分 retrieval 与 reading，最终 QA 不能反向唯一定位故障。

## 失败边界与限制

- [AUTHOR_FACT] session summary/fact 替换总体上会损失细节；facts 的优势只在 multi-session aggregation 等子集稳定出现。压缩 memory 不是单调增益。
- [AUTHOR_FACT] 更弱 time-range model 会 hallucinate temporal cues 并错误剪枝；time-aware filtering 必须允许“不限制时间”，且抽取器本身成为错误源。
- [AUTHOR_FACT] post-retrieval rank merging 显著低于把 fact 与原 key 合并的 key merging；平行多路径 index 会膨胀约 `m+1` 倍，并不自动改善 recall。
- [AUTHOR_FACT] 商业系统分析中 ChatGPT 会在后续压缩时修改/覆盖已记录信息，Coze 常在写入阶段漏掉间接表达；仅看最终错误不能区分 write corruption 与 recall miss。
- [AUTHOR_FACT] Ethics 明示 benchmark/method 没有 memory deletion operator，并有隐私泄漏、恶意写入 datastore 的风险；本文没有验证删除、更正来源、跨用户隔离或 poisoning defense。
- [READER_INTERPRETATION] Evidence sessions 的属性与问题由同类 LLM 辅助生成、无关 sessions 来自固定三源混合，可能有语体/来源线索；尽管人工编辑降低明显线索，论文未报告 evidence-vs-distractor source classifier 或 artifact audit。
- [READER_INTERPRETATION] Fact expansion 的生成由固定 Llama-8B 加十个人工修订 examples 完成；收益同时依赖 extraction model、prompt 和 extra indexing compute，不能简化为“多 key”普遍有效。
- [READER_INTERPRETATION] 论文报告 token-budget-aware value 比较，但未在主结果给出 indexing LLM cost、key expansion storage、query-expansion latency 与完整端到端等成本表；适合机制筛选，不足以声称 compute-optimal。

## 可抽取候选（尚非正式 Card）

- Evaluation Operator：`Index–Retrieve–Read Failure Decomposition`——分别用 annotated evidence recall 与 oracle reading 隔离写入/召回/阅读问题，避免只用最终 QA 猜故障位置。
- Operator：`Round-Preserving Fact-Augmented Keys`——value 保留 round 原文，用抽取 facts 仅扩展 key；避免以 facts 替代原信息。
- Operator：`Abstain-Capable Temporal Scope Filtering`——仅在可靠解析明确时间范围时过滤检索域，无范围则保持全域；需报告 extractor false-positive。
- Operator：`Structured Extract-Before-Reason Reading`——先逐 memory item 抽证据再聚合回答，并把 retrieval correctness 与 generation correctness分开。
- Failure：`Compression-Induced Memory Mutation or Detail Loss`——长期压缩可覆盖更新事实或丢失间接细节，表现为写入/维护层失败。
- Failure：`False Temporal Range Prunes Relevant Memory`——弱 query expander 虚构日期范围，主动排除正确 evidence。
- Failure：`Correct Recall Still Produces Wrong Reading`——即使 Recall@10 正确，13.2–24.6% 全样本仍可 generation 错误，说明 retrieval-only optimization 不够。

## 未解决问题

- `[OPEN_QUESTION]` 500 questions 在 attributes/source mixtures 上是否存在 trainable artifacts，论文未给对抗性检测。
- `[OPEN_QUESTION]` facts、summaries、events 的 extraction error rates 与跨 extraction model 稳定性未直接标注评估。
- `[OPEN_QUESTION]` key expansion、time extraction、CoN 的端到端 token/latency/storage 成本及联合消融未在同一表对齐。
- `[OPEN_QUESTION]` commercial system 的实现与产品版本为 2024 年 8 月短窗口，不可用于当前产品能力断言。
