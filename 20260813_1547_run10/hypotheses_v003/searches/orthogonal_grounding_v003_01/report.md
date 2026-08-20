<!-- CRL_RESEARCH_SEARCH_META {"created_at_utc":"2026-08-13T09:34:55.844252Z","request_fingerprint_sha256":"bde4667826b904a9e5b4563d2a2ff78cfe36b73762b82ad5931f57114dd3c33e","result_json_sha256":"628837b1c20ead630e3753c213f7e10d9c6744d25869e8e1f6432b0b119a511d","search_id":"orthogonal_grounding_v003_01"} -->
# 研究检索导航

> 本报告仅展示查询路线、来源、命中定位与覆盖；所有科研判断由主研究者完成。

- 搜索标识：`orthogonal_grounding_v003_01`
- 生成时间（协调世界时）：`2026-08-13T09:34:55.844252Z`

## 紧凑研究地图

> 跨路线按 Paper 去重；每个查询路线至多选一个尚未出现的最高排名代表项。完整原始命中保留在 `result.json`。

- Paper `P098` · Beyond Objective Equivalence: Constraint Injection for LLM-Based Optimization Modeling on Vehicle Routing Problems；用途 `failure`；路线 `q001:failure_card_fts` #1；Card `failure-objective-equivalence-passes-nonbinding-errors`（failure）；Evidence `ev-p098-diff-leak-550`, `ev-p098-nonbinding-blindness`, `ev-p098-open-problem`
- Paper `P072` · Structured Uncertainty guided Clarification for LLM Agents；用途 `failure`；路线 `q001:passage_hybrid` #1；Passage `P072:p0005:s0001`
- Paper `P030` · STALE: Can LLM Agents Know When Their Memories Are No Longer Valid?；用途 `failure`；路线 `q001:operator_card_fts` #1；Card `operator-write-side-state-adjudication`（operator）；Evidence `ev-p030-authorized-readout`, `ev-p030-failure-core`, `ev-p030-write-side-adjudication`
- Paper `P001` · ReAct: Synergizing Reasoning and Acting in Language Models；用途 `failure`；路线 `q001:paper_card_fts` #2；Card `paper-react`（paper）；Evidence `ev-p001-react-interleaved`, `ev-p001-search-hallucination-boundary`
- Paper `P039` · ToolFailBench: Diagnosing Tool-Use Failures in LLM Agents；用途 `problem`；路线 `q002:paper_card_fts` #1；Card `paper-p039`（paper）；Evidence `ev-p039-failure-core`
- Paper `P079` · Learning to Contextualize Web Pages for Enhanced Decision Making by LLM Agents；用途 `problem`；路线 `q002:failure_card_fts` #3；Card `failure-raw-observation-overload-hides-action-relevant-ui`（failure）；Evidence `ev-p079-action-conditioned-contextualization`, `ev-p079-ground-truth-action-retry`, `ev-p079-unseen-ui-boundary`
- Paper `P048` · NaviAgent: Graph-Driven Bilevel Planning for Scalable Tool Orchestration；用途 `problem`；路线 `q002:passage_hybrid` #2；Passage `P048:p0003:s0005`
- Paper `P003` · Language Agent Tree Search Unifies Reasoning, Acting, and Planning in Language Models；用途 `problem`；路线 `q002:operator_card_fts` #1；Card `operator-feedback-backpropagated-tree-search`（operator）；Evidence `ev-p003-search-control-loop`
- Paper `P074` · ToolGate: Contract-Grounded and Verified Tool Execution for LLMs；用途 `operator`；路线 `q003:operator_card_fts` #2；Card `operator-contract-gated-tool-state-commit`（operator）；Evidence `ev-p074-contract-state-commit`, `ev-p074-missing-schema-true-postcondition`
- Paper `P088` · Non-negative Elastic Net Decoding for Information Retrieval；用途 `operator`；路线 `q003:paper_card_fts` #1；Card `paper-p088`（paper）；Evidence `ev-p088-joint-nonnegative-objective`, `ev-p088-relevant-set-size-signature`, `ev-p088-theory-deployment-scale-boundary`
- Paper `P060` · Unifying Inference-Time Planning Language Generation；用途 `operator`；路线 `q003:passage_hybrid` #1；Passage `P060:p0012:s0001`
- Paper `P084` · On the Robustness of Agentic Function Calling；用途 `operator`；路线 `q003:failure_card_fts` #3；Card `failure-semantically-related-toolkit-expansion`（failure）；Evidence `ev-p084-expanded-toolkit-controlled-setting`, `ev-p084-expanded-toolkit-table`, `ev-p084-generated-tool-single-dataset-boundary`, `ev-p084-related-toolkit-error-types`
- Paper `P065` · Group-in-Group Policy Optimization for LLM Agent Training；用途 `measurement`；路线 `q004:paper_card_fts` #2；Card `paper-p065`（paper）；Evidence `ev-p065-anchor-state-credit`, `ev-p065-state-recurrence-boundary`
- Paper `P049` · Reinforced Agent: Inference-Time Feedback for Tool-Calling Agents；用途 `measurement`；路线 `q004:passage_hybrid` #1；Passage `P049:p0011:s0001`
- Paper `P054` · On the Limit of Language Models as Planning Formalizers；用途 `measurement`；路线 `q004:failure_card_fts` #3；Card `failure-constraint-shift-breaks-formalization`（failure）；Evidence `ev-p054-natural-language-implicit-predicate-failure`
- Paper `P037` · ToolSandbox: A Stateful, Conversational, Interactive Evaluation Benchmark for LLM Tool Use Capabilities；用途 `measurement`；路线 `q004:operator_card_fts` #1；Card `operator-milestone-dag-trajectory-evaluation`（operator）；Evidence `ev-p037-evaluation-core`, `ev-p037-minefield-violation`
- Paper `P027` · Verified Critical Step Optimization for LLM Agents；用途 `prior`；路线 `q005:paper_card_fts` #1；Card `paper-p027`（paper）；Evidence `ev-p027-operator-core`
- Paper `P097` · ReLoop: Structured Modeling and Behavioral Verification for Reliable LLM-Based Optimization；用途 `prior`；路线 `q005:operator_card_fts` #2；Card `operator-behavioral-perturbation-existence-test`（operator）；Evidence `ev-p097-behavioral-perturbation`, `ev-p097-feasibility-gap`
- Paper `P083` · TAMAS: Benchmarking Adversarial Risks in Multi-Agent LLM Systems；用途 `prior`；路线 `q005:failure_card_fts` #1；Card `failure-multi-agent-adversarial-coordination-spans-trust-surfaces`（failure）；Evidence `ev-p083-lightweight-defense-failure`, `ev-p083-simulated-tool-boundary`, `ev-p083-three-surface-adversarial-failure`
- Paper `P035` · Holistic Agent Leaderboard: The Missing Infrastructure for AI Agent Evaluation；用途 `prior`；路线 `q005:passage_hybrid` #1；Passage `P035:p0018:s0001`

