# P006 三读 reconciliation

## 1. 来源与全部尝试绑定

- PDF：`knowledge_base/staging/papers/P006_llmcompiler.pdf`；SHA-256：`36dde899ed8abe0df728215e054aab21d1699add719afeb0ddadbb4e4eb23263`
- 主 Codex 首读：`knowledge_base/pilot/reads/P006/read_1.md`；SHA-256：`f2de77325ef37f019376bf521d21e6cc4ef71b8f37f952409f7b73521b9f18e4`
- 二读 `r2-20260719-p006-a1`：`ACCEPTED`。Invocation：`knowledge_base/pilot/reads/P006/read_2_attempts/r2-20260719-p006-a1/invocation.md`；SHA-256：`93c36cf1375d0c2f0a657c36fb492be46a518b881d7fcea3c0eb78e8ad442761`。Report：`knowledge_base/pilot/reads/P006/read_2_attempts/r2-20260719-p006-a1/report.md`；SHA-256：`3bdef6d17a17c082e0502aa3506d1375fac77aceac604a38d741b0809cf05598`。
- 第三读 `r3-20260719-p006-a1`：`ACCEPTED`；触发原因是二读发现 Game of 24 speedup 2.01×/2.09× 来源不一致，属于主要效率结果。Invocation：`knowledge_base/pilot/reads/P006/read_3_attempts/r3-20260719-p006-a1/invocation.md`；SHA-256：`3450c8f35ecbd0ecac1903209602dfc1b75776e286fe268d29b43014081574e9`。Report：`knowledge_base/pilot/reads/P006/read_3_attempts/r3-20260719-p006-a1/report.md`；SHA-256：`458ba2fd46a31c2f7cfe87be081ebd2774c2fa5b66ffa5c4f896b871dc55ec90`。
- 其他 attempts：无。独立读者均为 `procedural_blinding`，声明未读前读/Cards/其他报告/blind query。二读完成可视页面核查；三读受工具回传限制，只完成原生 PDF 文本/几何核查，该限制如实保留。

## 2. 七类逐项裁决

### Changed computation — `AGREE`

三读一致：Planner 生成含 `$id` 数据依赖的任务 DAG；无 LLM Fetching Unit 依赖就绪即替换实际输出并调度，Executor 异步并行，必要时 observation 回到 Planner 重新编译；Planner 还可流式输出。核心是串行 reason-act-observe 改为显式依赖图+机械并发，而非模型权重改变。核点：PDF pp.3–5 §3–4/Figure 2。

### Baseline — `AGREE`

Hotpot/Movie/ParallelQA 的直接 baseline 是 ReAct/ReAct†与 OpenAI parallel calling；Game24 是 ToT；WebShop 用 ReAct/LATS/LASER，但 LATS/LASER 值来自各自论文，仅 ReAct由本文复现。缺少“相同 Planner/DAG/调用集合、仅串行 Executor”的纯并行消融。核点：PDF pp.6–9 Tables 1/3。

### 公平性与预算 — `AGREE`

同 benchmark 的模型/examples基本相同，但 ReAct†有专用 anti-loop prompt；调用数/信息覆盖不同，Movie Rec LLMCompiler几乎完成8次搜索，WebShop访问约10项，ReAct常早停。WebShop跨论文 latency 不同 N/模型/运行环境，不可严格比较 101.7×/2.69×。核点：PDF pp.6–9、13–16。

### 主要结果 — `RESOLVED_BY_SOURCE`

Table 1 支持近似 accuracy 下显著降 latency：Hotpot 62.00/3.95s vs ReAct† 62.47/7.12s；Movie 77.13/5.47s vs 72.47/20.47s；ParallelQA 89.38/16.69s vs 89.09/35.90s。Game24 LLaMA latency 952.06/456.02，直接复算为 2.0878≈2.09，因此采用 Table 1 的 2.09×，p.8 prose 的 2.01×记为来源 typo。核点：PDF p.6 Table 1、p.8 §5.3。

### Limitation — `RESOLVED_BY_SOURCE`

Appendix A 把 Movie Rec 70.00/77.80误称 Hotpot；Appendix B 的 10.6%/36 计数单位不明。并行上限受 Planner/final/join straggler；streaming 对短工具仅 1.01/1.03×；WebShop反而更慢；固定两搜索会失去少量 ReAct适应性 retry。副作用、隐藏依赖、rate limit、并发写未测。核点：PDF pp.9、13–17。

### Operator — `AGREE`

Pilot 抽取 `LLM-Declared Dependency DAG with Mechanical Parallel Dispatch`：LM 只声明任务/依赖，机械调度器在依赖满足后并行执行；observation-dependent 分支再局部 replan。Streaming 是实现优化，不另拆 Card。

### Failure — `AGREE`

Pilot 抽取 `Static Parallel Plan Loses Adaptive Retry / Misbinds Dependencies`：预编译减少循环但会错接 placeholder，且固定调用可失去失败查询后的替代实体重试。限定于论文工具/任务设置。

## 3. 未解决项与准入裁决

- `UNRESOLVED`：无阻断项。
- Open limits：WebShop跨论文 latency、ParallelQA失败计数单位、隐藏并发依赖和等调用预算 accuracy 归因未解决。
- CORE disposition：`ACCEPT`。三读解决主 speedup 数字口径并确认 changed computation。
- Task 5 计划：1 个 Operator Card、1 个 Failure Card、1 个 Paper Card；先建立 Evidence。
