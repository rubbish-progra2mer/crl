# Experiment Result

```json
{
  "experiment_id": "v007",
  "execution_provenance": "caller_recorded",
  "plan_sha256": "b4ec74383cffb3a202b7eeaaa711d315ddca92f6f178e456343f185f79c42ab1",
  "candidate_sha256": "bee9c37465b9f4dfa6cb1f0522569eed80fa4ca079332f2c84996c5708384e09",
  "evidence_packet_sha256": "32780d598e779fa25e5c8f4e65ecc2db07805ce8217e33b4be039b6562f4cee8",
  "execution": {
    "command": "MULTI_STAGE_CAPTURE_CHAIN; see experiment_v007/artifacts/attempts_manifest.json",
    "cwd": "D:\\Desktop\\crl\\20260722_1550_run01\\implementation_v007",
    "exit_code": 0,
    "stdout": "",
    "stderr": "",
    "environment": {
      "confirmation_capture_exit_code": "0",
      "cuda": "13.0",
      "gpu": "NVIDIA GeForce RTX 5060 Ti",
      "main_codex_audit_exit_code": "0",
      "python": "3.11.15",
      "torch": "2.12.0+cu130"
    }
  },
  "artifacts": [
    {
      "relative_path": "experiment_v007/artifacts/attempts_manifest.json",
      "byte_count": 3148,
      "sha256": "b0d85cacd6d43e95df499b2bea8cbf18a63a6759a2c6f4d68cb939c53794913b"
    },
    {
      "relative_path": "experiment_v007/artifacts/audit.py",
      "byte_count": 26431,
      "sha256": "68e70a21e04a7f10275e01733db8586910b6deea93033e4e014e73fdbb68f9a9"
    },
    {
      "relative_path": "experiment_v007/artifacts/config.json",
      "byte_count": 1008,
      "sha256": "b9ebb6f4e695772533b81e50d667dae92312fe8ecf3fcd6c9da4f1643d45e64b"
    },
    {
      "relative_path": "experiment_v007/artifacts/confirmation_acquire_001_execution.json",
      "byte_count": 3159,
      "sha256": "ce890ba33e0562ba331fec2dfb274853b3e8727100235c5892dbc657c7f85c03"
    },
    {
      "relative_path": "experiment_v007/artifacts/confirmation_acquire_001_stderr.bin",
      "byte_count": 0,
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    },
    {
      "relative_path": "experiment_v007/artifacts/confirmation_acquire_001_stdout.bin",
      "byte_count": 1051,
      "sha256": "14bc65bbf95c8b7ebdceb2f0aab4061ca053d3de59020ab82be419f43d1b72f6"
    },
    {
      "relative_path": "experiment_v007/artifacts/confirmation_acquisition_manifest.json",
      "byte_count": 1176,
      "sha256": "3049a28c5a8fb053d47faf72cba10734b5ad565b0d834ffdfffeb2b67aa1d330"
    },
    {
      "relative_path": "experiment_v007/artifacts/confirmation_audit_001_execution.json",
      "byte_count": 3240,
      "sha256": "c2efcd38a100116f399594b4b18da42286893b819f173fd34e1d8cc2519e5e25"
    },
    {
      "relative_path": "experiment_v007/artifacts/confirmation_audit_001_stderr.bin",
      "byte_count": 0,
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    },
    {
      "relative_path": "experiment_v007/artifacts/confirmation_audit_001_stdout.bin",
      "byte_count": 1833,
      "sha256": "10495bcfadf4d1c18086192386547bfe3bd07c5592c80db7035a64995984b496"
    },
    {
      "relative_path": "experiment_v007/artifacts/confirmation_corpus.jsonl",
      "byte_count": 8494336,
      "sha256": "77b9ba0b91038e71de18128351de10162b74df7cfe86b70a085936af154d9433"
    },
    {
      "relative_path": "experiment_v007/artifacts/confirmation_corpus_embeddings.npy",
      "byte_count": 14298752,
      "sha256": "7860fc2009981d3789dd97337628c299fd6d50a7dc76379058a21ee6d9a4375a"
    },
    {
      "relative_path": "experiment_v007/artifacts/confirmation_environment.json",
      "byte_count": 501,
      "sha256": "5248e9b685ce05b53370ff7f83842c929c4f337a7b3748acfe8b6459f3b6a4a4"
    },
    {
      "relative_path": "experiment_v007/artifacts/confirmation_eval_001_execution.json",
      "byte_count": 4341,
      "sha256": "30043f18bb3f75165cb59b7220afad659cf605cf5204329ef16a50ebbd0cdae8"
    },
    {
      "relative_path": "experiment_v007/artifacts/confirmation_eval_001_stderr.bin",
      "byte_count": 2492,
      "sha256": "ad54f30cca08d9d90d3d2666ab10eb793ddf10670e45d37dda4842ce9242114b"
    },
    {
      "relative_path": "experiment_v007/artifacts/confirmation_eval_001_stdout.bin",
      "byte_count": 5047,
      "sha256": "c4ce037d27df5245b42e2e326107ffaf708b6157763788d10e60a15ae132fbbc"
    },
    {
      "relative_path": "experiment_v007/artifacts/confirmation_queries.jsonl",
      "byte_count": 936868,
      "sha256": "a4bc9d6d7bf9adad15a6b3644d3f0311d3697ba178c736153bcc785a2118319b"
    },
    {
      "relative_path": "experiment_v007/artifacts/confirmation_raw.jsonl",
      "byte_count": 40927853,
      "sha256": "7f9243c75fff4bb64b03a1b354351d081ead0fc52095a63156611fea9374af7a"
    },
    {
      "relative_path": "experiment_v007/artifacts/confirmation_summary.json",
      "byte_count": 6274,
      "sha256": "42141501ae8c05d7a239a01581bcc10601d37674027a054f4be250d27f56be47"
    },
    {
      "relative_path": "experiment_v007/artifacts/dev_eval_001_execution.json",
      "byte_count": 4477,
      "sha256": "bf8ba85246ea732551c27cb663a93f42b6a27cd7962669cb5d82354ff671ac0e"
    },
    {
      "relative_path": "experiment_v007/artifacts/dev_eval_001_stderr.bin",
      "byte_count": 2492,
      "sha256": "5a6385cc29392dbe9f587a3c2082b097cac764dcf2ee913a6fe91acf402fc88e"
    },
    {
      "relative_path": "experiment_v007/artifacts/dev_eval_001_stdout.bin",
      "byte_count": 5016,
      "sha256": "69b02c0036b3437acb7ab8d368f9dd06f0377022bcd86bda113938d58cf8a40c"
    },
    {
      "relative_path": "experiment_v007/artifacts/development_acquisition_manifest.json",
      "byte_count": 1140,
      "sha256": "46ae061f7b973f311e3c01988707fede21553a011524a977452fdad0b04e11d8"
    },
    {
      "relative_path": "experiment_v007/artifacts/development_corpus.jsonl",
      "byte_count": 8749686,
      "sha256": "2380f54138270106dd20d769bb304f442c861e86986ce23812f0c552d82c0fb4"
    },
    {
      "relative_path": "experiment_v007/artifacts/development_corpus_embeddings.npy",
      "byte_count": 14493824,
      "sha256": "0d93ff18b69a8ceaab09b62e3715f2a9984e611cbd2e5c65ec6e36b59825a67c"
    },
    {
      "relative_path": "experiment_v007/artifacts/development_environment.json",
      "byte_count": 501,
      "sha256": "5248e9b685ce05b53370ff7f83842c929c4f337a7b3748acfe8b6459f3b6a4a4"
    },
    {
      "relative_path": "experiment_v007/artifacts/development_queries.jsonl",
      "byte_count": 965654,
      "sha256": "ab104b33af410eae9e09a60bf717b76bce7d8c908bb3ceae8cfce5a147c4b9a7"
    },
    {
      "relative_path": "experiment_v007/artifacts/development_raw.jsonl",
      "byte_count": 41879447,
      "sha256": "c297efbed9995cfc12e112c6e9b2406df7697e6cda8716578c9c19246fee3762"
    },
    {
      "relative_path": "experiment_v007/artifacts/development_source_acquire_001_execution.json",
      "byte_count": 3097,
      "sha256": "fc08a093c4e2e204c3e62d9c50f350bed30c354edf935d4f003432fedf7bf94d"
    },
    {
      "relative_path": "experiment_v007/artifacts/development_source_acquire_001_stderr.bin",
      "byte_count": 0,
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    },
    {
      "relative_path": "experiment_v007/artifacts/development_source_acquire_001_stdout.bin",
      "byte_count": 1015,
      "sha256": "4546dc6afdc5d79d40e497d5e6cfe2874dca0d560d5223fb00e31c78f1a79d25"
    },
    {
      "relative_path": "experiment_v007/artifacts/development_summary.json",
      "byte_count": 6243,
      "sha256": "cbe49f9951b4f6dc1bad768a78dbd9d8a9c9eb1079228960d0b73c16cbaccb75"
    },
    {
      "relative_path": "experiment_v007/artifacts/main_codex_confirmation_audit.json",
      "byte_count": 2182,
      "sha256": "56f68ee7b4dd81106c4bbba373623f980b5d44cdf702f7a785f5d4b1d0627c11"
    },
    {
      "relative_path": "experiment_v007/artifacts/main_codex_confirmation_audit.py",
      "byte_count": 13560,
      "sha256": "8d082102c145b54ee1c6f36b28f715bc39791c7c9ec6fa23a6311c8193c324cc"
    }
  ]
}
```

