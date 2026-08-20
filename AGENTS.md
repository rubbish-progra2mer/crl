# CRL 工作区入口

- 与用户交互始终使用中文；不得捏造已阅读文献、已运行命令、实验结果、Reviewer 意见、文件状态或系统能力。
- 用户请求理解、修改、初始化或运行 CRL 时，先阅读 `crl_agent_v3/AGENTS.md`，再完整阅读 `crl_agent_v3/CRL.md`。需要本机实验时再阅读 `crl_agent_v3/CRL_ENVIRONMENT.md`；Reviewer 与文件示例分别按需读取其协议和指南。
- 产品根固定为 `D:\Desktop\crl`，机器根固定为 `D:\Desktop\crl\crl_agent_v3`，共享论文知识库固定为 `D:\Desktop\crl\knowledge_base`；Run 是产品根的直接子目录。环境、运行时与大容量资源位置只以 `CRL_ENVIRONMENT.md` 为准。
- 用户只说“开始运行”时，直接创建 Contract v3 新 Run，由主 AI 研究者在文本与工具型大语言模型智能体领域自主选题；不要求用户补方向，不扫描旧 Run，也不执行机器验收、健康检查或启动测试。用户给出的领域内方向成为更窄 Charter 边界；领域外请求不创建 Run。
- 普通启动不恢复历史 Run。Contract v2 只读、可审计、不可恢复；已终局的 v3 Run 只有在用户明确指定后才核验历史并按 `CRL.md` 处理，`TERMINATED_BY_USER` 永不恢复。
- 必须区分任务授权：机器维护、代码修改和文档整理只实施用户当前批准的范围；AUTONOMOUS Research Run 一经创建，即按 `CRL.md` 在 Charter 内自主检索、实验、转向和推进科学版本，无需用户逐步骤或逐版本批准。维护任务不得借用科研自主授权扩张修改范围，科研 Run 也不得把维护 scope 规则误作逐步审批要求。
- 不同 Run 只共享正式论文知识库；禁止跨 Run 读取 Candidate、实验、Decision、Memory、Ledger、失败记录、Reviewer 报告或派生索引。知识库科学内容只读，不得把 Run 内容写回论文、PDF、Evidence、Cards、数据库、Passage 或向量索引。
- 默认宽 `TEXT_AND_TOOL_LLM_AGENT` AUTONOMOUS Research Run 在没有充分去风险的 Seed 时继续 frontier discovery；经过真实 backtracking、正交 re-expansion 与必要高信息量检查后，主研究者也可把“本次 Run 继续投入的预期科研价值已不足”写成 `CONCLUDED_NO_DELIVERY`，但这不表示领域穷尽。版本数、时长、Token、候选数、检索数或单个负结果不能单独支持该终局，脚本不替代主研究者判断。当前资源内若仍有可执行的高信息量实验，其失败会使论文级剩余贡献差分大幅塌缩，则不得靠缩窄 Claim Delivery。frontier 仍存而只是结束执行 episode 时，只有真实外部边界或用户显式暂停才能形成 `ACTIVE` handoff。完整停止条件、实验分层、Reviewer、Delivery 与 No-Delivery 规则只以 `crl_agent_v3/CRL.md` 为权威。
- Research Subagent 仅指 Codex App 原生委派实际创建、可在 App 检查的独立子智能体任务；Reviewer CLI、角色模拟、Python 子进程或 Markdown 文件都不算。未真实委派时不得声称已使用，其材料在主研究者采纳前均非权威。
- 正式 CRL Research Run 不套用通用 research-machine、state-resolver、action-router 或跨 Run memory 工作流形成第二套流程，除非用户明确要求。
- Windows PowerShell 5.1 读取 UTF-8 Markdown 必须显式使用 `Get-Content -Encoding UTF8` 或严格 UTF-8 API；研究文本保存为 UTF-8 无 BOM、LF。
