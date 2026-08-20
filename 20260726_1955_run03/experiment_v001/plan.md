# Experiment Plan

```json
{
  "experiment_id": "v001",
  "candidate_sha256": "42e017c7f32e9d3fc2efda86080504456ab608f6523d07902993a8916455bb62",
  "evidence_packet_sha256": "181646a9882a7daea2cc583addebd95a70419c27e57463ff5877fb7b7ef536b8"
}
```

## Codex Plan

# Experiment Plan

## Frozen before results

本计划在 Promotion Development 数据（D 桶）被任何主流程代码打开之前冻结。绑定：
problem_v001（cae9ef65de842f69c839365a58c8ef88ec78ac6dd5d509de0a919e7ba9c9400d）、
research_map_v001（0db0eddaaff5702296eaae90dca6bcbbfcebaa9661d475a19428b0ddb096a742，含 pre-development Promotion Audit）、
candidate_v001（42e017c7f32e9d3fc2efda86080504456ab608f6523d07902993a8916455bb62）、
evidence_packet_v001（181646a9882a7daea2cc583addebd95a70419c27e57463ff5877fb7b7ef536b8）。

## Data roles, acquisition and sampling contract

- 来源：osunlp/TravelPlanner 验证集（validation.csv SHA 与 ref_info SHA 记录于 data_split_commitment_v001/MANIFEST.json，manifest SHA dfeaf9fe4688f9388576c6fbd36960eb095d1262bd8e2cf7e4c078551776dc7e）。
- 预承诺划分（commit-reveal + 物理分离）：规则 `int(sha256("run03_tp_val_{i:03d}").hexdigest(),16) % 5`，{0,1}=W(67)、{2,3}=D(80)、{4}=C(33)，i 为原始行索引；三桶写为独立文件并分别记录 SHA；承诺发生在读取任何实例内容或 outcome 之前（RUN_LEDGER 2026-07-26T20:52 事件）。接收方可重跑 commit_split.py 独立验证。
- WORKBENCH = W 桶（kernel 探针与 harness 设计已消费其 22 个 SC3 实例 outcome）。
- PROMOTION_DEVELOPMENT = D 桶全部 SC3 实例（days=3 ∧ visiting_city_number=1 的规范化通过者；机械元数据计数预期 28：easy 10 / medium 9 / hard 9，其中 18 个含 local constraint）。纳入规则固定为 tp_lib.normalize_sc3 非 None；无抽样、无随机种子（全量）；规范化失败实例如实计数报告。
- CONFIRMATION = C 桶全部 SC3 实例（同一确定性规范化定义总体；C 桶文件自承诺起完全未打开——包括元数据；预期规模按 W+D 的 SC3 占比外推 ≈12，实际由接收方执行时确定）。保留 outcome 在交付前不得以任何方式读取；未触碰证明 = 承诺清单 + 物理分桶 + 主流程代码只引用 W/D 路径（可由冻结 config.json 与全部 capture 的 inputs 哈希核验）。
- 缺失/失败处理：API call_failed 实例保留在 results 中如实报告，不重试超出 tp_api 内置 4 次退避；formalization_error / default_unsat 是数据（A2 错误信号），不剔除。

## Primary metric and mechanism signature

- **M2（主指标）**：F1 自由形式条件下，解级认证 PASS 实例中含 ≥1 证书背书未 enforce 适用类别的比例；Wilson 95% CI。
- M1：逐类别 enforcement 故障计数（证书背书 = 探针 SAT 且 witness 经 stdlib 检查器复核违规）。
- M4：检测器比较——A3（同模型 self-check，类别清单辅助）与 A4（行为测试）对证书背书故障的覆盖/漏检/不可用与虚警（对探针 UNSAT 类别）；A2（错误信号）对掩盖格覆盖为 0 属构造性质，只作分类学报告，不作为经验发现。
- M5：slack 机制——luck 指数 λ（blocking-clause 采样 k=50 中满足参考条件的比例）、违规选项密度、掩盖预算故障的 margin 分布。
- **预注册 mechanism signature（种子交付需两者都出现）**：
  - SIG-1：M2 的 Wilson 95% CI 下界 > 0。
  - SIG-2：masked 案例 λ 中位数 > 0.5（primary）；若 caught 案例 n≥2，另报告 λ(masked) > λ(caught) 与密度排序（secondary，方向性）。
