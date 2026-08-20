<!-- CRL_RESEARCH_SEARCH_META {"created_at_utc":"2026-08-13T10:57:37.918451Z","request_fingerprint_sha256":"7bdee7d4e7e568aa2f7f61bbf48a1eaddc19fbe02c3195dff0f325ff6f972bd3","result_json_sha256":"05bee912fee44c333b3303cda95a2d07a00be1daeee729e24ed4466a62a98b6b","search_id":"downstream_continuation_equivalence_v008_02"} -->
# 研究检索导航

> 本报告仅展示查询路线、来源、命中定位与覆盖；所有科研判断由主研究者完成。

- 搜索标识：`downstream_continuation_equivalence_v008_02`
- 生成时间（协调世界时）：`2026-08-13T10:57:37.918451Z`

## 紧凑研究地图

> 跨路线按 Paper 去重；每个查询路线至多选一个尚未出现的最高排名代表项。完整原始命中保留在 `result.json`。

- Paper `P027` · Verified Critical Step Optimization for LLM Agents；用途 `problem`；路线 `q001:passage_hybrid` #1；Passage `P027:p0011:s0001`
- Paper `P074` · ToolGate: Contract-Grounded and Verified Tool Execution for LLMs；用途 `failure`；路线 `q002:passage_hybrid` #2；Passage `P074:p0012:s0001`
- Paper `P042` · LiveResearchBench: A Live Benchmark for User-Centric Deep Research in the Wild；用途 `operator`；路线 `q003:passage_hybrid` #1；Passage `P042:p0029:s0001`
- Paper `P016` · Why Do Multi-Agent LLM Systems Fail?；用途 `prior`；路线 `q004:paper_card_fts` #1；Card `paper-p016`（paper）；Evidence `ev-p016-intervention-residual-failures`, `ev-p016-mast-taxonomy`
- Paper `P071` · Agentic Plan Caching: Test-Time Memory for Fast and Cost-Efficient LLM Agents；用途 `prior`；路线 `q004:operator_card_fts` #1；Card `operator-adaptive-plan-template-reuse`（operator）；Evidence `ev-p071-cache-false-positive-boundary`, `ev-p071-plan-template-reuse`
- Paper `P077` · ArCHer: Training Language Model Agents via Hierarchical Multi-Turn RL；用途 `prior`；路线 `q004:failure_card_fts` #1；Card `failure-token-local-credit-misses-turn-level-delayed-value`（failure）；Evidence `ev-p077-hierarchical-utterance-critic-token-actor`, `ev-p077-oracle-reward-hacking-boundary`, `ev-p077-trajectory-only-sample-efficiency`
- Paper `P018` · ExpeL: LLM Agents Are Experiential Learners；用途 `prior`；路线 `q004:passage_hybrid` #1；Passage `P018:p0011:s0001`
- Paper `P057` · Automated Design of Agentic Systems；用途 `measurement`；路线 `q005:paper_card_fts` #1；Card `paper-p057`（paper）；Evidence `ev-p057-archive-code-search`, `ev-p057-search-evaluation-budget`
- Paper `P040` · From Confident Closing to Silent Failure: Characterizing False Success in LLM Agents；用途 `measurement`；路线 `q005:passage_hybrid` #1；Passage `P040:p0016:s0001`
- Paper `P058` · AFlow: Automating Agentic Workflow Generation；用途 `measurement`；路线 `q005:failure_card_fts` #1；Card `failure-reused-selection-feedback-in-agent-search`（failure）；Evidence `ev-p058-validation-selection-loop`
- Paper `P030` · STALE: Can LLM Agents Know When Their Memories Are No Longer Valid?；用途 `measurement`；路线 `q005:operator_card_fts` #2；Card `operator-write-side-state-adjudication`（operator）；Evidence `ev-p030-authorized-readout`, `ev-p030-failure-core`, `ev-p030-write-side-adjudication`

- 代表项：11 / 去重 Paper：90

## 查询与路线覆盖

### q001 · problem

- 原始查询：`旧、新工具版本可能返回结构不同但对当前任务的后续决策等价，也可能表面字段可映射却改变默认值或实体语义，导致下游智能体走向不同分支；完整响应等价过严，单次终局通过又过松。`
- 规范化查询：`"旧" OR "新工具版本可能返回结构不同但对当前任务的后续决策等价" OR "也可能表面字段可映射却改变默认值或实体语义" OR "导致下游智能体走向不同分支" OR "完整响应等价过严" OR "单次终局通过又过松"`
- 路线 `paper_card_fts`：0 条；降级 false（无）
- 路线 `failure_card_fts`：0 条；降级 false（无）
- 路线 `passage_hybrid`：100 条；降级 false（无）
- 路线 `operator_card_fts`：0 条；降级 false（无）

