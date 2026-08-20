# P075 Reconciliation

- Disposition: `ACCEPTED_AS_BOUNDED_NEGATIVE_KNOWLEDGE`
- Read 1 SHA-256: `f78cfab4d092743ae13b78255743ecec597ecea1ff5521e7bb22e782e284e816`
- Accepted read-2: `read_2_attempts/r2-20260720-p075-a1/`
- Final invocation SHA-256: `3c39c34acb22f35d0b04b63437f1b3db612cc082048e787393527d30a4395408`
- Read-2 report SHA-256: `a4322ebaf8adfbf4ff8d772f7b8c1f679f64215110f7a067ba1aeb3285faee9f`
- Other attempts: none; no read-3 required.

## Provenance note

The independent reader consumed the pre-completion invocation whose SHA is recorded inside its report. After completion, Codex corrected an accidentally future-dated snapshot field and filled reader/report metadata. The exact request and Frozen prompt bytes were not changed; the final invocation SHA above is the post-completion record.

## Source reconciliation

- `AGREE`: the demonstrated failure is not direct database access. A black-box query simultaneously shapes the top-k retrieval neighbourhood and induces the Agent to emit retrieved demonstrations through an output channel already valid for its workflow.
- `NARROWED`: the evidence covers static, shared, top-k demonstration memories without session isolation, primarily in two research Agents using GPT-4o. It does not establish the same exposure in access-controlled production memory or all memory architectures.
- `NARROWED`: the advanced-attacker condition is given the real scoring-function family; the paper does not implement its claimed black-box inference. Retrieval-set-aware RN/CER evaluation also uses an internal evaluator oracle unavailable to an ordinary attacker.
- `BUDGET_BOUNDARY`: each distinct attack prompt may run up to three times, while reported extraction efficiency is normalized by prompt count rather than actual calls, tokens or cost. The Cards must preserve this advantage.
- `NEGATIVE_RETAINED`: weaker backbone, larger retrieval depth and larger memory do not yield monotonic privacy conclusions; lower extraction can reflect low normal task competence, and extra exposure need not become complete output.
- `NO_OPERATOR_ADMISSION`: session isolation, sanitization and output controls are discussion-only defenses. This source freezes one Failure, not a validated positive Operator, and CRL retains no operational attack strings or private examples.

## Frozen source role

Failure: Retrieved Long-Term Memory Can Be Laundered Through Allowed Actions. Its reusable research value is to force future memory implements to test ownership/session boundaries, retrieval exposure and the final action channel together, under matched call and task-competence budgets.
