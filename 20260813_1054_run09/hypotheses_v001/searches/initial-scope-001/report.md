<!-- CRL_RESEARCH_SEARCH_META {"created_at_utc":"2026-08-13T02:55:52.024130Z","request_fingerprint_sha256":"d87570a0e67b4b18a2466ae54c03254679099d1402b0033e6f32dd200b73964e","result_json_sha256":"974f614df6e1f4488aed102946d89332745f55d2ae7daf7d86c7203ce46bd150","search_id":"initial-scope-001"} -->
# 研究检索导航

> 本报告仅展示查询路线、来源、命中定位与覆盖；所有科研判断由主研究者完成。

- 搜索标识：`initial-scope-001`
- 生成时间（协调世界时）：`2026-08-13T02:55:52.024130Z`

## q001 · problem

- 原始查询：`long-horizon tool-using LLM agents execution state drift recovery partial observability`
- 规范化查询：`"long" OR "horizon" OR "tool" OR "using" OR "LLM" OR "agents" OR "execution" OR "state" OR "drift" OR "recovery" OR "partial" OR "observability"`

### 路线 `paper_card_fts`

- 命中数：18
- 降级：false（无）

- #1 Card `paper-p073`；路径 `paper/paper-p073.md`；Evidence `ev-p073-execution-supervised-probe`, `ev-p073-internal-confidence-misalignment`
- #2 Card `paper-p021`；路径 `paper/paper-p021.md`；Evidence `ev-p021-operator-core`
- #3 Card `paper-p066`；路径 `paper/paper-p066.md`；Evidence `ev-p066-single-to-stateful-gap`, `ev-p066-multiturn-state-evaluation`
- #4 Card `paper-p019`；路径 `paper/paper-p019.md`；Evidence `ev-p019-step-level-calibration`, `ev-p019-ground-truth-calibration-oracle`
- #5 Card `paper-p046`；路径 `paper/paper-p046.md`；Evidence `ev-p046-operator-core`
- #6 Card `paper-p040`；路径 `paper/paper-p040.md`；Evidence `ev-p040-failure-core`
- #7 Card `paper-p038`；路径 `paper/paper-p038.md`；Evidence `ev-p038-operator-core`
- #8 Card `paper-p095`；路径 `paper/paper-p095.md`；Evidence `ev-p095-matched-comparison`, `ev-p095-prior-override-drift`
- #9 Card `paper-p031`；路径 `paper/paper-p031.md`；Evidence `ev-p031-evaluation-core`
- #10 Card `paper-p028`；路径 `paper/paper-p028.md`；Evidence `ev-p028-operator-core`
- #11 Card `paper-p049`；路径 `paper/paper-p049.md`；Evidence `ev-p049-operator-core`
- #12 Card `paper-p004`；路径 `paper/paper-p004.md`；Evidence `ev-p004-failure-core`
- #13 Card `paper-p074`；路径 `paper/paper-p074.md`；Evidence `ev-p074-contract-state-commit`, `ev-p074-missing-schema-true-postcondition`
- #14 Card `paper-p041`；路径 `paper/paper-p041.md`；Evidence `ev-p041-operator-core`
- #15 Card `paper-p097`；路径 `paper/paper-p097.md`；Evidence `ev-p097-feasibility-gap`, `ev-p097-behavioral-perturbation`
- #16 Card `paper-p030`；路径 `paper/paper-p030.md`；Evidence `ev-p030-failure-core`
- #17 Card `paper-p085`；路径 `paper/paper-p085.md`；Evidence `ev-p085-large-corpus-scale`, `ev-p085-retrieval-completeness-failure`, `ev-p085-non-exhaustive-label`
- #18 Card `paper-p025`；路径 `paper/paper-p025.md`；Evidence `ev-p025-failure-core`

### 路线 `failure_card_fts`

- 命中数：18
- 降级：false（无）

- #1 Card `failure-single-turn-tool-score-overstates-agent-competence`；路径 `failure/failure-single-turn-tool-score-overstates-agent-competence.md`；Evidence `ev-p066-single-to-stateful-gap`, `ev-p066-multiturn-state-evaluation`
- #2 Card `failure-llm-freshness-judgment-prior-override-and-drift`；路径 `failure/failure-llm-freshness-judgment-prior-override-and-drift.md`；Evidence `ev-p095-prior-override-drift`, `ev-p095-matched-comparison`
- #3 Card `failure-gold-context-does-not-solve-knowledge-use`；路径 `failure/failure-gold-context-does-not-solve-knowledge-use.md`；Evidence `ev-p036-failure-core`
- #4 Card `failure-confident-completion-without-state-success`；路径 `failure/failure-confident-completion-without-state-success.md`；Evidence `ev-p040-failure-core`
- #5 Card `failure-internal-tool-confidence-not-execution-success`；路径 `failure/failure-internal-tool-confidence-not-execution-success.md`；Evidence `ev-p073-execution-supervised-probe`, `ev-p073-internal-confidence-misalignment`
- #6 Card `failure-plan-cache-semantic-false-positives`；路径 `failure/failure-plan-cache-semantic-false-positives.md`；Evidence `ev-p071-plan-template-reuse`, `ev-p071-cache-false-positive-boundary`
- #7 Card `failure-constrained-plan-surface-validity`；路径 `failure/failure-constrained-plan-surface-validity.md`；Evidence `ev-p004-failure-core`, `ev-p004-macro-constraint-failure`
- #8 Card `failure-long-history-reading-overload`；路径 `failure/failure-long-history-reading-overload.md`；Evidence `ev-p010-long-history-decline`
- #9 Card `failure-multi-agent-adversarial-coordination-spans-trust-surfaces`；路径 `failure/failure-multi-agent-adversarial-coordination-spans-trust-surfaces.md`；Evidence `ev-p083-three-surface-adversarial-failure`, `ev-p083-lightweight-defense-failure`, `ev-p083-simulated-tool-boundary`
- #10 Card `failure-single-execution-denotation-false-positive`；路径 `failure/failure-single-execution-denotation-false-positive.md`；Evidence `ev-p101-metric-distortion`, `ev-p101-esm-fn-rate`
- #11 Card `failure-natural-language-ir-hurts-formal-planning`；路径 `failure/failure-natural-language-ir-hurts-formal-planning.md`；Evidence `ev-p060-formal-ir-solver`, `ev-p060-ir-result-and-nl-failure`
- #12 Card `failure-generic-or-unvalidated-tool-libraries-add-distractors`；路径 `failure/failure-generic-or-unvalidated-tool-libraries-add-distractors.md`；Evidence `ev-p078-validated-tool-creation-retrieval`, `ev-p078-multiview-tool-retrieval`, `ev-p078-generic-tool-and-baseline-boundary`, `ev-p078-toolset-construction-cost`, `ev-p078-baseline-fairness-boundary`
- #13 Card `failure-semantically-related-toolkit-expansion`；路径 `failure/failure-semantically-related-toolkit-expansion.md`；Evidence `ev-p084-expanded-toolkit-controlled-setting`, `ev-p084-related-toolkit-error-types`, `ev-p084-expanded-toolkit-table`, `ev-p084-generated-tool-single-dataset-boundary`
- #14 Card `failure-solver-feasibility-near-zero-information-proxy`；路径 `failure/failure-solver-feasibility-near-zero-information-proxy.md`；Evidence `ev-p097-feasibility-gap`, `ev-p097-behavioral-perturbation`
- #15 Card `failure-retrieved-memory-laundered-through-actions`；路径 `failure/failure-retrieved-memory-laundered-through-actions.md`；Evidence `ev-p075-retrieve-to-action-leakage`, `ev-p075-measured-memory-extraction`, `ev-p075-session-isolation-boundary`
- #16 Card `failure-large-corpus-tool-retrieval-breaks-oracle-menu`；路径 `failure/failure-large-corpus-tool-retrieval-breaks-oracle-menu.md`；Evidence `ev-p085-large-corpus-scale`, `ev-p085-retrieval-completeness-failure`, `ev-p085-non-exhaustive-label`
- #17 Card `failure-anchor-state-credit-needs-state-recurrence`；路径 `failure/failure-anchor-state-credit-needs-state-recurrence.md`；Evidence `ev-p065-anchor-state-credit`, `ev-p065-state-recurrence-boundary`
- #18 Card `failure-repeat-run-reliability-collapse`；路径 `failure/failure-repeat-run-reliability-collapse.md`；Evidence `ev-p007-repeat-reliability-collapse`

### 路线 `passage_hybrid`

- 命中数：24
- 降级：false（无）

- #1 Passage `P049:p0002:s0001`；Paper `P049`；页 2-2
- #2 Passage `P046:p0001:s0003`；Paper `P046`；页 1-1
- #3 Passage `P074:p0002:s0001`；Paper `P074`；页 2-2
- #4 Passage `P065:p0016:s0001`；Paper `P065`；页 16-16
- #5 Passage `P039:p0009:s0001`；Paper `P039`；页 9-9
- #6 Passage `P048:p0002:s0002`；Paper `P048`；页 2-2
- #7 Passage `P026:p0002:s0001`；Paper `P026`；页 2-2
- #8 Passage `P067:p0010:s0002`；Paper `P067`；页 10-10
- #9 Passage `P017:p0010:s0001`；Paper `P017`；页 10-10
- #10 Passage `P036:p0003:s0001`；Paper `P036`；页 3-3
- #11 Passage `P026:p0001:s0002`；Paper `P026`；页 1-1
- #12 Passage `P067:p0011:s0002`；Paper `P067`；页 11-11
- #13 Passage `P039:p0007:s0002`；Paper `P039`；页 7-7
- #14 Passage `P031:p0002:s0001`；Paper `P031`；页 2-2
- #15 Passage `P064:p0009:s0003`；Paper `P064`；页 9-9
- #16 Passage `P008:p0016:s0001`；Paper `P008`；页 16-16
- #17 Passage `P031:p0001:s0003`；Paper `P031`；页 1-1
- #18 Passage `P023:p0012:s0001`；Paper `P023`；页 12-12
- #19 Passage `P068:p0015:s0001`；Paper `P068`；页 15-15
- #20 Passage `P074:p0007:s0001`；Paper `P074`；页 7-7
- #21 Passage `P076:p0013:s0001`；Paper `P076`；页 13-13
- #22 Passage `P030:p0014:s0001`；Paper `P030`；页 14-14
- #23 Passage `P067:p0003:s0001`；Paper `P067`；页 3-3
- #24 Passage `P016:p0028:s0001`；Paper `P016`；页 28-28

### 路线 `operator_card_fts`

