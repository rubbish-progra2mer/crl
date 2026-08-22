# CRL Contract v3 正式运行规约

## 1. 唯一权威与机器边界

CRL 是交给主 AI 研究者使用的科研环境，不是替代科研判断的自动流水线。它由外置共享论文知识库、Run 内长期记忆、本机实验环境、可选 Codex-native 能力和少量机械脚本组成。

本文是正式 CRL Run 的唯一流程权威。`AGENTS.md` 只负责入口，`CRL_ENVIRONMENT.md` 只记录环境事实，Reviewer 协议和模板只解释各自材料；如有冲突，以本文为准。Codex App 是当前宿主事实，不构成科研模型资格。

机器只硬阻止四类会破坏产品真实性的错误：知识库科学内容污染、跨 Run 或路径越界、正式实验真实性失效、固定 Reviewer 可比性或最终绑定失效。除此之外，可选功能允许明确降级或记录 limitation，不得阻塞 v3 科研。

CRL 不设置 Ready、Commissioning、健康检查、启动测试或自动科研评分 Gate。核心原则是：自由探索，交付收口。

## 2. 产品领域、启动与契约

默认硬领域是：

```text
TEXT_AND_TOOL_LLM_AGENT
文本与工具型大语言模型智能体研究
```

自主 Run 只能在该领域内选题和转向。用户给出领域内方向时，该方向成为 `DIRECTED` Run 的更窄硬边界，不得越界寻找产出。只有这种由用户明确窄方向创建的 `DIRECTED` Run 才可形成 Run-level No-Delivery。默认宽 `TEXT_AND_TOOL_LLM_AGENT` AUTONOMOUS Run 的正常科学终局只有 Delivery；未形成 Delivery 时，只要授权仍有效且不存在不可越过的真实外部边界，就保持 `ACTIVE` 并继续研究。领域外请求不创建 Run。

用户只说“开始运行”时直接创建 Contract v3 新 Run，不要求补充方向，不扫描旧目录。Charter 顶层身份为：

```text
CRL_CONTRACT_VERSION: 3
DEFAULT_DOMAIN: TEXT_AND_TOOL_LLM_AGENT
```

版本号只用于机器兼容与语义识别，不传播到 Hypothesis、Claim、Card 或普通文档，也不增加流程 Gate。Contract v2 Run 保证只读、审计和历史终局解释；不迁移、不恢复、不继续写入。所有新的或继续投入的科研统一创建 v3 Run。

创建 AUTONOMOUS Run 即授权主研究者在 Charter 边界内自主经历多个 `vNNN`，无需逐版本请求用户批准。当前 Run 仍为 `ACTIVE` 时，`advance-version` 只表示有意义的科研转向，不是审批阶段。用户明确指定已有 v3 `DELIVERED` 或 `CONCLUDED_NO_DELIVERY` Run 时，机器核验全部结论历史后推进到下一科学版本；这是终局后的显式兼容恢复，不能被普通自主流程自动调用。既有 No-Delivery 记录包括历史 AUTONOMOUS 记录，均保持原样并继续只读解析、审计；恢复不改变 Run 的 `MODE`，恢复后的 AUTONOMOUS 版本不得再次写入 No-Delivery。`TERMINATED_BY_USER` 永不恢复，普通启动仍只新建 Run。

每次交付目标是一颗具有 CCF-B 论文潜力、方向已充分去风险且值得从方向发现进入扩大验证的研究种子。Seed 不必达到完整论文规模，也不限定为历史上全新的计算原语；可研究的贡献形态包括方法、稳定经验现象、基准/评价、系统能力或理论/分析。主研究者可用非评分的 Contribution Vector 说明相对最近先行新增的 `Problem / Phenomenon`、`Mechanism / Computation`、`Agent-specific Constraint`、`Evaluation / Benchmark`、`Empirical Finding`、`Theory / Analysis` 与 `System Capability`。不要求每一维都新，也不计算总分或机械通过；单纯换 Prompt、表面模块拼装、只换智能体场景的经典算法、弱基线优势、偶然基准缺陷或无稳定证据的故事仍不能成为 Seed。最大的剩余疑问不能仍是“核心代理信号是否基本对应真实目标”。

对默认宽 AUTONOMOUS Run，科学不确定、暂未找到合格方向、没有 sufficiently de-risked Seed、当前没有活动候选、候选耗尽、局部盆地失败、运行较久或多次验证无效，都不构成科学终局，也不得形成 `CONCLUDED_NO_DELIVERY`。只要授权仍有效且不存在不可越过的真实外部边界，Run 必须保持 `ACTIVE`，继续 backtracking、换题、正交 re-expansion 和必要高信息量验证；即使已经经历多轮真实回溯与扩展，主观判断继续投入的预期科研价值较低也不改变该边界。版本数、时长、Token、候选数、检索数或负结果数量不能自动改变写入资格，脚本不计算预期价值。一次 Codex Goal、会话或平台执行窗口只是一次执行 episode；若尚未 Delivery 而要停止当前执行，只能来自用户显式暂停或真实外部施加、已经客观达到的执行边界，并按相应规则保留 Run 状态与 continuation。

Delivery 是正向科学终局：当前 surviving paper-level contribution delta（相对最近先行仍存的论文级贡献差分）已经经受当前资源内最直接、最致命的反证，方向发现阶段已充分去风险，值得进入扩大验证，而不只是把一个局部真实事实写入 Seed。如果主研究者已经明确存在一个实验，同时满足：在当前可访问资源与时间内可实际执行；相对其他下一步具有高信息增益；其失败会使当前论文级差分大幅塌缩，或使方向退化为一般已知现象、最近先行的普通实例；那么主研究者应先继续该实验或完成等价强度的直接反证，不能仅通过缩窄 Claim、改写贡献形态或把更强解释移入“未来工作”来形成 Delivery。Reviewer 指出一个实验本身不自动触发此条件；主研究者必须结合可执行性、信息增益和对论文级差分的实际杀伤作科研判断，脚本不解析也不评分。

如果剩余问题主要是外部有效性、扩大数据/模型/任务覆盖、论文规模的稳健性与系统增强，或需要当前资源之外的新数据、权限、算力、平台或其他条件，则可以交付边界清楚的受限 Seed，并把扩大条件与失败边界如实写明。这个口径要求方向发现阶段的关键不确定性已被处理，不要求完成整篇论文。

