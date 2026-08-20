# P019 双读 reconciliation

## 1. 来源与尝试绑定

- PDF：`knowledge_base/staging/papers/P019_steca.pdf`；SHA-256：`f0957a2acf89227b77922ee4d5a9de10759cc6ad89778077f048c178a0184703`
- 主 Codex 首读：`knowledge_base/pilot/reads/P019/read_1.md`；SHA-256：`392a54c3c9ae2398430c8168a374631e8979bd27fdc2a7be2c3b7d97b76988e9`
- 二读 `r2-20260719-p019-a1`：`ACCEPTED`。Invocation：`knowledge_base/pilot/reads/P019/read_2_attempts/r2-20260719-p019-a1/invocation.md`；SHA-256：`655f8e5ce63df6357260174638627a6bec09980e97c74bc76d336ac068875ad7`。Report：`knowledge_base/pilot/reads/P019/read_2_attempts/r2-20260719-p019-a1/report.md`；SHA-256：`e0ea2859a5547b19fa4cd5a0736f2f24ca13ae306f2fbef8bebbe18b50acb661`。
- 其他二读 attempts：无。第三读 attempts：无；本文不是唯一祖先/强 baseline，计划不超过两个 Operator/Failure Cards；两读对方法、oracle、预算和主结果一致，来源内符号/案例瑕疵不改变窄结论。
- 独立性：`procedural_blinding`；二读者声明未读取项目首读/Cards/其他报告/blind query。系统要求的非项目技能说明不含 P019 结论。

## 2. 七类逐项裁决

### Changed computation — `AGREE`

两读一致：STeCa 在训练数据构造中以 N=5 continuation 的终奖估计 step reward，在 expert prefix 后探索并检测首个相邻 reward drop；随后将“上一动作非最优”及 ground-truth action 交给 GPT-4o 生成 reflection，拼接 expert suffix，再以 trajectory-distance reward 加权训练。测试只描述普通 ReAct greedy inference，没有在线 MC detector。核点：PDF pp.2–6 §§2–4、Eqs.1/5–10、pp.13–15。

### Baseline — `AGREE`

主表最强非 STeCa baseline 是 IPR，平均 68.6，STeCa 70.9；在相同收集数据上 SFT+DPO 70.0、无 reward tuning 69.6，是分离训练目标的更近组合 baseline。核点：PDF p.6 Table 1。

### 公平性与预算 — `AGREE`

Reflection 直接获得 ground-truth action，并由 GPT-4o 生成；自生成 variant 明显更差。MC 每步 5 rollouts，未报告总 rollout/GPU/GPT-4o token 成本或与 baseline 等预算。主表还并列 prompting-only 大模型与训练型 7B agent，不能跨类做纯方法归因。核点：PDF pp.6–7、13–15。

### 主要结果 — `AGREE`

Llama-2-7B SFT/IPR/STeCa 平均 63.3/68.6/70.9；同数据的 SFT+DPO/无 reward tuning 已到 70.0/69.6，说明大部分相对 SFT 增益可能来自新 expert-derived 轨迹，完整 weighting 的边际约 0.9–1.3 点。短任务与 SFT 同为 76.2。无多 seed/CI。核点：PDF pp.6、18 Tables 1/9。

### Limitation — `RESOLVED_BY_SOURCE`

只处理首个 deviation；detector precision/recall 与 N=5 方差未报；nDTW action representation/distance 不明；Figure 4 的 seen analysis 从训练 calibration pool `D_c` 抽样且未说明剔除，不能作独立泛化证据。`δ≥0` 定义却测 -0.01。来源内部另有 GPT-4/GPT-4o、`L_Ds/L_Db` 和 Figure 9 observation/thought 冲突，均按原文保留。

### Operator — `RESOLVED_BY_SOURCE`

Pilot 只抽取 `First-Deviation Oracle-Calibrated Trajectory Synthesis`：训练期用 outcome-rollout reward 找首个疑似偏差，再以 ground-truth action、teacher reflection 与 expert suffix造校准轨迹。Step reward 是其组成，不另拆 Operator Card。

### Failure — `RESOLVED_BY_SOURCE`

Pilot 只抽取 `Ground-Truth Rationalization Mistaken for Self-Reflection`：teacher 已知动作错误及正确 action，产生的是 oracle-guided rationale/蒸馏数据，不是未知答案条件下的自主纠错。有限 MC误检与 calibration-pool reuse 作为 Paper Card 的附加风险。

## 3. 未解决项与准入裁决

- `UNRESOLVED`：无阻断项；训练数据复用疑点阻止使用 Figure 4 seen 分析，但不使主 held-out Table 1 或方法身份失效。
- Open limits：seen 100 条是否剔除、detector 质量、nDTW 实现、预算对齐和多 seed 未解决。
- CORE disposition：`ACCEPT`。它提供 agent learning/反思交叉处清晰 Operator 与高价值 oracle Failure。
- Task 5 计划：1 个 Operator Card、1 个 Failure Card、1 个 Paper Card；先创建 Evidence。
