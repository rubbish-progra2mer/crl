# ToolPRMBench Data (v3)

Each evaluation file is a JSON list of step-level test cases. A case contains the
interaction history, a correct action (`action_chosen`), a plausible but
incorrect alternative (`action_rejected`), and the relevant tool metadata
(`functions`). A PRM/judge is correct on a case when it prefers `action_chosen`
over `action_rejected`.

## Evaluation splits

| File | Source benchmark | # cases |
| --- | --- | --- |
| `prmbench_GTA.json` | GTA | 118 |
| `prmbench_bfcl.json` | BFCL | 111 |
| `prmbench_tooltalk.json` | ToolTalk | 86 |
| `prmbench_ToolSandbox.json` | ToolSandbox | 130 |

Common fields across every split:

- `history` — list of chat turns (`role` / `content`) up to the decision point.
- `action_chosen` — the correct next action.
- `action_rejected` — a plausible but incorrect next action.
- `functions` — available tool/function specifications (may be `null`).

Some splits carry extra provenance fields, e.g. `error type`, `rationale`,
`milestones_*` (ToolSandbox) or `model_name`, `test_category`, `possible_answer`
(BFCL). Evaluators ignore fields they do not need.

## Training splits

`prmbench_bfcl_train.json` and `prmbench_ToolSandbox_train.json` are JSON-Lines
files (one record per line) used for ToolPRM training. They are **not** consumed
by the evaluation scripts.

## Overriding the data location

Evaluators read from this directory by default. Point them elsewhere with either
`--data_dir /path/to/data` or the `TOOLPRMBENCH_DATA_DIR` environment variable.
