<!-- CRL_RESEARCH_SEARCH_META {"created_at_utc":"2026-08-13T12:26:52.977994Z","request_fingerprint_sha256":"0c3814afe26276241666cb1420e3bb4fe6cdfed56e81af6fdcc3b471d4bd1471","result_json_sha256":"a33ef42b2f811260dd83a6a4f59854792793b1067a16cfe9d482da2dc704e149","search_id":"v015-nonmonotone-progress"} -->
# 研究检索导航

> 本报告仅展示查询路线、来源、命中定位与覆盖；所有科研判断由主研究者完成。

- 搜索标识：`v015-nonmonotone-progress`
- 生成时间（协调世界时）：`2026-08-13T12:26:52.977994Z`

## 紧凑研究地图

> 跨路线按 Paper 去重；每个查询路线至多选一个尚未出现的最高排名代表项。完整原始命中保留在 `result.json`。

- Paper `P030` · STALE: Can LLM Agents Know When Their Memories Are No Longer Valid?；用途 `problem`；路线 `q001:paper_card_fts` #1；Card `paper-p030`（paper）；Evidence `ev-p030-failure-core`
- Paper `P060` · Unifying Inference-Time Planning Language Generation；用途 `problem`；路线 `q001:failure_card_fts` #2；Card `failure-natural-language-ir-hurts-formal-planning`（failure）；Evidence `ev-p060-formal-ir-solver`, `ev-p060-ir-result-and-nl-failure`
- Paper `P040` · From Confident Closing to Silent Failure: Characterizing False Success in LLM Agents；用途 `problem`；路线 `q001:passage_hybrid` #1；Passage `P040:p0015:s0001`
- Paper `P037` · ToolSandbox: A Stateful, Conversational, Interactive Evaluation Benchmark for LLM Tool Use Capabilities；用途 `problem`；路线 `q001:operator_card_fts` #2；Card `operator-milestone-dag-trajectory-evaluation`（operator）；Evidence `ev-p037-evaluation-core`, `ev-p037-minefield-violation`
- Paper `P025` · Unlocking the Power of Multi-Agent LLM for Reasoning: From Lazy Agents to Deliberation；用途 `failure`；路线 `q002:failure_card_fts` #1；Card `failure-lazy-agent-effective-single-agent-collapse`（failure）；Evidence `ev-p025-failure-core`
- Paper `P069` · Tool Preferences in Agentic LLMs are Unreliable；用途 `failure`；路线 `q002:passage_hybrid` #1；Passage `P069:p0006:s0001`
- Paper `P021` · In-the-Flow Agentic System Optimization for Effective Planning and Tool Use；用途 `failure`；路线 `q002:operator_card_fts` #1；Card `operator-outcome-trained-execution-state-planner`（operator）；Evidence `ev-p021-operator-core`
- Paper `P012` · Reflexion: Language Agents with Verbal Reinforcement Learning；用途 `failure`；路线 `q002:paper_card_fts` #1；Card `paper-reflexion`（paper）；Evidence `ev-p012-forced-retry-harmful-edits`, `ev-p012-verbal-reflection-memory`
- Paper `P048` · NaviAgent: Graph-Driven Bilevel Planning for Scalable Tool Orchestration；用途 `operator`；路线 `q003:operator_card_fts` #1；Card `operator-bilevel-graph-toolchain-planning`（operator）；Evidence `ev-p048-operator-core`
- Paper `P094` · Evaluating Memory in LLM Agents via Incremental Multi-Turn Interactions；用途 `operator`；路线 `q003:paper_card_fts` #1；Card `paper-p094`（paper）；Evidence `ev-p094-incremental-protocol`, `ev-p094-sf-guardrails`, `ev-p094-sf-length-collapse`
- Paper `P091` · Temporal Validity in Retrieval Memory: Eliminating Stale-Fact Errors for AI Agents over Evolving Knowledge；用途 `operator`；路线 `q003:passage_hybrid` #6；Passage `P091:p0010:s0001`
- Paper `P017` · Understanding the Information Propagation Effects of Communication Topologies in LLM-based Multi-Agent Systems；用途 `operator`；路线 `q003:failure_card_fts` #1；Card `failure-sparse-topology-suppresses-correct-insight`（failure）；Evidence `ev-p017-failure-core`
- Paper `P057` · Automated Design of Agentic Systems；用途 `prior`；路线 `q004:paper_card_fts` #1；Card `paper-p057`（paper）；Evidence `ev-p057-archive-code-search`, `ev-p057-search-evaluation-budget`
- Paper `P081` · Self-Consistency Improves Chain of Thought Reasoning in Language Models；用途 `prior`；路线 `q004:operator_card_fts` #1；Card `operator-fixed-budget-independent-path-aggregation`（operator）；Evidence `ev-p081-fixed-answer-space-boundary`, `ev-p081-forty-sample-baseline`, `ev-p081-independent-path-majority-aggregation`
- Paper `P058` · AFlow: Automating Agentic Workflow Generation；用途 `prior`；路线 `q004:failure_card_fts` #1；Card `failure-reused-selection-feedback-in-agent-search`（failure）；Evidence `ev-p058-validation-selection-loop`
- Paper `P020` · AgentTTS: Large Language Model Agent for Test-time Compute-optimal Scaling Strategy in Complex Tasks；用途 `prior`；路线 `q004:passage_hybrid` #1；Passage `P020:p0037:s0001`
- Paper `P027` · Verified Critical Step Optimization for LLM Agents；用途 `measurement`；路线 `q005:paper_card_fts` #2；Card `paper-p027`（paper）；Evidence `ev-p027-operator-core`
- Paper `P098` · Beyond Objective Equivalence: Constraint Injection for LLM-Based Optimization Modeling on Vehicle Routing Problems；用途 `measurement`；路线 `q005:passage_hybrid` #6；Passage `P098:p0019:s0001`
- Paper `P071` · Agentic Plan Caching: Test-Time Memory for Fast and Cost-Efficient LLM Agents；用途 `measurement`；路线 `q005:failure_card_fts` #3；Card `failure-plan-cache-semantic-false-positives`（failure）；Evidence `ev-p071-cache-false-positive-boundary`, `ev-p071-plan-template-reuse`
- Paper `P088` · Non-negative Elastic Net Decoding for Information Retrieval；用途 `measurement`；路线 `q005:operator_card_fts` #1；Card `operator-joint-nonnegative-residual-retrieval`（operator）；Evidence `ev-p088-joint-nonnegative-objective`, `ev-p088-relevant-set-size-signature`, `ev-p088-theory-deployment-scale-boundary`

