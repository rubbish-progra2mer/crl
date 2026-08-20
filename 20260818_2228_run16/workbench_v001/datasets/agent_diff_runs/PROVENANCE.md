# Agent-Diff 公开运行检查点来源

- 来源仓库：`agent-diff-bench/agent-diff`
- 路径：`experiments/kdd 2026/evaluation_outputs/checkpoints/checkpoint_20260201_224804.json`
- 获取日期：2026-08-18
- 用途：检查公开实际运行是否保存完整状态差分，以及原通过运行中是否存在合同断言之外的变化。
- 原始地址：`https://github.com/agent-diff-bench/agent-diff/raw/refs/heads/main/experiments/kdd%202026/evaluation_outputs/checkpoints/checkpoint_20260201_224804.json`
- 文件大小：48,403,311 字节
- SHA-256：`cdb70cc8606674867f51bee48c330d84c4bc6243ce547d1c21c8e8f4c10071ea`

## 独立部分检查点

- 路径：`experiments/kdd 2026/evaluation_outputs/checkpoints/checkpoint_20260201_233808.json`
- 原始地址：`https://github.com/agent-diff-bench/agent-diff/raw/refs/heads/main/experiments/kdd%202026/evaluation_outputs/checkpoints/checkpoint_20260201_233808.json`
- 文件大小：5,600,781 字节
- SHA-256：`3151fb3240ebadc5939995252b8c9e8cea5ca7391309ab5472c41c6e87f60539`
- 内容边界：同为 `google/gemini-3-flash-preview`，保存 117 个独立运行；与完整检查点有 117 个任务标识重合，但运行标识全部不同，故可用于同模型第二次运行筛选，不可冒充完整 224 任务复现。

这些材料只属于 Run16，不写入共享知识库，也不启动原仓库服务。
