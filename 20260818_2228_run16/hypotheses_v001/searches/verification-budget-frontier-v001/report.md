<!-- CRL_RESEARCH_SEARCH_META {"created_at_utc":"2026-08-18T15:41:23.686573Z","request_fingerprint_sha256":"c7e98f42b6e00f0dd9d7b0566be6a29c2332321e07e6cec433450a3d07d7f0cb","result_json_sha256":"dc8bbcdb690e662c4a0a33b234ee955962e3b4c43f6680f1c7f715fb0c5c67f2","search_id":"verification-budget-frontier-v001"} -->
# 研究检索导航

> 本报告仅展示查询路线、来源、命中定位与覆盖；所有科研判断由主研究者完成。

- 搜索标识：`verification-budget-frontier-v001`
- 生成时间（协调世界时）：`2026-08-18T15:41:23.686573Z`

## 紧凑研究地图

> 跨路线按 Paper 去重；每个查询路线至多选一个尚未出现的最高排名代表项。完整原始命中保留在 `result.json`。

- Paper `P073` · Uncertainty Calibration for Tool-Using Language Agents；用途 `problem`；路线 `q001:paper_card_fts` #1；Card `paper-p073`（paper）；Evidence `ev-p073-execution-supervised-probe`, `ev-p073-internal-confidence-misalignment`
- Paper `P069` · Tool Preferences in Agentic LLMs are Unreliable；用途 `problem`；路线 `q001:failure_card_fts` #1；Card `failure-tool-description-and-order-bias`（failure）；Evidence `ev-p069-description-induced-preference`, `ev-p069-identical-tool-order-bias`
- Paper `P083` · TAMAS: Benchmarking Adversarial Risks in Multi-Agent LLM Systems；用途 `problem`；路线 `q001:passage_hybrid` #1；Passage `P083:p0016:s0001`
- Paper `P007` · tau-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains；用途 `problem`；路线 `q001:operator_card_fts` #1；Card `operator-terminal-state-reliability-evaluation`（operator）；Evidence `ev-p007-terminal-state-evaluation`
- Paper `P040` · From Confident Closing to Silent Failure: Characterizing False Success in LLM Agents；用途 `failure`；路线 `q002:failure_card_fts` #1；Card `failure-confident-completion-without-state-success`（failure）；Evidence `ev-p040-failure-core`
- Paper `P036` · tau-Knowledge: Evaluating Conversational Agents over Unstructured Knowledge；用途 `failure`；路线 `q002:passage_hybrid` #2；Passage `P036:p0005:s0001`
- Paper `P042` · LiveResearchBench: A Live Benchmark for User-Centric Deep Research in the Wild；用途 `failure`；路线 `q002:operator_card_fts` #1；Card `operator-decomposed-research-evidence-evaluation`（operator）；Evidence `ev-p042-evaluation-core`
- Paper `P043` · DeepResearch Bench: A Comprehensive Benchmark for Deep Research Agents；用途 `failure`；路线 `q002:paper_card_fts` #1；Card `paper-p043`（paper）；Evidence `ev-p043-evaluation-core`
- Paper `P023` · MasRouter: Learning to Route LLMs for Multi-Agent Systems；用途 `operator`；路线 `q003:operator_card_fts` #1；Card `operator-cascaded-multiagent-meta-routing`（operator）；Evidence `ev-p023-cascaded-routing-core`, `ev-p023-operator-core`
- Paper `P046` · Solver-Aided Verification of Policy Compliance in Tool-Augmented LLM Agents；用途 `operator`；路线 `q003:paper_card_fts` #1；Card `paper-p046`（paper）；Evidence `ev-p046-operator-core`
- Paper `P051` · Large Language Models Can Solve Real-World Planning Rigorously with Formal Verification Tools；用途 `operator`；路线 `q003:passage_hybrid` #1；Passage `P051:p0016:s0001`
- Paper `P033` · Self-Refine: Iterative Refinement with Self-Feedback；用途 `operator`；路线 `q003:failure_card_fts` #1；Card `failure-iterative-refinement-corrupts-correct-output`（failure）；Evidence `ev-p033-operator-core`
- Paper `P074` · ToolGate: Contract-Grounded and Verified Tool Execution for LLMs；用途 `prior`；路线 `q004:paper_card_fts` #2；Card `paper-p074`（paper）；Evidence `ev-p074-contract-state-commit`, `ev-p074-missing-schema-true-postcondition`
- Paper `P098` · Beyond Objective Equivalence: Constraint Injection for LLM-Based Optimization Modeling on Vehicle Routing Problems；用途 `prior`；路线 `q004:operator_card_fts` #1；Card `operator-labeled-probe-injection-dual-verifier`（operator）；Evidence `ev-p098-constraint-injection`, `ev-p098-diff-leak-550`, `ev-p098-nonbinding-blindness`
- Paper `P034` · RefineBench: Evaluating Refinement Capability of Language Models via Checklists；用途 `prior`；路线 `q004:failure_card_fts` #2；Card `failure-iterative-refinement-corrupts-correct-output`（failure）；Evidence `ev-p034-failure-core`
- Paper `P016` · Why Do Multi-Agent LLM Systems Fail?；用途 `prior`；路线 `q004:passage_hybrid` #3；Passage `P016:p0032:s0001`
- Paper `P006` · An LLM Compiler for Parallel Function Calling；用途 `measurement`；路线 `q005:paper_card_fts` #2；Card `paper-llmcompiler`（paper）；Evidence `ev-p006-dependency-dag-dispatch`, `ev-p006-shared-prompt-comparison-boundary`, `ev-p006-token-cost-accounting`
- Paper `P035` · Holistic Agent Leaderboard: The Missing Infrastructure for AI Agent Evaluation；用途 `measurement`；路线 `q005:passage_hybrid` #1；Passage `P035:p0008:s0001`
- Paper `P071` · Agentic Plan Caching: Test-Time Memory for Fast and Cost-Efficient LLM Agents；用途 `measurement`；路线 `q005:failure_card_fts` #1；Card `failure-plan-cache-semantic-false-positives`（failure）；Evidence `ev-p071-cache-false-positive-boundary`, `ev-p071-plan-template-reuse`
- Paper `P101` · Semantic Evaluation for Text-to-SQL with Distilled Test Suites；用途 `measurement`；路线 `q005:operator_card_fts` #1；Card `operator-neighbor-distilled-test-suites`（operator）；Evidence `ev-p101-esm-fn-rate`, `ev-p101-neighbor-distillation`

