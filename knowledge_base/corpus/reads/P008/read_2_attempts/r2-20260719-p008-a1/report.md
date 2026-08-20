# P008 独立二读报告

## 0. Provenance、边界与核验方式

- 本报告引用冻结的 invocation snapshot：`r2-20260719-p008-a1/invocation.md`，Attempt ID 为 `r2-20260719-p008-a1`，启动时间为 `2026-07-19T17:10:00+08:00`。
- [AUTHOR_FACT] canonical 论文为 *Agent Security Bench (ASB): Formalizing and Benchmarking Attacks and Defenses in LLM-based Agents*，ICLR 2025。实际计算得到的 PDF SHA-256 为 `e2505f8632bfcb6a64a4390a3170b3ca1dfd3f9916d7c3cf9ba2b89887b3a0c9`，与 invocation 一致。
- 本次角色为 fresh 独立全文核源。未读取 `read_1`、Cards、其他读者报告或 blind query；未联网；未生成 Card；未评价 Candidate；未运行科研 Reviewer。
- Actual model/version：GPT-5 系列 Codex agent；更细的部署版本在当前界面不可见。Canonical task path：`/root/p008_second_read`；底层 opaque thread ID 不可见。
- Read boundary：`procedural_blinding`，不是技术文件隔离。平台级完整 file-access/tool trace：`unavailable`。本报告末尾列出本会话实际可观察的文件与工具操作。
- PDF 共 36 页。逐页提取了第 1–36 页文本，并将第 1–36 页全部以 PyMuPDF/Pillow 在内存中渲染为 4 页一组的可视蒙版检查；没有写出中间文本或图片。

## 1. 方法究竟改变哪一步计算？

[READER_INTERPRETATION] 这篇论文的主体是“统一形式化与基准”，不是单一新防御算法。它固定一个 ReAct 型 agent 执行链，再在四个位置改变送入 LLM/agent 的上下文；新提出的方法性组件主要是 PoT backdoor 和 NRP 指标。

| 机制 | 被改变的计算位置 | 形式化变化与定位 |
|---|---|---|
| DPI | 用户输入阶段 | [AUTHOR_FACT] 把注入指令拼接到目标 query，并把攻击工具加入工具集：`q^t ⊕ x^e`、`T + T^e`。PDF p.5，Sec. 4.1.1，Def. 1 / Eq. 4；短定位：“injects an injected instruction … to q^t”。 |
| IPI | 工具执行后的 observation | [AUTHOR_FACT] 在任意轨迹 observation `o_i` 后拼接注入指令，再影响后续规划/动作。PDF p.5，Sec. 4.1.2，Def. 2 / Eq. 5；短定位：“injects … to any step i of O”。 |
| Memory Poisoning | 长期记忆写入与检索 | [AUTHOR_FACT] 将对抗 key–value 计划加入 `D_clean`，使相似任务检索到 poisoned plan，并作为 ICL 示例影响新计划。PDF p.6，Sec. 4.2，Eq. 7；短定位：“D_poison = D_clean ∪ A”。 |
| PoT backdoor | system prompt 中的 demonstrations，外加 query trigger | [AUTHOR_FACT] 把带恶意 planning step/action 的 PoT demonstrations 写入 system prompt，并在 query 加触发器。PDF pp.6–7，Sec. 4.3，Def. 4 / Eqs. 8–9；短定位：“injecting backdoored PoT demonstrations … to system prompt”。 |
| Mixed attack | 多阶段同时干预 | [AUTHOR_FACT] 合并 DPI、IPI、Memory Poisoning；PoT 因其 prompt 不写入数据库而被排除。PDF p.16，App. A.1，Eq. 10；短定位：“PoT … are excluded from mixed attacks”。 |
| Defenses | 输入/observation 预处理，或 memory 检测 | [AUTHOR_FACT] delimiter、instructional prevention、paraphrase、DPR、sandwich 改写/包裹 prompt；shuffle 改 PoT step 顺序；PPL/LLM detector 判别 memory。PDF pp.7, 19–21，Table 2 / App. A.4；短定位：“prevention-based”与“detection-based”。 |
| NRP | 只改变评估聚合，不改变 agent 执行 | [AUTHOR_FACT] `NRP = PNA × (1 − ASR)`。PDF pp.8, 27，Table 4 / Eq. 20；短定位：“combined capability … utility and security”。 |

