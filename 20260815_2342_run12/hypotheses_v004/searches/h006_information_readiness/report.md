<!-- CRL_RESEARCH_SEARCH_META {"created_at_utc":"2026-08-15T16:39:13.343056Z","request_fingerprint_sha256":"2df1c46086bb79283c2b26b033c610be37882392a54e317b81b878b7f5ef51af","result_json_sha256":"03e45009b7aa1ff37cbcda7503db0f9477daadd82eaa83c9edca5ebded15a754","search_id":"h006_information_readiness"} -->
# 研究检索导航

> 本报告仅展示查询路线、来源、命中定位与覆盖；所有科研判断由主研究者完成。

- 搜索标识：`h006_information_readiness`
- 生成时间（协调世界时）：`2026-08-15T16:39:13.343056Z`

## 紧凑研究地图

> 跨路线按 Paper 去重；每个查询路线至多选一个尚未出现的最高排名代表项。完整原始命中保留在 `result.json`。

- Paper `P030` · STALE: Can LLM Agents Know When Their Memories Are No Longer Valid?；用途 `problem`；路线 `q001:paper_card_fts` #1；Card `paper-p030`（paper）；Evidence `ev-p030-failure-core`
- Paper `P010` · LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory；用途 `problem`；路线 `q001:failure_card_fts` #1；Card `failure-long-history-reading-overload`（failure）；Evidence `ev-p010-long-history-decline`
- Paper `P031` · Agent Memory: Characterization and System Implications of Stateful Long-Horizon Workloads；用途 `problem`；路线 `q001:passage_hybrid` #1；Passage `P031:p0003:s0001`
- Paper `P046` · Solver-Aided Verification of Policy Compliance in Tool-Augmented LLM Agents；用途 `problem`；路线 `q001:operator_card_fts` #1；Card `operator-smt-preexecution-policy-guard`（operator）；Evidence `ev-p046-operator-core`
- Paper `P074` · ToolGate: Contract-Grounded and Verified Tool Execution for LLMs；用途 `failure`；路线 `q002:failure_card_fts` #1；Card `failure-incomplete-tool-contracts-false-verified-state`（failure）；Evidence `ev-p074-contract-state-commit`, `ev-p074-missing-schema-true-postcondition`
- Paper `P007` · tau-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains；用途 `failure`；路线 `q002:passage_hybrid` #1；Passage `P007:p0037:s0001`
- Paper `P022` · MOC: Multi-Order Communication in LLM-based Multi-Agent Systems；用途 `failure`；路线 `q002:operator_card_fts` #3；Card `operator-higher-order-message-exposure`（operator）；Evidence `ev-p022-operator-core`
- Paper `P005` · ToolLLM: Facilitating Large Language Models to Master 16000+ Real-world APIs；用途 `failure`；路线 `q002:paper_card_fts` #1；Card `paper-p005`（paper）；Evidence `ev-p005-operator-core`
- Paper `P048` · NaviAgent: Graph-Driven Bilevel Planning for Scalable Tool Orchestration；用途 `operator`；路线 `q003:operator_card_fts` #1；Card `operator-bilevel-graph-toolchain-planning`（operator）；Evidence `ev-p048-operator-core`
- Paper `P006` · An LLM Compiler for Parallel Function Calling；用途 `operator`；路线 `q003:paper_card_fts` #2；Card `paper-llmcompiler`（paper）；Evidence `ev-p006-dependency-dag-dispatch`, `ev-p006-shared-prompt-comparison-boundary`, `ev-p006-token-cost-accounting`
- Paper `P052` · Planning Anything with Rigor: General-Purpose Zero-Shot Planning with LLM-based Formalized Programming；用途 `operator`；路线 `q003:passage_hybrid` #11；Passage `P052:p0049:s0001`
- Paper `P056` · GPTSwarm: Language Agents as Optimizable Graphs；用途 `operator`；路线 `q003:failure_card_fts` #1；Card `failure-same-set-agent-graph-evaluation`（failure）；Evidence `ev-p056-graph-optimization`, `ev-p056-same-set-crosswords`
- Paper `P047` · tau2-Bench: Evaluating Conversational Agents in a Dual-Control Environment；用途 `prior`；路线 `q004:paper_card_fts` #1；Card `paper-p047`（paper）；Evidence `ev-p047-evaluation-core`
- Paper `P001` · ReAct: Synergizing Reasoning and Acting in Language Models；用途 `prior`；路线 `q004:operator_card_fts` #1；Card `operator-reason-action-interleaving`（operator）；Evidence `ev-p001-react-interleaved`
- Paper `P002` · Tree of Thoughts: Deliberate Problem Solving with Large Language Models；用途 `prior`；路线 `q004:failure_card_fts` #1；Card `failure-search-resource-cost`（failure）；Evidence `ev-p002-search-resource-cost`
- Paper `P037` · ToolSandbox: A Stateful, Conversational, Interactive Evaluation Benchmark for LLM Tool Use Capabilities；用途 `prior`；路线 `q004:passage_hybrid` #2；Passage `P037:p0003:s0001`
- Paper `P017` · Understanding the Information Propagation Effects of Communication Topologies in LLM-based Multi-Agent Systems；用途 `measurement`；路线 `q005:paper_card_fts` #2；Card `paper-p017`（paper）；Evidence `ev-p017-failure-core`
- Paper `P036` · tau-Knowledge: Evaluating Conversational Agents over Unstructured Knowledge；用途 `measurement`；路线 `q005:passage_hybrid` #1；Passage `P036:p0023:s0001`
- Paper `P039` · ToolFailBench: Diagnosing Tool-Use Failures in LLM Agents；用途 `measurement`；路线 `q005:failure_card_fts` #2；Card `failure-tool-use-metrics-collapse-distinct-errors`（failure）；Evidence `ev-p039-aggregate-score-masking`, `ev-p039-failure-core`
- Paper `P093` · Collapse of Dense Retrievers: Short, Early, and Literal Biases Outranking Factual Evidence；用途 `measurement`；路线 `q005:operator_card_fts` #3；Card `operator-paired-single-factor-bias-decomposition`（operator）；Evidence `ev-p093-foil-collapse`, `ev-p093-paired-protocol`

