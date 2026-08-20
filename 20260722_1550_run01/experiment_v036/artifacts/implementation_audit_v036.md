# Main-Codex Implementation Audit v036

Status: `PREFREEZE_ACCEPTED_FOR_ONE_DEVELOPMENT_EXECUTION`.

The main Codex personally compared v036 against the frozen v035 artifacts. No
subagent was used.

## Exact executable delta

`git diff --no-index` showed exactly one scientific-program hunk and the same
one audit hunk:

```text
- torch_dtype=torch.float16,
- device_map={"": "cuda"},
- )
+ dtype=torch.float16,
+ ).to("cuda")
```

`config.json` changes only `experiment_id` from `v035` to `v036` and the
Candidate-document SHA. `test_program.py` and `run_local_experiment.py` are
byte-identical to v035. `acquire_confirmation.py` changes only its version
guard and User-Agent.

No action parsing, difference projection, evidence selection, prompt, token
ID, model revision, data hash, control, bootstrap, gate or Claim changed.

## Prefreeze verification

Under `D:\Desktop\crl\20260722_1550_run01\implementation_v036` with
`PYTHONDONTWRITEBYTECODE=1`:

- five unit tests: exit `0`, `5/5` passed;
- AST parsing of all five Python files: exit `0`;
- no `__pycache__` or `.pyc` exists.

A synthetic loader smoke used no ToolPRMBench row and produced no scientific
metric. It executed the exact v036 load operation and one synthetic forward
pass:

```text
AutoModelForCausalLM.from_pretrained(
    frozen_snapshot,
    local_files_only=True,
    trust_remote_code=False,
    dtype=torch.float16,
).to("cuda")
```

Exit code: `0`. Observed:

- parameter device `cuda:0`;
- parameter dtype `torch.float16`;
- output shape `[1, 1, 151936]`;
- all logits finite.

The shared environment was not changed and `accelerate` was not installed.

## Executable hashes

| File | Bytes | SHA-256 |
|---|---:|---|
| `program.py` | 35,316 | `ac23300356663662e9529f0ec5feb8440447c51fdf1bd12d6e9927bc99f14aba` |
| `audit.py` | 37,441 | `710fdd75f683f41f81c5e402628ce04407889ec547d141d78252c065810f44e3` |
| `config.json` | 1,716 | `ce8ed62cdbc68753226aa07f9c417de60c75a47a115785d1444bc38366001c26` |
| `test_program.py` | 2,572 | `27fa74d6b278c57e872f0ba868084eebb3866a084eab4ad5df6aff2914eb0371` |
| `acquire_confirmation.py` | 2,009 | `61bac6cc9f5af4f93b07f19fb3bdf5dd46eec0fa3457f469b6ad4804e5b2df60` |
| `run_local_experiment.py` | 4,338 | `410a620d0734613036f4fea4bc017c0cd1d0de293e1a3d4577c75eec584eaa4a` |

ToolSandbox remains absent and unread. This audit authorizes only one frozen
v036 Development execution, not Confirmation, Review, Delivery or a status
transition.

