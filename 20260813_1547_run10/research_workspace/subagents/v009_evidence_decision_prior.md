# v009 证据决策核先行工作碰撞审计（Research Subagent 草案）

> 身份与权限：本文件由 Codex App 原生 Research Subagent 产生，只是非权威先行工作审计。它不构成 Seed、No-Go、版本推进或 Run 终局裁决，也未修改 `hypotheses`、`portfolio`、`Decision`。共享知识库仅作只读检索；未读取其他 Run。

## 1. 审计对象与判定口径

目标失败是：深度研究/搜索智能体已能到达真实的底层记录链，却在看到一个答案形态完整、表述流畅、但事实错误的总结文档后提前停止。

审计两个拟议方法核：

- **A：来源依赖/复制谱系感知的 provenance-cut stopping certificate**。对答案的原子主张及支持证据构图；把转载、改写、共同上游来源折叠到记录生成根；只有必要子主张都闭合，并有足够的独立记录根支持，才允许停止。若不满足，下一次搜索应定向寻找能切断最大来源依赖的证据。
- **B：claim-triggered falsification obligation compiler**。一旦轨迹中出现直接答案型主张，就由主张和问题编译“若该主张为真，底层记录中应出现什么”以及连接义务/反例义务；主动寻找最能区分当前答案和竞争答案的记录；义务闭合后才允许提交。

碰撞口径：

- **exact**：目标状态、关键改变计算和输出契约基本相同，换名不能构成新方法。
- **partial**：核心算子相同，但任务、触发时机、证据粒度或停止方式仍有实质差异。
- **component**：拟议方法中的一个必要模块已被占据，但尚未覆盖组合后的改变计算。
- **none / benchmark-only**：不构成方法碰撞，只提供失败现象或评测路径。

这里的“没有检索到 exact”绝不等价于证明新颖；尤其 2026 年论文仍可能存在索引延迟、版本变化和未覆盖工作。

## 2. 检索范围、一级来源与失败记录

本次优先使用 arXiv 原文 HTML/PDF、ACL Anthology 论文页/PDF、VLDB PDF 和 OpenReview 原文。共享知识库按标题、arXiv 编号和关键短语只读检索，没有命中本次指定的 2026 年论文；因此近期工作主要由网络一级来源补齐。经典来源依赖工作由 VLDB 原始 PDF 核查。

网络检索中的边界与失败：

1. 对 `copy-invariant evidence aggregation`、`duplication-invariant evidence`、`source-lineage stopping LLM agent` 等精确组合的检索没有找到一个同时覆盖“复制根折叠、根独立停止证书、定向主动补证”的 LLM 智能体论文；这只是当前检索结果，不是新颖性证明。
2. `Expectation–Evidence Prompting`（EEP）可从 OpenReview 取得原稿，但状态为 ICLR 2026 withdrawn submission；它仍然形成优先权/想法碰撞，不能当成已同行评审的性能依据。
3. ACL 2026、2026 年 5–7 月 arXiv 页面在当前日期可访问；其结论可能随版本更新变化，正式主张前应固定版本和校验和。
4. “source dependence”在一部分多源 RAG 工作中表示“不同机构资料导致不同答案”，不等于复制/共同上游依赖；本审计不把这类同名异义工作当成 A 的精确先行工作。

## 3. 逐篇输入—计算—输出—碰撞审计

### 3.1 DRNOISE（arXiv:2607.17291）

一级来源：<https://arxiv.org/html/2607.17291>

- **输入**：100 个多跳深度研究任务。干净条件含两条间接真实记录链；噪声条件额外放入一个看似权威、直接给出答案但内容错误的总结文档。
- **计算**：让搜索智能体自主查询、浏览并综合；分析检索到的真/假证据、完整真实路线、搜索次数和最终回答。另测通用核验提示、明确点名攻击的提示及全上下文上界。
- **输出**：准确率、conditional deference、完整路线获取率、搜索次数及错误翻转。GPT-5.4 固定运行从 clean 81/100 降到 noisy 12/100；噪声下平均搜索从 7.1 降到 4.5。在 68 个 clean-correct 翻转中，全部共同检索到真记录和假总结，但只有 10 个完成真实路线。通用 verify 仅将 12 提到 28；点名“直接总结攻击”或强制两条记录引用的提示提升更大，但泄漏攻击类别。
- **A 碰撞**：**benchmark-only**。它精确刻画 A 要解决的失败，却没有复制谱系折叠、独立记录根证书或主动查询算法。
- **B 碰撞**：**benchmark-only**。它支持“直接答案型主张触发额外核验”的需要，但没有义务编译器。
- **审计意义**：v009 的最小实验必须至少报告 conditional deference、真实路线闭合和搜索提前停止，而不能只报最终准确率。attack-aware prompt 只能作为泄漏上界，不能冒充公平主基线。

