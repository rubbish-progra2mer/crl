# CRL Active Diagnosis Facts

STATUS: ADVISORY_NON_AUTHORITATIVE
FACTS_SHA256: 6b84713f26b76d2bf8d89e2cb7dd14683403e470b56e32eddacad220b8fef7f5

> 这是机械事实视图，不是科研裁决。主研究者负责解释矛盾、盲点和高信息量下一步。

- Run: `20260818_2228_run16`
- Version: `v001`
- Indexed ordinary files: 97
- Current-version Recorded/Formal attempts: 4
- Comparison files: 0
- Search snapshot files: 6
- Review evaluation files: 0
- Recall FTS: READY（无）
- Recall semantic: DEGRADED（semantic_index_missing）
- Selection context template: READY

## Run-wide mechanical facts

- Scientific versions: 1
- Empty current version: False
- Scratch report files: 0
- Recorded attempts: 0
- Formal / Review-support attempts: 4
- Valid Formal / Review-support attempts: 3
- Search snapshots: 2
- Raw search bytes: 4378036
- Compact search report bytes: 16587
- Prior audits: 2
- Classified collision kinds: 0
- Normally unclassified prior audits: 0
- Prior assessment warning audits: 2
- Tail consecutive pre-experiment closures: 0
- Tail consecutive prior-collision pre-experiment closures: 0
- Experiment binding recovery: READY
- Run-local subagent-related Markdown summary artifacts: 0
- Native delegation evidence: UNAVAILABLE
- Verified native delegation count: UNKNOWN
- Recall contamination present: False
- Nested repository indexed bytes: 0
- Diagnosis indexed bytes: 0
- Recall stale indexed sources: 0

## Selection context evidence facts

- 当前最佳候选集合 [PRESENT]: 当前为空。`h-causal-replay-001` 被直接最近先行占据；`h-coverage-witness-001` 虽有两项成功 Screening，但 CROWN-QA 与 ToolGate 使其只剩已有组件组合；`h-delta-contract-001` 的当前局部义务实现被 Formal Screening 反证，较宽方法族只被纠正为 parked，因剩余数据流计算与 HyperAgent 高度重合而不进入最佳集合。
- 新增正向证据 [PRESENT]: 没有新增可投资候选的正向证据。新增科研信息增益来自 `experiment_v001/attempts/delta-contract-screening-v001-r1/`：24 个配对工作流、六类接口演化、100 次本地模型调用的 Formal 结果显示 latest、同信息 diff_prompt、额外预算 reflection 和 obligation 的成功率全部为 0.8333，模式合法率全部为 1.0。失败全部集中在新增前置工具的数据流绑定，说明缩小输出范围本身没有处理真正瓶颈。
- 已失效或被杀范围 [PRESENT]: 反事实轨迹重放与首次不可恢复步骤定位的方法核被 CAR、CausalFlow、ELPO 和 AgentTracer 占据。完整性敏感负向推理的问题、形式化、评价和自然文档现象被 CROWN-QA 占据，一般合约门控被 ToolGate 占据。最新 Formal 只杀死 `h-delta-contract-001` 当前“局部迁移义务相对同信息差分提示有增量”的本地主张和实现；它没有证明全部接口演化方法核心死亡。最初写成 `METHOD_CORE` 的过宽范围已通过后续 `parked` 事件和机器复查 M013 明确纠正。
- 剩余致命不确定性 [PRESENT]: 尚无候选同时满足贡献差分和本地实验支持。接口演化方向的剩余修复需要端口级输入/输出数据流、前置条件缺口扩展和运行态绑定，而 HyperAgent 已直接实现这些计算；仅在其外再加版本差分和局部回归是否足以形成独立论文贡献，目前没有证据。更广泛的不确定性仍是：正式知识库和 2026 最近前沿中是否还存在一个未被模式图、合约门、反事实归因或通用验证占据的可执行计算核心。
- 下一项最高信息量动作 [PRESENT]: 停止继续为接口演化候选叠加 HyperAgent 已有的数据流组件，执行第二次正交问题扩展。优先从“过程验证成本过高时，哪些步骤可由确定性不变量替代模型评判”与“表面成功但状态副作用错误的最小可执行验证”两个问题族寻找现象；先核验 2026 最近先行，再决定是否正式建候选。若仍只能得到已有验证、门控或模式图的组合，则转向改变贡献形态或诚实 No-Delivery 审计，而不是增加版本。
- 策略变化 [PRESENT]: 从“接口演化方法实现”回溯到正交现象优先探索。明确停止三类重复动作：不把公开基准发现当方法贡献；不把 HyperAgent/ToolLIFT/Contract2Tool 的组件重新组合成新方法；不因单次 Screening 失败而夸大整个方法族死亡。失败 attempt `delta-contract-screening-v001` 仅是指标输出契约错误，已以同等设置重跑为 `-r1`，不作为科学反证。

## Latest structured activity version facts

- Structured candidate: latest=v001, versions_since=0
- Recorded: latest=UNAVAILABLE, versions_since=UNAVAILABLE
- Formal: latest=v001, versions_since=0
- Prior Audit: latest=v001, versions_since=0

> 上述版本距离只是原始活动事实，不是科研质量、成熟度或停滞指标。

## Semantic overreach warnings

- `v001/h-delta-contract-001` decision 2: screening_paper_level_kill_without_structural_refutation, single_implementation_paper_level_kill

> 以上仅为声明字段的机械组合警告，不否定主研究者解释，也不自动改变候选状态。

## Prior assessment warnings

- `hypotheses_v001/priors/coverage-witness-prior-v001/assessment.md`
  - assessment collision kind is unknown: PROBLEM_AND_EVALUATION_OCCUPIED_RUNTIME_METHOD_UNRESOLVED
- `hypotheses_v001/priors/delta-contract-prior-v001/assessment.md`
  - assessment collision kind is unknown: PARTIAL_COMPONENT_OVERLAP

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
- 若已出现连续 5 个实验前关闭，明确停止重复什么动作，并从回溯、正交扩展、现象优先、贡献形态变化或长期推迟的高信息量实验中选择不同动作。
