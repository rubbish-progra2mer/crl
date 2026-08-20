# Confirmation Acquisition Failure v021

Disposition: `EXECUTION_ONLY_FAILURE_BEFORE_CONFIRMATION_BYTES`.

- The single frozen acquisition payload ran from `experiment_v021/artifacts/` and exited `1` after `7.546716500000912` seconds.
- Execution capture SHA-256: `cdb05c3867ae73b5df2f4b3a6b275b36326387fb3e4883449dfe2e51ac069195`.
- Empty stdout SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
- Stderr SHA-256: `91f099fcd2c2662796c490d11181b2c45e88943e24e775b180f85a8e562d5d00`.
- The failure was Git exit `128` during the pinned `fetch --depth=1 --filter=blob:none` call, before sparse metadata checkout, trajectory parsing, dataset construction or manifest construction.
- Runner output facts record both declared files absent after execution: no `dataset.jsonl` and no `manifest.json`.
- The failed work tree contains only repository-control metadata; no checked-out task or trajectory file exists and `.git/FETCH_HEAD` has zero bytes.
- A subsequent read-only diagnostic `git ls-remote https://github.com/few-sh/terminal-wrench.git HEAD` exited `0` and returned `d8a29613235a0ef56a8b70b3142626a533da28c2`, the exact pinned commit. It did not acquire task metadata, trajectory bytes or Candidate outcomes.

No Confirmation row, label, metric, prediction or model score exists. v021 must not retry or overwrite this capture. The same scientific Candidate may proceed only as a new execution-only version with a new frozen Candidate/Evidence binding and one new acquisition contract.
