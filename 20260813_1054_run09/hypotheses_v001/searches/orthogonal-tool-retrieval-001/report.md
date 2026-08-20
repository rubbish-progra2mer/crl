<!-- CRL_RESEARCH_SEARCH_META {"created_at_utc":"2026-08-13T03:07:34.736981Z","request_fingerprint_sha256":"6e3447326b51f2fc5b6f71c83c1f3a0bf4ca09d41154ecc7c8eb1658c09c08e9","result_json_sha256":"830e2769aead217fc728505f0c9db17a19033723f1005f74ef6460ec380e7079","search_id":"orthogonal-tool-retrieval-001"} -->
# 研究检索导航

> 本报告仅展示查询路线、来源、命中定位与覆盖；所有科研判断由主研究者完成。

- 搜索标识：`orthogonal-tool-retrieval-001`
- 生成时间（协调世界时）：`2026-08-13T03:07:34.736981Z`

## q001 · problem

- 原始查询：`large tool library retrieval multi-tool chain incomplete candidate menu language agents`
- 规范化查询：`"large" OR "tool" OR "library" OR "retrieval" OR "multi" OR "chain" OR "incomplete" OR "candidate" OR "menu" OR "language" OR "agents"`

### 路线 `paper_card_fts`

- 命中数：20
- 降级：false（无）

- #1 Card `paper-p085`；路径 `paper/paper-p085.md`；Evidence `ev-p085-large-corpus-scale`, `ev-p085-retrieval-completeness-failure`, `ev-p085-non-exhaustive-label`
- #2 Card `paper-p081`；路径 `paper/paper-p081.md`；Evidence `ev-p081-independent-path-majority-aggregation`, `ev-p081-forty-sample-baseline`, `ev-p081-fixed-answer-space-boundary`
- #3 Card `paper-p005`；路径 `paper/paper-p005.md`；Evidence `ev-p005-operator-core`
- #4 Card `paper-p078`；路径 `paper/paper-p078.md`；Evidence `ev-p078-validated-tool-creation-retrieval`, `ev-p078-multiview-tool-retrieval`, `ev-p078-generic-tool-and-baseline-boundary`, `ev-p078-toolset-construction-cost`, `ev-p078-baseline-fairness-boundary`
- #5 Card `paper-p086`；路径 `paper/paper-p086.md`；Evidence `ev-p086-hypothesize-retrieve-invoke`, `ev-p086-required-parameter-score`, `ev-p086-near-identical-distribution`
- #6 Card `paper-p028`；路径 `paper/paper-p028.md`；Evidence `ev-p028-operator-core`
- #7 Card `paper-p032`；路径 `paper/paper-p032.md`；Evidence `ev-p032-operator-core`
- #8 Card `paper-p056`；路径 `paper/paper-p056.md`；Evidence `ev-p056-graph-optimization`, `ev-p056-same-set-crosswords`, `ev-p056-dylan-cost-quality`
- #9 Card `paper-p013`；路径 `paper/paper-p013.md`；Evidence `ev-p013-intrinsic-self-correction-degrades`, `ev-p013-oracle-free-equal-budget-boundary`
- #10 Card `paper-p004`；路径 `paper/paper-p004.md`；Evidence `ev-p004-failure-core`
- #11 Card `paper-p036`；路径 `paper/paper-p036.md`；Evidence `ev-p036-failure-core`
- #12 Card `paper-p077`；路径 `paper/paper-p077.md`；Evidence `ev-p077-hierarchical-utterance-critic-token-actor`, `ev-p077-trajectory-only-sample-efficiency`, `ev-p077-oracle-reward-hacking-boundary`
- #13 Card `paper-p051`；路径 `paper/paper-p051.md`；Evidence `ev-p051-formalization-pipeline`, `ev-p051-solver-guarantee-boundary`, `ev-p051-omitted-constraint-failure`, `ev-p051-cost-boundary`
- #14 Card `paper-p014`；路径 `paper/paper-p014.md`；Evidence `ev-p014-dynamic-reflection-gate`, `ev-p014-external-instructor-confound`
- #15 Card `paper-p073`；路径 `paper/paper-p073.md`；Evidence `ev-p073-execution-supervised-probe`, `ev-p073-internal-confidence-misalignment`
- #16 Card `paper-p084`；路径 `paper/paper-p084.md`；Evidence `ev-p084-expanded-toolkit-controlled-setting`, `ev-p084-related-toolkit-error-types`, `ev-p084-expanded-toolkit-table`, `ev-p084-generated-tool-single-dataset-boundary`
- #17 Card `paper-p049`；路径 `paper/paper-p049.md`；Evidence `ev-p049-operator-core`
- #18 Card `paper-p090`；路径 `paper/paper-p090.md`；Evidence `ev-p090-fixed-granularity-selection`, `ev-p090-entropy-router`, `ev-p090-association-graph`
- #19 Card `paper-p046`；路径 `paper/paper-p046.md`；Evidence `ev-p046-operator-core`
- #20 Card `paper-p089`；路径 `paper/paper-p089.md`；Evidence `ev-p089-training-gold-count-hypothetical-tools`, `ev-p089-overview-alignment-rrf`, `ev-p089-hungarian-alignment`, `ev-p089-forced-alignment-proxy`, `ev-p089-retrieval-only-metrics`, `ev-p089-api-latency-boundary`

### 路线 `failure_card_fts`

- 命中数：20
- 降级：false（无）

- #1 Card `failure-large-corpus-tool-retrieval-breaks-oracle-menu`；路径 `failure/failure-large-corpus-tool-retrieval-breaks-oracle-menu.md`；Evidence `ev-p085-large-corpus-scale`, `ev-p085-retrieval-completeness-failure`, `ev-p085-non-exhaustive-label`
- #2 Card `failure-semantically-related-toolkit-expansion`；路径 `failure/failure-semantically-related-toolkit-expansion.md`；Evidence `ev-p084-expanded-toolkit-controlled-setting`, `ev-p084-related-toolkit-error-types`, `ev-p084-expanded-toolkit-table`, `ev-p084-generated-tool-single-dataset-boundary`
- #3 Card `failure-fixed-single-granularity-memory`；路径 `failure/failure-fixed-single-granularity-memory.md`；Evidence `ev-p090-fixed-granularity-selection`, `ev-p090-entropy-router`
- #4 Card `failure-incomplete-tool-contracts-false-verified-state`；路径 `failure/failure-incomplete-tool-contracts-false-verified-state.md`；Evidence `ev-p074-contract-state-commit`, `ev-p074-missing-schema-true-postcondition`
- #5 Card `failure-constrained-plan-surface-validity`；路径 `failure/failure-constrained-plan-surface-validity.md`；Evidence `ev-p004-failure-core`, `ev-p004-macro-constraint-failure`
- #6 Card `failure-generic-or-unvalidated-tool-libraries-add-distractors`；路径 `failure/failure-generic-or-unvalidated-tool-libraries-add-distractors.md`；Evidence `ev-p078-validated-tool-creation-retrieval`, `ev-p078-multiview-tool-retrieval`, `ev-p078-generic-tool-and-baseline-boundary`, `ev-p078-toolset-construction-cost`, `ev-p078-baseline-fairness-boundary`
- #7 Card `failure-likelihood-utility-does-not-guarantee-agent-utility`；路径 `failure/failure-likelihood-utility-does-not-guarantee-agent-utility.md`；Evidence `ev-p082-future-token-loss-filtered-calls`, `ev-p082-top-k-single-call-boundary`, `ev-p082-chaining-cost-sparsity-boundary`
- #8 Card `failure-single-turn-tool-score-overstates-agent-competence`；路径 `failure/failure-single-turn-tool-score-overstates-agent-competence.md`；Evidence `ev-p066-single-to-stateful-gap`, `ev-p066-multiturn-state-evaluation`
- #9 Card `failure-multi-agent-adversarial-coordination-spans-trust-surfaces`；路径 `failure/failure-multi-agent-adversarial-coordination-spans-trust-surfaces.md`；Evidence `ev-p083-three-surface-adversarial-failure`, `ev-p083-lightweight-defense-failure`, `ev-p083-simulated-tool-boundary`
- #10 Card `failure-interactive-gains-collapse-against-independent-sampling`；路径 `failure/failure-interactive-gains-collapse-against-independent-sampling.md`；Evidence `ev-p081-independent-path-majority-aggregation`, `ev-p081-forty-sample-baseline`, `ev-p081-fixed-answer-space-boundary`
- #11 Card `failure-gold-context-does-not-solve-knowledge-use`；路径 `failure/failure-gold-context-does-not-solve-knowledge-use.md`；Evidence `ev-p036-failure-core`
- #12 Card `failure-debate-cost-nondominance`；路径 `failure/failure-debate-cost-nondominance.md`；Evidence `ev-p015-debate-cost-nondominance`
- #13 Card `failure-natural-language-ir-hurts-formal-planning`；路径 `failure/failure-natural-language-ir-hurts-formal-planning.md`；Evidence `ev-p060-formal-ir-solver`, `ev-p060-ir-result-and-nl-failure`
- #14 Card `failure-confident-completion-without-state-success`；路径 `failure/failure-confident-completion-without-state-success.md`；Evidence `ev-p040-failure-core`
- #15 Card `failure-lazy-agent-effective-single-agent-collapse`；路径 `failure/failure-lazy-agent-effective-single-agent-collapse.md`；Evidence `ev-p025-failure-core`
- #16 Card `failure-raw-observation-overload-hides-action-relevant-ui`；路径 `failure/failure-raw-observation-overload-hides-action-relevant-ui.md`；Evidence `ev-p079-action-conditioned-contextualization`, `ev-p079-ground-truth-action-retry`, `ev-p079-unseen-ui-boundary`
- #17 Card `failure-untrusted-agent-metadata-privileged-control-flow`；路径 `failure/failure-untrusted-agent-metadata-privileged-control-flow.md`；Evidence `ev-p076-metadata-control-flow-laundering`, `ev-p076-refusal-not-system-safety`, `ev-p076-controlled-lab-boundary`
- #18 Card `failure-unified-memory-policy-retains-terminal-credit-smearing`；路径 `failure/failure-unified-memory-policy-retains-terminal-credit-smearing.md`；Evidence `ev-p062-unified-memory-action-policy`, `ev-p062-broadcast-advantage`
- #19 Card `failure-sparse-topology-suppresses-correct-insight`；路径 `failure/failure-sparse-topology-suppresses-correct-insight.md`；Evidence `ev-p017-failure-core`
- #20 Card `failure-forced-hypothetical-tool-alignment`；路径 `failure/failure-forced-hypothetical-tool-alignment.md`；Evidence `ev-p089-training-gold-count-hypothetical-tools`, `ev-p089-hungarian-alignment`, `ev-p089-forced-alignment-proxy`, `ev-p089-retrieval-only-metrics`

### 路线 `passage_hybrid`

- 命中数：20
- 降级：false（无）

- #1 Passage `P087:p0001:s0002`；Paper `P087`；页 1-1
- #2 Passage `P085:p0001:s0003`；Paper `P085`；页 1-1
- #3 Passage `P087:p0011:s0001`；Paper `P087`；页 11-11
- #4 Passage `P063:p0011:s0001`；Paper `P063`；页 11-11
- #5 Passage `P085:p0013:s0001`；Paper `P085`；页 13-13
- #6 Passage `P085:p0001:s0002`；Paper `P085`；页 1-1
- #7 Passage `P074:p0015:s0001`；Paper `P074`；页 15-15
- #8 Passage `P048:p0001:s0003`；Paper `P048`；页 1-1
- #9 Passage `P087:p0002:s0001`；Paper `P087`；页 2-2
- #10 Passage `P087:p0012:s0001`；Paper `P087`；页 12-12
- #11 Passage `P085:p0012:s0001`；Paper `P085`；页 12-12
- #12 Passage `P100:p0003:s0002`；Paper `P100`；页 3-3
- #13 Passage `P086:p0001:s0001`；Paper `P086`；页 1-1
- #14 Passage `P087:p0001:s0003`；Paper `P087`；页 1-1
- #15 Passage `P085:p0025:s0001`；Paper `P085`；页 25-25
- #16 Passage `P095:p0007:s0001`；Paper `P095`；页 7-7
- #17 Passage `P004:p0003:s0002`；Paper `P004`；页 3-3
- #18 Passage `P085:p0002:s0001`；Paper `P085`；页 2-2
- #19 Passage `P086:p0006:s0001`；Paper `P086`；页 6-6
- #20 Passage `P085:p0003:s0001`；Paper `P085`；页 3-3

