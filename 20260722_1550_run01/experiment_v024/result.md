# Experiment Result

```json
{
  "experiment_id": "v024",
  "execution_provenance": "caller_recorded",
  "plan_sha256": "30e6a7071686e036a7738b9af4d42b5f705949862b906740032799cd71c1f217",
  "candidate_sha256": "d7af6362080666bdecc927c8f2c65ea0894d2b7e1756d6434b61107ae8156c60",
  "evidence_packet_sha256": "87d886ba29d9096e35537802de1388f48fb2e9ef5f3a87b957044dedab99128f",
  "execution": {
    "command": "D:\\Desktop\\crl\\crl_agent_v3\\.venv\\python.exe D:\\Desktop\\crl\\20260722_1550_run01\\experiment_v024\\artifacts\\run_local_experiment.py --capture-dir D:\\Desktop\\crl\\20260722_1550_run01\\experiment_v024\\captures\\dev_acquire_001 --cwd D:\\Desktop\\crl\\20260722_1550_run01\\experiment_v024\\artifacts --input D:\\Desktop\\crl\\20260722_1550_run01\\experiment_v024\\artifacts\\config.json --output D:\\Desktop\\crl\\20260722_1550_run01\\experiment_v024\\dev_acquire_output_001\\dataset.jsonl --output D:\\Desktop\\crl\\20260722_1550_run01\\experiment_v024\\dev_acquire_output_001\\manifest.json -- D:\\Desktop\\crl\\crl_agent_v3\\.venv\\python.exe D:\\Desktop\\crl\\20260722_1550_run01\\experiment_v024\\artifacts\\acquire.py --phase development --config D:\\Desktop\\crl\\20260722_1550_run01\\experiment_v024\\artifacts\\config.json --output-dir D:\\Desktop\\crl\\20260722_1550_run01\\experiment_v024\\dev_acquire_output_001 --work-root D:\\Desktop\\crl\\20260722_1550_run01\\experiment_v024\\work\\dev_acquire_001",
    "cwd": "D:\\Desktop\\crl\\20260722_1550_run01\\experiment_v024\\artifacts",
    "exit_code": 1,
    "stdout": "",
    "stderr": "Traceback (most recent call last):\n  File \"D:\\Desktop\\crl\\20260722_1550_run01\\experiment_v024\\artifacts\\run_local_experiment.py\", line 136, in <module>\n    sys.exit(main())\n  File \"D:\\Desktop\\crl\\20260722_1550_run01\\experiment_v024\\artifacts\\run_local_experiment.py\", line 74, in main\n    capture_dir.mkdir()\n  File \"D:\\Desktop\\crl\\crl_agent_v3\\.venv\\Lib\\pathlib.py\", line 1116, in mkdir\n    os.mkdir(self, mode)\nFileNotFoundError: [WinError 3] ???????????: 'D:\\Desktop\\crl\\20260722_1550_run01\\experiment_v024\\captures\\dev_acquire_001'\n",
    "environment": {
      "python": "3.11.15",
      "python_executable": "D:\\Desktop\\crl\\crl_agent_v3\\.venv\\python.exe",
      "system_status": "DEVELOPMENT_NOT_COMMISSIONED"
    }
  },
  "artifacts": [
    {
      "relative_path": "experiment_v024/artifacts/selection_context_v024.md",
      "byte_count": 2076,
      "sha256": "3784287c7f93eb42aa8bd776f2c3f9fdb93391336f509d6d6674d82604b28690"
    },
    {
      "relative_path": "experiment_v024/artifacts/problem_v024.md",
      "byte_count": 1309,
      "sha256": "bd2d11c1f861ae98e43fee39aedda28de18a05456cdf69d536563cccdf4c9d1e"
    },
    {
      "relative_path": "experiment_v024/artifacts/research_map_v024.md",
      "byte_count": 5124,
      "sha256": "a775c4e8ac122a482e316699516b319decf4780f0997c2154c5b28f2f87bc034"
    },
    {
      "relative_path": "experiment_v024/artifacts/nearest_prior_v024.md",
      "byte_count": 2997,
      "sha256": "4c01037ddd330b41a84f80805239a64ce55774ee92b209a11e7595ba18ac61e5"
    },
    {
      "relative_path": "experiment_v024/artifacts/candidate_v024.md",
      "byte_count": 2123,
      "sha256": "d7af6362080666bdecc927c8f2c65ea0894d2b7e1756d6434b61107ae8156c60"
    },
    {
      "relative_path": "experiment_v024/artifacts/evidence_packet_v024.md",
      "byte_count": 4336,
      "sha256": "87d886ba29d9096e35537802de1388f48fb2e9ef5f3a87b957044dedab99128f"
    },
    {
      "relative_path": "experiment_v024/artifacts/implementation_audit_v024.md",
      "byte_count": 5289,
      "sha256": "56fd37fbc5b851adb5510b8d2cd691d2a6042c04db19690f022ddbee57f94ab0"
    },
    {
      "relative_path": "experiment_v024/artifacts/program.py",
      "byte_count": 23422,
      "sha256": "d47337fdf7cf9d6863c4efebb18abb9c7d80d72aec9a86df89cf28adbfd95437"
    },
    {
      "relative_path": "experiment_v024/artifacts/audit.py",
      "byte_count": 21053,
      "sha256": "7b0ec0a85d15ca6127ecadbf57d48e96a559d672dc2fea88e9cbeb73e7988dc7"
    },
    {
      "relative_path": "experiment_v024/artifacts/config.json",
      "byte_count": 1200,
      "sha256": "3e588a5d2052814b7bb64bc2cfc2d71d8838ded02fe2ab35ab8877f0f1faddd9"
    },
    {
      "relative_path": "experiment_v024/artifacts/test_viaf.py",
      "byte_count": 1937,
      "sha256": "1f334f43fb9222ef625f10732b9f17b072c5439cbfef76709ea28bf5b381a3fb"
    },
    {
      "relative_path": "experiment_v024/artifacts/base_v012.py",
      "byte_count": 39154,
      "sha256": "a29b8aace75bf5505620fab71c982e296e045cb1590a20a5a9c19a63c233d78d"
    },
    {
      "relative_path": "experiment_v024/artifacts/acquire.py",
      "byte_count": 12438,
      "sha256": "cf87ec4994081b4516695806b471daf75e923fe511d0b67d05b4ab126d34e836"
    },
    {
      "relative_path": "experiment_v024/artifacts/run_local_experiment.py",
      "byte_count": 4338,
      "sha256": "410a620d0734613036f4fea4bc017c0cd1d0de293e1a3d4577c75eec584eaa4a"
    },
    {
      "relative_path": "experiment_v024/artifacts/terminal_wrench_2604.17596.pdf",
      "byte_count": 248630,
      "sha256": "140df68e633bcb5544e37b67a6f362a917f7a38b566b25e1b42fe86beb619e8a"
    },
    {
      "relative_path": "experiment_v024/artifacts/cheap_reward_hacking_2606.08893.pdf",
      "byte_count": 1278533,
      "sha256": "c5fd945125b1b6cd4739b2aacf150156bbfc8e47aff2d7240ea05ed697075ce0"
    },
    {
      "relative_path": "experiment_v024/artifacts/trajectory_guard_2601.00516.pdf",
      "byte_count": 334806,
      "sha256": "ab6d2c66b081b32a90ff3f230854058199c049362ffb49f46bef9f869fc18d34"
    },
    {
      "relative_path": "experiment_v024/artifacts/trajad_2602.06443.pdf",
      "byte_count": 1148109,
      "sha256": "3237bcd13e7f2926c3f3cd3891c661ea398f57f1cb347523c87a217a73278fec"
    },
    {
      "relative_path": "experiment_v024/artifacts/agentrx_2602.02475.pdf",
      "byte_count": 616888,
      "sha256": "59680fd631934d6ad3046108a504195e8cd70066bdefbfb3561b7731f7d22923"
    },
    {
      "relative_path": "experiment_v024/artifacts/strained_coherence_2606.07889.pdf",
      "byte_count": 164886,
      "sha256": "33a2ee601361ab3c538732133ff2a937c93f765f112451a9bf96899d9fce3271"
    },
    {
      "relative_path": "experiment_v024/artifacts/promotion_audit_v023.md",
      "byte_count": 6435,
      "sha256": "ef9e892b449236ca4ec1f5b9b77c03f65d4716a0b33ec722a3b2f1a29ffd046d"
    },
    {
      "relative_path": "experiment_v024/artifacts/result_v023.md",
      "byte_count": 17430,
      "sha256": "8fb3cf684631c3996dfa0d9664266d283231d483a9be48d84e695c2df7926723"
    },
    {
      "relative_path": "experiment_v024/artifacts/attempts_manifest_v023.json",
      "byte_count": 1161,
      "sha256": "0003061496894f74991406fedd65e0e0d42317a2fe7ec7e7b1d6e022ea221cc7"
    },
    {
      "relative_path": "experiment_v024/artifacts/attempts_manifest_v024.json",
      "byte_count": 1496,
      "sha256": "521e02d57e11075b5cc1cc1fe528a317ff1384dee9d6eca8adea3764f472db09"
    },
    {
      "relative_path": "experiment_v024/artifacts/promotion_audit_v024.md",
      "byte_count": 1537,
      "sha256": "993cdab1120f8c51d8d47beba7c5cf19a7d6fd0fd817fb12aeb256b91e00dc4d"
    }
  ]
}
```

## Codex Interpretation

The single planned acquisition runner failed before its payload because the capture parent directory did not exist. No bucket-1 or bucket-0 data byte was acquired, so this is not a scientific result. The frozen Plan prohibits a same-version retry. v024 is closed as NO_GO_FOR_SAME_VERSION_RETRY and the same Run must advance to an execution-only v025 correction. There is no Confirmation, Review, Decision, Delivery, or Ready authorization.