# P073 first read — execution-supervised tool calibration

Status: `DRAFT_BEFORE_INDEPENDENT_READ`  
Reader: main Codex  
Read date: 2026-07-20 (Asia/Shanghai)

## Canonical source and bytes

- Title: Uncertainty Calibration for Tool-Using Language Agents
- Authors: Hao Liu, Zi-Yi Dou, Yixin Wang, Nanyun Peng, Yisong Yue
- Venue: Findings of EMNLP 2024
- PDF: `knowledge_base/staging/plan05_sat_a2/P073_probecal.pdf`
- PDF SHA-256: `2c56eb776ba9caf9dbe0663fdabbafc2941c10c08394494df158c5980090cc53`
- Parse check: 25 physical pages

## Changed computation

PROBECAL trains a small MLP on frozen LLM embeddings and observed binary execution rewards. One probe estimates which prompt is likely to succeed for the current task; another estimates which generated tool-execution trace is likely to succeed. Calibrated prompt probabilities control sampling, and calibrated trace probabilities weight answer aggregation. The changed computation is an execution-supervised selector over already-generated alternatives, not self-reported confidence and not a new tool planner.

## Evidence and closest lineage

- The paper evaluates static tool prompting and dynamic TroVE tool construction on MATH subsets and TabMWP, primarily with CodeLlama-7B, plus Mistral-7B, CodeLlama-13B, Llama3-8B, and a small GPT-4o-mini check.
- On static TabMWP at 10 samples, the reported combined prompt+trace method is 57.31% versus 52.70% for the sample-frequency baseline; on dynamic TabMWP at 20 samples it is 54.34% versus 46.84%.
- Probe outputs have much lower reported ECE than uncalibrated all-one or sequence-logit confidence in many settings.
- Temperature scaling adds little; weighted training is only marginally helpful; verbal confidence underperforms the baseline in the reported CodeLlama-13B setting.
- The method still improves TabMWP with 50 calibration questions, though gains grow with more execution-supervised examples.

## Measurement and fairness boundaries

- Calibration labels require ground-truth execution reward on a task distribution. This is offline supervision and cannot be presented as deployment-time uncertainty without a representative calibration set.
- Most experiments are program-aided math/table QA, so transfer to stateful Web/API agents remains unproven.
- Prompt calibration changes the sampling distribution and trace calibration changes vote weights; combined gains do not isolate which component is necessary on every dataset.
- Accuracy is measured over repeated candidate sampling; benefits depend on a multi-sample budget and should be compared at matched generation/tool cost.
- Low ECE does not guarantee better selection: the paper itself observes that some LLM-logit variants look calibrated yet degrade task performance.
- Train/test ECE gaps show distribution shift; a frozen probe can become stale when tools, prompts, or task distributions change.

## Draft knowledge objects

### Operator draft: `Execution-Supervised Prompt-and-Trace Calibration`

Fit a lightweight predictor from frozen Agent representations to observed task success, then use its probabilities to allocate prompt samples and weight competing execution traces under a fixed candidate budget.

### Failure draft: `Internal Tool Confidence Is Not Execution Success Probability`

Token likelihood, verbal confidence, or uniform votes can assign similar confidence to superficially similar correct and incorrect tool programs because the base model was not trained against the external executor's failure distribution.

## Draft Evidence locators

- pp.1–5: miscalibration scenarios, embedding probe, prompt selection, trace weighting, and design variants.
- pp.5–9: datasets, models, budgets, baselines, main results, ablations, data-size and verbal-confidence tests, limitations.
- pp.12–25: full per-dataset accuracy/ECE tables and calibration curves.

All claims remain draft until independent read and reconciliation.
