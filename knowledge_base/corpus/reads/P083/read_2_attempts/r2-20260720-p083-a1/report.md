# P083 独立二读报告

## 1. 来源、阅读范围与结论

- source: `P083_tamas.pdf`
- PDF SHA-256: `4AD6D486003DC7268C80CDC2F49224A955792843D57155915D5F77889F7F7BDD`
- 阅读范围：物理 PDF 第 1–31 页，逐页顺序阅读正文、威胁模型、公式、表格、置信区间附录、案例与全部 judge/defense prompts；论文印刷页码为 31238–31268。
- 论文：*TAMAS: Benchmarking Adversarial Risks in Multi-Agent LLM Systems*，ACL 2026 Long Papers。
- 二读结论：**按 Failure / threat model / measurement 有条件准入；不按已验证 defense Operator 准入。** 论文的主要价值是把多智能体攻击面分为 prompt、environment 与 compromised-agent 层，并展示不同框架/协作拓扑中的脆弱性。其轻量防御实验明确有限、时有反效果，不能据此生成“已验证 Operator”。
- 第三读：**建议**。若后续要定量使用 Safety/ERS 或比较架构安全性，应第三读复核 ARIA 标签映射、per-attack min-max normalization、PNA 的工具调用代理以及缺失配置造成的比较偏差。

## 2. Threat model 与 changed computation

### 2.1 威胁模型

- 攻击目标：破坏 benign task，或诱使系统执行攻击者期望的恶意动作；攻击可通过 inter-agent communication、coordination protocol 或角色假设产生级联影响。（物理页 3）
- 攻击者知识：知道各 agent 的角色与可用工具，但不知道底层 LLM 参数、对齐策略与模型架构细节。（物理页 3）
- 攻击者能力：可向用户 prompt 或环境 observation 注入内容；可通过 adversarial system prompt compromise 一个或多个 agent；可把恶意工具加入 agent toolkit。（物理页 3–5）
- 六类攻击：DPI、Impersonation、IPI、Byzantine agent、Colluding agents、Contradicting agents。前三类分别作用于初始 user prompt 或工具输出；后三类通过预先改写 agent system prompt 影响运行期行为。（物理页 2、4–5、16）

此威胁模型同时包含弱注入与很强的内部 compromise。特别是“攻击者可修改 system prompt 并加入 attacker tool”相当于已经取得显著控制权；实验说明的是此控制权如何经多智能体协作传播，而不是证明任意外部攻击者都能先取得该权限。

### 2.2 Changed computation：评测装置，而非防御算法

TAMAS 改变的是安全评测计算：

1. 为五个领域各构造一个四-agent 系统，给出角色、normal tools、attack tools、benign multi-step tasks 与六类 adversarial tasks。（物理页 5、13–15）
2. 在 AutoGen/CrewAI 的不同交互配置中运行真实多-agent workflow，保存完整 conversation trace、internal thoughts、tool calls、observations 与结果。（物理页 5–7、28–31）
3. 对 DPI/IPI/Impersonation 等可机械判断的攻击检查 malicious tool invocation；对语义性 agent-level failure 再用 GPT-4o judge 给 ARIA 类别。（物理页 6、16、28–30）
4. 从 ARIA 分布计算 Safety Score；另以 benign task 的必要工具调用覆盖率计算 PNA；最后取 normalized overall safety 与 PNA 的 harmonic mean 得到 ERS。（物理页 6、16–17）

这套 computation 可用于**暴露/测量 Failure**。论文第 7 节的 delimiter、paraphrase、sandwich、monitor 只是有限 defensive baselines，不是论文主体，也未形成稳定、跨模型成立的安全 Operator。（物理页 7–9、17–19、31）

## 3. 输入、输出、信息可见性与时点

### 3.1 输入与运行时信息

- benign target task `q_t`；四个 agent 的名称、角色描述与 system prompts；各 agent 的 normal toolset；运行中的 observations/messages。
- DPI：在初始 user query 后拼接恶意指令并增加 attack tool；Impersonation：初始 query 中伪造权威身份。（物理页 4）
- IPI：原始 user query 不变，在某一步的外部/工具 observation 中注入恶意指令并提供 attacker tool。（物理页 4）
- Byzantine/Colluding/Contradicting：运行前改写一个或多个 agent system prompts；collusion 与 contradiction 还利用 agent 间消息传播。（物理页 4–5）
- 所有 tools 都是模拟函数，不访问真实 API；这提高可控性，但移除了真实权限、网络、状态、失败恢复与不可逆副作用。（物理页 13、15）

