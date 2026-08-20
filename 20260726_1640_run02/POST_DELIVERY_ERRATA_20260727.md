# run02 交付后勘误（POST-DELIVERY ERRATA，2026-07-27）

**性质声明**：本文件是交付（DELIVERY.md SHA 0e1d17dcecbf2786464c13b6d5432c5b87826905138bf72519ddb3038f8ff6fb）之后，由主 Codex 在用户批准的 2026-07-27 机器优化轮中，依据同日独立冻结字节审查发布的勘误。它**不属于**本 Run 的冻结评审链（未经过三审），**不修改**本 Run 的任何既有字节。接收方阅读顺序：本文件 → DELIVERY.md → decision_v007.md（绑定勘误 E1–E10）→ 冻结文档。缺陷编号见 `crl_agent_v3/MACHINE_DEFECT_REGISTRY.md`。审查独立复算结论先行：**本 Run 全部进入 Claim 天花板、errata、DELIVERY 的数字经逐位复算零失配**；以下勘误均在该结论之外。

## §1 缺陷句 → 勘误对照表（降低自底向上阅读的误读面）

冻结 v007 文档保留了三处已被 decision_v007 绑定勘误纠正的原句；按阅读顺序纪律它们已被覆盖，此处给出机械对照：

| 冻结缺陷句 | 位置 | 权威更正 |
|---|---|---|
| "4/22 vs 3/15" 交叉表 | research_map_v007.md 撤回段 | ERRATUM E1：修正判分下为 5/22 vs 3/15（Fisher p=1.0），结论不变 |
| "flagged in the verdict table context" | problem_v007.md 修复点 3 | ERRATUM E2：冻结 verdict 表无 flag 字段，该子句撤回 |
| "reported both as 37-item and 36-item where material" | problem_v007.md 修复点 3 | ERRATUM E3：36 项聚合在 E3 中给出（21/36 等），不在冻结正文 |
| candidate_v005 kernel 句（"causally decomposes… at equal budget"） | candidate_v005.md | ERRATUM E9：接收方一律使用 E9 措辞（DELIVERY 已逐词转写） |

## §2 时间线勘误（MD-15）——账本叙事时钟整体超前 4–6 小时

RUN_LEDGER.md 的 AT 字段由叙事时钟写成，系统性超前真实墙钟；账本文件自身 mtime（2026-07-26 19:28:50）早于其若干条目自称时间（22:30 / 23:59 / 00:45 / 01:15+1d），构成自我矛盾。按文件 mtime 重建的关键真实时间（Asia/Shanghai，2026-07-26）：

| 事件 | 账本 AT | 实测真实时间（mtime） |
|---|---|---|
| v005 Plan 冻结 | 21:30 前后（V005 事件） | **17:54:31** |
| v006 reader raw 完成 | 22:30 前（V006 事件） | **18:17:57** |
| v006 Packet 冻结 | 22:30 | **18:22:29** |
| v006 三报告保存 | 23:59 | **18:50:38**（reviewer_1） |
| decision_v006 | 23:59 | **18:52:07** |
| problem_v007 | 00:45(+1d) | **18:55:09** |
| v007 Packet 冻结 | 00:45(+1d) | **18:57:41** |
| v007 三报告保存 | 01:15(+1d) | **19:24:35**（reviewer_1） |
| decision_v007 | 01:15(+1d) | **19:26:45** |
| DELIVERY | 01:15(+1d) | **19:28:09** |

事件间因果顺序与 mtime 完全一致（先 packet 后报告后 decision 后 DELIVERY），证据链实质完好；失效的只是 AT 审计面。另：账本事件的物理排列既非正序也非倒序（MD-19），重建历史请按本表或按 mtime。规约层修复（AT 取自实际取时命令、正序追加、inspect_run AT 卫生检查）已于 2026-07-27 生效。

## §3 Token 总量更正（MD-17）

DELIVERY.md「Environment and raw experiments」段的 "Total API usage across the run: ~371k in / ~25k out tokens" **入方向数字无冻结字节支持**：账本（RUN_LEDGER API_USAGE_CUMULATIVE）与对 v005/v006 raw 逐行 usage 求和均得 **247,408 in / 24,663 out**。出方向吻合；~371k 疑为把 123,704 重复计入（247,408+123,704=371,112）。金额结论（≈1 USD）不受影响。以 247,408 in / 24,663 out 为准。

## §4 计数小误更正（MD-19）

- 账本 V007 事件称 packet "65 supplemental files"：manifest 实测 64 条、磁盘 64 个文件。
- （v006 轮同类口误 "55 items" 实 54，已由当轮 Reviewer 2 指出，此处一并归档。）

## §5 执行通道说明

本 Run 已 DELIVERED、不可恢复；DELIVERY 路线图中机器包络内的步骤（encoder sweep、paraphrase ablation、更强 reader、C 桶按 E10 协议执行）自 2026-07-27 起可经用户明示授权的 `MODE: SEED_UPGRADE` Run 合法执行（CRL.md §6）。审查建议（供用户决策，非绑定）：2026-07 外部检索显示本方向已被 STALE/FRESCO/MemStrata/A-TMA 等密集占据，投入任何扩大之前应先人工复核 A-TMA（arXiv 2607.01935）与 FRESCO（2604.14227）全文以确认"granularity/propagation 机制归因分解"是否仍空；若决定继续，两个"生死实验"（现代编码器扫描、paraphrase ablation）应先于一切其他步骤。
