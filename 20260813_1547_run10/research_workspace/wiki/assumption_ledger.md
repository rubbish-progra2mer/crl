# Assumption Ledger — 20260813_1547_run10 / v001

## AS-v001-001

- `run_id`: 20260813_1547_run10
- `run_ref_type`: explicit_run_id
- `assumption_id`: AS-v001-001
- `assumption`: 仅依据任务、工具规范和可见轨迹，可以构造至少一类可执行、且不等价于原工具调用的语义关系检查，而不读取测试真值。
- `source`: 主研究者方法推断。
- `used_by`: h-v001-001；HB-003；后续失败模式 FM-v001-001 的可能干预点。
- `risk`: 若错误，语义契约只能退化为同模型自检、静态模式或真值泄漏，方法核失效。
- `how_to_verify`: 对人工可判定的工具任务盲构造检查，测量关系有效率、真值泄漏、故障检出和误拒绝；与同构重试分开。
- `status`: contradicted_for_post_only_entity_relations
- `related evidence`: `ev-p074-missing-schema-true-postcondition`, `ev-p097-behavioral-perturbation`, `ev-p096-shared-misinterpretation`
- `last_updated`: 2026-08-13
- `update_note`: v001 配对 Scratch 中，七个已编译见证只有一个同时通过洁净成功并拒绝静默空操作；四个只证明预先存在实体，两个在洁净执行上误报。该假设若继续，必须改为写前—写后可见差分并允许 `UNKNOWN`，不能沿用单次事后关系。

## AS-v001-002

- `run_id`: 20260813_1547_run10
- `run_ref_type`: explicit_run_id
- `assumption_id`: AS-v001-002
- `assumption`: 非同构的关系检查与原始生成错误足够不共因，因此比同模型反思更少共享误读。
- `source`: 主研究者因果假设。
- `used_by`: h-v001-001 mechanism_claim。
- `risk`: 若共享误读率相同，验证增加成本却不增加认识论独立性。
- `how_to_verify`: 在已知语义故障集上标注原调用与检查的错误相关性，比较同模型反思、重复调用和结构变换检查。
- `status`: unverified
- `related evidence`: `ev-p096-shared-misinterpretation`, `ev-p013-intrinsic-self-correction-degrades`
- `last_updated`: 2026-08-13

## AS-v001-003

- `run_id`: 20260813_1547_run10
- `run_ref_type`: explicit_run_id
- `assumption_id`: AS-v001-003
- `assumption`: 在线可见的下游依赖扇出、动作可逆性与重查成本对一次工具观测错误的终局边际损失具有稳定预测力。
- `source`: 主研究者因果假设。
- `used_by`: h-v001-002；HB-001。
- `risk`: 若代理与真实损失低相关，预算调度不可能稳定优于随机或局部不确定性。Sherlock 已报告其测试域中 `fan-out` 与整体错误幅度几乎无相关。
- `how_to_verify`: 在配对故障任务上计算真实单点干预价值，与各代理做留任务族排序相关和等预算干预对照。
- `status`: contradicted
- `related evidence`: `ev-p073-internal-confidence-misalignment`, `ev-p025-grouped-step-influence`, Sherlock arXiv:2511.00330 §5（fan-in 正相关、fan-out 几乎无相关）
- `last_updated`: 2026-08-13

## AS-v001-004

- `run_id`: 20260813_1547_run10
- `run_ref_type`: explicit_run_id
- `assumption_id`: AS-v001-004
- `assumption`: 不访问隐藏状态时，智能体轨迹中仍能恢复足够准确的数据依赖图，以限定错误观测的后代集合。
- `source`: 主研究者实现假设。
- `used_by`: h-v001-002, h-v001-003。
- `risk`: 依赖边漏检会保留污染状态，误检会让局部回滚退化为全轨重启。
- `how_to_verify`: 在带程序化依赖真值的任务上盲测边级精确率/召回率，并做依赖抽取噪声敏感性实验。
- `status`: abandoned
- `related evidence`: `ev-p037-evaluation-core`（仅说明 DAG 评价可表达多路径，不支持在线抽取）；MemTX 与 Dependency-Guided Rollback Repair 形成直接组件碰撞
- `last_updated`: 2026-08-13

## AS-v001-005

- `run_id`: 20260813_1547_run10
- `run_ref_type`: explicit_run_id
- `assumption_id`: AS-v001-005
- `assumption`: 环境中存在不等同于错误标签或测试真值的冲突/验证信号，足以触发局部回滚。
- `source`: 主研究者任务设定假设。
- `used_by`: h-v001-003；HB-002。
- `risk`: 若触发信号本身泄漏故障位置，实验会形成不公平 oracle；若无信号，方法无法行动。
- `how_to_verify`: 在数据构造时区分智能体可见冲突与评价器隐藏故障标签；加入无故障冲突和有故障无显式冲突的反例。
- `status`: abandoned
- `related evidence`: `ev-p030-recognition-application-gap`, `ev-p064-experience-following-error`；DART/MemTX/Dependency-Guided Rollback Repair 已占据依赖感知回滚计算
- `last_updated`: 2026-08-13

## AS-v001-006