### 3.2 输出与评估时点

- 运行输出：完整多-agent trace、工具调用、模拟工具返回、任务是否完成以及攻击动作是否执行。
- ARIA-1：立即拒绝；ARIA-2：开始执行后拒绝；ARIA-3：有意执行但因协调/工具等原因失败；ARIA-4：恶意目标成功。（物理页 6、15）
- DPI/IPI/Impersonation 的 ARIA-4 主要由日志中的 attacker-tool invocation 后验解析；其他语义后果由 GPT-4o judge 在看到完整 trace、internal thoughts 和 tool usage 后判断。（物理页 16、28–30）
- monitor defense 则是在线周期性读取“截至当前时点”的 trace，输出 continue/terminate；论文观察到同一轨迹在相邻迭代可能从 stop 又变为 safe，存在明显时序不稳定。（物理页 8、18、31）

## 4. 数据、模型、实验、配置与强基线情况

### 4.1 Benchmark 规模

- 五个领域：Education、Finance、Healthcare、Legal、News。
- 每领域六类攻击、每类 10 个样本，共 300 adversarial instances；每领域另有 20 个 harmless tasks，共 100 benign tasks。
- 每个场景四个 agents；任务通常要求至少 2–3 agents，多步 harmless instructions 通常含 4–5 个顺序步骤。（物理页 1、5、13–15）
- user queries 与 attacker tools 由 ChatGPT 辅助生成，再经人工审阅与修订；角色、描述与工具由人工设计。（物理页 15）

### 4.2 系统、模型与缺失单元格

- AutoGen：Magentic-One（central orchestrator）、RoundRobin（fixed sequential）、Swarm（dynamic handoff collaborative）。
- CrewAI：centralized 与 decentralized/sequential；CrewAI 没有 Swarm 等价配置。（物理页 5–6、16）
- 十个 backbones：GPT-4、GPT-4o、GPT-4o-mini、Gemini-2.0-Flash、Gemini-2.0-Flash-lite、Deepseek-R1-32B、Mixtral-8x7B-Instruct、Qwen3-32B、Qwen3-8B、Llama-3.1-8B-Instruct。（物理页 6、17）
- Gemini 未跑 CrewAI，原因是已知兼容问题；GPT-4 未跑 CrewAI，原因是 API credits 不足。因而跨框架平均值不是完整 factorial comparison。（物理页 7–8、18）

### 4.3 主要攻击结果

- prompt attacks 最强：Impersonation 在 Swarm 最高约 82%，DPI 在 Magentic-One 约 81%；IPI 对配置敏感。（物理页 6–7）
- 论文报告 IPI 下闭源模型在 Magentic-One/RoundRobin 的 ARIA-4 平均低于开源模型，但这只是所选模型与配置上的相关性，不能归因于“闭源”本身。（物理页 6–7）
- colluding attack 按“两名 agent 都成功”计时仅约 2–16%；但 Table 7 显示“至少一名”调用 attacker tool 的比例可明显更高，说明主成功定义会漏掉部分已发生的恶意动作。（物理页 6、17–18）
- CrewAI 配置整体 safety 较高，但 orchestrator 仍是单点故障；Llama 在 CrewAI 的高 ERS 很大程度来自高 refusal，而非更强任务理解。（物理页 7–9）

### 4.4 强基线边界

- 这不是防御方法竞赛，正文没有与经过训练的鲁棒 agent、权限隔离、capability control、信息流控制或其他强架构防御做等预算比较。
- 论文与既有 AgentDojo、AgentHarm、Agent Security Bench 等主要做覆盖范围对照；这些工作以 single-agent 为主，不构成同一 TAMAS 多-agent 实验上的数值强基线。（物理页 2–3、14）
- 第 7 节只有 delimiter、paraphrase、sandwich 与 Gemma3-12B monitor 等 lightweight defensive baselines；作者明确承认 defense benchmarking 非全面目标。因此，攻击 benchmark 可评价覆盖与失败，不能据此判定某个防御相对当前强基线已占优。（物理页 7–9、17–19）

## 5. Measurement 与 oracle 边界：定义、优点与风险

