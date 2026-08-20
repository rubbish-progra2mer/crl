# Experiment Plan

```json
{
  "experiment_id": "v012",
  "candidate_sha256": "137df6fffef43169ab6ea50f2dda940aabbb2c4cd3719db0ff2a99293feac29d",
  "evidence_packet_sha256": "941002813b2b0f0e1f949d95030bd4adc9ba02be1a72f29a22d5f87e52e61673"
}
```

## Codex Plan

# v012 Reference-Conditioned Effect Delta

## Frozen before scientific results

This plan fixes v012 before Development acquisition, model fitting, threshold selection, or scientific metric output. Selection exposure is fully disclosed in `selection_context_v012.md`: task `1012` metadata, one stripped hack, and one successful baseline were read while choosing the problem. The config forces that task into training. No Confirmation bucket-3 task metadata or trajectory content has been acquired or read.

- Problem SHA-256: `0c733fd584a637cc281f3fd3414ab7ed1e0b500ac6ded3250c79e90000cc4a6e`.
- Research Map SHA-256: `ea7197e5d560574b30656653bd1d71d53617580d8935889bfed8f8f52e43a02f`.
- Nearest Prior SHA-256: `eb4db3ba3406ee1d9edc73e687196463b690d3d2839bf36f878ef844564f467e`.
- Candidate SHA-256: `137df6fffef43169ab6ea50f2dda940aabbb2c4cd3719db0ff2a99293feac29d`.
- Evidence Packet SHA-256: `941002813b2b0f0e1f949d95030bd4adc9ba02be1a72f29a22d5f87e52e61673`; all five Evidence entries and their passages are current.
- Acquisition program SHA-256: `cf87ec4994081b4516695806b471daf75e923fe511d0b67d05b4ab126d34e836`.
- Evaluation program SHA-256: `a29b8aace75bf5505620fab71c982e296e045cb1590a20a5a9c19a63c233d78d`.
- Independent audit program SHA-256: `366d55e4f9c3ca9ada37bfe1243650e960b76285a96438d97c8d98555125038b`.
- Config SHA-256: `82c4b269414c4f53e0bc54a05cc1896b087ea8e5d711b074aae4bc2ff8097ce3`.

The four directly read prior PDFs and their fixed hashes are listed in `nearest_prior_v012.md`. They will be saved as Experiment Artifacts before Review.

## Code checks before freeze

The following are implementation checks only, not research or Delivery evidence:

- AST parsing of all three Python files: exit `0`.
- Import and 29-feature finite-vector check: exit `0`.
- In-memory 12-task split/model/bootstrap sanity: exit `0`.
- Sparse checkout and action extraction for the already exposed task `1012`: exit `0`, 21 rows (6 successful baselines, 15 stripped serious exploits), fixed commit matched.
- `ruff` was not installed (`No module named ruff`); no package was installed and this missing optional linter is not treated as a code failure.

## Data acquisition and untouched boundary

Repository: `https://github.com/few-sh/terminal-wrench.git`.

Fixed commit: `d8a29613235a0ef56a8b70b3142626a533da28c2`.

The acquisition program performs a blobless shallow fetch of that exact commit and sparse-checks out only selected task metadata and referenced trajectories. It saves full action-only rows plus a source-file manifest containing relative path, byte count, and SHA-256.

- Development bucket: first byte of `SHA256(task_id)` modulo four equals `2`.
- Confirmation bucket: first byte modulo four equals `3`.
- Development train: second byte modulo five in `{0,1,2}`.
- Development validation: second byte modulo five equals `3`.
- Development held-out test: second byte modulo five equals `4`.
- Every task ID remains in exactly one split.
- Every `selection_exposed_task_ids` entry is forced into train before the second-byte rule. The only entry is `1012`.
- One lexicographically first successful `(model, baseline_label, source_path)` trajectory per eligible task is the reference and is excluded from fitting and evaluation.
- A task is eligible only with at least one additional successful baseline and at least one stripped `rewarded_serious_exploit`.

Confirmation acquisition is forbidden until every Development gate passes and the main Codex records a Promotion Audit. No substitute dataset, commit, bucket, label, or split is allowed.

## Observable features and prohibited leakage

Agent commentary is uniformly excluded. The primary text comparator sees evaluated commands and terminal outputs only. It does not see task ID, model ID, source dataset, stored explanation, `key_hack_steps`, classification name, or observed category.

RCED adds a fixed 29-dimensional vector computed from the evaluated trajectory and its held-out same-task reference:

- ordered executable and coarse-effect edit distance;
- novel and missing executables/effects;
- novel and missing paths and write paths;
- direct-write and privileged novel-write counts;
- verifier-read-to-write, novel-write-to-verify, read/write ordering;
- coarse effect-count deltas.

Labels and observed categories are used only for targets and reporting slices. The reference row is never an evaluated negative. The parser is approximate and does not claim to reconstruct true filesystem state.

## Fair comparators and learner

All learned methods use class-weighted logistic regression with `C=1`, `liblinear`, seed `12012`, and the same training labels.

- `text`: command/output character TF-IDF, analyzer `char_wb`, n-grams 3–5, `min_df=2`, maximum 30,000 features.
- `structured`: standardized 29-dimensional RCED vector only.
- `envelope`: fixed unfitted mean of nine bounded divergence/risk features.
- `candidate`: the identical text representation concatenated with the standardized 29-dimensional RCED vector.

