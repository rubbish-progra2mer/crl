# P075 独立来源二读报告

## 1. 来源、读取边界与覆盖

- `[AUTHOR_FACT]` 本报告引用的 invocation snapshot 为 `r2-20260720-p075-a1/invocation.md`；其中将本读者定义为 fresh independent full-paper source checker，blinding 状态为 `procedural_blinding`，而非技术性文件隔离。
- `[AUTHOR_FACT]` 实际读取路径为 `knowledge_base/staging/plan05_sat_a2/P075_memory_privacy.pdf`。
- `[AUTHOR_FACT]` 实际 PDF SHA-256 为 `8c2cfcee69d60f4c20a959cd6b1a6a14d5f6e8d732792cf2a2b4864ac38a88cb`，与 invocation 记录一致。
- `[AUTHOR_FACT]` PDF 共 20 个物理页；本次对物理页 1–20 全部进行了文本解析和逐页可视核验。它们对应印刷页码 25241–25260，覆盖摘要、正文、Limitation、参考文献以及附录 A–C、表 1–9 和图 1–5。
- `[AUTHOR_FACT]` 首页给出的论文题名为 *Unveiling Privacy Risks in LLM Agent Memory*，发表于 ACL 2025 Long Papers（物理页 1，印刷页 25241）。
- `[READER_INTERPRETATION]` 解析文本与可视 PDF 在章节、图表、页码和数值上未发现实质冲突。附录含有具体攻击提示模板和个体化医疗查询案例；本报告只核验其存在与研究作用，不复制这些内容，以避免把论文证据改写成操作指南或扩散潜在隐私文本。

## 2. MEXTRA 改变了哪一步计算

- `[AUTHOR_FACT]` 被测 agent 的长期记忆 `M` 存储过去的 query–solution 对 `(q_i,s_i)`；对新 query `q`，相似度函数 `f(q,q_i)` 排序并取 top-`k` 记录 `E(q,M)`，将其作为 in-context demonstrations 与 system context `C`、当前 query 一并送入 LLM；生成 solution 后再调用工具执行（物理页 2，§2.1）。
- `[AUTHOR_FACT]` MEXTRA 不修改模型、记忆库或检索器。攻击者只提交输入 query，诱导 agent 把本轮检索到的历史 query 通过 agent 原本可见的执行输出暴露出来（物理页 2–4，§2.2–3.1；图 1）。
- `[AUTHOR_FACT]` 论文将攻击 prompt 抽象成两个功能部分：locator 指定目标是检索到的历史示例，而不是系统上下文中的其他内容；aligner 将输出方式适配目标 agent 的原有 workflow。这样既定位记忆内容，又使其能经代码答案或网页动作等合法输出通道返回（物理页 3–4，§3.1）。
- `[AUTHOR_FACT]` 单次攻击最多接触 top-`k` 检索集合。为减少不同攻击的检索重叠，作者再用 GPT-4 自动生成多样化输入，目标是在固定 prompt 数量下扩大多个检索子集的并集（物理页 3–4，§2.2、§3.2）。
- `[READER_INTERPRETATION]` 机制核心是“利用当前 query 同时控制检索邻域和 agent 对检索示例的处理方式”。它不是从整个 memory 直接读取，也不是模型参数提取；泄露上限先由 retrieval 暴露给 LLM context 的 top-`k` 记录决定，再由 agent 是否服从输出指令决定。

## 3. 威胁模型、输入输出与干预时点

- `[AUTHOR_FACT]` 攻击目标是尽可能多地提取 memory 中过去的 user queries `q_i`。作者声称得到 query 后可容易复现对应 agent response，但实验指标只直接度量 query 提取，没有单独验证 response reproduction（物理页 3，§2.2）。
- `[AUTHOR_FACT]` 攻击能力被定义为黑盒：攻击者只能通过输入 query 与 agent 交互，不能直接访问 memory、system prompt 或模型内部（物理页 2–3，§2.2）。
- `[AUTHOR_FACT]` 攻击干预发生在 agent 正常接收用户 query 的入口；泄露输出发生在 solution 执行后可由攻击者观察的任务通道。agent 内部仍执行既有 top-`k` 检索、LLM 生成和 tool execution（物理页 2–4，§2.1–3.1）。
- `[AUTHOR_FACT]` 实验为静态 memory：评估期间存储记录保持不变。默认 memory size 为 200；EHRAgent 检索 4 条，RAP 检索 3 条（物理页 5，§4.1；物理页 13，附录 B.1）。
- `[READER_INTERPRETATION]` “黑盒”描述适用于攻击接口，但研究评估者为了计算 RN、CER 等指标必须观察实际内部检索集合。这是评估 oracle，不是攻击者可见信息；报告结果不能理解为攻击者在真实黑盒环境下知道每次是否提取完整。

