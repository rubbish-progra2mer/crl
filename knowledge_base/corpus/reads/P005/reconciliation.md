# P005 双读 reconciliation

## 1. 来源与尝试绑定

- PDF：`knowledge_base/staging/papers/P005_toolllm.pdf`；SHA-256：`76f7d1a6acd0c8d86d0bd41340dd12976643b9bbcaed3008a2357ef2d492ff8a`
- 主 Codex 首读：`knowledge_base/pilot/reads/P005/read_1.md`；SHA-256：`86b9ef1728b19d8e40fec0cb526d760c92270bda1dc56d5a253ebb2c8806b514`
- 二读 `r2-20260719-p005-a1`：`ACCEPTED`。Invocation：`knowledge_base/pilot/reads/P005/read_2_attempts/r2-20260719-p005-a1/invocation.md`；SHA-256：`884c11f55a87ea937630155a0e73010fe50b77b052c41a3839687651bff3ac7e`。Report：`knowledge_base/pilot/reads/P005/read_2_attempts/r2-20260719-p005-a1/report.md`；SHA-256：`9c4e534932fc243ab6aede5b7e9375ddcf89813b58272553e70d6d0a655e2711`。
- 其他二读 attempts：无。第三读 attempts：无；本文不是唯一机制祖先，计划不超过两个 Operator/Failure Cards，两读对关键计算、oracle、预算和主结果无冲突，视觉核查无实质解析冲突。
- 独立性：`procedural_blinding`；二读者声明未读取项目首读/Cards/其他报告/blind query。其系统要求读取的两份非项目技能说明不含 P005 结论，不构成科研输入污染。

## 2. 七类逐项裁决

### Changed computation — `AGREE`

两读一致：ToolLLM 是数据/训练/检索/评估组合；最小且清晰的推理 changed computation 是 DFSDT 将不可撤回的 ReAct 单路径改为显式 give-up、回到分叉状态、把旧子动作放入上下文并要求生成不同分支的 preorder DFS。无回撤时退化为 ReAct。核点：PDF pp.5–6 Figure 4/§2.3、pp.13–14 §A.4、pp.22–23 §A.8。

### Baseline — `AGREE`

DFSDT 的最接近控制是同总 API 成本的 ReAct@N；Table 3 为 35.3/44.5/63.8（ReAct/ReAct@N/DFSDT average pass）。模型能力对照中 GPT-4+DFSDT 最强，不能把 ToolLLaMA 表述为全面最优；APIBench 上 Gorilla-RS+Oracle 亦更强。核点：PDF pp.7–9 Tables 3–5。

### 公平性与预算 — `AGREE`

主表除 retriever 版本外使用 generator 给出的 oracle API 集；Table 4 未逐模型统一/报告 token、tool call、分支深度、函数序列化与上下文预算；ReAct@N 只提供 ChatGPT 总成本近似对照。数据生成、路径标注、训练教师与 ToolEval 均高度依赖 ChatGPT，形成同源风格/偏好可能性。核点：PDF pp.6–8、13–15。

### 主要结果 — `AGREE`

两读的 Table 4 数字一致：GPT-4+DFSDT average pass 71.1，ToolLLaMA+DFSDT 66.7，Retriever 67.3，ChatGPT+DFSDT 64.8。该结果是在特定 ToolBench、ToolEval、API 条件下，不能等同于从 16k API 端到端发现并完成请求。Table 2 的高检索 NDCG 还受不完备 relevance 标签约束。核点：PDF pp.7–9。

### Limitation — `AGREE`

两读一致记录 RapidAPI 时变、只保留通过轨迹、长 response schema 压缩/1024-token 截断、自动评估人机非完全一致、无统一非 ChatGPT evaluator，以及真实用户分布/长期漂移/副作用未测。核点：PDF pp.4–6、13–16。

### Operator — `RESOLVED_BY_SOURCE`

二读列出完整系统多个环节；为避免把平台组件全部 Card 化，Pilot 只抽取 `Explicit Give-Up Backtracking with Sibling-Aware Resampling`：输入当前轨迹和已试子动作，失败时回撤，输出与旧子动作不同的新 action 分支，成功即停。API retriever、response compression 和 evaluator 只留在 Paper Card 的来源上下文。

### Failure — `RESOLVED_BY_SOURCE`

Pilot 只抽取一个直接有来源边界的 Failure：`Evaluator-Defined Refusal/Exploration as Apparent Success`。ToolEval 在特定可解/不可解条件会把充分尝试后的 give-up/refusal 计为 Pass，Win 又偏好尝试更多有用 API；因此 headline pass/win 不总等于请求完成/答案正确。核点：PDF pp.14–15 §A.5。成功路径选择、oracle API 和计算预算作为 Paper Card 限制，不另膨胀 Failure Cards。

## 3. 未解决项与准入裁决

- `UNRESOLVED`：无阻断项。
- Open limits：等成本的 token/tool-call/latency 明细、response compression 误删率、独立 evaluator 主结果均未报告；按来源未覆盖事实保留。
- CORE disposition：`ACCEPT`。DFSDT 提供清晰控制流 Operator，ToolEval/Oracle 设计提供重要负向知识；窄主张不依赖未解决外推。
- Task 5 计划：1 个 Operator Card、1 个 Failure Card、1 个 Paper Card；所有事实先创建页码级 Evidence。
