# PLAN_05 Operator Card 独立核源报告 A

- canonical task identity：`/root/plan05_card_source_audit_a`
- 报告生成时间：`2026-07-19T23:44:15+08:00`
- 审计性质：PLAN_05 Card 独立核源；不是 CRL 科研三审，不评价 Candidate。
- 审计范围：仅核对指定 8 张 Operator Card 的 metadata、Evidence、admitted PDF 原文与 SHA-256。
- 结论汇总：`PASS` 5 张；`REVISION_REQUIRED` 3 张。

## 核验方法与完整性结果

1. 读取 Card metadata，取得 `paper_id`、`evidence_ids`、`source_refs`。
2. 从 `knowledge_base/corpus/evidence.json` 读取对应 Evidence，并在 `knowledge.plan05_scratch.sqlite` 中机械核对 passage ID、页码、passage SHA、quote 坐标与 `source_content`。
3. 对照 `manifest.json` 和 admitted PDF 实际字节计算 SHA-256；8 份 PDF 均与 Card、Evidence、manifest 三方一致。
4. 直接阅读原始 PDF 的相关页和上下文；对包含图、算法或双栏方法说明的关键页进行了原页视觉核查。
5. 判断 Card 是否把作者直接报告的事实、Codex 综合和假设分开，以及 Evidence 是否足以回溯 intervention identity、before/after computation、输入输出时点和风险边界。

8 条 Evidence 的 passage、quote 与 PDF 字节链均为 `PASS`。以下 `REVISION_REQUIRED` 均是科研语义或 provenance 问题，不是文件完整性问题。

## 逐卡结论

### 1. `operator-outcome-trained-execution-state-planner.md`

- 结论：`PASS`
- Card SHA-256：`6a463a6961ca0e09daa88ba15eee39c3499f5631bc8fc6d25ae19e4416695c51`
- Evidence：`ev-p021-operator-core`；证据等级：B（单篇强相关论文直接报告）。
- PDF：`papers/P021_agentflow.pdf`；SHA-256：`33e04a3fa3ac197e69c2fffd5f53a274c80872a515a6269bc98ae7d4105f7095`
- 核源判断：原文第 5–6 页明确把 Action Planner 定义为唯一可训练策略；状态由 query、tool set、显式 memory 构成并随 executor/verifier 反馈演化；训练在当前策略产生的完整系统 rollout 内进行，并以最终结果奖励更新 planner。Card 的 intervention identity、训练前后变化、每步动作时点和终局奖励时点均与原文一致。
- 边界判断：全轨迹广播同一奖励、LLM-as-judge 和比较预算归因风险均标成 `[CODEX_SYNTHESIS]` 或 `[CODEX_HYPOTHESIS]`，没有冒充作者事实。

### 2. `operator-higher-order-message-exposure.md`

- 结论：`PASS`
- Card SHA-256：`8aad6edebdd91275bfa863bc554c2c9d695b8c3c69f0eb58ca31189b2351fc4a`
- Evidence：`ev-p022-operator-core`；证据等级：B（作者方法图为直接证据，抽取文本布局较噪，已回查同页正文）。
- PDF：`papers/P022_moc.pdf`；SHA-256：`ba1d15b954937e17f660891e1f3b52bde6d19aa7d4f4759ca3ca98703975ea83`
- 核源判断：原文第 4–6 页明确对比“仅直接上游邻居”与“按 K-hop 收集多跳祖先原始响应”，按全局拓扑顺序线性化，并在目标 Agent 响应前按 message-count budget 做语义—拓扑合并。Card 对 intervention、输入、输出和时点的表述准确。
- 边界判断：额外蒸馏调用、语义漂移/信息损失与性能饱和均能在原文方法讨论中找到直接边界；Card 将预测性表述正确标为 Codex 假设。

### 3. `operator-cascaded-multiagent-meta-routing.md`

- 结论：`REVISION_REQUIRED`
- Card SHA-256：`17af3add59018dcf8f92cf249901c8d8561dca78699b94f74d257094dae820e2`
- Evidence：`ev-p023-operator-core`；证据等级：B（仅直接支持 collaboration mode、role 和统一 MAS routing）；对完整 cascade、agent count、heterogeneous LLM routing 的当前引用覆盖不足。
- PDF：`papers/P023_masrouter.pdf`；SHA-256：`1bf45eaa68515ae2a6d3de2e2240ac321fef37a46ba831718aacee52bb12f457`
- 核源判断：Card 的主要机制本身与原文第 1、4–6 页一致：先确定协作模式和 Agent 数量，再分配有序角色，最后路由异构 LLM，并以 query-conditioned controller 在主推理 rollout 前配置 MAS。
- 问题 1：当前 Evidence 精确截取只覆盖 collaboration mode、agent roles 和“unified routing framework”，没有覆盖 Card 中的 agent scale、heterogeneous model routing 与 cascaded controller。原 PDF 支持这些内容，但当前 Card→Evidence 引用链不完整。
- 问题 2：`incompletely reproducible splits` 不是该 Evidence 或 admitted PDF 中可直接复核的主张；它来自 PDF 之外的代码级审计时，不能只以该 PDF 作为 `source_ref`。
- 最小修订：新增一条来自第 1 页摘要或第 4–6 页方法段的 Operator Evidence，覆盖 collaboration determiner、agent count、role allocator、LLM router 和 cascade；对 split 风险二选一：删除该短语，或加入可追溯的官方代码版本/审计来源。其余 Card 正文无需重写。

