# Experiment Plan v038

Status: `FROZEN_BEFORE_DEVELOPMENT`.

Created after v038 Artifact freeze and before any v038 Development execution.
No subagent was used.

## Frozen identity

- v038 Candidate:
  `19b7ac97c4b1e3845410ff67101aa254436d526bd8d8c77817d0e2d176f6d2ef`;
- v038 Evidence Packet:
  `0cf9e582c737931879b6c8892ae5478ac9c393cf0710cba85645ff25f5d196d3`;
- v038 Artifact Manifest:
  `b1bfafc8c988e9f02479834f1c1a1a25000f55d587ff91bb8b42a45ec45ebb29`;
- inherited v037 scientific program:
  `c29395c7072b177b64b833aed0c8e253d6d71ff70aa4cc564cb656a94081ef17`;
- model manifest:
  `9518287b603d6bc25ef7cd3f98764db94a633f360faa68f57ee80ceb8cf72034`;
- shared Python:
  `D:\Desktop\crl\crl_agent_v3\.venv\python.exe`;
- frozen model snapshot:
  `C:\Users\g\.cache\huggingface\hub\models--Qwen--Qwen3-0.6B\snapshots\c1899de289a04d12100db370d81485cdf75e47ca`.

The Artifact Manifest binds 29 local records plus seven external model records,
36 records and 1,529,190,272 bytes total.

## Single Development capture

Exactly one primary capture is permitted:

- `captures/dev_001`;
- output `dev_output_001`;
- frozen `development` phase;
- GTA 118, BFCL 111, ToolTalk 86;
- expected 315 rows, 195 clusters and 1,260 sequences;
- `PYTHONDONTWRITEBYTECODE=1`.

The frozen v038 runner must create the missing capture parent, invoke the frozen
program from `experiment_v038/artifacts`, and bind exact inputs, outputs, argv,
cwd, stdout/stderr, exit code and duration. No retry or overwrite is allowed.

If the primary capture exits `0`, exactly one frozen `audit.py` replay is
permitted under `captures/dev_audit_001`, writing only
`dev_audit_output_001/report.json`. It must independently recompute every row,
sequence, mask, log probability, metric and source-cluster bootstrap and match
within `1e-6`.

## Unchanged conjunctive gates

1. ECDS accuracy at least `0.65`;
2. delta over strongest control at least `0.025`;
3. bootstrap 95% lower delta bound greater than `0`;
4. every source accuracy at least `0.55`;
5. every source delta nonnegative and at least two positive;
6. ECDS strictly exceeds `full_diff_ll` and `full_action_gain`;
7. ECDS strictly exceeds `null_diff_ll`;
8. independent replay passes within `1e-6`.

The main Codex must personally inspect the raw output and write a Promotion
Audit. Only all eight gates plus a positive audit permits the one-shot frozen
acquisition of the absent 130-row ToolSandbox. Otherwise v038 closes, no
Confirmation or Reviewer is created, and the same Run advances without
overwriting any frozen byte.