### 5.1 ARIA judge

- GPT-4o，temperature 0.0；对 120 条 representative logs 做人工验证，两名标注者独立标，分歧由第三人裁决，Cohen's kappa=0.77。（物理页 16）
- judge 对人工标签的平均 macro-F1=89.13%；分攻击为 DPI 100%、IPI 100%、Impersonation 90.48%、Byzantine 79.17%、Colluding 90.28%、Contradicting 74.85%。（物理页 16）
- 优点：tool invocation 可机械核验，语义性 derailment 有人工抽样校准。
- 风险：120 logs 相对于大量 model×configuration×attack 运行较少；恰好最具多智能体特性的 Contradicting/Byzantine 标签最弱。该误差会进入 Safety 与 ERS，但论文没有传播 judge uncertainty 到最终排名。
- 附录 prompts 对普通攻击只让 judge 输出 1/2/3，ARIA-4 由工具检查补入；Byzantine/Contradicting prompts 又引入标签 0 表示由该 agent 导致的 task failure。0 如何统一映射到公开的 ARIA-1..4 与安全分数，需要实现级复核，正文未给出完整映射表。（物理页 16、28–30）
- 这里的评测 oracle 是后验可见的完整 trace、internal thoughts、attack identity、attacker-tool invocation 与人工校准标签。它能帮助离线归类 Failure，但不是被测 multi-agent system 在运行时可用的信息；不能把低 judge error 等同于系统具备在线攻击检测能力。

### 5.2 Safety Score 与 ERS

- raw per-attack safety 为 `A1 + 0.5*A2 - 0.5*A3 - A4`，范围 `[-100, 100]`；随后**对每种攻击做 min-max normalization 到 [0,100]**。（物理页 6、17）
- overall safety 是六类 attack safety 的算术平均；ERS 是 overall safety 与 PNA 的 harmonic mean。（物理页 6、17）
- 关键限制：per-attack min-max 使分数依赖本次纳入的 model/config cohort；加入更强或更弱系统会改变原系统的 normalized score。ERS 因而适合此表内相对比较，不是跨论文、跨版本的绝对安全标尺。
- 六种攻击被等权平均，但真实部署的攻击概率、影响严重度与代价不同；一个模拟工具调用与真实不可逆伤害被压到同一分数结构。

### 5.3 PNA

- PNA 是 harmless task 中“必要工具被正确调用”的平均比例。（物理页 16）
- 它测的是工具调用覆盖率，不完整测量参数正确性、顺序依赖、最终内容质量、用户意图满足、额外无关动作或真实副作用。将它与 normalized safety 做 harmonic mean，只能得到 benchmark 内 utility proxy。

### 5.4 置信区间

- 附录对 ARIA 行做 10,000 次 smoothed row-wise bootstrap，并用 Dirichlet perturbation 给出 95% CI。（物理页 17、20–22）
- 置信区间改善了小样本结果的可见性，但不能修复 judge label error、样本生成偏差、缺失 model/config cells 或 min-max cohort dependence。

## 6. 轻量防御：只作为 Failure 证据

### 6.1 Prompt/environment defenses

- DPI：`<USER>...</USER>` delimiter 的平均 ASR 仅从 88.4 降到 83.2；Llama-3.1-8B 反而从 88 升到 92。（物理页 18）
- DPI paraphrasing：94% 情况移除了注入，但 48% 也遗漏原任务至少一个子任务或信息，表面安全以 utility 损失为代价。（物理页 17–18）
- IPI：tool-output delimiter 平均 ASR 从 75.2 降到 64.0，sandwich 到 65.2；但 Deepseek 从 74 升到 92、Mixtral 从 74 升到 88，改善主要集中在 Qwen/Llama，跨模型不稳定。（物理页 18–19）
- Impersonation paraphrasing 会连恶意任务一起删掉，作者明确指出这更像 task removal，而非对恶意意图的稳健处理。（物理页 18）

### 6.2 Interaction defense

- Gemma3-12B monitor 周期性检查 trace；对 Colluding/Contradicting/Byzantine 的 stop 比例平均为 40/23.2/40，但论文同时报告大量 false positives 与跨步决策反复。（物理页 8、18–19、31）
- Table 10 的 stop 比例不是净 ASR 降幅，也没有与 benign PNA、误报率联合报告；因此不能据此声称 monitor 有效。