### 4. `operator-counterfactual-role-contribution-audit.md`

- 结论：`REVISION_REQUIRED`
- Card SHA-256：`d5871a1f347bb1554461ac9176b8997c3faa85953b59d65a591e92a06d0ff180`
- Evidence：`ev-p025-failure-core`；该 Evidence 对“lazy agent 现象”为 B 级直接证据，但对当前 Operator identity 为 D/insufficient-evidence。
- PDF：`papers/P025_lazy_agents_deliberation.pdf`；SHA-256：`5447d5ad949dd4b0061c36b80e395c97c1dc7534960576660096a2420408fc00`
- 核源判断：Card 将论文方法实质性改写成“替换或移除一个 role，观察 team outcome，再分配 role-level contribution”。原文实际方法不是这个计算：它把轨迹展开为 step 序列，对某一步做 masked-history 比较，计算下一步输出的 log-probability 差，并在不同 rollout 中对语义相似步骤的 one-step causal influence 求平均；训练时还移除 turn normalization，并把 outcome advantage、causal influence 和 restart reward 组合成 step-level advantage。
- 直接冲突：论文的 mask/removal 对象是历史中的具体 step，不是完整 role；被比较的是下一步分布，不是替换/删除 role 后的 team terminal outcome。当前 Card 的 intervention identity、输入输出和时点因此不成立。
- 最小修订：将卡片重命名或至少窄化为“grouped masked-history step-influence credit”；把 intervention target 改为 step/turn credit，把 before/after 改为移除 `1/T` normalization 并加入 grouped one-step causal influence；输入改为 trajectory steps、语义分组和 full/masked history，输出改为 step-level influence/advantage，时点改为 online RL credit computation。新增第 5–7 页方法 Evidence；现有 failure Evidence 可保留为动机，不能单独支撑 Operator。

### 5. `operator-verified-single-branch-repair.md`

- 结论：`PASS`
- Card SHA-256：`09a3b73ecc6e89594316d8a8c00bd81a7528c7b8ad093e48fd3cb76c845c0f9b`
- Evidence：`ev-p027-operator-core`；证据等级：B。
- PDF：`papers/P027_critical_step_optimization.pdf`；SHA-256：`2278960362823372029670a209ba7f9ce969485cd47f831c0406bb6016c1f288`
- 核源判断：原文第 3–5 页直接支持：从失败轨迹定位候选 critical step，用 expert alternative 替换单个动作，后续 suffix 由 policy 自己 rollout，只有 ground-truth outcome 从失败翻转为成功时才构造局部 preference pair，随后做 DPO。Card 的 intervention、输入输出与时点准确。
- 边界判断：强 teacher、PRM 与 outcome verifier 是额外信息；单条成功分支不证明唯一因果责任。Card 已把这些作为 Codex 综合风险而非作者事实。

### 6. `operator-learned-memory-crud-control.md`

- 结论：`PASS`
- Card SHA-256：`a68f33db2495bca9f2718493931b153fc5f4ea24a146f2541f4b582a73df8fc7`
- Evidence：`ev-p028-operator-core`；证据等级：B。
- PDF：`papers/P028_memory_r1.pdf`；SHA-256：`c206af4e792e9550f2aaec8a6c4d9b141d1ddcb587e781d7866870c8f3e4dd4f`
- 核源判断：原文第 1、3–5 页明确区分 Memory Manager 与 Answer Agent：前者在写入侧以 `ADD/UPDATE/DELETE/NOOP` 改变 memory bank，后者在回答前对检索到的 memories 做 distillation、筛选和推理；两者分别接受 outcome-driven PPO/GRPO。Card 对两个时点和两个输出的概括成立。
- 边界判断：manager 与 answer agent 联合带来的归因耦合、训练资产/计算和上下文描述冲突均被标为 Codex 综合，没有伪装为作者已证明的机制事实。

### 7. `operator-write-side-state-adjudication.md`

