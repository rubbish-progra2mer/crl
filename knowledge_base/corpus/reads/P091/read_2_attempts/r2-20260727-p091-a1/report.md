# P091 独立二读报告（fresh reader, W06 扩充波次）

## 0. 报告头部：文件校验与元数据核对

1. 实测 SHA-256：`10349a31de86116b7e4cc5a8cb5e60766a55ab7dbab7894906841a6e3234171f`（与任务给定值一致）。
2. 物理页数：21 页（pymupdf page_count = 21）。
3. [AUTHOR_FACT] 论文题目 "Temporal Validity in Retrieval Memory: Eliminating Stale-Fact Errors for AI Agents over Evolving Knowledge"，arXiv 侧栏戳记 "arXiv:2606.26511v1 [cs.CL] 25 Jun 2026"（p.1 左侧竖排文字），单一作者 Neeraj Yadav，署名 "MemStrata.dev — Called It Inc. (Enterprise)"，联系邮箱 memstrata@gmail.com（p.1 作者块）。与 canonical metadata（arXiv 2606.26511v1, 2026-06-25, single-author preprint）一致。
4. [AUTHOR_FACT] p.1 标题下方标注 "Draft v2 (temporal-validity framing)"，并保留一段斜体内部备注："For double-blind submission, anonymize the author block and the product/repository identifiers."（p.1）。
5. [READER_INTERPRETATION] 上述未删除的匿名化指示、"Draft v2" 标记与 gmail 联系方式表明这是一份尚未整理完毕的个人预印本；引用其数字时应按"未同行评审、不可外部复核"的证据等级处理。
6. 视觉抽查页面：p.1、p.6、p.7、p.11、p.13、p.20（140 dpi 渲染后逐表比对，见第 8 题）。

## 1. 方法究竟改变哪一步计算？

1. [AUTHOR_FACT] 改变的是记忆系统的写入步骤：不再"一律追加"，而是当传入事实与库中活动断言共享归一化 (subject, relation) 键但 object 不同时，新断言取代旧断言——旧行的有效区间被关闭（valid_to 置位、superseded_by 链接），新行开启；"Same object → duplicate (reinforce). No prior key → novel (store). No cosine, no LLM judge."（p.4, §4.1 第 2 条）。
2. [AUTHOR_FACT] 同时在读取路径加入确定性过滤：先按 cosine top-k 在活动事实上检索，然后 "apply the deterministic staleness filter (drop superseded rows)"，再打包幸存事实的原句而非重构三元组；"No LLM runs on the read path"（p.5, §4.4）。
3. [AUTHOR_FACT] 事实以 bi-temporal ledger 保存："Facts are retired, not deleted."，记录 valid_from / valid_to / superseded_by（p.4, §4.2）。
4. [READER_INTERPRETATION] 检索打分（cosine top-k）与答案生成（同一 7B 模型、同一 prompt 框架）均未改动；方法唯一的计算改动是"写入时按键取代 + 读取时滤除已取代行"。
5. [READER_INTERPRETATION] 注意口径："no LLM call" 只适用于取代判定本身与读路径。写路径的 (S,R,O) 三元组抽取来源是 prompt 文件 extract_triple_v1.md（p.17, C.1，标题 "Deterministic triple extractor (the supersession key source)"），非三元组散文还会落入 "surprise gate that classifies via similarity plus an LLM judge"（p.4, §4.1 第 3 条）——即写路径整体上仍依赖 LLM（temperature 0 意义上的"确定性"），只是键比较与读路径不用 LLM。

## 2. 输入、输出、可用信息与干预时点