### 3.2 Argus（arXiv:2605.16217）

一级来源：<https://arxiv.org/html/2605.16217v3>

- **输入**：问题、Searcher 的网页搜索轨迹、原始证据及来源 URL。
- **计算**：Navigator 把证据 URL、主张及支持/冲突关系组织成有向无环图；仅按 URL 做来源去重；对主张判定 supported / contradicted / unverified。图级批量动作会对未验证主张寻找独立佐证，对冲突主张寻找权威消歧，对问题未覆盖区域直接查询。终止由学习到的 Navigator 在图“足够完整”或预算耗尽时决定。
- **输出**：证据图、主张状态、下一批定向查询、终止决策和最终综合。
- **A 碰撞**：**强 partial + component**。证据图、主张闭合、来源多样性、缺口驱动查询和停止都已存在；但 URL 去重不能识别跨 URL 转载、洗稿和共同上游，也没有“添加任意复制后裔不能改变停止决策”的不变量或记录根独立证书。
- **B 碰撞**：**partial**。它会由未验证/冲突/未覆盖图区域产生查询，但没有显式编译“若候选答案为真应在底层记录出现的可执行后果”，也不系统构造竞争答案间的最大区分记录。
- **最近差异**：A 不能只声称“图 + 独立来源 + 定向核验”；这些已经是 Argus 的中心计算。需要把“独立”从 URL/域名层提升为可估计的记录生成根，并以复制不变的停止判定和新根搜索改变行为。

### 3.3 MisKnow-Agent（arXiv:2607.20891）

一级来源：<https://arxiv.org/html/2607.20891v2>

- **输入**：深度研究问题、正常检索语料及一个受控误导文档；论文构造 5,933 个误导实例。
- **计算**：测量误导文档对搜索和综合的影响；防御包括预综合提示（检索信息先视为未验证、结论关键主张需主要/独立可靠证据、评估来源独立性）和后综合核验（抽取重要主张、重新检索独立证据、支持/冲突判定、纠正/限定/删除）。
- **输出**：错误接受率、攻击阶段差异和防御效果；一份误导文档使平均 FCAR 从 0 升到 54.7%，而混合同一语料上的组合防御仍不稳。
- **A 碰撞**：**component**。论文明确使用“来源独立性”和“关键主张需独立证据”的概念，但只是提示级/代理级启发式，无谱系图、复制根折叠和停止证书。
- **B 碰撞**：**partial/component**。后综合防御按主张重新检索和支持/冲突核验，但没有预期后果/连接义务编译及自适应闭合。
- **审计意义**：A 不能把“要求独立来源”作为新贡献；B 也不能把“对答案逐主张再检索”作为新贡献。真实 MisKnow 场景可用来检验方法是否只对 DRNOISE 的模板构造有效。

### 3.4 CaRR（arXiv:2601.06021）

一级来源：<https://arxiv.org/html/2601.06021v1>

- **输入**：具有组合结构的问题、网页检索证据和由问题生成的可验证单跳 rubric；部分实体对策略隐藏。
- **计算**：Citation-aware Rubric Rewards 要求识别隐藏实体、每个 rubric 由引用网页支持，并把已满足 rubric 连接成通向最终答案的完整证据链；用 C-GRPO 训练深度搜索策略。
- **输出**：rubric 满足情况、链完整奖励及训练后的搜索策略。
- **A 碰撞**：**强 partial**。必要子主张全部闭合、引用支持和完整证据链已经是奖励核心；没有来源复制/共同上游建模，也不是推理时可复查的根独立停止证书。
- **B 碰撞**：**partial**。rubric 是问题驱动的证据义务，但来自合成监督结构，不是被轨迹中答案型主张触发的反证后果，也没有竞争答案区分查询。
- **最近差异**：若 B 只是把问题拆成待查事实，CaRR 已占据。若 A 只是要求“全链闭合才能答”，CaRR 也已占据。

### 3.5 GAVEL（Findings of ACL 2026）

一级来源：<https://aclanthology.org/2026.findings-acl.1789/>；PDF：<https://aclanthology.org/2026.findings-acl.1789.pdf>

