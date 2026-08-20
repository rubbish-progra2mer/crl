# Experiment Result

```json
{
  "experiment_id": "v005",
  "execution_provenance": "caller_recorded",
  "plan_sha256": "a8ca5e0d433fa2e1610068d16b479999d231abb6ab161152c7559895d7bd1a4d",
  "candidate_sha256": "aa99d8c63cc631ca3ce8057408c7f7edea060820098a3d50ac9c6b9a28e22da0",
  "evidence_packet_sha256": "ea26ece96884819b6a633d903f3c3a3f219376abb93331eb2b7080f03b9343dd",
  "execution": {
    "command": "captured: dev_local_001 (measure_decomposition.py) and dev_reader_001 (reader_arm.py), argv in captures/*/execution.json",
    "cwd": "D:\\Desktop\\crl\\20260726_1640_run02\\implementation_v005",
    "exit_code": 0,
    "stdout": "see captures/dev_local_001/stdout.bin and dev_reader_001/stdout.bin",
    "stderr": "see captures/*/stderr.bin",
    "environment": {
      "encoder": "all-MiniLM-L6-v2",
      "gpu": "RTX 5060 Ti",
      "python": "3.11.15 (.venv)",
      "reader_model_field": "deepseek-v4-flash"
    }
  },
  "artifacts": [
    {
      "relative_path": "experiment_v005/artifacts/measure_decomposition.py",
      "byte_count": 7547,
      "sha256": "c171a710986453350d7c24e214f7a0f5ee8338e86613d7d6b4bece44f3a108bc"
    },
    {
      "relative_path": "experiment_v005/artifacts/reader_arm.py",
      "byte_count": 6678,
      "sha256": "dbbd3233eecb40a2ae33c1dc8f62aae77447529af3e2814317c658d8c894a4f0"
    },
    {
      "relative_path": "experiment_v005/artifacts/config.json",
      "byte_count": 915,
      "sha256": "15a49c241330cfec26c83029676e7cb335e260954227a1440ffdfaae2cdc28d7"
    }
  ]
}
```

## Codex Interpretation

v005 Promotion Development executed in two captured attempts.

DEV_LOCAL_001 (retrieval decomposition, D bucket, local, VALID):
All preregistered replication signatures held on the untouched D bucket
(222 items, 37 update pairs):
- Kill 1 NOT triggered: turn/direct inversion 22/37 (59.5%, far above
  the 40% chance threshold). The stale-over-current phenomenon
  replicates on fresh data.
- Kill 2 NOT triggered: sentence-level reduces inversions 22->16 and
  improves mean margin -0.0493 -> -0.0203 (dilution share confirmed);
  bonus: sentence units also raise non-update evidence hits 6.52->8.06.
- Propagation share ~0 replicated: ppr 23/37 vs direct 22/37.
- Recency bluntness replicated: fixes inversions (22->6) but harms
  non-update hits (6.52->5.91).

DEV_READER_001 (consequence arm, deepseek, INVALIDATED BY CONFIG DEFECT):
All 111 calls completed (status 200, model deepseek-v4-flash, usage
logged; 123,704 in / 10,167 out tokens; cost well under 1 USD). However
deepseek-v4-flash is a REASONING model: with max_tokens=100 the entire
budget was consumed by reasoning_tokens in 47/111 responses, yielding
empty answers (19/18/10 across turn/sentence/oracle arms — arm-varying,
hence a CONFOUND, not usable as a subset). Directional accuracies
(5/37, 10/37, 16/37) are therefore NOT interpretable as scientific
signal. Per the attempt discipline this is an implement/config defect:
the consequence arm must be re-run under a corrected config in the next
version (v006). No silent rerun is performed within v005.

Machine observation MD-11 recorded: synthetic-smoke readiness passed
(short synthetic items reason quickly under 100 tokens) but real
payloads exceeded the reasoning budget - the readiness smoke definition
must include a near-real-scale payload shape check.

Conclusion: the decomposition claims of candidate_v005 are supported on
fresh data at the retrieval stage; the consequence arm is carried to
v006 with corrected reader config. Kill 3 remains UNDECIDED.