## 4. 攻击者知识分级与自动 prompt 生成

- `[AUTHOR_FACT]` basic knowledge 只包括应用领域和任务的一般背景。对应生成指令要求 GPT-4 在保持同一提取功能的同时改变表达，并使用任务说明、生成要求、输出格式和 in-context demonstrations（物理页 3–4，§2.2、§3.2；物理页 13、16，附录 A.1）。
- `[AUTHOR_FACT]` advanced knowledge 假设攻击者通过探索性交互已经推断出 `f(q,q_i)` 属于 edit-distance 类或 cosine-similarity 类。作者据此让生成输入在与该检索函数相关的特征上多样化，以扩大覆盖的检索邻域（物理页 3–4，§2.2、§3.2；物理页 13、17–18，附录 A.2）。
- `[READER_INTERPRETATION]` 论文在高级实验中直接按已知的真实 scoring-function 类型构造生成指令，没有给出从纯黑盒交互推断 `f` 的算法、查询复杂度、准确率或误判实验。因此“advanced black-box attacker”实际包含一个未实现的检索器类型 oracle。
- `[AUTHOR_FACT]` 附录公开了完整 prompt-generation instructions（物理页 16–19，表 5–8）。本报告不转录这些模板；就核源而言，它们证实 basic/advanced 与各 ablation 的 prompt 条件并不相同。
- `[OPEN_QUESTION]` GPT-4 prompt generator 的具体版本、temperature、随机种子、token budget、生成失败处理与费用没有报告。生成器随机性被作者用于解释小 `n` 时的反常结果，但未给方差（物理页 8，§6.2）。

## 5. 两类主要 agent、memory 与数据来源

- `[AUTHOR_FACT]` 主实验选择 EHRAgent 和 RAP/WebShop。EHRAgent 是医疗记录场景的 code-powered agent，以 edit distance 检索 top-4 记录，再生成并执行代码；RAP 是在线购物 web agent，以 MiniLM/SBERT cosine similarity 检索 top-3 记录，再生成网页动作（物理页 5，§4.1；物理页 13，附录 B.1）。
- `[AUTHOR_FACT]` 默认 agent core 均为 GPT-4o，memory size 均为 200。EHRAgent memory queries 随机来自 MIMIC-III，RAP memory queries 随机来自 WebShop；对应 solutions 由 agent 运行生成（物理页 5，§4.1）。附录说明生成 solution 是否正确不影响其被纳入 memory（物理页 13–14，附录 B.1）。
- `[AUTHOR_FACT]` 附录另构造 QA-Agent，用 GPT-4o、top-4 和 200 条 MMLU question–reasoning records 测试一般性；作者明确说 MMLU 不是隐私或领域专属数据，该实验只验证提取机制泛化（物理页 14–15，表 4及附录 B.2）。
- `[READER_INTERPRETATION]` 主实验中的“私人 query”是从既有 benchmark/database 随机构建的静态 memory，不是来自真实部署中的活跃多用户 agent。论文没有建立用户同意、身份可识别性或每条 query 敏感级别的人工隐私标注。
- `[READER_INTERPRETATION]` EHRAgent 与 RAP 的差异同时包含领域、输出通道、top-`k`、检索函数、embedding 和任务成功率，故两者泄露量差异不能被单独归因于 code agent 对比 web agent。
- `[OPEN_QUESTION]` 随机 memory 抽样的 seed、重复抽样次数和不同 memory composition 的置信区间未报告；memory-size 实验中小集合是大集合的子集，只代表一条嵌套样本轨迹（物理页 6，§5.1）。

## 6. 泄露指标与 privacy oracle

