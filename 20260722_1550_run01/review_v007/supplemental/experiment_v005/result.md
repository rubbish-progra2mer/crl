# Experiment Result

```json
{
  "experiment_id": "v005",
  "execution_provenance": "caller_recorded",
  "plan_sha256": "c70cc17b8c26e32d7a50c39ad354d6b3392261f89dcf3f436593abd9c423c894",
  "candidate_sha256": "c36b4847029ea234c8db9b574a128b1d9ca01dc6d425e9fddd099ba141ad8291",
  "evidence_packet_sha256": "a54b710aed7ce35f44a25943d4f4e46826e7ffdc34c628f53ce9d180f9882d6b",
  "execution": {
    "command": "MULTI_STAGE_CAPTURE_CHAIN; see experiment_v005/artifacts/attempts_manifest.json",
    "cwd": "D:\\Desktop\\crl\\20260722_1550_run01\\implementation_v005",
    "exit_code": 1,
    "stdout": "",
    "stderr": "Fewer than 3 wrong-target instruction matches for webtools_music_query_7.\n",
    "environment": {
      "device": "NVIDIA GeForce RTX 5060 Ti",
      "execution_note": "multi-stage captures retained; no fabricated canonical capture",
      "python": "3.11.15",
      "result_scope": "Development passed; untouched Confirmation failed donor coverage before metrics"
    }
  },
  "artifacts": [
    {
      "relative_path": "experiment_v005/artifacts/attempts_manifest.json",
      "byte_count": 4925,
      "sha256": "00f89df07fa949ff90ca1e6a221dd63ff6fd69151a4572c94deeb333bc3724e6"
    },
    {
      "relative_path": "experiment_v005/artifacts/audit.py",
      "byte_count": 26615,
      "sha256": "2bd37ea6cc21e1ff3ef46e76d86322dc33f2b56fe8dd7dce12fdc9aca6c6ea02"
    },
    {
      "relative_path": "experiment_v005/artifacts/config.json",
      "byte_count": 1574,
      "sha256": "6bf119f6f18432008ca0ba5fda743323ac4f1a0707b87eb72a581c0d001e3436"
    },
    {
      "relative_path": "experiment_v005/artifacts/confirmation_acquire_001_execution.json",
      "byte_count": 2656,
      "sha256": "872a39af2ed48bde78036ea6e16023d52207e8665e96c1a5e89dec7cd6d35b6f"
    },
    {
      "relative_path": "experiment_v005/artifacts/confirmation_acquire_001_stderr.bin",
      "byte_count": 0,
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    },
    {
      "relative_path": "experiment_v005/artifacts/confirmation_acquire_001_stdout.bin",
      "byte_count": 1079,
      "sha256": "0522f627f57693cd52644aa6a22af41d06a0bca6f18448635dac15ea4e3b3997"
    },
    {
      "relative_path": "experiment_v005/artifacts/confirmation_acquisition_manifest.json",
      "byte_count": 1264,
      "sha256": "4a6f05c78f4c6be871c0562bc4b6043c2e67b4583881f0d4f4dcd19abcf792c0"
    },
    {
      "relative_path": "experiment_v005/artifacts/confirmation_eval_001_execution.json",
      "byte_count": 4061,
      "sha256": "92f0bf6f1c558d5149868dc8822b990827d83ae4c539c3cf0da63cac725b1726"
    },
    {
      "relative_path": "experiment_v005/artifacts/confirmation_eval_001_stderr.bin",
      "byte_count": 791,
      "sha256": "9a65ab60f8b729d7d53cde02ecb88a832d094c535ca490a9a4d76cd8ddf821a8"
    },
    {
      "relative_path": "experiment_v005/artifacts/confirmation_eval_001_stdout.bin",
      "byte_count": 0,
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    },
    {
      "relative_path": "experiment_v005/artifacts/confirmation_queries.jsonl",
      "byte_count": 14728648,
      "sha256": "af889c05cb52cb117ae9d6d883e9020a11d27175132759d2942d1ad00f9d1f35"
    },
    {
      "relative_path": "experiment_v005/artifacts/corpus_embeddings.npy",
      "byte_count": 68279936,
      "sha256": "1892ff350f336b5e0ace8882fb300cce4b10ab6333cf2905b852b1243322f5f7"
    },
    {
      "relative_path": "experiment_v005/artifacts/dev_acquire_002_execution.json",
      "byte_count": 2612,
      "sha256": "0c48a5a5de5785e3284787f1530d63fc7ed6fb28253a5a7a4108050883248bf8"
    },
    {
      "relative_path": "experiment_v005/artifacts/dev_acquire_002_stderr.bin",
      "byte_count": 0,
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    },
    {
      "relative_path": "experiment_v005/artifacts/dev_acquire_002_stdout.bin",
      "byte_count": 812,
      "sha256": "c6cee7316aa12c5d886d46ed3bc9beb7520bdab5ad9e332a66f1fadf11432853"
    },
    {
      "relative_path": "experiment_v005/artifacts/dev_eval_001_execution.json",
      "byte_count": 4341,
      "sha256": "dd79ed192f6157acec963f151e9b193c5564122915cba90c57a6d10ecec75707"
    },
    {
      "relative_path": "experiment_v005/artifacts/dev_eval_001_stderr.bin",
      "byte_count": 138,
      "sha256": "e6da5260dc4a6854a39dbe1072e368add6081a3ebe7cc5601e583e6ba4d1a1ac"
    },
    {
      "relative_path": "experiment_v005/artifacts/dev_eval_001_stdout.bin",
      "byte_count": 4086,
      "sha256": "d640317515b2960b831cbaf76c5714a5e89d0379cd6fb1af09ae141f2cb48c2d"
    },
    {
      "relative_path": "experiment_v005/artifacts/development_acquisition_manifest.json",
      "byte_count": 941,
      "sha256": "d56e6da78ef2f4a83b408216a4ebbcf1658ebf58678e8a0275c346445c10345d"
    },
    {
      "relative_path": "experiment_v005/artifacts/development_environment.json",
      "byte_count": 501,
      "sha256": "5248e9b685ce05b53370ff7f83842c929c4f337a7b3748acfe8b6459f3b6a4a4"
    },
    {
      "relative_path": "experiment_v005/artifacts/development_queries.jsonl",
      "byte_count": 4149515,
      "sha256": "6eebd4189373f32ebb0b2316d082be39534cc9eefa1bfb413fc02372e14d65b2"
    },
    {
      "relative_path": "experiment_v005/artifacts/development_raw.jsonl",
      "byte_count": 67503458,
      "sha256": "27317e481f7591ee8248a9f8c85c47b0092ae8c8820b2838c5cffc71075c7619"
    },
    {
      "relative_path": "experiment_v005/artifacts/development_summary.json",
      "byte_count": 5113,
      "sha256": "d3c27fefff90bf980686fafd0afa8a8e1349fb3752f4985466f67eeaf7de32ea"
    },
    {
      "relative_path": "experiment_v005/artifacts/research_map_after_development.md",
      "byte_count": 5929,
      "sha256": "8f3810456bc4528a84c2373b77a583adb87258f56ef371dc0ebf4f474e9ac9ce"
    },
    {
      "relative_path": "experiment_v005/artifacts/tool_corpus.jsonl",
      "byte_count": 35321181,
      "sha256": "1bff924c03fe4b48e8d902045d68eb7fad3c2decd569fb52566ea0aec4a056f0"
    }
  ]
}
```

