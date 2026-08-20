<!-- CRL_RESEARCH_SEARCH_META {"created_at_utc":"2026-08-18T16:19:46.647340Z","request_fingerprint_sha256":"a5000930de2c1c773bb5e5b18dbf2a35a79b6017e797ffa67abdc25c86c0aea4","result_json_sha256":"c074f44aa7700e00b22cd81780c4ee914a90472b103e547c165f80bf384a25be","search_id":"ranking-distortion-frontier-v001"} -->
# 研究检索导航

> 本报告仅展示查询路线、来源、命中定位与覆盖；所有科研判断由主研究者完成。

- 搜索标识：`ranking-distortion-frontier-v001`
- 生成时间（协调世界时）：`2026-08-18T16:19:46.647340Z`

## 紧凑研究地图

> 跨路线按 Paper 去重；每个查询路线至多选一个尚未出现的最高排名代表项。完整原始命中保留在 `result.json`。

- Paper `P101` · Semantic Evaluation for Text-to-SQL with Distilled Test Suites；用途 `problem`；路线 `q001:paper_card_fts` #1；Card `paper-p101`（paper）；Evidence `ev-p101-esm-fn-rate`, `ev-p101-metric-distortion`, `ev-p101-neighbor-distillation`
- Paper `P039` · ToolFailBench: Diagnosing Tool-Use Failures in LLM Agents；用途 `problem`；路线 `q001:failure_card_fts` #1；Card `failure-tool-use-metrics-collapse-distinct-errors`（failure）；Evidence `ev-p039-aggregate-score-masking`, `ev-p039-failure-core`
- Paper `P040` · From Confident Closing to Silent Failure: Characterizing False Success in LLM Agents；用途 `problem`；路线 `q001:passage_hybrid` #2；Passage `P040:p0001:s0003`
- Paper `P008` · Agent Security Bench (ASB): Formalizing and Benchmarking Attacks and Defenses in LLM-based Agents；用途 `problem`；路线 `q001:operator_card_fts` #1；Card `operator-stagewise-agent-security-audit`（operator）；Evidence `ev-p008-stagewise-attack-surface`
- Paper `P082` · Toolformer: Language Models Can Teach Themselves to Use Tools；用途 `failure`；路线 `q002:failure_card_fts` #1；Card `failure-likelihood-utility-does-not-guarantee-agent-utility`（failure）；Evidence `ev-p082-chaining-cost-sparsity-boundary`, `ev-p082-future-token-loss-filtered-calls`, `ev-p082-top-k-single-call-boundary`
- Paper `P070` · ProMCP: Profiling Token Flows and Latency Costs in Model Context Protocol-Based LLM Agents；用途 `failure`；路线 `q002:passage_hybrid` #1；Passage `P070:p0011:s0002`
- Paper `P037` · ToolSandbox: A Stateful, Conversational, Interactive Evaluation Benchmark for LLM Tool Use Capabilities；用途 `failure`；路线 `q002:operator_card_fts` #1；Card `operator-milestone-dag-trajectory-evaluation`（operator）；Evidence `ev-p037-evaluation-core`, `ev-p037-minefield-violation`
- Paper `P006` · An LLM Compiler for Parallel Function Calling；用途 `failure`；路线 `q002:paper_card_fts` #2；Card `paper-llmcompiler`（paper）；Evidence `ev-p006-dependency-dag-dispatch`, `ev-p006-shared-prompt-comparison-boundary`, `ev-p006-token-cost-accounting`
- Paper `P027` · Verified Critical Step Optimization for LLM Agents；用途 `operator`；路线 `q003:operator_card_fts` #1；Card `operator-verified-single-branch-repair`（operator）；Evidence `ev-p027-operator-core`
- Paper `P019` · STeCa: Step-level Trajectory Calibration for LLM Agent Learning；用途 `operator`；路线 `q003:paper_card_fts` #1；Card `paper-p019`（paper）；Evidence `ev-p019-ground-truth-calibration-oracle`, `ev-p019-step-level-calibration`
- Paper `P036` · tau-Knowledge: Evaluating Conversational Agents over Unstructured Knowledge；用途 `operator`；路线 `q003:passage_hybrid` #1；Passage `P036:p0023:s0001`
- Paper `P093` · Collapse of Dense Retrievers: Short, Early, and Literal Biases Outranking Factual Evidence；用途 `operator`；路线 `q003:failure_card_fts` #1；Card `failure-dense-retriever-surface-bias-collapse`（failure）；Evidence `ev-p093-foil-collapse`, `ev-p093-paired-protocol`, `ev-p093-poison-rag`
- Paper `P035` · Holistic Agent Leaderboard: The Missing Infrastructure for AI Agent Evaluation；用途 `prior`；路线 `q004:paper_card_fts` #1；Card `paper-p035`（paper）；Evidence `ev-p035-evaluation-core`
- Paper `P074` · ToolGate: Contract-Grounded and Verified Tool Execution for LLMs；用途 `prior`；路线 `q004:operator_card_fts` #1；Card `operator-contract-gated-tool-state-commit`（operator）；Evidence `ev-p074-contract-state-commit`, `ev-p074-missing-schema-true-postcondition`
- Paper `P057` · Automated Design of Agentic Systems；用途 `prior`；路线 `q004:failure_card_fts` #2；Card `failure-reused-selection-feedback-in-agent-search`（failure）；Evidence `ev-p057-search-evaluation-budget`
- Paper `P067` · AgentHarm: A Benchmark for Measuring Harmfulness of LLM Agents；用途 `prior`；路线 `q004:passage_hybrid` #1；Passage `P067:p0006:s0001`
- Paper `P073` · Uncertainty Calibration for Tool-Using Language Agents；用途 `measurement`；路线 `q005:paper_card_fts` #3；Card `paper-p073`（paper）；Evidence `ev-p073-execution-supervised-probe`, `ev-p073-internal-confidence-misalignment`
- Paper `P083` · TAMAS: Benchmarking Adversarial Risks in Multi-Agent LLM Systems；用途 `measurement`；路线 `q005:passage_hybrid` #2；Passage `P083:p0017:s0001`
- Paper `P030` · STALE: Can LLM Agents Know When Their Memories Are No Longer Valid?；用途 `measurement`；路线 `q005:failure_card_fts` #2；Card `failure-retrieved-update-lacks-decision-authority`（failure）；Evidence `ev-p030-failure-core`, `ev-p030-recognition-application-gap`
- Paper `P089` · ToolDreamer: Instilling LLM Reasoning Into Tool Retrievers；用途 `measurement`；路线 `q005:operator_card_fts` #2；Card `operator-hypothetical-tool-query-expansion`（operator）；Evidence `ev-p089-api-latency-boundary`, `ev-p089-forced-alignment-proxy`, `ev-p089-hungarian-alignment`, `ev-p089-overview-alignment-rrf`, `ev-p089-retrieval-only-metrics`, `ev-p089-training-gold-count-hypothetical-tools`