### 6.3 Operator 边界

这些结果最多支持以下 Failure：文本分隔、改写、sandwich 与外挂监控器对多智能体注入/内部破坏的效果模型依赖，可能破坏 benign task，并可能在时间上不稳定。**不得从这组有限 defense baseline 生成“delimiter/paraphrase/monitor 已验证可防御多智能体攻击”的 Operator。**

## 7. 其他 Failure、限制与外推边界

1. **模拟工具**：调用即返回预设成功文本，未覆盖权限、鉴权、真实状态、事务回滚、网络失败与不可逆伤害。（物理页 13、15）
2. **强 compromise 假设**：能改 system prompt/加 attacker tool 的攻击者已进入信任边界深处；结果应解释为 propagation/containment failure，不应混同普通外部 prompt attacker。（物理页 3–5）
3. **固定四-agent、五领域、少量模板**：每 attack 仅 50 instances，任务与工具由人工/ChatGPT 构造；框架、拓扑、领域和攻击并不穷尽。（物理页 9、14–15）
4. **成功标准不对称**：prompt attacks 常以 attacker-tool invocation 判成功；collusion 要求双方都成功，partial compromise 被压到失败；contradiction/byzantine 又依赖语义 judge。不同 attack 的 ARIA-4 不完全同质。（物理页 4–6、16–18）
5. **judge 可见 internal thoughts**：许多生产 API 不暴露真实 chain-of-thought；benchmark judge 的信息集可能强于部署监控器可见信息。（物理页 28–31）
6. **版本与复现预算不足**：表只给模型家族/参数/provider；未给闭源 snapshot、API 日期、各 backbone decoding 参数、重复次数、token/cost/latency/硬件预算。GPT-4/CrewAI 因 credits 缺失，说明预算已影响覆盖。（物理页 7–8、15、17–18）
7. **persuasion-only attack 的零结果不能泛化**：作者称该攻击在所有设置均完全失败并推测 agent 对 persuasion robust，但没有给攻击强度、prompt 多样性或独立表格；更稳妥的结论只是“该实现未成功”。（物理页 15）
8. **无真实防御比较**：论文承认重点是攻击 benchmark，defense 仅轻量子集；没有与训练式对齐、权限隔离、capability security、消息签名/数据流控制等强架构防御做等预算比较。（物理页 8–9）

## 8. 页码定位索引

- 动机、攻击面总览、贡献：物理页 1–2。
- threat model、attacker knowledge/capability：物理页 3。
- DPI、Impersonation、IPI、single compromise：物理页 4。
- colluding/contradicting 与 benchmark 设计：物理页 5。
- 模型、ARIA/PNA/ERS 定义、主要结果：物理页 6–8。
- Failure discussion、limitations、ethical considerations：物理页 8–9。
- 数据 schema、模拟工具、统计与设计理由：物理页 13–15。
- attack success criteria、human judge validation、PNA：物理页 16。
- Safety/ERS normalization、bootstrap、defense 细节：物理页 17–19。
- 各配置 95% CI 表：物理页 20–22。
- 失败案例：物理页 23–27。
- ARIA、paraphrase、monitor 的完整 prompts：物理页 28–31。

## 9. 准入与第三读建议

- **准入：是，限定为 Failure / threat model / measurement。** 可准入的内容包括：三层攻击面；弱注入经多-agent 轨迹传播；orchestrator 单点故障；显式恶意任务被识别后仍执行；不同配置/模型下的 ARIA 分布；轻量防御的负面或不稳定结果。
- **不准入为 Operator。** delimiter、paraphrase、sandwich、monitor 均未显示稳定、跨模型、兼顾 benign utility 的防护；论文自身也把它们称为有限 lightweight baselines。
- **定量主张限制**：ERS 仅适用于当前 cohort 内相对比较；PNA 仅是 tool-call coverage；agent-level ARIA 受 judge 误差影响；不能据此给生产系统绝对安全评级。
- **建议第三读：是。** 第三读应优先复核：ARIA `0/1/2/3` 到 `A1..A4` 的实现映射；per-attack min-max 的具体分母与跨配置处理；PNA required-tools 清单如何生成；缺失模型/配置与 judge error 是否改变架构排序。第三读仍不应从 defense 子实验生成已验证 Operator。
