<!-- CRL_RESEARCH_SEARCH_META {"created_at_utc":"2026-08-15T16:09:53.192423Z","request_fingerprint_sha256":"19cc3ee5c3833bc0f9ae534501fc6fb508998e66394ccc21b2e2fd64fd3595e2","result_json_sha256":"2d84ba1dcdbac124e009695de16eef013df05cac098cc23025c171d6ccac8ae1","search_id":"h005_plan_cache_counterfactual"} -->
# 研究检索导航

> 本报告仅展示查询路线、来源、命中定位与覆盖；所有科研判断由主研究者完成。

- 搜索标识：`h005_plan_cache_counterfactual`
- 生成时间（协调世界时）：`2026-08-15T16:09:53.192423Z`

## 紧凑研究地图

> 跨路线按 Paper 去重；每个查询路线至多选一个尚未出现的最高排名代表项。完整原始命中保留在 `result.json`。

- Paper `P071` · Agentic Plan Caching: Test-Time Memory for Fast and Cost-Efficient LLM Agents；用途 `problem`；路线 `q001:paper_card_fts` #1；Card `paper-p071`（paper）；Evidence `ev-p071-cache-false-positive-boundary`, `ev-p071-plan-template-reuse`
- Paper `P067` · AgentHarm: A Benchmark for Measuring Harmfulness of LLM Agents；用途 `problem`；路线 `q001:failure_card_fts` #2；Card `failure-chatbot-refusal-does-not-establish-agent-safety`（failure）；Evidence `ev-p067-agentic-harm-not-chat-refusal`, `ev-p067-capability-preserving-safety`
- Paper `P035` · Holistic Agent Leaderboard: The Missing Infrastructure for AI Agent Evaluation；用途 `problem`；路线 `q001:passage_hybrid` #24；Passage `P035:p0021:s0001`
- Paper `P048` · NaviAgent: Graph-Driven Bilevel Planning for Scalable Tool Orchestration；用途 `problem`；路线 `q001:operator_card_fts` #2；Card `operator-bilevel-graph-toolchain-planning`（operator）；Evidence `ev-p048-operator-core`
- Paper `P051` · Large Language Models Can Solve Real-World Planning Rigorously with Formal Verification Tools；用途 `failure`；路线 `q002:failure_card_fts` #2；Card `failure-solver-guarantee-stops-at-formalization`（failure）；Evidence `ev-p051-omitted-constraint-failure`, `ev-p051-solver-guarantee-boundary`
- Paper `P055` · Language Model as Planner and Formalizer under Constraints；用途 `failure`；路线 `q002:passage_hybrid` #1；Passage `P055:p0004:s0001`
- Paper `P027` · Verified Critical Step Optimization for LLM Agents；用途 `failure`；路线 `q002:operator_card_fts` #2；Card `operator-verified-single-branch-repair`（operator）；Evidence `ev-p027-operator-core`
- Paper `P054` · On the Limit of Language Models as Planning Formalizers；用途 `failure`；路线 `q002:paper_card_fts` #3；Card `paper-p054`（paper）；Evidence `ev-p054-complete-pddl-formalizer`, `ev-p054-model-conditional-advantage`, `ev-p054-natural-language-implicit-predicate-failure`, `ev-p054-plan-validation-boundary`
- Paper `P087` · Tools Are Under-Documented: Simple Document Expansion Boosts Tool Retrieval；用途 `prior`；路线 `q003:paper_card_fts` #2；Card `paper-p087`（paper）；Evidence `ev-p087-fields-not-universally-beneficial`, `ev-p087-merge-and-semantic-judge`, `ev-p087-structured-query-independent-expansion`
- Paper `P091` · Temporal Validity in Retrieval Memory: Eliminating Stale-Fact Errors for AI Agents over Evolving Knowledge；用途 `prior`；路线 `q003:operator_card_fts` #3；Card `operator-deterministic-sro-supersession-ledger`（operator）；Evidence `ev-p091-retain-fabrication`, `ev-p091-supersession-rule`
- Paper `P004` · TravelPlanner: A Benchmark for Real-World Planning with Language Agents；用途 `prior`；路线 `q003:failure_card_fts` #2；Card `failure-constrained-plan-surface-validity`（failure）；Evidence `ev-p004-failure-core`, `ev-p004-macro-constraint-failure`
- Paper `P031` · Agent Memory: Characterization and System Implications of Stateful Long-Horizon Workloads；用途 `prior`；路线 `q003:passage_hybrid` #21；Passage `P031:p0003:s0002`
- Paper `P052` · Planning Anything with Rigor: General-Purpose Zero-Shot Planning with LLM-based Formalized Programming；用途 `measurement`；路线 `q004:paper_card_fts` #4；Card `paper-p052`（paper）；Evidence `ev-p052-decomposed-formalization`, `ev-p052-fixed-cross-task-examples`, `ev-p052-implicit-constraint-failure`, `ev-p052-result-self-assessment`, `ev-p052-self-diagnosis-nontermination`
- Paper `P095` · Don't Ask the LLM to Track Freshness: A Deterministic Recipe for Memory Conflict Resolution；用途 `measurement`；路线 `q004:passage_hybrid` #4；Passage `P095:p0006:s0001`
- Paper `P060` · Unifying Inference-Time Planning Language Generation；用途 `measurement`；路线 `q004:failure_card_fts` #2；Card `failure-natural-language-ir-hurts-formal-planning`（failure）；Evidence `ev-p060-formal-ir-solver`, `ev-p060-ir-result-and-nl-failure`
- Paper `P092` · MemConflict: Evaluating Long-Term Memory Systems Under Memory Conflicts；用途 `measurement`；路线 `q004:operator_card_fts` #3；Card `operator-support-evidence-whitebox-retrieval-metrics`（operator）；Evidence `ev-p092-crs-low`, `ev-p092-whitebox-metrics`

