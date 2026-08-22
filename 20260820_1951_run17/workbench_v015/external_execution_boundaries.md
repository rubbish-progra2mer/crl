# v015 外部执行边界

## 既有 episode 中断

用户声明上一 Codex execution episode 被平台侧网络/安全访问控制中断。该事实仅作为外部执行 episode 中断保留，不作为科研反证、机械失败或 Run 终局；Run17 继续保持 `ACTIVE`。

## 本 episode 的网络结果

- 公开 arXiv 一手论文页面：标准访问成功。
- `meta-agents-research-environments/gaia2` 公开数据集：通过 Hugging Face 数据集服务器公布的标准 Parquet 端点取得五个核心验证配置；每个文件下载字节数与端点元数据一致，后续 SHA-256 见 `audit/gaia2_task_read_opportunities.json`。
- Gaia2 排行榜 Space 源码：标准浅克隆成功，冻结修订为 `0304454f7a36f66399d191b5cf7293b0e2b03e17`。
- 排行榜后台 `meta-agents-research-environments/leaderboard_results`：未认证的标准数据集服务器请求返回 HTTP 401 `Unauthorized`。该仓库在排行榜源码中用于汇总结果，但当前没有授权令牌；未尝试绕过认证、复用他人会话或改走规避通道。因此，真实提交轨迹的工具调用发生率在本 episode 仍不可核验。

边界解释：401 是外部服务认证边界，不是科研阴性，也不是平台安全拒绝。当前后续动作改用公开 800 场景任务机会分母与本机冻结源码重放；不得把任务机会分母写成真实模型调用率。