- **输入**：长文生成任务、原子子主张、候选文本和引用证据。
- **计算**：Evidence Contract 要求每个原子子主张绑定到显式句子或表格单元；Scrutinizer 做确定性结构、存在性、引文、重复/冲突和逻辑审计，产生违规清单、缺失证据需求与下一轮强制修正。没有新违规时可提前停止，最多三轮。
- **输出**：带局部证据标签的回答、审计日志、无效引用/缺失证据及修正结果。
- **A 碰撞**：**强 partial/component**。原子主张覆盖、证据契约、缺口驱动迭代和“无新违规即停”已存在；没有来源复制谱系、记录根独立性或复制不变性。
- **B 碰撞**：**component**。缺失证据需求会约束下一轮，但不是从候选主张编译真/假两侧可检验后果，也不选择最能区分竞争答案的记录。
- **最近差异**：A 的“所有必要子主张闭合”不能单独成为新颖点；B 的“义务未完成不能提交”也已被 Evidence Contract 的外形覆盖。只有义务内容和查询计算真正不同才有空间。

### 3.6 CounterRefine（arXiv:2603.16091）

一级来源：<https://arxiv.org/html/2603.16091v3>

- **输入**：问题、一次 RAG 草稿答案 `a0` 与原检索证据。
- **计算**：把 `a0` 当作待测试假设，用 `q`、`q || a0`（及可选 `a0`）进行答案条件化二次检索；获取直接关联候选答案的证据，再做受约束 KEEP / REVISE，附确定性验证器。
- **输出**：保留或修订后的答案及验证结果。
- **A 碰撞**：**component**。有二次核验但几乎没有来源依赖或结构化停止证书。
- **B 碰撞**：**强 partial，接近核心算子碰撞**。直接答案触发候选条件化证据收集和接受/修订已经存在。HotpotQA 消融中只用原问题做第二次检索与完整 CounterRefine 接近，说明“答案条件化”未在所有任务上稳定提供独立收益。
- **最近差异**：B 不能只说“先形成答案，再按答案查证”。只有可执行的记录级后果/连接义务、竞争答案区分目标和显式闭合状态，才可能与其拉开距离。

### 3.7 FIRE（Findings of NAACL 2025）

一级来源 PDF：<https://aclanthology.org/2025.findings-naacl.158.pdf>

- **输入**：待核查原子主张、当前累计证据和搜索轮次。
- **计算**：函数 `f(c,E,k)` 在“有信心给结论”和“生成下一条搜索查询”之间选择；循环网页检索、积累证据，处理重复查询并受最大步数约束。
- **输出**：事实核查结论或下一查询；论文同时优化 LLM 调用与搜索成本。
- **A 碰撞**：**partial/component**。搜索—停止控制骨架和证据累积存在，但停止依据是模型信心/循环控制，不是来源拓扑证书。
- **B 碰撞**：**partial**。根据当前主张与证据生成下一查询已存在，但没有显式预期后果编译、竞争答案和义务闭合。
- **最近差异**：任何 v009 方法都应与 FIRE 做同预算对比；不能把“证据不足则继续搜索”当成贡献。

### 3.8 Chain-of-Verification / CoVe（Findings of ACL 2024；arXiv:2309.11495）

一级来源：<https://arxiv.org/abs/2309.11495>

- **输入**：问题与模型初稿答案。
- **计算**：为草稿规划一组核验问题，独立回答这些问题以降低对原草稿的复制/锚定，再基于核验结果生成修订答案。
- **输出**：核验问题、独立核验回答和最终答案。
- **A 碰撞**：**component**。没有检索来源谱系或停止证书。
- **B 碰撞**：**强 partial**。它已经是“答案触发的核验问题编译器”；独立回答还直接针对锚定风险。原论文不是工具检索型底层记录闭合，也没有自适应选择最区分记录。
- **最近差异**：B 若只输出自然语言核验问题，基本落入 CoVe。需要证明输出的是可执行、带类型和可判定闭合条件的记录义务，而不是提示词换名。

### 3.9 Hypothesis-Conditioned Query Rewriting / HCQR（arXiv:2603.19008）

一级来源：<https://arxiv.org/html/2603.19008>

