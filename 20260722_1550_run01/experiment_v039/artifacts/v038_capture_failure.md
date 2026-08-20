# v038 Development Capture Failure

Observed at: `2026-07-26T03:56:48.3734490+08:00`.

The frozen runner launched the scientific subprocess, but its post-execution
output capture treated `dev_output_001` as a file:

```text
PermissionError: [Errno 13] Permission denied:
'D:\Desktop\crl\20260722_1550_run01\experiment_v038\dev_output_001'
```

Outer runner exit code: `1`.

The capture directory exists but contains zero files. Therefore exact child
exit code, duration, stdout and stderr were not persisted and no
`execution.json` exists.

The completed output directory is frozen in place:

| File | Bytes | SHA-256 |
|---|---:|---|
| `environment.json` | 479 | `274b27ca22ac925ef76836f0d5cf21f92f1bb41cd73f1fea0647860c53e2176c` |
| `frozen_state.json` | 468 | `dc1fecdce3eba91bc65acfae9bacdc9a55aa827eed4212d3980714272f500fab` |
| `raw_predictions.jsonl` | 715,850 | `73986d3bdd8449952abd9410aa962b0edf39a2b8a908498108f31e58b7ffe389` |
| `summary.json` | 1,628 | `7b9189ebe772a13fff24295ff44f972e458beb69c6d4334e3c214c1c334cc647` |

The summary visibly reports ECDS accuracy `0.5396825396825397`, strongest
control `full_action_gain` at `0.4984126984126984`, delta
`0.041269841269841234`, bootstrap lower bound
`-0.0033444816053511683`, BFCL ECDS `0.43243243243243246` and ToolTalk ECDS
`0.45348837209302323`. These bytes are disclosed but are not accepted as a
formal Development capture because execution metadata and raw streams are
missing.

No independent replay is permitted under the v038 Plan. ToolSandbox remains
absent and unread. v038 is not retried or overwritten.
