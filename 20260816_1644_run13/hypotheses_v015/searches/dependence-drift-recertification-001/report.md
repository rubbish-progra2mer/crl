<!-- CRL_RESEARCH_SEARCH_META {"created_at_utc":"2026-08-16T10:34:17.712149Z","request_fingerprint_sha256":"e920fb38d7a065f643674f108bba7703cbd8b65aed7e24d4d651c62e28d8581d","result_json_sha256":"26099c8f85a20c42f3f594547436c8442a318e0ae440573ebcc17b53b4bc11a4","search_id":"dependence-drift-recertification-001"} -->
# 研究检索导航

> 本报告仅展示查询路线、来源、命中定位与覆盖；所有科研判断由主研究者完成。

- 搜索标识：`dependence-drift-recertification-001`
- 生成时间（协调世界时）：`2026-08-16T10:34:17.712149Z`

## 紧凑研究地图

> 跨路线按 Paper 去重；每个查询路线至多选一个尚未出现的最高排名代表项。完整原始命中保留在 `result.json`。

- Paper `P095` · Don't Ask the LLM to Track Freshness: A Deterministic Recipe for Memory Conflict Resolution；用途 `problem`；路线 `q001:paper_card_fts` #1；Card `paper-p095`（paper）；Evidence `ev-p095-matched-comparison`, `ev-p095-prior-override-drift`
- Paper `P030` · STALE: Can LLM Agents Know When Their Memories Are No Longer Valid?；用途 `problem`；路线 `q001:failure_card_fts` #2；Card `failure-retrieved-update-lacks-decision-authority`（failure）；Evidence `ev-p030-failure-core`, `ev-p030-recognition-application-gap`
- Paper `P076` · Multi-Agent Systems Execute Arbitrary Malicious Code；用途 `problem`；路线 `q001:passage_hybrid` #1；Passage `P076:p0001:s0002`
- Paper `P086` · Meta-Tool: Unleash Open-World Function Calling Capabilities of General-Purpose Large Language Models；用途 `problem`；路线 `q001:operator_card_fts` #3；Card `operator-required-parameter-description-tool-retrieval`（operator）；Evidence `ev-p086-hypothesize-retrieve-invoke`, `ev-p086-near-identical-distribution`, `ev-p086-required-parameter-score`
- Paper `P071` · Agentic Plan Caching: Test-Time Memory for Fast and Cost-Efficient LLM Agents；用途 `failure`；路线 `q002:failure_card_fts` #2；Card `failure-plan-cache-semantic-false-positives`（failure）；Evidence `ev-p071-cache-false-positive-boundary`, `ev-p071-plan-template-reuse`
- Paper `P016` · Why Do Multi-Agent LLM Systems Fail?；用途 `failure`；路线 `q002:passage_hybrid` #1；Passage `P016:p0029:s0001`
- Paper `P088` · Non-negative Elastic Net Decoding for Information Retrieval；用途 `failure`；路线 `q002:operator_card_fts` #1；Card `operator-joint-nonnegative-residual-retrieval`（operator）；Evidence `ev-p088-joint-nonnegative-objective`, `ev-p088-relevant-set-size-signature`, `ev-p088-theory-deployment-scale-boundary`
- Paper `P035` · Holistic Agent Leaderboard: The Missing Infrastructure for AI Agent Evaluation；用途 `failure`；路线 `q002:paper_card_fts` #3；Card `paper-p035`（paper）；Evidence `ev-p035-evaluation-core`
- Paper `P021` · In-the-Flow Agentic System Optimization for Effective Planning and Tool Use；用途 `operator`；路线 `q003:operator_card_fts` #1；Card `operator-outcome-trained-execution-state-planner`（operator）；Evidence `ev-p021-operator-core`
- Paper `P040` · From Confident Closing to Silent Failure: Characterizing False Success in LLM Agents；用途 `operator`；路线 `q003:paper_card_fts` #1；Card `paper-p040`（paper）；Evidence `ev-p040-failure-core`
- Paper `P073` · Uncertainty Calibration for Tool-Using Language Agents；用途 `operator`；路线 `q003:passage_hybrid` #1；Passage `P073:p0005:s0001`
- Paper `P064` · How Memory Management Impacts LLM Agents: An Empirical Study of Experience-Following Behavior；用途 `operator`；路线 `q003:failure_card_fts` #2；Card `failure-retrieved-experience-propagates-stored-errors`（failure）；Evidence `ev-p064-evaluator-reliability`, `ev-p064-experience-following-error`
- Paper `P037` · ToolSandbox: A Stateful, Conversational, Interactive Evaluation Benchmark for LLM Tool Use Capabilities；用途 `prior`；路线 `q004:paper_card_fts` #1；Card `paper-p037`（paper）；Evidence `ev-p037-evaluation-core`
- Paper `P097` · ReLoop: Structured Modeling and Behavioral Verification for Reliable LLM-Based Optimization；用途 `prior`；路线 `q004:operator_card_fts` #1；Card `operator-behavioral-perturbation-existence-test`（operator）；Evidence `ev-p097-behavioral-perturbation`, `ev-p097-feasibility-gap`
- Paper `P004` · TravelPlanner: A Benchmark for Real-World Planning with Language Agents；用途 `prior`；路线 `q004:failure_card_fts` #1；Card `failure-constrained-plan-surface-validity`（failure）；Evidence `ev-p004-failure-core`, `ev-p004-macro-constraint-failure`
- Paper `P098` · Beyond Objective Equivalence: Constraint Injection for LLM-Based Optimization Modeling on Vehicle Routing Problems；用途 `prior`；路线 `q004:passage_hybrid` #1；Passage `P098:p0019:s0001`
- Paper `P029` · MemFail: Stress-Testing Failure Modes of LLM Memory Systems；用途 `measurement`；路线 `q005:paper_card_fts` #2；Card `paper-p029`（paper）；Evidence `ev-p029-failure-core`
- Paper `P090` · From Single to Multi-Granularity: Toward Long-Term Memory Association and Selection of Conversational Agents；用途 `measurement`；路线 `q005:passage_hybrid` #4；Passage `P090:p0025:s0001`
- Paper `P091` · Temporal Validity in Retrieval Memory: Eliminating Stale-Fact Errors for AI Agents over Evolving Knowledge；用途 `measurement`；路线 `q005:failure_card_fts` #2；Card `failure-cosine-cannot-separate-contradiction-from-duplicate`（failure）；Evidence `ev-p091-cosine-auroc`, `ev-p091-retain-fabrication`
- Paper `P072` · Structured Uncertainty guided Clarification for LLM Agents；用途 `measurement`；路线 `q005:operator_card_fts` #3；Card `operator-cost-penalized-structured-clarification`（operator）；Evidence `ev-p072-compute-boundary`, `ev-p072-structured-clarification-gate`, `ev-p072-unstructured-clarification-failure`

