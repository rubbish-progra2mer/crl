# P017 双读 reconciliation

## 1. 来源与尝试绑定

- PDF：`knowledge_base/staging/papers/P017_information_propagation_topologies.pdf`；SHA-256：`f94767d936354030dc25f10db92a2f6f85f49b7d7163ac45b253e047ca67bd8b`
- 主 Codex 首读：`knowledge_base/pilot/reads/P017/read_1.md`；SHA-256：`82597ff7b53eb8c6e579a09ea5ac15ce9f3808b90d539a50560fef677554e0ee`
- 二读 `r2-20260719-p017-a1`：`ACCEPTED`。Invocation：`knowledge_base/pilot/reads/P017/read_2_attempts/r2-20260719-p017-a1/invocation.md`；SHA-256：`a7186fde756e17cd60b05f26f6667a71c4266757ab3bc1d5db4c56c154bd687e`。Report：`knowledge_base/pilot/reads/P017/read_2_attempts/r2-20260719-p017-a1/report.md`；SHA-256：`30d1e458e781d67bfb51e11cffb0c9d9407905192555429e5c5291a04a7e7617`。
- 其他二读 attempts：无。第三读 attempts：无；本文不是该簇唯一祖先/强 baseline，计划不超过两个 Operator/Failure Cards。两读对 changed computation、oracle、预算和主结果一致；来源内案例/伪代码瑕疵不影响窄结论。
- 独立性：`procedural_blinding`；二读者声明未读取首读、Cards、其他报告或 blind query。系统技能说明不含项目结论。

## 2. 七类逐项裁决

### Changed computation — `AGREE`

两读一致：CAPE/TCTE 是对固定拓扑的人工输出干预分析；EIB-Learner 则在会话前以 query/role 特征分别从 Chain/Full GNN 得 sparse/dense mask，用 query gate 融合并采样拓扑，以最终任务 reward 做 policy gradient。它改变 agent 间可见路径，不改变基础 LLM。核点：PDF pp.3–7 §§3–4、Figure 3、Eqs.5–11。

### Baseline — `AGREE`

Table 1 最强外部 baseline 是 G-Designer 90.04，EIB 91.38；固定/非自动拓扑中 LLM-Debate 87.53。Ablation 只覆盖 MMLU/GSM8K/HumanEval，不能推广全部六项。核点：PDF pp.7–8 Tables 1–2。

### 公平性与预算 — `AGREE`

错误干预由 prompt 强制，helpful insight 直接注入正确答案，是 oracle/artificial stress test，不是自然检测/恢复。EIB 相对 G-Designer token 略多（约 2.3e5 vs 2.2e5；8.8e6 vs 8.2e6），小优化集仅 40/60 queries，未报告 split、重复训练、CI/显著性和完整 prompts。核点：PDF pp.4–5、7–9。

### 主要结果 — `AGREE`

支持的窄结果是所测设置下 query-conditioned graph 平均高 1.34 个点，不能称等 token 或稳定显著。Chain 降低人工错误传播但也阻断 oracle insight；Full 相反。`5.11%` scalability claim 的参照不清，不进入 Card。核点：PDF pp.4–5、8、13 Tables/Figures 2/3。

### Limitation — `RESOLVED_BY_SOURCE`

两读共同指出 DAG 实现细节不完整：`Z^T Z` 对称、边方向定义不一致、未说明无环化；分析题集是否跨拓扑共享、训练/测试拆分未明确；只测 reasoning/math/code、固定 prompts/roles。Figure 5 A/B 标注冲突和 Algorithm 1 的 `Update G-Designer` 是来源问题，按原样记录，不用于核心事实。核点：PDF pp.2–3、13–15。

### Operator — `RESOLVED_BY_SOURCE`

Pilot 只抽取 `Query-Conditioned Sparse/Dense Topology Fusion`：按 query 在稀疏/稠密通信先验之间融合边 mask，再用任务 reward 学习图。CAPE/TCTE 作为其动机/评测分析，不另拆 Card。

### Failure — `RESOLVED_BY_SOURCE`

Pilot 只抽取 `Dense Error Amplification / Sparse Insight Blocking`：在本文人工干预协议中，高连通提高错误扩散敏感性，过稀又妨碍正确 insight；明确标注 oracle、模型、题集和 topology 条件，不写成自然传播定律。

## 3. 未解决项与准入裁决

- `UNRESOLVED`：无阻断项；上述复现细节不足限制精确实现，但不改变来源报告的窄干预/结果。
- Open limits：图定向/无环化、优化/测试拆分、随机图重复、5.11% 参照和逐消息中介均未解决。
- CORE disposition：`ACCEPT`。提供 multi-agent 通信 Operator 与重要双侧 Failure，但 Claim 必须保守。
- Task 5 计划：1 个 Operator Card、1 个 Failure Card、1 个 Paper Card；先建立 Evidence。