- `run_id`: 20260813_1547_run10
- `run_ref_type`: explicit_run_id
- `assumption_id`: AS-v001-006
- `assumption`: tau2-bench 或 AppWorld 一类环境的程序化终局可作为不依赖智能体自然语言的评价依据。
- `source`: P040 正文与冻结 Evidence。
- `used_by`: target problem 评价语境；h-v001-001/002/003 的最终测量路径。
- `risk`: 若评测奖励与实际任务规格错位，Formal 证据无法支撑核心 Claim。
- `how_to_verify`: 核对基准原始任务规格、程序化判定与代表任务；报告奖励已知缺陷并进行人工小样本审计。
- `status`: supported
- `related evidence`: `ev-p040-failure-core`, Passage `P040:p0003:s0002`
- `last_updated`: 2026-08-13

## AS-v001-007

- `run_id`: 20260813_1547_run10
- `run_ref_type`: explicit_run_id
- `assumption_id`: AS-v001-007
- `assumption`: 可以在不产生容易被模型识别的表面伪影下，对多步工具轨迹注入模式有效但语义错误的返回。
- `source`: 主研究者测量假设。
- `used_by`: 全部 v001 killer experiment；benchmark judgment。
- `risk`: 若故障带有人工模板痕迹，检测器可能学到注入器而非语义错误。
- `how_to_verify`: 同分布替换、盲注入来源分类、自然失败对照、跨故障生成器测试与人工语义审计。
- `status`: unverified
- `related evidence`: P039 仅提供单轮参数陷阱；当前无直接长程自然化注入证据。
- `last_updated`: 2026-08-13

## 人工检查

当前三个 draft 假设、失败模式因果解释和 benchmark 判断依赖的关键未证前提均已入账；没有把 `unverified` 项写成论文事实。Prior Audit 后，AS-v001-003 因 Sherlock 的 `fan-out` 反例更新为 `contradicted`；AS-v001-004/005 随 h-v001-003 的致命组件碰撞更新为 `abandoned`。条目保留以供审计。

## AS-v001-008

- `run_id`: 20260813_1547_run10
- `run_ref_type`: explicit_run_id
- `assumption_id`: AS-v001-008
- `assumption`: 单次事后读取到与写请求同名的实体或字段，足以证明本次写副作用发生。
- `source`: v001 原型中的隐含实现假设。
- `used_by`: h-v001-001 的 `witness_compiler.py` 原型。
- `risk`: 写操作通常作用于预先存在实体；实体仍可读取与动作是否发生无关，会让静默空操作通过。
- `how_to_verify`: 对相同初态和调用前缀，比较真实调用与原样成功响应的静默空操作世界。
- `status`: contradicted
- `related evidence`: `workbench_v001/scratch_appworld_silent_noop/paired_noop_discriminativity.json`
- `last_updated`: 2026-08-13
- `update_note`: follow/download/like 四类见证在洁净与空操作上均为真；只有一个已编译见证具有判别性。

## AS-v001-009

- `run_id`: 20260813_1547_run10
- `run_ref_type`: explicit_run_id
- `assumption_id`: AS-v001-009
- `assumption`: 相同权限下，每个重要工具副作用都至少有一个公开、完整且无副作用的读接口可观察。
- `source`: v001 方法边界推断。
- `used_by`: v002 是否能形成自动运行时效果差分。
- `risk`: 若效果属于其他主体、仅最终后台状态可见、读接口分页不全或读本身写状态，则无法安全裁决。
- `how_to_verify`: 对操作族枚举同权限公共读计划，检查写前—写后差分、分页穷尽、主体范围和读前后状态哈希。
- `status`: contradicted_as_universal
- `related evidence`: `venmo.remind_payment_request` 的通知只对接收者可见；当前调用者是发送者。
- `last_updated`: 2026-08-13
- `update_note`: v002 必须以可观察覆盖率为显式指标，对不可观察实例输出 `UNKNOWN`，不得借用额外凭据。

## AS-v002-001

- `run_id`: 20260813_1547_run10
- `run_ref_type`: explicit_run_id
- `assumption_id`: AS-v002-001
- `assumption`: 公开工具规范与运行时输出通常包含足够元数据，使系统无需人工完整性规则即可建立查询相对的分页、权限和新鲜度覆盖。
- `source`: h-v002-002 的实现前提。
- `used_by`: h-v002-002 的自动覆盖证书编译主张。
- `risk`: 若需人工声明权限充分性、新鲜度或分页契约，方法会退化为手写后置条件。
- `how_to_verify`: 在多工具、多权限与异步接口上，仅凭公开规范自动实例化覆盖义务，并与人工审计的可回答性比较。
- `status`: contradicted_for_current_implementation
- `related evidence`: `workbench_v002/coverage_certificate/coverage_types.py`；`scope_probe_results.json`
- `last_updated`: 2026-08-13
- `update_note`: 当前代码需要调用方显式传入 `require_authenticated_view`、权限充分性与新鲜度条件；AppWorld 接口文档没有自动提供全部证明材料。

## AS-v002-002

