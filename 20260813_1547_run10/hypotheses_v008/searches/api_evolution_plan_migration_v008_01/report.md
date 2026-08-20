<!-- CRL_RESEARCH_SEARCH_META {"created_at_utc":"2026-08-13T10:47:09.844617Z","request_fingerprint_sha256":"176c8d617cb7e79629fbe1ce70c4a84904a55b1321af7557af853e3d555d1ad1","result_json_sha256":"66524418ce640e415aa15dd0340fc8b44eb9b6d5a23db2fcfcc10634f9229e6c","search_id":"api_evolution_plan_migration_v008_01"} -->
# 研究检索导航

> 本报告仅展示查询路线、来源、命中定位与覆盖；所有科研判断由主研究者完成。

- 搜索标识：`api_evolution_plan_migration_v008_01`
- 生成时间（协调世界时）：`2026-08-13T10:47:09.844617Z`

## 紧凑研究地图

> 跨路线按 Paper 去重；每个查询路线至多选一个尚未出现的最高排名代表项。完整原始命中保留在 `result.json`。

- Paper `P013` · Large Language Models Cannot Self-Correct Reasoning Yet；用途 `problem`；路线 `q001:paper_card_fts` #1；Card `paper-p013`（paper）；Evidence `ev-p013-intrinsic-self-correction-degrades`, `ev-p013-oracle-free-equal-budget-boundary`
- Paper `P091` · Temporal Validity in Retrieval Memory: Eliminating Stale-Fact Errors for AI Agents over Evolving Knowledge；用途 `problem`；路线 `q001:failure_card_fts` #1；Card `failure-cosine-cannot-separate-contradiction-from-duplicate`（failure）；Evidence `ev-p091-cosine-auroc`, `ev-p091-retain-fabrication`
- Paper `P071` · Agentic Plan Caching: Test-Time Memory for Fast and Cost-Efficient LLM Agents；用途 `problem`；路线 `q001:passage_hybrid` #1；Passage `P071:p0027:s0001`
- Paper `P041` · LLM Agents Already Know When to Call Tools - Even Without Reasoning；用途 `problem`；路线 `q001:operator_card_fts` #1；Card `operator-hidden-state-tool-necessity-prefill`（operator）；Evidence `ev-p041-operator-core`, `ev-p041-probe-prefill-steering`
- Paper `P084` · On the Robustness of Agentic Function Calling；用途 `failure`；路线 `q002:failure_card_fts` #1；Card `failure-semantically-related-toolkit-expansion`（failure）；Evidence `ev-p084-expanded-toolkit-controlled-setting`, `ev-p084-expanded-toolkit-table`, `ev-p084-generated-tool-single-dataset-boundary`, `ev-p084-related-toolkit-error-types`
- Paper `P070` · ProMCP: Profiling Token Flows and Latency Costs in Model Context Protocol-Based LLM Agents；用途 `failure`；路线 `q002:passage_hybrid` #1；Passage `P070:p0003:s0001`
- Paper `P063` · A-Mem: Agentic Memory for LLM Agents；用途 `failure`；路线 `q002:operator_card_fts` #2；Card `operator-dynamic-linked-memory-evolution`（operator）；Evidence `ev-p063-dynamic-link-generation`, `ev-p063-neighbor-rewrite-action`, `ev-p063-retrieval-k-varies`
- Paper `P035` · Holistic Agent Leaderboard: The Missing Infrastructure for AI Agent Evaluation；用途 `failure`；路线 `q002:paper_card_fts` #3；Card `paper-p035`（paper）；Evidence `ev-p035-evaluation-core`
- Paper `P050` · Scaling Agentic Verifier for Competitive Coding；用途 `operator`；路线 `q003:operator_card_fts` #1；Card `operator-active-counterexample-verifier`（operator）；Evidence `ev-p050-operator-core`
- Paper `P089` · ToolDreamer: Instilling LLM Reasoning Into Tool Retrievers；用途 `operator`；路线 `q003:paper_card_fts` #1；Card `paper-p089`（paper）；Evidence `ev-p089-api-latency-boundary`, `ev-p089-forced-alignment-proxy`, `ev-p089-hungarian-alignment`, `ev-p089-overview-alignment-rrf`, `ev-p089-retrieval-only-metrics`, `ev-p089-training-gold-count-hypothetical-tools`
- Paper `P048` · NaviAgent: Graph-Driven Bilevel Planning for Scalable Tool Orchestration；用途 `operator`；路线 `q003:passage_hybrid` #1；Passage `P048:p0002:s0001`
- Paper `P098` · Beyond Objective Equivalence: Constraint Injection for LLM-Based Optimization Modeling on Vehicle Routing Problems；用途 `operator`；路线 `q003:failure_card_fts` #1；Card `failure-objective-equivalence-passes-nonbinding-errors`（failure）；Evidence `ev-p098-diff-leak-550`, `ev-p098-nonbinding-blindness`, `ev-p098-open-problem`
- Paper `P005` · ToolLLM: Facilitating Large Language Models to Master 16000+ Real-world APIs；用途 `prior`；路线 `q004:paper_card_fts` #4；Card `paper-p005`（paper）；Evidence `ev-p005-operator-core`
- Paper `P097` · ReLoop: Structured Modeling and Behavioral Verification for Reliable LLM-Based Optimization；用途 `prior`；路线 `q004:operator_card_fts` #1；Card `operator-behavioral-perturbation-existence-test`（operator）；Evidence `ev-p097-behavioral-perturbation`, `ev-p097-feasibility-gap`
- Paper `P095` · Don't Ask the LLM to Track Freshness: A Deterministic Recipe for Memory Conflict Resolution；用途 `prior`；路线 `q004:failure_card_fts` #4；Card `failure-llm-freshness-judgment-prior-override-and-drift`（failure）；Evidence `ev-p095-matched-comparison`, `ev-p095-prior-override-drift`
- Paper `P074` · ToolGate: Contract-Grounded and Verified Tool Execution for LLMs；用途 `prior`；路线 `q004:passage_hybrid` #12；Passage `P074:p0014:s0001`
- Paper `P087` · Tools Are Under-Documented: Simple Document Expansion Boosts Tool Retrieval；用途 `measurement`；路线 `q005:paper_card_fts` #1；Card `paper-p087`（paper）；Evidence `ev-p087-fields-not-universally-beneficial`, `ev-p087-merge-and-semantic-judge`, `ev-p087-structured-query-independent-expansion`
- Paper `P039` · ToolFailBench: Diagnosing Tool-Use Failures in LLM Agents；用途 `measurement`；路线 `q005:passage_hybrid` #2；Passage `P039:p0001:s0003`
- Paper `P085` · Retrieval Models Aren't Tool-Savvy: Benchmarking Tool Retrieval for Large Language Models；用途 `measurement`；路线 `q005:failure_card_fts` #1；Card `failure-large-corpus-tool-retrieval-breaks-oracle-menu`（failure）；Evidence `ev-p085-large-corpus-scale`, `ev-p085-non-exhaustive-label`, `ev-p085-retrieval-completeness-failure`
- Paper `P073` · Uncertainty Calibration for Tool-Using Language Agents；用途 `measurement`；路线 `q005:operator_card_fts` #1；Card `operator-execution-supervised-prompt-trace-calibration`（operator）；Evidence `ev-p073-execution-supervised-probe`, `ev-p073-internal-confidence-misalignment`

