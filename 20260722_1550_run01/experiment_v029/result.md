# Experiment Result

```json
{
  "experiment_id": "v029",
  "execution_provenance": "caller_recorded",
  "plan_sha256": "e0e16874dc10d305ab6680d06e43ea3c484a27789d4f9ad898299fb4c68b71d8",
  "candidate_sha256": "2ea2c1ef080a1edc1b81c94161e8f215931cb4fe4fb3449580baf8ef9814c244",
  "evidence_packet_sha256": "1317d24f9a2e63826b47f330fb0510f6567ab82c3df9fea899399c5c748dea6d",
  "execution": {
    "command": "D:\\Desktop\\crl\\crl_agent_v3\\.venv\\python.exe D:\\Desktop\\crl\\20260722_1550_run01\\experiment_v029\\artifacts\\program.py --phase development --config D:\\Desktop\\crl\\20260722_1550_run01\\experiment_v029\\artifacts\\config.json --candidate D:\\Desktop\\crl\\20260722_1550_run01\\experiment_v029\\artifacts\\candidate_v029.md --evidence-packet D:\\Desktop\\crl\\20260722_1550_run01\\experiment_v029\\artifacts\\evidence_packet_v029.md --expanded D:\\Desktop\\crl\\20260722_1550_run01\\experiment_v029\\artifacts\\development_expanded.jsonl --questions D:\\Desktop\\crl\\20260722_1550_run01\\experiment_v029\\artifacts\\development_questions.jsonl --gold D:\\Desktop\\crl\\20260722_1550_run01\\experiment_v029\\artifacts\\development_gold.jsonl --model-dir D:\\Desktop\\crl\\20260722_1550_run01\\experiment_v029\\model_cross --output-dir D:\\Desktop\\crl\\20260722_1550_run01\\experiment_v029\\dev_output_001",
    "cwd": "D:\\Desktop\\crl\\20260722_1550_run01\\experiment_v029\\artifacts",
    "exit_code": 0,
    "stdout": "{\"candidate_top1\": 0.905, \"gates\": \"0/7\", \"phase\": \"development\", \"strongest_comparator\": \"full_schema\", \"top1_delta\": -0.015}\r\n",
    "stderr": "\rLoading weights:   0%|          | 0/105 [00:00<?, ?it/s]\rLoading weights: 100%|��������������������| 105/105 [00:00<00:00, 6754.42it/s]\r\n",
    "environment": {
      "development_duration_seconds": "10.970545399999537",
      "gpu": "NVIDIA GeForce RTX 5060 Ti",
      "independent_audit": "AUDIT_OK",
      "python": "3.11.15",
      "python_executable": "D:\\Desktop\\crl\\crl_agent_v3\\.venv\\python.exe",
      "system_status": "DEVELOPMENT_NOT_COMMISSIONED",
      "torch": "2.12.0+cu130",
      "torch_cuda": "13.0"
    }
  },
  "artifacts": [
    {
      "relative_path": "experiment_v029/artifacts/acquire_confirmation.py",
      "byte_count": 3307,
      "sha256": "11405eb06a2683537a0788dde535cc9efa7a3d2dcc1e1a8adb6248784f86bd5c"
    },
    {
      "relative_path": "experiment_v029/artifacts/attempts_manifest_v028.json",
      "byte_count": 1873,
      "sha256": "603c4f130ab7cc8742a12d6d6651f1d227d5e0a571f7acb0938f353c860dde27"
    },
    {
      "relative_path": "experiment_v029/artifacts/attempts_manifest_v029.json",
      "byte_count": 1114,
      "sha256": "00c3d3b3dc46c1a739a9bc02bcd9b03a3efc0c610d8faac44de685fd164199d4"
    },
    {
      "relative_path": "experiment_v029/artifacts/audit.py",
      "byte_count": 27397,
      "sha256": "be43956b4099bbc8d37b6a775e40ee3f8419566e4dfbc91077c0715dca1f7308"
    },
    {
      "relative_path": "experiment_v029/artifacts/candidate_v029.md",
      "byte_count": 2187,
      "sha256": "2ea2c1ef080a1edc1b81c94161e8f215931cb4fe4fb3449580baf8ef9814c244"
    },
    {
      "relative_path": "experiment_v029/artifacts/config.json",
      "byte_count": 1879,
      "sha256": "48fc9344c937edf5007f2aabb71619bfcf070eba3274a19bbf5c19d1ab5e4431"
    },
    {
      "relative_path": "experiment_v029/artifacts/development_audit_execution.json",
      "byte_count": 6592,
      "sha256": "1bd8e77d442f32369766af10492bef6ac409f225f353af458c24b044fbdfec46"
    },
    {
      "relative_path": "experiment_v029/artifacts/development_audit_report.json",
      "byte_count": 749,
      "sha256": "336ff99c91ecff3ce925c7739bd9b8a116165daaab4edac06eaf73fda4083af1"
    },
    {
      "relative_path": "experiment_v029/artifacts/development_audit_stderr.bin",
      "byte_count": 138,
      "sha256": "40ff8f496c8219a9d9c55884e19e5f95195109b02e604fa39273f56c5471f43c"
    },
    {
      "relative_path": "experiment_v029/artifacts/development_audit_stdout.bin",
      "byte_count": 207,
      "sha256": "a80d969611dbb393d979fd1f41d9e9096151efa1d1006b2d4743bfc0fe54a647"
    },
    {
      "relative_path": "experiment_v029/artifacts/development_environment.json",
      "byte_count": 298,
      "sha256": "a7cc390735317c203866302eb2e3332a816284299d181ae7de9699715e1f168d"
    },
    {
      "relative_path": "experiment_v029/artifacts/development_execution.json",
      "byte_count": 6253,
      "sha256": "3075e5bef184403d6b3d14097ef98abfdbf3e7defb7d208e14003b37fea2d2f5"
    },
    {
      "relative_path": "experiment_v029/artifacts/development_expanded.jsonl",
      "byte_count": 582498,
      "sha256": "1be15f014a2d04af06fec2797e4e53f7a335ce46e6bbdc2ec0ef3cabd6074a7b"
    },
    {
      "relative_path": "experiment_v029/artifacts/development_gold.jsonl",
      "byte_count": 32254,
      "sha256": "244e00ce9395df948bcafc7bee64e8f9c87ef70887587d83cae45b13699f3047"
    },
    {
      "relative_path": "experiment_v029/artifacts/development_query_hashes.json",
      "byte_count": 14003,
      "sha256": "823b1cb3d37cb6485f5c4e0bbc6ed4033f1cf8053febe2b24ce3639d49b516da"
    },
    {
      "relative_path": "experiment_v029/artifacts/development_questions.jsonl",
      "byte_count": 316583,
      "sha256": "aef168155ebd74b7ac2401198b201343bc7d16d7a3d7e0d4e6d8ee82c6969b2a"
    },
    {
      "relative_path": "experiment_v029/artifacts/development_raw.jsonl",
      "byte_count": 2237103,
      "sha256": "f69c56403fcce9e417c565d92ba6f1e1063c77d257b34e4e0820193f9b8b3a6a"
    },
    {
      "relative_path": "experiment_v029/artifacts/development_stderr.bin",
      "byte_count": 138,
      "sha256": "fa1b3a7efa2b832f173132b7574e1dcf883787ce660334f5ba965f2a628f71dc"
    },
    {
      "relative_path": "experiment_v029/artifacts/development_stdout.bin",
      "byte_count": 128,
      "sha256": "7fd575e99c227db2ded870f9b64b5104e46b4b5d0a64b43fe5828b3583fb24d8"
    },
    {
      "relative_path": "experiment_v029/artifacts/development_summary.json",
      "byte_count": 19207,
      "sha256": "2b0622cfaa3b892f6df6f7ce938d7fb5279d8ab22cc29e44ba7160ce3af05c86"
    },
    {
      "relative_path": "experiment_v029/artifacts/evidence_packet_v029.md",
      "byte_count": 8908,
      "sha256": "1317d24f9a2e63826b47f330fb0510f6567ab82c3df9fea899399c5c748dea6d"
    },
    {
      "relative_path": "experiment_v029/artifacts/implementation_audit_v029.md",
      "byte_count": 3063,
      "sha256": "29b45c61e9e091b3ccd79ce2b5c1d7f8399fbe48cc19625844ce85d006a30052"
    },
    {
      "relative_path": "experiment_v029/artifacts/jtpro_2026_findings_acl_2017.pdf",
      "byte_count": 2591454,
      "sha256": "f564463c7e64bb2980f1d2b38bf5bedb25b31b8cf5bba7d6ae36818f90e9ad6b"
    },
    {
      "relative_path": "experiment_v029/artifacts/magicselector_2607.17751.pdf",
      "byte_count": 714284,
      "sha256": "bce125f5d225d72bba71bbe9a5ace065bb79815c7980359be0422e3e0b538527"
    },
    {
      "relative_path": "experiment_v029/artifacts/model_cross__config.json",
      "byte_count": 794,
      "sha256": "380e02c93f431831be65d99a4e7e5f67c133985bf2e77d9d4eba46847190bacc"
    },
    {
      "relative_path": "experiment_v029/artifacts/model_cross__model.safetensors",
      "byte_count": 90870598,
      "sha256": "821d1aa69520101d6e0737f78a042ae25b19e5cb9160701909d10434f4aeb0ae"
    },
    {
      "relative_path": "experiment_v029/artifacts/model_cross__special_tokens_map.json",
      "byte_count": 132,
      "sha256": "3c3507f36dff57bce437223db3b3081d1e2b52ec3e56ee55438193ecb2c94dd6"
    },
    {
      "relative_path": "experiment_v029/artifacts/model_cross__tokenizer.json",
      "byte_count": 711396,
      "sha256": "d241a60d5e8f04cc1b2b3e9ef7a4921b27bf526d9f6050ab90f9267a1f9e5c66"
    },
    {
      "relative_path": "experiment_v029/artifacts/model_cross__tokenizer_config.json",
      "byte_count": 1330,
      "sha256": "a5c2e5a7b1a29a0702cd28c08a399b5ecc110c263009d17f7e3b415f25905fd8"
    },
    {
      "relative_path": "experiment_v029/artifacts/model_cross__vocab.txt",
      "byte_count": 231508,
      "sha256": "07eced375cec144d27c900241f3e339478dec958f92fddbc551f295c992038a3"
    },
    {
      "relative_path": "experiment_v029/artifacts/nearest_prior_v029.md",
      "byte_count": 1805,
      "sha256": "d10843ed0d9b7b52687165201d218417edaeaaf525d6bcb7acdb71f0c85aea8c"
    },
    {
      "relative_path": "experiment_v029/artifacts/p084_function_calling_robustness.pdf",
      "byte_count": 402510,
      "sha256": "8276bcab484eef370bc63afca580ea19d8f6e2ccc6c2afcdaf684225d5e635c7"
    },
    {
      "relative_path": "experiment_v029/artifacts/p087_tool_document_expansion.pdf",
      "byte_count": 1096332,
      "sha256": "0e6dc98171a7ada43eb7b2a415099853afb090f29c25887d512660501d343eff"
    },
    {
      "relative_path": "experiment_v029/artifacts/problem_v029.md",
      "byte_count": 742,
      "sha256": "00d875a3c31b4db89daf37d2a46868a0c323d7c96d5d84089aa8fad88a539a9f"
    },
    {
      "relative_path": "experiment_v029/artifacts/program.py",
      "byte_count": 24374,
      "sha256": "2a77cfc2cd4f3b5f0d65ba6a9a4c08541dd7318edafabd39b72c92abdcfe74d5"
    },
    {
      "relative_path": "experiment_v029/artifacts/promotion_audit_v028.md",
      "byte_count": 1370,
      "sha256": "3f281c3fe8f31607f9aa0ffac1dc0d43ad09085c89bde11482d7fee380711828"
    },
    {
      "relative_path": "experiment_v029/artifacts/promotion_audit_v029.md",
      "byte_count": 891,
      "sha256": "e0b423d7767e5c5c331eccc5f501599dfafb8bd83c40fc0276646dbe4a206c57"
    },
    {
      "relative_path": "experiment_v029/artifacts/raw_analysis_v028.md",
      "byte_count": 3255,
      "sha256": "62b3a2c13628538c450ab2b23fe6390f2228f875dc42a9a5c7962682db2ce89d"
    },
    {
      "relative_path": "experiment_v029/artifacts/raw_analysis_v029.md",
      "byte_count": 2502,
      "sha256": "987e5b54b2f1abe9243b31d846685bdf8513ab9bc77fe7f2d6019c07295425d1"
    },
    {
      "relative_path": "experiment_v029/artifacts/research_map_v029.md",
      "byte_count": 3426,
      "sha256": "4fb035a11b34fa75a6a54a86c61db3be581e078cd7d756e2c69df975d0c97b5f"
    },
    {
      "relative_path": "experiment_v029/artifacts/result_v028.md",
      "byte_count": 13245,
      "sha256": "f002cdb9f4dd2dcd33e8163c22581cc6a4c3c63ad961e9a3297de33628a20724"
    },
    {
      "relative_path": "experiment_v029/artifacts/run_local_experiment.py",
      "byte_count": 4338,
      "sha256": "410a620d0734613036f4fea4bc017c0cd1d0de293e1a3d4577c75eec584eaa4a"
    },
    {
      "relative_path": "experiment_v029/artifacts/selection_context_v029.md",
      "byte_count": 1323,
      "sha256": "44e1e9a0b65b9e4001fb1467fa560b300a3fe75a6beac2ca4169baccd57fce23"
    },
    {
      "relative_path": "experiment_v029/artifacts/test_dcn.py",
      "byte_count": 4060,
      "sha256": "1425f3e239f12cefb6dd899b5afeff12389d3bc03888cfa79c8b596a278d8d89"
    },
    {
      "relative_path": "experiment_v029/artifacts/toolprm_2026_acl_855.pdf",
      "byte_count": 455786,
      "sha256": "f781b56a766748c261ab4c6c6804a6f3f85f7795c6894eaac9408e9dcecd0d55"
    },
    {
      "relative_path": "experiment_v029/artifacts/toolrerank_2403.06551.pdf",
      "byte_count": 757931,
      "sha256": "dc1d0cf7537401d602aef27160b5f854b688bf607e51d3c0e33febccc66237d4"
    }
  ]
}
```

## Codex Interpretation

The single fixed Development execution and independent replay are mechanically valid. Dual Counterfactual Necessity achieved top-1 0.905 and MRR 0.9428333333333333, below the unchanged full-schema control at 0.920 and 0.9554166666666667. It passed 0/7 prospective gates, with two corrections and five regressions. The main Codex records NO_GO_FOR_CONFIRMATION. Untouched BFCL v4 was not acquired or read; no Reviewer or Delivery is authorized.