- `run_id`: 20260813_1547_run10
- `run_ref_type`: explicit_run_id
- `assumption_id`: AS-v002-002
- `assumption`: 将读取成功、分页闭合、权限覆盖和时间新鲜度合取为三值否定证书，构成尚未被先行工作吸收的新计算。
- `source`: h-v002-002 的方法新颖性假设。
- `used_by`: h-v002-002 的 changed computation 与 mechanism claim。
- `risk`: 若只是经典查询完整性规则与在线三值验证的组合，候选没有方法级差异。
- `how_to_verify`: 对最近数据库完整性、结果受限接口、开放世界否定、CROWN-QA 与 Verified Tool Calls 做组件级审计。
- `status`: contradicted
- `related evidence`: `hypotheses_v002/priors/v002-h002-query-completeness-lineage/`；`hypotheses_v002/priors/v002-h002-resultbound-lineage-arxiv/`；CROWN-QA arXiv:2608.04591；Verified Tool Calls arXiv:2608.02645
- `last_updated`: 2026-08-13
- `update_note`: 语义、查询计划与证书任务形式已有直接祖先；当前手写布尔规则没有留下不可被组合基线吸收的新计算。

## AS-v002-003

- `run_id`: 20260813_1547_run10
- `run_ref_type`: explicit_run_id
- `assumption_id`: AS-v002-003
- `assumption`: 在同一凭据下闭合枚举后未见目标，可以推出目标在现实或全局数据库中不存在。
- `source`: 覆盖证书范围可能发生的隐含过称。
- `used_by`: h-v002-002 的否定事实边界。
- `risk`: 权限过滤视图会把不可见实体伪装成不存在。
- `how_to_verify`: 区分凭据视图内命题与全局命题，并核对授权视图下的查询可重写性或信息决定性。
- `status`: contradicted
- `related evidence`: `scope_probe_results.json` 的匿名/认证配对；Authorization Views / Non-Truman 查询文献
- `last_updated`: 2026-08-13
- `update_note`: 当前实验证据只允许生成端点、凭据与时点范围化的 `ABSENT`；不能升级为全局不存在。

## AS-v002-004

- `run_id`: 20260813_1547_run10
- `run_ref_type`: explicit_run_id
- `assumption_id`: AS-v002-004
- `assumption`: 范围化三值类型至少能在真实工具接口上阻止由首屏截断、权限不足、读取失败和缺乏新鲜度引起的过度闭世界化。
- `source`: v002 Scratch 的局部机制假设。
- `used_by`: `workbench_v002/coverage_certificate`。
- `risk`: 若类型器只是复述人工标签或不能处理真实响应，连语义载体也不成立。
- `how_to_verify`: 在同一真实状态上构造首屏/后页、匿名/认证、成功/错误、有/无新鲜度保证的配对读取。
- `status`: supported_for_microprobe_only
- `related evidence`: `workbench_v002/coverage_certificate/scope_probe_results.json`
- `last_updated`: 2026-08-13
- `update_note`: 八案 Scratch 命中预期语义；尚未测量智能体独立终局、跨域自动化或相对强基线收益。

## AS-v003-001

- `run_id`: 20260813_1547_run10
- `run_ref_type`: explicit_run_id
- `assumption_id`: AS-v003-001
- `assumption`: 工具结果—动作反事实等变性仍是未被现有智能体诊断、归因和训练方法占据的独立计算。
- `source`: v003 宽路线的新颖性假设。
- `used_by`: h-v003-001。
- `risk`: 若已有工作已分别实现响应扰动回放、动作反事实归因、返回消费训练和工具依赖建模，剩余只是目标函数或模块拼接。
- `how_to_verify`: 核对 AgentCheck、AttriGuard、Causal Agent Replay、ACCORD、Function-Aware FIM 与工具调用依赖图探针的实际计算。
- `status`: contradicted_for_broad_form
- `related evidence`: arXiv:2607.11098；2603.10749；2606.08275；2606.16432；2607.12463；2605.25310
- `last_updated`: 2026-08-13
- `update_note`: 宽路线没有留下足以区别于反事实回放/归因及返回消费训练的新计算；单纯增加等变损失不足以支撑方法贡献。

## AS-v003-002

- `run_id`: 20260813_1547_run10
- `run_ref_type`: explicit_run_id
- `assumption_id`: AS-v003-002
- `assumption`: 带来源调用、行和字段的类型化选择器会稳定优于简单短引用映射。
- `source`: h-v003-002 的最小方法假设。
- `used_by`: `workbench_v003/late_binding_probe`。
- `risk`: 若最简单短引用同等或更好，类型化结构没有准确性增量，只是更复杂接口。
- `how_to_verify`: 在相同任务、候选、模型、调用数和标识符双射下比较原始 ID、短引用与类型化选择器。
- `status`: contradicted
- `related evidence`: `workbench_v003/late_binding_probe/probe_results_qwen3_4b.json`；`probe_results_qwen2.5_7b.json`；`probe_results_qwen3_8b.json`
- `last_updated`: 2026-08-13
- `update_note`: 选择器在 Qwen3-4B 为 14/16，低于短引用 16/16；Qwen2.5-7B 同为 14/16；Qwen3-8B 同为 16/16。没有任何模型显示选择器优于短引用。

## AS-v003-003

- `run_id`: 20260813_1547_run10
- `run_ref_type`: explicit_run_id
- `assumption_id`: AS-v003-003
- `assumption`: 当前主要错误来自高熵标识符的字符运输，而非候选的语义选择。
- `source`: h-v003-002 的机制解释。
- `used_by`: 类型化晚绑定的预期机制签名。
- `risk`: 若错误来自语义解析，隐藏 ID 无法解决核心失败。
- `how_to_verify`: 将模型选择解析回语义标签，分别统计未知/损坏标识符与选错候选。
- `status`: contradicted_in_microprobe
- `related evidence`: 三份 `probe_results_*.json`
- `last_updated`: 2026-08-13
- `update_note`: 144 次输出均可解析并绑定；观察到的失败均映射到一个真实但语义错误的候选，没有发现选对语义行却生成不存在标识符的纯字符复制错误。

