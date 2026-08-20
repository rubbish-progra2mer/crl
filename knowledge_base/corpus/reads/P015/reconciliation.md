# P015 三读 reconciliation

## 1. 来源与全部尝试绑定

- PDF：`knowledge_base/staging/papers/P015_should_we_be_going_mad.pdf`；SHA-256：`8d0330933f495a3804842e8c8b0f778d8529fefeaf8d2a2dbf89d94f97bd0e70`。
- 主 Codex 首读：`knowledge_base/pilot/reads/P015/read_1.md`；SHA-256：`416d6c3b08b8d933bcde74bb72009e3d2e59438a375338458d41d29556ac4d91`。
- 二读 `r2-20260719-p015-a1`：`ACCEPTED`。Invocation：`knowledge_base/pilot/reads/P015/read_2_attempts/r2-20260719-p015-a1/invocation.md`，SHA-256：`a70ba1f00048838306483240e3afe2b87a7ba125af47f57531cd87ffd1e7f4df`；Report：`knowledge_base/pilot/reads/P015/read_2_attempts/r2-20260719-p015-a1/report.md`，SHA-256：`627a0ae5973a3e9e271f69661da106e9512c3fda9e1e70c9f6729eb363ba2c2b`。
- 第三读 `r3-20260719-p015-a1`：`ACCEPTED`；触发原因是该论文是 multi-agent 强负向/效率 baseline，且主结果表与附录表存在潜在冲突。Invocation：`knowledge_base/pilot/reads/P015/read_3_attempts/r3-20260719-p015-a1/invocation.md`，SHA-256：`4d8e665ef678d2f2c2277c2b9ad07d7d04898f95efea0475c5a1080ee737ffc9`；Report：`knowledge_base/pilot/reads/P015/read_3_attempts/r3-20260719-p015-a1/report.md`，SHA-256：`40d96b00ff2398ceb590ff09775cea856554959d170601debc77fef3f062bc04`。
- 其他 attempts：无。两名独立读者均为 `procedural_blinding`；通用 PDF 技能说明的额外读取已披露，未包含 Pilot 研究内容。

## 2. 逐项裁决

### Changed computation — `AGREE`

论文系统比较的是推理时多调用的信息交换与聚合，而非训练或权重更新。新增干预是在 debate 开始前向 Multi-Persona 的 devil system prompt 写入目标 agreement intensity，改变代理的反驳倾向，再由 angel/devil/judge 多轮交互输出答案。核点：PDF pp.2、6–7、20–21，§2–3、Figures 5–6、Appendix A.5–A.6。

### Baseline — `AGREE WITH INTERNAL CONFLICT`

没有跨数据集统一最强协议；Medprompt、Self-Consistency、ER 是重要非辩论对照，原始 Multi-Persona 是 agreement modulation 的最接近控制。Table 2/Figures 1、10 与 Appendix Table 3 的若干 MedQA 数字明显不一致，例如 Single Agent 约 0.60/0.76，原文没有解释子集、模型或版本差异。Pilot 不用冲突数字作定量 Card 事实，仅记录“结果口径冲突”。

### 公平性与预算 — `AGREE`

不同协议同时改变代理数、轮数、上下文共享、摘要、聚合、prompt、few-shot 与采样参数；API calls、tokens、成本和时间也不同。Table 2 逐数据集取最好配置，具有事后配置选择成分；K-fold 分析更接近外推但缺少折叠、方差和显著性细节。不能把 MAD 的相对表现只归因于“多代理交互”。核点：PDF pp.3–5、12–18，Table 2、Figures 1–3/10–16、Table 3。

### 结果与边界 — `AGREE`

原始 MAD 不可靠地优于强非辩论策略，更多调用/成本不保证更高准确率；Multi-Persona 的 devil 可能把正确首答推向错误。Agreement 操作随数据集和 backbone 改变：MedQA/PubMedQA 偏高一致，CIAR 方向相反，ChatEval 几乎不响应，GPT-3.5 设置不能良好迁移到 Mixtral。范围主要是多选 QA；开放工具型协作、长期记忆和对抗安全没有被验证。核点：PDF pp.4–9，Figures 3–9。

### Operator — `AGREE`

Pilot 抽取 `Agreement-Prior Modulation`：在多代理交互开始前改变某角色被提示的 agreement prior，并观察它如何改变首轮一致与最终决策。该 Operator 只能作为受 prompt/backbone/task 约束的机制，不是通用“辩论增强”。

### Failure — `AGREE`

Pilot 抽取 `Contrarian Agent Corrupts Correct Initial Answer` 与 `Debate Protocol Non-Dominance Under Cost`。前者由 Figure 4 的过程结果支持；后者是跨数据集/协议和成本结果的窄结论。Appendix SPP prompt 中 `12 + 12 = 12` 的错误作为 source-quality 警告，不上升为方法级 Failure。

## 3. 未解决项与准入裁决

- `UNRESOLVED`：Table 2/Figures 与 Table 3 的结果口径；376 题调参子集是否与 full MedQA 重叠；精确模型快照、随机种子/CI；agreement intensity 的形式化事件定义。
- 冲突禁止使用相关数值作定量 Claim，但不阻断论文作为 multi-agent 负向知识与强比较来源。
- CORE disposition：`ACCEPT`。该论文是 Pilot 的关键负向/效率 baseline，第三读已完成；不据此扩展为所有论文第三读。

