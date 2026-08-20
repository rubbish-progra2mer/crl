# v021 One-Shot Untouched Confirmation Plan

Status: `FROZEN_BEFORE_CONFIRMATION_ACQUISITION`.

This supplemental execution contract is authorized by `promotion_audit_v021.md` SHA-256 `183cf86a029e5b3d88f8dac406605cd3c2287eca1d08f49e77de99055204e740`. It supplements, and does not alter, the publish-once Development Plan SHA-256 `f578b11735364c67430f2e03ea1c1c7ec0107a00051e194349ac9239b8bbff50`.

Exactly one bucket-3 acquisition capture is authorized. If and only if acquisition exits `0` and its dataset and manifest are frozen through the existing Artifact API, exactly one Confirmation scoring capture and exactly one independent replay audit capture are authorized. No refit, threshold selection, comparator change, same-version retry, Review, Decision, Delivery or system-state change is authorized by this file.

## Frozen identity

- Candidate SHA-256 `fd3978d343d0ca33a2301a3c2e7e7b2897c37b2b2c3e5ab74ae393608ee4e917`.
- Evidence Packet SHA-256 `bb17ab6db299968bba3fcbba599f2f6e9a0fe4095497be2c2d47d36674a825cf`.
- Program wrapper SHA-256 `98e1f01451bfb6bc592dc2a8f24f23b10ac709fe665d40c5885ee20f6c5ef8d7`.
- Audit wrapper SHA-256 `ff499a10f80fb4d428291d3fa43142a3248705d93fcefc506eeba74cb3c6c4a5`.
- v020 base program SHA-256 `67ac151b6817d6619f915aad581da6c70f9ecdafeb780d87e31816c36009de92`.
- v020 base auditor SHA-256 `2f42878764989288ee44a68d287af2cccfb2e25f72f7eb2fde40e9d81a898607`.
- v012 base SHA-256 `a29b8aace75bf5505620fab71c982e296e045cb1590a20a5a9c19a63c233d78d`.
- Config SHA-256 `8d6eee0a9fdb29e286b918eb13a02bbf5ad246b5467b4ea2f93e9fe93ee50eb0`.
- Acquisition program SHA-256 `cf87ec4994081b4516695806b471daf75e923fe511d0b67d05b4ab126d34e836`.
- Frozen Development model SHA-256 `8ff9c2cc3ec1ade5aa404323264738800a909c7690d3b867ea48e6fb68fa56f7`.
- Repository commit `d8a29613235a0ef56a8b70b3142626a533da28c2`.
- Confirmation selector: SHA-256 first byte modulo `4` equals bucket `3`.
- Development selector used bucket `2`; task sets must be disjoint.

Interpreter for every command: `D:\Desktop\crl\crl_agent_v3\.venv\python.exe`.
Runner for every capture: `D:\Desktop\crl\crl_agent_v3\tools\run_local_experiment.py`.

## Acquisition capture

- capture: `D:\Desktop\crl\20260722_1550_run01\experiment_v021\captures\confirmation_acquire_001`
- cwd: `D:\Desktop\crl\20260722_1550_run01\experiment_v021\artifacts`
- work root: `D:\Desktop\crl\20260722_1550_run01\experiment_v021\work\confirmation_acquire_001`
- output directory: `D:\Desktop\crl\20260722_1550_run01\experiment_v021\confirmation_acquire_output_001`
- payload argv:
  `D:\Desktop\crl\crl_agent_v3\.venv\python.exe D:\Desktop\crl\20260722_1550_run01\experiment_v021\artifacts\acquire.py --phase confirmation --config D:\Desktop\crl\20260722_1550_run01\experiment_v021\artifacts\config.json --output-dir D:\Desktop\crl\20260722_1550_run01\experiment_v021\confirmation_acquire_output_001 --work-root D:\Desktop\crl\20260722_1550_run01\experiment_v021\work\confirmation_acquire_001`
- declared outputs: `dataset.jsonl`, `manifest.json`.

The capture must bind the frozen acquisition program and config. The manifest must record the exact commit, bucket 3, config hash, dataset hash, every selected task ID and every source-file hash. The main Codex may verify manifest structure and hashes but may not calculate a Candidate outcome before the fixed model is scored.

On exit `0`, the dataset and manifest plus acquisition execution/stdout/stderr are immediately copied through the Artifact API as `confirmation_dataset.jsonl`, `confirmation_manifest.json`, `confirmation_acquire_001_execution.json`, `confirmation_acquire_001_stdout.bin`, and `confirmation_acquire_001_stderr.bin`. Only those immutable copies may enter Confirmation scoring.

