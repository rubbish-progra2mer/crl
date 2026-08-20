# P001 主 Codex 首读

- PDF：`knowledge_base/staging/papers/P001_react.pdf`
- PDF SHA-256：`f285b0971ae4a790e402fb93966bed3adde2cf0a04977d08b2b40d6ab0cace69`
- 读取时间：`2026-07-19T15:08:00+08:00`
- 读取范围：逐页检查 1–33 页；正文 1–10 页，参考文献 10–13 页，附加结果/实验细节 14–15 页，完整 prompts/trajectories 16–31 页，失败例 32–33 页。第 2、14、15 页部分图中文字字体映射异常，但正文 caption 与相邻文本可读；裁决不依赖乱码图中文字。

## Changed computation

- [AUTHOR_FACT] 第 3 页 §2 将外部动作空间 `A` 扩为 `A ∪ L`：语言 thought 不改变环境、没有 observation，却写回上下文，后续 thought/action 均以更新后的上下文为条件。
- [AUTHOR_FACT] 第 3–4 页区分两种调度：知识推理任务交替生成 thought/action/observation；长程交互任务由模型稀疏、异步决定何时 thought。
- [READER_INTERPRETATION] 机制不是“多写一段 CoT”，而是在同一决策轨迹中让内部语言状态和真实环境观测循环互相改变下一动作；可迁移核心是 interleaved state update，Wikipedia/ALFWorld/WebShop 是载体。

## Baseline、预算与公平性

- 第 5 页 §3.2 从同一 ReAct exemplars 系统消融出 Standard、CoT、Act；CoT-SC 额外用温度 0.7 采样 21 条并投票。ReAct 与 Act 的示例来源相同，但一个保留 thought、一个移除 thought。
- HotpotQA/FEVER 主模型为 PaLM-540B；ReAct 设 7/5 步上限，作者称继续增加不改善（第 5 页脚注）。混合方法会在失败/低多数置信时调用 CoT-SC，因此不能把混合方法提升归因给纯 ReAct。
- ALFWorld 每任务人工标注 3 条轨迹，并用其中 2 条的 6 种排列评估；报告 `best of 6` 与平均值。Act 使用同轨迹去除 thought，是较强的局部公平对照；BUTLER 使用不同训练/解码设置（第 7–8 页）。
- WebShop 是 one-shot prompt；IL/IL+RL 使用 1,012 人工轨迹/10,587 指令，训练资源不可直接等同（第 7–8 页）。
- 附录 B.1（第 15 页）显示微调步数并不完全相同：ReAct/Act 4,000 步，Standard/CoT 1,000–2,000 步，因为后两者随后退化。微调结果不是严格等训练计算对比。

## 主要结果与定位

- 表 1，第 5 页：HotpotQA EM ReAct 27.4、CoT 29.4；FEVER Acc ReAct 60.9、CoT 56.3。纯 ReAct 并非所有任务都优于 CoT。
- 表 2，第 6 页：人工检查 200 个样例；CoT 错误中的 hallucination 56%，ReAct 错误中 reasoning error 47%、search result error 23%；作者明确把 groundedness 与推理灵活性视为权衡。
- 表 3，第 8 页：ALFWorld ReAct 平均 57、best-of-6 71；Act best-of-6 45；ReAct-IM best 53。表 4：WebShop success rate ReAct 40.0、Act 30.1、IL+RL 28.7、人类 59.6。
- 图 3/第 6–7 页：用各自生成的 3,000 条正确轨迹微调后，小 PaLM 的 ReAct 提升明显；这同时包含数据筛选、轨迹格式与训练的贡献。
- 附录 A.1 第 14 页只在 HotpotQA 500 子集和 ALFWorld 上补 GPT-3，支持跨两个基座的有限复现，不支持广泛模型不变性。

## 失败边界与限制

- [AUTHOR_FACT] 第 6 页：结构约束降低灵活性，出现重复 thought/action 循环；无信息检索会使后续推理难以恢复。第 33 页给出 search error 例。
- [AUTHOR_FACT] 第 8 页：WebShop 仍显著低于人类，产品探索与 query reformulation 是困难点。
- [AUTHOR_FACT] 第 9–10 页：复杂大动作空间需要更多 demonstrations，但受上下文长度限制；PaLM 不公开，复现依赖 GPT-3 补充与公开 prompts。
- [AUTHOR_FACT] 第 10 页 ethics：研究环境动作被限制；不能从该实验外推开放工具环境的安全性。
- [READER_INTERPRETATION] 方法对 tool observation 质量、终止规则、prompt 示例与大模型先验敏感；“可解释/可信”主要由轨迹可见性与小规模人工分析支持，不等于忠实因果解释。

## 可抽取候选（尚非正式 Card）

- Operator：`Interleaved Reason–Act Context Update`——把语言 thought 作为不触发环境的内部动作，与真实 action/observation 交替写回状态。
- Failure：`Ungrounded or Unrecoverable Interleaving`——检索为空/错误会污染后续推理；固定 thought-action 结构会循环且难恢复。
- Failure：`Best-of-Prompt and Extra-Compute Confound`——best-of-6、CoT-SC 21 samples、混合 fallback 与纯方法成本不同，不能只看最好分数。

## 未解决问题

- `[OPEN_QUESTION]` 论文没有严格等 token/tool-call 的 ReAct vs CoT/Act 总成本表。
- `[OPEN_QUESTION]` thought 是否忠实反映内部决策因果，而非可读事后文本，原文未验证。
- `[OPEN_QUESTION]` 第 2、14、15 页图中文字解析异常；其 caption/正文足够支撑上述事实，但若未来引用图内具体动作文本，应视觉复核原页。
