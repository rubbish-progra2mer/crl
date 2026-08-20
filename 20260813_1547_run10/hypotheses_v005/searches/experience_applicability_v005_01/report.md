<!-- CRL_RESEARCH_SEARCH_META {"created_at_utc":"2026-08-13T10:01:29.917409Z","request_fingerprint_sha256":"d7abc3c37d3794b12e01bc479951dc998e9b85205374ed3149117081a183535b","result_json_sha256":"8a7a1883b452eb4e320a20e7b392640f4cf3636d71be86814969f93fbbef0b82","search_id":"experience_applicability_v005_01"} -->
# 研究检索导航

> 本报告仅展示查询路线、来源、命中定位与覆盖；所有科研判断由主研究者完成。

- 搜索标识：`experience_applicability_v005_01`
- 生成时间（协调世界时）：`2026-08-13T10:01:29.917409Z`

## 紧凑研究地图

> 跨路线按 Paper 去重；每个查询路线至多选一个尚未出现的最高排名代表项。完整原始命中保留在 `result.json`。

- Paper `P027` · Verified Critical Step Optimization for LLM Agents；用途 `problem`；路线 `q001:paper_card_fts` #1；Card `paper-p027`（paper）；Evidence `ev-p027-operator-core`
- Paper `P071` · Agentic Plan Caching: Test-Time Memory for Fast and Cost-Efficient LLM Agents；用途 `problem`；路线 `q001:failure_card_fts` #1；Card `failure-plan-cache-semantic-false-positives`（failure）；Evidence `ev-p071-cache-false-positive-boundary`, `ev-p071-plan-template-reuse`
- Paper `P064` · How Memory Management Impacts LLM Agents: An Empirical Study of Experience-Following Behavior；用途 `problem`；路线 `q001:passage_hybrid` #1；Passage `P064:p0002:s0001`
- Paper `P018` · ExpeL: LLM Agents Are Experiential Learners；用途 `problem`；路线 `q001:operator_card_fts` #3；Card `operator-experience-insight-update`（operator）；Evidence `ev-p018-insight-update-operations`
- Paper `P011` · On Memory Construction and Retrieval for Personalized Conversational Agents；用途 `failure`；路线 `q002:failure_card_fts` #2；Card `failure-memory-unit-granularity-mismatch`（failure）；Evidence `ev-p011-failure-core`
- Paper `P030` · STALE: Can LLM Agents Know When Their Memories Are No Longer Valid?；用途 `failure`；路线 `q002:passage_hybrid` #1；Passage `P030:p0009:s0001`
- Paper `P025` · Unlocking the Power of Multi-Agent LLM for Reasoning: From Lazy Agents to Deliberation；用途 `failure`；路线 `q002:operator_card_fts` #2；Card `operator-grouped-masked-history-step-credit`（operator）；Evidence `ev-p025-failure-core`, `ev-p025-grouped-step-influence`
- Paper `P051` · Large Language Models Can Solve Real-World Planning Rigorously with Formal Verification Tools；用途 `failure`；路线 `q002:paper_card_fts` #2；Card `paper-p051`（paper）；Evidence `ev-p051-cost-boundary`, `ev-p051-formalization-pipeline`, `ev-p051-omitted-constraint-failure`, `ev-p051-solver-guarantee-boundary`
- Paper `P090` · From Single to Multi-Granularity: Toward Long-Term Memory Association and Selection of Conversational Agents；用途 `operator`；路线 `q003:operator_card_fts` #4；Card `operator-entropy-routed-multi-granularity-retrieval`（operator）；Evidence `ev-p090-association-graph`, `ev-p090-entropy-router`
- Paper `P054` · On the Limit of Language Models as Planning Formalizers；用途 `operator`；路线 `q003:paper_card_fts` #3；Card `paper-p054`（paper）；Evidence `ev-p054-complete-pddl-formalizer`, `ev-p054-model-conditional-advantage`, `ev-p054-natural-language-implicit-predicate-failure`, `ev-p054-plan-validation-boundary`
- Paper `P003` · Language Agent Tree Search Unifies Reasoning, Acting, and Planning in Language Models；用途 `operator`；路线 `q003:passage_hybrid` #1；Passage `P003:p0006:s0001`
- Paper `P081` · Self-Consistency Improves Chain of Thought Reasoning in Language Models；用途 `operator`；路线 `q003:failure_card_fts` #2；Card `failure-interactive-gains-collapse-against-independent-sampling`（failure）；Evidence `ev-p081-fixed-answer-space-boundary`, `ev-p081-forty-sample-baseline`, `ev-p081-independent-path-majority-aggregation`
- Paper `P065` · Group-in-Group Policy Optimization for LLM Agent Training；用途 `prior`；路线 `q004:paper_card_fts` #2；Card `paper-p065`（paper）；Evidence `ev-p065-anchor-state-credit`, `ev-p065-state-recurrence-boundary`
- Paper `P059` · Multi-Agent Collaboration via Evolving Orchestration；用途 `prior`；路线 `q004:operator_card_fts` #3；Card `operator-state-conditioned-agent-activation`（operator）；Evidence `ev-p059-compact-cyclic-topology`, `ev-p059-state-conditioned-orchestrator`
- Paper `P089` · ToolDreamer: Instilling LLM Reasoning Into Tool Retrievers；用途 `prior`；路线 `q004:failure_card_fts` #3；Card `failure-forced-hypothetical-tool-alignment`（failure）；Evidence `ev-p089-forced-alignment-proxy`, `ev-p089-hungarian-alignment`, `ev-p089-retrieval-only-metrics`, `ev-p089-training-gold-count-hypothetical-tools`
- Paper `P012` · Reflexion: Language Agents with Verbal Reinforcement Learning；用途 `prior`；路线 `q004:passage_hybrid` #1；Passage `P012:p0004:s0001`
- Paper `P040` · From Confident Closing to Silent Failure: Characterizing False Success in LLM Agents；用途 `measurement`；路线 `q005:paper_card_fts` #2；Card `paper-p040`（paper）；Evidence `ev-p040-failure-core`
- Paper `P036` · tau-Knowledge: Evaluating Conversational Agents over Unstructured Knowledge；用途 `measurement`；路线 `q005:passage_hybrid` #1；Passage `P036:p0023:s0001`
- Paper `P039` · ToolFailBench: Diagnosing Tool-Use Failures in LLM Agents；用途 `measurement`；路线 `q005:failure_card_fts` #2；Card `failure-tool-use-metrics-collapse-distinct-errors`（failure）；Evidence `ev-p039-aggregate-score-masking`, `ev-p039-failure-core`
- Paper `P007` · tau-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains；用途 `measurement`；路线 `q005:operator_card_fts` #2；Card `operator-terminal-state-reliability-evaluation`（operator）；Evidence `ev-p007-terminal-state-evaluation`

