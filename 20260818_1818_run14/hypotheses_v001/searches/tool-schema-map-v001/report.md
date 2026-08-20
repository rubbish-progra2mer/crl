<!-- CRL_RESEARCH_SEARCH_META {"created_at_utc":"2026-08-18T10:18:49.887708Z","request_fingerprint_sha256":"bd56cec9a0b4d92522bfcc97d008e99ae5f23b04d6070b6f990989508df719ec","result_json_sha256":"383303f8c4b9be1e64ca154ef3e36655889c151ca9977a3e9afb076d0996f005","search_id":"tool-schema-map-v001"} -->
# 研究检索导航

> 本报告仅展示查询路线、来源、命中定位与覆盖；所有科研判断由主研究者完成。

- 搜索标识：`tool-schema-map-v001`
- 生成时间（协调世界时）：`2026-08-18T10:18:49.887708Z`

## 紧凑研究地图

> 跨路线按 Paper 去重；每个查询路线至多选一个尚未出现的最高排名代表项。完整原始命中保留在 `result.json`。

- Paper `P084` · On the Robustness of Agentic Function Calling；用途 `problem`；路线 `q001:paper_card_fts` #1；Card `paper-p084`（paper）；Evidence `ev-p084-expanded-toolkit-controlled-setting`, `ev-p084-expanded-toolkit-table`, `ev-p084-generated-tool-single-dataset-boundary`, `ev-p084-related-toolkit-error-types`
- Paper `P074` · ToolGate: Contract-Grounded and Verified Tool Execution for LLMs；用途 `problem`；路线 `q001:failure_card_fts` #1；Card `failure-incomplete-tool-contracts-false-verified-state`（failure）；Evidence `ev-p074-contract-state-commit`, `ev-p074-missing-schema-true-postcondition`
- Paper `P038` · AgentDojo: A Dynamic Environment to Evaluate Prompt Injection Attacks and Defenses for LLM Agents；用途 `problem`；路线 `q001:passage_hybrid` #2；Passage `P038:p0026:s0001`
- Paper `P025` · Unlocking the Power of Multi-Agent LLM for Reasoning: From Lazy Agents to Deliberation；用途 `problem`；路线 `q001:operator_card_fts` #1；Card `operator-grouped-masked-history-step-credit`（operator）；Evidence `ev-p025-failure-core`, `ev-p025-grouped-step-influence`
- Paper `P080` · AutoSearch: Adaptive Search Depth for Efficient Agentic RAG via Reinforcement Learning；用途 `failure`；路线 `q002:failure_card_fts` #1；Card `failure-fixed-search-depth-causes-under-and-over-search`（failure）；Evidence `ev-p080-fixed-depth-under-over-search`, `ev-p080-gold-supervised-minimal-depth`, `ev-p080-shallow-depth-boundary`
- Paper `P037` · ToolSandbox: A Stateful, Conversational, Interactive Evaluation Benchmark for LLM Tool Use Capabilities；用途 `failure`；路线 `q002:passage_hybrid` #1；Passage `P037:p0013:s0001`
- Paper `P087` · Tools Are Under-Documented: Simple Document Expansion Boosts Tool Retrieval；用途 `failure`；路线 `q002:operator_card_fts` #1；Card `operator-grounded-structured-tool-document-expansion`（operator）；Evidence `ev-p087-fields-not-universally-beneficial`, `ev-p087-merge-and-semantic-judge`, `ev-p087-structured-query-independent-expansion`
- Paper `P095` · Don't Ask the LLM to Track Freshness: A Deterministic Recipe for Memory Conflict Resolution；用途 `failure`；路线 `q002:paper_card_fts` #2；Card `paper-p095`（paper）；Evidence `ev-p095-matched-comparison`, `ev-p095-prior-override-drift`
- Paper `P027` · Verified Critical Step Optimization for LLM Agents；用途 `operator`；路线 `q003:operator_card_fts` #1；Card `operator-verified-single-branch-repair`（operator）；Evidence `ev-p027-operator-core`
- Paper `P042` · LiveResearchBench: A Live Benchmark for User-Centric Deep Research in the Wild；用途 `operator`；路线 `q003:paper_card_fts` #2；Card `paper-p042`（paper）；Evidence `ev-p042-evaluation-core`
- Paper `P068` · DeepFact: Co-Evolving Benchmarks and Agents for Deep Research Factuality；用途 `operator`；路线 `q003:passage_hybrid` #5；Passage `P068:p0015:s0001`
- Paper `P065` · Group-in-Group Policy Optimization for LLM Agent Training；用途 `operator`；路线 `q003:failure_card_fts` #1；Card `failure-anchor-state-credit-needs-state-recurrence`（failure）；Evidence `ev-p065-anchor-state-credit`, `ev-p065-state-recurrence-boundary`
- Paper `P004` · TravelPlanner: A Benchmark for Real-World Planning with Language Agents；用途 `prior`；路线 `q004:paper_card_fts` #1；Card `paper-p004`（paper）；Evidence `ev-p004-failure-core`
- Paper `P097` · ReLoop: Structured Modeling and Behavioral Verification for Reliable LLM-Based Optimization；用途 `prior`；路线 `q004:operator_card_fts` #1；Card `operator-behavioral-perturbation-existence-test`（operator）；Evidence `ev-p097-behavioral-perturbation`, `ev-p097-feasibility-gap`
- Paper `P070` · ProMCP: Profiling Token Flows and Latency Costs in Model Context Protocol-Based LLM Agents；用途 `prior`；路线 `q004:failure_card_fts` #1；Card `failure-light-tool-runtime-bottleneck-overreach`（failure）；Evidence `ev-p070-light-tool-runtime-boundary`, `ev-p070-orchestration-bottleneck`, `ev-p070-six-stage-attribution`
- Paper `P007` · tau-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains；用途 `prior`；路线 `q004:passage_hybrid` #1；Passage `P007:p0002:s0001`
- Paper `P039` · ToolFailBench: Diagnosing Tool-Use Failures in LLM Agents；用途 `measurement`；路线 `q005:paper_card_fts` #1；Card `paper-p039`（paper）；Evidence `ev-p039-failure-core`
- Paper `P036` · tau-Knowledge: Evaluating Conversational Agents over Unstructured Knowledge；用途 `measurement`；路线 `q005:passage_hybrid` #1；Passage `P036:p0023:s0001`
- Paper `P040` · From Confident Closing to Silent Failure: Characterizing False Success in LLM Agents；用途 `measurement`；路线 `q005:failure_card_fts` #2；Card `failure-confident-completion-without-state-success`（failure）；Evidence `ev-p040-failure-core`
- Paper `P093` · Collapse of Dense Retrievers: Short, Early, and Literal Biases Outranking Factual Evidence；用途 `measurement`；路线 `q005:operator_card_fts` #2；Card `operator-paired-single-factor-bias-decomposition`（operator）；Evidence `ev-p093-foil-collapse`, `ev-p093-paired-protocol`

