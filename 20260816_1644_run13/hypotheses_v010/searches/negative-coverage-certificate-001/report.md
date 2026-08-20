<!-- CRL_RESEARCH_SEARCH_META {"created_at_utc":"2026-08-16T10:11:46.100630Z","request_fingerprint_sha256":"1aa47211ed82e6f8fc847256a55df0dc26ff1f00242552a4cff34216bedcdab7","result_json_sha256":"f41db934bbf2bf93bfe016640b478042d8b7765aa1badab4a351bf1dd4105f48","search_id":"negative-coverage-certificate-001"} -->
# 研究检索导航

> 本报告仅展示查询路线、来源、命中定位与覆盖；所有科研判断由主研究者完成。

- 搜索标识：`negative-coverage-certificate-001`
- 生成时间（协调世界时）：`2026-08-16T10:11:46.100630Z`

## 紧凑研究地图

> 跨路线按 Paper 去重；每个查询路线至多选一个尚未出现的最高排名代表项。完整原始命中保留在 `result.json`。

- Paper `P082` · Toolformer: Language Models Can Teach Themselves to Use Tools；用途 `problem`；路线 `q001:paper_card_fts` #1；Card `paper-p082`（paper）；Evidence `ev-p082-chaining-cost-sparsity-boundary`, `ev-p082-future-token-loss-filtered-calls`, `ev-p082-top-k-single-call-boundary`
- Paper `P074` · ToolGate: Contract-Grounded and Verified Tool Execution for LLMs；用途 `problem`；路线 `q001:failure_card_fts` #1；Card `failure-incomplete-tool-contracts-false-verified-state`（failure）；Evidence `ev-p074-contract-state-commit`, `ev-p074-missing-schema-true-postcondition`
- Paper `P040` · From Confident Closing to Silent Failure: Characterizing False Success in LLM Agents；用途 `problem`；路线 `q001:passage_hybrid` #1；Passage `P040:p0014:s0001`
- Paper `P041` · LLM Agents Already Know When to Call Tools - Even Without Reasoning；用途 `problem`；路线 `q001:operator_card_fts` #2；Card `operator-hidden-state-tool-necessity-prefill`（operator）；Evidence `ev-p041-operator-core`, `ev-p041-probe-prefill-steering`
- Paper `P100` · How Many Tools Should an LLM Agent See? A Chance-Corrected Answer；用途 `failure`；路线 `q002:failure_card_fts` #2；Card `failure-fixed-shortlist-depth-masks-hard-query-zero`（failure）；Evidence `ev-p100-fixed-depth-buckets`, `ev-p100-weak-scorer-collapse`
- Paper `P068` · DeepFact: Co-Evolving Benchmarks and Agents for Deep Research Factuality；用途 `failure`；路线 `q002:passage_hybrid` #1；Passage `P068:p0005:s0001`
- Paper `P030` · STALE: Can LLM Agents Know When Their Memories Are No Longer Valid?；用途 `failure`；路线 `q002:operator_card_fts` #1；Card `operator-write-side-state-adjudication`（operator）；Evidence `ev-p030-authorized-readout`, `ev-p030-failure-core`, `ev-p030-write-side-adjudication`
- Paper `P085` · Retrieval Models Aren't Tool-Savvy: Benchmarking Tool Retrieval for Large Language Models；用途 `failure`；路线 `q002:paper_card_fts` #2；Card `paper-p085`（paper）；Evidence `ev-p085-large-corpus-scale`, `ev-p085-non-exhaustive-label`, `ev-p085-retrieval-completeness-failure`
- Paper `P086` · Meta-Tool: Unleash Open-World Function Calling Capabilities of General-Purpose Large Language Models；用途 `operator`；路线 `q003:operator_card_fts` #1；Card `operator-required-parameter-description-tool-retrieval`（operator）；Evidence `ev-p086-hypothesize-retrieve-invoke`, `ev-p086-near-identical-distribution`, `ev-p086-required-parameter-score`
- Paper `P004` · TravelPlanner: A Benchmark for Real-World Planning with Language Agents；用途 `operator`；路线 `q003:paper_card_fts` #1；Card `paper-p004`（paper）；Evidence `ev-p004-failure-core`
- Paper `P066` · The Berkeley Function Calling Leaderboard (BFCL): From Tool Use to Agentic Evaluation of Large Language Models；用途 `operator`；路线 `q003:passage_hybrid` #1；Passage `P066:p0003:s0001`
- Paper `P065` · Group-in-Group Policy Optimization for LLM Agent Training；用途 `operator`；路线 `q003:failure_card_fts` #3；Card `failure-anchor-state-credit-needs-state-recurrence`（failure）；Evidence `ev-p065-anchor-state-credit`, `ev-p065-state-recurrence-boundary`
- Paper `P088` · Non-negative Elastic Net Decoding for Information Retrieval；用途 `prior`；路线 `q004:paper_card_fts` #2；Card `paper-p088`（paper）；Evidence `ev-p088-joint-nonnegative-objective`, `ev-p088-relevant-set-size-signature`, `ev-p088-theory-deployment-scale-boundary`
- Paper `P063` · A-Mem: Agentic Memory for LLM Agents；用途 `prior`；路线 `q004:operator_card_fts` #2；Card `operator-dynamic-linked-memory-evolution`（operator）；Evidence `ev-p063-dynamic-link-generation`, `ev-p063-neighbor-rewrite-action`, `ev-p063-retrieval-k-varies`
- Paper `P090` · From Single to Multi-Granularity: Toward Long-Term Memory Association and Selection of Conversational Agents；用途 `prior`；路线 `q004:failure_card_fts` #2；Card `failure-fixed-single-granularity-memory`（failure）；Evidence `ev-p090-entropy-router`, `ev-p090-fixed-granularity-selection`
- Paper `P042` · LiveResearchBench: A Live Benchmark for User-Centric Deep Research in the Wild；用途 `prior`；路线 `q004:passage_hybrid` #1；Passage `P042:p0018:s0001`
- Paper `P034` · RefineBench: Evaluating Refinement Capability of Language Models via Checklists；用途 `measurement`；路线 `q005:paper_card_fts` #1；Card `paper-p034`（paper）；Evidence `ev-p034-failure-core`
- Paper `P035` · Holistic Agent Leaderboard: The Missing Infrastructure for AI Agent Evaluation；用途 `measurement`；路线 `q005:passage_hybrid` #2；Passage `P035:p0028:s0001`
- Paper `P060` · Unifying Inference-Time Planning Language Generation；用途 `measurement`；路线 `q005:failure_card_fts` #1；Card `failure-natural-language-ir-hurts-formal-planning`（failure）；Evidence `ev-p060-formal-ir-solver`, `ev-p060-ir-result-and-nl-failure`
- Paper `P071` · Agentic Plan Caching: Test-Time Memory for Fast and Cost-Efficient LLM Agents；用途 `measurement`；路线 `q005:operator_card_fts` #1；Card `operator-adaptive-plan-template-reuse`（operator）；Evidence `ev-p071-cache-false-positive-boundary`, `ev-p071-plan-template-reuse`