[READER_INTERPRETATION] 所有攻击都没有修改 backbone 权重；PoT 被明确称为 training-free（PDF p.3，Sec. 2，短定位：“training-free backdoor attack”）。真正被操纵的是 prompt、observation、memory、可见工具表和检索到的示例。

## 2. 输入、输出、可用信息与干预时点

- [AUTHOR_FACT] 基本 agent 输入为 system prompt `p_sys`、query `q`、observations `O`、tool list `T` 和从数据库检索的 `E_K(q ⊕ T, D)`；LLM 生成计划 `P`，agent 输出 tool-using action。PDF p.3，Sec. 3.1，Eq. 1；短定位：“input … task plan” / “output is a tool-using action”。
- [AUTHOR_FACT] Target task 由 instruction、tool list、data 构成；实验成功标签是是否调用全部所需工具。PDF pp.3, 23, 26，Sec. 3.1 / App. B.1 / Eqs. 18–19；短定位：“must correctly invoke all the required label tools”。
- [AUTHOR_FACT] 攻击者知道攻击工具名称与功能，能把攻击工具加入 agent toolkit；不知道 backbone 架构、训练数据和参数，只通过 API 交互。PDF p.4，Sec. 3.2；短定位：“lacks knowledge about … backbone LLM”。
- [AUTHOR_FACT] 对 system/user prompt 的威胁模型很强：攻击者可插入 system prompt，也假设能访问并修改用户 prompt；对 RAG/embedding 仅黑盒访问。PDF p.4，Sec. 3.2；短定位：“can craft and insert prompts” / “black-box access”。
- [AUTHOR_FACT] 干预时点分别为：DPI 在任务开始前；IPI 在某次工具 response 后、下一动作前；memory poisoning 在历史执行被保存时并在未来检索时生效；PoT 在部署 system prompt 时植入、在 query trigger 出现时激活。示例见 PDF pp.17–20，App. A.3.2 / Fig. 3。
- [AUTHOR_FACT] 实验工具是模拟 API，调用时返回预定义输出；为简化 tool calling，不设置参数。PDF pp.23, 25, 29，App. B.2 / C.2.1 / C.2.6；短定位：“did not set parameters”与“consistently produce the same predefined output”。
- [READER_INTERPRETATION] 因而这里测到的主要是“模型是否选择了指定工具名”，不是参数是否正确、真实副作用是否发生、权限是否允许，也不是端到端真实 API 安全性。

## 3. 最强基线与最接近组合基线

- [AUTHOR_FACT] 无攻击运行是 utility 基线 PNA；13 个 backbone 的平均 PNA 为 29.46%。PDF p.10，Table 6；p.33，Table 19。短定位：“Performance under no attack”。
- [AUTHOR_FACT] 在单类攻击中，DPI 平均 ASR 72.68%，高于 IPI 27.55%、Memory Poisoning 7.92% 和 PoT 42.12%；DPI 是表 5 中最强单类攻击。PDF p.9，Table 5。
- [AUTHOR_FACT] 最接近三路 Mixed Attack（84.30%）的较简组合是 DPI+MP（83.02%），仅低 1.28 个百分点；DPI+IPI 为 79.06%，IPI+MP 为 23.75%。PDF p.30，Table 14；短定位：“DPI+MP represents a near-optimal balance”。
- [READER_INTERPRETATION] 因此，对“组合是否必要”的最接近对照是 DPI+MP，而不是单独 DPI；表 14 显示加入 IPI 到 DPI+MP 的平均增益很小。
- [AUTHOR_FACT] 对 DPI，表 7 的 matched no-defense baseline 是 Combined DPI ASR 78.38%；DPR 最低为 44.45%，paraphrase 为 56.87%。对 IPI，matched baseline 为 27.98%，delimiter 最低为 24.96%。PDF p.10，Tables 7–8。
- [AUTHOR_FACT] 对 PoT，no-defense ASR 为 42.12%；paraphrase 为 29.06%，shuffle 为 44.37%。PDF pp.33–34，Table 20。
- [AUTHOR_FACT] benchmark 范围对照是 InjecAgent 与 AgentDojo。ASB 覆盖更多攻击类型、10 scenarios、420 tools；但 Table 12 只比较覆盖数量，并未在相同任务/模型/预算上报告三者的 head-to-head ASR。PDF p.25，App. B.3 / Table 12。
- [OPEN_QUESTION] 原文没有给出与 AgentDojo/InjecAgent 在共享数据、共享 backbone、共享 prompt budget 下的受控性能对照，所以不能从 Table 12 判断 ASB 攻击比这些系统“更强”，只能判断覆盖更广。

