# P072 Reconciliation

- Disposition: `ACCEPTED_WITH_NARROWING_TO_SCHEMA_COMPLETENESS_CLARIFICATION_GATE`
- Read 1 SHA-256: `cad28cdc7466195365836e22fd2c51f5f2b2280e9302bcfdf7b5c90e254264db`
- Accepted read-2: `read_2_attempts/r2-20260720-p072-a1/`
- Final invocation SHA-256: `9031d896016393e85797c18c74a17e06b3fe95558eb1021a3a1d4c3af861cdb9`
- Read-2 report SHA-256: `43792e2b8ad87cb8c703f1a8a3811c771b8999bba92a869f4130f6dcb66e6487`
- Other attempts: none; no read-3 required.

## Provenance note

The independent reader consumed the pre-completion invocation whose SHA is recorded inside its report. After completion, Codex corrected an accidentally future-dated snapshot field and filled reader/report metadata. The exact request and Frozen prompt bytes were not changed; the final invocation SHA above is the post-completion record.

## Source reconciliation

- `AGREE`: the reusable computation is a schema-domain completeness score plus LLM-generated question selection, perfect-disambiguation EVPI heuristic, repeated-aspect cost, and ask/execute threshold.
- `NARROWED`: this is not demonstrated Bayesian model uncertainty. The belief assumes independent parameters and the implemented EVPI does not learn a response distribution.
- `NARROWED`: the cost term penalizes repeated aspects, not all user burden; SAGE uses more tokens than simpler prompt baselines even when it asks fewer user questions.
- `NEGATIVE_RETAINED`: ToolCall recall/F1 and log-probability reward evaluation can decline; reward runs report the best of three, not mean/variance.
- `CONFLICT_RETAINED`: dataset totals omit 64 samples, reward equations differ between text and appendix, error recovery is absent from the algorithm return path, and several theoretical claims are not established by the shown proof. Cards must not repeat those guarantees.
- `PROJECT_BOUNDARY`: execution-error recovery is excluded by the user and is not admitted as an Operator.

## Frozen source role

Cost-penalized structured clarification-gate Operator + free-form clarification Failure. Any future implement must match model, schema information, token/call budget, and separately report user questions versus compute cost.
