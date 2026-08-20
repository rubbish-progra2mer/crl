# P009 主 Codex 首读

- PDF：`knowledge_base/staging/papers/P009_memgpt.pdf`
- PDF SHA-256：`9f674bcff69c86f11c813dcfad613d8841f5f8ed17979e3c4df06a91df7762e0`
- 读取时间：`2026-07-19T15:27:19+08:00`
- 读取范围：逐页检查 1–13 页；正文 1–8 页，参考文献 9–10 页，实验 instructions、LLM judge 与数据生成 prompts 11–13 页。

## Changed computation / 方法对象

- [AUTHOR_FACT] MemGPT 将固定上下文改造成由 LLM 参与管理的分层 memory：main context 内含只读 system instructions、可读写 working context 和 FIFO queue，外部含保存全部 messages 的 recall storage 与 archival storage。
- [AUTHOR_FACT] queue manager 在上下文接近约 70% 时注入 memory-pressure warning，在达到容量时驱逐一部分队列内容并递归总结；原消息仍进入 recall storage。LLM 通过 function calls 自主更新 working context、检索 recall/archive，并可用 `request_heartbeat=true` 连续执行 memory function。
- [READER_INTERPRETATION] 计算差异不只是“加一个向量库”，而是把何时保存、何时检索、何时分页和何时继续函数链交给受系统事件驱动的 Agent policy；数据库检索只是外部存储实现。

## 数据、比较对象与评估边界

- 对话实验基于 Multi-Session Chat 的五段历史，并用另一个 LLM 生成第六段的 narrow-answer DMR 问题。MemGPT 能访问完整对话但需分页检索；fixed-context baseline 只看到前五段对话的 lossy summary。
- DMR 的判定同时用 ROUGE-L recall 与 LLM judge。附录要求 judge “generous”：只要生成答案触及 gold topic 即可判 correct；没有报告人工一致性或 judge sensitivity。
- Conversation opener 用与 persona labels 及 human opener 的 embedding similarity，而不是人类对参与感的直接偏好评估；MemGPT 的较长输出会覆盖更多 persona facts，可能天然抬高 similarity。
- Document QA 中两方使用同一初始 embedding retriever；baseline 一次接收 top-K documents，MemGPT 可反复调用 archival search 并分页。超过 baseline 原 context 时，论文通过截短每个 document segment 塞入更多 documents，这同时损失单文档内容。
- Document QA 仅抽样 50 个 NaturalQuestions-Open 问题，使用 2018 Wikipedia dump；正确性由 LLM judge 判定，且 prompt 明示答案总在 archival memory、找不到时继续检索。baseline 则被要求无证据输出 `INSUFFICIENT INFORMATION`。
- Nested KV 固定 140 对、约 8k tokens，0–4 层嵌套，每层/位置共 30 种 ordering；MemGPT prompt 直接要求持续 lookup 直到确认 value 不再是 key，baseline 也收到 nested-lookup 任务说明。

## 主要结果与定位

- DMR Table 2：GPT-3.5/GPT-4/GPT-4 Turbo 的 baseline accuracy 为 38.7/32.1/35.3%，加 MemGPT 后为 66.9/92.5/93.4%；ROUGE-L recall 同时由 0.394/0.296/0.359 升至 0.629/0.814/0.827。该结果支持“完整历史的受控检索优于其 summary baseline”，不能单独归因于层级 memory 的任一组件。
- Conversation opener Table 3 中 Human 的 SIM-1/3/H 为 0.800/0.800/1.000；三个 MemGPT 变体对 persona similarity 更高，但对 human opener similarity 仅 0.767–0.817。论文所谓偶尔超过 human 指代理相似度维度，不是总体人类质量超过人类。
- Document QA Figure 5 显示 fixed-context 随 K/压缩增加后下降或受限，MemGPT 在更多 documents 时保持约稳定；但 MemGPT 可以多次检索，baseline 是单次 top-K context，计算/检索调用预算没有以等成本方式对齐。
- Nested KV Figure 7：base GPT-3.5 在一层后跌至 0，GPT-4/4 Turbo 到三层为 0；MemGPT+GPT-4 在所测层数稳定完成，GPT-3.5/4 Turbo 变体在两层后也下降。它验证了 function-chained lookup 能执行合成多跳，不证明开放域长期记忆的一般可靠性。

## 失败边界与限制

- [AUTHOR_FACT] Document QA 的 gold document 常在前十几名之外；MemGPT 理论上可分页找到，但实际会在耗尽数据库前停止检索。失败来自 Agent 的 stopping policy，而非仅来自 retriever recall。
- [AUTHOR_FACT] GPT-3.5 上 document QA 明显退化，作者归因于 function-calling 能力；Nested KV 中 MemGPT+GPT-4 Turbo 也弱于 MemGPT+GPT-4。架构收益依赖 backbone 能否稳定执行控制函数。
- [AUTHOR_FACT] 附录中的 MemGPT prompts 为 brevity 编辑版，精确 implementation prompts 不在 PDF；仅依赖论文无法复现完整控制 policy。
- [READER_INTERPRETATION] DMR 对照把“完整可检索历史”与“有损总结历史”绑定，缺少等检索预算的普通 RAG、仅 recall storage、仅 recursive summary、固定 retrieval policy 等消融，无法分离 memory hierarchy、主动检索与信息保留量的贡献。
- [READER_INTERPRETATION] Document QA 的多次 archival search 与 baseline 单次 top-K/截断输入不等成本；未报告每题 tool calls、retrieved tokens、latency/cost，不能据图得出同预算优越。
- [READER_INTERPRETATION] 所有 document evidence 已预先 embedding 并装入 archive，且 agent 被告知答案必然存在；这排除了开放世界中的无答案判断、错误写入、记忆更新冲突和来源可信度问题。
- [READER_INTERPRETATION] 系统保存全部 messages 到 recall storage，不等于能可靠利用全部历史；搜索 query、分页、停止、working-context 更新任一环节失败都会形成 retrieval/control bottleneck。

## 可抽取候选（尚非正式 Card）

- Operator：`Event-Triggered Hierarchical Memory Control`——以 warning/flush/system events 触发 LLM 对 working context、recall 与 archive 的显式读写，改变决策上下文的构造过程。
- Operator：`Self-Directed Paginated Recall with Function Chaining`——Agent 自行生成检索、翻页并用 heartbeat 连续执行多步 lookup；需记录调用与 token 预算，避免把额外检索量当机制收益。
- Failure：`Agent-Controlled Retrieval Stops Before Evidence Exhaustion`——可检索证据存在但 policy 提前停止，导致理论无限外存不能转化为实际 recall。
- Failure：`Memory Architecture Benefit Confounded by Information and Retrieval Budget`——完整历史、多次 search 对比有损 summary/单次 top-K，收益无法归因于层级 memory 本身。

## 未解决问题

- `[OPEN_QUESTION]` DMR 的 summary baseline 如何生成、压缩率及其 token budget 未在 PDF 中充分披露。
- `[OPEN_QUESTION]` Document QA 与 Nested KV 每题平均/最大函数调用数、输入输出 tokens、latency 和失败重试未报告。
- `[OPEN_QUESTION]` working context 的更新质量、错误写入后的恢复、recall 与 archival duplication 的独立消融未提供。
- `[OPEN_QUESTION]` 论文网站上的 exact prompts/implementation 与该 v2 PDF 是否一致，需要代码或归档材料才能核对；Pilot 当前只以冻结 PDF 为证据源。
