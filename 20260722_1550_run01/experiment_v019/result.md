# Experiment Result

```json
{
  "experiment_id": "v019",
  "execution_provenance": "caller_recorded",
  "plan_sha256": "d44d80f2bc1f39493147f460ffcb34a059e9a206e104932d1a24a6bfff3e850f",
  "candidate_sha256": "30c51e3cbadb8affc925d42ff91b12240dc3e018e83df0069d5dcdbdb21026de",
  "evidence_packet_sha256": "d9239666b23a0aadc725f67c95dacccad1ef280a4537d3f48deba8d6ed2481f1",
  "execution": {
    "command": "[\"D:\\\\Desktop\\\\crl\\\\crl_agent_v3\\\\.venv\\\\python.exe\", \"D:\\\\Desktop\\\\crl\\\\20260722_1550_run01\\\\experiment_v019\\\\artifacts\\\\program.py\", \"--phase\", \"development\", \"--config\", \"D:\\\\Desktop\\\\crl\\\\20260722_1550_run01\\\\experiment_v019\\\\artifacts\\\\config.json\", \"--input\", \"D:\\\\Desktop\\\\crl\\\\20260722_1550_run01\\\\experiment_v019\\\\artifacts\\\\BFCL_v3_simple.json\", \"--rank-bm25-wheel\", \"D:\\\\Desktop\\\\crl\\\\20260722_1550_run01\\\\experiment_v019\\\\artifacts\\\\rank_bm25-0.2.2-py3-none-any.whl\", \"--output-dir\", \"D:\\\\Desktop\\\\crl\\\\20260722_1550_run01\\\\experiment_v019\\\\dev_output_001\"]",
    "cwd": "D:\\Desktop\\crl\\20260722_1550_run01\\experiment_v019\\artifacts",
    "exit_code": 0,
    "stdout": "training policy=target_bor_dqn seed=42 episode=3000/8000\r\ntraining policy=target_bor_dqn seed=42 episode=6000/8000\r\ntraining policy=target_f1_dqn seed=42 episode=3000/8000\r\ntraining policy=target_f1_dqn seed=42 episode=6000/8000\r\ntraining policy=unconstrained_ratio_dqn seed=42 episode=3000/8000\r\ntraining policy=unconstrained_ratio_dqn seed=42 episode=6000/8000\r\ntraining policy=coverage_constrained_chance_dqn seed=42 episode=3000/8000\r\ntraining policy=coverage_constrained_chance_dqn seed=42 episode=6000/8000\r\ntraining policy=target_bor_dqn seed=123 episode=3000/8000\r\ntraining policy=target_bor_dqn seed=123 episode=6000/8000\r\ntraining policy=target_f1_dqn seed=123 episode=3000/8000\r\ntraining policy=target_f1_dqn seed=123 episode=6000/8000\r\ntraining policy=unconstrained_ratio_dqn seed=123 episode=3000/8000\r\ntraining policy=unconstrained_ratio_dqn seed=123 episode=6000/8000\r\ntraining policy=coverage_constrained_chance_dqn seed=123 episode=3000/8000\r\ntraining policy=coverage_constrained_chance_dqn seed=123 episode=6000/8000\r\ntraining policy=target_bor_dqn seed=456 episode=3000/8000\r\ntraining policy=target_bor_dqn seed=456 episode=6000/8000\r\ntraining policy=target_f1_dqn seed=456 episode=3000/8000\r\ntraining policy=target_f1_dqn seed=456 episode=6000/8000\r\ntraining policy=unconstrained_ratio_dqn seed=456 episode=3000/8000\r\ntraining policy=unconstrained_ratio_dqn seed=456 episode=6000/8000\r\ntraining policy=coverage_constrained_chance_dqn seed=456 episode=3000/8000\r\ntraining policy=coverage_constrained_chance_dqn seed=456 episode=6000/8000\r\n{\"candidate_coverage\": 1.0, \"candidate_mean_k\": 370.0, \"elapsed_seconds\": 3269.0649259000056, \"phase\": \"development\", \"rows\": 2160, \"target_coverage\": 0.7916666666666666, \"target_mean_k\": 5.1499999999999995}\r\n",
    "stderr": "",
    "environment": {
      "cuda_available": "true",
      "cuda_runtime": "13.0",
      "gpu": "NVIDIA GeForce RTX 5060 Ti",
      "python": "3.11.15",
      "python_executable": "D:\\Desktop\\crl\\crl_agent_v3\\.venv\\python.exe",
      "runner_duration_seconds": "3271.7866745000065",
      "torch": "2.12.0+cu130",
      "training_device": "cpu"
    }
  },
  "artifacts": [
    {
      "relative_path": "experiment_v019/artifacts/BFCL_v3_simple.json",
      "byte_count": 280474,
      "sha256": "fbc37b2ad252bf9af985582e0e07b456173fe627d957491472ea9cef5fb83158"
    },
    {
      "relative_path": "experiment_v019/artifacts/audit.py",
      "byte_count": 21848,
      "sha256": "806794c0d46e706065c058281fe7db6b1fc598368cb3e59d5d9a78263a1c67c1"
    },
    {
      "relative_path": "experiment_v019/artifacts/bits_over_random_2605.18857.pdf",
      "byte_count": 527815,
      "sha256": "8587a2502cf4f5fa371a04eaca3eec4d782ad52d0a12f346606ee2ffd4b3ec02"
    },
    {
      "relative_path": "experiment_v019/artifacts/candidate_v019.md",
      "byte_count": 8842,
      "sha256": "30c51e3cbadb8affc925d42ff91b12240dc3e018e83df0069d5dcdbdb21026de"
    },
    {
      "relative_path": "experiment_v019/artifacts/config.json",
      "byte_count": 2312,
      "sha256": "bdd2683af36f5babed46203a66c419ff3017625a204649909f59b4b0aa478cbf"
    },
    {
      "relative_path": "experiment_v019/artifacts/dev_001_execution.json",
      "byte_count": 8028,
      "sha256": "6596b0748acbfa6804db05173e2f108dbac295be2678a52e27ed20cd9b0b6c00"
    },
    {
      "relative_path": "experiment_v019/artifacts/dev_001_stderr.bin",
      "byte_count": 0,
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    },
    {
      "relative_path": "experiment_v019/artifacts/dev_001_stdout.bin",
      "byte_count": 1767,
      "sha256": "91435cade294c11cc503f10926c75f4af52ad87b0c7ae9a0e5b0b8c56a99e4ba"
    },
    {
      "relative_path": "experiment_v019/artifacts/dev_audit_001_execution.json",
      "byte_count": 6792,
      "sha256": "d19ec3e75a491689f5022a6ff87a9d14c0ba013ac29fefeb62ab2f3c6434b365"
    },
    {
      "relative_path": "experiment_v019/artifacts/dev_audit_001_stderr.bin",
      "byte_count": 0,
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    },
    {
      "relative_path": "experiment_v019/artifacts/dev_audit_001_stdout.bin",
      "byte_count": 127,
      "sha256": "1296d5871dcde4ea2144d3f1598b164dcbbd7771d2e1031159e0f54af1736414"
    },
    {
      "relative_path": "experiment_v019/artifacts/dev_audit_report.json",
      "byte_count": 861,
      "sha256": "f4d75de02331b89014ce60a77bc2ffcb92026848a8a6aac4df77e5ac493a2128"
    },
    {
      "relative_path": "experiment_v019/artifacts/dev_controller_history.json",
      "byte_count": 24702,
      "sha256": "9f5901f7c6ef739ba53c8668dbc0299733646a9b850788c8866a5d9fc5c41ae0"
    },
    {
      "relative_path": "experiment_v019/artifacts/dev_coverage_constrained_chance_dqn_seed123.pt",
      "byte_count": 22741,
      "sha256": "229a9af136c839dbe1d1e2e448a55d166029a1b6180e3eb9fea7b4e0523b460a"
    },
    {
      "relative_path": "experiment_v019/artifacts/dev_coverage_constrained_chance_dqn_seed42.pt",
      "byte_count": 22729,
      "sha256": "df525c628a57f27644d37a49e0d23bf20a8b55a7e1075f71e6cc63044c8994f6"
    },
    {
      "relative_path": "experiment_v019/artifacts/dev_coverage_constrained_chance_dqn_seed456.pt",
      "byte_count": 22741,
      "sha256": "f15271d2867b7988dca8f27ff76c3d9554d3763116a58705a8707150aca58ac2"
    },
    {
      "relative_path": "experiment_v019/artifacts/dev_raw_rows.jsonl",
      "byte_count": 407046,
      "sha256": "68dc0bc02218c853245b00af22ffbf539873c42a2a48d85a6db3cb1bb9ab6897"
    },
    {
      "relative_path": "experiment_v019/artifacts/dev_split_manifest.json",
      "byte_count": 7246,
      "sha256": "2fd0bdf6a678067989d9027e6dbfbd3eb32bdf6d9d5793c2388ae8ffede86948"
    },
    {
      "relative_path": "experiment_v019/artifacts/dev_summary.json",
      "byte_count": 49864,
      "sha256": "928af6f01551c033bbccbc1004c35ec0cb255322cfa930d5cf7d9ab465105aef"
    },
    {
      "relative_path": "experiment_v019/artifacts/dev_target_bor_dqn_seed123.pt",
      "byte_count": 22537,
      "sha256": "e4b6cc3a261cbe1bfad74f5e94cf0d82c5689a4e83dda3aa4664072706f5ff0e"
    },
    {
      "relative_path": "experiment_v019/artifacts/dev_target_bor_dqn_seed42.pt",
      "byte_count": 22461,
      "sha256": "be48d4d751efeeb53e672c76f70e950c017de872362bd106158ee3424e3bdc2e"
    },
    {
      "relative_path": "experiment_v019/artifacts/dev_target_bor_dqn_seed456.pt",
      "byte_count": 22537,
      "sha256": "d6b25cd6c50a71e8c97b3644f14049fe5a298e8bff6fa8f0db4f16f77e8762bf"
    },
    {
      "relative_path": "experiment_v019/artifacts/dev_target_f1_dqn_seed123.pt",
      "byte_count": 22461,
      "sha256": "122ad7cb192ff7f012976a2108053c99254472e864ced083650e7f4b1b7d4117"
    },
    {
      "relative_path": "experiment_v019/artifacts/dev_target_f1_dqn_seed42.pt",
      "byte_count": 22449,
      "sha256": "5a13d2ca60eadd333de05fd633a968b11e846c24c034451d67bfdbaa10b013f4"
    },
    {
      "relative_path": "experiment_v019/artifacts/dev_target_f1_dqn_seed456.pt",
      "byte_count": 22461,
      "sha256": "30875effd4d551fcb096e87b659f1bd70f5e66438f9ac42dc1fb5f48ec6f33d3"
    },
    {
      "relative_path": "experiment_v019/artifacts/dev_unconstrained_ratio_dqn_seed123.pt",
      "byte_count": 22645,
      "sha256": "5921cc17569e00035f9e9725cc5cd868196cad48263cf3c554dbf57d5d33ec01"
    },
    {
      "relative_path": "experiment_v019/artifacts/dev_unconstrained_ratio_dqn_seed42.pt",
      "byte_count": 22633,
      "sha256": "597ad9d5fbf5842ab32a6d9d060a59a19519618e5ac3b43de603fd639f5baf16"
    },
    {
      "relative_path": "experiment_v019/artifacts/dev_unconstrained_ratio_dqn_seed456.pt",
      "byte_count": 22645,
      "sha256": "179612ab7706882f4b97b386cb12e3ce26cc5208fedd433be4c985c6d49f2778"
    },
    {
      "relative_path": "experiment_v019/artifacts/evidence_packet_v019.md",
      "byte_count": 5972,
      "sha256": "d9239666b23a0aadc725f67c95dacccad1ef280a4537d3f48deba8d6ed2481f1"
    },
    {
      "relative_path": "experiment_v019/artifacts/how_many_tools_2605.24660.pdf",
      "byte_count": 400683,
      "sha256": "4db89bfac79bc90dd5b532d04ac1012ed1691657a45379bbbb2312682847164c"
    },
    {
      "relative_path": "experiment_v019/artifacts/implementation_audit_v019.md",
      "byte_count": 6455,
      "sha256": "3a999df62100d6b6fdf6f47a2a3d0e991f7f4ecdaf6152b56dfacc3b006b7eb4"
    },
    {
      "relative_path": "experiment_v019/artifacts/nearest_prior_v019.md",
      "byte_count": 5610,
      "sha256": "5a04d7cba80e638f83aed7c59dca3ee9da78b32ccc3b0073b3b41cd622cb2cc4"
    },
    {
      "relative_path": "experiment_v019/artifacts/offline_adaptive_retrieval_2604.05125.pdf",
      "byte_count": 633333,
      "sha256": "357ec6826e8c4032d9f807cc31440e5bfe47f4b4003c22ef698a4eb85469122f"
    },
    {
      "relative_path": "experiment_v019/artifacts/problem_v019.md",
      "byte_count": 2440,
      "sha256": "17cf78b192508287ef9fa6a5687062338f03073bffc72e09a78c3ec1fe4bf660"
    },
    {
      "relative_path": "experiment_v019/artifacts/program.py",
      "byte_count": 28918,
      "sha256": "ddb36e59145228362597da2e559ed22ca987499e32cb25519293c9d3f4c4375a"
    },
    {
      "relative_path": "experiment_v019/artifacts/promotion_audit_v019.md",
      "byte_count": 5179,
      "sha256": "b80db3f45f429a793dd7b26149df95f93726885b51c8f4c747d63f699c64a78e"
    },
    {
      "relative_path": "experiment_v019/artifacts/rank_bm25-0.2.2-py3-none-any.whl",
      "byte_count": 8584,
      "sha256": "7bd4a95571adadfc271746fa146a4bcfd89c0cf731e49c3d1ad863290adbe8ae"
    },
    {
      "relative_path": "experiment_v019/artifacts/ratio_rl_icml2021.pdf",
      "byte_count": 541248,
      "sha256": "949fe7d0d8137a6ef1190bfca17f258603602ac881d8f99f04d1b720c71da877"
    },
    {
      "relative_path": "experiment_v019/artifacts/research_map_v019.md",
      "byte_count": 5938,
      "sha256": "257aab86d37e5c3d62c42cde10bf378572aa43459f6c5e626feb3fd992e54412"
    },
    {
      "relative_path": "experiment_v019/artifacts/selection_context_v019.md",
      "byte_count": 6055,
      "sha256": "216179aec060299c897994f9a44dbeb29a382f7a5206f646b3396e65973731e6"
    },
    {
      "relative_path": "experiment_v019/artifacts/target_bfcl_bm25_notebook.ipynb",
      "byte_count": 171036,
      "sha256": "61da53127597d7a90a440a87ff2efcea77665454852d50552df9bb2972a6ff81"
    },
    {
      "relative_path": "experiment_v019/artifacts/test_objective.py",
      "byte_count": 1516,
      "sha256": "e0fc74c3033b9010158e69829e95e9ac9b571f759b2895001a0894c6ba66e367"
    }
  ]
}
```

## Codex Interpretation

v019 completed one real Development capture and one independent audit capture. The audit returned AUDIT_OK with 0 errors, 2,160 rows, 18 groups, 96 controller updates, 12 models, and 1,440 replayed learned-policy actions. The maximum metric recomputation error was 1.3322676295501878e-14, within the frozen 1e-12 Candidate tolerance.

The Candidate failed scientifically: all three seeds selected K=370 for every Development query. Relative to target BoR-DQN, mean coverage changed by +0.208333, mean K by +364.85, and defined BoR by -5.830157; matched-seed support was 0/3. Main-Codex Promotion disposition is NO_GO_FOR_CONFIRMATION. The prospective Confirmation source was not acquired, no Reviewer was started, and no Delivery was created. See frozen `promotion_audit_v019.md` for the raw-case and dual-trajectory judgment.
