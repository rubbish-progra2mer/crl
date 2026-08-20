<!-- CRL_RESEARCH_SEARCH_META {"created_at_utc":"2026-08-18T10:39:19.023368Z","request_fingerprint_sha256":"398c70d6b0441508ea0411420018f848de1ff7ffa1ebfb7541b609bc8f25b339","result_json_sha256":"033b7d26d8a8386355cbcee29009cd805d269332f456154a201e08f9acdca752","search_id":"tool-error-recovery-map-v001"} -->
# 研究检索导航

> 本报告仅展示查询路线、来源、命中定位与覆盖；所有科研判断由主研究者完成。

- 搜索标识：`tool-error-recovery-map-v001`
- 生成时间（协调世界时）：`2026-08-18T10:39:19.023368Z`

## 紧凑研究地图

> 跨路线按 Paper 去重；每个查询路线至多选一个尚未出现的最高排名代表项。完整原始命中保留在 `result.json`。

- Paper `P049` · Reinforced Agent: Inference-Time Feedback for Tool-Calling Agents；用途 `problem`；路线 `q001:paper_card_fts` #1；Card `paper-p049`（paper）；Evidence `ev-p049-operator-core`
- Paper `P097` · ReLoop: Structured Modeling and Behavioral Verification for Reliable LLM-Based Optimization；用途 `problem`；路线 `q001:failure_card_fts` #1；Card `failure-solver-feasibility-near-zero-information-proxy`（failure）；Evidence `ev-p097-behavioral-perturbation`, `ev-p097-feasibility-gap`
- Paper `P046` · Solver-Aided Verification of Policy Compliance in Tool-Augmented LLM Agents；用途 `problem`；路线 `q001:passage_hybrid` #2；Passage `P046:p0005:s0002`
- Paper `P003` · Language Agent Tree Search Unifies Reasoning, Acting, and Planning in Language Models；用途 `problem`；路线 `q001:operator_card_fts` #2；Card `operator-feedback-backpropagated-tree-search`（operator）；Evidence `ev-p003-search-control-loop`
- Paper `P025` · Unlocking the Power of Multi-Agent LLM for Reasoning: From Lazy Agents to Deliberation；用途 `failure`；路线 `q002:failure_card_fts` #1；Card `failure-lazy-agent-effective-single-agent-collapse`（failure）；Evidence `ev-p025-failure-core`
- Paper `P040` · From Confident Closing to Silent Failure: Characterizing False Success in LLM Agents；用途 `failure`；路线 `q002:passage_hybrid` #1；Passage `P040:p0002:s0002`
- Paper `P022` · MOC: Multi-Order Communication in LLM-based Multi-Agent Systems；用途 `failure`；路线 `q002:operator_card_fts` #2；Card `operator-higher-order-message-exposure`（operator）；Evidence `ev-p022-operator-core`
- Paper `P034` · RefineBench: Evaluating Refinement Capability of Language Models via Checklists；用途 `failure`；路线 `q002:paper_card_fts` #1；Card `paper-p034`（paper）；Evidence `ev-p034-failure-core`
- Paper `P079` · Learning to Contextualize Web Pages for Enhanced Decision Making by LLM Agents；用途 `operator`；路线 `q003:operator_card_fts` #1；Card `operator-action-preserving-observation-contextualization`（operator）；Evidence `ev-p079-action-conditioned-contextualization`, `ev-p079-ground-truth-action-retry`, `ev-p079-unseen-ui-boundary`
- Paper `P012` · Reflexion: Language Agents with Verbal Reinforcement Learning；用途 `operator`；路线 `q003:paper_card_fts` #1；Card `paper-reflexion`（paper）；Evidence `ev-p012-forced-retry-harmful-edits`, `ev-p012-verbal-reflection-memory`
- Paper `P072` · Structured Uncertainty guided Clarification for LLM Agents；用途 `operator`；路线 `q003:passage_hybrid` #5；Passage `P072:p0012:s0001`
- Paper `P004` · TravelPlanner: A Benchmark for Real-World Planning with Language Agents；用途 `operator`；路线 `q003:failure_card_fts` #1；Card `failure-constrained-plan-surface-validity`（failure）；Evidence `ev-p004-failure-core`, `ev-p004-macro-constraint-failure`
- Paper `P048` · NaviAgent: Graph-Driven Bilevel Planning for Scalable Tool Orchestration；用途 `prior`；路线 `q004:paper_card_fts` #4；Card `paper-p048`（paper）；Evidence `ev-p048-operator-core`
- Paper `P068` · DeepFact: Co-Evolving Benchmarks and Agents for Deep Research Factuality；用途 `prior`；路线 `q004:operator_card_fts` #1；Card `operator-evidence-audit-before-score`（operator）；Evidence `ev-p068-audit-then-score`, `ev-p068-one-shot-gold-brittle`
- Paper `P064` · How Memory Management Impacts LLM Agents: An Empirical Study of Experience-Following Behavior；用途 `prior`；路线 `q004:failure_card_fts` #3；Card `failure-retrieved-experience-propagates-stored-errors`（failure）；Evidence `ev-p064-evaluator-reliability`, `ev-p064-experience-following-error`
- Paper `P039` · ToolFailBench: Diagnosing Tool-Use Failures in LLM Agents；用途 `prior`；路线 `q004:passage_hybrid` #1；Passage `P039:p0007:s0002`
- Paper `P093` · Collapse of Dense Retrievers: Short, Early, and Literal Biases Outranking Factual Evidence；用途 `measurement`；路线 `q005:paper_card_fts` #2；Card `paper-p093`（paper）；Evidence `ev-p093-foil-collapse`, `ev-p093-paired-protocol`, `ev-p093-poison-rag`
- Paper `P035` · Holistic Agent Leaderboard: The Missing Infrastructure for AI Agent Evaluation；用途 `measurement`；路线 `q005:passage_hybrid` #1；Passage `P035:p0009:s0001`
- Paper `P078` · CRAFT: Customizing LLMs by Creating and Retrieving from Specialized Toolsets；用途 `measurement`；路线 `q005:failure_card_fts` #2；Card `failure-generic-or-unvalidated-tool-libraries-add-distractors`（failure）；Evidence `ev-p078-baseline-fairness-boundary`, `ev-p078-generic-tool-and-baseline-boundary`, `ev-p078-multiview-tool-retrieval`, `ev-p078-toolset-construction-cost`, `ev-p078-validated-tool-creation-retrieval`
- Paper `P073` · Uncertainty Calibration for Tool-Using Language Agents；用途 `measurement`；路线 `q005:operator_card_fts` #3；Card `operator-execution-supervised-prompt-trace-calibration`（operator）；Evidence `ev-p073-execution-supervised-probe`, `ev-p073-internal-confidence-misalignment`

