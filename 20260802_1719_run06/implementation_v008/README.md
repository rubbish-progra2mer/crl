# v008 实现说明：表示同质、全量观察审计与响应承诺

本目录实现结构化列表连接器上的联合范围证据协议。v008 修复 v007 的三个核心缺口：表示版本检查仍晚于原始单元路由、未带证明观察被摘要前过滤、响应记录及分页语义没有可核对承诺。

## 文件

- `joint_coverage_kernel.py`：生产求值器、数据模型、规范请求/响应承诺、页链、证书生成与验证入口。
- `independent_certificate_verifier.py`：不调用生产求值器的第二验证路径，独立重算规范编码、响应承诺、全局预检和证书模式 8。
- `run_soundness_counterexamples.py`：180 个具有独立预期的声音性攻击案例。
- `test_joint_coverage_kernel.py`：55 项单元、变形与证书重放测试。
- `run_kernel_tests.py`：结构化测试运行器。
- `run_joint_coverage_experiment.py`：756 个任务、5 个预算、7 种方法的主回归；输出逐方法审计表和独立诊断面板标记。
- `compare_v007_v008_regression.py`：比较 v007 观察字段投影、配置和 13 个原有行为字段。
- `run_real_connector_response_attestation.py`：获取 GitLab 与 Crossref 公开响应，保存原始字节，用生产/审计投影分别解码并执行 8 个承诺变异。

## 批次预检顺序

`evaluate_claim` 对实际传入的每个 `Observation` 执行以下顺序：

1. 观察摘要进入全局收到观察多重集；
2. `attested` 必须为真，否则记录全局冲突；
3. `response_commitment` 必须存在且等于从规范请求、有序记录、下一游标、状态、权限完整性、静默截断标志重算的值；
4. 规范请求载荷必须可解析；外层来源键等于载荷来源键；每条记录的原始单元等于载荷请求单元；
5. 观察的范围模式、适配器、语义规范化和请求序列化版本必须全部等于主张表示元组；
6. 只有上述全局门通过，才允许按连接器、查询签名、鉴权主体、快照和原始单元作语义路由及页链求值。

任一全局冲突使当前主张 `UNKNOWN`。步骤 5 故意位于所有语义坐标之前，用于关闭不同范围模式将同一语义单元编码为 B1/B2 的绕过。它也会让真正异源但版本不同的观察污染当前主张，这是明确的可用性代价。

## 响应承诺与观察摘要

`canonical_response_commitment` 规范绑定：

- 模式版本；
- 规范请求载荷摘要；
- 原始顺序的完整记录列表，每条记录含 `id`、`cell`、`matches`、`compliant`；
- `next_cursor`、`status`、`permission_complete`、`silently_truncated`。

`Observation.pre_attestation_digest` 精确投影为 v007 的观察摘要字段。v008 `Observation.digest` 再绑定该投影摘要与 `response_commitment`。因此 v007/v008 可公平比较旧字段投影，同时完整 v008 证书不能忽略新增承诺。

承诺不是来源真实性本身。生产部署必须由可信采集/验证边界提供已经核验的 `attested=true` 和响应承诺；若调用者可同时伪造观察与承诺，本内核只能验证自洽性。

## 页链与证书模式 8

通过预检的观察按完整来源身份、声明快照和联合单元形成页链。每个游标只能有一个一致页面；不透明游标通过显式后继关系闭合，循环、缺页、权限不完整或静默截断均不能形成完整负证据。

存在量词的阳性记录和全称量词的反例记录可形成见证。否定存在或肯定全称必须覆盖精确联合范围的全部来源绑定页链。

证书模式 8、请求绑定 `homogeneous-attested-response-commitment-v5` 绑定：主张、决定、证明类型、页链或见证、全部收到观察的全局审计摘要、新观察摘要及配置。独立验证器有自己的规范 JSON 与 SHA-256 实现路径，不导入生产求值函数。

## 运行

在本目录用 Run 的 Python 环境可执行非正式复核：

```powershell
D:\Desktop\crl\crl_agent_v3\.venv\python.exe run_kernel_tests.py --output ..\workbench_v008\kernel-tests-local.json
D:\Desktop\crl\crl_agent_v3\.venv\python.exe run_soundness_counterexamples.py --output ..\workbench_v008\soundness-local.json
```

真实连接器脚本会访问公开网络并保存原始响应，只应用于明确的实验目录：

```powershell
D:\Desktop\crl\crl_agent_v3\.venv\python.exe run_real_connector_response_attestation.py --output-dir ..\workbench_v008\real-connector-local
```

正式证据不得由上述直接命令替代；本 Run 的正式结果均位于 `experiment_v008/attempts/`，并由 Harness 记录实现字节、输入、输出、命令、环境和宿主时长。

## 正式结果入口

- `homogeneous-attested-counterexamples-v008`：180/180，错误认证提交 0。
- `kernel-tests-55-v008`：55/55。
- `homogeneous-attested-joint-coverage-756x5-v008`：26,460 回合，17,445 个回答全正确；联合覆盖证书 3,780/3,780 有效。
- `v007-v008-projected-clean-regression-v008`：投影输入、配置和 13 个行为字段差异均为 0；时长比 1.017。
- `real-connector-response-attestation-v008`：2 个公开端点，2/2 双投影记录序列相等，2/2 承诺可重算，8/8 变异被检测。

详细分母、SHA-256 和信任边界见 `experiment_v008/result.md`。

## 已知边界

- 只承诺实际传入内核的观察；采集前省略仍未解决。
- `attested` 必须由外部可信边界验证，布尔值本身不是密码学证明。
- 响应承诺检测给定承诺后的不一致，不证明提供方事实正确。
- 当前策略拒绝混合表示，尚未实现安全跨版本语义规范化。
- 三个规划/联合方法共享执行器，不是独立系统基线。
- 真实连接器实验是单页、同进程双投影，不是透明日志或端到端负主张认证。
