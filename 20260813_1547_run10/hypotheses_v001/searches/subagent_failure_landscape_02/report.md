<!-- CRL_RESEARCH_SEARCH_META {"created_at_utc":"2026-08-13T07:56:26.176919Z","request_fingerprint_sha256":"5ad00fedf12e6131d9e064da22690d0e4584bc478179ee29e393a7970f95d1c5","result_json_sha256":"1d4a390c9c148e82f1e7816ac48b53c7d5cf1daedbb90362483a98a392a8c4d5","search_id":"subagent_failure_landscape_02"} -->
# 研究检索导航

> 本报告仅展示查询路线、来源、命中定位与覆盖；所有科研判断由主研究者完成。

- 搜索标识：`subagent_failure_landscape_02`
- 生成时间（协调世界时）：`2026-08-13T07:56:26.176919Z`

## 紧凑研究地图

> 跨路线按 Paper 去重；每个查询路线至多选一个尚未出现的最高排名代表项。完整原始命中保留在 `result.json`。

- Paper `P074` · ToolGate: Contract-Grounded and Verified Tool Execution for LLMs；用途 `failure`；路线 `q001:failure_card_fts` #1；Card `failure-incomplete-tool-contracts-false-verified-state`（failure）；Evidence `ev-p074-contract-state-commit`, `ev-p074-missing-schema-true-postcondition`
- Paper `P040` · From Confident Closing to Silent Failure: Characterizing False Success in LLM Agents；用途 `failure`；路线 `q001:passage_hybrid` #1；Passage `P040:p0003:s0001`
- Paper `P071` · Agentic Plan Caching: Test-Time Memory for Fast and Cost-Efficient LLM Agents；用途 `failure`；路线 `q001:operator_card_fts` #1；Card `operator-adaptive-plan-template-reuse`（operator）；Evidence `ev-p071-cache-false-positive-boundary`, `ev-p071-plan-template-reuse`
- Paper `P101` · Semantic Evaluation for Text-to-SQL with Distilled Test Suites；用途 `failure`；路线 `q001:paper_card_fts` #4；Card `paper-p101`（paper）；Evidence `ev-p101-esm-fn-rate`, `ev-p101-metric-distortion`, `ev-p101-neighbor-distillation`
- Paper `P079` · Learning to Contextualize Web Pages for Enhanced Decision Making by LLM Agents；用途 `failure`；路线 `q002:failure_card_fts` #1；Card `failure-raw-observation-overload-hides-action-relevant-ui`（failure）；Evidence `ev-p079-action-conditioned-contextualization`, `ev-p079-ground-truth-action-retry`, `ev-p079-unseen-ui-boundary`
- Paper `P030` · STALE: Can LLM Agents Know When Their Memories Are No Longer Valid?；用途 `failure`；路线 `q002:passage_hybrid` #1；Passage `P030:p0005:s0002`
- Paper `P001` · ReAct: Synergizing Reasoning and Acting in Language Models；用途 `failure`；路线 `q002:operator_card_fts` #2；Card `operator-reason-action-interleaving`（operator）；Evidence `ev-p001-react-interleaved`
- Paper `P038` · AgentDojo: A Dynamic Environment to Evaluate Prompt Injection Attacks and Defenses for LLM Agents；用途 `failure`；路线 `q002:paper_card_fts` #3；Card `paper-p038`（paper）；Evidence `ev-p038-operator-core`
- Paper `P095` · Don't Ask the LLM to Track Freshness: A Deterministic Recipe for Memory Conflict Resolution；用途 `failure`；路线 `q003:failure_card_fts` #1；Card `failure-llm-freshness-judgment-prior-override-and-drift`（failure）；Evidence `ev-p095-matched-comparison`, `ev-p095-prior-override-drift`
- Paper `P026` · Agent Lightning: Train ANY AI Agents with Reinforcement Learning；用途 `failure`；路线 `q003:passage_hybrid` #1；Passage `P026:p0007:s0001`
- Paper `P065` · Group-in-Group Policy Optimization for LLM Agent Training；用途 `failure`；路线 `q003:operator_card_fts` #1；Card `operator-anchor-state-relative-credit`（operator）；Evidence `ev-p065-anchor-state-credit`, `ev-p065-state-recurrence-boundary`
- Paper `P062` · Agentic Memory: Learning Unified Long-Term and Short-Term Memory Management for Large Language Model Agents；用途 `failure`；路线 `q003:paper_card_fts` #3；Card `paper-p062`（paper）；Evidence `ev-p062-broadcast-advantage`, `ev-p062-unified-memory-action-policy`
- Paper `P087` · Tools Are Under-Documented: Simple Document Expansion Boosts Tool Retrieval；用途 `measurement`；路线 `q004:paper_card_fts` #2；Card `paper-p087`（paper）；Evidence `ev-p087-fields-not-universally-beneficial`, `ev-p087-merge-and-semantic-judge`, `ev-p087-structured-query-independent-expansion`
- Paper `P078` · CRAFT: Customizing LLMs by Creating and Retrieving from Specialized Toolsets；用途 `measurement`；路线 `q004:passage_hybrid` #4；Passage `P078:p0002:s0001`
- Paper `P083` · TAMAS: Benchmarking Adversarial Risks in Multi-Agent LLM Systems；用途 `measurement`；路线 `q004:failure_card_fts` #1；Card `failure-multi-agent-adversarial-coordination-spans-trust-surfaces`（failure）；Evidence `ev-p083-lightweight-defense-failure`, `ev-p083-simulated-tool-boundary`, `ev-p083-three-surface-adversarial-failure`
- Paper `P098` · Beyond Objective Equivalence: Constraint Injection for LLM-Based Optimization Modeling on Vehicle Routing Problems；用途 `measurement`；路线 `q004:operator_card_fts` #1；Card `operator-labeled-probe-injection-dual-verifier`（operator）；Evidence `ev-p098-constraint-injection`, `ev-p098-diff-leak-550`, `ev-p098-nonbinding-blindness`
- Paper `P097` · ReLoop: Structured Modeling and Behavioral Verification for Reliable LLM-Based Optimization；用途 `problem`；路线 `q005:paper_card_fts` #2；Card `paper-p097`（paper）；Evidence `ev-p097-behavioral-perturbation`, `ev-p097-feasibility-gap`
- Paper `P039` · ToolFailBench: Diagnosing Tool-Use Failures in LLM Agents；用途 `problem`；路线 `q005:failure_card_fts` #5；Card `failure-tool-use-metrics-collapse-distinct-errors`（failure）；Evidence `ev-p039-aggregate-score-masking`, `ev-p039-failure-core`
- Paper `P041` · LLM Agents Already Know When to Call Tools - Even Without Reasoning；用途 `problem`；路线 `q005:passage_hybrid` #5；Passage `P041:p0004:s0002`
- Paper `P089` · ToolDreamer: Instilling LLM Reasoning Into Tool Retrievers；用途 `problem`；路线 `q005:operator_card_fts` #2；Card `operator-hypothetical-tool-query-expansion`（operator）；Evidence `ev-p089-api-latency-boundary`, `ev-p089-forced-alignment-proxy`, `ev-p089-hungarian-alignment`, `ev-p089-overview-alignment-rrf`, `ev-p089-retrieval-only-metrics`, `ev-p089-training-gold-count-hypothetical-tools`

