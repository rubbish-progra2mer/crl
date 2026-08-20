<!-- CRL_RESEARCH_SEARCH_META {"created_at_utc":"2026-08-16T09:58:02.833885Z","request_fingerprint_sha256":"ec9aff42c172547a419a081f51b46702b62f94f356a3327476144f99544b8633","result_json_sha256":"86945ae23073222f1f395885393f3ec3be66f67fa76564454d0a4417d7f6c419","search_id":"lineage-normalized-consensus-001"} -->
# 研究检索导航

> 本报告仅展示查询路线、来源、命中定位与覆盖；所有科研判断由主研究者完成。

- 搜索标识：`lineage-normalized-consensus-001`
- 生成时间（协调世界时）：`2026-08-16T09:58:02.833885Z`

## 紧凑研究地图

> 跨路线按 Paper 去重；每个查询路线至多选一个尚未出现的最高排名代表项。完整原始命中保留在 `result.json`。

- Paper `P024` · Improving Factuality and Reasoning in Language Models through Multiagent Debate；用途 `problem`；路线 `q001:paper_card_fts` #1；Card `paper-p024`（paper）；Evidence `ev-p024-operator-core`
- Paper `P015` · Should we be going MAD? A Look at Multi-Agent Debate Strategies for LLMs；用途 `problem`；路线 `q001:failure_card_fts` #1；Card `failure-debate-cost-nondominance`（failure）；Evidence `ev-p015-debate-cost-nondominance`
- Paper `P083` · TAMAS: Benchmarking Adversarial Risks in Multi-Agent LLM Systems；用途 `problem`；路线 `q001:passage_hybrid` #1；Passage `P083:p0025:s0001`
- Paper `P023` · MasRouter: Learning to Route LLMs for Multi-Agent Systems；用途 `problem`；路线 `q001:operator_card_fts` #1；Card `operator-cascaded-multiagent-meta-routing`（operator）；Evidence `ev-p023-cascaded-routing-core`, `ev-p023-operator-core`
- Paper `P017` · Understanding the Information Propagation Effects of Communication Topologies in LLM-based Multi-Agent Systems；用途 `failure`；路线 `q002:failure_card_fts` #1；Card `failure-sparse-topology-suppresses-correct-insight`（failure）；Evidence `ev-p017-failure-core`
- Paper `P016` · Why Do Multi-Agent LLM Systems Fail?；用途 `failure`；路线 `q002:passage_hybrid` #5；Passage `P016:p0033:s0001`
- Paper `P018` · ExpeL: LLM Agents Are Experiential Learners；用途 `failure`；路线 `q002:operator_card_fts` #1；Card `operator-experience-insight-update`（operator）；Evidence `ev-p018-insight-update-operations`
- Paper `P022` · MOC: Multi-Order Communication in LLM-based Multi-Agent Systems；用途 `failure`；路线 `q002:paper_card_fts` #3；Card `paper-p022`（paper）；Evidence `ev-p022-operator-core`
- Paper `P081` · Self-Consistency Improves Chain of Thought Reasoning in Language Models；用途 `operator`；路线 `q003:operator_card_fts` #1；Card `operator-fixed-budget-independent-path-aggregation`（operator）；Evidence `ev-p081-fixed-answer-space-boundary`, `ev-p081-forty-sample-baseline`, `ev-p081-independent-path-majority-aggregation`
- Paper `P087` · Tools Are Under-Documented: Simple Document Expansion Boosts Tool Retrieval；用途 `operator`；路线 `q003:paper_card_fts` #1；Card `paper-p087`（paper）；Evidence `ev-p087-fields-not-universally-beneficial`, `ev-p087-merge-and-semantic-judge`, `ev-p087-structured-query-independent-expansion`
- Paper `P044` · DEER: A Benchmark for Evaluating Deep Research Agents on Expert Report Generation；用途 `operator`；路线 `q003:passage_hybrid` #1；Passage `P044:p0039:s0001`
- Paper `P040` · From Confident Closing to Silent Failure: Characterizing False Success in LLM Agents；用途 `operator`；路线 `q003:failure_card_fts` #2；Card `failure-confident-completion-without-state-success`（failure）；Evidence `ev-p040-failure-core`
- Paper `P053` · Language Models as Higher-Order Planning Formalizers；用途 `prior`；路线 `q004:paper_card_fts` #3；Card `paper-p053`（paper）；Evidence `ev-p053-higher-order-generator`, `ev-p053-parser-evaluation-boundary`, `ev-p053-pattern-review-confound`, `ev-p053-python-to-pddl-pipeline`
- Paper `P046` · Solver-Aided Verification of Policy Compliance in Tool-Augmented LLM Agents；用途 `prior`；路线 `q004:operator_card_fts` #3；Card `operator-smt-preexecution-policy-guard`（operator）；Evidence `ev-p046-operator-core`
- Paper `P069` · Tool Preferences in Agentic LLMs are Unreliable；用途 `prior`；路线 `q004:failure_card_fts` #5；Card `failure-tool-description-and-order-bias`（failure）；Evidence `ev-p069-description-induced-preference`, `ev-p069-identical-tool-order-bias`
- Paper `P068` · DeepFact: Co-Evolving Benchmarks and Agents for Deep Research Factuality；用途 `prior`；路线 `q004:passage_hybrid` #3；Passage `P068:p0005:s0001`
- Paper `P071` · Agentic Plan Caching: Test-Time Memory for Fast and Cost-Efficient LLM Agents；用途 `measurement`；路线 `q005:paper_card_fts` #5；Card `paper-p071`（paper）；Evidence `ev-p071-cache-false-positive-boundary`, `ev-p071-plan-template-reuse`
- Paper `P042` · LiveResearchBench: A Live Benchmark for User-Centric Deep Research in the Wild；用途 `measurement`；路线 `q005:passage_hybrid` #18；Passage `P042:p0010:s0001`
- Paper `P074` · ToolGate: Contract-Grounded and Verified Tool Execution for LLMs；用途 `measurement`；路线 `q005:failure_card_fts` #2；Card `failure-incomplete-tool-contracts-false-verified-state`（failure）；Evidence `ev-p074-contract-state-commit`, `ev-p074-missing-schema-true-postcondition`
- Paper `P097` · ReLoop: Structured Modeling and Behavioral Verification for Reliable LLM-Based Optimization；用途 `measurement`；路线 `q005:operator_card_fts` #2；Card `operator-behavioral-perturbation-existence-test`（operator）；Evidence `ev-p097-behavioral-perturbation`, `ev-p097-feasibility-gap`

