<!-- CRL_RESEARCH_SEARCH_META {"created_at_utc":"2026-08-15T15:53:43.363892Z","request_fingerprint_sha256":"72e859a118fed6478bc09d0c148a2751f9718b2b7f867ed761256dc062f7ae65","result_json_sha256":"23c15b6dbe7c13d4f1162e5cfda55b64335667ddfbeb0b707035c4c06128689d","search_id":"correlated_tool_evidence_map"} -->
# 研究检索导航

> 本报告仅展示查询路线、来源、命中定位与覆盖；所有科研判断由主研究者完成。

- 搜索标识：`correlated_tool_evidence_map`
- 生成时间（协调世界时）：`2026-08-15T15:53:43.363892Z`

## 紧凑研究地图

> 跨路线按 Paper 去重；每个查询路线至多选一个尚未出现的最高排名代表项。完整原始命中保留在 `result.json`。

- Paper `P025` · Unlocking the Power of Multi-Agent LLM for Reasoning: From Lazy Agents to Deliberation；用途 `problem`；路线 `q001:paper_card_fts` #1；Card `paper-p025`（paper）；Evidence `ev-p025-failure-core`
- Paper `P083` · TAMAS: Benchmarking Adversarial Risks in Multi-Agent LLM Systems；用途 `problem`；路线 `q001:failure_card_fts` #1；Card `failure-multi-agent-adversarial-coordination-spans-trust-surfaces`（failure）；Evidence `ev-p083-lightweight-defense-failure`, `ev-p083-simulated-tool-boundary`, `ev-p083-three-surface-adversarial-failure`
- Paper `P038` · AgentDojo: A Dynamic Environment to Evaluate Prompt Injection Attacks and Defenses for LLM Agents；用途 `problem`；路线 `q001:passage_hybrid` #1；Passage `P038:p0025:s0001`
- Paper `P037` · ToolSandbox: A Stateful, Conversational, Interactive Evaluation Benchmark for LLM Tool Use Capabilities；用途 `problem`；路线 `q001:operator_card_fts` #1；Card `operator-milestone-dag-trajectory-evaluation`（operator）；Evidence `ev-p037-evaluation-core`, `ev-p037-minefield-violation`
- Paper `P096` · VeriSimpl: Robust Optimization Modeling from Natural Language using Simplification-based Verification；用途 `failure`；路线 `q002:failure_card_fts` #1；Card `failure-generator-aligned-verification-passes-shared-misreads`（failure）；Evidence `ev-p096-shared-misinterpretation`, `ev-p096-simplification-inversion`
- Paper `P040` · From Confident Closing to Silent Failure: Characterizing False Success in LLM Agents；用途 `failure`；路线 `q002:passage_hybrid` #1；Passage `P040:p0010:s0003`
- Paper `P073` · Uncertainty Calibration for Tool-Using Language Agents；用途 `failure`；路线 `q002:operator_card_fts` #1；Card `operator-execution-supervised-prompt-trace-calibration`（operator）；Evidence `ev-p073-execution-supervised-probe`, `ev-p073-internal-confidence-misalignment`
- Paper `P056` · GPTSwarm: Language Agents as Optimizable Graphs；用途 `failure`；路线 `q002:paper_card_fts` #2；Card `paper-p056`（paper）；Evidence `ev-p056-dylan-cost-quality`, `ev-p056-graph-optimization`, `ev-p056-same-set-crosswords`
- Paper `P081` · Self-Consistency Improves Chain of Thought Reasoning in Language Models；用途 `operator`；路线 `q003:operator_card_fts` #1；Card `operator-fixed-budget-independent-path-aggregation`（operator）；Evidence `ev-p081-fixed-answer-space-boundary`, `ev-p081-forty-sample-baseline`, `ev-p081-independent-path-majority-aggregation`
- Paper `P048` · NaviAgent: Graph-Driven Bilevel Planning for Scalable Tool Orchestration；用途 `operator`；路线 `q003:paper_card_fts` #1；Card `paper-p048`（paper）；Evidence `ev-p048-operator-core`
- Paper `P044` · DEER: A Benchmark for Evaluating Deep Research Agents on Expert Report Generation；用途 `operator`；路线 `q003:passage_hybrid` #1；Passage `P044:p0039:s0001`
- Paper `P017` · Understanding the Information Propagation Effects of Communication Topologies in LLM-based Multi-Agent Systems；用途 `operator`；路线 `q003:failure_card_fts` #2；Card `failure-sparse-topology-suppresses-correct-insight`（failure）；Evidence `ev-p017-failure-core`
- Paper `P097` · ReLoop: Structured Modeling and Behavioral Verification for Reliable LLM-Based Optimization；用途 `prior`；路线 `q004:paper_card_fts` #1；Card `paper-p097`（paper）；Evidence `ev-p097-behavioral-perturbation`, `ev-p097-feasibility-gap`
- Paper `P016` · Why Do Multi-Agent LLM Systems Fail?；用途 `prior`；路线 `q004:operator_card_fts` #1；Card `operator-trace-failure-taxonomy`（operator）；Evidence `ev-p016-mast-taxonomy`
- Paper `P015` · Should we be going MAD? A Look at Multi-Agent Debate Strategies for LLMs；用途 `prior`；路线 `q004:failure_card_fts` #1；Card `failure-debate-cost-nondominance`（failure）；Evidence `ev-p015-debate-cost-nondominance`
- Paper `P046` · Solver-Aided Verification of Policy Compliance in Tool-Augmented LLM Agents；用途 `prior`；路线 `q004:passage_hybrid` #3；Passage `P046:p0005:s0002`
- Paper `P004` · TravelPlanner: A Benchmark for Real-World Planning with Language Agents；用途 `measurement`；路线 `q005:paper_card_fts` #1；Card `paper-p004`（paper）；Evidence `ev-p004-failure-core`
- Paper `P068` · DeepFact: Co-Evolving Benchmarks and Agents for Deep Research Factuality；用途 `measurement`；路线 `q005:passage_hybrid` #1；Passage `P068:p0016:s0001`
- Paper `P098` · Beyond Objective Equivalence: Constraint Injection for LLM-Based Optimization Modeling on Vehicle Routing Problems；用途 `measurement`；路线 `q005:failure_card_fts` #7；Card `failure-objective-equivalence-passes-nonbinding-errors`（failure）；Evidence `ev-p098-diff-leak-550`, `ev-p098-nonbinding-blindness`, `ev-p098-open-problem`
- Paper `P049` · Reinforced Agent: Inference-Time Feedback for Tool-Calling Agents；用途 `measurement`；路线 `q005:operator_card_fts` #3；Card `operator-bounded-preexecution-reviewer`（operator）；Evidence `ev-p049-bounded-review-loop`, `ev-p049-operator-core`

