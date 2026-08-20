<!-- CRL_RESEARCH_SEARCH_META {"created_at_utc":"2026-08-15T15:43:30.511836Z","request_fingerprint_sha256":"073ea07854a2921b53466cd6b648d7451e3abf93abf800a7d8a2541432ac05c8","result_json_sha256":"aea40d742bc7605685fc6d0048c1469e00dd04a901db212e995c364db70ec9c3","search_id":"broad_tool_robustness"} -->
# 研究检索导航

> 本报告仅展示查询路线、来源、命中定位与覆盖；所有科研判断由主研究者完成。

- 搜索标识：`broad_tool_robustness`
- 生成时间（协调世界时）：`2026-08-15T15:43:30.511836Z`

## 紧凑研究地图

> 跨路线按 Paper 去重；每个查询路线至多选一个尚未出现的最高排名代表项。完整原始命中保留在 `result.json`。

- Paper `P084` · On the Robustness of Agentic Function Calling；用途 `problem`；路线 `q001:paper_card_fts` #1；Card `paper-p084`（paper）；Evidence `ev-p084-expanded-toolkit-controlled-setting`, `ev-p084-expanded-toolkit-table`, `ev-p084-generated-tool-single-dataset-boundary`, `ev-p084-related-toolkit-error-types`
- Paper `P065` · Group-in-Group Policy Optimization for LLM Agent Training；用途 `problem`；路线 `q001:failure_card_fts` #1；Card `failure-anchor-state-credit-needs-state-recurrence`（failure）；Evidence `ev-p065-anchor-state-credit`, `ev-p065-state-recurrence-boundary`
- Paper `P049` · Reinforced Agent: Inference-Time Feedback for Tool-Calling Agents；用途 `problem`；路线 `q001:passage_hybrid` #1；Passage `P049:p0002:s0001`
- Paper `P037` · ToolSandbox: A Stateful, Conversational, Interactive Evaluation Benchmark for LLM Tool Use Capabilities；用途 `problem`；路线 `q001:operator_card_fts` #1；Card `operator-milestone-dag-trajectory-evaluation`（operator）；Evidence `ev-p037-evaluation-core`, `ev-p037-minefield-violation`
- Paper `P091` · Temporal Validity in Retrieval Memory: Eliminating Stale-Fact Errors for AI Agents over Evolving Knowledge；用途 `failure`；路线 `q002:failure_card_fts` #1；Card `failure-cosine-cannot-separate-contradiction-from-duplicate`（failure）；Evidence `ev-p091-cosine-auroc`, `ev-p091-retain-fabrication`
- Paper `P083` · TAMAS: Benchmarking Adversarial Risks in Multi-Agent LLM Systems；用途 `failure`；路线 `q002:passage_hybrid` #1；Passage `P083:p0009:s0001`
- Paper `P021` · In-the-Flow Agentic System Optimization for Effective Planning and Tool Use；用途 `failure`；路线 `q002:operator_card_fts` #1；Card `operator-outcome-trained-execution-state-planner`（operator）；Evidence `ev-p021-operator-core`
- Paper `P030` · STALE: Can LLM Agents Know When Their Memories Are No Longer Valid?；用途 `failure`；路线 `q002:paper_card_fts` #2；Card `paper-p030`（paper）；Evidence `ev-p030-failure-core`
- Paper `P073` · Uncertainty Calibration for Tool-Using Language Agents；用途 `operator`；路线 `q003:operator_card_fts` #1；Card `operator-execution-supervised-prompt-trace-calibration`（operator）；Evidence `ev-p073-execution-supervised-probe`, `ev-p073-internal-confidence-misalignment`
- Paper `P072` · Structured Uncertainty guided Clarification for LLM Agents；用途 `operator`；路线 `q003:paper_card_fts` #2；Card `paper-p072`（paper）；Evidence `ev-p072-compute-boundary`, `ev-p072-structured-clarification-gate`, `ev-p072-unstructured-clarification-failure`
- Paper `P032` · CRITIC: Large Language Models Can Self-Correct with Tool-Interactive Critiquing；用途 `operator`；路线 `q003:passage_hybrid` #8；Passage `P032:p0022:s0001`
- Paper `P033` · Self-Refine: Iterative Refinement with Self-Feedback；用途 `operator`；路线 `q003:failure_card_fts` #3；Card `failure-iterative-refinement-corrupts-correct-output`（failure）；Evidence `ev-p033-operator-core`
- Paper `P013` · Large Language Models Cannot Self-Correct Reasoning Yet；用途 `prior`；路线 `q004:paper_card_fts` #1；Card `paper-p013`（paper）；Evidence `ev-p013-intrinsic-self-correction-degrades`, `ev-p013-oracle-free-equal-budget-boundary`
- Paper `P100` · How Many Tools Should an LLM Agent See? A Chance-Corrected Answer；用途 `prior`；路线 `q004:operator_card_fts` #1；Card `operator-chance-corrected-depth-reward`（operator）；Evidence `ev-p100-bor-self-pruning`, `ev-p100-fixed-depth-buckets`
- Paper `P066` · The Berkeley Function Calling Leaderboard (BFCL): From Tool Use to Agentic Evaluation of Large Language Models；用途 `prior`；路线 `q004:failure_card_fts` #2；Card `failure-single-turn-tool-score-overstates-agent-competence`（failure）；Evidence `ev-p066-multiturn-state-evaluation`, `ev-p066-single-to-stateful-gap`
- Paper `P097` · ReLoop: Structured Modeling and Behavioral Verification for Reliable LLM-Based Optimization；用途 `prior`；路线 `q004:passage_hybrid` #2；Passage `P097:p0003:s0001`
- Paper `P036` · tau-Knowledge: Evaluating Conversational Agents over Unstructured Knowledge；用途 `measurement`；路线 `q005:paper_card_fts` #1；Card `paper-p036`（paper）；Evidence `ev-p036-failure-core`
- Paper `P038` · AgentDojo: A Dynamic Environment to Evaluate Prompt Injection Attacks and Defenses for LLM Agents；用途 `measurement`；路线 `q005:passage_hybrid` #5；Passage `P038:p0001:s0002`
- Paper `P079` · Learning to Contextualize Web Pages for Enhanced Decision Making by LLM Agents；用途 `measurement`；路线 `q005:failure_card_fts` #1；Card `failure-raw-observation-overload-hides-action-relevant-ui`（failure）；Evidence `ev-p079-action-conditioned-contextualization`, `ev-p079-ground-truth-action-retry`, `ev-p079-unseen-ui-boundary`
- Paper `P001` · ReAct: Synergizing Reasoning and Acting in Language Models；用途 `measurement`；路线 `q005:operator_card_fts` #4；Card `operator-reason-action-interleaving`（operator）；Evidence `ev-p001-react-interleaved`