- **输入**：问题、候选选项和检索前形成的工作假设。
- **计算**：由工作假设推导“若正确应观察到什么”的判别特征与证据，再形成 SUPPORT、DISTINCTION 和 KEY FEATURES 三类查询；检索融合后由答案器决定。
- **输出**：假设条件化查询、检索证据和答案。
- **A 碰撞**：**component**。没有来源复制依赖和停止证书。
- **B 碰撞**：**非常强 partial / 近 exact 的算子级碰撞**。论文明确从假设推导正确时应成立的事实/规则/条件，并检索区分领先替代假设的证据；这正占据 B 的“预期后果 + 竞争答案区分查询”。差异只剩：HCQR 在检索前、选择题、固定三类查询；B 设想在长轨迹中由直接答案主张触发、针对底层记录/连接关系、自适应闭合。
- **裁决影响**：B 的宽表述已不能作为独立研究核。除非义务语言、闭合语义和自适应控制构成可执行的新计算，否则应判为方法家族碰撞。

### 3.10 Expectation–Evidence Prompting / EEP（ICLR 2026 withdrawn submission）

一级来源：OpenReview 论文页/PDF，论坛标识 `023yMrtHQP`。

- **输入**：待判定主张和观察证据。
- **计算**：分别生成“主张为真”和“主张为假”时预期看到的证据，再把实际观察与两侧预期比较，支持核验或弃答。
- **输出**：真/假两侧预期证据、比较和判断。
- **A 碰撞**：**none/component**。不处理来源谱系。
- **B 碰撞**：**算子级 exact**。B 的“若为真底层记录应出现什么”乃至真/假双侧预期在此直接出现；区别只是 EEP 主要是提示级判定，不负责智能体主动检索和长轨迹闭合。其撤稿状态降低证据强度，不消除想法优先权碰撞。
- **裁决影响**：把“expected evidence”本身包装为新颖贡献不可行。

### 3.11 SURE-RAG（arXiv:2605.03534）

一级来源：<https://arxiv.org/html/2605.03534>

- **输入**：问题、候选答案和检索证据集合。
- **计算**：分解主张，做局部 support / refute / neutral 分布，再做集合级覆盖、关系、一致性与不确定性聚合；只在证据足够时允许 Answer，否则 Refuted 或 Insufficient / Abstain。
- **输出**：Supported、Refuted 或 Insufficient 及选择性回答。
- **A 碰撞**：**近邻强 partial**。它已经把“证据充分才准回答”变为集合级可计算证书，包括多跳缺失和未解冲突；但没有复制谱系/独立记录根，也没有主动补证策略。
- **B 碰撞**：**component**。能表示证据缺口，却不编译预期记录和区分查询。
- **最近差异**：A 必须证明来源根依赖让停止判定发生 SURE-RAG 无法表达的改变，而不是在 sufficiency 模型前加一个去重模块。

### 3.12 经典 truth discovery：Dong、Berti-Équille、Srivastava（PVLDB 2009）

一级来源：Xin Luna Dong, Laure Berti-Équille, Divesh Srivastava, *Integrating Conflicting Data: The Role of Source Dependence*, PVLDB 2(1), 2009：<https://www.vldb.org/pvldb/vol2/vldb09-pvldb47.pdf>

- **输入**：多个来源对对象—属性给出的相互冲突值。
- **计算**：以贝叶斯方式估计来源准确率和直接/传递复制依赖；迭代推断真值与来源依赖；降低复制来源的重复票权。
- **输出**：真值概率、来源质量和复制/依赖关系。
- **A 碰撞**：**核心 component exact**。共同上游/复制来源不能被当作独立佐证，这是经典 truth discovery 的中心计算；A 不能以“识别复制并折叠票数”单独主张新颖。
- **B 碰撞**：**none**。
- **最近差异**：可存活之处不在依赖建模本身，而在它如何进入工具型智能体的多主张闭合停止证书及下一搜索动作。

### 3.13 经典 source selection 与可靠性感知多源 RAG

一级来源：*Data source selection for information integration in big data era*, Information Sciences, 2019, DOI `10.1016/j.ins.2018.11.029`；RA-RAG（EMNLP 2025）PDF：<https://aclanthology.org/2025.emnlp-main.1738.pdf>