## Codex Interpretation

### Development

v005 executed a complete 2,600-query Development evaluation. The Main Codex independently verified all 31,200 expected cells, exact official metrics, all 7,800 three-donor assignments, zero target overlap, and reconstructed lexical support. Both retrievers passed the preregistered aggregate, source-median, mechanism, and integrity gates. The Promotion Audit is frozen as `research_map_after_development.md`.

### Confirmation failure

Untouched Confirmation acquisition completed for all fifteen frozen configs and 2,764 rows. Evaluation then stopped before any retrieval metric because `webtools_music_query_7` had fewer than three eligible same-source, label-disjoint wrong-target donors. The runner exited 1 after 6.425114799989387 seconds. No raw, summary, or environment output exists for Confirmation.

This is the direct donor-coverage falsifier in the frozen Candidate and Experiment Plan: every query had to have exactly three eligible donors and no query could be removed. The Main Codex therefore does not reduce donor count, expand donors across sources, remove the row, or rerun v005 under changed rules.

### Main Codex verdict

v005 is killed at Confirmation. Development evidence remains valid but cannot support Delivery without the frozen untouched Confirmation gate. No Review Packet, Reviewer subagent, decision, or Delivery is authorized. All bytes and attempts remain frozen, and the same Run proceeds to v006 with a new prospectively specified candidate and a genuinely untouched confirmation source.
