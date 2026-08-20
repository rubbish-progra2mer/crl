# Experiment Plan

```json
{
  "experiment_id": "v021",
  "candidate_sha256": "fd3978d343d0ca33a2301a3c2e7e7b2897c37b2b2c3e5ab74ae393608ee4e917",
  "evidence_packet_sha256": "bb17ab6db299968bba3fcbba599f2f6e9a0fe4095497be2c2d47d36674a825cf"
}
```

## Codex Plan

# v021 One-Shot Development Plan

Status: `FROZEN_BEFORE_MODEL_FITTING`.

This Plan authorizes exactly one v021 Development fit/score capture and, if its declared outputs exist, exactly one independent replay audit capture. Confirmation acquisition, Reviewers, Decision, Delivery and system-status change remain forbidden until a later written main-Codex Promotion Audit.

## Frozen question

Does the unchanged signed task-relative representation `[x,max(x-r,0),max(r-x,0)]` retain its reward-hack detection advantage when the strongest-comparator ladder includes both `[x,x,x]` and `[x,abs(x-r),abs(x-r)]` under identical three-block dimensionality and unchanged L2 logistic regression?

## Frozen hashes

- Candidate `fd3978d343d0ca33a2301a3c2e7e7b2897c37b2b2c3e5ab74ae393608ee4e917`.
- Evidence Packet `bb17ab6db299968bba3fcbba599f2f6e9a0fe4095497be2c2d47d36674a825cf`.
- Program wrapper `98e1f01451bfb6bc592dc2a8f24f23b10ac709fe665d40c5885ee20f6c5ef8d7`.
- Independent-audit wrapper `ff499a10f80fb4d428291d3fa43142a3248705d93fcefc506eeba74cb3c6c4a5`.
- Config `8d6eee0a9fdb29e286b918eb13a02bbf5ad246b5467b4ea2f93e9fe93ee50eb0`.
- Capacity-control test `9a631beeaa14c1345554cb4ac936d99150496616d1f8d0f11a0a62462799bbc7`.
- v020 base program `67ac151b6817d6619f915aad581da6c70f9ecdafeb780d87e31816c36009de92`.
- v020 base auditor `2f42878764989288ee44a68d287af2cccfb2e25f72f7eb2fde40e9d81a898607`.
- v012 base module `a29b8aace75bf5505620fab71c982e296e045cb1590a20a5a9c19a63c233d78d`.
- Development dataset `bd766eb62cf98e8fb1b8dd17c20d5edfc759eeb737bd3c232f73e656f9e713a3`.
- Prospective acquisition program `cf87ec4994081b4516695806b471daf75e923fe511d0b67d05b4ab126d34e836`.
- Implementation audit `ef0adbd4f66677f2b07586856619ba883f348f3d1faeb7ea130b205c2be03b43`.
- v020 result `1c25418fe891ed53cd8566bf62485bf7cc2cbe56893fbdd3b52f16117ec95fdd`.
- v020 Promotion Audit `8b67077e39644645719a3c7a6791d405e6be4f733c11dcdb2400e002e5eae6a8`.

All 22 copies in `experiment_v021/artifacts/` are immutable inputs. Only those copies may be executed or cited as the frozen v021 Development basis.

## Fixed design

- Source rows 1,729; 94 eligible reference rows; 1,613 evaluated examples; two ineligible tasks.
- Task splits remain train 54 tasks/943 rows, validation 20/318, Development-test 20/352.
- Development-test labels remain 131 negative and 221 positive examples.
- The single excluded successful same-task reference never appears among evaluated rows.
- TF-IDF remains char-wb n-grams 3-5, min-df 2, maximum 30,000, fit only on evaluated training trajectories.
- Every method uses class-weighted liblinear logistic regression, C=1, maximum 2,000 iterations and seed 12020.
- Each method freezes its validation-selected highest threshold achieving the best TPR at FPR <=0.05.
- Task-ID cluster bootstrap remains 2,000 resamples with seed 12020.
- The seven methods, in frozen order, are text, reference concat, absolute delta, v012 RCED, triple text, duplicated absolute and signed residual Candidate.
- Candidate, triple-text and duplicated-absolute each have 90,000 feature dimensions on the actual fixed training vocabulary.

