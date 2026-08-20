# P025 Codex 首读：From Lazy Agents to Deliberation

- 状态：`DRAFT_BEFORE_SECOND_READ`
- PDF：`knowledge_base/staging/papers/P025_lazy_agents_deliberation.pdf`
- PDF SHA-256：`5447d5ad949dd4b0061c36b80e395c97c1dc7534960576660096a2420408fc00`
- 读取范围：lazy-agent 问题与 ReMA 背景（pp.1–4）、归一化偏差、causal influence、restart reward（pp.5–7）、结果/消融（pp.8–10）、训练细节与负结果（pp.18–19, 24–25）。

## Changed computation

- [AUTHOR_FACT] ReMA 让 Meta-thinking 与 Reasoning 两角色交替、共享模型参数，并把最终结果优势给各轮；论文观察到 Reasoning 逐渐只复制/总结甚至空答，系统退化为单 Agent（pp.1–4）。
- [AUTHOR_FACT] Dr. MAMR 去掉按轨迹轮数的 `1/T` 归一化，按语义相似步骤跨 rollout 聚合“移除该步骤后下一步 log probability 的变化”，并把该 causal signal 加入 step advantage（pp.5–7）。
- [AUTHOR_FACT] 另用 `<restart>` 允许 Reasoning 丢弃先前自己的输出；奖励比较屏蔽旧 Reasoning 后最终正确输出的概率变化（p.7）。
- [CODEX_SYNTHESIS] 对 CRL 主线最重要的是前两项：系统级成功可能掩盖某角色完全不贡献；长度/轮数归一化会意外改变策略偏好；仅看输出文本或最终分数无法判断角色必要性。

## Baseline、公平性与结果

- 主要在 DeepScaleR 训练，Qwen2.5 3B/7B/14B，比较单 Agent GRPO、VRP(CoT)、ReMA 与完整方法；七个数学 benchmark 上完整方法平均优于 ReMA 与 GRPO（pp.7–9）。
- 7B 平均：GRPO 55.08、ReMA 51.97、Dr. MAMR 58.43；14B 为 58.05、57.24、62.49（p.8 Table 1）。这支持“naive multi-agent RL 可差于单 Agent”的负向知识。
- 消融分别移除 normalization debias、causal influence、restart，四项 benchmark 均下降（p.9 Table 2），但三组件共同改变训练，单项边际并不等于完整机制因果独立。
- causal influence 基于对 attention/history 的反事实遮蔽及模型自身概率；它不是外部任务贡献的直接测量，语义聚类阈值 0.9 与 0.5B embedding 模型也会改变归组（pp.4, 6, 18）。
- 训练使用 batch 128、每步 128 rollouts；restart 还需 GPT-4o 合成噪声轨迹做 SFT（pp.18–19）。成本显著，不能直接作为个人本机轻量 implement。

## 失败边界与未否定项

- [AUTHOR_FACT] 只加反 lazy prompt 仅小幅修复；ReMA 的 Reasoning influence 随训练趋近零，训练后期 reward 甚至崩到零（pp.4, 9）。
- [AUTHOR_FACT] 加 process reward model 的 ReMA 约 30 步即崩溃，作者归因于 reward hacking（pp.24–25）。这说明“增加一个过程分数”不是稳健修复。
- [CODEX_SYNTHESIS] 去 `1/T` 也可能反向偏向长轨迹；论文主张消除短轨迹结构偏差，不等于获得长度中性的目标。必须同时测实际轮数、token 与角色边际贡献。
- [CODEX_SYNTHESIS] restart 属于多轮推理中的历史重置机制，接近本项目明确排除的“执行恢复”方向；本库可保存为边界证据，但不把它升级为核心研究方向或独立 Operator。
- 未否定：更简单的 frozen-role ablation、角色输出替换、单 Agent 等预算对照可能识别 lazy role；causal influence 不是唯一方案。

## Evidence 草案

| Evidence ID | kind | section / page | locator | source range（短引） | Codex note |
|---|---|---|---|---|---|
| P025-E01 | failure | §4, p.4 | Figure 2 | “reasoning agent ... contributes substantially less” | [AUTHOR_FACT] 角色贡献塌缩的实证。 |
| P025-E02 | mechanism | §5.1, p.5 | Theorem 1 | “bias toward actions that reduce the number of turns” | [AUTHOR_EXPLANATION] 作者对 `1/T` 偏差的理论解释。 |
| P025-E03 | mechanism | §5.2, p.6 | Eq.4–5 | “average across its group” | [AUTHOR_FACT] 跨相似步骤聚合影响估计。 |
| P025-E04 | result | §6.2, p.8 | Table 1 | “ReMA consistently underperforms ... single-agent GRPO” | [AUTHOR_FACT] naive MAS training 的负结果。 |
| P025-E05 | negative_result | Appendix G, pp.24–25 | Eq.21, Figure 6 | “process reward ... fails to mitigate” | [AUTHOR_FACT] PRM 加法在该设置下训练崩溃。 |

## Card 草案（不进入正式 Cards）

### Paper source role — `DRAFT_BEFORE_SECOND_READ`

Multi-agent learning/credit assignment 的高价值 Failure 来源；Operator 只保留“角色反事实贡献审计”，restart 不作为本库核心方向。

### Operator — `DRAFT_BEFORE_SECOND_READ`

- 名称：`Counterfactual Role-Contribution Audit`
- Baseline：只用终局任务分数判断多 Agent 系统是否协作成功。
- Changed computation：逐角色/步骤遮蔽或替换其历史，比较后续分布与任务结果，并跨语义相似 rollout 聚合，检查角色是否真实改变计算。
- 前提：反事实编辑不引入不自然输入；贡献指标与外部任务结果联合报告；不由内部分数自动决定科研结论。
- retrieval vocabulary：lazy agent, causal influence, role contribution, multi-turn credit assignment, collaboration collapse。

### Failure — `DRAFT_BEFORE_SECOND_READ`

- 名称：`Nominal Multi-Agent, Effective Single-Agent Collapse`
- 条件：共享终局奖励、角色共享权重或强依赖、没有单角色边际贡献约束。
- 现象：一个角色输出复制/空答且 influence 下降，另一个角色承担全部推理；系统名义多 Agent 但不再有计算差异。
- 替代解释：角色 prompt、基础模型 instruction-following 或反事实 influence 估计偏差也可造成观测差距。
- 未否定：多 Agent 在更强角色分工、独立参数或外部验证下仍可能有效。

## 首读裁决

`KEEP_FOR_SECOND_READ`。它直接支持 Failure-first 检索；二读需攻击 causal influence 的有效性与长度偏差的反向风险。
