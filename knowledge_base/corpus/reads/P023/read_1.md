# P023 Codex 首读：MasRouter

- 状态：`DRAFT_BEFORE_SECOND_READ`
- PDF：`knowledge_base/staging/papers/P023_masrouter.pdf`
- PDF SHA-256：`1bf45eaa68515ae2a6d3de2e2240ac321fef37a46ba831718aacee52bb12f457`
- 读取范围：问题定义与搜索空间（pp.1–4）、三级路由与优化（pp.4–6）、主结果/消融/限制（pp.7–9）、成本表与算法细节（pp.13, 19–20）。

## Changed computation

- [AUTHOR_FACT] MasRouter 不只为一个 Agent 选模型，而是按 query 依次选择协作模式与 Agent 数、逐个分配相互依赖的角色，再为各角色从异构 LLM pool 分配模型（pp.2–5）。
- [AUTHOR_FACT] 三个控制器共享 query/已选结构/角色语义，以 policy gradient 联合优化正确概率减去 λ×成本；Agent 数由可学习 query complexity 映射并受最大值 γ 限制（pp.4–6）。
- [CODEX_SYNTHESIS] 核心 Operator 是“先决定计算结构，再分配能力”，而不是把所有问题送进固定的最大 MAS。它适合用作成本受限 Agent 架构选择的机制祖先。

## Baseline、公平性与结果

- 比较覆盖单 Agent prompting、固定/动态 MAS、单 Agent routers；LLM pool 包含 gpt-4o-mini、Claude 3.5 Haiku、Gemini 1.5 Flash、Llama-3.1-70B，temperature=1（p.6）。
- MasRouter 五项平均 85.93，高于 RouterDC 82.42；但与动态 MAS 的比较同时改变模型异构性、结构选择、角色和成本目标，不能把差值分配给某一子模块（p.7）。
- 消融以随机选择替代三个路由器：去掉 LLM router 的性能下降最大；去掉成本项性能近似但 GSM8K/MATH 成本分别增加 54.09%/41.62%（p.8 Table 3）。
- γ 从 2 增至 6 提升 HumanEval，6→10 只有边际提升且每 query 成本约增至 1.5 倍；λ 提高降低 17.78% 开销但约损失 1.3 点（p.8）。
- 成本用当时商业 API 价格计；跨模型价格与服务版本会变化，且训练/推理成本表不是硬件归一的计算量。对 CRL 应保留 token/call 口径，不继承美元数值作为稳定事实。

## 失败边界与未否定项

- [AUTHOR_FACT] 方法假设模型池成员可靠；被投毒模型可能作为“bad apple”误导整个 MAS，论文未解决鲁棒路由（p.9）。
- [CODEX_SYNTHESIS] 训练监督使用 benchmark oracle answer，路由器可能学习数据集/题型捷径而非可迁移的任务计算需求；“inductive”只验证加入一个新模型后的选择与指标变化。
- [CODEX_SYNTHESIS] 三级级联有早期锁定：协作模式错误会约束后续角色与模型，主文未给 oracle/per-stage upper bound，无法定位剩余瓶颈。
- 未否定：简单的 query difficulty gate、只做 LLM routing 或固定小型结构可能在小搜索空间中同样有效；随机替代不是最强独立模块 baseline。

## Evidence 草案

| Evidence ID | kind | section / page | locator | source range（短引） | Codex note |
|---|---|---|---|---|---|
| P023-E01 | mechanism | §3.2, pp.3–4 | Definition 2, Eq.3 | “balance performance and cost” | [AUTHOR_FACT] MAS routing 的正式目标。 |
| P023-E02 | mechanism | §4, pp.4–5 | Eq.5–11 | “collaboration mode determiner, role allocator, and agent LLM router” | [AUTHOR_FACT] 三级级联选择。 |
| P023-E03 | result | §5.5, p.8 | Table 3 | “MasRouter w/o C(·)” | [AUTHOR_FACT] 去成本目标使成本显著增加而准确率接近。 |
| P023-E04 | saturation | §5.5, p.8 | Figure 5 | “further increases from 6 to 10 yield only marginal” | [AUTHOR_FACT] Agent 数扩张存在收益饱和。 |
| P023-E05 | limitation | §6, p.9 | Limitations | “some LLMs may be attacked or poisoned” | [AUTHOR_FACT] 路由器可靠模型池假设。 |

## Card 草案（不进入正式 Cards）

### Paper source role — `DRAFT_BEFORE_SECOND_READ`

成本约束、多 Agent 动态构型与能力路由的来源；对“固定最大 Agent 队伍”提供直接负向证据。

### Operator — `DRAFT_BEFORE_SECOND_READ`

- 名称：`Query-Conditioned Compute-Structure Routing`
- Baseline：所有 query 使用同一协作拓扑、角色和模型。
- Changed computation：先以 query 选择协作结构/规模，再条件化地分配角色与模型，并在目标中显式计入调用成本。
- 前提：候选结构/角色/模型池有限且已知；训练 query 有可信结果；成本口径可比较。
- retrieval vocabulary：MAS routing, collaboration mode, role allocation, heterogeneous LLM routing, cost-performance frontier。

### Failure — `DRAFT_BEFORE_SECOND_READ`

- 名称：`Unpriced Agent Scaling`
- 条件：优化或设计只奖励任务分数，不惩罚 Agent 数、调用数和 token。
- 现象：系统倾向更大的 MAS；增加 Agent 超过饱和点后成本显著增长而性能仅边际变化。
- 替代解释：路由器容量、候选池质量或训练数据覆盖可能限制更多 Agent 的利用。
- 未否定：难题子集可能仍受益于更大队伍，应按 query 分配而非全局裁剪。

## 首读裁决

`KEEP_FOR_SECOND_READ`。二读需要攻击路由训练的 oracle 依赖、级联误差和成本公平性。
