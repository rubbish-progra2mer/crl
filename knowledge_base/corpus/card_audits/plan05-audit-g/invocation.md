# PLAN_05 Card source audit G invocation

- Snapshot time: `2026-07-20T03:57:29+08:00`
- Role: independent source-grounding auditor, not research Candidate Reviewer
- Scope: the 13 A2 Cards listed below, their cited entries in `knowledge_base/corpus/evidence.json`, and only P072–P076 PDFs referenced by those Card metadata.
- Evidence JSON SHA-256: `ddcf22a35a67dd95c9319dec27ca62257e02399febc594dbf8130e9571a82aab`
- Corpus manifest SHA-256: `1692a02d7bc389d64f59f6904375c1e5b67d29a0a50b1c7b8ed60b9dcadc015d`
- Read boundary: procedural blinding; do not read `read_1.md`, any `read_2`, reconciliation, saturation, calibration/blind material, prior audits or CRL Candidate artifacts.
- Write boundary: only `knowledge_base/corpus/card_audits/plan05-audit-g/report.md`.
- Network: forbidden.

## Exact Card allowlist

Paper: `paper-p072.md`, `paper-p073.md`, `paper-p074.md`, `paper-p075.md`, `paper-p076.md` under `knowledge_base/cards/paper/`.

Operator: `operator-cost-penalized-structured-clarification.md`, `operator-execution-supervised-prompt-trace-calibration.md`, `operator-contract-gated-tool-state-commit.md` under `knowledge_base/cards/operator/`.

Failure: `failure-free-form-clarification-no-stop-value.md`, `failure-internal-tool-confidence-not-execution-success.md`, `failure-incomplete-tool-contracts-false-verified-state.md`, `failure-retrieved-memory-laundered-through-actions.md`, `failure-untrusted-agent-metadata-privileged-control-flow.md` under `knowledge_base/cards/failure/`.

## Audit questions

1. Does every `[AUTHOR_FACT]` say no more than its cited Evidence and exact PDF source?
2. Does each Operator state a real changed computation, inputs/outputs/timing and budget/oracle boundary?
3. Does each Failure distinguish observed fact, bounded synthesis and untested repair rather than inventing a universal failure?
4. Do Cards preserve supervision, session ownership, contract-completeness, capability and controlled-lab boundaries?
5. Identify only actionable `REJECT`, `REVISE`, or `ACCEPT` findings. Do not score, rank, vote, generate Candidates, or start another audit loop.

The main Codex will make one-pass dispositions. This audit checks source grounding only and is not the three-Reviewer research process.
