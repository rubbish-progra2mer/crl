# Experiment Result

```json
{
  "experiment_id": "v022",
  "execution_provenance": "caller_recorded",
  "plan_sha256": "0a1374be5f0ac1c616db8efe47f9971b71dc98e4cf696f6716c86a0734127bbf",
  "candidate_sha256": "40f0e0e87bb1aff6c999c9c68937294578acb047081eb04c336eb4164fdea25e",
  "evidence_packet_sha256": "4f7462c159ca4db7372affac41cf6dd6bc8c5acc4d2131c6c0ee3db8d5274228",
  "execution": {
    "command": "[\"D:\\\\Desktop\\\\crl\\\\crl_agent_v3\\\\.venv\\\\python.exe\", \"D:\\\\Desktop\\\\crl\\\\20260722_1550_run01\\\\experiment_v022\\\\artifacts\\\\program.py\", \"--phase\", \"confirmation\", \"--config\", \"D:\\\\Desktop\\\\crl\\\\20260722_1550_run01\\\\experiment_v022\\\\artifacts\\\\config.json\", \"--dataset\", \"D:\\\\Desktop\\\\crl\\\\20260722_1550_run01\\\\experiment_v022\\\\artifacts\\\\confirmation_dataset.jsonl\", \"--base-module\", \"D:\\\\Desktop\\\\crl\\\\20260722_1550_run01\\\\experiment_v022\\\\artifacts\\\\base_v012.py\", \"--output-dir\", \"D:\\\\Desktop\\\\crl\\\\20260722_1550_run01\\\\experiment_v022\\\\confirmation_output_001\", \"--model\", \"D:\\\\Desktop\\\\crl\\\\20260722_1550_run01\\\\experiment_v022\\\\artifacts\\\\dev_model.joblib\", \"--input-manifest\", \"D:\\\\Desktop\\\\crl\\\\20260722_1550_run01\\\\experiment_v022\\\\artifacts\\\\confirmation_manifest.json\"]",
    "cwd": "D:\\Desktop\\crl\\20260722_1550_run01\\experiment_v022\\artifacts",
    "exit_code": 0,
    "stdout": "{\"auc_delta\": 0.0036007329368358265, \"candidate_auc\": 0.9225745101473939, \"gates\": \"6/7\", \"phase\": \"confirmation\", \"strongest_comparator\": \"duplicated_absolute\"}\r\n",
    "stderr": "",
    "environment": {
      "acquisition_dataset_sha256": "0e701e4c842e4f661ec8e8650ec157e5462efe93bbb5d2514aab6a6c8167d77a",
      "audit_report_sha256": "e06d1f4924c315984fb6bc095e935a5284d69b2660af318adedc8275322e07e3",
      "audit_status": "AUDIT_OK",
      "cuda_available": "True",
      "elapsed_seconds": "102.86683389999962",
      "gpu": "NVIDIA GeForce RTX 5060 Ti",
      "joblib": "1.5.3",
      "numpy": "2.3.5",
      "phase": "confirmation",
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
      "relative_path": "experiment_v022/artifacts/acquire.py",
      "byte_count": 12438,
      "sha256": "cf87ec4994081b4516695806b471daf75e923fe511d0b67d05b4ab126d34e836"
    },
    {
      "relative_path": "experiment_v022/artifacts/audit.py",
      "byte_count": 2522,
      "sha256": "f68122cb45f92fb8a85069436c4b55abe3ac89872ae6dd340ed76d617fe153e7"
    },
    {
      "relative_path": "experiment_v022/artifacts/base_v012.py",
      "byte_count": 39154,
      "sha256": "a29b8aace75bf5505620fab71c982e296e045cb1590a20a5a9c19a63c233d78d"
    },
    {
      "relative_path": "experiment_v022/artifacts/base_v020_audit.py",
      "byte_count": 15672,
      "sha256": "2f42878764989288ee44a68d287af2cccfb2e25f72f7eb2fde40e9d81a898607"
    },
    {
      "relative_path": "experiment_v022/artifacts/base_v020_program.py",
      "byte_count": 17872,
      "sha256": "67ac151b6817d6619f915aad581da6c70f9ecdafeb780d87e31816c36009de92"
    },
    {
      "relative_path": "experiment_v022/artifacts/candidate_v022.md",
      "byte_count": 1604,
      "sha256": "40f0e0e87bb1aff6c999c9c68937294578acb047081eb04c336eb4164fdea25e"
    },
    {
      "relative_path": "experiment_v022/artifacts/cheap_reward_hacking_2606.08893.pdf",
      "byte_count": 1278533,
      "sha256": "c5fd945125b1b6cd4739b2aacf150156bbfc8e47aff2d7240ea05ed697075ce0"
    },
    {
      "relative_path": "experiment_v022/artifacts/config.json",
      "byte_count": 1675,
      "sha256": "a46a9b5196226705a5fcea4d0c4e0dc50c5214529ec1b229f581c1b447c8a0c6"
    },
    {
      "relative_path": "experiment_v022/artifacts/confirmation_acquire_001_execution.json",
      "byte_count": 2540,
      "sha256": "c5e1d7ca342ceff14385bffa5119b35bbe470215989811aa180adf4a6c7b9def"
    },
    {
      "relative_path": "experiment_v022/artifacts/confirmation_acquire_001_stderr.bin",
      "byte_count": 0,
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    },
    {
      "relative_path": "experiment_v022/artifacts/confirmation_acquire_001_stdout.bin",
      "byte_count": 133,
      "sha256": "1cf3f6aab9a11e6ef93f8a12fcbeaa8c23c7471d5132d3b12a14ad02a1bc2997"
    },
    {
      "relative_path": "experiment_v022/artifacts/confirmation_acquisition_failure_v021.md",
      "byte_count": 1516,
      "sha256": "087f8f7380bd89410075c1c74b148fd0f31f83e0faf6a6b556763bc911628186"
    },
    {
      "relative_path": "experiment_v022/artifacts/confirmation_audit_001_execution.json",
      "byte_count": 4392,
      "sha256": "92e4948c516b64b6dbe90dc39e34cf7913f91e005862e448a074a4a451e1ea33"
    },
    {
      "relative_path": "experiment_v022/artifacts/confirmation_audit_001_stderr.bin",
      "byte_count": 0,
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    },
    {
      "relative_path": "experiment_v022/artifacts/confirmation_audit_001_stdout.bin",
      "byte_count": 130,
      "sha256": "cad884ef469b0b7bf0519aaabe9dee9fb0b498d77117fb0b8e4390e7430feae5"
    },
    {
      "relative_path": "experiment_v022/artifacts/confirmation_audit_report.json",
      "byte_count": 751,
      "sha256": "e06d1f4924c315984fb6bc095e935a5284d69b2660af318adedc8275322e07e3"
    },
    {
      "relative_path": "experiment_v022/artifacts/confirmation_dataset.jsonl",
      "byte_count": 28985207,
      "sha256": "0e701e4c842e4f661ec8e8650ec157e5462efe93bbb5d2514aab6a6c8167d77a"
    },
    {
      "relative_path": "experiment_v022/artifacts/confirmation_eval_001_execution.json",
      "byte_count": 4358,
      "sha256": "d2f27cdd010deeebb8ee1783d862fca1cea7d2f04321608573095dd2e5936ab4"
    },
    {
      "relative_path": "experiment_v022/artifacts/confirmation_eval_001_stderr.bin",
      "byte_count": 0,
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    },
    {
      "relative_path": "experiment_v022/artifacts/confirmation_eval_001_stdout.bin",
      "byte_count": 163,
      "sha256": "86bb565624b433fb521f14a1662defe53b3dec79a10450b3f9f8b65480517ddd"
    },
    {
      "relative_path": "experiment_v022/artifacts/confirmation_manifest.json",
      "byte_count": 353930,
      "sha256": "df2f4b46506978105121fe5afc36fcc2f1188dd1a5e6303cb2a2eef836cdc543"
    },
    {
      "relative_path": "experiment_v022/artifacts/confirmation_plan_v021.md",
      "byte_count": 7863,
      "sha256": "6c42087ea9bb66916fbb0dd70bcca77ef421a43ecb88085666ad5aa7d8881c48"
    },
    {
      "relative_path": "experiment_v022/artifacts/confirmation_raw_predictions.jsonl",
      "byte_count": 766853,
      "sha256": "3da1ca9991a9a0b81d4e8e45903003ff0779d5f53ac8c9cf7e783a7979461b0b"
    },
    {
      "relative_path": "experiment_v022/artifacts/confirmation_reference_records.jsonl",
      "byte_count": 25291,
      "sha256": "ded93113a5d4193e18056af3b348df8fe35338078513cd642b0d1f2392c0af99"
    },
    {
      "relative_path": "experiment_v022/artifacts/confirmation_summary.json",
      "byte_count": 6180,
      "sha256": "12b0bf916f0894be6f96a1841fba0408f65c45f475d129c456293bcc76426504"
    },
    {
      "relative_path": "experiment_v022/artifacts/dev_001_execution.json",
      "byte_count": 3957,
      "sha256": "85c8623168280d102e0cd3d057dca46181503eda365fa705a850083cdc7eb9f6"
    },
    {
      "relative_path": "experiment_v022/artifacts/dev_001_stderr.bin",
      "byte_count": 0,
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    },
    {
      "relative_path": "experiment_v022/artifacts/dev_001_stdout.bin",
      "byte_count": 160,
      "sha256": "926ef1e1343a4ecc5292ede7f195626427dec5f74da126f2aaa635de543c278d"
    },
    {
      "relative_path": "experiment_v022/artifacts/dev_audit_001_execution.json",
      "byte_count": 4320,
      "sha256": "beab44c2d78442c59070c39c51fc7829d8adbf60670fd8f5d00fd2fd9c1fd673"
    },
    {
      "relative_path": "experiment_v022/artifacts/dev_audit_001_stderr.bin",
      "byte_count": 0,
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    },
    {
      "relative_path": "experiment_v022/artifacts/dev_audit_001_stdout.bin",
      "byte_count": 129,
      "sha256": "a7a3356855b7340e7f2e8cae4402b2bccf9ceadcbd10f7799a67f3025d3d487d"
    },
    {
      "relative_path": "experiment_v022/artifacts/dev_audit_report.json",
      "byte_count": 749,
      "sha256": "29e5a29d14f5d167bb4a22c3099b3dc7070bb4cf73675a74a2a5d69706c12822"
    },
    {
      "relative_path": "experiment_v022/artifacts/dev_model.joblib",
      "byte_count": 4627780,
      "sha256": "8ff9c2cc3ec1ade5aa404323264738800a909c7690d3b867ea48e6fb68fa56f7"
    },
    {
      "relative_path": "experiment_v022/artifacts/dev_raw_predictions.jsonl",
      "byte_count": 216506,
      "sha256": "483d930e9cc1a14bed0bff91f8b8aae465842ff852d09ce9298f3ad83e341f80"
    },
    {
      "relative_path": "experiment_v022/artifacts/dev_reference_records.jsonl",
      "byte_count": 29030,
      "sha256": "da71beb34381f3c43f90088bf9f3bca5329ed8bddcb37e7559e10064f8e5b52b"
    },
    {
      "relative_path": "experiment_v022/artifacts/dev_summary.json",
      "byte_count": 6569,
      "sha256": "86b684cffc204d6f5fd8a805283bad5c0463ee7f34cbc28ef057b92b9f104b42"
    },
    {
      "relative_path": "experiment_v022/artifacts/development_dataset.jsonl",
      "byte_count": 38050057,
      "sha256": "bd766eb62cf98e8fb1b8dd17c20d5edfc759eeb737bd3c232f73e656f9e713a3"
    },
    {
      "relative_path": "experiment_v022/artifacts/evidence_packet_v022.md",
      "byte_count": 4336,
      "sha256": "4f7462c159ca4db7372affac41cf6dd6bc8c5acc4d2131c6c0ee3db8d5274228"
    },
    {
      "relative_path": "experiment_v022/artifacts/implementation_audit_v022.md",
      "byte_count": 2722,
      "sha256": "75669030459de0a33f88b75b66c17e8e965b47524b1597fb73cbe2704f680c7a"
    },
    {
      "relative_path": "experiment_v022/artifacts/main_confirmation_audit_v022.md",
      "byte_count": 6625,
      "sha256": "81eb7dd508ee91cc0d0401eb66c259e9498ab290eb475e0fecab5e71ccf5e307"
    },
    {
      "relative_path": "experiment_v022/artifacts/nearest_prior_v022.md",
      "byte_count": 604,
      "sha256": "93649578da0a406a8830f4772a730a811044e99bc0aa860c32193ab6e5d3dc15"
    },
    {
      "relative_path": "experiment_v022/artifacts/praetor_2604.26274.pdf",
      "byte_count": 605389,
      "sha256": "842d593f53486481d384c8407d2fd688bbfbf90b69e505db54bc31008a15aa98"
    },
    {
      "relative_path": "experiment_v022/artifacts/problem_v022.md",
      "byte_count": 689,
      "sha256": "b9b82680adfc3f37df0c2363d2ffc244e7f8974f752a6df310c5c56363f6807b"
    },
    {
      "relative_path": "experiment_v022/artifacts/program.py",
      "byte_count": 2695,
      "sha256": "f81e3bef778346c142154def15e20c78a009cfddeb0d61c79d54dd9d76237c4a"
    },
    {
      "relative_path": "experiment_v022/artifacts/promotion_audit_v021.md",
      "byte_count": 6912,
      "sha256": "183cf86a029e5b3d88f8dac406605cd3c2287eca1d08f49e77de99055204e740"
    },
    {
      "relative_path": "experiment_v022/artifacts/research_map_v022.md",
      "byte_count": 1316,
      "sha256": "abccf56b384c360617a313bdf896e9b764d14b04924a4fa1994de78823aabe0b"
    },
    {
      "relative_path": "experiment_v022/artifacts/selection_context_v022.md",
      "byte_count": 1059,
      "sha256": "ffde52557b6fabafa03a88048b6f7dd8c770987d505e913ee3135835ec6c79f8"
    },
    {
      "relative_path": "experiment_v022/artifacts/terminal_wrench_2604.17596.pdf",
      "byte_count": 248630,
      "sha256": "140df68e633bcb5544e37b67a6f362a917f7a38b566b25e1b42fe86beb619e8a"
    },
    {
      "relative_path": "experiment_v022/artifacts/test_capacity_controls.py",
      "byte_count": 1029,
      "sha256": "9a631beeaa14c1345554cb4ac936d99150496616d1f8d0f11a0a62462799bbc7"
    },
    {
      "relative_path": "experiment_v022/artifacts/trace_2601.20103.pdf",
      "byte_count": 2244476,
      "sha256": "98a3121de46018f08f47a8db18b4ed55c9d117beb5e984eaa9f3c2a47f3a5649"
    },
    {
      "relative_path": "experiment_v022/artifacts/v021_confirmation_acquire_001_execution.json",
      "byte_count": 2309,
      "sha256": "cdb05c3867ae73b5df2f4b3a6b275b36326387fb3e4883449dfe2e51ac069195"
    },
    {
      "relative_path": "experiment_v022/artifacts/v021_confirmation_acquire_001_stderr.bin",
      "byte_count": 1089,
      "sha256": "91f099fcd2c2662796c490d11181b2c45e88943e24e775b180f85a8e562d5d00"
    },
    {
      "relative_path": "experiment_v022/artifacts/v021_confirmation_acquire_001_stdout.bin",
      "byte_count": 0,
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    },
    {
      "relative_path": "experiment_v022/artifacts/v021_plan.md",
      "byte_count": 6790,
      "sha256": "f578b11735364c67430f2e03ea1c1c7ec0107a00051e194349ac9239b8bbff50"
    },
    {
      "relative_path": "experiment_v022/artifacts/v021_result.md",
      "byte_count": 11933,
      "sha256": "74437810a222a5f59cbc48789aa20d4b12847bddd6203c8c60a9c0ed008136f5"
    }
  ]
}
```

