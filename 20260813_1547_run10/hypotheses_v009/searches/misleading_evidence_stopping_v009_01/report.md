<!-- CRL_RESEARCH_SEARCH_META {"created_at_utc":"2026-08-13T11:05:35.913143Z","request_fingerprint_sha256":"4ba6dc9f3db7d105a1f149e43b83b0a6e77aef2ce2d22ecae6f27957e6299791","result_json_sha256":"5a508cc4c6e02e152d452cb7b45de4975e8b9261e8cbbb995c8cefa07e30bc75","search_id":"misleading_evidence_stopping_v009_01"} -->
# 研究检索导航

> 本报告仅展示查询路线、来源、命中定位与覆盖；所有科研判断由主研究者完成。

- 搜索标识：`misleading_evidence_stopping_v009_01`
- 生成时间（协调世界时）：`2026-08-13T11:05:35.913143Z`

## 紧凑研究地图

> 跨路线按 Paper 去重；每个查询路线至多选一个尚未出现的最高排名代表项。完整原始命中保留在 `result.json`。

- Paper `P043` · DeepResearch Bench: A Comprehensive Benchmark for Deep Research Agents；用途 `problem`；路线 `q001:paper_card_fts` #1；Card `paper-p043`（paper）；Evidence `ev-p043-evaluation-core`
- Paper `P068` · DeepFact: Co-Evolving Benchmarks and Agents for Deep Research Factuality；用途 `problem`；路线 `q001:failure_card_fts` #1；Card `failure-one-shot-expert-gold-is-brittle`（failure）；Evidence `ev-p068-audit-then-score`, `ev-p068-one-shot-gold-brittle`
- Paper `P032` · CRITIC: Large Language Models Can Self-Correct with Tool-Interactive Critiquing；用途 `problem`；路线 `q001:passage_hybrid` #3；Passage `P032:p0025:s0001`
- Paper `P042` · LiveResearchBench: A Live Benchmark for User-Centric Deep Research in the Wild；用途 `problem`；路线 `q001:operator_card_fts` #1；Card `operator-decomposed-research-evidence-evaluation`（operator）；Evidence `ev-p042-evaluation-core`
- Paper `P074` · ToolGate: Contract-Grounded and Verified Tool Execution for LLMs；用途 `failure`；路线 `q002:failure_card_fts` #1；Card `failure-incomplete-tool-contracts-false-verified-state`（failure）；Evidence `ev-p074-contract-state-commit`, `ev-p074-missing-schema-true-postcondition`
- Paper `P022` · MOC: Multi-Order Communication in LLM-based Multi-Agent Systems；用途 `failure`；路线 `q002:passage_hybrid` #1；Passage `P022:p0004:s0002`
- Paper `P090` · From Single to Multi-Granularity: Toward Long-Term Memory Association and Selection of Conversational Agents；用途 `failure`；路线 `q002:operator_card_fts` #1；Card `operator-entropy-routed-multi-granularity-retrieval`（operator）；Evidence `ev-p090-association-graph`, `ev-p090-entropy-router`
- Paper `P040` · From Confident Closing to Silent Failure: Characterizing False Success in LLM Agents；用途 `failure`；路线 `q002:paper_card_fts` #1；Card `paper-p040`（paper）；Evidence `ev-p040-failure-core`
- Paper `P063` · A-Mem: Agentic Memory for LLM Agents；用途 `operator`；路线 `q003:operator_card_fts` #1；Card `operator-dynamic-linked-memory-evolution`（operator）；Evidence `ev-p063-dynamic-link-generation`, `ev-p063-neighbor-rewrite-action`, `ev-p063-retrieval-k-varies`
- Paper `P087` · Tools Are Under-Documented: Simple Document Expansion Boosts Tool Retrieval；用途 `operator`；路线 `q003:paper_card_fts` #1；Card `paper-p087`（paper）；Evidence `ev-p087-fields-not-universally-beneficial`, `ev-p087-merge-and-semantic-judge`, `ev-p087-structured-query-independent-expansion`
- Paper `P085` · Retrieval Models Aren't Tool-Savvy: Benchmarking Tool Retrieval for Large Language Models；用途 `operator`；路线 `q003:passage_hybrid` #2；Passage `P085:p0003:s0001`
- Paper `P018` · ExpeL: LLM Agents Are Experiential Learners；用途 `operator`；路线 `q003:failure_card_fts` #1；Card `failure-unfiltered-reflection-contamination`（failure）；Evidence `ev-p018-raw-reflection-contamination`
- Paper `P057` · Automated Design of Agentic Systems；用途 `prior`；路线 `q004:paper_card_fts` #1；Card `paper-p057`（paper）；Evidence `ev-p057-archive-code-search`, `ev-p057-search-evaluation-budget`
- Paper `P048` · NaviAgent: Graph-Driven Bilevel Planning for Scalable Tool Orchestration；用途 `prior`；路线 `q004:operator_card_fts` #1；Card `operator-bilevel-graph-toolchain-planning`（operator）；Evidence `ev-p048-operator-core`
- Paper `P079` · Learning to Contextualize Web Pages for Enhanced Decision Making by LLM Agents；用途 `prior`；路线 `q004:failure_card_fts` #2；Card `failure-raw-observation-overload-hides-action-relevant-ui`（failure）；Evidence `ev-p079-action-conditioned-contextualization`, `ev-p079-ground-truth-action-retry`, `ev-p079-unseen-ui-boundary`
- Paper `P044` · DEER: A Benchmark for Evaluating Deep Research Agents on Expert Report Generation；用途 `prior`；路线 `q004:passage_hybrid` #3；Passage `P044:p0029:s0001`
- Paper `P081` · Self-Consistency Improves Chain of Thought Reasoning in Language Models；用途 `measurement`；路线 `q005:paper_card_fts` #1；Card `paper-p081`（paper）；Evidence `ev-p081-fixed-answer-space-boundary`, `ev-p081-forty-sample-baseline`, `ev-p081-independent-path-majority-aggregation`
- Paper `P080` · AutoSearch: Adaptive Search Depth for Efficient Agentic RAG via Reinforcement Learning；用途 `measurement`；路线 `q005:passage_hybrid` #1；Passage `P080:p0004:s0001`
- Paper `P092` · MemConflict: Evaluating Long-Term Memory Systems Under Memory Conflicts；用途 `measurement`；路线 `q005:failure_card_fts` #1；Card `failure-answer-accuracy-without-conflict-recognition`（failure）；Evidence `ev-p092-crs-low`, `ev-p092-whitebox-metrics`
- Paper `P093` · Collapse of Dense Retrievers: Short, Early, and Literal Biases Outranking Factual Evidence；用途 `measurement`；路线 `q005:operator_card_fts` #2；Card `operator-paired-single-factor-bias-decomposition`（operator）；Evidence `ev-p093-foil-collapse`, `ev-p093-paired-protocol`

