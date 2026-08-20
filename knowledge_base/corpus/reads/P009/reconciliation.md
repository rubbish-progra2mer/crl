# P009 三读 reconciliation

## 1. 来源与全部尝试绑定

- PDF：`knowledge_base/staging/papers/P009_memgpt.pdf`；SHA-256：`9f674bcff69c86f11c813dcfad613d8841f5f8ed17979e3c4df06a91df7762e0`
- 主 Codex 首读：`knowledge_base/pilot/reads/P009/read_1.md`；SHA-256：`10f2feb34bc8950bd12871a60f1d1c4fe8865cc141956025a48ae312392fec4e`
- 二读 `r2-20260719-p009-a1`：`ACCEPTED`。Invocation：`knowledge_base/pilot/reads/P009/read_2_attempts/r2-20260719-p009-a1/invocation.md`；SHA-256：`75714e51dec1c9ba5374dc4f0af628491abdf1da55a7c9654f7cf5dd6bca1442`。Report：`knowledge_base/pilot/reads/P009/read_2_attempts/r2-20260719-p009-a1/report.md`；SHA-256：`87aa5ada6e4563c70dcec3b136fab8e0e66ab259e351ca85773835e8ab955db3`。
- 第三读 `r3-20260719-p009-a1`：`ACCEPTED`；触发原因是 MemGPT 是分层 agent memory 的唯一直接祖先。Invocation：`knowledge_base/pilot/reads/P009/read_3_attempts/r3-20260719-p009-a1/invocation.md`；SHA-256：`67eaea21cb148a7380ad7590f366c23546f5c77785bb1ec6cc806b4b771c4c3c`。Report：`knowledge_base/pilot/reads/P009/read_3_attempts/r3-20260719-p009-a1/report.md`；SHA-256：`7b2491b23b1116830a58fd6d770ccbace7bef1f62035c6941cdb4d0c2c812493`。
- 其他 attempts：无。独立读者均为 `procedural_blinding`，声明未读前读/Cards/其他报告/blind query。

## 2. 七类逐项裁决

### Changed computation — `AGREE`

三读一致：MemGPT 在固定 context LLM 外增加分层存储与事件控制流。主上下文含只读 system、可写 working context、FIFO queue；外部 recall 保存所有消息、archival 存文档。70% warning/100% flush 示例触发 pressure message、驱逐与递归摘要；LLM通过 function calls编辑/检索并可 heartbeat 连续执行。核点：PDF pp.2–4 §2/Figures 1–3。

### Baseline — `AGREE`

DMR baseline 只看前五段的 lossy summary，MemGPT可搜完整历史；Document QA baseline一次接收 top-K/截断文档，MemGPT可多次查询完整 archive；Nested KV baseline把全部140对直接放 context。因可用信息/调用次数不对称，这些是系统级比较而非单组件消融。核点：PDF pp.5–8、11–13。

### 公平性与预算 — `AGREE`

Document QA prompt 告知答案一定在 archive 并要求继续搜，baseline找不到则输出不足；未配平 tool calls、retrieved tokens、latency/cost。DMR双方 prompt/信息不同，最终 Accuracy 用 generous LLM judge，未做人类一致性/敏感性。Conversation opener以 embedding similarity 衡量，且无清晰固定-context对照。核点：PDF pp.5–7、11–13。

### 主要结果 — `AGREE`

DMR Table 2 baseline→MemGPT accuracy：GPT-3.5 38.7→66.9，GPT-4 32.1→92.5，GPT-4 Turbo 35.3→93.4；只支持完整历史可控检索优于其有损 summary baseline。Document QA曲线无逐点表，Nested KV 是合成查找；不从图估造精确数字。核点：PDF pp.5–8 Tables/Figures 2/5/7。

### Limitation — `AGREE`

MemGPT会在耗尽 archive 前停止；GPT-3.5/function-calling较弱时退化；prompts 是为 brevity 编辑版；未给等检索 baseline、组件消融、完整成本、规模曲线、开源模型、安全/隐私/poisoning/删除。Warning/flush/eviction 只是示例参数，无消融。核点：PDF pp.6–8、11–13。

### Operator — `AGREE`

Pilot 抽取 `Event-Driven Hierarchical Context Paging`：token pressure 与模型函数调用共同决定 working/FIFO/recall/archive 之间的写入、驱逐、分页检索和继续执行。强调“LLM参与 memory policy”，不是向量库同义词。

### Failure — `AGREE`

Pilot 抽取 `Agent-Controlled Retrieval Stops Before Evidence Exhaustion`：gold 可在 archive 中但 agent 提前停止翻页/检索，失败来自 stopping/control policy而非仅 retriever recall。适用条件限于本文 Document QA 与 prompts。

## 3. 未解决项与准入裁决

- `UNRESOLVED`：无阻断项。
- Open limits：完整 implementation prompts、等调用普通 RAG、judge人工校准、endpoint差异和大规模成本均未解决。
- CORE disposition：`ACCEPT`。三读确认 memory 祖先机制及 control-policy failure。
- Task 5 计划：1 个 Operator Card、1 个 Failure Card、1 个 Paper Card；先建立 Evidence。