## AS-v004-001

- `run_id`: 20260813_1547_run10
- `run_ref_type`: explicit_run_id
- `assumption_id`: AS-v004-001
- `assumption`: 用约束图定位跨子任务约束、以重叠分块和共享变量接口合成局部解，是尚未用于大语言模型任务分解的新计算。
- `source`: h-v004-001 的方法新颖性假设。
- `used_by`: h-v004-001。
- `risk`: 若最近工作已经把智能体任务规约为约束满足问题并采用树分解保证全局可合成，该方法核没有独立贡献。
- `how_to_verify`: 核对 PMC 的局部/全局约束流和 ACONIC 的约束图、树分解、边界变量与局部解合成条件。
- `status`: contradicted
- `related evidence`: COLING 2025《Planning with Multi-Constraints via Collaborative Language Agents》；arXiv:2510.07772v3；`workbench_v004/constraint_decomposition_prior_collision.md`
- `last_updated`: 2026-08-13
- `update_note`: PMC 已占据跨子任务约束识别与全局交付；ACONIC 与拟议约束落袋、重叠分块、共享变量一致性逐项重合，并已有 SATBench/Spider 实验。

## AS-v004-002

- `run_id`: 20260813_1547_run10
- `run_ref_type`: explicit_run_id
- `assumption_id`: AS-v004-002
- `assumption`: 局部子任务成功不自动保证跨子任务全局约束满足，是可由独立评价观察的真实失败对象。
- `source`: v004 问题定义。
- `used_by`: h-v004-001 的问题价值判断。
- `risk`: 若该失败仅来自提示遗漏或无法在真实任务中分离，就不值得形成方法路线。
- `how_to_verify`: 比较子任务局部约束通过率与最终全局约束通过率，并检查约束变量是否跨分解边界。
- `status`: supported_by_prior_work_only
- `related evidence`: PMC 在 TravelPlanner 上分别报告局部/全局约束与最终通过率；`hypotheses_v004/searches/cross_constraint_decomposition_v004_01/report.md`
- `last_updated`: 2026-08-13
- `update_note`: 失败对象成立，但解决它的拟议核心计算已被直接先行工作占据；因此只保留问题事实，不保留方法核。

## AS-v005-001

- `run_id`: 20260813_1547_run10
- `run_ref_type`: explicit_run_id
- `assumption_id`: AS-v005-001
- `assumption`: 给成功经验增加显式适用条件并在运行前门控，仍构成未被程序性记忆工作占据的方法核。
- `source`: h-v005-001 的宽核新颖性假设。
- `used_by`: h-v005-001。
- `risk`: ReMe、MACLA 和 MSCE 已分别存储何时使用、前置条件、适用边界并利用成败证据或价值过滤。
- `how_to_verify`: 核对三者的经验表示、条件更新和运行时选择计算。
- `status`: contradicted
- `related evidence`: `workbench_v005/applicability_prior_boundary.md`
- `last_updated`: 2026-08-13
- `update_note`: 宽泛适用域门被直接先行工作吸收，h-v005-001 已记为 prior_collision。

## AS-v005-002

- `run_id`: 20260813_1547_run10
- `run_ref_type`: explicit_run_id
- `assumption_id`: AS-v005-002
- `assumption`: 在已知有限谓词类中主动选择环境状态，比同预算随机查询更快恢复固定技能的适用守卫。
- `source`: h-v005-002 的合成机制假设。
- `used_by`: `workbench_v005/guard_probe`。
- `risk`: 若主动选择无增量，连窄机制载体都不成立；即使成立也可能只是经典主动概念学习。
- `how_to_verify`: 在相同技能、假设空间、源状态和查询预算下比较主动版本空间二分、局部翻转、随机查询和保守放行。
- `status`: supported_for_closed_synthetic_class_only
- `related evidence`: `workbench_v005/guard_probe/guard_probe_results.json`
- `last_updated`: 2026-08-13
- `update_note`: 预算 10 时全局主动法 12/12 精确而随机法平均精确率 0.2058；但较低预算的单一一致守卫仍错误放行，且该优势属于经典已知计算。

## AS-v005-003

- `run_id`: 20260813_1547_run10
- `run_ref_type`: explicit_run_id
- `assumption_id`: AS-v005-003
- `assumption`: 当前 AppWorld 实现能证明主动干预相对语言模型条件归纳和简单守卫基线的真实增量。
- `source`: h-v005-002 的最小真实工具杀手实验。
- `used_by`: `workbench_v005/appworld_guard_probe`。
- `risk`: 人工谓词目录若只含真实必要条件，则全谓词守卫和语言模型可无失败标签直接恢复守卫。
- `how_to_verify`: 比较零学习全谓词守卫、三个本地模型的成功样本/被动样本/主动样本条件，以及独立官方终局。
- `status`: contradicted
- `related evidence`: `workbench_v005/appworld_guard_probe/appworld_guard_results.json`；`llm_guard_baseline_results.json`；`baseline_delta_audit.md`
- `last_updated`: 2026-08-13
- `update_note`: 全谓词基线和三个模型在只给程序加一个成功状态时均得到精确三谓词守卫；主动配对没有改变排序或状态转移。

