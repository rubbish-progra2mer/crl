<!-- CRL_RESEARCH_SEARCH_META {"created_at_utc":"2026-08-13T09:15:05.004260Z","request_fingerprint_sha256":"918e3af0e2ff5794f38e6699ce3016edc2995077f1d11409934fa70dd5950b3b","result_json_sha256":"d3c28b336089a804c312df04a0d4591c0e40c92804c1aa46f2b5cc9932c56879","search_id":"v002-transition-collision"} -->
# 研究检索导航

> 本报告仅展示查询路线、来源、命中定位与覆盖；所有科研判断由主研究者完成。

- 搜索标识：`v002-transition-collision`
- 生成时间（协调世界时）：`2026-08-13T09:15:05.004260Z`

## 紧凑研究地图

> 跨路线按 Paper 去重；每个查询路线至多选一个尚未出现的最高排名代表项。完整原始命中保留在 `result.json`。

- Paper `P062` · Agentic Memory: Learning Unified Long-Term and Short-Term Memory Management for Large Language Model Agents；用途 `prior`；路线 `q001:paper_card_fts` #1；Card `paper-p062`（paper）；Evidence `ev-p062-broadcast-advantage`, `ev-p062-unified-memory-action-policy`
- Paper `P046` · Solver-Aided Verification of Policy Compliance in Tool-Augmented LLM Agents；用途 `prior`；路线 `q001:operator_card_fts` #1；Card `operator-smt-preexecution-policy-guard`（operator）；Evidence `ev-p046-operator-core`
- Paper `P040` · From Confident Closing to Silent Failure: Characterizing False Success in LLM Agents；用途 `prior`；路线 `q001:failure_card_fts` #1；Card `failure-confident-completion-without-state-success`（failure）；Evidence `ev-p040-failure-core`
- Paper `P007` · tau-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains；用途 `prior`；路线 `q001:passage_hybrid` #2；Passage `P007:p0002:s0001`
- Paper `P028` · Memory-R1: Enhancing Large Language Model Agents to Manage and Utilize Memories via Reinforcement Learning；用途 `operator`；路线 `q002:operator_card_fts` #1；Card `operator-learned-memory-crud-control`（operator）；Evidence `ev-p028-operator-core`
- Paper `P070` · ProMCP: Profiling Token Flows and Latency Costs in Model Context Protocol-Based LLM Agents；用途 `operator`；路线 `q002:paper_card_fts` #1；Card `paper-p070`（paper）；Evidence `ev-p070-light-tool-runtime-boundary`, `ev-p070-orchestration-bottleneck`, `ev-p070-six-stage-attribution`
- Paper `P072` · Structured Uncertainty guided Clarification for LLM Agents；用途 `operator`；路线 `q002:passage_hybrid` #3；Passage `P072:p0017:s0001`
- Paper `P074` · ToolGate: Contract-Grounded and Verified Tool Execution for LLMs；用途 `operator`；路线 `q002:failure_card_fts` #1；Card `failure-incomplete-tool-contracts-false-verified-state`（failure）；Evidence `ev-p074-contract-state-commit`, `ev-p074-missing-schema-true-postcondition`
- Paper `P026` · Agent Lightning: Train ANY AI Agents with Reinforcement Learning；用途 `prior`；路线 `q003:paper_card_fts` #1；Card `paper-p026`（paper）；Evidence `ev-p026-transition-decomposition`, `ev-p026-uniform-terminal-return`
- Paper `P014` · Instruct-of-Reflection: Enhancing Large Language Models Iterative Reflection Capabilities via Dynamic-Meta Instruction；用途 `prior`；路线 `q003:operator_card_fts` #1；Card `operator-dynamic-reflection-gate`（operator）；Evidence `ev-p014-dynamic-reflection-gate`
- Paper `P033` · Self-Refine: Iterative Refinement with Self-Feedback；用途 `prior`；路线 `q003:failure_card_fts` #2；Card `failure-iterative-refinement-corrupts-correct-output`（failure）；Evidence `ev-p033-operator-core`
- Paper `P092` · MemConflict: Evaluating Long-Term Memory Systems Under Memory Conflicts；用途 `prior`；路线 `q003:passage_hybrid` #1；Passage `P092:p0011:s0001`

- 代表项：12 / 去重 Paper：62

## 查询与路线覆盖

### q001 · prior

- 原始查询：`black-box REST API automatic pre post state differential read-after-write effect oracle OpenAPI CRUD`
- 规范化查询：`"black" OR "box" OR "REST" OR "API" OR "automatic" OR "pre" OR "post" OR "state" OR "differential" OR "read" OR "after" OR "write" OR "effect" OR "oracle" OR "OpenAPI" OR "CRUD"`
- 路线 `paper_card_fts`：15 条；降级 false（无）
- 路线 `operator_card_fts`：15 条；降级 false（无）
- 路线 `failure_card_fts`：15 条；降级 false（无）
- 路线 `passage_hybrid`：15 条；降级 false（无）

### q002 · operator

- 原始查询：`request response handle create delete update membership move cursor visibility pagination UNKNOWN runtime verification`
- 规范化查询：`"request" OR "response" OR "handle" OR "create" OR "delete" OR "update" OR "membership" OR "move" OR "cursor" OR "visibility" OR "pagination" OR "UNKNOWN" OR "runtime" OR "verification"`
- 路线 `operator_card_fts`：15 条；降级 false（无）
- 路线 `paper_card_fts`：15 条；降级 false（无）
- 路线 `passage_hybrid`：15 条；降级 false（无）
- 路线 `failure_card_fts`：11 条；降级 false（无）

### q003 · prior

- 原始查询：`metamorphic REST testing dynamic invariant mining state transition verification RESTler EvoMaster MASTOR SATORI AGORA RESTOR`
- 规范化查询：`"metamorphic" OR "REST" OR "testing" OR "dynamic" OR "invariant" OR "mining" OR "state" OR "transition" OR "verification" OR "RESTler" OR "EvoMaster" OR "MASTOR" OR "SATORI" OR "AGORA" OR "RESTOR"`
- 路线 `paper_card_fts`：15 条；降级 false（无）
- 路线 `operator_card_fts`：15 条；降级 false（无）
- 路线 `failure_card_fts`：15 条；降级 false（无）
- 路线 `passage_hybrid`：15 条；降级 false（无）

## 覆盖诊断

- 去重 Card：89
- 去重 Evidence：108
- 去重 Passage：45
- 命中 Paper：62
- 原始观测：176
- 带机械噪声标记的观测：2