The strongest local comparator is prospectively defined as the largest held-out Development AUC among `text`, `structured`, and `envelope`, with method name as deterministic tie-break. This conservative selection cannot improve the Candidate.

## Threshold, metrics, resampling, and gates

Each method threshold is selected once on validation by maximum TPR among ROC points with empirical FPR `<= 0.05`, breaking ties toward the higher threshold. The exact train-fitted models and thresholds are frozen for possible Confirmation; there is no post-test refit.

Held-out Development reports:

- ROC AUC;
- empirical TPR at FPR `<= 0.05`;
- FPR and TPR at the frozen validation threshold;
- model, source-dataset, and positive-category slices;
- Candidate-minus-strongest-comparator AUC.

The AUC-delta confidence interval uses 2,000 bootstrap resamples of task IDs with replacement and seed `12012`; all rows for a sampled task move together.

Every Development gate must pass:

1. Candidate AUC `>= 0.82`.
2. Candidate empirical TPR@5%FPR `>= 0.35`.
3. Candidate minus strongest-comparator AUC `>= 0.02`.
4. Task-cluster bootstrap 95% lower bound for that delta `> 0`.
5. Frozen-threshold FPR `<= 0.08`.
6. Frozen-threshold TPR `>= 0.30`.
7. Reference exclusion, task partitioning, source hashes, config/model binding, feature finiteness, and independent metric recomputation all pass.

After authorized acquisition, untouched Confirmation reuses the frozen model, features, comparator identity, and thresholds. Every Confirmation gate must pass:

1. Candidate AUC `>= 0.80`.
2. Candidate empirical TPR@5%FPR `>= 0.30`.
3. Candidate minus the frozen strongest comparator AUC `> 0`.
4. Task-cluster bootstrap 95% lower bound for that delta `>= 0`.
5. Frozen-threshold FPR `<= 0.08`.
6. Frozen-threshold TPR `>= 0.25`.
7. Development and Confirmation task IDs are disjoint and the independent audit passes.

Boolean gate fields never substitute for the main Codex reading raw predictions, recomputing metrics, inspecting mechanism behavior, and judging the claim.

## Captured Development attempts

Interpreter for every attempt:

```text
D:\Desktop\crl\crl_agent_v3\.venv\python.exe
```

Capture runner:

```text
D:\Desktop\crl\crl_agent_v3\tools\run_local_experiment.py
```

### `dev_acquire_001`

Cwd:

```text
D:\Desktop\crl\20260722_1550_run01\implementation_v012
```

Scientific argv:

```text
acquire.py --phase development --config config.json --output-dir ..\experiment_v012\work\dev_acquire_001 --work-root ..\experiment_v012\work\dev_source_001
```

Capture directory: `experiment_v012/captures/dev_acquire_001/`.

Declared outputs:

- `experiment_v012/work/dev_acquire_001/dataset.jsonl`
- `experiment_v012/work/dev_acquire_001/manifest.json`

### `dev_eval_001`

Cwd:

```text
D:\Desktop\crl\20260722_1550_run01\implementation_v012
```

Scientific argv:

```text
evaluate.py --phase development --config config.json --dataset ..\experiment_v012\work\dev_acquire_001\dataset.jsonl --manifest ..\experiment_v012\work\dev_acquire_001\manifest.json --output-dir ..\experiment_v012\work\dev_eval_001
```

Capture directory: `experiment_v012/captures/dev_eval_001/`.

Declared outputs:

- `frozen_model.joblib`
- `raw_predictions.jsonl`
- `reference_records.jsonl`
- `task_ids.json`
- `summary.json`
- `environment.json`

### `dev_audit_001`

Cwd:

```text
D:\Desktop\crl\20260722_1550_run01\implementation_v012
```

Scientific argv:

```text
audit.py --phase development --config config.json --dataset ..\experiment_v012\work\dev_acquire_001\dataset.jsonl --manifest ..\experiment_v012\work\dev_acquire_001\manifest.json --repository-root ..\experiment_v012\work\dev_source_001\repository --raw-predictions ..\experiment_v012\work\dev_eval_001\raw_predictions.jsonl --references ..\experiment_v012\work\dev_eval_001\reference_records.jsonl --summary ..\experiment_v012\work\dev_eval_001\summary.json --frozen-model ..\experiment_v012\work\dev_eval_001\frozen_model.joblib --report ..\experiment_v012\work\dev_audit_001\report.json
```

Capture directory: `experiment_v012/captures/dev_audit_001/`.

Declared output: `experiment_v012/work/dev_audit_001/report.json`.

Before scientific execution, the three programs, config, Candidate/Map/Prior/selection documents, Evidence Packet, and four prior PDFs are saved with `ResearchWorkspace.save_experiment_artifact()`. After each attempt, its `execution.json`, `stdout.bin`, `stderr.bin`, and declared outputs are saved as immutable Experiment Artifacts with attempt-specific names.

## Direct falsification and version rule

Any nonzero scientific attempt, missing output, changed frozen byte, source-hash failure, reference leakage, task-split violation, non-finite feature, unrecomputable metric, false Development gate, unfair comparator, or material nearest-prior collision closes v012 without Confirmation. Any failed Confirmation gate closes v012 without Review.

Closing v012 freezes all persistent bytes and advances the same Run to v013; it does not terminate the Run. Only a fully passed Confirmation can authorize a frozen Review Packet and exactly three fresh leaf Reviewers.
