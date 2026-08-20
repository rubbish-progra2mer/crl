<!-- CRL_RESEARCH_SEARCH_META {"created_at_utc":"2026-08-16T09:53:16.163398Z","request_fingerprint_sha256":"832046d3d6bddb9ebd50dd662857e72deaca929218c387fe6f8440da882c48a5","result_json_sha256":"78e51a50e5b38aef00fa5f7327767df4aa70b9a20d64bb4277497a0f3a15a4e4","search_id":"active-effect-diagnosis-001"} -->
# 研究检索导航

> 本报告仅展示查询路线、来源、命中定位与覆盖；所有科研判断由主研究者完成。

- 搜索标识：`active-effect-diagnosis-001`
- 生成时间（协调世界时）：`2026-08-16T09:53:16.163398Z`

## 紧凑研究地图

> 跨路线按 Paper 去重；每个查询路线至多选一个尚未出现的最高排名代表项。完整原始命中保留在 `result.json`。

- Paper `P074` · ToolGate: Contract-Grounded and Verified Tool Execution for LLMs；用途 `problem`；路线 `q001:paper_card_fts` #1；Card `paper-p074`（paper）；Evidence `ev-p074-contract-state-commit`, `ev-p074-missing-schema-true-postcondition`
- Paper `P091` · Temporal Validity in Retrieval Memory: Eliminating Stale-Fact Errors for AI Agents over Evolving Knowledge；用途 `problem`；路线 `q001:failure_card_fts` #1；Card `failure-cosine-cannot-separate-contradiction-from-duplicate`（failure）；Evidence `ev-p091-cosine-auroc`, `ev-p091-retain-fabrication`
- Paper `P030` · STALE: Can LLM Agents Know When Their Memories Are No Longer Valid?；用途 `problem`；路线 `q001:passage_hybrid` #1；Passage `P030:p0034:s0001`
- Paper `P007` · tau-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains；用途 `problem`；路线 `q001:operator_card_fts` #1；Card `operator-terminal-state-reliability-evaluation`（operator）；Evidence `ev-p007-terminal-state-evaluation`
- Paper `P040` · From Confident Closing to Silent Failure: Characterizing False Success in LLM Agents；用途 `failure`；路线 `q002:failure_card_fts` #3；Card `failure-confident-completion-without-state-success`（failure）；Evidence `ev-p040-failure-core`
- Paper `P099` · Verus-SpecGym: An Agentic Environment for Evaluating Specification Autoformalization；用途 `failure`；路线 `q002:passage_hybrid` #8；Passage `P099:p0014:s0001`
- Paper `P062` · Agentic Memory: Learning Unified Long-Term and Short-Term Memory Management for Large Language Model Agents；用途 `failure`；路线 `q002:operator_card_fts` #4；Card `operator-unified-language-memory-action-policy`（operator）；Evidence `ev-p062-broadcast-advantage`, `ev-p062-unified-memory-action-policy`
- Paper `P028` · Memory-R1: Enhancing Large Language Model Agents to Manage and Utilize Memories via Reinforcement Learning；用途 `failure`；路线 `q002:paper_card_fts` #5；Card `paper-p028`（paper）；Evidence `ev-p028-operator-core`
- Paper `P050` · Scaling Agentic Verifier for Competitive Coding；用途 `operator`；路线 `q003:operator_card_fts` #1；Card `operator-active-counterexample-verifier`（operator）；Evidence `ev-p050-operator-core`
- Paper `P072` · Structured Uncertainty guided Clarification for LLM Agents；用途 `operator`；路线 `q003:paper_card_fts` #2；Card `paper-p072`（paper）；Evidence `ev-p072-compute-boundary`, `ev-p072-structured-clarification-gate`, `ev-p072-unstructured-clarification-failure`
- Paper `P068` · DeepFact: Co-Evolving Benchmarks and Agents for Deep Research Factuality；用途 `operator`；路线 `q003:passage_hybrid` #2；Passage `P068:p0016:s0001`
- Paper `P026` · Agent Lightning: Train ANY AI Agents with Reinforcement Learning；用途 `operator`；路线 `q003:failure_card_fts` #1；Card `failure-uniform-terminal-return-erases-step-credit`（failure）；Evidence `ev-p026-transition-decomposition`, `ev-p026-uniform-terminal-return`
- Paper `P012` · Reflexion: Language Agents with Verbal Reinforcement Learning；用途 `prior`；路线 `q004:paper_card_fts` #2；Card `paper-reflexion`（paper）；Evidence `ev-p012-forced-retry-harmful-edits`, `ev-p012-verbal-reflection-memory`
- Paper `P079` · Learning to Contextualize Web Pages for Enhanced Decision Making by LLM Agents；用途 `prior`；路线 `q004:operator_card_fts` #2；Card `operator-action-preserving-observation-contextualization`（operator）；Evidence `ev-p079-action-conditioned-contextualization`, `ev-p079-ground-truth-action-retry`, `ev-p079-unseen-ui-boundary`
- Paper `P018` · ExpeL: LLM Agents Are Experiential Learners；用途 `prior`；路线 `q004:failure_card_fts` #2；Card `failure-unfiltered-reflection-contamination`（failure）；Evidence `ev-p018-raw-reflection-contamination`
- Paper `P046` · Solver-Aided Verification of Policy Compliance in Tool-Augmented LLM Agents；用途 `prior`；路线 `q004:passage_hybrid` #2；Passage `P046:p0003:s0001`
- Paper `P006` · An LLM Compiler for Parallel Function Calling；用途 `measurement`；路线 `q005:paper_card_fts` #4；Card `paper-llmcompiler`（paper）；Evidence `ev-p006-dependency-dag-dispatch`, `ev-p006-shared-prompt-comparison-boundary`, `ev-p006-token-cost-accounting`
- Paper `P097` · ReLoop: Structured Modeling and Behavioral Verification for Reliable LLM-Based Optimization；用途 `measurement`；路线 `q005:passage_hybrid` #1；Passage `P097:p0023:s0001`
- Paper `P069` · Tool Preferences in Agentic LLMs are Unreliable；用途 `measurement`；路线 `q005:failure_card_fts` #2；Card `failure-tool-description-and-order-bias`（failure）；Evidence `ev-p069-description-induced-preference`, `ev-p069-identical-tool-order-bias`
- Paper `P021` · In-the-Flow Agentic System Optimization for Effective Planning and Tool Use；用途 `measurement`；路线 `q005:operator_card_fts` #5；Card `operator-outcome-trained-execution-state-planner`（operator）；Evidence `ev-p021-operator-core`

