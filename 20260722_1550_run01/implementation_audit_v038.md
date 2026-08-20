# Main-Codex Implementation Audit v038

Status: `PREFREEZE_ACCEPTED_FOR_ONE_DEVELOPMENT_EXECUTION`.

The main Codex personally compared v038 against the frozen v037 artifacts. No
subagent was used.

## Exact delta

The scientific executables are byte-identical to v037:

| File | SHA-256 |
|---|---|
| `program.py` | `c29395c7072b177b64b833aed0c8e253d6d71ff70aa4cc564cb656a94081ef17` |
| `audit.py` | `abfcb551889d3e0051feee788be45192b80bbfd4bc344159ddc97e62d2dcb0a6` |
| `test_program.py` | `f98af7ecd9424b5c60b3372e528a96bfd6a7d6941b150c84cc10970c11d29d45` |

`git diff --no-index` showed one runner hunk:

```text
-        capture_dir.mkdir()
+        capture_dir.mkdir(parents=True)
```

The diff command returned its normal difference exit code `1`; the displayed
hunk above was the only runner difference.

`config.json` changes only experiment ID, Candidate label and Candidate-document
SHA. `acquire_confirmation.py` changes only its version guard and User-Agent.
`freeze_artifacts.py` changes versioned source/target paths and binds the v037
failure lineage. Data, model, method, masks, contexts, controls, bootstrap,
gates and claim ceiling do not change.

## Verification

Under the shared Python 3.11.15 environment with
`PYTHONDONTWRITEBYTECODE=1`:

- six inherited unit tests passed, exit `0`;
- AST parsing of all six Python files passed, exit `0`;
- a no-data runner smoke targeted a missing nested capture parent, invoked only
  `python -c` and exited `0`;
- the smoke child exited `0`;
- its execution record SHA-256 was
  `b91ea93a8efe20013d796eef9ee0dda3178925c77eec555126f9d8d1227a6e9e`;
- the temporary smoke directory was then precisely removed;
- no `.pyc` exists in the Run;
- ToolSandbox remains absent.

## v038 executable hashes

| File | Bytes | SHA-256 |
|---|---:|---|
| `program.py` | 27,605 | `c29395c7072b177b64b833aed0c8e253d6d71ff70aa4cc564cb656a94081ef17` |
| `audit.py` | 29,749 | `abfcb551889d3e0051feee788be45192b80bbfd4bc344159ddc97e62d2dcb0a6` |
| `config.json` | 1,664 | `86186d37f1fcfce3b9f1656555a416f2abe2ec4796bf88d2bbc9381f97092726` |
| `test_program.py` | 2,969 | `f98af7ecd9424b5c60b3372e528a96bfd6a7d6941b150c84cc10970c11d29d45` |
| `run_local_experiment.py` | 4,350 | `2a888a00cd9845f848fa2da8f572c105a55b5dbf7ca518dac8cd9988131abb37` |
| `acquire_confirmation.py` | 2,009 | `1848dbcc808ce2f2def9b6a945d9b3a264bbf626392840acf8e037791a2cf4ae` |
| `freeze_artifacts.py` | 4,933 | `8248a29682c37b107cd93cdc829f45c9d13b850e12e413f27ed4f9e9db2ebe97` |

This audit authorizes one frozen v038 Development capture and, only after exit
`0`, one frozen independent replay. It does not authorize Confirmation, Review,
Delivery or a system-state transition.
