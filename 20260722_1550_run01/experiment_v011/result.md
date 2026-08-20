# Experiment Result

```json
{
  "experiment_id": "v011",
  "execution_provenance": "caller_recorded",
  "plan_sha256": "7bf6fed25dd8dd5d2c44b30438088bfb4a358ae9debd3b18886996b0921f26be",
  "candidate_sha256": "acf6a6fab1f66622907bbf7c338bd388b8c871609bb151c718f06fb52476eb20",
  "evidence_packet_sha256": "212c7513d99878567d9339e9c1596e6ab726511efed436f15bd52719856bc1c7",
  "execution": {
    "command": "D:\\Desktop\\crl\\crl_agent_v3\\.venv\\python.exe D:\\Desktop\\crl\\20260722_1550_run01\\implementation_v011\\evaluate.py --phase development --config D:\\Desktop\\crl\\20260722_1550_run01\\implementation_v011\\config.json --expanded D:\\Desktop\\crl\\20260722_1550_run01\\implementation_v011\\inputs\\BFCL_v3_multiple_tool_enrichment.json --questions D:\\Desktop\\crl\\20260722_1550_run01\\implementation_v011\\inputs\\BFCL_v3_multiple.json --gold D:\\Desktop\\crl\\20260722_1550_run01\\implementation_v011\\inputs\\BFCL_v3_multiple_possible_answer.json --output-dir D:\\Desktop\\crl\\20260722_1550_run01\\experiment_v011\\work\\dev_eval_001",
    "cwd": "D:\\Desktop\\crl\\20260722_1550_run01\\implementation_v011",
    "exit_code": 0,
    "stdout": "{\"all_gates_passed\": false, \"anchored_delta\": 0.0, \"anchored_top1\": 0.93, \"baseline_top1\": 0.93, \"items\": 200, \"phase\": \"development\", \"unanchored_top1\": 0.93}\r\n",
    "stderr": "\rLoading weights:   0%|          | 0/105 [00:00<?, ?it/s]\rLoading weights: 100%|��������������������| 105/105 [00:00<00:00, 5797.05it/s]\r\n",
    "environment": {
      "gpu": "NVIDIA GeForce RTX 5060 Ti",
      "nvidia_driver": "591.86",
      "python": "3.11.15",
      "python_executable": "D:\\Desktop\\crl\\crl_agent_v3\\.venv\\python.exe",
      "torch": "2.12.0+cu130",
      "torch_cuda": "13.0"
    }
  },
  "artifacts": [
    {
      "relative_path": "experiment_v011/artifacts/config.json",
      "byte_count": 249,
      "sha256": "2df83a3f7a5e804dc2d3f2a503db50e50062a495ebd5cb1d24fd869a984c6ab7"
    },
    {
      "relative_path": "experiment_v011/artifacts/dev_audit_001_execution.json",
      "byte_count": 3523,
      "sha256": "a602a887706e41c4be30450744a4dd59e0e30b671f7054978bc619b26392c805"
    },
    {
      "relative_path": "experiment_v011/artifacts/dev_audit_001_stderr.bin",
      "byte_count": 0,
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    },
    {
      "relative_path": "experiment_v011/artifacts/dev_audit_001_stdout.bin",
      "byte_count": 114,
      "sha256": "1e5ce6e36fe53c1ad111b9747684bf6b7ff82d468b90f61a0f01492fc5fea787"
    },
    {
      "relative_path": "experiment_v011/artifacts/development_environment.json",
      "byte_count": 1436,
      "sha256": "dd5ba2bd297be0fee89c5740b8b956f59df98f2b63997f0a6b149ffd3fd54c12"
    },
    {
      "relative_path": "experiment_v011/artifacts/development_query_hashes.json",
      "byte_count": 14003,
      "sha256": "823b1cb3d37cb6485f5c4e0bbc6ed4033f1cf8053febe2b24ce3639d49b516da"
    },
    {
      "relative_path": "experiment_v011/artifacts/development_raw.jsonl",
      "byte_count": 10338855,
      "sha256": "e37f226db1e3e3d777edaad93ac332ad3ee1e829bcb8537cfab47cae0e3a034a"
    },
    {
      "relative_path": "experiment_v011/artifacts/development_selected_params.json",
      "byte_count": 26173,
      "sha256": "6898778cd773df4cf8e705edf44e7d45b1c182761c3f9074e91f8f1a1020a3c4"
    },
    {
      "relative_path": "experiment_v011/artifacts/development_summary.json",
      "byte_count": 4536,
      "sha256": "20262ccf4a03f9eb6d7097f73ee732760b1ebe346d83d28ef153817cc63dc2be"
    },
    {
      "relative_path": "experiment_v011/artifacts/evaluate.py",
      "byte_count": 28013,
      "sha256": "38d0320e37a960cbaaf64e20b27eb95d8f6f5704f459ca333742f0bb0b983874"
    },
    {
      "relative_path": "experiment_v011/artifacts/execution.json",
      "byte_count": 5901,
      "sha256": "ce9cbaddc118739298b5f087da47a347b7c63d5f0277a94808e3e18627bab914"
    },
    {
      "relative_path": "experiment_v011/artifacts/input__BFCL_v3_multiple.json",
      "byte_count": 316583,
      "sha256": "aef168155ebd74b7ac2401198b201343bc7d16d7a3d7e0d4e6d8ee82c6969b2a"
    },
    {
      "relative_path": "experiment_v011/artifacts/input__BFCL_v3_multiple_possible_answer.json",
      "byte_count": 32254,
      "sha256": "244e00ce9395df948bcafc7bee64e8f9c87ef70887587d83cae45b13699f3047"
    },
    {
      "relative_path": "experiment_v011/artifacts/input__BFCL_v3_multiple_tool_enrichment.json",
      "byte_count": 582498,
      "sha256": "1be15f014a2d04af06fec2797e4e53f7a335ce46e6bbdc2ec0ef3cabd6074a7b"
    },
    {
      "relative_path": "experiment_v011/artifacts/main_codex_development_audit.json",
      "byte_count": 2593,
      "sha256": "52c8ed78f4f0b4db9c6b466c066b34702fe7a840cc6c2926221772c6dc8e2ecf"
    },
    {
      "relative_path": "experiment_v011/artifacts/main_codex_development_audit.py",
      "byte_count": 10853,
      "sha256": "06f554224c16ab13c8a8b49514ccbdd824fd9131725260664ddfa75cbdfca17f"
    },
    {
      "relative_path": "experiment_v011/artifacts/model_cross__config.json",
      "byte_count": 794,
      "sha256": "380e02c93f431831be65d99a4e7e5f67c133985bf2e77d9d4eba46847190bacc"
    },
    {
      "relative_path": "experiment_v011/artifacts/model_cross__model.safetensors",
      "byte_count": 90870598,
      "sha256": "821d1aa69520101d6e0737f78a042ae25b19e5cb9160701909d10434f4aeb0ae"
    },
    {
      "relative_path": "experiment_v011/artifacts/model_cross__special_tokens_map.json",
      "byte_count": 132,
      "sha256": "3c3507f36dff57bce437223db3b3081d1e2b52ec3e56ee55438193ecb2c94dd6"
    },
    {
      "relative_path": "experiment_v011/artifacts/model_cross__tokenizer.json",
      "byte_count": 711396,
      "sha256": "d241a60d5e8f04cc1b2b3e9ef7a4921b27bf526d9f6050ab90f9267a1f9e5c66"
    },
    {
      "relative_path": "experiment_v011/artifacts/model_cross__tokenizer_config.json",
      "byte_count": 1330,
      "sha256": "a5c2e5a7b1a29a0702cd28c08a399b5ecc110c263009d17f7e3b415f25905fd8"
    },
    {
      "relative_path": "experiment_v011/artifacts/model_cross__vocab.txt",
      "byte_count": 231508,
      "sha256": "07eced375cec144d27c900241f3e339478dec958f92fddbc551f295c992038a3"
    },
    {
      "relative_path": "experiment_v011/artifacts/stderr.bin",
      "byte_count": 138,
      "sha256": "ca15dcad3ba3a1908e1e7cd554b54906b6c58a3c2e01d2adc32f056c9d983db8"
    },
    {
      "relative_path": "experiment_v011/artifacts/stdout.bin",
      "byte_count": 161,
      "sha256": "2305dbd3b8de50a1609f75a8a8a3d9b9c161747b353596ccb1af0abe79b96b7b"
    }
  ]
}
```

