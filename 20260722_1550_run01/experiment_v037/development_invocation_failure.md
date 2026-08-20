# v037 Development Invocation Failure

Observed at: `2026-07-26T03:47:41.6108948+08:00`.

The main Codex invoked the frozen `run_local_experiment.py` exactly as bound by
`plan.md`. The runner exited `1` before launching the scientific subprocess:

```text
FileNotFoundError: [WinError 3] 系统找不到指定的路径。:
'D:\Desktop\crl\20260722_1550_run01\experiment_v037\captures\dev_001'
```

Cause: the frozen runner calls `capture_dir.mkdir()` without `parents=True`,
while the parent `experiment_v037/captures` did not exist.

Post-failure filesystem checks exited `0` and showed:

- `CAPTURES_PARENT_EXISTS=False`;
- `DEV_CAPTURE_EXISTS=False`;
- `DEV_OUTPUT_EXISTS=False`;
- ToolSandbox file count `0`;
- frozen Artifact Manifest unchanged at
  `d434f3bcc36593ab9b94a1c4d8470dd56c6e9ef2c76ed0ec188e3c88c566a18c`;
- frozen Plan unchanged at
  `14992eda715fed3b543c5a30d979c99fb40d81178ceede2482085b7cb5cdc732`.

No Development subprocess, model forward, raw prediction, summary, environment
capture, frozen state or scientific metric was produced. v037 is not retried or
overwritten. An execution-only successor must correct capture-parent creation
without changing the scientific Candidate.
