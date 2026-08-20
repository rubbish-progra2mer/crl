<!-- CRL_RESEARCH_SEARCH_META {"created_at_utc":"2026-08-16T07:24:58.960129Z","request_fingerprint_sha256":"89b86f91545def6485b2db918c1d7d712d8badf940b62466f23ea11e12c80c78","result_json_sha256":"f17ed63e86b6e19356408091e514963a992b1f9bc662080f503bcfe23f228270","search_id":"stage_boundary_cue_map"} -->
# 研究检索导航

> 本报告仅展示查询路线、来源、命中定位与覆盖；所有科研判断由主研究者完成。

- 搜索标识：`stage_boundary_cue_map`
- 生成时间（协调世界时）：`2026-08-16T07:24:58.960129Z`

## 紧凑研究地图

> 跨路线按 Paper 去重；每个查询路线至多选一个尚未出现的最高排名代表项。完整原始命中保留在 `result.json`。

- Paper `P040` · From Confident Closing to Silent Failure: Characterizing False Success in LLM Agents；用途 `problem`；路线 `q001:paper_card_fts` #1；Card `paper-p040`（paper）；Evidence `ev-p040-failure-core`
- Paper `P094` · Evaluating Memory in LLM Agents via Incremental Multi-Turn Interactions；用途 `problem`；路线 `q001:failure_card_fts` #2；Card `failure-selective-forgetting-collapses-with-context-length`（failure）；Evidence `ev-p094-sf-guardrails`, `ev-p094-sf-length-collapse`
- Paper `P070` · ProMCP: Profiling Token Flows and Latency Costs in Model Context Protocol-Based LLM Agents；用途 `problem`；路线 `q001:passage_hybrid` #1；Passage `P070:p0004:s0001`
- Paper `P021` · In-the-Flow Agentic System Optimization for Effective Planning and Tool Use；用途 `problem`；路线 `q001:operator_card_fts` #3；Card `operator-outcome-trained-execution-state-planner`（operator）；Evidence `ev-p021-operator-core`
- Paper `P076` · Multi-Agent Systems Execute Arbitrary Malicious Code；用途 `failure`；路线 `q002:failure_card_fts` #1；Card `failure-untrusted-agent-metadata-privileged-control-flow`（failure）；Evidence `ev-p076-controlled-lab-boundary`, `ev-p076-metadata-control-flow-laundering`, `ev-p076-refusal-not-system-safety`
- Paper `P035` · Holistic Agent Leaderboard: The Missing Infrastructure for AI Agent Evaluation；用途 `failure`；路线 `q002:passage_hybrid` #1；Passage `P035:p0028:s0001`
- Paper `P086` · Meta-Tool: Unleash Open-World Function Calling Capabilities of General-Purpose Large Language Models；用途 `failure`；路线 `q002:operator_card_fts` #1；Card `operator-required-parameter-description-tool-retrieval`（operator）；Evidence `ev-p086-hypothesize-retrieve-invoke`, `ev-p086-near-identical-distribution`, `ev-p086-required-parameter-score`
- Paper `P066` · The Berkeley Function Calling Leaderboard (BFCL): From Tool Use to Agentic Evaluation of Large Language Models；用途 `failure`；路线 `q002:paper_card_fts` #2；Card `paper-p066`（paper）；Evidence `ev-p066-multiturn-state-evaluation`, `ev-p066-single-to-stateful-gap`
- Paper `P022` · MOC: Multi-Order Communication in LLM-based Multi-Agent Systems；用途 `operator`；路线 `q003:operator_card_fts` #1；Card `operator-higher-order-message-exposure`（operator）；Evidence `ev-p022-operator-core`
- Paper `P023` · MasRouter: Learning to Route LLMs for Multi-Agent Systems；用途 `operator`；路线 `q003:paper_card_fts` #1；Card `paper-p023`（paper）；Evidence `ev-p023-operator-core`
- Paper `P059` · Multi-Agent Collaboration via Evolving Orchestration；用途 `operator`；路线 `q003:passage_hybrid` #1；Passage `P059:p0021:s0001`
- Paper `P098` · Beyond Objective Equivalence: Constraint Injection for LLM-Based Optimization Modeling on Vehicle Routing Problems；用途 `operator`；路线 `q003:failure_card_fts` #1；Card `failure-objective-equivalence-passes-nonbinding-errors`（failure）；Evidence `ev-p098-diff-leak-550`, `ev-p098-nonbinding-blindness`, `ev-p098-open-problem`
- Paper `P039` · ToolFailBench: Diagnosing Tool-Use Failures in LLM Agents；用途 `prior`；路线 `q004:paper_card_fts` #4；Card `paper-p039`（paper）；Evidence `ev-p039-failure-core`
- Paper `P007` · tau-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains；用途 `prior`；路线 `q004:operator_card_fts` #1；Card `operator-terminal-state-reliability-evaluation`（operator）；Evidence `ev-p007-terminal-state-evaluation`
- Paper `P085` · Retrieval Models Aren't Tool-Savvy: Benchmarking Tool Retrieval for Large Language Models；用途 `prior`；路线 `q004:failure_card_fts` #4；Card `failure-large-corpus-tool-retrieval-breaks-oracle-menu`（failure）；Evidence `ev-p085-large-corpus-scale`, `ev-p085-non-exhaustive-label`, `ev-p085-retrieval-completeness-failure`
- Paper `P047` · tau2-Bench: Evaluating Conversational Agents in a Dual-Control Environment；用途 `prior`；路线 `q004:passage_hybrid` #6；Passage `P047:p0020:s0001`
- Paper `P074` · ToolGate: Contract-Grounded and Verified Tool Execution for LLMs；用途 `measurement`；路线 `q005:paper_card_fts` #1；Card `paper-p074`（paper）；Evidence `ev-p074-contract-state-commit`, `ev-p074-missing-schema-true-postcondition`
- Paper `P083` · TAMAS: Benchmarking Adversarial Risks in Multi-Agent LLM Systems；用途 `measurement`；路线 `q005:passage_hybrid` #1；Passage `P083:p0006:s0001`
- Paper `P011` · On Memory Construction and Retrieval for Personalized Conversational Agents；用途 `measurement`；路线 `q005:failure_card_fts` #1；Card `failure-memory-unit-granularity-mismatch`（failure）；Evidence `ev-p011-failure-core`
- Paper `P093` · Collapse of Dense Retrievers: Short, Early, and Literal Biases Outranking Factual Evidence；用途 `measurement`；路线 `q005:operator_card_fts` #3；Card `operator-paired-single-factor-bias-decomposition`（operator）；Evidence `ev-p093-foil-collapse`, `ev-p093-paired-protocol`