1. [AUTHOR_FACT] 输入：逐轮摄入的事实陈述（evolving 基准为 state-A 轮后接 state-B 轮，二者除单一变异值外逐字相同），随后是针对当前值的问题（p.5 §5 "Evolving scenarios ingest state-A then state-B; the question targets the current value"；p.15 B.1）。
2. [AUTHOR_FACT] 输出：按 token 预算打包的上下文块，交给答案模型 Qwen2.5-Coder-7B；正确性与捏造判定用两个互异的 Qwen2.5-Coder-3B judge，embedder 为 nomic-embed-text 768-d（p.4 §4 "composes a token-budgeted context block per query"; p.5 §5）。
3. [AUTHOR_FACT] 可用信息：归一化 (subject, relation) 键、活动断言表、摄入顺序；作者明言 "the only currency signal is ingestion order"（p.15, B.1），且 "The benchmarks use order (state-A then state-B) as the currency signal"（p.8, §7 第 2 条）。
4. [READER_INTERPRETATION] 干预时点有两个：写入时（取代判定，关闭旧行）与读取时（滤除已取代行、按原句打包）；不干预解码或答案模型本身。
5. [READER_INTERPRETATION] 信息不对称值得记录：MemStrata 在写入时利用了摄入顺序，而 RAG 基线的 chunk 在读取时不携带任何顺序/时间戳信息，模型无从复原先后。这是"结构性失败"论断的前提，也是第 3 题所述缺失基线的来源。

## 3. 最强基线与最接近组合基线

1. [AUTHOR_FACT] 共 8 个条件：no_memory、naive_rag、advanced_rag（+LLM reranker）、v6_no_verify、v6（gate + LLM relevance verify）、temporal_v6_lossy（消融）、temporal_v6（完整方法）、v6+infer（p.5, §5 "Conditions (8)"）。
2. [READER_INTERPRETATION] 最强纯 RAG 基线是 advanced_rag（naive + LLM 重排，~16–18 s 延迟）；最接近的组合基线是 v6 / v6+infer（相似度 gate + LLM 判定 + LLM 相关性校验），它们拥有 LLM 写入判定与 LLM 读取校验，但没有确定性键取代。
3. [AUTHOR_FACT] 组合基线表现：v6 在 evolving 上 0.35–0.65、且弃答允许时泄漏陈旧值 25–60%（p.7 §5.3 "they answer but leak stale 25–60%"；p.11 stale 表 v6_no_verify 0.250–0.600、v6 0.250–0.567）。
4. [READER_INTERPRETATION] 缺失的最自然廉价组合基线：给 RAG 的 chunk 附加摄入序号/时间戳并让答案模型自行择新（"timestamped-chunk RAG"），或 recency 加权检索。论文未测任何让基线获得顺序信号的变体，因此 "RAG cannot avoid by construction"（p.1 摘要）严格说只对"无时间元数据的 RAG"成立。
5. [AUTHOR_FACT] 未与任何外部记忆系统（Mem0、MemGPT/Letta 等，p.3 §2 仅作相关工作引用）做实测对比。

## 4. 结果是否可能来自模型、token、tool-call、prompt 或 oracle 差异？

