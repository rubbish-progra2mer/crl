<!-- CRL_RESEARCH_SEARCH_META {"created_at_utc":"2026-08-13T09:19:57.594000Z","request_fingerprint_sha256":"f9a11c3926f9a6a09a9cbb990b59abcf1985b20aeaeac5a22d8e1c69a2bf0443","result_json_sha256":"b86abc54213723cfe725d110a2bd6a8d982ac9bc277fe72f32cba011036d2e45","search_id":"observation_coverage_proof_v002"} -->
# 研究检索导航

> 本报告仅展示查询路线、来源、命中定位与覆盖；所有科研判断由主研究者完成。

- 搜索标识：`observation_coverage_proof_v002`
- 生成时间（协调世界时）：`2026-08-13T09:19:57.594000Z`

## 紧凑研究地图

> 跨路线按 Paper 去重；每个查询路线至多选一个尚未出现的最高排名代表项。完整原始命中保留在 `result.json`。

- Paper `P074` · ToolGate: Contract-Grounded and Verified Tool Execution for LLMs；用途 `failure`；路线 `q001:failure_card_fts` #1；Card `failure-incomplete-tool-contracts-false-verified-state`（failure）；Evidence `ev-p074-contract-state-commit`, `ev-p074-missing-schema-true-postcondition`
- Paper `P031` · Agent Memory: Characterization and System Implications of Stateful Long-Horizon Workloads；用途 `failure`；路线 `q001:passage_hybrid` #1；Passage `P031:p0003:s0001`
- Paper `P079` · Learning to Contextualize Web Pages for Enhanced Decision Making by LLM Agents；用途 `failure`；路线 `q001:operator_card_fts` #1；Card `operator-action-preserving-observation-contextualization`（operator）；Evidence `ev-p079-action-conditioned-contextualization`, `ev-p079-ground-truth-action-retry`, `ev-p079-unseen-ui-boundary`
- Paper `P090` · From Single to Multi-Granularity: Toward Long-Term Memory Association and Selection of Conversational Agents；用途 `failure`；路线 `q001:paper_card_fts` #1；Card `paper-p090`（paper）；Evidence `ev-p090-association-graph`, `ev-p090-entropy-router`, `ev-p090-fixed-granularity-selection`
- Paper `P038` · AgentDojo: A Dynamic Environment to Evaluate Prompt Injection Attacks and Defenses for LLM Agents；用途 `problem`；路线 `q002:paper_card_fts` #1；Card `paper-p038`（paper）；Evidence `ev-p038-operator-core`
- Paper `P030` · STALE: Can LLM Agents Know When Their Memories Are No Longer Valid?；用途 `problem`；路线 `q002:failure_card_fts` #1；Card `failure-retrieved-update-lacks-decision-authority`（failure）；Evidence `ev-p030-failure-core`, `ev-p030-recognition-application-gap`
- Paper `P072` · Structured Uncertainty guided Clarification for LLM Agents；用途 `problem`；路线 `q002:passage_hybrid` #1；Passage `P072:p0005:s0001`
- Paper `P037` · ToolSandbox: A Stateful, Conversational, Interactive Evaluation Benchmark for LLM Tool Use Capabilities；用途 `problem`；路线 `q002:operator_card_fts` #1；Card `operator-milestone-dag-trajectory-evaluation`（operator）；Evidence `ev-p037-evaluation-core`, `ev-p037-minefield-violation`
- Paper `P004` · TravelPlanner: A Benchmark for Real-World Planning with Language Agents；用途 `measurement`；路线 `q003:paper_card_fts` #1；Card `paper-p004`（paper）；Evidence `ev-p004-failure-core`
- Paper `P099` · Verus-SpecGym: An Agentic Environment for Evaluating Specification Autoformalization；用途 `measurement`；路线 `q003:passage_hybrid` #1；Passage `P099:p0012:s0001`
- Paper `P085` · Retrieval Models Aren't Tool-Savvy: Benchmarking Tool Retrieval for Large Language Models；用途 `measurement`；路线 `q003:failure_card_fts` #1；Card `failure-large-corpus-tool-retrieval-breaks-oracle-menu`（failure）；Evidence `ev-p085-large-corpus-scale`, `ev-p085-non-exhaustive-label`, `ev-p085-retrieval-completeness-failure`
- Paper `P086` · Meta-Tool: Unleash Open-World Function Calling Capabilities of General-Purpose Large Language Models；用途 `measurement`；路线 `q003:operator_card_fts` #1；Card `operator-required-parameter-description-tool-retrieval`（operator）；Evidence `ev-p086-hypothesize-retrieve-invoke`, `ev-p086-near-identical-distribution`, `ev-p086-required-parameter-score`
- Paper `P001` · ReAct: Synergizing Reasoning and Acting in Language Models；用途 `operator`；路线 `q004:operator_card_fts` #3；Card `operator-reason-action-interleaving`（operator）；Evidence `ev-p001-react-interleaved`
- Paper `P006` · An LLM Compiler for Parallel Function Calling；用途 `operator`；路线 `q004:paper_card_fts` #2；Card `paper-llmcompiler`（paper）；Evidence `ev-p006-dependency-dag-dispatch`, `ev-p006-shared-prompt-comparison-boundary`, `ev-p006-token-cost-accounting`
- Paper `P044` · DEER: A Benchmark for Evaluating Deep Research Agents on Expert Report Generation；用途 `operator`；路线 `q004:passage_hybrid` #10；Passage `P044:p0037:s0001`
- Paper `P065` · Group-in-Group Policy Optimization for LLM Agent Training；用途 `operator`；路线 `q004:failure_card_fts` #1；Card `failure-anchor-state-credit-needs-state-recurrence`（failure）；Evidence `ev-p065-anchor-state-credit`, `ev-p065-state-recurrence-boundary`
- Paper `P073` · Uncertainty Calibration for Tool-Using Language Agents；用途 `prior`；路线 `q005:paper_card_fts` #2；Card `paper-p073`（paper）；Evidence `ev-p073-execution-supervised-probe`, `ev-p073-internal-confidence-misalignment`
- Paper `P007` · tau-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains；用途 `prior`；路线 `q005:operator_card_fts` #4；Card `operator-terminal-state-reliability-evaluation`（operator）；Evidence `ev-p007-terminal-state-evaluation`
- Paper `P036` · tau-Knowledge: Evaluating Conversational Agents over Unstructured Knowledge；用途 `prior`；路线 `q005:failure_card_fts` #3；Card `failure-gold-context-does-not-solve-knowledge-use`（failure）；Evidence `ev-p036-failure-core`
- Paper `P059` · Multi-Agent Collaboration via Evolving Orchestration；用途 `prior`；路线 `q005:passage_hybrid` #13；Passage `P059:p0012:s0001`

