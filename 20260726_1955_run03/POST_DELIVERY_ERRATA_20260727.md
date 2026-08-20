# run03 交付后勘误（POST-DELIVERY ERRATA，2026-07-27）

**性质声明**：本文件是交付（2026-07-26，DELIVERY.md SHA fa8648aa62dabc472d4f98cb92e778c549d87cf81309e1e1c8d71decf1db82d0）之后，由主 Codex 在用户批准的 2026-07-27 机器优化轮中，依据同日独立冻结字节审查发布的勘误。它**不属于**本 Run 的冻结评审链（未经过三审），**不修改**本 Run 的任何既有字节；全部冻结产物保持原样。接收方阅读顺序：本文件 → DELIVERY.md → decision_v001.md → 冻结文档。缺陷编号见机器登记簿 `crl_agent_v3/MACHINE_DEFECT_REGISTRY.md`。

## §1 绑定勘误 E7 的执行本身不实（MD-14）——room_type 类别从未被 selftest 覆盖

DELIVERY.md「harness 保真证据」段声称 probe–checker selftest「覆盖全部四类 local 类别（idx001 600 比较 + 裁决前置补跑 idx064/122/135 共 600 赋值双向一致）」；`decision_support_v001/verification_notes.md` 声称 idx122 为 "house_rule + room_type + transportation 适用"。**两者均不成立**：

- 从冻结字节即可复核：三个 selftest 结果文件的 comparisons 计数为 800/1000/1000（每赋值 4/5/5 个类别），四类全覆盖需要 1200；用冻结 `tp_solve_probe.py` 对冻结 selftest 实例重建适用性，idx122 与 idx135 的 **room_type 探针断言均为 None（域内无 Shared room 违规选项）被静默跳过**。readiness 阶段的 idx001 也不含 room_type。
- **影响方向有限**：D 桶 room_type 零证书故障、只出现在 enforced 分母侧，若藏 bug 只会压低 M2（对 SIG-1 保守）；W 桶 idx078 的 room_type masked witness 有独立检查器复核 SAT 方向背书。核心 masked 证书（idx120 cuisine）不受影响。
- **但结论必须更正为**：probe–checker selftest 的实测覆盖为 cuisine / house_rule / transportation 三类 local 类别 + 全局类别；room_type 的探针编码从未被任何 selftest 双向验证。一个专为闭合"覆盖夸大"异议而做的补丁自己再次夸大了覆盖，且三审、裁决、交付全链无人发现——这是同模型评审链共同盲区的实证（已推动规约层修复：跨家族对抗通读、Reviewer 对修复声明的同等怀疑义务）。
- 待办（属种子升级 Run 工作）：补跑一个域内含 Shared room 违规选项的实例 selftest，双向验证 room_type 探针编码。

## §2 时间线勘误（MD-15）——修正事件之后的账本条目仍然全部超前

RUN_LEDGER.md 的 CORRECTION_TIMESTAMPS 事件披露了叙事时钟超前并修正了 8 条（自称 "six earlier entries"，实列 8 项——本身是一处笔误）。但**修正事件之后的全部 7 条条目仍超前 18–45 分钟，且从未再修正**；账本文件自身 mtime（21:56:13）早于其末条自称时间（22:40），构成自我矛盾。以下为按文件 mtime（经 DeepSeek 服务端 `created` 时间戳交叉锚定，两者秒级吻合，排除 mtime 被改的替代解释）重建的真实时间线（Asia/Shanghai，2026-07-26）：

| 事件 | 账本 AT | 实测真实时间 |
|---|---|---|
| RUN_CHARTER 落盘 | 19:55:49（RUN_CREATED） | 19:56:26（含付费预授权更新） |
| 分桶承诺 MANIFEST | 20:52 | **20:24:06**（超前 28 分钟且不在修正清单内） |
| z3 例外环境创建 | 修正值 ~20:40 | **20:26:05**（修正值本身仍余 14 分钟误差） |
| Workbench falsifier 报告 | 修正值 ~20:58 | **20:44:13** |
| nearest_prior 定稿 | 22:20（修正 ~20:52） | **20:48:06**（其正文内嵌"写入时间 22:10"亦为坏时钟产物） |
| Experiment Plan 冻结 | 23:30（修正 ~21:03） | **21:04:11** |
| dev_001 capture 完成 | 21:35 | **21:14:16**（execution.json 落盘） |
| Review Packet 冻结 | 21:52 | **21:22:58** |
| 三位 Reviewer staged 报告 | "launched 21:57" | **21:42:26 / 21:44:42 / 21:46:15**（三份 staged 文件 mtime） |
| 正式报告保存 | 22:20 | **21:50:17** |
| Decision | 22:35 | **21:52:50** |
| DELIVERY | 22:40 | **21:55:30** |
| 账本末次写入 | — | **21:56:13** |

**结论**：全链真实用时 2 小时 0 分（19:55:49–21:56:13），非账本表观的 2 小时 45 分。全部因果关键顺序（分桶承诺先于任何实例内容读取、plan 冻结先于 dev_001 启动、packet 先于 staged 先于保存先于 decision 先于 DELIVERY）**经真实时钟验证成立且比账本更强**；特别地，"staged 报告 mtime（21:42–21:46）早于账本宣称的 launch（21:57）"是坏时钟造成的表观假象而非评审造假——真实 launch 在 21:23–21:25 之间（packet 冻结 21:22:58 之后）。账本 AT 字段作为审计工具已失效，请一律以本表为准。规约层修复：CRL.md §6 Ledger 时间纪律（AT 必须取自实际取时命令）+ inspect_run 的 AT 卫生检查已于 2026-07-27 生效。

## §3 路线图顺序自毁矛盾更正（MD-16）

DELIVERY.md 的否证成本序「跨模型复跑 → **180 全量验证集复算** → C 桶预注册 Confirmation」存在顺序矛盾：180 行验证集含 33 行 C 桶，先执行"180 全量"就烧毁了 C 桶的 untouched 性、作废第 3 步预注册 Confirmation。**更正为**：

1. 跨模型复跑（<$1）；
2. **W+D 147 行**全量复算（收紧 M2 CI，不触 C）；
3. C 桶按原预注册计划一次性执行（≈其中 SC3 实例约 11–12 个；功效警告 [E13] 不变，不得回改门槛）；
4. （C 消耗后）如需更大 N，才允许触及完整 180 行口径的重算。

## §4 执行通道说明

本 Run 已 DELIVERED、不可恢复；上述待办与 DELIVERY 路线图中机器包络内的步骤（跨模型、147 行全量、近均匀 λ、VeriSimpl 型裁决探针补臂、C 桶执行、room_type selftest 补验），自 2026-07-27 起可经用户明示授权的 `MODE: SEED_UPGRADE` Run 合法执行（CRL.md §6"种子升级 Run"）；该 Run 只读取本 Run 冻结产物、产出 `DELIVERY_ADDENDUM.md`，不修改本 Run 任何字节。
