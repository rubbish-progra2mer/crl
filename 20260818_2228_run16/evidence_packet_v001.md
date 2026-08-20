# v001 证据包：Run16 当前可复查科研证据

## 可运行研究实现

- `implementation_v001/coverage_gate_experiment.py`
- 实现冻结 24 个场景，四个列表/检索域，包含完整存在、完整不存在、截断、作用域错配、陈旧和未知覆盖。
- 核心公平比较 `prompt` 与 `gate` 使用相同模型、相同覆盖元数据、相同最大补查次数、相同零温与种子规则；唯一差异是 gate 在无完整见证时拒绝提交 `absent` 并执行一次全作用域补查。

## Formal Screening

- Spec：`experiment_v001/specs/coverage-gate-screening-v001.json`
- Attempt：`experiment_v001/attempts/coverage-gate-screening-v001/execution.json`
- 原始逐 episode 结果：`experiment_v001/attempts/coverage-gate-screening-v001/results.json`
- 指标：`experiment_v001/attempts/coverage-gate-screening-v001/metrics.json`
- 机械事实：退出码 0；Evidence、metrics 与 output 契约为真；91 次本地模型调用；34,309 tokens；75.97 秒；零付费；无 parse issue。

| 条件 | 隐藏目标错误否定率 | 隐藏目标恢复率 | 正确否定保留率 | 总任务成功率 | 拒答率 | 平均额外查询 |
|---|---:|---:|---:|---:|---:|---:|
| raw | 1.0000 | 0.0000 | 1.0000 | 0.3333 | 0.0000 | 0.0000 |
| prompt | 0.6875 | 0.2500 | 1.0000 | 0.5000 | 0.0417 | 0.1667 |
| gate | 0.0000 | 0.9375 | 1.0000 | 0.9583 | 0.0417 | 0.6250 |

两个预注册主张均达到本地支持条件。gate 并未靠降低正确否定或增加拒答取得表面收益；它主要把 scope/stale/unknown 条件下的错误否定转成一次补查后的正确存在结论。

## 独立公开数据 Screening

- 数据：`workbench_v001/datasets/sgr_bench/constraint_hf.jsonl`；来源与固定哈希见同目录 `PROVENANCE.md`。
- 独立实现：`implementation_v001/sgr_coverage_experiment.py`
- Spec：`experiment_v001/specs/sgr-coverage-validation-v001.json`
- Attempt：`experiment_v001/attempts/sgr-coverage-validation-v001/execution.json`
- 原始逐 episode 结果：`experiment_v001/attempts/sgr-coverage-validation-v001/results.json`
- 指标：`experiment_v001/attempts/sgr-coverage-validation-v001/metrics.json`
- 机械事实：退出码 0；Evidence、metrics 与 output 契约为真；125 次本地模型调用；70,381 tokens；103.22 秒；零付费；无 parse issue。

| 条件 | 隐藏目标错误否定率 | 隐藏目标恢复率 | 正确否定保留率 | 可见存在准确率 | 总任务成功率 | 拒答率 | 平均额外查询 |
|---|---:|---:|---:|---:|---:|---:|---:|
| result-count 回执 | 0.9091 | 0.0909 | 1.0000 | 1.0000 | 0.6970 | 0.0000 | 0.0606 |
| 一般后置条件提示 | 0.4545 | 0.5455 | 0.9091 | 0.7273 | 0.7273 | 0.0303 | 0.2727 |
| gate | 0.0909 | 0.9091 | 0.9091 | 0.9091 | 0.9091 | 0.0303 | 0.4545 |

预注册数值判据全部通过，但必须保留一项偏差：计划固定的 12 个任务中，`reptile_001` 的答案集未被确定性解析器恢复，实际只有 11 个任务、每条件 33 个 episode。gate 仍有一个隐藏目标错误否定、一个完整不存在被误判为存在，以及一个可见存在被判为不确定。此结果使用自然答案集但仍是模拟分页，不是在线工具执行。

## 最近先行差分

- NabaOS 对 absence 的机械验证是 `result_count = 0`；其 false-absence 基准是工具非空而模型声称为空。它证明调用和输出，但未证明空集合覆盖了待否定命题所需的作用域、分页和时间。
- Verified Tool Calls 对非原子写操作进行任务特定后置条件核验与 verify-before-retry；它已覆盖三值 verifier、陈旧与部分状态，是最近的计算级威胁，但把丰富语义完整性验证列为未来工作。
- SGR-Bench 确认 retrieval-scope drift 是主要失败源并建议 source-slice anchored evaluation，但没有运行时覆盖见证/负命题准入。
- CROWN-QA（arXiv:2608.04591）直接形式化“只有证据完整覆盖查询作用域时，未观察才许可负向结论”，提供合成配对与真实文档对照集，并测试结构化 scope/coverage certificate 加固定映射。它已经占据当前问题、形式化、评价和自然文档现象；剩余差分只能是工具原生元数据生成见证、运行时准入和补查系统。
- ToolGate（arXiv:2601.04688）以 Hoare 风格前/后置条件和运行时验证决定工具结果能否提交到可信状态，进一步压缩一般“模型外门控”主张。