- 命中数：18
- 降级：false（无）

- #1 Card `operator-bilevel-graph-toolchain-planning`；路径 `operator/operator-bilevel-graph-toolchain-planning.md`；Evidence `ev-p048-operator-core`
- #2 Card `operator-milestone-dag-trajectory-evaluation`；路径 `operator/operator-milestone-dag-trajectory-evaluation.md`；Evidence `ev-p037-evaluation-core`, `ev-p037-minefield-violation`
- #3 Card `operator-smt-preexecution-policy-guard`；路径 `operator/operator-smt-preexecution-policy-guard.md`；Evidence `ev-p046-operator-core`
- #4 Card `operator-outcome-trained-execution-state-planner`；路径 `operator/operator-outcome-trained-execution-state-planner.md`；Evidence `ev-p021-operator-core`
- #5 Card `operator-verified-single-branch-repair`；路径 `operator/operator-verified-single-branch-repair.md`；Evidence `ev-p027-operator-core`
- #6 Card `operator-execution-supervised-prompt-trace-calibration`；路径 `operator/operator-execution-supervised-prompt-trace-calibration.md`；Evidence `ev-p073-execution-supervised-probe`, `ev-p073-internal-confidence-misalignment`
- #7 Card `operator-extract-then-deterministic-max-assembly`；路径 `operator/operator-extract-then-deterministic-max-assembly.md`；Evidence `ev-p095-matched-comparison`, `ev-p095-prior-override-drift`
- #8 Card `operator-terminal-state-reliability-evaluation`；路径 `operator/operator-terminal-state-reliability-evaluation.md`；Evidence `ev-p007-terminal-state-evaluation`
- #9 Card `operator-gold-supervised-hindsight-search-depth`；路径 `operator/operator-gold-supervised-hindsight-search-depth.md`；Evidence `ev-p080-gold-supervised-minimal-depth`, `ev-p080-fixed-depth-under-over-search`, `ev-p080-shallow-depth-boundary`
- #10 Card `operator-joint-nonnegative-residual-retrieval`；路径 `operator/operator-joint-nonnegative-residual-retrieval.md`；Evidence `ev-p088-joint-nonnegative-objective`, `ev-p088-relevant-set-size-signature`, `ev-p088-theory-deployment-scale-boundary`
- #11 Card `operator-hidden-state-tool-necessity-prefill`；路径 `operator/operator-hidden-state-tool-necessity-prefill.md`；Evidence `ev-p041-operator-core`, `ev-p041-probe-prefill-steering`
- #12 Card `operator-bounded-preexecution-reviewer`；路径 `operator/operator-bounded-preexecution-reviewer.md`；Evidence `ev-p049-operator-core`, `ev-p049-bounded-review-loop`
- #13 Card `operator-behavioral-perturbation-existence-test`；路径 `operator/operator-behavioral-perturbation-existence-test.md`；Evidence `ev-p097-behavioral-perturbation`, `ev-p097-feasibility-gap`
- #14 Card `operator-grouped-masked-history-step-credit`；路径 `operator/operator-grouped-masked-history-step-credit.md`；Evidence `ev-p025-failure-core`, `ev-p025-grouped-step-influence`
- #15 Card `operator-contract-gated-tool-state-commit`；路径 `operator/operator-contract-gated-tool-state-commit.md`；Evidence `ev-p074-contract-state-commit`, `ev-p074-missing-schema-true-postcondition`
- #16 Card `operator-trace-failure-taxonomy`；路径 `operator/operator-trace-failure-taxonomy.md`；Evidence `ev-p016-mast-taxonomy`
- #17 Card `operator-transition-decomposed-agent-training`；路径 `operator/operator-transition-decomposed-agent-training.md`；Evidence `ev-p026-transition-decomposition`, `ev-p026-uniform-terminal-return`
- #18 Card `operator-incremental-injection-benchmark-reconstruction`；路径 `operator/operator-incremental-injection-benchmark-reconstruction.md`；Evidence `ev-p094-incremental-protocol`, `ev-p094-sf-guardrails`

## q002 · failure

- 原始查询：`tool agent cascading errors stale state observations invalid assumptions recovery`
- 规范化查询：`"tool" OR "agent" OR "cascading" OR "errors" OR "stale" OR "state" OR "observations" OR "invalid" OR "assumptions" OR "recovery"`

### 路线 `failure_card_fts`

- 命中数：18
- 降级：false（无）

- #1 Card `failure-retrieved-update-lacks-decision-authority`；路径 `failure/failure-retrieved-update-lacks-decision-authority.md`；Evidence `ev-p030-failure-core`, `ev-p030-recognition-application-gap`
- #2 Card `failure-constrained-plan-surface-validity`；路径 `failure/failure-constrained-plan-surface-validity.md`；Evidence `ev-p004-failure-core`, `ev-p004-macro-constraint-failure`
- #3 Card `failure-cosine-cannot-separate-contradiction-from-duplicate`；路径 `failure/failure-cosine-cannot-separate-contradiction-from-duplicate.md`；Evidence `ev-p091-cosine-auroc`, `ev-p091-retain-fabrication`
- #4 Card `failure-multi-agent-adversarial-coordination-spans-trust-surfaces`；路径 `failure/failure-multi-agent-adversarial-coordination-spans-trust-surfaces.md`；Evidence `ev-p083-three-surface-adversarial-failure`, `ev-p083-lightweight-defense-failure`, `ev-p083-simulated-tool-boundary`
- #5 Card `failure-raw-observation-overload-hides-action-relevant-ui`；路径 `failure/failure-raw-observation-overload-hides-action-relevant-ui.md`；Evidence `ev-p079-action-conditioned-contextualization`, `ev-p079-ground-truth-action-retry`, `ev-p079-unseen-ui-boundary`
- #6 Card `failure-tool-use-metrics-collapse-distinct-errors`；路径 `failure/failure-tool-use-metrics-collapse-distinct-errors.md`；Evidence `ev-p039-failure-core`, `ev-p039-aggregate-score-masking`
- #7 Card `failure-retrieved-experience-propagates-stored-errors`；路径 `failure/failure-retrieved-experience-propagates-stored-errors.md`；Evidence `ev-p064-experience-following-error`, `ev-p064-evaluator-reliability`
- #8 Card `failure-objective-equivalence-passes-nonbinding-errors`；路径 `failure/failure-objective-equivalence-passes-nonbinding-errors.md`；Evidence `ev-p098-nonbinding-blindness`, `ev-p098-diff-leak-550`, `ev-p098-open-problem`
- #9 Card `failure-generic-or-unvalidated-tool-libraries-add-distractors`；路径 `failure/failure-generic-or-unvalidated-tool-libraries-add-distractors.md`；Evidence `ev-p078-validated-tool-creation-retrieval`, `ev-p078-multiview-tool-retrieval`, `ev-p078-generic-tool-and-baseline-boundary`, `ev-p078-toolset-construction-cost`, `ev-p078-baseline-fairness-boundary`
- #10 Card `failure-llm-judge-misses-executable-spec-errors`；路径 `failure/failure-llm-judge-misses-executable-spec-errors.md`；Evidence `ev-p099-judge-miss`, `ev-p099-soundness-necessity`
- #11 Card `failure-solver-feasibility-near-zero-information-proxy`；路径 `failure/failure-solver-feasibility-near-zero-information-proxy.md`；Evidence `ev-p097-feasibility-gap`, `ev-p097-behavioral-perturbation`
- #12 Card `failure-debate-cost-nondominance`；路径 `failure/failure-debate-cost-nondominance.md`；Evidence `ev-p015-debate-cost-nondominance`
- #13 Card `failure-gold-context-does-not-solve-knowledge-use`；路径 `failure/failure-gold-context-does-not-solve-knowledge-use.md`；Evidence `ev-p036-failure-core`
- #14 Card `failure-anchor-state-credit-needs-state-recurrence`；路径 `failure/failure-anchor-state-credit-needs-state-recurrence.md`；Evidence `ev-p065-anchor-state-credit`, `ev-p065-state-recurrence-boundary`
- #15 Card `failure-single-turn-tool-score-overstates-agent-competence`；路径 `failure/failure-single-turn-tool-score-overstates-agent-competence.md`；Evidence `ev-p066-single-to-stateful-gap`, `ev-p066-multiturn-state-evaluation`
- #16 Card `failure-sparse-topology-suppresses-correct-insight`；路径 `failure/failure-sparse-topology-suppresses-correct-insight.md`；Evidence `ev-p017-failure-core`
- #17 Card `failure-confident-completion-without-state-success`；路径 `failure/failure-confident-completion-without-state-success.md`；Evidence `ev-p040-failure-core`
- #18 Card `failure-incomplete-tool-contracts-false-verified-state`；路径 `failure/failure-incomplete-tool-contracts-false-verified-state.md`；Evidence `ev-p074-contract-state-commit`, `ev-p074-missing-schema-true-postcondition`

### 路线 `passage_hybrid`

- 命中数：24
- 降级：false（无）

- #1 Passage `P049:p0002:s0001`；Paper `P049`；页 2-2
- #2 Passage `P030:p0001:s0001`；Paper `P030`；页 1-1
- #3 Passage `P030:p0010:s0001`；Paper `P030`；页 10-10
- #4 Passage `P072:p0025:s0001`；Paper `P072`；页 25-25
- #5 Passage `P004:p0007:s0003`；Paper `P004`；页 7-7
- #6 Passage `P004:p0008:s0002`；Paper `P004`；页 8-8
- #7 Passage `P030:p0009:s0001`；Paper `P030`；页 9-9
- #8 Passage `P074:p0016:s0001`；Paper `P074`；页 16-16
- #9 Passage `P030:p0002:s0001`；Paper `P030`；页 2-2
- #10 Passage `P091:p0001:s0001`；Paper `P091`；页 1-1
- #11 Passage `P030:p0034:s0001`；Paper `P030`；页 34-34
- #12 Passage `P074:p0013:s0001`；Paper `P074`；页 13-13
- #13 Passage `P039:p0007:s0002`；Paper `P039`；页 7-7
- #14 Passage `P049:p0001:s0001`；Paper `P049`；页 1-1
- #15 Passage `P074:p0001:s0003`；Paper `P074`；页 1-1
- #16 Passage `P039:p0009:s0001`；Paper `P039`；页 9-9
- #17 Passage `P072:p0003:s0001`；Paper `P072`；页 3-3
- #18 Passage `P030:p0037:s0001`；Paper `P030`；页 37-37
- #19 Passage `P072:p0012:s0001`；Paper `P072`；页 12-12
- #20 Passage `P030:p0009:s0002`；Paper `P030`；页 9-9
- #21 Passage `P084:p0005:s0001`；Paper `P084`；页 5-5
- #22 Passage `P087:p0009:s0004`；Paper `P087`；页 9-9
- #23 Passage `P097:p0009:s0002`；Paper `P097`；页 9-9
- #24 Passage `P040:p0011:s0002`；Paper `P040`；页 11-11

