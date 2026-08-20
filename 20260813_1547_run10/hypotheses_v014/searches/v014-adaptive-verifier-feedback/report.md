<!-- CRL_RESEARCH_SEARCH_META {"created_at_utc":"2026-08-13T12:16:18.784973Z","request_fingerprint_sha256":"30ee49635ae15ab438b1af81922570a5ca9588d764e918ad42246b2cbeb2cded","result_json_sha256":"58995e9acfd7b0def0b13ede993ca708808a0fcf0f85471dfe450a634e9103c2","search_id":"v014-adaptive-verifier-feedback"} -->
# 研究检索导航

> 本报告仅展示查询路线、来源、命中定位与覆盖；所有科研判断由主研究者完成。

- 搜索标识：`v014-adaptive-verifier-feedback`
- 生成时间（协调世界时）：`2026-08-13T12:16:18.784973Z`

## 紧凑研究地图

> 跨路线按 Paper 去重；每个查询路线至多选一个尚未出现的最高排名代表项。完整原始命中保留在 `result.json`。

- Paper `P033` · Self-Refine: Iterative Refinement with Self-Feedback；用途 `problem`；路线 `q001:paper_card_fts` #1；Card `paper-p033`（paper）；Evidence `ev-p033-operator-core`
- Paper `P057` · Automated Design of Agentic Systems；用途 `problem`；路线 `q001:failure_card_fts` #1；Card `failure-reused-selection-feedback-in-agent-search`（failure）；Evidence `ev-p057-search-evaluation-budget`
- Paper `P032` · CRITIC: Large Language Models Can Self-Correct with Tool-Interactive Critiquing；用途 `problem`；路线 `q001:passage_hybrid` #1；Passage `P032:p0002:s0001`
- Paper `P058` · AFlow: Automating Agentic Workflow Generation；用途 `problem`；路线 `q001:operator_card_fts` #1；Card `operator-mcts-executable-workflow-refinement`（operator）；Evidence `ev-p058-mcts-workflow-search`, `ev-p058-validation-selection-loop`
- Paper `P034` · RefineBench: Evaluating Refinement Capability of Language Models via Checklists；用途 `failure`；路线 `q002:failure_card_fts` #1；Card `failure-iterative-refinement-corrupts-correct-output`（failure）；Evidence `ev-p034-failure-core`
- Paper `P040` · From Confident Closing to Silent Failure: Characterizing False Success in LLM Agents；用途 `failure`；路线 `q002:passage_hybrid` #1；Passage `P040:p0002:s0002`
- Paper `P042` · LiveResearchBench: A Live Benchmark for User-Centric Deep Research in the Wild；用途 `failure`；路线 `q002:operator_card_fts` #1；Card `operator-decomposed-research-evidence-evaluation`（operator）；Evidence `ev-p042-evaluation-core`
- Paper `P039` · ToolFailBench: Diagnosing Tool-Use Failures in LLM Agents；用途 `failure`；路线 `q002:paper_card_fts` #2；Card `paper-p039`（paper）；Evidence `ev-p039-failure-core`
- Paper `P049` · Reinforced Agent: Inference-Time Feedback for Tool-Calling Agents；用途 `operator`；路线 `q003:operator_card_fts` #3；Card `operator-bounded-preexecution-reviewer`（operator）；Evidence `ev-p049-bounded-review-loop`, `ev-p049-operator-core`
- Paper `P075` · Unveiling Privacy Risks in LLM Agent Memory；用途 `operator`；路线 `q003:paper_card_fts` #1；Card `paper-p075`（paper）；Evidence `ev-p075-measured-memory-extraction`, `ev-p075-retrieve-to-action-leakage`, `ev-p075-session-isolation-boundary`
- Paper `P020` · AgentTTS: Large Language Model Agent for Test-time Compute-optimal Scaling Strategy in Complex Tasks；用途 `operator`；路线 `q003:passage_hybrid` #9；Passage `P020:p0004:s0002`
- Paper `P013` · Large Language Models Cannot Self-Correct Reasoning Yet；用途 `operator`；路线 `q003:failure_card_fts` #3；Card `failure-intrinsic-self-correction-degradation`（failure）；Evidence `ev-p013-intrinsic-self-correction-degrades`, `ev-p013-oracle-free-equal-budget-boundary`
- Paper `P077` · ArCHer: Training Language Model Agents via Hierarchical Multi-Turn RL；用途 `prior`；路线 `q004:paper_card_fts` #1；Card `paper-p077`（paper）；Evidence `ev-p077-hierarchical-utterance-critic-token-actor`, `ev-p077-oracle-reward-hacking-boundary`, `ev-p077-trajectory-only-sample-efficiency`
- Paper `P100` · How Many Tools Should an LLM Agent See? A Chance-Corrected Answer；用途 `prior`；路线 `q004:operator_card_fts` #2；Card `operator-chance-corrected-depth-reward`（operator）；Evidence `ev-p100-bor-self-pruning`, `ev-p100-fixed-depth-buckets`
- Paper `P025` · Unlocking the Power of Multi-Agent LLM for Reasoning: From Lazy Agents to Deliberation；用途 `prior`；路线 `q004:failure_card_fts` #2；Card `failure-lazy-agent-effective-single-agent-collapse`（failure）；Evidence `ev-p025-failure-core`
- Paper `P035` · Holistic Agent Leaderboard: The Missing Infrastructure for AI Agent Evaluation；用途 `prior`；路线 `q004:passage_hybrid` #1；Passage `P035:p0002:s0001`
- Paper `P093` · Collapse of Dense Retrievers: Short, Early, and Literal Biases Outranking Factual Evidence；用途 `measurement`；路线 `q005:paper_card_fts` #1；Card `paper-p093`（paper）；Evidence `ev-p093-foil-collapse`, `ev-p093-paired-protocol`, `ev-p093-poison-rag`
- Paper `P097` · ReLoop: Structured Modeling and Behavioral Verification for Reliable LLM-Based Optimization；用途 `measurement`；路线 `q005:passage_hybrid` #1；Passage `P097:p0006:s0002`
- Paper `P082` · Toolformer: Language Models Can Teach Themselves to Use Tools；用途 `measurement`；路线 `q005:failure_card_fts` #2；Card `failure-likelihood-utility-does-not-guarantee-agent-utility`（failure）；Evidence `ev-p082-chaining-cost-sparsity-boundary`, `ev-p082-future-token-loss-filtered-calls`, `ev-p082-top-k-single-call-boundary`
- Paper `P056` · GPTSwarm: Language Agents as Optimizable Graphs；用途 `measurement`；路线 `q005:operator_card_fts` #5；Card `operator-utility-optimized-agent-graph`（operator）；Evidence `ev-p056-graph-optimization`, `ev-p056-same-set-crosswords`

