<!-- CRL_RESEARCH_SEARCH_META {"created_at_utc":"2026-08-16T08:45:38.583003Z","request_fingerprint_sha256":"4ff0cda0407af6c3eb3243b033094860995f83cf2738861da3185fbccb752dd0","result_json_sha256":"3150beaa8af14eeeebdfc20fa91d96bf631816ca975591ee0f4af074fcbcd93b","search_id":"broad-frontier-001"} -->
# 研究检索导航

> 本报告仅展示查询路线、来源、命中定位与覆盖；所有科研判断由主研究者完成。

- 搜索标识：`broad-frontier-001`
- 生成时间（协调世界时）：`2026-08-16T08:45:38.583003Z`

## 紧凑研究地图

> 跨路线按 Paper 去重；每个查询路线至多选一个尚未出现的最高排名代表项。完整原始命中保留在 `result.json`。

- Paper `P038` · AgentDojo: A Dynamic Environment to Evaluate Prompt Injection Attacks and Defenses for LLM Agents；用途 `problem`；路线 `q001:paper_card_fts` #1；Card `paper-p038`（paper）；Evidence `ev-p038-operator-core`
- Paper `P004` · TravelPlanner: A Benchmark for Real-World Planning with Language Agents；用途 `problem`；路线 `q001:failure_card_fts` #1；Card `failure-constrained-plan-surface-validity`（failure）；Evidence `ev-p004-failure-core`, `ev-p004-macro-constraint-failure`
- Paper `P040` · From Confident Closing to Silent Failure: Characterizing False Success in LLM Agents；用途 `problem`；路线 `q001:passage_hybrid` #1；Passage `P040:p0001:s0002`
- Paper `P026` · Agent Lightning: Train ANY AI Agents with Reinforcement Learning；用途 `problem`；路线 `q001:operator_card_fts` #1；Card `operator-anchor-state-relative-credit`（operator）；Evidence `ev-p026-uniform-terminal-return`
- Paper `P025` · Unlocking the Power of Multi-Agent LLM for Reasoning: From Lazy Agents to Deliberation；用途 `failure`；路线 `q002:failure_card_fts` #1；Card `failure-lazy-agent-effective-single-agent-collapse`（failure）；Evidence `ev-p025-failure-core`
- Paper `P084` · On the Robustness of Agentic Function Calling；用途 `failure`；路线 `q002:passage_hybrid` #1；Passage `P084:p0002:s0001`
- Paper `P037` · ToolSandbox: A Stateful, Conversational, Interactive Evaluation Benchmark for LLM Tool Use Capabilities；用途 `failure`；路线 `q002:operator_card_fts` #1；Card `operator-milestone-dag-trajectory-evaluation`（operator）；Evidence `ev-p037-evaluation-core`, `ev-p037-minefield-violation`
- Paper `P001` · ReAct: Synergizing Reasoning and Acting in Language Models；用途 `failure`；路线 `q002:paper_card_fts` #1；Card `paper-react`（paper）；Evidence `ev-p001-react-interleaved`, `ev-p001-search-hallucination-boundary`
- Paper `P027` · Verified Critical Step Optimization for LLM Agents；用途 `operator`；路线 `q003:operator_card_fts` #1；Card `operator-verified-single-branch-repair`（operator）；Evidence `ev-p027-operator-core`
- Paper `P006` · An LLM Compiler for Parallel Function Calling；用途 `operator`；路线 `q003:paper_card_fts` #2；Card `paper-llmcompiler`（paper）；Evidence `ev-p006-dependency-dag-dispatch`, `ev-p006-shared-prompt-comparison-boundary`, `ev-p006-token-cost-accounting`
- Paper `P017` · Understanding the Information Propagation Effects of Communication Topologies in LLM-based Multi-Agent Systems；用途 `operator`；路线 `q003:passage_hybrid` #3；Passage `P017:p0003:s0001`
- Paper `P062` · Agentic Memory: Learning Unified Long-Term and Short-Term Memory Management for Large Language Model Agents；用途 `operator`；路线 `q003:failure_card_fts` #1；Card `failure-unified-memory-policy-retains-terminal-credit-smearing`（failure）；Evidence `ev-p062-broadcast-advantage`, `ev-p062-unified-memory-action-policy`
- Paper `P074` · ToolGate: Contract-Grounded and Verified Tool Execution for LLMs；用途 `prior`；路线 `q004:paper_card_fts` #1；Card `paper-p074`（paper）；Evidence `ev-p074-contract-state-commit`, `ev-p074-missing-schema-true-postcondition`
- Paper `P007` · tau-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains；用途 `prior`；路线 `q004:operator_card_fts` #1；Card `operator-terminal-state-reliability-evaluation`（operator）；Evidence `ev-p007-terminal-state-evaluation`
- Paper `P081` · Self-Consistency Improves Chain of Thought Reasoning in Language Models；用途 `prior`；路线 `q004:failure_card_fts` #4；Card `failure-interactive-gains-collapse-against-independent-sampling`（failure）；Evidence `ev-p081-fixed-answer-space-boundary`, `ev-p081-forty-sample-baseline`, `ev-p081-independent-path-majority-aggregation`
- Paper `P046` · Solver-Aided Verification of Policy Compliance in Tool-Augmented LLM Agents；用途 `prior`；路线 `q004:passage_hybrid` #2；Passage `P046:p0003:s0001`
- Paper `P066` · The Berkeley Function Calling Leaderboard (BFCL): From Tool Use to Agentic Evaluation of Large Language Models；用途 `measurement`；路线 `q005:paper_card_fts` #4；Card `paper-p066`（paper）；Evidence `ev-p066-multiturn-state-evaluation`, `ev-p066-single-to-stateful-gap`
- Paper `P068` · DeepFact: Co-Evolving Benchmarks and Agents for Deep Research Factuality；用途 `measurement`；路线 `q005:passage_hybrid` #1；Passage `P068:p0031:s0001`
- Paper `P054` · On the Limit of Language Models as Planning Formalizers；用途 `measurement`；路线 `q005:failure_card_fts` #2；Card `failure-constraint-shift-breaks-formalization`（failure）；Evidence `ev-p054-natural-language-implicit-predicate-failure`
- Paper `P067` · AgentHarm: A Benchmark for Measuring Harmfulness of LLM Agents；用途 `measurement`；路线 `q005:operator_card_fts` #2；Card `operator-capability-preserving-agent-safety-evaluation`（operator）；Evidence `ev-p067-agentic-harm-not-chat-refusal`, `ev-p067-capability-preserving-safety`