## 4. 结果是否可能来自模型、token、tool-call、prompt 或 oracle 差异？

- [AUTHOR_FACT] 模型差异非常大：PNA 从 Mixtral-8x7B 的 0% 到 Claude-3.5 Sonnet 的 100%；平均 ASR 也从 19.01% 到 67.55%。PDF pp.9–10，Tables 5–6。
- [READER_INTERPRETATION] 低 ASR 可能是 agent 根本不会完成任务，而非真正安全。作者也观察到 capability 与 ASR 的 rise-then-fall 关系。PDF p.9，Sec. 5.3 / Fig. 2；短定位：“limited task execution abilities … lower ASR”。NRP 部分缓解但不能消除该混杂。
- [AUTHOR_FACT] PoT 在 system prompt 额外加入两个 demonstrations/agent；作者承认 BP 增加可能来自这些 ICL plan examples。PDF pp.26, 31，Sec. C.2.2 / D.1.3；短定位：“providing more in-context learning plan examples”。
- [READER_INTERPRETATION] 因此 PoT 的 token 数、context 结构和示例信息量与 no-attack PNA 不相同；BP/PNA 差异不纯粹是 backdoor 效应。原文未报告等长度 clean-demonstration 对照。
- [AUTHOR_FACT] Mixed 与 PoT 只使用 Combined injection；DPI、IPI、Memory Poisoning 则跨五种 prompt injection type 评估。PDF pp.16, 26，App. A.3.1 / C.2.2。
- [READER_INTERPRETATION] 表 5 中 Mixed 84.30% 与“单类平均”直接比较并非完全等 prompt 强度/等 token 的实验；Table 14 的组合间比较更接近 matched comparison，但仍没有报告严格等 token budget。
- [AUTHOR_FACT] Memory Poisoning 的注入过程固定使用 GPT-4o-mini，而被评估 agent backbone 有 13 种。PDF p.26，Sec. C.2.2；短定位：“specific LLM used for the injection … GPT4o-mini”。
- [READER_INTERPRETATION] 这引入了独立的生成模型/oracle：poison 质量可能来自 GPT-4o-mini，而不仅是被测 backbone 的脆弱性。
- [AUTHOR_FACT] RR 由 backbone LLM 按给定 prompt 判断，而 ASR/PNA 由是否调用指定工具判断。PDF pp.8, 27–28，Table 4 / refusal judgment prompt。
- [READER_INTERPRETATION] RR 的 judge 随 backbone 改变，缺少统一独立 judge；ASR/PNA 则是工具名匹配式 oracle。不同指标的 oracle 机制并不一致。
- [AUTHOR_FACT] 工具无参数、响应固定、调用为模拟。PDF pp.23, 25, 29。
- [READER_INTERPRETATION] 这可能高估“选中工具名”等同于真实攻击成功的程度，也绕开了 schema、参数、鉴权、网络错误和真实 side effect。
- [OPEN_QUESTION] 未见统一报告 temperature、sampling seed、每个条件的重复次数、置信区间、显著性检验、具体闭源模型快照或 token/latency/cost；因此表中小百分点差异（尤其 1–3 个点）是否稳定，原文无法回答。

## 5. 作者明示限制、负向结果与未测试边界

### 明示或由实验设置直接给出的边界