## Codex Interpretation

# v011 Development Result and Main Codex Promotion Audit

## Actual execution

The frozen Development capture completed with scientific exit code `0` in `10.2021047` seconds. `execution.json` SHA-256 is `ce9cbaddc118739298b5f087da47a347b7c63d5f0277a94808e3e18627bab914`. It binds 11 frozen inputs and five newly created declared outputs.

The independent Main Codex audit capture also exited `0`. Its report SHA-256 is `52c8ed78f4f0b4db9c6b466c066b34702fe7a840cc6c2926221772c6dc8e2ecf`. It recomputed 200 rows, 1,121 tools, 384-dimensional vectors, all recorded rankings, top-1, MRR, corrections/regressions, and both 20,000-resample paired bootstrap intervals. Every recomputed value matched `summary.json`; every source hash matched the Development capture.

## Development metrics

- Frozen cross-encoder: top-1 `0.930`, MRR `0.9591666667`.
- Unanchored related-negative residual: top-1 `0.930`, MRR `0.9591666667`.
- Thin-anchored residual: top-1 `0.930`, MRR `0.9591666667`.
- Candidate minus cross-encoder: top-1 `0.000`, MRR `0.000`, top-1 bootstrap `[0.0, 0.0]`, MRR bootstrap `[0.0, 0.0]`, corrections `0`, regressions `0`.
- Unanchored comparator minus cross-encoder: the same zeros.