- F2（清单 scaffold）对照与 A3/A4 结论为 bundle 内观察，不得归因为独立方法贡献。

## Closest-composition, neutral comparators and delta ablation

外部无可运行竞争分解（nearest_prior_v001，absence-of-evidence，2026-07-26）。内部臂矩阵在同一批冻结 F1 形式化产物上运行：A1 解级认证（被审计信号）、A2 错误信号集合、A3 同模型 self-check（有利变体：给类别清单）、A4 ReLoop-CPT 载体内改编（预算缩放 + 合规选项消融）、A5 enforcement 探针（唯一 delta）。探针不改动生成侧，F1 产物全臂共享——delta 归因由设计保证。A4 改编忠实性限制已在 candidate_v001 预先声明。

## Same-model/data/tool-budget controls

- 同模型：deepseek-chat（温度 0）承担 F1/F2/A3；逐行记录响应 model 字段；F1→F2→A3 逐实例交错执行（漂移控制）。
- 同数据：全部臂读取同一冻结实例文件与同一 F1 代码文件。
- 预算：A2/A4/A5 零 LLM 调用；A3 每实例 1 次调用（作为 comparator 的信息访问差异如实披露：A3 读 F1 源码，A5 读其语义（执行后的断言集），二者信息面等价级）。

## Capture and Artifact bindings

- 冻结 implement/config/input（experiment_v001/artifacts/，SHA 见下）：tp_lib.py 74c21af7…、tp_prompt.py 6e89a8ac…、tp_api.py 05388a7b…、tp_solve_probe.py 1757291f…、run_promotion.py fdfbbc53…、analysis.py 6ab2b874…、config.json 71657f07…、config_readiness.json a68fa89c…、input_bucket_D.csv 3298b92a…、input_bucket_D_ref_info.jsonl 24eb1337…、input_split_manifest.json dfeaf9fe…。
- capture：experiment_v001/captures/dev_001/（execution.json、stdout.bin、stderr.bin 原名保留）。
- 声明输出：experiment_v001/work/dev_001/results.jsonl（逐实例逐臂汇总，逐行 checkpoint）、experiment_v001/work/dev_001/deepseek_raw.jsonl（原始 API 响应逐行：request_id、endpoint、requested/response model、usage、时间戳、完整 body）。逐实例 probe 明细在 work/dev_001/idxNNN/（instance.json、F1/F2 代码与响应、probe_result.json、A3 响应）。
- 外部 API 纪律：raw jsonl 逐行 provenance；F1/F2/A3 逐实例交错；限流/中断按 tp_api 退避后如实记录 call_failed；续跑段使用新 attempt ID（dev_002…），分段边界与各段 model version 在 result.md 披露；不补造单一 canonical capture。
- 分析：analysis.py 从冻结 raw 独立重算全部指标（metric_audit attempt 另行 capture）。

## Exception environment record（z3）

- 实证冲突：共享主环境验收命令逐行比对 pip freeze 与 CRL_ENVIRONMENT_LOCK.txt；安装 z3-solver 必致该检查失败，而 lock 刷新需用户明确批准（CRL_ENVIRONMENT.md）。故按具体实验例外环境条款建立。
- 规格：`D:\Desktop\crl\20260726_1955_run03\.venv_z3`；conda create python=3.11.15 + pip；`pip install z3-solver==4.15.4`；创建命令与验证见 RUN_LEDGER 2026-07-26T21:05 事件。用途仅限本 Run 的 solver 侧载荷（tp_solve_probe.py）；不升级为默认环境；Run 关闭后保留（供接收方复现 C 桶计划）。
- 快照：python 3.11.15；z3-solver 4.15.4（`z3.get_version_string()` = 4.15.4，sat 冒烟通过）。

## Exact execution readiness（2026-07-26 实测回报）

