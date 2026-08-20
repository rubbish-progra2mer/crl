# Experiment Plan v040

Status: `FROZEN_BEFORE_DEVELOPMENT`.

Created after Artifact freeze and before any v040 Development execution. No
subagent was used.

## Frozen identity

- Candidate:
  `aa82bbe9988b7e1824a49a7e4d080c46a3d9e38b833e6d2c396b006f717cc51c`;
- Evidence Packet:
  `287c5628537281805cdb093f785c0002cd13c2880a85ad66bf3b4ed1c8962aa9`;
- Implementation Audit:
  `e980b0a0cef90f45bab24630d7cb87b7541eccf653e176796e4b718ebced6d89`;
- Artifact Manifest:
  `7fed84bdf490775299dc0e26c9e4c8e8080c17e2da58455d58de7c9365b0ea12`;
- config:
  `492a07187e61469c37faf521ee8526bf2db13eeeef41c4a48aab3450c27d1b16`;
- Python:
  `D:\Desktop\crl\crl_agent_v3\.venv\python.exe`.

The Manifest binds 37 files and 131,553,724 bytes.

## One Development capture

The frozen runner may create only `captures/dev_001`. The frozen program runs
phase `development` from `experiment_v040/artifacts` with:

- Candidate, Evidence Packet, config and `base_v012.py`;
- bucket 1--3 datasets and manifests;
- new output directory `dev_output_001`;
- `PYTHONDONTWRITEBYTECODE=1`.

Runner outputs are exactly:

1. `dev_output_001/raw_predictions.jsonl`;
2. `dev_output_001/source_records.jsonl`;
3. `dev_output_001/summary.json`;
4. `dev_output_001/model.joblib`.

Expected structural totals are 4,256 source rows, 228 eligible tasks and 4,072
OOF rows. No retry, overwrite or v026 model reuse is allowed.

## One independent replay

Only primary runner and child exit `0` permits one frozen audit:

- capture: `captures/dev_audit_001`;
- output: exact file `dev_audit_output_001/report.json`;
- inputs: all frozen identity/data bytes plus primary raw, source records,
  summary and model;
- required: `AUDIT_OK`, nine fold bundles, all six methods replayed, maximum
  score/metric/structural error `0`.

## Conjunctive gates

The eight Candidate gates are exactly those in `candidate_v040.md`: AUC
`>=0.88`, TPR@5%FPR `>=0.55`, strongest-control delta `>=0.005`, positive task
bootstrap lower bound, strict superiority to every comparator including CMCD,
all three generator deltas nonnegative, at least two positive generator deltas,
and eligible fraction `>=0.90`.

The independent audit and a positive main-Codex Promotion Audit are additionally
mandatory.

## Conditional bucket-0 Confirmation

Only all Development gates plus positive Promotion Audit permits exactly one
frozen acquisition of hash bucket 0 from Terminal Wrench commit
`d8a29613235a0ef56a8b70b3142626a533da28c2`, recording dataset, manifest,
repository bytes, command capture and environment. The acquisition must occur
after the Development decision; bucket 0 remains absent until then.

The frozen full model bundles, strongest Development comparator and unchanged
SFEC computation then receive one Confirmation capture and one independent
audit. All nine Confirmation gates are conjunctive.

Only positive Confirmation permits a complete frozen formal Review Packet and
three simultaneous fresh leaf Reviewers. If v040 fails before Delivery, no
Reviewer is created and run01 must be set to `PAUSED_BY_USER` with a single
resume point, per the user's cutoff.
