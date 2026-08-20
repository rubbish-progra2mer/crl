<!-- CRL_RESEARCH_SEARCH_META {"created_at_utc":"2026-08-16T10:17:55.701317Z","request_fingerprint_sha256":"ec60261b2d44855401489aaf40fe03dd50ee787646c26d16d7a1c0e2bd45c0be","result_json_sha256":"52e6737fedbdff24b99728ab24fc0a58c815cbe982b26155acca9bd48d779c00","search_id":"fork-calibrated-routing-001"} -->
# 研究检索导航

> 本报告仅展示查询路线、来源、命中定位与覆盖；所有科研判断由主研究者完成。

- 搜索标识：`fork-calibrated-routing-001`
- 生成时间（协调世界时）：`2026-08-16T10:17:55.701317Z`

## 紧凑研究地图

> 跨路线按 Paper 去重；每个查询路线至多选一个尚未出现的最高排名代表项。完整原始命中保留在 `result.json`。

- Paper `P019` · STeCa: Step-level Trajectory Calibration for LLM Agent Learning；用途 `problem`；路线 `q001:paper_card_fts` #1；Card `paper-p019`（paper）；Evidence `ev-p019-ground-truth-calibration-oracle`, `ev-p019-step-level-calibration`
- Paper `P026` · Agent Lightning: Train ANY AI Agents with Reinforcement Learning；用途 `problem`；路线 `q001:failure_card_fts` #1；Card `failure-uniform-terminal-return-erases-step-credit`（failure）；Evidence `ev-p026-transition-decomposition`, `ev-p026-uniform-terminal-return`
- Paper `P064` · How Memory Management Impacts LLM Agents: An Empirical Study of Experience-Following Behavior；用途 `problem`；路线 `q001:passage_hybrid` #2；Passage `P064:p0002:s0001`
- Paper `P021` · In-the-Flow Agentic System Optimization for Effective Planning and Tool Use；用途 `problem`；路线 `q001:operator_card_fts` #1；Card `operator-outcome-trained-execution-state-planner`（operator）；Evidence `ev-p021-operator-core`
- Paper `P090` · From Single to Multi-Granularity: Toward Long-Term Memory Association and Selection of Conversational Agents；用途 `failure`；路线 `q002:failure_card_fts` #1；Card `failure-fixed-single-granularity-memory`（failure）；Evidence `ev-p090-entropy-router`, `ev-p090-fixed-granularity-selection`
- Paper `P027` · Verified Critical Step Optimization for LLM Agents；用途 `failure`；路线 `q002:passage_hybrid` #1；Passage `P027:p0002:s0001`
- Paper `P050` · Scaling Agentic Verifier for Competitive Coding；用途 `failure`；路线 `q002:operator_card_fts` #2；Card `operator-active-counterexample-verifier`（operator）；Evidence `ev-p050-operator-core`
- Paper `P025` · Unlocking the Power of Multi-Agent LLM for Reasoning: From Lazy Agents to Deliberation；用途 `failure`；路线 `q002:paper_card_fts` #2；Card `paper-p025`（paper）；Evidence `ev-p025-failure-core`
- Paper `P003` · Language Agent Tree Search Unifies Reasoning, Acting, and Planning in Language Models；用途 `operator`；路线 `q003:operator_card_fts` #3；Card `operator-feedback-backpropagated-tree-search`（operator）；Evidence `ev-p003-search-control-loop`
- Paper `P042` · LiveResearchBench: A Live Benchmark for User-Centric Deep Research in the Wild；用途 `operator`；路线 `q003:paper_card_fts` #2；Card `paper-p042`（paper）；Evidence `ev-p042-evaluation-core`
- Paper `P098` · Beyond Objective Equivalence: Constraint Injection for LLM-Based Optimization Modeling on Vehicle Routing Problems；用途 `operator`；路线 `q003:passage_hybrid` #1；Passage `P098:p0006:s0001`
- Paper `P002` · Tree of Thoughts: Deliberate Problem Solving with Large Language Models；用途 `operator`；路线 `q003:failure_card_fts` #1；Card `failure-search-resource-cost`（failure）；Evidence `ev-p002-search-resource-cost`
- Paper `P046` · Solver-Aided Verification of Policy Compliance in Tool-Augmented LLM Agents；用途 `prior`；路线 `q004:paper_card_fts` #1；Card `paper-p046`（paper）；Evidence `ev-p046-operator-core`
- Paper `P023` · MasRouter: Learning to Route LLMs for Multi-Agent Systems；用途 `prior`；路线 `q004:operator_card_fts` #1；Card `operator-cascaded-multiagent-meta-routing`（operator）；Evidence `ev-p023-cascaded-routing-core`, `ev-p023-operator-core`
- Paper `P053` · Language Models as Higher-Order Planning Formalizers；用途 `prior`；路线 `q004:failure_card_fts` #1；Card `failure-grounded-formalization-output-expansion`（failure）；Evidence `ev-p053-higher-order-generator`, `ev-p053-parser-evaluation-boundary`, `ev-p053-pattern-review-confound`
- Paper `P006` · An LLM Compiler for Parallel Function Calling；用途 `prior`；路线 `q004:passage_hybrid` #3；Passage `P006:p0004:s0005`
- Paper `P040` · From Confident Closing to Silent Failure: Characterizing False Success in LLM Agents；用途 `measurement`；路线 `q005:paper_card_fts` #1；Card `paper-p040`（paper）；Evidence `ev-p040-failure-core`
- Paper `P037` · ToolSandbox: A Stateful, Conversational, Interactive Evaluation Benchmark for LLM Tool Use Capabilities；用途 `measurement`；路线 `q005:passage_hybrid` #2；Passage `P037:p0016:s0001`
- Paper `P007` · tau-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains；用途 `measurement`；路线 `q005:failure_card_fts` #2；Card `failure-repeat-run-reliability-collapse`（failure）；Evidence `ev-p007-repeat-reliability-collapse`
- Paper `P062` · Agentic Memory: Learning Unified Long-Term and Short-Term Memory Management for Large Language Model Agents；用途 `measurement`；路线 `q005:operator_card_fts` #2；Card `operator-unified-language-memory-action-policy`（operator）；Evidence `ev-p062-broadcast-advantage`, `ev-p062-unified-memory-action-policy`