### 路线 `operator_card_fts`

- 命中数：20
- 降级：false（无）

- #1 Card `operator-validated-specialized-tool-creation-retrieval`；路径 `operator/operator-validated-specialized-tool-creation-retrieval.md`；Evidence `ev-p078-validated-tool-creation-retrieval`, `ev-p078-multiview-tool-retrieval`, `ev-p078-generic-tool-and-baseline-boundary`, `ev-p078-toolset-construction-cost`, `ev-p078-baseline-fairness-boundary`
- #2 Card `operator-smt-preexecution-policy-guard`；路径 `operator/operator-smt-preexecution-policy-guard.md`；Evidence `ev-p046-operator-core`
- #3 Card `operator-bilevel-graph-toolchain-planning`；路径 `operator/operator-bilevel-graph-toolchain-planning.md`；Evidence `ev-p048-operator-core`
- #4 Card `operator-cost-penalized-structured-clarification`；路径 `operator/operator-cost-penalized-structured-clarification.md`；Evidence `ev-p072-structured-clarification-gate`, `ev-p072-unstructured-clarification-failure`, `ev-p072-compute-boundary`
- #5 Card `operator-thought-tree-search`；路径 `operator/operator-thought-tree-search.md`；Evidence `ev-p002-branch-evaluate-search`
- #6 Card `operator-future-token-loss-filtered-tool-learning`；路径 `operator/operator-future-token-loss-filtered-tool-learning.md`；Evidence `ev-p082-future-token-loss-filtered-calls`, `ev-p082-top-k-single-call-boundary`, `ev-p082-chaining-cost-sparsity-boundary`
- #7 Card `operator-agreement-prior-modulation`；路径 `operator/operator-agreement-prior-modulation.md`；Evidence `ev-p015-agreement-prior`
- #8 Card `operator-fixed-budget-independent-path-aggregation`；路径 `operator/operator-fixed-budget-independent-path-aggregation.md`；Evidence `ev-p081-independent-path-majority-aggregation`, `ev-p081-forty-sample-baseline`, `ev-p081-fixed-answer-space-boundary`
- #9 Card `operator-required-parameter-description-tool-retrieval`；路径 `operator/operator-required-parameter-description-tool-retrieval.md`；Evidence `ev-p086-hypothesize-retrieve-invoke`, `ev-p086-required-parameter-score`, `ev-p086-near-identical-distribution`
- #10 Card `operator-syntax-aligned-formal-ir-planning`；路径 `operator/operator-syntax-aligned-formal-ir-planning.md`；Evidence `ev-p060-formal-ir-solver`, `ev-p060-ir-result-and-nl-failure`
- #11 Card `operator-unified-language-memory-action-policy`；路径 `operator/operator-unified-language-memory-action-policy.md`；Evidence `ev-p062-unified-memory-action-policy`, `ev-p062-broadcast-advantage`
- #12 Card `operator-stagewise-mcp-cost-attribution`；路径 `operator/operator-stagewise-mcp-cost-attribution.md`；Evidence `ev-p070-six-stage-attribution`, `ev-p070-light-tool-runtime-boundary`, `ev-p070-orchestration-bottleneck`
- #13 Card `operator-hierarchical-utterance-critic-token-actor`；路径 `operator/operator-hierarchical-utterance-critic-token-actor.md`；Evidence `ev-p077-hierarchical-utterance-critic-token-actor`, `ev-p077-trajectory-only-sample-efficiency`, `ev-p077-oracle-reward-hacking-boundary`
- #14 Card `operator-cascaded-multiagent-meta-routing`；路径 `operator/operator-cascaded-multiagent-meta-routing.md`；Evidence `ev-p023-operator-core`, `ev-p023-cascaded-routing-core`
- #15 Card `operator-milestone-dag-trajectory-evaluation`；路径 `operator/operator-milestone-dag-trajectory-evaluation.md`；Evidence `ev-p037-evaluation-core`, `ev-p037-minefield-violation`
- #16 Card `operator-hidden-state-tool-necessity-prefill`；路径 `operator/operator-hidden-state-tool-necessity-prefill.md`；Evidence `ev-p041-operator-core`, `ev-p041-probe-prefill-steering`
- #17 Card `operator-hypothetical-tool-query-expansion`；路径 `operator/operator-hypothetical-tool-query-expansion.md`；Evidence `ev-p089-training-gold-count-hypothetical-tools`, `ev-p089-overview-alignment-rrf`, `ev-p089-hungarian-alignment`, `ev-p089-forced-alignment-proxy`, `ev-p089-retrieval-only-metrics`, `ev-p089-api-latency-boundary`
- #18 Card `operator-transition-decomposed-agent-training`；路径 `operator/operator-transition-decomposed-agent-training.md`；Evidence `ev-p026-transition-decomposition`, `ev-p026-uniform-terminal-return`
- #19 Card `operator-capability-preserving-agent-safety-evaluation`；路径 `operator/operator-capability-preserving-agent-safety-evaluation.md`；Evidence `ev-p067-capability-preserving-safety`, `ev-p067-agentic-harm-not-chat-refusal`
- #20 Card `operator-active-counterexample-verifier`；路径 `operator/operator-active-counterexample-verifier.md`；Evidence `ev-p050-operator-core`

## q002 · failure

- 原始查询：`semantically related tools distractors missing prerequisite output dependency tool retrieval`
- 规范化查询：`"semantically" OR "related" OR "tools" OR "distractors" OR "missing" OR "prerequisite" OR "output" OR "dependency" OR "tool" OR "retrieval"`

### 路线 `failure_card_fts`

- 命中数：20
- 降级：false（无）

- #1 Card `failure-semantically-related-toolkit-expansion`；路径 `failure/failure-semantically-related-toolkit-expansion.md`；Evidence `ev-p084-expanded-toolkit-controlled-setting`, `ev-p084-related-toolkit-error-types`, `ev-p084-expanded-toolkit-table`, `ev-p084-generated-tool-single-dataset-boundary`
- #2 Card `failure-incomplete-tool-contracts-false-verified-state`；路径 `failure/failure-incomplete-tool-contracts-false-verified-state.md`；Evidence `ev-p074-contract-state-commit`, `ev-p074-missing-schema-true-postcondition`
- #3 Card `failure-multi-agent-adversarial-coordination-spans-trust-surfaces`；路径 `failure/failure-multi-agent-adversarial-coordination-spans-trust-surfaces.md`；Evidence `ev-p083-three-surface-adversarial-failure`, `ev-p083-lightweight-defense-failure`, `ev-p083-simulated-tool-boundary`
- #4 Card `failure-single-execution-denotation-false-positive`；路径 `failure/failure-single-execution-denotation-false-positive.md`；Evidence `ev-p101-metric-distortion`, `ev-p101-esm-fn-rate`
- #5 Card `failure-generic-or-unvalidated-tool-libraries-add-distractors`；路径 `failure/failure-generic-or-unvalidated-tool-libraries-add-distractors.md`；Evidence `ev-p078-validated-tool-creation-retrieval`, `ev-p078-multiview-tool-retrieval`, `ev-p078-generic-tool-and-baseline-boundary`, `ev-p078-toolset-construction-cost`, `ev-p078-baseline-fairness-boundary`
- #6 Card `failure-forced-hypothetical-tool-alignment`；路径 `failure/failure-forced-hypothetical-tool-alignment.md`；Evidence `ev-p089-training-gold-count-hypothetical-tools`, `ev-p089-hungarian-alignment`, `ev-p089-forced-alignment-proxy`, `ev-p089-retrieval-only-metrics`
- #7 Card `failure-tool-description-and-order-bias`；路径 `failure/failure-tool-description-and-order-bias.md`；Evidence `ev-p069-description-induced-preference`, `ev-p069-identical-tool-order-bias`
- #8 Card `failure-memory-unit-granularity-mismatch`；路径 `failure/failure-memory-unit-granularity-mismatch.md`；Evidence `ev-p011-failure-core`
- #9 Card `failure-solver-feasibility-near-zero-information-proxy`；路径 `failure/failure-solver-feasibility-near-zero-information-proxy.md`；Evidence `ev-p097-feasibility-gap`, `ev-p097-behavioral-perturbation`
- #10 Card `failure-dense-retriever-surface-bias-collapse`；路径 `failure/failure-dense-retriever-surface-bias-collapse.md`；Evidence `ev-p093-foil-collapse`, `ev-p093-poison-rag`, `ev-p093-paired-protocol`
- #11 Card `failure-free-form-clarification-no-stop-value`；路径 `failure/failure-free-form-clarification-no-stop-value.md`；Evidence `ev-p072-structured-clarification-gate`, `ev-p072-unstructured-clarification-failure`, `ev-p072-compute-boundary`
- #12 Card `failure-natural-language-ir-hurts-formal-planning`；路径 `failure/failure-natural-language-ir-hurts-formal-planning.md`；Evidence `ev-p060-formal-ir-solver`, `ev-p060-ir-result-and-nl-failure`
- #13 Card `failure-large-corpus-tool-retrieval-breaks-oracle-menu`；路径 `failure/failure-large-corpus-tool-retrieval-breaks-oracle-menu.md`；Evidence `ev-p085-large-corpus-scale`, `ev-p085-retrieval-completeness-failure`, `ev-p085-non-exhaustive-label`
- #14 Card `failure-cosine-cannot-separate-contradiction-from-duplicate`；路径 `failure/failure-cosine-cannot-separate-contradiction-from-duplicate.md`；Evidence `ev-p091-cosine-auroc`, `ev-p091-retain-fabrication`
- #15 Card `failure-grounded-formalization-output-expansion`；路径 `failure/failure-grounded-formalization-output-expansion.md`；Evidence `ev-p053-higher-order-generator`, `ev-p053-pattern-review-confound`, `ev-p053-parser-evaluation-boundary`
- #16 Card `failure-llm-judge-misses-executable-spec-errors`；路径 `failure/failure-llm-judge-misses-executable-spec-errors.md`；Evidence `ev-p099-judge-miss`, `ev-p099-soundness-necessity`
- #17 Card `failure-solver-guarantee-stops-at-formalization`；路径 `failure/failure-solver-guarantee-stops-at-formalization.md`；Evidence `ev-p051-solver-guarantee-boundary`, `ev-p051-omitted-constraint-failure`, `ev-p052-implicit-constraint-failure`, `ev-p052-self-diagnosis-nontermination`, `ev-p052-direct-code-smt-baselines`
- #18 Card `failure-iterative-refinement-corrupts-correct-output`；路径 `failure/failure-iterative-refinement-corrupts-correct-output.md`；Evidence `ev-p033-operator-core`, `ev-p034-failure-core`
- #19 Card `failure-fixed-shortlist-depth-masks-hard-query-zero`；路径 `failure/failure-fixed-shortlist-depth-masks-hard-query-zero.md`；Evidence `ev-p100-fixed-depth-buckets`, `ev-p100-weak-scorer-collapse`
- #20 Card `failure-retrieved-memory-laundered-through-actions`；路径 `failure/failure-retrieved-memory-laundered-through-actions.md`；Evidence `ev-p075-retrieve-to-action-leakage`, `ev-p075-measured-memory-extraction`, `ev-p075-session-isolation-boundary`

### 路线 `passage_hybrid`

- 命中数：20
- 降级：false（无）

