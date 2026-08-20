# P012 主 Codex 首读

- PDF：`knowledge_base/staging/papers/P012_reflexion.pdf`
- PDF SHA-256：`efba04cd48b779131fc4c3c58ae49e8523ded534f9225a7c57c7bdad0823803d`
- 读取时间：`2026-07-19T15:38:00+08:00`
- 读取范围：逐页检查 1–19 页；正文 1–9 页，参考文献 9–11 页，跨模型结果 12 页，decision/programming/reasoning prompts、失败案例与 ablations 13–19 页。

## Changed computation / 方法对象

- [AUTHOR_FACT] Reflexion 不更新模型权重；Actor 生成 trajectory，Evaluator 产生 binary/scalar/语言 signal，Self-Reflection LLM 将 trajectory+signal 转成 verbal experience，追加到最多 1–3 条的 episodic memory，下一次对同一 task retry 时作为额外 context。
- [AUTHOR_FACT] Evaluator 的信息随任务不同：ALFWorld 用 environment completion 加 hand-written loop/30-action heuristic 或 LLM classifier；HotPotQA 用 exact-match gold grading；programming 用最多 6 个 self-generated tests 的实际执行结果。
- [READER_INTERPRETATION] Changed computation 是“把失败轨迹压缩为可执行的下一试次策略提示并持久化”，而不是 reflection 文字本身。反馈是否 grounding、任务是否可重置、是否允许多次同题尝试是机制成立的关键条件。

## 输入、基线与预算边界

- ALFWorld 对 134 environments 反复重置同一 task，ReAct-only baseline 也在触发 self-evaluation 后重置重试，但跳过 reflection；memory 保存最近 3 条。最多 12 iterative trials，累计 solved proportion 随试次报告。
- HotPotQA 仅 100 questions；CoT 是 6-shot、ReAct 2-shot、reflection 2-shot，temperature 0.7。失败任务可重复到连续 3 次失败；CoT(GT) 直接获得 ground-truth supporting context，exact match 只给 correct/incorrect，不给 gold answer。
- Programming 的 baseline 是一次 generation；Reflexion 先自生测试、执行、reflection、改代码，memory 1 条。作者称 pass@1 eligibility，理由是未访问 hidden tests；但它消耗多次模型调用与最多 6 个自生 tests，不是同 test-time compute 的单次生成比较。
- 最近组合 baseline 包括 previous trajectory only 的 episodic memory (EPM)、test execution without reflection、reflection without tests。HumanEval Rust ablation：base .60，reflection without test .52，test without reflection .60，full .68，支持 grounded feedback 与 verbal bridge 的互补。

## 主要结果与严格解释

- ALFWorld：正文称相对 strong baseline 在 12 次内 absolute +22%，cumulative curve 接近 1.0；这是“给同一环境多次 retry 后解出”的累计成功，不是首次轨迹 accuracy，也不证明跨新 task 学习。
- HotPotQA：Reflexion 改善 CoT/ReAct；CoT(GT) 在有 gold context 仍有 39% 首次错误，reflection 后 +14%；EPM ablation 显示 reflection 比仅附上 previous trajectory 再高 8 points。由于 exact-match feedback 对同一题重复，收益是 test-time correction。
- HumanEval Python Table 1：GPT-4 single generation .801、Reflexion .910；MBPP Python 反而 .801→.771。Table 2 显示 MBPP internal-test false-positive .16 而 HumanEval .01，是 method 负向结果而非普遍 code gain。
- Additional Table 4：StarChat-beta baseline 与 Reflexion 都 .26（8 trials average），弱模型完全无提升；作者明确称可指定 self-corrections 是更强/更大模型的 emergent quality。
- WebShop Appendix：100 requests、仅四 trials 后停止，ReAct+Reflexion 不显著优于 ReAct；self-reflections 不够有用，作者归因为逃离 local minima 需要更多 diversity/exploration。
- Table 5 跨 backbone HotPotQA 都提升，但 absolute 起点和终点显著不同；结果支持条件性的机制可迁移，不支持“模型越强 reflection 总会可靠”。

