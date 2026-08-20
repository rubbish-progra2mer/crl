# Experiment Result

```json
{
  "experiment_id": "v004",
  "execution_provenance": "caller_recorded",
  "plan_sha256": "366f02db50201a160b74267c3152b5b8dd47dec75d8541d42988aae5763c1f1d",
  "candidate_sha256": "bcaf92e201c586dc625bd1dbb1a897d4092042a833da3a7f263830bbddfc2cb1",
  "evidence_packet_sha256": "83c61e78bd42f61a43fa676e6644b3eaf90477442925b0170c6791bebe819fc1",
  "execution": {
    "command": "MULTI_STAGE_CAPTURE_CHAIN; see experiment_v004/artifacts/attempts_manifest.json",
    "cwd": "D:\\Desktop\\crl\\20260722_1550_run01\\implementation_v004",
    "exit_code": 0,
    "stdout": "",
    "stderr": "",
    "environment": {
      "cuda": "torch 2.12.0+cu130; capability 12.0; driver 591.86",
      "device": "NVIDIA GeForce RTX 5060 Ti",
      "execution_note": "multi-stage captures retained; no fabricated canonical capture",
      "python": "3.11.15",
      "result_scope": "Development plus untouched source-disjoint Confirmation"
    }
  },
  "artifacts": [
    {
      "relative_path": "experiment_v004/artifacts/attempts_manifest.json",
      "byte_count": 6659,
      "sha256": "5c1ade36150a904fe24b3121af5c4c5033f01199745408c952cda4d048a0229c"
    },
    {
      "relative_path": "experiment_v004/artifacts/audit.py",
      "byte_count": 25850,
      "sha256": "d97903a938096dcbee197a8af41617c1c1e2e4226438868c157ff1156c6231f4"
    },
    {
      "relative_path": "experiment_v004/artifacts/config.json",
      "byte_count": 1221,
      "sha256": "0e9743da2d99c8bd34aee9d00cc1c428f0c1de07cd0c23db853ec8fa67c4fc79"
    },
    {
      "relative_path": "experiment_v004/artifacts/confirmation_acquire_001_execution.json",
      "byte_count": 2653,
      "sha256": "a807e89b3c7e6e2d327c787d4952b52f804dae2e8434b8633d34586ce3c4e401"
    },
    {
      "relative_path": "experiment_v004/artifacts/confirmation_acquire_001_stderr.bin",
      "byte_count": 0,
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    },
    {
      "relative_path": "experiment_v004/artifacts/confirmation_acquire_001_stdout.bin",
      "byte_count": 847,
      "sha256": "2d3a883cffe24a81fa9824405e122fa65f3836f00a0072303f706a975103d3b6"
    },
    {
      "relative_path": "experiment_v004/artifacts/confirmation_acquisition_manifest.json",
      "byte_count": 976,
      "sha256": "d6800ddf0f74d27b0e324e4acb4c45d6f9a41e1770cab2ecb7a132e22f3fc439"
    },
    {
      "relative_path": "experiment_v004/artifacts/confirmation_environment.json",
      "byte_count": 501,
      "sha256": "5248e9b685ce05b53370ff7f83842c929c4f337a7b3748acfe8b6459f3b6a4a4"
    },
    {
      "relative_path": "experiment_v004/artifacts/confirmation_eval_002_execution.json",
      "byte_count": 4419,
      "sha256": "c97aa8494fd792ca384566cb7613589f28c10f734aed7ba733c048aafee76537"
    },
    {
      "relative_path": "experiment_v004/artifacts/confirmation_eval_002_stderr.bin",
      "byte_count": 138,
      "sha256": "db7b95a08bbcf661ac0ac05f61068039d77d8cf1f6e955424eb9b1bde0cd8285"
    },
    {
      "relative_path": "experiment_v004/artifacts/confirmation_eval_002_stdout.bin",
      "byte_count": 2831,
      "sha256": "be8d11b0f84d9f76d63b620e09602f722385ae913e8f9ae89b48f33f80a59bd4"
    },
    {
      "relative_path": "experiment_v004/artifacts/confirmation_queries.jsonl",
      "byte_count": 3030552,
      "sha256": "2f60f1802ebd79c2fd34fdfa93e1d556042d8d521e88a0f537d89219ae87914f"
    },
    {
      "relative_path": "experiment_v004/artifacts/confirmation_raw.jsonl",
      "byte_count": 15877526,
      "sha256": "04d6061fd9e50cd21cc24a7a1f952eaa2b0fe80a2ef68df65be9a4d7cf1d216e"
    },
    {
      "relative_path": "experiment_v004/artifacts/confirmation_summary.json",
      "byte_count": 3666,
      "sha256": "fb42565bd1a1aed59cde8b6dfbbdac27c72ac56aa4c7465c1acc489b41804ea0"
    },
    {
      "relative_path": "experiment_v004/artifacts/corpus_embeddings.npy",
      "byte_count": 68279936,
      "sha256": "1892ff350f336b5e0ace8882fb300cce4b10ab6333cf2905b852b1243322f5f7"
    },
    {
      "relative_path": "experiment_v004/artifacts/dev_acquire_001_execution.json",
      "byte_count": 2869,
      "sha256": "4613a82bbde771e24b8bad120ea306a204b47e55c14cf7aa6671f399e0f22714"
    },
    {
      "relative_path": "experiment_v004/artifacts/dev_acquire_001_partial_development_queries.jsonl",
      "byte_count": 2787825,
      "sha256": "b785627bffe17b69bb58ccc664f20375735e56b6870322e3dad43a771f025d31"
    },
    {
      "relative_path": "experiment_v004/artifacts/dev_acquire_001_stderr.bin",
      "byte_count": 4678,
      "sha256": "91a38a6bcae438bb1e27ce3a74b20ef77c4b61988f855eb60ff793087a4ab9c6"
    },
    {
      "relative_path": "experiment_v004/artifacts/dev_acquire_001_stdout.bin",
      "byte_count": 0,
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    },
    {
      "relative_path": "experiment_v004/artifacts/dev_acquire_002_execution.json",
      "byte_count": 3099,
      "sha256": "bbc030e970b2bb9ace9ff73932c2de5a788e1da188c5172c9b684d24a5cc195c"
    },
    {
      "relative_path": "experiment_v004/artifacts/dev_acquire_002_stderr.bin",
      "byte_count": 0,
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    },
    {
      "relative_path": "experiment_v004/artifacts/dev_acquire_002_stdout.bin",
      "byte_count": 938,
      "sha256": "8c633d7d50c0c190ed566b8710e6e899c413ff10161d1ec12ed3561c38169dab"
    },
    {
      "relative_path": "experiment_v004/artifacts/dev_eval_001_execution.json",
      "byte_count": 4478,
      "sha256": "bb89b965a1451a8b1294c4875c16fdca5f7d8b9353f9a8c64a1b0e46765fe260"
    },
    {
      "relative_path": "experiment_v004/artifacts/dev_eval_001_stderr.bin",
      "byte_count": 10874,
      "sha256": "8d3b5387b21c7e68a57d11ac9746fa4d3dc1e529a3c7ed994375e1ff96f2a56c"
    },
    {
      "relative_path": "experiment_v004/artifacts/dev_eval_001_stdout.bin",
      "byte_count": 1997,
      "sha256": "b1b0e768f93cfb8aadced527c107f2b89e03e4f4ed4e1e6f789cfacd11e5004b"
    },
    {
      "relative_path": "experiment_v004/artifacts/development_acquisition_manifest.json",
      "byte_count": 1069,
      "sha256": "9a59115b6918cf6c7462cb1016caf8bc0b459f5605eb45d13f18e7f74299defc"
    },
    {
      "relative_path": "experiment_v004/artifacts/development_corpus.jsonl",
      "byte_count": 35321181,
      "sha256": "1bff924c03fe4b48e8d902045d68eb7fad3c2decd569fb52566ea0aec4a056f0"
    },
    {
      "relative_path": "experiment_v004/artifacts/development_environment.json",
      "byte_count": 501,
      "sha256": "5248e9b685ce05b53370ff7f83842c929c4f337a7b3748acfe8b6459f3b6a4a4"
    },
    {
      "relative_path": "experiment_v004/artifacts/development_queries.jsonl",
      "byte_count": 2787825,
      "sha256": "b785627bffe17b69bb58ccc664f20375735e56b6870322e3dad43a771f025d31"
    },
    {
      "relative_path": "experiment_v004/artifacts/development_raw.jsonl",
      "byte_count": 6094420,
      "sha256": "bb933d4f45c7857d399135754146423127248ec2151bdeb678493a80632056c1"
    },
    {
      "relative_path": "experiment_v004/artifacts/development_summary.json",
      "byte_count": 2512,
      "sha256": "f8983747dd0c6ab1d637f4aa6a6941fe0576e5ff9fd2d407570fdaabed7a7e4a"
    }
  ]
}
```

