# v006 实现说明：逐坐标可能相关包络

本目录实现结构化列表连接器上的联合范围证据协议。v006 修复 v005 的跨坐标分裂：外层请求键与规范载荷键不再需要任一侧先完整匹配主张，才有资格进入一致性检查。

## 文件

- `joint_coverage_kernel.py`：生产求值、逐坐标预检、页链追踪、修复义务与证书模式 6。
- `independent_certificate_verifier.py`：不调用生产求值器或追踪器的第二实现路径；独立解析规范载荷并重算包络、页链和证书条件。
- `run_soundness_counterexamples.py`：150 项本地攻击与可用性对照。
- `test_joint_coverage_kernel.py`：41 项单元测试。
- `run_joint_coverage_experiment.py`：结构化半真实夹具与七方法回归。
- `compare_v005_v006_regression.py`：在相同 756 任务、5 档预算上逐行比较 v005 与 v006。
- `run_kernel_tests.py`：单元测试运行入口。

## 请求身份

`SourceIdentity` 包含：连接器、操作、认证主体、范围模式版本、适配器版本、语义规范化版本和请求序列化版本。`RequestKey` 还包含联合单元、游标与快照。规范 JSON 的字段集合、非空字符串、游标类型、排序和紧凑序列化均须精确匹配。

`semantic_normalization_version` 只把连接器级规范化方案绑定进请求与证书；它不证明方案正确。条件声音性仍要求：同一连接器响应语义的等价请求映射为唯一请求键。

## 逐坐标可能相关包络

令 `F` 为七个来源身份坐标，`U` 为主张联合范围。对有效载荷解析得到的 `K_outer` 和 `K_payload`：

```text
source_possible =
  对每个 f∈F：K_outer.f = C.f 或 K_payload.f = C.f

snapshot_possible =
  K_outer.snapshot = C.snapshot
  或 K_payload.snapshot = C.snapshot

scope_possible =
  K_outer.cell ∈ U
  或 K_payload.cell ∈ U
  或存在 record.cell ∈ U

possibly_relevant =
  source_possible 且 snapshot_possible 且 scope_possible
```

只要观察进入这个包络，`K_outer != K_payload` 或任一 `record.cell != K_payload.cell` 就使整项主张返回 `UNKNOWN`。这会捕获“期望来源只在一侧、期望快照只在另一侧、范围信号只在记录侧”的 v005 反例。

若两键完全相同，则实现采用等价快速路径：来源身份、快照必须完整匹配，范围信号可来自请求单元或记录单元。自洽的真正异源页和请求/记录均范围外的页面仍可忽略。

## 非规范载荷

载荷解析结果是“有效键”或“显式错误”的全状态。对任何已保留且已认证的观察，只要载荷不能严格规范解析，就没有声音的载荷路由键；当前实现把它作为所有主张的全局冲突并返回 `UNKNOWN`。这关闭“范围外请求＋范围内记录＋非规范载荷”组合，但会让真正异源的非规范页污染无关主张。该可用性代价在攻击面板中显式保留。

## 证书与边界

证书模式版本为 6。`audit_observation_digests` 是当前可能相关谓词选中的、求值器已收到的观察摘要排序多重集。它可以让加入已识别冲突页后的旧证书失效，但不证明：

- 外部输入日志完整；
- 相关谓词一般完备；
- 适配器载荷等于真实出站请求；
- 响应与记录请求在并发、重试或缓存下正确关联；
- 语义规范化映射正确。

第二路径是归一化观察级的独立实现，不是形式化证明或传输级外部真值裁决。

## 性能实现

最终字节缓存冻结对象的来源键、载荷解析、摘要及第二路径派生键，并在同一次求值内复用预检。缓存键由完整不可变输入构成，不跨主张复用主张相关判定。逐行正式比较显示，v005 与 v006 的 26,460 行配置和 13 个行为字段均为零差异；初始观察摘要因新增语义规范化版本而主动排除比较。

## 正式结果入口

- 150 项攻击：`coordinate-closed-counterexamples-r3-v006`
- 41 项测试：`kernel-tests-41-r3-v006`
- 同配置 26,460 回归：`coordinate-closed-joint-coverage-756x5-r4-v006`
- v005/v006 逐行比较：`v005-v006-clean-regression-v006`
- 扩大压力回归：`coordinate-closed-joint-coverage-756x5-r3-v006`，实际为 7,560 任务、105,840 回合。

两次早期大规模尝试因未优化重复预检而被主研究者终止，均无结果文件且证据契约失败；它们只作为性能失败记录，不支持当前实现。
