# Experiment Plan

```json
{
  "experiment_id": "v006",
  "candidate_sha256": "3dcadcdbb8aa88e81a1d0c8d51d15a30f154cf6c949aab7fb84a94a6412c6317",
  "evidence_packet_sha256": "e45c15b3dc5c98badc93f20ca92880e44f6fd8ea5673b16c9dd567b89316f4f1"
}
```

## Codex Plan

## Frozen before results

v006 plan = experiment_v005/plan.md (SHA a8ca5e0d433fa2e1610068d16b4799
99d231abb6ab161152c7559895d7bd1a4d) incorporated by reference, with one
delta: reader.max_tokens = 1000 (config defect repair; v005 reader arm
invalidated by reasoning-token starvation, see experiment_v005/
result.md SHA b72a09f149b22ef5ee9794b7b4b2f9c89db8b234a45ee7a9b254cfb5e
c635a03). Only the reader arm re-runs (attempt dev_reader_001 under
v006); the retrieval decomposition is NOT re-run - its v005 captures
remain the binding evidence for kills 1-2.

## Exact execution readiness (delta)

Same interpreter/cwd/import chain as v005 (verified this session);
corrected config verified present at implementation_v006/config.json;
capture dir experiment_v006/captures/dev_reader_001 and declared output
work/dev_reader_001/reader_raw.jsonl do not exist yet; key in process
env only. A near-real-scale payload check is impossible without
touching D again and is intentionally skipped: the failure mode being
repaired (reasoning starvation) is directly parameter-bounded and the
kill-3 gate protects against residual defects.

## Direct falsification conditions

Kill 3 (unchanged): no turn_topk accuracy deficit vs oracle_current on
update items at equal budget -> no consequence -> candidate records
failure.