## 失败边界与限制

- [AUTHOR_FACT] Self-generated tests 会产生 false positive（错程序通过，提前错误提交）和 false negative（对程序被误判，触发有害修改）；作者认为 FP 更危险，MBPP 的 .163 FP 对应总体倒退。
- [AUTHOR_FACT] 无 grounded test 时 forcing reflection 使 HumanEval Rust .60→.52；self-reflection 不能替代可靠 evaluator。
- [AUTHOR_FACT] WebShop 的 ambiguous search/local minima 下 reflection 不产生新探索，四次内没有显著收益；文本总结失败不等于产生策略多样性。
- [AUTHOR_FACT] 长期 memory 仅 sliding window 1–3 experiences，论文未处理跨任务积累、错误 reflection 遗忘、冲突经验检索或容量扩展。
- [AUTHOR_FACT] 作者明示 policy optimization 仍可陷入非最优 local minima，没有成功形式保证；code 还受 nondeterminism、API/impure functions、hardware-dependent 或 concurrency tests 限制。
- [READER_INTERPRETATION] HotPotQA/ALFWorld 的“learning”发生在同一 evaluation instance 的重复尝试，binary oracle 持续告知答案/trajectory 是否成功；不可外推为无反馈部署中的 intrinsic self-correction，也不可把累计 trials 与一次性 baseline 混称 pass@1。
- [READER_INTERPRETATION] Reflection memory 增加 prompt tokens、LLM calls 与 retry budget；论文没有严格等 token/call 的 search/self-consistency baseline。提升可能来自结构化使用额外 compute，机制价值仍需在等预算下验证。
- [READER_INTERPRETATION] Algorithm 1 写作 `while Me not pass or t < max trials`，按字面 OR 会在已 pass 时仍循环且在未 pass、超过 max 时可能不终止；正文意图明显是“未通过且未超预算”。这是论文伪代码逻辑冲突，Card 不应照抄。

## 可抽取候选（尚非正式 Card）

- Operator：`Grounded Failure-to-Action Verbal Memory`——把可验证 evaluator signal 与失败 trajectory 压缩为下一次同任务可执行的策略修正，作为有限 episodic context 注入 Actor。
- Operator：`Trajectory Compression Before Retry`——相对直接塞入上一 trajectory，用第一人称 error attribution/next-action plan 减少长轨迹噪声；必须保留 feedback provenance。
- Failure：`Ungrounded Reflection Causes Harmful Edits`——没有真实 tests/environment signal 时，reflection 迫使正确输出被重写并低于 baseline。
- Failure：`False-Positive Self-Test Prematurely Accepts Wrong Program`——self-generated evaluator 漏检使错误实现提前停止，且 reflection 无机会修复。
- Failure：`Reflection Cannot Escape Exploration-Poor Local Minima`——语言总结复述失败，却不产生足够不同的搜索行为，WebShop 无显著收益。
- Failure：`Weak Backbone Cannot Operationalize Reflection`——StarChat-beta 无增益，memory 中写有建议不等于 Actor 能执行。

## 未解决问题

- `[OPEN_QUESTION]` 各方法的总 LLM calls、tokens、wall time 与同等 compute best-of-N/self-consistency 未报告。
- `[OPEN_QUESTION]` ALFWorld/HotPotQA curves 的随机重复、置信区间及 100-question sampling variance 不充分。
- `[OPEN_QUESTION]` HotPotQA 的 repeated exact-match signal 是否允许模型通过答案空间试探而非真正改进 reasoning，论文未做诊断。
- `[OPEN_QUESTION]` “pass@1”在内部多轮生成/测试条件下与社区单样本 pass@1 的可比口径有争议，需在正式 Card 中显式限定。
