<!-- CRL_RESEARCH_SEARCH_META {"created_at_utc":"2026-08-16T09:08:28.865694Z","request_fingerprint_sha256":"2ddcd65cbacd49da504397c1ad3db708afd11088c6f936c042f5693760b503b7","result_json_sha256":"47d64d870da4c05727624fcb228414a34cae74a9c3a61be16b7109f72de41790","search_id":"typed-dataflow-binding-001"} -->
# 研究检索导航

> 本报告仅展示查询路线、来源、命中定位与覆盖；所有科研判断由主研究者完成。

- 搜索标识：`typed-dataflow-binding-001`
- 生成时间（协调世界时）：`2026-08-16T09:08:28.865694Z`

## 紧凑研究地图

> 跨路线按 Paper 去重；每个查询路线至多选一个尚未出现的最高排名代表项。完整原始命中保留在 `result.json`。

- Paper `P066` · The Berkeley Function Calling Leaderboard (BFCL): From Tool Use to Agentic Evaluation of Large Language Models；用途 `problem`；路线 `q001:paper_card_fts` #1；Card `paper-p066`（paper）；Evidence `ev-p066-multiturn-state-evaluation`, `ev-p066-single-to-stateful-gap`
- Paper `P084` · On the Robustness of Agentic Function Calling；用途 `problem`；路线 `q001:failure_card_fts` #1；Card `failure-semantically-related-toolkit-expansion`（failure）；Evidence `ev-p084-expanded-toolkit-controlled-setting`, `ev-p084-expanded-toolkit-table`, `ev-p084-generated-tool-single-dataset-boundary`, `ev-p084-related-toolkit-error-types`
- Paper `P039` · ToolFailBench: Diagnosing Tool-Use Failures in LLM Agents；用途 `problem`；路线 `q001:passage_hybrid` #1；Passage `P039:p0016:s0001`
- Paper `P030` · STALE: Can LLM Agents Know When Their Memories Are No Longer Valid?；用途 `problem`；路线 `q001:operator_card_fts` #1；Card `operator-write-side-state-adjudication`（operator）；Evidence `ev-p030-authorized-readout`, `ev-p030-failure-core`, `ev-p030-write-side-adjudication`
- Paper `P087` · Tools Are Under-Documented: Simple Document Expansion Boosts Tool Retrieval；用途 `operator`；路线 `q002:operator_card_fts` #1；Card `operator-grounded-structured-tool-document-expansion`（operator）；Evidence `ev-p087-fields-not-universally-beneficial`, `ev-p087-merge-and-semantic-judge`, `ev-p087-structured-query-independent-expansion`
- Paper `P041` · LLM Agents Already Know When to Call Tools - Even Without Reasoning；用途 `operator`；路线 `q002:paper_card_fts` #2；Card `paper-p041`（paper）；Evidence `ev-p041-operator-core`
- Paper `P099` · Verus-SpecGym: An Agentic Environment for Evaluating Specification Autoformalization；用途 `operator`；路线 `q002:passage_hybrid` #1；Passage `P099:p0007:s0003`
- Paper `P033` · Self-Refine: Iterative Refinement with Self-Feedback；用途 `operator`；路线 `q002:failure_card_fts` #1；Card `failure-iterative-refinement-corrupts-correct-output`（failure）；Evidence `ev-p033-operator-core`
- Paper `P060` · Unifying Inference-Time Planning Language Generation；用途 `prior`；路线 `q003:paper_card_fts` #1；Card `paper-p060`（paper）；Evidence `ev-p060-formal-ir-solver`, `ev-p060-ir-result-and-nl-failure`
- Paper `P048` · NaviAgent: Graph-Driven Bilevel Planning for Scalable Tool Orchestration；用途 `prior`；路线 `q003:operator_card_fts` #1；Card `operator-bilevel-graph-toolchain-planning`（operator）；Evidence `ev-p048-operator-core`
- Paper `P098` · Beyond Objective Equivalence: Constraint Injection for LLM-Based Optimization Modeling on Vehicle Routing Problems；用途 `prior`；路线 `q003:failure_card_fts` #2；Card `failure-objective-equivalence-passes-nonbinding-errors`（failure）；Evidence `ev-p098-diff-leak-550`, `ev-p098-nonbinding-blindness`, `ev-p098-open-problem`
- Paper `P006` · An LLM Compiler for Parallel Function Calling；用途 `prior`；路线 `q003:passage_hybrid` #1；Passage `P006:p0004:s0002`
- Paper `P078` · CRAFT: Customizing LLMs by Creating and Retrieving from Specialized Toolsets；用途 `measurement`；路线 `q004:paper_card_fts` #2；Card `paper-p078`（paper）；Evidence `ev-p078-baseline-fairness-boundary`, `ev-p078-generic-tool-and-baseline-boundary`, `ev-p078-multiview-tool-retrieval`, `ev-p078-toolset-construction-cost`, `ev-p078-validated-tool-creation-retrieval`
- Paper `P086` · Meta-Tool: Unleash Open-World Function Calling Capabilities of General-Purpose Large Language Models；用途 `measurement`；路线 `q004:passage_hybrid` #3；Passage `P086:p0004:s0001`
- Paper `P091` · Temporal Validity in Retrieval Memory: Eliminating Stale-Fact Errors for AI Agents over Evolving Knowledge；用途 `measurement`；路线 `q004:failure_card_fts` #2；Card `failure-cosine-cannot-separate-contradiction-from-duplicate`（failure）；Evidence `ev-p091-cosine-auroc`, `ev-p091-retain-fabrication`
- Paper `P037` · ToolSandbox: A Stateful, Conversational, Interactive Evaluation Benchmark for LLM Tool Use Capabilities；用途 `measurement`；路线 `q004:operator_card_fts` #3；Card `operator-milestone-dag-trajectory-evaluation`（operator）；Evidence `ev-p037-evaluation-core`, `ev-p037-minefield-violation`

