<!-- CRL_RESEARCH_SEARCH_META {"created_at_utc":"2026-08-16T10:44:26.345564Z","request_fingerprint_sha256":"25c014cf914c2d9301bee6746ad36e8f36fcd9e742418268f9edb46432139311","result_json_sha256":"ec8031dbc23b537a83fcb15740552d95912e1a2e60234041fc1bb9025073663d","search_id":"trajectory-observation-uq-001"} -->
# 研究检索导航

> 本报告仅展示查询路线、来源、命中定位与覆盖；所有科研判断由主研究者完成。

- 搜索标识：`trajectory-observation-uq-001`
- 生成时间（协调世界时）：`2026-08-16T10:44:26.345564Z`

## 紧凑研究地图

> 跨路线按 Paper 去重；每个查询路线至多选一个尚未出现的最高排名代表项。完整原始命中保留在 `result.json`。

- Paper `P038` · AgentDojo: A Dynamic Environment to Evaluate Prompt Injection Attacks and Defenses for LLM Agents；用途 `problem`；路线 `q001:paper_card_fts` #1；Card `paper-p038`（paper）；Evidence `ev-p038-operator-core`
- Paper `P083` · TAMAS: Benchmarking Adversarial Risks in Multi-Agent LLM Systems；用途 `problem`；路线 `q001:failure_card_fts` #1；Card `failure-multi-agent-adversarial-coordination-spans-trust-surfaces`（failure）；Evidence `ev-p083-lightweight-defense-failure`, `ev-p083-simulated-tool-boundary`, `ev-p083-three-surface-adversarial-failure`
- Paper `P019` · STeCa: Step-level Trajectory Calibration for LLM Agent Learning；用途 `problem`；路线 `q001:passage_hybrid` #1；Passage `P019:p0002:s0001`
- Paper `P001` · ReAct: Synergizing Reasoning and Acting in Language Models；用途 `problem`；路线 `q001:operator_card_fts` #1；Card `operator-reason-action-interleaving`（operator）；Evidence `ev-p001-react-interleaved`
- Paper `P081` · Self-Consistency Improves Chain of Thought Reasoning in Language Models；用途 `failure`；路线 `q002:failure_card_fts` #1；Card `failure-interactive-gains-collapse-against-independent-sampling`（failure）；Evidence `ev-p081-fixed-answer-space-boundary`, `ev-p081-forty-sample-baseline`, `ev-p081-independent-path-majority-aggregation`
- Paper `P074` · ToolGate: Contract-Grounded and Verified Tool Execution for LLMs；用途 `failure`；路线 `q002:passage_hybrid` #1；Passage `P074:p0005:s0002`
- Paper `P037` · ToolSandbox: A Stateful, Conversational, Interactive Evaluation Benchmark for LLM Tool Use Capabilities；用途 `failure`；路线 `q002:operator_card_fts` #2；Card `operator-milestone-dag-trajectory-evaluation`（operator）；Evidence `ev-p037-evaluation-core`, `ev-p037-minefield-violation`
- Paper `P047` · tau2-Bench: Evaluating Conversational Agents in a Dual-Control Environment；用途 `failure`；路线 `q002:paper_card_fts` #3；Card `paper-p047`（paper）；Evidence `ev-p047-evaluation-core`
- Paper `P093` · Collapse of Dense Retrievers: Short, Early, and Literal Biases Outranking Factual Evidence；用途 `operator`；路线 `q003:operator_card_fts` #1；Card `operator-paired-single-factor-bias-decomposition`（operator）；Evidence `ev-p093-foil-collapse`, `ev-p093-paired-protocol`
- Paper `P039` · ToolFailBench: Diagnosing Tool-Use Failures in LLM Agents；用途 `operator`；路线 `q003:paper_card_fts` #1；Card `paper-p039`（paper）；Evidence `ev-p039-failure-core`
- Paper `P077` · ArCHer: Training Language Model Agents via Hierarchical Multi-Turn RL；用途 `operator`；路线 `q003:passage_hybrid` #1；Passage `P077:p0012:s0002`
- Paper `P026` · Agent Lightning: Train ANY AI Agents with Reinforcement Learning；用途 `operator`；路线 `q003:failure_card_fts` #3；Card `failure-uniform-terminal-return-erases-step-credit`（failure）；Evidence `ev-p026-transition-decomposition`, `ev-p026-uniform-terminal-return`
- Paper `P072` · Structured Uncertainty guided Clarification for LLM Agents；用途 `prior`；路线 `q004:paper_card_fts` #1；Card `paper-p072`（paper）；Evidence `ev-p072-compute-boundary`, `ev-p072-structured-clarification-gate`, `ev-p072-unstructured-clarification-failure`
- Paper `P079` · Learning to Contextualize Web Pages for Enhanced Decision Making by LLM Agents；用途 `prior`；路线 `q004:operator_card_fts` #1；Card `operator-action-preserving-observation-contextualization`（operator）；Evidence `ev-p079-action-conditioned-contextualization`, `ev-p079-ground-truth-action-retry`, `ev-p079-unseen-ui-boundary`
- Paper `P100` · How Many Tools Should an LLM Agent See? A Chance-Corrected Answer；用途 `prior`；路线 `q004:failure_card_fts` #1；Card `failure-fixed-shortlist-depth-masks-hard-query-zero`（failure）；Evidence `ev-p100-fixed-depth-buckets`, `ev-p100-weak-scorer-collapse`
- Paper `P051` · Large Language Models Can Solve Real-World Planning Rigorously with Formal Verification Tools；用途 `prior`；路线 `q004:passage_hybrid` #4；Passage `P051:p0021:s0001`
- Paper `P091` · Temporal Validity in Retrieval Memory: Eliminating Stale-Fact Errors for AI Agents over Evolving Knowledge；用途 `measurement`；路线 `q005:paper_card_fts` #1；Card `paper-p091`（paper）；Evidence `ev-p091-cosine-auroc`, `ev-p091-retain-fabrication`, `ev-p091-supersession-rule`
- Paper `P032` · CRITIC: Large Language Models Can Self-Correct with Tool-Interactive Critiquing；用途 `measurement`；路线 `q005:passage_hybrid` #1；Passage `P032:p0023:s0001`
- Paper `P094` · Evaluating Memory in LLM Agents via Incremental Multi-Turn Interactions；用途 `measurement`；路线 `q005:failure_card_fts` #2；Card `failure-selective-forgetting-collapses-with-context-length`（failure）；Evidence `ev-p094-sf-guardrails`, `ev-p094-sf-length-collapse`
- Paper `P073` · Uncertainty Calibration for Tool-Using Language Agents；用途 `measurement`；路线 `q005:operator_card_fts` #1；Card `operator-execution-supervised-prompt-trace-calibration`（operator）；Evidence `ev-p073-execution-supervised-probe`, `ev-p073-internal-confidence-misalignment`