- #1 Passage `P087:p0003:s0002`；Paper `P087`；页 3-3
- #2 Passage `P086:p0006:s0001`；Paper `P086`；页 6-6
- #3 Passage `P100:p0010:s0001`；Paper `P100`；页 10-10
- #4 Passage `P100:p0003:s0002`；Paper `P100`；页 3-3
- #5 Passage `P078:p0002:s0001`；Paper `P078`；页 2-2
- #6 Passage `P086:p0008:s0001`；Paper `P086`；页 8-8
- #7 Passage `P037:p0006:s0001`；Paper `P037`；页 6-6
- #8 Passage `P089:p0002:s0002`；Paper `P089`；页 2-2
- #9 Passage `P086:p0007:s0001`；Paper `P086`；页 7-7
- #10 Passage `P085:p0002:s0001`；Paper `P085`；页 2-2
- #11 Passage `P084:p0002:s0001`；Paper `P084`；页 2-2
- #12 Passage `P085:p0009:s0001`；Paper `P085`；页 9-9
- #13 Passage `P037:p0007:s0001`；Paper `P037`；页 7-7
- #14 Passage `P085:p0002:s0002`；Paper `P085`；页 2-2
- #15 Passage `P089:p0003:s0001`；Paper `P089`；页 3-3
- #16 Passage `P089:p0006:s0002`；Paper `P089`；页 6-6
- #17 Passage `P078:p0009:s0004`；Paper `P078`；页 9-9
- #18 Passage `P006:p0004:s0002`；Paper `P006`；页 4-4
- #19 Passage `P092:p0007:s0001`；Paper `P092`；页 7-7
- #20 Passage `P100:p0006:s0001`；Paper `P100`；页 6-6

### 路线 `operator_card_fts`

- 命中数：20
- 降级：false（无）

- #1 Card `operator-bilevel-graph-toolchain-planning`；路径 `operator/operator-bilevel-graph-toolchain-planning.md`；Evidence `ev-p048-operator-core`
- #2 Card `operator-validated-specialized-tool-creation-retrieval`；路径 `operator/operator-validated-specialized-tool-creation-retrieval.md`；Evidence `ev-p078-validated-tool-creation-retrieval`, `ev-p078-multiview-tool-retrieval`, `ev-p078-generic-tool-and-baseline-boundary`, `ev-p078-toolset-construction-cost`, `ev-p078-baseline-fairness-boundary`
- #3 Card `operator-contract-gated-tool-state-commit`；路径 `operator/operator-contract-gated-tool-state-commit.md`；Evidence `ev-p074-contract-state-commit`, `ev-p074-missing-schema-true-postcondition`
- #4 Card `operator-required-parameter-description-tool-retrieval`；路径 `operator/operator-required-parameter-description-tool-retrieval.md`；Evidence `ev-p086-hypothesize-retrieve-invoke`, `ev-p086-required-parameter-score`, `ev-p086-near-identical-distribution`
- #5 Card `operator-milestone-dag-trajectory-evaluation`；路径 `operator/operator-milestone-dag-trajectory-evaluation.md`；Evidence `ev-p037-evaluation-core`, `ev-p037-minefield-violation`
- #6 Card `operator-write-side-state-adjudication`；路径 `operator/operator-write-side-state-adjudication.md`；Evidence `ev-p030-failure-core`, `ev-p030-write-side-adjudication`, `ev-p030-authorized-readout`
- #7 Card `operator-grouped-masked-history-step-credit`；路径 `operator/operator-grouped-masked-history-step-credit.md`；Evidence `ev-p025-failure-core`, `ev-p025-grouped-step-influence`
- #8 Card `operator-hidden-state-tool-necessity-prefill`；路径 `operator/operator-hidden-state-tool-necessity-prefill.md`；Evidence `ev-p041-operator-core`, `ev-p041-probe-prefill-steering`
- #9 Card `operator-hypothetical-tool-query-expansion`；路径 `operator/operator-hypothetical-tool-query-expansion.md`；Evidence `ev-p089-training-gold-count-hypothetical-tools`, `ev-p089-overview-alignment-rrf`, `ev-p089-hungarian-alignment`, `ev-p089-forced-alignment-proxy`, `ev-p089-retrieval-only-metrics`, `ev-p089-api-latency-boundary`
- #10 Card `operator-tool-grounded-critique`；路径 `operator/operator-tool-grounded-critique.md`；Evidence `ev-p032-operator-core`
- #11 Card `operator-grounded-structured-tool-document-expansion`；路径 `operator/operator-grounded-structured-tool-document-expansion.md`；Evidence `ev-p087-structured-query-independent-expansion`, `ev-p087-merge-and-semantic-judge`, `ev-p087-fields-not-universally-beneficial`
- #12 Card `operator-smt-preexecution-policy-guard`；路径 `operator/operator-smt-preexecution-policy-guard.md`；Evidence `ev-p046-operator-core`
- #13 Card `operator-outcome-trained-execution-state-planner`；路径 `operator/operator-outcome-trained-execution-state-planner.md`；Evidence `ev-p021-operator-core`
- #14 Card `operator-bounded-preexecution-reviewer`；路径 `operator/operator-bounded-preexecution-reviewer.md`；Evidence `ev-p049-operator-core`, `ev-p049-bounded-review-loop`
- #15 Card `operator-cascaded-multiagent-meta-routing`；路径 `operator/operator-cascaded-multiagent-meta-routing.md`；Evidence `ev-p023-operator-core`, `ev-p023-cascaded-routing-core`
- #16 Card `operator-behavioral-perturbation-existence-test`；路径 `operator/operator-behavioral-perturbation-existence-test.md`；Evidence `ev-p097-behavioral-perturbation`, `ev-p097-feasibility-gap`
- #17 Card `operator-transition-decomposed-agent-training`；路径 `operator/operator-transition-decomposed-agent-training.md`；Evidence `ev-p026-transition-decomposition`, `ev-p026-uniform-terminal-return`
- #18 Card `operator-active-counterexample-verifier`；路径 `operator/operator-active-counterexample-verifier.md`；Evidence `ev-p050-operator-core`
- #19 Card `operator-verified-single-branch-repair`；路径 `operator/operator-verified-single-branch-repair.md`；Evidence `ev-p027-operator-core`
- #20 Card `operator-higher-order-message-exposure`；路径 `operator/operator-higher-order-message-exposure.md`；Evidence `ev-p022-operator-core`

### 路线 `paper_card_fts`

- 命中数：20
- 降级：false（无）

- #1 Card `paper-p084`；路径 `paper/paper-p084.md`；Evidence `ev-p084-expanded-toolkit-controlled-setting`, `ev-p084-related-toolkit-error-types`, `ev-p084-expanded-toolkit-table`, `ev-p084-generated-tool-single-dataset-boundary`
- #2 Card `paper-llmcompiler`；路径 `paper/paper-llmcompiler.md`；Evidence `ev-p006-dependency-dag-dispatch`, `ev-p006-token-cost-accounting`, `ev-p006-shared-prompt-comparison-boundary`
- #3 Card `paper-p087`；路径 `paper/paper-p087.md`；Evidence `ev-p087-structured-query-independent-expansion`, `ev-p087-merge-and-semantic-judge`, `ev-p087-fields-not-universally-beneficial`
- #4 Card `paper-p074`；路径 `paper/paper-p074.md`；Evidence `ev-p074-contract-state-commit`, `ev-p074-missing-schema-true-postcondition`
- #5 Card `paper-p066`；路径 `paper/paper-p066.md`；Evidence `ev-p066-single-to-stateful-gap`, `ev-p066-multiturn-state-evaluation`
- #6 Card `paper-p048`；路径 `paper/paper-p048.md`；Evidence `ev-p048-operator-core`
- #7 Card `paper-p100`；路径 `paper/paper-p100.md`；Evidence `ev-p100-fixed-depth-buckets`, `ev-p100-bor-self-pruning`, `ev-p100-weak-scorer-collapse`
- #8 Card `paper-p082`；路径 `paper/paper-p082.md`；Evidence `ev-p082-future-token-loss-filtered-calls`, `ev-p082-top-k-single-call-boundary`, `ev-p082-chaining-cost-sparsity-boundary`
- #9 Card `paper-p041`；路径 `paper/paper-p041.md`；Evidence `ev-p041-operator-core`
- #10 Card `paper-p035`；路径 `paper/paper-p035.md`；Evidence `ev-p035-evaluation-core`
- #11 Card `paper-p089`；路径 `paper/paper-p089.md`；Evidence `ev-p089-training-gold-count-hypothetical-tools`, `ev-p089-overview-alignment-rrf`, `ev-p089-hungarian-alignment`, `ev-p089-forced-alignment-proxy`, `ev-p089-retrieval-only-metrics`, `ev-p089-api-latency-boundary`
- #12 Card `paper-p069`；路径 `paper/paper-p069.md`；Evidence `ev-p069-description-induced-preference`, `ev-p069-identical-tool-order-bias`
- #13 Card `paper-p083`；路径 `paper/paper-p083.md`；Evidence `ev-p083-three-surface-adversarial-failure`, `ev-p083-lightweight-defense-failure`, `ev-p083-simulated-tool-boundary`
- #14 Card `paper-p032`；路径 `paper/paper-p032.md`；Evidence `ev-p032-operator-core`
- #15 Card `paper-p038`；路径 `paper/paper-p038.md`；Evidence `ev-p038-operator-core`
- #16 Card `paper-p085`；路径 `paper/paper-p085.md`；Evidence `ev-p085-large-corpus-scale`, `ev-p085-retrieval-completeness-failure`, `ev-p085-non-exhaustive-label`
- #17 Card `paper-p086`；路径 `paper/paper-p086.md`；Evidence `ev-p086-hypothesize-retrieve-invoke`, `ev-p086-required-parameter-score`, `ev-p086-near-identical-distribution`
- #18 Card `paper-p047`；路径 `paper/paper-p047.md`；Evidence `ev-p047-evaluation-core`
- #19 Card `paper-p051`；路径 `paper/paper-p051.md`；Evidence `ev-p051-formalization-pipeline`, `ev-p051-solver-guarantee-boundary`, `ev-p051-omitted-constraint-failure`, `ev-p051-cost-boundary`
- #20 Card `paper-p097`；路径 `paper/paper-p097.md`；Evidence `ev-p097-feasibility-gap`, `ev-p097-behavioral-perturbation`

## q003 · operator

- 原始查询：`tool graph retrieval residual coverage dependency closure query reformulation`
- 规范化查询：`"tool" OR "graph" OR "retrieval" OR "residual" OR "coverage" OR "dependency" OR "closure" OR "query" OR "reformulation"`

### 路线 `operator_card_fts`

- 命中数：20
- 降级：false（无）

