# v130 失败归因

- 失败类型：`MATCHED_ATTRIBUTION_TEST_FAILS_AND_NATURAL_REPAIR_COLLIDES_WITH_TRACE_COMPILATION_PRIOR`。
- 预注册结果：`qwen2.5:7b` 在 `transfer_needed` 上四条件均严格成功 2/8；`qcr_correct-target_plan=0`，`qcr_correct-qcr_shuffled=0`，未达两个至少 4/8 的继续阈值。
- 载体有效：四条件总体响应有效性均为 16/16；目标充分组均为 8/8；所有调用绑定正确且没有来源标识符复制。
- 失败位置：正确 QCR 支持笔记的顺序提取仅 2/8，执行者在 7/8 例与支持顺序一致；主要是支持生成失败，而非支持未激活或未遵循。
- 顺序停止：没有运行 `qwen3:8b`，没有修改提示、顺序族、任务难度或判定阈值。
- 不外推：该结果是抽象合成本地小模型实验，不反证论文在 DeepSeek-V4-Pro、WebArena、WorkArena 和 AppWorld 上的公开系统效果。
- 方法碰撞：显式拒绝/状态不变动作的裁剪是确定性解析；一般轨迹编译、状态图、经验适用性验证和反事实轨迹价值选择已有直接方法及 Run 负记忆。
- 安全边界：实验只调用本机 Ollama，不执行真实工具、不写入外部业务状态、不访问外部网络、不涉及安全过滤绕过；v029 外部执行边界保持不变。