- 代表项：20 / 去重 Paper：89

## 查询与路线覆盖

### q001 · failure

- 原始查询：`tool agent copies wrong identifier from observation into downstream argument result ignored stale provenance referent binding`
- 规范化查询：`"tool" OR "agent" OR "copies" OR "wrong" OR "identifier" OR "from" OR "observation" OR "into" OR "downstream" OR "argument" OR "result" OR "ignored" OR "stale" OR "provenance" OR "referent" OR "binding"`
- 路线 `failure_card_fts`：30 条；降级 false（无）
- 路线 `passage_hybrid`：20 条；降级 false（无）
- 路线 `operator_card_fts`：30 条；降级 false（无）
- 路线 `paper_card_fts`：30 条；降级 false（无）

### q002 · problem

- 原始查询：`LLM agent tool result to action grounding entity binding exact value propagation observation use`
- 规范化查询：`"LLM" OR "agent" OR "tool" OR "result" OR "to" OR "action" OR "grounding" OR "entity" OR "binding" OR "exact" OR "value" OR "propagation" OR "observation" OR "use"`
- 路线 `paper_card_fts`：30 条；降级 false（无）
- 路线 `failure_card_fts`：30 条；降级 false（无）
- 路线 `passage_hybrid`：20 条；降级 false（无）
- 路线 `operator_card_fts`：30 条；降级 false（无）

### q003 · operator

- 原始查询：`causal sufficient statistic typed dataflow binding tool output downstream arguments constrained decoding`
- 规范化查询：`"causal" OR "sufficient" OR "statistic" OR "typed" OR "dataflow" OR "binding" OR "tool" OR "output" OR "downstream" OR "arguments" OR "constrained" OR "decoding"`
- 路线 `operator_card_fts`：30 条；降级 false（无）
- 路线 `paper_card_fts`：30 条；降级 false（无）
- 路线 `passage_hybrid`：20 条；降级 false（无）
- 路线 `failure_card_fts`：29 条；降级 false（无）

### q004 · measurement

- 原始查询：`paired tool response intervention downstream action argument correctness terminal state`
- 规范化查询：`"paired" OR "tool" OR "response" OR "intervention" OR "downstream" OR "action" OR "argument" OR "correctness" OR "terminal" OR "state"`
- 路线 `paper_card_fts`：30 条；降级 false（无）
- 路线 `passage_hybrid`：20 条；降级 false（无）
- 路线 `failure_card_fts`：30 条；降级 false（无）
- 路线 `operator_card_fts`：30 条；降级 false（无）

### q005 · prior

- 原始查询：`tool output grounding action binding provenance sensitivity counterfactual agent replay`
- 规范化查询：`"tool" OR "output" OR "grounding" OR "action" OR "binding" OR "provenance" OR "sensitivity" OR "counterfactual" OR "agent" OR "replay"`
- 路线 `paper_card_fts`：30 条；降级 false（无）
- 路线 `operator_card_fts`：30 条；降级 false（无）
- 路线 `failure_card_fts`：30 条；降级 false（无）
- 路线 `passage_hybrid`：20 条；降级 false（无）

## 覆盖诊断

- 去重 Card：165
- 去重 Evidence：190
- 去重 Passage：90
- 命中 Paper：89
- 原始观测：549
- 带机械噪声标记的观测：1