- 代表项：20 / 去重 Paper：98

## 查询与路线覆盖

### q001 · problem

- 原始查询：`LLM tool agent cached plan or skill fails under evolving API schemas, tool names, defaults, operation split, response changes`
- 规范化查询：`"LLM" OR "tool" OR "agent" OR "cached" OR "plan" OR "or" OR "skill" OR "fails" OR "under" OR "evolving" OR "API" OR "schemas" OR "names" OR "defaults" OR "operation" OR "split" OR "response" OR "changes"`
- 路线 `paper_card_fts`：40 条；降级 false（无）
- 路线 `failure_card_fts`：40 条；降级 false（无）
- 路线 `passage_hybrid`：100 条；降级 false（无）
- 路线 `operator_card_fts`：40 条；降级 false（无）

### q002 · failure

- 原始查询：`previously successful tool workflow becomes invalid or silently semantically wrong after tool or MCP server evolution`
- 规范化查询：`"previously" OR "successful" OR "tool" OR "workflow" OR "becomes" OR "invalid" OR "or" OR "silently" OR "semantically" OR "wrong" OR "after" OR "MCP" OR "server" OR "evolution"`
- 路线 `failure_card_fts`：39 条；降级 false（无）
- 路线 `passage_hybrid`：100 条；降级 false（无）
- 路线 `operator_card_fts`：40 条；降级 false（无）
- 路线 `paper_card_fts`：40 条；降级 false（无）

### q003 · operator

- 原始查询：`cross-version differential behavioral equivalence, plan migration, tool sequence repair, schema matching, one-to-many API replacement`
- 规范化查询：`"cross" OR "version" OR "differential" OR "behavioral" OR "equivalence" OR "plan" OR "migration" OR "tool" OR "sequence" OR "repair" OR "schema" OR "matching" OR "one" OR "to" OR "many" OR "API" OR "replacement"`
- 路线 `operator_card_fts`：40 条；降级 false（无）
- 路线 `paper_card_fts`：40 条；降级 false（无）
- 路线 `passage_hybrid`：100 条；降级 false（无）
- 路线 `failure_card_fts`：40 条；降级 false（无）

### q004 · prior

- 原始查询：`API migration, REST API differential regression testing, MCP tool evolution, agent robustness under schema drift, program repair`
- 规范化查询：`"API" OR "migration" OR "REST" OR "differential" OR "regression" OR "testing" OR "MCP" OR "tool" OR "evolution" OR "agent" OR "robustness" OR "under" OR "schema" OR "drift" OR "program" OR "repair"`
- 路线 `paper_card_fts`：40 条；降级 false（无）
- 路线 `operator_card_fts`：40 条；降级 false（无）
- 路线 `failure_card_fts`：40 条；降级 false（无）
- 路线 `passage_hybrid`：100 条；降级 false（无）

### q005 · measurement

- 原始查询：`end-state task success under unseen tool evolution, migration exactness, extra probes, abstention, semantic equivalence`
- 规范化查询：`"end" OR "state" OR "task" OR "success" OR "under" OR "unseen" OR "tool" OR "evolution" OR "migration" OR "exactness" OR "extra" OR "probes" OR "abstention" OR "semantic" OR "equivalence"`
- 路线 `paper_card_fts`：40 条；降级 false（无）
- 路线 `passage_hybrid`：100 条；降级 false（无）
- 路线 `failure_card_fts`：40 条；降级 false（无）
- 路线 `operator_card_fts`：40 条；降级 false（无）

## 覆盖诊断

- 去重 Card：205
- 去重 Evidence：216
- 去重 Passage：326
- 命中 Paper：98
- 原始观测：1099
- 带机械噪声标记的观测：4
