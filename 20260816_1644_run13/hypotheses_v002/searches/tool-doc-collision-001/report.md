<!-- CRL_RESEARCH_SEARCH_META {"created_at_utc":"2026-08-16T09:04:36.359578Z","request_fingerprint_sha256":"cbb5ea42069f95274b64ad041cf4b7cf4cb8abc6aef8fd0bacd16d421cc72991","result_json_sha256":"30747f770ef69f74eeb9fee68eb0808440a07f3932fc2980c4b4af344f90ba78","search_id":"tool-doc-collision-001"} -->
# 研究检索导航

> 本报告仅展示查询路线、来源、命中定位与覆盖；所有科研判断由主研究者完成。

- 搜索标识：`tool-doc-collision-001`
- 生成时间（协调世界时）：`2026-08-16T09:04:36.359578Z`

## 紧凑研究地图

> 跨路线按 Paper 去重；每个查询路线至多选一个尚未出现的最高排名代表项。完整原始命中保留在 `result.json`。

- Paper `P087` · Tools Are Under-Documented: Simple Document Expansion Boosts Tool Retrieval；用途 `problem`；路线 `q001:paper_card_fts` #1；Card `paper-p087`（paper）；Evidence `ev-p087-fields-not-universally-beneficial`, `ev-p087-merge-and-semantic-judge`, `ev-p087-structured-query-independent-expansion`
- Paper `P084` · On the Robustness of Agentic Function Calling；用途 `problem`；路线 `q001:failure_card_fts` #1；Card `failure-semantically-related-toolkit-expansion`（failure）；Evidence `ev-p084-expanded-toolkit-controlled-setting`, `ev-p084-expanded-toolkit-table`, `ev-p084-generated-tool-single-dataset-boundary`, `ev-p084-related-toolkit-error-types`
- Paper `P048` · NaviAgent: Graph-Driven Bilevel Planning for Scalable Tool Orchestration；用途 `problem`；路线 `q001:passage_hybrid` #4；Passage `P048:p0002:s0002`
- Paper `P101` · Semantic Evaluation for Text-to-SQL with Distilled Test Suites；用途 `problem`；路线 `q001:operator_card_fts` #2；Card `operator-neighbor-distilled-test-suites`（operator）；Evidence `ev-p101-esm-fn-rate`, `ev-p101-neighbor-distillation`
- Paper `P089` · ToolDreamer: Instilling LLM Reasoning Into Tool Retrievers；用途 `operator`；路线 `q002:operator_card_fts` #1；Card `operator-hypothetical-tool-query-expansion`（operator）；Evidence `ev-p089-api-latency-boundary`, `ev-p089-forced-alignment-proxy`, `ev-p089-hungarian-alignment`, `ev-p089-overview-alignment-rrf`, `ev-p089-retrieval-only-metrics`, `ev-p089-training-gold-count-hypothetical-tools`
- Paper `P041` · LLM Agents Already Know When to Call Tools - Even Without Reasoning；用途 `operator`；路线 `q002:paper_card_fts` #1；Card `paper-p041`（paper）；Evidence `ev-p041-operator-core`
- Paper `P086` · Meta-Tool: Unleash Open-World Function Calling Capabilities of General-Purpose Large Language Models；用途 `operator`；路线 `q002:passage_hybrid` #2；Passage `P086:p0004:s0001`
- Paper `P074` · ToolGate: Contract-Grounded and Verified Tool Execution for LLMs；用途 `operator`；路线 `q002:failure_card_fts` #1；Card `failure-incomplete-tool-contracts-false-verified-state`（failure）；Evidence `ev-p074-contract-state-commit`, `ev-p074-missing-schema-true-postcondition`
- Paper `P085` · Retrieval Models Aren't Tool-Savvy: Benchmarking Tool Retrieval for Large Language Models；用途 `prior`；路线 `q003:paper_card_fts` #4；Card `paper-p085`（paper）；Evidence `ev-p085-large-corpus-scale`, `ev-p085-non-exhaustive-label`, `ev-p085-retrieval-completeness-failure`
- Paper `P028` · Memory-R1: Enhancing Large Language Model Agents to Manage and Utilize Memories via Reinforcement Learning；用途 `prior`；路线 `q003:operator_card_fts` #3；Card `operator-learned-memory-crud-control`（operator）；Evidence `ev-p028-operator-core`
- Paper `P100` · How Many Tools Should an LLM Agent See? A Chance-Corrected Answer；用途 `prior`；路线 `q003:failure_card_fts` #2；Card `failure-fixed-shortlist-depth-masks-hard-query-zero`（failure）；Evidence `ev-p100-fixed-depth-buckets`, `ev-p100-weak-scorer-collapse`
- Paper `P069` · Tool Preferences in Agentic LLMs are Unreliable；用途 `prior`；路线 `q003:passage_hybrid` #19；Passage `P069:p0001:s0001`
- Paper `P013` · Large Language Models Cannot Self-Correct Reasoning Yet；用途 `measurement`；路线 `q004:paper_card_fts` #2；Card `paper-p013`（paper）；Evidence `ev-p013-intrinsic-self-correction-degrades`, `ev-p013-oracle-free-equal-budget-boundary`
- Paper `P078` · CRAFT: Customizing LLMs by Creating and Retrieving from Specialized Toolsets；用途 `measurement`；路线 `q004:passage_hybrid` #9；Passage `P078:p0009:s0004`
- Paper `P057` · Automated Design of Agentic Systems；用途 `measurement`；路线 `q004:failure_card_fts` #1；Card `failure-reused-selection-feedback-in-agent-search`（failure）；Evidence `ev-p057-search-evaluation-budget`
- Paper `P081` · Self-Consistency Improves Chain of Thought Reasoning in Language Models；用途 `measurement`；路线 `q004:operator_card_fts` #1；Card `operator-fixed-budget-independent-path-aggregation`（operator）；Evidence `ev-p081-fixed-answer-space-boundary`, `ev-p081-forty-sample-baseline`, `ev-p081-independent-path-majority-aggregation`

