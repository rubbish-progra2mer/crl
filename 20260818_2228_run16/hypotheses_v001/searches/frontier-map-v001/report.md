<!-- CRL_RESEARCH_SEARCH_META {"created_at_utc":"2026-08-18T14:29:22.248852Z","request_fingerprint_sha256":"3c5b1583645d68de9fc5a113280292f16547f05216c00ec55980e8adba6ce6e5","result_json_sha256":"64cdffe4f67972682070e30b754de8208edf0b2157e5c80eddeea226fe481540","search_id":"frontier-map-v001"} -->
# 研究检索导航

> 本报告仅展示查询路线、来源、命中定位与覆盖；所有科研判断由主研究者完成。

- 搜索标识：`frontier-map-v001`
- 生成时间（协调世界时）：`2026-08-18T14:29:22.248852Z`

## 紧凑研究地图

> 跨路线按 Paper 去重；每个查询路线至多选一个尚未出现的最高排名代表项。完整原始命中保留在 `result.json`。

- Paper `P073` · Uncertainty Calibration for Tool-Using Language Agents；用途 `problem`；路线 `q001:paper_card_fts` #1；Card `paper-p073`（paper）；Evidence `ev-p073-execution-supervised-probe`, `ev-p073-internal-confidence-misalignment`
- Paper `P033` · Self-Refine: Iterative Refinement with Self-Feedback；用途 `problem`；路线 `q001:failure_card_fts` #2；Card `failure-iterative-refinement-corrupts-correct-output`（failure）；Evidence `ev-p033-operator-core`
- Paper `P046` · Solver-Aided Verification of Policy Compliance in Tool-Augmented LLM Agents；用途 `problem`；路线 `q001:passage_hybrid` #1；Passage `P046:p0001:s0003`
- Paper `P041` · LLM Agents Already Know When to Call Tools - Even Without Reasoning；用途 `problem`；路线 `q001:operator_card_fts` #1；Card `operator-hidden-state-tool-necessity-prefill`（operator）；Evidence `ev-p041-operator-core`, `ev-p041-probe-prefill-steering`
- Paper `P064` · How Memory Management Impacts LLM Agents: An Empirical Study of Experience-Following Behavior；用途 `failure`；路线 `q002:failure_card_fts` #1；Card `failure-retrieved-experience-propagates-stored-errors`（failure）；Evidence `ev-p064-evaluator-reliability`, `ev-p064-experience-following-error`
- Paper `P040` · From Confident Closing to Silent Failure: Characterizing False Success in LLM Agents；用途 `failure`；路线 `q002:passage_hybrid` #1；Passage `P040:p0002:s0002`
- Paper `P037` · ToolSandbox: A Stateful, Conversational, Interactive Evaluation Benchmark for LLM Tool Use Capabilities；用途 `failure`；路线 `q002:operator_card_fts` #1；Card `operator-milestone-dag-trajectory-evaluation`（operator）；Evidence `ev-p037-evaluation-core`, `ev-p037-minefield-violation`
- Paper `P097` · ReLoop: Structured Modeling and Behavioral Verification for Reliable LLM-Based Optimization；用途 `failure`；路线 `q002:paper_card_fts` #2；Card `paper-p097`（paper）；Evidence `ev-p097-behavioral-perturbation`, `ev-p097-feasibility-gap`
- Paper `P016` · Why Do Multi-Agent LLM Systems Fail?；用途 `operator`；路线 `q003:operator_card_fts` #2；Card `operator-trace-failure-taxonomy`（operator）；Evidence `ev-p016-mast-taxonomy`
- Paper `P025` · Unlocking the Power of Multi-Agent LLM for Reasoning: From Lazy Agents to Deliberation；用途 `operator`；路线 `q003:paper_card_fts` #2；Card `paper-p025`（paper）；Evidence `ev-p025-failure-core`
- Paper `P072` · Structured Uncertainty guided Clarification for LLM Agents；用途 `operator`；路线 `q003:passage_hybrid` #2；Passage `P072:p0005:s0001`
- Paper `P094` · Evaluating Memory in LLM Agents via Incremental Multi-Turn Interactions；用途 `operator`；路线 `q003:failure_card_fts` #2；Card `failure-selective-forgetting-collapses-with-context-length`（failure）；Evidence `ev-p094-sf-guardrails`, `ev-p094-sf-length-collapse`
- Paper `P024` · Improving Factuality and Reasoning in Language Models through Multiagent Debate；用途 `prior`；路线 `q004:paper_card_fts` #1；Card `paper-p024`（paper）；Evidence `ev-p024-operator-core`
- Paper `P077` · ArCHer: Training Language Model Agents via Hierarchical Multi-Turn RL；用途 `prior`；路线 `q004:operator_card_fts` #1；Card `operator-hierarchical-utterance-critic-token-actor`（operator）；Evidence `ev-p077-hierarchical-utterance-critic-token-actor`, `ev-p077-oracle-reward-hacking-boundary`, `ev-p077-trajectory-only-sample-efficiency`
- Paper `P026` · Agent Lightning: Train ANY AI Agents with Reinforcement Learning；用途 `prior`；路线 `q004:failure_card_fts` #2；Card `failure-uniform-terminal-return-erases-step-credit`（failure）；Evidence `ev-p026-transition-decomposition`, `ev-p026-uniform-terminal-return`
- Paper `P019` · STeCa: Step-level Trajectory Calibration for LLM Agent Learning；用途 `prior`；路线 `q004:passage_hybrid` #1；Passage `P019:p0002:s0001`
- Paper `P035` · Holistic Agent Leaderboard: The Missing Infrastructure for AI Agent Evaluation；用途 `measurement`；路线 `q005:paper_card_fts` #1；Card `paper-p035`（paper）；Evidence `ev-p035-evaluation-core`
- Paper `P039` · ToolFailBench: Diagnosing Tool-Use Failures in LLM Agents；用途 `measurement`；路线 `q005:passage_hybrid` #1；Passage `P039:p0007:s0002`
- Paper `P070` · ProMCP: Profiling Token Flows and Latency Costs in Model Context Protocol-Based LLM Agents；用途 `measurement`；路线 `q005:failure_card_fts` #1；Card `failure-light-tool-runtime-bottleneck-overreach`（failure）；Evidence `ev-p070-light-tool-runtime-boundary`, `ev-p070-orchestration-bottleneck`, `ev-p070-six-stage-attribution`
- Paper `P001` · ReAct: Synergizing Reasoning and Acting in Language Models；用途 `measurement`；路线 `q005:operator_card_fts` #6；Card `operator-reason-action-interleaving`（operator）；Evidence `ev-p001-react-interleaved`

