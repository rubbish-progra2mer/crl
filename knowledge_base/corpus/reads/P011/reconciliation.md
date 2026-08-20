# P011 双读 reconciliation

## 1. 来源与尝试绑定

- PDF：`knowledge_base/staging/papers/P011_secom.pdf`；SHA-256：`998ab05ece554a83870b1baf5762f314837165e99f22ef2af8ffd7ba473c5004`
- 主 Codex 首读：`knowledge_base/pilot/reads/P011/read_1.md`；SHA-256：`34c5a06ef4fbf7dfc70ec28ed59d9a9653e1868b947624934383ef8b4529b194`
- 二读 `r2-20260719-p011-a1`：`ACCEPTED`。Invocation：`knowledge_base/pilot/reads/P011/read_2_attempts/r2-20260719-p011-a1/invocation.md`；SHA-256：`14bb82d2030cc72dbe30f4b85ce94e9b3b645806acd64ac7a26ddf54c8d9c894`。Report：`knowledge_base/pilot/reads/P011/read_2_attempts/r2-20260719-p011-a1/report.md`；SHA-256：`1da5dddbb41ecd0d776c819b56d3d31a2f782ce0ba320e5ae5884fbd4bd3de7a`。
- 其他二读 attempts：无。第三读 attempts：无；本文不是唯一机制祖先/强 baseline，计划不超过两个 Operator/Failure Cards；两读无关键分歧或解析冲突。
- 独立性：`procedural_blinding`；二读者声明未读取首读、Cards、其他报告或 blind query。

## 2. 七类逐项裁决

### Changed computation — `AGREE`

两读一致：SECOM 把 turn/session 固定 memory unit 改为连续、主题一致的 segment，并在检索前用 LLMLingua-2 压缩 unit；响应端在 token budget 内按时间拼接检索结果。主表 turn/session baseline 也使用 denoising，故 segment 差异主要测 granularity；Table 2 才测 compression 边际。核点：PDF pp.4–8 §2–3、Eqs.1–2、Tables 1–2。

### Baseline — `AGREE`

LOCOMO 最强简单粒度 baseline 是 BM25 turn，外部方法中 ConditionMem；Long-MT-Bench+ 最强简单粒度是 MPNet turn，外部方法是 MemoChat。Official LOCOMO 的 SECOM 对最强 turn margin 只有 2.69/1.25，需与原 GPT-4-generated QA 主表区分。核点：PDF pp.6、18 Tables 1/6。

### 公平性与预算 — `AGREE`

主表标称 LOCOMO/Long-MT-Bench+ 4k/1k token budget，但不可切分 session 实际可超 1k；外部 baseline 的 memory construction、training、tokens 不同。问答生成、judge、segmentation 都涉及 GPT-4，共享模型族偏好未系统分析。无 CI/显著性/多 seed，离线 segmentation cost 也未完整摊销。核点：PDF pp.5–6、15、18–22。

### 主要结果 — `AGREE`

LOCOMO BM25+GPT4-Seg 71.57 vs denoised turn 65.58；Long-MT-Bench+ MPNet 为 88.81 vs turn 84.91。去 denoise 的下降在两数据集为 9.46 与 1.30，说明 compression 收益不稳定同量级。RoBERTa-Seg 可低于 turn/MemoChat，表明分割器能力是组成因素。核点：PDF pp.6–8、22 Tables 1–2/11。

### Limitation — `AGREE`

75% compression 未做人评事实保真，尤其数字/否定/时间；GPT-4 分割会过切；Long-MT-Bench+ 是重构合成 benchmark；在线更新、冲突、删除、安全注入和真实用户长期使用均未测；人评盲法/一致率不完整。核点：PDF pp.20–26。

### Operator — `RESOLVED_BY_SOURCE`

Pilot 只抽取 `Topically Coherent Contiguous Memory Segmentation`：在 turn 碎片与 session 多 topic 噪声之间改变 retrieval unit。Compression 是配套干预与边界，不另拆正式 Operator Card，以保持最小 Pilot。

### Failure — `RESOLVED_BY_SOURCE`

Pilot 只抽取 `Retrieval Granularity Fragmentation–Noise Tradeoff`：turn 可拆散依赖证据/丢关键词，session 可混入无关 topic；附录案例直接展示两侧失败。过切、压缩信息损失和 JSON 格式失败保留在 Paper Card。

## 3. 未解决项与准入裁决

- `UNRESOLVED`：无阻断项。
- Open limits：主表 1k budget 对不可切分 session 的执行口径、compression 事实保持率、跨 session topic 维护和 judge-vs-human 一致性未解决。
- Canonical title note：PDF 首页题名为 *On Memory Construction and Retrieval for Personalized Conversational Agents*；admission 中 `SeCom` 是方法简称/映射，不应替代 manifest 的原始标题字段。
- CORE disposition：`ACCEPT`。提供清晰 granularity Operator 和双侧失败证据。
- Task 5 计划：1 个 Operator Card、1 个 Failure Card、1 个 Paper Card；先创建 Evidence。