贡献形态的探索口径宽于当前正式交付仪器的测量覆盖。使用现有 `CRL-EVAL-1.0` 时，核心贡献只有落实为可执行或可机械核验的研究 artifact，并能由真实 Formal / Review-support 证据测量、进入固定 Reviewer packet、与最终 Seed 和 Decision 一致绑定，才可正式 Delivery。artifact 可以是方法或系统实现、基准/评价协议与 harness、现象的可复现实验/测量/干预程序，或理论/分析的机械核验载体；它不等于“必须发明新算法”。尚无这类载体的纯概念理论或分析仍可作为高价值方向保留和继续研究，但不能绕过当前 implementation、Formal 与固定 Reviewer 体系正式交付。

## 3. 主研究者权力与科研文化

主 AI 研究者负责选题、文献取舍、方法构造、转向、实验设计、实验充分性、失败解释、Reviewer 意见处置和最终结束。脚本不能替代这些判断。

Run 采用自由探索：

- 文献、候选、实现、实验、失败排查和转向没有固定顺序或次数；
- 可选文档、Recall、Diagnosis、Tool Forge、Recorded、检索用途和子 Agent 都不构成交付资格；
- 当前环境允许时，优先选择能否定最大核心不确定性的高信息量实验；
- 交付时才收口到一个 Seed、真实 Formal 支撑、固定三审和主研究者 Decision；
- 交付前实质处理最近工作、真实方法变化、可证伪 Claim、公平基线、替代解释和失败边界，但脚本不解析其科学质量。

Research Subagent 专指 Codex App 原生委派实际创建、在 App 中可检查的独立子智能体任务。SCI / EMP / ADV Reviewer CLI、主线程角色模拟、普通 Python 子进程、仅写一份子智能体 Markdown 或没有真实委派的角色扮演都不算；未发生真实原生委派时不得声称“已使用 Research Subagent”。当至少两个任务边界清楚、可独立执行且并行能显著增加覆盖或可靠性时，主研究者优先考虑原生委派，但不设数量配额或固定组织图。其输出仍是非权威草案或事实材料，不产生第二个科研裁决者；只有主研究者显式采纳后才成为当前候选或论据。Research Subagent 不得读取其他 Run，也不得把材料写回共享知识库。

相对有生命力的候选需要并行认知时，主研究者宜避免把所有子任务都定义成“寻找为什么不能做”。可按实际价值分别考虑：最强直接先行攻击；假设所有已知先行均成立后仍存的真实增量；以及候选与最强可构造组合基线之间的最小区分实验。这只是认知平衡提示，不是固定角色、配额、调度框架或 Planner/Critic/Judge 流程；子智能体会额外消耗模型和工具资源，只用于边界清楚、可独立且能返回压缩结果的任务。

默认遵循反证—转向棘轮。负面证据按实际杀伤范围解释：当前实现、候选、方法核、方法谱系或局部研究盆地。当前候选失败、被公平强基线吸收、最近工作碰撞或 Reviewer 提出致命风险，都不自动推出整个 Run 无交付；一个 Formal 负结果只杀死它实际测量的 Claim、机制或现象范围。`DIRECT_EXACT` 或 `EMPIRICAL_ABSORPTION` 可以杀死对应精确 Claim，`CONSTRUCTIVE_COMPOSITE` 或 `ANALOGICAL_REDUCTION` 只表示相应路线高风险；方法死亡后仍须检查现象、评价机会、智能体特有约束、不同贡献形态或理论问题是否存活。

实验的 `evidence_fidelity` 与科研决策的 `kill_target` 是两个独立维度，不形成线性证据等级。`SCREENING` 用于廉价排雷，`REPRESENTATIVE` 用于与目标模型、任务、数据、种子和环境相符的代表性验证；`kill_target` 可为当前实现、局部经验 Claim、方法核或论文方向。单次实现失败或本地代理模型的 `SCREENING` 默认只杀当前实现或局部经验主张；若要关闭方法核或论文方向，需要代表性验证、第二独立实现或明确结构性反证。数学、逻辑或程序结构反例可直接杀死相应方法核，不因缺少大模型而自动降级；大规模经验实验也不自动杀死理论机制。机器只记录字段并提示高风险组合，不判断解释是否科学充分。

Hypothesis 的 `draft` 与 `active` 保持低摩擦；转入 `falsified`、`prior_collision` 或 `escalated` 时，模式版本 2 追加不可变 decision event，保存 `evidence_fidelity`、`kill_target`、模型/任务/数据/种子/环境范围、独立实现数、结构性反证及 `KILLED / SURVIVES / WHY`。`escalated` 复用现有状态表达需要更高保真资源，不新增等待类状态。模式版本 1 保持可读，不迁移、不回填。

局部盆地耗尽或当前没有活动候选时，默认进入 frontier discovery：backtrack，并寻找结构不同的研究问题、失败现象、机制/干预家族、评价/基准、系统约束或贡献形态，按需 `advance-version`；旧版负结果、实验和 Review 原位保留。文献扫描、改写查询或候选重命名不能冒充真实 re-expansion；同时，跨盆地的文献碰撞也只能按实际杀伤范围解释，不能替代仍有实证价值的现象或评价检查。不建立固定盆地清单、coverage score、候选配额或穷尽证明。

最近先行碰撞不是单一二元信号。主研究者可选用 `DIRECT_EXACT`（问题、信息、时机、计算、输出与评价路径基本直接占据）、`EMPIRICAL_ABSORPTION`（公平同信息/工具/预算实验被强基线追平或超过）、`CONSTRUCTIVE_COMPOSITE`（多个已知组件可具体组合）、`ANALOGICAL_REDUCTION`（与经典或跨领域计算范式类比）、`PROBLEM_OCCUPIED_METHOD_OPEN`（问题已提出但方法仍开放）和 `METHOD_KILLED_PHENOMENON_SURVIVES`（方法死亡而现象仍存）记录证据性质。前两类可直接杀伤相应新颖性主张或方法核；可构造组合与类比约化只表示高风险，不能由脚本或措辞自动终止候选，主研究者仍需检查智能体特有可观测性、约束、适配、现象、评价、系统要求及实际组合强基线。字段可缺失，自由笔记继续有效，不新增候选状态机或新颖性分数。

