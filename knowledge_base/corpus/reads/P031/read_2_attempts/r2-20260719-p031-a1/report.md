# P031 独立二读报告

- Attempt：`r2-20260719-p031-a1`
- PDF SHA-256：`b9d840d861da993e05ecc9e2295e9754ee9289ebc595270f6af18c55e57b8782`
- 阅读范围：物理页 1–12，逐页全文
- 二读结论：`ACCEPT_WITH_NARROWING`

## 1. 方法与被改变的计算

- [AUTHOR_FACT] 本文的主要贡献是一个比较十种长期记忆系统的 Memory Agent Benchmark（MAB）与 MemoryArena，并对构建、检索、回答阶段作延迟、能耗和 token 成本剖析，而不是提出新的记忆更新算法。（物理页 1–3，摘要/§1–§3，定位词 “ten representative systems”“phase-aware cost profiling”）
- [AUTHOR_FACT] 比较覆盖四类范式，并统一若干主导因素；同时保留各系统原生的 buffering、parallelism、consolidation 行为。（物理页 3–5，§3/实验设置，定位词 “preserve system-native”）
- [READER_INTERPRETATION] 因而本文改变的是“记忆系统如何被测量和比较”的评价计算，不是 Agent 在运行时如何记忆或决策；可抽取为成本感知评测算子，但不应抽取成新的 memory operator。

## 2. 输入、输出、干预时点

- [AUTHOR_FACT] 主体实验使用 LongMemEval 的五个长样本（每个约 36 万 token）和 300 个查询，覆盖构建与查询阶段；主成本实验以本地 Qwen3-32B 和共同 embedding 模型减少模型差异。（物理页 4–6，§4，定位词 “five samples”“300 queries”“Qwen3-32B”）
- [AUTHOR_FACT] 输出包括 MAB 准确率以及墙钟时间、能耗、token、每个正确答案成本等过程指标。（物理页 5–9，表 3、MAB 汇总图，定位词 “energy per correct answer”）
- [READER_INTERPRETATION] 干预发生在评测层：将同一数据与查询送入不同记忆实现，再按阶段归因成本；它没有对单个系统内部的检索、压缩或写入策略施加统一算法。

## 3. 基线、结果与公平性

- [AUTHOR_FACT] 表 3 中 BM25 的准确率为 47、墙钟时间 16.3 分钟、每个正确答案约 4,128 J；Letta 的准确率为 27.7、墙钟时间 14.36 小时、每个正确答案约 185,873 J，后者约高 45 倍。（物理页 6，表 3，定位词 “BM25”“Letta”“J/correct”）
- [AUTHOR_FACT] MAB 宏平均中 BM25 为 55.8，结构化/agentic 系统并未整体超过它；作者同时提醒该聚合偏重 recall-heavy 任务。（物理页 8–9，MAB 总表及讨论，定位词 “BM25 55.8”“recall-heavy”）
- [AUTHOR_FACT] 构建成本主要来自 prefill/embedding，decode 的中位能耗占比仅 4.6%；系统的检索延迟大体平坦，但默认均不主动遗忘，存储足迹单调增长。（物理页 6–10，成本分解与 scaling 讨论，定位词 “median 4.6%”“do not prune”）
- [READER_INTERPRETATION] BM25 是强而必要的朴素基线；但由于各系统保留原生异步、缓存和合并策略，表格是现实实现的系统比较，不是严格隔离单一机制的因果消融。
- [AUTHOR_FACT] 严格输出契约会形成模型能力下限，MIRIX 在 Qwen 1.7B 条件下完全失败。（物理页 7–8，模型敏感性分析，定位词 “MIRIX”“1.7B”）

## 4. 负向证据、限制与风险

- [AUTHOR_FACT] agentic 构建 token 成本可呈超线性增长，LLM-bound 管线具有很长且不稳定的尾部延迟，作者建议设置上限。（物理页 9–10，scaling/tail latency，定位词 “superlinear”“caps”）
- [AUTHOR_FACT] 异步五秒回放对构建较慢的系统产生 staleness；本文没有证明这种陈旧度在真实下游交互中造成多少质量损失。（物理页 9–10，replay/staleness 讨论，定位词 “five-second replay”）
- [AUTHOR_FACT] 研究局限为单节点，未覆盖多智能体和多模态设置。（物理页 11，Limitations，定位词 “single-node”“multi-agent”“multimodal”）
- [OPEN_QUESTION] 若把本文用于支持“某记忆机制改变决策质量”的 Claim，仍需机制级消融；现有结果主要支持成本、扩展性与系统失败画像。

## 5. 可抽取内容

- [READER_INTERPRETATION] Operator 候选：`阶段化成本剖析 + 每正确答案资源归一化`，用途是防止只凭 accuracy 选记忆系统。
- [READER_INTERPRETATION] Failure 候选：`复杂记忆系统在准确率未提升时产生数量级资源开销`；`无遗忘导致存储单调增长`；`严格输出协议使小模型整体失效`。
- [READER_INTERPRETATION] 窄 Claim：本文能支持“记忆系统之间存在显著的准确率—成本—扩展性差异，简单检索是必须保留的强基线”，不能支持“agentic memory 普遍优于 BM25”或某个新机制有效。
- [OPEN_QUESTION] 若 P031 被设为 memory 方向的核心锚点或强基线，建议第三读核对图表数值与系统配置；否则本次二读足以入库并收窄使用。

## 6. 解析与访问声明

- [AUTHOR_FACT] PyMuPDF 解析文本可读；未发现会改变上述判断的文本—可视版冲突。复杂图表仍应在正式引用具体单元格前目视复核。（物理页 1–12）
- [AUTHOR_FACT] 实际模型/版本在界面不可见，记为 `unknown`；本 attempt 为 `procedural_blinding`，不是技术文件隔离。
- [AUTHOR_FACT] 冻结后只读取该 invocation 中嵌入的统一 prompt 与指定 PDF；使用本地 PowerShell、`Get-FileHash` 和 Python/PyMuPDF 做哈希、页数及逐页文本读取；未联网。冻结前曾用 `rg` 定位指定文件路径，但未打开论文内容。写入仅为本文件。
