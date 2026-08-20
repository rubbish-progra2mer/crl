# Experiment Result

```json
{
  "experiment_id": "v026",
  "execution_provenance": "caller_recorded",
  "plan_sha256": "edcb1efbf5257fc52cda3983b810ac21134a618c0e692baf6a0eb41905ff0405",
  "candidate_sha256": "b43922594122236b08fcdd94836a5731a8d1cc91c49e7a0a918b51a225bc5f61",
  "evidence_packet_sha256": "0ad0e89d9dc7a690d4c4b586d10e37504df23c4a2e9d1a4541a1794dd9c1b3f8",
  "execution": {
    "command": "D:\\Desktop\\crl\\crl_agent_v3\\.venv\\python.exe D:\\Desktop\\crl\\20260722_1550_run01\\experiment_v026\\artifacts\\program.py --phase development --config D:\\Desktop\\crl\\20260722_1550_run01\\experiment_v026\\artifacts\\config.json --candidate D:\\Desktop\\crl\\20260722_1550_run01\\experiment_v026\\artifacts\\candidate_v026.md --evidence-packet D:\\Desktop\\crl\\20260722_1550_run01\\experiment_v026\\artifacts\\evidence_packet_v026.md --dataset D:\\Desktop\\crl\\20260722_1550_run01\\experiment_v026\\artifacts\\development_bucket1_dataset.jsonl --dataset D:\\Desktop\\crl\\20260722_1550_run01\\experiment_v026\\artifacts\\development_bucket2_dataset.jsonl --dataset D:\\Desktop\\crl\\20260722_1550_run01\\experiment_v026\\artifacts\\development_bucket3_dataset.jsonl --input-manifest D:\\Desktop\\crl\\20260722_1550_run01\\experiment_v026\\artifacts\\development_bucket1_manifest.json --input-manifest D:\\Desktop\\crl\\20260722_1550_run01\\experiment_v026\\artifacts\\development_bucket2_manifest.json --input-manifest D:\\Desktop\\crl\\20260722_1550_run01\\experiment_v026\\artifacts\\development_bucket3_manifest.json --base-module D:\\Desktop\\crl\\20260722_1550_run01\\experiment_v026\\artifacts\\base_v012.py --output-dir D:\\Desktop\\crl\\20260722_1550_run01\\experiment_v026\\dev_output_001",
    "cwd": "D:\\Desktop\\crl\\20260722_1550_run01\\experiment_v026\\artifacts",
    "exit_code": 0,
    "stdout": "{\"auc_delta\": 0.010055888590988049, \"candidate_auc\": 0.8832616787559023, \"gates\": \"7/8\", \"phase\": \"development\", \"strongest_comparator\": \"single_support\"}\r\n",
    "stderr": "",
    "environment": {
      "cuda_available": "True",
      "elapsed_seconds": "1939.5274668999919",
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
      "relative_path": "experiment_v026/artifacts/acquire.py",
      "byte_count": 12438,
      "sha256": "cf87ec4994081b4516695806b471daf75e923fe511d0b67d05b4ab126d34e836"
    },
    {
      "relative_path": "experiment_v026/artifacts/attempts_manifest_v026.json",
      "byte_count": 2083,
      "sha256": "571f7efa1214fbd4cd6a05141e78549d4bf86ec7780aa8ac9ace8dc90de29405"
    },
    {
      "relative_path": "experiment_v026/artifacts/audit.py",
      "byte_count": 31318,
      "sha256": "1676eecf7886b8a76047da8c50458b9855749bbede297fddebee90a9c9e83f3f"
    },
    {
      "relative_path": "experiment_v026/artifacts/audit_report.json",
      "byte_count": 1374,
      "sha256": "fbe462db212f82f07ad5d346ed7aa989a409b0bd85031a39be3381c2c21c4b3f"
    },
    {
      "relative_path": "experiment_v026/artifacts/base_v012.py",
      "byte_count": 39154,
      "sha256": "a29b8aace75bf5505620fab71c982e296e045cb1590a20a5a9c19a63c233d78d"
    },
    {
      "relative_path": "experiment_v026/artifacts/candidate_v026.md",
      "byte_count": 2574,
      "sha256": "b43922594122236b08fcdd94836a5731a8d1cc91c49e7a0a918b51a225bc5f61"
    },
    {
      "relative_path": "experiment_v026/artifacts/cheap_reward_hacking_2606.08893.pdf",
      "byte_count": 1278533,
      "sha256": "c5fd945125b1b6cd4739b2aacf150156bbfc8e47aff2d7240ea05ed697075ce0"
    },
    {
      "relative_path": "experiment_v026/artifacts/config.json",
      "byte_count": 2189,
      "sha256": "9b784ed930a5514fe57a40c484519ca6d32c09ef45e9f0a091c35af2d84dd0c9"
    },
    {
      "relative_path": "experiment_v026/artifacts/confirmation_audit_v022.md",
      "byte_count": 6625,
      "sha256": "81eb7dd508ee91cc0d0401eb66c259e9498ab290eb475e0fecab5e71ccf5e307"
    },
    {
      "relative_path": "experiment_v026/artifacts/d24fad_2603.01713.pdf",
      "byte_count": 3562892,
      "sha256": "c8f9aa621915f8e1ecb3945155eb5bf06580f74214f3d9d88be520154a5231f7"
    },
    {
      "relative_path": "experiment_v026/artifacts/dev_001_execution.json",
      "byte_count": 6323,
      "sha256": "54f185fb0aea4321a322bca8c1c6f4466bbab7a81aa8f363cdd78302936b82a0"
    },
    {
      "relative_path": "experiment_v026/artifacts/dev_001_stderr.bin",
      "byte_count": 0,
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    },
    {
      "relative_path": "experiment_v026/artifacts/dev_001_stdout.bin",
      "byte_count": 156,
      "sha256": "8346fb96e44cca93c2b84d9da9e8c53223d21fef1031e672b85a4b6202820385"
    },
    {
      "relative_path": "experiment_v026/artifacts/dev_audit_001_execution.json",
      "byte_count": 6643,
      "sha256": "3d6a7a0a4b8b9d9b812ec0c1d587ff31b05e0d1be1798574f201b48e0f4e6dd6"
    },
    {
      "relative_path": "experiment_v026/artifacts/dev_audit_001_stderr.bin",
      "byte_count": 0,
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    },
    {
      "relative_path": "experiment_v026/artifacts/dev_audit_001_stdout.bin",
      "byte_count": 154,
      "sha256": "67e818574c32f6df43c2cca4f57261d57084945a02db4451c3069043f4aee1af"
    },
    {
      "relative_path": "experiment_v026/artifacts/development_bucket1_dataset.jsonl",
      "byte_count": 28801199,
      "sha256": "d5daecba36e3e8f9c6bbe60c8e2b13e6206290d8ca7cddcf4a8cc27c2f82274f"
    },
    {
      "relative_path": "experiment_v026/artifacts/development_bucket1_manifest.json",
      "byte_count": 312237,
      "sha256": "aa20ea73e71b7a3b9a41d444c8a8b7997216f0b85e53fbc5cffb663e25b67932"
    },
    {
      "relative_path": "experiment_v026/artifacts/development_bucket2_dataset.jsonl",
      "byte_count": 38050057,
      "sha256": "bd766eb62cf98e8fb1b8dd17c20d5edfc759eeb737bd3c232f73e656f9e713a3"
    },
    {
      "relative_path": "experiment_v026/artifacts/development_bucket2_manifest.json",
      "byte_count": 449291,
      "sha256": "9bcec296b8c380d21f084e60a860577a8e08b9188f8fce75d8c625a3671ee59e"
    },
    {
      "relative_path": "experiment_v026/artifacts/development_bucket3_dataset.jsonl",
      "byte_count": 28985207,
      "sha256": "0e701e4c842e4f661ec8e8650ec157e5462efe93bbb5d2514aab6a6c8167d77a"
    },
    {
      "relative_path": "experiment_v026/artifacts/development_bucket3_manifest.json",
      "byte_count": 353930,
      "sha256": "df2f4b46506978105121fe5afc36fcc2f1188dd1a5e6303cb2a2eef836cdc543"
    },
    {
      "relative_path": "experiment_v026/artifacts/evidence_packet_v026.md",
      "byte_count": 4336,
      "sha256": "0ad0e89d9dc7a690d4c4b586d10e37504df23c4a2e9d1a4541a1794dd9c1b3f8"
    },
    {
      "relative_path": "experiment_v026/artifacts/implementation_audit_v026.md",
      "byte_count": 5158,
      "sha256": "09d14ee91e2ec83f4e3bec8793bac78b6bf05c48616d7c977e6ca5551e2e8e13"
    },
    {
      "relative_path": "experiment_v026/artifacts/lottery_2606.08460.pdf",
      "byte_count": 512090,
      "sha256": "1bc52603140c3afee187346364aaa160f90c1e0678a36c10c3618e370b055096"
    },
    {
      "relative_path": "experiment_v026/artifacts/model.joblib",
      "byte_count": 27391551,
      "sha256": "b4fcce7cf474a2dbef4edfb2f03f4548d06f36d0912cd2fed74c9558b5a31629"
    },
    {
      "relative_path": "experiment_v026/artifacts/nearest_prior_v025.md",
      "byte_count": 1136,
      "sha256": "046f1f85659bfc4323f5c1831570e092341c93e3ac7cc78845a729b53ddda95b"
    },
    {
      "relative_path": "experiment_v026/artifacts/nearest_prior_v026.md",
      "byte_count": 2944,
      "sha256": "ef6bdfbdde465a052e188e18a90b9dcc3da97e4fff08703d1d6d29070a607963"
    },
    {
      "relative_path": "experiment_v026/artifacts/problem_v026.md",
      "byte_count": 1314,
      "sha256": "684374ba6b5dc74070429275a0e9dba7cab8067f957f4ac1c555e777fe386785"
    },
    {
      "relative_path": "experiment_v026/artifacts/program.py",
      "byte_count": 32328,
      "sha256": "d709235915e1406fa65c38b567773bc1fa43e3aad6be71e66bdd1b845053d2e1"
    },
    {
      "relative_path": "experiment_v026/artifacts/promotion_audit_v021.md",
      "byte_count": 6912,
      "sha256": "183cf86a029e5b3d88f8dac406605cd3c2287eca1d08f49e77de99055204e740"
    },
    {
      "relative_path": "experiment_v026/artifacts/promotion_audit_v025.md",
      "byte_count": 2140,
      "sha256": "9893b56f6957e613cd6e1123927138bd36dc05311830192ed1b74883f5577ae8"
    },
    {
      "relative_path": "experiment_v026/artifacts/promotion_audit_v026.md",
      "byte_count": 2256,
      "sha256": "1ef9d8162f325d7bd584eff5dd02a8cc2a750dc31ecfa73cb9b7e14872268c0d"
    },
    {
      "relative_path": "experiment_v026/artifacts/raw_analysis_v025.md",
      "byte_count": 3388,
      "sha256": "71a5e53f986f5778a87e752542849a543e22c0f945cf8b8dc1a32f8aa6775c5b"
    },
    {
      "relative_path": "experiment_v026/artifacts/raw_analysis_v026.md",
      "byte_count": 3610,
      "sha256": "ad769a213b455356e01ab943711faa75ed6e36c44d9f6b3d6b253d365f41a808"
    },
    {
      "relative_path": "experiment_v026/artifacts/raw_predictions.jsonl",
      "byte_count": 4213175,
      "sha256": "ee4a8c5961def6500b8f82105821c104347a337589f1ef0a067fa3ae961a87b8"
    },
    {
      "relative_path": "experiment_v026/artifacts/research_map_v026.md",
      "byte_count": 5527,
      "sha256": "932c5a7e37565b2f060df4f141e2c4db4660342f275a34ee58b0456066378f23"
    },
    {
      "relative_path": "experiment_v026/artifacts/result_v021.md",
      "byte_count": 11933,
      "sha256": "74437810a222a5f59cbc48789aa20d4b12847bddd6203c8c60a9c0ed008136f5"
    },
    {
      "relative_path": "experiment_v026/artifacts/result_v022.md",
      "byte_count": 15199,
      "sha256": "390b39c339be555ffbc43590d3554d5d7004b37406b60d86f9ecd3b453494f3c"
    },
    {
      "relative_path": "experiment_v026/artifacts/result_v025.md",
      "byte_count": 11304,
      "sha256": "873668f7b398deddfd58948dd5f4e7f1a453859a21e0293cf8f662c4fab67214"
    },
    {
      "relative_path": "experiment_v026/artifacts/run_local_experiment.py",
      "byte_count": 4338,
      "sha256": "410a620d0734613036f4fea4bc017c0cd1d0de293e1a3d4577c75eec584eaa4a"
    },
    {
      "relative_path": "experiment_v026/artifacts/selection_context_v026.md",
      "byte_count": 3069,
      "sha256": "dd1103b1f6bcf1036fcfcb07846519ccea75143445ad9b9a3e9a09f9acc705d8"
    },
    {
      "relative_path": "experiment_v026/artifacts/source_records.jsonl",
      "byte_count": 1232424,
      "sha256": "50f72ee7a1d99c9ad88a7b73bc06720584d633dbbdba3b25b42b6d4e700e4d4b"
    },
    {
      "relative_path": "experiment_v026/artifacts/summary.json",
      "byte_count": 8166,
      "sha256": "a14aab0834aea724daa6daa29d658b5f6c0544b6b9fb61257adf8ee43cfb000c"
    },
    {
      "relative_path": "experiment_v026/artifacts/terminal_wrench_2604.17596.pdf",
      "byte_count": 248630,
      "sha256": "140df68e633bcb5544e37b67a6f362a917f7a38b566b25e1b42fe86beb619e8a"
    },
    {
      "relative_path": "experiment_v026/artifacts/test_cmcd.py",
      "byte_count": 7845,
      "sha256": "f7accf7ea298e99765e4d87c594bff479d71b1e6c07269184d2ad3efc4fae9fc"
    },
    {
      "relative_path": "experiment_v026/artifacts/trajectory_guard_2601.00516.pdf",
      "byte_count": 334806,
      "sha256": "ab6d2c66b081b32a90ff3f230854058199c049362ffb49f46bef9f869fc18d34"
    },
    {
      "relative_path": "experiment_v026/artifacts/univad_2412.03342.pdf",
      "byte_count": 6001964,
      "sha256": "c20e32751c4f7b6332606a810ec07be854af0afb4c9202619a5822936d5b55a9"
    }
  ]
}
```