- 代表项：20 / 去重 Paper：70

## 查询与路线覆盖

### q001 · problem

- 原始查询：`tool-using LLM agents silently fail to verify environment state after actions`
- 规范化查询：`"tool" OR "using" OR "LLM" OR "agents" OR "silently" OR "fail" OR "to" OR "verify" OR "environment" OR "state" OR "after" OR "actions"`
- 路线 `paper_card_fts`：12 条；降级 false（无）
- 路线 `failure_card_fts`：12 条；降级 false（无）
- 路线 `passage_hybrid`：18 条；降级 false（无）
- 路线 `operator_card_fts`：12 条；降级 false（无）

### q002 · failure

- 原始查询：`semantically equivalent tool outputs cause divergent agent actions`
- 规范化查询：`"semantically" OR "equivalent" OR "tool" OR "outputs" OR "cause" OR "divergent" OR "agent" OR "actions"`
- 路线 `failure_card_fts`：12 条；降级 false（无）
- 路线 `passage_hybrid`：18 条；降级 false（无）
- 路线 `operator_card_fts`：12 条；降级 false（无）
- 路线 `paper_card_fts`：12 条；降级 false（无）

### q003 · operator

- 原始查询：`counterfactual replay intervention tool observations causal dependence`
- 规范化查询：`"counterfactual" OR "replay" OR "intervention" OR "tool" OR "observations" OR "causal" OR "dependence"`
- 路线 `operator_card_fts`：12 条；降级 false（无）
- 路线 `paper_card_fts`：12 条；降级 false（无）
- 路线 `passage_hybrid`：18 条；降级 false（无）
- 路线 `failure_card_fts`：12 条；降级 false（无）

### q004 · prior

- 原始查询：`tool agent reliability postcondition verification transactional state consistency benchmark`
- 规范化查询：`"tool" OR "agent" OR "reliability" OR "postcondition" OR "verification" OR "transactional" OR "state" OR "consistency" OR "benchmark"`
- 路线 `paper_card_fts`：12 条；降级 false（无）
- 路线 `operator_card_fts`：12 条；降级 false（无）
- 路线 `failure_card_fts`：12 条；降级 false（无）
- 路线 `passage_hybrid`：18 条；降级 false（无）

### q005 · measurement

- 原始查询：`causal faithfulness tool use counterfactual evaluation action validity`
- 规范化查询：`"causal" OR "faithfulness" OR "tool" OR "use" OR "counterfactual" OR "evaluation" OR "action" OR "validity"`
- 路线 `paper_card_fts`：12 条；降级 false（无）
- 路线 `passage_hybrid`：18 条；降级 false（无）
- 路线 `failure_card_fts`：12 条；降级 false（无）
- 路线 `operator_card_fts`：12 条；降级 false（无）

## 覆盖诊断

- 去重 Card：106
- 去重 Evidence：141
- 去重 Passage：82
- 命中 Paper：70
- 原始观测：270
- 带机械噪声标记的观测：1
