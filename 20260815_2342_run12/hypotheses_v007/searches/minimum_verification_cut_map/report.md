<!-- CRL_RESEARCH_SEARCH_META {"created_at_utc":"2026-08-16T06:52:28.479118Z","request_fingerprint_sha256":"d7b8049bca1c576d3d34acc9104ca6046ca68bb2ab45ea6e1e451fac6a0eb879","result_json_sha256":"1d531fe1a082d59c11a79ef8af1e1af91bedac2bd3198662285bd28b84010212","search_id":"minimum_verification_cut_map"} -->
# 研究检索导航

> 本报告仅展示查询路线、来源、命中定位与覆盖；所有科研判断由主研究者完成。

- 搜索标识：`minimum_verification_cut_map`
- 生成时间（协调世界时）：`2026-08-16T06:52:28.479118Z`

## 紧凑研究地图

> 跨路线按 Paper 去重；每个查询路线至多选一个尚未出现的最高排名代表项。完整原始命中保留在 `result.json`。

- Paper `P048` · NaviAgent: Graph-Driven Bilevel Planning for Scalable Tool Orchestration；用途 `problem`；路线 `q001:paper_card_fts` #1；Card `paper-p048`（paper）；Evidence `ev-p048-operator-core`
- Paper `P004` · TravelPlanner: A Benchmark for Real-World Planning with Language Agents；用途 `problem`；路线 `q001:failure_card_fts` #1；Card `failure-constrained-plan-surface-validity`（failure）；Evidence `ev-p004-failure-core`, `ev-p004-macro-constraint-failure`
- Paper `P076` · Multi-Agent Systems Execute Arbitrary Malicious Code；用途 `problem`；路线 `q001:passage_hybrid` #1；Passage `P076:p0010:s0001`
- Paper `P057` · Automated Design of Agentic Systems；用途 `problem`；路线 `q001:operator_card_fts` #2；Card `operator-archive-conditioned-agent-code-search`（operator）；Evidence `ev-p057-archive-code-search`, `ev-p057-search-evaluation-budget`
- Paper `P037` · ToolSandbox: A Stateful, Conversational, Interactive Evaluation Benchmark for LLM Tool Use Capabilities；用途 `operator`；路线 `q002:operator_card_fts` #1；Card `operator-milestone-dag-trajectory-evaluation`（operator）；Evidence `ev-p037-evaluation-core`, `ev-p037-minefield-violation`
- Paper `P006` · An LLM Compiler for Parallel Function Calling；用途 `operator`；路线 `q002:paper_card_fts` #1；Card `paper-llmcompiler`（paper）；Evidence `ev-p006-dependency-dag-dispatch`, `ev-p006-shared-prompt-comparison-boundary`, `ev-p006-token-cost-accounting`
- Paper `P035` · Holistic Agent Leaderboard: The Missing Infrastructure for AI Agent Evaluation；用途 `operator`；路线 `q002:passage_hybrid` #1；Passage `P035:p0028:s0001`
- Paper `P074` · ToolGate: Contract-Grounded and Verified Tool Execution for LLMs；用途 `operator`；路线 `q002:failure_card_fts` #1；Card `failure-incomplete-tool-contracts-false-verified-state`（failure）；Evidence `ev-p074-contract-state-commit`, `ev-p074-missing-schema-true-postcondition`
- Paper `P026` · Agent Lightning: Train ANY AI Agents with Reinforcement Learning；用途 `prior`；路线 `q003:paper_card_fts` #1；Card `paper-p026`（paper）；Evidence `ev-p026-transition-decomposition`, `ev-p026-uniform-terminal-return`
- Paper `P022` · MOC: Multi-Order Communication in LLM-based Multi-Agent Systems；用途 `prior`；路线 `q003:operator_card_fts` #2；Card `operator-higher-order-message-exposure`（operator）；Evidence `ev-p022-operator-core`
- Paper `P033` · Self-Refine: Iterative Refinement with Self-Feedback；用途 `prior`；路线 `q003:failure_card_fts` #1；Card `failure-iterative-refinement-corrupts-correct-output`（failure）；Evidence `ev-p033-operator-core`
- Paper `P016` · Why Do Multi-Agent LLM Systems Fail?；用途 `prior`；路线 `q003:passage_hybrid` #1；Passage `P016:p0032:s0001`
- Paper `P005` · ToolLLM: Facilitating Large Language Models to Master 16000+ Real-world APIs；用途 `measurement`；路线 `q004:paper_card_fts` #1；Card `paper-p005`（paper）；Evidence `ev-p005-operator-core`
- Paper `P068` · DeepFact: Co-Evolving Benchmarks and Agents for Deep Research Factuality；用途 `measurement`；路线 `q004:passage_hybrid` #1；Passage `P068:p0014:s0001`
- Paper `P081` · Self-Consistency Improves Chain of Thought Reasoning in Language Models；用途 `measurement`；路线 `q004:failure_card_fts` #1；Card `failure-interactive-gains-collapse-against-independent-sampling`（failure）；Evidence `ev-p081-fixed-answer-space-boundary`, `ev-p081-forty-sample-baseline`, `ev-p081-independent-path-majority-aggregation`
- Paper `P065` · Group-in-Group Policy Optimization for LLM Agent Training；用途 `measurement`；路线 `q004:operator_card_fts` #2；Card `operator-anchor-state-relative-credit`（operator）；Evidence `ev-p065-anchor-state-credit`, `ev-p065-state-recurrence-boundary`