- 代表项：16 / 去重 Paper：58

## 查询与路线覆盖

### q001 · problem

- 原始查询：`multi-step function calling propagates stale or incorrect intermediate values into later tool arguments`
- 规范化查询：`"multi" OR "step" OR "function" OR "calling" OR "propagates" OR "stale" OR "or" OR "incorrect" OR "intermediate" OR "values" OR "into" OR "later" OR "tool" OR "arguments"`
- 路线 `paper_card_fts`：12 条；降级 false（无）
- 路线 `failure_card_fts`：12 条；降级 false（无）
- 路线 `passage_hybrid`：24 条；降级 false（无）
- 路线 `operator_card_fts`：12 条；降级 false（无）

### q002 · operator

- 原始查询：`typed immutable output references runtime dataflow binding resolves tool call fields without language model copying values`
- 规范化查询：`"typed" OR "immutable" OR "output" OR "references" OR "runtime" OR "dataflow" OR "binding" OR "resolves" OR "tool" OR "call" OR "fields" OR "without" OR "language" OR "model" OR "copying" OR "values"`
- 路线 `operator_card_fts`：12 条；降级 false（无）
- 路线 `paper_card_fts`：12 条；降级 false（无）
- 路线 `passage_hybrid`：24 条；降级 false（无）
- 路线 `failure_card_fts`：12 条；降级 false（无）

### q003 · prior

- 原始查询：`tool calling variable references intermediate outputs dataflow graph symbolic handles parameter binding`
- 规范化查询：`"tool" OR "calling" OR "variable" OR "references" OR "intermediate" OR "outputs" OR "dataflow" OR "graph" OR "symbolic" OR "handles" OR "parameter" OR "binding"`
- 路线 `paper_card_fts`：12 条；降级 false（无）
- 路线 `operator_card_fts`：12 条；降级 false（无）
- 路线 `failure_card_fts`：12 条；降级 false（无）
- 路线 `passage_hybrid`：24 条；降级 false（无）

### q004 · measurement

- 原始查询：`control distractor same-name values stale updates type mismatch across multi-step executable function DAG`
- 规范化查询：`"control" OR "distractor" OR "same" OR "name" OR "values" OR "stale" OR "updates" OR "type" OR "mismatch" OR "across" OR "multi" OR "step" OR "executable" OR "function" OR "DAG"`
- 路线 `paper_card_fts`：12 条；降级 false（无）
- 路线 `passage_hybrid`：24 条；降级 false（无）
- 路线 `failure_card_fts`：12 条；降级 false（无）
- 路线 `operator_card_fts`：12 条；降级 false（无）

## 覆盖诊断

- 去重 Card：83
- 去重 Evidence：109
- 去重 Passage：82
- 命中 Paper：58
- 原始观测：240
- 带机械噪声标记的观测：2