- 代表项：20 / 去重 Paper：71

## 查询与路线覆盖

### q001 · problem

- 原始查询：`LLM tool agents multiple tool corroboration correlated errors shared upstream provenance independence`
- 规范化查询：`"LLM" OR "tool" OR "agents" OR "multiple" OR "corroboration" OR "correlated" OR "errors" OR "shared" OR "upstream" OR "provenance" OR "independence"`
- 路线 `paper_card_fts`：14 条；降级 false（无）
- 路线 `failure_card_fts`：14 条；降级 false（无）
- 路线 `passage_hybrid`：20 条；降级 false（无）
- 路线 `operator_card_fts`：14 条；降级 false（无）

### q002 · failure

- 原始查询：`agents overcount agreeing tools same data source correlated failure false confidence`
- 规范化查询：`"agents" OR "overcount" OR "agreeing" OR "tools" OR "same" OR "data" OR "source" OR "correlated" OR "failure" OR "false" OR "confidence"`
- 路线 `failure_card_fts`：14 条；降级 false（无）
- 路线 `passage_hybrid`：20 条；降级 false（无）
- 路线 `operator_card_fts`：14 条；降级 false（无）
- 路线 `paper_card_fts`：14 条；降级 false（无）

### q003 · operator

- 原始查询：`provenance dependency graph independent verification source diversity evidence aggregation`
- 规范化查询：`"provenance" OR "dependency" OR "graph" OR "independent" OR "verification" OR "source" OR "diversity" OR "evidence" OR "aggregation"`
- 路线 `operator_card_fts`：14 条；降级 false（无）
- 路线 `paper_card_fts`：14 条；降级 false（无）
- 路线 `passage_hybrid`：20 条；降级 false（无）
- 路线 `failure_card_fts`：14 条；降级 false（无）

### q004 · prior

- 原始查询：`multi-tool verification source independence correlated tool errors LLM agent`
- 规范化查询：`"multi" OR "tool" OR "verification" OR "source" OR "independence" OR "correlated" OR "errors" OR "LLM" OR "agent"`
- 路线 `paper_card_fts`：14 条；降级 false（无）
- 路线 `operator_card_fts`：14 条；降级 false（无）
- 路线 `failure_card_fts`：14 条；降级 false（无）
- 路线 `passage_hybrid`：20 条；降级 false（无）

### q005 · measurement

- 原始查询：`effective independent sources agreement confidence tool agent benchmark`
- 规范化查询：`"effective" OR "independent" OR "sources" OR "agreement" OR "confidence" OR "tool" OR "agent" OR "benchmark"`
- 路线 `paper_card_fts`：14 条；降级 false（无）
- 路线 `passage_hybrid`：20 条；降级 false（无）
- 路线 `failure_card_fts`：14 条；降级 false（无）
- 路线 `operator_card_fts`：14 条；降级 false（无）

## 覆盖诊断

- 去重 Card：116
- 去重 Evidence：147
- 去重 Passage：84
- 命中 Paper：71
- 原始观测：310
- 带机械噪声标记的观测：0
