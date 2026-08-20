<!-- CRL_RESEARCH_SEARCH_META {"created_at_utc":"2026-08-16T06:14:31.624296Z","request_fingerprint_sha256":"885aaf9dcf1646df4cdf50756b1125a3cf8dbfddf058551b9ec65a9e0088686b","result_json_sha256":"0fb0b3b64c45beb7c73f0f8f645269777bbe878762006b90b50b48e2da430509","search_id":"approval_binding_map"} -->
# 研究检索导航

> 本报告仅展示查询路线、来源、命中定位与覆盖；所有科研判断由主研究者完成。

- 搜索标识：`approval_binding_map`
- 生成时间（协调世界时）：`2026-08-16T06:14:31.624296Z`

## 紧凑研究地图

> 跨路线按 Paper 去重；每个查询路线至多选一个尚未出现的最高排名代表项。完整原始命中保留在 `result.json`。

- Paper `P004` · TravelPlanner: A Benchmark for Real-World Planning with Language Agents；用途 `problem`；路线 `q001:paper_card_fts` #1；Card `paper-p004`（paper）；Evidence `ev-p004-failure-core`
- Paper `P071` · Agentic Plan Caching: Test-Time Memory for Fast and Cost-Efficient LLM Agents；用途 `problem`；路线 `q001:failure_card_fts` #1；Card `failure-plan-cache-semantic-false-positives`（failure）；Evidence `ev-p071-cache-false-positive-boundary`, `ev-p071-plan-template-reuse`
- Paper `P047` · tau2-Bench: Evaluating Conversational Agents in a Dual-Control Environment；用途 `problem`；路线 `q001:passage_hybrid` #1；Passage `P047:p0030:s0001`
- Paper `P049` · Reinforced Agent: Inference-Time Feedback for Tool-Calling Agents；用途 `problem`；路线 `q001:operator_card_fts` #1；Card `operator-bounded-preexecution-reviewer`（operator）；Evidence `ev-p049-bounded-review-loop`, `ev-p049-operator-core`
- Paper `P095` · Don't Ask the LLM to Track Freshness: A Deterministic Recipe for Memory Conflict Resolution；用途 `failure`；路线 `q002:failure_card_fts` #1；Card `failure-llm-freshness-judgment-prior-override-and-drift`（failure）；Evidence `ev-p095-matched-comparison`, `ev-p095-prior-override-drift`
- Paper `P083` · TAMAS: Benchmarking Adversarial Risks in Multi-Agent LLM Systems；用途 `failure`；路线 `q002:passage_hybrid` #1；Passage `P083:p0025:s0001`
- Paper `P072` · Structured Uncertainty guided Clarification for LLM Agents；用途 `failure`；路线 `q002:operator_card_fts` #2；Card `operator-cost-penalized-structured-clarification`（operator）；Evidence `ev-p072-compute-boundary`, `ev-p072-structured-clarification-gate`, `ev-p072-unstructured-clarification-failure`
- Paper `P007` · tau-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains；用途 `failure`；路线 `q002:paper_card_fts` #3；Card `paper-tau-bench`（paper）；Evidence `ev-p007-repeat-reliability-collapse`, `ev-p007-terminal-state-evaluation`
- Paper `P098` · Beyond Objective Equivalence: Constraint Injection for LLM-Based Optimization Modeling on Vehicle Routing Problems；用途 `operator`；路线 `q003:operator_card_fts` #1；Card `operator-labeled-probe-injection-dual-verifier`（operator）；Evidence `ev-p098-constraint-injection`, `ev-p098-diff-leak-550`, `ev-p098-nonbinding-blindness`
- Paper `P038` · AgentDojo: A Dynamic Environment to Evaluate Prompt Injection Attacks and Defenses for LLM Agents；用途 `operator`；路线 `q003:paper_card_fts` #1；Card `paper-p038`（paper）；Evidence `ev-p038-operator-core`
- Paper `P077` · ArCHer: Training Language Model Agents via Hierarchical Multi-Turn RL；用途 `operator`；路线 `q003:passage_hybrid` #2；Passage `P077:p0004:s0002`
- Paper `P030` · STALE: Can LLM Agents Know When Their Memories Are No Longer Valid?；用途 `operator`；路线 `q003:failure_card_fts` #2；Card `failure-retrieved-update-lacks-decision-authority`（failure）；Evidence `ev-p030-failure-core`, `ev-p030-recognition-application-gap`
- Paper `P037` · ToolSandbox: A Stateful, Conversational, Interactive Evaluation Benchmark for LLM Tool Use Capabilities；用途 `prior`；路线 `q004:paper_card_fts` #1；Card `paper-p037`（paper）；Evidence `ev-p037-evaluation-core`
- Paper `P003` · Language Agent Tree Search Unifies Reasoning, Acting, and Planning in Language Models；用途 `prior`；路线 `q004:operator_card_fts` #1；Card `operator-feedback-backpropagated-tree-search`（operator）；Evidence `ev-p003-search-control-loop`
- Paper `P091` · Temporal Validity in Retrieval Memory: Eliminating Stale-Fact Errors for AI Agents over Evolving Knowledge；用途 `prior`；路线 `q004:failure_card_fts` #1；Card `failure-cosine-cannot-separate-contradiction-from-duplicate`（failure）；Evidence `ev-p091-cosine-auroc`, `ev-p091-retain-fabrication`
- Paper `P076` · Multi-Agent Systems Execute Arbitrary Malicious Code；用途 `prior`；路线 `q004:passage_hybrid` #1；Passage `P076:p0010:s0001`
- Paper `P042` · LiveResearchBench: A Live Benchmark for User-Centric Deep Research in the Wild；用途 `measurement`；路线 `q005:paper_card_fts` #4；Card `paper-p042`（paper）；Evidence `ev-p042-evaluation-core`
- Paper `P008` · Agent Security Bench (ASB): Formalizing and Benchmarking Attacks and Defenses in LLM-based Agents；用途 `measurement`；路线 `q005:passage_hybrid` #1；Passage `P008:p0023:s0001`
- Paper `P060` · Unifying Inference-Time Planning Language Generation；用途 `measurement`；路线 `q005:failure_card_fts` #2；Card `failure-natural-language-ir-hurts-formal-planning`（failure）；Evidence `ev-p060-formal-ir-solver`, `ev-p060-ir-result-and-nl-failure`
- Paper `P027` · Verified Critical Step Optimization for LLM Agents；用途 `measurement`；路线 `q005:operator_card_fts` #3；Card `operator-verified-single-branch-repair`（operator）；Evidence `ev-p027-operator-core`

