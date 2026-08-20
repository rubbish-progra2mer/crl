<!-- CRL_RESEARCH_SEARCH_META {"created_at_utc":"2026-08-13T07:52:29.873212Z","request_fingerprint_sha256":"86e71800ce3d546d1ab89e601e693626a1611651691b724a286a861914561ff5","result_json_sha256":"5836acb231732b7bb77656670f5fb8e5f8ab8b421ed36a6e66d3fa8a8a2e0234","search_id":"landscape_v001"} -->
# 研究检索导航

> 本报告仅展示查询路线、来源、命中定位与覆盖；所有科研判断由主研究者完成。

- 搜索标识：`landscape_v001`
- 生成时间（协调世界时）：`2026-08-13T07:52:29.873212Z`

## 紧凑研究地图

> 跨路线按 Paper 去重；每个查询路线至多选一个尚未出现的最高排名代表项。完整原始命中保留在 `result.json`。

- Paper `P066` · The Berkeley Function Calling Leaderboard (BFCL): From Tool Use to Agentic Evaluation of Large Language Models；用途 `problem`；路线 `q001:paper_card_fts` #1；Card `paper-p066`（paper）；Evidence `ev-p066-multiturn-state-evaluation`, `ev-p066-single-to-stateful-gap`
- Paper `P071` · Agentic Plan Caching: Test-Time Memory for Fast and Cost-Efficient LLM Agents；用途 `problem`；路线 `q001:failure_card_fts` #2；Card `failure-plan-cache-semantic-false-positives`（failure）；Evidence `ev-p071-cache-false-positive-boundary`, `ev-p071-plan-template-reuse`
- Paper `P040` · From Confident Closing to Silent Failure: Characterizing False Success in LLM Agents；用途 `problem`；路线 `q001:passage_hybrid` #1；Passage `P040:p0010:s0003`
- Paper `P027` · Verified Critical Step Optimization for LLM Agents；用途 `problem`；路线 `q001:operator_card_fts` #1；Card `operator-verified-single-branch-repair`（operator）；Evidence `ev-p027-operator-core`
- Paper `P074` · ToolGate: Contract-Grounded and Verified Tool Execution for LLMs；用途 `failure`；路线 `q002:failure_card_fts` #1；Card `failure-incomplete-tool-contracts-false-verified-state`（failure）；Evidence `ev-p074-contract-state-commit`, `ev-p074-missing-schema-true-postcondition`
- Paper `P030` · STALE: Can LLM Agents Know When Their Memories Are No Longer Valid?；用途 `failure`；路线 `q002:passage_hybrid` #1；Passage `P030:p0010:s0001`
- Paper `P079` · Learning to Contextualize Web Pages for Enhanced Decision Making by LLM Agents；用途 `failure`；路线 `q002:operator_card_fts` #1；Card `operator-action-preserving-observation-contextualization`（operator）；Evidence `ev-p079-action-conditioned-contextualization`, `ev-p079-ground-truth-action-retry`, `ev-p079-unseen-ui-boundary`
- Paper `P091` · Temporal Validity in Retrieval Memory: Eliminating Stale-Fact Errors for AI Agents over Evolving Knowledge；用途 `failure`；路线 `q002:paper_card_fts` #2；Card `paper-p091`（paper）；Evidence `ev-p091-cosine-auroc`, `ev-p091-retain-fabrication`, `ev-p091-supersession-rule`
- Paper `P097` · ReLoop: Structured Modeling and Behavioral Verification for Reliable LLM-Based Optimization；用途 `operator`；路线 `q003:operator_card_fts` #1；Card `operator-behavioral-perturbation-existence-test`（operator）；Evidence `ev-p097-behavioral-perturbation`, `ev-p097-feasibility-gap`
- Paper `P016` · Why Do Multi-Agent LLM Systems Fail?；用途 `operator`；路线 `q003:paper_card_fts` #1；Card `paper-p016`（paper）；Evidence `ev-p016-intervention-residual-failures`, `ev-p016-mast-taxonomy`
- Paper `P046` · Solver-Aided Verification of Policy Compliance in Tool-Augmented LLM Agents；用途 `operator`；路线 `q003:passage_hybrid` #2；Passage `P046:p0003:s0001`
- Paper `P033` · Self-Refine: Iterative Refinement with Self-Feedback；用途 `operator`；路线 `q003:failure_card_fts` #1；Card `failure-iterative-refinement-corrupts-correct-output`（failure）；Evidence `ev-p033-operator-core`
- Paper `P013` · Large Language Models Cannot Self-Correct Reasoning Yet；用途 `prior`；路线 `q004:paper_card_fts` #2；Card `paper-p013`（paper）；Evidence `ev-p013-intrinsic-self-correction-degrades`, `ev-p013-oracle-free-equal-budget-boundary`
- Paper `P073` · Uncertainty Calibration for Tool-Using Language Agents；用途 `prior`；路线 `q004:operator_card_fts` #1；Card `operator-execution-supervised-prompt-trace-calibration`（operator）；Evidence `ev-p073-execution-supervised-probe`, `ev-p073-internal-confidence-misalignment`
- Paper `P096` · VeriSimpl: Robust Optimization Modeling from Natural Language using Simplification-based Verification；用途 `prior`；路线 `q004:failure_card_fts` #3；Card `failure-generator-aligned-verification-passes-shared-misreads`（failure）；Evidence `ev-p096-shared-misinterpretation`, `ev-p096-simplification-inversion`
- Paper `P032` · CRITIC: Large Language Models Can Self-Correct with Tool-Interactive Critiquing；用途 `prior`；路线 `q004:passage_hybrid` #2；Passage `P032:p0002:s0001`
- Paper `P076` · Multi-Agent Systems Execute Arbitrary Malicious Code；用途 `measurement`；路线 `q005:paper_card_fts` #2；Card `paper-p076`（paper）；Evidence `ev-p076-controlled-lab-boundary`, `ev-p076-metadata-control-flow-laundering`, `ev-p076-refusal-not-system-safety`
- Paper `P039` · ToolFailBench: Diagnosing Tool-Use Failures in LLM Agents；用途 `measurement`；路线 `q005:passage_hybrid` #3；Passage `P039:p0007:s0002`
- Paper `P026` · Agent Lightning: Train ANY AI Agents with Reinforcement Learning；用途 `measurement`；路线 `q005:failure_card_fts` #2；Card `failure-uniform-terminal-return-erases-step-credit`（failure）；Evidence `ev-p026-transition-decomposition`, `ev-p026-uniform-terminal-return`
- Paper `P025` · Unlocking the Power of Multi-Agent LLM for Reasoning: From Lazy Agents to Deliberation；用途 `measurement`；路线 `q005:operator_card_fts` #1；Card `operator-grouped-masked-history-step-credit`（operator）；Evidence `ev-p025-failure-core`, `ev-p025-grouped-step-influence`