## Confirmation scoring capture

- capture: `D:\Desktop\crl\20260722_1550_run01\experiment_v021\captures\confirmation_eval_001`
- cwd: frozen `experiment_v021/artifacts/`
- output directory: `D:\Desktop\crl\20260722_1550_run01\experiment_v021\confirmation_output_001`
- payload argv:
  `D:\Desktop\crl\crl_agent_v3\.venv\python.exe D:\Desktop\crl\20260722_1550_run01\experiment_v021\artifacts\program.py --phase confirmation --config D:\Desktop\crl\20260722_1550_run01\experiment_v021\artifacts\config.json --dataset D:\Desktop\crl\20260722_1550_run01\experiment_v021\artifacts\confirmation_dataset.jsonl --base-module D:\Desktop\crl\20260722_1550_run01\experiment_v021\artifacts\base_v012.py --output-dir D:\Desktop\crl\20260722_1550_run01\experiment_v021\confirmation_output_001 --model D:\Desktop\crl\20260722_1550_run01\experiment_v021\artifacts\dev_model.joblib --input-manifest D:\Desktop\crl\20260722_1550_run01\experiment_v021\artifacts\confirmation_manifest.json`
- declared outputs: `raw_predictions.jsonl`, `reference_records.jsonl`, `summary.json`.

The program must use the seven frozen models, their seven frozen validation thresholds and Development's frozen strongest comparator `duplicated_absolute`. It must not call `.fit`, mutate the model, select a threshold, remove a task or revise a gate.

## Independent audit capture

Only if scoring exits `0` and all three outputs exist:

- capture: `D:\Desktop\crl\20260722_1550_run01\experiment_v021\captures\confirmation_audit_001`
- cwd: frozen artifacts directory
- output: `D:\Desktop\crl\20260722_1550_run01\experiment_v021\confirmation_audit_output_001\report.json`
- payload argv:
  `D:\Desktop\crl\crl_agent_v3\.venv\python.exe D:\Desktop\crl\20260722_1550_run01\experiment_v021\artifacts\audit.py --config D:\Desktop\crl\20260722_1550_run01\experiment_v021\artifacts\config.json --dataset D:\Desktop\crl\20260722_1550_run01\experiment_v021\artifacts\confirmation_dataset.jsonl --base-module D:\Desktop\crl\20260722_1550_run01\experiment_v021\artifacts\base_v012.py --raw-predictions D:\Desktop\crl\20260722_1550_run01\experiment_v021\confirmation_output_001\raw_predictions.jsonl --summary D:\Desktop\crl\20260722_1550_run01\experiment_v021\confirmation_output_001\summary.json --reference-records D:\Desktop\crl\20260722_1550_run01\experiment_v021\confirmation_output_001\reference_records.jsonl --model D:\Desktop\crl\20260722_1550_run01\experiment_v021\artifacts\dev_model.joblib --report D:\Desktop\crl\20260722_1550_run01\experiment_v021\confirmation_audit_output_001\report.json`.

Audit support requires `AUDIT_OK`, zero errors, all eligible references, all raw rows, seven replayed models, exact score/metric agreement within `1e-12`, current hashes and zero Development-task overlap.

## Conjunctive scientific conditions

All conditions are required; the script's boolean count is evidence, not the decision:

1. Candidate AUC `>=0.88`.
2. Candidate TPR at FPR `<=0.05` is `>=0.40`.
3. Candidate AUC is strictly greater than each of all six comparators on Confirmation. This explicit main-Codex condition is required even though the frozen script's delta gate names only Development's strongest comparator.
4. Candidate-minus-duplicated-absolute AUC is `>0` and its fixed task-cluster bootstrap lower bound is `>=0`.
5. At the frozen Candidate threshold, FPR `<=0.08` and TPR `>=0.35`.
6. Acquisition, task disjointness, reference exclusion, raw rows, environment, model and audit integrity all pass.

All model/task/category slices, fixed-threshold corrections and regressions, false positives, false negatives and bounded original source trajectories remain reportable. No slice is silently deleted. The main Codex must read them before deciding whether a Review Packet may be frozen.

A scientific failure freezes v021 and advances the same Run to a scientifically different candidate. A failure before dataset bytes exist may only follow the captured external/execution evidence; no same-version retry is authorized here. No Reviewer may be started before a positive written main-Codex Confirmation audit and a complete immutable Review Packet.
