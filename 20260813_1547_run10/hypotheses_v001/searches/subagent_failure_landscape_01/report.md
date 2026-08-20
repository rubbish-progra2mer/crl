<!-- CRL_RESEARCH_SEARCH_META {"created_at_utc":"2026-08-13T07:53:27.099280Z","request_fingerprint_sha256":"245edd87cef4a725bd6cde1865f6847f90230ed1b01c996a89c03d61794856d4","result_json_sha256":"d27dc5f0139e88ad8bed508de54c3310eb9fc4093186803e3158c0df2d773587","search_id":"subagent_failure_landscape_01"} -->
# 研究检索导航

> 本报告仅展示查询路线、来源、命中定位与覆盖；所有科研判断由主研究者完成。

- 搜索标识：`subagent_failure_landscape_01`
- 生成时间（协调世界时）：`2026-08-13T07:53:27.099280Z`

## 紧凑研究地图

> 跨路线按 Paper 去重；每个查询路线至多选一个尚未出现的最高排名代表项。完整原始命中保留在 `result.json`。

- Paper `P064` · How Memory Management Impacts LLM Agents: An Empirical Study of Experience-Following Behavior；用途 `problem`；路线 `q001:paper_card_fts` #1；Card `paper-p064`（paper）；Evidence `ev-p064-evaluator-reliability`, `ev-p064-experience-following-error`
- Paper `P066` · The Berkeley Function Calling Leaderboard (BFCL): From Tool Use to Agentic Evaluation of Large Language Models；用途 `problem`；路线 `q001:failure_card_fts` #2；Card `failure-single-turn-tool-score-overstates-agent-competence`（failure）；Evidence `ev-p066-multiturn-state-evaluation`, `ev-p066-single-to-stateful-gap`
- Paper `P019` · STeCa: Step-level Trajectory Calibration for LLM Agent Learning；用途 `problem`；路线 `q001:passage_hybrid` #1；Passage `P019:p0001:s0001`
- Paper `P079` · Learning to Contextualize Web Pages for Enhanced Decision Making by LLM Agents；用途 `problem`；路线 `q001:operator_card_fts` #1；Card `operator-action-preserving-observation-contextualization`（operator）；Evidence `ev-p079-action-conditioned-contextualization`, `ev-p079-ground-truth-action-retry`, `ev-p079-unseen-ui-boundary`
- Paper `P074` · ToolGate: Contract-Grounded and Verified Tool Execution for LLMs；用途 `failure`；路线 `q002:failure_card_fts` #1；Card `failure-incomplete-tool-contracts-false-verified-state`（failure）；Evidence `ev-p074-contract-state-commit`, `ev-p074-missing-schema-true-postcondition`
- Paper `P039` · ToolFailBench: Diagnosing Tool-Use Failures in LLM Agents；用途 `failure`；路线 `q002:passage_hybrid` #1；Passage `P039:p0016:s0001`
- Paper `P037` · ToolSandbox: A Stateful, Conversational, Interactive Evaluation Benchmark for LLM Tool Use Capabilities；用途 `failure`；路线 `q002:operator_card_fts` #1；Card `operator-milestone-dag-trajectory-evaluation`（operator）；Evidence `ev-p037-evaluation-core`, `ev-p037-minefield-violation`
- Paper `P030` · STALE: Can LLM Agents Know When Their Memories Are No Longer Valid?；用途 `failure`；路线 `q002:paper_card_fts` #1；Card `paper-p030`（paper）；Evidence `ev-p030-failure-core`
- Paper `P060` · Unifying Inference-Time Planning Language Generation；用途 `failure`；路线 `q003:failure_card_fts` #3；Card `failure-natural-language-ir-hurts-formal-planning`（failure）；Evidence `ev-p060-formal-ir-solver`, `ev-p060-ir-result-and-nl-failure`
- Paper `P048` · NaviAgent: Graph-Driven Bilevel Planning for Scalable Tool Orchestration；用途 `failure`；路线 `q003:passage_hybrid` #2；Passage `P048:p0006:s0003`
- Paper `P003` · Language Agent Tree Search Unifies Reasoning, Acting, and Planning in Language Models；用途 `failure`；路线 `q003:operator_card_fts` #1；Card `operator-feedback-backpropagated-tree-search`（operator）；Evidence `ev-p003-search-control-loop`
- Paper `P021` · In-the-Flow Agentic System Optimization for Effective Planning and Tool Use；用途 `failure`；路线 `q003:paper_card_fts` #1；Card `paper-p021`（paper）；Evidence `ev-p021-operator-core`
- Paper `P040` · From Confident Closing to Silent Failure: Characterizing False Success in LLM Agents；用途 `measurement`；路线 `q004:paper_card_fts` #1；Card `paper-p040`（paper）；Evidence `ev-p040-failure-core`
- Paper `P072` · Structured Uncertainty guided Clarification for LLM Agents；用途 `measurement`；路线 `q004:passage_hybrid` #1；Passage `P072:p0025:s0001`
- Paper `P081` · Self-Consistency Improves Chain of Thought Reasoning in Language Models；用途 `measurement`；路线 `q004:failure_card_fts` #2；Card `failure-interactive-gains-collapse-against-independent-sampling`（failure）；Evidence `ev-p081-fixed-answer-space-boundary`, `ev-p081-forty-sample-baseline`, `ev-p081-independent-path-majority-aggregation`
- Paper `P087` · Tools Are Under-Documented: Simple Document Expansion Boosts Tool Retrieval；用途 `measurement`；路线 `q004:operator_card_fts` #2；Card `operator-grounded-structured-tool-document-expansion`（operator）；Evidence `ev-p087-fields-not-universally-beneficial`, `ev-p087-merge-and-semantic-judge`, `ev-p087-structured-query-independent-expansion`
- Paper `P097` · ReLoop: Structured Modeling and Behavioral Verification for Reliable LLM-Based Optimization；用途 `prior`；路线 `q005:paper_card_fts` #1；Card `paper-p097`（paper）；Evidence `ev-p097-behavioral-perturbation`, `ev-p097-feasibility-gap`
- Paper `P088` · Non-negative Elastic Net Decoding for Information Retrieval；用途 `prior`；路线 `q005:operator_card_fts` #2；Card `operator-joint-nonnegative-residual-retrieval`（operator）；Evidence `ev-p088-joint-nonnegative-objective`, `ev-p088-relevant-set-size-signature`, `ev-p088-theory-deployment-scale-boundary`
- Paper `P033` · Self-Refine: Iterative Refinement with Self-Feedback；用途 `prior`；路线 `q005:failure_card_fts` #1；Card `failure-iterative-refinement-corrupts-correct-output`（failure）；Evidence `ev-p033-operator-core`
- Paper `P027` · Verified Critical Step Optimization for LLM Agents；用途 `prior`；路线 `q005:passage_hybrid` #2；Passage `P027:p0001:s0001`