- 代表项：20 / 去重 Paper：73

## 查询与路线覆盖

### q001 · problem

- 原始查询：`tool-using language model agents partial observability hidden failure reliable execution`
- 规范化查询：`"tool" OR "using" OR "language" OR "model" OR "agents" OR "partial" OR "observability" OR "hidden" OR "failure" OR "reliable" OR "execution"`
- 路线 `paper_card_fts`：12 条；降级 false（无）
- 路线 `failure_card_fts`：12 条；降级 false（无）
- 路线 `passage_hybrid`：20 条；降级 false（无）
- 路线 `operator_card_fts`：12 条；降级 false（无）

### q002 · failure

- 原始查询：`LLM agent trajectory failure detection cascading errors recovery`
- 规范化查询：`"LLM" OR "agent" OR "trajectory" OR "failure" OR "detection" OR "cascading" OR "errors" OR "recovery"`
- 路线 `failure_card_fts`：12 条；降级 false（无）
- 路线 `passage_hybrid`：20 条；降级 false（无）
- 路线 `operator_card_fts`：12 条；降级 false（无）
- 路线 `paper_card_fts`：12 条；降级 false（无）

### q003 · operator

- 原始查询：`counterfactual replay execution trace uncertainty selective intervention`
- 规范化查询：`"counterfactual" OR "replay" OR "execution" OR "trace" OR "uncertainty" OR "selective" OR "intervention"`
- 路线 `operator_card_fts`：12 条；降级 false（无）
- 路线 `paper_card_fts`：12 条；降级 false（无）
- 路线 `passage_hybrid`：20 条；降级 false（无）
- 路线 `failure_card_fts`：12 条；降级 false（无）

### q004 · prior

- 原始查询：`agent process reward model trajectory verification error localization`
- 规范化查询：`"agent" OR "process" OR "reward" OR "model" OR "trajectory" OR "verification" OR "error" OR "localization"`
- 路线 `paper_card_fts`：12 条；降级 false（无）
- 路线 `operator_card_fts`：12 条；降级 false（无）
- 路线 `failure_card_fts`：12 条；降级 false（无）
- 路线 `passage_hybrid`：20 条；降级 false（无）

### q005 · measurement

- 原始查询：`tool agent failure attribution trace perturbation benchmark`
- 规范化查询：`"tool" OR "agent" OR "failure" OR "attribution" OR "trace" OR "perturbation" OR "benchmark"`
- 路线 `paper_card_fts`：12 条；降级 false（无）
- 路线 `passage_hybrid`：20 条；降级 false（无）
- 路线 `failure_card_fts`：12 条；降级 false（无）
- 路线 `operator_card_fts`：12 条；降级 false（无）

## 覆盖诊断

- 去重 Card：108
- 去重 Evidence：138
- 去重 Passage：88
- 命中 Paper：73
- 原始观测：280
- 带机械噪声标记的观测：0
