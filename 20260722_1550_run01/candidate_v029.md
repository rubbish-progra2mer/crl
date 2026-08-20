<!-- crl-v3-evidence-ids
["ev-p084-expanded-toolkit-controlled-setting","ev-p084-related-toolkit-error-types","ev-p087-structured-query-independent-expansion","ev-p087-fields-not-universally-beneficial"]
-->
# Candidate v029 — Dual Counterfactual Necessity (DCN)

## Changed computation

DCN scores a full real tool schema and two counterfactual deletions with the same frozen cross-encoder. Removing the operation description yields one relevance drop; removing the argument contract yields another. Candidate score is the full score plus the smaller drop:

`full + min(full - without_operation, full - without_arguments)`.

The minimum is a conjunctive lower-support rule: a tool gains only to the extent that both operation semantics and argument contract are necessary for its query relevance. A negative drop from either deletion penalizes the tool. Tool-name SHA-256 breaks exact score ties.

No label, fitted parameter, generated text, task decomposition, original-menu marker, per-query rule or Confirmation byte is available.

## Mandatory controls

The frozen full-schema score, operation-only schema score, argument-only schema score, arithmetic mean of both deletion drops, and maximum of both deletion drops are all reported. DCN must strictly exceed every control in Development top-1 and then survive untouched Confirmation.

## Data and Claim boundary

Development is the exposed 200-query P084/BFCL v3 expanded menu. Untouched Confirmation is BFCL v4 live-multiple at commit `6ea57973c7a6097fd7c5915698c54c17c5b1b6c8` and may be acquired only after a positive written Promotion Audit.

Only if Development, untouched Confirmation, independent audits, three fresh leaf Reviews and the main-Codex Decision all pass:

> On the two pinned BFCL compact related-tool menu datasets, adding the smaller of operation-description and argument-contract deletion drops to a frozen full-schema cross-encoder improves top-1 gold-function membership and first-gold MRR over full, single-deletion, mean-support and max-support controls.

No argument correctness, complete multi-call recall, execution, Agent success, large-registry, causal, universal or first-ever claim is allowed.