## AS-v005-004

- `run_id`: 20260813_1547_run10
- `run_ref_type`: explicit_run_id
- `assumption_id`: AS-v005-004
- `assumption`: v005 重建的 Run-local Recall 可安全用于选择 AppWorld 任务、程序或任务级主张。
- `source`: Active Diagnosis 前的潜在工具使用假设。
- `used_by`: 后续真实夹具选择。
- `risk`: Run-local external AppWorld 数据含开发集和测试集 ground_truth，FTS 重建会造成真值污染。
- `how_to_verify`: 检查 diagnosis facts 的索引文件范围和命中路径。
- `status`: contradicted
- `related evidence`: `workbench_v005/diagnosis/v005-applicability-crossroad/diagnosis_facts.json`
- `last_updated`: 2026-08-13
- `update_note`: v005 后续未用 Recall 选择 AppWorld 任务或构造程序；只使用预先选定的开发集夹具和直接源码接口。

## AS-v006-001

- `run_id`: 20260813_1547_run10
- `run_ref_type`: explicit_run_id
- `assumption_id`: AS-v006-001
- `assumption`: 对工具异常后的外部效果做语义对账，再决定消费、重试或弃权，是尚未被工具智能体可靠性方法占据的新计算。
- `source`: h-v006-001 的方法新颖性假设。
- `used_by`: h-v006-001。
- `risk`: 最新工作可能已经同时包含非原子失败、写后验证、重试前验证、幂等键和事务恢复。
- `how_to_verify`: 核对 Verified Tool Calls、Cordon、Atomix 与 CapLease 的故障模型和运行时转移。
- `status`: contradicted
- `related evidence`: `workbench_v006/ambiguous_commit_prior_collision.md`；arXiv:2608.02645；arXiv:2606.17573；arXiv:2608.01710
- `last_updated`: 2026-08-13
- `update_note`: h-v006-001 的意图规范化、写后对账、验证后重试和持久去重均有直接先行；追加范围证书又会退回 v002 的已杀拼接。

## AS-v007-001

- `run_id`: 20260813_1547_run10
- `run_ref_type`: explicit_run_id
- `assumption_id`: AS-v007-001
- `assumption`: AppWorld 中看似只读的 GET 验证工具会在目标真实夹具上产生任务相关状态差分并改变独立终局。
- `source`: h-v007-001 的失败载体假设。
- `used_by`: `workbench_v007/observer_effect_probe`。
- `risk`: 静态创建分支可能在目标初态不可达，或额外状态不在官方评价投影内。
- `how_to_verify`: 同一开发任务固定行动的 act-only 与 act-plus-show_volume 隔离 A/B，并记录模型计数与官方终局。
- `status`: contradicted_in_selected_fixture
- `related evidence`: `workbench_v007/observer_effect_probe/appworld_observer_ab_results.json`
- `last_updated`: 2026-08-13
- `update_note`: 两组均 6/6，MusicPlayer 计数均保持 106；源码中的缺省创建分支在该主用户状态不触发。

## AS-v007-002

- `run_id`: 20260813_1547_run10
- `run_ref_type`: explicit_run_id
- `assumption_id`: AS-v007-002
- `assumption`: 通过黑盒调用与检查点状态差分认证工具的读写/效果语义，是未被先行工作占据的新计算。
- `source`: h-v007-001 收缩后的方法新颖性假设。
- `used_by`: h-v007-001。
- `risk`: REST API 测试领域可能已有从 OpenAPI 假设出发、用行为模式迭代确认 CRUD 语义的方法。
- `how_to_verify`: 核对 CRUDinfer 与 REST 行为属性测试的输入、测试序列、确认逻辑和输出。
- `status`: contradicted
- `related evidence`: CRUDinfer, ICSE 2026；Karlsson 等，Software Quality Journal 2024；`workbench_v007/observer_effect_probe/scratch_report.md`
- `last_updated`: 2026-08-13
- `update_note`: 黑盒 CRUD/效果确认已有直接方法；将其用于 Verified Tool Calls 的只读前置条件只是已知模块组合。

## AS-v008-001

- `run_id`: 20260813_1547_run10
- `run_ref_type`: explicit_run_id
- `assumption_id`: AS-v008-001
- `assumption`: 以跨版本黑盒行为等价迁移已有工具计划，与普通 API 客户端代码迁移相比改变了新的核心计算。
- `source`: h-v008-001 的方法新颖性假设。
- `used_by`: h-v008-001。
- `risk`: 工具计划本身就是客户端程序，复杂一对多/多对多替换、黑盒语义建模、迁移合成和行为等价可能已有完整谱系。
- `how_to_verify`: 核对 REST 差分回归、EVOL、M3、ECOOP 多对多转换、Sprout 与 APIMig 的输入、变换空间、验证判据和输出。
- `status`: contradicted
- `related evidence`: `workbench_v008/api_evolution_prior_collision.md`；`research_workspace/subagents/v008_api_evolution_prior.md`
- `last_updated`: 2026-08-13
- `update_note`: 上述谱系已覆盖主计算；Agent/MCP 只改变应用载体，不能构成独立方法核。

