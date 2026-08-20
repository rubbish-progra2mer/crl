# P007 双读 reconciliation

## 1. 来源与尝试绑定

- PDF：`knowledge_base/staging/papers/P007_tau_bench.pdf`；SHA-256：`e2d45d573e1fce753ead1a44cc468ad386dd384e2668450d0a9c0e2c7920ada0`
- 主 Codex 首读：`knowledge_base/pilot/reads/P007/read_1.md`；SHA-256：`47f76f5f4fe60be1abd62c459f1ba0c1fd3ff0c5c4df8185b2af330c81c42631`
- 二读 `r2-20260719-p007-a1`：`ACCEPTED`。Invocation：`knowledge_base/pilot/reads/P007/read_2_attempts/r2-20260719-p007-a1/invocation.md`；SHA-256：`c8bb0d145ba285fe7d57828c6e643c4c5035482defc3810040f7314a2450de0d`。Report：`knowledge_base/pilot/reads/P007/read_2_attempts/r2-20260719-p007-a1/report.md`；SHA-256：`13b62cf423160b9a8121df6105399cc4c9a9f4c936ef1ab274a147a9d1a4fd42`。
- 其他二读 attempts：无。第三读 attempts：无；本文是 Pilot 的交互评测材料而非某机制簇唯一直接祖先/强方法基线，计划不超过两个 Operator/Failure Cards，两读对关键结论无冲突，视觉核查未发现实质解析冲突。
- 独立性边界：`procedural_blinding`；二读者声明未读首读、Cards、其他报告或 blind query。系统技能说明不是项目科研输入。

## 2. 七类逐项裁决

### Changed computation — `AGREE`

两读一致：τ-bench 改变的是评测计算而非 Agent 参数更新——把隐藏 intent、LM 用户、domain policy、数据库 read/write tools 组成动态交互闭环，以最终数据库与必要输出计算单次 reward，再用 `pass^k` 聚合 k 次均成功的可靠性。核点：PDF pp.3–5 §3、Figure 2 与公式。

### Baseline — `AGREE`

同模型 FC、text-ReAct、Act 是最接近接口对照；policy-removal 是政策利用消融。主表最佳组合为 gpt-4o+FC，retail/airline 为 61.2/35.2；论文中的 average 是两域等权，不按 115/50 task 数加权。用户模拟 reflection 的 0.406 是 simulator 改造结果，不能写成 agent reflection 基线。核点：PDF pp.7–9 Tables 2–4/Figures 3–4。

### 公平性与预算 — `AGREE`

两读一致：只统一最多 30 个 agent actions，未按方法配平 tokens/tool calls/latency；Llama-3 还因接口能力使用 text-ReAct。任务被反复用 GPT-4-Turbo FC 调整，存在作者明示的 curation bias。`pass^k` 同时包含 agent 与 LM-user 轨迹随机性，不能称纯 agent 随机性。核点：PDF pp.5、7–10。

### 主要结果 — `AGREE`

Figure 4 显示单次 retail 成功超过 60% 时 `pass^8` 仍低于 25%，支撑“best-of-k discovery 与连续可靠性不同”的窄结论。Table 3 的 policy removal 对 gpt-4o airline 33.2→10.8，说明 policy 可用性有影响，但不同模型利用程度不同。核点：PDF pp.7–9。

### Limitation — `AGREE`

两读一致：`r=1` 只是必要非充分，未经确认的 write 仍可能通过；字符串输出匹配未做人评校准；仅两个简化合成域，无真实用户外部效度；小模型、planning/self-reflection agent 未测；唯一结果与 simulator 仍有人工/模型偏差。核点：PDF pp.5、7、9–10。

### Operator — `RESOLVED_BY_SOURCE`

Pilot 只抽取一个 `Repeated-Trial Goal-State Reliability Evaluation`：允许自由交互/只读路径，以唯一终态+必要输出判断单次成功，并以 `pass^k` 衡量重复全成功。Interactive loop、policy condition 和 policy-removal 作为其实现/消融背景，不拆成多个 Operator Cards。

### Failure — `RESOLVED_BY_SOURCE`

Pilot 只抽取 `Terminal-State Success with Process-Policy Violation`：作者明确指出当前 reward 可能在未获用户确认的 return/write 下仍给 1。复合请求部分解决、wrong argument/info 等保留为 Paper Card 的实证失败谱，不外推为所有 agent 的普遍比例。

## 3. 未解决项与准入裁决

- `UNRESOLVED`：无阻断项。
- Open limits：输出 substring matcher 误差、过程级政策违规比例、`pass^k` 中双方随机性分解和 task curation 偏移未被原文解决。
- CORE disposition：`ACCEPT`。它提供可追溯的交互可靠性评测 Operator 和终态 oracle 覆盖缺口 Failure。
- Task 5 计划：1 个 Operator Card、1 个 Failure Card、1 个 Paper Card；先绑定页码级 Evidence。