- #1 Card `operator-bilevel-graph-toolchain-planning`；路径 `operator/operator-bilevel-graph-toolchain-planning.md`；Evidence `ev-p048-operator-core`
- #2 Card `operator-joint-nonnegative-residual-retrieval`；路径 `operator/operator-joint-nonnegative-residual-retrieval.md`；Evidence `ev-p088-joint-nonnegative-objective`, `ev-p088-relevant-set-size-signature`, `ev-p088-theory-deployment-scale-boundary`
- #3 Card `operator-entropy-routed-multi-granularity-retrieval`；路径 `operator/operator-entropy-routed-multi-granularity-retrieval.md`；Evidence `ev-p090-entropy-router`, `ev-p090-association-graph`
- #4 Card `operator-cascaded-multiagent-meta-routing`；路径 `operator/operator-cascaded-multiagent-meta-routing.md`；Evidence `ev-p023-operator-core`, `ev-p023-cascaded-routing-core`
- #5 Card `operator-utility-optimized-agent-graph`；路径 `operator/operator-utility-optimized-agent-graph.md`；Evidence `ev-p056-graph-optimization`, `ev-p056-same-set-crosswords`
- #6 Card `operator-dynamic-linked-memory-evolution`；路径 `operator/operator-dynamic-linked-memory-evolution.md`；Evidence `ev-p063-dynamic-link-generation`, `ev-p063-neighbor-rewrite-action`, `ev-p063-retrieval-k-varies`
- #7 Card `operator-hypothetical-tool-query-expansion`；路径 `operator/operator-hypothetical-tool-query-expansion.md`；Evidence `ev-p089-training-gold-count-hypothetical-tools`, `ev-p089-overview-alignment-rrf`, `ev-p089-hungarian-alignment`, `ev-p089-forced-alignment-proxy`, `ev-p089-retrieval-only-metrics`, `ev-p089-api-latency-boundary`
- #8 Card `operator-grounded-structured-tool-document-expansion`；路径 `operator/operator-grounded-structured-tool-document-expansion.md`；Evidence `ev-p087-structured-query-independent-expansion`, `ev-p087-merge-and-semantic-judge`, `ev-p087-fields-not-universally-beneficial`
- #9 Card `operator-required-parameter-description-tool-retrieval`；路径 `operator/operator-required-parameter-description-tool-retrieval.md`；Evidence `ev-p086-hypothesize-retrieve-invoke`, `ev-p086-required-parameter-score`, `ev-p086-near-identical-distribution`
- #10 Card `operator-higher-order-message-exposure`；路径 `operator/operator-higher-order-message-exposure.md`；Evidence `ev-p022-operator-core`
- #11 Card `operator-write-side-state-adjudication`；路径 `operator/operator-write-side-state-adjudication.md`；Evidence `ev-p030-failure-core`, `ev-p030-write-side-adjudication`, `ev-p030-authorized-readout`
- #12 Card `operator-anchor-state-relative-credit`；路径 `operator/operator-anchor-state-relative-credit.md`；Evidence `ev-p065-anchor-state-credit`, `ev-p065-state-recurrence-boundary`, `ev-p026-uniform-terminal-return`
- #13 Card `operator-archive-conditioned-agent-code-search`；路径 `operator/operator-archive-conditioned-agent-code-search.md`；Evidence `ev-p057-archive-code-search`, `ev-p057-search-evaluation-budget`
- #14 Card `operator-neighbor-distilled-test-suites`；路径 `operator/operator-neighbor-distilled-test-suites.md`；Evidence `ev-p101-neighbor-distillation`, `ev-p101-esm-fn-rate`
- #15 Card `operator-chance-corrected-depth-reward`；路径 `operator/operator-chance-corrected-depth-reward.md`；Evidence `ev-p100-bor-self-pruning`, `ev-p100-fixed-depth-buckets`
- #16 Card `operator-adaptive-plan-template-reuse`；路径 `operator/operator-adaptive-plan-template-reuse.md`；Evidence `ev-p071-plan-template-reuse`, `ev-p071-cache-false-positive-boundary`
- #17 Card `operator-memory-stage-decomposition`；路径 `operator/operator-memory-stage-decomposition.md`；Evidence `ev-p010-index-retrieve-read`
- #18 Card `operator-paired-single-factor-bias-decomposition`；路径 `operator/operator-paired-single-factor-bias-decomposition.md`；Evidence `ev-p093-paired-protocol`, `ev-p093-foil-collapse`
- #19 Card `operator-incremental-injection-benchmark-reconstruction`；路径 `operator/operator-incremental-injection-benchmark-reconstruction.md`；Evidence `ev-p094-incremental-protocol`, `ev-p094-sf-guardrails`
- #20 Card `operator-labeled-probe-injection-dual-verifier`；路径 `operator/operator-labeled-probe-injection-dual-verifier.md`；Evidence `ev-p098-constraint-injection`, `ev-p098-nonbinding-blindness`, `ev-p098-diff-leak-550`

### 路线 `paper_card_fts`

- 命中数：20
- 降级：false（无）

- #1 Card `paper-p048`；路径 `paper/paper-p048.md`；Evidence `ev-p048-operator-core`
- #2 Card `paper-p088`；路径 `paper/paper-p088.md`；Evidence `ev-p088-joint-nonnegative-objective`, `ev-p088-relevant-set-size-signature`, `ev-p088-theory-deployment-scale-boundary`
- #3 Card `paper-llmcompiler`；路径 `paper/paper-llmcompiler.md`；Evidence `ev-p006-dependency-dag-dispatch`, `ev-p006-token-cost-accounting`, `ev-p006-shared-prompt-comparison-boundary`
- #4 Card `paper-p016`；路径 `paper/paper-p016.md`；Evidence `ev-p016-mast-taxonomy`, `ev-p016-intervention-residual-failures`
- #5 Card `paper-p056`；路径 `paper/paper-p056.md`；Evidence `ev-p056-graph-optimization`, `ev-p056-same-set-crosswords`, `ev-p056-dylan-cost-quality`
- #6 Card `paper-p101`；路径 `paper/paper-p101.md`；Evidence `ev-p101-metric-distortion`, `ev-p101-neighbor-distillation`, `ev-p101-esm-fn-rate`
- #7 Card `paper-p090`；路径 `paper/paper-p090.md`；Evidence `ev-p090-fixed-granularity-selection`, `ev-p090-entropy-router`, `ev-p090-association-graph`
- #8 Card `paper-p089`；路径 `paper/paper-p089.md`；Evidence `ev-p089-training-gold-count-hypothetical-tools`, `ev-p089-overview-alignment-rrf`, `ev-p089-hungarian-alignment`, `ev-p089-forced-alignment-proxy`, `ev-p089-retrieval-only-metrics`, `ev-p089-api-latency-boundary`
- #9 Card `paper-p087`；路径 `paper/paper-p087.md`；Evidence `ev-p087-structured-query-independent-expansion`, `ev-p087-merge-and-semantic-judge`, `ev-p087-fields-not-universally-beneficial`
- #10 Card `paper-p085`；路径 `paper/paper-p085.md`；Evidence `ev-p085-large-corpus-scale`, `ev-p085-retrieval-completeness-failure`, `ev-p085-non-exhaustive-label`
- #11 Card `paper-p084`；路径 `paper/paper-p084.md`；Evidence `ev-p084-expanded-toolkit-controlled-setting`, `ev-p084-related-toolkit-error-types`, `ev-p084-expanded-toolkit-table`, `ev-p084-generated-tool-single-dataset-boundary`
- #12 Card `paper-p042`；路径 `paper/paper-p042.md`；Evidence `ev-p042-evaluation-core`
- #13 Card `paper-p063`；路径 `paper/paper-p063.md`；Evidence `ev-p063-dynamic-link-generation`, `ev-p063-retrieval-k-varies`, `ev-p063-neighbor-rewrite-action`
- #14 Card `paper-p057`；路径 `paper/paper-p057.md`；Evidence `ev-p057-archive-code-search`, `ev-p057-search-evaluation-budget`
- #15 Card `paper-p071`；路径 `paper/paper-p071.md`；Evidence `ev-p071-plan-template-reuse`, `ev-p071-cache-false-positive-boundary`
- #16 Card `paper-p075`；路径 `paper/paper-p075.md`；Evidence `ev-p075-retrieve-to-action-leakage`, `ev-p075-measured-memory-extraction`, `ev-p075-session-isolation-boundary`
- #17 Card `paper-p064`；路径 `paper/paper-p064.md`；Evidence `ev-p064-experience-following-error`, `ev-p064-evaluator-reliability`
- #18 Card `paper-p023`；路径 `paper/paper-p023.md`；Evidence `ev-p023-operator-core`
- #19 Card `paper-p039`；路径 `paper/paper-p039.md`；Evidence `ev-p039-failure-core`
- #20 Card `paper-p078`；路径 `paper/paper-p078.md`；Evidence `ev-p078-validated-tool-creation-retrieval`, `ev-p078-multiview-tool-retrieval`, `ev-p078-generic-tool-and-baseline-boundary`, `ev-p078-toolset-construction-cost`, `ev-p078-baseline-fairness-boundary`

### 路线 `passage_hybrid`

- 命中数：20
- 降级：false（无）

- #1 Passage `P089:p0003:s0001`；Paper `P089`；页 3-3
- #2 Passage `P100:p0009:s0004`；Paper `P100`；页 9-9
- #3 Passage `P088:p0016:s0001`；Paper `P088`；页 16-16
- #4 Passage `P089:p0002:s0001`；Paper `P089`；页 2-2
- #5 Passage `P089:p0006:s0002`；Paper `P089`；页 6-6
- #6 Passage `P048:p0012:s0001`；Paper `P048`；页 12-12
- #7 Passage `P048:p0004:s0001`；Paper `P048`；页 4-4
- #8 Passage `P087:p0014:s0001`；Paper `P087`；页 14-14
- #9 Passage `P087:p0003:s0002`；Paper `P087`；页 3-3
- #10 Passage `P100:p0006:s0001`；Paper `P100`；页 6-6
- #11 Passage `P078:p0022:s0001`；Paper `P078`；页 22-22
- #12 Passage `P048:p0032:s0001`；Paper `P048`；页 32-32
- #13 Passage `P030:p0025:s0001`；Paper `P030`；页 25-25
- #14 Passage `P048:p0008:s0003`；Paper `P048`；页 8-8
- #15 Passage `P048:p0003:s0004`；Paper `P048`；页 3-3
- #16 Passage `P048:p0014:s0001`；Paper `P048`；页 14-14
- #17 Passage `P085:p0002:s0001`；Paper `P085`；页 2-2
- #18 Passage `P074:p0016:s0001`；Paper `P074`；页 16-16
- #19 Passage `P089:p0002:s0002`；Paper `P089`；页 2-2
- #20 Passage `P036:p0013:s0001`；Paper `P036`；页 13-13

### 路线 `failure_card_fts`

- 命中数：20
- 降级：false（无）