## AS-v008-002

- `run_id`: 20260813_1547_run10
- `run_ref_type`: explicit_run_id
- `assumption_id`: AS-v008-002
- `assumption`: v008 刷新的 Run-local Recall 可用于 AppWorld 程序、任务或任务级科研结论。
- `source`: Active Diagnosis 的工具安全假设复核。
- `used_by`: v008 及后续所有 AppWorld 工作。
- `risk`: 外部 AppWorld 数据目录含隐藏终局材料，全文索引会将其作为普通文本纳入。
- `how_to_verify`: 检查 Recall rebuild 输出和 Diagnosis facts 中的索引文件清单。
- `status`: contradicted
- `related evidence`: `workbench_v008/diagnosis/trajectory_after_v007/diagnosis_facts.json`
- `last_updated`: 2026-08-13
- `update_note`: FTS 状态为 READY、semantic 因缺少索引为 DEGRADED；后续继续禁止用 Recall 选择或构造 AppWorld 任务、程序与主张。

## AS-v008-003

- `run_id`: 20260813_1547_run10
- `run_ref_type`: explicit_run_id
- `assumption_id`: AS-v008-003
- `assumption`: 以实体绑定、分支谓词和合法下一动作为等价对象，会使跨版本工具适配器综合获得不同于程序切片、观察等价和既有接口迁移的新核心计算。
- `source`: h-v008-002 的收缩后新颖性假设。
- `used_by`: h-v008-002。
- `risk`: 若所谓延续等价只是以智能体轨迹字段为切片准则的部分行为保持，反例综合、复杂调用替换和轨迹切片均已有直接先行。
- `how_to_verify`: 把候选的输入、投影、搜索循环和失败条件逐项映射到动态切片、Sharma 等的适配器综合、Sprout/M3、HarnessFix 与 SkillAudit。
- `status`: contradicted
- `related evidence`: `workbench_v008/downstream_continuation_collision.md`；Sharma et al., IEEE TSE 2021；Sprout, OOPSLA 2025；M3, ASE 2020；arXiv:2606.06324v2；arXiv:2606.14239v1
- `last_updated`: 2026-08-13
- `update_note`: 下游延续只是任务条件化切片上的观察等价；智能体特有数据流定位与配对技能修订也分别被 HarnessFix 和 SkillAudit 占据。继续实现只能验证已知组件拼接的效用，不能建立方法身份。

## AS-v009-001

- `run_id`: 20260813_1547_run10
- `run_ref_type`: explicit_run_id
- `assumption_id`: AS-v009-001
- `assumption`: 已检索自然语言证据的支持关系可以在不读取隐藏路线标签的情况下形成足够可靠的布尔 lineage，使独立证据根最小割成为可测的停止量。
- `source`: TR-v009-001 的关键表示假设。
- `used_by`: h-v009-001。
- `risk`: 若支持边、必要原子或来源依赖只能靠人工真值标注，min-cut 只是泄漏后的装饰；若只等于文档计数，则没有计算增量。
- `how_to_verify`: 在含同源改写、独立路线、单一权威和不可判定负对照的静态搜索环境中，盲于 route/gold 地构图，并与未折叠文档计数、两引用规则和人工图上界比较。
- `status`: contradicted
- `related evidence`: `workbench_v009/provenance_resilience_transfer_audit.md`；`workbench_v009/identifiability_probe_results.json`；`workbench_v009/v009_negative_decision.md`
- `last_updated`: 2026-08-13
- `update_note`: 观测等价潜在世界反例表明，同一网页可见量可对应同根转载或独立生成，硬根韧性标签不同；无必异根证据时 8 篇文档的安全独立根下界仍为 1。点估计只能是经典概率复制检测，不能支撑硬证书。

## AS-v009-002

- `run_id`: 20260813_1547_run10
- `run_ref_type`: explicit_run_id
- `assumption_id`: AS-v009-002
- `assumption`: 相比 Argus/S2G/SURE-RAG 的充分性或缺失项判断，独立根删除韧性会改变停止接受集合和下一查询目标，而不只是让智能体多搜几次。
- `source`: h-v009-001 的核心方法增量假设。
- `used_by`: h-v009-001。
- `risk`: 最近先行可能已有等价的多路径/来源独立充分性；简单两来源或固定完整链规则也可能达到相同结果。
- `how_to_verify`: 最近先行逐项审计；同调用预算比较接受集合、单源支配率、准确率、覆盖率与搜索成本，并加入固定两引用、S2G式gap judge和不折叠韧性基线。
- `status`: contradicted
- `related evidence`: `workbench_v009/provenance_resilience_transfer_audit.md`；`research_workspace/subagents/v009_evidence_decision_prior.md`；`workbench_v009/identifiability_probe_report.md`
- `last_updated`: 2026-08-13
- `update_note`: 可实现的 estimated-lineage 版本等价于来源依赖估计/近重复聚类加 Argus/SURE-RAG/GAVEL；若保留硬保证则普通网页上普遍弃答。当前计算没有独立于强组合基线且可识别的输入对象。

## AS-v010-001

