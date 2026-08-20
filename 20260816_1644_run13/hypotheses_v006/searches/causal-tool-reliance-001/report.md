<!-- CRL_RESEARCH_SEARCH_META {"created_at_utc":"2026-08-16T09:27:36.743866Z","request_fingerprint_sha256":"2ad6ab6bb319edf40ddef6ace260bda4e1078e43fea7e4a3f759ce397e161fd7","result_json_sha256":"334ccccc48b249f8c5ed71b60f352b30dcbe412c8dd3c32f7119c6f4fe21ced5","search_id":"causal-tool-reliance-001"} -->
# 研究检索导航

> 本报告仅展示查询路线、来源、命中定位与覆盖；所有科研判断由主研究者完成。

- 搜索标识：`causal-tool-reliance-001`
- 生成时间（协调世界时）：`2026-08-16T09:27:36.743866Z`

## 紧凑研究地图

> 跨路线按 Paper 去重；每个查询路线至多选一个尚未出现的最高排名代表项。完整原始命中保留在 `result.json`。

- Paper `P027` · Verified Critical Step Optimization for LLM Agents；用途 `problem`；路线 `q001:paper_card_fts` #1；Card `paper-p027`（paper）；Evidence `ev-p027-operator-core`
- Paper `P039` · ToolFailBench: Diagnosing Tool-Use Failures in LLM Agents；用途 `problem`；路线 `q001:failure_card_fts` #1；Card `failure-tool-use-metrics-collapse-distinct-errors`（failure）；Evidence `ev-p039-aggregate-score-masking`, `ev-p039-failure-core`
- Paper `P008` · Agent Security Bench (ASB): Formalizing and Benchmarking Attacks and Defenses in LLM-based Agents；用途 `problem`；路线 `q001:passage_hybrid` #2；Passage `P008:p0023:s0001`
- Paper `P021` · In-the-Flow Agentic System Optimization for Effective Planning and Tool Use；用途 `problem`；路线 `q001:operator_card_fts` #1；Card `operator-outcome-trained-execution-state-planner`（operator）；Evidence `ev-p021-operator-core`
- Paper `P025` · Unlocking the Power of Multi-Agent LLM for Reasoning: From Lazy Agents to Deliberation；用途 `failure`；路线 `q002:failure_card_fts` #1；Card `failure-lazy-agent-effective-single-agent-collapse`（failure）；Evidence `ev-p025-failure-core`
- Paper `P072` · Structured Uncertainty guided Clarification for LLM Agents；用途 `failure`；路线 `q002:passage_hybrid` #1；Passage `P072:p0005:s0001`
- Paper `P079` · Learning to Contextualize Web Pages for Enhanced Decision Making by LLM Agents；用途 `failure`；路线 `q002:operator_card_fts` #1；Card `operator-action-preserving-observation-contextualization`（operator）；Evidence `ev-p079-action-conditioned-contextualization`, `ev-p079-ground-truth-action-retry`, `ev-p079-unseen-ui-boundary`
- Paper `P033` · Self-Refine: Iterative Refinement with Self-Feedback；用途 `failure`；路线 `q002:paper_card_fts` #1；Card `paper-p033`（paper）；Evidence `ev-p033-operator-core`
- Paper `P074` · ToolGate: Contract-Grounded and Verified Tool Execution for LLMs；用途 `operator`；路线 `q003:operator_card_fts` #1；Card `operator-contract-gated-tool-state-commit`（operator）；Evidence `ev-p074-contract-state-commit`, `ev-p074-missing-schema-true-postcondition`
- Paper `P005` · ToolLLM: Facilitating Large Language Models to Master 16000+ Real-world APIs；用途 `operator`；路线 `q003:paper_card_fts` #4；Card `paper-p005`（paper）；Evidence `ev-p005-operator-core`
- Paper `P046` · Solver-Aided Verification of Policy Compliance in Tool-Augmented LLM Agents；用途 `operator`；路线 `q003:passage_hybrid` #7；Passage `P046:p0001:s0003`
- Paper `P062` · Agentic Memory: Learning Unified Long-Term and Short-Term Memory Management for Large Language Model Agents；用途 `operator`；路线 `q003:failure_card_fts` #2；Card `failure-unified-memory-policy-retains-terminal-credit-smearing`（failure）；Evidence `ev-p062-broadcast-advantage`, `ev-p062-unified-memory-action-policy`
- Paper `P066` · The Berkeley Function Calling Leaderboard (BFCL): From Tool Use to Agentic Evaluation of Large Language Models；用途 `prior`；路线 `q004:paper_card_fts` #4；Card `paper-p066`（paper）；Evidence `ev-p066-multiturn-state-evaluation`, `ev-p066-single-to-stateful-gap`
- Paper `P028` · Memory-R1: Enhancing Large Language Model Agents to Manage and Utilize Memories via Reinforcement Learning；用途 `prior`；路线 `q004:operator_card_fts` #2；Card `operator-learned-memory-crud-control`（operator）；Evidence `ev-p028-operator-core`
- Paper `P036` · tau-Knowledge: Evaluating Conversational Agents over Unstructured Knowledge；用途 `prior`；路线 `q004:failure_card_fts` #2；Card `failure-gold-context-does-not-solve-knowledge-use`（failure）；Evidence `ev-p036-failure-core`
- Paper `P016` · Why Do Multi-Agent LLM Systems Fail?；用途 `prior`；路线 `q004:passage_hybrid` #3；Passage `P016:p0035:s0001`
- Paper `P030` · STALE: Can LLM Agents Know When Their Memories Are No Longer Valid?；用途 `measurement`；路线 `q005:paper_card_fts` #1；Card `paper-p030`（paper）；Evidence `ev-p030-failure-core`
- Paper `P049` · Reinforced Agent: Inference-Time Feedback for Tool-Calling Agents；用途 `measurement`；路线 `q005:passage_hybrid` #10；Passage `P049:p0011:s0001`
- Paper `P004` · TravelPlanner: A Benchmark for Real-World Planning with Language Agents；用途 `measurement`；路线 `q005:failure_card_fts` #1；Card `failure-constrained-plan-surface-validity`（failure）；Evidence `ev-p004-failure-core`, `ev-p004-macro-constraint-failure`
- Paper `P041` · LLM Agents Already Know When to Call Tools - Even Without Reasoning；用途 `measurement`；路线 `q005:operator_card_fts` #2；Card `operator-hidden-state-tool-necessity-prefill`（operator）；Evidence `ev-p041-operator-core`, `ev-p041-probe-prefill-steering`