- 代表项：20 / 去重 Paper：93

## 查询与路线覆盖

### q001 · problem

- 原始查询：`LLM agent episodic memory successful trajectory reuse negative transfer applicability preconditions validity domain`
- 规范化查询：`"LLM" OR "agent" OR "episodic" OR "memory" OR "successful" OR "trajectory" OR "reuse" OR "negative" OR "transfer" OR "applicability" OR "preconditions" OR "validity" OR "domain"`
- 路线 `paper_card_fts`：30 条；降级 false（无）
- 路线 `failure_card_fts`：30 条；降级 false（无）
- 路线 `passage_hybrid`：20 条；降级 false（无）
- 路线 `operator_card_fts`：30 条；降级 false（无）

### q002 · failure

- 原始查询：`semantically similar task different causal precondition retrieved experience plan failure overgeneralization stale skill`
- 规范化查询：`"semantically" OR "similar" OR "task" OR "different" OR "causal" OR "precondition" OR "retrieved" OR "experience" OR "plan" OR "failure" OR "overgeneralization" OR "stale" OR "skill"`
- 路线 `failure_card_fts`：30 条；降级 false（无）
- 路线 `passage_hybrid`：20 条；降级 false（无）
- 路线 `operator_card_fts`：30 条；降级 false（无）
- 路线 `paper_card_fts`：30 条；降级 false（无）

### q003 · operator

- 原始查询：`learn experience applicability predicate counterfactual boundary initiation set case based reasoning adaptation abstention`
- 规范化查询：`"learn" OR "experience" OR "applicability" OR "predicate" OR "counterfactual" OR "boundary" OR "initiation" OR "set" OR "case" OR "based" OR "reasoning" OR "adaptation" OR "abstention"`
- 路线 `operator_card_fts`：30 条；降级 false（无）
- 路线 `paper_card_fts`：30 条；降级 false（无）
- 路线 `passage_hybrid`：20 条；降级 false（无）
- 路线 `failure_card_fts`：30 条；降级 false（无）

### q004 · prior

- 原始查询：`agent memory trajectory retrieval state conditioned experience reuse precondition skill library option initiation set`
- 规范化查询：`"agent" OR "memory" OR "trajectory" OR "retrieval" OR "state" OR "conditioned" OR "experience" OR "reuse" OR "precondition" OR "skill" OR "library" OR "option" OR "initiation" OR "set"`
- 路线 `paper_card_fts`：30 条；降级 false（无）
- 路线 `operator_card_fts`：30 条；降级 false（无）
- 路线 `failure_card_fts`：30 条；降级 false（无）
- 路线 `passage_hybrid`：20 条；降级 false（无）

### q005 · measurement

- 原始查询：`paired task variants one critical precondition memory retrieval success negative transfer independent terminal state`
- 规范化查询：`"paired" OR "task" OR "variants" OR "one" OR "critical" OR "precondition" OR "memory" OR "retrieval" OR "success" OR "negative" OR "transfer" OR "independent" OR "terminal" OR "state"`
- 路线 `paper_card_fts`：30 条；降级 false（无）
- 路线 `passage_hybrid`：20 条；降级 false（无）
- 路线 `failure_card_fts`：30 条；降级 false（无）
- 路线 `operator_card_fts`：30 条；降级 false（无）

## 覆盖诊断

- 去重 Card：187
- 去重 Evidence：209
- 去重 Passage：76
- 命中 Paper：93
- 原始观测：550
- 带机械噪声标记的观测：0
