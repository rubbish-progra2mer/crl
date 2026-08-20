# Search Failure Log

## 2026-08-13 / SF-001

- `source_name`: Semantic Scholar（Run-local Prior Audit）
- `attempted_query`: h-v001-001/002/003 的最近先行与引文扩展
- `failure_type`: HTTP 429 rate limit；三份审计均 `degraded=true`
- `impact`: 候选发现主要依赖 arXiv 与冻结知识库，不能声称穷尽全部会议与引文图。
- `next_action`: 对实际用于碰撞裁决的 ToolGate、Sherlock、MemTX、Dependency-Guided Rollback Repair、Cordon、ReLoop 等逐一回到一级全文；保留降级事实。

## 2026-08-13 / SF-002

- `source_name`: OpenReview
- `attempted_query`: ReflectAgent、Failing Tools 全文
- `failure_type`: HTTP 403 / 反机器人阻断
- `impact`: 只保留高风险身份线索，不以摘要或搜索片段作方法技术结论。
- `next_action`: 后续可从作者 arXiv 或正式会议页补核；当前致命碰撞由其他已核全文独立成立。

## 2026-08-13 / SF-003

- `source_name`: CRL `audit_prior.py` 标准命令行入口
- `attempted_query`: 绑定含 Evidence ID 的三个假设生成 Prior Audit
- `failure_type`: 未向 `ResearchWorkspace` 注入只读 `KnowledgeStore`，报 `a KnowledgeStore is required when Evidence IDs are supplied`
- `impact`: 标准入口失败；没有修改机器代码。子智能体使用同一 `create_prior_audit` 引擎并显式注入只读共享 `KnowledgeStore`，留下 request/candidates/report 与哈希，但报告需主研究者人工填写。
- `next_action`: 当前 Run 直接使用已保存审计材料；不把兼容调用当作机器认证。机器修复不属于本轮科研必要范围。

## 2026-08-13 / SF-004

- `source_name`: 聚合网页打开调用
- `attempted_query`: 同批打开 AppWorld、τ³、ToolMaze、AgentNoiseBench 官方页面
- `failure_type`: 持续无输出后由主研究者终止
- `impact`: 未从该调用取得任何事实。
- `next_action`: 改用官方 Git `ls-remote`、固定提交原始文件与 GitHub API 只读核验；后续均成功。