- 代表项：20 / 去重 Paper：90

## 查询与路线覆盖

### q001 · problem

- 原始查询：`non-atomic ambiguous tool execution partial commit delayed visibility unsafe retry duplicate side effect`
- 规范化查询：`"non" OR "atomic" OR "ambiguous" OR "tool" OR "execution" OR "partial" OR "commit" OR "delayed" OR "visibility" OR "unsafe" OR "retry" OR "duplicate" OR "side" OR "effect"`
- 路线 `paper_card_fts`：24 条；降级 false（无）
- 路线 `failure_card_fts`：24 条；降级 false（无）
- 路线 `passage_hybrid`：24 条；降级 false（无）
- 路线 `operator_card_fts`：24 条；降级 false（无）

### q002 · failure

- 原始查询：`incomplete postcondition false verified state stale read partial write ambiguous result`
- 规范化查询：`"incomplete" OR "postcondition" OR "false" OR "verified" OR "state" OR "stale" OR "read" OR "partial" OR "write" OR "ambiguous" OR "result"`
- 路线 `failure_card_fts`：22 条；降级 false（无）
- 路线 `passage_hybrid`：24 条；降级 false（无）
- 路线 `operator_card_fts`：24 条；降级 false（无）
- 路线 `paper_card_fts`：24 条；降级 false（无）

### q003 · operator

- 原始查询：`active diagnosis information gain verifier selection recovery action ambiguity`
- 规范化查询：`"active" OR "diagnosis" OR "information" OR "gain" OR "verifier" OR "selection" OR "recovery" OR "action" OR "ambiguity"`
- 路线 `operator_card_fts`：24 条；降级 false（无）
- 路线 `paper_card_fts`：24 条；降级 false（无）
- 路线 `passage_hybrid`：24 条；降级 false（无）
- 路线 `failure_card_fts`：24 条；降级 false（无）

### q004 · prior

- 原始查询：`verify before retry idempotency postcondition ToolGate transactional tool calls`
- 规范化查询：`"verify" OR "before" OR "retry" OR "idempotency" OR "postcondition" OR "ToolGate" OR "transactional" OR "tool" OR "calls"`
- 路线 `paper_card_fts`：24 条；降级 false（无）
- 路线 `operator_card_fts`：24 条；降级 false（无）
- 路线 `failure_card_fts`：24 条；降级 false（无）
- 路线 `passage_hybrid`：24 条；降级 false（无）

### q005 · measurement

- 原始查询：`unsafe retry duplicate side effect read cost terminal state task success`
- 规范化查询：`"unsafe" OR "retry" OR "duplicate" OR "side" OR "effect" OR "read" OR "cost" OR "terminal" OR "state" OR "task" OR "success"`
- 路线 `paper_card_fts`：24 条；降级 false（无）
- 路线 `passage_hybrid`：24 条；降级 false（无）
- 路线 `failure_card_fts`：24 条；降级 false（无）
- 路线 `operator_card_fts`：24 条；降级 false（无）

## 覆盖诊断

- 去重 Card：173
- 去重 Evidence：194
- 去重 Passage：96
- 命中 Paper：90
- 原始观测：478
- 带机械噪声标记的观测：2
