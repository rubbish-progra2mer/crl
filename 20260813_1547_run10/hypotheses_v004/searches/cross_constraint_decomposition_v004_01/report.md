<!-- CRL_RESEARCH_SEARCH_META {"created_at_utc":"2026-08-13T09:54:50.498957Z","request_fingerprint_sha256":"e61a05cb50083f78f2e266f5850d66d7ebd47730a70d89b27507aba2c3f5b8fb","result_json_sha256":"30de5aab72298c692963aaebfa286bb4cf03ba85c2a169318a9b039377c0f564","search_id":"cross_constraint_decomposition_v004_01"} -->
# 研究检索导航

> 本报告仅展示查询路线、来源、命中定位与覆盖；所有科研判断由主研究者完成。

- 搜索标识：`cross_constraint_decomposition_v004_01`
- 生成时间（协调世界时）：`2026-08-13T09:54:50.498957Z`

## 紧凑研究地图

> 跨路线按 Paper 去重；每个查询路线至多选一个尚未出现的最高排名代表项。完整原始命中保留在 `result.json`。

- Paper `P082` · Toolformer: Language Models Can Teach Themselves to Use Tools；用途 `failure`；路线 `q001:failure_card_fts` #1；Card `failure-likelihood-utility-does-not-guarantee-agent-utility`（failure）；Evidence `ev-p082-chaining-cost-sparsity-boundary`, `ev-p082-future-token-loss-filtered-calls`, `ev-p082-top-k-single-call-boundary`
- Paper `P016` · Why Do Multi-Agent LLM Systems Fail?；用途 `failure`；路线 `q001:passage_hybrid` #1；Passage `P016:p0005:s0001`
- Paper `P020` · AgentTTS: Large Language Model Agent for Test-time Compute-optimal Scaling Strategy in Complex Tasks；用途 `failure`；路线 `q001:operator_card_fts` #1；Card `operator-subtask-compute-allocation`（operator）；Evidence `ev-p020-compute-allocation-search`
- Paper `P004` · TravelPlanner: A Benchmark for Real-World Planning with Language Agents；用途 `failure`；路线 `q001:paper_card_fts` #1；Card `paper-p004`（paper）；Evidence `ev-p004-failure-core`
- Paper `P042` · LiveResearchBench: A Live Benchmark for User-Centric Deep Research in the Wild；用途 `problem`；路线 `q002:paper_card_fts` #1；Card `paper-p042`（paper）；Evidence `ev-p042-evaluation-core`
- Paper `P083` · TAMAS: Benchmarking Adversarial Risks in Multi-Agent LLM Systems；用途 `problem`；路线 `q002:failure_card_fts` #1；Card `failure-multi-agent-adversarial-coordination-spans-trust-surfaces`（failure）；Evidence `ev-p083-lightweight-defense-failure`, `ev-p083-simulated-tool-boundary`, `ev-p083-three-surface-adversarial-failure`
- Paper `P074` · ToolGate: Contract-Grounded and Verified Tool Execution for LLMs；用途 `problem`；路线 `q002:passage_hybrid` #2；Passage `P074:p0002:s0001`
- Paper `P023` · MasRouter: Learning to Route LLMs for Multi-Agent Systems；用途 `problem`；路线 `q002:operator_card_fts` #2；Card `operator-cascaded-multiagent-meta-routing`（operator）；Evidence `ev-p023-cascaded-routing-core`, `ev-p023-operator-core`
- Paper `P051` · Large Language Models Can Solve Real-World Planning Rigorously with Formal Verification Tools；用途 `operator`；路线 `q003:operator_card_fts` #2；Card `operator-decomposed-solver-backed-formal-planning`（operator）；Evidence `ev-p051-cost-boundary`, `ev-p051-formalization-pipeline`, `ev-p051-solver-guarantee-boundary`
- Paper `P026` · Agent Lightning: Train ANY AI Agents with Reinforcement Learning；用途 `operator`；路线 `q003:paper_card_fts` #3；Card `paper-p026`（paper）；Evidence `ev-p026-transition-decomposition`, `ev-p026-uniform-terminal-return`
- Paper `P046` · Solver-Aided Verification of Policy Compliance in Tool-Augmented LLM Agents；用途 `operator`；路线 `q003:passage_hybrid` #1；Passage `P046:p0002:s0001`
- Paper `P052` · Planning Anything with Rigor: General-Purpose Zero-Shot Planning with LLM-based Formalized Programming；用途 `operator`；路线 `q003:failure_card_fts` #1；Card `failure-solver-guarantee-stops-at-formalization`（failure）；Evidence `ev-p052-direct-code-smt-baselines`, `ev-p052-implicit-constraint-failure`, `ev-p052-self-diagnosis-nontermination`
- Paper `P027` · Verified Critical Step Optimization for LLM Agents；用途 `measurement`；路线 `q004:paper_card_fts` #1；Card `paper-p027`（paper）；Evidence `ev-p027-operator-core`
- Paper `P021` · In-the-Flow Agentic System Optimization for Effective Planning and Tool Use；用途 `measurement`；路线 `q004:passage_hybrid` #2；Passage `P021:p0003:s0001`
- Paper `P054` · On the Limit of Language Models as Planning Formalizers；用途 `measurement`；路线 `q004:failure_card_fts` #1；Card `failure-constraint-shift-breaks-formalization`（failure）；Evidence `ev-p054-natural-language-implicit-predicate-failure`
- Paper `P093` · Collapse of Dense Retrievers: Short, Early, and Literal Biases Outranking Factual Evidence；用途 `measurement`；路线 `q004:operator_card_fts` #3；Card `operator-paired-single-factor-bias-decomposition`（operator）；Evidence `ev-p093-foil-collapse`, `ev-p093-paired-protocol`
- Paper `P048` · NaviAgent: Graph-Driven Bilevel Planning for Scalable Tool Orchestration；用途 `prior`；路线 `q005:paper_card_fts` #1；Card `paper-p048`（paper）；Evidence `ev-p048-operator-core`
- Paper `P090` · From Single to Multi-Granularity: Toward Long-Term Memory Association and Selection of Conversational Agents；用途 `prior`；路线 `q005:operator_card_fts` #2；Card `operator-entropy-routed-multi-granularity-retrieval`（operator）；Evidence `ev-p090-association-graph`, `ev-p090-entropy-router`
- Paper `P055` · Language Model as Planner and Formalizer under Constraints；用途 `prior`；路线 `q005:failure_card_fts` #2；Card `failure-constraint-shift-breaks-formalization`（failure）；Evidence `ev-p055-constraint-formalism-taxonomy`, `ev-p055-constraint-performance-drop`, `ev-p055-plan-correctness-false-positive-boundary`, `ev-p055-representative-subset-boundary`, `ev-p055-three-revision-budget`
- Paper `P059` · Multi-Agent Collaboration via Evolving Orchestration；用途 `prior`；路线 `q005:passage_hybrid` #2；Passage `P059:p0003:s0001`