- 代表项：20 / 去重 Paper：60

## 查询与路线覆盖

### q001 · problem

- 原始查询：`LLM agents recover from tool execution errors observation feedback robustness`
- 规范化查询：`"LLM" OR "agents" OR "recover" OR "from" OR "tool" OR "execution" OR "errors" OR "observation" OR "feedback" OR "robustness"`
- 路线 `paper_card_fts`：10 条；降级 false（无）
- 路线 `failure_card_fts`：10 条；降级 false（无）
- 路线 `passage_hybrid`：10 条；降级 false（无）
- 路线 `operator_card_fts`：10 条；降级 false（无）

### q002 · failure

- 原始查询：`tool error messages cause repeated failure loops language agents`
- 规范化查询：`"tool" OR "error" OR "messages" OR "cause" OR "repeated" OR "failure" OR "loops" OR "language" OR "agents"`
- 路线 `failure_card_fts`：10 条；降级 false（无）
- 路线 `passage_hybrid`：10 条；降级 false（无）
- 路线 `operator_card_fts`：10 条；降级 false（无）
- 路线 `paper_card_fts`：10 条；降级 false（无）

### q003 · operator

- 原始查询：`structured error feedback retry policy tool using LLM agents`
- 规范化查询：`"structured" OR "error" OR "feedback" OR "retry" OR "policy" OR "tool" OR "using" OR "LLM" OR "agents"`
- 路线 `operator_card_fts`：10 条；降级 false（无）
- 路线 `paper_card_fts`：10 条；降级 false（无）
- 路线 `passage_hybrid`：10 条；降级 false（无）
- 路线 `failure_card_fts`：10 条；降级 false（无）

### q004 · prior

- 原始查询：`benchmark agent tool failure recovery error feedback`
- 规范化查询：`"benchmark" OR "agent" OR "tool" OR "failure" OR "recovery" OR "error" OR "feedback"`
- 路线 `paper_card_fts`：10 条；降级 false（无）
- 路线 `operator_card_fts`：10 条；降级 false（无）
- 路线 `failure_card_fts`：10 条；降级 false（无）
- 路线 `passage_hybrid`：10 条；降级 false（无）

### q005 · measurement

- 原始查询：`paired task success after informative versus generic tool errors`
- 规范化查询：`"paired" OR "task" OR "success" OR "after" OR "informative" OR "versus" OR "generic" OR "tool" OR "errors"`
- 路线 `paper_card_fts`：10 条；降级 false（无）
- 路线 `passage_hybrid`：10 条；降级 false（无）
- 路线 `failure_card_fts`：10 条；降级 false（无）
- 路线 `operator_card_fts`：10 条；降级 false（无）

## 覆盖诊断

- 去重 Card：89
- 去重 Evidence：106
- 去重 Passage：38
- 命中 Paper：60
- 原始观测：200
- 带机械噪声标记的观测：0
