<!-- CRL_RESEARCH_SEARCH_META {"created_at_utc":"2026-08-16T07:36:51.435516Z","request_fingerprint_sha256":"ac207a304acc426855892a23dbe7067b324ff20467efe99c44351904ebff9140","result_json_sha256":"b9557355191a473c1194b96365dc8bfdac5fec05285c4976904d2763081bb652","search_id":"parallel_result_binding_map"} -->
# 研究检索导航

> 本报告仅展示查询路线、来源、命中定位与覆盖；所有科研判断由主研究者完成。

- 搜索标识：`parallel_result_binding_map`
- 生成时间（协调世界时）：`2026-08-16T07:36:51.435516Z`

## 紧凑研究地图

> 跨路线按 Paper 去重；每个查询路线至多选一个尚未出现的最高排名代表项。完整原始命中保留在 `result.json`。

- Paper `P006` · An LLM Compiler for Parallel Function Calling；用途 `problem`；路线 `q001:paper_card_fts` #1；Card `paper-llmcompiler`（paper）；Evidence `ev-p006-dependency-dag-dispatch`, `ev-p006-shared-prompt-comparison-boundary`, `ev-p006-token-cost-accounting`
- Paper `P039` · ToolFailBench: Diagnosing Tool-Use Failures in LLM Agents；用途 `problem`；路线 `q001:failure_card_fts` #1；Card `failure-tool-use-metrics-collapse-distinct-errors`（failure）；Evidence `ev-p039-aggregate-score-masking`, `ev-p039-failure-core`
- Paper `P066` · The Berkeley Function Calling Leaderboard (BFCL): From Tool Use to Agentic Evaluation of Large Language Models；用途 `problem`；路线 `q001:passage_hybrid` #1；Passage `P066:p0007:s0002`
- Paper `P074` · ToolGate: Contract-Grounded and Verified Tool Execution for LLMs；用途 `problem`；路线 `q001:operator_card_fts` #1；Card `operator-contract-gated-tool-state-commit`（operator）；Evidence `ev-p074-contract-state-commit`, `ev-p074-missing-schema-true-postcondition`
- Paper `P033` · Self-Refine: Iterative Refinement with Self-Feedback；用途 `failure`；路线 `q002:failure_card_fts` #1；Card `failure-iterative-refinement-corrupts-correct-output`（failure）；Evidence `ev-p033-operator-core`
- Paper `P035` · Holistic Agent Leaderboard: The Missing Infrastructure for AI Agent Evaluation；用途 `failure`；路线 `q002:passage_hybrid` #3；Passage `P035:p0019:s0001`
- Paper `P060` · Unifying Inference-Time Planning Language Generation；用途 `failure`；路线 `q002:operator_card_fts` #1；Card `operator-syntax-aligned-formal-ir-planning`（operator）；Evidence `ev-p060-formal-ir-solver`, `ev-p060-ir-result-and-nl-failure`
- Paper `P034` · RefineBench: Evaluating Refinement Capability of Language Models via Checklists；用途 `failure`；路线 `q002:paper_card_fts` #1；Card `paper-p034`（paper）；Evidence `ev-p034-failure-core`
- Paper `P027` · Verified Critical Step Optimization for LLM Agents；用途 `operator`；路线 `q003:operator_card_fts` #1；Card `operator-verified-single-branch-repair`（operator）；Evidence `ev-p027-operator-core`
- Paper `P032` · CRITIC: Large Language Models Can Self-Correct with Tool-Interactive Critiquing；用途 `operator`；路线 `q003:paper_card_fts` #1；Card `paper-p032`（paper）；Evidence `ev-p032-operator-core`
- Paper `P047` · tau2-Bench: Evaluating Conversational Agents in a Dual-Control Environment；用途 `operator`；路线 `q003:passage_hybrid` #1；Passage `P047:p0024:s0001`
- Paper `P017` · Understanding the Information Propagation Effects of Communication Topologies in LLM-based Multi-Agent Systems；用途 `operator`；路线 `q003:failure_card_fts` #2；Card `failure-sparse-topology-suppresses-correct-insight`（failure）；Evidence `ev-p017-failure-core`
- Paper `P084` · On the Robustness of Agentic Function Calling；用途 `prior`；路线 `q004:paper_card_fts` #3；Card `paper-p084`（paper）；Evidence `ev-p084-expanded-toolkit-controlled-setting`, `ev-p084-expanded-toolkit-table`, `ev-p084-generated-tool-single-dataset-boundary`, `ev-p084-related-toolkit-error-types`
- Paper `P090` · From Single to Multi-Granularity: Toward Long-Term Memory Association and Selection of Conversational Agents；用途 `prior`；路线 `q004:operator_card_fts` #1；Card `operator-entropy-routed-multi-granularity-retrieval`（operator）；Evidence `ev-p090-association-graph`, `ev-p090-entropy-router`
- Paper `P007` · tau-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains；用途 `prior`；路线 `q004:failure_card_fts` #4；Card `failure-repeat-run-reliability-collapse`（failure）；Evidence `ev-p007-repeat-reliability-collapse`
- Paper `P049` · Reinforced Agent: Inference-Time Feedback for Tool-Calling Agents；用途 `prior`；路线 `q004:passage_hybrid` #2；Passage `P049:p0003:s0001`
- Paper `P053` · Language Models as Higher-Order Planning Formalizers；用途 `measurement`；路线 `q005:paper_card_fts` #1；Card `paper-p053`（paper）；Evidence `ev-p053-higher-order-generator`, `ev-p053-parser-evaluation-boundary`, `ev-p053-pattern-review-confound`, `ev-p053-python-to-pddl-pipeline`
- Paper `P098` · Beyond Objective Equivalence: Constraint Injection for LLM-Based Optimization Modeling on Vehicle Routing Problems；用途 `measurement`；路线 `q005:passage_hybrid` #1；Passage `P098:p0026:s0001`
- Paper `P069` · Tool Preferences in Agentic LLMs are Unreliable；用途 `measurement`；路线 `q005:failure_card_fts` #3；Card `failure-tool-description-and-order-bias`（failure）；Evidence `ev-p069-description-induced-preference`, `ev-p069-identical-tool-order-bias`
- Paper `P046` · Solver-Aided Verification of Policy Compliance in Tool-Augmented LLM Agents；用途 `measurement`；路线 `q005:operator_card_fts` #1；Card `operator-smt-preexecution-policy-guard`（operator）；Evidence `ev-p046-operator-core`

