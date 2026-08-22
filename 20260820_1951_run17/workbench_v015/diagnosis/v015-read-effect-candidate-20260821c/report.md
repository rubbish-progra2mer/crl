# CRL Active Diagnosis Facts

STATUS: ADVISORY_NON_AUTHORITATIVE
FACTS_SHA256: 1dbb01da8cb14c6ea3d01d1a9506cfcbcd55675fad56a162c91796bd4a1eb2a6

> 这是机械事实视图，不是科研裁决。主研究者负责解释矛盾、盲点和高信息量下一步。

- Run: `20260820_1951_run17`
- Version: `v015`
- Indexed ordinary files: 118500
- Current-version Recorded/Formal attempts: 0
- Comparison files: 0
- Search snapshot files: 0
- Review evaluation files: 0
- Recall FTS: READY（无）
- Recall semantic: DEGRADED（semantic_index_missing）
- Selection context template: READY
- Candidate preference declarations: READY

## Run-wide mechanical facts

- Scientific versions: 15
- Empty current version: False
- Scratch report files: 0
- Recorded attempts: 0
- Formal / Review-support attempts: 10
- Valid Formal / Review-support attempts: 2
- Search snapshots: 3
- Raw search bytes: 3469500
- Compact search report bytes: 25527
- Prior audits: 1
- Classified collision kinds: 1
- Normally unclassified prior audits: 0
- Prior assessment warning audits: 0
- Tail consecutive pre-experiment closures: UNKNOWN
- Tail consecutive prior-collision pre-experiment closures: UNKNOWN
- Experiment binding recovery: PARTIAL
- Run-local subagent-related Markdown summary artifacts: 0
- Native delegation evidence: UNAVAILABLE
- Verified native delegation count: UNKNOWN
- Recall contamination present: False
- Nested repository indexed bytes: 0
- Diagnosis indexed bytes: 0
- Recall stale indexed sources: 0

## Selection context evidence facts

- 当前最佳候选集合 [PRESENT]: INCUMBENT_SET: EMPTY
CHALLENGERS: READ-EFFECT-CLOSURE-ARE
SURVIVING_FRONTIER: 在冻结 ARE/Gaia2 中，官方 `AgentEventFilter` 只保留成功写事件；任务内名义读取或失败读取尝试可改变随机数、报价历史、调用额度或调度器偏移却被删除。存活的窄方法坐标是“读取效果闭包”：只为改变冻结语义应用或调度状态的读取生成紧凑胶囊，在仅写轨迹的过度合并与完整原始轨迹的过度区分之间建立可检验表示。当前无 Incumbent，因为自然可达性虽获独立低保真筛查支持，代表性官方受评碰撞与强状态基线差分仍不足。

CANDIDATE_ADMISSION: READ-EFFECT-CLOSURE-ARE
  TARGET_CLAIM: 在 ARE/Gaia2 的仅写评价投影下，任务内名义读取可改变后续语义或调度状态并被过滤；读取效果闭包能区分这类轨迹，同时合并不改变冻结投影的纯读取插入。
  CONTRIBUTION_COORDINATE: 工具智能体的评价表示、轨迹等价关系与状态效果审计。
  CHANGED_COMPUTATION: 相对仅写过滤器，为名义读取增加冻结语义应用状态及调度器 `offset`/`pause_offset` 的前后差分，只在差分非空时生成效果胶囊；相对完整轨迹删除所有无状态差分的纯读取及其原始文本。
  RESEARCH_ARTIFACT: `candidate_v015.md`；`workbench_v015/audit/run_effect_closure_detector.py`；`workbench_v015/audit/run_are_effect_closure_three_way.py`；`workbench_v015/audit/run_gaia2_local_effect_trace_panel.py`；`workbench_v015/audit/run_gaia2_local_effect_trace_admission.py`。
  STRONGEST_CONSTRUCTIVE_BASELINE: 官方仅写轨迹、完整原始轨迹、完整终态/代理状态、任务专用完整状态断言。
  FATAL_UNCERTAINTY: 尚未证明代表性官方受评轨迹中存在足量且任务相关的仅写等价碰撞，也未证明通用语义投影不会退化为昂贵完整状态或遗漏隐藏外部状态。
  REVERSAL_TEST: 若预冻结独立受评轨迹对不能达到奖励合同阈值，或完整终态/代理状态公平基线以不更高成本吸收同一能力，则降级或退出候选；若自然受评轨迹几乎无任务相关碰撞，则杀死论文级评价贡献但保留源码缺陷事实。