当连续候选主要被最近先行、经典类比或强组合基线吸收，且没有值得实现的差异时，应考虑暂时从 method-first 转为 phenomenon-first：先在公开可运行环境中确认失败是否稳定、可重复、跨模型/任务/种子存在、具有实际影响、未被当前指标正确观察且强基线仍无法解决，再用最小干预区分机制解释。现象成立后再决定是否需要新方法；不建设现象引擎、数据库或额外流程 Gate。

## 4. Run 隔离、生命周期与文件

产品根固定为 `D:\Desktop\crl`，Run 是其直接子目录：

```text
YYYYMMDD_HHMM_runNN
```

不同 Run 完全隔离，只共享外部论文知识库。禁止读取其他 Run 的 Candidate、Seed、实现、实验、Recall、Diagnosis、Decision、Memory、Ledger、失败记录、Reviewer 报告或终局文件。

所有正式操作先绑定产品根与 Run，拒绝非法名称、非直接子目录、符号链接、Junction、其他重解析点、错误编码、错误 Contract，以及身份、版本和状态不一致。绑定后每次正式读取仍重新检查完整路径链。

生命周期状态只描述客观写入资格：`ACTIVE`、`PAUSED_BY_USER`、`DELIVERED`、`CONCLUDED_NO_DELIVERY`、`TERMINATED_BY_USER`。`ACTIVE` 可以跨越多个 Goal、会话或平台执行窗口持续存在；执行窗口结束而科学 frontier 尚存时保持 `ACTIVE`，不新增 handoff 状态。新形成的 `CONCLUDED_NO_DELIVERY` 只属于 `DIRECTED` Run；默认宽 AUTONOMOUS Run 的正常科学终局只有 Delivery。已有历史 No-Delivery（包括 AUTONOMOUS）继续兼容读取和审计，用户明确指定后可按现有兼容恢复推进下一科学版本；恢复不改变 `MODE`，恢复后的 AUTONOMOUS 版本不得再次形成 No-Delivery。暂停只由用户显式产生并由用户显式恢复，永久终止不可恢复。脚本不从自然语言猜测终局。

`vNNN` 是有意义的科学搜索时期或转向边界，不是想法计数器、每次文字编辑，也不是终局。一个版本内允许多个 Hypothesis、候选修订、最近先行攻击、杀手实验、基线增强、机制修复和子智能体检查。只有研究问题、失败现象、干预位置、可用信息、机制家族、评价载体或贡献形态等重要科研坐标明显改变时才适合 `advance-version`；仅一个候选死亡、新增一篇先行、改参数/基线、增加实验或修订同一机制不要求推进版本。在同一问题、现象、机制、干预和评价载体内继续执行尚未解决的高信息量 killer experiment，仍属于当前科学版本。`advance-version --transition-file` 接受 UTF-8/LF JSON 对象，只机械要求 `CHANGED_COORDINATE`、`SURVIVING_FRONTIER`、`NEXT_HIGH_INFORMATION_ACTION` 三段自由文本及可选 `RESOURCE_NEEDED`，并把下一版本 continuation 与 Status、Ledger 原子提交；它不判断坐标改变是否科学成立。当前版本可按需使用 `problem`、`research_map`、`nearest_prior`、`candidate`、`evidence_packet`、`selection_context`、`memory`、`hypothesis_portfolio`、`failure_attribution`、`workbench`、`implementation`、实验计划与结果等材料。

### 4.1 候选集合、证据增长与收敛

完整历史候选档案继续由当前 Run 内既有 Candidate、Hypothesis 模式版本 2、Prior Audit、实验和失败材料保存，不迁移、不删除且不设数量上限。当前活动注意力另分为 `INCUMBENT_SET` 与 `CHALLENGERS`：前者是当前证据下非支配、最值得继续投资的一个或多个候选，后者是正在尝试超过、分裂或补充 Incumbent 的活动候选；历史已关闭、停放或仅作线索的候选不得混入活动集合。活动集合同样不设固定数量上限；集合过大时由主研究者压缩当前比较注意力，不删除历史档案。

候选的唯一比较语义是四值偏好关系，不是全局分数：

```text
Prefer(A, B | E) =
A_PREFERRED
B_PREFERRED
INCOMPARABLE
INSUFFICIENT_EVIDENCE
```

其中 `E` 是当前可追溯的文献、实现、实验、公平强基线和扩大风险证据。`A_PREFERRED` 表示 A 在至少一个可比较维度上取得新的可追溯证据优势，且没有引入同等或更严重的新致命不确定性；`B_PREFERRED` 与之对称。`INCOMPARABLE` 表示二者位于不同贡献坐标并各有当前不可替代的存活优势，必须保留二者，不得偷换成平局、失败或淘汰。`INSUFFICIENT_EVIDENCE` 表示现有证据无法区分，必须指定一项最可能改变偏好结论的区分动作，不能凭直觉选胜者。

语言更流畅、叙事更完整、模型或子智能体主观偏爱、候选更新、版本推进、文献数量增加、模块更多、尚未构造的组件组合、未匹配信息/工具/预算的弱基线或单次偶然高分，都不能产生 Preferred。`CONSTRUCTIVE_COMPOSITE` 与 `ANALOGICAL_REDUCTION` 只形成高风险判断；`DIRECT_EXACT` 与公平的 `EMPIRICAL_ABSORPTION` 可杀伤相应精确贡献差分，但仍须按实际范围解释。不得把新颖性、性能、成本和可行性求和为全局 idea 分数。

Challenger 获得实质资源前，应明确准备在哪个证据维度超过哪个 Incumbent；只有形成相应 Preferred 后才可替换。Incomparable 时保留二者，Insufficient Evidence 时执行区分动作。Incumbent 退出时，主研究者必须指出新增了什么可追溯证据、实际杀死的是实现/局部主张/方法核心/论文方向，以及仍存贡献；已有组件或局部先行不得自动解释为整条现象、评价或系统贡献死亡。Incumbent 可以为空，但必须说明为什么为空，以及下一扩张真实改变了问题、现象、机制、干预位置、可用信息、评价载体或贡献形态中的哪个科研坐标。

在同一科学坐标内继续修改候选、实现、基线和实验时反复修订当前 `selection_context_vNNN.md`，不推进版本。固定 Review 的 reading list 一旦锁定该文件，当前版本不再修改它。该文件仍只使用既有六项短模板，不新增 Run 文件类型或 JSON 模式；“当前最佳候选集合”可含一个或多个成对比较块：