- 代表项：20 / 去重 Paper：67

## 查询与路线覆盖

### q001 · problem

- 原始查询：`parallel tool calls result binding call id arrival order permutation invariance`
- 规范化查询：`"parallel" OR "tool" OR "calls" OR "result" OR "binding" OR "call" OR "id" OR "arrival" OR "order" OR "permutation" OR "invariance"`
- 路线 `paper_card_fts`：12 条；降级 false（无）
- 路线 `failure_card_fts`：12 条；降级 false（无）
- 路线 `passage_hybrid`：24 条；降级 false（无）
- 路线 `operator_card_fts`：12 条；降级 false（无）

### q002 · failure

- 原始查询：`correct call identifier but reordered tool result silently misassociated by position`
- 规范化查询：`"correct" OR "call" OR "identifier" OR "but" OR "reordered" OR "tool" OR "result" OR "silently" OR "misassociated" OR "by" OR "position"`
- 路线 `failure_card_fts`：12 条；降级 false（无）
- 路线 `passage_hybrid`：24 条；降级 false（无）
- 路线 `operator_card_fts`：12 条；降级 false（无）
- 路线 `paper_card_fts`：12 条；降级 false（无）

### q003 · operator

- 原始查询：`unique call id validate canonicalize original order self identifying result envelope`
- 规范化查询：`"unique" OR "call" OR "id" OR "validate" OR "canonicalize" OR "original" OR "order" OR "self" OR "identifying" OR "result" OR "envelope"`
- 路线 `operator_card_fts`：12 条；降级 false（无）
- 路线 `paper_card_fts`：12 条；降级 false（无）
- 路线 `passage_hybrid`：24 条；降级 false（无）
- 路线 `failure_card_fts`：12 条；降级 false（无）

### q004 · prior

- 原始查询：`AsyncFC BFCL AgentCheck parallel function calling future identifier result association execution order`
- 规范化查询：`"AsyncFC" OR "BFCL" OR "AgentCheck" OR "parallel" OR "function" OR "calling" OR "future" OR "identifier" OR "result" OR "association" OR "execution" OR "order"`
- 路线 `paper_card_fts`：12 条；降级 false（无）
- 路线 `operator_card_fts`：12 条；降级 false（无）
- 路线 `failure_card_fts`：12 条；降级 false（无）
- 路线 `passage_hybrid`：24 条；降级 false（无）

### q005 · measurement

- 原始查询：`factorial call id order conflict payload self identification same tool repeated entity value mapping`
- 规范化查询：`"factorial" OR "call" OR "id" OR "order" OR "conflict" OR "payload" OR "self" OR "identification" OR "same" OR "tool" OR "repeated" OR "entity" OR "value" OR "mapping"`
- 路线 `paper_card_fts`：12 条；降级 false（无）
- 路线 `passage_hybrid`：24 条；降级 false（无）
- 路线 `failure_card_fts`：12 条；降级 false（无）
- 路线 `operator_card_fts`：12 条；降级 false（无）

## 覆盖诊断

- 去重 Card：87
- 去重 Evidence：128
- 去重 Passage：87
- 命中 Paper：67
- 原始观测：300
- 带机械噪声标记的观测：2
