<!-- CRL_RESEARCH_SEARCH_META {"created_at_utc":"2026-08-16T09:10:09.557077Z","request_fingerprint_sha256":"48175597bdfee778b72bec456bf862f7224051f6b966c8f24903dd5903feb7f2","result_json_sha256":"5d78e0f18ad08ca36e8515ed70e3e19b0433d40d5b2454241cd4844a57af4c67","search_id":"parallel-result-order-001"} -->
# 研究检索导航

> 本报告仅展示查询路线、来源、命中定位与覆盖；所有科研判断由主研究者完成。

- 搜索标识：`parallel-result-order-001`
- 生成时间（协调世界时）：`2026-08-16T09:10:09.557077Z`

## 紧凑研究地图

> 跨路线按 Paper 去重；每个查询路线至多选一个尚未出现的最高排名代表项。完整原始命中保留在 `result.json`。

- Paper `P006` · An LLM Compiler for Parallel Function Calling；用途 `problem`；路线 `q001:paper_card_fts` #1；Card `paper-llmcompiler`（paper）；Evidence `ev-p006-dependency-dag-dispatch`, `ev-p006-shared-prompt-comparison-boundary`, `ev-p006-token-cost-accounting`
- Paper `P069` · Tool Preferences in Agentic LLMs are Unreliable；用途 `problem`；路线 `q001:failure_card_fts` #1；Card `failure-tool-description-and-order-bias`（failure）；Evidence `ev-p069-description-induced-preference`, `ev-p069-identical-tool-order-bias`
- Paper `P037` · ToolSandbox: A Stateful, Conversational, Interactive Evaluation Benchmark for LLM Tool Use Capabilities；用途 `problem`；路线 `q001:passage_hybrid` #3；Passage `P037:p0016:s0001`
- Paper `P026` · Agent Lightning: Train ANY AI Agents with Reinforcement Learning；用途 `problem`；路线 `q001:operator_card_fts` #1；Card `operator-anchor-state-relative-credit`（operator）；Evidence `ev-p026-uniform-terminal-return`
- Paper `P060` · Unifying Inference-Time Planning Language Generation；用途 `operator`；路线 `q002:operator_card_fts` #1；Card `operator-syntax-aligned-formal-ir-planning`（operator）；Evidence `ev-p060-formal-ir-solver`, `ev-p060-ir-result-and-nl-failure`
- Paper `P095` · Don't Ask the LLM to Track Freshness: A Deterministic Recipe for Memory Conflict Resolution；用途 `operator`；路线 `q002:paper_card_fts` #2；Card `paper-p095`（paper）；Evidence `ev-p095-matched-comparison`, `ev-p095-prior-override-drift`
- Paper `P020` · AgentTTS: Large Language Model Agent for Test-time Compute-optimal Scaling Strategy in Complex Tasks；用途 `operator`；路线 `q002:passage_hybrid` #11；Passage `P020:p0036:s0001`
- Paper `P017` · Understanding the Information Propagation Effects of Communication Topologies in LLM-based Multi-Agent Systems；用途 `operator`；路线 `q002:failure_card_fts` #3；Card `failure-sparse-topology-suppresses-correct-insight`（failure）；Evidence `ev-p017-failure-core`
- Paper `P022` · MOC: Multi-Order Communication in LLM-based Multi-Agent Systems；用途 `prior`；路线 `q003:paper_card_fts` #3；Card `paper-p022`（paper）；Evidence `ev-p022-operator-core`
- Paper `P097` · ReLoop: Structured Modeling and Behavioral Verification for Reliable LLM-Based Optimization；用途 `prior`；路线 `q003:operator_card_fts` #2；Card `operator-behavioral-perturbation-existence-test`（operator）；Evidence `ev-p097-behavioral-perturbation`, `ev-p097-feasibility-gap`
- Paper `P066` · The Berkeley Function Calling Leaderboard (BFCL): From Tool Use to Agentic Evaluation of Large Language Models；用途 `prior`；路线 `q003:failure_card_fts` #2；Card `failure-single-turn-tool-score-overstates-agent-competence`（failure）；Evidence `ev-p066-multiturn-state-evaluation`, `ev-p066-single-to-stateful-gap`
- Paper `P086` · Meta-Tool: Unleash Open-World Function Calling Capabilities of General-Purpose Large Language Models；用途 `prior`；路线 `q003:passage_hybrid` #14；Passage `P086:p0007:s0001`
- Paper `P079` · Learning to Contextualize Web Pages for Enhanced Decision Making by LLM Agents；用途 `measurement`；路线 `q004:paper_card_fts` #2；Card `paper-p079`（paper）；Evidence `ev-p079-action-conditioned-contextualization`, `ev-p079-ground-truth-action-retry`, `ev-p079-unseen-ui-boundary`
- Paper `P008` · Agent Security Bench (ASB): Formalizing and Benchmarking Attacks and Defenses in LLM-based Agents；用途 `measurement`；路线 `q004:passage_hybrid` #1；Passage `P008:p0023:s0001`
- Paper `P053` · Language Models as Higher-Order Planning Formalizers；用途 `measurement`；路线 `q004:failure_card_fts` #3；Card `failure-grounded-formalization-output-expansion`（failure）；Evidence `ev-p053-higher-order-generator`, `ev-p053-parser-evaluation-boundary`, `ev-p053-pattern-review-confound`
- Paper `P021` · In-the-Flow Agentic System Optimization for Effective Planning and Tool Use；用途 `measurement`；路线 `q004:operator_card_fts` #2；Card `operator-outcome-trained-execution-state-planner`（operator）；Evidence `ev-p021-operator-core`

