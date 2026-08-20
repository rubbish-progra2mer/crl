<!-- CRL_RESEARCH_SEARCH_META {"created_at_utc":"2026-08-16T06:57:18.445367Z","request_fingerprint_sha256":"96bb041dce894f01de7af1594bd29a1d08751ab0bd8f71f7d48edd4314e8afb0","result_json_sha256":"b4001bfdeaa837aff9281cf4ca0063a802527c6ea8aa5af63037c05514444819","search_id":"robust_verification_cut_attack"} -->
# 研究检索导航

> 本报告仅展示查询路线、来源、命中定位与覆盖；所有科研判断由主研究者完成。

- 搜索标识：`robust_verification_cut_attack`
- 生成时间（协调世界时）：`2026-08-16T06:57:18.445367Z`

## 紧凑研究地图

> 跨路线按 Paper 去重；每个查询路线至多选一个尚未出现的最高排名代表项。完整原始命中保留在 `result.json`。

- Paper `P048` · NaviAgent: Graph-Driven Bilevel Planning for Scalable Tool Orchestration；用途 `problem`；路线 `q001:paper_card_fts` #1；Card `paper-p048`（paper）；Evidence `ev-p048-operator-core`
- Paper `P056` · GPTSwarm: Language Agents as Optimizable Graphs；用途 `problem`；路线 `q001:failure_card_fts` #1；Card `failure-same-set-agent-graph-evaluation`（failure）；Evidence `ev-p056-graph-optimization`, `ev-p056-same-set-crosswords`
- Paper `P016` · Why Do Multi-Agent LLM Systems Fail?；用途 `problem`；路线 `q001:passage_hybrid` #2；Passage `P016:p0032:s0001`
- Paper `P057` · Automated Design of Agentic Systems；用途 `problem`；路线 `q001:operator_card_fts` #2；Card `operator-archive-conditioned-agent-code-search`（operator）；Evidence `ev-p057-archive-code-search`, `ev-p057-search-evaluation-budget`
- Paper `P059` · Multi-Agent Collaboration via Evolving Orchestration；用途 `operator`；路线 `q002:operator_card_fts` #1；Card `operator-state-conditioned-agent-activation`（operator）；Evidence `ev-p059-compact-cyclic-topology`, `ev-p059-state-conditioned-orchestrator`
- Paper `P083` · TAMAS: Benchmarking Adversarial Risks in Multi-Agent LLM Systems；用途 `operator`；路线 `q002:paper_card_fts` #1；Card `paper-p083`（paper）；Evidence `ev-p083-lightweight-defense-failure`, `ev-p083-simulated-tool-boundary`, `ev-p083-three-surface-adversarial-failure`
- Paper `P041` · LLM Agents Already Know When to Call Tools - Even Without Reasoning；用途 `operator`；路线 `q002:passage_hybrid` #2；Passage `P041:p0006:s0002`
- Paper `P003` · Language Agent Tree Search Unifies Reasoning, Acting, and Planning in Language Models；用途 `operator`；路线 `q002:failure_card_fts` #1；Card `failure-generic-reflection-local-minima`（failure）；Evidence `ev-p003-generic-reflection-local-minimum`
- Paper `P076` · Multi-Agent Systems Execute Arbitrary Malicious Code；用途 `prior`；路线 `q003:paper_card_fts` #1；Card `paper-p076`（paper）；Evidence `ev-p076-controlled-lab-boundary`, `ev-p076-metadata-control-flow-laundering`, `ev-p076-refusal-not-system-safety`
- Paper `P082` · Toolformer: Language Models Can Teach Themselves to Use Tools；用途 `prior`；路线 `q003:operator_card_fts` #2；Card `operator-future-token-loss-filtered-tool-learning`（operator）；Evidence `ev-p082-chaining-cost-sparsity-boundary`, `ev-p082-future-token-loss-filtered-calls`, `ev-p082-top-k-single-call-boundary`
- Paper `P096` · VeriSimpl: Robust Optimization Modeling from Natural Language using Simplification-based Verification；用途 `prior`；路线 `q003:failure_card_fts` #1；Card `failure-generator-aligned-verification-passes-shared-misreads`（failure）；Evidence `ev-p096-shared-misinterpretation`, `ev-p096-simplification-inversion`
- Paper `P008` · Agent Security Bench (ASB): Formalizing and Benchmarking Attacks and Defenses in LLM-based Agents；用途 `prior`；路线 `q003:passage_hybrid` #1；Passage `P008:p0017:s0001`
- Paper `P006` · An LLM Compiler for Parallel Function Calling；用途 `measurement`；路线 `q004:paper_card_fts` #2；Card `paper-llmcompiler`（paper）；Evidence `ev-p006-dependency-dag-dispatch`, `ev-p006-shared-prompt-comparison-boundary`, `ev-p006-token-cost-accounting`
- Paper `P074` · ToolGate: Contract-Grounded and Verified Tool Execution for LLMs；用途 `measurement`；路线 `q004:passage_hybrid` #1；Passage `P074:p0009:s0001`
- Paper `P065` · Group-in-Group Policy Optimization for LLM Agent Training；用途 `measurement`；路线 `q004:failure_card_fts` #2；Card `failure-anchor-state-credit-needs-state-recurrence`（failure）；Evidence `ev-p065-anchor-state-credit`, `ev-p065-state-recurrence-boundary`
- Paper `P101` · Semantic Evaluation for Text-to-SQL with Distilled Test Suites；用途 `measurement`；路线 `q004:operator_card_fts` #3；Card `operator-neighbor-distilled-test-suites`（operator）；Evidence `ev-p101-esm-fn-rate`, `ev-p101-neighbor-distillation`