- 代表项：20 / 去重 Paper：65

## 查询与路线覆盖

### q001 · problem

- 原始查询：`agent benchmark ranking reversal aggregate success rate subgroup failure model ranking evaluation distortion`
- 规范化查询：`"agent" OR "benchmark" OR "ranking" OR "reversal" OR "aggregate" OR "success" OR "rate" OR "subgroup" OR "failure" OR "model" OR "evaluation" OR "distortion"`
- 路线 `paper_card_fts`：10 条；降级 false（无）
- 路线 `failure_card_fts`：10 条；降级 false（无）
- 路线 `passage_hybrid`：8 条；降级 false（无）
- 路线 `operator_card_fts`：10 条；降级 false（无）

### q002 · failure

- 原始查询：`tool agent evaluation success score hides cost tool calls latency token usage or partial completion ranking`
- 规范化查询：`"tool" OR "agent" OR "evaluation" OR "success" OR "score" OR "hides" OR "cost" OR "calls" OR "latency" OR "token" OR "usage" OR "or" OR "partial" OR "completion" OR "ranking"`
- 路线 `failure_card_fts`：10 条；降级 false（无）
- 路线 `passage_hybrid`：8 条；降级 false（无）
- 路线 `operator_card_fts`：10 条；降级 false（无）
- 路线 `paper_card_fts`：10 条；降级 false（无）

### q003 · operator

- 原始查询：`paired counterfactual benchmark resampling robust model ranking task difficulty calibration agent trajectories`
- 规范化查询：`"paired" OR "counterfactual" OR "benchmark" OR "resampling" OR "robust" OR "model" OR "ranking" OR "task" OR "difficulty" OR "calibration" OR "agent" OR "trajectories"`
- 路线 `operator_card_fts`：10 条；降级 false（无）
- 路线 `paper_card_fts`：10 条；降级 false（无）
- 路线 `passage_hybrid`：8 条；降级 false（无）
- 路线 `failure_card_fts`：10 条；降级 false（无）

### q004 · prior

- 原始查询：`LLM agent benchmark contamination memorization test leakage dynamic benchmark ranking reliability 2025 2026`
- 规范化查询：`"LLM" OR "agent" OR "benchmark" OR "contamination" OR "memorization" OR "test" OR "leakage" OR "dynamic" OR "ranking" OR "reliability" OR "2025" OR "2026"`
- 路线 `paper_card_fts`：10 条；降级 false（无）
- 路线 `operator_card_fts`：10 条；降级 false（无）
- 路线 `failure_card_fts`：10 条；降级 false（无）
- 路线 `passage_hybrid`：8 条；降级 false（无）

### q005 · measurement

- 原始查询：`bootstrap rank stability model comparison agent benchmark confidence interval stratified failure`
- 规范化查询：`"bootstrap" OR "rank" OR "stability" OR "model" OR "comparison" OR "agent" OR "benchmark" OR "confidence" OR "interval" OR "stratified" OR "failure"`
- 路线 `paper_card_fts`：10 条；降级 false（无）
- 路线 `passage_hybrid`：8 条；降级 false（无）
- 路线 `failure_card_fts`：10 条；降级 false（无）
- 路线 `operator_card_fts`：10 条；降级 false（无）

## 覆盖诊断

- 去重 Card：98
- 去重 Evidence：139
- 去重 Passage：39
- 命中 Paper：65
- 原始观测：190
- 带机械噪声标记的观测：0
