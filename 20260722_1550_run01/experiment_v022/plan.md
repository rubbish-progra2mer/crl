# Experiment Plan

```json
{
  "experiment_id": "v022",
  "candidate_sha256": "40f0e0e87bb1aff6c999c9c68937294578acb047081eb04c336eb4164fdea25e",
  "evidence_packet_sha256": "4f7462c159ca4db7372affac41cf6dd6bc8c5acc4d2131c6c0ee3db8d5274228"
}
```

## Codex Plan

# v022 One-Shot Untouched Confirmation Plan

Status: `FROZEN_BEFORE_CONFIRMATION_ACQUISITION`.

v022 is an execution-only continuation. v021 produced valid comparator-complete Development evidence and a positive main-Codex Promotion Audit, then its single bucket-3 Git fetch failed before dataset or manifest creation. v022 changes only version bindings and capture paths. It authorizes exactly one acquisition, then?only after immutable Artifact-API freezing?exactly one Confirmation score pass and one independent replay audit. No Development rerun, refit, threshold selection, retry, Review, Decision, Delivery or status change is authorized.

## Frozen scientific identity

- Candidate `40f0e0e87bb1aff6c999c9c68937294578acb047081eb04c336eb4164fdea25e`.
- Evidence Packet `4f7462c159ca4db7372affac41cf6dd6bc8c5acc4d2131c6c0ee3db8d5274228`.
- Program `f81e3bef778346c142154def15e20c78a009cfddeb0d61c79d54dd9d76237c4a`.
- Independent auditor `f68122cb45f92fb8a85069436c4b55abe3ac89872ae6dd340ed76d617fe153e7`.
- Config `a46a9b5196226705a5fcea4d0c4e0dc50c5214529ec1b229f581c1b447c8a0c6`.
- Test `9a631beea14c1345554cb4ac936d99150496616d1f8d0f11a0a62462799bbc7`.
- Implementation Audit `75669030459de0a33f88b75b66c17e8e965b47524b1597fb73cbe2704f680c7a`.
- Acquisition program `cf87ec4994081b4516695806b471daf75e923fe511d0b67d05b4ab126d34e836`.
- v020 base program `67ac151b6817d6619f915aad581da6c70f9ecdafeb780d87e31816c36009de92`.
- v020 base auditor `2f42878764989288ee44a68d287af2cccfb2e25f72f7eb2fde40e9d81a898607`.
- v012 base `a29b8aace75bf5505620fab71c982e296e045cb1590a20a5a9c19a63c233d78d`.
- Frozen seven-model bundle `8ff9c2cc3ec1ade5aa404323264738800a909c7690d3b867ea48e6fb68fa56f7`.
- v021 Result `74437810a222a5f59cbc48789aa20d4b12847bddd6203c8c60a9c0ed008136f5`.
- v021 Promotion Audit `183cf86a029e5b3d88f8dac406605cd3c2287eca1d08f49e77de99055204e740`.

All 39 pre-execution files in `experiment_v022/artifacts/` are current immutable copies. They contain the complete selected Development data, raw predictions, model, captures, audit, primary sources, promotion judgment and v021 failed-acquisition evidence.

## Inherited Development result

Candidate AUC `0.9408656005`; duplicated-absolute AUC `0.9251839315`; delta `+0.0156816690`; task-bootstrap 95% `[+0.0041492512,+0.0253812488]`; seven of seven gates; seven models and 2,464 scores replayed with zero error. This evidence is inherited, not rerun.

## Fixed acquisition

Interpreter: `D:\Desktop\crl\crl_agent_v3\.venv\python.exe`.
Runner: `D:\Desktop\crl\crl_agent_v3\tools\run_local_experiment.py`.

- capture: `D:\Desktop\crl\20260722_1550_run01\experiment_v022\captures\confirmation_acquire_001`
- cwd: `D:\Desktop\crl\20260722_1550_run01\experiment_v022\artifacts`
- work root: `D:\Desktop\crl\20260722_1550_run01\experiment_v022\work\confirmation_acquire_001`
- output: `D:\Desktop\crl\20260722_1550_run01\experiment_v022\confirmation_acquire_output_001`
- payload argv:
  `D:\Desktop\crl\crl_agent_v3\.venv\python.exe D:\Desktop\crl\20260722_1550_run01\experiment_v022\artifacts\acquire.py --phase confirmation --config D:\Desktop\crl\20260722_1550_run01\experiment_v022\artifacts\config.json --output-dir D:\Desktop\crl\20260722_1550_run01\experiment_v022\confirmation_acquire_output_001 --work-root D:\Desktop\crl\20260722_1550_run01\experiment_v022\work\confirmation_acquire_001`
