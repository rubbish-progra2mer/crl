# P098 first read (W06) — P098 Constraint Injection：目标等价盲区 + 探针作训练信号

Status: `DRAFT_BEFORE_INDEPENDENT_READ`
Reader: main Codex
Read date: 2026-07-27 (Asia/Shanghai)

## Canonical source and bytes

- Title: Beyond Objective Equivalence: Constraint Injection for LLM-Based Optimization Modeling on Vehicle Routing Problems
- Authors: Xizi Luo; Changhong He; Dongdong Geng; Chenggong Shi; Yu Mei（北航 + 百度，实习工作，ACL 模板 preprint）
- Identity: arXiv 2606.04816v1 (2026-06-03)，cs.AI/cs.LG，28pp
- PDF: `knowledge_base/staging/w06_targeted/P098_constraint_injection.pdf`
- PDF SHA-256: `f73aaa44ab843311d0676030081b8f1b9e18f9e9bb0bb0b9a87c761917b43ab3`
- Parse check: 28 physical pages

## Canonical contribution

指认 SFT 过滤与 RL 奖励的共同盲区——**目标等价**（differential testing / answer agreement）对约束集结构性失明：非绑定约束的伪增（spurious over-constraint）与静默缺失（silent omission）都能通过。提出 **constraint injection**：把候选程序目标替换为常数变纯可行性查询，注入已知标签的解——可行探针必须被接受（测伪增）、单约束违反探针必须被拒绝（测缺失）；与 DIFF 组成 dual verifier，信号与单实例最优解解耦。**用途是训练信号**：作数据合成的拒绝采样过滤器 + GRPO 逐 rollout 奖励，训出 8B 端到端 VRPCoder（21 变体专家验证基准，18 训 3 留出）。


## Evidence and closest lineage

- 主结果（Table 2，四 VRP 基准 700 题 Pass@1）：VRPCoder-GRPO 93.00 平均，三个基准超 Gemini-3.1-Pro Preview，超 Claude-Sonnet-4.5 28 点、超既有 OR-LLM 78 点；把 Qwen3-8B 从 0.57 提到 93.00（+92 点，同规模）。
- 注入消融（Table 3）：去掉注入信号（保守设置下无注入侧数据集更大）SFT −2.86 / GRPO −4.00 平均——**探针信号对训练质量的净贡献被隔离**。
- Fig.1 钉子案例：漏 subtour-elimination 的候选与参考最优目标值相同（DIFF 通过），注入断连子回路探针即暴露。
- 谱系：ORLM/OptMATH/LLMOPT/ReSocratic（SFT 线）、SIRL/FOARL/StepORLM/OR-R1（RL 线）、DRoC/ARS/AFL（推理时 VRP 线）——均止于执行性/目标等价。

## Measurement and fairness boundaries

- 作者自认（Limitations）：域覆盖限 VRP 家族；探针依赖结构化 Cgold 形式化与**人工设计的 attacker 启发式目录**（奇异领域规则仍需手工）；**评测口径仍是 Pass@1（目标等价度量）**——dual verifier 算出的约束级多维信号被压成二元成功，细粒度约束违规剖面指标自认 open problem。
- Pass@1 与训练数据同族（18/21 变体在训练内）；Benchmark 4 的 TSPTW 缺席训练致 −8.4 点——组合泛化边界诚实披露。

## Draft knowledge objects

### Failure draft: `Objective Equivalence Passes Non-Binding Constraint Errors into Training Data`

非绑定约束的伪增/缺失通过 DIFF 与 answer-agreement 过滤进入 SFT 数据并获得正 RL 奖励（Fig.1 钉子案例）；评测 Pass@1 同样测不出。此失败在数据合成与奖励两个层面同时污染。

### Operator draft: `Feasibility-Probe Dual Verifier as Data Filter and RL Reward`

目标置常数 + 注入带标签解 → 可行性判定与标签比对；伪增/缺失双向覆盖；作为拒绝采样过滤器与 GRPO 逐 rollout 奖励复用。Predicted signature = 注入信号移除后 Pass@1 下降（−2.9/−4.0 实测）。前提 = 有结构化参考形式化与 attacker 目录。

## Draft Evidence locators

- Physical p.1: Fig.1 钉子案例与 dual verifier 图示。
- Physical p.2: 两失败模式定义与非绑定引语；贡献清单。
- Physical pp.3-4: CVRP/MTZ 形式化、DIFF/INJ 算子定义。
- Physical p.8: Table 2/3 主结果与注入消融。
- Limitations 节：域/attacker/口径三限与 open problem 引语。

All claims remain draft until independent read and reconciliation.