1. [AUTHOR_FACT] 模型差异：无。所有条件共用同一答案模型与同一批 judge；"answer ≠ correctness-judge ≠ fabrication-judge ≠ verifier"，temperature 0、固定 seed（p.5 §5；p.17 C 开头）。
2. [AUTHOR_FACT] token 差异：显著存在。Mean pack tokens（p.11）显示 v6/v6+infer 在多数基准仅打包 26.9–40.7 tokens（verifier 过滤激进），naive_rag 110–320，temporal_v6 150–486。[READER_INTERPRETATION] 条件间上下文规模差异本身是各方法的产物，不算注入性混淆，但"verifier 不值得"（D.3）的结论与其过度过滤行为纠缠，不能只归因于"无时间信号"。
3. [READER_INTERPRETATION] prompt/基准泄漏：抽取 prompt C.1 的第一个示例输入 "The function get_user_by_id(uid) looks up a user record by primary key in the users table." 与 code_mutation 基准第一个场景的 state-A 句逐字相同（p.17 C.1 vs p.15 B.3）。抽取器的 few-shot 示例覆盖了被测分布，~97% 抽取成功率（p.16 B.8）在此模板族上可能被高估；在措辞更自由的 fair_contradiction 上确实塌到 ~44%。
4. [READER_INTERPRETATION] oracle/基准共构：evolving 基准被构造为"单一可变值模板"，恰好保证 (S,R,O) 抽取器可靠取键、且"较新即正确"恒成立——即基准设计保证了机制假设成立。作者自己承认这一点（p.8 §7 第 1 条），但主表 0.95–1.00 与 RAG 0.20–0.47 的对比幅度应连同这一共构一起引用。
5. [AUTHOR_FACT] oracle 噪声：作者承认 "The 3B correctness judge occasionally scores a gate-condition answer correct while it contains the stale value"（p.8, §7 第 3 条，原文 correct 带引号）。[OPEN_QUESTION] correctness/fabrication judge 的 prompt 未印出（"inline in eval/run_matrix.py"，p.19 C.4 后注），stale-fact-error 的具体判定实现（字符串匹配还是 judge）无法从 PDF 核实。
6. [AUTHOR_FACT] tool-call 差异：advanced_rag/v6/v6+infer 每查询多出 LLM rerank/verify 调用（延迟 ~16–18 s vs ~2.1 s，p.12 Tables 4–5）；这解释延迟差，不直接解释准确率差。
7. [READER_INTERPRETATION] 支持"机制真实"的内部证据：D.1b 全保留消融（仅关掉取代，其余不动）使 evolving 平均准确率 0.99→0.33、与 naive_rag(0.32) 无差异，且条件捏造率 0.04→0.25（p.20 D.1b）——在同模型、同 prompt、同 grader 下把效应定位到取代机制本身。就该论文自身的实验封闭性而言，这是较强的消融设计。

## 5. 作者明示限制、负向结果和未测试边界

1. [AUTHOR_FACT] §7 四条明示限制（p.8）：(a) evolving 基准是结构化单值模板，"Extraction quality, not the supersession mechanism, is the gating factor"——自由文本矛盾基准上抽取率 ~44%，该基准被隔离不计入主结果；(b) "Ingestion order proxies time"，真实时间戳与 as-of-T 检索是未来工作；(c) 单 judge 噪声（3B judge 偶将含陈旧值的答案判"正确"）；(d) 单一 7B 模型、消费级硬件、每基准仅数十条（"isolate mechanisms rather than rank systems on a leaderboard"）。
2. [AUTHOR_FACT] 负向结果：(a) temporal_v6_lossy 激进合并使静态召回塌到 domain 0.62 / locomo 0.13（p.5 §4.3, p.19–20 D.1）；(b) D.1b 去取代使 evolving 均值 0.99→0.33、捏造 0.04→0.25（约 6 倍，config_migration 峰值 0.56）（p.20）；(c) LLM verifier（v6）"has no temporal signal and is not worth its cost"，静态上 v6 ≤ v6_no_verify（domain 0.80 vs 0.86）且 ~8× 延迟（p.20 D.3）；(d) v6+infer 处处中性（p.21 D.4）；(e) 隔离基准 fair_contradiction 上 temporal_v6 0.62 反而低于 advanced_rag 0.74（p.16 B.8）——方法在抽取失效的 56% 场景上 "never engages"；(f) 去掉 [OUTDATED] 标记使 reranker-RAG 掉 14 分、gate-only 掉 18 分，temporal 仅 −4（p.15 B.2）。
3. [AUTHOR_FACT] 未测试边界：as-of-time 查询（能力已存储但 "we build on but do not evaluate here"，p.4 §4.2）；多值抽取器 extract_triples_v1.md "P1.3; flag-gated"（p.18 C.2）未进入主矩阵；original-text packing 无单因子消融（"A dedicated single-factor packing cell was not run separately"，p.20 D.2）；更大模型/云推理；真实纵向数据。
4. [READER_INTERPRETATION] 作者未列但真实存在的未测边界：乱序或错误更新（后到的断言未必正确——机制等价于 (S,R) 键上的 last-write-wins）；含时间戳元数据的 RAG 基线（见第 3 题）；多跳/组合查询下的取代正确性。

## 6. 可抽取 Operator 与真实可记录 Failure

