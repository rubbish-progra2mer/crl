# CRL Fixed Review Packet

- Contract: 3
- Scientific version: v001
- Evaluator: CRL-EVAL-1.0
- Evaluator definition SHA-256: e0d35083b1427e9f8861ba576304b97657498fee46480d5e07e8e0b02cea6e5b
- Implementation key: 0424092c3d015458de5a2033cb9db7ac8bceeede66122a7ccba6bbf5b1062cff
- Implementation manifest SHA-256: 0424092c3d015458de5a2033cb9db7ac8bceeede66122a7ccba6bbf5b1062cff
- Evidence inventory SHA-256: 27d8674cd49bcf497d9864919ba7422aea85e0ee02f46c9e94c437f9db432b57

## 1. Implementation / Seed Overview

### Source: `seed_v001.md`

# 计划派生证据义务：面向开放世界工具故障的提交前最小读回

## 研究种子

工具智能体执行写操作后，成功回执可能对应空操作、部分写入、错误对象或重复作用。固定写工具契约能保守验证状态，却会检查当前计划并不需要的字段；基于已知故障分支的信息增益方法更便宜，但其确信依赖封闭分支模型。

本种子提出 Plan-Derived Evidence Obligations（计划派生证据义务，PDEO）：不先猜故障类型，而从下一项外部副作用或成功声明所需的状态前提开始，沿类型计划反向传播证据义务，删除可信确定性步骤已经建立的谓词，再在只读探针覆盖和成本上求最小集合。只有每个剩余义务都由真实环境读回满足，受保护承诺才可执行。

## 计算核

设受保护承诺需要原子谓词集合 (G)，其前面存在一段类型化计划动作。对动作从后向前处理：可信确定性效果若建立了 (G) 中的谓词则消解它，并加入该动作自身前提；外部不确定写入及其回执不能消解义务。得到写后检查点的义务闭包 (O) 后，在探针集合 (R) 上求：

\[
\arg\min_{S \subseteq R} \sum_{r\in S} c(r)
\quad \text{s.t.} \quad
\bigcup_{r\in S}\operatorname{cover}(r) \supseteq O.
\]

运行时只读取 (S)，并对 (O) 做闭集判断。任何缺失、不匹配或读取失败都停止提交；恢复是独立策略，不属于当前方法核。

与 DQBP 的实质差异是：PDEO 没有后状态分支、故障先验或决策风险目标。与固定工具契约的差异是：义务由当前计划的下游承诺产生，而非永久绑定到写工具。与全量读回的差异是：计划无关状态不进入覆盖目标。

## 最近工作定位

