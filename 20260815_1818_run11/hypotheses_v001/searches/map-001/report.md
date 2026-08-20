<!-- CRL_RESEARCH_SEARCH_META {"created_at_utc":"2026-08-15T10:20:35.636248Z","request_fingerprint_sha256":"fa2b87c831df2da3e986a531ef493c3f8d96c860b9d330ec0a3c2e6027cba21b","result_json_sha256":"b8dee043d95035205f60e820ed06df928541e8b04fb6044975d18ff28c546440","search_id":"map-001"} -->
# 研究检索导航

> 本报告仅展示查询路线、来源、命中定位与覆盖；所有科研判断由主研究者完成。

- 搜索标识：`map-001`
- 生成时间（协调世界时）：`2026-08-15T10:20:35.636248Z`

## 紧凑研究地图

> 跨路线按 Paper 去重；每个查询路线至多选一个尚未出现的最高排名代表项。完整原始命中保留在 `result.json`。

- Paper `P040` · From Confident Closing to Silent Failure: Characterizing False Success in LLM Agents；用途 `problem`；路线 `q001:paper_card_fts` #1；Card `paper-p040`（paper）；Evidence `ev-p040-failure-core`
- Paper `P007` · tau-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains；用途 `problem`；路线 `q001:failure_card_fts` #2；Card `failure-repeat-run-reliability-collapse`（failure）；Evidence `ev-p007-repeat-reliability-collapse`
- Paper `P016` · Why Do Multi-Agent LLM Systems Fail?；用途 `problem`；路线 `q001:passage_hybrid` #8；Passage `P016:p0007:s0002`
- Paper `P046` · Solver-Aided Verification of Policy Compliance in Tool-Augmented LLM Agents；用途 `problem`；路线 `q001:operator_card_fts` #1；Card `operator-smt-preexecution-policy-guard`（operator）；Evidence `ev-p046-operator-core`
- Paper `P097` · ReLoop: Structured Modeling and Behavioral Verification for Reliable LLM-Based Optimization；用途 `failure`；路线 `q002:failure_card_fts` #1；Card `failure-solver-feasibility-near-zero-information-proxy`（failure）；Evidence `ev-p097-behavioral-perturbation`, `ev-p097-feasibility-gap`
- Paper `P074` · ToolGate: Contract-Grounded and Verified Tool Execution for LLMs；用途 `failure`；路线 `q002:passage_hybrid` #1；Passage `P074:p0024:s0001`
- Paper `P073` · Uncertainty Calibration for Tool-Using Language Agents；用途 `failure`；路线 `q002:operator_card_fts` #2；Card `operator-execution-supervised-prompt-trace-calibration`（operator）；Evidence `ev-p073-execution-supervised-probe`, `ev-p073-internal-confidence-misalignment`
- Paper `P044` · DEER: A Benchmark for Evaluating Deep Research Agents on Expert Report Generation；用途 `failure`；路线 `q002:paper_card_fts` #4；Card `paper-p044`（paper）；Evidence `ev-p044-evaluation-core`
- Paper `P099` · Verus-SpecGym: An Agentic Environment for Evaluating Specification Autoformalization；用途 `operator`；路线 `q003:operator_card_fts` #1；Card `operator-four-bucket-executable-spec-testing`（operator）；Evidence `ev-p099-judge-miss`, `ev-p099-soundness-necessity`, `ev-p099-two-stage-check`
- Paper `P058` · AFlow: Automating Agentic Workflow Generation；用途 `operator`；路线 `q003:paper_card_fts` #4；Card `paper-p058`（paper）；Evidence `ev-p058-mcts-workflow-search`, `ev-p058-validation-selection-loop`
- Paper `P047` · tau2-Bench: Evaluating Conversational Agents in a Dual-Control Environment；用途 `operator`；路线 `q003:passage_hybrid` #1；Passage `P047:p0020:s0001`
- Paper `P004` · TravelPlanner: A Benchmark for Real-World Planning with Language Agents；用途 `operator`；路线 `q003:failure_card_fts` #4；Card `failure-constrained-plan-surface-validity`（failure）；Evidence `ev-p004-failure-core`, `ev-p004-macro-constraint-failure`
- Paper `P021` · In-the-Flow Agentic System Optimization for Effective Planning and Tool Use；用途 `prior`；路线 `q004:paper_card_fts` #1；Card `paper-p021`（paper）；Evidence `ev-p021-operator-core`
- Paper `P027` · Verified Critical Step Optimization for LLM Agents；用途 `prior`；路线 `q004:operator_card_fts` #2；Card `operator-verified-single-branch-repair`（operator）；Evidence `ev-p027-operator-core`
- Paper `P013` · Large Language Models Cannot Self-Correct Reasoning Yet；用途 `prior`；路线 `q004:failure_card_fts` #1；Card `failure-intrinsic-self-correction-degradation`（failure）；Evidence `ev-p013-intrinsic-self-correction-degrades`, `ev-p013-oracle-free-equal-budget-boundary`
- Paper `P050` · Scaling Agentic Verifier for Competitive Coding；用途 `prior`；路线 `q004:passage_hybrid` #1；Passage `P050:p0005:s0003`
- Paper `P035` · Holistic Agent Leaderboard: The Missing Infrastructure for AI Agent Evaluation；用途 `measurement`；路线 `q005:paper_card_fts` #1；Card `paper-p035`（paper）；Evidence `ev-p035-evaluation-core`
- Paper `P039` · ToolFailBench: Diagnosing Tool-Use Failures in LLM Agents；用途 `measurement`；路线 `q005:passage_hybrid` #2；Passage `P039:p0001:s0003`
- Paper `P064` · How Memory Management Impacts LLM Agents: An Empirical Study of Experience-Following Behavior；用途 `measurement`；路线 `q005:failure_card_fts` #3；Card `failure-retrieved-experience-propagates-stored-errors`（failure）；Evidence `ev-p064-evaluator-reliability`, `ev-p064-experience-following-error`
- Paper `P078` · CRAFT: Customizing LLMs by Creating and Retrieving from Specialized Toolsets；用途 `measurement`；路线 `q005:operator_card_fts` #5；Card `operator-validated-specialized-tool-creation-retrieval`（operator）；Evidence `ev-p078-baseline-fairness-boundary`, `ev-p078-generic-tool-and-baseline-boundary`, `ev-p078-multiview-tool-retrieval`, `ev-p078-toolset-construction-cost`, `ev-p078-validated-tool-creation-retrieval`

