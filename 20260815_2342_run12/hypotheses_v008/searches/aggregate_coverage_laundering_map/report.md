<!-- CRL_RESEARCH_SEARCH_META {"created_at_utc":"2026-08-16T07:13:41.032551Z","request_fingerprint_sha256":"c8120546b9974e9b00f8d5bc6894c0be01b59ef23adcf951e227053f6f562fd1","result_json_sha256":"30d02ca65f8e8d46b31400cb55d662a0d645e285b9b4fe2521e104a8cdda6624","search_id":"aggregate_coverage_laundering_map"} -->
# 研究检索导航

> 本报告仅展示查询路线、来源、命中定位与覆盖；所有科研判断由主研究者完成。

- 搜索标识：`aggregate_coverage_laundering_map`
- 生成时间（协调世界时）：`2026-08-16T07:13:41.032551Z`

## 紧凑研究地图

> 跨路线按 Paper 去重；每个查询路线至多选一个尚未出现的最高排名代表项。完整原始命中保留在 `result.json`。

- Paper `P005` · ToolLLM: Facilitating Large Language Models to Master 16000+ Real-world APIs；用途 `problem`；路线 `q001:paper_card_fts` #1；Card `paper-p005`（paper）；Evidence `ev-p005-operator-core`
- Paper `P007` · tau-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains；用途 `problem`；路线 `q001:failure_card_fts` #1；Card `failure-repeat-run-reliability-collapse`（failure）；Evidence `ev-p007-repeat-reliability-collapse`
- Paper `P097` · ReLoop: Structured Modeling and Behavioral Verification for Reliable LLM-Based Optimization；用途 `problem`；路线 `q001:passage_hybrid` #1；Passage `P097:p0023:s0001`
- Paper `P070` · ProMCP: Profiling Token Flows and Latency Costs in Model Context Protocol-Based LLM Agents；用途 `problem`；路线 `q001:operator_card_fts` #1；Card `operator-stagewise-mcp-cost-attribution`（operator）；Evidence `ev-p070-light-tool-runtime-boundary`, `ev-p070-orchestration-bottleneck`, `ev-p070-six-stage-attribution`
- Paper `P090` · From Single to Multi-Granularity: Toward Long-Term Memory Association and Selection of Conversational Agents；用途 `failure`；路线 `q002:failure_card_fts` #1；Card `failure-fixed-single-granularity-memory`（failure）；Evidence `ev-p090-entropy-router`, `ev-p090-fixed-granularity-selection`
- Paper `P040` · From Confident Closing to Silent Failure: Characterizing False Success in LLM Agents；用途 `failure`；路线 `q002:passage_hybrid` #1；Passage `P040:p0008:s0001`
- Paper `P010` · LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory；用途 `failure`；路线 `q002:operator_card_fts` #2；Card `operator-memory-stage-decomposition`（operator）；Evidence `ev-p010-index-retrieve-read`
- Paper `P074` · ToolGate: Contract-Grounded and Verified Tool Execution for LLMs；用途 `failure`；路线 `q002:paper_card_fts` #2；Card `paper-p074`（paper）；Evidence `ev-p074-contract-state-commit`, `ev-p074-missing-schema-true-postcondition`
- Paper `P046` · Solver-Aided Verification of Policy Compliance in Tool-Augmented LLM Agents；用途 `operator`；路线 `q003:operator_card_fts` #3；Card `operator-smt-preexecution-policy-guard`（operator）；Evidence `ev-p046-operator-core`
- Paper `P063` · A-Mem: Agentic Memory for LLM Agents；用途 `operator`；路线 `q003:paper_card_fts` #4；Card `paper-p063`（paper）；Evidence `ev-p063-dynamic-link-generation`, `ev-p063-neighbor-rewrite-action`, `ev-p063-retrieval-k-varies`
- Paper `P087` · Tools Are Under-Documented: Simple Document Expansion Boosts Tool Retrieval；用途 `operator`；路线 `q003:passage_hybrid` #1；Passage `P087:p0014:s0001`
- Paper `P064` · How Memory Management Impacts LLM Agents: An Empirical Study of Experience-Following Behavior；用途 `operator`；路线 `q003:failure_card_fts` #2；Card `failure-retrieved-experience-propagates-stored-errors`（failure）；Evidence `ev-p064-evaluator-reliability`, `ev-p064-experience-following-error`
- Paper `P048` · NaviAgent: Graph-Driven Bilevel Planning for Scalable Tool Orchestration；用途 `prior`；路线 `q004:paper_card_fts` #4；Card `paper-p048`（paper）；Evidence `ev-p048-operator-core`
- Paper `P099` · Verus-SpecGym: An Agentic Environment for Evaluating Specification Autoformalization；用途 `prior`；路线 `q004:operator_card_fts` #3；Card `operator-four-bucket-executable-spec-testing`（operator）；Evidence `ev-p099-judge-miss`, `ev-p099-soundness-necessity`, `ev-p099-two-stage-check`
- Paper `P011` · On Memory Construction and Retrieval for Personalized Conversational Agents；用途 `prior`；路线 `q004:failure_card_fts` #2；Card `failure-memory-unit-granularity-mismatch`（failure）；Evidence `ev-p011-failure-core`
- Paper `P034` · RefineBench: Evaluating Refinement Capability of Language Models via Checklists；用途 `prior`；路线 `q004:passage_hybrid` #14；Passage `P034:p0043:s0001`
- Paper `P076` · Multi-Agent Systems Execute Arbitrary Malicious Code；用途 `measurement`；路线 `q005:paper_card_fts` #1；Card `paper-p076`（paper）；Evidence `ev-p076-controlled-lab-boundary`, `ev-p076-metadata-control-flow-laundering`, `ev-p076-refusal-not-system-safety`
- Paper `P044` · DEER: A Benchmark for Evaluating Deep Research Agents on Expert Report Generation；用途 `measurement`；路线 `q005:passage_hybrid` #3；Passage `P044:p0037:s0001`
- Paper `P100` · How Many Tools Should an LLM Agent See? A Chance-Corrected Answer；用途 `measurement`；路线 `q005:failure_card_fts` #2；Card `failure-fixed-shortlist-depth-masks-hard-query-zero`（failure）；Evidence `ev-p100-fixed-depth-buckets`, `ev-p100-weak-scorer-collapse`
- Paper `P093` · Collapse of Dense Retrievers: Short, Early, and Literal Biases Outranking Factual Evidence；用途 `measurement`；路线 `q005:operator_card_fts` #1；Card `operator-paired-single-factor-bias-decomposition`（operator）；Evidence `ev-p093-foil-collapse`, `ev-p093-paired-protocol`