- 代表项：20 / 去重 Paper：72

## 查询与路线覆盖

### q001 · failure

- 原始查询：`agent tool observation incomplete pagination permissions stale freshness successful read absence unknown`
- 规范化查询：`"agent" OR "tool" OR "observation" OR "incomplete" OR "pagination" OR "permissions" OR "stale" OR "freshness" OR "successful" OR "read" OR "absence" OR "unknown"`
- 路线 `failure_card_fts`：16 条；降级 false（无）
- 路线 `passage_hybrid`：16 条；降级 false（无）
- 路线 `operator_card_fts`：16 条；降级 false（无）
- 路线 `paper_card_fts`：16 条；降级 false（无）

### q002 · problem

- 原始查询：`tool using LLM agent absence from partial observation not evidence of nonexistence belief state`
- 规范化查询：`"tool" OR "using" OR "LLM" OR "agent" OR "absence" OR "from" OR "partial" OR "observation" OR "not" OR "evidence" OR "of" OR "nonexistence" OR "belief" OR "state"`
- 路线 `paper_card_fts`：16 条；降级 false（无）
- 路线 `failure_card_fts`：16 条；降级 false（无）
- 路线 `passage_hybrid`：16 条；降级 false（无）
- 路线 `operator_card_fts`：16 条；降级 false（无）

### q003 · measurement

- 原始查询：`coverage pagination exhaustion permission scope freshness read success unknown open world tool benchmark`
- 规范化查询：`"coverage" OR "pagination" OR "exhaustion" OR "permission" OR "scope" OR "freshness" OR "read" OR "success" OR "unknown" OR "open" OR "world" OR "tool" OR "benchmark"`
- 路线 `paper_card_fts`：16 条；降级 false（无）
- 路线 `passage_hybrid`：16 条；降级 false（无）
- 路线 `failure_card_fts`：16 条；降级 false（无）
- 路线 `operator_card_fts`：16 条；降级 false（无）

### q004 · operator

- 原始查询：`coverage certificate observation completeness proof obligations belief state tool agent`
- 规范化查询：`"coverage" OR "certificate" OR "observation" OR "completeness" OR "proof" OR "obligations" OR "belief" OR "state" OR "tool" OR "agent"`
- 路线 `operator_card_fts`：16 条；降级 false（无）
- 路线 `paper_card_fts`：16 条；降级 false（无）
- 路线 `passage_hybrid`：16 条；降级 false（无）
- 路线 `failure_card_fts`：16 条；降级 false（无）

### q005 · prior

- 原始查询：`Agent-BRACE BeliefMem NeSyFS belief state uncertainty tool agent`
- 规范化查询：`"Agent" OR "BRACE" OR "BeliefMem" OR "NeSyFS" OR "belief" OR "state" OR "uncertainty" OR "tool"`
- 路线 `paper_card_fts`：16 条；降级 false（无）
- 路线 `operator_card_fts`：16 条；降级 false（无）
- 路线 `failure_card_fts`：16 条；降级 false（无）
- 路线 `passage_hybrid`：16 条；降级 false（无）

## 覆盖诊断

- 去重 Card：117
- 去重 Evidence：153
- 去重 Passage：64
- 命中 Paper：72
- 原始观测：320
- 带机械噪声标记的观测：3