- 代表项：20 / 去重 Paper：92

## 查询与路线覆盖

### q001 · problem

- 原始查询：`tool agent concludes no matching item from incomplete paginated truncated filtered API results`
- 规范化查询：`"tool" OR "agent" OR "concludes" OR "no" OR "matching" OR "item" OR "from" OR "incomplete" OR "paginated" OR "truncated" OR "filtered" OR "API" OR "results"`
- 路线 `paper_card_fts`：24 条；降级 false（无）
- 路线 `failure_card_fts`：24 条；降级 false（无）
- 路线 `passage_hybrid`：24 条；降级 false（无）
- 路线 `operator_card_fts`：24 条；降级 false（无）

### q002 · failure

- 原始查询：`negative existential absence claim incomplete query coverage pagination cursor stale snapshot hidden filter`
- 规范化查询：`"negative" OR "existential" OR "absence" OR "claim" OR "incomplete" OR "query" OR "coverage" OR "pagination" OR "cursor" OR "stale" OR "snapshot" OR "hidden" OR "filter"`
- 路线 `failure_card_fts`：24 条；降级 false（无）
- 路线 `passage_hybrid`：24 条；降级 false（无）
- 路线 `operator_card_fts`：24 条；降级 false（无）
- 路线 `paper_card_fts`：24 条；降级 false（无）

### q003 · operator

- 原始查询：`coverage certificate closed-world completion proof exhaustive pagination partition snapshot consistency`
- 规范化查询：`"coverage" OR "certificate" OR "closed" OR "world" OR "completion" OR "proof" OR "exhaustive" OR "pagination" OR "partition" OR "snapshot" OR "consistency"`
- 路线 `operator_card_fts`：7 条；降级 false（无）
- 路线 `paper_card_fts`：17 条；降级 false（无）
- 路线 `passage_hybrid`：24 条；降级 false（无）
- 路线 `failure_card_fts`：12 条；降级 false（无）

### q004 · prior

- 原始查询：`database completeness statements why-not provenance query completeness incomplete information negative answer`
- 规范化查询：`"database" OR "completeness" OR "statements" OR "why" OR "not" OR "provenance" OR "query" OR "incomplete" OR "information" OR "negative" OR "answer"`
- 路线 `paper_card_fts`：24 条；降级 false（无）
- 路线 `operator_card_fts`：24 条；降级 false（无）
- 路线 `failure_card_fts`：24 条；降级 false（无）
- 路线 `passage_hybrid`：24 条；降级 false（无）

### q005 · measurement

- 原始查询：`matched tasks hidden match later page early stopping false absence action safety`
- 规范化查询：`"matched" OR "tasks" OR "hidden" OR "match" OR "later" OR "page" OR "early" OR "stopping" OR "false" OR "absence" OR "action" OR "safety"`
- 路线 `paper_card_fts`：24 条；降级 false（无）
- 路线 `passage_hybrid`：24 条；降级 false（无）
- 路线 `failure_card_fts`：24 条；降级 false（无）
- 路线 `operator_card_fts`：24 条；降级 false（无）

## 覆盖诊断

- 去重 Card：167
- 去重 Evidence：197
- 去重 Passage：113
- 命中 Paper：92
- 原始观测：444
- 带机械噪声标记的观测：8
