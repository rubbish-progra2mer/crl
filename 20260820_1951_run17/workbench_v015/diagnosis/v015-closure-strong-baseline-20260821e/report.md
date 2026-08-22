# CRL Active Diagnosis Facts

STATUS: ADVISORY_NON_AUTHORITATIVE
FACTS_SHA256: af8014d2c508dae5abf29d226f5e51a60692036bce6808ccfdfdfc2fa1dd7863

> 这是机械事实视图，不是科研裁决。主研究者负责解释矛盾、盲点和高信息量下一步。

- Run: `20260820_1951_run17`
- Version: `v015`
- Indexed ordinary files: 118508
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
- Recall stale indexed sources: 2

## Selection context evidence facts

- 当前最佳候选集合 [PRESENT]: INCUMBENT_SET: EMPTY
CHALLENGERS: EMPTY
SURVIVING_FRONTIER: 冻结 ARE/Gaia2 的仅写过滤器确会合并潜在应用状态或全局调度时间不同的轨迹，但 `READ-EFFECT-CLOSURE-ARE` 已被完整终态和简单任务专用断言结构性吸收，不再是活动方法候选。存活的是两个事实坐标：仅写评价的来源/状态不完备现象，以及一个新暴露的时间评价现象——约 270 秒整体延迟仍获官方成功，可能源于图评判器只检查局部依赖边且在一秒阈值内跳过时间比较。后者尚未证明任务危害、跨场景稳定性或论文级贡献，需正交重开而不能继续包装为读取效果闭包。

CANDIDATE_ADMISSION: READ-EFFECT-CLOSURE-ARE
  TARGET_CLAIM: 在 ARE/Gaia2 的仅写评价投影下，任务内名义读取可改变后续语义或调度状态并被过滤；读取效果闭包能区分这类轨迹，同时合并不改变冻结投影的纯读取插入。
  CONTRIBUTION_COORDINATE: 工具智能体的评价表示、轨迹等价关系与状态效果审计。
  CHANGED_COMPUTATION: 相对仅写过滤器，为名义读取增加冻结语义应用状态及调度器 `offset`/`pause_offset` 的前后差分，只在差分非空时生成效果胶囊；相对完整轨迹删除所有无状态差分的纯读取及其原始文本。
  RESEARCH_ARTIFACT: `candidate_v015.md`；`workbench_v015/audit/run_effect_closure_detector.py`；`workbench_v015/audit/run_are_effect_closure_three_way.py`；`workbench_v015/audit/run_gaia2_local_effect_trace_panel.py`；`workbench_v015/audit/run_gaia2_local_effect_trace_admission.py`；`workbench_v015/audit/run_gaia2_natural_counterfactual_pairs.py`。
  STRONGEST_CONSTRUCTIVE_BASELINE: 官方仅写轨迹、完整原始轨迹、完整终态/代理状态、任务专用完整状态断言。
  FATAL_UNCERTAINTY: 尚未证明代表性官方受评轨迹中存在足量且任务相关的仅写等价碰撞，也未证明通用语义投影不会退化为昂贵完整状态或遗漏隐藏外部状态。
  REVERSAL_TEST: 若预冻结独立受评轨迹对不能达到奖励合同阈值，或完整终态/代理状态公平基线以不更高成本吸收同一能力，则降级或退出候选；若自然受评轨迹几乎无任务相关碰撞，则杀死论文级评价贡献但保留源码缺陷事实。
  DISPOSITION: KILLED_BY_STRONG_BASELINE；两个冻结预言补全反事实对中，完整终态与简单任务专用断言均吸收效果闭包的有效果/纯读取区分；保留现象但停止方法扩展。

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
  EXECUTION_DISPOSITION: NOT_SCALED；50+50 阈值未被冒充为已执行，因更早的强基线结构性退出条件已触发。

EVIDENCE_ROLE: READ-EFFECT-CLOSURE-ARE
  DEVELOPMENT_EVIDENCE: workbench_v015/audit/are_judge_collision.json；workbench_v015/audit/are_city_rate_limit_collision.json；workbench_v015/audit/effect_closure_detector.json；workbench_v015/audit/are_effect_closure_three_way.json；workbench_v015/audit/gaia2_task_read_opportunities.json；workbench_v015/audit/gaia2_local_effect_trace_panel.json
  ADMISSION_EVIDENCE: INSUFFICIENT；workbench_v015/audit/gaia2_local_effect_trace_admission.json
  ADMISSION_LIMITATION: 与开发任务身份零重叠并换用第二模型，但没有官方评判、反事实对标签或预设规模，只是独立低保真筛查。
  REJECTION_EVIDENCE: workbench_v015/audit/gaia2_natural_counterfactual_pairs.json