LOCAL_REWARD_CONTRACT: READ-EFFECT-CLOSURE-ARE
  PRIMARY_OBSERVABLE: 预冻结反事实轨迹对上的任务相关等价分类：有效果读取对应被分离，纯读取插入保持合并。
  STRONG_BASELINE: 官方仅写轨迹、完整原始轨迹、完整终态/代理状态、任务专用完整状态断言。
  METRIC_DIRECTION: 有效果对分离召回率越高越好，纯读取等价保持率越高越好，胶囊大小与评判开销越低越好；不求和为总分。
  MINIMUM_MEANINGFUL_DELTA: 在至少 50 个有效果对与 50 个纯读取对、覆盖至少三种机制的预冻结独立集合上，有效果对分离率不低于 90%，纯读取等价保持率不低于 95%，胶囊中位字节量低于完整原始轨迹对应增量的 20%；阈值不得事后下调。
  REPETITIONS_OR_UNCERTAINTY: 至少两个任务或模型隔离切片，并报告分层计数与自助法 95% 置信区间；当前 4+4 场景只用于筛查。
  FAILURE_NEGATIVE_INCONCLUSIVE: 达到样本要求后任一主阈值未达为负结果；样本不足、文件系统缺失、无官方评判或任务相关性未标注为不确定；机械调用失败不得冒充科学负结果。
  EXECUTION_COST: 当前投影和小面板只需本机源码、中央处理器及已安装本地模型；代表性官方提交轨迹或大规模复跑需要授权数据与显著计算，但不训练新模型。
  LOW_FIDELITY_SCOPE: 受控源码重放、一个 800 任务机会分母、两个各 4 场景且无评判器的本地模型面板；不得外推官方得分、排名或跨基准普遍性。
  INDEPENDENT_ADMISSION_CHECK: 冻结一个未参与投影修订、任务和模型均与开发面板隔离的受评反事实轨迹对集合，并由不读取开发标签的第二实现计算闭包；现有独立面板只完成自然调用筛查。
  SCALE_BRIDGE_ASSUMPTION: 公开提交或代表性代理轨迹必须自然包含足量有效果读取，且这些效果会改变任务相关未来状态或写轨迹可达性；机会线索和本地小模型调用不能替代该桥梁。
  MUTATION_ACCEPTANCE_CONDITION: 只有在不改变冻结阈值和独立集合时，提高有效果对分离或纯读取等价保持，并且不退化为完整轨迹/完整状态转储，才接受实现变异。

EVIDENCE_ROLE: READ-EFFECT-CLOSURE-ARE
  DEVELOPMENT_EVIDENCE: `workbench_v015/audit/are_judge_collision.json`；`workbench_v015/audit/are_city_rate_limit_collision.json`；`workbench_v015/audit/effect_closure_detector.json`；`workbench_v015/audit/are_effect_closure_three_way.json`；`workbench_v015/audit/gaia2_task_read_opportunities.json`；`workbench_v015/audit/gaia2_local_effect_trace_panel.json`。
  ADMISSION_EVIDENCE: INSUFFICIENT；`workbench_v015/audit/gaia2_local_effect_trace_admission.json` 与开发任务身份零重叠并换用第二模型，但没有官方评判、反事实对标签或预设规模，只是独立低保真筛查。