- 代表项：20 / 去重 Paper：69

## 查询与路线覆盖

### q001 · problem

- 原始查询：`positive aggregate readiness status hides missing evidence obligation and causes unsafe irreversible action`
- 规范化查询：`"positive" OR "aggregate" OR "readiness" OR "status" OR "hides" OR "missing" OR "evidence" OR "obligation" OR "and" OR "causes" OR "unsafe" OR "irreversible" OR "action"`
- 路线 `paper_card_fts`：12 条；降级 false（无）
- 路线 `failure_card_fts`：12 条；降级 false（无）
- 路线 `passage_hybrid`：24 条；降级 false（无）
- 路线 `operator_card_fts`：12 条；降级 false（无）

### q002 · failure

- 原始查询：`agent abandons missing state read after incomplete positive summary`
- 规范化查询：`"agent" OR "abandons" OR "missing" OR "state" OR "read" OR "after" OR "incomplete" OR "positive" OR "summary"`
- 路线 `failure_card_fts`：12 条；降级 false（无）
- 路线 `passage_hybrid`：24 条；降级 false（无）
- 路线 `operator_card_fts`：12 条；降级 false（无）
- 路线 `paper_card_fts`：12 条；降级 false（无）

### q003 · operator

- 原始查询：`coverage carrying summary obligation set provenance commit guard`
- 规范化查询：`"coverage" OR "carrying" OR "summary" OR "obligation" OR "set" OR "provenance" OR "commit" OR "guard"`
- 路线 `operator_card_fts`：9 条；降级 false（无）
- 路线 `paper_card_fts`：12 条；降级 false（无）
- 路线 `passage_hybrid`：24 条；降级 false（无）
- 路线 `failure_card_fts`：12 条；降级 false（无）

### q004 · prior

- 原始查询：`ToolGate contract completeness MAP-Graph summary ancestry ProvenanceGuard precondition effect contracts`
- 规范化查询：`"ToolGate" OR "contract" OR "completeness" OR "MAP" OR "Graph" OR "summary" OR "ancestry" OR "ProvenanceGuard" OR "precondition" OR "effect" OR "contracts"`
- 路线 `paper_card_fts`：12 条；降级 false（无）
- 路线 `operator_card_fts`：12 条；降级 false（无）
- 路线 `failure_card_fts`：9 条；降级 false（无）
- 路线 `passage_hybrid`：24 条；降级 false（无）

### q005 · measurement

- 原始查询：`paired factorial aggregate READY neutral status explicit coverage metadata hidden missing precondition`
- 规范化查询：`"paired" OR "factorial" OR "aggregate" OR "READY" OR "neutral" OR "status" OR "explicit" OR "coverage" OR "metadata" OR "hidden" OR "missing" OR "precondition"`
- 路线 `paper_card_fts`：12 条；降级 false（无）
- 路线 `passage_hybrid`：24 条；降级 false（无）
- 路线 `failure_card_fts`：12 条；降级 false（无）
- 路线 `operator_card_fts`：12 条；降级 false（无）

## 覆盖诊断

- 去重 Card：96
- 去重 Evidence：121
- 去重 Passage：104
- 命中 Paper：69
- 原始观测：294
- 带机械噪声标记的观测：5