- 代表项：20 / 去重 Paper：87

## 查询与路线覆盖

### q001 · problem

- 原始查询：`per-step LLM agent model routing offline replay static logged trajectory wrong future state policy switching`
- 规范化查询：`"per" OR "step" OR "LLM" OR "agent" OR "model" OR "routing" OR "offline" OR "replay" OR "static" OR "logged" OR "trajectory" OR "wrong" OR "future" OR "state" OR "policy" OR "switching"`
- 路线 `paper_card_fts`：24 条；降级 false（无）
- 路线 `failure_card_fts`：24 条；降级 false（无）
- 路线 `passage_hybrid`：24 条；降级 false（无）
- 路线 `operator_card_fts`：24 条；降级 false（无）

### q002 · failure

- 原始查询：`agent router model swap trajectory divergence counterfactual replay noise outcome flip`
- 规范化查询：`"agent" OR "router" OR "model" OR "swap" OR "trajectory" OR "divergence" OR "counterfactual" OR "replay" OR "noise" OR "outcome" OR "flip"`
- 路线 `failure_card_fts`：24 条；降级 false（无）
- 路线 `passage_hybrid`：24 条；降级 false（无）
- 路线 `operator_card_fts`：24 条；降级 false（无）
- 路线 `paper_card_fts`：24 条；降级 false（无）

### q003 · operator

- 原始查询：`paired live branch rollout same-model control causal treatment label cost-sensitive router`
- 规范化查询：`"paired" OR "live" OR "branch" OR "rollout" OR "same" OR "model" OR "control" OR "causal" OR "treatment" OR "label" OR "cost" OR "sensitive" OR "router"`
- 路线 `operator_card_fts`：24 条；降级 false（无）
- 路线 `paper_card_fts`：24 条；降级 false（无）
- 路线 `passage_hybrid`：24 条；降级 false（无）
- 路线 `failure_card_fts`：24 条；降级 false（无）

### q004 · prior

- 原始查询：`execution grounded agent routing model cascade verifier fallback branching rollout policy evaluation`
- 规范化查询：`"execution" OR "grounded" OR "agent" OR "routing" OR "model" OR "cascade" OR "verifier" OR "fallback" OR "branching" OR "rollout" OR "policy" OR "evaluation"`
- 路线 `paper_card_fts`：24 条；降级 false（无）
- 路线 `operator_card_fts`：24 条；降级 false（无）
- 路线 `failure_card_fts`：24 条；降级 false（无）
- 路线 `passage_hybrid`：24 条；降级 false（无）

### q005 · measurement

- 原始查询：`state matched fork environment snapshot stochastic control floor trajectory divergence success cost`
- 规范化查询：`"state" OR "matched" OR "fork" OR "environment" OR "snapshot" OR "stochastic" OR "control" OR "floor" OR "trajectory" OR "divergence" OR "success" OR "cost"`
- 路线 `paper_card_fts`：24 条；降级 false（无）
- 路线 `passage_hybrid`：24 条；降级 false（无）
- 路线 `failure_card_fts`：24 条；降级 false（无）
- 路线 `operator_card_fts`：24 条；降级 false（无）

## 覆盖诊断

- 去重 Card：152
- 去重 Evidence：177
- 去重 Passage：94
- 命中 Paper：87
- 原始观测：480
- 带机械噪声标记的观测：0