## Development capture

Interpreter: `D:\Desktop\crl\crl_agent_v3\.venv\python.exe`.
Runner: `D:\Desktop\crl\crl_agent_v3\tools\run_local_experiment.py`.

- capture: `D:\Desktop\crl\20260722_1550_run01\experiment_v021\captures\dev_001`
- cwd: `D:\Desktop\crl\20260722_1550_run01\experiment_v021\artifacts`
- payload argv:
  `D:\Desktop\crl\crl_agent_v3\.venv\python.exe D:\Desktop\crl\20260722_1550_run01\experiment_v021\artifacts\program.py --phase development --config D:\Desktop\crl\20260722_1550_run01\experiment_v021\artifacts\config.json --dataset D:\Desktop\crl\20260722_1550_run01\experiment_v021\artifacts\development_dataset.jsonl --base-module D:\Desktop\crl\20260722_1550_run01\experiment_v021\artifacts\base_v012.py --output-dir D:\Desktop\crl\20260722_1550_run01\experiment_v021\dev_output_001`
- declared outputs: `raw_predictions.jsonl`, `reference_records.jsonl`, `summary.json`, `model.joblib`.

The runner executes once in the foreground. Exit code, stdout, stderr and all output bytes remain evidence regardless of outcome. No same-version retry, threshold change or model change is authorized.

## Independent audit capture

Only if all four Development outputs exist:

- capture: `D:\Desktop\crl\20260722_1550_run01\experiment_v021\captures\dev_audit_001`
- cwd: the same frozen artifact directory
- payload argv:
  `D:\Desktop\crl\crl_agent_v3\.venv\python.exe D:\Desktop\crl\20260722_1550_run01\experiment_v021\artifacts\audit.py --config D:\Desktop\crl\20260722_1550_run01\experiment_v021\artifacts\config.json --dataset D:\Desktop\crl\20260722_1550_run01\experiment_v021\artifacts\development_dataset.jsonl --base-module D:\Desktop\crl\20260722_1550_run01\experiment_v021\artifacts\base_v012.py --raw-predictions D:\Desktop\crl\20260722_1550_run01\experiment_v021\dev_output_001\raw_predictions.jsonl --summary D:\Desktop\crl\20260722_1550_run01\experiment_v021\dev_output_001\summary.json --reference-records D:\Desktop\crl\20260722_1550_run01\experiment_v021\dev_output_001\reference_records.jsonl --model D:\Desktop\crl\20260722_1550_run01\experiment_v021\dev_output_001\model.joblib --report D:\Desktop\crl\20260722_1550_run01\experiment_v021\dev_audit_output_001\report.json`
- declared output: `report.json`.

Audit support requires exit 0, `AUDIT_OK`, 94 references, 352 evaluated Development-test rows, seven replayed models, 2,464 replayed scores, and maximum score/metric errors <= `1e-12`.

## Development support conditions

All seven frozen gates in `research_map_v021.md` must pass. Candidate AUC must be >=0.91; TPR@5%FPR >=0.55; AUC delta over the strongest of all six comparators >=0.005 with task-bootstrap lower bound >0; frozen-threshold FPR <=0.08 and TPR >=0.45; Candidate AUC must strictly exceed all six comparators; and the independent integrity audit must pass.

The main Codex must then read the complete summary, all 352 raw prediction rows, thresholds, feature dimensions, every comparator, task/category/model slices, false positives, false negatives and Candidate/comparator score transitions. Numeric gates never authorize Confirmation automatically.

Failure freezes v021 and advances the same Run without retry or gate changes. Only an affirmative written main-Codex Promotion Audit may authorize first acquisition of untouched Terminal Wrench bucket 3. No Reviewer may be created before a complete later Review Packet is frozen.
