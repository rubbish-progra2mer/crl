<!-- CRL_RESEARCH_SEARCH_META {"created_at_utc":"2026-08-15T10:22:01.289781Z","request_fingerprint_sha256":"9103154d94f84348d32850fba62351dc481a2e1018a9c97d4b72725dc405f34d","result_json_sha256":"cc415c94d5a3770446ac523e2607b826a0326ad51c2f93557f7df906bba4daef","search_id":"map-002"} -->
# 研究检索导航

> 本报告仅展示查询路线、来源、命中定位与覆盖；所有科研判断由主研究者完成。

- 搜索标识：`map-002`
- 生成时间（协调世界时）：`2026-08-15T10:22:01.289781Z`

## 紧凑研究地图

> 跨路线按 Paper 去重；每个查询路线至多选一个尚未出现的最高排名代表项。完整原始命中保留在 `result.json`。

- Paper `P039` · ToolFailBench: Diagnosing Tool-Use Failures in LLM Agents；用途 `problem`；路线 `q001:paper_card_fts` #1；Card `paper-p039`（paper）；Evidence `ev-p039-failure-core`
- Paper `P017` · Understanding the Information Propagation Effects of Communication Topologies in LLM-based Multi-Agent Systems；用途 `problem`；路线 `q001:failure_card_fts` #2；Card `failure-sparse-topology-suppresses-correct-insight`（failure）；Evidence `ev-p017-failure-core`
- Paper `P025` · Unlocking the Power of Multi-Agent LLM for Reasoning: From Lazy Agents to Deliberation；用途 `problem`；路线 `q001:passage_hybrid` #2；Passage `P025:p0004:s0002`
- Paper `P041` · LLM Agents Already Know When to Call Tools - Even Without Reasoning；用途 `problem`；路线 `q001:operator_card_fts` #1；Card `operator-hidden-state-tool-necessity-prefill`（operator）；Evidence `ev-p041-operator-core`, `ev-p041-probe-prefill-steering`
- Paper `P098` · Beyond Objective Equivalence: Constraint Injection for LLM-Based Optimization Modeling on Vehicle Routing Problems；用途 `failure`；路线 `q002:failure_card_fts` #2；Card `failure-objective-equivalence-passes-nonbinding-errors`（failure）；Evidence `ev-p098-diff-leak-550`, `ev-p098-nonbinding-blindness`, `ev-p098-open-problem`
- Paper `P089` · ToolDreamer: Instilling LLM Reasoning Into Tool Retrievers；用途 `failure`；路线 `q002:passage_hybrid` #2；Passage `P089:p0014:s0001`
- Paper `P074` · ToolGate: Contract-Grounded and Verified Tool Execution for LLMs；用途 `failure`；路线 `q002:operator_card_fts` #1；Card `operator-contract-gated-tool-state-commit`（operator）；Evidence `ev-p074-contract-state-commit`, `ev-p074-missing-schema-true-postcondition`
- Paper `P087` · Tools Are Under-Documented: Simple Document Expansion Boosts Tool Retrieval；用途 `failure`；路线 `q002:paper_card_fts` #2；Card `paper-p087`（paper）；Evidence `ev-p087-fields-not-universally-beneficial`, `ev-p087-merge-and-semantic-judge`, `ev-p087-structured-query-independent-expansion`
- Paper `P097` · ReLoop: Structured Modeling and Behavioral Verification for Reliable LLM-Based Optimization；用途 `operator`；路线 `q003:operator_card_fts` #1；Card `operator-behavioral-perturbation-existence-test`（operator）；Evidence `ev-p097-behavioral-perturbation`, `ev-p097-feasibility-gap`
- Paper `P016` · Why Do Multi-Agent LLM Systems Fail?；用途 `operator`；路线 `q003:paper_card_fts` #1；Card `paper-p016`（paper）；Evidence `ev-p016-intervention-residual-failures`, `ev-p016-mast-taxonomy`
- Paper `P095` · Don't Ask the LLM to Track Freshness: A Deterministic Recipe for Memory Conflict Resolution；用途 `operator`；路线 `q003:passage_hybrid` #3；Passage `P095:p0011:s0001`
- Paper `P062` · Agentic Memory: Learning Unified Long-Term and Short-Term Memory Management for Large Language Model Agents；用途 `operator`；路线 `q003:failure_card_fts` #1；Card `failure-unified-memory-policy-retains-terminal-credit-smearing`（failure）；Evidence `ev-p062-broadcast-advantage`, `ev-p062-unified-memory-action-policy`
- Paper `P027` · Verified Critical Step Optimization for LLM Agents；用途 `prior`；路线 `q004:paper_card_fts` #1；Card `paper-p027`（paper）；Evidence `ev-p027-operator-core`
- Paper `P092` · MemConflict: Evaluating Long-Term Memory Systems Under Memory Conflicts；用途 `prior`；路线 `q004:operator_card_fts` #2；Card `operator-support-evidence-whitebox-retrieval-metrics`（operator）；Evidence `ev-p092-crs-low`, `ev-p092-whitebox-metrics`
- Paper `P060` · Unifying Inference-Time Planning Language Generation；用途 `prior`；路线 `q004:failure_card_fts` #4；Card `failure-natural-language-ir-hurts-formal-planning`（failure）；Evidence `ev-p060-formal-ir-solver`, `ev-p060-ir-result-and-nl-failure`
- Paper `P086` · Meta-Tool: Unleash Open-World Function Calling Capabilities of General-Purpose Large Language Models；用途 `prior`；路线 `q004:passage_hybrid` #5；Passage `P086:p0006:s0001`
- Paper `P040` · From Confident Closing to Silent Failure: Characterizing False Success in LLM Agents；用途 `measurement`；路线 `q005:paper_card_fts` #1；Card `paper-p040`（paper）；Evidence `ev-p040-failure-core`
- Paper `P021` · In-the-Flow Agentic System Optimization for Effective Planning and Tool Use；用途 `measurement`；路线 `q005:passage_hybrid` #1；Passage `P021:p0032:s0001`
- Paper `P019` · STeCa: Step-level Trajectory Calibration for LLM Agent Learning；用途 `measurement`；路线 `q005:failure_card_fts` #1；Card `failure-oracle-trajectory-calibration`（failure）；Evidence `ev-p019-ground-truth-calibration-oracle`
- Paper `P007` · tau-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains；用途 `measurement`；路线 `q005:operator_card_fts` #2；Card `operator-terminal-state-reliability-evaluation`（operator）；Evidence `ev-p007-terminal-state-evaluation`

