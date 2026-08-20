# CRL 机器复查记录

本文件只记录 CRL 机器缺陷及其重跑状态，不属于任何科研 Run，不进入 Recall 或共享知识库，也不作为科研证据。

## M001：τ² 环境断言中的预期实体缺失被误记为机械失败

- 时间、Run 和科学版本：2026-08-20 11:10（Asia/Shanghai）；独立校准工作区 `reward_calibration_v001`；不属于科研 Run。
- 状态：`RESOLVED`
- 症状与可复查文件：14B 冒烟尝试 `preflight-smoke-auxiliary-qwen3-14b/attempt-001` 中，`create_task_1_with_env_assertions` 的轨迹没有创建预期任务；τ² 环境评价器查询 `task_2` 时抛出 `ValueError: Task task_2 not found`，适配器把所有异常一律记为 `runner_failure`。
- 缺陷类型：机械缺陷。它会把可归因于候选轨迹的科学失败误计为运行器故障，从而错误阻断预检。
- 修改内容：仅当异常是 `ValueError`、消息表示预期实体不存在，且回溯明确经过 `evaluator_env.py` 时，记录为 `completed` 科学失败；其余异常继续作为 `runner_failure`。保留异常类型、脱敏消息和日志清单。
- 受影响的候选、实验和结论：`tau2-auxiliary-qwen3-14b` 冒烟尝试 001 的机械失败率无效；6 个通过和其余明确完成的科学结果保留，但该尝试不用于放行。
- 执行的测试：`tests/test_scientific_search_calibration.py`，15 项通过。
- 必须重跑的材料：完整 10 项 14B 冒烟块，使用新 attempt，不只补单题。
- 重跑结果：完整 10 项 `attempt-002` 得到 8 项科学通过、2 项科学失败、0 项机械失败；评价器锁前后有效。

## M002：Windows 非 UTF-8 模式使 τ² 电信域资源无法读取

- 时间、Run 和科学版本：2026-08-20 11:24（Asia/Shanghai）；独立校准工作区 `reward_calibration_v001`；不属于科研 Run。
- 状态：`FIXED_PENDING_RERUN`
- 症状与可复查文件：`preflight-low-auxiliary-qwen3-14b-a/attempt-001` 的 8 个电信任务均在约 5 毫秒内以 `UnicodeDecodeError` 失败；解释器为 `utf8_mode=0`、首选编码 CP936，τ² 资源为 UTF-8。
- 缺陷类型：机械缺陷。它使电信域没有进入模型执行，不能算作候选科学失败。
- 修改内容：Windows 启动器在 UTF-8 模式关闭时，以 `PYTHONUTF8=1` 和 `PYTHONIOENCODING=utf-8` 原参数重启；核心执行函数拒绝在 Windows 非 UTF-8 模式下直接运行，避免生成部分无效块。
- 受影响的候选、实验和结论：`tau2-auxiliary-qwen3-14b` 低保真尝试 001 整体不用于门槛判断；其中 16 个科学失败只作诊断事实，不与后续尝试拼接。
- 执行的测试：校准目标测试 16 项通过；在 `utf8_mode=0` 的 Windows 解释器中直接调用启动器 `--help`，子进程正常返回。
- 必须重跑的材料：完整 24 项 14B 低保真块，使用新 attempt。
- 重跑结果：待重跑。
