# PLAN_05 Card source audit F invocation

- Snapshot time: `2026-07-20T03:07:00+08:00`
- Role: independent source-grounding auditor, not research Candidate Reviewer
- Scope: the 42 new Cards listed below, their cited entries in `knowledge_base/corpus/evidence.json`, and only the 16 PDFs referenced by those Card metadata.
- Evidence JSON SHA-256: `092c1f1dd85cc3a6bdd13b37e81dc37443827bd79697085d1004f885230c7496`
- Corpus manifest SHA-256: `c8b7efd4218efe439d08aa757862347811bdfc2c2796359fdb1e12a137a58512`
- Read boundary: procedural blinding; do not read `read_1.md`, any `read_2`, reconciliation, saturation, calibration/blind material, prior audits or CRL Candidate artifacts.
- Write boundary: only `knowledge_base/corpus/card_audits/plan05-audit-f/report.md`.
- Network: forbidden.

## Exact Card allowlist

Paper: `paper-p026.md`, `paper-p056.md`, `paper-p057.md`, `paper-p058.md`, `paper-p059.md`, `paper-p060.md`, `paper-p062.md`, `paper-p063.md`, `paper-p064.md`, `paper-p065.md`, `paper-p066.md`, `paper-p067.md`, `paper-p068.md`, `paper-p069.md`, `paper-p070.md`, `paper-p071.md` under `knowledge_base/cards/paper/`.

Operator: `operator-transition-decomposed-agent-training.md`, `operator-utility-optimized-agent-graph.md`, `operator-archive-conditioned-agent-code-search.md`, `operator-mcts-executable-workflow-refinement.md`, `operator-state-conditioned-agent-activation.md`, `operator-syntax-aligned-formal-ir-planning.md`, `operator-unified-language-memory-action-policy.md`, `operator-dynamic-linked-memory-evolution.md`, `operator-anchor-state-relative-credit.md`, `operator-capability-preserving-agent-safety-evaluation.md`, `operator-evidence-audit-before-score.md`, `operator-stagewise-mcp-cost-attribution.md`, `operator-adaptive-plan-template-reuse.md` under `knowledge_base/cards/operator/`.

Failure: `failure-uniform-terminal-return-erases-step-credit.md`, `failure-same-set-agent-graph-evaluation.md`, `failure-reused-selection-feedback-in-agent-search.md`, `failure-natural-language-ir-hurts-formal-planning.md`, `failure-unified-memory-policy-retains-terminal-credit-smearing.md`, `failure-retrieved-experience-propagates-stored-errors.md`, `failure-anchor-state-credit-needs-state-recurrence.md`, `failure-single-turn-tool-score-overstates-agent-competence.md`, `failure-chatbot-refusal-does-not-establish-agent-safety.md`, `failure-one-shot-expert-gold-is-brittle.md`, `failure-tool-description-and-order-bias.md`, `failure-light-tool-runtime-bottleneck-overreach.md`, `failure-plan-cache-semantic-false-positives.md` under `knowledge_base/cards/failure/`.

## Audit questions

1. Does every `[AUTHOR_FACT]` say no more than its cited Evidence and exact PDF source?
2. Does each Operator state a real changed computation, inputs/outputs/timing and budget boundary?
3. Does each Failure describe an observed fact or explicitly narrow an inference, rather than inventing a universal failure?
4. Are lineage, source-family dependence, user-excluded direction boundaries and experimental confounds stated honestly?
5. Identify only actionable `REJECT`, `REVISE`, or `ACCEPT` findings. Do not score, rank, vote, generate Candidates, or start another audit loop.

The main Codex will make one-pass dispositions. This audit checks source grounding only and is not the three-Reviewer research process.