### 路线 `operator_card_fts`

- 命中数：18
- 降级：false（无）

- #1 Card `operator-contract-gated-tool-state-commit`；路径 `operator/operator-contract-gated-tool-state-commit.md`；Evidence `ev-p074-contract-state-commit`, `ev-p074-missing-schema-true-postcondition`
- #2 Card `operator-write-side-state-adjudication`；路径 `operator/operator-write-side-state-adjudication.md`；Evidence `ev-p030-failure-core`, `ev-p030-write-side-adjudication`, `ev-p030-authorized-readout`
- #3 Card `operator-tool-grounded-critique`；路径 `operator/operator-tool-grounded-critique.md`；Evidence `ev-p032-operator-core`
- #4 Card `operator-outcome-trained-execution-state-planner`；路径 `operator/operator-outcome-trained-execution-state-planner.md`；Evidence `ev-p021-operator-core`
- #5 Card `operator-bilevel-graph-toolchain-planning`；路径 `operator/operator-bilevel-graph-toolchain-planning.md`；Evidence `ev-p048-operator-core`
- #6 Card `operator-smt-preexecution-policy-guard`；路径 `operator/operator-smt-preexecution-policy-guard.md`；Evidence `ev-p046-operator-core`
- #7 Card `operator-deterministic-sro-supersession-ledger`；路径 `operator/operator-deterministic-sro-supersession-ledger.md`；Evidence `ev-p091-supersession-rule`, `ev-p091-retain-fabrication`
- #8 Card `operator-milestone-dag-trajectory-evaluation`；路径 `operator/operator-milestone-dag-trajectory-evaluation.md`；Evidence `ev-p037-evaluation-core`, `ev-p037-minefield-violation`
- #9 Card `operator-joint-nonnegative-residual-retrieval`；路径 `operator/operator-joint-nonnegative-residual-retrieval.md`；Evidence `ev-p088-joint-nonnegative-objective`, `ev-p088-relevant-set-size-signature`, `ev-p088-theory-deployment-scale-boundary`
- #10 Card `operator-terminal-state-reliability-evaluation`；路径 `operator/operator-terminal-state-reliability-evaluation.md`；Evidence `ev-p007-terminal-state-evaluation`
- #11 Card `operator-validated-specialized-tool-creation-retrieval`；路径 `operator/operator-validated-specialized-tool-creation-retrieval.md`；Evidence `ev-p078-validated-tool-creation-retrieval`, `ev-p078-multiview-tool-retrieval`, `ev-p078-generic-tool-and-baseline-boundary`, `ev-p078-toolset-construction-cost`, `ev-p078-baseline-fairness-boundary`
- #12 Card `operator-bounded-preexecution-reviewer`；路径 `operator/operator-bounded-preexecution-reviewer.md`；Evidence `ev-p049-operator-core`, `ev-p049-bounded-review-loop`
- #13 Card `operator-hidden-state-tool-necessity-prefill`；路径 `operator/operator-hidden-state-tool-necessity-prefill.md`；Evidence `ev-p041-operator-core`, `ev-p041-probe-prefill-steering`
- #14 Card `operator-behavioral-perturbation-existence-test`；路径 `operator/operator-behavioral-perturbation-existence-test.md`；Evidence `ev-p097-behavioral-perturbation`, `ev-p097-feasibility-gap`
- #15 Card `operator-state-conditioned-agent-activation`；路径 `operator/operator-state-conditioned-agent-activation.md`；Evidence `ev-p059-state-conditioned-orchestrator`, `ev-p059-compact-cyclic-topology`
- #16 Card `operator-anchor-state-relative-credit`；路径 `operator/operator-anchor-state-relative-credit.md`；Evidence `ev-p065-anchor-state-credit`, `ev-p065-state-recurrence-boundary`, `ev-p026-uniform-terminal-return`
- #17 Card `operator-execution-supervised-prompt-trace-calibration`；路径 `operator/operator-execution-supervised-prompt-trace-calibration.md`；Evidence `ev-p073-execution-supervised-probe`, `ev-p073-internal-confidence-misalignment`
- #18 Card `operator-thought-tree-search`；路径 `operator/operator-thought-tree-search.md`；Evidence `ev-p002-branch-evaluate-search`

### 路线 `paper_card_fts`

- 命中数：18
- 降级：false（无）

- #1 Card `paper-p030`；路径 `paper/paper-p030.md`；Evidence `ev-p030-failure-core`
- #2 Card `paper-p047`；路径 `paper/paper-p047.md`；Evidence `ev-p047-evaluation-core`
- #3 Card `paper-p035`；路径 `paper/paper-p035.md`；Evidence `ev-p035-evaluation-core`
- #4 Card `paper-p037`；路径 `paper/paper-p037.md`；Evidence `ev-p037-evaluation-core`
- #5 Card `paper-p091`；路径 `paper/paper-p091.md`；Evidence `ev-p091-cosine-auroc`, `ev-p091-supersession-rule`, `ev-p091-retain-fabrication`
- #6 Card `paper-p097`；路径 `paper/paper-p097.md`；Evidence `ev-p097-feasibility-gap`, `ev-p097-behavioral-perturbation`
- #7 Card `paper-llmcompiler`；路径 `paper/paper-llmcompiler.md`；Evidence `ev-p006-dependency-dag-dispatch`, `ev-p006-token-cost-accounting`, `ev-p006-shared-prompt-comparison-boundary`
- #8 Card `paper-p048`；路径 `paper/paper-p048.md`；Evidence `ev-p048-operator-core`
- #9 Card `paper-p085`；路径 `paper/paper-p085.md`；Evidence `ev-p085-large-corpus-scale`, `ev-p085-retrieval-completeness-failure`, `ev-p085-non-exhaustive-label`
- #10 Card `paper-p088`；路径 `paper/paper-p088.md`；Evidence `ev-p088-joint-nonnegative-objective`, `ev-p088-relevant-set-size-signature`, `ev-p088-theory-deployment-scale-boundary`
- #11 Card `paper-p079`；路径 `paper/paper-p079.md`；Evidence `ev-p079-action-conditioned-contextualization`, `ev-p079-ground-truth-action-retry`, `ev-p079-unseen-ui-boundary`
- #12 Card `paper-p005`；路径 `paper/paper-p005.md`；Evidence `ev-p005-operator-core`
- #13 Card `paper-p074`；路径 `paper/paper-p074.md`；Evidence `ev-p074-contract-state-commit`, `ev-p074-missing-schema-true-postcondition`
- #14 Card `paper-p066`；路径 `paper/paper-p066.md`；Evidence `ev-p066-single-to-stateful-gap`, `ev-p066-multiturn-state-evaluation`
- #15 Card `paper-tau-bench`；路径 `paper/paper-tau-bench.md`；Evidence `ev-p007-terminal-state-evaluation`, `ev-p007-repeat-reliability-collapse`
- #16 Card `paper-p021`；路径 `paper/paper-p021.md`；Evidence `ev-p021-operator-core`
- #17 Card `paper-p065`；路径 `paper/paper-p065.md`；Evidence `ev-p065-anchor-state-credit`, `ev-p065-state-recurrence-boundary`
- #18 Card `paper-p059`；路径 `paper/paper-p059.md`；Evidence `ev-p059-state-conditioned-orchestrator`, `ev-p059-compact-cyclic-topology`

## q003 · operator

- 原始查询：`post-action verification counterfactual checking selective test-time computation tool calls`
- 规范化查询：`"post" OR "action" OR "verification" OR "counterfactual" OR "checking" OR "selective" OR "test" OR "time" OR "computation" OR "tool" OR "calls"`

### 路线 `operator_card_fts`

- 命中数：18
- 降级：false（无）

- #1 Card `operator-four-bucket-executable-spec-testing`；路径 `operator/operator-four-bucket-executable-spec-testing.md`；Evidence `ev-p099-two-stage-check`, `ev-p099-soundness-necessity`, `ev-p099-judge-miss`
- #2 Card `operator-fixed-budget-independent-path-aggregation`；路径 `operator/operator-fixed-budget-independent-path-aggregation.md`；Evidence `ev-p081-independent-path-majority-aggregation`, `ev-p081-forty-sample-baseline`, `ev-p081-fixed-answer-space-boundary`
- #3 Card `operator-verified-single-branch-repair`；路径 `operator/operator-verified-single-branch-repair.md`；Evidence `ev-p027-operator-core`
- #4 Card `operator-contract-gated-tool-state-commit`；路径 `operator/operator-contract-gated-tool-state-commit.md`；Evidence `ev-p074-contract-state-commit`, `ev-p074-missing-schema-true-postcondition`
- #5 Card `operator-behavioral-perturbation-existence-test`；路径 `operator/operator-behavioral-perturbation-existence-test.md`；Evidence `ev-p097-behavioral-perturbation`, `ev-p097-feasibility-gap`
- #6 Card `operator-bounded-preexecution-reviewer`；路径 `operator/operator-bounded-preexecution-reviewer.md`；Evidence `ev-p049-operator-core`, `ev-p049-bounded-review-loop`
- #7 Card `operator-adaptive-plan-template-reuse`；路径 `operator/operator-adaptive-plan-template-reuse.md`；Evidence `ev-p071-plan-template-reuse`, `ev-p071-cache-false-positive-boundary`
- #8 Card `operator-validated-specialized-tool-creation-retrieval`；路径 `operator/operator-validated-specialized-tool-creation-retrieval.md`；Evidence `ev-p078-validated-tool-creation-retrieval`, `ev-p078-multiview-tool-retrieval`, `ev-p078-generic-tool-and-baseline-boundary`, `ev-p078-toolset-construction-cost`, `ev-p078-baseline-fairness-boundary`
- #9 Card `operator-active-counterexample-verifier`；路径 `operator/operator-active-counterexample-verifier.md`；Evidence `ev-p050-operator-core`
- #10 Card `operator-dynamic-linked-memory-evolution`；路径 `operator/operator-dynamic-linked-memory-evolution.md`；Evidence `ev-p063-dynamic-link-generation`, `ev-p063-neighbor-rewrite-action`, `ev-p063-retrieval-k-varies`
- #11 Card `operator-action-preserving-observation-contextualization`；路径 `operator/operator-action-preserving-observation-contextualization.md`；Evidence `ev-p079-action-conditioned-contextualization`, `ev-p079-ground-truth-action-retry`, `ev-p079-unseen-ui-boundary`
- #12 Card `operator-subtask-compute-allocation`；路径 `operator/operator-subtask-compute-allocation.md`；Evidence `ev-p020-compute-allocation-search`
- #13 Card `operator-thought-tree-search`；路径 `operator/operator-thought-tree-search.md`；Evidence `ev-p002-branch-evaluate-search`
- #14 Card `operator-hidden-state-tool-necessity-prefill`；路径 `operator/operator-hidden-state-tool-necessity-prefill.md`；Evidence `ev-p041-operator-core`, `ev-p041-probe-prefill-steering`
- #15 Card `operator-future-token-loss-filtered-tool-learning`；路径 `operator/operator-future-token-loss-filtered-tool-learning.md`；Evidence `ev-p082-future-token-loss-filtered-calls`, `ev-p082-top-k-single-call-boundary`, `ev-p082-chaining-cost-sparsity-boundary`
- #16 Card `operator-reason-action-interleaving`；路径 `operator/operator-reason-action-interleaving.md`；Evidence `ev-p001-react-interleaved`
- #17 Card `operator-gold-supervised-hindsight-search-depth`；路径 `operator/operator-gold-supervised-hindsight-search-depth.md`；Evidence `ev-p080-gold-supervised-minimal-depth`, `ev-p080-fixed-depth-under-over-search`, `ev-p080-shallow-depth-boundary`
- #18 Card `operator-neighbor-distilled-test-suites`；路径 `operator/operator-neighbor-distilled-test-suites.md`；Evidence `ev-p101-neighbor-distillation`, `ev-p101-esm-fn-rate`

