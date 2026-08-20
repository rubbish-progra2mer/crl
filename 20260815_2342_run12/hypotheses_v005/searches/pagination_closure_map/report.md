<!-- CRL_RESEARCH_SEARCH_META {"created_at_utc":"2026-08-16T06:15:51.116231Z","request_fingerprint_sha256":"616c4fe23267fb0205a356833f05f08d2464a4ad41706a998a1665e5a7b6a54b","result_json_sha256":"f800d3463e49f3d8420a501d24ea9990dccead92eaa145359f8c7a059f7d210b","search_id":"pagination_closure_map"} -->
# 研究检索导航

> 本报告仅展示查询路线、来源、命中定位与覆盖；所有科研判断由主研究者完成。

- 搜索标识：`pagination_closure_map`
- 生成时间（协调世界时）：`2026-08-16T06:15:51.116231Z`

## 紧凑研究地图

> 跨路线按 Paper 去重；每个查询路线至多选一个尚未出现的最高排名代表项。完整原始命中保留在 `result.json`。

- Paper `P001` · ReAct: Synergizing Reasoning and Acting in Language Models；用途 `problem`；路线 `q001:paper_card_fts` #1；Card `paper-react`（paper）；Evidence `ev-p001-react-interleaved`, `ev-p001-search-hallucination-boundary`
- Paper `P074` · ToolGate: Contract-Grounded and Verified Tool Execution for LLMs；用途 `problem`；路线 `q001:failure_card_fts` #1；Card `failure-incomplete-tool-contracts-false-verified-state`（failure）；Evidence `ev-p074-contract-state-commit`, `ev-p074-missing-schema-true-postcondition`
- Paper `P079` · Learning to Contextualize Web Pages for Enhanced Decision Making by LLM Agents；用途 `problem`；路线 `q001:passage_hybrid` #1；Passage `P079:p0018:s0001`
- Paper `P060` · Unifying Inference-Time Planning Language Generation；用途 `problem`；路线 `q001:operator_card_fts` #2；Card `operator-syntax-aligned-formal-ir-planning`（operator）；Evidence `ev-p060-formal-ir-solver`, `ev-p060-ir-result-and-nl-failure`
- Paper `P051` · Large Language Models Can Solve Real-World Planning Rigorously with Formal Verification Tools；用途 `failure`；路线 `q002:failure_card_fts` #2；Card `failure-solver-guarantee-stops-at-formalization`（failure）；Evidence `ev-p051-omitted-constraint-failure`, `ev-p051-solver-guarantee-boundary`
- Paper `P085` · Retrieval Models Aren't Tool-Savvy: Benchmarking Tool Retrieval for Large Language Models；用途 `failure`；路线 `q002:passage_hybrid` #1；Passage `P085:p0020:s0001`
- Paper `P088` · Non-negative Elastic Net Decoding for Information Retrieval；用途 `failure`；路线 `q002:operator_card_fts` #1；Card `operator-joint-nonnegative-residual-retrieval`（operator）；Evidence `ev-p088-joint-nonnegative-objective`, `ev-p088-relevant-set-size-signature`, `ev-p088-theory-deployment-scale-boundary`
- Paper `P005` · ToolLLM: Facilitating Large Language Models to Master 16000+ Real-world APIs；用途 `failure`；路线 `q002:paper_card_fts` #1；Card `paper-p005`（paper）；Evidence `ev-p005-operator-core`
- Paper `P087` · Tools Are Under-Documented: Simple Document Expansion Boosts Tool Retrieval；用途 `operator`；路线 `q003:operator_card_fts` #3；Card `operator-grounded-structured-tool-document-expansion`（operator）；Evidence `ev-p087-fields-not-universally-beneficial`, `ev-p087-merge-and-semantic-judge`, `ev-p087-structured-query-independent-expansion`
- Paper `P039` · ToolFailBench: Diagnosing Tool-Use Failures in LLM Agents；用途 `operator`；路线 `q003:paper_card_fts` #4；Card `paper-p039`（paper）；Evidence `ev-p039-failure-core`
- Paper `P048` · NaviAgent: Graph-Driven Bilevel Planning for Scalable Tool Orchestration；用途 `operator`；路线 `q003:passage_hybrid` #1；Passage `P048:p0029:s0001`
- Paper `P071` · Agentic Plan Caching: Test-Time Memory for Fast and Cost-Efficient LLM Agents；用途 `operator`；路线 `q003:failure_card_fts` #3；Card `failure-plan-cache-semantic-false-positives`（failure）；Evidence `ev-p071-cache-false-positive-boundary`, `ev-p071-plan-template-reuse`
- Paper `P037` · ToolSandbox: A Stateful, Conversational, Interactive Evaluation Benchmark for LLM Tool Use Capabilities；用途 `prior`；路线 `q004:paper_card_fts` #1；Card `paper-p037`（paper）；Evidence `ev-p037-evaluation-core`
- Paper `P078` · CRAFT: Customizing LLMs by Creating and Retrieving from Specialized Toolsets；用途 `prior`；路线 `q004:operator_card_fts` #1；Card `operator-validated-specialized-tool-creation-retrieval`（operator）；Evidence `ev-p078-baseline-fairness-boundary`, `ev-p078-generic-tool-and-baseline-boundary`, `ev-p078-multiview-tool-retrieval`, `ev-p078-toolset-construction-cost`, `ev-p078-validated-tool-creation-retrieval`
- Paper `P082` · Toolformer: Language Models Can Teach Themselves to Use Tools；用途 `prior`；路线 `q004:failure_card_fts` #1；Card `failure-likelihood-utility-does-not-guarantee-agent-utility`（failure）；Evidence `ev-p082-chaining-cost-sparsity-boundary`, `ev-p082-future-token-loss-filtered-calls`, `ev-p082-top-k-single-call-boundary`
- Paper `P041` · LLM Agents Already Know When to Call Tools - Even Without Reasoning；用途 `prior`；路线 `q004:passage_hybrid` #5；Passage `P041:p0009:s0002`
- Paper `P021` · In-the-Flow Agentic System Optimization for Effective Planning and Tool Use；用途 `measurement`；路线 `q005:paper_card_fts` #1；Card `paper-p021`（paper）；Evidence `ev-p021-operator-core`
- Paper `P019` · STeCa: Step-level Trajectory Calibration for LLM Agent Learning；用途 `measurement`；路线 `q005:passage_hybrid` #1；Passage `P019:p0013:s0001`
- Paper `P056` · GPTSwarm: Language Agents as Optimizable Graphs；用途 `measurement`；路线 `q005:failure_card_fts` #1；Card `failure-same-set-agent-graph-evaluation`（failure）；Evidence `ev-p056-graph-optimization`, `ev-p056-same-set-crosswords`
- Paper `P073` · Uncertainty Calibration for Tool-Using Language Agents；用途 `measurement`；路线 `q005:operator_card_fts` #3；Card `operator-execution-supervised-prompt-trace-calibration`（operator）；Evidence `ev-p073-execution-supervised-probe`, `ev-p073-internal-confidence-misalignment`

