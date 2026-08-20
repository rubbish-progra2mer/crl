<!-- CRL_RESEARCH_SEARCH_META {"created_at_utc":"2026-08-18T15:11:48.981180Z","request_fingerprint_sha256":"8ef955956ea63c42c2de1896112d70d9b1853644957415ead180ea9ad3d4d8e9","result_json_sha256":"f12d1ddbd3ed5e87a89b50bc6de4183851703a74ace121eec8f68ffdac300bd1","search_id":"orthogonal-frontier-v001"} -->
# 研究检索导航

> 本报告仅展示查询路线、来源、命中定位与覆盖；所有科研判断由主研究者完成。

- 搜索标识：`orthogonal-frontier-v001`
- 生成时间（协调世界时）：`2026-08-18T15:11:48.981180Z`

## 紧凑研究地图

> 跨路线按 Paper 去重；每个查询路线至多选一个尚未出现的最高排名代表项。完整原始命中保留在 `result.json`。

- Paper `P040` · From Confident Closing to Silent Failure: Characterizing False Success in LLM Agents；用途 `problem`；路线 `q001:paper_card_fts` #1；Card `paper-p040`（paper）；Evidence `ev-p040-failure-core`
- Paper `P071` · Agentic Plan Caching: Test-Time Memory for Fast and Cost-Efficient LLM Agents；用途 `problem`；路线 `q001:failure_card_fts` #2；Card `failure-plan-cache-semantic-false-positives`（failure）；Evidence `ev-p071-cache-false-positive-boundary`, `ev-p071-plan-template-reuse`
- Paper `P035` · Holistic Agent Leaderboard: The Missing Infrastructure for AI Agent Evaluation；用途 `problem`；路线 `q001:passage_hybrid` #2；Passage `P035:p0034:s0001`
- Paper `P041` · LLM Agents Already Know When to Call Tools - Even Without Reasoning；用途 `problem`；路线 `q001:operator_card_fts` #1；Card `operator-hidden-state-tool-necessity-prefill`（operator）；Evidence `ev-p041-operator-core`, `ev-p041-probe-prefill-steering`
- Paper `P091` · Temporal Validity in Retrieval Memory: Eliminating Stale-Fact Errors for AI Agents over Evolving Knowledge；用途 `failure`；路线 `q002:failure_card_fts` #1；Card `failure-cosine-cannot-separate-contradiction-from-duplicate`（failure）；Evidence `ev-p091-cosine-auroc`, `ev-p091-retain-fabrication`
- Paper `P073` · Uncertainty Calibration for Tool-Using Language Agents；用途 `failure`；路线 `q002:passage_hybrid` #1；Passage `P073:p0002:s0001`
- Paper `P030` · STALE: Can LLM Agents Know When Their Memories Are No Longer Valid?；用途 `failure`；路线 `q002:operator_card_fts` #1；Card `operator-write-side-state-adjudication`（operator）；Evidence `ev-p030-authorized-readout`, `ev-p030-failure-core`, `ev-p030-write-side-adjudication`
- Paper `P019` · STeCa: Step-level Trajectory Calibration for LLM Agent Learning；用途 `failure`；路线 `q002:paper_card_fts` #3；Card `paper-p019`（paper）；Evidence `ev-p019-ground-truth-calibration-oracle`, `ev-p019-step-level-calibration`
- Paper `P042` · LiveResearchBench: A Live Benchmark for User-Centric Deep Research in the Wild；用途 `operator`；路线 `q003:operator_card_fts` #2；Card `operator-decomposed-research-evidence-evaluation`（operator）；Evidence `ev-p042-evaluation-core`
- Paper `P044` · DEER: A Benchmark for Evaluating Deep Research Agents on Expert Report Generation；用途 `operator`；路线 `q003:paper_card_fts` #1；Card `paper-p044`（paper）；Evidence `ev-p044-evaluation-core`
- Paper `P068` · DeepFact: Co-Evolving Benchmarks and Agents for Deep Research Factuality；用途 `operator`；路线 `q003:passage_hybrid` #6；Passage `P068:p0001:s0001`
- Paper `P033` · Self-Refine: Iterative Refinement with Self-Feedback；用途 `operator`；路线 `q003:failure_card_fts` #1；Card `failure-iterative-refinement-corrupts-correct-output`（failure）；Evidence `ev-p033-operator-core`
- Paper `P072` · Structured Uncertainty guided Clarification for LLM Agents；用途 `prior`；路线 `q004:paper_card_fts` #1；Card `paper-p072`（paper）；Evidence `ev-p072-compute-boundary`, `ev-p072-structured-clarification-gate`, `ev-p072-unstructured-clarification-failure`
- Paper `P099` · Verus-SpecGym: An Agentic Environment for Evaluating Specification Autoformalization；用途 `prior`；路线 `q004:operator_card_fts` #2；Card `operator-four-bucket-executable-spec-testing`（operator）；Evidence `ev-p099-judge-miss`, `ev-p099-soundness-necessity`, `ev-p099-two-stage-check`
- Paper `P034` · RefineBench: Evaluating Refinement Capability of Language Models via Checklists；用途 `prior`；路线 `q004:failure_card_fts` #1；Card `failure-iterative-refinement-corrupts-correct-output`（failure）；Evidence `ev-p034-failure-core`
- Paper `P016` · Why Do Multi-Agent LLM Systems Fail?；用途 `prior`；路线 `q004:passage_hybrid` #1；Passage `P016:p0032:s0001`
- Paper `P049` · Reinforced Agent: Inference-Time Feedback for Tool-Calling Agents；用途 `measurement`；路线 `q005:paper_card_fts` #2；Card `paper-p049`（paper）；Evidence `ev-p049-operator-core`
- Paper `P017` · Understanding the Information Propagation Effects of Communication Topologies in LLM-based Multi-Agent Systems；用途 `measurement`；路线 `q005:passage_hybrid` #2；Passage `P017:p0003:s0001`
- Paper `P069` · Tool Preferences in Agentic LLMs are Unreliable；用途 `measurement`；路线 `q005:failure_card_fts` #1；Card `failure-tool-description-and-order-bias`（failure）；Evidence `ev-p069-description-induced-preference`, `ev-p069-identical-tool-order-bias`
- Paper `P027` · Verified Critical Step Optimization for LLM Agents；用途 `measurement`；路线 `q005:operator_card_fts` #3；Card `operator-verified-single-branch-repair`（operator）；Evidence `ev-p027-operator-core`

