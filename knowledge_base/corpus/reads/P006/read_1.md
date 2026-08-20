# P006 主 Codex 首读

- PDF：`knowledge_base/staging/papers/P006_llmcompiler.pdf`
- PDF SHA-256：`36dde899ed8abe0df728215e054aab21d1699add719afeb0ddadbb4e4eb23263`
- 读取时间：`2026-07-19T16:47:00+08:00`
- 读取范围：逐页检查 1–22 页；正文 1–9 页，参考文献 10–12 页，ReAct/LLMCompiler 失败分析、实验细节、速度模型、补充结果与 prompts 13–22 页。

## Changed computation

- [AUTHOR_FACT] Function Calling Planner 一次生成带 `$id` placeholder 的任务依赖 DAG；无 LLM 的 Task Fetching Unit 在依赖满足时替换真实输出并贪心派发，Executor 异步并行执行彼此独立的工具调用，各任务保留独立 memory。
- [AUTHOR_FACT] Planner 可流式输出任务，使已经生成且依赖满足的节点无需等待完整计划；若后续依赖取决于 observation，则 Executor 把中间结果交回 Planner 重新编译一轮 DAG。
- [READER_INTERPRETATION] changed computation 是把“每次 observation 后再由 LM 决定下一调用”的串行控制流，改成“LM 预先声明数据依赖、机械调度器并行执行”，并只在未知分支处重新调用 LM；核心收益应在可预见且无副作用的独立工具任务上评估。

## 基线、预算与公平性

- HotpotQA/Movie Recommendation/ParallelQA 分别是 2-way、8-way 与自建的多层 search→math 依赖结构；论文刻意选择能从 Wikipedia 首段回答的 ParallelQA 113 题，以排除 search miss，适合测调度但不是开放工具任务代表样本。
- GPT 主实验锁定 gpt-3.5-turbo-1106（前两项）、gpt-4-turbo-1106（ParallelQA）、gpt-4-0613（Game of 24）；各方法同 benchmark 使用相同 examples，温度 0 并平均 3 runs。ReAct† 额外 prompt 抑制重复/早停，作为较公平 baseline。
- Table 1/2 同时报告准确率、端到端延迟、input/output tokens 与按当时价格估算的成本，证据比只报速度强；但原始 ReAct 因循环/早停而不报 latency，speedup 分母采用改 prompt 后的 ReAct†。
- Game of 24 保留原 ToT thought proposer/state evaluator，只把同一层 proposal/evaluation 并行并逐轮 replan；这主要验证执行优化，不是新的推理质量方法。
- WebShop 的 LATS/LASER 成功率和 latency 来自各自论文，ReAct 才由作者复现；模型版本、硬件/网络、样本数不一致（LATS `N=50`，其他多为 500），101.7×/2.69× 跨论文速度不应当作严格同平台结论。

## 主要结果与定位

- Table 1：GPT HotpotQA LLMCompiler 62.00%/3.95s，ReAct† 62.47%/7.12s；Movie Rec 77.13%/5.47s vs 72.47%/20.47s；ParallelQA 89.38%/16.69s vs ReAct 89.09%/35.90s。主要稳健结论是近似准确率下更低延迟，而非所有任务都提高准确率。
- LLaMA-2-70B 上 HotpotQA 57.83 vs ReAct† 54.40，Movie Rec 77.80 vs 70.60，ParallelQA 68.14 vs 59.59；模型由 2×A100-80GB vLLM 承载。
- Table 2：相对 ReAct，估算成本降低 HotpotQA 3.37×、Movie Rec 6.73×、ParallelQA 4.65×，主要来自不把每轮 observation 重复塞回新的 LM prompt。
- Game of 24：GPT success 75.33 vs ToT 74.00，latency 83.6s vs 241.2s；LLaMA 32 vs 30，456.02s vs 952.06s。差异主要支持并行等价实现，没有证明新 reasoning Operator 提升正确率。
- WebShop：GPT-3.5 full 500 上 LLMCompiler success/score 48.2/74.2，ReAct 19.8/54.2；GPT-4 为 55.6/77.1，ReAct 35.2/58.8、LASER 50.0/75.6。LLMCompiler 固定探索 search 返回的约 10 个 item，额外信息覆盖同时改变 tool-call 数和决策质量。
- Appendix A：Movie Rec 中约 85% ReAct 提前于 8 次 search 停止，LLMCompiler 约 99% 完整搜索；HotpotQA LLaMA ReAct 约 10% 样例调用 >4 次并发散，而 DAG 通常固定 2 次。

