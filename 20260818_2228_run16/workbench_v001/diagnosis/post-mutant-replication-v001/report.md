# CRL Active Diagnosis Facts

STATUS: ADVISORY_NON_AUTHORITATIVE
FACTS_SHA256: 4e315dd642ae0357cb8c23a1257213d921319845034f854f69abbab8df9f6848

> 这是机械事实视图，不是科研裁决。主研究者负责解释矛盾、盲点和高信息量下一步。

- Run: `20260818_2228_run16`
- Version: `v001`
- Indexed ordinary files: 156
- Current-version Recorded/Formal attempts: 6
- Comparison files: 0
- Search snapshot files: 9
- Review evaluation files: 0
- Recall FTS: READY（无）
- Recall semantic: DEGRADED（semantic_index_missing）
- Selection context template: READY

## Run-wide mechanical facts

- Scientific versions: 1
- Empty current version: False
- Scratch report files: 0
- Recorded attempts: 0
- Formal / Review-support attempts: 6
- Valid Formal / Review-support attempts: 5
- Search snapshots: 3
- Raw search bytes: 5306154
- Compact search report bytes: 24902
- Prior audits: 4
- Classified collision kinds: 0
- Normally unclassified prior audits: 0
- Prior assessment warning audits: 4
- Tail consecutive pre-experiment closures: 0
- Tail consecutive prior-collision pre-experiment closures: 0
- Experiment binding recovery: READY
- Run-local subagent-related Markdown summary artifacts: 0
- Native delegation evidence: UNAVAILABLE
- Verified native delegation count: UNKNOWN
- Recall contamination present: False
- Nested repository indexed bytes: 0
- Diagnosis indexed bytes: 0
- Recall stale indexed sources: 6

## Selection context evidence facts

- 当前最佳候选集合 [PRESENT]: 当前为空。`h-causal-replay-001` 被直接最近先行占据；`h-coverage-witness-001` 虽有两项成功 Screening，但 CROWN-QA 与 ToolGate 使其只剩已有组件组合；`h-delta-contract-001` 的局部义务实现没有强基线增量；`h-mutant-probe-001` 的开放世界现象虽被两个公开检查点支持，但没有观察到任务外可疑通过运行，且当前加固实现未过预注册风险线。后两者均为 `parked`，不以科研信息增益冒充投资成熟度。
- 新增正向证据 [PRESENT]: 没有新增可投资候选的正向证据。新增科研信息增益来自两个有效 Formal：`contract-mutation-screening-v001` 对 224/224 合同和 224 个公开运行完成匹配，151 个原通过运行中 65 个含保守未断言变化；`contract-mutation-replication-v001` 对独立部分检查点完成 117/117 匹配，67 个原通过运行中 40 个含未断言变化。两次人工语义核对分别覆盖 65/65 与 40/40，均无任务外可疑变化；这把“未断言”与“实际危险或得分虚高”明确分开。
- 已失效或被杀范围 [PRESENT]: 反事实轨迹重放与首次不可恢复步骤定位的方法核被 CAR、CausalFlow、ELPO 和 AgentTracer 占据。完整性敏感负向推理被 CROWN-QA 占据，一般合约门控被 ToolGate 占据。接口演化 Formal 只杀死“局部迁移义务相对同信息完整差分提示有增量”的本地主张与实现。状态合同实验杀死当前端点允许边界实现和“公开运行存在足量任务外副作用而造成实际得分扭曲”的主张：第一次端点边界风险变异逃逸率 0.2722，高于预注册上限 0.25；两个检查点人工核对的任务外可疑数均为 0。开放世界合同与未断言变化现象继续成立，不能被写成更宽死亡。
- 剩余致命不确定性 [PRESENT]: 尚无候选同时满足贡献差分和本地实验支持。最大不确定性已从单一候选效果转为研究空间本身：经过反事实归因、覆盖证明、接口演化和状态合同四个问题族后，是否还能找到一个未被模式图、合约门、状态差分或通用变异测试占据，并能用本机杀手实验验证的计算核心。若第三次正交扩展仍只能得到已知机制组合，则需要审计是否已达到诚实 No-Delivery，而不是继续改写已有候选。
- 下一项最高信息量动作 [PRESENT]: 执行第三次正交扩展并改变贡献形态：停止方法优先和通用验证叠加，转向寻找“已有智能体评测分数不能区分、但可由公开运行材料直接测得的系统性评价失真”，优先要求能改变模型/实现排序而不只是发现合同不完整。先做最近先行与公开数据可执行性筛选；若没有候选能同时保留排序影响、贡献差分和本地复现路径，则进入 No-Delivery 审计。
- 策略变化 [PRESENT]: 第二次正交扩展真实改变了动作：从接口演化转到状态合同现象，新增一个可运行实现、两个公开检查点 Formal 与两套全覆盖人工核对；结果没有挽救候选，因此停止继续调节允许边界阈值或把“未断言”改名为“危险”。上一条 `PAPER_DIRECTION` 的 SCREENING 关闭范围触发单实现/保真度警告后，已立即以 `parked` 事件纠正为只杀当前实现和实际得分扭曲主张。下一步改为评价失真/排序影响优先；不推进科学版本，不把 224 与 117 的样本量增长当质量增长。

## Latest structured activity version facts

- Structured candidate: latest=v001, versions_since=0
- Recorded: latest=UNAVAILABLE, versions_since=UNAVAILABLE
- Formal: latest=v001, versions_since=0
- Prior Audit: latest=v001, versions_since=0

> 上述版本距离只是原始活动事实，不是科研质量、成熟度或停滞指标。

## Semantic overreach warnings

- `v001/h-delta-contract-001` decision 2: screening_paper_level_kill_without_structural_refutation, single_implementation_paper_level_kill
- `v001/h-mutant-probe-001` decision 2: screening_paper_level_kill_without_structural_refutation, single_implementation_paper_level_kill

> 以上仅为声明字段的机械组合警告，不否定主研究者解释，也不自动改变候选状态。

## Prior assessment warnings

- `hypotheses_v001/priors/coverage-witness-prior-v001/assessment.md`
  - assessment collision kind is unknown: PROBLEM_AND_EVALUATION_OCCUPIED_RUNTIME_METHOD_UNRESOLVED
- `hypotheses_v001/priors/delta-contract-prior-v001/assessment.md`
  - assessment collision kind is unknown: PARTIAL_COMPONENT_OVERLAP
- `hypotheses_v001/priors/mutant-contract-prior-v001/assessment.md`
  - assessment collision kind is unknown: PARTIAL_COMPONENT_OVERLAP
- `hypotheses_v001/priors/mutant-probe-prior-v001/assessment.md`
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