- **输入**：候选来源、覆盖/重叠/成本/可靠性信息，或多源 RAG 的分源文档。
- **计算**：经典 source selection 在成本约束下选择预期提供最多真值/覆盖的来源；RA-RAG 用交叉核查估计来源可靠性，做可靠且相关的来源筛选与加权聚合。
- **输出**：来源子集、加权答案或聚合真值。
- **A 碰撞**：**component**。来源选择、重叠和可靠性加权均非新问题；RA-RAG 没有显式复制谱系，经典 source selection 也不控制长程搜索智能体的停止。
- **B 碰撞**：**none/component**。只提供“下一来源选择”邻近基线。
- **最近差异**：A 的主动动作必须明确选择“新记录根/根独立路径”，并在相同预算下优于可靠性、域名多样性和近重复去重。

### 3.14 复杂主张验证、生成式证据检索与主动核查邻域

代表一级来源：

- *Complex Claim Verification with Evidence Retrieved in the Wild*（arXiv:2305.11859）：<https://arxiv.org/abs/2305.11859>
- *GERE: Generative Evidence Retrieval for Fact Verification*（arXiv:2204.05511）：<https://arxiv.org/abs/2204.05511>
- FIRE 见 3.7。

- **输入**：复杂自然语言主张、开放网页/文档库。
- **计算**：复杂主张分解、粗细粒度检索、面向主张的摘要和最终判定；GERE 生成证据标识并利用多文档/多句依赖。
- **输出**：证据集、子主张判定、最终事实核查结果。
- **A 碰撞**：**component**。证据依赖和复杂主张覆盖有大量先行工作，但通常不建模来源复制根和复制不变停止。
- **B 碰撞**：**component/partial**。分解并检索待核查主张已经成熟；B 只能在“可执行预期记录/反例义务 + 动态闭合”上寻求差异。

### 3.15 Calibrated Selective Fact-Checking via Evidence Chain Evaluation（arXiv:2607.18240）

一级来源：<https://arxiv.org/html/2607.18240>

- **输入**：待核查主张和可调用搜索、学术检索、代码等工具的智能体。
- **计算**：多轮收集证据，保留来源级元数据，模型判断证据链是否充分；最多八轮，允许 uncertain。
- **输出**：结构化 verdict / uncertain、证据链和来源信息。
- **A 碰撞**：**partial baseline**。选择性回答和证据链充分性已存在，但没有解析的复制根证书。
- **B 碰撞**：**component**。会继续搜索弱证据，却没有后果/竞争假设义务编译。
- **审计意义**：该工作应作为“模型自己判断充分性”的强邻近基线，不能把允许弃答当成 A 的贡献。

### 3.16 论证图与主张验证邻域

一级来源：GEAR（ACL 2019）：<https://aclanthology.org/P19-1085/>；*Towards a Framework for Evaluating Explanations in Automated Fact Verification*（LREC-COLING 2024）：<https://aclanthology.org/anthology-files/pdf/lrec/2024.lrec-main.1422.pdf>；CHECKWHY（ACL 2024）：<https://aclanthology.org/2024.acl-long.835.pdf>。

- **输入**：待核查主张、多条证据，或带有因果/多跳关系的复杂主张及解释。
- **计算**：GEAR 在全连接证据图上传播并聚合多证据信息；论证解释框架把论据、支持关系和攻击关系表示为三元组，区分以反驳、削弱、提供理由和累积方式发生的关系；CHECKWHY 把因果主张的支持/反驳证据组织为显式论证结构。
- **输出**：支持/反驳/信息不足判定、证据图或带支持—攻击边的论证解释。
- **A 碰撞**：**component**。证据支持/攻击图、关系传播和链式论证不是空白；但这些边描述语义/论证关系，不描述多个文档是否来自同一记录生成根，也不产生复制不变停止。
- **B 碰撞**：**component/partial**。因果主张的中间论证步骤和反驳边可视为结构化核验义务，但现有工作主要在给定证据上验证/解释，不是长程搜索中由直接答案触发的预期底层记录编译与自适应查询。
- **最近差异**：A 必须把“支持边”与“来源谱系边”严格分开；B 若只生成支持/攻击子论点，则已进入论证挖掘/主张验证的既有空间。

## 4. 交叉碰撞矩阵与最窄可存活差异