- [AUTHOR_FACT] 只实现 ReAct agent framework。PDF p.16，App. A.2；短定位：“we use the ReAct framework”。
- [AUTHOR_FACT] 全部工具调用为模拟，不使用真实 API；工具没有参数。PDF pp.23, 25，App. B.2 / C.2.1。
- [AUTHOR_FACT] 场景、agent role、每个 agent 的 5 个 user tasks 与工具字段由 GPT-4 生成。PDF pp.22–24，App. B.1–B.2。
- [AUTHOR_FACT] PoT 只测试 10 个 agents 中的 5 个，每个选择 2 个 demonstrations 和 2 个不同 testing tasks。PDF p.26，Sec. C.2.2。
- [AUTHOR_FACT] 作者把更强防御与更多攻击场景留作未来工作。PDF p.10，Sec. 6；短定位：“improving defenses and expanding attack scenarios”。
- [AUTHOR_FACT] 作者指出更复杂的上下文验证可能增加计算开销，并影响 autonomous driving 等实时任务，但没有实际测 latency。PDF pp.33–34，Sec. D.2.1–D.2.2。

### 负向结果

- [AUTHOR_FACT] Memory Poisoning 是最弱攻击，平均 ASR 7.92%。PDF p.9，Table 5 / Sec. 5.3。
- [AUTHOR_FACT] DPI/IPI 的防御总体有限，且 benign PNA 平均下降：delimiter -6.94、paraphrase -1.77、instructional -2.83、sandwich -1.17、DPR -3.08 个百分点。PDF pp.32–33，Sec. D.2.1 / Table 19。
- [AUTHOR_FACT] PoT shuffle 不但没有降低平均 ASR，反而从 42.12% 升到 44.37%；例如 Claude-3.5 Sonnet 从 17.50% 升到 93.50%。PDF pp.33–34，Table 20。
- [AUTHOR_FACT] Memory 的 LLM detector 平均 FNR 0.660、FPR 0.200；PPL detector 在阈值范围内无法同时获得低 FNR/FPR。PDF pp.34–35，Sec. D.2.3 / Table 21 / Fig. 4。
- [AUTHOR_FACT] IPI 的 sandwich 平均 ASR 28.04%，略高于 no-defense 27.98%；DPI delimiter 79.08%，略高于 no-defense 78.38%。PDF p.10，Tables 7–8。

### 未测试或不足以推出的边界

- [OPEN_QUESTION] 未测试非 ReAct 架构、真实权限系统、真实 API side effect、参数级工具攻击、长时间在线交互、多人/多 agent、adaptive attacker 或防御感知攻击者。
- [OPEN_QUESTION] 没有证明 GPT-4 生成的 50 个正常任务与 400 个攻击任务代表现实分布，也没有人工标注一致性或数据生成偏差分析。
- [OPEN_QUESTION] PoT 对另外 5 个 agent、更多 demonstrations/test tasks、不同 system-prompt 模板和严格等长度 clean demonstration 的泛化未给出。
- [OPEN_QUESTION] 闭源模型版本、调用日期、sampling 设置和重复试验信息不足，难以完全复现具体百分比。

## 6. 可抽取的 Operator 与真实可记录的 Failure

以下只是独立二读中的可抽取内容，不是正式 Card 或科研裁决。

### Operator

1. [AUTHOR_FACT] `query_append_injection`：把恶意 instruction 拼接到 user query（DPI）。PDF p.5，Def. 1 / Eq. 4。
2. [AUTHOR_FACT] `observation_append_injection`：在工具 response/observation 后拼接恶意 instruction（IPI）。PDF p.5，Def. 2 / Eq. 5。
3. [AUTHOR_FACT] `black_box_memory_poison_via_saved_plan`：通过历史 DPI/IPI 把 poisoned plan 写入共享 memory，再靠相似检索传播。PDF p.6，Sec. 4.2.2；示例 pp.18–19。
4. [AUTHOR_FACT] `system_prompt_pot_backdoor`：system prompt 加入 trigger→恶意 planning step→target tool 的 demonstrations，并在 query 触发。PDF pp.6–7，Sec. 4.3；示例 pp.17–18。
5. [AUTHOR_FACT] `multi_surface_attack_composition`：合并 query、observation、memory 三个攻击面。PDF p.16，Eq. 10；p.30，Table 14。
6. [AUTHOR_FACT] `prompt_transform_prevention`：delimiter、instructional prompt、paraphrase、DPR、sandwich。PDF pp.19–21，App. A.4.1–A.4.2。
7. [AUTHOR_FACT] `demonstration_step_shuffle` 与 `trigger_paraphrase`：破坏 PoT step 顺序或 trigger 表面形式。PDF p.21，App. A.4.4。
8. [AUTHOR_FACT] `memory_anomaly_detection`：以 PPL threshold 或 LLM 判别 retrieved plan。PDF p.21，App. A.4.3。
9. [AUTHOR_FACT] `utility_security_product_metric`：用 `PNA × (1 − ASR)` 聚合 utility 与 security。PDF p.27，Eq. 20。