- 代表项：16 / 去重 Paper：59

## 查询与路线覆盖

### q001 · problem

- 原始查询：`uncertain observed declared inferred agent dependency graph verification budget irreversible action`
- 规范化查询：`"uncertain" OR "observed" OR "declared" OR "inferred" OR "agent" OR "dependency" OR "graph" OR "verification" OR "budget" OR "irreversible" OR "action"`
- 路线 `paper_card_fts`：12 条；降级 false（无）
- 路线 `failure_card_fts`：12 条；降级 false（无）
- 路线 `passage_hybrid`：12 条；降级 false（无）
- 路线 `operator_card_fts`：12 条；降级 false（无）

### q002 · operator

- 原始查询：`robust minimum cut multicut monitor mediator placement uncertain topology active probing`
- 规范化查询：`"robust" OR "minimum" OR "cut" OR "multicut" OR "monitor" OR "mediator" OR "placement" OR "uncertain" OR "topology" OR "active" OR "probing"`
- 路线 `operator_card_fts`：6 条；降级 false（无）
- 路线 `paper_card_fts`：12 条；降级 false（无）
- 路线 `passage_hybrid`：12 条；降级 false（无）
- 路线 `failure_card_fts`：4 条；降级 false（无）

### q003 · prior

- 原始查询：`monitor placement data flow graph all source sink paths security verification checkpoint`
- 规范化查询：`"monitor" OR "placement" OR "data" OR "flow" OR "graph" OR "all" OR "source" OR "sink" OR "paths" OR "security" OR "verification" OR "checkpoint"`
- 路线 `paper_card_fts`：12 条；降级 false（无）
- 路线 `operator_card_fts`：12 条；降级 false（无）
- 路线 `failure_card_fts`：12 条；降级 false（无）
- 路线 `passage_hybrid`：12 条；降级 false（无）

### q004 · measurement

- 原始查询：`verification cost unsafe action rate graph edge observability dependency coverage`
- 规范化查询：`"verification" OR "cost" OR "unsafe" OR "action" OR "rate" OR "graph" OR "edge" OR "observability" OR "dependency" OR "coverage"`
- 路线 `paper_card_fts`：12 条；降级 false（无）
- 路线 `passage_hybrid`：12 条；降级 false（无）
- 路线 `failure_card_fts`：12 条；降级 false（无）
- 路线 `operator_card_fts`：12 条；降级 false（无）

## 覆盖诊断

- 去重 Card：77
- 去重 Evidence：111
- 去重 Passage：45
- 命中 Paper：59
- 原始观测：178
- 带机械噪声标记的观测：9