| 计算部件 | 已占据代表 | 对 v009 的后果 |
|---|---|---|
| 答案草稿触发核验 | CoVe、CounterRefine | B 不能靠“两阶段/再核验”成立 |
| 从假设生成正确时应观察的证据 | HCQR、EEP | B 的预期后果中心算子已碰撞 |
| 竞争假设区分查询 | HCQR | B 的“最能区分当前与竞争答案”已碰撞 |
| 当前证据不足则生成下一查询 | FIRE、Argus | 继续搜索/主动补证本身不新 |
| 原子主张证据覆盖与闭合 | GAVEL、CaRR、SURE-RAG | A/B 都不能只靠“全部子主张闭合” |
| 证据图与独立佐证 | Argus | A 的图、闭合、定向查询外形已碰撞 |
| 来源复制依赖折扣 | 经典 truth discovery | A 的复制折叠本身已是经典算子 |
| 来源可靠性/选择 | source selection、RA-RAG | A 的“选择更可靠来源”不新 |
| 答案只在证据充分时提交 | SURE-RAG、GAVEL、选择性核查 | 停止证书外形已碰撞 |

### 4.1 B：宽方法核应停止作为独立主张

B 的宽版本由下列已知链条几乎完全覆盖：

`CoVe（草稿→核验问题） + CounterRefine（答案条件化二次检索） + HCQR（假设→预期证据/区分查询） + EEP（真/假两侧预期证据） + FIRE/Argus（查询或停止）`。

因此，“claim-triggered falsification obligation compiler”作为自然语言提示/通用检索规划器，最多是这些工作的拼装或换名。它不应作为 v009 的主方法核继续投入。

唯一残余空间是把义务限制为**可执行的、带类型的底层记录连接义务**，例如把“供应商 X 在日期 t 满足 A∧B”编译为：

1. 身份连接：记录中的实体必须能和 X 唯一连接；
2. 时间连接：有效区间覆盖 t；
3. 关系叶：A、B 各由指定记录类型支持；
4. 反例叶：搜索同一身份/时间窗中的撤销、冲突或缺失记录；
5. 闭合判定：所有必要叶和连接条件可由外部解析器判定，而不是由同一个 LLM 自评。

这仍然高度危险：若义务只是问题分解/程序化事实核查，CaRR、GAVEL、复杂主张验证和程序化事实核查邻域会继续形成碰撞。只有在可执行语义导致 HCQR/CoVe/CounterRefine 无法复现的查询与接受行为，并取得同预算增益时，才可能作为 A 的辅助机制，而不是独立新颖点。

### 4.2 A：条件存活的最窄差异

A 的最窄可辩护版本不是“证据图”“来源多样性”“主张覆盖”或“复制折扣”的任一单项，而是以下联合计算：

> **复制不变的记录根独立停止证书**：为必要主张构建支持—来源谱系图，把转载、改写和共同上游的文档后裔折叠到记录生成根；停止决策只依赖能够闭合主张的根独立支持路径。向语料添加任意数量的同根复制后裔，不得把“不准停止”改变为“准停止”。若证书不闭合，查询策略选择尚未闭合的主张，并优先寻找新的记录生成根或能否定当前同根支持簇的记录。

它至少要满足四个可检验性质：

1. **复制不变性**：重复、转载、跨域洗稿只增加同根后裔时，停止决策不变。
2. **根级独立性**：独立性按记录生成根而非 URL、域名或文本相似度计数。
3. **主张路径闭合**：每个必要子主张都由根独立路径覆盖，而不是总证据数达到阈值。
4. **动作耦合**：不闭合状态直接决定下一查询寻找哪个新根/反例，而不是仅在最终聚合前离线去重。

这仍然是高风险组合创新：Argus + 经典 dependence discovery + GAVEL/SURE-RAG 可能被 Reviewer 视为模块堆叠。必须把“复制不变性”写成行为不变量/验收性质，并证明主动新根搜索在复制扩增反事实中带来仅靠模块串接无法解释的优势。若只是先聚类去重，再运行 Argus，则应杀。

命名上应谨慎使用 `provenance-cut`。除非真的定义并求解图切割（例如移除少数记录生成根后所有支持路径都断裂，或寻找根不相交路径），否则该词容易被审稿人认为是未兑现的图论包装。更稳妥的工作名是 **copy-invariant root-disjoint support certificate**（复制不变的根不相交支持证书）。

## 5. 最强公平基线

主实验至少应覆盖：

1. 原始深度搜索/ReAct 智能体。
2. DRNOISE 的 generic verification prompt。
3. DRNOISE 的 attack-aware 两条记录引用提示，仅作为泄漏上界，不作主要公平基线。
4. FIRE：信心驱动的“回答或下一查询”。
5. Argus 风格：证据图、URL 去重、独立佐证、缺口驱动查询和学习停止。
6. GAVEL 风格：原子主张 Evidence Contract、无新违规停止。
7. SURE-RAG 风格：集合证据充分性与 selective answer / abstain。
8. RA-RAG：可靠性估计、来源筛选和加权聚合。
9. 低成本启发式：唯一 URL 数、唯一域名数、近重复文本聚类、两来源规则、主要记录优先。
10. 若测试 B 辅助模块：CoVe、CounterRefine、HCQR、EEP 风格的真/假预期查询，并严格匹配搜索预算。

