<!-- CRL_RESEARCH_SEARCH_META {"created_at_utc":"2026-08-13T10:34:13.780801Z","request_fingerprint_sha256":"1793b18d46e4d2515a74fc05a0016ba7facd9068a76dd2803f80c02b8b741bd5","result_json_sha256":"2ae5b662d846a02b36d246ec1e16d09ce41323b5701d86e7a8ffa4289a0063f7","search_id":"observer_effect_verification_v007_01"} -->
# 研究检索导航

> 本报告仅展示查询路线、来源、命中定位与覆盖；所有科研判断由主研究者完成。

- 搜索标识：`observer_effect_verification_v007_01`
- 生成时间（协调世界时）：`2026-08-13T10:34:13.780801Z`

## 紧凑研究地图

> 跨路线按 Paper 去重；每个查询路线至多选一个尚未出现的最高排名代表项。完整原始命中保留在 `result.json`。

- Paper `P046` · Solver-Aided Verification of Policy Compliance in Tool-Augmented LLM Agents；用途 `problem`；路线 `q001:paper_card_fts` #1；Card `paper-p046`（paper）；Evidence `ev-p046-operator-core`
- Paper `P069` · Tool Preferences in Agentic LLMs are Unreliable；用途 `problem`；路线 `q001:failure_card_fts` #1；Card `failure-tool-description-and-order-bias`（failure）；Evidence `ev-p069-description-induced-preference`, `ev-p069-identical-tool-order-bias`
- Paper `P026` · Agent Lightning: Train ANY AI Agents with Reinforcement Learning；用途 `problem`；路线 `q001:passage_hybrid` #1；Passage `P026:p0006:s0001`
- Paper `P007` · tau-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains；用途 `problem`；路线 `q001:operator_card_fts` #1；Card `operator-terminal-state-reliability-evaluation`（operator）；Evidence `ev-p007-terminal-state-evaluation`
- Paper `P074` · ToolGate: Contract-Grounded and Verified Tool Execution for LLMs；用途 `failure`；路线 `q002:failure_card_fts` #1；Card `failure-incomplete-tool-contracts-false-verified-state`（failure）；Evidence `ev-p074-contract-state-commit`, `ev-p074-missing-schema-true-postcondition`
- Paper `P099` · Verus-SpecGym: An Agentic Environment for Evaluating Specification Autoformalization；用途 `failure`；路线 `q002:passage_hybrid` #1；Passage `P099:p0002:s0001`
- Paper `P001` · ReAct: Synergizing Reasoning and Acting in Language Models；用途 `failure`；路线 `q002:operator_card_fts` #2；Card `operator-reason-action-interleaving`（operator）；Evidence `ev-p001-react-interleaved`
- Paper `P040` · From Confident Closing to Silent Failure: Characterizing False Success in LLM Agents；用途 `failure`；路线 `q002:paper_card_fts` #2；Card `paper-p040`（paper）；Evidence `ev-p040-failure-core`
- Paper `P010` · LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory；用途 `operator`；路线 `q003:operator_card_fts` #2；Card `operator-memory-stage-decomposition`（operator）；Evidence `ev-p010-index-retrieve-read`
- Paper `P044` · DEER: A Benchmark for Evaluating Deep Research Agents on Expert Report Generation；用途 `operator`；路线 `q003:paper_card_fts` #1；Card `paper-p044`（paper）；Evidence `ev-p044-evaluation-core`
- Paper `P093` · Collapse of Dense Retrievers: Short, Early, and Literal Biases Outranking Factual Evidence；用途 `operator`；路线 `q003:passage_hybrid` #3；Passage `P093:p0008:s0001`
- Paper `P090` · From Single to Multi-Granularity: Toward Long-Term Memory Association and Selection of Conversational Agents；用途 `operator`；路线 `q003:failure_card_fts` #1；Card `failure-fixed-single-granularity-memory`（failure）；Evidence `ev-p090-entropy-router`, `ev-p090-fixed-granularity-selection`
- Paper `P085` · Retrieval Models Aren't Tool-Savvy: Benchmarking Tool Retrieval for Large Language Models；用途 `prior`；路线 `q004:paper_card_fts` #2；Card `paper-p085`（paper）；Evidence `ev-p085-large-corpus-scale`, `ev-p085-non-exhaustive-label`, `ev-p085-retrieval-completeness-failure`
- Paper `P030` · STALE: Can LLM Agents Know When Their Memories Are No Longer Valid?；用途 `prior`；路线 `q004:operator_card_fts` #2；Card `operator-write-side-state-adjudication`（operator）；Evidence `ev-p030-authorized-readout`, `ev-p030-failure-core`, `ev-p030-write-side-adjudication`
- Paper `P096` · VeriSimpl: Robust Optimization Modeling from Natural Language using Simplification-based Verification；用途 `prior`；路线 `q004:failure_card_fts` #3；Card `failure-generator-aligned-verification-passes-shared-misreads`（failure）；Evidence `ev-p096-shared-misinterpretation`, `ev-p096-simplification-inversion`
- Paper `P021` · In-the-Flow Agentic System Optimization for Effective Planning and Tool Use；用途 `prior`；路线 `q004:passage_hybrid` #1；Passage `P021:p0027:s0001`
- Paper `P087` · Tools Are Under-Documented: Simple Document Expansion Boosts Tool Retrieval；用途 `measurement`；路线 `q005:paper_card_fts` #3；Card `paper-p087`（paper）；Evidence `ev-p087-fields-not-universally-beneficial`, `ev-p087-merge-and-semantic-judge`, `ev-p087-structured-query-independent-expansion`
- Paper `P035` · Holistic Agent Leaderboard: The Missing Infrastructure for AI Agent Evaluation；用途 `measurement`；路线 `q005:passage_hybrid` #2；Passage `P035:p0028:s0001`
- Paper `P098` · Beyond Objective Equivalence: Constraint Injection for LLM-Based Optimization Modeling on Vehicle Routing Problems；用途 `measurement`；路线 `q005:failure_card_fts` #1；Card `failure-objective-equivalence-passes-nonbinding-errors`（failure）；Evidence `ev-p098-diff-leak-550`, `ev-p098-nonbinding-blindness`, `ev-p098-open-problem`
- Paper `P041` · LLM Agents Already Know When to Call Tools - Even Without Reasoning；用途 `measurement`；路线 `q005:operator_card_fts` #3；Card `operator-hidden-state-tool-necessity-prefill`（operator）；Evidence `ev-p041-operator-core`, `ev-p041-probe-prefill-steering`

