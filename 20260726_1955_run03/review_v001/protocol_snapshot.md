# CRL v3 Reviewer Protocol

本文是 CRL 三位 Reviewer 的共同 Packet、独立启动、实际读取、互不可见和落盘纪律的唯一权威。三个角色的职责源文件位于机器目录 `reviewer_roles/`；项目根不建立自定义 Agent 配置。Reviewer 只提供独立意见，主 Codex 保留最终裁决权；不得投票、平均分或自动 PASS。

CRL_AGENT_TOPOLOGY: MAIN_CODEX_PLUS_THREE_LEAF_REVIEWERS_ONLY

REVIEWER_SUBAGENT_DELEGATION: FORBIDDEN

三位 Reviewer 是 CRL 唯一允许出现的 subagent，且必须都是主 Codex 的直接叶子节点。Reviewer 不得调用、创建或委派任何其他 Agent；不得把读取、检索、核验或报告撰写交给第二个上下文。任何违反本条的报告作废，不计入三审。

## 1. 冻结唯一中性 Packet

主 Codex 在启动任何 Reviewer 前，对当前 `vNNN`：

1. 冻结唯一 `review_vNNN/packet.md`，记录绝对路径和 SHA-256；
2. 确认三个正式报告文件均不存在；
3. 把实际使用的共同 Protocol 与 `reviewer_roles/` 三份角色源文件复制为 `review_vNNN/` 内不可覆盖的 snapshots，记录每份路径、byte size 与 SHA-256；
4. 在不可覆盖的 `nearest_prior_vNNN.md` 与来源 snapshots 中预提交主 Codex prior，只把 commitment SHA 放入共同 Packet；
5. 核对 Packet manifest 的每一项 frozen artifact 都真实存在，且 manifest 中的相对路径、byte size 与 SHA-256 对应 `review_vNNN/` 内实际冻结 bytes。

共同 Packet 对三个 Reviewer 完全相同。其 commitment 区绑定共同 Protocol、三个 role snapshots 与主 Codex prior 的 SHA；共同 frozen-artifact manifest 至少逐文件列明当前版本的 Problem、Candidate、Evidence Packet、中性 Research Map、Selection Context、全部科学相关尝试、实现、配置、输入、capture、原始输出、结果，以及每个 comparator 的中性 ID、真实身份、代码/config/bytes/cost。目录名不能代替逐文件清单；失败、中断和负向尝试不得省略。peer role 正文不进入共同 artifact manifest，每位 Reviewer 只读取自己的 role snapshot。

本文所称“同一 Packet”是同一个 `packet.md`、同一共同 manifest 和它列明的全部 frozen scientific artifact bytes。Packet 明确排除主 Codex 的 `nearest_prior_vNNN.md` 正文、search query/log、prior 排序、nearest/closest/current-strongest 标签、collision verdict 和相对差异叙事。Prior Reviewer 的报告冻结后，主 Codex 才能比较两份 prior 结论。

Packet 的复制、哈希和保存继续使用现有 `tools/manage_review.py` / `ResearchWorkspace` 机械内核；调用者必须显式给出当前 Run、版本和全部材料路径。工具不得自动选择 Run、扫描材料、判断准备度或裁决科研结论。

## 2. 三个 fresh default subagent 同时启动

- 主 Codex 在任何 Reviewer 报告返回或落盘前，主动启动三个 `agent_type=default`、`fork_turns=none` 的 fresh subagent；不得使用继承主线程历史的 fork，也不得依赖项目级自定义 Agent 配置。
- 三个 Reviewer 调用均以主 Codex 为直接父节点，禁止任何 Reviewer 再创建 subagent；exact request 必须原样包含 `REVIEWER_SUBAGENT_DELEGATION: FORBIDDEN`。
- 每个 Reviewer 只收到同一 Packet 的绝对路径/SHA、共同 Protocol snapshot 路径/SHA、属于自己的 role snapshot 路径/SHA，以及中性 exact request；不接收其他 Reviewer 报告或主 Codex 私有 prior 正文。
- 三个调用分别承担 Prior and Lineage Attacker、Scientific Skeptic、Implement Potential Reviewer；角色名称不是模型类型，职责只来自本次冻结的 Markdown snapshot。
- Reviewer 把完整原始报告返回主线程；同时**必须**把同一份完整报告逐字写入 exact request 指定的暂存路径（Run 根 `review_vNNN/staging/reviewer_N_staged.md`，非正式槽位）。主 Codex 核对暂存文件与返回文本一致后，用暂存文件作为 `save-report` 的输入，实现机械原样落盘；两者不一致时以返回文本为准并记录差异。Reviewer 不得写入三个正式报告槽位或任何其他工作区文件。（本条为 run02 MD-12 修复：长报告场景下主 Codex 手工转录曾产生披露性压缩，机械通道消除该失真源。）
- Candidate、实验、Selection Context 或其他科学相关 bytes 发生变化时，旧版本保持冻结，必须推进到同一 Run 的下一根部版本并重新冻结 Packet、重新启动三个 fresh subagent。