- 代表项：20 / 去重 Paper：90

## 查询与路线覆盖

### q001 · problem

- 原始查询：`LLM tool agent pagination cursor has_more list search incomplete result absence`
- 规范化查询：`"LLM" OR "tool" OR "agent" OR "pagination" OR "cursor" OR "has_more" OR "list" OR "search" OR "incomplete" OR "result" OR "absence"`
- 路线 `paper_card_fts`：15 条；降级 false（无）
- 路线 `failure_card_fts`：15 条；降级 false（无）
- 路线 `passage_hybrid`：15 条；降级 false（无）
- 路线 `operator_card_fts`：15 条；降级 false（无）

### q002 · failure

- 原始查询：`agent stops after first page concludes item absent incomplete tool results pagination`
- 规范化查询：`"agent" OR "stops" OR "after" OR "first" OR "page" OR "concludes" OR "item" OR "absent" OR "incomplete" OR "tool" OR "results" OR "pagination"`
- 路线 `failure_card_fts`：15 条；降级 false（无）
- 路线 `passage_hybrid`：15 条；降级 false（无）
- 路线 `operator_card_fts`：15 条；降级 false（无）
- 路线 `paper_card_fts`：15 条；降级 false（无）

### q003 · operator

- 原始查询：`query completeness certificate cursor exhaustion negative result tool agent`
- 规范化查询：`"query" OR "completeness" OR "certificate" OR "cursor" OR "exhaustion" OR "negative" OR "result" OR "tool" OR "agent"`
- 路线 `operator_card_fts`：15 条；降级 false（无）
- 路线 `paper_card_fts`：15 条；降级 false（无）
- 路线 `passage_hybrid`：15 条；降级 false（无）
- 路线 `failure_card_fts`：15 条；降级 false（无）

### q004 · prior

- 原始查询：`benchmark LLM agent pagination API cursor multi page tool use`
- 规范化查询：`"benchmark" OR "LLM" OR "agent" OR "pagination" OR "API" OR "cursor" OR "multi" OR "page" OR "tool" OR "use"`
- 路线 `paper_card_fts`：15 条；降级 false（无）
- 路线 `operator_card_fts`：15 条；降级 false（无）
- 路线 `failure_card_fts`：15 条；降级 false（无）
- 路线 `passage_hybrid`：15 条；降级 false（无）

### q005 · measurement

- 原始查询：`metamorphic pagination boundary same dataset agent task outcome`
- 规范化查询：`"metamorphic" OR "pagination" OR "boundary" OR "same" OR "dataset" OR "agent" OR "task" OR "outcome"`
- 路线 `paper_card_fts`：15 条；降级 false（无）
- 路线 `passage_hybrid`：15 条；降级 false（无）
- 路线 `failure_card_fts`：15 条；降级 false（无）
- 路线 `operator_card_fts`：15 条；降级 false（无）

## 覆盖诊断

- 去重 Card：145
- 去重 Evidence：184
- 去重 Passage：68
- 命中 Paper：90
- 原始观测：300
- 带机械噪声标记的观测：0
