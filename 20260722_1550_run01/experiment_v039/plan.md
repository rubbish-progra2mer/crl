# Experiment Plan v039

Status: `FROZEN_BEFORE_DEVELOPMENT`.

Created after Artifact freeze and before any v039 Development execution. No
subagent was used.

## Frozen identity

- Candidate:
  `84f515dbc6f2b347aad4078364ac711c03ca6eb2577b0797d9e3636a25058720`;
- Evidence Packet:
  `d0f65faf280a7691fd507355c322fd440f5cc892a849a6202d464a3c9d916f29`;
- Artifact Manifest:
  `c773bcb87ce03190203b657cdff33a4e686e752d85563d5795d6e2770c5f87de`;
- scientific program:
  `c29395c7072b177b64b833aed0c8e253d6d71ff70aa4cc564cb656a94081ef17`;
- model manifest:
  `9518287b603d6bc25ef7cd3f98764db94a633f360faa68f57ee80ceb8cf72034`;
- Python:
  `D:\Desktop\crl\crl_agent_v3\.venv\python.exe`.

The Artifact Manifest binds 33 local records, seven external model records,
40 total records and 1,529,904,186 bytes.

## One Development capture

The frozen runner may create only `captures/dev_001`. The program receives new
directory `dev_output_001`. Runner `--output` declares exactly:

1. `dev_output_001/raw_predictions.jsonl`;
2. `dev_output_001/summary.json`;
3. `dev_output_001/environment.json`;
4. `dev_output_001/frozen_state.json`.

All four files and the capture path must be absent before execution. Inputs are
the frozen Manifest, Candidate, Evidence Packet, program, config, model
manifest, GTA 118, BFCL 111 and ToolTalk 86. Expected total is 315 rows, 195
clusters and 1,260 sequences. No v038 output is passed to the program.

No retry or overwrite is permitted.

## One independent replay

Only primary exit `0` permits one audit capture at
`captures/dev_audit_001`. Runner output is the exact file
`dev_audit_output_001/report.json`. The frozen auditor must independently
recompute all rows, sequences, masks, log probabilities, metrics and bootstrap
values and match the primary raw JSONL and summary within `1e-6`.

## Unchanged gates

All eight v037 ECDS gates remain conjunctive: accuracy `>=0.65`; strongest
control delta `>=0.025`; bootstrap lower bound `>0`; every source accuracy
`>=0.55`; all source deltas nonnegative with at least two positive; superiority
to `full_diff_ll`, `full_action_gain` and `null_diff_ll`; audit success.

The main Codex must inspect raw outputs and write the Promotion Audit. Only all
gates plus a positive audit permits acquiring untouched ToolSandbox. Otherwise
v039 closes without Confirmation or Reviewer and the same Run advances to the
user's final allowed v040.