- 新增正向证据 [PRESENT]: - `workbench_v015/audit/are_judge_collision.json` 与 `workbench_v015/audit/are_city_rate_limit_collision.json` 给出两个官方脚本化评判碰撞：被删除读取分别改变后续出租车世界与城市调用可行性，而成功写轨迹和官方成功结果保持相同。
- `workbench_v015/audit/are_effect_closure_three_way.json` 实际构造官方仅写、完整原始轨迹和读取效果闭包三种表示；完整轨迹过度区分纯读取，闭包在受控三世界中保持纯读取等价并分离有效果读取。
- `workbench_v015/audit/gaia2_task_read_opportunities.json` 精确覆盖五个公开验证配置的 800 个场景，得到 129/800 的保守显式机会分母；严格不解释为调用率或碰撞率。
- `workbench_v015/audit/gaia2_local_effect_trace_panel.json` 的开发面板在 4 场景、15 次真实读取中捕获一次等待效果，并杀死仅应用终态投影；调度器偏移加入后，该读取被正确保留，其余 14 次纯读取不被保留。
- `workbench_v015/audit/gaia2_local_effect_trace_admission.json` 使用任务身份零重叠的第二哈希场景与 Qwen2.5 7B：4 场景、21 次实际读取、8 次闭包改变，覆盖 3/4 场景及城市额度、出租车随机数/报价历史、调度器等待三种机制。六次城市读取虽失败仍消耗 `api_call_count`，一次出租车列表读取和一次等待成功；只支持自然可达性的独立筛查。
- `workbench_v015/nearest_prior_effect_closure.md` 保留 Ghost Tool Calls、Agent Step Value、GroundEval、Proxy State-Based Evaluation 与 ToolSandbox 的组件级边界；一般“首次评价盲点”主张已被禁止，但精确的选择性读取效果胶囊差分尚未被当前材料直接吸收。
- 已失效或被杀范围 [PRESENT]: - 宽泛跨基准、“所有读取都有副作用”、静态机会比例等于自然调用率/碰撞率、当前已经改变官方得分或排名、一般“首次发现状态式评价盲点”均已失效或无证据。
- AppWorld 对应 9 个自然任务中的当前歌曲/队列状态创建分支均不可达，不能作为当前自然突变证据。
- 只比较应用调用前后终态的第一版闭包被自然等待轨迹杀死；等待结束后临时超时对象清空，但调度器偏移已经改变。当前实现必须投影调度器偏移。
- 原始事件通用唯一标识符不相等不能用作语义轨迹差异；当前比较排除该仪器噪声。
- 机会分母和两个小模型面板均不能支持代表性、任务必要性、官方碰撞率、得分修正或模型排名主张。
- 剩余致命不确定性 [PRESENT]: - 最大风险仍是任务相关性桥梁：现有自然面板没有官方评判，尚未展示自然代理轨迹因被删除读取而产生不同任务结论、得分或写轨迹可达性。
- 语义投影目前依赖可检查的应用内部状态和调度器偏移；隐藏外部服务、跨应用共享资源与不可序列化状态可能造成漏检，完整状态又可能造成成本和隐私退化。
- 独立面板的六次城市效果来自失败的无效邮政编码调用；它们机械消耗额度但未证明对该任务有利或对官方评判有决定性影响。
- 文件系统应用因本地缺少可选依赖而未进入两个面板；两个本地模型、8 个场景和迭代上限均不代表官方提交分布。
- 完整终态/代理状态与任务专用断言尚未在自然反事实对上公平构造，可能完全吸收候选差分。
- 下一项最高信息量动作 [PRESENT]: NEXT_HIGH_INFORMATION_ACTION: 预先冻结一组来自自然执行序列的反事实轨迹对，保持任务与后续写操作不变，只插入或删除已实测的出租车列表、城市额度消耗或等待读取；用官方评判器、完整原始轨迹、完整终态/代理状态和读取效果闭包同时评价。若不能形成任务相关的官方等价碰撞，或强状态基线完全吸收差分，则停止扩大当前方法实现并回到评价现象或正交贡献坐标；若形成碰撞且闭包满足纯读取负控，再扩大到预设 50+50 独立集合。
- 策略变化 [PRESENT]: PREFERENCE_UPDATE: NOT_APPLICABLE；当前无可比较 Incumbent/Challenger 对，不能制造四值偏好。
STOP_REPEATING: 停止继续扩大静态读取标记、把任务线索当调用率、重复同一受控碰撞或用同一模型/任务面板增加票数。
EXPANDED_COORDINATE: 证据坐标已从源码可达性和受控单例，扩展到任务身份与模型隔离的自然工具调用，以及“仅写、完整轨迹、完整状态、选择性效果胶囊”四种评价表示的可区分实验。
CHANGED_COORDINATE: 仍处 v015 的同一现象、干预位置和评价载体内；本次是候选形成、实现修订与高信息量实验推进，不构成新的科学版本边界。

