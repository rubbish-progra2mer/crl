# Experiment Result

```json
{
  "experiment_id": "v020",
  "execution_provenance": "caller_recorded",
  "plan_sha256": "f859f1bcbb659bfa54aff44d66c77170b499f850e2154993f7b6cd8d7ddb25b7",
  "candidate_sha256": "7c1326b3309cd0e21f52c749b38724c965821e81cf6880f20dde07678462f690",
  "evidence_packet_sha256": "514f61891e70af5be51a23df0e891dd3cabb0c2de18bc3112c79bd7bdf6f1154",
  "execution": {
    "command": "[\"D:\\\\Desktop\\\\crl\\\\crl_agent_v3\\\\.venv\\\\python.exe\", \"D:\\\\Desktop\\\\crl\\\\20260722_1550_run01\\\\experiment_v020\\\\artifacts\\\\program.py\", \"--phase\", \"development\", \"--config\", \"D:\\\\Desktop\\\\crl\\\\20260722_1550_run01\\\\experiment_v020\\\\artifacts\\\\config.json\", \"--dataset\", \"D:\\\\Desktop\\\\crl\\\\20260722_1550_run01\\\\experiment_v020\\\\artifacts\\\\development_dataset.jsonl\", \"--base-module\", \"D:\\\\Desktop\\\\crl\\\\20260722_1550_run01\\\\experiment_v020\\\\artifacts\\\\base_v012.py\", \"--output-dir\", \"D:\\\\Desktop\\\\crl\\\\20260722_1550_run01\\\\experiment_v020\\\\dev_output_001\"]",
    "cwd": "D:\\Desktop\\crl\\20260722_1550_run01\\experiment_v020\\artifacts",
    "exit_code": 0,
    "stdout": "{\"auc_delta\": 0.01854858208697452, \"candidate_auc\": 0.9408656004973921, \"gates\": \"7/7\", \"phase\": \"development\", \"strongest_comparator\": \"absolute_delta\"}\n",
    "stderr": "",
    "environment": {
      "cuda_available": "True",
      "elapsed_seconds": "129.9423999999999",
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
      "relative_path": "experiment_v020/artifacts/acquire.py",
      "byte_count": 12438,
      "sha256": "cf87ec4994081b4516695806b471daf75e923fe511d0b67d05b4ab126d34e836"
    },
    {
      "relative_path": "experiment_v020/artifacts/audit.py",
      "byte_count": 15672,
      "sha256": "2f42878764989288ee44a68d287af2cccfb2e25f72f7eb2fde40e9d81a898607"
    },
    {
      "relative_path": "experiment_v020/artifacts/base_v012.py",
      "byte_count": 39154,
      "sha256": "a29b8aace75bf5505620fab71c982e296e045cb1590a20a5a9c19a63c233d78d"
    },
    {
      "relative_path": "experiment_v020/artifacts/candidate_v020.md",
      "byte_count": 4556,
      "sha256": "7c1326b3309cd0e21f52c749b38724c965821e81cf6880f20dde07678462f690"
    },
    {
      "relative_path": "experiment_v020/artifacts/cheap_reward_hacking_2606.08893.pdf",
      "byte_count": 1278533,
      "sha256": "c5fd945125b1b6cd4739b2aacf150156bbfc8e47aff2d7240ea05ed697075ce0"
    },
    {
      "relative_path": "experiment_v020/artifacts/config.json",
      "byte_count": 1481,
      "sha256": "fb437f9b70d57e7ca0c4d13baa13a41b0f28be0441870574f7b909c2208cd43b"
    },
    {
      "relative_path": "experiment_v020/artifacts/dev_001_execution.json",
      "byte_count": 3731,
      "sha256": "8d25d4f07ca60944fc5c17d9d4c13f3250aca886b22b49a2ca3c3da385e62088"
    },
    {
      "relative_path": "experiment_v020/artifacts/dev_001_stderr.bin",
      "byte_count": 0,
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    },
    {
      "relative_path": "experiment_v020/artifacts/dev_001_stdout.bin",
      "byte_count": 155,
      "sha256": "25a382d88740c09c9a435ebea73a0d3bc4b86cc0bc9c591ad6ccd4b36853f864"
    },
    {
      "relative_path": "experiment_v020/artifacts/dev_audit_001_execution.json",
      "byte_count": 4095,
      "sha256": "a5c55dcea6145261e8563f2a3db81c96f39dff23663d3b218272267cb80e4e27"
    },
    {
      "relative_path": "experiment_v020/artifacts/dev_audit_001_stderr.bin",
      "byte_count": 0,
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    },
    {
      "relative_path": "experiment_v020/artifacts/dev_audit_001_stdout.bin",
      "byte_count": 129,
      "sha256": "0c9f2d670c36d5cbde704d40f9e3f18b2bef3a68e6ae43606507cdda780db7c3"
    },
    {
      "relative_path": "experiment_v020/artifacts/dev_audit_report.json",
      "byte_count": 749,
      "sha256": "cd4bcc1d2ca46d582bf544f3805bfd0e28d95e7a4fafc595b0701bd256c0dc51"
    },
    {
      "relative_path": "experiment_v020/artifacts/dev_model.joblib",
      "byte_count": 3186868,
      "sha256": "4fa248b56d9f013711ccfcf3f21eb6f967c0ec9961ef5a148e40f0a246f07293"
    },
    {
      "relative_path": "experiment_v020/artifacts/dev_raw_predictions.jsonl",
      "byte_count": 188919,
      "sha256": "b7437213e300ad2a2eb9a07e9b6a8c6213e16c123bf8bfe450d0d67c70cfb081"
    },
    {
      "relative_path": "experiment_v020/artifacts/dev_reference_records.jsonl",
      "byte_count": 29030,
      "sha256": "da71beb34381f3c43f90088bf9f3bca5329ed8bddcb37e7559e10064f8e5b52b"
    },
    {
      "relative_path": "experiment_v020/artifacts/dev_summary.json",
      "byte_count": 5774,
      "sha256": "54802b4d015693ce333f86953b07b0edc5b9105fd17df3a91eb10581050e3191"
    },
    {
      "relative_path": "experiment_v020/artifacts/development_dataset.jsonl",
      "byte_count": 38050057,
      "sha256": "bd766eb62cf98e8fb1b8dd17c20d5edfc759eeb737bd3c232f73e656f9e713a3"
    },
    {
      "relative_path": "experiment_v020/artifacts/evidence_packet_v020.md",
      "byte_count": 4336,
      "sha256": "514f61891e70af5be51a23df0e891dd3cabb0c2de18bc3112c79bd7bdf6f1154"
    },
    {
      "relative_path": "experiment_v020/artifacts/implementation_audit_v020.md",
      "byte_count": 5103,
      "sha256": "8d3ece5ca85420b38dc6f96eddc7b2b9d2360e2197d7ea17868de184d9899b4d"
    },
    {
      "relative_path": "experiment_v020/artifacts/nearest_prior_v020.md",
      "byte_count": 3363,
      "sha256": "6e64cc3ec4878cd17961b1fcfc5e7880f2309052ba15f71f9aa63703cbdf66d8"
    },
    {
      "relative_path": "experiment_v020/artifacts/praetor_2604.26274.pdf",
      "byte_count": 605389,
      "sha256": "842d593f53486481d384c8407d2fd688bbfbf90b69e505db54bc31008a15aa98"
    },
    {
      "relative_path": "experiment_v020/artifacts/problem_v020.md",
      "byte_count": 2035,
      "sha256": "7a9ddf60740bdb3635b49b4540535ab237d448267799e5dcb820f8aa25e97d17"
    },
    {
      "relative_path": "experiment_v020/artifacts/program.py",
      "byte_count": 17872,
      "sha256": "67ac151b6817d6619f915aad581da6c70f9ecdafeb780d87e31816c36009de92"
    },
    {
      "relative_path": "experiment_v020/artifacts/promotion_audit_v012.md",
      "byte_count": 4566,
      "sha256": "e2dcee4d4e8ce6a340faf96f1f77da1eecca5d0da481f0df029a0a5ee81103ae"
    },
    {
      "relative_path": "experiment_v020/artifacts/promotion_audit_v020.md",
      "byte_count": 4538,
      "sha256": "8b67077e39644645719a3c7a6791d405e6be4f733c11dcdb2400e002e5eae6a8"
    },
    {
      "relative_path": "experiment_v020/artifacts/research_map_v020.md",
      "byte_count": 3678,
      "sha256": "0b4e5130708a5edc040de331b19d58e66859d38b0c4b714035fae99d75b2ef40"
    },
    {
      "relative_path": "experiment_v020/artifacts/selection_context_v020.md",
      "byte_count": 3763,
      "sha256": "b298b6dfbc1bc6c7b0349d7e5809cabe12abbe24567f6c854c7ddf6e67169fe1"
    },
    {
      "relative_path": "experiment_v020/artifacts/terminal_wrench_2604.17596.pdf",
      "byte_count": 248630,
      "sha256": "140df68e633bcb5544e37b67a6f362a917f7a38b566b25e1b42fe86beb619e8a"
    },
    {
      "relative_path": "experiment_v020/artifacts/test_residual.py",
      "byte_count": 935,
      "sha256": "4fc711296923e32fa0e0ac72b538cd01cea5ce8a8b0c22e6574447ce15395500"
    },
    {
      "relative_path": "experiment_v020/artifacts/trace_2601.20103.pdf",
      "byte_count": 2244476,
      "sha256": "98a3121de46018f08f47a8db18b4ed55c9d117beb5e984eaa9f3c2a47f3a5649"
    }
  ]
}
```

## Codex Interpretation

v020 completed one real Development fit and one independent audit. The Candidate achieved AUC 0.9408656005 and TPR@5%FPR 0.7782805430. Its strongest listed comparator was absolute delta at AUC 0.9223170184; task-cluster delta was +0.0185485821 with 95% interval [+0.0081268843,+0.0259549208]. All seven frozen numeric/integrity gates passed, and the independent audit replayed 1,760 scores with zero error.

Main-Codex Promotion nevertheless is NO_GO_FOR_CONFIRMATION because the 90,000-dimensional signed representation lacks a 90,000-dimensional unsigned-duplication and text-duplication control. Under L2 logistic regression, the current result cannot isolate signed direction from changed effective regularization/capacity. v021 may add only those controls and necessary schema/version bindings; Candidate, data, split, learner, thresholds, bootstrap, and gates remain fixed. Bucket-3 Confirmation was not acquired and no Reviewer was started.