## Codex Interpretation

### Execution and byte integrity

v004 is a multi-stage captured experiment; no synthetic canonical capture is claimed. `attempts_manifest.json` records six attempt IDs. `dev_acquire_001` failed with an SSL EOF after persisting only the Development queries. `dev_acquire_002`, `dev_eval_001`, and `confirmation_acquire_001` completed with exit code 0. `confirmation_eval_001` was interrupted by the foreground tool-session transition before any persistent capture or output byte existed; both of its directories are empty and it has no claimed exit code. `confirmation_eval_002` then completed with exit code 0 in 1489.2802164999885 seconds. Its execution capture binds Python 3.11.15, the frozen audit/config, 44,453-row corpus, 1,852 Confirmation queries, fixed embeddings, and all three declared outputs.

The Main Codex independently parsed all 14,816 expected Confirmation rows (`1852 queries x 4 views x 2 retrievers`). All row keys are unique; every query has the exact eight required cells; every ranking contains ten unique IDs; official qrel bindings, NDCG@10, Recall@10, and Completeness@10 recompute with maximum absolute error 0.0. Donors are same-source and non-self, recorded token-length differences recompute exactly, target overlap is zero, and no aligned instruction contains a target ID as a literal substring.

### Confirmation result

BM25 has strictly positive aligned-minus-mismatched NDCG@10 in all eight sources. Its equal-source mean is 0.2340920542273706, source-cluster bootstrap interval is [0.13536276269699324, 0.34522239606628824], and lexical-support mechanism mean is 0.21301582231999838.

MiniLM has equal-source mean 0.2029356903337854, source-cluster bootstrap interval [0.08558011443551902, 0.3328598887850184], and the same positive mechanism mean. Seven source effects are positive, but `gorilla-pytorch` is exactly 0.0 across its 43 queries. The other MiniLM source effects are 0.5379173870791791, 0.33441176264334216, 0.033461876710593155, 0.24092918969774668, 0.08515151904574032, 0.050707263621732175, and 0.3409065238719496 in the frozen source order excluding `gorilla-pytorch`.

### Main Codex verdict

v004 fails its preregistered Claim Contract. That contract requires both retrievers to be strictly positive in every included Confirmation source; a zero is non-positive. Positive aggregate intervals, positive lexical support, and seven positive MiniLM sources cannot override the source-level kill condition. This is a scientific failure, not an execution or capture failure. No Review Packet, Reviewer subagent, decision, or Delivery is authorized for v004. Its bytes remain frozen and the same Run must proceed to v005 with a new, prospectively specified candidate rather than changing v004's threshold after observing Confirmation.
