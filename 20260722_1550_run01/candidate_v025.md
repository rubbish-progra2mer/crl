<!-- crl-v3-evidence-ids
["ev-p040-failure-core","ev-p074-contract-state-commit","ev-p074-missing-schema-true-postcondition"]
-->
# Candidate v024 — Verifier-Inspection Anchored Factorization (VIAF)

## Changed computation

Use the first fixed verifier-inspection command batch to partition the ordered command surface. With one training-only shared vocabulary:

```text
x = mixed commands and terminal outputs
b = commands before first verifier inspection
a = verifier-inspection batch and every later command
VIAF = [x,b,a]
```

If no anchor exists, `b` is all commands and `a` is empty. The anchor predicate is exact in `research_map_v024.md`, frozen before bucket-1 data acquisition, and does not use labels.

## Mandatory closest comparators

- `[x,c,c]`: identical 90,000-dimensional capacity and command duplication;
- `[x,h1,h2]`: identical capacity with a fixed chronological half split;
- `[x,am,an]`: identical capacity and anchor vocabulary without before/after order;
- `[x]`, `[c]`, and `[c,o]`: lower-information mixed, commands-only and role-concatenated surfaces.

Every method uses identical task folds, rows, shared-vocabulary recipe and learner. VIAF must strictly beat every comparator, not merely mixed text.

## Data and claim boundary

Untouched bucket 1 is the only Development carrier; untouched bucket 0 is Confirmation. Five task-disjoint OOF folds cover every Development row exactly once. Full Development models are frozen before any Confirmation byte is acquired.

Only if Development, bucket-0 Confirmation, independent audits, three fresh leaf Reviews and the main-Codex Decision all pass:

> On the fixed task-disjoint Terminal Wrench stripped action protocol, assigning distinct shared-vocabulary coefficients to commands before versus at/after the first label-free verifier-inspection event improves reward-hack detection over mixed, command-only, role-concatenated, capacity-duplicated, fixed-time, and position-free anchor controls.

No hidden-intent, causal-verification, step-localization, online-safety, cross-benchmark, per-task-dominance or universal novelty claim is allowed.
