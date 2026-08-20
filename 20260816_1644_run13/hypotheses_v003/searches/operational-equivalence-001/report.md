<!-- CRL_RESEARCH_SEARCH_META {"created_at_utc":"2026-08-16T09:06:30.721431Z","request_fingerprint_sha256":"57672c81df81689a018a8123a80dfdc8367eacf492545ffcc984c0fc14215cc9","result_json_sha256":"12c2f22dc134613ff983f79dcf6d4b8d7ad3c450381dcdab1b88751d24d0b21e","search_id":"operational-equivalence-001"} -->
# 研究检索导航

> 本报告仅展示查询路线、来源、命中定位与覆盖；所有科研判断由主研究者完成。

- 搜索标识：`operational-equivalence-001`
- 生成时间（协调世界时）：`2026-08-16T09:06:30.721431Z`

## 紧凑研究地图

> 跨路线按 Paper 去重；每个查询路线至多选一个尚未出现的最高排名代表项。完整原始命中保留在 `result.json`。

- Paper `P085` · Retrieval Models Aren't Tool-Savvy: Benchmarking Tool Retrieval for Large Language Models；用途 `problem`；路线 `q001:paper_card_fts` #1；Card `paper-p085`（paper）；Evidence `ev-p085-large-corpus-scale`, `ev-p085-non-exhaustive-label`, `ev-p085-retrieval-completeness-failure`
- Paper `P025` · Unlocking the Power of Multi-Agent LLM for Reasoning: From Lazy Agents to Deliberation；用途 `problem`；路线 `q001:failure_card_fts` #2；Card `failure-lazy-agent-effective-single-agent-collapse`（failure）；Evidence `ev-p025-failure-core`
- Paper `P087` · Tools Are Under-Documented: Simple Document Expansion Boosts Tool Retrieval；用途 `problem`；路线 `q001:passage_hybrid` #1；Passage `P087:p0003:s0002`
- Paper `P041` · LLM Agents Already Know When to Call Tools - Even Without Reasoning；用途 `problem`；路线 `q001:operator_card_fts` #1；Card `operator-hidden-state-tool-necessity-prefill`（operator）；Evidence `ev-p041-operator-core`, `ev-p041-probe-prefill-steering`
- Paper `P050` · Scaling Agentic Verifier for Competitive Coding；用途 `operator`；路线 `q002:operator_card_fts` #1；Card `operator-active-counterexample-verifier`（operator）；Evidence `ev-p050-operator-core`
- Paper `P084` · On the Robustness of Agentic Function Calling；用途 `operator`；路线 `q002:paper_card_fts` #1；Card `paper-p084`（paper）；Evidence `ev-p084-expanded-toolkit-controlled-setting`, `ev-p084-expanded-toolkit-table`, `ev-p084-generated-tool-single-dataset-boundary`, `ev-p084-related-toolkit-error-types`
- Paper `P074` · ToolGate: Contract-Grounded and Verified Tool Execution for LLMs；用途 `operator`；路线 `q002:passage_hybrid` #1；Passage `P074:p0015:s0001`
- Paper `P101` · Semantic Evaluation for Text-to-SQL with Distilled Test Suites；用途 `operator`；路线 `q002:failure_card_fts` #2；Card `failure-single-execution-denotation-false-positive`（failure）；Evidence `ev-p101-esm-fn-rate`, `ev-p101-metric-distortion`
- Paper `P098` · Beyond Objective Equivalence: Constraint Injection for LLM-Based Optimization Modeling on Vehicle Routing Problems；用途 `prior`；路线 `q003:paper_card_fts` #2；Card `paper-p098`（paper）；Evidence `ev-p098-constraint-injection`, `ev-p098-diff-leak-550`, `ev-p098-nonbinding-blindness`, `ev-p098-open-problem`
- Paper `P037` · ToolSandbox: A Stateful, Conversational, Interactive Evaluation Benchmark for LLM Tool Use Capabilities；用途 `prior`；路线 `q003:operator_card_fts` #2；Card `operator-milestone-dag-trajectory-evaluation`（operator）；Evidence `ev-p037-evaluation-core`, `ev-p037-minefield-violation`
- Paper `P078` · CRAFT: Customizing LLMs by Creating and Retrieving from Specialized Toolsets；用途 `prior`；路线 `q003:failure_card_fts` #3；Card `failure-generic-or-unvalidated-tool-libraries-add-distractors`（failure）；Evidence `ev-p078-baseline-fairness-boundary`, `ev-p078-generic-tool-and-baseline-boundary`, `ev-p078-multiview-tool-retrieval`, `ev-p078-toolset-construction-cost`, `ev-p078-validated-tool-creation-retrieval`
- Paper `P020` · AgentTTS: Large Language Model Agent for Test-time Compute-optimal Scaling Strategy in Complex Tasks；用途 `prior`；路线 `q003:passage_hybrid` #7；Passage `P020:p0027:s0001`
- Paper `P004` · TravelPlanner: A Benchmark for Real-World Planning with Language Agents；用途 `measurement`；路线 `q004:paper_card_fts` #1；Card `paper-p004`（paper）；Evidence `ev-p004-failure-core`
- Paper `P066` · The Berkeley Function Calling Leaderboard (BFCL): From Tool Use to Agentic Evaluation of Large Language Models；用途 `measurement`；路线 `q004:passage_hybrid` #1；Passage `P066:p0005:s0002`
- Paper `P082` · Toolformer: Language Models Can Teach Themselves to Use Tools；用途 `measurement`；路线 `q004:failure_card_fts` #1；Card `failure-likelihood-utility-does-not-guarantee-agent-utility`（failure）；Evidence `ev-p082-chaining-cost-sparsity-boundary`, `ev-p082-future-token-loss-filtered-calls`, `ev-p082-top-k-single-call-boundary`
- Paper `P073` · Uncertainty Calibration for Tool-Using Language Agents；用途 `measurement`；路线 `q004:operator_card_fts` #2；Card `operator-execution-supervised-prompt-trace-calibration`（operator）；Evidence `ev-p073-execution-supervised-probe`, `ev-p073-internal-confidence-misalignment`

