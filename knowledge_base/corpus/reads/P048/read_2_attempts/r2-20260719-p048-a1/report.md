# P048 独立二读报告

## 来源与读取声明

- 冻结调用快照：`knowledge_base/corpus/reads/P048/read_2_attempts/r2-20260719-p048-a1/invocation.md`
- 论文：*NaviAgent: Graph-Driven Bilevel Planning for Scalable Tool Orchestration*
- PDF SHA-256：`d7578b55678c89f2ffb78741c5faab8adf7c70e7e4160d2cd5fafea522e192ab`
- [AUTHOR_FACT] 已逐页读取全部 35 个物理页。

## 1. changed computation 与 I/O

- [AUTHOR_FACT] NaviAgent 把高层决策限制为 Direct Response、Intent Clarification、ToolChain Retrieval、Tool Execution 四种动作；输入为最近 3 个 observation–action 对、当前 observation 和上一步剪枝子图的文本序列化。（物理页 2–3，§3.1；短定位：“most recent three”）
- [AUTHOR_FACT] 执行层 TWNM 是 API/parameter 异构图，schema 提供结构边，历史成功调用提供 API/API 与 parameter/parameter 行为边；BGE 语义特征、调用统计和度特征送入两层、8-head HGT 做 link prediction，预测边权供图搜索。（物理页 3–5；附录物理页 12–13）
- [AUTHOR_FACT] 失败时有 I/O-equivalent substitution、upstream rerouting、subgraph switching 三种路径重组；边权按长期历史与最近成功率更新，新工具增量加入，失败/低频工具剪枝并周期探测恢复。（物理页 5，§3.2.4–3.3）
- [READER_INTERPRETATION] 核心改变是“先检索图子结构再执行，并用运行反馈更新图”，不是单纯 planner prompt。其输入依赖完整 API schema、语义标准化和历史调用日志。

## 2. 数据、基线与主结果

- [AUTHOR_FACT] 模拟评测用 API-Bank 444 题、ToolBench 461 题；任务按 ≤1、2、≥3 API 分 easy/medium/hard。另以 RapidAPI 50 个 live APIs、7 域、303 个查询做真实端点评测。（物理页 6–8；附录物理页 23，表 6）
- [AUTHOR_FACT] 基线包括 ReAct、ToolLLM、α-UMI、ToolPlanner、ToolNet；TSR 由 GPT-4.1 对最终回答、实际调用路径与 reference call path 做二元评判，Steps 只在成功任务上计 LLM calls，TCR 统计是否产出最终结果。（物理页 6–7；附录物理页 28–30）
- [AUTHOR_FACT] ToolBench 上 DeepSeek-V3 的 NaviAgent overall TSR 55.2、Steps 4.60；最强完整基线 ToolNet 为 44.9、6.02。不同 backbone 上领先约 7.8–10.3 点。（物理页 7，表 1）
- [AUTHOR_FACT] 真实 API 上 NaviAgent TSR 为 37.4/54.4/64.6（Qwen14B/32B/DeepSeek-V3），对应最强 ToolNet 为 33.1/45.1/52.6；NaviAgent Steps 约 5.0–5.3、时间 26–36 秒。（物理页 8，表 2）

## 3. 消融、负向结果与预算

- [AUTHOR_FACT] DeepSeek-V3 ToolBench 消融：ReAct 34.5；ReAct+Graph+Alpha 45.7；Bilevel 42.4；Bilevel+Graph+Unpruned 50.3；+Alpha 53.4；+Heuristic 55.2。（物理页 8，表 3）
- [AUTHOR_FACT] Dynamic+H 并非所有 cell 都优于 Dynamic+A：例如部分 hard/medium split 和 TCR 有回退；启发式搜索相对 Alpha 也有更高 runtime。DeepSeek-V3 overall runtime 为 Base 55.8s、Dynamic+A 40.6s、Dynamic+H 47.3s。（物理页 9，表 4；物理页 30，表 7）
- [AUTHOR_FACT] 动态剪枝/恢复只在同一 50 题、两阶段、随机禁用 10% API 的合成设置测试；TSR 从 44.0 到 48.0、Steps 5.12 到 4.72。（物理页 31，表 8）
- [READER_INTERPRETATION] 该实验支持对随机可用性变化的适应，不足以证明对语义 API drift、schema 改动或相关故障的真实鲁棒性。

## 4. oracle、泄漏与可复现性问题

- [AUTHOR_FACT] 模拟 API 对历史同输入复用输出；新 API 可由模型生成 mock data；提示甚至要求操作完成时 status 总为 success，`type` 再标 mock/error。（物理页 27，API simulator prompt）
- [AUTHOR_FACT] 合成任务由随机 API dependency tree 反向生成，严格要求父输出与子输入名称/类型匹配；评估再使用 reference call path。（物理页 22–23，Data generation）
- [READER_INTERPRETATION] 这使主基准与方法所建模的参数依赖图结构高度同构，且 API 模拟器倾向成功；它验证“在这种生成/评判机制下的图导航”，不等价于开放世界 API 正确性。
- [AUTHOR_FACT] Qwen14B SFT 用 3,500+ 生成样本并声称与评测严格分离；训练需 8 张 Ascend 910B 64G、约 10 小时。（物理页 6；物理页 23）
- [OPEN_QUESTION] 历史调用日志的确切来源、是否与评测任务或生成图共享轨迹没有被完整说明；多次随机运行、方差、seed 和最大 attempts 也未充分报告。
- [OPEN_QUESTION] Alpha-Beta 算法正文称 `β′=min(β,1.15s)`，伪代码第 21 行却写 `β←max(β,1.15s)`；伪代码返回行还出现 `Gsub=(Vsub,E)=0`，需要实现级核验。（物理页 13–15，Eq./Algorithm 1–2）

## 5. Operator、Failure 与理论边界

- [AUTHOR_FACT] KL 投影定理只针对给定 context-dependent feasible action set 后，把 base policy 限制到可行集合并重归一化；作者明确说它不刻画 TWNM 如何生成/更新集合，也不等价于全局动态过程。（物理页 5–6；物理页 32–35）
- [READER_INTERPRETATION] Operator 候选：API/parameter 图上的候选子图检索、执行失败后的等价替换/上游回退/换子图，以及异步边权更新。
- [READER_INTERPRETATION] Failure 候选：稀疏或带偏历史日志学错边；随机/mock API 过度乐观；启发式搜索有额外运行时且并非所有 split 单调提高；理论可行集投影被误写成端到端保证。
- [READER_INTERPRETATION] 建议保留 changed-computation，但主结论需同时记录合成链、LLM judge、调用/推理预算差异、日志来源未明和真实 API 仅 50 个；不能宣称已证明开放世界持续自进化。

## 6. 可视核验

- [AUTHOR_FACT] 已核对物理页 9 表 4，Dynamic+A/Static+A/Dynamic+H 的非单调 cell 与解析文本一致；未见渲染冲突。