- 新增正向证据 [PRESENT]: - `workbench_v015/audit/are_judge_collision.json` 与 `workbench_v015/audit/are_city_rate_limit_collision.json` 给出两个官方脚本化评判碰撞：被删除读取分别改变后续出租车世界与城市调用可行性，而成功写轨迹和官方成功结果保持相同。
- `workbench_v015/audit/are_effect_closure_three_way.json` 实际构造官方仅写、完整原始轨迹和读取效果闭包三种表示；完整轨迹过度区分纯读取，闭包在受控三世界中保持纯读取等价并分离有效果读取。
- `workbench_v015/audit/gaia2_task_read_opportunities.json` 精确覆盖五个公开验证配置的 800 个场景，得到 129/800 的保守显式机会分母；严格不解释为调用率或碰撞率。
- `workbench_v015/audit/gaia2_local_effect_trace_panel.json` 的开发面板在 4 场景、15 次真实读取中捕获一次等待效果，并杀死仅应用终态投影；调度器偏移加入后，该读取被正确保留，其余 14 次纯读取不被保留。
- `workbench_v015/audit/gaia2_local_effect_trace_admission.json` 使用任务身份零重叠的第二哈希场景与 Qwen2.5 7B：4 场景、21 次实际读取、8 次闭包改变，覆盖 3/4 场景及城市额度、出租车随机数/报价历史、调度器等待三种机制。六次城市读取虽失败仍消耗 `api_call_count`，一次出租车列表读取和一次等待成功；只支持自然可达性的独立筛查。
- `workbench_v015/nearest_prior_effect_closure.md` 保留 Ghost Tool Calls、Agent Step Value、GroundEval、Proxy State-Based Evaluation 与 ToolSandbox 的组件级边界；一般“首次评价盲点”主张已被禁止，但精确的选择性读取效果胶囊差分尚未被当前材料直接吸收。
- `workbench_v015/audit/gaia2_natural_counterfactual_pairs.json` 绑定当前脚本哈希，在冻结出租车与调度器任务身份上各构造直接、纯读取和有效果读取三世界。两组官方语义写轨迹与成功结果均相同；完整轨迹都误分纯读取，效果闭包都保留纯读取并分离有效果读取。
- 同一反事实审计也给出决定性强基线结果：完整终态与简单任务专用断言在两组中均做出与效果闭包完全相同的有效果/纯读取区分。出租车目标参数来自当前同设置成功调用；等待调用在当前重放未复现，参数只能由冻结面板 `269.999472` 秒调度差分恢复为 `timeout=270`。两条当前完整工具序列均与原独立面板不同，不能声称同设置轨迹稳定。
- 已失效或被杀范围 [PRESENT]: - 宽泛跨基准、“所有读取都有副作用”、静态机会比例等于自然调用率/碰撞率、当前已经改变官方得分或排名、一般“首次发现状态式评价盲点”均已失效或无证据。
- AppWorld 对应 9 个自然任务中的当前歌曲/队列状态创建分支均不可达，不能作为当前自然突变证据。
- 只比较应用调用前后终态的第一版闭包被自然等待轨迹杀死；等待结束后临时超时对象清空，但调度器偏移已经改变。当前实现必须投影调度器偏移。
- 原始事件通用唯一标识符不相等不能用作语义轨迹差异；当前比较排除该仪器噪声。
- 机会分母和两个小模型面板均不能支持代表性、任务必要性、官方碰撞率、得分修正或模型排名主张。
- `READ-EFFECT-CLOSURE-ARE` 相对完整终态/代理状态和任务专用断言的独特论文级差分已被两个直接强基线反事实对杀死；这不等于已执行 50+50 经验阈值，而是其预设强基线退出条件提前触发。
- 相同本地模型、温度和种子不保证完整工具序列重现；不得通过继续采样直到等待再次出现来制造稳定性或调用率。
- 剩余致命不确定性 [PRESENT]: - 约 270 秒整体写轨迹平移获官方成功是预言补全反事实事实，但尚未证明该延迟违反对应任务语义、在明确时间敏感任务上稳定存在，或会改变真实提交得分/排名。
- 需要区分“仅写过滤删除等待读取”和“图评判器时间检查对全局平移不敏感”两个机制；下一版本不得把前者的方法死亡偷换成后者的方法胜利。
- 当前只看到一个时间配置任务身份，且同设置工具序列漂移；跨任务、依赖图形状、平移幅度和显式时间约束的边界未知。
- 公平强基线应包括绝对回合时限、从用户事件起算的路径累计时限和现有逐边相对时间检查；若简单绝对时限完全吸收现象，则新方法坐标同样死亡。
- 下一项最高信息量动作 [PRESENT]: NEXT_HIGH_INFORMATION_ACTION: 关闭读取效果闭包的规模化路径并进入新的科学版本。只用 Run17 冻结本地 Gaia2 时间配置与 ARE 源码，预先选择具有显式时间约束或等待语义的任务及不同依赖图形状；对同一预言写序列施加 0、边界内和明显超界的全局时间平移，同时比较官方逐边检查、绝对回合时限与路径累计时限。若超界平移仍成功且与任务语义冲突，才形成时间评价现象候选；若简单绝对时限已公平吸收或任务并不要求时效，则杀死该坐标并继续正交扩展。
- 策略变化 [PRESENT]: PREFERENCE_UPDATE: NOT_APPLICABLE；当前无可比较 Incumbent/Challenger 对，不能制造四值偏好。
STOP_REPEATING: 停止扩大读取效果检测器、静态读取标记、机会计数、同模型重放票数和 50+50 集合；强基线吸收已经使该方法扩展失去信息价值。
EXPANDED_COORDINATE: v015 已从源码可达性推进到自然任务身份、官方反事实评判和完整终态/任务专用强基线；结果是方法死亡、现象保留，并意外暴露全局时间平移仍成功的新评价现象。
CHANGED_COORDINATE: v015 的读取效果现象、读取前后投影干预和效果胶囊评价载体已经完成结构性反证。下一步改为图评判器的累积时间语义、绝对/路径时限干预和时间敏感任务评价，属于明确的新科学版本边界。

## Candidate preference facts

- INCUMBENT_SET [EMPTY]: UNAVAILABLE (occurrences=1)
- CHALLENGERS [EMPTY]: UNAVAILABLE (occurrences=1)
- Pairwise comparisons: 0
- Candidate admission contracts: 1
- Local reward contracts: 1
- Implementation declarations with self-declared sessions: 0
- Preference updates: 1


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
