# v032 Main-Codex Implementation Audit

Disposition: `READY_TO_FREEZE_ONE_SHOT_DEVELOPMENT`.

This is the current main Codex's preexecution audit. No subagent or Reviewer
participated, and no v032 scientific metric has been computed.

## Files read completely

I read the complete current bytes of:

- `problem_v032.md`;
- `research_map_v032.md`;
- `nearest_prior_v032.md`;
- `candidate_v032.md`;
- `implementation_v032/program.py`;
- `implementation_v032/audit.py`;
- `implementation_v032/config.json`;
- `implementation_v032/test_program.py`.

I also re-read the relevant frozen `base_v012.py` data/action-text functions and
the current bucket manifests.

## Scientific implementation match

- `prepare_examples` extracts the bounded task description and the existing full
  stripped command/output surface. It neither parses commands into roles nor
  reads reasoning traces or exploit categories.
- A bundle holds out both one task fold and one complete target generator.
  Representation, conditional maps, scalers and all supervised classifiers are
  fitted only on rows outside both boundaries.
- The shared TF-IDF and SVD representation is fitted on training task/action
  text without labels.
- `successful_map` receives only `target=0` training rows. Its sample weights
  sum to one per task. `all_map` uses every training row with the same equal-task
  weighting.
- Candidate features are exactly `abs(action_latent -
  successful_map(task_latent))`.
- The equal-capacity `all_row_innovation`, identity innovation, raw latent,
  task-concatenation and direct-text controls are all implemented and scored on
  identical held-out rows.
- The Candidate is fixed as the last method and is excluded from comparator
  selection.
- Development builds a separate frozen full bundle for each target generator.
  A later Confirmation must use the matching generator-excluded bundle, rejects
  any Development-task overlap and performs no fit.
- The program does not acquire bucket 0. It merely accepts a future
  config-bound Confirmation dataset after the main Codex authorizes the
  separate acquisition.

## Independent audit path

`audit.py` does not import `program.py`. It independently:

- reads and reconstructs all 4,256 source rows;
- refits all nine task-fold×generator OOF bundles;
- recomputes every latent coordinate, both ridge maps, four dense feature
  blocks, six method scores, metrics, task bootstrap, slices and gates;
- independently refits the three full generator-excluded bundles;
- compares raw row identity, OOF scores, dense features, summary values and
  frozen full-bundle predictions;
- returns `AUDIT_OK` only when all maximum errors are at most `1e-12`.

The auditor shares only the already frozen generic `base_v012.py` action-text,
vectorizer and classifier constructors. It shares no v032 program function.

## Executed checks

From `D:\Desktop\crl\20260722_1550_run01` with
`D:\Desktop\crl\crl_agent_v3\.venv\python.exe`:

- `python -m py_compile implementation_v032\program.py
  implementation_v032\audit.py implementation_v032\test_program.py`:
  exit `0`;
- `python -m pytest -q -p no:cacheprovider
  implementation_v032\test_program.py`: exit `0`, `5 passed in 2.36s`;
- structural preflight: exit `0`, 4,256 unique rows, 250 tasks, 1,794
  successful rows, 2,462 serious-exploit rows, three generators and five
  sources;
- every one of the nine generator×fold held-out cells contains both classes,
  with 325-642 rows and 77-84 tasks.

The exact generated `implementation_v032/__pycache__` was resolved inside the
intended implementation directory and deleted. The audited files are UTF-8
without BOM and use LF newlines.

## Frozen-risk judgment

The main remaining scientific risk is substantive: a cross-task linear normal
map may be too coarse to improve the strong direct detector. That is the
registered hypothesis, not an implementation defect. Ridge alpha, latent
dimension, SVD iterations, vocabulary, folds, controls and gates may not be
retuned after the first frozen Development execution.

The implementation is ready for one-shot freeze and execution.