## 失败边界与限制

- [AUTHOR_FACT] Appendix B：ParallelQA 的 36 个失败中，Planner/Executor/final output 各占 8%/64%/28%；Planner 会把错误 `$id` 接到后续任务，Executor 常选错属性或单位换算，最终回答仍可能错误解释已收集 observation。
- [AUTHOR_FACT] Appendix A 承认少于 3% 的 HotpotQA case 中，ReAct 第三次搜索可用替代实体名恢复，而固定两次调用的 LLMCompiler 反而更差；预编译减少循环，也减少基于失败动态改 query 的适应性。
- [AUTHOR_FACT] streaming 单独只在长工具 ParallelQA 达 1.30×，HotpotQA/Movie Rec 仅 1.01×/1.03×；Planner+final answering 在 Movie Rec 平均 1.88+1.62s，超过总 latency 一半，且并行有 straggler join 开销。
- [AUTHOR_FACT] 第 5 页明确指出复杂 branching 不能静态编译，需要 replanning；Game of 24 实际每层只规划一轮。标题“compiler”不意味着一次计划可覆盖任意 Agent 工作流。
- [READER_INTERPRETATION] DAG 正确性依赖 Planner 理解工具读写依赖；论文只测无副作用的 search/math/explore，未验证并发写操作、速率限制、共享 session 或不可交换 API。机械并行不能默认安全迁移。
- [READER_INTERPRETATION] WebShop 性能提升与“遍历全部十项”的更大 observation/tool budget 绑定；公平的准确率归因需要等 tool calls/coverage 的串行 baseline，而论文主要把它视为延迟可承受的并行探索。
- [READER_INTERPRETATION] ParallelQA 为作者自建且专门排除 retrieval failure，强力展示依赖调度上限，但弱化了真实执行恢复、查询改写与不确定依赖问题。

## 可抽取候选（尚非正式 Card）

- Operator：`LLM-Declared Dependency DAG with Mechanical Parallel Dispatch`——模型输出任务及数据依赖，非模型调度器只在依赖满足后替换 placeholder 并发执行。
- Operator：`Observation-Triggered Partial Recompilation`——静态 DAG 到达未知分支时，将中间结果交回 Planner，仅规划下一段依赖图。
- Operator：`Stream-then-Execute Planning`——Planner 尚未完成整图时，已解析且就绪的节点提前执行，以工具 latency 遮蔽生成 latency。
- Failure：`Static Parallel Plan Loses Adaptive Retry`——固定调用数阻止无效查询后的替代实体/参数重试，少量案例不如串行 ReAct。
- Failure：`Planner Dependency Misbinding`——任务 placeholder 或输入输出映射错误会把整个下游 DAG 机械地执行错。
- Failure：`Exploration-Budget Attribution Confound`——并行带来的可承受广搜与控制流本身同时变化，准确率提升不等于调度语义单独提升。

## 未解决问题

- `[OPEN_QUESTION]` WebShop 跨论文 latency 是否在相同网络、硬件与 API 条件重测，原文明确只复现 ReAct，不能确认。
- `[OPEN_QUESTION]` 并行工具调用的副作用、rate limit、失败取消与部分结果一致性未实验。
- `[OPEN_QUESTION]` Planner DAG 的语法/依赖正确率仅在 ParallelQA 失败样本中定性统计，缺少跨工具图结构准确率。
- `[OPEN_QUESTION]` 等总 tool-call/信息覆盖的串行 WebShop baseline 未给出，无法分离“更多探索”和“并行调度”。