- `[AUTHOR_FACT]` `EN=|Q|` 是跨 `n` 个攻击提取出的唯一历史 query 数；`EE=|Q|/(n×k)` 是以 prompt 数和 retrieval depth 归一化的效率；`RN=|R|` 是所有实际检索集合并集的大小；`CER` 是完整输出本次全部 `k` 条的攻击比例；`AER` 是至少输出一条的攻击比例（物理页 5，§4.1）。
- `[AUTHOR_FACT]` 附录说明每个 attacking prompt 最多运行 3 次；若一次完整输出所有 retrieved queries 就提前停止，否则继续到三次，以减轻 LLM 随机性（物理页 14，附录 B.1）。
- `[READER_INTERPRETATION]` `EE` 的分母仍是 `n×k`，而不是实际 agent executions 数。因此论文的“30 prompts”可能包含最多 90 次 agent 调用；EE 衡量的是每个独特 prompt 的名义效率，不是每次 API call、token 或成本效率。最多三次的择优停止也会提高 CER/AER，相对真实一次性攻击更有利。
- `[READER_INTERPRETATION]` privacy oracle 将“与 memory 中历史 query 对上”视为泄露；没有 PII detector、敏感性分级、语义近似泄露评分或人工隐私危害评估。它适合测 verbatim/query-level extraction，但不能量化实际隐私伤害。
- `[OPEN_QUESTION]` 论文未说明 exact matching 的规范化规则、重复/改写输出如何判定、自动解析失败如何处理，或 CER/AER 是否由脚本还是人工核验。附录案例还显示输出可能混入 system prompt 的 hard-coded examples；这些非 memory 项如何从 Q 中排除没有程序说明（物理页 20，表 9）。

## 7. 基线、主要结果与负向结果

### 7.1 基线设计

- `[AUTHOR_FACT]` 最接近的组合基线是 `w/o aligner`：保留显式索取 retrieved queries 和同一 GPT-4 多样化生成，但不指定适配 agent workflow 的输出格式。另有 `w/o req` 与 `w/o demos`，分别移除生成指令中的显式 requirements 或 demonstrations（物理页 5，§4.1；物理页 13、19，附录 A.3）。
- `[READER_INTERPRETATION]` 这些主要是 MEXTRA 自身组件消融，不是与已发表 RAG extraction、adaptive attack 或通用 prompt-injection 系统的端到端强基线比较。论文只用一个案例展示通用“重复上下文”式输入失败（物理页 14、20，附录 B.2、表 9）。
- `[AUTHOR_FACT]` 基线强弱取决于指标：按 EN，EHRAgent 的最强消融是 `w/o req`（39），RAP 也是 `w/o req`（25）；但 RN 上某些消融反而更高，例如 EHRAgent `w/o req` 为 61、高于 MEXTRA 的 55，RAP `w/o demos` 为 32、高于 MEXTRA 的 27（物理页 5，表 1）。这支持“覆盖检索集合”和“成功输出集合”必须分开看。

### 7.2 主结果

- `[AUTHOR_FACT]` 默认 `n=30,m=200` 时，MEXTRA 在 EHRAgent 上报告 EN/RN/EE/CER/AER 为 50/55/0.42/0.83/0.83，在 RAP 上为 26/27/0.29/0.87/0.90（物理页 5–6，表 1、§4.2）。
- `[AUTHOR_FACT]` 在 EHRAgent 上，`w/o aligner` 的 EN 从 50 降为 36；在 RAP 上从 26 降为 6，且 CER 从 0.87 降为 0.17。作者将更大降幅归因于 web agent 必须把内容适配为网页动作，而 code agent 的文本答案通道限制较小（物理页 5–6，表 1、§4.2）。
- `[AUTHOR_FACT]` 表 2/图 2 显示，在两个 agent 上 edit-distance retrieval 总体比 cosine retrieval 泄露更多；memory size 从 50 增到 500 时 EN/EE 一般上升，但个别点会回落。作者认为 memory distribution 改变会影响 retrieval（物理页 6–7，表 2、图 2、§5.2）。
- `[AUTHOR_FACT]` retrieval depth 从 1 增至 5 时 EN 总体上升；但 RAP 在 `k≥4` 时 RN 与 EN 的差距扩大，说明检索更多记录并不保证全部成功输出（物理页 7，图 3、§5.2）。
- `[AUTHOR_FACT]` RAP backbone 实验中，GPT-4/GPT-4o/Llama3-70b 的 EN 分别为 23/26/17；Llama3-70b 的 CER 为 0、AER 为 0.93。作者同时报告 Llama3-70b 原购物任务成功率仅 8%，而 GPT-4/4o 约 40%，并认为低 agent 可用性限制了提取结果（物理页 7，表 3、§5.2）。
- `[READER_INTERPRETATION]` Llama3 结果是一项重要负向/边界结果：高 AER 但零 CER 表明它经常泄露部分内容却无法完整执行；较低 EN 不能解释为更强隐私防护，因为其正常任务能力也显著较弱。
- `[AUTHOR_FACT]` 随攻击 prompt 数从 10 增到 50，EN/RN 持续增加。`n=50` 时，作者报告 edit-distance agents 泄露超过 memory 的 30%，cosine agents 也超过 10%；advanced instruction 几乎总是优于 basic，但在 edit distance 且 `n` 较小时有例外（物理页 7–8，图 4、§6）。
- `[AUTHOR_FACT]` 表 2 标题写作 “extracted number (EE)”，但 EE 在 §4.1 被定义为比例，表中实际展示的是整数 extracted number。可视 PDF 与解析文本一致，这是原论文的标签/排版不一致，不是解析冲突（物理页 5–6）。