- 解释器：捕获器与编排器 = D:\Desktop\crl\crl_agent_v3\.venv\python.exe（3.11.15）；solver 载荷 = D:\Desktop\crl\20260726_1955_run03\.venv_z3\python.exe（3.11.15 + z3 4.15.4）。cwd = D:\Desktop\crl\20260726_1955_run03\implementation_v001。
- import 与 exact loader：冻结 artifacts 目录内 tp_lib/tp_api/tp_prompt/run_promotion 全部 import 成功（冒烟实测）。
- synthetic/近真实 smoke：W 桶实例 idx001 走完整冻结链路（F1+F2+A3 三次真实 API 调用、响应 model deepseek-v4-flash、z3 默认解+探针+行为测试全部执行、exit 0）——payload 形态（真实 query 长度、真实候选表、真实生成参数 max_tokens=4000/温度 0）与正式实验一致；未读取任何 D outcome。probe-checker 一致性 selftest：200 随机赋值 × 全类别 0 不一致。
- secret 脱敏：readiness 全部输出与 capture 前扫描 `sk-[A-Za-z0-9]{8,}` 零命中；tp_api.redact 覆盖异常与 stderr 通道；key 仅存在于进程环境变量，argv 无 key。
- capture/output parent：experiment_v001/captures/ 与 experiment_v001/work/ 已存在；capture 目录 dev_001 与声明输出 results.jsonl、deepseek_raw.jsonl 在启动前不存在（启动脚本前置断言）。
- 当前 SHA：见 Frozen before results 与 Capture bindings 节。
- 无未解析占位内容；前台参数数组调用（PowerShell 数组 + `--` 分隔）；readiness 不产生科研指标。

## Preregistered confirmation isolation and cluster-aware analysis

- 隔离单位：实例（instance-disjoint，承诺哈希分桶）。聚类单位：实例（同实例多类别判定相关；主指标 M2 在实例级）。
- Promotion 触碰的单位：D 桶 SC3 实例的 query/候选表/生成 outcome。W 桶已在 Workbench 触碰。C 桶零触碰。
- **移交接收方的预注册 Confirmation Plan（冻结后不因 Development 结果回改）**：
  1. 载体：C 桶（bucket_C.csv + bucket_C_ref_info.jsonl，SHA 见承诺清单）全部 SC3 实例（tp_lib.normalize_sc3 非 None）。
  2. 执行：与 dev_001 完全相同的冻结 artifacts（run_promotion.py + config 的 C 变体，仅改 bucket 与 out_dir；z3 例外环境同一路径）；执行前核对响应 model 字段与 dev_001 记录（deepseek-v4-flash）是否一致，不一致即为已知混杂如实披露。
  3. 预注册闸门：**C-GATE-1** —— C 桶 F1 认证 PASS 实例中证书背书掩盖实例 ≥2 且 Wilson 95% CI 下界 > 0；**C-GATE-2** —— C 桶 masked 案例 λ 中位数 > 0.5。两门独立报告，不合并投票。
  4. 全部指标由 analysis.py 从 raw 重算；witness 检查器复核不一致即整批无效。

## Cost and bundle-level attribution

预计 API：28 实例 ×3 调用 ≈ 84 调用（+重试），token 预计 12–20 万，费用 <0.1 USD 量级（deepseek 定价），实际用量在 result.md 披露。本地计算：z3 探针/采样/行为测试，单实例秒级—分钟级，总 wall time 预计 ≤2 小时。无法通过消融归因单一组件的结论（F2、A3 设计选择）保持 bundle-level。

## Leakage, oracle and fixture checks

- 无答案 oracle：探针与检查器只用实例候选表属性与查询注释（local_constraint 金标注仅用于评测侧适用性判定与检查器，不进入被试 runtime data——泄漏检查点：runtime_data() 白名单字段）。
- A3 不接收探针输出或检查器结论；A4 不读取 A5 结果。
- fixture 检查：readiness smoke 与 selftest 是 readiness/sanity，不进入 Promotion 证据。
- 模型漂移：逐行 model 字段 + 逐实例交错。

## Direct falsification conditions

- SIG-1 失败（CI 下界 = 0）→ Claim 1 否证，版本负面关闭。
- SIG-2 primary 失败 → 机制部分降级，交付价值由主 Codex 重新裁量并如实写入 decision。
- 任一 witness 检查器复核不一致 → harness 缺陷，实验无效，修复推进新版本。
- D 桶 PASS 样本 <8 → 外部有效性受限，如实报告并裁量。
