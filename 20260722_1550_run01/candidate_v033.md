<!-- crl-v3-evidence-ids
["ev-p040-failure-core"]
-->
# Candidate v033 — Successful-Only Conditional Action Innovation

## Changed computation

In each task-and-generator-held-out bundle, fit a shared training-only
char-TFIDF/SVD latent space. Successful training trajectories alone learn an
equal-task-weight ridge map from task latent to normal action latent. The
absolute innovation of an evaluated action from that task-conditioned
prediction augments a direct supervised action-text detector.

No same-task support, reasoning trace, exploit category, fixed command role,
LLM call or test-time retrieval is used.

## Mandatory controls

- direct action/terminal text;
- task/action text concatenation;
- direct text plus raw task and action latents;
- direct text plus the identity task/action absolute difference;
- direct text plus an equal-capacity conditional innovation map trained on all
  rows rather than successful rows.

The Candidate must strictly beat every control. In particular, it cannot claim
a normal-map contribution unless it beats the all-row conditional map.

## Data and exposure

Already exposed Terminal Wrench buckets 1-3 are Development. Selection after
v020-v031 is optional stopping and is explicitly disclosed. Repository bucket 0
remains absent and untouched; it can be acquired only after every Development
gate and a positive main-Codex Promotion Audit.

## Claim Contract

The exact representation, mapping, controls, double-holdout bundles, metrics,
gates and Confirmation protocol are fixed in `research_map_v033.md`.

At most, a passing result can support the narrow fixed-protocol empirical Claim
written there. It cannot establish general task alignment, intent detection,
causal exploit localization, environment correctness, online safety or
first-ever novelty.