```markdown
## 当前最佳候选集合

INCUMBENT_SET: <一个或多个候选标识；无则 EMPTY；未知则 UNKNOWN>
CHALLENGERS: <一个或多个候选标识；无则 EMPTY；证据不足则 INSUFFICIENT>

PAIRWISE_COMPARISON:
  PAIR: <A> | <B>
  VERDICT: A_PREFERRED | B_PREFERRED | INCOMPARABLE | INSUFFICIENT_EVIDENCE
  DECISIVE_EVIDENCE: <Run-local 路径或明确文献事实>
  A_SURVIVING_ADVANTAGES: <A 仍存优势>
  B_SURVIVING_ADVANTAGES: <B 仍存优势>
  SURVIVING_FATAL_UNCERTAINTIES: <仍存致命不确定性>
  REVERSAL_CONDITION: <什么新证据会改变结论>
  NEXT_DISCRIMINATING_ACTION: <可能结果及各结果如何改变偏好>

## 新增正向证据

新增实现、实验、强基线、先行差分及对应路径。

## 已失效或被杀范围

只记录证据实际杀死的实现、局部主张、方法核心或论文方向。

## 剩余致命不确定性

当前最可能使论文级贡献崩塌的问题。

## 下一项最高信息量动作

必须直接处理一个剩余致命不确定性。

## 策略变化

PREFERENCE_UPDATE:
  ACTION_ID: <已声明高信息量动作标识>
  AFFECTED_PAIR: <A> | <B>
  VERDICT_BEFORE: <四值之一>
  VERDICT_AFTER: <四值之一>
  FATAL_UNCERTAINTY_REDUCED: YES | NO
  EVIDENCE_PATHS: <可追溯路径>
  STOP_REPEATING: <停止重复的动作>
  EXPANDED_COORDINATE: <真实改变的科研坐标>
```

`DECISIVE_EVIDENCE` 必须引用 Run-local 路径或明确文献事实；`REVERSAL_CONDITION` 必须说明会改变结论的新证据；`NEXT_DISCRIMINATING_ACTION` 必须同时声明可能结果及其对偏好的影响。字段不适用时显式写 `NOT_APPLICABLE`，证据不足写 `INSUFFICIENT`，缺失写 `UNAVAILABLE`，未知写 `UNKNOWN`，不得由模型补猜。Diagnosis 对重复结构字段保留每次出现和次数，完全相同重复也发 advisory；同一块内互相冲突的 Verdict、候选合同、奖励合同、证据角色、实现声明或 `PREFERENCE_UPDATE` 按 `AMBIGUOUS`/`UNKNOWN` 披露，不取最后值，也不用于停滞判断。全部 `PAIRWISE_COMPARISON` 按无序候选对归一化；Pair 反向书写时，`A_PREFERRED`/`B_PREFERRED` 先换算为实际候选身份。同一无序候选对声明不同实际四值结果时，该组所有比较均为 `AMBIGUOUS`，不得产生机械胜者、实现彩票风险或其他机械推断；相同实际结果的重复块完整保留并发 advisory。只有 Pair、Verdict、`DECISIVE_EVIDENCE`、`SURVIVING_FATAL_UNCERTAINTIES`、`REVERSAL_CONDITION` 与 `NEXT_DISCRIMINATING_ACTION` 均可解析，且疑似 Run-local 决定性证据没有 `UNVERIFIED` 项时，`A_PREFERRED`/`B_PREFERRED` 才可产生机械可用胜者；否则保留 declared Verdict，但比较为 `UNKNOWN` 且胜者为空。重复 `INCUMBENT_SET` 或 `CHALLENGERS` 只有内容一致时才保留共同声明，内容冲突时不得合并候选；同一次声明若把 `EMPTY`、`NONE` 或 `NOT_APPLICABLE` 与实际候选标识同时写入，则整次声明为 `AMBIGUOUS` 且不保留候选列表。`DECISIVE_EVIDENCE`、`EVIDENCE_PATHS`、`DEVELOPMENT_EVIDENCE`、`ADMISSION_EVIDENCE` 中看起来像 Run-local 路径的值必须机械核验 Run 边界、存在性和普通文件身份；失败显示 `UNVERIFIED` 并发 advisory，普通 DOI、arXiv 与明确文献事实仍只作为 declared text。含 `UNVERIFIED EVIDENCE_PATHS` 的 `PREFERENCE_UPDATE` 为 `UNKNOWN` 且不可参与停滞判断；同一 `ACTION_ID` 与同一归一化 `AFFECTED_PAIR` 的冲突重复更新整组为 `AMBIGUOUS`。`PREFERENCE_UPDATE` 可重复；`EXPANDED_COORDINATE` 只能写真实科研坐标变化，查询改写和候选重命名不算扩张。

一段构想只有明确 `TARGET_CLAIM`、`CONTRIBUTION_COORDINATE`、`CHANGED_COMPUTATION`、`RESEARCH_ARTIFACT`、`STRONGEST_CONSTRUCTIVE_BASELINE`、`FATAL_UNCERTAINTY` 与 `REVERSAL_TEST` 后，才可进入 Incumbent 或 Challenger；否则只能作为探索线索保留。`TARGET_CLAIM` 必须可观察、实验或机械核验；`CHANGED_COMPUTATION` 必须说明相对最近强基线真正新增、删除或重排的计算；`RESEARCH_ARTIFACT` 必须说明本地执行或机械核验载体；最强可构造基线应尽量实际构造；致命不确定性应指向最可能使论文级差分崩塌的问题；反转测试应说明退出、降级、修订或超过 Incumbent 的条件。运行模板用 `CANDIDATE_ADMISSION: <candidate-id>` 将这七个字段绑定到活动候选，不把它变成新模式或 Gate。