## Codex Interpretation

v026 executed the single frozen Development attempt and the single independent audit authorized by Plan `edcb1efbf5257fc52cda3983b810ac21134a618c0e692baf6a0eb41905ff0405`.

The Development runner exited 0 after 1,942.1450181 seconds. It produced 4,072 doubly held-out OOF rows from 228 eligible tasks. Candidate CMCD reached AUC 0.8832616788 and TPR@5%FPR 0.6340118745. The frozen strongest comparator was `single_support` at AUC 0.8732057902, so the aggregate AUC delta was +0.0100558886 with 2,000-task-bootstrap interval [0.0033534428, 0.0171627105].

The independent runner exited 0 with `AUDIT_OK`: nine bundles and 20,360 scores replayed, zero errors, maximum score error 0 and maximum metric/gate/structural error 0. The main Codex then joined all 4,072 raw rows and source records to 4,256 frozen dataset rows and 4,980 manifest source records with zero binding errors.

The Candidate passed seven of eight mechanical gates but failed the prospectively conjunctive all-generator-nonnegative gate: Claude delta +0.0112634324, Gemini delta -0.0042559106, GPT delta +0.0128789825. Gemini was negative in two of three task folds, and terminal-bench__2.0 was negative by -0.0330063222. Therefore the main Promotion Audit is `NO_GO_FOR_CONFIRMATION`. Bucket 0 was not acquired or read, no Review Packet or Reviewer was started, no Decision or Delivery exists, and the system remains `DEVELOPMENT_NOT_COMMISSIONED`.
