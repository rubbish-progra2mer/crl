# CRL 工作区入口

- 与用户交互始终使用中文；不得捏造已阅读文献、已运行命令、实验结果、Reviewer 意见、文件状态或系统能力。
- 用户请求理解、修改、初始化或运行 CRL 时，先阅读 `crl_agent_v3/AGENTS.md`，再完整阅读 `crl_agent_v3/CRL.md`。需要本机实验时再阅读 `crl_agent_v3/CRL_ENVIRONMENT.md`；Reviewer 与文件示例分别按需读取其协议和指南。
- 产品根固定为 `D:\Desktop\crl`，机器根固定为 `D:\Desktop\crl\crl_agent_v3`，共享论文知识库固定为 `D:\Desktop\crl\knowledge_base`；Run 是产品根的直接子目录。环境、运行时与大容量资源位置只以 `CRL_ENVIRONMENT.md` 为准。
- 用户只说“开始运行”时，直接创建 Contract v3 新 Run，由主 AI 研究者在文本与工具型大语言模型智能体领域自主选题；不要求用户补方向，不扫描旧 Run，也不执行机器验收、健康检查或启动测试。用户给出的领域内方向成为更窄 Charter 边界；领域外请求不创建 Run。
- 普通启动不恢复历史 Run。Contract v2 只读、可审计、不可恢复；已终局的 v3 Run 只有在用户明确指定后才核验历史并按 `CRL.md` 处理，`TERMINATED_BY_USER` 永不恢复。
- 必须区分任务授权：机器维护、代码修改和文档整理只实施用户当前批准的范围；AUTONOMOUS Research Run 一经创建，即按 `CRL.md` 在 Charter 内自主检索、实验、转向和推进科学版本，无需用户逐步骤或逐版本批准。维护任务不得借用科研自主授权扩张修改范围，科研 Run 也不得把维护 scope 规则误作逐步审批要求。
- 不同 Run 只共享正式论文知识库；禁止跨 Run 读取 Candidate、实验、Decision、Memory、Ledger、失败记录、Reviewer 报告或派生索引。知识库科学内容只读，不得把 Run 内容写回论文、PDF、Evidence、Cards、数据库、Passage 或向量索引。
- 默认宽 `TEXT_AND_TOOL_LLM_AGENT` AUTONOMOUS Research Run 的正常科学终局只有 Delivery。暂未找到合格方向、没有充分去风险的 Seed、候选耗尽、局部方向失败、运行较久或多次验证无效都不构成科学终局；只要授权仍有效且不存在不可越过的真实外部边界，Run 必须保持 `ACTIVE`，继续 backtracking、换题、正交 re-expansion 和验证。只有用户明确给出窄研究方向而创建的 `DIRECTED` Run 才可形成 `CONCLUDED_NO_DELIVERY`。已有历史 No-Delivery（包括 AUTONOMOUS）保持只读解析、审计和用户显式恢复兼容，不迁移、不重写；恢复后的 AUTONOMOUS 版本不得再次写入 No-Delivery。当前资源内若仍有可执行的高信息量实验，其失败会使论文级剩余贡献差分大幅塌缩，则不得靠缩窄 Claim Delivery。frontier 仍存而只是结束执行 episode 时，只有真实外部边界才能形成 `ACTIVE` handoff；用户显式暂停按 `PAUSED_BY_USER` 处理。完整停止条件、实验分层、Reviewer、Delivery 与 No-Delivery 规则只以 `crl_agent_v3/CRL.md` 为权威。
- Diagnosis 读取候选偏好声明时必须保留重复结构字段的出现次数，不得以最后值覆盖；全部 `PAIRWISE_COMPARISON` 按无序候选对归一化并把反向 Pair 的 A/B Verdict 映射到实际候选身份，同对冲突 Verdict 整组为 `AMBIGUOUS` 且不得产生机械胜者或进入实现彩票，相同实际 Verdict 的重复块保留并发 advisory。`A_PREFERRED`/`B_PREFERRED` 只有在 Pair、Verdict、决定性证据、仍存致命不确定性、反转条件和下一区分动作均可解析，且疑似 Run-local 决定性证据均已核验时才产生机械可用胜者；否则只保留 declared Verdict 并报告 `UNKNOWN`。含 `UNVERIFIED EVIDENCE_PATHS` 的 `PREFERENCE_UPDATE` 不参与停滞判断，同一 `ACTION_ID` 与归一化 `AFFECTED_PAIR` 的冲突重复更新整组为 `AMBIGUOUS`。冲突的 `INCUMBENT_SET`/`CHALLENGERS` 不得合并，同次声明把 `EMPTY`、`NONE` 或 `NOT_APPLICABLE` 与候选标识混写时不得保留候选列表。会话标识只属于 `DECLARED_SESSION` 自报事实；`VERIFIED_ARTIFACT` 只表示 Run 边界、普通文件和 SHA-256 已机械核验，相同字节工件只能计一次，脚本不得声称认证了真实会话隔离或科学独立性。
- Research Subagent 仅指 Codex App 原生委派实际创建、可在 App 检查的独立子智能体任务；Reviewer CLI、角色模拟、Python 子进程或 Markdown 文件都不算。未真实委派时不得声称已使用，其材料在主研究者采纳前均非权威。
- 正式 CRL Research Run 不套用通用 research-machine、state-resolver、action-router 或跨 Run memory 工作流形成第二套流程，除非用户明确要求。
- Windows PowerShell 5.1 读取 UTF-8 Markdown 必须显式使用 `Get-Content -Encoding UTF8` 或严格 UTF-8 API；研究文本保存为 UTF-8 无 BOM、LF。