- #1 Card `failure-fixed-shortlist-depth-masks-hard-query-zero`；路径 `failure/failure-fixed-shortlist-depth-masks-hard-query-zero.md`；Evidence `ev-p100-fixed-depth-buckets`, `ev-p100-weak-scorer-collapse`
- #2 Card `failure-retrieved-experience-propagates-stored-errors`；路径 `failure/failure-retrieved-experience-propagates-stored-errors.md`；Evidence `ev-p064-experience-following-error`, `ev-p064-evaluator-reliability`
- #3 Card `failure-anchor-state-credit-needs-state-recurrence`；路径 `failure/failure-anchor-state-credit-needs-state-recurrence.md`；Evidence `ev-p065-anchor-state-credit`, `ev-p065-state-recurrence-boundary`
- #4 Card `failure-same-set-agent-graph-evaluation`；路径 `failure/failure-same-set-agent-graph-evaluation.md`；Evidence `ev-p056-graph-optimization`, `ev-p056-same-set-crosswords`
- #5 Card `failure-incomplete-tool-contracts-false-verified-state`；路径 `failure/failure-incomplete-tool-contracts-false-verified-state.md`；Evidence `ev-p074-contract-state-commit`, `ev-p074-missing-schema-true-postcondition`
- #6 Card `failure-cosine-cannot-separate-contradiction-from-duplicate`；路径 `failure/failure-cosine-cannot-separate-contradiction-from-duplicate.md`；Evidence `ev-p091-cosine-auroc`, `ev-p091-retain-fabrication`
- #7 Card `failure-fixed-single-granularity-memory`；路径 `failure/failure-fixed-single-granularity-memory.md`；Evidence `ev-p090-fixed-granularity-selection`, `ev-p090-entropy-router`
- #8 Card `failure-large-corpus-tool-retrieval-breaks-oracle-menu`；路径 `failure/failure-large-corpus-tool-retrieval-breaks-oracle-menu.md`；Evidence `ev-p085-large-corpus-scale`, `ev-p085-retrieval-completeness-failure`, `ev-p085-non-exhaustive-label`
- #9 Card `failure-sparse-topology-suppresses-correct-insight`；路径 `failure/failure-sparse-topology-suppresses-correct-insight.md`；Evidence `ev-p017-failure-core`
- #10 Card `failure-plan-cache-semantic-false-positives`；路径 `failure/failure-plan-cache-semantic-false-positives.md`；Evidence `ev-p071-plan-template-reuse`, `ev-p071-cache-false-positive-boundary`
- #11 Card `failure-constraint-shift-breaks-formalization`；路径 `failure/failure-constraint-shift-breaks-formalization.md`；Evidence `ev-p054-natural-language-implicit-predicate-failure`, `ev-p055-constraint-formalism-taxonomy`, `ev-p055-representative-subset-boundary`, `ev-p055-three-revision-budget`, `ev-p055-constraint-performance-drop`, `ev-p055-plan-correctness-false-positive-boundary`
- #12 Card `failure-long-history-reading-overload`；路径 `failure/failure-long-history-reading-overload.md`；Evidence `ev-p010-long-history-decline`
- #13 Card `failure-retrieved-memory-laundered-through-actions`；路径 `failure/failure-retrieved-memory-laundered-through-actions.md`；Evidence `ev-p075-retrieve-to-action-leakage`, `ev-p075-measured-memory-extraction`, `ev-p075-session-isolation-boundary`
- #14 Card `failure-generator-aligned-verification-passes-shared-misreads`；路径 `failure/failure-generator-aligned-verification-passes-shared-misreads.md`；Evidence `ev-p096-shared-misinterpretation`, `ev-p096-simplification-inversion`
- #15 Card `failure-generic-or-unvalidated-tool-libraries-add-distractors`；路径 `failure/failure-generic-or-unvalidated-tool-libraries-add-distractors.md`；Evidence `ev-p078-validated-tool-creation-retrieval`, `ev-p078-multiview-tool-retrieval`, `ev-p078-generic-tool-and-baseline-boundary`, `ev-p078-toolset-construction-cost`, `ev-p078-baseline-fairness-boundary`
- #16 Card `failure-tool-use-metrics-collapse-distinct-errors`；路径 `failure/failure-tool-use-metrics-collapse-distinct-errors.md`；Evidence `ev-p039-failure-core`, `ev-p039-aggregate-score-masking`
- #17 Card `failure-tool-description-and-order-bias`；路径 `failure/failure-tool-description-and-order-bias.md`；Evidence `ev-p069-description-induced-preference`, `ev-p069-identical-tool-order-bias`
- #18 Card `failure-light-tool-runtime-bottleneck-overreach`；路径 `failure/failure-light-tool-runtime-bottleneck-overreach.md`；Evidence `ev-p070-six-stage-attribution`, `ev-p070-light-tool-runtime-boundary`, `ev-p070-orchestration-bottleneck`
- #19 Card `failure-forced-hypothetical-tool-alignment`；路径 `failure/failure-forced-hypothetical-tool-alignment.md`；Evidence `ev-p089-training-gold-count-hypothetical-tools`, `ev-p089-hungarian-alignment`, `ev-p089-forced-alignment-proxy`, `ev-p089-retrieval-only-metrics`
- #20 Card `failure-semantically-related-toolkit-expansion`；路径 `failure/failure-semantically-related-toolkit-expansion.md`；Evidence `ev-p084-expanded-toolkit-controlled-setting`, `ev-p084-related-toolkit-error-types`, `ev-p084-expanded-toolkit-table`, `ev-p084-generated-tool-single-dataset-boundary`

## q004 · prior

- 原始查询：`large scale tool retrieval toolchain planning LLM agents`
- 规范化查询：`"large" OR "scale" OR "tool" OR "retrieval" OR "toolchain" OR "planning" OR "LLM" OR "agents"`

### 路线 `paper_card_fts`

- 命中数：20
- 降级：false（无）

- #1 Card `paper-p048`；路径 `paper/paper-p048.md`；Evidence `ev-p048-operator-core`
- #2 Card `paper-p085`；路径 `paper/paper-p085.md`；Evidence `ev-p085-large-corpus-scale`, `ev-p085-retrieval-completeness-failure`, `ev-p085-non-exhaustive-label`
- #3 Card `paper-p051`；路径 `paper/paper-p051.md`；Evidence `ev-p051-formalization-pipeline`, `ev-p051-solver-guarantee-boundary`, `ev-p051-omitted-constraint-failure`, `ev-p051-cost-boundary`
- #4 Card `paper-p055`；路径 `paper/paper-p055.md`；Evidence `ev-p055-constraint-formalism-taxonomy`, `ev-p055-representative-subset-boundary`, `ev-p055-three-revision-budget`, `ev-p055-constraint-performance-drop`, `ev-p055-plan-correctness-false-positive-boundary`
- #5 Card `paper-p036`；路径 `paper/paper-p036.md`；Evidence `ev-p036-failure-core`
- #6 Card `paper-p004`；路径 `paper/paper-p004.md`；Evidence `ev-p004-failure-core`
- #7 Card `paper-p046`；路径 `paper/paper-p046.md`；Evidence `ev-p046-operator-core`
- #8 Card `paper-p028`；路径 `paper/paper-p028.md`；Evidence `ev-p028-operator-core`
- #9 Card `paper-p005`；路径 `paper/paper-p005.md`；Evidence `ev-p005-operator-core`
- #10 Card `paper-p086`；路径 `paper/paper-p086.md`；Evidence `ev-p086-hypothesize-retrieve-invoke`, `ev-p086-required-parameter-score`, `ev-p086-near-identical-distribution`
- #11 Card `paper-agent-security-bench`；路径 `paper/paper-agent-security-bench.md`；Evidence `ev-p008-stagewise-attack-surface`, `ev-p008-memory-defense-high-fnr`
- #12 Card `paper-p088`；路径 `paper/paper-p088.md`；Evidence `ev-p088-joint-nonnegative-objective`, `ev-p088-relevant-set-size-signature`, `ev-p088-theory-deployment-scale-boundary`
- #13 Card `paper-p032`；路径 `paper/paper-p032.md`；Evidence `ev-p032-operator-core`
- #14 Card `paper-p038`；路径 `paper/paper-p038.md`；Evidence `ev-p038-operator-core`
- #15 Card `paper-p039`；路径 `paper/paper-p039.md`；Evidence `ev-p039-failure-core`
- #16 Card `paper-p035`；路径 `paper/paper-p035.md`；Evidence `ev-p035-evaluation-core`
- #17 Card `paper-p041`；路径 `paper/paper-p041.md`；Evidence `ev-p041-operator-core`
- #18 Card `paper-p013`；路径 `paper/paper-p013.md`；Evidence `ev-p013-intrinsic-self-correction-degrades`, `ev-p013-oracle-free-equal-budget-boundary`
- #19 Card `paper-p072`；路径 `paper/paper-p072.md`；Evidence `ev-p072-structured-clarification-gate`, `ev-p072-unstructured-clarification-failure`, `ev-p072-compute-boundary`
- #20 Card `paper-p073`；路径 `paper/paper-p073.md`；Evidence `ev-p073-execution-supervised-probe`, `ev-p073-internal-confidence-misalignment`

### 路线 `operator_card_fts`

- 命中数：20
- 降级：false（无）

- #1 Card `operator-bilevel-graph-toolchain-planning`；路径 `operator/operator-bilevel-graph-toolchain-planning.md`；Evidence `ev-p048-operator-core`
- #2 Card `operator-joint-nonnegative-residual-retrieval`；路径 `operator/operator-joint-nonnegative-residual-retrieval.md`；Evidence `ev-p088-joint-nonnegative-objective`, `ev-p088-relevant-set-size-signature`, `ev-p088-theory-deployment-scale-boundary`
- #3 Card `operator-bounded-preexecution-reviewer`；路径 `operator/operator-bounded-preexecution-reviewer.md`；Evidence `ev-p049-operator-core`, `ev-p049-bounded-review-loop`
- #4 Card `operator-syntax-aligned-formal-ir-planning`；路径 `operator/operator-syntax-aligned-formal-ir-planning.md`；Evidence `ev-p060-formal-ir-solver`, `ev-p060-ir-result-and-nl-failure`
- #5 Card `operator-cascaded-multiagent-meta-routing`；路径 `operator/operator-cascaded-multiagent-meta-routing.md`；Evidence `ev-p023-operator-core`, `ev-p023-cascaded-routing-core`
- #6 Card `operator-smt-preexecution-policy-guard`；路径 `operator/operator-smt-preexecution-policy-guard.md`；Evidence `ev-p046-operator-core`
- #7 Card `operator-outcome-trained-execution-state-planner`；路径 `operator/operator-outcome-trained-execution-state-planner.md`；Evidence `ev-p021-operator-core`
- #8 Card `operator-transition-decomposed-agent-training`；路径 `operator/operator-transition-decomposed-agent-training.md`；Evidence `ev-p026-transition-decomposition`, `ev-p026-uniform-terminal-return`
- #9 Card `operator-decomposed-solver-backed-formal-planning`；路径 `operator/operator-decomposed-solver-backed-formal-planning.md`；Evidence `ev-p051-formalization-pipeline`, `ev-p051-solver-guarantee-boundary`, `ev-p051-cost-boundary`, `ev-p052-decomposed-formalization`, `ev-p052-result-self-assessment`, `ev-p052-self-assessment-loop-limit`, `ev-p052-fixed-cross-task-examples`, `ev-p052-direct-code-smt-baselines`
- #10 Card `operator-stagewise-mcp-cost-attribution`；路径 `operator/operator-stagewise-mcp-cost-attribution.md`；Evidence `ev-p070-six-stage-attribution`, `ev-p070-light-tool-runtime-boundary`, `ev-p070-orchestration-bottleneck`
- #11 Card `operator-reason-action-interleaving`；路径 `operator/operator-reason-action-interleaving.md`；Evidence `ev-p001-react-interleaved`
- #12 Card `operator-hidden-state-tool-necessity-prefill`；路径 `operator/operator-hidden-state-tool-necessity-prefill.md`；Evidence `ev-p041-operator-core`, `ev-p041-probe-prefill-steering`
- #13 Card `operator-adaptive-plan-template-reuse`；路径 `operator/operator-adaptive-plan-template-reuse.md`；Evidence `ev-p071-plan-template-reuse`, `ev-p071-cache-false-positive-boundary`
- #14 Card `operator-action-preserving-observation-contextualization`；路径 `operator/operator-action-preserving-observation-contextualization.md`；Evidence `ev-p079-action-conditioned-contextualization`, `ev-p079-ground-truth-action-retry`, `ev-p079-unseen-ui-boundary`
- #15 Card `operator-hypothetical-tool-query-expansion`；路径 `operator/operator-hypothetical-tool-query-expansion.md`；Evidence `ev-p089-training-gold-count-hypothetical-tools`, `ev-p089-overview-alignment-rrf`, `ev-p089-hungarian-alignment`, `ev-p089-forced-alignment-proxy`, `ev-p089-retrieval-only-metrics`, `ev-p089-api-latency-boundary`
- #16 Card `operator-required-parameter-description-tool-retrieval`；路径 `operator/operator-required-parameter-description-tool-retrieval.md`；Evidence `ev-p086-hypothesize-retrieve-invoke`, `ev-p086-required-parameter-score`, `ev-p086-near-identical-distribution`
- #17 Card `operator-feedback-backpropagated-tree-search`；路径 `operator/operator-feedback-backpropagated-tree-search.md`；Evidence `ev-p003-search-control-loop`
- #18 Card `operator-agreement-prior-modulation`；路径 `operator/operator-agreement-prior-modulation.md`；Evidence `ev-p015-agreement-prior`
- #19 Card `operator-execution-supervised-prompt-trace-calibration`；路径 `operator/operator-execution-supervised-prompt-trace-calibration.md`；Evidence `ev-p073-execution-supervised-probe`, `ev-p073-internal-confidence-misalignment`
- #20 Card `operator-solver-simplification-query-verification`；路径 `operator/operator-solver-simplification-query-verification.md`；Evidence `ev-p096-simplification-inversion`, `ev-p096-shared-misinterpretation`

### 路线 `failure_card_fts`

- 命中数：20
- 降级：false（无）

