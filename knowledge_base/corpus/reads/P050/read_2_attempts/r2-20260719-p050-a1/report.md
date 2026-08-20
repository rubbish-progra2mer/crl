# P050 独立二读报告

## 来源与读取声明

- 冻结调用快照：`knowledge_base/corpus/reads/P050/read_2_attempts/r2-20260719-p050-a1/invocation.md`
- 论文：*Scaling Agentic Verifier for Competitive Coding*
- PDF SHA-256：`81b1a3759a4de1b246240342435ef32f0f7d7265d17a938bd78086fe027b8654`
- [AUTHOR_FACT] 已逐页读取全部 20 个物理页。

## 1. changed computation、I/O 与训练

- [AUTHOR_FACT] 给定题目和一对候选程序，Agentic Verifier 多轮调用 Python/C++ sandbox，分析两程序行为并最终输出一个 input generator；成功条件是生成满足题目约束且令两程序输出不同的输入。（物理页 4–5，§3.1；图 2）
- [AUTHOR_FACT] 推理时不生成 ground-truth output，而是对多个候选在生成输入上的输出按一致簇投票：每个输入上属于最大输出簇的候选得一票，总票最高者被选。（物理页 2–3，§2.1）
- [AUTHOR_FACT] 训练数据来自开源竞赛题与爬取 online-judge 提交；无公开测试的题目用多个参考解共识构造平均约 60 个测试。随后由 Qwen3-235B teacher 拒绝采样成功轨迹约 60K，SFT 到 Qwen3-30B；再以 10K queries 做 400 steps GRPO，500 queries 仅用于训练监控。（物理页 5–6，§3.2–3.4）
- [READER_INTERPRETATION] changed computation 是“主动、成对、交互式找分歧输入”，而非随机生成或生成完整 input-output oracle；输出分歧只能说明程序不等价，单独不能判断哪一个正确。

## 2. 基线、预算与主结果

- [AUTHOR_FACT] 评测 USACO 307、LiveCodeBench 175、OJBench 232、ICPC-Eval 118，以及作者构造的 CodeForces 64 题；policy models 为 Qwen3-30B-A3B-Thinking-2507 与 Qwen3-235B-A22B-Thinking-2507。（物理页 6，§4.1）
- [AUTHOR_FACT] 基线包括 Vanilla、Skywork Grading RM、MBR-Exec hard/soft、CodeT、CodeRM、Random Generator。所有需要生成 tests 的执行基线使用 Qwen3-30B，预算均为每题 512 个 test inputs/test cases；Agentic Verifier 随机抽候选对，每对生成一个输入以匹配数量预算。（物理页 6–7，Implementation details）
- [READER_INTERPRETATION] “512 个测试”只匹配产出数量，不匹配推理成本：Agentic Verifier 每个输入包含多轮 code execution 和专门训练模型，Random Generator/CodeRM 的每个样本计算不同；不能称为同 token/tool-call/latency 预算。
- [AUTHOR_FACT] 表 1 中 Agentic Verifier 在两 policy、五数据集、Best@8/64 全部为最高。30B policy 的 Best@64 例如 USACO 74.5（Random 70.2）、ICPC 25.8（22.2）、CodeForces 46.4（40.1）；235B policy 为 84.1（82.2）、31.2（29.7）、50.9（45.4）。（物理页 7，表 1）
- [AUTHOR_FACT] 强度分层并非处处单调压倒所有基线：OJBench medium、30B policy 下 Random Generator 82.7，高于 Agentic Verifier 80.0；但 hard 上 Agentic 为 20.7、Random 11.9。（物理页 8，表 2）

## 3. oracle、有效性与泄漏边界

- [AUTHOR_FACT] 输入有效性由 LLM 生成的 Python validator 判断；validator 只要求与所有高置信合成测试一致。参考解/正确提交也以多数输出共识和已有测试过滤。（物理页 5；物理页 20，validator prompt）
- [READER_INTERPRETATION] 这不是形式化输入语法/语义证明；validator 漏约束时，无效输入也可能制造“分歧”。训练奖励和推理收益均依赖该自动验证器质量。
- [AUTHOR_FACT] LiveCodeBench 选择 2025-02 之后题目以降低模型数据污染；但训练题来源只概述为多源开源集和在线 judge 爬取。（物理页 5–6）
- [OPEN_QUESTION] 原文没有报告训练问题与 USACO/OJBench/ICPC/CodeForces 评测题的去重、时间切分或污染审计；“新日期”主要针对 policy model 记忆，不能自动排除 verifier 训练重合。
- [OPEN_QUESTION] 没有报告 verifier 每个输入的平均轮次、sandbox calls、token、wall-clock、失败/timeout 率及端到端成本，无法完成等预算复算。

## 4. 负向结果、限制与 oracle 解释

- [AUTHOR_FACT] 随机输入即使扩到 64 个仍常显著弱于 benchmark ground-truth inputs；Agentic inputs 在 USACO 可超过 ground-truth，但 LiveCodeBench/OJBench 略低。（物理页 3，图 1）
- [AUTHOR_FACT] 训练监控的 500-query held-out set 只证明 GRPO 过程中 reward/invalid/distinguish rate 改善，不等于五个下游 benchmark 的无污染留出。（物理页 6，图 3）
- [AUTHOR_FACT] 论文展示两个都通过固定 benchmark tests 的程序被新输入分开，并经题意推导判定其中一个违反动态相邻约束。（物理页 9、13、15–17，图 5）
- [READER_INTERPRETATION] 该案例证明固定测试可能有 false positive，也说明用固定 benchmark pass label 评估 reranker 会受 oracle 噪声影响；但仅有分歧时多数投票仍可能拥护同一错误簇。
- [READER_INTERPRETATION] 论文没有独立 Limitations 节。未测边界包括 special judge/浮点/交互题、恶意程序、非 Python/C++、validator 系统性错误、候选高度相关导致多数错误，以及真实计算成本。

## 5. Operator、Failure 与建议

- [READER_INTERPRETATION] Operator 候选：对候选程序成对调用交互式 verifier 主动找分歧输入，再将输入加入输出一致性投票；若有高置信 reference，可把它改成定向 counterexample search。
- [READER_INTERPRETATION] Failure 候选：随机输入在大空间难触发角落条件；固定 benchmark tests 产生 false positive；LLM validator 漏约束；输出多数不等于真值；仅匹配测试条数掩盖多轮预算差异。
- [READER_INTERPRETATION] 建议保留为强 changed-computation 和跨数据集效果证据，但强制附带训练—测试去重未报告、validator 非形式证明、512 仅数量匹配与无成本报告；“发现行为差异”不得升级成“证明正确程序”。

## 6. 可视核验

- [AUTHOR_FACT] 已核对物理页 7 表 1 与物理页 8 图 4/表 2，Best@k 数值和部分非单调结果与抽取文本一致；未见实质冲突。