- 代表项：20 / 去重 Paper：91

## 查询与路线覆盖

### q001 · problem

- 原始查询：`LLM agent trajectory uncertainty tool observation environment stochasticity`
- 规范化查询：`"LLM" OR "agent" OR "trajectory" OR "uncertainty" OR "tool" OR "observation" OR "environment" OR "stochasticity"`
- 路线 `paper_card_fts`：30 条；降级 false（无）
- 路线 `failure_card_fts`：30 条；降级 false（无）
- 路线 `passage_hybrid`：80 条；降级 false（无）
- 路线 `operator_card_fts`：30 条；降级 false（无）

### q002 · failure

- 原始查询：`trajectory self-consistency confounds policy sampling with stochastic user simulator and tool outputs`
- 规范化查询：`"trajectory" OR "self" OR "consistency" OR "confounds" OR "policy" OR "sampling" OR "with" OR "stochastic" OR "user" OR "simulator" OR "and" OR "tool" OR "outputs"`
- 路线 `failure_card_fts`：30 条；降级 false（无）
- 路线 `passage_hybrid`：80 条；降级 false（无）
- 路线 `operator_card_fts`：30 条；降级 false（无）
- 路线 `paper_card_fts`：30 条；降级 false（无）

### q003 · operator

- 原始查询：`paired replay common random numbers crossed policy environment seeds uncertainty decomposition`
- 规范化查询：`"paired" OR "replay" OR "common" OR "random" OR "numbers" OR "crossed" OR "policy" OR "environment" OR "seeds" OR "uncertainty" OR "decomposition"`
- 路线 `operator_card_fts`：27 条；降级 false（无）
- 路线 `paper_card_fts`：25 条；降级 false（无）
- 路线 `passage_hybrid`：80 条；降级 false（无）
- 路线 `failure_card_fts`：20 条；降级 false（无）

### q004 · prior

- 原始查询：`observation uncertainty agent UQ trajectory resampling common random numbers`
- 规范化查询：`"observation" OR "uncertainty" OR "agent" OR "UQ" OR "trajectory" OR "resampling" OR "common" OR "random" OR "numbers"`
- 路线 `paper_card_fts`：30 条；降级 false（无）
- 路线 `operator_card_fts`：30 条；降级 false（无）
- 路线 `failure_card_fts`：30 条；降级 false（无）
- 路线 `passage_hybrid`：80 条；降级 false（无）

### q005 · measurement

- 原始查询：`selective prediction AUROC policy uncertainty environment uncertainty`
- 规范化查询：`"selective" OR "prediction" OR "AUROC" OR "policy" OR "uncertainty" OR "environment"`
- 路线 `paper_card_fts`：20 条；降级 false（无）
- 路线 `passage_hybrid`：80 条；降级 false（无）
- 路线 `failure_card_fts`：14 条；降级 false（无）
- 路线 `operator_card_fts`：20 条；降级 false（无）

## 覆盖诊断

- 去重 Card：160
- 去重 Evidence：196
- 去重 Passage：261
- 命中 Paper：91
- 原始观测：796
- 带机械噪声标记的观测：7