- 代表项：20 / 去重 Paper：75

## 查询与路线覆盖

### q001 · problem

- 原始查询：`tool-using LLM agent silent semantic tool-output error long-horizon state drift`
- 规范化查询：`"tool" OR "using" OR "LLM" OR "agent" OR "silent" OR "semantic" OR "output" OR "error" OR "long" OR "horizon" OR "state" OR "drift"`
- 路线 `paper_card_fts`：12 条；降级 false（无）
- 路线 `failure_card_fts`：12 条；降级 false（无）
- 路线 `passage_hybrid`：12 条；降级 false（无）
- 路线 `operator_card_fts`：12 条；降级 false（无）

### q002 · failure

- 原始查询：`syntactically successful but semantically incorrect stale incomplete tool observation cascading failure`
- 规范化查询：`"syntactically" OR "successful" OR "but" OR "semantically" OR "incorrect" OR "stale" OR "incomplete" OR "tool" OR "observation" OR "cascading" OR "failure"`
- 路线 `failure_card_fts`：12 条；降级 false（无）
- 路线 `passage_hybrid`：12 条；降级 false（无）
- 路线 `operator_card_fts`：12 条；降级 false（无）
- 路线 `paper_card_fts`：12 条；降级 false（无）

### q003 · operator

- 原始查询：`selective verification rollback replanning trajectory consistency budgeted diagnosis`
- 规范化查询：`"selective" OR "verification" OR "rollback" OR "replanning" OR "trajectory" OR "consistency" OR "budgeted" OR "diagnosis"`
- 路线 `operator_card_fts`：12 条；降级 false（无）
- 路线 `paper_card_fts`：12 条；降级 false（无）
- 路线 `passage_hybrid`：12 条；降级 false（无）
- 路线 `failure_card_fts`：12 条；降级 false（无）

### q004 · prior

- 原始查询：`LLM tool agent execution verification self-correction tool error recovery`
- 规范化查询：`"LLM" OR "tool" OR "agent" OR "execution" OR "verification" OR "self" OR "correction" OR "error" OR "recovery"`
- 路线 `paper_card_fts`：12 条；降级 false（无）
- 路线 `operator_card_fts`：12 条；降级 false（无）
- 路线 `failure_card_fts`：12 条；降级 false（无）
- 路线 `passage_hybrid`：12 条；降级 false（无）

### q005 · measurement

- 原始查询：`controlled semantic tool fault injection independent terminal success multi-step agent benchmark`
- 规范化查询：`"controlled" OR "semantic" OR "tool" OR "fault" OR "injection" OR "independent" OR "terminal" OR "success" OR "multi" OR "step" OR "agent" OR "benchmark"`
- 路线 `paper_card_fts`：12 条；降级 false（无）
- 路线 `passage_hybrid`：12 条；降级 false（无）
- 路线 `failure_card_fts`：12 条；降级 false（无）
- 路线 `operator_card_fts`：12 条；降级 false（无）

## 覆盖诊断

- 去重 Card：118
- 去重 Evidence：156
- 去重 Passage：56
- 命中 Paper：75
- 原始观测：240
- 带机械噪声标记的观测：0
