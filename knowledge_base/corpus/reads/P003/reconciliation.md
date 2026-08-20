# P003 三读 reconciliation

## 1. 来源与全部尝试绑定

- PDF：`knowledge_base/staging/papers/P003_lats.pdf`；SHA-256：`a6b84613eeeaa3beb979ac3e34cbb3575bceb7ccf6050a2c2fc677d5e3a3ab19`
- 主 Codex 首读：`knowledge_base/pilot/reads/P003/read_1.md`；SHA-256：`03cf7d8671e67421cea4b952b581dac88458e82709a532654589098faa3c6d5d`
- 二读 `r2-20260719-p003-a1`：`ACCEPTED`。Invocation：`knowledge_base/pilot/reads/P003/read_2_attempts/r2-20260719-p003-a1/invocation.md`；SHA-256：`b7952f853dcef79ab9cde64130ae560ab19820c71363c0dd4718ae9b919d12ac`。Report：`knowledge_base/pilot/reads/P003/read_2_attempts/r2-20260719-p003-a1/report.md`；SHA-256：`1f4ff18f91d0d47223f7120136e21b20d6d838f17e09154f4d2cb3283e96fec0`。
- 第三读 `r3-20260719-p003-a1`：`ACCEPTED`；触发原因是 LATS 属高使用的 ReAct/ToT/Reflexion 组合边界材料，且两读发现深度、test 数和表间结果的来源冲突。Invocation：`knowledge_base/pilot/reads/P003/read_3_attempts/r3-20260719-p003-a1/invocation.md`；SHA-256：`fa1e9b1497065e3553cb8c11fcffe81e5a6c4f555c0f3c40bd534f6a44b4b56c`。Report：`knowledge_base/pilot/reads/P003/read_3_attempts/r3-20260719-p003-a1/report.md`；SHA-256：`6c00eb0a5ee62ae833f45af059e72b99cabe0f0b62695eba23447aeda8b4f926`。
- 其他 attempts：无。独立读者均为 `procedural_blinding`，声明未读前读/Cards/其他报告/blind query；第三读额外读取的非项目技能说明不含 P003 结论。

## 2. 七类逐项裁决

### Changed computation — `AGREE`

三读一致：LATS 把 CoT/ReAct 单轨推理改为 inference-time MCTS 变体，含 selection/expansion/evaluation/simulation/backpropagation/reflection；同一 LM充当 agent、state evaluator、reflection generator，环境终奖回传，失败轨迹/反思进入后续上下文。核点：PDF pp.4–6 §4、Figure 2/Algorithm 1。

### Baseline — `AGREE`

Hotpot reasoning-only 最近 baseline RAP .60 vs LATS(CoT) .62；acting 组合 baseline ToT(ReAct) .39、RAP(ReAct) .54 vs LATS(ReAct) .63，CoT→ReAct 的 LATS 组合 .71。HumanEval GPT-3.5 最强 baseline Reflexion 68.1 vs LATS 83.8；GPT-4 gap 91.0→92.7。WebShop LATS score 75.9 高，但 SR 38 低于 fine-tuning 45。核点：PDF pp.6–8 Tables 2–7。

### 公平性与预算 — `AGREE`

相同 trajectory budget `k` 不等于相同 LM/token/tool budget：每个 expansion 采 n=5，另调用 value/reflection；Table 9 只统计成功样本并未给简单 prompting token。HumanEval pass@1 是 5 candidates×8 iterations 后内部选一，并非一次原始生成。无跨方法完整 prompt/tool-call audit、seed/CI。核点：PDF pp.6–9。

### 主要结果 — `RESOLVED_BY_SOURCE`

核心 accuracy 使用主 Tables 2–8：Hotpot LATS(ReAct) .63、ToT(ReAct) .39；p.9 成本 Tables 9–10 的 .49/.61 与主表不一致，故只用于说明作者给出成功样本 cost analysis，不用于 accuracy Card。HumanEval/MBPP/WebShop/Game24 仍按各自主结果表窄述，避免跨模型/任务汇总成普遍优势。

### Limitation — `RESOLVED_BY_SOURCE`

第三读确认多个原文内部复现冲突：Hotpot depth 6/7、GPT-3.5 generated tests 4/6、Table 3/8 vs 9/10 数值、backprop/Algorithm 1 下标与签名、Hotpot reflection prompt疑似复制 value prompt。它们阻止从 PDF 精确重建实现，但不改变六阶段方法身份。另有 generic reflection/local minima、更多 depth 无益、环境与模型范围有限。

### Operator — `AGREE`

Pilot 抽取 `Feedback-Backpropagated Agent Tree Search`：用环境 observation/terminal reward、LM heuristic 与 verbal reflection共同更新可回溯 search tree。明确它是 ReAct+MCTS+value+reflection 的组合 Operator，不冒充单一新 primitive。

### Failure — `AGREE`

Pilot 抽取 `Generic Reflection and Sparse-Reward Search Collapse`：WebShop reflection 可泛化空泛并陷入 local minima；去 LM heuristic 时 Hotpot .63→.37，说明仅 terminal binary reward 不足。适用范围保留模型/任务/预算。

## 3. 未解决项与准入裁决

- `UNRESOLVED`（非阻断、已隔离）：精确 depth、GPT-3.5 tests 数、成本表 accuracy run 和附录 reflection prompt。它们禁止从 PDF 声称可精确复现；正式 Cards 不引用冲突字段。
- CORE disposition：`ACCEPT`。三读确认方法身份与主表窄结果，来源冲突已通过 Evidence 排除规则隔离。
- Task 5 计划：1 个 Operator Card、1 个 Failure Card、1 个 Paper Card；先建立 Evidence。