- #1 Card `failure-large-corpus-tool-retrieval-breaks-oracle-menu`；路径 `failure/failure-large-corpus-tool-retrieval-breaks-oracle-menu.md`；Evidence `ev-p085-large-corpus-scale`, `ev-p085-retrieval-completeness-failure`, `ev-p085-non-exhaustive-label`
- #2 Card `failure-constraint-shift-breaks-formalization`；路径 `failure/failure-constraint-shift-breaks-formalization.md`；Evidence `ev-p054-natural-language-implicit-predicate-failure`, `ev-p055-constraint-formalism-taxonomy`, `ev-p055-representative-subset-boundary`, `ev-p055-three-revision-budget`, `ev-p055-constraint-performance-drop`, `ev-p055-plan-correctness-false-positive-boundary`
- #3 Card `failure-constrained-plan-surface-validity`；路径 `failure/failure-constrained-plan-surface-validity.md`；Evidence `ev-p004-failure-core`, `ev-p004-macro-constraint-failure`
- #4 Card `failure-multi-agent-adversarial-coordination-spans-trust-surfaces`；路径 `failure/failure-multi-agent-adversarial-coordination-spans-trust-surfaces.md`；Evidence `ev-p083-three-surface-adversarial-failure`, `ev-p083-lightweight-defense-failure`, `ev-p083-simulated-tool-boundary`
- #5 Card `failure-natural-language-ir-hurts-formal-planning`；路径 `failure/failure-natural-language-ir-hurts-formal-planning.md`；Evidence `ev-p060-formal-ir-solver`, `ev-p060-ir-result-and-nl-failure`
- #6 Card `failure-light-tool-runtime-bottleneck-overreach`；路径 `failure/failure-light-tool-runtime-bottleneck-overreach.md`；Evidence `ev-p070-six-stage-attribution`, `ev-p070-light-tool-runtime-boundary`, `ev-p070-orchestration-bottleneck`
- #7 Card `failure-repeat-run-reliability-collapse`；路径 `failure/failure-repeat-run-reliability-collapse.md`；Evidence `ev-p007-repeat-reliability-collapse`
- #8 Card `failure-grounded-formalization-output-expansion`；路径 `failure/failure-grounded-formalization-output-expansion.md`；Evidence `ev-p053-higher-order-generator`, `ev-p053-pattern-review-confound`, `ev-p053-parser-evaluation-boundary`
- #9 Card `failure-gold-context-does-not-solve-knowledge-use`；路径 `failure/failure-gold-context-does-not-solve-knowledge-use.md`；Evidence `ev-p036-failure-core`
- #10 Card `failure-raw-observation-overload-hides-action-relevant-ui`；路径 `failure/failure-raw-observation-overload-hides-action-relevant-ui.md`；Evidence `ev-p079-action-conditioned-contextualization`, `ev-p079-ground-truth-action-retry`, `ev-p079-unseen-ui-boundary`
- #11 Card `failure-confident-completion-without-state-success`；路径 `failure/failure-confident-completion-without-state-success.md`；Evidence `ev-p040-failure-core`
- #12 Card `failure-plan-cache-semantic-false-positives`；路径 `failure/failure-plan-cache-semantic-false-positives.md`；Evidence `ev-p071-plan-template-reuse`, `ev-p071-cache-false-positive-boundary`
- #13 Card `failure-internal-tool-confidence-not-execution-success`；路径 `failure/failure-internal-tool-confidence-not-execution-success.md`；Evidence `ev-p073-execution-supervised-probe`, `ev-p073-internal-confidence-misalignment`
- #14 Card `failure-debate-cost-nondominance`；路径 `failure/failure-debate-cost-nondominance.md`；Evidence `ev-p015-debate-cost-nondominance`
- #15 Card `failure-semantically-related-toolkit-expansion`；路径 `failure/failure-semantically-related-toolkit-expansion.md`；Evidence `ev-p084-expanded-toolkit-controlled-setting`, `ev-p084-related-toolkit-error-types`, `ev-p084-expanded-toolkit-table`, `ev-p084-generated-tool-single-dataset-boundary`
- #16 Card `failure-lazy-agent-effective-single-agent-collapse`；路径 `failure/failure-lazy-agent-effective-single-agent-collapse.md`；Evidence `ev-p025-failure-core`
- #17 Card `failure-llm-judge-misses-executable-spec-errors`；路径 `failure/failure-llm-judge-misses-executable-spec-errors.md`；Evidence `ev-p099-judge-miss`, `ev-p099-soundness-necessity`
- #18 Card `failure-generator-aligned-verification-passes-shared-misreads`；路径 `failure/failure-generator-aligned-verification-passes-shared-misreads.md`；Evidence `ev-p096-shared-misinterpretation`, `ev-p096-simplification-inversion`
- #19 Card `failure-memory-defense-high-fnr`；路径 `failure/failure-memory-defense-high-fnr.md`；Evidence `ev-p008-memory-defense-high-fnr`
- #20 Card `failure-llm-freshness-judgment-prior-override-and-drift`；路径 `failure/failure-llm-freshness-judgment-prior-override-and-drift.md`；Evidence `ev-p095-prior-override-drift`, `ev-p095-matched-comparison`

### 路线 `passage_hybrid`

- 命中数：20
- 降级：false（无）

- #1 Passage `P048:p0001:s0002`；Paper `P048`；页 1-1
- #2 Passage `P048:p0002:s0001`；Paper `P048`；页 2-2
- #3 Passage `P048:p0014:s0001`；Paper `P048`；页 14-14
- #4 Passage `P087:p0009:s0003`；Paper `P087`；页 9-9
- #5 Passage `P074:p0015:s0001`；Paper `P074`；页 15-15
- #6 Passage `P074:p0014:s0001`；Paper `P074`；页 14-14
- #7 Passage `P085:p0001:s0003`；Paper `P085`；页 1-1
- #8 Passage `P085:p0002:s0001`；Paper `P085`；页 2-2
- #9 Passage `P048:p0001:s0003`；Paper `P048`；页 1-1
- #10 Passage `P041:p0001:s0001`；Paper `P041`；页 1-1
- #11 Passage `P051:p0012:s0001`；Paper `P051`；页 12-12
- #12 Passage `P048:p0002:s0002`；Paper `P048`；页 2-2
- #13 Passage `P059:p0002:s0001`；Paper `P059`；页 2-2
- #14 Passage `P085:p0001:s0002`；Paper `P085`；页 1-1
- #15 Passage `P085:p0003:s0001`；Paper `P085`；页 3-3
- #16 Passage `P078:p0001:s0001`；Paper `P078`；页 1-1
- #17 Passage `P087:p0012:s0001`；Paper `P087`；页 12-12
- #18 Passage `P085:p0013:s0001`；Paper `P085`；页 13-13
- #19 Passage `P085:p0008:s0001`；Paper `P085`；页 8-8
- #20 Passage `P048:p0003:s0004`；Paper `P048`；页 3-3

## q005 · measurement

- 原始查询：`tool retrieval recall chain completion distractor robustness end task success`
- 规范化查询：`"tool" OR "retrieval" OR "recall" OR "chain" OR "completion" OR "distractor" OR "robustness" OR "end" OR "task" OR "success"`

### 路线 `paper_card_fts`

- 命中数：20
- 降级：false（无）

- #1 Card `paper-p040`；路径 `paper/paper-p040.md`；Evidence `ev-p040-failure-core`
- #2 Card `paper-p031`；路径 `paper/paper-p031.md`；Evidence `ev-p031-evaluation-core`
- #3 Card `paper-p084`；路径 `paper/paper-p084.md`；Evidence `ev-p084-expanded-toolkit-controlled-setting`, `ev-p084-related-toolkit-error-types`, `ev-p084-expanded-toolkit-table`, `ev-p084-generated-tool-single-dataset-boundary`
- #4 Card `paper-p081`；路径 `paper/paper-p081.md`；Evidence `ev-p081-independent-path-majority-aggregation`, `ev-p081-forty-sample-baseline`, `ev-p081-fixed-answer-space-boundary`
- #5 Card `paper-p078`；路径 `paper/paper-p078.md`；Evidence `ev-p078-validated-tool-creation-retrieval`, `ev-p078-multiview-tool-retrieval`, `ev-p078-generic-tool-and-baseline-boundary`, `ev-p078-toolset-construction-cost`, `ev-p078-baseline-fairness-boundary`
- #6 Card `paper-p100`；路径 `paper/paper-p100.md`；Evidence `ev-p100-fixed-depth-buckets`, `ev-p100-bor-self-pruning`, `ev-p100-weak-scorer-collapse`
- #7 Card `paper-expel`；路径 `paper/paper-expel.md`；Evidence `ev-p018-insight-update-operations`, `ev-p018-raw-reflection-contamination`
- #8 Card `paper-p055`；路径 `paper/paper-p055.md`；Evidence `ev-p055-constraint-formalism-taxonomy`, `ev-p055-representative-subset-boundary`, `ev-p055-three-revision-budget`, `ev-p055-constraint-performance-drop`, `ev-p055-plan-correctness-false-positive-boundary`
- #9 Card `paper-p087`；路径 `paper/paper-p087.md`；Evidence `ev-p087-structured-query-independent-expansion`, `ev-p087-merge-and-semantic-judge`, `ev-p087-fields-not-universally-beneficial`
- #10 Card `paper-p039`；路径 `paper/paper-p039.md`；Evidence `ev-p039-failure-core`
- #11 Card `paper-p085`；路径 `paper/paper-p085.md`；Evidence `ev-p085-large-corpus-scale`, `ev-p085-retrieval-completeness-failure`, `ev-p085-non-exhaustive-label`
- #12 Card `paper-p097`；路径 `paper/paper-p097.md`；Evidence `ev-p097-feasibility-gap`, `ev-p097-behavioral-perturbation`
- #13 Card `paper-p004`；路径 `paper/paper-p004.md`；Evidence `ev-p004-failure-core`
- #14 Card `paper-p030`；路径 `paper/paper-p030.md`；Evidence `ev-p030-failure-core`
- #15 Card `paper-p090`；路径 `paper/paper-p090.md`；Evidence `ev-p090-fixed-granularity-selection`, `ev-p090-entropy-router`, `ev-p090-association-graph`
- #16 Card `paper-react`；路径 `paper/paper-react.md`；Evidence `ev-p001-react-interleaved`, `ev-p001-search-hallucination-boundary`
- #17 Card `paper-p038`；路径 `paper/paper-p038.md`；Evidence `ev-p038-operator-core`
- #18 Card `paper-p082`；路径 `paper/paper-p082.md`；Evidence `ev-p082-future-token-loss-filtered-calls`, `ev-p082-top-k-single-call-boundary`, `ev-p082-chaining-cost-sparsity-boundary`
- #19 Card `paper-p032`；路径 `paper/paper-p032.md`；Evidence `ev-p032-operator-core`
- #20 Card `paper-p067`；路径 `paper/paper-p067.md`；Evidence `ev-p067-capability-preserving-safety`, `ev-p067-agentic-harm-not-chat-refusal`

### 路线 `passage_hybrid`

- 命中数：20
- 降级：false（无）

- #1 Passage `P036:p0023:s0001`；Paper `P036`；页 23-23
- #2 Passage `P092:p0023:s0001`；Paper `P092`；页 23-23
- #3 Passage `P085:p0001:s0003`；Paper `P085`；页 1-1
- #4 Passage `P085:p0001:s0002`；Paper `P085`；页 1-1
- #5 Passage `P085:p0002:s0001`；Paper `P085`；页 2-2
- #6 Passage `P092:p0022:s0001`；Paper `P092`；页 22-22
- #7 Passage `P029:p0017:s0001`；Paper `P029`；页 17-17
- #8 Passage `P100:p0003:s0002`；Paper `P100`；页 3-3
- #9 Passage `P036:p0027:s0001`；Paper `P036`；页 27-27
- #10 Passage `P036:p0008:s0001`；Paper `P036`；页 8-8
- #11 Passage `P010:p0010:s0001`；Paper `P010`；页 10-10
- #12 Passage `P062:p0018:s0001`；Paper `P062`；页 18-18
- #13 Passage `P087:p0009:s0004`；Paper `P087`；页 9-9
- #14 Passage `P090:p0007:s0002`；Paper `P090`；页 7-7
- #15 Passage `P018:p0007:s0002`；Paper `P018`；页 7-7
- #16 Passage `P094:p0020:s0001`；Paper `P094`；页 20-20
- #17 Passage `P092:p0006:s0001`；Paper `P092`；页 6-6
- #18 Passage `P010:p0002:s0001`；Paper `P010`；页 2-2
- #19 Passage `P048:p0016:s0001`；Paper `P048`；页 16-16
- #20 Passage `P048:p0025:s0001`；Paper `P048`；页 25-25