Operator（均为 [AUTHOR_FACT] 报告的做法 + [READER_INTERPRETATION] 的可迁移性判断）：
1. OP-A 标记洁净不变量：evolving 记忆评测中，陈旧/当前版本须除变异值外逐字相同，禁用 old/new/deprecated 等词，并用单测强制（p.5 §4.5；p.15 B.1）。依据：去标记使基线掉 14–18 分（p.15 B.2）——评测构造级 operator，可直接复用。
2. OP-B 强制作答补充（forced-answer supplement）：关掉弃答以暴露被弃答掩盖的陈旧承诺（p.5–6 §5 Metrics；p.12–13 A.2）。naive_rag 弃答允许时 stale 0.05–0.30，强答后 0.15–0.40（p.7 Table 3）。
3. OP-C 确定性键取代 + bi-temporal 退休（retire 而非 delete，保留 valid_from/valid_to/superseded_by）（p.4 §4.1–4.2）。
4. OP-D "retain, then supersede"：仅在矛盾轴上压缩，非矛盾近重复照存；激进合并会损害静态召回（p.5 §4.3）。
5. OP-E 打包原句而非重构三元组："packing the triple alone degrades the answer model on rich facts"（p.5 §4.4）。（注意：无单因子消融支撑，见 D.2。）
6. OP-F 评审卫生：answer/judge/verifier 模型互异防自评（p.5 §5；p.17 C）；prompt 全量 SHA-256（p.17 表）。
7. OP-G 隔离"坏尺子"：把抽取器失效的基准（fair_contradiction）标为 flawed ruler 隔离并如实报告，而非并入主表（p.16 B.8）。

Failure（论文内真实记录的失败模式）：
1. F-1 相似度阈值不能分离矛盾与重复：AUROC 0.5926，contradict 均值 cosine 0.8119 > duplicate 0.7998，任何阈值最大 precision 0.667（p.6 §5.1, Table 1；p.13–14 A.3）。
2. F-2 相似度+LLM gate 做取代会主动泄漏陈旧值 25–60%，弃答允许下比 naive RAG 更差（p.7 §5.3；p.11 stale 表）。
3. F-3 写入时有损合并换取压缩 → 静态召回塌陷（0.62/0.13，p.19–20 D.1）。
4. F-4 全保留（无取代）→ 不仅准确率塌回 RAG 水平，还制造捏造源（0.04→0.25，p.20 D.1b："not merely less accurate but less safe"）。
5. F-5 LLM 相关性校验对时效无效且 8× 延迟（p.20 D.3）。
6. F-6 单槽抽取器在多值句/扰动串上失效（97%→44%），方法在抽不出键的场景直接不生效并输给 advanced_rag（p.16 B.8）。
7. F-7 版本号表面启发式：dependency_bump 上 RAG 强答 stale 仅 0.15，因 "higher version number is newer" 是 "a lucky surface heuristic"（p.7）——评测解读时须防这类表面线索抬高基线。

## 7. 判断-页码对照（物理页码 = PDF 页序号；本文无图，全部为表）

