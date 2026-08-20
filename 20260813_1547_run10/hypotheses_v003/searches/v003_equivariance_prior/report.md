<!-- CRL_RESEARCH_SEARCH_META {"created_at_utc":"2026-08-13T09:37:56.709836Z","request_fingerprint_sha256":"5faaa1fab7225fcfab2091e468a6fdf82cbb305a2c638ad46da51b9d8d5959c6","result_json_sha256":"d5b755da4e0d3b5cda2a1971348eda061a3d7a2a86f831c9e4668818c4a8e610","search_id":"v003_equivariance_prior"} -->
# 研究检索导航

> 本报告仅展示查询路线、来源、命中定位与覆盖；所有科研判断由主研究者完成。

- 搜索标识：`v003_equivariance_prior`
- 生成时间（协调世界时）：`2026-08-13T09:37:56.709836Z`

## 紧凑研究地图

> 跨路线按 Paper 去重；每个查询路线至多选一个尚未出现的最高排名代表项。完整原始命中保留在 `result.json`。

- Paper `P039` · ToolFailBench: Diagnosing Tool-Use Failures in LLM Agents；用途 `prior`；路线 `q001:paper_card_fts` #1；Card `paper-p039`（paper）；Evidence `ev-p039-failure-core`
- Paper `P071` · Agentic Plan Caching: Test-Time Memory for Fast and Cost-Efficient LLM Agents；用途 `prior`；路线 `q001:operator_card_fts` #1；Card `operator-adaptive-plan-template-reuse`（operator）；Evidence `ev-p071-cache-false-positive-boundary`, `ev-p071-plan-template-reuse`
- Paper `P011` · On Memory Construction and Retrieval for Personalized Conversational Agents；用途 `prior`；路线 `q001:failure_card_fts` #2；Card `failure-memory-unit-granularity-mismatch`（failure）；Evidence `ev-p011-failure-core`
- Paper `P062` · Agentic Memory: Learning Unified Long-Term and Short-Term Memory Management for Large Language Model Agents；用途 `prior`；路线 `q001:passage_hybrid` #2；Passage `P062:p0010:s0002`
- Paper `P079` · Learning to Contextualize Web Pages for Enhanced Decision Making by LLM Agents；用途 `operator`；路线 `q002:operator_card_fts` #1；Card `operator-action-preserving-observation-contextualization`（operator）；Evidence `ev-p079-action-conditioned-contextualization`, `ev-p079-ground-truth-action-retry`, `ev-p079-unseen-ui-boundary`
- Paper `P065` · Group-in-Group Policy Optimization for LLM Agent Training；用途 `operator`；路线 `q002:paper_card_fts` #3；Card `paper-p065`（paper）；Evidence `ev-p065-anchor-state-credit`, `ev-p065-state-recurrence-boundary`
- Paper `P048` · NaviAgent: Graph-Driven Bilevel Planning for Scalable Tool Orchestration；用途 `operator`；路线 `q002:passage_hybrid` #1；Passage `P048:p0003:s0005`
- Paper `P082` · Toolformer: Language Models Can Teach Themselves to Use Tools；用途 `operator`；路线 `q002:failure_card_fts` #2；Card `failure-likelihood-utility-does-not-guarantee-agent-utility`（failure）；Evidence `ev-p082-chaining-cost-sparsity-boundary`, `ev-p082-future-token-loss-filtered-calls`, `ev-p082-top-k-single-call-boundary`
- Paper `P032` · CRITIC: Large Language Models Can Self-Correct with Tool-Interactive Critiquing；用途 `operator`；路线 `q003:operator_card_fts` #2；Card `operator-tool-grounded-critique`（operator）；Evidence `ev-p032-operator-core`
- Paper `P086` · Meta-Tool: Unleash Open-World Function Calling Capabilities of General-Purpose Large Language Models；用途 `operator`；路线 `q003:paper_card_fts` #1；Card `paper-p086`（paper）；Evidence `ev-p086-hypothesize-retrieve-invoke`, `ev-p086-near-identical-distribution`, `ev-p086-required-parameter-score`
- Paper `P044` · DEER: A Benchmark for Evaluating Deep Research Agents on Expert Report Generation；用途 `operator`；路线 `q003:passage_hybrid` #1；Passage `P044:p0029:s0001`
- Paper `P084` · On the Robustness of Agentic Function Calling；用途 `operator`；路线 `q003:failure_card_fts` #1；Card `failure-semantically-related-toolkit-expansion`（failure）；Evidence `ev-p084-expanded-toolkit-controlled-setting`, `ev-p084-expanded-toolkit-table`, `ev-p084-generated-tool-single-dataset-boundary`, `ev-p084-related-toolkit-error-types`
- Paper `P027` · Verified Critical Step Optimization for LLM Agents；用途 `operator`；路线 `q004:operator_card_fts` #2；Card `operator-verified-single-branch-repair`（operator）；Evidence `ev-p027-operator-core`
- Paper `P025` · Unlocking the Power of Multi-Agent LLM for Reasoning: From Lazy Agents to Deliberation；用途 `operator`；路线 `q004:paper_card_fts` #2；Card `paper-p025`（paper）；Evidence `ev-p025-failure-core`
- Paper `P092` · MemConflict: Evaluating Long-Term Memory Systems Under Memory Conflicts；用途 `operator`；路线 `q004:passage_hybrid` #4；Passage `P092:p0030:s0001`
- Paper `P060` · Unifying Inference-Time Planning Language Generation；用途 `operator`；路线 `q004:failure_card_fts` #3；Card `failure-natural-language-ir-hurts-formal-planning`（failure）；Evidence `ev-p060-formal-ir-solver`, `ev-p060-ir-result-and-nl-failure`
- Paper `P001` · ReAct: Synergizing Reasoning and Acting in Language Models；用途 `operator`；路线 `q005:operator_card_fts` #1；Card `operator-reason-action-interleaving`（operator）；Evidence `ev-p001-react-interleaved`
- Paper `P005` · ToolLLM: Facilitating Large Language Models to Master 16000+ Real-world APIs；用途 `operator`；路线 `q005:paper_card_fts` #3；Card `paper-p005`（paper）；Evidence `ev-p005-operator-core`
- Paper `P019` · STeCa: Step-level Trajectory Calibration for LLM Agent Learning；用途 `operator`；路线 `q005:passage_hybrid` #1；Passage `P019:p0013:s0001`
- Paper `P089` · ToolDreamer: Instilling LLM Reasoning Into Tool Retrievers；用途 `operator`；路线 `q005:failure_card_fts` #2；Card `failure-forced-hypothetical-tool-alignment`（failure）；Evidence `ev-p089-forced-alignment-proxy`, `ev-p089-hungarian-alignment`, `ev-p089-retrieval-only-metrics`, `ev-p089-training-gold-count-hypothetical-tools`
- Paper `P095` · Don't Ask the LLM to Track Freshness: A Deterministic Recipe for Memory Conflict Resolution；用途 `failure`；路线 `q006:failure_card_fts` #1；Card `failure-llm-freshness-judgment-prior-override-and-drift`（failure）；Evidence `ev-p095-matched-comparison`, `ev-p095-prior-override-drift`
- Paper `P030` · STALE: Can LLM Agents Know When Their Memories Are No Longer Valid?；用途 `failure`；路线 `q006:passage_hybrid` #1；Passage `P030:p0034:s0001`
- Paper `P074` · ToolGate: Contract-Grounded and Verified Tool Execution for LLMs；用途 `failure`；路线 `q006:operator_card_fts` #3；Card `operator-contract-gated-tool-state-commit`（operator）；Evidence `ev-p074-contract-state-commit`, `ev-p074-missing-schema-true-postcondition`
- Paper `P034` · RefineBench: Evaluating Refinement Capability of Language Models via Checklists；用途 `failure`；路线 `q006:paper_card_fts` #2；Card `paper-p034`（paper）；Evidence `ev-p034-failure-core`
- Paper `P040` · From Confident Closing to Silent Failure: Characterizing False Success in LLM Agents；用途 `measurement`；路线 `q007:paper_card_fts` #1；Card `paper-p040`（paper）；Evidence `ev-p040-failure-core`
- Paper `P036` · tau-Knowledge: Evaluating Conversational Agents over Unstructured Knowledge；用途 `measurement`；路线 `q007:passage_hybrid` #1；Passage `P036:p0023:s0001`
- Paper `P076` · Multi-Agent Systems Execute Arbitrary Malicious Code；用途 `measurement`；路线 `q007:failure_card_fts` #3；Card `failure-untrusted-agent-metadata-privileged-control-flow`（failure）；Evidence `ev-p076-controlled-lab-boundary`, `ev-p076-metadata-control-flow-laundering`, `ev-p076-refusal-not-system-safety`
- Paper `P097` · ReLoop: Structured Modeling and Behavioral Verification for Reliable LLM-Based Optimization；用途 `measurement`；路线 `q007:operator_card_fts` #3；Card `operator-behavioral-perturbation-existence-test`（operator）；Evidence `ev-p097-behavioral-perturbation`, `ev-p097-feasibility-gap`

