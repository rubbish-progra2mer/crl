<!-- CRL_RESEARCH_SEARCH_META {"created_at_utc":"2026-08-16T06:12:41.338762Z","request_fingerprint_sha256":"cc5fd3196accfacbc6184b41544983f8fd1c4b6e97ce61ee814f77c40870582d","result_json_sha256":"58e699c31289e4b5859b3a213dc705de8f7b73ac9e6318d522984c0506d6952e","search_id":"history_retraction_map"} -->
# 研究检索导航

> 本报告仅展示查询路线、来源、命中定位与覆盖；所有科研判断由主研究者完成。

- 搜索标识：`history_retraction_map`
- 生成时间（协调世界时）：`2026-08-16T06:12:41.338762Z`

## 紧凑研究地图

> 跨路线按 Paper 去重；每个查询路线至多选一个尚未出现的最高排名代表项。完整原始命中保留在 `result.json`。

- Paper `P010` · LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory；用途 `problem`；路线 `q001:paper_card_fts` #1；Card `paper-longmemeval`（paper）；Evidence `ev-p010-index-retrieve-read`, `ev-p010-long-history-decline`
- Paper `P094` · Evaluating Memory in LLM Agents via Incremental Multi-Turn Interactions；用途 `problem`；路线 `q001:failure_card_fts` #1；Card `failure-selective-forgetting-collapses-with-context-length`（failure）；Evidence `ev-p094-sf-guardrails`, `ev-p094-sf-length-collapse`
- Paper `P031` · Agent Memory: Characterization and System Implications of Stateful Long-Horizon Workloads；用途 `problem`；路线 `q001:passage_hybrid` #1；Passage `P031:p0003:s0002`
- Paper `P030` · STALE: Can LLM Agents Know When Their Memories Are No Longer Valid?；用途 `problem`；路线 `q001:operator_card_fts` #1；Card `operator-write-side-state-adjudication`（operator）；Evidence `ev-p030-authorized-readout`, `ev-p030-failure-core`, `ev-p030-write-side-adjudication`
- Paper `P011` · On Memory Construction and Retrieval for Personalized Conversational Agents；用途 `failure`；路线 `q002:failure_card_fts` #1；Card `failure-memory-unit-granularity-mismatch`（failure）；Evidence `ev-p011-failure-core`
- Paper `P021` · In-the-Flow Agentic System Optimization for Effective Planning and Tool Use；用途 `failure`；路线 `q002:passage_hybrid` #1；Passage `P021:p0026:s0001`
- Paper `P090` · From Single to Multi-Granularity: Toward Long-Term Memory Association and Selection of Conversational Agents；用途 `failure`；路线 `q002:operator_card_fts` #1；Card `operator-entropy-routed-multi-granularity-retrieval`（operator）；Evidence `ev-p090-association-graph`, `ev-p090-entropy-router`
- Paper `P019` · STeCa: Step-level Trajectory Calibration for LLM Agent Learning；用途 `failure`；路线 `q002:paper_card_fts` #1；Card `paper-p019`（paper）；Evidence `ev-p019-ground-truth-calibration-oracle`, `ev-p019-step-level-calibration`
- Paper `P091` · Temporal Validity in Retrieval Memory: Eliminating Stale-Fact Errors for AI Agents over Evolving Knowledge；用途 `operator`；路线 `q003:operator_card_fts` #1；Card `operator-deterministic-sro-supersession-ledger`（operator）；Evidence `ev-p091-retain-fabrication`, `ev-p091-supersession-rule`
- Paper `P037` · ToolSandbox: A Stateful, Conversational, Interactive Evaluation Benchmark for LLM Tool Use Capabilities；用途 `operator`；路线 `q003:paper_card_fts` #2；Card `paper-p037`（paper）；Evidence `ev-p037-evaluation-core`
- Paper `P092` · MemConflict: Evaluating Long-Term Memory Systems Under Memory Conflicts；用途 `operator`；路线 `q003:passage_hybrid` #6；Passage `P092:p0017:s0001`
- Paper `P004` · TravelPlanner: A Benchmark for Real-World Planning with Language Agents；用途 `operator`；路线 `q003:failure_card_fts` #3；Card `failure-constrained-plan-surface-validity`（failure）；Evidence `ev-p004-failure-core`, `ev-p004-macro-constraint-failure`
- Paper `P009` · MemGPT: Towards LLMs as Operating Systems；用途 `prior`；路线 `q004:paper_card_fts` #3；Card `paper-p009`（paper）；Evidence `ev-p009-operator-core`
- Paper `P079` · Learning to Contextualize Web Pages for Enhanced Decision Making by LLM Agents；用途 `prior`；路线 `q004:operator_card_fts` #3；Card `operator-action-preserving-observation-contextualization`（operator）；Evidence `ev-p079-action-conditioned-contextualization`, `ev-p079-ground-truth-action-retry`, `ev-p079-unseen-ui-boundary`
- Paper `P053` · Language Models as Higher-Order Planning Formalizers；用途 `prior`；路线 `q004:failure_card_fts` #5；Card `failure-grounded-formalization-output-expansion`（failure）；Evidence `ev-p053-higher-order-generator`, `ev-p053-parser-evaluation-boundary`, `ev-p053-pattern-review-confound`
- Paper `P029` · MemFail: Stress-Testing Failure Modes of LLM Memory Systems；用途 `prior`；路线 `q004:passage_hybrid` #2；Passage `P029:p0002:s0002`
- Paper `P068` · DeepFact: Co-Evolving Benchmarks and Agents for Deep Research Factuality；用途 `measurement`；路线 `q005:paper_card_fts` #3；Card `paper-p068`（paper）；Evidence `ev-p068-audit-then-score`, `ev-p068-one-shot-gold-brittle`
- Paper `P034` · RefineBench: Evaluating Refinement Capability of Language Models via Checklists；用途 `measurement`；路线 `q005:passage_hybrid` #4；Passage `P034:p0011:s0001`
- Paper `P013` · Large Language Models Cannot Self-Correct Reasoning Yet；用途 `measurement`；路线 `q005:failure_card_fts` #2；Card `failure-intrinsic-self-correction-degradation`（failure）；Evidence `ev-p013-intrinsic-self-correction-degrades`, `ev-p013-oracle-free-equal-budget-boundary`
- Paper `P027` · Verified Critical Step Optimization for LLM Agents；用途 `measurement`；路线 `q005:operator_card_fts` #1；Card `operator-verified-single-branch-repair`（operator）；Evidence `ev-p027-operator-core`