- 代表项：16 / 去重 Paper：76

## 查询与路线覆盖

### q001 · problem

- 原始查询：`limited verification budget tool agent dependency graph untrusted observations irreversible actions`
- 规范化查询：`"limited" OR "verification" OR "budget" OR "tool" OR "agent" OR "dependency" OR "graph" OR "untrusted" OR "observations" OR "irreversible" OR "actions"`
- 路线 `paper_card_fts`：15 条；降级 false（无）
- 路线 `failure_card_fts`：15 条；降级 false（无）
- 路线 `passage_hybrid`：20 条；降级 false（无）
- 路线 `operator_card_fts`：15 条；降级 false（无）

### q002 · operator

- 原始查询：`minimum cut verification witness placement provenance dependency DAG commit barrier`
- 规范化查询：`"minimum" OR "cut" OR "verification" OR "witness" OR "placement" OR "provenance" OR "dependency" OR "DAG" OR "commit" OR "barrier"`
- 路线 `operator_card_fts`：13 条；降级 false（无）
- 路线 `paper_card_fts`：15 条；降级 false（无）
- 路线 `passage_hybrid`：20 条；降级 false（无）
- 路线 `failure_card_fts`：9 条；降级 false（无）

### q003 · prior

- 原始查询：`agent selective verification budget graph cut critical transition risk-aware monitor placement`
- 规范化查询：`"agent" OR "selective" OR "verification" OR "budget" OR "graph" OR "cut" OR "critical" OR "transition" OR "risk" OR "aware" OR "monitor" OR "placement"`
- 路线 `paper_card_fts`：15 条；降级 false（无）
- 路线 `operator_card_fts`：15 条；降级 false（无）
- 路线 `failure_card_fts`：15 条；降级 false（无）
- 路线 `passage_hybrid`：20 条；降级 false（无）

### q004 · measurement

- 原始查询：`verification coverage every path untrusted evidence to irreversible sink equal budget`
- 规范化查询：`"verification" OR "coverage" OR "every" OR "path" OR "untrusted" OR "evidence" OR "to" OR "irreversible" OR "sink" OR "equal" OR "budget"`
- 路线 `paper_card_fts`：15 条；降级 false（无）
- 路线 `passage_hybrid`：20 条；降级 false（无）
- 路线 `failure_card_fts`：15 条；降级 false（无）
- 路线 `operator_card_fts`：15 条；降级 false（无）

## 覆盖诊断

- 去重 Card：97
- 去重 Evidence：137
- 去重 Passage：76
- 命中 Paper：76
- 原始观测：252
- 带机械噪声标记的观测：1
