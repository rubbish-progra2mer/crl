# v027 Preparation Failure

Recorded at: `2026-07-25T19:52:32.0791898+08:00`.

## Actual command outcome

- Scope: deterministic post-Plan directory preparation only.
- Working directory: `D:\Desktop\crl\crl_agent_v3`.
- Exit code: `1`.
- First failing operation: `New-Item -ItemType Directory -LiteralPath <path>`.
- PowerShell error: `A parameter cannot be found that matches parameter name 'LiteralPath'.`
- Cause: Windows PowerShell 5.1 `New-Item` accepts `-Path`, not `-LiteralPath`.
- Subsequent copy and verification operations failed because neither destination directory existed.

## Byte-state verification after failure

The following read-only verification command exited `0`:

```powershell
$exp='D:\Desktop\crl\20260722_1550_run01\experiment_v027'
Test-Path -LiteralPath "$exp\captures"
Test-Path -LiteralPath "$exp\model_cross"
Test-Path -LiteralPath "$exp\dev_output_001"
Test-Path -LiteralPath "$exp\dev_audit_output_001"
```

All four results were `false`. The 33 frozen preexecution artifacts still numbered 33 and totaled 97,323,644 bytes.

No model was loaded, no field score or metric was computed, no Development capture was created, and no Confirmation byte was acquired or read.

## Disposition

The publish-once v027 Plan forbids a same-version retry after a nonzero execution. v027 is therefore frozen as `NO_GO_FOR_SAME_VERSION_RETRY_PREPARATION_FAILURE`. The same scientific identity may advance only as an execution-only v028 correction whose sole change is using `New-Item -Path` for the two parent directories.