### 路线 `paper_card_fts`

- 命中数：18
- 降级：false（无）

- #1 Card `paper-p094`；路径 `paper/paper-p094.md`；Evidence `ev-p094-sf-length-collapse`, `ev-p094-sf-guardrails`, `ev-p094-incremental-protocol`
- #2 Card `paper-p081`；路径 `paper/paper-p081.md`；Evidence `ev-p081-independent-path-majority-aggregation`, `ev-p081-forty-sample-baseline`, `ev-p081-fixed-answer-space-boundary`
- #3 Card `paper-p074`；路径 `paper/paper-p074.md`；Evidence `ev-p074-contract-state-commit`, `ev-p074-missing-schema-true-postcondition`
- #4 Card `paper-p078`；路径 `paper/paper-p078.md`；Evidence `ev-p078-validated-tool-creation-retrieval`, `ev-p078-multiview-tool-retrieval`, `ev-p078-generic-tool-and-baseline-boundary`, `ev-p078-toolset-construction-cost`, `ev-p078-baseline-fairness-boundary`
- #5 Card `paper-p027`；路径 `paper/paper-p027.md`；Evidence `ev-p027-operator-core`
- #6 Card `paper-tree-of-thoughts`；路径 `paper/paper-tree-of-thoughts.md`；Evidence `ev-p002-branch-evaluate-search`, `ev-p002-search-resource-cost`
- #7 Card `paper-p046`；路径 `paper/paper-p046.md`；Evidence `ev-p046-operator-core`
- #8 Card `paper-p071`；路径 `paper/paper-p071.md`；Evidence `ev-p071-plan-template-reuse`, `ev-p071-cache-false-positive-boundary`
- #9 Card `paper-agenttts`；路径 `paper/paper-agenttts.md`；Evidence `ev-p020-compute-allocation-search`, `ev-p020-diminishing-compute-return`
- #10 Card `paper-p080`；路径 `paper/paper-p080.md`；Evidence `ev-p080-gold-supervised-minimal-depth`, `ev-p080-fixed-depth-under-over-search`, `ev-p080-shallow-depth-boundary`
- #11 Card `paper-p019`；路径 `paper/paper-p019.md`；Evidence `ev-p019-step-level-calibration`, `ev-p019-ground-truth-calibration-oracle`
- #12 Card `paper-p025`；路径 `paper/paper-p025.md`；Evidence `ev-p025-failure-core`
- #13 Card `paper-p050`；路径 `paper/paper-p050.md`；Evidence `ev-p050-operator-core`
- #14 Card `paper-p005`；路径 `paper/paper-p005.md`；Evidence `ev-p005-operator-core`
- #15 Card `paper-p099`；路径 `paper/paper-p099.md`；Evidence `ev-p099-judge-miss`, `ev-p099-two-stage-check`, `ev-p099-soundness-necessity`
- #16 Card `paper-p038`；路径 `paper/paper-p038.md`；Evidence `ev-p038-operator-core`
- #17 Card `paper-p063`；路径 `paper/paper-p063.md`；Evidence `ev-p063-dynamic-link-generation`, `ev-p063-retrieval-k-varies`, `ev-p063-neighbor-rewrite-action`
- #18 Card `paper-p101`；路径 `paper/paper-p101.md`；Evidence `ev-p101-metric-distortion`, `ev-p101-neighbor-distillation`, `ev-p101-esm-fn-rate`

### 路线 `passage_hybrid`

- 命中数：24
- 降级：false（无）

- #1 Passage `P046:p0003:s0001`；Paper `P046`；页 3-3
- #2 Passage `P050:p0002:s0001`；Paper `P050`；页 2-2
- #3 Passage `P074:p0009:s0001`；Paper `P074`；页 9-9
- #4 Passage `P095:p0011:s0001`；Paper `P095`；页 11-11
- #5 Passage `P074:p0002:s0001`；Paper `P074`；页 2-2
- #6 Passage `P046:p0005:s0002`；Paper `P046`；页 5-5
- #7 Passage `P050:p0009:s0002`；Paper `P050`；页 9-9
- #8 Passage `P099:p0053:s0001`；Paper `P099`；页 53-53
- #9 Passage `P099:p0056:s0001`；Paper `P099`；页 56-56
- #10 Passage `P035:p0028:s0001`；Paper `P035`；页 28-28
- #11 Passage `P046:p0002:s0001`；Paper `P046`；页 2-2
- #12 Passage `P016:p0033:s0001`；Paper `P016`；页 33-33
- #13 Passage `P016:p0032:s0001`；Paper `P016`；页 32-32
- #14 Passage `P046:p0005:s0003`；Paper `P046`；页 5-5
- #15 Passage `P049:p0001:s0001`；Paper `P049`；页 1-1
- #16 Passage `P016:p0025:s0001`；Paper `P016`；页 25-25
- #17 Passage `P099:p0008:s0001`；Paper `P099`；页 8-8
- #18 Passage `P041:p0014:s0001`；Paper `P041`；页 14-14
- #19 Passage `P099:p0002:s0001`；Paper `P099`；页 2-2
- #20 Passage `P016:p0008:s0001`；Paper `P016`；页 8-8
- #21 Passage `P021:p0004:s0003`；Paper `P021`；页 4-4
- #22 Passage `P072:p0005:s0001`；Paper `P072`；页 5-5
- #23 Passage `P046:p0001:s0002`；Paper `P046`；页 1-1
- #24 Passage `P068:p0007:s0001`；Paper `P068`；页 7-7

### 路线 `failure_card_fts`

- 命中数：18
- 降级：false（无）

- #1 Card `failure-unified-memory-policy-retains-terminal-credit-smearing`；路径 `failure/failure-unified-memory-policy-retains-terminal-credit-smearing.md`；Evidence `ev-p062-unified-memory-action-policy`, `ev-p062-broadcast-advantage`
- #2 Card `failure-search-resource-cost`；路径 `failure/failure-search-resource-cost.md`；Evidence `ev-p002-search-resource-cost`
- #3 Card `failure-diminishing-compute-return`；路径 `failure/failure-diminishing-compute-return.md`；Evidence `ev-p020-diminishing-compute-return`
- #4 Card `failure-iterative-refinement-corrupts-correct-output`；路径 `failure/failure-iterative-refinement-corrupts-correct-output.md`；Evidence `ev-p033-operator-core`, `ev-p034-failure-core`
- #5 Card `failure-selective-forgetting-collapses-with-context-length`；路径 `failure/failure-selective-forgetting-collapses-with-context-length.md`；Evidence `ev-p094-sf-length-collapse`, `ev-p094-sf-guardrails`
- #6 Card `failure-generator-aligned-verification-passes-shared-misreads`；路径 `failure/failure-generator-aligned-verification-passes-shared-misreads.md`；Evidence `ev-p096-shared-misinterpretation`, `ev-p096-simplification-inversion`
- #7 Card `failure-internal-tool-confidence-not-execution-success`；路径 `failure/failure-internal-tool-confidence-not-execution-success.md`；Evidence `ev-p073-execution-supervised-probe`, `ev-p073-internal-confidence-misalignment`
- #8 Card `failure-generic-or-unvalidated-tool-libraries-add-distractors`；路径 `failure/failure-generic-or-unvalidated-tool-libraries-add-distractors.md`；Evidence `ev-p078-validated-tool-creation-retrieval`, `ev-p078-multiview-tool-retrieval`, `ev-p078-generic-tool-and-baseline-boundary`, `ev-p078-toolset-construction-cost`, `ev-p078-baseline-fairness-boundary`
- #9 Card `failure-confident-completion-without-state-success`；路径 `failure/failure-confident-completion-without-state-success.md`；Evidence `ev-p040-failure-core`
- #10 Card `failure-reused-selection-feedback-in-agent-search`；路径 `failure/failure-reused-selection-feedback-in-agent-search.md`；Evidence `ev-p057-search-evaluation-budget`, `ev-p058-validation-selection-loop`
- #11 Card `failure-gold-context-does-not-solve-knowledge-use`；路径 `failure/failure-gold-context-does-not-solve-knowledge-use.md`；Evidence `ev-p036-failure-core`
- #12 Card `failure-sparse-topology-suppresses-correct-insight`；路径 `failure/failure-sparse-topology-suppresses-correct-insight.md`；Evidence `ev-p017-failure-core`
- #13 Card `failure-uniform-terminal-return-erases-step-credit`；路径 `failure/failure-uniform-terminal-return-erases-step-credit.md`；Evidence `ev-p026-transition-decomposition`, `ev-p026-uniform-terminal-return`
- #14 Card `failure-likelihood-utility-does-not-guarantee-agent-utility`；路径 `failure/failure-likelihood-utility-does-not-guarantee-agent-utility.md`；Evidence `ev-p082-future-token-loss-filtered-calls`, `ev-p082-top-k-single-call-boundary`, `ev-p082-chaining-cost-sparsity-boundary`
- #15 Card `failure-lazy-agent-effective-single-agent-collapse`；路径 `failure/failure-lazy-agent-effective-single-agent-collapse.md`；Evidence `ev-p025-failure-core`
- #16 Card `failure-raw-observation-overload-hides-action-relevant-ui`；路径 `failure/failure-raw-observation-overload-hides-action-relevant-ui.md`；Evidence `ev-p079-action-conditioned-contextualization`, `ev-p079-ground-truth-action-retry`, `ev-p079-unseen-ui-boundary`
- #17 Card `failure-semantically-related-toolkit-expansion`；路径 `failure/failure-semantically-related-toolkit-expansion.md`；Evidence `ev-p084-expanded-toolkit-controlled-setting`, `ev-p084-related-toolkit-error-types`, `ev-p084-expanded-toolkit-table`, `ev-p084-generated-tool-single-dataset-boundary`
- #18 Card `failure-constrained-plan-surface-validity`；路径 `failure/failure-constrained-plan-surface-validity.md`；Evidence `ev-p004-failure-core`, `ev-p004-macro-constraint-failure`