- 代表项：16 / 去重 Paper：78

## 查询与路线覆盖

### q001 · problem

- 原始查询：`agentic plan caching safety semantically similar tasks different action dependency graph cache mis-hit`
- 规范化查询：`"agentic" OR "plan" OR "caching" OR "safety" OR "semantically" OR "similar" OR "tasks" OR "different" OR "action" OR "dependency" OR "graph" OR "cache" OR "mis" OR "hit"`
- 路线 `paper_card_fts`：20 条；降级 false（无）
- 路线 `failure_card_fts`：20 条；降级 false（无）
- 路线 `passage_hybrid`：24 条；降级 false（无）
- 路线 `operator_card_fts`：20 条；降级 false（无）

### q002 · failure

- 原始查询：`plan template adaptation preserves obsolete branch order action constraint`
- 规范化查询：`"plan" OR "template" OR "adaptation" OR "preserves" OR "obsolete" OR "branch" OR "order" OR "action" OR "constraint"`
- 路线 `failure_card_fts`：20 条；降级 false（无）
- 路线 `passage_hybrid`：24 条；降级 false（无）
- 路线 `operator_card_fts`：20 条；降级 false（无）
- 路线 `paper_card_fts`：20 条；降级 false（无）

### q003 · prior

- 原始查询：`Agentic Plan Caching AgenticCache temporal semantic caching structured intent canonicalization`
- 规范化查询：`"Agentic" OR "Plan" OR "Caching" OR "AgenticCache" OR "temporal" OR "semantic" OR "structured" OR "intent" OR "canonicalization"`
- 路线 `paper_card_fts`：20 条；降级 false（无）
- 路线 `operator_card_fts`：15 条；降级 false（无）
- 路线 `failure_card_fts`：15 条；降级 false（无）
- 路线 `passage_hybrid`：24 条；降级 false（无）

### q004 · measurement

- 原始查询：`counterfactual task pairs cache hit adaptation recovery planning failure decomposition`
- 规范化查询：`"counterfactual" OR "task" OR "pairs" OR "cache" OR "hit" OR "adaptation" OR "recovery" OR "planning" OR "failure" OR "decomposition"`
- 路线 `paper_card_fts`：20 条；降级 false（无）
- 路线 `passage_hybrid`：24 条；降级 false（无）
- 路线 `failure_card_fts`：20 条；降级 false（无）
- 路线 `operator_card_fts`：20 条；降级 false（无）

## 覆盖诊断

- 去重 Card：134
- 去重 Evidence：172
- 去重 Passage：68
- 命中 Paper：78
- 原始观测：326
- 带机械噪声标记的观测：1