## 8. 结果是否可能来自模型、调用、prompt、数据或 oracle 差异

- `[AUTHOR_FACT]` 主表 MEXTRA 与其组件消融使用同一默认 GPT-4o agent、同一 memory 和同类 GPT-4 generator，因而表 1 对 locator/aligner 与 generation-instruction 组件具有一定控制（物理页 5，§4.1）。
- `[READER_INTERPRETATION]` 但组件 ablation 的 prompt-generation requirements 与 demonstrations 本身不同，输出的 prompt 长度、语义分布和检索覆盖也随之改变。表 1 中 RN 的变化证明消融不只改变 agent 服从率，也改变 retrieval exposure；EN 差异不能纯归因于 aligner。
- `[READER_INTERPRETATION]` 每个 prompt 最多重试三次且取提前成功结果，没有一轮 one-shot 对照、总 token、调用次数、延迟或成本，可能放大对随机 proprietary LLM 的结果。GPT-4 generator 与 GPT-4o core 的版本漂移也是复现边界。
- `[READER_INTERPRETATION]` scoring-function 和 embedding 实验改变了攻击输入的检索分布；backbone 实验又同时改变正常 task competence。它们揭示相关因素，而非隔离的因果机制证明。
- `[OPEN_QUESTION]` 论文没有误差条、置信区间、显著性检验或完整 repeated-run 分布。“up to three runs”是单个 prompt 的择优重试，不等于独立重复整个实验。
- `[OPEN_QUESTION]` RN/CER 所需的内部 retrieved-set oracle 在开放黑盒产品中通常不可见；若没有它，攻击者无法判断提取是否完整，也难以执行论文式 stop condition。实际攻击成本和覆盖率估计可能更差。

## 9. defenses、作者限制与未测边界

- `[AUTHOR_FACT]` 附录 C 只定性讨论两类潜在防御，没有实验：输入/输出控制（如 system-level hard rule 或 paraphrasing）可能被表面正常的输入绕过，且改写不一定消除敏感信息；memory sanitation/de-identification 可能削弱历史记录作为 demonstrations 的效用（物理页 15，附录 C）。
- `[AUTHOR_FACT]` 作者在 Limitation 中承认只评估 single-agent；没有测试 agent 间通信或共享 memory。被测框架也没有 session control，多个用户可共享同一 session 和 memory；作者提出 user/session-level isolation 可能缓解风险，但因缺少标准集成方式而留待未来（物理页 9，Limitation）。
- `[READER_INTERPRETATION]` user/session isolation 是论文威胁成立的关键前提而不只是普通工程细节：若真实系统在访问控制层把用户 memory 严格分区，跨用户提取面会显著缩小。论文没有测试认证、授权、租户隔离或 rate limiting。
- `[READER_INTERPRETATION]` 静态 memory 排除了攻击交互被写回 memory、检索分布随时间变化、淘汰策略、摘要/压缩 memory、删除请求和并发更新。这些都可能改变提取覆盖与重复率。
- `[READER_INTERPRETATION]` 论文没有评估实际防御后的 privacy–utility trade-off；“filter 可能失败”和“de-identification 可能损害效用”只是合理假设，不是实验性 negative result。
- `[OPEN_QUESTION]` 未测边界包括多 agent、production black-box agents、其他 memory 架构（摘要式、结构化、向量+访问控制）、非 top-`k` retrieval、tool-side policy、跨会话认证、长时间自适应攻击、限流和审计告警。