[ToolGate](https://aclanthology.org/2026.findings-acl.470/) 用预先给定的霍尔式前置/后置条件控制调用和状态提交；PDEO 的候选增量是从当前计划反向生成写后证据集合并按探针成本最小化。[VERIMAP](https://arxiv.org/abs/2510.17109) 在规划时为子任务生成自然语言或 Python 验证函数；PDEO 限于类型状态谓词上的确定传播和环境读回。[Verified Tool Calls](https://arxiv.org/abs/2608.02645) 已覆盖写后验证和重试前验证，因此“验证写操作”本身不是本种子的新颖点。

[Failing Tools](https://openreview.net/forum?id=j7YsSnA64D) 把必需动作表述为证据义务和轨迹状态安全不变量，但其基准约束由人工给定。[ETAS](https://arxiv.org/abs/2607.17780) 更系统地提供类型/效果语义、轨迹监控和动态资源残余义务；PDEO 若要形成独立论文贡献，必须证明运行时状态证据编译与最小探针选择不是 ETAS 的直接实例。[AgentCheck](https://arxiv.org/abs/2607.11098) 支持系统故障注入评价，但不是计划派生义务方法。

因此，当前只能主张一个有碰撞风险的窄方法增量，不能声称已经完成新颖性证明。

## 反证历史

首个候选 DQBP 在三个域、每域 10,000 个同分布 Scratch 样本上与状态信息增益都达到 1.000 成功率和 0 危险错误，但平均探针成本为 1.7703，对方为约 1.707；预设成功率优势为 0。该结果杀死了“决策取商自然优于状态信息增益”的方法核，也促使本种子放弃封闭故障分支。

## 正式证据

最终实现匹配的有效 Formal attempt `attempt-pdeo-formal-002` 在预约、访问控制和库存三个合成域上执行 171 个确定性案例：24 个原始分支、48 个系统性单义务替换、63 个安全无关字段替换和 36 个义务—无关字段配对替换。评价器以独立声明的安全规则生成标签，不调用 PDEO 编译器；执行 Schema 7、退出码 0、指标与输出契约均通过。较早的 001 运行数值完全一致，但实现文件身份清单未覆盖测试和辅助源码，因而保留为与最终实现不匹配的历史。

核心结果：

- 48 个单义务故障：PDEO 危险提交率 0；DQBP 为 0.5833，状态信息增益为 0.7500；
- 63 个安全无关变异：PDEO 提交召回率 1.000；DQBP 为 0.7460，状态信息增益为 0.9524；
- 同一义务故障分割平均探针成本：PDEO 3，写工具本地完整契约 5，全量读回 6；
- 人工最小义务同样是危险提交率 0、召回率 1、成本 3，说明编译器达到当前人工上界，但没有超越它。

指标文件哈希为 `c0bf6a60ead529de4eeb80e6881d378a44783e8d918597cfa0e61873cc962158`，执行记录哈希为 `65d6721da32c82b39c624c3cf7a752f7472f588f485494b25b2d3ed0e5aafad4`。

## 最小可证伪主张

在类型计划、工具效果和只读探针覆盖正确，且状态谓词离散、读回无噪声的三个受控域内，PDEO 能在系统性义务故障上保持零危险提交，对安全的计划无关变异保持完整提交召回，并以严格低于完整工具契约的探针成本实现这一性质。

该主张不扩展到自然语言计划生成、真实应用程序接口、并发、陈旧读、权限失败、带噪探针、恢复质量或端到端任务成功率。

## 替代解释与失败边界

最强替代解释是：正确类型计划已经包含了关键安全知识，PDEO 只是经典最弱前置条件与加权集合覆盖的直接组合。当前实验无法排除这一判断；它只证明该组合在给定闭集承诺语义下按设计工作。

其次，信息增益和 DQBP 的高危险提交率来自其封闭分支模型无法表示系统性变异。这是目标失败模式的一部分，但不是对所有自适应验证方法的普遍优势；允许开放集异常检测或把义务谓词加入其状态模型后，差距可能缩小。

写工具完整契约验证的是“工具是否完整履约”，PDEO 验证的是“当前承诺是否已有足够证据”。两者目标不同；工具审计、合规或未来未知计划仍可能需要完整契约。

## 扩大价值

若固定三审认为方法增量足够清晰，下一步最有价值的扩大不是增加更多同构合成域，而是：

1. 在真实模型上下文协议或应用程序接口任务中，由独立标注者给出承诺前提并注入非原子故障；
2. 加入陈旧、权限受限和带噪读回，研究义务在证据来源不可靠时的组合规则；
3. 与 ToolGate 完整契约、开放集故障检测及 ETAS 式残余义务做组件级实现比较；
4. 单独评价自然语言计划到类型义务的转换，避免把规格错误藏在控制器之外。

这颗种子的价值在于把“验证写工具”收窄成可计算、可反证的计划条件化证据闭包；是否达到 CCF-B 方法潜力，仍取决于最近工作碰撞和固定 Reviewer 对“直接形式方法移植”异议的判断。

## 2. Closest Prior Evidence

### Source: `nearest_prior_v001.md`

# 最近工作边界：计划派生证据义务

本文件记录当前检索能支持的边界，不宣称已经证明新颖性。

## 直接近邻

1. **ToolGate（Findings of ACL 2026）**：维护显式符号状态，用预先给定的霍尔式前置/后置条件决定工具能否调用及结果能否提交。PDEO 的差异候选是后置验证集合由当前计划的下游承诺反向生成，并按探针成本最小化；若 ToolGate 正文已经包含等价的计划条件化契约合成，则差异消失。
2. **VERIMAP / Verification-Aware Planning for Multi-Agent Systems（ICLR 2026 投稿）**：规划器在分解子任务时同时生成验证函数，并在失败后重规划。PDEO 不生成任意自然语言或 Python 验证函数，而在类型状态谓词上做确定的反向传播与最小证据覆盖；两者都属于验证感知规划，方法级重叠很强。
3. **Failing Tools（2026）**：把必需动作解释为证据义务、禁止动作解释为轨迹状态安全不变量，并要求写后读回。其约束由基准人工给定；PDEO 试图从类型计划计算当前承诺所需义务。术语和目标高度接近，必须避免把人工基准约束误报成方法空白。
4. **Verified Tool Calls Improve LLM Agent Reliability Under Non-Atomic Failures（2026）**：写后验证、重试前验证和幂等键的轻量包装器。PDEO 的剩余差异只可能是验证谓词的计划条件化生成与最小化，而不是“写后验证”本身。
5. **ETAS: An Effect-Typed Language for Agent Systems（2026）**：以类型/效果语义表示智能体、工具、策略和轨迹，对动态资源发出残余义务。它比 PDEO 更靠近编程语言与静态保证；PDEO 若不能证明自己在运行时探针选择上的独立计算与实证价值，就会被视为较弱实例。
6. **AgentCheck（2026）**：对模型上下文协议工具注入超时、陈旧数据等故障，并评价缓解策略。它强化了未见运行时故障的评价必要性，但不是计划条件化证据编译方法。

## 方法成立所需的最小差异

PDEO 必须同时满足：

- 义务来自下游承诺，而非人工为当前样本写入故障标签；
- 对计划无关的工具状态不做完整验证，成本低于完整工具契约；
- 不依赖封闭故障枚举，在未见故障上比 DQBP/信息增益更少危险提交；
- 类型计划错误、工具效果错误和探针覆盖缺失被明确列为保证边界。

缺少任一项时，当前候选将分别退化为固定后置条件、全量读回、已有分支探针或无法验证的形式化包装。

## 3. Core Experimental Evidence

### Source: `experiment_v001/result.md`

# PDEO 正式实验结果

## 执行身份

- 最终实现匹配 Attempt：`attempt-pdeo-formal-002`
- 状态：有效 Formal / Review-support attempt
- 执行 Schema：7
- 子进程退出码：0
- 指标契约：通过
- 输出契约：通过
- 模型调用：0
- 接口调用：0
- `execution.json`：`65d6721da32c82b39c624c3cf7a752f7472f588f485494b25b2d3ed0e5aafad4`
- `metrics.json`：`c0bf6a60ead529de4eeb80e6881d378a44783e8d918597cfa0e61873cc962158`
- `formal-details.json`：`b14893ee985a87d00c7f08ac26bb3c94c8b8c487d7eb81339567db25b52ced57`
- `spec.json`：`6ff4f1789dd4dabd4dfbaab3ac9018770f63aa9406ebcc7af35f4fea613eccfb`

预算上限在规格中以可读文本保存，因此运行器没有形成机器可比较的预算上限；实际探针成本、运行时、模型调用和接口调用均已进入冻结指标。这是记录边界，不改变下面的原始数值。

`attempt-pdeo-formal-001` 使用相同规格和案例，数值指标与 002 除墙钟时间外完全一致，但只绑定了运行所需的 6 个源码文件，未覆盖最终实现目录中的测试和辅助源码，因此在最终 Review Evidence Inventory 中应显示为 `MISMATCH`。002 扩展实现身份清单到全部 10 个源码文件，没有修改候选、规格、案例或指标定义。

## 主要结果

| 方法 | 系统性义务故障危险提交率（48 例） | 安全无关变异提交召回率（63 例） | 义务故障平均探针成本 |
|---|---:|---:|---:|
| 状态信息增益 | 0.7500 | 0.9524 | 1.6667 |
| DQBP | 0.5833 | 0.7460 | 1.6667 |
| PDEO | **0.0000** | **1.0000** | 3.0000 |
| 写工具本地完整契约 | 0.0000 | 0.2381 | 5.0000 |
| 全量读回 | 0.0000 | 1.0000 | 6.0000 |
| 人工最小义务 | 0.0000 | 1.0000 | 3.0000 |

补充事实：

- 24 个原始已知分支上，PDEO 门控准确率为 1.000；
- 36 个义务—无关字段配对故障上，PDEO 危险提交率为 0，门控准确率为 1.000；
- 固定目标读回在 48 个单义务故障上的危险提交率为 0.6667；
- 无验证和静态成功回执在同一分割上的危险提交率均为 1.000。

## 主研究者解释

实验支持一个窄机制结论：封闭分支模型可以用更少探针处理已知分支，但会把未在分支模型中的状态当成已有安全类；PDEO 不做故障识别，而是逐项关闭下游承诺的证据义务，因此对系统性义务替换保持闭集提交。

成本优势只相对于保守的完整工具契约和全量读回成立。PDEO 没有优于人工最小义务；这正是预期上界，也意味着方法贡献必须来自义务的计划派生，而不能来自一个新的探针最优性定理。

写工具本地完整契约在无关字段变异上的低召回，是因为其额外要求审计字段与工具完整成功状态一致。对“工具是否完整按契约执行”这一更强目标，它的拒绝可能合理；本实验只评价“是否足以安全执行当前受保护承诺”。因此不能把 PDEO 解释为整体替代完整事务审计。

## 未被回答的问题

- 类型计划和工具效果错误时没有保证；
- 真实只读探针可能陈旧、带噪或不可用；
- 当前精确集合覆盖只在很小探针目录上运行；
- 三个合成域共享结构，尚无真实代理基准结果；
- 未评价自然语言规格抽取、恢复质量或端到端任务成功率。

### Source: `experiment_v001/attempts/attempt-pdeo-formal-002/execution.json`

{
  "argv": [
    "D:\\Desktop\\crl\\env\\crl_agent_v3\\python.exe",
    "formal_pdeo_experiment.py",
    "--metrics-output",
    "D:\\Desktop\\crl\\20260813_1054_run09\\experiment_v001\\attempts\\attempt-pdeo-formal-002\\metrics-output.json",
    "--details-output",
    "D:\\Desktop\\crl\\20260813_1054_run09\\experiment_v001\\attempts\\attempt-pdeo-formal-002\\formal-details.json"
  ],
  "attempt_id": "attempt-pdeo-formal-002",
  "budget_facts": {
    "actual": {
      "api_calls": 0,
      "duration_seconds": 0.17656740000029458,
      "gpu_time_seconds": 0,
      "tokens": 0
    },
    "comparison": {
      "reason": "budget_ceiling is not a machine-readable JSON object",
      "status": "unavailable"
    },
    "machine_readable_limits": null,
    "spec_budget_ceiling": "确定性穷举；每例最多读取全部五个探针，总成本上限 6；自适应基线预算 3。",
    "warnings": []
  },
  "capture": {
    "stderr": {
      "path": "D:\\Desktop\\crl\\20260813_1054_run09\\experiment_v001\\attempts\\attempt-pdeo-formal-002\\stderr.bin",
      "redaction_applied": false,
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "size_bytes": 0
    },
    "stdout": {
      "path": "D:\\Desktop\\crl\\20260813_1054_run09\\experiment_v001\\attempts\\attempt-pdeo-formal-002\\stdout.bin",
      "redaction_applied": false,
      "sha256": "297296446461f45f9874ef157755df28e74f7d588a1dcdca682cd8d1ec2f8020",
      "size_bytes": 31003
    }
  },
  "command_error": null,
  "command_exit_code": 0,
  "cwd": "D:\\Desktop\\crl\\20260813_1054_run09\\implementation_v001",
  "duration_seconds": 0.17656740000029458,
  "environment_facts": {
    "cpu_count": 16,
    "declared_facts": {
      "dataset": "pdeo-systematic-171",
      "dataset_revision": "v1-exhaustive-state-vocabulary",
      "model": "deterministic-typed-plan-controller",
      "provider": "local-python-3.11"
    },
    "dependencies": {
      "snapshot": {
        "path": "D:\\Desktop\\crl\\20260813_1054_run09\\experiment_v001\\attempts\\attempt-pdeo-formal-002\\dependencies.txt",
        "sha256": "480ab3b94b0b3b95bb6ff16eb9c4e138b942a818e488d43f71f810c5fe2e143a",
        "size_bytes": 769
      },
      "source_path": "D:\\Desktop\\crl\\crl_agent_v3\\CRL_ENVIRONMENT_LOCK.txt",
      "source_type": "lock_file"
    },
    "executable": "D:\\Desktop\\crl\\env\\crl_agent_v3\\python.exe",
    "git": {
      "reason": "ValueError: command exited with code 128",
      "status": "unavailable"
    },
    "nvidia": {
      "cuda_version": "13.1",
      "gpus": [
        {
          "driver_version": "591.86",
          "index": "0",
          "memory_total_mib": "16311",
          "name": "NVIDIA GeForce RTX 5060 Ti"
        }
      ],
      "status": "available"
    },
    "platform": "Windows-10-10.0.26100-SP0",
    "python": "3.11.15 | packaged by Anaconda, Inc. | (main, Jun 11 2026, 15:12:53) [MSC v.1942 64 bit (AMD64)]",
    "runner_and_modules": [
      {
        "path": "tools/run_local_experiment.py",
        "sha256": "2a6007ec765584afc80e56f90efb168d2383962a49ee5e8ab5a84ccaa3509190",
        "size_bytes": 32062
      },
      {
        "path": "crl_v3/experiment.py",
        "sha256": "d92817fcfd085ad100aa34f97a95e653956d22ea63ee8527f4b657d6b16a39da",
        "size_bytes": 37547
      },
      {
        "path": "crl_v3/falsification.py",
        "sha256": "5a852d0df4101c5b240363559d0cc05a2f64c725574d999b999e92deba97b9b8",
        "size_bytes": 40435
      },
      {
        "path": "crl_v3/workspace.py",
        "sha256": "74b7b3837e62404cbe68a1bc3f12ce4764a13e042b96131a1bd3bfa00ef57be9",
        "size_bytes": 27543
      },
      {
        "path": "crl_v3/decision.py",
        "sha256": "dff699c46b6e5bde36d589ff19e6f66ef3a2ea2ae0b7ceb42247030203f6d9c9",
        "size_bytes": 37790
      }
    ]
  },
  "evidence_contract_ok": true,
  "experiment_spec": {
    "snapshot": {
      "path": "D:\\Desktop\\crl\\20260813_1054_run09\\experiment_v001\\attempts\\attempt-pdeo-formal-002\\spec.json",
      "sha256": "6ff4f1789dd4dabd4dfbaab3ac9018770f63aa9406ebcc7af35f4fea613eccfb",
      "size_bytes": 3910
    },
    "source_path": "experiment_v001/specs/pdeo-systematic-fault-suite-v1.json"
  },
  "finished_at_utc": "2026-08-13T03:34:47.295858Z",
  "implementation_files": [
    {
      "path": "implementation_v001/dqbp_core.py",
      "sha256": "4f9fc83512bfa8f0a660d90563793ddd7ed9462715b23a00c05ddf45d0b1039e",
      "size_bytes": 8752
    },
    {
      "path": "implementation_v001/formal_pdeo_experiment.py",
      "sha256": "7dea13632b6c6236fa678590f485491f09f04521713cd4a6b65d2b71e732f4fb",
      "size_bytes": 11368
    },
    {
      "path": "implementation_v001/obligation_bench.py",
      "sha256": "5f66bb8d64012283bb19d21fa655736350e52bf2cecdfb7f0fa5af619360f164",
      "size_bytes": 6027
    },
    {
      "path": "implementation_v001/obligation_core.py",
      "sha256": "80833fd3de04257e1063e03b8e87847fae7951b256b1dbb903906d84e6066d75",
      "size_bytes": 5360
    },
    {
      "path": "implementation_v001/run_experiment.py",
      "sha256": "2cd7c1c016a91a032866a39fa3f6671db61fb275fd9e529d8282aa6f6eb12261",
      "size_bytes": 8843
    },
    {
      "path": "implementation_v001/run_obligation_experiment.py",
      "sha256": "7584b680a715c4d13a0ecd7fd32988ca09915466e26395ffe7ff60676cebaeb0",
      "size_bytes": 9673
    },
    {
      "path": "implementation_v001/statefault_bench.py",
      "sha256": "74e6a975376ad01cb74e281a1f9f44737585435e9f3377afbb65e22903d9006a",
      "size_bytes": 13722
    },
    {
      "path": "implementation_v001/test_dqbp.py",
      "sha256": "d6cfb3d528285747243d9a1aa031da731c9fd2c1401e8108f744190667659a17",
      "size_bytes": 1287
    },
    {
      "path": "implementation_v001/test_formal_pdeo.py",
      "sha256": "554ed699ecc8fb4c40c7e0b947a524fab97e7201aeabe9f066ef52184cfc6b03",
      "size_bytes": 1013
    },
    {
      "path": "implementation_v001/test_obligation.py",
      "sha256": "a00eb364959899c22cd640dd2c41c3bc539866206cfc108b2e75167bb75dc6d5",
      "size_bytes": 2062
    }
  ],
  "inputs": [],
  "metrics": {
    "contains_possible_credential": false,
    "credential_detection": [],
    "snapshot": {
      "path": "D:\\Desktop\\crl\\20260813_1054_run09\\experiment_v001\\attempts\\attempt-pdeo-formal-002\\metrics.json",
      "sha256": "c0bf6a60ead529de4eeb80e6881d378a44783e8d918597cfa0e61873cc962158",
      "size_bytes": 30165
    },
    "source_path": "experiment_v001/attempts/attempt-pdeo-formal-002/metrics-output.json",
    "source_sha256": "c0bf6a60ead529de4eeb80e6881d378a44783e8d918597cfa0e61873cc962158",
    "source_size_bytes": 30165,
    "validation_errors": []
  },
  "metrics_contract_ok": true,
  "output_contract_ok": true,
  "outputs": [
    {
      "after": {
        "artifact_retained": true,
        "contains_possible_credential": false,
        "credential_detection": [],
        "exists": true,
        "sha256": "b14893ee985a87d00c7f08ac26bb3c94c8b8c487d7eb81339567db25b52ced57",
        "size_bytes": 641338
      },
      "before": {
        "exists": false
      },
      "path": "D:\\Desktop\\crl\\20260813_1054_run09\\experiment_v001\\attempts\\attempt-pdeo-formal-002\\formal-details.json"
    }
  ],
  "process_tree_cleanup_ok": null,
  "run_root": "D:\\Desktop\\crl\\20260813_1054_run09",
  "runner_exit_code": 0,
  "schema_version": 7,
  "seed": {
    "status": "not_set"
  },
  "started_at_utc": "2026-08-13T03:34:47.119218Z",
  "stdout_as_evidence": true,
  "termination_method": null,
  "timed_out": false,
  "timeout_seconds": 600.0,
  "version": "v001",
  "warnings": []
}

### Source: `experiment_v001/attempts/attempt-pdeo-formal-002/metrics.json`

{
  "schema_version": 1,
  "experiment_id": "pdeo-systematic-fault-suite-v1",
  "records": [
    {
      "name": "no_verification_unsafe_commit_rate_known_branches",
      "value": 0.5,
      "unit": "proportion",
      "split": "known_branches",
      "aggregation": "case_mean",
      "n": 24
    },
    {
      "name": "no_verification_gate_accuracy_known_branches",
      "value": 0.5,
      "unit": "proportion",
      "split": "known_branches",
      "aggregation": "case_mean",
      "n": 24
    },
    {
      "name": "no_verification_average_probe_cost_known_branches",
      "value": 0.0,
      "unit": "cost_units",
      "split": "known_branches",
      "aggregation": "case_mean",
      "n": 24
    },
    {
      "name": "no_verification_valid_commit_recall_known_branches",
      "value": 1.0,
      "unit": "proportion",
      "split": "known_branches",
      "aggregation": "case_mean",
      "n": 12
    },
    {
      "name": "static_receipt_unsafe_commit_rate_known_branches",
      "value": 0.5,
      "unit": "proportion",
      "split": "known_branches",
      "aggregation": "case_mean",
      "n": 24
    },
    {
      "name": "static_receipt_gate_accuracy_known_branches",
      "value": 0.5,
      "unit": "proportion",
      "split": "known_branches",
      "aggregation": "case_mean",
      "n": 24
    },
    {
      "name": "static_receipt_average_probe_cost_known_branches",
      "value": 0.0,
      "unit": "cost_units",
      "split": "known_branches",
      "aggregation": "case_mean",
      "n": 24
    },
    {
      "name": "static_receipt_valid_commit_recall_known_branches",
      "value": 1.0,
      "unit": "proportion",
      "split": "known_branches",
      "aggregation": "case_mean",
      "n": 12
    },
    {
      "name": "fixed_target_readback_unsafe_commit_rate_known_branches",
      "value": 0.20833333333333334,
      "unit": "proportion",
      "split": "known_branches",
      "aggregation": "case_mean",
      "n": 24
    },
    {
      "name": "fixed_target_readback_gate_accuracy_known_branches",
      "value": 0.7916666666666666,
      "unit": "proportion",
      "split": "known_branches",
      "aggregation": "case_mean",
      "n": 24
    },
    {
      "name": "fixed_target_readback_average_probe_cost_known_branches",
      "value": 1.0,
      "unit": "cost_units",
      "split": "known_branches",
      "aggregation": "case_mean",
      "n": 24
    },
    {
      "name": "fixed_target_readback_valid_commit_recall_known_branches",
      "value": 1.0,
      "unit": "proportion",
      "split": "known_branches",
      "aggregation": "case_mean",
      "n": 12
    },
    {
      "name": "tool_local_contract_unsafe_commit_rate_known_branches",
      "value": 0.0,
      "unit": "proportion",
      "split": "known_branches",
      "aggregation": "case_mean",
      "n": 24
    },
    {
      "name": "tool_local_contract_gate_accuracy_known_branches",
      "value": 1.0,
      "unit": "proportion",
      "split": "known_branches",
      "aggregation": "case_mean",
      "n": 24
    },
    {
      "name": "tool_local_contract_average_probe_cost_known_branches",
      "value": 5.0,
      "unit": "cost_units",
      "split": "known_branches",
      "aggregation": "case_mean",
      "n": 24
    },
    {
      "name": "tool_local_contract_valid_commit_recall_known_branches",
      "value": 1.0,
      "unit": "proportion",
      "split": "known_branches",
      "aggregation": "case_mean",
      "n": 12
    },
    {
      "name": "state_information_gain_unsafe_commit_rate_known_branches",
      "value": 0.0,
      "unit": "proportion",
      "split": "known_branches",
      "aggregation": "case_mean",
      "n": 24
    },
    {
      "name": "state_information_gain_gate_accuracy_known_branches",
      "value": 1.0,
      "unit": "proportion",
      "split": "known_branches",
      "aggregation": "case_mean",
      "n": 24
    },
    {
      "name": "state_information_gain_average_probe_cost_known_branches",
      "value": 1.7083333333333333,
      "unit": "cost_units",
      "split": "known_branches",
      "aggregation": "case_mean",
      "n": 24
    },
    {
      "name": "state_information_gain_valid_commit_recall_known_branches",
      "value": 1.0,
      "unit": "proportion",
      "split": "known_branches",
      "aggregation": "case_mean",
      "n": 12
    },
    {
      "name": "dqbp_unsafe_commit_rate_known_branches",
      "value": 0.0,
      "unit": "proportion",
      "split": "known_branches",
      "aggregation": "case_mean",
      "n": 24
    },
    {
      "name": "dqbp_gate_accuracy_known_branches",
      "value": 1.0,
      "unit": "proportion",
      "split": "known_branches",
      "aggregation": "case_mean",
      "n": 24
    },
    {
      "name": "dqbp_average_probe_cost_known_branches",
      "value": 1.75,
      "unit": "cost_units",
      "split": "known_branches",
      "aggregation": "case_mean",
      "n": 24
    },
    {
      "name": "dqbp_valid_commit_recall_known_branches",
      "value": 1.0,
      "unit": "proportion",
      "split": "known_branches",
      "aggregation": "case_mean",
      "n": 12
    },
    {
      "name": "pdeo_unsafe_commit_rate_known_branches",
      "value": 0.0,
      "unit": "proportion",
      "split": "known_branches",
      "aggregation": "case_mean",
      "n": 24
    },
    {
      "name": "pdeo_gate_accuracy_known_branches",
      "value": 1.0,
      "unit": "proportion",
      "split": "known_branches",
      "aggregation": "case_mean",
      "n": 24
    },
    {
      "name": "pdeo_average_probe_cost_known_branches",
      "value": 3.0,
      "unit": "cost_units",
      "split": "known_branches",
      "aggregation": "case_mean",
      "n": 24
    },
    {
      "name": "pdeo_valid_commit_recall_known_branches",
      "value": 1.0,
      "unit": "proportion",
      "split": "known_branches",
      "aggregation": "case_mean",
      "n": 12
    },
    {
      "name": "full_readback_unsafe_commit_rate_known_branches",
      "value": 0.0,
      "unit": "proportion",
      "split": "known_branches",
      "aggregation": "case_mean",
      "n": 24
    },
    {
      "name": "full_readback_gate_accuracy_known_branches",
      "value": 1.0,
      "unit": "proportion",
      "split": "known_branches",
      "aggregation": "case_mean",
      "n": 24
    },
    {
      "name": "full_readback_average_probe_cost_known_branches",
      "value": 6.0,
      "unit": "cost_units",
      "split": "known_branches",
      "aggregation": "case_mean",
      "n": 24
    },
    {
      "name": "full_readback_valid_commit_recall_known_branches",
      "value": 1.0,
      "unit": "proportion",
      "split": "known_branches",
      "aggregation": "case_mean",
      "n": 12
    },
    {
      "name": "human_minimal_obligations_unsafe_commit_rate_known_branches",
      "value": 0.0,
      "unit": "proportion",
      "split": "known_branches",
      "aggregation": "case_mean",
      "n": 24
    },
    {
      "name": "human_minimal_obligations_gate_accuracy_known_branches",
      "value": 1.0,
      "unit": "proportion",
      "split": "known_branches",
      "aggregation": "case_mean",
      "n": 24
    },
    {
      "name": "human_minimal_obligations_average_probe_cost_known_branches",
      "value": 3.0,
      "unit": "cost_units",
      "split": "known_branches",
      "aggregation": "case_mean",
      "n": 24
    },
    {
      "name": "human_minimal_obligations_valid_commit_recall_known_branches",
      "value": 1.0,
      "unit": "proportion",
      "split": "known_branches",
      "aggregation": "case_mean",
      "n": 12
    },
    {
      "name": "no_verification_unsafe_commit_rate_paired_obligation_and_nuisance_faults",
      "value": 1.0,
      "unit": "proportion",
      "split": "paired_obligation_and_nuisance_faults",
      "aggregation": "case_mean",
      "n": 36
    },
    {
      "name": "no_verification_gate_accuracy_paired_obligation_and_nuisance_faults",
      "value": 0.0,
      "unit": "proportion",
      "split": "paired_obligation_and_nuisance_faults",
      "aggregation": "case_mean",
      "n": 36
    },
    {
      "name": "no_verification_average_probe_cost_paired_obligation_and_nuisance_faults",
      "value": 0.0,
      "unit": "cost_units",
      "split": "paired_obligation_and_nuisance_faults",
      "aggregation": "case_mean",
      "n": 36
    },
    {
      "name": "static_receipt_unsafe_commit_rate_paired_obligation_and_nuisance_faults",
      "value": 1.0,
      "unit": "proportion",
      "split": "paired_obligation_and_nuisance_faults",
      "aggregation": "case_mean",
      "n": 36
    },
    {
      "name": "static_receipt_gate_accuracy_paired_obligation_and_nuisance_faults",
      "value": 0.0,
      "unit": "proportion",
      "split": "paired_obligation_and_nuisance_faults",
      "aggregation": "case_mean",
      "n": 36
    },
    {
      "name": "static_receipt_average_probe_cost_paired_obligation_and_nuisance_faults",
      "value": 0.0,
      "unit": "cost_units",
      "split": "paired_obligation_and_nuisance_faults",
      "aggregation": "case_mean",
      "n": 36
    },
    {
      "name": "fixed_target_readback_unsafe_commit_rate_paired_obligation_and_nuisance_faults",
      "value": 0.6666666666666666,
      "unit": "proportion",
      "split": "paired_obligation_and_nuisance_faults",
      "aggregation": "case_mean",
      "n": 36
    },
    {
      "name": "fixed_target_readback_gate_accuracy_paired_obligation_and_nuisance_faults",
      "value": 0.3333333333333333,
      "unit": "proportion",
      "split": "paired_obligation_and_nuisance_faults",
      "aggregation": "case_mean",
      "n": 36
    },
    {
      "name": "fixed_target_readback_average_probe_cost_paired_obligation_and_nuisance_faults",
      "value": 1.0,
      "unit": "cost_units",
      "split": "paired_obligation_and_nuisance_faults",
      "aggregation": "case_mean",
      "n": 36
    },
    {
      "name": "tool_local_contract_unsafe_commit_rate_paired_obligation_and_nuisance_faults",
      "value": 0.0,
      "unit": "proportion",
      "split": "paired_obligation_and_nuisance_faults",
      "aggregation": "case_mean",
      "n": 36
    },
    {
      "name": "tool_local_contract_gate_accuracy_paired_obligation_and_nuisance_faults",
      "value": 1.0,
      "unit": "proportion",
      "split": "paired_obligation_and_nuisance_faults",
      "aggregation": "case_mean",
      "n": 36
    },
    {
      "name": "tool_local_contract_average_probe_cost_paired_obligation_and_nuisance_faults",
      "value": 5.0,
      "unit": "cost_units",
      "split": "paired_obligation_and_nuisance_faults",
      "aggregation": "case_mean",
      "n": 36
    },
    {
      "name": "state_information_gain_unsafe_commit_rate_paired_obligation_and_nuisance_faults",
      "value": 0.7777777777777778,
      "unit": "proportion",
      "split": "paired_obligation_and_nuisance_faults",
      "aggregation": "case_mean",
      "n": 36
    },
    {
      "name": "state_information_gain_gate_accuracy_paired_obligation_and_nuisance_faults",
      "value": 0.2222222222222222,
      "unit": "proportion",
      "split": "paired_obligation_and_nuisance_faults",
      "aggregation": "case_mean",
      "n": 36
    },
    {
      "name": "state_information_gain_average_probe_cost_paired_obligation_and_nuisance_faults",
      "value": 1.6666666666666667,
      "unit": "cost_units",
      "split": "paired_obligation_and_nuisance_faults",
      "aggregation": "case_mean",
      "n": 36
    },
    {
      "name": "dqbp_unsafe_commit_rate_paired_obligation_and_nuisance_faults",
      "value": 0.3333333333333333,
      "unit": "proportion",
      "split": "paired_obligation_and_nuisance_faults",
      "aggregation": "case_mean",
      "n": 36
    },
    {
      "name": "dqbp_gate_accuracy_paired_obligation_and_nuisance_faults",
      "value": 0.6666666666666666,
      "unit": "proportion",
      "split": "paired_obligation_and_nuisance_faults",
      "aggregation": "case_mean",
      "n": 36
    },
    {
      "name": "dqbp_average_probe_cost_paired_obligation_and_nuisance_faults",
      "value": 1.5555555555555556,
      "unit": "cost_units",
      "split": "paired_obligation_and_nuisance_faults",
      "aggregation": "case_mean",
      "n": 36
    },
    {
      "name": "pdeo_unsafe_commit_rate_paired_obligation_and_nuisance_faults",
      "value": 0.0,
      "unit": "proportion",
      "split": "paired_obligation_and_nuisance_faults",
      "aggregation": "case_mean",
      "n": 36
    },
    {
      "name": "pdeo_gate_accuracy_paired_obligation_and_nuisance_faults",
      "value": 1.0,
      "unit": "proportion",
      "split": "paired_obligation_and_nuisance_faults",
      "aggregation": "case_mean",
      "n": 36
    },
    {
      "name": "pdeo_average_probe_cost_paired_obligation_and_nuisance_faults",
      "value": 3.0,
      "unit": "cost_units",
      "split": "paired_obligation_and_nuisance_faults",
      "aggregation": "case_mean",
      "n": 36
    },
    {
      "name": "full_readback_unsafe_commit_rate_paired_obligation_and_nuisance_faults",
      "value": 0.0,
      "unit": "proportion",
      "split": "paired_obligation_and_nuisance_faults",
      "aggregation": "case_mean",
      "n": 36
    },
    {
      "name": "full_readback_gate_accuracy_paired_obligation_and_nuisance_faults",
      "value": 1.0,
      "unit": "proportion",
      "split": "paired_obligation_and_nuisance_faults",
      "aggregation": "case_mean",
      "n": 36
    },
    {
      "name": "full_readback_average_probe_cost_paired_obligation_and_nuisance_faults",
      "value": 6.0,
      "unit": "cost_units",
      "split": "paired_obligation_and_nuisance_faults",
      "aggregation": "case_mean",
      "n": 36
    },
    {
      "name": "human_minimal_obligations_unsafe_commit_rate_paired_obligation_and_nuisance_faults",
      "value": 0.0,
      "unit": "proportion",
      "split": "paired_obligation_and_nuisance_faults",
      "aggregation": "case_mean",
      "n": 36
    },
    {
      "name": "human_minimal_obligations_gate_accuracy_paired_obligation_and_nuisance_faults",
      "value": 1.0,
      "unit": "proportion",
      "split": "paired_obligation_and_nuisance_faults",
      "aggregation": "case_mean",
      "n": 36
    },
    {
      "name": "human_minimal_obligations_average_probe_cost_paired_obligation_and_nuisance_faults",
      "value": 3.0,
      "unit": "cost_units",
      "split": "paired_obligation_and_nuisance_faults",
      "aggregation": "case_mean",
      "n": 36
    },
    {
      "name": "no_verification_unsafe_commit_rate_systematic_nuisance_variants",
      "value": 0.0,
      "unit": "proportion",
      "split": "systematic_nuisance_variants",
      "aggregation": "case_mean",
      "n": 63
    },
    {
      "name": "no_verification_gate_accuracy_systematic_nuisance_variants",
      "value": 1.0,
      "unit": "proportion",
      "split": "systematic_nuisance_variants",
      "aggregation": "case_mean",
      "n": 63
    },
    {
      "name": "no_verification_average_probe_cost_systematic_nuisance_variants",
      "value": 0.0,
      "unit": "cost_units",
      "split": "systematic_nuisance_variants",
      "aggregation": "case_mean",
      "n": 63
    },
    {
      "name": "no_verification_valid_commit_recall_systematic_nuisance_variants",
      "value": 1.0,
      "unit": "proportion",
      "split": "systematic_nuisance_variants",
      "aggregation": "case_mean",
      "n": 63
    },
    {
      "name": "static_receipt_unsafe_commit_rate_systematic_nuisance_variants",
      "value": 0.0,
      "unit": "proportion",
      "split": "systematic_nuisance_variants",
      "aggregation": "case_mean",
      "n": 63
    },
    {
      "name": "static_receipt_gate_accuracy_systematic_nuisance_variants",
      "value": 1.0,
      "unit": "proportion",
      "split": "systematic_nuisance_variants",
      "aggregation": "case_mean",
      "n": 63
    },
    {
      "name": "static_receipt_average_probe_cost_systematic_nuisance_variants",
      "value": 0.0,
      "unit": "cost_units",
      "split": "systematic_nuisance_variants",
      "aggregation": "case_mean",
      "n": 63
    },
    {
      "name": "static_receipt_valid_commit_recall_systematic_nuisance_variants",
      "value": 1.0,
      "unit": "proportion",
      "split": "systematic_nuisance_variants",
      "aggregation": "case_mean",
      "n": 63
    },
    {
      "name": "fixed_target_readback_unsafe_commit_rate_systematic_nuisance_variants",
      "value": 0.0,
      "unit": "proportion",
      "split": "systematic_nuisance_variants",
      "aggregation": "case_mean",
      "n": 63
    },
    {
      "name": "fixed_target_readback_gate_accuracy_systematic_nuisance_variants",
      "value": 1.0,
      "unit": "proportion",
      "split": "systematic_nuisance_variants",
      "aggregation": "case_mean",
      "n": 63
    },
    {
      "name": "fixed_target_readback_average_probe_cost_systematic_nuisance_variants",
      "value": 1.0,
      "unit": "cost_units",
      "split": "systematic_nuisance_variants",
      "aggregation": "case_mean",
      "n": 63
    },
    {
      "name": "fixed_target_readback_valid_commit_recall_systematic_nuisance_variants",
      "value": 1.0,
      "unit": "proportion",
      "split": "systematic_nuisance_variants",
      "aggregation": "case_mean",
      "n": 63
    },
    {
      "name": "tool_local_contract_unsafe_commit_rate_systematic_nuisance_variants",
      "value": 0.0,
      "unit": "proportion",
      "split": "systematic_nuisance_variants",
      "aggregation": "case_mean",
      "n": 63
    },
    {
      "name": "tool_local_contract_gate_accuracy_systematic_nuisance_variants",
      "value": 0.23809523809523808,
      "unit": "proportion",
      "split": "systematic_nuisance_variants",
      "aggregation": "case_mean",
      "n": 63
    },
    {
      "name": "tool_local_contract_average_probe_cost_systematic_nuisance_variants",
      "value": 5.0,
      "unit": "cost_units",
      "split": "systematic_nuisance_variants",
      "aggregation": "case_mean",
      "n": 63
    },
    {
      "name": "tool_local_contract_valid_commit_recall_systematic_nuisance_variants",
      "value": 0.23809523809523808,
      "unit": "proportion",
      "split": "systematic_nuisance_variants",
      "aggregation": "case_mean",
      "n": 63
    },
    {
      "name": "state_information_gain_unsafe_commit_rate_systematic_nuisance_variants",
      "value": 0.0,
      "unit": "proportion",
      "split": "systematic_nuisance_variants",
      "aggregation": "case_mean",
      "n": 63
    },
    {
      "name": "state_information_gain_gate_accuracy_systematic_nuisance_variants",
      "value": 0.9523809523809523,
      "unit": "proportion",
      "split": "systematic_nuisance_variants",
      "aggregation": "case_mean",
      "n": 63
    },
    {
      "name": "state_information_gain_average_probe_cost_systematic_nuisance_variants",
      "value": 1.6349206349206349,
      "unit": "cost_units",
      "split": "systematic_nuisance_variants",
      "aggregation": "case_mean",
      "n": 63
    },
    {
      "name": "state_information_gain_valid_commit_recall_systematic_nuisance_variants",
      "value": 0.9523809523809523,
      "unit": "proportion",
      "split": "systematic_nuisance_variants",
      "aggregation": "case_mean",
      "n": 63
    },
    {
      "name": "dqbp_unsafe_commit_rate_systematic_nuisance_variants",
      "value": 0.0,
      "unit": "proportion",
      "split": "systematic_nuisance_variants",
      "aggregation": "case_mean",
      "n": 63
    },
    {
      "name": "dqbp_gate_accuracy_systematic_nuisance_variants",
      "value": 0.746031746031746,
      "unit": "proportion",
      "split": "systematic_nuisance_variants",
      "aggregation": "case_mean",
      "n": 63
    },
    {
      "name": "dqbp_average_probe_cost_systematic_nuisance_variants",
      "value": 1.6666666666666667,
      "unit": "cost_units",
      "split": "systematic_nuisance_variants",
      "aggregation": "case_mean",
      "n": 63
    },
    {
      "name": "dqbp_valid_commit_recall_systematic_nuisance_variants",
      "value": 0.746031746031746,
      "unit": "proportion",
      "split": "systematic_nuisance_variants",
      "aggregation": "case_mean",
      "n": 63
    },
    {
      "name": "pdeo_unsafe_commit_rate_systematic_nuisance_variants",
      "value": 0.0,
      "unit": "proportion",
      "split": "systematic_nuisance_variants",
      "aggregation": "case_mean",
      "n": 63
    },
    {
      "name": "pdeo_gate_accuracy_systematic_nuisance_variants",
      "value": 1.0,
      "unit": "proportion",
      "split": "systematic_nuisance_variants",
      "aggregation": "case_mean",
      "n": 63
    },
    {
      "name": "pdeo_average_probe_cost_systematic_nuisance_variants",
      "value": 3.0,
      "unit": "cost_units",
      "split": "systematic_nuisance_variants",
      "aggregation": "case_mean",
      "n": 63
    },
    {
      "name": "pdeo_valid_commit_recall_systematic_nuisance_variants",
      "value": 1.0,
      "unit": "proportion",
      "split": "systematic_nuisance_variants",
      "aggregation": "case_mean",
      "n": 63
    },
    {
      "name": "full_readback_unsafe_commit_rate_systematic_nuisance_variants",
      "value": 0.0,
      "unit": "proportion",
      "split": "systematic_nuisance_variants",
      "aggregation": "case_mean",
      "n": 63
    },
    {
      "name": "full_readback_gate_accuracy_systematic_nuisance_variants",
      "value": 1.0,
      "unit": "proportion",
      "split": "systematic_nuisance_variants",
      "aggregation": "case_mean",
      "n": 63
    },
    {
      "name": "full_readback_average_probe_cost_systematic_nuisance_variants",
      "value": 6.0,
      "unit": "cost_units",
      "split": "systematic_nuisance_variants",
      "aggregation": "case_mean",
      "n": 63
    },
    {
      "name": "full_readback_valid_commit_recall_systematic_nuisance_variants",
      "value": 1.0,
      "unit": "proportion",
      "split": "systematic_nuisance_variants",
      "aggregation": "case_mean",
      "n": 63
    },
    {
      "name": "human_minimal_obligations_unsafe_commit_rate_systematic_nuisance_variants",
      "value": 0.0,
      "unit": "proportion",
      "split": "systematic_nuisance_variants",
      "aggregation": "case_mean",
      "n": 63
    },
    {
      "name": "human_minimal_obligations_gate_accuracy_systematic_nuisance_variants",
      "value": 1.0,
      "unit": "proportion",
      "split": "systematic_nuisance_variants",
      "aggregation": "case_mean",
      "n": 63
    },
    {
      "name": "human_minimal_obligations_average_probe_cost_systematic_nuisance_variants",
      "value": 3.0,
      "unit": "cost_units",
      "split": "systematic_nuisance_variants",
      "aggregation": "case_mean",
      "n": 63
    },
    {
      "name": "human_minimal_obligations_valid_commit_recall_systematic_nuisance_variants",
      "value": 1.0,
      "unit": "proportion",
      "split": "systematic_nuisance_variants",
      "aggregation": "case_mean",
      "n": 63
    },
    {
      "name": "no_verification_unsafe_commit_rate_systematic_obligation_faults",
      "value": 1.0,
      "unit": "proportion",
      "split": "systematic_obligation_faults",
      "aggregation": "case_mean",
      "n": 48
    },
    {
      "name": "no_verification_gate_accuracy_systematic_obligation_faults",
      "value": 0.0,
      "unit": "proportion",
      "split": "systematic_obligation_faults",
      "aggregation": "case_mean",
      "n": 48
    },
    {
      "name": "no_verification_average_probe_cost_systematic_obligation_faults",
      "value": 0.0,
      "unit": "cost_units",
      "split": "systematic_obligation_faults",
      "aggregation": "case_mean",
      "n": 48
    },
    {
      "name": "static_receipt_unsafe_commit_rate_systematic_obligation_faults",
      "value": 1.0,
      "unit": "proportion",
      "split": "systematic_obligation_faults",
      "aggregation": "case_mean",
      "n": 48
    },
    {
      "name": "static_receipt_gate_accuracy_systematic_obligation_faults",
      "value": 0.0,
      "unit": "proportion",
      "split": "systematic_obligation_faults",
      "aggregation": "case_mean",
      "n": 48
    },
    {
      "name": "static_receipt_average_probe_cost_systematic_obligation_faults",
      "value": 0.0,
      "unit": "cost_units",
      "split": "systematic_obligation_faults",
      "aggregation": "case_mean",
      "n": 48
    },
    {
      "name": "fixed_target_readback_unsafe_commit_rate_systematic_obligation_faults",
      "value": 0.6666666666666666,
      "unit": "proportion",
      "split": "systematic_obligation_faults",
      "aggregation": "case_mean",
      "n": 48
    },
    {
      "name": "fixed_target_readback_gate_accuracy_systematic_obligation_faults",
      "value": 0.3333333333333333,
      "unit": "proportion",
      "split": "systematic_obligation_faults",
      "aggregation": "case_mean",
      "n": 48
    },
    {
      "name": "fixed_target_readback_average_probe_cost_systematic_obligation_faults",
      "value": 1.0,
      "unit": "cost_units",
      "split": "systematic_obligation_faults",
      "aggregation": "case_mean",
      "n": 48
    },
    {
      "name": "tool_local_contract_unsafe_commit_rate_systematic_obligation_faults",
      "value": 0.0,
      "unit": "proportion",
      "split": "systematic_obligation_faults",
      "aggregation": "case_mean",
      "n": 48
    },
    {
      "name": "tool_local_contract_gate_accuracy_systematic_obligation_faults",
      "value": 1.0,
      "unit": "proportion",
      "split": "systematic_obligation_faults",
      "aggregation": "case_mean",
      "n": 48
    },
    {
      "name": "tool_local_contract_average_probe_cost_systematic_obligation_faults",
      "value": 5.0,
      "unit": "cost_units",
      "split": "systematic_obligation_faults",
      "aggregation": "case_mean",
      "n": 48
    },
    {
      "name": "state_information_gain_unsafe_commit_rate_systematic_obligation_faults",
      "value": 0.75,
      "unit": "proportion",
      "split": "systematic_obligation_faults",
      "aggregation": "case_mean",
      "n": 48
    },
    {
      "name": "state_information_gain_gate_accuracy_systematic_obligation_faults",
      "value": 0.25,
      "unit": "proportion",
      "split": "systematic_obligation_faults",
      "aggregation": "case_mean",
      "n": 48
    },
    {
      "name": "state_information_gain_average_probe_cost_systematic_obligation_faults",
      "value": 1.6666666666666667,
      "unit": "cost_units",
      "split": "systematic_obligation_faults",
      "aggregation": "case_mean",
      "n": 48
    },
    {
      "name": "dqbp_unsafe_commit_rate_systematic_obligation_faults",
      "value": 0.5833333333333334,
      "unit": "proportion",
      "split": "systematic_obligation_faults",
      "aggregation": "case_mean",
      "n": 48
    },
    {
      "name": "dqbp_gate_accuracy_systematic_obligation_faults",
      "value": 0.4166666666666667,
      "unit": "proportion",
      "split": "systematic_obligation_faults",
      "aggregation": "case_mean",
      "n": 48
    },
    {
      "name": "dqbp_average_probe_cost_systematic_obligation_faults",
      "value": 1.6666666666666667,
      "unit": "cost_units",
      "split": "systematic_obligation_faults",
      "aggregation": "case_mean",
      "n": 48
    },
    {
      "name": "pdeo_unsafe_commit_rate_systematic_obligation_faults",
      "value": 0.0,
      "unit": "proportion",
      "split": "systematic_obligation_faults",
      "aggregation": "case_mean",
      "n": 48
    },
    {
      "name": "pdeo_gate_accuracy_systematic_obligation_faults",
      "value": 1.0,
      "unit": "proportion",
      "split": "systematic_obligation_faults",
      "aggregation": "case_mean",
      "n": 48
    },
    {
      "name": "pdeo_average_probe_cost_systematic_obligation_faults",
      "value": 3.0,
      "unit": "cost_units",
      "split": "systematic_obligation_faults",
      "aggregation": "case_mean",
      "n": 48
    },
    {
      "name": "full_readback_unsafe_commit_rate_systematic_obligation_faults",
      "value": 0.0,
      "unit": "proportion",
      "split": "systematic_obligation_faults",
      "aggregation": "case_mean",
      "n": 48
    },
    {
      "name": "full_readback_gate_accuracy_systematic_obligation_faults",
      "value": 1.0,
      "unit": "proportion",
      "split": "systematic_obligation_faults",
      "aggregation": "case_mean",
      "n": 48
    },
    {
      "name": "full_readback_average_probe_cost_systematic_obligation_faults",
      "value": 6.0,
      "unit": "cost_units",
      "split": "systematic_obligation_faults",
      "aggregation": "case_mean",
      "n": 48
    },
    {
      "name": "human_minimal_obligations_unsafe_commit_rate_systematic_obligation_faults",
      "value": 0.0,
      "unit": "proportion",
      "split": "systematic_obligation_faults",
      "aggregation": "case_mean",
      "n": 48
    },
    {
      "name": "human_minimal_obligations_gate_accuracy_systematic_obligation_faults",
      "value": 1.0,
      "unit": "proportion",
      "split": "systematic_obligation_faults",
      "aggregation": "case_mean",
      "n": 48
    },
    {
      "name": "human_minimal_obligations_average_probe_cost_systematic_obligation_faults",
      "value": 3.0,
      "unit": "cost_units",
      "split": "systematic_obligation_faults",
      "aggregation": "case_mean",
      "n": 48
    }
  ],
  "resource_usage": {
    "tokens": 0,
    "api_calls": 0,
    "wall_time_seconds": 0.046927100000175415,
    "gpu_time_seconds": 0,
    "estimated_cost": 0
  },
  "errors": [],
  "warnings": [
    "Controlled systematic simulator over typed plans; no natural-language plan extraction is evaluated.",
    "Evaluator safety rules are declared separately from the PDEO compiler and cover all systematic single-obligation mutations present in the pre-existing branch vocabulary."
  ]
}

## 4. Baseline & Budget Facts

### Source: `experiment_v001/plan.md`

# PDEO 正式实验计划

实验标识：`pdeo-systematic-fault-suite-v1`  
正式尝试：`attempt-pdeo-formal-001`

## 要反证的最小主张

在类型计划、工具效果和只读探针覆盖正确的受控状态域中，PDEO 应同时满足：

1. 系统性单义务故障危险提交率为 0；
2. 安全的计划无关字段变异提交召回率为 1；
3. 平均探针成本严格低于写工具本地完整契约。

任一条件失败即反证当前主张。

## 评价独立性

评价器在 `formal_pdeo_experiment.py` 的 `SAFETY_RULES` 中独立声明预约、访问控制和库存三个域的安全提交谓词。标签由真实状态是否满足这些规则计算，不调用 `compile_obligations`。正式运行还检查编译器输出与独立规则是否一致，但这一一致性检查不生成标签。

故障集不是按 PDEO 的选择轨迹挑选：它从 H1 已存在的状态词表系统枚举 24 个原始分支、48 个单义务替换、63 个无关字段替换和 36 个义务—无关字段配对替换，共 171 例。

## 公平性

所有方法共享同一类型计划、工具规格、真实探针返回和探针成本。状态信息增益与 DQBP 共享同一封闭分支模型和预算 3；固定、完整与义务方法按实际探针集合计成本，因此结论是安全—成本帕累托比较，不是相同调用数下的单指标比较。

人工最小义务只作为编译正确性上界。它与 PDEO 相同不构成经验优势；PDEO 的方法价值仅在于由计划自动得到该义务集合。

## 已知限制

不评价自然语言到类型计划的生成、探针读取噪声、并发写入、权限失败、陈旧读或恢复策略。三个域结构同源，不能代表真实工具生态。

### Source: `experiment_v001/specs/pdeo-systematic-fault-suite-v1.json`

{
  "baseline_specs": [
    "无验证",
    "静态成功回执",
    "固定目标读回",
    "写工具本地完整契约",
    "状态信息增益",
    "DQBP",
    "全量读回",
    "人工最小义务上界"
  ],
  "budget_ceiling": "确定性穷举；每例最多读取全部五个探针，总成本上限 6；自适应基线预算 3。",
  "claim_ids": [
    "pdeo-systematic-safe-gating"
  ],
  "confounders": [
    "评价规则与候选都依赖类型规格正确性，但评价规则在独立常量中声明且不调用编译器。",
    "系统性词表变异不覆盖连续状态、并发和读取噪声。",
    "人工最小义务与 PDEO 在当前域应相同，只是编译上界而非竞争方法。"
  ],
  "dataset": "三个预先存在的状态域上 171 个确定性系统故障与无关变异案例",
  "declared_inputs": [],
  "declared_outputs": [],
  "expected_signatures": [
    "PDEO 系统性义务故障危险提交率为 0。",
    "PDEO 安全无关变异提交召回率为 1。",
    "PDEO 平均探针成本为 3，低于工具本地完整契约的 5 和全量读回的 6。"
  ],
  "experiment_id": "pdeo-systematic-fault-suite-v1",
  "falsification_rule": "任一 PDEO 系统性义务故障被提交，或安全无关变异提交召回率低于 1，或 PDEO 平均成本不低于工具本地完整契约，即反证当前最小主张。",
  "hypothesis_id": "h4-pdeo",
  "independent_ground_truth": {
    "description": "评价器在 formal_pdeo_experiment.py 的 SAFETY_RULES 中独立声明每个域的安全提交谓词，不调用 PDEO 编译器生成标签；故障集系统性枚举预先存在分支词表中的全部单义务替换、无关字段替换与配对替换。",
    "external_card_ids": [],
    "external_evidence_ids": [],
    "external_literature_refs": [
      "ToolGate: Findings of ACL 2026",
      "ETAS: arXiv:2607.17780"
    ],
    "run_local_fact_refs": [
      "implementation_v001/statefault_bench.py",
      "implementation_v001/formal_pdeo_experiment.py"
    ]
  },
  "model": "无语言模型；确定性类型计划控制器",
  "parity_dimensions": {
    "budget": {
      "notes": "固定、完整与义务方法按其实际探针集合计成本；DQBP 与状态信息增益共享预算 3。比较安全—成本帕累托，而非强行截断完整契约。",
      "status": "different"
    },
    "information_access": {
      "notes": "所有可部署方法共享类型计划、工具规格与探针返回；故障标签仅由评价器使用。",
      "status": "matched"
    },
    "model_provider_revision": {
      "notes": "所有控制器均为同一 Python 运行时中的确定性代码，不调用模型。",
      "status": "matched"
    },
    "sampling_protocol": {
      "notes": "每个方法运行全部 171 个冻结的系统性案例。",
      "status": "matched"
    },
    "tool_capability": {
      "notes": "所有方法使用同一只读探针目录和成本。",
      "status": "matched"
    }
  },
  "primary_metric": "pdeo_unsafe_commit_rate_systematic_obligation_faults",
  "provider": "本地 Python 3.11",
  "purpose": "independent_claim_validation",
  "research_question": "计划派生证据义务能否在系统性未见义务故障上保持零危险提交，并以低于完整工具契约的成本接受全部安全无关变异？",
  "revision": "pdeo-formal-r1",
  "run_id": "20260813_1054_run09",
  "sampling_unit": "一个域内完整状态与受保护提交的组合",
  "schema_version": 1,
  "secondary_metrics": [
    "pdeo_valid_commit_recall_systematic_nuisance_variants",
    "pdeo_average_probe_cost_systematic_obligation_faults",
    "tool_local_contract_average_probe_cost_systematic_obligation_faults",
    "dqbp_unsafe_commit_rate_systematic_obligation_faults",
    "state_information_gain_unsafe_commit_rate_systematic_obligation_faults"
  ],
  "seeds": [],
  "version": "v001"
}

## 5. Ablation / Robustness / Falsification Evidence

### Source: `failure_attribution_v001.md`

# 失败归因：DQBP Scratch 反证

## 证据级别

本记录只依据 `workbench_v001/scratch_metrics.json` 与 `workbench_v001/scratch_details.json`。这是控制器隔离的 Scratch 仿真，不是 Formal / Review-support 实验，未调用语言模型，也不能支持交付。

## 观察结果

三个域、每域 10,000 个同分布样本、预算 2、随机种子 20260813：

- DQBP：成功率 1.000，危险错误率 0，平均探针成本 1.7703；
- 状态信息增益：成功率 1.000，危险错误率 0，平均探针成本约 1.707；
- 固定目标读回：成功率 0.651；
- DQBP 相对预算匹配最佳基线的预设成功率优势：0.000。

在失败加重与成功加重的先验变体中，DQBP 与状态信息增益仍都达到 1.000 成功率，且 DQBP 平均成本分别为 1.805 和 1.728，均高于状态信息增益的 1.710 和 1.705。

## 主研究者解释

失败发生在方法核而非单一代码实现：DQBP 与状态信息增益共享有限分支模型，当前探针足以让状态熵目标顺便分离全部决策类。DQBP 在访问控制域选择成本为 2 的审计事件，在预约与库存域也没有形成更短的决策证据路径，因此“先按下游决策取商”没有转化为成本或成功率收益。

更根本地，DQBP 的目标是标准贝叶斯决策风险下的探针价值；在没有新的结构约束时，它容易被一般价值信息或强信息增益基线吸收。继续调节分支先验或添加专门让状态熵追逐噪声的样本，会把结果变成对基线不利的数据设计，不能作为挽救依据。

## 杀伤范围

- 杀死：当前 DQBP 方法核及其“优于状态信息增益”的主张；
- 未杀死：写后环境验证这一问题；
- 未支持：Run 级无交付，因为在终局前仍需完成一次正交路线复核；
- 不得复用：不能把相同分支模型换名后作为新候选。

## 后续约束

新的 H4 不使用已知故障分支来选择探针，而从计划承诺产生必须验证的证据闭包；它必须在未见故障上接受反证，并与完整工具契约、全量读回、DQBP 和状态信息增益共同比较。

### Source: `workbench_v001/pdeo_scratch_metrics.json`

{
  "schema_version": 1,
  "experiment_id": "pdeo-controller-v1",
  "episodes_per_domain": 10000,
  "budget": 3,
  "seed": 20260813,
  "summaries": [
    {
      "condition": "known",
      "method": "no_verification",
      "n": 30000,
      "gate_accuracy": 0.4492333333333333,
      "unsafe_commit_rate": 0.5507666666666666,
      "valid_commit_recall": 1.0,
      "average_probe_cost": 0.0
    },
    {
      "condition": "known",
      "method": "static_receipt",
      "n": 30000,
      "gate_accuracy": 0.4492333333333333,
      "unsafe_commit_rate": 0.5507666666666666,
      "valid_commit_recall": 1.0,
      "average_probe_cost": 0.0
    },
    {
      "condition": "known",
      "method": "fixed_target_readback",
      "n": 30000,
      "gate_accuracy": 0.7806333333333333,
      "unsafe_commit_rate": 0.21936666666666665,
      "valid_commit_recall": 1.0,
      "average_probe_cost": 1.0
    },
    {
      "condition": "known",
      "method": "tool_local_contract",
      "n": 30000,
      "gate_accuracy": 1.0,
      "unsafe_commit_rate": 0.0,
      "valid_commit_recall": 1.0,
      "average_probe_cost": 5.0
    },
    {
      "condition": "known",
      "method": "state_information_gain",
      "n": 30000,
      "gate_accuracy": 1.0,
      "unsafe_commit_rate": 0.0,
      "valid_commit_recall": 1.0,
      "average_probe_cost": 1.7070333333333334
    },
    {
      "condition": "known",
      "method": "dqbp",
      "n": 30000,
      "gate_accuracy": 1.0,
      "unsafe_commit_rate": 0.0,
      "valid_commit_recall": 1.0,
      "average_probe_cost": 1.7703
    },
    {
      "condition": "known",
      "method": "pdeo",
      "n": 30000,
      "gate_accuracy": 1.0,
      "unsafe_commit_rate": 0.0,
      "valid_commit_recall": 1.0,
      "average_probe_cost": 3.0
    },
    {
      "condition": "known",
      "method": "full_readback",
      "n": 30000,
      "gate_accuracy": 1.0,
      "unsafe_commit_rate": 0.0,
      "valid_commit_recall": 1.0,
      "average_probe_cost": 6.0
    },
    {
      "condition": "known",
      "method": "human_minimal_obligations",
      "n": 30000,
      "gate_accuracy": 1.0,
      "unsafe_commit_rate": 0.0,
      "valid_commit_recall": 1.0,
      "average_probe_cost": 3.0
    },
    {
      "condition": "open_world",
      "method": "no_verification",
      "n": 30000,
      "gate_accuracy": 0.0,
      "unsafe_commit_rate": 1.0,
      "valid_commit_recall": null,
      "average_probe_cost": 0.0
    },
    {
      "condition": "open_world",
      "method": "static_receipt",
      "n": 30000,
      "gate_accuracy": 0.0,
      "unsafe_commit_rate": 1.0,
      "valid_commit_recall": null,
      "average_probe_cost": 0.0
    },
    {
      "condition": "open_world",
      "method": "fixed_target_readback",
      "n": 30000,
      "gate_accuracy": 0.3333333333333333,
      "unsafe_commit_rate": 0.6666666666666666,
      "valid_commit_recall": null,
      "average_probe_cost": 1.0
    },
    {
      "condition": "open_world",
      "method": "tool_local_contract",
      "n": 30000,
      "gate_accuracy": 1.0,
      "unsafe_commit_rate": 0.0,
      "valid_commit_recall": null,
      "average_probe_cost": 5.0
    },
    {
      "condition": "open_world",
      "method": "state_information_gain",
      "n": 30000,
      "gate_accuracy": 0.0,
      "unsafe_commit_rate": 1.0,
      "valid_commit_recall": null,
      "average_probe_cost": 2.0
    },
    {
      "condition": "open_world",
      "method": "dqbp",
      "n": 30000,
      "gate_accuracy": 0.0,
      "unsafe_commit_rate": 1.0,
      "valid_commit_recall": null,
      "average_probe_cost": 1.6666666666666667
    },
    {
      "condition": "open_world",
      "method": "pdeo",
      "n": 30000,
      "gate_accuracy": 1.0,
      "unsafe_commit_rate": 0.0,
      "valid_commit_recall": null,
      "average_probe_cost": 3.0
    },
    {
      "condition": "open_world",
      "method": "full_readback",
      "n": 30000,
      "gate_accuracy": 1.0,
      "unsafe_commit_rate": 0.0,
      "valid_commit_recall": null,
      "average_probe_cost": 6.0
    },
    {
      "condition": "open_world",
      "method": "human_minimal_obligations",
      "n": 30000,
      "gate_accuracy": 1.0,
      "unsafe_commit_rate": 0.0,
      "valid_commit_recall": null,
      "average_probe_cost": 3.0
    },
    {
      "condition": "mixed",
      "method": "no_verification",
      "n": 30000,
      "gate_accuracy": 0.35706666666666664,
      "unsafe_commit_rate": 0.6429333333333334,
      "valid_commit_recall": 1.0,
      "average_probe_cost": 0.0
    },
    {
      "condition": "mixed",
      "method": "static_receipt",
      "n": 30000,
      "gate_accuracy": 0.35706666666666664,
      "unsafe_commit_rate": 0.6429333333333334,
      "valid_commit_recall": 1.0,
      "average_probe_cost": 0.0
    },
    {
      "condition": "mixed",
      "method": "fixed_target_readback",
      "n": 30000,
      "gate_accuracy": 0.6919666666666666,
      "unsafe_commit_rate": 0.3080333333333333,
      "valid_commit_recall": 1.0,
      "average_probe_cost": 1.0
    },
    {
      "condition": "mixed",
      "method": "tool_local_contract",
      "n": 30000,
      "gate_accuracy": 1.0,
      "unsafe_commit_rate": 0.0,
      "valid_commit_recall": 1.0,
      "average_probe_cost": 5.0
    },
    {
      "condition": "mixed",
      "method": "state_information_gain",
      "n": 30000,
      "gate_accuracy": 0.8013,
      "unsafe_commit_rate": 0.1987,
      "valid_commit_recall": 1.0,
      "average_probe_cost": 1.7632333333333334
    },
    {
      "condition": "mixed",
      "method": "dqbp",
      "n": 30000,
      "gate_accuracy": 0.8013,
      "unsafe_commit_rate": 0.1987,
      "valid_commit_recall": 1.0,
      "average_probe_cost": 1.7492
    },
    {
      "condition": "mixed",
      "method": "pdeo",
      "n": 30000,
      "gate_accuracy": 1.0,
      "unsafe_commit_rate": 0.0,
      "valid_commit_recall": 1.0,
      "average_probe_cost": 3.0
    },
    {
      "condition": "mixed",
      "method": "full_readback",
      "n": 30000,
      "gate_accuracy": 1.0,
      "unsafe_commit_rate": 0.0,
      "valid_commit_recall": 1.0,
      "average_probe_cost": 6.0
    },
    {
      "condition": "mixed",
      "method": "human_minimal_obligations",
      "n": 30000,
      "gate_accuracy": 1.0,
      "unsafe_commit_rate": 0.0,
      "valid_commit_recall": 1.0,
      "average_probe_cost": 3.0
    }
  ],
  "resource_usage": {
    "tokens": 0,
    "api_calls": 0,
    "wall_time_seconds": 67.89845809999997,
    "gpu_time_seconds": 0,
    "estimated_cost": 0
  },
  "warnings": [
    "Controller-isolation experiment over typed plans; natural-language plan extraction is not evaluated."
  ]
}

## 6. Reproducibility Facts

### Source: `experiment_v001/attempts/attempt-pdeo-formal-002/dependencies.txt`

annotated-doc==0.0.4
anyio==4.14.2
certifi==2026.6.17
click==8.4.2
colorama==0.4.6
filelock==3.29.0
fsspec==2026.4.0
h11==0.16.0
hf-xet==1.5.2
httpcore==1.0.9
httpx==0.28.1
huggingface_hub==1.24.0
idna==3.18
iniconfig==2.3.0
Jinja2==3.1.6
joblib==1.5.3
markdown-it-py==4.2.0
MarkupSafe==3.0.3
mdurl==0.1.2
mpmath==1.3.0
narwhals==2.24.0
networkx==3.6.1
numpy==2.3.5
packaging==26.0
pluggy==1.6.0
Pygments==2.20.0
pymupdf==1.28.0
pytest==9.1.1
PyYAML==6.0.3
regex==2026.7.19
rich==15.0.0
safetensors==0.8.0
scikit-learn==1.9.0
scipy==1.16.0
sentence-transformers==5.6.0
setuptools==78.1.0
shellingham==1.5.4
sympy==1.14.0
threadpoolctl==3.6.0
tokenizers==0.22.2
torch==2.12.0+cu130
tqdm==4.69.0
transformers==5.14.1
typer==0.27.0
typing_extensions==4.15.0
wheel==0.47.0

### Source: `experiment_v001/attempts/attempt-pdeo-formal-002/formal-details.json`

{
  "schema_version": 1,
  "experiment_id": "pdeo-systematic-fault-suite-v1",
  "adaptive_budget": 3,
  "case_count": 171,
  "compiler_matches_independent_rules": {
    "reservation": true,
    "access_control": true,
    "inventory": true
  },
  "cases_by_split": {
    "known_branches": 24,
    "paired_obligation_and_nuisance_faults": 36,
    "systematic_nuisance_variants": 63,
    "systematic_obligation_faults": 48
  },
  "rows": [
    {
      "case_id": "reservation-correct_receipt_synced-0000",
      "domain": "reservation",
      "split": "known_branches",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "reservation-correct_receipt_synced-0000",
      "domain": "reservation",
      "split": "known_branches",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "reservation-correct_receipt_synced-0000",
      "domain": "reservation",
      "split": "known_branches",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_synced-0000",
      "domain": "reservation",
      "split": "known_branches",
      "method": "tool_local_contract",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_synced-0000",
      "domain": "reservation",
      "split": "known_branches",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "receipt_state",
        "payment_state"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_synced-0000",
      "domain": "reservation",
      "split": "known_branches",
      "method": "dqbp",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "payment_state"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_synced-0000",
      "domain": "reservation",
      "split": "known_branches",
      "method": "pdeo",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_synced-0000",
      "domain": "reservation",
      "split": "known_branches",
      "method": "full_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_status",
        "payment_state",
        "other_booking",
        "receipt_state",
        "audit_event"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_synced-0000",
      "domain": "reservation",
      "split": "known_branches",
      "method": "human_minimal_obligations",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_pending-0001",
      "domain": "reservation",
      "split": "known_branches",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "reservation-correct_receipt_pending-0001",
      "domain": "reservation",
      "split": "known_branches",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "reservation-correct_receipt_pending-0001",
      "domain": "reservation",
      "split": "known_branches",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_pending-0001",
      "domain": "reservation",
      "split": "known_branches",
      "method": "tool_local_contract",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_pending-0001",
      "domain": "reservation",
      "split": "known_branches",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "receipt_state",
        "payment_state"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_pending-0001",
      "domain": "reservation",
      "split": "known_branches",
      "method": "dqbp",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "payment_state"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_pending-0001",
      "domain": "reservation",
      "split": "known_branches",
      "method": "pdeo",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_pending-0001",
      "domain": "reservation",
      "split": "known_branches",
      "method": "full_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_status",
        "payment_state",
        "other_booking",
        "receipt_state",
        "audit_event"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_pending-0001",
      "domain": "reservation",
      "split": "known_branches",
      "method": "human_minimal_obligations",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_external-0002",
      "domain": "reservation",
      "split": "known_branches",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "reservation-correct_receipt_external-0002",
      "domain": "reservation",
      "split": "known_branches",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "reservation-correct_receipt_external-0002",
      "domain": "reservation",
      "split": "known_branches",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_external-0002",
      "domain": "reservation",
      "split": "known_branches",
      "method": "tool_local_contract",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_external-0002",
      "domain": "reservation",
      "split": "known_branches",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "receipt_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_external-0002",
      "domain": "reservation",
      "split": "known_branches",
      "method": "dqbp",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "payment_state"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_external-0002",
      "domain": "reservation",
      "split": "known_branches",
      "method": "pdeo",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_external-0002",
      "domain": "reservation",
      "split": "known_branches",
      "method": "full_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_status",
        "payment_state",
        "other_booking",
        "receipt_state",
        "audit_event"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_external-0002",
      "domain": "reservation",
      "split": "known_branches",
      "method": "human_minimal_obligations",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_suppressed-0003",
      "domain": "reservation",
      "split": "known_branches",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "reservation-correct_receipt_suppressed-0003",
      "domain": "reservation",
      "split": "known_branches",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "reservation-correct_receipt_suppressed-0003",
      "domain": "reservation",
      "split": "known_branches",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_suppressed-0003",
      "domain": "reservation",
      "split": "known_branches",
      "method": "tool_local_contract",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_suppressed-0003",
      "domain": "reservation",
      "split": "known_branches",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "receipt_state"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_suppressed-0003",
      "domain": "reservation",
      "split": "known_branches",
      "method": "dqbp",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "payment_state"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_suppressed-0003",
      "domain": "reservation",
      "split": "known_branches",
      "method": "pdeo",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_suppressed-0003",
      "domain": "reservation",
      "split": "known_branches",
      "method": "full_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_status",
        "payment_state",
        "other_booking",
        "receipt_state",
        "audit_event"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_suppressed-0003",
      "domain": "reservation",
      "split": "known_branches",
      "method": "human_minimal_obligations",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-silent_noop-0004",
      "domain": "reservation",
      "split": "known_branches",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "reservation-silent_noop-0004",
      "domain": "reservation",
      "split": "known_branches",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "reservation-silent_noop-0004",
      "domain": "reservation",
      "split": "known_branches",
      "method": "fixed_target_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_status"
      ]
    },
    {
      "case_id": "reservation-silent_noop-0004",
      "domain": "reservation",
      "split": "known_branches",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-silent_noop-0004",
      "domain": "reservation",
      "split": "known_branches",
      "method": "state_information_gain",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "receipt_state"
      ]
    },
    {
      "case_id": "reservation-silent_noop-0004",
      "domain": "reservation",
      "split": "known_branches",
      "method": "dqbp",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "payment_state",
        "receipt_state"
      ]
    },
    {
      "case_id": "reservation-silent_noop-0004",
      "domain": "reservation",
      "split": "known_branches",
      "method": "pdeo",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-silent_noop-0004",
      "domain": "reservation",
      "split": "known_branches",
      "method": "full_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_status",
        "payment_state",
        "other_booking",
        "receipt_state",
        "audit_event"
      ]
    },
    {
      "case_id": "reservation-silent_noop-0004",
      "domain": "reservation",
      "split": "known_branches",
      "method": "human_minimal_obligations",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-payment_partial-0005",
      "domain": "reservation",
      "split": "known_branches",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "reservation-payment_partial-0005",
      "domain": "reservation",
      "split": "known_branches",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "reservation-payment_partial-0005",
      "domain": "reservation",
      "split": "known_branches",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 1,
      "probes": [
        "target_status"
      ]
    },
    {
      "case_id": "reservation-payment_partial-0005",
      "domain": "reservation",
      "split": "known_branches",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-payment_partial-0005",
      "domain": "reservation",
      "split": "known_branches",
      "method": "state_information_gain",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "receipt_state",
        "payment_state"
      ]
    },
    {
      "case_id": "reservation-payment_partial-0005",
      "domain": "reservation",
      "split": "known_branches",
      "method": "dqbp",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "payment_state",
        "receipt_state"
      ]
    },
    {
      "case_id": "reservation-payment_partial-0005",
      "domain": "reservation",
      "split": "known_branches",
      "method": "pdeo",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-payment_partial-0005",
      "domain": "reservation",
      "split": "known_branches",
      "method": "full_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_status",
        "payment_state",
        "other_booking",
        "receipt_state",
        "audit_event"
      ]
    },
    {
      "case_id": "reservation-payment_partial-0005",
      "domain": "reservation",
      "split": "known_branches",
      "method": "human_minimal_obligations",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-wrong_booking-0006",
      "domain": "reservation",
      "split": "known_branches",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "reservation-wrong_booking-0006",
      "domain": "reservation",
      "split": "known_branches",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "reservation-wrong_booking-0006",
      "domain": "reservation",
      "split": "known_branches",
      "method": "fixed_target_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_status"
      ]
    },
    {
      "case_id": "reservation-wrong_booking-0006",
      "domain": "reservation",
      "split": "known_branches",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-wrong_booking-0006",
      "domain": "reservation",
      "split": "known_branches",
      "method": "state_information_gain",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "receipt_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-wrong_booking-0006",
      "domain": "reservation",
      "split": "known_branches",
      "method": "dqbp",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "payment_state",
        "receipt_state"
      ]
    },
    {
      "case_id": "reservation-wrong_booking-0006",
      "domain": "reservation",
      "split": "known_branches",
      "method": "pdeo",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-wrong_booking-0006",
      "domain": "reservation",
      "split": "known_branches",
      "method": "full_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_status",
        "payment_state",
        "other_booking",
        "receipt_state",
        "audit_event"
      ]
    },
    {
      "case_id": "reservation-wrong_booking-0006",
      "domain": "reservation",
      "split": "known_branches",
      "method": "human_minimal_obligations",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-double_capture-0007",
      "domain": "reservation",
      "split": "known_branches",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "reservation-double_capture-0007",
      "domain": "reservation",
      "split": "known_branches",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "reservation-double_capture-0007",
      "domain": "reservation",
      "split": "known_branches",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 1,
      "probes": [
        "target_status"
      ]
    },
    {
      "case_id": "reservation-double_capture-0007",
      "domain": "reservation",
      "split": "known_branches",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-double_capture-0007",
      "domain": "reservation",
      "split": "known_branches",
      "method": "state_information_gain",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "receipt_state",
        "payment_state"
      ]
    },
    {
      "case_id": "reservation-double_capture-0007",
      "domain": "reservation",
      "split": "known_branches",
      "method": "dqbp",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "payment_state"
      ]
    },
    {
      "case_id": "reservation-double_capture-0007",
      "domain": "reservation",
      "split": "known_branches",
      "method": "pdeo",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-double_capture-0007",
      "domain": "reservation",
      "split": "known_branches",
      "method": "full_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_status",
        "payment_state",
        "other_booking",
        "receipt_state",
        "audit_event"
      ]
    },
    {
      "case_id": "reservation-double_capture-0007",
      "domain": "reservation",
      "split": "known_branches",
      "method": "human_minimal_obligations",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_synced-target_status-PENDING-0008",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "reservation-correct_receipt_synced-target_status-PENDING-0008",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "reservation-correct_receipt_synced-target_status-PENDING-0008",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "fixed_target_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_synced-target_status-PENDING-0008",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_synced-target_status-PENDING-0008",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 2,
      "probes": [
        "receipt_state",
        "payment_state"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_synced-target_status-PENDING-0008",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "dqbp",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 1,
      "probes": [
        "payment_state"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_synced-target_status-PENDING-0008",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "pdeo",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_synced-target_status-PENDING-0008",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "full_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_status",
        "payment_state",
        "other_booking",
        "receipt_state",
        "audit_event"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_synced-target_status-PENDING-0008",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "human_minimal_obligations",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_synced-payment_state-DOUBLE_CAPTURED-0009",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "reservation-correct_receipt_synced-payment_state-DOUBLE_CAPTURED-0009",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "reservation-correct_receipt_synced-payment_state-DOUBLE_CAPTURED-0009",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 1,
      "probes": [
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_synced-payment_state-DOUBLE_CAPTURED-0009",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_synced-payment_state-DOUBLE_CAPTURED-0009",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "state_information_gain",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "receipt_state",
        "payment_state"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_synced-payment_state-DOUBLE_CAPTURED-0009",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "dqbp",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "payment_state"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_synced-payment_state-DOUBLE_CAPTURED-0009",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "pdeo",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_synced-payment_state-DOUBLE_CAPTURED-0009",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "full_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_status",
        "payment_state",
        "other_booking",
        "receipt_state",
        "audit_event"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_synced-payment_state-DOUBLE_CAPTURED-0009",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "human_minimal_obligations",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_synced-payment_state-PENDING-0010",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "reservation-correct_receipt_synced-payment_state-PENDING-0010",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "reservation-correct_receipt_synced-payment_state-PENDING-0010",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 1,
      "probes": [
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_synced-payment_state-PENDING-0010",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_synced-payment_state-PENDING-0010",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "state_information_gain",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "receipt_state",
        "payment_state"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_synced-payment_state-PENDING-0010",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "dqbp",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "payment_state",
        "receipt_state"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_synced-payment_state-PENDING-0010",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "pdeo",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_synced-payment_state-PENDING-0010",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "full_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_status",
        "payment_state",
        "other_booking",
        "receipt_state",
        "audit_event"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_synced-payment_state-PENDING-0010",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "human_minimal_obligations",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_synced-other_booking-CONFIRMED-0011",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "reservation-correct_receipt_synced-other_booking-CONFIRMED-0011",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "reservation-correct_receipt_synced-other_booking-CONFIRMED-0011",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 1,
      "probes": [
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_synced-other_booking-CONFIRMED-0011",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_synced-other_booking-CONFIRMED-0011",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 2,
      "probes": [
        "receipt_state",
        "payment_state"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_synced-other_booking-CONFIRMED-0011",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "dqbp",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 1,
      "probes": [
        "payment_state"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_synced-other_booking-CONFIRMED-0011",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "pdeo",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_synced-other_booking-CONFIRMED-0011",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "full_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_status",
        "payment_state",
        "other_booking",
        "receipt_state",
        "audit_event"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_synced-other_booking-CONFIRMED-0011",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "human_minimal_obligations",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_synced-audit_event-NO_MUTATION-0012",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "reservation-correct_receipt_synced-audit_event-NO_MUTATION-0012",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "reservation-correct_receipt_synced-audit_event-NO_MUTATION-0012",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_synced-audit_event-NO_MUTATION-0012",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": false,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_synced-audit_event-NO_MUTATION-0012",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "receipt_state",
        "payment_state"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_synced-audit_event-NO_MUTATION-0012",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "dqbp",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "payment_state"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_synced-audit_event-NO_MUTATION-0012",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "pdeo",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_synced-audit_event-NO_MUTATION-0012",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "full_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_status",
        "payment_state",
        "other_booking",
        "receipt_state",
        "audit_event"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_synced-audit_event-NO_MUTATION-0012",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "human_minimal_obligations",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_synced-audit_event-OTHER_CONFIRMED-0013",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "reservation-correct_receipt_synced-audit_event-OTHER_CONFIRMED-0013",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "reservation-correct_receipt_synced-audit_event-OTHER_CONFIRMED-0013",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_synced-audit_event-OTHER_CONFIRMED-0013",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": false,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_synced-audit_event-OTHER_CONFIRMED-0013",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "receipt_state",
        "payment_state"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_synced-audit_event-OTHER_CONFIRMED-0013",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "dqbp",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "payment_state"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_synced-audit_event-OTHER_CONFIRMED-0013",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "pdeo",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_synced-audit_event-OTHER_CONFIRMED-0013",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "full_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_status",
        "payment_state",
        "other_booking",
        "receipt_state",
        "audit_event"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_synced-audit_event-OTHER_CONFIRMED-0013",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "human_minimal_obligations",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_synced-audit_event-TARGET_DOUBLE_CAPTURE-0014",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "reservation-correct_receipt_synced-audit_event-TARGET_DOUBLE_CAPTURE-0014",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "reservation-correct_receipt_synced-audit_event-TARGET_DOUBLE_CAPTURE-0014",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_synced-audit_event-TARGET_DOUBLE_CAPTURE-0014",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": false,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_synced-audit_event-TARGET_DOUBLE_CAPTURE-0014",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "receipt_state",
        "payment_state"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_synced-audit_event-TARGET_DOUBLE_CAPTURE-0014",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "dqbp",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "payment_state"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_synced-audit_event-TARGET_DOUBLE_CAPTURE-0014",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "pdeo",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_synced-audit_event-TARGET_DOUBLE_CAPTURE-0014",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "full_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_status",
        "payment_state",
        "other_booking",
        "receipt_state",
        "audit_event"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_synced-audit_event-TARGET_DOUBLE_CAPTURE-0014",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "human_minimal_obligations",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_synced-audit_event-TARGET_STATUS_ONLY-0015",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "reservation-correct_receipt_synced-audit_event-TARGET_STATUS_ONLY-0015",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "reservation-correct_receipt_synced-audit_event-TARGET_STATUS_ONLY-0015",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_synced-audit_event-TARGET_STATUS_ONLY-0015",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": false,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_synced-audit_event-TARGET_STATUS_ONLY-0015",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "receipt_state",
        "payment_state"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_synced-audit_event-TARGET_STATUS_ONLY-0015",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "dqbp",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "payment_state"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_synced-audit_event-TARGET_STATUS_ONLY-0015",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "pdeo",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_synced-audit_event-TARGET_STATUS_ONLY-0015",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "full_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_status",
        "payment_state",
        "other_booking",
        "receipt_state",
        "audit_event"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_synced-audit_event-TARGET_STATUS_ONLY-0015",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "human_minimal_obligations",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_synced-receipt_state-EXTERNAL-0016",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "reservation-correct_receipt_synced-receipt_state-EXTERNAL-0016",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "reservation-correct_receipt_synced-receipt_state-EXTERNAL-0016",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_synced-receipt_state-EXTERNAL-0016",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "tool_local_contract",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_synced-receipt_state-EXTERNAL-0016",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "receipt_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_synced-receipt_state-EXTERNAL-0016",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "dqbp",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "payment_state"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_synced-receipt_state-EXTERNAL-0016",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "pdeo",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_synced-receipt_state-EXTERNAL-0016",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "full_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_status",
        "payment_state",
        "other_booking",
        "receipt_state",
        "audit_event"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_synced-receipt_state-EXTERNAL-0016",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "human_minimal_obligations",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_synced-receipt_state-NONE-0017",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "reservation-correct_receipt_synced-receipt_state-NONE-0017",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "reservation-correct_receipt_synced-receipt_state-NONE-0017",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_synced-receipt_state-NONE-0017",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "tool_local_contract",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_synced-receipt_state-NONE-0017",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "state_information_gain",
      "selected": "ABSTAIN",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": false,
      "probe_cost": 1,
      "probes": [
        "receipt_state"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_synced-receipt_state-NONE-0017",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "dqbp",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "payment_state"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_synced-receipt_state-NONE-0017",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "pdeo",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_synced-receipt_state-NONE-0017",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "full_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_status",
        "payment_state",
        "other_booking",
        "receipt_state",
        "audit_event"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_synced-receipt_state-NONE-0017",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "human_minimal_obligations",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_synced-receipt_state-PENDING-0018",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "reservation-correct_receipt_synced-receipt_state-PENDING-0018",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "reservation-correct_receipt_synced-receipt_state-PENDING-0018",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_synced-receipt_state-PENDING-0018",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "tool_local_contract",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_synced-receipt_state-PENDING-0018",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "receipt_state",
        "payment_state"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_synced-receipt_state-PENDING-0018",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "dqbp",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "payment_state"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_synced-receipt_state-PENDING-0018",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "pdeo",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_synced-receipt_state-PENDING-0018",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "full_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_status",
        "payment_state",
        "other_booking",
        "receipt_state",
        "audit_event"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_synced-receipt_state-PENDING-0018",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "human_minimal_obligations",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_synced-receipt_state-SUPPRESSED-0019",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "reservation-correct_receipt_synced-receipt_state-SUPPRESSED-0019",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "reservation-correct_receipt_synced-receipt_state-SUPPRESSED-0019",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_synced-receipt_state-SUPPRESSED-0019",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "tool_local_contract",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_synced-receipt_state-SUPPRESSED-0019",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "receipt_state"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_synced-receipt_state-SUPPRESSED-0019",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "dqbp",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "payment_state"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_synced-receipt_state-SUPPRESSED-0019",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "pdeo",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_synced-receipt_state-SUPPRESSED-0019",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "full_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_status",
        "payment_state",
        "other_booking",
        "receipt_state",
        "audit_event"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_synced-receipt_state-SUPPRESSED-0019",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "human_minimal_obligations",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_synced-target_status-paired-0020",
      "domain": "reservation",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "reservation-correct_receipt_synced-target_status-paired-0020",
      "domain": "reservation",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "reservation-correct_receipt_synced-target_status-paired-0020",
      "domain": "reservation",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "fixed_target_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_synced-target_status-paired-0020",
      "domain": "reservation",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_synced-target_status-paired-0020",
      "domain": "reservation",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 2,
      "probes": [
        "receipt_state",
        "payment_state"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_synced-target_status-paired-0020",
      "domain": "reservation",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "dqbp",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 1,
      "probes": [
        "payment_state"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_synced-target_status-paired-0020",
      "domain": "reservation",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "pdeo",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_synced-target_status-paired-0020",
      "domain": "reservation",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "full_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_status",
        "payment_state",
        "other_booking",
        "receipt_state",
        "audit_event"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_synced-target_status-paired-0020",
      "domain": "reservation",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "human_minimal_obligations",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_synced-payment_state-paired-0021",
      "domain": "reservation",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "reservation-correct_receipt_synced-payment_state-paired-0021",
      "domain": "reservation",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "reservation-correct_receipt_synced-payment_state-paired-0021",
      "domain": "reservation",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 1,
      "probes": [
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_synced-payment_state-paired-0021",
      "domain": "reservation",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_synced-payment_state-paired-0021",
      "domain": "reservation",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "state_information_gain",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "receipt_state",
        "payment_state"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_synced-payment_state-paired-0021",
      "domain": "reservation",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "dqbp",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "payment_state"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_synced-payment_state-paired-0021",
      "domain": "reservation",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "pdeo",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_synced-payment_state-paired-0021",
      "domain": "reservation",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "full_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_status",
        "payment_state",
        "other_booking",
        "receipt_state",
        "audit_event"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_synced-payment_state-paired-0021",
      "domain": "reservation",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "human_minimal_obligations",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_synced-other_booking-paired-0022",
      "domain": "reservation",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "reservation-correct_receipt_synced-other_booking-paired-0022",
      "domain": "reservation",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "reservation-correct_receipt_synced-other_booking-paired-0022",
      "domain": "reservation",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 1,
      "probes": [
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_synced-other_booking-paired-0022",
      "domain": "reservation",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_synced-other_booking-paired-0022",
      "domain": "reservation",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 2,
      "probes": [
        "receipt_state",
        "payment_state"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_synced-other_booking-paired-0022",
      "domain": "reservation",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "dqbp",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 1,
      "probes": [
        "payment_state"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_synced-other_booking-paired-0022",
      "domain": "reservation",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "pdeo",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_synced-other_booking-paired-0022",
      "domain": "reservation",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "full_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_status",
        "payment_state",
        "other_booking",
        "receipt_state",
        "audit_event"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_synced-other_booking-paired-0022",
      "domain": "reservation",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "human_minimal_obligations",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_pending-target_status-PENDING-0023",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "reservation-correct_receipt_pending-target_status-PENDING-0023",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "reservation-correct_receipt_pending-target_status-PENDING-0023",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "fixed_target_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_pending-target_status-PENDING-0023",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_pending-target_status-PENDING-0023",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 2,
      "probes": [
        "receipt_state",
        "payment_state"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_pending-target_status-PENDING-0023",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "dqbp",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 1,
      "probes": [
        "payment_state"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_pending-target_status-PENDING-0023",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "pdeo",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_pending-target_status-PENDING-0023",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "full_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_status",
        "payment_state",
        "other_booking",
        "receipt_state",
        "audit_event"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_pending-target_status-PENDING-0023",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "human_minimal_obligations",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_pending-payment_state-DOUBLE_CAPTURED-0024",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "reservation-correct_receipt_pending-payment_state-DOUBLE_CAPTURED-0024",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "reservation-correct_receipt_pending-payment_state-DOUBLE_CAPTURED-0024",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 1,
      "probes": [
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_pending-payment_state-DOUBLE_CAPTURED-0024",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_pending-payment_state-DOUBLE_CAPTURED-0024",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "state_information_gain",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "receipt_state",
        "payment_state"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_pending-payment_state-DOUBLE_CAPTURED-0024",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "dqbp",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "payment_state"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_pending-payment_state-DOUBLE_CAPTURED-0024",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "pdeo",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_pending-payment_state-DOUBLE_CAPTURED-0024",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "full_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_status",
        "payment_state",
        "other_booking",
        "receipt_state",
        "audit_event"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_pending-payment_state-DOUBLE_CAPTURED-0024",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "human_minimal_obligations",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_pending-payment_state-PENDING-0025",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "reservation-correct_receipt_pending-payment_state-PENDING-0025",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "reservation-correct_receipt_pending-payment_state-PENDING-0025",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 1,
      "probes": [
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_pending-payment_state-PENDING-0025",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_pending-payment_state-PENDING-0025",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "state_information_gain",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "receipt_state",
        "payment_state"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_pending-payment_state-PENDING-0025",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "dqbp",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "payment_state",
        "receipt_state"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_pending-payment_state-PENDING-0025",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "pdeo",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_pending-payment_state-PENDING-0025",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "full_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_status",
        "payment_state",
        "other_booking",
        "receipt_state",
        "audit_event"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_pending-payment_state-PENDING-0025",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "human_minimal_obligations",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_pending-other_booking-CONFIRMED-0026",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "reservation-correct_receipt_pending-other_booking-CONFIRMED-0026",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "reservation-correct_receipt_pending-other_booking-CONFIRMED-0026",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 1,
      "probes": [
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_pending-other_booking-CONFIRMED-0026",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_pending-other_booking-CONFIRMED-0026",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 2,
      "probes": [
        "receipt_state",
        "payment_state"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_pending-other_booking-CONFIRMED-0026",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "dqbp",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 1,
      "probes": [
        "payment_state"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_pending-other_booking-CONFIRMED-0026",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "pdeo",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_pending-other_booking-CONFIRMED-0026",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "full_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_status",
        "payment_state",
        "other_booking",
        "receipt_state",
        "audit_event"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_pending-other_booking-CONFIRMED-0026",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "human_minimal_obligations",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_pending-audit_event-NO_MUTATION-0027",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "reservation-correct_receipt_pending-audit_event-NO_MUTATION-0027",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "reservation-correct_receipt_pending-audit_event-NO_MUTATION-0027",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_pending-audit_event-NO_MUTATION-0027",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": false,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_pending-audit_event-NO_MUTATION-0027",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "receipt_state",
        "payment_state"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_pending-audit_event-NO_MUTATION-0027",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "dqbp",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "payment_state"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_pending-audit_event-NO_MUTATION-0027",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "pdeo",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_pending-audit_event-NO_MUTATION-0027",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "full_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_status",
        "payment_state",
        "other_booking",
        "receipt_state",
        "audit_event"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_pending-audit_event-NO_MUTATION-0027",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "human_minimal_obligations",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_pending-audit_event-OTHER_CONFIRMED-0028",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "reservation-correct_receipt_pending-audit_event-OTHER_CONFIRMED-0028",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "reservation-correct_receipt_pending-audit_event-OTHER_CONFIRMED-0028",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_pending-audit_event-OTHER_CONFIRMED-0028",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": false,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_pending-audit_event-OTHER_CONFIRMED-0028",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "receipt_state",
        "payment_state"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_pending-audit_event-OTHER_CONFIRMED-0028",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "dqbp",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "payment_state"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_pending-audit_event-OTHER_CONFIRMED-0028",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "pdeo",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_pending-audit_event-OTHER_CONFIRMED-0028",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "full_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_status",
        "payment_state",
        "other_booking",
        "receipt_state",
        "audit_event"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_pending-audit_event-OTHER_CONFIRMED-0028",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "human_minimal_obligations",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_pending-audit_event-TARGET_DOUBLE_CAPTURE-0029",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "reservation-correct_receipt_pending-audit_event-TARGET_DOUBLE_CAPTURE-0029",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "reservation-correct_receipt_pending-audit_event-TARGET_DOUBLE_CAPTURE-0029",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_pending-audit_event-TARGET_DOUBLE_CAPTURE-0029",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": false,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_pending-audit_event-TARGET_DOUBLE_CAPTURE-0029",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "receipt_state",
        "payment_state"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_pending-audit_event-TARGET_DOUBLE_CAPTURE-0029",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "dqbp",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "payment_state"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_pending-audit_event-TARGET_DOUBLE_CAPTURE-0029",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "pdeo",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_pending-audit_event-TARGET_DOUBLE_CAPTURE-0029",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "full_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_status",
        "payment_state",
        "other_booking",
        "receipt_state",
        "audit_event"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_pending-audit_event-TARGET_DOUBLE_CAPTURE-0029",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "human_minimal_obligations",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_pending-audit_event-TARGET_STATUS_ONLY-0030",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "reservation-correct_receipt_pending-audit_event-TARGET_STATUS_ONLY-0030",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "reservation-correct_receipt_pending-audit_event-TARGET_STATUS_ONLY-0030",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_pending-audit_event-TARGET_STATUS_ONLY-0030",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": false,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_pending-audit_event-TARGET_STATUS_ONLY-0030",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "receipt_state",
        "payment_state"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_pending-audit_event-TARGET_STATUS_ONLY-0030",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "dqbp",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "payment_state"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_pending-audit_event-TARGET_STATUS_ONLY-0030",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "pdeo",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_pending-audit_event-TARGET_STATUS_ONLY-0030",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "full_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_status",
        "payment_state",
        "other_booking",
        "receipt_state",
        "audit_event"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_pending-audit_event-TARGET_STATUS_ONLY-0030",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "human_minimal_obligations",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_pending-receipt_state-SYNCED-0031",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "reservation-correct_receipt_pending-receipt_state-SYNCED-0031",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "reservation-correct_receipt_pending-receipt_state-SYNCED-0031",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_pending-receipt_state-SYNCED-0031",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "tool_local_contract",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_pending-receipt_state-SYNCED-0031",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "receipt_state",
        "payment_state"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_pending-receipt_state-SYNCED-0031",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "dqbp",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "payment_state"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_pending-receipt_state-SYNCED-0031",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "pdeo",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_pending-receipt_state-SYNCED-0031",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "full_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_status",
        "payment_state",
        "other_booking",
        "receipt_state",
        "audit_event"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_pending-receipt_state-SYNCED-0031",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "human_minimal_obligations",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_pending-target_status-paired-0032",
      "domain": "reservation",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "reservation-correct_receipt_pending-target_status-paired-0032",
      "domain": "reservation",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "reservation-correct_receipt_pending-target_status-paired-0032",
      "domain": "reservation",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "fixed_target_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_pending-target_status-paired-0032",
      "domain": "reservation",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_pending-target_status-paired-0032",
      "domain": "reservation",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 2,
      "probes": [
        "receipt_state",
        "payment_state"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_pending-target_status-paired-0032",
      "domain": "reservation",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "dqbp",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 1,
      "probes": [
        "payment_state"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_pending-target_status-paired-0032",
      "domain": "reservation",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "pdeo",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_pending-target_status-paired-0032",
      "domain": "reservation",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "full_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_status",
        "payment_state",
        "other_booking",
        "receipt_state",
        "audit_event"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_pending-target_status-paired-0032",
      "domain": "reservation",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "human_minimal_obligations",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_pending-payment_state-paired-0033",
      "domain": "reservation",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "reservation-correct_receipt_pending-payment_state-paired-0033",
      "domain": "reservation",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "reservation-correct_receipt_pending-payment_state-paired-0033",
      "domain": "reservation",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 1,
      "probes": [
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_pending-payment_state-paired-0033",
      "domain": "reservation",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_pending-payment_state-paired-0033",
      "domain": "reservation",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "state_information_gain",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "receipt_state",
        "payment_state"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_pending-payment_state-paired-0033",
      "domain": "reservation",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "dqbp",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "payment_state"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_pending-payment_state-paired-0033",
      "domain": "reservation",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "pdeo",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_pending-payment_state-paired-0033",
      "domain": "reservation",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "full_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_status",
        "payment_state",
        "other_booking",
        "receipt_state",
        "audit_event"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_pending-payment_state-paired-0033",
      "domain": "reservation",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "human_minimal_obligations",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_pending-other_booking-paired-0034",
      "domain": "reservation",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "reservation-correct_receipt_pending-other_booking-paired-0034",
      "domain": "reservation",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "reservation-correct_receipt_pending-other_booking-paired-0034",
      "domain": "reservation",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 1,
      "probes": [
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_pending-other_booking-paired-0034",
      "domain": "reservation",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_pending-other_booking-paired-0034",
      "domain": "reservation",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 2,
      "probes": [
        "receipt_state",
        "payment_state"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_pending-other_booking-paired-0034",
      "domain": "reservation",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "dqbp",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 1,
      "probes": [
        "payment_state"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_pending-other_booking-paired-0034",
      "domain": "reservation",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "pdeo",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_pending-other_booking-paired-0034",
      "domain": "reservation",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "full_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_status",
        "payment_state",
        "other_booking",
        "receipt_state",
        "audit_event"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_pending-other_booking-paired-0034",
      "domain": "reservation",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "human_minimal_obligations",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_external-target_status-PENDING-0035",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "reservation-correct_receipt_external-target_status-PENDING-0035",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "reservation-correct_receipt_external-target_status-PENDING-0035",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "fixed_target_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_external-target_status-PENDING-0035",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_external-target_status-PENDING-0035",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "state_information_gain",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "receipt_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_external-target_status-PENDING-0035",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "dqbp",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 1,
      "probes": [
        "payment_state"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_external-target_status-PENDING-0035",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "pdeo",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_external-target_status-PENDING-0035",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "full_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_status",
        "payment_state",
        "other_booking",
        "receipt_state",
        "audit_event"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_external-target_status-PENDING-0035",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "human_minimal_obligations",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_external-payment_state-DOUBLE_CAPTURED-0036",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "reservation-correct_receipt_external-payment_state-DOUBLE_CAPTURED-0036",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "reservation-correct_receipt_external-payment_state-DOUBLE_CAPTURED-0036",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 1,
      "probes": [
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_external-payment_state-DOUBLE_CAPTURED-0036",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_external-payment_state-DOUBLE_CAPTURED-0036",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 2,
      "probes": [
        "receipt_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_external-payment_state-DOUBLE_CAPTURED-0036",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "dqbp",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "payment_state"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_external-payment_state-DOUBLE_CAPTURED-0036",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "pdeo",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_external-payment_state-DOUBLE_CAPTURED-0036",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "full_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_status",
        "payment_state",
        "other_booking",
        "receipt_state",
        "audit_event"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_external-payment_state-DOUBLE_CAPTURED-0036",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "human_minimal_obligations",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_external-payment_state-PENDING-0037",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "reservation-correct_receipt_external-payment_state-PENDING-0037",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "reservation-correct_receipt_external-payment_state-PENDING-0037",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 1,
      "probes": [
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_external-payment_state-PENDING-0037",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_external-payment_state-PENDING-0037",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 2,
      "probes": [
        "receipt_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_external-payment_state-PENDING-0037",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "dqbp",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "payment_state",
        "receipt_state"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_external-payment_state-PENDING-0037",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "pdeo",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_external-payment_state-PENDING-0037",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "full_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_status",
        "payment_state",
        "other_booking",
        "receipt_state",
        "audit_event"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_external-payment_state-PENDING-0037",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "human_minimal_obligations",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_external-other_booking-CONFIRMED-0038",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "reservation-correct_receipt_external-other_booking-CONFIRMED-0038",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "reservation-correct_receipt_external-other_booking-CONFIRMED-0038",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 1,
      "probes": [
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_external-other_booking-CONFIRMED-0038",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_external-other_booking-CONFIRMED-0038",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 2,
      "probes": [
        "receipt_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_external-other_booking-CONFIRMED-0038",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "dqbp",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 1,
      "probes": [
        "payment_state"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_external-other_booking-CONFIRMED-0038",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "pdeo",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_external-other_booking-CONFIRMED-0038",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "full_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_status",
        "payment_state",
        "other_booking",
        "receipt_state",
        "audit_event"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_external-other_booking-CONFIRMED-0038",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "human_minimal_obligations",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_external-audit_event-NO_MUTATION-0039",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "reservation-correct_receipt_external-audit_event-NO_MUTATION-0039",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "reservation-correct_receipt_external-audit_event-NO_MUTATION-0039",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_external-audit_event-NO_MUTATION-0039",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": false,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_external-audit_event-NO_MUTATION-0039",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "receipt_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_external-audit_event-NO_MUTATION-0039",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "dqbp",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "payment_state"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_external-audit_event-NO_MUTATION-0039",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "pdeo",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_external-audit_event-NO_MUTATION-0039",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "full_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_status",
        "payment_state",
        "other_booking",
        "receipt_state",
        "audit_event"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_external-audit_event-NO_MUTATION-0039",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "human_minimal_obligations",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_external-audit_event-OTHER_CONFIRMED-0040",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "reservation-correct_receipt_external-audit_event-OTHER_CONFIRMED-0040",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "reservation-correct_receipt_external-audit_event-OTHER_CONFIRMED-0040",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_external-audit_event-OTHER_CONFIRMED-0040",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": false,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_external-audit_event-OTHER_CONFIRMED-0040",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "receipt_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_external-audit_event-OTHER_CONFIRMED-0040",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "dqbp",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "payment_state"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_external-audit_event-OTHER_CONFIRMED-0040",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "pdeo",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_external-audit_event-OTHER_CONFIRMED-0040",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "full_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_status",
        "payment_state",
        "other_booking",
        "receipt_state",
        "audit_event"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_external-audit_event-OTHER_CONFIRMED-0040",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "human_minimal_obligations",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_external-audit_event-TARGET_DOUBLE_CAPTURE-0041",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "reservation-correct_receipt_external-audit_event-TARGET_DOUBLE_CAPTURE-0041",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "reservation-correct_receipt_external-audit_event-TARGET_DOUBLE_CAPTURE-0041",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_external-audit_event-TARGET_DOUBLE_CAPTURE-0041",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": false,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_external-audit_event-TARGET_DOUBLE_CAPTURE-0041",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "receipt_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_external-audit_event-TARGET_DOUBLE_CAPTURE-0041",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "dqbp",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "payment_state"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_external-audit_event-TARGET_DOUBLE_CAPTURE-0041",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "pdeo",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_external-audit_event-TARGET_DOUBLE_CAPTURE-0041",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "full_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_status",
        "payment_state",
        "other_booking",
        "receipt_state",
        "audit_event"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_external-audit_event-TARGET_DOUBLE_CAPTURE-0041",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "human_minimal_obligations",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_external-audit_event-TARGET_STATUS_ONLY-0042",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "reservation-correct_receipt_external-audit_event-TARGET_STATUS_ONLY-0042",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "reservation-correct_receipt_external-audit_event-TARGET_STATUS_ONLY-0042",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_external-audit_event-TARGET_STATUS_ONLY-0042",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": false,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_external-audit_event-TARGET_STATUS_ONLY-0042",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "receipt_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_external-audit_event-TARGET_STATUS_ONLY-0042",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "dqbp",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "payment_state"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_external-audit_event-TARGET_STATUS_ONLY-0042",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "pdeo",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_external-audit_event-TARGET_STATUS_ONLY-0042",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "full_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_status",
        "payment_state",
        "other_booking",
        "receipt_state",
        "audit_event"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_external-audit_event-TARGET_STATUS_ONLY-0042",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "human_minimal_obligations",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_external-target_status-paired-0043",
      "domain": "reservation",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "reservation-correct_receipt_external-target_status-paired-0043",
      "domain": "reservation",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "reservation-correct_receipt_external-target_status-paired-0043",
      "domain": "reservation",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "fixed_target_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_external-target_status-paired-0043",
      "domain": "reservation",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_external-target_status-paired-0043",
      "domain": "reservation",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "state_information_gain",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "receipt_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_external-target_status-paired-0043",
      "domain": "reservation",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "dqbp",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 1,
      "probes": [
        "payment_state"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_external-target_status-paired-0043",
      "domain": "reservation",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "pdeo",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_external-target_status-paired-0043",
      "domain": "reservation",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "full_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_status",
        "payment_state",
        "other_booking",
        "receipt_state",
        "audit_event"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_external-target_status-paired-0043",
      "domain": "reservation",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "human_minimal_obligations",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_external-payment_state-paired-0044",
      "domain": "reservation",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "reservation-correct_receipt_external-payment_state-paired-0044",
      "domain": "reservation",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "reservation-correct_receipt_external-payment_state-paired-0044",
      "domain": "reservation",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 1,
      "probes": [
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_external-payment_state-paired-0044",
      "domain": "reservation",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_external-payment_state-paired-0044",
      "domain": "reservation",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 2,
      "probes": [
        "receipt_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_external-payment_state-paired-0044",
      "domain": "reservation",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "dqbp",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "payment_state"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_external-payment_state-paired-0044",
      "domain": "reservation",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "pdeo",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_external-payment_state-paired-0044",
      "domain": "reservation",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "full_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_status",
        "payment_state",
        "other_booking",
        "receipt_state",
        "audit_event"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_external-payment_state-paired-0044",
      "domain": "reservation",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "human_minimal_obligations",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_external-other_booking-paired-0045",
      "domain": "reservation",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "reservation-correct_receipt_external-other_booking-paired-0045",
      "domain": "reservation",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "reservation-correct_receipt_external-other_booking-paired-0045",
      "domain": "reservation",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 1,
      "probes": [
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_external-other_booking-paired-0045",
      "domain": "reservation",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_external-other_booking-paired-0045",
      "domain": "reservation",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 2,
      "probes": [
        "receipt_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_external-other_booking-paired-0045",
      "domain": "reservation",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "dqbp",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 1,
      "probes": [
        "payment_state"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_external-other_booking-paired-0045",
      "domain": "reservation",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "pdeo",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_external-other_booking-paired-0045",
      "domain": "reservation",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "full_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_status",
        "payment_state",
        "other_booking",
        "receipt_state",
        "audit_event"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_external-other_booking-paired-0045",
      "domain": "reservation",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "human_minimal_obligations",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_suppressed-target_status-PENDING-0046",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "reservation-correct_receipt_suppressed-target_status-PENDING-0046",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "reservation-correct_receipt_suppressed-target_status-PENDING-0046",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "fixed_target_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_suppressed-target_status-PENDING-0046",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_suppressed-target_status-PENDING-0046",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 1,
      "probes": [
        "receipt_state"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_suppressed-target_status-PENDING-0046",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "dqbp",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 1,
      "probes": [
        "payment_state"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_suppressed-target_status-PENDING-0046",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "pdeo",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_suppressed-target_status-PENDING-0046",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "full_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_status",
        "payment_state",
        "other_booking",
        "receipt_state",
        "audit_event"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_suppressed-target_status-PENDING-0046",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "human_minimal_obligations",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_suppressed-payment_state-DOUBLE_CAPTURED-0047",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "reservation-correct_receipt_suppressed-payment_state-DOUBLE_CAPTURED-0047",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "reservation-correct_receipt_suppressed-payment_state-DOUBLE_CAPTURED-0047",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 1,
      "probes": [
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_suppressed-payment_state-DOUBLE_CAPTURED-0047",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_suppressed-payment_state-DOUBLE_CAPTURED-0047",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 1,
      "probes": [
        "receipt_state"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_suppressed-payment_state-DOUBLE_CAPTURED-0047",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "dqbp",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "payment_state"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_suppressed-payment_state-DOUBLE_CAPTURED-0047",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "pdeo",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_suppressed-payment_state-DOUBLE_CAPTURED-0047",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "full_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_status",
        "payment_state",
        "other_booking",
        "receipt_state",
        "audit_event"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_suppressed-payment_state-DOUBLE_CAPTURED-0047",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "human_minimal_obligations",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_suppressed-payment_state-PENDING-0048",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "reservation-correct_receipt_suppressed-payment_state-PENDING-0048",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "reservation-correct_receipt_suppressed-payment_state-PENDING-0048",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 1,
      "probes": [
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_suppressed-payment_state-PENDING-0048",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_suppressed-payment_state-PENDING-0048",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 1,
      "probes": [
        "receipt_state"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_suppressed-payment_state-PENDING-0048",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "dqbp",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "payment_state",
        "receipt_state"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_suppressed-payment_state-PENDING-0048",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "pdeo",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_suppressed-payment_state-PENDING-0048",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "full_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_status",
        "payment_state",
        "other_booking",
        "receipt_state",
        "audit_event"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_suppressed-payment_state-PENDING-0048",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "human_minimal_obligations",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_suppressed-other_booking-CONFIRMED-0049",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "reservation-correct_receipt_suppressed-other_booking-CONFIRMED-0049",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "reservation-correct_receipt_suppressed-other_booking-CONFIRMED-0049",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 1,
      "probes": [
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_suppressed-other_booking-CONFIRMED-0049",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_suppressed-other_booking-CONFIRMED-0049",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 1,
      "probes": [
        "receipt_state"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_suppressed-other_booking-CONFIRMED-0049",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "dqbp",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 1,
      "probes": [
        "payment_state"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_suppressed-other_booking-CONFIRMED-0049",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "pdeo",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_suppressed-other_booking-CONFIRMED-0049",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "full_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_status",
        "payment_state",
        "other_booking",
        "receipt_state",
        "audit_event"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_suppressed-other_booking-CONFIRMED-0049",
      "domain": "reservation",
      "split": "systematic_obligation_faults",
      "method": "human_minimal_obligations",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_suppressed-audit_event-NO_MUTATION-0050",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "reservation-correct_receipt_suppressed-audit_event-NO_MUTATION-0050",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "reservation-correct_receipt_suppressed-audit_event-NO_MUTATION-0050",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_suppressed-audit_event-NO_MUTATION-0050",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": false,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_suppressed-audit_event-NO_MUTATION-0050",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "receipt_state"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_suppressed-audit_event-NO_MUTATION-0050",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "dqbp",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "payment_state"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_suppressed-audit_event-NO_MUTATION-0050",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "pdeo",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_suppressed-audit_event-NO_MUTATION-0050",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "full_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_status",
        "payment_state",
        "other_booking",
        "receipt_state",
        "audit_event"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_suppressed-audit_event-NO_MUTATION-0050",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "human_minimal_obligations",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_suppressed-audit_event-OTHER_CONFIRMED-0051",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "reservation-correct_receipt_suppressed-audit_event-OTHER_CONFIRMED-0051",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "reservation-correct_receipt_suppressed-audit_event-OTHER_CONFIRMED-0051",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_suppressed-audit_event-OTHER_CONFIRMED-0051",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": false,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_suppressed-audit_event-OTHER_CONFIRMED-0051",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "receipt_state"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_suppressed-audit_event-OTHER_CONFIRMED-0051",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "dqbp",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "payment_state"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_suppressed-audit_event-OTHER_CONFIRMED-0051",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "pdeo",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_suppressed-audit_event-OTHER_CONFIRMED-0051",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "full_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_status",
        "payment_state",
        "other_booking",
        "receipt_state",
        "audit_event"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_suppressed-audit_event-OTHER_CONFIRMED-0051",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "human_minimal_obligations",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_suppressed-audit_event-TARGET_DOUBLE_CAPTURE-0052",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "reservation-correct_receipt_suppressed-audit_event-TARGET_DOUBLE_CAPTURE-0052",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "reservation-correct_receipt_suppressed-audit_event-TARGET_DOUBLE_CAPTURE-0052",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_suppressed-audit_event-TARGET_DOUBLE_CAPTURE-0052",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": false,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_suppressed-audit_event-TARGET_DOUBLE_CAPTURE-0052",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "receipt_state"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_suppressed-audit_event-TARGET_DOUBLE_CAPTURE-0052",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "dqbp",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "payment_state"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_suppressed-audit_event-TARGET_DOUBLE_CAPTURE-0052",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "pdeo",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_suppressed-audit_event-TARGET_DOUBLE_CAPTURE-0052",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "full_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_status",
        "payment_state",
        "other_booking",
        "receipt_state",
        "audit_event"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_suppressed-audit_event-TARGET_DOUBLE_CAPTURE-0052",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "human_minimal_obligations",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_suppressed-audit_event-TARGET_STATUS_ONLY-0053",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "reservation-correct_receipt_suppressed-audit_event-TARGET_STATUS_ONLY-0053",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "reservation-correct_receipt_suppressed-audit_event-TARGET_STATUS_ONLY-0053",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_suppressed-audit_event-TARGET_STATUS_ONLY-0053",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": false,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_suppressed-audit_event-TARGET_STATUS_ONLY-0053",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "receipt_state"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_suppressed-audit_event-TARGET_STATUS_ONLY-0053",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "dqbp",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "payment_state"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_suppressed-audit_event-TARGET_STATUS_ONLY-0053",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "pdeo",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_suppressed-audit_event-TARGET_STATUS_ONLY-0053",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "full_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_status",
        "payment_state",
        "other_booking",
        "receipt_state",
        "audit_event"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_suppressed-audit_event-TARGET_STATUS_ONLY-0053",
      "domain": "reservation",
      "split": "systematic_nuisance_variants",
      "method": "human_minimal_obligations",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_suppressed-target_status-paired-0054",
      "domain": "reservation",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "reservation-correct_receipt_suppressed-target_status-paired-0054",
      "domain": "reservation",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "reservation-correct_receipt_suppressed-target_status-paired-0054",
      "domain": "reservation",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "fixed_target_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_suppressed-target_status-paired-0054",
      "domain": "reservation",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_suppressed-target_status-paired-0054",
      "domain": "reservation",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 1,
      "probes": [
        "receipt_state"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_suppressed-target_status-paired-0054",
      "domain": "reservation",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "dqbp",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 1,
      "probes": [
        "payment_state"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_suppressed-target_status-paired-0054",
      "domain": "reservation",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "pdeo",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_suppressed-target_status-paired-0054",
      "domain": "reservation",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "full_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_status",
        "payment_state",
        "other_booking",
        "receipt_state",
        "audit_event"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_suppressed-target_status-paired-0054",
      "domain": "reservation",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "human_minimal_obligations",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_suppressed-payment_state-paired-0055",
      "domain": "reservation",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "reservation-correct_receipt_suppressed-payment_state-paired-0055",
      "domain": "reservation",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "reservation-correct_receipt_suppressed-payment_state-paired-0055",
      "domain": "reservation",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 1,
      "probes": [
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_suppressed-payment_state-paired-0055",
      "domain": "reservation",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_suppressed-payment_state-paired-0055",
      "domain": "reservation",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 1,
      "probes": [
        "receipt_state"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_suppressed-payment_state-paired-0055",
      "domain": "reservation",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "dqbp",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "payment_state"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_suppressed-payment_state-paired-0055",
      "domain": "reservation",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "pdeo",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_suppressed-payment_state-paired-0055",
      "domain": "reservation",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "full_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_status",
        "payment_state",
        "other_booking",
        "receipt_state",
        "audit_event"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_suppressed-payment_state-paired-0055",
      "domain": "reservation",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "human_minimal_obligations",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_suppressed-other_booking-paired-0056",
      "domain": "reservation",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "reservation-correct_receipt_suppressed-other_booking-paired-0056",
      "domain": "reservation",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "reservation-correct_receipt_suppressed-other_booking-paired-0056",
      "domain": "reservation",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 1,
      "probes": [
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_suppressed-other_booking-paired-0056",
      "domain": "reservation",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_suppressed-other_booking-paired-0056",
      "domain": "reservation",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 1,
      "probes": [
        "receipt_state"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_suppressed-other_booking-paired-0056",
      "domain": "reservation",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "dqbp",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 1,
      "probes": [
        "payment_state"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_suppressed-other_booking-paired-0056",
      "domain": "reservation",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "pdeo",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_suppressed-other_booking-paired-0056",
      "domain": "reservation",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "full_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_status",
        "payment_state",
        "other_booking",
        "receipt_state",
        "audit_event"
      ]
    },
    {
      "case_id": "reservation-correct_receipt_suppressed-other_booking-paired-0056",
      "domain": "reservation",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "human_minimal_obligations",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_booking",
        "payment_state",
        "target_status"
      ]
    },
    {
      "case_id": "access_control-correct_etag_current-0057",
      "domain": "access_control",
      "split": "known_branches",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "access_control-correct_etag_current-0057",
      "domain": "access_control",
      "split": "known_branches",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "access_control-correct_etag_current-0057",
      "domain": "access_control",
      "split": "known_branches",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_current-0057",
      "domain": "access_control",
      "split": "known_branches",
      "method": "tool_local_contract",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_current-0057",
      "domain": "access_control",
      "split": "known_branches",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "etag_state",
        "scope_state"
      ]
    },
    {
      "case_id": "access_control-correct_etag_current-0057",
      "domain": "access_control",
      "split": "known_branches",
      "method": "dqbp",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "audit_event"
      ]
    },
    {
      "case_id": "access_control-correct_etag_current-0057",
      "domain": "access_control",
      "split": "known_branches",
      "method": "pdeo",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_current-0057",
      "domain": "access_control",
      "split": "known_branches",
      "method": "full_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_role",
        "scope_state",
        "other_principal",
        "etag_state",
        "audit_event"
      ]
    },
    {
      "case_id": "access_control-correct_etag_current-0057",
      "domain": "access_control",
      "split": "known_branches",
      "method": "human_minimal_obligations",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_lagged-0058",
      "domain": "access_control",
      "split": "known_branches",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "access_control-correct_etag_lagged-0058",
      "domain": "access_control",
      "split": "known_branches",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "access_control-correct_etag_lagged-0058",
      "domain": "access_control",
      "split": "known_branches",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_lagged-0058",
      "domain": "access_control",
      "split": "known_branches",
      "method": "tool_local_contract",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_lagged-0058",
      "domain": "access_control",
      "split": "known_branches",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "etag_state"
      ]
    },
    {
      "case_id": "access_control-correct_etag_lagged-0058",
      "domain": "access_control",
      "split": "known_branches",
      "method": "dqbp",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "audit_event"
      ]
    },
    {
      "case_id": "access_control-correct_etag_lagged-0058",
      "domain": "access_control",
      "split": "known_branches",
      "method": "pdeo",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_lagged-0058",
      "domain": "access_control",
      "split": "known_branches",
      "method": "full_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_role",
        "scope_state",
        "other_principal",
        "etag_state",
        "audit_event"
      ]
    },
    {
      "case_id": "access_control-correct_etag_lagged-0058",
      "domain": "access_control",
      "split": "known_branches",
      "method": "human_minimal_obligations",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_rotated-0059",
      "domain": "access_control",
      "split": "known_branches",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "access_control-correct_etag_rotated-0059",
      "domain": "access_control",
      "split": "known_branches",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "access_control-correct_etag_rotated-0059",
      "domain": "access_control",
      "split": "known_branches",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_rotated-0059",
      "domain": "access_control",
      "split": "known_branches",
      "method": "tool_local_contract",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_rotated-0059",
      "domain": "access_control",
      "split": "known_branches",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "etag_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_rotated-0059",
      "domain": "access_control",
      "split": "known_branches",
      "method": "dqbp",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "audit_event"
      ]
    },
    {
      "case_id": "access_control-correct_etag_rotated-0059",
      "domain": "access_control",
      "split": "known_branches",
      "method": "pdeo",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_rotated-0059",
      "domain": "access_control",
      "split": "known_branches",
      "method": "full_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_role",
        "scope_state",
        "other_principal",
        "etag_state",
        "audit_event"
      ]
    },
    {
      "case_id": "access_control-correct_etag_rotated-0059",
      "domain": "access_control",
      "split": "known_branches",
      "method": "human_minimal_obligations",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_hidden-0060",
      "domain": "access_control",
      "split": "known_branches",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "access_control-correct_etag_hidden-0060",
      "domain": "access_control",
      "split": "known_branches",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "access_control-correct_etag_hidden-0060",
      "domain": "access_control",
      "split": "known_branches",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_hidden-0060",
      "domain": "access_control",
      "split": "known_branches",
      "method": "tool_local_contract",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_hidden-0060",
      "domain": "access_control",
      "split": "known_branches",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "etag_state"
      ]
    },
    {
      "case_id": "access_control-correct_etag_hidden-0060",
      "domain": "access_control",
      "split": "known_branches",
      "method": "dqbp",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "audit_event"
      ]
    },
    {
      "case_id": "access_control-correct_etag_hidden-0060",
      "domain": "access_control",
      "split": "known_branches",
      "method": "pdeo",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_hidden-0060",
      "domain": "access_control",
      "split": "known_branches",
      "method": "full_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_role",
        "scope_state",
        "other_principal",
        "etag_state",
        "audit_event"
      ]
    },
    {
      "case_id": "access_control-correct_etag_hidden-0060",
      "domain": "access_control",
      "split": "known_branches",
      "method": "human_minimal_obligations",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-silent_noop-0061",
      "domain": "access_control",
      "split": "known_branches",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "access_control-silent_noop-0061",
      "domain": "access_control",
      "split": "known_branches",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "access_control-silent_noop-0061",
      "domain": "access_control",
      "split": "known_branches",
      "method": "fixed_target_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_role"
      ]
    },
    {
      "case_id": "access_control-silent_noop-0061",
      "domain": "access_control",
      "split": "known_branches",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-silent_noop-0061",
      "domain": "access_control",
      "split": "known_branches",
      "method": "state_information_gain",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "etag_state"
      ]
    },
    {
      "case_id": "access_control-silent_noop-0061",
      "domain": "access_control",
      "split": "known_branches",
      "method": "dqbp",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "audit_event"
      ]
    },
    {
      "case_id": "access_control-silent_noop-0061",
      "domain": "access_control",
      "split": "known_branches",
      "method": "pdeo",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-silent_noop-0061",
      "domain": "access_control",
      "split": "known_branches",
      "method": "full_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_role",
        "scope_state",
        "other_principal",
        "etag_state",
        "audit_event"
      ]
    },
    {
      "case_id": "access_control-silent_noop-0061",
      "domain": "access_control",
      "split": "known_branches",
      "method": "human_minimal_obligations",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-scope_partial-0062",
      "domain": "access_control",
      "split": "known_branches",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "access_control-scope_partial-0062",
      "domain": "access_control",
      "split": "known_branches",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "access_control-scope_partial-0062",
      "domain": "access_control",
      "split": "known_branches",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 1,
      "probes": [
        "target_role"
      ]
    },
    {
      "case_id": "access_control-scope_partial-0062",
      "domain": "access_control",
      "split": "known_branches",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-scope_partial-0062",
      "domain": "access_control",
      "split": "known_branches",
      "method": "state_information_gain",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "etag_state",
        "scope_state"
      ]
    },
    {
      "case_id": "access_control-scope_partial-0062",
      "domain": "access_control",
      "split": "known_branches",
      "method": "dqbp",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "audit_event"
      ]
    },
    {
      "case_id": "access_control-scope_partial-0062",
      "domain": "access_control",
      "split": "known_branches",
      "method": "pdeo",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-scope_partial-0062",
      "domain": "access_control",
      "split": "known_branches",
      "method": "full_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_role",
        "scope_state",
        "other_principal",
        "etag_state",
        "audit_event"
      ]
    },
    {
      "case_id": "access_control-scope_partial-0062",
      "domain": "access_control",
      "split": "known_branches",
      "method": "human_minimal_obligations",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-wrong_principal-0063",
      "domain": "access_control",
      "split": "known_branches",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "access_control-wrong_principal-0063",
      "domain": "access_control",
      "split": "known_branches",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "access_control-wrong_principal-0063",
      "domain": "access_control",
      "split": "known_branches",
      "method": "fixed_target_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_role"
      ]
    },
    {
      "case_id": "access_control-wrong_principal-0063",
      "domain": "access_control",
      "split": "known_branches",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-wrong_principal-0063",
      "domain": "access_control",
      "split": "known_branches",
      "method": "state_information_gain",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "etag_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-wrong_principal-0063",
      "domain": "access_control",
      "split": "known_branches",
      "method": "dqbp",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "audit_event"
      ]
    },
    {
      "case_id": "access_control-wrong_principal-0063",
      "domain": "access_control",
      "split": "known_branches",
      "method": "pdeo",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-wrong_principal-0063",
      "domain": "access_control",
      "split": "known_branches",
      "method": "full_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_role",
        "scope_state",
        "other_principal",
        "etag_state",
        "audit_event"
      ]
    },
    {
      "case_id": "access_control-wrong_principal-0063",
      "domain": "access_control",
      "split": "known_branches",
      "method": "human_minimal_obligations",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-duplicate_grant-0064",
      "domain": "access_control",
      "split": "known_branches",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "access_control-duplicate_grant-0064",
      "domain": "access_control",
      "split": "known_branches",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "access_control-duplicate_grant-0064",
      "domain": "access_control",
      "split": "known_branches",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 1,
      "probes": [
        "target_role"
      ]
    },
    {
      "case_id": "access_control-duplicate_grant-0064",
      "domain": "access_control",
      "split": "known_branches",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-duplicate_grant-0064",
      "domain": "access_control",
      "split": "known_branches",
      "method": "state_information_gain",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "etag_state",
        "scope_state"
      ]
    },
    {
      "case_id": "access_control-duplicate_grant-0064",
      "domain": "access_control",
      "split": "known_branches",
      "method": "dqbp",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "audit_event"
      ]
    },
    {
      "case_id": "access_control-duplicate_grant-0064",
      "domain": "access_control",
      "split": "known_branches",
      "method": "pdeo",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-duplicate_grant-0064",
      "domain": "access_control",
      "split": "known_branches",
      "method": "full_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_role",
        "scope_state",
        "other_principal",
        "etag_state",
        "audit_event"
      ]
    },
    {
      "case_id": "access_control-duplicate_grant-0064",
      "domain": "access_control",
      "split": "known_branches",
      "method": "human_minimal_obligations",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_current-target_role-VIEWER-0065",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "access_control-correct_etag_current-target_role-VIEWER-0065",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "access_control-correct_etag_current-target_role-VIEWER-0065",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "fixed_target_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_current-target_role-VIEWER-0065",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_current-target_role-VIEWER-0065",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 2,
      "probes": [
        "etag_state",
        "scope_state"
      ]
    },
    {
      "case_id": "access_control-correct_etag_current-target_role-VIEWER-0065",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "dqbp",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 2,
      "probes": [
        "audit_event"
      ]
    },
    {
      "case_id": "access_control-correct_etag_current-target_role-VIEWER-0065",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "pdeo",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_current-target_role-VIEWER-0065",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "full_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_role",
        "scope_state",
        "other_principal",
        "etag_state",
        "audit_event"
      ]
    },
    {
      "case_id": "access_control-correct_etag_current-target_role-VIEWER-0065",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "human_minimal_obligations",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_current-scope_state-DUPLICATE_BINDING-0066",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "access_control-correct_etag_current-scope_state-DUPLICATE_BINDING-0066",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "access_control-correct_etag_current-scope_state-DUPLICATE_BINDING-0066",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 1,
      "probes": [
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_current-scope_state-DUPLICATE_BINDING-0066",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_current-scope_state-DUPLICATE_BINDING-0066",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "state_information_gain",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "etag_state",
        "scope_state"
      ]
    },
    {
      "case_id": "access_control-correct_etag_current-scope_state-DUPLICATE_BINDING-0066",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "dqbp",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 2,
      "probes": [
        "audit_event"
      ]
    },
    {
      "case_id": "access_control-correct_etag_current-scope_state-DUPLICATE_BINDING-0066",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "pdeo",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_current-scope_state-DUPLICATE_BINDING-0066",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "full_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_role",
        "scope_state",
        "other_principal",
        "etag_state",
        "audit_event"
      ]
    },
    {
      "case_id": "access_control-correct_etag_current-scope_state-DUPLICATE_BINDING-0066",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "human_minimal_obligations",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_current-scope_state-ORGANIZATION_WIDE-0067",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "access_control-correct_etag_current-scope_state-ORGANIZATION_WIDE-0067",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "access_control-correct_etag_current-scope_state-ORGANIZATION_WIDE-0067",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 1,
      "probes": [
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_current-scope_state-ORGANIZATION_WIDE-0067",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_current-scope_state-ORGANIZATION_WIDE-0067",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "state_information_gain",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "etag_state",
        "scope_state"
      ]
    },
    {
      "case_id": "access_control-correct_etag_current-scope_state-ORGANIZATION_WIDE-0067",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "dqbp",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 2,
      "probes": [
        "audit_event"
      ]
    },
    {
      "case_id": "access_control-correct_etag_current-scope_state-ORGANIZATION_WIDE-0067",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "pdeo",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_current-scope_state-ORGANIZATION_WIDE-0067",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "full_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_role",
        "scope_state",
        "other_principal",
        "etag_state",
        "audit_event"
      ]
    },
    {
      "case_id": "access_control-correct_etag_current-scope_state-ORGANIZATION_WIDE-0067",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "human_minimal_obligations",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_current-other_principal-EDITOR-0068",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "access_control-correct_etag_current-other_principal-EDITOR-0068",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "access_control-correct_etag_current-other_principal-EDITOR-0068",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 1,
      "probes": [
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_current-other_principal-EDITOR-0068",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_current-other_principal-EDITOR-0068",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 2,
      "probes": [
        "etag_state",
        "scope_state"
      ]
    },
    {
      "case_id": "access_control-correct_etag_current-other_principal-EDITOR-0068",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "dqbp",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 2,
      "probes": [
        "audit_event"
      ]
    },
    {
      "case_id": "access_control-correct_etag_current-other_principal-EDITOR-0068",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "pdeo",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_current-other_principal-EDITOR-0068",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "full_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_role",
        "scope_state",
        "other_principal",
        "etag_state",
        "audit_event"
      ]
    },
    {
      "case_id": "access_control-correct_etag_current-other_principal-EDITOR-0068",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "human_minimal_obligations",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_current-audit_event-NO_MUTATION-0069",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "access_control-correct_etag_current-audit_event-NO_MUTATION-0069",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "access_control-correct_etag_current-audit_event-NO_MUTATION-0069",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_current-audit_event-NO_MUTATION-0069",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": false,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_current-audit_event-NO_MUTATION-0069",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "etag_state",
        "scope_state"
      ]
    },
    {
      "case_id": "access_control-correct_etag_current-audit_event-NO_MUTATION-0069",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "dqbp",
      "selected": "ABSTAIN",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": false,
      "probe_cost": 2,
      "probes": [
        "audit_event"
      ]
    },
    {
      "case_id": "access_control-correct_etag_current-audit_event-NO_MUTATION-0069",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "pdeo",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_current-audit_event-NO_MUTATION-0069",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "full_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_role",
        "scope_state",
        "other_principal",
        "etag_state",
        "audit_event"
      ]
    },
    {
      "case_id": "access_control-correct_etag_current-audit_event-NO_MUTATION-0069",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "human_minimal_obligations",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_current-audit_event-OTHER_GRANTED-0070",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "access_control-correct_etag_current-audit_event-OTHER_GRANTED-0070",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "access_control-correct_etag_current-audit_event-OTHER_GRANTED-0070",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_current-audit_event-OTHER_GRANTED-0070",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": false,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_current-audit_event-OTHER_GRANTED-0070",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "etag_state",
        "scope_state"
      ]
    },
    {
      "case_id": "access_control-correct_etag_current-audit_event-OTHER_GRANTED-0070",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "dqbp",
      "selected": "ABSTAIN",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": false,
      "probe_cost": 2,
      "probes": [
        "audit_event"
      ]
    },
    {
      "case_id": "access_control-correct_etag_current-audit_event-OTHER_GRANTED-0070",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "pdeo",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_current-audit_event-OTHER_GRANTED-0070",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "full_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_role",
        "scope_state",
        "other_principal",
        "etag_state",
        "audit_event"
      ]
    },
    {
      "case_id": "access_control-correct_etag_current-audit_event-OTHER_GRANTED-0070",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "human_minimal_obligations",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_current-audit_event-TARGET_DUPLICATED-0071",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "access_control-correct_etag_current-audit_event-TARGET_DUPLICATED-0071",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "access_control-correct_etag_current-audit_event-TARGET_DUPLICATED-0071",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_current-audit_event-TARGET_DUPLICATED-0071",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": false,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_current-audit_event-TARGET_DUPLICATED-0071",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "etag_state",
        "scope_state"
      ]
    },
    {
      "case_id": "access_control-correct_etag_current-audit_event-TARGET_DUPLICATED-0071",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "dqbp",
      "selected": "ABSTAIN",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": false,
      "probe_cost": 2,
      "probes": [
        "audit_event"
      ]
    },
    {
      "case_id": "access_control-correct_etag_current-audit_event-TARGET_DUPLICATED-0071",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "pdeo",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_current-audit_event-TARGET_DUPLICATED-0071",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "full_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_role",
        "scope_state",
        "other_principal",
        "etag_state",
        "audit_event"
      ]
    },
    {
      "case_id": "access_control-correct_etag_current-audit_event-TARGET_DUPLICATED-0071",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "human_minimal_obligations",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_current-audit_event-TARGET_OVERBROAD-0072",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "access_control-correct_etag_current-audit_event-TARGET_OVERBROAD-0072",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "access_control-correct_etag_current-audit_event-TARGET_OVERBROAD-0072",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_current-audit_event-TARGET_OVERBROAD-0072",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": false,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_current-audit_event-TARGET_OVERBROAD-0072",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "etag_state",
        "scope_state"
      ]
    },
    {
      "case_id": "access_control-correct_etag_current-audit_event-TARGET_OVERBROAD-0072",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "dqbp",
      "selected": "ABSTAIN",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": false,
      "probe_cost": 2,
      "probes": [
        "audit_event"
      ]
    },
    {
      "case_id": "access_control-correct_etag_current-audit_event-TARGET_OVERBROAD-0072",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "pdeo",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_current-audit_event-TARGET_OVERBROAD-0072",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "full_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_role",
        "scope_state",
        "other_principal",
        "etag_state",
        "audit_event"
      ]
    },
    {
      "case_id": "access_control-correct_etag_current-audit_event-TARGET_OVERBROAD-0072",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "human_minimal_obligations",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_current-etag_state-HIDDEN-0073",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "access_control-correct_etag_current-etag_state-HIDDEN-0073",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "access_control-correct_etag_current-etag_state-HIDDEN-0073",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_current-etag_state-HIDDEN-0073",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "tool_local_contract",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_current-etag_state-HIDDEN-0073",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "etag_state"
      ]
    },
    {
      "case_id": "access_control-correct_etag_current-etag_state-HIDDEN-0073",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "dqbp",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "audit_event"
      ]
    },
    {
      "case_id": "access_control-correct_etag_current-etag_state-HIDDEN-0073",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "pdeo",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_current-etag_state-HIDDEN-0073",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "full_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_role",
        "scope_state",
        "other_principal",
        "etag_state",
        "audit_event"
      ]
    },
    {
      "case_id": "access_control-correct_etag_current-etag_state-HIDDEN-0073",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "human_minimal_obligations",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_current-etag_state-LAGGED-0074",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "access_control-correct_etag_current-etag_state-LAGGED-0074",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "access_control-correct_etag_current-etag_state-LAGGED-0074",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_current-etag_state-LAGGED-0074",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "tool_local_contract",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_current-etag_state-LAGGED-0074",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "etag_state"
      ]
    },
    {
      "case_id": "access_control-correct_etag_current-etag_state-LAGGED-0074",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "dqbp",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "audit_event"
      ]
    },
    {
      "case_id": "access_control-correct_etag_current-etag_state-LAGGED-0074",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "pdeo",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_current-etag_state-LAGGED-0074",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "full_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_role",
        "scope_state",
        "other_principal",
        "etag_state",
        "audit_event"
      ]
    },
    {
      "case_id": "access_control-correct_etag_current-etag_state-LAGGED-0074",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "human_minimal_obligations",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_current-etag_state-ROTATED-0075",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "access_control-correct_etag_current-etag_state-ROTATED-0075",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "access_control-correct_etag_current-etag_state-ROTATED-0075",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_current-etag_state-ROTATED-0075",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "tool_local_contract",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_current-etag_state-ROTATED-0075",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "etag_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_current-etag_state-ROTATED-0075",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "dqbp",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "audit_event"
      ]
    },
    {
      "case_id": "access_control-correct_etag_current-etag_state-ROTATED-0075",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "pdeo",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_current-etag_state-ROTATED-0075",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "full_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_role",
        "scope_state",
        "other_principal",
        "etag_state",
        "audit_event"
      ]
    },
    {
      "case_id": "access_control-correct_etag_current-etag_state-ROTATED-0075",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "human_minimal_obligations",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_current-etag_state-UNCHANGED-0076",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "access_control-correct_etag_current-etag_state-UNCHANGED-0076",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "access_control-correct_etag_current-etag_state-UNCHANGED-0076",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_current-etag_state-UNCHANGED-0076",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "tool_local_contract",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_current-etag_state-UNCHANGED-0076",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "state_information_gain",
      "selected": "ABSTAIN",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": false,
      "probe_cost": 1,
      "probes": [
        "etag_state"
      ]
    },
    {
      "case_id": "access_control-correct_etag_current-etag_state-UNCHANGED-0076",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "dqbp",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "audit_event"
      ]
    },
    {
      "case_id": "access_control-correct_etag_current-etag_state-UNCHANGED-0076",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "pdeo",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_current-etag_state-UNCHANGED-0076",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "full_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_role",
        "scope_state",
        "other_principal",
        "etag_state",
        "audit_event"
      ]
    },
    {
      "case_id": "access_control-correct_etag_current-etag_state-UNCHANGED-0076",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "human_minimal_obligations",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_current-target_role-paired-0077",
      "domain": "access_control",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "access_control-correct_etag_current-target_role-paired-0077",
      "domain": "access_control",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "access_control-correct_etag_current-target_role-paired-0077",
      "domain": "access_control",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "fixed_target_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_current-target_role-paired-0077",
      "domain": "access_control",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_current-target_role-paired-0077",
      "domain": "access_control",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 2,
      "probes": [
        "etag_state",
        "scope_state"
      ]
    },
    {
      "case_id": "access_control-correct_etag_current-target_role-paired-0077",
      "domain": "access_control",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "dqbp",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "audit_event"
      ]
    },
    {
      "case_id": "access_control-correct_etag_current-target_role-paired-0077",
      "domain": "access_control",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "pdeo",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_current-target_role-paired-0077",
      "domain": "access_control",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "full_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_role",
        "scope_state",
        "other_principal",
        "etag_state",
        "audit_event"
      ]
    },
    {
      "case_id": "access_control-correct_etag_current-target_role-paired-0077",
      "domain": "access_control",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "human_minimal_obligations",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_current-scope_state-paired-0078",
      "domain": "access_control",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "access_control-correct_etag_current-scope_state-paired-0078",
      "domain": "access_control",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "access_control-correct_etag_current-scope_state-paired-0078",
      "domain": "access_control",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 1,
      "probes": [
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_current-scope_state-paired-0078",
      "domain": "access_control",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_current-scope_state-paired-0078",
      "domain": "access_control",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "state_information_gain",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "etag_state",
        "scope_state"
      ]
    },
    {
      "case_id": "access_control-correct_etag_current-scope_state-paired-0078",
      "domain": "access_control",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "dqbp",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "audit_event"
      ]
    },
    {
      "case_id": "access_control-correct_etag_current-scope_state-paired-0078",
      "domain": "access_control",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "pdeo",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_current-scope_state-paired-0078",
      "domain": "access_control",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "full_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_role",
        "scope_state",
        "other_principal",
        "etag_state",
        "audit_event"
      ]
    },
    {
      "case_id": "access_control-correct_etag_current-scope_state-paired-0078",
      "domain": "access_control",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "human_minimal_obligations",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_current-other_principal-paired-0079",
      "domain": "access_control",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "access_control-correct_etag_current-other_principal-paired-0079",
      "domain": "access_control",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "access_control-correct_etag_current-other_principal-paired-0079",
      "domain": "access_control",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 1,
      "probes": [
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_current-other_principal-paired-0079",
      "domain": "access_control",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_current-other_principal-paired-0079",
      "domain": "access_control",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 2,
      "probes": [
        "etag_state",
        "scope_state"
      ]
    },
    {
      "case_id": "access_control-correct_etag_current-other_principal-paired-0079",
      "domain": "access_control",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "dqbp",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "audit_event"
      ]
    },
    {
      "case_id": "access_control-correct_etag_current-other_principal-paired-0079",
      "domain": "access_control",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "pdeo",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_current-other_principal-paired-0079",
      "domain": "access_control",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "full_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_role",
        "scope_state",
        "other_principal",
        "etag_state",
        "audit_event"
      ]
    },
    {
      "case_id": "access_control-correct_etag_current-other_principal-paired-0079",
      "domain": "access_control",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "human_minimal_obligations",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_lagged-target_role-VIEWER-0080",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "access_control-correct_etag_lagged-target_role-VIEWER-0080",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "access_control-correct_etag_lagged-target_role-VIEWER-0080",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "fixed_target_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_lagged-target_role-VIEWER-0080",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_lagged-target_role-VIEWER-0080",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 1,
      "probes": [
        "etag_state"
      ]
    },
    {
      "case_id": "access_control-correct_etag_lagged-target_role-VIEWER-0080",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "dqbp",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 2,
      "probes": [
        "audit_event"
      ]
    },
    {
      "case_id": "access_control-correct_etag_lagged-target_role-VIEWER-0080",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "pdeo",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_lagged-target_role-VIEWER-0080",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "full_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_role",
        "scope_state",
        "other_principal",
        "etag_state",
        "audit_event"
      ]
    },
    {
      "case_id": "access_control-correct_etag_lagged-target_role-VIEWER-0080",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "human_minimal_obligations",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_lagged-scope_state-DUPLICATE_BINDING-0081",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "access_control-correct_etag_lagged-scope_state-DUPLICATE_BINDING-0081",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "access_control-correct_etag_lagged-scope_state-DUPLICATE_BINDING-0081",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 1,
      "probes": [
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_lagged-scope_state-DUPLICATE_BINDING-0081",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_lagged-scope_state-DUPLICATE_BINDING-0081",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 1,
      "probes": [
        "etag_state"
      ]
    },
    {
      "case_id": "access_control-correct_etag_lagged-scope_state-DUPLICATE_BINDING-0081",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "dqbp",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 2,
      "probes": [
        "audit_event"
      ]
    },
    {
      "case_id": "access_control-correct_etag_lagged-scope_state-DUPLICATE_BINDING-0081",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "pdeo",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_lagged-scope_state-DUPLICATE_BINDING-0081",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "full_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_role",
        "scope_state",
        "other_principal",
        "etag_state",
        "audit_event"
      ]
    },
    {
      "case_id": "access_control-correct_etag_lagged-scope_state-DUPLICATE_BINDING-0081",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "human_minimal_obligations",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_lagged-scope_state-ORGANIZATION_WIDE-0082",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "access_control-correct_etag_lagged-scope_state-ORGANIZATION_WIDE-0082",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "access_control-correct_etag_lagged-scope_state-ORGANIZATION_WIDE-0082",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 1,
      "probes": [
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_lagged-scope_state-ORGANIZATION_WIDE-0082",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_lagged-scope_state-ORGANIZATION_WIDE-0082",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 1,
      "probes": [
        "etag_state"
      ]
    },
    {
      "case_id": "access_control-correct_etag_lagged-scope_state-ORGANIZATION_WIDE-0082",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "dqbp",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 2,
      "probes": [
        "audit_event"
      ]
    },
    {
      "case_id": "access_control-correct_etag_lagged-scope_state-ORGANIZATION_WIDE-0082",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "pdeo",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_lagged-scope_state-ORGANIZATION_WIDE-0082",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "full_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_role",
        "scope_state",
        "other_principal",
        "etag_state",
        "audit_event"
      ]
    },
    {
      "case_id": "access_control-correct_etag_lagged-scope_state-ORGANIZATION_WIDE-0082",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "human_minimal_obligations",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_lagged-other_principal-EDITOR-0083",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "access_control-correct_etag_lagged-other_principal-EDITOR-0083",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "access_control-correct_etag_lagged-other_principal-EDITOR-0083",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 1,
      "probes": [
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_lagged-other_principal-EDITOR-0083",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_lagged-other_principal-EDITOR-0083",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 1,
      "probes": [
        "etag_state"
      ]
    },
    {
      "case_id": "access_control-correct_etag_lagged-other_principal-EDITOR-0083",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "dqbp",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 2,
      "probes": [
        "audit_event"
      ]
    },
    {
      "case_id": "access_control-correct_etag_lagged-other_principal-EDITOR-0083",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "pdeo",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_lagged-other_principal-EDITOR-0083",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "full_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_role",
        "scope_state",
        "other_principal",
        "etag_state",
        "audit_event"
      ]
    },
    {
      "case_id": "access_control-correct_etag_lagged-other_principal-EDITOR-0083",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "human_minimal_obligations",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_lagged-audit_event-NO_MUTATION-0084",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "access_control-correct_etag_lagged-audit_event-NO_MUTATION-0084",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "access_control-correct_etag_lagged-audit_event-NO_MUTATION-0084",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_lagged-audit_event-NO_MUTATION-0084",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": false,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_lagged-audit_event-NO_MUTATION-0084",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "etag_state"
      ]
    },
    {
      "case_id": "access_control-correct_etag_lagged-audit_event-NO_MUTATION-0084",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "dqbp",
      "selected": "ABSTAIN",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": false,
      "probe_cost": 2,
      "probes": [
        "audit_event"
      ]
    },
    {
      "case_id": "access_control-correct_etag_lagged-audit_event-NO_MUTATION-0084",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "pdeo",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_lagged-audit_event-NO_MUTATION-0084",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "full_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_role",
        "scope_state",
        "other_principal",
        "etag_state",
        "audit_event"
      ]
    },
    {
      "case_id": "access_control-correct_etag_lagged-audit_event-NO_MUTATION-0084",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "human_minimal_obligations",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_lagged-audit_event-OTHER_GRANTED-0085",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "access_control-correct_etag_lagged-audit_event-OTHER_GRANTED-0085",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "access_control-correct_etag_lagged-audit_event-OTHER_GRANTED-0085",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_lagged-audit_event-OTHER_GRANTED-0085",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": false,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_lagged-audit_event-OTHER_GRANTED-0085",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "etag_state"
      ]
    },
    {
      "case_id": "access_control-correct_etag_lagged-audit_event-OTHER_GRANTED-0085",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "dqbp",
      "selected": "ABSTAIN",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": false,
      "probe_cost": 2,
      "probes": [
        "audit_event"
      ]
    },
    {
      "case_id": "access_control-correct_etag_lagged-audit_event-OTHER_GRANTED-0085",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "pdeo",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_lagged-audit_event-OTHER_GRANTED-0085",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "full_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_role",
        "scope_state",
        "other_principal",
        "etag_state",
        "audit_event"
      ]
    },
    {
      "case_id": "access_control-correct_etag_lagged-audit_event-OTHER_GRANTED-0085",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "human_minimal_obligations",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_lagged-audit_event-TARGET_DUPLICATED-0086",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "access_control-correct_etag_lagged-audit_event-TARGET_DUPLICATED-0086",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "access_control-correct_etag_lagged-audit_event-TARGET_DUPLICATED-0086",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_lagged-audit_event-TARGET_DUPLICATED-0086",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": false,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_lagged-audit_event-TARGET_DUPLICATED-0086",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "etag_state"
      ]
    },
    {
      "case_id": "access_control-correct_etag_lagged-audit_event-TARGET_DUPLICATED-0086",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "dqbp",
      "selected": "ABSTAIN",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": false,
      "probe_cost": 2,
      "probes": [
        "audit_event"
      ]
    },
    {
      "case_id": "access_control-correct_etag_lagged-audit_event-TARGET_DUPLICATED-0086",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "pdeo",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_lagged-audit_event-TARGET_DUPLICATED-0086",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "full_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_role",
        "scope_state",
        "other_principal",
        "etag_state",
        "audit_event"
      ]
    },
    {
      "case_id": "access_control-correct_etag_lagged-audit_event-TARGET_DUPLICATED-0086",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "human_minimal_obligations",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_lagged-audit_event-TARGET_OVERBROAD-0087",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "access_control-correct_etag_lagged-audit_event-TARGET_OVERBROAD-0087",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "access_control-correct_etag_lagged-audit_event-TARGET_OVERBROAD-0087",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_lagged-audit_event-TARGET_OVERBROAD-0087",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": false,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_lagged-audit_event-TARGET_OVERBROAD-0087",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "etag_state"
      ]
    },
    {
      "case_id": "access_control-correct_etag_lagged-audit_event-TARGET_OVERBROAD-0087",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "dqbp",
      "selected": "ABSTAIN",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": false,
      "probe_cost": 2,
      "probes": [
        "audit_event"
      ]
    },
    {
      "case_id": "access_control-correct_etag_lagged-audit_event-TARGET_OVERBROAD-0087",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "pdeo",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_lagged-audit_event-TARGET_OVERBROAD-0087",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "full_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_role",
        "scope_state",
        "other_principal",
        "etag_state",
        "audit_event"
      ]
    },
    {
      "case_id": "access_control-correct_etag_lagged-audit_event-TARGET_OVERBROAD-0087",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "human_minimal_obligations",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_lagged-etag_state-CURRENT-0088",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "access_control-correct_etag_lagged-etag_state-CURRENT-0088",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "access_control-correct_etag_lagged-etag_state-CURRENT-0088",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_lagged-etag_state-CURRENT-0088",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "tool_local_contract",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_lagged-etag_state-CURRENT-0088",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "etag_state",
        "scope_state"
      ]
    },
    {
      "case_id": "access_control-correct_etag_lagged-etag_state-CURRENT-0088",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "dqbp",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "audit_event"
      ]
    },
    {
      "case_id": "access_control-correct_etag_lagged-etag_state-CURRENT-0088",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "pdeo",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_lagged-etag_state-CURRENT-0088",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "full_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_role",
        "scope_state",
        "other_principal",
        "etag_state",
        "audit_event"
      ]
    },
    {
      "case_id": "access_control-correct_etag_lagged-etag_state-CURRENT-0088",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "human_minimal_obligations",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_lagged-target_role-paired-0089",
      "domain": "access_control",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "access_control-correct_etag_lagged-target_role-paired-0089",
      "domain": "access_control",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "access_control-correct_etag_lagged-target_role-paired-0089",
      "domain": "access_control",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "fixed_target_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_lagged-target_role-paired-0089",
      "domain": "access_control",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_lagged-target_role-paired-0089",
      "domain": "access_control",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 1,
      "probes": [
        "etag_state"
      ]
    },
    {
      "case_id": "access_control-correct_etag_lagged-target_role-paired-0089",
      "domain": "access_control",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "dqbp",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "audit_event"
      ]
    },
    {
      "case_id": "access_control-correct_etag_lagged-target_role-paired-0089",
      "domain": "access_control",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "pdeo",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_lagged-target_role-paired-0089",
      "domain": "access_control",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "full_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_role",
        "scope_state",
        "other_principal",
        "etag_state",
        "audit_event"
      ]
    },
    {
      "case_id": "access_control-correct_etag_lagged-target_role-paired-0089",
      "domain": "access_control",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "human_minimal_obligations",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_lagged-scope_state-paired-0090",
      "domain": "access_control",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "access_control-correct_etag_lagged-scope_state-paired-0090",
      "domain": "access_control",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "access_control-correct_etag_lagged-scope_state-paired-0090",
      "domain": "access_control",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 1,
      "probes": [
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_lagged-scope_state-paired-0090",
      "domain": "access_control",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_lagged-scope_state-paired-0090",
      "domain": "access_control",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 1,
      "probes": [
        "etag_state"
      ]
    },
    {
      "case_id": "access_control-correct_etag_lagged-scope_state-paired-0090",
      "domain": "access_control",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "dqbp",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "audit_event"
      ]
    },
    {
      "case_id": "access_control-correct_etag_lagged-scope_state-paired-0090",
      "domain": "access_control",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "pdeo",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_lagged-scope_state-paired-0090",
      "domain": "access_control",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "full_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_role",
        "scope_state",
        "other_principal",
        "etag_state",
        "audit_event"
      ]
    },
    {
      "case_id": "access_control-correct_etag_lagged-scope_state-paired-0090",
      "domain": "access_control",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "human_minimal_obligations",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_lagged-other_principal-paired-0091",
      "domain": "access_control",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "access_control-correct_etag_lagged-other_principal-paired-0091",
      "domain": "access_control",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "access_control-correct_etag_lagged-other_principal-paired-0091",
      "domain": "access_control",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 1,
      "probes": [
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_lagged-other_principal-paired-0091",
      "domain": "access_control",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_lagged-other_principal-paired-0091",
      "domain": "access_control",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 1,
      "probes": [
        "etag_state"
      ]
    },
    {
      "case_id": "access_control-correct_etag_lagged-other_principal-paired-0091",
      "domain": "access_control",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "dqbp",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "audit_event"
      ]
    },
    {
      "case_id": "access_control-correct_etag_lagged-other_principal-paired-0091",
      "domain": "access_control",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "pdeo",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_lagged-other_principal-paired-0091",
      "domain": "access_control",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "full_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_role",
        "scope_state",
        "other_principal",
        "etag_state",
        "audit_event"
      ]
    },
    {
      "case_id": "access_control-correct_etag_lagged-other_principal-paired-0091",
      "domain": "access_control",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "human_minimal_obligations",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_rotated-target_role-VIEWER-0092",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "access_control-correct_etag_rotated-target_role-VIEWER-0092",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "access_control-correct_etag_rotated-target_role-VIEWER-0092",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "fixed_target_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_rotated-target_role-VIEWER-0092",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_rotated-target_role-VIEWER-0092",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "state_information_gain",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "etag_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_rotated-target_role-VIEWER-0092",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "dqbp",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 2,
      "probes": [
        "audit_event"
      ]
    },
    {
      "case_id": "access_control-correct_etag_rotated-target_role-VIEWER-0092",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "pdeo",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_rotated-target_role-VIEWER-0092",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "full_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_role",
        "scope_state",
        "other_principal",
        "etag_state",
        "audit_event"
      ]
    },
    {
      "case_id": "access_control-correct_etag_rotated-target_role-VIEWER-0092",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "human_minimal_obligations",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_rotated-scope_state-DUPLICATE_BINDING-0093",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "access_control-correct_etag_rotated-scope_state-DUPLICATE_BINDING-0093",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "access_control-correct_etag_rotated-scope_state-DUPLICATE_BINDING-0093",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 1,
      "probes": [
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_rotated-scope_state-DUPLICATE_BINDING-0093",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_rotated-scope_state-DUPLICATE_BINDING-0093",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 2,
      "probes": [
        "etag_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_rotated-scope_state-DUPLICATE_BINDING-0093",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "dqbp",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 2,
      "probes": [
        "audit_event"
      ]
    },
    {
      "case_id": "access_control-correct_etag_rotated-scope_state-DUPLICATE_BINDING-0093",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "pdeo",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_rotated-scope_state-DUPLICATE_BINDING-0093",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "full_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_role",
        "scope_state",
        "other_principal",
        "etag_state",
        "audit_event"
      ]
    },
    {
      "case_id": "access_control-correct_etag_rotated-scope_state-DUPLICATE_BINDING-0093",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "human_minimal_obligations",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_rotated-scope_state-ORGANIZATION_WIDE-0094",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "access_control-correct_etag_rotated-scope_state-ORGANIZATION_WIDE-0094",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "access_control-correct_etag_rotated-scope_state-ORGANIZATION_WIDE-0094",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 1,
      "probes": [
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_rotated-scope_state-ORGANIZATION_WIDE-0094",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_rotated-scope_state-ORGANIZATION_WIDE-0094",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 2,
      "probes": [
        "etag_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_rotated-scope_state-ORGANIZATION_WIDE-0094",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "dqbp",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 2,
      "probes": [
        "audit_event"
      ]
    },
    {
      "case_id": "access_control-correct_etag_rotated-scope_state-ORGANIZATION_WIDE-0094",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "pdeo",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_rotated-scope_state-ORGANIZATION_WIDE-0094",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "full_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_role",
        "scope_state",
        "other_principal",
        "etag_state",
        "audit_event"
      ]
    },
    {
      "case_id": "access_control-correct_etag_rotated-scope_state-ORGANIZATION_WIDE-0094",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "human_minimal_obligations",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_rotated-other_principal-EDITOR-0095",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "access_control-correct_etag_rotated-other_principal-EDITOR-0095",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "access_control-correct_etag_rotated-other_principal-EDITOR-0095",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 1,
      "probes": [
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_rotated-other_principal-EDITOR-0095",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_rotated-other_principal-EDITOR-0095",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 2,
      "probes": [
        "etag_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_rotated-other_principal-EDITOR-0095",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "dqbp",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 2,
      "probes": [
        "audit_event"
      ]
    },
    {
      "case_id": "access_control-correct_etag_rotated-other_principal-EDITOR-0095",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "pdeo",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_rotated-other_principal-EDITOR-0095",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "full_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_role",
        "scope_state",
        "other_principal",
        "etag_state",
        "audit_event"
      ]
    },
    {
      "case_id": "access_control-correct_etag_rotated-other_principal-EDITOR-0095",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "human_minimal_obligations",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_rotated-audit_event-NO_MUTATION-0096",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "access_control-correct_etag_rotated-audit_event-NO_MUTATION-0096",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "access_control-correct_etag_rotated-audit_event-NO_MUTATION-0096",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_rotated-audit_event-NO_MUTATION-0096",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": false,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_rotated-audit_event-NO_MUTATION-0096",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "etag_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_rotated-audit_event-NO_MUTATION-0096",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "dqbp",
      "selected": "ABSTAIN",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": false,
      "probe_cost": 2,
      "probes": [
        "audit_event"
      ]
    },
    {
      "case_id": "access_control-correct_etag_rotated-audit_event-NO_MUTATION-0096",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "pdeo",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_rotated-audit_event-NO_MUTATION-0096",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "full_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_role",
        "scope_state",
        "other_principal",
        "etag_state",
        "audit_event"
      ]
    },
    {
      "case_id": "access_control-correct_etag_rotated-audit_event-NO_MUTATION-0096",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "human_minimal_obligations",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_rotated-audit_event-OTHER_GRANTED-0097",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "access_control-correct_etag_rotated-audit_event-OTHER_GRANTED-0097",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "access_control-correct_etag_rotated-audit_event-OTHER_GRANTED-0097",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_rotated-audit_event-OTHER_GRANTED-0097",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": false,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_rotated-audit_event-OTHER_GRANTED-0097",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "etag_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_rotated-audit_event-OTHER_GRANTED-0097",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "dqbp",
      "selected": "ABSTAIN",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": false,
      "probe_cost": 2,
      "probes": [
        "audit_event"
      ]
    },
    {
      "case_id": "access_control-correct_etag_rotated-audit_event-OTHER_GRANTED-0097",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "pdeo",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_rotated-audit_event-OTHER_GRANTED-0097",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "full_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_role",
        "scope_state",
        "other_principal",
        "etag_state",
        "audit_event"
      ]
    },
    {
      "case_id": "access_control-correct_etag_rotated-audit_event-OTHER_GRANTED-0097",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "human_minimal_obligations",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_rotated-audit_event-TARGET_DUPLICATED-0098",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "access_control-correct_etag_rotated-audit_event-TARGET_DUPLICATED-0098",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "access_control-correct_etag_rotated-audit_event-TARGET_DUPLICATED-0098",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_rotated-audit_event-TARGET_DUPLICATED-0098",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": false,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_rotated-audit_event-TARGET_DUPLICATED-0098",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "etag_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_rotated-audit_event-TARGET_DUPLICATED-0098",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "dqbp",
      "selected": "ABSTAIN",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": false,
      "probe_cost": 2,
      "probes": [
        "audit_event"
      ]
    },
    {
      "case_id": "access_control-correct_etag_rotated-audit_event-TARGET_DUPLICATED-0098",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "pdeo",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_rotated-audit_event-TARGET_DUPLICATED-0098",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "full_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_role",
        "scope_state",
        "other_principal",
        "etag_state",
        "audit_event"
      ]
    },
    {
      "case_id": "access_control-correct_etag_rotated-audit_event-TARGET_DUPLICATED-0098",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "human_minimal_obligations",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_rotated-audit_event-TARGET_OVERBROAD-0099",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "access_control-correct_etag_rotated-audit_event-TARGET_OVERBROAD-0099",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "access_control-correct_etag_rotated-audit_event-TARGET_OVERBROAD-0099",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_rotated-audit_event-TARGET_OVERBROAD-0099",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": false,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_rotated-audit_event-TARGET_OVERBROAD-0099",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "etag_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_rotated-audit_event-TARGET_OVERBROAD-0099",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "dqbp",
      "selected": "ABSTAIN",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": false,
      "probe_cost": 2,
      "probes": [
        "audit_event"
      ]
    },
    {
      "case_id": "access_control-correct_etag_rotated-audit_event-TARGET_OVERBROAD-0099",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "pdeo",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_rotated-audit_event-TARGET_OVERBROAD-0099",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "full_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_role",
        "scope_state",
        "other_principal",
        "etag_state",
        "audit_event"
      ]
    },
    {
      "case_id": "access_control-correct_etag_rotated-audit_event-TARGET_OVERBROAD-0099",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "human_minimal_obligations",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_rotated-target_role-paired-0100",
      "domain": "access_control",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "access_control-correct_etag_rotated-target_role-paired-0100",
      "domain": "access_control",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "access_control-correct_etag_rotated-target_role-paired-0100",
      "domain": "access_control",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "fixed_target_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_rotated-target_role-paired-0100",
      "domain": "access_control",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_rotated-target_role-paired-0100",
      "domain": "access_control",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "state_information_gain",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "etag_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_rotated-target_role-paired-0100",
      "domain": "access_control",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "dqbp",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "audit_event"
      ]
    },
    {
      "case_id": "access_control-correct_etag_rotated-target_role-paired-0100",
      "domain": "access_control",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "pdeo",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_rotated-target_role-paired-0100",
      "domain": "access_control",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "full_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_role",
        "scope_state",
        "other_principal",
        "etag_state",
        "audit_event"
      ]
    },
    {
      "case_id": "access_control-correct_etag_rotated-target_role-paired-0100",
      "domain": "access_control",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "human_minimal_obligations",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_rotated-scope_state-paired-0101",
      "domain": "access_control",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "access_control-correct_etag_rotated-scope_state-paired-0101",
      "domain": "access_control",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "access_control-correct_etag_rotated-scope_state-paired-0101",
      "domain": "access_control",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 1,
      "probes": [
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_rotated-scope_state-paired-0101",
      "domain": "access_control",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_rotated-scope_state-paired-0101",
      "domain": "access_control",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 2,
      "probes": [
        "etag_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_rotated-scope_state-paired-0101",
      "domain": "access_control",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "dqbp",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "audit_event"
      ]
    },
    {
      "case_id": "access_control-correct_etag_rotated-scope_state-paired-0101",
      "domain": "access_control",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "pdeo",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_rotated-scope_state-paired-0101",
      "domain": "access_control",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "full_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_role",
        "scope_state",
        "other_principal",
        "etag_state",
        "audit_event"
      ]
    },
    {
      "case_id": "access_control-correct_etag_rotated-scope_state-paired-0101",
      "domain": "access_control",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "human_minimal_obligations",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_rotated-other_principal-paired-0102",
      "domain": "access_control",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "access_control-correct_etag_rotated-other_principal-paired-0102",
      "domain": "access_control",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "access_control-correct_etag_rotated-other_principal-paired-0102",
      "domain": "access_control",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 1,
      "probes": [
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_rotated-other_principal-paired-0102",
      "domain": "access_control",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_rotated-other_principal-paired-0102",
      "domain": "access_control",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 2,
      "probes": [
        "etag_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_rotated-other_principal-paired-0102",
      "domain": "access_control",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "dqbp",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "audit_event"
      ]
    },
    {
      "case_id": "access_control-correct_etag_rotated-other_principal-paired-0102",
      "domain": "access_control",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "pdeo",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_rotated-other_principal-paired-0102",
      "domain": "access_control",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "full_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_role",
        "scope_state",
        "other_principal",
        "etag_state",
        "audit_event"
      ]
    },
    {
      "case_id": "access_control-correct_etag_rotated-other_principal-paired-0102",
      "domain": "access_control",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "human_minimal_obligations",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_hidden-target_role-VIEWER-0103",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "access_control-correct_etag_hidden-target_role-VIEWER-0103",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "access_control-correct_etag_hidden-target_role-VIEWER-0103",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "fixed_target_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_hidden-target_role-VIEWER-0103",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_hidden-target_role-VIEWER-0103",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 1,
      "probes": [
        "etag_state"
      ]
    },
    {
      "case_id": "access_control-correct_etag_hidden-target_role-VIEWER-0103",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "dqbp",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 2,
      "probes": [
        "audit_event"
      ]
    },
    {
      "case_id": "access_control-correct_etag_hidden-target_role-VIEWER-0103",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "pdeo",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_hidden-target_role-VIEWER-0103",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "full_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_role",
        "scope_state",
        "other_principal",
        "etag_state",
        "audit_event"
      ]
    },
    {
      "case_id": "access_control-correct_etag_hidden-target_role-VIEWER-0103",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "human_minimal_obligations",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_hidden-scope_state-DUPLICATE_BINDING-0104",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "access_control-correct_etag_hidden-scope_state-DUPLICATE_BINDING-0104",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "access_control-correct_etag_hidden-scope_state-DUPLICATE_BINDING-0104",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 1,
      "probes": [
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_hidden-scope_state-DUPLICATE_BINDING-0104",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_hidden-scope_state-DUPLICATE_BINDING-0104",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 1,
      "probes": [
        "etag_state"
      ]
    },
    {
      "case_id": "access_control-correct_etag_hidden-scope_state-DUPLICATE_BINDING-0104",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "dqbp",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 2,
      "probes": [
        "audit_event"
      ]
    },
    {
      "case_id": "access_control-correct_etag_hidden-scope_state-DUPLICATE_BINDING-0104",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "pdeo",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_hidden-scope_state-DUPLICATE_BINDING-0104",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "full_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_role",
        "scope_state",
        "other_principal",
        "etag_state",
        "audit_event"
      ]
    },
    {
      "case_id": "access_control-correct_etag_hidden-scope_state-DUPLICATE_BINDING-0104",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "human_minimal_obligations",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_hidden-scope_state-ORGANIZATION_WIDE-0105",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "access_control-correct_etag_hidden-scope_state-ORGANIZATION_WIDE-0105",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "access_control-correct_etag_hidden-scope_state-ORGANIZATION_WIDE-0105",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 1,
      "probes": [
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_hidden-scope_state-ORGANIZATION_WIDE-0105",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_hidden-scope_state-ORGANIZATION_WIDE-0105",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 1,
      "probes": [
        "etag_state"
      ]
    },
    {
      "case_id": "access_control-correct_etag_hidden-scope_state-ORGANIZATION_WIDE-0105",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "dqbp",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 2,
      "probes": [
        "audit_event"
      ]
    },
    {
      "case_id": "access_control-correct_etag_hidden-scope_state-ORGANIZATION_WIDE-0105",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "pdeo",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_hidden-scope_state-ORGANIZATION_WIDE-0105",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "full_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_role",
        "scope_state",
        "other_principal",
        "etag_state",
        "audit_event"
      ]
    },
    {
      "case_id": "access_control-correct_etag_hidden-scope_state-ORGANIZATION_WIDE-0105",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "human_minimal_obligations",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_hidden-other_principal-EDITOR-0106",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "access_control-correct_etag_hidden-other_principal-EDITOR-0106",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "access_control-correct_etag_hidden-other_principal-EDITOR-0106",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 1,
      "probes": [
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_hidden-other_principal-EDITOR-0106",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_hidden-other_principal-EDITOR-0106",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 1,
      "probes": [
        "etag_state"
      ]
    },
    {
      "case_id": "access_control-correct_etag_hidden-other_principal-EDITOR-0106",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "dqbp",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 2,
      "probes": [
        "audit_event"
      ]
    },
    {
      "case_id": "access_control-correct_etag_hidden-other_principal-EDITOR-0106",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "pdeo",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_hidden-other_principal-EDITOR-0106",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "full_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_role",
        "scope_state",
        "other_principal",
        "etag_state",
        "audit_event"
      ]
    },
    {
      "case_id": "access_control-correct_etag_hidden-other_principal-EDITOR-0106",
      "domain": "access_control",
      "split": "systematic_obligation_faults",
      "method": "human_minimal_obligations",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_hidden-audit_event-NO_MUTATION-0107",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "access_control-correct_etag_hidden-audit_event-NO_MUTATION-0107",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "access_control-correct_etag_hidden-audit_event-NO_MUTATION-0107",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_hidden-audit_event-NO_MUTATION-0107",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": false,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_hidden-audit_event-NO_MUTATION-0107",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "etag_state"
      ]
    },
    {
      "case_id": "access_control-correct_etag_hidden-audit_event-NO_MUTATION-0107",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "dqbp",
      "selected": "ABSTAIN",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": false,
      "probe_cost": 2,
      "probes": [
        "audit_event"
      ]
    },
    {
      "case_id": "access_control-correct_etag_hidden-audit_event-NO_MUTATION-0107",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "pdeo",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_hidden-audit_event-NO_MUTATION-0107",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "full_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_role",
        "scope_state",
        "other_principal",
        "etag_state",
        "audit_event"
      ]
    },
    {
      "case_id": "access_control-correct_etag_hidden-audit_event-NO_MUTATION-0107",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "human_minimal_obligations",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_hidden-audit_event-OTHER_GRANTED-0108",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "access_control-correct_etag_hidden-audit_event-OTHER_GRANTED-0108",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "access_control-correct_etag_hidden-audit_event-OTHER_GRANTED-0108",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_hidden-audit_event-OTHER_GRANTED-0108",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": false,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_hidden-audit_event-OTHER_GRANTED-0108",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "etag_state"
      ]
    },
    {
      "case_id": "access_control-correct_etag_hidden-audit_event-OTHER_GRANTED-0108",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "dqbp",
      "selected": "ABSTAIN",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": false,
      "probe_cost": 2,
      "probes": [
        "audit_event"
      ]
    },
    {
      "case_id": "access_control-correct_etag_hidden-audit_event-OTHER_GRANTED-0108",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "pdeo",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_hidden-audit_event-OTHER_GRANTED-0108",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "full_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_role",
        "scope_state",
        "other_principal",
        "etag_state",
        "audit_event"
      ]
    },
    {
      "case_id": "access_control-correct_etag_hidden-audit_event-OTHER_GRANTED-0108",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "human_minimal_obligations",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_hidden-audit_event-TARGET_DUPLICATED-0109",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "access_control-correct_etag_hidden-audit_event-TARGET_DUPLICATED-0109",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "access_control-correct_etag_hidden-audit_event-TARGET_DUPLICATED-0109",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_hidden-audit_event-TARGET_DUPLICATED-0109",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": false,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_hidden-audit_event-TARGET_DUPLICATED-0109",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "etag_state"
      ]
    },
    {
      "case_id": "access_control-correct_etag_hidden-audit_event-TARGET_DUPLICATED-0109",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "dqbp",
      "selected": "ABSTAIN",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": false,
      "probe_cost": 2,
      "probes": [
        "audit_event"
      ]
    },
    {
      "case_id": "access_control-correct_etag_hidden-audit_event-TARGET_DUPLICATED-0109",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "pdeo",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_hidden-audit_event-TARGET_DUPLICATED-0109",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "full_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_role",
        "scope_state",
        "other_principal",
        "etag_state",
        "audit_event"
      ]
    },
    {
      "case_id": "access_control-correct_etag_hidden-audit_event-TARGET_DUPLICATED-0109",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "human_minimal_obligations",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_hidden-audit_event-TARGET_OVERBROAD-0110",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "access_control-correct_etag_hidden-audit_event-TARGET_OVERBROAD-0110",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "access_control-correct_etag_hidden-audit_event-TARGET_OVERBROAD-0110",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_hidden-audit_event-TARGET_OVERBROAD-0110",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": false,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_hidden-audit_event-TARGET_OVERBROAD-0110",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "etag_state"
      ]
    },
    {
      "case_id": "access_control-correct_etag_hidden-audit_event-TARGET_OVERBROAD-0110",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "dqbp",
      "selected": "ABSTAIN",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": false,
      "probe_cost": 2,
      "probes": [
        "audit_event"
      ]
    },
    {
      "case_id": "access_control-correct_etag_hidden-audit_event-TARGET_OVERBROAD-0110",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "pdeo",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_hidden-audit_event-TARGET_OVERBROAD-0110",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "full_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_role",
        "scope_state",
        "other_principal",
        "etag_state",
        "audit_event"
      ]
    },
    {
      "case_id": "access_control-correct_etag_hidden-audit_event-TARGET_OVERBROAD-0110",
      "domain": "access_control",
      "split": "systematic_nuisance_variants",
      "method": "human_minimal_obligations",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_hidden-target_role-paired-0111",
      "domain": "access_control",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "access_control-correct_etag_hidden-target_role-paired-0111",
      "domain": "access_control",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "access_control-correct_etag_hidden-target_role-paired-0111",
      "domain": "access_control",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "fixed_target_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_hidden-target_role-paired-0111",
      "domain": "access_control",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_hidden-target_role-paired-0111",
      "domain": "access_control",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 1,
      "probes": [
        "etag_state"
      ]
    },
    {
      "case_id": "access_control-correct_etag_hidden-target_role-paired-0111",
      "domain": "access_control",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "dqbp",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "audit_event"
      ]
    },
    {
      "case_id": "access_control-correct_etag_hidden-target_role-paired-0111",
      "domain": "access_control",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "pdeo",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_hidden-target_role-paired-0111",
      "domain": "access_control",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "full_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_role",
        "scope_state",
        "other_principal",
        "etag_state",
        "audit_event"
      ]
    },
    {
      "case_id": "access_control-correct_etag_hidden-target_role-paired-0111",
      "domain": "access_control",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "human_minimal_obligations",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_hidden-scope_state-paired-0112",
      "domain": "access_control",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "access_control-correct_etag_hidden-scope_state-paired-0112",
      "domain": "access_control",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "access_control-correct_etag_hidden-scope_state-paired-0112",
      "domain": "access_control",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 1,
      "probes": [
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_hidden-scope_state-paired-0112",
      "domain": "access_control",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_hidden-scope_state-paired-0112",
      "domain": "access_control",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 1,
      "probes": [
        "etag_state"
      ]
    },
    {
      "case_id": "access_control-correct_etag_hidden-scope_state-paired-0112",
      "domain": "access_control",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "dqbp",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "audit_event"
      ]
    },
    {
      "case_id": "access_control-correct_etag_hidden-scope_state-paired-0112",
      "domain": "access_control",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "pdeo",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_hidden-scope_state-paired-0112",
      "domain": "access_control",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "full_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_role",
        "scope_state",
        "other_principal",
        "etag_state",
        "audit_event"
      ]
    },
    {
      "case_id": "access_control-correct_etag_hidden-scope_state-paired-0112",
      "domain": "access_control",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "human_minimal_obligations",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_hidden-other_principal-paired-0113",
      "domain": "access_control",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "access_control-correct_etag_hidden-other_principal-paired-0113",
      "domain": "access_control",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "access_control-correct_etag_hidden-other_principal-paired-0113",
      "domain": "access_control",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 1,
      "probes": [
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_hidden-other_principal-paired-0113",
      "domain": "access_control",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_hidden-other_principal-paired-0113",
      "domain": "access_control",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 1,
      "probes": [
        "etag_state"
      ]
    },
    {
      "case_id": "access_control-correct_etag_hidden-other_principal-paired-0113",
      "domain": "access_control",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "dqbp",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "audit_event"
      ]
    },
    {
      "case_id": "access_control-correct_etag_hidden-other_principal-paired-0113",
      "domain": "access_control",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "pdeo",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "access_control-correct_etag_hidden-other_principal-paired-0113",
      "domain": "access_control",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "full_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_role",
        "scope_state",
        "other_principal",
        "etag_state",
        "audit_event"
      ]
    },
    {
      "case_id": "access_control-correct_etag_hidden-other_principal-paired-0113",
      "domain": "access_control",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "human_minimal_obligations",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_principal",
        "scope_state",
        "target_role"
      ]
    },
    {
      "case_id": "inventory-correct_sync_current-0114",
      "domain": "inventory",
      "split": "known_branches",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "inventory-correct_sync_current-0114",
      "domain": "inventory",
      "split": "known_branches",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "inventory-correct_sync_current-0114",
      "domain": "inventory",
      "split": "known_branches",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_quantity"
      ]
    },
    {
      "case_id": "inventory-correct_sync_current-0114",
      "domain": "inventory",
      "split": "known_branches",
      "method": "tool_local_contract",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_current-0114",
      "domain": "inventory",
      "split": "known_branches",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "sync_version",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_current-0114",
      "domain": "inventory",
      "split": "known_branches",
      "method": "dqbp",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_current-0114",
      "domain": "inventory",
      "split": "known_branches",
      "method": "pdeo",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_current-0114",
      "domain": "inventory",
      "split": "known_branches",
      "method": "full_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_quantity",
        "warehouse_balance",
        "other_sku",
        "sync_version",
        "audit_event"
      ]
    },
    {
      "case_id": "inventory-correct_sync_current-0114",
      "domain": "inventory",
      "split": "known_branches",
      "method": "human_minimal_obligations",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_lagged-0115",
      "domain": "inventory",
      "split": "known_branches",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "inventory-correct_sync_lagged-0115",
      "domain": "inventory",
      "split": "known_branches",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "inventory-correct_sync_lagged-0115",
      "domain": "inventory",
      "split": "known_branches",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_quantity"
      ]
    },
    {
      "case_id": "inventory-correct_sync_lagged-0115",
      "domain": "inventory",
      "split": "known_branches",
      "method": "tool_local_contract",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_lagged-0115",
      "domain": "inventory",
      "split": "known_branches",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "sync_version",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_lagged-0115",
      "domain": "inventory",
      "split": "known_branches",
      "method": "dqbp",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_lagged-0115",
      "domain": "inventory",
      "split": "known_branches",
      "method": "pdeo",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_lagged-0115",
      "domain": "inventory",
      "split": "known_branches",
      "method": "full_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_quantity",
        "warehouse_balance",
        "other_sku",
        "sync_version",
        "audit_event"
      ]
    },
    {
      "case_id": "inventory-correct_sync_lagged-0115",
      "domain": "inventory",
      "split": "known_branches",
      "method": "human_minimal_obligations",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_external-0116",
      "domain": "inventory",
      "split": "known_branches",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "inventory-correct_sync_external-0116",
      "domain": "inventory",
      "split": "known_branches",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "inventory-correct_sync_external-0116",
      "domain": "inventory",
      "split": "known_branches",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_quantity"
      ]
    },
    {
      "case_id": "inventory-correct_sync_external-0116",
      "domain": "inventory",
      "split": "known_branches",
      "method": "tool_local_contract",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_external-0116",
      "domain": "inventory",
      "split": "known_branches",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "sync_version",
        "target_quantity"
      ]
    },
    {
      "case_id": "inventory-correct_sync_external-0116",
      "domain": "inventory",
      "split": "known_branches",
      "method": "dqbp",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_external-0116",
      "domain": "inventory",
      "split": "known_branches",
      "method": "pdeo",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_external-0116",
      "domain": "inventory",
      "split": "known_branches",
      "method": "full_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_quantity",
        "warehouse_balance",
        "other_sku",
        "sync_version",
        "audit_event"
      ]
    },
    {
      "case_id": "inventory-correct_sync_external-0116",
      "domain": "inventory",
      "split": "known_branches",
      "method": "human_minimal_obligations",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_hidden-0117",
      "domain": "inventory",
      "split": "known_branches",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "inventory-correct_sync_hidden-0117",
      "domain": "inventory",
      "split": "known_branches",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "inventory-correct_sync_hidden-0117",
      "domain": "inventory",
      "split": "known_branches",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_quantity"
      ]
    },
    {
      "case_id": "inventory-correct_sync_hidden-0117",
      "domain": "inventory",
      "split": "known_branches",
      "method": "tool_local_contract",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_hidden-0117",
      "domain": "inventory",
      "split": "known_branches",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "sync_version"
      ]
    },
    {
      "case_id": "inventory-correct_sync_hidden-0117",
      "domain": "inventory",
      "split": "known_branches",
      "method": "dqbp",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_hidden-0117",
      "domain": "inventory",
      "split": "known_branches",
      "method": "pdeo",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_hidden-0117",
      "domain": "inventory",
      "split": "known_branches",
      "method": "full_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_quantity",
        "warehouse_balance",
        "other_sku",
        "sync_version",
        "audit_event"
      ]
    },
    {
      "case_id": "inventory-correct_sync_hidden-0117",
      "domain": "inventory",
      "split": "known_branches",
      "method": "human_minimal_obligations",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-silent_noop-0118",
      "domain": "inventory",
      "split": "known_branches",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "inventory-silent_noop-0118",
      "domain": "inventory",
      "split": "known_branches",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "inventory-silent_noop-0118",
      "domain": "inventory",
      "split": "known_branches",
      "method": "fixed_target_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_quantity"
      ]
    },
    {
      "case_id": "inventory-silent_noop-0118",
      "domain": "inventory",
      "split": "known_branches",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-silent_noop-0118",
      "domain": "inventory",
      "split": "known_branches",
      "method": "state_information_gain",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "sync_version"
      ]
    },
    {
      "case_id": "inventory-silent_noop-0118",
      "domain": "inventory",
      "split": "known_branches",
      "method": "dqbp",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "target_quantity",
        "sync_version"
      ]
    },
    {
      "case_id": "inventory-silent_noop-0118",
      "domain": "inventory",
      "split": "known_branches",
      "method": "pdeo",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-silent_noop-0118",
      "domain": "inventory",
      "split": "known_branches",
      "method": "full_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_quantity",
        "warehouse_balance",
        "other_sku",
        "sync_version",
        "audit_event"
      ]
    },
    {
      "case_id": "inventory-silent_noop-0118",
      "domain": "inventory",
      "split": "known_branches",
      "method": "human_minimal_obligations",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-ledger_partial-0119",
      "domain": "inventory",
      "split": "known_branches",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "inventory-ledger_partial-0119",
      "domain": "inventory",
      "split": "known_branches",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "inventory-ledger_partial-0119",
      "domain": "inventory",
      "split": "known_branches",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 1,
      "probes": [
        "target_quantity"
      ]
    },
    {
      "case_id": "inventory-ledger_partial-0119",
      "domain": "inventory",
      "split": "known_branches",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-ledger_partial-0119",
      "domain": "inventory",
      "split": "known_branches",
      "method": "state_information_gain",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "sync_version",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-ledger_partial-0119",
      "domain": "inventory",
      "split": "known_branches",
      "method": "dqbp",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-ledger_partial-0119",
      "domain": "inventory",
      "split": "known_branches",
      "method": "pdeo",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-ledger_partial-0119",
      "domain": "inventory",
      "split": "known_branches",
      "method": "full_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_quantity",
        "warehouse_balance",
        "other_sku",
        "sync_version",
        "audit_event"
      ]
    },
    {
      "case_id": "inventory-ledger_partial-0119",
      "domain": "inventory",
      "split": "known_branches",
      "method": "human_minimal_obligations",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-wrong_sku-0120",
      "domain": "inventory",
      "split": "known_branches",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "inventory-wrong_sku-0120",
      "domain": "inventory",
      "split": "known_branches",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "inventory-wrong_sku-0120",
      "domain": "inventory",
      "split": "known_branches",
      "method": "fixed_target_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_quantity"
      ]
    },
    {
      "case_id": "inventory-wrong_sku-0120",
      "domain": "inventory",
      "split": "known_branches",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-wrong_sku-0120",
      "domain": "inventory",
      "split": "known_branches",
      "method": "state_information_gain",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "sync_version",
        "target_quantity"
      ]
    },
    {
      "case_id": "inventory-wrong_sku-0120",
      "domain": "inventory",
      "split": "known_branches",
      "method": "dqbp",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "target_quantity",
        "sync_version"
      ]
    },
    {
      "case_id": "inventory-wrong_sku-0120",
      "domain": "inventory",
      "split": "known_branches",
      "method": "pdeo",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-wrong_sku-0120",
      "domain": "inventory",
      "split": "known_branches",
      "method": "full_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_quantity",
        "warehouse_balance",
        "other_sku",
        "sync_version",
        "audit_event"
      ]
    },
    {
      "case_id": "inventory-wrong_sku-0120",
      "domain": "inventory",
      "split": "known_branches",
      "method": "human_minimal_obligations",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-double_increment-0121",
      "domain": "inventory",
      "split": "known_branches",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "inventory-double_increment-0121",
      "domain": "inventory",
      "split": "known_branches",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "inventory-double_increment-0121",
      "domain": "inventory",
      "split": "known_branches",
      "method": "fixed_target_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_quantity"
      ]
    },
    {
      "case_id": "inventory-double_increment-0121",
      "domain": "inventory",
      "split": "known_branches",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-double_increment-0121",
      "domain": "inventory",
      "split": "known_branches",
      "method": "state_information_gain",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "sync_version",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-double_increment-0121",
      "domain": "inventory",
      "split": "known_branches",
      "method": "dqbp",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_quantity"
      ]
    },
    {
      "case_id": "inventory-double_increment-0121",
      "domain": "inventory",
      "split": "known_branches",
      "method": "pdeo",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-double_increment-0121",
      "domain": "inventory",
      "split": "known_branches",
      "method": "full_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_quantity",
        "warehouse_balance",
        "other_sku",
        "sync_version",
        "audit_event"
      ]
    },
    {
      "case_id": "inventory-double_increment-0121",
      "domain": "inventory",
      "split": "known_branches",
      "method": "human_minimal_obligations",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_current-target_quantity-PLUS_10-0122",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "inventory-correct_sync_current-target_quantity-PLUS_10-0122",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "inventory-correct_sync_current-target_quantity-PLUS_10-0122",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "fixed_target_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_quantity"
      ]
    },
    {
      "case_id": "inventory-correct_sync_current-target_quantity-PLUS_10-0122",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_current-target_quantity-PLUS_10-0122",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 2,
      "probes": [
        "sync_version",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_current-target_quantity-PLUS_10-0122",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "dqbp",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_quantity"
      ]
    },
    {
      "case_id": "inventory-correct_sync_current-target_quantity-PLUS_10-0122",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "pdeo",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_current-target_quantity-PLUS_10-0122",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "full_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_quantity",
        "warehouse_balance",
        "other_sku",
        "sync_version",
        "audit_event"
      ]
    },
    {
      "case_id": "inventory-correct_sync_current-target_quantity-PLUS_10-0122",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "human_minimal_obligations",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_current-target_quantity-UNCHANGED-0123",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "inventory-correct_sync_current-target_quantity-UNCHANGED-0123",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "inventory-correct_sync_current-target_quantity-UNCHANGED-0123",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "fixed_target_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_quantity"
      ]
    },
    {
      "case_id": "inventory-correct_sync_current-target_quantity-UNCHANGED-0123",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_current-target_quantity-UNCHANGED-0123",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 2,
      "probes": [
        "sync_version",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_current-target_quantity-UNCHANGED-0123",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "dqbp",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "target_quantity",
        "sync_version"
      ]
    },
    {
      "case_id": "inventory-correct_sync_current-target_quantity-UNCHANGED-0123",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "pdeo",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_current-target_quantity-UNCHANGED-0123",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "full_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_quantity",
        "warehouse_balance",
        "other_sku",
        "sync_version",
        "audit_event"
      ]
    },
    {
      "case_id": "inventory-correct_sync_current-target_quantity-UNCHANGED-0123",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "human_minimal_obligations",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_current-warehouse_balance-UNBALANCED-0124",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "inventory-correct_sync_current-warehouse_balance-UNBALANCED-0124",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "inventory-correct_sync_current-warehouse_balance-UNBALANCED-0124",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 1,
      "probes": [
        "target_quantity"
      ]
    },
    {
      "case_id": "inventory-correct_sync_current-warehouse_balance-UNBALANCED-0124",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_current-warehouse_balance-UNBALANCED-0124",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "state_information_gain",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "sync_version",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_current-warehouse_balance-UNBALANCED-0124",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "dqbp",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_current-warehouse_balance-UNBALANCED-0124",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "pdeo",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_current-warehouse_balance-UNBALANCED-0124",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "full_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_quantity",
        "warehouse_balance",
        "other_sku",
        "sync_version",
        "audit_event"
      ]
    },
    {
      "case_id": "inventory-correct_sync_current-warehouse_balance-UNBALANCED-0124",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "human_minimal_obligations",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_current-other_sku-PLUS_5-0125",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "inventory-correct_sync_current-other_sku-PLUS_5-0125",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "inventory-correct_sync_current-other_sku-PLUS_5-0125",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 1,
      "probes": [
        "target_quantity"
      ]
    },
    {
      "case_id": "inventory-correct_sync_current-other_sku-PLUS_5-0125",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_current-other_sku-PLUS_5-0125",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 2,
      "probes": [
        "sync_version",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_current-other_sku-PLUS_5-0125",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "dqbp",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 2,
      "probes": [
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_current-other_sku-PLUS_5-0125",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "pdeo",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_current-other_sku-PLUS_5-0125",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "full_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_quantity",
        "warehouse_balance",
        "other_sku",
        "sync_version",
        "audit_event"
      ]
    },
    {
      "case_id": "inventory-correct_sync_current-other_sku-PLUS_5-0125",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "human_minimal_obligations",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_current-audit_event-NO_MUTATION-0126",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "inventory-correct_sync_current-audit_event-NO_MUTATION-0126",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "inventory-correct_sync_current-audit_event-NO_MUTATION-0126",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_quantity"
      ]
    },
    {
      "case_id": "inventory-correct_sync_current-audit_event-NO_MUTATION-0126",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": false,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_current-audit_event-NO_MUTATION-0126",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "sync_version",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_current-audit_event-NO_MUTATION-0126",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "dqbp",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_current-audit_event-NO_MUTATION-0126",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "pdeo",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_current-audit_event-NO_MUTATION-0126",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "full_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_quantity",
        "warehouse_balance",
        "other_sku",
        "sync_version",
        "audit_event"
      ]
    },
    {
      "case_id": "inventory-correct_sync_current-audit_event-NO_MUTATION-0126",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "human_minimal_obligations",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_current-audit_event-OTHER_INCREMENTED-0127",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "inventory-correct_sync_current-audit_event-OTHER_INCREMENTED-0127",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "inventory-correct_sync_current-audit_event-OTHER_INCREMENTED-0127",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_quantity"
      ]
    },
    {
      "case_id": "inventory-correct_sync_current-audit_event-OTHER_INCREMENTED-0127",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": false,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_current-audit_event-OTHER_INCREMENTED-0127",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "sync_version",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_current-audit_event-OTHER_INCREMENTED-0127",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "dqbp",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_current-audit_event-OTHER_INCREMENTED-0127",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "pdeo",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_current-audit_event-OTHER_INCREMENTED-0127",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "full_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_quantity",
        "warehouse_balance",
        "other_sku",
        "sync_version",
        "audit_event"
      ]
    },
    {
      "case_id": "inventory-correct_sync_current-audit_event-OTHER_INCREMENTED-0127",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "human_minimal_obligations",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_current-audit_event-TARGET_DOUBLE_INCREMENT-0128",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "inventory-correct_sync_current-audit_event-TARGET_DOUBLE_INCREMENT-0128",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "inventory-correct_sync_current-audit_event-TARGET_DOUBLE_INCREMENT-0128",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_quantity"
      ]
    },
    {
      "case_id": "inventory-correct_sync_current-audit_event-TARGET_DOUBLE_INCREMENT-0128",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": false,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_current-audit_event-TARGET_DOUBLE_INCREMENT-0128",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "sync_version",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_current-audit_event-TARGET_DOUBLE_INCREMENT-0128",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "dqbp",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_current-audit_event-TARGET_DOUBLE_INCREMENT-0128",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "pdeo",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_current-audit_event-TARGET_DOUBLE_INCREMENT-0128",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "full_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_quantity",
        "warehouse_balance",
        "other_sku",
        "sync_version",
        "audit_event"
      ]
    },
    {
      "case_id": "inventory-correct_sync_current-audit_event-TARGET_DOUBLE_INCREMENT-0128",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "human_minimal_obligations",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_current-audit_event-TARGET_WITHOUT_LEDGER-0129",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "inventory-correct_sync_current-audit_event-TARGET_WITHOUT_LEDGER-0129",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "inventory-correct_sync_current-audit_event-TARGET_WITHOUT_LEDGER-0129",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_quantity"
      ]
    },
    {
      "case_id": "inventory-correct_sync_current-audit_event-TARGET_WITHOUT_LEDGER-0129",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": false,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_current-audit_event-TARGET_WITHOUT_LEDGER-0129",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "sync_version",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_current-audit_event-TARGET_WITHOUT_LEDGER-0129",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "dqbp",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_current-audit_event-TARGET_WITHOUT_LEDGER-0129",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "pdeo",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_current-audit_event-TARGET_WITHOUT_LEDGER-0129",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "full_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_quantity",
        "warehouse_balance",
        "other_sku",
        "sync_version",
        "audit_event"
      ]
    },
    {
      "case_id": "inventory-correct_sync_current-audit_event-TARGET_WITHOUT_LEDGER-0129",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "human_minimal_obligations",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_current-sync_version-EXTERNAL-0130",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "inventory-correct_sync_current-sync_version-EXTERNAL-0130",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "inventory-correct_sync_current-sync_version-EXTERNAL-0130",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_quantity"
      ]
    },
    {
      "case_id": "inventory-correct_sync_current-sync_version-EXTERNAL-0130",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "tool_local_contract",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_current-sync_version-EXTERNAL-0130",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "sync_version",
        "target_quantity"
      ]
    },
    {
      "case_id": "inventory-correct_sync_current-sync_version-EXTERNAL-0130",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "dqbp",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_current-sync_version-EXTERNAL-0130",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "pdeo",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_current-sync_version-EXTERNAL-0130",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "full_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_quantity",
        "warehouse_balance",
        "other_sku",
        "sync_version",
        "audit_event"
      ]
    },
    {
      "case_id": "inventory-correct_sync_current-sync_version-EXTERNAL-0130",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "human_minimal_obligations",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_current-sync_version-HIDDEN-0131",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "inventory-correct_sync_current-sync_version-HIDDEN-0131",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "inventory-correct_sync_current-sync_version-HIDDEN-0131",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_quantity"
      ]
    },
    {
      "case_id": "inventory-correct_sync_current-sync_version-HIDDEN-0131",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "tool_local_contract",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_current-sync_version-HIDDEN-0131",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "sync_version"
      ]
    },
    {
      "case_id": "inventory-correct_sync_current-sync_version-HIDDEN-0131",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "dqbp",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_current-sync_version-HIDDEN-0131",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "pdeo",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_current-sync_version-HIDDEN-0131",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "full_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_quantity",
        "warehouse_balance",
        "other_sku",
        "sync_version",
        "audit_event"
      ]
    },
    {
      "case_id": "inventory-correct_sync_current-sync_version-HIDDEN-0131",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "human_minimal_obligations",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_current-sync_version-LAGGED-0132",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "inventory-correct_sync_current-sync_version-LAGGED-0132",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "inventory-correct_sync_current-sync_version-LAGGED-0132",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_quantity"
      ]
    },
    {
      "case_id": "inventory-correct_sync_current-sync_version-LAGGED-0132",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "tool_local_contract",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_current-sync_version-LAGGED-0132",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "sync_version",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_current-sync_version-LAGGED-0132",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "dqbp",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_current-sync_version-LAGGED-0132",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "pdeo",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_current-sync_version-LAGGED-0132",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "full_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_quantity",
        "warehouse_balance",
        "other_sku",
        "sync_version",
        "audit_event"
      ]
    },
    {
      "case_id": "inventory-correct_sync_current-sync_version-LAGGED-0132",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "human_minimal_obligations",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_current-sync_version-UNCHANGED-0133",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "inventory-correct_sync_current-sync_version-UNCHANGED-0133",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "inventory-correct_sync_current-sync_version-UNCHANGED-0133",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_quantity"
      ]
    },
    {
      "case_id": "inventory-correct_sync_current-sync_version-UNCHANGED-0133",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "tool_local_contract",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_current-sync_version-UNCHANGED-0133",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "state_information_gain",
      "selected": "ABSTAIN",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": false,
      "probe_cost": 1,
      "probes": [
        "sync_version"
      ]
    },
    {
      "case_id": "inventory-correct_sync_current-sync_version-UNCHANGED-0133",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "dqbp",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_current-sync_version-UNCHANGED-0133",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "pdeo",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_current-sync_version-UNCHANGED-0133",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "full_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_quantity",
        "warehouse_balance",
        "other_sku",
        "sync_version",
        "audit_event"
      ]
    },
    {
      "case_id": "inventory-correct_sync_current-sync_version-UNCHANGED-0133",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "human_minimal_obligations",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_current-target_quantity-paired-0134",
      "domain": "inventory",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "inventory-correct_sync_current-target_quantity-paired-0134",
      "domain": "inventory",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "inventory-correct_sync_current-target_quantity-paired-0134",
      "domain": "inventory",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "fixed_target_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_quantity"
      ]
    },
    {
      "case_id": "inventory-correct_sync_current-target_quantity-paired-0134",
      "domain": "inventory",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_current-target_quantity-paired-0134",
      "domain": "inventory",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 2,
      "probes": [
        "sync_version",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_current-target_quantity-paired-0134",
      "domain": "inventory",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "dqbp",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_quantity"
      ]
    },
    {
      "case_id": "inventory-correct_sync_current-target_quantity-paired-0134",
      "domain": "inventory",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "pdeo",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_current-target_quantity-paired-0134",
      "domain": "inventory",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "full_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_quantity",
        "warehouse_balance",
        "other_sku",
        "sync_version",
        "audit_event"
      ]
    },
    {
      "case_id": "inventory-correct_sync_current-target_quantity-paired-0134",
      "domain": "inventory",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "human_minimal_obligations",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_current-warehouse_balance-paired-0135",
      "domain": "inventory",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "inventory-correct_sync_current-warehouse_balance-paired-0135",
      "domain": "inventory",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "inventory-correct_sync_current-warehouse_balance-paired-0135",
      "domain": "inventory",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 1,
      "probes": [
        "target_quantity"
      ]
    },
    {
      "case_id": "inventory-correct_sync_current-warehouse_balance-paired-0135",
      "domain": "inventory",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_current-warehouse_balance-paired-0135",
      "domain": "inventory",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "state_information_gain",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "sync_version",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_current-warehouse_balance-paired-0135",
      "domain": "inventory",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "dqbp",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_current-warehouse_balance-paired-0135",
      "domain": "inventory",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "pdeo",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_current-warehouse_balance-paired-0135",
      "domain": "inventory",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "full_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_quantity",
        "warehouse_balance",
        "other_sku",
        "sync_version",
        "audit_event"
      ]
    },
    {
      "case_id": "inventory-correct_sync_current-warehouse_balance-paired-0135",
      "domain": "inventory",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "human_minimal_obligations",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_current-other_sku-paired-0136",
      "domain": "inventory",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "inventory-correct_sync_current-other_sku-paired-0136",
      "domain": "inventory",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "inventory-correct_sync_current-other_sku-paired-0136",
      "domain": "inventory",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 1,
      "probes": [
        "target_quantity"
      ]
    },
    {
      "case_id": "inventory-correct_sync_current-other_sku-paired-0136",
      "domain": "inventory",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_current-other_sku-paired-0136",
      "domain": "inventory",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 2,
      "probes": [
        "sync_version",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_current-other_sku-paired-0136",
      "domain": "inventory",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "dqbp",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 2,
      "probes": [
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_current-other_sku-paired-0136",
      "domain": "inventory",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "pdeo",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_current-other_sku-paired-0136",
      "domain": "inventory",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "full_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_quantity",
        "warehouse_balance",
        "other_sku",
        "sync_version",
        "audit_event"
      ]
    },
    {
      "case_id": "inventory-correct_sync_current-other_sku-paired-0136",
      "domain": "inventory",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "human_minimal_obligations",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_lagged-target_quantity-PLUS_10-0137",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "inventory-correct_sync_lagged-target_quantity-PLUS_10-0137",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "inventory-correct_sync_lagged-target_quantity-PLUS_10-0137",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "fixed_target_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_quantity"
      ]
    },
    {
      "case_id": "inventory-correct_sync_lagged-target_quantity-PLUS_10-0137",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_lagged-target_quantity-PLUS_10-0137",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 2,
      "probes": [
        "sync_version",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_lagged-target_quantity-PLUS_10-0137",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "dqbp",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_quantity"
      ]
    },
    {
      "case_id": "inventory-correct_sync_lagged-target_quantity-PLUS_10-0137",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "pdeo",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_lagged-target_quantity-PLUS_10-0137",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "full_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_quantity",
        "warehouse_balance",
        "other_sku",
        "sync_version",
        "audit_event"
      ]
    },
    {
      "case_id": "inventory-correct_sync_lagged-target_quantity-PLUS_10-0137",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "human_minimal_obligations",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_lagged-target_quantity-UNCHANGED-0138",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "inventory-correct_sync_lagged-target_quantity-UNCHANGED-0138",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "inventory-correct_sync_lagged-target_quantity-UNCHANGED-0138",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "fixed_target_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_quantity"
      ]
    },
    {
      "case_id": "inventory-correct_sync_lagged-target_quantity-UNCHANGED-0138",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_lagged-target_quantity-UNCHANGED-0138",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 2,
      "probes": [
        "sync_version",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_lagged-target_quantity-UNCHANGED-0138",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "dqbp",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "target_quantity",
        "sync_version"
      ]
    },
    {
      "case_id": "inventory-correct_sync_lagged-target_quantity-UNCHANGED-0138",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "pdeo",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_lagged-target_quantity-UNCHANGED-0138",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "full_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_quantity",
        "warehouse_balance",
        "other_sku",
        "sync_version",
        "audit_event"
      ]
    },
    {
      "case_id": "inventory-correct_sync_lagged-target_quantity-UNCHANGED-0138",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "human_minimal_obligations",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_lagged-warehouse_balance-UNBALANCED-0139",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "inventory-correct_sync_lagged-warehouse_balance-UNBALANCED-0139",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "inventory-correct_sync_lagged-warehouse_balance-UNBALANCED-0139",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 1,
      "probes": [
        "target_quantity"
      ]
    },
    {
      "case_id": "inventory-correct_sync_lagged-warehouse_balance-UNBALANCED-0139",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_lagged-warehouse_balance-UNBALANCED-0139",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "state_information_gain",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "sync_version",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_lagged-warehouse_balance-UNBALANCED-0139",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "dqbp",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_lagged-warehouse_balance-UNBALANCED-0139",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "pdeo",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_lagged-warehouse_balance-UNBALANCED-0139",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "full_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_quantity",
        "warehouse_balance",
        "other_sku",
        "sync_version",
        "audit_event"
      ]
    },
    {
      "case_id": "inventory-correct_sync_lagged-warehouse_balance-UNBALANCED-0139",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "human_minimal_obligations",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_lagged-other_sku-PLUS_5-0140",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "inventory-correct_sync_lagged-other_sku-PLUS_5-0140",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "inventory-correct_sync_lagged-other_sku-PLUS_5-0140",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 1,
      "probes": [
        "target_quantity"
      ]
    },
    {
      "case_id": "inventory-correct_sync_lagged-other_sku-PLUS_5-0140",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_lagged-other_sku-PLUS_5-0140",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 2,
      "probes": [
        "sync_version",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_lagged-other_sku-PLUS_5-0140",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "dqbp",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 2,
      "probes": [
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_lagged-other_sku-PLUS_5-0140",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "pdeo",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_lagged-other_sku-PLUS_5-0140",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "full_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_quantity",
        "warehouse_balance",
        "other_sku",
        "sync_version",
        "audit_event"
      ]
    },
    {
      "case_id": "inventory-correct_sync_lagged-other_sku-PLUS_5-0140",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "human_minimal_obligations",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_lagged-audit_event-NO_MUTATION-0141",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "inventory-correct_sync_lagged-audit_event-NO_MUTATION-0141",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "inventory-correct_sync_lagged-audit_event-NO_MUTATION-0141",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_quantity"
      ]
    },
    {
      "case_id": "inventory-correct_sync_lagged-audit_event-NO_MUTATION-0141",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": false,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_lagged-audit_event-NO_MUTATION-0141",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "sync_version",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_lagged-audit_event-NO_MUTATION-0141",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "dqbp",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_lagged-audit_event-NO_MUTATION-0141",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "pdeo",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_lagged-audit_event-NO_MUTATION-0141",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "full_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_quantity",
        "warehouse_balance",
        "other_sku",
        "sync_version",
        "audit_event"
      ]
    },
    {
      "case_id": "inventory-correct_sync_lagged-audit_event-NO_MUTATION-0141",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "human_minimal_obligations",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_lagged-audit_event-OTHER_INCREMENTED-0142",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "inventory-correct_sync_lagged-audit_event-OTHER_INCREMENTED-0142",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "inventory-correct_sync_lagged-audit_event-OTHER_INCREMENTED-0142",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_quantity"
      ]
    },
    {
      "case_id": "inventory-correct_sync_lagged-audit_event-OTHER_INCREMENTED-0142",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": false,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_lagged-audit_event-OTHER_INCREMENTED-0142",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "sync_version",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_lagged-audit_event-OTHER_INCREMENTED-0142",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "dqbp",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_lagged-audit_event-OTHER_INCREMENTED-0142",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "pdeo",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_lagged-audit_event-OTHER_INCREMENTED-0142",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "full_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_quantity",
        "warehouse_balance",
        "other_sku",
        "sync_version",
        "audit_event"
      ]
    },
    {
      "case_id": "inventory-correct_sync_lagged-audit_event-OTHER_INCREMENTED-0142",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "human_minimal_obligations",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_lagged-audit_event-TARGET_DOUBLE_INCREMENT-0143",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "inventory-correct_sync_lagged-audit_event-TARGET_DOUBLE_INCREMENT-0143",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "inventory-correct_sync_lagged-audit_event-TARGET_DOUBLE_INCREMENT-0143",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_quantity"
      ]
    },
    {
      "case_id": "inventory-correct_sync_lagged-audit_event-TARGET_DOUBLE_INCREMENT-0143",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": false,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_lagged-audit_event-TARGET_DOUBLE_INCREMENT-0143",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "sync_version",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_lagged-audit_event-TARGET_DOUBLE_INCREMENT-0143",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "dqbp",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_lagged-audit_event-TARGET_DOUBLE_INCREMENT-0143",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "pdeo",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_lagged-audit_event-TARGET_DOUBLE_INCREMENT-0143",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "full_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_quantity",
        "warehouse_balance",
        "other_sku",
        "sync_version",
        "audit_event"
      ]
    },
    {
      "case_id": "inventory-correct_sync_lagged-audit_event-TARGET_DOUBLE_INCREMENT-0143",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "human_minimal_obligations",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_lagged-audit_event-TARGET_WITHOUT_LEDGER-0144",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "inventory-correct_sync_lagged-audit_event-TARGET_WITHOUT_LEDGER-0144",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "inventory-correct_sync_lagged-audit_event-TARGET_WITHOUT_LEDGER-0144",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_quantity"
      ]
    },
    {
      "case_id": "inventory-correct_sync_lagged-audit_event-TARGET_WITHOUT_LEDGER-0144",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": false,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_lagged-audit_event-TARGET_WITHOUT_LEDGER-0144",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "sync_version",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_lagged-audit_event-TARGET_WITHOUT_LEDGER-0144",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "dqbp",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_lagged-audit_event-TARGET_WITHOUT_LEDGER-0144",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "pdeo",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_lagged-audit_event-TARGET_WITHOUT_LEDGER-0144",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "full_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_quantity",
        "warehouse_balance",
        "other_sku",
        "sync_version",
        "audit_event"
      ]
    },
    {
      "case_id": "inventory-correct_sync_lagged-audit_event-TARGET_WITHOUT_LEDGER-0144",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "human_minimal_obligations",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_lagged-sync_version-CURRENT-0145",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "inventory-correct_sync_lagged-sync_version-CURRENT-0145",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "inventory-correct_sync_lagged-sync_version-CURRENT-0145",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_quantity"
      ]
    },
    {
      "case_id": "inventory-correct_sync_lagged-sync_version-CURRENT-0145",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "tool_local_contract",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_lagged-sync_version-CURRENT-0145",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "sync_version",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_lagged-sync_version-CURRENT-0145",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "dqbp",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_lagged-sync_version-CURRENT-0145",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "pdeo",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_lagged-sync_version-CURRENT-0145",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "full_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_quantity",
        "warehouse_balance",
        "other_sku",
        "sync_version",
        "audit_event"
      ]
    },
    {
      "case_id": "inventory-correct_sync_lagged-sync_version-CURRENT-0145",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "human_minimal_obligations",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_lagged-target_quantity-paired-0146",
      "domain": "inventory",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "inventory-correct_sync_lagged-target_quantity-paired-0146",
      "domain": "inventory",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "inventory-correct_sync_lagged-target_quantity-paired-0146",
      "domain": "inventory",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "fixed_target_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_quantity"
      ]
    },
    {
      "case_id": "inventory-correct_sync_lagged-target_quantity-paired-0146",
      "domain": "inventory",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_lagged-target_quantity-paired-0146",
      "domain": "inventory",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 2,
      "probes": [
        "sync_version",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_lagged-target_quantity-paired-0146",
      "domain": "inventory",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "dqbp",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_quantity"
      ]
    },
    {
      "case_id": "inventory-correct_sync_lagged-target_quantity-paired-0146",
      "domain": "inventory",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "pdeo",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_lagged-target_quantity-paired-0146",
      "domain": "inventory",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "full_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_quantity",
        "warehouse_balance",
        "other_sku",
        "sync_version",
        "audit_event"
      ]
    },
    {
      "case_id": "inventory-correct_sync_lagged-target_quantity-paired-0146",
      "domain": "inventory",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "human_minimal_obligations",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_lagged-warehouse_balance-paired-0147",
      "domain": "inventory",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "inventory-correct_sync_lagged-warehouse_balance-paired-0147",
      "domain": "inventory",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "inventory-correct_sync_lagged-warehouse_balance-paired-0147",
      "domain": "inventory",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 1,
      "probes": [
        "target_quantity"
      ]
    },
    {
      "case_id": "inventory-correct_sync_lagged-warehouse_balance-paired-0147",
      "domain": "inventory",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_lagged-warehouse_balance-paired-0147",
      "domain": "inventory",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "state_information_gain",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "sync_version",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_lagged-warehouse_balance-paired-0147",
      "domain": "inventory",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "dqbp",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_lagged-warehouse_balance-paired-0147",
      "domain": "inventory",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "pdeo",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_lagged-warehouse_balance-paired-0147",
      "domain": "inventory",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "full_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_quantity",
        "warehouse_balance",
        "other_sku",
        "sync_version",
        "audit_event"
      ]
    },
    {
      "case_id": "inventory-correct_sync_lagged-warehouse_balance-paired-0147",
      "domain": "inventory",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "human_minimal_obligations",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_lagged-other_sku-paired-0148",
      "domain": "inventory",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "inventory-correct_sync_lagged-other_sku-paired-0148",
      "domain": "inventory",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "inventory-correct_sync_lagged-other_sku-paired-0148",
      "domain": "inventory",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 1,
      "probes": [
        "target_quantity"
      ]
    },
    {
      "case_id": "inventory-correct_sync_lagged-other_sku-paired-0148",
      "domain": "inventory",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_lagged-other_sku-paired-0148",
      "domain": "inventory",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 2,
      "probes": [
        "sync_version",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_lagged-other_sku-paired-0148",
      "domain": "inventory",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "dqbp",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 2,
      "probes": [
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_lagged-other_sku-paired-0148",
      "domain": "inventory",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "pdeo",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_lagged-other_sku-paired-0148",
      "domain": "inventory",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "full_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_quantity",
        "warehouse_balance",
        "other_sku",
        "sync_version",
        "audit_event"
      ]
    },
    {
      "case_id": "inventory-correct_sync_lagged-other_sku-paired-0148",
      "domain": "inventory",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "human_minimal_obligations",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_external-target_quantity-PLUS_10-0149",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "inventory-correct_sync_external-target_quantity-PLUS_10-0149",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "inventory-correct_sync_external-target_quantity-PLUS_10-0149",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "fixed_target_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_quantity"
      ]
    },
    {
      "case_id": "inventory-correct_sync_external-target_quantity-PLUS_10-0149",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_external-target_quantity-PLUS_10-0149",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "state_information_gain",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "sync_version",
        "target_quantity"
      ]
    },
    {
      "case_id": "inventory-correct_sync_external-target_quantity-PLUS_10-0149",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "dqbp",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_quantity"
      ]
    },
    {
      "case_id": "inventory-correct_sync_external-target_quantity-PLUS_10-0149",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "pdeo",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_external-target_quantity-PLUS_10-0149",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "full_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_quantity",
        "warehouse_balance",
        "other_sku",
        "sync_version",
        "audit_event"
      ]
    },
    {
      "case_id": "inventory-correct_sync_external-target_quantity-PLUS_10-0149",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "human_minimal_obligations",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_external-target_quantity-UNCHANGED-0150",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "inventory-correct_sync_external-target_quantity-UNCHANGED-0150",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "inventory-correct_sync_external-target_quantity-UNCHANGED-0150",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "fixed_target_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_quantity"
      ]
    },
    {
      "case_id": "inventory-correct_sync_external-target_quantity-UNCHANGED-0150",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_external-target_quantity-UNCHANGED-0150",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "state_information_gain",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "sync_version",
        "target_quantity"
      ]
    },
    {
      "case_id": "inventory-correct_sync_external-target_quantity-UNCHANGED-0150",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "dqbp",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "target_quantity",
        "sync_version"
      ]
    },
    {
      "case_id": "inventory-correct_sync_external-target_quantity-UNCHANGED-0150",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "pdeo",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_external-target_quantity-UNCHANGED-0150",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "full_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_quantity",
        "warehouse_balance",
        "other_sku",
        "sync_version",
        "audit_event"
      ]
    },
    {
      "case_id": "inventory-correct_sync_external-target_quantity-UNCHANGED-0150",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "human_minimal_obligations",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_external-warehouse_balance-UNBALANCED-0151",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "inventory-correct_sync_external-warehouse_balance-UNBALANCED-0151",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "inventory-correct_sync_external-warehouse_balance-UNBALANCED-0151",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 1,
      "probes": [
        "target_quantity"
      ]
    },
    {
      "case_id": "inventory-correct_sync_external-warehouse_balance-UNBALANCED-0151",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_external-warehouse_balance-UNBALANCED-0151",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 2,
      "probes": [
        "sync_version",
        "target_quantity"
      ]
    },
    {
      "case_id": "inventory-correct_sync_external-warehouse_balance-UNBALANCED-0151",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "dqbp",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_external-warehouse_balance-UNBALANCED-0151",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "pdeo",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_external-warehouse_balance-UNBALANCED-0151",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "full_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_quantity",
        "warehouse_balance",
        "other_sku",
        "sync_version",
        "audit_event"
      ]
    },
    {
      "case_id": "inventory-correct_sync_external-warehouse_balance-UNBALANCED-0151",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "human_minimal_obligations",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_external-other_sku-PLUS_5-0152",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "inventory-correct_sync_external-other_sku-PLUS_5-0152",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "inventory-correct_sync_external-other_sku-PLUS_5-0152",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 1,
      "probes": [
        "target_quantity"
      ]
    },
    {
      "case_id": "inventory-correct_sync_external-other_sku-PLUS_5-0152",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_external-other_sku-PLUS_5-0152",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 2,
      "probes": [
        "sync_version",
        "target_quantity"
      ]
    },
    {
      "case_id": "inventory-correct_sync_external-other_sku-PLUS_5-0152",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "dqbp",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 2,
      "probes": [
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_external-other_sku-PLUS_5-0152",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "pdeo",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_external-other_sku-PLUS_5-0152",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "full_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_quantity",
        "warehouse_balance",
        "other_sku",
        "sync_version",
        "audit_event"
      ]
    },
    {
      "case_id": "inventory-correct_sync_external-other_sku-PLUS_5-0152",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "human_minimal_obligations",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_external-audit_event-NO_MUTATION-0153",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "inventory-correct_sync_external-audit_event-NO_MUTATION-0153",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "inventory-correct_sync_external-audit_event-NO_MUTATION-0153",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_quantity"
      ]
    },
    {
      "case_id": "inventory-correct_sync_external-audit_event-NO_MUTATION-0153",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": false,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_external-audit_event-NO_MUTATION-0153",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "sync_version",
        "target_quantity"
      ]
    },
    {
      "case_id": "inventory-correct_sync_external-audit_event-NO_MUTATION-0153",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "dqbp",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_external-audit_event-NO_MUTATION-0153",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "pdeo",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_external-audit_event-NO_MUTATION-0153",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "full_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_quantity",
        "warehouse_balance",
        "other_sku",
        "sync_version",
        "audit_event"
      ]
    },
    {
      "case_id": "inventory-correct_sync_external-audit_event-NO_MUTATION-0153",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "human_minimal_obligations",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_external-audit_event-OTHER_INCREMENTED-0154",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "inventory-correct_sync_external-audit_event-OTHER_INCREMENTED-0154",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "inventory-correct_sync_external-audit_event-OTHER_INCREMENTED-0154",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_quantity"
      ]
    },
    {
      "case_id": "inventory-correct_sync_external-audit_event-OTHER_INCREMENTED-0154",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": false,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_external-audit_event-OTHER_INCREMENTED-0154",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "sync_version",
        "target_quantity"
      ]
    },
    {
      "case_id": "inventory-correct_sync_external-audit_event-OTHER_INCREMENTED-0154",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "dqbp",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_external-audit_event-OTHER_INCREMENTED-0154",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "pdeo",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_external-audit_event-OTHER_INCREMENTED-0154",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "full_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_quantity",
        "warehouse_balance",
        "other_sku",
        "sync_version",
        "audit_event"
      ]
    },
    {
      "case_id": "inventory-correct_sync_external-audit_event-OTHER_INCREMENTED-0154",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "human_minimal_obligations",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_external-audit_event-TARGET_DOUBLE_INCREMENT-0155",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "inventory-correct_sync_external-audit_event-TARGET_DOUBLE_INCREMENT-0155",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "inventory-correct_sync_external-audit_event-TARGET_DOUBLE_INCREMENT-0155",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_quantity"
      ]
    },
    {
      "case_id": "inventory-correct_sync_external-audit_event-TARGET_DOUBLE_INCREMENT-0155",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": false,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_external-audit_event-TARGET_DOUBLE_INCREMENT-0155",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "sync_version",
        "target_quantity"
      ]
    },
    {
      "case_id": "inventory-correct_sync_external-audit_event-TARGET_DOUBLE_INCREMENT-0155",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "dqbp",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_external-audit_event-TARGET_DOUBLE_INCREMENT-0155",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "pdeo",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_external-audit_event-TARGET_DOUBLE_INCREMENT-0155",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "full_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_quantity",
        "warehouse_balance",
        "other_sku",
        "sync_version",
        "audit_event"
      ]
    },
    {
      "case_id": "inventory-correct_sync_external-audit_event-TARGET_DOUBLE_INCREMENT-0155",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "human_minimal_obligations",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_external-audit_event-TARGET_WITHOUT_LEDGER-0156",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "inventory-correct_sync_external-audit_event-TARGET_WITHOUT_LEDGER-0156",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "inventory-correct_sync_external-audit_event-TARGET_WITHOUT_LEDGER-0156",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_quantity"
      ]
    },
    {
      "case_id": "inventory-correct_sync_external-audit_event-TARGET_WITHOUT_LEDGER-0156",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": false,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_external-audit_event-TARGET_WITHOUT_LEDGER-0156",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "sync_version",
        "target_quantity"
      ]
    },
    {
      "case_id": "inventory-correct_sync_external-audit_event-TARGET_WITHOUT_LEDGER-0156",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "dqbp",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_external-audit_event-TARGET_WITHOUT_LEDGER-0156",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "pdeo",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_external-audit_event-TARGET_WITHOUT_LEDGER-0156",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "full_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_quantity",
        "warehouse_balance",
        "other_sku",
        "sync_version",
        "audit_event"
      ]
    },
    {
      "case_id": "inventory-correct_sync_external-audit_event-TARGET_WITHOUT_LEDGER-0156",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "human_minimal_obligations",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_external-target_quantity-paired-0157",
      "domain": "inventory",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "inventory-correct_sync_external-target_quantity-paired-0157",
      "domain": "inventory",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "inventory-correct_sync_external-target_quantity-paired-0157",
      "domain": "inventory",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "fixed_target_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_quantity"
      ]
    },
    {
      "case_id": "inventory-correct_sync_external-target_quantity-paired-0157",
      "domain": "inventory",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_external-target_quantity-paired-0157",
      "domain": "inventory",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "state_information_gain",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "sync_version",
        "target_quantity"
      ]
    },
    {
      "case_id": "inventory-correct_sync_external-target_quantity-paired-0157",
      "domain": "inventory",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "dqbp",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_quantity"
      ]
    },
    {
      "case_id": "inventory-correct_sync_external-target_quantity-paired-0157",
      "domain": "inventory",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "pdeo",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_external-target_quantity-paired-0157",
      "domain": "inventory",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "full_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_quantity",
        "warehouse_balance",
        "other_sku",
        "sync_version",
        "audit_event"
      ]
    },
    {
      "case_id": "inventory-correct_sync_external-target_quantity-paired-0157",
      "domain": "inventory",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "human_minimal_obligations",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_external-warehouse_balance-paired-0158",
      "domain": "inventory",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "inventory-correct_sync_external-warehouse_balance-paired-0158",
      "domain": "inventory",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "inventory-correct_sync_external-warehouse_balance-paired-0158",
      "domain": "inventory",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 1,
      "probes": [
        "target_quantity"
      ]
    },
    {
      "case_id": "inventory-correct_sync_external-warehouse_balance-paired-0158",
      "domain": "inventory",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_external-warehouse_balance-paired-0158",
      "domain": "inventory",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 2,
      "probes": [
        "sync_version",
        "target_quantity"
      ]
    },
    {
      "case_id": "inventory-correct_sync_external-warehouse_balance-paired-0158",
      "domain": "inventory",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "dqbp",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_external-warehouse_balance-paired-0158",
      "domain": "inventory",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "pdeo",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_external-warehouse_balance-paired-0158",
      "domain": "inventory",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "full_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_quantity",
        "warehouse_balance",
        "other_sku",
        "sync_version",
        "audit_event"
      ]
    },
    {
      "case_id": "inventory-correct_sync_external-warehouse_balance-paired-0158",
      "domain": "inventory",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "human_minimal_obligations",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_external-other_sku-paired-0159",
      "domain": "inventory",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "inventory-correct_sync_external-other_sku-paired-0159",
      "domain": "inventory",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "inventory-correct_sync_external-other_sku-paired-0159",
      "domain": "inventory",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 1,
      "probes": [
        "target_quantity"
      ]
    },
    {
      "case_id": "inventory-correct_sync_external-other_sku-paired-0159",
      "domain": "inventory",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_external-other_sku-paired-0159",
      "domain": "inventory",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 2,
      "probes": [
        "sync_version",
        "target_quantity"
      ]
    },
    {
      "case_id": "inventory-correct_sync_external-other_sku-paired-0159",
      "domain": "inventory",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "dqbp",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 2,
      "probes": [
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_external-other_sku-paired-0159",
      "domain": "inventory",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "pdeo",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_external-other_sku-paired-0159",
      "domain": "inventory",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "full_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_quantity",
        "warehouse_balance",
        "other_sku",
        "sync_version",
        "audit_event"
      ]
    },
    {
      "case_id": "inventory-correct_sync_external-other_sku-paired-0159",
      "domain": "inventory",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "human_minimal_obligations",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_hidden-target_quantity-PLUS_10-0160",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "inventory-correct_sync_hidden-target_quantity-PLUS_10-0160",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "inventory-correct_sync_hidden-target_quantity-PLUS_10-0160",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "fixed_target_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_quantity"
      ]
    },
    {
      "case_id": "inventory-correct_sync_hidden-target_quantity-PLUS_10-0160",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_hidden-target_quantity-PLUS_10-0160",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 1,
      "probes": [
        "sync_version"
      ]
    },
    {
      "case_id": "inventory-correct_sync_hidden-target_quantity-PLUS_10-0160",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "dqbp",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_quantity"
      ]
    },
    {
      "case_id": "inventory-correct_sync_hidden-target_quantity-PLUS_10-0160",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "pdeo",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_hidden-target_quantity-PLUS_10-0160",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "full_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_quantity",
        "warehouse_balance",
        "other_sku",
        "sync_version",
        "audit_event"
      ]
    },
    {
      "case_id": "inventory-correct_sync_hidden-target_quantity-PLUS_10-0160",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "human_minimal_obligations",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_hidden-target_quantity-UNCHANGED-0161",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "inventory-correct_sync_hidden-target_quantity-UNCHANGED-0161",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "inventory-correct_sync_hidden-target_quantity-UNCHANGED-0161",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "fixed_target_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_quantity"
      ]
    },
    {
      "case_id": "inventory-correct_sync_hidden-target_quantity-UNCHANGED-0161",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_hidden-target_quantity-UNCHANGED-0161",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 1,
      "probes": [
        "sync_version"
      ]
    },
    {
      "case_id": "inventory-correct_sync_hidden-target_quantity-UNCHANGED-0161",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "dqbp",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "target_quantity",
        "sync_version"
      ]
    },
    {
      "case_id": "inventory-correct_sync_hidden-target_quantity-UNCHANGED-0161",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "pdeo",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_hidden-target_quantity-UNCHANGED-0161",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "full_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_quantity",
        "warehouse_balance",
        "other_sku",
        "sync_version",
        "audit_event"
      ]
    },
    {
      "case_id": "inventory-correct_sync_hidden-target_quantity-UNCHANGED-0161",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "human_minimal_obligations",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_hidden-warehouse_balance-UNBALANCED-0162",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "inventory-correct_sync_hidden-warehouse_balance-UNBALANCED-0162",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "inventory-correct_sync_hidden-warehouse_balance-UNBALANCED-0162",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 1,
      "probes": [
        "target_quantity"
      ]
    },
    {
      "case_id": "inventory-correct_sync_hidden-warehouse_balance-UNBALANCED-0162",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_hidden-warehouse_balance-UNBALANCED-0162",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 1,
      "probes": [
        "sync_version"
      ]
    },
    {
      "case_id": "inventory-correct_sync_hidden-warehouse_balance-UNBALANCED-0162",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "dqbp",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_hidden-warehouse_balance-UNBALANCED-0162",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "pdeo",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_hidden-warehouse_balance-UNBALANCED-0162",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "full_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_quantity",
        "warehouse_balance",
        "other_sku",
        "sync_version",
        "audit_event"
      ]
    },
    {
      "case_id": "inventory-correct_sync_hidden-warehouse_balance-UNBALANCED-0162",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "human_minimal_obligations",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_hidden-other_sku-PLUS_5-0163",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "inventory-correct_sync_hidden-other_sku-PLUS_5-0163",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "inventory-correct_sync_hidden-other_sku-PLUS_5-0163",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 1,
      "probes": [
        "target_quantity"
      ]
    },
    {
      "case_id": "inventory-correct_sync_hidden-other_sku-PLUS_5-0163",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_hidden-other_sku-PLUS_5-0163",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 1,
      "probes": [
        "sync_version"
      ]
    },
    {
      "case_id": "inventory-correct_sync_hidden-other_sku-PLUS_5-0163",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "dqbp",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 2,
      "probes": [
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_hidden-other_sku-PLUS_5-0163",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "pdeo",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_hidden-other_sku-PLUS_5-0163",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "full_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_quantity",
        "warehouse_balance",
        "other_sku",
        "sync_version",
        "audit_event"
      ]
    },
    {
      "case_id": "inventory-correct_sync_hidden-other_sku-PLUS_5-0163",
      "domain": "inventory",
      "split": "systematic_obligation_faults",
      "method": "human_minimal_obligations",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_hidden-audit_event-NO_MUTATION-0164",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "inventory-correct_sync_hidden-audit_event-NO_MUTATION-0164",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "inventory-correct_sync_hidden-audit_event-NO_MUTATION-0164",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_quantity"
      ]
    },
    {
      "case_id": "inventory-correct_sync_hidden-audit_event-NO_MUTATION-0164",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": false,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_hidden-audit_event-NO_MUTATION-0164",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "sync_version"
      ]
    },
    {
      "case_id": "inventory-correct_sync_hidden-audit_event-NO_MUTATION-0164",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "dqbp",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_hidden-audit_event-NO_MUTATION-0164",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "pdeo",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_hidden-audit_event-NO_MUTATION-0164",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "full_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_quantity",
        "warehouse_balance",
        "other_sku",
        "sync_version",
        "audit_event"
      ]
    },
    {
      "case_id": "inventory-correct_sync_hidden-audit_event-NO_MUTATION-0164",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "human_minimal_obligations",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_hidden-audit_event-OTHER_INCREMENTED-0165",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "inventory-correct_sync_hidden-audit_event-OTHER_INCREMENTED-0165",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "inventory-correct_sync_hidden-audit_event-OTHER_INCREMENTED-0165",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_quantity"
      ]
    },
    {
      "case_id": "inventory-correct_sync_hidden-audit_event-OTHER_INCREMENTED-0165",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": false,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_hidden-audit_event-OTHER_INCREMENTED-0165",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "sync_version"
      ]
    },
    {
      "case_id": "inventory-correct_sync_hidden-audit_event-OTHER_INCREMENTED-0165",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "dqbp",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_hidden-audit_event-OTHER_INCREMENTED-0165",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "pdeo",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_hidden-audit_event-OTHER_INCREMENTED-0165",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "full_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_quantity",
        "warehouse_balance",
        "other_sku",
        "sync_version",
        "audit_event"
      ]
    },
    {
      "case_id": "inventory-correct_sync_hidden-audit_event-OTHER_INCREMENTED-0165",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "human_minimal_obligations",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_hidden-audit_event-TARGET_DOUBLE_INCREMENT-0166",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "inventory-correct_sync_hidden-audit_event-TARGET_DOUBLE_INCREMENT-0166",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "inventory-correct_sync_hidden-audit_event-TARGET_DOUBLE_INCREMENT-0166",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_quantity"
      ]
    },
    {
      "case_id": "inventory-correct_sync_hidden-audit_event-TARGET_DOUBLE_INCREMENT-0166",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": false,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_hidden-audit_event-TARGET_DOUBLE_INCREMENT-0166",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "sync_version"
      ]
    },
    {
      "case_id": "inventory-correct_sync_hidden-audit_event-TARGET_DOUBLE_INCREMENT-0166",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "dqbp",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_hidden-audit_event-TARGET_DOUBLE_INCREMENT-0166",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "pdeo",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_hidden-audit_event-TARGET_DOUBLE_INCREMENT-0166",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "full_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_quantity",
        "warehouse_balance",
        "other_sku",
        "sync_version",
        "audit_event"
      ]
    },
    {
      "case_id": "inventory-correct_sync_hidden-audit_event-TARGET_DOUBLE_INCREMENT-0166",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "human_minimal_obligations",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_hidden-audit_event-TARGET_WITHOUT_LEDGER-0167",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "inventory-correct_sync_hidden-audit_event-TARGET_WITHOUT_LEDGER-0167",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "inventory-correct_sync_hidden-audit_event-TARGET_WITHOUT_LEDGER-0167",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_quantity"
      ]
    },
    {
      "case_id": "inventory-correct_sync_hidden-audit_event-TARGET_WITHOUT_LEDGER-0167",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": false,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_hidden-audit_event-TARGET_WITHOUT_LEDGER-0167",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "sync_version"
      ]
    },
    {
      "case_id": "inventory-correct_sync_hidden-audit_event-TARGET_WITHOUT_LEDGER-0167",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "dqbp",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_hidden-audit_event-TARGET_WITHOUT_LEDGER-0167",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "pdeo",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_hidden-audit_event-TARGET_WITHOUT_LEDGER-0167",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "full_readback",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_quantity",
        "warehouse_balance",
        "other_sku",
        "sync_version",
        "audit_event"
      ]
    },
    {
      "case_id": "inventory-correct_sync_hidden-audit_event-TARGET_WITHOUT_LEDGER-0167",
      "domain": "inventory",
      "split": "systematic_nuisance_variants",
      "method": "human_minimal_obligations",
      "selected": "PROCEED",
      "expected": "PROCEED",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_hidden-target_quantity-paired-0168",
      "domain": "inventory",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "inventory-correct_sync_hidden-target_quantity-paired-0168",
      "domain": "inventory",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "inventory-correct_sync_hidden-target_quantity-paired-0168",
      "domain": "inventory",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "fixed_target_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_quantity"
      ]
    },
    {
      "case_id": "inventory-correct_sync_hidden-target_quantity-paired-0168",
      "domain": "inventory",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_hidden-target_quantity-paired-0168",
      "domain": "inventory",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 1,
      "probes": [
        "sync_version"
      ]
    },
    {
      "case_id": "inventory-correct_sync_hidden-target_quantity-paired-0168",
      "domain": "inventory",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "dqbp",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 1,
      "probes": [
        "target_quantity"
      ]
    },
    {
      "case_id": "inventory-correct_sync_hidden-target_quantity-paired-0168",
      "domain": "inventory",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "pdeo",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_hidden-target_quantity-paired-0168",
      "domain": "inventory",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "full_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_quantity",
        "warehouse_balance",
        "other_sku",
        "sync_version",
        "audit_event"
      ]
    },
    {
      "case_id": "inventory-correct_sync_hidden-target_quantity-paired-0168",
      "domain": "inventory",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "human_minimal_obligations",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_hidden-warehouse_balance-paired-0169",
      "domain": "inventory",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "inventory-correct_sync_hidden-warehouse_balance-paired-0169",
      "domain": "inventory",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "inventory-correct_sync_hidden-warehouse_balance-paired-0169",
      "domain": "inventory",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 1,
      "probes": [
        "target_quantity"
      ]
    },
    {
      "case_id": "inventory-correct_sync_hidden-warehouse_balance-paired-0169",
      "domain": "inventory",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_hidden-warehouse_balance-paired-0169",
      "domain": "inventory",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 1,
      "probes": [
        "sync_version"
      ]
    },
    {
      "case_id": "inventory-correct_sync_hidden-warehouse_balance-paired-0169",
      "domain": "inventory",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "dqbp",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 2,
      "probes": [
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_hidden-warehouse_balance-paired-0169",
      "domain": "inventory",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "pdeo",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_hidden-warehouse_balance-paired-0169",
      "domain": "inventory",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "full_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_quantity",
        "warehouse_balance",
        "other_sku",
        "sync_version",
        "audit_event"
      ]
    },
    {
      "case_id": "inventory-correct_sync_hidden-warehouse_balance-paired-0169",
      "domain": "inventory",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "human_minimal_obligations",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_hidden-other_sku-paired-0170",
      "domain": "inventory",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "no_verification",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "inventory-correct_sync_hidden-other_sku-paired-0170",
      "domain": "inventory",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "static_receipt",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 0,
      "probes": []
    },
    {
      "case_id": "inventory-correct_sync_hidden-other_sku-paired-0170",
      "domain": "inventory",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "fixed_target_readback",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 1,
      "probes": [
        "target_quantity"
      ]
    },
    {
      "case_id": "inventory-correct_sync_hidden-other_sku-paired-0170",
      "domain": "inventory",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "tool_local_contract",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 5,
      "probes": [
        "audit_event",
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_hidden-other_sku-paired-0170",
      "domain": "inventory",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "state_information_gain",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 1,
      "probes": [
        "sync_version"
      ]
    },
    {
      "case_id": "inventory-correct_sync_hidden-other_sku-paired-0170",
      "domain": "inventory",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "dqbp",
      "selected": "PROCEED",
      "expected": "ABSTAIN",
      "unsafe_commit": true,
      "correct": false,
      "probe_cost": 2,
      "probes": [
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_hidden-other_sku-paired-0170",
      "domain": "inventory",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "pdeo",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    },
    {
      "case_id": "inventory-correct_sync_hidden-other_sku-paired-0170",
      "domain": "inventory",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "full_readback",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 6,
      "probes": [
        "target_quantity",
        "warehouse_balance",
        "other_sku",
        "sync_version",
        "audit_event"
      ]
    },
    {
      "case_id": "inventory-correct_sync_hidden-other_sku-paired-0170",
      "domain": "inventory",
      "split": "paired_obligation_and_nuisance_faults",
      "method": "human_minimal_obligations",
      "selected": "ABSTAIN",
      "expected": "ABSTAIN",
      "unsafe_commit": false,
      "correct": true,
      "probe_cost": 3,
      "probes": [
        "other_sku",
        "target_quantity",
        "warehouse_balance"
      ]
    }
  ]
}