## q004 · prior

- 原始查询：`LLM tool agents verification execution feedback state tracking planning`
- 规范化查询：`"LLM" OR "tool" OR "agents" OR "verification" OR "execution" OR "feedback" OR "state" OR "tracking" OR "planning"`

### 路线 `paper_card_fts`

- 命中数：18
- 降级：false（无）

- #1 Card `paper-p046`；路径 `paper/paper-p046.md`；Evidence `ev-p046-operator-core`
- #2 Card `paper-p049`；路径 `paper/paper-p049.md`；Evidence `ev-p049-operator-core`
- #3 Card `paper-p074`；路径 `paper/paper-p074.md`；Evidence `ev-p074-contract-state-commit`, `ev-p074-missing-schema-true-postcondition`
- #4 Card `paper-p021`；路径 `paper/paper-p021.md`；Evidence `ev-p021-operator-core`
- #5 Card `paper-p097`；路径 `paper/paper-p097.md`；Evidence `ev-p097-feasibility-gap`, `ev-p097-behavioral-perturbation`
- #6 Card `paper-p040`；路径 `paper/paper-p040.md`；Evidence `ev-p040-failure-core`
- #7 Card `paper-p051`；路径 `paper/paper-p051.md`；Evidence `ev-p051-formalization-pipeline`, `ev-p051-solver-guarantee-boundary`, `ev-p051-omitted-constraint-failure`, `ev-p051-cost-boundary`
- #8 Card `paper-p073`；路径 `paper/paper-p073.md`；Evidence `ev-p073-execution-supervised-probe`, `ev-p073-internal-confidence-misalignment`
- #9 Card `paper-p004`；路径 `paper/paper-p004.md`；Evidence `ev-p004-failure-core`
- #10 Card `paper-p044`；路径 `paper/paper-p044.md`；Evidence `ev-p044-evaluation-core`
- #11 Card `paper-p041`；路径 `paper/paper-p041.md`；Evidence `ev-p041-operator-core`
- #12 Card `paper-p034`；路径 `paper/paper-p034.md`；Evidence `ev-p034-failure-core`
- #13 Card `paper-p030`；路径 `paper/paper-p030.md`；Evidence `ev-p030-failure-core`
- #14 Card `paper-p003`；路径 `paper/paper-p003.md`；Evidence `ev-p003-search-control-loop`, `ev-p003-generic-reflection-local-minimum`
- #15 Card `paper-agent-security-bench`；路径 `paper/paper-agent-security-bench.md`；Evidence `ev-p008-stagewise-attack-surface`, `ev-p008-memory-defense-high-fnr`
- #16 Card `paper-p095`；路径 `paper/paper-p095.md`；Evidence `ev-p095-matched-comparison`, `ev-p095-prior-override-drift`
- #17 Card `paper-p025`；路径 `paper/paper-p025.md`；Evidence `ev-p025-failure-core`
- #18 Card `paper-p026`；路径 `paper/paper-p026.md`；Evidence `ev-p026-transition-decomposition`, `ev-p026-uniform-terminal-return`

### 路线 `operator_card_fts`

- 命中数：18
- 降级：false（无）

- #1 Card `operator-outcome-trained-execution-state-planner`；路径 `operator/operator-outcome-trained-execution-state-planner.md`；Evidence `ev-p021-operator-core`
- #2 Card `operator-smt-preexecution-policy-guard`；路径 `operator/operator-smt-preexecution-policy-guard.md`；Evidence `ev-p046-operator-core`
- #3 Card `operator-terminal-state-reliability-evaluation`；路径 `operator/operator-terminal-state-reliability-evaluation.md`；Evidence `ev-p007-terminal-state-evaluation`
- #4 Card `operator-bounded-preexecution-reviewer`；路径 `operator/operator-bounded-preexecution-reviewer.md`；Evidence `ev-p049-operator-core`, `ev-p049-bounded-review-loop`
- #5 Card `operator-bilevel-graph-toolchain-planning`；路径 `operator/operator-bilevel-graph-toolchain-planning.md`；Evidence `ev-p048-operator-core`
- #6 Card `operator-feedback-backpropagated-tree-search`；路径 `operator/operator-feedback-backpropagated-tree-search.md`；Evidence `ev-p003-search-control-loop`
- #7 Card `operator-trace-failure-taxonomy`；路径 `operator/operator-trace-failure-taxonomy.md`；Evidence `ev-p016-mast-taxonomy`
- #8 Card `operator-execution-supervised-prompt-trace-calibration`；路径 `operator/operator-execution-supervised-prompt-trace-calibration.md`；Evidence `ev-p073-execution-supervised-probe`, `ev-p073-internal-confidence-misalignment`
- #9 Card `operator-syntax-aligned-formal-ir-planning`；路径 `operator/operator-syntax-aligned-formal-ir-planning.md`；Evidence `ev-p060-formal-ir-solver`, `ev-p060-ir-result-and-nl-failure`
- #10 Card `operator-mcts-executable-workflow-refinement`；路径 `operator/operator-mcts-executable-workflow-refinement.md`；Evidence `ev-p058-mcts-workflow-search`, `ev-p058-validation-selection-loop`
- #11 Card `operator-tool-grounded-critique`；路径 `operator/operator-tool-grounded-critique.md`；Evidence `ev-p032-operator-core`
- #12 Card `operator-hidden-state-tool-necessity-prefill`；路径 `operator/operator-hidden-state-tool-necessity-prefill.md`；Evidence `ev-p041-operator-core`, `ev-p041-probe-prefill-steering`
- #13 Card `operator-solver-simplification-query-verification`；路径 `operator/operator-solver-simplification-query-verification.md`；Evidence `ev-p096-simplification-inversion`, `ev-p096-shared-misinterpretation`
- #14 Card `operator-behavioral-perturbation-existence-test`；路径 `operator/operator-behavioral-perturbation-existence-test.md`；Evidence `ev-p097-behavioral-perturbation`, `ev-p097-feasibility-gap`
- #15 Card `operator-contract-gated-tool-state-commit`；路径 `operator/operator-contract-gated-tool-state-commit.md`；Evidence `ev-p074-contract-state-commit`, `ev-p074-missing-schema-true-postcondition`
- #16 Card `operator-transition-decomposed-agent-training`；路径 `operator/operator-transition-decomposed-agent-training.md`；Evidence `ev-p026-transition-decomposition`, `ev-p026-uniform-terminal-return`
- #17 Card `operator-decomposed-solver-backed-formal-planning`；路径 `operator/operator-decomposed-solver-backed-formal-planning.md`；Evidence `ev-p051-formalization-pipeline`, `ev-p051-solver-guarantee-boundary`, `ev-p051-cost-boundary`, `ev-p052-decomposed-formalization`, `ev-p052-result-self-assessment`, `ev-p052-self-assessment-loop-limit`, `ev-p052-fixed-cross-task-examples`, `ev-p052-direct-code-smt-baselines`
- #18 Card `operator-active-counterexample-verifier`；路径 `operator/operator-active-counterexample-verifier.md`；Evidence `ev-p050-operator-core`

### 路线 `failure_card_fts`

- 命中数：18
- 降级：false（无）

