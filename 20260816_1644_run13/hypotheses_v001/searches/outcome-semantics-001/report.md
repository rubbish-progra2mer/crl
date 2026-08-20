<!-- CRL_RESEARCH_SEARCH_META {"created_at_utc":"2026-08-16T08:49:46.145222Z","request_fingerprint_sha256":"cad764d0f4f72b5b02c379f05f840edbd6445882f0430030a38bf05ef05083eb","result_json_sha256":"3b7adc332fbcbfc3cb96a4d6dc070a1abd8a5c4e6a1c41cbb9dccea6abd32f5f","search_id":"outcome-semantics-001"} -->
# 研究检索导航

> 本报告仅展示查询路线、来源、命中定位与覆盖；所有科研判断由主研究者完成。

- 搜索标识：`outcome-semantics-001`
- 生成时间（协调世界时）：`2026-08-16T08:49:46.145222Z`

## 紧凑研究地图

> 跨路线按 Paper 去重；每个查询路线至多选一个尚未出现的最高排名代表项。完整原始命中保留在 `result.json`。

- Paper `P030` · STALE: Can LLM Agents Know When Their Memories Are No Longer Valid?；用途 `problem`；路线 `q001:paper_card_fts` #1；Card `paper-p030`（paper）；Evidence `ev-p030-failure-core`
- Paper `P072` · Structured Uncertainty guided Clarification for LLM Agents；用途 `problem`；路线 `q001:failure_card_fts` #1；Card `failure-free-form-clarification-no-stop-value`（failure）；Evidence `ev-p072-compute-boundary`, `ev-p072-structured-clarification-gate`, `ev-p072-unstructured-clarification-failure`
- Paper `P039` · ToolFailBench: Diagnosing Tool-Use Failures in LLM Agents；用途 `problem`；路线 `q001:passage_hybrid` #1；Passage `P039:p0003:s0002`
- Paper `P074` · ToolGate: Contract-Grounded and Verified Tool Execution for LLMs；用途 `problem`；路线 `q001:operator_card_fts` #1；Card `operator-contract-gated-tool-state-commit`（operator）；Evidence `ev-p074-contract-state-commit`, `ev-p074-missing-schema-true-postcondition`
- Paper `P089` · ToolDreamer: Instilling LLM Reasoning Into Tool Retrievers；用途 `failure`；路线 `q002:failure_card_fts` #1；Card `failure-forced-hypothetical-tool-alignment`（failure）；Evidence `ev-p089-forced-alignment-proxy`, `ev-p089-hungarian-alignment`, `ev-p089-retrieval-only-metrics`, `ev-p089-training-gold-count-hypothetical-tools`
- Paper `P040` · From Confident Closing to Silent Failure: Characterizing False Success in LLM Agents；用途 `failure`；路线 `q002:passage_hybrid` #2；Passage `P040:p0003:s0001`
- Paper `P079` · Learning to Contextualize Web Pages for Enhanced Decision Making by LLM Agents；用途 `failure`；路线 `q002:operator_card_fts` #1；Card `operator-action-preserving-observation-contextualization`（operator）；Evidence `ev-p079-action-conditioned-contextualization`, `ev-p079-ground-truth-action-retry`, `ev-p079-unseen-ui-boundary`
- Paper `P001` · ReAct: Synergizing Reasoning and Acting in Language Models；用途 `failure`；路线 `q002:paper_card_fts` #1；Card `paper-react`（paper）；Evidence `ev-p001-react-interleaved`, `ev-p001-search-hallucination-boundary`
- Paper `P073` · Uncertainty Calibration for Tool-Using Language Agents；用途 `operator`；路线 `q003:operator_card_fts` #2；Card `operator-execution-supervised-prompt-trace-calibration`（operator）；Evidence `ev-p073-execution-supervised-probe`, `ev-p073-internal-confidence-misalignment`
- Paper `P044` · DEER: A Benchmark for Evaluating Deep Research Agents on Expert Report Generation；用途 `operator`；路线 `q003:paper_card_fts` #2；Card `paper-p044`（paper）；Evidence `ev-p044-evaluation-core`
- Paper `P034` · RefineBench: Evaluating Refinement Capability of Language Models via Checklists；用途 `operator`；路线 `q003:passage_hybrid` #6；Passage `P034:p0043:s0001`
- Paper `P096` · VeriSimpl: Robust Optimization Modeling from Natural Language using Simplification-based Verification；用途 `operator`；路线 `q003:failure_card_fts` #3；Card `failure-generator-aligned-verification-passes-shared-misreads`（failure）；Evidence `ev-p096-shared-misinterpretation`, `ev-p096-simplification-inversion`
- Paper `P035` · Holistic Agent Leaderboard: The Missing Infrastructure for AI Agent Evaluation；用途 `prior`；路线 `q004:paper_card_fts` #4；Card `paper-p035`（paper）；Evidence `ev-p035-evaluation-core`
- Paper `P088` · Non-negative Elastic Net Decoding for Information Retrieval；用途 `prior`；路线 `q004:operator_card_fts` #2；Card `operator-joint-nonnegative-residual-retrieval`（operator）；Evidence `ev-p088-joint-nonnegative-objective`, `ev-p088-relevant-set-size-signature`, `ev-p088-theory-deployment-scale-boundary`
- Paper `P076` · Multi-Agent Systems Execute Arbitrary Malicious Code；用途 `prior`；路线 `q004:failure_card_fts` #2；Card `failure-untrusted-agent-metadata-privileged-control-flow`（failure）；Evidence `ev-p076-controlled-lab-boundary`, `ev-p076-metadata-control-flow-laundering`, `ev-p076-refusal-not-system-safety`
- Paper `P097` · ReLoop: Structured Modeling and Behavioral Verification for Reliable LLM-Based Optimization；用途 `prior`；路线 `q004:passage_hybrid` #16；Passage `P097:p0003:s0001`
- Paper `P085` · Retrieval Models Aren't Tool-Savvy: Benchmarking Tool Retrieval for Large Language Models；用途 `measurement`；路线 `q005:paper_card_fts` #2；Card `paper-p085`（paper）；Evidence `ev-p085-large-corpus-scale`, `ev-p085-non-exhaustive-label`, `ev-p085-retrieval-completeness-failure`
- Paper `P048` · NaviAgent: Graph-Driven Bilevel Planning for Scalable Tool Orchestration；用途 `measurement`；路线 `q005:passage_hybrid` #4；Passage `P048:p0032:s0001`
- Paper `P069` · Tool Preferences in Agentic LLMs are Unreliable；用途 `measurement`；路线 `q005:failure_card_fts` #2；Card `failure-tool-description-and-order-bias`（failure）；Evidence `ev-p069-description-induced-preference`, `ev-p069-identical-tool-order-bias`
- Paper `P037` · ToolSandbox: A Stateful, Conversational, Interactive Evaluation Benchmark for LLM Tool Use Capabilities；用途 `measurement`；路线 `q005:operator_card_fts` #1；Card `operator-milestone-dag-trajectory-evaluation`（operator）；Evidence `ev-p037-evaluation-core`, `ev-p037-minefield-violation`