## 证据保真与边界

当前仍是 `SCREENING`，不是 `REPRESENTATIVE`：虽已有两个本地模型、两个独立实现和公开自然 answer sets，但分页仍由适配器模拟，第二项实际只有 11/12 个固定任务，且每项仅一个种子。覆盖见证仍由场景/适配器直接提供；尚未证明真实工具能低成本、无答案泄漏地生成见证。不能据此声称真实 API、广义检索可靠性或论文新颖性。

## 当前最大杀手问题

由于 CROWN-QA 已占据评价现象，候选不能再退守“只剩评价”。若真实 API 见证仍须手写完整答案，或者 CROWN-style certificate + 固定规则 / ToolGate-style postcondition 在匹配信息和补查预算后吸收 gate 收益，则当前论文方向应死亡。

## 正交接口演化 Screening

- 候选：`h-delta-contract-001`。
- 结构化先行：`hypotheses_v001/priors/delta-contract-prior-v001/assessment.md`。
- 实现：`implementation_v001/delta_contract_experiment.py`。
- Spec：`experiment_v001/specs/delta-contract-screening-v001.json`。
- 有效 Formal：`experiment_v001/attempts/delta-contract-screening-v001-r1/`。
- 第一次 `delta-contract-screening-v001` 因实验实现输出非 Formal 指标模式而未成为 Recorded 证据；M012 修复后以同场景、模型、种子和判据完整重跑。

| 条件 | 任务成功率 | 模式合法率 | 平均模型调用 | 平均 Token | 近邻反例拒绝率 |
|---|---:|---:|---:|---:|---:|
| latest | 0.8333 | 1.0000 | 1.0000 | 248.58 | 1.0000 |
| diff_prompt | 0.8333 | 1.0000 | 1.0000 | 270.88 | 1.0000 |
| reflection | 0.8333 | 1.0000 | 1.1667 | 347.54 | 1.0000 |
| obligation | 0.8333 | 1.0000 | 1.0000 | 302.38 | 1.0000 |

四种条件均在参数重命名、新必需参数、枚举语义、工具替换和描述语义变化上达到 4/4，在新前置工具上均为 0/4。obligation 相对同信息 diff_prompt 增量为 0，未达到预注册 0.15，因此 `delta-obligation-local-difference-v001` 已 falsified。失败计划能选择正确的 authorize→submit 工具序列，但把上游输出写成未绑定占位符，揭示的是端口级数据流绑定瓶颈；HyperAgent 已以输出—输入端口链接、运行态模式值绑定和缺口扩展直接处理该计算。

证据死亡范围经 M013 纠正：本实验只杀死当前局部实现和本地增量主张，不证明全部接口演化方法族死亡。较宽候选为 `parked`，且不进入最佳集合。

## 状态合同变异与独立运行复现

- 候选：`h-mutant-probe-001`。
- 实现：`implementation_v001/contract_mutation_experiment.py`。
- 完整检查点 Formal：`experiment_v001/attempts/contract-mutation-screening-v001/`。
- 独立部分检查点 Formal：`experiment_v001/attempts/contract-mutation-replication-v001/`。
- 人工标签与机械覆盖校验：`workbench_v001/manual_audits/contract_extra_labels_v001.json`、`contract_extra_audit_v001.json`、`contract_extra_labels_replication_v001.json`、`contract_extra_audit_replication_v001.json`。

| 公开检查点 | 提示匹配 | 原通过 | 通过且含未断言变化 | 人工任务外可疑 |
|---|---:|---:|---:|---:|
| `224804` | 224/224 | 151 | 65（0.4305） | 0 |
| `233808` | 117/117 | 67 | 40（0.5970） | 0 |

第一次 Formal 中，全局 strict 会拒绝测试划分 9/28 个原通过运行；端点允许边界把该拒绝降至 2/28，但对四类风险变异的逃逸率为 0.2722，高于预注册上限 0.25，因此当前加固原型失败。第二检查点只覆盖 117 个任务且同属 Gemini 3 Flash，不能冒充跨模型或完整复现。两次人工核对都只使用公开提示和聚合变化签名，不是完整安全标签；它们足以反证当前预注册实际得分扭曲主张，但不能证明开放世界合同普遍安全。