| 判断 | 物理页 | 章节/图表 | 逐字定位语 |
|---|---|---|---|
| 取代规则定义 | p.4 | §4.1 第 2 条 | "No cosine, no LLM judge." |
| 读路径无 LLM | p.5 | §4.4 | "No LLM runs on the read path" |
| AUROC 与逐类 cosine | p.6 | §5.1, Table 1 | "cosine AUROC ... is 0.5926" |
| 阈值精度上限 | p.6 | §5.1 | "maximum precision achievable at any duplicate threshold is 0.667" |
| 主准确率矩阵（5 列摘选） | p.6 | §5.2, Table 2 | "ties RAG on static and dominates on evolving" |
| stale-fact-error 双 regime | p.7 | §5.3, Table 3 | "0.10 / 0.40 ... 0.03 / 0.03" |
| gate 泄漏 25–60% | p.7 | §5.3 | "they answer but leak stale 25–60%" |
| 压缩率 | p.7 / p.12 | §5.4 / A.1 | "code 48%, config 47.5%, dependency 50%, API 47.5%" |
| 延迟 | p.7 / p.12 | §5.5 / Tables 4–5 | "all sit at ∼2.1 s" |
| 四条限制 | p.8 | §7 | "Extraction quality, not the supersession mechanism, is the gating factor" |
| 8×6 全矩阵 | p.10–11 | A.1 | "reproduced verbatim from the committed source reports" |
| forced 补充 | p.12–13 | A.2 | "REPORT_PAPER1_forced.md" |
| 校准扫值表 | p.13–15 | A.3 | "τdup sweep (DUPLICATE auto-accept)" |
| 标记洁净不变量 | p.15 | B.1–B.2 | "the only currency signal is ingestion order" |
| 隔离基准 | p.16 | B.8 | "97% clean supersession on code_mutation vs 44% here" |
| 抽取 prompt 及示例 | p.17 | C.1 | "The function get_user_by_id(uid) looks up ..." |
| 全保留消融 | p.20 | D.1b | "collapses mean evolving accuracy from 0.99 to 0.33" |
| packing 无单因子消融 | p.20 | D.2 | "not run separately and is marked future work" |

## 8. 解析文本与可视 PDF 是否冲突（就抽查页面回答）

1. [READER_INTERPRETATION] 抽查 p.1、p.6、p.7、p.11、p.13、p.20 共六页：pymupdf 抽取文本与渲染图像逐表核对（Table 1 四行 cosine 统计、Table 2 全部 24 个准确率格、Table 3 八对 allow/forced、A.1 条件捏造/尝试数/记忆量/打包 token/stale 五张表、A.2 三张表、A.3 分布表、D.1/D.1b 两张表），数值完全一致，无冲突。抽取文本将表格线性化为逐格一行，但未发现错位或丢值。
2. [READER_INTERPRETATION] 交叉一致性抽验通过：D.3 的 "locomo 0.13 vs 0.17" 对应 A.1 的 0.133/0.167；§5.4 压缩率与 A.1 表一致；Table 3 与 A.1/A.2 相应格一致。
3. 发现的内部异常（非文本-图像冲突）：
   - [OPEN_QUESTION] A.1 "Memory size (active facts)" 与 "Memory compression" 表中，no_memory 条件报出非零活动事实数（47/16/31/24/22/25）与非零压缩率，数值与 gate 条件完全相同，而其 pack tokens 为 0.0、准确率为 0.000（p.11–12）。疑为流水线统计沿用摄入侧数据的报告瑕疵，原文无解释。
   - [READER_INTERPRETATION] 摘要与 §5.2 称静态上 "ties RAG"，但 domain 0.82 vs 0.86 有 4 分差距；"tie" 是作者的宽松措辞。
   - [OPEN_QUESTION] 全文多处称 "We release the harness, prompts, datasets"（p.1 摘要、p.9 Reproducibility），但 PDF 内无任何代码/数据仓库 URL（引用列表外无链接），发布物无从核验。
   - [READER_INTERPRETATION] 参考文献含 SWE-bench（Jimenez et al., p.9）但正文未见引用点，仅 B.1 出现 swe_longitudinal 测试文件名——疑为残留引用。
   - [AUTHOR_FACT] MemStrata 的 stale error 在 code_mutation 上并非严格 0 而是 0.033（两 regime 同，p.7 Table 3），作者以 "∼0%" 概括。

## 附注（证据等级总评）

[READER_INTERPRETATION] 本文全部数字出自作者本地单机、单模型、数十条/基准的自建模板评测，主张的封闭性（消融 D.1/D.1b 夹逼、标记洁净不变量、prompt 哈希）在论文内部自洽且设计认真；但基准-抽取器共构（第 4 题第 3–4 条）、缺失顺序信号 RAG 基线（第 3 题第 4 条）、无外部可核验发布物（第 8 题）三点使 "RAG cannot avoid by construction" 的普适口径应降格为"无时间元数据的 naive/rerank RAG 在此模板族上不能避免"。