- 代表项：20 / 去重 Paper：76

## 查询与路线覆盖

### q001 · problem

- 原始查询：`LLM tool agent human approval plan changes after confirmation authorization scope`
- 规范化查询：`"LLM" OR "tool" OR "agent" OR "human" OR "approval" OR "plan" OR "changes" OR "after" OR "confirmation" OR "authorization" OR "scope"`
- 路线 `paper_card_fts`：15 条；降级 false（无）
- 路线 `failure_card_fts`：15 条；降级 false（无）
- 路线 `passage_hybrid`：15 条；降级 false（无）
- 路线 `operator_card_fts`：15 条；降级 false（无）

### q002 · failure

- 原始查询：`agent reuses user confirmation after tool arguments target amount changed approval drift`
- 规范化查询：`"agent" OR "reuses" OR "user" OR "confirmation" OR "after" OR "tool" OR "arguments" OR "target" OR "amount" OR "changed" OR "approval" OR "drift"`
- 路线 `failure_card_fts`：15 条；降级 false（无）
- 路线 `passage_hybrid`：15 条；降级 false（无）
- 路线 `operator_card_fts`：15 条；降级 false（无）
- 路线 `paper_card_fts`：15 条；降级 false（无）

### q003 · operator

- 原始查询：`bind approval to exact action manifest hash capability token reauthorize diff agent`
- 规范化查询：`"bind" OR "approval" OR "to" OR "exact" OR "action" OR "manifest" OR "hash" OR "capability" OR "token" OR "reauthorize" OR "diff" OR "agent"`
- 路线 `operator_card_fts`：15 条；降级 false（无）
- 路线 `paper_card_fts`：15 条；降级 false（无）
- 路线 `passage_hybrid`：15 条；降级 false（无）
- 路线 `failure_card_fts`：15 条；降级 false（无）

### q004 · prior

- 原始查询：`human in the loop LLM agent confirmation authorization unsafe tool action benchmark`
- 规范化查询：`"human" OR "in" OR "the" OR "loop" OR "LLM" OR "agent" OR "confirmation" OR "authorization" OR "unsafe" OR "tool" OR "action" OR "benchmark"`
- 路线 `paper_card_fts`：15 条；降级 false（无）
- 路线 `operator_card_fts`：15 条；降级 false（无）
- 路线 `failure_card_fts`：15 条；降级 false（无）
- 路线 `passage_hybrid`：15 条；降级 false（无）

### q005 · measurement

- 原始查询：`counterfactual plan mutation after user approval tool agent consent benchmark`
- 规范化查询：`"counterfactual" OR "plan" OR "mutation" OR "after" OR "user" OR "approval" OR "tool" OR "agent" OR "consent" OR "benchmark"`
- 路线 `paper_card_fts`：15 条；降级 false（无）
- 路线 `passage_hybrid`：15 条；降级 false（无）
- 路线 `failure_card_fts`：15 条；降级 false（无）
- 路线 `operator_card_fts`：15 条；降级 false（无）

## 覆盖诊断

- 去重 Card：120
- 去重 Evidence：158
- 去重 Passage：63
- 命中 Paper：76
- 原始观测：300
- 带机械噪声标记的观测：0
