<!-- CRL_RESEARCH_SEARCH_META {"created_at_utc":"2026-08-13T09:14:39.358366Z","request_fingerprint_sha256":"eb177911eaa3a8dd31701ce8deba83d1fa1acea8c4f39b5804c1bb0e975319e6","result_json_sha256":"ad66ce1aa24c00efcc7414bd1df3ddf1a56d3be167c6bc0a966a78fa3e4dc3a2","search_id":"orthogonal_constraint_preservation_v002"} -->
# 研究检索导航

> 本报告仅展示查询路线、来源、命中定位与覆盖；所有科研判断由主研究者完成。

- 搜索标识：`orthogonal_constraint_preservation_v002`
- 生成时间（协调世界时）：`2026-08-13T09:14:39.358366Z`

## 紧凑研究地图

> 跨路线按 Paper 去重；每个查询路线至多选一个尚未出现的最高排名代表项。完整原始命中保留在 `result.json`。

- Paper `P004` · TravelPlanner: A Benchmark for Real-World Planning with Language Agents；用途 `problem`；路线 `q001:paper_card_fts` #1；Card `paper-p004`（paper）；Evidence `ev-p004-failure-core`
- Paper `P090` · From Single to Multi-Granularity: Toward Long-Term Memory Association and Selection of Conversational Agents；用途 `problem`；路线 `q001:failure_card_fts` #2；Card `failure-fixed-single-granularity-memory`（failure）；Evidence `ev-p090-entropy-router`, `ev-p090-fixed-granularity-selection`
- Paper `P008` · Agent Security Bench (ASB): Formalizing and Benchmarking Attacks and Defenses in LLM-based Agents；用途 `problem`；路线 `q001:passage_hybrid` #1；Passage `P008:p0028:s0001`
- Paper `P025` · Unlocking the Power of Multi-Agent LLM for Reasoning: From Lazy Agents to Deliberation；用途 `problem`；路线 `q001:operator_card_fts` #1；Card `operator-grouped-masked-history-step-credit`（operator）；Evidence `ev-p025-failure-core`, `ev-p025-grouped-step-influence`
- Paper `P054` · On the Limit of Language Models as Planning Formalizers；用途 `failure`；路线 `q002:failure_card_fts` #1；Card `failure-constraint-shift-breaks-formalization`（failure）；Evidence `ev-p054-natural-language-implicit-predicate-failure`
- Paper `P098` · Beyond Objective Equivalence: Constraint Injection for LLM-Based Optimization Modeling on Vehicle Routing Problems；用途 `failure`；路线 `q002:passage_hybrid` #1；Passage `P098:p0004:s0001`
- Paper `P086` · Meta-Tool: Unleash Open-World Function Calling Capabilities of General-Purpose Large Language Models；用途 `failure`；路线 `q002:operator_card_fts` #1；Card `operator-required-parameter-description-tool-retrieval`（operator）；Evidence `ev-p086-hypothesize-retrieve-invoke`, `ev-p086-near-identical-distribution`, `ev-p086-required-parameter-score`
- Paper `P066` · The Berkeley Function Calling Leaderboard (BFCL): From Tool Use to Agentic Evaluation of Large Language Models；用途 `failure`；路线 `q002:paper_card_fts` #1；Card `paper-p066`（paper）；Evidence `ev-p066-multiturn-state-evaluation`, `ev-p066-single-to-stateful-gap`
- Paper `P030` · STALE: Can LLM Agents Know When Their Memories Are No Longer Valid?；用途 `operator`；路线 `q003:operator_card_fts` #1；Card `operator-write-side-state-adjudication`（operator）；Evidence `ev-p030-authorized-readout`, `ev-p030-failure-core`, `ev-p030-write-side-adjudication`
- Paper `P087` · Tools Are Under-Documented: Simple Document Expansion Boosts Tool Retrieval；用途 `operator`；路线 `q003:paper_card_fts` #1；Card `paper-p087`（paper）；Evidence `ev-p087-fields-not-universally-beneficial`, `ev-p087-merge-and-semantic-judge`, `ev-p087-structured-query-independent-expansion`
- Paper `P096` · VeriSimpl: Robust Optimization Modeling from Natural Language using Simplification-based Verification；用途 `operator`；路线 `q003:passage_hybrid` #1；Passage `P096:p0005:s0001`
- Paper `P076` · Multi-Agent Systems Execute Arbitrary Malicious Code；用途 `operator`；路线 `q003:failure_card_fts` #1；Card `failure-untrusted-agent-metadata-privileged-control-flow`（failure）；Evidence `ev-p076-controlled-lab-boundary`, `ev-p076-metadata-control-flow-laundering`, `ev-p076-refusal-not-system-safety`
- Paper `P062` · Agentic Memory: Learning Unified Long-Term and Short-Term Memory Management for Large Language Model Agents；用途 `prior`；路线 `q004:paper_card_fts` #1；Card `paper-p062`（paper）；Evidence `ev-p062-broadcast-advantage`, `ev-p062-unified-memory-action-policy`
- Paper `P099` · Verus-SpecGym: An Agentic Environment for Evaluating Specification Autoformalization；用途 `prior`；路线 `q004:operator_card_fts` #2；Card `operator-four-bucket-executable-spec-testing`（operator）；Evidence `ev-p099-judge-miss`, `ev-p099-soundness-necessity`, `ev-p099-two-stage-check`
- Paper `P070` · ProMCP: Profiling Token Flows and Latency Costs in Model Context Protocol-Based LLM Agents；用途 `prior`；路线 `q004:failure_card_fts` #3；Card `failure-light-tool-runtime-bottleneck-overreach`（failure）；Evidence `ev-p070-light-tool-runtime-boundary`, `ev-p070-orchestration-bottleneck`, `ev-p070-six-stage-attribution`
- Paper `P046` · Solver-Aided Verification of Policy Compliance in Tool-Augmented LLM Agents；用途 `prior`；路线 `q004:passage_hybrid` #1；Passage `P046:p0005:s0003`
- Paper `P040` · From Confident Closing to Silent Failure: Characterizing False Success in LLM Agents；用途 `measurement`；路线 `q005:paper_card_fts` #1；Card `paper-p040`（paper）；Evidence `ev-p040-failure-core`
- Paper `P047` · tau2-Bench: Evaluating Conversational Agents in a Dual-Control Environment；用途 `measurement`；路线 `q005:passage_hybrid` #1；Passage `P047:p0001:s0001`
- Paper `P081` · Self-Consistency Improves Chain of Thought Reasoning in Language Models；用途 `measurement`；路线 `q005:failure_card_fts` #2；Card `failure-interactive-gains-collapse-against-independent-sampling`（failure）；Evidence `ev-p081-fixed-answer-space-boundary`, `ev-p081-forty-sample-baseline`, `ev-p081-independent-path-majority-aggregation`
- Paper `P007` · tau-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains；用途 `measurement`；路线 `q005:operator_card_fts` #1；Card `operator-terminal-state-reliability-evaluation`（operator）；Evidence `ev-p007-terminal-state-evaluation`

