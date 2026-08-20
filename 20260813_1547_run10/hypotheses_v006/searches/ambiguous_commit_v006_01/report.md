<!-- CRL_RESEARCH_SEARCH_META {"created_at_utc":"2026-08-13T10:30:57.617570Z","request_fingerprint_sha256":"81d4edf0c389416e061027f7ab93a9810d9843a7eaa98b643404ad027188a4f2","result_json_sha256":"a4e20ba5970d96028a0dc4a098a915975b700fc0ebb8b9979e205c32d3a3307b","search_id":"ambiguous_commit_v006_01"} -->
# 研究检索导航

> 本报告仅展示查询路线、来源、命中定位与覆盖；所有科研判断由主研究者完成。

- 搜索标识：`ambiguous_commit_v006_01`
- 生成时间（协调世界时）：`2026-08-13T10:30:57.617570Z`

## 紧凑研究地图

> 跨路线按 Paper 去重；每个查询路线至多选一个尚未出现的最高排名代表项。完整原始命中保留在 `result.json`。

- Paper `P046` · Solver-Aided Verification of Policy Compliance in Tool-Augmented LLM Agents；用途 `problem`；路线 `q001:paper_card_fts` #1；Card `paper-p046`（paper）；Evidence `ev-p046-operator-core`
- Paper `P069` · Tool Preferences in Agentic LLMs are Unreliable；用途 `problem`；路线 `q001:failure_card_fts` #1；Card `failure-tool-description-and-order-bias`（failure）；Evidence `ev-p069-description-induced-preference`, `ev-p069-identical-tool-order-bias`
- Paper `P030` · STALE: Can LLM Agents Know When Their Memories Are No Longer Valid?；用途 `problem`；路线 `q001:passage_hybrid` #1；Passage `P030:p0029:s0001`
- Paper `P007` · tau-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains；用途 `problem`；路线 `q001:operator_card_fts` #2；Card `operator-terminal-state-reliability-evaluation`（operator）；Evidence `ev-p007-terminal-state-evaluation`
- Paper `P074` · ToolGate: Contract-Grounded and Verified Tool Execution for LLMs；用途 `failure`；路线 `q002:failure_card_fts` #1；Card `failure-incomplete-tool-contracts-false-verified-state`（failure）；Evidence `ev-p074-contract-state-commit`, `ev-p074-missing-schema-true-postcondition`
- Paper `P040` · From Confident Closing to Silent Failure: Characterizing False Success in LLM Agents；用途 `failure`；路线 `q002:passage_hybrid` #1；Passage `P040:p0008:s0001`
- Paper `P079` · Learning to Contextualize Web Pages for Enhanced Decision Making by LLM Agents；用途 `failure`；路线 `q002:operator_card_fts` #2；Card `operator-action-preserving-observation-contextualization`（operator）；Evidence `ev-p079-action-conditioned-contextualization`, `ev-p079-ground-truth-action-retry`, `ev-p079-unseen-ui-boundary`
- Paper `P041` · LLM Agents Already Know When to Call Tools - Even Without Reasoning；用途 `failure`；路线 `q002:paper_card_fts` #3；Card `paper-p041`（paper）；Evidence `ev-p041-operator-core`
- Paper `P087` · Tools Are Under-Documented: Simple Document Expansion Boosts Tool Retrieval；用途 `operator`；路线 `q003:operator_card_fts` #1；Card `operator-grounded-structured-tool-document-expansion`（operator）；Evidence `ev-p087-fields-not-universally-beneficial`, `ev-p087-merge-and-semantic-judge`, `ev-p087-structured-query-independent-expansion`
- Paper `P071` · Agentic Plan Caching: Test-Time Memory for Fast and Cost-Efficient LLM Agents；用途 `operator`；路线 `q003:paper_card_fts` #2；Card `paper-p071`（paper）；Evidence `ev-p071-cache-false-positive-boundary`, `ev-p071-plan-template-reuse`
- Paper `P036` · tau-Knowledge: Evaluating Conversational Agents over Unstructured Knowledge；用途 `operator`；路线 `q003:passage_hybrid` #2；Passage `P036:p0014:s0001`
- Paper `P101` · Semantic Evaluation for Text-to-SQL with Distilled Test Suites；用途 `operator`；路线 `q003:failure_card_fts` #3；Card `failure-single-execution-denotation-false-positive`（failure）；Evidence `ev-p101-esm-fn-rate`, `ev-p101-metric-distortion`
- Paper `P049` · Reinforced Agent: Inference-Time Feedback for Tool-Calling Agents；用途 `prior`；路线 `q004:paper_card_fts` #1；Card `paper-p049`（paper）；Evidence `ev-p049-operator-core`
- Paper `P097` · ReLoop: Structured Modeling and Behavioral Verification for Reliable LLM-Based Optimization；用途 `prior`；路线 `q004:operator_card_fts` #7；Card `operator-behavioral-perturbation-existence-test`（operator）；Evidence `ev-p097-behavioral-perturbation`, `ev-p097-feasibility-gap`
- Paper `P018` · ExpeL: LLM Agents Are Experiential Learners；用途 `prior`；路线 `q004:failure_card_fts` #2；Card `failure-unfiltered-reflection-contamination`（failure）；Evidence `ev-p018-raw-reflection-contamination`
- Paper `P016` · Why Do Multi-Agent LLM Systems Fail?；用途 `prior`；路线 `q004:passage_hybrid` #1；Passage `P016:p0007:s0002`
- Paper `P033` · Self-Refine: Iterative Refinement with Self-Feedback；用途 `measurement`；路线 `q005:paper_card_fts` #2；Card `paper-p033`（paper）；Evidence `ev-p033-operator-core`
- Paper `P058` · AFlow: Automating Agentic Workflow Generation；用途 `measurement`；路线 `q005:passage_hybrid` #5；Passage `P058:p0017:s0001`
- Paper `P091` · Temporal Validity in Retrieval Memory: Eliminating Stale-Fact Errors for AI Agents over Evolving Knowledge；用途 `measurement`；路线 `q005:failure_card_fts` #1；Card `failure-cosine-cannot-separate-contradiction-from-duplicate`（failure）；Evidence `ev-p091-cosine-auroc`, `ev-p091-retain-fabrication`
- Paper `P032` · CRITIC: Large Language Models Can Self-Correct with Tool-Interactive Critiquing；用途 `measurement`；路线 `q005:operator_card_fts` #3；Card `operator-tool-grounded-critique`（operator）；Evidence `ev-p032-operator-core`