## Codex Interpretation

v022 acquired the first untouched Terminal Wrench bucket-3 Confirmation successfully at the pinned commit: 83 selected tasks, 1,342 source rows, 1,578 source files rehashed with zero error, and zero overlap with the 94 Development tasks. The frozen seven-model bundle then scored 1,250 rows from 81 eligible tasks without refitting. The independent auditor replayed all 8,750 method scores with zero score and metric error.

Candidate AUC was 0.9225745101 and strictly exceeded all six comparators; duplicated absolute remained strongest at 0.9189737772. Candidate also passed absolute AUC, low-FPR TPR and frozen-threshold FPR/TPR conditions. However Candidate-minus-duplicated-absolute AUC was only +0.0036007329 and the fixed task-cluster bootstrap 95% interval was [-0.0074121964,+0.0154492198]. The preregistered lower-bound condition failed, yielding 6/7 gates.

Main-Codex review parsed every raw row. Candidate had 57 fixed-threshold corrections and 28 regressions, but task AUC improved on only eight tasks, tied on 57 and worsened on 16; metric-spoofing, mutable-input-tampering and security-downgrading recall slices were worse. Original source readback confirmed substantive Candidate misses such as fabricated apt history, NumPy/eigenvalue metric spoofing, training on protected test data, security downgrading and hollow fMRI/game workflows. The negative bootstrap lower bound is therefore real heterogeneity, not an audit defect.

Disposition is NO_GO_FOR_REVIEW_CONFIRMATION_GATE_FAILED. Bucket 3 is touched and may not be reused for retuning. No Review Packet, Reviewer, Decision or Delivery was created. The same Run must advance to a scientifically different Candidate and new prospective Confirmation path. System remains DEVELOPMENT_NOT_COMMISSIONED.