- 代表项：20 / 去重 Paper：90

## 查询与路线覆盖

### q001 · problem

- 原始查询：`multi-agent distributed evidence misinformation cascade repeated relaying correlated consensus`
- 规范化查询：`"multi" OR "agent" OR "distributed" OR "evidence" OR "misinformation" OR "cascade" OR "repeated" OR "relaying" OR "correlated" OR "consensus"`
- 路线 `paper_card_fts`：24 条；降级 false（无）
- 路线 `failure_card_fts`：24 条；降级 false（无）
- 路线 `passage_hybrid`：24 条；降级 false（无）
- 路线 `operator_card_fts`：24 条；降级 false（无）

### q002 · failure

- 原始查询：`sparse topology suppresses correct insight debate conformity correlated errors copied testimony`
- 规范化查询：`"sparse" OR "topology" OR "suppresses" OR "correct" OR "insight" OR "debate" OR "conformity" OR "correlated" OR "errors" OR "copied" OR "testimony"`
- 路线 `failure_card_fts`：17 条；降级 false（无）
- 路线 `passage_hybrid`：24 条；降级 false（无）
- 路线 `operator_card_fts`：15 条；降级 false（无）
- 路线 `paper_card_fts`：22 条；降级 false（无）

### q003 · operator

- 原始查询：`provenance source lineage independent evidence aggregation claim routing`
- 规范化查询：`"provenance" OR "source" OR "lineage" OR "independent" OR "evidence" OR "aggregation" OR "claim" OR "routing"`
- 路线 `operator_card_fts`：24 条；降级 false（无）
- 路线 `paper_card_fts`：24 条；降级 false（无）
- 路线 `passage_hybrid`：24 条；降级 false（无）
- 路线 `failure_card_fts`：24 条；降级 false（无）

### q004 · prior

- 原始查询：`source-aware higher-order message exposure provenance guard consensus anti-conformity voting`
- 规范化查询：`"source" OR "aware" OR "higher" OR "order" OR "message" OR "exposure" OR "provenance" OR "guard" OR "consensus" OR "anti" OR "conformity" OR "voting"`
- 路线 `paper_card_fts`：24 条；降级 false（无）
- 路线 `operator_card_fts`：24 条；降级 false（无）
- 路线 `failure_card_fts`：11 条；降级 false（无）
- 路线 `passage_hybrid`：24 条；降级 false（无）

### q005 · measurement

- 原始查询：`truth recovery false consensus evidence root propagation unique source coverage communication cost`
- 规范化查询：`"truth" OR "recovery" OR "false" OR "consensus" OR "evidence" OR "root" OR "propagation" OR "unique" OR "source" OR "coverage" OR "communication" OR "cost"`
- 路线 `paper_card_fts`：24 条；降级 false（无）
- 路线 `passage_hybrid`：24 条；降级 false（无）
- 路线 `failure_card_fts`：24 条；降级 false（无）
- 路线 `operator_card_fts`：24 条；降级 false（无）

## 覆盖诊断

- 去重 Card：168
- 去重 Evidence：202
- 去重 Passage：77
- 命中 Paper：90
- 原始观测：449
- 带机械噪声标记的观测：3
