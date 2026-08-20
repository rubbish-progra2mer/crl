# Experiment Result

```json
{
  "experiment_id": "v006",
  "execution_provenance": "caller_recorded",
  "plan_sha256": "6bc127ecb55561e611a70a88937d5b6989d092038deffbb2c94d58dd29574598",
  "candidate_sha256": "bee9c37465b9f4dfa6cb1f0522569eed80fa4ca079332f2c84996c5708384e09",
  "evidence_packet_sha256": "32780d598e779fa25e5c8f4e65ecc2db07805ce8217e33b4be039b6562f4cee8",
  "execution": {
    "command": "MULTI_STAGE_CAPTURE_CHAIN; see experiment_v006/artifacts/attempts_manifest.json",
    "cwd": "D:\\Desktop\\crl\\20260722_1550_run01\\implementation_v006",
    "exit_code": 1,
    "stdout": "",
    "stderr": "FileNotFoundError: corpus embeddings output parent did not exist.\n",
    "environment": {
      "python": "3.11.15",
      "result_scope": "Development execution failed before metrics"
    }
  },
  "artifacts": [
    {
      "relative_path": "experiment_v006/artifacts/attempts_manifest.json",
      "byte_count": 1108,
      "sha256": "288153c7b5e13a456c85c6dec3b4e37ab884e8d92c2505b1fa8dc0e32e6a78d9"
    },
    {
      "relative_path": "experiment_v006/artifacts/audit.py",
      "byte_count": 26358,
      "sha256": "ba44d7893e239983affffa2e20653ce4370b46a1eff60b38de2ffb41ae5efe74"
    },
    {
      "relative_path": "experiment_v006/artifacts/config.json",
      "byte_count": 1008,
      "sha256": "b9ebb6f4e695772533b81e50d667dae92312fe8ecf3fcd6c9da4f1643d45e64b"
    },
    {
      "relative_path": "experiment_v006/artifacts/dev_acquire_001_execution.json",
      "byte_count": 3097,
      "sha256": "fc08a093c4e2e204c3e62d9c50f350bed30c354edf935d4f003432fedf7bf94d"
    },
    {
      "relative_path": "experiment_v006/artifacts/dev_acquire_001_stderr.bin",
      "byte_count": 0,
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    },
    {
      "relative_path": "experiment_v006/artifacts/dev_acquire_001_stdout.bin",
      "byte_count": 1015,
      "sha256": "4546dc6afdc5d79d40e497d5e6cfe2874dca0d560d5223fb00e31c78f1a79d25"
    },
    {
      "relative_path": "experiment_v006/artifacts/dev_eval_001_execution.json",
      "byte_count": 4015,
      "sha256": "a8884bbdd9d63a6702faf84e37177bd3cda1abc6fa52feaa965b9d3d832909b1"
    },
    {
      "relative_path": "experiment_v006/artifacts/dev_eval_001_stderr.bin",
      "byte_count": 3331,
      "sha256": "63ecdd77164feab66590edb89d43dcc21cece5048e9c4ade689c7eb1224a03e3"
    },
    {
      "relative_path": "experiment_v006/artifacts/dev_eval_001_stdout.bin",
      "byte_count": 0,
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    },
    {
      "relative_path": "experiment_v006/artifacts/development_acquisition_manifest.json",
      "byte_count": 1140,
      "sha256": "46ae061f7b973f311e3c01988707fede21553a011524a977452fdad0b04e11d8"
    },
    {
      "relative_path": "experiment_v006/artifacts/development_corpus.jsonl",
      "byte_count": 8749686,
      "sha256": "2380f54138270106dd20d769bb304f442c861e86986ce23812f0c552d82c0fb4"
    },
    {
      "relative_path": "experiment_v006/artifacts/development_queries.jsonl",
      "byte_count": 965654,
      "sha256": "ab104b33af410eae9e09a60bf717b76bce7d8c908bb3ceae8cfce5a147c4b9a7"
    }
  ]
}
```

## Codex Interpretation

v006 acquired and froze the exact 1,000-row Development range and its 9,436-document phase corpus. The first evaluation produced no metric: after BM25 work and dense corpus encoding, `np.save` raised `FileNotFoundError` because the new embeddings output parent directory had not been created. The runner exited 1 and declared every output absent. This is an implementation execution failure, not scientific evidence. v006 is frozen, Confirmation was never acquired, no Review is authorized, and v007 may reuse the touched Development bytes with only the output-directory fix while preserving the untouched Confirmation range.