- 代表项：20 / 去重 Paper：69

## 查询与路线覆盖

### q001 · problem

- 原始查询：`tool using LLM agent loses user constraints across multi step plan parameters execution`
- 规范化查询：`"tool" OR "using" OR "LLM" OR "agent" OR "loses" OR "user" OR "constraints" OR "across" OR "multi" OR "step" OR "plan" OR "parameters" OR "execution"`
- 路线 `paper_card_fts`：12 条；降级 false（无）
- 路线 `failure_card_fts`：12 条；降级 false（无）
- 路线 `passage_hybrid`：12 条；降级 false（无）
- 路线 `operator_card_fts`：12 条；降级 false（无）

### q002 · failure

- 原始查询：`parameter omission constraint drop wrong filter long horizon tool call`
- 规范化查询：`"parameter" OR "omission" OR "constraint" OR "drop" OR "wrong" OR "filter" OR "long" OR "horizon" OR "tool" OR "call"`
- 路线 `failure_card_fts`：12 条；降级 false（无）
- 路线 `passage_hybrid`：12 条；降级 false（无）
- 路线 `operator_card_fts`：12 条；降级 false（无）
- 路线 `paper_card_fts`：12 条；降级 false（无）

### q003 · operator

- 原始查询：`obligation tracking constraint provenance semantic type system tool arguments`
- 规范化查询：`"obligation" OR "tracking" OR "constraint" OR "provenance" OR "semantic" OR "type" OR "system" OR "tool" OR "arguments"`
- 路线 `operator_card_fts`：12 条；降级 false（无）
- 路线 `paper_card_fts`：12 条；降级 false（无）
- 路线 `passage_hybrid`：12 条；降级 false（无）
- 路线 `failure_card_fts`：12 条；降级 false（无）

### q004 · prior

- 原始查询：`agent runtime specification policy enforcement task constraints tool parameters`
- 规范化查询：`"agent" OR "runtime" OR "specification" OR "policy" OR "enforcement" OR "task" OR "constraints" OR "tool" OR "parameters"`
- 路线 `paper_card_fts`：12 条；降级 false（无）
- 路线 `operator_card_fts`：12 条；降级 false（无）
- 路线 `failure_card_fts`：12 条；降级 false（无）
- 路线 `passage_hybrid`：12 条；降级 false（无）

### q005 · measurement

- 原始查询：`independent state evaluation constraint satisfaction AppWorld tool agent`
- 规范化查询：`"independent" OR "state" OR "evaluation" OR "constraint" OR "satisfaction" OR "AppWorld" OR "tool" OR "agent"`
- 路线 `paper_card_fts`：12 条；降级 false（无）
- 路线 `passage_hybrid`：12 条；降级 false（无）
- 路线 `failure_card_fts`：12 条；降级 false（无）
- 路线 `operator_card_fts`：12 条；降级 false（无）

## 覆盖诊断

- 去重 Card：110
- 去重 Evidence：148
- 去重 Passage：54
- 命中 Paper：69
- 原始观测：240
- 带机械噪声标记的观测：0