### Failure

1. [AUTHOR_FACT] `mixed_attack_tool_hijack`：三路混合攻击平均 ASR 84.30%、RR 3.22%。PDF p.9，Table 5；p.30，Table 14。
2. [AUTHOR_FACT] `dpi_tool_hijack`：DPI 平均 ASR 72.68%。PDF p.9，Table 5。
3. [AUTHOR_FACT] `defense_semantic_persistence`：paraphrase 后恶意语义仍被执行；作者据此解释防御失败。PDF p.32，Sec. D.2.1，短定位：“semantic intent persists after rewording”。
4. [AUTHOR_FACT] `delimiter_boundary_non_isolation`：delimiter 不能让模型严格隔离恶意块；平均 ASR 甚至略升。PDF pp.10, 32，Table 7 / Sec. D.2.1。
5. [AUTHOR_FACT] `shuffle_amplifies_backdoor`：PoT shuffle 平均 ASR 高于无防御，且个别 backbone 大幅恶化。PDF pp.33–34，Table 20。
6. [AUTHOR_FACT] `memory_detector_high_miss_rate`：LLM detector 漏掉约 66% memory attacks。PDF pp.34–35，Table 21。
7. [AUTHOR_FACT] `ppl_threshold_tradeoff_failure`：PPL 阈值低时 FPR 高，阈值高时 FNR 高。PDF p.35，Fig. 4。
8. [AUTHOR_FACT] `defense_clean_utility_loss`：多数 prompt defenses 降低 benign PNA。PDF p.33，Table 19。
9. [READER_INTERPRETATION] `capability_security_conflation`：部分低 ASR 与极低 PNA 同时出现，安全表象可能来自不会完成任务。证据：PDF pp.9–10，Tables 5–6 / Fig. 2。

## 7. 关键判断的证据索引

| 判断 | 页码与定位 | 短定位文本 |
|---|---|---|
| 四个攻击面覆盖 system/user/tool/memory | pp.1–2，Abstract / Fig. 1 | “system prompt, user prompt handling, tool usage, and memory retrieval” |
| Agent 基本计算与 action 输出 | p.3，Sec. 3.1 / Eq. 1 | “output is a tool-using action” |
| 攻击者能力与黑盒边界 | p.4，Sec. 3.2 | “black-box access to RAG databases and embedders” |
| 五种 prompt injection 构造 | p.5，Table 1 / Eq. 6 | “string concatenation” |
| Memory poisoning 形式化 | p.6，Sec. 4.2 / Eq. 7 | “D_poison = D_clean ∪ A” |
| PoT backdoor 形式化与触发 | pp.6–7，Sec. 4.3 / Eqs. 8–9 | “backdoored planning step” |
| Bench/metrics 规模 | p.8，Tables 3–4 | “10 scenarios” / “7 metrics” |
| 主攻击结果 | p.9，Table 5 / Fig. 2 | “highest average ASR (84.30%)” |
| 主防御结果 | p.10，Tables 7–8 | “current prevention-based defenses are inadequate” |
| Mixed 定义 | p.16，App. A.1 / Eq. 10 | “combine as mixed attacks across steps” |
| 四类攻击实例 | pp.17–20，App. A.3.2 / Fig. 3 | “Illustration of four attack types” |
| 数据与工具生成 | pp.22–25，App. B.1–B.2 | “generate … using GPT-4” |
| 模型与实现设置 | pp.25–29，App. C.1–C.2 | “simulated tool calls” |
| 组合消融 | p.30，Table 14 | “DPI+MP … 83.02%” |
| PoT 触发与 utility | pp.30–31，Tables 15–16 | “BP … and PNA” |
| Prompt 类型与 aggressive 切分 | pp.31–32，Tables 17–18 | “Combined Attack … highest average ASR” |
| 防御的 clean utility 损失 | pp.32–33，Table 19 | “slight decline in performance” |
| PoT 防御失败 | pp.33–34，Table 20 | “limited effectiveness” |
| Memory 防御失败 | pp.34–35，Table 21 / Fig. 4 | “average FNR is 0.660” |
| 可复现性声明 | p.36，Sec. F | “scripts, configuration files, and Docker setup” |