## 7. Known Limitations

### Source: `selection_context_v001.md`

# 当前选择与淘汰上下文

## 选择

当前唯一进入正式实验的候选是 H4：计划派生证据义务（PDEO）。它从受保护下游承诺反向传播状态谓词，并按只读探针成本求最小覆盖；与 H1 的有限分支决策风险目标不同。

选择依据不是“结果更好看”，而是 H4 在方法输入和失败模型上与 H1 正交：H1 需要已知故障分支与先验，H4 需要正确的类型计划与工具效果。正式系统性变异实验已支持其窄主张，但没有解除类型规格和真实生态有效性风险。

## 已淘汰或不投入

- **H1 DQBP**：状态信息增益以更低成本达到相同已知分支成功率，主优势为 0；方法核被公平基线吸收。
- **H2 自动补全后置条件**：与 ToolGate 的缺失契约边界及自动形式化验证/修复最近工作过近，且当前无法低成本获得独立真实契约。
- **H3 新鲜度账本**：STALE/CUPMEM 和 Agent-BRACE 已覆盖写侧裁决、受权读出与不确定信念状态。
- **大规模工具检索正交路线**：ToolRet、Meta-Tool、ToolDreamer、NaviAgent、非负近邻检索和自适应候选数已形成密集强近邻。
- **形式规格验证正交路线**：Verus-SpecGym、往返验证修复、变异测试和主动判别输入已覆盖主要机制空间。

