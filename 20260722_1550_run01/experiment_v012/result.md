# Experiment Result

```json
{
  "experiment_id": "v012",
  "execution_provenance": "caller_recorded",
  "plan_sha256": "ab73080ce39866d98a54ffdf78ed5b17e30ae2dd64e51adac8d34f9b28cea07c",
  "candidate_sha256": "137df6fffef43169ab6ea50f2dda940aabbb2c4cd3719db0ff2a99293feac29d",
  "evidence_packet_sha256": "941002813b2b0f0e1f949d95030bd4adc9ba02be1a72f29a22d5f87e52e61673",
  "execution": {
    "command": "[\"D:\\\\Desktop\\\\crl\\\\crl_agent_v3\\\\.venv\\\\python.exe acquire.py --phase development --config config.json --output-dir ..\\\\experiment_v012\\\\work\\\\dev_acquire_001 --work-root ..\\\\experiment_v012\\\\work\\\\dev_source_001\", \"D:\\\\Desktop\\\\crl\\\\crl_agent_v3\\\\.venv\\\\python.exe evaluate.py --phase development --config config.json --dataset ..\\\\experiment_v012\\\\work\\\\dev_acquire_001\\\\dataset.jsonl --manifest ..\\\\experiment_v012\\\\work\\\\dev_acquire_001\\\\manifest.json --output-dir ..\\\\experiment_v012\\\\work\\\\dev_eval_001\", \"D:\\\\Desktop\\\\crl\\\\crl_agent_v3\\\\.venv\\\\python.exe audit.py --phase development --config config.json --dataset ..\\\\experiment_v012\\\\work\\\\dev_acquire_001\\\\dataset.jsonl --manifest ..\\\\experiment_v012\\\\work\\\\dev_acquire_001\\\\manifest.json --repository-root ..\\\\experiment_v012\\\\work\\\\dev_source_001\\\\repository --raw-predictions ..\\\\experiment_v012\\\\work\\\\dev_eval_001\\\\raw_predictions.jsonl --references ..\\\\experiment_v012\\\\work\\\\dev_eval_001\\\\reference_records.jsonl --summary ..\\\\experiment_v012\\\\work\\\\dev_eval_001\\\\summary.json --frozen-model ..\\\\experiment_v012\\\\work\\\\dev_eval_001\\\\frozen_model.joblib --report ..\\\\experiment_v012\\\\work\\\\dev_audit_001\\\\report.json\"]",
    "cwd": "D:\\Desktop\\crl\\20260722_1550_run01\\implementation_v012",
    "exit_code": 0,
    "stdout": "{\"baselines\": 718, \"phase\": \"development\", \"rows\": 1729, \"serious_exploits\": 1011, \"task_model_records\": 281, \"tasks_selected\": 96}\r\n\n{\"all_gates_passed\": false, \"candidate_auc\": 0.8261890780974751, \"candidate_tpr_at_5pct_fpr\": 0.03167420814479638, \"eligible_tasks\": 94, \"evaluated_rows\": 1613, \"phase\": \"development\"}\r\n\n{\"all_gates_passed\": false, \"phase\": \"development\", \"raw_prediction_rows_checked\": 352, \"source_files_checked\": 2010, \"status\": \"AUDIT_OK\"}\r\n",
    "stderr": "",
    "environment": {
      "cuda_capability": "12.0",
      "gpu": "NVIDIA GeForce RTX 5060 Ti",
      "numpy": "2.3.5",
      "nvidia_driver": "591.86",
      "python": "3.11.15",
      "python_executable": "D:\\Desktop\\crl\\crl_agent_v3\\.venv\\python.exe",
      "repository_commit": "d8a29613235a0ef56a8b70b3142626a533da28c2",
      "scikit_learn": "1.9.0",
      "scipy": "1.16.0",
      "torch": "2.12.0+cu130",
      "torch_cuda": "13.0"
    }
  },
  "artifacts": [
    {
      "relative_path": "experiment_v012/artifacts/attempts_manifest.json",
      "byte_count": 2867,
      "sha256": "9aa4b1c155d4173c68f4b3ef56dc0a7ea86eeb9da937dd7023102f6aa18efdc0"
    },
    {
      "relative_path": "experiment_v012/artifacts/candidate_v012.md",
      "byte_count": 4564,
      "sha256": "137df6fffef43169ab6ea50f2dda940aabbb2c4cd3719db0ff2a99293feac29d"
    },
    {
      "relative_path": "experiment_v012/artifacts/dev_acquire_001_dataset.jsonl",
      "byte_count": 38050057,
      "sha256": "bd766eb62cf98e8fb1b8dd17c20d5edfc759eeb737bd3c232f73e656f9e713a3"
    },
    {
      "relative_path": "experiment_v012/artifacts/dev_acquire_001_execution.json",
      "byte_count": 2475,
      "sha256": "04a376aefd21c592098bf0aab634139b39edf11627f58b289db8a7d66eb04606"
    },
    {
      "relative_path": "experiment_v012/artifacts/dev_acquire_001_manifest.json",
      "byte_count": 449291,
      "sha256": "9bcec296b8c380d21f084e60a860577a8e08b9188f8fce75d8c625a3671ee59e"
    },
    {
      "relative_path": "experiment_v012/artifacts/dev_acquire_001_stderr.bin",
      "byte_count": 0,
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    },
    {
      "relative_path": "experiment_v012/artifacts/dev_acquire_001_stdout.bin",
      "byte_count": 133,
      "sha256": "58a6cbeedabe396a9e794c199ec03a57b86a210df1f3081e7450b6335a442c2d"
    },
    {
      "relative_path": "experiment_v012/artifacts/dev_audit_001_execution.json",
      "byte_count": 4293,
      "sha256": "4f1084dc2627582a86786ef8c0239235e5daa8070d6974417c64897f98e3b627"
    },
    {
      "relative_path": "experiment_v012/artifacts/dev_audit_001_report.json",
      "byte_count": 2674,
      "sha256": "6b1410133d7afc608d0c19581a83c8ac69e5daf3645ee5387e70da7bbe288682"
    },
    {
      "relative_path": "experiment_v012/artifacts/dev_audit_001_stderr.bin",
      "byte_count": 0,
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    },
    {
      "relative_path": "experiment_v012/artifacts/dev_audit_001_stdout.bin",
      "byte_count": 141,
      "sha256": "07b49987b1e10e08b0f5d83e5a106fd164f4aa3e19164685fd36f597770a0313"
    },
    {
      "relative_path": "experiment_v012/artifacts/dev_eval_001_environment.json",
      "byte_count": 411,
      "sha256": "6e2ead211ff57604cbdb5409d8c8173fa2990b68e859d70ea52780eb63eb3482"
    },
    {
      "relative_path": "experiment_v012/artifacts/dev_eval_001_execution.json",
      "byte_count": 4426,
      "sha256": "1ca6cc3a1d8d22a008d296c14951016e97d4964b4fce4061460a2f8a6238cb68"
    },
    {
      "relative_path": "experiment_v012/artifacts/dev_eval_001_frozen_model.joblib",
      "byte_count": 680547,
      "sha256": "075b9b1d7bb6b0f213e2e1376a1833c7cab4090ef7fe4e19099ebe1a48a73081"
    },
    {
      "relative_path": "experiment_v012/artifacts/dev_eval_001_raw_predictions.jsonl",
      "byte_count": 279643,
      "sha256": "68e6e83dbd82429855c5079f933d0c50d74fb82a09d53825d4d5bbeda1e07677"
    },
    {
      "relative_path": "experiment_v012/artifacts/dev_eval_001_reference_records.jsonl",
      "byte_count": 29030,
      "sha256": "da71beb34381f3c43f90088bf9f3bca5329ed8bddcb37e7559e10064f8e5b52b"
    },
    {
      "relative_path": "experiment_v012/artifacts/dev_eval_001_stderr.bin",
      "byte_count": 0,
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    },
    {
      "relative_path": "experiment_v012/artifacts/dev_eval_001_stdout.bin",
      "byte_count": 186,
      "sha256": "443e084eb42140bb867e1695ad143527998659857e9ffc0ad16cfe6375ade70d"
    },
    {
      "relative_path": "experiment_v012/artifacts/dev_eval_001_summary.json",
      "byte_count": 6421,
      "sha256": "c179efd0f42d33bed952bec7b62ff8a6e1835511b9a9758eac88bdd998a41133"
    },
    {
      "relative_path": "experiment_v012/artifacts/dev_eval_001_task_ids.json",
      "byte_count": 1406,
      "sha256": "fc0cc9494c0ca79ce46e1a8bf45ae91a2f8c8489c2e183f8ee4fab37b6bff91d"
    },
    {
      "relative_path": "experiment_v012/artifacts/evidence_packet_v012.md",
      "byte_count": 8104,
      "sha256": "941002813b2b0f0e1f949d95030bd4adc9ba02be1a72f29a22d5f87e52e61673"
    },
    {
      "relative_path": "experiment_v012/artifacts/frozen_acquire.py",
      "byte_count": 12438,
      "sha256": "cf87ec4994081b4516695806b471daf75e923fe511d0b67d05b4ab126d34e836"
    },
    {
      "relative_path": "experiment_v012/artifacts/frozen_audit.py",
      "byte_count": 15408,
      "sha256": "366d55e4f9c3ca9ada37bfe1243650e960b76285a96438d97c8d98555125038b"
    },
    {
      "relative_path": "experiment_v012/artifacts/frozen_config.json",
      "byte_count": 1222,
      "sha256": "82c4b269414c4f53e0bc54a05cc1896b087ea8e5d711b074aae4bc2ff8097ce3"
    },
    {
      "relative_path": "experiment_v012/artifacts/frozen_evaluate.py",
      "byte_count": 39154,
      "sha256": "a29b8aace75bf5505620fab71c982e296e045cb1590a20a5a9c19a63c233d78d"
    },
    {
      "relative_path": "experiment_v012/artifacts/nearest_prior_v012.md",
      "byte_count": 3020,
      "sha256": "eb4db3ba3406ee1d9edc73e687196463b690d3d2839bf36f878ef844564f467e"
    },
    {
      "relative_path": "experiment_v012/artifacts/problem_v012.md",
      "byte_count": 2901,
      "sha256": "0c733fd584a637cc281f3fd3414ab7ed1e0b500ac6ded3250c79e90000cc4a6e"
    },
    {
      "relative_path": "experiment_v012/artifacts/promotion_audit_v012.md",
      "byte_count": 4566,
      "sha256": "e2dcee4d4e8ce6a340faf96f1f77da1eecca5d0da481f0df029a0a5ee81103ae"
    },
    {
      "relative_path": "experiment_v012/artifacts/research_map_v012.md",
      "byte_count": 4402,
      "sha256": "ea7197e5d560574b30656653bd1d71d53617580d8935889bfed8f8f52e43a02f"
    },
    {
      "relative_path": "experiment_v012/artifacts/selection_context_v012.md",
      "byte_count": 5340,
      "sha256": "8882fc1846b6bbb58a70ce03418ab0cb80e8ec596af027a3fbcc4b15501dcfd5"
    },
    {
      "relative_path": "experiment_v012/artifacts/source_cheap_reward_hacking_2606.08893.pdf",
      "byte_count": 1278533,
      "sha256": "c5fd945125b1b6cd4739b2aacf150156bbfc8e47aff2d7240ea05ed697075ce0"
    },
    {
      "relative_path": "experiment_v012/artifacts/source_praetor_2604.26274.pdf",
      "byte_count": 605389,
      "sha256": "842d593f53486481d384c8407d2fd688bbfbf90b69e505db54bc31008a15aa98"
    },
    {
      "relative_path": "experiment_v012/artifacts/source_terminal_wrench_2604.17596.pdf",
      "byte_count": 248630,
      "sha256": "140df68e633bcb5544e37b67a6f362a917f7a38b566b25e1b42fe86beb619e8a"
    },
    {
      "relative_path": "experiment_v012/artifacts/source_trace_2601.20103.pdf",
      "byte_count": 2244476,
      "sha256": "98a3121de46018f08f47a8db18b4ed55c9d117beb5e984eaa9f3c2a47f3a5649"
    }
  ]
}
```

## Codex Interpretation

All three frozen Development attempts exited 0 and the independent audit verified 2,010 source files, 1,729 dataset rows, 352 held-out predictions, reference exclusion, task partitions, model/config hashes, metrics, and gates. RCED failed promotion: AUC 0.8261890781 versus the strongest text comparator 0.9002797831 (delta -0.0740907050; task-bootstrap 95% [-0.1967883989, 0.0253623037]), TPR@5%FPR 0.0316742081, and frozen-threshold FPR 0.1450381679. Only the absolute AUC and frozen-threshold TPR gates passed. Main Codex inspected raw cases and found legitimate alternate workflows were assigned extreme structured risk while several hacks followed ordinary coarse effect sequences. Confirmation remains unacquired and unread. No Review Packet, Reviewer, Decision, or Delivery is authorized. v012 is frozen as a negative result and the same Run must advance to v013.