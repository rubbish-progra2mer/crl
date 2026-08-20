# Decision-support verification notes (v001, post-review, pre-decision)

执行者：主 Codex；日期 2026-07-26。本目录内容是主 Codex 阅读三份 Reviewer 报告后的裁决前置核验，
不进入 Promotion/Confirmation 证据，不修改任何冻结 bytes。

## 1. 扩展 probe–checker 一致性 selftest（回应 Reviewer 2 异议 5-2）

冻结 readiness selftest 只覆盖了无 local 约束的 idx001（200 赋值 × 3 类别 = 600 比较），
plan.md 的"全类别"表述被 Reviewer 2 正确指出不成立。补跑（frozen tp_solve_probe.py selftest
模式，frozen tp_lib 检查器，z3 例外环境，W 桶实例，无 API 调用）：

- selftest_instance_idx064.json（cuisine ×2 适用）→ selftest_result_idx064.json：200 赋值，0 不一致。
- selftest_instance_idx122.json（house_rule + room_type + transportation 适用）→ 0 不一致。
- selftest_instance_idx135.json（cuisine ×4 + room_type + transportation 适用）→ 0 不一致。

结论：全部四类 local 约束类别的探针编码（双向：probe-true ⟺ checker-violated）在含约束实例上
经系统随机赋值验证一致。Reviewer 2 指出的"UNSAT 方向无系统验证"缺口在这些类别上已闭合；
plan.md 的表述错误在 Decision 中以 erratum 记载。

## 2. 近邻自认引语核验（回应 Reviewer 1 异议 6.4）

- ReLoop（arXiv 2602.15983，HTML v2）：句子 "Solver feedback catches syntax errors, not missing
  constraints; LLM self-critique inherits the reasoning gaps that caused errors; ..." 逐字存在，
  locator：§1 Introduction。91.1%/0.5% gap 句同在 §1，另见 Table 5（DeepSeek-V3.2 行）。
- Constraint Injection（arXiv 2606.04816，HTML）：句子 "Developing decoupled evaluation metrics
  that reflect independent constraint-violation profiles at finer granularity remains an open
  problem" 逐字存在，locator：Limitations。非 binding 掩盖概念句："a candidate may introduce a
  spurious constraint or omit a required one while still matching the reference optimum, whenever
  the affected constraint is non-binding"，locator：Introduction。

结论：candidate/research map 所引两条自认均可给出精确 locator，无需降级。

## 3. C-GATE-1 功效重算（回应 Reviewer 2 异议 5-8 / Reviewer 3 异议 5.8）

按 D 点估计 p̂ = 1/21 ≈ 0.0476：C 桶预期 SC3 ≈ 11–12，F1-ok∧PASS ≈ 9–10；
P(masked ≥ 2 | n=9, p̂) ≈ 6.5%，P(masked ≥ 2 | n=10, p̂) ≈ 7.9%；P(masked = 0 | n=10, p̂) ≈ 61%。
即 C-GATE-1 是严酷 stability gate：失败无法区分"现象不稳定"与"功效不足"，通过则为强证据。
该数字组随 DELIVERY 移交并禁止接收方看到结果后回改门槛。