- 代表项：20 / 去重 Paper：55

## 查询与路线覆盖

### q001 · problem

- 原始查询：`tool-using LLM agents robustness to semantically equivalent API schema changes`
- 规范化查询：`"tool" OR "using" OR "LLM" OR "agents" OR "robustness" OR "to" OR "semantically" OR "equivalent" OR "API" OR "schema" OR "changes"`
- 路线 `paper_card_fts`：8 条；降级 false（无）
- 路线 `failure_card_fts`：8 条；降级 false（无）
- 路线 `passage_hybrid`：10 条；降级 false（无）
- 路线 `operator_card_fts`：8 条；降级 false（无）

### q002 · failure

- 原始查询：`tool schema drift argument renaming reordering serialization causes agent failure`
- 规范化查询：`"tool" OR "schema" OR "drift" OR "argument" OR "renaming" OR "reordering" OR "serialization" OR "causes" OR "agent" OR "failure"`
- 路线 `failure_card_fts`：8 条；降级 false（无）
- 路线 `passage_hybrid`：10 条；降级 false（无）
- 路线 `operator_card_fts`：8 条；降级 false（无）
- 路线 `paper_card_fts`：8 条；降级 false（无）

### q003 · operator

- 原始查询：`canonicalization invariance counterfactual tool interface evaluation`
- 规范化查询：`"canonicalization" OR "invariance" OR "counterfactual" OR "tool" OR "interface" OR "evaluation"`
- 路线 `operator_card_fts`：8 条；降级 false（无）
- 路线 `paper_card_fts`：8 条；降级 false（无）
- 路线 `passage_hybrid`：10 条；降级 false（无）
- 路线 `failure_card_fts`：8 条；降级 false（无）

### q004 · prior

- 原始查询：`benchmark tool-using agents API schema perturbation robustness`
- 规范化查询：`"benchmark" OR "tool" OR "using" OR "agents" OR "API" OR "schema" OR "perturbation" OR "robustness"`
- 路线 `paper_card_fts`：8 条；降级 false（无）
- 路线 `operator_card_fts`：8 条；降级 false（无）
- 路线 `failure_card_fts`：8 条；降级 false（无）
- 路线 `passage_hybrid`：10 条；降级 false（无）

### q005 · measurement

- 原始查询：`paired task success under equivalent tool schemas`
- 规范化查询：`"paired" OR "task" OR "success" OR "under" OR "equivalent" OR "tool" OR "schemas"`
- 路线 `paper_card_fts`：8 条；降级 false（无）
- 路线 `passage_hybrid`：10 条；降级 false（无）
- 路线 `failure_card_fts`：8 条；降级 false（无）
- 路线 `operator_card_fts`：8 条；降级 false（无）

## 覆盖诊断

- 去重 Card：79
- 去重 Evidence：105
- 去重 Passage：45
- 命中 Paper：55
- 原始观测：170
- 带机械噪声标记的观测：0