- 代表项：20 / 去重 Paper：84

## 查询与路线覆盖

### q001 · problem

- 原始查询：`deployed multi-agent reliability certificate drift stale recertification model version mission distribution`
- 规范化查询：`"deployed" OR "multi" OR "agent" OR "reliability" OR "certificate" OR "drift" OR "stale" OR "recertification" OR "model" OR "version" OR "mission" OR "distribution"`
- 路线 `paper_card_fts`：24 条；降级 false（无）
- 路线 `failure_card_fts`：24 条；降级 false（无）
- 路线 `passage_hybrid`：24 条；降级 false（无）
- 路线 `operator_card_fts`：24 条；降级 false（无）

### q002 · failure

- 原始查询：`component marginals stable dependence correlation drift joint failure certificate invalidation`
- 规范化查询：`"component" OR "marginals" OR "stable" OR "dependence" OR "correlation" OR "drift" OR "joint" OR "failure" OR "certificate" OR "invalidation"`
- 路线 `failure_card_fts`：24 条；降级 false（无）
- 路线 `passage_hybrid`：24 条；降级 false（无）
- 路线 `operator_card_fts`：13 条；降级 false（无）
- 路线 `paper_card_fts`：24 条；降级 false（无）

### q003 · operator

- 原始查询：`sequential monitoring confidence sequence distribution shift change detection moment ambiguity set robust reliability`
- 规范化查询：`"sequential" OR "monitoring" OR "confidence" OR "sequence" OR "distribution" OR "shift" OR "change" OR "detection" OR "moment" OR "ambiguity" OR "set" OR "robust" OR "reliability"`
- 路线 `operator_card_fts`：16 条；降级 false（无）
- 路线 `paper_card_fts`：19 条；降级 false（无）
- 路线 `passage_hybrid`：24 条；降级 false（无）
- 路线 `failure_card_fts`：17 条；降级 false（无）

### q004 · prior

- 原始查询：`anytime-valid reliability certificate decay recertification e-process dual sensitivity active constraints`
- 规范化查询：`"anytime" OR "valid" OR "reliability" OR "certificate" OR "decay" OR "recertification" OR "e" OR "process" OR "dual" OR "sensitivity" OR "active" OR "constraints"`
- 路线 `paper_card_fts`：19 条；降级 false（无）
- 路线 `operator_card_fts`：8 条；降级 false（无）
- 路线 `failure_card_fts`：6 条；降级 false（无）
- 路线 `passage_hybrid`：24 条；降级 false（无）

### q005 · measurement

- 原始查询：`co-failure moment drift lower bound certificate threshold monitoring`
- 规范化查询：`"co" OR "failure" OR "moment" OR "drift" OR "lower" OR "bound" OR "certificate" OR "threshold" OR "monitoring"`
- 路线 `paper_card_fts`：24 条；降级 false（无）
- 路线 `passage_hybrid`：24 条；降级 false（无）
- 路线 `failure_card_fts`：24 条；降级 false（无）
- 路线 `operator_card_fts`：12 条；降级 false（无）

## 覆盖诊断

- 去重 Card：143
- 去重 Evidence：179
- 去重 Passage：97
- 命中 Paper：84
- 原始观测：398
- 带机械噪声标记的观测：5
