# P036 独立二读报告

- Attempt：`r2-20260719-p036-a1`
- PDF SHA-256：`f6fbe657daa349b1495bef6fecd7b1a3c845da3bf296d2589eedb45e051613bd`
- 阅读范围：物理页 1–29，逐页全文
- 二读结论：`ACCEPT_WITH_NARROWING`

## 1. 方法与计算干预

- [AUTHOR_FACT] τ-Knowledge/τ-Banking 把约 698 篇、19.5 万 token 的非结构化内部文档、51 个可发现工具、14 个常驻工具和 97 个对话任务放在同一可验证状态环境中。（物理页 1–5，表 1/§3–§4，定位词 “698”“51”“97”）
- [AUTHOR_FACT] 工具只有在文档中被检索发现后才能 unlock/call，任务成功由最终数据库状态判定；平均每任务需 18.6 篇文档和 9.52 次工具调用。（物理页 3–4，表 1，定位词 “Discoverable Tools”）
- [READER_INTERPRETATION] 本文改变的是 benchmark 的信息结构：把检索质量、政策推理、能力发现和状态变更耦合；它不是新的检索或规划方法。

## 2. 基线、结果与信息边界

- [AUTHOR_FACT] 比较 text-embedding-3-large、Qwen3-embedding-8B、BM25、自由 terminal search 与直接给 gold 文档；所有 dense/sparse 检索每次返回 top-10，并允许重复调用。（物理页 5–7，§5/表 2，定位词 “top k=10”）
- [AUTHOR_FACT] 非 gold 最佳 pass^1 为 GPT-5.2 high+Terminal 的 25.52%；gold 条件最佳为 Claude-4.5-Opus high 的 39.69%，说明检索瓶颈被移除后仍有大量政策推理失败。（物理页 2、6–7，表 2）
- [AUTHOR_FACT] no-knowledge 平均 pass^1 约 2%；全知识库 long-context 最好约 12%，明显低于定向检索和 gold。（物理页 8、25，额外消融/表 6）
- [AUTHOR_FACT] Terminal 跨模型平均显著优于结构化检索，但优势集中在较新的高推理模型；旧 GPT 与 GPT-5.2 无 reasoning 并未受益。（物理页 7、28，§6/表 12）
- [AUTHOR_FACT] Terminal 平均搜索更多、耗时更长；GPT-5.2 high 的 terminal 平均任务时长约 1,567.8 秒，Claude Opus terminal 约 177.1 秒。（物理页 7、28–29，表 11/13）
- [READER_INTERPRETATION] 最强基线是 gold-documents，它隔离知识使用上限；long-context 和 no-knowledge 分别检验噪声与知识必要性。不能把 Terminal 的增益只归为“grep 更强”，因为查询策略与模型能力共同变化。

## 3. 负向结果与失败机制

- [AUTHOR_FACT] 定性失败中约 23% 与搜索低效/未经澄清的假设有关，约 14.5% 与产品跨文档依赖有关，约 5% 与隐式操作顺序有关，约 4% 与过度相信用户陈述有关。（物理页 8–9，图 4/§7.2）
- [AUTHOR_FACT] document recall 对同一 retriever 随模型显著变化，例如 text-embedding-3-large 配 Opus 约 57%，配无 reasoning GPT-5.2 约 28%。（物理页 8，检索分析，定位词 “57%”“28%”）
- [READER_INTERPRETATION] 检索不是静态前置模块：Agent 的查询形成与迭代策略决定相同 retriever 的有效召回；但 gold 结果仍低说明“找到文档”不足以解决跨文档和状态依赖。
- [AUTHOR_FACT] reranker、附加 grep、k=5/10/20 多数对 pass^1 无显著改善；terminal 允许写笔记也无显著提升，GPT-5.2 从未写，其他模型偶尔写但未再引用。（物理页 23–25，表 3–5，定位词 “no significant”“write commands”）

## 4. Oracle、构造与限制

- [AUTHOR_FACT] gold 文档由任务创建时整理，并经两名未参与创建的 reviewer 独立审计；每任务至少人工模拟一条可行轨迹，实验后又复审捷径。（物理页 5，Stage 5 Review）
- [READER_INTERPRETATION] gold 是分析 oracle，只能用来分解瓶颈，不能作为可部署方法的输入。
- [AUTHOR_FACT] 用户模拟器为 GPT-5.2 low；194 条双标轨迹中有 4 条 task-critical 用户错误。（物理页 6、9，§5/§7.1）
- [AUTHOR_FACT] 作者限制包括用户模拟过于简化、API 延迟不可泛化、现实常见的有限搜索预算未覆盖，以及 terminal 写工具/笔记作用尚不清楚。（物理页 9–10，Limitations）
- [OPEN_QUESTION] 数据由结构化数据库经 LLM 转成非结构化文档并人工精修，任务又围绕该数据库构造；这种可验证性很强，但与真实企业文档的矛盾、缺失和陈旧程度差异尚未测试。

## 5. 可抽取内容

- [READER_INTERPRETATION] Operator 候选：`文档中发现能力后再解锁工具`（评测/安全型机制）；`以 gold/no-knowledge/full-context 三角消融分解检索与知识使用`。
- [READER_INTERPRETATION] Failure 候选：`检索成功后仍无法正确应用政策`；`相同 retriever 因查询策略产生大幅召回差异`；`自由搜索用更多调用和延迟换有限收益`；`写笔记能力存在但模型不实际复用`。
- [READER_INTERPRETATION] 窄 Claim：τ-Knowledge 证明检索、跨文档政策推理与状态执行应联合评估，并揭示 gold 文档下仍显著失败；不能证明 terminal search 是普遍最优方法。
- [OPEN_QUESTION] 若作为 knowledge-grounded agent 的核心 benchmark，建议在正式实验设计阶段核对其当前公开版本；本次语义入库无需第三读。

## 6. 解析与访问声明

- [AUTHOR_FACT] 解析覆盖物理页 1–29，文本和表格可读，未发现影响判断的文本—可视版冲突。
- [AUTHOR_FACT] 实际模型/版本 `unknown`；程序性盲化。冻结后只读指定 PDF 与 invocation 内统一 prompt；使用本地 PowerShell、`Get-FileHash`、Python/PyMuPDF；未联网。冻结前仅用 `rg` 定位指定路径，未读论文。只写本报告。