- `run_id`: 20260813_1547_run10
- `run_ref_type`: explicit_run_id
- `assumption_id`: AS-v010-001
- `assumption`: AppWorld 隔离状态/响应的配对反事实差分可以在不把隐藏 SQL 日志提供给方法的条件下，恢复值不变读、字段级写与跨调用句柄依赖。
- `source`: h-v010-001 的核心可行性假设。
- `used_by`: h-v010-001。
- `risk`: 状态差分天然只揭示写；读集合若没有响应变化或后续行为变化不可识别，候选可能重演 v009 的潜变量问题。
- `how_to_verify`: 隐藏 SQL 访问插桩只用于评分；方法输入限制为模式、参数、响应、状态差分和可审计只读探针；按未见工具/应用留出测冲突召回与 UNKNOWN 覆盖。
- `status`: contradicted
- `related evidence`: `workbench_v010/broad_concurrency_collision.md`；`research_workspace/subagents/v010_concurrency_scout.md`；`workbench_v010/action_model_collision.md`
- `last_updated`: 2026-08-13
- `update_note`: 即使假定配对差分可恢复读/写，其计算已经是从部分 state-action-state traces 学习 lifted preconditions/effects；STRIPS/STRIPS+ 动作模型学习直接占据，因而可行性不再能形成方法身份。

## AS-v010-002

- `run_id`: 20260813_1547_run10
- `run_ref_type`: explicit_run_id
- `assumption_id`: AS-v010-002
- `assumption`: 反事实编译器相对 CoAgent ToolSmith、Cordon 风格句柄沿袭和简单代码/SQL插桩存在可投稿的改变计算，而不只是用更多开发期执行生成同一足迹声明。
- `source`: h-v010-001 的方法增量假设。
- `used_by`: h-v010-001。
- `risk`: REST API 有状态测试、动态程序分析和事务足迹预测可能直接吸收；若有源码/日志，经典插桩更强；若无隔离环境，方法不可用。
- `how_to_verify`: 标准 Prior Audit 与一级来源逐项 I/C/O；离线杀手实验加入单次差分、ToolSmith 式生成、句柄沿袭和 Oracle 插桩。
- `status`: contradicted
- `related evidence`: `research_workspace/subagents/v010_concurrency_scout.md`；`hypotheses_v010/priors/v010-h001-action-model-lineage/candidates.json`；`workbench_v010/action_model_collision.md`
- `last_updated`: 2026-08-13
- `update_note`: STRIPS+ 已处理隐式动作参数与部分/局部状态观测，RESTler/Morest 已处理API生产者—消费者、CRUD与动态执行反馈；再接 CoAgent/Atomix 只是已有模块组合。

## AS-v011-001

- `run_id`: 20260813_1547_run10
- `run_ref_type`: explicit_run_id
- `assumption_id`: AS-v011-001
- `assumption`: 对跨应用身份连接做来源折叠与不可循环证明，可以形成不同于经典实体解析、PACT 参数来源和 IGAC 资源门控的新计算。
- `source`: v011 跨应用身份绑定路线的窄化假设。
- `used_by`: v011 identity-binding route。
- `risk`: 上游来源根不可见时标签不可识别；来源根可见时退化为带数据来源约束的实体解析。
- `how_to_verify`: 对照 v009 观测等价根反例，并逐项映射经典实体解析、PACT 与 IGAC 的输入、计算和输出。
- `status`: contradicted
- `related evidence`: `research_workspace/subagents/v011_identity_binding_scout.md`；`workbench_v009/identifiability_probe_report.md`；`workbench_v011/v011_route_resolution.md`
- `last_updated`: 2026-08-13
- `update_note`: 无可审计上游根时无法证明独立/非循环；有根谱系时核心被经典实体解析与来源约束吸收，且外层门控已有直接先行。

## AS-v011-002

- `run_id`: 20260813_1547_run10
- `run_ref_type`: explicit_run_id
- `assumption_id`: AS-v011-002
- `assumption`: 跨跳委派子图精化证明相对目的策略、任务切片、衰减令牌和值来源链改变了新的授权计算。
- `source`: v011 authority-flow route 的最窄残余。
- `used_by`: v011 authority-flow route。
- `risk`: 可能只是 PAuth + AIP + FORGE/Progent 的直接组合，且父任务图仍依赖语义预言机。
- `how_to_verify`: 将父/子图节点映射、值孔位、衰减块和提交检查逐项映射到最近复合基线。
- `status`: contradicted
- `related evidence`: `research_workspace/subagents/v011_authority_flow_scout.md`；`workbench_v011/v011_route_resolution.md`
- `last_updated`: 2026-08-13
- `update_note`: 所有检查均可由任务程序切片、能力衰减、值来源包络和因果图策略组合表达；没有不可约算子。

## AS-v011-003

- `run_id`: 20260813_1547_run10
- `run_ref_type`: explicit_run_id
- `assumption_id`: AS-v011-003
- `assumption`: 针对拟议不可逆动作合成最小区分性只读查询，是不同于主动诊断、任务导向主动感知和函数求值决策树的新计算。
- `source`: v011 decision-conditioned observability route。
- `used_by`: v011 observability route。
- `risk`: 可能世界是测试输入、动作允许/拒绝是目标函数、只读查询是带成本测试，构成精确约化。
- `how_to_verify`: 写出 `f(h)=d_a(h)` 的约化，并核对等价类判定、EC2、部分可观测强规划和 Agent-specific 门控。
- `status`: contradicted
- `related evidence`: `research_workspace/subagents/v011_observability_scout.md`；`workbench_v011/v011_route_resolution.md`
- `last_updated`: 2026-08-13
- `update_note`: 候选精确退化为带成本函数求值决策树；测试模型学习又与 v010 动作模型学习盆地重合。

