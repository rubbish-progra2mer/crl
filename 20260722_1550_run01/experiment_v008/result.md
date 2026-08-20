# Experiment Result

```json
{
  "experiment_id": "v008",
  "execution_provenance": "caller_recorded",
  "plan_sha256": "9c9c2046c345e433857fc74f03f9d7e47a25f73ebee7afec942a493c736f8815",
  "candidate_sha256": "3952ebd104e457c10b03ab43b2092695156c66d8c7dfbb628a53725bd13febea",
  "evidence_packet_sha256": "dc66e45036069b3ab310b3ee3e60b929e70a91de5f0994335d09886040882be9",
  "execution": {
    "command": "SINGLE_CAPTURE dev_eval_001; exact argv and 22 declared inputs are in dev_eval_001_execution.json",
    "cwd": "D:\\Desktop\\crl\\20260722_1550_run01\\implementation_v008",
    "exit_code": 1,
    "stdout": "",
    "stderr": "AttributeError: list-valued properties.required reached schema_text value.get before any metric or output was produced.\n",
    "environment": {
      "confirmation_acquired": "false",
      "python": "3.11.15",
      "result_scope": "Development execution failed before metrics"
    }
  },
  "artifacts": [
    {
      "relative_path": "experiment_v008/artifacts/attempts_manifest.json",
      "byte_count": 715,
      "sha256": "2a31a97fe1af1a2b21e78e326b859d7be92860a0f8b3ee50acb7f912ac7af72f"
    },
    {
      "relative_path": "experiment_v008/artifacts/config.json",
      "byte_count": 410,
      "sha256": "999db63c02c0b57e93f9cc6fe9efc47f11a7ff6e7058defd490cbac0a3323c2d"
    },
    {
      "relative_path": "experiment_v008/artifacts/dev_eval_001_execution.json",
      "byte_count": 7891,
      "sha256": "d8d95372e7fc72ef9b8eea68fed2b0f6aa3739e2f82f8e6f5f65f850fc567658"
    },
    {
      "relative_path": "experiment_v008/artifacts/dev_eval_001_stderr.bin",
      "byte_count": 1176,
      "sha256": "93b1311bb429b43e9cfecd868c29f6bbfb85430b5b8cafb8dfcada6a3633bf4b"
    },
    {
      "relative_path": "experiment_v008/artifacts/dev_eval_001_stdout.bin",
      "byte_count": 0,
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    },
    {
      "relative_path": "experiment_v008/artifacts/evaluate.py",
      "byte_count": 32515,
      "sha256": "657b710318b850c11a02bc6ad7b836d19ae8dc348251cdb546043fa8171a6888"
    },
    {
      "relative_path": "experiment_v008/artifacts/input__BFCL_v3_multiple.json",
      "byte_count": 316583,
      "sha256": "aef168155ebd74b7ac2401198b201343bc7d16d7a3d7e0d4e6d8ee82c6969b2a"
    },
    {
      "relative_path": "experiment_v008/artifacts/input__BFCL_v3_multiple_possible_answer.json",
      "byte_count": 32254,
      "sha256": "244e00ce9395df948bcafc7bee64e8f9c87ef70887587d83cae45b13699f3047"
    },
    {
      "relative_path": "experiment_v008/artifacts/input__BFCL_v3_multiple_tool_enrichment.json",
      "byte_count": 582498,
      "sha256": "1be15f014a2d04af06fec2797e4e53f7a335ce46e6bbdc2ec0ef3cabd6074a7b"
    },
    {
      "relative_path": "experiment_v008/artifacts/model_cross__config.json",
      "byte_count": 794,
      "sha256": "380e02c93f431831be65d99a4e7e5f67c133985bf2e77d9d4eba46847190bacc"
    },
    {
      "relative_path": "experiment_v008/artifacts/model_cross__model.safetensors",
      "byte_count": 90870598,
      "sha256": "821d1aa69520101d6e0737f78a042ae25b19e5cb9160701909d10434f4aeb0ae"
    },
    {
      "relative_path": "experiment_v008/artifacts/model_cross__special_tokens_map.json",
      "byte_count": 132,
      "sha256": "3c3507f36dff57bce437223db3b3081d1e2b52ec3e56ee55438193ecb2c94dd6"
    },
    {
      "relative_path": "experiment_v008/artifacts/model_cross__tokenizer.json",
      "byte_count": 711396,
      "sha256": "d241a60d5e8f04cc1b2b3e9ef7a4921b27bf526d9f6050ab90f9267a1f9e5c66"
    },
    {
      "relative_path": "experiment_v008/artifacts/model_cross__tokenizer_config.json",
      "byte_count": 1330,
      "sha256": "a5c2e5a7b1a29a0702cd28c08a399b5ecc110c263009d17f7e3b415f25905fd8"
    },
    {
      "relative_path": "experiment_v008/artifacts/model_cross__vocab.txt",
      "byte_count": 231508,
      "sha256": "07eced375cec144d27c900241f3e339478dec958f92fddbc551f295c992038a3"
    },
    {
      "relative_path": "experiment_v008/artifacts/model_dense__1_Pooling__config.json",
      "byte_count": 190,
      "sha256": "4be450dde3b0273bb9787637cfbd28fe04a7ba6ab9d36ac48e92b11e350ffc23"
    },
    {
      "relative_path": "experiment_v008/artifacts/model_dense__README.md",
      "byte_count": 10502,
      "sha256": "dcd602d2fd35c203a247304a06fec6654a12f7941b739f9221a064fe8dc3b7f0"
    },
    {
      "relative_path": "experiment_v008/artifacts/model_dense__config.json",
      "byte_count": 612,
      "sha256": "953f9c0d463486b10a6871cc2fd59f223b2c70184f49815e7efbcab5d8908b41"
    },
    {
      "relative_path": "experiment_v008/artifacts/model_dense__config_sentence_transformers.json",
      "byte_count": 116,
      "sha256": "061ca9d39661d6c6d6de5ba27f79a1cd5770ea247f8d46412a68a498dc5ac9f3"
    },
    {
      "relative_path": "experiment_v008/artifacts/model_dense__model.safetensors",
      "byte_count": 90868376,
      "sha256": "53aa51172d142c89d9012cce15ae4d6cc0ca6895895114379cacb4fab128d9db"
    },
    {
      "relative_path": "experiment_v008/artifacts/model_dense__modules.json",
      "byte_count": 349,
      "sha256": "84e40c8e006c9b1d6c122e02cba9b02458120b5fb0c87b746c41e0207cf642cf"
    },
    {
      "relative_path": "experiment_v008/artifacts/model_dense__sentence_bert_config.json",
      "byte_count": 53,
      "sha256": "fc1993fde0a95c24ec6c022539d41cf6e2f7c9721e5415d6fb6897472a9cd4b7"
    },
    {
      "relative_path": "experiment_v008/artifacts/model_dense__special_tokens_map.json",
      "byte_count": 112,
      "sha256": "303df45a03609e4ead04bc3dc1536d0ab19b5358db685b6f3da123d05ec200e3"
    },
    {
      "relative_path": "experiment_v008/artifacts/model_dense__tokenizer.json",
      "byte_count": 466247,
      "sha256": "be50c3628f2bf5bb5e3a7f17b1f74611b2561a3a27eeab05e5aa30f411572037"
    },
    {
      "relative_path": "experiment_v008/artifacts/model_dense__tokenizer_config.json",
      "byte_count": 350,
      "sha256": "acb92769e8195aabd29b7b2137a9e6d6e25c476a4f15aa4355c233426c61576b"
    },
    {
      "relative_path": "experiment_v008/artifacts/model_dense__vocab.txt",
      "byte_count": 231508,
      "sha256": "07eced375cec144d27c900241f3e339478dec958f92fddbc551f295c992038a3"
    }
  ]
}
```

## Codex Interpretation

v008 froze the full TPPA program, config, models, and 200-row Development inputs before one real capture. The capture loaded both models, then produced no scientific metric because schema_text treated every properties entry as a parameter object. One observed BFCL tool (multiple_197 / genetic_disorder.diagnose) stores a required-name list at properties.required and nests the family_history schema under symptoms, so value.get raised AttributeError. The runner exited 1 and all five declared outputs remained absent. This is an implementation execution failure, not evidence for or against TPPA. Confirmation was never acquired and Review is not authorized. v009 may reuse the same touched Development bytes with only a strict normalization of this observed schema layout; every scientific rule, model, grid, metric, gate, and untouched Confirmation source remains unchanged.