- 代表项：20 / 去重 Paper：73

## 查询与路线覆盖

### q001 · problem

- 原始查询：`LLM agent calls a tool but final action does not causally depend on changed tool result outcome unfaithful post hoc tool use`
- 规范化查询：`"LLM" OR "agent" OR "calls" OR "a" OR "tool" OR "but" OR "final" OR "action" OR "does" OR "not" OR "causally" OR "depend" OR "on" OR "changed" OR "result" OR "outcome" OR "unfaithful" OR "post" OR "hoc" OR "use"`
- 路线 `paper_card_fts`：14 条；降级 false（无）
- 路线 `failure_card_fts`：14 条；降级 false（无）
- 路线 `passage_hybrid`：28 条；降级 false（无）
- 路线 `operator_card_fts`：14 条；降级 false（无）

### q002 · failure

- 原始查询：`counterfactual tool output perturbation changes evidence but agent keeps same action overtrust prior belief ignores observation`
- 规范化查询：`"counterfactual" OR "tool" OR "output" OR "perturbation" OR "changes" OR "evidence" OR "but" OR "agent" OR "keeps" OR "same" OR "action" OR "overtrust" OR "prior" OR "belief" OR "ignores" OR "observation"`
- 路线 `failure_card_fts`：14 条；降级 false（无）
- 路线 `passage_hybrid`：28 条；降级 false（无）
- 路线 `operator_card_fts`：14 条；降级 false（无）
- 路线 `paper_card_fts`：14 条；降级 false（无）

### q003 · operator

- 原始查询：`paired counterfactual replay verify action sensitivity to tool result before irreversible execution causal contract`
- 规范化查询：`"paired" OR "counterfactual" OR "replay" OR "verify" OR "action" OR "sensitivity" OR "to" OR "tool" OR "result" OR "before" OR "irreversible" OR "execution" OR "causal" OR "contract"`
- 路线 `operator_card_fts`：14 条；降级 false（无）
- 路线 `paper_card_fts`：14 条；降级 false（无）
- 路线 `passage_hybrid`：28 条；降级 false（无）
- 路线 `failure_card_fts`：14 条；降级 false（无）

### q004 · prior

- 原始查询：`causal faithfulness tool use counterfactual intervention outcome reliance verification agent decision`
- 规范化查询：`"causal" OR "faithfulness" OR "tool" OR "use" OR "counterfactual" OR "intervention" OR "outcome" OR "reliance" OR "verification" OR "agent" OR "decision"`
- 路线 `paper_card_fts`：14 条；降级 false（无）
- 路线 `operator_card_fts`：14 条；降级 false（无）
- 路线 `failure_card_fts`：14 条；降级 false（无）
- 路线 `passage_hybrid`：28 条；降级 false（无）

### q005 · measurement

- 原始查询：`hold prompt and tool call fixed swap valid result values measure action sensitivity and correctness`
- 规范化查询：`"hold" OR "prompt" OR "and" OR "tool" OR "call" OR "fixed" OR "swap" OR "valid" OR "result" OR "values" OR "measure" OR "action" OR "sensitivity" OR "correctness"`
- 路线 `paper_card_fts`：14 条；降级 false（无）
- 路线 `passage_hybrid`：28 条；降级 false（无）
- 路线 `failure_card_fts`：14 条；降级 false（无）
- 路线 `operator_card_fts`：14 条；降级 false（无）

## 覆盖诊断

- 去重 Card：113
- 去重 Evidence：150
- 去重 Passage：112
- 命中 Paper：73
- 原始观测：350
- 带机械噪声标记的观测：0