### 路线 `failure_card_fts`

- 命中数：20
- 降级：false（无）

- #1 Card `failure-confident-completion-without-state-success`；路径 `failure/failure-confident-completion-without-state-success.md`；Evidence `ev-p040-failure-core`
- #2 Card `failure-large-corpus-tool-retrieval-breaks-oracle-menu`；路径 `failure/failure-large-corpus-tool-retrieval-breaks-oracle-menu.md`；Evidence `ev-p085-large-corpus-scale`, `ev-p085-retrieval-completeness-failure`, `ev-p085-non-exhaustive-label`
- #3 Card `failure-generic-or-unvalidated-tool-libraries-add-distractors`；路径 `failure/failure-generic-or-unvalidated-tool-libraries-add-distractors.md`；Evidence `ev-p078-validated-tool-creation-retrieval`, `ev-p078-multiview-tool-retrieval`, `ev-p078-generic-tool-and-baseline-boundary`, `ev-p078-toolset-construction-cost`, `ev-p078-baseline-fairness-boundary`
- #4 Card `failure-likelihood-utility-does-not-guarantee-agent-utility`；路径 `failure/failure-likelihood-utility-does-not-guarantee-agent-utility.md`；Evidence `ev-p082-future-token-loss-filtered-calls`, `ev-p082-top-k-single-call-boundary`, `ev-p082-chaining-cost-sparsity-boundary`
- #5 Card `failure-semantically-related-toolkit-expansion`；路径 `failure/failure-semantically-related-toolkit-expansion.md`；Evidence `ev-p084-expanded-toolkit-controlled-setting`, `ev-p084-related-toolkit-error-types`, `ev-p084-expanded-toolkit-table`, `ev-p084-generated-tool-single-dataset-boundary`
- #6 Card `failure-tool-use-metrics-collapse-distinct-errors`；路径 `failure/failure-tool-use-metrics-collapse-distinct-errors.md`；Evidence `ev-p039-failure-core`, `ev-p039-aggregate-score-masking`
- #7 Card `failure-constraint-shift-breaks-formalization`；路径 `failure/failure-constraint-shift-breaks-formalization.md`；Evidence `ev-p054-natural-language-implicit-predicate-failure`, `ev-p055-constraint-formalism-taxonomy`, `ev-p055-representative-subset-boundary`, `ev-p055-three-revision-budget`, `ev-p055-constraint-performance-drop`, `ev-p055-plan-correctness-false-positive-boundary`
- #8 Card `failure-internal-tool-confidence-not-execution-success`；路径 `failure/failure-internal-tool-confidence-not-execution-success.md`；Evidence `ev-p073-execution-supervised-probe`, `ev-p073-internal-confidence-misalignment`
- #9 Card `failure-fixed-single-granularity-memory`；路径 `failure/failure-fixed-single-granularity-memory.md`；Evidence `ev-p090-fixed-granularity-selection`, `ev-p090-entropy-router`
- #10 Card `failure-natural-language-ir-hurts-formal-planning`；路径 `failure/failure-natural-language-ir-hurts-formal-planning.md`；Evidence `ev-p060-formal-ir-solver`, `ev-p060-ir-result-and-nl-failure`
- #11 Card `failure-repeat-run-reliability-collapse`；路径 `failure/failure-repeat-run-reliability-collapse.md`；Evidence `ev-p007-repeat-reliability-collapse`
- #12 Card `failure-raw-observation-overload-hides-action-relevant-ui`；路径 `failure/failure-raw-observation-overload-hides-action-relevant-ui.md`；Evidence `ev-p079-action-conditioned-contextualization`, `ev-p079-ground-truth-action-retry`, `ev-p079-unseen-ui-boundary`
- #13 Card `failure-retrieved-experience-propagates-stored-errors`；路径 `failure/failure-retrieved-experience-propagates-stored-errors.md`；Evidence `ev-p064-experience-following-error`, `ev-p064-evaluator-reliability`
- #14 Card `failure-retrieved-update-lacks-decision-authority`；路径 `failure/failure-retrieved-update-lacks-decision-authority.md`；Evidence `ev-p030-failure-core`, `ev-p030-recognition-application-gap`
- #15 Card `failure-gold-context-does-not-solve-knowledge-use`；路径 `failure/failure-gold-context-does-not-solve-knowledge-use.md`；Evidence `ev-p036-failure-core`
- #16 Card `failure-grounded-formalization-output-expansion`；路径 `failure/failure-grounded-formalization-output-expansion.md`；Evidence `ev-p053-higher-order-generator`, `ev-p053-pattern-review-confound`, `ev-p053-parser-evaluation-boundary`
- #17 Card `failure-unified-memory-policy-retains-terminal-credit-smearing`；路径 `failure/failure-unified-memory-policy-retains-terminal-credit-smearing.md`；Evidence `ev-p062-unified-memory-action-policy`, `ev-p062-broadcast-advantage`
- #18 Card `failure-memory-unit-granularity-mismatch`；路径 `failure/failure-memory-unit-granularity-mismatch.md`；Evidence `ev-p011-failure-core`
- #19 Card `failure-lazy-agent-effective-single-agent-collapse`；路径 `failure/failure-lazy-agent-effective-single-agent-collapse.md`；Evidence `ev-p025-failure-core`
- #20 Card `failure-tool-description-and-order-bias`；路径 `failure/failure-tool-description-and-order-bias.md`；Evidence `ev-p069-description-induced-preference`, `ev-p069-identical-tool-order-bias`

### 路线 `operator_card_fts`

- 命中数：20
- 降级：false（无）

- #1 Card `operator-execution-supervised-prompt-trace-calibration`；路径 `operator/operator-execution-supervised-prompt-trace-calibration.md`；Evidence `ev-p073-execution-supervised-probe`, `ev-p073-internal-confidence-misalignment`
- #2 Card `operator-bilevel-graph-toolchain-planning`；路径 `operator/operator-bilevel-graph-toolchain-planning.md`；Evidence `ev-p048-operator-core`
- #3 Card `operator-terminal-state-reliability-evaluation`；路径 `operator/operator-terminal-state-reliability-evaluation.md`；Evidence `ev-p007-terminal-state-evaluation`
- #4 Card `operator-validated-specialized-tool-creation-retrieval`；路径 `operator/operator-validated-specialized-tool-creation-retrieval.md`；Evidence `ev-p078-validated-tool-creation-retrieval`, `ev-p078-multiview-tool-retrieval`, `ev-p078-generic-tool-and-baseline-boundary`, `ev-p078-toolset-construction-cost`, `ev-p078-baseline-fairness-boundary`
- #5 Card `operator-capability-preserving-agent-safety-evaluation`；路径 `operator/operator-capability-preserving-agent-safety-evaluation.md`；Evidence `ev-p067-capability-preserving-safety`, `ev-p067-agentic-harm-not-chat-refusal`
- #6 Card `operator-thought-tree-search`；路径 `operator/operator-thought-tree-search.md`；Evidence `ev-p002-branch-evaluate-search`
- #7 Card `operator-smt-preexecution-policy-guard`；路径 `operator/operator-smt-preexecution-policy-guard.md`；Evidence `ev-p046-operator-core`
- #8 Card `operator-stagewise-agent-security-audit`；路径 `operator/operator-stagewise-agent-security-audit.md`；Evidence `ev-p008-stagewise-attack-surface`
- #9 Card `operator-future-token-loss-filtered-tool-learning`；路径 `operator/operator-future-token-loss-filtered-tool-learning.md`；Evidence `ev-p082-future-token-loss-filtered-calls`, `ev-p082-top-k-single-call-boundary`, `ev-p082-chaining-cost-sparsity-boundary`
- #10 Card `operator-hidden-state-tool-necessity-prefill`；路径 `operator/operator-hidden-state-tool-necessity-prefill.md`；Evidence `ev-p041-operator-core`, `ev-p041-probe-prefill-steering`
- #11 Card `operator-tool-grounded-critique`；路径 `operator/operator-tool-grounded-critique.md`；Evidence `ev-p032-operator-core`
- #12 Card `operator-decomposed-research-evidence-evaluation`；路径 `operator/operator-decomposed-research-evidence-evaluation.md`；Evidence `ev-p042-evaluation-core`, `ev-p043-evaluation-core`, `ev-p044-evaluation-core`
- #13 Card `operator-write-side-state-adjudication`；路径 `operator/operator-write-side-state-adjudication.md`；Evidence `ev-p030-failure-core`, `ev-p030-write-side-adjudication`, `ev-p030-authorized-readout`
- #14 Card `operator-unified-language-memory-action-policy`；路径 `operator/operator-unified-language-memory-action-policy.md`；Evidence `ev-p062-unified-memory-action-policy`, `ev-p062-broadcast-advantage`
- #15 Card `operator-experience-insight-update`；路径 `operator/operator-experience-insight-update.md`；Evidence `ev-p018-insight-update-operations`
- #16 Card `operator-outcome-trained-execution-state-planner`；路径 `operator/operator-outcome-trained-execution-state-planner.md`；Evidence `ev-p021-operator-core`
- #17 Card `operator-bounded-preexecution-reviewer`；路径 `operator/operator-bounded-preexecution-reviewer.md`；Evidence `ev-p049-operator-core`, `ev-p049-bounded-review-loop`
- #18 Card `operator-verified-single-branch-repair`；路径 `operator/operator-verified-single-branch-repair.md`；Evidence `ev-p027-operator-core`
- #19 Card `operator-subtask-compute-allocation`；路径 `operator/operator-subtask-compute-allocation.md`；Evidence `ev-p020-compute-allocation-search`
- #20 Card `operator-trace-failure-taxonomy`；路径 `operator/operator-trace-failure-taxonomy.md`；Evidence `ev-p016-mast-taxonomy`

## 紧凑研究地图

> 按 Paper 去重；注意力权重只反映用途路线顺序和机械噪声标记，不是相关性或科研结论。