每个准备进入实现或系统实验迭代的候选，必须在同一 selection context 中用 `LOCAL_REWARD_CONTRACT: <candidate-id>` 声明自己的 `PRIMARY_OBSERVABLE`、`STRONG_BASELINE`、`METRIC_DIRECTION`、`MINIMUM_MEANINGFUL_DELTA`、`REPETITIONS_OR_UNCERTAINTY`、`FAILURE_NEGATIVE_INCONCLUSIVE`、`EXECUTION_COST`、`LOW_FIDELITY_SCOPE`、`INDEPENDENT_ADMISSION_CHECK`、`SCALE_BRIDGE_ASSUMPTION` 与 `MUTATION_ACCEPTANCE_CONDITION`。局部奖励只用于同一候选内部的实现变异、实验排序和资源分配；不同贡献形态不共享总奖励，新颖性、论文意义、候选终局和 Delivery 不得由它自动决定。机械失败与科学负结果分开，未达到预设最小差异时不得事后降阈值保护候选，低保真结果未经校准不得解释为扩大成功概率。Reward calibration 继续保持离线、非权威、非 Gate，不接入正式候选状态或终局。

开发证据与准入证据必须分开声明。`DEVELOPMENT_EVIDENCE` 可用于发现问题、修复实现和选择下一变异；`ADMISSION_EVIDENCE` 用于宣布 Challenger 优于 Incumbent。同一证据可以帮助理解候选，但不能无限次同时承担修改与证明修改有效的职责。替换 Incumbent 前，至少需要一项未直接参与本次修订设计的检查，例如新任务、新模型、新数据切片、新随机种子、预先冻结反例、未用于调试的强基线、由主研究者实际隔离并重新完成的实现，或评价依据独立的机械检查；完全相同的开发样本反复重跑不是独立准入。不同声明、来源路径或文件哈希只证明相应文本、路径或字节不同，不由机器自动认证科学独立性。

Implementation Lottery（实现彩票）按现有 Hypothesis 模式版本 2 与实验语义处理，不新增状态。单次实现失败默认只杀当前实现或局部经验主张；同一研究工件的重复运行只测量运行噪声，不能代替独立实现。当经验结果将用于想法级偏好、方法核关闭、研究分支分配或长期 Run-local 科研记忆时，原则上需要至少两个由主研究者实际隔离、依据同一冻结 Candidate Card 独立完成的实现，并各有不看实验结果的实现忠实度检查。`FRESH_SESSION_ID` 只记录为 `DECLARED_SESSION` 自报标识，不是已验证独立会话；Diagnosis 对实现工件、冻结 Candidate Card 和忠实度文件记录 SHA-256，`VERIFIED_ARTIFACT` 只表示 Run 边界内普通文件及字节身份已经机械核验。不同路径但相同 SHA-256 的实现工件只能计一次；不同 SHA-256 也不能由脚本认证真实会话隔离、过程独立或科学独立性。机械唯一实现或明确结构性反例可以例外，但须写明理由与证据路径。方法核或论文方向的经验性关闭需要两个经主研究者确认科学独立的实现均在相应范围失败、公平 `REPRESENTATIVE` 强基线吸收或可机械核验结构反例之一；主要依赖性能的正向 Preferred 也不得由一个高方差实现决定。best-of-N 最佳工件成绩不代表想法的平均可靠性，交付最佳工件与判断想法是否值得继续是不同问题。

纯文字润色、增加同类论文、候选重命名、重复已有否定理由和版本增长都不算候选质量增长。只有以下变化才是正向证据增量：得到新的可运行研究实现；自然数据上的现象从未验证变为 Screening 支持或 Representative 支持；在匹配信息、工具和预算的强基线后仍存活；结构化最近先行审计明确保留新的贡献差分；一个可能杀死论文方向的关键不确定性被实验处理；或本地结果与扩大实验之间形成可执行桥梁。科研信息增益与候选成熟度必须分开记录：真实反证杀死候选可以增加信息，但不能伪装成“可投资候选质量提高”。

比较最佳候选集合前后时使用非评分证据向量：问题或现象是否真实；最近先行后还剩什么贡献；关键计算是否明确改变；是否存在可运行实现；本地实验处于主张、Screening、Representative 还是独立支持；是否经受匹配强基线；本地结果能否合理桥接扩大实验；最大致命不确定性是否减少。不求和，不换算成 0—100 分。

发现证据向量没有改善且动作模式重复时，主研究者立即改用一种不同动作：回溯、正交扩展、现象优先、改变贡献形态，或执行被长期推迟的高信息量实验。停滞不由版本数、时长、Token、候选数或检索数判断。Diagnosis 先按每个 `ACTION_ID` 的最后出现位置排序，再选择最近三个不同动作；同一动作包含多组成对更新时仍只计一个动作。若这三个动作的所有可解释更新既没有改变任何四值 Pairwise Verdict，也没有减少任何致命不确定性，Diagnosis 输出显著的 `PREFERENCE_STAGNATION_WARNING`。含冲突重复字段、同一动作与归一化 Pair 的冲突重复结果，或含 `UNVERIFIED EVIDENCE_PATHS` 的 `PREFERENCE_UPDATE` 为 `AMBIGUOUS`/`UNKNOWN`，不得作为停滞证据，也不能凭自报 Verdict 变化伪造进展；它位于最近动作窗口时只能使该次机械判断为 `UNKNOWN`，不得越过后误报停滞。主研究者必须更新 selection context、写明 `STOP_REPEATING`、扩大至少一个真实科研坐标、选择新的区分动作，并让 Run 保持 `ACTIVE`。脚本不得自动推进版本、切换候选、暂停、终止或形成 No-Delivery。

模式版本 2 的决策历史中，若尾部连续 5 个候选转入 `falsified` 或 `prior_collision`，且整个当前 Run 没有任何以该假设标识绑定的实验规格、Recorded 或 Formal，必须调用 Active Diagnosis，解释重复模式，更新六项 selection context，明确停止重复什么动作并立即改变研究策略；该预警不自动形成 No-Delivery，不授权脚本改变候选状态。

主研究者可在确有比较价值时使用 Codex App 原生子智能体盲审同格式 A/B 证据包，用于发现遗漏基线、替代解释、实现忠实度或未决证据；材料可保存在 `workbench_vNNN/quality_reviews/<quality-review-id>/`。子智能体的主观偏好或多数票不能形成四值 Preferred，也不得通过持续加票强行制造胜者；只有它们指出并由主研究者核验、采纳的可追溯新证据才能进入 Pairwise Comparison。`adoption.md` 如实说明采纳、部分采纳或拒绝，子智能体始终不能自动改变候选、认证新颖性或形成 Delivery。

唯一最终科学正文是 `seed_vNNN.md`。Seed 应自足说明问题、文献定位、真实计算变化、Claim、实验依据、边界和扩大价值；章节形式仍由主研究者决定。

