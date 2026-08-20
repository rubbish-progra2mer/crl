# Experiment Plan

```json
{
  "experiment_id": "v019",
  "candidate_sha256": "30c51e3cbadb8affc925d42ff91b12240dc3e018e83df0069d5dcdbdb21026de",
  "evidence_packet_sha256": "d9239666b23a0aadc725f67c95dacccad1ef280a4537d3f48deba8d6ed2481f1"
}
```

## Codex Plan

# v019 One-Shot Development Plan

Plan status: `FROZEN_BEFORE_SCIENTIFIC_EXECUTION`.

This plan authorizes one Development training capture and one independent audit capture. It does not authorize Confirmation, Reviewer agents, Decision, Delivery, or a system status change.

## Scientific question

On the fixed BFCL v3 simple/BM25 protocol, does the predeclared coverage-constrained terminal utility `lambda*hit-K/N` reduce shortlist depth relative to the published per-query BoR reward while preserving presented-gold coverage? The changed computation and maximum claim are exactly those in frozen `candidate_v019.md`.

## Frozen bindings

- Candidate `30c51e3cbadb8affc925d42ff91b12240dc3e018e83df0069d5dcdbdb21026de`.
- Evidence Packet `d9239666b23a0aadc725f67c95dacccad1ef280a4537d3f48deba8d6ed2481f1`.
- Program `ddb36e59145228362597da2e559ed22ca987499e32cb25519293c9d3f4c4375a`.
- Independent audit `806794c0d46e706065c058281fe7db6b1fc598368cb3e59d5d9a78263a1c67c1`.
- Config `bdd2683af36f5babed46203a66c419ff3017625a204649909f59b4b0aa478cbf`.
- Objective tests `e0fc74c3033b9010158e69829e95e9ac9b571f759b2895001a0894c6ba66e367`.
- Development input `fbc37b2ad252bf9af985582e0e07b456173fe627d957491472ea9cef5fb83158` (400 lines).
- `rank-bm25==0.2.2` wheel `7bd4a95571adadfc271746fa146a4bcfd89c0cf731e49c3d1ad863290adbe8ae`.
- Implementation audit `3a999df62100d6b6fdf6f47a2a3d0e991f7f4ecdaf6152b56dfacc3b006b7eb4`.
- Target notebook `61da53127597d7a90a440a87ff2efcea77665454852d50552df9bb2972a6ff81`, target repository commit `9759eb9f0e7ed90ff289d34300acc15453f7851a`.

Every executable/input path below points to `experiment_v019/artifacts/`, the copies made by `ResearchWorkspace.save_experiment_artifact()`. No source file under `implementation_v019/` or `sources_vNNN/` is an execution input.

## Fixed design

- Registry/candidate maximum 370; sorted tool names; target notebook's two-stage gold-included BM25 ranking.
- All 400 fixed source queries; deterministic 70/30 split with seed 42; expected Development test count 120.
- Learned policies: target BoR-DQN, target F1-DQN, unconstrained-ratio ablation, Candidate.
- Seeds 42, 123, 456; 8,000 episodes per policy/seed; all architecture and optimizer values are those in frozen config.
- Fixed K comparators: 1, 3, 5, 10, 20, 50.
- Expected raw rows: 2,160 = 12 learned groups x 120 plus 6 fixed groups x 120.
- Expected slow-controller history rows: 96 = 2 policies x 3 seeds x 16 updates.
- Expected frozen models: 12.
- No Development-test result enters training or controller updates.

## Development capture

Authoritative runner:
`D:\Desktop\crl\crl_agent_v3\.venv\python.exe D:\Desktop\crl\crl_agent_v3\tools\run_local_experiment.py`

Runner facts:

