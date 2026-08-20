# P002 三读 reconciliation

## 1. 来源与全部尝试绑定

- PDF：`knowledge_base/staging/papers/P002_tree_of_thoughts.pdf`；SHA-256：`6939cadebd84c8cdcc6ff3c2082b75851a86e2ef82008848d0af692f80521fa7`
- 主 Codex 首读：`knowledge_base/pilot/reads/P002/read_1.md`；SHA-256：`74eabbb16fddb11aeb7f0b529b0d1172de8ab8b1a034c35a2e995222d2a6a3ad`
- 二读 `r2-20260719-p002-a1`：`ACCEPTED`。Invocation：`knowledge_base/pilot/reads/P002/read_2_attempts/r2-20260719-p002-a1/invocation.md`；SHA-256：`e84f1f3f8bd27202c370b8ff14d9e9c7f6635a22c990e9856f7965fb06f59f2b`。Report：`knowledge_base/pilot/reads/P002/read_2_attempts/r2-20260719-p002-a1/report.md`；SHA-256：`2ce94285e65e4307337b4a1878bf5e283c4edef26da5a3823daa0c5e93df7d95`。
- 第三读 `r3-20260719-p002-a1`：`ACCEPTED`；触发原因为 ToT 是显式 test-time search 的唯一直接祖先/强 baseline。Invocation：`knowledge_base/pilot/reads/P002/read_3_attempts/r3-20260719-p002-a1/invocation.md`；SHA-256：`8909b3373bc13ffaf3cc9193830262b43884fc2804062ca609d48d94c2bd68ba`。Report：`knowledge_base/pilot/reads/P002/read_3_attempts/r3-20260719-p002-a1/report.md`；SHA-256：`7dbe86a3e30d56c2f6766b142a0ccf41f8b143860b8e615a99ea17d6290e1ddf`。
- 其他 attempts：无。两位独立读者均为 `procedural_blinding`，声明未读前读/Cards/其他报告/blind query。

## 2. 七类逐项裁决

### Changed computation — `AGREE`

三读一致：ToT 将连续 CoT 改为显式 state tree；每一层按任务定义 thought unit，生成多个候选、用 LM 评价，再由 BFS/DFS 保留、剪枝或回溯。四个可分组件是 decomposition/generator/evaluator/search。核点：PDF pp.3–5 §3、Algorithms 1–2/Table 1。

### Baseline — `AGREE`

Game of 24 最近非 oracle baseline 是 IO+Refine 27%，ToT b=5 为 74；oracle best-of-100 不是部署 baseline。Creative Writing IO+Refine 7.67 数值高于纯 ToT 7.56，ToT+Refine 7.91；Crosswords 主要对照 IO/CoT。不同任务最强 baseline 不同，不能只与弱 CoT 比。核点：PDF pp.5–8 Tables 2–3/Figures 3–5。

### 公平性与预算 — `AGREE`

ToT 同时改变 prompt、调用数、候选数、自评和控制流；Game of 24 约 5.5k completion tokens/$0.74，Creative Writing 约 4k/$0.32，作者称可为 CoT 的 5–100 倍生成 token。IO+Refine、best-of-k 和 Crosswords best state 含 oracle反馈/选择。无严格等计算对照、模型 snapshot/seed/CI。核点：PDF pp.5–8、14 Tables 7–8。

### 主要结果 — `AGREE`

Game of 24 ToT b=1/b=5 45/74 vs IO 7.3、CoT 4；Crosswords word/game 60%/4 of 20；但 GSM8K/StrategyQA 附录仅 90 vs 86、83 vs 82，说明已有强 CoT/外部知识瓶颈下增益有限。Creative Writing pure ToT 不胜 IO+Refine。核点：PDF pp.6–8、13–14。

### Limitation — `RESOLVED_BY_SOURCE`

Crosswords evaluator 会 false-negative prune；无剪枝找到的解可被最终启发式遗漏，oracle best-state 7/20 vs 主输出 4/20。Algorithm 2 变量/状态写法有原文笔误，Table 8 图注误称 Game of 24，图内字体文本抽取异常需视觉核对。只测 BFS/DFS、三个刻意挑战任务，未测试动态工具环境或等预算。

### Operator — `AGREE`

Pilot 抽取 `LM-Heuristic Branch-and-Revisit Search`：任务化 thought state，多候选扩展、LM heuristic 评价与 BFS/DFS 回溯。各 task 的具体 thought 粒度是实例化而非新 Card。

### Failure — `AGREE`

Pilot 抽取 `False-Negative Pruning and Output-State Loss`：LM 把可解状态判 impossible 会剪掉正确子树，即使轨迹中找到解，启发式最终状态选择仍可漏解。核点：PDF p.8 §4.3。

## 3. 未解决项与准入裁决

- `UNRESOLVED`：无阻断项。
- Open limits：等 token/call 对照、评价者独立性、模型快照、图内精确 prompt 与高级搜索未测试。
- CORE disposition：`ACCEPT`。三读确认显式 search 祖先机制与直接 failure。
- Task 5 计划：1 个 Operator Card、1 个 Failure Card、1 个 Paper Card；先建立 Evidence。
