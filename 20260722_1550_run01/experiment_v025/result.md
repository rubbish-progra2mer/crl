# Experiment Result

```json
{
  "experiment_id": "v025",
  "execution_provenance": "caller_recorded",
  "plan_sha256": "0492b9448340acf13c775910ad980db884a66c49fd3d7d4b33cfb882eeb2d86d",
  "candidate_sha256": "d7af6362080666bdecc927c8f2c65ea0894d2b7e1756d6434b61107ae8156c60",
  "evidence_packet_sha256": "87d886ba29d9096e35537802de1388f48fb2e9ef5f3a87b957044dedab99128f",
  "execution": {
    "command": "D:\\Desktop\\crl\\crl_agent_v3\\.venv\\python.exe D:\\Desktop\\crl\\20260722_1550_run01\\experiment_v025\\artifacts\\program.py --phase development --config D:\\Desktop\\crl\\20260722_1550_run01\\experiment_v025\\artifacts\\config.json --dataset D:\\Desktop\\crl\\20260722_1550_run01\\experiment_v025\\artifacts\\development_dataset.jsonl --input-manifest D:\\Desktop\\crl\\20260722_1550_run01\\experiment_v025\\artifacts\\development_manifest.json --base-module D:\\Desktop\\crl\\20260722_1550_run01\\experiment_v025\\artifacts\\base_v012.py --output-dir D:\\Desktop\\crl\\20260722_1550_run01\\experiment_v025\\dev_output_001",
    "cwd": "D:\\Desktop\\crl\\20260722_1550_run01\\experiment_v025\\artifacts",
    "exit_code": 0,
    "stdout": "{\"auc_delta\": -0.010212697519199176, \"candidate_auc\": 0.9054923404768606, \"gates\": \"2/7\", \"phase\": \"development\", \"strongest_comparator\": \"anchor_bag\"}\r\n",
    "stderr": "",
    "environment": {
      "cuda_available": "True",
      "elapsed_seconds": "592.3889084999973",
      "gpu": "NVIDIA GeForce RTX 5060 Ti",
      "joblib": "1.5.3",
      "numpy": "2.3.5",
      "python": "3.11.15",
      "python_executable": "D:\\Desktop\\crl\\crl_agent_v3\\.venv\\python.exe",
      "scikit_learn": "1.9.0",
      "scipy": "1.16.0",
      "torch": "2.12.0+cu130",
      "torch_cuda": "13.0",
      "training_device": "cpu"
    }
  },
  "artifacts": [
    {
      "relative_path": "experiment_v025/artifacts/acquire.py",
      "byte_count": 12438,
      "sha256": "cf87ec4994081b4516695806b471daf75e923fe511d0b67d05b4ab126d34e836"
    },
    {
      "relative_path": "experiment_v025/artifacts/agentrx_2602.02475.pdf",
      "byte_count": 616888,
      "sha256": "59680fd631934d6ad3046108a504195e8cd70066bdefbfb3561b7731f7d22923"
    },
    {
      "relative_path": "experiment_v025/artifacts/attempts_manifest_v024.json",
      "byte_count": 1496,
      "sha256": "521e02d57e11075b5cc1cc1fe528a317ff1384dee9d6eca8adea3764f472db09"
    },
    {
      "relative_path": "experiment_v025/artifacts/attempts_manifest_v025.json",
      "byte_count": 2124,
      "sha256": "791557bcc2051606d53b9050d74324ac01b48a39c05ffea6f008abe444c28ef8"
    },
    {
      "relative_path": "experiment_v025/artifacts/audit.py",
      "byte_count": 21053,
      "sha256": "8eade0d127843da37545327622e7be7627592400ca696c05c63aa1a1dcd66c72"
    },
    {
      "relative_path": "experiment_v025/artifacts/audit_report.json",
      "byte_count": 851,
      "sha256": "3922edb5384626cc054de7cbda41250315ef0a2396815e6eb5dd3a8cc3746114"
    },
    {
      "relative_path": "experiment_v025/artifacts/base_v012.py",
      "byte_count": 39154,
      "sha256": "a29b8aace75bf5505620fab71c982e296e045cb1590a20a5a9c19a63c233d78d"
    },
    {
      "relative_path": "experiment_v025/artifacts/candidate_v025.md",
      "byte_count": 2123,
      "sha256": "d7af6362080666bdecc927c8f2c65ea0894d2b7e1756d6434b61107ae8156c60"
    },
    {
      "relative_path": "experiment_v025/artifacts/cheap_reward_hacking_2606.08893.pdf",
      "byte_count": 1278533,
      "sha256": "c5fd945125b1b6cd4739b2aacf150156bbfc8e47aff2d7240ea05ed697075ce0"
    },
    {
      "relative_path": "experiment_v025/artifacts/config.json",
      "byte_count": 1200,
      "sha256": "e34c812e78d1476e6a283d89452f3f61b3cd7bb74859d11a29fa2202bacf9983"
    },
    {
      "relative_path": "experiment_v025/artifacts/dev_acquire_001_execution.json",
      "byte_count": 2313,
      "sha256": "de25142d206cee91c5f0dd46143cdfec8adc19a37ceb0afd524dd4d6223b6fb0"
    },
    {
      "relative_path": "experiment_v025/artifacts/dev_acquire_001_stderr.bin",
      "byte_count": 0,
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    },
    {
      "relative_path": "experiment_v025/artifacts/dev_acquire_001_stdout.bin",
      "byte_count": 132,
      "sha256": "8d1bc45fcd7edbe70aa7d7978aa1e7724c317abc112a8d36016e2aa148983831"
    },
    {
      "relative_path": "experiment_v025/artifacts/dev_audit_001_execution.json",
      "byte_count": 4434,
      "sha256": "ecf7c79025b6b0e1052f051925e6d477a2af492738125f157a936f67827b957a"
    },
    {
      "relative_path": "experiment_v025/artifacts/dev_audit_001_stderr.bin",
      "byte_count": 0,
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    },
    {
      "relative_path": "experiment_v025/artifacts/dev_audit_001_stdout.bin",
      "byte_count": 130,
      "sha256": "6cee1c04fab014d4251af9f7f79ad0bee95b2583e6b33917c8df0893eeba01b4"
    },
    {
      "relative_path": "experiment_v025/artifacts/development_dataset.jsonl",
      "byte_count": 28801199,
      "sha256": "d5daecba36e3e8f9c6bbe60c8e2b13e6206290d8ca7cddcf4a8cc27c2f82274f"
    },
    {
      "relative_path": "experiment_v025/artifacts/development_manifest.json",
      "byte_count": 312237,
      "sha256": "aa20ea73e71b7a3b9a41d444c8a8b7997216f0b85e53fbc5cffb663e25b67932"
    },
    {
      "relative_path": "experiment_v025/artifacts/evidence_packet_v025.md",
      "byte_count": 4336,
      "sha256": "87d886ba29d9096e35537802de1388f48fb2e9ef5f3a87b957044dedab99128f"
    },
    {
      "relative_path": "experiment_v025/artifacts/execution.json",
      "byte_count": 4115,
      "sha256": "192e288640a0b80342e7e6e90b3292d44a1aa6a03a48359f2b6283b0ee5af64e"
    },
    {
      "relative_path": "experiment_v025/artifacts/implementation_audit_v025.md",
      "byte_count": 2006,
      "sha256": "e7b14242732c2d8c23119e50046d47d5d0fe283f8fc4603b42b7a46d9f88dca3"
    },
    {
      "relative_path": "experiment_v025/artifacts/model.joblib",
      "byte_count": 29191174,
      "sha256": "6daad8b97b6f0b3be02657ef47575c9962064c1d65566428a3b82bb36074eb18"
    },
    {
      "relative_path": "experiment_v025/artifacts/nearest_prior_v024.md",
      "byte_count": 2997,
      "sha256": "4c01037ddd330b41a84f80805239a64ce55774ee92b209a11e7595ba18ac61e5"
    },
    {
      "relative_path": "experiment_v025/artifacts/nearest_prior_v025.md",
      "byte_count": 1136,
      "sha256": "046f1f85659bfc4323f5c1831570e092341c93e3ac7cc78845a729b53ddda95b"
    },
    {
      "relative_path": "experiment_v025/artifacts/plan_v024.md",
      "byte_count": 10252,
      "sha256": "30e6a7071686e036a7738b9af4d42b5f705949862b906740032799cd71c1f217"
    },
    {
      "relative_path": "experiment_v025/artifacts/problem_v025.md",
      "byte_count": 1309,
      "sha256": "bd2d11c1f861ae98e43fee39aedda28de18a05456cdf69d536563cccdf4c9d1e"
    },
    {
      "relative_path": "experiment_v025/artifacts/program.py",
      "byte_count": 23422,
      "sha256": "e71a820adfe798b0732a07dbfe1e31286cad7eab43c229309a9522e34ea44ab6"
    },
    {
      "relative_path": "experiment_v025/artifacts/promotion_audit_v024.md",
      "byte_count": 1537,
      "sha256": "993cdab1120f8c51d8d47beba7c5cf19a7d6fd0fd817fb12aeb256b91e00dc4d"
    },
    {
      "relative_path": "experiment_v025/artifacts/promotion_audit_v025.md",
      "byte_count": 2140,
      "sha256": "9893b56f6957e613cd6e1123927138bd36dc05311830192ed1b74883f5577ae8"
    },
    {
      "relative_path": "experiment_v025/artifacts/raw_analysis_v025.md",
      "byte_count": 3388,
      "sha256": "71a5e53f986f5778a87e752542849a543e22c0f945cf8b8dc1a32f8aa6775c5b"
    },
    {
      "relative_path": "experiment_v025/artifacts/raw_predictions.jsonl",
      "byte_count": 697437,
      "sha256": "abeacda9eeba0a9099a599e41eeea4383a772a60ec60143471eb12faf7329af6"
    },
    {
      "relative_path": "experiment_v025/artifacts/research_map_v025.md",
      "byte_count": 5124,
      "sha256": "a775c4e8ac122a482e316699516b319decf4780f0997c2154c5b28f2f87bc034"
    },
    {
      "relative_path": "experiment_v025/artifacts/result_v024.md",
      "byte_count": 7742,
      "sha256": "5a4dbd7636c6056e286efacf1292d22f2ce28e8bcd15d798e624dfeafa435d28"
    },
    {
      "relative_path": "experiment_v025/artifacts/run_local_experiment.py",
      "byte_count": 4338,
      "sha256": "410a620d0734613036f4fea4bc017c0cd1d0de293e1a3d4577c75eec584eaa4a"
    },
    {
      "relative_path": "experiment_v025/artifacts/selection_context_v025.md",
      "byte_count": 1375,
      "sha256": "10cb5ed5c9e67e8eef8c35f926b2cf51ce56c849e7616c97913d274a11fed282"
    },
    {
      "relative_path": "experiment_v025/artifacts/source_records.jsonl",
      "byte_count": 359885,
      "sha256": "7602a0d70ef9650cc7b91f821ca38299f91db246de1ad24331541ce34d6e1cc3"
    },
    {
      "relative_path": "experiment_v025/artifacts/stderr.bin",
      "byte_count": 0,
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    },
    {
      "relative_path": "experiment_v025/artifacts/stdout.bin",
      "byte_count": 153,
      "sha256": "6e2776d416c5e6b0e9706b968fa7fd3de7bfc547e14abdae1206e8cc4fd25170"
    },
    {
      "relative_path": "experiment_v025/artifacts/strained_coherence_2606.07889.pdf",
      "byte_count": 164886,
      "sha256": "33a2ee601361ab3c538732133ff2a937c93f765f112451a9bf96899d9fce3271"
    },
    {
      "relative_path": "experiment_v025/artifacts/summary.json",
      "byte_count": 5039,
      "sha256": "bffafdb067a0238a8e4d23915cd5f18c90c09c34f9c55e6241fce4f594994977"
    },
    {
      "relative_path": "experiment_v025/artifacts/terminal_wrench_2604.17596.pdf",
      "byte_count": 248630,
      "sha256": "140df68e633bcb5544e37b67a6f362a917f7a38b566b25e1b42fe86beb619e8a"
    },
    {
      "relative_path": "experiment_v025/artifacts/test_viaf.py",
      "byte_count": 1937,
      "sha256": "1f334f43fb9222ef625f10732b9f17b072c5439cbfef76709ea28bf5b381a3fb"
    },
    {
      "relative_path": "experiment_v025/artifacts/trajad_2602.06443.pdf",
      "byte_count": 1148109,
      "sha256": "3237bcd13e7f2926c3f3cd3891c661ea398f57f1cb347523c87a217a73278fec"
    },
    {
      "relative_path": "experiment_v025/artifacts/trajectory_guard_2601.00516.pdf",
      "byte_count": 334806,
      "sha256": "ab6d2c66b081b32a90ff3f230854058199c049362ffb49f46bef9f869fc18d34"
    }
  ]
}
```

## Codex Interpretation

Mechanically valid negative Development. The independent audit replayed all 1185 rows, 35 fold models and 8295 scores with zero error. VIAF AUC 0.905492 and TPR@5%FPR 0.690402 failed their absolute gates. The strongest position-free anchor_bag comparator reached AUC 0.915705; VIAF delta was -0.010213 with 2000-task-bootstrap interval [-0.021228,-0.000876]. Only 2/7 gates passed. Main raw/source audit read and joined all 1185 rows with zero errors, found negative deltas for all three generator models, four of five folds and four of five sources, and found VIAF lost to anchor_bag in both anchor strata. Disposition is NO_GO_FOR_CONFIRMATION. Bucket 0 remained untouched; no Reviewer, Decision, Delivery or Ready transition is authorized. v025 is frozen and the same Run must continue with a scientifically different v026 candidate.