- 代表项：16 / 去重 Paper：71

## 查询与路线覆盖

### q001 · problem

- 原始查询：`tool documentation expansion may increase nearest-neighbor semantic collisions and reduce downstream LLM tool selection accuracy`
- 规范化查询：`"tool" OR "documentation" OR "expansion" OR "may" OR "increase" OR "nearest" OR "neighbor" OR "semantic" OR "collisions" OR "and" OR "reduce" OR "downstream" OR "LLM" OR "selection" OR "accuracy"`
- 路线 `paper_card_fts`：12 条；降级 false（无）
- 路线 `failure_card_fts`：12 条；降级 false（无）
- 路线 `passage_hybrid`：24 条；降级 false（无）
- 路线 `operator_card_fts`：12 条；降级 false（无）

### q002 · operator

- 原始查询：`contrastive relative tool descriptions distinguish similar sibling tools using explicit boundaries and non-affordances`
- 规范化查询：`"contrastive" OR "relative" OR "tool" OR "descriptions" OR "distinguish" OR "similar" OR "sibling" OR "tools" OR "using" OR "explicit" OR "boundaries" OR "and" OR "non" OR "affordances"`
- 路线 `operator_card_fts`：12 条；降级 false（无）
- 路线 `paper_card_fts`：12 条；降级 false（无）
- 路线 `passage_hybrid`：24 条；降级 false（无）
- 路线 `failure_card_fts`：12 条；降级 false（无）

### q003 · prior

- 原始查询：`similarity-aware tool documentation optimization comparative descriptions hard negatives ToolExpNet ToolObserver Tool-DE`
- 规范化查询：`"similarity" OR "aware" OR "tool" OR "documentation" OR "optimization" OR "comparative" OR "descriptions" OR "hard" OR "negatives" OR "ToolExpNet" OR "ToolObserver" OR "DE"`
- 路线 `paper_card_fts`：12 条；降级 false（无）
- 路线 `operator_card_fts`：12 条；降级 false（无）
- 路线 `failure_card_fts`：12 条；降级 false（无）
- 路线 `passage_hybrid`：24 条；降级 false（无）

### q004 · measurement

- 原始查询：`joint retrieval recall and downstream final tool-selection accuracy under equal documentation token budget`
- 规范化查询：`"joint" OR "retrieval" OR "recall" OR "and" OR "downstream" OR "final" OR "tool" OR "selection" OR "accuracy" OR "under" OR "equal" OR "documentation" OR "token" OR "budget"`
- 路线 `paper_card_fts`：12 条；降级 false（无）
- 路线 `passage_hybrid`：24 条；降级 false（无）
- 路线 `failure_card_fts`：12 条；降级 false（无）
- 路线 `operator_card_fts`：12 条；降级 false（无）

## 覆盖诊断

- 去重 Card：95
- 去重 Evidence：141
- 去重 Passage：69
- 命中 Paper：71
- 原始观测：240
- 带机械噪声标记的观测：0
