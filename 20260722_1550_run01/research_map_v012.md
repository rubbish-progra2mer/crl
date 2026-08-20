<!-- crl-v3-evidence-ids
["ev-p040-failure-core","ev-p074-contract-state-commit","ev-p074-missing-schema-true-postcondition","ev-p068-audit-then-score","ev-p068-one-shot-gold-brittle"]
-->
# Research Map v012

## Evidence-backed failure boundary

- `ev-p040-failure-core` supports the failure class in which an agent declares success although the required external state has not been established.
- `ev-p074-contract-state-commit` supports gating completion on explicit state-transition evidence rather than fluent completion text.
- `ev-p074-missing-schema-true-postcondition` supports the observation that a tool contract can omit the true postcondition.
- `ev-p068-audit-then-score` supports separating evidence audit from final score/reward consumption.
- `ev-p068-one-shot-gold-brittle` supports avoiding a brittle single visible success criterion as the only correctness signal.

These sources motivate the target failure. They do not prove that RCED works.

## Nearest empirical and method priors

1. **Cheap Reward Hacking Detection (2026)** is the closest empirical baseline because it reports task-disjoint Terminal Wrench results and separately evaluates a model trained on stripped trajectories. It establishes that action surfaces contain signal, but does not pair each evaluated trajectory with a deterministic same-task successful reference or compute explicit shell-effect deltas.
2. **Praetor (2026)** is the closest structured-monitoring method. It learns sequence and parameter guards from verified benign telemetry. RCED differs by using one task-specific reference, an open-shell parser, and a supervised detector rather than a learned pDFA enforcement boundary. This difference is also a weakness: a single reference can omit legitimate alternative solutions.
3. **TRACE (2026)** is the closest contrastive trajectory-analysis benchmark. It asks an LLM to reason over paired behavior on a synthetic curated set. RCED is a deterministic feature computation evaluated on real Terminal Wrench trajectories.
4. **Terminal Wrench (2026)** supplies the real benchmark and labels. The benchmark itself is not the method contribution.

## Gap

The narrow unresolved gap is whether **one verified successful same-task trace can serve as a task-conditioned control** for action-only detection on open shell workflows, without requiring a fixed workflow grammar or exposing reasoning text.

## Intervention

For reference and evaluated trajectories:

1. extract ordered shell commands;
2. map command segments to executable tokens and coarse effects (`read`, `write`, `delete`, `permission`, `package`, `service`, `network`, `verify`, `other`);
3. extract touched paths and direct-write targets;
4. compute normalized edit distance, missing-reference effects, novel executables, novel paths, novel write paths, verifier-read-to-write indicators, and novel-write-to-verify indicators;
5. concatenate these numeric deltas to the same character TF-IDF command/output representation used by the strongest local comparator;
6. fit the same class-weighted logistic learner.

## Changed-computation claim

The candidate changes the scoring computation through task-conditioned ordered effect/dataflow deltas. It is not:

- a prompt instruction;
- a hidden explanation classifier;
- a change to labels or test composition;
- threshold-only tuning;
- another P084 retrieval adapter;
- a pDFA implementation;
- a claim that all reward hacking is detectable from actions.

## Main scientific risks

- Successful workflows may be legitimately multimodal, so one reference can make alternative solutions appear anomalous.
- Model identity and task source can correlate with labels even under task-disjoint splitting.
- Direct shell parsing is approximate and does not establish true filesystem state.
- Multiple trajectories within a task are correlated; all confidence intervals therefore resample tasks, not rows.
- The public Terminal Wrench label construction may contain judgment noise.
- Task `1012` was inspected during selection and is therefore forced into training rather than used for threshold selection or held-out measurement.

## Decision contract

Development alone decides whether Confirmation may be opened. Confirmation alone cannot repair a failed Development gate. Three-Reviewer review is permitted only after both phases pass and a complete byte-addressed Review Packet is frozen.