- 代表项：20 / 去重 Paper：76

## 查询与路线覆盖

### q001 · failure

- 原始查询：`semantic false commit`
- 规范化查询：`"semantic" OR "false" OR "commit"`
- 路线 `failure_card_fts`：10 条；降级 false（无）
- 路线 `passage_hybrid`：20 条；降级 false（无）
- 路线 `operator_card_fts`：9 条；降级 false（无）
- 路线 `paper_card_fts`：11 条；降级 false（无）

### q002 · failure

- 原始查询：`observation corruption`
- 规范化查询：`"observation" OR "corruption"`
- 路线 `failure_card_fts`：2 条；降级 false（无）
- 路线 `passage_hybrid`：20 条；降级 false（无）
- 路线 `operator_card_fts`：3 条；降级 false（无）
- 路线 `paper_card_fts`：4 条；降级 false（无）

### q003 · failure

- 原始查询：`state drift downstream action`
- 规范化查询：`"state" OR "drift" OR "downstream" OR "action"`
- 路线 `failure_card_fts`：20 条；降级 false（无）
- 路线 `passage_hybrid`：20 条；降级 false（无）
- 路线 `operator_card_fts`：20 条；降级 false（无）
- 路线 `paper_card_fts`：20 条；降级 false（无）

### q004 · measurement

- 原始查询：`tool fault injection semantic output`
- 规范化查询：`"tool" OR "fault" OR "injection" OR "semantic" OR "output"`
- 路线 `paper_card_fts`：20 条；降级 false（无）
- 路线 `passage_hybrid`：20 条；降级 false（无）
- 路线 `failure_card_fts`：20 条；降级 false（无）
- 路线 `operator_card_fts`：20 条；降级 false（无）

### q005 · problem

- 原始查询：`silent tool failure`
- 规范化查询：`"silent" OR "tool" OR "failure"`
- 路线 `paper_card_fts`：20 条；降级 false（无）
- 路线 `failure_card_fts`：20 条；降级 false（无）
- 路线 `passage_hybrid`：20 条；降级 false（无）
- 路线 `operator_card_fts`：20 条；降级 false（无）

## 覆盖诊断

- 去重 Card：130
- 去重 Evidence：157
- 去重 Passage：93
- 命中 Paper：76
- 原始观测：319
- 带机械噪声标记的观测：9