- 代表项：20 / 去重 Paper：92

## 查询与路线覆盖

### q001 · problem

- 原始查询：`LLM agent tool call timeout ambiguous outcome committed but response lost duplicate side effect exactly once`
- 规范化查询：`"LLM" OR "agent" OR "tool" OR "call" OR "timeout" OR "ambiguous" OR "outcome" OR "committed" OR "but" OR "response" OR "lost" OR "duplicate" OR "side" OR "effect" OR "exactly" OR "once"`
- 路线 `paper_card_fts`：30 条；降级 false（无）
- 路线 `failure_card_fts`：30 条；降级 false（无）
- 路线 `passage_hybrid`：20 条；降级 false（无）
- 路线 `operator_card_fts`：30 条；降级 false（无）

### q002 · failure

- 原始查询：`retry after timeout tool action already executed duplicate payment message deletion false failure ambiguous commit`
- 规范化查询：`"retry" OR "after" OR "timeout" OR "tool" OR "action" OR "already" OR "executed" OR "duplicate" OR "payment" OR "message" OR "deletion" OR "false" OR "failure" OR "ambiguous" OR "commit"`
- 路线 `failure_card_fts`：30 条；降级 false（无）
- 路线 `passage_hybrid`：20 条；降级 false（无）
- 路线 `operator_card_fts`：30 条；降级 false（无）
- 路线 `paper_card_fts`：30 条；降级 false（无）

### q003 · operator

- 原始查询：`semantic idempotency reconciliation intent fingerprint read after timeout commit status query transaction recovery`
- 规范化查询：`"semantic" OR "idempotency" OR "reconciliation" OR "intent" OR "fingerprint" OR "read" OR "after" OR "timeout" OR "commit" OR "status" OR "query" OR "transaction" OR "recovery"`
- 路线 `operator_card_fts`：30 条；降级 false（无）
- 路线 `paper_card_fts`：28 条；降级 false（无）
- 路线 `passage_hybrid`：20 条；降级 false（无）
- 路线 `failure_card_fts`：17 条；降级 false（无）

### q004 · prior

- 原始查询：`tool agent transactional execution idempotency key exactly once ambiguous failure retry side effects`
- 规范化查询：`"tool" OR "agent" OR "transactional" OR "execution" OR "idempotency" OR "key" OR "exactly" OR "once" OR "ambiguous" OR "failure" OR "retry" OR "side" OR "effects"`
- 路线 `paper_card_fts`：30 条；降级 false（无）
- 路线 `operator_card_fts`：30 条；降级 false（无）
- 路线 `failure_card_fts`：30 条；降级 false（无）
- 路线 `passage_hybrid`：20 条；降级 false（无）

### q005 · measurement

- 原始查询：`commit then timeout fault injection duplicate action independent terminal same budget reconcile no retry retry`
- 规范化查询：`"commit" OR "then" OR "timeout" OR "fault" OR "injection" OR "duplicate" OR "action" OR "independent" OR "terminal" OR "same" OR "budget" OR "reconcile" OR "no" OR "retry"`
- 路线 `paper_card_fts`：30 条；降级 false（无）
- 路线 `passage_hybrid`：20 条；降级 false（无）
- 路线 `failure_card_fts`：30 条；降级 false（无）
- 路线 `operator_card_fts`：30 条；降级 false（无）

## 覆盖诊断

- 去重 Card：189
- 去重 Evidence：198
- 去重 Passage：73
- 命中 Paper：92
- 原始观测：535
- 带机械噪声标记的观测：3
