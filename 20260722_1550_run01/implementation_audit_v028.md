# Main Codex Implementation Audit v028

Disposition: `APPROVED_FOR_DEVELOPMENT_FREEZE`.

v028 is an execution-only correction. I re-read the v027 source audit and compared the complete v028 implementation against it before any v028 model inference.

## Exact code delta

- `audit.py`, `acquire_confirmation.py` and `test_mfcr.py` are byte-identical to v027.
- `program.py` changes only two emitted `experiment_id` literals from `v027` to `v028`.
- `config.json` changes only `experiment_id` from `v027` to `v028`.
- Candidate, Evidence Packet, Problem and Research Map are byte-identical to v027.
- Seed remains `12027`; all fields, serializers, folds, pair weights, controls, learner, C, bootstrap, gates, data hashes, model hashes and Confirmation commit remain unchanged.
- The post-Plan PowerShell preparation command will use `New-Item -Path` instead of the unsupported `New-Item -LiteralPath`. This is outside the scientific program and is the sole execution correction.

## Actual checks

Shared Python 3.11.15 ran `py_compile` on all four Python files with exit `0`. It ran `pytest -q test_mfcr.py` with exit `0`: `5 passed in 16.96s`. Exact generated `.pytest_cache` and `__pycache__` directories were then removed; `CACHE_LEFT=0`.

Current bytes:

- program `9a13e18bfffab4d44b5d185c003a8c8fbe7639de2ddb8fb6a6d5cf985351d9fb`;
- independent auditor `37d93688c96618d2423a77fc3377e21023a023f9a8ac71dd510092a018530674`;
- config `8c64c396dd095a689cc7da63036d92b6b9fcde02c7cc6b8016616e174d28a656`;
- conditional acquisition `11405eb06a2683537a0788dde535cc9efa7a3d2dcc1e1a8adb6248784f86bd5c`;
- tests `b5e6c8733588346043d0f9b991ca9b575951d232002f09fdf0530a794b5c4429`;
- Candidate `249a050c1539e579bb120a9f13399f9ddcc49a8e73728d2c733a33415d0dddb3`;
- Evidence Packet `ba3e98ff68703cb062ef3ad01bd1321cf30c031ea84e8ff9027e47c56b854972`.

This audit authorizes immutable v028 artifact freezing, one publish-once v028 Plan, corrected byte preparation and one Development capture. It does not authorize Confirmation, Review, Decision, Delivery or `READY_FOR_RESEARCH_USAGE`.