## 3. 必须实际读取全部 frozen bytes

每位 Reviewer 都必须：

1. 实际打开并阅读 `packet.md`、共同 Protocol snapshot 和自己的 role snapshot；
2. 按 manifest 顺序逐项打开列明的每一个 frozen artifact，核对实际路径、byte size 与 SHA-256；
3. 对文本、代码、配置和原始输出阅读实际内容；对二进制或结构化产物使用能够解释其内容的相应工具读取，不得只查看文件名、摘要、存在性或 manifest；
4. 在报告中逐项回报实际读取的 frozen relative path 与 SHA-256，并列出任何 byte size/SHA 不符、不可读或语义无法解释的材料。

只要 manifest 中有一项未实际读取、缺失或哈希不符，该 Reviewer 就不能声称完成审查；必须把报告标为不完整并说明受影响判断。主 Codex 不得把不完整报告计入三审，须修复 Packet 或重新调用 fresh Reviewer。公开来源全文不可得等 Packet 外部限制可以标 `unresolved`，但不能用来豁免共同 Packet 的实际读取。

Protocol 不要求 OS allowlist、文件访问轨迹或额外 ACL 系统；实际读取纪律由 Reviewer 的逐项 readback 和主 Codex 对报告的核验保证。

## 4. “独立”的运行含义

必须同时满足：

1. `agent_type=default` 且 `fork_turns=none` 的 fresh context；
2. 三份不同角色 snapshot；
3. 同一中性 Packet 及其全部 frozen bytes；
4. peer reports 互不可见；
5. 主 Codex prior 在启动前预提交且未进入 Packet。

若 Reviewer 继承主线程科研推理历史、提前读取 peer report 或私有 prior 正文，本轮对应报告作废，必须以 fresh context 重做。

## 5. 每次调用保存的最小 provenance

每位 Reviewer 的 `reviewer_instructions` 原样保存：

- exact request；
- task/subagent ID；
- Packet path/SHA；
- role snapshot path/SHA；
- common Protocol snapshot path/SHA；
- Reviewer 回报的逐项 frozen-artifact path/SHA readback；
- 可取得时记录工具、联网使用和模型信息；不可见字段如实写不可见。

这些事实写入现有 Reviewer 报告记录，不另建 invocation 数据库或 Reviewer 管理系统。

## 6. 统一报告合同

每份原始报告必须包含：

1. Packet 与全部 frozen artifacts 的逐项实际读取回报；
2. 材料完整性与未解决限制；
3. 最强支持；
4. 致命异议；
5. 可修复异议；
6. 当前证据最多支持的 Claim；
7. 绝不能支持的 Claim；
8. 建议处置及证据理由；
9. 实际用于判断的公开来源、URL/version、SHA 与 locator。

不得输出总分、票数或自动 PASS 标签。全文不可得或方法身份不清时必须标 `unresolved`，不能依据摘要作无碰撞或正向结论。

## 7. 返回、落盘与主 Codex 裁决

三个完整报告全部返回前，不写入任何正式 `reviewer_*.md`。全部返回后，主 Codex 使用现有 `write_reviewer_report()` / `tools/manage_review.py save-report` 将三份原始文本分别原样保存到 `review_vNNN/reviewer_1.md`、`reviewer_2.md`、`reviewer_3.md`；不摘要、不合并、不让后一个覆盖前一个。

主 Codex 随后完整阅读同一 Packet、全部 frozen artifacts、三份报告及其引用依据，逐项处置每个可信异议，并把裁决保存为根部 `decision_vNNN.md`。任何未解决的可信致命异议都阻止该版本 Delivery；另外两份意见不能以票数覆盖它。

候选版本被否定只产生该版本的冻结 Decision 与同 Run 经验记录，不终止 Run，也不改变机器 commissioning 状态。主 Codex继续探索时推进到 `vNNN+1`；只有根部 `DELIVERY.md` 生成并绑定获批版本的实现、实验、三审和 Decision SHA 后，Run 才能进入 `DELIVERED`。
