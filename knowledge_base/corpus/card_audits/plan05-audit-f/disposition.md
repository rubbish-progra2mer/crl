# PLAN_05 Card Source Audit F — Codex Disposition

## Decision

- Audit report SHA-256: `5746BCE8053C9897C7C6DF5AF208ED681045DC2306FCF09D4CBF71DBF406133B`
- Codex decision: **ACCEPT AFTER ONE-PASS REVISION**
- Scope: source-grounding correction only; this is not a Candidate review or research Reviewer decision.
- Closure rule: apply every localized `REVISE` once, run the existing mechanical Card/Evidence validator, and do not start another full audit loop for these Cards.

## Applied source corrections

1. Corrected all nine Evidence `section` locators listed by the auditor without changing page bounds, passage text, or Passage SHA.
2. Removed ungrounded shorthand such as “二读发现……” where the Card did not carry a direct PDF locator.
3. Corrected P059 from subset/roster selection to one-next-Agent activation.
4. Corrected P060 to the paper's 8/8 Level-2 comparison and four-IR result; removed undeclared P051/P052 lineage.
5. Added P062's training-only expected-answer boundary and retained the same-trajectory advantage broadcast limitation.
6. Corrected P064 from execution similarity to input/query similarity.
7. Corrected P065 to identical environment states, actions, and discounted returns; removed an undeclared named baseline from the Paper Card.
8. Narrowed P067 safety observations to AgentHarm's tested models, tasks, and jailbreak/template conditions.
9. Corrected P068 to disagreement-gated challenger/auditor adjudication rather than immutable-oracle gold.
10. Kept P069 as a selection-instability result and P070 as a light-to-moderate-tool regime result, without importing unsupported arithmetic/provenance claims.

## Final disposition of audit items

- Original `ACCEPT`: 17 retained.
- Original `REVISE`: 25 revised and accepted subject to the existing mechanical validator.
- Original `REJECT`: 0.

No new retrieval component, scoring system, Candidate process, or review hierarchy was introduced.