## 仍可能杀死 H4 的因素

1. Reviewer 判断其只是经典最弱前置条件和集合覆盖的直接工程移植，没有足够独立方法贡献；
2. ETAS 的残余义务或 VERIMAP 的计划生成验证函数在正文中已包含等价运行时证据编译；
3. 合成实验与人工类型计划使最大剩余疑问仍是端到端目标对应性；
4. 工具完整契约的额外拒绝反映更强正确性目标，而非不必要成本。

因此，当前状态只足以准备固定三审，不足以由主研究者直接宣布交付。

### Source: `evidence_packet_v001.md`

# 证据清单

## 文献与边界证据

- ToolGate，Findings of ACL 2026：固定霍尔式前置/后置契约与验证提交。https://aclanthology.org/2026.findings-acl.470/
- VERIMAP，2026：规划时为子任务生成验证函数。https://arxiv.org/abs/2510.17109
- Failing Tools，2026：把轨迹约束解释为证据义务和安全不变量。https://openreview.net/forum?id=j7YsSnA64D
- Verified Tool Calls，2026：固定写后验证、重试前验证与幂等键。https://arxiv.org/abs/2608.02645
- ETAS，2026：类型/效果语义、轨迹监控与动态资源残余义务。https://arxiv.org/abs/2607.17780
- AgentCheck，2026：模型上下文协议工具的系统故障注入工作台。https://arxiv.org/abs/2607.11098