- 代表项：28 / 去重 Paper：93

## 查询与路线覆盖

### q001 · prior

- 原始查询：`ACCORD 2606.16432 EG-VAR 2607.12650 AgentCheck AttriGuard Causal Agent Replay ToolFailBench Tool use Tax`
- 规范化查询：`"ACCORD" OR "2606" OR "16432" OR "EG" OR "VAR" OR "2607" OR "12650" OR "AgentCheck" OR "AttriGuard" OR "Causal" OR "Agent" OR "Replay" OR "ToolFailBench" OR "Tool" OR "use" OR "Tax"`
- 路线 `paper_card_fts`：24 条；降级 false（无）
- 路线 `operator_card_fts`：24 条；降级 false（无）
- 路线 `failure_card_fts`：24 条；降级 false（无）
- 路线 `passage_hybrid`：24 条；降级 false（无）

### q002 · operator

- 原始查询：`equivariant training paired tool observation structured action transformation contrastive policy loss`
- 规范化查询：`"equivariant" OR "training" OR "paired" OR "tool" OR "observation" OR "structured" OR "action" OR "transformation" OR "contrastive" OR "policy" OR "loss"`
- 路线 `operator_card_fts`：24 条；降级 false（无）
- 路线 `paper_card_fts`：24 条；降级 false（无）
- 路线 `passage_hybrid`：24 条；降级 false（无）
- 路线 `failure_card_fts`：24 条；降级 false（无）