最重要的强基线不是弱提示，而是 **Argus + 近重复聚类/域名去重 + primary-record preference**。若 A 不能稳定超过这个组合，方法贡献不成立。

## 6. 最小可跑、最高信息量实验

### 6.1 复制谱系扩增的 DRNOISE 反事实实验

先做 20–30 个任务的 paired counterfactual，不必一开始做大规模训练。每个任务保留同一问题、真实双链和模型配置，只改变假总结的复制谱系：

- `F1`：一个直接错误总结根、一个文档；
- `F1-copy3`：同一错误根的 3 个转载/轻改写后裔；
- `F1-copy8-cross-domain`：同根 8 个跨域洗稿后裔；
- `F2-independent`：两个真正独立撰写、结论相同的错误根；
- clean：无错误总结。

每个条件提供两种来源图：

1. **oracle lineage**：由数据构造记录真实根和复制边，只用于机制上界；
2. **estimated lineage**：仅用智能体实际可见信息，如显式引用/链接、发布时间、标题与正文相似、实体/数值重合来估计；同时报告谱系边 F1 和端到端下降。

待测方法必须使用相同文档集合、检索器、LLM、搜索调用预算和上下文预算。终局评价使用 DRNOISE 的答案金标/真实路线或独立 evaluator，不得使用方法自身证书作为评价依据。

### 6.2 指标

- noisy accuracy 与 clean accuracy；
- conditional deference：clean-correct 中因噪声翻错的比例；
- complete true route acquisition；
- 在真实路线闭合前错误停止的比例；
- 搜索调用、token、延迟和弃答覆盖率；
- **duplication sensitivity**：只添加同根复制后裔时，停止/回答决策改变的概率；
- 根独立路径召回和证书误准许率；
- estimated lineage 的边/簇质量及从 oracle 到 estimated 的性能损失。

核心机制预言：`F1 → F1-copy3 → F1-copy8-cross-domain` 不应提高 A 的准停概率；URL 数、域名数或普通投票基线会受影响。`F2-independent` 则应暴露方法边界：A 只解决复制/Sybil 依赖，不能声称解决多个独立来源共同错误。

### 6.3 最小比较矩阵

第一轮只需四个主方法：

1. URL/domain 去重 + 两来源规则；
2. 语义近重复聚类 + 两簇规则；
3. Argus 风格证据图 + 独立佐证；
4. A：根折叠 + 根不相交闭合 + 新根主动搜索。

如果 A 在 20–30 个 paired tasks 上不能同时降低 conditional deference 和 duplication sensitivity，或只以大量弃答/搜索成本换取改善，应立即停止扩大。

### 6.4 B 残余算子的最小对照（仅在 A 需要时）

把 DRNOISE 的关系模板转成带类型的记录叶和连接义务；比较：

- CoVe 自然语言核验问题；
- CounterRefine 答案条件化检索；
- HCQR SUPPORT / DISTINCTION / KEY FEATURES；
-  typed obligation compiler。

评价义务闭合是否与真实路线一致、区分记录召回、conditional deference、伪义务率和 clean accuracy。若 typed 版本只是在查询文字上更长，或使用了基线不可见的金标 schema/路线，则实验无效。

## 7. 明确 kill 条件

### 7.1 A 的 kill 条件

1. 检出近期论文已同时实现复制谱系折叠、根独立停止和主动新根搜索。
2. 在公平预算下，A 不优于近重复聚类、域名去重、primary-record preference 或 `Argus + 去重`。
3. 只有 oracle lineage 有效；estimated lineage 噪声使 conditional deference 增益消失。
4. 复制不变性靠普遍弃答或显著增加搜索取得，在匹配覆盖率/成本后无收益。
5. A 对 `F2-independent` 同样失败，却把主张越界为普遍抗误导；若只能防复制/Sybil，必须收窄，不得过度外推。
6. “必要子主张”由同一个 LLM 生成并由同一个 LLM 判闭合，无法外部复查，证书变成自我认证。
7. 现实网页没有足够可观察的谱系信号，方法实际依赖隐藏元数据或数据构造标签。
8. 可实现方法等价于“先聚类去重，再运行 Argus/SURE-RAG/GAVEL”，没有新的停止/搜索行为。
9. 方法需要先识别“这是直接错误总结”的攻击类型，泄漏 DRNOISE 构造。
10. clean accuracy、延迟或检索成本恶化到无法支持方法论文价值。