- 代表项：20 / 去重 Paper：99

## 查询与路线覆盖

### q001 · problem

- 原始查询：`deep research agents prematurely stop after answer-shaped misleading evidence despite reachable record-level evidence`
- 规范化查询：`"deep" OR "research" OR "agents" OR "prematurely" OR "stop" OR "after" OR "answer" OR "shaped" OR "misleading" OR "evidence" OR "despite" OR "reachable" OR "record" OR "level"`
- 路线 `paper_card_fts`：99 条；降级 false（无）
- 路线 `failure_card_fts`：63 条；降级 false（无）
- 路线 `passage_hybrid`：1200 条；降级 false（无）
- 路线 `operator_card_fts`：66 条；降级 false（无）

### q002 · failure

- 原始查询：`verification inertia direct false summary shortens search and prevents completion of true multi-hop evidence routes`
- 规范化查询：`"verification" OR "inertia" OR "direct" OR "false" OR "summary" OR "shortens" OR "search" OR "and" OR "prevents" OR "completion" OR "of" OR "true" OR "multi" OR "hop" OR "evidence" OR "routes"`
- 路线 `failure_card_fts`：63 条；降级 false（无）
- 路线 `passage_hybrid`：1200 条；降级 false（无）
- 路线 `operator_card_fts`：66 条；降级 false（无）
- 路线 `paper_card_fts`：99 条；降级 false（无）

### q003 · operator

- 原始查询：`query-compiled evidence obligations proof-carrying stopping active counterevidence retrieval source-dependence-aware provenance cuts`
- 规范化查询：`"query" OR "compiled" OR "evidence" OR "obligations" OR "proof" OR "carrying" OR "stopping" OR "active" OR "counterevidence" OR "retrieval" OR "source" OR "dependence" OR "aware" OR "provenance" OR "cuts"`
- 路线 `operator_card_fts`：66 条；降级 false（无）
- 路线 `paper_card_fts`：99 条；降级 false（无）
- 路线 `passage_hybrid`：1200 条；降级 false（无）
- 路线 `failure_card_fts`：63 条；降级 false（无）

### q004 · prior

- 原始查询：`Argus evidence graph CaRR complete evidence chains GAVEL evidence contract CounterRefine answer-conditioned counterevidence FIRE CoVe truth discovery source dependence`
- 规范化查询：`"Argus" OR "evidence" OR "graph" OR "CaRR" OR "complete" OR "chains" OR "GAVEL" OR "contract" OR "CounterRefine" OR "answer" OR "conditioned" OR "counterevidence" OR "FIRE" OR "CoVe" OR "truth" OR "discovery" OR "source" OR "dependence"`
- 路线 `paper_card_fts`：99 条；降级 false（无）
- 路线 `operator_card_fts`：66 条；降级 false（无）
- 路线 `failure_card_fts`：63 条；降级 false（无）
- 路线 `passage_hybrid`：1200 条；降级 false（无）

### q005 · measurement

- 原始查询：`clean-noisy paired intervention conditional deference complete route retrieval accuracy abstention search cost independent terminal answer`
- 规范化查询：`"clean" OR "noisy" OR "paired" OR "intervention" OR "conditional" OR "deference" OR "complete" OR "route" OR "retrieval" OR "accuracy" OR "abstention" OR "search" OR "cost" OR "independent" OR "terminal" OR "answer"`
- 路线 `paper_card_fts`：99 条；降级 false（无）
- 路线 `passage_hybrid`：1200 条；降级 false（无）
- 路线 `failure_card_fts`：63 条；降级 false（无）
- 路线 `operator_card_fts`：66 条；降级 false（无）

## 覆盖诊断

- 去重 Card：228
- 去重 Evidence：224
- 去重 Passage：2685
- 命中 Paper：99
- 原始观测：7140
- 带机械噪声标记的观测：374