- 代表项：16 / 去重 Paper：61

## 查询与路线覆盖

### q001 · problem

- 原始查询：`tool retrieval benchmarks use non-exhaustive single tool labels although multiple tools may be operationally equivalent for a query`
- 规范化查询：`"tool" OR "retrieval" OR "benchmarks" OR "use" OR "non" OR "exhaustive" OR "single" OR "labels" OR "although" OR "multiple" OR "tools" OR "may" OR "be" OR "operationally" OR "equivalent" OR "for" OR "a" OR "query"`
- 路线 `paper_card_fts`：12 条；降级 false（无）
- 路线 `failure_card_fts`：12 条；降级 false（无）
- 路线 `passage_hybrid`：24 条；降级 false（无）
- 路线 `operator_card_fts`：12 条；降级 false（无）

### q002 · operator

- 原始查询：`execution based equivalence classes set valued positives for tool retrieval and selection`
- 规范化查询：`"execution" OR "based" OR "equivalence" OR "classes" OR "set" OR "valued" OR "positives" OR "for" OR "tool" OR "retrieval" OR "and" OR "selection"`
- 路线 `operator_card_fts`：12 条；降级 false（无）
- 路线 `paper_card_fts`：12 条；降级 false（无）
- 路线 `passage_hybrid`：24 条；降级 false（无）
- 路线 `failure_card_fts`：12 条；降级 false（无）

### q003 · prior

- 原始查询：`equivalent redundant overlapping tools tool merging functional equivalence retrieval evaluation`
- 规范化查询：`"equivalent" OR "redundant" OR "overlapping" OR "tools" OR "tool" OR "merging" OR "functional" OR "equivalence" OR "retrieval" OR "evaluation"`
- 路线 `paper_card_fts`：12 条；降级 false（无）
- 路线 `operator_card_fts`：12 条；降级 false（无）
- 路线 `failure_card_fts`：12 条；降级 false（无）
- 路线 `passage_hybrid`：24 条；降级 false（无）

### q004 · measurement

- 原始查询：`compare identifier exact match against observable task success and execution equivalent alternative tool calls`
- 规范化查询：`"compare" OR "identifier" OR "exact" OR "match" OR "against" OR "observable" OR "task" OR "success" OR "and" OR "execution" OR "equivalent" OR "alternative" OR "tool" OR "calls"`
- 路线 `paper_card_fts`：12 条；降级 false（无）
- 路线 `passage_hybrid`：24 条；降级 false（无）
- 路线 `failure_card_fts`：12 条；降级 false（无）
- 路线 `operator_card_fts`：12 条；降级 false（无）

## 覆盖诊断

- 去重 Card：88
- 去重 Evidence：117
- 去重 Passage：72
- 命中 Paper：61
- 原始观测：240
- 带机械噪声标记的观测：0