## 5. 长期回忆与 Active Diagnosis

Run Recall 是可删除、可重建的派生索引，不是权威状态。FTS5 是稳定底座；调用者明确请求且现有向量能力可用时，可构建 Run-local hybrid semantic recall。向量不可用时必须明确报告 `DEGRADED` 并完整回退 FTS，不能假装语义检索成功。

Recall 是 research-owned memory，不是 Run 目录全文爬虫。它索引 Run 控制文件、研究笔记与正式研究文档、Prior Audit 报告、Research Subagent 摘要、Scratch/Recorded/Formal 的研究者报告、实现源码及小型结构化结果，同时记录来源路径、大小和 SHA-256。它必须拒绝重解析点，默认排除 `.env`、credentials、private key、token dump 等敏感路径，以及任意嵌套 `.git` 标记所属的完整代码仓库子树、`workbench_v*/diagnosis/**`、`external/`、环境、依赖、vendor、ground truth、hidden test、reference solution 与完整 raw search `result.json`；排除不限制主研究者按路径直接读取。完整搜索结果继续作为可审计 artifact 保存，只索引 request、紧凑 report 和适量 metadata。查询时若源文件缺失或哈希变化，不再返回旧 chunk；rebuild 移除陈旧条目，不建设 watcher。派生索引位于 Run 的 `.crl/recall/`，可删除重建，不得跨 Run 查询或作为科学事实来源。

仓库级 `.agents/skills/crl-active-diagnosis/SKILL.md` 只提醒主研究者在大量阅读后、想法重复、连续实验失败、候选收敛、准备 Review 或长时间恢复时按需调用 Diagnosis。显式诊断前优先刷新一次 FTS-only Recall；刷新失败仍继续，并将 FTS 状态以 `READY` 或 `UNAVAILABLE` 加原因结构化披露，semantic 状态另行报告。Diagnosis 同时呈现 current-version 与 Run-wide 的可追溯事实，使用正式完整性校验区分有效 Formal/Review-support，显示 selection context 六项事实、Incumbent/Challenger、每组成对比较的四值 Verdict、决定性证据、反转条件、仍存致命不确定性、区分动作、候选准入与局部奖励声明、开发/准入证据声明及其路径核验、实现声明中的 `DECLARED_SESSION`、实现工件/冻结 Candidate Card/忠实度文件的 `VERIFIED_ARTIFACT` 与 SHA-256、显式实现彩票例外、Preference Update 变化，以及每个结构化候选的实验规格/Recorded/Formal 绑定、模式版本 2 决策事件的尾部连续实验前关闭、结构化检索来源、Recall 来源所有权与污染字节、空当前版本和少数可机械识别的语义越权组合。重复结构字段保留次数，冲突块报告 `AMBIGUOUS`/`UNKNOWN`；不存在、越界或非普通文件的疑似 Run-local 证据路径报告 `UNVERIFIED`，普通文献事实保留为 declared text。旧六项自由文本、模式版本 1、缺失字段或不可恢复绑定明确报告 `UNAVAILABLE` 或 `UNKNOWN`，不得猜测。距离最近候选、Recorded、Formal 和 Prior Audit 的版本数只是低显著度原始活动事实，不是科研质量指标。Diagnosis 不记录机器代码身份或聚合指纹；它只发 facts-only advisory，包括 `PREFERENCE_STAGNATION_WARNING` 和单工件想法级判断风险。`DECLARED_SESSION` 与 `VERIFIED_ARTIFACT` 都不认证真实会话隔离或科学独立性；强模型负责解释杀伤范围、候选成熟度、科研信息增益、现象价值和正交探索真实性。Diagnosis 不轮询、不改状态、不形成 Gate，不自动选择、淘汰、推进版本或结束 Run。

## 6. 知识库、PDF 与用途检索

共享知识库固定在 `D:\Desktop\crl\knowledge_base`。论文、PDF、Evidence、Cards、`knowledge.sqlite`、Passage 和 vector index 是冻结的科学内容，只读投入正式 Run。Run 的候选、实验、Seed、失败记忆、评审和诊断不得回写。

认识论权威顺序是：

```text
论文 PDF、散列与原文核对
→ 可定位 Evidence
→ Paper / Failure / Operator Card
→ Passage、全文、向量或混合排名
```

中央 PDF 解析器先尝试知识库相对路径和有效绝对路径；历史绝对路径失效时，只允许按文件名在中央 `papers/` 下寻找候选，并以论文记录 SHA-256 验证。缺失、多个候选或哈希不符必须失败，不能静默选错文件。知识库记录本身不因路径修复而改写。

purpose-aware retrieval 支持 `problem`、`failure`、`operator`、`prior`、`measurement` 五种用途，以不同入口顺序组织 Paper、Failure、Operator 与 Passage 事实。`result.json` 保留全部原始路线命中、rank、来源和降级信息；默认 `report.md` 先给跨路线去重的少量代表项，再给路线命中数和降级摘要，需要时再下钻原始结果或 Card / Evidence / PDF。覆盖率不是科研探索覆盖率，排序也不自动宣称研究空白、Novelty、因果机制、候选质量或交付资格。

同一研究盆地通常先做一次 broad purpose-aware map，随后优先 targeted nearest-prior、citation neighborhood 与 Evidence/PDF drill-down，不因每个小假设重复覆盖大部分语料。主上下文优先保留最危险的少量 prior、各自吸收的计算、仍存贡献增量及最具区分力的实验；完整 raw evidence 留在 artifact，不进入长期 Recall 主语料。资源节制追求每次检索和子任务的信息增益，不建立自动预算器。

当最近工作碰撞成为候选淘汰、Reviewer 致命风险、Delivery 或 `DIRECTED` Run-level No-Go 的主要依据时，优先复用现有 Run-local structured Prior Audit 和 citation expansion，把实时来源、最近工作、组件重叠与未解决差异留下可复查记录；这不是所有候选的强制 Gate，也不产生新颖性分数或 oracle。

Prior Audit 先冻结查询、来源、网络响应、候选与 provenance 等 machine-owned 检索事实；nearest prior、collision 类型、组件重合、surviving contribution delta、替代解释和区分实验由主研究者在阅读候选、PDF、Evidence 与实验后写入独立、可继续修订的 researcher assessment。只有先行实际参与候选关闭、方法核/论文方向杀伤或重大升级时，才补充 `KILLED / SURVIVES / WHY`；普通检索无需填写。解释变化不得重写或使原始检索快照失效，未分类 Audit 仍是完整有效的事实材料；机器不得要求先分类再检索，也不得据分类自动改变 Candidate、Hypothesis、版本或终局。