- capture dir: `D:\Desktop\crl\20260722_1550_run01\experiment_v019\captures\dev_001`
- cwd: `D:\Desktop\crl\20260722_1550_run01\experiment_v019\artifacts`
- declared inputs: `program.py`, `config.json`, `BFCL_v3_simple.json`, `rank_bm25-0.2.2-py3-none-any.whl`
- payload argv:
  `D:\Desktop\crl\crl_agent_v3\.venv\python.exe D:\Desktop\crl\20260722_1550_run01\experiment_v019\artifacts\program.py --phase development --config D:\Desktop\crl\20260722_1550_run01\experiment_v019\artifacts\config.json --input D:\Desktop\crl\20260722_1550_run01\experiment_v019\artifacts\BFCL_v3_simple.json --rank-bm25-wheel D:\Desktop\crl\20260722_1550_run01\experiment_v019\artifacts\rank_bm25-0.2.2-py3-none-any.whl --output-dir D:\Desktop\crl\20260722_1550_run01\experiment_v019\dev_output_001`
- declared outputs: `raw_rows.jsonl`, `summary.json`, `split_manifest.json`, `controller_history.json`, and all 12 `<policy>_seed<seed>.pt` files under `dev_output_001/models/`.

The runner must execute once in the foreground. Its `execution.json`, stdout bytes, stderr bytes, every declared output fact, and program wall time are evidence regardless of exit code.

## Independent audit capture

Only if Development produced every declared output, run frozen `audit.py` once through the same runner:

- capture dir: `D:\Desktop\crl\20260722_1550_run01\experiment_v019\captures\dev_audit_001`
- cwd: `D:\Desktop\crl\20260722_1550_run01\experiment_v019\artifacts`
- declared inputs: frozen `audit.py`, config, BFCL input, wheel, Development raw rows, summary, controller history, and all 12 model files
- payload argv:
  `D:\Desktop\crl\crl_agent_v3\.venv\python.exe D:\Desktop\crl\20260722_1550_run01\experiment_v019\artifacts\audit.py --config D:\Desktop\crl\20260722_1550_run01\experiment_v019\artifacts\config.json --input D:\Desktop\crl\20260722_1550_run01\experiment_v019\artifacts\BFCL_v3_simple.json --rank-bm25-wheel D:\Desktop\crl\20260722_1550_run01\experiment_v019\artifacts\rank_bm25-0.2.2-py3-none-any.whl --raw-rows D:\Desktop\crl\20260722_1550_run01\experiment_v019\dev_output_001\raw_rows.jsonl --summary D:\Desktop\crl\20260722_1550_run01\experiment_v019\dev_output_001\summary.json --controller-history D:\Desktop\crl\20260722_1550_run01\experiment_v019\dev_output_001\controller_history.json --report D:\Desktop\crl\20260722_1550_run01\experiment_v019\dev_audit_output_001\report.json`
- declared output: `dev_audit_output_001/report.json`.

Audit support requires exit 0, `AUDIT_OK`, 2,160 rows, 18 groups, 120 query IDs, 96 controller updates, 12 models, 1,440 learned-policy actions, and every maximum error equal to zero (therefore <= `1e-12`).

## Predeclared Development support conditions

Relative to target BoR-DQN, Candidate must satisfy all:

1. mean coverage delta >= `-0.01`;
2. mean K delta <= `-1.0`;
3. mean defined-BoR delta >= `0.25` bits;
4. at least two matched seeds have coverage delta >= `-0.025` and lower mean K;
5. Candidate is not dominated in `(coverage, mean K)` by any target or fixed-K comparator;
6. the independent audit passes exactly as specified.

These conditions are evidence inputs, not an automatic Promotion decision.

## Main-Codex Promotion Audit

After both captures, the main Codex must personally read the execution records, raw rows, all summaries, controller histories, model/output hashes, audit report, and representative paired cases. It must distinguish reduced K from coverage abandonment, inspect seed stability and dual trajectories, and assess the 0.5-point source-snapshot discrepancy recorded in `implementation_audit_v019.md`. Only a scientifically positive written Promotion Audit may authorize first acquisition of the fixed untouched Confirmation bytes.

Any failed support condition, execution failure after frozen scientific bytes, comparator mismatch, or substantive code/config correction closes v019 without Confirmation and advances the same Run to v020. Thresholds may not be lowered. No Reviewer may be created before a later complete frozen Review Packet.
