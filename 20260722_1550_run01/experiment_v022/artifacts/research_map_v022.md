<!-- crl-v3-evidence-ids
["ev-p040-failure-core","ev-p074-contract-state-commit","ev-p074-missing-schema-true-postcondition"]
-->
# Research Map v022

## Frozen Candidate and comparators

Candidate remains `[x,max(x-r,0),max(r-x,0)]`. The six comparators remain text, reference concat, absolute delta, v012 RCED, triple text and duplicated absolute. The frozen Development strongest comparator is duplicated absolute.

## Inherited Development evidence

v021 Candidate AUC `0.9408656005`; duplicated-absolute AUC `0.9251839315`; delta `+0.0156816690`; task-bootstrap 95% `[+0.0041492512,+0.0253812488]`; seven of seven gates; independent replay error zero. v021 Promotion Audit SHA-256 is `183cf86a029e5b3d88f8dac406605cd3c2287eca1d08f49e77de99055204e740`.

## Frozen Confirmation conditions

On bucket 3, Candidate AUC must be at least `0.88`, TPR@5%FPR at least `0.40`, frozen-threshold FPR at most `0.08`, and frozen-threshold TPR at least `0.35`. Candidate must strictly exceed every one of the six comparators. Candidate-minus-duplicated-absolute AUC must be positive with task-cluster bootstrap lower bound at least zero. Task sets, references, model, thresholds, source hashes and independent replay must be valid.

The main Codex must read all raw outcomes and limitations; booleans cannot authorize Review.
