# Main Codex Development Promotion Audit v025

Disposition: `NO_GO_FOR_CONFIRMATION`.

Development and independent replay are mechanically valid. The runner exited 0 after 592.389 seconds in the fixed Python 3.11.15 environment; audit exited 0 with `AUDIT_OK`, 1,185 rows, 71 tasks, 35 models and 8,295 scores replayed, zero errors, maximum score error 0 and maximum metric error 0. Dataset, manifest, program, config, base, raw, source, model, summary, capture and audit hashes are frozen and current.

Scientifically, VIAF fails five of seven preregistered gates. Its AUC `0.9054923404768606` and TPR@5%FPR `0.6904024767801857` miss the absolute gates. The strongest comparator is position-free `anchor_bag` at AUC `0.9157050379960597`; VIAF's delta is `-0.010212697519199176`, with task-bootstrap 95% interval `[-0.021227694512958452,-0.0008757622717760083]`. It therefore neither reaches the required `+0.005` nor beats all comparators, and the uncertainty interval is wholly negative.

The two passing mechanism gates do not rescue the Claim. VIAF beats command duplication slightly on anchor-present rows and stays within tolerance without an anchor, but it loses to `anchor_bag` in both strata. Results are negative for every generator model, four of five folds, four of five source datasets, and within-task pairwise orderings favor anchor_bag 139 to 52 on comparator-exclusive correct pairs. At equal observed FPR, anchor_bag yields ten more true positives. Full raw/source inspection found real isolated VIAF wins but no coherent concentration that could justify the frozen Claim or a narrower post-hoc subgroup Claim.

The bounded Claim specifically requires verifier-relative order to beat the position-free anchor control. The evidence directly falsifies that condition. Confirmation bucket 0 must remain unopened. There will be no v025 Reviewer, Decision or Delivery. v025 is frozen as a valid negative Development result. The same Run advances to v026, but v026 may not retune VIAF's predicate, block weights, vocabulary, regularization, gates, task selection or Claim; it must select a scientifically different computation.