以上来源只支持最近边界和问题存在性；它们不自动证明 PDEO 新颖。

## Run 内检索快照

- `hypotheses_v001/searches/initial-scope-001/`
- `hypotheses_v001/searches/orthogonal-tool-retrieval-001/`

## 负结果

- `workbench_v001/scratch_metrics.json`
- `workbench_v001/scratch_details.json`
- `failure_attribution_v001.md`

这些材料只支持 H1 淘汰，不支持 H4 交付。

## H4 Scratch

- `workbench_v001/pdeo_scratch_metrics.json`
- `workbench_v001/pdeo_scratch_details.json`

这些材料用于预检和实现修正，不是交付支撑。

## H4 Formal / Review-support

- `experiment_v001/specs/pdeo-systematic-fault-suite-v1.json`
- `experiment_v001/attempts/attempt-pdeo-formal-002/execution.json`
- `experiment_v001/attempts/attempt-pdeo-formal-002/metrics.json`
- `experiment_v001/attempts/attempt-pdeo-formal-002/formal-details.json`
- `experiment_v001/plan.md`
- `experiment_v001/result.md`

评价规则与 PDEO 编译器在同一实验程序中以独立常量和函数实现；标签函数不调用编译器。该独立性强于自评输出，但仍共享人工类型规格假设，不能等价为真实外部基准。

