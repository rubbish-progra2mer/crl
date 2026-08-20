<!-- CRL_RESEARCH_SEARCH_META {"created_at_utc":"2026-08-13T07:53:27.126269Z","request_fingerprint_sha256":"42cfba4217a1461fcbd5e6795c6fa2e63a14f1df3fc39a08e71688d7020c021c","result_json_sha256":"27f1ae5d7db8be56959f5d89e8d96516e8ff716f200b82053fc13342ba9ac69d","search_id":"prior-operator-collision-001"} -->
# 研究检索导航

> 本报告仅展示查询路线、来源、命中定位与覆盖；所有科研判断由主研究者完成。

- 搜索标识：`prior-operator-collision-001`
- 生成时间（协调世界时）：`2026-08-13T07:53:27.126269Z`

## 紧凑研究地图

> 跨路线按 Paper 去重；每个查询路线至多选一个尚未出现的最高排名代表项。完整原始命中保留在 `result.json`。

- Paper `P019` · STeCa: Step-level Trajectory Calibration for LLM Agent Learning；用途 `prior`；路线 `q001:paper_card_fts` #1；Card `paper-p019`（paper）；Evidence `ev-p019-ground-truth-calibration-oracle`, `ev-p019-step-level-calibration`
- Paper `P025` · Unlocking the Power of Multi-Agent LLM for Reasoning: From Lazy Agents to Deliberation；用途 `prior`；路线 `q001:operator_card_fts` #1；Card `operator-grouped-masked-history-step-credit`（operator）；Evidence `ev-p025-failure-core`, `ev-p025-grouped-step-influence`
- Paper `P033` · Self-Refine: Iterative Refinement with Self-Feedback；用途 `prior`；路线 `q001:failure_card_fts` #1；Card `failure-iterative-refinement-corrupts-correct-output`（failure）；Evidence `ev-p033-operator-core`
- Paper `P040` · From Confident Closing to Silent Failure: Characterizing False Success in LLM Agents；用途 `prior`；路线 `q001:passage_hybrid` #1；Passage `P040:p0002:s0002`
- Paper `P097` · ReLoop: Structured Modeling and Behavioral Verification for Reliable LLM-Based Optimization；用途 `operator`；路线 `q002:operator_card_fts` #1；Card `operator-behavioral-perturbation-existence-test`（operator）；Evidence `ev-p097-behavioral-perturbation`, `ev-p097-feasibility-gap`
- Paper `P074` · ToolGate: Contract-Grounded and Verified Tool Execution for LLMs；用途 `operator`；路线 `q002:paper_card_fts` #2；Card `paper-p074`（paper）；Evidence `ev-p074-contract-state-commit`, `ev-p074-missing-schema-true-postcondition`
- Paper `P046` · Solver-Aided Verification of Policy Compliance in Tool-Augmented LLM Agents；用途 `operator`；路线 `q002:passage_hybrid` #3；Passage `P046:p0003:s0001`
- Paper `P095` · Don't Ask the LLM to Track Freshness: A Deterministic Recipe for Memory Conflict Resolution；用途 `operator`；路线 `q002:failure_card_fts` #1；Card `failure-llm-freshness-judgment-prior-override-and-drift`（failure）；Evidence `ev-p095-matched-comparison`, `ev-p095-prior-override-drift`

- 代表项：8 / 去重 Paper：77

## 查询与路线覆盖

### q001 · prior

- 原始查询：`tool-using LLM agent semantic incorrect tool output selective verification rollback replanning trajectory fault localization budgeted self-correction`
- 规范化查询：`"tool" OR "using" OR "LLM" OR "agent" OR "semantic" OR "incorrect" OR "output" OR "selective" OR "verification" OR "rollback" OR "replanning" OR "trajectory" OR "fault" OR "localization" OR "budgeted" OR "self" OR "correction"`
- 路线 `paper_card_fts`：30 条；降级 false（无）
- 路线 `operator_card_fts`：30 条；降级 false（无）
- 路线 `failure_card_fts`：30 条；降级 false（无）
- 路线 `passage_hybrid`：30 条；降级 false（无）

### q002 · operator

- 原始查询：`selective verification execution checking rollback replanning state drift causal fault localization budgeted recovery`
- 规范化查询：`"selective" OR "verification" OR "execution" OR "checking" OR "rollback" OR "replanning" OR "state" OR "drift" OR "causal" OR "fault" OR "localization" OR "budgeted" OR "recovery"`
- 路线 `operator_card_fts`：30 条；降级 false（无）
- 路线 `paper_card_fts`：30 条；降级 false（无）
- 路线 `passage_hybrid`：30 条；降级 false（无）
- 路线 `failure_card_fts`：25 条；降级 false（无）

## 覆盖诊断

- 去重 Card：126
- 去重 Evidence：157
- 去重 Passage：53
- 命中 Paper：77
- 原始观测：235
- 带机械噪声标记的观测：0
