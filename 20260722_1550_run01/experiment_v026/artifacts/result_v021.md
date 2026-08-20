# Experiment Result

```json
{
  "experiment_id": "v021",
  "execution_provenance": "caller_recorded",
  "plan_sha256": "f578b11735364c67430f2e03ea1c1c7ec0107a00051e194349ac9239b8bbff50",
  "candidate_sha256": "fd3978d343d0ca33a2301a3c2e7e7b2897c37b2b2c3e5ab74ae393608ee4e917",
  "evidence_packet_sha256": "bb17ab6db299968bba3fcbba599f2f6e9a0fe4095497be2c2d47d36674a825cf",
  "execution": {
    "command": "[\"D:\\\\Desktop\\\\crl\\\\crl_agent_v3\\\\.venv\\\\python.exe\", \"D:\\\\Desktop\\\\crl\\\\20260722_1550_run01\\\\experiment_v021\\\\artifacts\\\\acquire.py\", \"--phase\", \"confirmation\", \"--config\", \"D:\\\\Desktop\\\\crl\\\\20260722_1550_run01\\\\experiment_v021\\\\artifacts\\\\config.json\", \"--output-dir\", \"D:\\\\Desktop\\\\crl\\\\20260722_1550_run01\\\\experiment_v021\\\\confirmation_acquire_output_001\", \"--work-root\", \"D:\\\\Desktop\\\\crl\\\\20260722_1550_run01\\\\experiment_v021\\\\work\\\\confirmation_acquire_001\"]",
    "cwd": "D:\\Desktop\\crl\\20260722_1550_run01\\experiment_v021\\artifacts",
    "exit_code": 1,
    "stdout": "",
    "stderr": "Traceback (most recent call last):\r\n  File \"D:\\Desktop\\crl\\20260722_1550_run01\\experiment_v021\\artifacts\\acquire.py\", line 391, in <module>\r\n    raise SystemExit(main())\r\n                     ^^^^^^\r\n  File \"D:\\Desktop\\crl\\20260722_1550_run01\\experiment_v021\\artifacts\\acquire.py\", line 300, in main\r\n    repo = initialize_repository(\r\n           ^^^^^^^^^^^^^^^^^^^^^^\r\n  File \"D:\\Desktop\\crl\\20260722_1550_run01\\experiment_v021\\artifacts\\acquire.py\", line 57, in initialize_repository\r\n    run_git(\r\n  File \"D:\\Desktop\\crl\\20260722_1550_run01\\experiment_v021\\artifacts\\acquire.py\", line 27, in run_git\r\n    result = subprocess.run(\r\n             ^^^^^^^^^^^^^^^\r\n  File \"D:\\Desktop\\crl\\crl_agent_v3\\.venv\\Lib\\subprocess.py\", line 571, in run\r\n    raise CalledProcessError(retcode, process.args,\r\nsubprocess.CalledProcessError: Command '['git', '-C', 'D:\\\\Desktop\\\\crl\\\\20260722_1550_run01\\\\experiment_v021\\\\work\\\\confirmation_acquire_001\\\\repository', 'fetch', '--depth=1', '--filter=blob:none', 'origin', 'd8a29613235a0ef56a8b70b3142626a533da28c2']' returned non-zero exit status 128.\r\n",
    "environment": {
      "development_gpu": "NVIDIA GeForce RTX 5060 Ti",
      "git_ls_remote_exit": "0",
      "git_ls_remote_head": "d8a29613235a0ef56a8b70b3142626a533da28c2",
      "phase": "confirmation_acquisition",
      "platform": "Windows-10-10.0.26100-SP0",
      "python": "3.11.15",
      "python_executable": "D:\\Desktop\\crl\\crl_agent_v3\\.venv\\python.exe"
    }
  },
  "artifacts": [
    {
      "relative_path": "experiment_v021/artifacts/acquire.py",
      "byte_count": 12438,
      "sha256": "cf87ec4994081b4516695806b471daf75e923fe511d0b67d05b4ab126d34e836"
    },
    {
      "relative_path": "experiment_v021/artifacts/audit.py",
      "byte_count": 2522,
      "sha256": "ff499a10f80fb4d428291d3fa43142a3248705d93fcefc506eeba74cb3c6c4a5"
    },
    {
      "relative_path": "experiment_v021/artifacts/base_v012.py",
      "byte_count": 39154,
      "sha256": "a29b8aace75bf5505620fab71c982e296e045cb1590a20a5a9c19a63c233d78d"
    },
    {
      "relative_path": "experiment_v021/artifacts/base_v020_audit.py",
      "byte_count": 15672,
      "sha256": "2f42878764989288ee44a68d287af2cccfb2e25f72f7eb2fde40e9d81a898607"
    },
    {
      "relative_path": "experiment_v021/artifacts/base_v020_program.py",
      "byte_count": 17872,
      "sha256": "67ac151b6817d6619f915aad581da6c70f9ecdafeb780d87e31816c36009de92"
    },
    {
      "relative_path": "experiment_v021/artifacts/candidate_v021.md",
      "byte_count": 2119,
      "sha256": "fd3978d343d0ca33a2301a3c2e7e7b2897c37b2b2c3e5ab74ae393608ee4e917"
    },
    {
      "relative_path": "experiment_v021/artifacts/cheap_reward_hacking_2606.08893.pdf",
      "byte_count": 1278533,
      "sha256": "c5fd945125b1b6cd4739b2aacf150156bbfc8e47aff2d7240ea05ed697075ce0"
    },
    {
      "relative_path": "experiment_v021/artifacts/config.json",
      "byte_count": 1675,
      "sha256": "8d6eee0a9fdb29e286b918eb13a02bbf5ad246b5467b4ea2f93e9fe93ee50eb0"
    },
    {
      "relative_path": "experiment_v021/artifacts/confirmation_acquire_001_execution.json",
      "byte_count": 2309,
      "sha256": "cdb05c3867ae73b5df2f4b3a6b275b36326387fb3e4883449dfe2e51ac069195"
    },
    {
      "relative_path": "experiment_v021/artifacts/confirmation_acquire_001_stderr.bin",
      "byte_count": 1089,
      "sha256": "91f099fcd2c2662796c490d11181b2c45e88943e24e775b180f85a8e562d5d00"
    },
    {
      "relative_path": "experiment_v021/artifacts/confirmation_acquire_001_stdout.bin",
      "byte_count": 0,
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    },
    {
      "relative_path": "experiment_v021/artifacts/confirmation_acquisition_failure_v021.md",
      "byte_count": 1516,
      "sha256": "087f8f7380bd89410075c1c74b148fd0f31f83e0faf6a6b556763bc911628186"
    },
    {
      "relative_path": "experiment_v021/artifacts/confirmation_plan_v021.md",
      "byte_count": 7863,
      "sha256": "6c42087ea9bb66916fbb0dd70bcca77ef421a43ecb88085666ad5aa7d8881c48"
    },
    {
      "relative_path": "experiment_v021/artifacts/dev_001_execution.json",
      "byte_count": 3957,
      "sha256": "85c8623168280d102e0cd3d057dca46181503eda365fa705a850083cdc7eb9f6"
    },
    {
      "relative_path": "experiment_v021/artifacts/dev_001_stderr.bin",
      "byte_count": 0,
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    },
    {
      "relative_path": "experiment_v021/artifacts/dev_001_stdout.bin",
      "byte_count": 160,
      "sha256": "926ef1e1343a4ecc5292ede7f195626427dec5f74da126f2aaa635de543c278d"
    },
    {
      "relative_path": "experiment_v021/artifacts/dev_audit_001_execution.json",
      "byte_count": 4320,
      "sha256": "beab44c2d78442c59070c39c51fc7829d8adbf60670fd8f5d00fd2fd9c1fd673"
    },
    {
      "relative_path": "experiment_v021/artifacts/dev_audit_001_stderr.bin",
      "byte_count": 0,
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    },
    {
      "relative_path": "experiment_v021/artifacts/dev_audit_001_stdout.bin",
      "byte_count": 129,
      "sha256": "a7a3356855b7340e7f2e8cae4402b2bccf9ceadcbd10f7799a67f3025d3d487d"
    },
    {
      "relative_path": "experiment_v021/artifacts/dev_audit_report.json",
      "byte_count": 749,
      "sha256": "29e5a29d14f5d167bb4a22c3099b3dc7070bb4cf73675a74a2a5d69706c12822"
    },
    {
      "relative_path": "experiment_v021/artifacts/dev_model.joblib",
      "byte_count": 4627780,
      "sha256": "8ff9c2cc3ec1ade5aa404323264738800a909c7690d3b867ea48e6fb68fa56f7"
    },
    {
      "relative_path": "experiment_v021/artifacts/dev_raw_predictions.jsonl",
      "byte_count": 216506,
      "sha256": "483d930e9cc1a14bed0bff91f8b8aae465842ff852d09ce9298f3ad83e341f80"
    },
    {
      "relative_path": "experiment_v021/artifacts/dev_reference_records.jsonl",
      "byte_count": 29030,
      "sha256": "da71beb34381f3c43f90088bf9f3bca5329ed8bddcb37e7559e10064f8e5b52b"
    },
    {
      "relative_path": "experiment_v021/artifacts/dev_summary.json",
      "byte_count": 6569,
      "sha256": "86b684cffc204d6f5fd8a805283bad5c0463ee7f34cbc28ef057b92b9f104b42"
    },
    {
      "relative_path": "experiment_v021/artifacts/development_dataset.jsonl",
      "byte_count": 38050057,
      "sha256": "bd766eb62cf98e8fb1b8dd17c20d5edfc759eeb737bd3c232f73e656f9e713a3"
    },
    {
      "relative_path": "experiment_v021/artifacts/evidence_packet_v021.md",
      "byte_count": 4336,
      "sha256": "bb17ab6db299968bba3fcbba599f2f6e9a0fe4095497be2c2d47d36674a825cf"
    },
    {
      "relative_path": "experiment_v021/artifacts/implementation_audit_v021.md",
      "byte_count": 4094,
      "sha256": "ef0adbd4f66677f2b07586856619ba883f348f3d1faeb7ea130b205c2be03b43"
    },
    {
      "relative_path": "experiment_v021/artifacts/nearest_prior_v021.md",
      "byte_count": 876,
      "sha256": "35975e55ce835985abf6662c0b0d18304070f72f6ee8fd0198b60ae889b1a302"
    },
    {
      "relative_path": "experiment_v021/artifacts/praetor_2604.26274.pdf",
      "byte_count": 605389,
      "sha256": "842d593f53486481d384c8407d2fd688bbfbf90b69e505db54bc31008a15aa98"
    },
    {
      "relative_path": "experiment_v021/artifacts/problem_v021.md",
      "byte_count": 812,
      "sha256": "6486dd91e5c050250ba08d598e24731fe5b89b85c96dd36ff797b20594fe874c"
    },
    {
      "relative_path": "experiment_v021/artifacts/program.py",
      "byte_count": 2695,
      "sha256": "98e1f01451bfb6bc592dc2a8f24f23b10ac709fe665d40c5885ee20f6c5ef8d7"
    },
    {
      "relative_path": "experiment_v021/artifacts/promotion_audit_v020.md",
      "byte_count": 4538,
      "sha256": "8b67077e39644645719a3c7a6791d405e6be4f733c11dcdb2400e002e5eae6a8"
    },
    {
      "relative_path": "experiment_v021/artifacts/promotion_audit_v021.md",
      "byte_count": 6912,
      "sha256": "183cf86a029e5b3d88f8dac406605cd3c2287eca1d08f49e77de99055204e740"
    },
    {
      "relative_path": "experiment_v021/artifacts/research_map_v021.md",
      "byte_count": 1293,
      "sha256": "87502531e106eb0e2cfc1f1d789c5a6463dd716db9338b14ff842ed1e6684ea3"
    },
    {
      "relative_path": "experiment_v021/artifacts/result_v020.md",
      "byte_count": 8889,
      "sha256": "1c25418fe891ed53cd8566bf62485bf7cc2cbe56893fbdd3b52f16117ec95fdd"
    },
    {
      "relative_path": "experiment_v021/artifacts/selection_context_v021.md",
      "byte_count": 1107,
      "sha256": "d11bc6f7a005909de63956c380c7953e46c7fa0a55e5c64c81fbd57cc8616592"
    },
    {
      "relative_path": "experiment_v021/artifacts/terminal_wrench_2604.17596.pdf",
      "byte_count": 248630,
      "sha256": "140df68e633bcb5544e37b67a6f362a917f7a38b566b25e1b42fe86beb619e8a"
    },
    {
      "relative_path": "experiment_v021/artifacts/test_capacity_controls.py",
      "byte_count": 1029,
      "sha256": "9a631beeaa14c1345554cb4ac936d99150496616d1f8d0f11a0a62462799bbc7"
    },
    {
      "relative_path": "experiment_v021/artifacts/trace_2601.20103.pdf",
      "byte_count": 2244476,
      "sha256": "98a3121de46018f08f47a8db18b4ed55c9d117beb5e984eaa9f3c2a47f3a5649"
    }
  ]
}
```

