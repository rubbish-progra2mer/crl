# P023 独立二读报告

## 1. 读取边界与方法

- 本报告对应 `r2-20260719-p023-a1/invocation.md`；只读取 invocation、统一问题及指定的 24 页 PDF，未读取首读、Cards、其他报告或 blind query，未联网。
- [AUTHOR_FACT] 正文与全部附录逐页检查，并对全文检索了 split、train/test、seed、trial 等实验可复现关键词。
- [OPEN_QUESTION] PDF 文本层未见表格字段断裂；未逐页位图渲染，不能完全排除图形解析差异。

## 2. 方法改变的计算

- [AUTHOR_FACT] MasRouter 以 query 为条件，级联决定 collaboration mode、agent 数量、顺序角色及各角色使用的异构 LLM，再执行所选 multi-agent workflow（方法节，物理页 3–6）。
- [AUTHOR_FACT] router 用策略梯度优化准确性/成本 utility，训练奖励依赖 benchmark 的 oracle answer（算法与训练，物理页 5–7）。
- [AUTHOR_FACT] 候选模式含 CoT、Reflexion、Self-Consistency、Debate、MacNet；模型池含 GPT-4o-mini、Claude-3.5-Haiku、Gemini-1.5-Flash、Llama-3.1-70B（设置，物理页 7–8）。
- [READER_INTERPRETATION] changed computation 是“按样本路由整个协作结构”，不是单一 prompt router；其核心价值取决于训练泛化，而非在已知答案上学会每题配置。

## 3. 输入、输出与干预时点

- [AUTHOR_FACT] 输入为当前 query 以及模型/模式 profiles；输出依次为协作方式、参与规模、角色序列和 LLM 分配（方法，物理页 4–6）。
- [AUTHOR_FACT] 干预发生在任务执行前；执行后以 oracle answer 计算正确性奖励并结合成本训练 router（算法，物理页 6–7）。
- [READER_INTERPRETATION] 这是 meta-control Operator；若训练/测试严格隔离，它可学习问题到资源配置的条件映射，若不隔离则可能接近 benchmark-specific policy search。

## 4. 基线、结果和消融

- [AUTHOR_FACT] Table 1 报告 MasRouter 平均 85.93，RouterDC 82.42，AFlow 84.20；不同数据集胜负并非完全一致（物理页 8–9）。
- [AUTHOR_FACT] 成本表显示 MasRouter 通常比 single agent / 简单 router 昂贵，但比部分固定大型 MAS 便宜（物理页 9–10）。
- [AUTHOR_FACT] 随机化路由组件会降低效果，其中 LLM 分配 router 的消融影响最大（ablation，物理页 10–11）。
- [AUTHOR_FACT] 对新加入模型 DeepSeek 的实验依赖其 profile 与性能/成本信息（扩展实验，物理页 11–12）。

## 5. 关键有效性缺口

- [OPEN_QUESTION] 全文及附录没有找到明确的 benchmark train/validation/test 划分、数据隔离协议或按 split 报告；算法却对 `Q∈D` 使用 oracle answer 训练。原文因此不足以确认 Table 1 的查询是否独立于 router 训练查询。
- [OPEN_QUESTION] 未找到随机种子、多次独立训练方差或 trial 数量；不能判断路由策略的稳定性。
- [READER_INTERPRETATION] 这是阻断性证据缺口：若 evaluation queries 曾参与 policy-gradient reward，主结果不能被解释为对新查询的研究泛化。
- [READER_INTERPRETATION] 模型 profile 中若含同 benchmark 性能，会给 router 额外先验；原文不足以量化这部分信息优势。

## 6. 负向结果与边界

- [AUTHOR_FACT] MasRouter 并非最低成本方法，且完整路由含多次 agent 调用；某些任务上固定方法仍有竞争力（结果/成本表）。
- [READER_INTERPRETATION] 可记录 Failure：`Oracle-trained per-query routing without explicit split can collapse evaluation validity`；`Dynamic MAS gains may be resource-allocation gains rather than new reasoning computation`。
- [OPEN_QUESTION] 未充分测试分布外任务、全新协作模式，以及 profiles 错误或模型 API 行为漂移时的鲁棒性。

## 7. 可抽取资产与 Claim 边界

- [READER_INTERPRETATION] 暂定 Operator 候选：`Query-conditioned joint routing of collaboration structure and heterogeneous models`。
- [READER_INTERPRETATION] 在 split 问题澄清前，只能记录方法结构与实验待核状态，不能把 85.93 的优势写成已验证的泛化 Claim。
- [READER_INTERPRETATION] 即便 split 合法，结果也最多支持论文的模型池、模式池和 benchmark；不支持任意 agent 系统上动态路由普遍提高性价比。

## 8. 独立二读建议

`NEED_THIRD_READ`。需要第三读或外部原始实现核验数据划分、训练样本与评估样本关系、随机种子/重复实验；在此之前不应把主表当成可靠 Operator 效果证据。本建议仅供主 Codex reconciliation。
