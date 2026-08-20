<!-- CRL_RESEARCH_SEARCH_META {"created_at_utc":"2026-08-16T10:25:57.374674Z","request_fingerprint_sha256":"646ae078bc7634c4ae85a4b26cd4482f08e8008fbe486579eade7b5a0e7b91dd","result_json_sha256":"62afb6496cb67847ab492f477e7fd3499e7bfa0fbc31f33632251b4be97c6c1c","search_id":"stale-observation-invalidation-001"} -->
# 研究检索导航

> 本报告仅展示查询路线、来源、命中定位与覆盖；所有科研判断由主研究者完成。

- 搜索标识：`stale-observation-invalidation-001`
- 生成时间（协调世界时）：`2026-08-16T10:25:57.374674Z`

## 紧凑研究地图

> 跨路线按 Paper 去重；每个查询路线至多选一个尚未出现的最高排名代表项。完整原始命中保留在 `result.json`。

- Paper `P030` · STALE: Can LLM Agents Know When Their Memories Are No Longer Valid?；用途 `problem`；路线 `q001:paper_card_fts` #1；Card `paper-p030`（paper）；Evidence `ev-p030-failure-core`
- Paper `P091` · Temporal Validity in Retrieval Memory: Eliminating Stale-Fact Errors for AI Agents over Evolving Knowledge；用途 `problem`；路线 `q001:failure_card_fts` #1；Card `failure-cosine-cannot-separate-contradiction-from-duplicate`（failure）；Evidence `ev-p091-cosine-auroc`, `ev-p091-retain-fabrication`
- Paper `P071` · Agentic Plan Caching: Test-Time Memory for Fast and Cost-Efficient LLM Agents；用途 `problem`；路线 `q001:passage_hybrid` #2；Passage `P071:p0027:s0001`
- Paper `P074` · ToolGate: Contract-Grounded and Verified Tool Execution for LLMs；用途 `problem`；路线 `q001:operator_card_fts` #1；Card `operator-contract-gated-tool-state-commit`（operator）；Evidence `ev-p074-contract-state-commit`, `ev-p074-missing-schema-true-postcondition`
- Paper `P036` · tau-Knowledge: Evaluating Conversational Agents over Unstructured Knowledge；用途 `failure`；路线 `q002:failure_card_fts` #2；Card `failure-gold-context-does-not-solve-knowledge-use`（failure）；Evidence `ev-p036-failure-core`
- Paper `P008` · Agent Security Bench (ASB): Formalizing and Benchmarking Attacks and Defenses in LLM-based Agents；用途 `failure`；路线 `q002:passage_hybrid` #4；Passage `P008:p0023:s0001`
- Paper `P028` · Memory-R1: Enhancing Large Language Model Agents to Manage and Utilize Memories via Reinforcement Learning；用途 `failure`；路线 `q002:operator_card_fts` #2；Card `operator-learned-memory-crud-control`（operator）；Evidence `ev-p028-operator-core`
- Paper `P005` · ToolLLM: Facilitating Large Language Models to Master 16000+ Real-world APIs；用途 `failure`；路线 `q002:paper_card_fts` #2；Card `paper-p005`（paper）；Evidence `ev-p005-operator-core`
- Paper `P063` · A-Mem: Agentic Memory for LLM Agents；用途 `operator`；路线 `q003:operator_card_fts` #1；Card `operator-dynamic-linked-memory-evolution`（operator）；Evidence `ev-p063-dynamic-link-generation`, `ev-p063-neighbor-rewrite-action`, `ev-p063-retrieval-k-varies`
- Paper `P006` · An LLM Compiler for Parallel Function Calling；用途 `operator`；路线 `q003:paper_card_fts` #1；Card `paper-llmcompiler`（paper）；Evidence `ev-p006-dependency-dag-dispatch`, `ev-p006-shared-prompt-comparison-boundary`, `ev-p006-token-cost-accounting`
- Paper `P068` · DeepFact: Co-Evolving Benchmarks and Agents for Deep Research Factuality；用途 `operator`；路线 `q003:passage_hybrid` #6；Passage `P068:p0031:s0001`
- Paper `P083` · TAMAS: Benchmarking Adversarial Risks in Multi-Agent LLM Systems；用途 `operator`；路线 `q003:failure_card_fts` #1；Card `failure-multi-agent-adversarial-coordination-spans-trust-surfaces`（failure）；Evidence `ev-p083-lightweight-defense-failure`, `ev-p083-simulated-tool-boundary`, `ev-p083-three-surface-adversarial-failure`
- Paper `P070` · ProMCP: Profiling Token Flows and Latency Costs in Model Context Protocol-Based LLM Agents；用途 `prior`；路线 `q004:paper_card_fts` #2；Card `paper-p070`（paper）；Evidence `ev-p070-light-tool-runtime-boundary`, `ev-p070-orchestration-bottleneck`, `ev-p070-six-stage-attribution`
- Paper `P099` · Verus-SpecGym: An Agentic Environment for Evaluating Specification Autoformalization；用途 `prior`；路线 `q004:operator_card_fts` #4；Card `operator-four-bucket-executable-spec-testing`（operator）；Evidence `ev-p099-judge-miss`, `ev-p099-soundness-necessity`, `ev-p099-two-stage-check`
- Paper `P081` · Self-Consistency Improves Chain of Thought Reasoning in Language Models；用途 `prior`；路线 `q004:failure_card_fts` #3；Card `failure-interactive-gains-collapse-against-independent-sampling`（failure）；Evidence `ev-p081-fixed-answer-space-boundary`, `ev-p081-forty-sample-baseline`, `ev-p081-independent-path-majority-aggregation`
- Paper `P031` · Agent Memory: Characterization and System Implications of Stateful Long-Horizon Workloads；用途 `prior`；路线 `q004:passage_hybrid` #2；Passage `P031:p0002:s0001`
- Paper `P066` · The Berkeley Function Calling Leaderboard (BFCL): From Tool Use to Agentic Evaluation of Large Language Models；用途 `measurement`；路线 `q005:paper_card_fts` #2；Card `paper-p066`（paper）；Evidence `ev-p066-multiturn-state-evaluation`, `ev-p066-single-to-stateful-gap`
- Paper `P092` · MemConflict: Evaluating Long-Term Memory Systems Under Memory Conflicts；用途 `measurement`；路线 `q005:passage_hybrid` #18；Passage `P092:p0018:s0002`
- Paper `P054` · On the Limit of Language Models as Planning Formalizers；用途 `measurement`；路线 `q005:failure_card_fts` #5；Card `failure-constraint-shift-breaks-formalization`（failure）；Evidence `ev-p054-natural-language-implicit-predicate-failure`
- Paper `P014` · Instruct-of-Reflection: Enhancing Large Language Models Iterative Reflection Capabilities via Dynamic-Meta Instruction；用途 `measurement`；路线 `q005:operator_card_fts` #3；Card `operator-dynamic-reflection-gate`（operator）；Evidence `ev-p014-dynamic-reflection-gate`