- 代表项：20 / 去重 Paper：90

## 查询与路线覆盖

### q001 · failure

- 原始查询：`multi agent task decomposition global constraints cross subtask dependencies local success global failure handoff information loss`
- 规范化查询：`"multi" OR "agent" OR "task" OR "decomposition" OR "global" OR "constraints" OR "cross" OR "subtask" OR "dependencies" OR "local" OR "success" OR "failure" OR "handoff" OR "information" OR "loss"`
- 路线 `failure_card_fts`：30 条；降级 false（无）
- 路线 `passage_hybrid`：20 条；降级 false（无）
- 路线 `operator_card_fts`：30 条；降级 false（无）
- 路线 `paper_card_fts`：30 条；降级 false（无）

### q002 · problem

- 原始查询：`LLM multi agent delegation decomposition nonseparable constraints interface contract coordination consistency`
- 规范化查询：`"LLM" OR "multi" OR "agent" OR "delegation" OR "decomposition" OR "nonseparable" OR "constraints" OR "interface" OR "contract" OR "coordination" OR "consistency"`
- 路线 `paper_card_fts`：30 条；降级 false（无）
- 路线 `failure_card_fts`：30 条；降级 false（无）
- 路线 `passage_hybrid`：20 条；降级 false（无）
- 路线 `operator_card_fts`：30 条；降级 false（无）

### q003 · operator

- 原始查询：`constraint graph partition cut interface variables assumption guarantee contract decomposition LLM agents`
- 规范化查询：`"constraint" OR "graph" OR "partition" OR "cut" OR "interface" OR "variables" OR "assumption" OR "guarantee" OR "contract" OR "decomposition" OR "LLM" OR "agents"`
- 路线 `operator_card_fts`：30 条；降级 false（无）
- 路线 `paper_card_fts`：30 条；降级 false（无）
- 路线 `passage_hybrid`：20 条；降级 false（无）
- 路线 `failure_card_fts`：29 条；降级 false（无）

### q004 · measurement

- 原始查询：`paired decomposition cross constraint density global verifier subtask success terminal outcome`
- 规范化查询：`"paired" OR "decomposition" OR "cross" OR "constraint" OR "density" OR "global" OR "verifier" OR "subtask" OR "success" OR "terminal" OR "outcome"`
- 路线 `paper_card_fts`：30 条；降级 false（无）
- 路线 `passage_hybrid`：20 条；降级 false（无）
- 路线 `failure_card_fts`：27 条；降级 false（无）
- 路线 `operator_card_fts`：28 条；降级 false（无）

### q005 · prior

- 原始查询：`multi agent task decomposition constraint aware dependency graph contract net blackboard handoff`
- 规范化查询：`"multi" OR "agent" OR "task" OR "decomposition" OR "constraint" OR "aware" OR "dependency" OR "graph" OR "contract" OR "net" OR "blackboard" OR "handoff"`
- 路线 `paper_card_fts`：30 条；降级 false（无）
- 路线 `operator_card_fts`：30 条；降级 false（无）
- 路线 `failure_card_fts`：30 条；降级 false（无）
- 路线 `passage_hybrid`：20 条；降级 false（无）

## 覆盖诊断

- 去重 Card：173
- 去重 Evidence：200
- 去重 Passage：90
- 命中 Paper：90
- 原始观测：544
- 带机械噪声标记的观测：3