- 代表项：20 / 去重 Paper：96

## 查询与路线覆盖

### q001 · problem

- 原始查询：`tool agent successful final answer hidden wrong intermediate state side effects false success`
- 规范化查询：`"tool" OR "agent" OR "successful" OR "final" OR "answer" OR "hidden" OR "wrong" OR "intermediate" OR "state" OR "side" OR "effects" OR "false" OR "success"`
- 路线 `paper_card_fts`：35 条；降级 false（无）
- 路线 `failure_card_fts`：35 条；降级 false（无）
- 路线 `passage_hybrid`：30 条；降级 false（无）
- 路线 `operator_card_fts`：35 条；降级 false（无）

### q002 · failure

- 原始查询：`agent receives conflicting tool outputs stale disagreement provenance calibration`
- 规范化查询：`"agent" OR "receives" OR "conflicting" OR "tool" OR "outputs" OR "stale" OR "disagreement" OR "provenance" OR "calibration"`
- 路线 `failure_card_fts`：35 条；降级 false（无）
- 路线 `passage_hybrid`：30 条；降级 false（无）
- 路线 `operator_card_fts`：35 条；降级 false（无）
- 路线 `paper_card_fts`：35 条；降级 false（无）

### q003 · operator

- 原始查询：`adaptive verification budget choose which tool result or claim to verify`
- 规范化查询：`"adaptive" OR "verification" OR "budget" OR "choose" OR "which" OR "tool" OR "result" OR "or" OR "claim" OR "to" OR "verify"`
- 路线 `operator_card_fts`：35 条；降级 false（无）
- 路线 `paper_card_fts`：35 条；降级 false（无）
- 路线 `passage_hybrid`：30 条；降级 false（无）
- 路线 `failure_card_fts`：35 条；降级 false（无）

### q004 · prior

- 原始查询：`runtime verifier selective verification tool agents uncertainty budget`
- 规范化查询：`"runtime" OR "verifier" OR "selective" OR "verification" OR "tool" OR "agents" OR "uncertainty" OR "budget"`
- 路线 `paper_card_fts`：35 条；降级 false（无）
- 路线 `operator_card_fts`：35 条；降级 false（无）
- 路线 `failure_card_fts`：35 条；降级 false（无）
- 路线 `passage_hybrid`：30 条；降级 false（无）

### q005 · measurement

- 原始查询：`counterfactual task success process correctness hidden side effects`
- 规范化查询：`"counterfactual" OR "task" OR "success" OR "process" OR "correctness" OR "hidden" OR "side" OR "effects"`
- 路线 `paper_card_fts`：35 条；降级 false（无）
- 路线 `passage_hybrid`：30 条；降级 false（无）
- 路线 `failure_card_fts`：23 条；降级 false（无）
- 路线 `operator_card_fts`：29 条；降级 false（无）

## 覆盖诊断

- 去重 Card：198
- 去重 Evidence：213
- 去重 Passage：129
- 命中 Paper：96
- 原始观测：657
- 带机械噪声标记的观测：1
