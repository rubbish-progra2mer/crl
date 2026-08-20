# Experiment Plan

```json
{
  "experiment_id": "v020",
  "candidate_sha256": "7c1326b3309cd0e21f52c749b38724c965821e81cf6880f20dde07678462f690",
  "evidence_packet_sha256": "514f61891e70af5be51a23df0e891dd3cabb0c2de18bc3112c79bd7bdf6f1154"
}
```

## Codex Plan

# v020 One-Shot Development Plan

Status: `FROZEN_BEFORE_MODEL_FITTING`.

This Plan authorizes one Development fit/score capture and one independent audit capture. Confirmation acquisition, Reviewers, Decision, Delivery, and system status change remain forbidden.

## Frozen question

Does the signed sparse task-relative representation `[x,max(x-r,0),max(r-x,0)]` improve stripped Terminal Wrench reward-hack detection over raw text, reference concatenation, unsigned absolute delta, and v012 RCED under identical data, vocabulary, learner, and threshold selection?

## Frozen hashes

- Candidate `7c1326b3309cd0e21f52c749b38724c965821e81cf6880f20dde07678462f690`.
- Evidence Packet `514f61891e70af5be51a23df0e891dd3cabb0c2de18bc3112c79bd7bdf6f1154`.
- Program `67ac151b6817d6619f915aad581da6c70f9ecdafeb780d87e31816c36009de92`.
- Independent audit `2f42878764989288ee44a68d287af2cccfb2e25f72f7eb2fde40e9d81a898607`.
- Config `fb437f9b70d57e7ca0c4d13baa13a41b0f28be0441870574f7b909c2208cd43b`.
- Tests `4fc711296923e32fa0e0ac72b538cd01cea5ce8a8b0c22e6574447ce15395500`.
- Development dataset `bd766eb62cf98e8fb1b8dd17c20d5edfc759eeb737bd3c232f73e656f9e713a3`.
- Frozen v012 base module `a29b8aace75bf5505620fab71c982e296e045cb1590a20a5a9c19a63c233d78d`.
- Prospective acquisition program `cf87ec4994081b4516695806b471daf75e923fe511d0b67d05b4ab126d34e836`.
- Implementation audit `8d3ece5ca85420b38dc6f96eddc7b2b9d2360e2197d7ea17868de184d9899b4d`.

Only the copies in `experiment_v020/artifacts/` may be executed.

## Fixed design

- Source rows 1,729; 94 eligible references; 1,613 evaluated examples; two ineligible tasks.
- Task splits: train 54 tasks/943 rows; validation 20/318; Development-test 20/352.
- Development-test labels: 131 negatives, 221 positives.
- Reference IDs are excluded from every evaluated row.
- TF-IDF: char-wb n-grams 3-5, min df 2, max 30,000, vocabulary fit only on evaluated training trajectories.
- Learner: class-weighted liblinear logistic regression, C=1, max 2,000 iterations, seed 12020.
- Validation selects each method's highest threshold achieving its best TPR with FPR <=0.05.
- Bootstrap: 2,000 task-ID cluster resamples, seed 12020.

## Development capture

Runner interpreter: `D:\Desktop\crl\crl_agent_v3\.venv\python.exe`.
Runner: `D:\Desktop\crl\crl_agent_v3\tools\run_local_experiment.py`.

- capture: `D:\Desktop\crl\20260722_1550_run01\experiment_v020\captures\dev_001`
- cwd: `D:\Desktop\crl\20260722_1550_run01\experiment_v020\artifacts`
- inputs: `program.py`, `config.json`, `development_dataset.jsonl`, `base_v012.py`
- payload argv:
  `D:\Desktop\crl\crl_agent_v3\.venv\python.exe D:\Desktop\crl\20260722_1550_run01\experiment_v020\artifacts\program.py --phase development --config D:\Desktop\crl\20260722_1550_run01\experiment_v020\artifacts\config.json --dataset D:\Desktop\crl\20260722_1550_run01\experiment_v020\artifacts\development_dataset.jsonl --base-module D:\Desktop\crl\20260722_1550_run01\experiment_v020\artifacts\base_v012.py --output-dir D:\Desktop\crl\20260722_1550_run01\experiment_v020\dev_output_001`
- declared outputs: `raw_predictions.jsonl`, `reference_records.jsonl`, `summary.json`, `model.joblib`.

The runner executes once in the foreground. Exit code and every byte remain evidence regardless of outcome.

## Independent audit capture

Only if all Development outputs exist:

- capture: `D:\Desktop\crl\20260722_1550_run01\experiment_v020\captures\dev_audit_001`
- cwd: frozen artifacts directory
- inputs: frozen `audit.py`, config, dataset, base module, all four Development outputs
- payload argv:
  `D:\Desktop\crl\crl_agent_v3\.venv\python.exe D:\Desktop\crl\20260722_1550_run01\experiment_v020\artifacts\audit.py --config D:\Desktop\crl\20260722_1550_run01\experiment_v020\artifacts\config.json --dataset D:\Desktop\crl\20260722_1550_run01\experiment_v020\artifacts\development_dataset.jsonl --base-module D:\Desktop\crl\20260722_1550_run01\experiment_v020\artifacts\base_v012.py --raw-predictions D:\Desktop\crl\20260722_1550_run01\experiment_v020\dev_output_001\raw_predictions.jsonl --summary D:\Desktop\crl\20260722_1550_run01\experiment_v020\dev_output_001\summary.json --reference-records D:\Desktop\crl\20260722_1550_run01\experiment_v020\dev_output_001\reference_records.jsonl --model D:\Desktop\crl\20260722_1550_run01\experiment_v020\dev_output_001\model.joblib --report D:\Desktop\crl\20260722_1550_run01\experiment_v020\dev_audit_output_001\report.json`
- declared output: audit report.

Audit support requires exit 0, `AUDIT_OK`, 94 references, 352 evaluated Development-test rows, five models, 1,760 replayed scores, and maximum score/metric errors <= `1e-12`.

## Development support conditions

All seven frozen gates in `research_map_v020.md` must pass. Candidate must reach AUC >=0.91, TPR@5%FPR >=0.55, AUC delta >=0.005 over the strongest comparator with task-bootstrap lower bound >0, validation-threshold FPR <=0.08 and TPR >=0.45, and strictly beat each comparator. Reference/split/integrity audit must pass.

The main Codex must then read all predictions, thresholds, feature dimensions, per-comparator outcomes, bootstrap, task/category slices, false positives, false negatives, and score transitions. Gates do not automatically authorize Confirmation.

A failure freezes v020 and advances the same Run without retry or threshold changes. Only a positive written Promotion Audit may authorize acquisition of repository bucket 3. No Reviewer may be created before a complete later Review Packet.