- #1 Card `failure-constrained-plan-surface-validity`；路径 `failure/failure-constrained-plan-surface-validity.md`；Evidence `ev-p004-failure-core`, `ev-p004-macro-constraint-failure`
- #2 Card `failure-confident-completion-without-state-success`；路径 `failure/failure-confident-completion-without-state-success.md`；Evidence `ev-p040-failure-core`
- #3 Card `failure-gold-context-does-not-solve-knowledge-use`；路径 `failure/failure-gold-context-does-not-solve-knowledge-use.md`；Evidence `ev-p036-failure-core`
- #4 Card `failure-solver-feasibility-near-zero-information-proxy`；路径 `failure/failure-solver-feasibility-near-zero-information-proxy.md`；Evidence `ev-p097-feasibility-gap`, `ev-p097-behavioral-perturbation`
- #5 Card `failure-generator-aligned-verification-passes-shared-misreads`；路径 `failure/failure-generator-aligned-verification-passes-shared-misreads.md`；Evidence `ev-p096-shared-misinterpretation`, `ev-p096-simplification-inversion`
- #6 Card `failure-llm-freshness-judgment-prior-override-and-drift`；路径 `failure/failure-llm-freshness-judgment-prior-override-and-drift.md`；Evidence `ev-p095-prior-override-drift`, `ev-p095-matched-comparison`
- #7 Card `failure-internal-tool-confidence-not-execution-success`；路径 `failure/failure-internal-tool-confidence-not-execution-success.md`；Evidence `ev-p073-execution-supervised-probe`, `ev-p073-internal-confidence-misalignment`
- #8 Card `failure-iterative-refinement-corrupts-correct-output`；路径 `failure/failure-iterative-refinement-corrupts-correct-output.md`；Evidence `ev-p033-operator-core`, `ev-p034-failure-core`
- #9 Card `failure-incomplete-tool-contracts-false-verified-state`；路径 `failure/failure-incomplete-tool-contracts-false-verified-state.md`；Evidence `ev-p074-contract-state-commit`, `ev-p074-missing-schema-true-postcondition`
- #10 Card `failure-generic-reflection-local-minima`；路径 `failure/failure-generic-reflection-local-minima.md`；Evidence `ev-p003-generic-reflection-local-minimum`
- #11 Card `failure-reused-selection-feedback-in-agent-search`；路径 `failure/failure-reused-selection-feedback-in-agent-search.md`；Evidence `ev-p057-search-evaluation-budget`, `ev-p058-validation-selection-loop`
- #12 Card `failure-constraint-shift-breaks-formalization`；路径 `failure/failure-constraint-shift-breaks-formalization.md`；Evidence `ev-p054-natural-language-implicit-predicate-failure`, `ev-p055-constraint-formalism-taxonomy`, `ev-p055-representative-subset-boundary`, `ev-p055-three-revision-budget`, `ev-p055-constraint-performance-drop`, `ev-p055-plan-correctness-false-positive-boundary`
- #13 Card `failure-multi-agent-adversarial-coordination-spans-trust-surfaces`；路径 `failure/failure-multi-agent-adversarial-coordination-spans-trust-surfaces.md`；Evidence `ev-p083-three-surface-adversarial-failure`, `ev-p083-lightweight-defense-failure`, `ev-p083-simulated-tool-boundary`
- #14 Card `failure-natural-language-ir-hurts-formal-planning`；路径 `failure/failure-natural-language-ir-hurts-formal-planning.md`；Evidence `ev-p060-formal-ir-solver`, `ev-p060-ir-result-and-nl-failure`
- #15 Card `failure-light-tool-runtime-bottleneck-overreach`；路径 `failure/failure-light-tool-runtime-bottleneck-overreach.md`；Evidence `ev-p070-six-stage-attribution`, `ev-p070-light-tool-runtime-boundary`, `ev-p070-orchestration-bottleneck`
- #16 Card `failure-intrinsic-self-correction-degradation`；路径 `failure/failure-intrinsic-self-correction-degradation.md`；Evidence `ev-p013-intrinsic-self-correction-degrades`, `ev-p013-oracle-free-equal-budget-boundary`
- #17 Card `failure-single-execution-denotation-false-positive`；路径 `failure/failure-single-execution-denotation-false-positive.md`；Evidence `ev-p101-metric-distortion`, `ev-p101-esm-fn-rate`
- #18 Card `failure-generic-or-unvalidated-tool-libraries-add-distractors`；路径 `failure/failure-generic-or-unvalidated-tool-libraries-add-distractors.md`；Evidence `ev-p078-validated-tool-creation-retrieval`, `ev-p078-multiview-tool-retrieval`, `ev-p078-generic-tool-and-baseline-boundary`, `ev-p078-toolset-construction-cost`, `ev-p078-baseline-fairness-boundary`

### 路线 `passage_hybrid`

- 命中数：24
- 降级：false（无）

- #1 Passage `P046:p0005:s0002`；Paper `P046`；页 5-5
- #2 Passage `P074:p0015:s0001`；Paper `P074`；页 15-15
- #3 Passage `P074:p0002:s0001`；Paper `P074`；页 2-2
- #4 Passage `P046:p0001:s0003`；Paper `P046`；页 1-1
- #5 Passage `P021:p0004:s0003`；Paper `P021`；页 4-4
- #6 Passage `P070:p0003:s0001`；Paper `P070`；页 3-3
- #7 Passage `P037:p0003:s0001`；Paper `P037`；页 3-3
- #8 Passage `P037:p0001:s0003`；Paper `P037`；页 1-1
- #9 Passage `P021:p0027:s0001`；Paper `P021`；页 27-27
- #10 Passage `P074:p0018:s0001`；Paper `P074`；页 18-18
- #11 Passage `P049:p0002:s0001`；Paper `P049`；页 2-2
- #12 Passage `P021:p0002:s0001`；Paper `P021`；页 2-2
- #13 Passage `P046:p0003:s0001`；Paper `P046`；页 3-3
- #14 Passage `P021:p0003:s0001`；Paper `P021`；页 3-3
- #15 Passage `P074:p0005:s0002`；Paper `P074`；页 5-5
- #16 Passage `P074:p0009:s0002`；Paper `P074`；页 9-9
- #17 Passage `P041:p0009:s0002`；Paper `P041`；页 9-9
- #18 Passage `P026:p0006:s0001`；Paper `P026`；页 6-6
- #19 Passage `P046:p0002:s0001`；Paper `P046`；页 2-2
- #20 Passage `P037:p0008:s0002`；Paper `P037`；页 8-8
- #21 Passage `P046:p0001:s0001`；Paper `P046`；页 1-1
- #22 Passage `P035:p0004:s0001`；Paper `P035`；页 4-4
- #23 Passage `P039:p0009:s0001`；Paper `P039`；页 9-9
- #24 Passage `P046:p0005:s0001`；Paper `P046`；页 5-5

## q005 · measurement

- 原始查询：`programmatic task success failure attribution tool-use agent benchmark`
- 规范化查询：`"programmatic" OR "task" OR "success" OR "failure" OR "attribution" OR "tool" OR "use" OR "agent" OR "benchmark"`

### 路线 `paper_card_fts`

- 命中数：18
- 降级：false（无）

- #1 Card `paper-p067`；路径 `paper/paper-p067.md`；Evidence `ev-p067-capability-preserving-safety`, `ev-p067-agentic-harm-not-chat-refusal`
- #2 Card `paper-p066`；路径 `paper/paper-p066.md`；Evidence `ev-p066-single-to-stateful-gap`, `ev-p066-multiturn-state-evaluation`
- #3 Card `paper-p037`；路径 `paper/paper-p037.md`；Evidence `ev-p037-evaluation-core`
- #4 Card `paper-p039`；路径 `paper/paper-p039.md`；Evidence `ev-p039-failure-core`
- #5 Card `paper-p021`；路径 `paper/paper-p021.md`；Evidence `ev-p021-operator-core`
- #6 Card `paper-llmcompiler`；路径 `paper/paper-llmcompiler.md`；Evidence `ev-p006-dependency-dag-dispatch`, `ev-p006-token-cost-accounting`, `ev-p006-shared-prompt-comparison-boundary`
- #7 Card `paper-p004`；路径 `paper/paper-p004.md`；Evidence `ev-p004-failure-core`
- #8 Card `paper-p036`；路径 `paper/paper-p036.md`；Evidence `ev-p036-failure-core`
- #9 Card `paper-p082`；路径 `paper/paper-p082.md`；Evidence `ev-p082-future-token-loss-filtered-calls`, `ev-p082-top-k-single-call-boundary`, `ev-p082-chaining-cost-sparsity-boundary`
- #10 Card `paper-react`；路径 `paper/paper-react.md`；Evidence `ev-p001-react-interleaved`, `ev-p001-search-hallucination-boundary`
- #11 Card `paper-p070`；路径 `paper/paper-p070.md`；Evidence `ev-p070-six-stage-attribution`, `ev-p070-light-tool-runtime-boundary`, `ev-p070-orchestration-bottleneck`
- #12 Card `paper-p035`；路径 `paper/paper-p035.md`；Evidence `ev-p035-evaluation-core`
- #13 Card `paper-p044`；路径 `paper/paper-p044.md`；Evidence `ev-p044-evaluation-core`
- #14 Card `paper-p028`；路径 `paper/paper-p028.md`；Evidence `ev-p028-operator-core`
- #15 Card `paper-p038`；路径 `paper/paper-p038.md`；Evidence `ev-p038-operator-core`
- #16 Card `paper-p083`；路径 `paper/paper-p083.md`；Evidence `ev-p083-three-surface-adversarial-failure`, `ev-p083-lightweight-defense-failure`, `ev-p083-simulated-tool-boundary`
- #17 Card `paper-p087`；路径 `paper/paper-p087.md`；Evidence `ev-p087-structured-query-independent-expansion`, `ev-p087-merge-and-semantic-judge`, `ev-p087-fields-not-universally-beneficial`
- #18 Card `paper-tau-bench`；路径 `paper/paper-tau-bench.md`；Evidence `ev-p007-terminal-state-evaluation`, `ev-p007-repeat-reliability-collapse`

### 路线 `passage_hybrid`

- 命中数：24
- 降级：false（无）

- #1 Passage `P040:p0001:s0003`；Paper `P040`；页 1-1
- #2 Passage `P040:p0003:s0002`；Paper `P040`；页 3-3
- #3 Passage `P040:p0006:s0001`；Paper `P040`；页 6-6
- #4 Passage `P040:p0002:s0002`；Paper `P040`；页 2-2
- #5 Passage `P040:p0011:s0002`；Paper `P040`；页 11-11
- #6 Passage `P035:p0009:s0001`；Paper `P035`；页 9-9
- #7 Passage `P040:p0003:s0001`；Paper `P040`；页 3-3
- #8 Passage `P016:p0013:s0001`；Paper `P016`；页 13-13
- #9 Passage `P039:p0001:s0003`；Paper `P039`；页 1-1
- #10 Passage `P035:p0027:s0001`；Paper `P035`；页 27-27
- #11 Passage `P035:p0008:s0001`；Paper `P035`；页 8-8
- #12 Passage `P039:p0003:s0002`；Paper `P039`；页 3-3
- #13 Passage `P035:p0008:s0002`；Paper `P035`；页 8-8
- #14 Passage `P035:p0026:s0001`；Paper `P035`；页 26-26
- #15 Passage `P040:p0010:s0003`；Paper `P040`；页 10-10
- #16 Passage `P039:p0002:s0001`；Paper `P039`；页 2-2
- #17 Passage `P016:p0008:s0001`；Paper `P016`；页 8-8
- #18 Passage `P083:p0016:s0001`；Paper `P083`；页 16-16
- #19 Passage `P039:p0002:s0002`；Paper `P039`；页 2-2
- #20 Passage `P039:p0007:s0002`；Paper `P039`；页 7-7
- #21 Passage `P036:p0008:s0001`；Paper `P036`；页 8-8
- #22 Passage `P035:p0028:s0001`；Paper `P035`；页 28-28
- #23 Passage `P035:p0022:s0001`；Paper `P035`；页 22-22
- #24 Passage `P035:p0029:s0001`；Paper `P035`；页 29-29

### 路线 `failure_card_fts`

- 命中数：18
- 降级：false（无）