- 代表项：16 / 去重 Paper：68

## 查询与路线覆盖

### q001 · problem

- 原始查询：`parallel tool calls return identical results in different asynchronous completion orders and change agent decision`
- 规范化查询：`"parallel" OR "tool" OR "calls" OR "return" OR "identical" OR "results" OR "in" OR "different" OR "asynchronous" OR "completion" OR "orders" OR "and" OR "change" OR "agent" OR "decision"`
- 路线 `paper_card_fts`：12 条；降级 false（无）
- 路线 `failure_card_fts`：12 条；降级 false（无）
- 路线 `passage_hybrid`：24 条；降级 false（无）
- 路线 `operator_card_fts`：12 条；降级 false（无）

### q002 · operator

- 原始查询：`permutation invariant aggregation deterministic plan indexed result frames for parallel tool observations`
- 规范化查询：`"permutation" OR "invariant" OR "aggregation" OR "deterministic" OR "plan" OR "indexed" OR "result" OR "frames" OR "for" OR "parallel" OR "tool" OR "observations"`
- 路线 `operator_card_fts`：12 条；降级 false（无）
- 路线 `paper_card_fts`：12 条；降级 false（无）
- 路线 `passage_hybrid`：24 条；降级 false（无）
- 路线 `failure_card_fts`：12 条；降级 false（无）

### q003 · prior

- 原始查询：`parallel function calling result order sensitivity asynchronous completion tool messages positional bias`
- 规范化查询：`"parallel" OR "function" OR "calling" OR "result" OR "order" OR "sensitivity" OR "asynchronous" OR "completion" OR "tool" OR "messages" OR "positional" OR "bias"`
- 路线 `paper_card_fts`：12 条；降级 false（无）
- 路线 `operator_card_fts`：12 条；降级 false（无）
- 路线 `failure_card_fts`：12 条；降级 false（无）
- 路线 `passage_hybrid`：24 条；降级 false（无）

### q004 · measurement

- 原始查询：`permute tool result message order while holding results calls and prompts fixed measure next action disagreement`
- 规范化查询：`"permute" OR "tool" OR "result" OR "message" OR "order" OR "while" OR "holding" OR "results" OR "calls" OR "and" OR "prompts" OR "fixed" OR "measure" OR "next" OR "action" OR "disagreement"`
- 路线 `paper_card_fts`：12 条；降级 false（无）
- 路线 `passage_hybrid`：24 条；降级 false（无）
- 路线 `failure_card_fts`：12 条；降级 false（无）
- 路线 `operator_card_fts`：12 条；降级 false（无）

## 覆盖诊断

- 去重 Card：99
- 去重 Evidence：147
- 去重 Passage：74
- 命中 Paper：68
- 原始观测：240
- 带机械噪声标记的观测：0