- 代表项：20 / 去重 Paper：99

## 查询与路线覆盖

### q001 · problem

- 原始查询：`verified progress becomes stale when later agent actions invalidate earlier completed work units`
- 规范化查询：`"verified" OR "progress" OR "becomes" OR "stale" OR "when" OR "later" OR "agent" OR "actions" OR "invalidate" OR "earlier" OR "completed" OR "work" OR "units"`
- 路线 `paper_card_fts`：61 条；降级 false（无）
- 路线 `failure_card_fts`：32 条；降级 false（无）
- 路线 `passage_hybrid`：1200 条；降级 false（无）
- 路线 `operator_card_fts`：42 条；降级 false（无）

### q002 · failure

- 原始查询：`later edits regress previously passed tests or undo completed tool state`
- 规范化查询：`"later" OR "edits" OR "regress" OR "previously" OR "passed" OR "tests" OR "or" OR "undo" OR "completed" OR "tool" OR "state"`
- 路线 `failure_card_fts`：35 条；降级 false（无）
- 路线 `passage_hybrid`：1200 条；降级 false（无）
- 路线 `operator_card_fts`：38 条；降级 false（无）
- 路线 `paper_card_fts`：55 条；降级 false（无）

### q003 · operator

- 原始查询：`dynamic dependency graph change propagation selective revalidation test impact analysis incremental build`
- 规范化查询：`"dynamic" OR "dependency" OR "graph" OR "change" OR "propagation" OR "selective" OR "revalidation" OR "test" OR "impact" OR "analysis" OR "incremental" OR "build"`
- 路线 `operator_card_fts`：25 条；降级 false（无）
- 路线 `paper_card_fts`：25 条；降级 false（无）
- 路线 `passage_hybrid`：1200 条；降级 false（无）
- 路线 `failure_card_fts`：16 条；降级 false（无）

### q004 · prior

- 原始查询：`PushBench StateQGP UnitQGP self adjusting computation build systems regression test selection`
- 规范化查询：`"PushBench" OR "StateQGP" OR "UnitQGP" OR "self" OR "adjusting" OR "computation" OR "build" OR "systems" OR "regression" OR "test" OR "selection"`
- 路线 `paper_card_fts`：99 条；降级 false（无）
- 路线 `operator_card_fts`：66 条；降级 false（无）
- 路线 `failure_card_fts`：29 条；降级 false（无）
- 路线 `passage_hybrid`：1200 条；降级 false（无）

### q005 · measurement

- 原始查询：`same snapshot global completion full rerun versus minimal affected revalidation stale progress rate`
- 规范化查询：`"same" OR "snapshot" OR "global" OR "completion" OR "full" OR "rerun" OR "versus" OR "minimal" OR "affected" OR "revalidation" OR "stale" OR "progress" OR "rate"`
- 路线 `paper_card_fts`：22 条；降级 false（无）
- 路线 `passage_hybrid`：1200 条；降级 false（无）
- 路线 `failure_card_fts`：18 条；降级 false（无）
- 路线 `operator_card_fts`：13 条；降级 false（无）

## 覆盖诊断

- 去重 Card：225
- 去重 Evidence：224
- 去重 Passage：2745
- 命中 Paper：99
- 原始观测：6576
- 带机械噪声标记的观测：623
