# Experiment Result

```json
{
  "experiment_id": "v013",
  "execution_provenance": "caller_recorded",
  "plan_sha256": "220b618a4810870f188eda537f5876ff6905a173581323ab8e8bae766e5bf24d",
  "candidate_sha256": "50ad937e5aa6df51e76223ef002a675273902a59d71170082d05c222db61fff5",
  "evidence_packet_sha256": "1e8563b6eccb27dacef35f2c0b277b80c1742ce2ebc2ad83984053a59cb3c96e",
  "execution": {
    "command": "dev_eval_001 + dev_audit_001",
    "cwd": "D:\\Desktop\\crl\\20260722_1550_run01\\implementation_v013",
    "exit_code": 0,
    "stdout": "dev_eval_001 exit 0; dev_audit_001 exit 0; 1440 raw rows; 27 strict reversals",
    "stderr": "",
    "environment": {
      "cuda_runtime": "13.0",
      "development_device": "cpu",
      "gpu_available": "True",
      "gpu_name": "NVIDIA GeForce RTX 5060 Ti",
      "numpy": "2.3.5",
      "python": "3.11.15",
      "python_executable": "D:\\Desktop\\crl\\crl_agent_v3\\.venv\\python.exe",
      "scipy": "1.16.0",
      "system_status": "DEVELOPMENT_NOT_COMMISSIONED",
      "torch": "2.12.0+cu130"
    }
  },
  "artifacts": [
    {
      "relative_path": "experiment_v013/artifacts/BFCL_v3_simple.json",
      "byte_count": 280474,
      "sha256": "fbc37b2ad252bf9af985582e0e07b456173fe627d957491472ea9cef5fb83158"
    },
    {
      "relative_path": "experiment_v013/artifacts/attempts_manifest.json",
      "byte_count": 3531,
      "sha256": "fe0fc6c738a72ade625abfa0185152a67a64e713729125018fba0015734c7770"
    },
    {
      "relative_path": "experiment_v013/artifacts/bor_paper.pdf",
      "byte_count": 527815,
      "sha256": "8587a2502cf4f5fa371a04eaca3eec4d782ad52d0a12f346606ee2ffd4b3ec02"
    },
    {
      "relative_path": "experiment_v013/artifacts/candidate.md",
      "byte_count": 4537,
      "sha256": "50ad937e5aa6df51e76223ef002a675273902a59d71170082d05c222db61fff5"
    },
    {
      "relative_path": "experiment_v013/artifacts/config.json",
      "byte_count": 2668,
      "sha256": "6fb1fcdad39ab7d3080900fc0ef1c47f998456abb9a895d4961e1cb04bd8e7ba"
    },
    {
      "relative_path": "experiment_v013/artifacts/dev_audit_001_execution.json",
      "byte_count": 3509,
      "sha256": "7a8917d7b5e1e20d9bdbb31a5ec2a0da5fb4a4ed6851d9935c7f02ed511355a7"
    },
    {
      "relative_path": "experiment_v013/artifacts/dev_audit_001_report.json",
      "byte_count": 16081,
      "sha256": "e7b71ab8e2370df3d297214771f1a676e3bafe1ccca06c6600cbe01e2410233e"
    },
    {
      "relative_path": "experiment_v013/artifacts/dev_audit_001_stderr.bin",
      "byte_count": 0,
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    },
    {
      "relative_path": "experiment_v013/artifacts/dev_audit_001_stdout.bin",
      "byte_count": 156,
      "sha256": "d1cfa34a11c9af09e330592538fb97800362af799b24ba49b20a0f87d6d718ea"
    },
    {
      "relative_path": "experiment_v013/artifacts/dev_eval_001_bor_dqn_seed123.pt",
      "byte_count": 22389,
      "sha256": "5c8127b653aca1c121f13c45edace4c05bff21c8dcc2653267fcbbabf98839fa"
    },
    {
      "relative_path": "experiment_v013/artifacts/dev_eval_001_bor_dqn_seed42.pt",
      "byte_count": 22377,
      "sha256": "758d3f676681c26a44a81cf9c277cc4ef994c4df777d597082c4034e13584040"
    },
    {
      "relative_path": "experiment_v013/artifacts/dev_eval_001_bor_dqn_seed456.pt",
      "byte_count": 22389,
      "sha256": "ac03e80ef745fd443dc55c33b9bd2bc7be7d3a31782f87a3681631e80bde7ae9"
    },
    {
      "relative_path": "experiment_v013/artifacts/dev_eval_001_execution.json",
      "byte_count": 5506,
      "sha256": "e57ba013b6edcbf46940eadf961dbdb7e3f8cb7aef48e637000c75a4cd16ac17"
    },
    {
      "relative_path": "experiment_v013/artifacts/dev_eval_001_f1_dqn_seed123.pt",
      "byte_count": 22377,
      "sha256": "56f7473f4b4bcef3ac0f3d2634b8cabcd6ae9b8678bcc4699d6f3280957ab8bc"
    },
    {
      "relative_path": "experiment_v013/artifacts/dev_eval_001_f1_dqn_seed42.pt",
      "byte_count": 22365,
      "sha256": "a1f0503413f34cead846920b5d9fec65b07b376a204aebff17136838241056ba"
    },
    {
      "relative_path": "experiment_v013/artifacts/dev_eval_001_f1_dqn_seed456.pt",
      "byte_count": 22377,
      "sha256": "7ce456bc99c7c07afedd4b6094faf9ec4a34c25ec6da17fb3aa20724813062f5"
    },
    {
      "relative_path": "experiment_v013/artifacts/dev_eval_001_raw_rows.jsonl",
      "byte_count": 266191,
      "sha256": "64046fe59ae1706975830585d48896d689c31807d6139d153f7f18f91c598a68"
    },
    {
      "relative_path": "experiment_v013/artifacts/dev_eval_001_split_manifest.json",
      "byte_count": 7191,
      "sha256": "016b0d09c1fc0fb8b599b55c120d07ad6983e518922c3e75f93122ed92f2a107"
    },
    {
      "relative_path": "experiment_v013/artifacts/dev_eval_001_stderr.bin",
      "byte_count": 0,
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    },
    {
      "relative_path": "experiment_v013/artifacts/dev_eval_001_stdout.bin",
      "byte_count": 1011,
      "sha256": "5d6eff7957cf37c6bf2d126746d1e2d6d08905c2834b21f5bd492af94005fe09"
    },
    {
      "relative_path": "experiment_v013/artifacts/dev_eval_001_summary.json",
      "byte_count": 43381,
      "sha256": "a1fc5202dbc462a935181ddec2a3b1746af4d7985edfecafeb27aebb4b7cba7f"
    },
    {
      "relative_path": "experiment_v013/artifacts/evidence_packet.md",
      "byte_count": 5972,
      "sha256": "1e8563b6eccb27dacef35f2c0b277b80c1742ce2ebc2ad83984053a59cb3c96e"
    },
    {
      "relative_path": "experiment_v013/artifacts/implementation_audit.md",
      "byte_count": 5075,
      "sha256": "06b701b044ae64fe3b2441d6041b779a287ad1443da6496bfa3d72de10ce27da"
    },
    {
      "relative_path": "experiment_v013/artifacts/nearest_prior.md",
      "byte_count": 4000,
      "sha256": "20e62887dcc3c88622d4388e86f3b9da1a9c1c70c34fa1e0572afc779bf83cb3"
    },
    {
      "relative_path": "experiment_v013/artifacts/official_bor_audit.py",
      "byte_count": 5569,
      "sha256": "3da2d063ccd78242686f54d3fdcd2e89a1e318ba20c6dad4261f64552a8645c8"
    },
    {
      "relative_path": "experiment_v013/artifacts/official_bor_metrics.py",
      "byte_count": 3119,
      "sha256": "5d1e282b72b267314c8da83b3fba192d40fdd97a7fdb8d9d69943eac34f6724d"
    },
    {
      "relative_path": "experiment_v013/artifacts/problem.md",
      "byte_count": 3506,
      "sha256": "1f5fc32fcf8632126173c57283e0a76d3567047ba248bc45fc8162976106875b"
    },
    {
      "relative_path": "experiment_v013/artifacts/program_audit.py",
      "byte_count": 28357,
      "sha256": "ea92265abf4b6d2fe8b6838f424b17e383f8361c0fc65658fe25fcc96b82f9e8"
    },
    {
      "relative_path": "experiment_v013/artifacts/program_independent_audit.py",
      "byte_count": 16076,
      "sha256": "990a33893a98af7c4996d89a754cb67861729840e729c8a424e382ca3e1212de"
    },
    {
      "relative_path": "experiment_v013/artifacts/promotion_audit.md",
      "byte_count": 6736,
      "sha256": "11f3af78c52ff9eeb7aaae8147550b545a86d8a0fba32d317f00e48bcfe14b26"
    },
    {
      "relative_path": "experiment_v013/artifacts/rank_bm25-0.2.2-py3-none-any.whl",
      "byte_count": 8584,
      "sha256": "7bd4a95571adadfc271746fa146a4bcfd89c0cf731e49c3d1ad863290adbe8ae"
    },
    {
      "relative_path": "experiment_v013/artifacts/research_map.md",
      "byte_count": 8248,
      "sha256": "23c0e7d4e3e183a7f38563d9377c69b3712fb0fb309df3a5a870c5fba6f556f5"
    },
    {
      "relative_path": "experiment_v013/artifacts/selection_context.md",
      "byte_count": 7770,
      "sha256": "0d32ea2d3f55b5ccb05bbc0b7a03cfe04e30d3106f809a9b697d9fa20436d5f7"
    },
    {
      "relative_path": "experiment_v013/artifacts/target_notebook_01.ipynb",
      "byte_count": 171036,
      "sha256": "61da53127597d7a90a440a87ff2efcea77665454852d50552df9bb2972a6ff81"
    },
    {
      "relative_path": "experiment_v013/artifacts/target_notebook_02.ipynb",
      "byte_count": 374908,
      "sha256": "35c2cb2b624c0d364f196a3db7493f0c7502af120228410673a587460b2d85c3"
    },
    {
      "relative_path": "experiment_v013/artifacts/target_paper.pdf",
      "byte_count": 400683,
      "sha256": "4db89bfac79bc90dd5b532d04ac1012ed1691657a45379bbbb2312682847164c"
    },
    {
      "relative_path": "experiment_v013/artifacts/target_results_bm25.json",
      "byte_count": 241402,
      "sha256": "8872db7f8528560419ab74aae8d1f268c193aece3e670cc11f96b15c336efb93"
    },
    {
      "relative_path": "experiment_v013/artifacts/test_metric_logic.py",
      "byte_count": 1381,
      "sha256": "9ae5104a273c9045c33b7e420b5dfa5444e7c289911c7cfae1d78d6a6ec78cfd"
    }
  ]
}
```

