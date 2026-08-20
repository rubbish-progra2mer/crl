# Experiment Plan v037

Status: `FROZEN_BEFORE_DEVELOPMENT`.

Created after Artifact freeze and before any v037 Development execution. No
subagent was used.

## Frozen identity

- Candidate:
  `85a6636225de3465641c185db4725781731fc3d1bc7cc4413c2df63507a4096e`;
- Evidence Packet:
  `c12fba01f2b7d739d92d6df6bd208deee9570e4af2d7c03bc453e268c3101b19`;
- Artifact Manifest:
  `d434f3bcc36593ab9b94a1c4d8470dd56c6e9ef2c76ed0ec188e3c88c566a18c`;
- model manifest:
  `9518287b603d6bc25ef7cd3f98764db94a633f360faa68f57ee80ceb8cf72034`;
- Python:
  `D:\Desktop\crl\crl_agent_v3\.venv\python.exe`;
- model snapshot:
  `C:\Users\g\.cache\huggingface\hub\models--Qwen--Qwen3-0.6B\snapshots\c1899de289a04d12100db370d81485cdf75e47ca`.

The frozen Artifact Manifest contains 30 local artifact records and seven
external model records, 37 total records and 1,529,210,560 bound bytes.

## Development execution

Exactly one primary capture is permitted:

- capture directory: `captures/dev_001`;
- output directory: `dev_output_001`;
- phase: `development`;
- frozen inputs: Artifact Manifest, Candidate, Evidence Packet, program,
  config, model manifest and the three Development JSON files;
- sources: GTA 118, BFCL 111 and ToolTalk 86;
- expected rows/clusters/sequences: 315 / 195 / 1,260;
- `PYTHONDONTWRITEBYTECODE=1`.

The capture runner must invoke the frozen `program.py` from the frozen artifacts
directory. It records exact argv, cwd, input and output facts, stdout/stderr
bytes, exit code and duration. No retry or overwrite is allowed.

If primary execution exits `0`, exactly one independent frozen `audit.py`
replay is permitted:

- capture directory: `captures/dev_audit_001`;
- report directory: `dev_audit_output_001`;
- inputs additionally include the primary raw JSONL, summary and frozen state;
- the audit must independently recompute 315 rows and 1,260 sequences;
- every token mask, hash, log probability, metric and bootstrap value must match
  within `1e-6`.

## Conjunctive Development gates

1. ECDS accuracy at least `0.65`;
2. delta over the strongest mandatory control at least `0.025`;
3. source-cluster bootstrap 95% lower delta bound greater than `0`;
4. every source accuracy at least `0.55`;
5. every source delta nonnegative and at least two source deltas positive;
6. ECDS strictly exceeds `full_diff_ll` and `full_action_gain`;
7. ECDS strictly exceeds `null_diff_ll`;
8. independent replay passes within `1e-6`.

Ties score `0.5`. The strongest control is selected deterministically from
Development and frozen in `frozen_state.json`.

## Promotion boundary

After primary output and audit, the main Codex must personally inspect raw rows,
source results, controls, bootstrap values, truncation, environment capture and
the audit report, then write a Promotion Audit.

Only all eight gates plus a positive Promotion Audit permits running the frozen
one-shot acquisition script for the 130-row ToolSandbox. Otherwise:

- ToolSandbox remains absent and unread;
- no Confirmation, Review Packet, Reviewer, decision or Delivery is created;
- v037 is closed without overwriting frozen bytes;
- the same Run advances to v038.