- 代表项：20 / 去重 Paper：99

## 查询与路线覆盖

### q001 · problem

- 原始查询：`adaptive verifier feedback leakage in repeatedly repairing text and tool agents`
- 规范化查询：`"adaptive" OR "verifier" OR "feedback" OR "leakage" OR "in" OR "repeatedly" OR "repairing" OR "text" OR "and" OR "tool" OR "agents"`
- 路线 `paper_card_fts`：99 条；降级 false（无）
- 路线 `failure_card_fts`：63 条；降级 false（无）
- 路线 `passage_hybrid`：1200 条；降级 false（无）
- 路线 `operator_card_fts`：66 条；降级 false（无）

### q002 · failure

- 原始查询：`agent reconstructs hidden evaluation target from repeated scores failures counterexamples or judge feedback`
- 规范化查询：`"agent" OR "reconstructs" OR "hidden" OR "evaluation" OR "target" OR "from" OR "repeated" OR "scores" OR "failures" OR "counterexamples" OR "or" OR "judge" OR "feedback"`
- 路线 `failure_card_fts`：46 条；降级 false（无）
- 路线 `passage_hybrid`：1200 条；降级 false（无）
- 路线 `operator_card_fts`：66 条；降级 false（无）
- 路线 `paper_card_fts`：78 条；降级 false（无）

### q003 · operator

- 原始查询：`reusable holdout differential privacy feedback channel budget ladder selective disclosure`
- 规范化查询：`"reusable" OR "holdout" OR "differential" OR "privacy" OR "feedback" OR "channel" OR "budget" OR "ladder" OR "selective" OR "disclosure"`
- 路线 `operator_card_fts`：17 条；降级 false（无）
- 路线 `paper_card_fts`：20 条；降级 false（无）
- 路线 `passage_hybrid`：1200 条；降级 false（无）
- 路线 `failure_card_fts`：18 条；降级 false（无）

### q004 · prior

- 原始查询：`adaptive data analysis reusable holdout leaderboard CEGIS hidden tests reward hacking agent benchmarks`
- 规范化查询：`"adaptive" OR "data" OR "analysis" OR "reusable" OR "holdout" OR "leaderboard" OR "CEGIS" OR "hidden" OR "tests" OR "reward" OR "hacking" OR "agent" OR "benchmarks"`
- 路线 `paper_card_fts`：64 条；降级 false（无）
- 路线 `operator_card_fts`：44 条；降级 false（无）
- 路线 `failure_card_fts`：34 条；降级 false（无）
- 路线 `passage_hybrid`：1200 条；降级 false（无）

### q005 · measurement

- 原始查询：`paired public feedback repair utility versus sealed holdout generalization and target reconstruction`
- 规范化查询：`"paired" OR "public" OR "feedback" OR "repair" OR "utility" OR "versus" OR "sealed" OR "holdout" OR "generalization" OR "and" OR "target" OR "reconstruction"`
- 路线 `paper_card_fts`：99 条；降级 false（无）
- 路线 `passage_hybrid`：1200 条；降级 false（无）
- 路线 `failure_card_fts`：63 条；降级 false（无）
- 路线 `operator_card_fts`：66 条；降级 false（无）

## 覆盖诊断

- 去重 Card：228
- 去重 Evidence：224
- 去重 Passage：2599
- 命中 Paper：99
- 原始观测：6843
- 带机械噪声标记的观测：592
