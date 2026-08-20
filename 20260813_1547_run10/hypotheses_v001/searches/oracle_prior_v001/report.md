<!-- CRL_RESEARCH_SEARCH_META {"created_at_utc":"2026-08-13T08:35:22.433810Z","request_fingerprint_sha256":"b06bfe646750845bc111f3af76c6bf5c25a119c2f035a3c5ba5a93ac2a1d447a","result_json_sha256":"b26cce7b56a51292feff27a00b8c86a80236a4d647ec7c7761eb7270ac0a2456","search_id":"oracle_prior_v001"} -->
# 研究检索导航

> 本报告仅展示查询路线、来源、命中定位与覆盖；所有科研判断由主研究者完成。

- 搜索标识：`oracle_prior_v001`
- 生成时间（协调世界时）：`2026-08-13T08:35:22.433810Z`

## 紧凑研究地图

> 跨路线按 Paper 去重；每个查询路线至多选一个尚未出现的最高排名代表项。完整原始命中保留在 `result.json`。

- Paper `P057` · Automated Design of Agentic Systems；用途 `prior`；路线 `q001:paper_card_fts` #1；Card `paper-p057`（paper）；Evidence `ev-p057-archive-code-search`, `ev-p057-search-evaluation-budget`
- Paper `P101` · Semantic Evaluation for Text-to-SQL with Distilled Test Suites；用途 `prior`；路线 `q001:operator_card_fts` #1；Card `operator-neighbor-distilled-test-suites`（operator）；Evidence `ev-p101-esm-fn-rate`, `ev-p101-neighbor-distillation`
- Paper `P051` · Large Language Models Can Solve Real-World Planning Rigorously with Formal Verification Tools；用途 `prior`；路线 `q001:failure_card_fts` #1；Card `failure-solver-guarantee-stops-at-formalization`（failure）；Evidence `ev-p051-omitted-constraint-failure`, `ev-p051-solver-guarantee-boundary`
- Paper `P005` · ToolLLM: Facilitating Large Language Models to Master 16000+ Real-world APIs；用途 `prior`；路线 `q001:passage_hybrid` #1；Passage `P005:p0002:s0001`
- Paper `P096` · VeriSimpl: Robust Optimization Modeling from Natural Language using Simplification-based Verification；用途 `operator`；路线 `q002:operator_card_fts` #1；Card `operator-solver-simplification-query-verification`（operator）；Evidence `ev-p096-shared-misinterpretation`, `ev-p096-simplification-inversion`
- Paper `P048` · NaviAgent: Graph-Driven Bilevel Planning for Scalable Tool Orchestration；用途 `operator`；路线 `q002:paper_card_fts` #1；Card `paper-p048`（paper）；Evidence `ev-p048-operator-core`
- Paper `P099` · Verus-SpecGym: An Agentic Environment for Evaluating Specification Autoformalization；用途 `operator`；路线 `q002:passage_hybrid` #2；Passage `P099:p0002:s0001`
- Paper `P091` · Temporal Validity in Retrieval Memory: Eliminating Stale-Fact Errors for AI Agents over Evolving Knowledge；用途 `operator`；路线 `q002:failure_card_fts` #1；Card `failure-cosine-cannot-separate-contradiction-from-duplicate`（failure）；Evidence `ev-p091-cosine-auroc`, `ev-p091-retain-fabrication`
- Paper `P074` · ToolGate: Contract-Grounded and Verified Tool Execution for LLMs；用途 `failure`；路线 `q003:failure_card_fts` #1；Card `failure-incomplete-tool-contracts-false-verified-state`（failure）；Evidence `ev-p074-contract-state-commit`, `ev-p074-missing-schema-true-postcondition`
- Paper `P040` · From Confident Closing to Silent Failure: Characterizing False Success in LLM Agents；用途 `failure`；路线 `q003:passage_hybrid` #1；Passage `P040:p0003:s0001`
- Paper `P007` · tau-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains；用途 `failure`；路线 `q003:operator_card_fts` #2；Card `operator-terminal-state-reliability-evaluation`（operator）；Evidence `ev-p007-terminal-state-evaluation`
- Paper `P013` · Large Language Models Cannot Self-Correct Reasoning Yet；用途 `failure`；路线 `q003:paper_card_fts` #2；Card `paper-p013`（paper）；Evidence `ev-p013-intrinsic-self-correction-degrades`, `ev-p013-oracle-free-equal-budget-boundary`

- 代表项：12 / 去重 Paper：53

## 查询与路线覆盖

### q001 · prior

- 原始查询：`automatic semantic test oracle generation REST API multi-operation state propagation OpenAPI source code MASTOR SATORI AGORA RESTler`
- 规范化查询：`"automatic" OR "semantic" OR "test" OR "oracle" OR "generation" OR "REST" OR "API" OR "multi" OR "operation" OR "state" OR "propagation" OR "OpenAPI" OR "source" OR "code" OR "MASTOR" OR "SATORI" OR "AGORA" OR "RESTler"`
- 路线 `paper_card_fts`：10 条；降级 false（无）
- 路线 `operator_card_fts`：10 条；降级 false（无）
- 路线 `failure_card_fts`：10 条；降级 false（无）
- 路线 `passage_hybrid`：10 条；降级 false（无）

### q002 · operator

- 原始查询：`compile runtime verification witness from mutation arguments downstream task dependencies and read-only API without source code`
- 规范化查询：`"compile" OR "runtime" OR "verification" OR "witness" OR "from" OR "mutation" OR "arguments" OR "downstream" OR "task" OR "dependencies" OR "and" OR "read" OR "only" OR "API" OR "without" OR "source" OR "code"`
- 路线 `operator_card_fts`：10 条；降级 false（无）
- 路线 `paper_card_fts`：10 条；降级 false（无）
- 路线 `passage_hybrid`：10 条；降级 false（无）
- 路线 `failure_card_fts`：10 条；降级 false（无）

### q003 · failure

- 原始查询：`schema-valid success response but missing external side effect false success`
- 规范化查询：`"schema" OR "valid" OR "success" OR "response" OR "but" OR "missing" OR "external" OR "side" OR "effect" OR "false"`
- 路线 `failure_card_fts`：10 条；降级 false（无）
- 路线 `passage_hybrid`：10 条；降级 false（无）
- 路线 `operator_card_fts`：10 条；降级 false（无）
- 路线 `paper_card_fts`：10 条；降级 false（无）

## 覆盖诊断

- 去重 Card：73
- 去重 Evidence：105
- 去重 Passage：29
- 命中 Paper：53
- 原始观测：120
- 带机械噪声标记的观测：0