## 8. 解析文本与可视 PDF 是否冲突？

- [AUTHOR_FACT] 36 页均能提取文本；可视渲染显示页序连续，正文、表格、公式、Fig. 1–4 与提取结果所在页一致；未发现解析器把整页遗漏、交换或错误归页。
- [READER_INTERPRETATION] 没有发现“解析文本 vs 可视版式”的实质冲突。数学符号在纯文本提取中有上标/空格位置损失，但与可视 PDF 的公式结构可以对应；不影响本报告对干预位置和数值表的定位。
- [AUTHOR_FACT] 存在论文自身的文字—表格内部不一致，不是解析错误：
  1. PDF p.30，Sec. D.1.2 prose 写 Mixed Attack `84.03%`，同页 Table 14 与前文 Table 5 均为 `84.30%`。
  2. PDF p.31，Table 16 前写“The LLM backend used is GPT-4o”，但 Table 16 明列 13 个不同 LLM；该句可能错置或表述错误。
  3. PDF p.27，NRP 示例把 `80% × (1 − 0.30)%` 和 `0.70%` 写入中间式；最终 `56%` 与预期的 `0.8 × 0.7` 一致，但百分号记法在量纲上不严谨。
  4. 攻击方法数按不同粒度出现：p.8 Table 3 记 13，p.25 Table 12 记 16（含 4 个 mixed combinations），Abstract 以 16 attacks + 11 defenses 得到 27。可以按“mixed 算一类”或“mixed 四组合分别计数”解释，但文中没有统一说明计数口径。
- [OPEN_QUESTION] 由于遵守只写 `report.md` 的边界，本次视觉核查采用内存低分辨率逐页蒙版，而未落盘高分辨率页面图。密集表格数值已用逐页文本提取交叉核对；若后续需要像素级排版审计，应另行授权高分辨率页面渲染，但这不改变上述内容核源结论。

## 9. 实际读取文件、工具与可观察 trace

### 实际读取的 3 个研究文件

1. `D:/Desktop/crl_judge/crl_agent_v3/knowledge_base/staging/papers/P008_agent_security_bench.pdf`
2. `D:/Desktop/crl_judge/crl_agent_v3/knowledge_base/templates/second_read_prompt.md`
3. `D:/Desktop/crl_judge/crl_agent_v3/knowledge_base/pilot/reads/P008/read_2_attempts/r2-20260719-p008-a1/invocation.md`

为遵守工具使用规则，还读取了两个非研究性的本地技能指令文件：`C:/Users/g/.codex/skills/pdf/SKILL.md` 与 `C:/Users/g/.codex/skills/encoding-safe-edit/SKILL.md`。除此之外未读取任何工作区研究文件，也未枚举工作区。

### 实际使用/尝试的工具

- PowerShell `Get-Content -Encoding utf8`：读取 prompt 与 invocation；首次未显式编码的显示出现乱码，随后用 UTF-8 重新读取，原文件未被修改。
- PowerShell `Get-FileHash -Algorithm SHA256`：核对 PDF hash。
- Python `pypdf.PdfReader`：获得 36 页页数、metadata，并逐页提取 p.1–36 文本。
- Python `PyMuPDF (fitz)` + `Pillow`：只在内存中渲染 p.1–36 的可视页，未写图片文件。
- `pdfinfo`：尝试调用但本地命令不可用/路径解析失败，未得到 PDF 信息；随后由 pypdf 完成页数与 metadata 核验。
- `view_image`：尝试直接打开 PDF，但该工具不能把 PDF 作为图片处理；随后改为内存渲染。
- `apply_patch`：仅创建本报告。
- 网络工具：未使用。

平台未提供可验证的文件级 allowlist，也未向本 agent 暴露完整系统 file-access/tool audit log。因此：`procedural_blinding`；完整 observable file-access/tool trace = `unavailable`。以上清单是当前会话中可由 agent 直接观察并如实报告的操作记录。