- 代表项：20 / 去重 Paper：85

## 查询与路线覆盖

### q001 · problem

- 原始查询：`long-horizon tool-using LLM agent semantic observation error state drift error propagation`
- 规范化查询：`"long" OR "horizon" OR "tool" OR "using" OR "LLM" OR "agent" OR "semantic" OR "observation" OR "error" OR "state" OR "drift" OR "propagation"`
- 路线 `paper_card_fts`：20 条；降级 false（无）
- 路线 `failure_card_fts`：20 条；降级 false（无）
- 路线 `passage_hybrid`：20 条；降级 false（无）
- 路线 `operator_card_fts`：20 条；降级 false（无）

### q002 · failure

- 原始查询：`tool returns syntactically valid but semantically wrong stale incomplete contradictory result silent failure`
- 规范化查询：`"tool" OR "returns" OR "syntactically" OR "valid" OR "but" OR "semantically" OR "wrong" OR "stale" OR "incomplete" OR "contradictory" OR "result" OR "silent" OR "failure"`
- 路线 `failure_card_fts`：20 条；降级 false（无）
- 路线 `passage_hybrid`：20 条；降级 false（无）
- 路线 `operator_card_fts`：20 条；降级 false（无）
- 路线 `paper_card_fts`：20 条；降级 false（无）

### q003 · failure

- 原始查询：`incorrect tool observation compounds through downstream planning trajectory execution`
- 规范化查询：`"incorrect" OR "tool" OR "observation" OR "compounds" OR "through" OR "downstream" OR "planning" OR "trajectory" OR "execution"`
- 路线 `failure_card_fts`：20 条；降级 false（无）
- 路线 `passage_hybrid`：20 条；降级 false（无）
- 路线 `operator_card_fts`：20 条；降级 false（无）
- 路线 `paper_card_fts`：20 条；降级 false（无）

### q004 · measurement

- 原始查询：`controlled semantic tool-output corruption fault injection independent terminal success recovery detection budget`
- 规范化查询：`"controlled" OR "semantic" OR "tool" OR "output" OR "corruption" OR "fault" OR "injection" OR "independent" OR "terminal" OR "success" OR "recovery" OR "detection" OR "budget"`
- 路线 `paper_card_fts`：20 条；降级 false（无）
- 路线 `passage_hybrid`：20 条；降级 false（无）
- 路线 `failure_card_fts`：20 条；降级 false（无）
- 路线 `operator_card_fts`：20 条；降级 false（无）

### q005 · prior

- 原始查询：`trajectory verification fault localization rollback recovery selective verification tool agent`
- 规范化查询：`"trajectory" OR "verification" OR "fault" OR "localization" OR "rollback" OR "recovery" OR "selective" OR "tool" OR "agent"`
- 路线 `paper_card_fts`：20 条；降级 false（无）
- 路线 `operator_card_fts`：20 条；降级 false（无）
- 路线 `failure_card_fts`：20 条；降级 false（无）
- 路线 `passage_hybrid`：20 条；降级 false（无）

## 覆盖诊断

- 去重 Card：160
- 去重 Evidence：184
- 去重 Passage：81
- 命中 Paper：85
- 原始观测：400
- 带机械噪声标记的观测：1
