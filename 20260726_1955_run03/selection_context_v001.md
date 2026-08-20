# Neutral Selection Context

RUN_ID: 20260726_1955_run03。截至 v001 的完整选择集合与数据触碰记录（中性陈述，无 prior 排名、无最近先行结论）。

## Kernels 与 disposition

- K1：逐约束 enforcement 探针与掩盖率分解（认证侧测量 harness）。disposition = keep → 冻结为 candidate_v001。生成通道与理由见 research_map_v001。
- K2：探针触发的静默修复环。disposition = kill（本版本）——依赖 K1 未验证跃迁、且与 K1 同版本推进将构成第二条独立科学跃迁；修复环节点由外部工作密集占用（中性事实：见 research_map_v001 的新颖性探针记录）。
- 本版本无其他被考虑后放弃的 kernel；Problem 级选择过程（11 轮占用度扫描、9 个被排除的失败空间）记录于 problem_v001 占用度扫描节。

## Candidate / Claim 版本

- candidate_v001（SHA 42e017c7f32e9d3fc2efda86080504456ab608f6523d07902993a8916455bb62）：唯一 Claim 契约见其 Minimal Claim Contract；无先前版本、无 Claim 收缩/扩张历史。

## 数据触碰与角色

- 预承诺分桶（data_split_commitment_v001/MANIFEST.json，SHA dfeaf9fe4688f9388576c6fbd36960eb095d1262bd8e2cf7e4c078551776dc7e）先于任何实例内容读取。
- W 桶（WORKBENCH，67 行）：22 个 SC3 实例的完整 outcome 在 Workbench 决定性探针中被读取（workbench_v001/）；另 1 个 W 实例（idx001）用于 readiness 冒烟。W 桶 outcome 参与了 harness/prompt 设计与 kernel 存活判断。
- D 桶（PROMOTION_DEVELOPMENT，80 行）：候选形成期间仅做机械元数据计数（level/days/cities 列直方图，预期 SC3=28）；outcome 在 plan.md 冻结后的 dev_001 捕获执行中首次读取。
- C 桶（CONFIRMATION，33 行）：完全未打开（含元数据），保留 untouched，随 Delivery 移交。

## 实验尝试

- workbench_v001 falsifier（W 桶 22 实例，2026-07-26）：结果性质 = kernel 授权继续（掩盖质量非零）；不作晋级证据。
- experiment_v001 readiness（selftest + W idx001 冒烟）：readiness/sanity 性质。
- experiment_v001 dev_001（D 桶 SC3 全量 28 实例，plan.md e53f6475 冻结后执行）：Promotion Development 唯一科学执行，单段完整 capture（无中断、无分段），exit 0；metric_audit_001 为 analysis.py 独立重算的第二个 capture attempt。结果见 experiment_v001/result.md 与冻结 artifacts。
- 无其他隐藏尝试；全部 API 调用逐行记录于 output_deepseek_raw.jsonl（84 调用）。attempt 清单：dev_001（科学执行）、metric_audit_001（指标重算）——无废弃或复用 attempt ID。

## Optional stopping 相关

本 Run 无先前版本；v001 是第一个候选版本。Workbench 探针一次通过（无多次探针择优）；dev_001 为单次执行（如遇中断分段将以 attempt manifest 披露）。

## 源路径 / SHA

- problem_v001.md：cae9ef65de842f69c839365a58c8ef88ec78ac6dd5d509de0a919e7ba9c9400d
- research_map_v001.md：5ba2f32e3a090393e6356cc6c30ccfa351c5be231dea8d45d203ef7f348b3940（含两阶段 Promotion Audit 与 Seed Readiness Audit；送审冻结时以 Packet manifest 为准）
- experiment_v001/result.md：422f4d34a08491b0719a7f1a063d8ab7d653154b9385af17f23c2ca035b7d416
- candidate_v001.md：42e017c7f32e9d3fc2efda86080504456ab608f6523d07902993a8916455bb62
- evidence_packet_v001.md：181646a9882a7daea2cc583addebd95a70419c27e57463ff5877fb7b7ef536b8
- experiment_v001/plan.md：e53f64759163dd80c584e62c293fd08533865be7b07037903c2dcfa33d84d3de
- 冻结实现工件 11 项：见 plan.md Capture bindings 节。