- 代表项：20 / 去重 Paper：72

## 查询与路线覆盖

### q001 · problem

- 原始查询：`LLM agent context compaction history summarization stale invalidated facts corrections retractions long horizon memory`
- 规范化查询：`"LLM" OR "agent" OR "context" OR "compaction" OR "history" OR "summarization" OR "stale" OR "invalidated" OR "facts" OR "corrections" OR "retractions" OR "long" OR "horizon" OR "memory"`
- 路线 `paper_card_fts`：15 条；降级 false（无）
- 路线 `failure_card_fts`：15 条；降级 false（无）
- 路线 `passage_hybrid`：15 条；降级 false（无）
- 路线 `operator_card_fts`：15 条；降级 false（无）

### q002 · failure

- 原始查询：`agent memory summary forgets correction revocation superseded constraint causes wrong tool action`
- 规范化查询：`"agent" OR "memory" OR "summary" OR "forgets" OR "correction" OR "revocation" OR "superseded" OR "constraint" OR "causes" OR "wrong" OR "tool" OR "action"`
- 路线 `failure_card_fts`：15 条；降级 false（无）
- 路线 `passage_hybrid`：15 条；降级 false（无）
- 路线 `operator_card_fts`：15 条；降级 false（无）
- 路线 `paper_card_fts`：15 条；降级 false（无）

### q003 · operator

- 原始查询：`event sourced state ledger temporal validity belief revision memory consolidation agent`
- 规范化查询：`"event" OR "sourced" OR "state" OR "ledger" OR "temporal" OR "validity" OR "belief" OR "revision" OR "memory" OR "consolidation" OR "agent"`
- 路线 `operator_card_fts`：15 条；降级 false（无）
- 路线 `paper_card_fts`：15 条；降级 false（无）
- 路线 `passage_hybrid`：15 条；降级 false（无）
- 路线 `failure_card_fts`：15 条；降级 false（无）

### q004 · prior

- 原始查询：`LLM agent memory consistency stale memory contradiction resolution context compression summarization benchmark`
- 规范化查询：`"LLM" OR "agent" OR "memory" OR "consistency" OR "stale" OR "contradiction" OR "resolution" OR "context" OR "compression" OR "summarization" OR "benchmark"`
- 路线 `paper_card_fts`：15 条；降级 false（无）
- 路线 `operator_card_fts`：15 条；降级 false（无）
- 路线 `failure_card_fts`：15 条；降级 false（无）
- 路线 `passage_hybrid`：15 条；降级 false（无）

### q005 · measurement

- 原始查询：`counterfactual history compression retraction retention correction benchmark tool agent`
- 规范化查询：`"counterfactual" OR "history" OR "compression" OR "retraction" OR "retention" OR "correction" OR "benchmark" OR "tool" OR "agent"`
- 路线 `paper_card_fts`：15 条；降级 false（无）
- 路线 `passage_hybrid`：15 条；降级 false（无）
- 路线 `failure_card_fts`：15 条；降级 false（无）
- 路线 `operator_card_fts`：15 条；降级 false（无）

## 覆盖诊断

- 去重 Card：120
- 去重 Evidence：150
- 去重 Passage：65
- 命中 Paper：72
- 原始观测：300
- 带机械噪声标记的观测：0