- 结论：`REVISION_REQUIRED`
- Card SHA-256：`13ee316cd43a0939623c8c71c84a3d74e1f1f7467e13d02b8793d853bf4b434b`
- Evidence：`ev-p030-failure-core`；该 Evidence 对“识别旧状态不等于在下游应用更新状态”为 B 级直接证据，但不能支撑 CUPMEM Operator。
- PDF：`papers/P030_stale_memory.pdf`；SHA-256：`388f71f1eb952e7d7e7b19c2f25bfc744c47efa8ee00a548093b949432495109`
- 核源判断：Card 的 Operator 正文本身与原文第 9 页 Section 5 基本一致：CUPMEM 在写入时对旧状态执行 `KEEP/STALE/REPLACE/UNKNOWN` adjudication，以 topology-triggered search 扩展受影响槽位，并让 query-time readout 仅受授权状态约束。
- 问题：Card metadata 只引用 failure Evidence；该片段位于实验诊断，内容仅说明 retrieval/recognition 与 downstream application 之间的 gap，没有出现 write-side adjudication、typed state、propagation search 或 constrained readout。因此当前 Evidence ledger 所称“establish the intervention identity”不成立。
- 最小修订：从第 9 页 Section 5 新增一条 Operator Evidence，覆盖 write-side adjudication 和 constrained readout，并把它加入 Card metadata/Evidence ledger；保留 `ev-p030-failure-core` 作为问题动机即可。Card 主体无需实质重写。

### 8. `operator-tool-grounded-critique.md`

- 结论：`PASS`
- Card SHA-256：`7375e1dfce68c9434b097352cc56a9f93713fb045eef762639084aabc60ed503`
- Evidence：`ev-p032-operator-core`；证据等级：B。
- PDF：`papers/P032_critic.pdf`；SHA-256：`30a3161dbbb9531528bf410bd1df84eeb9ada8151f614789ae80ca86b7b32c7e`
- 核源判断：原文第 3–5 页和 Algorithm 1 直接支持“先生成→调用任务相关工具验证→把 critique 与原输出一起用于修订→按停止条件迭代”的 changed computation。Card 的输入、输出和发生时点准确。
- 边界判断：原文实验包含 `CRITIC w/o Tool`、oracle 变体和个别负增益，足以支持工具信息量、非单调修订和 oracle 不可部署等边界；预测项和额外混杂均明确标为 Codex 判断。

## 实际读取文件

### 规约与技能

- `D:/Desktop/crl_judge/crl_agent_v3/AGENTS.md`
- `D:/Desktop/crl_judge/crl_agent_v3/CRL.md`
- `D:/Desktop/crl_judge/crl_agent_v3/CRL_ENVIRONMENT.md`
- `C:/Users/g/.codex/skills/evidence-quality-gate/SKILL.md`
- `C:/Users/g/.codex/skills/evidence-quality-gate/references/rules.md`
- `C:/Users/g/.codex/skills/evidence-quality-gate/references/output_schema.md`
- `C:/Users/g/.codex/skills/evidence-quality-gate/references/checklists.md`
- `C:/Users/g/.codex/skills/encoding-safe-edit/SKILL.md`
- `C:/Users/g/.codex/skills/pdf/SKILL.md`

### Card、Evidence 与派生核对源

- 上述 8 张 `knowledge_base/cards/operator/*.md`
- `knowledge_base/corpus/evidence.json`，SHA-256：`14595b5d45f8861752e6ef188505e761ca87f16885becfb46bfbd2e1667ea257`
- `knowledge_base/corpus/manifest.json`，SHA-256：`44b2ee67cf7b7bea8394d83f6142e3aa34fb65eee812813b0fe541c90a62e971`
- `knowledge_base/knowledge.plan05_scratch.sqlite`，仅用于机械核对 8 条 passage/quote 链；SHA-256：`855c0e9aa11c666e61c0b1cefa04e232aa0cd93644ef4814495a85e604fdf3e5`

### 原始 PDF 阅读范围

- `P021_agentflow.pdf`：重点第 5–7 页；视觉核查第 5 页。
- `P022_moc.pdf`：重点第 4–7 页；视觉核查第 4 页。
- `P023_masrouter.pdf`：重点第 1、3–6 页，并对全文做与 routing/split/oracle 相关的定向定位；视觉核查第 4 页。
- `P025_lazy_agents_deliberation.pdf`：重点第 2–7、9、18 页相关段落，并对全文做 step masking/counterfactual/credit 定向定位；视觉核查第 6 页。
- `P027_critical_step_optimization.pdf`：重点第 3–6 页；视觉核查第 4 页。
- `P028_memory_r1.pdf`：重点第 1、3–6 页；视觉核查第 4 页。
- `P030_stale_memory.pdf`：重点第 1、3–10、14–15 页；视觉核查第 9 页。
- `P032_critic.pdf`：重点第 1、3–7 页，并对全文做 oracle/w-o-tool/harm/stopping 定向定位；视觉核查第 4 页。

## 未读与未执行范围

- 未读取任何 blind query、blind judgment 或 blind evaluator 输出。
- 未读取或审计 A 组之外的 Card 和论文。
- 未联网扩展文献，也未引入外部论文。
- 未创建或评价 Candidate，未执行 novelty/prior-work 审查、Reviewer 三审、Commissioning 或实验。
- 未修改 8 张 Card、Evidence、manifest、PDF、数据库或其他项目文件；仅创建本报告。