知识库维护元数据与科学内容分离。只有 `knowledge_base/evaluation/` 中的 `PRODUCTION_RETRIEVAL_LOCK`、与机器版本直接绑定的检索评测元数据和维护审计报告，可在机器修改完成、真实 KB 全量回归通过后显式重建；必须记录旧值、新值、原因和接受结果，不能借机重建论文、Cards、Passage、数据库或索引。

## 7. 三层实验与工具能力

CRL 区分：

- **Scratch**：`workbench_vNNN/` 内自由试验，无正式契约；
- **Recorded**：低摩擦执行记录，保存命令、stdout/stderr、输入输出、实现身份和可取得的环境事实，可用于探索、分析和 Reviewer 辅助；
- **Formal / Review-support**：由正式运行器记录、可支撑最终核心主张和 Delivery 的真实实验。

实验层级与证据保真度正交：Scratch、Recorded、Formal 描述记录与完整性强度，`SCREENING`、`REPRESENTATIVE` 描述实验对目标模型、任务、数据、种子和环境的代表性。Formal 可以只是 Screening，Recorded 也可以提供有价值的代表性观察；主研究者不得把记录层级冒充证据外推范围。反证 Spec 模式版本 2 保存预期保真度、subject scope 与独立实现策略，旧模式版本 1 保持可读。

Recorded 位于 `experiment_vNNN/recorded/`，不能被交付验证器当成 Formal。Tool Forge 只生成 Run-local helper 模板并提供受 Run 路径约束的原子 JSON/Markdown/CSV 输出接口；它不是任意代码的操作系统沙箱。

Formal attempt 位于 `experiment_vNNN/attempts/attempt-id/`。当前写入器使用 execution schema 8，读取器兼容已有 schema 5、6、7、8；其中 schema 7、8 支持 Spec、Claim、metrics 与完整性绑定。产品规则不永久写死某个 schema 名称。未来等价后继只要保持来源、真实执行、独立评价依据、实现/输入/输出身份、原始 stdout/stderr、结构化指标和可复查性，即可由明确的机器升级纳入 Review-support。

本文及机器字段中的 `implementation` 指本次测量所绑定的可执行或可机械核验研究 artifact，不是“新算法”的同义词。它必须承载 Seed 的核心贡献并参与相应 Formal 测量；只把无关脚本放入 `implementation_vNNN/` 不能使概念主张获得交付资格。

有效 Formal attempt 至少要求：命令与运行器真实成功；绑定当前实现的非空文件清单和 SHA-256；保存精确 Spec、指标、依赖、输入输出、stdout/stderr 与执行身份；至少一个非空证据通道；无超时和密钥污染；交付时实现与执行记录仍一致。正式实验的科学充分性、评价独立性和主张边界由主研究者判断，脚本只核验机械事实。

交付前至少有一次评价标签、终局、失败事实或判定逻辑不由方法自身生成规则直接定义的 Formal / Review-support 核心验证。更换数据域、冻结方法或分离代码不自动构成认识论独立。公平比较要求候选与强基线获得相同信息、工具能力和合理可比预算；这属于科学披露，不由脚本评分。

## 8. 固定 Reviewer 仪器

准备交付或比较 materially changed implementation 时，主研究者使用固定 `CRL-EVAL-1.0`。三个角色是：

- `SCI`：科学问题、最近工作分离、机制和 Claim 校准；
- `EMP`：实验有效性、基线公平、测量可靠性、稳健性和结果强度；
- `ADV`：复现、泄漏/混杂、边界、对抗失败和证据可审计性。

三者固定为 `gpt-5.6-sol`、`xhigh`，角色权重为 35%/40%/25%，各维度 0—4 分并按冻结维度权重聚合。分数用于同一评估器下比较 implementation，不是交付阈值、投票、论文接受概率或绝对质量 oracle。主研究者保留最终裁决权。

每个 Reviewer 必须 fresh、互不可见，读取完全相同的不可变 `packet.md`，且不得主动获得 packet 外科研信息。运行后端使用固定 Codex CLI、独立临时 Codex Home（只复制登录凭据）、空工作目录、read-only、ephemeral、结构化输出、禁用中介服务器和最小环境。协议禁止所有工具、网络、外部读取和继续委派；JSONL 事件中出现任何工具或外部访问事件时，整组三审无效并保留原始结果，不能只凭 Reviewer 自述。

packet 固定有七个逻辑区域；未提供的区域明确写 `NOT PROVIDED`。机器自动附加 Evidence Inventory，列出与当前 implementation 关联的全部 Formal attempts、相关 comparisons，以及当前版本全部 Recorded attempts 的身份、状态、关联与是否进入核心材料。final-delivery packet 还自动附加确定性、限长的 Core Evidence Closure，使 Reviewer 直接看见所选 Formal 的关键 Spec、Claim 和指标值，以及 Seed 显式指标映射的解析结果与未映射数字 advisory；完整代码、日志和 raw JSON 仍留在 artifact。packet 优先使用紧凑摘要、代表性证据及 hash/path，不复制大体量原始 JSON；Reviewer 不必读取所有日志，但必须看见哪些证据存在、哪些被选择、哪些未进入正文。

身份分离为：

```text
implementation_key = 当前 implementation manifest
packet_key = packet 精确字节
measurement_key = implementation_key + packet_key + evaluator definition
```

同一 `measurement_key` 的第一次有效三 Reviewer 测量是不可替换的 `CANONICAL_IMPLEMENTATION_SCORE`；后续完全相同 packet 只作为 `STABILITY_MEASUREMENT`，全部保留并报告方差，永不替换 canonical。无效测量不占 canonical。相同 implementation 更换 packet 会产生新 measurement，并在 implementation 历史中关联披露，不能挑最好的一份冒充唯一结果。

一次 materially changed implementation 对应一次正式 Review。固定 Reviewer 可在最终交付前重复使用，但不得刷分。最终 Decision 必须绑定最终 implementation、最终 packet、该 measurement 的第一次有效 canonical、三份原始报告、Evidence Inventory 和聚合哈希；最终 Delivery 再次计算实现、Seed 和证据清单，禁止用旧实现或旧 packet 的高分覆盖后续变化。

