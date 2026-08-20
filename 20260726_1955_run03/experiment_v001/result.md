# Experiment Result

```json
{
  "experiment_id": "v001",
  "execution_provenance": "caller_recorded",
  "plan_sha256": "e53f64759163dd80c584e62c293fd08533865be7b07037903c2dcfa33d84d3de",
  "candidate_sha256": "42e017c7f32e9d3fc2efda86080504456ab608f6523d07902993a8916455bb62",
  "evidence_packet_sha256": "181646a9882a7daea2cc583addebd95a70419c27e57463ff5877fb7b7ef536b8",
  "execution": {
    "command": "crl_agent_v3/.venv/python.exe tools/run_local_experiment.py --capture-dir experiment_v001/captures/dev_001 --cwd implementation_v001 --input experiment_v001/artifacts/{config.json,run_promotion.py,tp_solve_probe.py} --input data_split_commitment_v001/{bucket_D.csv,bucket_D_ref_info.jsonl} --output experiment_v001/work/dev_001/{results.jsonl,deepseek_raw.jsonl} -- crl_agent_v3/.venv/python.exe experiment_v001/artifacts/run_promotion.py experiment_v001/artifacts/config.json",
    "cwd": "D:\\Desktop\\crl\\20260726_1955_run03\\implementation_v001",
    "exit_code": 0,
    "stdout": "(captured verbatim in artifact stdout.bin, sha 885eedf8...)",
    "stderr": "(empty; sha e3b0c442...)",
    "environment": {
      "api": "deepseek-chat via https://api.deepseek.com/chat/completions; response model deepseek-v4-flash per-row; key via process env only",
      "orchestrator_python": "D:\\Desktop\\crl\\crl_agent_v3\\.venv\\python.exe (3.11.15)",
      "solver_python": "D:\\Desktop\\crl\\20260726_1955_run03\\.venv_z3\\python.exe (3.11.15, z3-solver 4.15.4)",
      "torch": "not used"
    }
  },
  "artifacts": [
    {
      "relative_path": "experiment_v001/artifacts/execution.json",
      "byte_count": 2966,
      "sha256": "5191ec68309e2a339be86d6ac0004a97ee941d9679cac56d020ae695754a59c2"
    },
    {
      "relative_path": "experiment_v001/artifacts/stdout.bin",
      "byte_count": 1058,
      "sha256": "885eedf827aedf8ccc7172cc185b508ab15cd696d04fb40d2a58b59c941b0cc5"
    },
    {
      "relative_path": "experiment_v001/artifacts/stderr.bin",
      "byte_count": 0,
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    },
    {
      "relative_path": "experiment_v001/artifacts/metric_audit_001_execution.json",
      "byte_count": 2267,
      "sha256": "2141d28c92a2c5220c0a4cc39384a2c30386f8a44933b0896281b3f3b7b5413b"
    },
    {
      "relative_path": "experiment_v001/artifacts/metric_audit_001_stdout.bin",
      "byte_count": 286,
      "sha256": "4d81df66c85413d1c6004a77080c38526d72625a0d11fbcd17f50dbf5a2f4e5e"
    },
    {
      "relative_path": "experiment_v001/artifacts/metric_audit_001_stderr.bin",
      "byte_count": 0,
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    },
    {
      "relative_path": "experiment_v001/artifacts/output_results.jsonl",
      "byte_count": 61964,
      "sha256": "c63d084b0ebe98227e5379e62dc4ab7f0a27c193386ca3eb87a40d7684df8f43"
    },
    {
      "relative_path": "experiment_v001/artifacts/output_deepseek_raw.jsonl",
      "byte_count": 267271,
      "sha256": "aa6ebf9dd835ab0d2ea25eed13794e4c45b832900c16555beba1ff490a1d9d78"
    },
    {
      "relative_path": "experiment_v001/artifacts/output_analysis_out.json",
      "byte_count": 2425,
      "sha256": "168235fc99645662cf34f25cf7634da7e8f84507e85e041f94d13a1341ab2514"
    },
    {
      "relative_path": "experiment_v001/artifacts/output_instance_files.zip",
      "byte_count": 243231,
      "sha256": "42d5b3430d0bf25ae5bff9aa01aa1baef91e7844b1554e30e2b015427daa13e7"
    }
  ]
}
```

## Codex Interpretation

Promotion Development dev_001（D 桶全部 28 个 SC3 实例，单段完整捕获，exit 0）+ metric_audit_001（analysis.py 独立重算捕获）。全部指标可从 output_deepseek_raw.jsonl 与 output_instance_files.zip 内的逐实例 probe_result 重算。

主结果（F1 自由形式，deepseek-chat，响应 model 逐行 = deepseek-v4-flash，温度 0）：
- 状态：23 ok / 1 formalization_error / 3 default_unsat / 1 default_unknown（z3 超时）。
- 解级认证 PASS：21/23。证书背书 enforcement 故障 3 例（witness 全部经 stdlib 检查器复核一致，all_witnesses_checker_confirmed=true）：
  - idx120 cuisine，masked（默认解通过全部检查）——查询列举四种菜系偏好，生成模型编码为逐餐厅成员归属而非菜系覆盖（与 Workbench idx064 同型的量词结构误译）；四菜系覆盖逐一可违；luck 采样 50/50 全部碰巧满足（λ=1.0）。
  - idx132、idx134 house_rule，caught（默认解即违规，被解级检查捕获）；λ=0.0。
- M2 掩盖率 = 1/21 = 4.8%，Wilson 95% CI [0.85%, 22.7%]。预注册 SIG-1（CI 下界 > 0）成立。
- 预注册 SIG-2 primary（masked λ 中位数 > 0.5）成立（λ=1.0；n_masked=1，样本量如实声明）。secondary luck 排序 masked(1.0)>caught(0.0) 成立；违规选项密度排序与预注册方向相反（masked 0.78 > caught 0.33）——域级密度是坏的 slack 代理，M 可行集内的 luck 指数才是机制变量；如实报告，不改指标。
- 检测器比较（M4，对 3 例证书背书故障）：A3 同模型自查（类别清单辅助）0/3 全部漏检、0/91 虚警——自信地把未编码约束报告为已编码（P052 自评失败的证书级再现）；A4 行为测试（合规选项消融/预算缩放）3/3 覆盖、0/68 虚警。A2 错误信号对 masked 格覆盖为 0 属构造性质。
- F2 一行类别清单 scaffold：26 ok / 26 PASS / 0 故障——最便宜的 scaffold 在本批完全关闭了静默通道（bundle 级观察）。
- W→D 衰减：Workbench 掩盖率 29%（4/14）→ D 桶 4.8%（1/21）。W 桶选择偏向 local-constraint 实例且含更多 cuisine 约束；掩盖质量对实例构成敏感，数值不外推。

环境与用量：编排 python 3.11.15（共享 .venv）；solver 载荷 .venv_z3（z3 4.15.4）；API 84 次调用，78,282 prompt + 46,484 completion tokens（约 0.03–0.06 USD 量级）；dev_001 wall ≈ 11.5 分钟。种子/随机性：温度 0；z3 默认确定性；luck 采样种子固定 20260726（selftest）/blocking 顺序确定。

结论边界：SIG-1 与 SIG-2 primary 按预注册出现；掩盖现象在 fresh 数据上以单实例、低单位数比例出现——证书是硬的（可行集 SAT witness + 检查器复核），但质量估计薄（n_masked=1），Claim 必须保持在 candidate_v001 契约内。C 桶未触碰。