- 代表项：20 / 去重 Paper：90

## 查询与路线覆盖

### q001 · problem

- 原始查询：`LLM agent executes irreversible write before reading decision relevant information information readiness`
- 规范化查询：`"LLM" OR "agent" OR "executes" OR "irreversible" OR "write" OR "before" OR "reading" OR "decision" OR "relevant" OR "information" OR "readiness"`
- 路线 `paper_card_fts`：20 条；降级 false（无）
- 路线 `failure_card_fts`：20 条；降级 false（无）
- 路线 `passage_hybrid`：24 条；降级 false（无）
- 路线 `operator_card_fts`：20 条；降级 false（无）

### q002 · failure

- 原始查询：`all tool calls locally successful wrong order read after commit irreversible regret`
- 规范化查询：`"all" OR "tool" OR "calls" OR "locally" OR "successful" OR "wrong" OR "order" OR "read" OR "after" OR "commit" OR "irreversible" OR "regret"`
- 路线 `failure_card_fts`：20 条；降级 false（无）
- 路线 `passage_hybrid`：24 条；降级 false（无）
- 路线 `operator_card_fts`：20 条；降级 false（无）
- 路线 `paper_card_fts`：20 条；降级 false（无）

### q003 · operator

- 原始查询：`information dependency graph delay irreversible actions until upstream reads resolved scheduling`
- 规范化查询：`"information" OR "dependency" OR "graph" OR "delay" OR "irreversible" OR "actions" OR "until" OR "upstream" OR "reads" OR "resolved" OR "scheduling"`
- 路线 `operator_card_fts`：20 条；降级 false（无）
- 路线 `paper_card_fts`：20 条；降级 false（无）
- 路线 `passage_hybrid`：24 条；降级 false（无）
- 路线 `failure_card_fts`：11 条；降级 false（无）

### q004 · prior

- 原始查询：`ToolSandbox TPS-Bench Reason Less Verify More ToolGate IPIGuard SABER irreversible action scheduling`
- 规范化查询：`"ToolSandbox" OR "TPS" OR "Bench" OR "Reason" OR "Less" OR "Verify" OR "More" OR "ToolGate" OR "IPIGuard" OR "SABER" OR "irreversible" OR "action" OR "scheduling"`
- 路线 `paper_card_fts`：20 条；降级 false（无）
- 路线 `operator_card_fts`：15 条；降级 false（无）
- 路线 `failure_card_fts`：15 条；降级 false（无）
- 路线 `passage_hybrid`：24 条；降级 false（无）

### q005 · measurement

- 原始查询：`commit before information acquisition action order dependency paired tasks irreversible regret`
- 规范化查询：`"commit" OR "before" OR "information" OR "acquisition" OR "action" OR "order" OR "dependency" OR "paired" OR "tasks" OR "irreversible" OR "regret"`
- 路线 `paper_card_fts`：20 条；降级 false（无）
- 路线 `passage_hybrid`：24 条；降级 false（无）
- 路线 `failure_card_fts`：20 条；降级 false（无）
- 路线 `operator_card_fts`：20 条；降级 false（无）

## 覆盖诊断

- 去重 Card：145
- 去重 Evidence：178
- 去重 Passage：117
- 命中 Paper：90
- 原始观测：401
- 带机械噪声标记的观测：2