四个冻结校准包 Weak、Medium、Strong、Unfair Baseline Trap 只检验相对尺度：`Strong > Medium > Weak`，Unfair 不高于 Medium，且 EMP/ADV 必须重罚不公平基线与测试真值泄漏。不得为逼近精确分数在看到结果后修改 fixture 或 Prompt。

完整操作与结构化字段见 `CRL_REVIEWER_PROTOCOL.md`。

## 9. Decision、Delivery、No-Go 与终止

主研究者完整阅读三份固定角色意见，在 `decision_vNNN.md` 中独立裁决继续研究或交付；只有 `DIRECTED` Run 可按第 9 节语义裁决 No-Go，宽 AUTONOMOUS Run 未交付时继续研究。Reviewer 分数和意见都没有机械否决权，但不得隐瞒实际评审历史或捏造认可。

Delivery 的机械资格是：

- 当前唯一、非空、UTF-8 无 BOM、LF 的 `seed_vNNN.md`；
- 明确选中至少一个有效且在最终 Review packet 中绑定的 Formal / Review-support attempt；
- Seed 已显式声明的 metric mapping 必须能机械解析且与所引 Formal / comparison 事实一致；未声明 mapping 本身不构成硬拒绝；
- 最终 implementation 与 final-delivery Review 的 manifest 完全一致；
- Evidence Inventory 自 Review 后未变化；
- Decision 绑定最终 measurement 的 canonical 三审和三角色原始报告；
- 无路径、跨 Run、版本、密钥或终局冲突。

这些条件保证 artifact、证据、评审和终局记录的真实性绑定，不自动证明任意贡献已被充分验证，也不替代第 2 节的 AUTONOMOUS Delivery 正向科学终局条件。主研究者还必须确保 Seed 的核心贡献、被测 artifact、Formal 的独立评价依据和 Reviewer 实际看到的材料彼此对应；当前仪器无法覆盖的贡献继续保留为研究方向，而不是改名后交付。一个 Claim 在缩窄后机械真实，不足以绕过一个当前可执行、失败会使论文级剩余贡献差分大幅塌缩的 killer experiment。

首次交付写 `DELIVERY.md`，后续科学版本写 `DELIVERY_vNNN.md`。薄交付记录绑定 Seed、Decision、implementation、packet、measurement、canonical evaluation、聚合、Evidence Inventory、实现 manifest 和 Formal execution 哈希。正式科学内容仍以 Seed 字节为准。

No-Delivery 是只适用于 `DIRECTED` Run 的负向强科学终局，用来表示用户明确给出的窄 Charter 边界与当前资源下已无值得投入的路线。默认宽 AUTONOMOUS Run 不得新形成 No-Delivery，其正常科学终局只有 Delivery；未交付时按本规约保持 `ACTIVE` 并继续探索。既有历史 No-Delivery，包括历史 AUTONOMOUS 记录，仍保持只读解析、审计和用户显式恢复兼容，不迁移、不重写。

`DIRECTED` No-Delivery 正文保持自由表达，不要求 Seed、实验、Review 或固定章节，但必须由明确 Charter 边界内的实际探索、反证和剩余科研价值判断支持，不能由版本数、时长、Token、候选数、检索数、查询互不重复、局部盆地耗尽、一个或多个先行碰撞或单个 Formal 负结果单独支持。脚本核验 Run 身份、版本、终局冲突、秘密、哈希链以及 Charter/Status 的 `MODE: DIRECTED` 一致性，不解析或评分科研理由，也不自动结束 Run。

只有执行边界已经真实发生或客观达到，而 frontier 仍存、主研究者又没有形成科学终局时，才可以结束当前 Goal/会话并让 Run 保持 `ACTIVE`。这类边界包括实际平台或模型额度耗尽、服务当前不可用、权限缺失、明确算力/进程/执行限制已经触发，或下一步必须等待当前不可获得的资源；它们必须是外部施加或可核实的客观事实，不能由主研究者为了方便结束 Goal 自行设定软预算。已运行时长、Token 使用量、候选/版本/检索数量、上下文压缩、主观认为“这一轮已经够久”或预计后续工作很多，单独都不是 `ACTIVE` handoff 理由。

合法 handoff 时，主研究者应在现有 Run 研究材料中留下耐久 continuation：当前科学坐标、已杀内容及其杀伤范围、仍存 frontier、下一项最高信息增益动作、所需资源与关键 artifact 定位，使后继 Goal 能继续；这不是第三种科学终局，也不新增生命周期状态。`DIRECTED` Run 可形成 Delivery 或 No-Delivery；宽 AUTONOMOUS Run 的正常科学终局只有 Delivery。用户显式暂停、真实平台阻塞和上述客观执行边界停止只是执行停止。局部版本转换也不能被当作 Goal 完成。用户明确永久终止时写 `TERMINATED_BY_USER.md`，形成后永不恢复。

终局秘密扫描只硬阻止真实环境密钥、私钥、明确凭据存储/会话缓存/令牌转储及第一方高可信泄漏；第三方源码、模板、测试夹具、原始检索响应和源码中的普通凭据样字段可作为需主研究者解释的 warning，不要求清零，也不得诱导删除、改写或搬移科研现场。终局正文自由说明真实停止理由和正交探索，不按章节检查。

## 10. 脚本权力与明确不建设

脚本可以管理：路径、编码、重解析点、Run 绑定、版本和覆盖保护；Run-local 派生索引；实验真实记录与文件身份；固定 packet、Evidence Inventory、Reviewer 事件和三类键；Decision、终局与哈希链。

脚本不得自动生成最终 Claim、认证 Novelty、判断实验充分性、淘汰候选、结束 Run、解释 Reviewer 科学意见、把分数变成 Delivery Gate，或写回共享论文知识库。可选能力缺失或降级本身不阻塞科研。

当前不建设 Ready/Commissioning、后台服务、定时任务、周期知识库扩充、自动科研评分/淘汰、跨 Run 记忆、自动迁移 v2、复杂科研状态机、额外版本编号、全目录冻结、独立 API Reviewer 服务或第二套运行基础设施。

机器是否有用由真实 Run 的科研质量持续判断，而不是由一份永久验收状态证明。
