# v039 Selection Context

v038 launched the unchanged ECDS program and produced four output files, but
the runner exited `1` in post-execution capture because the invocation declared
the output directory as a file. No execution record or raw stream was saved, so
v038 is not a formal Development result.

v039 is an execution-only successor. Program, auditor, runner, tests, data,
model, method, controls, bootstrap, gates, untouched ToolSandbox boundary and
claim ceiling are inherited unchanged. No research query, feature screen,
metric-driven method change or environment mutation occurs.

The only correction is in the frozen Experiment Plan and actual runner argv:
declare `raw_predictions.jsonl`, `summary.json`, `environment.json` and
`frozen_state.json` as four exact `--output` files instead of declaring their
parent directory.
