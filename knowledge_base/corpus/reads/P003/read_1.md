# P003 主 Codex 首读

- PDF：`knowledge_base/staging/papers/P003_lats.pdf`
- PDF SHA-256：`a6b84613eeeaa3beb979ac3e34cbb3575bceb7ccf6050a2c2fc677d5e3a3ab19`
- 读取时间：`2026-07-19T16:13:00+08:00`
- 读取范围：逐页检查 1–23 页；正文 1–10 页，参考文献 10–13 页，算法、限制、补充消融与环境细节 14–17 页，完整 prompts/trajectories 18–23 页。

## Changed computation

- [AUTHOR_FACT] 第 4–6 页把 ReAct 轨迹节点化为含输入、动作与 observation 的树状态；每轮执行 selection、expansion、evaluation、simulation、backpropagation、reflection，直到成功或耗尽 `k` 条轨迹预算。
- [AUTHOR_FACT] 每次 expansion 从 LM 采样 `n` 个动作并真实查询环境；value 是 LM 状态评分与同一状态动作 self-consistency 的加权和，外部 terminal reward 再沿路径反向传播，UCT 平衡利用与探索。
- [AUTHOR_FACT] 失败轨迹与基于轨迹/最终 reward 的语言 reflection 被存入上下文，后续 agent 与 value function 都能看到；算法显式假设环境可回退到历史状态。
- [READER_INTERPRETATION] 核心改变是让已观察到的环境结果共同参与分支价值更新和再访问，而不是只在一条 ReAct 轨迹末尾重试；search、external observation、semantic reflection 三种信号通过共享树状态耦合。

## Baseline、预算与公平性

- HotpotQA（第 6–7、15 页）只随机抽 100 题，3 个 few-shot examples，所有采样方法最多 `k=50` trajectories；LATS 通常每次扩 `n=5`，因此“相同轨迹数”并不等于相同 LM calls/tokens。该环境会在提交答案后直接返回正确性，作者明确称为 oracle setup。
- Programming（第 7、16 页）用 LM 为每题生成 4/6 个 synthetic asserts，并用其通过率作为搜索 reward；HumanEval 最后在隐藏真实测试上评估。`k=8,n=5`，因此 Pass@1 是搜索选出的一个解，不是单次生成，但 synthetic tests 的质量/覆盖度构成额外变量。
- WebShop（第 8、16–17 页）只测 50 instructions；LATS、ReAct best-of-k、Reflexion 都设 `k=30`，LATS 另有每次 `n=5` expansion。与 IL/RL/fine-tuning 的训练资源不同，表 6 不构成严格等成本比较。
- 表 9–10 的 token/node 成本只统计成功时的平均展开节点；作者推断失败也会更省，但未给所有样本的完整 token、延迟、环境调用成本。ReAct/CoT-SC token consumption 在表中为 `-`，不能据此证明对简单 prompting 总体更高效。

## 主要结果与定位

- HotpotQA：CoT 版 LATS EM 0.62；ReAct 版 0.63，`n=3` 0.58、`n=10` 0.65；先 CoT、失败后切 ReAct 的混合版 0.71。主对照 ReAct 0.32、best-of-k 0.38、Reflexion 0.51、ToT(ReAct) 0.39、RAP(ReAct) 0.54。
- Programming：GPT-3.5 HumanEval Pass@1 LATS 83.8，Reflexion 68.1，RAP 63.1；GPT-4 LATS 92.7、Reflexion 91.0、Base LM 80.1。MBPP 为 LATS 81.1、RAP 71.4、Reflexion 70.0。
- WebShop：LATS score/SR 75.9/38.0；Reflexion 64.2/35.0；ReAct best-of-30 59.1/32.0。仍低于 expert 82.1/59.6，且 fine-tuning SR 45.0 高于 LATS 38.0。
- Game of 24（第 8、17 页）仅 50 题，GPT-3.5：LATS 0.44、RAP 0.40、ToT 0.20；去掉 self-consistency（`lambda=1`）降至 0.40。
- HotpotQA 消融（表 8/11）：无 LM heuristic 0.37、DFS 0.42、无 reflection 0.58、完整 LATS 0.63；降低 exploration weight `w=0.5` 为 0.55，`w=2.0` 不增益。支持多个部件有贡献，但并非正交逐项、等预算的完整因果分解。

## 失败边界与限制

- [AUTHOR_FACT] 第 8 页：WebShop 的 reflections 经常泛化、缺乏可用反馈，使 agent 陷入局部最优；同等 `k=30` 下 Reflexion 与 ReAct best-of-k 提升接近。
- [AUTHOR_FACT] 第 9、14 页：相对 ReAct/Reflexion 计算成本更高；MCTS 要求环境可回退，而该性质并非普遍存在。论文 benchmark 也被作者称为相对简单、比真实交互环境窄。
- [AUTHOR_FACT] 第 14 页称所测工具/API 的环境查询成本“trivial”，但只基于当前 benchmark；不能外推到付费、不可逆或有副作用的真实 API。
- [READER_INTERPRETATION] HotpotQA 正确性 oracle 与 programming synthetic test reward 为搜索提供强反馈；若真实任务没有可验证 reward，value 主要退回同一 LM 的自评与 self-consistency，机制可信度会明显变化。
- [READER_INTERPRETATION] 生成、评价、reflection 常由同一 `p_theta` 承担，共享盲点可能让树系统性偏向错误分支；论文未做独立 critic 或反馈噪声鲁棒性实验。
- [READER_INTERPRETATION] 把完整交互历史复制为可回退节点只适用于文本状态可充分重建、动作副作用可撤销的环境；真实网页/API 的隐藏状态、并发与不可逆动作会破坏假设。

## 可抽取候选（尚非正式 Card）

- Operator：`Observation-Grounded MCTS over Agent Trajectories`——在可回退文本环境中扩展多条 reason/action 分支，用外部 observation、LM heuristic、terminal reward 和访问次数共同更新再搜索。
- Operator：`Failure Reflection as Search Context`——把失败轨迹的语义诊断写入后续生成器与 evaluator 上下文，而非只更新标量 value。
- Failure：`Rollback and Verifier Dependence`——没有可回退环境或可信 terminal/synthetic verifier 时，树重放与价值反传的关键假设不成立。
- Failure：`Generic Reflection Local-Minimum Trap`——reflection 缺少可操作差异时只会重复局部策略，搜索增益主要来自扩展而非语义学习。

## 未解决问题

- `[OPEN_QUESTION]` 论文未报告 HotpotQA oracle correctness feedback 的调用时点/次数在各 baseline 间是否严格一致。
- `[OPEN_QUESTION]` synthetic tests 是否与 HumanEval 隐藏测试存在生成模型记忆或覆盖偏差，原文没有污染与测试质量审计。
- `[OPEN_QUESTION]` 表 9 对失败轨迹成本的结论主要是推断；缺少逐题总 token、wall-clock 与环境调用分解。
