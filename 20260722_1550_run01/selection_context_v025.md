# Selection Context v025

v025 is an execution-only correction of v024. It carries the byte-identical VIAF Candidate, Evidence Packet, Problem and Research Map. It introduces no new kernel, Claim, comparator, threshold, gate, bucket, task selection, literature judgment or scientific inspection.

v024's sole planned `dev_acquire_001` invocation failed in frozen `run_local_experiment.py` at `capture_dir.mkdir()` because `experiment_v024/captures` did not exist. The payload `acquire.py` was never started. Read-only checks found no capture, output or work directory. Therefore bucket 1 Development metadata/labels/trajectories and bucket 0 Confirmation metadata/labels/trajectories remain byte-untouched.

The only v025 change is execution preparation: after its publish-once Plan is frozen, the main Codex will create the empty `experiment_v025/captures` and `experiment_v025/work` parent directories, verify the unique attempt/output children remain absent, and then invoke exactly one acquisition. This does not change the frozen runner or scientific computation. Same-version retry remains forbidden.

Buckets 2+3 remain exposed selection context only. The exact unlabeled substrate result remains 1,760/3,071 anchored rows (57.31%), median first-anchor relative position `0.177521`, interquartile range `[0.0769231, 0.375]`; it used no target, model or method metric.