### q002 · failure

- 原始查询：`迁移验证没有刻画工具观测对后续智能体决策的任务条件化影响，因而误拒绝无害结构变化或误接收会改变后续分支的适配器。`
- 规范化查询：`"迁移验证没有刻画工具观测对后续智能体决策的任务条件化影响" OR "因而误拒绝无害结构变化或误接收会改变后续分支的适配器"`
- 路线 `failure_card_fts`：0 条；降级 false（无）
- 路线 `passage_hybrid`：100 条；降级 false（无）
- 路线 `operator_card_fts`：0 条；降级 false（无）
- 路线 `paper_card_fts`：0 条；降级 false（无）

### q003 · operator

- 原始查询：`从旧成功计划抽取响应到后续参数、实体绑定和分支的动态切片；在配对快照上以切片诱导的合法下一动作/分支签名定义目标条件化延续等价，并反例引导地综合最小返回适配器或新版调用子序列，无法辨识时拒绝。 对任务相关下游延续进行切片和等价判定，能比全响应比较、模式映射和最终测试更准确地区分无害结构变化与会改变智能体分支的语义漂移。`
- 规范化查询：`"从旧成功计划抽取响应到后续参数" OR "实体绑定和分支的动态切片" OR "在配对快照上以切片诱导的合法下一动作" OR "分支签名定义目标条件化延续等价" OR "并反例引导地综合最小返回适配器或新版调用子序列" OR "无法辨识时拒绝" OR "对任务相关下游延续进行切片和等价判定" OR "能比全响应比较" OR "模式映射和最终测试更准确地区分无害结构变化与会改变智能体分支的语义漂移"`
- 路线 `operator_card_fts`：0 条；降级 false（无）
- 路线 `paper_card_fts`：0 条；降级 false（无）
- 路线 `passage_hybrid`：100 条；降级 false（无）
- 路线 `failure_card_fts`：0 条；降级 false（无）

### q004 · prior

- 原始查询：`程序切片、观察等价、反例引导函数适配器综合、Sprout、M3、GUPPY、SkillRevise、Causal Agent Replay 与动作条件上下文方法可能吸收各组件；必须证明等价对象改变了候选排序或接受集合。`
- 规范化查询：`"程序切片" OR "观察等价" OR "反例引导函数适配器综合" OR "Sprout" OR "M3" OR "GUPPY" OR "SkillRevise" OR "Causal" OR "Agent" OR "Replay" OR "与动作条件上下文方法可能吸收各组件" OR "必须证明等价对象改变了候选排序或接受集合"`
- 路线 `paper_card_fts`：40 条；降级 false（无）
- 路线 `operator_card_fts`：35 条；降级 false（无）
- 路线 `failure_card_fts`：29 条；降级 false（无）
- 路线 `passage_hybrid`：100 条；降级 false（无）

### q005 · measurement

- 原始查询：`该目标函数退化为经典程序切片/适配器综合的普通观察等价；公平的 GUPPY/SkillRevise 式执行修复或新文档重新规划达到相同结果；或下一动作签名不比独立终局测试更能预测 held-out 迁移正确性。 在固定旧计划和本地语言模型上构造参数重命名、返回嵌套、默认值变化与一对多操作拆分，比较全响应相等、模式映射、终局训练测试、文档重规划和延续等价综合在未见快照的独立终局准确率与拒绝率。`
- 规范化查询：`"该目标函数退化为经典程序切片" OR "适配器综合的普通观察等价" OR "公平的" OR "GUPPY" OR "SkillRevise" OR "式执行修复或新文档重新规划达到相同结果" OR "或下一动作签名不比独立终局测试更能预测" OR "held" OR "out" OR "迁移正确性" OR "在固定旧计划和本地语言模型上构造参数重命名" OR "返回嵌套" OR "默认值变化与一对多操作拆分" OR "比较全响应相等" OR "模式映射" OR "终局训练测试" OR "文档重规划和延续等价综合在未见快照的独立终局准确率与拒绝率"`
- 路线 `paper_card_fts`：2 条；降级 false（无）
- 路线 `passage_hybrid`：100 条；降级 false（无）
- 路线 `failure_card_fts`：1 条；降级 false（无）
- 路线 `operator_card_fts`：3 条；降级 false（无）

## 覆盖诊断

- 去重 Card：105
- 去重 Evidence：129
- 去重 Passage：339
- 命中 Paper：90
- 原始观测：610
- 带机械噪声标记的观测：349