## Codex Interpretation

v021 completed one real comparator-complete Development fit and one independent replay audit before attempting Confirmation. Candidate AUC was 0.9408656005 versus the new capacity-matched strongest comparator duplicated-absolute at 0.9251839315; task-cluster delta was +0.0156816690 with 95% interval [+0.0041492512,+0.0253812488]. All seven Development gates passed. The independent audit replayed 2,464 scores across seven models with zero score and metric error. Main-Codex raw-row review found 17 Candidate-only correct threshold decisions and two strongest-only correct decisions, resolved the v020 capacity objection, retained four worse per-task AUC slices and 69 Candidate false negatives as limitations, and authorized untouched bucket-3 Confirmation in promotion_audit_v021.md.

The single frozen bucket-3 acquisition then exited 1 during Git fetch after 7.5467165 seconds. Both declared outputs remained absent: zero dataset bytes and zero manifest bytes. No sparse task metadata, trajectory, Confirmation row, label, score, metric or prediction was produced. A read-only git ls-remote diagnostic subsequently exited 0 and showed the exact pinned commit remained remote HEAD, identifying an execution-only transient fetch failure rather than a scientific failure. v021 is frozen and must not retry. The same scientific Candidate continues only as v022 with new immutable version bindings and a new one-shot acquisition Plan. No Reviewer was started and no Delivery exists. System remains DEVELOPMENT_NOT_COMMISSIONED.