## Codex Interpretation

# v013 Development result ? not promoted

The captured Development execution exited 0 after 668.1302038999984 seconds and wrote 1,440 raw rows, a 280/120 frozen split, six DQN state dictionaries, and the summary. The independent audit exited 0 after 2.8199131000001216 seconds. Both stderr captures are empty.

The main Codex independently reread the raw rows. Each of 12 policy/seed groups contains exactly 120 unique test query IDs, all groups equal the split manifest test set, train/test overlap is zero, hit/depth errors are zero, and the maximum stored reward error is 1.509903313490213e-14. The independent report's 12 count errors arise because summary.json mislabeled the total 400 parsed inputs as query_count while the frozen policy evaluation correctly uses 120 test queries. That metadata defect is preserved; no output was repaired or rerun.

The central metric discrepancy is real in the frozen rows. FK3 minus FK1 is +0.32253264219641586 under the notebook statistic but -1.2002986504858315 under paper-defined BoR. The notebook statistic selects a learned DQN policy for all three seeds, while defined BoR selects FK1 for all three seeds. There are 27 strict pairwise reversals, 21 involving a learned policy, across seeds 42, 123, and 456.

Development nevertheless fails two conjunctive preregistered gates. BoR-DQN mean K is 9.738888888888889 versus the fixed official 7.4, an absolute delta of 2.3388888888888886 above the 1.0 tolerance. The coupled bootstrap supports positive FK3-minus-FK1 under the notebook statistic with probability 0.86415, below 0.95; its 95% interval is [-0.22796335969107417, 0.9177074479095237]. Defined-BoR negative support is 1.0 with interval [-1.3479233034203064, -1.023083613113041].

The main Codex therefore sets MAIN_CODEX_PROMOTION_AUTHORIZED to false. Confirmation was not acquired or read. No Review Packet, Reviewer, Decision, or Delivery is authorized. v013 freezes as a Development-screen failure. Thresholds, pair selection, tolerances, metadata, and seeds will not be retuned; the same Run advances to a scientifically different v014.
