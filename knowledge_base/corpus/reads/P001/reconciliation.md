# P001 三读 reconciliation

## 1. 来源与全部尝试绑定

- PDF：`knowledge_base/staging/papers/P001_react.pdf`；SHA-256：`f285b0971ae4a790e402fb93966bed3adde2cf0a04977d08b2b40d6ab0cace69`
- 主 Codex 首读：`knowledge_base/pilot/reads/P001/read_1.md`；SHA-256：`987b888fed6d263eee5756a928d9405846be42f33a1f95c00bc0b9684ff76134`
- 二读 `r2-20260719-p001-a1`：`ACCEPTED`。Invocation：`knowledge_base/pilot/reads/P001/read_2_attempts/r2-20260719-p001-a1/invocation.md`；SHA-256：`fbe4dea820e4cf8a45d2273ee8f283d72e8924785cb68e31d53c4a743a41e385`。Report：`knowledge_base/pilot/reads/P001/read_2_attempts/r2-20260719-p001-a1/report.md`；SHA-256：`d1bd437bb205c5796d42fd7a1fd566ced1f4d824b55dc7fd0698e64bda5dc3a4`。
- 第三读 `r3-20260719-p001-a1`：`ACCEPTED`；触发原因为 ReAct 是 planning/tool-use 唯一直接祖先之一，且 p.23 Table 7 视觉内容与 “Act no thoughts” 标题冲突。Invocation：`knowledge_base/pilot/reads/P001/read_3_attempts/r3-20260719-p001-a1/invocation.md`；SHA-256：`d30b77cce1ec84f4d8cf29ee359c698212fbc3b47906bd483692133a79d13664`。Report：`knowledge_base/pilot/reads/P001/read_3_attempts/r3-20260719-p001-a1/report.md`；SHA-256：`1a2538acbd50f7a76a2cbc4bfc81d2a895e9c17a6db4b405f17c89f7d5fcd96d`。
- 其他二/三读 attempts：无。两位独立读者均为 `procedural_blinding`，声明未读取前读、Cards、其他报告或 blind query；App 无文件级技术 allowlist。

## 2. 七类逐项裁决

### Changed computation — `AGREE`

三读一致：ReAct 将 agent 动作空间从外部 actions `A` 扩展为 `A∪L`，thought 不改变环境却写回上下文，随后 action 获得 observation；知识任务密集交错，决策任务稀疏异步。最小机制是 forward 之间增加语言状态更新，不是环境或模型参数改变。核点：PDF pp.3–4 §2。

### Baseline — `RESOLVED_BY_SOURCE`

知识任务最接近机制对照为同工具 access 的 Act（移除 thoughts），reasoning-only 为 CoT，最高非 ReAct prompting baseline 是 CoT-SC；混合 gated fallback 通常最强。ALFWorld 的 Act/ReAct也意图使用同轨迹删除 thought，但 Table 7 原文矛盾使其 prompt-level isolation 不可完全复核，故不以该附录例子作为 clean baseline 证据。核点：PDF pp.5–8 Tables 1/3/4、p.23 Table 7。

### 公平性与预算 — `AGREE`

Standard/CoT 无 Wikipedia，Act/ReAct 有工具；CoT-SC 使用 21 条温度 0.7 samples，ReAct/Act多为单轨 greedy；best-of-6、IL/RL 数据规模亦不同。未报告逐题 token/tool-call/latency，不能把所有差异归因 thought。Wikipedia state 与 API snapshot 也未冻结。核点：PDF pp.4–8、14、22–23。

### 主要结果 — `AGREE`

Table 1：ReAct 在 HotpotQA 27.4 低于 CoT 29.4/CoT-SC 33.4，但 FEVER 60.9 高于 CoT-SC 60.4；混合策略达 35.1/64.6。ALFWorld ReAct average/best-of-6 57/71 vs Act 45；WebShop 66.6/40.0 vs 62.3/30.1。支持“交错机制在部分设置有效且混合最好”，不支持普遍单独最优。

### Limitation — `RESOLVED_BY_SOURCE`

第三读确认 p.23 Table 7 同一可视页标题称 Act 无 thought，却含 `think:`；来源无法说明是排版遗留还是实际 prompt 污染。该点记为 open source limitation，并明确禁止用该表作 Act 完全移除 thought 的证据。另有 search error、循环、small-model few-shot 退化、成本/统计缺失及动态 Wikipedia 复现问题。

### Operator — `AGREE`

Pilot 抽取 `Interleaved Reason–Act Context Update`：在环境 action 前/后生成可写回 context 的 thought，用 observation 再规划下一步。Tool API 是独立信息源，Paper Card 必须写清，不把外部信息增益混入 Operator 定义。

### Failure — `RESOLVED_BY_SOURCE`

Pilot 抽取 `Non-Informative Retrieval / Repetitive Loop Recovery Failure`：空/无用 observation 后重复旧 thought/action或难以改写 query。它只描述本文轨迹与失败样本，p.6 Table 2 的 23% 是作者标注子集条件比例。

## 3. 未解决项与准入裁决

- `UNRESOLVED`（非阻断、已隔离）：实际 ALFWorld Act prompt 是否完全移除 thoughts。它会阻止把 ALFWorld Act gap 当 thought 的纯因果效应，但不改变 ReAct 方法身份、其他任务结果或祖先角色。
- 其他 open limits：等预算成本、prompt best-of selection、微调轨迹筛选和 Wikipedia snapshot。
- CORE disposition：`ACCEPT`。三读确认祖先机制，且 source conflict 已通过缩窄 Evidence 使用范围隔离。
- Task 5 计划：1 个 Operator Card、1 个 Failure Card、1 个 Paper Card；先建立 Evidence。