- 代表项：20 / 去重 Paper：70

## 查询与路线覆盖

### q001 · problem

- 原始查询：`tool-using LLM agents robustness partial observability state tracking error recovery`
- 规范化查询：`"tool" OR "using" OR "LLM" OR "agents" OR "robustness" OR "partial" OR "observability" OR "state" OR "tracking" OR "error" OR "recovery"`
- 路线 `paper_card_fts`：12 条；降级 false（无）
- 路线 `failure_card_fts`：12 条；降级 false（无）
- 路线 `passage_hybrid`：18 条；降级 false（无）
- 路线 `operator_card_fts`：12 条；降级 false（无）

### q002 · failure

- 原始查询：`stale observations misleading tool outputs execution feedback ambiguity agent failure`
- 规范化查询：`"stale" OR "observations" OR "misleading" OR "tool" OR "outputs" OR "execution" OR "feedback" OR "ambiguity" OR "agent" OR "failure"`
- 路线 `failure_card_fts`：12 条；降级 false（无）
- 路线 `passage_hybrid`：18 条；降级 false（无）
- 路线 `operator_card_fts`：12 条；降级 false（无）
- 路线 `paper_card_fts`：12 条；降级 false（无）

### q003 · operator

- 原始查询：`belief state uncertainty selective verification re-observation causal consistency`
- 规范化查询：`"belief" OR "state" OR "uncertainty" OR "selective" OR "verification" OR "re" OR "observation" OR "causal" OR "consistency"`
- 路线 `operator_card_fts`：12 条；降级 false（无）
- 路线 `paper_card_fts`：12 条；降级 false（无）
- 路线 `passage_hybrid`：18 条；降级 false（无）
- 路线 `failure_card_fts`：12 条；降级 false（无）

### q004 · prior

- 原始查询：`tool agent verification self-correction tool error recovery stateful environments`
- 规范化查询：`"tool" OR "agent" OR "verification" OR "self" OR "correction" OR "error" OR "recovery" OR "stateful" OR "environments"`
- 路线 `paper_card_fts`：12 条；降级 false（无）
- 路线 `operator_card_fts`：12 条；降级 false（无）
- 路线 `failure_card_fts`：12 条；降级 false（无）
- 路线 `passage_hybrid`：18 条；降级 false（无）

### q005 · measurement

- 原始查询：`agent robustness benchmark tool perturbation observation corruption state change`
- 规范化查询：`"agent" OR "robustness" OR "benchmark" OR "tool" OR "perturbation" OR "observation" OR "corruption" OR "state" OR "change"`
- 路线 `paper_card_fts`：12 条；降级 false（无）
- 路线 `passage_hybrid`：18 条；降级 false（无）
- 路线 `failure_card_fts`：12 条；降级 false（无）
- 路线 `operator_card_fts`：12 条；降级 false（无）

## 覆盖诊断

- 去重 Card：104
- 去重 Evidence：134
- 去重 Passage：76
- 命中 Paper：70
- 原始观测：270
- 带机械噪声标记的观测：0