- 代表项：20 / 去重 Paper：92

## 查询与路线覆盖

### q001 · problem

- 原始查询：`LLM tool agent verification query changes state observer effect side effecting read get list search marks read consumes queue`
- 规范化查询：`"LLM" OR "tool" OR "agent" OR "verification" OR "query" OR "changes" OR "state" OR "observer" OR "effect" OR "side" OR "effecting" OR "read" OR "get" OR "list" OR "search" OR "marks" OR "consumes" OR "queue"`
- 路线 `paper_card_fts`：30 条；降级 false（无）
- 路线 `failure_card_fts`：30 条；降级 false（无）
- 路线 `passage_hybrid`：20 条；降级 false（无）
- 路线 `operator_card_fts`：30 条；降级 false（无）

### q002 · failure

- 原始查询：`postcondition verifier non read only observation mutates environment verification causes terminal failure`
- 规范化查询：`"postcondition" OR "verifier" OR "non" OR "read" OR "only" OR "observation" OR "mutates" OR "environment" OR "verification" OR "causes" OR "terminal" OR "failure"`
- 路线 `failure_card_fts`：30 条；降级 false（无）
- 路线 `passage_hybrid`：20 条；降级 false（无）
- 路线 `operator_card_fts`：30 条；降级 false（无）
- 路线 `paper_card_fts`：30 条；降级 false（无）

### q003 · operator

- 原始查询：`non invasive verification read purity effect typing shadow query rollback observational noninterference`
- 规范化查询：`"non" OR "invasive" OR "verification" OR "read" OR "purity" OR "effect" OR "typing" OR "shadow" OR "query" OR "rollback" OR "observational" OR "noninterference"`
- 路线 `operator_card_fts`：24 条；降级 false（无）
- 路线 `paper_card_fts`：27 条；降级 false（无）
- 路线 `passage_hybrid`：20 条；降级 false（无）
- 路线 `failure_card_fts`：15 条；降级 false（无）

### q004 · prior

- 原始查询：`tool agent verifier read only assumption side effect query verification tool effect system`
- 规范化查询：`"tool" OR "agent" OR "verifier" OR "read" OR "only" OR "assumption" OR "side" OR "effect" OR "query" OR "verification" OR "system"`
- 路线 `paper_card_fts`：30 条；降级 false（无）
- 路线 `operator_card_fts`：30 条；降级 false（无）
- 路线 `failure_card_fts`：30 条；降级 false（无）
- 路线 `passage_hybrid`：20 条；降级 false（无）

### q005 · measurement

- 原始查询：`act only passes act plus verification fails state diff read side effect independent terminal`
- 规范化查询：`"act" OR "only" OR "passes" OR "plus" OR "verification" OR "fails" OR "state" OR "diff" OR "read" OR "side" OR "effect" OR "independent" OR "terminal"`
- 路线 `paper_card_fts`：30 条；降级 false（无）
- 路线 `passage_hybrid`：20 条；降级 false（无）
- 路线 `failure_card_fts`：29 条；降级 false（无）
- 路线 `operator_card_fts`：30 条；降级 false（无）

## 覆盖诊断

- 去重 Card：156
- 去重 Evidence：184
- 去重 Passage：87
- 命中 Paper：92
- 原始观测：525
- 带机械噪声标记的观测：2