- declared outputs: `dataset.jsonl`, `manifest.json`.

The repository is `https://github.com/few-sh/terminal-wrench.git`, commit `d8a29613235a0ef56a8b70b3142626a533da28c2`, selector SHA-256 first byte modulo 4 equals bucket 3. The output manifest must bind exact commit, bucket, config, dataset, task IDs and source hashes. On success, dataset, manifest and three capture files are immediately copied through the Artifact API. Only those copies may be scored.

## Fixed Confirmation scoring

- capture: `D:\Desktop\crl\20260722_1550_run01\experiment_v022\captures\confirmation_eval_001`
- cwd: frozen artifact directory
- output: `D:\Desktop\crl\20260722_1550_run01\experiment_v022\confirmation_output_001`
- payload argv:
  `D:\Desktop\crl\crl_agent_v3\.venv\python.exe D:\Desktop\crl\20260722_1550_run01\experiment_v022\artifacts\program.py --phase confirmation --config D:\Desktop\crl\20260722_1550_run01\experiment_v022\artifacts\config.json --dataset D:\Desktop\crl\20260722_1550_run01\experiment_v022\artifacts\confirmation_dataset.jsonl --base-module D:\Desktop\crl\20260722_1550_run01\experiment_v022\artifacts\base_v012.py --output-dir D:\Desktop\crl\20260722_1550_run01\experiment_v022\confirmation_output_001 --model D:\Desktop\crl\20260722_1550_run01\experiment_v022\artifacts\dev_model.joblib --input-manifest D:\Desktop\crl\20260722_1550_run01\experiment_v022\artifacts\confirmation_manifest.json`
- declared outputs: `raw_predictions.jsonl`, `reference_records.jsonl`, `summary.json`.

The seven serialized models, seven validation thresholds and Development strongest comparator `duplicated_absolute` are immutable. The scoring path may not call fit, choose thresholds, remove tasks or change gates.

## Fixed independent audit

Only after scoring exit 0 and all outputs exist:

- capture: `D:\Desktop\crl\20260722_1550_run01\experiment_v022\captures\confirmation_audit_001`
- cwd: frozen artifact directory
- output: `D:\Desktop\crl\20260722_1550_run01\experiment_v022\confirmation_audit_output_001\report.json`
- payload argv:
  `D:\Desktop\crl\crl_agent_v3\.venv\python.exe D:\Desktop\crl\20260722_1550_run01\experiment_v022\artifacts\audit.py --config D:\Desktop\crl\20260722_1550_run01\experiment_v022\artifacts\config.json --dataset D:\Desktop\crl\20260722_1550_run01\experiment_v022\artifacts\confirmation_dataset.jsonl --base-module D:\Desktop\crl\20260722_1550_run01\experiment_v022\artifacts\base_v012.py --raw-predictions D:\Desktop\crl\20260722_1550_run01\experiment_v022\confirmation_output_001\raw_predictions.jsonl --summary D:\Desktop\crl\20260722_1550_run01\experiment_v022\confirmation_output_001\summary.json --reference-records D:\Desktop\crl\20260722_1550_run01\experiment_v022\confirmation_output_001\reference_records.jsonl --model D:\Desktop\crl\20260722_1550_run01\experiment_v022\artifacts\dev_model.joblib --report D:\Desktop\crl\20260722_1550_run01\experiment_v022\confirmation_audit_output_001\report.json`.

Audit support requires `AUDIT_OK`, zero errors, all raw rows, all eligible references, seven replayed models, exact score/metric agreement within `1e-12`, current hashes and zero Development-task overlap.

## Conjunctive scientific gates

Candidate AUC >=0.88; TPR@5%FPR >=0.40; frozen-threshold FPR <=0.08; frozen-threshold TPR >=0.35; Candidate AUC strictly exceeds all six comparators; Candidate-minus-duplicated-absolute AUC >0 with task-cluster bootstrap lower bound >=0; and all acquisition, reference, task-disjointness, model and audit integrity conditions pass.

The main Codex must then read the entire summary, every raw row, all comparators, all task/model/category slices, corrections, regressions, false positives, false negatives and bounded original source trajectories. Booleans do not authorize Review. Only a positive written Confirmation Audit permits freezing a complete Review Packet; no subagent is allowed before that packet exists.
