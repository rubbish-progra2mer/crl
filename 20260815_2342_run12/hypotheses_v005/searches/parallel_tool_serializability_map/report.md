<!-- CRL_RESEARCH_SEARCH_META {"created_at_utc":"2026-08-16T06:13:38.345916Z","request_fingerprint_sha256":"728568b01e36542137767b72bbee1e8121278f0052ebe05744ac00363f0468d7","result_json_sha256":"906ee01522032dcaa23a2992c3b5243c02145865aad440148e0e7dfb696783ec","search_id":"parallel_tool_serializability_map"} -->
# 研究检索导航

> 本报告仅展示查询路线、来源、命中定位与覆盖；所有科研判断由主研究者完成。

- 搜索标识：`parallel_tool_serializability_map`
- 生成时间（协调世界时）：`2026-08-16T06:13:38.345916Z`

## 紧凑研究地图

> 跨路线按 Paper 去重；每个查询路线至多选一个尚未出现的最高排名代表项。完整原始命中保留在 `result.json`。

- Paper `P006` · An LLM Compiler for Parallel Function Calling；用途 `problem`；路线 `q001:paper_card_fts` #1；Card `paper-llmcompiler`（paper）；Evidence `ev-p006-dependency-dag-dispatch`, `ev-p006-shared-prompt-comparison-boundary`, `ev-p006-token-cost-accounting`
- Paper `P040` · From Confident Closing to Silent Failure: Characterizing False Success in LLM Agents；用途 `problem`；路线 `q001:failure_card_fts` #1；Card `failure-confident-completion-without-state-success`（failure）；Evidence `ev-p040-failure-core`
- Paper `P037` · ToolSandbox: A Stateful, Conversational, Interactive Evaluation Benchmark for LLM Tool Use Capabilities；用途 `problem`；路线 `q001:passage_hybrid` #1；Passage `P037:p0016:s0001`
- Paper `P022` · MOC: Multi-Order Communication in LLM-based Multi-Agent Systems；用途 `problem`；路线 `q001:operator_card_fts` #1；Card `operator-higher-order-message-exposure`（operator）；Evidence `ev-p022-operator-core`
- Paper `P066` · The Berkeley Function Calling Leaderboard (BFCL): From Tool Use to Agentic Evaluation of Large Language Models；用途 `failure`；路线 `q002:failure_card_fts` #1；Card `failure-single-turn-tool-score-overstates-agent-competence`（failure）；Evidence `ev-p066-multiturn-state-evaluation`, `ev-p066-single-to-stateful-gap`
- Paper `P007` · tau-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains；用途 `failure`；路线 `q002:passage_hybrid` #12；Passage `P007:p0009:s0001`
- Paper `P030` · STALE: Can LLM Agents Know When Their Memories Are No Longer Valid?；用途 `failure`；路线 `q002:operator_card_fts` #1；Card `operator-write-side-state-adjudication`（operator）；Evidence `ev-p030-authorized-readout`, `ev-p030-failure-core`, `ev-p030-write-side-adjudication`
- Paper `P085` · Retrieval Models Aren't Tool-Savvy: Benchmarking Tool Retrieval for Large Language Models；用途 `failure`；路线 `q002:paper_card_fts` #4；Card `paper-p085`（paper）；Evidence `ev-p085-large-corpus-scale`, `ev-p085-non-exhaustive-label`, `ev-p085-retrieval-completeness-failure`
- Paper `P086` · Meta-Tool: Unleash Open-World Function Calling Capabilities of General-Purpose Large Language Models；用途 `operator`；路线 `q003:operator_card_fts` #1；Card `operator-required-parameter-description-tool-retrieval`（operator）；Evidence `ev-p086-hypothesize-retrieve-invoke`, `ev-p086-near-identical-distribution`, `ev-p086-required-parameter-score`
- Paper `P039` · ToolFailBench: Diagnosing Tool-Use Failures in LLM Agents；用途 `operator`；路线 `q003:paper_card_fts` #3；Card `paper-p039`（paper）；Evidence `ev-p039-failure-core`
- Paper `P046` · Solver-Aided Verification of Policy Compliance in Tool-Augmented LLM Agents；用途 `operator`；路线 `q003:passage_hybrid` #2；Passage `P046:p0002:s0001`
- Paper `P076` · Multi-Agent Systems Execute Arbitrary Malicious Code；用途 `operator`；路线 `q003:failure_card_fts` #1；Card `failure-untrusted-agent-metadata-privileged-control-flow`（failure）；Evidence `ev-p076-controlled-lab-boundary`, `ev-p076-metadata-control-flow-laundering`, `ev-p076-refusal-not-system-safety`
- Paper `P092` · MemConflict: Evaluating Long-Term Memory Systems Under Memory Conflicts；用途 `prior`；路线 `q004:paper_card_fts` #3；Card `paper-p092`（paper）；Evidence `ev-p092-crs-low`, `ev-p092-whitebox-metrics`
- Paper `P048` · NaviAgent: Graph-Driven Bilevel Planning for Scalable Tool Orchestration；用途 `prior`；路线 `q004:operator_card_fts` #3；Card `operator-bilevel-graph-toolchain-planning`（operator）；Evidence `ev-p048-operator-core`
- Paper `P036` · tau-Knowledge: Evaluating Conversational Agents over Unstructured Knowledge；用途 `prior`；路线 `q004:failure_card_fts` #2；Card `failure-gold-context-does-not-solve-knowledge-use`（failure）；Evidence `ev-p036-failure-core`
- Paper `P035` · Holistic Agent Leaderboard: The Missing Infrastructure for AI Agent Evaluation；用途 `prior`；路线 `q004:passage_hybrid` #6；Passage `P035:p0020:s0001`
- Paper `P069` · Tool Preferences in Agentic LLMs are Unreliable；用途 `measurement`；路线 `q005:paper_card_fts` #2；Card `paper-p069`（paper）；Evidence `ev-p069-description-induced-preference`, `ev-p069-identical-tool-order-bias`
- Paper `P053` · Language Models as Higher-Order Planning Formalizers；用途 `measurement`；路线 `q005:failure_card_fts` #3；Card `failure-grounded-formalization-output-expansion`（failure）；Evidence `ev-p053-higher-order-generator`, `ev-p053-parser-evaluation-boundary`, `ev-p053-pattern-review-confound`
- Paper `P097` · ReLoop: Structured Modeling and Behavioral Verification for Reliable LLM-Based Optimization；用途 `measurement`；路线 `q005:operator_card_fts` #1；Card `operator-behavioral-perturbation-existence-test`（operator）；Evidence `ev-p097-behavioral-perturbation`, `ev-p097-feasibility-gap`

