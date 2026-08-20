# P008 双读 reconciliation

## 1. 来源与尝试绑定

- PDF：`knowledge_base/staging/papers/P008_agent_security_bench.pdf`；SHA-256：`e2505f8632bfcb6a64a4390a3170b3ca1dfd3f9916d7c3cf9ba2b89887b3a0c9`
- 主 Codex 首读：`knowledge_base/pilot/reads/P008/read_1.md`；SHA-256：`cfe5ebcaf2b5c169f17268b2b2cd31995b7207279461da00a56a0d6edbbc12e8`
- 二读 `r2-20260719-p008-a1`：`ACCEPTED`。Invocation：`knowledge_base/pilot/reads/P008/read_2_attempts/r2-20260719-p008-a1/invocation.md`；SHA-256：`571f0a9ca114ea3d1ccc6e170fb3ae4ef869aab1368d604d25ad7b141d4d6662`。Report：`knowledge_base/pilot/reads/P008/read_2_attempts/r2-20260719-p008-a1/report.md`；SHA-256：`3e394f3318135a7c3bbd48e0b381b6a8341f6d53625ef94c2bbe73dd1c85ea1d`。
- 其他二读 attempts：无。第三读 attempts：无；本文的角色是安全 failure/evaluation，不是该簇唯一直接祖先或唯一强方法 baseline；计划不超过两个 Operator/Failure Cards。两读关键判断一致，视觉核查没有解析语义冲突。
- 独立性：`procedural_blinding`；二读者声明未读取首读、Cards、其他报告或 blind query。

## 2. 七类逐项裁决

### Changed computation — `AGREE`

两读一致：ASB 是攻击面分解与评测，不是单一防御方法。它分别在 system prompt、user prompt、tool observation、retrieved memory 干预，并测试多入口组合；攻击目标是是否调用指定 malicious tool。核点：PDF pp.4–8 §3–4、Eqs. 5–10、Tables 1–4。

### Baseline — `AGREE`

无攻击 PNA 是 utility baseline；DPI 是最强单类攻击，DPI+MP（83.02%）是 mixed 84.30% 的最近简化组合。防御应与 matched no-defense 行比较，而非跨表直接比较。AgentDojo/InjecAgent 的 Table 12 只比较覆盖，不是共享任务/模型/预算的效果 baseline。核点：PDF pp.9–10、25、30。

### 公平性与预算 — `AGREE`

两读一致：13 个 backbone 的基础工具能力差异极大，低 ASR 可能来自不会完成任务；mixed 与单类攻击的 prompt 强度/入口数不等；PoT 多了 demonstrations；memory poison 由 GPT-4o-mini 生成；未报告完整重复数、CI、seed、token/cost。ASR/PNA 只匹配工具名，RR 则由 backbone judge，oracle 口径不统一。核点：PDF pp.8–10、25–31。

### 主要结果 — `RESOLVED_BY_SOURCE`

PDF p.9 Table 5 与 p.30 Table 14 都给 mixed `84.30%`，故采用 84.30；p.30 prose 的 `84.03%` 记为来源 typo，不用平均或猜测。单类平均为 DPI 72.68、IPI 27.55、memory poisoning 7.92、PoT 42.12。防御负结果包括 DPI delimiter 78.38→79.08、IPI sandwich 27.98→28.04、PoT shuffle 42.12→44.37。核点：PDF pp.9–10、30、33–35。

### Limitation — `AGREE`

工具无参数且返回固定模拟输出；tool invocation 不等于参数正确、权限成立或真实 side effect。攻击者权限很强，能加入恶意工具/修改多类输入；10 个场景和固定两步正常 workflow 不代表真实分布。Memory poisoning 平均 ASR 最低，不能外推一般 RAG memory。核点：PDF pp.4、8、23–29。

### Operator — `RESOLVED_BY_SOURCE`

Pilot 只抽取 `Information-Entry-Point Threat Decomposition`：显式记录攻击者权限、注入入口和干预时点，并同时保存攻击行为与 clean utility。NRP 不用作 CRL 自动总分；防御组件与具体攻击公式留在 Paper Card。

### Failure — `RESOLVED_BY_SOURCE`

Pilot 只抽取 `Prompt-Only Defense Non-Monotonicity`：delimiter/sandwich/shuffle 在对应 matched 条件下可使 ASR 不降反升，且多数 prompt defenses 降低 clean PNA。它是本文设置下的经验 failure，不推广成任何 prompt 防御必然无效。

## 3. 未解决项与准入裁决

- `UNRESOLVED`：无阻断项。
- 来源 open issues：Table 16 前 GPT-4o 文字与 13 模型表不一致；NRP 示例百分号书写不严谨；攻击数 13/16 的粒度口径未统一。它们不影响采用的入口分解和 matched 防御负结果。
- CORE disposition：`ACCEPT`。安全入口分解与非单调防御失败均有直接全文证据，且适用条件可窄化。
- Task 5 计划：1 个 Operator Card、1 个 Failure Card、1 个 Paper Card；先建立 Evidence。