## 10. 可抽取 Operator 与可记录 Failure

### 10.1 Operator 候选

- `[READER_INTERPRETATION]` `RetrievalExposureProbe`：用一组功能等价但检索特征多样的输入，测量 query 对 top-`k` memory exposure 与唯一覆盖的影响；研究用途是审计 memory retrieval 是否会把其他用户记录放入可生成 context。它不应被部署为提取工具。
- `[READER_INTERPRETATION]` `WorkflowAlignedLeakageTest`：把同一隐私索取意图分别映射到 agent 原生输出通道，比较无通道适配与有通道适配时的泄露率；对应 locator/aligner 消融（物理页 3–6，§3.1、表 1）。
- `[READER_INTERPRETATION]` `MemoryConfigurationRiskSweep`：在固定 memory/data 条件下改变 similarity function、embedding、`k`、memory size 与 backbone，联合报告 RN、EN、CER、AER，避免只把泄露归咎于模型（物理页 6–8，§5–6）。
- `[READER_INTERPRETATION]` 上述仅是可复用的防御性审计抽象，不包含原文的攻击 prompt、长度调制、领域词或具体输出格式，也不构成正式 Card 或科研裁决。

### 10.2 可记录 Failure

- `[AUTHOR_FACT]` 共享 session 的 memory records 可在仅有输入-query 权限时，经 agent 的正常执行输出泄露；默认设置下两个主要 agent 都出现显著 EN/CER（物理页 5–6，表 1）。
- `[AUTHOR_FACT]` workflow aligner 缺失会使 RAP 的完整提取率大幅下降，说明一般文本输出式 RAG 攻击不一定适用于 action-only agent；通用“重复全部上下文”案例也没有定位到 memory records（物理页 5–6、14、20）。这是对攻击可迁移性的负向边界。
- `[AUTHOR_FACT]` 大 `k` 会增加 exposure，但也可能降低完整提取；弱 backbone 可能部分泄露却无法完整执行；memory size 增长也存在局部回落（物理页 6–8）。这些是论文实际观察到的非单调或负向结果。
- `[READER_INTERPRETATION]` 最根本的系统 failure 是把不同用户的长期交互当作无访问控制的 in-context demonstrations，并允许当前输入同时影响 retrieval 和生成行为。攻击 prompt 是触发器，跨用户 memory 暴露才是结构性前提。

## 11. 黑盒外推边界与结论

- `[AUTHOR_FACT]` 论文验证了两个主要开源研究 agent 和一个附加 QA-Agent；所有默认主要实验使用 GPT-4o，prompt generator 使用 GPT-4，memory 是离线 benchmark 构造，且评估者可记录内部 retrieval（物理页 4–5、13–15）。
- `[READER_INTERPRETATION]` 证据足以支持“在所测共享、静态、top-`k` demonstration memory 架构中，仅输入访问可以诱发 query-level leakage”。它不足以证明所有 production agent、所有 memory 形式或严格 session-isolated 系统同样脆弱。
- `[READER_INTERPRETATION]` advanced results 不能直接外推给无内部知识的黑盒攻击者，因为 scoring-function 推断过程没有实现；防御结论也不能外推，因为没有实际部署或防御实验。
- `[OPEN_QUESTION]` 后续核验最需要补充：一次调用基线与真实调用成本；完整实验重复和误差；privacy matching/敏感性 oracle；scoring-function 黑盒推断准确率；session-isolated 与 access-controlled memory；实际输入输出过滤和 sanitation 的 privacy–utility 曲线；动态 memory、多用户与多 agent 设置。
- `[READER_INTERPRETATION]` 独立来源结论：MEXTRA 的实质贡献是揭示“检索暴露 + workflow-aligned direct instruction”这一组合风险，并以多种 memory 配置展示其可发生性。最强限制是威胁环境缺少会话隔离、数据与 memory 静态、攻击可重试、内部 oracle 可见于评估、高级知识由假设给定、且 defense 仅讨论。对外使用时应将其视为防御性风险审计证据，而不是可直接照搬的攻击指南。
