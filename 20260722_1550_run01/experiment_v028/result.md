# Experiment Result

```json
{
  "experiment_id": "v028",
  "execution_provenance": "caller_recorded",
  "plan_sha256": "aeb61660302ebdd6a48bd6f87c5427a59b1a3ee3845fdb41f52d6593e79ec6ab",
  "candidate_sha256": "249a050c1539e579bb120a9f13399f9ddcc49a8e73728d2c733a33415d0dddb3",
  "evidence_packet_sha256": "ba3e98ff68703cb062ef3ad01bd1321cf30c031ea84e8ff9027e47c56b854972",
  "execution": {
    "command": "D:\\Desktop\\crl\\crl_agent_v3\\.venv\\python.exe D:\\Desktop\\crl\\20260722_1550_run01\\experiment_v028\\artifacts\\program.py --phase development --config D:\\Desktop\\crl\\20260722_1550_run01\\experiment_v028\\artifacts\\config.json --candidate D:\\Desktop\\crl\\20260722_1550_run01\\experiment_v028\\artifacts\\candidate_v028.md --evidence-packet D:\\Desktop\\crl\\20260722_1550_run01\\experiment_v028\\artifacts\\evidence_packet_v028.md --expanded D:\\Desktop\\crl\\20260722_1550_run01\\experiment_v028\\artifacts\\development_expanded.jsonl --questions D:\\Desktop\\crl\\20260722_1550_run01\\experiment_v028\\artifacts\\development_questions.jsonl --gold D:\\Desktop\\crl\\20260722_1550_run01\\experiment_v028\\artifacts\\development_gold.jsonl --model-dir D:\\Desktop\\crl\\20260722_1550_run01\\experiment_v028\\model_cross --output-dir D:\\Desktop\\crl\\20260722_1550_run01\\experiment_v028\\dev_output_001",
    "cwd": "D:\\Desktop\\crl\\20260722_1550_run01\\experiment_v028\\artifacts",
    "exit_code": 0,
    "stdout": "{\"candidate_top1\": 0.935, \"gates\": \"3/7\", \"phase\": \"development\", \"strongest_comparator\": \"pointwise_fields\", \"top1_delta\": 0.0}\r\n",
    "stderr": "\rLoading weights:   0%|          | 0/105 [00:00<?, ?it/s]\rLoading weights: 100%|��������������������| 105/105 [00:00<00:00, 5031.04it/s]\r\n",
    "environment": {
      "development_duration_seconds": "11.45576119999896",
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
      "relative_path": "experiment_v028/artifacts/acquire_confirmation.py",
      "byte_count": 3307,
      "sha256": "11405eb06a2683537a0788dde535cc9efa7a3d2dcc1e1a8adb6248784f86bd5c"
    },
    {
      "relative_path": "experiment_v028/artifacts/attempts_manifest_v027.json",
      "byte_count": 688,
      "sha256": "6dca4b6af2ee489684832ae01e99d3439b3f38dae01bbcc0ea17bcdad1a31570"
    },
    {
      "relative_path": "experiment_v028/artifacts/attempts_manifest_v028.json",
      "byte_count": 1873,
      "sha256": "603c4f130ab7cc8742a12d6d6651f1d227d5e0a571f7acb0938f353c860dde27"
    },
    {
      "relative_path": "experiment_v028/artifacts/audit.py",
      "byte_count": 30460,
      "sha256": "37d93688c96618d2423a77fc3377e21023a023f9a8ac71dd510092a018530674"
    },
    {
      "relative_path": "experiment_v028/artifacts/candidate_v009.md",
      "byte_count": 8816,
      "sha256": "182c5a684c80b5ea391b1693c499ae0a5a5036a15f0656e521e1cd1f53e2c109"
    },
    {
      "relative_path": "experiment_v028/artifacts/candidate_v028.md",
      "byte_count": 2913,
      "sha256": "249a050c1539e579bb120a9f13399f9ddcc49a8e73728d2c733a33415d0dddb3"
    },
    {
      "relative_path": "experiment_v028/artifacts/config.json",
      "byte_count": 1901,
      "sha256": "8c64c396dd095a689cc7da63036d92b6b9fcde02c7cc6b8016616e174d28a656"
    },
    {
      "relative_path": "experiment_v028/artifacts/development_audit_execution.json",
      "byte_count": 6923,
      "sha256": "3545f5983d6daa7d3967c3ae1b595a35a521c1e187bbc3518464a019e66641cf"
    },
    {
      "relative_path": "experiment_v028/artifacts/development_audit_report.json",
      "byte_count": 836,
      "sha256": "3bc0ad342565e3bd8184998a7599d93d1b3918e845b14e23a37f9985e1beef5a"
    },
    {
      "relative_path": "experiment_v028/artifacts/development_audit_stderr.bin",
      "byte_count": 138,
      "sha256": "8e472b8d129210681f6d59b862c2a490d695cfbcdb160c09604949f1d397ff4c"
    },
    {
      "relative_path": "experiment_v028/artifacts/development_audit_stdout.bin",
      "byte_count": 208,
      "sha256": "6df3af19fa792c9270235fb717f6c86d54bbea2a18d3532899f1ec3d0e85f188"
    },
    {
      "relative_path": "experiment_v028/artifacts/development_environment.json",
      "byte_count": 346,
      "sha256": "9ddb1e9cb16558e0a4db15932f90620fbfe3cf42ff35f29241c6fb9afccba658"
    },
    {
      "relative_path": "experiment_v028/artifacts/development_execution.json",
      "byte_count": 6580,
      "sha256": "3e5feadddc6edf4c6b9fd231903bba1fc19bdc9c259a19c87535d95375a87b94"
    },
    {
      "relative_path": "experiment_v028/artifacts/development_expanded.jsonl",
      "byte_count": 582498,
      "sha256": "1be15f014a2d04af06fec2797e4e53f7a335ce46e6bbdc2ec0ef3cabd6074a7b"
    },
    {
      "relative_path": "experiment_v028/artifacts/development_gold.jsonl",
      "byte_count": 32254,
      "sha256": "244e00ce9395df948bcafc7bee64e8f9c87ef70887587d83cae45b13699f3047"
    },
    {
      "relative_path": "experiment_v028/artifacts/development_model.joblib",
      "byte_count": 26837,
      "sha256": "d04d1853500b599c929d0e33e36de58be8d86d1a080df7287153c4281d19379d"
    },
    {
      "relative_path": "experiment_v028/artifacts/development_query_hashes.json",
      "byte_count": 14003,
      "sha256": "823b1cb3d37cb6485f5c4e0bbc6ed4033f1cf8053febe2b24ce3639d49b516da"
    },
    {
      "relative_path": "experiment_v028/artifacts/development_questions.jsonl",
      "byte_count": 316583,
      "sha256": "aef168155ebd74b7ac2401198b201343bc7d16d7a3d7e0d4e6d8ee82c6969b2a"
    },
    {
      "relative_path": "experiment_v028/artifacts/development_raw.jsonl",
      "byte_count": 1920831,
      "sha256": "2cb8d4502a0a8478e015f608a1ca71d00e467eea3712336c6d59743db347b604"
    },
    {
      "relative_path": "experiment_v028/artifacts/development_stderr.bin",
      "byte_count": 138,
      "sha256": "2ee7ff9cd6a44fcbff04848c3269e4ba61e7d5c1666cf3b29a68cac6f030b2c0"
    },
    {
      "relative_path": "experiment_v028/artifacts/development_stdout.bin",
      "byte_count": 130,
      "sha256": "50ea79005935266b39e2e0a5aa35d764dca362e3907d675d51b457185a44e575"
    },
    {
      "relative_path": "experiment_v028/artifacts/development_summary.json",
      "byte_count": 5659,
      "sha256": "5b6d88370fc262f150acd4e12e46b6c1f66a3587a2be7db870ff1b936d0b3850"
    },
    {
      "relative_path": "experiment_v028/artifacts/dtdr_2026_findings_acl_1680.pdf",
      "byte_count": 1215907,
      "sha256": "099f012ad01bd8b24154093c2bfe55ad9eabdb668ddc7ecf0c2735e01d89a833"
    },
    {
      "relative_path": "experiment_v028/artifacts/evidence_packet_v028.md",
      "byte_count": 8908,
      "sha256": "ba3e98ff68703cb062ef3ad01bd1321cf30c031ea84e8ff9027e47c56b854972"
    },
    {
      "relative_path": "experiment_v028/artifacts/implementation_audit_v027.md",
      "byte_count": 5040,
      "sha256": "e6f6dbe077b6596a0971c31e4e937d456261fd79e822d8f38c2c6d9996b9797f"
    },
    {
      "relative_path": "experiment_v028/artifacts/implementation_audit_v028.md",
      "byte_count": 2075,
      "sha256": "02ee8307b464dc2b316507e272cac62607c3cdb16cc908226727a2a52046f3a2"
    },
    {
      "relative_path": "experiment_v028/artifacts/model_cross__config.json",
      "byte_count": 794,
      "sha256": "380e02c93f431831be65d99a4e7e5f67c133985bf2e77d9d4eba46847190bacc"
    },
    {
      "relative_path": "experiment_v028/artifacts/model_cross__model.safetensors",
      "byte_count": 90870598,
      "sha256": "821d1aa69520101d6e0737f78a042ae25b19e5cb9160701909d10434f4aeb0ae"
    },
    {
      "relative_path": "experiment_v028/artifacts/model_cross__special_tokens_map.json",
      "byte_count": 132,
      "sha256": "3c3507f36dff57bce437223db3b3081d1e2b52ec3e56ee55438193ecb2c94dd6"
    },
    {
      "relative_path": "experiment_v028/artifacts/model_cross__tokenizer.json",
      "byte_count": 711396,
      "sha256": "d241a60d5e8f04cc1b2b3e9ef7a4921b27bf526d9f6050ab90f9267a1f9e5c66"
    },
    {
      "relative_path": "experiment_v028/artifacts/model_cross__tokenizer_config.json",
      "byte_count": 1330,
      "sha256": "a5c2e5a7b1a29a0702cd28c08a399b5ecc110c263009d17f7e3b415f25905fd8"
    },
    {
      "relative_path": "experiment_v028/artifacts/model_cross__vocab.txt",
      "byte_count": 231508,
      "sha256": "07eced375cec144d27c900241f3e339478dec958f92fddbc551f295c992038a3"
    },
    {
      "relative_path": "experiment_v028/artifacts/nearest_prior_v009.md",
      "byte_count": 4015,
      "sha256": "4255a0753ed2e4ad643f813926dbe3f3a75676315c138542e33c408891434e80"
    },
    {
      "relative_path": "experiment_v028/artifacts/nearest_prior_v028.md",
      "byte_count": 549,
      "sha256": "48efa93fc197f0d87f93d5a0dc2ccf1c2981c7b8d3a58977052a485edf907de0"
    },
    {
      "relative_path": "experiment_v028/artifacts/p084_function_calling_robustness.pdf",
      "byte_count": 402510,
      "sha256": "8276bcab484eef370bc63afca580ea19d8f6e2ccc6c2afcdaf684225d5e635c7"
    },
    {
      "relative_path": "experiment_v028/artifacts/p086_meta_tool.pdf",
      "byte_count": 955613,
      "sha256": "02064499a8345eb333e4fdd71abaa5ee69133af5be7b81626ba09816f48d194b"
    },
    {
      "relative_path": "experiment_v028/artifacts/p087_tool_document_expansion.pdf",
      "byte_count": 1096332,
      "sha256": "0e6dc98171a7ada43eb7b2a415099853afb090f29c25887d512660501d343eff"
    },
    {
      "relative_path": "experiment_v028/artifacts/preparation_failure_v027.md",
      "byte_count": 1544,
      "sha256": "fe1f0b279f89f08b7d46b1b6080e3662884b4443c4587a3093af9818984da374"
    },
    {
      "relative_path": "experiment_v028/artifacts/preparation_note_v028.md",
      "byte_count": 1019,
      "sha256": "074e32b622d4b9873849f546c58a3ba0925a6c74bb46e02ca08bb8ccba71c218"
    },
    {
      "relative_path": "experiment_v028/artifacts/problem_v028.md",
      "byte_count": 864,
      "sha256": "9951f4cb537e79ebb56925f1bbd093c07ca911e2f5a621a98f360c2e611ea81e"
    },
    {
      "relative_path": "experiment_v028/artifacts/program.py",
      "byte_count": 29323,
      "sha256": "9a13e18bfffab4d44b5d185c003a8c8fbe7639de2ddb8fb6a6d5cf985351d9fb"
    },
    {
      "relative_path": "experiment_v028/artifacts/promotion_audit_v026.md",
      "byte_count": 2256,
      "sha256": "1ef9d8162f325d7bd584eff5dd02a8cc2a750dc31ecfa73cb9b7e14872268c0d"
    },
    {
      "relative_path": "experiment_v028/artifacts/promotion_audit_v028.md",
      "byte_count": 1370,
      "sha256": "3f281c3fe8f31607f9aa0ffac1dc0d43ad09085c89bde11482d7fee380711828"
    },
    {
      "relative_path": "experiment_v028/artifacts/raw_analysis_v028.md",
      "byte_count": 3255,
      "sha256": "62b3a2c13628538c450ab2b23fe6390f2228f875dc42a9a5c7962682db2ce89d"
    },
    {
      "relative_path": "experiment_v028/artifacts/research_map_v009.md",
      "byte_count": 9852,
      "sha256": "a497c8e64147d520406c055f9d05bc7d5e77d3c5dcdc07f1459af81d3c58739b"
    },
    {
      "relative_path": "experiment_v028/artifacts/research_map_v028.md",
      "byte_count": 4860,
      "sha256": "e1cb8a5cf8f540fd7251d0a3d0053d8ae17c67c81b23c98b17c849615019e10d"
    },
    {
      "relative_path": "experiment_v028/artifacts/result_v009.md",
      "byte_count": 9289,
      "sha256": "e6cfdeb170900e0921274c98fea0a58d8625dd145fe18ab6cde1df8b33978d5f"
    },
    {
      "relative_path": "experiment_v028/artifacts/result_v026.md",
      "byte_count": 13427,
      "sha256": "1e93bf3a5980f3851ed2f8180b9d33984cdbfe4b323b0794c7cb8e8652e029f6"
    },
    {
      "relative_path": "experiment_v028/artifacts/result_v027.md",
      "byte_count": 8573,
      "sha256": "a3ed21d9c3d73c492193e30c35d14fbe6eac0e359bf64c0c9d7a59e421279c62"
    },
    {
      "relative_path": "experiment_v028/artifacts/run_local_experiment.py",
      "byte_count": 4338,
      "sha256": "410a620d0734613036f4fea4bc017c0cd1d0de293e1a3d4577c75eec584eaa4a"
    },
    {
      "relative_path": "experiment_v028/artifacts/selection_context_v028.md",
      "byte_count": 879,
      "sha256": "bd86a94c3cdb63f00517ccc932ea483240e9b769791546a8b9405f92509ff80d"
    },
    {
      "relative_path": "experiment_v028/artifacts/test_mfcr.py",
      "byte_count": 4713,
      "sha256": "b5e6c8733588346043d0f9b991ca9b575951d232002f09fdf0530a794b5c4429"
    },
    {
      "relative_path": "experiment_v028/artifacts/toolrerank_2403.06551.pdf",
      "byte_count": 757931,
      "sha256": "dc1d0cf7537401d602aef27160b5f854b688bf607e51d3c0e33febccc66237d4"
    }
  ]
}
```

## Codex Interpretation

The single frozen Development execution and independent audit are mechanically valid. MFCR reached top-1 0.935 and MRR 0.9629166666666668, but pointwise_fields and equal_fields achieved the identical top-1 and MRR, with identical per-row reciprocal rank on all 200 queries. Four prospective gates failed; only 3/7 passed. The main Codex therefore records NO_GO_FOR_CONFIRMATION. The untouched BFCL v4 files were not acquired or read, and no Reviewer or Delivery is authorized.