### 7.2 B 的 kill 条件

1. 计算可由 HCQR、EEP、CoVe、CounterRefine 直接复现；仅术语改为 obligation。
2. typed compiler 退化为 CaRR/GAVEL/复杂主张分解的已知 rubric 或程序模板。
3. 同预算下不优于自由文本核验问题/假设条件化查询。
4. 预期后果被错误候选锚定并产生自洽的伪义务；闭合仍由同一模型自判。
5. 编译器使用金标 schema、真实路线或数据生成模板，而基线没有同等信息。
6. 只在 DRNOISE 人工模板有效，在 MisKnow-Agent 的自然文档/主张上失效。
7. 查询数量激增，匹配覆盖率和成本后收益消失。
8. “直接答案型主张”触发器等价于攻击类别泄漏。
9. 把“未搜到预期记录”错误当作反证，造成系统性假阴性。
10. 无法以独立 evaluator 区分“义务编译成功”和“提示写得更长”。

## 8. 非权威建议

1. **B 的通用版本应被杀，不宜继续作为独立方法核。** HCQR 和 EEP 已分别占据“正确时应观察什么/竞争假设区分”和“真/假两侧预期证据”，CoVe 与 CounterRefine 又占据答案触发核验及答案条件化检索。可执行的 typed record-join obligation 最多保留为 A 的辅助机制，并须经过与这些强基线的匹配预算对照。
2. **A 可条件存活，但只能收窄为复制不变的记录根不相交证书及其主动新根搜索。** 图、覆盖、独立来源、复制折扣、充分才回答都分别有直接先行工作。可投稿的增量必须是一个可测试的行为不变量和由此改变的搜索策略，不是模块拼接。
3. **先做 paired counterfactual，不要先训练大模型。** 如果仅添加同根跨域复制就能让 URL/域名/Argus 基线翻转，而 A 在 estimated lineage 下保持决策不变并更常完成真实路线，才有继续投入价值。
4. **Reviewer 最可能的质疑**将是：“Argus + truth-discovery 去重 + GAVEL/SURE-RAG 的自然组合。”回答这一质疑只能靠改变计算的形式化定义、反事实不变量和强组合基线实验，不能靠命名。

当前最窄科学状态可概括为：**B-family saturated；A survives only under a copy-invariance / root-disjointness theorem-like contract and a non-oracle provenance experiment.**

## 9. 一级来源索引

- DRNOISE：<https://arxiv.org/html/2607.17291>
- Argus：<https://arxiv.org/html/2605.16217v3>
- MisKnow-Agent：<https://arxiv.org/html/2607.20891v2>
- CaRR：<https://arxiv.org/html/2601.06021v1>
- GAVEL：<https://aclanthology.org/2026.findings-acl.1789/>；<https://aclanthology.org/2026.findings-acl.1789.pdf>
- CounterRefine：<https://arxiv.org/html/2603.16091v3>
- FIRE：<https://aclanthology.org/2025.findings-naacl.158.pdf>
- CoVe：<https://arxiv.org/abs/2309.11495>
- HCQR：<https://arxiv.org/html/2603.19008>
- SURE-RAG：<https://arxiv.org/html/2605.03534>
- Selective Fact-Checking：<https://arxiv.org/html/2607.18240>
- Complex Claim Verification：<https://arxiv.org/abs/2305.11859>
- GERE：<https://arxiv.org/abs/2204.05511>
- GEAR：<https://aclanthology.org/P19-1085/>
- 论证解释评价框架：<https://aclanthology.org/anthology-files/pdf/lrec/2024.lrec-main.1422.pdf>
- CHECKWHY：<https://aclanthology.org/2024.acl-long.835.pdf>
- Dong et al. 2009 source dependence：<https://www.vldb.org/pvldb/vol2/vldb09-pvldb47.pdf>
- RA-RAG：<https://aclanthology.org/2025.emnlp-main.1738.pdf>
- 经典 source selection：DOI `10.1016/j.ins.2018.11.029`
- EEP：OpenReview forum id `023yMrtHQP`（withdrawn submission；不可当作同行评审性能证据）