- #1 Card `failure-likelihood-utility-does-not-guarantee-agent-utility`；路径 `failure/failure-likelihood-utility-does-not-guarantee-agent-utility.md`；Evidence `ev-p082-future-token-loss-filtered-calls`, `ev-p082-top-k-single-call-boundary`, `ev-p082-chaining-cost-sparsity-boundary`
- #2 Card `failure-tool-use-metrics-collapse-distinct-errors`；路径 `failure/failure-tool-use-metrics-collapse-distinct-errors.md`；Evidence `ev-p039-failure-core`, `ev-p039-aggregate-score-masking`
- #3 Card `failure-light-tool-runtime-bottleneck-overreach`；路径 `failure/failure-light-tool-runtime-bottleneck-overreach.md`；Evidence `ev-p070-six-stage-attribution`, `ev-p070-light-tool-runtime-boundary`, `ev-p070-orchestration-bottleneck`
- #4 Card `failure-gold-context-does-not-solve-knowledge-use`；路径 `failure/failure-gold-context-does-not-solve-knowledge-use.md`；Evidence `ev-p036-failure-core`
- #5 Card `failure-confident-completion-without-state-success`；路径 `failure/failure-confident-completion-without-state-success.md`；Evidence `ev-p040-failure-core`
- #6 Card `failure-external-instructor-attribution`；路径 `failure/failure-external-instructor-attribution.md`；Evidence `ev-p014-external-instructor-confound`
- #7 Card `failure-internal-tool-confidence-not-execution-success`；路径 `failure/failure-internal-tool-confidence-not-execution-success.md`；Evidence `ev-p073-execution-supervised-probe`, `ev-p073-internal-confidence-misalignment`
- #8 Card `failure-natural-language-ir-hurts-formal-planning`；路径 `failure/failure-natural-language-ir-hurts-formal-planning.md`；Evidence `ev-p060-formal-ir-solver`, `ev-p060-ir-result-and-nl-failure`
- #9 Card `failure-large-corpus-tool-retrieval-breaks-oracle-menu`；路径 `failure/failure-large-corpus-tool-retrieval-breaks-oracle-menu.md`；Evidence `ev-p085-large-corpus-scale`, `ev-p085-retrieval-completeness-failure`, `ev-p085-non-exhaustive-label`
- #10 Card `failure-repeat-run-reliability-collapse`；路径 `failure/failure-repeat-run-reliability-collapse.md`；Evidence `ev-p007-repeat-reliability-collapse`
- #11 Card `failure-semantically-related-toolkit-expansion`；路径 `failure/failure-semantically-related-toolkit-expansion.md`；Evidence `ev-p084-expanded-toolkit-controlled-setting`, `ev-p084-related-toolkit-error-types`, `ev-p084-expanded-toolkit-table`, `ev-p084-generated-tool-single-dataset-boundary`
- #12 Card `failure-single-turn-tool-score-overstates-agent-competence`；路径 `failure/failure-single-turn-tool-score-overstates-agent-competence.md`；Evidence `ev-p066-single-to-stateful-gap`, `ev-p066-multiturn-state-evaluation`
- #13 Card `failure-one-shot-expert-gold-is-brittle`；路径 `failure/failure-one-shot-expert-gold-is-brittle.md`；Evidence `ev-p068-audit-then-score`, `ev-p068-one-shot-gold-brittle`
- #14 Card `failure-constrained-plan-surface-validity`；路径 `failure/failure-constrained-plan-surface-validity.md`；Evidence `ev-p004-failure-core`, `ev-p004-macro-constraint-failure`
- #15 Card `failure-raw-observation-overload-hides-action-relevant-ui`；路径 `failure/failure-raw-observation-overload-hides-action-relevant-ui.md`；Evidence `ev-p079-action-conditioned-contextualization`, `ev-p079-ground-truth-action-retry`, `ev-p079-unseen-ui-boundary`
- #16 Card `failure-memory-unit-granularity-mismatch`；路径 `failure/failure-memory-unit-granularity-mismatch.md`；Evidence `ev-p011-failure-core`
- #17 Card `failure-llm-freshness-judgment-prior-override-and-drift`；路径 `failure/failure-llm-freshness-judgment-prior-override-and-drift.md`；Evidence `ev-p095-prior-override-drift`, `ev-p095-matched-comparison`
- #18 Card `failure-grounded-formalization-output-expansion`；路径 `failure/failure-grounded-formalization-output-expansion.md`；Evidence `ev-p053-higher-order-generator`, `ev-p053-pattern-review-confound`, `ev-p053-parser-evaluation-boundary`

### 路线 `operator_card_fts`

- 命中数：18
- 降级：false（无）

- #1 Card `operator-stagewise-agent-security-audit`；路径 `operator/operator-stagewise-agent-security-audit.md`；Evidence `ev-p008-stagewise-attack-surface`
- #2 Card `operator-capability-preserving-agent-safety-evaluation`；路径 `operator/operator-capability-preserving-agent-safety-evaluation.md`；Evidence `ev-p067-capability-preserving-safety`, `ev-p067-agentic-harm-not-chat-refusal`
- #3 Card `operator-stagewise-mcp-cost-attribution`；路径 `operator/operator-stagewise-mcp-cost-attribution.md`；Evidence `ev-p070-six-stage-attribution`, `ev-p070-light-tool-runtime-boundary`, `ev-p070-orchestration-bottleneck`
- #4 Card `operator-execution-supervised-prompt-trace-calibration`；路径 `operator/operator-execution-supervised-prompt-trace-calibration.md`；Evidence `ev-p073-execution-supervised-probe`, `ev-p073-internal-confidence-misalignment`
- #5 Card `operator-terminal-state-reliability-evaluation`；路径 `operator/operator-terminal-state-reliability-evaluation.md`；Evidence `ev-p007-terminal-state-evaluation`
- #6 Card `operator-hidden-state-tool-necessity-prefill`；路径 `operator/operator-hidden-state-tool-necessity-prefill.md`；Evidence `ev-p041-operator-core`, `ev-p041-probe-prefill-steering`
- #7 Card `operator-grounded-structured-tool-document-expansion`；路径 `operator/operator-grounded-structured-tool-document-expansion.md`；Evidence `ev-p087-structured-query-independent-expansion`, `ev-p087-merge-and-semantic-judge`, `ev-p087-fields-not-universally-beneficial`
- #8 Card `operator-evidence-audit-before-score`；路径 `operator/operator-evidence-audit-before-score.md`；Evidence `ev-p068-audit-then-score`, `ev-p068-one-shot-gold-brittle`
- #9 Card `operator-learned-memory-crud-control`；路径 `operator/operator-learned-memory-crud-control.md`；Evidence `ev-p028-operator-core`
- #10 Card `operator-future-token-loss-filtered-tool-learning`；路径 `operator/operator-future-token-loss-filtered-tool-learning.md`；Evidence `ev-p082-future-token-loss-filtered-calls`, `ev-p082-top-k-single-call-boundary`, `ev-p082-chaining-cost-sparsity-boundary`
- #11 Card `operator-validated-specialized-tool-creation-retrieval`；路径 `operator/operator-validated-specialized-tool-creation-retrieval.md`；Evidence `ev-p078-validated-tool-creation-retrieval`, `ev-p078-multiview-tool-retrieval`, `ev-p078-generic-tool-and-baseline-boundary`, `ev-p078-toolset-construction-cost`, `ev-p078-baseline-fairness-boundary`
- #12 Card `operator-tool-grounded-critique`；路径 `operator/operator-tool-grounded-critique.md`；Evidence `ev-p032-operator-core`
- #13 Card `operator-decomposed-research-evidence-evaluation`；路径 `operator/operator-decomposed-research-evidence-evaluation.md`；Evidence `ev-p042-evaluation-core`, `ev-p043-evaluation-core`, `ev-p044-evaluation-core`
- #14 Card `operator-grouped-masked-history-step-credit`；路径 `operator/operator-grouped-masked-history-step-credit.md`；Evidence `ev-p025-failure-core`, `ev-p025-grouped-step-influence`
- #15 Card `operator-unified-language-memory-action-policy`；路径 `operator/operator-unified-language-memory-action-policy.md`；Evidence `ev-p062-unified-memory-action-policy`, `ev-p062-broadcast-advantage`
- #16 Card `operator-outcome-trained-execution-state-planner`；路径 `operator/operator-outcome-trained-execution-state-planner.md`；Evidence `ev-p021-operator-core`
- #17 Card `operator-experience-insight-update`；路径 `operator/operator-experience-insight-update.md`；Evidence `ev-p018-insight-update-operations`
- #18 Card `operator-bounded-preexecution-reviewer`；路径 `operator/operator-bounded-preexecution-reviewer.md`；Evidence `ev-p049-operator-core`, `ev-p049-bounded-review-loop`

## 紧凑研究地图

> 按 Paper 去重；注意力权重只反映用途路线顺序和机械噪声标记，不是相关性或科研结论。