- 代表项：20 / 去重 Paper：91

## 查询与路线覆盖

### q001 · problem

- 原始查询：`LLM agent tool stale observation after mutation cached result invalidation state version consistency`
- 规范化查询：`"LLM" OR "agent" OR "tool" OR "stale" OR "observation" OR "after" OR "mutation" OR "cached" OR "result" OR "invalidation" OR "state" OR "version" OR "consistency"`
- 路线 `paper_card_fts`：24 条；降级 false（无）
- 路线 `failure_card_fts`：24 条；降级 false（无）
- 路线 `passage_hybrid`：24 条；降级 false（无）
- 路线 `operator_card_fts`：24 条；降级 false（无）

### q002 · failure

- 原始查询：`tool agent uses outdated result after write stale context inconsistent state irreversible action`
- 规范化查询：`"tool" OR "agent" OR "uses" OR "outdated" OR "result" OR "after" OR "write" OR "stale" OR "context" OR "inconsistent" OR "state" OR "irreversible" OR "action"`
- 路线 `failure_card_fts`：24 条；降级 false（无）
- 路线 `passage_hybrid`：24 条；降级 false（无）
- 路线 `operator_card_fts`：24 条；降级 false（无）
- 路线 `paper_card_fts`：24 条；降级 false（无）

### q003 · operator

- 原始查询：`resource read set write set dependency provenance invalidate refresh tool observation`
- 规范化查询：`"resource" OR "read" OR "set" OR "write" OR "dependency" OR "provenance" OR "invalidate" OR "refresh" OR "tool" OR "observation"`
- 路线 `operator_card_fts`：24 条；降级 false（无）
- 路线 `paper_card_fts`：24 条；降级 false（无）
- 路线 `passage_hybrid`：24 条；降级 false（无）
- 路线 `failure_card_fts`：24 条；降级 false（无）

### q004 · prior

- 原始查询：`transactional tool use cache coherence optimistic concurrency agent runtime snapshot consistency`
- 规范化查询：`"transactional" OR "tool" OR "use" OR "cache" OR "coherence" OR "optimistic" OR "concurrency" OR "agent" OR "runtime" OR "snapshot" OR "consistency"`
- 路线 `paper_card_fts`：24 条；降级 false（无）
- 路线 `operator_card_fts`：24 条；降级 false（无）
- 路线 `failure_card_fts`：24 条；降级 false（无）
- 路线 `passage_hybrid`：24 条；降级 false（无）

### q005 · measurement

- 原始查询：`stateful tool benchmark stale read write conflict refresh correctness extra calls`
- 规范化查询：`"stateful" OR "tool" OR "benchmark" OR "stale" OR "read" OR "write" OR "conflict" OR "refresh" OR "correctness" OR "extra" OR "calls"`
- 路线 `paper_card_fts`：24 条；降级 false（无）
- 路线 `passage_hybrid`：24 条；降级 false（无）
- 路线 `failure_card_fts`：24 条；降级 false（无）
- 路线 `operator_card_fts`：24 条；降级 false（无）

## 覆盖诊断

- 去重 Card：163
- 去重 Evidence：194
- 去重 Passage：88
- 命中 Paper：91
- 原始观测：480
- 带机械噪声标记的观测：5
