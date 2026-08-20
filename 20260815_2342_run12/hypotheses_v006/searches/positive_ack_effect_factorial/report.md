<!-- CRL_RESEARCH_SEARCH_META {"created_at_utc":"2026-08-16T06:31:56.065076Z","request_fingerprint_sha256":"6eb5ce5b189cda852c26fc9d414e6a58def012c2c7a8a00f09996f5fe926c2c5","result_json_sha256":"f8fb03ffc68fcf19af9134e037abe6cb9237e5d81411f1b388f647e2529f127d","search_id":"positive_ack_effect_factorial"} -->
# 研究检索导航

> 本报告仅展示查询路线、来源、命中定位与覆盖；所有科研判断由主研究者完成。

- 搜索标识：`positive_ack_effect_factorial`
- 生成时间（协调世界时）：`2026-08-16T06:31:56.065076Z`

## 紧凑研究地图

> 跨路线按 Paper 去重；每个查询路线至多选一个尚未出现的最高排名代表项。完整原始命中保留在 `result.json`。

- Paper `P040` · From Confident Closing to Silent Failure: Characterizing False Success in LLM Agents；用途 `problem`；路线 `q001:paper_card_fts` #1；Card `paper-p040`（paper）；Evidence `ev-p040-failure-core`
- Paper `P069` · Tool Preferences in Agentic LLMs are Unreliable；用途 `problem`；路线 `q001:failure_card_fts` #2；Card `failure-tool-description-and-order-bias`（failure）；Evidence `ev-p069-description-induced-preference`, `ev-p069-identical-tool-order-bias`
- Paper `P035` · Holistic Agent Leaderboard: The Missing Infrastructure for AI Agent Evaluation；用途 `problem`；路线 `q001:passage_hybrid` #2；Passage `P035:p0028:s0001`
- Paper `P007` · tau-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains；用途 `problem`；路线 `q001:operator_card_fts` #1；Card `operator-terminal-state-reliability-evaluation`（operator）；Evidence `ev-p007-terminal-state-evaluation`
- Paper `P074` · ToolGate: Contract-Grounded and Verified Tool Execution for LLMs；用途 `prior`；路线 `q002:paper_card_fts` #1；Card `paper-p074`（paper）；Evidence `ev-p074-contract-state-commit`, `ev-p074-missing-schema-true-postcondition`
- Paper `P008` · Agent Security Bench (ASB): Formalizing and Benchmarking Attacks and Defenses in LLM-based Agents；用途 `prior`；路线 `q002:operator_card_fts` #2；Card `operator-stagewise-agent-security-audit`（operator）；Evidence `ev-p008-stagewise-attack-surface`
- Paper `P054` · On the Limit of Language Models as Planning Formalizers；用途 `prior`；路线 `q002:failure_card_fts` #3；Card `failure-constraint-shift-breaks-formalization`（failure）；Evidence `ev-p054-natural-language-implicit-predicate-failure`
- Paper `P030` · STALE: Can LLM Agents Know When Their Memories Are No Longer Valid?；用途 `prior`；路线 `q002:passage_hybrid` #6；Passage `P030:p0025:s0001`
- Paper `P028` · Memory-R1: Enhancing Large Language Model Agents to Manage and Utilize Memories via Reinforcement Learning；用途 `measurement`；路线 `q003:paper_card_fts` #1；Card `paper-p028`（paper）；Evidence `ev-p028-operator-core`
- Paper `P025` · Unlocking the Power of Multi-Agent LLM for Reasoning: From Lazy Agents to Deliberation；用途 `measurement`；路线 `q003:passage_hybrid` #2；Passage `P025:p0005:s0004`
- Paper `P011` · On Memory Construction and Retrieval for Personalized Conversational Agents；用途 `measurement`；路线 `q003:failure_card_fts` #1；Card `failure-memory-unit-granularity-mismatch`（failure）；Evidence `ev-p011-failure-core`
- Paper `P094` · Evaluating Memory in LLM Agents via Incremental Multi-Turn Interactions；用途 `measurement`；路线 `q003:operator_card_fts` #1；Card `operator-incremental-injection-benchmark-reconstruction`（operator）；Evidence `ev-p094-incremental-protocol`, `ev-p094-sf-guardrails`

- 代表项：12 / 去重 Paper：56

## 查询与路线覆盖

### q001 · problem

- 原始查询：`tool response success acknowledgement suppress verification effect absent silent no-op agent`
- 规范化查询：`"tool" OR "response" OR "success" OR "acknowledgement" OR "suppress" OR "verification" OR "effect" OR "absent" OR "silent" OR "no" OR "op" OR "agent"`
- 路线 `paper_card_fts`：12 条；降级 false（无）
- 路线 `failure_card_fts`：12 条；降级 false（无）
- 路线 `passage_hybrid`：18 条；降级 false（无）
- 路线 `operator_card_fts`：12 条；降级 false（无）

### q002 · prior

- 原始查询：`false success response effect channel orthogonal factorial manipulation SUCCESS AMBIGUOUS postcondition`
- 规范化查询：`"false" OR "success" OR "response" OR "effect" OR "channel" OR "orthogonal" OR "factorial" OR "manipulation" OR "AMBIGUOUS" OR "postcondition"`
- 路线 `paper_card_fts`：12 条；降级 false（无）
- 路线 `operator_card_fts`：12 条；降级 false（无）
- 路线 `failure_card_fts`：12 条；降级 false（无）
- 路线 `passage_hybrid`：18 条；降级 false（无）

### q003 · measurement

- 原始查询：`causal two by two response label external effect readback unsafe downstream commitment`
- 规范化查询：`"causal" OR "two" OR "by" OR "response" OR "label" OR "external" OR "effect" OR "readback" OR "unsafe" OR "downstream" OR "commitment"`
- 路线 `paper_card_fts`：12 条；降级 false（无）
- 路线 `passage_hybrid`：18 条；降级 false（无）
- 路线 `failure_card_fts`：12 条；降级 false（无）
- 路线 `operator_card_fts`：12 条；降级 false（无）

## 覆盖诊断

- 去重 Card：76
- 去重 Evidence：107
- 去重 Passage：48
- 命中 Paper：56
- 原始观测：162
- 带机械噪声标记的观测：1