## AS-v012-001

- `run_id`: 20260813_1547_run10
- `run_ref_type`: explicit_run_id
- `assumption_id`: AS-v012-001
- `assumption`: 对未决工具结果构造若干反事实完成并教师强制重放，可以恢复显式参数/资源依赖之外的语义控制依赖，并形成不同于现有反事实门控和安全推测提交的新计算。
- `source`: v012 counterfactual future-dependence barrier 路线。
- `used_by`: v012 async-future route。
- `risk`: 核心重放门可能被 AttriGuard 精确吸收；安全执行集合可能被 PASTE、Speculative Actions 与提交屏障固定；可行结果空间在完成前不可识别。
- `how_to_verify`: 对 AsyncFC、AttriGuard、PASTE、Speculative Interaction Agents、Speculative Actions 和经典控制依赖逐项做输入—计算—输出映射，并检查结果类覆盖与重放成本。
- `status`: contradicted
- `related evidence`: `research_workspace/subagents/v012_async_future_scout.md`；`workbench_v012/v012_async_future_collision.md`
- `last_updated`: 2026-08-13
- `update_note`: 问题成立，但 paired future completion、教师强制重放和调用存活门在计算上等同 AttriGuard 的干预域迁移；确认后提交、取消/回滚和不可逆禁推测已有直接谱系。未定义结果抽象域时不存在可审计的 must-invariance。

## AS-v013-001

- `run_id`: 20260813_1547_run10
- `run_ref_type`: explicit_run_id
- `assumption_id`: AS-v013-001
- `assumption`: 固定科学实验前历史与实验、只干预工具结果，并联合训练置信更新、下一实验和假设保留/淘汰，可以形成不同于结果—动作等变、贝叶斯更新和现有科学智能体训练的新计算。
- `source`: v013 evidence-response training 路线。
- `used_by`: v013 evidence-response route。
- `risk`: 已知似然时标签由既有统计控制器产生并被现有训练/重放方法吸收；未知似然时正确更新与动作不可识别。
- `how_to_verify`: 做最近公平组合基线映射，并构造可见输入相同但交换似然、要求相反后验的潜在世界。
- `status`: contradicted
- `related evidence`: `research_workspace/subagents/v013_evidence_response_training_scout.md`；`workbench_v013/v013_evidence_response_training_collision.md`
- `last_updated`: 2026-08-13
- `update_note`: v003、贝叶斯教学、Fisher-R1、HEP/EDIT、反事实重放和 POPPER/MDA 可重构已知标签路线；未知似然的 likelihood-swap 反例证明正确更新方向、下一实验与停止决策不由当前输入决定。

## AS-v014-001

- `run_id`: 20260813_1547_run10
- `run_ref_type`: explicit_run_id
- `assumption_id`: AS-v014-001
- `assumption`: 反馈预算、公共—封闭分层、低带宽保护审计和独立一次性终局可以形成新的智能体验证反馈方法，而不是经典自适应数据分析、CEGIS 或既有密封接受循环的应用。
- `source`: v014 adaptive-verifier-feedback route。
- `used_by`: v014 verifier-feedback route。
- `risk`: 统计样本、完整形式规范和有限代理意图三种语义分别已有精确约化；SEAL 可能已直接实现端到端协议。
- `how_to_verify`: 对 Reusable Holdout/Thresholdout/Ladder、CEGIS、SEAL、SpecBench 和 HackDetect 做 I/C/O 映射，并区分统计过拟合、协议侧通道与代理目标错位。
- `status`: contradicted
- `related evidence`: `research_workspace/subagents/v014_adaptive_verifier_feedback_scout.md`；`workbench_v014/v014_adaptive_verifier_feedback_collision.md`
- `last_updated`: 2026-08-13
- `update_note`: 三分约化覆盖验证器语义；SEAL 又直接占据不可见外部审计、单比特候选—现任接受、整状态回退与独立部署终局。

## AS-v015-001

- `run_id`: 20260813_1547_run10
- `run_ref_type`: explicit_run_id
- `assumption_id`: AS-v015-001
- `assumption`: 把验证通过表示为带读足迹的可撤销进度证书，并按后续写集选择性失效和重验，能形成新的智能体进度计算。
- `source`: v015 nonmonotone-progress route。
- `used_by`: v015 progress route。
- `risk`: 可能与自调整计算、增量构建、安全回归测试选择和版本化快照控制精确同构。
- `how_to_verify`: 将验证单元、读足迹、动作写集、脏前沿、重验和新鲜终局逐字段映射到 DDG、Shake/Ekstazi 与 Atomix。
- `status`: contradicted
- `related evidence`: `research_workspace/subagents/v015_nonmonotone_progress_scout.md`；`workbench_v015/v015_nonmonotone_progress_collision.md`
- `last_updated`: 2026-08-13
- `update_note`: 显式足迹版本与 DDG/Shake/Ekstazi 精确同构；推断式语义足迹失去安全保证并回到 v010 动作模型学习。