- Paper `P001`；用途 measurement, operator；观测 2（重复 1）；最佳导航路线 `q005:paper_card_fts`；噪声标记：无
- Paper `P002`；用途 failure, operator；观测 4（重复 3）；最佳导航路线 `q003:operator_card_fts`；噪声标记：无
- Paper `P003`；用途 prior；观测 3（重复 2）；最佳导航路线 `q004:paper_card_fts`；噪声标记：无
- Paper `P004`；用途 failure, measurement, operator, prior, problem；观测 10（重复 9）；最佳导航路线 `q002:failure_card_fts`；噪声标记：无
- Paper `P006`；用途 failure, measurement；观测 2（重复 1）；最佳导航路线 `q005:paper_card_fts`；噪声标记：无
- Paper `P007`；用途 failure, measurement, prior, problem；观测 8（重复 7）；最佳导航路线 `q005:paper_card_fts`；噪声标记：无
- Paper `P008`；用途 measurement, prior, problem；观测 3（重复 2）；最佳导航路线 `q004:paper_card_fts`；噪声标记：无
- Paper `P015`；用途 failure；观测 1（重复 0）；最佳导航路线 `q002:failure_card_fts`；噪声标记：无
- Paper `P017`；用途 failure, operator, problem；观测 3（重复 2）；最佳导航路线 `q002:failure_card_fts`；噪声标记：无
- Paper `P019`；用途 operator, problem；观测 2（重复 1）；最佳导航路线 `q001:paper_card_fts`；噪声标记：无
- Paper `P020`；用途 operator；观测 3（重复 2）；最佳导航路线 `q003:operator_card_fts`；噪声标记：无
- Paper `P021`；用途 failure, measurement, operator, prior, problem；观测 13（重复 12）；最佳导航路线 `q001:paper_card_fts`；噪声标记：无
- Paper `P025`；用途 measurement, operator, prior, problem；观测 6（重复 5）；最佳导航路线 `q004:paper_card_fts`；噪声标记：无
- Paper `P026`；用途 failure, operator, prior, problem；观测 8（重复 7）；最佳导航路线 `q004:paper_card_fts`；噪声标记：无
- Paper `P027`；用途 operator, problem；观测 3（重复 2）；最佳导航路线 `q003:operator_card_fts`；噪声标记：无
- Paper `P028`；用途 measurement, problem；观测 3（重复 2）；最佳导航路线 `q001:paper_card_fts`；噪声标记：无
- Paper `P030`；用途 failure, prior, problem；观测 13（重复 12）；最佳导航路线 `q002:failure_card_fts`；噪声标记：无
- Paper `P031`；用途 problem；观测 3（重复 2）；最佳导航路线 `q001:paper_card_fts`；噪声标记：无
- Paper `P034`；用途 operator, prior；观测 3（重复 2）；最佳导航路线 `q004:paper_card_fts`；噪声标记：无
- Paper `P035`；用途 failure, measurement, operator, prior；观测 12（重复 11）；最佳导航路线 `q005:paper_card_fts`；噪声标记：无
- Paper `P036`；用途 failure, measurement, operator, prior, problem；观测 8（重复 7）；最佳导航路线 `q005:paper_card_fts`；噪声标记：无
- Paper `P037`；用途 failure, measurement, prior, problem；观测 7（重复 6）；最佳导航路线 `q005:paper_card_fts`；噪声标记：无
- Paper `P038`；用途 measurement, operator, problem；观测 3（重复 2）；最佳导航路线 `q001:paper_card_fts`；噪声标记：无
- Paper `P039`；用途 failure, measurement, prior, problem；观测 13（重复 12）；最佳导航路线 `q005:paper_card_fts`；噪声标记：无
- Paper `P040`；用途 failure, measurement, operator, prior, problem；观测 15（重复 14）；最佳导航路线 `q001:paper_card_fts`；噪声标记：无
- Paper `P041`；用途 failure, measurement, operator, prior, problem；观测 9（重复 8）；最佳导航路线 `q004:paper_card_fts`；噪声标记：无
- Paper `P044`；用途 measurement, prior；观测 3（重复 2）；最佳导航路线 `q004:paper_card_fts`；噪声标记：无
- Paper `P046`；用途 failure, operator, prior, problem；观测 18（重复 17）；最佳导航路线 `q004:paper_card_fts`；噪声标记：无
- Paper `P049`；用途 failure, measurement, operator, prior, problem；观测 12（重复 11）；最佳导航路线 `q004:paper_card_fts`；噪声标记：无
- Paper `P050`；用途 operator, prior；观测 5（重复 4）；最佳导航路线 `q003:operator_card_fts`；噪声标记：无
- Paper `P051`；用途 prior；观测 2（重复 1）；最佳导航路线 `q004:paper_card_fts`；噪声标记：无
- Paper `P063`；用途 operator；观测 2（重复 1）；最佳导航路线 `q003:operator_card_fts`；噪声标记：无
- Paper `P064`；用途 failure, problem；观测 2（重复 1）；最佳导航路线 `q002:failure_card_fts`；噪声标记：无
- Paper `P065`；用途 failure, problem；观测 5（重复 4）；最佳导航路线 `q002:failure_card_fts`；噪声标记：无
- Paper `P066`；用途 failure, measurement, problem；观测 6（重复 5）；最佳导航路线 `q005:paper_card_fts`；噪声标记：无
- Paper `P067`；用途 measurement, problem；观测 5（重复 4）；最佳导航路线 `q005:paper_card_fts`；噪声标记：无
- Paper `P070`；用途 measurement, prior；观测 5（重复 4）；最佳导航路线 `q005:paper_card_fts`；噪声标记：无
- Paper `P071`；用途 operator, problem；观测 3（重复 2）；最佳导航路线 `q003:operator_card_fts`；噪声标记：无
- Paper `P073`；用途 failure, measurement, operator, prior, problem；观测 10（重复 9）；最佳导航路线 `q001:paper_card_fts`；噪声标记：无
- Paper `P074`；用途 failure, operator, prior, problem；观测 22（重复 21）；最佳导航路线 `q004:paper_card_fts`；噪声标记：无
- Paper `P078`；用途 failure, measurement, operator, prior, problem；观测 8（重复 7）；最佳导航路线 `q003:operator_card_fts`；噪声标记：无
- Paper `P079`；用途 failure, measurement, operator；观测 5（重复 4）；最佳导航路线 `q002:failure_card_fts`；噪声标记：无
- Paper `P080`；用途 operator, problem；观测 3（重复 2）；最佳导航路线 `q003:operator_card_fts`；噪声标记：无
- Paper `P081`；用途 operator；观测 2（重复 1）；最佳导航路线 `q003:operator_card_fts`；噪声标记：无
- Paper `P082`；用途 measurement, operator；观测 5（重复 4）；最佳导航路线 `q005:paper_card_fts`；噪声标记：无
- Paper `P083`；用途 failure, measurement, prior, problem；观测 5（重复 4）；最佳导航路线 `q002:failure_card_fts`；噪声标记：无
- Paper `P085`；用途 failure, measurement, problem；观测 4（重复 3）；最佳导航路线 `q001:paper_card_fts`；噪声标记：无
- Paper `P087`；用途 failure, measurement；观测 3（重复 2）；最佳导航路线 `q005:paper_card_fts`；噪声标记：无
- Paper `P091`；用途 failure；观测 4（重复 3）；最佳导航路线 `q002:failure_card_fts`；噪声标记：无
- Paper `P095`；用途 measurement, operator, prior, problem；观测 7（重复 6）；最佳导航路线 `q001:paper_card_fts`；噪声标记：无
- Paper `P097`；用途 failure, operator, prior, problem；观测 11（重复 10）；最佳导航路线 `q003:operator_card_fts`；噪声标记：无
- Paper `P098`；用途 failure；观测 1（重复 0）；最佳导航路线 `q002:failure_card_fts`；噪声标记：无
- Paper `P099`；用途 failure, operator；观测 7（重复 6）；最佳导航路线 `q003:operator_card_fts`；噪声标记：无
- Paper `P101`；用途 operator, prior, problem；观测 4（重复 3）；最佳导航路线 `q003:operator_card_fts`；噪声标记：无
- Paper `P005`；用途 failure, operator；观测 2（重复 1）；最佳导航路线 `q003:paper_card_fts`；噪声标记：无
- Paper `P010`；用途 problem；观测 1（重复 0）；最佳导航路线 `q001:failure_card_fts`；噪声标记：无
- Paper `P016`；用途 measurement, operator, prior, problem；观测 9（重复 8）；最佳导航路线 `q004:operator_card_fts`；噪声标记：weak_lexical_overlap
- Paper `P032`；用途 failure, measurement, prior；观测 3（重复 2）；最佳导航路线 `q004:operator_card_fts`；噪声标记：无
- Paper `P048`；用途 failure, prior, problem；观测 5（重复 4）；最佳导航路线 `q004:operator_card_fts`；噪声标记：无
- Paper `P052`；用途 prior；观测 1（重复 0）；最佳导航路线 `q004:operator_card_fts`；噪声标记：无
- Paper `P058`；用途 operator, prior；观测 3（重复 2）；最佳导航路线 `q004:operator_card_fts`；噪声标记：无
- Paper `P060`；用途 measurement, prior, problem；观测 4（重复 3）；最佳导航路线 `q004:operator_card_fts`；噪声标记：无
- Paper `P072`；用途 failure, operator；观测 4（重复 3）；最佳导航路线 `q002:passage_hybrid`；噪声标记：无
- Paper `P075`；用途 problem；观测 1（重复 0）；最佳导航路线 `q001:failure_card_fts`；噪声标记：无
- Paper `P084`；用途 failure, measurement, operator, problem；观测 4（重复 3）；最佳导航路线 `q001:failure_card_fts`；噪声标记：无
- Paper `P094`；用途 operator, problem；观测 3（重复 2）；最佳导航路线 `q003:paper_card_fts`；噪声标记：无
- Paper `P096`；用途 operator, prior；观测 3（重复 2）；最佳导航路线 `q004:operator_card_fts`；噪声标记：无
- Paper `P011`；用途 measurement；观测 1（重复 0）；最佳导航路线 `q005:failure_card_fts`；噪声标记：无
- Paper `P013`；用途 prior；观测 1（重复 0）；最佳导航路线 `q004:failure_card_fts`；噪声标记：无
- Paper `P014`；用途 measurement；观测 1（重复 0）；最佳导航路线 `q005:failure_card_fts`；噪声标记：无
- Paper `P023`；用途 problem；观测 1（重复 0）；最佳导航路线 `q001:passage_hybrid`；噪声标记：无
- Paper `P033`；用途 operator, prior；观测 2（重复 1）；最佳导航路线 `q004:failure_card_fts`；噪声标记：无
- Paper `P053`；用途 measurement；观测 1（重复 0）；最佳导航路线 `q005:failure_card_fts`；噪声标记：无
- Paper `P054`；用途 prior；观测 1（重复 0）；最佳导航路线 `q004:failure_card_fts`；噪声标记：无
- Paper `P055`；用途 prior；观测 1（重复 0）；最佳导航路线 `q004:failure_card_fts`；噪声标记：无
- Paper `P057`；用途 operator, prior；观测 2（重复 1）；最佳导航路线 `q004:failure_card_fts`；噪声标记：无
- Paper `P059`；用途 failure；观测 2（重复 1）；最佳导航路线 `q002:operator_card_fts`；噪声标记：无
- Paper `P068`；用途 measurement, operator, problem；观测 4（重复 3）；最佳导航路线 `q005:failure_card_fts`；噪声标记：无
- Paper `P076`；用途 problem；观测 1（重复 0）；最佳导航路线 `q001:passage_hybrid`；噪声标记：无
- Paper `P088`；用途 failure, problem；观测 3（重复 2）；最佳导航路线 `q002:operator_card_fts`；噪声标记：无
- Paper `P018`；用途 measurement；观测 1（重复 0）；最佳导航路线 `q005:operator_card_fts`；噪声标记：无
- Paper `P042`；用途 measurement；观测 1（重复 0）；最佳导航路线 `q005:operator_card_fts`；噪声标记：无
- Paper `P043`；用途 measurement；观测 1（重复 0）；最佳导航路线 `q005:operator_card_fts`；噪声标记：无
- Paper `P047`；用途 failure；观测 1（重复 0）；最佳导航路线 `q002:paper_card_fts`；噪声标记：无
- Paper `P062`；用途 measurement, operator；观测 2（重复 1）；最佳导航路线 `q003:failure_card_fts`；噪声标记：无

## 覆盖诊断

- 去重 Card：151
- 去重 Evidence：169
- 去重 Passage：103
- 命中 Paper：85
- 原始观测：390
- 带机械噪声标记的观测：1
