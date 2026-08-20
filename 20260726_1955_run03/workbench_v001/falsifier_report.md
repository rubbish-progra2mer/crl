# Workbench v001 — K1 决定性前置反证报告

日期：2026-07-26（Asia/Shanghai）。执行者：主 Codex。数据角色：全部实例来自预承诺 W 桶
（data_split_commitment_v001，manifest SHA dfeaf9fe4688f9388576c6fbd36960eb095d1262bd8e2cf7e4c078551776dc7e）。
本报告只能杀伤或授权继续，不构成 Promotion、Confirmation、Review 或 Delivery 证据。

## 被攻击的必要箭头

K1 最弱必要箭头：**多约束 agent 规划载体上，自由形式形式化的 enforcement 故障中存在
非零质量被解级成功掩盖**（掩盖质量≈0 即 kernel 死亡）。

## 设置

- 载体：TP-SC3（TravelPlanner 验证集单城 3 日全槽位变体；deviations 见 wb_lib.py 头注释）。
- 被试：deepseek-chat（响应 model 字段 deepseek-v4-flash），temperature 0，单次调用，
  自由形式条件（提示不枚举约束类别；成本公式与结构规则给出；query 原文照付）。
- 接口合同：harness 建立决策变量与域界；被试生成 add_constraints(s, choices, data)；
  runtime data 不含 local_constraint 金标注（约束必须从 NL query 编码）。
- 探针：对每个适用类别，在生成模型可行集内 SAT 查询"违反参考条件"（z3 4.15.4，
  例外环境 .venv_z3）；SAT 证据经 stdlib 参考检查器复核（witness_violates_reference）。
- 实例：22 个 W 桶 SC3 实例（19 个含 local constraint 的 medium/hard 优先 + 3 easy）。

## 结果（完整原始数据：out/falsifier_summary.json、out/falsifier_aggregate.json、逐实例 out/idxNNN/）

| 量 | 值 |
|---|---|
| 尝试 | 22 |
| 形式化成功且默认解 SAT | 16 |
| default UNSAT（过约束/编码错误，错误信号可见） | 5 |
| formalization_error（执行失败，错误信号可见） | 1 |
| 解级 PASS（认证通过） | 14 |
| **PASS 且 ≥1 类别未 enforce（掩盖，证书背书）** | **4（4/14 ≈ 29%）** |
| 未 enforce 类别计数 | cuisine 3、house_rule 2、room_type 1 |
| 未 enforce 且被解级检查抓住（caught） | ≥1（idx122 house_rule） |

典型掩盖案例 idx064：query "we enjoy American and Indian cuisines"；生成模型编码为
"每家所选餐厅须为 American 或 Indian"（成员归属量词结构），参考语义为"两种菜系均须
至少出现一次"（覆盖）；探针证明模型允许 American 零覆盖方案（witness 经检查器复核违规），
默认解碰巧双覆盖 → 静默误译被解级认证掩盖。

## 判定

否证条件未触发（掩盖质量显著非零；且并非全部故障都伴随错误信号）。K1 获授权进入
全量冻结实现。附带观察（供实验设计，不作证据）：过约束 UNSAT 率不可忽略（5/22），
错误信号臂（A2）在正式实验中必须与掩盖臂同时报告；cuisine 的量词结构误译是重复出现
的故障形态。

## 工件清单（本报告引用后冻结，后续迭代须用新文件名）

- wb_lib.py、wb_prompt.py、wb_formalize.py、wb_solve_probe.py、wb_run.py
- out/falsifier_summary.json、out/falsifier_aggregate.json、out/deepseek_raw.jsonl、out/idx*/
- API 用量：约 35.4k tokens（deepseek-v4-flash），费用约 0.01–0.03 USD 量级。