- 代表项：20 / 去重 Paper：71

## 查询与路线覆盖

### q001 · problem

- 原始查询：`causal attribution whether LLM agent actually uses tool result in final answer`
- 规范化查询：`"causal" OR "attribution" OR "whether" OR "LLM" OR "agent" OR "actually" OR "uses" OR "tool" OR "result" OR "in" OR "final" OR "answer"`
- 路线 `paper_card_fts`：10 条；降级 false（无）
- 路线 `failure_card_fts`：10 条；降级 false（无）
- 路线 `passage_hybrid`：14 条；降级 false（无）
- 路线 `operator_card_fts`：10 条；降级 false（无）

### q002 · failure

- 原始查询：`tool result ignoring spurious dependence irrelevant tool output fields`
- 规范化查询：`"tool" OR "result" OR "ignoring" OR "spurious" OR "dependence" OR "irrelevant" OR "output" OR "fields"`
- 路线 `failure_card_fts`：10 条；降级 false（无）
- 路线 `passage_hybrid`：14 条；降级 false（无）
- 路线 `operator_card_fts`：10 条；降级 false（无）
- 路线 `paper_card_fts`：10 条；降级 false（无）

### q003 · operator

- 原始查询：`counterfactual tool output perturbation metamorphic testing causal sensitivity paired interventions`
- 规范化查询：`"counterfactual" OR "tool" OR "output" OR "perturbation" OR "metamorphic" OR "testing" OR "causal" OR "sensitivity" OR "paired" OR "interventions"`
- 路线 `operator_card_fts`：10 条；降级 false（无）
- 路线 `paper_card_fts`：10 条；降级 false（无）
- 路线 `passage_hybrid`：14 条；降级 false（无）
- 路线 `failure_card_fts`：10 条；降级 false（无）

### q004 · prior

- 原始查询：`counterfactual evaluation tool agents causal tracing tool result utilization`
- 规范化查询：`"counterfactual" OR "evaluation" OR "tool" OR "agents" OR "causal" OR "tracing" OR "result" OR "utilization"`
- 路线 `paper_card_fts`：10 条；降级 false（无）
- 路线 `operator_card_fts`：10 条；降级 false（无）
- 路线 `failure_card_fts`：10 条；降级 false（无）
- 路线 `passage_hybrid`：14 条；降级 false（无）

### q005 · measurement

- 原始查询：`ground-truth-free evaluation causal tool uptake answer sensitivity`
- 规范化查询：`"ground" OR "truth" OR "free" OR "evaluation" OR "causal" OR "tool" OR "uptake" OR "answer" OR "sensitivity"`
- 路线 `paper_card_fts`：10 条；降级 false（无）
- 路线 `passage_hybrid`：14 条；降级 false（无）
- 路线 `failure_card_fts`：10 条；降级 false（无）
- 路线 `operator_card_fts`：10 条；降级 false（无）

## 覆盖诊断

- 去重 Card：93
- 去重 Evidence：125
- 去重 Passage：59
- 命中 Paper：71
- 原始观测：220
- 带机械噪声标记的观测：2