Both learned scores differ from the frozen scores on all 200 rows and alter the complete ranking on 22 rows, but no change moves the first relevant tool. Hence both top-1 and best-gold MRR remain exactly unchanged.

## Proposed-delta audit

Every fold-specific anchor scale and the full-Development anchor scale equals `1.0`. The thin-menu non-reversal cap never binds. Therefore the Candidate and its closest-composition comparator are computationally identical on every held-out score, and the unique proposed delta has no observed effect.

The full adapter vector relation `anchored_vector = anchor_scale * unanchored_vector` has maximum absolute error `0.0`. The OOF fold vectors themselves were not persisted, so the stored raw held-out scores and rankings are independently auditable but the OOF fitting path cannot be reconstructed from frozen bytes without rerunning the frozen program. This is an additional reproducibility limitation and cannot rescue a zero final-result delta.

## Candidate Promotion Audit

- The baseline reproduces the previously observed P084 ranking failure: fourteen of 200 rows miss top-1.
- Development and any future Confirmation would be exact-query/file separated only; P084 is already outcome-exposed and shares one generation pipeline.
- The Candidate does not improve the final target variable or any best-gold rank. Its 22 lower-order changes are not a proxy that justifies Confirmation.
- Relative to the fair unanchored comparator, the unique anchor delta never activates.
- Four decisive conditions fail: top-1 improvement, positive MRR lower bound, positive net corrections, and anchor-specific regression reduction. The correction-retention condition is vacuously true because both methods have zero corrections.

Main Codex disposition: `DEVELOPMENT_NOT_PROMOTED`. Confirmation remains unacquired and unread. No Review Packet, Reviewer, Decision, or Delivery is authorized for v011. The version is frozen and the same Run must continue with v012 using a scientifically different computation; no L2, margin-fraction, fold, or anchor-threshold retuning is allowed.
