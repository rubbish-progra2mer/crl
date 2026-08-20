# Experiment Result

```json
{
  "experiment_id": "v027",
  "execution_provenance": "caller_recorded",
  "plan_sha256": "dad4de05714ad90d11db5349a8c80fe81fb9abaaf9e775a1b40021c09b59ade2",
  "candidate_sha256": "249a050c1539e579bb120a9f13399f9ddcc49a8e73728d2c733a33415d0dddb3",
  "evidence_packet_sha256": "ba3e98ff68703cb062ef3ad01bd1321cf30c031ea84e8ff9027e47c56b854972",
  "execution": {
    "command": "PowerShell 5.1 deterministic preparation: New-Item -ItemType Directory -LiteralPath <captures>; New-Item -ItemType Directory -LiteralPath <model_cross>; copy and verify six frozen model files",
    "cwd": "D:\\Desktop\\crl\\crl_agent_v3",
    "exit_code": 1,
    "stdout": "",
    "stderr": "New-Item: A parameter cannot be found that matches parameter name 'LiteralPath'. Subsequent copies failed because both destination directories were absent.",
    "environment": {
      "powershell": "Windows PowerShell 5.1",
      "python": "3.11.15",
      "python_executable": "D:\\Desktop\\crl\\crl_agent_v3\\.venv\\python.exe",
      "scope": "post_plan_directory_preparation_only",
      "system_status": "DEVELOPMENT_NOT_COMMISSIONED"
    }
  },
  "artifacts": [
    {
      "relative_path": "experiment_v027/artifacts/acquire_confirmation.py",
      "byte_count": 3307,
      "sha256": "11405eb06a2683537a0788dde535cc9efa7a3d2dcc1e1a8adb6248784f86bd5c"
    },
    {
      "relative_path": "experiment_v027/artifacts/attempts_manifest_v027.json",
      "byte_count": 688,
      "sha256": "6dca4b6af2ee489684832ae01e99d3439b3f38dae01bbcc0ea17bcdad1a31570"
    },
    {
      "relative_path": "experiment_v027/artifacts/audit.py",
      "byte_count": 30460,
      "sha256": "37d93688c96618d2423a77fc3377e21023a023f9a8ac71dd510092a018530674"
    },
    {
      "relative_path": "experiment_v027/artifacts/candidate_v009.md",
      "byte_count": 8816,
      "sha256": "182c5a684c80b5ea391b1693c499ae0a5a5036a15f0656e521e1cd1f53e2c109"
    },
    {
      "relative_path": "experiment_v027/artifacts/candidate_v027.md",
      "byte_count": 2913,
      "sha256": "249a050c1539e579bb120a9f13399f9ddcc49a8e73728d2c733a33415d0dddb3"
    },
    {
      "relative_path": "experiment_v027/artifacts/config.json",
      "byte_count": 1901,
      "sha256": "cd18ad8b645a2c82d98aa9009596303d10097426da2fa7649e84964500bb30c9"
    },
    {
      "relative_path": "experiment_v027/artifacts/development_expanded.jsonl",
      "byte_count": 582498,
      "sha256": "1be15f014a2d04af06fec2797e4e53f7a335ce46e6bbdc2ec0ef3cabd6074a7b"
    },
    {
      "relative_path": "experiment_v027/artifacts/development_gold.jsonl",
      "byte_count": 32254,
      "sha256": "244e00ce9395df948bcafc7bee64e8f9c87ef70887587d83cae45b13699f3047"
    },
    {
      "relative_path": "experiment_v027/artifacts/development_questions.jsonl",
      "byte_count": 316583,
      "sha256": "aef168155ebd74b7ac2401198b201343bc7d16d7a3d7e0d4e6d8ee82c6969b2a"
    },
    {
      "relative_path": "experiment_v027/artifacts/dtdr_2026_findings_acl_1680.pdf",
      "byte_count": 1215907,
      "sha256": "099f012ad01bd8b24154093c2bfe55ad9eabdb668ddc7ecf0c2735e01d89a833"
    },
    {
      "relative_path": "experiment_v027/artifacts/evidence_packet_v027.md",
      "byte_count": 8908,
      "sha256": "ba3e98ff68703cb062ef3ad01bd1321cf30c031ea84e8ff9027e47c56b854972"
    },
    {
      "relative_path": "experiment_v027/artifacts/implementation_audit_v027.md",
      "byte_count": 5040,
      "sha256": "e6f6dbe077b6596a0971c31e4e937d456261fd79e822d8f38c2c6d9996b9797f"
    },
    {
      "relative_path": "experiment_v027/artifacts/model_cross__config.json",
      "byte_count": 794,
      "sha256": "380e02c93f431831be65d99a4e7e5f67c133985bf2e77d9d4eba46847190bacc"
    },
    {
      "relative_path": "experiment_v027/artifacts/model_cross__model.safetensors",
      "byte_count": 90870598,
      "sha256": "821d1aa69520101d6e0737f78a042ae25b19e5cb9160701909d10434f4aeb0ae"
    },
    {
      "relative_path": "experiment_v027/artifacts/model_cross__special_tokens_map.json",
      "byte_count": 132,
      "sha256": "3c3507f36dff57bce437223db3b3081d1e2b52ec3e56ee55438193ecb2c94dd6"
    },
    {
      "relative_path": "experiment_v027/artifacts/model_cross__tokenizer.json",
      "byte_count": 711396,
      "sha256": "d241a60d5e8f04cc1b2b3e9ef7a4921b27bf526d9f6050ab90f9267a1f9e5c66"
    },
    {
      "relative_path": "experiment_v027/artifacts/model_cross__tokenizer_config.json",
      "byte_count": 1330,
      "sha256": "a5c2e5a7b1a29a0702cd28c08a399b5ecc110c263009d17f7e3b415f25905fd8"
    },
    {
      "relative_path": "experiment_v027/artifacts/model_cross__vocab.txt",
      "byte_count": 231508,
      "sha256": "07eced375cec144d27c900241f3e339478dec958f92fddbc551f295c992038a3"
    },
    {
      "relative_path": "experiment_v027/artifacts/nearest_prior_v009.md",
      "byte_count": 4015,
      "sha256": "4255a0753ed2e4ad643f813926dbe3f3a75676315c138542e33c408891434e80"
    },
    {
      "relative_path": "experiment_v027/artifacts/nearest_prior_v027.md",
      "byte_count": 2217,
      "sha256": "1f96a9551ccd6642e7bbb4602d58fa2f71e9c2c689d529427d6200dc9bee0630"
    },
    {
      "relative_path": "experiment_v027/artifacts/p084_function_calling_robustness.pdf",
      "byte_count": 402510,
      "sha256": "8276bcab484eef370bc63afca580ea19d8f6e2ccc6c2afcdaf684225d5e635c7"
    },
    {
      "relative_path": "experiment_v027/artifacts/p086_meta_tool.pdf",
      "byte_count": 955613,
      "sha256": "02064499a8345eb333e4fdd71abaa5ee69133af5be7b81626ba09816f48d194b"
    },
    {
      "relative_path": "experiment_v027/artifacts/p087_tool_document_expansion.pdf",
      "byte_count": 1096332,
      "sha256": "0e6dc98171a7ada43eb7b2a415099853afb090f29c25887d512660501d343eff"
    },
    {
      "relative_path": "experiment_v027/artifacts/preparation_failure_v027.md",
      "byte_count": 1544,
      "sha256": "fe1f0b279f89f08b7d46b1b6080e3662884b4443c4587a3093af9818984da374"
    },
    {
      "relative_path": "experiment_v027/artifacts/problem_v027.md",
      "byte_count": 864,
      "sha256": "9951f4cb537e79ebb56925f1bbd093c07ca911e2f5a621a98f360c2e611ea81e"
    },
    {
      "relative_path": "experiment_v027/artifacts/program.py",
      "byte_count": 29323,
      "sha256": "58e2493aaf5a9bd1f7063d28ed7153ebbc7885b53e6c205deda9d21132e91da6"
    },
    {
      "relative_path": "experiment_v027/artifacts/promotion_audit_v026.md",
      "byte_count": 2256,
      "sha256": "1ef9d8162f325d7bd584eff5dd02a8cc2a750dc31ecfa73cb9b7e14872268c0d"
    },
    {
      "relative_path": "experiment_v027/artifacts/research_map_v009.md",
      "byte_count": 9852,
      "sha256": "a497c8e64147d520406c055f9d05bc7d5e77d3c5dcdc07f1459af81d3c58739b"
    },
    {
      "relative_path": "experiment_v027/artifacts/research_map_v027.md",
      "byte_count": 4860,
      "sha256": "e1cb8a5cf8f540fd7251d0a3d0053d8ae17c67c81b23c98b17c849615019e10d"
    },
    {
      "relative_path": "experiment_v027/artifacts/result_v009.md",
      "byte_count": 9289,
      "sha256": "e6cfdeb170900e0921274c98fea0a58d8625dd145fe18ab6cde1df8b33978d5f"
    },
    {
      "relative_path": "experiment_v027/artifacts/result_v026.md",
      "byte_count": 13427,
      "sha256": "1e93bf3a5980f3851ed2f8180b9d33984cdbfe4b323b0794c7cb8e8652e029f6"
    },
    {
      "relative_path": "experiment_v027/artifacts/run_local_experiment.py",
      "byte_count": 4338,
      "sha256": "410a620d0734613036f4fea4bc017c0cd1d0de293e1a3d4577c75eec584eaa4a"
    },
    {
      "relative_path": "experiment_v027/artifacts/selection_context_v027.md",
      "byte_count": 1759,
      "sha256": "f0462c31ef4224aee4e2be64d4291774311024c917e4ce1e82963fcdc314256f"
    },
    {
      "relative_path": "experiment_v027/artifacts/test_mfcr.py",
      "byte_count": 4713,
      "sha256": "b5e6c8733588346043d0f9b991ca9b575951d232002f09fdf0530a794b5c4429"
    },
    {
      "relative_path": "experiment_v027/artifacts/toolrerank_2403.06551.pdf",
      "byte_count": 757931,
      "sha256": "dc1d0cf7537401d602aef27160b5f854b688bf607e51d3c0e33febccc66237d4"
    }
  ]
}
```

## Codex Interpretation

The post-Plan preparation command exited 1 before creating any directory or copying any model byte. A separate read-only verification found captures, model_cross, dev_output_001 and dev_audit_output_001 all absent; Development and Confirmation did not start. The frozen Plan prohibits a same-version retry, so v027 is closed as NO_GO_FOR_SAME_VERSION_RETRY_PREPARATION_FAILURE and only an execution-only v028 correction may proceed.