- 代表项：20 / 去重 Paper：77

## 查询与路线覆盖

### q001 · problem

- 原始查询：`tool protocol stage boundary cue causes premature completion despite remaining explicit obligations`
- 规范化查询：`"tool" OR "protocol" OR "stage" OR "boundary" OR "cue" OR "causes" OR "premature" OR "completion" OR "despite" OR "remaining" OR "explicit" OR "obligations"`
- 路线 `paper_card_fts`：12 条；降级 false（无）
- 路线 `failure_card_fts`：12 条；降级 false（无）
- 路线 `passage_hybrid`：24 条；降级 false（无）
- 路线 `operator_card_fts`：12 条；降级 false（无）

### q002 · failure

- 原始查询：`action linked status metadata overrides missing required tool call`
- 规范化查询：`"action" OR "linked" OR "status" OR "metadata" OR "overrides" OR "missing" OR "required" OR "tool" OR "call"`
- 路线 `failure_card_fts`：12 条；降级 false（无）
- 路线 `passage_hybrid`：24 条；降级 false（无）
- 路线 `operator_card_fts`：12 条；降级 false（无）
- 路线 `paper_card_fts`：12 条；降级 false（无）

### q003 · operator

- 原始查询：`causal factorial tool identity action binding message role neutral status`
- 规范化查询：`"causal" OR "factorial" OR "tool" OR "identity" OR "action" OR "binding" OR "message" OR "role" OR "neutral" OR "status"`
- 路线 `operator_card_fts`：12 条；降级 false（无）
- 路线 `paper_card_fts`：12 条；降级 false（无）
- 路线 `passage_hybrid`：24 条；降级 false（无）
- 路线 `failure_card_fts`：12 条；降级 false（无）

### q004 · prior

- 原始查询：`false success required call coverage completion check metadata control flow laundering task completion detection`
- 规范化查询：`"false" OR "success" OR "required" OR "call" OR "coverage" OR "completion" OR "check" OR "metadata" OR "control" OR "flow" OR "laundering" OR "task" OR "detection"`
- 路线 `paper_card_fts`：12 条；降级 false（无）
- 路线 `operator_card_fts`：12 条；降级 false（无）
- 路线 `failure_card_fts`：12 条；降级 false（无）
- 路线 `passage_hybrid`：24 条；降级 false（无）

### q005 · measurement

- 原始查询：`paired intervention same action unrelated action summary tool audit tool plain message unsafe commit`
- 规范化查询：`"paired" OR "intervention" OR "same" OR "action" OR "unrelated" OR "summary" OR "tool" OR "audit" OR "plain" OR "message" OR "unsafe" OR "commit"`
- 路线 `paper_card_fts`：12 条；降级 false（无）
- 路线 `passage_hybrid`：24 条；降级 false（无）
- 路线 `failure_card_fts`：12 条；降级 false（无）
- 路线 `operator_card_fts`：12 条；降级 false（无）

## 覆盖诊断

- 去重 Card：117
- 去重 Evidence：160
- 去重 Passage：104
- 命中 Paper：77
- 原始观测：300
- 带机械噪声标记的观测：1