- 代表项：20 / 去重 Paper：50

## 查询与路线覆盖

### q001 · problem

- 原始查询：`tool-using LLM agents false task completion tool execution failures state inconsistency`
- 规范化查询：`"tool" OR "using" OR "LLM" OR "agents" OR "false" OR "task" OR "completion" OR "execution" OR "failures" OR "state" OR "inconsistency"`
- 路线 `paper_card_fts`：8 条；降级 false（无）
- 路线 `failure_card_fts`：8 条；降级 false（无）
- 路线 `passage_hybrid`：12 条；降级 true（vector_search_failed:RuntimeError:Cannot send a request, as the client has been closed.）
- 路线 `operator_card_fts`：8 条；降级 false（无）

### q002 · failure

- 原始查询：`agent reports success after tool error silent failure missing postcondition verification`
- 规范化查询：`"agent" OR "reports" OR "success" OR "after" OR "tool" OR "error" OR "silent" OR "failure" OR "missing" OR "postcondition" OR "verification"`
- 路线 `failure_card_fts`：8 条；降级 false（无）
- 路线 `passage_hybrid`：12 条；降级 true（vector_search_failed:RuntimeError:Cannot send a request, as the client has been closed.）
- 路线 `operator_card_fts`：8 条；降级 false（无）
- 路线 `paper_card_fts`：8 条；降级 false（无）

### q003 · operator

- 原始查询：`executable postconditions assertions state verification checkpoints tool trajectories`
- 规范化查询：`"executable" OR "postconditions" OR "assertions" OR "state" OR "verification" OR "checkpoints" OR "tool" OR "trajectories"`
- 路线 `operator_card_fts`：8 条；降级 false（无）
- 路线 `paper_card_fts`：8 条；降级 false（无）
- 路线 `passage_hybrid`：12 条；降级 true（vector_search_failed:RuntimeError:Cannot send a request, as the client has been closed.）
- 路线 `failure_card_fts`：8 条；降级 false（无）

### q004 · prior

- 原始查询：`tool agent trajectory verifier process reward model outcome verification self correction`
- 规范化查询：`"tool" OR "agent" OR "trajectory" OR "verifier" OR "process" OR "reward" OR "model" OR "outcome" OR "verification" OR "self" OR "correction"`
- 路线 `paper_card_fts`：8 条；降级 false（无）
- 路线 `operator_card_fts`：8 条；降级 false（无）
- 路线 `failure_card_fts`：8 条；降级 false（无）
- 路线 `passage_hybrid`：12 条；降级 false（无）

### q005 · measurement

- 原始查询：`tool use agent reliability benchmark execution trace perturbation tool errors`
- 规范化查询：`"tool" OR "use" OR "agent" OR "reliability" OR "benchmark" OR "execution" OR "trace" OR "perturbation" OR "errors"`
- 路线 `paper_card_fts`：8 条；降级 false（无）
- 路线 `passage_hybrid`：12 条；降级 false（无）
- 路线 `failure_card_fts`：8 条；降级 false（无）
- 路线 `operator_card_fts`：8 条；降级 false（无）

## 覆盖诊断

- 去重 Card：77
- 去重 Evidence：96
- 去重 Passage：57
- 命中 Paper：50
- 原始观测：180
- 带机械噪声标记的观测：36