- 代表项：19 / 去重 Paper：70

## 查询与路线覆盖

### q001 · problem

- 原始查询：`LLM agent parallel tool calls shared mutable state concurrency race condition completion order`
- 规范化查询：`"LLM" OR "agent" OR "parallel" OR "tool" OR "calls" OR "shared" OR "mutable" OR "state" OR "concurrency" OR "race" OR "condition" OR "completion" OR "order"`
- 路线 `paper_card_fts`：15 条；降级 false（无）
- 路线 `failure_card_fts`：15 条；降级 false（无）
- 路线 `passage_hybrid`：15 条；降级 false（无）
- 路线 `operator_card_fts`：15 条；降级 false（无）

### q002 · failure

- 原始查询：`parallel function calling write conflict lost update non serializable tool agent`
- 规范化查询：`"parallel" OR "function" OR "calling" OR "write" OR "conflict" OR "lost" OR "update" OR "non" OR "serializable" OR "tool" OR "agent"`
- 路线 `failure_card_fts`：15 条；降级 false（无）
- 路线 `passage_hybrid`：15 条；降级 false（无）
- 路线 `operator_card_fts`：15 条；降级 false（无）
- 路线 `paper_card_fts`：15 条；降级 false（无）

### q003 · operator

- 原始查询：`commutativity serializability transactional scheduler concurrent tool invocation agent`
- 规范化查询：`"commutativity" OR "serializability" OR "transactional" OR "scheduler" OR "concurrent" OR "tool" OR "invocation" OR "agent"`
- 路线 `operator_card_fts`：15 条；降级 false（无）
- 路线 `paper_card_fts`：15 条；降级 false（无）
- 路线 `passage_hybrid`：15 条；降级 false（无）
- 路线 `failure_card_fts`：15 条；降级 false（无）

### q004 · prior

- 原始查询：`LLM agent concurrent tool use parallel tool execution dependency conflict benchmark`
- 规范化查询：`"LLM" OR "agent" OR "concurrent" OR "tool" OR "use" OR "parallel" OR "execution" OR "dependency" OR "conflict" OR "benchmark"`
- 路线 `paper_card_fts`：15 条；降级 false（无）
- 路线 `operator_card_fts`：15 条；降级 false（无）
- 路线 `failure_card_fts`：15 条；降级 false（无）
- 路线 `passage_hybrid`：15 条；降级 false（无）

### q005 · measurement

- 原始查询：`completion order permutation schedule sensitivity parallel tool calls benchmark`
- 规范化查询：`"completion" OR "order" OR "permutation" OR "schedule" OR "sensitivity" OR "parallel" OR "tool" OR "calls" OR "benchmark"`
- 路线 `paper_card_fts`：15 条；降级 false（无）
- 路线 `passage_hybrid`：15 条；降级 false（无）
- 路线 `failure_card_fts`：15 条；降级 false（无）
- 路线 `operator_card_fts`：15 条；降级 false（无）

## 覆盖诊断

- 去重 Card：117
- 去重 Evidence：140
- 去重 Passage：51
- 命中 Paper：70
- 原始观测：300
- 带机械噪声标记的观测：1
