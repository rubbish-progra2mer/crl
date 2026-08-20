# Experiment Result

```json
{
  "experiment_id": "v009",
  "execution_provenance": "caller_recorded",
  "plan_sha256": "7ff4d681b7a47cb631107468c0bdc0ce09defd6ee70065e6f6ecdad5ec717664",
  "candidate_sha256": "182c5a684c80b5ea391b1693c499ae0a5a5036a15f0656e521e1cd1f53e2c109",
  "evidence_packet_sha256": "17fe03a8c21b615df093fa09764474a2ba4590c778c2fae16f9bc4d986971898",
  "execution": {
    "command": "SINGLE_DEVELOPMENT_CAPTURE dev_eval_001 plus independent dev_audit_001; exact argv are in execution.json and dev_audit_001_execution.json",
    "cwd": "D:\\Desktop\\crl\\20260722_1550_run01\\implementation_v009",
    "exit_code": 0,
    "stdout": "Development capture completed; independent raw audit passed; preregistered Development gates did not all pass.\n",
    "stderr": "",
    "environment": {
      "gpu": "NVIDIA GeForce RTX 5060 Ti",
      "python": "3.11.15",
      "result_scope": "Development screen; Confirmation not acquired"
    }
  },
  "artifacts": [
    {
      "relative_path": "experiment_v009/artifacts/attempts_manifest.json",
      "byte_count": 1786,
      "sha256": "1711050f3bf887fdf22211e8e9028bfa0bb3e6cf012781a1d60b92e9046b357b"
    },
    {
      "relative_path": "experiment_v009/artifacts/config.json",
      "byte_count": 410,
      "sha256": "999db63c02c0b57e93f9cc6fe9efc47f11a7ff6e7058defd490cbac0a3323c2d"
    },
    {
      "relative_path": "experiment_v009/artifacts/dev_audit_001_execution.json",
      "byte_count": 4175,
      "sha256": "2d504878558bdaf317d592a26db44ad093b7c73f0a9ff0ac69a8746b704b010d"
    },
    {
      "relative_path": "experiment_v009/artifacts/dev_audit_001_stderr.bin",
      "byte_count": 0,
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    },
    {
      "relative_path": "experiment_v009/artifacts/dev_audit_001_stdout.bin",
      "byte_count": 48,
      "sha256": "5c5d27b8a16639331b59d82792131623c0350dbb6dae400867670a6525d8c65b"
    },
    {
      "relative_path": "experiment_v009/artifacts/development_environment.json",
      "byte_count": 3243,
      "sha256": "9d13a2ae2c5252d59f581e0ab125b7dc95acaef987d729f5bad3a1913dfa4515"
    },
    {
      "relative_path": "experiment_v009/artifacts/development_query_hashes.json",
      "byte_count": 14003,
      "sha256": "823b1cb3d37cb6485f5c4e0bbc6ed4033f1cf8053febe2b24ce3639d49b516da"
    },
    {
      "relative_path": "experiment_v009/artifacts/development_raw.jsonl",
      "byte_count": 3215288,
      "sha256": "db92c7867d7366656bcca58441ca04102913b18c9adf63c2bdac1605ec85c871"
    },
    {
      "relative_path": "experiment_v009/artifacts/development_selected_params.json",
      "byte_count": 298,
      "sha256": "80b3a484924b8fcdf1b1a5a4d035c9beecb133e363de3bcff78484fd14ff0aa4"
    },
    {
      "relative_path": "experiment_v009/artifacts/development_summary.json",
      "byte_count": 96440,
      "sha256": "7b96477d01703d3f4f912b800c1aadfe3be0f724ee0d045819460d5042ec7475"
    },
    {
      "relative_path": "experiment_v009/artifacts/evaluate.py",
      "byte_count": 33630,
      "sha256": "d9c03c2b43bf452da2d62c4b3e6ccb05c2ef3a8abbe82be3be6dcd708e9fe9cd"
    },
    {
      "relative_path": "experiment_v009/artifacts/execution.json",
      "byte_count": 8459,
      "sha256": "46bd9fec2f67ed3f0274ffe0c705cd4acd21b20a35a5f1177c06bb0431fbfc1a"
    },
    {
      "relative_path": "experiment_v009/artifacts/input__BFCL_v3_multiple.json",
      "byte_count": 316583,
      "sha256": "aef168155ebd74b7ac2401198b201343bc7d16d7a3d7e0d4e6d8ee82c6969b2a"
    },
    {
      "relative_path": "experiment_v009/artifacts/input__BFCL_v3_multiple_possible_answer.json",
      "byte_count": 32254,
      "sha256": "244e00ce9395df948bcafc7bee64e8f9c87ef70887587d83cae45b13699f3047"
    },
    {
      "relative_path": "experiment_v009/artifacts/input__BFCL_v3_multiple_tool_enrichment.json",
      "byte_count": 582498,
      "sha256": "1be15f014a2d04af06fec2797e4e53f7a335ce46e6bbdc2ec0ef3cabd6074a7b"
    },
    {
      "relative_path": "experiment_v009/artifacts/main_codex_development_audit.json",
      "byte_count": 2032,
      "sha256": "db36c2dfd11b25e714620ef89b373816f577e684110c1e9a20bdf2d1ab025aac"
    },
    {
      "relative_path": "experiment_v009/artifacts/main_codex_development_audit.py",
      "byte_count": 16402,
      "sha256": "a7c04320de00f9538a4e5a107fce58226c3f2ed0006384e59180937e537dde1b"
    },
    {
      "relative_path": "experiment_v009/artifacts/model_cross__config.json",
      "byte_count": 794,
      "sha256": "380e02c93f431831be65d99a4e7e5f67c133985bf2e77d9d4eba46847190bacc"
    },
    {
      "relative_path": "experiment_v009/artifacts/model_cross__model.safetensors",
      "byte_count": 90870598,
      "sha256": "821d1aa69520101d6e0737f78a042ae25b19e5cb9160701909d10434f4aeb0ae"
    },
    {
      "relative_path": "experiment_v009/artifacts/model_cross__special_tokens_map.json",
      "byte_count": 132,
      "sha256": "3c3507f36dff57bce437223db3b3081d1e2b52ec3e56ee55438193ecb2c94dd6"
    },
    {
      "relative_path": "experiment_v009/artifacts/model_cross__tokenizer.json",
      "byte_count": 711396,
      "sha256": "d241a60d5e8f04cc1b2b3e9ef7a4921b27bf526d9f6050ab90f9267a1f9e5c66"
    },
    {
      "relative_path": "experiment_v009/artifacts/model_cross__tokenizer_config.json",
      "byte_count": 1330,
      "sha256": "a5c2e5a7b1a29a0702cd28c08a399b5ecc110c263009d17f7e3b415f25905fd8"
    },
    {
      "relative_path": "experiment_v009/artifacts/model_cross__vocab.txt",
      "byte_count": 231508,
      "sha256": "07eced375cec144d27c900241f3e339478dec958f92fddbc551f295c992038a3"
    },
    {
      "relative_path": "experiment_v009/artifacts/model_dense__1_Pooling__config.json",
      "byte_count": 190,
      "sha256": "4be450dde3b0273bb9787637cfbd28fe04a7ba6ab9d36ac48e92b11e350ffc23"
    },
    {
      "relative_path": "experiment_v009/artifacts/model_dense__README.md",
      "byte_count": 10502,
      "sha256": "dcd602d2fd35c203a247304a06fec6654a12f7941b739f9221a064fe8dc3b7f0"
    },
    {
      "relative_path": "experiment_v009/artifacts/model_dense__config.json",
      "byte_count": 612,
      "sha256": "953f9c0d463486b10a6871cc2fd59f223b2c70184f49815e7efbcab5d8908b41"
    },
    {
      "relative_path": "experiment_v009/artifacts/model_dense__config_sentence_transformers.json",
      "byte_count": 116,
      "sha256": "061ca9d39661d6c6d6de5ba27f79a1cd5770ea247f8d46412a68a498dc5ac9f3"
    },
    {
      "relative_path": "experiment_v009/artifacts/model_dense__model.safetensors",
      "byte_count": 90868376,
      "sha256": "53aa51172d142c89d9012cce15ae4d6cc0ca6895895114379cacb4fab128d9db"
    },
    {
      "relative_path": "experiment_v009/artifacts/model_dense__modules.json",
      "byte_count": 349,
      "sha256": "84e40c8e006c9b1d6c122e02cba9b02458120b5fb0c87b746c41e0207cf642cf"
    },
    {
      "relative_path": "experiment_v009/artifacts/model_dense__sentence_bert_config.json",
      "byte_count": 53,
      "sha256": "fc1993fde0a95c24ec6c022539d41cf6e2f7c9721e5415d6fb6897472a9cd4b7"
    },
    {
      "relative_path": "experiment_v009/artifacts/model_dense__special_tokens_map.json",
      "byte_count": 112,
      "sha256": "303df45a03609e4ead04bc3dc1536d0ab19b5358db685b6f3da123d05ec200e3"
    },
    {
      "relative_path": "experiment_v009/artifacts/model_dense__tokenizer.json",
      "byte_count": 466247,
      "sha256": "be50c3628f2bf5bb5e3a7f17b1f74611b2561a3a27eeab05e5aa30f411572037"
    },
    {
      "relative_path": "experiment_v009/artifacts/model_dense__tokenizer_config.json",
      "byte_count": 350,
      "sha256": "acb92769e8195aabd29b7b2137a9e6d6e25c476a4f15aa4355c233426c61576b"
    },
    {
      "relative_path": "experiment_v009/artifacts/model_dense__vocab.txt",
      "byte_count": 231508,
      "sha256": "07eced375cec144d27c900241f3e339478dec958f92fddbc551f295c992038a3"
    },
    {
      "relative_path": "experiment_v009/artifacts/stderr.bin",
      "byte_count": 276,
      "sha256": "67cc41545e0e1b4422038e1f8d250bc9f4b75065348ddf7170046ba5450c0488"
    },
    {
      "relative_path": "experiment_v009/artifacts/stdout.bin",
      "byte_count": 170,
      "sha256": "87997eb81d857cf425cff0f40cac7be50c9fe0a3e0affe25e2730b99e3b5a7fe"
    }
  ]
}
```

## Codex Interpretation

v009 executed the frozen 200-row Development screen and a separate Main Codex raw audit. The audit independently verified 200 rows, 1,121 tools, 7,120 edge cells, 1,815 assignments, every ranking, all 384 grid rows, both bootstrap intervals, and the parameter-contrast subset with zero numerical discrepancy. Cross-encoder top-1/MRR were 0.930/0.9591667 and TPPA were 0.935/0.9625: top-1 +0.005, MRR +0.0033333, one correction, no regressions, and MRR bootstrap [0.0,0.0091667]. The frozen +0.02 top-1 and strictly positive MRR-lower conditions failed. TPPA and relaxed reusable matching had identical top-1 and MRR on all rows despite internal assignment and ranking differences, so the proposed capacity/null delta did not improve the final outcome. Main Codex does not authorize Confirmation. Confirmation bytes remain unacquired, no Review Packet is authorized, and v010 must use a scientifically different failure and changed computation rather than lower thresholds or retune TPPA.