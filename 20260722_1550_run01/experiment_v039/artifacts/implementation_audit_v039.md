# Main-Codex Implementation Audit v039

Status: `PREFREEZE_ACCEPTED_FOR_ONE_DEVELOPMENT_EXECUTION`.

The main Codex personally compared v039 with frozen v038. No subagent was used.

## Byte identity and only correction

These files are byte-identical to v038:

| File | SHA-256 |
|---|---|
| `program.py` | `c29395c7072b177b64b833aed0c8e253d6d71ff70aa4cc564cb656a94081ef17` |
| `audit.py` | `abfcb551889d3e0051feee788be45192b80bbfd4bc344159ddc97e62d2dcb0a6` |
| `run_local_experiment.py` | `2a888a00cd9845f848fa2da8f572c105a55b5dbf7ca518dac8cd9988131abb37` |
| `test_program.py` | `f98af7ecd9424b5c60b3372e528a96bfd6a7d6941b150c84cc10970c11d29d45` |

The only execution correction is in the Plan and eventual argv: four exact
output files replace the v038 output-directory argument. `config.json` changes
only experiment identity, Candidate label and Candidate-document SHA.
Confirmation acquisition changes only its version guard/User-Agent. Freeze
paths and predecessor bindings change to v039/v038.

No action parsing, contract selection, token alignment, context, likelihood,
control, bootstrap, gate, model, data, Confirmation carrier or claim changes.

## Verification

With shared Python 3.11.15 and `PYTHONDONTWRITEBYTECODE=1`:

- six unit tests passed, exit `0`;
- six Python files passed AST parsing, exit `0`;
- a no-data exact-output smoke used a missing capture parent and one expected
  output file; runner and child both exited `0`;
- the output was captured with SHA-256
  `4f44ad1fc91ebb29132d1df8fe26842978f5c1701d1b024bf33317515fedb8d7`;
- smoke execution record:
  `12dd47ea7d33f53bda03bb583758a6de194d6b8a3b9a508ff30f957e2d468c0d`;
- the temporary directory was precisely removed;
- Run `.pyc` count and ToolSandbox file count remain zero.

## Executable hashes

| File | Bytes | SHA-256 |
|---|---:|---|
| `program.py` | 27,605 | `c29395c7072b177b64b833aed0c8e253d6d71ff70aa4cc564cb656a94081ef17` |
| `audit.py` | 29,749 | `abfcb551889d3e0051feee788be45192b80bbfd4bc344159ddc97e62d2dcb0a6` |
| `run_local_experiment.py` | 4,350 | `2a888a00cd9845f848fa2da8f572c105a55b5dbf7ca518dac8cd9988131abb37` |
| `test_program.py` | 2,969 | `f98af7ecd9424b5c60b3372e528a96bfd6a7d6941b150c84cc10970c11d29d45` |
| `config.json` | 1,656 | `19571514487d3a24a8577427886ff8fa0f27080ffb85b6aa0f9c8614ea3157bc` |
| `acquire_confirmation.py` | 2,009 | `0ac0965c72796705b13569dcf2cf440ad03d7b1f8c1bd2a69b39dc4e1fa67df6` |
| `freeze_artifacts.py` | 5,271 | `15b801981aa2a4f01dc8bfa840d61b40b88eeecf21ba5e5d1500c6a71f8c43f4` |

This audit authorizes one frozen v039 Development capture and then, only after
exit `0`, one independent replay. It does not authorize Confirmation or Review.
