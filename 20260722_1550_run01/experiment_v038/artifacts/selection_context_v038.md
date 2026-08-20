# v038 Selection Context

v037 did not launch its scientific subprocess. The frozen capture runner exited
`1` because `experiment_v037/captures` did not exist and it called
`capture_dir.mkdir()` without parent creation. No v037 model forward, metric or
Development output exists.

v038 is an execution-only successor. It inherits the frozen v037 ECDS
computation, exposed Development data, model, controls, bootstrap, gates,
untouched ToolSandbox boundary and claim ceiling byte-for-byte. No new Card
query, paper search, feature screen, metric inspection or scientific selection
is performed.

The only execution correction is for the frozen capture runner to create the
capture path with `parents=True`. Version guards, document hashes and freeze
paths change only as required to bind v038. The shared environment is not
mutated.