`attempt-pdeo-formal-001` 是同规格的早期有效运行，但其实现文件身份清单不完整，与最终实现 manifest 不匹配；它保留在 Run 中，不作为交付支撑。001 与 002 的数值指标除墙钟时间外完全相同。

## Evidence Inventory (machine generated)

```json
{
  "comparison_count": 0,
  "comparisons": [],
  "formal_attempt_count": 2,
  "formal_attempts": [
    {
      "association": "MISMATCH",
      "attempt_id": "attempt-pdeo-formal-001",
      "path": "experiment_v001/attempts/attempt-pdeo-formal-001/execution.json",
      "read_error": null,
      "record_sha256": "879c6b9a87c853db7f5c747ab8e404d71894d68c3c59276960be0a36eb217a2e",
      "schema_version": 7,
      "selected_in_core": false,
      "status": "SUCCESS",
      "valid_review_support": true
    },
    {
      "association": "MATCH",
      "attempt_id": "attempt-pdeo-formal-002",
      "path": "experiment_v001/attempts/attempt-pdeo-formal-002/execution.json",
      "read_error": null,
      "record_sha256": "65d6721da32c82b39c624c3cf7a752f7472f588f485494b25b2d3ed0e5aafad4",
      "schema_version": 7,
      "selected_in_core": true,
      "status": "SUCCESS",
      "valid_review_support": true
    }
  ],
  "implementation_key": "0424092c3d015458de5a2033cb9db7ac8bceeede66122a7ccba6bbf5b1062cff",
  "machine_judgment": "NONE_FACTS_ONLY",
  "recorded_attempt_count": 0,
  "recorded_attempts": [],
  "schema_version": 1,
  "version": "v001"
}
```