## Candidate preference facts

- INCUMBENT_SET [EMPTY]: UNAVAILABLE (occurrences=1)
- CHALLENGERS [PRESENT]: READ-EFFECT-CLOSURE-ARE (occurrences=1)
- Pairwise comparisons: 0
- Candidate admission contracts: 1
- Local reward contracts: 1
- Implementation declarations with self-declared sessions: 0
- Preference updates: 1
- Advisory codes:
  - declared_run_path_unverified candidate=READ-EFFECT-CLOSURE-ARE
  - declared_run_path_unverified candidate=READ-EFFECT-CLOSURE-ARE


## Latest structured activity version facts

- Structured candidate: latest=v009, versions_since=6
- Recorded: latest=UNAVAILABLE, versions_since=UNAVAILABLE
- Formal: latest=v011, versions_since=4
- Prior Audit: latest=v009, versions_since=6

> 上述版本距离只是原始活动事实，不是科研质量、成熟度或停滞指标。

## Main researcher interpretation prompts

- 当前注意力是否只围绕同一实现或同一证据簇？
- 重复失败是否共享可检验的机制或隐藏前提？
- 哪些假设、基线公平性或评价依据仍未验证？
- 当前负面证据真正杀死的是实现、候选、方法谱系、局部研究盆地，还是整个 Run 边界？
- 所谓正交路线是只做了文献扫描，还是已形成结构不同的问题、失败模式或算子并做了最小高信息量检查？
- 哪个下一步最能减少不确定性，正反结果分别会改变什么？
- 连续方法碰撞时，是否应先验证一个跨模型、任务或种子稳定的现象，再生成新方法？
- 当前碰撞是直接同构、经验吸收、可构造组合、类比约化，还是仅问题已被提出？其杀伤范围是否被夸大？
- 不要从 summary artifact 数量推断原生委派已经发生；若另有平台可核验的真实子智能体任务，其认知任务是否只集中于先行攻击？
- 版本变化是否改变了问题、现象、干预位置、可用信息、机制族、评价载体或贡献形态？
- 候选成熟度是否真的提高，还是只有科研信息增益来自一次真实反证？两者必须分开解释。
- 当前 INCUMBENT_SET 与 CHALLENGERS 是否完整保留了不可比候选，而没有把 INCOMPARABLE 偷换成平局、失败或淘汰？
- INSUFFICIENT_EVIDENCE 是否绑定了能区分候选的下一动作、逆转条件和仍存致命不确定性？
- 本地奖励是否只用于本候选的局部变异与实验设计，并与新颖性、终局和 Delivery 判断隔离？
- 开发证据和准入证据是否只是路径不同，还是确有独立的评价角色？不要从不同路径自动推断科学独立性。
- 想法级偏好或死亡若依赖经验实现，主研究者是否确认同一冻结 Candidate Card 下有两份实际隔离完成的实现及盲保真检查，或有明确且可核验的例外？DECLARED_SESSION 与不同 VERIFIED_ARTIFACT 都不能替代这一科学判断。
- 若已出现连续 5 个实验前关闭，明确停止重复什么动作，并从回溯、正交扩展、现象优先、贡献形态变化或长期推迟的高信息量实验中选择不同动作。