### q003 · operator

- 原始查询：`context aware contrastive decoding external evidence parametric prior action logits tool result`
- 规范化查询：`"context" OR "aware" OR "contrastive" OR "decoding" OR "external" OR "evidence" OR "parametric" OR "prior" OR "action" OR "logits" OR "tool" OR "result"`
- 路线 `operator_card_fts`：24 条；降级 false（无）
- 路线 `paper_card_fts`：24 条；降级 false（无）
- 路线 `passage_hybrid`：24 条；降级 false（无）
- 路线 `failure_card_fts`：24 条；降级 false（无）

### q004 · operator

- 原始查询：`counterfactual action distribution language model agent abstract counterfactual orbit projection group consistency`
- 规范化查询：`"counterfactual" OR "action" OR "distribution" OR "language" OR "model" OR "agent" OR "abstract" OR "orbit" OR "projection" OR "group" OR "consistency"`
- 路线 `operator_card_fts`：24 条；降级 false（无）
- 路线 `paper_card_fts`：24 条；降级 false（无）
- 路线 `passage_hybrid`：24 条；降级 false（无）
- 路线 `failure_card_fts`：24 条；降级 false（无）

### q005 · operator

- 原始查询：`visibility grounded action supervision tool result next action fine tuning Graph Explorer IPR ACT`
- 规范化查询：`"visibility" OR "grounded" OR "action" OR "supervision" OR "tool" OR "result" OR "next" OR "fine" OR "tuning" OR "Graph" OR "Explorer" OR "IPR" OR "ACT"`
- 路线 `operator_card_fts`：24 条；降级 false（无）
- 路线 `paper_card_fts`：24 条；降级 false（无）
- 路线 `passage_hybrid`：24 条；降级 false（无）
- 路线 `failure_card_fts`：24 条；降级 false（无）

### q006 · failure

- 原始查询：`correct tool result ignored overlooked evidence prior override downstream action integration`
- 规范化查询：`"correct" OR "tool" OR "result" OR "ignored" OR "overlooked" OR "evidence" OR "prior" OR "override" OR "downstream" OR "action" OR "integration"`
- 路线 `failure_card_fts`：24 条；降级 false（无）
- 路线 `passage_hybrid`：24 条；降级 false（无）
- 路线 `operator_card_fts`：24 条；降级 false（无）
- 路线 `paper_card_fts`：24 条；降级 false（无）

### q007 · measurement

- 原始查询：`relevant result perturbation irrelevant metadata perturbation action equivariance invariance terminal success`
- 规范化查询：`"relevant" OR "result" OR "perturbation" OR "irrelevant" OR "metadata" OR "action" OR "equivariance" OR "invariance" OR "terminal" OR "success"`
- 路线 `paper_card_fts`：24 条；降级 false（无）
- 路线 `passage_hybrid`：24 条；降级 false（无）
- 路线 `failure_card_fts`：24 条；降级 false（无）
- 路线 `operator_card_fts`：24 条；降级 false（无）

## 覆盖诊断

- 去重 Card：180
- 去重 Evidence：197
- 去重 Passage：152
- 命中 Paper：93
- 原始观测：672
- 带机械噪声标记的观测：3
