# P047 Codex 首读：tau2-bench

- 状态：`DRAFT_BEFORE_SECOND_READ`
- PDF：`knowledge_base/staging/papers/P047_tau2_bench.pdf`
- PDF SHA-256：`0817e3fd33915326180d548caa900dcc5cba42ded27688105d8ce2f7e73aad84`
- 读取范围：全文，重点为 dual-control 设计、oracle-plan/no-user ablation、难度分解和 simulator error audit。

## Changed evaluation

- [AUTHOR_FACT] 将用户也建模为具有私有目标与工具权限的交互主体；Agent 必须通过对话协调双方动作，而不是单方面完成预设工具链。
- [AUTHOR_FACT] 114 个正式任务从 2,285 个程序生成任务中采样，覆盖 airline、retail、telecom；以 database state、policy compliance 与沟通结果联合判定。
- [CODEX_SYNTHESIS] 其核心价值是把“模型会不会调用工具”拆成“已知计划执行能力”和“从不完美用户交互中发现、协调计划的能力”。

## 关键结果与边界

- GPT-4.1 在 retail/airline/telecom 的 pass^1 约为 0.74/0.56/0.34；telecom 上 no-user 为 0.52、oracle-plan 为 0.73，说明 dual-control 本身造成显著落差。
- o4-mini telecom 为 0.42，no-user 0.67，oracle-plan 0.96；动作数超过 7 后默认设定接近零成功。
- 用户模拟器并非 oracle。人工审计显示各域均有 simulator 错误；telecom 表格记录 3/50 critical 与 5/50 benign，而正文一处“无 critical error”的表述与表格/附录冲突，需二读核对。
- 本项目明确不把环境反馈学习与执行恢复作为研究方向；本论文只作为评测载体和失败归因证据，不抽取该方向 Operator。

## Evidence 草案

| Evidence ID | kind | section / page | locator | Codex note |
|---|---|---|---|---|
| P047-E01 | evaluation | benchmark design | dual control | [AUTHOR_FACT] 双方私有状态与动作权限。 |
| P047-E02 | result | ablations | default/no-user/oracle-plan | [AUTHOR_FACT] 协调计划发现与已知计划执行的落差。 |
| P047-E03 | limitation | simulator audit | critical/benign errors | [AUTHOR_FACT] 评测用户模型会污染 Agent 失败归因。 |
| P047-E04 | conflict | main text vs table/app. | telecom critical errors | [CODEX_SYNTHESIS] 来源内部数字/措辞冲突。 |

## Card 草案（不进入正式 Cards）

### Failure — `DRAFT_BEFORE_SECOND_READ`

- 名称：`User-Simulator Error Contaminates Agent Failure`
- 现象：评测将模拟用户的提前结束、错误工具动作或信息遗漏计入 Agent 失败，掩盖方法真实差异。
- 边界：只能用于要求 simulator audit 和分层报告，不能据此自动修正分数。

## 首读裁决

`KEEP_FOR_SECOND_READ_AS_EVALUATION_CARRIER`。不建立环境恢复方向 Operator；二读重点解决 simulator audit 内部冲突。