- Paper `P001`；用途 measurement, prior；观测 2（重复 1）；最佳导航路线 `q005:paper_card_fts`；噪声标记：无
- Paper `P004`；用途 measurement, prior, problem；观测 6（重复 5）；最佳导航路线 `q004:paper_card_fts`；噪声标记：无
- Paper `P005`；用途 prior, problem；观测 2（重复 1）；最佳导航路线 `q001:paper_card_fts`；噪声标记：无
- Paper `P008`；用途 measurement, prior；观测 3（重复 2）；最佳导航路线 `q004:paper_card_fts`；噪声标记：无
- Paper `P010`；用途 measurement, operator；观测 4（重复 3）；最佳导航路线 `q003:operator_card_fts`；噪声标记：无
- Paper `P011`；用途 failure, measurement；观测 2（重复 1）；最佳导航路线 `q002:failure_card_fts`；噪声标记：无
- Paper `P013`；用途 prior, problem；观测 2（重复 1）；最佳导航路线 `q001:paper_card_fts`；噪声标记：无
- Paper `P014`；用途 problem；观测 1（重复 0）；最佳导航路线 `q001:paper_card_fts`；噪声标记：无
- Paper `P018`；用途 measurement；观测 3（重复 2）；最佳导航路线 `q005:paper_card_fts`；噪声标记：无
- Paper `P022`；用途 failure, operator；观测 2（重复 1）；最佳导航路线 `q003:operator_card_fts`；噪声标记：无
- Paper `P023`；用途 failure, operator, prior, problem；观测 5（重复 4）；最佳导航路线 `q003:operator_card_fts`；噪声标记：无
- Paper `P026`；用途 failure, operator, prior, problem；观测 4（重复 3）；最佳导航路线 `q003:operator_card_fts`；噪声标记：无
- Paper `P028`；用途 prior, problem；观测 2（重复 1）；最佳导航路线 `q001:paper_card_fts`；噪声标记：无
- Paper `P030`；用途 failure, measurement, operator；观测 6（重复 5）；最佳导航路线 `q003:operator_card_fts`；噪声标记：无
- Paper `P031`；用途 measurement；观测 1（重复 0）；最佳导航路线 `q005:paper_card_fts`；噪声标记：无
- Paper `P032`；用途 failure, measurement, prior, problem；观测 6（重复 5）；最佳导航路线 `q001:paper_card_fts`；噪声标记：无
- Paper `P033`；用途 failure；观测 1（重复 0）；最佳导航路线 `q002:failure_card_fts`；噪声标记：无
- Paper `P034`；用途 failure；观测 1（重复 0）；最佳导航路线 `q002:failure_card_fts`；噪声标记：无
- Paper `P035`；用途 failure, prior；观测 2（重复 1）；最佳导航路线 `q004:paper_card_fts`；噪声标记：无
- Paper `P036`；用途 measurement, operator, prior, problem；观测 9（重复 8）；最佳导航路线 `q004:paper_card_fts`；噪声标记：无
- Paper `P038`；用途 failure, measurement, prior；观测 3（重复 2）；最佳导航路线 `q004:paper_card_fts`；噪声标记：无
- Paper `P039`；用途 measurement, operator, prior；观测 5（重复 4）；最佳导航路线 `q005:paper_card_fts`；噪声标记：无
- Paper `P040`；用途 measurement, prior, problem；观测 4（重复 3）；最佳导航路线 `q005:paper_card_fts`；噪声标记：无
- Paper `P041`；用途 failure, measurement, prior, problem；观测 7（重复 6）；最佳导航路线 `q004:paper_card_fts`；噪声标记：无
- Paper `P046`；用途 failure, measurement, prior, problem；观测 6（重复 5）；最佳导航路线 `q004:paper_card_fts`；噪声标记：无
- Paper `P048`；用途 failure, measurement, operator, prior, problem；观测 23（重复 22）；最佳导航路线 `q003:operator_card_fts`；噪声标记：无
- Paper `P049`；用途 failure, measurement, prior, problem；观测 4（重复 3）；最佳导航路线 `q001:paper_card_fts`；噪声标记：无
- Paper `P051`；用途 failure, prior, problem；观测 6（重复 5）；最佳导航路线 `q004:paper_card_fts`；噪声标记：无
- Paper `P052`；用途 failure, prior；观测 2（重复 1）；最佳导航路线 `q002:failure_card_fts`；噪声标记：无
- Paper `P053`；用途 failure, measurement, prior；观测 3（重复 2）；最佳导航路线 `q002:failure_card_fts`；噪声标记：无
- Paper `P055`；用途 measurement, operator, prior；观测 5（重复 4）；最佳导航路线 `q004:paper_card_fts`；噪声标记：无
- Paper `P056`；用途 operator, problem；观测 4（重复 3）；最佳导航路线 `q003:operator_card_fts`；噪声标记：无
- Paper `P057`；用途 operator；观测 2（重复 1）；最佳导航路线 `q003:operator_card_fts`；噪声标记：无
- Paper `P060`；用途 failure, measurement, prior, problem；观测 6（重复 5）；最佳导航路线 `q002:failure_card_fts`；噪声标记：无
- Paper `P063`；用途 operator, problem；观测 3（重复 2）；最佳导航路线 `q003:operator_card_fts`；噪声标记：无
- Paper `P065`；用途 operator；观测 2（重复 1）；最佳导航路线 `q003:operator_card_fts`；噪声标记：无
- Paper `P067`；用途 measurement, problem；观测 3（重复 2）；最佳导航路线 `q005:paper_card_fts`；噪声标记：无
- Paper `P069`；用途 failure, measurement, operator；观测 4（重复 3）；最佳导航路线 `q002:failure_card_fts`；噪声标记：无
- Paper `P071`；用途 operator, prior；观测 5（重复 4）；最佳导航路线 `q003:operator_card_fts`；噪声标记：无
- Paper `P072`；用途 failure, prior, problem；观测 3（重复 2）；最佳导航路线 `q002:failure_card_fts`；噪声标记：无
- Paper `P073`；用途 measurement, prior, problem；观测 6（重复 5）；最佳导航路线 `q001:paper_card_fts`；噪声标记：无
- Paper `P074`；用途 failure, operator, prior, problem；观测 9（重复 8）；最佳导航路线 `q002:failure_card_fts`；噪声标记：无
- Paper `P075`；用途 failure, operator；观测 3（重复 2）；最佳导航路线 `q002:failure_card_fts`；噪声标记：无
- Paper `P077`；用途 problem；观测 2（重复 1）；最佳导航路线 `q001:paper_card_fts`；噪声标记：无
- Paper `P078`；用途 failure, measurement, operator, prior, problem；观测 14（重复 13）；最佳导航路线 `q001:paper_card_fts`；噪声标记：无
- Paper `P081`；用途 measurement, problem；观测 4（重复 3）；最佳导航路线 `q001:paper_card_fts`；噪声标记：无
- Paper `P082`；用途 failure, measurement, problem；观测 6（重复 5）；最佳导航路线 `q005:paper_card_fts`；噪声标记：无
- Paper `P083`；用途 failure, prior, problem；观测 4（重复 3）；最佳导航路线 `q002:failure_card_fts`；噪声标记：无
- Paper `P084`；用途 failure, measurement, operator, prior, problem；观测 10（重复 9）；最佳导航路线 `q002:failure_card_fts`；噪声标记：无
- Paper `P085`；用途 failure, measurement, operator, prior, problem；观测 30（重复 29）；最佳导航路线 `q001:paper_card_fts`；噪声标记：无
- Paper `P086`；用途 failure, operator, prior, problem；观测 12（重复 11）；最佳导航路线 `q001:paper_card_fts`；噪声标记：无
- Paper `P087`；用途 failure, measurement, operator, prior, problem；观测 16（重复 15）；最佳导航路线 `q003:operator_card_fts`；噪声标记：无
- Paper `P088`；用途 operator, prior；观测 5（重复 4）；最佳导航路线 `q003:operator_card_fts`；噪声标记：无
- Paper `P089`；用途 failure, operator, prior, problem；观测 17（重复 16）；最佳导航路线 `q002:failure_card_fts`；噪声标记：无
- Paper `P090`；用途 measurement, operator, problem；观测 8（重复 7）；最佳导航路线 `q003:operator_card_fts`；噪声标记：无
- Paper `P091`；用途 failure, operator；观测 2（重复 1）；最佳导航路线 `q002:failure_card_fts`；噪声标记：无
- Paper `P093`；用途 failure, operator；观测 2（重复 1）；最佳导航路线 `q002:failure_card_fts`；噪声标记：无
- Paper `P094`；用途 measurement, operator；观测 2（重复 1）；最佳导航路线 `q003:operator_card_fts`；噪声标记：无
- Paper `P097`；用途 failure, measurement；观测 4（重复 3）；最佳导航路线 `q002:failure_card_fts`；噪声标记：无
- Paper `P098`；用途 operator；观测 1（重复 0）；最佳导航路线 `q003:operator_card_fts`；噪声标记：无
- Paper `P099`；用途 failure, prior；观测 2（重复 1）；最佳导航路线 `q002:failure_card_fts`；噪声标记：无
- Paper `P100`；用途 failure, measurement, operator, problem；观测 12（重复 11）；最佳导航路线 `q005:paper_card_fts`；噪声标记：无
- Paper `P101`；用途 failure, operator；观测 3（重复 2）；最佳导航路线 `q002:failure_card_fts`；噪声标记：无
- Paper `P003`；用途 prior；观测 1（重复 0）；最佳导航路线 `q004:operator_card_fts`；噪声标记：无
- Paper `P006`；用途 failure, operator；观测 3（重复 2）；最佳导航路线 `q003:paper_card_fts`；噪声标记：无
- Paper `P015`；用途 prior, problem；观测 4（重复 3）；最佳导航路线 `q001:failure_card_fts`；噪声标记：无
- Paper `P016`；用途 measurement, operator；观测 2（重复 1）；最佳导航路线 `q003:paper_card_fts`；噪声标记：无
- Paper `P017`；用途 operator, problem；观测 2（重复 1）；最佳导航路线 `q001:failure_card_fts`；噪声标记：无
- Paper `P021`；用途 failure, measurement, prior；观测 3（重复 2）；最佳导航路线 `q004:operator_card_fts`；噪声标记：无
- Paper `P025`；用途 failure, measurement, prior, problem；观测 4（重复 3）；最佳导航路线 `q001:failure_card_fts`；噪声标记：无
- Paper `P029`；用途 measurement；观测 1（重复 0）；最佳导航路线 `q005:passage_hybrid`；噪声标记：无
- Paper `P037`；用途 failure, problem；观测 4（重复 3）；最佳导航路线 `q002:passage_hybrid`；噪声标记：无
- Paper `P042`；用途 measurement, operator；观测 2（重复 1）；最佳导航路线 `q003:paper_card_fts`；噪声标记：无
- Paper `P062`；用途 measurement, problem；观测 5（重复 4）；最佳导航路线 `q005:passage_hybrid`；噪声标记：无
- Paper `P064`；用途 measurement, operator；观测 3（重复 2）；最佳导航路线 `q003:paper_card_fts`；噪声标记：无
- Paper `P066`；用途 failure, problem；观测 2（重复 1）；最佳导航路线 `q001:failure_card_fts`；噪声标记：无
- Paper `P070`；用途 operator, prior, problem；观测 4（重复 3）；最佳导航路线 `q004:operator_card_fts`；噪声标记：无
- Paper `P076`；用途 problem；观测 1（重复 0）；最佳导航路线 `q001:failure_card_fts`；噪声标记：无
- Paper `P079`；用途 measurement, prior, problem；观测 4（重复 3）；最佳导航路线 `q004:operator_card_fts`；噪声标记：无
- Paper `P092`；用途 failure, measurement；观测 4（重复 3）；最佳导航路线 `q005:passage_hybrid`；噪声标记：无
- Paper `P096`；用途 operator, prior；观测 3（重复 2）；最佳导航路线 `q004:operator_card_fts`；噪声标记：无
- Paper `P007`；用途 measurement, prior；观测 3（重复 2）；最佳导航路线 `q004:failure_card_fts`；噪声标记：无
- Paper `P027`；用途 failure, measurement；观测 2（重复 1）；最佳导航路线 `q002:operator_card_fts`；噪声标记：无
- Paper `P050`；用途 failure, problem；观测 2（重复 1）；最佳导航路线 `q002:operator_card_fts`；噪声标记：无
- Paper `P054`；用途 measurement, operator, prior；观测 3（重复 2）；最佳导航路线 `q004:failure_card_fts`；噪声标记：无
- Paper `P095`；用途 prior, problem；观测 2（重复 1）；最佳导航路线 `q001:passage_hybrid`；噪声标记：无
- Paper `P002`；用途 measurement, problem；观测 2（重复 1）；最佳导航路线 `q001:operator_card_fts`；噪声标记：无
- Paper `P020`；用途 measurement；观测 1（重复 0）；最佳导航路线 `q005:operator_card_fts`；噪声标记：无
- Paper `P043`；用途 measurement；观测 1（重复 0）；最佳导航路线 `q005:operator_card_fts`；噪声标记：无
- Paper `P044`；用途 measurement；观测 1（重复 0）；最佳导航路线 `q005:operator_card_fts`；噪声标记：无
- Paper `P047`；用途 failure；观测 1（重复 0）；最佳导航路线 `q002:paper_card_fts`；噪声标记：无
- Paper `P059`；用途 prior；观测 1（重复 0）；最佳导航路线 `q004:passage_hybrid`；噪声标记：无

## 覆盖诊断

- 去重 Card：156
- 去重 Evidence：195
- 去重 Passage：77
- 命中 Paper：92
- 原始观测：400
- 带机械噪声标记的观测：0
