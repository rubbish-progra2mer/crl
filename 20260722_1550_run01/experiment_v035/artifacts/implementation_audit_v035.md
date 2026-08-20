# Main-Codex Implementation Audit v035

Status: `PREFREEZE_ACCEPTED_FOR_ONE_DEVELOPMENT_EXECUTION`.

The current main Codex personally inspected `program.py`, `audit.py`,
`config.json`, `test_program.py`, `acquire_confirmation.py` and the shared
capture runner. No subagent was used.

## Scientific-to-code trace

The implementation matches the Candidate:

- `extract_call`, `action_fields` and `flatten_value` deterministically parse
  call mode, tool and recursive argument paths;
- `build_difference` removes exactly shared canonical fields and retains only
  candidate-specific fields;
- the non-call fallback uses word/punctuation-token opcodes, not character
  similarity;
- `implicated_contracts` selects only exact tool-name matches, with an
  explicitly marked system-message fallback when the dataset supplies no
  separate function structure;
- `build_prompt_records` creates exactly eight prompts per pair: two SDEJ,
  two full-pair, two evidence-free-difference and two pointwise prompts;
- `score_prompts` reads bare next-token `A`/`B` or `Yes`/`No` probabilities
  from the same frozen Qwen3-0.6B;
- `pair_aligned` averages aligned forward/reverse probabilities;
- no supervised fit, source-specific threshold, external retrieval, tool
  execution or generated rationale occurs;
- `summarize` names the strongest mandatory Development control before any
  Confirmation and stores it in `frozen_state.json`;
- the bootstrap samples source/task clusters with replacement within source
  using fixed seed `3501`.

## Independent audit path

`audit.py` imports no implementation module. It independently loads and hashes
the datasets and model, rebuilds all projections and prompts, replays all
next-token probabilities, rebuilds every row and summary metric, and compares
numeric values within `1e-6`. It reads the captured raw and summary files only
after reconstructing the expected values.

The audit shares the frozen mathematical specification with the scientific
program, as required for reproduction, but has a separate entry point and
performs no call into `program.py`.

## Prefreeze commands and evidence

The first five-test run exited `1` because a test exposed that character-level
`SequenceMatcher` reduced `ask` versus `open` to partial character spans. No
Development model score or output existed. Before freeze, the main Codex
changed only the non-call fallback and Candidate wording to
word/punctuation-token spans.

The corrected command, under
`D:\Desktop\crl\20260722_1550_run01\implementation_v035`, was:

```text
D:\Desktop\crl\crl_agent_v3\.venv\python.exe -m unittest -v test_program.py
```

Exit code: `0`. Result: `5/5` tests passed.

AST parsing of `program.py`, `audit.py`, `test_program.py`,
`acquire_confirmation.py` and `run_local_experiment.py` exited `0`.
`program.py --help`, `audit.py --help` and
`acquire_confirmation.py --help` each exited `0`.

The static Development construction command loaded no causal model and
produced no preference score. It exited `0` and found:

- 315 rows and 195 source/task clusters;
- 2,520 prompts, exactly eight per row;
- prompt tokens: minimum 103, median 607, mean 757.052778, maximum 8,072;
- zero prompt-cap violations against 12,288;
- zero rows with an empty difference;
- source rows/clusters: BFCL 111/52, GTA 118/92, ToolTalk 86/51;
- no `__pycache__` directory or `.pyc` file.

The tokenizer-only token check exited `0` and verified:

- `A` -> token 32;
- `B` -> token 33;
- `Yes` -> token 9454;
- `No` -> token 2753.

## Frozen executable hashes

| File | Bytes | SHA-256 |
|---|---:|---|
| `program.py` | 35,344 | `f3a1fa0ac4b69daa4a629701f223ff595ffa430014c25755142cffd536e0ac64` |
| `audit.py` | 37,469 | `591a89bad636f5bfd8e86d487f9eaf014b0c604f9a838a03ea5f1fb19525f2a8` |
| `config.json` | 1,716 | `f1ad651c0804422e534ba53fb87d2a6295f633f17659d730b38edc68e50e6d92` |
| `test_program.py` | 2,572 | `27fa74d6b278c57e872f0ba868084eebb3866a084eab4ad5df6aff2914eb0371` |
| `acquire_confirmation.py` | 2,009 | `a26821f7df2554490da04469d088abc9ebeeeadd1e4a0e941136062eaa3d6c14` |
| `run_local_experiment.py` | 4,338 | `410a620d0734613036f4fea4bc017c0cd1d0de293e1a3d4577c75eec584eaa4a` |

## Confirmation and side-effect boundary

`sources_v035/prmbench_ToolSandbox.json` does not exist. A recursive Run check
found no ToolSandbox data file. The program and auditor contain no networking
code. `acquire_confirmation.py` is the only network-capable implementation
file and has not been executed; it refuses to overwrite an existing output.

The implementation is accepted only for the one frozen Development execution.
This audit does not authorize Confirmation, Review, Delivery or a system-state
change.

