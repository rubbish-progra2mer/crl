# Experiment Plan

```json
{
  "experiment_id": "v007",
  "candidate_sha256": "bee9c37465b9f4dfa6cb1f0522569eed80fa4ca079332f2c84996c5708384e09",
  "evidence_packet_sha256": "32780d598e779fa25e5c8f4e65ecc2db07805ce8217e33b4be039b6562f4cee8"
}
```

## Codex Plan

# v007 execution-only replay of the frozen training-prompt audit

v006 acquired Development rows `[0,1000)` and built its phase corpus, but produced no metric because the embeddings output parent did not exist. v007 changes only that output-path preparation. Candidate, Evidence Packet, config, data ranges, donor logic, six views, retrievers, metrics, ten blocks, bootstrap seed/count, promotion gates, Claim boundary, and untouched Confirmation rows `[207826,208826)` are unchanged.

Frozen audit expected SHA-256 `68e70a21e04a7f10275e01733db8586910b6deea93033e4e014e73fdbb68f9a9`; config `b9ebb6f4e695772533b81e50d667dae92312fe8ecf3fcd6c9da4f1643d45e64b`; reused Development queries `ab104b33af410eae9e09a60bf717b76bce7d8c908bb3ceae8cfce5a147c4b9a7`; reused Development corpus `2380f54138270106dd20d769bb304f442c861e86986ce23812f0c552d82c0fb4`; acquisition manifest `46ae061f7b973f311e3c01988707fede21553a011524a977452fdad0b04e11d8`.

Development evaluation must pass both retrievers' positive equal-block mean, bootstrap lower bound, block median, positive lexical mechanism, donor coverage, raw-cell integrity and exact independent metrics before Confirmation acquisition. Confirmation uses the same frozen gates. Capture and review rules remain those in the v006 Candidate and CRL protocol.
