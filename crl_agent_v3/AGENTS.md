# CRL Agent v3 机器代码库规则

- 处理 CRL 代码、文档或 Run 前完整阅读 `CRL.md`；需要本机执行时再读 `CRL_ENVIRONMENT.md`，需要 Reviewer 细节或文件示例时分别读 `CRL_REVIEWER_PROTOCOL.md`、`CRL_RUNTIME_TEMPLATES.md`。这些说明不得形成第二套科研流程。
- `CRL.md` 是正式 Research Run 的唯一完整科研权威；本文件只约束机器代码库的工程修改与文档路由，不重新定义候选、碰撞、版本、实验充分性或终局。
- 新写入的 `CONCLUDED_NO_DELIVERY` 只属于 Charter 与 Status 均声明 `MODE: DIRECTED` 的窄方向 Run。默认宽 AUTONOMOUS Run 的正常科学终局只有 Delivery；暂未找到合格方向、候选耗尽、局部失败、运行较久或多次验证无效都要求在授权仍有效且无不可越过外部边界时保持 `ACTIVE` 并继续探索。已有历史 No-Delivery（包括 AUTONOMOUS）仍可只读解析、审计和由用户显式恢复，但恢复后的 AUTONOMOUS 版本不得再次写入 No-Delivery。
- 机器维护、代码修改、测试和文档整理只实施用户当前明确批准的范围，发现旁支问题只记录；这条 scope restraint 不适用于已创建 AUTONOMOUS Research Run 在 Charter 内的科研行动，后者无需逐步骤或逐版本取得许可。
- 产品根、机器根、共享知识库和外置环境的位置以产品根 `AGENTS.md` 与 `CRL_ENVIRONMENT.md` 为准。不得把环境、模型、运行时或跨 Run 科研材料搬入机器目录。
- Contract、固定 Reviewer、Formal/Review-support、Delivery 绑定和知识库科学内容属于高完整性边界；除非用户当前任务明确授权相应模块，不得顺手修改、迁移、重建或改变其语义。知识库维护例外仍须遵守 `CRL.md` 的显式范围与回归要求。
- 工具可维护路径、编码、身份、哈希、真实执行记录和兼容读取；不得自动生成科研 Claim、认证 Novelty、判断实验充分性、淘汰 Candidate、结束 Run 或把可选能力变成 Gate。
- 修改应遵循 Minimum Sufficient Engineering：优先修复现有规则、薄工具和已确认 bug，不为未来扩展新增状态机、后台服务、重复 Gate、跨 Run memory、自动调度或第二套基础设施。
- 保留用户已有和无关改动；按风险运行必要窄测试与明确要求的回归，不得捏造通过结果。代码和研究文本会被其他 AI 同行复核，应保持实现、测试和报告可审计。
- 修改文本前确认编码、BOM 与换行；研究文本使用 UTF-8 无 BOM、LF。PowerShell 5.1 读取 Markdown 时显式使用 `-Encoding UTF8`。
