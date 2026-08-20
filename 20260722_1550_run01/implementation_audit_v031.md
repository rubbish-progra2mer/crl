# Implementation Audit v031

Status: `APPROVED_FOR_FROZEN_DEVELOPMENT_PLAN`.

This is the Main Codex's pre-execution source audit. No v031 scientific score, fitted classifier, control ranking or gate outcome existed when this audit was written.

## Reviewed computation

- `program.py` extracts only the task-description span, uses the frozen v012 physical command splitter and operation classifier, and computes one frozen cross-encoder score for every command segment.
- Candidate features are exactly four ordered role blocks (`mutation`, `verify`, `read`, `other`) with fraction, minimum, mean, maximum and population standard deviation. Empty blocks are zero-filled.
- `direct_action`, `task_concat`, four role fractions, global relevance and equal-capacity chronological relevance are all present as mandatory controls.
- Development scoring excludes both the held-out task fold and the complete target generator. Every target-generator×fold cell is assigned once.
- Dense scaling is fit only on training rows. Every method uses the same frozen character TF-IDF and balanced logistic-regression constructors from `base_v012.py`.
- Confirmation can only apply frozen full target-generator bundles. It rejects any task overlap with Development and uses the strongest comparator selected once on Development.
- Development requires a strictly positive task-bootstrap lower bound; Confirmation requires a nonnegative lower bound exactly, without numerical slack.

## Corrections before freeze

The draft incorrectly derived the Python executable from the PyTorch package path. It now records `sys.executable`. An unused dense-model helper was removed. The Confirmation bootstrap comparison was changed from an epsilon approximation to exact `>= 0.0`.

The first unit-test execution produced `4 passed, 1 failed`: the test expected a mutation score in the verify block. The implementation's documented role order was correct. The assertion was corrected to check mutation at index 1 and verify at index 6; the second and final necessary execution produced `5 passed in 4.20s`, exit `0`. `py_compile` for program, auditor and tests exited `0`. Generated `__pycache__` was removed, and no `.pyc` remains.

## Structural preflight

A read-only source preflight under the shared Python 3.11.15 interpreter found:

- 4,256 rows and 4,256 unique row IDs;
- 250 task IDs and 460 exact task-description strings;
- 444,000 task-command pairs;
- role counts: 59,269 mutation, 3,337 verify, 34,018 read and 347,376 other;
- task-fold row counts: 1,525, 1,339 and 1,392;
- all nine target-generator×fold cells contain both classes;
- all three generator slices and all five source-dataset slices contain both classes.

No score or label-derived feature was computed by this preflight.

## Independent auditor

`audit.py` does not import `program.py`. It independently repeats input/model hash checks, task extraction, segmentation, operation roles, all 444,000 cross-encoder scores, dense features, double-held-out training, OOF predictions, task bootstrap, slice metrics and gates. For Development it additionally retrains all three full target-generator bundles and compares their predictions against the serialized frozen bundles.

Required maximum errors are `1e-6` for pair scores, `1e-12` for dense features, `1e-10` for predictions and frozen full-model predictions, and `1e-12` for metrics/gates.

## Frozen implementation identities

- program: `2bd01db3af6b9e448df4cebbbd53d7e1bcf811f2bd588577954deaebecb18300`
- independent auditor: `b5e923337bf698f8d7a66a5519e757bf42aa245dd08c5effe7e8da1c7dddb3c5`
- tests: `13d3b8f9e28b633d0506d2e616652a05d66209f06225f004233d60a4d95cb347`
- config: `e98e37614cec3ce86bce8fd70f0634678e93b58f29c94734299d591d832dff55`
- frozen v012 base: `a29b8aace75bf5505620fab71c982e296e045cb1590a20a5a9c19a63c233d78d`
- conditional acquisition: `cf87ec4994081b4516695806b471daf75e923fe511d0b67d05b4ab126d34e836`
- capture runner: `410a620d0734613036f4fea4bc017c0cd1d0de293e1a3d4577c75eec584eaa4a`

The six cross-encoder file hashes in `config.json` were rechecked against `experiment_v029/model_cross`; the directory contains exactly those six files.

## Main-Codex judgment

The implementation matches the narrow Claim Contract and is suitable for one frozen Development execution. This approval is not a scientific result, does not authorize untouched Confirmation, and does not authorize any Reviewer or Delivery.