- 代表项：20 / 去重 Paper：71

## 查询与路线覆盖

### q001 · problem

- 原始查询：`valid empty tool result versus runtime failure LLM agent outcome ambiguity`
- 规范化查询：`"valid" OR "empty" OR "tool" OR "result" OR "versus" OR "runtime" OR "failure" OR "LLM" OR "agent" OR "outcome" OR "ambiguity"`
- 路线 `paper_card_fts`：12 条；降级 false（无）
- 路线 `failure_card_fts`：12 条；降级 false（无）
- 路线 `passage_hybrid`：18 条；降级 false（无）
- 路线 `operator_card_fts`：12 条；降级 false（无）

### q002 · failure

- 原始查询：`null empty list retries hallucination tool agent`
- 规范化查询：`"null" OR "empty" OR "list" OR "retries" OR "hallucination" OR "tool" OR "agent"`
- 路线 `failure_card_fts`：12 条；降级 false（无）
- 路线 `passage_hybrid`：18 条；降级 false（无）
- 路线 `operator_card_fts`：12 条；降级 false（无）
- 路线 `paper_card_fts`：12 条；降级 false（无）

### q003 · operator

- 原始查询：`typed outcome contract success failure unknown verification`
- 规范化查询：`"typed" OR "outcome" OR "contract" OR "success" OR "failure" OR "unknown" OR "verification"`
- 路线 `operator_card_fts`：12 条；降级 false（无）
- 路线 `paper_card_fts`：12 条；降级 false（无）
- 路线 `passage_hybrid`：18 条；降级 false（无）
- 路线 `failure_card_fts`：12 条；降级 false（无）

### q004 · prior

- 原始查询：`tool failure recovery empty result semantic status agent benchmark`
- 规范化查询：`"tool" OR "failure" OR "recovery" OR "empty" OR "result" OR "semantic" OR "status" OR "agent" OR "benchmark"`
- 路线 `paper_card_fts`：12 条；降级 false（无）
- 路线 `operator_card_fts`：12 条；降级 false（无）
- 路线 `failure_card_fts`：12 条；降级 false（无）
- 路线 `passage_hybrid`：18 条；降级 false（无）

### q005 · measurement

- 原始查询：`calibrated recovery decision valid empty no-op transient failure unknown effect`
- 规范化查询：`"calibrated" OR "recovery" OR "decision" OR "valid" OR "empty" OR "no" OR "op" OR "transient" OR "failure" OR "unknown" OR "effect"`
- 路线 `paper_card_fts`：12 条；降级 false（无）
- 路线 `passage_hybrid`：18 条；降级 false（无）
- 路线 `failure_card_fts`：12 条；降级 false（无）
- 路线 `operator_card_fts`：12 条；降级 false（无）

## 覆盖诊断

- 去重 Card：110
- 去重 Evidence：145
- 去重 Passage：73
- 命中 Paper：71
- 原始观测：270
- 带机械噪声标记的观测：0