## Codex Interpretation

v007 is the execution-only repair of v006: it creates the embeddings output parent before np.save and reuses the exact touched Development acquisition bytes. Development produced 12,000 complete cells and passed the preregistered promotion audit. The previously untouched Confirmation range [207826,208826) was then acquired as 1,000 contiguous rows and a 9,309-document phase corpus; a new Confirmation embedding matrix was generated rather than reusing Development embeddings. The captured Confirmation evaluation exited 0. The foreground caller had earlier returned timeout code 124 while the single runner continued; process inspection prevented a duplicate attempt, and the runner later closed a valid exit-0 capture. The Main Codex independent audit also exited 0 and verified 12,000 unique cells, complete unique corpus-bound top-10 lists, 3,000 deterministic label-disjoint donors, zero target overlap, exact qrel metrics, ten-block effects, bootstrap intervals, and lexical mechanism. BM25 equal-block effect/median/bootstrap are 0.15472698575926586, 0.15881437019579883, and [0.13810078540627505,0.17154230511897298]. MiniLM values are 0.19767190048609523, 0.1985772107226651, and [0.18139115743783601,0.21385848024999743]. Both are positive in all ten blocks; mechanism mean is 0.21566037397225948. The only permitted claim is positive-tool-linked retrieval information in target-aware generated training prompts beyond this frozen three-donor control on the two fixed ranges. This is not a deployable, causal, exhaustive-label, end-to-end, universal, or all-row claim. The frozen Candidate final sentence contains a disclosed stale v006 failure label; actual protocol would freeze v007. The executed bytes were not overwritten. Confirmation success authorizes only a frozen Review Packet and three fresh leaf Reviewers, not Delivery or Ready status.