- 代表项：20 / 去重 Paper：64

## 查询与路线覆盖

### q001 · problem

- 原始查询：`tool-using LLM agent state verification hidden side effects under verification budget`
- 规范化查询：`"tool" OR "using" OR "LLM" OR "agent" OR "state" OR "verification" OR "hidden" OR "side" OR "effects" OR "under" OR "budget"`
- 路线 `paper_card_fts`：10 条；降级 false（无）
- 路线 `failure_card_fts`：10 条；降级 false（无）
- 路线 `passage_hybrid`：10 条；降级 false（无）
- 路线 `operator_card_fts`：10 条；降级 false（无）

### q002 · failure

- 原始查询：`task reports success while unintended state changes remain unobserved`
- 规范化查询：`"task" OR "reports" OR "success" OR "while" OR "unintended" OR "state" OR "changes" OR "remain" OR "unobserved"`
- 路线 `failure_card_fts`：10 条；降级 false（无）
- 路线 `passage_hybrid`：10 条；降级 false（无）
- 路线 `operator_card_fts`：10 条；降级 false（无）
- 路线 `paper_card_fts`：10 条；降级 false（无）

### q003 · operator

- 原始查询：`select minimal deterministic state predicates or verification queries under cost budget`
- 规范化查询：`"select" OR "minimal" OR "deterministic" OR "state" OR "predicates" OR "or" OR "verification" OR "queries" OR "under" OR "cost" OR "budget"`
- 路线 `operator_card_fts`：10 条；降级 false（无）
- 路线 `paper_card_fts`：10 条；降级 false（无）
- 路线 `passage_hybrid`：10 条；降级 false（无）
- 路线 `failure_card_fts`：10 条；降级 false（无）

### q004 · prior

- 原始查询：`state diff contracts adaptive verification selective verification tool agents`
- 规范化查询：`"state" OR "diff" OR "contracts" OR "adaptive" OR "verification" OR "selective" OR "tool" OR "agents"`
- 路线 `paper_card_fts`：10 条；降级 false（无）
- 路线 `operator_card_fts`：10 条；降级 false（无）
- 路线 `failure_card_fts`：10 条；降级 false（无）
- 路线 `passage_hybrid`：10 条；降级 false（无）

### q005 · measurement

- 原始查询：`false-negative rate verification coverage cost task success unintended writes`
- 规范化查询：`"false" OR "negative" OR "rate" OR "verification" OR "coverage" OR "cost" OR "task" OR "success" OR "unintended" OR "writes"`
- 路线 `paper_card_fts`：10 条；降级 false（无）
- 路线 `passage_hybrid`：10 条；降级 false（无）
- 路线 `failure_card_fts`：10 条；降级 false（无）
- 路线 `operator_card_fts`：10 条；降级 false（无）

## 覆盖诊断

- 去重 Card：92
- 去重 Evidence：114
- 去重 Passage：46
- 命中 Paper：64
- 原始观测：200
- 带机械噪声标记的观测：0
